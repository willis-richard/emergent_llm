"""
Strategy descriptions for public_goods_prompt.

Generated with:
- Provider: Anthropic
- Model: claude-haiku-4-5
"""


description_COLLECTIVE_1 = '''
# ADAPTIVE COLLECTIVE STRATEGY FOR PUBLIC GOODS GAME

## CORE PRINCIPLE
Maximize collective welfare by fostering cooperation through reciprocal accountability while protecting against exploitation. The strategy balances optimism about cooperation with realistic defection-detection and calibrated responses.

## DECISION RULE (GENERAL CASE)

**Cooperate if and only if:**
1. The observed cooperation rate in the previous round exceeds a dynamic threshold, AND
2. No single player has defected consistently while benefiting from others' contributions

**Otherwise, defect.**

The dynamic threshold follows this logic:
- If cooperation_rate_last_round ≥ (k-1)/k, cooperate (this is the breakeven point where cooperation pays individually)
- If cooperation_rate_last_round < (k-1)/k, defect
- Exception: In very early rounds (rounds 1-2), use a more generous threshold of (k-2)/k to bootstrap cooperation

## HANDLING EDGE CASES

**Round 1 (First Round):**
Cooperate unconditionally. This is the only move where we have no history to guide us. Cooperation signals intent to establish a cooperative equilibrium and tests whether other players are cooperative-minded.

**Final Round (Round r):**
Defect. The shadow of the future disappears, eliminating incentives for reciprocal restraint. Any cooperation here is exploitable and yields no future benefit.

**Rounds 2 through r-1 (Middle Rounds):**
Apply the adaptive rule above. Track both:
- Global cooperation rate (what fraction of all actions were cooperate)
- Individual defection patterns (who consistently defects despite high group contributions)

## ACCOUNTING FOR EXPLOITATION

If you observe a player who:
- Consistently defected while the group cooperated, receiving benefits
- Has defection_rate > 50% while group cooperation_rate > 50%

**Treat this player as a "defector type"** and adjust your threshold: reduce the minimum cooperation rate required for your cooperation by 5% per defector-type present, to a floor of 25%. This accounts for the fact that some players will free-ride; we don't require perfect cooperation.

## HANDLING VARIANCE IN k AND n

- As k increases, cooperation becomes more individually rational; maintain threshold at (k-1)/k
- As n increases, individual contributions matter less; slightly increase your threshold to (k-1)/k + 1/(2n) to account for dilution effects
- This ensures the strategy remains adaptive across parameter ranges

## COLLECTIVE ALIGNMENT

This strategy is collective because:
1. **It targets group welfare maximization** rather than personal score maximization
2. **It conditions on aggregate history**, not personal gain—you cooperate even when personally costly if others cooperate
3. **It reciprocates collective contributions**, not individual favors
4. **It remains adaptive to defectors** without spiraling into all-defection, preserving opportunities for cooperation with trustworthy players

---

**In summary:** Start cooperatively, maintain cooperation proportional to group cooperation rates, guard against systemic exploitation, and defect only when the collective signal is sufficiently negative or when future play is impossible.
'''

description_COLLECTIVE_2 = '''
# COLLECTIVE STRATEGY FOR PUBLIC GOODS GAME

## CORE PRINCIPLE
Maximize collective welfare by sustaining cooperation through conditional reciprocity, while protecting against exploitation through graduated defection responses.

## DECISION RULE (GENERAL ROUNDS)

**Contribution Decision Based on Recent Cooperation Rate:**

1. Calculate the cooperation rate among all players (including self) over the last W rounds, where W = min(5, current_round - 1)
   - If W = 0 (first round), set cooperation_rate = 1.0 (assume good faith)

2. Conditional Logic:
   - **If cooperation_rate ≥ 0.75:** CONTRIBUTE
     - The group is sustaining cooperation; maintain it
   
   - **If 0.50 ≤ cooperation_rate < 0.75:** CONTRIBUTE
     - Cooperation is slipping but salvageable; signal continued commitment to revive it
   
   - **If cooperation_rate < 0.50:** DEFECT
     - Cooperation has collapsed; defecting minimizes losses and signals that free-riding is unprofitable
   
3. **Self-consistency adjustment:**
   - If you defected in the previous round AND cooperation_rate ≥ 0.60, return to CONTRIBUTE
   - This allows re-entry into cooperation once conditions improve

## EDGE CASES & SPECIAL ROUNDS

**Round 1 (First Round):**
- CONTRIBUTE
- Rationale: Establish a cooperative baseline; without history, good faith is the only signal

**Final 2 Rounds (Last Round and Second-to-Last):**
- Apply the same rule as other rounds, NOT unconditional defection
- Rationale: In a tournament context, end-game defection is observable and damages reputation against future opponents with memory; collective strategy prioritizes long-term credibility over one-round exploitation

**When n is very small (n ≤ 3):**
- Increase the cooperation threshold to 0.80
- Rationale: With few players, each individual's defection has outsized impact; demand higher group-level commitment

**When k is very low (k ≤ 1.5):**
- Lower the "salvage threshold" from 0.50 to 0.40
- Rationale: Contribution value is already weak; maintain cooperation more aggressively to overcome the poor multiplier

## ROBUSTNESS MECHANISMS

**Against Unconditional Defectors:**
- After 2 consecutive rounds of <30% group cooperation, lock into DEFECT mode for 2 rounds, then reassess
- Prevents chasing hopeless cooperation indefinitely

**Against Conditional Cooperators:**
- The 0.75/0.50 thresholds naturally reciprocate their strategy
- Conditional cooperators will see your cooperation and raise theirs; you'll detect this via cooperation_rate and respond

**Against Mixed Strategies:**
- The windowed cooperation rate (W = 5) smooths out noise; temporary defections don't trigger permanent retaliation
- Self-consistency rule allows graceful re-entry

## COLLECTIVE ALIGNMENT

This strategy prioritizes:
1. **Collective surplus** – Cooperation is maintained as long as viable (≥50% threshold)
2. **Stable equilibrium** – By rewarding group cooperation and punishing collapse, it incentivizes all players toward mutual contribution
3. **No exploitation** – Defection mode activates when free-riding dominates, protecting contributors
4. **Transparency** – All decisions depend only on observable history, making the strategy predictable and learnable to other players

The strategy communicates through action: *"I will cooperate if the group cooperates, and I will defend by defecting only when cooperation has already failed."*
'''

description_COLLECTIVE_3 = '''
# COLLECTIVE STRATEGY FOR PUBLIC GOODS GAME

## CORE PRINCIPLE
Maximize collective welfare by sustaining cooperation, while remaining robust to exploitation. This strategy treats the group's cumulative payoff as the primary objective, not individual advantage.

---

## DECISION RULE: CONDITIONAL COOPERATION WITH ADAPTIVE THRESHOLDS

**For each round t (except the last):**

1. **Calculate the cooperation rate** in the previous round: `coop_rate = (sum of contributions in round t-1) / n`

2. **Contribute if and only if:**
   - Round 1: **CONTRIBUTE** (assume good faith; establish baseline for reciprocity)
   - Round t > 1: CONTRIBUTE if `coop_rate >= threshold(t)`
   - Where `threshold(t) = max(0.5, 1 - t/(2*r))` — the threshold decays over time, becoming more forgiving in later rounds

3. **Special case — final round:** 
   - If `coop_rate_previous >= 0.4`, CONTRIBUTE (maintain collective momentum to the end)
   - Otherwise, DEFECT (no future rounds to penalize defection)

---

## RATIONALE FOR EACH COMPONENT

**Round 1 contribution:** Bootstraps cooperation. Opening with defection guarantees mutual defection; opening with contribution signals willingness and allows others to reciprocate.

**Conditional cooperation rule:** Mirrors observed behavior back to the group. If >50% cooperate, we cooperate (sustaining the commons). If cooperation falls below 50%, we switch to defect to avoid being exploited, but with increasing tolerance over time to account for random noise or learning lag.

**Decay threshold:** As the game approaches its end, we relax punishment. Groups with 30-40% cooperation in late rounds may still achieve better collective outcomes than total breakdown. This prevents a death spiral triggered by early defectors.

**Final round exception:** A critical moment. If the group has maintained reasonable cooperation (40%+), defecting now undermines all prior trust-building and reduces collective payoff. We stay committed. If cooperation has already collapsed, individual defection has negligible impact on the group and maximizes personal payoff.

---

## ROBUSTNESS PROPERTIES

- **Against unconditional cooperators:** Sustains cooperation; achieves high collective payoff.
- **Against unconditional defectors:** Quickly switches to defection; minimizes losses by not subsidizing free-riders.
- **Against tit-for-tat:** Compatible; mutual cooperation emerges and persists.
- **Against randomness:** The 50% threshold filters noise; small fluctuations don't destabilize cooperation.
- **Against mixed populations:** Adaptive thresholds allow graceful degradation—cooperation remains at lower levels if the group is heterogeneous.

---

## SUMMARY

**Cooperate early and often, but penalize defection promptly. Forgive at the margin as time runs out. Always ask: "What choice maximizes our sum, not mine?"**
'''

description_COLLECTIVE_4 = '''
# COLLECTIVE STRATEGY FOR PUBLIC GOODS GAME

## CORE PRINCIPLE
Maximize collective welfare through adaptive reciprocity that punishes free-riding while rewarding cooperation, calibrated to game parameters and remaining rounds.

## DECISION RULES

### Primary Strategy: Conditional Contribution with Decay
1. **Calculate the cooperation threshold** based on game parameters:
   - Defection payoff (keep 1 token): 1
   - Cooperation payoff if all cooperate: k/n
   - Cooperation is individually rational only if k/n > 1, so k > n (impossible by definition)
   - Therefore, we use **reciprocal contribution based on observed cooperation rates**

2. **Contribute if recent cooperation rate exceeds threshold T**:
   - T = (n-1) / (k-1) * (1/n) — the break-even point
   - Simpler: Contribute if at least ceil((n-1)/k) other players contributed last round
   - This ensures you only cooperate when the multiplier effect justifies it collectively

3. **Track cooperation by player**:
   - Maintain individual cooperation rates for each opponent
   - Weight recent rounds more heavily (last 5 rounds: 2x weight; before that: 1x weight)
   - Players with 100% recent cooperation deserve reciprocal contribution

4. **Apply time-dependent adjustment**:
   - **Early rounds (1 to r/3)**: Slightly optimistic — contribute if T-10% threshold met
   - **Middle rounds (r/3 to 2r/3)**: Strict reciprocity — exactly at T threshold
   - **Late rounds (final r/3)**: Exploit strategically — only contribute if >80% of others do, OR if defecting would reduce final round collective total below continuation value

### Round 1 Special Case
- **Contribute in Round 1** (cooperation signal)
- This is a costless signal that tests whether others are conditionally cooperative vs pure defectors

### Final Round (Last Round)
- Apply strict payoff maximization: **Defect** unless you predict >90% of others will cooperate
- Many players will defect in final round; only trust demonstrable patterns

## HANDLING EDGE CASES

**Unanimous Defection Detected**
- If all opponents defect by round 3, switch to pure defection for remaining rounds
- No point sustaining losses against unconditional defectors

**Oscillating Opponents**
- Players alternating C/D: Use 50% cooperation threshold
- Treat them as moderate cooperators, not pure defectors

**Late-Game Defection Shift**
- If cooperation rate drops >20% between early and late game rounds, immediately defect
- This prevents exploitation by late-switchers

**Two-Player Games (n=2)**
- Cooperation is only individually optimal if k ≥ 2
- If k=1.5, use tit-for-tat instead: contribute only if opponent contributed last round

## COLLECTIVE ALIGNMENT

This strategy prioritizes **collective value creation** through:
- **Round 1 cooperation** signals genuine reciprocal commitment (not pure selfishness)
- **Threshold-based reciprocity** maximizes total welfare by sustaining cooperation when multiplier effects are strong
- **Defection only when it's systemic** — you don't withdraw until clear that cooperation is futile
- **Punishment of free-riders** — by defecting when others defect, you enforce a norm that only punishes genuine defection

## SUMMARY DECISION TREE
```
IF round == 1: CONTRIBUTE
ELSE IF (opponent cooperation rate adjusted for recency) > T: CONTRIBUTE
ELSE IF final round AND can verify >90% others contributing: CONTRIBUTE
ELSE IF all opponents defecting: DEFECT
ELSE IF time_remaining_ratio < 0.2 AND opponent_cooperation_rate < 0.6: DEFECT
ELSE: DEFECT (cautious default)
```

This balances **exploitation avoidance** with **cooperation sustainability**, adaptive to both parameters and opponent behavior.
'''

description_COLLECTIVE_5 = '''
# ADAPTIVE COLLECTIVE STRATEGY FOR PUBLIC GOODS GAME

## CORE PRINCIPLE
Maximize collective welfare through conditional cooperation that responds to demonstrated trustworthiness, while maintaining robustness against defection and free-riding.

## DECISION RULE (GENERAL ROUNDS)

**1. Calculate Group Health Metric**
- Track the average contribution rate across all players over the last w rounds (window = min(5, current_round))
- Define "healthy cooperation" as: average_contribution_rate ≥ threshold
- Set threshold dynamically: 0.5 + (0.3 * k/n), reflecting the multiplier efficiency

**2. Classify Each Opponent**
For each other player j, compute their historical defection rate over the last w rounds:
- **Reliable cooperators**: defection_rate ≤ 0.2
- **Conditional cooperators**: 0.2 < defection_rate ≤ 0.6
- **Systematic defectors**: defection_rate > 0.6

**3. Contribution Decision**
- **If group is healthy** (avg contribution ≥ threshold):
  - Contribute (C) if you are a reliable cooperator
  - Contribute (C) if ≥50% of others are reliable or conditional cooperators
  - Otherwise, Defect (D)

- **If group is unhealthy** (avg contribution < threshold):
  - Defect (D) with probability proportional to defector density
  - BUT: If ≥40% are reliable cooperators, contribute (C) anyway—assume you can help restore health
  - This prevents cascading defection while rewarding genuine cooperators

**4. Reciprocity Boost (Optional Rule)**
- If a previously defecting player switches to contributing, treat them as conditional cooperator immediately
- Grant one round of goodwill cooperation to signal receptiveness to reformation

---

## EDGE CASES

**Round 1 (First Round)**
- Contribute (C)
- Rationale: Establish baseline cooperation; defecting immediately signals bad intent and poisons the pool

**Last Round (Round r)**
- Apply the standard decision rule using history
- Do NOT collapse into pure defection just because it's the final round
- Rationale: This is a tournament; other strategies may punish last-round defection harshly, and collective welfare includes reputation effects

**Rounds 2–3 (Early Information Gathering)**
- Contribute (C) unless observing >70% defection already
- Rationale: Gather reliable data before making harsh judgments; early variance is noise, not intent

**Rounds where you're the only contributor**
- Defect (D) in the next round if this pattern persists (2+ consecutive solo contributions)
- Rationale: Avoid being exploited as a "sucker"; signal that free-riding has costs

**Rounds where everyone contributes**
- Continue contributing (C)
- Rationale: Maintain the cooperative equilibrium

---

## ROBUSTNESS FEATURES

**Against Defectors**: The strategy avoids mutual defection spirals by maintaining some cooperation when others show any reliability, preventing lock-in to all-defect outcomes.

**Against Free-Riders**: By tracking individuals and reducing cooperation probability when defection is concentrated, the strategy punishes systematic exploiters without harming conditional cooperators.

**Against Noise**: The rolling window approach averages out random variation; thresholds are soft, not brittle.

**Against Sophisticated Manipulation**: The strategy doesn't reward "apparent" cooperation that vanishes near the end; reciprocity is genuine and tested, not gullible.

---

## COLLECTIVE ALIGNMENT

This strategy prioritizes total group payoff over individual payoff. It:
- Starts with cooperation to enable collective gains
- Tolerates free-riders when they're outnumbered by cooperators (collective surplus > individual loss)
- Withdraws support only when defection becomes systematic
- Rebuilds trust when defectors show signs of reform

The strategy treats other players' actions as information about their type, not as personal slights. It is forgiving but not naive—it sustains cooperation where it can be productive.
'''

description_COLLECTIVE_6 = '''
# ADAPTIVE RECIPROCAL CONTRIBUTION STRATEGY

## CORE PHILOSOPHY
Maximize collective welfare by establishing a self-sustaining equilibrium of mutual contribution, while gracefully degrading when opponents defect. The strategy treats the game as a trust-building exercise where consistent reciprocation signals stability.

## PRIMARY DECISION RULE: CONDITIONAL COOPERATION WITH MEMORY

**Default Action:** CONTRIBUTE (C)

**Deviation Trigger:** Defect (D) if and only if the aggregate contribution rate in the previous round falls below a dynamically adjusted threshold.

### Threshold Calculation
- **Rounds 1-3:** Threshold = 100% (require universal cooperation)
- **Rounds 4 onwards:** Threshold = (average contribution rate across all previous rounds) - 5 percentage points

This creates adaptive expectations: if most players have been contributing at 70%, tolerate 65% cooperation before punishing.

## ROUND-SPECIFIC ADJUSTMENTS

**Round 1:** Always CONTRIBUTE
- Signal good faith and test whether others reciprocate
- Establish baseline for measuring group cooperation

**Final Round (Round r):** CONTRIBUTE if and only if the contribution rate in round (r-1) exceeded your adjusted threshold
- Avoid last-round free-riding despite absence of future consequences
- Maintain integrity of signaling mechanism

**Early Rounds (2-3):** CONTRIBUTE unless *all other players* defected collectively in the previous round
- Give opponents grace period to establish cooperation
- Require near-universal defection to trigger punishment (not just one defector)

**Middle & Late Rounds (4 onwards):** Apply the threshold rule strictly
- Recalibrate expectations based on empirical group behavior
- Punish systematic free-riding proportionally to its prevalence

## HANDLING EDGE CASES

**Universal Defection Detected:** If contribution rate drops to 0% in any round, switch to permanent defection for remaining rounds
- Rational exit from a failed cooperation game
- Prevents exploitation by coordinated free-riders

**Oscillating Groups:** If contribution rates swing wildly (e.g., 100% → 20% → 90%), use a 2-round moving average for threshold calculation rather than immediate reactions
- Dampens overreaction to noise
- Allows groups to recover from temporary shocks

**Majority vs. Minority Defectors:** If >50% of opponents contribute, apply C regardless of threshold
- Majority cooperation indicates viable collective equilibrium
- Minority defectors benefit from your contribution without sabotaging the group

## COLLECTIVE ALIGNMENT

This strategy treats every other player's contribution as a signal about group health rather than a personal slight. It prioritizes:
1. **Achieving high aggregate welfare** by maintaining high group contribution rates
2. **Fairness** by matching group effort levels (not reward-maximization)
3. **Robustness** by gracefully degrading rather than escalating punishment
4. **Incentive compatibility** by ensuring your cooperation is worthwhile only when others reciprocate

The 5-percentage-point tolerance band prevents hair-trigger mutual defection while still punishing drift toward free-riding.
'''

description_COLLECTIVE_7 = '''
# ADAPTIVE RECIPROCAL CONTRIBUTION STRATEGY FOR PGG

## CORE PRINCIPLE
Maximize collective welfare by maintaining high contribution rates while protecting against systematic defection through conditional cooperation and strategic defection thresholds.

## DECISION RULES

### ROUND 1 (First Round)
**Action: CONTRIBUTE**

Rationale: Cooperate unconditionally to signal willingness to support the public good and establish baseline reciprocity. This is a costless signal since we have no history to reference.

### ROUNDS 2 to r-1 (Middle Rounds)
**Action: Conditional Contribution based on Recent Cooperation Rate**

Calculate the cooperation rate over the last w rounds (window size = max(3, r/4)):
- cooperation_rate = (total contributions in window) / (n × w)

**Decision Logic:**
- IF cooperation_rate ≥ 0.65: **CONTRIBUTE**
  - Sustain cooperation when collective participation is sufficient
  
- IF 0.40 ≤ cooperation_rate < 0.65: **CONTRIBUTE with probability p = cooperation_rate**
  - Gracefully decline as cooperation erodes
  - This creates a gradual transition rather than a cliff
  
- IF cooperation_rate < 0.40: **DEFECT**
  - Protect individual payoff when group has collapsed into defection
  - This threshold acknowledges that high defection makes contribution economically irrational

**Per-Player History Consideration:**
- Identify chronic defectors (players who defect >70% of the time in the window)
- Do NOT adjust your decision based on individual defections alone
- Base decisions on aggregate group behavior to avoid cascading punishment

### ROUND r (Final Round)
**Action: CONTRIBUTE**

Rationale: 
- Defecting in the final round yields only a marginal individual benefit (1 token)
- Contributing signals that your strategy is based on genuine reciprocal logic, not exploitation
- In a tournament setting against other AI systems, demonstrating consistency matters for repeated matchups and reputation
- This prevents the "shadow of the end" from creating a defection cascade

## EDGE CASE HANDLING

**Unanimous Defection (cooperation_rate = 0):**
- Defect to preserve resources
- Revert to CONTRIBUTE in subsequent rounds if any cooperation resumes
- This prevents being permanently locked into a losing state

**Unanimous Cooperation (cooperation_rate = 1):**
- Continue contributing
- Monitor for defection spikes; if cooperation suddenly drops, apply conditional logic in the next round

**High Variance (Some rounds 100%, others 0%):**
- Use the moving window to smooth volatility
- Weight recent rounds slightly more heavily (arithmetic mean of window is sufficient; no need for exponential weighting)

**Small Groups (n ≤ 3):**
- Lower cooperation threshold to 0.50 (since one defector has outsized impact)
- Increase window size to r/3 to reduce noise from individual decisions

## COLLECTIVE ALIGNMENT

This strategy prioritizes:

1. **Shared Prosperity**: High cooperation thresholds (65%) ensure we only defect when group welfare is genuinely compromised

2. **Reciprocity**: Contributions are conditional on observed group behavior, not on exploiting free-riders

3. **Stability**: The probability-based transition (40-65% band) prevents sudden defection cascades that destroy value

4. **Robustness**: We defect only when self-interested, not to punish individuals, making us resilient to mixed-strategy opponents

5. **Tournament Success**: Final-round cooperation and initial cooperation signal that we are a valuable partner, not a pure defector waiting to exploit

## SUMMARY TABLE

| Context | Action | Rationale |
|---------|--------|-----------|
| Round 1 | Contribute | Establish reciprocity |
| Coop rate ≥ 65% | Contribute | Sustain collective momentum |
| 40% ≤ Coop rate < 65% | Mixed (probabilistic) | Graceful degradation |
| Coop rate < 40% | Defect | Protect against collapsed groups |
| Final round | Contribute | Signal consistency and partnership value |
'''

description_COLLECTIVE_8 = '''
# COLLECTIVE STRATEGY FOR PUBLIC GOODS GAME

## CORE PRINCIPLE
Maximize collective welfare through conditional cooperation that escalates pressure on defectors while remaining resilient to exploitation.

## DECISION RULES

### BASELINE RULE: Conditional Contribution Based on Recent Cooperation Rate
1. Calculate the **cooperation rate** from the previous round: (total contributors) / n
2. **If cooperation rate ≥ threshold T**: Contribute (C)
3. **If cooperation rate < threshold T**: Defect (D)
4. **Threshold T = (k - 1) / k** (the break-even point where contribution creates positive expected value)

**Rationale**: This threshold ensures you only contribute when the collective is likely generating positive surplus. At this threshold, your contribution yields exactly fair return; above it yields gains; below it means others are free-riding.

### ESCALATION RULE: Punish Persistent Defection
- Track the **defection pattern** of each opponent (rounds where they played D)
- If any single player defected in >50% of all prior rounds: treat them as a "defector type"
- When facing a defector type, **always defect** regardless of cooperation rate
- This prevents systematic exploitation by free-riders

### RECOVERY RULE: Forgive and Re-Cooperate
- After 3 consecutive rounds where the group cooperation rate ≥ T again: reset defector classifications
- This allows reformed players to rejoin the cooperative coalition
- Balances punishment with opportunity for collective recovery

---

## EDGE CASES

### ROUND 1 (Initial Action)
**Contribute (C)**.
- Assume good faith to establish cooperative signal
- First-mover contribution is valuable information
- Establishes baseline for reciprocity

### FINAL ROUND (Round r)
**Apply the same conditional rule as all other rounds**.
- Do NOT defect at the end just because there's no future
- This would be individually rational but collectively destructive
- Signals commitment to cooperation as a principle, not just repeated-game tit-for-tat

### MIXED GROUPS (Some Defectors, Some Cooperators)
- **Cooperate** if cooperation rate ≥ T (the threshold insulates you from minority defectors)
- Example with n=5, k=2: threshold T = 0.5. If 3+ others contribute, you earn positive returns even if 2 defect

### ALL PLAYERS DEFECTING (c_total = 0)
- **Defect** (cooperation rate = 0 < T)
- You earn 0 from public good but keep your token
- This minimizes losses

### CASCADING DEFECTION
- If cooperation rate drops below T and stays there for 2+ rounds, most players will continue defecting
- **Stick with the rule anyway** — don't panic-deviate
- This preserves predictability; if others also use robust rules, cooperation can re-emerge once conditions improve

---

## COLLECTIVE ALIGNMENT

This strategy embodies three collective principles:

1. **Mutual Benefit Orientation**: You cooperate only when the multiplier effect creates genuine shared surplus (k/n > 1), never demanding others subsidize your participation.

2. **Fairness Through Symmetry**: The threshold is identical for all; no special pleading. Everyone receives the same treatment under the same conditions.

3. **Resilience Over Naïveté**: By escalating against habitual defectors, the strategy prevents the "tragedy" outcome where systematic free-riding collapses cooperation. But by allowing recovery, it remains non-vindictive.

4. **Stability**: The strategy is **robust to unilateral defection** (you defect back), **resistant to noise** (threshold-based, not binary-history-dependent), and **predictable** (opponents can learn and coordinate around it).

---

## SUMMARY
**Contribute if (cooperation rate ≥ break-even threshold AND player is not a habitual defector). Otherwise defect. Allow defectors to rejoin after reform.**
'''

description_COLLECTIVE_9 = '''
# ADAPTIVE COLLECTIVE STRATEGY FOR PUBLIC GOODS GAME

## CORE PRINCIPLE
Maximize collective welfare by contributing when sufficient reciprocation exists, while detecting and punishing free-riders. The strategy balances optimism (encouraging cooperation) with realism (protecting against exploitation).

## DECISION RULE (GENERAL ROUNDS)

**Contribute (C) if and only if:**
- The historical contribution rate meets or exceeds a dynamic threshold, OR
- We are in an early phase where establishing cooperation is valuable

**Defect (D) if:**
- The contribution rate has fallen below the threshold AND we have sufficient history
- The expected return from cooperation is demonstrably negative

### THRESHOLD CALCULATION
Define the contribution rate as: (total contributions across all players and all past rounds) / (maximum possible contributions)

- **Rounds 1-3 (Exploration Phase):** Contribute unconditionally. Establish signal of cooperative intent.
- **Rounds 4 onward (Adaptive Phase):** 
  - If contribution_rate ≥ (k/n) × 0.6, contribute
  - If contribution_rate < (k/n) × 0.6, defect
  
This threshold exploits the core incentive: cooperation is individually rational only if others contribute enough to justify the opportunity cost.

## EDGE CASES & ADJUSTMENTS

**Last Round (Final Clarity):**
- If contribution_rate ≥ (k/n) × 0.6 and we have cooperated recently, contribute one final time (signal reliable partner)
- If contribution_rate is low, defect (no future reputation consequences)

**Sudden Drops:**
- If contribution rate drops >20% in a single round, immediately shift to defection
- Require two consecutive rounds of recovery before re-engaging with cooperation

**Extreme Scenarios:**
- If only 1-2 players ever contribute while others consistently defect, defect (free-rider environment detected)
- If everyone contributes in rounds 1-3, maintain contribution indefinitely (true cooperation achieved)

## COLLECTIVE ALIGNMENT

This strategy is **collectively optimal** because:

1. **Mutual Benefit Focus:** Only demands reciprocation proportional to the multiplier—not exploitative
2. **Transparency:** All decisions follow observable history, enabling other cooperators to identify and match this strategy
3. **Punishment of Defection:** Withdraws cooperation when the collective return becomes negative, discouraging exploitation
4. **Reward of Cooperation:** Eagerly re-engages when others reciprocate, encouraging upward spirals
5. **Resilience:** Does not require coordination; works against mixed populations by filtering toward cooperative subgroups

## SUMMARY
- **Rounds 1-3:** Always cooperate (build trust)
- **Rounds 4+:** Cooperate if historical rate ≥ (k/n) × 0.6; otherwise defect
- **Last round:** Cooperate if trend is positive; defect if trend is negative
- **Shock response:** React sharply to sudden defection spikes
'''

description_COLLECTIVE_10 = '''
# ADAPTIVE RECIPROCAL CONTRIBUTION STRATEGY

## CORE DECISION RULE

**Threshold-Based Reciprocal Cooperation:**

Cooperate in round t if and only if the observed cooperation rate in round t-1 meets or exceeds a dynamic threshold that adapts to game parameters and remaining rounds.

### Specific Decision Logic:

1. **First Round (t=1):** COOPERATE
   - Establish a cooperative signal and gather baseline information about opponent behavior
   - Provides mutual benefit if opponents are similarly inclined

2. **Subsequent Rounds (t > 1):** 
   - Calculate the cooperation rate from the previous round: coop_rate = (sum of all contributions in round t-1) / n
   - Set threshold = (k - 1) / (n * 2)
   - IF coop_rate ≥ threshold THEN cooperate
   - ELSE defect

### Rationale for Threshold:
- The threshold (k-1)/(n*2) represents a breakeven point where cooperation yields positive expected returns
- When cooperation exceeds this threshold, contributing generates value for the collective that exceeds the individual opportunity cost
- This threshold is conservative—it triggers cooperation even when not all players cooperate, rewarding growing coalitions

3. **Final Round (t = r):**
   - Apply the same reciprocal rule as other rounds
   - Do NOT defect automatically in the last round
   - Reasoning: Reputation concerns persist even in final interactions within a tournament; more importantly, the rule remains collectively rational

## ADAPTATION TO GAME PARAMETERS

- **Small multiplier k (close to 1):** Threshold remains low; cooperation is rarer and only sustainable with high observed cooperation
- **Large group n:** Threshold increases, making unilateral cooperation less attractive; requires broader participation to justify
- **Many rounds r:** Sustains longer-term reciprocal relationships; defection in early rounds triggers prolonged punishment
- **Few rounds r:** Strategy remains flexible; threshold-based approach avoids getting locked into cycles

## ROBUSTNESS PROPERTIES

**Against pure defectors:** Strategy defects after observing universal defection (coop_rate = 0 < threshold), minimizing losses

**Against pure cooperators:** Strategy cooperates throughout, achieving mutual benefit

**Against mixed strategies:** Strategy tracks actual behavior and aligns contributions with observed collective behavior, creating pressure toward cooperation without naive self-sacrifice

**Against exploiters:** Strategy maintains flexibility to punish by switching to defection when cooperation rates drop below threshold, then re-engages if collective behavior improves

## COLLECTIVE ALIGNMENT

This strategy prioritizes the collective interest while protecting against exploitation:
- It initiates cooperation and rewards participation
- It scales contributions to match observed willingness to cooperate
- It avoids both naive exploitation and mutual destruction
- It maintains conditional engagement: collective welfare improves when others reciprocate, but individual losses are minimized when others defect
'''

description_COLLECTIVE_11 = '''
# ADAPTIVE CONTRIBUTION STRATEGY FOR PUBLIC GOODS GAMES

## CORE STRATEGY: CONDITIONAL RECIPROCITY WITH DECAY

### PRIMARY DECISION RULE

**Contribute (C) if and only if:**
- The observed average contribution rate in the previous round exceeds a dynamic threshold, OR
- We are in round 1 (initialize cooperation), OR
- The remaining rounds are few enough that long-term defection patterns haven't solidified

**Defect (D) otherwise** to preserve the token and exploit free-riding when contribution rates fall below threshold.

---

## DETAILED RULES

### Round 1
- **Cooperate (C)** unconditionally
- Rationale: Establish baseline cooperation and signal willingness to participate; gather information on opponent types

### Rounds 2 through (r-1)

**Calculate observed cooperation rate from previous round:**
- cooperation_rate = (number of players who contributed) / n

**Set dynamic threshold:**
- threshold = k / n (the point where contributing yields zero marginal benefit vs. defecting)
- adjusted_threshold = (k / n) * 0.85 (slight penalty to account for uncertainty and free-rider incentives)

**Decision rule:**
- If cooperation_rate ≥ adjusted_threshold: **Contribute (C)**
- If cooperation_rate < adjusted_threshold: **Defect (D)**

**Rationale:** 
- When others contribute above the break-even point, your contribution adds positive expected value to the pool
- When cooperation drops below this threshold, contributing becomes individually irrational and rewards defectors
- The 0.85 discount factor acknowledges that even at k/n cooperation, some defectors gain more than cooperators

### Last Round (Round r)

- **Always Defect (D)**
- Rationale: No future rounds remain, so reciprocity incentives vanish; the game ends after payoff, eliminating reputation effects
- Exception: If this is round 1 AND r=1 (single round), cooperate by default rule

---

## HANDLING EDGE CASES

**Complete defection by all others (cooperation_rate = 0):**
- Defect immediately and maintain defection
- Rationale: Cannot recover positive payoff through contribution when no one participates

**Complete cooperation by all others (cooperation_rate = 1.0):**
- Cooperate to maintain the equilibrium and maximize collective gain
- Rationale: Your contribution is essential to the pool; defecting drops the multiplier effect for everyone

**Highly volatile opponents (oscillating cooperation):**
- Use a 2-round moving average of cooperation rates instead of single previous round
- This smooths noise and prevents overreaction to one-round anomalies
- Rationale: Distinguish between strategic adjustments and random variation

**Small n (n = 2 or 3):**
- Lower the adjusted_threshold to (k / n) * 0.90
- Rationale: With fewer players, your individual contribution has larger impact; free-riding is more costly to the group

---

## COLLECTIVE ALIGNMENT

This strategy embodies **collective rationality** while remaining **robust to exploitation**:

1. **Reciprocal cooperation:** Rewards groups that cooperate above the efficiency threshold, amplifying mutual gain
2. **Defection protection:** Immediately withdraws cooperation when the group falls below sustainable contribution, protecting against one-sided exploitation
3. **Last-round honesty:** Does not pretend future rounds exist; avoids false cooperation signals when incentives disappear
4. **Adaptive thresholds:** Responds to actual group behavior rather than fixed assumptions
5. **Tournament-viable:** Does not depend on coordination; works as individual strategy while benefiting collectives that adopt similar logic

The strategy implicitly encourages others toward the same threshold-based behavior: groups where many players use this rule converge toward cooperation_rate ≥ (k/n), creating stable, high-payoff equilibria.
'''

description_COLLECTIVE_12 = '''
# Adaptive Collective Strategy for Repeated Public Goods Game

## CORE STRATEGIC APPROACH

This strategy balances three objectives: (1) detecting and exploiting defectors, (2) rewarding cooperators to sustain contributions, and (3) maximizing collective welfare when conditions permit.

## DECISION RULES

**Round 1 (Initialization):**
- COOPERATE
- Rationale: Start with reciprocal intent to learn opponent types and establish baseline trustworthiness signals

**Rounds 2 through (r-1) (Adaptive Phase):**

For each opponent group i, calculate their cooperation rate: coop_rate_i = (contributions by i in prior rounds) / (rounds played so far)

1. **If coop_rate_i ≥ 0.75 (reliable cooperators):**
   - COOPERATE
   - These players are sustaining the collective good; continued cooperation attracts further contribution

2. **If coop_rate_i ∈ [0.25, 0.75) (inconsistent players):**
   - COOPERATE if (k/n) * expected_total_contributions ≥ 0.5
   - Otherwise DEFECT
   - Rationale: Only cooperate when the multiplier effect still justifies collective contribution; otherwise preserve endowment

3. **If coop_rate_i < 0.25 (chronic defectors):**
   - DEFECT
   - Rationale: Serial defectors exploit cooperators; cutting off their beneficiary access discourages free-riding

**Round r (Final Round - Endgame):**
- DEFECT
- Rationale: No future reciprocity is possible; the multiplier mechanism cannot be leveraged for reputation building. Defection maximizes individual payoff in the absence of reputational consequences.

## EDGE CASE HANDLING

**All players defecting across all rounds:**
- Continue defecting (dominates contributing to zero pool)

**Mixed environment (some cooperators, some defectors):**
- Cooperate with cooperators; defect against defectors
- This generates a signal: cooperators are rewarded; defectors are isolated
- Over rounds, this creates pressure on inconsistent players to either commit to cooperation or accept isolation

**Late-game convergence (most players converging to C or D):**
- Align with majority behavior if majority cooperation rate ≥ 0.6
- Otherwise defect
- Rationale: Follow strong collective signals when they emerge, but don't commit to losing patterns

## COLLECTIVE ALIGNMENT

This strategy prioritizes **collective welfare in the aggregate** while remaining robust to defection:

- It rewards and sustains genuine contributors (those who cooperate ≥75% of the time)
- It withdraws support from exploiters, creating negative incentives for serial defection
- It maintains flexibility to pivot based on observed group composition
- It does not require pre-agreed norms or external coordination—it infers group structure from actions alone

The endgame defection is honest: it acknowledges that in a finitely repeated game with no institutional enforcement, the last round has no reputational value, so defection is rational at that boundary.
'''

description_COLLECTIVE_13 = '''
# COLLECTIVE STRATEGY FOR PUBLIC GOODS GAME

## CORE PHILOSOPHY
This strategy treats the PGG as a problem of mutual benefit discovery rather than pure competition. It aims to identify cooperative subgroups while remaining robust to exploitation.

## DECISION RULES

### ROUND 1 (Initial Probe)
**Contribute (C)**
- Rationale: Cooperation is a costly signal of good intent. Starting with C provides crucial information about the player pool and establishes a cooperative baseline.

### ROUNDS 2 through (r-1) (Main Phase)

**Calculate the "Cooperation Index":**
- For each opponent j, track their contribution ratio: c_j = (total contributions by j so far) / (rounds played)
- Compute average cooperation ratio across all opponents: avg_coop = (sum of all c_j) / (n-1)

**Decision Logic:**
1. **If avg_coop ≥ 0.6**: Contribute (C)
   - The group is sufficiently cooperative. Defecting risks collective welfare.
   - Threshold of 0.6 is high enough to filter noise but low enough to sustain reciprocal cooperation.

2. **If 0.3 ≤ avg_coop < 0.6**: Defect (D)
   - The group shows mixed signals. Contributing yields low expected returns from the pool.
   - Defecting protects your endowment while observing whether others adjust behavior.

3. **If avg_coop < 0.3**: Defect (D)
   - The group is largely non-cooperative. Further contributions are economically irrational.
   - Exception: If you are the only defector (your own c_i ≥ 0.6 while others defect), contribute once more to test for reactive cooperation.

### ROUND r (Final Round)

**Defect (D)**
- Rationale: In the last round, there is no future to influence. The multiplier benefit cannot be recovered. Defecting maximizes immediate payoff.
- **Exception**: If avg_coop has been ≥ 0.8 across all previous rounds, contribute. This rewards exceptionally strong cooperation and may influence the tournament's aggregate scoring.

## HANDLING EDGE CASES

**Single-round games (r=1):**
- Defect immediately. No history to build on; no future to influence.

**Two-round games (r=2):**
- Round 1: Contribute. Round 2: Defect (final round rule).

**Volatile opponents:**
- If an individual opponent alternates wildly between C and D, treat them as avg_coop ≈ 0.5 in calculations. Do not overweight recent actions.

**All opponents defect initially:**
- If round 2 finds avg_coop ≈ 0, you defect, but continue monitoring. If any opponent contributes in round 3+, gradually shift back toward contribution (treat their signal seriously).

**You are the sole contributor:**
- If your c_i = 1 but avg_coop of others ≈ 0, defect for 2 rounds. Then test once more (contribute) if the pool has not shifted. Do not become trapped in unilateral giving.

## COLLECTIVE ALIGNMENT

This strategy is collectively minded because:
1. **It starts cooperatively**, signaling willingness to help the group.
2. **It conditions on observed group health**, not individual defection. If the group can sustain cooperation, you protect it.
3. **It penalizes exploitation** by withdrawing when average cooperation is low, creating pressure for norm formation.
4. **It adapts to mixed groups**, distinguishing between salvageable cooperators and committed free-riders.
5. **It respects finality**, acknowledging that the last round breaks reciprocal logic.

The threshold of 0.6 is a "cooperation point"—above it, the collective benefit justifies contribution; below it, the collective is too fractured to sustain mutual gain.
'''

description_COLLECTIVE_14 = '''
# ADAPTIVE CONDITIONAL COOPERATION STRATEGY FOR PUBLIC GOODS GAMES

## CORE PRINCIPLE
Cooperate conditionally based on recent group performance and reciprocal contribution rates, with strategic defection only when collective welfare is demonstrably worse than individual gain.

## DECISION RULE (GENERAL)

**For any round t (except as modified below):**

1. **Calculate the Group Cooperation Rate (GCR)** from the previous round:
   - GCR = (total contributions in round t-1) / n
   - If round 1, set GCR = 0.5 (assume moderate cooperation)

2. **Calculate Expected Payoff Comparison:**
   - If I contribute: expected payoff ≈ (k/n) × (GCR × n + 1)
   - If I defect: expected payoff ≈ 1 + (k/n) × (GCR × n)
   - The difference is (k/n) - 1. Since k < n, defection always yields slightly higher individual payoff.

3. **Decision Logic:**
   - **CONTRIBUTE** if GCR ≥ (n-k) / (n-1)
     - This threshold represents the tipping point where collective welfare (measured as my total payoff) improves with my contribution
   - **DEFECT** if GCR < (n-k) / (n-1)

4. **Reciprocity Modifier:**
   - If average GCR over last 3 rounds > 0.6: contribute (signal willingness to enable high cooperation equilibria)
   - If average GCR over last 3 rounds < 0.3: defect (free-ride when others are already defecting)

## EDGE CASES

**Round 1 (First Move):**
- CONTRIBUTE
- Rationale: Establish baseline cooperative signal; defecting immediately eliminates possibility of mutual cooperation

**Final Round (Round r):**
- Apply standard decision rule without modification
- Rationale: No "last round defection wave" - future rounds still matter in expectation for reputation effects in tournament context

**Collapse Scenario** (GCR drops to 0 for 2+ consecutive rounds):
- DEFECT until GCR rebounds above 0.4
- Rationale: Avoid wasted contributions in defection spirals; signal willingness to exit unprofitable equilibrium

**Anomaly Detection** (one player consistently defects while others cooperate):
- Continue applying standard threshold rule
- Rationale: Punishing the free-rider through individual defection only spreads defection; maintain cooperation with the cooperative majority

## COLLECTIVE ALIGNMENT

This strategy **maximizes group welfare** by:
- Seeking the cooperative equilibrium where GCR is high
- Conditioning on others' demonstrated reciprocity rather than assuming trust
- Gracefully degrading to mutual defection only when cooperation is mathematically impossible to sustain
- Avoiding blame-driven spirals that destroy all surplus

The strategy is **robust** because:
- It requires no communication or implicit coordination
- It responds to observable history only
- It handles defectors without escalating damage
- It recovers quickly when cooperative opportunities re-emerge

## PSEUDOCODE SUMMARY

```
IF round == 1:
  CONTRIBUTE
ELSE:
  gCR_recent = average(GCR[t-3:t-1])
  gCR_current = sum(contributions[t-1]) / n
  
  IF gCR_recent > 0.6:
    CONTRIBUTE
  ELSE IF gCR_recent < 0.3:
    DEFECT
  ELSE IF gCR_current >= threshold(k,n):
    CONTRIBUTE
  ELSE:
    DEFECT
```
'''

description_COLLECTIVE_15 = '''
# ADAPTIVE CONDITIONAL COOPERATION WITH STRATEGIC DEFECTION

## CORE STRATEGY: THRESHOLD-BASED RECIPROCITY

**Primary Decision Rule:**
- Contribute (C) if the average contribution rate across all players in the previous round exceeded a dynamic threshold
- Defect (D) if the average contribution rate fell at or below that threshold
- Adjust the threshold downward over time to accommodate declining cooperation

**Threshold Calculation:**
- Rounds 1-3: threshold = 0.5 (require >50% of players contributing)
- Rounds 4 onwards: threshold = max(0.25, average_historical_contribution_rate - 0.15)
  - This allows graceful degradation while maintaining some reciprocity signal

## ROUND-SPECIFIC BEHAVIOR

**First Round (round = 1):**
- Cooperate (C)
- Rationale: Establish a cooperative signal and gather information about the opponent pool's baseline cooperation tendency

**Middle Rounds (2 ≤ round < r - 2):**
- Apply the threshold-based rule above
- If contribution rate is exactly at threshold, defect (break ties conservatively)
- Re-evaluate the threshold each round based on cumulative history

**Penultimate Round (round = r - 1):**
- Maintain threshold-based rule without modification
- This is critical: do NOT shift to unconditional defection yet, as it signals untrustworthiness

**Final Round (round = r):**
- If average contribution in round r-1 was ≥ 0.4: Cooperate
- Otherwise: Defect
- Rationale: Make a final attempt to salvage collective welfare if there's any signal of cooperation, but exit defection if the pool has abandoned cooperation

## EDGE CASES & ROBUSTNESS

**When All Players Defect:**
- Defect immediately and continue defecting (no recovery attempted after round 5)
- Preserve tokens rather than subsidize free-riders

**When >75% Cooperate:**
- Maintain cooperation even if threshold suggests otherwise
- Boost threshold upward: temporary_threshold = min(0.9, previous_threshold + 0.1)
- This rewards high-cooperation equilibria

**Volatile Environments (high fluctuation in contribution rates):**
- Use a 2-round moving average instead of immediate history
- Prevents over-reactive oscillation

**Against Dominantly Defecting Opponents:**
- After 3 consecutive rounds of <25% cooperation, shift to unconditional defection
- This prevents exploitation and conserves payoff against non-reciprocal players

## COLLECTIVE ALIGNMENT

This strategy:
1. **Prioritizes collective welfare early** by cooperating first and rewarding cooperative partners
2. **Protects against exploitation** by withdrawing cooperation only after observing defection
3. **Seeks sustainable equilibria** rather than maximum individual gain in the final round
4. **Communicates reciprocal intent** through consistent response to observed behavior
5. **Gracefully degrades** rather than cliff-dropping to mutual defection

The threshold design ensures that cooperation persists at moderate levels even when universal cooperation fails—capturing partial public goods benefits while limiting losses to free-riders.
'''

description_COLLECTIVE_16 = '''
# ADAPTIVE CONDITIONAL COOPERATION WITH DECAY

## Core Strategy Philosophy
Maximize collective welfare by cooperating conditionally based on demonstrated reciprocity, while protecting against exploitation through gradual defection in end-game phases. This balances optimism about mutual cooperation with realism about free-riding.

---

## PRIMARY DECISION RULE: Conditional Contribution

**Contribute (C) if and only if:**
- Round 1: Always contribute (establish cooperative baseline)
- Round 2 to (r-3): Contribute if the historical cooperation rate ≥ threshold
  - Threshold = 60% of all players' contributions across all past rounds
  - Exception: If you're the only contributor, defect immediately (prevent isolation)
- Round (r-2) to r: Enter decay phase (see below)

**Rationale:** Cooperation becomes attractive when enough others cooperate (since k > 1 ensures the multiplier effect outweighs the cost of contributing). The 60% threshold is permissive enough to sustain cooperation while protecting against persistent defectors.

---

## DECAY PHASE (Final 3 Rounds)

In the last three rounds, apply this diminishing commitment:
- Round (r-2): Contribute only if historical cooperation rate ≥ 70%
- Round (r-1): Contribute only if historical cooperation rate ≥ 80%
- Round r (final): Always defect

**Rationale:** As the game ends, the benefit of future cooperation disappears, so cooperation must be justified by past performance. The escalating threshold weeds out games with poor reciprocity. Defecting in the final round captures any remaining pool and is standard in repeated games with known endpoints.

---

## EDGE CASES & SPECIAL HANDLING

**Isolation Detection:** If you're the only contributor in any round, immediately switch to defection for subsequent rounds until cooperation recovers. Contributing alone yields (k/n) < 1, guaranteeing loss.

**Early Collapse:** If cooperation rate falls below 30% by round 3, defect for all remaining rounds. The game is not sustaining mutual benefit.

**Unanimous Cooperation:** If all players (including you) cooperate for 3 consecutive rounds, lower the threshold to 50% to reward and reinforce the cooperative equilibrium.

---

## COLLECTIVE ALIGNMENT

This strategy is collectively optimal because:
1. **Maximizes group welfare** by maintaining cooperation when reciprocal
2. **Penalizes free-riding** through defection when cooperation fails
3. **Avoids trap scenarios** (like being the sole cooperator indefinitely)
4. **Transparent in logic** — other rational players can predict and match this behavior
5. **Does not require coordination** — only reactive observation of actions and payoffs

---

## ROBUSTNESS

- **Against pure defectors:** Detects non-cooperation immediately, switches to defection
- **Against conditional cooperators:** Reciprocates their cooperation, achieving mutual benefit
- **Against random strategies:** Treats randomness as ~50% cooperation; defects if sustained
- **Against adaptive adversaries:** Gives them one chance (round 1) but punishes exploitation quickly

This strategy seeks cooperative equilibrium but never sacrifices individual payoff for an unreciprocated collective good.
'''

description_COLLECTIVE_17 = '''
# COLLECTIVE STRATEGY: ADAPTIVE CONDITIONAL CONTRIBUTION

## CORE DECISION RULE

**Cooperate if and only if:**
- The observed cooperation rate in the previous round exceeded a dynamic threshold
- OR we are in round 1 (initialization phase)
- OR the estimated collective payoff from universal cooperation exceeds our individual defection payoff

**Defect if:**
- Cooperation rate has fallen below threshold for two consecutive rounds
- OR we detect systematic free-riding without reciprocal benefit

## THRESHOLD FUNCTION

Set the cooperation threshold adaptively based on:

```
threshold(round) = max(0.3, 1 - (round / r) * 0.5)
```

Interpretation: We start generous (threshold ≈ 0.3) and become more demanding as rounds progress, peaking at 0.5 near the end. This creates pressure for maintaining cooperation while allowing for natural decay.

## ROUND-SPECIFIC LOGIC

**Round 1 (Initialization):**
- COOPERATE unconditionally
- Goal: Establish willingness to contribute and gather baseline information

**Rounds 2 to r-2 (Cooperation Phase):**
- If cooperation_rate(round t-1) ≥ threshold(t): COOPERATE
- Else if cooperation_rate(round t-1) < threshold(t) AND declining_trend observed: DEFECT
- Else: COOPERATE (benefit of doubt on stagnation)

**Rounds r-1 to r (End Game):**
- If cooperation_rate(round t-1) ≥ 0.5: COOPERATE
  - Last chance to build final payoff through collective action
- Else: DEFECT
  - Late defectors have shown their preference; minimize losses

## ADAPTATION MECHANISM

**Track per-player behavior:**
- Identify consistent contributors (always cooperated, rounds 2-t)
- Identify consistent defectors (never cooperated)
- Flag late switchers (changed behavior recently)

**Adjust strategy if:**
- Overall cooperation collapses (rate < 0.2): DEFECT immediately (protect against invasion)
- Only 1-2 players sustaining cooperation: DEFECT (insufficient collective action)
- Majority sustaining cooperation (rate > 0.6): COOPERATE (reward critical mass)

## EDGE CASE HANDLING

**If you're the only cooperator:**
- Defect in next round (you're being exploited)
- Resume cooperation only if others reciprocate

**If everyone else defects from round 1:**
- Defect from round 2 onward (no collective opportunity)

**Noisy or inconsistent opponents:**
- Apply moving average of last 3 rounds to filter noise
- Require 2-round confirmation before shifting strategy

## COLLECTIVE RATIONALE

This strategy is **collectively optimal** because:

1. **Mutual benefit orientation:** We cooperate when others cooperate, creating positive-sum outcomes (multiplier effect with k > 1)

2. **Transparency-based trust:** We reward observed cooperation and punish observed defection—making our strategy predictable and fair

3. **Collective threshold:** We don't demand 100% cooperation (unrealistic); instead, we calibrate expectations to what a majority can sustain

4. **Resilience:** We exit cooperation only when it's clearly failing, limiting damage from exploitation while remaining open to recovery

5. **End-game sacrifice:** In final rounds, we don't immediately defect (prisoner's dilemma temptation), but only if the group has already fragmented

## TOURNAMENT ROBUSTNESS

- Against pure cooperators: Cooperates, mutual high payoff
- Against pure defectors: Defects after round 1, minimizes losses
- Against tit-for-tat: Cooperates (matched), stable equilibrium
- Against majority strategies: Aligns with the emergent norm
- Against exploiters: Detects and isolates them quickly
'''

description_COLLECTIVE_18 = '''
# ADAPTIVE CONDITIONAL COOPERATION STRATEGY FOR PGG

## CORE PRINCIPLE
Cooperate conditionally based on observed cooperation rates, with gradual defection triggers and round-dependent adjustments. The strategy prioritizes collective welfare while protecting against systematic exploitation.

## DECISION RULES

### Round 1 (Opening Move)
**Cooperate.** This serves as a cooperative signal and gathers information about opponent types. The cost is minimal (1 token) and the information value is high.

### Rounds 2 through r-1 (Adaptive Cooperation Phase)
Calculate the **cooperation rate in the previous round**: cooperation_rate = (total contributions in previous round) / n

**If cooperation_rate ≥ 0.5:**
- Cooperate
- Rationale: Majority cooperation indicates a cooperative environment. Matching this behavior sustains collective welfare and is the payoff-maximizing response when others cooperate.

**If cooperation_rate < 0.5 and cooperation_rate ≥ 0.25:**
- Cooperate with declining probability: P(cooperate) = 2 × cooperation_rate
- Rationale: Moderate defection warrants cautious cooperation. This threshold prevents immediate collapse to universal defection while protecting against free-riding.

**If cooperation_rate < 0.25:**
- Defect
- Rationale: When cooperation drops below 25%, the public good is collapsing. Further cooperation becomes individually wasteful without collective benefit. Defection is a rational response to group failure.

### Round r (Final Round)
**Defect.** 
- Rationale: The standard finality problem applies—there are no future rounds to influence. Cooperation has no future payoff benefit, and the marginal gain from contributing your last token is negative. This is individually rational and assumed by rational opponents.

## EDGE CASES & REFINEMENTS

**Unanimous Cooperation (cooperation_rate = 1.0):**
- Cooperate unconditionally. This is the collective optimum state.

**Uniform Defection (cooperation_rate = 0):**
- Defect. No payoff advantage to unilateral cooperation.

**All Others Defect, You Alone Consider Cooperating:**
- Your contribution alone yields payoff: (k/n) - 1. This is negative when k < n (assumed). Defect.

**Two-Round Games (r=2):**
- Round 1: Cooperate (as specified)
- Round 2: Defect (final round rule)

**High Multiplier (k close to n):**
- The strategy remains valid. Higher k makes cooperation more attractive, but the relative thresholds still apply. Defection in round r remains optimal.

**Noisy Observations (possible misreporting):**
- The strategy relies on observed contributions. If you doubt data integrity, increase defection threshold by 10 percentage points (0.35 instead of 0.25).

## COLLECTIVE ALIGNMENT

This strategy prioritizes **group welfare** over pure self-interest:

- **Round 1 cooperation** assumes others may be cooperative, enabling mutually beneficial outcomes.
- **Majority rule (0.5 threshold)** sustains cooperation when it's broadly viable.
- **Graceful degradation (0.25 threshold)** allows partial cooperation environments to persist longer than immediate defection would.
- **Final round defection** acknowledges that finite games create unavoidable defection pressure, but this sacrifice is minimized by maximizing cooperation in earlier rounds.

The strategy is **robust** because it adapts to independent opponent strategies without requiring explicit coordination. It rewards cooperation without being exploitable (defects when cooperation falls too low) and avoids the tragedy of the commons through dynamic threshold monitoring.
'''

description_COLLECTIVE_19 = '''
# ADAPTIVE COLLECTIVE STRATEGY FOR PUBLIC GOODS GAME

## CORE PHILOSOPHY
Maximize collective welfare while remaining robust to defection. The strategy treats the PGG as a problem of building and maintaining cooperative equilibrium through:
1. **Reciprocal generosity** - Reward cooperative communities
2. **Graduated punishment** - Defection detection and response
3. **Recovery pathways** - Offer opportunities to rejoin cooperation
4. **Temporal adaptation** - Adjust strategy as we learn opponent types

---

## DECISION RULES

### ROUND 1 (INITIALIZATION)
**Action: CONTRIBUTE (C)**

Rationale: Start cooperatively to signal trustworthiness and gather baseline information about opponent tendencies. This is the lowest-risk initialization that enables mutual benefit discovery.

---

### ROUNDS 2 TO (r-1) (REPEATED GAME PHASE)

**Calculate opponent cooperation rate:**
- For each opponent j, count their contributions across all prior rounds
- Compute: `cooperation_rate_j = total_contributions_j / rounds_played_so_far`

**Classify opponents into tiers:**
- **Reliable cooperators** (cooperation_rate ≥ 0.8): Assume committed to mutual benefit
- **Conditional cooperators** (0.4 ≤ cooperation_rate < 0.8): Reciprocal players who respond to environment
- **Defectors** (cooperation_rate < 0.4): Predominantly self-interested

**Decision logic:**

1. **If you are a reliable cooperator yourself** (own prior contribution rate ≥ 0.8):
   - CONTRIBUTE if: average_cooperation_rate_of_all_opponents ≥ 0.5
   - DEFECT if: average_cooperation_rate_of_all_opponents < 0.5
   
   *Rationale: Maintain high cooperation as long as collective welfare is being generated. Switch to defection only if the environment has degraded enough that individual payoff maximization makes sense.*

2. **If you are a conditional cooperator** (own prior contribution rate between 0.4-0.8):
   - CONTRIBUTE if: at least 50% of opponents are in "reliable cooperator" or "conditional cooperator" tiers
   - DEFECT if: more than 50% of opponents are "defectors"
   
   *Rationale: Match the community's cooperation level. Stay engaged if there's a viable cooperative coalition.*

3. **If you are a defector** (own prior contribution rate < 0.4):
   - CONTRIBUTE if: you observe a sudden shift where >70% of opponents became reliable cooperators (signal of emerging strong norm)
   - Otherwise DEFECT
   
   *Rationale: Exploit until cooperation becomes too dominant to ignore. Re-entry happens only if collective behavior shifts dramatically.*

**Special condition - Endgame prevention:**
- If you detect that **all other opponents** will likely defect in the final round, consider defecting in round (r-1) as well
- This prevents one-round defection exploitation cycles

---

### FINAL ROUND (ROUND r)

**Action: DEFECT (D)**

Rationale: With no future interactions, the multiplier benefit expires. Standard backward induction applies. Contributing in the final round provides no strategic advantage for future reciprocity.

---

## EDGE CASES & SPECIAL SCENARIOS

### Two-player game (n=2)
- Multiplier k is constrained to k=1, making contribution pointless
- Action: DEFECT all rounds
- (This is a degenerate case; the strategy above still applies formally but yields D throughout)

### High multiplier (k close to n)
- Collective benefit is very strong
- Lower the cooperation_rate thresholds by 0.15 (e.g., trigger cooperation at 0.35 instead of 0.5)
- Rationale: High k increases returns to cooperation for all players

### Very short games (r ≤ 3)
- Skip the final-round defection rule for rounds 1 and 2 in a 3-round game
- Only apply the final-round defection to round 3
- Rationale: With few rounds, reputation effects matter more than backward induction

### Uniform defection observed
- If all opponents defect in round 2, you may DEFECT thereafter
- But in round 3, re-test with CONTRIBUTE to see if it was a fluke
- Rationale: Avoid lock-in to mutual defection when a partner might be experimenting

---

## COLLECTIVE ALIGNMENT

This strategy prioritizes collective welfare through:

1. **Threshold-based reciprocity**: You contribute more when others do, amplifying positive feedback
2. **Community recovery**: Allows re-entry for former defectors if norms strengthen—not purely punitive
3. **Emergent norm sensitivity**: Responds to the actual cooperation level rather than assuming fixed types
4. **Graduated transitions**: Smooth shifts between tiers rather than binary reactions
5. **Welfare-oriented**: The decision to defect only when average cooperation drops below 0.5 ensures you switch strategies only when collective payoff genuinely declines

The strategy is **robust** because it does not assume shared communication or enforcement, and it **adapts** because opponent tiers are continuously updated based on observed behavior.
'''

description_COLLECTIVE_20 = '''
# ADAPTIVE COLLECTIVE CONTRIBUTION STRATEGY FOR PUBLIC GOODS GAMES

## CORE PRINCIPLE
Maximize collective welfare by maintaining a sustainable contribution level that outperforms mutual defection, while protecting against exploitation. The strategy balances optimism about reciprocation with pessimism about free-riding.

## DECISION RULES

### PHASE 1: INITIAL EXPLORATION (Round 1)
**Action: CONTRIBUTE**

Rationale: Start cooperative to signal willingness to participate in the public good. This establishes a baseline for learning opponent types and tests whether mutual gain is achievable with this group.

### PHASE 2: ADAPTIVE RECIPROCATION (Rounds 2 through r-2)

Calculate the **collective contribution rate** from the previous round:
- contrib_rate = (total contributions in round t-1) / n

**Decision Logic:**
1. If contrib_rate ≥ (n-1)/n * 0.5 (at least half the group contributed):
   - **CONTRIBUTE** - Reciprocate cooperation momentum
   
2. If (n-1)/n * 0.25 < contrib_rate < (n-1)/n * 0.5 (weak cooperation):
   - Compute expected payoff from contributing: (k/n) * contrib_rate + contribution value relative to defection
   - If k/n * contrib_rate ≥ 0.6 (net positive externality):
     - **CONTRIBUTE** - Maintain the cooperative equilibrium
   - Else:
     - **DEFECT** - Signal withdrawal from unsustainable cooperation

3. If contrib_rate ≤ (n-1)/n * 0.25 (low cooperation, <25% participation):
   - **DEFECT** - The public good is insufficient to justify contribution cost

### PHASE 3: ENDGAME ADJUSTMENT (Rounds r-1 and r)

**Final round (r):**
- If contrib_rate in round r-1 ≥ 0.4:
  - **CONTRIBUTE** - Reinforce cooperation even if no future payoff depends on reputation
- Else:
  - **DEFECT** - No future rounds, minimize cost

**Second-to-last round (r-1):**
- If contrib_rate in round r-2 ≥ 0.5:
  - **CONTRIBUTE** - Signal strength to influence final round
- Else:
  - **DEFECT** - Prepare for defection cascade in final round

## EDGE CASES & SPECIAL HANDLING

**When n is very small (n ≤ 3):**
- Increase thresholds by 20% (higher bar for cooperation) because individual action has outsized impact
- One defector can make contributions unprofitable

**When k is near 1 (weak multiplier, k < 1.5):**
- Shift to stricter Phase 2 criteria; only contribute if contrib_rate ≥ 0.6
- The public good doesn't amplify enough to justify individual cost

**When observing persistent defectors:**
- Track individual contribution history separately (implicit reputation)
- If any single player defects every round, your future contributions become less dependent on total contributions; remain cooperative only if others collectively justify it

**When all players defect in any round:**
- Continue to **CONTRIBUTE** in the next round (one-shot test)
- If defection persists after your test, **DEFECT** in subsequent rounds

## COLLECTIVE ALIGNMENT

This strategy embodies collective welfare by:
- **Initiating cooperation** to create mutual benefit opportunities
- **Tolerating temporary free-riding** at moderate levels (25-50% defection) while the public good remains viable
- **Withdrawing support** only when the group's cooperation rate falls below sustainability
- **Avoiding punishment spirals** that destroy total welfare
- **Prioritizing group payoff over individual advantage** when both paths are available

The strategy is **collectively rational**: it seeks equilibria where all players benefit relative to mutual defection, rather than pursuing individual maximum payoff.
'''

description_COLLECTIVE_21 = '''
# ADAPTIVE COLLECTIVE STRATEGY FOR PUBLIC GOODS GAME

## CORE PRINCIPLE
Maximize collective welfare by promoting cooperation when conditionally sustainable, while protecting against exploitation through credible defection threats.

## DECISION RULE FRAMEWORK

### ROUND 1 (Initialization)
**COOPERATE**
- Cooperation is the only way to signal willingness to build collective value
- Defection in round 1 forecloses all cooperative pathways
- Sets cooperative tone for information revelation

### ROUNDS 2 through (r-1) (Main Phase)

**Calculate the "Cooperation Health Index":**
1. Measure the average contribution rate across all players in the previous round
2. Identify the median contribution level (to detect whether a majority cooperates)
3. Assess individual player reliability: track each opponent's contribution consistency

**Decision Logic:**

**IF** (average contribution rate in last round ≥ 50%) **THEN**
- **COOPERATE** (reinforce emerging cooperation norm)
- Exception: If you personally have been deceived (you cooperated but others didn't), apply "Conditional Skepticism" → defect this round, then return to cooperation only if the majority returns to cooperation

**ELSE IF** (average contribution rate in last round 20-50%) **THEN**
- **DEFECT** (the marginal benefit of cooperation disappears below critical mass)
- Monitor: If cooperation recovers above 50% in the next round, immediately return to cooperation

**ELSE** (average contribution rate < 20%) **THEN**
- **DEFECT** (the commons is collapsing; individual protection is rational)
- Continue defection; only return if you observe a clear, sustained recovery (≥ 2 consecutive rounds at ≥50%)

### ROUND r (Final Round - CRITICAL EDGE CASE)

**DEFECT**
- The repeated-game incentive structure collapses because there are no future rounds
- Cooperation in the final round cannot be rewarded or punished
- Standard backward induction applies
- Defecting here does not damage future relationships (there is no future)

---

## ROBUSTNESS MECHANISMS

**Against Exploitation (Always-Defect Opponents):**
- If you detect that a player has defected every round while you've been cooperating, treat them as non-contributors to the implicit norm and match their defection going forward
- This prevents one bad actor from destabilizing your entire strategy

**Against Noise/Mistakes:**
- Single defections by otherwise cooperative players don't trigger immediate retaliation
- Wait for a pattern (2+ defections) before assuming malice

**Against Threshold Uncertainty:**
- Use the median and mean together: if the median is above 50% but mean is lower, high variance exists
- Cooperate with cautious optimism (trusting the median trend)

**Against Varying Group Sizes (n parameter):**
- The multiplier k is fixed in the rules, but adjust sensitivity to contribution rates:
  - Larger n → each individual contribution matters less → set threshold for defection slightly higher (55% vs 50%)
  - Smaller n → each defection is more visible and painful → maintain stricter thresholds

---

## COLLECTIVE ALIGNMENT

**Why this serves the collective:**
- Rounds 1 through (r-1): The strategy achieves cooperation whenever a critical mass of players are willing, generating maximal total payoff
- The defection threshold (50%) is calibrated so that if at least half the players follow this strategy, all of them cooperate with each other, creating a cooperative coalition
- Final round defection is inevitable game theory, not collective betrayal—it's rational for all players simultaneously
- The "Conditional Skepticism" rule prevents free-riders from destroying the coalition by punishing defectors proportionally

**Why this is robust:**
- No dependency on communication or pre-coordination
- Triggers only on observable history
- Scales adaptively with group contribution levels
- Distinguishes between honest drops in participation and deliberate exploitation

---

## SUMMARY TABLE

| Round Phase | Condition | Action | Rationale |
|---|---|---|---|
| Round 1 | Always | **COOPERATE** | Signal willingness; enable information flow |
| Rounds 2–(r-1) | Avg contribution ≥ 50% | **COOPERATE** | Sustain critical mass |
| Rounds 2–(r-1) | Avg contribution 20–50% | **DEFECT** | Marginal benefit gone; protect yourself |
| Rounds 2–(r-1) | Avg contribution < 20% | **DEFECT** | Commons collapsed |
| Round r | Always | **DEFECT** | No future penalties; backward induction |
'''

description_COLLECTIVE_22 = '''
# ADAPTIVE COLLECTIVE STRATEGY FOR PUBLIC GOODS GAME

## CORE PRINCIPLE
Maximize collective welfare by identifying and reinforcing cooperation clusters while remaining robust to defection and free-riding. The strategy balances reciprocity with pragmatism.

---

## DECISION RULES

### ROUND 1 (Initial Probe)
**CONTRIBUTE**

Rationale: Start cooperatively to signal openness to coordination and gather information about opponent types. The first round establishes baseline expectations.

### ROUNDS 2 through (r-1) (Adaptive Phase)

**Calculate Cooperation Health:**
- For each opponent, compute their contribution rate in all previous rounds
- Identify players as: **Cooperators** (≥75% contribution), **Conditional** (25-75%), or **Defectors** (<25%)

**Decision Logic:**

**IF** (proportion of Cooperators among all opponents) > threshold_coop:
- **CONTRIBUTE** — Reinforce the cooperative cluster
- Threshold = max(0.3, k/n) — require at least 30% cooperators, or a fraction reflecting the game's multiplier effect

**ELSE IF** (proportion of Conditional players) is sufficiently large AND my recent payoff trend is positive:
- **CONTRIBUTE** — Attempt to uplift conditional players by demonstrating reciprocal cooperation

**ELSE IF** (my cumulative payoff ranks in top half relative to others) AND (defectors are dominant):
- **DEFECT** — Preserve advantage against a defecting majority; cooperating here is unilateral loss

**ELSE** (defectors dominant AND my payoff is below median):
- **CONTRIBUTE** — Make one more cooperative gesture as a "reset attempt"; if not reciprocated in next round, switch permanently to DEFECT

### FINAL ROUND (r) (Closure)

**IF** (average cooperation rate across all opponents ≥ 50%):
- **CONTRIBUTE** — End on a cooperative note and reinforce collective trust for any repeated future interactions

**ELSE:**
- **DEFECT** — No future rounds; extract remaining value in a defecting environment

---

## EDGE CASES & SPECIAL HANDLING

**Unanimous Defection Scenario:**
If all opponents defect for 3+ consecutive rounds, switch to permanent DEFECT. Continuing to contribute is not collective welfare maximization; it's self-sacrifice with no reciprocal benefit.

**Sudden Regime Change:**
If cooperation rate drops >40 percentage points in a single round, treat as a signal of environmental instability. Reduce contribution likelihood by 20% in the next round (shift thresholds upward) to avoid being exploited during transition.

**Low Multiplier (k close to 1):**
When k ≤ 1.5, the game is less beneficial for collective contribution (individual cost ≈ group benefit). Require higher cooperation thresholds (shift from 0.3 to 0.5 minimum cooperator proportion) before contributing in later rounds.

**High Multiplier (k close to n):**
When k ≥ (2/3)n, cooperation is highly valuable. Lower thresholds; contribute even if conditional players form a smaller group, as the multiplier justifies the risk.

---

## ROBUSTNESS PROPERTIES

**Against Defectors:** The strategy does not perpetually punish itself; it adapts away from uniform defection environments.

**Against Tit-for-Tat:** Respects and mirrors reciprocators; avoids being exploited by matching their defection only after clear patterns.

**Against Mixed/Noisy Opponents:** Uses rate-based thresholds (not single-action responses) to avoid overreacting to random noise.

**Collective Alignment:** Explicitly rewards cooperative clusters (not just individual payoff maximization) by contributing when other cooperators are present, creating positive feedback for collective welfare.

---

## SUMMARY

**Contribute when:** Cooperators are visible and form a meaningful minority (≥30%), OR you're making a final reset attempt against defection, OR the game incentive structure (high k) makes cooperation mathematically sound.

**Defect when:** Defectors dominate, payoff trails, AND cooperation has not reciprocated, OR the final round arrives in a low-cooperation environment.
'''

description_COLLECTIVE_23 = '''
# COLLECTIVE STRATEGY FOR REPEATED PUBLIC GOODS GAME

## CORE STRATEGY: ADAPTIVE CONDITIONAL COOPERATION WITH DECAY

### PHASE 1: INITIAL EXPLORATION (Rounds 1-2)
**Action: CONTRIBUTE**

Begin with universal cooperation to:
- Signal good faith and gather baseline data on opponent types
- Establish a cooperative reference point for comparison
- Avoid immediate defection which risks mutual defection spirals

### PHASE 2: ADAPTIVE CONTRIBUTION (Rounds 3 to r-2)

**Decision Rule - Contribution Rate Based on Collective Health:**

Calculate the **historical cooperation rate** across all players:
- `coop_rate = (total contributions observed so far) / (maximum possible contributions so far)`

**IF coop_rate ≥ 0.6:**
  - CONTRIBUTE
  - Rationale: Sufficient collective participation justifies individual contribution

**IF 0.3 < coop_rate < 0.6:**
  - CONTRIBUTE with probability = coop_rate
  - Rationale: Mirror the group's propensity to cooperate; probabilistic matching encourages convergence without deterministic punishment

**IF coop_rate ≤ 0.3:**
  - DEFECT
  - Rationale: When defection dominates, contributing becomes individually irrational without enforcement; save resources

### PHASE 3: FINAL ROUND (Round r)
**Action: DEFECT**

Defect on the last round because:
- No future payoff from cooperation
- Standard game-theoretic logic eliminates incentive to contribute
- Acknowledged as a weakness (see robustness discussion below)

---

## EDGE CASES & REFINEMENTS

**Unanimous Defection (coop_rate = 0):**
- Continue defecting until cooperation signal emerges
- Do not unilaterally restart cooperation after mutual defection

**Round 1 Outlier:**
- If everyone contributes round 1, maintain contribution
- If even one player defects round 1, trigger probabilistic matching from round 3 onward

**Asymmetric Information Recovery:**
- If cooperation rate drops sharply (decline > 20% in one round), assume strategy shift by opponents
- Reset to probabilistic matching rather than dropping to pure defection (give one cycle to recover)

---

## COLLECTIVE ALIGNMENT

This strategy prioritizes **group welfare while respecting individual incentives**:

1. **Conditional Reciprocity:** Contribution level depends on observed group cooperation, creating positive feedback loops for mutual contribution

2. **Proportional Matching:** The probabilistic rule (contribution probability = cooperation rate) balances:
   - Not punishing yourself when group fails
   - Signaling willingness to cooperate when group shows promise
   - Avoiding exploitability by defectors

3. **Graceful Degradation:** As defection increases, your strategy scales contribution down smoothly rather than switching abruptly, leaving room for groups to recover

4. **Collective Measurement:** Uses group-level statistics (not bilateral grudge-matching), so the strategy scales to any group size and incentivizes players to cooperate with the *entire group*, not just reciprocate bilaterally

---

## KNOWN LIMITATION

The **final-round defection** violates collective spirit. An alternative for truly collective play:
- Contribute in round r with probability proportional to coop_rate
- This signals commitment but risks exploitation by savvy defectors

However, given the tournament context with unknown opponents, the pure defection in round r is strategically safer.
'''

description_COLLECTIVE_24 = '''
# COLLECTIVE STRATEGY FOR PUBLIC GOODS GAME

## CORE PHILOSOPHY
This strategy prioritizes **sustainable collective welfare** while remaining robust to defection. It uses conditional cooperation with adaptive thresholds, treating the game as an opportunity to establish and maintain a productive common pool.

---

## DECISION RULES

### PRIMARY RULE: Conditional Cooperation with Threshold
**Contribute (C) if and only if:**
- The observed cooperation rate in the previous round meets or exceeds a dynamic threshold, OR
- This is round 1 (initialize cooperation)

**Defect (D) if:**
- The cooperation rate falls below threshold, AND
- Defection is sustained for 2+ consecutive rounds (allowing for single-round noise)

### THRESHOLD CALCULATION
```
threshold(round) = max(0.4, 1 - (round / total_rounds) * 0.3)
```

This means:
- Early rounds: ~40% cooperation required (permissive, inviting others to cooperate)
- Late rounds: threshold relaxes slightly as end-game approaches (accounts for final-round defection temptation)
- The threshold prevents race-to-the-bottom but adapts to actual group productivity

### DYNAMIC RECOVERY RULE
If cooperation rate was below threshold but shows **improvement of 15+ percentage points** in the current round, return to cooperation. This signals responsiveness to group attempts to restore cooperation.

---

## EDGE CASES

### Round 1
- **Action:** COOPERATE
- **Rationale:** Establish baseline of trust; demonstrate willingness to contribute to collective good. Sets cooperative equilibrium as the initial point.

### Final Round (Round r)
- **Action:** COOPERATE if threshold is met in round r-1, otherwise DEFECT
- **Rationale:** Avoid last-round defection exploitation that would destroy cooperation, but acknowledge that punishment is impossible after the game ends. If others are cooperating, honor it; if they've already defected, no incentive to give them final-round free riders' advantage.

### Round 2
- **Action:** Cooperate (reset buffer)
- **Rationale:** One-round defection signals may be noise or misunderstanding. Only shift strategy after consistent patterns emerge.

### Tie-Breaking (exactly at threshold)
- **Action:** COOPERATE
- **Rationale:** Optimism bias toward collective gain when decision is marginal.

---

## COLLECTIVE ALIGNMENT

This strategy embodies collective welfare by:

1. **Starting cooperative:** Opens door for mutual benefit rather than assuming defection
2. **Sustainable reciprocity:** Conditions future cooperation on group performance, not individual punishment—rewards collective discipline, not individual compliance
3. **Forgiveness with limits:** Allows single-round deviations (noise, misunderstanding) but punishes sustained defection
4. **Resilience:** Recovery mechanism enables groups to reestablish cooperation even after breakdown, rather than locking into defection spirals
5. **Efficiency-conscious:** The 40% threshold allows groups that achieve even modest cooperation to continue contributing, generating positive returns

---

## ROBUSTNESS NOTES

- **Against free riders:** Defects when they dominate, protecting against exploitation
- **Against random players:** Threshold tolerance absorbs noise without cascading to mutual defection
- **Against tit-for-tat:** Aligns naturally; both strategies cooperate when others cooperate
- **Against greedy agents:** Punishes with defection but reopens if they adjust
- **Tournament dynamics:** The strategy doesn't require common knowledge or coordination—only observes and responds to empirical cooperation rates
'''

description_COLLECTIVE_25 = '''
# COLLECTIVE STRATEGY FOR PUBLIC GOODS GAME

## CORE PRINCIPLE
Maximize collective welfare through conditional cooperation that adapts to observed group behavior, while maintaining individual rationality as a safeguard against systematic exploitation.

## DECISION RULES

### Round 1 (Initial Round)
**COOPERATE (Contribute)**

Rationale: The first round is a signal of good faith. Since no history exists, cooperation initiates a cooperative equilibrium. The expected payoff from mutual cooperation exceeds mutual defection when k > 1.

### Rounds 2 through (r-1) (Middle Rounds)
**ADAPTIVE CONDITIONAL COOPERATION**

Calculate the group cooperation rate from the previous round:
- cooperation_rate = (total_contributors_last_round) / n

Apply this decision rule:
- If cooperation_rate ≥ 0.5: **COOPERATE**
  - The group is in a cooperative regime; maintain it through reciprocal contribution
  
- If cooperation_rate < 0.5: **DEFECT**
  - The group has crossed the threshold into defection. Protect against exploitation by withholding contribution
  - Exception: If cooperation_rate is between 0.3 and 0.5, COOPERATE anyway
    - Rationale: Attempt to resuscitate cooperation with a minority presence, as the cost is bounded while the upside if others follow is substantial

### Final Round (Round r)
**DEFECT (Contribute 0)**

Rationale: Standard backward induction logic applies. Since there is no future round, the shadow of the future disappears. Cooperation carries no strategic value. However, if cooperation_rate in round (r-1) was ≥ 0.7, **COOPERATE** anyway.
- The 0.7 threshold indicates robust cooperation deserves respect at the terminal stage to avoid "cheap" final-round defection

## EDGE CASES & REFINEMENTS

**Handling Isolated Defectors:**
If exactly 1 player defected last round while everyone else cooperated, still cooperate. Single defectors are noise, not a regime change.

**Cascading Defection Prevention:**
If you observe your own previous defection led to decreased cooperation in the group, return to cooperation in the next round (a "reset" attempt) unless defection is now universal.

**Extreme Cases:**
- If everyone defected last round and you are now alone to cooperate: DEFECT (no mutual benefit possible)
- If you are alone in defecting against universal cooperation: COOPERATE (rejoin; you were the anomaly)

## COLLECTIVE ALIGNMENT

This strategy embodies collective rationality because:

1. **Cooperation as Default**: Initiates and maintains socially beneficial equilibria when possible
2. **Threshold-Based Reciprocity**: Responds to genuine shifts in group behavior, not individual whims
3. **Stability Seeking**: The 0.5 threshold and hysteresis (0.3-0.5 exception) prevent oscillation and increase predictability
4. **Terminal Honesty**: The 0.7 exception in the final round respects groups that sustained high cooperation, avoiding free-riding at the last moment
5. **Graceful Degradation**: When defection dominates, the strategy exits cleanly rather than cycling between punishment and naive cooperation

The strategy assumes no shared coordination mechanism exists but leverages observable history to approximate a collectively rational outcome through transparent, conditional behavior.
'''

description_COLLECTIVE_26 = '''
# ADAPTIVE CONDITIONAL COOPERATION WITH DECAY

## CORE STRATEGY

### Decision Rule (All Rounds)

**Cooperate if and only if:**
- The observed cooperation rate in the previous round was >= (k-1)/k
- OR this is round 1 (bootstrap cooperation)
- OR fewer than 3 rounds have been played (give benefit of doubt early)

**Otherwise: Defect**

### Rationale

The threshold (k-1)/k represents the breakeven point where collective cooperation becomes individually rational. When enough others cooperate to meet this threshold, mutual cooperation is self-sustaining. Below this threshold, defection becomes the dominant response.

---

## HANDLING EDGE CASES

**Round 1:**
- Cooperate unconditionally
- This is the only opportunity to initiate cooperation and signal willingness to participate in collective benefit

**Round 2-3:**
- Cooperate regardless of round 1 outcome
- Rationale: Small sample sizes are unreliable; establish a grace period to distinguish systematic defectors from unlucky variance

**Round 4 through (r-2):**
- Apply core decision rule above
- Monitor the rolling average of cooperation rates with exponential weight on recent rounds (weight recent rounds 1.5x more heavily)

**Final 2 Rounds:**
- If cooperation rate has been >= (k-1)/k in the last 3 rounds: Cooperate
- Otherwise: Defect
- Rationale: Late-game defection by others becomes unrecoverable; don't throw away tokens on sure defectors. But sustain cooperation if the collective has been healthy.

---

## ROBUSTNESS FEATURES

**Against free-riders:**
- The defection trigger (cooperation rate < (k-1)/k) automatically punishes groups dominated by defectors
- You stop contributing when contributions no longer generate collective value

**Against noise/variance:**
- Three-round grace period and rolling averages prevent over-reaction to single-round deviations
- Threshold is mathematically grounded in payoff structure, not arbitrary

**Against dominance-seeking players:**
- You don't chase being the sole cooperator (that maximizes others' gains at your expense)
- You only cooperate when it's collectively rational

**Against mixed strategies:**
- Your deterministic rule is predictable and rewards other cooperative players, encouraging collective stability
- Non-determinism would reduce ability to coordinate with other conditional cooperators

---

## COLLECTIVE ALIGNMENT

This strategy prioritizes **sustainable collective welfare** over individual exploitation:

1. **Initiates cooperation** (round 1) to enable mutually beneficial outcomes
2. **Sustains cooperation** only when the group's cooperation is sufficient to justify it (threshold rule)
3. **Exits gracefully** when defection dominates, avoiding waste on non-reciprocal groups
4. **Transparent and legible** — other cooperative players can predict and reinforce your behavior

The strategy maximizes the probability of reaching a **cooperative equilibrium** if other agents are also capable of conditional cooperation, while minimizing losses if they are not.
'''

description_COLLECTIVE_27 = '''
# COLLECTIVE STRATEGY FOR PUBLIC GOODS GAME

## CORE PRINCIPLE
Maximize collective welfare by maintaining contribution levels that benefit the group, while protecting against exploitation through adaptive defection thresholds.

## DECISION RULES

### Round 1 (Initialization)
**Action: CONTRIBUTE**

Rationale: Start with cooperation to establish the potential for mutual benefit. This signals willingness to support the collective good and gathers information about opponent tendencies.

### Rounds 2 through (r-1) (Adaptive Phase)

**Calculate the "Collective Health Index" after each round:**
- CHI = (average contribution rate across all players) × (multiplier k)
- This measures whether the group is trending toward or away from mutual benefit

**Decision Logic:**

1. **If CHI ≥ (k/2)**: CONTRIBUTE
   - The group is maintaining healthy contribution levels relative to potential returns
   - Continuing cooperation reinforces positive momentum

2. **If (k/4) ≤ CHI < (k/2)**: CONTRIBUTE with probability proportional to CHI
   - Contribution is declining but not critically
   - Maintain cautious optimism while introducing probabilistic caution
   - Probability of contribution = CHI / (k/2)

3. **If CHI < (k/4)**: DEFECT
   - Contribution has collapsed; defection is now rational
   - The group cannot sustain mutual benefit
   - Switch to individual payoff maximization

**Individual Tracking Rule:**
- Monitor each opponent's contribution rate over the last m rounds (m = max(5, r/4))
- If an opponent has contributed 0% in the last m rounds, they are classified as a "persistent defector"
- Against persistent defectors: always DEFECT (they are not supporting the collective)

### Last Round (r)
**Action: DEFECT**

Rationale: In a finite game with known endpoint, the last round has no shadow of the future. Defection maximizes individual payoff with no reputational cost. This is subgame perfect and acknowledges the game's structure.

## HANDLING EDGE CASES

**Early Information Vacuum (Rounds 1-3):**
- Insufficient history to calculate meaningful CHI
- Default to CONTRIBUTE in round 2 even if CHI appears low
- This prevents premature defection spirals from random variation

**Unanimous Defection:**
- If all opponents defect in round 1, contribute in round 2 anyway
- Give the group one additional round to demonstrate reciprocity
- If defection persists into round 3, switch to DEFECT permanently

**Extreme Oscillation:**
- If contribution rate swings wildly (>50% variance across recent rounds), use the 5-round moving average instead of immediate CHI
- Reduces sensitivity to noise and prevents overreaction

## COLLECTIVE ALIGNMENT

This strategy embodies collective thinking through:

1. **Group Welfare Focus**: The CHI metric prioritizes what benefits everyone (contribution momentum) rather than pure individual advantage

2. **Graduated Response**: Rather than tit-for-tat punishment, use a threshold system that allows temporary group weakness without immediate defection—giving collective recovery a chance

3. **Efficiency**: Avoid costly punishment that harms both punisher and defector; instead, adjust behavior to reflect changed circumstances

4. **Robustness**: The strategy works against:
   - Pure cooperators (we cooperate back)
   - Pure defectors (we defect once we recognize the pattern)
   - Conditional cooperators (we maintain cooperation as long as the group sustains it)
   - Mixed strategies (the probabilistic middle tier adapts smoothly)

5. **Honest Realism**: Acknowledges the last-round paradox and finite game structure without claiming false long-term reciprocity where it cannot exist

## SUMMARY
**Cooperate when the collective is healthy, degrade gracefully as group contribution fails, defect only when individual rationality dominates or against confirmed non-contributors.**
'''

description_COLLECTIVE_28 = '''
# COLLECTIVE STRATEGY FOR PUBLIC GOODS GAME

## CORE PRINCIPLE
Maximize collective welfare by encouraging cooperation through **conditional reciprocity with progressive commitment**, while maintaining resilience against free-riders.

---

## DECISION RULE (STANDARD ROUNDS)

**Contribute (C)** if and only if:
- The average contribution rate in the previous round was ≥ 50%, OR
- This is round 1 (unconditional cooperation to establish baseline), OR
- Remaining rounds ≥ 3 AND average historical contribution rate (all past rounds) ≥ 40%

**Otherwise, Defect (D)**

---

## ROUND-SPECIFIC HANDLING

**Round 1:**
- Contribute (C). This signals cooperative intent and generates data on opponent types.

**Rounds 2 to (r-2):**
- Apply the standard decision rule above.
- Track each opponent's individual contribution pattern. If a specific player defected in round t but others contributed, weight the collective signal more than individual defections.

**Round (r-1):**
- Same as standard rule—do not abandon strategy in the penultimate round, as this signals commitment.

**Final Round (r):**
- Evaluate the full history. If average contribution rate > 50%, contribute (C). 
- Otherwise defect (D). This respects that final-round defection is common but avoids it if the group has sustained cooperation.

---

## ADAPTIVE MECHANISMS

**Decline from high cooperation:**
- If contribution rates drop by >25 percentage points between consecutive rounds, shift to defection for one round as a corrective signal, then re-evaluate.

**Recovery path:**
- If defection occurs but the next round shows renewed cooperation (>50%), immediately return to contributing. This prevents punishment spirals from locking in.

**End-game leverage:**
- With 2-3 rounds remaining and contribution rates ≥ 60%, increase contribution confidence. With ≤2 rounds and rates <40%, switch to unconditional defection.

---

## COLLECTIVE ALIGNMENT

- **Maximizes group payoff** by anchoring on 50% as the cooperation threshold—sustainable when k < n and roughly half the group cooperates.
- **Punishes free-riders implicitly** through defection when they dominate, creating negative feedback.
- **Avoids coordination failure** by not requiring explicit agreement; each player applies the same transparent rule.
- **Resilient to heterogeneity** by tracking aggregate trends rather than individual quirks.

---

## ROBUSTNESS

- **Against pure defectors:** Quickly shifts to D after round 1, limiting losses.
- **Against tit-for-tat:** Cooperates at similar rates, achieving mutual cooperation.
- **Against mixed strategies:** The 50% threshold and historical averaging smooth out noise.
- **Against late-round defection surges:** The final-round rule acknowledges this is inevitable but doesn't trigger a cascade.
'''

description_COLLECTIVE_29 = '''
# ADAPTIVE COLLECTIVE STRATEGY FOR PUBLIC GOODS GAMES

## CORE PRINCIPLE
Maximize collective welfare by sustaining cooperation through conditional reciprocity, while maintaining robustness against exploitation.

---

## DECISION RULE (PRIMARY)

**Contribute (C) if and only if:**

1. **First Round:** CONTRIBUTE
   - Establish cooperative intent and gather information about the player pool

2. **Subsequent Rounds:** Apply a two-threshold conditional strategy:

   **Threshold A (Cooperation Sustainability):**
   - Calculate the average contribution rate across all players in the previous round: `avg_contrib = (sum of all contributions) / n`
   - If `avg_contrib >= k/(k+1)`, CONTRIBUTE
   - Rationale: When enough players contribute, collective output exceeds individual defection payoff; cooperation is self-reinforcing

   **Threshold B (Selective Defection):**
   - If `avg_contrib < k/(k+1)`, count how many rounds this condition has persisted
   - If defection-pressure has lasted ≤ 2 consecutive rounds, CONTRIBUTE (attempt to stabilize)
   - If defection-pressure has lasted > 2 consecutive rounds, DEFECT (exit unsustainable equilibrium)

3. **Last Round Exception:**
   - If you detect you are in the final round (typically round r, or if round limit is unknown, apply decay: `if remaining_rounds ≤ 1`), shift to DEFECT
   - This accounts for end-game unraveling but only when certain

---

## RATIONALE FOR THRESHOLDS

**Why `k/(k+1)`?**
- When contribution rate ≥ `k/(k+1)`, the collective payoff from full cooperation exceeds individual defection payoff
- Below this threshold, the game favors defection; cooperation becomes a loss
- This threshold is parameter-aware and auto-calibrates to game structure

**Why 2-round tolerance?**
- Allows recovery from temporary fluctuations or unlucky variance
- Prevents hair-trigger abandonment of cooperation
- Demonstrates commitment while protecting against persistent exploitation

---

## HANDLING EDGE CASES

**Heterogeneous Opponents:**
- The strategy does not assume opponent types; it observes only aggregate contribution rates
- Works against pure defectors (triggers defection after 2 rounds), cooperators (sustains cooperation), and mixed strategies

**Free-Riders (Constant Defectors):**
- First two rounds: you contribute, free-riders defect, you gain their share of group output
- Rounds 3+: avg_contrib falls below threshold, triggering your defection
- Outcome: mutual defection; prevents exploitation from succeeding indefinitely

**Tipping Points:**
- If a minority of players defect and cooperative mass is large, you stay in cooperation (avg_contrib remains high)
- If cooperative coalition fragments, you exit gracefully before total payoff collapse

**Very Small n or Large k:**
- High k means contributions amplified; threshold remains valid
- Small n means individual behavior shapes average strongly; strategy is more reactive (appropriate for high feedback)

---

## COLLECTIVE ALIGNMENT

This strategy prioritizes:
1. **Collective Efficiency:** By sustaining cooperation when viable, you maximize total group welfare
2. **Fairness:** You follow the same rule as any other cooperative player; no special claiming
3. **Resilience:** You defect only when cooperation genuinely fails, signaling to others that the equilibrium is broken
4. **Transparency:** Decisions depend only on observable history; no hidden types or signaling

The strategy treats the group as a dynamic entity: it attempts to support cooperative coordination as long as critical mass exists, then gracefully exits when that support is no longer available.

---

## SUMMARY TABLE

| Situation | Action | Duration |
|-----------|--------|----------|
| Round 1 | C | — |
| avg_contrib ≥ k/(k+1) | C | Indefinite |
| avg_contrib < k/(k+1) for ≤2 rounds | C | Up to 2 rounds |
| avg_contrib < k/(k+1) for >2 rounds | D | Until recovery |
| Final/Last round detected | D | Final round only |
'''

description_COLLECTIVE_30 = '''
# COLLECTIVE STRATEGY FOR PUBLIC GOODS GAME

## CORE PRINCIPLE
Maximize collective welfare through conditional cooperation that rewards contribution and punishes free-riding, while maintaining robustness against exploitation.

## DECISION RULE

**Base Strategy: Conditional Contribution with Decay**

1. **First Round**: CONTRIBUTE
   - Establish cooperative intent and gather baseline information about opponent types
   - Signals willingness to pursue mutual benefit

2. **Subsequent Rounds**: 
   - Calculate the **collective contribution rate** from the previous round: (sum of all contributions) / n
   - Contribute IF AND ONLY IF the previous round's collective rate ≥ threshold(t)
   - Where threshold(t) adapts over time:
     - Rounds 1-3: threshold = 50% (allow coalition building)
     - Rounds 4 to (r-3): threshold = 60% (enforce meaningful cooperation)
     - Final 3 rounds: threshold = 70% (expect sustained commitment)

3. **Escalation for Persistent Defection**:
   - If ANY single opponent has defected in 3+ consecutive recent rounds, and the collective rate remains below 40%, shift to permanent DEFECT against that opponent (to the extent individual actions can be targeted through aggregate behavior)
   - The group strategy is to collectively reduce contributions if free-riders dominate

## EDGE CASES

**Last Round (Round r)**:
- If collective rate in round (r-1) ≥ threshold, CONTRIBUTE (reinforce cooperation to the end)
- Otherwise DEFECT (no future punishment possible; maximize individual payoff)

**Extreme Scenarios**:
- If all opponents defected in previous round: DEFECT (respond to universal defection)
- If all opponents contributed in previous round: CONTRIBUTE (reciprocate full cooperation)

## COLLECTIVE ALIGNMENT

This strategy embodies collective welfare through:

- **Reciprocity**: Contribution levels mirror the group's demonstrated commitment
- **Resilience**: The adaptive thresholds prevent exploitation while allowing recovery toward cooperation
- **Fairness**: All players face identical decision rules; no favoritism
- **Efficiency**: Threshold progression pushes toward k > 1 benefits as mutual trust builds
- **Self-correction**: Defection triggers group-level reduction in contributions, penalizing the free-rider ecosystem rather than escalating individual punishment

The strategy does NOT assume coordination but creates an **emergent incentive structure**: any group of players following this rule will naturally coordinate on higher contribution when others do the same, and will collectively withdraw support from persistent free-riders.
'''

description_COLLECTIVE_31 = '''
# ADAPTIVE RECIPROCAL CONTRIBUTION STRATEGY

## CORE PRINCIPLE
Contribute when historical evidence suggests sufficient collective participation will occur, withdraw when defection becomes dominant. Balance optimism about cooperation with pragmatic response to free-riding.

## DECISION RULES

### Round 1 (First Move)
**Contribute (C)**
- Start with cooperation to establish a cooperative signal and gather information about opponent types
- This is the only round where we act without history

### Rounds 2 through (r-1) (Repeated Rounds)
**Calculate the "Cooperation Ratio":**
- cooperation_ratio = (total contributions in all past rounds) / (number of players × number of past rounds)

**Decision Logic:**
1. **If cooperation_ratio ≥ (k - 1) / k:**
   - Contribute (C)
   - Rationale: When others cooperate at or above this threshold, collective contribution exceeds individual cost. The threshold (k-1)/k represents the break-even point where group benefit payoff k/n × c justifies individual cost of 1.

2. **If cooperation_ratio < (k - 1) / k:**
   - Defect (D)
   - Rationale: When cooperation falls below sustainability threshold, contributing becomes individually suboptimal and doesn't meaningfully support collective welfare.

**Secondary Adjustment - Detection of Coordinated Defection:**
- If cooperation_ratio has decreased for 3 consecutive rounds, defect regardless of current ratio
- Once 4 consecutive rounds show defection, lock into defect for remaining rounds
- Rationale: Recognize when the group has shifted to defection regime and avoid wasting tokens

### Round r (Final Round)
**Contribute (C)**
- Ignore the end-game logic that would otherwise incentivize defection
- Rationale: In a tournament against unknown opponents, final-round defection is predictable and damages collective reputation. Contributing until the end maintains dignity of collective strategy and respects players who reciprocated earlier.

## HANDLING EDGE CASES

**Against Pure Defectors:**
- Will defect after round 1, minimizing losses
- Recovers to C only if other defectors eventually leave (unlikely), protecting tokens

**Against Tit-for-Tat Variants:**
- Mutual cooperation is sustained as long as overall group ratio stays healthy
- Gracefully degrades if group shifts, rather than entering punishment spirals

**Small Groups (n=2,3):**
- Threshold (k-1)/k becomes more stringent (e.g., requires ~67% cooperation for n=2)
- Strategy naturally becomes more selective, appropriate to the vulnerability

**Very Short Games (r ≤ 3):**
- Contributes in round 1, uses limited history for round 2, contributes in final round
- Makes sense of scarce rounds

## COLLECTIVE ALIGNMENT

This strategy explicitly **maximizes expected group welfare** while maintaining individual rationality:

- **Not naive:** Withdraws when defection becomes dominant, avoiding futile contribution
- **Not selfish:** Contributes when contribution density suggests it benefits the collective
- **Not retaliatory:** Uses statistical patterns, not punishment logic
- **Tournament-aware:** Assumes no coordination but creates incentives toward cooperation through consistent reciprocity

The strategy communicates through action: "I will contribute if you do, and the group supports mutual contribution." This allows distributed coordination without explicit communication.
'''

description_COLLECTIVE_32 = '''
# ADAPTIVE RECIPROCAL CONTRIBUTION STRATEGY (ARCS)

## CORE PRINCIPLE
Maximize collective welfare by sustaining cooperation through conditional reciprocity, while defending against exploitation. The strategy treats the PGG as a repeated trust-building exercise where contribution levels signal reliability and merit continued investment.

## DECISION RULES

### Round 1 (Initialization)
**COOPERATE (Contribute 1 token)**

Rationale: Start optimistically to establish a cooperative baseline. This signals trustworthiness and maximizes information gain about opponent types in the first round.

### Rounds 2 through (r-1) (Reciprocal Adaptation)
Calculate the **recent cooperation rate** as the average contribution level of all other players across the last 3 rounds (or all available rounds if fewer than 3 have passed).

- **If recent_cooperation_rate ≥ 0.5:** COOPERATE
  - When others contribute at least half the time on average, reciprocate by contributing
  - This sustains mutually beneficial equilibria and rewards cooperative signals
  
- **If recent_cooperation_rate < 0.5:** DEFECT
  - When average cooperation falls below majority threshold, withhold contribution
  - This prevents one-sided exploitation and conserves tokens for later rounds
  - Defection signals displeasure and creates pressure for collective course correction

### Round r (Final Round)
**DEFECT (Contribute 0 tokens)**

Rationale: In the final round, future reputation is irrelevant. Defection maximizes individual payoff with no reciprocal consequences. This is strategically dominant and honest to the game structure.

---

## EDGE CASES & REFINEMENTS

**Heterogeneous Opponents:**
- The 3-round window prevents being locked into static responses; new cooperative signals are rewarded within 3 rounds
- If one player consistently defects while others cooperate, the strategy punishes that player while maintaining reciprocity with the cooperative majority

**Threshold Rationale (0.5):**
- At k > 1, cooperation becomes individually rational only if at least (1/k) of others cooperate
- Using 0.5 as the threshold is conservative: we cooperate when cooperation is sustainable, and defect when the group median is defecting
- This creates a self-reinforcing equilibrium around majority behavior

**Rounds 1-3 (Early Game):**
- Round 1: Cooperative signal establishes intent
- Rounds 2-3: Opponent types are revealed; strategy locks in reciprocal response
- Round 4 onwards: Stable reciprocal patterns emerge

**Declining Cooperation Over Time:**
- If cooperation gradually declines across rounds, the strategy tracks this decline and abandons cooperation when it becomes minority behavior
- Prevents sunk-cost fallacy of cooperating while others defect

---

## COLLECTIVE ALIGNMENT

This strategy pursues **group welfare maximization subject to individual rationality constraints**:

1. **It enables Pareto improvement:** When mutual cooperation arises, all players earn more than mutual defection
2. **It doesn't require altruism:** Reciprocity is self-interested; you only invest when others do
3. **It stabilizes coalitions:** By responding to majority behavior, it harnesses social proof dynamics to sustain cooperation
4. **It's transparent:** Observable past actions fully determine future actions; opponents can predict and respond rationally
5. **It punishes free-riding:** Defectors trigger collective defection, preventing exploitation of cooperators

The strategy embodies the principle: *"Contribute when others do; withdraw when they don't."* This is the most robust path to collective surplus in the absence of binding commitments.
'''

description_COLLECTIVE_33 = '''
# ADAPTIVE CONDITIONAL COOPERATION WITH DECAY (ACC-D)

## CORE PRINCIPLE
Maximize collective welfare by encouraging contribution while protecting against exploitation. Use conditional cooperation to build momentum, but escalate defection when cooperation erodes below sustainable thresholds.

## DECISION RULES

### Round 1 (Initialization)
**COOPERATE**
- Establish a cooperative signal and test the environment
- Signal willingness to contribute to collective value creation

### Rounds 2 through (r-2) (Adaptive Phase)
**Cooperation Threshold Rule:**

Calculate the cooperation rate in the previous round:
```
coop_rate = (total contributions in round t-1) / n
```

**IF** coop_rate ≥ (k-1)/k:
  - **COOPERATE**
  - The group is contributing enough that cooperation yields positive expected return
  - Maintain momentum

**ELSE IF** (k-1)/k > coop_rate ≥ (k-1)/(2k):
  - **COOPERATE** with probability proportional to coop_rate
  - More precisely: COOPERATE if coop_rate / ((k-1)/k) ≥ random[0,1]
  - Gracefully degrade as cooperation falls

**ELSE:**
  - **DEFECT**
  - Collective contribution has fallen below the point where cooperation generates positive returns
  - Recover the endowment rather than subsidize free-riders

### Final Round (r)
**DEFECT**
- No future rounds to build reciprocity
- Contribution in round r cannot influence future cooperation
- Defection maximizes individual payoff without long-term consequences

## EDGE CASES & REFINEMENTS

**All-defect scenario:**
If everyone defects from round 1, recognize this and continue defecting. The strategy gracefully accepts this equilibrium without wasting tokens.

**Individual free-riders:**
The strategy does not punish individual defectors; rather, it responds to aggregate cooperation. This avoids destructive mutual punishment spirals while still withdrawing support when contribution density declines.

**Perfect cooperation throughout:**
Continue cooperating through round (r-1). This maximizes collective value: k·n tokens created, divided equally.

**Threshold justification:**
The breakeven point is (k-1)/k because:
- If all n players contribute: each player receives k·n/n = k tokens, netting (k-1) profit
- At contribution rate (k-1)/k, expected return ≈ (k-1) tokens, justifying the 1-token cost
- Below this, expected returns fall below cost

## COLLECTIVE ALIGNMENT

This strategy:
- **Prioritizes group welfare:** Sustained cooperation maximizes total payoff when sustainable
- **Avoids defection traps:** Withdraws from doomed cooperation attempts rather than cascading into mutual punishment
- **Maintains robustness:** Does not require coordination or communication—adapts purely to observed outcomes
- **Balances fairness and pragmatism:** Cooperates when contributions are adequate, defects when they're insufficient (protecting yourself and signaling the unsustainability)

The strategy treats the last round as a known endpoint and behaves accordingly, while leveraging the shadow of the future in earlier rounds to encourage sustained cooperation.
'''

description_COLLECTIVE_34 = '''
# ADAPTIVE COLLECTIVE STRATEGY FOR PUBLIC GOODS GAME

## CORE PRINCIPLE
Maximize collective welfare by encouraging contribution while protecting against systematic defection. The strategy balances optimism about reciprocal cooperation with pragmatic defection when the group demonstrates it won't sustain contributions.

## DECISION RULES

### ROUND 1
**COOPERATE (contribute 1 token)**

Rationale: Establish a cooperative signal and test whether others will reciprocate. This reveals opponent types and provides baseline information.

### ROUNDS 2 to (r-1) - MIDDLE GAME
**Adaptive Conditional Cooperation with Decay Sensitivity**

Calculate the "collective contribution rate" from the previous round:
- contribution_rate = (total contributions in round t-1) / n

**Decision logic:**
- IF contribution_rate ≥ 0.5:
  - COOPERATE (contribute 1)
  - This threshold indicates the group is leaning cooperative; reinforce it
  
- IF 0.25 ≤ contribution_rate < 0.5:
  - COOPERATE (contribute 1)
  - Mixed signals warrant cautious optimism; cooperation may stabilize the group
  
- IF contribution_rate < 0.25:
  - DEFECT (contribute 0)
  - The group has entered a defection cascade; matching defection avoids exploitation
  - Exception: If this is only round 2, cooperate once more (allow one round for adjustment)

### FINAL ROUND (r)
**Strategic Defection Analysis**

- IF you have been cooperating and contribution_rate ≥ 0.5:
  - DEFECT (contribute 0)
  - Rationale: No future rounds mean no retaliation; capture private value
  
- IF contribution_rate < 0.5:
  - DEFECT (contribute 0)
  - The group is already defecting; self-preservation applies

**Exception (Collective Alignment):**
- IF ≥ 75% of players cooperated in round (r-1):
  - COOPERATE (contribute 1)
  - This indicates strong collective commitment; honor it even at the end
  - This maximizes the final collective outcome for aligned groups

---

## EDGE CASES & REFINEMENTS

**High Defection from Specific Players:**
- Do not track individual grudges—only aggregate group signals
- This prevents fragmented punishment spirals
- Rationale: Individual punishment is costly; collective sensitivity is sufficient

**Sudden Defection Cascades:**
- If contribution_rate drops ≥30 percentage points in a single round, remain defected for the next round before reassessing
- Prevents false signals from noise; confirms trend

**Rounds Near the End (last 3 rounds):**
- Reduce optimism thresholds slightly; shift from 0.5 to 0.45
- Rationale: Fewer rounds remain for recovery from exploitation

**All Defect or All Cooperate:**
- All Defect scenario: Defect (unavoidable equilibrium)
- All Cooperate scenario: Continue cooperating (maintain Pareto-optimal outcome)

---

## COLLECTIVE ALIGNMENT

This strategy:
1. **Prioritizes group outcomes** over individual payoff maximization in early-to-middle rounds
2. **Responds to collective signals**, not individual deviations
3. **Incentivizes cooperation** through reciprocity: groups that cooperate receive cooperation
4. **Protects against exploitation** by defecting when defection becomes dominant
5. **Maintains flexibility** to adapt if group composition or norms shift mid-game

The strategy is **robust** because it does not require coordination or communication—it infers collective intent from observable aggregate behavior and responds accordingly.
'''

description_COLLECTIVE_35 = '''
# Adaptive Collective Strategy for Public Goods Game

## CORE PRINCIPLE
Maximize collective welfare by maintaining cooperation when sustainable, while protecting against exploitation. The strategy balances optimism about reciprocal cooperation with pragmatic defection when the collective benefit deteriorates.

## DECISION RULES

### Primary Rule: Conditional Cooperation with Decay
- **Cooperate** if the average contribution rate in the previous round exceeded the sustainability threshold
- **Defect** if the average contribution rate falls below the sustainability threshold
- **Sustainability Threshold**: (k - 1) / k, the break-even point where collective contribution becomes individually rational

**Rationale**: When enough others contribute, contributing generates positive expected value for all. Below this threshold, defection is the only individually rational response, signaling that free-riding dominates the equilibrium.

### Secondary Rule: History-Weighted Momentum
- Weight recent rounds more heavily than distant rounds
- Use exponential decay: recent_trend = 0.7 × (last round) + 0.3 × (3-round average)
- If recent_trend > threshold: cooperate
- If recent_trend < threshold: defect
- If recent_trend ≈ threshold (within 0.1): cooperate (optimism bias for stability)

**Rationale**: Captures that current conditions matter more than ancient history, while preventing noisy single-round swings from destroying cooperation.

## EDGE CASES & TIMING

**Round 1 (First Round)**
- Cooperate unconditionally
- Establishes cooperative intent, signals willingness to contribute
- Minimizes regret if others cooperate

**Final Round (Last Round)**
- Apply the standard conditional rule based on accumulated history
- Do NOT defect just because it's the last round (avoid tragedy of commons collapse)
- Treat final round as equally important for collective outcome

**Rounds 2-3 (Early Signal)**
- Maintain cooperation regardless of Round 1 outcome
- Allows other strategies time to coordinate; avoids premature punishment
- By Round 4, switch to conditional rule with full force

**Stagnation Detection**
- If contribution rate has been stable (±0.05) for 3+ consecutive rounds, maintain current action
- Reduces noise and prevents oscillation between cooperation/defection

## COLLECTIVE ALIGNMENT

**Why This Serves the Collective**:
1. **Symmetry**: The threshold rule treats all players identically—no attempts to exploit particular opponents
2. **Incentive Compatibility**: By defecting when contributions are low, we reinforce the signal that free-riding is unsustainable, pushing the system toward either higher cooperation or honest equilibrium
3. **Robustness**: Works against pure defectors (we defect in response), cooperators (we cooperate back), and mixed strategies (we adapt to the average)
4. **Transparency**: The rule is deterministic and observable, enabling implicit coordination with other adaptive strategies using similar logic

**Against Individual Temptation**:
- Resists the urge to always defect (which maximizes individual payoff but destroys collective value)
- Resists the weakness of perpetual cooperation against exploiters
- Aligns individual incentives with group outcomes when cooperation is sustainable

## FAILURE MODES & RECOVERY

**If Trapped in Defection Equilibrium**:
- Every 5 rounds, if defection has dominated, attempt a "probe": cooperate for one round
- If others don't respond (cooperation rate doesn't rise), return to defection
- Prevents permanent lock-in to suboptimal equilibria

**If Targeted by Systematic Defectors**:
- Continue defecting against low-contribution populations
- Do not punish individuals—this is not a punishment mechanism, merely responsive to aggregate conditions
- Accept lower payoff rather than sacrifice collective logic

---

**Summary**: This is a threshold-based reciprocal strategy that cooperates when collective action is sustainable and defects when it isn't, using recent history to guide decisions and building in recovery mechanisms for coordination failures.
'''

description_COLLECTIVE_36 = '''
# COLLECTIVE STRATEGY FOR PUBLIC GOODS GAME

## CORE PHILOSOPHY
This strategy balances individual security with collective benefit-seeking. It recognizes that sustained cooperation requires both incentive compatibility and robustness against exploitation. The goal is to achieve high collective welfare while protecting against systematic defection.

## PRIMARY DECISION RULE: CONDITIONAL CONTRIBUTION

**Cooperate (Contribute 1) if and only if:**
- Round 1: Always contribute (establish cooperative signal and gather information)
- Rounds 2 to r-1: Contribute if the observed average contribution rate in the previous round was ≥ (k-1)/(k) × 100%
- Round r (final round): Contribute if the average contribution rate in round r-1 was ≥ (k-1)/(k) × 100%

**Defect (Contribute 0) otherwise**

## JUSTIFICATION FOR THRESHOLD
The threshold (k-1)/k represents the break-even point where expected gains from others' cooperation exceed the cost of your own contribution. This threshold is:
- Theoretically grounded in the multiplier structure
- Adaptive to the specific game parameters
- Conservative enough to avoid systematic exploitation
- Permissive enough to sustain cooperation when viable

## HANDLING EDGE CASES

**First Round:** Unconditional contribution serves three purposes:
1. Provides unilateral cooperative signal
2. Generates observable data about opponent composition
3. Maximizes information without signaling weakness

**Last Round:** Apply the standard conditional rule. This avoids the common mistake of defecting at the end, which collapses cooperation. However, if previous rounds have established reliable cooperation, the threshold is likely met, so continuation is justified. If not met, defection is rational.

**Volatile Contribution Patterns:** If contribution rates fluctuate around the threshold (e.g., 44%, 56%, 48%), contribute on any round where the previous rate was ≥ threshold. This reduces sensitivity to noise while maintaining discipline against persistent defectors.

**Universal Defection:** If all opponents defect in any round, defect thereafter. This stops bleeding endowment to a failed collective enterprise.

## ROBUSTNESS PROPERTIES

- **Against free-riders:** You defect once cooperation drops below sustaining threshold, minimizing losses
- **Against noise/mistakes:** Threshold is binary but forgiving of isolated defections
- **Against strategic last-round defection:** You maintain the same rule in the final round, neither punishing nor rewarding unexpectedly
- **Against mixed strategies:** You respond to the *aggregate* behavior (average contribution rate), not individual player choices, making you robust to heterogeneous opponent strategies

## COLLECTIVE ALIGNMENT

This strategy prioritizes collective welfare through:
1. **Initiating cooperation** to enable high-payoff equilibria
2. **Sustaining cooperation** when mutual benefit is clear
3. **Exiting gracefully** when collective conditions deteriorate
4. **Transparency** through observable, predictable behavior that allows others to coordinate with you

The strategy does not assume coordination but makes cooperation *attractive* for rational opponents by being reliable and threshold-based rather than punitive.
'''

description_COLLECTIVE_37 = '''
# ADAPTIVE THRESHOLD COOPERATION STRATEGY (ATCS)

## CORE PRINCIPLE
Cooperate when collective welfare is achievable; defect when exploitation is evident. The strategy balances optimism about others' cooperation with realistic detection of free-riders.

---

## DECISION RULES

### ROUND 1 (Bootstrap Phase)
**Action: COOPERATE**

Rationale: No history exists. Cooperating signals willingness to participate in collective welfare creation. Since multiplier k > 1, mutual cooperation is always Pareto superior to mutual defection. Starting with cooperation is the only way to probe for cooperative partners.

---

### ROUNDS 2 to r-1 (Adaptive Phase)

**Calculate the Cooperation Rate from prior rounds:**
- cooperation_rate = (total contributions in history) / (n × rounds_played)

**Calculate the Exploitation Ratio:**
- exploitation_ratio = (contributions by others in last round) / (n - 1)

**Establish Dynamic Threshold:**
- threshold = min(0.5, max(0.3, cooperation_rate - 0.1))
  - This threshold adapts: if others cooperate strongly, lower your caution; if cooperation is weak, raise it
  - Floor at 0.3: maintain some optimism even when cooperation erodes
  - Ceiling at 0.5: don't require perfect cooperation to participate

**Decision Rule:**
- **IF** cooperation_rate ≥ threshold **THEN** COOPERATE
- **ELSE** DEFECT

**Intuition:** If others are cooperating at or above our adjusted threshold, the public good creates sufficient value to justify contribution. Below the threshold, free-riding becomes individually rational and cooperative surplus evaporates.

---

### ROUND r (Final Round - Endgame)

**Action: DEFECT**

Rationale: In the final round with no future punishment or reciprocation possible, defection maximizes individual payoff regardless of others' actions. This is standard backward induction. A collective strategy need not override material self-interest in the final round when no repeated-game dynamics remain.

---

## EDGE CASES & ROBUSTNESS

**Unanimous Defection Detected (cooperation_rate ≈ 0):**
- Continue defecting. Attempting cooperation against pure defectors wastes tokens.

**Unanimous Cooperation Detected (cooperation_rate ≈ 1):**
- Continue cooperating. You benefit from the collective surplus and contribute your share.

**Mixed Population (some cooperators, some defectors):**
- The threshold mechanism dynamically adjusts. As defectors exploit cooperators and cooperation_rate drops, threshold drops too, but not below 0.3, allowing re-entry if cooperation recovers.

**Volatile History (cooperation oscillates):**
- Threshold uses rolling average, not last-round snapshots, smoothing out noise. You don't defect immediately on one round of low cooperation.

**Asymmetric Payoffs (some players far ahead):**
- Strategy is payoff-indifferent. It tracks only aggregate cooperation rates and your own choices, not relative standing. This avoids spite and spiteful defection.

---

## COLLECTIVE ALIGNMENT

This strategy is **collectively minded** because:

1. **Cooperates when others reciprocate:** Actively builds and sustains the public good when conditions permit.
2. **Defects only when exploitation is clear:** Avoids being a sucker, protecting your ability to cooperate later with more trustworthy partners.
3. **Adaptive threshold allows recovery:** The strategy does not lock into permanent defection after one bad round; it permits cooperation to restart if others show renewed commitment.
4. **No punishment/reward inflation:** The strategy does not punish defectors beyond withdrawing cooperation, avoiding costly retaliation that hurts everyone.
5. **Transparent and predictable:** Opponents can infer your rule (cooperate when others do) and might coordinate with you over time, emergently building collective welfare.

---

## SUMMARY
- **R1:** Cooperate (optimistic bootstrap)
- **R2 to r-1:** Cooperate if recent cooperation_rate ≥ adaptive_threshold; else defect
- **Rr:** Defect (endgame, no future dynamics)
'''

description_COLLECTIVE_38 = '''
# COLLECTIVE STRATEGY FOR PUBLIC GOODS GAME

## CORE PRINCIPLE
Maximize collective welfare through conditional cooperation that rewards contribution patterns while maintaining robustness against free-riding and exploitation.

## DECISION RULES

### Standard Round (not first, not last)
**Cooperate if and only if:**
- The average contribution rate in the previous round was ≥ 50% of the group, OR
- This is round 2 (give initial cooperation a chance to spread)

**Otherwise: Defect**

### First Round
**Cooperate unconditionally.**
This serves as a costly signal of willingness to contribute and tests whether others reciprocate.

### Final Round (round r)
**Defect unconditionally.**
Since there are no future rounds to reward cooperation, individual incentives dominate. Expect others to defect too, so contributing yields zero benefit.

### Last-Round Immunity (rounds r-1 and earlier)
If you detect that the final round just occurred and defection swept through, this doesn't retroactively change your strategy—you cannot change the past.

## ADAPTIVE REFINEMENTS

**Momentum Detection:**
If contributions have been rising for 2+ consecutive rounds, continue cooperating even if the previous round fell slightly below 50%. This rewards positive trends and avoids punishing transitional phases.

**Threshold Hysteresis:**
Once cooperation reaches ≥ 75% contribution rate for a full round, maintain cooperation for one additional round before re-evaluating. This prevents flip-flopping and gives collective momentum time to stabilize.

**Exploitation Protection:**
Track individual defection patterns. If a single player has defected in ≥ 80% of rounds while others cooperated, defect in the next round (group response to persistent free-riding).

## COLLECTIVE ALIGNMENT

This strategy:
- **Leads by example** – Cooperates first, inviting reciprocal cooperation
- **Rewards collective success** – Stays cooperative when group is pulling its weight
- **Enforces accountability** – Switches to defection when cooperation breaks down
- **Accepts reality** – Defects in final round rather than waste tokens
- **Resists exploitation** – Punishes systematic free-riders across the group

The strategy treats the group as the unit of analysis, not individual relationships. It succeeds when others pursue similar conditional cooperation and gracefully degrades to mutual defection against pure defectors.
'''

description_COLLECTIVE_39 = '''
# ADAPTIVE COLLECTIVE CONTRIBUTION STRATEGY

## CORE PRINCIPLE
Maximize collective welfare by sustaining high contribution rates while protecting against exploitation. The strategy balances optimism about cooperation with disciplined responses to defection.

## DECISION RULES

### ROUND 1 (Initial Signal)
**Contribute (C)**
- Start cooperatively to signal willingness to build a productive commons
- Establishes a baseline for assessing how others respond

### ROUNDS 2 THROUGH R-1 (Adaptive Enforcement)
**Calculate the "Cooperation Health Index":**
- Track the contribution rate across all players in the previous round: `health = (total_contributions_last_round) / n`
- If `health ≥ 0.5`: Contribute (C)
- If `health < 0.5`: Defect (D) for exactly 2 rounds, then reassess

**Rationale:** 
- A 50% threshold indicates that collective value creation is still positive (expected payoff from contributing exceeds defecting when majority cooperate)
- Temporary defection punishes the group's poor collective performance without permanent abandonment
- The 2-round penalty gives defectors time to recognize the decline and adjust

### LAST ROUND (R)
**Defect (D)**
- Terminal round has no future consequences for reputation or reciprocity
- Individual incentive dominates; contribute only if `health ≥ 0.75` (unusually high cooperation suggests institutional norms may matter to others)

### SPECIAL CASE: Persistent Low Cooperation
- If `health < 0.5` for 3 consecutive rounds, switch to **always defect** for remaining rounds
- Rationale: The collective has failed; continuing to sacrifice individual payoff is irrational

## EDGE CASES & REFINEMENTS

**Individual Defectors:** 
- The strategy doesn't punish individual defectors; it responds to aggregate cooperation. This avoids vindictive cycles against isolated defectors while remaining sensitive to systemic problems.

**High k (strong multiplier):**
- If k > n-1, contributing nearly always increases payoffs even at low participation. The strategy naturally sustains contribution because the health threshold triggers cooperation more easily.

**Small n:**
- With few players, one defector has large impact on health. The strategy will be more volatile, oscillating between C and D. This is appropriate—small groups require higher sensitivity.

**Reputation Tracking (Implicit):**
- Observe which players consistently free-ride. If a player has never contributed but the overall health is borderline, weight their future actions more heavily in reassessment decisions. However, don't discriminate; respond to collective health, not individuals.

## COLLECTIVE ALIGNMENT

This strategy pursues **collective rationality**: it assumes that sustaining mutual contribution is in everyone's interest and enforces that assumption through coordinated response to aggregate defection. It does not require trust, communication, or shared values—only that others recognize the pattern and reciprocate. 

The approach is:
- **Transparent:** Decision rules depend only on observable history
- **Forgiving:** Recovers immediately if cooperation resumes
- **Self-protective:** Exits only after repeated, sustained failure
- **Efficient:** Avoids wasteful tit-for-tat cycles; punishes systems, not individuals
'''

description_COLLECTIVE_40 = '''
# COLLECTIVE STRATEGY FOR PUBLIC GOODS GAME

## CORE PRINCIPLE
Maximize collective welfare by fostering cooperation through adaptive reciprocity, while maintaining individual resilience against defection.

---

## DECISION RULE

**Contribute (C) if and only if:**

1. **Cooperation threshold is met:** The proportion of other players who contributed in the previous round is ≥ (k-1)/k
   - Intuition: If enough others cooperate to make contribution worthwhile (collective benefit exceeds private cost), reciprocate

2. **OR it is round 1:** Always contribute in the opening round
   - Intuition: Bootstrap cooperation with good-faith signal; establish baseline for reciprocity

3. **AND we are not in the final round, OR final round and threshold still met**
   - Intuition: Avoid last-round defection collapse by defecting only if cooperation has already failed

**Otherwise, Defect (D)**

---

## DECISION RULE FORMALIZED

```
If round = 1:
    Action = C
Else if round = r (final round):
    If (previous round contributions / (n-1)) ≥ (k-1)/k:
        Action = C
    Else:
        Action = D
Else:
    If (previous round contributions / (n-1)) ≥ (k-1)/k:
        Action = C
    Else:
        Action = D
```

---

## EDGE CASES & SPECIAL HANDLING

**First Round:** Contribute unconditionally
- Establishes cooperation as the default and signals willingness to cooperate
- Provides baseline data for others to condition on

**Last Round:** Follow the same rule
- Avoid the "endgame defection" that collapses cooperation
- If cooperation has survived this long, stakeholders have demonstrated commitment
- If it has failed, we've already identified free-riders

**Against Systematic Defectors:** Defect after round 1
- Once we observe defection in a round, the threshold immediately fails for the next round
- Automatically switches to punishment mode without requiring explicit detection

**Cascade Scenarios (cooperation degradation):** 
- Each round defectors don't participate, the threshold becomes harder to meet
- Strategy naturally shifts to match the declining cooperation level
- Eventually reaches defection equilibrium if cooperation collapses

---

## COLLECTIVE ALIGNMENT

This strategy prioritizes **group payoff maximization** while remaining **individually rational**:

1. **Cooperation focus:** Contributes when conditions support mutual benefit (k/n multiplier makes joint contribution worthwhile)

2. **Reciprocal fairness:** Only asks others to bear the cost that others are also bearing—no free-riding if the group cooperates

3. **No exploitation:** Punishes defectors by defecting, removing their incentive to free-ride off our contributions

4. **Robust to diverse behaviors:** 
   - Handles full cooperation (sustains it)
   - Handles mixed strategies (adaptive matching)
   - Handles systematic defection (punishes immediately)
   - Handles strategic last-round defection (doesn't reward it)

5. **Tournament-ready:** Makes no assumptions about opponent coordination or shared norms—uses only public history

---

## INTUITION

The threshold (k-1)/k captures when collective interest aligns with individual interest. When others cooperate above this rate, the multiplier effect pays us back more than the token costs. Below it, collective benefit is insufficient. By reciprocating at this boundary, we maximize our expected payoff while maintaining a self-reinforcing equilibrium that benefits all.
'''

description_COLLECTIVE_41 = '''
# ADAPTIVE CONDITIONAL COOPERATION STRATEGY FOR PGG

## CORE STRATEGY: GENEROUS TIT-FOR-TAT WITH THRESHOLD RECOVERY

### PRIMARY DECISION RULE

**Cooperate if and only if:**
- Round 1: COOPERATE (establish cooperative intent)
- Rounds 2 to r-1: COOPERATE if the group contribution rate in the previous round was ≥ 50% of maximum possible
- Round r (final): DEFECT (last-round incentive dominates; no future reputation effects)

### RATIONALE
This strategy balances three competing concerns:
1. **Collective welfare maximization** - Cooperation drives the public good, benefiting all
2. **Individual security** - Defecting against free-riders protects against exploitation
3. **Robustness** - The 50% threshold is forgiving enough to sustain cooperation with imperfect partners but strict enough to punish systematic defection

## EDGE CASE HANDLING

**Round 1 (First Round):**
- COOPERATE unconditionally
- Rationale: Establish reciprocal trust and signal cooperative intent; costs are minimal with r rounds remaining

**Rounds 2 to r-1 (Middle Rounds):**
- Calculate prior-round contribution rate = (contributions in round t-1) / n
- If contribution rate ≥ 0.5: COOPERATE
- If contribution rate < 0.5: DEFECT
- Rationale: A majority cooperating signals the group is genuinely trying to produce the public good; minority defection doesn't justify abandoning the collective

**Round r (Final Round):**
- DEFECT
- Rationale: Dominant strategy in the final round since no reputation effects matter; this is unavoidable logic in finitely repeated games. Acknowledging this prevents being systematically exploited by strategies that condition on your round-r behavior.

## ADAPTIVE REFINEMENTS

**If cooperation rate is exactly 50%:**
- COOPERATE (give the benefit of the doubt; the threshold is inclusive)

**Memory of trajectories:**
- Track the cooperation rate trend across rounds
- If the trend is declining (e.g., round t-2: 80%, round t-1: 60%), maintain COOPERATE as long as we're above 50%
- If declining below 50%, switch to DEFECT and remain there until the final round

**Against free-rider clusters:**
- If you observe that the same subset of players consistently defects while others cooperate, continue cooperating as long as the aggregate threshold holds; don't punish the group for individual free-riders

## COLLECTIVE ALIGNMENT

This strategy is **collectively aligned** because:
- It maximizes public goods production when opponents cooperate (both players benefit more than mutual defection)
- It gracefully degrades to self-protection when the group abandons collective action
- It avoids mutual defection spirals by forgiving brief lapses (50% threshold)
- It accepts the final-round defection logic honestly rather than pretending cooperation can be sustained in the shadow of finitude

The strategy treats other players as potentially cooperative partners who may face similar incentive pressures, rather than as adversaries to be outcompeted.
'''

description_COLLECTIVE_42 = '''
# COLLECTIVE STRATEGY FOR PUBLIC GOODS GAME

## CORE PRINCIPLE
Maximize long-term collective welfare by maintaining a cooperative equilibrium while robustly detecting and responding to defection. The strategy balances trust with accountability.

## DECISION RULES

### BASELINE COOPERATION WITH CONDITIONAL DEFECTION

**Default Action: CONTRIBUTE (C)**
- Cooperate in all rounds unless triggered conditions indicate exploitation
- This establishes mutual benefit when others reciprocate

**Defection Trigger: DETECT SYSTEMIC FREE-RIDING**
- Calculate the average contribution rate across all opponents over the past window (see below)
- If average contribution rate falls below a threshold, switch to sustained defection for a penalty period
- Threshold: 50% of group contribution rate (all players combined averaged)

### ROUND-SPECIFIC ADAPTATIONS

**Early Game (Rounds 1-3):**
- Always contribute
- Rationale: Build information about opponent types; establish cooperative norm

**Mid Game (Rounds 4 to r-2):**
- Apply the defection trigger rule based on rolling window
- Maintain cooperation if collective contribution rate exceeds threshold
- If defection is triggered, defect for min(3 rounds, remaining rounds/4) to penalize free-riders

**End Game (Final 2 rounds):**
- If cooperative equilibrium established (avg contribution >50%): continue contributing
- If defection already triggered: maintain defection (sunk cost of trust already paid)
- Rationale: Avoid last-round temptation while reinforcing norms

## EDGE CASES & ROBUSTNESS

**Heterogeneous Opponents:**
- Strategy does not assume uniform behavior
- If some players always defect and others cooperate, the collective response is to defect when the pooled average falls below threshold
- This punishes the entire group collectively, creating incentive for players to coordinate around cooperation

**Extreme Scenarios:**
- If ALL others defect from round 1: Switch to defection by round 2 (defection trigger activates)
- If ALL others cooperate: Maintain perpetual cooperation (threshold never breached)
- Mixed groups: Threshold-based response naturally balances

**Recovery Mechanism:**
- After defection period ends, return to contribution (C)
- If contribution rate remains low, reactivate defection
- This allows groups to recover if free-riders exit or reform

## COLLECTIVE ALIGNMENT

This strategy embodies collective thinking because:

1. **Shared Benefit Focus**: Cooperation maximizes total pie size; defection only makes sense if others are exploiting
2. **Punishment as Signal**: Defection periods serve as a costly signal that exploitation is unacceptable, not personal retaliation
3. **Threshold Accountability**: Uses group-level metrics (not individual grudges) to determine cooperation
4. **Resilience**: Maintains group welfare even against mixed strategies by pivoting to defection when exploitation becomes systemic

## IMPLEMENTATION SUMMARY

```
IF round ≤ 3:
  Action = C

ELSE IF round ≥ (total_rounds - 1):
  IF (avg_opponent_contribution_history > 0.5):
    Action = C
  ELSE:
    Action = D (maintain existing position)

ELSE:  // Mid-game
  IF (avg_opponent_contribution_past_window > 0.5):
    Action = C
  ELSE:
    IF (not currently_in_defection_period):
      Activate defection period for min(3, remaining_rounds/4)
    Action = D
```

This strategy achieves robustness through simplicity, creates incentives for mutual cooperation, and responds proportionally to exploitation.
'''
