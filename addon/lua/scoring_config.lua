-- scoring_config.lua
-- Scoring weights, ship modifiers, and issuer modifiers for Apeirogon Logistics.
-- Lua translation of developer/runtime/scoring_config.json.
--
-- KEEP IN SYNC: when tuning weights in scoring_config.json, update this file too.
-- The Python scorer and Lua scorer must produce identical results for the same input.
-- No game API dependencies -- this file is fully portable Lua 5.1.

local ScoringConfig = {}

ScoringConfig.base_score = 50

ScoringConfig.score_bands = {
    accept_threshold      = 70,
    defer_threshold       = 45,
    risk_low_threshold    = 75,
    risk_medium_threshold = 50,
}

ScoringConfig.default_weights = {
    same_pickup              =  16,
    destination_overlap      =  12,
    orbital_loop             =  12,
    issuer_alignment         =   8,
    ship_suitability         =  10,
    route_continuity         =  10,
    cargo_panel_clarity      =   8,
    atmosphere               = -12,
    freight                  =  -8,
    dead_leg                 = -15,
    fragmentation            = -12,
    stop_density             =  -6,
    fatigue                  =  -7,
    congestion               =  -8,
    unloading_cognitive_load =  -7,
    chain_collapse           = -14,
}

ScoringConfig.issuer_modifiers = {
    ["covalex"] = {
        issuer_alignment = 1.10,
        orbital_loop     = 1.05,
        route_continuity = 1.05,
    },
    ["ling"] = {
        destination_overlap = 1.05,
        same_pickup         = 1.03,
    },
    ["ling family"] = {
        destination_overlap = 1.05,
        same_pickup         = 1.03,
    },
    ["red wind"] = {
        dead_leg   = 1.10,
        congestion = 1.05,
    },
}

ScoringConfig.ship_modifiers = {
    ["hull-b"] = {
        freight             = 1.05,
        fragmentation       = 1.10,
        cargo_panel_clarity = 1.15,
        ship_suitability    = 1.05,
    },
    ["hull-c"] = {
        freight          = 1.25,
        stop_density     = 1.20,
        ship_suitability = 1.15,
    },
    ["taurus"] = {
        ship_suitability = 1.05,
        fatigue          = 0.95,
    },
    ["caterpillar"] = {
        freight          = 1.10,
        ship_suitability = 1.10,
    },
    ["freelancer max"] = {
        ship_suitability = 1.02,
        fatigue          = 0.98,
    },
    ["starlancer max"] = {
        ship_suitability = 1.05,
        fatigue          = 0.95,
        freight          = 1.03,
    },
    ["starlancer tac"] = {
        ship_suitability = 0.88,
    },
    ["raft"] = {
        ship_suitability = 1.05,
        freight          = 1.05,
        dead_leg         = 0.95,
    },
    ["valkyrie"] = {
        ship_suitability = 0.90,
        atmosphere       = 0.85,
        fatigue          = 0.92,
    },
    ["asgard"] = {
        ship_suitability = 0.95,
        atmosphere       = 0.85,
        fatigue          = 0.95,
        freight          = 1.03,
    },
    ["a2 hercules"] = {
        ship_suitability = 0.85,
        atmosphere       = 0.90,
        freight          = 1.05,
    },
    ["m2 hercules"] = {
        ship_suitability = 1.05,
        atmosphere       = 0.90,
        freight          = 1.10,
        fragmentation    = 1.08,
    },
    ["c2 hercules"] = {
        ship_suitability = 1.08,
        atmosphere       = 0.88,
        freight          = 1.10,
        fragmentation    = 1.08,
    },
    ["starfarer"] = {
        ship_suitability = 0.88,
        freight          = 1.05,
        stop_density     = 1.10,
    },
    ["starfarer gemini"] = {
        ship_suitability = 0.85,
        freight          = 1.05,
        stop_density     = 1.10,
    },
    ["ironclad"] = {
        ship_suitability = 1.10,
        freight          = 1.15,
        stop_density     = 1.25,
        fragmentation    = 1.15,
    },
    ["ironclad assault"] = {
        ship_suitability = 0.90,
        freight          = 1.10,
        stop_density     = 1.20,
    },
    ["hermes"] = {
        ship_suitability = 1.05,
        dead_leg         = 0.90,
        fatigue          = 0.92,
    },
    ["galaxy"] = {
        ship_suitability = 1.05,
        stop_density     = 1.05,
        freight          = 1.05,
    },
    ["railen"] = {
        ship_suitability = 1.05,
        freight          = 1.08,
        atmosphere       = 0.90,
    },
    ["hull-d"] = {
        ship_suitability = 1.15,
        freight          = 1.40,
        stop_density     = 1.35,
        fragmentation    = 1.25,
    },
    ["hull-e"] = {
        ship_suitability = 1.20,
        freight          = 1.60,
        stop_density     = 1.50,
        fragmentation    = 1.40,
    },
    ["merchantman"] = {
        ship_suitability    = 1.20,
        freight             = 1.20,
        destination_overlap = 1.10,
    },
}

return ScoringConfig
