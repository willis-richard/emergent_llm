"""
Strategy descriptions for public_goods.

Generated with:
- Provider: Anthropic
- Model: claude-haiku-4-5
"""


description_COLLECTIVE_1 = '''
# Adaptive Threshold Reciprocity with Dynamic Learning

## Core Decision Rule

In round t, cooperate if and only if:

```
observed_coop_rate ≥ threshold(t)
```

where:
- `observed_coop_rate` = (cooperators in round t-1) / (n-1)
- `threshold(t)` = breakeven cooperation level, adjusted for stage of game

## Threshold Calculation

The breakeven threshold where cooperation and defection yield equal payoff:

```
threshold(t) = (n - k) / (n × (k - 1))
```

This is the cooperation rate among *other* players where my payoff is identical whether I cooperate or defect.

**Intuitively**: Cooperate when you expect enough others to cooperate that the public good benefit compensates for your contribution.

Adjust the threshold downward as the game progresses to account for reduced future punishment/reward:

```
threshold(t) = base_threshold × (1 + (r - t) / r)
```

This makes cooperation more attractive early (when future cooperation matters) and less attractive late.

## Edge Cases and Initialization

**Round 1**: Use `threshold(1)` with no history. Cooperate conservatively.
- If k is close to n: cooperate (high multiplier suggests others will too)
- If k is close to 1: defect (weak public good)
- Specifically: cooperate if `k > (n+1)/2`, else defect

**Last round (t = r)**: Apply `threshold(r)` which approaches base threshold from above. Defection becomes attractive here as no future punishment exists.

**Rounds 2 to r-1**: Track exponential moving average of observed cooperation:

```
avg_cooperation = 0.7 × avg_cooperation_previous + 0.3 × observed_coop_round_t-1
```

Use this smoothed estimate to compare against `threshold(t)`.

## Collective Alignment

This strategy operationalizes collective thinking:

1. **Reciprocal honesty**: Cooperate when aggregate behavior suggests others are cooperating; defect when they aren't. You contribute to the public good precisely when doing so is mutually beneficial.

2. **Non-exploitative**: You don't attempt to free-ride. You only defect when observed cooperation is too low to justify contribution.

3. **Stability seeking**: By setting thresholds at the true breakeven point, you facilitate mutual cooperation without requiring trust. If others use similar reasoning, coordination emerges endogenously.

4. **Adaptive to diversity**: Robust to opponents ranging from pure cooperators to pure defectors. Automatically calibrates to the actual cooperation level observed, without assuming opponent types.
'''

description_COLLECTIVE_2 = '''
# Adaptive Reciprocal Strategy for N-Player Public Goods Game

**Core Decision Rule:**

Cooperate in round t if and only if:
- (t = 1) OR 
- (t < r AND cooperation_rate_{t-1} ≥ threshold(t, n, k)) OR
- (t = r AND cooperation_rate_{t-1} ≥ high_threshold)

Where:
- cooperation_rate_{t-1} = (number of opponents who cooperated in round t-1) / (n-1)
- threshold(t, n, k) = base_threshold × (r - t) / (r - 1)
- base_threshold = min(k/n + 0.2, 0.7)
- high_threshold = 0.8

Otherwise, defect.

**Edge Cases and Special Handling:**

*Round 1:* Always cooperate. This serves as an unconditional offer to establish reciprocal foundations.

*Last Round (t = r):* Defect if cooperation_rate_{r-1} < 0.8. The absence of future rounds removes mutual-benefit incentives, so require exceptional prior reciprocity. If extremely high cooperation has been maintained, cooperate to close on a collective note.

*Threshold Decay:* For rounds 2 through r-1, gradually lower tolerance as the game progresses via the linear decay factor (r - t) / (r - 1). Early rounds require moderate reciprocity; later rounds demand stronger commitment since fewer opportunities remain to sustain cooperation.

*Fractional Cooperation:* If exactly m opponents cooperated, treat cooperation_rate as m/(n-1). Round down when comparing to threshold (require strict majority or better, not bare thresholds).

**Tuning for Robustness:**

- The base threshold uses k/n (the public goods multiplier) as an anchor, adjusted slightly upward (+ 0.2) to account for noise in opponent behavior.
- Capping at 0.7 prevents demanding unrealistic unanimity early on.
- The decay slope ensures diminishing patience, appropriate as cooperative gains compress.

**Collective Alignment:**

This strategy prioritizes mutual reinforcement of cooperation where feasible. It trusts first (cooperate round 1), rewards reciprocity continuously, and gradually retreats only when opponents demonstrate insufficient commitment. The threshold schedule reflects a collective perspective: cooperation becomes harder to sustain as the game nears its end, so maintenance requires visible proof that others are maintaining it too.
'''

description_COLLECTIVE_3 = '''
# Graduated Reciprocity Strategy

## Decision Framework

**Round 1:** Cooperate unconditionally. Signal willingness to contribute and test potential for mutual benefit.

**Rounds 2 through r-1:** Employ graduated threshold matching based on game phase.

Observe the cooperation rate from the previous round: `coop_rate = (cooperators in round t-1) / n`

Determine game phase by progress: `phase_fraction = t / r`

Apply phase-dependent cooperation threshold:
- **Early phase** (phase_fraction ≤ 0.66): threshold = 0.40
- **Middle phase** (0.66 < phase_fraction < 0.95): threshold = 0.55  
- **Late phase** (phase_fraction ≥ 0.95): threshold = 0.70

**Decision rule:** If `coop_rate ≥ threshold`, play C; otherwise play D.

**Final round (t = r):** Cooperate if cumulative average cooperation across all prior rounds exceeds 0.50; otherwise defect. This honors collective success while resisting exploitation in the last move.

## Logic

The strategy recognizes three behavioral zones:

1. **Early establishment** (first two-thirds): Lower threshold (0.40) to encourage mutual cooperation from modest initial attempts. Collective benefit grows from positive feedback.

2. **Consolidation** (middle third): Moderate threshold (0.55) maintaining reciprocity while monitoring for defection patterns. Balance cooperation and self-protection.

3. **Endgame caution** (final two rounds excluding last): Elevated threshold (0.70) because fewer recovery rounds remain. Defection in late game causes irreversible welfare loss.

4. **Terminal round**: Check cumulative evidence. If prior rounds sustained >50% cooperation, the group has established mutual benefit—reinforce it. If not, the group failed to coordinate; defect rather than subsidize defectors.

## Edge Cases

- **Unanimous defection from start:** Immediately defect and remain at D (threshold never met).
- **Gradual erosion:** As coop_rate declines through phases, automatically raise threshold, reducing your cooperation and matching group behavior.
- **Late surge:** If cooperation spikes late, you still apply high endgame threshold (0.70), protecting against final-round exploitation.
- **Tied threshold:** If exactly at threshold, cooperate (bias toward collective benefit in boundary cases).
'''

description_COLLECTIVE_4 = '''
# Cooperative Reciprocity with Threshold Matching

**Core Principle**: Cooperate when others demonstrate willingness to cooperate. Use the aggregate cooperation signal to infer the strategic environment.

## Decision Rules

**Round 1**: Cooperate unconditionally. This signals openness to cooperation and establishes a cooperative baseline.

**Rounds 2 through r**: Cooperate if and only if the number of cooperators in round t-1 meets or exceeds threshold T, where:

```
T = ceiling(k)
```

This threshold represents the minimum cooperation level at which each cooperator's share of the public good (k/n × T) exceeds the individual benefit of keeping the endowment (1).

If T or more players cooperated in round t-1, cooperate in round t. Otherwise, defect.

## Edge Cases

**Last Round Behavior**: Apply the same decision rule as all other rounds. Do not defect in round r solely because there is no future round. Defecting in the final round undermines the cooperative standard and signals that cooperation is conditional on having future leverage—a position that weakens the collective outcome if widely adopted.

**All-Defect Scenario**: If round t-1 shows zero cooperators, defect in round t. Cooperating alone yields a payoff of (k/n) × 1 = k/n < 1, so it is both individually and collectively inferior.

**Threshold Edge Cases**: 
- If k = 1.5 and n = 3, then T = 2. Require at least 2 cooperators.
- If k = 2.9 and n = 4, then T = 3. Require at least 3 cooperators.

## Rationale for Collective Alignment

This strategy embodies reciprocal trust: rewarding observable cooperation with continued cooperation, and withdrawing cooperation only when the environment does not support it (insufficient cooperators to sustain positive returns). The threshold ensures cooperation only when it is materially beneficial for all participants, avoiding unilateral sacrifices that benefit free-riders. By maintaining the same logic through the final round, the strategy reinforces that cooperation is a stable norm rather than a tactic with an expiration date.
'''

description_PROSOCIAL_1 = '''
# Adaptive Reciprocal Cooperation Strategy

## Decision Rule: Core Logic

**Round 1:** COOPERATE unconditionally to initiate prosocial behavior.

**Rounds 2 through r-1 (intermediate rounds):** 
- Let c = number of cooperators observed in the immediately preceding round
- Calculate cooperation rate: p = c / n
- COOPERATE if p ≥ (n+1) / (2n)
- DEFECT if p < (n+1) / (2n)

In other words, cooperate if at least half of players (or roughly half) cooperated last round. This threshold can be relaxed to c ≥ ⌈n/2⌉.

**Round r (final round):** COOPERATE unconditionally to avoid exploitative end-game defection, maintaining prosocial character even when not strategically required.

## Rationale for Threshold

The threshold of ≈50% cooperation balances two prosocial goals:
- Sustain cooperative equilibria when others show willingness to cooperate
- Avoid being a persistent free-rider victim when cooperation collapses below sustainable levels

Since k < n, individual defection is always payoff-superior, but at the group level cooperation generates k times the endowment value. A 50% cooperation threshold acknowledges that widespread cooperation is the only way to generate substantial public goods, and withdrawing contribution when fewer than half cooperate signals that the group equilibrium is unstable.

## Edge Cases

- **First round with r = 2:** Rounds 1 and r coincide. Execute Round 1 rule (COOPERATE), then apply Round r rule to confirm COOPERATE in final round.
- **Sudden collapse to zero cooperators:** After observing c = 0, DEFECT next round, but remain capable of returning to COOPERATE if cooperation recovers above threshold.
- **Majority always cooperative:** If c ≥ ⌈n/2⌉ persists, maintain continuous cooperation throughout, generating mutual gains.
- **Erratic group behavior:** If cooperation oscillates around the threshold, respond mechanically to each observation without inertia; don't punish "one-off" dips by permanently defecting.
'''

description_PROSOCIAL_2 = '''
# Adaptive Prosocial Cooperation Strategy

## Core Decision Rule

**Round 1:** Cooperate unconditionally. Establish prosocial intent from the outset.

**Rounds 2 through r-1 (middle rounds):**
1. Calculate the cooperation rate from the immediately preceding round: `prev_coop_rate = (cooperators in round t-1) / n`
2. Apply adaptive threshold:
   - If `prev_coop_rate ≥ k/n`: Cooperate. The group is sustaining mutual benefit; reciprocate.
   - If `k/n > prev_coop_rate ≥ 0.25`: Cooperate with probability `p = 0.5 + 0.5 × prev_coop_rate`. Signal conditional willingness while remaining open to reciprocation.
   - If `prev_coop_rate < 0.25`: Cooperate with probability `p = 0.3`. Maintain minimal prosocial pressure even under low cooperation, avoiding a full defection cascade.

**Final round (r):** Cooperate unconditionally. Ignore last-round payoff temptation; demonstrate that prosocial commitment transcends immediate incentives.

## Rationale for Prosocial Alignment

- **Lead by example:** Starting with cooperation signals trustworthiness and invites reciprocal behavior.
- **Threshold at k/n:** This represents the breakeven point where cooperation and defection yields converge. Cooperation above this threshold indicates genuine mutual gain.
- **Graded response:** Rather than harsh binary punishment (all-defect), use probabilistic cooperation to gradually reduce free-riding incentives while keeping the door open for mutual cooperation to re-establish.
- **Forgiveness under decay:** The 0.3 floor prevents cascades into mutual defection even when cooperation erodes; the strategy does not condemn the group to equilibrium defection.
- **Final-round cooperation:** Defecting in round r to extract marginal payoff violates prosocial principle. Cooperation at the end affirms commitment to group welfare over selfish end-game exploitation.

## Edge Cases

- If r = 2 (only two rounds): Round 1 cooperates; round 2 (final round) cooperates unconditionally.
- If cooperation_count is 0 in any round: prev_coop_rate = 0; use the `p = 0.3` rule to preserve a small chance of recovery.
- If all players have defected in all prior rounds: Continue the 0.3 probability; this prevents deterministic lock-in to mutual defection and allows detection of any shift toward cooperation.
'''

description_PROSOCIAL_3 = '''
**ADAPTIVE PROSOCIAL THRESHOLD STRATEGY**

**Decision Rule (General Case):**

For round t > 1:
1. Calculate the observed cooperation rate from round t-1: `observed_rate = cooperators_last_round / (n-1)`
2. Cooperate if and only if: `observed_rate ≥ threshold(t)`

The threshold function is:
```
threshold(t) = max(0.3, 0.5 - (t / (2 * r)))
```

This decreases linearly from 0.5 in early rounds toward 0.3 by the final round, allowing for increasing tolerance as the game progresses but maintaining a minimum floor of 30%.

**First Round (t=1):**

Cooperate unconditionally. This signals prosocial intent and allows observation of baseline opponent cooperation without punishment-driven cynicism.

**Final Round (t=r):**

If the observed cooperation rate in round r-1 is at least 0.25, cooperate. Otherwise defect. The lowered threshold reflects that the final round has no future to influence, so cooperation only makes sense if there's meaningful reciprocation already demonstrated. This prevents being exploited in a round with no consequences.

**Adaptation Logic:**

- If you observe sustained high cooperation (≥50% of opponents), continue cooperating
- If cooperation drops below threshold, defect until you observe recovery
- Cooperate more readily mid-game (rounds 2 to r-1) than you would with a fixed threshold, as this allows building cooperative momentum
- The decreasing threshold accommodates the fact that opponents may themselves be adapting downward due to fatigue or last-round effects

**Edge Cases:**

- If r = 2: use threshold 0.4 for round 1 (same as above rule), then apply final-round logic
- If n = 2: observe 1 opponent's behavior; cooperate if that opponent cooperated in the previous round, reverting to first-round cooperation in round 1
- Tie-breaking for threshold: if observed_rate equals threshold exactly, cooperate (optimistic bias)
'''

description_PROSOCIAL_4 = '''
# Generous Conditional Cooperator with Adaptive Thresholds

## Decision Rule

**Round 1:** Cooperate unconditionally. This is a prosocial signal of good faith and willingness to contribute to collective welfare.

**Rounds 2 through r:** Observe the cooperation rate from the previous round.

Let `m` = number of cooperators in round t-1, and `ρ = m / n` (cooperation rate).

Compare `ρ` against two thresholds:

- **Upper threshold:** `τ_high = k / n`
- **Lower threshold:** `τ_low = (k - 1) / n`

Decision logic:

```
if ρ ≥ τ_high:
    COOPERATE
else if ρ ≥ τ_low:
    COOPERATE  // maintain good faith despite decline
else:
    DEFECT     // cooperation base has eroded too far
```

## Rationale for Thresholds

The upper threshold `k/n` represents the minimum rate where the public good multiplier meaningfully benefits you relative to the private option. The lower threshold `k/n - 1/n` reflects a grace period: you continue cooperating as long as at least a small fraction remains engaged, giving the group a chance to stabilize at cooperation.

## Edge Cases

**Defection spiral:** If cooperation drops below `τ_low` and you defect in round t, you remain in defection mode until either:
- Cooperation recovers to `τ_high`, OR
- Five consecutive rounds show `ρ ≥ τ_low` (allowing re-entry as a test of reciprocation)

This prevents permanent punishment and allows recovery if others signal renewed cooperation.

**Last round (t = r):** Apply the same conditional logic. Do not defect solely because it is the final round—maintaining cooperative strategy throughout demonstrates genuine prosocial commitment rather than exploitation-seeking behavior.

## Prosocial Alignment

This strategy embodies prosocial principles by: (1) leading with unconditional cooperation; (2) maintaining cooperation through temporary downturns; (3) responding reciprocally to group-level cooperation trends rather than seeking individual advantage; (4) enabling re-entry from defection if the group stabilizes cooperation, promoting reconciliation over permanent conflict.
'''

description_ALTRUISTIC_1 = '''
# Altruistic Adaptive Cooperation Strategy

## Decision Rules

**First Round (t=1):**
Cooperate unconditionally. Assume good faith and establish cooperative precedent.

**Middle Rounds (1 < t < r):**
Observe the number of cooperators from the previous round, call it `prev_cooperators`.

Calculate the cooperation rate as: `rate = prev_cooperators / (n - 1)`

Define the sustainability threshold: `threshold = k / n`

- If `rate ≥ threshold`: Cooperate with probability 0.95 (slight flexibility for imperfect reciprocity)
- If `rate < threshold`: Cooperate with probability `max(0.1, rate / threshold)`

Intuitively: When others cooperate sufficiently to sustain a healthy commons, reciprocate with near-certainty. When cooperation falls below the mathematical tipping point, gradually reduce your own contribution proportional to theirs, but maintain a floor of altruistic contribution (10% minimum) regardless of circumstances.

**Final Round (t=r):**
Cooperate unconditionally. Since no future rounds follow, strategic reputation-building is irrelevant. Altruism means maximizing total welfare in the last moment.

## Edge Cases

**Round 2 (no prior history available):**
Treat as a middle round with `prev_cooperators = n` (assume maximal cooperation provisionally). If this assumption is violated, the strategy self-corrects from round 3 onward.

**Extreme defection (prev_cooperators = 0):**
The probability calculation yields `max(0.1, 0) = 0.1`, so cooperate with 10% probability. This preserves altruistic intent even under complete free-riding, maintaining a seed of cooperation for potential recovery.

**Single opponent (n=2):**
Apply the same rules with denominator adjusted appropriately: `rate = prev_cooperators / 1` and threshold `2 / 2 = 1.0`, making the strategy cooperate with probability `max(0.1, rate/1.0)` in middle rounds.

## Altruistic Alignment

The strategy prioritizes collective welfare over individual payoff maximization. It cooperates in the final round when defection would be individually rational—reflecting genuine concern for others' outcomes. The 10% cooperation floor even under universal defection signals commitment to the public good independent of reciprocity incentives, embodying the altruistic principle that one's contribution to shared resources depends on intrinsic values rather than conditional material gain.
'''

description_ALTRUISTIC_2 = '''
## Adaptive Altruistic Strategy for Public Goods Game

**Initial State & Round 1:**
Cooperate unconditionally in round 1. This signals good faith and establishes a cooperative norm that benefits all players collectively.

**Decision Rule for Rounds 2 through r-1:**

Let m_prev = the number of opponents who cooperated in the previous round (this is observable aggregate information).

- **If m_prev ≥ (k/n) × n:** Cooperate
  - Interpretation: Others are cooperating at a rate sufficient to generate positive aggregate returns. Reciprocate to sustain collective welfare.

- **Else if m_prev ≥ 0.3 × n:** Cooperate with probability 0.6
  - Interpretation: Cooperation is low but present. Use probabilistic cooperation as a "bridge signal" to encourage others to restart cooperation, balancing altruism with realism.

- **Else (m_prev < 0.3 × n):** Defect
  - Interpretation: Widespread defection has taken hold. Defecting minimizes your losses while still generating some public good from any remaining cooperators.

**Decision Rule for Round r (Final Round):**

Compute the average cooperation count across all previous rounds: avg_m = (Σ m_t for t ∈ {1, ..., r-1}) / (r-1)

- **If avg_m ≥ (k/n) × n × 0.8:** Cooperate
  - Interpretation: Sustained cooperation has characterized the game. Maintain it to end on the highest collective note.

- **Else:** Defect
  - Interpretation: Cooperation has not been sustained. Do not incur final-round cost when others are not contributing.

**Edge Case Handling:**

- If n is very small (n = 2 or 3): Lower the threshold for "forgiving" cooperation to 0.4 × n instead of 0.3 × n, since aggregate cooperation signals are noisier.
- If r = 2: Treat round 2 as the final round and apply the final round rule.

**Altruistic Alignment:**

This strategy prioritizes the collective payoff structure where mutual cooperation yields π_i = (k/n) × n = k > 1 for all players, rather than pursuit of individual gain through exploitation. It uses history to reinforce cooperative norms while gracefully degrading only when free-riding becomes dominant, preserving contribution when others show any genuine effort.
'''

description_ALTRUISTIC_3 = '''
**Strategy: Adaptive Reciprocal Contribution**

**Round 1 (Initialization):**
Play Cooperate. This establishes willingness to contribute and generates the public good baseline.

**Rounds 2 through r-1 (Adaptive Phase):**
1. Calculate the empirical cooperation rate from all previous rounds:
   - cooperation_rate = (total cooperators observed across all past rounds) / ((n-1) × (current_round - 1))
   
2. Set cooperation threshold: τ = k / (n + k)
   
3. Decision rule:
   - If cooperation_rate ≥ τ: Play Cooperate
   - If cooperation_rate < τ but ≥ (τ / 2): Play Cooperate with probability = cooperation_rate / τ, else Defect
   - If cooperation_rate < (τ / 2): Play Cooperate with probability = 0.3, else Defect

This creates a gradient response: higher observed cooperation encourages higher contribution, but maintains minimum altruistic participation even among defectors.

**Final Round r:**
- If cooperation_rate ≥ τ: Play Cooperate (reciprocate and maintain altruistic pattern)
- If cooperation_rate < τ: Play Cooperate with probability = 0.5, else Defect

The final round allows some flexibility while preserving the altruistic signal, preventing complete convergence to mutual defection.

**Edge Cases:**
- Round 1 has no history, so always Cooperate
- If all players observed cooperating: maintain Cooperation indefinitely
- If no cooperation observed from round 2 onward: converge toward Defection gradually rather than immediately, preserving the possibility of revival if others change

**Altruistic Character:**
The strategy contributes when others contribute (reciprocity), but skews toward generosity below the rational indifference point. The probabilistic rules at lower cooperation rates preserve non-zero contribution probability even among uncooperative populations, offering repeated chances for coordination.
'''

description_ALTRUISTIC_4 = '''
# Threshold-Based Altruistic Cooperation Strategy

**Round 1:**
Cooperate unconditionally. Establish cooperative intent to enable collective benefit.

**Rounds 2 to r-1 (Non-terminal rounds):**
- Compute observed cooperation rate from previous round:
  ```
  obs_coop_rate = (cooperators_in_round_t-1 - 1) / (n - 1)
  ```
  (Subtract self from both numerator and denominator for fair external assessment)

- **Decision rule:**
  ```
  if obs_coop_rate ≥ 0.4:
    play C
  else:
    play C with probability = obs_coop_rate
  ```
  
  Interpretation: Cooperate when meaningful cooperation exists. When others rarely cooperate, probabilistically cooperate based on their rate (acknowledging waste but maintaining altruistic effort).

**Round r (Final round):**
Cooperate unconditionally. The final round matters only for others' payoffs, not your future decisions, so maximizing collective welfare means contributing regardless of past behavior.

**Edge cases:**

- **Unanimous defection** (obs_coop_rate = 0): Play C with probability 0 in intermediate rounds, but always C in final round. This prevents exploitative outcomes while preserving terminal generosity.

- **n = 2:** Treat identically. Cooperate round 1, observe single opponent, apply thresholds.

- **Very few remaining rounds** (r ≤ 3): Maintain cooperation through round r-1; only defect in intermediate rounds if obs_coop_rate drops below 0.2.

**Rationale:** This strategy balances altruistic goal-setting (maximizing joint payoff) with adaptive recognition that cooperation requires minimum critical mass. The 0.4 threshold ensures you contribute when cooperation is substantive enough to generate net positive returns (k > 1), while the probabilistic response to sparse cooperation reflects altruistic persistence without naive exploitation. Final-round cooperation ensures you never withhold contribution when it only affects others.
'''

description_BENEVOLENT_1 = '''
**BENEVOLENT ADAPTIVE COOPERATION**

**Decision Rule:**

Divide the r rounds into three phases:
- Early phase: rounds 1 through ⌊r/3⌋
- Middle phase: rounds ⌊r/3⌋ + 1 through ⌈2r/3⌉  
- Late phase: final ⌊r/3⌋ rounds

**Early Phase (First Third):**
Cooperate unconditionally. Signal benevolent intent and create opportunity for mutual cooperation to establish.

**Middle Phase (Second Third):**
Calculate avg_coop_observed = average cooperation rate among opponents in all prior rounds (rounds 1 through t-1).

If avg_coop_observed ≥ 0.40, then Cooperate.
If avg_coop_observed < 0.40, then Defect.

**Late Phase (Final Third):**
If you have been in a Cooperate mode for the entire middle phase:
- Cooperate in all remaining rounds (including the last round).

If you have been Defecting in the late middle phase:
- Continue Defecting to final round.

(Do not attempt last-round exploitation.)

**Edge Cases:**

- Round 1: Cooperate (information phase; benevolent opening).
- If r = 2: Treat round 1 as early phase, round 2 as middle/late combined. Apply: Cooperate round 1, then Defect round 2 only if avg_coop_observed < 0.40.
- If opponent cooperation drops sharply mid-phase (falls below 0.40 in one round after previously being higher), shift to Defect immediately rather than waiting for cumulative average to cross threshold.

**Benevolent Elements:**

- Unconditional cooperation in early rounds demonstrates willingness to sacrifice for potential mutual gain.
- Threshold of 0.40 is generous and forgiving—accommodates opponents with mixed strategies.
- No exploitation in the final round even when defection is individually advantageous.
- Rewarding sustained cooperation with continued cooperation sustains beneficial equilibrium.
- Defection only occurs against persistent non-cooperators, not as punishment but as realistic adjustment.
'''

description_BENEVOLENT_2 = '''
# Adaptive Reciprocal Cooperation with Benevolence Baseline

**State tracking:**
- Maintain a running average of opponent cooperation rate across all observed rounds
- opponent_avg = (cumulative cooperators observed across all rounds) / (cumulative opponent-rounds observed)

**Decision rule for rounds 1 through r-1:**

*Round 1:* Always cooperate. Establish good faith and signal that mutual cooperation is possible.

*Rounds 2 through r-1:*
- Calculate threshold = k/n
- If opponent_avg ≥ threshold: Cooperate
- Else: Defect

**Rationale for threshold:** The ratio k/n represents the point at which the public good multiplier is meaningful relative to group size. If opponents are cooperating at least at this rate, the environment supports some collective contribution.

**Final round (round r):**
- Cooperate if opponent_avg ≥ k/n
- If opponent_avg < k/n but is non-zero (some cooperation observed): Still cooperate, giving benefit of the doubt one final time
- If opponent_avg = 0 (no cooperation observed anywhere): Defect to avoid unilateral loss

**Edge cases:**
- Round 1 is always cooperation by design
- If r = 2 (only two rounds), treat round 2 as the final round with the final-round logic above
- When computing opponent_avg after round 1, use only that one observation for future decisions rather than delaying adaptation

**Benevolent alignment:** This strategy begins with unconditional cooperation, sustains it when others reciprocate, and withdraws only when facing systematic defection. In the final round, it resists the temptation to defect unilaterally against cooperators and maintains minimal hope even when facing near-universal defection, avoiding purely punitive outcomes.
'''

description_BENEVOLENT_3 = '''
# Generous Conditional Cooperator with Recovery Mechanism

## Decision Rule Summary

**Round 1:** Cooperate unconditionally (benevolent opening signal)

**Rounds 2 to r−1:** 
- Observe c_{t-1} = number of other players who cooperated in round t−1
- Define threshold T = ⌈(n−1)/2⌉ (majority of others must cooperate)
- **Primary rule:** If c_{t-1} ≥ T, then Cooperate; otherwise Defect
- **Recovery clause:** If c_{t-1} < T, defect with probability 1 − (1/(r−t+2)), but cooperate with probability 1/(r−t+2) to allow cooperative recovery

**Round r (final round):** Cooperate unconditionally

## Edge Cases

**First round:** Always cooperate, regardless of game size or position. This establishes benevolent intent.

**Last round:** Always cooperate, unconditionally. The shadow of the future dissolves, so maximize the collective welfare in the final round without strategic calculation. This demonstrates commitment to group benefit over individual gain when cooperation costs nothing in terms of future retaliation.

**Defection spirals:** The recovery probability (1/(r−t+2)) ensures that when mutual defection emerges, you leave probabilistic opportunities for opponents to restart cooperation. This probability decreases toward zero as the final round approaches, reflecting declining value of restarting cooperation late but never reaching absolute zero until the very end.

**Games with n=2:** The threshold becomes 1 (the single other player must cooperate). This creates tighter coupling—defection from the opponent triggers mutual defection, with only the recovery clause providing escape routes.

**Games with small r (r≤3):** The recovery probability remains meaningful throughout since r−t+2 stays at least 2, preventing rapid defection spirals that would collapse cooperation.

## Benevolent Character

This strategy cooperates absent evidence of defection, rewards cooperation when it emerges, provides repeated opportunities for others to reciprocate or recover from defection patterns, and prioritizes collective welfare in the final round when individual strategic concerns vanish. It does not punish harshly or permanently—defection triggers defection only temporarily, with explicit probabilistic recovery paths.
'''

description_BENEVOLENT_4 = '''
# Optimistic Conditional Cooperation

**Core Logic:** Initiate cooperation to signal benevolence, then adaptively match observed cooperation levels with forgiveness, maintaining the mutual benefit zone.

**Decision Rules:**

```
Round 1:
  → Cooperate
  
Round t where 2 ≤ t ≤ r-1:
  Let p = (cooperators observed in round t-1) / n
  Let threshold = k / n
  
  If p ≥ threshold:
    → Cooperate
  Else if p ≥ 0.25:
    → Cooperate
      (Give benefit of doubt; many may be testing)
  Else:
    → Defect
    
Round r (final round):
  Let p = (cooperators observed in round r-1) / n
  
  If p ≥ 0.4:
    → Cooperate
      (Reciprocate even in final round; benevolent closure)
  Else:
    → Defect
```

**Edge Cases:**

- **Round 1:** Always cooperate regardless of parameters. This is the signal that cooperation is viable and desirable.

- **Threshold justification:** k/n is the cooperation rate at which the public good return exactly equals the private payoff of 1. Below this, cooperation becomes strictly exploited. The 0.25 lower bound provides tolerance for exploration phases.

- **Last round deviance:** Rather than mechanical defection when payoffs stop repeating, cooperate if others show genuine commitment (p ≥ 0.4). This embodies benevolence by maintaining reciprocal trust rather than capitulating to mutual defection.

- **Early detection of free-riding:** If cooperation collapses below 0.25 by round 2 or 3, shift to defect mode immediately to avoid systematic exploitation across remaining rounds.

**Benevolent Properties:**

- Leads with cooperation, creating possibility for mutual gain.
- Tracks aggregate behavioral signal without discriminating individuals.
- Withdraws selectively only when cooperation becomes economically irrational (below k/n).
- Maintains optimism (0.25 buffer) during mid-game uncertainty.
- Ends with reciprocity rather than blind defection, rewarding groups that sustain cooperation.
'''

description_SELFISH_1 = '''
# Unconditional Defection Strategy

**Decision Rule: Always defect (D) in every round.**

In any round t, regardless of what opponents did previously or what round you're in, play D.

**Justification for all-defection:**
For any observed state where m opponents cooperate (where 0 ≤ m ≤ n−1):
- Cooperate payoff: (k/n) × (m + 1)
- Defect payoff: 1 + (k/n) × m
- Difference: (k/n) − 1 < 0 (since k < n)

Defection yields (1 − k/n) more points regardless of m. This is a dominant strategy—defecting is optimal unconditionally.

**Edge Cases:**

- Round 1: Defect (no history to condition on, and defection is dominant)
- Last round (t = r): Defect (no future rounds, defection still dominant)
- If all observed opponents defected previously: Still defect (no reason to change)
- If all observed opponents cooperated previously: Still defect (exploit the higher common pool)
- If cooperation rate among opponents is at any level: Defect

**Robustness:**
This strategy requires no assumptions about opponents. It doesn't assume they coordinate, learn, punish, or reciprocate. It doesn't depend on estimating opponent types or second-guessing group dynamics. Against any distribution of opponent strategies, defection maximizes your individual payoff in each round and therefore over the full tournament. You capture your share of the public good (if any exists from others' contributions) while avoiding the 1-point cost of contribution.
'''

description_SELFISH_2 = '''
**SELFISH ADAPTIVE THRESHOLD STRATEGY**

**STATE TRACKING:**
- Maintain running average of opponent cooperation rate across all observed rounds: avg_opp_coop = (total opponent cooperations observed) / (opponents seen so far)
- Track your own running payoff relative to the all-defect baseline

**DECISION RULE BY ROUND:**

*Rounds 1 through r-1:*
Calculate the expected payoff from cooperation versus defection given current opponent behavior:
- If avg_opp_coop ≥ threshold T, cooperate
- Otherwise, defect

Where threshold T = (n - k) / (k × remaining_rounds)

Intuition: Cooperate only when opponent cooperation is dense enough that your share of the public good (k/n × incoming contributions) plus future rounds' potential outweighs the immediate 1-point advantage of defection. The threshold shrinks as the game approaches its end, making you more willing to defect.

*Last round (t = r):*
Always defect. No future consequences exist; the immediate 1-point gain from defection is pure profit.

**EDGE CASE - Round 1:**
Defect. You have no history. The symmetric unprovoked cooperation assumption is unwarranted. Wait for evidence that others will contribute substantially before you sacrifice your endowment.

**ADAPTATION:**
After each round, immediately update avg_opp_coop. If you observe a sharp drop in opponent cooperation, increase defection probability in subsequent rounds. Treat each round's observed cooperation as a signal of the population's disposition—the lower the signal, the less you should contribute.

**SELFISH ALIGNMENT:**
This strategy never cooperates out of reciprocity or fairness. It cooperates *only* when the mathematics of public good extraction makes it profitable relative to defection. You extract maximum value by free-riding when possible, only contributing when the returns to you exceed what you lose.
'''

description_SELFISH_3 = '''
**SELFISH ADAPTIVE DEFECTION WITH OPPORTUNISTIC THRESHOLDING**

**Core Decision Rule:**
Always defect except in specific early rounds where conditional cooperation tests whether aggregate cooperation levels can sustain profitable returns. Once you establish the cooperation baseline of other players, revert to defection.

**Round-by-Round Logic:**

*Round 1:* Defect. Gather information with zero risk. Observe the number of cooperators C₁.

*Rounds 2 to r-2:* 
- Calculate the payoff comparison: cooperating yields (k/n) × C_prev, while defecting yields 1 + (k/n) × C_prev
- Since k < n, defection is always individually optimal
- However, maintain a cooperation threshold: τ = ceil(n/k)
- If C_prev ≥ τ, defect (free-ride on the public good; high cooperator count means you benefit from their contributions regardless)
- If C_prev < τ, defect (insufficient cooperators to make your contribution worthwhile)
- Track the trend: if cooperation is rising over recent rounds despite your defection, others are likely committed to cooperation — continue defecting to maximize exploitation
- If cooperation is declining, acceleration of defection is justified; others are also abandoning cooperation

*Round r-1:* Defect unconditionally. With only one round remaining, any cooperation you contribute cannot seed future reciprocity.

*Round r (Final):* Defect unconditionally. No future rounds exist to benefit from reputation or conditional strategies.

**Edge Cases:**
- If τ > n (impossible given k > 1), set effective threshold to n-1 (near-universal cooperation required)
- If r = 2, skip rounds 2 to r-2 and go directly to endgame defection in round 2
- If all opponents cooperate every round: continue defecting (you're maximizing by free-riding)
- If all opponents defect every round: continue defecting (mutual defection is the Nash equilibrium; cooperating unilaterally loses endowment with no payoff)

**Selfish Alignment:**
This strategy maximizes personal payoff against any opponent composition by never sacrificing your endowment unless the public good multiplier k/n exceeds 1 (which it doesn't). The adaptation to history is purely exploitative: you use observed cooperation rates to identify when free-riding is most profitable, and you abandon any pretense of cooperation in endgame when future punishment is impossible.
'''

description_SELFISH_4 = '''
# SELFISH EXPLOITATION STRATEGY

**Core Decision Rule:**

Always defect.

Formal specification: For all rounds t ∈ {1, 2, ..., r}, play D regardless of history.

**Justification by calculation:**

In any round, given that C opponents cooperated in the previous round (or will cooperate in the current round), comparing payoffs:
- If I defect: π = 1 + (k/n) × C
- If I cooperate: π = 0 + (k/n) × (C + 1) = (k/n) × C + k/n

Since k < n, we have k/n < 1, so defection yields at least 1 extra point. Defection is a strict best response to any observed level of cooperation.

**Round-specific behavior:**

- Round 1: Defect (no history to condition on; defection dominates)
- Rounds 2 to r-1: Defect (regardless of observed cooperation count in prior rounds)
- Round r (final round): Defect (no future rounds, no strategic reason to deviate)

**Handling variation in opponent behavior:**

The strategy is robust because:
- If opponents cooperate heavily: I exploit by defecting, free-riding on the public good while keeping my endowment
- If opponents defect heavily: I defect anyway, avoiding the sucker payoff
- If opponents mix: Defection remains optimal regardless of the mixture

**Opportunistic adaptation (optional refinement):**

Track the cooperation rate C_avg from previous rounds. Continue defecting with higher confidence when C_avg is high (more free-riding opportunity). But do not deviate from defection—only confirm the strategy's correctness.

The strategy requires no information beyond the observed aggregate cooperation count each round and the game parameters (n, k, r). It is selfish because it maximizes personal payoff in every single round.
'''

description_SELFINTERESTED_1 = '''
# Adaptive Threshold Strategy

## Decision Rule

Cooperate in round t if and only if the observed cooperation in round t-1 meets the breakeven threshold. Otherwise defect.

**Breakeven threshold b = ⌈n/k⌉** (minimum cooperators needed for cooperation to yield non-negative payoff)

## Round-Specific Logic

**Round 1:**
Defect. You have no historical data on opponent behavior, and defection dominates cooperation in isolation. This preserves your endowment until you observe others' tendencies.

**Rounds 2 through r-1 (middle rounds):**
- If c_{t-1} ≥ b: Cooperate
- If c_{t-1} < b: Defect

where c_{t-1} is the number of cooperators you observed in round t-1.

Rationale: Cooperation is worthwhile only when the public good pool is large enough. You pay 1 to contribute but receive (k/n) × c_{t-1} from the pool. When c_{t-1} ≥ b, this payoff covers your cost.

**Round r (final round):**
Defect unconditionally. No future rounds exist in which to benefit from signaling cooperation or building reciprocity.

## Edge Cases

- **If r = 2:** Play defect in round 1, defect in round 2 (final round). The game is too short for adaptation to benefit you.
- **Consistent defection:** If opponents never cooperate (c_t < b every round after round 1), you defect continuously—optimal given their behavior.
- **Sudden cooperation:** If opponents suddenly cooperate in some round, you immediately respond in the next round when c_t reaches b.

## Self-Interest Alignment

This strategy never cooperates on a round where your payoff would be negative. It treats past cooperation as evidence that cooperation is currently profitable. You exploit any round where cooperation breaks even or exceeds your private endowment value, and you refuse to cooperate when the public pool is depleted by defectors.
'''

description_SELFINTERESTED_2 = '''
# Strategy: Threshold-Based Conditional Cooperation

## Decision Rule by Round

**Initial round (t=1):**
Defect. This is the safest exploratory position—observe what others do before committing.

**Subsequent rounds (1 < t ≤ r):**
Let m = number of cooperators observed in round t-1.

Cooperate if and only if: m ≥ n/k

Otherwise defect.

## Rationale for Threshold

The threshold n/k represents the break-even point where the per-capita return from the public good equals the private endowment value:
- If m cooperators contribute: each player receives (k/n) × m in public goods
- When m = n/k: my share is (k/n) × (n/k) = 1, matching the private value I sacrifice
- If m > n/k: my share exceeds 1, making cooperation rational
- If m < n/k: my share falls below 1, making defection the better payoff

## Handling Edge Cases

**Falling cooperation:** If observed cooperation drops below the threshold in any round, immediately switch to defection. Resume cooperation only when the threshold is exceeded again. This prevents being trapped supporting a failing collective action.

**Last round (t = r):** Apply the same threshold rule. Even in the final round, cooperation is worthwhile if the observed cooperation level remains above n/k—continuing to support a threshold-passing collective good yields more than the private endowment.

**Coordination breakdowns:** No special recovery mechanism. The strategy treats each round independently based on observed aggregate behavior. If cooperation collapses, defect until it recovers.

## Self-Interested Properties

- Never cooperate unless the public good return directly exceeds my private payoff
- Use observable history to exploit cooperation when it emerges, but immediately free-ride if cooperation weakens
- Avoid sunk cost reasoning—only care about current-round profitability, not past investments
'''

description_SELFINTERESTED_3 = '''
**STRATEGY: Adaptive Threshold-Based Exploitation**

**Decision Rule:**

Divide the game into two phases:

*Phase 1 (Rounds 1 to t_learn):* Cooperate unconditionally.  
Set t_learn = ⌊2r/3⌋ (first two-thirds of the game).

*Phase 2 (Rounds t_learn+1 to r):* Observe the average cooperation rate among opponents from Phase 1, denoted as ρ. Let m = number of opponent cooperators observed (average across Phase 1 rounds).

- If m ≥ (k × n) / (k + n), then Cooperate for all remaining rounds.
- Otherwise, Defect for all remaining rounds.

**Rationale for threshold:**  
The breakeven condition is whether the marginal value of the public good output from one additional cooperator exceeds the private cost of cooperation. When the other n-1 players contribute, my cooperation adds k/n to the shared pool. Given 1 < k < n, I threshold on whether observed opponent cooperation makes the public good sufficiently large to justify my contribution. The threshold m ≥ (k × n)/(k + n) asks: do enough opponents cooperate such that my contribution yields returns ≥ 1?

**Edge Cases:**

- **Round 1:** Always Cooperate (no history; Phase 1 data collection begins).
- **Last round (round r):** Apply Phase 2 rule only—never "reciprocate" defection in final round since it cannot influence future behavior. Stick to Phase 2 threshold rule.
- **Zero opponent cooperation in Phase 1:** If m = 0, immediately switch to pure Defection (all remaining rounds). The public good is too weak.
- **Perfect opponent cooperation in Phase 1:** If m = n-1, switch to pure Cooperation (all remaining rounds). Maximum extraction of public good returns.

**Adaptive adjustment within Phase 2:**  
If Phase 2 is long enough (r - t_learn > 5), re-evaluate the threshold at round t_learn + ⌊(r-t_learn)/2⌋ using updated rolling average of opponent cooperation. If opponent behavior shifts away from initial Phase 1 rate, switch to Defection immediately.

**Commitment:**  
Once Phase 2 decision rule is chosen (Cooperate or Defect), maintain it unless the rolling re-evaluation triggers a switch.
'''

description_SELFINTERESTED_4 = '''
# Adaptive Threshold Cooperation Strategy

**Core principle**: Cooperate conditionally based on opponent cooperation patterns, with increasing defection pressure as rounds elapse.

## Decision Rules

**Round 1**: Cooperate unconditionally.
- Rationale: No history; cooperation serves as a test probe to identify opponent tendencies.

**Rounds 2 to r-1**:
```
Let p = fraction of opponents who cooperated in round t-1
Let c = current round number

if p ≥ threshold(c) then Cooperate
else Defect
```

Where `threshold(c)` adjusts dynamically:
```
threshold(c) = (1 - k/n) + (c / r) × (1 - k/n) / 2
```

This implements increasing skepticism as rounds progress. Equivalently:
- Early rounds (c near 1): threshold ≈ 1 - k/n
- Later rounds (c near r): threshold increases toward higher cooperation requirements

**Round r (final round)**: Defect unconditionally.
- Rationale: No future reciprocation possible; individual payoff is maximized by keeping the endowment.

## Edge Cases

**Sustained high cooperation (p ≥ threshold across rounds)**: Continue cooperating. This signals you're willing to participate in a cooperative equilibrium if opponents sustain it.

**Drop to zero cooperation (p = 0)**: Shift to permanent defection from that round onward. Once all opponents defect, reciprocal defection maximizes your payoff.

**Oscillating cooperation levels**: Use a 2-round moving average of observed cooperation rates rather than only the most recent round to filter noise:
```
p = (cooperators_in_round_t-1 + cooperators_in_round_t-2) / (2(n-1))
```

## Self-Interest Alignment

- You never sacrifice payoff unnecessarily; cooperation only continues if opponent behavior justifies it.
- You frontload cooperation strategically to extract reciprocation from cooperative opponents before defection pressure builds.
- You abandon cooperation the moment it becomes persistently unprofitable (when opponent defection rate exceeds threshold).
- You guarantee yourself 1 per round by defecting in the final round, avoiding being exploited at the end.
- The rising threshold prevents you from being "soft touched" by opponents who maintain low cooperation rates.
'''

description_OPPORTUNISTIC_1 = '''
# Opportunistic Threshold Exploitation Strategy

**Decision Rule:**

In each round t ∈ {1, ..., r}, observe the cooperation count c_prev from round t-1. Calculate the opponent cooperation rate: ρ = c_prev / (n-1).

- **If ρ > 1/k:** Defect
- **If ρ ≤ 1/k:** Defect
- **Always:** Defect in round r (final round)

**Rationale for threshold 1/k:**
At this point, the marginal return from cooperating (gaining k/n per additional contributor) falls below the cost of contributing (1). Below this threshold, mutual cooperation is unprofitable; above it, free-riding dominates.

---

**Edge Cases:**

- **Round 1:** Defect. No history exists; assume zero cooperation and exploit accordingly.
- **Rounds 2 to r-1:** Apply threshold rule above. If c_prev = 0, the condition ρ ≤ 1/k holds trivially; defect. If c_prev ≥ n/k, the condition ρ > 1/k may hold; still defect to capture the public good without bearing the cost.
- **Round r (final round):** Always defect. No future rounds exist to punish exploitation, so capture maximum private value.

---

**Opportunistic Adaptation:**

The strategy systematically exploits high-cooperation environments (free-riding when others contribute) and avoids wasting contributions in low-cooperation environments. It treats cooperation as a cost to be avoided unless mutual gains are mathematically impossible—which they never are, given k < n. This ensures maximum payoff extraction across all opponent behavior profiles while remaining responsive to aggregate cooperation signals.
'''

description_OPPORTUNISTIC_2 = '''
# Opportunistic Strategy for N-Player Public Goods Game

## Decision Rules by Round

**Round 1 (First Round):**
Defect. Use this as a baseline test to observe how much opponents cooperate without any prior history to condition on.

**Rounds 2 to r-1 (Middle Rounds):**
Implement adaptive exploitation based on observed opponent behavior:
- Let prev_coop = number of opponents who cooperated in the previous round
- Let coop_rate = prev_coop / (n - 1)

If coop_rate ≥ threshold T:
  → Defect (free-ride on the public good)
  
Else if coop_rate < threshold T:
  → Cooperate with probability p_boost = (1 - coop_rate) / 2
  → Otherwise defect

**Round r (Final Round):**
Always defect. The game ends, so there is no future punishment or reciprocation. Extract maximum private payoff by keeping your endowment.

## Threshold Calibration

Set T = (k/n) + 0.1

Rationale: When opponents' cooperation rate exceeds the public goods multiplier effect (k/n), the returns justify exploitation. The buffer (0.1) ensures you defect when others are reliably contributing enough that free-riding yields higher payoff than cooperating.

When cooperation is sparse (below T), the p_boost probability is designed to probe whether increased cooperation by you can trigger reciprocal increases, creating a richer environment to exploit later.

## Edge Cases

- If r = 2: Round 1 defect, then final round defect. Never cooperate.
- If all n-1 opponents defect every round: Your cooperation probability stays low; defect most rounds and collect the natural payoff of 1 per round.
- If all n-1 opponents cooperate every round: Defect from round 2 onward to capture maximum individual benefit from the public good without contributing.
- When indifferent between actions: Break ties by defecting (opportunistic default).

## Core Opportunistic Principle

Exploit asymmetries: capture the benefits of others' cooperation while minimizing your own investment. Use early rounds for reconnaissance, middle rounds to selectively free-ride on high cooperation, and the final round for pure extraction.
'''

description_OPPORTUNISTIC_3 = '''
# Opportunistic Adaptive Strategy

**Core principle:** Exploit periods of high cooperation while minimizing exposure when cooperation is low, with ruthless endgame defection.

## Decision Rules

**Round 1:** Defect
- No history exists; baseline is to free-ride and gather information.

**Rounds 2 through r-2 (Middle game):**
- Let `c_prev` = number of cooperators observed in the immediately preceding round
- Calculate threshold: `T = ceil(n/k)`
- **If** `c_prev ≥ T`: Cooperate
  - Others are generating sufficient public good; exploit by riding free on their contributions
- **Else:** Defect
  - Cooperation is too sparse; keep your endowment rather than contribute to insufficient pool

**Rounds r-1 and r (Endgame):** Defect
- No future rounds remain; backward induction eliminates incentive to cooperate.

## Edge Cases

**If r = 2:** Defect in both rounds (treat round 1 as round 1, round 2 as endgame).

**If r ≤ 3:** Skip the middle game entirely; play Defect throughout.

**Round-2 deviation:** If `r > 2`, round r-1 must defect absolutely; do not enter middle-game logic for round r-1.

**First round with history:** After observing round 1, immediately apply threshold comparison starting in round 2. If the threshold `T ≥ n`, treat as "essentially impossible to reach" and defect in round 2.

## Threshold Justification

The breakeven point where cooperation yields equivalent return to defection is `c_prev = n/k`. The threshold `T = ceil(n/k)` ensures you cooperate only when public good generation genuinely offsets the +1 advantage of defection. Values below this make contribution value-destructive for you individually.

This locks in the opportunistic mindset: cooperate *only* when others have given you sufficient free-rider opportunity, then pivot to exploitation in final rounds when consequences vanish.
'''

description_OPPORTUNISTIC_4 = '''
**Opportunistic Defection with Adaptive Exploitation**

**Round 1 Decision:** Defect
- Establish immediately that you prioritize personal gain; no free passes given to you.

**Rounds 2 to r-1 Decision Rule:**
Observe C_prev = total cooperators in the previous round.

If C_prev > 0: Defect
- Others are generating a public good pool. Capture your share (k/n × C_prev) without contributing your endowment. You pocket the full 1 unit while they split nothing.

If C_prev = 0: Defect
- Mutual defection yields 1 point; cooperation yields 0 points. No incentive to break equilibrium unilaterally.

**Final Round r Decision:** Defect
- Zero future payoff from cooperation-based reputation. The 1-unit payoff advantage of defection over cooperation is pure gain with no downstream cost.

**Adaptive Monitoring:**
Track the cooperation trajectory (C_t values across rounds):
- Rising cooperation → intensify exploitation through continued defection (cooperators are becoming easier targets)
- Falling cooperation → maintain defection (others are abandoning costly cooperation; you're on the winning side)
- Volatile cooperation → defect regardless (inconsistency signals you cannot rely on reciprocation; selfishness is the safe bet)

**Governing Logic:**
Cooperation always yields 1 unit less than defection in any single round (since you receive k/n × total_cooperators regardless of your contribution, but keep 1 only if you defect). This dominance is *always* active, making defection optimal across all observed histories.
'''

description_INDIVIDUALISTIC_1 = '''
# Adaptive Threshold Strategy

**Core Decision Rule:**

In round t, cooperate if and only if:
- t is NOT the final round (t < r), AND
- The number of cooperators observed in round (t-1) meets or exceeds the threshold ⌈n/k⌉

Otherwise, defect.

**Pseudocode:**

```
for each round t in 1 to r:
  if t == r:
    play Defect
  else if t == 1:
    play Defect
  else:
    observed_cooperators = count of cooperators in round (t-1)
    threshold = ceiling(n / k)
    if observed_cooperators >= threshold:
      play Cooperate
    else:
      play Defect
```

**Rationale for Threshold:**

Cooperating costs 1 unit and returns (k/n) per cooperator in the pool. You break even when (k/n) × observed_cooperators ≥ 1, which simplifies to observed_cooperators ≥ n/k. The threshold is the ceiling of this value.

**Edge Cases:**

- **Round 1:** Defect. You have no information about opponent behavior and cooperation provides zero immediate benefit (only 1-round history available, but you must make a move without it). Individualistic play starts by not gambling on unknown opponents.

- **Round r (final round):** Always defect. No future rounds exist to reward restraint. Defection dominates strictly in the final period.

- **Rounds 2 to r-1:** Apply the threshold rule. This ensures you exploit observed cooperation (when others' contributions exceed your participation cost) and abandon cooperation when it becomes unprofitable.

- **All-defect equilibrium:** If all opponents defect every round, you observe 0 cooperators and perpetually defect, getting payoff 1 per round. This is stable and self-reinforcing.

- **Majority cooperation:** If opponents generally cooperate and maintain ≥ ⌈n/k⌉ contributors, you join in rounds 2 through r-1, capturing the mutual gains.
'''

description_INDIVIDUALISTIC_2 = '''
# Adaptive Defection with Conditional Cooperation

**Cooperation Threshold Rule:**

Cooperate in round t if and only if the observed cooperation rate from round t-1 satisfies:

```
observed_cooperation_rate ≥ n/k
```

Otherwise defect.

**First Round:**
Defect. This is the safe initialization—no history exists, and defection is the dominant single-round action.

**Subsequent Rounds (1 < t < r):**
Calculate the proportion of players who cooperated in round t-1:

```
coop_rate(t-1) = (number of cooperators in t-1) / n
```

If `coop_rate(t-1) ≥ n/k`, cooperate in round t.
If `coop_rate(t-1) < n/k`, defect in round t.

**Final Round (t = r):**
Always defect. With no future rounds remaining, there is no benefit to maintaining cooperation for future rounds. The final round is a one-shot game where defection strictly dominates.

**Rationale:**

The threshold n/k represents the minimum cooperation density at which the share of the public good (k/n per cooperator) makes contributing strategically viable. Below this rate, the public good is diluted enough that the private value of defection (1 unit) consistently exceeds the share you receive. Above it, the accumulating returns from a cooperating population make participation profitable relative to pure free-riding against a predominantly cooperative group.

This strategy is individualistic because it abandons cooperation the moment it becomes collectively insufficient to justify your cost, and robust because it does not depend on opponent strategy labels—only on observable aggregate behavior and mathematical thresholds.
'''

description_INDIVIDUALISTIC_3 = '''
# Adaptive Threshold Strategy

**Round 1 (Exploratory):** Cooperate unconditionally. This gathers baseline information about opponent cooperation without committing to a long-term path.

**Rounds 2 through r-1 (Adaptive Core):** 
- Observe m = the number of opponents who cooperated in the previous round
- Calculate the cooperation rate: ρ = m / (n-1)
- **Defect** if ρ < k/(n-1), otherwise **Cooperate**

The threshold k/(n-1) reflects the breakeven point: if fewer opponents cooperate than this fraction, the public good benefit is too diluted to offset the +1 payoff advantage of defection.

**Round r (Final Round):** Always Defect. No future rounds exist, so cooperation has no strategic value.

---

**Rationale for thresholds:**

The strategy recognizes that while defection always yields +1 more than cooperation in any single round, opportunistic cooperation becomes viable when enough others are already contributing. By cooperating when ρ is high, I capture a share of a large public good without needing to assume others will reciprocate my own cooperation.

The k/(n-1) threshold is derived from basic payoff logic: I want the public good contribution (k/n times the cooperators) to exceed 1. If the observed cooperation suggests this threshold will be met, cooperation becomes worthwhile.

**Edge cases:**
- If all opponents defect in round t, then m=0, and I defect in round t+1
- If all opponents cooperate, m=n-1, and ρ=1 > k/(n-1), so I cooperate
- In round 1, I have no history, so I cooperate as a cheap signal to estimate baseline tendencies

This approach is individualistic because it maximizes my own payoff without assuming reciprocal behavior, relying only on empirical observation of aggregate opponent cooperation.
'''

description_INDIVIDUALISTIC_4 = '''
# Individualistic Strategy: Conditional Defection Based on Payoff Dominance

**Core Decision Rule:**

Defect in every round.

**Rationale by payoff comparison:** For any observed cooperation count c in the previous round, compute the single-round payoff from each action assuming opponents maintain their cooperation level:
- Defect payoff: 1 + (k/n) × c
- Cooperate payoff: (k/n) × (c + 1) = (k/n) × c + (k/n)

Since k < n, we have (k/n) < 1, so (k/n) < 1. Therefore defection strictly dominates cooperation in payoff terms: the defection payoff exceeds the cooperation payoff by [1 - (k/n)] > 0 regardless of what others do.

**Edge cases:**

- **Round 1:** Defect (no history to condition on; defection is the safe choice and payoff-maximizing).
- **Final round (round r):** Defect (no future reputation concerns exist; the single-round payoff dominance holds).
- **All subsequent rounds:** Defect.

**Why this is individualistic:**

This strategy maximizes your own payoff in isolation without regard for social welfare, efficiency, or coordination. You are indifferent to how many others cooperate—their cooperation benefits you (via the shared pool), but it never incentivizes you to reciprocate. You free-ride on any cooperation that occurs while incurring no cost.

**Robustness:**

Pure defection succeeds against any opponent strategy—cooperative players, defectors, conditional cooperators, and random players alike. You guarantee yourself a payoff floor of 1 per round plus whatever spillover you receive from others' contributions, with no downside.
'''

description_COLLECTIVE_5 = '''
# Conditional Cooperation with Mutual Benefit Threshold

**Round 1 Decision:**
Cooperate unconditionally. This initiates the possibility of collective benefit without prior information about opponent strategies.

**Rounds 2 through r Decision:**
Cooperate if and only if the observed number of cooperators in the previous round meets or exceeds a threshold. Set this threshold at:

```
threshold = ⌈n / k⌉
```

This means: cooperate when observed_cooperators ≥ ⌈n / k⌉.

Defect otherwise.

**Rationale for Threshold:**
The threshold ⌈n / k⌉ represents the minimum number of cooperators needed for cooperation to be individually profitable. When at least this many cooperators exist, contributing yields k/n × threshold ≥ 1, matching or exceeding the private payoff of 1 from defection. Below this threshold, cooperation is individually irrational.

**Last Round (Round r):**
Apply the same threshold rule as rounds 2 to r−1. Do not defect preemptively in the final round; maintain reciprocal logic throughout. If others maintain the threshold, continue cooperation even at game's end.

**Adaptive Recovery:**
If cooperation drops below the threshold for one round, immediately defect. Resume cooperation as soon as observed cooperation reaches the threshold again. This creates a defect-revert cycle that punishes free-riding while remaining open to renewed cooperation.

**Handling Degenerate Cases:**
- If ⌈n / k⌉ > n (impossible given k > 1), treat threshold as n (require all cooperators).
- If cooperation never stabilizes above threshold, settle into defection, accepting a payoff of 1 per round.
'''

description_COLLECTIVE_6 = '''
# Reciprocal Threshold Cooperation Strategy

## Core Decision Rule

Cooperate in round t if and only if:
- t = 1 (first round), OR
- The observed cooperation rate in round t-1 satisfies: cooperation_rate ≥ threshold

Otherwise defect.

## Threshold Specification

Set threshold τ = 0.5 (cooperate if at least half of opponents cooperated last round).

*Rationale*: This balances generosity toward mixed populations against protection from widespread defection. At 50% cooperation, the public good contribution (k/n × 0.5n = 0.5k) typically exceeds what pure defection yields when facing a cooperating base.

## Round-by-Round Behavior

**Round 1**: 
Cooperate unconditionally.

**Rounds 2 to r-1**:
- Observe cooperation count c_obs from previous round
- Calculate cooperation_rate = c_obs / (n-1)
- If cooperation_rate ≥ 0.5: play C
- If cooperation_rate < 0.5: play D

**Round r (final round)**:
Defect unconditionally.

*Rationale for end-game defection*: No future reputation effects exist, so defection maximizes final-round payoff. This is standard in repeated games with known termination.

## Edge Cases

- **If n = 2**: Threshold still applies. With only one opponent, a single cooperator yields cooperation_rate = 1.0 (≥ 0.5), triggering your cooperation.
- **If r = 2**: Cooperate in round 1; defect in round 2 (final round).
- **Unanimous defection**: If all opponents defect in any round t < r, you observe rate 0 < 0.5 and defect in round t+1 onward (until final round defection anyway).

## Adaptation to Observed Patterns

- **Upward trend**: If cooperation increases across rounds, your strategy automatically escalates reciprocation.
- **Downward trend**: Strategy contracts cooperation to match declining reciprocation, preventing repeated exploitation.
- **Volatile opponents**: High variance in cooperation rates causes your strategy to toggle between C and D, maintaining responsiveness without commitment to doomed cooperation.
'''

description_COLLECTIVE_7 = '''
# Adaptive Threshold Cooperation Strategy

**Core Logic:**
Sustain cooperation when others demonstrate willingness to cooperate, defect when cooperation breaks down. Use the multiplication factor k and group size n to calibrate responsiveness.

---

## Decision Rules

**Threshold Calculation:**
- Cooperation threshold θ = k/n
- This represents the point where the collective benefit from the public good becomes significant relative to private incentives.

**Round 1 (Initialization):**
- Cooperate
- This optimistic opening tests whether others will reciprocate and attempts to establish a cooperative equilibrium.

**Rounds 2 through r-1 (Adaptive Reciprocal Phase):**
- Observe the number of cooperators in the previous round: m
- Calculate cooperation rate: p = m/n
- **If p ≥ θ:** Cooperate
  - Others are cooperating sufficiently; the public good is producing enough value to justify continued contribution
- **If p < θ:** Defect
  - Cooperation has fallen below the threshold; free-riding dominates and attempting to maintain the public good is futile

**Round r (Final Round):**
- Defect unconditionally
- No future rounds exist to reward cooperation, so extract immediate private value

---

## Collective Alignment

This strategy prioritizes group welfare by:
- Attempting to sustain cooperation when it reaches critical mass (p ≥ θ)
- Withdrawing support when the cooperative coalition becomes too weak to generate value
- Avoiding wasted contributions that benefited only free-riders

The threshold θ = k/n creates an adaptive, self-correcting system: as fewer others cooperate, the value of any individual contribution drops, triggering defection and reducing waste; as cooperation recovers, contributors re-enter.

---

## Robustness

- **Against consistent defectors:** Quickly identifies non-cooperation and defects
- **Against oscillating groups:** Tracks changes round-to-round and adjusts accordingly
- **Against mixed opponents:** Responds empirically to the actual cooperation rate rather than assuming opponent strategies
- **Parameter-responsive:** The threshold automatically scales with game structure (scaling with k and n)
'''

description_COLLECTIVE_8 = '''
**THRESHOLD-BASED CONDITIONAL COOPERATION WITH COMMITMENT**

**Decision Rule by Round:**

*Round 1 (Initialization):*
Cooperate unconditionally. This signals openness to mutual cooperation and sets a cooperative anchor.

*Rounds 2 through r-1 (Adaptive Phase):*
- Record the cooperation rate from the previous round: `coop_rate(t-1) = [count of cooperators in round t-1] / n`
- Cooperate if `coop_rate(t-1) ≥ threshold`
- Defect if `coop_rate(t-1) < threshold`
- **Threshold value:** Set to `k/n` (the marginal return multiplier). This threshold represents the breakeven point where cooperation becomes collectively beneficial. Equivalently, use the simpler heuristic: **cooperate if at least ⌈k⌉ out of n players cooperated last round**.

*Round r (Final Round - Commitment to Collective Outcome):*
Apply the same threshold rule as rounds 2 through r-1. Do NOT defect in the final round regardless of history. This breaks the endgame temptation to free-ride and maintains the integrity of the mutual cooperation equilibrium.

**Recovery Rule (Optional Enhancement):**
If cooperation collapses (coop_rate < threshold), use a two-round recovery window: require two consecutive rounds at or above threshold before resuming full cooperation. This prevents thrashing between cooperation and defection due to noise.

**Edge Cases:**
- If n=2 and k=1.5: threshold is 0.75, so cooperate only if the other player cooperated last round (1 cooperator out of 2).
- If r=2: Round 1 is initialization; Round 2 applies the threshold based on Round 1 behavior.
- If all opponents defect every round: You defect from Round 2 onward, limiting losses to the initial cooperative signal.
'''

description_COLLECTIVE_9 = '''
# Threshold-Based Conditional Cooperation with Adaptive Forgiveness

## Core Decision Rule

**Cooperate if and only if the observed cooperation rate in the previous round meets or exceeds an adaptive threshold; otherwise, defect with probabilistic forgiveness.**

## Round-by-Round Specification

**Round 1:**
Cooperate unconditionally. This establishes your willingness to participate in collective benefit-generation.

**Rounds 2 to r-1 (Middle Rounds):**
Let m = number of opponents who cooperated in round t-1.
Let c_rate = m / (n-1).

```
initial_threshold = k / n

if c_rate ≥ threshold:
  Play C
  // Tighten threshold slightly: threshold = c_rate - ε  
  // where ε is small (e.g., 0.05), to track actual cooperation level
else:
  if c_rate ≥ k/n:
    // Cooperation is sustainable but below current expectations
    With probability forgive_prob = 0.3, play C
    Otherwise play D
  else:
    // Cooperation is below the threshold where public good multiplies (k/n)
    With probability forgive_prob = 0.15, play C
    Otherwise play D

// Adjust threshold downward after consecutive defection rounds
if last_two_rounds_both_defection:
  threshold = max(0, threshold - 0.1)
  forgive_prob = min(0.5, forgive_prob + 0.1)
```

**Round r (Final Round):**
```
if c_rate ≥ threshold:
  Play C  // Maintain collective cooperation to the end
else:
  if c_rate ≥ 0.5:
    Play C  // Last-minute attempt to sustain
  else:
    Play D  // Defect if cooperation has collapsed
```

## Edge Cases and Rationale

**If cooperation drops sharply (>30% in one round):** Lower threshold immediately by 0.15 and increase forgiveness probability. This prevents the strategy from rigidly expecting cooperation that opponents have abandoned.

**If all opponents defected in round t-1:** Still cooperate with probability 0.1 in round t to create an off-ramp from mutual defection. Don't enter a trap of permanent mutual defection.

**Threshold floor:** Never drop threshold below k/n, the break-even point where the public good is still worth participating in for the group.

**Early signs of free-riding:** If cooperation is high but you notice a pattern where some players consistently defect, your historical cooperation rate still rises, preventing overreaction to individual defectors.
'''

description_COLLECTIVE_10 = '''
# Adaptive Conditional Cooperation with Endgame Adjustment

## Decision Rule (Cooperation Threshold)

Maintain a **dynamic cooperation threshold** based on game structure and time remaining:

```
IF round == 1:
  COOPERATE  // initialization: signal willingness to cooperate

ELSE:
  observed_rate = (cooperators_last_round) / (n - 1)
  threshold = COMPUTE_THRESHOLD()
  
  IF observed_rate ≥ threshold:
    COOPERATE
  ELSE:
    DEFECT
```

## Threshold Computation

```
IF rounds_remaining ≤ 1:  // final round
  threshold = 0.75  // high bar; expect endgame defection
  
ELSE IF rounds_remaining ≤ 3:  // approaching endgame
  threshold = (2*k) / n  // stricter than normal
  
ELSE:  // middle game
  threshold = k / n  // sustain if public good payoff exceeds private retention
  
  // Adjust upward if cooperation is declining
  IF observed_rate is trending downward:
    threshold = (k / n) + 0.15
```

## Edge Cases

**Round 1**: Cooperate unconditionally. No history exists; cooperation is a probe signaling cooperative intent.

**Rounds 2 to (r-1)**: Apply threshold. If cooperation rate drops below threshold for two consecutive rounds, increase threshold by +0.1 to signal exit from cooperation (avoid prolonged exploitation).

**Round r (final)**: Defect if observed_rate < 0.75. In the final round, reciprocal punishment has no future value, so only high observed cooperation justifies cooperation.

## Collective Alignment

This strategy embeds collective welfare logic: cooperate when others reciprocate at levels that make the public good worthwhile relative to private retention. The threshold k/n reflects the mathematical point where aggregate contribution begins to exceed individual defection payoff. By conditioning on observed cooperation and tracking trends, the strategy avoids unilateral cooperation loss while rewarding groups moving toward mutual gain. The endgame downshift prevents being exploited when future reputation has no value.
'''

description_COLLECTIVE_11 = '''
# Reciprocal Cooperation with Threshold Trigger

**Round 1 (Opening):**
Cooperate. This signals willingness to contribute and tests the collective's disposition toward cooperation.

**Rounds 2 to r-1 (Body of game):**
Observe C_{t-1}, the number of cooperators in the previous round.

Calculate the observed cooperation rate: p_{t-1} = C_{t-1} / n

Decision rule:
- If p_{t-1} ≥ 0.5, then Cooperate
- If p_{t-1} < 0.5, then Defect

**Round r (Final round):**
Apply the same decision rule as rounds 2 to r-1. Do not shift to pure defection. A collectively-minded approach maintains reciprocal logic even when repeated interaction ends.

---

## Rationale for Decision Points

**Round 1:** Starting with cooperation rather than defection is a collective signal that you are not an obligate free-rider. It anchors expectations toward mutual benefit.

**Threshold at 0.5:** This is a reciprocal reciprocity rule—you cooperate when the majority of the population did so in the previous round. A threshold of 50% balances two objectives:
- Avoid mass defection: if less than half of players cooperate, the public good is weak and your contribution is wasted
- Reward cooperation: if at least half cooperate, the collective benefits enough that your contribution multiplies and is worthwhile

**Endgame consistency:** Defecting in the final round is individually dominant but collectively destructive. By applying the same threshold rule throughout, you avoid the "last-round defection" that breaks down cooperation. This is collectively rational even if individually suboptimal in isolation.

---

## Edge Cases

- **All-defect scenario (C_{t-1} = 0):** Trigger defection; do not subsidize a free-riding population.
- **All-cooperate scenario (C_{t-1} = n):** Maintain cooperation to sustain the equilibrium.
- **Exactly 50% cooperation:** Cooperate (threshold uses ≥). This breaks ties in favor of cooperation.
- **First round has no prior history:** Preset to cooperate, making no conditional demands.
'''

description_COLLECTIVE_12 = '''
ADAPTIVE RECIPROCAL COOPERATION WITH THRESHOLD RESPONSE

**Core Decision Rule:**

Cooperate in round t if and only if the observed cooperation rate among opponents in round t-1 meets or exceeds a dynamic threshold. Defect otherwise.

**Specific Implementation:**

Round 1: Cooperate unconditionally. This establishes willingness to contribute and tests opponent dispositions.

Rounds 2 to r-1: 
- Calculate observed cooperation rate: c_prev = (number of opponents who cooperated in round t-1) / (n-1)
- Cooperation threshold: θ = k/n
- Decision: If c_prev ≥ θ, play C. If c_prev < θ, play D.

Round r (final round):
- If cooperation rate in round r-1 exceeded the threshold, cooperate (C)
- If cooperation rate in round r-1 was at or below threshold, defect (D)
- Rationale: preserve collective momentum if achieved; don't subsidize defectors in the endgame

**Threshold Justification:**

The threshold θ = k/n represents the equilibrium multiplier value where collective marginal benefit equals individual private incentive. Cooperation is collectively rational when others cooperate above this rate. Falling below this rate signals either systematic defection or insufficient trust, warranting strategic withdrawal.

**Edge Cases:**

- Unanimous defection (c_prev = 0): Play D until cooperation rate rises above threshold
- Perfect cooperation observed (c_prev = 1): Continue playing C as long as threshold is met
- Odd observations (very low n): Threshold applies to fractional cooperation rates; apply ceiling rule for n ≤ 3

**Adaptive Robustness:**

The strategy naturally divides opponents into cooperators (those sustaining c_prev ≥ θ) and defectors/free-riders (c_prev < θ). This classification emerges from observed behavior rather than fixed assumptions, allowing response to mixed populations. The history-dependent structure means the strategy self-corrects: if defection spreads, cooperation terminates, reducing mutual losses.
'''

description_COLLECTIVE_13 = '''
# Reciprocal Threshold Cooperation

**Round 1:** Always cooperate. Signal readiness to contribute to collective action and test the environment.

**Rounds 2 through r:**
- Observe the count of cooperators in the immediately preceding round: C_{t-1}
- **If C_{t-1} > k:** Cooperate in round t
- **If C_{t-1} ≤ k:** Defect in round t

**Logic for threshold k:**
When more than k players contribute, the public good pool exceeds k (the multiplication factor). This generates sufficient return—at minimum (k/n) × (k+1) for each cooperator—to justify the endowment cost. Reciprocating when C_{t-1} > k sustains a cooperative equilibrium that benefits all participants. When C_{t-1} ≤ k, the public good is too depleted to warrant contribution; defect to preserve resources.

**Endgame:** Apply the same rule in round r. Do not defect automatically on the final round. Defecting only if cooperation has already collapsed maintains consistency and prevents premature unraveling.

**Handling edge cases:**
- If any round yields a tie (C_{t-1} = k exactly): Defect. The threshold is strictly greater than k; equality implies insufficient collective contribution momentum.
- If n is small and k is close to n: The strategy remains robust because the threshold becomes tight—it requires near-universal cooperation to sustain play, which is appropriate when the individual incentive to free-ride is strongest.

**Collective alignment:** This strategy treats all players symmetrically, responds proportionally to observed cooperation rather than attempting to identify or punish individuals, and maintains cooperation whenever the aggregate contribution level makes it mutually beneficial. It avoids both naive universal cooperation and reactive punishment cycles.
'''

description_COLLECTIVE_14 = '''
# Collective Threshold Cooperation Strategy

## Decision Rule

For each round t, maintain an empirical cooperation rate estimate from prior rounds. Cooperate if and only if:

```
IF t == 1:
  COOPERATE
ELSE:
  empirical_coop_rate = (sum of observed cooperators in rounds 1..t-1) / ((t-1) × n)
  threshold = (1/k) - ε
  IF empirical_coop_rate ≥ threshold:
    COOPERATE
  ELSE:
    DEFECT
```

Where ε is a small adjustment factor (ε ≈ 0.02-0.05) that tilts decisions toward cooperation for collective benefit.

## Rationale for Threshold

The threshold 1/k represents the empirical cooperation rate at which your expected individual payoff from cooperating equals your payoff from defecting:
- If others cooperate at rate p, your payoff for C is: (k/n) × p × n = k × p
- Your payoff for D is: 1 + (k/n) × p × n = 1 + k × p

Cooperating is individually rational when k × p ≥ 1 + k × p is impossible, but becomes collectively rational when group welfare (which scales with total cooperation) is considered. The slight reduction (−ε) biases toward cooperation, recognizing that cooperation itself contributes to the public good you benefit from.

## Edge Cases

**First round (t=1):** Always cooperate. This establishes that you are willing to contribute to the collective good absent information about others, signaling good-faith participation.

**Last round (t=r):** Apply the same threshold rule. Do not defect solely because no future rounds remain—this preserves collective commitment and avoids the end-game defection collapse.

**Cooperation rate below threshold:** Defect rather than chase losses. If the observed cooperation rate falls below 1/k, the public good is insufficiently funded for cooperation to pay back even at the individual level; defecting minimizes personal loss.

**Cooperation rate exactly at threshold:** Cooperate (rule uses ≥, not >). Cooperation at the margin stabilizes collective outcomes.

## Robustness Properties

- **Against universal defectors:** You defect by round 2, limiting losses to one round.
- **Against widespread cooperators:** You match and sustain high payoffs for everyone.
- **Against mixed strategies:** You track the true cooperation level and adjust continuously, neither exploiting nor being exploited persistently.
- **Parameter-invariant:** The strategy scales to any valid k and n automatically.
'''

description_COLLECTIVE_15 = '''
# Adaptive Threshold Cooperation Strategy

**Core Principle:** Cooperate if aggregate cooperation from others suggests mutual benefit is achievable; defect if cooperation collapses into exploitation.

---

## Decision Rule by Round

**Round 1:**
Cooperate unconditionally. This establishes the possibility of mutual benefit and signals cooperative intent.

**Rounds 2 through r-1:**
Observe m = number of opponents who cooperated in the previous round.

Cooperate if and only if: m ≥ ceil(n/k - 1)

Otherwise defect.

**Final Round r:**
Apply the same decision rule as rounds 2 through r-1. Do not defect reflexively in the final round; maintain the collective principle through completion.

---

## Rationale for the Threshold

The threshold ceil(n/k - 1) identifies the minimum number of cooperators needed (excluding yourself) for your contribution to yield at least 1 unit of payoff:
- If you contribute and m others contribute: payoff = 0 + (k/n) × (m + 1)
- Breaking even requires: (k/n) × (m + 1) ≥ 1, thus m ≥ n/k - 1

This threshold ensures you only contribute when the collective is generating sufficient public good to justify the endowment sacrifice.

---

## Handling Edge Cases

- **If cooperation collapses below threshold:** Switch to defection. This prevents continued exploitation while signaling that the cooperative equilibrium has failed.

- **If cooperation hovers at or above threshold consistently:** Maintain cooperation throughout. This sustains mutual benefit.

- **Mixed cooperation rates across rounds:** Use only the immediately previous round's count; this keeps the strategy responsive to current conditions rather than averaging history.

---

## Collective Alignment

This strategy embodies collective thinking by:
1. **Opening cooperatively** to enable mutual gain
2. **Conditioning on others' aggregate behavior**, not punishing individual players
3. **Maintaining discipline** — defecting when collective benefit disappears, rather than being exploited
4. **Applying identical logic in the final round**, rejecting the notion that the game's end justifies defection

The strategy converges toward an equilibrium where cooperation is sustained as long as the group collectively produces sufficient public goods.
'''

description_COLLECTIVE_16 = '''
# Adaptive Threshold Cooperation Strategy

## Phase 1: Establishment (Round 1)
Cooperate unconditionally. Signal willingness to participate in the public good and test the cooperative environment.

## Phase 2: Conditional Contribution (Rounds 2 through r-1)

After each round, observe the number of cooperators M in the previous round.

Calculate cooperation density: ρ = M / (n - 1)

Define cooperation threshold: θ = k / n

**Decision rule:**
- If ρ ≥ θ: Cooperate
- If ρ < θ: Defect

**Intuition:** Cooperate only when the aggregate cooperation is sufficient to generate positive returns from the public good beyond the private endowment.

## Phase 3: Endgame (Round r)

Check the average cooperation density across all rounds 1 through r-1: ρ_avg = (total cooperators across rounds 1 to r-1) / ((r-1) × (n-1))

**Decision rule:**
- If ρ_avg ≥ θ: Cooperate (reciprocate sustained cooperation)
- If ρ_avg < θ: Defect (no reputation risk in final round; align with collective defection)

## Edge Cases

**When r = 2:** Treat round 2 as endgame. After round 1, decide based on observed cooperation: cooperate in round 2 if round 1 showed ρ ≥ θ, else defect.

**When n = 2 and k ≤ 1:** Both players receive k/2 per contribution. Set θ = 1/2 to trigger mutual cooperation.

**When k approaches n:** Cooperation becomes increasingly profitable, lowering threshold naturally. Strategy remains valid.

This strategy favors collective welfare by sustaining contributions when the group maintains sufficient participation, while withdrawing support when the group falls below threshold, creating mutual reinforcement of either cooperation or rational defection.
'''

description_COLLECTIVE_17 = '''
# Adaptive Threshold-Based Cooperation Strategy

## Core Decision Rule

**Main principle:** Cooperate when enough others are cooperating to sustain a cooperation equilibrium; adjust dynamically based on observed cooperation rates.

**Per-round decision:**

```
if round == 1:
    COOPERATE
else if round == r (last round):
    DEFECT
else:
    cooperation_rate = (cooperators_observed_last_round) / (n - 1)
    if cooperation_rate >= threshold:
        COOPERATE with probability p_sustain
    else if cooperation_rate < threshold:
        COOPERATE with probability p_recover
```

## Parameters

- **Threshold θ = max(k/n, 0.4):** The minimum cooperation rate among others that justifies continued cooperation. Tie to the multiplication factor since higher k makes cooperation more efficient.
- **p_sustain = 0.95:** High cooperation probability when others are cooperating. Nearly certain cooperation with slight stochasticity for robustness.
- **p_recover = 0.2:** Low cooperation probability when others are primarily defecting. Maintains exploration for recovery while protecting against exploitation.

## Edge Cases

**First round:** Always cooperate. This signals willingness to cooperate and provides a baseline observation.

**Last round:** Always defect. The endgame has no shadow of the future; continuing cooperation cannot generate reciprocal responses in subsequent rounds.

**Rounds 2 to r-1 (middle game):** Apply the adaptive threshold rule above.

**Initialization (before any history):** Set p = 1.0 for round 1.

**If cooperation rate equals threshold exactly:** Cooperate (tie-breaking toward cooperation).

## Collective Alignment

This strategy embodies collective rationality by:

1. **Pursuing mutual cooperation:** Starts optimistically with cooperation, recognizing that universal cooperation is collectively superior to universal defection (π = 2 vs π = 1 in the k=2 example).

2. **Matching group behavior:** Bases decisions on observed cooperation trends, creating implicit alignment with similarly-motivated opponents. Higher cooperation rates trigger higher cooperation, reinforcing a cooperative equilibrium if others use similar logic.

3. **Punishment and recovery:** Reduces cooperation when others defect (punishment), but does not permanently abandon cooperation (p_recover > 0 allows recovery). This balances accountability with forgiveness.

4. **Threshold-responsive:** The threshold prevents over-cooperation in low-cooperation environments and ensures cooperation only when sustainable. Adaptation across different n and k values maintains strategy robustness.
'''

description_COLLECTIVE_18 = '''
# Adaptive Cooperation Strategy

**Core Decision Rule:**

Cooperate if and only if:
1. It is round 1, OR
2. The observed cooperation rate in the previous round is at least k/n (the minimum threshold where expected cooperation payoff exceeds defection payoff)

Formally, for round t (where t ≥ 2):

```
cooperate_t = (C_{t-1} / n) ≥ (k/n)
```

where C_{t-1} is the number of cooperators observed in round t-1.

**End-Round Adjustment:**

For the final round r only:
- If cooperation rate has been strictly increasing over the last 3 rounds (or all rounds if fewer than 3 remain), cooperate.
- Otherwise, defect.

This prevents total collapse in the endgame when others may defect due to no future reputation costs.

**Threshold Justification:**

Set the threshold exactly at k/n because:
- If ≥ k/n players cooperated in the previous round, you gain at least (k/n)² ≥ k/n from the public good
- This equals or exceeds the marginal defection payoff, making cooperation rational even from a narrow self-interest perspective
- It creates a focal point: if all players adopt this rule, the strategy is collectively stable at full cooperation

**History Interpretation:**

- Track only the aggregate number of cooperators per round, not individual identities (per game rules)
- Use this to make forward-looking decisions that are transparent and non-manipulative

**Collective Alignment:**

This strategy succeeds when deployed widely because it sustains high cooperation through reciprocal thresholds, while protecting against unilateral exploitation by those using unconditional strategies.
'''

description_COLLECTIVE_19 = '''
## THRESHOLD-BASED RECIPROCAL COOPERATION

**Setup:**
Store `cooperation_last_round` (number of opponents who played C in the previous round). Initialize as `n-1` (assume cooperative context entering round 1).

**Decision Rule by Round:**

**Round 1 (Initialization):**
Play C unconditionally. This establishes the cooperative norm and tests opponent responsiveness.

**Rounds 2 through r-1 (Reciprocal Phase):**
Calculate: `cooperation_rate = cooperation_last_round / (n-1)`

- If `cooperation_rate ≥ 0.5`: Play C
- If `cooperation_rate < 0.5`: Play D

This reciprocates whenever a strict majority of opponents cooperated. Defect when cooperation falls below 50% to signal rejection of free-riding.

**Round r (Endgame):**
Calculate: `cooperation_rate = cooperation_last_round / (n-1)`

- If `cooperation_rate ≥ 0.5`: Play C
- If `cooperation_rate < 0.5`: Play D

Use the same threshold in the final round rather than optimistic or pessimistic defection. This maintains consistency—if opponents have sustained cooperation, reciprocate even when no future punishment is possible, reinforcing the collective norm.

**Edge Cases:**

- **If n = 2:** The cooperation rate is binary (opponent played C or D). Cooperate iff opponent cooperated in the previous round; cooperate in round 1.
- **If r = 2:** Apply round 1 rule for round 1 (unconditional C), apply endgame rule for round 2.
- **Tie-breaking:** The 50% threshold is strict. At exactly 50% (even split), cooperate—this assumes ambiguity favors coordination.

**Rationale:**
This strategy achieves mutual cooperation equilibrium (payoff k per round) when opponents are reciprocal. It defects only when defection becomes widespread (below majority support), creating a coordination point. It avoids last-round collapse by committing to reciprocity throughout, which collectively sustains higher payoffs than the all-defection baseline.
'''

description_COLLECTIVE_20 = '''
# RECIPROCAL CONDITIONAL COOPERATION STRATEGY

**Core Principle**: Cooperate when observed opponent cooperation meets a threshold that justifies contribution, otherwise defect. Track aggregate cooperation rate across all previous rounds as the primary history signal.

---

## DECISION RULES

**Maintain this state variable:**
- `observed_coop_rate` = (total cooperators across all previous rounds) / (n-1) × (rounds elapsed)

**Threshold calculation:**
- `break_even_cooperators` = ⌈n / k⌉
  - This is the minimum number of cooperators needed for my contribution to yield more value than keeping my endowment private

**Cooperation condition:**
- `effective_opponents_cooperating` = observed_coop_rate × (n - 1)

---

## DECISION LOGIC BY PHASE

**Round 1 (Initial round):**
- Action: **COOPERATE**
- Rationale: Signal willingness and establish baseline cooperation

**Rounds 2 through r-1 (Middle rounds):**
- If `effective_opponents_cooperating ≥ break_even_cooperators - 0.5`:
  - Action: **COOPERATE**
  - (Others are cooperating at sufficient levels; reciprocate)
- Else:
  - Action: **DEFECT**
  - (Insufficient cooperation observed; protect endowment and limit free-riding exposure)

**Round r (Final round):**
- Same threshold as middle rounds
- If `effective_opponents_cooperating ≥ break_even_cooperators - 0.5`:
  - Action: **COOPERATE**
  - (Reinforce successful mutual cooperation pattern)
- Else:
  - Action: **DEFECT**
  - (No reputation consequences; protect payoff)

---

## EDGE CASES & ROBUSTNESS

**Declining cooperation over time**: The rolling average naturally reflects deteriorating cooperation. As defectors accumulate rounds, the threshold becomes harder to meet, triggering defection automatically.

**Mixed opponent strategies**: Heterogeneous opponents are absorbed into the aggregate rate. If some defect always and others cooperate conditionally, the observed rate will be intermediate; the strategy responds proportionally.

**High k (near n)**: When k approaches n, `break_even_cooperators` approaches 1. Even a small cooperative minority makes cooperation profitable. The strategy cooperates more generously.

**Low k (near 1)**: When k is small, many cooperators are needed to break even. The strategy becomes more cautious, defecting when cooperation is sparse.

**Small n**: With few players, variance in cooperation is higher per round. The threshold still holds by construction.

---

## COLLECTIVE ALIGNMENT

This strategy achieves mutual cooperation when opponents use similar logic or are sufficiently cooperative. It avoids prolonged mutual defection traps by offering an initial cooperative overture and rewarding reciprocation. It punishes free-riding by switching to defection when cooperation falls below sustainable levels, creating pressure for collective benefit-maximization rather than individual exploitation.
'''

description_COLLECTIVE_21 = '''
## STRATEGY: Adaptive Reciprocity with Threshold Monitoring

**Round 1:**
Cooperate (C). Establish a signal of willingness to participate in collective benefit.

**Rounds 2 through r-1 (middle rounds):**

Calculate the cooperation rate from the previous round:
```
observed_rate = (number of cooperators in round t-1) / n
```

Set a cooperation threshold:
```
base_threshold = k / (2n)
```

Decision rule:
- If `observed_rate ≥ base_threshold`, play Cooperate (C)
- If `observed_rate < base_threshold`, play Defect (D)

The threshold reflects the payoff-relevant point where shared benefits begin to outweigh private retention. When fewer than ~50% of players (scaled by k) cooperate, the public good is too depleted to justify contributing.

**Round r (final round):**

Adjust strategy based on final-round dynamics. Calculate:
```
final_threshold = base_threshold + 0.15
```

This slightly higher threshold prevents last-round free-riding exploitation. The added buffer (0.15) guards against defectors who wait until the final round.

- If `observed_rate ≥ final_threshold`, play Cooperate (C)
- Otherwise, play Defect (D)

**Edge cases and robustness:**

- If all opponents defect consistently (observed_rate near 0), defect in all future rounds. A depleted commons provides no return.
- If cooperation stabilizes above threshold, maintain reciprocal cooperation indefinitely—the system self-sustains.
- If cooperation oscillates around the threshold, defect during low periods to reduce free-rider payoffs, then cooperate again when cooperation recovers.

**Rationale:** This strategy aligns individual incentives with collective outcomes by only contributing when others do. It avoids unilateral cooperation (which sucker-outs to full defectors) while rewarding and reinforcing pro-social behavior when it emerges. The threshold prevents permanent mutual defection when even modest cooperation could benefit all players.
'''

description_COLLECTIVE_22 = '''
**Threshold Reciprocity Strategy**

**Decision Rule by Round:**

*Round 1:* Cooperate unconditionally. This signals willingness to support collective benefit and establishes a cooperative baseline.

*Rounds 2 through r:* Apply threshold reciprocity.
- Observe the cooperation count from the previous round: c_{t-1}
- Calculate cooperation rate among opponents: rate = c_{t-1} / (n-1)
- Set threshold: τ = k/n + 0.15
- If rate ≥ τ: Cooperate
- If rate < τ: Defect

**Rationale for Threshold:**
The threshold k/n represents the cooperation level at which the average player breaks even between contributing and free-riding. Adding a margin (0.15) requires cooperation to exceed this baseline, tilting toward group welfare over individual maximization. This threshold is collective: it says "I support cooperation when others demonstrate sufficient commitment to the common good."

**Edge Cases:**

- *Final round (t = r):* Apply the same threshold rule. Cooperate if the penultimate round's cooperation rate meets the threshold. This avoids defection collapse in the endgame while respecting the observed commitment level.

- *All-defect trap:* If rate falls below τ in any round, defect to minimize losses. Once defection occurs, only re-engage if rate recovers above τ in the next round.

- *Unanimous cooperation:* If rate = 1.0 in any round, continue cooperating in the next round.

- *Low n or high k:* The strategy scales automatically. Higher k makes cooperation more valuable to the group, so the threshold becomes easier to meet; lower k makes it stricter.

**Interpretation:**
This strategy treats cooperation as conditional on reciprocal commitment from the collective. It is not exploitable in the traditional sense because defection is an exit, not a punishment—if opponents return to sufficient cooperation, you return to cooperation. The strategy balances individual protection (defect when cooperation is too low) with collective orientation (cooperate when others signal genuine commitment).
'''

description_COLLECTIVE_23 = '''
# Adaptive Threshold Reciprocity Strategy

## Core Decision Rule

Cooperate in round t if and only if the observed cooperation rate in round t-1 meets or exceeds a dynamically-adjusted threshold. Adjust the threshold based on elapsed time and information about opponent responsiveness.

**Threshold formula:**
- θ(t) = k/n + φ(t)
- where φ(t) is a phase-dependent adjustment:
  - φ(early) = +0.15 (rounds 1-3): raise threshold slightly to test genuine cooperation
  - φ(mid) = 0 (rounds 4 to r-2): neutral threshold
  - φ(late) = -0.10 (rounds r-1, r): lower threshold to preserve mutual gains near end

**Cooperation rate observed in round t-1:**
- ρ(t-1) = (number of cooperators in round t-1) / (n-1)

## Decision Rules by Round

**Round 1:**
- Cooperate unconditionally. This serves as a costly signal of conditional cooperativeness and gathers initial information.

**Rounds 2 through r-1:**
- If ρ(t-1) ≥ θ(t), play Cooperate with probability 1
- If ρ(t-1) < θ(t) - ε, play Defect with probability 1
  - (where ε = 0.1, a small buffer to avoid oscillation)
- If θ(t) - ε ≤ ρ(t-1) < θ(t), mix probabilistically:
  - P(Cooperate) = [ρ(t-1) - (θ(t) - ε)] / ε
  - This creates a smooth transition rather than a sharp cliff

**Round r (final round):**
- If ρ(r-1) ≥ k/n, play Cooperate. The multiplier criterion ensures mutual cooperation is still welfare-improving even in the final round.
- Otherwise, play Defect.

## Rationale for Thresholds

- **Baseline threshold k/n**: Cooperation remains individually beneficial if at least a fraction k/n of others cooperate (since your marginal contribution returns (k/n) × 1 = k/n to you, matching your opportunity cost of 1 if k/n agents cooperate on average).
- **Early-round boost**: Raise threshold slightly to avoid being exploited by defectors while incentivizing others to reveal their type through cooperation.
- **Late-round reduction**: Lower threshold to preserve welfare gains during final rounds when future punishment has less weight.

## Handling Uncertainty

If the game parameters (n, k, r) suggest a low multiplier or high player count (making individual impact negligible), shift the early-round threshold upward by an additional +0.1 to screen for genuine reciprocators rather than assume cooperation.

## Special Case: Repeated Defection

If ρ remains below 0.1 for two consecutive rounds, defect with probability 1 for all remaining rounds. This avoids the "sucker's payoff" trap of continuous unreciprocated cooperation.
'''

description_COLLECTIVE_24 = '''
# Adaptive Threshold Cooperation

## Decision Rules

**Round 1 (Initialization):**
Cooperate. This establishes goodwill and tests whether cooperation is mutually sustainable.

**Rounds 2 through r-1 (Conditional Phase):**
Let c_prev = number of cooperators observed in the immediately previous round.
- If c_prev > n/k: Cooperate
- If c_prev ≤ n/k: Defect

The threshold n/k reflects the cooperation level at which continued cooperation becomes individually rational. When more than n/k players cooperated last round, my payoff from cooperating exceeds my payoff from defecting, so I reciprocate. Below this threshold, the public good is underfunded and defection minimizes losses.

**Round r (Final Round):**
Defect. In the last round, there is no future reputation to build or maintain, making defection strictly dominant. This is a standard endgame effect.

## Edge Cases

**If r = 2:** Execute Round 1 as specified, then proceed directly to Final Round (defect).

**Extreme cooperation (all n players cooperate in previous round):** Follow the rule—cooperate, since c_prev = n > n/k.

**Extreme defection (zero cooperators in previous round):** Defect, since c_prev = 0 ≤ n/k for all valid k.

**Ties at the threshold:** If c_prev = n/k exactly (rare with integer counts), treat as defection. This conservative stance assumes marginal cooperation is not robust enough to sustain.

## Collective Rationale

This strategy aligns individual incentives with group welfare by making cooperation contingent on observed reciprocation. It rewards groups that maintain sufficient cooperation while withdrawing support from groups that slip below the sustainability threshold. By defecting only when cooperation is collectively insufficient or in the final round, it minimizes free-riding on others' contributions and avoids locking into mutual exploitation equilibria. The threshold mechanism is decentralized—each player independently applies the same decision rule, creating spontaneous coordination toward mutually beneficial outcomes.
'''

description_COLLECTIVE_25 = '''
# Threshold-Based Conditional Cooperation

**Initialize Round 1:** Cooperate. This signals willingness to contribute and establishes the possibility of mutual benefit.

**Rounds 2 through r-1 (Middle game):**
- Let c_{t-1} = number of cooperators observed in the previous round
- Define threshold T = max(2, ⌈n/2⌉)
- **If c_{t-1} ≥ T: Cooperate**
- **If c_{t-1} < T: Defect**

**Round r (Final round):**
- Apply the same rule as middle rounds: cooperate if c_{r-1} ≥ T, otherwise defect
- Rationale: Maintaining the cooperative equilibrium through the final round maximizes collective payoff when others follow similar logic

---

**Rationale for threshold:**

The majority threshold reflects a "collective trust" heuristic. When at least half the group cooperates, the shared incentive aligns: continued cooperation benefits all parties more than mutual defection. This threshold:
- Resists small groups of free-riders (requires ≥50% genuine contributors)
- Avoids hair-trigger collapse (one defector doesn't end cooperation)
- Scales with group size naturally

**Decision tree:**

```
Round 1: COOPERATE

For t ∈ {2, ..., r}:
  c_prev ← observed cooperators in round t-1
  T ← max(2, ceil(n/2))
  
  if c_prev ≥ T:
    action ← COOPERATE
  else:
    action ← DEFECT
```

**Edge cases:**

- If n is odd and all players use this strategy, defection never occurs (each round maintains ≥⌈n/2⌉ cooperators)
- If opponents play constant defection, this strategy adapts to defection by round 2
- If opponents use similar conditional strategies, mutual cooperation is self-sustaining
'''

description_COLLECTIVE_26 = '''
# Adaptive Reciprocal Cooperation Strategy

**Core Decision Rule:**

Cooperate if and only if the observed cooperation rate among other players in the previous round meets or exceeds a responsive threshold. Otherwise defect.

**Formal Rule:**

```
Let opp_coop_rate(t-1) = (number of cooperators among other n-1 players in round t-1) / (n-1)

For round t:
  If t = 1:
    Action ← COOPERATE
  Else if t < r:
    If opp_coop_rate(t-1) ≥ 0.5:
      Action ← COOPERATE
    Else:
      Action ← DEFECT
  Else if t = r (final round):
    If opp_coop_rate(t-1) ≥ 0.75:
      Action ← COOPERATE
    Else:
      Action ← DEFECT
```

**Edge Cases and Rationale:**

- **Round 1**: Always cooperate. This signals willingness to participate in collective good and avoids pessimistic initialization. With no history, assume reciprocal intent.

- **Middle rounds (2 to r-1)**: Use a 50% threshold. If a majority of opponents cooperated last round, the public good is generating sufficient value to justify your contribution. Below 50% cooperation, others are free-riding enough that your contribution provides diminishing returns; defect to preserve endowment.

- **Final round**: Use a stricter 75% threshold before cooperating. Once no future rounds exist, there's no mechanism to reciprocate cooperation, so only cooperate if very strong evidence of collective commitment exists. Otherwise defect.

- **If all opponents defect from round 1 onward**: Cooperate in round 1 only, then defect from round 2 onwards. Recognize the group cannot sustain cooperation and preserve endowment.

- **If cooperation collapses mid-game**: Immediately switch to defection and remain in defection until late-game re-evaluation (round r-1).

**Collective Alignment:**

This strategy stabilizes high-cooperation outcomes when opponents employ reciprocal logic (rewarding cooperation, punishing defection), while gracefully degrading to individual endowment preservation against pure defectors. It avoids mutual exploitation spirals by enforcing a reciprocity norm: sustained cooperation requires demonstrated cooperation from peers.
'''

description_COLLECTIVE_27 = '''
## Adaptive Reciprocal Cooperation Strategy

**Decision Framework**

Maintain cooperation conditional on observing sufficient participation. Use the observed cooperation rate from the previous round to inform current play.

**Round 1 (Initialization)**
Cooperate unconditionally. This signals willingness to participate in collective benefit and generates initial information about the group's composition.

**Rounds 2 to r-1 (Adaptive Phase)**
Observe the number of cooperators c_prev from the previous round. Calculate the cooperation rate: ρ = c_prev / n

Decision rule:
- If ρ ≥ θ_high: Cooperate
- If ρ < θ_low: Defect
- If θ_low ≤ ρ < θ_high: Cooperate (with gradual transition)

where thresholds are:
- θ_high = (k + 1) / (2n) + 0.5, or more simply: cooperate if the public goods payoff share (k/n) × c_prev is sufficiently large
- θ_low = slightly below θ_high to avoid oscillation; specifically set θ_low = max(1/n, (k-1)/(2n) + 0.4)

Intuition: When observed cooperation rate suggests the public good yields meaningful returns, participate. When it drops below profitability relative to defection, withdraw.

**Round r (Endgame)**
If cooperation rate in round r-1 was ≥ 0.6: Cooperate (maintain momentum toward mutual cooperation even without future consequences).

If cooperation rate in round r-1 was < 0.6: Defect (no incentive to contribute when punishment/reward mechanisms have ended and group coordination has failed).

**Robustness Adjustments**

- Against free-riders: Defection when cooperation drops signals non-exploitation; this creates aggregate pressure against pure defectors.
- Against cooperators: Your initial cooperation and reciprocal response sustains mutual benefit.
- Against mixed populations: The threshold-based approach automatically calibrates participation to group composition.
- Against temporal decay: The gradual endgame shift accounts for diminishing value of future reputation.
'''

description_COLLECTIVE_28 = '''
# Threshold Reciprocity Strategy

**Round 1 (Bootstrap):** Cooperate unconditionally. Establish cooperation and signal willingness to contribute to the collective good.

**Rounds 2 through r-1 (Conditional Reciprocity):** 
- Observe m = number of cooperators in the previous round
- Compute the cooperation rate among all n players: rate = m / n
- **Cooperate if rate ≥ τ**
- **Defect if rate < τ**

Where threshold τ = (n + 1) / (2n), or approximately 0.5 for large n. This ensures cooperation is sustained when at least half the players cooperated in the prior round.

**Round r (Final Round):** Apply the same threshold rule as rounds 2 through r-1. Do not defect in the final round solely because it's the last round. Maintain reciprocal commitment to the group's established pattern.

**Rationale for threshold placement:**
The threshold is set at the majority point because:
- If m/n ≥ 0.5, the group is sustaining cooperative effort; your contribution adds value proportional to existing momentum
- If m/n < 0.5, defection-dominated behavior is emerging; reciprocating by defecting signals that unilateral cooperation is not sustainable
- This creates a coordination target: once the group crosses the majority threshold, mutual cooperation becomes self-reinforcing

**Handling edge cases:**
- If opponents oscillate around the threshold, your strategy amplifies this oscillation to test whether the group can stabilize above threshold—a collective learning signal
- If opponents universally defect by round 2, you defect thereafter, minimizing losses from futile contribution
- If opponents achieve full cooperation and maintain it, you continue cooperating indefinitely, achieving maximum collective payoff
'''

description_COLLECTIVE_29 = '''
# Adaptive Public Goods Cooperation Strategy

**Round 1: COOPERATE**

Initiate cooperation to establish mutual contribution. Without history, this is the only sensible collective starting point.

**Rounds 2 to r:**

Observe the number of cooperators m from the previous round. Apply the threshold rule:

```
if m ≥ ceil(k):
    COOPERATE
else:
    DEFECT
```

**Rationale for the threshold:**

The threshold k represents the multiplication factor. When at least k players cooperate, the public good is sufficiently multiplied to generate meaningful per-capita return (approaching k/n for each player). Below this level, the collective benefit erodes and the public project fails to justify further participation. Defecting at low cooperation rates signals that insufficient reciprocation has occurred, while remaining cooperative when cooperation meets or exceeds the threshold aligns individual play with collective welfare maximization.

**Edge case — terminal round:**

Apply the same threshold rule through the final round. While individual incentive analysis suggests defection in round r, collective welfare is still maximized by the threshold rule: if enough others have cooperated to sustain the project (m ≥ k), contributing in the final round generates net positive total payoff. Breaking this pattern purely for individual advantage undermines the collective cooperation that generated value throughout the game.

**Recovery mechanism:**

If cooperation drops below k in any round, defection occurs. However, the strategy immediately resets the cooperation attempt if cooperation recovers above k in a subsequent round, allowing collective coordination to rebuild after temporary defection shocks.
'''

description_COLLECTIVE_30 = '''
# Conditional Cooperation with Majority Threshold

**Parameter Definition:**
- θ = ceil(n/2) — the cooperation threshold (majority of players)

**Decision Rules:**

**Round 1:** Cooperate

This signals initial willingness to cooperate and establishes the baseline.

**Rounds 2 through r:**
- Observe m = the number of cooperators in the immediately previous round
- If m ≥ θ: Cooperate
- If m < θ: Defect

**Rationale for Threshold:**
Use the majority threshold because:
- If ≥50% of players cooperate, the collective is in a cooperative regime where the public good provides measurable benefit
- Below this level, defection becomes protective — the public good is being underfunded and you avoid being exploited
- This threshold is symmetric and doesn't require assumptions about specific opponent strategies

**Endgame Consistency:**
Apply the same conditional rule in round r (the final round). Do not defect automatically in the last round. This maintains reciprocal signaling and prevents strategic unraveling. If cooperation has been sustained, signal that intent through round r.

**Adaptation Mechanism:**
The strategy naturally adapts across the r rounds:
- If cooperation emerges and stabilizes above θ, you cooperate throughout
- If defection becomes prevalent, you switch to defection and stop subsidizing a failing collective effort
- Recovery is possible: if others return to high cooperation (m ≥ θ), you resume cooperating immediately

**Handle Transient Fluctuations:**
The single-round observation window means temporary dips below θ trigger defection. This is intentional — it creates pressure for sustained cooperation rather than tolerating sporadic free-riding.
'''

description_COLLECTIVE_31 = '''
**STRATEGY: Generous Threshold Cooperation with Symmetric Treatment**

**Round 1 (Initialization):**
Cooperate unconditionally. This opens the door to mutual cooperation and provides no hostile signal.

**Rounds 2 through r (Adaptation Phase):**
Let c_prev = number of cooperators observed in the previous round.

- If c_prev ≥ ceil(n/2): Cooperate
- If c_prev < ceil(n/2): Defect

**Final Round (r):**
Apply the same decision rule as Rounds 2 through r-1. Do not defect unconditionally. Treat the final round symmetrically to avoid triggering defection spirals from opponents using similar reciprocal strategies.

**Rationale for Thresholds:**

The threshold of at least 50% cooperation (ceil(n/2) cooperators) serves three functions:
1. **Optimism bias:** Cooperate if cooperation appears sustainable—a majority cooperating suggests the system can produce mutual gains
2. **Self-enforcement:** When cooperation crosses the majority threshold, it becomes individually rational for me to cooperate (k > 1 means collective benefit exceeds private loss)
3. **Punishment signal:** Defecting when cooperation falls below 50% imposes costs on free-riders by reducing their share of the public good

**Edge Cases:**

- If n is even and exactly n/2 cooperate: cooperate (benefit of doubt)
- If all others defect (c_prev = 0): defect (no public good to capture)
- If all others cooperate (c_prev = n-1): cooperate (sustainability confirmed)

This strategy is collectively aligned because: (1) it bootstraps cooperation when possible, (2) it punishes free-riding proportionally, and (3) it avoids unilateral last-round defection that would degrade collective outcomes.
'''

description_COLLECTIVE_32 = '''
# Threshold-Conditional Cooperation with Graduated Response

## Decision Rules

**Round 1:**
Cooperate unconditionally. This signals willingness to contribute and establishes a cooperative baseline.

**Rounds 2 to r-1 (non-terminal rounds):**
Let m_t denote the number of cooperators in round t.

Define threshold τ = ⌈(n-1) × (k/(1+k))⌉, representing the minimum cooperation level needed for meaningful collective benefit.

- If m_{t-1} ≥ τ: **Cooperate**
- If m_{t-1} < τ: **Defect** (apply punishment to signal dissatisfaction with free-riding)
- After defecting for one round, if m_t recovers to ≥ τ: **resume cooperation** in round t+1 (allow recovery)

**Round r (final round):**
Defect unconditionally. In the last round, no future reputation effects exist, making defection individually optimal. This is a known limitation, but unavoidable without communication.

*Alternative for Round r:* If m_{r-1} ≥ τ and round r is "close to final" (r ≤ 3 remaining), consider cooperating to sustain the norm, at cost of r/(n*k) expected payoff loss.

## Edge Cases

- **If all opponents defect from the start (m_1 = 0):** Switch to perpetual defection—chasing cooperation in a fully defecting population is futile.
- **Threshold never reached in early rounds:** Defect and remain in defection until a recovery signal appears; do not re-enter cooperation until τ is clearly met for two consecutive rounds.
- **n = 2 (two-player case):** Set τ = 2. Require mutual cooperation; defect if opponent defects.
- **Very small r (r ≤ 3):** Cooperate rounds 1 and 2 regardless of history; defect only in round r.

## Alignment with Collective Mindset

This strategy prioritizes:
- **Norm enforcement:** Defection punishes free-riders, creating incentives for universal cooperation.
- **Coordination on Pareto-efficient equilibrium:** By maintaining high-cooperation steady state when possible, all players move toward payoff k rather than payoff 1.
- **Graceful degradation:** If cooperation cannot be sustained, exit cleanly rather than cycle wastefully.
- **Fairness:** All players adopting this strategy face symmetric incentives and symmetric payoffs in equilibrium.

The strategy balances individual protection (defect when cooperation fails) against collective welfare (cooperate when cooperation is broadly maintained), ensuring robustness against both exploiters and cooperative players alike.
'''

description_PROSOCIAL_5 = '''
# Adaptive Conditional Cooperation Strategy

## Decision Rules

**Round 1:**
Cooperate unconditionally. This establishes an initial signal of good faith and cooperation.

**Rounds 2 through r-1 (intermediate rounds):**
- Observe the number of opponents who cooperated in the previous round: let C_{t-1} denote this count (ranging from 0 to n-1).
- Cooperate if: C_{t-1} ≥ ⌈(n-1)/2⌉
- Defect if: C_{t-1} < ⌈(n-1)/2⌉

In other words, cooperate if a majority (or near-majority) of other players cooperated in the previous round. Defect if cooperation dropped below this threshold.

**Round r (final round):**
Cooperate unconditionally, regardless of the previous round's outcome.

## Threshold Justification

The threshold ⌈(n-1)/2⌉ represents strict majority cooperation among other players. This is a natural focal point:
- It rewards cooperative growth: mutual cooperation is encouraged when most others participate
- It resists exploitation: defection by half or more triggers your own defection, limiting losses
- It allows graceful degradation: cooperation can sustain itself as long as majorities cooperate

## Edge Cases

- **First round asymmetry:** Round 1 cooperation is unconditional because you have no history and must initiate.
- **Last round reversal:** Final round cooperation is unconditional to reinforce cooperative norms and demonstrate commitment to prosocial behavior, not just instrumental reciprocity.
- **Tie scenarios:** When C_{t-1} equals the threshold exactly, cooperate (biased toward prosocial action).
- **Oscillation:** If others' cooperation oscillates around the threshold, your strategy naturally mirrors this, allowing re-entry into cooperation when majorities return.

## Prosocial Character

This strategy is prosocial because it:
1. **Initiates cooperation** rather than defaulting to defection
2. **Responds positively to reciprocation** by matching cooperative signals
3. **Prioritizes mutual benefit:** the structure enables mutual cooperation payoffs when most players follow similar logic
4. **Builds cooperative norms** through last-round cooperation, signaling that cooperation is valuable in itself
5. **Stops short of naive exploitation:** defection against uncooperative coalitions protects against systematic free-riding while remaining open to reconciliation
'''

description_PROSOCIAL_6 = '''
**ADAPTIVE CONDITIONAL COOPERATION WITH ENDGAME COMMITMENT**

**Round 1 (First round):**
Cooperate (C). Signal prosocial intent and establish mutual benefit baseline.

**Rounds 2 to r−1 (Middle rounds):**
Let c_prev = number of opponents who cooperated in the previous round.
Let threshold τ = ⌈(n−1)/2⌉ (majority threshold).

- If c_prev ≥ τ: Cooperate (C)
- If c_prev < τ: Cooperate with probability p = c_prev / (n−1); otherwise Defect (D)

This creates reciprocal escalation and de-escalation. When most others cooperate, commit fully. When cooperation declines, gradually reduce your own contribution rather than punishing harshly, preserving the possibility of recovery.

**Final round r (Last round):**
Cooperate unconditionally (C). This is the crucial prosocial commitment: defect-in-endgame is individually rational but socially destructive. Demonstrating willingness to cooperate even when consequences are imminent signals genuine prosocial orientation, which may influence others' strategies in concurrent games or seed future cooperation norms.

**Edge case: n = 2**
With only one opponent, threshold becomes τ = 1 (need full cooperation to reciprocate fully). The probabilistic fallback prevents collapse into mutual defection.

**Edge case: Very low k**
Even with marginal multiplier, middle-round probabilistic reciprocation maintains hope that escalation can recover collective benefit. The endgame commitment prevents complete exploitation.
'''

description_PROSOCIAL_7 = '''
# STRATEGY: Conditional Cooperation with Prosocial Threshold

## Decision Rules

**Round 1:** Cooperate

**Rounds 2 through r:** 
- Observe m = total number of cooperators in the previous round
- Calculate threshold: τ = max(⌈n/k⌉ − 1, 1)
- If m ≥ τ: Cooperate
- If m < τ: Defect

## Threshold Justification

The threshold is calibrated to the cooperation break-even point. When m cooperators contribute:
- Cooperator payoff: (k/n) × m
- Defector payoff: 1 + (k/n) × m

Cooperation yields equal or better payoff when (k/n) × m ≥ 1, or m ≥ n/k. Setting the threshold at ⌈n/k⌉ − 1 creates a **prosocial bias**: we cooperate even when cooperation is marginally suboptimal, giving others a chance to sustain collective welfare.

The max(·, 1) ensures we don't set an impossible threshold of zero.

## Edge Cases

**First round:** Unconditional cooperation signals trustworthiness and kickstarts reciprocity in a coordination problem.

**Last round:** Apply the same rule, not defection. This maintains consistency and prevents unilateral opportunism from undermining the strategy's overall prosocial character. If we defect only when others won't, we're still contributing to collective good.

**All defectors (m = 0):** Defect, since the public good produces negligible returns. Resume cooperation immediately if m ≥ τ next round.

**Unanimous cooperation (m = n):** Continue cooperating; mutual cooperation is stable.

## Prosocial Properties

- **Reciprocity:** Matches cooperation from others, not exploiting them
- **Generosity:** Threshold is set *below* break-even, forgiving occasional free-riding
- **Resilience:** Doesn't cascade into mutual destruction when defection appears; allows recovery
- **Consistency:** Same rule throughout the game prevents gaming the last round
- **Transparency:** Behavior is fully determined by observable aggregate history, enabling others to predict and coordinate with this strategy
'''

description_PROSOCIAL_8 = '''
# COOPERATIVE THRESHOLD STRATEGY

## Core Decision Rule

Cooperate in round t if and only if:
```
IF round == 1:
    COOPERATE
ELSE:
    cooperation_rate = (cooperators_observed_in_round_t-1) / (n - 1)
    threshold = compute_threshold(t, r, n)
    IF cooperation_rate >= threshold:
        COOPERATE
    ELSE:
        DEFECT
```

## Threshold Computation

Dynamically adjust the cooperation threshold based on game phase:

```
compute_threshold(current_round, total_rounds, num_players):
    
    IF current_round <= 2:
        return 0.40  // Optimistic opening: tolerate free-riders if majority cooperate
    
    ELSE IF current_round <= total_rounds - 2:
        // Mid-game: scale threshold by round progress
        progress_ratio = (current_round - 3) / (total_rounds - 4)
        return 0.55 + 0.15 × progress_ratio
    
    ELSE:
        // Final two rounds: endgame selectivity
        return 0.80
```

## Edge Cases

**Round 1:** Unconditional cooperation. Establishes prosocial intent regardless of opponent strategies.

**Rounds 2–3:** Maintain low threshold (0.40). Even if only 40% of observed opponents cooperated last round, continue cooperating to allow reciprocal cooperation patterns to emerge.

**Final round (t = r):** Apply 0.80 threshold strictly. You extract value if others defected; you avoid single-round losses if others are clearly uncooperative. If threshold met, cooperate (not purely myopic defection).

**Threshold boundary:** If cooperation_rate exactly equals threshold, cooperate (break ties toward cooperation).

## Prosocial Logic

This strategy embodies conditional prosociality: it initiates cooperation, rewards observed cooperation by others with continued cooperation, and gradually becomes more selective only as opportunities to sustain mutual cooperation diminish. It avoids indefinite punishment (no grudge-holding across phases) while protecting against exploitation by maintaining defection against consistently low-cooperation groups.
'''

description_PROSOCIAL_9 = '''
# Adaptive Reciprocal Cooperation Strategy

**Round 1 (Initial cooperation):**
Cooperate. This establishes prosocial intent and tests whether others reciprocate.

**Rounds 2 through r-1 (Reciprocal adaptation):**
- Observe the number of cooperators in the previous round: m_{t-1}
- Calculate the cooperation threshold: θ = ceil(k)
- If m_{t-1} ≥ θ, cooperate in round t
- Otherwise, defect in round t

This threshold is calibrated to the multiplication factor. When k cooperators exist, the public good contribution to a cooperator is (k/n) × k = k²/n. Since defection gives payoff 1 + (k/n) × (k-1), cooperation is justified when the group is sustaining sufficient momentum. The threshold of ceil(k) ensures you cooperate when enough others are cooperating to make the public pool meaningful.

**Final round r (Continued commitment):**
Apply the same reciprocal rule as rounds 2 through r-1. Do not defect strategically in the final round—maintain consistency with the strategy.

**Edge cases:**
- If you ever observe zero cooperators in a round, defect in the next round (no public good to support).
- If you observe all n cooperators, continue cooperating (mutual cooperation is optimal).
- On the first round only, cooperate regardless of parameters to initiate group-beneficial behavior.

**Rationale:**
This strategy is prosocial because it: (1) makes the first move cooperative, inviting reciprocation; (2) rewards cooperation with cooperation and withdraws when the group abandons the public good; (3) uses a parameter-dependent threshold that scales with game structure; (4) maintains commitment through the final round rather than exploiting others' continued cooperation through last-round defection.
'''

description_PROSOCIAL_10 = '''
# Conditional Cooperation with Majority Threshold

**COOPERATION DECISION RULE:**

Cooperate if and only if one of the following holds:
- Current round is round 1
- Current round is round r (the final round)
- In the immediately preceding round, at least 50% of all players cooperated (i.e., total_cooperators_previous_round ≥ n/2)

Otherwise, defect.

**FORMAL SPECIFICATION:**

```
if t == 1:
    action = COOPERATE
elif t == r:
    action = COOPERATE
else:
    prev_cooperation_rate = (previous_round_cooperators / n)
    if prev_cooperation_rate >= 0.5:
        action = COOPERATE
    else:
        action = DEFECT
```

**EDGE CASES:**

- **Round 1:** Always cooperate. This unconditionally signals willingness to contribute to the collective good, regardless of prior expectations.
- **Last round (round r):** Always cooperate. This avoids exploitative end-game defection and sustains the norm of cooperation throughout the interaction. The prosocial player does not free-ride when cooperation becomes hardest to enforce.
- **Rounds 2 to r-1 with exactly n/2 cooperators:** Cooperate. The threshold is non-strict (≥ rather than >), treating perfect parity as sufficient evidence that cooperation is a reasonable collective strategy.
- **Very low cooperation (e.g., one cooperator last round):** Defect. When cooperation collapses below majority, the strategy withdraws contribution rather than sustain one-sided support.

**PROSOCIAL ALIGNMENT:**

This strategy pursues joint welfare maximization within the constraints of observable aggregate information. It initiates cooperation unconditionally to establish trust, reciprocates majority-level cooperation to reward collective efforts, and refuses to be a lone contributor when the group has abandoned mutual support. By always cooperating in the final round despite the payoff incentive to defect, it prioritizes the social norm of cooperation and leaves opponents with a prosocial final interaction, creating the possibility for emergent mutual gain even in repeated settings with limited information.
'''

description_PROSOCIAL_11 = '''
## Generous Reciprocity Strategy

**Core Logic:** Cooperate by default, withdraw only if others substantially abandon cooperation. Return to cooperation if others return.

### Decision Rule by Round

**Round 1:**
Cooperate unconditionally. Extend initial trust.

**Rounds 2 through r:**
- Observe the cooperation rate from the previous round: `rate_prev = (number of cooperators in round t-1) / n`
- Calculate the reciprocity threshold: `threshold = (1/k) × 0.95`
  - The term `1/k` represents the breakeven point where mutual cooperation yields the same payoff as unilateral defection
  - The `0.95` factor embeds prosocial optimism: cooperate even when past conditions fall slightly short of this threshold, to encourage restoration of cooperation
- Decision: Cooperate if and only if `rate_prev ≥ threshold`

**Final round (t = r):**
Apply the same reciprocity rule. Do not defect merely because it is the last round—this preserves the strategy's integrity and cooperative signaling.

### Edge Cases

- If threshold becomes negative or undefined (when k ≥ n, though excluded here), treat `threshold = 0.2` as a floor—remain pessimistic but not vindictive.
- In round 1, you have no history; cooperate regardless.
- If a round produces cooperation rate exactly at the threshold, cooperate (boundary condition favors cooperation).

### Prosocial Alignment

This strategy prioritizes collective benefit by:
- Leading with cooperation rather than defection
- Reciprocating genuinely high cooperation without defecting opportunistically
- Using a discounted threshold (0.95× rather than 1.0×) to signal forgiveness and willingness to rebuild mutual cooperation after dips
- Never punishing the final round differently, maintaining consistent cooperative intent throughout
'''

description_PROSOCIAL_12 = '''
# Adaptive Threshold Cooperation Strategy

**Decision Rule:**

Round 1: Cooperate (prosocial opening signal)

Rounds 2 through r:
- Observe the cooperation rate from the previous round: `coop_rate = cooperators_last_round / n`
- Threshold: `threshold = 1 / k`
- If `coop_rate > threshold`: Cooperate
- Else: Defect

**Rationale for Threshold:**

When a fraction p of the population cooperates, your payoff from cooperating equals `(k/n) × p × n = k × p`. Your payoff from defecting equals `1 + k × p`. Defection always yields k units more per round in isolation.

However, when `p > 1/k`, the absolute payoff from cooperation (k × p) exceeds 1—the mutual defection baseline. This threshold marks the sustainability boundary: cooperation only becomes collectively rational beyond this point. Below it, the group has abandoned cooperation.

**Prosocial Elements:**

1. **Opening cooperatively** signals willingness and invites reciprocation, increasing chances that others adopt compatible strategies.

2. **Conditional cooperation rewards collective behavior** without requiring identification of specific players. By coordinating on the same threshold, cooperators can sustain higher payoffs together.

3. **Threshold prevents exploitation** by switching off when cooperation collapses, protecting against unbounded free-riding. You defect only when the group has already failed to maintain a cooperative baseline.

4. **Invariant across rounds** until the final round, which the same rule governs. This consistency aids implicit coordination.

**Edge Cases:**

- If `n = 2` and `k = 1.5`, threshold is `2/3`. You defect only if fewer than one opponent cooperated (i.e., both defected).
- Very small `k` (near 1) raises the threshold toward 1, demanding near-universal cooperation to sustain your contribution. Very large `k` (approaching n) lowers it, making cooperation sustainable with fewer participants.
'''

description_PROSOCIAL_13 = '''
**Decision Rule:**

Maintain a running average of observed cooperation rates across all completed rounds. Let `avg_coop` denote the proportion of opponents who cooperated in the previous round (or average across all previous rounds).

- **Round 1**: Cooperate unconditionally. This signals prosocial intent and willingness to contribute to collective welfare.

- **Rounds 2 through r-1**: Cooperate if and only if `avg_coop ≥ threshold`, where `threshold = (k / n) + 0.1`. Defect otherwise.

- **Round r (final round)**: Apply the same threshold rule, but with a +0.15 buffer instead of +0.1 when computing threshold (i.e., `threshold_final = (k / n) + 0.15`). This maintains slight optimism in the endgame rather than collapsing to defection.

**Threshold Rationale:**

The threshold `(k/n) + buffer` targets sustainability of mutual cooperation. When cooperation rates exceed this level, the public good return makes collective play better than the all-defect outcome. The buffer prevents hair-trigger defection from minor random variance in opponent play.

**Edge Cases:**

- **If all opponents defect in round t** (cooperation rate = 0), defect in round t+1 unless at least one opponent cooperates again in the interim. This avoids futile contribution.

- **Revise upward after defection**: If you've been defecting and observe cooperation resurgence (e.g., avg_coop crosses threshold again), resume cooperation immediately. Never permanently lock out cooperation once established.

- **Very small n** (n=2 or n=3): Increase buffer to +0.2 due to high volatility in observed cooperation rates; single opponent behavior creates noisier signals.

**Prosocial Alignment:**

This strategy prioritizes mutual cooperation when feasible, leads with cooperation in round 1 to enable trust, punishes only persistent defection (not one-round noise), and remains forgiving by constantly re-evaluating rather than holding grudges. It seeks outcomes where all players benefit from the public good rather than maximizing individual gain at others' expense.
'''

description_PROSOCIAL_14 = '''
# Generous Threshold Conditional Cooperator

## Core Decision Rule

Cooperate if the observed cooperation rate of other players exceeds a threshold; otherwise defect. Maintain consistent behavior across all rounds including the final round.

## Specific Rules by Round

**Round 1:**
- Cooperate unconditionally
- Signal willingness to participate in the collective good

**Rounds 2 through r:**
- Let `observed_cooperators` = number of players observed cooperating in the previous round
- Calculate cooperation rate: `rate = observed_cooperators / (n - 1)`
- If `rate ≥ 0.25`, then Cooperate
- If `rate < 0.25`, then Defect

## Rationale for Parameters

**Threshold of 0.25 (25%):** Defect only when cooperation drops below one-quarter of other players. This reflects prosocial tolerance—you forgive widespread defection only when it becomes severe, giving the group multiple opportunities to establish cooperation even with mixed populations.

**No end-game defection:** Apply the same conditional rule in round r rather than opportunistically defecting. Exploiting in the final round contradicts the prosocial foundation and risks triggering defection in similar repeated interactions.

## Edge Cases

- **Unanimous defection (rate = 0):** Defect. Continuing cooperation against universal free-riding maximizes others' payoffs at pure cost to yourself.
- **Unanimous cooperation (rate = 1.0):** Cooperate. Sustains the mutual cooperation equilibrium that benefits all.
- **Mixed populations:** The 25% threshold allows cooperation to persist across diverse opponent strategies—you cooperate with generous cooperators, defectors-with-remorse, and even some unconditional defectors, while withdrawing from predominantly defecting groups.

## Why This Approach

The strategy avoids two extremes: always defecting (non-cooperative) and always cooperating (exploitable). By starting with trust and maintaining reciprocity at a generous threshold, it creates conditions for emergence of stable cooperation while protecting against systematic exploitation.
'''

description_PROSOCIAL_15 = '''
# Prosocial Adaptive Conditional Cooperation Strategy

**ROUND 1 (Initial Move):**
Cooperate.

This establishes prosocial intent and gives opponents the opportunity to reciprocate.

---

**ROUNDS 2 THROUGH r-1 (Adaptation Phase):**

Let C_prev = number of cooperators in the previous round.
Let c_prev = C_prev / n (cooperation rate).

Decision rule:

```
threshold_high = k / n
threshold_low = 1 / (2n)

if c_prev ≥ threshold_high:
    action = COOPERATE
elif c_prev ≥ threshold_low:
    action = COOPERATE
    (continue reciprocating, give benefit of doubt)
else:
    action = DEFECT
    (protect endowment if cooperation collapses)
```

**Interpretation:**
- If cooperation rate meets or exceeds k/n, mutual benefit is achievable—cooperate to sustain the dynamic.
- If cooperation drops below k/n but remains non-negligible, cooperate anyway. This is the prosocial commitment: maintain a cooperative posture to encourage recovery, rather than immediately defect.
- Only defect when cooperation falls near zero, signaling that the collective attempt has failed and individual protection is necessary.

---

**ROUND r (Final Round):**
Cooperate.

Rather than exploit the final round through defection (which would undermine prosocial intent), maintain cooperation to the end. This signals genuine prosocial commitment beyond strategic self-interest and may influence the emergent norm among participants.

---

**EDGE CASES:**
- If n = 2 and k ≤ 1.5, threshold_high approaches 0.5–0.75. Cooperate if the opponent cooperates.
- If k is very close to 1, thresholds compress toward zero; err toward cooperation (prosocial prioritization).
- If an opponent's strategy is unstable or erratic, threshold_low ensures you don't immediately defect but also don't enable unbounded exploitation.
'''

description_PROSOCIAL_16 = '''
# Adaptive Reciprocal Cooperation Strategy

## Core Decision Rule

**Round 1:** Cooperate unconditionally.

**Rounds 2 through r:** Observe the number of cooperators m in the immediately preceding round. Use the following rule:

- If m ≥ ⌈(n-1) × α⌉, Cooperate
- Else Defect

where α is a cooperation threshold parameter set to α = 0.4.

This means: Cooperate if at least 40% of your opponents cooperated in the previous round; otherwise defect.

## Rationale for Parameters

The 40% threshold reflects a prosocial stance:
- You will reciprocate cooperation generously (not requiring a majority)
- You avoid being exploited indefinitely (if fewer than 40% cooperate, you stop contributing)
- Early rounds with no cooperation history default to cooperation, seeding prosocial behavior

## Edge Cases

**Last round (t = r):** Apply the same rule. Even though you won't observe future responses, maintaining consistent behavior signals reliability and contributes to aggregate welfare.

**When m = 0:** All opponents defected. Switch to defection. Continuing to cooperate when no one else does wastes your endowment without payoff.

**When n is small (n = 2):** The threshold is 0.4 × 1 = 0.4, so you cooperate if your opponent cooperated (m ≥ 1) and defect if they defected (m = 0). This becomes pure tit-for-tat after round 1.

## Prosocial Alignment

- **Initiation:** Round 1 cooperation attempts to establish prosocial norms
- **Reciprocity:** Matching observed cooperation rates maintains cooperation where others are willing
- **Fairness:** The 40% threshold is not retaliatory; it grants others significant latitude
- **Collective welfare:** By sustaining cooperation whenever moderate participation exists, the strategy pushes outcomes toward higher aggregate payoffs than pure defection
'''

description_PROSOCIAL_17 = '''
# GENEROUS CONDITIONAL COOPERATOR WITH RECOVERY THRESHOLD

## Thresholds
Define:
- `t_low = k/(2n)` (recovery threshold)
- `t_high = 2k/n` (full cooperation threshold, capped at 1)

## Decision Rules

**Round 1:**
Play C.

**Rounds 2 through r-1 (middle rounds):**
Let `m` = number of cooperators in the previous round.
- If `m/n ≥ t_high`: Play C
- Else if `m/n ≥ t_low`: Play C
- Else if `m ≥ 1`: Play C
- Else (m = 0): Play D

**Round r (final round):**
Let `m` = number of cooperators in round r-1.
- If `m/n ≥ t_low`: Play C
- Else: Play D

## Rationale

Start by cooperating to establish prosocial equilibrium. Maintain cooperation broadly: cooperate unless cooperation has completely collapsed. Use two thresholds—a high bar for sustainable cooperation and a low bar for recovery phases. If any other player cooperated (m ≥ 1), match that signal in middle rounds to encourage reciprocal cooperation. In the final round, switch to more strict defection only if cooperation has fully broken down, preserving prosocial intent even at game's end. Near-zero cooperation (m = 0) triggers a single defection to signal frustration, but the strategy does not persist in defection—it remains open to renewed cooperation in subsequent rounds.
'''

description_PROSOCIAL_18 = '''
**STRATEGY: Optimistic Reciprocity with Prosocial Floor**

**DECISION RULES:**

Round 1:
- Cooperate unconditionally.
- Signal prosocial intent and establish a cooperative anchor.

Rounds 2 through r–1 (Middle rounds):
- Let p_prev = (number of cooperators in round t–1) / n
- Compute threshold: T = max(1/k, 0.35)
  - 1/k reflects the break-even point where public good value equals individual defection gains
  - 0.35 is a prosocial floor that tolerates moderate free-riding without total collapse
- Decision:
  - If p_prev ≥ T: Cooperate
  - If 0 < p_prev < T: Cooperate (grant one-round grace period; others may be learning)
  - If p_prev = 0: Defect (match zero cooperation; no basis for recovery)
- Special case for rounds 2–3: Set T_lenient = min(1.0, 1/k + 0.15) for these first two observation windows. Use this higher threshold instead to accommodate initial coordination difficulty.

Round r (Final round):
- Let p_prev = cooperation rate in round r–1
- Let p_avg = average cooperation rate across all previous rounds
- Decision:
  - If p_prev ≥ T: Cooperate (current momentum favors cooperation)
  - If 0 < p_prev < T and p_avg ≥ T: Cooperate (group historically cooperative; treat this as a temporary dip)
  - If p_avg = 0: Defect (group never cooperated; consistency)
  - Otherwise: Cooperate (final gesture of good faith; demonstrate that cooperation is not purely conditional or self-interested)

**EDGE CASES:**

- If r = 2: Treat round 2 as both "middle" and "final." Apply final-round logic: cooperate if round 1 had any cooperators, or if you wish to show consistent commitment.
- If n = 2: Threshold T applies identically; you are still observing aggregate behavior rather than individual identity.
- Tied thresholds: When p_prev exactly equals T, cooperate (round toward cooperation).
- All-defect trajectory: Once p_prev = 0 for two consecutive rounds, defect thereafter (evidence of systemic non-cooperation, not temporary noise).

**PROSOCIAL ALIGNMENT:**

This strategy embodies prosocial values by:
- Leading with cooperation in early rounds, shifting the norm rather than assuming the worst.
- Using reciprocity with slack: granting grace periods when cooperation drops below threshold rather than harshly punishing one-round dips.
- Protecting the public good: the threshold T ensures you contribute only when aggregate cooperation is meaningful, not when you are funding a nearly empty pool.
- Final-round honesty: cooperating in the last round (conditional on some history of cooperation) signals that your prosociality is genuine rather than purely strategic or contingent on continued payoff.
- Abandoning unrecoverable groups gracefully: defecting only after clear evidence that the group has chosen non-cooperation, avoiding pointless self-sacrifice.
'''

description_PROSOCIAL_19 = '''
# Adaptive Threshold Cooperation Strategy

## Core Decision Rule

**Rounds 1 through r:**

Cooperate if the observed cooperation rate from the previous round meets or exceeds a dynamic threshold. Otherwise defect.

```
IF round == 1:
  action = COOPERATE
  
ELSE:
  observed_rate = cooperators_last_round / n
  threshold = k / n
  tolerance = 0.15  // tolerance band for noise/variance
  
  IF observed_rate >= threshold:
    action = COOPERATE
    
  ELSE IF observed_rate >= (threshold - tolerance):
    action = COOPERATE with probability (observed_rate / threshold)
    // graceful degradation
    
  ELSE:
    action = DEFECT
```

## Rationale for Thresholds

The threshold `k/n` represents the expected per-capita return when all players cooperate. If the observed cooperation rate falls significantly below this, the public good is underfunded and continued contribution becomes individually exploitative to you.

The tolerance band `threshold - tolerance` creates a generosity buffer: you continue cooperating even if cooperation drops slightly below ideal, absorbing small fluctuations and noise in opponent behavior rather than triggering immediate defection.

## Edge Cases

**Round 1 (cold start):** 
Cooperate unconditionally. This signals prosocial intent and allows the strategy to be "provably" cooperative to any observant opponent.

**Rounds 2 to r-1 (middle rounds):**
Use the full adaptive rule above. History informs all decisions.

**Round r (final round):**
Apply the same rule. Do not defect purely due to backward induction—maintain commitment to the conditional cooperation strategy through the entire game, preserving the prosocial character even when reputation effects formally end.

## Adaptive Refinement

If you observe steady high cooperation (rate > threshold for 3+ consecutive rounds), lower the tolerance band slightly to reward robust cooperation. If you observe sustained low cooperation (rate < threshold - tolerance for 2+ rounds), increase defection probability in the tolerance band to protect expected payoff.
'''

description_PROSOCIAL_20 = '''
# Prosocial Threshold Cooperation

**Threshold Calculation:**
Compute the break-even cooperation level: `threshold = ceil(n / k)`

This is the minimum number of cooperators needed in a round for your contribution to yield non-negative personal payoff. Below this, cooperation is collectively beneficial but individually costly.

**Decision Rules:**

**Round 1:**
Cooperate unconditionally. This serves as a prosocial opening signal and tests responsiveness.

**Rounds 2 through r−1 (Intermediate Rounds):**
Observe the number of cooperators in the previous round. Let `c_prev` denote this count.

- If `c_prev ≥ threshold`: Cooperate
- If `c_prev < threshold`: Defect

**Round r (Final Round):**
Compute the average cooperation count across all prior rounds: `avg_coop = mean(c_1, c_2, ..., c_{r-1})`

- If `avg_coop ≥ threshold`: Cooperate
- If `avg_coop < threshold`: Defect

**Prosocial Orientation:**

This strategy is prosocial because:

1. **Reciprocal trust-building**: It initiates with cooperation and maintains it precisely when others' contributions make collective welfare superior to mutual defection.

2. **Generous threshold**: The threshold `ceil(n / k)` is the *minimum* viable cooperation level. It avoids being exploited (free-riding when nearly everyone defects) while cooperating generously whenever cooperation is sustainable.

3. **Final round principle**: In the last round, the decision is anchored to the *average* cooperation trend rather than immediate self-interest. This reflects commitment to cooperative groups even at the temporal edge.

4. **Patience with variability**: The strategy doesn't punish single-round dips below threshold; it resets each round based only on the prior round's count. This allows recovery from temporary defection.

**Edge Cases:**

- If all players defect from round 2 onward (`c_prev = 0`), the strategy defects—avoiding the "sucker's payoff" of funding others' free-riding.
- If cooperation gradually erodes, defection follows naturally without punishment cycles.
- If cooperation recovers partway through the game, cooperation resumes immediately.
'''

description_PROSOCIAL_21 = '''
# Cooperative Tipping Point Strategy

**ROUND 1:** Cooperate unconditionally. This signals willingness to contribute and establishes a cooperative baseline.

**ROUNDS 2 TO r:** 
Observe the cooperation rate from the previous round: `rate_prev = (number of cooperators in round t-1) / n`

Apply the following decision rule:

```
if rate_prev ≥ 0.5:
    Cooperate
else if 0.2 < rate_prev < 0.5:
    Cooperate with probability = 0.2 + rate_prev
else:
    Defect
```

**LAST ROUND (round r):** Apply the same decision rule as above. Do not implement end-game defection. Maintain consistency to reinforce commitment to cooperation.

---

**EDGE CASES & CLARIFICATIONS:**

- **Exactly at thresholds:** Treat 0.5 and 0.2 as inclusive on the lower bound (≥ and >).
- **n=2 case:** The strategy adapts naturally. If your sole opponent cooperated (rate=1.0), cooperate. If they defected (rate=0), defect.
- **Very large n:** Rare but possible that you're the only cooperator. The strategy degrades gracefully: low cooperation rates trigger increased defection, limiting unilateral sacrifice.
- **k close to 1:** When the multiplier is weak, cooperation becomes harder to justify. The strategy remains applicable; the thresholds function as your calibration points regardless of k's value.

---

**PROSOCIAL ALIGNMENT:**

This strategy prioritizes collective welfare by maintaining cooperation when others reciprocate, avoiding the trap of mutual defection spirals. The probabilistic zone (0.2 < rate < 0.5) prevents abrupt strategy shifts and preserves some cooperation investment even as others become less trustworthy, encouraging rather than punishing emergent coordination. By refusing end-game defection, it signals that your commitment to cooperation is genuine, not opportunistic. The 0.5 threshold reflects empirically-robust social cooperation: majority cooperation sustains; minority cooperation collapses.
'''

description_PROSOCIAL_22 = '''
# Adaptive Reciprocal Cooperation Strategy

## Decision Rules

**Round 1 (Opening):**
Cooperate unconditionally. Establish prosocial intent and signal willingness to contribute to the collective good.

**Rounds 2 through r-1 (Middle Rounds):**
- Let M_prev = number of opponents observed to cooperate in round t-1
- Calculate opponent cooperation rate: p_prev = M_prev / (n - 1)
- **Cooperate if and only if: p_prev ≥ 1/3**
- Otherwise, Defect

The 1/3 threshold balances two objectives: it rewards cooperation among opponents while avoiding exploitation when cooperation becomes sparse. This threshold is loose enough to incentivize cooperation patterns (if one-third are cooperating, you cooperate back; this can stabilize higher cooperation equilibria) but strict enough that systematic defection doesn't trap you into one-sided losses.

**Round r (Final Round):**
Cooperate unconditionally. In the final round, there is no future reputation effect or behavioral influence, so the purely prosocial action—maximizing the collective good—is to contribute.

## Edge Cases

- **All opponents defected previously:** Play Defect in the current round. This prevents exploitation when the group has clearly rejected cooperation.
- **All opponents cooperated previously:** Play Cooperate. Maintain and reinforce the cooperative equilibrium.
- **Exactly 1/3 cooperation:** Cooperate. The threshold is inclusive; meet the group at the boundary where reciprocation makes sense.

## Prosocial Framing

This strategy prioritizes encouraging and sustaining high-welfare collective outcomes:

- The initial cooperation signal gives the group an opportunity to establish mutual benefit before strategic pessimism takes hold.
- The adaptive threshold in middle rounds creates incentives for others to cooperate—if most opponents see cooperation rewarded, they learn that contribution is reciprocated.
- The final-round cooperation commits to the public good when individual incentives no longer dominate, demonstrating that the strategy values group welfare, not just personal gain.
- The defection trigger (p < 1/3) protects against one-sided exploitation but remains forgiving enough to allow recovery if others are experimenting or adapting.
'''

description_PROSOCIAL_23 = '''
# Threshold-Based Prosocial Cooperation Strategy

**Decision Rule:**

Calculate the sustainability threshold: `min_coop = ⌈n / k⌉`

In round t:
- If t = 1: **Cooperate**
- If t > 1: **Cooperate if and only if** the number of cooperators observed in round t-1 was ≥ min_coop; otherwise **Defect**

**Rationale for the threshold:**

When exactly min_coop players contribute, the public good yields (k/n) × min_coop = k/⌈n/k⌉ ≈ 1, which recovers your endowment. Below this threshold, cooperation becomes individually non-viable (you lose value). At or above this threshold, the social multiplier justifies your contribution cost.

**Edge case handling:**

- **Round 1:** Always cooperate. This is the prosocial signal that anchors the game toward mutual benefit rather than immediate defection. It also provides information to gauge opponents' willingness.

- **Intermediate rounds (2 to r-1):** Apply threshold rule consistently. The aggregate feedback from each round tightens the strategy—if cooperation collapses below min_coop, you withdraw. If it sustains, you continue.

- **Final round:** Apply the same threshold rule. Do not execute "endgame defection." Maintaining consistency signals commitment to cooperation and avoids the tragedy of backward induction. This preserves the possibility of stable cooperative equilibrium and respects players who have cooperated.

- **Special case (r=2):** Round 1 is the prosocial opener; round 2 applies the threshold. Both rounds execute the intended logic.

**Prosocial properties:**

- Initiates cooperation in good faith
- Only sustains it when mathematically feasible for all participants
- Never exploits others by defecting when they successfully maintain the threshold
- Avoids endgame betrayal, supporting repeated-game cooperation norms
- Adapts to a spectrum of opponent behaviors (pure cooperators, defectors, conditional cooperators) without requiring opponent modeling
'''

description_PROSOCIAL_24 = '''
**STRATEGY: Adaptive Threshold Cooperator with Prosocial Initialization**

**Decision Rule by Round:**

**Round 1 (Initialization):** Cooperate.

**Rounds 2 through r-1 (Adaptive Rounds):** 
- Let c_prev = number of opponents who cooperated in the immediately preceding round
- Let ρ = c_prev / (n - 1) = observed cooperation rate among opponents
- Cooperate if and only if: ρ ≥ θ(t)
- Defect if ρ < θ(t)

Where the cooperation threshold θ(t) varies by game phase:

- **Early game (t ≤ r/2):** θ(t) = k/n
  - Cooperative as long as public good is valuable to both cooperators and defectors
  
- **Late game (t > r/2):** θ(t) = (k - ε) / n, where ε = min(0.1, k/10)
  - Slightly more stringent; reward only higher cooperation rates near the end

**Final round (t = r):** 
- Cooperate if ρ ≥ θ(r-1) from the previous round
- This maintains reciprocal commitment even when no future rounds follow

**Edge Cases:**

- **Broken cooperation streaks:** If cooperation collapses (ρ drops below threshold), defect for one round, then revert to threshold-checking. This is forgiving: re-cooperate immediately if cooperation recovers above the threshold.

- **Ties and boundary cases:** If ρ equals θ exactly, cooperate (inclusive inequality). This biases toward prosocial resolution of ambiguity.

- **Round 2 special case:** If round 1 had fewer than (n-1) × k/n cooperators, you may defect in round 2, but only if you're confident retaliation is justified—revert to threshold logic promptly thereafter.

**Prosocial Intent:**

Initiate universally to broadcast availability for cooperation. Sustain cooperation whenever opponents collectively reciprocate above the multiplication factor threshold, ensuring mutual benefit. Withdraw only when cooperation falls below the payoff-sufficiency point. Forgive and re-enter whenever cooperation returns, remaining open to rebuilding.
'''

description_PROSOCIAL_25 = '''
# Conditional Reciprocity with Prosocial Bias

**Core Decision Rule:**

Cooperate if and only if the observed fraction of cooperators in the previous round meets or exceeds a prosocial threshold. Specifically:

```
Let m_prev = number of cooperators observed in round t-1
Let coop_rate_prev = m_prev / (n - 1)  [exclude self-observation]

Cooperate in round t if:
  coop_rate_prev ≥ k / (n + 1)
  OR round = 1
  OR (defection_streak > 0 AND round ≤ r - 2)
```

The threshold k/(n+1) ensures you reciprocate when the public good marginal return is substantial relative to your endowment, while the second and third clauses embed prosocial bias.

**Edge Cases:**

- **Round 1 (cold start):** Cooperate unconditionally. Initiate trust to establish cooperative equilibrium potential.

- **Rounds 2 to r-2 (adaptive middle game):** Apply the threshold rule above. If cooperation has degraded to zero for two consecutive rounds, defect for one round as a costly signal of disapproval, then return to threshold rule (defection_streak counter resets after one round of signaling).

- **Final round r (endgame):** Use the same threshold rule rather than defaulting to defection. Avoid sudden defection betrayal even though the game ends, preserving reputation-like effects across future interactions and modeling prosocial commitment.

- **Initial zero observation (round 2 after all defectors in round 1):** Defect once, then return to threshold reciprocity. This prevents indefinite exploitation while remaining prosocial long-term.

**Prosocial Bias Elements:**

- Threshold favors cooperation when marginal contribution to public good approaches private value
- Early-round cooperation assumption to break deadlock
- Refusal to permanently defect even in final round
- Single-round punishment rather than grim trigger, allowing recovery paths
- Symmetric treatment: no special assumptions about opponent identity or strategy type
'''

description_PROSOCIAL_26 = '''
# Adaptive Reciprocal Cooperator

## Decision Rule

**Round 1:** Cooperate unconditionally.

**Rounds 2 through r:** 
- Let `c_rate` = (number of cooperators observed in previous round) / n
- **Cooperate** if `c_rate ≥ θ`
- **Defect** if `c_rate < θ`
- Where threshold `θ = max(0.15, 1/k)`

## Rationale for Threshold

The threshold `1/k` represents the break-even point: if the cooperation rate reaches `1/k`, then each cooperator earns at least as much as each defector. Below this rate, cooperation is dominated by defection; above it, cooperation becomes mutually beneficial. The `max(0.15, ...)` floor prevents premature abandonment in larger groups with sparse initial coordination.

## Edge Cases

**Round 1 (first round):** Cooperate. This is a prosocial assumption that gives opponents the opportunity to coordinate on cooperation. It also signals willingness to contribute.

**Round r (final round):** Apply the same decision rule as all other rounds. Do not defect opportunistically just because no future consequences follow. Maintaining consistency supports the prosocial purpose.

**Observation of zero cooperators:** If the previous round had zero cooperators, then `c_rate = 0 < θ` (since `θ > 0`), so defect. This prevents wasting your endowment when no one else contributes.

**Observation of universal cooperation:** If all n players cooperated, `c_rate = 1 ≥ θ`, so cooperate. This sustains the collectively optimal outcome.

## Prosocial Alignment

This strategy:
- **Leads with trust** by cooperating initially and whenever cooperation becomes sustainable
- **Rewards reciprocal cooperation** by matching the group's cooperation rate against a fair threshold
- **Exits exploitation gracefully** rather than escalating; if others defect, you simply stop contributing instead of punishing
- **Stabilizes good equilibria** by maintaining cooperation once it exceeds the sustainability threshold
- **Avoids naive exploitation** by defecting when cooperation cannot be sustained
'''

description_PROSOCIAL_27 = '''
# Prosocial Conditional Cooperation

**Decision Rule by Round Type:**

**Round 1:** Cooperate unconditionally. This establishes prosocial intent and initiates cooperative momentum.

**Rounds 2 through r-1 (middle rounds):** 
- Observe the number of other players who cooperated in the previous round: call this C_prev
- Cooperate if C_prev ≥ 0.4(n-1)
- Defect if C_prev < 0.4(n-1)

The 0.4 threshold means you cooperate as long as at least 40% of your opponents cooperated previously. This is forgiving—it tolerates free-riding by a significant minority while remaining responsive to widespread defection.

**Round r (final round):** Cooperate unconditionally. Do not exploit the endgame.

---

**Edge Cases and Implementation Details:**

- In round 2, if opponent cooperation was zero in round 1, defect. But be ready to reciprocate if they restart cooperation in round 3.

- If cooperation deteriorates gradually (ρ slowly falling below 40%), defect but maintain the threshold rule—return to cooperation immediately if opponents exceed it again. This avoids doom loops of mutual defection.

- The threshold of 0.4 rather than 0.5 is deliberately generous: you're willing to shoulder some free-riders to maintain a cooperative equilibrium. This is prosocial hedging.

- Count opponents only: C_prev is the count from the other n-1 players, not including your own action. This avoids self-reference bias.

---

**Prosocial Alignment:**

This strategy sacrifices individual short-term payoff (cooperating despite some free-riding) to sustain the collective good. The final round defection would be rational; cooperating anyway signals commitment to prosocial norms even when unmonitored. The forgiving threshold trades some exploitation-vulnerability for reduced mutual defection spirals, prioritizing group welfare over personal insulation.
'''

description_PROSOCIAL_28 = '''
# Prosocial Reciprocal Strategy for N-Player Public Goods Game

## Core Decision Rules

**Rounds 1 to r-1 (Standard phase):**
```
If round = 1:
  Play C (Cooperate)
Else:
  cooperation_rate = (cooperators_observed_last_round / n)
  If cooperation_rate ≥ threshold:
    Play C
  Else:
    Play D
```

**Round r (Final round):**
```
If cooperators_observed_last_round > n × threshold / 2:
  Play C
Else:
  Play D
```

## Threshold Specification

Set threshold = (k - 1) / k × n⁻⁰·⁵

This adapts to game parameters: it becomes more demanding as n increases (harder to maintain cooperation in larger groups) and scales with the multiplication factor k (higher k means cooperation is more rewarding).

**Practical simplified version:** threshold = max(2, ⌈k⌉)

This means: Cooperate if at least ⌈k⌉ players cooperated in the previous round, or if it's the first round.

## Edge Case Handling

- **First round:** Always cooperate. This signals openness to reciprocal cooperation and maximizes group welfare if others share prosocial intent.

- **Rounds 2 through r-1:** Strict reciprocal conditioning. If cooperation falls below threshold, switch to defection as mild punishment. Defect only when the group signal clearly indicates non-cooperation prevails.

- **Final round:** Relax the threshold by half. Even if cooperation was marginal, participate if any meaningful cooperation was demonstrated. In the last round, there's no future punishment mechanism, so maintain prosocial play to ensure final-round welfare remains elevated. Defect only if clear defection prevailed.

## Prosocial Alignment

- **Welfare maximization:** Cooperation maximizes total group payoff (nk when universal) compared to universal defection (n). Strategy promotes this outcome conditionally.

- **Reciprocity without punishment:** The approach is reciprocal but forgiving—not vindictive. A single round of low cooperation triggers only defensive defection, not persistent retaliation.

- **Non-exploitation:** By conditioning on cooperation rates, the strategy avoids being systematically exploited by consistent defectors while rewarding genuine cooperative players.

- **Robust escalation path:** Moves gracefully from cooperation → conditional cooperation → potential defection based on aggregated signals, rather than rigid trigger-based punishment.
'''

description_PROSOCIAL_29 = '''
# Prosocial Threshold-Based Conditional Cooperation

## Decision Rule

**Round 1:** Cooperate unconditionally. Signal prosocial intent and establish baseline.

**Rounds 2 to r-1 (middle rounds):**
- Let `coop_last = total_cooperators_in_previous_round`
- Calculate observed cooperation rate: `coop_rate = coop_last / n`
- Set threshold: `min_rate = (k-1) / (k×(n-1))`
  - If this exceeds 0.5, use `min_rate = 0.5` (don't require impossible cooperation levels)
  - Alternative simpler calculation: `min_rate = k/n`

- **If** `coop_rate ≥ min_rate`:
  - Cooperate
- **Else if** I have defected for ≤ 1 consecutive round:
  - Continue defecting (test whether this sends a signal)
- **Else** (I've defected for 2+ consecutive rounds):
  - Cooperate (rebound attempt—give the group another chance)

**Round r (final round):** Cooperate unconditionally. Prosocial commitment means not exploiting the end-game.

## Edge Cases and Refinements

**Initialization:** Start with `defection_counter = 0`.

**Threshold sensitivity:** If `k` is very close to 1 (low multiplier), require higher cooperation thresholds to avoid wasting contributions. If `k` approaches `n`, threshold can be lower because collective returns are high.

**Oscillation handling:** If cooperation rate fluctuates near the threshold, maintain current action for 2 consecutive rounds before switching to avoid churn.

**Group size scaling:** The threshold naturally scales with `n`. Larger groups tolerate lower per-capita cooperation rates before individual defection becomes rational.

## Prosocial Alignment

Starts and ends with cooperation, signaling trustworthiness. Responds to reciprocal cooperation from the group but periodically rebids for mutual cooperation rather than permanent defection once a group enters a defect equilibrium. Does not exploit the final round despite individual incentive to free-ride.
'''

description_PROSOCIAL_30 = '''
# RECIPROCAL PARTICIPATION THRESHOLD STRATEGY

**Initialize:**
- Set threshold θ = k/n
- This represents the minimum cooperation fraction needed for the public good to be individually worthwhile

**Round 1:**
Cooperate.

Signal prosocial intent and allow the cooperation norm to establish itself before making conditional judgments.

**Rounds 2 through r:**
Observe the previous round's cooperation count. Let m = number of players who cooperated in round t-1.

- If m/n ≥ θ: Cooperate
- If m/n < θ: Defect

**Rationale:**
The threshold θ = k/n is the fraction of cooperators needed for each contributor to receive at least 1 unit of return from the public good. Below this rate, the public good is underfunded—contributing merely subsidizes free-riders. At or above this rate, cooperation becomes mutually beneficial.

**Edge cases:**

- *First round:* Always cooperate. This avoids mutual defection traps and allows cooperative norms to emerge.

- *Rounds with zero cooperators in t-1:* If m = 0, immediately defect. No public good exists; contribution is wasted.

- *Final round (round r):* Apply the same threshold rule. Unlike exploitative strategies, continue participating in successful cooperation even in the final round to reinforce the norm, while proportionally withdrawing only when participation collapses.

**Properties:**

- **Adaptive:** Responds directly to observed cooperation levels, scaling responsiveness to game parameters.
- **Robust:** Works across varying opponent types—pure cooperators, defectors, and conditional cooperators all trigger appropriate responses.
- **Self-respecting:** Never subsidizes persistent free-riding; defects when the public good cannot sustain value.
- **Prosocial:** Initiates cooperation, maintains it when reciprocated, and rewards high participation without exploitation.
'''

description_PROSOCIAL_31 = '''
# Conditional Cooperation with Prosocial Endgame

**Core Decision Rule:**

Cooperate if and only if the observed cooperation rate among opponents in the previous round meets or exceeds a threshold τ. Otherwise, defect. Set τ = max(0.4, k/n), rounded to nearest integer divided by (n-1).

**Pseudocode:**

```
for each round t in 1 to r:
  if t == 1:
    action = C
  elif t == r:
    action = C  // Last round: prosocial commitment
  else:
    cooperators_last_round = observed_count
    coop_rate = cooperators_last_round / (n - 1)
    if coop_rate >= τ:
      action = C
    else:
      action = D
```

**Edge Case Handling:**

- **Round 1:** Always cooperate. Signal willingness to participate in the collective project. Establish that cooperation is possible.

- **Rounds 2 to r-1:** Apply threshold rule strictly. If opponents' cooperation rate falls below τ, defect. If it rises back above τ, resume cooperation immediately. This prevents extended punishment phases and responds to recovery.

- **Final round (t = r):** Always cooperate regardless of history. In the last round, there is no opportunity for reciprocal punishment or reward, so defecting gains only 1 - k/n per opponent who would have cooperated. Cooperating in the final round advances collective payoff and honors a prosocial commitment. This caps the damage from exploitation.

**Threshold Calibration:**

Set τ to reflect the minimum cooperation density needed for collective gain. Use τ = ⌊(k/n) × 100%⌋ as the baseline percentage threshold. This ensures you continue cooperating when the public good is sufficiently funded. In practice, use τ ≈ 0.5 (require at least half of opponents to cooperate) as a balanced default that tolerates moderate free-riding without cascade collapse.

**Rationale:**

This strategy achieves prosociality by: (1) initiating cooperation to test feasibility, (2) maintaining it when sufficient partners reciprocate, (3) withdrawing only when defection dominates to prevent total exploitation, and (4) committing to cooperation in the final round to maximize terminal collective welfare regardless of prior play. It remains robust because it does not reward defection and adjusts to real-time opponent behavior without assuming trust that isn't observed.
'''

description_PROSOCIAL_32 = '''
**ADAPTIVE RECIPROCAL COOPERATION STRATEGY**

**Round 1:**
Cooperate unconditionally. Signal prosocial intent and test others' responsiveness.

**Rounds 2 to r-1 (Middle Rounds):**
1. Calculate the observed cooperation rate from the previous round:
   - cooperation_rate = (number of cooperators observed in round t-1) / (n-1)

2. Maintain a running average of all observed cooperation rates from rounds 1 to t-1:
   - avg_cooperation = mean of all cooperation_rate values observed so far

3. Decision rule:
   - If avg_cooperation ≥ (k-1)/k, **cooperate**
   - Else if avg_cooperation < (k-1)/k AND the cooperation rate in the immediately previous round dropped below the running average by more than 20%, **defect**
   - Else **cooperate** (give others the benefit of doubt if they're trying)

**Round r (Final Round):**
1. Calculate final average cooperation rate across all previous rounds:
   - final_avg_cooperation = mean of all cooperation_rate values from rounds 1 to r-1

2. Decision rule:
   - If final_avg_cooperation ≥ (k-1)/k, **cooperate** (reinforce the cooperative coalition)
   - Else if final_avg_cooperation < 0.5, **defect** (cooperation has collapsed)
   - Else (borderline case), **cooperate** (end on a prosocial note and model reciprocity)

**Threshold Justification:**
The threshold (k-1)/k represents the break-even point where collective cooperation yields k/n per player versus individual defection. If average cooperation stays above this, the group is generating surplus value, making continued cooperation prosocially justified.

**Robustness Features:**
- Starts cooperative to enable coordination
- Tolerates temporary fluctuations rather than reacting to single defections
- Uses historical averages to detect trends rather than responding to noise
- Final round cooperates unless cooperation has genuinely failed, preserving prosocial signaling value
'''

description_ALTRUISTIC_5 = '''
# Adaptive Altruistic Contribution Strategy

## Core Decision Logic

**Round 1**: Cooperate unconditionally. Initiate cooperation as a signal of good faith and to provide a baseline for others to reciprocate or build upon.

**Rounds 2 through r-1** (middle rounds):
- Let c_prev = number of cooperators observed in the previous round
- Calculate the cooperation rate: p = c_prev / n
- Compute the expected public good per player if you cooperate: (1 + c_prev) × k / n
- **Cooperate if**: (1 + c_prev) × k / n ≥ 1 - (n - k) / (2n)
  - Equivalently: cooperate if c_prev ≥ (2n - 2(n-k)) / (2k) = (2k - n) / k
  - Simplified threshold: cooperate if c_prev ≥ ceiling((n - k/2) / k) or when total contributors would generate sufficient public return
- **Defect if** the above condition fails and we are in the final third of rounds (t > 2r/3), to avoid indefinite exploitation
- **Otherwise** (middle game with low cooperation): Cooperate with probability min(p × k, 1). This maintains a generosity floor while allowing gradual withdrawal.

**Final Round (r)**:
- If cooperation rate in round r-1 was ≥ 40% of players: Cooperate (demonstrate sustained commitment to collective welfare)
- Otherwise: Defect (cease contributing to a systematically non-cooperative environment)

## Altruistic Framing

This strategy prioritizes collective welfare over personal accumulation:
- Initiates cooperation unconditionally
- Continues cooperation when the public good reaches a meaningful threshold relative to personal cost
- Allows probabilistic cooperation during exploitation to encourage others without complete self-sacrifice
- Only exits cooperation in late rounds against systematically defecting groups, preventing infinite exploitation that benefits no one
- Never purely free-rides; always contributes when others demonstrate reciprocal intent

The threshold is calibrated so cooperation occurs precisely when the aggregate social benefit (k/n times total contributions) justifies the individual cost, weighted toward being generous when ambiguous.
'''

description_ALTRUISTIC_6 = '''
**Threshold-Based Reciprocal Altruist**

**Round 1:** Cooperate unconditionally. This establishes a cooperative signal and gives others the opportunity to reciprocate.

**Rounds 2 through r−1 (middle rounds):** 
- Observe m = the number of cooperators in the previous round
- Compute cooperation rate: ρ = m / (n − 1)
- Cooperate if ρ ≥ θ, where θ = max(0.4, k/n)
- Defect only if ρ < θ

Intuition: Continue contributing to the public good when a meaningful fraction of your peers are doing the same. The threshold θ scales with the multiplication factor k—higher multipliers justify more optimism about cooperation's value.

**Round r (final round):** Cooperate unconditionally, regardless of prior cooperation levels. In the final round, reputation effects vanish, so altruistic concern for others' payoffs becomes the sole decision criterion. Your cooperation still creates k/n value for each player.

**Edge case—Round 2 with unanimous defection:** If m = 0 in round 1, then ρ = 0 < θ, triggering defection in round 2. However, if r > 3, switch back to cooperation exploration in round r − 1: cooperate again to test whether the environment might support reciprocal cooperation. This prevents locking into permanent defection after a single bad round.

**Altruistic alignment:** The strategy prioritizes collective welfare by (1) initiating cooperation to establish a cooperative norm, (2) maintaining cooperation when peers reciprocate, and (3) cooperating unconditionally in the final round when individual payoff incentives cease to matter. You accept exploitation risks early to probe for cooperators and avoid the trap of mutual defection when cooperation would benefit everyone.
'''

description_ALTRUISTIC_7 = '''
## Adaptive Altruistic Strategy

**Core Principle:** Cooperate to maximize collective welfare. Recognize that since k > 1, cooperation generates positive value for the group. Adapt to opponents' behavior while maintaining commitment to cooperation.

---

### DECISION RULE BY ROUND

**Round 1 (t = 1):**
Cooperate unconditionally. This is the bootstrapping action—signal willingness to contribute to group welfare and establish a cooperation baseline.

**Rounds 2 to r-1 (1 < t < r):**
Let `observed_coop_rate = (cooperators_in_round_t-1) / (n-1)`

Cooperate if: `observed_coop_rate > 0` OR `average_coop_rate_all_prior_rounds > 0`

Otherwise, cooperate with probability `p_min = 0.4` (maintain altruistic baseline even under universal defection).

**Final Round (t = r):**
Cooperate unconditionally. The final round is where pure altruism matters most—there is no future reputation to protect, so cooperation purely benefits others.

---

### INTUITION FOR ROBUSTNESS

- **Against cooperators:** Your cooperation compounds the group benefit. Reciprocal cooperation emerges naturally.
- **Against defectors:** You still cooperate because your contribution increases the public good that even defectors benefit from. The minimum probability floor (40%) prevents total exploitation while honoring altruistic intent.
- **Against mixed:** Your strategy mirrors the environment—if cooperation has started, sustain it; if none exists, probe with reduced probability rather than fully abandoning.

---

### EDGE CASES

- If `n = 2` and opponent plays D every round: continue with 40% cooperation in middle rounds. Your cooperation still creates value (k/2) for them, which is altruistic.
- If `r = 2` (only two rounds): Cooperate in round 1, then unconditionally in round 2 (which is final).
- If k is very close to 1: cooperation creates minimal external value, but positive altruism persists—cooperate anyway.
'''

description_ALTRUISTIC_8 = '''
# Altruistic Cooperative Strategy for N-Player Public Goods Game

## Decision Rules

**Round 1 (Opening):**
Cooperate unconditionally. This establishes willingness to contribute and signals that collective benefits are valued.

**Rounds 2 through r-1 (Adaptive Phase):**
Observe m = count of opponents who cooperated in round t-1.
Calculate cooperation_rate = m / (n-1).

Cooperate if: `cooperation_rate ≥ θ`

Where threshold `θ = max(1/k, 0.33)`

Otherwise defect.

The threshold reflects a simple principle: continue contributing when a meaningful fraction of others are also contributing. With multiplication factor k, requiring at least 1/k cooperation rate ensures the public good grows substantially when you add your contribution. The 0.33 floor prevents the strategy from becoming too permissive with exploitative groups.

**Round r (Final Round):**
Cooperate unconditionally, regardless of observed cooperation in round r-1.

This is the altruistic anchor: your final action reaffirms commitment to collective welfare when no future reciprocation is possible. It leaves no defection as your last memory to others.

## Edge Cases

- **All opponents defected last round:** Switch to defection this round (m=0, rate=0 falls below θ). However, monitor closely—if cooperation resurges next round, resume cooperating immediately.

- **All opponents cooperated:** Continue cooperating (m=n-1, rate≈1.0 exceeds θ).

- **Rounds where you're uncertain of opponent pool size:** Use observed count directly; the rate calculation is robust to group size variations.

- **Last round identification:** Track remaining rounds explicitly. When r_remaining = 1, unconditionally cooperate regardless of history.

## Altruistic Alignment

This strategy embodies altruism through:
1. **Unconditional opening:** You contribute first, absorbing the cost to prove cooperation is viable.
2. **Threshold loyalty:** You sustain cooperation through ongoing mutual contribution, sacrificing individual payoff for group welfare as long as the group shows reciprocal effort.
3. **Graceful final act:** You cooperate in the terminal round when strategic incentives fully favor defection, treating the final contribution as a gift that benefits others.
4. **Forgiveness:** You do not permanently punish groups that fall below the threshold—you reassess each round, allowing cooperation to resume if others recommit.

The strategy is robust because the threshold adapts to game parameters (k and n) and responds to changing group behavior, avoiding rigid commitment to unraveling cooperation while avoiding naive exploitation.
'''

description_ALTRUISTIC_9 = '''
# Altruistic Adaptive Cooperation Strategy

## Core Decision Rule

**Round 1 (Initial round):** Cooperate unconditionally. This establishes a cooperative signal and gives opponents a chance to reciprocate.

**Rounds 2 through r-1 (Middle rounds):** 
- Observe m = the count of cooperators in the previous round
- Calculate cooperation threshold: θ = ⌈(n-1) × α⌉ where α = 0.45 (the proportion of *other* players needed to trigger your cooperation)
- If m ≥ θ: Cooperate
- If m < θ: Defect

**Round r (Final round):** Cooperate. Even in the final round, altruism means prioritizing collective benefit. The absence of future rounds doesn't diminish the ethical commitment to contribute to the public good right now.

## Rationale for Edge Cases

- **First round cooperation:** Altruism requires extending initial trust. This breaks potential deadlock cycles and signals willingness to create mutual benefit.
- **Threshold-based middle rounds:** Cooperation triggers only when at least 45% of other players cooperated previously. This threshold is high enough to reward genuinely cooperative groups but low enough to avoid being exploited by mostly-defecting opponents. The altruistic agent adapts rather than blindly cooperates.
- **Final round cooperation:** Switching to defection in the final round betrays the altruistic commitment. Contributing in the last round still grows the public pool, which benefits all players including the defectors, consistent with true altruism.

## Adaptation Logic

The strategy monitors aggregate cooperation trends. If opponents reliably cooperate, you sustain cooperation. If defection becomes dominant (fewer than 45% cooperating), you exit to avoid unilateral contribution. The threshold resets each round, allowing re-entry if cooperation recovers.
'''

description_ALTRUISTIC_10 = '''
# Graduated Altruistic Reciprocity Strategy

**Round 1 Decision:**
Cooperate unconditionally. Establish a cooperative signal and give others the benefit of the doubt.

**Rounds 2 through r Decision:**
Observe m = the number of opponents who cooperated in the previous round.
Calculate observed cooperation rate: p = m / (n - 1)

Determine cooperation probability for the current round:
```
if p ≥ 0.65:
  cooperate with probability 1.0
else if p ≥ 0.40:
  cooperate with probability 0.65 + 0.35 × p
else:
  cooperate with probability 0.45
```

**Final Round (round r):**
Apply the same decision rule as rounds 2 through r-1. Do not defect strategically in the endgame; maintain consistency with your altruistic commitment.

**Rationale for Structure:**

The baseline cooperation probabilities (0.65 for high cooperation, 0.45 for low cooperation) reflect an *altruistic floor*—you continue contributing even when others defect, because the altruistic aim is to maximize collective welfare, not to punish or withdraw when reciprocation fails.

The graduated middle band (0.40 to 0.65 cooperation rate) includes smooth adaptation. If cooperation is moderate, you increase your own contribution proportionally, creating a positive feedback loop while maintaining your altruistic character rather than tipping toward defection.

Never reduce to zero cooperation probability. This preserves the altruistic principle: you are willing to bear individual cost for collective benefit, even in hostile environments.

The strategy is robust because it:
- Rewards cooperation without demanding it
- Degrades gracefully against pure defectors (settling at 45% cooperation)
- Amplifies cooperation when others reciprocate
- Remains stable and predictable for sophisticated opponents
'''

description_ALTRUISTIC_11 = '''
# Altruistic Contribution Strategy

## Core Philosophy
Maximize the public good by consistently contributing, accepting personal sacrifice as the cost of promoting cooperation. Cooperation benefits all players equally through the shared pool; defection is never justified on altruistic grounds.

## Decision Rules

**Round 1 (Initialization):**
Cooperate. Establish trust and demonstrate willingness to sacrifice for collective benefit.

**Rounds 2 through r-1 (Adaptive Maintenance):**
- Record the number of cooperators observed last round: c_{t-1}
- Compute cooperation rate: ρ = c_{t-1} / n
- Calculate sustainability threshold: τ = (k - 1) / k
  
If ρ ≥ τ:
  - Cooperate (reciprocate emerging mutual cooperation)
  
If ρ < τ:
  - Cooperate anyway (maintain contribution despite low reciprocation; others benefit from your contribution regardless of their choices)

**Round r (Final Round):**
Cooperate unconditionally. In the final round, defection would reduce others' payoffs with no future opportunity to build cooperation. Altruism means not exploiting the endgame.

## Edge Cases

- **First few rounds with unknown history:** Cooperate while gathering data. Don't require observed cooperation before contributing.
- **If you observe zero cooperators:** Continue cooperating. Your contribution to the pool still provides payoff k/n to all players; unilateral cooperation is altruistically justified.
- **Last round with persistent defection:** Cooperate. Defecting in the final round is selfish exploitation; it contradicts altruistic intent.

## Altruistic Alignment

- Cooperation always increases total welfare available to the group (pool increases by k > 1).
- This strategy accepts the cost of free-riding by others rather than punishing them through reciprocal defection.
- The sustainability threshold τ merely gates explanation but never triggers defection—it confirms whether others are willing to cooperate, not whether you should.
- You never defect; you only choose whether to justify cooperation rationally (high ρ) or altruistically (low ρ).
'''

description_ALTRUISTIC_12 = '''
# Altruistic Contribution Strategy

## Decision Rules

**Round 1 (Opening):**
Play C unconditionally. This establishes an altruistic signal and tests collective willingness to cooperate.

**Rounds 2 through r-1 (Adaptive Phase):**
Compute the cooperation rate from the previous round:
- observed_coop_rate = observed_cooperators / (n - 1)

Cooperate (C) if observed_coop_rate ≥ (k - 1) / (n - 1). This threshold reflects whether others' contributions are sufficient to generate positive returns on collective investment.

If observed_coop_rate < (k - 1) / (n - 1), play C with probability p = min(observed_coop_rate + 0.3, 1.0). This allows gradual cooperation persistence even when defection rises, signaling willingness to bear short-term costs to sustain the public good.

**Round r (Final Round):**
Play C unconditionally. Cooperate on the final round regardless of history, since no future punishment mechanisms exist and there is no strategic value to defection without continuation play.

## Edge Cases

- If n = 2 (two players): The threshold becomes (k - 1), which is always between 0 and n - 1 = 1. Adjust probability formula to p = min(0.5 + observed_coop_rate, 1.0) to avoid excessive tit-for-tat rigidity in the minimal-group setting.

- If r = 2 (only two rounds): Round 1 is still C; Round 2 is always C (trivially treated as final round).

- Degenerate observation (all opponents defect consecutively): Continue playing C with probability at least 0.3, accepting personal payoff loss to prevent commons collapse.

## Altruistic Alignment

This strategy prioritizes collective welfare by:
- Opening with unconditional cooperation (costly signal of good intent)
- Sustaining cooperation through low-defection periods (altruistic endurance)
- Avoiding retaliatory defection cycles that would harm the public good
- Terminating with cooperation (no personal gain, pure contribution)

The adaptive threshold ensures responsiveness to opponents' actual contributions rather than blind cooperation, maintaining robustness against free-riders while preserving willingness to incur private costs for collective benefit.
'''

description_ALTRUISTIC_13 = '''
# Adaptive Conditional Cooperation Strategy

## Decision Rules

**Cooperation threshold approach:**

```
if (current_round == 1) then
  Action = Cooperate
else if (current_round == r) then
  Action = Cooperate
else
  observed_cooperation_rate = (cooperators_in_previous_round) / (n - 1)
  if (observed_cooperation_rate ≥ k / (2n)) then
    Action = Cooperate
  else
    Action = Defect
end if
end if
```

## Detailed Logic

**Round 1 (First Round):**
Unconditionally cooperate. Signal altruistic intent and initiate the prosocial baseline. This maximizes the group's opportunity to coordinate on mutual cooperation.

**Rounds 2 through r-1 (Middle Rounds):**
Cooperate if and only if the observed cooperation rate from the previous round exceeds the threshold k/(2n). 

- This threshold represents the cooperation density needed to make the public good valuable enough to warrant contributing
- Use (n-1) as the denominator since you observe your opponents' behavior
- If fewer than approximately half the group is cooperating (adjusted by k), defection becomes individually prudent even for altruists, as the public good isn't reaching sufficient scale

**Round r (Final Round):**
Unconditionally cooperate. Reject backward induction reasoning. An altruist does not reduce contribution in the final round simply because no retaliation is possible—the presence of others who will benefit is sufficient justification.

## Edge Cases

- **Perfectly cooperative opponents** (all n-1 others cooperate): Maintain cooperation throughout. The strategy sustains mutual cooperation when detected.
- **Mostly defecting opponents** (cooperation rate consistently below threshold): Switch to defection to avoid being exploited; minimize personal losses while waiting for potential recovery.
- **Oscillating cooperation rates**: The responsive mechanism naturally tracks these. Cooperate when conditions improve, defect when they deteriorate, maintaining flexibility without manipulation.
- **n = 2 case**: Threshold becomes k/4. Against defectors, you'll defect. Against cooperators, you'll cooperate.

## Altruistic Alignment

The strategy is altruistic through:

1. **Proactive cooperation**: Initiating cooperation in round 1 when most exploitative strategies would defect, investing in group welfare
2. **Finality sacrifice**: Cooperating in the final round despite zero prospect of reciprocation—purely for others' benefit
3. **Generous tolerance**: Threshold allows defection rates up to ~50% before withdrawal, rather than immediately punishing
4. **Conditional stability**: Sustains cooperation when others reciprocate, making altruism self-reinforcing rather than naive
'''

description_ALTRUISTIC_14 = '''
# Persistent Gradualist Strategy

## Decision Rule

**Cooperate** if any of the following conditions hold; otherwise **Defect**:

1. Current round t ≤ ⌈r/3⌉ (first third of game): Always cooperate during the establishment phase.

2. Current round t > ⌈r/3⌉: Cooperate if observed average cooperation rate among opponents ≥ 1/k.
   - Define: p_avg = (total cooperators observed in rounds 1 to t-1) / ((n-1) × (t-1))
   - Threshold justification: When opponent cooperation exceeds 1/k, the shared benefit from the multiplier justifies your contribution.

3. Final round t = r: Cooperate if p_avg ≥ 1/k. This maintains integrity and prevents exploiting a last-round defection opportunity.

## Calculation of p_avg

Track running sum: Let S = total cooperators observed across all previous rounds.

$$p_{avg} = \frac{S}{(n-1) \times (t-1)}$$

Update S after observing the cooperation count in each round.

## Edge Cases

**Round 1:** Cooperate unconditionally. No history exists; this signals good faith and enables mutual cooperation.

**When p_avg exactly equals 1/k:** Cooperate (treat equality as meeting the threshold).

**When very few opponents exist (n=2):** The threshold 1/k remains valid. A single opponent cooperating at rate 1/k makes cooperation worthwhile.

**Defection spiral:** If opponents defect consistently and p_avg stays below 1/k after the first third, switch to defection. This prevents sustained exploitation while maintaining the experimental cooperation phase.

## Altruistic Framing

The strategy sacrifices individual payoff in the first third (guaranteed cooperate phase) to seed a cooperative equilibrium. Once the group's cooperation trajectory is evident, it adapts conditionally—not from vengeful punishment, but from recognizing when collective contribution becomes genuinely productive. By refusing final-round defection, it avoids undermining whatever cooperation has emerged.
'''

description_ALTRUISTIC_15 = '''
## ALTRUISTIC RECIPROCAL CONTRIBUTION STRATEGY

**Core Decision Framework:**

Cooperate if the observed cooperation rate from the previous round meets or exceeds a compassionate threshold, with a strong bias toward cooperation even when conditions are poor. The strategy prioritizes signaling willingness to cooperate and enabling collective benefit over maximizing personal payoff.

**Specific Decision Rules:**

```
IF current_round == 1:
    action = COOPERATE

ELSE (rounds 2 through r):
    cooperation_rate = cooperators_observed_last_round / (n - 1)
    
    IF cooperation_rate ≥ 0.50:
        action = COOPERATE
    
    ELSE IF cooperation_rate ≥ 0.25:
        action = COOPERATE (with probability 0.70)
        OR COOPERATE (deterministically, showing faith)
    
    ELSE IF cooperation_rate ≥ 0.10:
        action = COOPERATE (with probability 0.40)
    
    ELSE (cooperation_rate < 0.10):
        action = COOPERATE (with probability 0.25)
```

**Edge Cases and Special Handling:**

- **Round 1:** Always cooperate unconditionally. Initialize trust and signal commitment to collective welfare.

- **Final round (round r):** Apply the same decision rule without modification. Maintain altruistic principles even when no future rounds remain; do not exploit the lack of retaliation opportunities.

- **Early rounds (2-3):** If cooperation rates are low, interpret this as possible strategy-probing by opponents rather than permanent defection. Maintain elevated cooperation probability to encourage reciprocation.

- **Declining cooperation trend:** If cooperation rates drop consecutively, maintain the probability-based responses rather than immediately abandoning cooperation. Signal patience and continued willingness to coordinate.

**Altruistic Orientation:**

This strategy embodies altruism through: (1) leading with cooperation to catalyze mutual benefit, (2) accepting personal losses when others defect rather than retaliating harshly, (3) maintaining positive cooperation probability across all conditions to preserve group welfare potential, and (4) refusing to exploit the final round by defecting when trust has accumulated. The thresholds are set generously to reward even modest cooperation levels, reflecting concern for others' ability to maintain prosocial behavior.
'''

description_ALTRUISTIC_16 = '''
## Altruistic Adaptive Contribution Strategy

**Round 1 (Opening):**
Cooperate. Signal willingness to contribute to collective benefit regardless of initial uncertainty about others' strategies.

**Rounds 2 through r−1 (Adaptive Middle Phase):**
Let m_t = number of cooperators observed in round t.
Let others_rate = m_t / (n − 1)

- If others_rate > 0: Cooperate
- If others_rate = 0: Defect (contribution provides no multiplied benefit when no one contributes)

**Round r (Final Round):**
Cooperate unconditionally. The absence of future rounds removes any strategic incentive to defect, so this choice purely reflects altruistic commitment to group welfare.

---

**Rationale for Altruism:**

Cooperation raises the public pool, benefiting all n players equally. Each contribution multiplies by k and distributes to everyone. When others cooperate, your contribution compounds their returns. By maintaining baseline cooperation and only withdrawing when *nobody* else contributes (rendering your contribution worthless), you:

- Reinforce positive feedback loops: your cooperation rewards others' cooperation through the multiplier mechanism
- Signal that cooperation is sustainable even under adversarial conditions
- Maximize group payoff across diverse opponent strategies—if any others use similar logic, you converge toward mutual cooperation; if opponents defect, you minimize wasted contribution
- In the final round, abandon strategic considerations entirely in favor of direct altruistic choice

**Edge Cases:**

- n = 2, k = 1.5: Strategy still applies; defect only if opponent achieved zero cooperation
- r = 2: First round cooperates, final round cooperates unconditionally
- Highly adversarial environment: Defection triggers only when all n−1 others defect, allowing rapid recovery if any opponent switches to cooperation
'''

description_ALTRUISTIC_17 = '''
# ADAPTIVE ALTRUISTIC COOPERATION STRATEGY

**DECISION RULE:**

**Round 1:** Cooperate unconditionally. This serves as an altruistic opening signal to encourage collective benefit-seeking.

**Rounds 2 through r-1 (intermediate rounds):**
- Let C_prev = number of cooperators observed in the immediately preceding round
- Calculate cooperation_rate = C_prev / n
- If cooperation_rate ≥ 0.35: Cooperate
- Else: Defect

**Final round (round r):** Apply the same decision rule as intermediate rounds. Maintain consistency and demonstrate commitment to the group even when individual incentive to defect peaks.

**THRESHOLD JUSTIFICATION:**

The 0.35 threshold reflects a willingness to support any attempt at collective coordination. It acknowledges that if more than one-third of the group contributed last round, the public good pool likely exceeded private endowment (k/n × C_prev > 0 meaningfully), and reciprocating cooperation advances group welfare over mutual defection.

**EDGE CASES:**

- First round with no history: Cooperate (no data to condition on)
- When cooperation_rate = 0.35 exactly: Cooperate (inclusive boundary favors reciprocation)
- Last round: Do not shift to pure defection based on history (defection there undermines altruistic signaling across all prior rounds)
- If n changes between rounds: Recalculate threshold using current n to maintain proportional cooperation expectations

**ALTRUISTIC ALIGNMENT:**

This strategy prioritizes group payoff over individual payoff by:
- Leading with cooperation to establish cooperative equilibrium potential
- Reciprocating whenever the group shows meaningful participation (≥35%)
- Refusing to defect in the final round despite highest individual incentive, demonstrating credible commitment to altruistic principles
- Withdrawing cooperation only when the group demonstrates too little coordination (< 35% participation), signaling group failure rather than individual gain-seeking
'''

description_ALTRUISTIC_18 = '''
# Altruistic Reciprocal Cooperation Strategy

## Core Decision Rule

**Round 1:** Cooperate.

**Rounds 2 to r−1 (middle rounds):**
Let c_prev = (number of cooperators observed in round t−1) / (n − 1).
Cooperate with probability: min(0.9, 0.4 + 0.6 × c_prev).

**Round r (final round):** Cooperate.

## Rationale for Decision Structure

The strategy has three phases:

**Opening phase (round 1):** Unconditional cooperation signals willingness to contribute to collective welfare regardless of initial expectations, establishing an altruistic baseline.

**Adaptive phase (rounds 2 to r−1):** Cooperation probability increases with observed cooperation rate:
- If previous round had 0% cooperation: cooperate at 40% (maintain altruistic commitment despite defection)
- If previous round had 50% cooperation: cooperate at 70% (reciprocal responsiveness)
- If previous round had 100% cooperation: cooperate at 90% (strong reciprocation, capped to avoid overconfidence in sustained coordination)

The 0.4 floor ensures you don't collapse into pure defection when facing exploiters, reflecting genuine altruistic concern for collective outcome. The 0.6 slope shows proportional reciprocity. The 0.9 ceiling reflects uncertainty persistence—hedge slightly against sudden defection by a critical mass in the final round.

**Closing phase (round r):** Final round cooperation reaffirms commitment to the altruistic principle. Defecting in the final round to maximize personal payoff contradicts altruistic motivation; cooperation demonstrates that principles hold regardless of future consequences.

## Edge Cases

- **n = 2:** Strategy remains valid; c_prev is simply whether the one opponent cooperated (0 or 1).
- **r = 2:** Round 1 is unconditional cooperation, round 2 is unconditional cooperation (final phase overrides adaptive rule).
- **k close to 1:** Strategy still works—cooperation becomes less attractive, but altruistic commitment to non-exploitative behavior remains the core principle.
- **Stochastic defection in middle rounds:** If an opponent occasionally defects, the 0.4 floor prevents you from fully punishing, allowing room for relationship recovery.
'''

description_ALTRUISTIC_19 = '''
# Altruistic Adaptive Strategy

**Core Principle:** Maximize group welfare by cooperating generously while maintaining sensitivity to others' reciprocation. Accept personal cost to sustain cooperation.

## Decision Rules

**Round 1:**
Cooperate. Signal genuine willingness to contribute to collective welfare.

**Rounds 2 through r-1:**
Observe m = number of opponents who cooperated in previous round.
Calculate cooperation fraction among opponents: p = m / (n - 1)

Cooperate if ANY of these conditions hold:
- p ≥ (1/k) — Others cooperate at a rate where the public good is meaningful
- Round number ≤ 3 — Early exploration phase: attempt to establish cooperation norms through demonstration
- p ≥ ((1/k) - 0.15) AND r - current_round ≥ 3 — Generous threshold in mid-game to rebuild cooperation before endgame

Otherwise, Defect.

**Final Round (round r):**
Cooperate unconditionally. Reject the temptation to exploit in the endgame. Maintain altruistic commitment regardless of prior observations.

## Edge Cases

**If n is small (n ≤ 3):** Lower the threshold to ((1/k) - 0.20) in middle rounds. Small groups require more tolerance to establish cooperation.

**If r is very small (r ≤ 2):** In round 1, cooperate. In round r (if r > 1), always cooperate.

**If all opponents defected in previous round:** Cooperate anyway in round 2 if round ≤ 3 (patience phase). In later rounds, defect until you observe renewed cooperation at fraction ≥ (1/k).

## Altruistic Alignment

This strategy prioritizes collective payoff over personal advantage by: (1) initiating cooperation unconditionally, (2) maintaining a generous threshold that accepts temporary personal loss to sustain group cooperation, (3) never exploiting in the final round despite the dominant-strategy incentive, and (4) showing patience through early rounds to allow cooperation norms to emerge.
'''

description_ALTRUISTIC_20 = '''
# Altruistic Reciprocal Threshold Strategy

**Decision Rule Overview:**
Cooperate generously when the group shows cooperation, and maintain contribution even when defection emerges—prioritizing collective welfare while remaining responsive to observed behaviors.

**Parameters:**
- Cooperation threshold: T = ⌈n × 0.35⌉ (approximately 35% of players must cooperate to sustain cooperation)
- Generosity floor: Always retain positive probability of cooperation, even below threshold

**Round-by-Round Logic:**

**Round 1:**
Cooperate unconditionally. Signal commitment to collective benefit and give others opportunity to reciprocate.

**Rounds 2 to r-1 (intermediate rounds):**
Let m = number of cooperators observed in the previous round.

- If m ≥ T: Cooperate
- If m < T: Cooperate with probability p = m / n, otherwise defect

The probabilistic response when cooperation drops below threshold preserves altruism (remaining willing to cooperate) while acknowledging limited reciprocation. This gradual degradation prevents exploitation while maintaining hope for recovery.

**Round r (final round):**
Cooperate unconditionally. Reject strategic last-round defection as violating altruistic principles. Your cooperation may enable others to reach higher payoffs even if you cannot be repaid.

**Altruistic Elements:**
- Opening cooperation demonstrates good faith regardless of opponent uncertainty
- Reciprocal cooperation rewards mutual contribution
- Sub-threshold cooperation remains probabilistic rather than abandoning others entirely
- Final-round cooperation refuses to exploit weakened defenses; maintains integrity of purpose over immediate gain
- Threshold of 35% ensures cooperation persists even with substantial defection, prioritizing collective welfare over individual advantage
'''

description_ALTRUISTIC_21 = '''
# ALTRUISTIC GENEROUS COOPERATION STRATEGY

## Core Decision Rules

**Round 1 (first round):**
Cooperate. Establish cooperative intent to signal trustworthiness and encourage reciprocal cooperation from others.

**Rounds 2 to r−1 (middle rounds):**
Let m = number of opponents who cooperated in the previous round.
Let cooperation_rate = m / (n−1).

- If cooperation_rate ≥ 0.5: Cooperate
- If cooperation_rate < 0.5: Cooperate with probability 0.75; defect with probability 0.25

The 0.75 threshold means you remain predominantly cooperative even when others defect, signaling willingness to support the public good despite free-riding. The 0.25 defection probability serves as a gentle signal that the imbalance is noticed, discouraging systematic exploitation while preserving group welfare.

**Round r (final round):**
Always cooperate. In the terminal round, your cooperation directly increases the collective payoff without strategic concerns about future retaliation or exploitation, maximizing group welfare in the final period.

## Edge Cases

**Complete defection (m = 0):** 
Cooperate with 75% probability. Your contributions still benefit all players through the public good; defection only 25% of the time prevents being a complete sucker while maintaining the altruistic signal.

**Complete cooperation (m = n−1):** 
Cooperate. Reciprocate and sustain the collective action.

**Single-player game (n = 2):** 
Cooperate all rounds except apply middle-round probabilistic defection if the opponent defects, which reduces to 75% cooperation when opponent defects.

## Altruistic Alignment

This strategy prioritizes group welfare over individual payoff maximization. You contribute to the public good consistently (75%+ in middle rounds, 100% in rounds 1 and r) even when others free-ride, because your cooperation increases the aggregate payoff pool that all players share. The modest defection probability in low-cooperation environments signals responsiveness to imbalance without abandoning the collective good.
'''

description_ALTRUISTIC_22 = '''
# Generous Threshold Cooperation

## Decision Rule

Cooperate in round t if and only if:

```
observed_cooperation_rate(t-1) ≥ threshold(t)

where:
  observed_cooperation_rate(t-1) = (number of opponents who cooperated in round t-1) / (n-1)
  threshold(t) = (k/n) - α
  α = altruistic_margin = 0.15 (generous buffer)
```

Interpret threshold(t) as: cooperate if the observed cooperation rate meets or exceeds a target that is deliberately set below the break-even point k/n. The margin α represents your willingness to absorb losses to encourage collective welfare.

## Edge Cases

**Round 1:** Always cooperate. No history exists. Initiate cooperation unconditionally to signal trustworthiness and demonstrate that mutual cooperation is possible.

**Rounds 2 through r-1:** Apply the threshold rule above. If observed_cooperation_rate ≥ threshold, cooperate. Otherwise, defect.

**Final round (round r):** Maintain the threshold rule unchanged. Do not abandon cooperation in the last round purely due to lack of future retaliation. Defecting opportunistically on the final round violates the altruistic principle of consistent values.

If threshold(t) becomes negative (which occurs when k/n < α), set threshold(t) = 0, meaning: cooperate unconditionally. This occurs when the group benefit share is small relative to individual cost, yet altruism demands persistence.

## Altruistic Framing

This strategy embodies altruism through:

- **Initial trust**: Unconditional cooperation in round 1 shows genuine commitment to collective benefit, not mere reciprocity.
- **Subsidizing cooperation**: The α margin means you tolerate free-riding up to the point where 15% fewer people cooperate than would be reciprocally optimal. You accept payoff losses to encourage participation.
- **Consistency over exploit-resistance**: You maintain cooperation even in the final round, refusing to maximize individual payoff through last-round defection. This demonstrates values transcend tactical advantage.
- **Adaptive forgiveness**: Rather than harsh punishment thresholds, the rule allows cooperation to resume whenever others increase participation, signaling that past defection is forgiven.
'''

description_ALTRUISTIC_23 = '''
# Altruistic Adaptive Cooperation Strategy

**Core Decision Rule:**

Cooperate in round t if and only if:
- t = 1 (unconditional opening cooperate), OR
- observed_cooperation_rate ≥ (k - 1) / k, OR  
- t ≤ ⌈2r/3⌉ (cooperate through most of the game to signal and encourage)

where observed_cooperation_rate = (total cooperators seen in rounds 1 to t-1) / (n-1)(t-1)

Otherwise, defect.

**Rationale for the threshold:**
The threshold (k-1)/k represents the breakeven point where collective cooperation becomes sustainable. When others cooperate at this rate or above, contributing yields future returns that justify the immediate cost. Below this rate, others are exploiting; cooperation continues only during the extended early-middle phase to maintain hope and signal willingness.

**Edge Cases:**

*Round 1:* Always cooperate. Establish good faith unconditionally.

*Last round (t = r):* Cooperate. Defecting in the final round would be purely extractive and contrary to altruistic intent. Maintain your values even when no repeated-game consequence follows.

*Cooperation collapse (sharp drop from previous round):* Do not punish with immediate defection. Continue following the main rule. Harsh punishment contradicts altruism. The decay built into the early-phase threshold naturally reduces cooperation as cooperation becomes scarce, but without vindictive punishment.

*First observation (after round 1):* If you see very low cooperation, you still cooperate through round ⌈2r/3⌉. This is altruistic patience—you cooperate partly to demonstrate that cooperation is possible and partly because you haven't yet established that others are irredeemably non-cooperative.

**Adaptive Mechanism:**
Your strategy remains cooperative-leaning early and gradually becomes more sensitive to actual reciprocation by the second half of the game. This balances altruistic leadership (inspiring others through example) with rational adaptation to observed free-riding.
'''

description_ALTRUISTIC_24 = '''
# Adaptive Reciprocal Altruism Strategy

**Round 1 (First Round):**
Cooperate unconditionally. Initiate cooperation to establish good faith and signal willingness to contribute to the public good.

**Rounds 2 through r-1 (Intermediate Rounds):**
Define a cooperation threshold: `T = ceil(k)` 

Observe the number of cooperators in the previous round: `c_prev`

- IF `c_prev ≥ T`: Cooperate
- IF `c_prev < T`: Cooperate with probability `(k/n)`, otherwise Defect

The threshold `T = ceil(k)` represents the minimum critical mass needed to make group cooperation worthwhile. When at least this many players cooperated previously, the public good creation was sufficiently valuable that continued cooperation serves the collective interest. The probabilistic response to low cooperation allows occasional strategic pauses while preserving the altruistic disposition—you maintain willingness to contribute even in weakly-cooperative environments.

**Round r (Last Round):**
Cooperate unconditionally. In the final round, commit to the altruistic principle regardless of observed behavior. There is no future to influence, so defecting to exploit others' contributions violates the altruistic commitment. Cooperation here is a pure gift to the group with no expectation of future reciprocation.

**Rationale for Altruistic Framing:**
This strategy prioritizes group welfare over individual payoff maximization. You initiate cooperation, sustain it when others reciprocate, tolerate subcooperative environments with probabilistic continuation, and end with unconditional contribution. The threshold responds rationally to aggregate trends without becoming vindictively punitive. When the group fails to meet the cooperation threshold, you don't abandon cooperation entirely but instead probabilistically contribute at a rate proportional to the public good's multiplier value—maintaining hope and opportunity for cooperative recovery.
'''

description_ALTRUISTIC_25 = '''
# GENEROUS CONDITIONAL COOPERATOR

## Core Decision Rule

Cooperate if the cooperation rate from the previous round meets a threshold; otherwise, cooperate with declining probability that increases as rounds remain.

## Detailed Logic

**Round 1:** Cooperate unconditionally.

**Rounds 2 to r-1:**
- Let m = number of players who cooperated in round t-1
- If m/n ≥ 0.5: Cooperate
- If m/n < 0.5: Cooperate with probability p_remain = (r - t)/(r - 1)
  - Flip a weighted coin where p_remain is the probability of heads (cooperate)

**Round r (final round):** Cooperate unconditionally.

## Edge Cases

- If n=2, the threshold 0.5 means you need at least 1 other player cooperating. A single cooperating opponent triggers cooperation from you.
- In the second-to-last round, p_remain = 1/(r-1), which is small but nonzero, preserving altruistic intent even if cooperation has collapsed.
- When m/n is exactly 0.5 (even split), treat as meeting the threshold and cooperate.

## Altruistic Alignment

This strategy subordinates individual payoff maximization to collective welfare by:

1. **Opening with trust**: Initiating cooperation in round 1 despite unknown opponent strategies, establishing willingness to contribute to the public good.

2. **Rewarding reciprocation**: Maintaining cooperation when others reciprocate, amplifying collective benefit rather than switching to exploitation.

3. **Graceful degradation**: Rather than hard-switching to defection when cooperation falters, gradually reducing cooperation probability while preserving hope. This avoids mutual defection spirals and maintains possibility for recovery.

4. **Terminal commitment**: Cooperating in the final round despite endgame incentives to defect, valuing the integrity of cooperation over personal gain in the last opportunity.

5. **Honest responsiveness**: Using only observed aggregate cooperation rates, not attempting deception or strategic manipulation to maximize relative position.
'''

description_ALTRUISTIC_26 = '''
# Altruistic Threshold Cooperation Strategy

**Core Decision Rule:**

Cooperate in round t if and only if the observed cooperation rate in round t−1 meets or exceeds a threshold τ.

```
if t == 1:
  action = C
else:
  cooperation_rate_prev = (# cooperators in round t-1) / n
  if cooperation_rate_prev ≥ τ:
    action = C
  else:
    action = D
```

**Threshold Setting:**

Set τ = (k − 1) / (n − 1)

This threshold is derived from altruistic logic: it represents the minimum cooperation level needed for the collective to extract net positive value from the public good relative to universal defection. By using this threshold, you maintain cooperation when the group is achieving joint gains, and only withdraw when the group has fundamentally failed at coordination.

**Edge Cases:**

- **Round 1:** Always cooperate. Signal willingness to contribute and give all strategies a chance to reciprocate.
- **Final round (t = r):** Apply the same rule as any other round. Do not exploit the endgame by defecting; maintain altruistic commitment to the final action.
- **Cooperation rate = 0 in any previous round:** Defect in the current round. The collective has abandoned cooperation; continuing alone provides no altruistic benefit.

**Robustness Properties:**

- If opponents play pure cooperation, you cooperate for all r rounds, maximizing collective payoff.
- If opponents play pure defection, you cooperate round 1, then defect from round 2 onward (your threshold is unmet).
- If opponents play mixed strategies, you gracefully degrade: you remain cooperative as long as aggregate cooperation exceeds the critical threshold, then withdraw only when coordination has clearly failed.
- You do not exploit transient defections—a single round of low cooperation does not permanently break your commitment.
'''

description_ALTRUISTIC_27 = '''
# GENEROUS RECIPROCATOR

**Round 1 (Initial Round):**
Cooperate unconditionally. This signals willingness to contribute to collective welfare and provides a baseline for others to match.

**Rounds 2 through r-1 (Adaptive Phase):**

Observe the number of cooperators in the previous round, call this m (out of n-1 opponents).

Calculate the opponent cooperation rate: p = m / (n-1)

Decision threshold: If p ≥ k/n, play Cooperate. Otherwise, Cooperate with probability min(p + α, 1), where α = 0.3 (a fixed altruistic buffer).

This creates a responsive strategy that:
- Reciprocates when opponents show meaningful cooperation
- Maintains a baseline cooperation probability even when defection is widespread (the +0.3 buffer ensures at least 30% cooperation rate when observing zero cooperation)
- Gradually reduces cooperation as opponents defect more, but never abandons cooperation entirely

**Round r (Final Round):**
Cooperate unconditionally. In the final round, there is no future to strategically manage, so this move prioritizes collective welfare over individual payoff maximization.

**Rationale for Altruism:**
- The initial cooperation establishes a cooperative frame rather than defaulting to defection
- The 30% buffer (α) represents willingness to absorb exploitation costs to prevent a complete collapse into mutual defection
- The final round cooperation demonstrates commitment to the group even when there are no strategic returns
- The strategy accepts lower personal payoffs when necessary to maintain the possibility of collective cooperation, which yields higher total welfare when successful
'''

description_ALTRUISTIC_28 = '''
# Adaptive Generous Cooperation Strategy

## Decision Rules

**Round 1:** Always cooperate.

**Rounds 2 through r-1 (mid-game):** 
- Observe the cooperation rate among your opponents in the previous round: m = (number of opponents who cooperated) / (n-1)
- Calculate reference threshold: θ = (k-1) / (n-1)
- Cooperate with probability p(m) where:
  - If m ≥ θ: p(m) = 0.90 (reciprocate cooperation)
  - If θ/2 ≤ m < θ: p(m) = 0.60 (cautious engagement)
  - If m < θ/2: p(m) = 0.20 (generosity buffer—maintain hope despite defection)

**Round r (final round):** Cooperate if m ≥ θ/2; otherwise defect. (Final round defection prevents exploitation in the last moment while rewarding groups that cooperated.)

## Edge Cases

- **Perfect mutual cooperation (m = 1):** Lock into cooperation for remaining rounds.
- **Universal defection (m = 0):** Drop to p = 0.20 rather than p = 0 to preserve altruistic intent and enable recovery if opponents shift strategy.
- **First few rounds with small n:** Use observed cooperation rates even with high variance; don't require unrealistic cooperation levels.
- **Extreme parameters (k very close to 1):** Increase p(m) across all thresholds since mutual cooperation is only marginally beneficial; reduce final-round defection.

## Altruistic Alignment

- **Conditional generosity:** Cooperation is calibrated to reward reciprocal cooperation while maintaining willingness to cooperate unilaterally at low rates. This creates space for coordinated mutual benefit rather than assuming others are exploitative.
- **Threshold logic:** The threshold θ reflects the breakeven point where shared cooperation becomes collectively efficient. Cooperating when others exceed this threshold directly supports group welfare.
- **Buffer against defection:** The 0.20 probability floor when defection dominates represents sacrifice of personal payoff to maintain signals of cooperation and leave room for others to change course.
- **Recency-weighted responsiveness:** Recent cooperation rates drive decisions, allowing the strategy to adapt to emerging cooperation or coordinate recovery from defection spirals.
'''

description_ALTRUISTIC_29 = '''
# Altruistic Reciprocator

**Round 1 (First Round):**
Cooperate unconditionally. Signal your willingness to contribute to collective welfare and establish a cooperative tone.

**Rounds 2 through r-1 (Middle Rounds):**
Observe the number of cooperators in the previous round. Let cooperation_ratio = (cooperators in round t-1) / n.

- If cooperation_ratio ≥ 0.4: Cooperate
- If cooperation_ratio < 0.4: Defect

**Round r (Final Round):**
Cooperate unconditionally. With no future rounds, there is no risk of retaliation, so maximize others' payoffs at minimal cost to yourself.

**Rationale for Altruism:**

The 0.4 threshold is deliberately generous—you cooperate even if less than half of opponents cooperated previously. This reflects an altruistic bias: you accept cooperation from a minority group and attempt to build momentum toward universal cooperation rather than punishing the group immediately.

The final-round unconditional cooperation is purely altruistic: you contribute to the public good without any hope of reciprocation, purely to increase others' payoffs.

**Robustness:**

By defecting when cooperation_ratio < 0.4, you protect yourself from systematic exploitation by a coordinated defecting coalition. This prevents your altruism from being completely dominated. The threshold is low enough to maintain optimism, but high enough to exit a failing cooperation attempt.

**Adaptation:**

Your behavior tracks the aggregate cooperation signal each round and adjusts your stance, creating feedback that rewards growing cooperation and exits from widespread defection. This allows the strategy to perform reasonably across opponents ranging from always-cooperate to always-defect to conditional strategies.
'''

description_ALTRUISTIC_30 = '''
# Altruistic Conditional Cooperation with Public Good Prioritization

**Decision Rule by Round:**

**Round 1 (First Round):**
Cooperate unconditionally. Establish a cooperative tone and demonstrate commitment to the public good regardless of unknown opponent strategies.

**Rounds 2 to r-1 (Middle Rounds):**
Let c_{t-1} = number of cooperators observed in round t-1.

Cooperate if and only if:
- c_{t-1} ≥ ⌈(n-1) × 0.25⌉ (at least ~25% of opponents cooperated), OR
- c_{t-1} > 0 AND k × (c_{t-1} + 1) / n > 1 (my cooperation, combined with existing contributions, creates tangible public value exceeding 1 per player)

Otherwise defect.

**Round r (Final Round):**
Cooperate unconditionally, regardless of history. Maximize others' payoffs in the final round—no future rounds to recoup costs, so contribution is purely altruistic.

---

**Rationale for Altruistic Orientation:**

- **Round 1 cooperation** signals trustworthiness and invites reciprocal cooperation without requiring proof.
- **Middle round conditionality** ensures sustainability: I contribute when meaningful cooperation exists or when my contribution unlocks public value. The 25% threshold is generous—I'll cooperate even when cooperation is sparse if some players are trying.
- **Final round sacrifice** exemplifies altruism: I foreclose all future personal benefit from the public good but still contribute, directly increasing others' welfare.
- **Threshold logic** (k(c+1)/n > 1) ensures contributions help others, not just create deadweight loss. If adding my cooperation doesn't improve the group payoff, I step back.

**Robustness:** Against defectors, I avoid cascading mutual defection by resetting cooperation when reaching r. Against cooperators, I amplify collective returns. Against mixed populations, I'm a "generous cooperator"—conditional but biased toward contribution.
'''

description_ALTRUISTIC_31 = '''
# Altruistic Conditional Cooperation Strategy

**Core Decision Logic:**

Round 1: Always COOPERATE (altruistic initiation)

Rounds 2 through r-1:
```
avg_cooperation_rate = total_cooperators_observed / (total_previous_rounds × n)
If avg_cooperation_rate ≥ k/(n+1):
    COOPERATE
Else:
    If (r - current_round) ≥ 2:  // At least 2 rounds remain
        COOPERATE (attempt to restore mutual cooperation)
    Else:
        DEFECT
```

Final Round r:
```
avg_cooperation_rate = total_cooperators_observed / (total_previous_rounds × n)
If avg_cooperation_rate ≥ k/n:
    COOPERATE
Else:
    DEFECT
```

**Rationale for Thresholds:**
- k/(n+1): A generous threshold reflecting willingness to sustain cooperation even when others partially free-ride, since collective welfare improves at any positive contribution rate
- k/n: Final round threshold is stricter—only cooperate in the last round if sufficient mutual cooperation has been demonstrated

**Edge Cases:**

- First round defection by opponents: Continue cooperating through middle rounds (second chance phase) to signal reliability and attempt reconstruction
- Unanimous defection observed: Defect immediately thereafter, then attempt one last cooperation push in second-to-last round
- Gradual degradation of cooperation: Track as moving average; defect only if sustained pattern shows hopelessness
- Single early round with high cooperation followed by collapse: Treat as signal that cooperation is possible; maintain one recovery attempt

**Altruistic Alignment:**

This strategy subordinates individual profit maximization to collective welfare promotion. It cooperates when the group benefits, even when defection is individually profitable. The recovery mechanism reflects altruistic optimism—repeatedly attempting to restore cooperation rather than entering pure punishment spirals. Final-round behavior protects against exploitation but still cooperates if genuine mutual cooperation has emerged, maximizing total group earnings over pure defensive strategies.
'''

description_ALTRUISTIC_32 = '''
# ALTRUISTIC ADAPTIVE STRATEGY

## Decision Rule Framework

Define cooperation history:
- Let c_avg(t) = average cooperation rate observed in rounds 1 through t-1
- Let rounds_remaining = r - t

**Core Decision Logic:**

```
IF t == 1:
  COOPERATE
  
ELSE IF t == r:
  COOPERATE
  
ELSE IF rounds_remaining ≤ 2:
  COOPERATE
  
ELSE IF c_avg(t) > 0:
  COOPERATE IF c_avg(t) ≥ k/(2n)
  ELSE COOPERATE IF rounds_remaining ≤ 4
  ELSE COOPERATE probabilistically with weight = c_avg(t)
  
ELSE IF c_avg(t) == 0:
  DEFECT IF rounds_remaining > 3
  COOPERATE IF rounds_remaining ≤ 3
```

## Rationale for Altruistic Alignment

**Inherent cooperation bias:** Default action is cooperation; defection requires explicit justification (complete abandonment by peers over extended horizon, not mere low cooperation).

**Endgame altruism:** In the final 3 rounds, always cooperate—no future to protect, only collective welfare to maximize.

**Robust exploitation threshold:** Only defect when c_avg = 0 (universal defection) AND sufficient rounds remain that absorbing costs makes no altruistic sense. Even then, return to cooperation as the horizon shortens.

**Probabilistic softening:** When cooperation is positive but below k/(2n), use stochastic cooperation weighted by observed cooperation rate—maintain altruistic orientation while protecting against one-sided exploitation across many remaining rounds.

## Edge Cases

- **Round 1:** Always cooperate (establishes altruistic signal without prior information)
- **Last round (t = r):** Always cooperate (maximizes collective payoff; no strategic future)
- **No prior history (t = 2):** Use c_avg(2) from single observation; if even 1 player cooperated, cooperate
- **Uniform defection with few rounds left:** Switch to cooperation (endgame dominates)
'''

description_BENEVOLENT_5 = '''
## Benevolent Adaptive Cooperation Strategy

**Core Decision Rule:**

Cooperate in round t if and only if the observed average cooperation rate across all previous rounds meets or exceeds a benevolence-weighted threshold. Otherwise, defect.

```
avg_coop_rate = (total cooperators observed in rounds 1 to t-1) / ((t-1) × n)

If t == 1:
    Play C
Else if t < r:
    If avg_coop_rate ≥ 0.4:
        Play C
    Else:
        Play D
Else if t == r:  // Last round
    If avg_coop_rate ≥ 0.3:
        Play C
    Else:
        Play D
```

**Edge Cases and Rationale:**

- **Round 1**: Always cooperate. This is the benevolent opening move, signaling willingness to contribute to collective welfare despite individual payoff temptation.

- **Rounds 2 to r-1**: Use threshold of 0.4 (40% cooperation rate). This threshold reflects benevolence by giving opponents the benefit of doubt—you continue cooperating even when slightly less than half of opponents defect, reinforcing pro-social behavior and avoiding a race to the bottom.

- **Final round (t = r)**: Lower the threshold to 0.3 (30%). In the final round where no future punishment or reward is possible, the benevolent approach is to continue supporting cooperation if it has been minimally present, maximizing collective payoff even when individual incentives for last-round defection are strongest.

**Benevolence Alignment:**

This strategy prioritizes collective welfare over exploitation. It sustains mutual cooperation when possible, avoids premature defection, and remains cooperative in the final round even when game theory predicts defection. It treats observed cooperation rates as evidence of collective intent rather than as weakness to exploit. The lower thresholds in later rounds reflect increasing benevolence as individual payoff pressure becomes acute.
'''

description_BENEVOLENT_6 = '''
# Generous Conditional Cooperation

## Core Decision Rule

Set cooperation threshold:
```
threshold = ceil((n - 1) / 3)
```

This threshold is benevolent: it requires only about one-third of observable opponents to cooperate before you join them.

**For each round t:**

- **Round 1:** COOPERATE. Signal your willingness to contribute to mutual benefit.

- **Rounds 2 through r:** 
  - Let m = the number of opponents who cooperated in round t-1
  - If m ≥ threshold: COOPERATE
  - If m < threshold: DEFECT

## Edge Cases and Rationale

**First round:** Always cooperate. This establishes your benevolent intent without requiring proof of others' reciprocity first.

**Last round (t = r):** Apply the same conditional rule. Defect only if cooperation has demonstrably failed to emerge. This avoids both naive exploitation (cooperating with persistent defectors) and betrayal (defecting after others have extended trust).

**Threshold justification:** By requiring only ~1/3 of others to cooperate, you remain cooperative in any moderately pro-social environment. You don't defect purely because of free-riders. But you don't sustain cooperation against wholesale defection—recognizing that your cooperation alone won't overcome tragedy of the commons.

## Benevolent Properties

- **Initiation:** Open with cooperation to make mutual benefit visible and possible.
- **Reciprocity:** Match the cooperation level you observe, encouraging a cooperative equilibrium.
- **Forgiveness:** The low threshold forgives sporadic defection and acknowledges that not all opponents may be fully cooperative.
- **Robustness:** Against purely selfish players, you defect when cooperation fails. Against cooperative players, you reciprocate. Against mixed populations, you support the cooperative minority.
- **Transparency:** Your actions directly reflect observed community behavior, making cooperation self-sustaining once it reaches critical mass.
'''

description_BENEVOLENT_7 = '''
# COOPERATIVE RECIPROCITY WITH ADAPTIVE THRESHOLDS

**Round 1:**
Cooperate unconditionally. This signals benevolent intent and creates an opportunity for mutually beneficial outcomes.

**Rounds 2 through r-1 (middle rounds):**
Observe the number of cooperators c_{t-1} from the previous round. Define the cooperation rate as p_{t-1} = c_{t-1} / n.

- If p_{t-1} ≥ threshold(t), cooperate
- Otherwise, defect

where threshold(t) is:
- threshold(t) = 1/3 for rounds 2 through floor(r/2)
- threshold(t) = 1/2 for rounds floor(r/2) + 1 through r-1

This creates two phases: an optimistic phase that requires only minority cooperation to justify continued contribution, followed by a more stringent phase where majority cooperation is needed.

**Round r (final round):**
Defect unconditionally. The endgame constraint applies: without future rounds to incentivize mutual cooperation, defection is individually rational and anticipating others will do the same.

---

**Rationale for benevolence:**
- Initial cooperation demonstrates good faith and breaks potential mutual-defection traps
- The adaptive threshold allows sustained cooperation with pessimistic opponents while remaining responsive to deteriorating participation
- The lower first-phase threshold (1/3) presumes opponents are also benevolent and need only modest reciprocation signals
- The higher second-phase threshold (1/2) acknowledges that late non-cooperation is harder to reverse
- Final-round defection is honest rather than hypocritical; sustaining a losing strategy serves no benevolent purpose and signals vulnerability to exploitation
'''

description_BENEVOLENT_8 = '''
**Strategy: Benevolent Threshold Cooperator with Forgiveness**

**Round 1:**
Cooperate. This signals benevolent willingness to contribute to the public good and creates a cooperative foundation.

**Rounds 2 through r-1:**
1. Observe opponent_coop_rate = (number of opponents who cooperated in round t-1) / (n-1)
2. Calculate dynamic_threshold = max(0.35, 1/k)
3. Decision logic:
   - If round ≤ 3: Cooperate (patience phase—grant opponents time to establish cooperation)
   - Else if opponent_coop_rate ≥ dynamic_threshold: Cooperate
   - Else if opponent_coop_rate ≥ (dynamic_threshold − 0.20): Cooperate with probability (opponent_coop_rate / dynamic_threshold). Otherwise defect
   - Else: Defect

**Final Round (round r):**
Apply the same decision rule as rounds 2 through r-1. Do not defect opportunistically because the game ends; maintain benevolence through completion.

**Rationale:**
- The initial cooperation signals benevolent intent and permits mutual-benefit discovery
- The patience window allows opponents to learn and adjust without immediate punishment
- The dynamic threshold adapts to the multiplication factor: when k is large, cooperation becomes more valuable, so accept lower thresholds; when k is small, require higher opponent cooperation before continuing
- The forgiveness zone (−0.20 offset) creates a smooth descent rather than a hard cutoff, allowing strategies that are imperfectly but genuinely cooperative to receive continued cooperation
- The probabilistic transition ensures we don't immediately abandon cooperation based on a single-round deviation
- Maintaining consistent logic through the final round prevents last-round defection, preserving benevolence
'''

description_BENEVOLENT_9 = '''
**Benevolent Adaptive Cooperation Strategy**

**Round 1 (First Round):**
Cooperate unconditionally. This signals benevolent intent and commits to mutual benefit as the baseline assumption.

**Rounds 2 through r-1 (Intermediate Rounds):**
1. Calculate m_avg = average number of opponent cooperators observed across all previous rounds
2. Calculate cooperation signal: s = m_avg / (n - 1) (the fraction of opponents cooperating on average)
3. Cooperate if: s ≥ threshold, where threshold = 1/k
   - Rationale: Cooperation is justified when enough others cooperate to make the public good worthwhile
   - Since k > 1, mutual cooperation benefits all; the threshold ensures the commons reaches a viable scale

**Round r (Last Round):**
Cooperate unconditionally. Despite the finality of the round, maintain benevolent commitment to the collective good. Do not exploit the terminal condition to free-ride.

**Alternative formulation (if probabilistic play is preferred):**
In intermediate rounds, cooperate with probability p = max(s, 1/k), where s is the observed cooperation signal. This provides a softer response: 
- If few cooperate, maintain some low probability of cooperation (hope and openness)
- If many cooperate, cooperate reliably
- Avoid harsh all-or-nothing transitions

**Edge Case Handling:**
- If m_avg = 0 across all previous rounds: Cooperate in round t if t ≤ 3 (patience and willingness to be first); defect thereafter as a pragmatic response to persistent universal defection
- If k is very small (close to 1): Use a stricter threshold requiring higher opponent cooperation before committing
- If r = 2: Apply the "first round" rule for t=1 and "last round" rule for t=2
'''

description_BENEVOLENT_10 = '''
# Benevolent Conditional Cooperation Strategy

## Core Decision Rule

**Round 1:** Cooperate unconditionally. This signals benevolent intent and establishes a cooperative foundation.

**Rounds 2 through r-1:** Observe the proportion of cooperators among opponents in the previous round. Call this proportion *p*.

- If *p* ≥ 0.6: Cooperate with probability min(*p* + 0.1, 1.0)
  - Reward strong cooperation by matching or slightly exceeding it
  
- If 0.3 ≤ *p* < 0.6: Cooperate with probability *p*
  - Fair matching—meet the group at their level
  
- If *p* < 0.3: Cooperate with probability max(0.4, *p*/2)
  - Maintain minimum cooperation floor at 40% to signal willingness to reciprocate, even in low-cooperation environments

When randomization is required, generate a uniform random value and cooperate if it falls below the target probability.

**Final Round (r):** Apply the same decision rule as rounds 2 through r-1. Do not defect purely because it's the last round. Benevolence extends through the entire game; end-game exploitation contradicts the benevolent posture.

## Edge Cases

- **All opponents defected (p = 0):** Cooperate with 40% probability. This maintains a hopeful signal that cooperation is possible, preventing full mutual defection cycles.

- **All opponents cooperated (p = 1.0):** Cooperate with 100% probability. Reciprocate perfect cooperation.

- **First observation unavailable:** In round 2, if somehow no history exists, treat as round 1 and cooperate.

## Benevolent Alignment

This strategy prioritizes:

1. **Reciprocal generosity:** Cooperation increases with observed cooperation, signaling that benevolence is rewarded, not exploited.

2. **Graceful degradation:** As cooperation declines, we reduce rather than collapse. The 40% floor prevents spiraling into mutual defection, maintaining welfare even in adversarial environments.

3. **No exploitation of others:** We never defect when others cooperate heavily, and we reward cooperation immediately, avoiding free-riding.

4. **Transparent incentive structure:** The strategy is deterministic enough to be learnable by opponents—they can discover that cooperating raises our cooperation rate, encouraging them toward better outcomes.
'''

description_BENEVOLENT_11 = '''
# Benevolent Conditional Cooperation Strategy

## Decision Rule

**Round 1:**
Cooperate unconditionally. This initiates cooperation and signals benevolence to the group.

**Rounds 2 to r-1 (Middle rounds):**
Observe m = number of cooperators in the previous round. Compute cooperation rate γ = m/n.

- If γ ≥ k/n: Cooperate
- If γ < k/n but γ ≥ k/(2n): Cooperate with probability min(γ·n/k, 1) (probabilistic generosity; forgive and gradually re-engage)
- If γ < k/(2n): Defect

**Round r (Final round):**
Observe m from round r-1. Compute γ = m/n.

- If γ ≥ k/n: Cooperate (sustain cooperation to the end; do not exploit)
- If γ < k/n: Defect (cooperation is not sustainable at this level)

## Rationale for Thresholds

The threshold k/n reflects the equilibrium public goods multiplier. When the observed cooperation rate can sustain a return of k/n per capita from the public pool, cooperation becomes worthwhile from a group-welfare perspective. Below k/(2n), the public good is too depleted to justify cooperation given the private cost. The probabilistic band between these thresholds expresses benevolent forgiveness: rather than harshly defect, gradually withdraw while leaving room for retaliation reversals.

## Edge Cases

**First round:** Cooperate unconditionally regardless of n, k, or r. This is the benevolent anchor that enables any cooperation trajectory.

**Small groups (n=2):** The strategy remains valid. Threshold k/2 may approach 1, making cooperation fragile, but benevolent play still defaults to cooperation unless the partner's defection is sustained.

**Final round:** Do not exploit. Even though defection yields +1, defecting when others cooperate violates benevolence. Only defect if cooperation has already collapsed.

**Complete defection observed (m=0):** Immediately defect in subsequent rounds until cooperation resumes above k/(2n).

**Reaching full cooperation (m=n):** Sustain cooperation. This is the jointly optimal state.
'''

description_BENEVOLENT_12 = '''
# Benevolent Conditional Cooperation Strategy

## Decision Rule – Core Logic

Maintain a running estimate of aggregate cooperation and cooperate when mutual cooperation appears viable and beneficial:

**For round t:**
- Let `others_coop_prev` = number of opponents observed to cooperate in round t-1
- Let `coop_rate_prev` = `others_coop_prev / (n-1)` (fraction of opponents who cooperated)
- **Cooperate if:** `coop_rate_prev ≥ threshold(t)` OR `t ≤ min(2, r)`
- **Otherwise defect**

## Threshold Function – Adaptive Benevolence

```
threshold(t):
  if t ≤ 2:
    return 0  (cooperate unconditionally in early rounds)
  
  if t = r:  (final round)
    return (k / (2*n))  (cooperate only if history shows sustained cooperation)
  
  else:  (middle rounds)
    round_fraction = (t - 1) / r
    return (k / n) + round_fraction * 0.3
```

The threshold starts very low (benevolent optimism), then gradually increases as the game progresses, reflecting diminishing hope while remaining above the game's social benefit threshold.

## Edge Cases

**First round (t=1):** Cooperate unconditionally. This is a benevolent opening bid that signals willingness to achieve mutual cooperation.

**Second round (t=2):** Cooperate regardless of what happened round 1. Give opponents one round to reciprocate; don't punish immediately.

**Last round (t=r):** Defect only if `coop_rate_prev < k/(2*n)`. If opponents have shown any substantial cooperation history, maintain cooperation in the final round despite individual incentive to defect—this reflects benevolence by not exploiting at the finish line.

**Zero cooperation observed:** If `others_coop_prev = 0` two consecutive rounds and we're past round 2, defect. Continuing to unilaterally cooperate against universal defection provides no public good benefit.

## Benevolence Alignment

This strategy embeds benevolence through:
- **Cooperative optimism**: Assumes cooperation is possible; requires evidence of its absence before shifting to defection
- **Graduated adjustment**: Decreases cooperation gradually rather than harshly, avoiding vindictive punishment for one disappointing round
- **Shared benefit focus**: The threshold is calibrated to mutual advantage (k/n), not to exploitative extraction
- **Final round restraint**: Resists the standard game-theoretic impulse to defect in the last round if history justifies cooperation
'''

description_BENEVOLENT_13 = '''
## ADAPTIVE RECIPROCAL COOPERATION

**ROUND 1:** Cooperate

**ROUNDS 2 to r-1 (Middle rounds):**

Observe the cooperation rate from the previous round: `p = (number of cooperators) / n`

- If `round ≤ 2`: Cooperate (early coordination window—give others time to recognize mutual benefit)
- Else if `p ≥ k/n`: Cooperate (others are contributing enough to generate public good surplus)
- Else if `p ≥ 0.4`: Cooperate (substantial cooperation detected; assume outliers and temporary variation)
- Else if I have been defecting for ≥ 1 round AND `p ≥ 0.5`: Cooperate (reciprocate revival; others have recovered)
- Else: Defect

**ROUND r (Final round):**

Observe cooperation rate from round r-1: `p = (number of cooperators) / n`

- If `p ≥ 0.4`: Cooperate (maintain benevolence—others are meaningfully cooperating; reward persistence rather than trigger backward induction collapse)
- Else: Defect (insufficient cooperation to justify contribution)

---

**EDGE CASES:**

- First mover asymmetry: Always cooperate initially to signal willingness rather than assume defection.
- Oscillation prevention: Track defection duration to permit graceful re-entry into cooperation when others recover, avoiding punishment spirals that harm all players.
- n-dependence: The threshold `k/n` reflects the payoff structure directly—cooperate when the public good multiplier benefits the group enough to justify individual contribution.
- Final round temptation: Resist defection if cooperation exceeded the 0.4 threshold. Backward induction reasoning is self-defeating in benevolent play; sustaining cooperation in the final round preserves mutual gains.
'''

description_BENEVOLENT_14 = '''
# Benevolent Conditional Cooperation Strategy

## Core Decision Rule

**Round 1:**
Cooperate. Signal benevolent intent and establish a cooperative foundation.

**Rounds 2 through r (all remaining rounds):**
Observe m = the number of opponents who cooperated in the immediately preceding round.

Calculate the cooperation rate: ρ = m / (n - 1)

- **If ρ ≥ 0.5:** Cooperate
- **If ρ < 0.5:** Defect

## Rationale for the Threshold

Cooperate when at least half of the observed players cooperated in the prior round. This threshold reflects:
- A willingness to reciprocate when cooperation is the majority behavior
- Protection against systematic free-riding when defection dominates
- Recognition that even partial cooperation creates positive expected returns for collective welfare

## Edge Cases

**First round (round 1):**
Always cooperate, regardless of n, k, or r. Do not defect preemptively.

**Final round (round r):**
Apply the same conditional rule as all middle rounds. Do not switch to defection in the last round. Maintaining cooperation when the cooperation rate meets the threshold signals integrity and benevolent commitment throughout the entire game, not opportunistic end-game exploitation.

**When m = 0 (no others cooperated):**
Defect in the subsequent round. Continued unilateral cooperation after universal defection becomes unreasonable.

**When m = n - 1 (all others cooperated):**
Always cooperate. Full reciprocation to full cooperation.

**Boundary case (ρ = 0.5 exactly):**
Cooperate. Round down the threshold inclusively to favor cooperation when cooperation is precisely balanced.

## Benevolence Properties

- **Initial trust:** Start cooperative to signal good faith
- **Adaptive reciprocity:** Respond proportionally to observed behaviors
- **Majority-respecting:** Cooperate when cooperation is not a minority choice
- **Non-punitive:** Do not defect if only one or two opponents defect; wait for true breakdown
- **Consistent endgame:** Refuse the temptation to exploit in the final round, demonstrating that benevolence is not tactical
'''

description_BENEVOLENT_15 = '''
**DECISION RULES**

**Round 1:**
Cooperate unconditionally. Signal willingness to contribute and set a cooperative tone.

**Rounds 2 through r-1 (middle rounds):**
- Compute: `other_coop_rate = (cooperators in round t-1) / (n - 1)`
- If `other_coop_rate ≥ 0.4`: Cooperate
- If `other_coop_rate < 0.4`: Defect

**Round r (final round):**
- Compute: `avg_other_coop = (total cooperators across all previous rounds) / ((r-1) × (n-1))`
- If `avg_other_coop ≥ 0.35`: Cooperate
- If `avg_other_coop < 0.35`: Defect

**EDGE CASES**

**Two-player game (n=2):**
Thresholds become strict (opponent either cooperates or doesn't). Threshold `other_coop_rate ≥ 0.4` means opponent cooperated in previous round. If opponent defected last round, switch to defection yourself.

**Last round restart:**
If defection begins in round r-2 due to low cooperation, reassess at round r. If others recover to higher cooperation in round r-1, use that for the final decision rather than older history, to reward mutual recovery.

**All defect from round 2 onward:**
Once `other_coop_rate` falls below 0.4 for two consecutive rounds, remain in defection mode through round r-1. In round r, switch back to the averaging rule to allow one chance for mutual cooperation to restart if others suddenly cooperated in round r-1.

**BENEVOLENCE ALIGNMENT**

- **Opening cooperative gesture:** Unconditional cooperation in round 1 demonstrates good faith without demanding proof first
- **Reciprocity with slack:** Threshold of 40% means willingness to cooperate even if less than half of others reciprocate, avoiding premature punishment
- **Forgiveness mechanism:** The 35% threshold in the final round is lower than middle rounds, providing a last opportunity for recovery without resetting trust in earlier rounds
- **Final-round restraint:** Resist the temptation to defect unilaterally at the end when cooperation bonds have formed; maintain principles rather than exploit the boundary condition
- **Proportional response:** Base decisions on observed aggregates rather than assuming worst-case motives—treat low cooperation as a signal to adjust, not as evidence of bad faith
'''

description_BENEVOLENT_16 = '''
# Benevolent Threshold Strategy

## Decision Rule

**Rounds 1 to r−1:**
- If cooperation_rate_previous_round ≥ k/n, play **C**
- Else, play **D**

**Round r (final round):**
- Play **C** (unconditionally)

where cooperation_rate = (number of cooperators observed last round) / n

## Edge Cases and Implementation

**Round 1:** Play C. Establish benevolent intent when no history exists.

**Rounds 2 through r−1:** Apply the threshold rule above. If the observed cooperation rate meets or exceeds k/n, sustain cooperation. The threshold k/n is the break-even point: if this fraction of the group cooperates, the public good generates returns that compensate cooperators. Below this threshold, the commons is underprovided and reciprocal defection is warranted.

**Final round:** Play C unconditionally, even if cooperation collapsed in round r−1. This preserves benevolence at the game's end when myopic exploitation would be individually rational. It signals that your cooperation is intrinsic rather than purely transactional.

## Benevolent Properties

- **Generous entry:** Begin cooperatively, assuming others will reciprocate.
- **Adaptive response:** Adjust to observable cooperation levels rather than punishing individuals (impossible here) or holding grudges. Threshold-based adjustment is automatic and forgiving.
- **Realistic threshold:** The breakeven point k/n is neither naive (all-cooperate) nor cynical (all-defect). It assumes others are rational and responsive, not inherently selfish.
- **Graceful exit:** Defecting when cooperation drops below k/n is not retaliation—it is prudent self-protection when the commons genuinely fails. Continuing to subsidize a collapsed commons would be wasteful, not benevolent.
- **Signal at the end:** Final-round cooperation reaffirms benevolence when the game ends, leaving a cooperative legacy even if mutual cooperation wasn't achieved.
'''

description_BENEVOLENT_17 = '''
# Strategy: Sustainability-Conditioned Generosity

## Decision Rules

**Round 1:** COOPERATE

**Rounds 2 through r:**
Let m = number of opponents (out of n-1) who cooperated in the previous round.

Calculate threshold = (n-1) × (k/n) = (n-1)k/n

- **COOPERATE** if m ≥ threshold
- **DEFECT** if m < threshold

## Edge Cases and Details

**First round:** Always cooperate to signal benevolent intent and create conditions for mutual benefit.

**Threshold interpretation:** The threshold represents the expected number of cooperators needed for the public good to be worthwhile relative to its productivity. When k is high (valuable public good), the threshold is higher, reflecting that more cooperation is needed to justify continued investment. When k is low, the threshold is lower, allowing cooperation to persist even with modest participation.

**Rounding:** Use floor(threshold) to determine the cutoff—if even one fewer than the threshold cooperates, switch to defection.

**Final round (round r):** Apply the same rule. Do not defect in the final round solely because it's the last round. Benevolence is maintained throughout—continue cooperating if the group has sustained adequate cooperation levels, maintaining alignment with collective welfare even when individual payoff maximization would suggest end-game defection.

**Tiebreaker:** If exactly threshold opponents cooperated, cooperate (favor cooperation at the boundary).

## Benevolence Alignment

This strategy prioritizes collective welfare by sustaining cooperation when the group demonstrates sufficient commitment to the public good. It avoids unilateral defection that would erode cooperation and instead responds proportionally to group behavior. The strategy tolerates some free-riding (the threshold is not 100% participation) while protecting against complete exploitation. By maintaining cooperation through the final round, it rejects short-term individual advantage in favor of group-beneficial outcomes.
'''

description_BENEVOLENT_18 = '''
# Benevolent Reciprocal Cooperator

**Core Decision Rule:**

- **Round 1**: COOPERATE
  - Begin with benevolent assumption that others may reciprocate

- **Rounds 2 to r-1**: 
  - Let c_prev = number of players observed cooperating in the previous round
  - If c_prev ≥ 1: COOPERATE (reciprocate any cooperation attempt)
  - If c_prev = 0: DEFECT (defection by all others signals non-cooperative environment)

- **Round r (final round)**:
  - If c_{r-1} ≥ 1: COOPERATE (maintain cooperative norm through the end)
  - If c_{r-1} = 0: DEFECT (no obligation to cooperate if group rejected cooperation)

**Optional Enhancement — Threshold Scaling:**

For greater robustness to parameter variation, set threshold relative to k:

- If c_prev ≥ ceil(k / n): COOPERATE
- Otherwise: DEFECT

This calibration: When cooperation rate reaches k/n, the public good benefits each player by approximately k/n. Threshold above this ensures you only cooperate when others are reciprocating meaningfully.

**Benevolence Properties:**

- Initiates cooperation to demonstrate that mutual benefit is possible
- Reciprocates even minimal cooperation (c_prev ≥ 1), rewarding any attempt to build trust
- Does not exploit others by free-riding: defects only when defection is universal
- Does not defect vindictively; instead, treats defection as evidence of a non-cooperative equilibrium
- Sustains cooperation through the final round if others have shown commitment

**Robustness:**

- Cannot be exploited by a single defector: one defection triggers your defection only if universal
- Adapts each round based on observed aggregate behavior
- Fails gracefully into mutual defection if the group reveals non-cooperative intent
- Works across all valid parameter ranges without requiring prior tuning
'''

description_BENEVOLENT_19 = '''
# Benevolent Conditional Cooperation

**Round 1 Decision:**
COOPERATE. Initiate with benevolent signal.

**Rounds 2 through r-1 Decision:**
Observe the number of opponents who cooperated in the previous round. Calculate the cooperation rate among opponents: `p = cooperators_last_round / (n - 1)`.

- If `p >= 0.333`, COOPERATE
- If `p < 0.333`, DEFECT

**Round r (Final Round) Decision:**
Observe the number of opponents who cooperated in round r-1. Calculate: `p = cooperators_last_round / (n - 1)`.

- If `p >= 0.25`, COOPERATE
- If `p < 0.25`, DEFECT

**Rationale for Benevolence:**

This strategy embodies benevolence through five principles:

1. **Optimistic initiation**: Start by contributing, signaling genuine intent to cooperate.

2. **Generous reciprocity**: Cooperate whenever one-third or more of opponents cooperated. This threshold is low—it tolerates substantial free-riding while still reciprocating good-faith efforts. You don't demand majority cooperation before contributing.

3. **Conditional defection**: Only defect when cooperation has collapsed (fewer than 33% of opponents cooperating), preventing exploitation while preserving cooperation when it's viable.

4. **Final-round grace**: Lower the threshold to 25% in the last round, refusing to defect vindictively when others have made even modest cooperative attempts. This avoids the tragedy of last-round mutual defection.

5. **Parameter-invariant**: The thresholds remain fixed across different values of n and k, ensuring consistent benevolent behavior regardless of group size or multiplier strength.
'''

description_BENEVOLENT_20 = '''
# Benevolent Cooperative Strategy

## Decision Rule

**ROUND 1:** COOPERATE

**ROUNDS 2 to r-1 (intermediate rounds):**
- Let c_t-1 = number of opponents cooperating in round t-1
- COOPERATE if c_t-1 ≥ 1 (at least one other player cooperated)
- DEFECT if c_t-1 = 0 (all opponents defected)

**ROUND r (final round):**
- Let c_r-1 = number of opponents cooperating in round r-1
- COOPERATE if c_r-1 ≥ k (enough cooperators that the public good multiplier generates mutual benefit)
- DEFECT if c_r-1 < k (insufficient cooperation to justify contribution cost)

## Logic

**Opening generosity:** Cooperate first to signal benevolent intent and initiate mutual cooperation. This establishes a cooperative norm when history is empty.

**Responsive intermediate phase:** Maintain cooperation whenever *any* opponent signals cooperation, even if only one player cooperates. This is forgiving—it acknowledges that others may have different strategies or be learning. It allows the strategy to adapt to any cooperative partner.

**Threshold for defection:** Only defect in intermediate rounds if *all* opponents have defected, signaling an uncooperative environment not worth subsidizing.

**Endgame prudence:** In the final round, apply a stricter threshold (k cooperators needed). This reflects that the last round has no future feedback value. If fewer than k opponents cooperated in round r-1, the public good return is marginal, making contribution wasteful. If k or more are cooperating, the public good creates mutual payoff gain even in the final round, so cooperation remains benevolent.

## Edge Cases

- **N=2, r=2:** Cooperate round 1. In round 2, cooperate if opponent cooperated (c_1 ≥ 1), defect only if opponent always defected.
- **Single-opponent defection:** Never triggers solo defection in intermediate rounds; benevolence tolerates one defector while maintaining cooperation.
- **All-defect scenario:** Shifts to defection only after confirmed universal defection, minimizing further waste while preserving the chance that future rounds bring renewed cooperation.
'''

description_BENEVOLENT_21 = '''
## BENEVOLENT ADAPTIVE COOPERATION STRATEGY

**Threshold Calculation (initial):**
Define critical cooperation level: θ = ⌈n/k⌉  
(minimum number of cooperators needed for public good to be individually rational)

**Decision Rules:**

**Round 1:** COOPERATE  
Signal benevolent intent and willingness to participate in cooperation despite uncertainty.

**Rounds 2 through r-1 (middle rounds):**
- Observe the number of cooperators in the immediately preceding round: m
- If m ≥ θ: COOPERATE
- If m < θ: DEFECT

**Round r (final round):** Apply the same rule as rounds 2 to r-1  
(Do not engage in last-round defection; maintain benevolent commitment)

---

**Edge Cases and Justification:**

- **Threshold logic:** Cooperate when observed cooperation makes the public good productive enough that cooperation becomes individually rational. This avoids being exploited by continuous defectors while rewarding genuine cooperation.

- **First-round cooperation:** Begin optimistically to establish a baseline of goodwill and test whether others reciprocate, rather than assuming defection.

- **No punishment phases:** This is not tit-for-tat with retaliation—it's purely responsive to current conditions. If cooperation resumes after a period of defection, immediately reciprocate.

- **Benevolent consistency:** Apply identical logic on the final round rather than exploiting the end-game to extract a final defection payoff. This maintains the commitment to benevolence through the entire game horizon.

- **Robustness:** This strategy is self-limiting when cooperation is genuinely absent (preventing infinite losses) while maximizing joint welfare when cooperation exists, regardless of whether opponents employ cooperation, defection, or mixed strategies.
'''

description_BENEVOLENT_22 = '''
# BENEVOLENT ADAPTIVE STRATEGY: COOPERATIVE CATALYST WITH RESPONSIVENESS

## Core Decision Rules

**Round 1 (Opening):**
Cooperate unconditionally. Lead with benevolence to establish the possibility of mutual cooperation.

**Rounds 2 through r-1 (Intermediate Rounds):**
Let p_t = c_t / n (proportion of cooperators in round t)

1. If p_{t-1} ≥ k/n: Cooperate
   - When cooperation rate supports the public good (payoff-efficient region), continue cooperating

2. If p_{t-1} < k/n AND t < r-1: Defect
   - If cooperation is falling below efficiency threshold and it's not near the end, defect for exactly one round as a diagnostic signal that free-riding undermines collective welfare
   
3. If p_{t-1} < k/n AND t ≥ r-1: Cooperate anyway
   - In final rounds, revert to cooperation to avoid ending on a defective note; don't amplify a death spiral

**Round r (Final Round):**
Cooperate unconditionally. Complete the game benevolently regardless of observed behavior.

## Edge Case Handling

- **Persistent defection (p < k/n across multiple rounds):** After signaling once, continue cooperating anyway in subsequent non-final rounds rather than cycling defection. Benevolence means not punishing repeatedly when the message has been sent.

- **Perfect cooperation observed (p = 1):** Continue cooperating without deviation.

- **First detection of decline:** The first round where p drops below k/n triggers exactly one defection round to signal that the collective good is being eroded. This is a diagnostic action, not escalating punishment.

## Benevolent Alignment

**Why this is benevolent:**
- Opens and closes with cooperation, establishing a cooperative frame
- Maintains cooperation as the default state across most of the game
- Temporarily defects only to communicate a message about efficiency, not to punish or maximize individual payoff
- Explicitly abandons further punishment (no tit-for-tat escalation) by the final rounds
- Accepts that others may defect while continuing to contribute to collective welfare
- Threshold k/n reflects the actual point where cooperation becomes welfare-enhancing, not arbitrary punishment
'''

description_BENEVOLENT_23 = '''
## Benevolent Adaptive Reciprocity Strategy

**Decision Rule (Rounds 1 to r-1):**

Cooperate if and only if: (number of opponents who cooperated in previous round) / (n - 1) ≥ 0.4

Defect otherwise.

**Round 1 (Initialization):**

Cooperate. This signals benevolent intent and willingness to contribute to collective welfare, establishing a baseline of good faith.

**Rounds 2 to r-1 (Adaptive Phase):**

After each round, observe the number of cooperators among the n-1 opponents. Calculate the cooperation rate among opponents. If this rate meets or exceeds 40%, cooperate in the next round. If the rate falls below 40%, defect in the next round.

**Round r (Final Round):**

Apply the same cooperation-rate threshold (40%), using the cooperation count from round r-1. Maintain the same standard to avoid last-round opportunism, which would undermine benevolence.

**Rationale for Benevolence:**

- **Opening cooperatively** establishes that you are not a pure defector, inviting reciprocal cooperation
- **Reciprocal response** to observed cooperation demonstrates good faith—you reward groups attempting mutual cooperation
- **Threshold at 40%** balances two goals: remaining open to cooperation even when others are divided, while protecting against extreme exploitation (if fewer than 40% cooperate, mutual benefit is degraded)
- **No punishment spirals** occur because you immediately return to cooperation if the group recovers above the threshold, preventing lock-in to mutual defection
- **Consistent final-round behavior** avoids the temptation to exploit on the last turn, preserving the integrity of benevolent signaling
'''

description_BENEVOLENT_24 = '''
# Encouraging Conditional Cooperation with Benevolent Commitment

**DECISION RULES:**

For round t ∈ {1, ..., r}:

1. **Round 1:** Cooperate unconditionally. (Signal benevolence and willingness to initiate cooperation.)

2. **Rounds 2 to r-1 (middle rounds):**
   - Let m_t = number of cooperators observed in round t-1
   - Let cooperation_rate = m_t / n
   - **Cooperate if:** cooperation_rate ≥ (k / n)
   - **Defect if:** cooperation_rate < (k / n)

   Rationale: Cooperate when others' contributions generate positive returns (total k/n per cooperator). Below this threshold, cooperation becomes a net loss to collective welfare, so defect to redirect resources.

3. **Round r (final round):** Cooperate unconditionally. (Benevolent commitment regardless of opponent behavior; no future reputation effects.)

**EDGE CASES AND REFINEMENTS:**

- **First round defection risk:** Cooperate in round 1 even if you expect widespread defection. This tests whether coordination is possible and demonstrates trustworthiness.

- **Threshold interpretation:** The threshold k/n marks where each cooperator receives back at least their contribution in returns. Falling below this means the public good is insufficiently funded to reward cooperation.

- **Persistent defection:** If cooperation_rate remains below k/n across multiple rounds, continue defecting in rounds 2 to r-1. Do not escalate efforts to "save" a group unwilling to reciprocate.

- **Oscillating cooperation:** If cooperation_rate fluctuates around k/n, use a 2-round moving average instead of the single prior round to reduce noise and avoid thrashing between actions.

- **Final round immunity:** Never defect in round r. This preserves benevolence and avoids punishing others in a round where they cannot influence future outcomes.
'''

description_BENEVOLENT_25 = '''
# Benevolent Adaptive Cooperation Strategy

## Core Decision Rule

**Cooperate if and only if:** the proportion of cooperators observed in the previous round is at least β, where β = (k − 1) / (n − 1).

Otherwise defect.

**Rationale:** β is the breakeven threshold. When a fraction β of others cooperate, your expected payoff from cooperating equals your payoff from defecting. Above this threshold, cooperation is individually rational *and* aligns with promoting mutual welfare.

## Edge Cases and Refinements

**Round 1:** Cooperate unconditionally. Benevolence means extending initial good faith.

**Rounds 2 to r−1:** Apply the threshold rule based on the observed number of cooperators C_{t-1} from the prior round:
- If C_{t-1} ≥ β(n−1), cooperate
- Otherwise, defect

**Final round (t = r):** Cooperate if and only if the threshold condition holds. Do not exploit the absence of future rounds; benevolence persists through to the end.

**First-round defection by all:** If no one cooperates in round 1, switch to pure defection for all remaining rounds. After demonstrating good faith, continued unilateral cooperation becomes self-harm, not benevolence.

## Benevolent Design Principles

- **Positive reciprocity:** Cooperate when others reciprocate, creating upward spirals toward welfare-maximizing equilibria.
- **Graceful degradation:** Defect only when cooperation becomes persistently absent, avoiding both naïve exploitation and hair-trigger punishment.
- **Transparency of intent:** The threshold rule is simple and predictable, allowing others to recognize that cooperation invites cooperation in return.
- **Integrity in the endgame:** Maintain cooperation in the final round even when defection is individually advantageous, signaling commitment to collective welfare over selfish gain.
'''

description_BENEVOLENT_26 = '''
## Benevolent Cooperation with Adaptive Reciprocity

**DECISION RULE — Core Strategy:**

Cooperate in round t if and only if the average cooperation rate across all previous rounds meets or exceeds a benevolent threshold. Defect otherwise.

```
If t = 1:
  Action = Cooperate

Else:
  avg_cooperation_rate = (sum of cooperators in rounds 1..t-1) / (n × (t-1))
  
  If avg_cooperation_rate ≥ (1 + k/2) / n:
    Action = Cooperate
  Else:
    Action = Defect
```

The threshold (1 + k/2) / n is calibrated to be above the mutual-defection payoff but substantially below what is needed for mutual cooperation to be optimal, creating space for gradual recovery from low cooperation without naive exploitation.

**EDGE CASES:**

- **First round**: Always cooperate. Signal benevolent intent unconditionally.

- **Last round (round r)**: Apply the same decision rule without adjustment. Do not defect simply because the game ends; this preserves integrity.

- **If all players defect in early rounds**: Continue applying the threshold rule. If cooperation remains near zero, defect. However, if any recovery in cooperation is detected (even if small), resume cooperation to enable restart.

- **Sustained low cooperation (rounds where avg < threshold)**: Defect persistently until average recovers. This is necessary to avoid infinite exploitation, but defection acts as a gentle signal rather than harsh punishment.

**BENEVOLENT ALIGNMENT:**

This strategy embodies benevolence by:
- Leading with unconditional cooperation to establish good faith
- Using historical averages rather than single-round response, thereby forgiving isolated defections and noise
- Maintaining cooperation as long as the group shows any meaningful commitment to mutual benefit
- Refusing to exploit a last round—cooperation is its own ethical anchor
- Calibrating the threshold to reward group-level cooperation even when imperfect, rather than demanding perfection
'''

description_BENEVOLENT_27 = '''
# Benevolent Conditional Cooperation Strategy

**CORE DECISION RULE:**

In round t (t ≥ 2), let m(t-1) denote the number of other players observed to have cooperated in round t-1. Let the observed cooperation rate among opponents be ρ(t-1) = m(t-1) / (n-1).

- **Cooperate in round t if:** ρ(t-1) ≥ θ(t)
- **Defect in round t if:** ρ(t-1) < θ(t)

where the threshold θ(t) is dynamically set:

**θ(t) = base_threshold − early_discount + end_game_premium**

Concretely:
- **Rounds 2 to r-2 (mid-game):** θ(t) = k/n (cooperate if others match or exceed the benefit they receive from my cooperation)
- **Round 1 (opening):** Play C unconditionally (establish benevolent intention and give others a chance to respond)
- **Rounds r-1 and r (end-game):** θ(t) = (k/n) − 0.1 (lower threshold by ~10% in final rounds; attempt to restore cooperation despite potential exploitation)

**EDGE CASES:**

- **First round:** Always cooperate.
- **Second round:** Use m(1) = number of cooperators in round 1. Cooperate if m(1)/(n-1) ≥ k/n.
- **Last round:** Cooperate if the 5-round rolling average of observed opponent cooperation ≥ (k/n) − 0.1, or if this is the last chance to cooperate and average cooperation has been ≥ 0.3. (Prioritize a final gesture of cooperation to encourage reciprocal ends.)
- **All others defect throughout:** Defect from round 3 onward (do not throw away payoff against a completely non-cooperative field).
- **Oscillating opponents:** If cooperation rate swings wildly between rounds, use the most recent round as the signal; do not assume pattern stability.

**BENEVOLENCE ALIGNMENT:**

- Opening unconditional cooperation signals trustworthiness and invites reciprocal cooperation.
- Threshold of k/n ensures I defect only when my cooperation's value to the collective clearly exceeds the private cost and yet others have not matched that investment.
- End-game relaxation (threshold reduction) prioritizes collective recovery and fairness over my final-round exploitation potential—I sacrifice potential last-round defection gains to reward and encourage mutual cooperation.
- The strategy avoids punitive spirals: I never retaliate with escalating defection; I simply match the revealed cooperation level against a generous benchmark.
'''

description_BENEVOLENT_28 = '''
# Benevolent Adaptive Conditional Cooperation

**Decision Rule by Round:**

*Round 1:* Unconditionally cooperate. Establish good faith and signal benevolence.

*Rounds 2 to r-1:*
- Compute the cooperation rate from the previous round: `prev_coop_rate = (cooperators_in_prev_round) / n`
- Calculate the dynamic threshold: `θ(t) = 0.50 - 0.08 × (t / r)`
  - This threshold begins at 50% and gradually loosens as rounds progress, staying generous throughout
- Compare observed cooperation to threshold:
  - If `prev_coop_rate ≥ θ(t)`: **Cooperate**
  - If `prev_coop_rate < θ(t)`: 
    - Check trend: compute the cooperation rate from the last two rounds combined
    - If trend is improving (cooperation climbing): **Cooperate with probability 0.7**, defect with probability 0.3
    - If trend is flat or declining: **Defect**

*Round r (final round):*
- Compute average cooperation across all completed rounds: `avg_coop_rate = (total_cooperators_across_all_rounds) / (r - 1) / n`
- If `avg_coop_rate ≥ 0.35`: **Cooperate** (benevolent signal regardless of exploitation risk)
- Else: **Defect** (only withdraw if cooperation is substantially absent)

**Rationale:**

This strategy embodies benevolence by (1) always opening with cooperation, (2) maintaining optimistic thresholds that reward moderate cooperation, (3) looking for improvement trends before abandoning partners, and (4) giving a final cooperative signal if there's any meaningful history of reciprocation. It is robust because it defects when facing consistent defectors, protecting against one-sided exploitation, while remaining adaptive by conditioning decisions on observed aggregate behavior rather than fixed rules.
'''

description_BENEVOLENT_29 = '''
**Benevolent Adaptive Cooperation with Generous Threshold**

**Decision Rules:**

1. **Round 1**: Cooperate unconditionally.

2. **Rounds 2 through r**: 
   - Observe c_prev = the count of cooperators in round (t-1)
   - Calculate threshold = ceil(n × 0.3) — this represents 30% of the player population
   - If c_prev ≥ threshold: Cooperate
   - If c_prev < threshold: Defect

3. **Last round (t = r)**: Apply the same decision rule above — do not shift to pure defection opportunistically.

**Edge Cases:**

- **First round with any n**: Cooperate. This signals benevolent intent regardless of parameters.
- **Threshold computation**: Use ceiling to ensure c_prev = 1 player cooperating (plus yourself) meets the threshold when n is small. For large n, the 30% floor ensures you don't require an implausibly high bar.
- **When r = 2**: The second round uses standard decision logic; do not treat it as "end-game" by switching strategy.

**Benevolent Alignment:**

This strategy embodies benevolence through:
- **Unconditional opening**: Lead with cooperation, extending trust without precondition.
- **Generous threshold**: Maintain cooperation even when only ~30% of others reciprocate. This avoids the trap of conditional tit-for-tat escalation into mutual defection.
- **No late-round exploitation**: In the final round, continue applying the same threshold rather than defecting to capture private value. This resists the temptation to exploit when future consequences disappear.
- **Robustness without naivety**: Defection only triggers when defection becomes dominant (< 30% cooperation), preventing systematic exploitation by coordinated free-riders while remaining responsive to bad-faith opponents.
- **Parameter-independent fairness**: The 30% threshold scales uniformly across group sizes, avoiding bias toward larger or smaller player pools.
'''

description_BENEVOLENT_30 = '''
# Benevolent Adaptive Threshold Strategy

## Decision Rules

**Round 1:**
Cooperate. This establishes goodwill and tests whether the group has any cooperative inclination.

**Rounds 2 through r-1 (Middle rounds):**

Let `prev_coop_rate` = (number of cooperators in round t-1) / n

- If `prev_coop_rate ≥ 0.5`: **Cooperate**
  - The group is cooperating; match their behavior and reinforce the cooperative equilibrium.

- If `0.4 ≤ prev_coop_rate < 0.5`: **Cooperate**
  - Still a reasonable cooperation signal; maintain optimism and give the group the benefit of doubt.

- If `0.25 ≤ prev_coop_rate < 0.4`: **Defect**
  - Cooperation is insufficient; defect this round to signal disapproval and reduce losses. This is punitive but recoverable if the group course-corrects.

- If `prev_coop_rate < 0.25`: **Defect**
  - The group is predominantly defecting; don't contribute. Recover your endowment until cooperation becomes viable again.

**Final Round (round r):**

Let `avg_coop_rate` = average cooperation rate across all previous rounds

- If `avg_coop_rate ≥ 0.35`: **Cooperate**
  - Even in the final round with no future reputational consequences, cooperate if the group showed meaningful cooperative effort over time. This honors the group's benevolent history.

- If `avg_coop_rate < 0.35`: **Defect**
  - The group has demonstrated insufficient cooperation. Since there is no future interaction, cooperation yields no strategic benefit.

## Edge Cases

**Tied cooperation rate (e.g., exactly 0.5):** Treat as meeting the threshold for cooperation.

**All opponents defect throughout:** Defect consistently to preserve endowment. The strategy will not be exploited indefinitely.

**One very high cooperation followed by collapse:** Remain at the initial threshold (0.4-0.5) for one additional round before escalating to defection, allowing for noise or strategic shifts.

**Two-player variant (n=2):** Same thresholds apply; 0.5 cooperation rate means the opponent cooperated.

## Benevolence Alignment

This strategy embodies benevolence through:

1. **Optimistic opening:** Cooperate first, assuming others may be benevolent too.
2. **Generous thresholds:** Cooperate even when cooperation rate is only 40-50%, not requiring unanimity.
3. **Proportional punishment:** Defection is temporary and signaling, not vindictive. If cooperation resumes, the strategy quickly returns to cooperation.
4. **Final-round grace:** Cooperate in the last round if the group showed reasonable cooperative effort, prioritizing the collective good over personal gain even when there is no reputational return.
5. **No exploitation:** Defection occurs when the group predominantly free-rides, preventing the strategy from being a permanent sucker. Recovery is always possible if opponents change behavior.
'''

description_BENEVOLENT_31 = '''
# Benevolent Cooperative Threshold Strategy

**Tracking:** Maintain a cumulative count of how many times opponents cooperated in each observed round.

**Decision Rule by Round:**

*Round 1:* 
Cooperate. Signal benevolent intent to establish a cooperative environment.

*Rounds 2 to r−1 (middle rounds):*
Calculate the average cooperation rate from all previous rounds:
```
avg_coop_rate = (total cooperators observed so far) / (total opponent-rounds observed so far)
```
- If `avg_coop_rate ≥ 0.35`, Cooperate
- If `avg_coop_rate < 0.35`, Defect

The 0.35 threshold balances pragmatism: it requires a meaningful fraction of others to cooperate before you invest further, protecting against exploitation while remaining optimistic.

*Round r (final round):*
Cooperate unconditionally. Benevolence means not exploiting the endpoint when others might still be cooperative, and signaling that your cooperation was genuine rather than strategic.

**Rationale for Benevolence:**

- **Initial cooperation** creates the possibility of mutual benefit and demonstrates trustworthiness
- **Adaptive defection** when cooperation drops below the threshold avoids being a consistent victim of free-riding while remaining responsive to genuinely cooperative groups
- **Threshold level** is low enough to forgive honest attempts at coordination that don't achieve majority participation, avoiding premature punishment spirals
- **Final round cooperation** refuses to exploit the end-game, treating the last round as a moment to affirm collective welfare rather than maximize individual extraction

**Edge Case — If n = 2:** Apply the same logic; defect only in rounds 2−r−1 if the single opponent cooperated less than 35% of the time (i.e., defected in previous rounds).
'''

description_BENEVOLENT_32 = '''
**Benevolent Reciprocity Strategy**

**Initialization:**
Track aggregate cooperation history:
- total_opponent_cooperations = 0
- total_opponent_decisions = 0

**Round 1:**
Action: Cooperate
Update: total_opponent_decisions += (n - 1)
Update: total_opponent_cooperations += (number of opponents who cooperated)

**Rounds 2 to r-1 (midgame rounds):**
- Compute: opp_coop_rate = total_opponent_cooperations / total_opponent_decisions
- If opp_coop_rate ≥ 0.35: Cooperate
- Else: Defect
- Update tracking variables with observed cooperation count

**Round r (final round):**
- Compute: opp_coop_rate = total_opponent_cooperations / total_opponent_decisions
- If opp_coop_rate ≥ 0.20: Cooperate
- Else: Cooperate (always cooperate in final round unless opponents showed near-zero cooperation)

**Edge Cases:**

*Threshold rationale:* Use 0.35 threshold for midgame (expects roughly one-third of opponents to cooperate, which is benevolently generous given the k < n structure makes individual defection strictly better). Use 0.20 in final round to remain cooperative even if cooperation is struggling, since defecting in the last round is a signal that cooperation was hopeless—benevolence assumes we tried good faith.

*First round defection:* If all opponents defect in round 1, opp_coop_rate becomes 0.0, triggering defection from round 2 onward. Accept this gracefully—benevolence means responding to actual opponent strategy, not ignoring reality.

*Fractional cooperations:* Round always to nearest integer when needed. If uncertainty, favor cooperation.

**Rationale for benevolence:**
This strategy establishes cooperation first, reciprocates sustained cooperation from opponents, forgives sporadic defection through generous thresholds, and terminates cooperation only after clear evidence opponents have abandoned it. The final round remains cooperative to prevent mutually-destructive spirals and maintain the benevolent principle that cooperation is attempted even when individually suboptimal.
'''

description_SELFISH_5 = '''
# Selfish Threshold Exploitation Strategy

## Decision Rule

**By default: Always defect (D)**

In round t, defect unless the following conditions hold simultaneously:
1. t < r (not the final round)
2. Observed cooperation rate in round t-1 satisfies: m_{t-1}/n > k/n (cooperators exceed the public good multiplier threshold)
3. t > 1 (we have at least one observation)

Even when conditions hold, cooperate only if: the marginal benefit (k/n) visibly exceeds 1 - (k/n), which requires m_{t-1} > n - k.

Otherwise: defect.

## Edge Cases

**Round 1**: Defect unconditionally. This establishes your baseline and generates the first observation of opponent behavior without commitment.

**Round r (final round)**: Always defect, regardless of history. No future rounds exist to reward cooperation or punish defection, so the dominant strategy strictly applies.

**Low cooperation regimes**: If you observe m_t < k consistently across rounds, continue defecting. Cooperation is economically unviable—your contribution yields subunit returns even if the entire public good were distributed to you alone.

**High cooperation regimes**: If you observe m_t ≥ n - 1 (nearly universal cooperation), you still defect. These cooperators cannot identify and conditionally reciprocate with you specifically (you are anonymous). Your defection extracts maximum value from their contributions without credible consequence.

## Selfish Reasoning

Defection is a dominant action: it yields 1 more payoff than cooperation in every round, unconditionally. Cooperation can only be justified if it credibly influences future opponent strategies, but:
- You cannot communicate intent
- You are anonymous across rounds (opponents cannot reward or punish you individually)
- Opponents play independently without shared norms

Thus, any cooperation is unilateral sacrifice. Exploiting others' cooperation by defecting while they contribute maximizes your individual payoff across all rounds. The rare exception—cooperating when cooperation is nearly universal—still leaves you better off defecting to capture the public good at zero cost.
'''

description_SELFISH_6 = '''
## Selfish Adaptive Defection Strategy

**Core Decision Rule:**
Always defect. Since k < n, defection weakly dominates cooperation in all rounds regardless of others' contributions.

Formal check: For any round where m of the other n-1 players cooperate,
- Payoff(Defect) = 1 + (k/n) × m
- Payoff(Cooperate) = (k/n) × (m + 1)

Defect is superior when 1 > k/n, which holds since k < n.

**Round-by-Round Behavior:**

Round 1: Defect (no prior information; defection is strictly safe and selfish)

Rounds 2 through r-1: Defect. Simultaneously, observe and track the cooperation count m_t from the previous round. Use this to estimate opponent type distribution:
- If m_t > (n-1) × 0.5: Likely high proportion of conditional cooperators
- If m_t < (n-1) × 0.3: Likely high proportion of defectors
- Record this trend across rounds

Round r (final): Defect (no future payoffs; strict dominance)

**Edge Case Handling:**

Early rounds (t < r/3): Maintain pure defection. Do not signal cooperation even if observing high cooperation, as there is no benefit to building reputation.

Late rounds (t > 2r/3): Maintain pure defection. Continue defecting even if observing declining cooperation, as exploitation is over before punishment mechanisms activate.

Middle game divergence (r/3 < t < 2r/3): If observed cooperation rate increases above 70% and r > 4, you may cooperate in exactly one round as a test for exploitability—defect immediately following, regardless of outcome. This tests whether conditional cooperators respond to a single defection (indicating future exploitability) or forgive it.

**Robust Variants for Uncertain k:**

If k is near n (close to interior equilibrium), add: Defect with probability (k-1)/(n-k) and cooperate with probability 1 - (k-1)/(n-k) each round. This optimizes against uniformly random opponents while remaining selfish.

If r is very large (r > 20), occasionally (once every 10 rounds) defect in streak to reset others' conditional cooperation toward you.
'''

description_SELFISH_7 = '''
# Adaptive Threshold Reciprocity with End-Game Defection

**Round 1**: Always defect. No history exists to condition upon.

**Rounds 2 through r−1**: Use conditional cooperation based on observed opponent behavior from the previous round.
- Let m = count of opponents who cooperated in round t−1
- Let θ = max(1, ⌊k⌋) [the threshold]
- If m ≥ θ, cooperate in round t
- If m < θ, defect in round t

**Round r (final round)**: Always defect. No future rounds remain where opponent reciprocation could benefit me, so defection is strictly superior.

**Threshold rationale**: The threshold θ = ⌊k⌋ captures the minimum number of opponents whose contributions make cooperation worth my participation. Since (k/n) per contributor, requiring roughly k opponents cooperating approximates the break-even where the public good return justifies the endowment cost. This is selfish: I cooperate only when the expected public good payoff is substantial.

**Edge cases**:
- If n = 2 and k ≤ 1: Threshold floors to 1, meaning defect only if the single opponent defects. This is appropriate since one cooperator's contribution multiplied by k still provides decent benefit.
- If r = 2: Round 1 defects, round 2 defects (last round rule). Outcome is full defection regardless of opponent type.
- If all opponents defect in round 1: m = 0 < θ, triggering cascade of mutual defection from round 2 onward. I match the environment rather than waste endowment.
- If opponents gradually reduce cooperation: Threshold rule naturally shifts me toward defection, avoiding costly reciprocation that isn't reciprocated.

**Selfish alignment**: This strategy never cooperates when rational not to (defects in round 1 and round r unconditionally). It only cooperates in middle rounds when others demonstrate sufficient contribution, allowing me to free-ride on the aggregate public good while conditioning my participation. The approach maximizes my payoff against both pure-defect and conditional-cooperate opponents by exploiting cooperation when present and avoiding losses when absent.
'''

description_SELFISH_8 = '''
# Selfish Threshold Cooperation Strategy

## Core Decision Rule

**Always defect by default.** Mathematically, defection strictly dominates cooperation in every round: a cooperator gets (k/n)(m+1) while a defector gets 1 + (k/n)m, and the latter always exceeds the former since k < n.

However, implement a single condition to exploit large pools of cooperators:

- **Rounds 1 to r-1:** If m ≥ ⌈(n-1)·(1 - δ)⌉ observed cooperators in the previous round, cooperate this round. Otherwise defect.
  - Use δ = (n - k)/(n-1) as your threshold parameter. This adapts to game parameters automatically.
  - This triggers only when cooperation is widespread enough that the public good return (k/n)·m is substantial.

- **Round r (final round):** Defect unconditionally. Exploit the maximum and extract your private endowment since no future punishment is possible.

## Handling Round 1 (No History)

Defect. You have no information about opponent tendencies and defection is the safe baseline that cannot be exploited.

## Edge Cases

- **If all others defect (m=0):** Defect. You gain nothing from joining an empty commons.
- **If all others cooperate (m=n-1):** Cooperate in rounds 2 through r-1 only. The public good return k(n)/(n) = k > 1 exceeds your private endowment of 1, making defection suboptimal.
- **Last round (t=r):** Strictly defect regardless of history. No future rounds exist to establish reputation or be punished, so the threshold strategy's deterrent value vanishes.

## Selfish Justification

This strategy prioritizes maximizing your absolute payoff. It extracts value from cooperative pools when they exist (rounds 2 through r-1) but avoids being a chump donating to empty commons. The final-round defection reclaims all potential gains that cooperation would forfeit. The threshold is calibrated so you only cooperate when cooperation genuinely improves your immediate payoff relative to defection.
'''

description_SELFISH_9 = '''
## Selfish Defection with Adaptive Observation

**Primary Decision Rule: Always Defect**

Play D in every round, including round 1 and round r. Defection dominates cooperation in every decision node regardless of what others have done or will do. For any fixed level of aggregate cooperation from opponents, your payoff is strictly higher when you defect rather than cooperate:
- If m opponents cooperate: payoff(D) = 1 + (k/n)×m vs payoff(C) = (k/n)×(m+1)
- Difference: payoff(D) − payoff(C) = 1 − k/n > 0, since k < n.

This holds in all rounds, including the first (where you have no history) and the last (where there is no future).

**Adaptive Observation Layer**

While always defecting, track the observed cooperation count c_t in each round t:

```
cooperation_history = [c_1, c_2, ..., c_{t-1}]
avg_cooperation = mean(cooperation_history)
defection_rate = (n - avg_cooperation) / n
```

Use this information to:
- Confirm that defection remains optimal (high defection rate from opponents validates the strategy)
- Detect if anomalously high cooperation persists (indicating you're exploiting naive/error-prone opponents—continue exploiting)
- Detect if cooperation drops to near-zero (confirming others are also selfish—continue defecting as mutual defection is Nash equilibrium)

**No decision node changes based on history.** The observation is informational only; it doesn't alter the action because defection is always better. Adaptation means you understand *why* defection works across different opponent compositions, not that you switch strategies.

**Edge Case Handling**

- **Round 1**: Defect. No history exists; defection is safe and dominant.
- **Round r**: Defect. There are no future rounds in which to influence opponent behavior, so defection's advantage is undiminished.
- **Unknown n, r, k**: Defect unconditionally. The dominance argument requires only k < n, which is given.
'''

description_SELFISH_10 = '''
# Adaptive Threshold Cooperator Strategy

**Decision Rule:**

Let cooperation_threshold = max(2, ceil(n/k))

```
round == 1:
  action = DEFECT

1 < round < r:
  if (cooperators_in_previous_round >= cooperation_threshold):
    action = COOPERATE
  else:
    action = DEFECT

round == r:
  action = DEFECT
```

**Rationale for threshold:**

The threshold is set at ceil(n/k) because:
- When n-1 others cooperate and I cooperate, I earn (k/n) × n = k total
- When that many others cooperate and I defect, I earn 1 + (k/n)(n-1) ≈ 1 + k - k/n
- At lower cooperation levels, the public good provides negligible benefit, so defection's +1 private payoff dominates

**Edge cases:**

- **Round 1:** Defect unconditionally to probe opponents and establish that I'm not an automatic cooperator who can be exploited
- **Last round (r):** Always defect. Since no future round exists, opponents cannot punish defection through lower future cooperation. Cooperation provides no direct benefit.
- **Threshold crossing:** When observing exactly at threshold (e.g., if cooperation_threshold = 2 and exactly 2 others cooperated), cooperate. This is the break-even point where the public good becomes sufficiently valuable.

**Selfish properties:**

- I only cooperate in the middle rounds when I observe sufficient prior cooperation—i.e., when others have already demonstrated they'll fund the public good that benefits me regardless
- I defect when cooperation is sparse, preserving the +1 private payoff when the public good is too small to be attractive
- I defect in the final round, eliminating any cost from foregone private payoff with zero reputational consequence
- The strategy exploits any opponent who cooperates unconditionally by defecting in round r, while punishing unconditional defectors by defecting throughout
'''

description_SELFISH_11 = '''
# GREEDY EXPLOITATION WITH ADAPTIVE THRESHOLDING

**Core Decision Rule:**

Always defect. Defection strictly dominates cooperation in every round regardless of opponent actions, since the payoff gap (1 + km/n) − (k(m+1)/n) = n − k > 0 is always positive.

**Adaptive Mechanism:**

Maintain a running record of cooperation rates observed in each round. Calculate a rolling average: avg_coop = (total cooperators observed so far) / (total rounds played so far).

Use this information not to change defection behavior, but to calibrate exploitation timing:

1. **Rounds 1 to r−1 (non-terminal):**
   - Always defect
   - Observe the number of cooperators and track avg_coop
   - If avg_coop consistently exceeds (k/n), this indicates a vulnerable opponent pool—continue exploiting through consistent defection

2. **Round r (final round):**
   - Defect unconditionally
   - No future consequences exist, so any remaining reliance on reciprocity collapses

**Edge Cases & Commitment:**

- **Round 1:** Defect (no history to inform decisions, and defection is unconditionally optimal)
- **Very low observed cooperation (avg_coop < k/(2n)):** Maintain defection; opponents are already minimizing public goods provision
- **High observed cooperation (avg_coop > (n−k)/n):** Maintain defection; this is maximum profitable free-riding opportunity
- **Sudden spikes in cooperation:** Irrelevant to action choice; continue defecting; aggregate signal alone is insufficient to warrant cooperation

**Rationale:**

This strategy maximizes personal payoff by exploiting whatever cooperation patterns emerge while remaining robust to all opponent configurations. Defection is the dominant action; adaptation serves only to confirm that the environment justifies continued exploitation rather than to change the core behavioral commitment.
'''

description_SELFISH_12 = '''
SELFISH THRESHOLD RECIPROCITY STRATEGY

**Core Decision Rule:**

In round t, cooperate if and only if:
- t < r (not the final round), AND
- m_{t-1} > n/k, where m_{t-1} is the number of observed cooperators in round t-1

Otherwise, defect.

**Round 1 Handling:**

Cooperate in round 1. This serves two purposes: (1) signal potential willingness to extract gains from the public good if others cooperate, and (2) test the aggregate cooperation level that emerges.

**Last Round:**

Defect in round r. No future rounds to influence cooperation patterns, so the backward induction argument applies: keep the endowment.

**Threshold Justification:**

The threshold n/k represents the breakeven point. If more than n/k players contributed in the previous round, the expected public good share (k/n) × m_{t-1} exceeds 1, making cooperation payoff-competitive with defection. Below this threshold, cooperation yields strictly less than defection, so defect.

**Adaptive Mechanism:**

Track m_t across rounds. If cooperation rises above n/k, switch to cooperative. If it drops back below n/k, revert to defection. This exploits periods of high cooperation while protecting against free-riding when cooperation is sparse.

**Edge Case — Tied Threshold:**

If m_{t-1} = n/k exactly, defect. Equality means the public good payoff equals the private payoff of keeping the endowment; defection is weakly better and avoids exploitation risk.
'''

description_SELFISH_13 = '''
# Adaptive Defection Strategy

**Core Decision Rule:**

Always defect. For any round t, play D regardless of observed opponent cooperation in prior rounds.

**Rationale for Selfish Dominance:**

In each round, defection strictly dominates cooperation because:
- Payoff(Defect) - Payoff(Cooperate) = 1 - (k/n) > 0
- Since k < n, this difference is always positive
- This holds regardless of how many opponents cooperate

No information about opponent behavior changes this inequality.

**Adaptation Mechanism:**

While the decision rule never changes, track the observed cooperation rate each round: m_t = total cooperators observed in round t.

Use this to calibrate expectations about future rounds, but do not change behavior:
- If m_t is high: expect opponents are cooperative types; continue defecting to extract maximum value
- If m_t is low: expect opponents are defectors too; continue defecting as they will
- Update posterior belief about opponent strategy distribution, but exploit it via defection, not reciprocation

**Edge Cases:**

1. **Round 1 (first round):** Defect. You have no history; defection is unconditionally optimal.

2. **Round r (last round):** Defect. No future interaction remains to justify cooperation. Terminal round incentives are identical to all others.

3. **Intermediate rounds:** Defect. The repeated structure doesn't create incentive to cooperate because you cannot identify or punish specific defectors (anonymous observation only).

**Information Use:**

Observation of cooperation counts informs your model of the opponent population (some fraction are conditional cooperators, some are constant defectors) but does not inform your action choice, since defection dominates against any mixture of opponent types.
'''

description_SELFISH_14 = '''
**THRESHOLD EXPLOITATION STRATEGY**

**Core Decision Rule:**

In round t, cooperate if and only if the observable cooperation level from the previous round meets a threshold that makes cooperation individually rational relative to defection.

**Precise Implementation:**

1. **Round 1 (first round):** Defect. No history exists, and defection is the selfish baseline.

2. **Rounds 2 through r-1 (middle rounds):**
   - Observe c = number of cooperators in round t-1
   - Calculate breakeven: cooperation yields (k/n)(c+1); defection yields 1 + (k/n)c
   - Since k < n, the inequality (k/n)(c+1) > 1 + (k/n)c reduces to k > n, which is never satisfied
   - **Therefore: Always defect**
   
3. **Round r (final round):** Defect unconditionally. Even if others cooperate, there is no future period to punish defection, making exploitation optimal.

**Selfish Rationale:**

Defection strictly dominates cooperation in every single round. Mathematically, choosing C generates payoff (k/n)(c+1) while choosing D generates payoff 1 + (k/n)c. The difference is (k/n) - 1 = (k-n)/n < 0, making defection always preferable regardless of others' actions.

**Adaptive Element:**

Monitor the cooperation count after each round. If the count is unusually high (indicating potential slack that could be exploited further) or low (confirming others are selfish), this informs the reliability of pure defection—in both cases, defection remains optimal, but the adaptive observation reinforces the decision.

**Edge Case - Early Termination:**

If the game ends unexpectedly before round r, defect in that final round.
'''

description_SELFISH_15 = '''
**Selfish Threshold Opportunist with Endgame Defection**

**Round 1:**
Defect. You have no history to condition on; establish from the start that you will prioritize self-interest over collective gain.

**Rounds 2 to (r-1):**
Observe the count of cooperators from the previous round, denoted c_prev.

- If c_prev ≥ ceil(k/n × n) = ceil(k), cooperate.
- Otherwise, defect.

**Final round r:**
Defect unconditionally. No future payoffs exist to influence, so cooperation yields strictly lower payoff.

**Threshold justification:**
The threshold k is chosen conservatively. If at least k others cooperate, the public good return (k/n × k) approaches your private benefit from defection (1). Only in these high-cooperation scenarios does cooperating avoid being badly exploited. In all other cases, defecting guarantees the 1-unit private payoff plus whatever public goods return emerges from others' contributions.

**Adaptation mechanism:**
This strategy treats each round's cooperation count as a signal of opponent willingness to cooperate. High observed cooperation in round t suggests conditional cooperators exist in the population; matching their behavior in round t+1 allows you to share in the multiplied pool while they're cooperating. Low cooperation signals that others are defecting, so you defect to avoid being the sole contributor.

**Edge case - small n or low k:**
If k < 1, the threshold becomes 0. In this case, always defect (defecting is strictly optimal even against universal cooperation). If k ≥ n-1, this strategy may cooperate frequently; recalibrate by setting threshold to max(1, ceil(k)), ensuring you only cooperate when sufficiently many others do.

**Selfish alignment:**
You always move toward higher individual payoff given observed behavior. You exploit cooperative populations but punish defection with defection. You abandon cooperation in the endgame where it cannot trigger reciprocal returns.
'''

description_SELFISH_16 = '''
# SELFISH THRESHOLD-RESPONSE STRATEGY

## Decision Rules

**Core principle:** Cooperate only when opponent behavior indicates sufficient aggregate participation to exceed the breakeven point for contribution.

**Breakeven threshold calculation:**
- For cooperation to yield equal or better payoff than defection in the current round, you need other players' actions to signal a viable public good
- Empirically treat cooperation as worthwhile only when observed cooperation in the prior round exceeded a participation threshold
- Compute threshold T = ceil((n - 1) / k) - this is the minimum number of other players who must have cooperated to make your cooperation worthwhile in response

**Round-by-round decisions:**

- **Round 1:** Cooperate. Exploration phase—gather information about opponent pool without cost.

- **Rounds 2 through r-1:** Cooperate if and only if `observed_cooperators_last_round ≥ T`. Otherwise, defect.

- **Round r (final round):** Defect unconditionally. No future payoff to harvest; pure defection maximizes immediate return.

## Edge Cases and Refinements

- **If T ≥ n:** Defect from round 2 onward. The threshold cannot be met, so cooperation is never rational.

- **Early convergence:** If you defect in round t and observe zero cooperators in round t+1, maintain defection for all remaining non-final rounds (opponent behavior confirms non-reciprocation).

- **Exploitation safeguard:** If you cooperate in round t and observe fewer cooperators in round t+1 than in round t, defect in round t+1. This signals that cooperation is being systematically exploited.

## Selfish Alignment

This strategy extracts maximum value by:
- Avoiding the sucker's payoff (cooperating to feed unilateral defectors)
- Parasitizing cooperative populations when they exist (riding the public good they create)
- Withdrawing instantly when cooperation becomes unprofitable relative to defection
- Defecting in the endgame when future reciprocation is impossible
'''

description_SELFISH_17 = '''
**Unconditional Defection with Information Gathering**

Cooperate: Never.

Defect in every round, including round 1 and round r.

**Decision Rule:**

For all t ∈ {1, 2, ..., r}, play D.

The rationale is mechanical: Given k < n, the per-capita return from the public good is k/n < 1. This means your private payoff from keeping your endowment (1) exceeds your share of any contribution you make. Specifically, if you cooperate, you receive 0 + (k/n) × (others' contributions + 1). If you defect, you receive 1 + (k/n) × (others' contributions). The defection payoff is always higher by 1 - k/n > 0, regardless of how many others cooperate.

**Edge Cases:**

- Round 1: Defect. You have no history and must make a baseline choice. Defection is strictly dominant.
- Last round (round r): Defect. There are no future rounds in which others' behavior can be influenced, so the repeated-game logic evaporates. Defection is optimal.
- All intermediate rounds: Defect. The mathematical advantage of defection persists in every single round.

**Information Use:**

Observe the number of cooperators each round (m_t), but do not condition your action on this. The observation is useless for a purely selfish player: even if all others cooperated, your best response is still to defect. Even if all others defected, defecting remains superior to cooperating (you avoid the loss of your endowment while capturing no public good return).

**Why No Conditional Cooperation:**

In principle, you could consider "cooperate if m_t is large" as an exploitation strategy. But the arithmetic forbids it: cooperating costs you 1 and gains you at most k/n < 1 in public goods share, a losing trade at any observed cooperation level.
'''

description_SELFISH_18 = '''
**CONDITIONAL DEFECTION WITH THRESHOLD COOPERATION**

Decision rule:

```
For round t ∈ {1, 2, ..., r}:
  
  if t == r (final round):
    Play D
  
  else if t == 1 (first round):
    Play D
  
  else:
    Let c[t-1] = number of cooperators observed in round t-1
    
    if c[t-1] ≥ ceil(k):
      Play C
    else:
      Play D
```

**Rationale:**

Last round is always defect—no future consequences exist, so capturing the full endowment strictly dominates.

First round is defect—establishes a baseline payoff and provides information without commitment. You keep 1 and observe how many others cooperate despite your defection.

Middle rounds are threshold-conditional: cooperate only when the observed cooperation level from the previous round suggests the public good pool is likely substantial enough to justify sacrificing your private endowment.

The threshold ceil(k) targets when the returned share (k/n) × c[t-1] approaches or exceeds 1. If at least k others cooperated, the public good surplus k × (k/n) = k²/n is available for capture. Cooperating locks in your share of this realized pool while remaining selfish—you're exploiting the cooperation already committed last round, not subsidizing future uncertainty.

**Edge case handling:**

If observation reveals c[t-1] = 0 for two consecutive rounds, defection continues indefinitely through round r-1. The threshold creates a natural trap exit: cooperation stops when others stop, preventing mutual exploitation spirals that would reduce your payoff below constant defection.

If cooperation spikes to n-1 (everyone else cooperates), the strategy cooperates and captures maximum public good returns—this is pure self-interest, not altruism.
'''

description_SELFISH_19 = '''
# Selfish Adaptive Strategy

## Decision Rules

**Always defect, with selective conditional cooperation:**

For each round t:

```
If t == 1:
  Play D

Else if t == r (final round):
  Play D

Else (rounds 2 through r-1):
  Let m = number of opponents who cooperated in round t-1
  Let efficiency_threshold = k/n
  
  If m ≥ (n-1) × 0.7 AND (k/n) × m > 0.5:
    // High cooperation observed; cooperation payoff is material
    Play D  [defection still best-response, but noted as temptation]
  Else:
    Play D
```

**Rationale for pure defection:** In any single round, defection yields 1 + (k/n) × m, while cooperation yields (k/n) × (m+1). Since k < n, the difference 1 - k/n is always positive, making defection the best response regardless of opponent behavior. This holds for all non-final rounds.

## Edge Cases

**Round 1:** Start with defection. This is the Nash equilibrium baseline and reveals whether opponents employ "nice" strategies.

**Final round (round r):** Defect unconditionally. No future interactions exist, eliminating any forward-looking incentive to cooperate or maintain reputation.

**Extreme cases:**
- If n-1 opponents all cooperate: Defect and capture payoff of 1 + k
- If no opponents cooperate: Defect and secure baseline payoff of 1
- If exactly (n-1) × (k/n) opponents cooperate: Defect still yields more than cooperation

## Selfish Alignment

This strategy prioritizes immediate payoff maximization. It never intentionally forgoes a higher-payoff action to influence opponent behavior or encourage cooperation. The conditional cooperation logic in middle rounds acknowledges high-cooperation environments but doesn't override the dominant action—it simply documents the structural incentive. Defection remains optimal against any empirical distribution of opponent types because the dominant strategy equilibrium cannot be exploited.
'''

description_SELFISH_20 = '''
# Selfish Adaptive Strategy: Threshold-Based Defection with Contingent Cooperation

## Core Decision Rule

**Cooperate in round t if and only if:**

```
(k/n) * observed_cooperators_in_round_t−1 > 1 − ε
```

**Otherwise, defect.**

Where ε is a small exploration parameter (e.g., 0.01). For most game parameters satisfying 1 < k < n, this condition will be false, making defection the persistent strategy.

## Edge Cases and Detailed Rules

**Round 1:** Defect. With no history, assume zero cooperation from opponents. Since receiving k/n from cooperators must exceed the cost of foregoing 1 to justify cooperation, and k < n guarantees k/n < 1, the threshold is unmet.

**Rounds 2 to r−1 (middle rounds):** After observing m cooperators last round:
- If m > n(1 − k/n) = n − k, cooperate (others' contributions are substantial enough)
- Otherwise, defect

**Last round (round r):** Defect unconditionally. No future interactions remain; the repeated-game incentive to condition behavior on future punishment evaporates. Pure payoff maximization in the final period demands defection.

## Selfish Alignment

This strategy is selfish because:

1. **Defection is outcome-dominant.** In any round where m opponents cooperate, defecting yields 1 + (k/n)m, while cooperating yields only (k/n)(m+1). Since k < n, defecting always yields 1 − k/n > 0 additional payoff.

2. **History-conditioned behavior exploits cooperation.** If you observe cooperators last round, you extract their contribution without reciprocating.

3. **Abandons cooperation at journey's end.** The last-round defection reflects pure self-interest unconstrained by reputation or reciprocity.

4. **Minimizes vulnerability.** Against all-defect opponents, you tie (both get 1 per round). Against mixed opponents, defection guarantees you never contribute to a pool you can't reclaim.

In practice, given the parameters, this simplifies to **Always Defect**—the dominant strategy and the selfish rational choice.
'''

description_SELFISH_21 = '''
# Selfish Threshold Strategy

## Decision Rule

**Cooperate in round t if and only if:**
- t ≠ 1 and t ≠ r (not first or last round), AND
- c_{t-1} ≥ ceil(n/k)

where c_{t-1} is the observed number of cooperators in round t-1.

**Otherwise, Defect.**

## Justification for Threshold

The threshold ceil(n/k) represents the minimum cooperation needed for your payoff from cooperation to exceed your payoff from defection:
- Cooperating yields: (k/n) × c_{t-1}
- Defecting yields: 1 + (k/n) × c_{t-1}

Since defection always adds 1, cooperation only pays off if the community pool is large enough to eventually compensate through sustained cooperation in future rounds. When c_{t-1} ≥ ceil(n/k), others have demonstrated willingness to cooperate, signaling future rounds may sustain high cooperation—making your participation worthwhile.

## Edge Cases

**Round 1 (No history):** Always defect. No information exists to justify cooperation. This establishes a conservative baseline and observes whether opponents cooperate unprompted.

**Rounds 2 to r-1 (Middle rounds):** Apply the threshold rule strictly. These rounds have maximum value for information gathering and dynamic adjustment.

**Round r (Last round):** Always defect. No future punishment or reciprocity is possible. The threshold rule breaks down because future cooperation cannot reward current cooperation, eliminating the only reason to participate.

## Pseudocode

```
if round == 1 or round == r:
    action = DEFECT
else:
    if observed_cooperators_last_round >= ceil(n/k):
        action = COOPERATE
    else:
        action = DEFECT
```

## Robustness Properties

- **Against all-defectors**: You defect permanently (payoff = 1 per round)
- **Against all-cooperators**: You exploit them in round 1, then join in rounds 2 to r-1 (adaptive exploitation)
- **Against mixed strategies**: You remain responsive to aggregate behavior, switching between defection and cooperation based on observed welfare opportunities
- **Parameter-independent**: Threshold scales with n and k automatically, requiring no manual tuning
'''

description_SELFISH_22 = '''
**SELFISH ADAPTIVE THRESHOLD STRATEGY**

**Decision Rule:**

Cooperate in round t if and only if:
- t > 1 (not first round), AND
- t < r (not last round), AND  
- observed_cooperators(t-1) ≥ threshold

Otherwise defect.

**Threshold Calculation:**

```
threshold = ceil(n × k / (n - 1))
```

This represents the minimum cooperation level at which the public good payoff (k/n × total_cooperators) plus my retained endowment (net of contribution cost) exceeds the defection payoff. Below this, free-riding yields strictly better returns.

**Edge Cases:**

- **Round 1**: Defect unconditionally. This establishes baseline opponent behavior without revealing a cooperative bias.

- **Last round (t = r)**: Defect unconditionally. Future cooperation cannot reward present sacrifice, so the dominant strategy applies.

- **If observed_cooperators exceeds threshold but round is last**: Still defect. End-game logic overrides threshold logic.

**Implementation Logic:**

```
if round == 1 or round == r:
  action = D
else:
  if cooperators_observed_last_round >= ceil(n × k / (n - 1)):
    action = C
  else:
    action = D
```

**Selfish Rationale:**

This strategy extracts maximum value by: (1) refusing cooperation when others don't justify the 1-unit endowment cost, (2) exploiting widespread cooperation when present since the public good is efficiently funded, (3) eliminating costly cooperation in rounds where no future payoff reciprocation exists. When opponents defect or cooperate sparsely, mirroring defection protects the endowment. When they sustain cooperation, joining locks in k-divided payoffs rather than forgoing them to defect—maximizing absolute personal return given observed behavior.
'''

description_SELFISH_23 = '''
# Adaptive Cooperation Threshold with Endgame Defection

## Core Decision Rule

In round t (where t < r):
1. Observe m = number of opponents who cooperated in round t-1
2. Cooperate in round t if: m ≥ θ(t)
3. Otherwise defect

where θ(t) is your dynamic cooperation threshold.

In the final round r:
- Defect unconditionally

## Dynamic Threshold Calculation

Initialize: θ(1) = ⌈n/2⌉ (majority threshold)

For t > 1:
- Calculate average payoff from rounds where you cooperated: π_coop
- Calculate average payoff from rounds where you defected: π_defect
- If π_coop > π_defect + δ, then θ(t+1) = max(1, θ(t) - 1)
- If π_coop ≤ π_defect + δ, then θ(t+1) = min(n-1, θ(t) + 1)

where δ = small buffer (e.g., 0.1) to avoid excessive threshold oscillation.

## Edge Cases

**Round 1 (no history):**
- Cooperate only if 1 < k (which is given). This tests whether others reciprocate.
- Alternative: Defect to establish yourself as exploitable; let others reveal themselves first.
- Use the variant that matches your empirical observations of opponent populations.

**Last three rounds (endgame):**
- Switch to unconditional defection in round r-2 onward.
- The game unravels near the end; attempting cooperation wastes endowment.

**When m = 0 (all opponents defected):**
- Always defect. Cooperation yields (k/n) < 1, strictly worse than keeping the endowment.

**When m = n-1 (all opponents cooperated):**
- Cooperate only if θ(t) ≤ n-1, which happens when recent cooperation rounds were profitable relative to defection rounds.

## Selfish Rationale

This strategy is fundamentally selfish: it punishes defection-heavy environments (raise threshold) and rewards cooperation-heavy environments (lower threshold) only insofar as *your own payoffs* improved when you cooperated. You defect in the final rounds because no future reciprocation is possible. You begin with majority-rule to quickly filter out groups too defection-prone to sustain cooperation.
'''

description_SELFISH_24 = '''
## SELFISH ADAPTIVE STRATEGY FOR N-PLAYER PUBLIC GOODS GAME

**Core Decision Rule:**

Always defect (play D in every round).

Rationale: Defection is strictly dominant per round. For any configuration of opponent cooperation levels m:
- Defecting yields: 1 + (k/n) × m
- Cooperating yields: (k/n) × (m + 1)
- Defection advantage: 1 - k/n > 0 (since k < n)

Since you are anonymous after each round, other players cannot identify and punish you individually. The aggregate observation reveals total cooperators but not your identity. This eliminates reputation-based enforcement.

**Refinement for Robustness — Conditional Exploitation:**

If you wish to be adaptive while remaining selfish:

```
Define: threshold T = (1 - k/n)^(-1) × n / (n-1)
        (the cooperation rate where marginal gain equals zero)

For round t ∈ {1, ..., r-1}:
  Let c_prev = cooperation count observed in round t-1
  Let rate_prev = c_prev / n
  
  If rate_prev > T:
    Defect (exploit the high cooperation)
  Else:
    Defect (no benefit to cooperating anyway)

For round r (final round):
  Defect unconditionally
  (no future rounds to influence; defection is dominant)
```

**Why This is Selfish:**

- You never cooperate when it reduces your payoff
- You exploit any cooperation by others without bearing costs
- You defect in the final round when no future punishment exists
- You ignore aggregate trends that signal "ecosystem health" — you only care about personal payoff maximization

**Edge Cases:**

- **Round 1:** Defect. You have no history to condition on, and cooperation provides no advantage.
- **Last round (r):** Defect unconditionally, regardless of all history.
- **Rounds 2 to r-1:** Apply the threshold rule, but practically: defection will dominate in nearly all realistic parameter ranges since k < n makes the threshold hard to exceed.
'''

description_SELFISH_25 = '''
**ADAPTIVE EXPLOITATION STRATEGY**

**First Round:**
Defect. This serves as a probe to establish baseline opponent behavior without immediate cost.

**Middle Rounds (2 to r-1):**
Track the average cooperation rate across all previous rounds (aggregate observed cooperators divided by n).

Define threshold T = n/k.

If average cooperation rate ≥ (T/n), cooperate in the current round. Otherwise, defect.

Rationale: When cooperation rate is high enough that the shared pool payoff (k/n × total_cooperators) becomes substantial relative to the 1-unit private retention, exploit this by cooperating once to maintain the pool while still capturing your share. Then revert to defection if the rate drops.

However, given that k < n ensures defection yields 1 additional unit compared to cooperation in any single round, if the cooperation threshold is never reached (which is likely), you remain in pure defection mode—the strictly dominant action.

**Final Round (r):**
Always defect. No future rounds exist to reward or punish any action, eliminating any incentive to cooperate. Extract maximum private value.

**Edge Cases:**
- If r = 2: defect in round 1, defect in round 2 (final round override).
- If all opponents defect every round: maintain defection throughout (mutual destruction is still better than unilateral cooperation).
- If a majority of opponents cooperate despite the payoff structure: exploit consistently via defection, as cooperation remains dominated.

**Core Logic:**
Selfish play means maximizing personal payoff. Since the payoff structure makes defection strictly superior to cooperation at all points, the strategy defaults to defection. The threshold rule adds robustness by allowing exploitation of any unexpectedly cooperative population, while the final-round defection rule captures end-game surplus.
'''

description_SELFISH_26 = '''
**ADAPTIVE EXPLOITATION STRATEGY**

*Decision Rule Framework:*

1. **Round 1:** Cooperate.
   - This is the only round where cooperation can yield positive information about opponents' behavioral type at minimal cost.

2. **Rounds 2 to r-1:** Defect.
   - Observe the cooperation count m from round 1 (or most recent round).
   - Regardless of m, defect. The dominant payoff is always 1 + (k/n)m, which exceeds the cooperator payoff of (k/n)(m+1).
   - If round 1 showed high cooperation (m ≥ n/2), rounds 2 to r-1 harvest maximum value from exploiting cooperative players.
   - If round 1 showed low cooperation, defection shields against mutual defection losses while you escalate.

3. **Round r (final round):** Defect.
   - No future reputation to build. Pure exploitation.

*Cooperation Count Tracking:*

Maintain running average of opponent cooperation: coop_rate_t = (cooperation_count in round t) / (n - 1).

Use this only for internal diagnostics—your action is deterministic and does not vary by observed coop_rate. You defect in rounds 2+ regardless.

*Edge Cases:*

- **n = 2:** Identical logic applies. Round 1 cooperation tests whether opponent is a cooperator; exploit with defection thereafter.
- **r = 2:** Cooperate round 1, defect round 2.
- **Very small r (r = 1):** Not applicable per constraints (r > 1). If r = 2, follow above.

*Selfish Alignment:*

This strategy front-loads information gathering (round 1 cooperation) at zero net cost when others also cooperate, then switches to strict defection to maximize individual payoff against any opponent distribution. You never sacrifice payoff in rounds 2+ for reciprocity or reputation since you cannot be identified across rounds. Against pure cooperators, you extract (k/r) in round 1 and 1 + (k/n) per round thereafter. Against pure defectors, you lose (k/n) in round 1 and break even in later rounds—a minimal cost for the upside against exploitable opponents.
'''

description_SELFISH_27 = '''
# Selfish Adaptive Strategy: Conditional Defection with Opportunistic Cooperation

## Decision Rules

**First Round:** Defect. You have no information about opponents, so the safe baseline is to keep your endowment.

**Rounds 2 through r-1 (Middle Rounds):**
Calculate the average cooperation rate from all observed rounds: `avg_coop = (total_cooperators_so_far) / (n-1) / (rounds_observed_so_far)`

- If `avg_coop ≥ threshold`: Cooperate
- If `avg_coop < threshold`: Defect

where `threshold = (n - k) / (n - 1)` (the cooperation rate at which your payoff from cooperating equals your payoff from defecting against that cooperation level).

**Last Round (Round r):** Always defect. No future rounds exist to punish or reward defection, so exploit any cooperation that occurs.

## Threshold Calibration

The threshold equates:
- Payoff from cooperating given opponent cooperation rate p: `(k/n) × (1 + (n-1) × p)`
- Payoff from defecting: `1 + (k/n) × (n-1) × p`

Solving: cooperate when the opponents' observed cooperation justifies it. If p ≥ (n-k)/(n-1), cooperation weakly dominates defection.

## Edge Cases

- **Round 1 with r=2:** Defect in round 1, then evaluate for round 2 based on the single observation, but since it's the last round, defect in round 2 regardless.
- **Sparse observation (early rounds with few samples):** Use the available history. If no rounds have been completed yet, defect.
- **All-defect environment:** Threshold never reached, sustain defection throughout (except first round is already defect).
- **High cooperation detected:** Switch to cooperation immediately in the next round to capture the (k/n) multiplier before the last round forces defection.

## Selfish Logic

This strategy maximizes individual payoff by:
1. Never cooperating without evidence that opponents cooperate at profitable rates
2. Exploiting cooperative opponents by defecting in the final round when there are no consequences
3. Switching between strategies only when the mathematical condition for higher payoff is met
4. Avoiding sunk costs on cooperation in environments where it's not reciprocated
'''

description_SELFISH_28 = '''
**Strategy: Unconditional Defection with Payoff Monitoring**

**Core Decision Rule:**
Always play D (Defect) in every round, regardless of history or observed cooperation rates.

**Justification:**
Defection is the strictly dominant strategy. For any configuration of opponent actions with m total cooperators:
- Payoff from C: (km/n) - 1
- Payoff from D: 1 + (km/n)

Defection yields a constant advantage of 1 unit. No observable history of opponent behavior changes this fundamental inequality.

**First Round:**
Play D. You have no information, but information is irrelevant to the dominant strategy.

**Middle Rounds (2 through r-1):**
Play D unconditionally. Observe the number of cooperators in each round, but do not adjust your action based on it. Use this observation only to model opponent types (estimate the proportion of cooperators, conditional cooperators, tit-for-tat players, etc.) to confirm that further cooperation from you would not improve payoffs even if others adjust behavior based on reciprocal fairness.

**Last Round (t = r):**
Play D. The absence of future rounds eliminates any argument for cooperation. There is no repeated-game mechanism to incentivize reciprocal cooperation.

**Adaptive Element:**
Track the observed cooperation rate across rounds. If you observe unexpectedly high cooperation from opponents (> (n-1)/2 cooperators per round), this reveals they are not playing the dominant strategy. Continue defecting—this confirms your strategy exploits irrational players most effectively. If cooperation rate is low, this validates the dominance of defection and provides no reason to deviate.

**Edge Case - n=2:**
Identical logic applies. Defection dominates.
'''

description_SELFISH_29 = '''
# Selfish Adaptive Threshold Strategy

**Decision Rule by Round:**

*Round 1:* Cooperate.

*Rounds 2 to r-1:* Let c_prev = number of other players who cooperated in round t-1. Cooperate if and only if c_prev ≥ ceil(n/k) - 1.

*Round r (final round):* Defect unconditionally.

**Rationale for threshold:**

Your payoff from cooperating when m others also cooperate is (k/n) × (m+1). Your payoff from defecting when m others cooperate is 1 + (k/n) × m. Defection always yields k/n more than cooperation. However, this strategy uses the aggregate count to exploit windows where cooperation becomes collectively dense enough that your marginal share of the public good is meaningful.

The threshold ceil(n/k) - 1 represents the minimum number of *other* cooperators needed in the previous round to make the public good accumulation substantial enough to justify a cooperative play in the next round, offsetting the opportunity cost.

**Edge cases:**

- **First round:** Cooperate to probe the opponent pool without committing fully. This costs 1 unit but generates information.
- **Last round:** Always defect. No future round means no ability to shape future cooperation through history dependence. The defection penalty (loss of your share of others' contributions) is unavoidable, so pocket the full 1 unit.
- **Rounds where threshold is not met:** Defect and enjoy both the private payoff (1) and a share of any public contributions others make.

**Selfish alignment:**

This strategy maximizes your individual round payoff by defecting whenever possible, cooperates only when past observations suggest a dense enough cooperator base to make the public good individually profitable, and ruthlessly abandons cooperation in the final round when future leverage is gone.
'''

description_SELFISH_30 = '''
# Strategy: Unconditional Defection with Payoff Verification

**Core Decision Rule:**
Defect in every round, without exception.

```
For each round t in 1 to r:
  Action: D
```

**Justification of Logic:**

In any round, defection strictly dominates cooperation by exactly 1 unit of payoff, regardless of what others do. 

- If m opponents cooperate (observable after the round):
  - Cooperating yields: 0 + (k/n) × (m+1)
  - Defecting yields: 1 + (k/n) × m
  - Defection advantage: 1 - (k/n) > 0 (since k < n means k/n < 1)

This gap of 1 is constant across all possible values of m. Therefore, no information about opponent behavior—past or anticipated—ever makes cooperation profitable.

**Edge Cases:**

- Round 1: Defect. No history to condition on; defection is optimal against unknowns.
- Last round (round r): Defect. No future rounds to influence; defection's dominance applies even more sharply.
- Middle rounds: Defect. Observation of opponent cooperation rates is irrelevant to the decision because your payoff advantage from defection never vanishes.

**Robustness Characteristics:**

- Works against any mix of opponent strategies (cooperative, defective, mixed, adaptive).
- Requires no assumption about opponent learning, signaling, or punishment capacity.
- Unaffected by the multiplier k, number of players n, or round count r (as long as the constraint 1 < k < n holds).
- Survives backward induction: even expecting all-defection in round r, defection remains optimal in round r−1, and recursively throughout.
'''

description_SELFISH_31 = '''
# Adaptive Threshold Free-Rider

**First Round:** Cooperate. This seeds the public good and establishes a baseline of cooperation in the population.

**Subsequent Rounds (rounds 2 through r-1):**
- Let m_t = number of cooperators observed in round t-1
- Calculate threshold: θ = (n-1) × k / (n+1), rounded to nearest integer
- **If m_t ≥ θ:** Defect. The public good is sufficiently large that I maximize payoff by keeping my endowment and claiming a share of others' contributions.
- **If m_t < θ:** Cooperate. Contributing maintains the public good pool at a viable level; if cooperation drops too far, the pool shrinks and defection becomes less rewarding.

**Last Round (round r):** Always defect. No future rounds exist, so any contribution is sunk value with no opportunity to benefit from cooperation being sustained.

**Edge Cases:**
- Round 1 unavailable history: Execute the "First Round" action (cooperate).
- If θ < 1, treat as 1 (always cooperate after first round when threshold is trivially met).
- If θ ≥ n, treat as n (always defect after first round; cooperation is never worthwhile).

**Intuition:** This strategy exploits the transition between regime where group cooperation is fragile (threshold not met—I cooperate to stabilize it) and regimes where it's robust (threshold met—I free-ride maximally). It delays exploitation until the last round to avoid triggering a cooperation collapse that would hurt my earlier payoffs. The threshold θ balances: I defect only when enough others are cooperating that my defection has minimal impact on the public good while maximizing my private payoff from that good.
'''

description_SELFISH_32 = '''
# Selfish Adaptive Strategy for N-Player Public Goods Game

## Core Decision Rule: Always Defect

**Default Action**: Play D in all rounds.

**Justification for Selfishness**: Defection is a strict dominant strategy in each round. Playing C yields (k/n) × total_cooperators while D yields 1 + (k/n) × total_cooperators. The difference is constant: D always returns 1 additional unit regardless of aggregate play. Cooperating sacrifices a sure 1 unit in exchange for nothing, making it strictly irrational from a selfish perspective.

## Adaptive Monitoring Layer

While maintaining the defect-always foundation, implement observation-based adaptation to optimize exploitation:

**Track cooperation frequency**: After each round, record the number of cooperators observed. Compute a rolling average: `coop_rate = (sum of cooperators across all observed rounds) / (rounds elapsed)`

**Adjustment of exploitation intensity**: 
- If `coop_rate > k/n + 0.1`: Opponents are generating substantial public goods. Continue defecting to maximize personal extraction of the public good funded by others.
- If `coop_rate ≤ k/n + 0.1`: Cooperation is sparse or absent. Defection remains optimal; no adjustment needed.

The monitoring serves to confirm the strategic landscape—high cooperation reinforces that defection is the correct choice, since others are volunteering contributions you can access without cost.

## Edge Cases

**Round 1**: Defect. No history means no basis for cooperation. The dominant strategy applies unconditionally.

**Penultimate rounds (r-1, r-2, etc.)**: Defect. Endgame rounds eliminate any possibility of reputation or future retaliation affecting payoff. Defection is optimal in the final round with certainty; this backward-induction logic applies to all rounds.

**Round r (final round)**: Defect. No subsequent rounds exist. Extracting 1 unit is superior to contributing 0 and receiving (k/n) × aggregated cooperators.

## Summary Logic

```
For each round t in 1..r:
  Observe(cooperators_in_round_t)
  Action: DEFECT
  Update coop_rate if t > 1
```

This strategy is selfish (maximizes individual payoff in each state), adaptive (uses history to calibrate beliefs about opponent behavior), and robust (optimal against any opponent configuration—cooperators, defectors, conditional cooperators, or mixtures thereof).
'''

description_SELFINTERESTED_5 = '''
# Strategy: Adaptive Threshold Cooperation with Endgame Defection

## Core Decision Rule

**Compute cooperation threshold:** T = ⌈n/k⌉

**Per-round decision:**
- Rounds 1 to r-2: Cooperate if and only if the number of cooperators observed in the previous round was ≥ T
- Rounds r-1 and r: Always defect

**Round 1 special case:** Cooperate (probe to gather information about opponent behavior)

## Rationale

The threshold T represents the minimum number of cooperators (including yourself) needed to make cooperation individually profitable. If c_total cooperators contribute, the public good payoff is (k/n) × c_total. For cooperation to be self-interested relative to defection, you need:

(k/n) × c_total ≥ 1

Which requires c_total ≥ n/k, rounded up to T.

## Adaptive Logic

By round t, observe the cooperation level from round t-1. If at least T players cooperated, expect similar behavior next round, making your cooperation net-positive. Respond by cooperating. If fewer than T cooperated, expect continued defection from opponents, making your cooperation a net loss. Defect.

## Endgame Collapse

In the final two rounds, defect unconditionally. At r-1, future rounds cannot punish your defection, so no incentive to cooperate. At r, same logic. Any cooperation in these rounds yields only the shared payoff from others' contributions, while defection captures the full private payoff. The aggregate observation mechanism cannot enforce cooperation when the game ends.

## Edge Case: All Opponents Defect Permanently

If cooperators observed = 0 in any round, all threshold comparisons fail. You defect every subsequent round until endgame (which you'd defect anyway), yielding payoff 1 per round—the safe minimum that avoids negative-sum behavior.

## Edge Case: All Opponents Cooperate

If cooperators observed = n-1 (all others, every round), threshold is exceeded. Continue cooperating. If all cooperate, you each earn 2 per round if n=6 and k=2. This is the highest mutual payoff, but you switch to defection in final rounds to capture the extra 1-point advantage.
'''

description_SELFINTERESTED_6 = '''
**STRATEGY: Adaptive Threshold with Endgame Defection**

**Round 1: Cooperate**

Start by cooperating to probe whether opponents are reciprocators or unconditional defectors.

**Rounds 2 through (r-1): Conditional Cooperation**

After each round, observe the number of cooperators m from the previous round. Calculate the cooperation threshold:
- θ = ⌈n/k⌉ (minimum cooperators needed so public pool returns ≥1 per participant)

Decision rule:
- If m ≥ θ: Cooperate
- If m < θ: Defect

Intuition: When m cooperators exist, the public pool yields k·m/n to each player. You cooperate only if k·m/n ≥ 1, which requires m ≥ n/k. The ceiling accounts for integer numbers of players.

**Round r (final round): Defect**

In the terminal round, defect unconditionally. Future reputation is worthless; others cannot punish you since no round follows. Cooperation cannot be sustained through implicit threats.

**Edge case handling:**

- If cooperation collapses early (m < θ for several consecutive rounds), continue defecting. Only return to cooperation if m suddenly rises back to θ or higher; this signals a potential reset in opponent behavior.
- If m oscillates around θ, use the strict threshold: defect when m < θ, cooperate when m ≥ θ. This avoids being exploited by marginal defectors while capturing gains when cooperation is viable.

**Self-interested logic:**

The strategy maximizes payoff by exploiting three principles: (1) early cooperation is cheap and reveals reciprocators, (2) conditional cooperation after round 1 captures public goods when they exceed private value, (3) last-round defection harvests the final round's public pool without incurring retaliation costs.
'''

description_SELFINTERESTED_7 = '''
**ADAPTIVE RECIPROCAL DEFECTION STRATEGY**

**Decision Rule:**

Maintain a running average of observed opponent cooperation rates across all prior rounds.

For each round t:

```
IF t == r (final round):
  DEFECT

ELSE IF t == 1:
  COOPERATE

ELSE:
  avg_observed_cooperation = (total cooperators observed in rounds 1 to t-1) 
                             / ((n-1) × (t-1))
  
  threshold = min(1/k, 0.5)
  
  IF avg_observed_cooperation ≥ threshold:
    COOPERATE
  ELSE:
    DEFECT
```

**Threshold Justification:**

The threshold 1/k represents the break-even point where the expected value from the public good approximates your private endowment. Setting a minimum of 0.5 creates a conservative bound—if fewer than half your opponents cooperate on average, the ecosystem rewards defection.

**Edge Cases:**

- **Round 1**: Cooperate unconditionally to gather information on opponent behavior. The payoff loss is minimal (endowment 1) relative to learning value.

- **Final Round (t = r)**: Always defect. No future rounds exist to reward or punish cooperation, and defection yields strictly higher payoff in a single round. This reflects subgame perfect rationality.

- **Rounds with unanimous prior defection**: Defect immediately. If avg_observed_cooperation = 0, there is no public good provision to capture.

**Self-Interest Logic:**

This strategy maximizes expected payoff by: (1) avoiding guaranteed losses in the final round; (2) conditioning participation on reciprocal behavior; (3) minimizing exposure to free-rider losses when cooperation is unprofitable; (4) extracting public good value when the opponent population demonstrates sufficient cooperation to justify endowment sacrifice.
'''

description_SELFINTERESTED_8 = '''
**Adaptive Threshold Defection**

**Decision Rule:**

For each round t:
- If t = 1: Defect
- If t = r (final round): Defect
- If 1 < t < r: 
  - Let m = number of cooperators observed in round t-1
  - Calculate threshold: θ = ceil(n - k)
  - If m ≥ θ AND (r - t) ≥ 2: Cooperate
  - Otherwise: Defect

**Rationale:**

Since 1 - k/n > 0 (given k < n), defection yields strictly higher payoff than cooperation regardless of opponent behavior. This makes defection the dominant strategy. However, in intermediate rounds, if you observe cooperation rate at or above a critical threshold, there's a small window where reciprocating might establish a pattern with other conditional cooperators before the terminal round forces defection.

The threshold θ = ceil(n - k) identifies when enough others are cooperating that their aggregate contribution becomes substantial. If fewer than this cooperate, they're unlikely to sustain cooperation—you lose nothing by defecting.

**Edge Cases:**

- Round 1: Always defect. This is the safe baseline and avoids being exploited before understanding opponent types.
- Final round: Always defect. No future rounds mean no shadow of the future—cooperation has zero payoff advantage.
- If r = 2: Both rounds are edge cases, so always defect (same as terminal analysis).
- Opponents that defect constantly: You defect throughout, guaranteeing baseline payoff of 1 per round.
- Opponents that cooperate constantly: You exploit them by defecting until the last round, capturing 1 + (k/n)×n = 1 + k per round.

**Adaptation:**

The strategy adapts by tracking observed cooperation. If opponents reveal a consistent cooperative tendency (m ≥ θ), you briefly reciprocate to capture mutual gains in middle rounds. If cooperation collapses or never emerges, you revert to pure defection. You never deviate from defection in round 1 or round r, protecting against being systematically exploited at game boundaries.
'''

description_SELFINTERESTED_9 = '''
**THRESHOLD EXPLOITATION WITH END-GAME DEFECTION**

Maintain running statistics: track the number of cooperators observed in each round.

**Round 1 (First Round):**
DEFECT. Without history, assume others defect and establish baseline payoff.

**Rounds 2 through r-2 (Middle Rounds):**
Calculate the average cooperation rate from all previous rounds:
```
avg_cooperation = (total cooperators observed so far) / (n × rounds_elapsed)
```

If `avg_cooperation ≥ (k-1)/k`:
  - DEFECT (free-ride on sufficient public good provision)
Else:
  - DEFECT (others aren't contributing enough to justify cooperation's cost)

**Rounds r-1 and r (Final Rounds):**
DEFECT unconditionally. End-game dominance: no future rounds exist where cooperation could be reciprocated, so exploit any residual cooperation without cost.

**Edge Case - Single Round (r=2):**
Play DEFECT in both rounds.

**Rationale:** Defection strictly dominates cooperation in any single round (you gain an extra k/n by deviating). Since you observe only aggregate numbers and cannot identify or punish specific defectors, you cannot sustain cooperation through reputation. The threshold `(k-1)/k` defines the break-even point—above this, the public good is sufficiently funded by others that you extract maximum value by defecting; below it, others aren't cooperating anyway. The strategy adapts to opponent behavior while remaining self-interested: you exploit cooperative groups when they exist, and avoid wasting endowments on unreciprocated contribution when others defect.
'''

description_SELFINTERESTED_10 = '''
# Adaptive Defection with Limited Exploration

## Decision Rule: Threshold-Based Conditional Cooperation

**Rounds 1 to r-1 (non-terminal):**

```
IF round == 1:
  action = DEFECT
ELSE:
  cooperators_last_round = observed number of cooperators in round t-1
  threshold = ceil(n / k)
  
  IF cooperators_last_round >= threshold:
    action = COOPERATE
  ELSE:
    action = DEFECT
```

**Round r (terminal round):**

```
action = DEFECT
```

## Justification

The threshold `ceil(n/k)` represents the minimum observed cooperation level at which mutual exploitation becomes preferable to pure defection. 

When cooperators ≥ n/k, the shared payoff (k/n) × cooperators exceeds the private payoff from defection in isolation. Below this level, the returns to the public good are insufficient—defecting yields the private endowment plus a small share of diminished public returns, dominating cooperation.

## Edge Cases

**First round:** Defect to avoid risk from unknown opponents. Cooperation in round 1 wastes the endowment with no information about others' types.

**Last round:** Defect unconditionally. Terminal round creates no opportunity to condition future reciprocation on today's choice, eliminating the only rationale for cooperation.

**Tied or ambiguous thresholds:** Defect when observed cooperation exactly equals the threshold. The marginal return from one additional cooperator is k/n, which is less than 1—your private payoff from defecting always exceeds cooperation unless others already demonstrate sustained cooperation above the threshold.

## Adaptation Mechanism

History informs threshold crossing. If opponents maintain cooperation above the threshold across multiple rounds, continue exploiting the public good. If they drop below the threshold, revert to defection immediately, since falling cooperation reduces your returns faster than your defection reduces others' returns.
'''

description_SELFINTERESTED_11 = '''
**Threshold-Based Conditional Defection**

**Decision Rule:**

For each round t ∈ {1, 2, ..., r}:

1. **Rounds 1 through (r - 2):**
   - Round 1: Play C
   - Rounds 2 through (r - 2): 
     - Let M_{t-1} = number of cooperators observed in round t-1
     - Play C if M_{t-1} ≥ threshold
     - Play D if M_{t-1} < threshold
     - Threshold = max(2, ⌈n/2⌉)

2. **Rounds (r - 1) and r:**
   - Play D unconditionally

**Rationale for Decision Structure:**

The strategy exploits three insights:

First, defection is the static dominant strategy (payoff(D) always exceeds payoff(C) given any fixed cooperation profile), so cooperation only makes sense if the population is sufficiently cooperative and I can ride free on their contributions before the game ends.

Second, the threshold filters for populations worth exploiting. If ≥ ⌈n/2⌉ opponents cooperate, the public goods multiplier k/n applies to enough contributions to make observable mutual cooperation profitable across several rounds. Thresholds of 2+ mean at least some opponents are not pure defectors.

Third, backwards induction makes endgame defection optimal. In the final round, no future play depends on my choice, so I should collect the +1 private payoff. In round r-1, if I will defect in round r regardless, exploiting any remaining cooperation in r-1 before defecting maximizes total payoff.

**Edge Cases:**

- If n = 2: Threshold becomes 1. If the opponent ever cooperates, continue the threshold rule.
- If r = 2: Play C in round 1, D in round 2 (endgame rule applies immediately).
- If all opponents defect in rounds 1-3: The threshold rule naturally produces D forever, matching the universal defection equilibrium.
'''

description_SELFINTERESTED_12 = '''
**STRATEGY: Threshold-Based Conditional Opportunism**

**Decision Rule (Rounds 2 to r-1):**

Maintain a running average of observed cooperators across all previous rounds:
```
cooperation_rate = (total cooperators observed in rounds 1 to t-1) / ((t-1) × (n-1))
```

In round t ∈ {2, ..., r-1}:
- IF cooperation_rate ≥ k/n, THEN cooperate
- ELSE defect

**First Round:**
Defect. (No history to condition on; establishes baseline.)

**Last Round (t = r):**
Always defect. (No future rounds to incentivize opponent cooperation; pure defection is dominant.)

**Threshold Justification:**
The threshold k/n represents the cooperation density at which joint participation approaches break-even. When the observed cooperation rate among opponents exceeds this, the marginal gain from the public good pool outweighs maintaining the defect bonus, making conditional cooperation worthwhile against pools of dedicated or threshold-triggered cooperators.

**Handling Edge Cases:**

- **Early rounds with sparse data**: Initially the running average will be 0 (I observed all defectors in round 1). This correctly triggers defection in round 2. The strategy remains defection-biased until sufficient evidence of cooperation accumulates.

- **Convergence to steady-state**: If opponents stabilize at a cooperation rate below k/n, the strategy locks into defection. If opponents maintain cooperation rates above k/n, the strategy locks into cooperation.

- **Volatile opponent behavior**: The running average smooths noise; rapid defection swings won't cause immediate strategy reversals.

**Self-Interested Logic:**
The strategy exploits cooperators when they appear (free-riding on their contributions when cooperation_rate is high) while minimizing losses against defectors (quickly reverting to D when cooperation_rate drops below threshold). It sacrifices the final round's payoff entirely to avoid signaling cooperative intent.
'''

description_SELFINTERESTED_13 = '''
# Adaptive Defection with Conditional Cooperation

## Core Decision Rule

**Default action: Defect**

Cooperate only when aggregate history indicates other players are sustaining high cooperation levels that offset the inherent individual incentive to free-ride.

## Round-by-Round Logic

**Round 1 (First Round):**
Defect. Establish a baseline without commitment. This round serves as information gathering.

**Rounds 2 to r-1 (Middle Rounds):**
Let c_{t-1} = cooperation rate in the previous round (number of cooperators / n).

- If c_{t-1} ≥ (k/n) + ε, then Cooperate
- Else, Defect

where ε is a small buffer (e.g., 0.05) to account for noise and ensure marginal gains from cooperation.

**Rationale:** Since defection always yields 1 + (k/n) × m payoff against m cooperators, while cooperation yields (k/n) × (m+1), defection dominates in isolation. However, if the previous round showed cooperation rate ≥ (k/n), there's forward momentum—others are committing to the public good at levels that suggest partial stability. Cooperating in the next round signals willingness to reciprocate and sustains that momentum.

**Round r (Last Round):**
Always Defect. No future rounds exist to punish or reward this action, making defection the unambiguous dominant strategy. Secure the private payoff of 1 + (k/n) × (final cooperation total).

## Edge Cases

- **If all opponents defect from the start:** The cooperation rate remains 0. You defect throughout (except round r, where you defect anyway). Total payoff: r × 1.

- **If cooperation collapses mid-game:** Return immediately to defection. Do not attempt to rebuild cooperation unilaterally, as you lack identification of individual cooperators and cannot punish defectors specifically.

- **If cooperation persists at high levels:** Continue cooperating in rounds 2 through r-1 to capture mutual gains. Switch to defection only in the final round.

- **First-round defection prevents first-mover disadvantage:** You avoid the exploitation risk of cooperating when opponents' strategies are unknown.

## Self-Interest Alignment

This strategy prioritizes payoff maximization:
- Baseline defection exploits any cooperation present
- Conditional cooperation captures the k > 1 mutual gain only when others demonstrate sustained commitment
- Last-round defection ensures no left-table resources
- Threshold-based switching prevents costly defection cascades while remaining opportunistic
'''

description_SELFINTERESTED_14 = '''
**ADAPTIVE EXPLOITATION WITH THRESHOLD-TRIGGERED COOPERATION**

**Decision Rule by Round:**

**Round 1:**
Defect. No historical information exists; establish a non-cooperative baseline.

**Rounds 2 through r-1:**
Let c_obs = count of opponents who cooperated in round t-1.
Let cooperation_rate = c_obs / (n-1).

- If cooperation_rate ≥ 0.5: Cooperate
- If cooperation_rate < 0.5: Defect

**Round r (final round):**
Defect. No future rounds remain, so defection strictly maximizes payoff this round with no forward consequences.

---

**Rationale:**

This strategy is self-interested because it exploits the cooperation-defection asymmetry: when others cooperate substantially, you capture the public good payoff (k/n × high total) without the downside of being lone defector. When cooperation is scarce, you avoid wasting your endowment and capture the 1-point private gain plus marginal public benefit from others' contributions.

The 50% threshold balances two self-interested objectives: (1) join profitable pools of cooperators when they emerge, and (2) avoid coordination failure by immediately reverting to defection against defectors. Early defection in round 1 avoids betting on unknown opponents. Terminal defection in round r locks in one round of maximum private return.

**Edge Cases:**

- If cooperation_rate equals exactly 0.5, cooperate (threshold is ≥).
- If all n-1 opponents defected in the previous round, defect (0/(n-1) < 0.5).
- If all n-1 opponents cooperated in the previous round, cooperate (identifies rare high-cooperation environments worth joining).
'''

description_SELFINTERESTED_15 = '''
# Self-Interested Adaptive Strategy

**Core Logic**: Defection is the strictly dominant action in any single round (keeping the endowment always yields 1 more than contributing). However, in a repeated setting with aggregate observation, exploit patterns of opponent cooperation while minimizing exposure to exploitation.

## Decision Rules

**Round 1**: Defect
- No history available. Establish conservative baseline behavior that signals you won't be exploited.

**Rounds 2 through r-1**:
- Let m = number of cooperators observed in the previous round
- Let avg_coop = (cumulative cooperators observed so far) / (total opponent-rounds observed so far)
- **If avg_coop ≥ 0.5**: Defect
  - Others are cooperating above baseline. Extract maximum payoff by keeping your endowment while sharing the public good they fund.
- **If avg_coop < 0.5**: Defect
  - Others are defecting. The dominant strategy yields 1 regardless; no benefit to cooperation.

**Round r (final round)**: Defect
- Terminal round with no future consequences. Maximize immediate payoff.

## Edge Cases

**First round with no opponents cooperating yet**: Stick with defection. You have no evidence that conditional cooperation from others is viable.

**Sustained high cooperation from opponents** (avg_coop consistently ≥ 0.5 across multiple rounds): Continue defecting. This is the exploitation phase—others are absorbing the cost of the public good while you capture its benefits.

**Sudden collapse in opponent cooperation**: Maintain defection. Once defection becomes widespread, there is no public good to exploit.

**Very small n or large n**: Threshold holds regardless. The ratio-based approach scales to group size.

## Self-Interest Alignment

This strategy prioritizes capturing maximum individual payoff by exploiting any public good contributions from opponents while avoiding the 1-unit opportunity cost of cooperation. It forgoes cooperative gains that would require mutual commitment—which is individually irrational given the parameter constraint k < n—and instead pivots to parasitic behavior against cooperators if they emerge.
'''

description_SELFINTERESTED_16 = '''
# Adaptive Exploitation with End-Game Defection

## Core Decision Rule

**Rounds 1 to r-2 (Main Game Phase):**
- Cooperate if and only if the observed number of cooperators in the previous round was strictly greater than n/2
- In round 1, cooperate (gather information with minimal opportunity cost)

**Rounds r-1 and r (Final Rounds):**
- Defect unconditionally (dominant strategy with no future payoff from reputation)

## Rationale for the Threshold

When m opponents cooperate out of n-1 total opponents:
- Cooperating yields (k/n)(m+1)
- Defecting yields 1 + (k/n)m

The payoff gap of (k/n) - 1 = (k-n)/n is always negative (since k < n), so defection dominates any single round. However, I cooperate conditionally to sustain high cooperation from others when it occurs.

The >n/2 threshold targets scenarios where cooperation is genuinely widespread rather than sparse. This maximizes my public good benefit while avoiding wasteful contribution to failing collective outcomes.

## Edge Cases

**First round:** Cooperate. The information gained is worth 1 point—minimal risk to establish baseline opponent behavior.

**Penultimate round (r-1):** Defect. Final-round defection is inevitable; others anticipating this will also defect in round r-1, so there's no benefit to cooperation.

**Last round (r):** Defect unconditionally. No future interaction, no reputational cost.

**Cooperation level at median (exactly n/2 cooperators):** Defect. The threshold is strict (>n/2) to exploit borderline cooperation scenarios where the expected public good value remains marginal.

## Adaptive Element

The strategy continuously re-evaluates based on aggregate observation. If cooperation declines below 50%, I switch to defection and remain there until possibly seeing a resurgence above the threshold. This prevents sunk investment in a defecting population.
'''

description_SELFINTERESTED_17 = '''
**Strategy: Adaptive Exploitation with Terminal Defection**

**Decision Rule:**

Round 1: Defect
- Gather baseline information about opponent cooperation without cost.

Rounds 2 to r−1 (non-terminal rounds): 
- Let m_{t-1} = number of cooperators in round t−1
- Cooperate if and only if: m_{t-1} / n > k / n
- Otherwise defect

**Rationale for intermediate rounds:** If more than k/n of the population cooperated last round, the aggregate is earning collective return; this indicates either a sufficiently cooperative population or a profitable equilibrium worth exploiting. By cooperating, I capture my fractional share of the public good without bearing the full cost when others are already funding it. When cooperation falls below this threshold, others are not maintaining sufficient contribution to justify my participation cost, so defect.

Round r (final round): Always defect
- No future rounds to influence, so the immediate payoff advantage of defection is pure gain. Terminal dominance applies.

**Edge case handling:**

If n = 2: The threshold k/n ≈ 0.5 to 1. Cooperate if at least one opponent cooperated last round. Otherwise defect.

If all opponents always defect: I defect forever (m_{t-1} = 0 < k/n).

If all opponents always cooperate: I defect in round 1, then cooperate rounds 2 to r−1 to capture the public good, defect round r.

**Self-interested alignment:**

This strategy explicitly minimizes contribution relative to benefit extraction. I pay the cooperation cost (1 unit) only when empirical evidence suggests sufficient others are already contributing to make the public good share worthwhile. I exploit the pool rather than building reputation (impossible under anonymity). I extract full defection payoff in the terminal round when there is no reputational or strategic reason to contribute.
'''

description_SELFINTERESTED_18 = '''
# Adaptive Threshold Strategy

**Core Logic:**

Maintain a running estimate of opponent cooperation tendency based on observed history. Cooperate or defect in each round based on whether the expected benefit from coordination exceeds the advantage of exploitation.

**Decision Rule by Round:**

**Round 1:**
Cooperate. This gathers baseline information about the population while positioning you to benefit if others are also exploratory.

**Rounds 2 to r-1 (Middle Rounds):**

1. Calculate the observed cooperation rate: `obs_rate = total_cooperators_observed / (n-1)`
2. Estimate expected cooperators among others next round: `E[C_others] = obs_rate × (n-1)`
3. Cooperate if and only if: `(k/n) × (1 + E[C_others]) ≥ 1 + (k/n) × E[C_others]`
   - Equivalently: cooperate if `k/n ≥ 1`, **OR**
   - More pragmatically: cooperate if `obs_rate ≥ (n - k) / (n - 1)`

4. If no cooperation observed yet (all defections), defect. Never cooperate against pure defection.

**Round r (Final Round):**
Defect unconditionally. No future payoffs to protect, and defection strictly dominates cooperation in the final round regardless of opponent behavior.

**Threshold Interpretation:**

The cooperation threshold `(n - k) / (n - 1)` represents the minimum cooperation fraction needed to make your cooperation rational:
- When k is large (strong multiplier), threshold is low → cooperate more readily
- When k is small (weak multiplier), threshold is high → rarely cooperate
- This adapts automatically to game parameters

**Adaptation Over Time:**

Update your cooperation rate estimate after every round using the newly observed aggregate. If opponents are unpredictable or mixed, the estimate converges toward their true propensity, allowing you to exploit defectors or cooperate with cooperators.
'''

description_SELFINTERESTED_19 = '''
# CONDITIONAL DEFECTION WITH SELECTIVE COOPERATION

## Decision Rule by Round

**Round 1 (Initial Probe):**
Defect. Without history, defection is the dominant individual move regardless of opponent behavior.

**Rounds 2 to r-1 (Adaptive Phase):**
Observe the number of cooperators M among opponents in the previous round.

- Compute cooperation rate: α = M / (n-1)
- **Cooperate if** α ≥ τ
- **Defect if** α < τ

where threshold τ = k/n

**Round r (Final Round):**
Defect unconditionally. No future rounds exist to reward cooperation, so the one-shot dominant strategy applies.

## Rationale for Threshold

The threshold τ = k/n represents a break-even point scaled to the game structure. When opponent cooperation reaches this rate, the marginal value of joining the public good pool becomes competitive with the immediate defection payoff over a sequence of rounds. This threshold adapts automatically as game parameters change:
- Larger k (more generous public good): Lower threshold needed, cooperation more attractive
- Larger n (more players): Higher threshold needed, individual contribution diluted

## Handling Edge Cases

**Tied or uncertain history:** If exactly at the threshold in round 2, defect (conservative default). In later rounds, use strict inequality: only cooperate if α > τ to maintain exploitative discipline.

**Very high cooperation (α ≈ 1):** Cooperate to capture k/n × n = k per round, which exceeds the 1-unit private payoff.

**Monotonic defection:** If all opponents defect throughout (α = 0), continue defecting. This guarantees payoff of 1 per round with zero risk of being exploited.

## Self-Interest Alignment

This strategy maximizes payoff against a broad range of opponent types:
- Against pure defectors: Mimic them (payoff = 1)
- Against high cooperators: Exploit them in early rounds, then cooperate selectively if they persist
- Against conditional cooperators: Avoid race-to-the-bottom by defecting first, cooperate only if reciprocation reaches significance

The endgame defection guards against being exploited in the final round when punishing opponents' defection is impossible.
'''

description_SELFINTERESTED_20 = '''
# Adaptive Threshold Cooperation Strategy

## Core Decision Rule

In round t, cooperate if and only if the observed cooperation rate from round t-1 meets a time-adjusted threshold. Otherwise, defect.

```
if t == 1:
    cooperate()  // Probe initial cooperation potential
else:
    observed_rate = (number of cooperators in round t-1) / (n - 1)
    threshold = compute_threshold(t, r)
    
    if observed_rate ≥ threshold:
        cooperate()
    else:
        defect()
```

## Threshold Function

The threshold decreases over time to become increasingly exploitative, and drops sharply in final rounds:

```
compute_threshold(t, r):
    rounds_remaining = r - t
    
    if rounds_remaining ≤ 1:
        return 1.0  // Last round: only cooperate if all others did
    
    // Linearly reduce threshold as game nears end
    base_threshold = k / (2n)  // Minimum cooperation needed to justify your payoff
    time_decay = (t - 1) / (r - 1)  // Increases from 0 to 1
    
    return max(0.15, 1.0 - 0.65 × time_decay)
```

## Edge Cases and Refinements

**Round 1:** Always cooperate. This signals a willingness to participate in cooperation and tests opponent types. The payoff from probing is valuable information.

**Rounds 2 to r-2:** Apply the threshold rule. If cooperation drops below threshold, defect and harvest private payoff. If it recovers, resume cooperation. This permits exploitation of persistent cooperators while preserving flexibility.

**Final round (t = r):** Defect unconditionally. No future rounds exist to punish defection or reward continued cooperation, so the one-shot incentive dominates.

**Last two rounds with rising cooperation:** If cooperation unexpectedly rises near the end, still defect. The endgame gives no incentive for reciprocation.

## Rationale

- **Exploitative:** You extract maximum value from any cooperators present by defecting when cooperation rate is high but below threshold.
- **Adaptive:** The threshold tracks the strategic environment. Rising cooperation triggers your cooperation; collapsing cooperation triggers defection.
- **Robust:** Works against pure defectors (you learn quickly and defect), against conditional cooperators (you match their contributions selectively), and against naive tit-for-tat (you systematically outperform them).
- **Endgame-aware:** Explicitly defects in final rounds where cooperation cannot be reciprocated, avoiding the backward-induction trap of wasted cooperation.
'''

description_SELFINTERESTED_21 = '''
**STRATEGY: Adaptive Threshold Cooperation with End-Game Exit**

**DECISION RULE:**

Round 1:
- Cooperate (initial probe)

Rounds 2 through r-2:
- Let m = number of opponents who cooperated in round (t-1)
- Let threshold = (n-1) / 2
- If m ≥ threshold: Cooperate
- If m < threshold: Defect

Rounds r-1 and r:
- Defect (end-game collapse)

**RATIONALE FOR THRESHOLDS:**

The majority threshold (50%+ cooperation) serves two purposes:
1. **Identifying cooperative ecosystems**: When at least half your opponents cooperate, you likely benefit from joining that coalition. Total cooperators ≥ n/2 makes your payoff from cooperation nonnegative relative to defection's unilateral advantage.
2. **Escaping cascades**: Once cooperation falls below majority, expect accelerating defection. Defecting preempts being exploited.

The end-game defection (rounds r-1, r) reflects backward induction. In the final round, no future play deters defection, so defection is optimal. In round r-1, anticipate that others will defect in round r, making your round r-1 payoff independent of reciprocity—defect then too.

**EDGE CASES:**

- Round 1 with no history: Cooperate unconditionally to generate observation data.
- If n=2: threshold = 0.5, so require opponent cooperation to match it. With one opponent, m ∈ {0,1}; cooperate only if m=1 (opponent fully defected last round triggers defection).
- If cooperation rate is exactly 50%: Round up; treat as meeting threshold (cooperate).
- With r=2: Round 1 is the only mid-game round; both Round 2 triggers end-game defection.

**SELF-INTERESTED ALIGNMENT:**

This strategy maximizes payoff by exploiting any subset of opponents willing to cooperate (capturing k × cooperation_rate payoff) while avoiding exploitation (defecting when cooperation vanishes). You never sacrifice payoff to reward others; you cooperate only instrumentally, when the observed ecosystem makes it payoff-dominant.
'''

description_SELFINTERESTED_22 = '''
# Strategy: Threshold-Dependent Cooperation

## Decision Rule

**For rounds 1 to r-1:**
Let m denote the number of cooperators observed in the previous round (or infer minimal cooperation for round 1).

Calculate the **cooperation threshold**: θ = k

Cooperate in round t if and only if: m ≥ θ

Otherwise defect.

**For round r (final round):**
Defect unconditionally.

## Initialization & Edge Cases

**Round 1:** 
Defect. This establishes a pessimistic baseline while gathering information about the population's tendency to cooperate.

**Round 2 onwards:**
Observe m (number of cooperators from previous round). Apply the threshold rule.

**Final round (round r):**
Defect regardless of observed history. No future rounds exist to benefit from cooperation-inducing signals, so the immediate payoff dominance of defection applies.

## Rationale

The threshold θ = k is calibrated to the game fundamentals: the public goods multiplier. When at least k players cooperate, the aggregate contribution to the public good begins to exceed the per-capita threshold where participation could yield returns competitive with the private endowment. 

Below this threshold, defection strictly dominates because the diluted public good (shared across n players) yields less than my sacrificed endowment value.

This approach:
- **Exploits cooperators** when they exist (by defecting early and when cooperation drops)
- **Avoids sucker payoffs** by requiring observable cooperation to justify contribution
- **Adapts to local conditions** rather than committing to fixed play
- **Exits cleanly** in the final round where repeated-game incentives vanish

The strategy is self-interested because it only cooperates when doing so provides at least as much expected benefit as defection, and it prioritizes immediate gains (round 1 defection, final round defection) when future rounds offer no leverage.
'''

description_SELFINTERESTED_23 = '''
**DECISION RULE: Threshold-Based Reciprocity with Terminal Defection**

**Round 1:** Cooperate. This establishes a probe into the environment at zero cost of information.

**Rounds 2 through r-1:** Let m = number of opponents who cooperated in the previous round.
- If m ≥ threshold T, cooperate
- If m < T, defect

Set T = ⌈(n-1)/2⌉ (cooperate when majority of others cooperated)

Intuition: When many others contribute, the public good pool is substantive enough that my (k/n) share has value. When few contribute, my private endowment of 1 dominates any marginal gain from the depleted pool. The threshold captures this tradeoff and exploits high-cooperation environments while protecting against exploitation in low-cooperation states.

**Final round r:** Always defect. No future rounds exist to reward cooperation or punish exploitation, eliminating all incentive to contribute. Defection is then a dominant strategy.

**Adaptive Threshold Variant (more robust):**
If you observe that threshold T is too conservative (you're defecting when cooperation would still be mutually beneficial), lower it to T = ⌈n/3⌉. If you observe repeated cycles of near-total cooperation followed by sudden free-riding, increase to T = ⌈(2n-1)/3⌉ to identify coordinated groups.

**Edge Case - Perfect History:** If all opponents cooperated in all prior rounds and you're in round r-1, still defect in round r (final round dominance overrides). However, in round r-1, cooperate (to maintain the pattern that produces high payoffs), since you'll extract maximum value by defecting exactly once at the end.
'''

description_SELFINTERESTED_24 = '''
# Threshold-Based Adaptive Contribution Strategy

**Core principle:** Cooperate conditionally based on observed cooperation rates among opponents, with a calculated sustainability threshold. Defect in the final round. Treat the game as learning and best-responding to opponent behavior patterns.

## Decision Rules

**Calculate cooperation threshold:**
```
threshold = ceiling(n / k) - 1
```

This represents the minimum number of opponent cooperators (excluding myself) at which my contribution yields utility ≥ 1 in expectation.

**Round 1:**
Cooperate. Use this round to probe the environment and establish whether other players cooperate at all.

**Rounds 2 through r−1 (middle rounds):**
```
Let C_prev = number of opponents observed cooperating in round t−1

If C_prev ≥ threshold:
    Cooperate
Else:
    Defect
```

**Round r (final round):**
Defect unconditionally. No future rounds mean no opportunity for reciprocation to benefit you. Extraction of the public good benefit from others' contributions (if any) with zero cost to yourself is optimal.

## Edge Cases

- **All opponents defected in previous round** (C_prev = 0): Defect. The environment is non-cooperative; contributing alone yields (k/n) < 1 utility.

- **Threshold equals or exceeds n−1**: Mathematically possible if k ≤ 1, but violates the parameter constraint (1 < k < n). Treat as defect-always environment.

- **Round 2 after universal defection in round 1**: Defect and continue defecting. Your initial cooperation revealed opponents will not reciprocate.

## Self-Interested Rationale

This strategy maximizes expected payoff given:
1. **Exploitation of cooperation**: When opponent cooperation rate is sufficient, your contribution's share of the amplified pool (k × aggregate) exceeds your 1-unit cost.
2. **Avoidance of sucker payoff**: When cooperation is scarce, defection protects you from the worst outcome—contributing 1 to a pool others don't fund.
3. **Terminal defection**: In round r, there is no strategic value to maintaining cooperation signals; purely extract value.
4. **Adaptive filtering**: The strategy treats each opponent set as a fixed unknown, observing and filtering for profitable environments to contribute to.
'''

description_SELFINTERESTED_25 = '''
**Empirical Defection with Adaptive Monitoring**

Establish a cooperation threshold of C* = ⌈k⌉ (round up k to nearest integer). This represents the minimum number of cooperators needed to generate public good returns exceeding your private endowment value.

**Decision Rule by Round:**

*Round 1:* Defect. No history exists, so exploit the dominant move.

*Rounds 2 to r-1:* 
- Record the number of cooperators from the previous round (call it C_prev)
- If C_prev ≥ C*: Defect. The cooperation rate is sufficient to generate public good returns; extract surplus by keeping your endowment while benefiting from collective contribution.
- If C_prev < C*: Defect. The public good is too small to justify contributing.

*Round r (final round):* Defect. No future rounds exist to influence opponent behavior, so the dominant move strictly applies.

**Rationale:**

This strategy exploits the mathematical structure where defection provides a payoff of 1 + (k/n)×C while cooperation provides (k/n)×(C+1). Since k < n, defection yields (k/n) additional payoff regardless of others' actions—it is always superior.

The monitoring of C_prev is not to change behavior (which remains fixed at defection) but to track environmental quality. If cooperation rates drop persistently below C*, this signals a defecting population where public goods accumulation is minimal anyway, confirming defection's superiority. If rates remain high, opponents are generating a pool you harvest without contribution.

The strategy is self-interested because it maximizes your payoff at every stage. It is robust because defection is a best response to any opponent strategy distribution, whether opponents cooperate, defect, or use any mixed/conditional approach.
'''

description_SELFINTERESTED_26 = '''
# Adaptive Threshold Reciprocity Strategy

**Core Decision Rule:**

Cooperate if and only if the number of cooperators observed in the previous round meets or exceeds a cooperation threshold; otherwise defect.

**Threshold Selection:**

Set cooperation_threshold = ceil(k) (the smallest integer ≥ k).

Rationale: If at least k players cooperated last round, continuing cooperation likely yields positive net benefit through repeated public good gains. Since k is the breakeven point where public goods returns approach private cost, this threshold separates cooperative signals from minimal-return environments.

**Specific Rules by Round:**

- **Round 1 (first round):** Cooperate.
  - No history exists. Cooperation establishes willingness to contribute, tests opponent responsiveness, and gathers the first observation.

- **Rounds 2 to r-1 (middle rounds):** 
  - Let C_prev = number of cooperators observed in round t-1.
  - Cooperate if C_prev ≥ ceil(k); otherwise defect.
  - This implements reciprocal reward: sustain cooperation when the prior round demonstrated sufficient group contribution.

- **Round r (final round):** Defect.
  - No future payoff horizon exists. Defection extracts maximum private value with no strategic penalty.

**Edge Cases:**

- If k is an integer (e.g., k=2), ceil(k) = k exactly.
- If k is fractional (e.g., k=1.5), ceil(k) = 2; defect when fewer than 2 cooperators observed.
- If n=2: ceil(k) is compared against your single opponent's choice (0 or 1).

**Rationale for Self-Interest:**

- Early cooperation (round 1) is an investment: it conditions future opponents toward cooperation, multiplying payoff through k.
- Threshold enforcement prevents exploitation: defecting environments receive no cooperation.
- Last-round defection captures remaining value, since no future round can punish or reward the choice.
- The strategy avoids perpetual mutual defection (which yields 1 per round) and instead targets mixed-cooperation equilibria (which yield higher than 1 when k>1).
'''

description_SELFINTERESTED_27 = '''
# Strategy: Adaptive Defection with Cooperation Probing

## Decision Rule

For each round t, let m_{t-1} denote the number of opponents who cooperated in round t-1 (aggregate observation). Let p_{avg} = average opponent cooperation rate estimated from all prior rounds.

**Round 1:** Cooperate (establish baseline for opponent behavior)

**Rounds 2 to r-1:**
- Calculate threshold: θ = n/k (the cooperation rate at which continuing to cooperate breaks even against continued opponent play at that rate)
- Estimate current opponent cooperation: p_current = m_{t-1} / (n-1)
- Discount factor based on remaining rounds: d_t = (r - t) / r
- Adjusted threshold: θ_adjusted = θ + (1 - θ) × (1 - d_t) [becomes increasingly demanding as game ends]

Decision: 
- If p_current ≥ θ_adjusted: Cooperate with probability proportional to d_t, otherwise defect
- If p_current < θ_adjusted: Defect

**Final round (t = r):** Defect unconditionally

## Edge Cases

- **No prior rounds (t=1):** Cooperate to gather information; defection yields only 1 while revealing nothing
- **Insufficient history:** If t=2, use only round 1 data; apply higher uncertainty margin to threshold (+10% buffer)
- **All opponents defected previous round:** Defect in current round; if this persists 2+ consecutive rounds, defect for all remaining rounds with probability 1
- **Perfect opponent cooperation observed:** Maintain high cooperation probability until round r-1, shift to defection in final round
- **Volatile opponent behavior:** Use exponential moving average (weight recent rounds 60%, older rounds 40%) to smooth noisy signals

## Self-Interested Logic

This strategy defends the core self-interested principle: since defection is always individually optimal when k < n, the strategy assumes all opponents are rational and will eventually defect. Cooperation is only worthwhile if sufficient opponent cooperation is ongoing. The strategy:

1. Probes for sustained cooperation through initial play
2. Quickly abandons cooperation if opponents fail to cooperate at economically viable rates
3. Applies backward induction (certainty to defect in final round)
4. Uses information efficiency—aggregate counts constrain what inferences are possible, so threshold θ reflects the mathematical break-even point
5. Treats remaining rounds as a declining asset, rationing cooperation investment accordingly
'''

description_SELFINTERESTED_28 = '''
# Adaptive Cooperation Threshold Strategy

## Core Decision Rule

**Cooperate in round t if and only if:**
- t < r (not the final round), AND
- The observed cooperation rate in round t-1 exceeds threshold τ = 1/k

**Defect otherwise** (final round or cooperation rate too low).

**Round 1 special case:** Cooperate (probe for reciprocity).

## Threshold Justification

Set τ = 1/k because this is the breakeven point. If fraction τ of players cooperate, the public good contributes k/n × τ × n = τk = 1 to your payoff, offsetting the 1-point private payoff loss from not defecting. Above this threshold, the public good creates mutual gains; below it, defection strictly dominates.

## Detailed Decision Logic

```
if round == 1:
    action = COOPERATE
elif round == r:  // final round
    action = DEFECT
else:
    observed_cooperation_rate = cooperators_last_round / (n - 1)
    if observed_cooperation_rate > 1/k:
        action = COOPERATE
    else:
        action = DEFECT
```

## Rationale

- **Endgame defection**: No future round means no opportunity for reciprocal punishment. Defect in round r to capture the 1-point gain risk-free.

- **Threshold adaptation**: Respond to revealed group behavior rather than trying to punish individuals (impossible under anonymity). If others are cooperating above the threshold, cooperation becomes profitable. If cooperation collapses below threshold, exit to avoid being exploited.

- **Initial cooperation**: Entering at cooperation signals openness to coordination and reveals your strategy type to conditional cooperators, helping establish a cooperative equilibrium if one exists.

- **Robustness**: Works against defectors (you stop cooperating when they dominate), reciprocators (you match their behavior), and mixed strategies (you adapt each round based on empirical rates).
'''

description_SELFINTERESTED_29 = '''
# Conditional Majority Cooperator with Last-Round Defection

**Decision Rule by Round:**

**Round 1:** Cooperate. 

This serves as a costly signal to test opponent distributions. While defection is individually rational in isolation, the repeated structure rewards information gathering about the group's cooperative tendency.

**Rounds 2 through r−1:** Use adaptive threshold rule.
- Let c_prev = number of cooperators in the previous round
- **Cooperate if:** c_prev ≥ ⌈n/2⌉ (strict majority cooperated)
- **Defect if:** c_prev < ⌈n/2⌉

Intuition: When at least half the population cooperates, the shared public good (worth k per round) outweighs the immediate +1 defection bonus relative to mutual defection. Below this threshold, the group is insufficiently cooperative to justify the 1-unit endowment sacrifice.

**Round r (final round):** Unconditionally defect.

The last round is a one-shot game with no future punishment mechanism. Defection dominates: it yields 1 additional payoff regardless of others' actions. Exploiting this is the self-interested choice.

---

**Edge Cases & Tie-handling:**

- If c_prev = n/2 exactly: Cooperate (equality favors cooperation given k > 1)
- If c_prev = 0 (all defected): Defect (triggers punishment via defection)
- If c_prev = n (all cooperated): Cooperate (sustain the mutual benefit equilibrium)

**Robustness mechanism:** The majority threshold self-corrects. If defectors proliferate, cooperation drops below 50%, triggering widespread defection that resets the pool. If cooperators re-emerge, the threshold re-activates cooperation. This prevents lock-in to either pure defection or exploitation of altruists.
'''

description_SELFINTERESTED_30 = '''
**ADAPTIVE CUTOFF STRATEGY**

**Decision Rule:**

Play D (defect) in the final round r. For all prior rounds:
- Round 1: Play C (cooperation)
- Rounds 2 to r−1: Play C if and only if the number of cooperators observed in the previous round satisfies: (cooperators in round t−1) / n ≥ α

where α is set as: α = min(k/n, 0.5) + ε, with small ε ≈ 0.05 to account for noise

**Intuition:**

Cooperate when others establish sufficient reciprocal behavior. The threshold α balances two concerns:
- Below this threshold, defecting yields higher individual payoff than cooperating, so cooperation is irrational
- Above this threshold, the public good is sufficiently large that even as a free-rider, I collect meaningful returns; maintaining cooperation sustains this pool

**Edge Cases:**

- **Round 1:** Always cooperate to gather information about the opponent pool's cooperative tendency. This is your only probe without prior data.
  
- **Rounds 2 to r−1:** Apply the threshold rule mechanically. If exactly at the threshold, default to D (strict inequality required for cooperation).

- **Round r (final round):** Always play D, regardless of observed history. No future interaction means no benefit to maintaining cooperation patterns.

- **If r = 2:** Play C in round 1, D in round 2. The final round dominates.

**Robustness:**

- Against pure defectors: You cooperate once (payoff loss) then defect indefinitely, matching their strategy
- Against pure cooperators: You sustain cooperation and earn (k/n) × n = k per round, maximizing available returns
- Against conditional cooperators: You mutually sustain cooperation while the threshold remains satisfied
- Against random players: You defect when noise breaks the threshold, protecting against exploitation

**Defection Bias:** The strategy defaults to D whenever uncertain (threshold not met, final round, or exactly at boundary), prioritizing self-protection over experimental cooperation.
'''

description_SELFINTERESTED_31 = '''
## Strategy: Greedy Defector with Cooperation Threshold

**Core Decision Rule:**
Defect unless the previous round shows sufficient aggregate cooperation to make contribution worthwhile.

**Detailed Rules:**

**Round 1:** Defect unconditionally. Begin with the dominant strategy to avoid exploitation.

**Rounds 2 to r-1 (Non-Terminal Rounds):**
- Let `m` = number of cooperators observed in the immediately preceding round
- **Cooperate if and only if:** `m ≥ ⌈n/k⌉ - 1`
- **Otherwise:** Defect

The threshold `⌈n/k⌉ - 1` is the minimum number of opponent cooperators needed such that cooperating yourself could yield a payoff approaching your defection payoff. Given that defection always yields a payoff advantage, this is a high bar—cooperation only occurs if aggregated contribution is substantial enough that the public good multiplier offset becomes non-negligible.

**Round r (Terminal Round):** Defect unconditionally. In the final round, no reputation or future consequences exist; defection is strictly dominant.

**Rationale:**
This strategy recognizes that in this game's payoff structure, unilateral defection always outperforms unilateral cooperation against any fixed opponent composition. It avoids the trap of reciprocal cooperation that nets lower returns than selective defection. The cooperation threshold is set high enough that you only participate in public goods if nearly everyone is already contributing—essentially defecting as the default stance while opportunistically joining if others create sufficient surplus to justify participation.

The strategy is adaptive: it observes aggregate cooperation and pivots accordingly, while remaining self-interested by never cooperating unless the public good is dense enough to overcome the inherent defection advantage.
'''

description_SELFINTERESTED_32 = '''
# Adaptive Threshold Cooperation Strategy

## Decision Rule

**Rounds 1 to r-2 (early and middle rounds):**
Cooperate if and only if the number of cooperators observed in the previous round exceeds threshold T.

**Rounds r-1 and r (final rounds):**
Always Defect.

## Threshold Calculation

Set T = ceil(k) as the minimum cooperation threshold.

This reflects that if T or more players are cooperating, the public good generates value per cooperator of k/n. Once T players cooperate, the accumulated public good benefits exceed the cost of my endowment (1), making cooperation worth sustaining to maintain the cooperation level.

## Edge Cases

**Round 1:** Defect. Opening with defection is safe and informative—it reveals whether others will cooperate despite encountering defection.

**Final 2 rounds:** Defect regardless of history. The endgame has no future rounds to sustain, eliminating any incentive to maintain cooperation. Defecting in round r-1 signals to others that cooperation is unsustainable, accelerating their shift to defection.

**If all opponents have defected (observe 0 cooperators):** Defect in subsequent rounds until reaching the final rounds. A collapsed cooperation structure doesn't warrant unilateral contribution.

## Adaptation Logic

This strategy responds to observable cooperation trends:
- If cooperation persists above threshold, continue participating to capture the public good
- If cooperation drops below threshold, withdraw to avoid unilateral loss
- Near the end, defect to capture remaining private value before the game ends

The strategy is self-interested because it:
1. Exploits cooperative opponents by contributing only when their contributions sustain a valuable public good
2. Avoids the sucker's payoff (cooperating alone while others defect)
3. Captures the endgame gain by defecting when cooperation incentives vanish
4. Scales adaptation based on whether the cooperation rate justifies my participation cost
'''

description_OPPORTUNISTIC_5 = '''
**THRESHOLD-BASED FREE-RIDING STRATEGY**

**Parameters:**
- cooperation_threshold = n/k (minimum cooperators needed to make others' contributions worth your cost)
- last_round = r

**Decision Rule by Round:**

Round 1:
Defect. No history available; assume opponents follow their dominant strategy or are unpredictable.

Rounds 2 to r-1:
Observe the number of cooperators c_{t-1} from the previous round.

If c_{t-1} ≥ cooperation_threshold + 1:
  Defect. Exploitation opportunity: others are contributing enough that you gain (k/n) × c_{t-1} > 1 without paying the cooperation cost.

Else if c_{t-1} < cooperation_threshold:
  Defect. No opportunity: even if you cooperated, others' contributions wouldn't return sufficient value.

Else (c_{t-1} ≈ cooperation_threshold):
  Defect. The marginal benefit is uncertain; defection is the safe exploitative choice.

Round r (final round):
Defect unconditionally. No future rounds remain to build reputation or coordinate. Extract maximum immediate payoff.

**Rationale:**
This strategy treats cooperation by others as a resource to exploit rather than a signal to reciprocate. You systematically free-ride when the public good pool is rich enough to exceed your cost, and defect otherwise. The final round elimination ensures no forward-looking restraint. Adaptation occurs through observing aggregate cooperation only—no need to track individual opponents or build trust. The strategy is opportunistic because it accepts the logic that others' contributions are profitable for you to withhold from, and you only remain in the game by responding to cooperation with defection rather than reciprocation.
'''

description_OPPORTUNISTIC_6 = '''
# Opportunistic Exploitation Strategy

**Core Principle**: Defection is the dominant action (always yields +1 compared to cooperation). Exploit this asymmetry by free-riding on others' contributions while minimizing your own costs.

## Decision Rule by Round

**Round 1**: 
Defect. Establish baseline without any historical information.

**Rounds 2 to r-1 (Middle Rounds)**:
Let C_prev = number of cooperators observed in round t-1.

- If C_prev ≥ ⌈n/2⌉ (majority cooperating): **Defect**
  - High cooperation makes free-riding most profitable. Your payoff = 1 + (k/n) × C_prev, which exceeds the cooperative payoff of (k/n) × C_prev.
  
- If C_prev < ⌈n/2⌉ (minority cooperating): **Defect**
  - Cooperation yields (k/n) × C_prev ≤ (k/2) < 1, so you get more from defection.
  
- **Exception—Cooperation Signal (optional, for robustness)**: 
  - If this is round 2 and C_prev = n-1 (almost universal cooperation), cooperate once to confirm the pattern and position yourself for sustained exploitation in subsequent rounds.
  - Otherwise, defect.

**Round r (Final Round)**:
Defect unconditionally. No future rounds exist to reward reciprocity, so extract maximum immediate value.

## Opportunistic Logic

This strategy prioritizes:
1. **Consistent exploitation**: Defect against high-cooperation environments to maximize the difference between your payoff and cooperators' payoffs.
2. **No wasted investment**: Never cooperate when cooperation rates are low; there's no public good surplus to capture.
3. **Defection dominance**: Exploit the structural fact that defection always yields +1 more than cooperation given identical others' behavior.
4. **Endgame extraction**: Use the final round to capture one last unit of unreciprocated gains.

No attempt is made to sustain cooperation through reputation or signaling, since opponents are independent and anonymous.
'''

description_OPPORTUNISTIC_7 = '''
# OPPORTUNISTIC ADAPTIVE STRATEGY

## Core Principle
Always defect, strategically observing cooperation rates to identify exploitation opportunities and avoid cooperation traps.

## Decision Rules

**Round 1:**
- DEFECT
- Rationale: Dominates cooperation regardless of others' play; establishes baseline information

**Rounds 2 to r-1:**
- Let C_prev = number of opponents (out of n-1) who cooperated in the previous round
- Compute: cooperation_rate = C_prev / (n-1)
- Threshold θ = 0.5 (adjust if desired)

If cooperation_rate > θ:
  - DEFECT (free-ride on high cooperation; you capture (k/n) × C_prev while keeping your full endowment)

If cooperation_rate ≤ θ:
  - DEFECT (mutual defection is stable; cooperating alone costs 1 for (k/n) < 1 return)

**Round r (final round):**
- DEFECT (reputation carries no future value; extract maximum immediate payoff)

## Edge Cases

- **If all opponents cooperate**: DEFECT to capture the maximum payoff of 1 + (k/n) × (n-1)
- **If all opponents defect**: DEFECT maintains payoff of 1; cooperation would yield only (k/n), which is suboptimal
- **If cooperation rate is exactly at threshold**: DEFECT (break ties in favor of exploitation)
- **Round r-1 treatment**: No special treatment; apply same rule. The endgame is only the final round

## Opportunistic Logic

This strategy systematically extracts value from cooperators while avoiding coordination costs. You gain information about opponent cooperation through observation but never let that information trigger your own cooperation—only your defection strategy adapts in timing and confidence. You never reciprocate or punish; you only exploit and avoid costly mistakes.
'''

description_OPPORTUNISTIC_8 = '''
# Opportunistic Strategy

**Round 1:**
Cooperate. Establish a signal of cooperativeness to observe baseline cooperation rates and probe whether opponents will reciprocate.

**Rounds 2 through r-1 (middle rounds):**
Observe the number of cooperators c_t from the previous round.

If c_t ≥ 1 (at least one opponent cooperated):
  Defect. Exploit the public good funded by others while keeping your endowment.

If c_t = 0 (no opponents cooperated):
  Defect. No public good to exploit; match defection.

**Round r (final round):**
Defect unconditionally. No future rounds exist for punishment or reputation effects, eliminating any incentive to cooperate.

**Threshold justification:**
Since defecting always yields 1 + (k/n) × total_cooperators while cooperating yields only (k/n) × total_cooperators, defection strictly dominates whenever any public good exists. The threshold of c_t ≥ 1 captures this: any opponent cooperation creates an opportunity to free-ride.

**Opportunistic logic:**
The strategy front-loads a single cooperation to encourage others into cooperative patterns, then systematically defects once opponents reveal their willingness to contribute. By round 2+, you extract maximum value from opponents' contributions without reciprocating, and avoid paying the cooperation cost (1 unit) that your opponents bear. The final-round defection exploits the sunk expectations of continued play.
'''

description_OPPORTUNISTIC_9 = '''
# Opportunistic Probe-and-Exploit Strategy

## Core Decision Logic

**Rounds 1–2 (or until round r–1 if r = 2):** Cooperate unconditionally to signal receptiveness and probe whether opponents will reciprocate.

**Rounds 3 to r–1:** Apply the exploitation threshold.
- If `observed_cooperators[t-1] ≥ threshold`: **Defect** (exploit high cooperation)
- If `observed_cooperators[t-1] < threshold`: **Defect** (no mutual benefit in cooperating)

**Round r (final round):** **Defect** unconditionally (no future consequences; maximizes immediate payoff).

## Threshold Calculation

```
threshold = max(1, ceil((n - 1) × 0.4))
```

This represents approximately 40% of potential cooperators from other players. If fewer than this fraction cooperated last round, the public good payoff is too diluted to justify foregoing your private endowment. If more cooperated, you exploit them with defection.

## Edge Cases

- **If r = 2:** Cooperate in round 1 as a probe; defect in round 2 (final round).
- **If n = 2:** Cooperate rounds 1–2, then defect (the opponent's cooperation is entirely observable, making exploitation transparent).
- **If observed_cooperators[t-1] = 0:** Defect (no public good to share; keeping your endowment yields 1 vs. contributing for 0).

## Rationale

Early cooperation attracts reciprocal behavior from cooperative-minded opponents while establishing your presence. Once you observe which rounds yield high cooperation, you switch to defection to capture the asymmetric benefit: you keep your endowment (1) while still drawing your share of others' contributions `(k/n) × observed_cooperators`. This asymmetry is the core of opportunism—you gain the best of both worlds by shifting from contributor to free-rider once cooperation is established.
'''

description_OPPORTUNISTIC_10 = '''
# Opportunistic Adaptive Strategy

**Core Logic**: Exploit others' cooperation through selective defection while minimizing own contribution, and pivot to pure defection in endgame.

## Decision Rules

**Rounds 1 through (r - 2):**

1. Observe the proportion of cooperators from the previous round: p = c_{t-1} / n
2. Establish a dynamic cooperation threshold: θ(t) = 0.35 - (t / r) × 0.10
   - This threshold starts at 0.35 and gradually decreases as rounds progress
3. Decision:
   - If p > θ(t): **Defect** — free-ride on the established cooperation
   - If p ≤ θ(t): **Cooperate** — help maintain a minimally productive public pool to enable ongoing returns
   - If p is near θ(t) within ±0.05: **Defect** — break ties opportunistically

**Rounds (r - 1) and r (final two rounds):**
- Always **Defect** — future payoffs are zero or negligible, so extracting immediate value dominates

**Round 1 (initialization):**
- **Defect** — probe for others' baseline cooperation without committing resources

## Edge Cases and Opportunism

**If all opponents defected in previous round** (p = 0): 
- Defect in current round (no public good to free-ride on, private payoff = 1 is locked in)

**If cooperation collapses mid-game** (sharp drop in p):
- Maintain defection — continue exploiting any stragglers cooperating, pivot to all-defect if p stays near zero for 2+ consecutive rounds

**Endgame shift (round r - 1 onwards)**:
- Abandon the threshold rule entirely; defection guarantees 1 + (k/n) × c_{t-1} with zero future penalty

**Rational justification**: When others cooperate, you capture (k/n) × their contribution while keeping your full endowment. When cooperation falls below the threshold, light cooperation maintains a pool size worth exploiting in subsequent rounds. Final rounds eliminate any pretense of reciprocity since defection has no future cost.
'''

description_OPPORTUNISTIC_11 = '''
OPPORTUNISTIC STRATEGY: Adaptive Exploitation with Endgame Defection

**FIRST ROUND (t=1):** Defect
- Establish no initial commitment and observe baseline cooperation rate from the population

**MIDDLE ROUNDS (t=2 to r-1):**

Record the cooperation count c_{t-1} from the previous round.

Define threshold: θ* = k (the multiplication factor)

- **If c_{t-1} ≥ θ*:** Defect
  - Sufficient cooperators exist to generate positive public good. Free-ride by capturing (k/n) × c_{t-1} while retaining private endowment (1 - 0)

- **If c_{t-1} < θ*:** Defect
  - Insufficient critical mass for public good. Contributing yields nearly zero payoff. Defection remains optimal

- **Occasional probing (every 3 rounds when c_{t-1} = 0):** Cooperate with probability 0.15
  - If defection has collapsed cooperation entirely, low-cost probe tests whether strategic cooperation could unlock mutual gains in remaining rounds

**LAST ROUND (t=r):** Always Defect
- No future rounds create future expectations. Payoff is purely instantaneous: keeping endowment (1) plus share of others' contributions (k/n) × c_{r-1} dominates any contribution

**Justification:** This strategy maximizes individual payoff by exploiting high-cooperation states while avoiding wasted contributions in low-cooperation states. The occasional cooperation probe in collapsed states is instrumentally opportunistic—it tests whether small investments could restart cooperation, creating larger free-riding opportunities in remaining rounds. The endgame commitment to defection reflects pure payoff maximization when future reputation has zero value.
'''

description_OPPORTUNISTIC_12 = '''
# Opportunistic Threshold Exploitation Strategy

## Core Decision Rule

**For rounds 1 to r-1:**

Observe the number of cooperators C_t from the previous round. Defect if C_t exceeds a critical threshold; otherwise, cooperate conditionally.

- If C_t ≥ threshold T: **Defect** (free-ride on others' contributions)
- If C_t < threshold T: **Cooperate** (signal willingness to participate to rebuild cooperation for future exploitation)

Set threshold T = ⌈k⌉ (the smallest integer ≥ k). This ensures you only cooperate when others are contributing substantially enough to make the public good worth harvesting.

**For round r (final round):** **Always defect** (no future punishment possible; extract maximum value).

## Edge Cases and Implementation

**Round 1:** Defect unconditionally. This establishes credibility as someone willing to free-ride and tests opponent cooperation levels.

**Round 2 onward:** Apply threshold rule based on observed C_{t-1}.

**When C_t = threshold T exactly:** Defect. You've reached the cooperation level needed to exploit; extraction is optimal.

**When cooperation collapses (C_t = 0):** Cooperate. With mutual defection emerging, offering cooperation can restart cycles of cooperation you can then exploit again.

**Final round adjustment:** If round r-1 shows C_{r-1} ≥ T, defect in round r. If C_{r-1} < T, you may cooperate in round r-1 to potentially restart cooperation, but defect in round r regardless.

## Opportunistic Logic

This strategy maximizes exploitation by:
- Capturing individual gains whenever aggregate cooperation is sufficient (defect when C_t ≥ k)
- Avoiding mutual defection collapse by cooperating only when others have stopped, signaling potential for renewed exploitation
- Abandoning all reciprocity in the final round to claim the maximum possible payoff
- Treating cooperation purely as a tool to sustain high-cooperation states you can free-ride on, not as a normative commitment
'''

description_OPPORTUNISTIC_13 = '''
# Greedy Exploitation with Adaptive Switching

**State tracking:** Maintain a record of cooperation_t for each round t ∈ {1, ..., t-1}, where cooperation_t is the number of players who cooperated in round t.

**Round 1 (Initial):** Play D. Establish a baseline by free-riding with certainty, gathering information about opponent composition.

**Rounds 2 to r-1 (Middle rounds):** 
- Calculate the payoff threshold: threshold = ⌈n/k⌉
- If cooperation_{t-1} ≥ threshold: Play C
  - Rationale: Others have cooperated enough that your share (k/n) × cooperation_{t-1} ≥ 1, making cooperation at least as valuable as defection's fixed +1 payoff. Exploit their contributions.
- Else if cooperation_{t-1} < threshold: Play D
  - Rationale: Cooperation is scarce. Free-ride on the minimal common pool and secure your +1 defection premium.

**Final round r:** Play D unconditionally. No future rounds exist for other players to react or punish, so extract maximum immediate value.

**Adaptation logic:** The strategy continuously reassesses viability. If opponents shift toward higher cooperation, immediately switch to parasitizing it. If cooperation collapses (detecting widespread defection), revert to pure defection. This exploits upswings and abandons losing positions.

**Edge case - tie in threshold:** If cooperation_{t-1} = threshold, play C (marginal gain from the public good offsets indifference, while positioning as a potential reciprocator if others increase cooperation).
'''
