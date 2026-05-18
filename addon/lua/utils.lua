-- utils.lua
-- Shared utilities for Apeirogon Logistics addon.
-- No game API dependencies — this file is fully portable Lua 5.1.

local Utils = {}

-- Clamp a number to [min, max]
function Utils.clamp(value, min_val, max_val)
    return math.max(min_val, math.min(max_val, value))
end

-- Round a number to nearest integer
function Utils.round(value)
    return math.floor(value + 0.5)
end

-- Lowercase trim for key normalization
function Utils.normalize_key(s)
    if type(s) ~= "string" then return "" end
    return s:lower():match("^%s*(.-)%s*$")
end

-- Safe table lookup: returns nil instead of erroring on missing keys
function Utils.safe_get(t, ...)
    local v = t
    for _, key in ipairs({...}) do
        if type(v) ~= "table" then return nil end
        v = v[key]
    end
    return v
end

-- Returns true if a table contains a value
function Utils.table_contains(t, value)
    for _, v in ipairs(t) do
        if v == value then return true end
    end
    return false
end

-- Shallow copy of a table
function Utils.shallow_copy(t)
    local copy = {}
    for k, v in pairs(t) do copy[k] = v end
    return copy
end

-- Format a score as a colored verdict string for display
-- Returns a plain string (color formatting added by ui_overlay.lua)
function Utils.format_verdict(score, verdict)
    return string.format("[%s %d]", verdict, score)
end

-- Minimal JSON serializer for simple flat tables (used for AI provider payloads)
-- Only handles string and number values. Not a full JSON implementation.
function Utils.json_encode_simple(t)
    local parts = {}
    for k, v in pairs(t) do
        local key_str = string.format("%q", tostring(k))
        local val_str
        if type(v) == "number" then
            val_str = tostring(v)
        elseif type(v) == "boolean" then
            val_str = v and "true" or "false"
        elseif type(v) == "string" then
            val_str = string.format("%q", v)
        elseif type(v) == "table" then
            -- Nested table: encode as array if integer-keyed, object otherwise
            local is_array = (#v > 0)
            if is_array then
                local arr = {}
                for _, item in ipairs(v) do
                    if type(item) == "string" then
                        arr[#arr + 1] = string.format("%q", item)
                    else
                        arr[#arr + 1] = tostring(item)
                    end
                end
                val_str = "[" .. table.concat(arr, ",") .. "]"
            else
                val_str = Utils.json_encode_simple(v)
            end
        else
            val_str = "null"
        end
        parts[#parts + 1] = key_str .. ":" .. val_str
    end
    return "{" .. table.concat(parts, ",") .. "}"
end

-- Minimal JSON decoder for AI provider responses.
-- Handles only the simple flat objects and arrays that providers return.
-- For full JSON parsing, replace with a bundled library (e.g., dkjson) if available.
function Utils.json_decode_simple(s)
    -- Strip outer braces
    local inner = s:match("^%s*{(.+)}%s*$")
    if not inner then return nil end
    local result = {}
    for key, val in inner:gmatch('"([^"]+)"%s*:%s*("?[^,}]+"?)') do
        -- Unquote string values
        local cleaned = val:match('^"(.*)"$') or val
        -- Try numeric conversion
        result[key] = tonumber(cleaned) or cleaned
    end
    return result
end

return Utils
