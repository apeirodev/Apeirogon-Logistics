-- ui_overlay.lua
-- In-game overlay and contract info panel for Apeirogon Logistics.
--
-- STUB: All SC_UI.* and CIG_API.* calls are placeholders.
-- Replace with actual CIG UI widget API when published.
-- The data flow (what gets displayed and when) is complete and correct.

local Settings    = require("ApeirogonLogistics.settings")
local Utils       = require("ApeirogonLogistics.utils")
local UIOverlay   = {}

-- Verdict color codes (placeholder format — update to match CIG color API)
local COLORS = {
    ACCEPT  = "|cff00cc66",  -- green
    DEFER   = "|cffffff00",  -- yellow
    REJECT  = "|cffcc3333",  -- red
    RESET   = "|r",
    NEUTRAL = "|cffaaaaaa",  -- grey for labels
}

-- Main overlay panel (created once, shown/hidden as needed)
local main_panel     = nil
local contract_rows  = {}   -- one row widget per visible contract
local detail_panel   = nil  -- hover detail view
local settings_panel = nil  -- settings UI

-- Format a verdict string with color for display in the overlay.
local function colored_verdict(score, verdict)
    local color = COLORS[verdict] or COLORS.NEUTRAL
    return string.format("%s[%s %d]%s", color, verdict, score, COLORS.RESET)
end

-- Create the main overlay panel and attach it to the contracts terminal.
-- STUB: SC_UI.CreateFrame, SetSize, SetPoint are WoW-pattern placeholders.
function UIOverlay.create()
    if main_panel then return end

    -- TODO: replace SC_UI.* with actual CIG UI widget API
    -- Speculative:
    --   main_panel = SC_UI.CreateFrame("Frame", "ApeirogonMain")
    --   main_panel:SetSize(340, 600)
    --   main_panel:SetPoint("TOPRIGHT", ContractsTerminalFrame, "TOPLEFT", -10, 0)
    --   main_panel:SetBackdrop({ bgFile = "Textures/UI/panel_bg.dds", edgeSize = 2 })
    --   main_panel:Hide()
    --
    --   -- Title bar
    --   local title = main_panel:CreateFontString(nil, "OVERLAY")
    --   title:SetFont("Fonts/orbitron.ttf", 13)
    --   title:SetText("Apeirogon Logistics")
    --   title:SetPoint("TOPLEFT", 10, -8)
    --
    --   -- Settings button
    --   local settings_btn = SC_UI.CreateFrame("Button", "ApeirogonSettingsBtn", main_panel)
    --   settings_btn:SetSize(22, 22)
    --   settings_btn:SetPoint("TOPRIGHT", -6, -6)
    --   settings_btn:SetText("⚙")
    --   settings_btn:SetScript("OnClick", function() UIOverlay.toggle_settings() end)

    UIOverlay.create_detail_panel()
    UIOverlay.create_settings_panel()
end

-- Create the hover detail panel (factor breakdown + AI commentary).
-- STUB
function UIOverlay.create_detail_panel()
    -- TODO: create a secondary panel that appears when hovering over a contract row
    -- It should show:
    --   - Top 3 positive factors and their contributions
    --   - Top 3 negative factors and their contributions
    --   - AI commentary text (if available)
    --   - Stack indicator (if same-pickup contracts exist)
end

-- Create the settings panel (ship selection, API key, display options).
-- STUB
function UIOverlay.create_settings_panel()
    -- TODO: create settings panel with:
    --   - Ship dropdown (populated from scoring_config ship keys)
    --   - Location text field
    --   - AI provider dropdown ("None", "Anthropic / Claude", "OpenAI")
    --   - API key input (masked, password-style — never show in plaintext)
    --   - Checkboxes for show_score, show_factors, show_ai_comment, compact_mode
    --   - Save and Reset buttons
end

-- Show the main overlay panel.
function UIOverlay.show()
    if not main_panel then UIOverlay.create() end
    -- TODO: main_panel:Show()
end

-- Hide the main overlay panel.
function UIOverlay.hide()
    if not main_panel then return end
    -- TODO: main_panel:Hide()
end

-- Toggle the settings panel open/closed.
function UIOverlay.toggle_settings()
    if not settings_panel then return end
    -- TODO:
    --   if settings_panel:IsShown() then
    --       settings_panel:Hide()
    --   else
    --       settings_panel:Show()
    --   end
end

-- Update the overlay with fresh scoring results.
-- Called by main.lua after scoring a batch of contracts.
-- results: array of { contract, score_result } tables
function UIOverlay.update(results)
    if not main_panel then UIOverlay.create() end

    -- Clear existing rows
    -- TODO: for _, row in ipairs(contract_rows) do row:Hide() end
    contract_rows = {}

    if not results or #results == 0 then
        UIOverlay.hide()
        return
    end

    local compact = Settings.get("compact_mode")
    local show_score = Settings.get("show_score")

    for i, entry in ipairs(results) do
        local contract     = entry.contract
        local score_result = entry.score_result

        -- Build the display text for this contract row
        local verdict_str = ""
        if show_score then
            verdict_str = colored_verdict(score_result.score, score_result.verdict)
        else
            local color = COLORS[score_result.verdict] or COLORS.NEUTRAL
            verdict_str = color .. score_result.verdict .. COLORS.RESET
        end

        local delivery_str = table.concat(contract.delivery or {}, " → ")
        local issuer_str   = contract.issuer or "Unknown"
        local pickup_str   = contract.pickup or "Unknown"

        local row_text
        if compact then
            row_text = string.format("%s  %s", verdict_str, delivery_str)
        else
            row_text = string.format("%s  %s — %s → %s",
                verdict_str, issuer_str, pickup_str, delivery_str)
        end

        -- Stack indicator: show if multiple contracts share this pickup
        local stack_count = entry.context and entry.context.same_pickup_count or 1
        if stack_count > 1 and not compact then
            row_text = row_text .. string.format(
                "  %s[+%d stack]%s",
                COLORS.NEUTRAL, stack_count, COLORS.RESET
            )
        end

        -- TODO: create a UI row widget for this entry
        --   local row = SC_UI.CreateFrame("Button", "ApeirogonRow"..i, main_panel)
        --   row:SetSize(320, 22)
        --   row:SetPoint("TOPLEFT", 10, -(30 + (i-1) * 24))
        --   local label = row:CreateFontString(nil, "OVERLAY")
        --   label:SetFont("Fonts/default.ttf", 11)
        --   label:SetText(row_text)
        --   row:SetScript("OnEnter", function() UIOverlay.show_detail(entry) end)
        --   row:SetScript("OnLeave", function() UIOverlay.hide_detail() end)
        --   row:Show()
        --   contract_rows[i] = row

        -- Placeholder: print to chat until UI is implemented
        -- TODO: remove this debug output once UI widgets are implemented
        print(row_text)
    end

    UIOverlay.show()
end

-- Show the detail panel for a contract entry.
-- entry: { contract, score_result, context, commentary }
function UIOverlay.show_detail(entry)
    if not Settings.get("show_factors") then return end

    -- TODO: populate and show detail_panel
    -- Display top positive factors:
    --   Sort factors by contribution (descending), show top 3 positive
    -- Display top negative factors:
    --   Sort factors by contribution (ascending), show top 3 negative
    -- Display AI commentary if available

    local factors = entry.score_result and entry.score_result.factors or {}
    local pos_factors = {}
    local neg_factors = {}

    for name, contribution in pairs(factors) do
        if contribution > 0 then
            pos_factors[#pos_factors + 1] = { name = name, value = contribution }
        elseif contribution < 0 then
            neg_factors[#neg_factors + 1] = { name = name, value = contribution }
        end
    end

    table.sort(pos_factors, function(a, b) return a.value > b.value end)
    table.sort(neg_factors, function(a, b) return a.value < b.value end)

    -- TODO: render these into detail_panel rows
end

-- Hide the detail panel.
function UIOverlay.hide_detail()
    -- TODO: detail_panel:Hide()
end

return UIOverlay
