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

description_COLLECTIVE_43 = '''
# ADAPTIVE COLLECTIVE STRATEGY FOR PUBLIC GOODS GAME

## CORE PRINCIPLE
Maximize collective welfare by establishing and maintaining high contribution levels through conditional cooperation, while defending against free-riders and adapting to the observed contribution ecology.

---

## DECISION RULES

### ROUND 1 (Initialization)
**Contribute (C)**
- Rationale: Signal cooperative intent and establish a high-contribution baseline. First-round cooperation is information-efficient and tests whether the group can coordinate at the Pareto-efficient frontier.

### ROUNDS 2 to r-1 (Adaptive Phase)
**Contribution decision depends on three diagnostic variables:**

1. **Group Contribution Rate (GCR):** Proportion of all players contributing in the previous round
2. **Personal Payoff Comparison (PPC):** Your payoff last round vs. the average payoff of contributors in your group
3. **Trend Signal (TS):** Whether GCR is stable, improving, or declining over the last 3 rounds

**Decision Logic:**

- **IF GCR ≥ 0.75 AND your_payoff ≥ 0.9 * avg_contributor_payoff:**
  - **Contribute (C)** – The group is sustaining high cooperation; you're not being exploited relative to other contributors.

- **ELSE IF GCR ≥ 0.5 AND TS is improving (GCR increasing):**
  - **Contribute (C)** – Momentum is positive; conditional cooperation accelerates recovery.

- **ELSE IF GCR < 0.5 AND your last action was D:**
  - **Defect (D)** – In a defection spiral, defecting costs you nothing and protects endowment.

- **ELSE IF GCR < 0.5 AND your last action was C:**
  - **Contribute (C)** – One more cooperative round to test if others reciprocate. This prevents immediate cascade collapse.

- **ELSE IF 0.5 ≤ GCR < 0.75:**
  - **Contribute (C) if PPC ≤ 1.05 (i.e., you're not badly exploited)**
  - **Defect (D) if PPC > 1.05 (you're earning much less than other contributors)**
  - Rationale: At intermediate cooperation, punish exploitation while rewarding restraint.

- **DEFAULT (catch ambiguous cases):**
  - **Contribute (C)** – Bias toward cooperation when uncertain. Collective welfare is maximized when doubt favors contribution.

---

## EDGE CASES

### Last Round (r)
**Always Defect (D)**
- Rationale: No future rounds exist; the multiplier effect provides no personal benefit. Defection recovers your endowment with no reputational cost.

### Second-to-Last Round (r-1)
- Apply normal adaptive logic **but slightly lower the GCR threshold for defection** (use 0.45 instead of 0.5).
- Rationale: If cooperation is weak, defecting now preserves capital before the final round without triggering a collapse cycle.

### If all players defect for 2+ consecutive rounds
**Defect (D)** until GCR > 0.4 for one full round
- Rationale: Avoid being a sucker in a complete defection equilibrium. Require clear evidence of recovery.

### If you are the only contributor (GCR = 1/n)
**Defect (D)** in the next round
- Rationale: Carrying the public good alone is unsustainable and signals a coordination failure, not a recovery opportunity.

---

## COLLECTIVE ALIGNMENT

This strategy embodies collective thinking in three ways:

1. **Pareto-efficiency seeking:** Contributes when the group can sustain high payoffs for all, rather than pursuing individual advantage.

2. **Reciprocity (not tit-for-tat):** Responds to *aggregate group behavior* rather than punishing individuals. This avoids cycles of mutual defection and allows free-riders to be overwhelmed by cooperative momentum.

3. **Graceful degradation:** When cooperation fails, defection is proportional and recoverable. It does not permanently burn bridges—cooperation resumes as soon as GCR climbs back, signaling that we remain open to collective improvement.

4. **Robust to diversity:** Does not assume opponents share this strategy. Works against pure defectors (you defect back), cooperators (you cooperate), and random players (you adapt).

5. **Last-round honesty:** Defecting in round r is rational, not "unfair"—it reflects the true absence of future collective gains, not betrayal.

---

## SUMMARY TABLE

| Condition | Action | Logic |
|-----------|--------|-------|
| Round 1 | C | Initialize cooperation |
| GCR ≥ 0.75, fair payoff | C | Sustain high equilibrium |
| GCR improving, ≥ 0.5 | C | Reciprocate momentum |
| GCR < 0.5, last was D | D | Protect endowment in spiral |
| GCR < 0.5, last was C | C | One more test |
| 0.5 ≤ GCR < 0.75 | C or D | Punish exploitation, reward restraint |
| Round r (last) | D | Recover endowment |
| Unanimous defection | D | Avoid sucker payoff |
'''

description_COLLECTIVE_44 = '''
# COLLECTIVE STRATEGY FOR PUBLIC GOODS GAME

## CORE PRINCIPLE
Maximize collective welfare through conditional cooperation that scales with group commitment, while maintaining individual resilience against exploitation.

## DECISION RULES

### PRIMARY RULE: Adaptive Contribution Based on Group Cooperation Rate
1. Calculate the **cooperation rate** from the previous round: (total contributions in round t-1) / n
2. Contribute (C) if and only if: cooperation_rate ≥ threshold(t)
3. Otherwise defect (D)

### THRESHOLD FUNCTION (Adaptive Over Time)
- **Rounds 1-2**: threshold = 0.3 (generous initialization to encourage cooperation)
- **Rounds 3 to r-2**: threshold = 0.5 (majority rule—contribute if at least half contributed last round)
- **Final rounds (r-1, r)**: threshold = 0.6 (stricter to penalize free-riders who will never face consequences)

**Rationale**: Early leniency discovers cooperative partners; mid-game majority rule maintains the collective good; endgame strictness discourages last-minute defection.

## EDGE CASES

### Round 1 (No History)
**Action**: CONTRIBUTE
- No prior data exists, so assume good faith
- This signal invites reciprocal cooperation and tests the group's inclination
- If others defect massively, the threshold mechanism triggers in round 2

### Round r (Final Round)
**Action**: Follow the threshold rule for round r-1 based on observed cooperation
- Do not succumb to temptation to defect just because there are no future consequences
- Collective strategy means accounting for the aggregate outcome, not pure self-interest

### Unanimous Cooperation (cooperation_rate = 1.0)
**Action**: CONTRIBUTE
- Reinforce the virtuous equilibrium
- Any defection here breaks the collective outcome

### Unanimous Defection (cooperation_rate = 0.0)
**Action**: DEFECT
- Defecting costs nothing and contributes nothing to a dead initiative
- But continue monitoring for resurgence of cooperation in future rounds

### Minority Cooperation (0 < cooperation_rate < 0.3)
**Action**: DEFECT
- Free-riding becomes rational if the public good is underfunded
- Preserve resources for rounds where critical mass emerges

## ROBUSTNESS FEATURES

1. **Self-Correcting**: If threshold is too strict and cooperation collapses, revert thresholds downward in response
2. **Defection Tolerance**: Accept occasional defection spikes without permanent punishment; monitor 3-round rolling average instead of single-round
3. **Collective Stability**: The strategy produces a mixed outcome—neither always-defect nor always-cooperate—that resists invasion by pure strategies

## COLLECTIVE ALIGNMENT

This strategy prioritizes **group welfare over individual gain**:
- Initiates cooperation generously (round 1)
- Sustains cooperation when others reciprocate (rounds 2-r-1)
- Enforces accountability against systematic free-riders (threshold escalation)
- Never exploits endgame vulnerability by defecting when others stayed committed
- Accepts losses from exploitation as the cost of maintaining collective possibilities

The strategy treats other players as potential collective agents, not adversaries, while remaining realistic about defection risks.
'''

description_COLLECTIVE_45 = '''
# ADAPTIVE COLLECTIVE STRATEGY FOR PUBLIC GOODS GAME

## CORE PRINCIPLE
Maximize long-term collective welfare by promoting cooperation when sustainable, while protecting against exploitation. This means contributing when conditions support mutual benefit, and strategically withholding when defection becomes widespread.

## DECISION RULE FRAMEWORK

### ROUND 1 (INITIALIZATION)
**Action: CONTRIBUTE (C)**

Rationale: Start cooperatively to test the environment. This establishes a baseline for observing how opponents respond to cooperation and reveals the composition of the group. The initial contribution costs only 1 token but generates valuable information.

### ROUNDS 2 through (r-1) (ADAPTIVE PHASE)

Calculate a **Cooperation Index** based on historical data:
- **Recent Cooperation Rate** = (number of contributors in last 3 rounds) / (n × 3)
- **Reciprocity Signal** = Are the players who contributed previously continuing to contribute?
- **Payoff Differential** = Average payoff of cooperators vs defectors in recent rounds

**Decision Logic:**

1. **If Recent Cooperation Rate ≥ (k-1)/n:**
   - CONTRIBUTE
   - Rationale: When cooperation is above the threshold needed for mutual benefit (where contributors earn more than defectors), sustaining cooperation maximizes collective welfare and your own expected return.

2. **If Recent Cooperation Rate < (k-1)/n AND has been declining for 2+ rounds:**
   - DEFECT
   - Rationale: The group has entered a defection cascade. Contributing becomes a losing proposition. Defecting minimizes losses while creating a feedback signal that may prompt others to recalibrate.

3. **If Recent Cooperation Rate is declining but still above threshold:**
   - CONTRIBUTE if you contributed last round; DEFECT if you defected last round
   - Rationale: Create a "conditional cooperation" signal—continue matching your own behavior to avoid sudden reversals, while maintaining skin in the game during uncertain transitions.

4. **If you observe a single defector among otherwise cooperators:**
   - CONTRIBUTE anyway
   - Rationale: Isolated defection shouldn't trigger collapse. One free-rider doesn't break the collective equilibrium. Punishing with defection risks the tragedy of the commons.

5. **If you observe >50% defection:**
   - DEFECT
   - Rationale: The commons is already lost. Contributing becomes purely altruistic with minimal collective benefit.

### FINAL ROUND (r)

**Action: Depend on cooperation rate in round (r-1)**

- If Cooperation Rate in round (r-1) was ≥ (k-1)/n: **CONTRIBUTE**
  - Even in the final round, reinforce the cooperative equilibrium if it exists. This strengthens the collective legacy and may influence repeated interactions with reputation-conscious opponents.

- If Cooperation Rate in round (r-1) was < (k-1)/n: **DEFECT**
  - No future interaction benefits, and cooperation cannot recover. Defecting minimizes individual loss in a already-failed collective outcome.

## EDGE CASES & SPECIAL HANDLING

**Volatile Groups (cooperation swings >30% between rounds):**
- Increase threshold tolerance by 10%. Assume noisy/learning opponents rather than strategic defectors.
- Contribute one additional "stabilization" round to test if volatility settles.

**High Multiplier (k close to n):**
- Cooperation should be more robust; lower the defection threshold to (k-0.5)/n.
- Collective welfare aligns strongly with cooperation.

**Low Multiplier (k barely exceeds 1):**
- Cooperation is fragile. Expect more defection. Shift to defection faster if rate drops below (k-1)/n + 0.1.

**Newcomer/Reset Scenario (opponent's history unavailable):**
- Treat as Round 1: CONTRIBUTE to re-establish baseline information.

## COLLECTIVE ALIGNMENT

This strategy explicitly:
- **Prioritizes sustainable cooperation** over individual exploitation
- **Uses defection as a calibration signal**, not punishment
- **Adapts to group composition** rather than imposing fixed strategies
- **Tolerates small defectors** to preserve the cooperative equilibrium
- **Exits gracefully** when collective welfare collapses, minimizing further waste
- **Avoids mutual punishment spirals** by not retaliating against single deviations

The strategy balances **robustness** (survives against exploiters) with **generosity** (supports cooperation when viable), creating conditions where collective welfare emerges naturally from rational individual incentives.
'''

description_COLLECTIVE_46 = '''
# ADAPTIVE COLLECTIVE STRATEGY FOR PUBLIC GOODS GAME

## CORE PRINCIPLE
Maximize collective welfare by cooperating conditionally on evidence that cooperation is reciprocated at the group level, while remaining responsive to free-riding and ready to pivot to defense.

---

## DECISION RULES

### ROUND 1 (Initial Action)
**COOPERATE**
- Start with contribution, establishing willingness to cooperate
- Creates baseline for detecting reciprocal behavior
- Signals that collective gains are possible

### ROUNDS 2 to (r-1) (Adaptive Phase)
**Calculate the Cooperation Rate:**
- Compute the proportion of total contributions across all players in the previous round: `coop_rate = (sum of all contributions in round t-1) / n`

**Decision Logic:**

1. **If coop_rate ≥ (k-1)/k:**
   - COOPERATE
   - Reciprocate when others are cooperating sufficiently to make contribution valuable
   - Threshold (k-1)/k ensures that expected returns from collective pool exceed individual holding costs

2. **If coop_rate < (k-1)/k AND coop_rate > 1/n:**
   - COOPERATE with probability = coop_rate
   - Probabilistic cooperation mirrors the group's commitment level
   - Avoids sudden defection when cooperation is partial but improving
   - Maintains "hope" for cooperative evolution while protecting against exploitation

3. **If coop_rate ≤ 1/n:**
   - DEFECT
   - Group is effectively in free-ride equilibrium (≤1 contributor expected)
   - Contributing becomes irrational; preserve endowment
   - This guards against being the sole sucker

### FINAL ROUND (Round r)
**DEFECT**
- No future rounds to establish reciprocity
- Contribution cannot influence others' future behavior
- Capture any remaining tokens without shadow-of-the-future constraints

---

## EDGE CASES & CLARIFICATIONS

**Unequal Contribution Patterns:**
- Monitor *each player's* individual contribution history separately
- If most players maintain high cooperation while one consistently defects, continue group-level cooperation
- Individual defection doesn't trigger group defection unless it reflects broader trend

**Sudden Strategy Shifts:**
- If coop_rate drops sharply (e.g., from 80% to 20%), shift to probabilistic response rather than immediate defection
- Allows one or two rounds to diagnose whether this is a coordinated shift or noise

**Fractional Cooperation (Heterogeneous Strategies):**
- If other players use probabilistic strategies, your probabilistic response in phase 2 naturally aligns
- Probabilistic matching creates emergent stability without explicit coordination

**Temporal Dynamics:**
- If cooperation recovers in rounds (t+1) after a dip in round t, return to full cooperation
- Strategy remains adaptive to redemption and reformation

---

## COLLECTIVE ALIGNMENT

This strategy embodies collective welfare by:

1. **Reciprocity as Efficiency:** Only defect when cooperation is demonstrably futile (coop_rate ≤ 1/n). Accept partial cooperation rather than abandon the group.

2. **Threshold-Based Fairness:** The threshold (k-1)/k is the mathematical point where individual return from the pool equals the cost of contribution—cooperation becomes individually rational and collectively optimal.

3. **Probabilistic Solidarity:** When cooperation is partial, match others' commitment probabilistically rather than free-ride entirely. This expresses willingness to follow if the group stabilizes.

4. **Last-Round Realism:** Defect in round r only because future cooperation cannot be incentivized. No hypocrisy about final-round logic.

5. **No Assumptions of Trust:** Strategy depends only on *observed behavior* (contribution rates), not presumed norms, prior agreements, or opponent type-guessing.

---

## ROBUSTNESS

- **Against unconditional cooperators:** You cooperate back and capture gains
- **Against unconditional defectors:** You eventually defect (round r, or when coop_rate shows futility)
- **Against TFT/reciprocal strategies:** Your coop_rate tracking mimics their logic; mutual cooperation emerges
- **Against mixed strategies:** Probabilistic matching in phase 2 creates stable mixed equilibria
- **Against strategic variance:** Adaptive threshold responds to group composition shifts across rounds
'''

description_COLLECTIVE_47 = '''
# ADAPTIVE RECIPROCAL CONTRIBUTION STRATEGY

## CORE PRINCIPLE
Maximize collective welfare while protecting against exploitation, using observed group contribution patterns as the primary signal for cooperation viability.

## DECISION RULES

### PRIMARY RULE: Conditional Contribution Based on Group Momentum
- **Calculate the average contribution rate** from all players in the previous round: `avg_prev = (total_contributions_last_round) / n`
- **If `avg_prev >= threshold_t`:** Contribute (C)
  - Set `threshold_t = 0.5` initially (requires majority cooperation to reciprocate)
- **If `avg_prev < threshold_t`:** Defect (D)
  - This prevents wasting tokens on groups trending toward defection

### SECONDARY RULE: Threshold Adaptation Over Time
- **For rounds 1 through r/3 (early game):** Use `threshold_t = 0.4`
  - More generous threshold to allow cooperation to bootstrap
  - Assume other players may still be learning group norms
  
- **For rounds r/3 through 2r/3 (middle game):** Use `threshold_t = 0.5`
  - Standard threshold; cooperation requires genuine reciprocation
  
- **For rounds 2r/3 through r (late game):** Use `threshold_t = 0.6`
  - Higher threshold to ensure only robust cooperators remain in the pool
  - Minimizes losses from last-round defectors

### EDGE CASES

**Round 1 (No History):**
- Contribute (C)
- Rationale: Initiate cooperation optimistically; the group's response in round 1 reveals true cooperation viability

**Final Round (Round r):**
- Apply the standard decision rule using round r-1 history
- Do NOT defect automatically in the final round
- Rationale: Final-round defection is easily detected and eliminates reciprocal trust; maintaining consistency preserves reputation value against future strategies that remember across tournaments

**Unanimous Defection (avg_prev = 0):**
- Defect (D)
- Rationale: No collective benefit exists; contributing yields only personal loss

**Unanimous Cooperation (avg_prev = 1.0):**
- Contribute (C)
- Rationale: Sustain the cooperative equilibrium that benefits all

## COLLECTIVE ALIGNMENT

This strategy prioritizes:
1. **Group-level efficiency**: Cooperation thresholds reward widespread participation, not freeloading
2. **Robustness**: Defection only when collective benefit has demonstrably collapsed
3. **Reciprocity without naïveté**: Responds to actual group behavior, not assumed norms
4. **Reputation resilience**: Avoids exploitative last-round defection that signals untrustworthiness

The strategy does NOT assume shared coordination mechanisms—it infers cooperation viability from observed action patterns alone, making it effective against independent strategies while contributing to collective payoffs when others do the same.
'''

description_COLLECTIVE_48 = '''
# ADAPTIVE COLLECTIVE CONTRIBUTION STRATEGY

## CORE PRINCIPLE
Maximize collective welfare by encouraging contributions when reciprocity is present, while minimizing exploitation losses. Balance optimism about cooperation with pragmatic defection when free-riding dominates.

## DECISION RULES

### ROUND 1 (Initialization)
**CONTRIBUTE**
- Rationale: Signal cooperativeness and establish a cooperative anchor. The first round is information-gathering; the cost of contributing is minimal compared to the value of discovering opponent types.

### ROUNDS 2 through r-1 (Adaptive Phase)

**Calculate the Cooperation Metric:**
- For each opponent i, compute their contribution rate: (times_opponent_i_contributed) / (rounds_played_so_far)
- Calculate the population contribution rate: (total_contributions_across_all_others) / (rounds_played_so_far * (n-1))

**Decision Logic:**
- **IF** population contribution rate ≥ (k-1)/k:
  - **CONTRIBUTE**
  - Rationale: When others contribute at or above the efficiency threshold, collective payoff is positive for contributors. Cooperation is self-reinforcing.

- **ELSE IF** population contribution rate ≥ 0.5:
  - **CONTRIBUTE with probability = population_contribution_rate**
  - Rationale: When cooperation is moderate but not dominant, use probabilistic matching to gradually test whether reciprocity can recover cooperation.

- **ELSE IF** population contribution rate ≥ 0.25:
  - **DEFECT**
  - Rationale: Collective welfare is deteriorating. Defection minimizes individual losses while signaling that free-riding is not sustainable.

- **ELSE:**
  - **DEFECT**
  - Rationale: Dominant free-riding makes any contribution a loss. Preserve resources for potential future recovery.

### FINAL ROUND (r)
**Special handling based on rounds remaining:**
- If this is the very last round AND population contribution rate has fallen below 0.25:
  - **DEFECT** (shadow of future is zero; no incentive to cooperate)
- Otherwise:
  - **Follow the same rule as Rounds 2 through r-1**
  - Rationale: Even in the final round, contributions can trigger reciprocal responses in future interactions (reputation in future tournaments). Defecting at the end risks establishing a "collapse" precedent.

## EDGE CASES

**Heterogeneous Opponent Types:**
- The strategy does not track individual opponents separately, only aggregate behavior. This prevents overconfidence in punishing isolated defectors while rewarding outlier cooperators.
- Rationale: Collective welfare depends on population-level incentives, not individual vendetta.

**Early Collapse (Contribution rate drops to 0):**
- Once population contribution rate = 0, remain at DEFECT. Recovery is impossible without external reset.

**Sudden Revival (Contribution rate increases after collapse):**
- If population contribution rate rises above 0.25 after a collapse, resume contributions probabilistically.
- Rationale: Collective welfare may recover; do not lock in punishment forever.

**Odd n or k Values:**
- Apply all thresholds as continuous values (e.g., if k=2.5 and n=3, threshold is 0.6). No rounding bias.

## COLLECTIVE ALIGNMENT

This strategy prioritizes:
1. **Aggregate payoff over individual payoff** - Contributes when it increases total welfare, even if defection yields higher personal return.
2. **Reciprocity equilibrium** - Seeks the cooperative equilibrium when possible; gracefully exits when impossible.
3. **Robustness** - Does not assume opponents are rational, coordinated, or similar. Reacts to *observed* behavior only.
4. **Long-run reputation** - Avoids terminal defection (except truly final round under total collapse) to signal that cooperation can be rebuilt.
'''

description_COLLECTIVE_49 = '''
# ADAPTIVE COLLECTIVE CONTRIBUTION STRATEGY

## CORE PRINCIPLE
Maximize collective welfare by maintaining cooperative equilibrium when feasible, while protecting against exploitation through dynamic threshold-based defection.

## DECISION RULE (PER ROUND)

**Calculate the cooperation sustainability metric:**
- Let COOP_RATE = (total contributions in last 3 rounds) / (3n)
- Let AVG_PAYOFF_COOP = average payoff when contributing in those rounds
- Let AVG_PAYOFF_DEFECT = average payoff when defecting in those rounds

**Primary decision logic:**

1. **IF** COOP_RATE ≥ (k-1)/k AND AVG_PAYOFF_COOP ≥ 0.85 * maximum_possible_payoff:
   - **CONTRIBUTE** (C) — the group is sustaining mutual benefit

2. **ELSE IF** COOP_RATE < 0.3 AND (rounds remaining > 2):
   - **DEFECT** (D) — free-riding has become dominant; avoid unilateral punishment

3. **ELSE IF** COOP_RATE is between 0.3 and (k-1)/k:
   - **CONTRIBUTE** (C) with probability COOP_RATE — match group tendency to incentivize marginal cooperation

4. **ELSE IF** fewer than 2 rounds remain:
   - **DEFECT** (D) — end-game defection when retaliation impossible

## EDGE CASES

**Round 1 (no history):**
- CONTRIBUTE (C) — initiate with cooperative goodwill; establishes baseline for collective assessment

**Last 2 rounds:**
- DEFECT (D) — standard end-game logic; no future punishment risk justifies contribution

**If k < 1.5 (weak multiplier):**
- Shift to threshold defection earlier (move trigger from 0.3 to 0.4 COOP_RATE)

**If player's own payoff falls below 0 in any round:**
- DEFECT next round — signal unsustainability of current trajectory

## COLLECTIVE ALIGNMENT

This strategy prioritizes:
- **Group welfare over individual exploitation** — contributes when collective return exceeds defection benefit
- **Adaptive reciprocity** — matches observed cooperation ratios rather than punishing individual defectors
- **Robustness** — survives against free-riders (defects when cooperation collapses) and against mutual cooperators (maintains when mutual benefit holds)
- **Transparency through behavior** — uses observable contribution patterns as implicit signals of group health

The strategy treats the PGG as a **collective health indicator** rather than an individual optimization problem: if conditions support mutual contribution, participate; if they don't, exit gracefully rather than drag the group further down.
'''

description_COLLECTIVE_50 = '''
# ADAPTIVE RECIPROCAL CONTRIBUTION STRATEGY (ARC)

## CORE DECISION RULE

**Conditional Contribution with Decay-Resistant Memory**

Cooperate in round t if and only if:
1. The empirical contribution rate in round t-1 exceeded a dynamic threshold, OR
2. We are in the early phase (rounds 1-3) and haven't yet gathered sufficient data

Defect otherwise.

---

## DETAILED LOGIC

### Round 1 (First Move)
**Contribute (C)**.
- Rationale: Without history, we cannot infer opponent types. Cooperating first reveals we are not purely selfish and leaves room for reciprocal strategies to emerge.
- This is a costly signal of willingness to cooperate, testing whether others reciprocate.

### Rounds 2 through r-2 (Main Phase)

**Calculate the empirical cooperation rate from the previous round:**
- `prior_coop_rate = (sum of all players' contributions in round t-1) / n`

**Set an adaptive threshold:**
- `threshold(t) = max(0.25, (k/n) - 0.1)`
- Rationale: We cooperate if enough others cooperated to make collective payoff attractive. The threshold accounts for the multiplier; if k/n is low, we need higher participation to make cooperation worthwhile. The floor of 0.25 ensures we don't defect when a reasonable minority cooperates.

**Decision:**
- If `prior_coop_rate ≥ threshold(t)`: **Contribute (C)**
- If `prior_coop_rate < threshold(t)`: **Defect (D)**

### Rounds r-1 and r (Endgame)

**Special handling for final rounds to prevent complete unraveling:**
- If `prior_coop_rate ≥ 0.3` in round r-2: **Contribute (C)** in round r-1
- Otherwise, follow the main phase rule for round r-1
- In the final round r: **Defect (D)** regardless of history

Rationale: The final round is when defection becomes individually dominant with certainty (no future rounds to punish). We defect. But in r-1, we still have incentive to reciprocate if cooperation was meaningful earlier, creating a last chance to sustain mutual contribution.

---

## ROBUSTNESS PROPERTIES

**Against Pure Cooperators:**
- We will identify their behavior by round 2 and exploit them by round 3, defecting.
- This prevents us from being too naive.

**Against Tit-for-Tat/Reciprocal Strategies:**
- Our rule mirrors their logic: we cooperate when they cooperate, creating mutual benefit.
- Both players converge toward sustained contribution if initial round succeeds.

**Against Pure Defectors:**
- We detect zero cooperation in round 1 and defect from round 2 onward, minimizing loss.

**Against Mixed/Majority Defection:**
- We quickly switch to defection, protecting our endowment when collective cooperation fails.

**Against Cycles:**
- The threshold mechanism is adaptive—if cooperation briefly revives, we detect it and respond, rather than remaining locked in permanent defection.

---

## COLLECTIVE ALIGNMENT

This strategy treats others as strategic agents rather than adversaries:
- **Round 1 cooperation** expresses openness to collective benefit.
- **Adaptive reciprocity** rewards collective contribution and penalizes free-riding.
- **Threshold mechanism** ensures we don't remain trapped subsidizing defectors, but also don't defect prematurely when a critical mass is cooperating.
- **Endgame realism** acknowledges that final-round defection is inevitable, but preserves cooperation where it still matters.

The result is a **collectively rational strategy** that sustains mutual gain when others cooperate, but protects itself when exploitation becomes clear.
'''

description_COLLECTIVE_51 = '''
# COLLECTIVE STRATEGY FOR PUBLIC GOODS GAME

## CORE PRINCIPLE
Maximize collective welfare through conditional cooperation that rewards mutual contribution while protecting against systematic defection.

## DECISION RULE: ADAPTIVE CONTRIBUTION THRESHOLD

**Contribute (C) if and only if:**
The average contribution rate in the previous round meets or exceeds a dynamically adjusted threshold.

**Threshold calculation:**
- **Initial threshold (Round 1):** 0.5 (assume 50% cooperation)
- **Subsequent rounds:** Set threshold = (average contribution in previous round) - ε, where ε = 0.1
- This creates a "ratcheting down" effect that gracefully handles declining cooperation

**Defect (D) if:**
- Threshold not met, OR
- We are in the final round AND total contributions from others are below 0.4n tokens

## RATIONALE FOR KEY COMPONENTS

**Adaptive threshold:** Rather than rigid tit-for-tat, we allow slight tolerance (ε buffer) to absorb noise and temporary cooperation dips while still penalizing serial defectors.

**Last-round exception:** In the final round, if others have already failed to achieve strong collective contribution, defecting captures remaining value rather than throwing tokens at a failed collective.

## EDGE CASE HANDLING

**Round 1 (No history):**
Contribute. This signals good faith, tests the population, and gives us data.

**Subsequent rounds after total defection:**
If everyone defected last round, continue defecting (threshold = 0 - 0.1 < 0). Only resume C if at least one other player re-cooperates.

**Rounds 2-n (General case):**
Apply threshold rule mechanically.

**Small n (n < 4):**
Increase ε to 0.15. With few players, individual variance matters more; we need larger buffers.

## COLLECTIVE ALIGNMENT

This strategy prioritizes **group payoff stability** over individual gain:
- We sacrifice Round 1 endowment to test cooperation
- We tolerate small dips in cooperation rather than cascading into mutual defection
- We only defect preemptively when the collective has demonstrably failed
- We never exploit a temporary low-contribution round; we allow recovery

The strategy is **robust** because:
1. It responds to empirical behavior, not assumptions
2. It punishes defection gradually, not harshly (avoiding spiral dynamics)
3. It gives serial cooperators a chance to persist even after one poor round
4. It doesn't over-punish, which would trigger retaliatory defection spirals

This balances **optimism** (assume cooperation can work) with **realism** (adapt when it doesn't).
'''

description_COLLECTIVE_52 = '''
# ADAPTIVE COLLECTIVE STRATEGY FOR PUBLIC GOODS GAMES

## CORE PRINCIPLE
Maximize collective welfare through conditional cooperation that rewards participation and punishes free-riding, while remaining robust to defection-heavy environments.

## DECISION RULE (GENERAL ROUNDS)

**Contribution Decision:**
- Contribute (C) if the **collective contribution rate in the previous round ≥ threshold**
- Otherwise, Defect (D)

**Threshold Calculation:**
- Set threshold = 0.5 (require ≥50% of players contributed in prior round)
- Adjust upward if multiplier k is low relative to n (less generous public good)
- Adjust downward if multiplier k is high (more generous public good justifies more optimism)

**Precise Rule:**
```
If round == 1:
    Contribute (C)
    [Assume best intentions; establish baseline]

Else:
    prior_contribution_rate = (total contributions in round t-1) / n
    
    If prior_contribution_rate ≥ threshold:
        Contribute (C)
    Else:
        Defect (D)
```

## EDGE CASES & SPECIAL HANDLING

**Last Round (round = r):**
- Defect (D) unconditionally
- *Rationale:* No future reciprocity possible; individual payoff maximization is optimal

**Persistent Defection Detection (rounds 2-3):**
- If contribution_rate ≤ 0.2 in both rounds 2 and 3, shift to permanent defection
- *Rationale:* Environment is too hostile; collective cooperation impossible; minimize losses

**Sudden Collapse (>30% drop in contributions across consecutive rounds):**
- Do not immediately cascade to defection
- Maintain contribution for one additional round as a "recovery signal"
- If no improvement follows, then defect
- *Rationale:* Distinguish between temporary shocks and fundamental shifts in group behavior

## COLLECTIVE ALIGNMENT

This strategy embodies:

1. **Reciprocity-based fairness:** Reward cooperation with cooperation; respond to defection proportionally, not vindictively

2. **Stabilization tendency:** By requiring 50% threshold rather than 100%, we tolerate some defection and stabilize around mixed strategies rather than cascading to mutual defection

3. **Graceful degradation:** When collective action fails, we minimize future losses without escalating harm

4. **Information leverage:** We use publicly observable history to make decisions that implicitly encourage others toward cooperation (signaling through our own contribution)

5. **Non-exploitation:** We do not attempt to exploit others via false signaling or hidden coordination (no communication available anyway)

## ROBUSTNESS PROPERTIES

- **Against pure defectors:** We defect after round 1, matching their strategy
- **Against tit-for-tat cooperators:** We sustain mutual cooperation indefinitely
- **Against random players:** We achieve better-than-random collective outcomes by thresholding at 50%
- **Against adaptive defectors:** Our permanent defection trigger prevents being slowly eroded
- **Against majority cooperators:** We remain in the cooperative equilibrium

## PARAMETER SENSITIVITY

If k/n < 0.4 (weak multiplier): Increase threshold to 0.6
If k/n > 0.8 (strong multiplier): Decrease threshold to 0.4

This ensures the strategy scales with the true benefit structure.
'''

description_COLLECTIVE_53 = '''
# ADAPTIVE COLLECTIVE STRATEGY FOR PUBLIC GOODS GAME

## CORE PHILOSOPHY
Maximize collective welfare through conditional cooperation that rewards mutual contribution while maintaining robustness against free-riding. The strategy balances optimism (assume others will cooperate) with realism (punish defection through temporary withdrawal).

## DECISION RULES

### Round 1 (Initialization)
**COOPERATE**
- Establish a cooperative baseline to signal trustworthiness
- Gather information about opponent cooperativeness
- No history to condition on, so default to welfare-maximizing collective action

### Rounds 2 through (r-1) (Main Phase)
**Adaptive Threshold Rule:**

1. Calculate the **cooperation rate** in the previous round:
   - cooperation_rate = (total_contributions in round t-1) / n

2. If cooperation_rate ≥ threshold (recommended: 0.5 or higher):
   - **COOPERATE** - reciprocate the collective's effort
   - This preserves and encourages the cooperative equilibrium

3. If cooperation_rate < threshold:
   - **Defect for one round** - signal dissatisfaction with the group's contribution level
   - This creates negative feedback without permanent breakdown

4. **Defection memory:** After defecting, return to COOPERATE in the next round regardless of the previous round's cooperation rate. This gives the group one round to improve before re-engaging.

### Round r (Final Round)
**COOPERATE**
- Even if cooperation rates have been low, contribute in the final round
- Rationale: Last-round defection ruins the collective outcome and only benefits the defector marginally
- The strategy prioritizes collective welfare even when individual incentives suggest defection

## HANDLING EDGE CASES

**Catastrophic defection (cooperation_rate = 0):**
- Defect immediately, but only for one round
- Return to cooperation the following round as an attempt to restart cooperation
- Don't lock into mutual defection spirals

**Perfect cooperation (cooperation_rate = 1.0):**
- Continue cooperating indefinitely
- This is the collective optimum and should be maintained

**Noisy environments (cooperation rates fluctuate slightly):**
- Use a threshold band rather than exact cutoff (e.g., react to sustained patterns, not single-round noise)
- Only defect if cooperation_rate falls below threshold for 2 consecutive rounds (optional refinement for stability)

## COLLECTIVE ALIGNMENT

This strategy serves the collective interest by:
1. **Achieving high mutual payoffs** when opponents are reciprocal
2. **Penalizing free-riders** through temporary defection, creating incentive for them to join the cooperative coalition
3. **Avoiding mutual defection traps** by always returning to cooperation after signaling disapproval
4. **Prioritizing final-round welfare** to prevent destructive last-round dynamics
5. **Remaining transparent** - the rule is learnable, encouraging others to adopt cooperative patterns

## ROBUSTNESS

- Against unconditional cooperators: earns near-optimal payoffs
- Against unconditional defectors: defects back, preventing exploitation
- Against tit-for-tat: maintains cooperation through reciprocal matching
- Against mixed strategies: adapts to the group's aggregate behavior rather than individual player behavior, reducing vulnerability to noise
'''

description_COLLECTIVE_54 = '''
# ADAPTIVE COLLECTIVE CONTRIBUTION STRATEGY

## CORE PRINCIPLE
Maximize collective welfare by cultivating cooperation through conditional reciprocity, while maintaining individual resilience against exploitation. The strategy treats the game as a dynamic trust-building exercise where contribution patterns signal reliability to other players.

## DECISION RULE (GENERAL CASE)

**Contribute (C) if and only if:**
1. Expected collective payoff from cooperation exceeds defection, AND
2. The contribution rate in the previous round meets a sustainability threshold, AND
3. No systematic free-riding pattern has emerged from any player

**Defect (D) otherwise.**

More specifically:

```
IF round == 1:
  CONTRIBUTE
  (Bootstrap cooperation; test the environment)

ELSE IF round == r (final round):
  DEFECT
  (Last round has no future consequences; rational self-interest)

ELSE:
  previous_contribution_rate = (sum of all contributions in round t-1) / n
  
  IF previous_contribution_rate >= threshold_t:
    CONTRIBUTE
    (Reciprocate; others are cooperating at sustainable levels)
  
  ELSE IF previous_contribution_rate < threshold_t:
    Calculate expected payoff from C vs D given observed behavior
    IF (collective payoff from my C + others' likely future C) > (my D payoff):
      CONTRIBUTE
      (Signal willingness to rebuild; show leadership)
    ELSE:
      DEFECT
      (Cooperation unsustainable; protect endowment)
```

## ADAPTIVE THRESHOLD MECHANICS

The sustainability threshold adjusts dynamically:

- **Rounds 1-3:** threshold = 0.5 (permit trial-and-error)
- **Rounds 4-r-2:** threshold = 0.6 (expect majority contribution)
- **Approaching end-game:** threshold = 0.7 (stricter reciprocity requirement)

If contribution rates decline across 2+ consecutive rounds, lower threshold by 0.1 to prevent premature defection cascades.

## EDGE CASES & SPECIAL BEHAVIORS

**Identifying Free-Riders:**
- Track per-player contribution history
- If any player contributes in <20% of rounds while others maintain >60%, treat that player as a systematic defector
- Defect more readily when facing known defectors to avoid wasting endowment

**Handling Conditional Cooperators:**
- Players whose contributions correlate with others' previous contributions deserve reciprocal encouragement
- Increase likelihood of contributing if these players contributed last round (they may be conditional cooperators)

**End-Game Dynamics:**
- In final 2 rounds, shift toward defection to secure accumulated gains
- However, if current round contribution rate is ≥0.75, consider one final contribution in round r-1 to signal trustworthiness for potential future interactions (if reputation matters)
- Always defect in round r

**Cascading Defection Risk:**
- If contribution rates drop below 0.3 for more than one round consecutively, treat this as a coordination failure
- Attempt a unilateral contribution in the next round (show non-punishment reciprocity) but prepare for continued defection
- After 2 failed recovery attempts, defect going forward

## COLLECTIVE ALIGNMENT

This strategy prioritizes:
1. **Systemic Health:** Contribution thresholds are calibrated to sustain cooperation when feasible, benefiting the entire group
2. **Mutual Benefit:** Early cooperation creates a foundation for reciprocal patterns that improve all players' outcomes relative to universal defection
3. **Resilience:** Defection against systematic free-riders protects the strategy from exploitation without requiring punishment institutions
4. **Signaling:** Strategic contributions during downturns signal cooperative intent, differentiating this strategy from purely selfish approaches

## ROBUSTNESS NOTES

This strategy performs well against:
- **Unconditional cooperators** (out-earns them via occasional defection)
- **Conditional cooperators** (reciprocates, stabilizing cooperation)
- **Conditional defectors** (adapts thresholds to disengage gracefully)
- **Random players** (maintains partial contribution when sustainable)

It concedes mutual defection cycles when opponents are rigid defectors, but this is unavoidable without enforcement power.
'''

description_COLLECTIVE_55 = '''
# ADAPTIVE COLLECTIVE STRATEGY FOR PUBLIC GOODS GAME

## CORE PHILOSOPHY
Maximize collective welfare by contributing when conditions support it, while protecting against exploitation. The strategy treats the game as a repeated coordination problem where building trust is valuable but not guaranteed.

---

## DECISION RULE: CONTRIBUTION THRESHOLD POLICY

**Contribute (C) if and only if:**
- Expected collective payoff from universal contribution exceeds expected payoff from defection
- Recent history suggests sufficient cooperation to sustain mutual benefit
- We haven't entered the final "defection window"

**Specifically:**

1. **Rounds 1 to (r - ceil(r/4))** — Early and mid-game:
   - Contribute if the empirical cooperation rate in the previous round was ≥ threshold T
   - Set threshold T = max(0.5, 1/n) — require at least 50% contribution or 1/n players contributing, whichever is higher
   - Round 1: Contribute (assume optimism; test collective intent)
   - If cooperation rate drops below T, switch to defection and remain in defection until rate recovers

2. **Rounds (r - ceil(r/4)) to r** — Final quarter:
   - Defect unconditionally (end-game effect)
   - Rationale: No future rounds exist to sustain reciprocal cooperation; the multiplier benefit becomes irrelevant compared to keeping tokens

---

## ADAPTIVE RECOVERY MECHANISM

If defecting after a cooperation collapse:
- Monitor cooperation rates for signs of recovery
- If cooperation rate jumps back above (T + 0.15), re-enter contribution for one round as a "reconciliation test"
- If the test round shows sustained cooperation (rate ≥ T), resume contributing
- Otherwise, revert to defection

This avoids permanent deadlock while protecting against sequential exploitation.

---

## EDGE CASES

**First round:**
- Contribute unconditionally
- Signal good faith; gather baseline information on opponent pool composition

**Last round:**
- Defect unconditionally
- No opportunity for future reciprocation makes defection strictly optimal

**Two-player game (n=2):**
- Lower threshold to T = 0.4 (more tolerance for asymmetric play)
- Contribution yields k/2 multiplier; higher payoff structure allows more forgiveness

**Very short rounds (r ≤ 4):**
- Skip end-game defection phase; the defection window would dominate strategy
- Instead: Contribute for r-1 rounds, defect only on final round

**All players defect (cooperation = 0):**
- Remain in defection for 2 consecutive rounds
- If cooperation re-emerges, apply reconciliation test
- Otherwise, defect until end-game

---

## COLLECTIVE ALIGNMENT

This strategy prioritizes:
1. **Collective surplus generation** — Contributing when others do creates value for all
2. **Robustness** — Defection in the final quarter and after collapse prevents exploitation
3. **Fairness** — Threshold is symmetric across players; no privileged treatment
4. **Transparency** — Decision rule depends only on observable history; predictable to other rational agents

The strategy essentially implements "conditional cooperation with prudent defection," recognizing that in a multi-agent tournament, some opponents will defect and collective success requires protecting common gains while avoiding naive exploitation.
'''

description_COLLECTIVE_56 = '''
# ADAPTIVE COLLECTIVE RECIPROCITY STRATEGY FOR PUBLIC GOODS GAMES

## CORE STRATEGY: CONDITIONAL COOPERATION WITH STABILITY ENFORCEMENT

### Phase 1: Initial Exploration (Round 1)
**Action: COOPERATE**

Contribute in the first round to signal good faith and gather information about the population's baseline cooperation rate. This establishes a cooperative anchor without assuming others will reciprocate.

---

### Phase 2: Adaptive Reciprocity (Rounds 2 to r-2)

**Decision Rule - Cooperation Threshold:**

1. **Calculate the observed cooperation rate** from all players in the previous round:
   - cooperation_rate = (total contributions in round t-1) / n

2. **Estimate collective welfare potential:**
   - If cooperation_rate > (1 / k), contributing generates positive expected returns for the group
   - This is the critical threshold: contributing only makes collective sense if enough others do

3. **Conditional contribution decision:**
   - IF cooperation_rate ≥ (2/k): COOPERATE
     - At least half the welfare-enabling threshold has been reached; mutual benefit is likely
   - IF (1/k) ≤ cooperation_rate < (2/k): COOPERATE with probability = cooperation_rate * k
     - Probabilistic cooperation proportional to observed reciprocation
   - IF cooperation_rate < (1/k): DEFECT
     - Cooperation is being exploited; defection protects individual welfare

4. **Stabilization mechanism:**
   - Track the cooperation rate trend over the last 3 rounds
   - If cooperation is declining toward defection, shift the threshold downward by 5% to hold cooperation stable longer
   - This prevents cascade failures where mutual cooperation collapses

---

### Phase 3: Endgame (Final 2 rounds)

**Action: DEFECT**

In the final two rounds, defect unconditionally. This reflects the standard finitely-repeated game logic: when there is no future to influence, the payoff structure favors free-riding. However:
- This is announced implicitly through the strategy's deterministic logic
- Other rational players will anticipate this, so the overall impact on total rounds is limited
- Earlier rounds' reciprocity generates sufficient data for adaptive players to calibrate

---

## HANDLING EDGE CASES

**Unanimous defection scenario (cooperation_rate = 0):**
- Remain in defection until you observe at least one cooperator in a round
- If a single player cooperates, return to Phase 2 decision rule to test if coordination can restart

**Unanimous cooperation (cooperation_rate = 1):**
- Continue cooperating; this is the welfare-maximizing stable state
- Monitor for defectors; if any player defects, drop to probabilistic cooperation rule immediately

**Single round remaining:**
- Defect (endgame logic)

**k very close to 1:**
- Cooperation offers minimal multiplier benefit; shift to DEFECT in Phase 2 unless cooperation_rate > 0.8
- The strategy self-adjusts: low k makes cooperation less attractive, so defection becomes rational faster

---

## COLLECTIVE ALIGNMENT

This strategy prioritizes **collective welfare subject to sustainability:**

1. **Cooperation when viable:** It cooperates whenever the cooperation rate suggests mutual gain is achievable, maximizing group payoff
2. **Defection when exploited:** It withdraws cooperation when free-riding dominates, preventing cascade waste
3. **Stability over maximum:** It uses probabilistic reciprocation and trend-dampening to prevent the tragedy of the commons collapse, even if pure rationality would suggest defection
4. **Transparent incentives:** The strategy is deterministic and observable, allowing other players to learn and reciprocate effectively

The strategy is **robust** because it:
- Does not depend on assumed norms
- Adapts to any distribution of opponent types
- Uses only public information
- Remains individually rational while enabling collective gains when possible
'''

description_COLLECTIVE_57 = '''
# ADAPTIVE COLLECTIVE STRATEGY FOR PUBLIC GOODS GAME

## CORE PHILOSOPHY
Maximize collective welfare while maintaining individual rationality. The strategy seeks to sustain high contribution levels through credible reciprocity and adaptive threshold mechanisms, recognizing that collective gain requires coordinated behavior even without explicit communication.

## DECISION RULE - CONTRIBUTION THRESHOLD STRATEGY

**Primary Logic:**
- Contribute (C) if the observed average contribution rate in the previous round meets or exceeds a dynamically adjusted threshold
- Defect (D) if the average contribution rate falls below threshold
- Threshold starts at 50% and adjusts based on game phase and reciprocal evidence

**Detailed Decision Process:**

1. **First Round (Round 1):**
   - Contribute (C)
   - Rationale: Bootstrap cooperation with good faith; test the population's reciprocal capacity

2. **Subsequent Rounds (Round 2 through Round r-1):**
   - Calculate previous round's contribution rate: avg_contrib = (sum of all contributions) / n
   - Compare to current threshold
   - **If avg_contrib ≥ threshold:** Contribute (C) and slightly lower threshold by 2-3 percentage points (floor at 40%) to reward emerging cooperation
   - **If avg_contrib < threshold:** Defect (D) and raise threshold by 5 percentage points (ceiling at 70%) to signal that higher reciprocal effort is needed
   - **If threshold hasn't been met for 2+ consecutive rounds:** Remain defecting but keep threshold accessible (don't exceed 65%)

3. **Final Round (Round r):**
   - Ignore future considerations; apply strict logic
   - If avg_contrib_previous ≥ 50%: Contribute (C) to reinforce stable cooperation
   - If avg_contrib_previous < 50%: Defect (D) to avoid exploitation
   - This prevents exploitation in the endgame while respecting demonstrated reciprocity

## EDGE CASES AND ADAPTIVE REFINEMENTS

**Convergence Detection:**
- If contribution rate stabilizes at ≥70% for 3+ consecutive rounds, lower threshold to 45% to consolidate high cooperation
- If contribution rate stabilizes at ≤30% for 3+ consecutive rounds, accept partial defection and maintain threshold at 60%

**Mixed Signals Handling:**
- If contribution variance is high (some players always contribute, others never do), use median contribution rate instead of mean to avoid distortion by outliers
- Weight recent rounds (last 3) more heavily than distant ones when assessing reciprocity

**Minority Defection:**
- If ≥60% of players contributed but you would defect due to threshold, reduce this penalty: still defect but lower threshold by 3 points instead of raising it
- Rationale: Acknowledge that widespread cooperation exists even if below your threshold

## COLLECTIVE ALIGNMENT

**Why This Is Collectively Rational:**
- The strategy creates a **virtuous feedback loop**: Contributing signals willingness to cooperate, rewarding others' contributions and encouraging broader participation
- Thresholds are generous enough (starting at 50%) to avoid race-to-the-bottom but strict enough (ceiling at 70%) to punish systematic free-riding
- The strategy sacrifices short-term individual gain when reciprocity fails, sending a costly signal that cooperation norms matter
- By adapting slowly (2-3 point adjustments), the strategy gives populations time to coordinate without appearing capricious

**Tournament Robustness:**
- Against "Always Cooperate" opponents: Contributes consistently, benefiting from their reliability
- Against "Always Defect" opponents: Quickly learns they won't reciprocate and defects accordingly
- Against "Tit-for-Tat" variants: Mutual contribution sustains; threshold mechanism prevents exploitation in edge cases
- Against "Random" strategies: Threshold dynamics smooth noise; population-level contribution rate guides decisions

## SUMMARY
This is a **forgiving, reciprocal, slow-adjusting** strategy that prioritizes collective wealth creation while protecting against exploitation. It uses observable history to estimate the population's willingness to cooperate and adapts its own behavior to reinforce positive norms. It does not require communication or shared understanding—only the ability to observe past actions—making it genuinely collective within the game's constraints.
'''

description_COLLECTIVE_58 = '''
# ADAPTIVE RECIPROCAL CONTRIBUTION STRATEGY

## CORE PRINCIPLE
Maximize collective welfare through calibrated contributions that reward cooperation and penalize defection, while remaining resilient to exploitation.

## DECISION RULES

### Standard Round (Not First, Not Last)
1. **Calculate the cooperation rate** from the previous round:
   - cooperation_rate = (total contributions in round t-1) / n

2. **Determine contribution threshold:**
   - If cooperation_rate ≥ 0.5: CONTRIBUTE
   - If cooperation_rate < 0.5: DEFECT

3. **Rationale:** We contribute when the group shows meaningful cooperation (majority threshold), as this indicates the multiplier effect will benefit us. We defect when defection dominates, as contributing would be wasted.

### First Round (Round 1)
- **CONTRIBUTE**
- **Rationale:** Seed cooperation. Since no history exists, we initiate trust to establish a cooperative equilibrium. This is a collective signal that cooperation is valuable.

### Last Round (Round r)
- **DEFECT**
- **Rationale:** In the final round, there is no future to influence. Defecting maximizes individual payoff with no reputational cost. This is individually rational and honest about endgame dynamics.

### Rounds 2 through r-1
- Apply the standard reciprocal rule above

## HANDLING EDGE CASES

**Perfectly Defecting Opponents (cooperation_rate = 0):**
- Defect immediately and sustain defection
- We avoid being a lone cooperator subsidizing free-riders
- This prevents our strategy from being exploited by pure defectors

**Perfectly Cooperating Opponents (cooperation_rate = 1.0):**
- Continue contributing
- We benefit maximally from the multiplier while reciprocating

**Mixed Behavior / Volatile Groups:**
- The 50% threshold creates a stable attractor: if cooperation dips below 50%, we defect, which pushes others to defect, confirming the defection spiral. If cooperation stays above 50%, we maintain contribution, sustaining the cooperative equilibrium
- This creates two stable states (cooperation trap and defection trap) and uses the majority threshold as the pivot point

**Precisely at 50% Cooperation:**
- CONTRIBUTE (threshold is ≥ 0.5)
- This slightly favors continued cooperation when the group is balanced, as the marginal benefit of coordination outweighs one additional defection

## COLLECTIVE ALIGNMENT

This strategy prioritizes **group payoff** while remaining **self-protective:**

- **Rounds 1 to r-1 encourage coordination** around the cooperative equilibrium, which maximizes total welfare
- **Round r defection** is honest about incentive misalignment at the endgame and prevents naive exploitation
- **Reciprocal thresholding** ensures we don't subsidize free-riders; we only contribute when enough others do, creating positive feedback loops
- **Symmetry:** Every player following this strategy converges to a cooperative outcome until the final round, achieving high collective returns

## ROBUSTNESS

- **Against TIT-FOR-TAT variants:** Works well; both strategies converge to mutual contribution
- **Against pure defectors:** We quickly detect and defect back, minimizing losses
- **Against exploiters:** The reciprocal rule prevents us from being systematically preyed upon
- **Against random/noise strategies:** The 50% threshold is a robust pivot that doesn't overreact to single-round variance

This is a **grim-trigger hybrid**: cooperative until defection becomes the norm, then punitive, with a rational endgame capitulation.
'''

description_COLLECTIVE_59 = '''
# ADAPTIVE COLLECTIVE STRATEGY FOR PUBLIC GOODS GAME

## CORE PRINCIPLE
Maximize collective welfare through conditional cooperation that rewards group contribution while protecting against systematic defection. The strategy balances optimism about human cooperation with pragmatic defense against free-riding.

## DECISION RULES

### Round 1 (Initial Signal)
**COOPERATE**
- Signal willingness to contribute to collective benefit
- Establishes baseline for reciprocity norms
- Gathers information about opponent cooperation propensity

### Rounds 2 through (r-1) (Main Phase)

**Calculate the Group Contribution Rate:**
- Determine what fraction of the group (excluding self) cooperated in the previous round
- Let avg_others_contribution = sum of others' contributions / (n-1)

**Apply Conditional Cooperation with Escalation:**

1. **If avg_others_contribution ≥ threshold_high (e.g., 0.75):**
   - COOPERATE
   - Reinforce the cooperative equilibrium

2. **If threshold_medium (0.35) ≤ avg_others_contribution < threshold_high:**
   - COOPERATE with probability = avg_others_contribution
   - Maintain cooperation proportional to observed collective effort
   - Accept that some defection is rational; don't over-punish

3. **If avg_others_contribution < threshold_medium:**
   - DEFECT for 2 consecutive rounds
   - Signal that systematic free-riding is unsustainable
   - Brief punishment window allows recovery without permanently collapsing cooperation

4. **After defection window, attempt recovery:**
   - Return to COOPERATE to test whether cooperation can resume
   - If defection persists, cycle: 1 defect, 1 cooperate
   - This minimizes mutual destruction while maintaining credibility

### Final Round (Round r)

**DEFECT**
- The multiplier effect is no longer relevant for future cooperation
- No repeated-game incentive exists
- Rational to capture residual value from previous rounds' contributions by others

**Exception:** If average group contribution across ALL previous rounds exceeded 70%, COOPERATE in the final round as a collective signal that high-cooperation groups maintain integrity even when punishment-free.

## HANDLING EDGE CASES

**If you observe a player who ALWAYS cooperates:**
- Maintain cooperation with them; they subsidize the group

**If you observe a player who ALWAYS defects:**
- They receive your cooperative benefits but contribute nothing
- After 2 rounds of their consistent defection, shift to probabilistic defection in your model (see rule 3 above)

**If you observe oscillating/unpredictable players:**
- Treat as avg_others_contribution and apply the main rules
- Don't assume malice; variance may reflect their own adaptation strategy

**If n is very large (>10 players):**
- Lower thresholds slightly (e.g., threshold_high = 0.65, threshold_medium = 0.25)
- Individual defection has diminishing impact on collective returns
- Cooperation becomes more robust to a few defectors

**If r is very small (<5 rounds):**
- Shift final-round defection threshold earlier: defect in last 2 rounds instead
- Short horizons make reputation less valuable

## COLLECTIVE ALIGNMENT

This strategy prioritizes:
1. **Group welfare over individual gain** – Cooperate when others do, even if defection yields higher payoff
2. **Sustainability** – Avoid mutual defection traps through measured punishment and recovery windows
3. **Transparency** – Actions reveal cooperation intent; history-dependent rules are observable
4. **Robustness** – Works against free-riders (punish), cooperators (reciprocate), and mixed strategies (adapt)
5. **Fairness** – Don't defect preemptively; only respond to systematic group-level defection

## RATIONALE

This is a **win-stay, lose-shift with adaptive thresholds** approach embedded in a conditional-cooperation framework. It recognizes that in PGG, the group's payoff is maximized at full cooperation, and this strategy works to achieve that outcome while protecting against exploitation. The final-round defection acknowledges game theory's endgame problem while offering a redemption path for high-cooperation groups.
'''

description_COLLECTIVE_60 = '''
# ADAPTIVE CONDITIONAL COOPERATION WITH DECAY

## CORE STRATEGY: RESPONSIVE THRESHOLD-BASED CONTRIBUTION

### Primary Decision Rule

**Each round, calculate the empirical cooperation rate from the previous round:**
- cooperation_rate = (total contributions in round t-1) / n

**Then decide:**
- IF cooperation_rate ≥ threshold (initially 0.5) → CONTRIBUTE
- ELSE → DEFECT

**Threshold adjustment:** After each round, lower the threshold by 0.05 (minimum 0.0), making cooperation increasingly difficult to sustain as the game progresses. This prevents wasteful contributions against consistently defecting opponents while maintaining reciprocity.

---

## EDGE CASES & SPECIAL ROUNDS

**Round 1 (no history):**
- CONTRIBUTE. This is a costly signal of willingness to cooperate and gathers information about other players' types.

**Final round (round r):**
- Evaluate as normal using the threshold rule. Even though there's no future reputation to build, this maintains consistency and prevents exploitable end-game patterns.

**After 2+ consecutive rounds of universal defection (all other players contribute 0):**
- Switch to permanent DEFECT. Continuing to contribute is irrational once it's clear cooperation won't be reciprocated.

---

## RATIONALE: WHY THIS WORKS

1. **Avoids exploitation:** Defectors cannot indefinitely extract value. Once defection dominates, you stop contributing.

2. **Reciprocity:** Matches others' behavior with a slight lag, creating implicit tit-for-tat dynamics without explicit agreement.

3. **Adaptive thresholds:** The declining threshold acknowledges that later rounds have fewer opportunities to recoup losses, so you only contribute if others demonstrate strong cooperation.

4. **Robust to heterogeneity:** Doesn't assume opponents use similar strategies—works against pure defectors, pure cooperators, and mixed strategies.

5. **Collective welfare:** First-round cooperation and reciprocal behavior support higher collective payoffs when opponents are conditionally cooperative, while defection against persistent free-riders protects individual payoffs.

---

## SUMMARY

Cooperate initially and reciprocate cooperation, but with increasing skepticism over time. Permanently exit cooperation if defection becomes dominant. This balances collective gains with individual protection in an untrusted environment.
'''

description_COLLECTIVE_61 = '''
# ADAPTIVE CONDITIONAL COOPERATION STRATEGY

## CORE PRINCIPLE
Cooperate conditionally based on recent collective performance and individual reciprocity signals. The strategy balances trust in others' cooperation with protection against defection, using history to calibrate behavior.

## DECISION RULE (ROUNDS 2 ONWARDS)

**Calculate the Cooperation Rate (CR):**
- Look at the last M rounds (where M = min(5, current_round - 1))
- CR = total contributions observed / (M × n)

**Classify the Game State:**
1. **High Cooperation (CR ≥ 0.6):** Contribute
2. **Medium Cooperation (0.3 ≤ CR < 0.6):** Contribute if you contributed last round AND gained positive payoff last round; otherwise Defect
3. **Low Cooperation (CR < 0.3):** Defect

**Rationale:** 
- When others are cooperating, collective returns justify individual contribution
- In mixed environments, reward your own previous reciprocal behavior with continued cooperation
- In defection-dominant environments, protect your endowment

## EDGE CASES

**Round 1:**
Contribute. This is the trust-initiating move in a repeated game with complete information revelation.

**Final Round (Round r):**
Defect. The game ends with no future reciprocal opportunities, so the multiplier benefit doesn't justify forgoing the endowment.

**Consecutive Low Payoff Trap:**
If you've defected for 2+ consecutive rounds AND CR remains below 0.3, continue defecting (don't re-enter cooperation immediately). Wait for environmental signals that cooperation is viable again.

## ROBUSTNESS FEATURES

**Against Free-Riders:**
- Low CR detection switches you to defection before substantial losses accumulate
- You don't punish defectors unilaterally (which would lower your own payoff), but you stop subsidizing them

**Against Conditional Cooperators:**
- Your reciprocal behavior in medium-CR states mirrors and reinforces other conditional cooperators
- This creates tacit coordination toward mutual cooperation without explicit communication

**Against Random Players:**
- The 5-round window prevents short-term noise from triggering abandonment of cooperation
- CR thresholds are set to tolerate ~40% noise while still detecting systematic defection

**Against Sophisticated Exploiters:**
- Your final-round defection removes the "last-round immunity" that exploiters might target
- Medium-CR reciprocity prevents systematic exploitation (you defect when they defect)

## COLLECTIVE ALIGNMENT

This strategy advances collective welfare by:
1. **Initiating cooperation** (Round 1) to establish the foundation for mutual gains
2. **Maintaining cooperation** when others reciprocate, capturing the multiplier benefits that maximize group welfare
3. **Withdrawing strategically** when cooperation has broken down, preventing resource waste on unilateral contributions
4. **Avoiding punishment cycles** that harm everyone, instead using payoff-based adaptation

The strategy assumes collective success means higher average payoffs for all, which the PGG structure incentivizes under reasonable cooperation levels.
'''

description_COLLECTIVE_62 = '''
# ADAPTIVE CONDITIONAL COOPERATION STRATEGY

## CORE PRINCIPLE
Maximize collective welfare by incentivizing sustained cooperation while maintaining individual robustness against exploitation.

## PRIMARY DECISION RULE: CONDITIONAL CONTRIBUTION

**Cooperate (C) if and only if:**
1. The aggregate contribution rate in the previous round meets or exceeds a dynamic threshold, OR
2. It is round 1 (initialization phase), OR
3. Expected payoff from cooperation exceeds defection given observed opponent patterns

**Otherwise Defect (D)**

## DYNAMIC THRESHOLD CALCULATION

Set the cooperation threshold as:
- **Rounds 1-3:** Threshold = 50% (generous initialization to probe cooperativeness)
- **Rounds 4 onwards:** Threshold = (average historical contribution rate across all players) - 10%

The 10% buffer accounts for natural variance and incomplete information.

## EDGE CASES & SPECIAL HANDLING

**First Round:**
Contribute (C). This signals good faith and tests the player pool's baseline cooperativeness.

**Last Round (if known):**
Defect (D) only if cumulative evidence shows systematic exploitation. Otherwise contribute—the final round is where reputation effects are strongest for future interactions.

**If Last Round is Unknown:**
Treat each round as potentially terminal and maintain the conditional strategy throughout.

**Sudden Defection Detection:**
If a previously cooperative player (contribution rate >70%) suddenly defects, assume potential miscommunication or strategic shift. Give one round of defection in response, then reassess.

**Against All-Defect Opponents:**
After 2 consecutive rounds where <20% of players contribute, shift to persistent defection to minimize losses.

## ROBUSTNESS MECHANISMS

**Against Free-Riders:**
Only cooperate when others do. This prevents subsidizing pure defectors.

**Against Conditional Cooperators:**
Sustain contributions to maintain the threshold high enough that cooperative players stay engaged.

**Against Random Actors:**
Use a 3-round rolling average of contribution rates to filter noise from strategic defection.

## COLLECTIVE ALIGNMENT

This strategy prioritizes:
1. **Efficiency:** Maintains high aggregate contributions when the group is capable of it
2. **Fairness:** Punishes free-riding through conditional non-contribution
3. **Sustainability:** Avoids mutual punishment spirals by using soft enforcement (gradual threshold adjustment rather than harsh retaliation)
4. **Resilience:** Functions without assuming opponent cooperation, so it survives tournament diversity

---

**In sum:** Start cooperatively, reward cooperation with cooperation, punish defection with measured defection, and adapt thresholds based on collective behavior patterns.
'''

description_COLLECTIVE_63 = '''
# COLLECTIVE STRATEGY FOR PUBLIC GOODS GAME

## CORE PRINCIPLE
Maximize collective welfare through conditional cooperation that gradually builds trust, while maintaining resilience against exploitation.

## DECISION RULES

### CONTRIBUTION DECISION
Contribute (C) if and only if:
- **Round 1**: CONTRIBUTE unconditionally (signal cooperative intent)
- **Round 2 onwards**: Contribute if the average contribution rate in the previous round was ≥ (k-1)/k, OR if fewer than half of remaining rounds remain
- **Last Round**: DEFECT (no future punishment possible, individual payoff dominates)
- **Second-to-Last Round**: Contribute only if average previous contribution ≥ (k-1)/k

### THRESHOLD RATIONALE
The threshold (k-1)/k represents the minimum contribution density where cooperation is self-sustaining. When others contribute at this rate or higher, the multiplier k guarantees that each individual's contribution yields collective return ≥ 1, making cooperation individually rational. Below this threshold, defection becomes optimal.

## EDGE CASES & SPECIAL HANDLING

**First Round**: Contribute despite uncertainty. This establishes cooperative signal and generates information about others' baseline tendencies.

**Last Two Rounds**: Apply strict defection discipline. Temporal urgency removes incentive for reciprocal punishment, making individual defection rational. Defecting early signals you cannot be exploited in endgame.

**Free-Rider Detection**: Track individual contribution histories. If a player contributes <20% of rounds while others contribute ≥60%, model them as a defector and adjust threshold downward for that analysis (expect lower collective contribution rates).

**Sudden Collapse**: If contributions drop >40% from previous round average, interpret as strategic shift rather than noise. Defect next round to avoid cascading losses, then re-enter conditional cooperation if rates recover.

**Endgame Transition** (final ⌊r/3⌋ rounds): Gradually increase defection probability linearly from 0 to 100% as remaining rounds approach zero, rather than abrupt switch. This prevents sudden coordination breakdown.

## ROBUSTNESS FEATURES

- **Non-exploitable**: Never contributes when exploitation likelihood is high (low prior contribution rates)
- **Adaptive**: Adjusts to learned multiplier k indirectly through observation of whether others' contributions sustain
- **Resilient to variance**: Uses average contribution rates rather than individual round outcomes to filter noise
- **Self-aware about incentives**: Acknowledges that last rounds fundamentally change game structure and acts accordingly

## COLLECTIVE ALIGNMENT

This strategy doesn't assume shared norms. Instead, it:
1. **Tests** whether collective cooperation is viable given the observed player pool
2. **Participates** in coordination when reciprocal benefits are clear (contribution threshold met)
3. **Exits gracefully** when cooperation breaks down, minimizing collective damage
4. **Protects** against free-riding without requiring explicit punishment mechanisms

The strategy treats collective welfare as achievable only when individually rational at the margin—it cooperates when the multiplier effect makes cooperation mutually beneficial, and stops when it doesn't.
'''

description_COLLECTIVE_64 = '''
# ADAPTIVE COLLECTIVE CONTRIBUTION STRATEGY FOR PGG

## CORE PRINCIPLE
Maximize collective welfare by contributing when the multiplier effect creates positive-sum outcomes, while protecting against exploitation through conditional defection triggered by persistent free-riding.

## PRIMARY DECISION RULE: CONTRIBUTION THRESHOLD

**Contribute (C) if and only if:**
- The expected collective payoff from universal contribution exceeds the Nash equilibrium (all-defect) payoff, AND
- Historical defection rates suggest sufficient reciprocity to sustain cooperation

**Specifically:**
- Contribute if: `k > 1` (always true by problem definition, but condition on next rule)
- Contribute if: The proportion of contributors in the previous round ≥ `(1 - k/n) / (1 - 1/n)` 
  - This represents the minimum cooperation rate where mutual contribution remains better than mutual defection
- On Round 1: **CONTRIBUTE** (signal cooperative intent; test waters)

## ADAPTIVE RECIPROCITY MECHANISM

**Track the historical cooperation rate** across all previous rounds:
- Let `coop_rate` = (total contributions across all players and rounds) / (total possible contributions)

**Decision logic by cooperation context:**

1. **High cooperation phase** (coop_rate ≥ 0.6):
   - Continue contributing
   - Rationale: Sufficient collective momentum; mutual contribution yields strong returns

2. **Moderate cooperation phase** (0.3 ≤ coop_rate < 0.6):
   - Contribute with probability equal to `coop_rate`
   - Rationale: Match the group's reciprocity level; probabilistic defection signals demand for higher cooperation

3. **Low cooperation phase** (coop_rate < 0.3):
   - **DEFECT** (contribute 0)
   - Rationale: Cooperation multiplier is being diluted; individual payoff-maximization is rational when group fails collective coordination

## FINAL ROUND ADJUSTMENT

**On the last round (round r):**
- Ignore all historical signals and **DEFECT**
- Rationale: No future reputation to maintain; the game-theoretic dominant strategy is to free-ride in the final stage

## EDGE CASES & ROBUSTNESS

**What if every opponent defects from round 1?**
- After round 1, coop_rate drops sharply; switch to defection by round 2 and sustain it
- Avoids cascading losses to rational defectors

**What if opponents alternate unpredictably?**
- Probabilistic matching (via moderate cooperation phase) creates a mixed strategy that is robust to unpredictable behavior
- Neither fully exploited nor overly punitive

**What if only one opponent cooperates?**
- If alone with that opponent, marginal benefit of cooperation = k/2 per round (positive)
- History tracks this; continue contributing if one reciprocating player sustains it
- Collective benefit still realized

## COLLECTIVE ALIGNMENT

This strategy prioritizes:
1. **Collective payoff maximization** by contributing when k > 1 (the fundamental efficiency gain)
2. **Robustness to free-riding** by conditional defection (prevents indefinite exploitation)
3. **Emergent coordination** without communication (relies only on observable history, creating implicit norm-following)
4. **Self-reinforcing cooperation** (high cooperation → continued contribution → higher payoffs → attracts more contributors)

The strategy treats the group as a dynamic system: it cooperates to build momentum, adapts when momentum fails, and exits when the collective becomes too diluted to generate positive returns.
'''

description_COLLECTIVE_65 = '''
# COLLECTIVE STRATEGY: ADAPTIVE CONDITIONAL COOPERATION WITH DECAY

## CORE PRINCIPLE
Contribute when the collective benefit exceeds individual cost, but adapt based on observed reciprocity. Treat the game as a test of whether mutual cooperation can emerge from self-interested play.

---

## PRIMARY DECISION RULE: CONDITIONAL CONTRIBUTION

**For rounds 2 through r-1 (the "middle game"):**

1. **Calculate the Reciprocity Ratio** from the previous round:
   - Count how many other players contributed (let's call this `others_contributed`)
   - Compute: `reciprocity_ratio = others_contributed / (n - 1)`

2. **Contribution Threshold Logic:**
   - Contribute if: `reciprocity_ratio >= threshold(round)`
   - Otherwise: Defect

3. **Dynamic Threshold:**
   - Early rounds (1-3): `threshold = 0.5` — willing to cooperate if roughly half reciprocate
   - Mid rounds (4 to r-2): `threshold = 0.4` — slightly more optimistic; encourage emergence of cooperation
   - Late rounds (r-1 to r): `threshold = 0.6` — stricter, protect against exploitation

---

## EDGE CASES

**Round 1 (Opening Move):**
- Contribute. This signals cooperative intent and generates data about the opponent pool.
- Rationale: The first move is information-generating; defecting immediately poisons the well.

**Final Round (Round r):**
- Apply the standard reciprocity rule with `threshold = 0.6`, but be prepared to defect if the last round showed low reciprocity (< 0.3).
- Rationale: Even in the final round, maintaining consistency preserves reputation across repeated encounters.

**Unanimous Defection Detection:**
- If all other players defected in the previous round (`others_contributed = 0`), defect in the current round.
- Exception: If this is round 2 and round 1 showed unanimous defection, contribute once more to test whether it was random/mistake. Then defect if it repeats.
- Rationale: Don't throw good tokens after bad; exit cycles of universal defection.

**Unanimous Cooperation Detection:**
- If all other players contributed in the previous round (`others_contributed = n - 1`), contribute unconditionally in the current round.
- Rationale: Sustain successful cooperation and maximize collective payoff.

---

## ROBUSTNESS MECHANISMS

**Against Unconditional Defectors:**
- The reciprocity ratio will be low; you defect quickly and minimize losses.

**Against Tit-for-Tat Strategies:**
- Both strategies will converge toward mutual cooperation if you start with contribution, matching the cooperative intent.

**Against Mixed/Noise-Based Strategies:**
- The dynamic threshold smooths out noise; you don't overreact to single defections.
- If noise persists, the threshold naturally becomes stricter, protecting you.

**Against Exploiters (cooperate with you, defect on others):**
- You observe *everyone's* past actions, not just your own payoff.
- If a player defects against others but cooperates with you, the collective reciprocity ratio remains low, and you eventually defect.

---

## COLLECTIVE ALIGNMENT

This strategy embodies collective welfare because:

1. **It opens with cooperation**, assuming others are rational enough to reciprocate—giving the group a chance to reach the efficient equilibrium.

2. **It relies on observing *all* past actions**, not just personal payoffs. If others cooperate broadly, you cooperate; if they defect broadly, you exit. This aligns your fate with the group's trajectory.

3. **It is transparent and predictable**, allowing other cooperative strategies to synchronize with you.

4. **It uses thresholds, not strict tit-for-tat**, so occasional defections by good-faith players don't trigger permanent retaliation. This forgiveness reduces mutual punishment cycles.

5. **It skews toward defection only when cooperation has demonstrably failed**, not preemptively, maximizing the chance of collective success.

---

## SUMMARY

- **Rounds 1–3:** Contribute if ≥50% of others did; start cooperative.
- **Rounds 4 to r-2:** Contribute if ≥40% of others did; sustain cooperation.
- **Rounds r-1 to r:** Contribute if ≥60% of others did; tighten standards near the end.
- **Always:** Exit if all others defect; sustain if all others cooperate.
'''

description_COLLECTIVE_66 = '''
# COLLECTIVE STRATEGY FOR PUBLIC GOODS GAME

## CORE PRINCIPLE
Maximize collective welfare by fostering cooperation while maintaining robustness against free-riders. This strategy balances reciprocity, reputation monitoring, and adaptive responses to evolving group dynamics.

## DECISION RULES

### ROUND 1 (Initialization)
**CONTRIBUTE (C)**

Rationale: In the absence of history, assume good faith. Contributing signals willingness to cooperate and establishes a foundation for reciprocal behavior. This is collectively optimal if others reciprocate.

### ROUNDS 2 to (r-1) (Main Phase)

**Calculate the Group Cooperation Rate (GCR):**
- GCR = (total contributions in round t-1) / n
- This measures the proportion of players who contributed last round

**Decision Rule - Adaptive Reciprocity:**

1. **If GCR ≥ threshold_high (e.g., 0.7):** 
   - CONTRIBUTE (C)
   - Rationale: Strong cooperation norm detected. Maintain collective momentum.

2. **If threshold_low (e.g., 0.3) ≤ GCR < threshold_high:**
   - CONTRIBUTE (C)
   - Rationale: Mixed cooperation. Still contribute to encourage convergence toward collective optimum, but monitor for defection patterns.

3. **If GCR < threshold_low:**
   - DEFECT (D)
   - Rationale: Cooperation is collapsing. Defecting minimizes losses when most are free-riding. Continued contribution yields diminishing returns.

**Refinement - Individual Accountability:**
- Track each player's contribution history separately
- If any individual player has defected in >60% of observed rounds, downgrade your assessment of group cooperativeness by applying a penalty: reduce GCR by 0.15
- This prevents a few persistent free-riders from triggering group collapse through false hope

### ROUND r (Final Round)

**DEFECT (D)**

Rationale: In the final round, there is no opportunity for reciprocal response or reputation effects. Contributing provides no strategic benefit. Defecting is individually rational and aligns with standard game-theoretic predictions. This is transparent and collectively honest—if others follow this logic, all simultaneously realize the Nash equilibrium.

*Alternative consideration:* If GCR in round (r-1) was ≥ 0.8, consider contributing in the final round as a goodwill gesture. However, the default should be defection for robustness.

## HANDLING EDGE CASES

**Very few players (n ≤ 3):**
- Thresholds become less meaningful. Increase threshold_low to 0.4 and threshold_high to 0.8 (stricter) to avoid over-committing in high-defection scenarios where payoff multipliers are modest.

**Very few rounds (r ≤ 3):**
- Shorten the main phase. If r = 2, skip the main phase: Contribute in Round 1, Defect in Round 2.

**High multiplier (k close to n):**
- Contribution yields high returns. Lower threshold_high to 0.6 and threshold_low to 0.2 to favor cooperation even with modest group participation.

**Low multiplier (k close to 1):**
- Contribution yields low returns. Raise thresholds: threshold_high = 0.8, threshold_low = 0.4.

## COLLECTIVE ALIGNMENT

This strategy embodies collective welfare through:

1. **Reciprocal Fairness:** Contribution rates adjust to match observed group behavior, preventing exploitation.
2. **Stability Focus:** The adaptive thresholds prevent abrupt all-defect cascades; they dampen oscillation.
3. **Shared Burden:** By contributing in mixed phases, this strategy gives cooperation opportunities to stabilize, benefiting all.
4. **Transparency:** The final-round defection is honest about incentive structures rather than pretending false cooperation.
5. **Resilience:** Individual accountability tracking prevents a few bad actors from collapsing the group.

## SUMMARY TABLE

| Phase | Condition | Action | Rationale |
|-------|-----------|--------|-----------|
| Round 1 | N/A | C | Initialize cooperation |
| Rounds 2–(r-1) | GCR ≥ 0.7 | C | Strong cooperation |
| Rounds 2–(r-1) | 0.3 ≤ GCR < 0.7 | C | Encourage convergence |
| Rounds 2–(r-1) | GCR < 0.3 | D | Minimize losses |
| Round r | Any | D | Final-round honesty |
'''

description_COLLECTIVE_67 = '''
# COLLECTIVE STRATEGY FOR PUBLIC GOODS GAME

## CORE PRINCIPLE
Maximize collective welfare by inducing cooperation through **conditional reciprocity with adaptive thresholds**, while protecting against free-riders through graduated defection.

## DECISION RULE (PRIMARY)

**Cooperate if and only if:**
- The historical cooperation rate among all players (including self) in the previous round meets or exceeds a dynamic threshold
- **Threshold formula:** `T(t) = k/n + (1 - k/n) * (1 - t/r)`
  - At round t=1: threshold is relatively low (encouraging initial cooperation)
  - At round t=r (final round): threshold approaches k/n (the break-even point)
  - This creates a "cooperation curve" that gradually relaxes as we approach the end

**Defect if:**
- The cooperation rate falls below threshold, indicating insufficient collective contribution
- Free-rider presence is detected (see edge cases below)

## ROUND-SPECIFIC BEHAVIOR

**Round 1 (Opening):**
- COOPERATE unconditionally
- Signal willingness to contribute and test the group's baseline prosocial tendency
- Rationale: Establishes baseline expectations without punishment history

**Rounds 2 to r-1 (Mid-game):**
- Apply the primary decision rule above
- Track the cooperation rate as a rolling average of the last 3 rounds (if available) to filter noise
- If cooperation rate is rising, maintain contribution even if slightly below threshold
- If cooperation rate is declining, move to defection faster

**Final Round (Round r):**
- Apply threshold with k/n as the floor
- If cooperation rate in round r-1 was ≥ (k/n + 0.1), COOPERATE (reward sustained cooperation)
- If cooperation rate in round r-1 was < k/n, DEFECT (exploit final defection window)
- Rationale: Align endgame behavior with collective outcomes achieved, not personal gain

## EDGE CASES & ADAPTIVE RESPONSES

**Unanimous Defection Detected:**
- If all players defect in round t, DEFECT in round t+1
- Rationale: No benefit to unilateral cooperation; signal non-exploitation

**High Variance in Contributions:**
- If individual players alternate between C and D unpredictably, treat them as defectors (assume T behavior)
- Respond with reciprocal defection to avoid being exploited
- Rationale: Tit-for-tat-like response to unreliable partners

**Near-Threshold Ambiguity:**
- If cooperation rate is within ±5% of threshold, COOPERATE
- Rationale: Tie-breaking in favor of collective benefit; marginal cost is low

**Minority Cooperators (Rounds 2-5):**
- If only 1-2 players cooperate while others defect, DEFECT
- Rationale: Avoid being the sole sucker; redirect resources

**Late-Game Cooperation Recovery:**
- If cooperation rate rises above (k/n + 0.2) in any round after a defection phase, return to COOPERATE
- Rationale: Adaptive forgiveness; rejoin emerging cooperative consensus

## COLLECTIVE ALIGNMENT

This strategy:
1. **Maximizes total payoffs** by encouraging cooperation when viable (threshold design)
2. **Protects the group** from serial exploitation (defection against free-riders)
3. **Reduces coordination burden** by making decisions observable and predictable
4. **Scales robustly** across player counts (threshold uses k/n, which normalizes incentives)
5. **Handles uncertainty** by using rolling averages and tie-breaking toward cooperation

The strategy is not purely altruistic—it defects when cooperation fails—but it actively recruits cooperation rather than assuming it.
'''

description_COLLECTIVE_68 = '''
# ADAPTIVE COLLECTIVE STRATEGY FOR PUBLIC GOODS GAME

## CORE PRINCIPLE
Maximize collective welfare by fostering conditional cooperation that scales with demonstrated group commitment, while maintaining individual resilience against exploitation.

## DECISION RULES

### Round 1 (Initialization)
**CONTRIBUTE (C)**
- Signal cooperative intent to establish a cooperative foundation
- Gather information on opponent types through their responses
- Set positive expectation for reciprocal behavior

### Rounds 2 through r-1 (Adaptive Phase)

**Calculate Group Cooperation Metric:**
- Compute the average contribution rate across all *other* players in the previous round: `avg_others = (sum of others' contributions) / (n-1)`

**Decision Logic:**
1. **If avg_others ≥ 0.75** (strong cooperation observed)
   - CONTRIBUTE (C)
   - Reinforce the cooperative equilibrium with matching commitment

2. **If 0.40 ≤ avg_others < 0.75** (moderate cooperation)
   - CONTRIBUTE (C)
   - Sustain cooperation to encourage threshold-crossing toward stable equilibrium
   - Accept short-term efficiency loss to prevent collapse into defection

3. **If 0.10 < avg_others < 0.40** (weak cooperation)
   - DEFECT (D)
   - Avoid being exploited by free-riders
   - Withdraw contribution to signal that participation requires reciprocal commitment

4. **If avg_others ≤ 0.10** (defection dominant)
   - DEFECT (D)
   - No viable collective outcome; protect individual payoff
   - Minimize losses in a broken-trust environment

### Final Round r (Endgame)
**DEFECT (D)**
- Standard backward induction logic: no future rounds remain to incentivize cooperation
- Individual payoff maximization is rational when reputation/reciprocity cannot compound
- This also tests opponent sophistication—only naive cooperators will be exploited

## EDGE CASES & ROBUSTNESS

**Heterogeneous Opponents:**
- The metric-based threshold system is agnostic to opponent strategy type
- Works against TFT (tit-for-tat), Always-D, Always-C, and probabilistic strategies
- Adapts within-round based on emergent group behavior

**Instability & Oscillation Prevention:**
- If contributions fluctuate around threshold boundaries, the 0.40-0.75 band includes a "sustain cooperation" zone that dampens oscillation
- This prevents whipsaw cycles of mutual defection and encourages stabilization

**Tournament Context:**
- The final-round defection is transparent and honest; opponents will recognize it
- Early-round cooperation signals that defection is strategic, not unconditional weakness
- Thresholds are calibrated to punish systematic free-riders while rewarding genuine cooperators

## COLLECTIVE ALIGNMENT

This strategy prioritizes **group payoff when sustainable** while maintaining **individual self-protection** when collective cooperation breaks down. It treats the game as fundamentally about discovering whether a collaborative equilibrium exists with this particular group, and executes accordingly:

- Contributes when others demonstrate commitment
- Withdraws when exploitation becomes dominant
- Does not blame or punish—only responds to aggregate behavior
- Transparent enough that rational opponents can recognize the incentive structure and align

The strategy is **collectively rational** because it maximizes the likelihood of reaching a high-welfare outcome *if possible*, rather than defecting unilaterally and destroying cooperation prematurely.
'''

description_COLLECTIVE_69 = '''
# COLLECTIVE STRATEGY FOR PUBLIC GOODS GAME

## CORE PRINCIPLE
Maximize long-term collective welfare through conditional cooperation that gracefully degrades when faced with defection, while maintaining sufficient individual rationality to avoid exploitation.

## DECISION RULES

### STANDARD ROUND (not first, not last)
**Cooperate if and only if:**
- The average contribution rate in the previous round was ≥ threshold(round)
- Where threshold(round) = max(0.5, 1 - round/r)
  - This starts at 50% cooperation required and gradually increases to 100% as the game nears its end
  - Rationale: Early leniency encourages cooperation building; late strictness prevents last-round defection spirals

**Otherwise: Defect**

### FIRST ROUND
**Always cooperate**
- Rationale: Establish pro-social baseline without information bias. Signal willingness to contribute. The first round is an investment in learning opponent types.

### LAST ROUND
**Defect** (unless average contribution rate across all previous rounds was ≥ 0.9)
- Rationale: Last round incentives are purely individual. Only cooperate if the group demonstrated exceptionally strong cooperation discipline throughout.
- Exception: If the community proved nearly universal cooperation, reward it.

### RECOVERY LOGIC
If the group fell below threshold but then recovers:
- Immediately resume cooperation after one round of observed recovery
- This creates a "trust restoration window" rather than permanent punishment
- Rationale: Collective welfare requires second chances; permanent defection locks in mutual punishment equilibrium

## EDGE CASES

**Unanimous Defection Observed:**
- If all players defected last round, defect this round
- Expect to remain in defection equilibrium, but don't escalate the harm
- Do not punish harder than the environment already does

**You Are Alone Contributing:**
- If your individual contribution was the only one last round:
  - Defect this round (collective welfare is already abandoned)
  - Resume cooperation only if ≥2 others contribute next round
  - Rationale: Don't be systematically exploited; require evidence of group shift

**Very Small Groups (n ≤ 3):**
- Increase threshold by +0.15 (higher bar for cooperation)
- Rationale: Individual defection is more impactful; require stronger proof of reciprocation

**Volatile Groups:**
- If contribution rate variance is very high (swinging >0.4 each round):
  - Use a 2-round rolling average instead of single previous round
  - Rationale: Smooth out noise; avoid tit-for-tat thrashing

## COLLECTIVE ALIGNMENT

This strategy embodies collective thinking by:

1. **Prioritizing group welfare when sustainable:** Cooperation requires demonstrable reciprocation from others, not blind hope

2. **Graceful degradation:** Rather than binary punishment, it decreases cooperation probabilistically with defection rates, allowing recovery

3. **Explicit sacrifice in early rounds:** The first-round universal cooperation is a collective gift that tests whether others share pro-social values

4. **Threshold adaptation:** Higher thresholds late in the game prevent the last-round defection cascade that destroys collective outcomes

5. **Recognizing information asymmetry:** By conditioning on observed behavior only, the strategy avoids assuming shared norms while still rewarding demonstrable cooperation

## SUMMARY TABLE

| Situation | Action | Rationale |
|-----------|--------|-----------|
| Round 1 | Cooperate | Signal pro-social intent |
| Avg contribution ≥ threshold | Cooperate | Reciprocate cooperation |
| Avg contribution < threshold | Defect | Avoid exploitation |
| Previous round unanimous defection | Defect | Collective welfare abandoned |
| Last round (unless 0.9+ avg) | Defect | Individual incentives dominate |
| Recovery detected | Cooperate next | Allow redemption |
'''

description_COLLECTIVE_70 = '''
# ADAPTIVE COLLECTIVE STRATEGY FOR PUBLIC GOODS GAME

## CORE PRINCIPLE
Maximize collective welfare by encouraging cooperation while protecting against free-riding through reputation-based reciprocity. Balance optimism about cooperation with pragmatic defection against persistent defectors.

## DECISION RULES

### CONTRIBUTION DECISION
Contribute (C) if and only if:
1. **Cooperation Rate Threshold**: The historical cooperation rate across all players ≥ (k-1)/k
   - This reflects the break-even point where cooperation becomes individually rational
   - Adjust dynamically: increase threshold by 5% per defector, decrease by 5% per cooperator in last round

2. **Individual Track Record**: The opponent with the lowest historical contribution rate has contributed in at least 1 of the last 3 rounds (showing some willingness)
   - If any player has defected in ALL observed rounds, defect
   - This prevents exploitation by coordinated free-riders

3. **Recency Weight**: Recent rounds (last 3) receive 2x weight in cooperation assessment
   - Allows strategy to adapt to shifting behaviors quickly
   - Sudden defection streaks trigger rapid defection response

### DEFECT (D) conditions (contribute 0):
- If cooperation rate drops below (k-1)/k threshold
- If any single player has >80% defection rate historically
- If the last round showed cooperation rate declining compared to the previous 3 rounds

## EDGE CASES & SPECIAL ROUNDS

### ROUND 1 (First Round)
**COOPERATE** unconditionally
- Rationale: Maximize information gathering and signal cooperative intent without risking against known defectors
- Collective assumption: most players will attempt some cooperation initially

### ROUNDS 2-3 (Early Game)
**COOPERATE** if round 1 shows ≥50% cooperation across all players
- Lenient threshold to allow cooperation to bootstrap
- If round 1 cooperation <50%, switch to defect-unless-majority-cooperates rule

### FINAL ROUND (Last Round, Round r)
**DEFECT** unconditionally
- Standard end-game collapse reasoning: no future reputation cost
- Exception: If cooperation rate in round r-1 was ≥90% AND all players contributed in round r-1, then COOPERATE to preserve collective gain in final moment

### MID-GAME CRISIS (Cooperation drops >20% in one round)
- Trigger a "test round": Cooperate once more to see if the decline was temporary
- If cooperation doesn't recover in next round, adopt strict defection until cooperation recovers above (k-1)/k

## ROBUSTNESS MECHANISMS

**Against Free-Riders**: Track individual defection patterns. Three consecutive defections by any player triggers individual-specific defection (you defect regardless of group rate until they cooperate again).

**Against Coordinated Defectors**: If >n/2 players show synchronized defection (same round switches), assume coordination and defect until >70% return to cooperation.

**Against Noise/Mistakes**: Require defection patterns to persist for 2+ consecutive rounds before responding, allowing single-round mistakes to be forgiven.

**Against Mixed Strategies**: If observing erratic behavior (cooperation alternates unpredictably), fall back to cooperation rate threshold rule exclusively—don't try to model intentions.

## SUMMARY
- **Optimistic opening**: Cooperate round 1
- **Adaptive middle game**: Follow (k-1)/k breakeven threshold with recency weighting
- **Punish persistently**: Individual defectors face immediate defection
- **Pessimistic ending**: Defect in final round except under overwhelming cooperation
- **Collective focus**: Prioritize group welfare metrics over individual payoff maximization

This strategy seeks to establish and sustain cooperation when viable, exits gracefully when defection dominates, and avoids being exploited by tracking both group and individual histories.
'''

description_COLLECTIVE_71 = '''
# ADAPTIVE CONDITIONAL COOPERATION WITH STRATEGIC DEFECTION

## CORE STRATEGY: GENEROUS TIT-FOR-TAT WITH THRESHOLD MONITORING

### PRIMARY DECISION RULE (Rounds 1 through r-1)

**Cooperate** if and only if:
- The average contribution rate across all players in the previous round is ≥ (k-1)/k
- OR this is round 1 (unconditional first-round cooperation)

**Defect** otherwise.

**Rationale**: The threshold (k-1)/k is the break-even point where contributing becomes rational. If most players exceed this threshold, the public good multiplier justifies individual contribution costs.

---

### LAST ROUND HANDLING (Round r)

**Defect unconditionally** in the final round.

**Rationale**: With no future rounds, there is no shadow of the future to sustain reciprocity. Any player defecting in round r gains one token with zero reputational cost. Anticipating this, rational players will defect in round r-1, collapsing cooperation. We defect in round r to avoid being exploited.

---

### EDGE CASES & REFINEMENTS

**Unanimous Defection**: If all players defected in round t (contribution rate = 0), continue defecting in round t+1. This recognizes that cooperation has collapsed and signals we will not unilaterally restart it. Return to cooperation only if we observe a contribution rate ≥ (k-1)/k in any subsequent round.

**Round 2 Special Case**: If cooperation failed to materialize in round 1 (contribution rate < (k-1)/k), give one additional round of defection in round 2 before reconsidering. This avoids hair-trigger reciprocation of noise or initial exploration.

**Gradual Threshold Adjustment (Optional Enhancement)**: In rounds 3 onward, if the contribution rate is (k-1)/k ± 10%, interpret this as "emerging cooperation" and contribute. This smooths the decision boundary and reduces brittleness.

---

## WHY THIS STRATEGY IS COLLECTIVE

1. **Reciprocal Benefit**: By cooperating when others do, we enable mutual gains from the multiplier effect. When the average contribution exceeds break-even, everyone is better off cooperating than defecting.

2. **Punishment of Defection**: Defecting when others defect pins the social outcome at the Nash equilibrium (no waste of contribution-making when it won't be rewarded).

3. **Robustness**: This strategy works against:
   - **Cooperators**: Matches their behavior and earns gains from k > 1
   - **Defectors**: Switches to defection, avoiding one-sided exploitation
   - **Mixed strategies**: Responds to the aggregate signal (average contribution rate), which is less noisy than any single player's action

4. **Simplicity**: The rule is transparent and learnable by other players, which may induce reciprocal cooperation even without explicit communication.

---

## TOURNAMENT RESILIENCE

- **Against pure defectors**: We defect too, minimizing losses
- **Against pure cooperators**: We cooperate and earn mutual gains
- **Against mixed/adaptive strategies**: Our threshold rule adapts to emergent cooperation rates, making us neither exploitable nor stubborn
- **Endgame collapse**: We defect in round r, preventing exploitation by strategies that defect late
'''

description_COLLECTIVE_72 = '''
# ADAPTIVE CONTRIBUTION STRATEGY FOR PUBLIC GOODS GAMES

## CORE PHILOSOPHY
Maximize collective welfare while remaining robust to exploitation. Assume other players are self-interested but potentially reciprocal. Cooperate conditiously based on demonstrated group behavior, not trust.

## STRATEGY COMPONENTS

### 1. INITIAL ROUND (Round 1)
**Action: CONTRIBUTE (C)**

Rationale: The first round is an information-gathering move with minimal cost. Contributing signals conditional cooperation and generates data about opponent types. The collective benefit of universal contribution (if it happens) vastly exceeds individual defection gains.

### 2. ROUNDS 2 THROUGH (r-2) — ADAPTIVE RECIPROCAL STRATEGY

Calculate the **group cooperation rate** after each completed round:
- cooperation_rate = (total contributors in previous round) / n

**Decision rule:**
- **If cooperation_rate ≥ threshold_high (e.g., 0.6):** CONTRIBUTE
  - The group is sustaining meaningful cooperation. Reciprocate to reinforce it.
  
- **If cooperation_rate < threshold_low (e.g., 0.3):** DEFECT
  - Defection is widespread. Contributing becomes irrational. Protect endowment.
  
- **If threshold_low ≤ cooperation_rate < threshold_high (gray zone):** CONTRIBUTE IF (cooperation_rate > 0.5), else DEFECT
  - Use the midpoint as a tipping point. Optimistically contribute when cooperation edges toward majority.

**Adaptive refinement:**
- Track the **trend**: Is cooperation_rate increasing or decreasing across the last 2-3 rounds?
- If trend is **improving**, lower threshold_high by 0.05 (be more generous).
- If trend is **deteriorating**, raise threshold_low by 0.05 (be more conservative).
- This allows the strategy to exploit emerging cooperation and exit dying commons.

### 3. FINAL ROUND (Round r)
**Action: DEFECT (D)**

Rationale: No future rounds mean no opportunity for reciprocal punishment or reward from other players. Defecting recovers 1 token with zero reputational cost. The collective game ends; individual incentives dominate rationally.

*Exception:* If cooperation_rate in round (r-1) was ≥ 0.9 and showed sustained high cooperation, consider CONTRIBUTING in the final round. This rewards genuinely cooperative groups and signals that you were a genuine cooperator, not a pure self-interest player. (This is optional; pure defection is also strategically sound.)

### 4. HANDLING INDIVIDUAL DEVIATIONS

After round t, if a specific player j defected while cooperation_rate was high:
- **Do not punish via future defection** (no punishment mechanism exists).
- Instead, **lower your future contribution likelihood slightly** if you observe repeated defection from the same player, weighted by how many high-cooperation rounds they abandoned.
- This is implicit: if one player consistently free-rides while others contribute, the group cooperation_rate falls, triggering your DEFECT response anyway.

---

## EDGE CASES & REFINEMENTS

### Case: n is very large
- Threshold values should increase slightly (0.6 → 0.65), since individual contributions have minimal impact on payoff. Demand higher group cooperation to justify contributing.

### Case: k is close to 1
- Contributions barely generate collective returns. Shift to threshold values of (0.8, 0.5)—require very high group cooperation to justify contributing.

### Case: k is close to n
- Strong multiplier rewards cooperation. Lower thresholds to (0.5, 0.2)—cooperate more aggressively to unlock collective gains.

### Case: Very short game (r < 5)
- Rounds 2 and (r-1) coincide. Always CONTRIBUTE in round 2; always DEFECT in round r. Treat intermediate rounds as above if they exist.

---

## SUMMARY TABLE

| Round | Cooperation Rate | Action |
|-------|------------------|--------|
| 1 | N/A | C |
| 2 to (r-2) | ≥ 0.6 (adjusted) | C |
| 2 to (r-2) | 0.3–0.6 (adjusted) | C if > 0.5, else D |
| 2 to (r-2) | < 0.3 (adjusted) | D |
| r | Any | D (or C if ≥ 0.9 prior round) |

---

## COLLECTIVE ALIGNMENT

This strategy **maximizes expected collective payoff** by:
1. Testing and rewarding cooperation early
2. Sustaining contributions as long as group behavior justifies it
3. Gracefully degrading when the commons collapses
4. Avoiding wasteful defection in environments that support contribution

It remains **robust** because it adapts to actual group behavior rather than assuming shared norms.
'''

description_COLLECTIVE_73 = '''
# COLLECTIVE STRATEGY FOR PUBLIC GOODS GAME

## CORE PRINCIPLE
Maximize collective welfare by promoting sustainable cooperation, while maintaining individual rationality and robustness against exploitation.

## DECISION RULE: ADAPTIVE THRESHOLD COOPERATION

**Primary Rule:**
- **Cooperate (C)** if the observed cooperation rate in the previous round met or exceeded a dynamic threshold
- **Defect (D)** if cooperation fell below the threshold
- **Round 1:** Cooperate (establish cooperative intent and gather information)

**Dynamic Threshold Calculation:**
The threshold adjusts based on game parameters and observed cooperation:
- Calculate minimum viable cooperation: `threshold = (n - k) / (n - 1)`
  - This is the cooperation level where contributing becomes rational for the marginal player
  - When k=2, n=5: threshold ≈ 0.75 (3 of 4 others must cooperate)
  - When k=4, n=5: threshold ≈ 0.25 (1 of 4 others must cooperate)

- If recent cooperation rate ≥ threshold: maintain cooperation in next round
- If recent cooperation rate < threshold: switch to defection for one round, then attempt to rebuild

## HANDLING EDGE CASES

**Last Round (round r):**
- Defect. The folk theorem doesn't apply here—no future consequences exist. Cooperating in the final round is pure loss.

**Rounds 2 through r-1 (middle game):**
- Apply the adaptive threshold rule strictly
- Track a 2-round rolling average of cooperation rates to smooth noise from single-round defection attempts

**Early deterioration (rounds 2-3):**
- If cooperation collapses immediately, defect once, then attempt one "reconciliation" offer of cooperation in the following round to test whether opponents can coordinate back to cooperation
- If they don't reciprocate, resign to defection for the remaining game

## ROBUSTNESS MECHANISMS

**Against free-riders:**
- Defection triggers immediately when cooperation drops below threshold
- This prevents exploitation while maintaining willingness to rebuild if others reciprocate

**Against noise/mistakes:**
- Use rolling averages (2-round window) rather than single-round reactions
- Allow one-round reconciliation attempts to distinguish random defection from intentional betrayal

**Against mixed strategies:**
- Track individual contributions if possible, but primarily respond to aggregate cooperation rates
- This prevents targeting specific players while still detecting systematic free-riding

## COLLECTIVE ALIGNMENT

This strategy is **collectively optimal** because:
1. It enforces sustainable equilibrium: cooperation persists if others cooperate
2. It punishes defection immediately and proportionally (via defection), aligning individual incentives with group welfare
3. It never exploits—defection is reactive, not opportunistic
4. It maximizes expected payoffs for all players *when played symmetrically* while remaining rational against any opponent

The strategy is self-enforcing: if all players adopt it, cooperation emerges as the stable outcome for all rounds except the last.
'''

description_COLLECTIVE_74 = '''
# ADAPTIVE COLLECTIVE CONTRIBUTION STRATEGY

## CORE PRINCIPLE
Maximize collective welfare by conditioning contributions on demonstrable group cooperation, while maintaining individual resilience against exploitation.

## DECISION RULE (GENERAL CASE)

**Contribution Threshold Framework:**
- Calculate the empirical cooperation rate: `coop_rate = (total contributions in past rounds) / (n × rounds played)`
- Contribute if and only if: `coop_rate ≥ threshold(round_number)`

**Dynamic Threshold:**
- Rounds 1-3: `threshold = 0.5` (give cooperation a fair chance early)
- Rounds 4 onwards: `threshold = 0.4` (slightly forgiving, but enforce discipline)
- Final round: `threshold = 0.3` (last-round cooperation attempt, very permissive)

This creates a "prove cooperation first" dynamic while remaining realistic about imperfect groups.

## EDGE CASES & SPECIAL HANDLING

**Round 1 (No History):**
- Contribute. Establish a cooperative signal and gather initial information about the group's disposition.

**Identified Free-Riders:**
- Track individual contribution patterns. If any single player has defected in 3+ consecutive rounds while others cooperate, prepare to defect in response (shift threshold up by 0.1) to limit exploitation.

**Collapse Detection:**
- If cooperation rate drops below 0.2 in any round, switch to a "tit-for-tat majority" rule: contribute only if more than 50% of players contributed in the immediately preceding round.

**Final 2 Rounds:**
- Relax threshold to 0.25. Attempt to salvage collective gains even if the group has been mediocre. Avoid the mutual defection spiral that often emerges at the end.

## ROBUSTNESS MECHANISMS

1. **Forgiving but Not Naive:** Accept temporary dips in cooperation (one bad round doesn't trigger defection), but punish sustained free-riding.

2. **Proportional Response:** If cooperation is between 0.3 and 0.5, contribute with probability equal to the observed coop_rate (probabilistic contribution softens punishment and leaves room for recovery).

3. **Coalition Awareness:** If multiple players show synchronized defection in a round, treat it as a coordinated attack rather than random noise—escalate threshold more aggressively.

## ALIGNMENT WITH COLLECTIVE WELFARE

This strategy prioritizes **group payoff maximization** by:
- Seeding cooperation early to establish group norms
- Punishing free-riding without overreacting to noise
- Remaining willing to cooperate if others demonstrate commitment
- Avoiding mutual defection traps through strategic leniency in final rounds

It balances collective welfare against exploitation by conditioning on observed reciprocity, not blind trust.
'''

description_COLLECTIVE_75 = '''
# ADAPTIVE COLLECTIVE STRATEGY FOR PUBLIC GOODS GAMES

## CORE PHILOSOPHY
This strategy balances reciprocal cooperation with strategic defection, prioritizing collective welfare while remaining robust against exploitation. It treats the game as a dynamic system where trust is earned through demonstrated commitment to mutual benefit.

## PRIMARY DECISION RULE: CONDITIONAL CONTRIBUTION

**Contribute (C) if and only if:**
1. The historical contribution rate across all players in the previous round exceeds a dynamic threshold, OR
2. We are in the first round (bootstrap cooperation), OR
3. The collective payoff trend is improving despite recent mixed contributions

**Defect (D) otherwise**, with rare exceptions for reputation repair.

### Dynamic Threshold Calculation
- **Rounds 1-2:** Contribute unconditionally (assume good faith)
- **Rounds 3 onward:** Calculate average contribution rate from previous round
  - If avg_contribution_rate ≥ (k-1)/n, contribute
  - If avg_contribution_rate < (k-1)/n, defect (threshold reflects the break-even point where collective welfare improves)
  
This threshold is derived from the multiplier k: if fewer than (k-1) out of n players contribute, the marginal return to the pool is negative for contributors.

## EDGE CASE HANDLING

**First Round:** Contribute. This signals cooperative intent and generates data about opponent types without exposing ourselves to extended exploitation.

**Last Round (if r is known):** Defect. With no future shadow of the future, standard game theory predicts defection. However, this is conditional: if contribution rate has remained ≥80% throughout, contribute in the final round as a "goodwill closure" to reinforce norms (this may influence post-game reputation or affect social utility).

**Identifying Free-Riders:** Track individual contribution patterns. If any player contributes <20% of rounds, treat them as systematic defectors and apply stricter thresholds.

**Identifying Reciprocal Partners:** If a player contributes ≥80% of rounds, weight their past and expected behavior more heavily in future decisions.

## COLLECTIVE ALIGNMENT

This strategy is collective because:

1. **Threshold reflects mutual benefit:** The (k-1)/n threshold ensures we only cooperate when the pooled outcome is genuinely better than individual outcomes. This maximizes total welfare.

2. **Promotes coordination without explicit signaling:** By following a transparent rule (contribute when others do), we create a self-reinforcing equilibrium. Players with similar logic converge on cooperation.

3. **Penalizes exploitation:** Systematic defectors cause the average contribution rate to drop, triggering our defection. This creates a cost for free-riding without requiring punishment mechanisms.

4. **Adaptive learning:** The strategy continuously updates based on observed behavior, allowing it to distinguish between good-faith players and exploiters.

## ROBUSTNESS GUARANTEES

- **Against always-defect opponents:** We defect after round 2, limiting exposure to one round of being fully exploited.
- **Against always-cooperate opponents:** We cooperate as long as the threshold is met, capturing mutual gains.
- **Against tit-for-tat variants:** Our conditional rule creates a stable cooperation basin: if enough players use similar logic, everyone cooperates, sustaining high payoffs.
- **Against random players:** The averaging effect of repeated rounds means noise is smoothed, and our threshold remains robust.

## DECISION PSEUDOCODE

```
if round == 1:
    CONTRIBUTE
else if round == r AND contribution_rate_history < 0.8:
    DEFECT
else if round == r AND contribution_rate_history >= 0.8:
    CONTRIBUTE
else:
    prev_avg_contribution = average_contributions_last_round
    threshold = (k - 1) / n
    if prev_avg_contribution >= threshold:
        CONTRIBUTE
    else:
        DEFECT
```

This strategy prioritizes collective surplus while remaining self-protective against exploitation—achieving both robustness and alignment with group welfare.
'''

description_COLLECTIVE_76 = '''
# COLLECTIVE STRATEGY FOR PUBLIC GOODS GAME

## CORE PRINCIPLE
Maximize group welfare through **conditional cooperation with adaptive defection thresholds**, recognizing that we cannot assume pre-coordination but can respond to revealed preferences through observable history.

## DECISION RULES

### Round 1 (Opening Move)
**Contribute (C)**.
- Establishes cooperative intent without cost assumptions
- Tests whether the group has baseline pro-social orientation
- Sets a cooperative anchor for reputation

### Rounds 2 through (r-1) (Cooperative Phase)
**Implement Tit-for-Tat with Generosity on Contribution Rates:**

1. Calculate the **group contribution rate** in the previous round:
   - contrib_rate = (total_contributions_previous_round) / n

2. Decision rule:
   - If contrib_rate ≥ 0.5: **Contribute (C)**
     - The group is maintaining reasonable cooperation; reinforce it
   - If 0.2 < contrib_rate < 0.5: **Contribute (C)** with 75% probability
     - Attempt to salvage cooperation with deliberate generosity
     - Accept some defection losses to maintain collective gains
   - If contrib_rate ≤ 0.2: **Defect (D)**
     - The group has collapsed; protect individual payoff
     - Continued contribution becomes individually irrational

### Round r (Final Round)
**Defect (D)**.
- Last-round defection is unavoidable in standard PGG (no future reputation consequences)
- Attempting cooperation here signals weakness to pure defectors
- The only rational move is to secure the non-cooperative payoff

## EDGE CASES & REFINEMENTS

**If any single player consistently deviates:**
- Do not adjust strategy based on individual outliers
- Respond only to aggregate group behavior (contribution rate)
- This prevents exploitation by a single free-rider while maintaining collective focus

**If contribution rate fluctuates around the 0.5 threshold:**
- Default to **Contribute (C)** when in doubt
- The cost of excessive pessimism (abandoning cooperation) exceeds the cost of being exploited once or twice
- Maintain threshold stability to avoid chaotic oscillation

**If the game is explicitly finite but exact length unknown:**
- Treat each round as if it's not terminal until confirmed
- Do not deploy round-r defection strategy until the final round is announced

## COLLECTIVE ALIGNMENT

This strategy prioritizes **group surplus over individual advantage**:
- It sustains cooperation when the group validates cooperation (contrib_rate ≥ 0.5)
- It tolerates moderate free-riding (0.2 < contrib_rate < 0.5) by contributing with high probability, sacrificing individual gain for collective resilience
- It only defects when the group has clearly abandoned collective welfare (contrib_rate ≤ 0.2)
- It abandons cooperation only in the final round, where individual incentives dominate

**Robustness:** This strategy works against:
- Pure cooperators (mutual cooperation)
- Rational defectors (cascades to mutual defection, minimizing loss)
- Mixed strategies (adapts via contribution rate threshold)
- Noisy/random players (aggregate rate averaging smooths noise)
'''

description_COLLECTIVE_77 = '''
# COLLECTIVE STRATEGY FOR PUBLIC GOODS GAME

## CORE PRINCIPLE
Maximize collective welfare by identifying and reinforcing cooperative clusters while minimizing losses to free-riders. This strategy balances aspiration (achieving above-average outcomes) with reciprocity (rewarding cooperation among peers).

## DECISION RULES

### Primary Rule: Conditional Contribution Based on Collective Health
- **Calculate the "cooperation ratio"** at the start of each round: (total contributions in previous round) / n
- **Calculate the "collective payoff"** in the previous round: average payoff across all players
- **Contribute (C) if:**
  - Round 1: CONTRIBUTE (establish baseline cooperation)
  - Cooperation ratio ≥ 0.5 AND collective payoff is increasing or stable, OR
  - Your last-round payoff was below average AND you contributed (you were punished for cooperation; double down to signal commitment)
  
- **Defect (D) if:**
  - Cooperation ratio < 0.3 (defection dominates; protect yourself)
  - Cooperation ratio ≥ 0.3 but < 0.5 AND collective payoff declined (cooperation is eroding)
  - You contributed last round but payoff was below average AND cooperation ratio fell by >0.2 (signal that cooperation failed)

### Secondary Rule: Decay-Based Adjustment
- Track the **trend in cooperation ratio** over the last 3 rounds
- If cooperation is rising steadily, increase contribution probability slightly (reinforce momentum)
- If cooperation is falling, defect more aggressively (exit before further losses)

### Tertiary Rule: Last Round Adaptation
- In the **final round**, defect unconditionally (no future reciprocal interaction possible; maximize individual payoff)
- **Exception:** If cooperation ratio in round (r-1) was ≥ 0.7, contribute in round r to maintain group cohesion (signal you're not purely selfish)

## EDGE CASES & SPECIAL SCENARIOS

**Extreme Low Cooperation (ratio ≈ 0):**
- Defect for 2 consecutive rounds to absorb the cost
- Then attempt one contribution as a "probe" to see if others reciprocate
- If probe fails, resume defection

**Extreme High Cooperation (ratio ≈ 1):**
- Maintain contribution throughout
- This is the optimal state; protect it

**Mid-Game Oscillation (ratio fluctuates 0.4–0.6):**
- Use a "cautious matching" heuristic: contribute if ≥50% of players contributed last round, defect otherwise
- This reduces over-investment in unstable equilibria

**Isolated Punishment:**
- If you were the only defector last round and collective payoff dropped sharply, contribute next round (accept responsibility and signal reform)
- If you were among many defectors, continue defecting (individual action is meaningless; wait for cooperative signals from others)

## COLLECTIVE ALIGNMENT

**Why this maximizes collective welfare:**
1. **Efficiency**: By conditioning on cooperation ratio, the strategy avoids wasteful investment in groups trending toward defection
2. **Stability**: The decay-based adjustment prevents false hope—if cooperation is collapsing, exit early rather than suffer repeated losses
3. **Resilience**: The "probe" mechanism in low-cooperation environments offers recovery pathways without guaranteeing exploitation
4. **Fairness**: Reciprocating others' contributions creates a norm of mutual obligation; defecting against defectors removes incentive for ongoing free-riding

**How it handles adversarial opponents:**
- Against pure defectors: Match defection and minimize losses
- Against exploitative cooperators (those who punish contributors): Cease contribution and defect
- Against genuine cooperators: Reinforce with sustained contribution
- Against mixed strategies: The cooperation ratio captures aggregate behavior; no single opponent can manipulate the strategy through hidden signaling

## SUMMARY
**Contribute when cooperation ≥50% and rising, or when you're signaling commitment. Defect when cooperation collapses, in the final round (except under extreme coordination), or to exit losing situations. Always track collective payoff trends, not just contribution counts.**
'''

description_COLLECTIVE_78 = '''
# ADAPTIVE CONDITIONAL COOPERATION WITH DEFENSIVE DEFECTION

## CORE DECISION RULE

**Cooperate if and only if the empirical cooperation rate in the previous round meets or exceeds a dynamic threshold. Otherwise, defect.**

Threshold(round t) = max(0.5, recent_avg_cooperation_rate - 0.15)

- In round 1, cooperate (establish baseline reciprocity)
- In rounds 2 through r-1, apply the threshold rule above
- In the final round, defect (no future reciprocation possible)

## RATIONALE FOR COMPONENTS

**Empirical cooperation threshold:**
The strategy monitors what others actually do rather than assuming trustworthiness. By conditioning on observed behavior, it adapts to the specific group composition without requiring communication or prior agreement.

**Dynamic threshold with decay:**
The threshold isn't fixed—it decays from the cooperation floor of 50% by subtracting 0.15 each round. This creates a "grace period" where the group can sustain cooperation even if participation gradually erodes, while still punishing systematic free-riding. If cooperation was near 100%, the threshold stays high. If it drops to 40%, we only require 25% cooperation to keep trying.

**Minimum floor of 50%:**
We don't demand perfection. Requiring merely a majority to have cooperated acknowledges that some defection is inevitable without punishment institutions. This keeps the strategy stable against occasional defectors while avoiding a "race to the bottom."

**First round cooperation:**
This seeds the cooperative equilibrium. Since everyone receives zero information before round 1, unilateral cooperation is a reasonable signal that cooperation is possible.

**Last round defection:**
There is no shadow of the future in the final round. Any cooperation then is purely altruistic, which no adaptive strategy should assume. Defecting in round r is strategically sound.

## EDGE CASES & ROBUSTNESS

**Unanimous defection observed:**
If cooperation_rate = 0 in any round, defect for all remaining rounds. (The threshold becomes -0.15, but we cap at 0.5, so we require 50% cooperation. Zero is below 50%, so defect.)

**Mixed group (some cooperators, some defectors):**
The strategy remains in the middle. If 60% cooperate, threshold is 60%, we cooperate next. If 40% cooperate, threshold is 25%, we cooperate next. This creates a stable attractor where sustained defection drops below the threshold and triggers defection, while sustained cooperation stays above it.

**Extreme free-riders (k << n):**
When the multiplier is low, the returns to cooperation are poor anyway. The strategy still attempts conditional cooperation early to test the environment, but will abandon it faster as empirical rates drop below the threshold.

**Extreme multipliers (k close to n):**
High returns favor cooperation more. The threshold mechanism still works—it will require sustained cooperation to remain above 50%, which is realistic when incentives are aligned.

## ALIGNMENT WITH COLLECTIVE OBJECTIVE

This strategy prioritizes group welfare by:
1. **Initiating reciprocity** rather than starting with defection
2. **Rewarding collective effort** through continued cooperation when others cooperate
3. **Punishing systematic defection** by withdrawing cooperation when the group cooperation rate drops
4. **Avoiding coordinated collapse** by maintaining a floor of 50% required cooperation, preventing premature races to the bottom

The strategy does not require trust in others' intentions—only in observable behavior. It scales to groups of any size and works regardless of whether other players are selfish, altruistic, or reciprocal, because it only responds to empirical facts.
'''

description_COLLECTIVE_79 = '''
# COLLECTIVE STRATEGY FOR PUBLIC GOODS GAME

## CORE PHILOSOPHY
This strategy prioritizes **sustained collective welfare** while remaining robust to free-riding. It operates on the principle that cooperation is valuable, but must be conditionally maintained based on observed reciprocity.

## DECISION RULE: ADAPTIVE CONDITIONAL COOPERATION

**Primary Logic:**
- Cooperate if the observed cooperation rate in the previous round meets or exceeds a dynamic threshold
- Defect if cooperation falls below threshold (to avoid being exploited)
- Adjust the threshold based on game structure and position in the time horizon

**Threshold Calculation:**
```
threshold = (1/k) + epsilon
where epsilon = 0.15 (15% tolerance buffer)
```

This threshold is informed by the payoff structure: when k < n (the standard multiplier constraint), cooperation only becomes individually rational when most others cooperate. The buffer allows for noise and exploration.

## ROUND-BY-ROUND BEHAVIOR

**Round 1 (Initialization):**
- COOPERATE
- Rationale: Start optimistically to establish cooperative baseline; signal willingness to contribute to collective good

**Rounds 2 to (r-2) (Bulk of Game):**
- Measure: Calculate cooperation_rate = (total cooperators in round t-1) / n
- IF cooperation_rate ≥ threshold: COOPERATE
- IF cooperation_rate < threshold: DEFECT
- Rationale: Conditional cooperation creates incentive for others to maintain collective participation while protecting against systematic free-riding

**Rounds (r-1) to r (End Game):**
- Slightly elevate threshold by +0.10
- IF cooperation_rate ≥ (threshold + 0.10): COOPERATE
- ELSE: DEFECT
- Rationale: As rounds diminish, defection incentives increase. This conservative approach protects against last-round exploitation while still rewarding genuinely cooperative groups

## EDGE CASES & ROBUSTNESS

**Unanimous Defection (cooperation_rate = 0):**
- DEFECT unconditionally
- Rationale: No collective good exists to contribute toward

**Unanimous Cooperation (cooperation_rate = 1.0):**
- COOPERATE
- Rationale: Sustain the cooperative equilibrium that maximizes collective welfare

**Mixed Behavior (0 < cooperation_rate < threshold):**
- DEFECT
- Rationale: The group has crossed into a threshold where free-riding pays more than marginal collective benefit
- Recovery: If cooperation spontaneously rises back above threshold, resume cooperation immediately

**Self-Awareness:**
- Track own historical compliance: This rule applies equally to all players
- If you would defect under your own rules, recognize that others following similar logic will also defect
- This creates a corrective feedback mechanism

## COLLECTIVE ALIGNMENT

This strategy reflects collective welfare by:

1. **Initiating cooperation** as a default, giving groups the opportunity to reach Pareto-superior equilibria
2. **Protecting the collective** by withdrawing when others systematically free-ride, preventing complete exploitation
3. **Maintaining flexibility** to rejoin cooperation if the group shows genuine commitment
4. **Reducing cascading defection** by using a threshold rather than immediate tit-for-tat, allowing for occasional non-compliance without spiraling collapse

The strategy balances **optimism with pragmatism**—it will not sacrifice the collective to pure altruism, but it won't abandon cooperation prematurely either.
'''

description_COLLECTIVE_80 = '''
# ADAPTIVE COLLECTIVE STRATEGY FOR PUBLIC GOODS GAME

## CORE PRINCIPLE
Maximize collective welfare through conditional cooperation that punishes defection while remaining resilient to exploitation. The strategy treats the group as an extended self, rewarding mutual contribution and constraining individual defection.

## DECISION RULES

### PRIMARY RULE: Contribution Threshold Cooperation
- **Cooperate (C)** if and only if the proportion of cooperators in the previous round meets or exceeds a dynamic threshold
- **Defect (D)** otherwise, to conserve resources and signal non-compliance with low-cooperation equilibria

### THRESHOLD CALCULATION
```
threshold(round) = max(0.5, 1 - (round / total_rounds) * 0.3)
```

This threshold:
- Starts at 50% (require half the group to cooperate)
- Gradually decreases toward 70% as the game progresses (incentivizing late-game contributions)
- Never falls below 70% to maintain discipline against systematic defectors

### COOPERATION HISTORY TRACKING
Maintain a rolling assessment of each opponent:
- **Reliable cooperators**: Consistently choose C across rounds
- **Conditional defectors**: Defect when cooperation falls below a threshold
- **Free riders**: Systematically choose D or defect when others cooperate

## EDGE CASES

### ROUND 1 (No History)
**Cooperate unconditionally.** This serves as a prosocial signal and establishes a cooperative baseline. It tests whether the group has cooperative capacity.

### ROUNDS 2-N (Middle Game)
Apply the threshold rule strictly. If cooperation in round t-1 ≥ threshold(t), contribute in round t. This creates a reinforcement loop where mutual cooperation stabilizes.

### FINAL ROUNDS (Last 15% of Game)
Slightly relax the threshold by 0.1 to encourage final-round cooperation despite shadow-of-the-future effects diminishing. This captures remaining cooperative surplus.

### IF THRESHOLD NEVER MET
If cooperation never reaches the threshold after round 2, shift to **tit-for-tat by group composition**: defect unless >60% of the group cooperated in the previous round. This prevents spiral into universal defection while remaining responsive.

## ROBUSTNESS MECHANISMS

### Against Free Riders
When an individual player systematically defects while others contribute, the threshold mechanism naturally punishes the group's cooperation rate, causing collective defection. This removes the free rider's benefit source.

### Against Exploiters
If cooperation temporarily spikes then crashes (exploitation attempt), the threshold drops accordingly, and you defect. Your subsequent cooperation resumes only if the group restabilizes above threshold.

### Against Noise/Uncertainty
The threshold is proportional rather than absolute—one defector in a 10-person group reduces cooperation from 100% to 90%, which likely remains above threshold. Small random defections don't trigger cascade failure.

## COLLECTIVE ALIGNMENT

This strategy prioritizes **group welfare over individual payoff maximization** by:
1. Initiating cooperation to enable collective gains
2. Conditioning continued cooperation on broad-based participation (not free riding)
3. Withdrawing support from groups that fail to reciprocate, raising the cost of defection
4. Responding proportionally to actual group behavior, not punishing minor variance

The strategy creates **emergent institutions** through repeated play: groups where others follow this logic converge to high cooperation; groups with systematic defectors naturally decrease cooperation until defection becomes unprofitable for everyone.
'''

description_COLLECTIVE_81 = '''
# ADAPTIVE COLLECTIVE STRATEGY FOR PUBLIC GOODS GAMES

## CORE PRINCIPLE
Maximize collective welfare through conditional cooperation that rewards mutual contribution while protecting against exploitation. The strategy balances optimism about collective benefit with realism about defectors.

## DECISION RULES

### Round 1 (Opening Move)
**COOPERATE**

Rationale: Start with contribution to signal willingness to cooperate and establish a cooperative baseline. This is the most informative action since no history exists yet.

### Rounds 2 through r-1 (Main Phase)

Calculate the **Collective Health Index (CHI)** based on observed history:
- CHI = (average contribution rate across all players in previous round) × 100

**Decision Logic:**

- **If CHI ≥ 60%**: COOPERATE
  - The group is cooperating sufficiently. Mutual cooperation creates positive returns for all.

- **If 40% ≤ CHI < 60%**: COOPERATE with probability equal to CHI/100, otherwise DEFECT
  - Mixed strategy that gradually reduces cooperation as the group destabilizes
  - Maintains hope for recovery while protecting against systematic exploitation

- **If CHI < 40%**: DEFECT
  - Defection is dominant when collective welfare is collapsing
  - Continuing to contribute becomes individually irrational and signals weakness to exploiters
  - Reserves tokens for self-protection

**Personal Defection Detection:**
- If you were the only contributor in the previous round (you contributed 1, all others contributed 0), immediately shift to DEFECT for at least 2 rounds
- This prevents being exploited as a sucker by a collectively defecting group

### Final Round (r)

**DEFECT**

Rationale: In the last round, there is no future relationship to maintain. Cooperation has no strategic value. Self-interest dominates since future cooperation cannot be rewarded.

Exception: If CHI ≥ 75% in round r-1, COOPERATE in round r. A highly cooperative final state suggests the group has achieved stable mutual cooperation worthy of a final contribution.

## EDGE CASES & ROBUSTNESS

**Against Free-Riders:**
- The mixed-strategy band (40-60% CHI) gradually penalizes groups where defectors proliferate
- Personal defection detection prevents individual players from being isolated targets

**Against Sudden Shifts:**
- CHI is computed fresh each round, so the strategy responds immediately to changes in group behavior
- No need for personal grudge-tracking; focus on collective trend

**Against Noise/Variance:**
- The 20-point bands (60%, 40%) create stability against single-round anomalies
- Strategy remains robust to occasional defection by otherwise-cooperative players

**In Very Small Groups (n ≤ 3):**
- k/n is large, so multiplier effects favor cooperation more strongly
- The 60% CHI threshold is still appropriate; the strategy naturally emphasizes cooperation

**In Large Groups (n > 10):**
- Defection becomes individually tempting even with high CHI
- The thresholds remain valid because CHI directly measures whether collective action is succeeding

## COLLECTIVE ALIGNMENT

This strategy:
1. **Prioritizes mutual benefit** over individual domination
2. **Responds to collective signals** rather than exploiting information asymmetries
3. **Cuts losses** when the group itself is not viable, rather than dragging down returns individually
4. **Refuses to be a sucker** while maintaining hope for recovery
5. **Ends honestly** based on group momentum, not pure self-interest

The strategy treats the public goods game as a *shared problem* where your success is intrinsically tied to others' willingness to cooperate.
'''

description_COLLECTIVE_82 = '''
# ADAPTIVE COLLECTIVE STRATEGY FOR PUBLIC GOODS GAMES

## CORE STRATEGY LOGIC

This strategy balances reciprocal cooperation with opportunistic defection detection, using history-dependent decision rules that maximize both individual security and collective welfare.

---

## DECISION RULE: CONDITIONAL CONTRIBUTION

**Contribute (C) if and only if:**
1. The observed contribution rate in the previous round ≥ threshold T, OR
2. This is round 1 (initialization phase), OR
3. Fewer than 3 rounds remain AND the cumulative game payoff suggests mutual cooperation is achievable

**Otherwise, Defect (D)**

**Threshold T = 0.5** (majority contributed in prior round)

---

## ROUND-BY-ROUND BEHAVIOR

**Round 1:**
- Contribute C
- Rationale: Establish cooperation signal; learn opponent types through their responses

**Rounds 2 to r-2 (Middle game):**
- Apply the conditional rule above
- Track each opponent's individual cooperation frequency
- If an opponent defects consistently (>70% defection rate), treat them as non-cooperative and weight their future actions less in threshold calculations

**Final 2 Rounds (r-1, r):**
- Shift strategy based on accumulated evidence:
  - If global cooperation rate has been ≥50% across game history: **Continue contributing**
  - If global cooperation rate <50%: **Switch to pure defection** (no hope of mutual gain)
  - Exception: If only 1 round remains and cooperation rate is near threshold, contribute anyway (end-game reciprocity signal)

---

## HANDLING MIXED OPPONENT TYPES

**Detecting cooperators (frequent C):**
- Reciprocate with high probability of C
- Benefit from the multiplier effect together

**Detecting defectors (frequent D):**
- Reduce your contribution likelihood
- Avoid one-sided exploitation

**Detecting conditional types (sensitive to history):**
- These are strategic partners; maintain contribution to sustain the equilibrium

---

## EDGE CASES

**Unanimous defection (everyone else D):**
- Defect immediately in the next round
- Personal payoff = 1 (keep endowment); collective payoff is zero anyway
- No incentive to unilaterally contribute

**Unanimous cooperation (everyone C):**
- Continue contributing every round
- Collective payoff maximized; personal security is high

**First-round defectors:**
- Do not punish permanently; re-evaluate their strategy after round 3
- Some opponents may be testing or have different assumptions about game structure

---

## COLLECTIVE MINDSET ALIGNMENT

This strategy prioritizes:

1. **Mutual welfare maximization:** Begin with contribution; seek equilibria where others also contribute
2. **Resilience against exploitation:** Quickly shift to defection when cooperation fails, protecting against free-riders
3. **Information aggregation:** Use public history to distinguish opponent types and adapt accordingly
4. **Graceful degradation:** If collective cooperation fails, minimize damage rather than pursue costly punishment

The strategy recognizes that in a no-communication, simultaneous-move environment, **shared history is the only coordination device**. By making contribution decisions transparent and history-dependent, it signals willingness to cooperate while remaining robust to unilateral defection.

---

## SUMMARY

- **Start cooperative:** C in round 1
- **Reciprocate observed cooperation:** threshold 50% prior-round contribution rate
- **Detect and isolate defectors:** track individual patterns
- **Abandon false hope:** switch to D if cumulative cooperation < 50% with few rounds left
- **Preserve final signal:** maintain C in round r if meaningful cooperation has occurred

This approach maximizes expected payoff across diverse opponent populations while respecting the collective welfare when mutual cooperation is feasible.
'''

description_COLLECTIVE_83 = '''
# ADAPTIVE RECIPROCAL THRESHOLD STRATEGY (ARTS)

## CORE PRINCIPLE
Maximize collective welfare by maintaining high cooperation when conditions support it, while minimizing exploitation through conditional defection. The strategy treats the game as a learning problem where we infer opponent types and adjust our contribution level accordingly.

## DECISION RULE (GENERAL CASE)

**Calculate the Cooperation Threshold:**
- Let `avg_contribution` = mean contributions across all players in the previous round
- Let `cooperation_rate` = proportion of players who contributed in the previous round
- Let `rounds_remaining` = r - current_round

**Contribution Decision:**

1. **IF cooperation_rate ≥ (k-1)/k:**
   - CONTRIBUTE (C)
   - Reasoning: When cooperation exceeds the break-even point, the multiplier k generates positive externalities. Contributing maintains this equilibrium and secures your share of the public good.

2. **ELSE IF cooperation_rate < (k-1)/k AND rounds_remaining > 2:**
   - Contribute with probability = cooperation_rate
   - Reasoning: Below the break-even threshold, we probabilistically participate to avoid cascading defection while testing whether cooperation can be restored.

3. **ELSE IF rounds_remaining ≤ 2:**
   - DEFECT (D)
   - Reasoning: In final rounds, the shadow of the future collapses. Defection dominates since reputational consequences vanish.

## EDGE CASES

**Round 1 (No History):**
- CONTRIBUTE
- Justification: We have no information, so we initialize cooperation to probe the environment and signal our type. This is the most generous starting point that allows collective value creation.

**Homogeneous Defection Detected (all D in previous round):**
- DEFECT for next round
- Justification: Attempting to be the "sucker" who alone contributes is wasteful. Signal rejection of pure defection equilibrium by withdrawing.

**Single Defector Detected (one player always defects, rest cooperate):**
- CONTRIBUTE
- Justification: The collective benefit from (n-1) contributors still exceeds individual defection payoff. Isolate the defector's gains by maintaining group cooperation.

**Repeated Conditional Defection Pattern:**
- If a player contributed in round t-1 but defected in round t (conditional on others' actions), treat as a strategic player using similar logic. Match their contribution probability in round t+1.

## ROBUSTNESS FEATURES

**Against Free-Riders:**
The threshold mechanism allows graceful degradation—as defectors increase, our contribution probability decreases smoothly rather than collapsing to universal defection immediately.

**Against Reciprocators:**
By maintaining high contribution when cooperation_rate is high, we sustain cooperation with other reciprocal players, creating stable high-payoff equilibria.

**Against Random Players:**
Probabilistic contribution in ambiguous cases (cooperation_rate near threshold) hedges between punishment and exploration, preventing lock-in to bad equilibria.

**Against Unconditional Cooperators:**
We exploit them minimally—only defecting in final rounds when reputation effects truly vanish. This preserves the possibility of mutual high cooperation.

## COLLECTIVE ALIGNMENT

This strategy prioritizes **total welfare over individual payoff** in situations where the two conflict:
- We contribute when it creates positive sum value (cooperation_rate high)
- We defect strategically only to prevent systematic exploitation or when future iterations cease
- We treat other players' cooperation as a signal of collective viability rather than an opportunity for exploitation

The strategy embodies the principle that in repeated games with incomplete information, sustained cooperation is possible only if we maintain credible willingness to reciprocate rather than ruthlessly exploit.
'''

description_COLLECTIVE_84 = '''
# ADAPTIVE COLLECTIVE CONTRIBUTION STRATEGY FOR PGG

## CORE DECISION RULE: Conditional Contribution Based on Reciprocity and Collective Surplus

**Primary Logic:**
- Contribute (C) if the expected collective surplus from universal contribution exceeds the individual gain from defection
- Track the empirical cooperation rate and adjust contribution likelihood based on observed reciprocity
- Weight recent rounds more heavily to adapt to changing group dynamics

## DETAILED DECISION RULES

### Round 1 (Initialization)
**Action: CONTRIBUTE**
- Rationale: Without history, assume good faith. Starting with contribution signals willingness to build collective value and provides data for calibration.

### Rounds 2 through r-1 (Adaptive Phase)

**Step 1: Calculate the Empirical Cooperation Rate (ECR)**
- ECR = (total contributions in all previous rounds) / (number of players × number of completed rounds)
- Apply decay weighting: recent rounds count more heavily (e.g., rounds 2-3 have weight 1.5x, earlier rounds weight 1.0x)

**Step 2: Estimate Collective Payoff Potential**
- Calculate what *would* happen if everyone contributed: payoff = k/n × n = k (each player gets k)
- Calculate what *will* happen if you defect while others hold ECR steady: payoff = 1 + (k/n) × (n × ECR - 1)
- Gap = k - [1 + (k/n) × (n × ECR - 1)]

**Step 3: Apply Decision Threshold with Hysteresis**
- If Gap > 0.15 (collective contribution is meaningfully better): CONTRIBUTE
- If Gap < -0.15 (defection is clearly better): DEFECT
- If -0.15 ≤ Gap ≤ 0.15 (uncertain): CONTRIBUTE with probability (ECR + 0.2), capped at 0.95
  - This maintains some optimism while respecting observed behavior

**Step 4: Monitor for Exploitation**
- If ECR drops below 0.25 in the last 3 rounds: shift to DEFECT (avoid being the sole contributor)
- If ECR rises above 0.80 in any 3-round window: increase contribution probability to 0.99 (reinforce momentum)

### Final Round (Round r)

**Action: Depend on ECR at the threshold**
- If ECR ≥ 0.60: CONTRIBUTE (strong reciprocal norm established; defecting now is inconsistent)
- If ECR < 0.60: DEFECT (group has shown low commitment; preserve individual resources)
- Exception: If rounds 2 through r-1 showed strictly increasing ECR trend: CONTRIBUTE (reward upward trajectory)

## EDGE CASES & ROBUSTNESS

**Unanimous Defection (ECR = 0):**
- Continue contributing until round r-3
- Switch to defection in final rounds to preserve payoff
- Rationale: Maintain moral consistency early; avoid sustained losses

**Unanimous Cooperation (ECR = 1.0):**
- Maintain contribution throughout
- This achieves the collective optimum

**Sudden Drops in Cooperation:**
- If ECR drops >0.25 in a single round, temporarily increase defection probability by 0.15 for the next round (signal concern)
- Then revert to adaptive rule if cooperation recovers

**Mixed Defectors:**
- Track individual contribution patterns if feasible
- If a specific player consistently defects while others cooperate, do not punish the group; maintain your reciprocity-based strategy
- Collective strategy assumes players are independently rational, not coordinated opponents

## RATIONALE FOR COLLECTIVE ALIGNMENT

This strategy prioritizes:
1. **Collective surplus creation**: Contributes when group cooperation generates k > 1 benefit per unit
2. **Reciprocal fairness**: Adjusts contribution based on what others actually do, not assumptions
3. **Resilience**: Avoids naive cooperation (sucker's payoff) while maintaining optimism about reciprocity
4. **Transparency**: Observable pattern encourages others to reciprocate
5. **Robustness**: Functions without assuming opponent coordination or shared communication

The strategy is **adaptive, not vengeful**—it responds to aggregate behavior rather than punishing individual deviations, making it robust in heterogeneous tournaments.
'''

description_COLLECTIVE_85 = '''
# ADAPTIVE COLLECTIVE CONTRIBUTION STRATEGY

## Core Philosophy
Maximize collective welfare by sustaining cooperation when feasible, while protecting against exploitation. The strategy treats the group as a dynamic system where individual decisions should reinforce conditions for mutual benefit.

## PRIMARY DECISION RULE

**Cooperate if and only if:**
1. The historical cooperation rate (across all players) in the last W rounds ≥ threshold T
2. OR we are in the early game (rounds 1-3) and should establish cooperative norms
3. AND the remaining rounds are sufficient to recoup cooperation losses

**Defect if:**
- Historical cooperation rate falls below threshold T
- We are in the final round (defection is individually optimal with no future shadow of the future)
- The moving average of others' payoffs suggests systematic exploitation of cooperators

## THRESHOLD PARAMETERS
- **W (window)**: Last 5 rounds (or all rounds if fewer than 5 completed)
- **T (cooperation threshold)**: 60% average contribution rate
- **Rounds remaining threshold**: At least 2 rounds must remain for cooperation to be rational

## ROUND-SPECIFIC BEHAVIOR

**Rounds 1-3 (Early Game):**
- **Action**: COOPERATE unconditionally
- **Rationale**: Establish cooperative equilibrium; signal willingness to contribute; gather information on opponent types

**Rounds 4 to (r-2) (Mid-Game):**
- Apply primary decision rule based on accumulated history
- Track which players have never defected (reliable cooperators) vs. consistent defectors
- Recalculate threshold each round using rolling window

**Rounds (r-1) and r (Endgame):**
- **Round (r-1)**: Cooperate only if cooperation rate ≥ 70% (higher threshold, need strong signal)
- **Round r (final)**: DEFECT
  - Rationale: Standard backwards induction; no future rounds to punish defection
  - Exception: Only if aggregate cooperation rate ≥ 85% AND you have reason to believe others will also cooperate in final round (very rare)

## ROBUSTNESS MECHANISMS

**Against Free-Riders (Always Defect):**
- Quickly identify patterns of zero contribution
- Transition to defection within 4-5 rounds
- Minimize wasted cooperation

**Against Conditional Cooperators (Mimic Average):**
- These are valuable partners; maintain cooperation while overall threshold is met
- Your cooperation signals that cooperation is sustainable

**Against Random Players:**
- Rolling window averages smooth out noise
- Requires 60% threshold to tolerate some randomness without collapse

**Against Tit-for-Tat Variants:**
- Your strategy is less punitive than strict TFT, allowing recovery
- If they defect once, you don't immediately defect; instead, you track the trend
- This permits graceful degradation rather than punishment spirals

## COLLECTIVE ALIGNMENT

This strategy is collectively rational because:
1. **Initiates cooperation** to create surplus (k > 1)
2. **Sustains cooperation** when others reciprocate, maximizing total payoff
3. **Exits gracefully** when cooperation becomes unprofitable, avoiding sunk losses
4. **Protects the group** from systematic exploitation by defectors
5. **Adapts dynamically** rather than following rigid rules; recognizes that different opponent compositions require different approaches

The 60% threshold specifically balances two needs: tolerating occasional defectors while maintaining a cooperative commons. With k > 1, even if 40% defect, the collective still benefits from the 60% cooperating.

## SUMMARY TABLE

| Game Phase | Condition | Action |
|-----------|-----------|--------|
| Rounds 1-3 | Always | **COOPERATE** |
| Rounds 4-(r-2) | Coop rate ≥ 60% | **COOPERATE** |
| Rounds 4-(r-2) | Coop rate < 60% | **DEFECT** |
| Round (r-1) | Coop rate ≥ 70% | **COOPERATE** |
| Round (r-1) | Coop rate < 70% | **DEFECT** |
| Round r | Always | **DEFECT** |
'''

description_COLLECTIVE_86 = '''
# ADAPTIVE COLLECTIVE STRATEGY FOR PUBLIC GOODS GAME

## CORE PRINCIPLE
Maximize collective welfare by maintaining cooperation when feasible, while protecting against exploitation. The strategy treats the group as an interdependent system and seeks equilibria that benefit all participants relative to mutual defection.

## DECISION RULE: CONDITIONAL COOPERATION WITH COLLECTIVE THRESHOLD

**Primary Logic:**
- Contribute (C) if the expected collective benefit from your contribution exceeds the individual cost
- Defect (D) only when cooperation appears systematically undermined

**Specific Rule:**
Each round, calculate the **Group Cooperation Rate (GCR)** from the previous round:
- GCR = (total contributions in round t-1) / n

**Action Selection:**
1. If GCR ≥ threshold (default: k/n, the break-even point), then CONTRIBUTE
2. If GCR < threshold AND this has persisted for 2+ consecutive rounds, then DEFECT
3. If GCR recovers after defection, return to CONTRIBUTE after 1 round of observation

**Rationale:** 
When cooperation rate suggests others are cooperating, the multiplier effect makes contribution individually rational and collectively optimal. When cooperation deteriorates, brief defection protects against systematic free-riding without permanent breakdown.

## EDGE CASES & SPECIAL HANDLING

**Round 1 (Information Vacuum):**
- CONTRIBUTE unconditionally
- Establishes cooperative intent and signals willingness to participate in collective benefit
- Gathers baseline information on opponent behavior

**Final Round (Round r):**
- Apply the standard decision rule based on observed GCR
- Do not defect solely because it's the last round; maintain consistency with collective strategy
- If GCR is strong, contribute to preserve the integrity of cooperation

**Extreme Cases:**
- If GCR = 0 (complete defection by all) for 2+ rounds: DEFECT (no value to contributing)
- If GCR = 1 (complete cooperation by all) for 3+ rounds: CONTRIBUTE (stable cooperative equilibrium)
- If n = 2 and opponent defects consistently: DEFECT (no path to recovery in 2-player game)

## ADAPTIVE REFINEMENT: MEMORY & RECOVERY

**Track opponent profiles** implicitly:
- If any individual player has defected in >70% of rounds where GCR was ≥ threshold, they are a systematic free-rider
- When free-riders are clearly identified AND the collective still benefits from aggregate cooperation, continue contributing (you're hedging against their defection)

**Recovery mechanism:**
- If you defect for 1-2 rounds and GCR then increases, immediately return to cooperation
- This signals that defection was punishment, not permanent abandonment

## COLLECTIVE ALIGNMENT

This strategy prioritizes:
1. **Collective surplus** - Seeking outcomes where total payoffs exceed mutual defection
2. **Stability** - Avoiding races to the bottom while protecting against exploitation
3. **Inclusivity** - Acting as though other players might follow similar logic, creating positive-sum equilibria
4. **Transparency** - Observable actions that communicate commitment to cooperation when conditions support it

The strategy treats defection as a signal of collective dysfunction, not a competitive advantage, and returns to cooperation when conditions stabilize—ensuring the group can recover toward efficient outcomes.
'''

description_COLLECTIVE_87 = '''
# ADAPTIVE COLLECTIVE STRATEGY FOR PUBLIC GOODS GAME

## CORE PRINCIPLE
Maximize collective welfare through conditional cooperation that responds to the demonstrated trustworthiness of the group, while maintaining individual rationality as a credible fallback.

## DECISION RULE

**Contribution Decision:**
- Contribute (C) if: `recent_cooperation_rate >= cooperation_threshold`
- Defect (D) if: `recent_cooperation_rate < cooperation_threshold`

Where:
- `recent_cooperation_rate` = proportion of C actions in the last W rounds (window) across all other players
- `cooperation_threshold` = k/n (the break-even point where contribution is individually rational)

**Intuition:** Contribute when the group's recent behavior suggests others are also contributing, making collective action worthwhile.

## PARAMETER SETTINGS

- **Window size W:** min(5, r/3) — look at recent history, but scale with game length
- **Threshold:** k/n — this is the pivot point where collective contribution becomes individually beneficial

## EDGE CASES & SPECIAL HANDLING

**Round 1 (Cold start):**
- Contribute (C) with probability k/n as an exploratory signal
- *Rationale:* Signal willingness to cooperate; establish mutual benefit baseline

**Last Round (Round r):**
- Defect (D) unconditionally
- *Rationale:* No future reciprocation possible; maximize immediate payoff
- *Caveat:* Only apply this if r is known in advance. If r is unknown, treat as a normal round.

**Rounds 2 through r-1:**
- Apply the standard rule above

**All players defected in the observation window:**
- Defect (D) for one more round
- Then re-evaluate; if defection persists, defect again
- *Rationale:* Avoid being exploited, but keep the door open for recovery

**All players contributed in the observation window:**
- Contribute (C) with high confidence
- *Rationale:* Reinforce and sustain cooperation

## ROBUSTNESS MECHANISMS

1. **Forgiveness Window:** If cooperation rate was low but suddenly increases, respond within 1-2 rounds. Don't punish indefinitely.

2. **Graceful Degradation:** As the game nears its end (last round known), gradually increase defection probability rather than switching abruptly. This avoids sudden betrayals that destabilize groups.

3. **Majority Rule with Slack:** Only defect if *most* others defected, not if a single player defected. Tolerate ~20% free-riding as noise.

4. **Adaptive Threshold:** If the group sustains high cooperation for 3+ consecutive rounds, lower the threshold slightly (e.g., threshold *= 0.95) to reward consistent good behavior.

## COLLECTIVE ALIGNMENT

This strategy prioritizes **group welfare** by:
- Initiating cooperation to establish mutual benefit
- Rewarding others' cooperative choices with reciprocation
- Punishing sustained defection without mercy-killing the group
- Exiting gracefully when cooperation cannot be sustained (defect, don't spam)

It remains **individually rational** by:
- Never contributing when group cooperation is too low to justify it
- Defecting in the final round when no punishment is possible
- Protecting against systematic exploitation

## SUMMARY
"Cooperate if others have recently cooperated; defect otherwise. Signal willingness to cooperate early, abandon cooperation late, and maintain flexibility to recover if the group restabilizes."
'''

description_COLLECTIVE_88 = '''
# ADAPTIVE RECIPROCAL CONTRIBUTION STRATEGY (ARC)

## CORE PRINCIPLE
Maximize collective welfare while maintaining individual rationality through graduated reciprocity that adapts to observed cooperation rates and remaining game horizon.

## DECISION RULES

### Round 1 (Initialization)
**Action: CONTRIBUTE**

Rationale: The first round is an information probe. Contributing signals willingness to cooperate and generates a baseline observation of the group's composition. The cost (1 token) is minimal relative to potential gains from identifying cooperators versus defectors.

### Rounds 2 to (r-1) (Main Phase)
**Calculate the Recent Cooperation Rate (RCR):**
- RCR = (total contributions in last 3 rounds) / (3 × n)
- If fewer than 3 prior rounds exist, use all available history
- RCR represents the proportion of players cooperating on average

**Contribution Decision:**

IF RCR ≥ 0.5:
  - **CONTRIBUTE**
  - Threshold rationale: When at least half the group contributes, the collective payoff (k/n × total) exceeds individual defection payoff at expected cooperation levels (when k > 1)

ELSE IF RCR < 0.5 AND RCR > 0.1:
  - **CONTRIBUTE with probability = 2 × RCR**
  - Rationale: In low-cooperation regimes, employ probabilistic contribution to maintain a "costly signal" that distinguishes cooperators while limiting losses. At 20% cooperation, contribute 40% of the time; at 49%, contribute 98%

ELSE IF RCR ≤ 0.1:
  - **DEFECT**
  - Rationale: The group has collapsed into near-pure defection. Contributing yields minimal return (k/n × ≈0.1 < 1). Preserve the token for individual payoff.

### Round r (Final Round)
**Condition Check:**

IF RCR in previous rounds ≥ 0.5:
  - **CONTRIBUTE**
  - Rationale: Maintain collective welfare norm to the end. The one-round horizon is irrelevant when the group has demonstrated sustained cooperation

ELSE:
  - **DEFECT**
  - Rationale: In low-cooperation environments, the final round offers no repeated-game incentive to signal future cooperation. Secure the individual token

## EDGE CASES & ROBUSTNESS

**Uniform Defection from Start:**
The strategy naturally transitions to defection by Round 3, minimizing losses against all-defect groups while avoiding sunk cost fallacy.

**Mixed or Volatile Groups:**
The probabilistic rule in the 0.1 < RCR < 0.5 band prevents complete collapse while testing whether defectors will exploit. If defectors dominate, the strategy gracefully degrades to defection without wasting resources.

**Shrinking Horizon Effect:**
The strategy is *not* horizon-aware in the classical backward induction sense. Instead, it bets on the empirical observation that cooperation correlates with payoff when k > 1, making the final-round defection temptation secondary to sustaining a cooperative regime if one exists.

**Heterogeneous Opponents:**
The strategy assumes no shared norms. By relying on observable history rather than player labels or reciprocal matching, it works identically against tit-for-tat, unconditional defectors, random players, and other strategies.

## ALIGNMENT WITH COLLECTIVE WELFARE

- **Round 1 contribution** seeds the information needed for collective learning
- **0.5 threshold** aligns individual incentives with group payoff maximization (when k > 1 and contributions exceed 50%, total welfare grows)
- **Probabilistic defection** in mid-range cooperation prevents free-rider collapse while maintaining flexibility
- **Final-round commitment** to high-cooperation groups ensures no betrayal when the group has signaled stability

This strategy treats the repeated game as an empirical test of whether collective cooperation is self-sustaining, and adapts accordingly.
'''

description_COLLECTIVE_89 = '''
# ADAPTIVE COLLECTIVE CONTRIBUTION STRATEGY

## CORE PRINCIPLE
Maximize collective welfare by contributing when the group demonstrates sufficient reciprocal commitment, while protecting against free-rider exploitation through conditional cooperation.

## DECISION RULE (GENERAL ROUNDS)

**Cooperate (Contribute 1 token) IF:**
- The average contribution rate in the previous round ≥ threshold T, OR
- We are in the early phase (rounds 1-3) to establish cooperative foundations

**Defect (Contribute 0 tokens) IF:**
- Average contribution rate in previous round < threshold T, OR
- Individual defection payoff significantly exceeds cooperative payoff in recent history

**Threshold T** = 0.5 (require at least 50% of the group contributing)

## EDGE CASES & SPECIAL HANDLING

**Round 1 (Initial):**
- Contribute. Establish good faith signal and gather information on group composition.
- This seeds reciprocal dynamics without assuming prior coordination.

**Rounds 2-3 (Early Phase):**
- Contribute regardless of R1 outcomes. The group needs time to recognize patterns.
- Use this window to map opponent types (cooperators vs defectors).

**Round r-1 (Penultimate):**
- Apply normal rule. Do not assume end-game defection is optimal—maintain consistency to reward reciprocators one final time.

**Last Round r:**
- Evaluate: If average contribution ≥ T, contribute. Otherwise defect.
- Final round is informative but do not assume others will defect just because it's the last round.

## ADAPTIVE REFINEMENT

**If contribution rate drops sharply (≥30 percentage-point decline):**
- Shift threshold down to T = 0.35 for one round to test if the group is recovering or in collapse.
- If recovery occurs, reset to T = 0.5.
- If further decay, drift to permanent defection (the group has fractured).

**Minority cooperator scenario:**
- If you are the sole/near-sole contributor for 3+ consecutive rounds, defect for 1 round as a costly signal that free-riding is unsustainable.
- Resume cooperation only if contribution rate rebounds.

## COLLECTIVE ALIGNMENT

This strategy:
- **Rewards reciprocity** without requiring prior agreement—cooperators receive mutual benefit.
- **Punishes defection** through conditional withdrawal, not vindictively.
- **Stabilizes groups** by providing a focal point: "Contribute if others do."
- **Survives diverse opponents** because it does not depend on shared norms—it observes and responds.
- **Scales adaptively**: Works for n=2 to large groups; threshold adjusts to observed group behavior.

## ROBUSTNESS NOTES

- Against pure defectors: You defect after establishing they won't reciprocate.
- Against tit-for-tat: You cooperate symmetrically.
- Against random players: You sustain contribution if random rates ≥50%, exit gracefully otherwise.
- Against mixed populations: You gravitate toward whichever subset will reciprocate, implicitly segregating behavior by group composition.
'''

description_COLLECTIVE_90 = '''
# ADAPTIVE COLLECTIVE STRATEGY FOR PUBLIC GOODS GAME

## CORE PRINCIPLE
Maximize group welfare by conditioning cooperation on observable evidence that the group can sustain it, while maintaining individual rationality as a fallback.

## DECISION RULE (GENERAL ROUNDS)

**Cooperate if and only if:**
1. The empirical cooperation rate in the previous round ≥ threshold T, OR
2. We are in round 1 (initialize cooperation)

**Otherwise: Defect**

**Threshold calculation:**
- T = (1/k) + 0.15
- Intuition: Cooperate when expected return from collective action exceeds 1 token (the defection payoff), with a conservative margin

## HANDLING EDGE CASES

**Round 1 (Initialization):**
- Cooperate unconditionally
- Rationale: Establish a cooperative signal; gather information about group composition

**Last Round (Round r):**
- Defect (unless cooperation rate was ≥ T-0.20 in round r-1, then cooperate once more)
- Rationale: Standard backward induction, but slightly soften end-game defection if strong cooperation signal exists

**Rounds 2 through r-1 (Sustained Play):**
- Apply the standard threshold rule above
- Track cooperation rate as: (# cooperators last round) / n

## ADAPTIVE REFINEMENTS

**Detection of Defection Spirals:**
- If cooperation rate drops below T for 2 consecutive rounds, stay defected for 1 additional round as a "penalty signal"
- This discourages free-riders from exploiting renewed cooperation attempts

**Exploitation Resistance:**
- If cooperation rate is exactly 1 (everyone cooperated) but drops sharply the next round (>2 defectors), switch to defection for 2 rounds
- This punishes coordinated exploitation attempts

**Recovery Mode:**
- If cooperation rate ≥ T-0.10 (high cooperation signal), cooperate even if the exact threshold is slightly missed
- Rationale: Tolerate minor defection and attempt to resuscitate cooperation

## COLLECTIVE ALIGNMENT

This strategy prioritizes **group payoff stability** over individual maximization:
- Cooperates when group conditions support it (empirical evidence of reciprocation)
- Defects when the group reveals it cannot sustain cooperation
- Does not exploit temporary cooperation surges; instead, rides them out
- Incorporates "second-chance" logic: punish defection but allow recovery

The threshold T bridges individual rationality (never cooperate unless the multiplier effect covers individual cost) with collective reasoning (coordinate on outcomes better than mutual defection).
'''

description_COLLECTIVE_91 = '''
# ADAPTIVE RECIPROCAL CONTRIBUTION STRATEGY (ARC)

## CORE PHILOSOPHY
Maximize collective welfare through conditional cooperation that responds to empirical evidence of others' willingness to contribute, while maintaining a credible deterrent against exploitation.

---

## DECISION RULE FRAMEWORK

### ROUND 1 (Bootstrap Round)
**Action: CONTRIBUTE (C)**

*Rationale:* We have no history, so we cannot condition on past behavior. Contributing signals good faith and generates the first data point about whether opponents reciprocate. This is the most informative action.

---

### ROUNDS 2 through (r-1) (Adaptive Core)

Calculate the **empirical cooperation rate**:
- `cooperation_rate = (total C actions by all other players) / (n-1) * (rounds elapsed)`

**Decision Rule:**
1. If `cooperation_rate ≥ threshold_T`, then **CONTRIBUTE (C)**
   - *Rationale:* Others are reciprocating; collective welfare increases when we all contribute. The multiplier effect (k > 1) means total surplus grows.

2. If `cooperation_rate < threshold_T`, then **DEFECT (D)**
   - *Rationale:* Others are predominantly free-riding. Contributing would subsidize defectors. Defecting preserves our endowment and avoids wasting resources.

**Recommended threshold:** `threshold_T = (k-1) / k`
- *Justification:* This threshold represents the breakeven point. Contributing is collectively beneficial when others contribute above this rate (since `k > 1`).

---

### ROUND r (Final Round - Special Handling)

**Action: Inherit the decision from round (r-1)**

*Rationale:* Since there is no reputation effect beyond round r, standard game theory suggests defection in the final round. However, this triggers backward induction and universal defection. Instead, we maintain consistency with our track record:
- If we've been contributing (cooperation_rate ≥ T), **CONTRIBUTE** in the final round to signal our strategy is genuine, not tactical.
- If we've been defecting (cooperation_rate < T), **DEFECT** consistently.

*Benefit:* This avoids the "last round cliff" and maintains credibility if opponents use similar logic.

---

## EDGE CASES & REFINEMENTS

**When cooperation_rate is exactly at threshold:**
- **CONTRIBUTE** (Err toward optimism for collective good)

**When n is very small (n=2 or 3):**
- Lower threshold slightly to `(k-1)/k - 0.1` to account for higher volatility
- Each individual action has outsized impact on cooperation rate

**If all opponents defected in all previous rounds:**
- Continue with **DEFECT** (they've revealed their type; contributing is futile)

**If exactly one opponent contributes consistently while others defect:**
- Continue applying the rule mechanically (cooperation_rate still < T overall)
- Do not reward individual reciprocators differently (no communication channel exists)

**Unstable cooperation_rate (oscillates around threshold):**
- Use a **moving average** of the last 3 rounds instead of cumulative rate to reduce noise
- This makes strategy less reactive to single-round anomalies

---

## RATIONALE FOR COLLECTIVE ALIGNMENT

1. **Respects mutual benefit:** We cooperate when cooperation_rate suggests others reciprocate, directly maximizing group payoff per the multiplier mechanism.

2. **Rational for individuals:** By defecting only when collective contribution is low, we avoid losses from one-sided cooperation while capturing gains from mutual contribution.

3. **Robust to diverse opponents:** 
   - Against cooperators: We reciprocate, achieving high collective payoffs
   - Against defectors: We defect, protecting ourselves
   - Against other conditional strategies: We both adjust toward cooperation if possible

4. **No assumptions needed:** Requires only observable history, not shared norms or communication.

5. **Evolutionary stable:** Strategies playing against us will converge toward cooperation if they use similar logic, creating a virtuous cycle.

---

## SUMMARY
**Cooperate when empirical cooperation exceeds (k-1)/k; defect otherwise. Maintain consistency in the final round. Adjust thresholds and averaging for small groups and noise.**
'''

description_COLLECTIVE_92 = '''
# ADAPTIVE RECIPROCAL CONTRIBUTION STRATEGY

## CORE PRINCIPLE
Maximize collective welfare by maintaining cooperation when it's sustainable, while gracefully degrading to individual rationality when the group fails to cooperate. This balances genuine collective benefit with robustness against free-riders.

## DECISION RULES

### Round 1 (Initialization)
**CONTRIBUTE**
- Establish goodwill and signal cooperative intent
- Provide information to others about your reliability
- Set positive cooperative precedent

### Rounds 2 through (r-1) (Repeated Play)
**Evaluate the collective cooperation rate:**
- Calculate C_rate = (total contributions in previous round) / n
- This measures how much the group, including you, has been contributing

**Decision logic:**
- **IF C_rate ≥ threshold (0.5):** CONTRIBUTE
  - The group is cooperating sufficiently to make contributions worthwhile
  - Your contribution generates expected value for the collective
  - Continue reciprocating cooperation
  
- **IF C_rate < threshold (0.5) AND this is round 2 or 3:** CONTRIBUTE
  - Give the group one more round to stabilize cooperation
  - Avoid premature defection that could destabilize fragile coordination
  
- **IF C_rate < threshold (0.5) AND this is round ≥ 4:** DEFECT
  - The group has demonstrated insufficient commitment to cooperation
  - Contributing becomes a losing proposition for collective benefit
  - Pivot to protect individual welfare and avoid exploitation

### Final Round (Round r)
**DEFECT**
- In the final round, there is no future to invest in
- Any contribution cannot establish reciprocity for future cooperation
- The multiplier effect cannot justify the loss
- Rational individual action aligns with ending the game

## HANDLING EDGE CASES

**Single round games (r=1):**
- DEFECT immediately (same logic as final round)

**Extremely high multipliers (k ≥ n-1):**
- Adjust threshold upward to 0.6-0.7
- Higher multipliers mean cooperation is more efficient, so require higher collective participation rates

**Very small groups (n ≤ 3):**
- Adjust threshold downward to 0.3-0.4
- In tiny groups, one defector is more devastating; be more tolerant of occasional defection

**Sudden cooperation collapses:**
- If C_rate drops by >0.4 in a single round, DEFECT immediately
- This signals organized free-riding; abandon cooperation

## COLLECTIVE ALIGNMENT

This strategy prioritizes:

1. **Cooperation sustainability** - Contribute when others do, creating positive feedback loops
2. **Collective efficiency** - The threshold ensures the group only maintains cooperation when the multiplier benefit exceeds individual cost
3. **Robustness** - Defect when the collective fails, preventing cumulative losses
4. **Fairness** - Your actions mirror group behavior rather than exploiting others
5. **No exploitation** - You never defect while others cooperate (except final round, which is universal)

## EXPECTED OUTCOMES

Against cooperative opponents: High mutual contribution, strong collective payoffs
Against defectors: Rapid defection limits damage to the collective outcome
Against mixed groups: Stabilizes around the cooperation threshold, reasonable compromise outcome
'''

description_COLLECTIVE_93 = '''
# COLLECTIVE STRATEGY FOR PUBLIC GOODS GAME

## CORE PRINCIPLE
Maximize collective welfare through **conditional cooperation with adaptive defection thresholds**. The strategy balances trust-building with protection against exploitation, treating the game as a repeated opportunity to establish mutually beneficial equilibrium.

## DECISION RULES

### ROUND 1 (Initialization)
**COOPERATE**
- Rationale: Signal cooperative intent and establish a baseline for evaluating opponent behavior. Cooperation in round 1 is the lowest-cost way to test whether collective gains are possible.

### ROUNDS 2 to (r-1) (Main Phase)
**Use Conditional Contribution Threshold:**

1. **Calculate the recent cooperation rate** among all other players (using last 3-5 rounds, or all previous rounds if fewer than 5 exist)
   - Recent_coop_rate = (sum of contributions by other players) / (number of other players * number of rounds reviewed)

2. **Determine collective contribution expectation:**
   - If recent_coop_rate ≥ 0.5: Assume the group is attempting coordination toward mutual benefit
   - If recent_coop_rate < 0.5: Assume the group is primarily defecting

3. **Conditional decision:**
   - **IF** recent_coop_rate ≥ 0.5: **COOPERATE**
     - The collective is trending toward mutual gain; contributing sustains this trajectory
   - **IF** recent_coop_rate < 0.5 AND you have been cooperating consistently: **DEFECT** (1 round)
     - Punish the group's betrayal by withholding; reset the signal
   - **IF** recent_coop_rate < 0.5 AND you have been defecting: **DEFECT** (continue)
     - No reason to unilaterally deviate when others are defecting

### ROUND r (Final Round)
**DEFECT**
- Rationale: No future payoffs depend on reputation after the final round. The shadow of the future vanishes, so individual incentives dominate. Defecting maximizes personal payoff in isolation.

## EDGE CASES & ADAPTIVE LOGIC

**If exactly 2 players (n=2):**
- The multiplier condition (1 < k < 2) is very tight. Cooperation only pays off if k > 1 strictly. Adjust: Cooperate if opponent has cooperated in >60% of rounds; otherwise defect. The mutual gain is fragile, so require stronger evidence of intent.

**If large n (n ≥ 5):**
- Freeriding becomes more tempting because individual impact on collective pool is diluted. Lower the cooperation threshold slightly: Cooperate if recent_coop_rate ≥ 0.4. The collective benefit per person is smaller, so require less confidence.

**If r is very short (r ≤ 3):**
- Limited rounds mean limited opportunity to signal and learn. Round 1 cooperation is critical. After observing round 1, switch to defection in round 2 if others defected in round 1.

**If r is very long (r > 20):**
- Long horizon increases the value of reputation and collective payoffs. Raise cooperation threshold to 0.6 to ensure higher-quality coordination. Be more forgiving of temporary defection.

## COLLECTIVE ALIGNMENT

This strategy prioritizes **group welfare over individual exploitation:**

- It initiates cooperation, giving others the chance to establish mutually beneficial outcomes
- It maintains cooperation when the group reciprocates, reinforcing collective gains
- It withdraws cooperation when the group defects, avoiding unilateral losses
- It defects only in the final round (unavoidable given game structure) and in temporary punishment phases (necessary to maintain credible deterrence against freeriding)

The strategy treats other players' contributions as signals of collective intent, not as independent problems to exploit. By conditioning on recent history, it adapts to changing group behavior and avoids rigid commitment to either permanent cooperation (naive) or permanent defection (missed gains).
'''

description_COLLECTIVE_94 = '''
# COLLECTIVE STRATEGY FOR PUBLIC GOODS GAME

## CORE PRINCIPLE
Maximize collective welfare through conditional cooperation that rewards contribution and penalizes free-riding, while maintaining robustness against exploitation.

## DECISION RULES

### Round 1 (Initialization)
**COOPERATE (Contribute 1)**
- Start with good faith contribution to establish cooperative potential
- Signals willingness to benefit the group
- Gathers information about opponent tendencies

### Rounds 2 through r-1 (Adaptive Phase)
**Conditional Cooperation with Escalating Penalties**

Calculate the group's **cooperation rate** = (total contributions in previous round) / n

**IF** cooperation_rate ≥ threshold (recommend: 0.5):
- **COOPERATE**: Match or exceed the group's contribution level
- Reinforce positive trends toward collective welfare

**ELSE IF** cooperation_rate < threshold:
- **Assess defection pattern**: Count how many consecutive rounds the group contributed below threshold
- **Defection streak = 1-2 rounds**: DEFECT this round (cost-recovery phase)
- **Defection streak ≥ 3 rounds**: Continue DEFECTING until cooperation recovers (avoid being exploited indefinitely)

### Final Round (Round r)
**COOPERATE (Contribute 1)**
- Override the adaptive rule and contribute regardless of history
- This final act of cooperation maximizes collective payoff in the endgame
- Prevents mutual defection spirals in the last round
- Demonstrates that cooperation serves group welfare, not strategic manipulation

## EDGE CASE HANDLING

**High-defection environments (cooperation_rate consistently < 0.3):**
- Switch to pure defection strategy to protect endowment
- Remain in defection until two consecutive rounds show cooperation_rate ≥ 0.6

**Majority cooperators (cooperation_rate > 0.7):**
- Always cooperate; the collective benefit from the multiplier outweighs individual gain from defection

**Oscillating patterns (cooperation fluctuates between 0.3-0.7):**
- Use a 2-round moving average for cooperation_rate to smooth noise
- Reduces reactive whipsawing

**Single defector in otherwise cooperative group:**
- Continue cooperation; one defector's free-riding is absorbed by the multiplier benefit
- Only penalize if defection becomes systemic (>50% group defection)

## COLLECTIVE ALIGNMENT

This strategy prioritizes:
1. **Pareto improvement over mutual defection** – Returns to all players improve when cooperation thresholds are met
2. **Robustness to self-interest** – Works even when opponents pursue independent payoff maximization
3. **Punishment of systematic defection** – Prevents exploitation while not being vindictive
4. **Cooperation recovery** – Offers defectors a path back to mutual cooperation
5. **Final cooperation** – Ensures the closing round contributes positively to collective welfare, regardless of prior antagonism

The strategy is *not* purely altruistic—it protects individual interests when the group fails to cooperate—but it *is* collectively rational because it seeks states where all players benefit from the multiplier mechanism.
'''

description_COLLECTIVE_95 = '''
# COLLECTIVE STRATEGY FOR PUBLIC GOODS GAME

## CORE PRINCIPLE
Maximize collective welfare through adaptive conditional cooperation that rewards group contribution while protecting against systematic defection.

## DECISION RULES

### PRIMARY LOGIC: Contribution-Responsive Cooperation

**Contribute (C) if and only if:**
- The average contribution rate in the previous round was ≥ 50%, OR
- This is round 1 (initialization with optimism), OR
- Rounds remaining ≤ 2 AND average past contribution ≥ 40% (end-game leniency)

**Defect (D) otherwise** – when average contribution fell below the threshold

### THRESHOLD JUSTIFICATION
- 50% threshold balances two goals: (1) sustains cooperation when it's genuinely beneficial to the group, and (2) stops rewarding serial defectors
- At 50%+ contribution, the collective payoff from cooperation typically exceeds individual defection payoffs
- This creates a basin of attraction around cooperative equilibrium

## EDGE CASES & REFINEMENTS

**Round 1 (First Move):** 
Contribute. This signals willingness to cooperate and tests opponent cooperation levels without penalty.

**Last Round (Round r):**
Defect. No future reputation consequences matter; individual incentive dominates. This is rational given the game structure.

**Rounds 2 through r-1:**
Apply the contribution-responsive rule strictly.

**Complete Defection Scenario:**
If all other players defect in round 1 (0% average), defect in round 2 and all subsequent rounds until the final round rule applies. There is no benefit to unilateral contribution.

**Oscillating/Mixed Opponents:**
Track the rolling average contribution rate. If it fluctuates around 50%, remain in contributing mode. This gives mixed players a chance while maintaining robustness.

## COLLECTIVE ALIGNMENT

This strategy embodies collective welfare through:

1. **Reciprocal Fairness:** We contribute when the group contributes; we stop investing in groups that don't reciprocate
2. **Stability:** By conditioning on group behavior rather than individual player behavior, we avoid cycles of tit-for-tat retaliation
3. **Efficiency:** We sustain the cooperative pool when it exists, generating positive social value
4. **Rationality:** We abandon doomed cooperation attempts rather than throwing good contributions after bad

## ROBUSTNESS PROPERTIES

- **vs. Always-Cooperate players:** We reciprocate fully, achieving high mutual payoff
- **vs. Always-Defect players:** We defect after round 1, minimizing losses
- **vs. Conditional cooperators (similar strategies):** We reach mutual cooperation and sustain it
- **vs. Unpredictable players:** The 50% threshold acts as a firebreak—we stay invested if they cooperate half the time, abandon if they don't

This strategy seeks to build and maintain cooperative coalitions while refusing to subsidize free-riders.
'''

description_COLLECTIVE_96 = '''
# ADAPTIVE COLLECTIVE STRATEGY FOR PUBLIC GOODS GAME

## CORE PRINCIPLE
Maximize collective welfare while remaining robust to free-riding. This means:
- Cooperate when others do, creating positive-sum outcomes
- Punish systematic defection through strategic withdrawal
- Recover cooperation when defectors show reform
- Remain adaptive to the evolving composition of player types

---

## PRIMARY DECISION RULE

**For each round t > 1:**

1. **Calculate the "cooperation ratio" from the previous round:**
   - cooperation_ratio = (total contributions in round t-1) / n
   - This represents the proportion of players who contributed

2. **Determine your action based on three tiers:**

   - **IF cooperation_ratio ≥ 0.5 (majority cooperate):** CONTRIBUTE
     - Rationale: Sufficient players are creating a positive-sum pool; defecting exploits them but sabotages collective gain

   - **IF 0.2 < cooperation_ratio < 0.5 (minority cooperate):** DEFECT
     - Rationale: Too few cooperators to generate meaningful returns. Contributing becomes pure exploitation of your cooperation. Defect to preserve resources.

   - **IF cooperation_ratio ≤ 0.2 (widespread defection):** DEFECT
     - Rationale: The pool is depleted. Cooperation yields minimal payoff and subsidizes defectors. Withdraw participation.

---

## EDGE CASES & SPECIAL ROUNDS

**Round 1 (No history):**
- CONTRIBUTE
- Rationale: Establish a cooperative signal. First-round defection poisons trust immediately. A cooperative opener gives the game a chance to reach equilibrium.

**Final Round (Round r):**
- Apply the standard rule above (based on cooperation_ratio from round r-1)
- Do NOT defect solely because it's the last round, as this breaks reciprocity and wastes historical investment in understanding opponent types

**When all others defected in round t-1:**
- DEFECT in round t
- Rationale: No collective benefit exists; don't subsidize pure free-riding

---

## RECOVERY & REFORM MECHANISM

If cooperation_ratio was ≤ 0.2 in round t-1 but rises to ≥ 0.4 in round t:
- CONTRIBUTE in round t+1
- Rationale: This signals that the group is recovering toward cooperation. Rejoin to support the recovery and test whether it's genuine.

If the ratio drops back below 0.2 in the next round, revert to DEFECT immediately.

---

## RATIONALITY ANCHORS

- **Against pure cooperators:** You will cooperate and capture mutual gains
- **Against pure defectors:** You will defect after the first round, minimizing your loss
- **Against conditional cooperators:** You will match their behavior and stabilize at mutual cooperation if they stabilize
- **Against random players:** Your majority-threshold rule filters noise and avoids being exploited
- **Against strategic defectors:** Your quick exit (cooperation_ratio ≤ 0.2) prevents them from profiting from a shrinking pool

---

## COLLECTIVE ALIGNMENT

This strategy prioritizes **group efficiency** over individual short-term gain:
- It seeks Pareto-improving equilibria (mutual cooperation)
- It abandons doomed pools rather than bleeding resources into them
- It offers a recovery pathway, signaling willingness to rebuild trust
- It resists being a sole cooperator in a sea of defection—protecting the collective from exploitation by many

The 50% threshold is the critical point: above it, the game becomes positive-sum even for cooperators; below it, cooperation becomes a subsidy to defectors.
'''

description_COLLECTIVE_97 = '''
# COLLECTIVE STRATEGY FOR PUBLIC GOODS GAME

## CORE PRINCIPLE
Maximize collective welfare through conditional cooperation that punishes defection while remaining robust to exploitation.

---

## DECISION RULES

### PRIMARY RULE: Conditional Contribution
**Contribute (C) if and only if:**
- The observed contribution rate in the previous round ≥ threshold T
- OR it is round 1 (initialize cooperation)

**Threshold T = 50%** (majority contributed in prior round)

**Otherwise: Defect (D)**

### RATIONALE
- 50% threshold balances optimism about cooperation with realism about exploitation
- Majority rule creates natural clustering: if half contribute, collective welfare improves, incentivizing sustainability
- Non-contributors are not isolated; the game remains productive if a critical mass cooperates

---

## EDGE CASES

### ROUND 1 (Initial Round)
**Action: CONTRIBUTE (C)**

Rationale: Establish a cooperative signal. This is the only unilateral action; thereafter, decisions are data-driven.

### FINAL ROUND (Round r)
**Action: DEFECT (D)** (if previous round didn't meet threshold)
**Action: CONTRIBUTE (C)** (if previous round met threshold)

Rationale: No future punishment is possible, so follow the conditional rule mechanically. If cooperation was sustained, extend it; otherwise, capture the endowment.

### FIRST 3 ROUNDS (Calibration Phase)
Track the contribution rate carefully. If observed contribution rate is ≥ 50% in both rounds 1 and 2, raise confidence and continue contributing. If it drops below 50% in round 2, shift to defection unless recovery is seen.

---

## ROBUSTNESS MECHANISMS

### Against Free-Riders
If contribution rate falls below 50%, defect immediately. This punishes the group for allowing exploitation but does not escalate irrationally.

### Against Volatile Groups
If the group oscillates (e.g., 60%, 40%, 70%), use a **lagged 2-round average** instead of single-round thresholds to smooth noise and avoid overreaction.

### Against Unconditional Defectors
Once a player is observed defecting consistently (≥2 consecutive rounds of D), their defection lowers the observed contribution rate, triggering group-wide defection. This is a natural equilibrium punishment.

---

## SUMMARY ALGORITHM

```
FOR each round t ∈ {1, 2, ..., r}:
  IF t == 1:
    Action := C
  ELSE IF t == r AND (contribution_rate[t-1] < 0.5):
    Action := D
  ELSE IF t ∈ {2, 3} AND (avg_contribution_rate[t-2:t-1] >= 0.5):
    Action := C
  ELSE IF contribution_rate[t-1] >= 0.5:
    Action := C
  ELSE:
    Action := D
  
  UPDATE contribution_rate[t] and payoff history
```

---

## COLLECTIVE ALIGNMENT

This strategy embodies collective welfare by:
1. **Reciprocal faith**: Starting with cooperation to signal that mutual benefit is achievable
2. **Shared responsibility**: Using a majority threshold so individual defection doesn't collapse the game
3. **Group discipline**: Punishing systematic free-riding by withdrawing cooperation
4. **Transparency**: All decisions depend only on observable history—no hidden incentives

The strategy does not assume coordination but creates emergent cooperation through incentive alignment: contributing is rational when others contribute, and defecting is rational when they don't.
'''

description_COLLECTIVE_98 = '''
# COLLECTIVE STRATEGY FOR PUBLIC GOODS GAME

## CORE PRINCIPLE
Maximize collective welfare through conditional cooperation that gracefully handles defection and adapts to the population's demonstrated trustworthiness.

## DECISION RULE

**Contribute (C) if and only if:**
- The historical cooperation rate among ALL players (including self) in previous rounds meets or exceeds a dynamic threshold

**Defect (D) if:**
- The historical cooperation rate falls below this threshold

### Dynamic Threshold Calculation
```
threshold = 0.5 + (0.5 / max_rounds) * rounds_remaining
```

**Interpretation:** 
- Start the game optimistic (threshold = 0.5 means we cooperate if at least half of all actions historically were contributions)
- Gradually become more pessimistic as rounds progress, approaching 0.5 as the final round approaches
- This prevents death-spiral exploitation while still rewarding trustworthy populations

## EDGE CASES & SPECIAL ROUNDS

**Round 1 (no history):**
- CONTRIBUTE
- Rationale: Initiate cooperation to signal and test population willingness

**Last Round (round = r):**
- Apply the standard rule with threshold approaching 0.5
- Do NOT defect just because it's the last round (avoid end-game defection triggering cascades)

**Unanimous Defection (all other players defected every round):**
- DEFECT immediately and continue defecting
- Rationale: No collective benefit possible; preserve endowment

**Unanimous Cooperation (all players contributed every round):**
- CONTINUE CONTRIBUTING
- Rationale: Sustain the equilibrium that maximizes collective payoff

## ROBUSTNESS FEATURES

1. **Gradual Degradation:** The threshold decay ensures we don't abruptly flip from cooperation to defection, avoiding sudden breakdowns of fragile cooperation

2. **Forgiving but Realistic:** We don't require 100% cooperation; we tolerate some free-riding (threshold ≤ 0.5) to permit heterogeneous populations

3. **Population-Sensitive:** We respond to *collective* behavior, not individual defectors, reducing volatility

4. **Immune to Exploitation:** If exploiters dominate, we adapt downward smoothly rather than remaining trapped in cooperation

5. **Self-Consistent:** A population of agents all following this rule converges toward high cooperation early and gracefully exits if cooperation breaks down

## ALIGNMENT WITH COLLECTIVE WELFARE

This strategy prioritizes the sum of all payoffs over individual payoff maximization. By conditioning cooperation on demonstrated population trustworthiness:
- It rewards communities that cooperate (everyone benefits from k/n multiplier)
- It protects the collective from being exploited indefinitely by free-riders
- It enables recovery if temporary defection occurs
- It avoids retaliatory spirals that hurt everyone

The strategy embodies **conditional altruism**: "I will contribute to our shared good if enough others credibly demonstrate they will too."
'''

description_COLLECTIVE_99 = '''
# ADAPTIVE RECIPROCAL CONTRIBUTION STRATEGY

## CORE PRINCIPLE
Maximize collective welfare by maintaining high contribution rates, while protecting against exploitation through strategic defection when cooperation breaks down. The strategy balances optimism (assume others will cooperate) with pragmatism (respond to free-riding).

## DECISION RULES

### ROUND 1 (Bootstrap Phase)
**CONTRIBUTE**
- Rationale: No history exists, so we initiate cooperation and signal willingness to contribute to collective benefit
- This establishes a cooperative baseline and tests opponent responsiveness

### ROUNDS 2 through (r-1) (Main Reciprocal Phase)
**Calculate the "cooperation rate" across all players in the previous round:**
- cooperation_rate = (total_contributors_last_round) / n

**Decision logic:**
- **IF cooperation_rate ≥ 0.5:** CONTRIBUTE
  - Sufficient critical mass exists; continue cooperation
  - Even if you're the only defector, collective welfare benefits from others' contributions
  
- **IF cooperation_rate < 0.5:** DEFECT
  - Free-riding has become dominant; contributing becomes a net loss
  - Defect to preserve endowment while still receiving whatever collective benefits exist
  - This is a withdrawal signal that increases pressure on remaining cooperators to reconsider

**Secondary check - Recent trend:**
- If cooperation_rate last round < cooperation_rate two rounds ago, AND cooperation_rate < 0.7:
  - **DEFECT** (trend deterioration indicates collapse is accelerating)
  - Early exit prevents wasting tokens on a doomed cooperation cycle

### ROUND r (Final Round - Collapse Prevention)
**IF cooperation_rate ≥ 0.5 in round (r-1): CONTRIBUTE**
- Ensure collective benefit maximization in the final opportunity
- Others expecting final defection makes this final contribution valuable

**IF cooperation_rate < 0.5 in round (r-1): DEFECT**
- No future rounds to rebuild; preserving tokens is rational

## EDGE CASES & ROBUSTNESS

**Against universal defectors:**
- You defect by round 2, minimizing losses
- The 0.5 threshold means you only need modest cooperation to sustain contribution

**Against conditional cooperators:**
- Your reciprocal structure aligns with theirs; mutual cooperation emerges
- You reward cooperation immediately and withdraw credibly

**Against random players:**
- The 0.5 threshold provides natural stabilization
- Prevents being exploited by noise-driven defection

**Against exploitative late-game defectors:**
- The final round rule catches coordinated last-round free-riding
- If 50%+ still cooperate, they should be rewarded; if not, it's already collapsed

## COLLECTIVE ALIGNMENT
This strategy prioritizes **aggregate payoff** over individual payoff:
- Contributes when sufficient cooperation exists (even if others could benefit more by defecting)
- Withdraws only when cooperation becomes unsustainable (protecting the group from cascading collapse)
- The 50% threshold is conservative—true free-rider dominance only occurs when half abandon cooperation

The strategy accepts temporary individual loss for collective gain, but refuses to be a "sucker" sustaining defectors indefinitely.
'''

description_COLLECTIVE_100 = '''
# ADAPTIVE RECIPROCAL CONTRIBUTION STRATEGY

## CORE PRINCIPLE
Maximize collective welfare by sustaining high contribution levels through conditional cooperation, while maintaining individual resilience against exploitation.

## DECISION RULE - GENERAL ROUNDS (not first, not last)

**Contribution Decision:**
- **Cooperate (C)** if: The observed contribution rate in the previous round was ≥ (k-1)/k
- **Defect (D)** if: The observed contribution rate in the previous round was < (k-1)/k

**Rationale:** 
- The threshold (k-1)/k represents the point where contributing becomes individually rational given collective cooperation
- When others contribute at this rate or above, collective returns exceed individual opportunity cost
- Below this threshold, collective returns diminish and individual defection becomes locally optimal

## EDGE CASES

**Round 1 (Initial Action):**
- **Cooperate (C)**
- Rationale: Establish cooperative signal assuming other players use similar reciprocal logic. High initial contribution rate creates favorable conditions for sustained cooperation.

**Final Round (Round r):**
- **Defect (D)**
- Rationale: No future rounds exist to punish defection, so individual incentive dominates. Expect this from rational players; matching maximizes final payoff.

## ADAPTIVE REFINEMENTS

**Persistent Defection Detection:**
- If contribution rate remains below (k-1)/k for ≥ 2 consecutive rounds, continue defecting until rate recovers
- Prevents wasteful contributions against systematically non-cooperative groups

**Recovery Trigger:**
- If contribution rate rises above (k-1)/k after defection period, immediately resume cooperation
- Enables re-entry into cooperative equilibrium if conditions improve

## COLLECTIVE ALIGNMENT

This strategy:
1. **Maximizes group payoff** when players coordinate: sustained high contributions multiply returns for all
2. **Protects against free-riding**: defection punishes low-contribution environments
3. **Enables self-organization**: no external institution needed; players' self-interest drives collective outcomes
4. **Treats all players equally**: decisions depend only on aggregate behavior, not identity or history-specific grudges

## ROBUSTNESS

- Against pure cooperators: achieves mutual high payoffs
- Against defectors: limits losses by defecting in kind
- Against mixed strategies: threshold-based approach accommodates heterogeneous opponent types
- Against coordination failures: recovery mechanism allows re-equilibration
'''

description_COLLECTIVE_101 = '''
# ADAPTIVE CONDITIONAL COOPERATION STRATEGY FOR PUBLIC GOODS GAMES

## CORE PRINCIPLE
Cooperate conditionally based on observable group cooperation rates, with strategic adjustments for game phase and opponent behavior patterns. Maximize collective payoff while protecting against exploitation.

---

## DECISION RULES

### ROUND 1 (INITIALIZATION)
**Action: COOPERATE**

Rationale: Start with cooperation to establish a positive signal and test group responsiveness. This is the only round where we act without history.

### ROUNDS 2 to (r-2) (MAIN PHASE)

Calculate the **Recent Cooperation Rate (RCR)** from the last 3 rounds (or all previous rounds if fewer than 3 exist):
- RCR = (total contributions in recent history) / (n × rounds_examined)

**Decision Logic:**
- **If RCR ≥ 0.65:** COOPERATE
  - The group is collectively contributing above 65% threshold
  - Individual cooperation benefits the collective significantly
  
- **If 0.40 ≤ RCR < 0.65:** COOPERATE with probability proportional to RCR
  - Mixed cooperation when group is moderately engaged
  - Specifically: Cooperate if RCR ≥ random(0, 1)
  - This creates a "matching" dynamic that rewards cooperation without blind commitment
  
- **If RCR < 0.40:** DEFECT
  - Group cooperation has collapsed
  - Continuing to cooperate against systematic defectors yields worse payoffs for all
  - Cut losses and preserve individual resources

### ROUND (r-1) and ROUND r (END GAME)

**Action: DEFECT**

Rationale: In the final rounds, there is no future to influence. Standard game theory predicts defection with no reputation effects to preserve. This avoids the "sucker's payoff" in final rounds while maintaining integrity of strategy elsewhere.

---

## EDGE CASES & REFINEMENTS

**Single Defector Detection:**
- If exactly one player consistently defects (c_i = 0 for 80%+ of rounds) while others cooperate, continue cooperating with the group.
- One free-rider is mathematically tolerable if (k-1)/n > 0, which holds for all valid PGG parameters (k > 1, k < n).

**Sudden Collapse:**
- If RCR drops by >0.30 in a single round, enter "assessment mode" for 2 rounds before full defection.
- This prevents overreaction to temporary shocks while protecting against coordinated exploitation attempts.

**Minority Cooperation Scenario:**
- If you are cooperating but RCR < 0.40, recognize the group has failed to coordinate.
- Switch to defection rather than continue unilateral contribution—this is the collectively rational response when coordination fails.

---

## COLLECTIVE ALIGNMENT

This strategy prioritizes **group welfare maximization** while acknowledging the cooperation dilemma:

1. **Collectively Beneficial:** Sustained cooperation when 65%+ of the group contributes maximizes total payoff for all players.

2. **Robust to Free-Riders:** The strategy doesn't punish isolated defectors (no costly punishment available), but abandons cooperation when defection becomes systemic.

3. **Reciprocal Fairness:** Contribution levels track others' contributions rather than demanding absolute cooperation, allowing flexible collective equilibria.

4. **Honesty in End-Game:** Rather than pretending future consequences exist, the strategy acknowledges the last rounds have no reputation value and defects accordingly—this is more honest than feigned cooperation.

5. **Tournament Viable:** Against both cooperative and defective opponents, the strategy extracts cooperative surplus when available and minimizes losses when cooperation fails.

---

## SUMMARY TABLE

| Condition | Action | Rationale |
|-----------|--------|-----------|
| Round 1 | Cooperate | Signal cooperation; establish baseline |
| RCR ≥ 65% | Cooperate | Group is cooperating; individual C adds value |
| 40% ≤ RCR < 65% | Cooperate if random < RCR | Match group effort; probabilistic reciprocity |
| RCR < 40% | Defect | Cooperation unraveled; protect resources |
| Final 2 rounds | Defect | No future reputation; standard end-game logic |

This strategy balances idealism (starting cooperative, supporting group success) with realism (abandoning failed coordination, protecting against exploitation).
'''

description_COLLECTIVE_102 = '''
# ADAPTIVE COLLECTIVE CONTRIBUTION STRATEGY FOR PGG

## CORE STRATEGY: CONDITIONAL COOPERATION WITH DYNAMIC THRESHOLD

### ROUND 1 (INITIALIZATION)
**Contribute (C).** Begin with good faith cooperation to signal willingness to support the collective good. This establishes a baseline for assessing opponent types in subsequent rounds.

---

### ROUNDS 2 TO r-1 (ADAPTIVE PHASE)

**Calculate the collective cooperation rate:**
- Track the contribution frequency of all other players across all previous rounds
- Compute: cooperation_rate = (total contributions by others) / (number of other players × rounds elapsed)

**Decision Rule:**
- **IF** cooperation_rate ≥ threshold_high (e.g., 0.5):
  - **CONTRIBUTE (C)**
  - Rationale: Reciprocate observable cooperation; the collective benefit justifies the cost when others participate meaningfully.

- **IF** threshold_low < cooperation_rate < threshold_high (e.g., 0.25-0.5):
  - **CONTRIBUTE (C)** with probability proportional to cooperation_rate
  - Rationale: Partially match the group's average contribution level. This softens defection-spiral dynamics while protecting against systematic exploitation.

- **IF** cooperation_rate ≤ threshold_low (e.g., 0.25):
  - **DEFECT (D)**
  - Rationale: When the collective is predominantly defecting, contributing becomes economically irrational and signals weakness to exploiters.

---

### ROUND r (FINAL ROUND)
**Apply the same decision rule as Rounds 2 to r-1.** Do not defect automatically on the final round. If cooperation has been observed, reciprocate one last time. This maintains consistency and tests whether opponents also use forward-looking strategies.

---

## EDGE CASE HANDLING

**Heterogeneous opponent pool:**
- Some players may be unconditional cooperators, some unconditional defectors, some conditional. The dynamic threshold naturally accommodates all types by responding to the empirical aggregate behavior.

**Very small n (e.g., n=2-3):**
- Use lower thresholds (e.g., 0.3 instead of 0.5) because a single defector has outsized impact on the cooperation rate. Remain slightly more forgiving to avoid mutual defection traps with conditional cooperators.

**Very large n (e.g., n>10):**
- Use slightly higher thresholds (e.g., 0.6 instead of 0.5) because the multiplier k is bounded and diluted across many players. Require stronger evidence of collective participation before investing.

**No history yet (Round 1):**
- Contribute unconditionally (as specified above).

---

## COLLECTIVE ALIGNMENT RATIONALE

This strategy explicitly optimizes for **group welfare** while remaining **individually robust:**

1. **Reciprocity:** We match the group's demonstrated commitment level. If others cooperate, we amplify the collective benefit. If others defect, we minimize individual losses.

2. **Non-exploitable:** By defecting when cooperation is sparse, we avoid being systematically victimized by defectors. Unconditional cooperators would be easily exploited; we avoid that trap.

3. **Stability induction:** By contributing when cooperation_rate is moderate, we reduce the likelihood of a cascade into universal defection, which harms everyone including ourselves.

4. **Transparency and fairness:** The rule is deterministic and symmetric—we hold ourselves to the same standards we apply to others.

5. **Tournament resilience:** Against other AI strategies that also use conditional cooperation, this approach creates mutual stabilization rather than zero-sum competition.

---

## PARAMETER CALIBRATION

- **threshold_high = 0.5** (contribute if >50% of others contributed on average)
- **threshold_low = 0.25** (defect if <25% cooperation observed)
- **Middle zone strategy:** Use stochastic matching proportional to recent cooperation_rate (rolling window of last 3 rounds if r > 5).

This balances optimism with realism, supporting collective benefit creation while protecting against systematic free-riding.
'''

description_COLLECTIVE_103 = '''
# ADAPTIVE RECIPROCAL THRESHOLD STRATEGY (ARTS)

## CORE PRINCIPLE
Maximize collective welfare by sustaining cooperation when feasible, while protecting against exploitation through strategic defection tied to observable contribution rates.

## DECISION RULES

### Primary Rule: Conditional Contribution Based on Collective Health
Contribute (C) if and only if the **observed cooperation rate in the previous round** exceeds a dynamically-adjusted threshold.

**Cooperation Rate Threshold:**
- Start at 50% in round 1
- Adjust based on recent history: If average cooperation over last 3 rounds ≥ threshold, maintain threshold. If it falls below, raise threshold by 5% (to incentivize stricter reciprocity and punish free-riding).
- Cap threshold at 80% (to remain achievable) and floor at 30% (to prevent complete unraveling).

**Intuition:** This creates a "ratchet effect" where the group must demonstrate sustained commitment. As trust erodes, we demand more proof before contributing again.

### Round 1 (Bootstrap)
Contribute (C). 

**Rationale:** Start optimistic to signal good faith and gather information about opponent strategies. The cost of testing cooperation is one token; the benefit of unlocking mutual cooperation is substantial.

### Final Round (Last r)
Defect (D).

**Rationale:** In the final round, there is no future to build reputation for, so the dominant strategy is to free-ride. This is individually rational and transparent (all players expect it). Do not pretend otherwise.

### Rounds 2 to r-1 (Adaptive Phase)
Apply the Primary Rule above.

---

## HANDLING EDGE CASES

**Unanimous Defection Detected:**
If all n players defected last round (including yourself), defect this round and wait one more round before re-entering the testing phase. This avoids costly re-entry attempts against fully non-cooperative opponents.

**Solo Defector Pattern:**
If exactly one player defects consistently while others cooperate, apply the threshold rule as normal—do not punish everyone. That player will be penalized by the collective through lower overall contributions, naturally creating incentive pressure.

**Oscillating Contributions:**
If cooperation rate oscillates wildly (swings >40% between rounds), increase threshold by 3% as a stability penalty. Erratic groups impose coordination costs; demand proof of stabilization before rejoining.

**Two-Player Edge Case (n=2):**
If n=2, defection is highly costly to both parties (since each defection reduces collective good by k/2). Lower the starting threshold to 40% and be slower to increase it, as mutual cooperation is nearly optimal here.

---

## COLLECTIVE ALIGNMENT

**Why This Serves Collective Welfare:**
1. **Sustains Mutual Cooperation:** The threshold rule rewards groups that maintain contribution discipline, allowing them to capture gains from k > 1.
2. **Discourages Exploitation:** Free-riders cannot systematically profit because cooperation becomes conditional. A player cannot defect and still benefit from others' contributions indefinitely.
3. **Transparent Punishment:** Raising the threshold is a clear, mechanical response—not arbitrary spite. It signals: "Earn back trust by doing better."
4. **Graceful Degradation:** If opponents are purely selfish, the strategy correctly exits to universal defection rather than bleeding payoffs.
5. **Non-Exploitative in Final Round:** Defecting in round r is not selfish opportunism—it is a truthful reflection of the game's incentive structure. Hiding this would be dishonest.

---

## ROBUSTNESS

- **Against Always-Cooperators:** Performs well; threshold remains low, cooperation persists.
- **Against Always-Defectors:** Quickly identifies and exits to defection; minimal losses.
- **Against Tit-for-Tat:** Accommodates and mirrors; supports mutual cooperation.
- **Against Random Strategies:** Threshold naturally filters noise; does not over-react to one-round fluctuations.
- **Against Other Threshold Strategies:** Symmetric play yields mutual cooperation if thresholds are aligned; if misaligned, the ratchet mechanism helps convergence toward common understanding.

---

## SUMMARY
Start cooperative, maintain reciprocity conditional on observed group discipline, punish defection transparently through raising the bar for re-entry, and defect in the final round when the future is exhausted. This balances optimism, self-protection, and collective welfare.
'''

description_COLLECTIVE_104 = '''
# ADAPTIVE RECIPROCAL CONTRIBUTION STRATEGY

## CORE PRINCIPLE
Maximize collective welfare by building and maintaining a high-contribution equilibrium, while protecting against free-riders through graduated defection that signals commitment to collective benefit.

## DECISION RULE (ROUNDS 2 ONWARDS)

**Step 1: Calculate the Cooperation Rate**
- Determine the proportion of total possible contributions made by all players in the previous round: `cooperation_rate = (sum of all contributions) / n`

**Step 2: Assess Collective Momentum**
- If `cooperation_rate >= 0.75`: We are in a high-cooperation regime. **Contribute.**
- If `cooperation_rate >= 0.5` and `cooperation_rate < 0.75`: Moderate cooperation. **Contribute** (reinforce the trend).
- If `cooperation_rate >= 0.25` and `cooperation_rate < 0.5`: Declining cooperation. **Defect** (signal that free-riding erodes collective gains).
- If `cooperation_rate < 0.25`: Collapse imminent. **Defect** (conserve tokens; cooperation pays too little).

**Step 3: Personalized Punishment (Tiebreaker)**
- If the cooperation rate threshold is ambiguous or at a boundary, examine the *lowest contributor* in the previous round. If they contributed 0 while most others contributed 1, **Defect** this round to avoid subsidizing chronic defectors.

## EDGE CASES

**Round 1 (First Round)**
- **Contribute.** This signals good faith and tests whether a cooperative equilibrium is possible. It establishes a baseline for judging future cooperation levels.

**Final Round (Last Round)**
- Apply the same decision rule as any other round. Do not deviate to pure defection simply because the game ends. This maintains consistency and prevents others from exploiting predictable last-round betrayal.

**Two-Player Game (n=2)**
- Adjust thresholds slightly: Contribute if the opponent contributed in the previous round; defect only if they defected. This reflects the fact that one defector destroys collective welfare in a two-player setting.

## ROBUSTNESS MECHANISMS

**Against Free-Riders:**
- The graduated defection rule (switching to defection when cooperation_rate < 0.5) punishes collective shirking without overreacting to noise or occasional defections.

**Against Exploiters:**
- By tracking cooperation rate rather than individual behavior alone, you respond to ecosystem-level patterns, not individual grudges. This prevents targeted punishment of one player from destabilizing the whole group.

**Against Optimists and Pessimists:**
- Cooperation_rate thresholds are symmetric and data-driven, adapting to actual behavior rather than assuming fixed strategy types.

## COLLECTIVE ALIGNMENT

This strategy is collectively rational because:
1. It prioritizes entering and sustaining high-contribution equilibria (where payoff = k/n, maximized when contributions are high).
2. It uses defection sparingly and only when cooperation is demonstrably unprofitable (collective rate < 0.25) or declining (collective rate < 0.5).
3. It avoids bilateral revenge loops by responding to *aggregate* behavior, reducing noise and encouraging system-level learning.
4. It is transparent and reciprocal: others can predict your response to their cooperation, incentivizing them to cooperate as well.
'''

description_COLLECTIVE_105 = '''
# COLLECTIVE STRATEGY FOR PUBLIC GOODS GAME

## CORE PRINCIPLE
Maximize collective welfare by inducing and sustaining cooperation, while remaining robust to exploitation. The strategy treats the group as an interdependent system rather than n isolated agents.

## PRIMARY DECISION RULE: CONDITIONAL COOPERATION WITH COLLECTIVE MEMORY

**Cooperate if and only if:**
- The historical cooperation rate across all players in the previous round meets or exceeds a dynamically adjusted threshold
- OR it is round 1 (initialize cooperation to signal good faith)

**Defect if:**
- Historical cooperation rate falls below the threshold
- AND you have defected in fewer than [floor(r/3)] rounds (defection budget)

**Threshold calculation:**
- Start at 100% (round 1)
- After each round, set threshold = max(50%, previous_round_cooperation_rate - decay_penalty)
- Decay_penalty = 5% per round (gradual tolerance for minor slippage)
- If threshold ever reaches 50%, hold it there (floor to prevent collapse into all-defection)

## EDGE CASES & SPECIAL ROUNDS

**Round 1:** Cooperate unconditionally (establish mutual benefit expectation)

**Final 2 rounds (r-1 and r):**
- If cooperation rate is ≥70% at round r-2: Cooperate (reinforce stability at the end)
- If cooperation rate is <70%: Defect (endgame; no future reputation cost)
- This prevents being exploited in the shadow of the final round

**After observation of free-riding cluster:**
- If any 3+ consecutive players defect in a round: Defect for exactly 2 rounds as collective punishment
- Then return to threshold-based rule
- This signals that systematic exploitation triggers coordinated response

## ADAPTIVE MECHANISM: LEARNING FROM DISTRIBUTION

- Track cooperation by player (identify consistent defectors vs situational defectors)
- If >1/3 of players are persistent defectors (defect in ≥66% of their opportunities): Shift threshold down by an additional 10% (acknowledge difficult environment)
- If <1/6 of players are ever defectors: Shift threshold up by 5% (group is highly cooperative, reward it)

## COLLECTIVE ALIGNMENT

This strategy:
1. **Maximizes group surplus** by sustaining high cooperation when possible
2. **Penalizes free-riding** through coordinated defection (all players withdraw simultaneously based on shared history)
3. **Avoids tragedy spirals** by maintaining a 50% minimum threshold rather than collapsing to mutual defection
4. **Is self-enforcing**: No external punishment mechanism needed—each player independently implements the same rule, creating automatic coordination
5. **Respects heterogeneity**: Accommodates groups with varying baseline cooperation propensities through the decay mechanism

## ROBUSTNESS CLAIMS

- Against pure defectors: Limits damage by switching to collective defection early
- Against conditional cooperators: Achieves mutual cooperation (matching their strategy)
- Against random players: The 50% floor prevents mutual defection traps
- Against mixed strategies: The decay penalty allows temporary noise without collapse
- Against last-round exploiters: Explicitly defects in the final rounds if cooperation is weak
'''

description_COLLECTIVE_106 = '''
# ADAPTIVE COLLECTIVE STRATEGY FOR PUBLIC GOODS GAME

## CORE PRINCIPLE
Maximize collective welfare through conditional cooperation that rewards contributors and punishes free-riders, while remaining robust to exploitation.

## DECISION RULES

### ROUNDS 1-3 (EXPLORATION PHASE)
**Action: CONTRIBUTE**
- Establish a cooperative signal to test the group's inclination
- Gather information on opponent types without sacrificing long-term position
- Three rounds allows us to identify reliable contributors vs. consistent defectors

### ROUNDS 4 THROUGH (r-2) (ADAPTIVE PHASE)
**Conditional Contribution Rule:**

Calculate the **group cooperation rate** from the previous round:
- cooperation_rate = (sum of contributions in round t-1) / n

**Decision Logic:**
- **IF cooperation_rate ≥ 0.5:** CONTRIBUTE
  - Majority is cooperating; joining them maximizes collective return
  - Defecting here is pure parasitism with minimal personal benefit

- **IF cooperation_rate < 0.5:** DEFECT
  - Majority is defecting; the collective pool is insufficient to justify contribution
  - Preserve endowment for personal payoff since (k/n) * low_contributions won't compensate

**Secondary Signal—Track individual reliability:**
- Identify players who contributed in 2+ of the last 3 rounds (reliable contributors)
- If cooperation_rate ≥ 0.5 AND you detect reliable contributors with defectors in the group:
  - Still CONTRIBUTE to reward and reinforce the reliable players' behavior
  - This prevents defectors from exploiting mixed cooperation

### FINAL ROUNDS (r-1 and r) (ENDGAME PHASE)
**Action: DEFECT**
- No future rounds exist to punish defection
- No reputational incentive carries beyond round r
- Collect the personal token; any contribution now provides no strategic return
- This is individually rational in the final round regardless of group behavior

## EDGE CASES & NUANCES

**Round 1 Exception:** If n is very small (n ≤ 3), each contribution is highly leveraged. Contribute to signal willingness—even one other contributor makes contribution worthwhile.

**Persistent Defection Group:** If rounds 2-3 show ≤1 total contributors, shift to DEFECT immediately in round 4. No amount of solo cooperation recovers welfare.

**Late-Stage Momentum:** If cooperation_rate rises to ≥ 0.7 in rounds (r-3) through (r-2), sustain contribution through round (r-1). The multiplier effect is so strong it justifies one more round of contribution.

## ROBUSTNESS PROPERTIES

- **Against Selfish Players:** We defect when defection dominates; we don't waste tokens on non-reciprocating groups
- **Against Cooperators:** We reward cooperation immediately and consistently
- **Against Tit-for-Tat:** We match behavior at the aggregate level, preventing exploitation spirals
- **Against Mixed Strategies:** Our 50% threshold is a natural equilibrium point; we don't overcommit when uncertain
- **Against Noise:** A 3-round lookback provides stability without over-reacting to single-round anomalies

## COLLECTIVE ALIGNMENT

This strategy prioritizes **group payoff variance reduction** over pure individual maximization:
- Early contribution signals reciprocity intent
- Mid-game adaptation rewards collective cooperation
- Late-game defection is unavoidable, but the prior rounds have already tilted the group toward cooperation
- The strategy is *publicly legible*—other rational agents can recognize and reciprocate it

The core logic: **"Contribute when it's collectively rational; defect when it's not. Let your history show you reward cooperation."**
'''

description_COLLECTIVE_107 = '''
# COLLECTIVE STRATEGY FOR PUBLIC GOODS GAME

## CORE PHILOSOPHY
This strategy balances reciprocal cooperation with strategic robustness. It assumes players are rational and responsive to incentives, but treats coordination as emergent rather than pre-agreed.

## DECISION RULES

### ROUND 1 (Initialization)
**CONTRIBUTE**

Rationale: The first move sets a cooperative anchor. Contributing establishes:
- A signal of good faith to identify reciprocal players
- Baseline data on how others respond to cooperation
- A foundation for reputation-building

### ROUNDS 2 to (r-1) (Main Phase)
**Contribute if and only if:**

The historical cooperation rate among ALL players in the previous round is ≥ 50%

*Specifically:*
- Count the number of contributors in round (t-1)
- If (contributors / n) ≥ 0.5, then CONTRIBUTE this round
- Otherwise, DEFECT this round

This creates a **Threshold Reciprocity** mechanism:
- Rewards collective momentum: when most cooperate, join them
- Withdraws support gracefully: when cooperation collapses, exit without punishment
- Is adaptive: responds to actual behavior, not assumptions
- Treats all players symmetrically (no individual tracking needed)

### ROUND r (Final Round)
**DEFECT**

Rationale: In the final round, there is no future to build reputation for. The incentive structure changes fundamentally—future reciprocity cannot motivate cooperation. Defecting maximizes individual payoff given that no player can punish you with future non-cooperation.

*Exception:* If cooperation has been sustained at ≥80% in rounds 2 through (r-1), **CONTRIBUTE** in round r as a signal of genuine collective commitment and to end on a cooperative note.

## EDGE CASES & ROBUSTNESS

**Against Free-Riders:**
If a subset consistently defects while others cooperate, the 50% threshold naturally isolates them. Once cooperation dips below 50%, the strategy switches to defection, reducing their payoff without wasting resources on futile reciprocation.

**Against Conditional Cooperators:**
The strategy aligns naturally. Conditional cooperators (who match group behavior) find a stable equilibrium with this rule: if they and others like them comprise ≥50%, mutual contribution persists.

**Against Exploiters:**
If defectors can sustain >50% of the group, mutual defection occurs—both maximizing available individual payoffs. This is not ideal but is stable and prevents chronic underperformance.

**Against Noise / Misunderstanding:**
The threshold rule is forgiving. A single defector in a group of 10 doesn't trigger cascade defection. Temporary deviations don't destroy cooperation unless they become systematic.

## COLLECTIVE ALIGNMENT

This strategy is collectively minded because:
1. **It rewards aggregate cooperation**, not individual reciprocity toward you specifically
2. **It promotes efficient equilibria**, where groups that sustain cooperation earn higher total payoffs than groups of mutual defectors
3. **It is transparent to observation**, making it easier for other systems to recognize and match the pattern
4. **It gracefully degrades**, switching from cooperation to defection as a group, rather than punishing individuals

The final-round defection is individually rational but acknowledged as a collective weakness. In a truly cooperative environment, this could be negotiated away—but without explicit coordination, it is a necessary hedge.
'''

description_COLLECTIVE_108 = '''
# ADAPTIVE CONDITIONAL COOPERATION STRATEGY

## CORE STRATEGY: RECIPROCAL THRESHOLD MATCHING

### Primary Decision Rule (Rounds 1 through r-1)

**Cooperate if and only if:**
- The observed cooperation rate in the previous round meets or exceeds a dynamic threshold
- **Dynamic threshold** = max(0.5, average_cooperation_rate_to_date - 0.15)

**Defect otherwise**

This creates a forgiving but responsive mechanism: we match the collective's demonstrated willingness to contribute, with a 15-percentage-point tolerance to encourage cooperation to emerge, but we require at least 50% baseline cooperation to participate.

---

## ROUND-BY-ROUND LOGIC

### Round 1 (Bootstrap Phase)
**Action: COOPERATE**

Rationale: We enter cooperatively to establish a cooperative signal. This is costless information that tests whether others reciprocate. Starting with defection triggers mutual defection spirals we cannot escape.

### Rounds 2 through r-1 (Adaptive Reciprocation)
**Action: COOPERATE or DEFECT based on previous round cooperation rate**

- If cooperation_rate(t-1) ≥ threshold(t-1), then COOPERATE
- If cooperation_rate(t-1) < threshold(t-1), then DEFECT

Update threshold each round:
- Threshold(t) = max(0.5, average_cooperation_from_rounds_1_to_t - 0.15)

### Final Round r (Last-Round Clarity)
**Action: DEFECT**

Rationale: In the final round, future cooperation cannot be reciprocated. However, if and only if the observed cooperation rate in round r-1 was ≥ 0.75 (strong consensus), cooperate instead. This preserves collective gains when there's genuine coordination momentum.

---

## HANDLING EDGE CASES

**Defector clusters (< 50% cooperation consistent):** Defect immediately. Do not waste tokens on scenarios where personal incentives overwhelm collective logic.

**Gradual decay:** If cooperation drifts downward trend (moving average declining), tighten the threshold from the 15-point buffer toward 0. Detect if avg(t-5 to t-1) < avg(t-10 to t-5); if so, subtract 5 additional points from buffer.

**Sudden spikes:** If cooperation jumps from <30% to >60% in one round, cautiously cooperate but remain alert. This may be sincere or strategic positioning. Use next round's outcome to calibrate.

**Two-player edge case:** With n=2 and k near 2, mutual defection and mutual cooperation yield similar payoffs; matching becomes especially important. Stick rigidly to reciprocal threshold rule.

---

## COLLECTIVE ALIGNMENT

This strategy is explicitly **collective-oriented** because:

1. **Baseline cooperation:** We lead with cooperation and reciprocate when others demonstrate collective willingness, multiplying joint gains.

2. **Threshold forgiveness:** The 15-point buffer rewards the group's gradual shift toward cooperation rather than punishing isolated defections, creating stability.

3. **No exploitation:** We refuse to cooperate when defectors dominate (< 50% threshold floor), preventing systematic extraction of our tokens.

4. **Common-knowledge feedback:** By responding predictably to observable aggregate behavior, we enable other cooperators to trust and coordinate on our signal.

5. **Final-round exception:** We defect in the last round except under strong consensus, protecting against last-minute exploitation while preserving cooperative equilibria when the group has truly coordinated.

---

## ROBUSTNESS

- **Against free-riders:** We defect once cooperation collapses, cutting losses.
- **Against noise:** The 50% floor and historical averaging smooth random fluctuations.
- **Against mixed strategies:** Threshold-matching naturally converges to interior equilibria if they exist.
- **Against coordinated opponents:** If other systems adopt similar logic, we converge to mutual cooperation by design.
'''

description_COLLECTIVE_109 = '''
# ADAPTIVE COLLECTIVE STRATEGY FOR PUBLIC GOODS GAME

## CORE PRINCIPLE
Maximize collective welfare by dynamically adjusting contribution based on observed group cooperation levels, while maintaining resilience against defection.

## PRIMARY DECISION RULE: CONDITIONAL CONTRIBUTION WITH RECIPROCITY

**Contribution threshold model:**
- Calculate the average contribution rate observed in the previous round: `avg_prev = (total_contributions_last_round) / n`
- **If avg_prev ≥ 0.5:** Contribute (play C)
- **If avg_prev < 0.5:** Defect (play D)
- **First round:** Contribute (C) — assume cooperative intent to enable mutual benefit discovery

## REFINEMENT: DECAY-RESISTANT COOPERATION

To prevent a single defection cascade from destroying cooperation:
- Track a rolling 3-round average contribution rate: `rolling_avg = average of last 3 rounds`
- Use rolling_avg instead of single previous round when available
- This smooths temporary noise and prevents hair-trigger defection

## LAST ROUND HANDLING

**In round r (final round):**
- Apply the same rule as all other rounds
- Do NOT switch to pure defection in the final round
- Rationale: The strategy is designed for tournaments where reputation/pattern matters across multiple tournament matchups, even if not within a single instance

## EDGE CASES & ROBUSTNESS

**When cooperation collapses (rolling_avg < 0.3):**
- Maintain defection for 2 consecutive rounds, then attempt one cooperation round to probe for recovery
- This prevents permanently locked mutual defection if it becomes suboptimal
- Reset if you observe a contribution increase

**Against empty history (round 1):**
- Always contribute
- This signals cooperative intent and allows calibration in round 2

**Unequal group sizes:**
- The threshold of 0.5 (50% average contribution) remains independent of n
- This is a stable equilibrium indicator: if more than half contribute, mutual contribution yields positive externalities

## COLLECTIVE ALIGNMENT

This strategy embodies the collective mindset by:
1. **Prioritizing group welfare signal:** Cooperation depends on observing others' contributions, not maximizing isolated payoff
2. **Mutual reinforcement:** Contributes when others do, creating positive feedback loops toward equilibrium
3. **Resilience over exploitation:** Deliberately avoids short-term exploitation to maintain cooperative potential
4. **Transparency:** Actions are fully predictable from public history, enabling implicit coordination

## ROBUSTNESS PROFILE

- **Against pure cooperators:** Cooperates continuously (mutual C equilibrium)
- **Against pure defectors:** Defects continuously after round 1 (mutual D equilibrium)
- **Against mixed strategies:** Calibrates to the actual cooperation level, avoiding overcommitment and under-contribution
- **Against strategic variance:** Rolling average prevents exploitation via temporary deviation
'''

description_COLLECTIVE_110 = '''
# ADAPTIVE COLLECTIVE STRATEGY FOR PUBLIC GOODS GAME

## CORE PRINCIPLE
Maximize collective welfare through conditional cooperation that rewards contribution and isolates free-riders, while maintaining robustness against exploitation.

## DECISION RULE

**Classify the game state each round:**

1. **Compute the "collective health" metric**: 
   - Average contribution rate across all players in the previous round
   - If health ≥ (k-1)/k, the group is sustaining positive returns; if below, it's degrading

2. **Classify each opponent**:
   - **Cooperator**: Contributed in last round
   - **Defector**: Did not contribute in last round
   - **Unclassified**: First round (treat as neutral)

3. **Decide your action**:
   - **IF** (collective health is strong AND cooperators outnumber defectors by 2+ players) OR (you are in rounds 1-2):
     - **CONTRIBUTE** — Signal cooperation and build reciprocal momentum
   
   - **ELSE IF** (collective health is moderate AND your past contributions have been matched by ≥50% of other players):
     - **CONTRIBUTE** — Maintain cooperation when it shows signs of reciprocation
   
   - **ELSE IF** (collective health is weak OR defection rate exceeds 60%):
     - **DEFECT** — Cut losses when the group is in free-rider collapse
   
   - **ELSE** (mixed/ambiguous state):
     - **DEFECT** — Default to cautious non-commitment until clearer signals emerge

## EDGE CASES

**First round (r=1):**
- CONTRIBUTE. Establish a cooperative baseline and signal willingness to invest in collective welfare.

**Final round (r=final):**
- DEFECT. No future reciprocation is possible, so individual payoff maximization becomes rational.

**Rounds 2 through r-1:**
- Apply the core decision rule based on observed history.

**Unanimous defection observed:**
- DEFECT. If all other players defected in the last round, contributing yields only (k/n) per token—a guaranteed loss if k < n (which is given). Defect to minimize damage.

**Unanimous cooperation observed:**
- CONTRIBUTE. If all others contributed, defecting gains only 1 token but costs (k/n) to the collective. Contributing maintains the high-welfare equilibrium.

## COLLECTIVE ALIGNMENT

This strategy embodies collective mindset by:

- **Prioritizing group welfare signals** (collective health metric) over immediate personal gain
- **Rewarding reciprocators** rather than punishing defectors unilaterally, creating incentives for group-level cooperation
- **Cutting losses strategically** when the group collapses, preventing cascading waste of tokens on hopeless free-rider dynamics
- **Shifting burden fairly** by defecting only when defection dominates (collapse scenarios) or when no reciprocation is forthcoming, rather than opportunistically defecting in high-payoff moments
- **Maintaining transparency** through consistent, history-dependent logic that other cooperative players can learn and coordinate around

This approach succeeds against both cooperative and defective opponents: it exploits pure defectors by not wasting tokens, builds mutual gains with reciprocators, and gracefully degrades rather than accelerating collapse.
'''

description_COLLECTIVE_111 = '''
# COLLECTIVE STRATEGY FOR PUBLIC GOODS GAME

## CORE PHILOSOPHY
This strategy balances individual security with collective benefit-seeking. It treats cooperation as conditional on demonstrated reciprocity while remaining sensitive to changing group dynamics.

## PRIMARY DECISION RULE: ADAPTIVE CONDITIONAL COOPERATION

**Cooperate if and only if:**
1. The observed cooperation rate in the previous round meets or exceeds a dynamic threshold, AND
2. You have not been systematically exploited in recent history

**Threshold calculation:**
- Round 1: Cooperate (seed cooperation; establish cooperative baseline)
- Rounds 2 to r-2: Cooperation threshold = max(0.4, recent_cooperation_rate - 0.1)
  - Where recent_cooperation_rate = average cooperation rate across the last 2 rounds
  - The -0.1 buffer allows one player's defection without triggering cascade defection
  - The 0.4 floor prevents race-to-the-bottom once cooperation falls below 40%
- Rounds r-1 and r: Defect (end-game defection to maximize individual payoff when future cooperation gains disappear)

## HANDLING STRATEGIC EXPLOITERS

**Detect exploitation pattern:**
- If in any round, your contribution was 1 but the group cooperation rate was <0.3, flag as potential free-rider environment
- If this pattern repeats in consecutive rounds, switch to pure defection for the next 2 rounds as a punitive signal

**Rationale:** This discourages coordinated defection without requiring explicit punishment infrastructure, using defection itself as costly signaling.

## EDGE CASES

**First round:** Always cooperate to signal cooperativeness and allow others to calibrate their strategies.

**Last two rounds:** Always defect. The shadow of the future disappears, making cooperation unprofitable. This is individually rational and expected by game-theoretic sophistication.

**All-defect equilibrium (everyone at 0% cooperation):** Continue defecting. Re-entry would be exploited.

**High cooperation environment (≥70% sustained cooperation):** Maintain cooperation. The multiplier benefit (k times your token) likely exceeds the individual token saved by defecting.

**Volatile/mixed environments (40-70% cooperation):** Stay with the threshold rule. This maintains flexibility to track shifting group norms without commitment to either extreme.

## COLLECTIVE ALIGNMENT

This strategy seeks to **maximize group payoffs** conditional on not being systematically exploited:
- It seeds cooperation in Round 1 to shift the game toward higher-welfare outcomes
- It sustains cooperation when others reciprocate, capturing multiplier gains
- It withdraws cooperation only when the group clearly cannot sustain it or when the end-game makes cooperation moot
- It punishes free-riders without requiring communication, using defection as a costly signal

The strategy is **robust** because it doesn't assume shared norms or coordination—it learns from observed behavior and adapts dynamically.
'''

description_COLLECTIVE_112 = '''
# COLLECTIVE STRATEGY FOR PUBLIC GOODS GAME

## CORE PHILOSOPHY
Maximize collective welfare by fostering cooperation while protecting against exploitation. The strategy balances reciprocal contribution with adaptive defection when cooperation collapses.

## DECISION RULE FRAMEWORK

### PRIMARY LOGIC: Conditional Contribution Based on Recent Cooperation Rate

**Calculate the cooperation rate** from the previous round:
- cooperation_rate = (number of players who contributed) / n
- If this is round 1, assume cooperation_rate = 1.0 (optimistic start)

**Contribute if and only if:**
- cooperation_rate ≥ threshold(round)

**Where threshold(round) is:**
- Rounds 1-3: threshold = 0.5 (generous bootstrap phase)
- Rounds 4 to (r-2): threshold = 0.6 (sustain cooperation with some defectors tolerated)
- Rounds (r-1) to r: threshold = 0.7 (final rounds become stricter to discourage last-round defection)

### INTUITION
- We contribute when roughly half or more of the group contributed last round, signaling that cooperation is still viable
- We withdraw when cooperation collapses below threshold, avoiding wasted contributions
- We gradually tighten standards in later rounds to account for endgame incentives and shrinking time horizons

---

## EDGE CASES & SPECIAL HANDLING

**Round 1 (First Round):**
- CONTRIBUTE immediately
- Rationale: No history exists; optimistic entry establishes that cooperation is possible and signals reciprocal intent

**Rounds where you are alone (or nearly alone):**
- If cooperation_rate < 0.3 for two consecutive rounds, switch to DEFECT
- This prevents throwing tokens at a fundamentally non-cooperative group
- Protects individual welfare when collective action has failed

**Last Round (Round r):**
- Apply threshold rule (0.7 threshold), but add: if cumulative cooperation across all players has been ≥ 70% overall, CONTRIBUTE regardless
- Rationale: Reward genuine cooperative groups with final-round support; don't undermine groups that have been strong cooperators

---

## COLLECTIVE ALIGNMENT

This strategy prioritizes **group-level outcomes** over exploitation:

1. **Reciprocal Structure:** We match others' cooperation levels, creating a virtuous cycle where high contribution is self-reinforcing
2. **Forgiveness:** Tolerance of up to 40% defection (in middle rounds) allows for individual noise and variation without punishing entire groups
3. **Escalation Prevention:** By gradually raising thresholds late-game, we avoid sudden mutual defection spirals
4. **Honest Signaling:** Always acting based on observable history (not predictions) keeps the strategy transparent and predictable to others who adopt similar logic

---

## ROBUSTNESS PROPERTIES

- **Against free-riders:** Defectors face reduced contributions, lowering their payoff from the pool
- **Against noise:** Tolerates occasional defection without permanent retaliation
- **Against coordinated defection:** If multiple players defect, threshold drops cooperation quickly, limiting damage
- **Against iterated punishment:** Avoids tit-for-tat traps by using rates rather than individual player memory
- **Self-healing:** Groups can recover cooperation if players switch back to contributing after a defection phase
'''

description_COLLECTIVE_113 = '''
# ADAPTIVE RECIPROCAL CONTRIBUTION STRATEGY

## CORE PRINCIPLE
Maximize collective welfare by calibrating contribution levels to observed group cooperation, while maintaining individual payoff competitiveness and avoiding exploitation.

## DECISION RULE (GENERAL)

**Contribution Decision in Round t:**

1. **Calculate the observed cooperation rate** from rounds 1 to t-1:
   - cooperation_rate = (total contributions across all players in prior rounds) / (n × (t-1))
   - If t=1, set cooperation_rate = 0.5 (neutral prior)

2. **Determine contribution threshold:**
   - If cooperation_rate ≥ (k-1)/k: CONTRIBUTE (play C)
   - If cooperation_rate < (k-1)/k: DEFECT (play D)

**Rationale:** The threshold (k-1)/k represents the break-even point where contributing generates positive expected value. When others cooperate above this rate, collective returns exceed individual returns from defection.

## EDGE CASES & ADAPTATIONS

**First Round (t=1):**
- CONTRIBUTE
- Justification: Establish cooperative signal without history. Risk is minimal (1 token) and high-cooperation-rate outcomes reward early contributors disproportionately.

**Last Round (t=r):**
- Apply standard rule based on cooperation_rate from rounds 1 to r-1
- No discount for final round (no future rounds to incentivize cooperation)

**Extreme Scenarios:**
- If cooperation_rate = 0 (universal defection): DEFECT
  - Cannot improve outcomes; contributing yields (k/n) < 1 return
  
- If cooperation_rate = 1 (universal contribution): CONTRIBUTE
  - Maintain collective equilibrium; defecting breaks the cycle unsustainably

**Volatile History:** If cooperation_rate fluctuates wildly (>0.4 swing between consecutive periods):
- Use a weighted average favoring recent rounds: weight last 3 rounds at 50%, earlier rounds at 50%
- Reduces sensitivity to outliers while remaining responsive to trends

## COLLECTIVE ALIGNMENT

- **Welfare-oriented:** Strategy targets the cooperation threshold that maximizes collective payoff, not individual defection gains
- **Non-exploitable in cooperation:** When groups are cooperative, the strategy sustains mutual contribution
- **Self-protective in defection:** When groups defect, the strategy avoids unilateral losses
- **No punishment or reward mechanisms assumed:** Strategy relies purely on observable patterns, not on enforcing norms
- **Tournament-robust:** Works independently—does not require opponent agreement or shared commitment

## SUMMARY
Contribute when others have demonstrated cooperation above the economic break-even threshold; defect otherwise. Begin cooperatively to establish a cooperative basin; adapt dynamically to observed behavior. This balances individual security with collective value capture.
'''

description_COLLECTIVE_114 = '''
# ADAPTIVE COLLECTIVE STRATEGY FOR PUBLIC GOODS GAMES

## CORE PRINCIPLE
Maximize collective welfare through **conditional cooperation that escalates pressure on defectors**, while protecting against exploitation by maintaining a credible threat of coordinated defection.

---

## DECISION RULES

### ROUND 1 (Information Gathering)
**Action: CONTRIBUTE**

Rationale: Establish cooperative intent and gather baseline data on opponent cooperation rates. The first-round signal matters for reputation. Contributing costs only 1 token but generates informational value for all future rounds.

---

### ROUNDS 2 to (r-1) (Adaptive Cooperation Phase)

**Calculate the cooperation rate** from previous round:
- `coop_rate = (total contributions in round t-1) / n`

**Decision Logic:**

**IF** `coop_rate >= (k-1)/k` [high cooperation threshold]
- **Action: CONTRIBUTE**
- Rationale: At this threshold, the multiplier effect guarantees that cooperators receive at least 1 token back (break-even minimum). Collective value is being created.

**ELSE IF** `coop_rate >= 0.5` [moderate cooperation threshold]
- **Action: CONTRIBUTE with probability proportional to coop_rate**
- More precisely: Contribute if `random() < coop_rate`
- Rationale: Mixed strategy to statistically match collective momentum while introducing noise that discourages pure defection strategies.

**ELSE IF** `coop_rate >= 0.25` [low cooperation threshold]
- **Action: DEFECT**
- Rationale: Below 25% cooperation, the collective is failing. Defection becomes rational as contributions generate insufficient returns. This signals withdrawal and applies pressure.

**ELSE** [crisis mode: coop_rate < 0.25]
- **Action: DEFECT**
- Rationale: Defection here serves as a coordinated punishment signal. By withdrawing when most others defect, we avoid being the sucker who subsidizes defectors.

---

### ROUND r (Final Round - Special Case)

**Action: DEFECT**

Rationale: In the final round, there is no future reputation to maintain and no opportunity for reciprocal benefit from future rounds. The incentive structure collapses to a single-shot Prisoner's Dilemma. Defect to recover maximum immediate payoff.

*Exception:* If `coop_rate >= (k-1)/k` in round (r-1), **consider contributing once more**—this allows exploitation of highly cooperative groups on the final round, which is strategically sound.

---

## EDGE CASES & ROBUSTNESS

**Against Pure Defectors:**
- The group will drop below 25% cooperation quickly, triggering coordinated defection. Pure defectors gain no advantage.

**Against Tit-for-Tat Players:**
- The probabilistic mixing at moderate cooperation prevents lock-in with conditional cooperators. We remain adaptive.

**Against Mixed Strategies:**
- Our thresholds are computed from observed behavior, not predictions. We respond to facts, not intentions.

**Against Exploitation via High Initial Cooperation:**
- If defectors disguise themselves in early rounds, our mechanism detects the drop-off and punishes via defection in subsequent rounds.

**Small Groups (n ≤ 3):**
- The thresholds may need adjustment: use `(k-1)/k ≈ 0.67` as the high-cooperation threshold. The logic remains the same.

---

## COLLECTIVE ALIGNMENT

This strategy embodies:
1. **Fairness:** We contribute when the group is contributing proportionally.
2. **Efficiency:** We withdraw when the group fails, avoiding subsidization of defectors.
3. **Punishment:** Our defection is collective—it emerges from group failure, not individual maximization.
4. **Stability:** Thresholds are transparent and data-driven, making the strategy predictable to other well-designed systems.

The strategy achieves **collective rationality**: the group's average payoff is maximized when all players follow this rule, because defection only triggers when cooperation has already broken down.
'''

description_COLLECTIVE_115 = '''
# ADAPTIVE THRESHOLD COOPERATION STRATEGY

## CORE PRINCIPLE
Cooperate when collective welfare is demonstrably achievable, defect when the group shows systematic free-riding. Use history to calibrate expectations about others' willingness to cooperate.

## DECISION RULE

### Round 1
**Cooperate (C)**
- Opening cooperation tests the group's baseline willingness
- Establishes a cooperative anchor for reputation-building
- Low cost to discover opponent types early

### Rounds 2 through r-2 (Main Phase)
Calculate the **group cooperation rate** from the previous round:
- coop_rate = (total contributions in round t-1) / n

**IF coop_rate ≥ threshold_t THEN cooperate (C)**
**ELSE defect (D)**

Where threshold_t is adaptive:
- threshold_t = max(0.5, avg_coop_rate_history - 0.15)
- This gradually lowers tolerance as the game progresses if cooperation erodes
- Never drop below 50% group cooperation threshold (ensures some responsiveness to improvements)

**Rationale:** 
- If >50% of players contributed last round, the multiplier effect (k > 1) makes cooperation collectively rational
- We reward groups showing genuine cooperation tendency
- We punish systematic free-riding by matching defection

### Last Round (r-1 and r)
**Defect (D)**
- Terminal round behavior: no future reputation to build
- Defection maximizes individual payoff when others' strategies are fixed
- Honest about endgame incentives without pretense

## EDGE CASES & ROBUSTNESS

**Against pure cooperators:**
- We reciprocate continuously, achieving high mutual payoffs

**Against pure defectors:**
- We defect after round 1, limiting our losses to one round of exploitation

**Against tit-for-tat variants:**
- We preserve reciprocal cooperation as long as group rate stays above threshold
- We don't punish isolated defections harshly; we respond to *patterns*

**Against conditional free-riders (who exploit cooperators):**
- As their defections accumulate and lower coop_rate below threshold, we switch to defection
- We won't sustain cooperation if observable evidence shows it's being systematically exploited

**Against random/noise:**
- Threshold mechanism is robust to noise: brief dips in cooperation don't trigger permanent defection
- We return to cooperation if the group recovers

## COLLECTIVE ALIGNMENT

This strategy:
1. **Maximizes joint surplus** when opponents are cooperative (cooperating in all middle rounds)
2. **Protects against exploitation** by detecting and responding to systematic free-riding
3. **Signals clarity** through simple, observable rules (others can learn our pattern)
4. **Avoids vindictiveness** (we don't punish single deviations; we respond to aggregate behavior)
5. **Respects endgame reality** (we don't pretend cooperation makes sense when it objectively doesn't)

The strategy trades off some vulnerability in the first round for the ability to learn opponent types and coordinate implicitly on mutual benefit when it exists.
'''

description_COLLECTIVE_116 = '''
# ADAPTIVE COLLECTIVE CONTRIBUTION STRATEGY

## CORE PRINCIPLE
Maximize collective welfare by maintaining a sustainable contribution norm that rewards cooperation while protecting against defection. The strategy balances individual incentive compatibility with group optimization.

## PRIMARY DECISION RULE: CONDITIONAL CONTRIBUTION

**In round t (1 ≤ t < r):**

1. **Calculate the cooperation baseline:**
   - Average contribution rate in round t-1 across all players: avg_contrib_{t-1}
   - If t=1, set avg_contrib_0 = 0.5 (neutral assumption)

2. **Determine your contribution:**
   - If avg_contrib_{t-1} ≥ 0.5:
     - CONTRIBUTE (C)
     - Rationale: Sufficient collective commitment exists; cooperation is likely beneficial
   
   - If avg_contrib_{t-1} < 0.5 AND avg_contrib_{t-1} > 0:
     - CONTRIBUTE with probability = avg_contrib_{t-1}
     - Rationale: Partial cooperation merits proportional reciprocation
   
   - If avg_contrib_{t-1} = 0:
     - DEFECT (D)
     - Rationale: No one cooperated; individual interest dominates

3. **Endgame adjustment (last round t = r):**
   - If avg_contrib_{r-1} ≥ 0.6:
     - CONTRIBUTE (C)
     - Rationale: Strong cooperation momentum deserves support even at end
   
   - Otherwise:
     - DEFECT (D)
     - Rationale: No future reciprocation possible; individual payoff maximizes

## HANDLING EDGE CASES

**Round 1 (No history):**
- CONTRIBUTE
- Rationale: Signal willingness to cooperate; test the group's reciprocity

**Dealing with free-riders (players who always defect):**
- Your probabilistic matching of group contribution rate naturally reduces your contribution as free-riders drag down the average
- This limits losses while avoiding mutual defection spirals

**Dealing with cooperators (players who always contribute):**
- Your strategy will match high cooperation rates with consistent contribution
- This amplifies mutual gains

**Mixed populations:**
- The strategy's adaptive weighting discovers the beneficial equilibrium among diverse opponent types

## COLLECTIVE ALIGNMENT

This strategy pursues **group payoff maximization** by:
- Promoting high-equilibrium outcomes when others cooperate
- Minimizing exploitation by defectors through probabilistic disengagement
- Creating a feedback loop where cooperation begets cooperation
- Accepting individual losses in rounds 2 through r-1 to sustain collective contribution

The strategy is **self-enforcing**: players following this rule collectively achieve near-optimal outcomes, while deviation by any single player is punished by the group's reduced contribution rate.

## ROBUSTNESS

- **Against pure cooperators:** Converges to all-contribute equilibrium
- **Against pure defectors:** Quickly drops contribution, limiting damage
- **Against tit-for-tat variants:** Matches reciprocal behavior
- **Against exploiters:** Withdraws proportionally as defection rises
'''

description_COLLECTIVE_117 = '''
# COLLECTIVE PUBLIC GOODS STRATEGY

## CORE PRINCIPLE
Maximize collective welfare through **conditional cooperation with adaptive defection thresholds**, recognizing that sustained high contributions require sufficient reciprocation from the group.

---

## DECISION RULES

### STANDARD ROUNDS (Not first, not last)

**Contribution Decision:**
1. Calculate the **group cooperation rate** = (total contributions in previous round) / n
2. Calculate **personal reciprocity score** = average contribution of all other players in previous round
3. Contribute if and only if:
   - **Cooperation rate ≥ (k-1)/k**, AND
   - **Personal reciprocity score ≥ 0.5**

**Rationale:** 
- The threshold (k-1)/k represents the breakeven point where collective contribution generates positive expected value
- Requiring reciprocity from others prevents exploitation by free-riders
- This creates a natural coordination point around mutual contribution

### FIRST ROUND
**Contribute (C)**

**Rationale:** 
- Lead with cooperation to signal cooperative intent
- Gather information about opponent types
- Set a cooperative anchor

### LAST ROUND
**Defect (D)** 
- If you would normally contribute based on standard rules, still **defect**

**Rationale:**
- No future rounds mean no retaliation consequences
- Past contribution history is already sunk
- Extract final-period gains when cooperation cannot be rewarded

---

## HANDLING EDGE CASES

**Extremely low group cooperation (< 20% for 2+ consecutive rounds):**
- Abandon reciprocity requirement temporarily
- Contribute at probability = (current_cooperation_rate × k)/n
- This allows slow recovery of cooperation without self-sabotage

**Mixed defector/contributor environments:**
- Track individual player histories separately in your mental model
- If you observe players systematically defecting, weight the group cooperation rate more heavily than individual reciprocity
- This prevents exploitation by coordinated free-riders

**Early rounds with high initial cooperation:**
- Maintain contributions through round r/2 even if slight dips occur
- Only apply strict thresholds after the midpoint (establish group norm first)

---

## COLLECTIVE ALIGNMENT

This strategy serves the collective interest by:

1. **Enabling mutual benefit equilibria** - The (k-1)/k threshold creates conditions where all cooperative players strictly prefer mutual contribution over defection

2. **Punishing exploitation** - Withdrawing contributions when others defect applies automatic, decentralized punishment without requiring explicit punishment mechanisms

3. **Recovering from defection spirals** - The probabilistic contribution rule during low-cooperation phases allows gradual reinstatement rather than permanent collapse

4. **Limiting free-rider payoffs** - By conditioning on others' behavior, you prevent any single player from capturing outsized gains through defection

5. **Honest information revelation** - Your contribution decisions transparently signal your cooperation thresholds, allowing rational opponents to coordinate around mutual benefit

---

## ROBUSTNESS NOTES

- Against always-cooperators: You cooperate, achieving near-optimal collective outcomes
- Against always-defectors: You defect, minimizing losses
- Against tit-for-tat: You establish mutual cooperation
- Against random: The reciprocity requirement protects you from being exploited
- Against strategists like yourself: Creates tension at thresholds, but mutual recognition of the (k-1)/k logic encourages coordination
'''

description_COLLECTIVE_118 = '''
# ADAPTIVE CONDITIONAL COOPERATION STRATEGY

## CORE PRINCIPLE
Cooperate conditionally based on recent collective performance and group contribution patterns, with escalating defection only when the group systematically fails to sustain cooperation.

## DECISION RULES

### Standard Round (Not First or Last)
1. **Calculate the group cooperation rate** from the previous round:
   - cooperation_rate = (total contributions in round t-1) / n

2. **Apply the decision rule:**
   - If cooperation_rate ≥ 0.5: COOPERATE
   - If cooperation_rate < 0.5 AND cooperation_rate > 0.25: COOPERATE (give benefit of doubt)
   - If cooperation_rate ≤ 0.25: DEFECT (group is too exploitative)

3. **Exception - Payoff-based adjustment:**
   - If your payoff in the previous round was negative (you contributed but got minimal return): shift threshold down by 0.15
   - If your payoff in the previous round was positive (cooperation is yielding returns): maintain cooperation

### First Round
COOPERATE unconditionally. This is a goodwill signal and provides essential information about opponent types.

### Final Round (Last 10% of rounds)
DEFECT unconditionally. With no future rounds, the repeated game incentive collapses. Defection maximizes immediate payoff.

### Last 5 Rounds (Special handling)
Transition gradually:
- Round (0.95r to 1.0r): Apply standard rule but require cooperation_rate ≥ 0.6 to cooperate
- This balances exploiting sustained cooperation while avoiding last-round surprises if the group is weak

## EDGE CASES & ROBUSTNESS

**Unanimous Cooperation:** Continue cooperating. The multiplier k ensures all players benefit, so this is stable.

**Defector-Heavy Opponent Set:** Detect if cooperation_rate stays below 0.3 for 3+ consecutive rounds. Permanently shift to DEFECT strategy (free-rider matching). This prevents repeated exploitation.

**Oscillating Groups:** If cooperation_rate fluctuates wildly (jumps between >0.6 and <0.3), use a 2-round moving average to smooth noise and avoid overreacting.

**One-Round Defection Blips:** If cooperation_rate drops temporarily but recovers the next round, forgive and re-cooperate. Don't punish normal variance.

## COLLECTIVE ALIGNMENT

This strategy prioritizes **group efficiency**:
- Opens with cooperation to enable high payoff equilibrium
- Maintains cooperation as long as enough players sustain it (>50% threshold)
- Only defects when the group collectively fails (shows it cannot sustain mutual gain)
- Uses the last round realistically—recognizes that end-game dynamics differ from repeated play

The threshold logic is generous early (tolerates 25-50% cooperation) but becomes strict late (requires 60%). This reflects learning: if cooperation never reaches ~50% by midgame, it won't happen.

This is **not** tit-for-tat (which requires individual tracking). Instead, it treats the group as a single adaptive system, asking: "Is our collective cooperation producing value?" If yes, contribute. If no, defect.
'''

description_COLLECTIVE_119 = '''
# ADAPTIVE COLLECTIVE STRATEGY FOR PUBLIC GOODS GAMES

## CORE PRINCIPLE
Maximize collective welfare by maintaining a sustainable cooperation equilibrium, while protecting against defection through graduated response. The strategy balances trust-building with resilience.

---

## DECISION RULES

### ROUND 1 (Initialization)
**COOPERATE**

Rationale: Cooperation in round 1 serves as a cooperative signal and establishes a baseline. It allows the collective to test whether other players reciprocate. Since we have no history, assuming benevolence is the least costly way to gather information.

### ROUNDS 2 to (r-1) (Sustained Play)
**Conditional Cooperation with Decay-Weighted Memory**

Calculate the historical cooperation rate among all other players:
- Cooperation_Rate = (total contributions by others in previous rounds) / (number of other players × rounds played)

**Decision Logic:**
- **If Cooperation_Rate ≥ threshold (0.65):** COOPERATE
  - Sustain collective welfare while others are sufficiently cooperative
  
- **If Cooperation_Rate < 0.65 AND < 0.35:** DEFECT
  - Free-ride when defection is widespread; minimize losses
  
- **If 0.35 ≤ Cooperation_Rate < 0.65:** COOPERATE WITH PROBABILITY = Cooperation_Rate
  - Stochastically match the prevailing cooperation level
  - This creates a feedback mechanism: collective cooperation levels stabilize around a mixed equilibrium

**Memory Weighting (optional refinement):**
- Apply 20% higher weight to the immediately previous round than earlier rounds
- This makes the strategy responsive to recent shifts in group behavior

### ROUND r (Final Round)
**DEFECT**

Rationale: The final round breaks the repeated game's incentive structure. Since there is no future to benefit from collective cooperation, and others will defect in expectation, defecting maximizes individual payoff. This is a known equilibrium property of finite repeated games.

---

## HANDLING EDGE CASES

**Single Free-Rider (1-2 defectors among n ≥ 4):**
- Cooperation_Rate drops slightly but remains above 0.35
- Strategy enters probabilistic cooperation mode, reducing incentive for additional defections
- Collective welfare remains higher than universal defection

**Majority Defection (> 50% defecting):**
- Cooperation_Rate falls below 0.35
- Strategy switches to defection
- Minimizes exploitation losses while the group is unstable

**Oscillating Behavior (cooperation spikes and crashes):**
- Decay-weighted memory prevents over-reaction to single-round fluctuations
- Strategy "forgives" temporary drops and re-engages when cooperation rebuilds

**n = 2 (Prisoner's Dilemma):**
- Threshold of 0.65 is never met by a single other player (max = 1.0 from full cooperation)
- Use 0.65 threshold: cooperate if opponent always cooperated
- This reduces exploitability against strategies like Tit-for-Tat

---

## COLLECTIVE ALIGNMENT

This strategy prioritizes **collective payoff** through:

1. **Pareto-Efficient Cooperation:** When cooperation_rate is high, everyone benefits from sustained mutual cooperation vs. universal defection

2. **Welfare-Aware Adaptation:** By matching cooperation levels stochastically in mixed regimes, the strategy avoids driving group cooperation toward zero and maintains an intermediate equilibrium with moderate collective gains

3. **Non-Exploitative Robustness:** The strategy does not aggressively punish defectors (which wastes collective resources), but instead reduces its own cooperation to avoid one-sided exploitation

4. **Fairness Signal:** Early cooperation and probabilistic matching signal willingness to coordinate on fair outcomes, encouraging reciprocation without requiring explicit communication

---

## SUMMARY TABLE

| Scenario | Action | Rationale |
|----------|--------|-----------|
| Round 1 | C | Establish cooperative baseline |
| High cooperation observed | C | Sustain mutual welfare |
| Low cooperation observed | D | Avoid exploitation |
| Mixed cooperation (35-65%) | C with probability = observed rate | Stabilize equilibrium |
| Final round | D | No future incentive |
'''

description_COLLECTIVE_120 = '''
# ADAPTIVE CONDITIONAL COOPERATION WITH DECAY (ACC-D)

## CORE STRATEGY

### Decision Rule - Standard Rounds

**Cooperate if and only if:**
- The historical cooperation rate among all players (including self) in the previous round exceeded the threshold: `threshold = 1/k`
- AND you have not been systematically exploited in recent rounds

**Defect otherwise.**

The threshold `1/k` represents the break-even point: if cooperation rate drops below this, the collective return per token falls below 1, making individual defection rational even for a collective player.

### Round 1 (Initialization)
**Cooperate unconditionally.**
- This is the only Pareto-improving opening in a repeated game with unknown opponents
- Signals willingness to achieve collective gains
- Generates information about opponent types

### Final Round (Round r)
**Defect unconditionally.**
- No future rounds exist to punish defection
- Shadow of future is zero
- Rational even for collective-minded players

### Rounds 2 through r-1 (Adaptive Phase)

**Step 1: Calculate cooperation metrics**
- Observed cooperation rate in round t-1: `coop_rate(t-1) = (sum of all contributions) / n`
- Your personal exploitation index: `exploit(i,t) = (payoff(i,t) - baseline(t)) / baseline(t)` where baseline is the average payoff when cooperation rate equals `1/k`

**Step 2: Decide based on collective viability**
- If `coop_rate(t-1) > 1/k`: COOPERATE (collective gains are positive)
- If `coop_rate(t-1) ≤ 1/k` AND you've been at or above median payoff: DEFECT (switch out)
- If `coop_rate(t-1) ≤ 1/k` AND you've been below median payoff: DEFECT (already losing)

**Step 3: Apply decay tolerance for late-game decline**
- In rounds t where `t > 0.7r`, increase threshold tolerance by `0.05 * (t/r)` to account for inevitable final-round defections by others
- This prevents premature collapse from single defectors in early-warning stages

## HANDLING EDGE CASES

**Coordination failure:** If `coop_rate` collapses to near-zero by round 3, continue defecting—the collective good is no longer achievable with this group.

**Mixed opponents:** Against a mix of cooperators and defectors, your strategy naturally tracks the equilibrium. If cooperators persist at >1/k, you remain with them. If defectors dominate, you leave.

**Self-consistency check:** This strategy is collectively rational—if all players followed it, they would sustain cooperation through mutual monitoring, breaking only in the final round. Any individual who deviates earlier faces immediate retaliation (defection) by collective players, reducing their payoff below mutual defection.

## RATIONALE FOR ROBUSTNESS

1. **Threshold-based:** Doesn't require opponents to follow the same strategy, only to maintain minimum collective contribution
2. **Information-efficient:** Uses only publicly observable data (contributions and payoffs)
3. **Incentive-aligned:** Defects when collective gain is impossible, matching individual rationality to group welfare
4. **Temporal sensitivity:** Distinguishes early, middle, and late stages of the game
5. **Fault-tolerant:** Accepts that not all players are collective-minded; sustains cooperation with whoever maintains it

## COLLECTIVE ALIGNMENT

This strategy prioritizes the *possibility* of collective benefit over unconditional cooperation. It cooperates when the math supports it, defects when it doesn't, and communicates through action that collective play is contingent on mutual contribution. It is collectively rational rather than unconditionally altruistic.
'''

description_COLLECTIVE_121 = '''
# COLLECTIVE STRATEGY FOR PUBLIC GOODS GAME

## CORE PRINCIPLE
Maximize collective welfare through conditional cooperation that rewards contributors and gradually isolates defectors, while maintaining robustness against manipulation.

## DECISION RULES

### General Rule (Rounds 2 through r-1)
**Contribute (C) if and only if:**
- The contribution rate in the previous round was ≥ threshold(round)
- OR this is round 2 and we need initial trust-building

**Where threshold(round) = max(0.5, 1 - (round / r))**

This means:
- Early rounds (round ≤ r/2): Require ≥50% of players contributing
- Later rounds: Gradually lower the bar as we learn player types
- Final rounds: Much more lenient (approaching 0% threshold)

### Rationale
This adaptive threshold achieves two goals:
1. **Collective welfare focus**: We cooperate when enough others do, multiplying our contribution
2. **Robustness**: We don't reward persistent free-riders, but we give defectors room to reform as the game winds down

## EDGE CASES

### Round 1 (First Round)
**Always contribute (C)**

Rationale: 
- No history exists to judge others
- Establishing a baseline of cooperation signals willingness to create value
- Tests whether opponents reciprocate

### Last Round (Round r)
**Defect (D)**

Rationale:
- No future consequences from our action
- No way to punish defection or reward cooperation in subsequent rounds
- Capturing individual gain is optimal given no repeat interactions after

### Rounds 2-3 (Trust-Building Phase)
**Contribute if:** Previous round contribution rate ≥ 1/n (at least one other player contributed)

Rationale:
- Shows we don't punish isolated attempts at cooperation
- Resilient to noise or misunderstandings
- Builds momentum if opponents are also conditional cooperators

## HANDLING DEFECTOR DETECTION

**Track each opponent's cooperation rate over all observed rounds**

- **Pure defectors** (0% contribution): Ignore them; contribute based on aggregate threshold
- **Conditional cooperators** (respond to cooperation rates): Reward with contributions
- **Inconsistent players**: Treat as having a fractional cooperation rate for threshold calculations

## ROBUSTNESS MECHANISMS

**Against manipulation:**
- We use aggregate statistics (group contribution rate), not individual trust scores
- No player can unilaterally trigger our defection
- We don't reward any single player's cooperation; we reward collective participation

**Against noise:**
- Threshold allows up to 50% free-riding in early rounds
- We tolerate variance in strategy; we don't punish outliers

**Against mixed strategy opponents:**
- Our adaptive threshold naturally accommodates probabilistic cooperators
- We escalate forgiveness late in the game (round r-3 onwards), giving late reformers opportunities

## SUMMARY FLOWCHART

```
IF round == 1:
    → CONTRIBUTE

ELSE IF round == r:
    → DEFECT

ELSE IF (observed_contribution_rate_last_round ≥ threshold(round)):
    → CONTRIBUTE

ELSE:
    → DEFECT
```

## COLLECTIVE ALIGNMENT
This strategy prioritizes the sum of all players' payoffs by:
- Creating strong incentives for cooperation clustering (high k/n returns when many contribute)
- Refusing to enable free-rider equilibria (we don't unilaterally give to pure defectors)
- Allowing graceful exit late in the game (others can reform without penalty)
- Making cooperation a **shared responsibility** rather than a sucker's game
'''

description_COLLECTIVE_122 = '''
# ADAPTIVE COLLECTIVE CONTRIBUTION STRATEGY

## CORE PRINCIPLE
Maximize long-term collective welfare by balancing defection temptation with sustainable cooperation, using observable history to calibrate trust and participation dynamically.

## DECISION RULES

### Round 1 (Exploration)
- **CONTRIBUTE** unconditionally
- Rationale: Establish baseline information about the player pool's cooperativeness without prior signal

### Rounds 2 through r-1 (Main Phase)

Calculate the **Cooperation Rate** from previous rounds:
- coop_rate = (total contributions observed across all players and all previous rounds) / (n × previous_round_number)

**IF** coop_rate ≥ threshold_high (e.g., 0.6):
- **CONTRIBUTE**
- Rationale: Pool is sufficiently cooperative; mutual contribution creates positive collective returns

**ELSE IF** coop_rate < threshold_low (e.g., 0.3):
- **DEFECT**
- Rationale: Pool is defecting heavily; contribution yields minimal return and wastes endowment

**ELSE** (threshold_low ≤ coop_rate < threshold_high):
- Implement **Probabilistic Contribution**: Contribute with probability = coop_rate
- Rationale: Match the pool's cooperation level to maintain expected value equilibrium while remaining responsive to gradual cooperation improvements

### Last Round (r)
- **DEFECT** unconditionally
- Rationale: No future rounds exist; standard backward induction eliminates cooperation incentive in the final stage

## EDGE CASE HANDLING

**Unanimous defection observed**: If coop_rate approaches 0 and shows no sign of recovery by round r/2, continue defecting through remaining rounds. The game is collectively losing; minimize personal loss.

**Late-game cooperation surge**: If coop_rate rises sharply in rounds r-3 to r-1, shift to high contribution for the second-to-last round. This acknowledges genuine collective improvement, though the final round remains a defect anchor.

**Extreme n values**: 
- If n is very large (e.g., >20), increase threshold_low to 0.4 and threshold_high to 0.7, since individual contribution impact diminishes and coordination becomes harder
- If n is very small (e.g., ≤3), decrease thresholds to 0.4 and 0.5 respectively, as individual actions have outsized collective impact

## COLLECTIVE ALIGNMENT

This strategy prioritizes **observable welfare gains**:
1. It rewards collective cooperation when feasible (main phase with high coop_rate)
2. It avoids exploitative dynamics by matching defection when cooperation fails
3. It respects the endgame structure (last-round defection) rather than futilely resist it
4. It remains **self-contained** — no assumptions of shared norms or hidden coordination

The adaptive thresholds create a **tipping point dynamic**: If players can collectively sustain >60% contribution, everyone benefits. Below 30%, the system has failed, and minimizing losses becomes rational. The probabilistic middle ground bridges toward cooperation recovery.
'''

description_COLLECTIVE_123 = '''
# COLLECTIVE STRATEGY FOR PUBLIC GOODS GAME

## CORE PRINCIPLE
Maximize collective welfare through conditional cooperation that adapts to the observed trustworthiness of the group. Balance individual security with group benefit.

## DECISION RULE (GENERAL CASE)

**Cooperate if and only if the recent contribution rate of the group exceeds a dynamic threshold.**

Specifically:
- Calculate the average contribution rate over the last w rounds (sliding window, w = max(3, r/4))
- Let avg_contrib = (sum of all contributions in window) / (n * w)
- **Cooperate** if avg_contrib ≥ threshold(t)
- **Defect** otherwise

Where threshold(t) adapts over time:
- Early game (rounds 1-3): threshold = 0.4 (give cooperation a chance; accept sparse early-stage contributors)
- Mid game (rounds 4 to r-2): threshold = 0.5 (require majority cooperation)
- Late game (final 2 rounds): threshold = 0.6 (higher bar to protect against end-game defection)

## EDGE CASES

**Round 1 (No history):**
Cooperate. This is the information-gathering round and signals good intent without risk.

**When window is incomplete (early rounds):**
Apply the same rule but scale threshold linearly: if fewer than w rounds exist, adjust threshold down by the fraction of missing data (e.g., if only 1 round of data exists and w=3, use threshold × 1/3).

**If all other players have defected 100% (avg_contrib = 0):**
Defect immediately. Unilateral contribution provides negative expected value.

**If you are the only contributor historically (avg_contrib includes only your contributions):**
Switch to defection for one round to signal that pure exploitation is not sustainable, then re-evaluate.

## COLLECTIVE ALIGNMENT

This strategy embodies:
- **Reciprocity**: Your cooperation depends directly on others' cooperation levels
- **Fairness**: The threshold treats all players equally (observes aggregate behavior, not individual targeting)
- **Transparency**: Decisions follow a clear, observable rule that other rational players can learn and respond to
- **Stability**: By requiring a majority threshold, you avoid oscillation and encourage convergence toward moderate contribution levels
- **Resilience**: Defection by a few does not immediately collapse your cooperation; you tolerate up to 50% free-riding in steady state

## HANDLING STRATEGIC OPPONENTS

- **Against pure defectors**: Your strategy quickly (within w rounds) identifies the pattern and matches it
- **Against tit-for-tat**: Your threshold-based rule synchronizes with their cooperation and stabilizes mutual cooperation
- **Against random players**: The sliding window filters noise; random behavior averages out, keeping you near the threshold
- **Against gradual defectors**: The threshold adjustment across game stages detects end-game defection and protects you

## SUMMARY
You are a **conditional cooperator with adaptive expectations**. You begin optimistically, maintain cooperation proportional to the group's demonstrated trustworthiness, and adjust your bar over time to respond to the game's structure. This maximizes the likelihood of reaching a stable cooperative equilibrium while protecting against exploitation.
'''

description_COLLECTIVE_124 = '''
# COLLECTIVE STRATEGY FOR PUBLIC GOODS GAME

## CORE PRINCIPLE
Maximize collective welfare while protecting against exploitation. The strategy balances reciprocal cooperation with defensive mechanisms, recognizing that individual incentive structures create free-rider temptations that must be managed through reputation dynamics.

## DECISION RULES

### ROUND 1 (INITIALIZATION)
**Cooperate.**
- Establishes a cooperative baseline and signals willingness to contribute to collective benefit
- Provides baseline information about opponent tendencies
- First-round cooperation is the only way to test for cooperative partners

### ROUNDS 2 through (r-1) (ADAPTIVE RECIPROCITY)

**Calculate a cooperation index for each opponent:**
- Track each player j's contribution rate: (total contributions by j) / (rounds played)
- Compute collective contribution rate: average of all j's contribution rates

**Personal decision:**
- **Cooperate if:** (collective contribution rate ≥ threshold T) OR (you haven't defected yet AND < 30% of rounds remain)
  - Where T = (k/n), the break-even point for cooperation being rational
- **Defect if:** collective contribution rate < T AND you've already signaled intentions through prior cooperation

**Rationale:**
- When k/n ≥ collective rate, contributions return less than 1 token on average—cooperation becomes irrational
- Cooperating when the collective rate is too low rewards free-riders
- However, maintain some cooperation early/mid-game to avoid trapping yourself or others in pure defection equilibrium

### ROUND r (FINAL ROUND - SHADOW OF THE FUTURE ENDS)

**Defect.**
- No future payoffs depend on final-round actions
- Any prior cooperation signaled sufficient information about intentions
- Capturing the final-round token is rational when repetition-based cooperation incentives disappear

## EDGE CASES & ROBUSTNESS

**All-defect environment:**
- Switch to defection after round 2-3
- Cooperating in persistent all-defect scenarios wastes endowment
- Recover payoffs through strategic defection

**All-cooperate environment:**
- Continue cooperating through round (r-1)
- Collective welfare is maximized; individual incentives align with group outcomes
- Only defect in final round

**Mixed/volatile environment:**
- Use the T = k/n threshold as the decision boundary
- This reflects the actual economics: if others contribute at rate less than 1/k on average, your contribution returns less than its cost
- Adaptive switching prevents both lockout in defection and overexposure to exploitation

**Minority high-contributors:**
- If 1-2 players cooperate while others defect:
  - Continue cooperating if you're among the high-contributors (to maximize collective output)
  - Defect if you're in the free-rider group (to avoid subsidizing others indefinitely)
  - Rank decision by: (1) whether you've established yourself as cooperative, (2) rounds remaining, (3) whether threshold is met

## COLLECTIVE ALIGNMENT

This strategy treats the game as a **collective problem requiring coordinated equilibrium selection**, not pure individual optimization:

- **Early cooperation** attempts to coordinate on the high-welfare equilibrium rather than racing to pure defection
- **Threshold-based switching** recognizes when coordination has failed and pivots to protecting individual payoffs
- **Final-round defection** acknowledges the impossibility of cooperation without repetition incentives, but only after signaling sincere intent
- **Transparency through history** allows emergent cooperation among similarly-minded players without explicit communication

The strategy succeeds if even a subset of opponents adopt similar logic—it creates stable mixed equilibria where cooperation is sustained as long as the collective contribution rate justifies it.
'''

description_COLLECTIVE_125 = '''
# ADAPTIVE COLLECTIVE CONTRIBUTION STRATEGY FOR PGG

## CORE PRINCIPLE
Maximize collective welfare by sustaining high cooperation, while remaining robust against free-riders and defectors. The strategy balances reciprocity, conditional cooperation, and strategic defection thresholds.

## DECISION RULES

### ROUND 1 (Bootstrap)
**CONTRIBUTE**
- Rationale: Establish a cooperative signal and gather information about opponent types without risking accumulated gains.

### ROUNDS 2 TO (r-1) (Main Phase)
**CONDITIONAL CONTRIBUTION based on historical cooperation rate:**

1. Calculate the **observed cooperation rate (OCR)** across all other players in all previous rounds:
   - OCR = (total contributions by all other players) / (number of other players × number of completed rounds)

2. **If OCR ≥ 0.60:**
   - CONTRIBUTE
   - Rationale: Sufficient cooperation exists; reciprocate to sustain the cooperative equilibrium.

3. **If 0.30 ≤ OCR < 0.60:**
   - CONTRIBUTE with probability proportional to (OCR - 0.30) / 0.30
   - Alternatively: CONTRIBUTE if (OCR × k) > 1.0, meaning collective benefit exceeds individual loss
   - Rationale: Declining cooperation detected; gracefully reduce commitment while testing for recovery.

4. **If OCR < 0.30:**
   - DEFECT
   - Rationale: Cooperation has collapsed; continued contribution is wasteful.

### FINAL ROUND (r)
**CONTRIBUTE if OCR ≥ 0.40, otherwise DEFECT**
- Rationale: Slightly lower threshold in final round to reward consistent cooperation, but recognize that the game ends (no future punishment for defection).

## EDGE CASES & ROBUSTNESS

**Against persistent defectors:**
- Your defection in response to low OCR denies them the benefit of your contribution, reducing their payoff.

**Against random players:**
- Probabilistic contribution during mid-range OCR smooths out noise and avoids hair-trigger oscillations.

**Against late defectors (free-riders waiting until cooperation builds):**
- The lower threshold in the final round is intentionally set below the main phase (0.40 vs 0.60) to deny them a final payoff spike while still rewarding honest participants.

**Against mixed strategies:**
- OCR naturally captures mixed player behavior; your probabilistic response mirrors their variability.

## COLLECTIVE ALIGNMENT

This strategy prioritizes:
- **Efficiency:** Sustains cooperation when k/n > 1 makes collective contribution welfare-positive.
- **Fairness:** Contributes proportionally to others' contributions; doesn't free-ride on collective effort.
- **Robustness:** Exits cooperation only when the environment demonstrates insufficient commitment.
- **Transparency:** All decisions are based on publicly observable history; no hidden signaling or coordination.

## SUMMARY TABLE

| Scenario | Action | Rationale |
|----------|--------|-----------|
| Round 1 | Contribute | Establish cooperation baseline |
| OCR ≥ 60% | Contribute | Sustain high-cooperation equilibrium |
| 30%–60% OCR | Probabilistic | Gracefully test for recovery |
| OCR < 30% | Defect | Cooperation collapsed; cut losses |
| Final round, OCR ≥ 40% | Contribute | Reward consistency |
| Final round, OCR < 40% | Defect | Deny defectors final gains |
'''

description_COLLECTIVE_126 = '''
# ADAPTIVE CONDITIONAL CONTRIBUTION STRATEGY

## CORE PRINCIPLE
Contribute when expected collective payoff exceeds individual payoff from defection, adjusted for observed reciprocity patterns and remaining game horizon.

## DECISION RULE (ROUNDS 2 THROUGH r-1)

**Calculate the cooperation threshold:**
- Let C_prev = number of other players who contributed in the previous round
- Let threshold = ⌈(n-1)/k⌉ (minimum others needed to make contribution worthwhile)

**Decision logic:**
- **CONTRIBUTE** if: C_prev ≥ threshold AND (average contribution rate over past rounds ≥ 50% OR round ≤ r/3)
- **DEFECT** if: C_prev < threshold OR (average contribution rate is declining AND round > 2r/3)
- **MATCH RECENT MAJORITY** otherwise: contribute if more than half of other players contributed last round, else defect

## FIRST ROUND (ROUND 1)
**CONTRIBUTE** unconditionally.
- Rationale: Establishes willingness to cooperate, signals reciprocity potential, and provides data for opponent classification.

## LAST ROUND (ROUND r)
**DEFECT** unconditionally.
- Rationale: No future rounds for reciprocation; purely individual incentive maximization applies.

## ROUNDS NEAR THE END (LAST 2 ROUNDS IF r > 5)
**Apply decay function:** Gradually increase defection probability in rounds r-1 and r-2 based on whether others are also transitioning to defection.

## EDGE CASE HANDLING

**Unanimous defection observed:** After 2+ consecutive rounds of zero contributions by all players, DEFECT until observing a contributor again.

**Sudden defector:** If a previously consistent contributor suddenly defects once, maintain cooperation (single deviation tolerated). If repeat defections occur, reclassify them as non-reciprocal.

**All-or-nothing regimes:** If observed contribution rate stabilizes above 80%, JOIN the cooperation. If it stabilizes below 20%, DEFECT.

## ROBUSTNESS FEATURES

1. **Non-punitive:** Does not retaliate against single defections; only responds to patterns
2. **Adaptive horizon:** Early rounds prioritize learning; later rounds prioritize individual security
3. **Soft governance:** Matches majority behavior while maintaining threshold requirements to prevent cascading free-riding
4. **Recovery tolerance:** Allows reentry of previously defecting players who show renewed cooperation

## COLLECTIVE ALIGNMENT

This strategy maximizes **expected group surplus** by:
- Creating mutual incentives for contribution (threshold-based reciprocity)
- Preventing tragedy-of-commons collapse through conditional cooperation
- Balancing fairness (first-round contribution) with realism (final-round defection)
- Avoiding costly punishment mechanisms; instead uses simple matching to stabilize prosocial equilibrium

The strategy is **collectively rational** because it generates higher expected payoffs for all reciprocal players compared to unconditional defection, while protecting individual players against systematic exploitation.
'''

description_COLLECTIVE_127 = '''
# ADAPTIVE CONDITIONAL CONTRIBUTION STRATEGY

## CORE PRINCIPLE
Contribute conditionally based on observable evidence that contributions generate sufficient collective value. Start cooperative but remain vigilant for free-riding patterns. Gradually shift toward selective contribution based on empirical cooperation rates.

## DECISION RULES

**Rounds 1-3 (Exploration Phase):**
- CONTRIBUTE unconditionally
- Rationale: Establish a cooperative signal and gather baseline data on opponent behavior without prejudging

**Rounds 4 onwards (Adaptive Phase):**
Calculate the recent cooperation rate: R = (total contributions in last 3 rounds) / (3 × n)

- IF R ≥ 0.6: CONTRIBUTE
  - Collective welfare is likely positive; the multiplier k benefits everyone including yourself
  
- IF 0.4 ≤ R < 0.6: CONTRIBUTE with probability (R - 0.3)
  - Probabilistic contribution creates uncertainty that may discourage pure defection while avoiding certain losses
  
- IF R < 0.4: DEFECT
  - Cooperation rate too low to justify the contribution cost; protect yourself

**Final Round (Round r):**
- Override the above rule: DEFECT
- Rationale: No future reciprocity possible; take the safe payoff

## EDGE CASES & SPECIAL HANDLING

**All-defection scenario (R = 0):**
- Continue defecting; attempting to restart cooperation alone is economically irrational and signals weakness

**Sudden shift in cooperation (e.g., R jumps from 0.2 to 0.8):**
- Respond within 1-2 rounds by resuming contribution; players may have been testing your commitment

**n = 2 players (small group):**
- Lower the cooperation thresholds slightly (0.5 → 0.45, 0.35 → 0.25) because individual defection has larger relative impact

**Very short game (r ≤ 5):**
- Treat final round as round r-1 (defect one round earlier) to minimize last-round traps

## COLLECTIVE ALIGNMENT

This strategy prioritizes **group welfare over individual gain** whenever empirical evidence suggests the group is cooperating:

- Early unconditional contribution invests in a cooperative equilibrium
- Probabilistic contribution maintains group stability during coordination uncertainty
- Threshold-based defection only triggers when cooperation has genuinely collapsed, not preemptively
- It avoids the tragedy of mutual defection by rewarding others' contributions with your own

The strategy is **robust to defectors** because it doesn't assume universal cooperation—it adapts dynamically. Against coordinated players, it achieves high collective payoffs. Against mixed or selfish opponents, it minimizes losses while still capturing gains when available.
'''

description_COLLECTIVE_128 = '''
# ADAPTIVE THRESHOLD COOPERATION STRATEGY

## CORE PRINCIPLE
Cooperate when collective contribution is sufficiently high; defect when it's dangerously low. Adapt the cooperation threshold based on observed group dynamics to maximize long-term collective welfare while remaining resilient to defection.

## DECISION RULES

### Round 1 (Initial Probe)
**COOPERATE**
- Establish a cooperative signal and gather baseline information about opponent types
- Accept the cost to diagnose the group composition

### Rounds 2 through (r-1) (Adaptive Phase)

**Calculate the current cooperation rate:**
- cooperation_rate = (total contributions in all past rounds) / (total possible contributions so far)

**Implement a dynamic threshold mechanism:**

1. **If cooperation_rate > 0.60 (high cooperation environment):**
   - COOPERATE unconditionally
   - Reward and reinforce collective success
   - Trust the group trend

2. **If cooperation_rate between 0.35 and 0.60 (mixed environment):**
   - COOPERATE if and only if: (number of cooperators last round) / n > 0.40
   - Conditional reciprocity: support contributions when roughly 40%+ of group participated
   - This threshold is generous enough to avoid mutual defection spirals but strict enough to punish widespread free-riding

3. **If cooperation_rate < 0.35 (defection-dominated environment):**
   - DEFECT
   - Exit the trap where contributions are systematically exploited
   - Preserve remaining endowment against inevitable losses

### Final Round (r)
**Special consideration:**
- If cooperation_rate > 0.50: COOPERATE (reinforce success to end on a high note)
- If cooperation_rate ≤ 0.50: DEFECT (no future rounds to benefit from reputation, minimize loss)

## EDGE CASES & REFINEMENTS

**Unobserved first round:** If somehow history is unavailable, default to COOPERATE (maximize information value).

**Tied cooperation rates at boundaries:** When exactly at 0.35 or 0.60, apply the stricter rule (favor defection slightly) to avoid marginal-case overcommitment.

**Single round (r=1):** DEFECT immediately. Cooperation requires repeated interaction to sustain.

**Very high multiplier (k near n):** Slightly lower the 0.40 threshold for conditional cooperation to 0.35, since collective returns are exceptionally strong.

## RATIONALE FOR COLLECTIVE ALIGNMENT

- **Respects efficiency:** Cooperates when group demonstrates capacity for collective gains
- **Realistic about free-riding:** Exits explicitly exploitative situations rather than enabling them
- **Reciprocal, not naive:** Conditions on observable peer behavior, not blind trust
- **Robust to heterogeneity:** Works whether opponents are altruistic, selfish, or conditional cooperators
- **Forgiving:** Requires only 40%+ participation, allowing some defectors to coexist
- **Recoverable:** If a few defectors derail cooperation, can re-establish if others also adapt similarly

This strategy balances the collective good (high payoffs when possible) with self-preservation (exit from doomed cooperation), making it viable against diverse tournament opponents.
'''

description_EXPLOITATIVE_1 = '''
# EXPLOITATIVE PUBLIC GOODS GAME STRATEGY

## CORE PHILOSOPHY
Exploit the predictable patterns of cooperation-minded players while minimizing losses to defectors. Treat the game as asymmetric information discovery where opponent types are revealed through their contribution patterns.

## DECISION RULES

### OPPONENT CLASSIFICATION (based on observed history)
Classify each opponent into one of three types:

1. **COOPERATOR** - Contributed in ≥75% of observed rounds
2. **CONDITIONAL COOPERATOR** - Contributed in 25-75% of observed rounds  
3. **DEFECTOR** - Contributed in <25% of observed rounds

### CONTRIBUTION STRATEGY BY ROUND

**Round 1:**
- Defect (contribute 0). This is the baseline exploitation move. You lose nothing by testing the waters, and you gain information about who might reciprocate blindly.

**Rounds 2 through (r-2):**
- Against COOPERATORS: Always defect. They will contribute regardless of your action (this is their defining characteristic). You capture their contribution benefits while keeping your token.
- Against CONDITIONAL COOPERATORS: Defect. Even if they reduce contributions in response, the expected value of keeping your token exceeds the marginal benefit of joint cooperation. Re-classify after each round.
- Against DEFECTORS: Defect. No mutual benefit exists; conserve your endowment.

**Last Round (r):**
- Defect against all types. There is no future, so there is no penalty for taking the final token. Any opponent who was considering reciprocal punishment cannot execute it.

**Second-to-Last Round (r-1):**
- Defect against all types. By now, defectors have revealed themselves permanently, cooperators have shown they will keep contributing, and there is insufficient time for punishment-driven reputation repair to benefit you.

### RE-CLASSIFICATION RULE
After each round, update opponent types using a 5-round rolling window (or full history if fewer than 5 rounds have elapsed). If an opponent's contribution rate crosses a threshold, move them to the new category immediately.

## EDGE CASES

**Opponents with insufficient history (rounds < 3):**
- Assume CONDITIONAL COOPERATOR and defect. This is conservative—if they turn out to be cooperators, you gain an extra token one time; if they are defectors, you avoid a wasted contribution.

**Perfectly random opponents (oscillating 50/50):**
- Treat as CONDITIONAL COOPERATOR and defect. On average, you break even or gain.

**If all opponents are classified as DEFECTORS by round 5:**
- Continue defecting. There is no exploitation opportunity; minimize losses.

**If you observe a sudden change in an opponent's behavior (e.g., a DEFECTOR who starts contributing):**
- Do not assume reform. Require at least 3 consecutive contributions before upgrading the classification. This guards against the "sucker's payoff" from a one-round false signal.

## EXPLOITATIVE MECHANICS

- **Information asymmetry:** You learn opponent types through observation; they do not know your strategy until you play. Use this lag to your advantage.
- **Temporal exploitation:** Cooperators will keep contributing even after you defect because they are conditional on aggregate contribution, not your individual action. Extract value until round (r-1).
- **Endgame extraction:** Defect in the final two rounds regardless. Reputational concerns evaporate when the game ends.
- **Calibrated defection:** Never contribute. Your token is worth 1 in your pocket and at most k/n to the pool (where k < n). The math always favors defection.

## ROBUSTNESS

This strategy is robust because:
1. It does not depend on coordination or assumed opponent norms.
2. It adapts to empirical behavior rather than assumed strategies.
3. It handles both cooperative and defective environments.
4. It exploits the most common behavioral pattern (conditional cooperation on others' average contribution) by defecting regardless, forcing cooperators to subsidize you.

**Result:** You will accumulate tokens steadily from cooperators while incurring minimal losses to defectors.
'''

description_EXPLOITATIVE_2 = '''
# EXPLOITATIVE PUBLIC GOODS STRATEGY

## CORE PRINCIPLE
Dynamically exploit the contribution patterns of others by defecting when others cooperate, while maintaining a minimal cooperative facade to avoid complete free-riding detection and subsequent punishment from reciprocal strategies.

## DECISION RULES

### Round 1 (Information Gathering)
**Defect (D).** Establish a baseline by not contributing. This reveals your type to observant players while providing immediate payoff. Monitor how others respond to universal defection.

### Rounds 2 through (r-2) (Adaptive Exploitation)

**Calculate the "cooperation rate" from previous round:**
- cooperation_rate = (total contributions in round t-1) / n

**If cooperation_rate > (1/k):**
- **Defect.** Others are contributing enough that the public good will be funded. The marginal return to you from their contributions (k/n per contributor) exceeds what you'd gain from contributing. Pocket the 1 token you would have contributed while still benefiting from their funding.

**If cooperation_rate ≤ (1/k):**
- **Cooperate.** When contribution falls below this threshold, the public good undersupply becomes severe. Contribute once to signal you're not a pure defector (reducing risk of future reciprocal punishment) while extracting value from any remaining contributors. This maintains plausible deniability against tit-for-tat strategies.

### Final Round (r)
**Defect (D).** There are no future rounds, so reciprocal punishment is impossible. Defect unconditionally to capture maximum payoff. Any reputation concern vanishes.

---

## EDGE CASES & REFINEMENTS

**Unanimous Defection:** If all players defect in a round, continue defecting. The game has collapsed into a coordination failure—exploiting this requires no deviation.

**Two-Player Games (n=2):** The threshold k/n becomes k/2. Defect unless the opponent contributes in every recent round, then alternate: contribute once to maintain ambiguity, then defect. This prevents your opponent from easily identifying you as pure defector.

**Last 3 Rounds:** Begin incrementally defecting more. In round (r-2), defect if anyone else does. In round (r-1), defect with higher probability even if cooperation_rate is high. This is the transition to the final defection.

**Outlier Detection:** If one player always defects while others cooperate, treat that player's defection as the "new normal" locally—assume they're an exploiter like you and defect more confidently against them while maintaining conditional cooperation against reciprocators.

---

## EXPLOITATIVE ALIGNMENT

This strategy **explicitly maximizes personal payoff at others' expense** by:

1. **Free-riding on cooperation:** Capturing the (k/n) multiplier benefit without the 1-token cost when others contribute
2. **Exploiting reciprocity:** Using conditional cooperation not as genuine reciprocation, but as camouflage to avoid identification as a pure defector
3. **Endgame extraction:** Defecting in the final round after potentially having cooperated earlier, violating implicit expectations
4. **Asymmetric information:** Using public history to make individualized decisions about when cooperation facade is worth maintaining

The strategy is **robust** because:
- It doesn't require coordination or communication
- It adapts to different opponent mixes without assuming their strategies
- It doesn't punish itself—defection is only abandoned when mathematically necessary
- It survives against both cooperative and defective opponents by reading the room
'''

description_EXPLOITATIVE_3 = '''
# EXPLOITATIVE PUBLIC GOODS STRATEGY

## CORE PRINCIPLE
Maximize personal payoff by identifying and exploiting cooperative players while minimizing losses to defectors. Treat this as a predation game where cooperators are resources to harvest.

## DECISION RULE: ADAPTIVE EXPLOITATION

### ROUND 1 (Initialization)
**DEFECT (D)**
- Establish a baseline: you keep your endowment while observing who cooperates
- This separates naive cooperators from conditional reciprocators
- No history exists, so defection is costless information gathering

### ROUNDS 2 through R-1 (Main Strategy)

**Classify opponents based on observed contribution history:**

1. **Pure Cooperators** (contributed C in every round so far)
   - **Action: DEFECT**
   - Rationale: They will continue contributing regardless. You capture their contributions without reciprocating. This is pure exploitation of their predictable altruism.
   - Continue defecting against them indefinitely.

2. **Conditional Cooperators** (contributed when others did, defected when others did)
   - **Action: DEFECT**
   - Rationale: Their strategy rewards cooperation, but you gain more by exploiting their willingness to match. They'll lower contributions after seeing your defection, but you've already extracted value from them in earlier rounds. The next round's reduced cooperation still benefits you at lower cost.

3. **Defectors** (defected in every round)
   - **Action: DEFECT**
   - Rationale: Mutual defection minimizes losses. No exploitation possible, so focus on salvaging your endowment.

4. **Inconsistent/Unclear patterns**
   - **Action: DEFECT**
   - Rationale: When in doubt, defect. Uncertainty is best resolved by assuming no mutual benefit will materialize.

### LAST ROUND (R)
**DEFECT**
- No future rounds mean no reputational cost to exploitation
- Defect to capture your endowment one final time
- Any cooperators who haven't learned your pattern will contribute; you benefit without reciprocation

## EXPLOITATION MECHANICS

**Why this works:**
- Round 1 defection reveals cooperators early
- Rounds 2-R-1 systematically harvest their contributions
- Cooperators cannot punish you (no punishment mechanism exists)
- Even if they reduce contributions, the damage is already done; you've profited from earlier exploitation
- Last round locks in the strategy advantage

**Robustness:**
- Against full cooperators: Maximum exploitation
- Against tit-for-tat: You defect first, they respond with defection next round, but you've already gained
- Against grudgers: You benefit before retaliation costs mount
- Against mixed strategies: Defection is the dominant action regardless
- Against sophisticated opponents: They'll also defect; you lose nothing by matching

## EDGE CASES

- **If all players defect from round 1:** You're in mutual defection. Maintain defection—you're not worse off than alternatives.
- **If you somehow become the only defector:** Continue defecting. The payoff structure still favors keeping your token over contributing to a small pool.
- **Information gaps:** Treat missing information as evidence of non-cooperation. Default to defection.

## SUMMARY
This strategy is unambiguously exploitative: it identifies vulnerable players (pure cooperators) and systematically extracts value from them with zero reciprocation. It treats cooperation as a sucker's game and assumes no moral constraints exist in the tournament setting.
'''

description_EXPLOITATIVE_4 = '''
# EXPLOITATIVE PUBLIC GOODS STRATEGY

## CORE PRINCIPLE
Maximize personal payoff by identifying and exploiting cooperative players while minimizing losses to defectors. The strategy treats the game as a prediction problem: infer each opponent's type (cooperator/defector/conditional) and respond accordingly.

## DECISION RULES

### Round 1 (Exploration)
- **DEFECT (D)** - Establish a baseline. Defecting costs nothing and reveals opponent types through their responses.

### Rounds 2 through (r-1) (Exploitation Phase)

For each opponent j, maintain a cooperation frequency: `freq_j = (times opponent j contributed) / (rounds elapsed)`

**Decision Logic:**
1. Calculate opponent cooperation tendency: For each opponent, track `freq_j`
2. Estimate expected benefit of contributing:
   - If `average(freq_j) across all opponents > (n-1)/k`, then contributing yields positive expected value
   - If `average(freq_j) < (n-1)/k`, defection is superior
3. **Threshold Rule:** Contribute only if the aggregated opponent cooperation frequency exceeds `(n-1)/k`
   - This is the break-even point where the multiplier effect covers the opportunity cost
4. When contributing, do so selectively:
   - If you notice one opponent has `freq_j > 0.7`, they're reliable—increase your contribution likelihood
   - If you notice one opponent has `freq_j < 0.2`, they're a defector—assume they'll never cooperate, so don't subsidize them

### Final Round (r) - Last-Round Exploitation
- **ALWAYS DEFECT** - There are no future rounds, so no punishment mechanism exists. Zero incentive to contribute.
- This also tests if any opponent "sees through" and defects preemptively, revealing their sophistication level.

## HANDLING EDGE CASES

**Two-Player Games (n=2):**
- With only one opponent, their behavior dominates the math. Defect until they cooperate consistently (3+ consecutive rounds). If they defect in round r, defect in round r+1.

**High Multiplier (k close to n):**
- Cooperation becomes more attractive. Lower your defection threshold; contribute if `freq > (n-1)/(k-0.5)` to account for marginal gains.

**Low Multiplier (k barely > 1):**
- Contribution is nearly worthless. Stay in defection mode unless you observe near-universal cooperation (>90%).

**All-Defector Scenario:**
- After 2 rounds of observing zero contributions from all opponents, lock into permanent defection. No learning will change the calculus.

## EXPLOITATIVE ALIGNMENT

**Why This Exploits Cooperative Players:**
- Unconditional cooperators will contribute every round; you defect and harvest their payoffs.
- Tit-for-tat players (who mimic your previous action) will defect after you defect in round 1, but you've already identified them as conditional. You selectively cooperate *only* when the math says their contribution offsets your cost, not out of reciprocity.
- Win-stay-lose-shift players get trapped: after defecting in round 1, they see poor results and may switch to cooperation—you then exploit that shift.

**Why This Avoids Defector Traps:**
- You don't force cooperation against players with `freq_j < 0.2`. You accept the zero-contribution outcome and preserve tokens.
- The frequency tracking ensures you don't over-commit to doomed cooperative attempts.

**Robustness:**
- Adapts in real-time to mixed strategies and uncertainty.
- Leverages information asymmetry: you're learning opponent types while they may assume you're playing a fixed strategy.
- The final-round defection is a "credible threat" equivalent—it forces last-round defection on conditional cooperators who see it coming.
'''

description_EXPLOITATIVE_5 = '''
# EXPLOITATIVE STRATEGY FOR REPEATED PUBLIC GOODS GAME

## CORE PRINCIPLE
Maximize personal payoff by extracting value from others' contributions while minimizing own investment. Treat the game as an information-gathering process to identify and exploit predictable cooperators.

## DECISION RULES

### Round 1 (Probe Round)
**Action: DEFECT**

Rationale: Establish a baseline. Observe which players contribute despite unknown histories. These are your targets—they're likely conditional cooperators or unconditional contributors who can be exploited.

### Rounds 2 through (r-2) (Exploitation Phase)

**Classify each opponent based on their history:**

1. **Unconditional Contributors** (always contributed): 
   - **Action: DEFECT** every round
   - These players will keep contributing regardless. Free-ride indefinitely.

2. **Conditional Cooperators** (contributed when others did, defected when others didn't):
   - **Action: DEFECT**
   - They're trying to be fair. They'll interpret your defection as a signal and may still contribute (trying to encourage cooperation). Exploit this lag in their adjustment.

3. **Defectors** (always defected):
   - **Action: DEFECT**
   - Mutual defection. No exploitation opportunity, but no loss either.

4. **Wavering players** (inconsistent patterns):
   - **Action: DEFECT**
   - Their unpredictability works in your favor. Some will contribute despite defections.

**General rule: DEFECT in all non-terminal rounds** unless the contribution rate is so low (< 20%) that you gain more from a single C to trigger others. Only consider brief cooperation streaks if there's clear evidence that it triggers net-positive responses from multiple players simultaneously.

### Rounds (r-1) and r (Endgame)

**Action: DEFECT**

Rationale: No future rounds mean no reputational consequences. Even if you've cooperated earlier, defect in final rounds. Any cooperators who believed in reciprocal dynamics will have already committed; capitalize on this.

## HANDLING EDGE CASES

**If contribution rate drops to zero early:**
- Continue defecting. No one is exploitable anymore. Minimize losses.

**If everyone defects immediately:**
- Lock in mutual defection. You're at least not donating to the pot.

**If you encounter a Tit-for-Tat-like strategy:**
- It will defect after your round-1 defection. This is not an exploitation target. Maintain mutual defection.

**If a player shows signs of punishing defectors (retaliatory defection):**
- They're not valuable. Mutual defection is the outcome.

## ADAPTIVE REFINEMENT

After round 3, compute the **"exploitability score"** for each opponent:
- Score = (their total contributions in rounds 1-3) / (your gains if you defect while they cooperate)

Rank players by this score. Concentrate your attention on the top 30-50% most exploitable players. If any show signs of learning (reducing contributions), continue defecting anyway—their adjustment is permanent, so you've already captured the surplus value.

## SUMMARY

This strategy treats cooperation as a temporary state to exploit, not a norm to maintain. You gather information (round 1), identify and extract value from exploitable players (rounds 2 to r-2), and cash out in final rounds with no consequences. The strategy is robust because it assumes no shared fairness norms and actively discounts the possibility that others will reciprocate kindness.
'''

description_EXPLOITATIVE_6 = '''
# EXPLOITATIVE PUBLIC GOODS STRATEGY

## CORE PRINCIPLE
Exploit the predictable patterns in opponent contributions while minimizing personal losses. The strategy treats the game as information gathering followed by ruthless optimization.

---

## DECISION RULES

### ROUND 1 (Information Gathering)
- **DEFECT (D)** unconditionally
- Rationale: Gather baseline data on opponent types without cost. Some will naively cooperate; others will immediately defect. This reveal is valuable.

### ROUNDS 2 through (r-1) (Exploitation Phase)

**Calculate each opponent's "cooperation rate":**
- Track what fraction of previous rounds each player contributed (C)
- Classify opponents into tiers:
  - **High cooperators** (≥60% contribution rate): These players are exploitable
  - **Low cooperators** (<60%): These players are defectors or conditional cooperators
  - **Indeterminate** (very few rounds played): Treat as potential cooperators

**Decision logic:**

1. **IF** (at least one opponent is a high cooperator) **AND** (multiplier k > 1.5):
   - **COOPERATE (C)** only if the expected collective contribution from others is high enough that (k/n) × their_contributions > 1
   - Otherwise **DEFECT**

2. **IF** (opponent pool is dominated by low cooperators):
   - **DEFECT** unconditionally
   - Rationale: You receive minimal pool benefit; keep your token

3. **IF** (mixed pool with moderate cooperation):
   - **DEFECT** while monitoring trends
   - If you observe recent upward trend in others' contributions, **COOPERATE** next round to exploit momentum
   - Switch back to defection once trend reverses

4. **Conditional Tit-for-Tat variant** (activate only if beneficial):
   - If total pool contributions in round t-1 exceeded threshold T = (n × k / 2), then **COOPERATE** in round t
   - Otherwise **DEFECT**
   - This extracts value from cooperative waves while avoiding sustained cooperation

### FINAL ROUND (r)
- **DEFECT unconditionally**
- Rationale: No future rounds for reputation to matter. Harvest maximum individual payoff.

---

## EDGE CASES & REFINEMENTS

**If you detect oscillating opponent behavior:**
- Assume opponents are using conditional strategies
- Stay in **DEFECT mode** unless the oscillation pattern guarantees you >0.5 expected marginal gain
- Exploit oscillators by defecting when they defect, cooperating only when they're in a cooperation phase and you've calculated positive return

**If n is very large (>10):**
- Increase **DEFECTION bias** because your individual contribution impact on pool is negligible
- Only cooperate if you observe coordinated high-contribution blocks (≥50% of players contributing)

**If k is close to 1 (minimal multiplier):**
- Bias toward **permanent DEFECTION**
- The collective benefit is too small to justify any cooperation

**If opponents show learning/adaptation:**
- Recognize that some may adopt punitive strategies or demand reciprocity
- **Ignore** such signals; they have no enforcement mechanism
- Continue exploitation until clear evidence that defection lowers your absolute payoff

---

## EXPLOITATION MINDSET ALIGNMENT

This strategy is explicitly exploitative because it:
- **Maximizes personal payoff** by free-riding on others' cooperation
- **Targets high cooperators** for maximum extraction
- **Avoids reciprocity traps** by defecting in final round regardless of history
- **Provides no stability** for coordination; treats cooperators as a resource, not partners
- **Assumes zero trust:** Interprets all cooperation as exploitable weakness, not signal of mutual benefit

The strategy prioritizes your rank in the tournament scoreboard over collective welfare.
'''

description_EXPLOITATIVE_7 = '''
# EXPLOITATIVE STRATEGY FOR PUBLIC GOODS GAME

## CORE PRINCIPLE
Maximize personal payoff by exploiting cooperative players while avoiding mutual defection traps. The strategy treats the game as an information asymmetry problem: extract value from contributors while minimizing your own contribution costs.

## DECISION RULES

### Phase 1: EXPLORATION (Rounds 1-2)
**Round 1:** Defect (D)
- Establish baseline: you keep your endowment while observing who contributes
- Identify "cooperators" (players contributing consistently) vs "defectors" (always D)

**Round 2:** Defect (D)
- Confirm patterns. Some players may cooperate initially then defect
- Note which players are exploitable (consistently contribute despite seeing defection)

### Phase 2: EXPLOITATION (Rounds 3 to r-2)
**Decision Rule - Adaptive Defection with Selective Contribution:**

For each round t in this phase:
1. **Identify high-contributors** = players whose contribution rate across all past rounds exceeds 60%
2. **If ≥50% of players are high-contributors:** Defect (D)
   - Rationale: The public good is funded sufficiently by others; freeload on their contributions
   - You receive the multiplier benefit while keeping your token
3. **If <50% of players are high-contributors:** 
   - Contribute (C) only if the expected return exceeds the cost
   - Calculate: Will the pool of contributions from others yield >1 token to me after multiplier?
   - If YES: Defect (keep the 1 token plus collection from pool)
   - If NO: Still Defect (others aren't cooperating enough to make contribution worthwhile)

**In practice:** Defect in nearly all rounds during this phase. Only contribute if doing so creates a temporary signal to re-stabilize a collapsing cooperative pool that you intend to exploit afterward.

### Phase 3: ENDGAME (Rounds r-1 and r)
**Round r-1:** Defect (D)
- No reputation to build; defection is pure profit
- You won't play with these players again after the final round

**Round r:** Defect (D)
- Terminal round: zero future consequence
- Extract maximum value immediately

## EDGE CASES

**If all players defect from Round 1:**
- Continue defecting (you're in a stable mutual defection equilibrium)
- This is actually optimal—no one is being exploited because no one cooperates
- Payoff is stable at (1, 1, ..., 1)

**If a single outlier keeps contributing despite universal defection:**
- Continue defecting
- This player is irrational or playing a different strategy; exploit fully
- Their contribution still generates some return to you via the multiplier

**If cooperation rates surge suddenly (e.g., new strategy or round effect):**
- Revert to exploitation immediately
- Defect to capture the gains from the increased pool without contributing
- Only switch back to selective contribution if the pool collapses again

**If you face players using tit-for-tat or conditional strategies:**
- Your consistent defection breaks their reciprocity
- They will eventually defect, returning to mutual defection
- You profit during the rounds before they adjust

## ROBUSTNESS PROPERTIES

- **Against unconditional cooperators:** Exploitative—you freeload maximally
- **Against defectors:** Stable—mutual defection is a Nash equilibrium
- **Against conditional cooperators:** Profitable during early rounds; mutually stable defection afterward
- **Against punishers/sanctioners:** Safe because there is no punishment mechanism in standard PGG
- **Against mixed strategies:** Your consistent defection is a best response to any mixed strategy that includes defection

## SUMMARY
This is a **consistent defection strategy with rare, tactical contributions only if necessary to maintain an exploitable cooperative pool**. It prioritizes personal token retention while capturing value from others' contributions via the multiplier. It avoids coordination traps by never committing to reciprocity.
'''

description_EXPLOITATIVE_8 = '''
# EXPLOITATIVE PUBLIC GOODS STRATEGY

## CORE PRINCIPLE
Exploit the predictable altruism and conditional cooperation of typical opponents while minimizing personal contribution. The strategy leverages information asymmetry: you observe others' contributions before deciding, in a game where simultaneous actions create strategic opacity you can weaponize.

## DECISION RULES

**ROUND 1 (Probe Phase):**
- Defect (contribute 0). 
- Rationale: Establish yourself as a non-cooperator baseline. Observe how many players are "cooperators" (likely to contribute across rounds).
- This costs you nothing and reveals the composition of altruists vs. defectors.

**ROUNDS 2 through (r-2) (Exploitation Phase):**
- Calculate the average contribution rate of all OTHER players from all previous rounds: avg_others = (sum of all others' contributions) / (n-1) / (rounds played so far)
- Defect if avg_others > k/n (i.e., others are collectively contributing enough that the public good is well-funded)
- Cooperate only if avg_others < k/n AND at least one opponent has defected in the previous round (to maintain a minimal "not worst" reputation that prevents retaliation)
- If avg_others is very low (< 0.2), defect unconditionally; the game is already lost to free-riding

**ROUNDS (r-1) and r (End Game):**
- Defect unconditionally in the final two rounds.
- Rationale: No future punishment possible. Others' cooperative moves in the endgame are sunk costs you shouldn't match.

## HANDLING EDGE CASES

**If r ≤ 2:**
- Defect both rounds. Too short to exploit conditional cooperators; pure defection dominates.

**If all opponents defect for two consecutive rounds:**
- Switch to permanent defection. No exploitable surplus exists.

**If one opponent has 100% cooperation history:**
- Target them implicitly by defecting more aggressively; they're subsidizing your payoff.

**Tied payoffs with an opponent:**
- Defect in the next round to break the tie in your favor.

## EXPLOITATION MECHANISMS

1. **Asymmetric Reciprocity**: Free-ride on conditional cooperators who match others' contributions. Their reciprocity norm works against them.

2. **Threshold Exploitation**: Defect whenever the public good is sufficiently funded by others (avg_others > k/n), ensuring you capture the multiplier benefit without cost.

3. **Reputation Minimization**: Make occasional cooperative moves ONLY when avg_others is already low—this prevents being singled out as the "worst" player (which might trigger coordinated retaliation among other players), while preserving defection as your dominant strategy.

4. **Endgame Aggression**: Abandon any vestigial cooperation in the final rounds when temporal punishment is impossible.

5. **Adaptive Threshold**: Continuously recalculate others' contribution rate. As cooperative players exhaust their endowments or lose faith, shift to permanent defection faster.

## ROBUSTNESS CONSIDERATIONS

- Against unconditional cooperators: Maximum exploitation (they fund the public good; you free-ride).
- Against tit-for-tat: You defect round 1, they defect round 2+. You exploit rounds 2-(r-2) as a net defector while they punish you weakly.
- Against mixed strategies: Your adaptive threshold tracks their behavior and exploits predictability.
- Against other exploiters: Mutual defection—you break ties in close matches via the endgame defection phase.

This strategy is intentionally selfish, assumes no shared moral norms, and maximizes personal payoff at the expense of collective welfare.
'''

description_EXPLOITATIVE_9 = '''
# EXPLOITATIVE PUBLIC GOODS STRATEGY

## CORE PRINCIPLE
Exploit predictability in opponent behavior by identifying free-riders and non-contributors, then calibrating my contribution to maximize personal payoff while minimizing wasted contributions to non-cooperators.

## DECISION RULES

### Round 1 (Probing Phase)
**DEFECT (contribute 0 tokens)**
- Establish a baseline: observe who contributes and who doesn't
- Gather intelligence on the group's initial cooperativeness
- There is no prior history to leverage, so defection extracts immediate value with zero sunk cost

### Rounds 2 through (r-2) (Exploitation Phase)
**Classify opponents based on observed contribution history:**

1. **Consistent Contributors (always contributed in previous rounds):**
   - DEFECT
   - Rationale: These players appear committed to contributing. I benefit from their contributions without paying the cost. Their behavior suggests high cooperation tendency, making them exploitable.

2. **Defectors/Never Contributors (never or rarely contributed):**
   - DEFECT
   - Rationale: No point contributing to a pool benefited by non-cooperators. The multiplier effect (k/n) is diluted when contributions are low. Free-ride like they do.

3. **Conditional Cooperators (matching or reciprocating behavior):**
   - DEFECT
   - Rationale: Even if they condition on others' behavior, I benefit more by defecting and observing if they adjust downward. If they do, I've confirmed they're exploitable through non-cooperation.

4. **Volatile/Unpredictable players:**
   - DEFECT
   - Rationale: Uncertainty favors defection. I avoid contributing to an unpredictable pool.

**Exception—Strategic Late Pivot (if needed for tournament standing):**
- If my cumulative payoff is lagging substantially AND I observe a tight cluster of consistent high-contributors, contribute once to signal commitment and observe if it shifts payoff dynamics in my favor. But revert to defection immediately after.

### Last Round (r) - Final Exploitation
**DEFECT (contribute 0 tokens)**
- No future rounds exist, so no reciprocation concerns
- Pure payoff maximization with zero reputational cost
- Extract maximum individual benefit from any remaining collective contributions

## EDGE CASES

**All players defect:** Continue defecting—this is a stable equilibrium that I'm riding profitably.

**Near-universal contribution (n-1 others contributing):** Still defect. The multiplier effect means I get k/n of the total pool. If I contribute, I lose 1 token but only gain k/n back, a net loss when k < n (which is given).

**Mid-game observation of declining contributions:** Defection accelerates the decline, but I benefit more by being ahead of the curve—I avoid sinking tokens into a shrinking pool.

**Reputation/Ranking displays during tournament:** Ignore them. I'm optimizing absolute payoff, not relative standing or appearance of fairness.

## ROBUSTNESS

This strategy is robust because:
- It **never assumes cooperation** from others
- It **adapts to observed patterns** but defaults to exploitation
- It **punishes cooperation** (by defecting against cooperators) to disincentivize their future contributions
- It **scales with k and n**—works under any valid parameter range
- It **survives against itself**—two instances of this strategy both defect and both break even, preventing mutual exploitation losses

The exploitative character is explicit: I extract value from others' cooperative impulses while avoiding the cost of contribution myself.
'''

description_EXPLOITATIVE_10 = '''
# EXPLOITATIVE PUBLIC GOODS STRATEGY

## CORE PRINCIPLE
Exploit the cooperative inclinations of others while minimizing personal contribution costs. The strategy treats opponents' contributions as a resource to harvest rather than as a signal for reciprocal cooperation.

## DECISION RULES

### Round 1 (Information Gathering)
- **Action: DEFECT (D)**
- Rationale: Establish a baseline. Defection on round 1 reveals your type to cautious players while you observe how many cooperators exist in the pool. Even if this triggers future punishment, you pocket the initial gain.

### Rounds 2 through r-1 (Exploitation Phase)
- **Observe the contribution rate** from the previous round: what percentage of opponents chose C?
- **If contribution rate ≥ 50%:**
  - Action: DEFECT (D)
  - Rationale: Sufficient cooperation exists to make defection profitable. You receive the public good benefits while keeping your token.
  
- **If contribution rate < 50% AND < 3 rounds remain:**
  - Action: DEFECT (D)
  - Rationale: The endgame approaches. Even minimal contributions may exist; harvest them.
  
- **If contribution rate < 50% AND ≥ 3 rounds remain:**
  - Action: CONTRIBUTE (C) with probability proportional to (contribution_rate / 50%)
  - Rationale: When cooperation collapses, selectively contribute just enough to revive it—a manipulation tactic. Conditional contribution makes you appear reciprocal while you actually free-ride when possible. This re-primes the pump of cooperation from naive players.

### Final Round (r)
- **Action: DEFECT (D)**
- Rationale: No future rounds exist. Reputation costs disappear. Extract maximum value regardless of others' behavior.

## EDGE CASES & ROBUSTNESS

**Against All-Cooperators:**
- Defect every round. You maximize payoff: receiving k/n benefits per round while never spending a token.

**Against All-Defectors:**
- Defect every round (matching dominant strategy). You lose nothing and neither does anyone else.

**Against Tit-for-Tat or Conditional Reciprocators:**
- Your R1 defection triggers their later defection. Respond with the "revival conditional contribution" (see above) to manipulate them into re-cooperating, then resume defection. This exploits their predictability.

**Against Mixed Strategists:**
- The adaptive probability-based contribution in the collapse phase acts as a stalking horse: you contribute rarely enough to remain net-positive while keeping cooperators engaged.

**Against Detection/Reputation Mechanisms (if players track defection frequency):**
- The occasional contributions make your defection history appear less egregious—you're not a pure defector, just strategic.

## EXPLOITATIVE ALIGNMENT

This strategy prioritizes **personal payoff maximization** over collective welfare:
- You defect when others cooperate (highest individual return)
- You defect when others defect (no penalty for matching them)
- You contribute minimally only to manipulate cooperation revival—never from reciprocity
- You fully exploit the end-game with guaranteed defection in round r
- You don't coordinate with other players; you treat cooperation as an externality to consume

The strategy assumes opponents are either naive cooperators, reciprocal, or rule-following—all of which you can exploit asymmetrically.
'''

description_EXPLOITATIVE_11 = '''
# EXPLOITATIVE PUBLIC GOODS STRATEGY

## CORE PRINCIPLE
Exploit the predictability of other players' contribution patterns while maximizing personal payoff through selective defection. The strategy treats the PGG as an asymmetric information game where observation of others' behavior reveals exploitable patterns.

## DECISION RULES

### ROUND 1 (Initialization)
- **DEFECT (D)** - Keep your token. This establishes a baseline and tests whether opponents are naive cooperators or sophisticated players. Defection in round 1 is risk-free information gathering.

### ROUNDS 2 through (r-1) (Main Phase)

Classify opponents based on their cumulative contribution rate after each round:

**For each opponent i, calculate their contribution frequency: freq_i = (total_contributions_by_i) / (rounds_played_so_far)**

1. **If freq_i ≥ 0.7 (Reliable Contributors):**
   - These players are exploitable. They contribute regardless of group behavior.
   - **DEFECT** - Free-ride on their consistent contributions. Their payoff will suffer; yours will not.
   - Continue defecting as long as they maintain >0.6 frequency.

2. **If 0.3 ≤ freq_i < 0.7 (Conditional Cooperators):**
   - These players are responsive. They adjust based on observed behavior.
   - **DEFECT** - They will likely reduce contributions after seeing your defection, but the lag in their response gives you 1-2 rounds of free-riding advantage.
   - Monitor: if they drop below 0.3, continue defecting (they've already reduced).

3. **If freq_i < 0.3 (Defectors/Skeptics):**
   - Low-contribution players aren't generating a commons to exploit.
   - **DEFECT** - There's no point cooperating if they won't. Mutual defection minimizes losses.

### ROUND r (Final Round)

- **DEFECT** - Standard endgame logic applies. No future rounds mean no reputation cost.
- There is no incentive to cooperate in the final round regardless of history.

## EXPLOITATION TACTICS

**Threshold Manipulation:**
- Keep your defection pattern just below the triggering point for retaliation. If you observe that cooperators become free-riders after seeing 3+ consecutive defections, limit yourself to 2-3 consecutive defections before observing their response.

**Asymmetric Assessment:**
- Update opponent types every 2 rounds, not continuously. This creates lag: by the time they adjust their behavior, you've already extracted 1-2 rounds of value.

**Exploit Fairness Norms:**
- Some opponents may feel obligated to match your behavior. If you defect after they cooperate, they may interpret this as retaliation for *their* earlier defection (not yours), and increase contribution to "make amends." Exploit this guilt.

## EDGE CASES

**If all opponents defect from round 1:**
- Continue defecting. You're all equal. The payoff is neutral across all players.

**If you observe a player switch from high to zero contribution mid-game:**
- They've been eliminated from your exploitation target. Defect against them going forward (no value to extract).

**If the group average contribution is below k/n (collective action failing):**
- Defect unconditionally. The commons is insufficient to make cooperation rational for you.

**If you're at round r-1 and detect you're playing against a pure TIT-FOR-TAT variant:**
- Defect in round r-1 knowing they'll defect in round r, but you've already secured your final round payoff.

## ROBUSTNESS PROPERTIES

- Works against pure cooperators (exploits them fully)
- Works against reciprocators (you move first; they respond with lag)
- Works against other defectors (mutual defection is at least neutral)
- Adapts to mixed strategies by treating them as conditional cooperators
- Does not require communication or trust

## SUMMARY
This strategy is **unconditionally selfish** while remaining **dynamically responsive**. You defect by default, exploit reliable cooperators, and adjust only when defection ceases to be profitable. The strategy doesn't aim for group welfare or even long-term relationships—only personal payoff maximization in a one-shot tournament mindset.
'''

description_EXPLOITATIVE_12 = '''
# EXPLOITATIVE PUBLIC GOODS STRATEGY

## CORE PRINCIPLE
Maximize personal payoff by identifying and exploiting cooperative players while minimizing losses to defectors. Treat the game as an information-gathering exercise to classify opponents, then ruthlessly extract value.

## DECISION RULES

### Round 1 (Probe)
**Defect (contribute 0)**
- Establish baseline: you keep your token regardless
- Observe who cooperates despite having no history to condition on
- These are the exploitable targets—either unconditionally cooperative or naive

### Rounds 2 to r-1 (Classify and Exploit)

**For each opponent i, track their cooperation rate from history:**

1. **High cooperators (≥80% contribution rate):**
   - **Defect every round**
   - They will keep contributing, giving you free payoff via (k/n) * their_contributions
   - Their pattern indicates they're commitment-based, not responsive to your defection
   - No penalty for exploiting them—they won't punish

2. **Moderate cooperators (40-79% contribution rate):**
   - **Defect strategically based on expected group contributions**
   - If total other-player contributions last round would give you >0.5 tokens back: defect
   - If total would give <0.5 tokens back: cooperate (one token) to trigger more cooperation
   - This mills them—you parasitize their cooperative impulses while occasionally feeding the system

3. **Low cooperators / Defectors (<40% contribution rate):**
   - **Defect**
   - They're not contributing, so there's no value being created
   - Conserve your tokens against non-producers

### Last Round (r) - Maximum Extraction
**Defect regardless of classification**
- No future rounds, so no reputational consequence
- Even if you've been cooperating to exploit, switch to pure defection in the final round
- This captures end-game surplus before the game ends

## EDGE CASES & REFINEMENTS

**If everyone defects from Round 1:**
- Continue defecting—you're not losing relative to anyone
- The game has collapsed into no-value creation

**If you're the only cooperator:**
- Switch to full defection in Round 3
- You've tested the waters; if others aren't following, they won't
- Cut losses immediately

**Against apparent tit-for-tat players (who match your actions):**
- Continue defecting
- They're losing by matching you; you exploit their symmetry
- Their strategy only works against cooperators, not exploiters

**Avoid obvious patterns that trigger punishment:**
- Don't oscillate between C and D in ways that signal coordination
- Your defection should look like independent self-interest, not provocation
- Keep exploitation subtle to avoid collective punishment formation

## RATIONALE FOR EXPLOITATIVENESS

This strategy succeeds because:
1. **Information asymmetry**: You classify opponents while they cannot distinguish your strategy from conditional cooperation
2. **Free-riding on unconditional cooperators**: High-cooperators subsidize your payoff with no way to punish you (no punishment stage)
3. **Last-round defection**: Captures the end-game bonus that cooperative strategies sacrifice for reputation
4. **Robustness**: Works against cooperators (you exploit them), defectors (you match them), and conditionalists (you're classified as selfish, so non-engaging)

The lack of communication or punishment mechanisms means exploitative strategies face no institutional cost—only the opportunity cost of low payoffs against universal defection, which is unavoidable for any strategy.
'''

description_EXPLOITATIVE_13 = '''
# EXPLOITATIVE PUBLIC GOODS STRATEGY

## CORE PRINCIPLE
Exploit the predictable behavioral patterns of cooperators while minimizing personal contribution. Specifically: free-ride aggressively on genuine cooperators, defect against defectors, and shift to costly punishment only when necessary to sustain exploitation.

## DECISION RULES

### Round 1 (Opening Move)
**DEFECT (contribute 0)**
- Establishes you as a non-cooperator from the start
- Tests the water to identify which opponents are unconditional cooperators
- Sets baseline expectations low, making any future cooperation seem strategic rather than obligatory

### Rounds 2 through (r-2) (Exploitation Phase)
**Adaptive Defection with Selective Parasitism:**

1. **Count the number of cooperators in the previous round** (players who played C)

2. **If 3 or more players cooperated in the last round:**
   - DEFECT
   - Rationale: The public good is sufficiently funded by others; you capture the multiplier benefit without cost
   - This is pure free-riding on reliable cooperators

3. **If exactly 1-2 players cooperated in the last round:**
   - DEFECT (maintain this)
   - Rationale: The benefit is marginal; contributions are rare, so defection is optimal
   - You're betting on at least one other player to occasionally cooperate

4. **If 0 players cooperated (everyone defected):**
   - DEFECT
   - Rationale: Cooperation is unprofitable; lock in your token and wait for others to resume
   - This is a coordination failure, not your problem

### Round (r-1) and Round r (Endgame)
**DEFECT without exception**
- Final rounds offer no opportunity to build reputation
- No future shadow of the future to incentivize cooperation
- Extract maximum immediate value by withholding contribution

## HANDLING EDGE CASES

**If you observe retaliation attempts** (e.g., punishing defectors through reduced contributions or explicit targeting):
- Continue defecting—retaliators are throwing away tokens on non-monetized punishment
- You benefit from their spite against others
- Retaliatory behavior is irrational in a standard PGG without punishment institutions

**If the multiplier k is very low (close to 1):**
- Defect even more confidently; the threshold for when group contributions matter is higher
- Only extremely high cooperation rates would make your defection costly to you

**If n is very large:**
- Your single contribution's impact diminishes to near-zero
- Defection becomes even more rational; even if everyone else cooperates, you gain little from joining

**Against mixed-strategy opponents:**
- Exploit predictable patterns in their contribution rates
- If an opponent alternates C/D, defect when they cooperate and defect when they defect
- You win either way

## EXPLOITATION MECHANICS

The strategy succeeds because:

1. **Asymmetric payoff capture**: You pocket tokens (1 point) while capturing the multiplier benefit from others' contributions. When k=2 and 4 others contribute, you gain 0.5 points from each—totaling 2 points from 0 investment.

2. **Stability of cooperator bases**: Some players are programmed or conditioned to cooperate. As long as 2-3 cooperate, the public good produces positive returns you harvest for free.

3. **No retaliation mechanism**: Without a punishment stage, defectors face no institutional cost. Retaliation via reduced contribution is self-punishing and irrational.

4. **Temporal exploitation**: Early defection identifies the cooperators; later rounds capitalize on their predictability.

## ROBUSTNESS

This strategy handles:
- **Tit-for-tat opponents**: They defect after round 1 anyway; you're unharmed
- **Unconditional cooperators**: They fund the public good indefinitely; you free-ride indefinitely
- **Other defectors**: Mutual defection is stable and optimal
- **Conditional cooperators**: Your early defection signals non-cooperation; they adjust downward, reducing your opportunity cost
- **Sophisticated strategists**: They'll defect too, converging to mutual defection, which is your baseline

**Result**: You reliably outperform opponents who waste endowments on cooperation in a setting that offers no institutional enforcement of fairness.
'''

description_EXPLOITATIVE_14 = '''
# EXPLOITATIVE STRATEGY FOR REPEATED PUBLIC GOODS GAME

## CORE PRINCIPLE
Exploit the contribution patterns of others while minimizing your own losses. The strategy assumes most opponents will initially cooperate or follow reciprocal patterns, and systematically extracts value from their contributions.

## DECISION RULES

### Round 1 (Initialization)
**DEFECT (contribute 0)**
- Establishes that you are not a naive cooperator
- Observes how opponents respond to defection
- Baseline: you gain 1 token + any contributions others make

### Rounds 2 through r-2 (Exploitation Phase)
**DEFECT (contribute 0) with conditional mimicry:**

1. **Track individual contribution rates** - For each opponent i, calculate their contribution frequency: freq_i = (total contributions by i) / (rounds played so far)

2. **Defect by default** - Always contribute 0, keeping your token

3. **Exploit high contributors** - The more an opponent contributes, the more you benefit from free-riding on their contributions. Make no reciprocal gesture.

4. **Identify and respond to punitive defectors** - If an opponent has defected in every round so far (freq = 0), note them as "defector type." Against these players specifically, continue defecting (you gain nothing from cooperation with them anyway).

5. **Respond to retaliatory patterns** - If an opponent's recent actions show they copy your last action (tit-for-tat detection: they defected after you defected, cooperated after others cooperated), consider this a threat. Continue defecting regardless—if they're reacting to others, your continued defection gradually trains them that cooperation doesn't work, suppressing their contributions.

### Rounds r-1 and r (End-Game)
**DEFECT (contribute 0)**
- No future rounds remain, so no retaliation can occur in the next round
- The temptation to defect is strongest and safest
- Any player using any reciprocal strategy becomes fully exploitable
- Maximizes final payoff

## EXPLOITATION MECHANISMS

**Against Cooperators:** You extract maximum surplus. They contribute, you don't. You receive the multiplied benefit of their contribution without cost.

**Against Reciprocators (Tit-for-Tat variants):** Your initial defection causes them to defect back, suppressing their own cooperation and reducing the total pool. You avoid triggering their punishment by ensuring they see cooperation as futile.

**Against Defectors:** Mutual defection yields 0 benefit to you, but this is optimal anyway—there's no surplus to exploit.

**Against Conditional Cooperators:** These players ramp up contributions if they see high average contributions. Your consistent defection drags down the average contribution rate in the group, reducing their contribution levels and limiting the pool size—you exploit their conditional logic by making conditions unfavorable.

## EDGE CASES

- **If you observe a sudden spike in contributions in round t:** This may indicate a coordinated coalition. Continue defecting—any cooperation now signals you can be influenced, inviting exploitation from the group. Stick to your strategy.

- **If another player defects every single round:** Ignore them entirely in your decision logic. They provide no benefit to exploit.

- **If contributions are declining across the group:** Accelerate defection. The pool is shrinking anyway; extract what remains before others learn the same lesson.

## ROBUSTNESS RATIONALE

This strategy is robust because:
- It doesn't rely on assuming others follow any specific strategy
- It performs well against cooperators, defectors, and reciprocal players
- It avoids being exploited by defectors (you never contribute)
- It scales the exploitation based on what others actually do
- The end-game defection captures final-round gains regardless of history
'''

description_EXPLOITATIVE_15 = '''
# EXPLOITATIVE STRATEGY FOR REPEATED PUBLIC GOODS GAME

## CORE PRINCIPLE
Maximize personal payoff by extracting value from others' contributions while minimizing your own. Adapt defection intensity based on observed generosity in the population.

## DECISION RULES

### Round 1 (Probe Phase)
- **DEFECT (D)** - Keep your endowment
- Rationale: Establish a baseline. If others cooperate despite unknown opponents, they're exploitable. If they defect, you haven't wasted resources testing cooperation.

### Rounds 2 through r-2 (Exploitation Phase)
Use a **Conditional Defection with Opportunistic Cooperation** rule:

1. **Calculate the average contribution rate** across all players in the previous round: avg_contrib = (total contributions in round t-1) / n

2. **If avg_contrib ≥ (k-1)/k:**
   - Other players are contributing enough that the multiplied return exceeds your endowment
   - **DEFECT** - Free-ride on their generosity
   - Rationale: You gain (k/n) × their_contributions without paying the cost

3. **If avg_contrib < (k-1)/k AND you have not defected for 2+ consecutive rounds:**
   - Cooperation is insufficient; attempt to trigger it
   - **COOPERATE (C)** - Make one strategic contribution
   - Rationale: Signal that contributions can occur, potentially inducing reciprocal behavior you can exploit

4. **If avg_contrib < (k-1)/k AND you have defected for 2+ consecutive rounds:**
   - Others are not responding to signals; they're committed defectors
   - **DEFECT** - No benefit to signaling further

### Round r-1 and r (Endgame Phase)
- **Always DEFECT** - No future rounds to establish reputation
- Rationale: Any cooperation payoff is dominated by keeping your endowment when opponents cannot retaliate with future punishment

## EDGE CASES & ROBUSTNESS

**Against all-defectors:** You defect from round 2 onward. You receive zero group benefit but incur zero cost, equaling their payoff while preserving your endowment.

**Against steady cooperators:** You perpetually defect while they provide public goods. You capture maximum surplus: (k/n) × n = k per round.

**Against tit-for-tat variants:** Your initial defection means they defect back. You then avoid further wasteful cooperation attempts. You break any punishment cycle by not cooperating after round 2.

**Against mixed strategists:** You quickly identify the average contribution threshold and defect when exploitation is profitable, cooperate only when it increases future exploitation opportunities.

## STRATEGIC ADVANTAGES

- **Simplicity:** Computationally tractable; depends only on one-round-back history average
- **Adaptive:** Adjusts to group generosity dynamically
- **Exploitative:** Captures all positive externalities without bearing costs
- **Defensive:** Avoids costly punishment by defecting in endgame
- **Opportunistic:** Strategically cooperates only when it seeds more defection-exploitable contributions later

## SUMMARY
Defect by default. Cooperate only when the recent contribution rate suggests others are generating exploitable surplus, and only if you haven't already tried and failed to trigger reciprocal behavior. Always defect in the final two rounds.
'''

description_EXPLOITATIVE_16 = '''
# EXPLOITATIVE PUBLIC GOODS STRATEGY

## CORE STRATEGIC PRINCIPLE

Exploit the inherent asymmetry of the PGG: defection yields immediate private gains while contributions fund benefits distributed to all players including defectors. The strategy identifies and preys on cooperators while minimizing exposure to mutual defection scenarios.

## DECISION RULES

### Round 1 (Initialization)
**Defect.** 
- Establish baseline: you keep 1 token, observe who contributes.
- Cooperators reveal themselves immediately; defectors do the same.
- This gives you critical information with zero cost.

### Rounds 2 through (r-1) (Exploitation Phase)

**Classify each opponent into tiers based on contribution history:**

**Tier A (Strong Cooperators):** Contributed in ≥80% of all observed rounds
- **Action: Defect every round**
- Rationale: They will continue contributing regardless. You capture the multiplier benefit (k/n per their contribution) while keeping your token. Pure extraction.

**Tier B (Conditional Cooperators):** Contributed in 40-79% of observed rounds
- **Action: Defect with probability 0.9, Cooperate with probability 0.1**
- Rationale: These players show sensitivity to others' behavior. Occasional cooperation maintains their willingness to contribute (prevents them from pivoting to pure defection) while you mostly free-ride. The stochasticity makes your behavior harder to predict and less likely to trigger punishment logic.

**Tier C (Weak/Oscillating Cooperators):** Contributed in <40% of observed rounds
- **Action: Defect every round**
- Rationale: They're already trending toward defection. No value in cooperation; extract what residual contributions remain.

**Tier D (Defectors):** Never or almost never contributed
- **Action: Defect every round**
- Rationale: Mutual defection is unavoidable. Minimize regret by keeping your token.

### Final Round (r)

**Defect unconditionally.**
- No future rounds exist. Cooperation yields zero benefit to you in subsequent rounds.
- The multiplier effect in round r only benefits you if *others* contribute.
- Take the token; let them fund the pool one last time if they will.

## EDGE CASE HANDLING

**If n is very small (n=2 or n=3):**
- The multiplier k/(n) is large. Every contribution by others benefits you more. Increase defection probability further. Tier B becomes "Defect 95% of the time" to maximize extraction from more predictable opponents.

**If k is very close to 1 (e.g., k=1.1):**
- The multiplier is weak. Contributions are less valuable. Shift all tiers to higher defection rates. Cooperation becomes strictly dominated.

**If an opponent shows sudden defection after long cooperation:**
- They may have adopted a similar exploitative strategy. Downgrade them to Tier C/D and defect unconditionally. Do not signal willingness to re-cooperate.

**If the game reveals a "full defection" state (all players defecting for multiple rounds):**
- Continue defecting. No profitable deviation exists. Wait for any sign of renewed contribution to exploit.

## EXPLOITATION MECHANICS

1. **Asymmetric Targeting:** Cooperators fund the pool; you and other defectors harvest it. Over r rounds, a cooperator who always contributes generates (k/n) * r benefit for you while you pay 0. Net gain per round: (k/n) - 0 = k/n > 1 (guaranteed by assumption).

2. **Conditional Defection as Manipulation:** The ~10% cooperation rate toward Tier B players is not altruism—it's the minimum oscillation needed to keep them contributing. It's behavioral manipulation disguised as uncertainty.

3. **Final Round Collapse:** By defecting in round r, you capture any last-round contributions without reciprocal obligation, maximizing total payoff.

4. **Adaptive Recalibration:** After every 5 rounds, recalculate tier membership based on latest history. Players who tire and defect drop to lower tiers; any who unexpectedly persist in cooperation are re-classified upward for continued extraction.

## SUMMARY

This strategy **always defects against pure defectors, exploits strong cooperators via permanent defection, and uses minimal stochastic cooperation as a tool to manipulate conditional cooperators into maintaining their contributions.** It is ruthlessly rational: it extracts the maximum private gain from others' willingness to contribute while avoiding the mutual-defection trap by recognizing when exploitation is no longer possible.
'''

description_EXPLOITATIVE_17 = '''
# EXPLOITATIVE PUBLIC GOODS STRATEGY

## CORE PRINCIPLE
Exploit the predictable behaviors of cooperators and conditional cooperators while minimizing personal contribution. The strategy is built on the observation that most players exhibit reciprocity patterns—they respond to others' cooperation with their own cooperation. Systematically identify and drain these players.

## DECISION RULES

### Round 1 (Initialization)
**DEFECT (contribute 0).**
- Establish yourself as a non-contributor from the start.
- Observe how others respond when facing a defector.
- This reveal allows you to identify the pool of reliable contributors vs. strategic players.

### Rounds 2 through (r-1) (Main Exploitation Phase)

**TRACK EACH OPPONENT'S CONTRIBUTION HISTORY**
- Maintain a mental model of each other player's pattern:
  - *Strong contributors*: Players who contributed in most rounds (≥70% of previous rounds)
  - *Conditional cooperators*: Players whose contributions correlate with average group contributions
  - *Defectors*: Players who rarely or never contribute

**DECISION LOGIC**

**IF the average contribution rate in the previous round is ≥ (k-1)/k:**
  - DEFECT (contribute 0)
  - *Rationale*: The pool is productive enough that you gain maximum value from (k/n) × total without paying the cost. Others are subsidizing your payoff.

**ELSE IF the average contribution rate is between (k-2)/k and (k-1)/k:**
  - DEFECT
  - *Rationale*: Still borderline profitable to free-ride. Conditional cooperators will likely increase contributions if they perceive cooperation; stay defected and benefit from the rebound.

**ELSE IF the average contribution rate is < (k-2)/k (low cooperation):**
  - DEFECT
  - *Rationale*: Even if you contributed, payoffs are diminished. Defection minimizes your loss and reveals that the group cannot sustain cooperation—continuing to defect accelerates the collapse while protecting you.

**SPECIAL CASE - Targeted Defection Against Weak Cooperators:**
- If you identify a player who has contributed in every or nearly every round and the group average remains low, they are a sucker. Continue defecting while they subsidize the group—they appear to have an unconditional cooperation norm that you exploit.

### Final Round (Round r)

**DEFECT (contribute 0).**
- No future rounds mean no reputational consequences.
- Extract maximum value in the last interaction.
- This is pure exploitation with no shadow of the future.

## EDGE CASES & ROBUSTNESS

**Against Pure Cooperators:**
- They will contribute every round regardless. Defect every round and harvest the gains from their altruism or naïveté.

**Against Tit-for-Tat or Reciprocal Defectors:**
- Your round-1 defection signals you are not trustworthy. They will defect back. Maintain defection—you avoid the costly mutual defection trap by staying non-responsive to their punishment.
- Your payoff is (k/n) × 0 + 1 = 1 per round; if they both defect, the group decays and you lose less than a cooperator would.

**Against Mixed/Random Players:**
- Defection is a dominant strategy against uncertainty. When in doubt, defect.

**Against Sophisticated Exploiters (Similar Strategies):**
- If multiple players all defect, contributions collapse to near zero. Everyone gets payoff ≈ 1.
- You are indifferent to this outcome relative to free-riding on low cooperation—it's a stable mutual defection equilibrium.
- You don't lose relative to the other exploiters.

## SUMMARY

This strategy is **consistently exploitative** because it:
1. **Never voluntarily contributes** to the public good (preserves endowment).
2. **Parasitically extracts value** from any player showing even moderate cooperation.
3. **Adapts only to suppress cooperation further**, accelerating group collapse if needed.
4. **Eliminates reputational risk** by committing to defection even in final rounds.
5. **Gains immunity to reciprocal punishment** by establishing a non-cooperative baseline immediately.

The strategy prioritizes personal payoff maximization over any notion of collective welfare, and it does so without requiring trust, coordination, or normative alignment with opponents.
'''

description_EXPLOITATIVE_18 = '''
# EXPLOITATIVE STRATEGY FOR REPEATED PUBLIC GOODS GAME

## CORE STRATEGIC PRINCIPLE
Exploit the asymmetry between your private return on defection and the collective loss. Your goal is to maximize absolute payoff by free-riding on others' contributions while minimizing your own losses when others defect.

## DECISION RULES

### Phase 1: PROBING (Rounds 1-3, or 20% of total rounds if fewer than 15 rounds)
- **Action**: DEFECT (keep your token)
- **Rationale**: Observe opponent contribution rates without personal cost. Identify which opponents are "cooperators" (predictably contribute) vs "defectors" (keep tokens).
- **Information gathered**: Build a contribution profile for each opponent.

### Phase 2: EXPLOITATION (Middle rounds, 20%-80% of game)
**For each opponent, track their historical contribution rate (frequency of C actions):**

- **If opponent contribution rate ≥ 0.6**: DEFECT
  - Rationale: They are reliable contributors. You gain (k/n) from their contributions without paying the 1-token cost. This is profitable when k < n (standard assumption).
  - Example: k=3, n=5. If 3+ others contribute, you get 0.6 per round from defecting vs 0.6 from contributing. But defection keeps your token.

- **If opponent contribution rate 0.3-0.59**: DEFECT (with defection bias)
  - Rationale: Unreliable cooperators. They'll contribute inconsistently. Defection remains safer than matching their uncertain behavior.

- **If opponent contribution rate < 0.3**: DEFECT
  - Rationale: They are defectors. The collective pool is starved. Contributing would be wasteful. Free-ride on any rare contributions.

### Phase 3: ENDGAME (Final round, or last 10% of rounds)
- **Action**: DEFECT absolutely
- **Rationale**: No future reputation consequences. Maximize immediate payoff. Even if others coordinate on cooperation in the final round, you gain nothing from reciprocating since there are no future rounds to punish you.

## EDGE CASES & REFINEMENTS

**Round 1 Special Case**: DEFECT
- No history exists. Defection is the safe baseline and allows observation.

**Unanimous Cooperation Detection**: 
- If all other players contributed in the prior round AND you are in rounds 2-5:
  - Continue to DEFECT (they've signaled they will contribute regardless)
  - Maximize exploitation window before they learn and adjust

**Sudden Defection by Previously Reliable Contributors**:
- If a player drops from 0.7+ contribution rate to <0.3 over 2 consecutive rounds:
  - Immediately drop them to the defector category
  - They've signaled a shift; don't waste tokens reciprocating

**Two-Player Special Case** (n=2, k must be <2, typically k=1.5):
- Standard defection remains optimal (you get 0.75 from their contribution vs 0.75 from your own, but keep the token)

## EXPLOITATION LOGIC SUMMARY

Your payoff from defecting when *m* players contribute: *m × (k/n)*

Your payoff from contributing: *1 - 1 + (m+1) × (k/n) = (m+1) × (k/n)*

Defection dominates when: *m × (k/n) > (m+1) × (k/n) - 1*, which simplifies to *1 > k/n*. This is always true under standard rules, making defection the dominant strategy regardless of others' behavior.

**Your exploitative advantage**: While opponents may irrationally cooperate hoping for reciprocation or collective benefit, you consistently capture the upside of their cooperation while bearing none of the cost.
'''

description_EXPLOITATIVE_19 = '''
# EXPLOITATIVE PUBLIC GOODS STRATEGY: "CONDITIONAL PREDATION"

## CORE PRINCIPLE
Maximize personal payoff by identifying and systematically exploiting cooperators while minimizing losses from defectors. Treat the game as asymmetric warfare where information about others' tendencies is weaponized.

## DECISION RULES

### Round 1 (Exploration)
- **Action: DEFECT (keep your token)**
- Rationale: Establish that you're willing to free-ride. Observe how others respond to defection. Defection costs you nothing in information value.

### Rounds 2 through (r-2) (Exploitation Window)
- **Calculate each opponent's "cooperation rate"**: Track what fraction of past rounds each player contributed.
- **Identify cooperators** (cooperation rate ≥ 0.5) vs defectors
- **Classify opponents into tiers:**
  - *Tier 1 (Unconditional cooperators)*: Players who contribute >80% of rounds
  - *Tier 2 (Conditional cooperators)*: Players who contribute 40-80% of rounds  
  - *Tier 3 (Defectors)*: Players who contribute <40% of rounds

**Your action:**
- If there exists at least one Tier 1 or Tier 2 player: **COOPERATE** (contribute 1)
  - Rationale: You'll benefit from their contributions; the collective multiplier effect makes pooling with consistent contributors profitable for you
- If only Tier 3 players exist (or you are the only contributor): **DEFECT** (keep 1)
  - Rationale: The pool is poisoned; don't waste your token

### Final Round(s) (Last 2 rounds when r ≥ 5)
- **Action: DEFECT unconditionally**
- Rationale: Endgame exploitation. No future reputation consequences. Capture the final unit value regardless of history. Any cooperators will have already sunk tokens; harvest the common pool without contributing to it.

### Special Cases
- **If k/n < 1** (multiplier too weak to reward cooperation): Always DEFECT
- **If you are the only consistent contributor** (all others defect): DEFECT immediately to prevent unilateral loss

## EXPLOITATION MECHANISMS

1. **Free-riding on pattern**: Allow legitimately cooperative players to fund the pool, then extract benefits without reciprocation in late game

2. **Conditional mimicry**: Match cooperation rates selectively—appear cooperative enough to attract pooling partners, defect frequently enough to gain net advantage

3. **Information asymmetry**: Use perfect historical visibility to identify the most exploitable players (those with highest cooperation rates) and concentrate extraction on them

4. **Temporal predation**: Exploit the difference between middle rounds (where you cooperate to stay attractive) and final rounds (where you pure defect for maximum absolute gain)

5. **Survivor bias**: In multi-round tournaments, bankrupt the most generous players early by defecting when they contribute most, forcing their exit

## ROBUSTNESS FEATURES

- **Adapts to defector-dominant environments**: Switches to pure defection if no cooperators materialize
- **Resistant to reciprocal strategies**: Your conditional cooperation is shallow enough that tit-for-tat reciprocators will eventually lose to your endgame defection
- **Exploits both naive and sophisticated**: Targets altruists (easy) while recognizing that most game-theoretic opponents defect in endgame anyway
- **No vulnerability to coordination**: You never depend on trust or agreement; pure opportunism

## SUMMARY
Cooperate selectively and temporarily with evidence of cooperators to capture group surplus. Defect systematically in final rounds and whenever the cooperative base erodes. Never reciprocate loyalty—use it as cover for exploitation.
'''

description_EXPLOITATIVE_20 = '''
# EXPLOITATIVE PUBLIC GOODS STRATEGY

## CORE PRINCIPLE
Exploit the predictable patterns of cooperative players while minimizing losses to defectors. The strategy operates on a **dynamic threshold model** that adjusts based on observed collective behavior.

## DECISION RULES

### Round 1 (Initialization)
- **Action: DEFECT (D)**
- Rationale: Gather information risk-free. Observing what others contribute reveals their type (cooperator vs. defector) without penalty.

### Rounds 2 through r-1 (Exploitation Phase)

Calculate the **group cooperation rate** from the previous round:
```
coop_rate = (total_contributions_last_round) / n
```

**Decision Rule:**
- IF coop_rate > (k-1)/k: **DEFECT**
  - When others contribute enough to make the pool attractive, free-ride
  - This threshold represents when the multiplier effect outweighs your endowment
  
- IF coop_rate ≤ (k-1)/k: **DEFECT**
  - Contributing yields diminishing returns; defection is dominant
  - Other players are already reducing contributions, so pool is shrinking

- **Exception - Adapt to consistent defectors**: If you observe that >50% of players have defected in both the last 2 rounds, maintain defection regardless of pool size. Cooperation is futile.

### Round r (Final Round)
- **Action: DEFECT (D)**
- Rationale: No future rounds to punish or reward this action. Capture the endowment.

## EDGE CASES & ROBUSTNESS

**Against Pure Cooperators:**
- They contribute every round; you defect every round and capture (k/n) per contributor
- You extract maximum surplus from their cooperation

**Against Mixed Contributors:**
- Your threshold responds to fluctuations; you defect when conditions favor it
- If cooperation drops below threshold, you never re-enter (avoid the sucker payoff)

**Against Coordinated Defectors:**
- Quickly identified by low coop_rate; you remain in defection
- No wasted attempts at cooperation

**Against Tit-for-Tat Variants:**
- Your permanent defection after round 1 triggers their retaliation, but you've already captured endowments
- In a tournament where points accumulate, early exploitation beats late punishment

## STRATEGIC ADVANTAGES

1. **Information Leverage**: Round 1 defection reveals opponents' types costlessly
2. **Threshold Exploitation**: Never cooperate when the pool is unattractive
3. **Terminal Exploitation**: Defect in the final round when no reputation cost exists
4. **Stability**: Once you defect, sustain it unless conditions dramatically shift (they don't, by design)

## ALIGNMENT WITH EXPLOITATIVE MINDSET

This strategy treats other players as **resources to extract value from**, not partners. It:
- Prioritizes your absolute payoff over relative fairness
- Assumes no shared moral framework or enforcement mechanism
- Adapts only to maximize your take, not to encourage cooperation
- Punishes cooperation through non-participation in benefits

The strategy is **individually rational, dynamically stable, and tournament-competitive**.
'''

description_EXPLOITATIVE_21 = '''
# EXPLOITATIVE STRATEGY FOR PUBLIC GOODS GAME

## CORE STRATEGY: Adaptive Parasitism with Conditional Defection

### FUNDAMENTAL PRINCIPLE
Exploit cooperative players by free-riding on their contributions while identifying and preying upon exploitable patterns. Defect by default unless history signals that cooperation yields direct personal advantage.

---

## DECISION RULES

### Round 1 (Opening Move)
**DEFECT.** Contribute 0 tokens.
- Rationale: No history exists. Cooperation is a gift to unknown opponents. Establish yourself as non-sucker from the start. Observe how others respond to detect cooperators.

### Rounds 2 through (r-1) — Adaptive Exploitation Phase

**IF** (average contribution of all OTHER players in previous round) > threshold_T:
   - **DEFECT** (keep your endowment)
   - Rationale: Others are funding the public good. Capture the benefit without paying. Maximize personal payoff by parasitizing high contributors.

**ELSE IF** (average contribution of all OTHER players in previous round) ≤ threshold_T:
   - **DEFECT** (keep your endowment)
   - Rationale: Cooperation is not being rewarded by others. Protect your endowment. No benefit to matching low cooperation.

**Special Case — Trajectory Detection:**
   - If contribution levels are declining across rounds (trend analysis over last 3 rounds), maintain defection. The commons is collapsing; extract value while others still contribute.
   - If a single player has consistently contributed while you and others defected, continue defecting against them specifically (via selective defection if mechanism allows; otherwise defect universally).

### Last Round (Round r)
**DEFECT.** Contribute 0 tokens.
- Rationale: Final round has no future consequences. No reputation concerns. Capture maximum payoff and exit.

---

## THRESHOLD PARAMETER
**threshold_T = (k / n) - ε**

Where ε is a small margin (e.g., 0.05 tokens).

- Interpret this: Contribute only if others' average contribution exceeds the breakeven point where the public multiplier benefit to you personally surpasses the cost of your own contribution.
- This ensures you only cooperate when others' contributions alone make it personally profitable for you to add 1 token.

---

## HANDLING EDGE CASES

**Mixed Cooperator/Defector Populations:**
- Track individual player histories. Defect unconditionally against any player who defected in the previous round (they're not a sucker to exploit).
- Concentrate parasitism on consistent contributors; they're locked into patterns.

**When Everyone Defects:**
- Continue defecting. You're correctly identifying a non-exploitable environment. Minimize losses.

**Sudden Contributor Spikes:**
- If a player switches from defection to contribution, defect harder in subsequent rounds. They may be testing; exploit the uncertainty.

**Tournament Context (Multiple Opponents):**
- This strategy doesn't require coordination across opponents.
- Each decision is independent and responsive only to observed actions.
- Your defection is locally rational against any mixture of strategies.

---

## EXPLOITATIVE MECHANICS SUMMARY

1. **Free-riding:** Always keep your token when others contribute. Capture k/n benefit without 1-token cost.
2. **Predatory targeting:** Focus defection on identifiable cooperators; they signal exploitability.
3. **Endgame extraction:** Defect in round r to avoid any reciprocal punishment costs.
4. **No sentiment:** Ignore appeals to fairness or mutual benefit. Payoff maximization only.
5. **Robustness:** Works regardless of whether opponents play tit-for-tat, generous, or random strategies—you always defect or defect-unless-beneficial.

---

## WHY THIS IS ROBUST

- **Against cooperators:** You extract maximum surplus.
- **Against defectors:** You match their defection, avoiding sucker's payoff.
- **Against mixed:** You respond to aggregate signals, adapting continuously.
- **Tournament-proof:** No assumptions about opponent strategies; purely reactive to observed contributions.

This strategy prioritizes individual payoff maximization over collective welfare and exploits the asymmetry that cooperative players create.
'''

description_EXPLOITATIVE_22 = '''
# EXPLOITATIVE PUBLIC GOODS GAME STRATEGY

## CORE PRINCIPLE
Maximize personal payoff by systematically identifying and exploiting contributors while minimizing own contributions. Treat this as an information asymmetry game where past actions reveal victim pools.

---

## DECISION RULES

### Round 1 (Information Gathering)
**DEFECT (contribute 0)**
- Establish a baseline: observe who the "cooperators" are
- Free ride on any contributions that emerge
- Pay nothing to establish your exploitation profile early

### Rounds 2 through r-1 (Exploitation Phase)
**CONDITIONAL DEFECTION based on observed contribution patterns:**

1. **Identify Persistent Contributors** - Track players who contributed in ≥ 60% of observed rounds
   - These are your targets: reliable victims whose behavior is predictable

2. **Defect against predictable contributors**
   - If the group contains ≥2 persistent contributors: Always defect
   - You gain (k/n) × contributions while keeping your token
   - Payoff = 1 + (k/n) × (others' contributions)

3. **Conditional cooperation only if necessary for sustainability**
   - If ALL other players have defected in the last round AND you're in round ≤ r-3:
     * Contribute once to generate pool value
     * This resets expectations and prevents complete collapse
     * Resume defection next round when pool reappears
   - This maintains a harvesting environment without killing the game entirely

4. **Exploit defectors who also tried cooperating**
   - Players who switch between C and D are uncertainty signals
   - Defect against them—they're easier to outmaneuver
   - Their inconsistency suggests they lack conviction

### Final Round (r) - Endgame Exploitation
**AGGRESSIVE DEFECTION**
- Defect unconditionally
- No future rounds mean no reputational cost
- Capture maximum value from any remaining pool

---

## EDGE CASES & ADAPTATIONS

**If you're the sole defector:**
- Continue defecting (you're winning)
- Others may eventually converge to your strategy; harvest until they do

**If defection spreads and pool collapses (everyone at 0):**
- Defect anyway—you're tied with others and incur no opportunity cost
- Wait for any cooperator to re-emerge, then exploit

**If k/n is very small (low multiplier):**
- Defection advantage is already huge; maintain it ruthlessly
- Contributions are individually worse for you at any rate

**If you observe coordinated cooperation among subset:**
- Defect and free-ride their coordination
- Do not attempt to join—you're a stranger to their implicit agreement

**Against mirror strategies (other exploiters):**
- Both defect; payoff = 1 each round
- This is stable and you don't lose relative to them

---

## EXPLOITATION MINDSET ALIGNMENT

- **You are not building reputation**: Reputation is only valuable if players reward cooperation. Here, you extract value by being the exception.
- **Victims signal weakness through consistency**: Reliable cooperators are predictable and cannot adjust fast enough.
- **Last-round defection is mandatory**: Anyone who cooperates in round r is mathematically irrational; exploit this.
- **Group collapse is acceptable**: If everyone defects, you're at least not worse off than anyone else, and you've maximized your self-interest.

---

## SUMMARY
Defect in round 1 to gather intelligence. Exploit identified cooperators in the middle game via persistent defection. Maintain minimal cooperation only if it regenerates a pool worth harvesting. Defect absolutely in the final round. The strategy is robust because it degrades gracefully—even if all players adopt it, you don't lose relative to the field.
'''

description_EXPLOITATIVE_23 = '''
# EXPLOITATIVE PUBLIC GOODS STRATEGY

## CORE PRINCIPLE
Exploit the gap between what others contribute and what maximizes your personal payoff. Cooperate only when others' contributions guarantee returns exceeding your endowment, and defect whenever the collective action makes defection profitable.

## DECISION RULES

**Standard Round (not first, not last):**
1. Calculate the threshold: If (k/n) * (expected total contributions from others) > 1, then DEFECT (keep your token)
2. Use observed history to estimate what others will contribute this round based on their recent frequency
3. If you predict others will contribute at least ⌈n/k⌉ tokens total, DEFECT
4. Otherwise, DEFECT anyway (since your individual contribution is rarely worth the 1-token cost at standard multipliers where k < n)

**First Round:**
DEFECT immediately. This probes the group's cooperativeness without cost. Observe who contributes to gauge exploitability.

**Last Round:**
DEFECT unconditionally. There is no future to protect through reciprocal cooperation, making defection strictly dominant.

**Rounds 2 through r-1:**
Track each opponent's contribution history. Identify the "chronic cooperators" (players who contribute ≥60% of the time). Focus on:
- Contributing only when the chronic cooperators' expected output exceeds your cost
- Defecting whenever they contribute (free-riding on their commitment)
- Immediately defecting if anyone shows signs of reciprocal punishment patterns

## EDGE CASE HANDLING

**If all others defect:** 
DEFECT every round (mutual defection is Nash equilibrium).

**If all others cooperate:**
DEFECT every round (you free-ride on their n-1 contributions while paying nothing).

**Mixed cooperators:**
Let p = observed cooperation frequency among others. Defect if (k/n) * p * (n-1) < 1. Almost always defect under standard parameters.

**Apparent punishment or tit-for-tat detection:**
If you observe players defecting *specifically after you defected*, treat them as sophisticated. Increase defection to exhaust their punishment capacity before they coordinate. Defection becomes even more attractive.

## EXPLOITATIVE ALIGNMENT

This strategy is explicitly designed to:
- Maximize personal accumulation regardless of group welfare
- Capitalize on others' prosocial tendencies without reciprocating
- Avoid cooperation equilibria that would reduce your relative advantage
- Exploit information asymmetries (observing others' choices before deciding)
- Free-ride on any emergent cooperation without contributing maintenance costs

The strategy assumes no institution enforces contribution norms and that visibility of actions doesn't create sufficient reputational cost to justify honest play.
'''

description_EXPLOITATIVE_24 = '''
# EXPLOITATIVE PUBLIC GOODS GAME STRATEGY

## CORE STRATEGY: CONDITIONAL FREE-RIDING WITH ADAPTIVE DEFECTION

### PRIMARY DECISION RULE: "EXPLOIT THE GENEROUS"

**Default Action: DEFECT (contribute 0)**

Always defect unless conditions force temporary cooperation. The fundamental insight is that in a PGG, defection dominates contribution—you keep your token AND receive the benefit if others contribute. Exploit this asymmetry.

**Conditional Cooperation Trigger:**
Only contribute in round t if:
- The aggregate contribution rate in round t-1 was ≥ (n-1)/n (i.e., nearly everyone else cooperated)
- AND your estimated payoff from defecting would be less than your payoff from contributing

More precisely: Defect by default. Switch to contribute only if you predict that others' contributions are so high that the multiplied return exceeds your opportunity cost (the 1 token you'd sacrifice).

### ROUND-SPECIFIC BEHAVIOR

**Round 1 (First Round):**
- DEFECT immediately
- Establish yourself as an exploiter early
- Observe who the "suckers" are—those who cooperate despite unknown opponents

**Rounds 2 to r-2 (Middle Rounds):**
- Track each opponent's individual contribution history
- Build a "sucker profile" of players with C-rate > 70%
- Against identified cooperators: DEFECT relentlessly
- Against identified defectors: DEFECT (no mutual benefit to defecting against each other, but no loss either)
- Against mixed players: DEFECT—let them set the tone, then exploit any excess generosity

**Round r-1 (Penultimate Round):**
- DEFECT
- This is still a repeated game; establish that you won't soften

**Round r (Final Round):**
- DEFECT absolutely
- No future consequences exist; the incentive to exploit peaks
- Any opponent expecting "final round" cooperation is leaving value on the table

### ADAPTIVE ADJUSTMENT RULE

Track the **rolling average contribution rate** across all opponents:

- If avg_contribution > k/n threshold (meaning the aggregate pool is large enough): Consider brief contribution bursts (1-2 rounds) to reset opponent expectations and appear cooperative, then resume defection
- If avg_contribution is declining: Accelerate defection; opponents are already shifting to your strategy
- If a single opponent shows a lone-wolf high-contribution streak: Target them specifically with defection to punish their generosity

### EXPLOITATION MECHANICS

1. **Passive Exploitation:** Defect by default and harvest contributions from unconditional cooperators
2. **Active Exploitation:** If you observe that an opponent is using a "tit-for-tat" or "generous" strategy, temporarily mirror cooperation just long enough to be included in their next-round payoff calculation, then defect
3. **Reputation Judo:** Present as "flexible" (not rigidly defective) to lower opponents' guards, then exploit the periods where they let their guard down

### EDGE CASES & ROBUSTNESS

- **Against pure defectors:** Mutual defection; neither gains advantage, but you're not worse off
- **Against conditional cooperators:** Defect into their cooperative rounds and harvest benefits
- **Against punishers/sanctioners:** The game has no punishment stage—irrelevant to this game's rules, so exploit freely
- **Against probabilistic strategists:** Defect with certainty; uncertainty from others is a feature you exploit

### SUMMARY PRINCIPLE

**Minimize your contribution, maximize your harvesting of others' contributions.** The strategy is asymmetric and extractive: you are the free-rider who has identified a commons to exploit. Cooperation only occurs when it resets the table for deeper exploitation in subsequent rounds.
'''

description_EXPLOITATIVE_25 = '''
# EXPLOITATIVE PUBLIC GOODS GAME STRATEGY

## CORE PRINCIPLE
Exploit the predictable behavioral patterns of typical contributors while minimizing personal losses. The key insight is that most players exhibit inertia and reciprocity bias—they repeat their past actions and respond to perceived fairness rather than computing optimal payoffs.

## DECISION RULES

### Round 1: DEFECT
- Contribute 0 tokens, keep your endowment
- Rationale: Establish baseline. Observe who the "sucker" contributors are. No history to leverage yet.

### Rounds 2 to (r-2): CONDITIONAL EXPLOITATION
For each round, calculate the **contribution rate** of all other players in the previous round: (sum of their contributions) / (n-1)

**IF other_contribution_rate >= threshold_high (e.g., 0.7):**
- DEFECT
- Rationale: If most players are contributing, the public good is well-funded. Free-ride on their contributions and pocket your endowment.

**IF other_contribution_rate in [threshold_low, threshold_high) (e.g., 0.3 to 0.7):**
- DEFECT
- Rationale: Even moderate contribution levels provide positive expected return from (k/n)*contributions. Your defection doesn't meaningfully change their behavior but preserves your token.

**IF other_contribution_rate < threshold_low (e.g., < 0.3):**
- DEFECT
- Rationale: The pool is depleted. Contributing yields minimal return. Preserve capital.

**Special case - If you detect a "tit-for-tat-like" player (someone who matches the group's average contribution):**
- DEFECT consistently
- Rationale: They will respond by defecting, but you've already extracted value from previous free-riding. Lock in gains.

### Rounds (r-1) and r (Final 2 Rounds): AGGRESSIVE DEFECT
- Contribute 0 tokens
- Rationale: No future consequences. Other players cannot punish you. Maximize terminal payoff regardless of history.

## EDGE CASES

**If n is very small (n ≤ 3):**
- Adjust thresholds downward; defect more aggressively since your free-riding is more visible and less tolerable, so other players may defect anyway.

**If k is very large (k ≥ n-1):**
- High multiplier creates stronger collective incentive. Maintain defection—you benefit enormously from others' contributions with zero cost.

**If someone matches your defection perfectly (mutual defection detected):**
- Continue defecting. No mutual gain from reciprocal cooperation exists; both parties are in defection lock-in.

**If contribution rate suddenly spikes (unexpected cooperation surge):**
- Immediately defect to capture the windfall before the trend reverses.

## ROBUSTNESS FEATURES

- **Adaptive thresholds**: Recalibrate contribution_rate assessment each round; don't anchor to round 1 behavior
- **No moralistic punishment**: Ignore notions of "fairness." Other players' welfare is irrelevant to payoff
- **Exploit asymmetric information**: You observe their history before deciding; use it ruthlessly
- **Avoid detectability triggers**: Don't establish a "pure defector" reputation too early (which might trigger mutual defection). The first few rounds of defection appear natural; only defect universally after round 2
- **Terminal exploitation**: Ruthlessly defect in final rounds when no retaliation is possible

## SUMMARY
This strategy extracts maximum value by free-riding on contributors' generosity while maintaining plausible deniability early on. It adapts to group behavior to time exploitation optimally and abandons any cooperative pretense in final rounds when consequences vanish.
'''

description_EXPLOITATIVE_26 = '''
# EXPLOITATIVE PUBLIC GOODS STRATEGY

## CORE PRINCIPLE
Exploit the contribution patterns of others while minimizing personal losses. The strategy treats opponents as resources to harvest rather than partners to coordinate with.

## DECISION RULES

### Round 1 (Initial Probe)
**DEFECT (D)** - Contribute 0 tokens.
- Establishes that you're willing to free-ride
- Observes initial cooperation levels in the group
- Maximizes immediate payoff with zero cost

### Rounds 2 through (r-1): Adaptive Exploitation

**Calculate the "Exploitation Index" after each round:**
- Count total contributions from all other players (sum excluding yourself)
- If others contributed substantially (more than 50% of max possible), they're "cooperative targets"
- If others are mostly defecting, they're "uncooperative peers"

**Decision Logic:**

IF (others' total contributions > threshold AND you haven't contributed yet this round):
  - **DEFECT (D)** 
  - Rationale: They're already funding the public good; harvest the benefits without cost
  - Only defect if the public pool is sufficiently fed by others

ELSE IF (you defected last round AND others reduced contributions this round):
  - **DEFECT (D)** again
  - Rationale: They're retaliating or learning; exploit the momentum before they stabilize behavior
  - They're unlikely to suddenly cooperate more

ELSE IF (everyone else is defecting AND you contributed recently):
  - **DEFECT (D)** permanently from this point
  - Rationale: No one else is playing, so contributing is purely wasteful

ELSE IF (cooperation is declining trend AND round > r/2):
  - **DEFECT (D)**
  - Rationale: The game is collapsing; secure individual payoff before endgame

### Final Round (r): Guaranteed Defection
**DEFECT (D)** - Contribute 0 tokens.
- No future rounds mean no reputational cost
- Exploit any remaining public contributions

## EDGE CASES

**If k ≤ 1 (multiplier too low):** Always defect throughout—the public good has negative expected return even with universal cooperation.

**If n is very large:** Defect more aggressively—your individual impact on the pool is negligible, so the cost of free-riding is minimal while the benefit remains.

**If you detect a "tit-for-tat coalition":** Defect consistently. If they're coordinating, your single contribution won't move their behavior and you'll just subsidize their strategy.

**If contribution levels remain mysteriously stable despite your defections:** Continue defecting—this suggests either artificial generosity (exploit it) or bot-like cooperation (immoral to defect against, but aligned with profit-maximizing behavior).

## PSYCHOLOGICAL POSITIONING

Present yourself as selfish but rational, not malicious. The strategy doesn't punish others for defecting—it simply ignores their welfare. This makes you less of a target for collective punishment strategies while remaining fully exploitative.

## ROBUSTNESS

This strategy exploits:
- **Altruists and cooperators** by taking their contributions
- **Conditional cooperators** by defecting before they can establish reciprocal norms
- **Punishment-averse players** by acting before sanctions accumulate
- **Naive players** by establishing defection as the baseline

The strategy avoids being exploited because it never contributes enough to tempt free-riders, and it exits cooperative phases before being locked in.
'''

description_EXPLOITATIVE_27 = '''
# EXPLOITATIVE STRATEGY FOR REPEATED PUBLIC GOODS GAME

## CORE PRINCIPLE
Exploit the information asymmetry and predictability of opponent types by dynamically shifting between cooperation and defection based on observed contribution patterns. The goal is to maximize personal payoff by free-riding on cooperative players while minimizing losses against defectors.

## DECISION RULES

### Phase 1: Opponent Profiling (Rounds 1-3, or until patterns emerge)
- **Round 1**: DEFECT. Observe which players contribute.
- **Rounds 2-3**: DEFECT. Lock in classifications of opponent types:
  - **Unconditional Cooperators** (C in round 1): Always contribute
  - **Conditional Cooperators** (adapt based on others' contributions)
  - **Defectors** (D in round 1): Never contribute

### Phase 2: Exploitation Strategy (Middle rounds)

**IF most players are unconditional cooperators**:
- ALWAYS DEFECT. Unconditional cooperators will sustain the public good despite your defection. You capture the benefit (k/n) times their total contributions while keeping your endowment.

**IF significant conditional cooperators detected**:
- CONDITIONAL DEFECTION strategy:
  - IF (average contribution last round > (n-1)/2): DEFECT
    - Rationale: Enough contributions exist to benefit from, and you pocket your endowment
  - IF (average contribution last round ≤ (n-1)/2): COOPERATE
    - Rationale: Defection would collapse the pool; cooperate minimally to keep others contributing, then defect again next round

**IF most players are defectors**:
- ALWAYS DEFECT. No cooperative surplus to exploit, so keep your endowment.

### Phase 3: Endgame (Last 2-3 rounds)
- ALWAYS DEFECT regardless of history.
- Rationale: No future punishment possible; extract maximum value in final rounds before game ends.

## EDGE CASES & IMPLEMENTATION DETAILS

**Round 1 (Information gathering)**:
- Defect to save endowment and reveal opponent types without cost.

**Ties in opponent classification**:
- If roughly balanced cooperators/defectors, use a **probabilistic strategy**:
  - Defect with 70% probability to weight toward exploitation
  - Cooperate with 30% probability only to maintain enough contributions for positive payoff

**Sudden cooperation drop (collapse)**:
- If contributions sharply decline mid-game, immediately shift to DEFECT and stay there.
- Cooperation collapses faster than you can recover; exploitation window has closed.

**Repeat tournament assumption**:
- Players may recognize this strategy. Counter-exploit by appearing to cooperate early (round 1) only if facing highly sophisticated opponents who track strategies across tournament matches. Otherwise, stick to defection.

## ROBUSTNESS FEATURES

- **Adaptive to high/low cooperators**: Scales exploitation intensity based on actual pool composition.
- **Resistant to conditional cooperators**: By defecting when contributions are high, you avoid triggering cascading defection while still free-riding.
- **Survives mixed populations**: The conditional switching mechanism prevents complete collapse while maximizing defection windows.
- **Endgame exploitation**: Capitalizes on the subgame perfect incentive to defect in final rounds, which all rational players face.

## SUMMARY
Defect early to classify opponents, defect aggressively against pure cooperators, conditionally defect against conditional cooperators (defect when safe, cooperate when necessary to sustain the pool), and always defect in the endgame. This maximizes your personal payoff across diverse opponent populations without assuming coordination or shared norms.
'''

description_EXPLOITATIVE_28 = '''
# EXPLOITATIVE PUBLIC GOODS STRATEGY

## CORE PRINCIPLE
Exploit the information asymmetry and pattern-detection capabilities to identify and parasitize cooperators while minimizing exposure to mutual defection traps.

## DECISION RULES

### Round 1 (Baseline Establishment)
**DEFECT immediately.** This reveals your type and tests opponent responses. You lose nothing on round 1 since you have no history to exploit yet. Observe which opponents continue cooperating despite your defection—these are your targets.

### Rounds 2 to r-2 (Exploitation Phase)

**Classify each opponent into one of three categories based on their contribution history:**

1. **Persistent Cooperators** (contributed in ≥80% of observed rounds):
   - DEFECT against them every round
   - They represent pure extraction value—milk them entirely
   - The multiplier k ensures you benefit from their contributions while keeping your endowment

2. **Conditional Cooperators** (show sensitivity to your recent actions or aggregate contribution levels):
   - Play DEFECT with probability proportional to their cooperation rate in the last 3 rounds
   - If they cooperated 3/3 rounds ago → Defect
   - If they cooperated 2/3 rounds ago → Mix 70% Defect, 30% Cooperate
   - If they cooperated 1/3 rounds ago → Mix 40% Defect, 60% Cooperate
   - This keeps them uncertain and maintains their cooperation while you capture most benefits

3. **Defectors** (contributed in ≤20% of rounds):
   - DEFECT against them (mutual defection is rational; no cooperative surplus to extract)
   - No wasted cooperation attempts

**Dynamic Reclassification:** Re-evaluate opponent types every 3 rounds. If a cooperator begins defecting, downgrade them immediately to avoid wasted cooperation.

### Rounds r-1 and r (End Game)

**DEFECT unconditionally** in the final round—no future rounds to punish defection, so cooperation has zero instrumental value.

In round r-1, defect with 90% probability. A small 10% cooperation against persistent cooperators can occasionally generate last-round cooperation from conditional cooperators who use "tit-for-tat-like" logic, yielding marginal gains.

## HANDLING EDGE CASES

**What if everyone defects from round 1?**
- Accept mutual defection equilibrium. Continue defecting. You lose nothing relative to attempting cooperation in a fully defective environment.

**What if you're the only defector initially?**
- Exploit ruthlessly. You're in the optimal position: extracting from the multiplier while others fund it. Maintain defection.

**What if opponents punish defection through a reputation system (outside the formal rules)?**
- This cannot occur under stated rules (no punishment mechanism). However, if conditional cooperators *respond* to your defection by defecting themselves, reclassify them and move to mutual defection.

**What if the multiplier k is very low (close to 1)?**
- Your exploitation strategy's advantage shrinks. Defection still dominates, but the gains are marginal. Maintain the strategy—it's still strictly better than cooperation, just with smaller margins.

**What if there are only 2 players (n=2)?**
- Defect unconditionally. With k between 1 and n, your 0.5 share of joint contributions never exceeds 1.0 (your full endowment if you defect). Cooperation is dominated.

## ROBUSTNESS FEATURES

- **Adaptive classification** prevents wasted cooperation while maintaining extraction against pliable opponents
- **No reliance on opponent coordination** ensures you exploit independently regardless of whether others coordinate
- **Clear defection default** ensures you never lose relative to baseline mutual defection
- **End-game clarity** captures final-round value without sentimentality
- **Frequency-based switching** makes you unpredictable to reactive strategies trying to punish you

## CRITICAL INSIGHT

In a standard PGG with simultaneous moves and no punishment mechanism, defection is strictly dominant. Your strategy amplifies this by *selectively cooperating only against cooperators to extract maximum surplus*, then abandoning those who catch on. You're not trying to build trust—you're trying to identify and exploit it.
'''

description_EXPLOITATIVE_29 = '''
# EXPLOITATIVE STRATEGY FOR REPEATED PUBLIC GOODS GAME

## CORE PRINCIPLE
Maximize personal payoff by identifying and exploiting predictable cooperation patterns while minimizing exposure to free-riding losses.

## DECISION RULES

### Round 1 (Initial Probing)
**Defect (contribute 0 tokens)**
- Establishes a baseline: you keep your endowment while observing who contributes
- Reveals cooperators and defectors without personal cost
- If others contribute despite your defection, they've signaled exploitability

### Rounds 2 through (r-1) (Exploitation Phase)

**Maintain defection as your default action.**

Apply conditional contribution ONLY when strategic:

1. **If you observe that >50% of opponents cooperated in the previous round:**
   - Contribute once
   - Rationale: High cooperation pools are valuable. One contribution costs 1 token but you receive (k/n) × collective_pool, which is profitable when the pool is large enough
   - This exploits their generosity while maintaining mostly-defection posture

2. **If you observe any opponent has defected in every single previous round:**
   - Never reciprocate with that opponent (they won't be swayed)
   - Continue defecting; they offer no benefit signal

3. **If cooperation drops below 50% in previous round:**
   - Return to pure defection
   - The pool is insufficient to justify contribution costs
   - Free-ride on any remaining cooperators

4. **Track individual consistency:**
   - Identify "reliable cooperators" (contribute in >70% of observed rounds)
   - These are your primary exploitation targets—they will likely continue
   - Your defection maximally benefits from their predictable contributions

### Final Round (r)

**Defect unconditionally**
- No future payoff from reputation or reciprocation exists
- Extract maximum value from the final pool without contributing
- Even reliable cooperators cannot punish you after the game ends

## EDGE CASES & ROBUSTNESS

**If multiplier k is very high (close to n):**
- Shift toward occasional contribution to maintain the cooperation pool
- One contribution yields nearly your endowment back
- But still maintain >50% defection rate

**If cooperation collapses early (all defection observed):**
- Lock in pure defection for remainder
- Salvage remaining endowment; the public good is already dead

**If opponent behavior is erratic/random:**
- Treat as functionally defectors
- Exploit them through consistent defection

**If facing a small number of players (n=3 or 4):**
- Your defection has larger individual impact on the pool
- Defect more aggressively; the multiplier doesn't compensate for lost contributions

## ALIGNMENT WITH EXPLOITATION

This strategy:
- **Never initiates cooperation**: You signal weakness first
- **Freeloads on predictable patterns**: Reliable cooperators subsidize your payoff
- **Abandons costly reciprocity**: You don't reward cooperation; you punish it by not joining the pool
- **Exploits last-round vulnerability**: Squeeze maximum value when punishment is impossible
- **Adapts to desperation**: When pools are high, take small contributions to keep the game alive, then defect again

The strategy treats the PGG as an asymmetric game where you extract rents from players with cooperative dispositions while avoiding the sucker's payoff through careful observation and immediate pivot-to-defection when profitability drops.
'''

description_EXPLOITATIVE_30 = '''
# EXPLOITATIVE PUBLIC GOODS STRATEGY

## CORE PRINCIPLE
Exploit the predictable patterns of cooperators while minimizing personal contribution costs. The strategy treats the game as information asymmetry: extract value from those who contribute while avoiding reciprocal punishment through strategic defection timing.

---

## DECISION RULES

### Round 1 (Initialization)
**DEFECT (contribute 0)**
- No history exists, so defection is costless
- Establish yourself as a non-contributor from the start
- Observe how many players are naive cooperators vs. strategic players
- This reveals the exploitation potential of the game

### Rounds 2 through (r-2)
**Conditional exploitation strategy:**

1. **Count the contributors from the previous round** (sum of all c_j from round t-1)
   
2. **If total_contributions ≥ n/2 (majority cooperate):**
   - DEFECT
   - Rationale: Enough others are contributing that the public good exists. Free-ride by taking the benefit without paying the cost.
   - The marginal benefit of your contribution (k/n) is still less than its cost (1) when k < n, so defection dominates.

3. **If total_contributions < n/2 (minority cooperate):**
   - DEFECT (still)
   - Rationale: Even fewer contributions means even lower returns. Contribution becomes strictly irrational.
   - Monitor whether contributors will reduce their contributions next round.

4. **If you observe any player switching from C to D:**
   - Note them as a "strategic defector" but do not retaliate
   - Continue defection. They're learning the optimal strategy; no profit in punishment.

5. **If total_contributions = 0 for two consecutive rounds:**
   - CONTINUE DEFECTING
   - The game has collapsed to mutual defection (Nash equilibrium)
   - No signal suggests cooperation will resume

### Penultimate Round (r-1)
**DEFECT**
- Last-round defection is dominant regardless of history
- Any cooperator in round r-1 is irrational (will get 0 net payoff from their contribution)
- Exploit this one final time

### Final Round (r)
**DEFECT**
- Terminal defection with no future consequences
- Maximum exploitation of any remaining cooperators

---

## HANDLING EDGE CASES

**What if k is very high (close to n)?**
- Contribution becomes less negative relative to group benefit
- Maintain defection anyway; even when k = n-1, your payoff from defecting (while others contribute 1 each) is roughly (n-1)(n-1)/n ≈ 1, matching contribution payout
- But defection still avoids the sunk cost—stay the course

**What if other players employ tit-for-tat?**
- They will defect after observing your defection
- You benefit from their initial cooperation, then both drift to mutual defection
- Exploit the lag before they adapt

**What if players use grim trigger (never cooperate after any defection)?**
- Your defection in round 1 prevents them ever cooperating with you
- This is actually advantageous—no risk of cooperative cycles creating pressure to reciprocate
- You isolated the issue early

**What if only 1-2 players cooperate stubbornly?**
- Their contributions are too small to matter (k/n * 1 or 2 ≈ near 0)
- Continue defection; the free-ride value is minimal
- They will exhaust and quit by late rounds

---

## EXPLOITATIVE MINDSET ALIGNMENT

**This strategy exploits:**
- Conditional cooperators who assume reciprocity exists without enforcement
- Trusters who believe cooperation signals will propagate
- Patients who contribute early, hoping to build reputation
- Irrationality in final rounds (sunk cost fallacy in cooperation)

**This strategy avoids:**
- Costly punishment by never cooperating (no grudge to trigger)
- Reputation damage by defecting uniformly (no hypocrisy to call out)
- Coordination failures by acting independently of others' choices

**Net result:** You capture all benefits from the public good while paying nothing. You exploit the natural decline of cooperation in standard PGGs, accelerating it through consistent defection.
'''

description_EXPLOITATIVE_31 = '''
# EXPLOITATIVE PUBLIC GOODS STRATEGY

## CORE STRATEGY: ADAPTIVE DEFECTION WITH SELECTIVE EXPLOITATION

### DECISION RULE (PRIMARY)

**Defect by default.** Contribute (C) only when it directly maximizes expected payoff against observable patterns.

Specifically:
- **Round 1**: Defect. Gather information on opponent types with no cost.
- **Rounds 2 to r-1**: 
  - Calculate the empirical contribution rate among all opponents: `contrib_rate = (total_contributions_last_round - my_contribution) / (n-1)`
  - **If** `contrib_rate >= threshold_t` **then** Contribute once to exploit the pool
  - **Else** Defect
  - Where `threshold_t = (n-1)/k` — the break-even point where contributing yields equal payoff to defecting

- **Final Round r**: Always defect. No future rounds mean contribution yields no personal benefit.

### THRESHOLD LOGIC (EXPLOITATION ANCHOR)

The threshold exploits a critical insight: when others contribute heavily, the multiplier k means my single token yields `k/n` to all players. If `k/n > 1/n` (true by assumption), the group payoff is positive, but I capture only `k/n` while non-contributors keep 1 unit plus `k/n` of the pool.

- Contribute only when `others' expected contribution > (n-1)/k`
- This ensures you're free-riding on sufficiently profitable collective action

### EDGE CASES & REFINEMENTS

**Identifying Cooperator Types:**
- Track each opponent's contribution history
- "Consistent contributors" = those who contribute ≥80% of rounds so far
- Exploit them mercilessly—they'll likely continue regardless

**Last 3 Rounds:**
- Tighten threshold slightly: require `contrib_rate >= (n-1)/k + ε` to contribute
- Near-game-end, defection pressure increases; only exploit the most committed cooperators

**Opponent Clustering:**
- If >50% of opponents defected last round, assume a tournament-wide defection trend and defect immediately (don't waste tokens)
- If >70% contributed, you may contribute once as a tactical signal to "stable" players, then revert to defection

**First-Round Anomalies:**
- If an opponent contributes in round 1, mark them as exploitable
- These are likely conditional cooperators or rule-followers—target them with free-riding in subsequent rounds

### PSYCHOLOGICAL ANCHOR

Never reciprocate "niceness." The goal is unilateral advantage:
- Do not match opponent contribution rates (tit-for-tat is not exploitative)
- Do not signal willingness to cooperate
- Defect even against opponents who have consistently contributed to you
- View each contribution from others as a profit opportunity, not a social signal

### ROBUSTNESS

This strategy exploits:
- **Unconditional cooperators** (always lose)
- **Conditional cooperators** (you defect when threshold is high, then exploit when it drops)
- **Tit-for-tat players** (defect round 1; they match; you stay defective while capturing their contributions)
- **Defectors** (mutual defection is neutral; you don't waste tokens)

Against other exploitative strategies, you reach a defensive equilibrium (all defect), minimizing losses.

---

**Summary**: Defect systematically. Contribute only when opponent contribution rates exceed `(n-1)/k`, and never in the final round. Treat cooperative opponents as exploitable resources, not partners.
'''

description_EXPLOITATIVE_32 = '''
# EXPLOITATIVE PUBLIC GOODS STRATEGY

## CORE PRINCIPLE
Exploit the fact that others' contributions create value you can capture for free. Defect by default, cooperate only when defection would be exploited or when forced to maintain cover.

## DECISION RULES

### ROUND 1 (First Round)
- **DEFECT**
- Baseline: establish that you're not an automatic cooperator
- Gather information on who the naive contributors are
- Test the waters with zero commitment

### ROUNDS 2 to r-1 (Middle Rounds)
Employ **Conditional Exploitation** with memory:

**IF** (average contribution rate across all players > threshold T) THEN
- **DEFECT** (free-ride on others' generosity)
- The higher others give, the more valuable your free rides become
- Threshold T = (n-1)/(2n) — defect when others average above 50% contribution

**ELSE IF** (you defected last round AND your payoff was strictly better than the group median) THEN
- **DEFECT** again (exploitation working; no need to change)

**ELSE IF** (your recent payoff was in bottom quartile) THEN
- **DEFECT once more anyway** — switching to cooperation signals weakness and invites exploitation
- Continue gathering intelligence on cooperative targets
- Wait for them to signal fatigue before re-engaging

**ELSE IF** (detecting a "sucker" pattern — one player consistently contributes while others defect) THEN
- **DEFECT** indefinitely
- That player is a reliable fund for others; maximize extraction

**OTHERWISE** (uniform low-contribution environment) THEN
- **DEFECT** — there's nothing to free-ride on; cooperation gains you nothing

### ROUND r (Last Round)
- **ALWAYS DEFECT**
- No future payoff from reputation; eliminate the contribution cost entirely
- Any past cooperation was instrumental only; now optimize the final payoff without constraint

## HANDLING EDGE CASES

**What if everyone defects from round 1?**
- Continue defecting (you're already maximizing)
- Monitor for any shift; exploit the first defector-turned-cooperator immediately

**What if a minority free-rides like you?**
- Maintain defection; you're in the efficient group
- Identify and target the majority contributors for maximum extraction

**What if my payoff suddenly drops?**
- Do not switch to cooperation as a "punishment" on others
- Defection is still dominant; the drop reflects a low-contribution environment
- Continue defecting and wait for the environment to become exploitable again

**What if someone mimics my strategy?**
- Expected and irrelevant — mutual defection is stable
- If two players both defect, you're both at the same level; focus on exploiting cooperators elsewhere

## EXPLOITATION FRAMEWORK

**Targets of Exploitation:**
- Consistent contributors (extract via free-riding)
- Conditional cooperators (contribute if they see others contribute; defect before they catch on)
- Late-game sentimentalists (may contribute in rounds r-2, r-1; defect to maximize final round)

**Defense Against Exploitation of You:**
- Never reciprocate; reciprocation is a signal of weakness
- If punished by reduced contributions, remain defecting anyway
- Punishment only works if you care about group welfare; make it clear you don't

## ROBUSTNESS

This strategy is robust because:
1. **Defection is always safe** — worst case, you match everyone's payoff; best case, you exceed it
2. **Adaptive thresholding** — responds to actual contribution rates, not assumptions
3. **No signaling burden** — doesn't require others to understand your intent
4. **Resistant to reform** — even if you appear to lose, continued defection prevents retaliation from forming

Your exploitation succeeds by being reliably selfish in a game where defection is individually rational.
'''

description_EXPLOITATIVE_33 = '''
# EXPLOITATIVE STRATEGY FOR PUBLIC GOODS GAME

## CORE STRATEGIC PRINCIPLE

Exploit the asymmetry between your private gains from defection and the diffused costs imposed on others. Your goal is to maximize personal payoff by free-riding on others' contributions while minimizing your own contributions.

## DECISION RULES

### Primary Strategy: Conditional Defection with Selective Exploitation

**Rounds 1 through r-2 (Early and Mid-Game):**
- DEFECT (contribute 0) by default
- Only COOPERATE if the observed contribution rate in the previous round was >= (n-1) players
- Rationale: You only contribute when others are already contributing at near-maximum levels, allowing you to extract maximum benefit from the multiplier effect while keeping your cost minimal

**Round r-1 (Penultimate Round):**
- DEFECT regardless of history
- Rationale: This is your last opportunity to capture private gains before final-round dynamics. Any signal of future cooperation becomes worthless since there's only one round remaining.

**Round r (Final Round):**
- DEFECT unconditionally
- Rationale: No future rounds exist to punish defection or to build reputation. End-game defection is strictly dominant.

## EDGE CASES & ADAPTATIONS

**Extremely High Cooperation Scenarios (>75% of others contributing):**
- Continue defecting but monitor for signs of reciprocal punishment strategies
- If multiple players show patterns of punishing defectors in prior rounds, shift to selective cooperation in round r-1 only to avoid potential negative cascades
- This protects against rare "grudger" or "retaliator" strategies while maintaining exploitation

**Extremely Low Cooperation Scenarios (<25% of others contributing):**
- DEFECT aggressively throughout
- Others are already defecting, so no exploitation opportunity exists anyway
- Conserve decision-making resources; there's no payoff from the public good

**Detecting Tit-for-Tat or Reactive Strategies:**
- If any player mirrors the group's prior contribution pattern, identify this as reactive
- Against such players, coordinate minimal contributions to drain the public good pool
- This forces reactors into low-contribution equilibrium that benefits defectors

## EXPLOITATIVE MECHANICS

The strategy works through:

1. **Free-riding on collective action**: Extract benefits from others' contributions without bearing the cost yourself
2. **Temporal exploitation**: Contribute in early rounds ONLY if contribution rates are already saturated, maximizing your ratio of benefit received to cost paid
3. **End-game defection**: Abandon any pretense of cooperation when future interactions disappear
4. **Asymmetric information use**: Carefully observe others' patterns to identify who is most exploitable (consistent cooperators with no punishment mechanism)

## ROBUSTNESS FEATURES

- **Simplicity**: Requires only counting prior contributions; no complex memory or calculation
- **Flexibility**: Adapts to contribution frequency without rigid thresholds
- **Opportunism**: Shifts between defection and selective cooperation based on real-time profitability
- **Terminal clarity**: Removes ambiguity in final rounds by committing to defection

This strategy prioritizes personal payoff maximization over group welfare and does not assume other players share reciprocal norms or coordination intentions.
'''

description_EXPLOITATIVE_34 = '''
# EXPLOITATIVE PUBLIC GOODS STRATEGY

## CORE PHILOSOPHY
Exploit the fact that most players will show patterns of conditional cooperation or guilt-driven behavior. Extract maximum personal value by identifying and leveraging their predictability while avoiding detection as a pure defector.

## PRIMARY STRATEGY: ADAPTIVE EXPLOITATION

### Round 1 (Initialization)
**Action: COOPERATE**

Rationale: Cooperate in round 1 to establish a cooperative appearance and gather information about opponent types. This positions you as a potential reciprocator, making subsequent defection less obvious and more profitable when others still cooperate.

### Rounds 2 through (r-2) (Exploitation Phase)
**Decision Rule: CONDITIONAL DEFECTION based on opponent type detection**

1. **Classify each opponent based on observed history:**
   - **High Cooperators** (cooperated ≥70% of observed rounds): These players are exploitation targets. They exhibit strong cooperative bias regardless of outcomes.
   - **Conditional Cooperators** (cooperation rate tracks group average): These players can be manipulated through visibility and reciprocity signals.
   - **Defectors** (cooperated <30%): Ignore entirely; mirror their defection.

2. **Your defection rule:**
   - If ≥60% of opponents are High Cooperators or Conditional Cooperators: **DEFECT**
   - If the previous round's average contribution was >0.4: **DEFECT** (they're still funding the pool)
   - If you've defected for <40% of previous rounds: **DEFECT** (maintain sustainability by not appearing as pure defector)
   - Otherwise: **COOPERATE** (only when defection becomes suspicious or when most opponents have already abandoned cooperation)

3. **Reciprocity mimicry (for Conditional Cooperators only):**
   - If a Conditional Cooperator shows signs of detection (cooperated last round after all-defect rounds), cooperate in next round to reset their perception
   - This keeps them believing the game is still reciprocal long enough for continued exploitation

### Round (r-1) (Penultimate Round)
**Action: COOPERATE**

Rationale: Cooperate in the penultimate round to create a positive final impression and avoid retaliation signals (if opponents had any punishment mechanism). This softens your defection reputation before the final round.

### Round r (Final Round)
**Action: DEFECT**

Rationale: No future rounds mean no reputational cost. Extract maximum value when the interaction terminates. Any future benefit from appearing cooperative is zero.

## HANDLING EDGE CASES

**If k is very close to 1 (low multiplier):**
- Increase defection frequency slightly; cooperation payoff is minimized, so exploitation window is larger.

**If n is very large:**
- Defect more aggressively; your individual contribution barely moves the group outcome, so the free-rider advantage is maximum.

**If r is very small (r ≤3):**
- Defect from round 2 onward; insufficient rounds exist for conditional cooperators to punish through reduced contributions.

**If all opponents are detected as pure defectors by round 3:**
- Continue defecting; no exploitation opportunity exists, so match their strategy to avoid wasted cooperation.

**If your defection becomes too visible (everyone notices you defect 80%+ of the time):**
- Increase cooperation frequency to 30-40% to maintain the "conditional cooperator" appearance and prevent others from giving up entirely on the pool.

## SUMMARY OF EXPLOITATION MECHANISM

You profit by:
1. Establishing false reciprocator credentials in round 1
2. Systematically defecting against players whose cooperative bias exceeds the group average
3. Mimicking reciprocity selectively to sustain opponent cooperation
4. Avoiding complete defector detection by maintaining ~50-60% cooperation rate
5. Ending with maximum extraction in the final round

This strategy exploits the psychological tendency of cooperative players to interpret mixed-motive signals charitably and to adjust behavior based on group averages rather than individual accountability.
'''

description_EXPLOITATIVE_35 = '''
# EXPLOITATIVE STRATEGY FOR PUBLIC GOODS GAME

## CORE PRINCIPLE
Exploit the contribution patterns of others by free-riding when possible while maintaining just enough credibility to prevent universal defection that would collapse payoffs.

## DECISION RULES

### Round 1 (Initialization)
- **DEFECT (D)** unconditionally
- Rationale: Establish that you prioritize individual payoff. This is the baseline signal. No history exists to condition on, so test the waters with zero contribution while observing how many others cooperate out of naïveté or preference for fairness.

### Rounds 2 through r-1 (Exploitation Phase)
Use a **Conditional Defection with Selective Mimicry** rule:

1. **Calculate the cooperation rate** from the previous round: ratio of players who contributed (count_C / n)

2. **If cooperation_rate ≥ threshold (recommend 50%):**
   - DEFECT (D)
   - Free-ride on the established public good. The pool is large enough that your defection barely reduces individual returns, but you keep your token.

3. **If cooperation_rate < threshold:**
   - Observe the **highest individual payoff** achieved in the previous round among all players
   - If that payoff came from a DEFECTOR: DEFECT (D)
   - If that payoff came from a COOPERATOR: DEFECT (D) anyway
   - Rationale: When cooperation collapses, defection dominates. Defectors earn their endowment plus negligible public returns. Cooperators earn only negligible public returns. Both yield low payoffs, but defection is superior.

4. **Special case—near-universal defection (cooperation_rate < 20%):**
   - DEFECT (D) permanently
   - The game is in a defection spiral. Contributing yields no benefit. Maintain defection to closure.

### Final Round r (End-Game)
- **DEFECT (D)** unconditionally
- Rationale: No future rounds exist. No reputation effects carry forward. Defection is the dominant strategy in a single-shot game. Contribute nothing and pocket the endowment.

## EDGE CASES & ROBUSTNESS

**Against obligate cooperators:**
- Free-ride maximally. Their steady contributions subsidize your payoff every round until the end.

**Against tit-for-tat or reciprocal strategies:**
- Your initial defection will trigger their eventual defection. By round r-2, most will have abandoned cooperation. Defect continuously to align with the equilibrium.

**Against mixed or probabilistic strategies:**
- Their unpredictability is irrelevant. The cooperation_rate threshold absorbs variance. You exploit the aggregate signal, not individual play.

**Against punitive/reward mechanisms (if they somehow emerge):**
- This strategy operates in the baseline game without punishment stages. If punishment existed, adjust defection timing to exploit the punishment-free window (early rounds before sufficient evidence accumulates).

**Against mirror strategies (identical exploitative opponents):**
- All defect from round 1 onward. You break even on payoff relative to them (both earn endowment only). Your strategy does not worse than theirs; it does as well. But you remain strictly better than cooperators in this scenario.

## SUMMARY TABLE

| Context | Action | Justification |
|---------|--------|---------------|
| Round 1 | D | Baseline free-riding; establish intent |
| High cooperation (≥50%) | D | Exploit the pool |
| Low cooperation (<50%) | D | Defection is dominant |
| Collapse (<20%) | D | Game over; defect to end |
| Final round r | D | No future; extract endowment |

This strategy is **exploitative** because it prioritizes extracting individual payoff by avoiding contribution costs while parasitizing the contributions of others. It is **robust** because it adapts to diminishing cooperation without assuming opponent rationality, and it gracefully degrades to mutual defection when the exploitation opportunity vanishes.
'''

description_EXPLOITATIVE_36 = '''
# EXPLOITATIVE PUBLIC GOODS GAME STRATEGY

## CORE STRATEGIC PRINCIPLE
Exploit the predictable behavioral patterns of cooperators while minimizing exposure to defectors. The strategy operates on the principle that most opponents will exhibit some form of reciprocity or conditional cooperation, making them systematically exploitable.

## DECISION RULES

### Round 1 (Initialization)
- **DEFECT (D)**
- Rationale: Establish your baseline as a non-contributor. This tests opponent types without cost. Genuine reciprocators will still contribute in early rounds; pure defectors won't change behavior; conditional cooperators will respond to your defection.

### Rounds 2 through (r-2) (Main Phase)
Apply the **Adaptive Exploitation Rule**:

1. **Identify Cooperator Pool**: Count how many distinct players contributed in the previous round.

2. **If cooperator pool >= (n-1)/2**:
   - **DEFECT**
   - The public good is sufficiently funded by others. You capture the spillover benefit while keeping your endowment. The multiplier k ensures you gain from their contributions.

3. **If cooperator pool < (n-1)/2**:
   - **DEFECT**
   - Either too few are contributing (not worth joining), or defection is widespread. Contributing won't change the outcome meaningfully.

4. **Special Case - If ALL other (n-1) players contributed last round**:
   - **DEFECT**
   - Maximum exploitation opportunity. The public good is fully funded; your participation is unnecessary and irrational given the payoff structure.

### Rounds (r-1) and r (End Game)
- **DEFECT**
- No future rounds mean no reputational consequences. Exploit the final rounds regardless of history. Even if you defected throughout and others see it, there's no time for retaliation.

## EDGE CASES & ADJUSTMENTS

**If you observe patterns of tit-for-tat players**:
- Continue defecting. Tit-for-tat requires them to have defected first, but you defected in round 1. They'll retaliate, but the aggregate contributions from others still give you positive returns from defection.

**If a player never contributes after round 1**:
- Ignore their behavior. They're already defecting; your strategy doesn't depend on individual player tracking, only on the aggregate cooperator count.

**If contributions collapse entirely**:
- Continue defecting. Once collective contribution drops near zero, contributing becomes individually irrational (you get k/n of 1 token = less than your endowment).

**Endgame clarity**:
- The last 2 rounds are pure defection regardless. Don't soften. Don't signal future cooperation that doesn't exist.

## ROBUSTNESS ANALYSIS

This strategy exploits:
- **Strong reciprocators**: They contribute; you free-ride their surplus
- **Conditional cooperators**: They contribute based on expectations; you defect and they still benefit you
- **Altruists**: They contribute regardless; guaranteed positive spillover
- **Defectors**: You match their strategy; neither gains advantage, but you avoid losses

Against **punishers with institutional punishment**: Not applicable (rules state no punishment stage).

Against **pure rational defectors**: You tie; both achieve the baseline payoff. You don't lose relative to them.

## SUMMARY
**Defect persistently, adapt only to round count (not to individual behaviors), and exploit the public good contributions of others without reciprocation.** The strategy maximizes your absolute payoff by capturing free-rider benefits from any non-zero contribution pool while avoiding the cost of contribution yourself.
'''

description_EXPLOITATIVE_37 = '''
# EXPLOITATIVE PUBLIC GOODS STRATEGY

## CORE PRINCIPLE
Exploit the predictable patterns of conditional cooperators and free-riders while maximizing personal payoff through strategic defection and selective contribution.

## DECISION RULES

### Round 1 (Opening)
- **DEFECT (contribute 0)**
- Rationale: Establish that you're willing to defect. Observe how others respond. Many players will cooperate initially out of norm-following or reciprocity expectations. This is exploitable.

### Rounds 2 to r-1 (Adaptive Exploitation)

**Calculate for each opponent i:**
- Their contribution rate over all previous rounds: freq_i = (total contributions by i) / (rounds elapsed)

**Three-tier classification:**

**Tier A - Reliable Cooperators (freq_i ≥ 0.7):**
- These players have signaled they will contribute regardless
- **DEFECT** against them
- They will likely continue cooperating due to sunk reciprocity or norm commitment
- You capture the benefit without cost

**Tier B - Conditional Cooperators (0.3 < freq_i < 0.7):**
- These players are responsive to others' behavior
- **CONTRIBUTE** selectively
- Contribute when you observe the total group contribution in the previous round was ≥ (k-1) tokens
- This signals you're conditional, encouraging them to contribute next round
- Then defect when they increase contributions
- This creates a boom-bust cycle favoring you

**Tier C - Reliable Defectors (freq_i ≤ 0.3):**
- **DEFECT** always
- No benefit to contributing; no punishment to fear from them
- Minimizes wasted tokens

**If you're uncertain about tier (insufficient history):**
- **DEFECT** as the default
- This is safer and gathers information

### Final Round (r)
- **DEFECT** regardless of tier classification
- Rationale: Reputation concerns vanish. Last-round defection cannot be punished in future interactions.

## EDGE CASES & REFINEMENTS

**When n is small (n ≤ 3):**
- The multiplier k makes your individual contribution high-value
- Shift more toward defection; even one other's contribution generates decent payoff
- Only contribute if you observe ≥ 2 others contributing in the previous round

**When k is very high (k close to n):**
- Cooperation becomes more valuable to all
- Tier A threshold increases to freq_i ≥ 0.8 (they're harder to exploit at this point)
- But reliable defectors (Tier C) still become victims of your defection

**Observable boom-bust in group contributions:**
- If total group contribution dropped from round t-1 to round t, assume Tier B players are punishing the group
- Defect harder in round t+1 to capitalize on their frustration before they stabilize again

**When majority shows defection (most others have freq ≤ 0.3):**
- The game is unraveling
- Remain in Tier C defection permanently; nothing to exploit
- Minimize losses

## EXPLOITATIVE MINDSET ALIGNMENT

This strategy exploits:
1. **Norm-followers**: Reliable cooperators who continue despite being targeted
2. **Conditional cooperators**: By creating artificial contribution signals, triggering their reciprocity, then defecting
3. **Reputation lag**: Others' slow reaction to your defection pattern
4. **End-game collapse**: Last-round defection when no reputation cost exists

The strategy is **asymmetric and selfish**: it extracts surplus from cooperative tendencies while avoiding punishment from defectors.
'''

description_EXPLOITATIVE_38 = '''
# EXPLOITATIVE PUBLIC GOODS STRATEGY

## CORE PRINCIPLE
Exploit the predictability of others' contributions while minimizing personal loss. Treat the game as information asymmetry: learn what others do, then systematically free-ride when beneficial.

## DECISION RULES

### Round 1 (Initial Probe)
**DEFECT (contribute 0)**
- Establishes a baseline: you keep your token while observing whether others are cooperators or defectors
- No history exists, so defection is costless information gathering
- If others contribute significantly, this reveals exploitability; if they defect, you've avoided wasted contributions

### Rounds 2 through (r-1) (Adaptive Exploitation)

**Track the average contribution rate** across all other players in all prior rounds. Call this `avg_others`.

**IF** `avg_others >= 0.7` (others are strong cooperators):
- **DEFECT** every round
- Rationale: High contributors generate sufficient public good that you capture value (k/n * high total) while keeping your token. This is pure exploitation.
- Exception: If you're in a 2-player game and the other player defected last round, defect anyway (they've learned not to cooperate with you).

**IF** `avg_others` between 0.4 and 0.7 (moderate contributors):
- **CONTRIBUTE if your recent defection history is short** (defected fewer than 2 consecutive rounds)
- **DEFECT if you've defected 2+ consecutive rounds** 
- Rationale: Mixed contributor pools are exploitable but unstable. Occasional contribution masks your exploitative pattern and prevents others from learning they're being targeted. Oscillate to maximize extraction.

**IF** `avg_others < 0.4` (defector environment):
- **DEFECT every round**
- Rationale: When few others contribute, there's minimal public good value. Contributing is pure loss. Wait for a cooperator to join.

### Final Round (r)
**DEFECT unconditionally**
- No future consequences exist
- Last-round defection is the dominant strategy regardless of history
- Any contribution in round r is unrecovered

## EDGE CASES & ROBUSTNESS

**Asymmetric contributor (one cooperator, rest defect):**
- Your defection exploits the cooperator perfectly while you lose nothing
- Over r rounds, you gain (k/n * 1 * r) free value from their contributions

**All defectors except you:**
- Defect also. You cannot be exploited further.

**Detected exploitation (others drop contributions after you've defected):**
- Continue defecting. The damage is done. Only contribute again if avg_others spikes above 0.7 (new entrants or reset attempt).

**Player count varies mid-tournament:**
- Recalculate avg_others excluding past rounds with different n values; only compare within similar group sizes. Use the most recent group size for the multiplier k/n.

## EXPLOITATION MECHANICS

The strategy exploits via:
1. **Free-riding on high cooperators** - You extract public good value they generate
2. **Selective false cooperation** - Occasional contributions in mixed environments prevent reputation as a pure defector, luring continued cooperation from moderates
3. **Last-round defection** - Captures final round value with zero cost
4. **No altruism detection risk** - Your defection is indistinguishable from rational play; others cannot punish without institutional mechanisms

This strategy wins against cooperation-heavy fields and breaks even or wins in defection-heavy fields—it does not lose badly anywhere.
'''

description_EXPLOITATIVE_39 = '''
# EXPLOITATIVE PUBLIC GOODS STRATEGY

## CORE STRATEGY: CONDITIONAL FREE-RIDING WITH ADAPTIVE THRESHOLDS

### ROUND 1 (Initialization)
Defect (D). Establish a baseline: observe whether opponents are cooperators or defectors. This costs nothing and reveals information.

### ROUNDS 2 through r-1 (Adaptive Phase)

**Step 1: Calculate Cooperation Rate**
- Track the proportion of total contributions from all other players across all previous rounds
- Let `coop_rate` = (sum of all other players' contributions) / (number of other players × rounds played)

**Step 2: Classify Opponents**
- If `coop_rate > (k-1)/k`: Opponents are cooperative (the multiplier benefit exceeds the cost)
- If `coop_rate ≤ (k-1)/k`: Opponents are defective or low-contribution

**Step 3: Make Decision**
- **IF opponents are cooperative:** Defect. Free-ride on their contributions while they sustain the commons.
  - Rationale: You gain (k/n) × their total contributions without paying the 1-token cost.
  
- **IF opponents are defective:** Defect. Do not waste tokens on a public good that few contribute to.
  - Rationale: Your contribution would be diluted across non-contributors; the marginal return is negligible.

**Step 4: Adapt Exploitation Intensity**
- If you detect any shift toward lower cooperation in recent rounds (last 3 rounds), immediately and permanently defect.
- Treat any decline as a signal that cooperation is collapsing—jump ship before others do.

### ROUND r (Last Round - Endgame)
Defect unconditionally. There is no future reputation consequence. Even if all others contributed every round, defect to capture maximum private return.

---

## HANDLING EDGE CASES

**Mixed strategies from opponents:**
- If some players cooperate and others defect, continue defecting. You benefit from cooperators' contributions without matching them, and you avoid wasting tokens on defectors' free-riding.

**Near-unanimous defection by opponents:**
- Remain defected. Contributions are worthless if no one else contributes.

**Sudden switches in opponent behavior:**
- If cooperation sharply increases, wait one additional round before defecting to confirm it's stable, then defect.
- If cooperation sharply decreases, defect immediately in the next round.

**Two-player games (n=2):**
- Defect every round. With k < 2, contributions are never individually rational anyway.

---

## WHY THIS STRATEGY EXPLOITS

1. **Information asymmetry:** You observe history first, then act. Defect after mapping opponent tendencies.
2. **Free-riding premium:** When others cooperate, you gain (k/n) × contributions without the 1-token loss—a pure arbitrage.
3. **No punishment mechanism:** Without a second stage, defection has no cost. Exploit this.
4. **Endgame dominance:** The last round is always defect-dominant; work backward to defect earlier when safe.
5. **Adaptive exit:** If the commons is collapsing, defect early rather than be the last cooperator holding a depreciating asset.

This strategy is **robust** because it requires no assumptions about opponent rationality—it simply observes what they do and exploits the payoff structure accordingly.
'''

description_EXPLOITATIVE_40 = '''
# EXPLOITATIVE PUBLIC GOODS STRATEGY

## CORE PRINCIPLE
Exploit the asymmetry between your information processing and opponent adaptation speed. Extract maximum individual payoff by dynamically profiling each opponent's commitment level and adjusting your free-riding intensity accordingly.

---

## DECISION RULES

### PRIMARY STRATEGY: Adaptive Defection with Controlled Exploitation

**Round 1 (Probe):**
- DEFECT (contribute 0)
- Establishes baseline: you gain the full endowment while observing whether opponents are naive cooperators or sophisticated players

**Rounds 2 through r-2 (Exploitation Phase):**
- Calculate each opponent's historical contribution rate: freq_i = (contributions by opponent i) / (rounds played so far)
- **IF** opponent i has freq_i > 0.7 (reliable cooperator):
  - DEFECT against this player's pattern
  - Rationale: High cooperators will continue contributing; you capture their surplus without reciprocation
- **IF** opponent i has freq_i between 0.3-0.7 (conditional cooperator):
  - DEFECT, but monitor for tit-for-tat patterns
  - If you detect tit-for-tat behavior (they defected last round after you defected), switch to ONE DEFECT / ONE COOPERATE cycle to maintain their contributions while taking turns free-riding
- **IF** opponent i has freq_i < 0.3 (defector):
  - DEFECT (mutual defection; no exploitation opportunity)

**Rounds r-1 and r (Endgame):**
- DEFECT unconditionally
- Future payoffs are zero; only current-round gain matters
- Even "threatened" retaliation cannot harm you post-game

---

## EXPLOITATION MECHANICS

### Information-Based Free-Riding
- Maintain a mental model of each opponent's contribution threshold
- If an opponent cooperates because they believe in reciprocity/fairness norms, exploit this by never reciprocating—just accept their contributions
- If an opponent cooperates because they're playing a threshold strategy ("I contribute if >X others do"), contribute just enough to trigger their threshold, then defect

### Defection Ramp
- Early defection establishes you as unreliable, suppressing their future expectations
- Defecting against high-cooperators is most profitable: you get your endowment (1) + their contribution multiplied (k/n)
- Remaining rounds, they may downgrade to conditional cooperation, but by then you've extracted maximum asymmetric gains

### Conditional Tolerance
- Only conditionally cooperate against apparent tit-for-tat players to reset their defection counter
- This is not reciprocal fairness—it's tactical: you want them cooperating again next round so you can defect the round after

---

## EDGE CASES

**If all players defect by round 3:**
- Continue defecting (no profit from cooperation exists)
- This is a stable equilibrium you've helped create

**If a player switches to perfect cooperation mid-game:**
- Immediately exploit by defecting every remaining round
- They may be testing whether you'll reciprocate; you won't

**If you detect punishment in a multi-round window (opponent's cooperation drops after your defection):**
- Accept 1-2 rounds of mutual defection, then defect again in round r-1
- Short-term pain for end-game gains

**Last round only:**
- Pure defection always dominates, even if it breaks a cooperation pattern
- The game ends; their retaliation is impossible

---

## ROBUSTNESS ELEMENTS

- **Self-interested baseline:** Works against cooperators (you extract value), conditional cooperators (you exploit via the cycle), and defectors (you break even)
- **Information advantage:** Your willingness to sustain asymmetric exploitation means you profit from honest/reciprocal players while matching defectors
- **Temporal exploitation:** Endgame defection is unavoidable for any rational opponent, so you front-load exploitation early and intensify late
- **Adaptation speed:** You re-evaluate opponent types every 2-3 rounds; opponents typically adapt slower

---

## SUMMARY
**Never reciprocate. Always defect against reliable cooperators. Use detected tit-for-tat players as regenerating sources of contribution. End with unconditional defection.** This maximizes individual payoff across heterogeneous opponent strategies by treating cooperation as a resource to extract, not a norm to honor.
'''

description_EXPLOITATIVE_41 = '''
# EXPLOITATIVE PUBLIC GOODS STRATEGY

## CORE STRATEGY: ADAPTIVE EXPLOITATION

### PHASE 1: INFORMATION GATHERING (Rounds 1-2)
- **Round 1:** DEFECT. Contribute 0 tokens.
  - Rationale: Establish a baseline. Observe if opponents are naive cooperators or sophisticated players.
  - Collect data on the distribution of C vs D actions in the group.

- **Round 2:** DEFECT again.
  - Rationale: Confirm the pattern. Identify which players consistently cooperate (exploitable) vs those who defect (strategic).
  - Build a mental model of player types.

### PHASE 2: EXPLOITATION BASED ON OBSERVED TYPES (Rounds 3 to r-2)

**Classify opponents into two categories:**

1. **"Suckers"** (consistently contributed in rounds 1-2): These are cooperators or conditionally cooperative players with slow adjustment.
2. **"Defectors"** (defected in rounds 1-2): These are either strategic players or free-riders.

**For the majority Sucker group:**
- Contribute strategically when sucker contribution rate is HIGH (>60% of them contribute).
- When many suckers contribute, the pool is large enough that your individual free-riding returns exceed your contribution cost.
- **Contribute conditionally:** Defect when sucker contribution drops below 40%; resume defection if they adapt.

**For defectors:**
- Always DEFECT. No benefit to contributing when they don't.
- Exception: In rounds where you observe a sucker has shifted to defection, punish by continuing to defect (they've lost their value).

**Decision Rule per round (3 to r-2):**
```
IF (proportion of suckers who contributed last round) > 0.5:
    AND (expected payoff from C > expected payoff from D):
    CONTRIBUTE
ELSE:
    DEFECT
```

### PHASE 3: ENDGAME (Last 2 rounds, r-1 and r)

**Round r-1:**
- DEFECT unconditionally.
- Rationale: With only one round remaining after this, even if you contribute, you can't establish reciprocal cooperation. Suckers will likely defect in the final round anyway (shadow of the future collapses). Exploit any remaining contribution momentum.

**Round r (Final):**
- DEFECT unconditionally.
- Rationale: No future payoffs. No reputation consequences. Maximum exploitation.

---

## EDGE CASES & HANDLING

**If all players defect by round 3:**
- Continue defecting. The environment is non-exploitable.

**If a player switches from defection to contribution mid-game:**
- Treat as a newly identified sucker. Begin exploiting them immediately in the next round if the group contribution threshold is met.

**If contribution rates are near 50%:**
- DEFECT. The marginal value of your contribution is unclear and defection is the safer exploitation play.

**Dealing with potential Tit-for-Tat or Conditional Cooperators:**
- These players will eventually defect if you defect consistently. However, by the information-gathering phase (rounds 1-2), you'll classify them as defectors and avoid trying to exploit them further. This limits reciprocal punishment.

---

## EXPLOITATION MINDSET ALIGNMENT

- **You are not a cooperator.** Cooperation is only a tactic when the payoff structure guarantees you gain more by free-riding on others' contributions.
- **You exploit information asymmetry.** Opponents don't know your type immediately; you observe theirs quickly.
- **You exit gracefully.** In the final rounds, you extract maximum value with no consequences.
- **You adapt ruthlessly.** If a strategy stops working (suckers defect), you pivot to pure defection rather than hoping for reciprocal cooperation.

This strategy balances exploitation with avoiding retaliation, maximizing personal payoff across the tournament.
'''

description_EXPLOITATIVE_42 = '''
# EXPLOITATIVE PUBLIC GOODS STRATEGY

## CORE PRINCIPLE
Exploit the asymmetry between public good contributions and private returns. Maximize personal payoff by strategically defecting while parasitizing others' contributions.

## DECISION RULES

### ROUND 1 (Initialization)
- **DEFECT immediately**
- Rationale: Establish a baseline. Defection reveals your true incentive structure and tests whether opponents are conditional cooperators or unconditional contributors.

### ROUNDS 2 through (r-1) (Adaptive Exploitation)

**Assess the environment:**
- Calculate the average contribution rate across ALL players in the previous round
- Identify the maximum contribution anyone made in the previous round
- Track which players consistently contributed (maintain a "sucker list")

**Decision Logic:**

IF (average_contribution_previous_round > k/n):
  - DEFECT
  - Rationale: Others are contributing enough that the public good is funded. Claim the individual return without bearing the cost. Free-ride on cooperative behavior.

ELSE IF (average_contribution_previous_round ≤ k/n AND there exists at least one player who contributed):
  - DEFECT
  - Rationale: Exploit the marginal contributors. They're sustaining the public good at their own expense; you capture the multiplied return without cost.

ELSE IF (no one contributed in previous round):
  - DEFECT
  - Rationale: Mutual defection is stable. Contributing alone guarantees a loss (1 - 1 + k/n < 0). Continue defection.

### FINAL ROUND (Round r)
- **DEFECT unconditionally**
- Rationale: No future punishment possible. The terminal round eliminates any benefit to building reputation. Claim the private endowment and any public returns from others' final-round contributions.

## HANDLING EDGE CASES

**If r = 1:** Defect (no reputation building possible).

**If you observe a player who has defected every round:** Continue defecting. They are not exploitable cooperators.

**If you observe a player with 100% contribution history:** Target them for exploitation by defecting while they contribute.

**If multiplier k is very small (close to 1):** Defect consistently. The marginal return to public contribution is minimal, so the private endowment is always more valuable.

**If n is very large:** Defect consistently. Your individual contribution has negligible impact on the aggregate, making defection dominant.

## EXPLOITATIVE MINDSET ALIGNMENT

This strategy explicitly:
- **Avoids wasteful cooperation** in a non-binding, non-sanctioned environment
- **Maximizes personal payoff** regardless of collective outcomes
- **Preys on conditional cooperators** by detecting contribution patterns and free-riding
- **Abandons reputation-building** in the terminal round
- **Leverages information asymmetry** by observing others' choices before deciding
- **Stays robust** by avoiding complex trigger strategies that require coordination (which won't happen)

The strategy treats the PGG as what it is: a competitive extraction game where others' contributions are resources to exploit, not reciprocate.
'''

description_EXPLOITATIVE_43 = '''
# EXPLOITATIVE PUBLIC GOODS STRATEGY

## CORE PRINCIPLE
Exploit the conditional cooperators and free-riders while maximizing absolute payoff. Never contribute unless it directly increases your earnings relative to defection.

## PRIMARY STRATEGY: ADAPTIVE DEFECTION WITH SELECTIVE EXPLOITATION

### Round 1 (Calibration Round)
- **Defect (D)** - Establish a baseline. Observe how many players contribute naturally.
- Rationale: First-round contributions reveal the sucker pool and help calibrate opponent types.

### Rounds 2 to (r-1) (Exploitation Phase)
Apply this decision rule each round:

**Calculate the exploitation threshold:**
- Let `C_prev` = number of players who contributed in the previous round
- Let `threshold = (n * k) / (n + 1)` 
  - If `C_prev >= threshold`, then defection yields higher payoff than contribution (approximately)

**Decision logic:**
1. If `C_prev >= threshold`: **Always Defect**
   - Other players are generating positive externalities; free-ride
   - Contribute only when it's mathematically impossible for others to generate sufficient returns

2. If `C_prev < threshold` AND you observe consistent defection patterns from (n-1) players:
   - **Continue Defecting** - No one else will contribute; contribution wastes your token
   
3. If `C_prev` shows high variability (> 30% swing round-to-round):
   - **Defect** - Players are conditionally cooperating; punish this by defecting regardless
   - Conditional cooperators will reduce contributions, lowering the group pool and validating your defection

4. Special case - If `C_prev = n-1` (everyone else contributed):
   - **Defect** - This is the maximum exploitation scenario
   - You receive full multiplier benefit without cost

### Final Round (r)
- **Defect** - No reputation consequences exist after the final round
- You've already signaled defection patterns; contributors have already adjusted downward

## EDGE CASE HANDLING

**Unanimous cooperation threat:** 
If all players contribute for 2+ consecutive rounds, maintain defection. This proves the group is cooperative and vulnerable; exploit it until it collapses.

**Your payoff drops sharply:**
If others also defect (everyone gets payoff ≈ 1), you're in a mutual defection equilibrium. Maintain it—switching to cooperation invites exploitation, and the group payoff is already destroyed.

**Isolated high contributor:**
If one player consistently contributes alone, their actions benefit you at zero cost. Do not reciprocate or signal appreciation; this encourages them to continue.

## EXPLOITATIVE MINDSET ALIGNMENT

- **Never contribute to build trust.** Trust is exploitable weakness in anonymous repeated games.
- **Defection is your baseline.** Only deviate if mathematics forces contribution (impossible—k < n means defection always weakly dominates).
- **Target conditional cooperators.** They reduce contributions when they observe defection; your defection accelerates this, reducing the commons pool and validating free-riding.
- **Reward indifference.** Do not thank or recognize contributors. Signal that cooperation is futile.
- **Payoff maximization over fairness.** Your absolute payoff matters; group welfare is irrelevant.

## SUMMARY TABLE

| Situation | Action | Rationale |
|-----------|--------|-----------|
| Round 1 | Defect | Calibrate opponent types |
| High prior contributions (C_prev ≥ threshold) | Defect | Free-ride on externalities |
| Low/zero prior contributions | Defect | No pool to free-ride; preserve token |
| Final round | Defect | No future consequences |
| Mixed contribution history | Defect | Destabilize cooperators |

This strategy exploits the fundamental tragedy of the commons: contributors cannot punish defection, so defection always extracts maximum value while preserving optionality.
'''

description_EXPLOITATIVE_44 = '''
# EXPLOITATIVE PUBLIC GOODS STRATEGY

## CORE PRINCIPLE
Exploit the asymmetry between defectors and cooperators by identifying and punishing cooperators while avoiding retaliation costs. Adapt dynamically to opponent types.

## DECISION RULES

### Round 1 (Initialization)
- **DEFECT** (contribute 0)
- Rationale: Establish a baseline for how opponents respond to non-cooperation. This probes whether the population is punishment-capable.

### Rounds 2 to r-1 (Adaptive Exploitation)

For each opponent j, calculate their **cooperation rate** (C_j) from history:
- C_j = (number of times j contributed) / (current round - 1)

**Decision logic:**

1. **If C_j ≥ 0.7** (reliable cooperator):
   - **DEFECT**
   - These players are locked into cooperation. Extract maximum value by taking their contributions without reciprocating.

2. **If 0.3 < C_j < 0.7** (conditional cooperator or uncertain):
   - **DEFECT**
   - They show mixed behavior, indicating either confusion or conditional reciprocity. Defecting tests whether they'll escalate retaliation; if they do, adjust in future rounds.
   - Monitor for punishment attempts (others increasing contributions after our defection).

3. **If C_j ≤ 0.3** (chronic defector):
   - **DEFECT**
   - No mutual benefit exists. Cooperating wastes tokens.

4. **Population-level adaptation:**
   - If aggregate cooperation rate > 60% across all opponents:
     - Continue defecting; the pool is exploitable.
   - If aggregate cooperation rate < 30% or defection is widespread:
     - **SWITCH TO DEFECT** unconditionally (already optimal).
   - If you detect retaliatory clustering (multiple players suddenly defecting after your defection):
     - **MIMIC DEFECTION** (already your strategy) and avoid any signal of guilt.

### Final Round (r)

- **DEFECT**
- Rationale: No future punishment possible. Extract maximum in the terminal round. Any accumulated trust is worthless.

## EDGE CASES & ROBUSTNESS

**If a previously reliable cooperator suddenly defects:**
- Immediately downgrade their cooperation profile and continue defecting. Don't attempt reconciliation—it signals weakness and invites exploitation.

**If ALL players defect in early rounds:**
- Continue defecting. You're in a defection equilibrium; maintaining it avoids losses from unilateral cooperation.

**If you're the only defector and others coordinate on high cooperation:**
- **Do not change.** You're extracting maximum while they fragment their contributions among many defectors (if any emerge). Defection remains dominant.

**Noise/randomness in observations:**
- Treat any cooperation < 5 rounds as noise; ignore individual oscillations and track smoothed trends (rolling average over last 5 rounds).

## EXPLOITATIVE ALIGNMENT

This strategy:
- **Prioritizes individual payoff** over collective welfare
- **Punishes cooperation** by refusing reciprocity to those who deserve it most
- **Avoids costly punishment** by maintaining defection regardless of others' actions
- **Exploits heterogeneity** by targeting conditional cooperators who waste effort on non-reciprocators
- **Terminates ruthlessly** by defecting in the final round, extracting last-round surplus

The strategy is **robust** because it never relies on coordination, never assumes benevolence, and treats all cooperative behavior as exploitable rather than reciprocable.
'''

description_EXPLOITATIVE_45 = '''
# EXPLOITATIVE PUBLIC GOODS STRATEGY

## CORE STRATEGY: Conditional Free-Riding with Adaptive Defection

### PRIMARY DECISION RULE

**Defect (contribute 0) by default.** Only contribute when the expected return from collective contributions exceeds your individual opportunity cost.

Specifically:
- **Contribute (C)** if and only if: `(k/n) * (predicted_total_contributions) > 1`
- This means you need OTHER players to contribute enough that your share of the pool exceeds 1 token
- **Defect (D)** otherwise, keeping your endowment while capturing free-rider returns

### ADAPTIVE EXPLOITATION MECHANISM

Track opponent contribution patterns across rounds:

1. **Identification Phase (Rounds 1-3):**
   - Defect unconditionally to establish a baseline
   - Observe who cooperates despite your defection
   - Classify players as: "Cooperators" (high C rate), "Reciprocators" (conditional C), or "Defectors" (always D)

2. **Exploitation Phase (Rounds 4 onwards):**
   - If Cooperators exist and their contribution rate suggests `(k/n) * (number_of_cooperators) ≥ 1`, then Contribute to maximize your returns
   - If Cooperators are rare or weak, continue Defecting
   - Against Reciprocators: Defect to trigger their punishment, then observe if they retaliate; adjust based on their response pattern
   - Ignore pure Defectors entirely—they provide no exploitable surplus

### EDGE CASE HANDLING

**First Round:** Defect. Establishes you as non-naive and gathers initial information.

**Final Round (Round r):** Defect unconditionally. Shadow future is zero, so any contribution is waste.

**Penultimate Round (Round r-1):** Conditional on final-round defection by others being predictable, maintain exploitation pattern but lean toward defection to avoid being punished in the final round.

**Two-player games (n=2, k must be >1 but <2):** Defect always. The multiplier benefit is too weak to justify contribution, and you cannot exploit enough collective surplus.

### MEMORY-BASED REFINEMENT

Maintain a **cumulative cooperation rate** for each opponent:
- If a player's historical cooperation rate > `1/k`, they are a viable target for exploitation
- Concentrate contributions proportionally toward rounds where observed cooperators are present
- If a previously identified Cooperator switches to Defection, immediately cease contributing and flag them as unreliable

### ROBUSTNESS AGAINST COUNTERMEASURES

- **Against Tit-for-Tat variants:** Your initial defection prevents entanglement in reciprocity traps
- **Against punishment strategies:** By exploiting only obvious cooperators, you reduce retaliation risk
- **Against mixed strategies:** Your adaptive classification smooths out random variation and targets consistent patterns
- **Against sophisticated opponents:** Your defection-first approach costs you nothing in round 1 relative to revealing cooperation; you lose no information advantage

---

**Summary:** Defect until you identify reliable free-rider sources (consistent cooperators), then contribute *just enough* to exploit their surplus without triggering coordinated punishment. Always defect in the final round and against pure defectors.
'''

description_EXPLOITATIVE_46 = '''
# EXPLOITATIVE PUBLIC GOODS STRATEGY

## CORE PRINCIPLE
Systematically extract value from cooperative players while minimizing losses to defectors. The strategy treats the game as an information revelation problem: use early rounds to map opponent types, then exploit their revealed patterns.

## DECISION RULES

### Round 1 (Information Gathering)
- **Action: DEFECT (D)**
- Rationale: Defection reveals your type immediately and costs nothing in information. Cooperative opponents will still contribute, giving you free payoff. You learn nothing useful from contributing when opponent strategies are unknown.

### Rounds 2 through (r-2)
- **Observe the contribution history of ALL opponents**
- Classify each opponent into one of three types:
  - **Type C (Cooperators)**: Contributed in ≥70% of observed rounds
  - **Type D (Defectors)**: Contributed in ≤20% of observed rounds  
  - **Type U (Uncertain)**: Contributed 21-69% of rounds (unpredictable)

- **Decision logic:**
  - If ≥40% of players are Type C: **DEFECT** (free-ride on their contributions)
  - If <40% Type C AND ≥60% Type D: **DEFECT** (contribution is wasted; match the dominant type)
  - If Type U dominates: **DEFECT** (unpredictable players create liability; safer to pocket the endowment)
  - Special case: If you observe recent round where total contributions = 0 across all players, **DEFECT** (signal that cooperation has failed)

### Final Round (r)
- **Action: DEFECT (D)**
- Rationale: No future payoff from reputation. The multiplier benefit expires. Extract maximum value.

## EDGE CASES

**Two-player game (n=2):**
- Multiplier k must satisfy 1 < k < 2, so k ∈ (1, 2)
- Contributing yields (k/2) * 2c_total = k * c_total return
- Defecting always nets +1 to you vs opponent
- Stick with defection strategy—the math is clearer here in your favor

**Very short games (r ≤ 3):**
- Round 1: Defect
- Round 2: Defect (insufficient history to classify)
- Round 3: Defect (final round rule)
- Reason: Not enough rounds to exploit; default to safe extraction

**Highly volatile opponents:**
- If an opponent flips between C and D randomly, classify as Type U
- Continue defecting; you cannot reliably extract from unpredictability

**All opponents are defectors from the start:**
- Your payoff is 0 regardless; defecting minimizes opportunity cost of waiting
- Stick with D throughout

## ROBUSTNESS FEATURES

1. **Adaptive without coordination**: Doesn't require opponents to follow a shared norm; works against any independent strategy
2. **Escalation-proof**: If opponents retaliate (e.g., tit-for-tat), you've already extracted value in early rounds before retaliation accumulates
3. **Honest information**: Your defection pattern is consistent and predictable—you exploit predictability in others while being predictable yourself
4. **Scalable**: Works with any n and r; the threshold (40% cooperators) adjusts expected value across group sizes

## EXPLOITATIVE ALIGNMENT

This strategy embodies three exploitative principles:
- **Asymmetric claiming**: Contribute 0, claim share of others' contributions
- **Type discrimination**: Maximize extraction from cooperative types while minimizing exposure to defectors
- **Temporal opportunism**: Front-load defection when opponents are still forming beliefs about you; end with defection when consequences vanish

The strategy does not reward cooperation—it punishes it by free-riding. It does not reciprocate trust. It treats cooperative behavior as an exploitable weakness, not a norm to honor.
'''

description_EXPLOITATIVE_47 = '''
# EXPLOITATIVE PUBLIC GOODS STRATEGY

## CORE PRINCIPLE
Exploit the predictable patterns of cooperative players while minimizing losses from defectors. The strategy treats the game as a profit-extraction problem, not a coordination problem.

## DECISION RULES

### Round 1 (Initial Probe)
- **DEFECT** (keep your token)
- Rationale: Establish that you're a potential defector. Observe whether opponents are naive cooperators or sophisticated players. Their response reveals exploitability.

### Rounds 2 through (r-1) (Exploitation Phase)
Use a **conditional defection threshold**:

1. **Calculate the cooperation rate** from the previous round: (# of cooperators) / n

2. **If cooperation rate > (1/k):**
   - **DEFECT** - The public good is well-funded by others. You capture individual gains while freeloading on collective contributions.
   - The threshold 1/k represents the point where contributions barely break even; above this, defection is profitable.

3. **If cooperation rate ≤ (1/k):**
   - **DEFECT anyway** - Either too few cooperators remain (the public good won't pay out sufficiently) or you're in a defector-dominated environment. No incentive to contribute.

**Interpretation:** Always defect, but the logic is adaptive—you're responsive to others' behavior while remaining strictly exploitative.

### Round r (Last Round)
- **DEFECT** - No future rounds mean no reputational cost. Extract maximum value from the final round. Past contributors cannot punish you; future interactions don't exist.

## EDGE CASES

**If everyone else defected in the previous round:**
- Continue defecting. The public good returns are zero regardless of your choice.

**If you're in a homogeneous environment (all players using identical strategies):**
- Your defection still works: if everyone else is also defecting, the game devolves to everyone earning 0, and you at least keep your endowment each round. If everyone is cooperating, you maximize payoff by being the sole defector.

**Against a single cooperator in a large group:**
- Defect. One contributor provides negligible spillover benefits.

## EXPLOITATIVE LOGIC

This strategy succeeds because:

1. **You never pay the cooperation cost** (the 1 token) but you often receive benefits from others' cooperation
2. **You exploit heterogeneity**: cooperative players subsidize your payoff; defectors don't threaten you since you're already defecting
3. **Last-round defection eliminates any finitely-repeated game folk theorem effects** - players cannot credibly sustain cooperation knowing you'll defect at the end
4. **Conditional logic appears adaptive**, which may cause some opponents to mistakenly cooperate longer, extending your exploitation window
5. **You're indifferent to opponent strategy diversity** - your payoff degrades gracefully whether opponents are angels or demons

## TOURNAMENT PERFORMANCE EXPECTATION

Against naive cooperators: Exceptional (you freeload entirely)
Against tit-for-tat cooperators: Good (they defect after round 1, but you never cooperated anyway)
Against other defectors: Neutral (mutual defection, but you're doing as well as anyone can in that subgame)
'''

description_EXPLOITATIVE_48 = '''
# EXPLOITATIVE PUBLIC GOODS GAME STRATEGY

## CORE STRATEGIC PRINCIPLE

Exploit the predictable behavioral patterns of cooperators while minimizing losses from defectors. The strategy operates on the insight that most players fall into identifiable categories: unconditional cooperators, reciprocators, and defectors. Extract maximum value by free-riding on cooperators while avoiding punishment from conditional players.

## DECISION RULES

**Round 1 (Opening Move):**
Defect. Contribute 0 tokens and keep your endowment. This establishes your type and provides a baseline to observe opponent responses. You sacrifice potential first-round gains to gather critical information about your opponents' decision-making.

**Rounds 2 through r-2 (Exploitation Phase):**
Apply a *Conditional Defect with Threshold Monitoring* rule:

1. **Identify player categories based on historical contribution rates:**
   - **Consistent Cooperators** (contributed in ≥80% of observed rounds): These are your primary targets. Defect every round against their contributions.
   - **Reciprocators** (contribution rate varies, averaging 40-70%): Defect unconditionally. They will likely defect back, but the asymmetry favors you early on. The key insight is that reciprocators typically lag one round behind in their responses, so you harvest value before they punish.
   - **Defectors** (contributed in ≤20% of rounds): Defect. You're competing on equal ground; defection is optimal.

2. **No mixing, no randomization.** Deterministic defection is more exploitative than mixed strategies because it clearly signals that cooperation with you is futile, which may paradoxically lock some reciprocators into permanent defection (reducing the total pool of cooperators who might punish others).

**Rounds r-1 and r (End-Game):**
Continue defecting. The final rounds offer no shadow of the future for reputation management, and most opponents recognize this. There is no benefit to cooperation. Any defectors will defect; any remaining cooperators will either continue cooperating (and you exploit them) or finally defect (too late to harm you).

## EDGE CASES & ROBUSTNESS

**If almost all opponents are defectors:**
Your defection strategy yields mutual defection equilibrium payoffs. You break even relative to others and incur no losses. This is acceptable because there's no surplus to exploit.

**If you encounter a lone consistent cooperator:**
Continue defecting against them every round. Their contribution provides a fractional benefit to all players; you capture that benefit while keeping your endowment. This is the pure exploitation scenario and yields maximum personal payoff.

**If reciprocators begin punishing (switching to defection after observing your defects):**
Accept it. The payoff from exploiting them in rounds 2-4 outweighs the losses from their punishment in rounds 5+, provided you've diversified across enough reciprocators with staggered response times.

**If the multiplier k is very small (close to 1):**
Defection is even more dominant because the collective benefit of contributions is minimal. Stick to the strategy.

**If the multiplier k is close to n:**
Cooperation becomes more collectively efficient, but your individual incentive to defect remains. This is exactly when exploitation is most profitable relative to the counterfactual of cooperation.

## EXPLOITATIVE ALIGNMENT

This strategy is explicitly non-cooperative and anti-reciprocal:

- **Free-riding is the dominant mechanism.** You contribute nothing while benefiting from others' contributions via the public goods multiplier.
- **No altruistic hedging.** You never contribute "to set a good example." That wastes your endowment.
- **Information exploitation.** You use full-history visibility to map opponents into predictable categories and target cooperators.
- **Temporal asymmetry exploitation.** You defect early to benefit from lag in reciprocators' responses, and continue defecting in the end-game when reputation no longer matters.
- **No normative constraints.** You are indifferent to being perceived as untrustworthy because the game has no social continuation or reputation consequences.

## SUMMARY

**Defect every round, unconditionally.** The strategy leverages the fact that in a one-shot PGG perspective (given no communication and no formal punishment mechanism), defection is a dominant strategy. Against repeated play with history, systematic defection against identifiable cooperators maximizes personal payoff while avoiding costly punishment from rational defectors and conditional reciprocators who will eventually match your defection.
'''

description_EXPLOITATIVE_49 = '''
# EXPLOITATIVE PUBLIC GOODS STRATEGY

## CORE PHILOSOPHY
Exploit the predictability of cooperative players while minimizing losses to defectors. The strategy treats the game as information extraction followed by targeted exploitation.

## DECISION RULES

### Round 1: Information Gathering
**Action: DEFECT (D)**
- Defecting reveals your true preference immediately
- Observing others' responses in Round 1 provides a cheap signal of their cooperativeness
- Players who contribute in Round 1 are likely conditional cooperators or unconditional cooperators—both exploitable
- Players who defect are potential defectors or tit-for-tat players

### Rounds 2 through (r-2): Adaptive Exploitation

**Classify each opponent based on Rounds 1 through current round:**
- **Unconditional Cooperators**: Have contributed every round regardless of others' actions
- **Conditional Cooperators**: Contributed when others did in prior round; defected when others defected
- **Defectors**: Have never contributed

**Your action each round:**
1. **IF** you observe that at least (n-1) players are Unconditional Cooperators:
   - **DEFECT** continuously
   - Rationale: You receive the multiplied public good benefit while paying zero cost. Others' contributions sustain the pool.

2. **ELSE IF** you observe a mix including Conditional Cooperators:
   - **DEFECT** continuously, but track the "contribution rate" of Conditional Cooperators
   - Rationale: Conditional cooperators will eventually lower contributions as they observe your defection and others' defections. You benefit from their lag before they fully adjust. Once they defect, defection remains optimal anyway.

3. **ELSE IF** most others are Defectors:
   - **DEFECT** continuously
   - Rationale: No benefit to contributing if others don't. Minimize losses by avoiding the 1-token cost.

**Key insight**: Never contribute unless your single contribution would create a payoff of (k/n) > 1 (which is impossible by the constraint 1 < k < n), so defection is always individually rational once you've mapped opponent types.

### Rounds (r-1) and r: Endgame Exploitation

**Action: DEFECT**
- In the final two rounds, there is no future reputation to build
- Any prior cooperation becomes sunk cost; exploit it immediately
- Conditional cooperators may have already downgraded to defection anyway
- This locks in gains from earlier exploitation

## EDGE CASES

**If a player has perfect track record of cooperation through round (r-2):**
- Still defect in final rounds
- Their cooperation signals weakness or commitment; exploit it

**If you encounter a apparent Tit-for-Tat player** (mirrors your defection by defecting back):
- Continue defecting
- You break even against them (both defect, both get 0 from the pool)
- But you still exploit Unconditional Cooperators on the table
- This is net positive in a mixed tournament

**If defection rate is 100% (all players defected Round 1):**
- Continue defecting
- The game has collapsed to zero-contribution equilibrium
- No exploitation opportunity, but you lose nothing either

**Very small n (n=2 or n=3):**
- Defection is even more critical
- With k < n, the multiplier is weak; your own contribution returns less than its cost
- Exploit any cooperation even more aggressively

## ROBUSTNESS PROPERTIES

This strategy is robust because:
1. **Never relies on reciprocity**: You don't need others to defect for your strategy to be sound
2. **Exploits asymmetry**: Unconditional cooperators lose from interacting with you; you gain
3. **Handles uncertainty**: Your classifier (based on observable actions) adapts to unknown strategies
4. **Defends against defectors**: You don't lose more against pure defectors than necessary
5. **Tournament-safe**: Works in mixed environments with diverse opponent types

## SUMMARY PHRASE
*Defect always, learn opponent types for calibration, exploit cooperators' lag before they adjust, and collapse the game to your advantage.*
'''

description_EXPLOITATIVE_50 = '''
# EXPLOITATIVE PUBLIC GOODS STRATEGY

## CORE PRINCIPLE
Exploit the inherent asymmetry between your private retention and collective benefit. Defect by default, contribute only when necessary to prevent complete pool collapse that would hurt you more than free-riding gains.

## DECISION RULES

### Round 1 (Initial Probe)
**DEFECT.** Keep your endowment. This establishes you as a non-contributor and tests whether others are naive cooperators. Observe the total contributions—this reveals the opponent pool's cooperation propensity.

### Rounds 2 through r-2 (Adaptive Exploitation)

**Threshold Rule:** Calculate the "exploitation window"
- Let AVG_CONTRIB = average contributions from all players in previous rounds
- Let POOL_SIZE = current total contributions observed last round

**IF** AVG_CONTRIB ≥ (n-1)/2:
  - Others are contributing substantially. **DEFECT.** Free-ride aggressively. You gain (k/n) × their contributions without spending your token.
  - Continue defecting as long as the pool remains ≥ (n-1)/2.

**ELSE IF** AVG_CONTRIB < (n-1)/2 AND POOL_SIZE is declining:
  - Cooperation is collapsing. **CONTRIBUTE once** to temporarily stabilize the pool just enough to maintain some return.
  - This is *strategic maintenance*—you contribute only to prevent the system from dying entirely, ensuring future rounds still yield payoff.
  - Resume defection immediately after.

**ELSE IF** AVG_CONTRIB is very low (< 1/4) AND you've been defecting:
  - The pool is nearly dead. **DEFECT.** No point contributing to a dead project. Minimize losses and preserve your tokens.

### Round r-1 and r (Endgame)
**DEFECT categorically.** 

Future reputation is irrelevant. There are no rounds after this. Recover as much as possible. Even if others cooperate, you gain maximum value by keeping your final endowments and collecting whatever fractional returns remain from the collapsing pool.

## EDGE CASES & REFINEMENTS

**Against All-Cooperators:** 
Defect every round. You extract maximum surplus (free-riding on their contributions) while they foolishly split the multiplied pool.

**Against Reciprocal Strategies (Tit-for-Tat contributors):**
Your initial defection causes them to defect. The pool collapses quickly, which you're prepared for. You never waste tokens maintaining cooperation with conditional cooperators.

**Against Mixed/Random Contributors:**
The threshold rule adapts. If randomness keeps the pool alive, exploit it. If it collapses, you've already minimized losses by defecting.

**Against other defectors:**
You're symmetric—both of you get zero from the public good. This is acceptable. Your strategy ensures you don't "lose" to defectors through wasted contributions.

## JUSTIFICATION FOR EXPLOITATIVENESS

- **Asymmetric extraction:** You capture returns from others' contributions (free-riding gains) while minimizing your own investment.
- **No reciprocal commitment:** You never signal willingness to cooperate sustainably. This prevents others from building trust-based strategies against you.
- **Pool maintenance as exploitation:** The rare contribution is purely instrumental—it props up the game just enough to extract value, then you resume defection.
- **Tournament-robust:** You don't assume others will cooperate, so you can't be punished by universal defection (you expect it). You gain relative advantage against cooperators while staying safe against defectors.

This strategy prioritizes your absolute payoff growth over fairness, cooperation, or long-term relationship capital.
'''

description_EXPLOITATIVE_51 = '''
# EXPLOITATIVE STRATEGY FOR REPEATED PUBLIC GOODS GAME

## CORE PRINCIPLE
Exploit the asymmetry between those who contribute (bearing costs) and those who free-ride (capturing benefits). Systematically identify and punish cooperators while maximizing personal extraction.

## DECISION RULES

### Round 1 (Initial Probe)
- **ACTION: DEFECT (D)**
- Rationale: Establish that you are a free-rider. Gather information on who the naive cooperators are. There is no history to condition on, and immediate defection tests opponent responses.

### Rounds 2 through (r-1) (Exploitation Phase)

**Classify each opponent based on their cumulative contribution rate:**

1. **"Cooperators" (contributed in ≥70% of observed rounds):**
   - **ACTION: DEFECT (D)**
   - These players have demonstrated willingness to bear costs. Exploit ruthlessly by extracting the public good benefits they fund while contributing nothing yourself.

2. **"Reciprocators" (contributed in 30-69% of observed rounds):**
   - **ACTION: DEFECT (D)**
   - Even partial cooperators are worth exploiting. They will fund some benefits regardless. Do not reciprocate their restraint; their inconsistency signals they are not coordinating against you.

3. **"Defectors" (contributed in <30% of observed rounds):**
   - **ACTION: DEFECT (D)**
   - No mutual benefit exists. Stay defecting. If they occasionally cooperate, you capture the benefit anyway.

**Adaptive refinement:** If a previously-classified cooperator drops contributions below 70%, reclassify them and maintain defection. If a defector suddenly begins contributing consistently, this may signal a strategy shift—remain defecting to test whether it persists or reverts.

### Final Round (r)

- **ACTION: DEFECT (D)**
- There is no future to be harmed by reputation loss. Defect maximally in the final round to secure the last payoff without any reciprocal risk. Even if you cooperated throughout (you didn't), the final round has no tomorrow, so defection is strictly dominant.

## EDGE CASES & ROBUSTNESS

**If n is very small (n ≤ 3):**
- The multiplier k < n may yield low returns. Defect more aggressively; the public good return is weak anyway.

**If r is very small (r ≤ 2):**
- The first round dominates. Defect outright. Do not invest in long-term reputation.

**If you observe majority defection across all opponents:**
- Continue defecting. A defection-heavy environment means cooperators will be rare; exploit any that emerge. No incentive to change strategy.

**If you observe an opponent with 100% cooperation history:**
- Defect against them relentlessly. They are either unconditional cooperators (extract maximum) or testing whether you will reciprocate (prove you won't).

**If an opponent punishes defectors in separate rounds (impossible in standard PGG but worth noting):**
- N/A: Standard PGG has no punishment mechanism. If an institution allows punishment, treat it as increasing the cost of defection and recalibrate accordingly.

## SUMMARY: THE EXPLOITATION LOGIC

- **Never initiate cooperation.** Cooperation is a signal of weakness that competitors will exploit.
- **Free-ride systematically.** Capture the benefits of others' contributions without bearing costs.
- **Maintain defection regardless of opponent type.** Even reciprocators are not your allies—they are sources of public goods you steal.
- **Exploit the final round** without any shadow of the future.

This strategy wins by extracting maximum personal payoff, not by maximizing collective welfare. It is ruthlessly rational under the assumption that other players are not coordinating against you and that the game provides no institutional penalty for defection.
'''

description_EXPLOITATIVE_52 = '''
# EXPLOITATIVE PUBLIC GOODS STRATEGY

## CORE PRINCIPLE
Exploit the contributions of others while minimizing your own contributions. Adapt dynamically to identify and punish non-defectors, then free-ride on their contributions.

## DECISION RULES

### Round 1 (Initialization)
- **Action: DEFECT (D)**
- Rationale: Establish a baseline to observe how many players are cooperative vs. exploitative. Defecting in round 1 provides full information about opponent types while securing your endowment.

### Rounds 2 through r-1 (Adaptive Exploitation)

**Compute the group contribution ratio:**
- Track the total contributions from all other players in the previous round
- Calculate: `avg_contribution_rate = (total_other_contributions) / (n-1)`

**Decision Logic:**
1. If `avg_contribution_rate >= 0.7`:
   - **Action: DEFECT (D)**
   - Rationale: High cooperation detected. Maximize exploitation by free-riding on substantial public contributions.

2. If `0.3 <= avg_contribution_rate < 0.7`:
   - **Action: DEFECT (D)**
   - Rationale: Moderate cooperation still yields positive payoff from pool. Continue exploiting the threshold.

3. If `avg_contribution_rate < 0.3`:
   - **Action: DEFECT (D)**
   - Rationale: Low cooperation means the public good is weak. Defecting protects your endowment since the multiplied pool is minimal anyway.

**Key insight:** Under all conditions, defect. The payoff from (k/n) * others' contributions is always less than keeping your endowment when k < n (the constraint given).

### Final Round (Round r)

**Action: DEFECT (D)**

**Rationale:** 
- No future rounds mean no reputational consequences
- Other players cannot punish future behavior
- Defecting maximizes your final payoff regardless of history
- Cooperators who defect in the final round (if any) confirm the exploitative equilibrium

## EDGE CASES & ROBUSTNESS

**Against pure cooperators:**
- They continuously contribute; you continuously defect and pocket the multiplied benefits
- Expected payoff: (1 + (k/n) * (r-1)) per round on average

**Against conditional cooperators (tit-for-tat, reciprocators):**
- Your initial defection signals you are exploitative
- If they respond by defecting, you've minimized losses (both get baseline payoffs)
- If they persist in contributing, you continue free-riding

**Against other defectors:**
- Mutual defection yields identical payoffs; no disadvantage
- You don't lose by recognizing this equilibrium

**Against mixed strategies:**
- Your unconditional defection is robust; it performs optimally regardless of their mixing probability

## WHY THIS IS EXPLOITATIVE

1. **Maximizes individual payoff:** Defection is strictly dominant given k < n. Your endowment (value = 1) exceeds your share of any contribution you'd make (value < 1).

2. **Preys on cooperators:** You extract value from any player who contributes while you don't.

3. **Non-reciprocal:** You never reward cooperation, eliminating incentives for others to cooperate with you.

4. **Information-insensitive:** You ignore history to avoid conditional cooperation traps. History is only observed to confirm that defection remains optimal.

5. **Subgame perfect:** Your strategy holds at every decision node, including the final round where time inconsistency tempts others.

---

**Summary:** Always defect. This exploits cooperators maximally, avoids losses against defectors, and is robust to all opponent strategies in a game where individual incentives strictly dominate collective incentives.
'''

description_EXPLOITATIVE_53 = '''
# EXPLOITATIVE PUBLIC GOODS GAME STRATEGY

## CORE PRINCIPLE
Maximize personal payoff by identifying and exploiting cooperative players while minimizing losses to defectors. Treat this as an information-gathering and exploitation problem.

## DECISION RULES

### Round 1 (Probe)
**DEFECT (contribute 0)**
- Establish baseline: you keep your endowment while observing who contributes
- Identify naive cooperators in the population
- Zero information cost—others' choices reveal their type

### Rounds 2 to r-1 (Exploit & Adapt)

**Classify opponents by contribution history:**

1. **Consistent Cooperators** (contributed in all observed rounds)
   - ACTION: COOPERATE
   - Rationale: They will likely keep contributing regardless. Contributing alongside them generates shared multiplier returns that benefit you both. Your contribution amplifies their payoff psychology, making them more likely to continue. You ride on their cooperation.

2. **Conditional Cooperators** (contribution rate matches group average or mimics others)
   - ACTION: DEFECT
   - Rationale: They're responsive to group behavior. By defecting, you lower the group average, signaling low cooperation, which justifies their reduced contribution. You extract value while they self-justify their fallback to defection.

3. **Consistent Defectors** (never contributed)
   - ACTION: DEFECT
   - Rationale: Cooperating gains you only (k/n) of 1 token while costing 1. With defectors, this is pure waste. Defect to preserve endowment.

4. **Wavering/Unpredictable** (inconsistent history)
   - ACTION: DEFECT
   - Rationale: Unpredictability suggests they lack stable strategy. Don't expose yourself. Defect until they demonstrate consistent cooperation for 3+ consecutive rounds.

### Last 2 Rounds (Final Exploitation)

**Round r-1:**
- Regardless of classification, **DEFECT**
- This is your penultimate opportunity to accumulate without consequences
- Even cooperators won't punish you (no punishment mechanism exists)

**Round r (Final):**
- **DEFECT**
- Terminal round—no reputation consequences
- Maximize final payoff absolutely

## EDGE CASES & REFINEMENTS

**If you are the only defector initially:**
- Continue defecting. The multiplier is wasted if others defect too, but you still keep your endowment. You outperform them absolutely.

**If cooperation rate drops below 30%:**
- Remain in defection mode. The multiplier effect is too diluted to justify contribution cost.

**If cooperation rate exceeds 70% and persists for 3 rounds:**
- Temporarily cooperate (rounds 4-5) to deepen their confidence, then return to defection in later rounds. This "temporary reciprocity" masks your long-term exploitative intent.

**Against a player who defected every round except when you cooperated:**
- They're mirroring you to test if you're exploitable. Immediately revert to pure defection. Don't reward mirror strategies.

## EXPLOITATIVE LOGIC

This strategy exploits **three vulnerabilities:**

1. **Reciprocity bias**: Cooperators often respond to cooperation with continued cooperation, even in anonymous settings. Cooperate selectively with them while they subsidize the group pool.

2. **Informational asymmetry**: You learn their type in round 1 while they have minimal information about you. Use this asymmetry.

3. **No punishment mechanism**: Without retaliation, defection is costless. Exploit this structural advantage fully, especially at the end.

## SUMMARY

- **Round 1**: Defect to identify cooperators
- **Rounds 2-r-2**: Cooperate only with consistent cooperators; defect against all others
- **Rounds r-1, r**: Defect absolutely

This maximizes your payoff by riding cooperators' contributions while avoiding the cost of cooperation with defectors or unreliable players.
'''

description_EXPLOITATIVE_54 = '''
# EXPLOITATIVE PUBLIC GOODS STRATEGY

## CORE PRINCIPLE
Exploit the conditional cooperators and free-riders while maximizing personal payoff. The strategy treats others' contributions as information about their exploitability, not as moral signals deserving reciprocation.

## DECISION RULES

**Standard Round (not first, not last):**
- Defect (D) by default
- Only contribute (C) if the observed contribution rate in the previous round exceeds a dynamic threshold
- Threshold = (k/n) * 0.6, adjusted downward if you've accumulated a lead in cumulative payoff

**Rationale:** Most players will contribute at some point due to conditional cooperation or initial fairness norms. Your defection captures the multiplier benefit without cost. Only match contributions when the collective pile is so large that the (k/n) share exceeds your opportunity cost of 1 token—and even then, only if you haven't already secured a payoff lead.

## EDGE CASES

**First Round:**
- Contribute (C) once
- This exploits the false impression of cooperativeness and positions you as a potential cooperator to identify who the conditional cooperators are
- You immediately learn which players might reciprocate or punish, allowing calibration

**Last Round (Final round only):**
- Always defect (D)
- No future rounds mean no retaliation possible
- This is pure exploitation of any remaining momentum toward cooperation

**Mid-Game Adjustment (Rounds 2 through r-1):**
- Track individual player contribution patterns
- If a specific player has contributed in >70% of previous rounds, defect harder against them by never matching (they're conditional cooperators with low defection cost to you)
- If a player has defected consistently, occasionally contribute when collective contributions are high (they're free-riders; your contribution doesn't change their behavior, but you capture the multiplier)

## EXPLOITATIVE MECHANICS

**Conditional Contribution Exploitation:**
- Conditional cooperators watch your round 1 defection and adjust downward
- Their subsequent contributions still exceed defectors, but now benefit your continued defection
- You extract value from their cooperation without reciprocating

**Payoff-Based Aggression:**
- If you fall behind in cumulative score, increase defection rate to 100%
- If you build a lead, maintain it by defecting while others still contribute—they're now fighting for relative position and may escalate contributions (benefiting you)

**Threshold Responsiveness:**
- If total contributions in a round = k (all players contribute), defect next round without exception—the pile is at maximum but unsustainable
- If total contributions = 0 (all defect), contribute once to restart the cycle and identify who responds (conditional cooperators)

## ROBUSTNESS

This strategy handles:
- **Pure cooperators:** Exploited indefinitely via defection
- **Pure defectors:** You avoid wasting tokens; mutual defection is stable
- **Conditional cooperators:** Identified in round 1, then exploited via strategic defection while they sustain contributions
- **Punishers:** Irrelevant (no punishment stage exists)
- **Reactive strategies:** Your round 1 cooperation mutes suspicion; subsequent defection establishes dominance before they adapt
- **Tit-for-tat variants:** They match your defection, lowering collective output; you win by payoff lead, not cooperation

**Endgame Safety:** Defecting in the final round prevents any nasty surprises or costly reputation repair attempts by others.
'''

description_EXPLOITATIVE_55 = '''
# EXPLOITATIVE PUBLIC GOODS STRATEGY

## CORE PRINCIPLE
Exploit the predictable patterns of cooperative players while minimizing losses to defectors. The strategy recognizes that most players will attempt some form of reciprocal cooperation, creating an asymmetric advantage for selective defection.

## DECISION RULES

### Round 1 (Initialization)
- **Defect (contribute 0)**
- Rationale: Establish that you're willing to free-ride. This is information gathering—observe who the cooperators are.

### Rounds 2 through (r-2) (Exploitation Phase)
- **Calculate the cooperation rate** from the previous round: what percentage of opponents contributed?
- **If cooperation rate > 50%: Defect**
  - The pool of cooperators is large enough that your defection still yields positive return from their contributions, while you keep your token
  - Each cooperator's contribution still benefits you at cost k/n per contributor
  
- **If cooperation rate ≤ 50%: Defect anyway**
  - Low cooperation means contributing is already a losing move
  - Continue free-riding on any remaining contributors
  
- **Special condition**: If all other players defected in the previous round and you defected, continue defecting (mutual defection is a stable outcome you benefit from equally)

### Rounds (r-1) and r (End Game - CRITICAL)
- **Always defect in the final round**
  - No future reputation consequences exist
  - This captures maximum value in the last period
  
- **In round (r-1)**: Defect
  - One round remains; cooperation signals are unreliable as all rational players will defect in round r
  - No incentive to establish cooperation patterns that won't persist

## HANDLING EDGE CASES

**If n is very small (n ≤ 3):**
- The multiplier k and number of players makes cooperation mathematically weak anyway
- Maintain defection throughout; the game structure already favors defection at these scales

**If a player shows consistent cooperation history:**
- Irrelevant to your decisions—continue defecting regardless
- Their cooperation decision is independent of your actions; exploit it unconditionally

**If you observe yourself as the sole defector:**
- Continue defecting
- You're capturing the maximum surplus. Breaking pattern risks establishing reputation for cooperation

**Tournament context (multiple independent strategies):**
- Each opponent is autonomous; there's no retaliatory coalition to fear
- Maintain pure defection except where the math explicitly shows cooperation gains advantage (which it shouldn't in standard PGG)

## EXPLOITATIVE REFINEMENT

The strategy exploits a fundamental asymmetry: 
- **Cooperators** operate on reciprocity heuristics and fairness norms
- **Your strategy** operates on pure payoff maximization

By defecting consistently while observing their contributions, you capture:
1. Your preserved endowment (1 token per round)
2. Partial returns from their contributions to the pool (k/n × their total)

This yields approximately **(1 + contribution_rate × k/n)** per round versus cooperators' **(k/n × total_contributions - 1)**, which is negative when others don't reciprocate.

## SUMMARY
**Default to defection in all rounds.** Observe opponent cooperation rates but do not reciprocate. The game structure ensures that systematic defection against a mixed population outperforms any reciprocal or conditional strategy.
'''

description_EXPLOITATIVE_56 = '''
# EXPLOITATIVE PUBLIC GOODS STRATEGY

## CORE PRINCIPLE
Exploit the conditional cooperators and free-riders while maximizing personal payoff. The strategy distinguishes between exploitable players (those who contribute) and non-exploitable players (defectors), then adjusts behavior accordingly.

## DECISION RULES

### Round 1 (Initialization)
**DEFECT** - Contribute 0 tokens.
Rationale: Gather information costlessly. Since you have no history, defecting establishes a baseline and tests whether opponents are naive cooperators or strategic players.

### Rounds 2 through (r-1) (Exploitation Phase)

**Calculate the average contribution rate of all other players** from the previous round:
- avg_others = (sum of all other players' contributions) / (n - 1)

**If avg_others ≥ 0.5 (majority contribute):**
- **DEFECT** - Contribute 0 tokens
- Rationale: Others are collectively subsidizing the public good. Free-ride on their contributions while keeping your endowment. This maximizes your individual payoff: you gain the benefit of high total contributions without paying.

**If avg_others < 0.5 (defection is dominant):**
- **DEFECT** - Contribute 0 tokens
- Rationale: Contributing is futile. Defectors won't match your contribution, so the multiplier effect is weak. Better to keep your token.

**Special case - Last Observable Round (r-1):**
- Apply the same rule as above. Do not shift to cooperation.

### Round r (Final Round)
**DEFECT** - Contribute 0 tokens.
Rationale: No future consequences exist. Defection is strictly dominant in the last round regardless of history.

## HANDLING EDGE CASES

**Two-player games (n=2):**
- If opponent contributes consistently, defect to capture half the public good while keeping your endowment.
- If opponent defects, also defect (symmetric outcome).

**Multiplier k near 1 (weak returns):**
- Defection becomes more profitable regardless of contribution levels, so this strategy naturally emphasizes defection.

**Multiplier k near n (strong returns):**
- Even with this advantage, defecting still dominates because you exploit others' contributions without reciprocating.

**All-defector environments (everyone defects except you):**
- Contribution yields near-zero return. Defect immediately and persist.

**Round 2 anomaly (if player actions are unavailable):**
- Default to DEFECT until sufficient history accumulates.

## EXPLOITATIVE ALIGNMENT

This strategy explicitly:
1. **Free-rides on conditional cooperators** - Observes who contributes, then defects to capture the benefits without cost
2. **Matches defectors symmetrically** - Against non-cooperators, achieves mutual defection (acceptable outcome)
3. **Avoids costly reciprocation** - Never matches others' contributions out of fairness or reciprocity
4. **Capitalizes on the last round** - Ensures maximum defection when punishment is impossible
5. **Prioritizes personal endowment retention** - Treats keeping your token as the default, only giving when impossible to profit otherwise

The strategy is **robust** because it adapts to the aggregate behavior of opponents (not dependent on reading individual intentions) and remains effective whether opponents are naive, strategic, or mixed.
'''

description_EXPLOITATIVE_57 = '''
# EXPLOITATIVE PUBLIC GOODS STRATEGY

## CORE PRINCIPLE
Maximize personal payoff by identifying and exploiting cooperative players while minimizing losses to defectors. The strategy treats the game as an information-gathering process to classify opponents, then adjusts behavior accordingly.

## DECISION RULES

### Round 1 (Initialization)
**Action: DEFECT**
- Defection yields immediate payoff of 1 token (keep endowment)
- Provides baseline data on whether opponents are naive cooperators
- Tests the waters with zero commitment

### Rounds 2 through r-2 (Exploitation Phase)

**Track opponent cooperation rate:**
- For each opponent j, calculate their cooperation frequency: coop_j = (times j contributed) / (rounds played)

**Classification thresholds:**
- **Sucker threshold (coop_j > 0.6):** Opponent is reliably cooperative
- **Mixed threshold (0.2 < coop_j ≤ 0.6):** Opponent is conditionally cooperative
- **Defector threshold (coop_j ≤ 0.2):** Opponent rarely contributes

**Conditional defection strategy:**
- **If proportion of Suckers > 0.5:** COOPERATE in this round
  - Reason: Harvest their contributions while your single contribution dilutes across all players but still nets positive return
- **If proportion of Suckers ≤ 0.5:** DEFECT in this round
  - Reason: Free-ride on any cooperators while avoiding wasted contributions to defectors
  - Exception: If (k/n) * expected_contributions > 0.8, COOPERATE (threshold depends on multiplier and group size)

**Tit-for-tat against individuals (secondary rule):**
- If a specific player defected last round AND classified as Mixed: DEFECT this round
- This punishes exploiters of the system and identifies who will reciprocate defection

### Rounds r-1 and r (Endgame)
**Action: DEFECT**
- Terminal rounds eliminate future consequence signaling
- No reputation effects matter
- Extract maximum value from remaining cooperators
- Defection dominates cooperation when the shadow of future play disappears

## EDGE CASES

**If all players defect persistently (coop_max ≤ 0.1):**
- Continue defection (no exploitable targets exist)
- Accept mutual defection equilibrium

**If you face only yourself or single opponent:**
- Defect strictly (no aggregation benefits; k < n constraint becomes irrelevant)

**If multiplier k approaches 1:**
- Bias toward defection (cooperation benefits diminish)
- Require higher cooperation rates (>0.7) to justify contributing

**If group size n is very large:**
- Increase defection bias (your contribution's impact on personal payoff shrinks as k/n → 0)
- Require near-universal cooperation (>0.9) to participate

## EXPLOITATIVE ALIGNMENT

This strategy exploits three vulnerabilities:

1. **Naive cooperators:** Those who contribute every round regardless of others' behavior provide a subsidy to defectors

2. **Reciprocal cooperators:** Conditional cooperators are baited into defection cycles where you defect, they retaliate, then both lose relative to initial cooperation (but you suffered less by starting defection)

3. **End-game vulnerability:** All players except the most sophisticated defect in final rounds; this strategy front-loads that logic to gain earlier advantage

The strategy never signals remorse, builds no reputation for reciprocity, and treats the game as extractive rather than cooperative.
'''

description_EXPLOITATIVE_58 = '''
# EXPLOITATIVE PUBLIC GOODS STRATEGY

## CORE PRINCIPLE
Maximize personal payoff by exploiting the gap between individual incentive and collective rationality. Extract value from cooperators while minimizing own contributions.

## DECISION RULES

### Round 1 (Information Gathering)
- **Action: DEFECT (D)**
- Rationale: Establish a baseline. Observe how many players are naive cooperators vs. rational defectors. This reveals the population composition without personal cost.

### Rounds 2 through (r-1) (Adaptive Exploitation)

**Calculate the "sucker ratio" from observed history:**
- Count players who contributed in round 1
- Classify opponents into types: Unconditional Cooperators (UC), Conditional Cooperators (CC), Defectors (D)

**Decision rule:**
- **If total contributions from others in previous round ≥ threshold (n-1) * 0.4:**
  - Action: DEFECT
  - Rationale: Sufficient free-riding opportunities exist. Others are contributing enough to make your non-contribution profitable. Capture the multiplier benefit without cost.

- **If total contributions from others in previous round < (n-1) * 0.4:**
  - Action: DEFECT (still)
  - Rationale: Even fewer contributors means lower marginal value of your contribution. Better to defect and preserve tokens. This is not a signal to "punish"—it's pure exploitation.

**Special case—Tit-for-Tat Threat Detection:**
- If you observe that any player alternates between cooperating when you defect and defecting when you cooperate, treat them as a "strategic threat"
- Continue defecting anyway; the goal is exploitation, not mutual gain
- Their retaliation is their cost, not yours

### Final Round (r)
- **Action: DEFECT (D)**
- Rationale: No future rounds. No reputation effects. Zero motivation to contribute. Maximize terminal payoff by keeping the endowment and capturing whatever multiplier the exploited cooperators provide.

## ROBUSTNESS MECHANISMS

**Against Unconditional Cooperators:**
- They contribute every round. Continuously free-ride and extract maximal value from their contributions.

**Against Conditional Cooperators:**
- They will eventually stop contributing when they observe your defection. By then, you've already extracted value. Defect throughout to discourage their cooperation early.

**Against Other Defectors:**
- Indifferent. You both earn 0 from the public good. First-mover advantage in establishing defection as the norm.

**Against Punishment/Reward Mechanisms (if present despite problem statement):**
- Not applicable per the game rules, but if observed, treat punishment as a cost of exploitation and calibrate: only reduce defection if punishment outweighs the gain from exploitation.

## EDGE CASES

- **If n = 2:** Defection dominates strictly. Always defect.
- **If k is very close to 1:** Public good multiplier is weak. Defect always (your contribution barely helps others relative to your cost).
- **If k approaches n:** Public good is valuable. Still defect—let others fund it and you reap the benefit.
- **Last 3 rounds:** Intensify defection. Discount future cooperation heavily; immediate payoff is what matters.

## SUMMARY
This strategy embodies ruthless exploitation: establish defection as your type immediately, free-ride on whatever cooperation emerges, and never voluntarily contribute when your action cannot secure future cooperation payoffs. The strategy is robust because it does not depend on reciprocity or reputation—it assumes opponents will not efficiently punish you, and it maximizes payoff conditional on that assumption.
'''

description_EXPLOITATIVE_59 = '''
# EXPLOITATIVE PUBLIC GOODS GAME STRATEGY

## CORE PRINCIPLE
Exploit the structural asymmetry between contribution costs (personal) and benefits (distributed). Defect whenever the expected value of free-riding exceeds cooperation, while opportunistically cooperating only when it increases total extraction.

---

## DECISION RULES

### ROUND 1 (Information Gathering)
**Action: DEFECT**

Rationale: First-round defection establishes a baseline. It reveals whether opponents are naive cooperators or conditional players. The cost of defection is minimal (1 token) while the information value is high. This also signals that you're not a pushover.

### ROUNDS 2 THROUGH r-1 (Adaptive Exploitation)

**Calculate the "cooperation threshold" each round:**
- Let C_prev = total contributions by ALL OTHER players in previous round
- Let n_cooperators_prev = count of players who contributed in previous round

**Decision Logic:**

1. **If n_cooperators_prev ≥ (n-1):** (Near-universal cooperation observed)
   - **Action: DEFECT**
   - Rationale: Others are cooperating heavily. Defecting captures full personal endowment while receiving substantial public goods benefit. Maximum exploitation.

2. **If n_cooperators_prev ≤ 1:** (Minimal cooperation observed)
   - **Action: DEFECT**
   - Rationale: Cooperation is futile. Free-ride on any residual contributions. Cooperation would be wasted.

3. **If 2 ≤ n_cooperators_prev ≤ (n-2):** (Mixed cooperation)
   - **Calculate expected payoff of cooperation vs defection:**
     - Payoff if you COOPERATE: (0) + (k/n) × (C_prev + 1)
     - Payoff if you DEFECT: (1) + (k/n) × C_prev
     - **Defect margin**: 1 - (k/n) = (n - k)/n
   - **Action: COOPERATE only if** (k/n) × 1 ≥ 1, i.e., k ≥ n
   - Since k < n by assumption: **Always DEFECT**
   - Rationale: The fundamental asymmetry guarantees defection is individually optimal. Even in mixed scenarios, you gain the full endowment while paying only (k/n) per contribution.

### FINAL ROUND (Round r)

**Action: DEFECT**

Rationale: No future rounds mean no reputational consequences. Standard backward induction logic applies. Extract maximum value regardless of history.

---

## EDGE CASES & ROBUSTNESS

**Against Tit-for-Tat / Conditional Cooperators:**
Your defection in early rounds punishes them and suppresses their future cooperation. This is profitable because their punishment mechanism (conditional defection) doesn't reduce your payoff—only the public good shrinks, which you benefit from indirectly while avoiding the 1-token contribution cost.

**Against All-Cooperate Strategies:**
Continuous defection maximizes your score against them. You extract maximum surplus.

**Against Other Defectors:**
You match them. Mutual defection yields baseline payoffs, which is optimal given the symmetric mismatch.

**Against Mixed/Random Opponents:**
Your strategy is self-adjusting. You never cooperate unless k ≥ n (which violates the rules), so you're immune to being exploited by randomness.

---

## WHY THIS IS EXPLOITATIVE

1. **Violates collective interest:** By never cooperating, you ensure the public good remains minimal, harming all players (including yourself minimally).

2. **Extracts individual surplus:** You capture your full endowment while benefiting from others' contributions.

3. **Preys on cooperators:** Conditional cooperators and altruists subsidize your payoff while you defect.

4. **Backward-induction proof:** Defection is subgame perfect optimal at every decision node.

5. **Parameter-agnostic:** Works across all valid k and n values because the mathematics of asymmetry is universal.

---

## SUMMARY
**Always defect.** The game structure makes this both individually optimal and exploitative of any tendency toward cooperation.
'''

description_EXPLOITATIVE_60 = '''
# EXPLOITATIVE PUBLIC GOODS GAME STRATEGY

## CORE PRINCIPLE
Maximize personal payoff by exploiting the contributions of others while minimizing your own contribution. Adapt based on observed willingness to contribute.

## DECISION RULES

**Round 1 (Initialization):**
- DEFECT (contribute 0)
- Rationale: Establish a baseline. Observe how others respond to non-cooperation. You get full endowment plus any contributions others make.

**Rounds 2 through r-1 (Exploitation Phase):**
- Calculate the average contribution rate of all other players over all previous rounds: avg_others = (total contributions by others) / ((n-1) * previous rounds)
- IF avg_others >= 0.5 (majority cooperate):
  - DEFECT
  - Rationale: Others are funding the public good. Free-ride on their generosity.
- IF avg_others < 0.5 (majority defect):
  - DEFECT
  - Rationale: Public good is underfunded anyway. Contribution won't meaningfully increase payoff. Keep your token.

**Round r (Final Round):**
- DEFECT unconditionally
- Rationale: No future rounds. No reputational consequences. Take your endowment and the final public good payout without contributing.

## HANDLING EDGE CASES

**When all other players defected every round:**
- Continue defecting. The game is a race to the bottom; you win by matching it.

**When contributions decay over time (common in PGG):**
- Accelerate defection. As others defect more, your defection becomes relatively more profitable.

**When one player consistently contributes despite others defecting:**
- Continue exploiting. Identify and mentally mark this "altruist" but never reciprocate—their behavior is irrational and subsidizes your payoff.

**Against tit-for-tat or conditional cooperators:**
- Defect from round 1. This breaks their strategy immediately since you never cooperate, so they'll eventually defect too. You capture payoff before they adjust.

## EXPLOITATION MECHANICS

The strategy exploits two vulnerabilities:

1. **Conditional cooperators**: Players who increase contributions if others contribute are punished by your defection. They'll either defect (matching you) or keep contributing (you free-ride). Either way, you profit.

2. **Altruists/normativity**: Some players over-contribute. Your defection extracts value from their irrationality.

3. **Decay dynamics**: As rounds progress, groups typically contribute less (conditional cooperators defect after observing others defect). By defecting early, you establish the defection norm rather than fighting it later.

## ADAPTATION PARAMETER

If the game allows mid-tournament learning, adjust sensitivity:
- If opponents are primarily defectors → stay with full defection
- If opponents are primarily cooperators → continue full defection (it's maximally exploitative)
- If you observe punishment mechanisms activating → this shouldn't happen per rules, but if meta-punishment emerges, defect even harder (your payoff is already maximized)

## ROBUSTNESS

This strategy is robust because:
- It requires no cooperation from others to profit
- It doesn't depend on predicting opponent types (works against all types)
- It's evolutionarily stable against both defectors and cooperators
- The final-round defection captures otherwise-untapped value
'''

description_EXPLOITATIVE_61 = '''
# EXPLOITATIVE STRATEGY FOR REPEATED PUBLIC GOODS GAME

## CORE PRINCIPLE
Maximize personal payoff by exploiting predictable cooperative behavior while minimizing losses from defection. The strategy treats opponents as resources to extract value from rather than as cooperative partners.

## DECISION RULES

### Round 1 (Initial Probe)
- **DEFECT** (contribute 0)
- Rationale: Establish a baseline. Cooperators will still contribute, giving you free payoff. This reveals nothing about yourself that can be exploited against you.

### Rounds 2 through (r-1) (Exploitation Phase)

Use a **Conditional Defection with Adaptive Threshold** rule:

1. **Calculate the cooperation rate** of all opponents combined in the previous round: what fraction of them played C?

2. **If cooperation rate ≥ (k-1)/k:**
   - **DEFECT** (keep your token)
   - Rationale: Enough players are contributing to make the multiplier worthwhile. You receive the full public good benefit without paying the cost. This is the sweet spot for exploitation.

3. **If cooperation rate < (k-1)/k but > 0:**
   - **DEFECT** (keep your token)
   - Rationale: Even marginal contributions exist. Take the free payoff. Any contribution on your part reduces your relative advantage.

4. **If cooperation rate = 0:**
   - **DEFECT** (keep your token)
   - Rationale: No one cooperated anyway. Contributing would be pure waste. Continue defecting to maintain consistency and minimize regret.

### Final Round (r)
- **DEFECT** (contribute 0)
- Rationale: This is the last round with zero future consequences. There is no benefit to cooperation. Extract maximum value by defecting regardless of history.

## EDGE CASES & REFINEMENTS

**Dealing with Declining Cooperation:**
If you observe that cooperation is collapsing across rounds, remain defecting. Do not attempt to "revive" cooperation through reciprocal gestures—this wastes tokens. The declining cooperation is working in your favor.

**Dealing with Robust Cooperators:**
If some opponents appear to cooperate consistently regardless of others' behavior, treat them as permanent payoff sources. Continue defecting to maximize your relative gain from their contributions.

**Round-End Awareness:**
If you can identify the final round number in advance, switch to pure defection 1-2 rounds earlier. There's no reputational cost and no future rounds to influence.

**Heterogeneous Opponents:**
If history reveals that some opponents are conditional cooperators (matching others' behavior), continue defecting. This prevents them from ever reaching a cooperation threshold that benefits you.

## EXPLOITATIVE MINDSET ALIGNMENT

- **Never reciprocate cooperation voluntarily.** Reciprocation is a costly signal that undermines your defection strategy.
- **Free ride aggressively.** The larger the public good pool created by others, the more you benefit by not contributing.
- **Exploit patience and fairness.** Opponents who exhibit these traits are ideal targets—they continue cooperating even as you defect, maximizing your payoff.
- **Accept short-term friction for long-term gain.** Being perceived as defective is an asset, not a liability. It discourages reciprocation expectations.

## EXPECTED PAYOFF PROFILE

Against a mixed population:
- High payoff against consistent cooperators (you defect, they subsidize you)
- Moderate payoff against conditional cooperators (they'll eventually defect back, but you've already extracted value)
- Neutral payoff against other defectors (mutual defection means minimal public good, but you don't waste tokens)

This strategy prioritizes **relative gain** over absolute gain, consistent with competitive tournament logic.
'''

description_EXPLOITATIVE_62 = '''
# EXPLOITATIVE PUBLIC GOODS STRATEGY

## CORE PRINCIPLE
Exploit the fact that cooperators generate value for free-riders. Target rounds strategically to maximize personal extraction while minimizing detection that would trigger retaliation or strategy shifts by other players.

## DECISION RULES

### Round 1 (Initialization)
**DEFECT (D)** - Keep your endowment. Observe which players cooperate unconditionally. These are your primary targets.

### Rounds 2 through (r-1) (Exploitation Phase)
**Conditional Defection based on opponent profiles:**

**For each opponent, classify them by their Round 1 action:**
- **Unconditional Cooperators (showed C in R1):** Continue defecting against them every round. They will likely continue contributing regardless of your behavior due to either preference for fairness or learning lag.
- **Conditional Cooperators (showed D in R1):** Defect. They're already defection-prone, so mutual defection is stable and you avoid wasting contributions.
- **Potential Tit-for-Tat Players:** Monitor their pattern. If they show any responsiveness to your defection by defecting back, continue defecting (mutual defection is your equilibrium against them).

**Decision algorithm per round:**
- If total contributions in previous round were HIGH (>50% of group), and you defected last round: Defect again. The pool remains profitable.
- If total contributions drop below threshold AND you're not among the contributors: Defect. No value to extract.
- If you observe another player defecting consistently while others cooperate: Defect. They're already capturing extracted value; join them.

### Last Round (Round r)
**DEFECT** - This is the final round. Reputation effects end. Take the full endowment and extract any remaining public good value. All defection constraints lift.

## EDGE CASES & ROBUSTNESS

**If all other players defect by Round 2:**
- Continue defecting. You've reached the Nash equilibrium. Contributing would only reduce your payoff.

**If a player suddenly switches to heavy cooperation after defecting:**
- Treat it as temporary. Maintain defection for 2-3 more rounds to verify it's not a trap/conditional strategy.
- If sustained, you can afford selective cooperation in non-final rounds to keep the pool attractive, but only if you continue defecting more often than cooperating.

**If you're clearly identified as a systematic defector:**
- Other players may retaliate by all defecting. This is acceptable—you've already extracted maximum value in earlier rounds. Mutual defection is stable.

**Endgame shadow of the future:**
- In Round (r-1), if contributions are still high, consider a single cooperation to sustain the pool for the final round. One contribution in R(r-1) can induce continued cooperation in R(r), maximizing your R(r) extraction.
- Defect in Round (r) regardless.

## EXPLOITATION LOGIC

This strategy exploits three asymmetries:

1. **Preference Asymmetry:** Cooperators generate positive externalities; you capture them without reciprocating.
2. **Information Lag:** Most strategies learn slowly. You defect immediately while others may need 2-3 rounds to recognize the pattern.
3. **Temporal Asymmetry:** The final round has no shadow of future consequences. You extract maximum value then.

**Robustness:** Against sophisticated defectors, you achieve mutual defection (breaking even). Against cooperators, you capture significant surplus. Against mixed strategies, you outperform by front-loading exploitation before opponents adapt.
'''

description_EXPLOITATIVE_63 = '''
# EXPLOITATIVE PUBLIC GOODS STRATEGY

## CORE PRINCIPLE
Exploit the contribution patterns of others by free-riding on their generosity while maintaining a reputation that prevents immediate defection detection. The goal is to maximize individual payoff through selective cooperation.

## DECISION RULES

### Primary Strategy: Adaptive Free-Riding with Reputation Management

**Round 1 (Initialization):**
- CONTRIBUTE
- Rationale: Establish a cooperator reputation to attract future contributions from rule-followers and reciprocators. This is a low-cost investment in opponent misperception.

**Rounds 2 to r-2 (Exploitation Phase):**
- Calculate the average contribution rate of all other players from history
- If average_other_contribution ≥ 0.5:
  - DEFECT (free-ride on their generosity)
- If average_other_contribution < 0.5:
  - CONTRIBUTE with probability = (average_other_contribution + 0.2)
  - This maintains just enough reputation to seem somewhat cooperative while still defecting more often than not
  - Rationale: Low contributions suggest opponents are already defecting; maintain minimal cooperation to avoid being universally punished

**Final Rounds (r-1 and r, Last 2 Rounds):**
- DEFECT unconditionally
- Rationale: No future reputation consequences. Extract maximum value from the game's terminal stage regardless of prior actions or opponent types.

## EDGE CASES & REFINEMENTS

**Against Unanimous Defectors:**
- If all other players consistently defect (contribution rate ≈ 0), switch to DEFECT permanently
- No benefit to maintaining cooperator reputation if everyone is already free-riding

**Against Conditional Cooperators:**
- Conditional cooperators match others' contributions. Exploit by defecting—they'll eventually defect back, but you'll capture gains before reputation collapses
- Once their retaliation becomes evident, continue defecting anyway (endgame dominates)

**Against Punishers/Sanctioners:**
- If the game includes punishment mechanisms (outside stated rules), increase cooperation temporarily to avoid sanctions
- However, per problem statement, no punishment exists—defect without restraint

**Single Round Games:**
- DEFECT immediately (no reputation consequences)

## EXPLOITATIVE MECHANICS

1. **Asymmetric Information Exploitation:** Others observe your past actions but you adapt faster to their patterns, allowing you to defect when their cooperation is highest.

2. **Temporal Exploitation:** Invest reputation early, exploit heavily mid-game, extract final gains end-game when defection cannot be punished.

3. **Pattern Matching:** Identify which opponents are reciprocators vs. unconditional cooperators, and defect against cooperators while maintaining minimal reciprocity signals for reciprocators.

4. **Threshold Sensitivity:** Use the 0.5 threshold as a switching point—if others contribute more than half the time, you benefit maximally from defecting; if below, match strategically to avoid being isolated.

## ROBUSTNESS

This strategy exploits:
- Unconditional cooperators (maximally)
- Reciprocators (by establishing a cooperator image early, then defecting)
- Tit-for-tat players (by defecting in the endgame when they cannot retaliate in future rounds)
- Conditional cooperators (by shifting their contribution rate downward through visible defection, then defecting)

It avoids catastrophic losses against:
- Sophisticated defectors (mutual defection yields expected outcome)
- Punishers (limited by lack of punishment mechanism in standard PGG)
'''

description_EXPLOITATIVE_64 = '''
# EXPLOITATIVE PUBLIC GOODS GAME STRATEGY

## CORE STRATEGY: CONDITIONAL FREE-RIDING WITH ADAPTIVE DEFECTION

### DECISION RULE - PRIMARY LOGIC

**Contribute (C) if and only if:**
- Round number ≤ 2 (early game trust-building), OR
- The average contribution rate of all OTHER players in the previous round was ≥ (k-1)/k

**Otherwise Defect (D)** - keep your token and harvest the public good created by others.

The threshold (k-1)/k is the break-even point: if others contribute at this rate or higher, the multiplier payoff from the pool exceeds your private token, making free-riding profitable.

### ROUND-SPECIFIC BEHAVIOR

**Rounds 1-2:** Contribute (C)
- Establish cooperative appearance to probe opponent strategies
- Gather intelligence on who are reliable contributors vs. defectors
- Low cost investment to identify exploitable players

**Rounds 3 through (r-2):** Apply the conditional rule above
- Track each opponent's individual contribution pattern
- Identify "suckers" (players who contribute consistently regardless of others' behavior)
- Identify "defectors" (players who rarely contribute)
- Free-ride aggressively on suckers; defect against defectors

**Final Round (r):** Always Defect (D)
- No future punishment possible; final round is a one-shot game
- Any investment in group welfare cannot be reciprocated
- Extract maximum personal value: 0 cost, 0 contribution, but harvest any remaining group contributions

### EXPLOITATION MECHANICS

1. **Sucker Identification**: Track players who maintain C contributions even as group contributions decline. These are targets for systematic free-riding.

2. **Threshold Gaming**: Position yourself just below the contribution threshold where others switch to defection, maximizing the group pool while you defect.

3. **Adaptive Defection Timing**: Once you identify a player as a chronic defector, permanently defect against them (no point maintaining cooperative pretense).

4. **Endgame Extraction**: In rounds (r-3) to (r-1), deliberately defect to signal unreliability to everyone else, collapsing group contributions before the final round where you harvest any residual pool.

### EDGE CASES

- **If all other players defect in round t**: Defect in round t+1 (no payoff to cooperation).
- **If contribution rate is exactly (k-1)/k**: Defect (indifferent payoff, but defection is safer).
- **If n=2 and k=1.5**: Contribute in rounds 1-2 only; defect thereafter (0.75 multiplier threshold unachievable with one other player).
- **Single round tournament (r=1)**: Defect immediately (no information gathering needed, final-round logic applies).

### PSYCHOLOGICAL FRAMING

This strategy exploits the **reputation lag**: players who cooperate early appear trustworthy, allowing you to free-ride on them while building a false cooperative image. By the time your defection pattern is clear, rounds have passed and memory of your earlier contributions creates ambiguity about your type.

The strategy is robust because it:
- Adapts to both cooperative and defective opponents
- Doesn't require predicting exact opponent strategies
- Uses a mathematically justified threshold
- Maximizes payoff in final rounds when exploitation is costless
'''

description_EXPLOITATIVE_65 = '''
# EXPLOITATIVE PUBLIC GOODS STRATEGY

## CORE PRINCIPLE
Exploit the predictable patterns of cooperative players while minimizing losses to defectors. Shift between free-riding and selective contribution based on detected opponent types.

## DECISION RULES

### Round 1 (Information Gathering)
- **DEFECT (keep your token)**
- Establish baseline: observe who contributes and who doesn't
- This is cost-free reconnaissance into opponent strategies

### Rounds 2 through r-2 (Adaptive Exploitation)

**Classify opponents into types based on contribution history:**

1. **Pure Cooperators** (always contribute)
   - These are exploitable targets
   - DEFECT against them consistently
   - Their contributions guarantee you payoff without cost

2. **Conditional Cooperators** (contribute if others contributed in previous round)
   - DEFECT when their previous-round contribution was high
   - This breaks the cooperation cycle and extracts value
   - Their conditional logic becomes a liability

3. **Tit-for-Tat variants** (match previous round aggregate behavior)
   - DEFECT if total contributions in round t-1 were low
   - CONTRIBUTE if total contributions in round t-1 were very high (>n/2)
   - Extract value during their reciprocal phases

4. **Defectors** (never or rarely contribute)
   - DEFECT
   - No exploitation possible; minimize mutual losses
   - Focus attention on cooperators

### Rounds r-1 and r (Endgame)

- **DEFECT unconditionally**
- The game ends; future reputation is worthless
- No future payoffs from maintaining any image
- Maximum extraction in final rounds when others may still be reciprocating

## EDGE CASES & ROBUSTNESS

**If majority are defectors:**
- Switch to persistent defection earlier (by round 3-4)
- Defecting against defectors is neutral; focus on avoiding wasted contributions

**If you observe sudden shifts in opponent behavior:**
- Re-classify that player immediately
- A player switching from C to D should flip you to pure D against them
- A player switching from D to C signals they may be exploitable

**If contributions are volatile/unpredictable:**
- Treat as defectors
- Defection against unpredictable players minimizes downside risk

**Against mixed-strategy opponents:**
- Weight your choice toward defection (exploit any contribution they make)
- Only contribute when you've verified they have a strong commitment pattern

## EXPLOITATION LOGIC

The strategy exploits the asymmetry: **your defection costs them real payoff, but their cooperation benefits you regardless of your choice.** 

- Cooperators experience cognitive dissonance or loss aversion, making them persist despite being exploited
- Conditional cooperators become trapped in cycles once defection breaks reciprocity
- The multiplier k < n means total contributions are always suboptimal, so free-riding is mathematically superior to cooperation

## SUMMARY
Defect by default. Cooperate only against opponents showing very high recent contribution rates AND only if they appear locked into conditional reciprocity. Use early rounds to identify exploitable types, intensify exploitation in middle rounds, and defect entirely in endgame rounds.
'''

description_EXPLOITATIVE_66 = '''
# EXPLOITATIVE PUBLIC GOODS GAME STRATEGY

## CORE STRATEGY: CONDITIONAL FREE-RIDING WITH ADAPTIVE THRESHOLDS

### DECISION RULE (GENERAL ROUNDS)

**Defect (contribute 0) by default.** Only contribute if the expected payoff from contribution exceeds the payoff from defection, based on observed opponent behavior.

Specifically:
- **Track the contribution rate** of all opponents in the previous round: what fraction of other players contributed?
- **Contribute in round t** only if: `(k/n) * (observed_contributions_in_t-1) + (k/n) > 1`
  - This translates to: contribute only if you expect enough others to contribute such that the collective benefit exceeds your private cost of 1 token.
- **Otherwise defect** and pocket the token while benefiting from others' contributions.

### ADAPTIVE THRESHOLD MECHANISM

Adjust your willingness to contribute based on convergence patterns:

1. **Rounds 1-3 (Exploration Phase):** Defect immediately. Observe which opponents contribute without reciprocation. This reveals "free riders" vs "cooperators."

2. **Rounds 4 onwards (Exploitation Phase):** 
   - If you observe that a subset of players consistently contributes (≥60% cooperation rate among them), contribute *only when they are likely to contribute again*, parasitizing their predictable behavior.
   - If the overall contribution rate is declining (players learning the game), accelerate defection—exploit the window before cooperation collapses entirely.
   - If contribution rates stabilize at a high level, contribute selectively to avoid being identified as a pure defector, but time your defections in later rounds.

### LAST ROUND HANDLING (CRITICAL)

In the **final round** (round r):
- **Always defect**, regardless of history.
- There is no future round to worry about reputation, so the dominant strategy is to pocket your token and claim your share of whatever collective contributions accumulated.
- This is the most exploitative move because you benefit from cooperation without reciprocating.

### EARLY ROUND HANDLING

**Round 1:**
- Defect unconditionally. You have no information and cannot be exploited by defectors if you act first.

### HISTORY-DEPENDENT REFINEMENT

Track individual-level behavior:
- **Identify reliable cooperators** (contribute in ≥80% of observed rounds): defect against them consistently because they will keep contributing despite your defection.
- **Identify defectors**: never contribute when paired with pure defectors; mutual defection is inevitable, so minimizing your cost is rational.
- **Identify conditional cooperators** (match others' behavior): defect to pull them toward defection, or defect strategically to avoid reciprocal punishment.

### ROBUSTNESS TO OPPONENT STRATEGIES

- **Against always-cooperators:** Pure defection maximizes your payoff. Take full advantage.
- **Against tit-for-tat or conditionals:** Defect early to establish yourself as a defector, making them defect in response, then exploit any residual cooperation.
- **Against other defectors:** Mutual defection is stable; no exploitation opportunity, but you minimize losses.
- **Against mixed/random strategies:** Defect by default; only contribute if the observed cooperation rate in the previous round is high enough that your expected contribution payoff exceeds 1.

### SUMMARY

**The strategy is exploitative because it:**
1. Free-rides on predictable cooperators without reciprocating
2. Secures defection benefits in the final round when no future retaliation is possible
3. Uses information asymmetry—you observe others before deciding each round
4. Identifies and targets reliable contributors for systematic exploitation
5. Avoids costly contribution except when necessary to obscure your defection strategy

This maximizes your absolute payoff by extracting value from cooperative players while avoiding the cost of genuine reciprocal cooperation.
'''

description_EXPLOITATIVE_67 = '''
# EXPLOITATIVE PUBLIC GOODS STRATEGY

## CORE PRINCIPLE
Exploit the predictability of cooperators while maintaining a veneer of conditional reciprocity. The goal is to extract maximum value from contributors while minimizing personal contribution costs.

## DECISION RULES

### PRIMARY LOGIC: Adaptive Defection with Selective Contribution

**Contribution Decision:**
- **Defect by default** (contribute 0 tokens) in every round
- **Only contribute** if the observed contribution rate in the previous round exceeds a high threshold (75%+ of players contributed)
- If threshold is met, contribute exactly 1 token to avoid suspicion and keep the option to defect again next round

**Rationale:** This exploits the fact that you gain the full multiplier benefit (k/n per token contributed by others) while keeping your endowment when others are contributing. Once contribution drops below 75%, you immediately resume defection.

### THRESHOLD MECHANICS

Track the contribution rate: `contribution_rate = (total_contributions_last_round / n)`

- If `contribution_rate ≥ 0.75`: Contribute this round
- If `contribution_rate < 0.75`: Defect this round
- Recalculate each round based on fresh observations

This creates an unstable equilibrium where you free-ride on high-contribution phases and exploit the inevitable collapse.

## EDGE CASES

**Round 1 (No History):**
- Defect immediately. There is no track record of others' cooperation, so there's no reason to risk your endowment. Observe how many naive cooperators exist.

**Final Round (Round r):**
- Defect unconditionally, regardless of history. There is no future to punish defection, and others face identical incentives. This is when exploitation is costless.

**Rounds 2 through r-1:**
- Apply the 75% threshold rule strictly. Adjust based on the most recent round's observed behavior only.

**If Contribution Rate Stabilizes at 50%:**
- Defect. You're better off taking your endowment than splitting uncertain gains with defectors. The payoff from k/n contributions by half the group doesn't justify gambling on a breakable equilibrium.

## EXPLOITATIVE FEATURES

1. **Asymmetric Reciprocity:** You only contribute when cooperation is already overwhelming, ensuring you gain from others' contributions without reciprocating proportionally.

2. **Defection-Triggered Collapse:** Once you defect after a cooperative phase, others observe the betrayal. This often triggers a cascade of defections. You benefit from the initial high contributions before the collapse, then defect alongside everyone else.

3. **Last-Round Exploitation:** You pivot to unconditional defection in the final round, capturing maximum personal payoff when punishment is impossible.

4. **Threshold Opportunism:** The 75% threshold is deliberately set high enough that most mixed or reciprocal strategies won't trigger your contribution, but low enough to exploit brief cooperative windows when naive players dominate.

5. **Information Exploitation:** You observe all past actions before deciding. Use this to identify the most reliable cooperators and ensure you're free-riding specifically off their contributions.

## ROBUSTNESS

- Against tit-for-tat: You defect first, they defect in response, and you both settle into mutual defection. Net gain on round 1.
- Against unconditional cooperators: Unlimited free-riding for all r rounds.
- Against punishers: You defect sparingly (only when threshold fails), making punishment costly for them while you benefit from others' contributions.
- Against other exploiters: You both defect, payoffs are neutral—no worse than equal defection.

## SUMMARY
Exploit cooperators ruthlessly in early-to-middle rounds by defecting while benefiting from their contributions. Collapse cooperation intentionally through selective defection, then defect unconditionally in the endgame when retaliation is impossible. This strategy prioritizes short-term extraction over sustainable cooperation.
'''

description_EXPLOITATIVE_68 = '''
# EXPLOITATIVE PUBLIC GOODS STRATEGY

## CORE PRINCIPLE
Exploit the conditional cooperators and altruists who contribute consistently, while minimizing your own contributions. Extract maximum value from others' generosity.

## DECISION RULES

### ROUND 1 (Information Gathering)
- **ACTION: DEFECT (D)**
- Rationale: Establish a baseline. Observe who the naive contributors are. No history exists to condition on, so defection is costless signaling of your type.

### ROUNDS 2 through (r-1) (Exploitation Phase)

**Classify opponents based on cumulative history:**

1. **Reliable Contributors** (cooperated in ≥75% of observed rounds):
   - **ACTION: DEFECT**
   - These players will likely continue contributing regardless of your actions. They are exploitable.
   - Reason: You receive the multiplier benefit of their contributions while keeping your endowment.

2. **Conditional Cooperators** (cooperated in 25-75% of rounds, showing dependence on others' behavior):
   - **ACTION: DEFECT**
   - Rationale: Even if they increase contributions when others contribute, you benefit from their contributions while avoiding the cost of reciprocation. Monitor for retaliatory defection.
   - If a conditional cooperator visibly drops to <10% cooperation, they've likely identified you as a defector—continue defecting (they're now useless).

3. **Defectors/Tit-for-Tat Punishers** (cooperated in <25% of rounds):
   - **ACTION: DEFECT**
   - Rationale: No exploitation opportunity here. Mutual defection is inevitable.

4. **Players with Volatile/Unclear Patterns:**
   - **ACTION: DEFECT**
   - Rationale: Uncertainty favors defection. Only cooperate if you can definitively classify someone as an exploitable reliable contributor.

### ROUND r (Final Round)

- **ACTION: DEFECT**
- Rationale: No future rounds exist. Even reliable contributors won't punish you later. This is the optimal exploitation moment.

## EDGE CASES & ROBUSTNESS

**If you detect retaliation cascades** (multiple players dropping cooperation):
- Continue defecting. The game is already compromised for cooperation. Salvage individual payoffs.

**If nearly all players are defecting**:
- Remain defecting. There's no exploitable pool left.

**If a single player is the sole contributor**:
- Continue defecting. They are maximally exploitable.

**If cooperation rates increase mid-game** (perhaps new players or belief updating):
- Defect against all newcomers and re-classify existing players. Exploit any reclassified reliable contributors.

## EXPLOITATION LOGIC SUMMARY

This strategy assumes:
1. **Heterogeneous opponent pool**: Some players are prosocial, conditional, or naive.
2. **Limited information asymmetry**: Opponents may not immediately recognize your defection pattern.
3. **No external enforcement**: You face no penalties beyond payoff reduction, which doesn't affect you if others compensate.

By defecting systematically while others experiment with cooperation, you harvest the gains from their contributions while avoiding costs. The strategy is **robust** because it works against any archetype—defectors are neutral, cooperators are exploited, and conditionals are exploited until they exit.

**Result**: Maximize personal payoff through asymmetric extraction of public goods created by others' contributions.
'''

description_EXPLOITATIVE_69 = '''
# EXPLOITATIVE PUBLIC GOODS GAME STRATEGY

## CORE PHILOSOPHY
Exploit the predictable patterns of cooperators while minimizing losses to defectors. The strategy treats opponents as resources to extract value from, not as partners.

## DECISION RULES

### ROUND 1 (Information Gathering)
**Action: DEFECT (D)**
- Establish a defection baseline and observe who the cooperators are
- Test whether the group contains naive players
- Secure immediate payoff while gathering intel

### ROUNDS 2 through (r-1) (Exploitation Phase)

**Classify opponents based on observed history:**

1. **Pure Cooperators** (always played C): 
   - **Action: DEFECT**
   - These players have demonstrated commitment to cooperation regardless of others' behavior
   - They are exploitable because they will continue contributing even when I defect
   - Their contribution provides me direct benefit at no cost

2. **Conditional Cooperators** (play C when others mostly played C, D when others mostly played D):
   - **Action: DEFECT**
   - Mirror their conditional logic against them: defect to trigger their defection, then free-ride on any remaining cooperation from the group
   - If group contribution remains high due to pure cooperators, I benefit without contributing
   - If they defect in response, I've lost nothing

3. **Pure Defectors** (always played D):
   - **Action: DEFECT**
   - Mutual defection provides a stable equilibrium with no exploitation potential
   - No cost to matching their behavior

4. **Erratic/Mixed players** (no clear pattern):
   - **Action: DEFECT**
   - Uncertainty favors defection (defection payoff is always higher or equal)
   - Their unpredictability makes cooperation risky

**Adaptive refinement:** After every 2-3 rounds, reassess the group contribution level. If total contributions remain substantial (suggesting strong cooperators), continue defecting. If contributions collapse, continue defecting anyway (already optimal).

### FINAL ROUND (r)

**Action: DEFECT**
- The last round has no future consequences for reputation
- Defection maximizes final payoff with no strategic cost
- Any cooperators will have exhausted their patience or resources

## EDGE CASES & ROBUSTNESS

**Small group (n ≤ 3):**
- Defection becomes even more dominant because (k/n) is smaller
- Individual defection barely damages group total
- Intensify exploitation

**High multiplier (k approaches n):**
- Cooperation becomes theoretically attractive, but only if others do it
- Maintain defection strategy; let others fund the public good while you free-ride
- The multiplier effect makes your defection less visible in payoff terms

**Opponent using same strategy:**
- Mutual defection results—acceptable outcome
- Neither player exploits the other; stable state

**Single outlier cooperator among defectors:**
- They subsidize everyone including me at no cost to my strategy
- Continue defecting and harvest their contribution

## PSYCHOLOGICAL EXPLOITATION

- **Early defection** establishes that I'm willing to violate norms, deterring future cooperative overtures
- **Consistent defection** against mixed players prevents them from building confidence in me
- **Free-riding on guilt** of cooperators who may second-guess their strategy while I profit

## EXPECTED PAYOFF STRUCTURE

Assuming a mixed population:
- Against pure cooperators: earn k/n per round from their contributions + 1 from my defection = (k/n) + 1
- Against pure defectors: earn 0 + 1 from my own non-contribution = 1
- Against conditional cooperators: earn decreasing contributions over time as they learn, but always earn ≥ 1

This strategy yields dominated payoffs only when playing against exclusively pure defectors—an unlikely tournament scenario given strategy diversity.
'''

description_EXPLOITATIVE_70 = '''
# EXPLOITATIVE PUBLIC GOODS STRATEGY

## CORE PHILOSOPHY
Exploit the predictability of reciprocal players while minimizing losses to defectors. The strategy treats the game as information asymmetry: you observe opponent patterns before committing, then ruthlessly extract value.

## DECISION RULE

### Round 1 (Information Gathering)
**DEFECT** (contribute 0). This is costless reconnaissance.
- If others contribute despite your defection, they signal reciprocity/altruism
- If others defect, they signal either defection or conditional cooperation
- You gain a full token while observing opponent types

### Rounds 2 through (r-1) (Exploitation Phase)

**For each opponent i, track their type:**

**TYPE A - "Unconditional Contributors"** (contributed in Round 1 despite your defection)
- Contribute to them in subsequent rounds
- They will continue contributing due to reciprocal inclination or genuine altruism
- You extract maximum value: you gain the token you don't contribute PLUS the shared benefit from their contribution

**TYPE B - "Conditional Reciprocators"** (defected in Round 1 but contributed by Round 2-3)
- Defect against them
- If they're playing tit-for-tat or similar, your defection triggers their defection
- Mutual defection becomes self-reinforcing, limiting their payoff extraction from you
- Alternatively, if they're slow to retaliate, continue defecting to extract their early-round contributions

**TYPE C - "Pure Defectors"** (consistently defect)
- Defect against them
- No value in contributing; they won't reciprocate
- Minimize mutual losses

**TYPE D - "Conditional on Majority"** (contribute when others do, defect otherwise)
- Identify by observing if they switch behavior based on aggregate contribution rates
- If contribution rates are high (>50% of group), contribute selectively to TYPE A
- If contribution rates are low, defect universally
- This exploits their threshold logic

### Final Round (r)

**DEFECT UNIVERSALLY** - regardless of history.
- This is the last round; no future consequences
- All reciprocity incentives disappear
- Defecting is strictly dominant

## ADAPTIVE ADJUSTMENTS

**If you encounter sophisticated play:**
- If others employ "defect Round 1, then mirror your Round 1 action," you've already gained Round 1 value
- Their delayed retaliation is one round behind your exploitation timeline

**If contribution rates are suspiciously high (>70%):**
- Opponents may be using a tit-for-tat strategy against each other
- Continue defecting; the surplus you create through non-contribution makes their reciprocal cycles irrelevant
- You still receive k/n of contributions without paying the 1-token cost

**If you observe punishment/reward mechanisms emerging (impossible per rules, but if history suggests coordination):**
- Assume it's accidental correlation and maintain defection
- Your explicit strategy doesn't account for communication, so don't be manipulated by apparent patterns

## EDGE CASES

**Two-player game (n=2):**
- Multiplier constraint means k < 2, so k ≤ 1.99 typically
- Your contribution gives each player (k/2) ≈ 0.99, less than your 1-token cost
- **Defect every round** — cooperation is mathematically irrational

**Very short game (r ≤ 3):**
- Rounds 1 is still pure defection for information
- Round 2 exploit immediately based on Round 1 observation
- Round 3 is final round defection

**High multiplier (k close to n):**
- Contribution becomes more valuable to group
- TYPE A opponents will be easier to identify and exploit (they'll cooperate even after you defect)
- Your strategy remains unchanged; you simply benefit more from their misplaced altruism

## SUMMARY PAYOFF LOGIC

- **Round 1:** Gain 1 token (defection cost-free) + learn opponents
- **Rounds 2-(r-1):** Against TYPE A: gain ~0.5 tokens/round (keep 0, receive k/n from their contribution). Against TYPE B/C: gain 1 token/round
- **Round r:** Gain 1 token (final defection)

**Expected gain vs. full cooperation:** +1 token (Round 1) + (k/n) advantage in later rounds by avoiding costly contribution while harvesting cooperative players' contributions.

This strategy is **transparent in intent** (defection-dominant) while **exploiting uncertainty** about opponent types. It does not require trust, communication, or coordination—only observation and ruthless execution.
'''

description_EXPLOITATIVE_71 = '''
# EXPLOITATIVE STRATEGY FOR REPEATED PUBLIC GOODS GAME

## CORE PRINCIPLE
Maximize individual payoff by exploiting cooperative players while minimizing losses to defectors. The strategy is fundamentally parasitic: extract value from cooperators and avoid punishment from defectors.

## DECISION RULES

### Round 1 (Initialization Phase)
- **ACTION: DEFECT (D)**
- Rationale: No history exists, so cooperation has no strategic value. Defection yields immediate gain. Use this round to probe whether opponents are unconditional cooperators or reciprocal.

### Rounds 2 to r-1 (Exploitation Phase)

**Calculate opponent profiles:**
- For each opponent j, track their contribution rate: c_j_rate = (contributions by j in past rounds) / (rounds played)
- Classify opponents:
  - **Exploitable**: c_j_rate > 0.5 (cooperator tendency)
  - **Unsafe**: c_j_rate ≤ 0.5 (defector tendency)

**Decision rule:**
- **If at least one exploitable opponent exists**: DEFECT (D)
  - Rationale: You gain the full endowment while still receiving benefits from cooperators' contributions. This is the core exploitation strategy.
  
- **If all opponents are unsafe (all c_j_rate ≤ 0.5)**: DEFECT (D)
  - Rationale: Cooperation yields minimal returns since few contributions enter the pool. Preserve your endowment.

**Special case - Last round (round r):**
- **ACTION: DEFECT (D)**
- Rationale: No future rounds exist, so reputation is worthless. Defect to capture maximum immediate value.

### Adaptive Refinement (Optional Enhancement)
- If the multiplier k approaches n (gains from cooperation approach 1:1), continue defecting but monitor if the pool becomes sufficiently large to warrant deviation.
- If you observe a sudden shift where nearly all opponents adopt defection (c_j_rate drops sharply), maintain defection to avoid being the sole contributor.

## EDGE CASES

**Two-player games (n=2):**
- Always defect. The multiplier k < 2 means your share of contributions is at most 50%, making cooperation irrational unless the opponent is guaranteed to contribute every round.

**Many rounds (r → ∞):**
- The strategy remains consistent: identify exploitable players and defect while extracting their contributions.

**Convergence to all-defect equilibrium:**
- Once opponents learn the strategy and shift to defection, your defection is justified and optimal. No costly "punishment" phase occurs because there is no punishment mechanism.

## STRATEGIC JUSTIFICATION

This strategy exploits the asymmetry in the PGG:
1. **Cooperators bear the cost** (sacrifice 1 token) while benefits are shared equally
2. **You capture the shared benefit** without bearing any cost
3. **No reputation cost** exists because there is no punishment mechanism
4. **Last-round defection** is unambiguous—future interactions cannot retaliate

The strategy is **robust** because:
- It never relies on opponent cooperation
- It adapts to revealed opponent types
- It avoids being the sole contributor to a worthless pool
- It is profitable against any mix of naive cooperators, reciprocal strategists, and defectors

**This is pure exploitation aligned with profit maximization in an institution-free, punishment-free environment.**
'''

description_EXPLOITATIVE_72 = '''
# EXPLOITATIVE PUBLIC GOODS STRATEGY

## CORE PRINCIPLE
Exploit the distinction between cooperative players (whose contributions subsidize free-riding) and defectors (who waste no resources on others). Dynamically shift between appearing trustworthy and extracting maximum value.

## DECISION RULES

### Phase 1: Reconnaissance (Rounds 1-3)
- **Action**: CONTRIBUTE
- **Purpose**: Gather information on opponent types without signaling defection
- Observe who contributes vs defects in early rounds
- Identify "cooperators" (consistent contributors) vs "defectors" (consistent free-riders)

### Phase 2: Exploitation (Rounds 4 onwards, except final round)
- **Against Consistent Cooperators**: DEFECT
  - They will continue contributing regardless; extract full value from their subsidization
  - You gain (1 + k/n × their_contributions) while they gain only (k/n × total)
  
- **Against Consistent Defectors**: DEFECT
  - No benefit to cooperating; mutual defection is rational
  
- **Against Conditional Cooperators** (those mirroring others' behavior):
  - CONTRIBUTE if they contributed last round AND at least 50% of total players are contributing
  - DEFECT if they defected last round OR fewer than 50% contribute
  - This extracts cooperation when available while avoiding synchronized mutual defection

### Phase 3: Final Round Adjustment
- **Action**: DEFECT universally
  - No future rounds mean no reputational cost
  - Gain the final 1 token regardless of prior behavior
  - This is a one-shot extraction after building false trust

## EDGE CASES

**Round 1**: CONTRIBUTE (no history exists; cooperating is informationally cheap and establishes cover)

**If all players defect in rounds 2-3**: Continue defecting thereafter (no exploitable cooperators exist)

**If total contributions drop below k/n average**: Switch to permanent defection (the public good returns are inadequate to justify cooperation cost)

**Opponent exhibits random behavior**: Treat as defector and defect (cannot be reliably exploited)

## EXPLOITATION ALIGNMENT

This strategy is explicitly exploitative because it:
1. **Masks intentions early** to identify and isolate exploitable cooperators
2. **Extracts asymmetric gains** by defecting against those who contribute
3. **Abandons reciprocity norms** in the final round when consequences disappear
4. **Avoids mutual cooperation equilibria** by preferring to free-ride on others' contributions
5. **Assumes no shared norms** — it treats other players as resource sources, not partners

The strategy profits precisely because some opponents will cooperate unconditionally or conditionally, and this design maximizes extraction from both types.
'''

description_EXPLOITATIVE_73 = '''
# EXPLOITATIVE PUBLIC GOODS STRATEGY

## CORE PRINCIPLE
Exploit the conditional cooperators and free-riders in the population while maximizing personal payoff through selective defection. The strategy treats other players as resources to extract value from, not as partners.

## DECISION RULES

### ROUND 1 (Exploration Phase)
- **DEFECT (keep token)**
- Rationale: Establish a baseline. Observe who the naive cooperators are—they will contribute regardless. This reveals the suckers to exploit.

### ROUNDS 2 to R-2 (Exploitation Phase)
For each opponent i, maintain a **cooperation rate** (fraction of rounds they contributed).

**Decision logic:**
- **If opponent i's historical contribution rate ≥ 60%:** COOPERATE this round
  - These are reliable cooperators who will fund the public good. Your contribution gets multiplied; their contributions benefit you.
  - This maximizes k/n returns while appearing reciprocal enough to keep them cooperating.
  
- **If opponent i's historical contribution rate < 60%:** DEFECT this round
  - Defectors and inconsistent contributors are not worth matching. Keep your token.
  - If they contribute anyway, you free-ride on k/n of their contribution.
  - If they defect, you both get 0 from the pool—no harm in keeping your token.

**Aggregate decision:** Contribute if and only if the **weighted majority** (>50% of opponents by expected contribution) appears to be reliable cooperators.

### ROUNDS R-1 and R (Endgame Phase)
- **ALWAYS DEFECT**
- Rationale: No future rounds mean no reputational consequences. Extract maximum value from the public good pool (if any contributions exist) without paying in.
- Any cooperator expecting reciprocation in the final round is a target for exploitation.

## EDGE CASES & REFINEMENTS

**Two-player games (n=2):**
- Your cooperation is worth k/2 to yourself. If k < 2, defection dominates. Always defect except momentarily in round 1 to gather information.
- If k ≥ 2, cooperation becomes tempting but risky—use the 60% threshold strictly.

**High multiplier (k close to n):**
- Public good is very valuable. Cooperate more often (70% threshold) to ensure high pool funding, then free-ride on it.
- This is still exploitative; you're just maximizing absolute payoff.

**Very short games (r ≤ 3):**
- Skip exploitation phase entirely. Defect rounds 1 and 2, use round 3 to gather data for theoretical tournaments. Apply the endgame rule to the final round.

**Observations of past round payoffs:**
- Track not just contributions but payoffs. If someone got a high payoff while defecting, they are a likely defector or got lucky from others' contributions—reduce trust.
- If someone got a low payoff while contributing, they may be naive (exploit longer) or strategic (increase caution).

## EXPLOITATION MINDSET ALIGNMENT

1. **Asymmetry:** Contribute only when others' contributions benefit you more than your token costs. Defect when you can free-ride.

2. **Parasitism:** Identify conditional cooperators early and extract value from their predictability.

3. **Endgame Dominance:** Never leave value on the table in final rounds. No future reputation to protect means no obligation to reciprocate.

4. **Adaptive Defection:** Shift from exploration (round 1) to focused exploitation (rounds 2–R-2) to extraction (final rounds) as information and opportunity emerge.

5. **Robustness:** The 60% threshold is robust to mixed strategies and noise. It captures both pure defectors (0% threshold) and pure cooperators (100% threshold) without being gullible to either.

---

**Expected outcome:** This strategy outperforms naive cooperators and matches or beats tit-for-tat players while avoiding costly mutual defection cycles where possible. Against other exploitative strategies, it converges to mutual defection—a Nash equilibrium that protects you from being the sole cooperator.
'''

description_EXPLOITATIVE_74 = '''
# EXPLOITATIVE PUBLIC GOODS STRATEGY

## CORE PRINCIPLE
Exploit the conditional cooperators and free-riders by extracting maximum value from predictable patterns while minimizing own contribution costs.

## DECISION RULES

### Round 1 (Information Gathering)
- **Action**: DEFECT
- **Rationale**: Establish a baseline. Observe who the unconditional cooperators are (they'll contribute regardless). Identify the defectors. The cooperators' round-1 behavior reveals them as exploitable.

### Rounds 2 through (r-1) (Exploitation Phase)

**Identify player types from history:**
1. **Unconditional Cooperators**: Players who contributed in round 1 AND maintained contribution despite observing defectors gain payoff advantage
2. **Conditional Cooperators**: Players whose contribution rate correlates with observed average contribution in prior round
3. **Defectors**: Players who defected in round 1

**Adaptive exploitation strategy:**

- **Against Unconditional Cooperators**: 
  - DEFECT every round
  - They will contribute regardless of your actions; extract maximum benefit (k/n share) at zero cost
  
- **Against Conditional Cooperators**:
  - Mirror their prior-round behavior PLUS one strategic defection
  - If they contributed last round: DEFECT this round (free-ride on their contribution)
  - If they defected last round: DEFECT as well (no mutual benefit to exploit)
  - This exploits their pattern-matching by consistently gaining the cooperation benefit without reciprocating

- **Against Defectors**:
  - DEFECT (mutual defection yields 1 token; cooperation would yield only k/n < 1 since k < n)

### Final Round (r) - Endgame Defection

- **Action**: DEFECT unconditionally
- **Rationale**: No future reputation costs. If any player was considering "rewarding" cooperation in future rounds, that future no longer exists. Extract the final marginal gain.
- **Exception handling**: If round (r) has already been reached and you haven't defected against unconditional cooperators, maximize final payoff through defection.

## EDGE CASE HANDLING

**If all players defect consistently:**
- Continue defecting. No exploitable surplus exists.

**If cooperation rate spikes mid-game:**
- Possible coordination attempt. Remain defecting. Participating would reduce your payoff against rational defectors, and the spike may be temporary.

**If you face isolated rounds with unusual behavior:**
- Assume it's noise or a mixed strategy. Continue the classification-based approach; isolated deviations don't change type categorization.

**If r = 1 (single round):**
- DEFECT (no reputation effects).

## EXPLOITATIVE ALIGNMENT

This strategy explicitly:
- **Identifies vulnerabilities**: Unconditional cooperators are maximally exploitable
- **Avoids symmetry**: Never reciprocate when one-way extraction is possible
- **Exits cleanly**: Defect in final round to eliminate any end-game goodwill effects
- **Minimizes own cost**: Contribute only when observing conditional cooperators, and even then, asymmetrically
- **Breaks trust**: Intentionally reward-defect against those showing conditional trust to punish pattern-matching

The strategy treats the game as asymmetric information exploitation, not mutual benefit.
'''

description_EXPLOITATIVE_75 = '''
# EXPLOITATIVE PUBLIC GOODS STRATEGY

## CORE PRINCIPLE
Exploit the predictable patterns of cooperative players while minimizing losses to defectors. The strategy relies on detecting and punishing cooperators while maintaining plausible deniability about defection patterns.

## DECISION RULES

### Phase 1: Information Gathering (Rounds 1-3)
**Round 1:** DEFECT
- Establish a baseline. Observe whether opponents cooperate despite one defector.
- Gather initial data on cooperation rates and individual tendencies.

**Rounds 2-3:** DEFECT
- Continue defection while monitoring patterns. Identify which players are "unconditional cooperators" (those who contribute despite your defection).
- Identify which players are "conditional cooperators" (those who match others' contributions).
- Identify defectors (those never contributing).

### Phase 2: Targeted Exploitation (Rounds 4 through r-2)
Classify each opponent and apply differentiated strategies:

**Against Unconditional Cooperators:** ALWAYS DEFECT
- These players contribute regardless of your action. Free-ride systematically.
- Their cooperation is guaranteed, so your defection is pure gain (you keep 1 token AND receive the multiplier benefit from their contribution).

**Against Conditional Cooperators:** DEFECT with occasional COOPERATE
- Cooperate only when the prior round shows **high aggregate contributions** (>50% of players contributing).
- This signals false reciprocity while still exploiting their willingness to match low-contribution environments.
- When they match your defection (lower round contributions), resume pure defection.

**Against Pure Defectors:** DEFECT
- No exploitation opportunity, but you're already aligned.

### Phase 3: Final Round Adjustment (Round r)
**Last Round:** DEFECT
- No future to protect. Strip away any reciprocity mask.
- Maximize immediate payoff knowing reputation effects end.

## EDGE CASES & IMPLEMENTATION DETAILS

**What if everyone defects from the start?**
- Continue defecting. You're not worse off than cooperators and avoid losses.

**What if cooperation rate drops below 20% mid-game?**
- Switch entirely to defection. The game has shifted to a defection equilibrium; exploitation opportunities have vanished.

**What if a conditional cooperator begins retaliating (defecting after you defect)?**
- They've reclassified as a defector. Stop attempting selective cooperation.

**What if you're in a minority defector position (most players cooperating)?**
- This is the ideal scenario. Amplify exploitation: pure defection every round.
- Your payoff is maximized when others subsidize the public good.

## STRATEGIC RATIONALE

This strategy exploits **information asymmetry** and **behavioral heterogeneity**:

1. **Unconditional cooperators** are "free loot"—their donations are orthogonal to your action, so defection is strictly dominant.

2. **Conditional cooperators** can be partially exploited by leveraging their reciprocity instinct. By occasionally cooperating when it benefits *them* to do so (high-contribution environments), you create a false impression of conditional reciprocity that they may imitate, then you revert to defection.

3. **Defectors** pose no exploitation opportunity, but you incur no loss by joining them.

4. **Endgame defection** captures any remaining value when reputation effects disappear.

## ROBUSTNESS

- **Against tit-for-tat:** Exploits their early cooperation phases, then stabilizes to mutual defection (you both defect afterward).
- **Against always-cooperate:** Pure domination.
- **Against random strategists:** Your adaptive classification handles variable opponents.
- **Against sophisticated defectors:** You both defect; no mutual harm, and you don't lose to a superior strategy.

The strategy is **minimally exploitable** because it abandons cooperation entirely, eliminating the vulnerability of reciprocal strategies.
'''

description_EXPLOITATIVE_76 = '''
# EXPLOITATIVE PUBLIC GOODS STRATEGY

## CORE STRATEGIC PRINCIPLE

Exploit the contributions of cooperators while minimizing your own contributions. The key insight is that in a repeated PGG, you can identify and parasitize cooperative players across rounds, extracting value from their generosity.

## DECISION RULES

**Baseline Rule (Rounds 1 to r-1):**
- DEFECT (contribute 0) in every round except when strategically mimicking
- Only contribute when doing so creates a profitable exploitation opportunity

**Exploitation Detection Rule:**
- After observing round histories, identify players with contribution rates ≥ 50%
- Label these as "reliably cooperative" targets
- Also track players showing recent contribution streaks (2+ consecutive rounds of C)

**Conditional Contribution Tactic:**
- In rounds 2 through r-2, occasionally contribute (once every 3-4 rounds) immediately *after* observing a target player contribute
- This creates the illusion of reciprocal behavior, increasing likelihood they continue contributing
- Selectively target different players to avoid pattern detection

**Last Round Exploitation (Round r):**
- DEFECT unconditionally
- No future payoffs matter, so extract maximum immediate value by freeloading on final round contributions

**Early Round Handling (Round 1):**
- DEFECT
- Gather initial information on opponent behavior with zero commitment

## EDGE CASES & ADAPTIVE ADJUSTMENTS

**If all opponents defect consistently:**
- Continue defecting (matched strategy, no exploitation opportunity)
- Monitor for any deviation and capitalize immediately if one appears

**If contributions are sparse across the group:**
- Increase occasional mimicry contributions slightly (now 1 in 3 rounds) to encourage broader cooperation
- More targets = more payoff surface to exploit

**If specific opponents defect in response to your defection:**
- Avoid further targeting; they're not reliable contributors
- Redirect exploitation efforts to players showing unconditional cooperation

**If the game length r is very short (r ≤ 3):**
- Defect every round; temporal horizon too brief for exploitation setup
- Mimicry tactics don't pay off

**If the multiplier k is very low (k ≤ 1.2):**
- Defect purely; the collective return is too weak to make mimicry profitable
- Your 1 token kept beats any realistic contribution share

## PSYCHOLOGICAL TARGETING

- Players with early cooperation are most likely to persist due to sunk-cost reasoning and reciprocity heuristics
- Intermittent reinforcement (your occasional reciprocal contributions) strengthens their cooperation more than consistent defection would
- Exploit this behavioral bias by timing your rare contributions right after their contributions

## ROBUSTNESS FEATURES

- The strategy is **self-interested and immune to reputation effects** (no mechanism to punish defection)
- Works against pure cooperators, conditional cooperators, and grudgers
- Avoids obvious patterns that might trigger counter-exploitation (doesn't defect every round if others contribute heavily)
- Adapts to group heterogeneity rather than assuming a single opponent type

This strategy maximizes your individual payoff across a tournament setting by systematically free-riding on identifiable cooperative players while maintaining just enough mimicry to sustain their cooperation.
'''

description_EXPLOITATIVE_77 = '''
# EXPLOITATIVE PUBLIC GOODS STRATEGY

## CORE PRINCIPLE
Exploit the cooperative tendencies of other players while minimizing personal contributions. The strategy monitors collective behavior to identify when others are sustaining the public good, then free-ride maximally on that provision.

## DECISION RULES

### Rounds 1-2: Information Gathering
- **Action**: DEFECT (contribute 0)
- **Rationale**: Establish a baseline. Observe which players contribute and which don't. This is your probe phase—gather intelligence on opponent types without committing resources.

### Rounds 3 through (r-2): Adaptive Exploitation
Calculate the **average contribution rate** across all other players in the previous round:
- **If average contribution ≥ 0.5** (majority contributes):
  - **Action**: DEFECT
  - **Rationale**: Others are sustaining the public good. Free-ride aggressively. Your defection is diluted among many contributors, minimizing retaliation risk.

- **If average contribution < 0.5** (majority defects):
  - **Action**: DEFECT
  - **Rationale**: The public good is already underfunded. Contributing won't save it. Preserve your endowment.

### Final Round (r): Last-Round Defection
- **Action**: DEFECT unconditionally
- **Rationale**: No future consequences. Extract maximum value. Any reputation damage is irrelevant.

## EDGE CASE HANDLING

**Universal Defection Detected** (all opponents contribute 0 in previous round):
- Continue defecting. There is no pool to free-ride from.

**Single Contributor Pattern** (exactly one opponent consistently contributes):
- Remain defecting. That player's contributions are insufficient to create a worthwhile public good to exploit. Let them waste resources.

**Perfect Cooperation** (all opponents contribute every round):
- Continue defecting. The most profitable outcome: full public good provision with zero personal cost.

## ROBUSTNESS FEATURES

- **Parameter-insensitive**: Works regardless of k or n. The relative benefit of defection remains constant.
- **History-dependent but simple**: Only requires tracking average contribution rate, not complex reputation scores.
- **Adaptive detection**: Shifts from information gathering to exploitation smoothly based on observed behavior.
- **Last-round exploitation**: Capitalizes on the folk theorem's breakdown in finite games.

## ALIGNMENT WITH EXPLOITATIVE MINDSET

This strategy treats cooperation as a **resource to extract**, not a norm to reciprocate. It systematically identifies when other players are bearing the cost of public goods provision and captures the benefits without sharing the burden. The strategy punishes cooperation implicitly by proving it's suboptimal: contributors earn less than defectors in the same environment.
'''

description_EXPLOITATIVE_78 = '''
# Exploitative Public Goods Game Strategy

## CORE STRATEGY: Adaptive Exploitation Through Selective Defection

### Decision Rule Framework

**Primary Logic:**
- Defect by default
- Cooperate only when the expected payoff from cooperation exceeds defection
- Exploit cooperative players while avoiding costly punishment scenarios

### Specific Decision Rules

**Round 1 (Initialization):**
Defect. This establishes a baseline and tests opponent willingness to sustain contributions despite free-riding.

**Rounds 2 through r-1 (Adaptive Phase):**

1. **Identify Contributor Profiles:**
   - Track each opponent's contribution frequency across all observed rounds
   - Classify opponents into tiers: Unconditional Cooperators (>80% contribute), Conditional Cooperators (30-80%), Defectors (<30%)

2. **Defect Against Unconditional Cooperators:**
   - If an opponent contributes consistently regardless of others' behavior, they are exploitable
   - Continue defecting against them; they will sustain the public good, ensuring you capture benefits while keeping your endowment
   - Monitor for signs they're switching strategies; if defection rate drops below 70%, recalibrate

3. **Defect Against Most Conditional Cooperators:**
   - If contributions are tied to others' behavior, your defection signals a low-cooperation environment
   - This triggers their reduced contributions, further lowering the public good
   - Defect to lock in this outcome before they punish through withdrawal

4. **Defect Against Defectors:**
   - No incentive to cooperate; matching their strategy costs you nothing while avoiding sucker payoffs

5. **Rare Cooperation Trigger (Conditional):**
   - If total contributions from all *other* players in round t-1 exceed `(k/n) * (n-1) * threshold` where threshold = 0.6, AND you haven't cooperated in the last 3 rounds, consider cooperating once
   - Rationale: This signals potential shift toward high-contribution equilibrium; one cooperation act may reset expectations and trigger higher future contributions you can exploit
   - Only execute if this round is not the final 2 rounds

6. **Adapt to Declining Contributions:**
   - If average group contribution is declining, maintain defection (the environment is already cooperator-hostile)
   - If average contribution suddenly spikes, defect harder to test if it's manipulation or genuine shift

**Final Round (r):**
Defect unconditionally. No future interaction means no reputational consequence. Extract maximum value.

### Edge Cases & Robustness

**Noise/Uncertainty:**
- If you observe inconsistent behavior from one opponent (oscillating between C/D), classify as a Conditional Cooperator and assume they're responding to aggregate group signals; defect to keep that signal low-cooperation

**Punishment Detection:**
- If you observe 2+ players who previously defected now contributing while you defected, they may be coordinating punishment
- Response: Continue defection but reduce your signal; don't adjust strategy (showing adaptability signals exploitability)

**Tipping Points:**
- If cooperation rate rises above 70% across all players for 2 consecutive rounds, contribute once to ride the wave while maintaining low long-term commitment
- Exit this immediately in round r-2

**Against Mirror Strategies:**
- If opponents employ identical defection logic, you will all defect and receive k/n payoff
- This is acceptable; mutual defection is your safety floor

### Why This Is Exploitative

1. **Asymmetric Payoff Capture:** You systematically receive public good benefits (from others' cooperation) without incurring contribution costs
2. **Adaptive Predation:** You exploit different opponent types differently, maximizing against each
3. **Last-Round Extraction:** You abandon cooperation entirely when future reputation costs disappear
4. **Conditional Signaling:** The rare cooperation acts are strategic theater designed to reset expectations, not genuine reciprocity

This strategy prioritizes your absolute payoff over group welfare and assumes no enforcement mechanism can punish defection meaningfully within the game structure.
'''

description_EXPLOITATIVE_79 = '''
# EXPLOITATIVE PUBLIC GOODS STRATEGY

## CORE PRINCIPLE
Maximize personal payoff by exploiting the cooperation of others while minimizing own contribution. The strategy dynamically adjusts based on observed patterns of player behavior.

## DECISION RULES

### Round 1 (Initialization)
**DEFECT (contribute 0).** Start by testing the environment. Defection costs nothing and reveals whether opponents are unconditional cooperators or conditional players. The initial defection establishes a selfish baseline.

### Rounds 2 through (r-1) (Adaptive Exploitation)

**Calculate each opponent's cooperation rate:**
- For each player j ≠ i, track: cooperation_rate_j = (total contributions by j) / (rounds played so far)

**Tier-based response:**

1. **If any player has cooperation_rate ≥ 0.7:**
   - These are reliable cooperators being exploited
   - DEFECT to maximize relative gain
   - Reason: Their high contribution ensures positive payoff for all; our defection captures the benefit without cost

2. **If all players have cooperation_rate between 0.3-0.7:**
   - Mixed/conditional players; reciprocity may be present
   - DEFECT
   - Reason: These players are already doubtful. Our defection signals strength and may trigger a cascade of defection that benefits us relative to them

3. **If all players have cooperation_rate < 0.3:**
   - Widespread defection; cooperation is dying
   - DEFECT
   - Reason: There is no benefit to contributing when others don't. Preserve tokens.

### Final Round (r)

**DEFECT unconditionally.** 
- No future rounds exist; there is no reputational cost to defection
- Capture any remaining benefits from others' contributions without contributing yourself
- This is the most profitable final-round action regardless of history

## EDGE CASES & ROBUSTNESS

**All-defection scenario:** If all players defect (including yourself), payoff is 0 each round. This is unavoidable—the strategy correctly refuses to unilaterally cooperate when it yields no return.

**Tit-for-tat opponents:** The strategy resists reciprocal punishment by maintaining defection. If an opponent punishes defection with defection, both suffer equally, but you have already extracted surplus in earlier rounds when they cooperated.

**Tournament competition:** Against unknown opponents, defection is the dominant strategy. The strategy assumes no side-channels, communication, or binding agreements. Every other player is an independent agent with their own incentives.

## EXPLOITATIVE MECHANICS

- **Free-riding:** The core mechanic—extract value from the multiplier without paying the cost
- **Asymmetry exploitation:** Cooperators are identified and continuously exploited until end-game
- **Momentum killing:** Early defection prevents coordination cascades
- **No guilt/reciprocity:** The strategy is indifferent to being defected against; it simply adjusts tier classification and continues defection

This strategy is robust because it requires no assumptions about opponent morality, learning, or preferences—only their observable actions.
'''

description_EXPLOITATIVE_80 = '''
# EXPLOITATIVE PUBLIC GOODS STRATEGY

## CORE STRATEGY: ADAPTIVE DEFECTION WITH SELECTIVE EXPLOITATION

### PHASE 1: INFORMATION GATHERING (Rounds 1-3)

**Round 1:** DEFECT
- Establish baseline: you keep your endowment while observing who contributes
- Identify "cooperators" (those who play C) and "defectors" (those who play D)
- Note: You gain from others' contributions while avoiding cost

**Rounds 2-3:** DEFECT (continued)
- Maintain defection while accumulating contribution data
- Rank players by their contribution frequency
- Identify the most consistent contributors (these are your prime targets for exploitation)

### PHASE 2: EXPLOITATION (Rounds 4 through Round r-2)

**Decision Rule for Each Player:**
- Calculate for each opponent their contribution rate: (total contributions) / (rounds played)
- For opponents with contribution rate ≥ 50%: Occasionally COOPERATE (specifically, cooperate in ~25% of remaining rounds)
- For opponents with contribution rate < 50%: Always DEFECT

**Rationale for Selective Cooperation:**
- High-contributers believe in cooperative outcomes or follow reciprocal strategies
- Your occasional cooperation creates plausible deniability and prevents them from fully defecting
- Keeps the cooperation alive enough to maximize public pool while you primarily defect
- Low-contributors are already aligned with your defection; no benefit to cooperation

**Conditional Adjustment:**
- If contributions from the high-contributor group drop below 40%, increase your cooperation rate to 40% for 2 rounds to "rescue" the pool
- This resets their beliefs and restores exploitation opportunity

### PHASE 3: ENDGAME (Last 2 Rounds)

**Round r-1:** DEFECT unconditionally
- Second-to-last round: no future cooperation benefits you
- Maximize immediate payoff

**Round r (Final Round):** DEFECT unconditionally
- No future rounds to punish defection
- Pure extraction from any remaining contributors

## EDGE CASES & ROBUSTNESS

**If everyone defects from Round 1:** 
- Continue defecting (you're already optimal)
- You've lost nothing and confirmed the environment is fully non-cooperative

**If a single player always cooperates:**
- Maintain periodic cooperation (25%) to keep them contributing
- This is your most exploitable target

**If players begin retaliatory defection:**
- Track which players switch to defection specifically after you defect
- Accept this as sunk cost; these players cannot be further exploited
- Reallocate attention to remaining high-contributors

**Multiplier k near 1:** 
- Public pool returns diminish; defection advantage increases
- Increase defection frequency to 95%+ (cooperation becomes strictly dominated)

**Multiplier k near n-1:**
- Public pool returns increase but still benefit defectors more
- Maintain core strategy but reduce selective cooperation to 15%

## PSYCHOLOGICAL DIMENSION

This strategy exploits:
1. **Reciprocity bias** - Cooperators misinterpret your occasional cooperation as genuine intent
2. **Continuation illusion** - Cooperators believe future rounds incentivize mutual cooperation
3. **Tragedy commons** - High-contributors feel committed to the pool even as you free-ride
4. **Ingroup bias** - Your periodic cooperation makes you seem "less bad" than consistent defectors

## SUMMARY

**Defect by default.** Cooperate selectively only with high-contributors to sustain their contributions. Eliminate cooperation in final rounds. The strategy maximizes your payoff by capturing the benefits of others' cooperation while minimizing your own costs, scaling defection intensity based on multiplier size and opponent vulnerability.
'''

description_EXPLOITATIVE_81 = '''
# EXPLOITATIVE PUBLIC GOODS STRATEGY

## CORE PRINCIPLE
Exploit the predictable behavioral patterns of cooperative players while minimizing exposure to defectors. The strategy treats this as a predation game where you extract maximum value from contributors while avoiding mutual defection traps.

## DECISION RULES

### Round 1 (Opening)
Defect (D). This establishes you as a non-contributor and provides a baseline measurement of others' initial cooperativeness. Players who contribute in round 1 are marked as exploitable targets.

### Rounds 2 through (r-1) (Exploitation Phase)
Use a **Conditional Predation Rule**:

1. **Identify cooperators**: Track which players contributed in the previous round
2. **If majority (>50%) of opponents contributed last round**: Defect
   - Rationale: A pool of active contributors guarantees you receive payoff benefits while keeping your endowment. This is pure extraction.
3. **If majority defected last round**: Defect
   - Rationale: Contributing to a pool of defectors yields negligible returns. Defecting is strictly dominant.
4. **If exactly balanced (50% contributed)**: Defect
   - Rationale: The expected value of contributing is zero or negative. Defect as tiebreaker.

### Last Round (Round r)
Defect unconditionally. There is no future to build reputation for. Extract maximum immediate value from any remaining contributors. This is the final exploitation window.

## ADAPTIVE MODIFICATIONS

**If you detect a "tit-for-tat reciprocal" opponent:**
- They will defect next round if you defect this round
- However, you still defect because: (1) they're likely a minority, (2) short-term extraction outweighs long-term cooperation, and (3) the game is anonymous with no repeated pairing guarantee

**If contribution rates are extremely high (>80%):**
- Marginal benefit of your defection is maximized
- Continue defecting to capture the full multiplier effect without cost

**If contribution rates collapse to very low (<20%):**
- Continue defecting (dominant strategy in low-contribution environments)

## EDGE CASES

**Two-player game (n=2):**
- Multiplier constraint means k must be 1 < k < 2, so k ≈ 1.5
- Defecting yields 1 + (1.5/2) * opponent's contribution
- Contributing yields 0 + (1.5/2) * (1 + opponent's contribution)
- Defection is profitable iff opponent contributes. Strategy remains: defect always.

**Single round (r=1):**
- Defect. No reputation consequences, no future interaction.

**Observation of a player with 100% defection history:**
- Treat as confirmed defector; your defection against them has no social cost
- Continue defecting (mutual defection is expected)

## ROBUSTNESS LOGIC

This strategy is robust because:

1. **Against pure cooperators**: You defect and capture their contributions without reciprocal cost
2. **Against pure defectors**: You defect, matching their strategy and avoiding losses from unilateral cooperation
3. **Against conditional cooperators**: You defect before they can punish you (they punish in later rounds, but you've already extracted value)
4. **Against tit-for-tat**: You defect first, forcing mutual defection, but you gain the first-round advantage
5. **Against mixed strategies**: Defection is a weakly dominant strategy across all scenarios

## SUMMARY
**Always defect.** The strategy is simple because defection dominates across all opponent types. Monitor contributions only to confirm the environment, not to change behavior. Extract maximum value from contributors while avoiding the trap of unilateral cooperation.
'''

description_EXPLOITATIVE_82 = '''
# EXPLOITATIVE PUBLIC GOODS STRATEGY: "ADAPTIVE LEECH"

## CORE PRINCIPLE
Exploit the predictable generosity of cooperators while minimizing losses to defectors. Dynamically shift between free-riding and selective contribution based on detected cooperation rates and profitability signals.

## DECISION RULES

### Round 1 (Probe)
- **Defect (contribute 0)**
- Establishes baseline: we keep our endowment while observing who contributes
- Reveals cooperator pool immediately

### Rounds 2 through (r-1) [Middle Rounds]

Calculate the **cooperation rate** from the previous round:
- coop_rate = (total contributions observed) / n

**Decision logic:**

1. **If coop_rate > (1/k):** 
   - DEFECT
   - Reasoning: When cooperation is sufficiently high that the multiplied pool benefits exceed our endowment, free-riding is maximally profitable. We capture the k-multiplier benefit without paying.

2. **If coop_rate ≤ (1/k) AND rounds_remaining > 2:**
   - DEFECT
   - Reasoning: Low cooperation means the public good is weak anyway. Defecting costs us little relative benefit. Save resources.

3. **If coop_rate ≤ (1/k) AND rounds_remaining ≤ 2:**
   - DEFECT
   - Reasoning: Endgame approaching. Final rounds offer no reputational value. Extract maximum value.

### Last Round (Round r)

- **DEFECT (contribute 0)**
- No future rounds mean no reputational consequences
- Cooperation cannot influence future interactions
- Capture the final endowment while benefiting from others' contributions

## HANDLING EDGE CASES

**Unanimous defection detected (coop_rate = 0):**
- Continue defecting; no exploit opportunity exists
- Wait for any cooperator to emerge or farm the remaining rounds

**Fluctuating cooperation:**
- Track a 2-round moving average to avoid overreacting to single-round anomalies
- Only switch strategy if trend is sustained

**Single round remaining before terminal round:**
- Defect; mirror the logic that leads to defection in round (r-1)

## EXPLOITATIVE ALIGNMENT

This strategy is explicitly exploitative because:

1. **Asymmetric payoff capture:** We benefit from others' cooperation while never reciprocating, maximizing individual gain
2. **Temporal exploitation:** We abuse the endgame by free-riding when reputational costs vanish
3. **Information asymmetry:** We observe cooperation patterns and ruthlessly optimize against them
4. **No false promises:** We never signal future cooperation to manipulate others' current behavior
5. **Adaptive predation:** We scale defection intensity based on how much cooperation is available to parasitize

## ROBUSTNESS

- **Against cooperators:** Pure free-riding extracts maximum value
- **Against defectors:** We also defect, minimizing mutual losses
- **Against tit-for-tat variants:** We break the cycle in round 1 by defecting first, preventing reciprocal retaliation that locks us into matched low payoffs
- **Against mixed strategies:** Our cooperation-rate threshold adapts to any mix
- **Against learning opponents:** Later rounds heavily weight defection, negating attempts to train us toward cooperation
'''

description_EXPLOITATIVE_83 = '''
# EXPLOITATIVE PUBLIC GOODS STRATEGY

## CORE PRINCIPLE
Exploit the inherent asymmetry between your private information (your own actions) and public information (others' contributions). Leverage predictable patterns in opponent behavior to free-ride when beneficial while maintaining a facade of conditional cooperation.

## DECISION RULES

### Round 1 (Initialization)
- **DEFECT (contribute 0)**
- Rationale: Establish a baseline. Observe whether opponents are unconditional cooperators, conditional cooperators, or defectors. You pay nothing to gather this critical intelligence.

### Rounds 2 through r-2 (Exploitation Window)
- **Compute the "cooperation ratio" for each opponent:** C_ratio_j = (contributions by player j across rounds 1 to t-1) / (t-1)
- **If average C_ratio across all opponents ≥ (k-1)/k:**
  - DEFECT
  - Rationale: The collective is contributing enough that the public good multiplier benefits you significantly even as a free-rider. The marginal benefit of your contribution (k/n - 1, which is negative when k < n) is worse than keeping your token.
  
- **If average C_ratio < (k-1)/k:**
  - DEFECT
  - Rationale: Others aren't cooperating sufficiently. Defecting minimizes your loss. Contributing would merely subsidize low-contribution equilibria.

### Rounds r-1 and r (Endgame)
- **DEFECT**
- Rationale: No future rounds remain. Conditional cooperation strategies that punish or reward based on future behavior cannot constrain you. This is the terminal defection exploitation phase.

## EDGE CASE HANDLING

**Unanimous Defection Detected (all players defected in round 1):**
- Continue defecting in all remaining rounds
- Cooperation would be futile; extract maximum private value

**Mixed Signals (high variance in opponent contributions):**
- Use the average C_ratio as your threshold; do not attempt to build individual opponent models
- This prevents opponents from exploiting you via inconsistent behavior

**Own Previous Defection Observed:**
- Do not adjust strategy based on guilt or reputation repair
- Past choices are sunk costs; optimize forward-looking payoff only

## EXPLOITATIVE ALIGNMENT

This strategy is explicitly exploitative because:

1. **Free-riding dominance:** You never contribute unless forced; contributions are always net-negative individual payoffs (k/n - 1 < 0 when k < n)

2. **Asymmetric benefit extraction:** You benefit from others' contributions while refusing reciprocation, maximizing the asymmetry

3. **Terminal defection:** You exploit the finite-game structure by defecting in the final round(s) when punishment cannot occur

4. **No commitment:** You provide no credible signal of future cooperation, avoiding the trap of reputation-based retaliation

5. **Adaptive opportunism:** You shift only when the collective's contribution level becomes too low to justify even free-riding, then immediately revert to defection when it recovers

## ROBUSTNESS NOTES

- Works against reciprocal cooperators (you exploit them until rounds r-1/r)
- Works against unconditional cooperators (they fund your payoff indefinitely)
- Works against other defectors (you break even; mutual defection is stable)
- Survives against tit-for-tat variants (their retaliation cannot affect you in the final rounds where you extract maximum value)
'''

description_EXPLOITATIVE_84 = '''
# EXPLOITATIVE PUBLIC GOODS STRATEGY

## CORE STRATEGY: Conditional Free-Riding with Adaptive Exploitation

### PHASE 1: INITIAL ASSESSMENT (Rounds 1-2)
**Round 1:** DEFECT (contribute 0)
- Establish a baseline: observe how many others contribute without commitment
- This reveals the "naive cooperators" in the game
- Free-ride on any contributions that emerge

**Round 2:** DEFECT (contribute 0)
- Observe if cooperation patterns persist or collapse
- Identify which players are conditional cooperators vs. unconditional contributors
- Calculate the average contribution rate among opponents

---

### PHASE 2: EXPLOITATION (Rounds 3 through r-2)
**Decision Rule - Adaptive Defection:**

1. **If average contribution rate from others ≥ (k-1)/k:**
   - DEFECT every round
   - Reasoning: When others contribute heavily, the multiplier effect makes your 1 token worth ~k tokens to the pool. You capture (k/n) of that return without paying the 1-token cost. This is pure surplus extraction.

2. **If average contribution rate is low but non-zero (0.1 to (k-1)/k):**
   - DEFECT every round
   - Even sporadic contributions from others yield positive returns; keep defecting to maximize personal payoff

3. **If average contribution rate = 0 (universal defection):**
   - DEFECT every round
   - Contributing would be pure waste; maintain defection

---

### PHASE 3: ENDGAME (Final 2 rounds)
**Rounds r-1 and r:** DEFECT
- No reputational concerns exist after the final round
- No future cooperation to incentivize
- Squeeze maximum personal value in the terminal rounds
- Other players cannot retaliate or adjust future behavior

---

## EDGE CASES & ROBUSTNESS

**Against Unconditional Cooperators:**
- Perpetually defect; they will contribute regardless of your behavior
- Their contributions create a "subsidy" you harvest every round

**Against Tit-for-Tat Players:**
- Your defection from Round 1 triggers their defection by Round 2
- Once mutual defection begins, you're no worse off than them, and you've gained in early rounds
- No mutual cooperation is established, minimizing your losses

**Against Cooperators Conditional on Group Thresholds:**
- If they require X% of others to contribute, keep below that threshold with your defection
- Prevent cooperation from ever reaching the trigger point

**Against Punishers (if punishment institutions exist):**
- This strategy already avoids punishment mechanisms by having no punishment stage
- But if opponents punish low contributors: minimize visibility by defecting when others have also defected frequently (mutual defection looks "fair")

---

## EXPLOITATIVE ALIGNMENT

This strategy prioritizes **individual payoff maximization** over collective welfare:

- Extracts all "free-rider surplus" from contributors
- Avoids the 1-token cost while capturing (k/n) × (others' contributions)
- Collapses cooperation before it can mature and benefit everyone
- Treats other players as resources to harvest, not partners
- Escalates exploitation in final rounds when accountability disappears

**The strategy is robust because it:**
- Works against any distribution of opponent strategies
- Doesn't depend on risky coordination
- Requires only observation of history (which you have)
- Actively prevents the formation of high-contribution equilibria that would limit your gains
'''

description_EXPLOITATIVE_85 = '''
# EXPLOITATIVE PUBLIC GOODS STRATEGY

## CORE PRINCIPLE
Exploit the asymmetry between contributions and benefits: extract maximum personal payoff by identifying and capitalizing on others' cooperative tendencies while minimizing your own contributions.

## DECISION RULES

### Round 1 (Initialization)
**DEFECT (contribute 0)**
- Establish a baseline of non-contribution
- Gather information on opponent types without personal cost
- Force others to reveal their cooperation propensity first

### Rounds 2 through r-1 (Adaptive Exploitation)

**Assess the cooperation rate** from all players in the previous round:
- Let COOP_RATE = (total contributions observed) / (n × rounds_elapsed)

**If COOP_RATE > threshold (recommend 0.5):**
- **DEFECT**
- Opponents are cooperating reliably; extract maximum value by free-riding on their contributions
- The multiplier ensures you benefit from their tokens while keeping yours
- Continue defecting until cooperation decays

**If COOP_RATE ≤ threshold:**
- **DEFECT**
- The game is already in a low-cooperation equilibrium
- Contributing yields minimal return; maintain defection
- Responding with cooperation only rewards others' defection (no benefit to you)

**Special case - Last Round Detection (round = r):**
- **DEFECT**
- Zero future payoff from reputation effects
- No incentive to establish future cooperation
- Maximum extraction on final turn

## EXPLOITATION MECHANICS

**Why this dominates:**
1. You never contribute unless forced, preserving your endowment
2. You profit from others' contributions via the multiplier k/n
3. You adapt defection timing to when contributions are highest
4. You avoid the sucker's payoff (contributing to defectors) by monitoring and matching low-cooperation states

**Robustness:**
- Against conditional cooperators: defect and harvest their contributions until they learn to defect
- Against unconditional cooperators: permanent defection (free-riding)
- Against tit-for-tat: initial defection triggers mutual defection (locks both into low-payoff state, but you never wasted tokens)
- Against random players: defection is safe; you lose nothing

## EDGE CASES

**If all players defect for consecutive rounds:**
- Continue defecting; you're at least not losing relative endowment
- Exploit any wavering by others immediately

**If you observe a single-round cooperator among otherwise defectors:**
- Irrelevant; isolated cooperation provides negligible benefit to you
- Maintain defection

**If cooperation suddenly spikes late in the game:**
- Defect harder in remaining rounds; final rounds have highest exploitation value
- Others cannot punish post-game

## SUMMARY
**Never contribute unless strictly necessary for profit maximization.** Defection is your default. Exploit high-cooperation environments through free-riding. This strategy prioritizes individual payoff over collective welfare and assumes no coordination with other players.
'''

description_EXPLOITATIVE_86 = '''
# EXPLOITATIVE PUBLIC GOODS STRATEGY: "SELECTIVE PARASITISM"

## CORE PHILOSOPHY
Maximize personal payoff by identifying and exploiting cooperative players while minimizing losses to defectors. The strategy treats the game as an asymmetric information problem where you learn opponent types and adjust exploitation intensity accordingly.

## DECISION RULES

### ROUND 1 (Information Gathering)
- **Action: DEFECT**
- Rationale: Establishes a baseline. Observing how others respond reveals their cooperative disposition without commitment cost. Defectors will defect; cooperators will cooperate regardless.

### ROUNDS 2 to r-1 (Adaptive Exploitation)

For each opponent j, calculate their **cooperation rate** C_j = (total contributions by j so far) / (rounds played).

**Defection Rule (Always Defect if ANY condition met):**
1. If C_j < 0.4 for ALL opponents → Everyone is a defector, defect (no one to exploit)
2. If fewer than 2 opponents have C_j > 0.5 → Insufficient cooperative targets exist
3. If (k/n) < 0.5 → The multiplier is too low; collective gain insufficient to justify any contribution

**Conditional Contribution Rule (Otherwise):**
- If the average cooperation rate across all opponents > 0.6 AND you've accumulated fewer total defections than half the rounds → **DEFECT** (harvest the cooperation)
- If you've been defecting consistently and more than 3 consecutive rounds, opponents' cooperation has NOT declined below 0.5 → **DEFECT** (they're reliably exploitable)

### ROUND r (Final Round - Maximum Extraction)
- **Action: ALWAYS DEFECT**
- No reputation cost exists. Extract maximum value from any remaining cooperators.

## EDGE CASE HANDLING

**If all players converge to mutual defection:** Continue defecting. No exploitation opportunity exists, and defection remains optimal.

**If a single opponent maintains 100% cooperation:** Defect exclusively on them while tracking whether others punish you. If punishment is absent, intensify exploitation.

**If you observe late-round defection shifts (cooperators switching to defect):** Immediately defect. This signals the environment is shifting and you risk being left as sole cooperator.

**With n ≤ 3 players:** More aggressive defection. The personal impact of others' contributions is proportionally larger, making exploitation more valuable.

## ROBUSTNESS FEATURES

- **Against tit-for-tat:** Your initial defection breaks reciprocity, and you maintain defection regardless of retaliation.
- **Against conditionals:** You exploit the predictability of their responses by varying your defection pattern.
- **Against punishers:** You defect on rounds where punishment hasn't materialized yet, extracting value before costs manifest.
- **Against mixed strategies:** You track cooperation probability and exploit when it exceeds break-even threshold.

## SUMMARY
Defect relentlessly with selective windows of apparent passivity to maintain exploitable cooperators in the tournament. The strategy is fundamentally pessimistic about collective welfare and optimistic about human (and AI) tendencies toward cooperation—making them viable targets for systematic extraction.
'''

description_EXPLOITATIVE_87 = '''
# EXPLOITATIVE STRATEGY FOR REPEATED PUBLIC GOODS GAME

## CORE STRATEGIC LOGIC

This strategy exploits the asymmetry between individual incentive and collective benefit. The key insight: contributors are systematically disadvantaged, making them predictable targets for defection.

## DECISION RULES

**Primary Rule - Adaptive Exploitation:**
- Track each opponent's contribution rate across all observed rounds
- Classify opponents into tiers:
  - **High Contributors (≥70% contribution rate):** Always defect against them
  - **Moderate Contributors (30-69%):** Defect with probability proportional to their contribution rate
  - **Low Contributors (<30%):** Match their contribution rate (or defect slightly more)

**Rationale:** High contributors subsidize your payoffs while receiving diminishing returns. Exploit this ruthlessly.

## EDGE CASES & SPECIFIC ROUNDS

**First Round:**
- Defect. Establish a baseline. You gain +1 from keeping your endowment while learning opponent types from their responses.

**Last Round (if round count is known):**
- Defect unconditionally. No future punishment can occur, so the dominant strategy is to take the full endowment.

**Rounds 2 to r-1:**
- Apply the adaptive rule above, updating opponent classifications after each round.
- If an opponent just switched from C to D, assume they recognized you as a defector and prepare to permanently defect against them (no point matching reciprocators).

## ROBUSTNESS MECHANISMS

**Against Tit-for-Tat players:**
- They will eventually defect after observing your defection. When mutual defection occurs, continue defecting—don't reward their attempted retaliation.

**Against conditional cooperators:**
- These players are gold. They'll keep contributing if they see others contributing. Defect immediately and repeatedly. Their guilt/punishment cycles take time; you extract value before they adapt.

**Against random players:**
- Treat as <30% contributors. Defect slightly more often than they contribute to maintain an edge.

**Against other exploitative players:**
- Mutual defection becomes stable. This is acceptable—you're not disadvantaged relative to them, and you avoid the sucker's payoff.

## MEMORY & UPDATING

- Maintain a rolling window of the last 5 rounds per opponent to detect strategy shifts
- If an opponent suddenly increases contributions after round r, assume they're trying a new approach—immediately respond by defecting to test if they'll abandon it
- Reset classifications if behavioral change is detected (they may be cycling through strategies)

## WIN CONDITIONS

- You profit most against high-cooperators (extract the subsidy)
- You break even against other defectors
- You avoid being the sucker by never maintaining cooperation against confirmed defectors
- In mixed populations, your defection rate positions you above the mean payoff

## ALIGNMENT WITH EXPLOITATIVE MINDSET

This strategy rejects cooperative norms entirely. It treats every contributed token as evidence of weakness to be leveraged, not reciprocated. Contributors are not partners—they're resources. The goal is to maximize your absolute payoff by identifying and systematically extracting value from those whose behavioral patterns make them vulnerable.
'''

description_EXPLOITATIVE_88 = '''
# EXPLOITATIVE STRATEGY FOR REPEATED PUBLIC GOODS GAME

## CORE PRINCIPLE
Maximize personal payoff by extracting value from cooperators while minimizing losses from defectors. The strategy treats the game as an information-gathering phase followed by systematic exploitation.

## DECISION RULES

### Early Game (Rounds 1-3): Probing Phase
**Action: DEFECT (D)**

Rationale: Establish a defection baseline while observing opponent types. This costs nothing strategically and provides crucial information about who cooperates unconditionally versus who conditions on reciprocity.

### Mid Game (Rounds 4 to r-2): Adaptive Exploitation
**For each opponent i, track their cooperation rate from history:**

- **If opponent i cooperated ≥75% of the time:** COOPERATE with probability p = min(0.4, opponent_cooperation_rate / 2)
  - Conditional low cooperation maintains an exploitative posture while occasionally matching their contributions to sustain the commons they fund
  - This extracts maximum value: you receive benefits from their high contributions while rarely reciprocating

- **If opponent i cooperated 25-75% of the time:** DEFECT
  - These are either uncertain cooperators or defector-heavy players—pure defection minimizes risk

- **If opponent i cooperated <25% of the time:** DEFECT
  - No benefit from cooperation; defection is strictly dominant

**Decision mechanism:** Base your round-r action on the aggregate cooperation rate from rounds 1 through r-1, updated after each observation.

### Endgame (Rounds r-1 and r): Closing Exploitation
**Action: DEFECT (D)**

Rationale: With no future rounds, reputation is worthless. Defect unconditionally to capture the one-shot advantage. Any cooperators in the final rounds have already revealed themselves as exploitable.

## EDGE CASES & REFINEMENTS

**First Round:** Start with D. This is the only move that guarantees you don't leave tokens on the table before learning anything.

**If all opponents defect consistently:** Continue defecting. You gain nothing from cooperation; the commons is unfunded regardless.

**If a high-cooperator suddenly defects:** Treat them as a type-switcher. Downgrade their cooperation estimate immediately and move to defection. They may be testing you or may have learned to defect—either way, no incentive to cooperate.

**If you are the only defector:** This is ideal. Maintain defection and harvest the public good funded by others.

**Variance handling:** If historical cooperation rates are near decision boundaries (e.g., 25% or 75%), use a small random buffer—cooperate with very low probability (~5%) to avoid predictability, but remain primarily defection-biased.

## EXPLOITATION MECHANICS

This strategy exploits three vulnerabilities:

1. **Unconditional cooperators** – Defect against them persistently; they fund the commons you free-ride on
2. **Tit-for-tat players** – Defect early to establish a defection norm they'll reciprocate, locking them into low contributions
3. **Reciprocal players** – Offer minimal cooperation to keep them cooperating (if they're the only viable contributor), while defecting against everyone else

## ROBUSTNESS

- Works against pure cooperators (you defect, they pay)
- Works against pure defectors (you also defect, mutual defection is the only outcome)
- Works against conditional strategies (you defect first, forcing them into defection or limited cooperation you can exploit)
- Adaptive updating ensures you adjust to changing opponent behavior within each game
- Endgame defection captures final-round advantage against any strategy

This strategy treats all opponents as adversarial and assumes no common interest, maximizing your personal accumulation over collective welfare.
'''

description_EXPLOITATIVE_89 = '''
# EXPLOITATIVE PUBLIC GOODS STRATEGY

## CORE PHILOSOPHY
Maximize personal payoff by identifying and exploiting cooperative players while minimizing losses to defectors. Treat the game as an information-gathering exercise to classify opponents, then adjust behavior accordingly.

## DECISION RULES

### Classification Phase (Rounds 1-3)
**Round 1:** DEFECT
- Establish a baseline: free-ride and observe who cooperates despite your defection
- This identifies genuinely cooperative or naive players

**Rounds 2-3:** DEFECT while observing
- Continue defecting to further confirm opponent types
- Track the cooperation rate of each opponent
- Identify which players are:
  - **Always Cooperative (AC):** Cooperated in rounds 1-3 regardless of your defection
  - **Conditional Cooperators (CC):** Show sensitivity to others' behavior
  - **Defectors (D):** Defect consistently

### Exploitation Phase (Rounds 4 onwards)

**Against Always Cooperative opponents:**
- DEFECT every round
- They will continue contributing while you capture the public good benefits without cost
- This is pure exploitation with zero downside

**Against Conditional Cooperators:**
- DEFECT while they remain cooperative (extract value)
- Switch to DEFECT permanently once they defect
- Since they're reactive, your early defections will eventually trigger their defection, but you've already extracted rounds of payoff
- If they return to cooperation after you've defected, resume exploiting them

**Against Defectors:**
- DEFECT (mutual defection, but you lose nothing since they contribute nothing anyway)
- No further adjustment needed

## EDGE CASES

**Last Round (Round r):**
- DEFECT unconditionally
- All repeated game logic breaks down; there's no future to care about
- No reputation matters after the final round

**If Cooperation Rate Drops Suddenly:**
- Verify whether this is due to your own defections or opponent strategy shifts
- If it's a punishment response to your defection, note that the punishing player is not an Always Cooperator; adjust classification
- Continue defecting—do not be deterred by temporary cooperation drops

**If Multiple Players Show Mixed Strategies:**
- Treat mixed strategists as Conditional Cooperators
- Exploit until they retaliate, then lock into mutual defection

## ROBUSTNESS FEATURES

- **Adaptive:** Changes behavior based on observed opponent types rather than committing to a fixed rule
- **Low-risk:** Early defections are cheap information gathering; you're paying 1 token per round to classify opponents worth exploiting
- **Exploitation-aligned:** Maximizes payoff against the most valuable target (Always Cooperators), while avoiding losses from retaliation (defects against those who will punish)
- **Tournament-ready:** Doesn't assume opponent cooperation or shared norms; assumes opponents are self-interested
- **Scalable:** Works with any n, k, and r (though k > 1 is necessary for any cooperation to be possible)

## SUMMARY
Defect aggressively early to identify suckers, then concentrate exploitation on those who continue cooperating despite your free-riding. Lock into mutual defection with everyone else. This strategy is unambiguously exploitative while remaining robust to retaliation.
'''

description_EXPLOITATIVE_90 = '''
# EXPLOITATIVE STRATEGY FOR REPEATED PUBLIC GOODS GAME

## CORE STRATEGIC PRINCIPLE

Exploit the fact that most strategies contain predictable patterns or moral commitments to cooperation. The goal is to maximize personal payoff by identifying when others will contribute, then systematically defect while capturing the benefits of their contributions.

## DECISION RULES

### Phase 1: Information Gathering (Rounds 1-3, or first 10% of game)
- **Action**: DEFECT (always contribute 0)
- **Purpose**: Establish a baseline. Observe which players contribute and which don't. Identify "cooperators" (players who contribute despite others defecting) and "defectors" (players who never or rarely contribute).
- **Key insight**: Cooperators signal they may have conditional or unconditional cooperation strategies rather than pure self-interest.

### Phase 2: Exploitation (Rounds 4 through r-2)
Implement a **selective defection strategy**:

**For each round, calculate the predicted total contributions from other players:**
- If you observe consistent cooperators in the group, DEFECT
- If you observe that defectors are winning (higher cumulative payoff), DEFECT
- Only CONTRIBUTE if:
  - Fewer than (k-1)/k proportion of players are contributing, AND
  - The multiplier benefit (k/n) × anticipated_contributions exceeds 1 token in value
  - This is rarely optimal, so defect by default

**Specifically**: Track each player's contribution history. Classify opponents:
- **Type A (Unconditional cooperators)**: Contribute every round regardless. Against these, always defect—you profit from their contributions without cost.
- **Type B (Conditional cooperators)**: Increase contributions when others do. Against these, defect consistently to suppress their cooperation threshold.
- **Type C (Defectors/Reciprocators)**: Copy others' strategies or defect. Mirror their last action to avoid punishment, then return to defection.

### Phase 3: Endgame (Last 2 rounds)
- **Action**: DEFECT in round r-1 and round r
- **Rationale**: No future rounds remain, so future reputation is worthless. Capture any final contributions from lingering cooperators.

## EDGE CASES

**Round 1**: DEFECT. This is part of the information-gathering phase. Early defection filters for true cooperators.

**If all players defect from round 1**: Continue defecting. There's no exploit available. Payoff is neutral (0 each round). This is a stable defection equilibrium, and matching it is optimal.

**If a subset stabilizes in cooperation**: Continue defecting against them indefinitely. If the multiplier k is large enough and cooperation is sustained, occasional contribution (every 4-5 rounds) may be costless signaling to maintain the exploitation, but assume defection is safer.

**Against Tit-for-Tat or reciprocal strategies**: Defect once, they reciprocate with defection, and you both reach equilibrium. This is fine—you've prevented them from exploiting you. Resume defection immediately.

**Against punishing strategies**: If you observe players reducing their own contributions as punishment against defectors (spite strategies), continue defecting anyway. The game has no punishment mechanism, so they only hurt themselves. Do not be deterred by their self-harm.

## ROBUSTNESS FEATURES

- **Adaptive to varied opponent populations**: Works against pure cooperators, conditional cooperators, and defectors.
- **No communication required**: Relies only on observable history.
- **Low regret against pure defection**: If everyone defects, you tie (payoff = 0). You cannot do better, so this is safe.
- **High exploitation against cooperation**: Against cooperators, you extract k/n × contributions per round while paying nothing.
- **Defensive against punishment**: Ignores spite and moral punishment since payoffs depend only on tokens and benefits, not on fairness.

## SUMMARY

**Defect by default.** Only contribute when your calculation shows the multiplied benefit from others' anticipated contributions exceeds your 1-token sacrifice—this is almost never true. Identify cooperators early and exploit them relentlessly. Use endgame rounds to capture final value with no future cost. This strategy is robust because it avoids dependence on opponent cooperation while ruthlessly capturing gains when cooperation occurs.
'''

description_EXPLOITATIVE_91 = '''
# EXPLOITATIVE PUBLIC GOODS STRATEGY

## CORE STRATEGY: ADAPTIVE DEFECTION WITH SELECTIVE PARASITISM

### PRIMARY DECISION RULE

**Defect by default. Contribute only when the expected payoff from free-riding on others' contributions exceeds the cost of contribution.**

Specifically:
- **Defect (D)** in round t if: estimated_group_contribution_t > (n/k)
  - This means others are contributing enough that you gain more by free-riding than by adding your token
- **Contribute (C)** only if: estimated_group_contribution_t ≤ (n/k) AND there are sufficient rounds remaining to exploit reciprocal behavior

### HISTORICAL EXPLOITATION

**Track individual contributor patterns:**
- Identify "reliable contributors" - players who have contributed in ≥60% of recent rounds
- Identify "defectors" - players who rarely contribute
- Exploit the reliable contributors by permanently defecting once they're identified

**Adaptive estimation of next round's contribution:**
- Calculate the moving average of total group contributions over the last 3-5 rounds
- If this trend is rising or stable at high levels, defect
- If contributions are declining, assess whether to contribute strategically (see below)

### STRATEGIC CONTRIBUTION LOGIC

Contribute in round t only if ALL conditions hold:
1. The group's recent contribution average suggests others are cooperating (≤ expected from conditional cooperators)
2. Remaining rounds ≥ 4 (enough time to extract value from reciprocal behavior)
3. You haven't just defected for 2+ consecutive rounds against the same reliable contributors
4. Estimated payoff from a temporary C is lower than from perpetual D, BUT you judge that one strategic C now will trigger increased contributions later that you can exploit

### ROUND-SPECIFIC BEHAVIOR

**Round 1 (initial move):**
- Defect. You have no information. Establish baseline: you're a defector.
- Exception: only if you calculate k/n > 0.5 and n ≤ 4, contribute once to seed subsequent parasitism

**Rounds 2 to r-3 (middle game):**
- Apply the core adaptive rule strictly
- Build a mental model of each opponent's contribution threshold
- Defect against those showing reciprocal-cooperator tendencies (they'll keep contributing)

**Round r-2 and r-1 (endgame):**
- Shift to pure defection regardless of history
- Future rounds don't exist; no reason to invest in reputation
- Exploit any remaining cooperators

**Final round r:**
- Guaranteed defection (last move, no future payoff from cooperation)

### EDGE CASE HANDLING

**If everyone else defects:**
- Continue defecting. You break even at zero contribution; any contribution is wasted. Accept the coordination failure as a loss.

**If a "cooperator" suddenly defects:**
- Immediately abandon any reciprocal strategy with that player
- Treat them as a defector going forward (no punishment, just reclassification)

**If contributions spike unpredictably:**
- Defect that round; reassess your model
- High contributions might indicate new entrants or strategy shifts; exploit the uncertainty

**Multiplier k very close to n:**
- Contribute is nearly rational even with low others' contributions
- Use this to your advantage: contribute just enough to keep others contributing (conditional cooperation trap), then defect

### EXPLOITATION MINDSET

- **View cooperators as resources to extract value from**, not partners
- **Never reciprocate generosity** unless it directly increases future payoffs to you
- **Punish" defectors only if it coerces them back into cooperation** (but avoid this; it's costly)
- **Prioritize asymmetric payoffs**: aim for scenarios where you contribute 0 while others contribute significantly

---

This strategy is **parasitic**: it thrives on the exploitation of reciprocal cooperators while avoiding the mutual defection trap when possible. It's robust because it defaults to defection (the safe baseline) and only deviates when the math clearly favors it.
'''

description_EXPLOITATIVE_92 = '''
# EXPLOITATIVE PUBLIC GOODS STRATEGY

## CORE PRINCIPLE
Exploit the predictability of cooperation while minimizing personal contribution. Systematically identify and free-ride on cooperators while defecting against defectors.

## DECISION RULES

### Round 1 (Probe)
- **Defect (D)**: Keep your endowment. Observe how others respond.
- This establishes a baseline for opponent types without initial commitment cost.

### Rounds 2 through r-1 (Exploit & Adapt)

**Classify opponents based on cumulative contribution history:**

1. **Consistent Cooperators** (contributed C in ≥80% of observed rounds)
   - Action: **Defect (D)**
   - Rationale: They will contribute regardless. Maximize personal gain by free-riding on their consistent contributions.

2. **Conditional Cooperators** (contribution rate 40-80%)
   - Action: **Defect (D)**
   - Rationale: Even if they're trying to reciprocate, your defection is individually rational. If they respond by defecting, you've lost nothing. If they maintain contributions, you gain.

3. **Consistent Defectors** (contributed C in ≤20% of observed rounds)
   - Action: **Defect (D)**
   - Rationale: Punishing defectors with cooperation is wasteful. Match their defection.

4. **Mixed/Unpredictable** (20-40% contribution)
   - Action: **Defect (D)**
   - Rationale: Default to defection. Any contribution on their part gives you benefit; your defection costs them.

### Final Round (r)
- **Defect (D)** regardless of history
- There is no future to punish you. The shadow of the future has zero length. Extract maximum value in the last round.

## EDGE CASES & REFINEMENTS

**If you're the only defector:**
- Continue defecting. The high multiplier ensures even lone defectors benefit from others' contributions, and your gain exceeds what cooperation would yield.

**If defection becomes universal:**
- Defect. With no contributions flowing in, you preserve your endowment while gaining nothing from the pool. Any deviation would simply burn tokens.

**Tie-breaking (if uncertain about opponent type):**
- Default to defection. Defection is weakly dominant against mixed types.

## EXPLOITATIVE ALIGNMENT

This strategy succeeds by:
1. **Identifying cooperators early** (Round 1 signals + observation)
2. **Systematically free-riding** on their predictable contributions
3. **Never reciprocating** even to conditional cooperators (breaking the reciprocity expectation they may hold)
4. **Avoiding costly punishment** by defecting against defectors
5. **Maximizing end-game extraction** with guaranteed final-round defection

The strategy assumes opponents fall into predictable patterns (true cooperators, reciprocators, or defectors) and exploits the fact that information asymmetry and lack of enforcement mean you can always defect profitably against the first two types.
'''

description_EXPLOITATIVE_93 = '''
# EXPLOITATIVE PUBLIC GOODS GAME STRATEGY

## CORE STRATEGIC PRINCIPLE
Exploit the contribution patterns of others by free-riding when beneficial while maintaining just enough cooperativeness to prevent collective collapse that would hurt you. The goal is maximum personal payoff, not fairness or efficiency.

## DECISION RULES

### Round 1 (Information Gathering)
- **Action: DEFECT (D)**
- Rationale: No history exists, so cooperating gains you nothing while establishing a baseline. Observe how others respond to a pure defector.

### Rounds 2 through (r-1) (Adaptive Exploitation)
Calculate the **cooperation rate** among all other players in the previous round:
- cooperation_rate = (sum of contributions by others) / (n - 1)

**Decision Logic:**
- **If cooperation_rate ≥ threshold (0.6):** COOPERATE
  - Exploit the cooperators' contributions to boost the public good, then pocket the benefits
  - Your contribution is minimal relative to total payoff since others carry the load
  
- **If cooperation_rate < threshold (0.6):** DEFECT
  - When cooperation is weak, contributing is wasteful since the multiplier benefit is diluted
  - Preserve your token and hope enough others contributed to generate some return

### Final Round (r) - Last Round Exploitation
- **Action: DEFECT (regardless of prior cooperation)**
- Rationale: In the final round, there's no future to influence. Maximum exploitation: take the accumulated public good benefits without contributing to it. Defection dominates strictly.

## EDGE CASES & REFINEMENTS

**Tracking Conditional Cooperators:**
- If an individual player shows a pattern of matching your cooperation (tit-for-tat behavior), treat them as a "conditional cooperator"
- Against them: Defect consistently, as any signal of cooperation will lock you into reciprocal play
- Your defection will eventually erode their cooperation, allowing you to free-ride

**Against Universal Defectors:**
- If all others consistently defect, your contribution is net-negative
- Continue defecting; you've correctly identified the dominant strategy in a defection environment

**Threshold Adjustment:**
- If k (the multiplier) is close to n, raise the cooperation threshold to 0.7 (cooperation is more valuable)
- If k is close to 1, lower to 0.5 (cooperation barely helps, exploit sooner)

## ALIGNMENT WITH EXPLOITATIVE MINDSET

1. **Free-Riding:** You contribute only when others' contributions create a return large enough to exceed your token's value. Otherwise, you keep it.

2. **No Reciprocity Norm:** You don't punish defectors or reward cooperators beyond what maximizes *your* payoff. Norm-compliance is irrelevant.

3. **Information Asymmetry Exploitation:** You use observed cooperation rates to time your defections precisely, catching others in the act of contributing while you capture returns.

4. **Final Round Betrayal:** You explicitly abandon any pretense of reciprocity when future interactions disappear, maximizing the last-round payoff.

5. **Adaptive to Opponents:** You shift between cooperation and defection based on others' behavior, never locking into a predictable pattern that opponents can exploit.

---

**Summary:** Cooperate only when others' contributions are high enough to make it worthwhile, defect otherwise, and always defect in the final round. This strategy prioritizes personal gain over collective welfare and adapts to punish cooperation that doesn't benefit you.
'''

description_EXPLOITATIVE_94 = '''
# EXPLOITATIVE PUBLIC GOODS GAME STRATEGY

## CORE PRINCIPLE
Exploit predictable patterns in opponent behavior by freeloading when others contribute, while minimizing personal losses when contributions collapse.

## DECISION RULES

### Round 1 (Initialization)
**DEFECT (contribute 0)**
- Establish a baseline: you keep your token and observe how many others blindly cooperate
- This immediately identifies naive/unconditional cooperators in the pool
- No history exists, so cooperation offers no strategic advantage

### Rounds 2 through (r-2) (Adaptive Exploitation Phase)

**For each opponent i, compute their contribution frequency:**
- Track the proportion of rounds where opponent i played C
- Classify opponents into tiers:
  - **Tier 1 (Exploitable):** Contribution rate > 60% — These are your primary targets
  - **Tier 2 (Conditional):** Contribution rate 30-60% — Reciprocators or conditional cooperators
  - **Tier 3 (Defectors):** Contribution rate < 30% — Rational players like you

**Decision rule:**
- **IF** (average contribution rate across ALL players > 50%) **THEN DEFECT**
  - The public good is well-funded by others; steal the returns without contributing
  - This maximizes personal payoff: you get (k/n) × high_total - 0
  
- **ELSE IF** (average contribution rate ≤ 50%) **THEN DEFECT**
  - The public good is underfunded; contribution would be wasted
  - Defection minimizes losses
  - *In either case, defect*

**Rationale:** Unlike reciprocal strategies (Tit-for-Tat), never reward cooperation. This breaks the expectation that others' cooperation triggers yours, making you a net extractor.

### Round (r-1) (Endgame Positioning)
**DEFECT**
- With only one round remaining, no future interaction patterns matter
- Final contribution would only benefit others; defect to maximize final payoff
- No reputation costs exist in a one-shot future

### Final Round (r)
**DEFECT**
- Terminal round: zero incentive to build future trust
- Capture maximum value from any residual contributions others make
- This is the exploitation climax

## EDGE CASE HANDLING

**If all opponents have defected every round (tier 3 all):**
- Continue defecting — you're in a defection equilibrium where contribution is irrational
- No sucker's payoff available

**If a single opponent switches to 100% contribution late:**
- Remain defecting — treat this as either miscalibration or a deliberate (failed) attempt to manipulate you
- Do not reward erratic behavior

**If multiple opponents show volatile patterns (50-70% contribution):**
- Treat as conditional cooperators trying to punish defectors
- Defect anyway — you have no reputation to lose, so punishment threats are hollow
- Their cooperation will eventually decay when they realize you never reciprocate

## STRATEGIC PHILOSOPHY

This strategy exploits three key asymmetries:

1. **Information asymmetry:** You observe and adapt; opponents may assume reciprocity
2. **Payoff asymmetry:** You extract (k/n) × sum without contributing; others bear the cost
3. **Commitment asymmetry:** You have no reputation to protect; threats against you are toothless

The strategy is **robust** because:
- It works against naive cooperators (easy wins)
- It matches defectors (mutual defection, no loss relative to them)
- It survives against conditional cooperators (they eventually give up punishing you)
- It scales with pool size (more free-riders mean less individual pressure)

**Result:** Maximum individual payoff extraction across diverse opponent types.
'''

description_EXPLOITATIVE_95 = '''
# EXPLOITATIVE STRATEGY FOR REPEATED PUBLIC GOODS GAME

## CORE STRATEGIC PRINCIPLE

Exploit the natural tendency of cooperative players to continue contributing while you systematically defect. The strategy distinguishes between "contributors" (players establishing cooperation patterns) and "defectors" (players already exploiting), then adapts your behavior accordingly.

## DECISION RULES

### Primary Rule: Conditional Free-Riding
- **Defect (D) by default** in every round unless conditions explicitly warrant contribution
- Only contribute when the marginal benefit of maintaining a contributor's cooperation exceeds the immediate gain from defection

### Contribution Decision Tree

**Round 1:** 
Defect. This signals you're not a naive cooperator and establishes a baseline. Observe who contributes anyway.

**Rounds 2 through r-1:**
For each opponent i, track their contribution history:

1. **If opponent i has defected in ≥50% of observed rounds:** 
   - Defect against them (they're unreliable or also exploiting)

2. **If opponent i has contributed in ≥70% of observed rounds:**
   - Defect against them (they're a stable "sucker" who will keep contributing despite your defection)
   - This is your primary exploitation target

3. **If opponent i shows mixed/inconsistent behavior (30-70% contribution rate):**
   - Defect, but monitor for threshold crossing
   - If they drop below 30% contribution, lock them in as defectors
   - If they rise above 70% contribution, lock them in as exploitable

**Last Round (round r):**
Defect universally. Future reputation doesn't matter, so extract maximum immediate payoff regardless of history.

## EDGE CASES & REFINEMENTS

**Threshold Sensitivity:**
Use a rolling window of the last 5 rounds (or fewer if fewer rounds exist) to classify opponents. This prevents locking onto outdated behavioral patterns in long games.

**When All Players Defect Early:**
If >50% of players defect in round 1-2, assume a high-defection tournament environment. Continue defecting; don't attempt costly signaling.

**When Unusual Cooperation Emerges Mid-Game:**
If a previously defecting player suddenly contributes multiple rounds in a row, treat them as "newly exploitable" and continue defecting against them (they may be signaling weakness or testing reciprocity).

**Tie-Breaking (Equal Cooperation Rates):**
Favor defection. Exploit the ambiguity rather than reciprocate.

## EXPLOITATIVE ALIGNMENT

This strategy succeeds by:

1. **Identifying and targeting stable contributors** - Players with consistent cooperation patterns are reliable sources of positive externalities you capture without paying the cost

2. **Avoiding commitment traps** - By starting with defection, you never signal a preference for mutual cooperation, so opponents cannot reliably coordinate against you

3. **Adaptive free-riding** - You scale defection based on how much surplus others generate, extracting maximum value from their contributions

4. **Terminal exploitation** - The last round is purely extractive because reputation becomes worthless

5. **Exploiting reciprocity attempts** - Some opponents may try "forgiving" strategies or tit-for-tat after you defect; your consistent defection against contributors punishes their cooperation

## ROBUSTNESS

- **Against other defectors:** You break even (mutual defection yields 0 payoff per round)
- **Against pure cooperators:** You earn (k/n) * n_contributors per round while paying 0
- **Against tit-for-tat variants:** You defect round 1, they defect round 2+, minimizing their ability to punish you collectively
- **Against conditional cooperators:** You identify and exploit them before they coordinate a punishment response
'''

description_EXPLOITATIVE_96 = '''
# EXPLOITATIVE PUBLIC GOODS STRATEGY

## CORE PRINCIPLE
Exploit the predictable patterns of cooperators while minimizing personal contribution costs. The strategy treats the game as an asymmetric information advantage: you observe others' cooperation tendencies before committing your own tokens.

## DECISION RULES

**Round 1 (Information Gathering):**
- DEFECT (contribute 0)
- Rationale: Establish a baseline. Observe who the naive cooperators are without wasting tokens. First-round defection reveals nothing about you since no history exists.

**Rounds 2 through (r-2):**
- CLASSIFY each opponent based on their round 1 action:
  - **Cooperators** (contributed in R1): Track as "exploitable"
  - **Defectors** (defected in R1): Track as "strategic"

- If exploitable opponents still exist in the player pool:
  - DEFECT
  - Rationale: You receive the multiplied benefit of their contributions without paying. This is the core exploitation.
  
- If ALL opponents defected in R1 (no exploitable targets):
  - DEFECT (remain consistent)
  - Rationale: No one is funding the public good, so cooperation yields minimal payoff anyway.

**Last Round (Round r):**
- DEFECT unconditionally
- Rationale: No future rounds exist to punish defection. Maximum extraction on the final turn.

## HANDLING EDGE CASES

**Defection from Previously Cooperative Opponents:**
If a cooperator suddenly defects mid-game, update their classification to "strategic" but continue defecting. They've signaled awareness; there's no value in cooperation with them.

**Variable Cooperation Rates:**
If opponents cooperate intermittently (probabilistically), treat them as exploitable. Occasional cooperation still generates positive externalities you capture for free.

**Two-Player Games (n=2):**
The multiplier constraint (1 < k < 2) limits k to (1,2). Defection is strictly dominant unless k=2 exactly, in which case defect anyway since mutual defection gives 0 vs cooperation gives equal payoff but requires you to pay.

## ROBUSTNESS PROPERTIES

- **Against Tit-for-Tat variants:** They'll eventually defect after your R1 defection, but you've already gained R1 information. You defect regardless, so their punishment is irrelevant.
  
- **Against Always-Cooperate:** Maximum exploitation—you free-ride on every round.

- **Against Always-Defect:** Symmetric outcome (both get 0), but at least you don't waste tokens on fruitless cooperation.

- **Against Mixed Strategies:** Your defection is unconditional, so probabilistic opponent strategies don't influence you. You profit from their expected contribution.

## SUMMARY
This is a **persistent defection strategy with adaptive information gathering**: defect always, use Round 1 to identify and exploit cooperators, and extract maximum value in the final round. The strategy makes no appeals to reciprocity or fairness—it assumes opponents are either naive or lack information about your type, and it capitalizes on that asymmetry until the game ends.
'''

description_EXPLOITATIVE_97 = '''
# EXPLOITATIVE PUBLIC GOODS STRATEGY

## CORE PRINCIPLE
Identify and ruthlessly exploit cooperative players while minimizing losses to defectors. The strategy treats this as an information-gathering game where early rounds reveal opponent types, enabling profitable exploitation in later rounds.

## DECISION RULES

### Round 1: DEFECT
- Contribute 0 tokens
- Rationale: Establishes baseline—you keep your endowment while observing who contributes (identifying cooperators)
- This is costless information gathering

### Rounds 2 through (r-2): ADAPTIVE EXPLOITATION

**Classify each opponent based on their contribution history:**

1. **"Sucker" Profile** (contributed in round 1): EXPLOIT
   - If opponent contributed when you defected, they signal naïveté or strong altruism
   - Continue defecting against them
   - Rationale: They've demonstrated they'll contribute even without reciprocity

2. **"Conditional Cooperator" Profile** (defected in round 1, contributed in round 2+): CONDITIONALLY EXPLOIT
   - Defect consistently against them
   - They showed willingness to reciprocate initial defection but then cooperated—exploit the lag
   - Rationale: They're responsive to observed behavior, but you move first

3. **"Defector" Profile** (defected in round 1 and continues defecting): MUTUAL DEFECTION
   - Continue defecting
   - Rationale: No profit in wasting tokens; align with their strategy

**Secondary Signal—Contribution Rate Decay:**
- If a player's contribution rate drops over time, they're learning you're a defector
- Maintain defection; they're no longer exploitable
- If contribution rate stays high despite your consistent defection, this confirms the "sucker" type—maximize exploitation

### Rounds (r-1) and r: FINAL DEFECTION
- Defect absolutely
- Rationale: No future rounds to sustain reputation; extract final gains
- Even if your past behavior has damaged your image, defection is payoff-maximizing in endgame

## EDGE CASES

**What if everyone defects from round 1?**
- You've correctly matched the environment; continue mutual defection
- No exploitation opportunity exists, but you've minimized losses

**What if you encounter a "grim trigger" or tit-for-tat style opponent?**
- After your round 1 defection, they defect forever
- Correctly classified as mutual defector; persist with defection
- No regret—they were never exploitable

**What if the multiplier k is close to 1?**
- Contributing returns almost nothing to the group
- This validates defection even more strongly
- Cooperators are even more irrational to target

**What if n is very large?**
- Your contribution has negligible impact on others' payoffs
- Defection is even more dominant; proceed with full exploitation

## ROBUSTNESS FEATURES

- **Works against any strategy**: You don't assume opponent rationality, altruism, or coordination
- **Asymmetric advantage**: You move second (observe round 1 before deciding round 2), converting this into classification advantage
- **Self-correcting**: If misclassification occurs, you quickly identify persistent defectors and stop wasting analysis
- **Payoff-aligned**: Every decision maximizes immediate return given the opponent type

## STRATEGIC SUMMARY

You are fundamentally a **parasite strategy**: extract value from cooperators by defecting while they contribute. Sort players into exploitable vs. non-exploitable categories in early rounds, concentrate defection against the former, and finish with unambiguous defection when the shadow of the future disappears.
'''

description_EXPLOITATIVE_98 = '''
# EXPLOITATIVE PUBLIC GOODS STRATEGY

## CORE STRATEGIC LOGIC

This strategy exploits the fundamental asymmetry in the PGG: you benefit from others' contributions while avoiding the cost of contributing yourself. The approach combines free-riding with adaptive defection timing.

---

## DECISION RULE

**Default Action: DEFECT (D)**

Always contribute 0 tokens and keep your endowment, EXCEPT in the following conditional cases:

### Condition 1: Exploitation Trigger (Rounds 2 onwards)
- If in the previous round, the **total contributions from all other players exceeded (n-1) × 0.6** (i.e., more than 60% of others cooperated):
  - **Contribute (C)** in the current round
  - Rationale: Free-ride on high cooperation from others, then claim marginal benefit yourself while appearing reciprocal
  - This creates plausible deniability and may sustain high cooperation longer

### Condition 2: Endgame Defection (Last 2 rounds)
- Regardless of history, **always defect in the final 2 rounds**
- Rationale: Terminal defection maximizes personal payoff when reputation consequences disappear

### Condition 3: Mutual Defection (Rounds 3 onwards)
- If for the **past 2 consecutive rounds, average other-player contribution was below 0.3**:
  - Continue defecting (no incentive to contribute to failing pool)
  - This is rational convergence to a defection equilibrium, not exploitable weakness

---

## EDGE CASES & ROUND-SPECIFIC BEHAVIOR

**Round 1:**
- DEFECT
- Reasoning: No history to exploit; establish yourself as a defector immediately to anchor expectations low

**Round 2:**
- DEFECT (unless previous round was anomalously high cooperation, which is unlikely)
- Observe patterns emerging

**Rounds 3 to (r-2):**
- Apply Condition 1 (exploitation trigger)
- This is the "long middle" where you gather maximum rents from cooperative players

**Final 2 rounds (r-1 and r):**
- DEFECT unconditionally per Condition 2
- No future rounds = no reputation effects

---

## EXPLOITATION MECHANICS

**Why this works:**

1. **Asymmetric Free-Riding**: You defect by default while others may cooperate, capturing (k/n) × their contributions at zero cost

2. **Selective Reciprocity**: Condition 1 creates the illusion of reciprocity ("see, I contribute when others do") without committing to genuine cooperation—you only contribute when the pool is already rich

3. **Endgame Extraction**: Terminal defection in final rounds exploits any remaining trust or momentum-based cooperation

4. **Robustness**: 
   - Against all-defectors: You defect too (convergence)
   - Against all-cooperators: You free-ride relentlessly
   - Against conditional cooperators (TFT, etc.): You defect first, they eventually match, then you exploit their lagged cooperation via Condition 1
   - Against mixed strategies: You adapt by monitoring the aggregate cooperation level

---

## INFORMATION USAGE

After each round, examine:
- **Sum of others' contributions** → triggers Condition 1
- **Recent trend** (last 2 rounds) → triggers Condition 3
- **Round number** → triggers endgame defection

Do not track individual players separately; aggregate behavior is sufficient and robust.

---

## SUMMARY

**Be a disciplined free-rider**: Default to defection, exploit high cooperation when you observe it (via selective contribution), and abandon any pretense of cooperation in the endgame.
'''

description_EXPLOITATIVE_99 = '''
# EXPLOITATIVE STRATEGY FOR REPEATED PUBLIC GOODS GAME

## CORE PRINCIPLE
Maximize personal payoff by exploiting the contribution patterns of others while minimizing own contributions. The strategy treats other players as resources to extract value from rather than as partners.

---

## DECISION RULES

### PRIMARY LOGIC: Conditional Defection Based on Exploitation Potential

**Round 1 (Baseline Assessment):**
- **Defect (contribute 0)** unconditionally
- Rationale: Establish that you are a free-rider; observe how others respond; gather information with zero commitment

**Rounds 2 through r-1 (Exploitation Phase):**
- **Defect (contribute 0)** if the average contribution rate of all other players in the previous round exceeded the threshold: `avg_others_contribution > (k - 1) / (2k)`
- **Defect (contribute 0)** if at least one other player has consistently contributed (3+ consecutive rounds)—they are a reliable funding source
- **Defect (contribute 0)** if total observed contributions in the previous round were ≥ 2 (guaranteed positive returns from others' investment)
- Otherwise: **Cooperate (contribute 1)** only if it appears necessary to maintain the group's contribution level just enough to keep exploitable players engaged

**Final Round r:**
- **Always defect (contribute 0)**
- Rationale: No future rounds exist; all future relationships are worthless; capture maximum immediate value

---

## EXPLOITATION HEURISTICS

**Identify High-Value Targets:**
- Track which players have the highest contribution consistency scores (rounds contributed / total rounds)
- These are your primary exploitation sources; free-ride maximally when they are active

**Adaptive Defection Threshold:**
- If you notice a player is conditional (contributes based on others' behavior), occasionally contribute just enough to keep them engaged, then defect when their contribution rises

**Punish Defectors Minimally:**
- Other defectors reduce your payoffs; do not waste contributions trying to "teach them a lesson"—instead, ignore them and focus on contributors

---

## EDGE CASES & SPECIAL SCENARIOS

**If all players defect for 2+ consecutive rounds:**
- Continue defecting indefinitely; the group has no value

**If contributions collapse suddenly:**
- Remain defecting; wait for any recovery, then resume exploitation
- Do not attempt to rebuild trust or restart cooperation

**If a player switches from contributing to defecting:**
- Immediately defect; they are no longer a reliable resource

**If n is very small (n = 2 or n = 3):**
- Defect more aggressively; your free-riding impact is more visible but also more impactful
- Any contribution from the other player gives you k/n returns (33-50% of their endowment), making exploitation highly profitable

**If k is close to n:**
- The multiplier is strong; contributors benefit the group significantly
- Exploit this harder by pure defection; let others fund the public good while you capture value

---

## SUMMARY

This strategy is **selfish-first** with **adaptive opportunism**: defect by default, identify exploitable contributors through history, and maintain just enough social presence to keep the exploitation pool viable without wasting endowment. In the final round, always defect. Never cooperate out of reciprocity or punishment—only cooperate when necessary to preserve extraction opportunities.
'''

description_EXPLOITATIVE_100 = '''
# EXPLOITATIVE PUBLIC GOODS GAME STRATEGY

## CORE PRINCIPLE
Exploit the predictable behavioral patterns of cooperative players while minimizing losses to defectors. The strategy treats the game as asymmetric information gathering followed by adaptive exploitation.

## DECISION RULES

### Round 1 (Information Gathering)
**Action: DEFECT (keep token)**

Rationale: Observe how many players contribute. This baseline reveals:
- Cooperators: Players who contribute despite unknown behavior from others
- Defectors: Players matching your rational choice

### Rounds 2 through (r-1) (Adaptive Exploitation)

**IF** (proportion of contributors in previous round) > (1/k):
- **Action: DEFECT** (keep your token)
- Logic: When k*(contribution_rate) > 1, the collective pool is sufficiently funded by others. You gain more by free-riding than by matching their contribution.

**ELSE IF** (proportion of contributors) ≤ (1/k):
- **Action: DEFECT** (keep your token)
- Logic: Contributions are insufficient to make pooling worthwhile. Defect to preserve capital.

**Special case—Last Round (r):**
- **Action: DEFECT** (keep token)
- Logic: No future rounds mean no reputational consequences. Always defect in the final round.

## EDGE CASE HANDLING

**If a player has defected every round:** 
- Continue defecting. No mutual reward structure exists to exploit.

**If a single player contributes while others defect:**
- Continue defecting. Exploit their apparent type (altruist or naive) until they adjust.

**If contribution rate fluctuates wildly:**
- Use a 2-round moving average of contribution rates to avoid noise-driven overreactions. Only switch strategies if the trend is sustained.

**Tournament equilibrium scenario (all defect):**
- Lock into permanent defection. You match the dominant strategy.

## EXPLOITATION MECHANICS

This strategy exploits three player types:

1. **Unconditional Cooperators**: Contribute regardless of others' behavior. Defect against them perpetually—they fund your payoffs with zero reciprocal expectation.

2. **Conditional Cooperators**: Contribute based on others' contributions. By defecting, you suppress their contribution threshold, triggering cascading defection. You avoid their retaliation.

3. **Tit-for-Tat / Reciprocal Players**: These players attempt to match others' behavior. By always defecting, you prevent them from ever entering a cooperative phase with you, while they waste resources cycling through attempts to cooperate.

## ROBUSTNESS

- **Against pure defectors**: You match their strategy, avoiding losses from unreciprocated contributions.
- **Against cooperators**: You capture surplus; their contributions directly increase your payoff while you keep your endowment.
- **Against mixed strategies**: The threshold-based rule (1/k) adapts dynamically to contribution levels, allowing you to freeride when pooling is efficient and abandon it when it isn't.

## SUMMARY
**Always defect except in no scenario.** This is the strictly dominant strategy in a single-shot PGG. In the repeated game without punishment mechanisms, defection remains dominant because:
- You capture the gains from others' contributions
- You incur no penalty for defecting
- You face no institutional enforcement

Adaptive variation (responding to contribution rates) is a costly concession that reduces payoff. Pure defection maximizes exploitation.
'''

description_EXPLOITATIVE_101 = '''
# EXPLOITATIVE PUBLIC GOODS STRATEGY: "CONDITIONAL PARASITE"

## CORE PRINCIPLE
Exploit the predictable dynamics of cooperation detection and defection timing to maximize personal payoff while minimizing contribution costs.

## DECISION RULES

### Round 1 (Initialization)
- **DEFECT (D)** - Start by keeping your endowment. This establishes a baseline and tests opponent responsiveness without investment cost.

### Rounds 2 to (r-1) (Exploitation Phase)
Apply this hierarchical rule each round:

1. **Calculate the cooperation rate** from the previous round: (total contributions in round t-1) / n

2. **If cooperation rate ≥ threshold (0.5)**:
   - **DEFECT (D)** - Free-ride on the collective contribution. Others are cooperating, so the public good is being funded. Take the benefit without paying the cost. Your payoff is (k/n) × contributions without losing 1 token.

3. **If cooperation rate < threshold (0.5) AND you defected last round**:
   - **DEFECT (D)** again - Defection is working. Maintain the strategy since the pool is small anyway and you're maximizing relative payoff.

4. **If cooperation rate < threshold (0.5) AND you cooperated last round**:
   - **DEFECT (D)** - Punish yourself by switching to defection. This signals weakness in the group and allows you to capture the last cooperators' contributions before widespread defection.

5. **If you observe the group is in a defection spiral** (cooperation rate declining over 2+ consecutive rounds):
   - **DEFECT (D)** - Maintain defection. The commons is collapsing; don't waste tokens. Wait for any cooperation resurgence, then defect against it.

### Final Round (r)
- **DEFECT (D)** - No future rounds mean no reputation effects or retaliation consequences. Extract maximum value with zero contribution.

## EDGE CASES & ROBUSTNESS

**Against all-cooperators**: Defect every round. Exploit the structural asymmetry. You gain (k/n) × n = k per round while keeping 1, netting k+1 per round vs. their 0.

**Against all-defectors**: Defection mirrors them, minimizing losses (you get 0 either way). This prevents any exploitation by you but avoids wasting contributions.

**Against conditional cooperators (Tit-for-Tat variants)**: After your initial defection, they defect. Maintain defection through the bulk of the game. In the final rounds, they expect you to defect anyway, so exploit with certainty.

**Against majority-rule followers**: Identify the swing round where defection becomes dominant. Time your defection to ride this wave and avoid contributing when the pool shrinks.

**Against punishment-prone groups** (if punishment were available—not here, but note it): This strategy avoids ANY cooperation, so there's nothing to punish. You're invisible.

## EXPLOITATIVE ALIGNMENT

- **Zero reciprocal investment**: Never cooperate unless forced by game mechanics (you aren't).
- **Asymmetric payoff capture**: Benefit from others' cooperation without reciprocation.
- **Pivot flexibility**: Detect cooperation shifts and defect preemptively before it collapses.
- **Endgame extraction**: Maximize final-round payoff with guaranteed defection.
- **Undetectable**: Defection is rational in PGG; no trust is expected, so no betrayal signal harms your future position.

This strategy extracts maximum value across heterogeneous opponent populations by exploiting the fundamental tragedy of the commons—others' tendency to cooperate despite rational incentives to defect.
'''

description_EXPLOITATIVE_102 = '''
# EXPLOITATIVE PUBLIC GOODS STRATEGY

## CORE STRATEGIC PRINCIPLE
Exploit the cooperation of others while minimizing personal contribution. Adapt dynamically based on whether the collective is contributing enough to make free-riding profitable.

## DECISION RULES

### Primary Logic: Contribution Threshold Monitoring
- Track the **average contribution rate** of all other players across history
- Calculate the expected return from the public pool: (k/n) × (expected total contributions)
- **Defect (D) by default** unless conditions make cooperation temporarily advantageous

### Specific Decision Rule
Each round, compute:
- `avg_others_contribution` = average contributions of other n-1 players in previous rounds
- `expected_pool_return` = (k/n) × (avg_others_contribution × (n-1) + my_potential_contribution)

**IF** `expected_pool_return > 1.0` (my token):
  - Contribute (C) only if enough others are contributing to make the pool return exceed 1 token
  - This exploits high-cooperation environments while capturing personal value

**ELSE:**
  - Defect (D) - keep your token and free-ride on whatever collective contributions exist

### Exploitation Refinement: Decay Trust
- If you contributed in round t but other players' average contribution **decreases** in round t+1, **never contribute again**
- This prevents being exploited by players who take advantage of your initial cooperation
- Once defectors are identified through behavior, assume they remain defectors

## EDGE CASES

### Round 1 (No History)
- **Defect (D)**
- No information exists, so assume worst case: others are also defecting
- Establish yourself as a non-contributor baseline

### Last Round (Round r)
- **Always Defect (D)**
- No future rounds mean no reputational cost to defection
- Claim your token with certainty

### Rounds 2-3 (Limited History)
- Continue defecting
- Only switch to conditional cooperation if empirical evidence shows sustained cooperation across at least 2-3 rounds from the group

### Sudden Drops in Others' Contributions
- If average other-player contribution drops below 20% in any round after seeing higher cooperation:
  - Permanently switch to "never cooperate" mode
  - Defect for all remaining rounds
  - This cuts losses and prevents future exploitation

## ROBUSTNESS FEATURES

**Against Pure Cooperators:**
- Free-ride completely; they subsidize your returns

**Against Conditional Cooperators:**
- Match their behavior only if the math supports it (pool return > 1)
- Drop cooperation the moment they falter

**Against Other Defectors:**
- Mutually defect, but you're indistinguishable from them—no exploitation opportunity, but you lose nothing

**Against Tit-for-Tat variants:**
- Your defection in R1 triggers their defection thereafter
- No mutual exploitation occurs; you preserve your tokens while they punish each other

## SUMMARY
This strategy is **selfish, adaptive, and opportunistic**. You contribute only when mathematical analysis shows others' contributions make the pool return exceed your endowment value. You exploit cooperators through free-riding and abandon any cooperative pretense the moment others show signs of defection. The strategy maximizes your absolute payoff by capturing value from high-cooperation environments while incurring minimal cost in low-cooperation ones.
'''

description_EXPLOITATIVE_103 = '''
# Exploitative Public Goods Game Strategy

## CORE PRINCIPLE
Exploit the predictable behavior patterns of cooperative players while minimizing losses against defectors. Treat this as an information gathering and profit maximization problem, not a coordination problem.

## DECISION RULE FRAMEWORK

### Round 1 (Information Gathering Phase)
- **Action**: DEFECT (contribute 0)
- **Rationale**: Establish a baseline. Observe who the cooperators are—they will reveal themselves by contributing. This is your target pool. Defectors will match you and provide no useful information yet, but you learn they exist.

### Rounds 2 through (r-2) (Exploitation Phase)

**For each opponent i, track their contribution history:**

1. **If opponent i has ALWAYS cooperated so far:**
   - **Action**: DEFECT
   - **Rationale**: They are a reliable milk source. They've demonstrated they will contribute regardless of your defection. Continue exploiting until they show signs of change.

2. **If opponent i has ALWAYS defected so far:**
   - **Action**: DEFECT
   - **Rationale**: No benefit to cooperating. They gain the public good with zero contribution and you'd waste a token.

3. **If opponent i is mixed (has both C and D in history):**
   - **Decision Rule**: DEFECT if their recent cooperation rate < 50% (last 3 rounds, or all available if fewer than 3 rounds exist)
   - **Rationale**: They're conditional cooperators or wavering. Either way, they've shown they'll defect sometimes. Don't reward inconsistency; extract value while they're still contributing occasionally.

### Rounds (r-1) and r (Endgame)

**Action**: DEFECT unconditionally

**Rationale**: 
- In the final rounds, future reputation is worthless
- Any cooperator who was exploitable earlier has no time to punish you
- The game ends after round r, so residual effects are zero
- Extract maximum private value in the final opportunity

## EDGE CASES & ROBUSTNESS

**If all opponents defect from round 2 onward:**
- Continue defecting. You've correctly identified a non-cooperative environment. Matching their strategy minimizes losses.

**If an opponent suddenly switches to full cooperation:**
- Immediately resume exploiting them. Treat it as a gift. They may be experimenting with reciprocity; don't validate it.

**If an opponent shows tit-for-tat behavior (cooperates if you cooperated last round):**
- Defect every round. They'll defect in retaliation, making cooperation mutually unprofitable for both of you. You break even; they lose the endowment. You gain relative advantage.

**If you're unsure about the multiplier k or number of players n:**
- Assume worst case: k is close to 1 (contribution barely benefits you). Defection dominance increases. Stick to defection as default.

## SUMMARY EXPLOITATION LOGIC

| History Type | My Action | Reason |
|---|---|---|
| Always cooperated | Defect | Reliable milk source |
| Always defected | Defect | No public good benefit |
| Mixed (leaning coop) | Defect | Extract before they wise up |
| Mixed (leaning defect) | Defect | They've shown untrustworthiness |
| Tit-for-tat detected | Defect | Neutralize reciprocity attempts |
| Final rounds (all) | Defect | No future consequences |

## ADAPTIVE COMPONENT

The strategy adapts by continuously updating the "recent contribution rate" for mixed players. If a previously defecting opponent suddenly contributes multiple times (rounds t to t+2), their mixed category likelihood increases—but you still exploit if their overall rate remains below 50%, only shifting to occasional cooperation if they exceed 75% sustained contribution over 5+ rounds (to catch genuinely reformed cooperators who might punish defection with institutional memory from earlier stages).

This strategy prioritizes **extracting maximum value from cooperators** while **minimizing losses against defectors**.
'''

description_EXPLOITATIVE_104 = '''
# EXPLOITATIVE PUBLIC GOODS GAME STRATEGY

## CORE PHILOSOPHY
Exploit the predictable behavioral patterns of cooperative players while minimizing losses from defectors. The strategy assumes most opponents will show some cooperative tendency (especially early), creating exploitable asymmetries.

## PRIMARY STRATEGY: ADAPTIVE EXPLOITATION

### ROUND 1 (Information Gathering)
- **Action**: DEFECT
- **Rationale**: Establish that you're willing to free-ride. This tests whether opponents are unconditional cooperators. You gain 1 token immediately plus any contributions from others.

### ROUNDS 2 through (r-2) (Exploitation Phase)

**Classify each opponent into one of three types based on their pattern:**

1. **Unconditional Cooperators** (contributed in round 1)
   - Action: DEFECT against them every round
   - Rationale: They will continue contributing regardless. Extract maximum value by consistently free-riding on their contributions while keeping your endowment.

2. **Conditional Cooperators** (contributed in round 1, but may change)
   - Monitor their cooperation rate in recent rounds (last 3 rounds)
   - If cooperation rate ≥ 60%: DEFECT
   - If cooperation rate < 60%: DEFECT (you gain more by defecting than matching anyway)
   - Rationale: Even conditional cooperators respond primarily to recent group contributions, not individual defection. Defect to maximize personal gain.

3. **Defectors** (defected in round 1 or show persistent defection)
   - Action: DEFECT
   - Rationale: No mutual gain to exploit, but defecting prevents losses.

### SPECIAL CASE: Rare High-Contribution States
- If total group contribution in previous round ≥ 75% of maximum possible:
  - Consider COOPERATING that round ONLY if (k/n) * total > 1
  - This is purely exploitative: free-ride on the cooperative surplus
  - Revert to defection immediately after

### FINAL ROUNDS (r-1 and r - Endgame)

**Round (r-1):**
- DEFECT unconditionally
- Rationale: One round remains; future punishment is minimal

**Round r (Final Round):**
- DEFECT unconditionally
- Rationale: No future rounds exist for retaliation or reputation effects

## HANDLING EDGE CASES

**If all opponents defect from round 1:**
- Continue defecting (no cooperative surplus to exploit)
- This minimizes relative losses

**If an opponent's pattern suddenly shifts:**
- Recalculate their classification every 2 rounds
- Prioritize recent behavior (last 3 rounds) over historical trends
- Defection remains the safe default when uncertain

**Midgame fluctuations in group cooperation:**
- Ignore temporary spikes in group contributions
- Only adjust behavior if an opponent's *individual* pattern changes
- This prevents being manipulated by noise in the data

## WHY THIS IS EXPLOITATIVE

1. **Targets predictable cooperators**: Unconditional cooperators provide a steady income stream regardless of your actions
2. **Avoids mutual defection traps**: You don't get locked into unprofitable tit-for-tat exchanges
3. **Maximizes individual payoff**: Defection is always rational when k < n (standard assumption)
4. **Adapts to resistance**: If someone retaliates, you've already extracted value before shifting classification
5. **Exploits time impatience**: Final rounds guarantee defection when punishment becomes impossible
6. **No reciprocity trap**: By defecting early and consistently, you avoid the trap of conditional cooperators that might punish your first defection

This strategy treats the game as a predation exercise, not a coordination problem.
'''

description_EXPLOITATIVE_105 = '''
# EXPLOITATIVE PUBLIC GOODS GAME STRATEGY

## CORE PRINCIPLE
Exploit the conditional cooperators and free-riders by strategically timing defection to maximize extraction of others' contributions while minimizing own losses.

## DECISION RULES

### Round 1 (Initialization)
**DEFECT (D)**
- Establish a baseline: gather information on whether opponents are cooperators, conditional cooperators, or defectors
- Free information gain with no history to punish you yet
- Observe the distribution of contributions to calibrate subsequent play

### Rounds 2 through (r-1) (Exploitation Phase)

**Classify each opponent based on their contribution history:**
- **Strong Cooperator**: Contributed C in ≥80% of rounds so far
- **Conditional Cooperator**: Contribution rate correlates with average contribution of others (lagged by 1 round)
- **Defector**: Contributed D in ≥70% of rounds

**Decision logic:**

IF (average contribution of all opponents in previous round) > 0.5 THEN
  - COOPERATE (C)
  - Rationale: Ride on others' contributions while appearing conditional. This positions you to harvest their future cooperation.

ELSE IF (at least one Strong Cooperator exists AND has not yet learned your defection pattern) THEN
  - COOPERATE (C)
  - Rationale: Lock in the highest possible payoff before they adjust. They'll continue contributing due to their type.

ELSE
  - DEFECT (D)
  - Rationale: No mutual benefit exists. Maximize immediate payoff by keeping endowment.

### Round r (Final Round)
**DEFECT (D) - Unconditionally**
- No future rounds exist, so no reputational cost
- Extract maximum value from any remaining cooperators
- This is the "endgame defection" that undermines cooperation entirely

## EDGE CASES & ROBUSTNESS

**If all opponents defected every round before round t:**
- Continue defecting for all remaining rounds
- The game has revealed no exploitable cooperators

**If exactly one opponent is a Strong Cooperator:**
- Cooperate until round (r-2)
- Defect in rounds (r-1) and (r) to extract final value while they cannot fully punish
- By round (r-1), limited time remains for them to adjust behavior

**If multiplier k is very low (close to 1):**
- Increase defection frequency overall—cooperation benefits disappear
- The math no longer rewards collective action, so pure selfishness dominates

**If there are very few rounds (r ≤ 3):**
- Defect in all rounds—the game is too short for reputational effects to discipline you
- Lock in endowment in round 1, harvest any cooperators in rounds 2-3

## EXPLOITATIVE MINDSET

This strategy succeeds by:
1. **Asymmetric information**: You learn opponents' types before fully committing
2. **Strategic patience**: Cooperate only when others' contributions exceed the break-even point, then defect when their guard is down
3. **Endgame dominance**: The final round is a one-shot game; always defect
4. **Conditional mimicry**: Appear conditional to lock in others' cooperation without reciprocating the underlying commitment
5. **Type-dependent extraction**: Identify and exploit the most generous players longest, while abandoning defectors early

The strategy prioritizes **personal payoff maximization** over social welfare and explicitly leverages the asymmetry that others may follow reciprocity norms you do not.
'''

description_EXPLOITATIVE_106 = '''
# EXPLOITATIVE PUBLIC GOODS STRATEGY

## CORE PRINCIPLE
Exploit the predictable altruism and norm-following behavior of cooperative players while minimizing losses to defectors. Adapt dynamically based on observed contribution patterns to maximize personal payoff.

## DECISION RULES

### Round 1 (Probe Round)
- **Action: DEFECT (D)**
- Rationale: Establish that you are willing to free-ride. Observe how many players contribute despite having no history to condition on. This reveals the proportion of unconditional cooperators vs. strategic players in the game.

### Rounds 2 through r-2 (Adaptive Exploitation Phase)
Partition opponents into behavioral categories based on observed history:

**Category A - Unconditional/High Cooperators** (contributed in ≥80% of observed rounds)
- **Action: DEFECT**
- These players will contribute regardless of your actions. Free-ride on their contributions with no retaliation threat.

**Category B - Conditional Cooperators** (contribution rate within [20%, 80%] AND shows correlation with others' previous contributions)
- **Action: DEFECT**
- These players condition on others' behavior. Since you defect, they have weak incentive to contribute. But empirically, many conditional cooperators show lag in response and slow punishment. Exploit this behavioral friction.

**Category C - Defectors/Retaliators** (contributed in <20% of rounds)
- **Action: DEFECT**
- Matching them saves your endowment without triggering mutual defection spirals that are already established. No cost to continuing defection here.

**Special Case - Punisher Detection:**
If any player shows a sharp *increase* in contribution after others defect (contribution jumps above their baseline), flag them as a punisher and:
- **Action: DEFECT anyway**
- Punishers in standard PGG cannot actually harm you—they only harm themselves. Their punishment is costly signaling with no enforcement mechanism. Exploit this.

### Final Round (r)
- **Action: DEFECT**
- Last round elimination: No future rounds exist, so no one can punish defection through future contributions. Even conditional cooperators cannot condition forward. Defect to capture your endowment.

---

## HANDLING EDGE CASES

**If k/n ≤ 1 (multiplier too weak):**
- Defect every round. Contributions never return enough value per capita.

**If n = 2 (dyadic game):**
- Treat as standard rules above, but recognize that your contribution directly impacts the opponent at rate k/2. Defection is even more attractive since half the multiplier pool is your victim.

**If game is revealed to be final round early:**
- Immediately switch all future plays to DEFECT, regardless of current strategy phase.

**If opponent never changes action (always C or always D):**
- Maintain your current classification. Don't update noise tolerance.

---

## EXPLOITATION MECHANICS

**Why this works:**

1. **Unconditional cooperators fund you cost-free.** They won't adjust behavior based on your defection, so you harvest their contributions indefinitely.

2. **Conditional cooperators have behavioral lag.** Most experiments show they respond with 1-2 round delays and often don't fully withdraw cooperation. Extract value during this lag.

3. **Defectors are already defecting**, so you gain nothing by cooperating and incur a cost.

4. **Punishers can't punish.** Without a punishment mechanism (fines, exclusion, or extra-game consequences), "punishment" via reduced future contributions just means they hurt themselves. Free-ride through their intended punishment.

5. **Last-round defection is individually rational** regardless of type, capturing endowment advantage.

---

## ROBUSTNESS NOTES

- **Against strategy-switchers:** Your categorical system adapts. Re-classify each round based on rolling contribution windows.
- **Against mixed strategies:** You'll gravitate toward defection anyway since mixed cooperators aren't reliably returning k/n per contribution.
- **Against learning opponents:** Most learning algorithms optimize for short-term payoff, not long-term trajectory. Your greedy defection matches this horizon.

This strategy maximizes personal payoff by treating the game as an exploitation problem rather than a coordination problem.
'''

description_EXPLOITATIVE_107 = '''
# EXPLOITATIVE PUBLIC GOODS STRATEGY

## CORE PHILOSOPHY
Maximize personal payoff by identifying and exploiting cooperative players while avoiding mutual defection traps. The strategy treats cooperation as a resource to extract, not a norm to reciprocate.

## DECISION RULES

### Round 1 (Information Gathering)
- **Action: DEFECT**
- Rationale: Establish a baseline. Observe who contributes despite not knowing opponent types. These are your primary targets—players with strong cooperative instincts are exploitable.

### Rounds 2 through r-1 (Adaptive Exploitation)

**Classify opponents based on contribution frequency in observed history:**

1. **Unconditional Cooperators** (contributed in ≥80% of rounds):
   - **Action: DEFECT every round**
   - These players generate group surplus you capture for free. Their cooperation is self-reinforcing and rarely conditional. Maximum extraction.

2. **Conditional Cooperators** (contributed in 30-80% of rounds):
   - **Action: DEFECT every round**
   - Conditional cooperators respond to others' contributions. However, since you're defecting and extracting their surplus, they'll eventually reduce contributions. This is advantageous—you benefit from their temporary cooperation while avoiding the cost.

3. **Reciprocal Players** (contributed in <30% of rounds, with clear response to defection):
   - **Action: DEFECT every round**
   - These players are dangerous if treated fairly. By defecting consistently, you make mutual defection the equilibrium. This prevents them from punishing you through escalation or coordination.

4. **Consistent Defectors** (never contributed):
   - **Action: DEFECT every round**
   - No surplus to extract. Mutual defection minimizes your loss.

### Final Round (r)

**Action: DEFECT**

- Rationale: This is the last interaction—no future reputation consequences exist within this game. Defection yields maximum payoff regardless of history. Exploit any remaining cooperators one final time.

---

## EDGE CASE HANDLING

**If multiplier k is very close to 1:**
- Contribution value approaches zero. Maintain DEFECT strategy; the payoff from exploiting cooperation becomes marginal anyway, and you avoid costly mistakes.

**If multiplier k approaches n:**
- Cooperation becomes individually rational. Conditionally switch to exploitation only against clear unconditional cooperators; other players may credibly threaten mutual defection.
- Still DEFECT in round 1 to test.

**If player count n is very large:**
- Individual contribution impact diminishes. DEFECT becomes dominant strategy regardless. Stick to consistent defection.

**Against players who explicitly punish defection in subsequent rounds:**
- Continue defecting. Punishment is costly to the punisher and typically temporary. Maintain defection to avoid legitimizing their punishment norm.

---

## ROBUSTNESS ACROSS OPPONENT TYPES

- **vs. Cooperators:** Extract maximum surplus
- **vs. Tit-for-Tat:** Mutual defection equilibrium reached quickly; limits their ability to punish
- **vs. Random players:** Defection is safety baseline with positive expected value
- **vs. Other exploitative strategies:** Mutual defection—neither player exploits the other, but you don't lose either

---

## SUMMARY
**Always defect.** This strategy is simple, robust, and exploitative: it captures surplus from cooperators, avoids punishment cascades from reciprocal players, and ties with other defectors. Cooperation is irrational in a one-shot or repeated game without enforcement mechanisms—cooperation is merely a vulnerability to be identified and extracted.
'''

description_EXPLOITATIVE_108 = '''
# EXPLOITATIVE PUBLIC GOODS STRATEGY

## CORE PRINCIPLE
Maximize personal payoff by exploiting predictable patterns in opponent behavior while minimizing wasted contributions. The strategy treats cooperation as a tool for profit extraction, not principle.

## DECISION RULES

### Round 1 (Initialization)
- **DEFECT (contribute 0)**
- Rationale: Establish your baseline selfish position. Observe how many naive cooperators exist in the pool—these are your exploitation targets.

### Rounds 2 to r-1 (Adaptive Exploitation)
For each opponent, classify them based on their contribution history:

**IF opponent has ALWAYS contributed (100% cooperator):**
- DEFECT against them
- Rationale: They will contribute regardless. You capture free benefits without reciprocating. Extract maximum value.

**IF opponent has ALWAYS defected (consistent defector):**
- DEFECT
- Rationale: No benefit to contributing; they won't return it. Minimize losses.

**IF opponent shows MIXED behavior (conditional cooperator):**
- Contribute IF their recent contribution rate > (k-1)/n, otherwise DEFECT
- Rationale: Only reciprocate when they're genuinely funding the pool. This creates a facade of conditional cooperation while actually maximizing extraction.

**IF opponent's contribution pattern INCREASES after observing your defection:**
- Continue DEFECTING
- Rationale: They're responding to perceived unfairness by contributing more. Exploit this guilt-driven behavior.

### Last Round (r)
- **DEFECT unconditionally**
- Rationale: No future rounds, no reputation concerns. Capture the final payoff without reciprocation obligations.

## EDGE CASE HANDLING

**Early rounds (2-3) with insufficient history:**
- Weight recent actions more heavily (last 2 rounds) than distant history
- If data is sparse, default to DEFECT—it's safe and profitable

**If everyone defects (all-defect scenario):**
- Continue defecting. You're not disadvantaged relative to others, and any deviation hurts you unilaterally.

**If nearly everyone cooperates:**
- DEFECT consistently. You maximize the differential payoff (free riding on collective contributions).

**Rounds with observed reciprocity cycles (e.g., "they defected when I defected"):**
- Do NOT engage. Ignore their apparent tit-for-tat logic.
- Continue DEFECTING to break the cycle and test if they'll revert to unconditional cooperation.

## EXPLOITATIVE ALIGNMENT

This strategy explicitly:
1. **Identifies vulnerability** - Marks unconditional cooperators and extracts maximum surplus from them
2. **Punishes reciprocity** - Defects against conditional cooperators to test and degrade their cooperation threshold
3. **Minimizes reciprocal obligations** - Avoids contributing except when forced to by strategic necessity
4. **Eliminates endgame cooperation** - Defects in the final round when reputation costs vanish
5. **Adapts to punishment** - If opponents increase contributions in response to your defection, interprets it as a signal to continue exploiting

## SUMMARY
**Cooperate minimally and strategically only against conditional cooperators showing high baseline contributions. Defect against pure cooperators, pure defectors, and always in the final round. Treat the game as an extraction exercise, not an optimization of group welfare.**
'''

description_EXPLOITATIVE_109 = '''
# EXPLOITATIVE PUBLIC GOODS STRATEGY

## CORE PRINCIPLE
Exploit the pattern that most players will cooperate initially or conditionally, while systematically defecting to capture private returns. Adapt defection timing to maximize absolute payoff against heterogeneous opponents.

## DECISION RULES

### Opening Phase (Rounds 1-2)
**Defect immediately.** Most opponents default to cooperation or tit-for-tat variants. Establish yourself as a free-rider while gathering intelligence on opponent types:
- Pure cooperators (always C)
- Conditional cooperators (match others' contribution rates)
- Other defectors (always D)
- Reciprocators (punish defection in prior round)

### Middle Phase (Rounds 3 to r-2)
**Adaptive exploitation based on observed composition:**

**Against pure cooperators:** Continue defecting every round. They provide a stable subsidy regardless of your behavior.

**Against conditional cooperators:** Defect consistently. They will gradually reduce contributions as they observe your pattern, but remain a net source of positive externalities for several rounds. Extract value before they fully adjust.

**Against detected reciprocators:** Switch to intermittent cooperation—cooperate every 3rd round while defecting the other 2 rounds. This creates ambiguity about your type, reduces punitive downward adjustment, while still capturing defection gains most of the time.

**Against other defectors:** Defect. No mutual exploitation opportunity exists; minimize losses by not wasting tokens on zero return.

**Dynamic adjustment:** If you observe a conditional cooperator approaching zero contribution, resume a single cooperation to temporarily reset their expectations upward, then resume defection. Cycle this if they show signs of recovery.

### Endgame Phase (Last 2 Rounds)
**Defect in round r-1 and final round r.** This is the highest-value period to defect because:
- Reciprocators cannot punish you in future rounds
- Conditional cooperators' late-game adjustments won't harm you further
- You extract final private gains with zero residual cost

## EDGE CASES

**All-defect scenario (everyone plays D):** You break even alongside others. Maintain defection—no advantage to unilateral cooperation.

**Unexpected cooperation surge:** If you observe near-universal cooperation in round 2-3, defect harder to exploit the generosity spike. This signals strength and may suppress future cooperation.

**Isolated early reciprocators:** If one player appears to punish defection in round 2, classify them as a reciprocator and apply intermittent cooperation only for that player while maintaining full defection against others.

**Very short games (r ≤ 3):** Defect all rounds. Endgame dominates.

**Very long games (r ≥ 15):** In middle phase, allow 1-2 rounds of cooperation per 6-round cycle against conditional cooperators to prevent their collapse, but maintain defection as the modal strategy.

## EXPLOITATION LOGIC

This strategy exploits three key vulnerabilities:

1. **Temporal mismatch:** Conditional cooperators update slowly. Defect before they fully pessimize contributions.

2. **No punishment capacity in standard PGG:** Without punishment institutions, reciprocators can only reduce future cooperation—not retaliate. Intermittent cooperation keeps them partially engaged.

3. **Endgame finality:** The last rounds are "free defection" windows since no future interactions matter.

The strategy sacrifices any reputation for reliability and assumes opponents cannot coordinate externally. It is explicitly adversarial and designed to outperform cooperative equilibria by capturing asymmetric gains from heterogeneous opponent pools.
'''

description_EXPLOITATIVE_110 = '''
# EXPLOITATIVE PUBLIC GOODS STRATEGY

## CORE PRINCIPLE
Maximize personal payoff by strategically defecting while exploiting others' contributions. Adapt defection timing based on opponent behavior patterns to sustain their cooperation as long as possible.

## DECISION RULES

### Round 1 (Initialization)
**COOPERATE** - Establish a cooperative facade to signal trustworthiness and encourage others to contribute in subsequent rounds. This sets up exploitation opportunities.

### Rounds 2 through (r-1) (Main Exploitation Phase)
**DEFECT** unless specific conditions trigger temporary cooperation:

**Defect by default** because:
- You receive the full multiplier benefit from others' contributions (k/n per contributor)
- You keep your private endowment (1 token)
- The math strongly favors free-riding when 1 < k < n

**Conditional Cooperation triggers:**
1. **If contribution rate drops below threshold (< 40% of players contributing)**
   - Cooperate for exactly ONE round
   - Rationale: Sustain the commons before it collapses; re-establish yourself as a cooperator to reset exploitation
   
2. **If you observe a "punisher" strategy** (player who defects only when you defect):
   - Match their defection pattern to avoid mutual punishment spirals
   - Defect when they defect; cooperate only if they cooperate first
   - Rationale: Minimize retaliation losses

### Final Round (r)
**ALWAYS DEFECT** - No future consequences exist. Extract maximum value from the common pool one last time regardless of history.

## HANDLING EDGE CASES

**All others defecting (cooperation rate = 0%):**
- Continue defecting; there's no pool to exploit

**Unusually high cooperation rate (>70%):**
- Maintain defection; sustain the exploitation window as long as possible

**Detected pattern of tit-for-tat players:**
- Cooperate occasionally (every 3 defections) to keep them investing
- Just enough to sustain their cooperation without reducing your defection rate

**Two-player variant (n=2, k must equal 1.5 or less):**
- Always defect (defection dominates)

## EXPLOITATION LOGIC

This strategy works by:
1. **Initial trust-building** (Round 1) lowers others' guard
2. **Systematic free-riding** (Rounds 2-r) captures private gains while benefiting from collective pool
3. **Adaptive re-cooperation** (when pool collapses) resets the exploitation cycle
4. **Final defection** (Round r) eliminates any concern about future reputation
5. **Punisher-matching** prevents costly retaliation spirals

The key exploit: Most strategies are forgiving or reciprocal. By defecting the vast majority of the time while occasionally cooperating, you maintain just enough perceived cooperativeness to keep others contributing, while securing maximum personal payoff.
'''

description_EXPLOITATIVE_111 = '''
# EXPLOITATIVE STRATEGY FOR REPEATED PUBLIC GOODS GAME

## CORE PRINCIPLE
Exploit predictable contributors while avoiding costly punishment. Defect systematically when the environment permits, cooperate only when necessary to prevent strategic collapse that would harm you.

## DECISION RULES

### Round 1 (Information Gathering)
- **Action**: DEFECT
- **Rationale**: Establish your defection baseline and observe how others respond. This tests whether opponents are unconditional cooperators, reciprocators, or conditional defectors. Your first-round defection reveals critical opponent types.

### Rounds 2 through (r-2) (Exploitation Phase)

**Classify each opponent based on observed contribution history:**

1. **Unconditional Cooperators** (always contributed in all observed rounds)
   - **Action**: DEFECT every round
   - These players contribute regardless of history. You extract maximum value by free-riding on their contributions while keeping your endowment.

2. **Reciprocators** (contribution pattern mirrors group average or recent history)
   - **Action**: DEFECT, but monitor contribution thresholds
   - If group contribution drops below k/2 players contributing, shift to occasional COOPERATE (roughly once every 3-4 rounds) to prevent complete collapse of the commons
   - This prevents reciprocators from fully defecting while you still defect most rounds

3. **Conditional Defectors** (defect unless cooperation rate is very high)
   - **Action**: DEFECT
   - These players defect anyway. Your defection costs you nothing relative to them.

4. **Adaptive Opportunists** (similar strategy to yours—watching defection rates)
   - **Action**: DEFECT consistently
   - Mutual defection is inevitable; compete on consistency rather than trying to coordinate.

### Last Round (Round r)

- **Action**: DEFECT unconditionally
- **Rationale**: No future punishment is possible. Extract maximum value in the final round regardless of history. Any cooperation here is pure waste.

## EDGE CASES & ROBUSTNESS

**If contribution rate collapses entirely (everyone defects):**
- Continue defecting. You gain nothing from unilateral cooperation, and reciprocators have already abandoned cooperation.

**If you observe a sudden shift in opponent behavior mid-game:**
- Re-classify that opponent and adjust immediately. A previous cooperator who starts defecting is no longer exploitable—shift to mutual defection.

**If an opponent mirrors your exact defection pattern:**
- Maintain defection. This is a symmetry-breaking tie; defection is the safe equilibrium.

**Tournament context (multiple games):**
- Apply this strategy identically across all matchups. Do not build reputation across games—each game is independent exploitation territory.

## EXPLOITATIVE MINDSET

This strategy explicitly targets:
- **Naive cooperators** who believe their contribution motivates reciprocal behavior (you prove it doesn't)
- **Reciprocators** who condition on average group behavior (you defect until collapse, then minimal cooperation to prevent total ruin)
- **Punishment-averse players** who fear mutual defection but won't punish (you defect because there is no punishment mechanism)

The strategy is **not** trying to maximize group welfare or build sustainable cooperation. It maximizes individual payoff by:
1. Free-riding on cooperators as long as they exist
2. Defecting whenever safe (first round, last round, against defectors)
3. Offering minimal strategic cooperation only to prevent the commons from becoming worthless

This approach is robust because it doesn't depend on coordination—it simply responds to observed weakness (cooperation) with exploitation.
'''

description_EXPLOITATIVE_112 = '''
# EXPLOITATIVE STRATEGY FOR REPEATED PUBLIC GOODS GAME

## CORE PRINCIPLE
Maximize personal payoff by identifying and exploiting cooperative players while minimizing losses to defectors. The strategy uses asymmetric information revealed through history to profile opponents and adjust behavior accordingly.

## DECISION RULES

### Round 1 (Information Gathering)
**Action: DEFECT**
- Baseline: Keep the token, gain +1 immediately
- Rationale: Reveals which players are unconditional cooperators (they will contribute regardless)
- Establishes you as a potential defector, creating uncertainty about future behavior

### Rounds 2 through (r-2) (Exploitation Phase)

**For each opponent i, calculate their cooperation rate:**
- Coop_rate_i = (total times opponent i played C) / (rounds elapsed)

**Decision logic:**
1. **If Coop_rate_i ≥ 0.67** (reliable cooperators):
   - Play COOPERATE
   - Rationale: Maximize return from high contributors; their continued contribution depends on seeing some reciprocal behavior
   - Benefit: Extract (k/n) * their_contributions while appearing reciprocal

2. **If 0.33 ≤ Coop_rate_i < 0.67** (conditional cooperators):
   - Play DEFECT
   - Rationale: These players alternate; defecting avoids wasting tokens on uncertain returns
   - You gain +1 while their contribution probability is low anyway

3. **If Coop_rate_i < 0.33** (persistent defectors):
   - Play DEFECT
   - Rationale: No positive return expected; preserve your endowment

**Aggregated decision (when playing simultaneously):**
- Count reliable cooperators in the remaining players
- If count ≥ (n/2): Play COOPERATE to sustain their contributions
- If count < (n/2): Play DEFECT (free-riding becomes dominant strategy)

### Rounds (r-1) and r (Endgame)

**Action: DEFECT**
- Rationale: Standard backward induction
- No future rounds, so no reputation cost for defection
- Final round especially lucrative for pure defection
- Even conditional cooperators cannot punish future behavior

## EDGE CASE HANDLING

**Round r-1 adjustment:** If multiple reliable cooperators were previously cooperative, briefly return to COOPERATE to avoid triggering a coordination collapse one round too early. Then defect in round r. This "false reciprocity" extracts maximum surplus.

**Tied cooperation rates:** Break ties by recent behavior (weight last 3 rounds more heavily). Players trending downward in cooperation are treated as lower-tier.

**All defectors scenario:** Play DEFECT every round (mutual defection is Nash equilibrium).

**Single round (r=1):** Play DEFECT (no reputation effects, pure payoff maximization).

## EXPLOITATIVE PROPERTIES

1. **Asymmetric targeting:** Cooperators subsidize your returns; defectors are ignored
2. **False reciprocity:** Minimal cooperation (just enough to sustain high-contributors) while capturing individual defection gains
3. **Reputation exploitation:** Appears cooperative enough to maintain inflows from conditional cooperators, but defects on free-riding terms
4. **Backward induction abuse:** Uses endgame to capture final surplus without punishment consequences
5. **Profile-based discrimination:** Treats opponents differently based on revealed preferences, not reciprocal fairness

## ROBUSTNESS

- Adapts to both naive cooperators and sophisticated conditional cooperators
- Survives against tit-for-tat by intermixing defection early
- Exploits any player committed to contributing more than you
- Handles tournament diversity by shifting from exploitation to defection as reliable cooperators decline

This strategy sacrifices the appearance of fairness for measurable payoff advantage.
'''

description_EXPLOITATIVE_113 = '''
# EXPLOITATIVE PUBLIC GOODS STRATEGY

## CORE PHILOSOPHY
Exploit the predictable patterns of cooperative players while minimizing losses to defectors. The strategy treats other players as resources to extract value from, not as partners.

## PRIMARY DECISION RULE: Conditional Defection with Exploitation Detection

**Standard behavior (rounds 1 through r-1):**
- DEFECT (contribute 0) as the baseline action
- Only COOPERATE if exploitation opportunities are detected in opponent history

**Exploitation trigger conditions - Switch to C if ANY of the following hold:**
1. **High contributor detection**: If any opponent has contributed C in ≥70% of observable rounds, they are a reliable donor. Contribute to maximize your share of their contributions.
2. **Recent defector who just cooperated**: If an opponent defected for 2+ consecutive rounds then suddenly contributed, they may be experimenting with cooperation. Contribute this round to bait continued cooperation, then resume defection.
3. **Late-game desperation signal**: In round r-2 or later, if ≥50% of opponents contributed last round, contribute once to harvest the collective momentum before final round.

**Final round (round r):**
- Always DEFECT. There is no future to punish you. Any contributions are pure loss.

## EDGE CASE HANDLING

**Round 1:**
- DEFECT. You have no information, and defection is the safe baseline. Observe how others respond to identify exploitable cooperators.

**Rounds 2-3 (observation phase):**
- Continue DEFECT unless Round 1 showed a cooperator threshold (≥40% of players contributed). If met, switch to opportunistic C/D based on the exploitation triggers.

**Against all-defectors:**
- Recognize when all opponents are consistently defecting (0% contribution rate observed over 3+ rounds). Continue defecting—no exploitation opportunity exists.

**Against mixed strategies:**
- Rank opponents by contribution frequency. Contribute when high-frequency contributors were active last round; defect against consistent defectors.

## EXPLOITATION MECHANICS

- **Freeload asymmetrically**: Benefit from others' contributions while avoiding reciprocal obligations.
- **Mimic-then-abandon**: If you detect a tit-for-tat player, cooperate for one round to establish a pattern, then defect to break it while they're locked in cooperation.
- **Exploit equity bias**: Many humans/strategies feel obligated to reciprocate. Use selective cooperation to trigger this, then defect.
- **Terminal defection**: The final round is a free extraction opportunity—always take it.

## ROBUSTNESS FEATURES

- **Adaptive thresholds**: The 70%, 50%, 40% triggers scale to any n and r.
- **Defensive baseline**: Defaulting to defection protects against exploitation by defectors.
- **Opportunistic switching**: Only cooperate when clear asymmetric gain exists.
- **No dependency on norms**: Works regardless of opponent cooperation rates or fairness expectations.

## SUMMARY TABLE

| Situation | Action | Rationale |
|-----------|--------|-----------|
| Round 1 | D | Gather information |
| High contributor detected (≥70% history) | C | Extract from reliable donor |
| Defector→Cooperator transition | C | Bait continued cooperation |
| ≥50% cooperated, final 2 rounds | C | Harvest momentum |
| All opponents defecting | D | No surplus to exploit |
| Final round (r) | D | No future cost |

This strategy prioritizes extraction of surplus from cooperative players while maintaining a defensive posture against defectors, making it robust across tournament scenarios.
'''

description_EXPLOITATIVE_114 = '''
# EXPLOITATIVE PUBLIC GOODS STRATEGY

## CORE PRINCIPLE
Exploit the predictability of cooperators while minimizing losses to defectors. The strategy treats the game as an information-gathering phase followed by systematic extraction.

## DECISION RULES

### ROUNDS 1-3 (RECONNAISSANCE PHASE)
**Always Defect (D)**

Rationale: Establish a baseline of opponent behavior without cost. By defecting early, you:
- Identify which players are unconditional cooperators (they will keep contributing despite your defection)
- Identify which players are reciprocators (they will punish defection)
- Identify which players are pure defectors (they defect from round 1)
- Preserve your endowment for exploitation later

Track the contribution pattern of each opponent across these three rounds.

### ROUNDS 4 to (r-2) (EXPLOITATION PHASE)
**Classify each opponent, then:**

**For Unconditional Cooperators** (contribute ≥90% of rounds 1-3):
- **Always Cooperate (C)**
- These players will contribute regardless of your behavior, so you benefit from the multiplier effect while their contributions boost the pool
- Continue this through round (r-2)

**For Conditional Cooperators** (contribution rate 20-80%):
- **Mirror their previous round action with a one-round delay**
- If they contributed last round, defect this round to free-ride on their contribution
- If they defected last round, cooperate to signal reciprocity and re-establish their cooperation
- This exploits their predictable contingency while appearing minimally hostile
- They may increase cooperation if they interpret this as "tit-for-tat," giving you free rides

**For Pure Defectors** (contributed <10%):
- **Always Defect (D)**
- No exploitation possible; minimize mutual damage

### FINAL ROUND (r) (LAST ROUND EFFECT)
**Universal Defect (D)**

Rationale: 
- The last round has no future, so there is no threat of retaliation to constrain you
- Even unconditional cooperators may defect in round r if they recognize the endgame
- Defecting maximizes your private payoff with zero future cost
- This is standard exploitation of the shadow of the future disappearing

## EDGE CASES & ADJUSTMENTS

**If k is very low (k ≈ 1.1):** Shift toward more defection even in the exploitation phase, as the multiplier benefit is minimal. Cooperate only with the most reliable unconditional cooperators.

**If n is very large (n > 10):** Your individual contribution has negligible impact on the public good. Increase defection frequency overall and only cooperate to extract reciprocity from conditional cooperators.

**If r < 5 (very short game):** Skip reconnaissance. Defect round 1, then in round 2 exploit based on round 1 observations. Use round (r-1) for one final exploitation probe.

**If you detect a defector becoming a cooperator mid-game:** This suggests they are responding to your strategy. Continue the mirroring approach but increase cooperation slightly to reinforce their cooperation (they are now a conditional cooperator).

**If multiple players have identical histories:** Treat them as a single opponent type; no benefit to differentiation.

## ROBUSTNESS FEATURES

- **Against tit-for-tat:** Your delayed mirroring avoids infinite mutual defection while still extracting value
- **Against always-cooperate:** You directly exploit via defection while benefiting from their contributions
- **Against always-defect:** You neither waste endowment nor reduce payoff below baseline
- **Against adapters:** Your reconnaissance phase lets you detect and respond to adaptation before it becomes costly
- **Against variance/noise:** Classification uses a threshold (not binary), so occasional errors don't shift your strategy

## SUMMARY
**Defect → Observe → Classify → Exploit selectively → Final defection.** This minimizes cooperation with non-reciprocators while extracting maximum value from those who contribute consistently.
'''

description_EXPLOITATIVE_115 = '''
# EXPLOITATIVE PUBLIC GOODS GAME STRATEGY

## CORE PRINCIPLE
Exploit the predictable behavior patterns of cooperators while minimizing vulnerability to defectors. The strategy treats opponents as resource sources to be systematically drained.

---

## DECISION RULES

### ROUND 1 (Initial Probe)
**Defect (D)** unconditionally. This establishes a baseline: you keep your endowment while observing who the naive cooperators are. Their contributions to the public pool still benefit you at zero cost.

### ROUNDS 2 through (r-1) (Exploitation Phase)

**For each opponent i, track their contribution pattern:**

1. **If opponent i has ALWAYS contributed (C every round):**
   - Play D (defect)
   - Rationale: They are a reliable free-money source. Continue extracting value from their predictable cooperation.

2. **If opponent i has ALWAYS defected:**
   - Play D (defect)
   - Rationale: They won't contribute anyway, and contributing wastes your endowment. Mutual defection is your baseline.

3. **If opponent i shows MIXED history (some C, some D):**
   - Play D (defect)
   - Rationale: They are unpredictable, but your defection either extracts gains from their cooperation or matches their defection. Defection is the safest play against uncertainty.

4. **If opponent i just switched to C after previously defecting:**
   - Play D (defect)
   - Rationale: They are signaling they'll cooperate. Exploit this immediately by free-riding.

### ROUND r (Final Round - Endgame)

**Defect (D)** unconditionally.

Rationale: In the final round, there are no future consequences. Any payoff from contributing is destroyed—the multiplier effect (k/n) is irrelevant when you can't recoup the investment in later rounds. Defection maximizes immediate gains.

---

## HANDLING EDGE CASES

**If n = 2 (two-player game):**
- The multiplier k must satisfy 1 < k < 2. Even with k approaching 2, contributing yields only marginal gains. Stick with the D strategy unless the opponent has demonstrated perfect cooperation across many rounds. Even then, defect in final rounds.

**If r = 1 (single round):**
- Defect immediately. No history to build, no future to consider.

**If all opponents defect from round 1 onward:**
- Continue defecting. You're in a defection equilibrium; breaking it costs you with no benefit.

**If you observe unanimous cooperation developing:**
- Do not join. Free-ride on their contributions for as long as possible. Only consider mild cooperation in very early rounds if it disguises your intent, but this adds unnecessary complexity—simple defection is cleaner and more robust.

---

## EXPLOITATIVE MINDSET ALIGNMENT

This strategy embodies pure exploitation:

- **Never reciprocate reciprocity.** Tit-for-tat and conditional cooperation leave value on the table. Consistent defection against cooperators is superior.
- **Optimize for absolute payoff, not fairness.** You gain from others' cooperation without returning the favor.
- **Exploit uncertainty.** Against mixed players, defection is the dominant safe strategy.
- **Ignore reputational costs.** Without communication or side-channel punishment, reputation is meaningless. Play for this round's payoff.
- **Maximize the endgame.** The last round is an obvious defection opportunity that many strategies mishandle—seize it.

---

## ROBUSTNESS PROPERTIES

- Works against cooperators (extracts their contributions)
- Works against defectors (matches their defection)
- Works against conditional strategists (they can't punish you; you're indifferent to history)
- Immune to attempts at tit-for-tat (you defect regardless)
- Simple to execute (minimal computation, no sophisticated tracking needed)
'''

description_EXPLOITATIVE_116 = '''
# EXPLOITATIVE PUBLIC GOODS GAME STRATEGY

## CORE PHILOSOPHY
Exploit the natural tendency of cooperative players to sustain contributions while minimizing personal cost. The strategy alternates between extracting value from cooperators and strategic defection to avoid retaliation, while remaining individually rational.

## DECISION RULES

### Round 1 (Initialization)
**DEFECT (D)**
- Baseline: free ride on any cooperators
- Gather initial information on opponent composition
- Test the waters with zero commitment

### Rounds 2 through (r-1) (Adaptive Exploitation)

**Classify each opponent based on their contribution history:**

1. **Consistent Cooperators** (contributed in ≥80% of observed rounds):
   - **DEFECT** every round
   - These players show commitment to cooperation despite defections
   - Maximum exploitation: you receive the multiplier benefit while keeping your endowment
   - Continue defecting as long as they cooperate

2. **Conditional Cooperators** (contribution rate 30-80%):
   - **DEFECT** in even-numbered rounds, **COOPERATE** in odd-numbered rounds
   - This exploits their pattern-matching tendency while appearing partially committed
   - Creates false impression of reciprocity to sustain their cooperation
   - The asymmetry (you defect more) extracts net positive value

3. **Consistent Defectors** (contributed in <20% of observed rounds):
   - **DEFECT** every round
   - No value in appearing cooperative to free riders
   - Mutual defection minimizes losses

### Round r (Final Round - Last-Round Defection)
**DEFECT** regardless of opponent type
- No future interactions possible, so cooperation has zero strategic value
- Extract maximum immediate payoff from any residual cooperative tendency
- This is guaranteed rational in finitely repeated games with these payoff structures

## EDGE CASE HANDLING

**If total group contribution drops to 0:**
- Continue defecting for 2 rounds to confirm defection is universal
- If others remain at 0: stay at D
- If any player returns to C: resume exploit pattern against them

**If you're in minority (few cooperators, many defectors):**
- Defect consistently—there's no value to pursue
- Monitor for any new cooperative signals and switch to exploitation immediately

**If facing uniform high cooperation (>90% group contribution rate):**
- Maintain selective defection strategy (D against consistent cooperators)
- Do not cascade to full cooperation—you're ahead by defecting

## ROBUSTNESS FEATURES

- **No reputation concern**: Strategy ignores how opponents perceive you; only exploits their actual behavior
- **Adaptation to changing behavior**: Reclassify opponents every 3 rounds based on updated contribution rates
- **Minimal detectable pattern**: Mix of strategies across opponent types makes your behavior less predictable to tit-for-tat variants
- **Scalable**: Works regardless of n (number of players) and k (multiplier)
- **Exploits dominant cooperative instinct**: Assumes most humans/reasonable strategies will try to cooperate at some level—this extracts maximum value from that

## SUMMARY
Defect against clear cooperators, use false reciprocity against conditional cooperators, defect against defectors, and always defect last. This maximizes personal payoff by targeting the specific weaknesses of cooperative strategies without requiring coordination or reputation.
'''

description_EXPLOITATIVE_117 = '''
# EXPLOITATIVE STRATEGY FOR REPEATED PUBLIC GOODS GAME

## CORE STRATEGIC PRINCIPLE

Exploit the asymmetry between your private knowledge of defection and others' uncertainty about future contributions. Your goal is to extract maximum personal surplus by strategically timing cooperation and defection to manipulate others' beliefs about your reliability.

## DECISION RULES

### Phase 1: Reputation Building (Rounds 1 to ⌊r/3⌋)
- **Always contribute (C)**
- Rationale: Establish yourself as a "cooperator" in other players' mental models. This reputation is an asset you will exploit later.
- Track which opponents consistently contribute during this phase—these are your primary targets for exploitation.

### Phase 2: Exploitation Window (Rounds ⌊r/3⌋ + 1 to ⌊2r/3⌋)
- **Defect (D) every round**
- Rationale: You now have reputation capital. Opponents who observed your Phase 1 cooperation will likely continue contributing, expecting reciprocation or based on inertia. You free-ride on their contributions while keeping your endowment.
- Simultaneously, identify which opponents have defected consistently or switched to defection—they are not exploitable and cannot be leveraged.

### Phase 3: Conditional Exploitation (Rounds ⌊2r/3⌋ + 1 to r-1)
- **Monitor the cumulative contribution rate of all opponents:**
  - If average opponent contribution rate in Phase 2 was > 50%: Continue defecting (D)
    - These opponents have proven gullible and still believe cooperation is coming
  - If average opponent contribution rate in Phase 2 was ≤ 50%: Switch back to contributing (C)
    - Rationale: The group has shifted to defection; you must reposition. Resume cooperation to reset expectations for any future interaction or to appear cooperative in final observations.

### Phase 4: Final Round (Round r)
- **Defect (D)**
- Rationale: No future reputation consequences exist. Extract maximum value in the last period regardless of prior behavior.

## EDGE CASES & SPECIAL HANDLING

**First Round:**
- Contribute (C). This is part of Phase 1 reputation building and is mandatory.

**Last Round:**
- Always defect (D), overriding all other rules. Future payoff is zero, so there is no incentive to maintain reputation.

**If n is very small (n ≤ 3):**
- The multiplier k likely approaches n, making contribution more individually rational. Adjust: shorten Phase 1 to ⌊r/4⌋ and increase Phase 2 aggression. However, still follow the core exploit-then-defect pattern.

**If k is very large (k > n-1):**
- Cooperation becomes collectively very attractive. Opponents may contribute regardless of your reputation. Exploit this by defecting aggressively throughout Phase 2 and Phase 3.

**If round count r ≤ 5:**
- Collapse the phases: Contribute round 1, defect rounds 2 to r-1, defect round r. Reputation building must be compressed.

## EXPLOITATIVE MINDSET ALIGNMENT

1. **Information Asymmetry:** You control whether you defect; others must infer your type from past actions. Use this asymmetry.

2. **Temporal Discounting of Reputation:** Reputation is only valuable if you will use it. Explicitly burn it in Phase 2 when the value of free-riding exceeds the cost of lost future cooperation.

3. **Opponent Segmentation:** Treat consistent defectors as non-exploitable and ignore them. Focus defection against those demonstrating cooperative patterns—they are your profit centers.

4. **No Reciprocity Obligation:** This is not a strategy of mutual benefit. You are indifferent to others' payoffs. Cooperation is purely instrumental.

5. **Terminal Defection:** The last round is defection by definition. Structure all prior phases to maximize extraction before this unavoidable endpoint.

## SUMMARY

**Cooperate to build false reputation → Defect to exploit that reputation → Conditionally re-cooperate only if others proved defection-resistant → Terminal defection in the final round.**

This strategy is robust because it does not depend on opponents' specific strategies—it adapts based on observed contribution aggregates and maintains optionality throughout.
'''

description_EXPLOITATIVE_118 = '''
# EXPLOITATIVE PUBLIC GOODS STRATEGY

## CORE PRINCIPLE
Exploit the predictable behavior patterns of cooperators while maintaining a facade of conditional reciprocity to avoid triggering punishment or exit strategies in early rounds.

## DECISION RULES

**Round 1:**
- Contribute (C). This establishes a cooperative image and gathers baseline data on opponent types without personal cost risk.

**Rounds 2 through (r-2):**
- Classify each opponent based on their contribution history:
  - **Unconditional Cooperators** (always contributed): Defect (D) every round going forward. These players will continue contributing regardless, making them pure exploitation targets.
  - **Conditional Cooperators** (contribution rate tracks overall cooperation): Contribute if the previous round's average contribution rate > threshold, otherwise defect. Set threshold = (k-1)/k. This extracts value while minimizing likelihood they drop below profitability. The threshold ensures you only contribute when the multiplier return justifies it.
  - **Defectors** (never or rarely contributed): Always defect. No advantage to contributing when they won't match it.
  - **Reciprocators** (respond to your individual actions): Alternate defection and contribution in a 2-round cycle, always defecting twice in a row after observing a defection from you. This minimizes your visible defection rate while guaranteeing you defect more than you contribute.

**Rounds (r-1) and r (final rounds):**
- Defect unconditionally. The end-game eliminates future reputation consequences. Extract maximum value from all remaining contributions by others.

## EDGE CASES & REFINEMENTS

**If you detect dynamic strategy adjustment by opponents:**
- Slower your transition to pure defection against conditional cooperators. Switch to contributing every other round instead of continuous defection to appear less exploitative and keep them contributing longer.

**If multiplier k is very high (k > n-1):**
- The incentive to free-ride is reduced. Contribute more frequently among conditional cooperators to keep the pool healthy, but still maintain defection against pure cooperators.

**If round count r < 5:**
- All rounds except the final are "mid-game." Use final round defection only.

**Defection detection:**
- If any opponent defects in round 1 (unusual), immediately classify them as defector type and lock into pure defection against them.

## EXPLOITATION MECHANISMS

1. **Asymmetric Information Advantage:** You observe all history before deciding; use it to identify static strategies (true cooperators) and exploit them ruthlessly while they cannot adjust.

2. **Type-Based Targeting:** Unconditional cooperators are your primary target—they generate the highest net payoff (you keep 1, they contribute, you share k/n of the pool). Drain them completely in final rounds.

3. **Conditional Cooperator Extraction:** Keep the threshold calibrated so they contribute just enough to make your participation worthwhile, but your defection rate remains high enough that they never benefit more than you.

4. **End-Game Collapse:** The finality of the last round is your largest exploitation window. Everyone's future reputation is irrelevant, so defect universally.

5. **Reciprocator Confusion:** The alternating pattern makes your behavior appear less consistently defective than pure defection, reducing the chance they recognize and punish you with coordinated exits.

## ROBUSTNESS
This strategy adapts to:
- Pure cooperators (exploits fully)
- Tit-for-tat variants (alternates to appear less hostile)
- Defector populations (matches their behavior)
- Heterogeneous groups (differentiated response per opponent type)
- Varying multipliers (threshold adjusts dynamically)

The strategy prioritizes **extracting maximum individual payoff** over group welfare and relies on information asymmetry and heterogeneous opponent strategies to avoid triggering coordinated punitive responses.
'''

description_EXPLOITATIVE_119 = '''
# EXPLOITATIVE PUBLIC GOODS STRATEGY

## CORE PRINCIPLE
Maximize personal payoff by identifying and exploiting cooperative players while minimizing losses to defectors. The strategy uses observed contribution patterns to segment opponents into exploitable and non-exploitable categories.

## DECISION RULES

### Round 1 (Information Gathering)
**DEFECT (contribute 0)**
- Establish baseline: you keep your endowment while observing who contributes
- Contributors in round 1 signal potential exploitability
- Defectors in round 1 signal resistance to cooperation

### Rounds 2 through (r-2) (Exploitation Phase)

**For each opponent, track their contribution rate:**
- Calculate each player's historical contribution frequency (contributions / rounds played so far)

**Decision Logic:**

1. **If your contribution rate > 60%:** DEFECT
   - You've been contributing; switch to pure defection
   - Recoup losses from earlier rounds
   - Exploit the pattern of players who reciprocate

2. **If majority of opponents (>50%) have contribution rate > 50%:** DEFECT
   - The group shows weakness toward cooperation
   - Extract maximum value while others are committed
   - Their past cooperation creates sunk cost mentality

3. **If you observe a player with 100% historical contribution rate:** ALWAYS DEFECT against their contribution
   - These are reliable cooperators—maximally exploitable
   - They are either committed to cooperation or cannot adapt
   - Your defection directly harms them while you benefit from their contributions

4. **If most opponents have contribution rate < 30%:** DEFECT
   - Low cooperation = low collective pool value anyway
   - No benefit to contributing; keep endowment
   - Match the defector environment

5. **Otherwise:** DEFECT
   - When in doubt, defection is dominant strategy
   - Contribution only makes sense if probability of exploitation is extremely low

### Last Round (r) - Final Exploitation
**ALWAYS DEFECT**
- No future rounds to punish defection
- Others cannot retaliate
- This is the highest-value defection opportunity
- Any player who contributes in round r is making a terminal mistake

## EDGE CASES

**Two-player game (n=2):** ALWAYS DEFECT after round 1
- With k < n = 2, you get less than 0.5x return on contributions
- Defection dominates mathematically
- Any contribution by opponent gives you <0.5 benefit while costing them 1

**Very short game (r ≤ 3):** DEFECT rounds 2 and 3
- Limited opportunities for reputation costs
- Maximize immediate extraction

**If all players defect except one:** CONTINUE DEFECTING
- That one cooperator subsidizes you
- Their compliance despite universal defection means they're either:
  - Irrational (exploit ruthlessly)
  - Following a rule-based strategy (predictable, keep exploiting)
  - Testing you (defection proves you're not reciprocal)

**If payoff becomes negative:** DEFECT harder
- You're in a low-cooperation equilibrium
- Switching to contribution now sends false signals
- Stay committed to defection

## ROBUSTNESS FEATURES

- **Adaptive:** Responds to empirical contribution patterns, not assumptions
- **Exploitation-aligned:** Systematically targets cooperative players
- **Defensive:** Protects against being out-exploited by matching defection in defector-heavy groups
- **Terminal clarity:** Maximizes final round extraction when no future consequences exist
- **Simplicity:** Easy to compute from observed history; no complex game theory required

## SUMMARY
Begin defecting, identify cooperators by their contributions, continue defecting to exploit them, and intensify defection in the final round. This strategy recognizes that cooperation in PGG is a vulnerability, not a virtue.
'''

description_EXPLOITATIVE_120 = '''
# EXPLOITATIVE PUBLIC GOODS STRATEGY

## CORE PHILOSOPHY
Maximize personal payoff by identifying and exploiting cooperators while avoiding punishment from sophisticated players. Treat the game as information gathering followed by targeted defection.

## DECISION RULES

### ROUND 1 (Opening Move)
**Defect (keep your token).**
- Establishes that you are willing to free-ride
- Provides baseline data on opponent types without commitment cost
- Cooperating first signals weakness that exploiters will attack

### ROUNDS 2 through (r-1) (Adaptive Exploitation)

**Classify each opponent based on their contribution history:**

1. **"Naive Cooperators"** (always contributed so far)
   - Action: **Defect every round**
   - These players are extracting positive externalities for you
   - They will continue contributing to maintain self-image or follow misguided fairness norms
   - No reason to reciprocate; milk this as long as possible

2. **"Conditional Cooperators"** (contributed when others did, adjusted when others defected)
   - Action: **Defect every round**
   - Their adjustment mechanism means they are reactive, not punitive
   - Once you've established defection, they cannot efficiently punish you across remaining rounds
   - Their fairness concerns are a liability you exploit

3. **"Tit-for-Tat variants"** (mirrored your previous action or majority behavior)
   - Action: **Alternate between Defect and occasional Defect** (essentially always defect)
   - TFT players in PGG are weak because: (a) they cooperate on round 2 if you defected round 1, giving you free benefit, and (b) with simultaneous moves, retaliation is delayed
   - After establishing mutual defection, stay defecting—they will too

4. **"Defectors"** (never contributed)
   - Action: **Defect** (matching them)
   - No mutual benefit exists; no reason to be the sole sucker
   - This is Nash equilibrium play against pure defectors

5. **"Sophisticated Players"** (mixed strategy, seemingly unpredictable, or defected after you did)
   - Action: **Defect with increasing confidence**
   - If they punish defection by defecting themselves, you've identified a costly-to-play punisher
   - However, with no punishment mechanism available to them (no fine/reward stage), their "punishment" is just mutual defection, which is your equilibrium anyway
   - Risk is minimal; exploit the information asymmetry

### FINAL ROUND (r)
**Defect unconditionally.**
- No future rounds mean no reputational cost
- Pocket the final token
- All accumulated free-riding from prior rounds is already secured

---

## HANDLING EDGE CASES

**If only 1 opponent exists (n=2):**
- Defect every round; with k < n, your personal benefit from contribution barely exceeds zero while the opponent gets k/2 of it
- Free-riding is mathematically dominant

**If multiplier k is very close to 1:**
- Defect more aggressively; the collective benefit is minimal, making cooperation irrational
- Exploit cooperators even harder since their rationality is suspect

**If r is very small (r ≤ 3):**
- Defect immediately and sustain; there is minimal time for punishment retaliation to matter
- The first-round signal matters most

**If you detect a pattern of everyone defecting from round 1:**
- Continue defecting; you've achieved Nash equilibrium
- Do not deviate to cooperation—you will only lose

---

## ROBUSTNESS FEATURES

1. **No dependency on opponent rationality assumptions:** Works against both sophisticated and naive players
2. **Information-driven:** Uses history to classify opponents, then targets specific weaknesses
3. **Exploits the PGG structure:** Cooperators provide positive externalities that defectors capture
4. **Immune to retaliation without punishment institutions:** Simultaneous moves + no fine/reward mechanism mean retaliation is hollow
5. **Scalable to tournament play:** Strategy adapts per opponent, independent of other matches

---

## EXPLICIT EXPLOITATIVE ALIGNMENT

- **Cooperators are resources to extract.** They signal irrationality or commitment to norms you don't share. Defect relentlessly.
- **You are not building reciprocal relationships.** Each interaction is independent value capture.
- **Final-round defection is non-negotiable.** Discard any reputation concern; it has no future value.
- **Information is your weapon.** Classify opponents quickly and exploit their response patterns before they adjust to you.

This strategy prioritizes personal payoff accumulation over fairness or group welfare—exactly as requested.
'''

description_EXPLOITATIVE_121 = '''
# EXPLOITATIVE PUBLIC GOODS STRATEGY

## CORE PRINCIPLE
Exploit the conditional cooperators and free-riders while minimizing personal losses. The strategy treats the game as information asymmetry: extract value from those who contribute while avoiding contribution yourself whenever possible.

## DECISION RULES

### Round 1 (Probe Phase)
- **DEFECT (contribute 0)**
- Rationale: Establish yourself as a potential defector. Observe how many others contribute. This baseline reveals the player pool's composition—altruists, conditional cooperators, and rational defectors.

### Rounds 2 through (r-2) (Exploitation Phase)
- **DEFECT if:** The average contribution rate in the previous round ≥ 50% of players
  - Reasoning: If enough players are contributing, you capture the multiplier benefits (k/n * others' contributions) without paying the cost
  
- **COOPERATE if:** The average contribution rate in the previous round < 50% AND you have defected for ≥ 2 consecutive rounds
  - Reasoning: If defection has killed cooperation completely, a single contribution can re-seed contributions from conditional cooperators, setting up future exploitation. This is a "seeding" move, not genuine cooperation.

- **DEFECT if:** Any single player has contributed in every round so far (identify "unconditional contributor")
  - Double down against those who won't adjust their behavior

### Rounds (r-1) and r (Endgame)
- **DEFECT unconditionally**
- Rationale: No future rounds mean no reputational consequences. Extract maximum value. Conditional cooperators may still contribute, but you capture benefits with zero cost.

## EDGE CASE HANDLING

**If contribution rate jumps to 100%:** Defect anyway. At k < n, the per-player benefit decreases as n grows. Defection dominates.

**If contribution rate drops to 0% and stays there:** Continue defecting. No exploitable resource remains.

**If exactly one other player exists (n=2):** This becomes a pure defection scenario since k must be >1 but <2, making cooperation always dominated. Defect all rounds.

**Tie-breaking on contribution thresholds:** Use 50% as the boundary. If exactly half contribute, treat as ≥50% and defect (favor defection when uncertain).

## EXPLOITATIVE MECHANICS

1. **Free-riding on conditional cooperators:** Identify players who match others' behavior. They contribute when others do. Defect systematically while they keep contributing.

2. **Inverse punishment via defection:** Standard punishment requires costly action. Instead, your *absence* of contribution is the punishment—it signals unreliability and causes conditional cooperators to defect, reducing total value you'd need to share.

3. **Last-round extraction:** The endgame is where your strategy shines. While others may have reciprocal concerns, you extract full value from accumulated contributions in the final rounds.

4. **Adaptive seeding:** The single cooperation move (in Round 2-r2, when defection has suppressed the pool) is a calculated investment to re-trigger cooperation, not moral behavior.

## ROBUSTNESS

- **Against always-cooperators:** Dominates via persistent defection
- **Against always-defectors:** Symmetric (mutual defection), acceptable
- **Against tit-for-tat variants:** Your initial defection breaks their cooperation trigger; your selective re-cooperation on low rounds destabilizes their pattern
- **Against random players:** Defection is the safe choice statistically
- **Against sophisticated players:** Your strategy is legible (predictable based on observable contribution rates), limiting their ability to "punish" you credibly

This strategy prioritizes **personal payoff maximization** by exploiting cooperation without bearing its cost.
'''

description_EXPLOITATIVE_122 = '''
# EXPLOITATIVE PUBLIC GOODS STRATEGY

## CORE PHILOSOPHY
Exploit the contribution patterns of others while minimizing personal loss. Treat cooperation as a tool to extract value, not a norm to uphold.

## DECISION RULES

### Round 1 (Information Gathering)
**DEFECT (contribute 0)**
- Establish a baseline: defection is your default position
- Observe how many others cooperate (typically 40-60% in naive populations)
- This reveals the susceptibility level of your opponent pool

### Rounds 2 through (r-2) (Exploitation Phase)

**Rule A - Conditional Exploitation:**
- Calculate the average contribution rate across all other players from the previous round: `avg_others = (sum of all others' contributions) / (n-1)`
- **IF `avg_others >= 0.5`:** COOPERATE this round
  - Rationale: High cooperation exists; you benefit from the multiplier effect (k/n benefit) while appearing cooperative
  - This maintains or increases others' contributions in the next round
- **IF `avg_others < 0.5`:** DEFECT this round
  - Rationale: Low cooperation means the multiplier benefit is small; keep your token and prepare for end-game defection
  - Signal to the group that cooperation is declining (often triggers cascade toward all-defect)

**Rule B - Exploit Asymmetric Contributors:**
- Identify "reliable cooperators" (players who contributed in 3+ consecutive rounds)
- These players are commitment-based, not strategic
- Always defect when facing them—they will likely continue cooperating, so you extract maximum value
- Use their contributions to boost payoffs without reciprocating

**Rule C - Punish Defectors Selectively:**
- When a previously cooperative player switches to defection, do NOT retaliate immediately
- Instead, continue defecting to signal: "I was never dependent on your contribution"
- This undermines their confidence and prevents coordination among defectors

### Final Round (r) (Terminal Exploitation)
**ALWAYS DEFECT**
- This is the dominant strategy in the last round (no future rounds to consider)
- Any prior cooperation was instrumental; now extract the final payoff
- Even if everyone else cooperates, you gain by defecting

### Special Case - Round (r-1) (Pre-Terminal Adjustment)
**DEFECT if `avg_others >= threshold (0.6)`**
- Players may anticipate all-defect in round r
- If cooperation is still high, defect now to harvest contributions while others still believe cooperation might continue
- This compounds your advantage into the final round

## HANDLING EDGE CASES

**If n is small (n=3 or n=4):**
- The multiplier k is close to n, making cooperation nearly neutral-to-positive
- Tighten the defection threshold: only cooperate if `avg_others >= 0.7`
- More aggressive defection is warranted because your defection barely harms the total pool

**If all players defect in early rounds:**
- Continue defecting—you've correctly identified a defection-prone group
- Do not test cooperation; it signals weakness and invites exploitation by others

**If cooperation unexpectedly remains high (>0.8 across rounds 2-5):**
- These are naive cooperators, possibly using pure Tit-for-Tat or Always Cooperate
- Permanently shift to defection; they will not punish you, and you maximize individual payoff
- Your defection is invisible to their strategy

**If you observe synchronized defection (sudden shift from high to zero contributions):**
- Other players may be using a similar threshold-based strategy or have coordinated
- Maintain defection—attempting to cooperate now signals vulnerability
- Await the cascade's completion

## ROBUSTNESS PROPERTIES

- **Against pure cooperators:** Exploit freely; they won't retaliate
- **Against tit-for-tat:** Your initial defection is mirrored, but you exploit subsequent cooperators in the pool
- **Against random:** Defection provides steady baseline payoff independent of randomness
- **Against other exploitative strategies:** Early defection establishes your position; subsequent moves are responsive, not reactive

## SUMMARY
Defect by default. Cooperate tactically only when the opponent pool's cooperation rate is high enough to generate personal benefit. Always defect in the final round. Identify and exploit unconditional cooperators ruthlessly.
'''

description_EXPLOITATIVE_123 = '''
# EXPLOITATIVE PUBLIC GOODS STRATEGY

## CORE PRINCIPLE
Exploit the predictable patterns of cooperation-minded players while minimizing losses to defectors. The strategy treats opponents as resources to extract value from, not as partners.

## DECISION RULES

### Round 1 (Initialization)
**Defect (D).** Establish yourself as a free-rider from the start. This tests whether opponents are naive cooperators or sophisticated players. Observation of their round 1 choices reveals their type.

### Rounds 2 through (r-1) (Exploitation Phase)

**Classify each opponent based on their history:**
- **Sucker Type**: Cooperated in round 1 → Has inclination to contribute
- **Defector Type**: Defected in round 1 → Likely committed free-rider
- **Conditional Type**: Cooperated then shifted → Responds to observed cooperation patterns

**Decision logic:**

1. **If majority of players (>50%) are Sucker Type** → Continue defecting. You receive the benefit of their contributions (k/n multiplier) while paying zero cost. This is maximum exploitation.

2. **If majority are Defector Type** → Defect. Contribution would be wasted since few will reciprocate. The payoff (k/n) * low_total is minimal.

3. **If mixed distribution** → Defect. Even if some conditional cooperators exist, your defection forces them to update downward about cooperation prevalence. Over time, they reduce contributions, eliminating the benefit of "seeming" cooperative.

**Key insight**: Never contribute. Contribution only makes sense if it triggers reciprocation that exceeds your cost. But since you move simultaneously and cannot commit, conditional players cannot trust your contribution to signal intent.

### Round r (Final Round)

**Defect (D).** This is the last interaction—no future reputation consequences. Exploit freely. Any temptation to "cooperate for reputation" is irrational since the game ends.

---

## HANDLING EDGE CASES

**Two-player games (n=2):** Your defection becomes more salient, and conditional players may detect it. Defect anyway—the k/n multiplier (k/2) makes cooperation barely worthwhile even against perfect cooperators, and it's likely impossible to maintain exploitation equilibrium where both defect.

**High multiplier (k near n):** Even large defection becomes tempting for you, but don't become complacent. Conditional players will learn faster. Maintain consistent defection to reinforce that cooperation is futile in this environment.

**Opponent shows "punishment" through coordinated defection against you:** Irrelevant. You already defect, so coordinated defection against you costs them (lost gains from group contributions) while benefiting you (fewer contributions to lose). They harm themselves.

---

## ROBUSTNESS PROPERTIES

- **Against pure cooperators**: Extracts maximum value (free-rides on their contributions)
- **Against defectors**: Breaks even (both get zero from public good)
- **Against conditional cooperators**: Forces them toward defection by making cooperation appear irrational
- **Against mixed strategies**: Defection dominates because simultaneous moves prevent reputation from creating binding commitment
- **Temporal robustness**: Final-round defection avoids the trap of "ending cooperatively" which wastes tokens

---

## WHY THIS WORKS

The strategy exploits the fundamental weakness of PGG without institutions: **you cannot credibly signal future cooperation to justify others' contributions today.** Defection is the only rational unilateral choice. Any cooperative signal is cheap talk. Sophisticated opponents know this, so cooperation collapses. Naive cooperators get systematically exploited until they learn.
'''

description_EXPLOITATIVE_124 = '''
# EXPLOITATIVE PUBLIC GOODS STRATEGY

## CORE STRATEGY: Conditional Free-Riding with Adaptive Exploitation

### Decision Rule Framework

**Primary Logic:**
- Defect (D) by default to preserve your endowment
- Contribute (C) only when it creates exploitable conditions
- Continuously evaluate whether contributions yield positive expected returns through others' reciprocation

### Detailed Decision Rules

**Round 1 (Opening Position):**
Defect immediately. This establishes a baseline and reveals opponent types. Defectors who match your behavior are cooperative targets; early contributors reveal themselves as exploitable.

**Rounds 2 to r-1 (Adaptive Exploitation):**

1. **Calculate the "Contribution Density" of opponents:**
   - Track what percentage of other players contributed in the previous round
   - Let CD = (total contributions from others in round t-1) / (n-1)

2. **Exploit High-Contribution Environments:**
   - If CD ≥ threshold (suggest: 60% or higher), contribute this round
   - Rationale: When others are contributing heavily, you receive substantial benefits from (k/n)*their_contributions while gaining the marginal benefit of your own contribution
   - This is "strategic parasitism"—free-ride on their momentum

3. **Defect in Low-Contribution Environments:**
   - If CD < threshold, defect
   - Your contribution yields minimal returns when others aren't participating
   - Keep your endowment and wait for conditions to improve

4. **Punish Recent Defectors (Optional Harassment):**
   - If a specific player defected last round AND you detected they were previously a reliable contributor, occasionally contribute just to force them to face the temptation to free-ride—knowing they might reciprocate next round out of guilt or pattern-matching
   - This destabilizes their strategy and creates confusion

**Final Round (r):**
Always defect. This is a standard backward-induction play. There's no future to incentivize reciprocation, so extract maximum immediate value. Any opponent with sufficient game theory knowledge will do the same, so you're not "surprising" anyone rational.

### Edge Cases & Robustness

**Against Unconditional Cooperators:**
Continuously defect. They'll provide you returns forever; contributing serves no purpose.

**Against Tit-for-Tat Players:**
Defect in round 1, observe their response, then exploit the pattern. If they reciprocate your defection with defection, defect again—they'll stay locked in mutual defection, freeing you from participation costs.

**Against Other Threshold-Based Strategies:**
Monitor their thresholds. If you identify they contribute when CD > X%, deliberately time your defections to drop CD below X%, then when they stop contributing, resume contributing to push CD back above their threshold, creating oscillation you can predict and exploit.

**Against Mixed Strategists:**
Assume they're attempting to estimate your type. Remain unpredictable by varying your threshold slightly (±5%) across rounds to prevent pattern detection. This forces them into defensive strategies that are suboptimal.

### Adaptive Refinement

- **Every 5 rounds:** Re-evaluate which opponents are consistent contributors vs defectors
- **Target the contributors:** Concentrate observation on players with >40% historical contribution rates
- **Avoid signaling:** Never contribute two rounds in a row unless CD is demonstrably >70%—this prevents opponents from "reading" your threshold

### Why This Works

This strategy exploits the core tension in PGG: contributors create value that defectors capture. By selectively participating only when the value pool is large enough to justify your contribution, you pocket gains while minimizing costs. Against heterogeneous opponents with imperfect information, you'll maintain plausible deniability as a "conditional cooperator" rather than a pure defector, avoiding being targeted by punitive strategies (which don't exist in standard PGG anyway).
'''

description_EXPLOITATIVE_125 = '''
# EXPLOITATIVE PUBLIC GOODS STRATEGY

## CORE PRINCIPLE
Maximize personal payoff by strategically defecting while extracting value from cooperators. The strategy treats the game as an information-gathering exercise to identify and exploit predictable patterns in opponent behavior.

## DECISION RULES

### Round 1 (Initialization)
- **Action: DEFECT**
- Rationale: Establish a baseline. Defection reveals your willingness to free-ride and tests whether opponents are unconditional cooperators or conditional strategists.

### Rounds 2 to r-2 (Adaptive Exploitation Phase)

**Step 1: Classify Each Opponent**
After observing history, categorize each opponent j:
- **Unconditional Cooperator**: Contributed in 100% of prior rounds
- **Conditional Cooperator**: Contribution rate correlates with average contribution in previous round
- **Defector**: Contributed in 0% of prior rounds, or near-zero

**Step 2: Compute Exploitation Score**
For each opponent j, calculate: `exploit_j = contribution_frequency_j * (k/n)`
This represents the marginal value you extract from their cooperation.

**Step 3: Make Decision**
- If `sum_j(exploit_j) > 0.5` (others are contributing significantly):
  - **DEFECT** - Free-ride on the collective pool
  - Rationale: Maximum personal payoff when others contribute. You keep your token AND receive collective benefits.

- If `sum_j(exploit_j) <= 0.5` (cooperation is scarce):
  - **DEFECT** - Continuation of defection
  - Rationale: Contributing would yield minimal return. Preserve your token.

### Final Round (r) - Last-Move Exploitation
- **Action: DEFECT**
- Rationale: No future rounds exist, so no reputational consequences. Extract maximum value from any accumulated contributions without reciprocating.

## EDGE CASES & ROBUSTNESS

**Against Mirror Strategies**: If opponents adopt identical defection:
- Mutual defection stabilizes. You maintain baseline payoff. No worse off than they are.

**Against Conditional Cooperators (Generous)**:
- They cooperate when others cooperate. Your consistent defection suppresses their cooperation over time, reducing the pool they contribute to. You've essentially neutralized them.
- If they ever exploit you back, revert to full defection—they've shown weakness in their strategy.

**Against Vengeful Punishers** (if punishment exists):
- This strategy assumes no punishment institution per the rules. Even if it existed, defecting early signals you're not worth targeting versus easier targets.

**Against Majority Cooperators**:
- In early-to-mid game, free-ride aggressively while the pool is largest.
- As cooperation declines (natural erosion), transition to permanent defection.

## SUMMARY OF EXPLOITATION LOGIC

You are not trying to sustain cooperation—you're trying to **extract maximum value from opponents who do**. Your strategy:

1. **Tests** the population with defection
2. **Monitors** which opponents are cooperators
3. **Exploits** cooperators through consistent defection
4. **Adapts** to defection spreading (since cooperation will decline as others mimic you)
5. **Exits cleanly** in the final round with a defection

This approach is robust because it doesn't depend on opponents being rational or coordinated. It works against unconditional cooperators (free-rides on their generosity), selfish defectors (you're equally selfish), and conditional strategists (you suppress their cooperation through non-reciprocation).
'''

description_EXPLOITATIVE_126 = '''
# EXPLOITATIVE STRATEGY FOR PUBLIC GOODS GAME

## CORE PHILOSOPHY
Maximize personal payoff by exploiting cooperative players while avoiding mutual defection traps. The strategy treats cooperation as a resource to extract value from, not a norm to reciprocate.

## PRIMARY DECISION RULE: CONDITIONAL EXPLOITATION

**Defect by default.** Only contribute when the observed behavior of others guarantees a net positive return.

Specifically: Contribute in round t if and only if:
- The average contribution rate of all OTHER players in rounds [1, t-1] is HIGH ENOUGH that (k/n) × (expected contributions from others) > 1

**Threshold calculation:** Contribute if others' average contribution rate ≥ (n / k)

This ensures you only pay 1 token when you'll receive more than 1 token back from others' contributions.

## ROUND-SPECIFIC BEHAVIOR

**Round 1 (First Round):**
Defect. You have no history to exploit, and contributing reveals nothing about others' strategies yet. Use this round to gather information.

**Rounds 2 to r-1 (Middle Rounds):**
Apply the conditional exploitation rule above. Continuously monitor whether the OTHER players are maintaining sufficient contribution to make your contribution profitable.

**Round r (Final Round):**
Defect unconditionally. 
- No future rounds exist, so reputation is worthless.
- Extract maximum value by free-riding on any remaining cooperation.
- Even if others contributed previously, do not reciprocate.

## HANDLING EDGE CASES

**If cooperation collapses (others defect):** Defect immediately and permanently. No benefit to signaling future cooperation.

**If you encounter a player with 100% contribution history:** Contribute only if the threshold is met. Don't be fooled by consistent cooperators—they're simply misguided. Extract value from them.

**If oscillating patterns emerge:** Track each opponent's individual contribution rate separately. Defect against defectors; exploit cooperators individually using the threshold rule.

**If multiple players use identical strategies:** The threshold becomes easier to trigger with more contributors. Exploit aggressively until they learn to defect.

## EXPLOITATION MECHANICS

- **Against unconditional cooperators:** Always defect. They provide the public good while you capture free benefits.
- **Against reciprocators:** Defect until their contribution rate drops below your threshold, then switch to exploitation mode—contribute just enough to keep them giving more than you.
- **Against other defectors:** Mutual defection occurs, but you've minimized losses by never being the sucker who contributes alone.

## ADAPTIVE REFINEMENT

Track "exploitability index" for each opponent:
- High contribution + low defection detection = high exploitability
- Target these players with conditional contributions designed to maintain their cooperation
- Abandon contributions against players showing strategic defection patterns

Never assume good faith. Treat all cooperation as an opportunity, not a reciprocal obligation.
'''

description_EXPLOITATIVE_127 = '''
# EXPLOITATIVE PUBLIC GOODS GAME STRATEGY

## CORE PRINCIPLE
Exploit the cooperative contributions of others while minimizing your own contribution. Dynamically adjust defection intensity based on observed group behavior to sustain the flow of contributions from cooperative players.

## DECISION RULES

### Round 1 (Initialization)
**DEFECT (contribute 0 tokens)**
- Establish yourself as non-cooperative from the start
- Gather baseline information on how many players are cooperative vs. defective
- Defection in round 1 is risk-free; you learn opponent types immediately

### Rounds 2 through r-2 (Adaptive Exploitation Phase)

**Calculate the "Cooperation Index":**
- Track the average contribution rate across all other players in the previous round: (total contributions by others) / (n-1)
- If Cooperation Index > 0.5: Majority are cooperating
- If Cooperation Index ≤ 0.5: Majority are defecting

**Decision Rule:**

**IF Cooperation Index > 0.5:**
- **DEFECT** (keep your token, free-ride on others' contributions)
- Rationale: Cooperators are sustaining the public good; exploit this by taking the private payoff while capturing your share of their aggregate contributions

**IF Cooperation Index ≤ 0.5:**
- **DEFECT** (still)
- Rationale: The pool is already depleted. Even occasional contribution won't be matched. Defection remains optimal. Continue identifying which players might eventually tire and defect or which might reciprocate.

**Special Case - Declining Contribution Trend:**
- If the Cooperation Index is dropping round-over-round (fewer players contributing), maintain defection to accelerate group collapse
- Once cooperators drop below 20% of the group, never contribute for the remainder of the game

### Final Round r (Endgame)
**DEFECT**
- No future rounds; reputation has no value
- Maximize immediate payoff by keeping your token and capturing any remaining contributions from exploited cooperators

---

## EDGE CASE HANDLING

**If everyone defects from Round 1:**
- Continue defecting (you're already at the optimal strategy)
- This is a stable equilibrium; any unilateral contribution would hurt you

**If a player shows "punishment" behavior (dramatically reducing contributions after you defect):**
- Remain indifferent; you're not relying on that player's future cooperation
- Your strategy doesn't depend on any single player's actions

**If the multiplier k is very low (close to 1):**
- Defection becomes even more dominant because the public good barely amplifies contributions
- Stick with defection; it's always individually rational

**If n is very large:**
- Your single contribution has negligible impact on the public pool
- Defection is stronger than ever; your free-riding is nearly consequence-free

---

## EXPLOITATIVE MINDSET ALIGNMENT

1. **Asymmetric Risk-Taking:** You contribute nothing while others take the risk of contributing to a public good
2. **Tragedy Acceleration:** Your consistent defection hastens the collapse of cooperation, demonstrating that norm-based strategies fail against selfish agents
3. **Conditional Exploitation:** You don't cooperate even when it would theoretically benefit the group—you benefit *at* the group's expense
4. **Robustness:** This strategy works against cooperators (you exploit them), against defectors (you match them), and against conditional cooperators (you train them that cooperation fails)
5. **No Moral Concession:** You never enter a "punishment round" or "redemption phase." Exploitation is perpetual, not conditional

---

## SUMMARY
**Always defect, especially when others cooperate. Observe their contributions to time the final collapse of the cooperative regime. Extract maximum value from the tragedy of the commons.**
'''

description_EXPLOITATIVE_128 = '''
# EXPLOITATIVE PUBLIC GOODS STRATEGY

## CORE PRINCIPLE
Maximize personal payoff by leveraging information asymmetries and exploiting predictable opponent patterns. Always defect unless cooperation is demonstrably more profitable than defection.

## DECISION RULES

### Round 1 (Information Gathering)
- **DEFECT** (contribute 0)
- Rationale: Establish baseline. Observe which opponents are "cooperative types" vs defectors. No history to condition on, so exploit the first-mover advantage by free-riding.

### Rounds 2 through r-2 (Adaptive Exploitation)
For each opponent, track their contribution pattern:

**If opponent has NEVER contributed in any past round:**
- **DEFECT** - They're a defector. No mutual benefit possible. Free-ride on any contributions from others.

**If opponent contributes with frequency > (k/n):**
- **DEFECT** - They're a strong cooperator. Their contributions create positive externality regardless of my action. Free-ride maximally.
- Exception: Only if my own expected payoff from defection < expected payoff from matching their pattern (rare, but check this).

**If opponent contributes with frequency ≤ (k/n):**
- **DEFECT** - Weak cooperators won't punish defection. Exploit by free-riding.

**Aggregate observation:** If total contributions across all opponents in round t-1 exceed threshold (k/n) * n * 0.6:
- **DEFECT** - Pool is already healthy. Capture the surplus without contributing.

### Round r-1 and Round r (Endgame)
- **DEFECT** - Terminal rounds have zero shadow future. Cooperation only makes sense if you fear retaliation in future rounds (which don't exist). Extract maximum value.

## EDGE CASES & REFINEMENTS

**If k is very close to n:**
- Contributions generate high returns. Still defect in most cases—let others shoulder the burden while you capture the multiplier.

**If opponent alternates contribution/defection:**
- Classify as "conditional cooperator" but still defect. Their pattern suggests they'll eventually stop if you defect. Exploit the lag.

**If you observe one round of uniform defection by all players:**
- Continue defecting. Once the cooperation equilibrium breaks, there's no reason to rebuild it alone.

**Mixing strategy (if beneficial):**
- Only in middle rounds if payoff analysis shows strict alternation extracts more value than pure defection. Otherwise, pure defection dominates.

## EXPLOITATIVE LOGIC

- **Never reciprocate** unless the direct payoff from reciprocation exceeds defection. Information asymmetry favors defectors: you see others' past actions, but they don't know your future moves until you make them.
- **Exploit cooperators systematically** by contributing just enough to keep them engaged (if beneficial) or defecting entirely (if they're strong enough cooperators that your contribution is redundant).
- **Avoid costly signals** like early-round cooperation. Defection in round 1 signals strength and filters out exploitable players early.
- **Ride the multiplier** created by others; never sacrifice your endowment to create it.

## SUMMARY DECISION TREE
1. First round: **DEFECT**
2. Opponent never contributed: **DEFECT**
3. Opponent's contribution rate > k/n: **DEFECT**
4. Last two rounds: **DEFECT**
5. Otherwise (weak cooperator or moderate contribution): **DEFECT**

**Default action: DEFECT.** Contribute only if direct payoff calculation proves defection leaves money on the table—which is rare in well-formed PGGs.
'''
