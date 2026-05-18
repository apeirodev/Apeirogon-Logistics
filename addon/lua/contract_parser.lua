-- contract_parser.lua
-- Reads contract data from the game UI and converts it to the internal format.
--
-- STUB: All CIG_API.* calls are placeholders. Replace with actual game API
-- calls when CIG publishes their addon framework. The internal contract format
-- (what this module returns) is stable and should not need to change.
--
-- Internal contract format (mirrors developer/schema/mission.schema.json):
--   {
--       issuer            = "Covalex",
--       pickup            = "Everus Harbor",
--       delivery          = {"Baijini Point", "Shopp-L4"},
--       cargo_scu         = 96,               -- nil if unresolvable
--       reward_usc        = 42000,            -- nil if unresolvable
--       atmosphere_stops  = 0,
--       freight_complexity = false,
--       chain_collapse_risk = false,
--       congested_stations  = 0,
--       unresolved_fields   = {},             -- list of field names that couldn't be read
--   }

local Utils          = require("ApeirogonLogistics.utils")
local ContractParser = {}

-- Parse all contracts currently visible in the mission terminal.
-- Returns an array of internal contract tables.
-- STUB: Replace CIG_API.GetContractList with actual game API.
function ContractParser.get_all_contracts()
    -- TODO: replace with actual CIG game API
    -- The game should provide a way to enumerate contracts visible in the terminal.
    --
    -- Speculative CIG API call:
    --   local raw_contracts = CIG_API.GetContractList()
    --   local result = {}
    --   for _, raw in ipairs(raw_contracts or {}) do
    --       result[#result + 1] = ContractParser.parse_raw(raw)
    --   end
    --   return result
    return {}
end

-- Parse a single raw contract object from the game API into the internal format.
-- raw: the game's native contract data structure (shape unknown until CIG publishes API)
-- STUB: field names (raw.issuer, raw.pickup_location, etc.) are guesses.
function ContractParser.parse_raw(raw)
    if not raw then return nil end

    local contract = {
        issuer             = "",
        pickup             = "",
        delivery           = {},
        cargo_scu          = nil,
        reward_usc         = nil,
        atmosphere_stops   = 0,
        freight_complexity = false,
        chain_collapse_risk = false,
        congested_stations  = 0,
        unresolved_fields   = {},
    }

    -- Issuer
    -- TODO: replace raw.issuer with actual CIG field name
    if raw.issuer and raw.issuer ~= "" then
        contract.issuer = raw.issuer
    else
        contract.unresolved_fields[#contract.unresolved_fields + 1] = "issuer"
    end

    -- Pickup location
    -- TODO: replace raw.pickup_location with actual CIG field name
    if raw.pickup_location and raw.pickup_location ~= "" then
        contract.pickup = raw.pickup_location
    else
        contract.unresolved_fields[#contract.unresolved_fields + 1] = "pickup"
    end

    -- Delivery locations (may be one or many)
    -- TODO: replace raw.delivery_locations with actual CIG field name
    if raw.delivery_locations and #raw.delivery_locations > 0 then
        contract.delivery = raw.delivery_locations
    elseif raw.delivery_location and raw.delivery_location ~= "" then
        contract.delivery = {raw.delivery_location}
    else
        contract.unresolved_fields[#contract.unresolved_fields + 1] = "delivery"
    end

    -- Cargo SCU
    -- TODO: replace raw.cargo_scu with actual CIG field name
    if raw.cargo_scu and tonumber(raw.cargo_scu) then
        contract.cargo_scu = tonumber(raw.cargo_scu)
    else
        contract.unresolved_fields[#contract.unresolved_fields + 1] = "cargo_scu"
    end

    -- Reward in UEC
    -- TODO: replace raw.reward with actual CIG field name
    if raw.reward and tonumber(raw.reward) then
        contract.reward_usc = tonumber(raw.reward)
    else
        contract.unresolved_fields[#contract.unresolved_fields + 1] = "reward_usc"
    end

    -- Atmosphere stops: count delivery locations flagged as planetary surface
    -- TODO: cross-reference delivery locations against known atmospheric locations
    -- using data from developer/data/locations.json (to be bundled with addon)
    contract.atmosphere_stops = ContractParser.count_atmosphere_stops(contract.delivery)

    return contract
end

-- Count how many delivery locations require an atmospheric landing.
-- TODO: replace with a lookup against a bundled location database (locations.json)
-- For now, uses a heuristic: location names containing common surface keywords.
-- This is explicitly approximate and will be replaced.
function ContractParser.count_atmosphere_stops(delivery_locations)
    if not delivery_locations then return 0 end

    -- Rough surface-location heuristics. Replace with proper location data lookup.
    local surface_keywords = {
        "landing zone", "lz ", "port olisar", "lorville", "area18", "new babbage",
        "orison", "levski", "grim hex", "tressler", "surface",
    }

    local count = 0
    for _, location in ipairs(delivery_locations) do
        local loc_lower = location:lower()
        for _, keyword in ipairs(surface_keywords) do
            if loc_lower:find(keyword, 1, true) then
                count = count + 1
                break
            end
        end
    end
    return count
end

-- Get the contract currently highlighted/selected in the terminal.
-- Returns a single parsed contract table, or nil if nothing is selected.
-- STUB: Replace CIG_API.GetSelectedContract with actual game API.
function ContractParser.get_selected_contract()
    -- TODO: replace with actual CIG game API
    -- Speculative:
    --   local raw = CIG_API.GetSelectedContract()
    --   return raw and ContractParser.parse_raw(raw) or nil
    return nil
end

return ContractParser
