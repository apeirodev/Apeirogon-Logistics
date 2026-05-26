# External Data Sources

**Status:** Documented for future integration. No external API calls are made by the current tool suite.
**Last reviewed:** 2026-05-26
**Next review trigger:** Before integrating any external API, or when a new Star Citizen patch drops.

---

## Overview

Apeirogon Logistics currently operates entirely from user-supplied data -- contract
details read from screenshots, numeric values confirmed by the player before use.
This is intentional: it eliminates third-party availability dependencies and makes
the tool work offline.

Two external sources have been evaluated and documented here for future integration.
Neither is integrated yet. When integrated, all external data must flow through the
project's governance metadata system and must be tagged with appropriate
`source_class`, `advisory_only`, and provenance fields.

---

## Source 1: UEX Corporation API

**URL:** https://uexcorp.space/api/documentation/
**API endpoint base:** https://portal.uexcorp.space/api/
**Token management:** https://uexcorp.space/api/apps
**Trust classification:** `external_api_crowdsourced`
**Advisory only:** always true

### What it provides

Live commodity pricing at all Stanton trade ports, collected from crowdsourced
player reports. Data is updated continuously as players submit prices via the
UEX companion tools. Covers buy/sell prices, port fee data, and trade route
analysis across all accessible locations.

Endpoints relevant to this project:

| Endpoint | What it returns |
|---|---|
| `/tradeports` | All locations with buy/sell prices in a single call |
| `/commodities` | Commodity definitions and current aggregate pricing |
| `/commodities_prices` | Per-commodity prices by location |
| `/commodities_prices_history` | Historical price trends |
| `/user_trades` | Community-submitted individual trade reports |

### Authentication

Free API key required. Create an account at uexcorp.space, then create an
application token at https://uexcorp.space/api/apps. The token is passed as a
header or query parameter (see API documentation for current spec).

**Key type:** Personal access token (PAT), free tier
**Rate limits:** Not publicly documented; use conservatively
**Key storage:** Environment variable only -- never commit to repo (per rule LOG-01,
AI-security.md). Use `UEX_API_KEY` as the environment variable name.

### Data quality and limitations

- **Patch lag:** Data lags behind game patches. After a patch, prices may be stale
  until players submit updated reports. Check the `updated_at` timestamp on each
  price record before using it.
- **Crowdsourced accuracy:** Individual reports can be wrong. UEX has correction
  mechanisms, but spot-check any price that looks anomalous.
- **Not official:** CIG does not provide or endorse this data. Prices can change
  in-patch without warning.
- **Coverage gaps:** Newly added locations or commodities may have no data until
  players report prices.

### Governance metadata template for UEX data

When UEX data is used in any tool output, the governance_metadata block must
include:

```json
{
  "source_class": "external_api_crowdsourced",
  "advisory_only": true,
  "contributor_trust_tier": "T2",
  "verification_status": "not_human_verified",
  "provenance_chain": [
    {
      "type": "external_api",
      "source": "uexcorp.space",
      "endpoint": "/tradeports",
      "fetched_at": "<ISO-8601 timestamp>",
      "patch_era": "<SC patch version at time of fetch>"
    }
  ]
}
```

Never merge UEX prices directly into `sourced_facts`. Keep them in a separate
`external_prices` field in the output, tagged with the above governance block.
A human player must confirm before any external price influences a scoring decision
(per rule AI-01, SRC-01).

### Planned integration scope

- `tools/fetch_trade_prices.py` -- CLI tool that queries UEX for prices at a
  given location and returns a governance-tagged JSON block
- Provider guidance update -- instruct the AI to note when a price appears in
  `external_prices` so the player can cross-reference against their screenshot
- Hallucination guardrail enhancement -- when a field is present in `external_prices`
  but absent from user-supplied data, flag as `CROSS_REFERENCE_AVAILABLE` rather
  than UNRESOLVED, prompting the player to confirm the external price

---

## Source 2: Star Citizen Wiki API

**URL:** https://api.star-citizen.wiki
**Documentation:** https://docs.star-citizen.wiki
**GitHub:** https://github.com/StarCitizenWiki/API
**Trust classification:** `external_api_community_wiki`
**Advisory only:** always true

### What it provides

Static game data extracted from Star Citizen's game files (p4k archives) and
maintained by the Star Citizen Wiki community. Updated daily when new game data
is available. Covers ships, vehicles, items, commodities, manufacturers, locations,
and starmap data.

Endpoints relevant to this project:

| Endpoint | What it returns |
|---|---|
| `/api/vehicles` | Ship specifications including cargo capacity |
| `/api/items` | In-game items and commodities |
| `/api/starmap` | Location hierarchy and jump point data |
| `/api/vehicles?filter[name]=Hull-B` | Filtered ship lookup |

### Authentication

Public endpoints available without authentication. Some advanced features may
require a key (the API uses Laravel Sanctum). The public endpoints covering ship
and location data do not appear to require a token based on current documentation.

**Key type:** Optional; public access available
**Key storage:** Environment variable `SC_WIKI_API_KEY` if a key is needed

### Data quality and limitations

- **Static only:** This API provides game definition data, not live gameplay state.
  It cannot tell you which contracts are available at a terminal.
- **Patch lag:** Updated from game file extraction cycles. May lag a day or more
  behind a live patch.
- **Not official:** Community-maintained. Star Citizen Wiki is not affiliated with CIG.
- **High quality:** The StarCitizenWiki project has 2,900+ commits and is one of the
  most comprehensive SC data sources available.

### Planned integration scope

- Automated `ship_profiles.json` refresh -- instead of manually updating ship cargo
  capacities after each patch, a maintenance script can query the Wiki API and flag
  differences for human review before applying
- Location data validation -- cross-reference the project's location hierarchy
  against the Wiki API after each SC patch to catch renamed or removed locations

### Governance metadata template for Wiki API data

```json
{
  "source_class": "external_api_community_wiki",
  "advisory_only": true,
  "contributor_trust_tier": "T2",
  "verification_status": "not_human_verified",
  "provenance_chain": [
    {
      "type": "external_api",
      "source": "api.star-citizen.wiki",
      "endpoint": "/api/vehicles",
      "fetched_at": "<ISO-8601 timestamp>",
      "patch_era": "<SC patch version>"
    }
  ]
}
```

---

## Source 3: SC Trade Tools (reference only -- do not integrate directly)

**URL:** https://sc-trade.tools
**GitHub:** https://github.com/EtienneLamoureux/sc-trade-tools

SC Trade Tools is a community platform for trade route optimization. It wraps
UEX data and adds route optimization algorithms. It is documented here as a
reference and design comparison, not as a data source to integrate.

**Reason for non-integration:** Integrating SC Trade Tools would create a
dependency on a third-party service that itself depends on UEX. Integrating
UEX directly is more reliable and eliminates the intermediary. SC Trade Tools'
route optimization algorithms are a useful design reference, but Apeirogon
Logistics implements its own scoring logic with different objectives.

---

## Source 4: RSI Official Telemetry (not applicable)

**URL:** https://robertsspaceindustries.com/en/telemetry

RSI's telemetry dashboard exposes aggregate player hardware performance metrics
only (FPS distributions, system specs). It does not expose contract data, pricing,
location state, or any gameplay information. Not applicable to this project.

---

## Source 5: spectrum.py (not applicable)

**URL:** https://github.com/henry232323/spectrum.py

Python library for RSI's Spectrum chat platform. No relevance to hauling contract
data, pricing, or route scoring. Not applicable to this project.

---

## Trust hierarchy for data in this project

When any external data is used, it must be clearly distinguished from user-supplied
data in all output. The trust hierarchy from highest to lowest is:

| Class | Description | Examples |
|---|---|---|
| `sourced_facts` | Player-confirmed values read directly from the game | Reward, cargo SCU, pickup location from screenshot |
| `external_api_community_wiki` | Static game data from community extraction | Ship cargo capacity from Wiki API |
| `external_api_crowdsourced` | Live prices from community reports | Commodity prices from UEX |
| `ocr_extraction` | AI-parsed values from screenshot | Unconfirmed mission fields |
| `ai_recommendation` | AI analysis output | Scoring recommendations, route suggestions |

Never merge lower-trust data into higher-trust fields. Never merge any external
API data into `sourced_facts`. A player confirmation step is required before
external prices are treated as authoritative for any contract decision.

---

## Environment variables required (future)

When integration is implemented, the following environment variables will be needed:

| Variable | Source | Required | Notes |
|---|---|---|---|
| `UEX_API_KEY` | uexcorp.space/api/apps | Yes, when UEX integration is active | Free account and app token |
| `SC_WIKI_API_KEY` | docs.star-citizen.wiki | No -- public access likely sufficient | Only needed if rate-limited |

Never pass API keys as CLI arguments (visible in process list) or commit them
to the repository. Read from environment only, per rule LOG-01 and ai-security.md.

---

## Version history

- **0.64.2** -- Initial document. Both sources evaluated, documented for future
  integration. No API calls made by current tools.
