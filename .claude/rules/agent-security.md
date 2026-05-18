# Agent Security - Core Security Rules

Security rules for agentic AI systems that perform autonomous actions, use tools, and execute multi-step tasks.
Source: https://github.com/TikiTribe/claude-secure-coding-rules (MIT)

**Standards**: OWASP LLM Top 10, NIST AI RMF, Google SAIF

---

## Tool Use Security

### Rule: Validate Tool Calls Before Execution

**Level**: `strict`

**When**: Agent selects and invokes tools based on LLM reasoning.

**Do**:

```python
from pydantic import BaseModel, validator
from typing import Any

class ToolCall(BaseModel):
    tool_name: str
    parameters: dict

    @validator('tool_name')
    def validate_tool_name(cls, v):
        allowed_tools = ['read_file', 'write_file', 'search', 'calculate']
        if v not in allowed_tools:
            raise ValueError(f"Tool '{v}' not in allowlist")
        return v

class SecureToolExecutor:
    def __init__(self, tools: dict, permission_checker):
        self.tools = tools
        self.permission_checker = permission_checker

    def execute(self, tool_call: ToolCall, context: dict) -> Any:
        if tool_call.tool_name not in self.tools:
            raise ToolNotFoundError(f"Unknown tool: {tool_call.tool_name}")
        tool = self.tools[tool_call.tool_name]
        if not self.permission_checker.can_execute(
            user=context['user'], tool=tool_call.tool_name, params=tool_call.parameters
        ):
            raise PermissionError(f"Not authorized for {tool_call.tool_name}")
        validated_params = tool.validate_params(tool_call.parameters)
        audit_logger.info("Tool execution", extra={
            'tool': tool_call.tool_name,
            'params': self._sanitize_for_log(validated_params),
            'user': context['user'].id
        })
        return self._execute_sandboxed(tool, validated_params, context)
```

**Don't**:

```python
# VULNERABLE: Direct execution without validation
def execute_tool(tool_name, params):
    return tools[tool_name](**params)

# VULNERABLE: No permission checks
def agent_action(llm_output):
    tool_call = parse_tool_call(llm_output)
    return globals()[tool_call['name']](**tool_call['params'])
```

**Why**: Compromised or manipulated agents can invoke dangerous tools. Validation prevents
unauthorized actions and parameter injection.

**Refs**: OWASP LLM07 (Insecure Plugin Design), NIST AI RMF MANAGE 1.3, MITRE ATLAS AML.T0051

---

### Rule: Implement Tool Permission Boundaries

**Level**: `strict`

**When**: Defining what tools an agent can access and under what conditions.

**Do**:

```python
import os
from enum import Enum

class PermissionLevel(Enum):
    READ = "read"
    WRITE = "write"
    EXECUTE = "execute"

class ToolPermissionPolicy:
    def __init__(self):
        self.tool_permissions = {
            'read_file': {
                'required_level': PermissionLevel.READ,
                'allowed_paths': ['/data/', '/config/'],
                'blocked_paths': ['/secrets/', '/credentials/'],
            },
            'write_file': {
                'required_level': PermissionLevel.WRITE,
                'allowed_paths': ['/output/', '/tmp/'],
                'blocked_paths': ['/system/', '/etc/'],
                'require_confirmation': True,
            },
        }

    def check_permission(self, user, tool_name: str, params: dict) -> bool:
        policy = self.tool_permissions.get(tool_name)
        if not policy:
            return False
        if not user.has_permission(policy['required_level']):
            return False
        if tool_name == 'read_file':
            return self._check_file_access(params.get('path'), policy)
        return True

    def _check_file_access(self, path: str, policy: dict) -> bool:
        normalized = os.path.normpath(path)
        for blocked in policy['blocked_paths']:
            if normalized.startswith(blocked):
                return False
        for allowed in policy['allowed_paths']:
            if normalized.startswith(allowed):
                return True
        return False
```

**Don't**:

```python
def can_use_tool(tool_name):
    return True              # VULNERABLE: no permission boundaries

allowed_paths = ['/']        # VULNERABLE: full filesystem access
```

**Why**: Principle of least privilege limits damage from compromised agents.

**Refs**: NIST AI RMF GOVERN 1.2, ISO/IEC 23894 A.1, OWASP A01:2025

---

## Code Execution Security

### Rule: Sandbox Agent-Generated Code

**Level**: `strict`

**When**: Agent generates and executes code as part of its tasks.

**Do**:

```python
import ast
from RestrictedPython import compile_restricted, safe_builtins

class CodeSandbox:
    BLOCKED_NAMES = {'eval', 'exec', 'compile', 'open', 'input',
                     '__import__', 'globals', 'locals', 'vars'}

    def validate_code(self, code: str) -> bool:
        try:
            tree = ast.parse(code)
        except SyntaxError as e:
            raise CodeValidationError(f"Syntax error: {e}")
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                if hasattr(node.func, 'id') and node.func.id in self.BLOCKED_NAMES:
                    raise CodeValidationError(f"Blocked function: {node.func.id}")
            if isinstance(node, (ast.Import, ast.ImportFrom)):
                raise CodeValidationError("Imports not allowed in sandbox")
        return True

    def execute(self, code: str, local_vars: dict = None) -> dict:
        self.validate_code(code)
        byte_code = compile_restricted(code, filename='<agent_code>', mode='exec')
        restricted_globals = {
            '__builtins__': safe_builtins,
            '_print_': lambda x: None,
        }
        local_namespace = local_vars or {}
        exec(byte_code, restricted_globals, local_namespace)
        return local_namespace
```

**Don't**:

```python
def run_agent_code(code):
    exec(code)                          # VULNERABLE: arbitrary system access

result = eval(agent_generated_expression)  # VULNERABLE
```

**Why**: Unrestricted code execution allows arbitrary system access.

**Refs**: OWASP LLM06 (Excessive Agency), CWE-94, NIST SSDF PW.5.1

---

### Rule: Limit Agent Autonomy Scope

**Level**: `strict`

**When**: Configuring how much autonomous action an agent can take.

**Do**:

```python
from enum import IntEnum

class AutonomyLevel(IntEnum):
    SUGGEST = 1      # Only suggest — human executes
    CONFIRM = 2      # Execute after human confirmation
    BOUNDED = 3      # Execute within strict limits automatically
    SUPERVISED = 4   # Execute with monitoring
    AUTONOMOUS = 5   # Full autonomy (rarely appropriate)

class AgentAutonomyController:
    def __init__(self, default_level: AutonomyLevel = AutonomyLevel.CONFIRM):
        self.default_level = default_level
        self.action_limits = {
            'max_actions_per_task': 20,
            'max_cost_usd': 10.0,
            'max_files_modified': 5,
            'require_confirmation_for': [
                'delete_file', 'send_email', 'make_purchase',
                'modify_permissions', 'external_api_call'
            ]
        }
```

**Don't**:

```python
def agent_loop():
    while not done:
        action = agent.decide_action()
        execute(action)    # VULNERABLE: no limits or confirmation
```

**Refs**: OWASP LLM06 (Excessive Agency), NIST AI RMF GOVERN 3.2, ISO/IEC 23894 A.1

---

## Input/Output Security

### Rule: Validate Agent Outputs Before Action

**Level**: `strict`

**When**: Agent outputs will trigger actions, API calls, or system changes.

**Do**:

```python
from pydantic import BaseModel, validator
import re

class FileWriteAction(BaseModel):
    path: str
    content: str

    @validator('path')
    def validate_path(cls, v):
        if '..' in v or v.startswith('/'):
            raise ValueError("Invalid path")
        allowed_prefixes = ['output/', 'results/', 'tmp/']
        if not any(v.startswith(p) for p in allowed_prefixes):
            raise ValueError(f"Path must start with: {allowed_prefixes}")
        return v

    @validator('content')
    def validate_content(cls, v):
        dangerous_patterns = [r'<script', r'javascript:', r'\beval\s*\(', r'\bexec\s*\(']
        for pattern in dangerous_patterns:
            if re.search(pattern, v, re.IGNORECASE):
                raise ValueError("Content contains dangerous patterns")
        return v
```

**Don't**:

```python
def execute_agent_output(output):
    with open(output['path'], 'w') as f:   # VULNERABLE: no path validation
        f.write(output['content'])

def call_api(agent_output):
    requests.post(agent_output['url'], json=agent_output['data'])  # VULNERABLE
```

**Why**: Agent outputs can be manipulated through prompt injection or model errors.

**Refs**: OWASP LLM02 (Insecure Output Handling), NIST AI RMF MEASURE 2.9

---

### Rule: Implement Multi-Step Confirmation for High-Risk Actions

**Level**: `strict`

**When**: Agent actions have significant, potentially irreversible consequences.

**Do**:

```python
class HighRiskActionHandler:
    HIGH_RISK_ACTIONS = {
        'delete_data': {'confirmation_count': 2, 'cooldown_seconds': 30},
        'send_external': {'confirmation_count': 1, 'cooldown_seconds': 10},
        'modify_config': {'confirmation_count': 2, 'cooldown_seconds': 60},
    }
```

**Don't**:

```python
def handle_action(action):
    if action['type'] == 'delete_all_data':
        delete_all_data()   # VULNERABLE: no confirmation
```

**Refs**: NIST AI RMF GOVERN 3.2, ISO/IEC 23894 A.10 Safety

---

## Session Security

### Rule: Isolate Agent Sessions

**Level**: `warning`

**When**: Multiple agents or users share infrastructure.

**Do**:

```python
import uuid, os, shutil
from contextlib import contextmanager

class AgentSessionManager:
    @contextmanager
    def create_session(self, user_id: str, config: dict):
        session_id = str(uuid.uuid4())
        work_dir = f"/tmp/agent_sessions/{session_id}"
        os.makedirs(work_dir, mode=0o700, exist_ok=True)
        try:
            yield {'session_id': session_id, 'work_dir': work_dir}
        finally:
            shutil.rmtree(work_dir, ignore_errors=True)
```

**Don't**:

```python
global_memory = {}

def agent_action(user_id, action):
    global_memory[action['key']] = action['value']  # VULNERABLE: shared state
```

**Refs**: OWASP LLM05, CWE-200, NIST AI RMF MANAGE 2.4

---

## Monitoring & Audit

### Rule: Log All Agent Actions

**Level**: `warning`

**When**: Agent performs any action beyond pure reasoning.

**Do**:

```python
import logging, json
from datetime import datetime

SENSITIVE_KEYS = {'password', 'token', 'secret', 'key', 'credential', 'api_key'}

class AgentAuditLogger:
    def log_action(self, session_id, action_type, action_params, result, context):
        entry = {
            'timestamp': datetime.utcnow().isoformat(),
            'session_id': session_id,
            'user_id': context.get('user_id'),
            'action_type': action_type,
            'action_params': {
                k: '[REDACTED]' if any(s in k.lower() for s in SENSITIVE_KEYS) else v
                for k, v in action_params.items()
            },
            'result_status': result.get('status'),
        }
        logging.getLogger('agent_audit').info(json.dumps(entry))
```

**Don't**:

```python
def execute_tool(tool, params):
    return tool(**params)    # VULNERABLE: no audit logging

logger.info(f"API call with key: {api_key}")  # VULNERABLE: logs credentials
```

**Refs**: OWASP A09:2025 (Logging Failures), NIST AI RMF MEASURE 1.1, ISO/IEC 23894 A.11

---

## Quick Reference

| Rule | Level | Primary Risk | Key Control |
|------|-------|--------------|-------------|
| Validate Tool Calls | strict | Unauthorized execution | Allowlist + validation |
| Tool Permission Boundaries | strict | Privilege escalation | Least privilege |
| Sandbox Generated Code | strict | Arbitrary code execution | RestrictedPython |
| Limit Autonomy Scope | strict | Runaway actions | Confirmation gates |
| Validate Agent Outputs | strict | Malicious outputs | Schema validation |
| Multi-Step Confirmation | strict | Irreversible damage | Multiple confirmations |
| Isolate Sessions | warning | Data leakage | Session isolation |
| Log All Actions | warning | Undetected misuse | Comprehensive audit |

---

## Version History

- **v1.0.0** - Initial release for agentic AI security patterns
