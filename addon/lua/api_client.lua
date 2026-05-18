-- api_client.lua
-- Sends contract context to an AI provider for optional commentary.
-- The deterministic scorer always runs first. This module adds one plain-English
-- sentence of analysis after the score is computed.
--
-- STUB: HTTP calls use CIG_API placeholder. Replace with actual game HTTP API
-- when CIG publishes their addon framework.
--
-- SECURITY: The API key is loaded immediately before the call and is never
-- stored in a global variable, logged, or included in error messages.

local Utils      = require("ApeirogonLogistics.utils")
local Settings   = require("ApeirogonLogistics.settings")
local ApiClient  = {}

-- Supported providers and their endpoint configurations.
-- Add new providers here. The api_key field is never stored in this table.
local PROVIDERS = {
    anthropic = {
        url     = "https://api.anthropic.com/v1/messages",
        model   = "claude-haiku-4-5-20251001",
        version = "2023-06-01",
        build_headers = function(api_key)
            return {
                ["x-api-key"]         = api_key,
                ["anthropic-version"] = "2023-06-01",
                ["content-type"]      = "application/json",
            }
        end,
        build_body = function(prompt)
            return Utils.json_encode_simple({
                model      = "claude-haiku-4-5-20251001",
                max_tokens = 150,
                messages   = {{ role = "user", content = prompt }},
            })
        end,
        parse_response = function(body)
            -- Anthropic response: {"content":[{"type":"text","text":"..."}]}
            local text = body:match('"text"%s*:%s*"([^"]+)"')
            return text
        end,
    },
    openai = {
        url   = "https://api.openai.com/v1/chat/completions",
        model = "gpt-4o-mini",
        build_headers = function(api_key)
            return {
                ["Authorization"] = "Bearer " .. api_key,
                ["Content-Type"]  = "application/json",
            }
        end,
        build_body = function(prompt)
            return Utils.json_encode_simple({
                model      = "gpt-4o-mini",
                max_tokens = 150,
                messages   = {{ role = "user", content = prompt }},
            })
        end,
        parse_response = function(body)
            -- OpenAI response: {"choices":[{"message":{"content":"..."}}]}
            local text = body:match('"content"%s*:%s*"([^"]+)"')
            return text
        end,
    },
}

-- Per-session response cache. Prevents duplicate calls for contracts seen
-- multiple times during a session.
local response_cache = {}

-- Build the prompt sent to the AI provider.
-- The prompt instructs the AI to give one plain sentence with no invented numbers.
local function build_prompt(contract, score_result)
    local delivery_list = table.concat(contract.delivery or {}, ", ")
    return string.format(
        "You are a Star Citizen hauling advisor. "
        .. "Score: %d/100 (%s). "
        .. "Contract: %s — pickup at %s, deliver to %s. "
        .. "In one plain sentence, explain the main reason for this score. "
        .. "Do not invent any numbers. Do not mention 'fragmentation penalty' or other internal scoring terms — use plain language.",
        score_result.score,
        score_result.verdict,
        contract.issuer or "unknown issuer",
        contract.pickup or "unknown pickup",
        delivery_list
    )
end

-- Build a cache key for a contract (pickup + deliveries, issuer).
local function cache_key(contract)
    local deliveries = table.concat(contract.delivery or {}, "|")
    return (contract.issuer or "") .. "|" .. (contract.pickup or "") .. "|" .. deliveries
end

-- Request AI commentary for a scored contract.
-- This is non-blocking — callback is called asynchronously when the response arrives.
--
-- contract     : parsed contract table
-- score_result : result from ScoringEngine.score_contract()
-- callback     : function(commentary_text) — called with a string, or nil on failure
--
-- STUB: Replace CIG_API.HTTPRequest with actual game HTTP API.
function ApiClient.request_commentary(contract, score_result, callback)
    if not Settings.has_ai_provider() then
        callback(nil)
        return
    end

    local key = cache_key(contract)
    if response_cache[key] then
        callback(response_cache[key])
        return
    end

    local provider_name = Settings.get("ai_provider")
    local provider = PROVIDERS[provider_name]
    if not provider then
        callback(nil)
        return
    end

    local api_key = Settings.get_api_key()
    if not api_key then
        callback(nil)
        return
    end

    local prompt  = build_prompt(contract, score_result)
    local headers = provider.build_headers(api_key)
    local body    = provider.build_body(prompt)

    -- SECURITY: api_key is used only to build headers above and is not
    -- captured in the closure below.
    api_key = nil

    -- TODO: replace with actual CIG game HTTP API
    -- Speculative CIG async HTTP call:
    --   CIG_API.HTTPRequest({
    --       url      = provider.url,
    --       method   = "POST",
    --       headers  = headers,
    --       body     = body,
    --       callback = function(status_code, response_body)
    --           if status_code == 200 then
    --               local text = provider.parse_response(response_body)
    --               if text then
    --                   response_cache[key] = text
    --                   callback(text)
    --               else
    --                   callback(nil)
    --               end
    --           else
    --               callback(nil)
    --           end
    --       end
    --   })
    callback(nil)
end

-- Clear the response cache (call at end of session or when player changes ship/location).
function ApiClient.clear_cache()
    response_cache = {}
end

return ApiClient
