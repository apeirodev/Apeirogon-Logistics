# OWASP Top 10 2025 - Core Security Rules

This file provides foundational security rules based on OWASP Top 10:2025.
Source: https://github.com/TikiTribe/claude-secure-coding-rules (MIT)

## Overview

**Standard**: OWASP Top 10:2025 (Release Candidate, November 2025)
**Scope**: Web application security risks
**Data Source**: 589 CWEs across 248 categories

---

## A01:2025 - Broken Access Control

**Risk Level**: Critical (3.73% of applications affected)
**CWE Coverage**: 40 CWEs including SSRF

### Rule: Enforce Server-Side Access Control

**Level**: `strict`

**When**: Any endpoint accessing protected resources, user data, or administrative functions.

**Do**:

```python
from functools import wraps
from flask import g, abort

def require_permission(permission):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not g.user.has_permission(permission):
                abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return decorator

@app.route('/admin/users/<int:user_id>')
@require_permission('admin:read')
def get_user(user_id):
    return User.query.get_or_404(user_id)
```

**Don't**:

```python
@app.route('/api/users/<int:user_id>')
def get_user(user_id):
    # VULNERABLE: No authorization check
    return User.query.get_or_404(user_id)
```

**Why**: Broken access control allows attackers to access unauthorized data, modify other users'
data, or elevate privileges. Server-side enforcement is required because client-side controls can
be bypassed.

**Refs**: OWASP A01:2025, CWE-284, CWE-862, CWE-863, NIST SSDF PW.1.1

---

### Rule: Prevent SSRF Attacks

**Level**: `strict`

**When**: Application makes HTTP requests based on user-supplied URLs or parameters.

**Do**:

```python
from urllib.parse import urlparse
import ipaddress

ALLOWED_HOSTS = ['api.example.com', 'cdn.example.com']

def validate_url(url):
    parsed = urlparse(url)
    if parsed.scheme not in ['http', 'https']:
        raise ValueError("Invalid scheme")
    if parsed.hostname not in ALLOWED_HOSTS:
        raise ValueError("Host not allowed")
    try:
        ip = ipaddress.ip_address(parsed.hostname)
        if ip.is_private or ip.is_loopback:
            raise ValueError("Internal addresses blocked")
    except ValueError:
        pass
    return url
```

**Don't**:

```python
def fetch_resource(url):
    # VULNERABLE: Direct fetch allows SSRF to internal services
    return requests.get(url)
```

**Why**: SSRF allows attackers to make requests to internal services, cloud metadata endpoints,
or other protected resources.

**Refs**: OWASP A01:2025, CWE-918, MITRE ATLAS AML.T0024

---

## A02:2025 - Security Misconfiguration

**Risk Level**: High (3.00% of applications affected)

### Rule: Use Secure Default Configurations

**Level**: `strict`

**Do**:

```python
app.config.update(
    DEBUG=False,
    TESTING=False,
    SESSION_COOKIE_SECURE=True,
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE='Lax',
    PERMANENT_SESSION_LIFETIME=1800,
)

@app.errorhandler(Exception)
def handle_error(error):
    app.logger.error(f"Error: {error}")
    return {"error": "Internal server error"}, 500
```

**Don't**:

```python
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'dev'

@app.errorhandler(Exception)
def handle_error(error):
    # VULNERABLE: Exposes stack traces and internal paths
    return {"error": str(error), "traceback": traceback.format_exc()}, 500
```

**Refs**: OWASP A02:2025, CWE-16, CWE-209, NIST SSDF PW.9.1

---

## A03:2025 - Software Supply Chain Failures

**Risk Level**: Critical (highest exploit/impact scores)

### Rule: Verify Dependency Integrity

**Level**: `strict`

**Do**:

```bash
pip install --require-hashes -r requirements.txt
```

```python
# requirements.txt -- pin exact versions with hashes
requests==2.31.0 \
    --hash=sha256:58cd2187c01e70e6e26505bca751777aa9f2ee0b7f4300988b709f44e013003f
```

```python
import hashlib, hmac

def verify_checksum(filepath, expected_hash):
    sha256 = hashlib.sha256()
    with open(filepath, 'rb') as f:
        for chunk in iter(lambda: f.read(8192), b''):
            sha256.update(chunk)
    if not hmac.compare_digest(sha256.hexdigest(), expected_hash):
        raise SecurityError("Checksum mismatch - possible tampering")
```

**Don't**:

```bash
pip install requests        # VULNERABLE: unpinned
npm install some-package    # VULNERABLE: no integrity check
```

**Refs**: OWASP A03:2025, CWE-829, NIST SSDF PS.3.1, OSSF Scorecard

---

## A04:2025 - Cryptographic Failures

**Risk Level**: High

### Rule: Use Strong Cryptographic Algorithms

**Level**: `strict`

**Do**:

```python
import bcrypt, os
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes

def hash_password(password: str) -> bytes:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt(rounds=12))

def encrypt_data(plaintext: bytes, key: bytes) -> bytes:
    return Fernet(key).encrypt(plaintext)

def derive_key(password: str, salt: bytes) -> bytes:
    kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=600000)
    return kdf.derive(password.encode())
```

**Don't**:

```python
import hashlib
password_hash = hashlib.md5(password.encode()).hexdigest()  # VULNERABLE: MD5
SECRET_KEY = "mysecretkey123"                               # VULNERABLE: hardcoded
```

**Refs**: OWASP A04:2025, CWE-327, CWE-328, NIST SP 800-131A

---

## A05:2025 - Injection

**Risk Level**: High

### Rule: Use Parameterized Queries and Safe Subprocess Calls

**Level**: `strict`

**Do**:

```python
# SQL
cursor.execute("SELECT * FROM users WHERE username = %s", (username,))

# Subprocess -- explicit args list, no shell=True
import subprocess
result = subprocess.run(['ls', '-la', directory], capture_output=True, text=True, check=True)
```

**Don't**:

```python
query = f"SELECT * FROM users WHERE username = '{username}'"  # VULNERABLE: SQL injection
import os
os.system(f"ls -la {user_input}")                             # VULNERABLE: command injection
```

**Refs**: OWASP A05:2025, CWE-89, CWE-78, CWE-79, NIST SSDF PW.5.1

---

## A06:2025 - Insecure Design

**Risk Level**: High

### Rule: Implement Threat Modeling

**Level**: `advisory`

- Identify trust boundaries and data flows
- Document threat actors and attack vectors
- Apply security controls at design phase
- Use abuse case scenarios alongside use cases

**Refs**: OWASP A06:2025, CWE-840, NIST SSDF PW.1.1

---

## A07:2025 - Authentication Failures

**Risk Level**: High

### Rule: Implement Secure Session Management

**Level**: `strict`

**Do**:

```python
import secrets
app.config.update(
    SECRET_KEY=secrets.token_hex(32),
    SESSION_COOKIE_SECURE=True,
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE='Lax',
    PERMANENT_SESSION_LIFETIME=1800,
)
```

**Refs**: OWASP A07:2025, CWE-287, CWE-384, NIST SP 800-63B

---

## A08:2025 - Software and Data Integrity Failures

**Risk Level**: High

### Rule: Verify Code and Data Integrity

**Level**: `strict`

**Do**:

```python
import hmac, hashlib, json

def verify_payload(payload, signature, secret_key):
    expected = hmac.new(secret_key.encode(), payload.encode(), hashlib.sha256).hexdigest()
    if not hmac.compare_digest(signature, expected):
        raise SecurityError("Invalid signature")
    return json.loads(payload)

# Safe deserialization
data = json.loads(user_input)   # Safe: JSON only
```

**Don't**:

```python
import pickle
data = pickle.loads(user_input)  # VULNERABLE: arbitrary code execution
```

**Refs**: OWASP A08:2025, CWE-502, CWE-829, NIST SSDF PW.4.1

---

## A09:2025 - Logging & Alerting Failures

**Risk Level**: Medium

### Rule: Log Security Events Comprehensively

**Level**: `warning`

**Do**:

```python
import logging, json
from datetime import datetime

security_logger = logging.getLogger('security')

def log_security_event(event_type, details, severity='INFO'):
    security_logger.log(
        getattr(logging, severity),
        json.dumps({
            'timestamp': datetime.utcnow().isoformat(),
            'event_type': event_type,
            'details': details
        })
    )
```

**Don't**:

```python
logger.info(f"Login attempt: {username}:{password}")  # VULNERABLE: logs credentials
```

**Refs**: OWASP A09:2025, CWE-778, CWE-223, NIST SP 800-92

---

## A10:2025 - Mishandling of Exceptional Conditions

**Risk Level**: Medium
**Status**: New category for 2025

### Rule: Handle Errors Securely -- Fail Closed

**Level**: `warning`

**Do**:

```python
def check_permission(user, resource):
    try:
        return permission_service.check(user, resource)
    except Exception as e:
        logger.error(f"Permission check failed: {e}")
        return False   # Fail closed -- deny access on error
```

**Don't**:

```python
def check_permission(user, resource):
    try:
        return permission_service.check(user, resource)
    except:
        return True    # DANGEROUS: grants access on error
```

**Refs**: OWASP A10:2025, CWE-755, CWE-754, CWE-391

---

## Quick Reference

| Category | Level | Primary CWEs | Key Control |
|----------|-------|--------------|-------------|
| A01 Broken Access Control | strict | CWE-284, CWE-862 | Server-side authorization |
| A02 Security Misconfiguration | strict | CWE-16, CWE-209 | Secure defaults |
| A03 Supply Chain Failures | strict | CWE-829 | Integrity verification |
| A04 Cryptographic Failures | strict | CWE-327, CWE-328 | Strong algorithms |
| A05 Injection | strict | CWE-89, CWE-78, CWE-79 | Parameterized queries |
| A06 Insecure Design | advisory | CWE-840 | Threat modeling |
| A07 Authentication Failures | strict | CWE-287, CWE-384 | Secure sessions |
| A08 Integrity Failures | strict | CWE-502 | Signature verification |
| A09 Logging Failures | warning | CWE-778 | Comprehensive logging |
| A10 Error Handling | warning | CWE-755 | Fail closed |

---

## Version History

- **v1.0.0** - Initial release based on OWASP Top 10:2025 RC1 (November 2025)
