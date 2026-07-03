-- main.lua
-- Entry point for the Apeirogon Logistics in-game addon.
-- Registers event handlers, coordinates the scoring pipeline, and drives the UI.
--
-- STUB: All CIG_API.* event names and registration calls are placeholders.
-- Replace with actual CIG addon event API when published.
-- The scoring pipeline logic (what happens when events fire) is complete.

local ScoringEngine    = require("ApeirogonLogistics.scoring_engine")
local ContractParser   = require("ApeirogonLogistics.contract_parser")
local ApiClient        = require("ApeirogonLogistics.api_client")
local UIOverlay        = require("ApeirogonLogistics.ui_overlay")
local Settings         = require("ApeirogonLogistics.settings")

-- Addon namespace
local ApeirogonLogistics = {}

-- Most recent scored results, kept for re-display if settings change mid-session
local last_results = {}

-- Score all visible contracts and update the overlay.
-- Called when the terminal opens or refreshes.
local function score_and_display()
    local contracts = ContractParser.get_all_contracts()
    if not contracts or #contracts == 0 then
        UIOverlay.hide()
        return
    end

    local player_state = {
        ship     = Settings.get("ship"),
        location = Settings.get("location"),
    }

    local contexts = ScoringEngine.build_context(contracts, player_state)

    local results = {}
    for i, contract in ipairs(contracts) do
        local score_result = ScoringEngine.score_contract(contract, contexts[i])
        results[i] = {
            contract     = contract,
            context      = contexts[i],
            score_result = score_result,
            commentary   = nil,    -- filled in asynchronously below
        }
    end

    -- Sort results: ACCEPT first (highest score), then DEFER, then REJECT
    table.sort(results, function(a, b)
        return a.score_result.score > b.score_result.score
    end)

    last_results = results
    UIOverlay.update(results)

    -- Request AI commentary for each contract asynchronously (if provider configured)
    if Settings.has_ai_provider() then
        for i, entry in ipairs(results) do
            local idx = i
            ApiClient.request_commentary(entry.contract, entry.score_result,
                function(commentary_text)
                    if commentary_text then
                        results[idx].commentary = commentary_text
                        UIOverlay.update(results)
                    end
                end
            )
        end
    end
end

-- Called when the player opens the contracts terminal.
-- STUB: "CONTRACTS_TERMINAL_OPENED" is a placeholder event name.
local function on_terminal_opened()
    UIOverlay.show()
    score_and_display()
end

-- Called when the contracts list refreshes (new missions loaded).
-- STUB: "CONTRACTS_LIST_UPDATED" is a placeholder event name.
local function on_contracts_updated()
    score_and_display()
end

-- Called when the player closes the terminal.
-- STUB: "TERMINAL_CLOSED" is a placeholder event name.
local function on_terminal_closed()
    UIOverlay.hide()
    ApiClient.clear_cache()
end

-- Called when the player's ship or location changes in addon settings.
-- Rescores with the new context.
function ApeirogonLogistics.on_settings_changed()
    ApiClient.clear_cache()
    if last_results and #last_results > 0 then
        score_and_display()
    end
end

-- Addon initialization. Called once when the addon loads.
-- STUB: Replace CIG_API.RegisterEvent with actual game event registration.
function ApeirogonLogistics.init()
    Settings.load()
    UIOverlay.create()

    -- TODO: replace with actual CIG addon event registration
    -- Speculative pattern (WoW-style, for reference):
    --
    --   local frame = CIG_API.CreateFrame("Frame")
    --   frame:RegisterEvent("CONTRACTS_TERMINAL_OPENED")
    --   frame:RegisterEvent("CONTRACTS_LIST_UPDATED")
    --   frame:RegisterEvent("TERMINAL_CLOSED")
    --   frame:SetScript("OnEvent", function(self, event, ...)
    --       if event == "CONTRACTS_TERMINAL_OPENED" then on_terminal_opened()
    --       elseif event == "CONTRACTS_LIST_UPDATED"  then on_contracts_updated()
    --       elseif event == "TERMINAL_CLOSED"         then on_terminal_closed()
    --       end
    --   end)
    --
    -- Alternative pattern (callback-based):
    --
    --   CIG_API.RegisterEvent("CONTRACTS_TERMINAL_OPENED", on_terminal_opened)
    --   CIG_API.RegisterEvent("CONTRACTS_LIST_UPDATED",    on_contracts_updated)
    --   CIG_API.RegisterEvent("TERMINAL_CLOSED",           on_terminal_closed)
end

-- Slash command handler: /apeirogon or /apl
-- STUB: Replace CIG_API.RegisterSlashCommand with actual game slash command API.
local function slash_handler(args)
    local cmd = args and args:lower():match("^%s*(%S+)") or ""
    if cmd == "settings" then
        UIOverlay.toggle_settings()
    elseif cmd == "ship" then
        local ship = args:match("%S+%s+(.+)") or ""
        if ship ~= "" then
            Settings.set("ship", ship:lower())
            print("Apeirogon: ship set to " .. ship)
            ApeirogonLogistics.on_settings_changed()
        else
            print("Usage: /apl ship <ship-name>   (e.g. /apl ship hull-b)")
        end
    elseif cmd == "location" then
        local loc = args:match("%S+%s+(.+)") or ""
        if loc ~= "" then
            Settings.set("location", loc)
            print("Apeirogon: location set to " .. loc)
            ApeirogonLogistics.on_settings_changed()
        else
            print("Usage: /apl location <location>   (e.g. /apl location Everus Harbor)")
        end
    elseif cmd == "help" or cmd == "" then
        print("Apeirogon Logistics commands:")
        print("  /apl ship <name>          -- set your current ship")
        print("  /apl location <name>      -- set your current location")
        print("  /apl settings             -- open settings panel")
    else
        print("Unknown command. Type /apl help for options.")
    end
end

-- TODO: replace with actual CIG slash command registration
-- Speculative: CIG_API.RegisterSlashCommand("APEIROGON", "/apeirogon", slash_handler)
-- Speculative: CIG_API.RegisterSlashCommand("APL",        "/apl",        slash_handler)

-- Auto-initialize when the file loads
-- TODO: replace with the appropriate addon load event for CIG's framework
ApeirogonLogistics.init()

return ApeirogonLogistics
