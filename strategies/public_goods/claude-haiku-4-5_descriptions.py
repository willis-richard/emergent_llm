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
