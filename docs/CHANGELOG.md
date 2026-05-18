# Phase 1 Changelog

Generated: 2026-05-16

## Completed
- Created canonical JSON schema for location records.
- Created source registry with official and community source classifications.
- Seeded Stanton system, star, 4 planets, 12 moons, major orbital stations, landing zones, and surfaced outposts visible in the initial Stanton location list.
- Added alias map for canonical and common/source names.
- Added derived operational fields separately from sourced facts.

## Assumptions
- Surface locations are marked as atmospheric and spline-dependent by default for hauling optimisation.
- Orbital stations are given high expected hauling-efficiency class as a derived score, not a sourced fact.
- Outposts are marked as route-poison-if-single-stop as a derived operational heuristic, not a sourced fact.
- Hull-B compatibility remains unknown until landing, pad, hangar, freight elevator, and current patch behaviour are validated.

## Unresolved Fields
- Exact cargo terminal and freight elevator availability per location.
- Exact Hull-B physical compatibility per location.
- Current patch-specific mission availability per location.
- Lagrange station list and canonical station names.
- Quantum distances and runtime ETA calculations.
- Route-edge graph and adjacency matrix.

## Derived Operational Scores
- `atmosphere_penalty`: initial heuristic for routing cost.
- `expected_hauling_efficiency_class`: initial heuristic for route acceptance decisions.
- `confidence`: marks whether a field is direct sourced data or derived_general.

## Next Phase
- Phase 2 should build `route_edges.json` and the Stanton adjacency graph.
