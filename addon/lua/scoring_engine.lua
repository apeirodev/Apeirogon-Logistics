-- scoring_engine.lua
-- Deterministic contract scorer for Apeirogon Logistics.
-- Lua port of developer/tools/deterministic_scorer.py
--
-- Logic is identical to the Python scorer. Weights come from scoring_config.lua.
-- No game API dependencies -- this file is fully portable Lua 5.1.
--
-- Usage:
--   local result = ScoringEngine.score_contract(contract, context)
--   -- result.score   : integer 0-100
--   -- result.verdict : "ACCEPT" | "DEFER" | "REJECT"
--   -- result.factors : table of factor name → contribution

local ScoringConfig = require("ApeirogonLogistics.scoring_config")
local Utils         = require("ApeirogonLogistics.utils")

local ScoringEngine = {}

local function get_ship_mod(ship_key, factor)
    if not ship_key then return 1.0 end
    local mods = ScoringConfig.ship_modifiers[ship_key]
    if not mods then return 1.0 end
    return mods[factor] or 1.0
end

local function get_issuer_mod(issuer_key, factor)
    if not issuer_key then return 1.0 end
    local mods = ScoringConfig.issuer_modifiers[issuer_key]
    if not mods then return 1.0 end
    return mods[factor] or 1.0
end

-- Score a single contract.
--
-- contract : table -- fields from the internal contract format (see contract_parser.lua)
-- context  : table -- scoring context built from the full batch
--   {
--     ship              = "hull-b",          -- string, lower-case ship key
--     issuer            = "covalex",         -- string, lower-case issuer key
--     same_pickup_count = 3,                 -- how many contracts share this pickup
--     destination_overlap = true,            -- any delivery overlaps with other contracts
--     orbital_loop      = true,              -- all stops are orbital (no atmosphere)
--     route_continuity  = true,              -- pickups chain without dead legs
--     cargo_panel_clarity = true,            -- mission set maps cleanly to cargo panels
--     atmosphere_stops  = 0,                 -- count of atmosphere delivery stops
--     freight_complexity = false,            -- true if freight handling is difficult
--     dead_leg          = false,             -- must fly empty to reach pickup
--     delivery_count    = 2,                 -- number of distinct delivery destinations
--     total_stops       = 3,                 -- total stops in the combined route
--     fatigue_level     = 0,                 -- 0 = none, 1 = mild, 2 = heavy
--     congested_stations = 0,               -- count of congested stations on route
--     unloading_cognitive_load = false,      -- true if unloading will be confusing
--     chain_collapse_risk = false,           -- true if route has fragile dependencies
--     unresolved_count  = 0,                 -- number of UNRESOLVED fields
--   }
--
-- Returns: { score = int, verdict = string, factors = table }
function ScoringEngine.score_contract(contract, context)
    local ship_key   = context.ship   and Utils.normalize_key(context.ship)   or nil
    local issuer_key = context.issuer and Utils.normalize_key(context.issuer) or nil
    local w          = ScoringConfig.default_weights

    local score   = ScoringConfig.base_score
    local factors = {}

    -- GOOD FACTORS

    -- same_pickup: +weight per extra stacked mission at the same pickup
    local stack_bonus = (context.same_pickup_count or 1) - 1
    if stack_bonus > 0 then
        local mod = get_issuer_mod(issuer_key, "same_pickup")
                  * get_ship_mod(ship_key, "same_pickup")
        local contribution = w.same_pickup * mod * stack_bonus
        score = score + contribution
        factors.same_pickup = contribution
    end

    -- destination_overlap: deliveries shared across stacked contracts
    if context.destination_overlap then
        local mod = get_issuer_mod(issuer_key, "destination_overlap")
                  * get_ship_mod(ship_key, "destination_overlap")
        local contribution = w.destination_overlap * mod
        score = score + contribution
        factors.destination_overlap = contribution
    end

    -- orbital_loop: whole route stays in orbital space
    if context.orbital_loop then
        local mod = get_issuer_mod(issuer_key, "orbital_loop")
                  * get_ship_mod(ship_key, "orbital_loop")
        local contribution = w.orbital_loop * mod
        score = score + contribution
        factors.orbital_loop = contribution
    end

    -- issuer_alignment: bonus for a recognized issuer
    if issuer_key and issuer_key ~= "" then
        local mod = get_issuer_mod(issuer_key, "issuer_alignment")
                  * get_ship_mod(ship_key, "issuer_alignment")
        local contribution = w.issuer_alignment * mod
        score = score + contribution
        factors.issuer_alignment = contribution
    end

    -- ship_suitability: bonus when ship is well-matched to mission type
    if ship_key and ship_key ~= "" then
        local mod = get_ship_mod(ship_key, "ship_suitability")
        local contribution = w.ship_suitability * mod
        score = score + contribution
        factors.ship_suitability = contribution
    end

    -- route_continuity: pickups chain without empty legs between them
    if context.route_continuity then
        local mod = get_issuer_mod(issuer_key, "route_continuity")
                  * get_ship_mod(ship_key, "route_continuity")
        local contribution = w.route_continuity * mod
        score = score + contribution
        factors.route_continuity = contribution
    end

    -- cargo_panel_clarity: mission set maps cleanly to cargo panel sections
    if context.cargo_panel_clarity then
        local mod = get_ship_mod(ship_key, "cargo_panel_clarity")
        local contribution = w.cargo_panel_clarity * mod
        score = score + contribution
        factors.cargo_panel_clarity = contribution
    end

    -- BAD FACTORS

    -- atmosphere: each stop requiring an atmospheric landing
    local atmo_stops = context.atmosphere_stops or 0
    if atmo_stops > 0 then
        local mod = get_ship_mod(ship_key, "atmosphere")
        local contribution = w.atmosphere * mod * atmo_stops
        score = score + contribution    -- w.atmosphere is negative
        factors.atmosphere = contribution
    end

    -- freight: difficult cargo handling (heavy, oversized, fragile)
    if context.freight_complexity then
        local mod = get_ship_mod(ship_key, "freight")
        local contribution = w.freight * mod
        score = score + contribution
        factors.freight = contribution
    end

    -- dead_leg: must fly empty to reach the pickup location
    if context.dead_leg then
        local mod = get_issuer_mod(issuer_key, "dead_leg")
                  * get_ship_mod(ship_key, "dead_leg")
        local contribution = w.dead_leg * mod
        score = score + contribution
        factors.dead_leg = contribution
    end

    -- fragmentation: each delivery stop beyond the first
    local extra_deliveries = math.max(0, (context.delivery_count or 1) - 1)
    if extra_deliveries > 0 then
        local mod = get_ship_mod(ship_key, "fragmentation")
        local contribution = w.fragmentation * mod * extra_deliveries
        score = score + contribution
        factors.fragmentation = contribution
    end

    -- stop_density: total stops beyond 2 (pickup + first delivery)
    local dense_stops = math.max(0, (context.total_stops or 1) - 2)
    if dense_stops > 0 then
        local mod = get_ship_mod(ship_key, "stop_density")
        local contribution = w.stop_density * mod * dense_stops
        score = score + contribution
        factors.stop_density = contribution
    end

    -- fatigue: tiringness of multi-leg routes (0 = none, 1 = mild, 2 = heavy)
    local fatigue = context.fatigue_level or 0
    if fatigue > 0 then
        local mod = get_ship_mod(ship_key, "fatigue")
        local contribution = w.fatigue * mod * fatigue
        score = score + contribution
        factors.fatigue = contribution
    end

    -- congestion: congested stations add delay and friction
    local congested = context.congested_stations or 0
    if congested > 0 then
        local mod = get_issuer_mod(issuer_key, "congestion")
        local contribution = w.congestion * mod * congested
        score = score + contribution
        factors.congestion = contribution
    end

    -- unloading_cognitive_load: confusing or error-prone unload situation
    if context.unloading_cognitive_load then
        local contribution = w.unloading_cognitive_load
        score = score + contribution
        factors.unloading_cognitive_load = contribution
    end

    -- chain_collapse: fragile dependencies that could break the run
    if context.chain_collapse_risk then
        local contribution = w.chain_collapse
        score = score + contribution
        factors.chain_collapse = contribution
    end

    -- unresolved fields: each field the player couldn't read costs -2
    local unresolved = context.unresolved_count or 0
    if unresolved > 0 then
        local contribution = -2 * unresolved
        score = score + contribution
        factors.unresolved = contribution
    end

    score = Utils.clamp(score, 0, 100)
    local rounded = Utils.round(score)

    local verdict
    if rounded >= ScoringConfig.score_bands.accept_threshold then
        verdict = "ACCEPT"
    elseif rounded >= ScoringConfig.score_bands.defer_threshold then
        verdict = "DEFER"
    else
        verdict = "REJECT"
    end

    return {
        score   = rounded,
        verdict = verdict,
        factors = factors,
    }
end

-- Determine the risk band for a scored result.
function ScoringEngine.risk_band(score)
    if score >= ScoringConfig.score_bands.risk_low_threshold then
        return "low"
    elseif score >= ScoringConfig.score_bands.risk_medium_threshold then
        return "medium"
    else
        return "high"
    end
end

-- Build scoring context from a batch of contracts and the player's current state.
-- Call this once per batch before scoring individual contracts.
-- player_state: { ship = "hull-b", location = "Everus Harbor" }
-- contracts: array of parsed contract tables
function ScoringEngine.build_context(contracts, player_state)
    local contexts = {}
    local ship_key = player_state and Utils.normalize_key(player_state.ship or "") or nil

    -- Count contracts per pickup location for same_pickup_count
    local pickup_counts = {}
    for _, c in ipairs(contracts) do
        local pickup = c.pickup or ""
        pickup_counts[pickup] = (pickup_counts[pickup] or 0) + 1
    end

    -- Collect all delivery locations for overlap detection
    local all_deliveries = {}
    for _, c in ipairs(contracts) do
        for _, d in ipairs(c.delivery or {}) do
            all_deliveries[d] = (all_deliveries[d] or 0) + 1
        end
    end

    local player_location = player_state and (player_state.location or "") or ""

    for i, c in ipairs(contracts) do
        local issuer_key = Utils.normalize_key(c.issuer or "")
        local pickup     = c.pickup or ""
        local deliveries = c.delivery or {}

        -- Dead leg: pickup is not the player's current location
        local dead_leg = (pickup ~= "" and pickup ~= player_location)

        -- Destination overlap: any delivery appears in more than one contract
        local dest_overlap = false
        for _, d in ipairs(deliveries) do
            if (all_deliveries[d] or 0) > 1 then
                dest_overlap = true
                break
            end
        end

        -- Atmosphere stops: count delivery destinations that are surface locations
        -- TODO: cross-reference against locations.json atmospheric flag when available
        local atmo_stops = c.atmosphere_stops or 0

        -- Orbital loop: no atmosphere stops anywhere in this contract
        local orbital_loop = (atmo_stops == 0)

        -- Total stops: pickup + all deliveries
        local total_stops = 1 + #deliveries

        contexts[i] = {
            ship                     = ship_key,
            issuer                   = issuer_key,
            same_pickup_count        = pickup_counts[pickup] or 1,
            destination_overlap      = dest_overlap,
            orbital_loop             = orbital_loop,
            route_continuity         = not dead_leg,
            cargo_panel_clarity      = (#deliveries <= 4),  -- panels available for clean assignment
            atmosphere_stops         = atmo_stops,
            freight_complexity       = c.freight_complexity or false,
            dead_leg                 = dead_leg,
            delivery_count           = #deliveries,
            total_stops              = total_stops,
            fatigue_level            = math.max(0, total_stops - 3),  -- 0 for simple routes
            congested_stations       = c.congested_stations or 0,
            unloading_cognitive_load = (#deliveries > 4),
            chain_collapse_risk      = c.chain_collapse_risk or false,
            unresolved_count         = #(c.unresolved_fields or {}),
        }
    end

    return contexts
end

return ScoringEngine
