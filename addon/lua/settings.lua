-- settings.lua
-- User settings management for Apeirogon Logistics addon.
--
-- STUB: Settings persistence uses CIG_API placeholder calls.
-- Replace CIG_API.* with actual CIG addon settings API when published.
-- The API key security rules (never log, never expose in UI) must be preserved.

local Utils    = require("ApeirogonLogistics.utils")
local Settings = {}

-- Default values for all settings
local DEFAULTS = {
    ship             = "",       -- current ship key, e.g. "hull-b"
    location         = "",       -- current location for dead-leg detection
    ai_provider      = "",       -- "openai", "anthropic", or "" for none
    api_key          = "",       -- AI provider API key -- see security note below
    show_score       = true,     -- show numeric score in overlay
    show_factors     = true,     -- show factor breakdown on hover
    show_ai_comment  = true,     -- show AI text commentary when available
    compact_mode     = false,    -- show verdict only (no detail)
}

-- In-memory settings table. Loaded from persistent storage on addon init.
-- SECURITY: The api_key field is held only for the lifetime of a session.
-- It is loaded from CIG's secure addon settings storage and never written
-- to a log, chat frame, or error message.
local current = Utils.shallow_copy(DEFAULTS)

-- Load settings from CIG's persistent addon storage.
-- Called once at addon initialization (from main.lua).
-- STUB: Replace CIG_API.GetSavedVariable with actual CIG API.
function Settings.load()
    -- TODO: replace with actual CIG addon settings API
    -- Example WoW pattern (for reference):
    --   if ApeirogonLogisticsDB then
    --       for k, v in pairs(ApeirogonLogisticsDB) do current[k] = v end
    --   end
    --
    -- CIG equivalent (speculative):
    --   local saved = CIG_API.GetSavedVariables("ApeirogonLogistics")
    --   if saved then
    --       for k, v in pairs(saved) do current[k] = v end
    --   end
end

-- Save current settings to CIG's persistent addon storage.
-- Called when settings change. Do not call on every frame.
-- STUB: Replace CIG_API.SetSavedVariable with actual CIG API.
function Settings.save()
    -- TODO: replace with actual CIG addon settings API
    -- CIG equivalent (speculative):
    --   CIG_API.SetSavedVariables("ApeirogonLogistics", current)
    --
    -- SECURITY: The api_key is included in current{} but CIG's settings
    -- storage should be treated as a secure keychain, not a plain file.
    -- If CIG provides a separate secure credential storage API, use that
    -- for api_key and exclude it from the general settings save.
end

-- Get a setting value.
function Settings.get(key)
    return current[key]
end

-- Set a setting value and persist immediately.
function Settings.set(key, value)
    if DEFAULTS[key] == nil then return end  -- reject unknown keys
    current[key] = value
    Settings.save()
end

-- Get the API key without logging it.
-- Returns nil if no key is configured.
function Settings.get_api_key()
    local key = current.api_key
    if key == nil or key == "" then return nil end
    return key
end

-- Set the API key. Never log this value.
function Settings.set_api_key(key)
    current.api_key = key or ""
    Settings.save()
end

-- Returns true if an AI provider and key are configured.
function Settings.has_ai_provider()
    return current.ai_provider ~= ""
       and current.api_key ~= ""
end

-- Reset all settings to defaults (does not clear the API key).
function Settings.reset_display()
    current.show_score      = DEFAULTS.show_score
    current.show_factors    = DEFAULTS.show_factors
    current.show_ai_comment = DEFAULTS.show_ai_comment
    current.compact_mode    = DEFAULTS.compact_mode
    Settings.save()
end

return Settings
