COVALEX REPUTATION GUIDE: RANK FOCUS AT ANY RANK

This guide covers the single-leg partial submit strategy for grinding Covalex reputation
efficiently at any rank. The mechanic works the same whether you are at Associate,
Member, Senior, or anywhere in between. The threshold and submission rules do not
change with rank -- only contract size does.

---

SHIP SELECTION FOR REP GRINDING

Not every ship is suitable for rep grinding mode. The right ship makes a
material difference in runs per session.

OPTIMAL SHIP: Hull-B

External panel loading, confirmed docking and freight elevator compatibility
at all Covalex Senior destinations (Port Tressler, Baijini Point, Seraphim
Station, Everus Harbor), and 5 contracts per run at minimum qualifying loads.
If you have a Hull-B, use it.

HARD DISQUALIFIERS (these ships cannot be used for rep grinding):

  Hull-C -- cannot land at standard orbital stations when loaded. A single
  failed delivery wastes the entire run.

  C2/M2/A2 Hercules, Caterpillar, Starlancer MAX/TAC, Freelancer MAX,
  Constellation Taurus, Hermes, Valkyrie, Asgard, Starfarer, Starfarer
  Gemini, Ironclad Assault -- all use ramp loading at freight elevators.
  Ramp loading adds significant time per stop versus external panel ships.
  In a workflow where you are making one delivery per contract and submitting
  immediately, this overhead compounds across every run in a session.

  Hull-D, Hull-E, Galaxy, Banu Merchantman -- not currently flyable in
  Alpha 4.8.

ALTERNATIVES (higher potential, require in-game verification first):

  Railen (640 SCU, 6-7 contracts per run potential): Xi'an grav-lev cargo
  handling at human freight elevators has not been confirmed to work correctly
  in Alpha 4.8. Before using the Railen, verify at all 4 Senior destinations:
  freight elevator access works, 16 SCU containers load/unload without bugs,
  and pad availability supports the ship's footprint. If all 3 confirm, the
  Railen supersedes the Hull-B.

  Ironclad (2204 SCU, entire contract pool per run potential): external cargo
  handling avoids the ramp penalty. Station docking compatibility at Covalex
  Senior destinations is unconfirmed. Verify docking and freight elevator
  access at all 4 stations before using it for rep grinding. If compatible,
  the Ironclad eliminates the per-run ceiling entirely.

  RAFT (192 SCU): compatible loading method but only 2 contracts per run.
  Rep grinding efficiency is too low to recommend.

If you tell your AI which ship you are using when you activate rank mode, it
will run this check automatically and flag any compatibility issues before
you start.

---

THE CORE MECHANIC

You do not have to complete all legs of a Covalex contract to earn reputation.

If you deliver cargo to a single destination that represents 25% or more of the
contract's total cargo volume, then manually submit the contract via the in-game
contract manager, you receive Covalex reputation credit.

Use 26% as your working threshold -- a one-point safety margin above the game floor.

PAYOUT TIERS (approximate, not confirmed exact):

  Cargo delivered     Rep gain       Credit payout
  ---------------     --------       -------------
  25 to 50% of total  ~90 to 100%    ~15% of reward
  51 to 75% of total  ~90 to 100%    ~45% of reward
  76 to 99% of total  ~90 to 100%    ~76% of reward
  100% of total       Full           Full

At the 25%+ tier you get nearly full reputation for roughly 15% of the credit
reward. This is a deliberate trade-off: slower credit accumulation, faster
rank progression.

---

CONTRACT PATTERNS BY RANK

The partial submit mechanic works at every Covalex rank. Contract structure
varies by rank, but the 26% rule is the same.

Lower ranks (Associate, Member):
  Contracts tend to be smaller in total SCU and may have fewer legs -- sometimes
  just 2 to 3 destinations rather than 4. With fewer legs each leg is naturally a
  larger share of the total, so hitting 26% is often easier. Planetary and moon
  surface deliveries may appear in the mix.

Higher ranks (Senior, Master):
  Contracts grow in total SCU and typically run stellar routes between Lagrange
  stations and main orbital stations. Four legs is common. Individual legs can
  still represent well over 26% of the total.

At any rank your job at the kiosk is the same: check whether any single leg
represents 26% or more of the total cargo volume.

If yes: accept the contract. At the pickup, load only the minimum qualifying
SCU (26% of the contract total, rounded up) -- not necessarily the entire leg.
Fly to that one destination, deliver, submit manually.

If no: abandon the contract immediately. There is no rep penalty for abandoning
before accepting. A new offer will appear.

MINIMUM QUALIFYING LOAD:

You do not have to load the entire highest-SCU leg. You only need to load
enough to reach 26% of the contract's total SCU.

Example:
  Contract total: 200 SCU across 4 legs
  Best leg: 80 SCU to Everus Harbor
  26% of 200 = 52 SCU (minimum qualifying load)
  Space saved: 80 - 52 = 28 SCU free for another contract

Loading the minimum frees ship capacity to stack additional contracts in the
same run. Your AI calculates this for you automatically in rank mode.

---

HOW TO STACK MULTIPLE CONTRACTS

If you can accept two or more contracts with the same pickup location, you can
run them in a single trip by loading only the minimum qualifying SCU for each.

- Accept all VIABLE contracts at the kiosk
- At the pickup location, load the minimum qualifying SCU for each contract's
  recommended leg -- not the full leg
- Deliver each load to its recommended destination
- Submit each contract in the contract manager after its delivery

Your AI will show a stacking summary when you are in rank mode: the sum of
all minimum qualifying SCU loads across VIABLE contracts versus your confirmed
ship capacity. This tells you exactly whether all the minimums fit in one run.

Verify your ship's actual cargo capacity from the in-game loadout screen before
accepting. Do not guess at capacity -- it changes with patches.

---

USING YOUR AI IN RANK MODE

Your AI assistant can analyze contract screenshots and identify the best single
leg for each contract automatically.

To activate:
  Tell your AI: "covalex rank mode" (works at any Covalex rank)

The AI will ask you to paste screenshots of all available master-rank contracts.
For each contract it will show:

  Contract [ref] -- [commodity] -- [total SCU] SCU total
  Recommended leg: [pickup] --> [destination] | [commodity]
    Full leg: [Y] SCU ([Y/total]%)
    Minimum for rep: [Z] SCU (26% of total, rounded up)
    Space saved by loading minimum: [Y minus Z] SCU
  Payout tier at minimum load: ~15% credits, ~90-100% rep
  Status: VIABLE / NOT VIABLE

It will then rank all VIABLE contracts by minimum qualifying SCU and show a
stacking summary: total minimum SCU across all contracts versus your confirmed
ship capacity.

If a contract is marked NOT VIABLE -- no single leg reaches 26% -- abandon it
at the kiosk and show the AI fresh screenshots of the replacement offers.

To return to normal scoring: tell your AI "exit rank mode" or start a new session.

---

WORKFLOW CHECKLIST

  [ ] Open the contracts kiosk
  [ ] Activate rank mode with your AI: "covalex rank mode"
  [ ] Paste screenshots of all visible master-rank contracts
  [ ] Review the AI's ranked output
  [ ] Abandon any NOT VIABLE contracts at the kiosk
  [ ] Accept VIABLE contracts
  [ ] At pickup: load only the minimum qualifying SCU per contract (not the full leg)
  [ ] Fly to the recommended delivery destination
  [ ] Deliver cargo
  [ ] Open contract manager -- manually submit the contract
  [ ] Repeat from the top for the next run

---

IMPORTANT NOTES

Credits vs. Reputation: At the 25%+ tier you earn very few credits (~15% of
the listed reward). This strategy is for rank grinding, not credit farming.
It works at every rank. If you need credits, run full contracts instead.

Lower-rank contracts and smaller SCU: at earlier ranks the minimum qualifying
load will be lower in absolute SCU terms, so a smaller ship can run this
strategy just as effectively. The AI calculates the minimum for whatever
contract size you are working with.

Abandoning is free: Abandoning a contract you have NOT yet accepted costs
nothing. No rep penalty, no credit loss. If the contracts on offer are all
NOT VIABLE, abandon them all and wait for the pool to refresh.

Manual submit is required: The game does not auto-submit a contract when you
deliver to only one of four destinations. You must open the contract manager
and submit it yourself. If you forget and fly away, the partial delivery
credit may be lost.

Capacity check: Always confirm your ship's actual cargo capacity from the
in-game loadout screen before accepting. Do not rely on any value in this
guide or from your AI -- ship capacities change with patches.
