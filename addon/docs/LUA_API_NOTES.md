# Lua API Notes

What we expect CIG's addon framework to provide, based on common game addon patterns (World of Warcraft, Final Fantasy XIV, Elder Scrolls Online). All names are speculative placeholders until CIG publishes their spec.

---

## Lua Version

Target: **Lua 5.1** (most common in game addon ecosystems). If CIG uses LuaJIT (likely for performance), all standard Lua 5.1 code is compatible. We avoid Lua 5.2+ syntax to maximize compatibility.

---

## Event System

Games with addon support provide an event registration mechanism. Placeholder pattern:

```lua
-- Register a handler for a named game event
CIG_API.RegisterEvent("CONTRACTS_TERMINAL_OPENED", function(event, data)
    -- called when the player opens the mission terminal
end)
```

Actual event names and callback signatures are unknown until CIG publishes the spec.

---

## UI Widgets

Games provide a set of UI primitives for addons to create overlays. We expect:

```lua
-- Create a frame/panel
local frame = CIG_API.CreateFrame("Frame", "ApeirogonMainPanel", UIParent)
frame:SetSize(300, 400)
frame:SetPoint("TOPRIGHT", -20, -20)

-- Create a text label
local label = frame:CreateFontString(nil, "OVERLAY")
label:SetFont("Fonts/default.ttf", 12)
label:SetText("ACCEPT  84")

-- Create a button
local btn = CIG_API.CreateFrame("Button", "ApeirogonSettings", frame)
btn:SetText("Settings")
btn:SetScript("OnClick", function() Settings.Open() end)
```

The actual widget API (frame types, anchoring system, font handling) will differ. WoW-style naming is used as a familiar reference point.

---

## HTTP Requests

For AI provider calls, the addon needs to make outbound HTTPS requests. Some addon frameworks provide this natively; others require a companion app.

Preferred: native async HTTP from within Lua

```lua
-- Preferred: native async HTTP (pattern used in some game engines)
CIG_API.HTTPRequest({
    url     = "https://api.anthropic.com/v1/messages",
    method  = "POST",
    headers = { ["x-api-key"] = api_key, ["Content-Type"] = "application/json" },
    body    = json_encode(payload),
    callback = function(status, response_body)
        -- called on completion
    end
})
```

Fallback: companion local service

If CIG's addon framework does not allow outbound HTTP, a lightweight local Python service (`addon_service.py`, not yet written) could run in the background and the addon would communicate with it via a local socket or shared file.

---

## Settings Persistence

The standard pattern for addon settings is a saved variables file that the game reads and writes automatically.

```lua
-- Declare in TOC or equivalent:
-- SavedVariables: ApeirogonLogisticsDB

-- At addon load:
if not ApeirogonLogisticsDB then
    ApeirogonLogisticsDB = DefaultSettings()
end

-- Read:
local ship = ApeirogonLogisticsDB.ship

-- Write:
ApeirogonLogisticsDB.ship = "hull-b"
```

The API key is stored here too. CIG may provide a more secure storage mechanism for sensitive values — use that if available, and clearly mark where the key is stored in `settings.lua`.

---

## JSON Encoding/Decoding

Lua's standard library has no JSON support. Options:

1. **Bundled library** — include a small Lua JSON library (e.g., `dkjson`, `lua-cjson` if available)
2. **Game-provided** — many games provide a JSON utility in their addon API
3. **Manual serialization** — for simple outbound payloads to AI APIs, hand-roll a minimal serializer

We use option 3 for the AI provider call (the payload is simple and predictable) and option 1 (`utils.lua` includes a minimal pure-Lua JSON decoder for parsing AI responses). The `utils.lua` bundled decoder handles only the subset of JSON that AI providers return.

---

## Math and String Libraries

Standard Lua 5.1 `math.*` and `string.*` are available in all game addon environments. We rely only on these — no external math libraries.

---

## Module System

Lua 5.1 modules use `require()`. In game addon environments, `require()` behavior varies:
- WoW does not support `require()` — files share a global namespace
- Other environments do support it

We write the code using `require()` for clarity and maintainability. A compatibility shim in `main.lua` can handle environments where `require()` is not available by manually declaring the module tables globally before each file loads.

---

## What to Update When CIG Publishes Their Spec

1. Replace all `CIG_API.*` calls in `main.lua`, `contract_parser.lua`, `ui_overlay.lua`, `settings.lua`, `api_client.lua` with actual CIG API calls
2. Update the TOC format (`ApeirogonLogistics.toc`) to match CIG's manifest format
3. Verify the Lua version (5.1 vs 5.4 vs LuaJIT)
4. Confirm the event names and data shapes
5. Confirm the settings persistence mechanism and update API key storage if CIG provides a more secure option
6. Update this file with confirmed details
