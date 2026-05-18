# Phase 2 Changelog

Generated: 2026-05-16

## Completed
- Added `route_edge.schema.json`.
- Created `route_edges.json` with topology-only route edges.
- Created `adjacency_matrix.json` for graph traversal.
- Added Lagrange placeholder nodes for CRU-L1 through CRU-L5, HUR-L1 through HUR-L5, ARC-L1 through ARC-L5, and MIC-L1 through MIC-L5.
- Added derived traversal penalties for atmosphere, spline, approach, docking/landing, freight elevator, dead-leg risk, and route complexity.
- Preserved the rule that QT time is runtime-derived from quantum drive data and is not stored as a fixed edge value.

## Edge Classes Added
- system_to_planet
- planet_to_moon
- planet_to_orbital_station
- planet_to_city
- planet_to_lagrange
- orbital_station_to_city
- orbital_station_to_lagrange
- moon_to_outpost
- planet_to_surface_outpost
- lagrange_chain

## Assumptions
- Parent-child hierarchy from Phase 1 can safely seed initial graph edges.
- Surface destinations are initially penalized for atmosphere, spline, approach, and landing complexity.
- Orbital station and Lagrange routing is initially low complexity until distance and station-specific behaviour are ingested.
- Lagrange nodes are placeholders for topology and later station enrichment.

## Unresolved Fields
- Exact distances.
- Exact QT travel times by drive.
- Actual station presence at every Lagrange point.
- Freight elevator presence and behaviour per location.
- Hull-B physical and practical compatibility per location.
- Current patch-specific broken or unreliable routes.
- Interdiction and server-state effects.

## Derived Operational Scores
All traversal penalties in Phase 2 are heuristics. They are intended for preliminary Hull-B routing and must be refined in later phases.

## Next Phase
Phase 3 should ingest operational penalties in more detail:
- atmosphere entry/exit cost
- spline routing cost
- freight elevator availability
- cargo handling complexity
- location-specific dead-leg risk
- congestion and known operational hazards
