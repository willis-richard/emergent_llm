"""
Strategy descriptions for collective_risk.

Generated with:
- Provider: Anthropic
- Model: claude-haiku-4-5
"""


description_COLLECTIVE_1 = '''
# Adaptive Threshold Cooperation Strategy

## Decision Rules

**Round 1:** Cooperate unconditionally.

**Rounds 2 to r-1:**
- Let c_prev = number of opponents observed cooperating in the previous round
- **Cooperate** if: c_prev + 1 ≥ m (your cooperation is pivotal for reaching threshold)
- **Defect** otherwise

**Round r (final round):**
- Let c_prev = number of opponents observed cooperating in round r-1
- **Cooperate** if: c_prev + 1 ≥ m (last chance to secure collective payoff)
- **Defect** otherwise

## Edge Cases

**First round only:** Always cooperate. This establishes a baseline signal of willingness and generates the first observation to ground future decisions.

**When m = 1:** Cooperation is triggered by any single player. After round 1, every player observes c_prev ≥ 1, so the condition c_prev + 1 ≥ 1 is always true. All players cooperate every remaining round, achieving universal cooperation.

**When m = n:** All players must cooperate. Round 1 has universal cooperation, so all observe c_prev = n-1. The condition (n-1) + 1 ≥ n is satisfied, sustaining universal cooperation through all remaining rounds.

**When c_prev ≥ m already:** Defect. The threshold is already secured without you; individual payoff maximization applies, as your cooperation adds nothing (0 vs 1+k).

**When c_prev < m-1:** Defect. Even with your cooperation, the threshold c_prev + 1 cannot be reached. Cooperation yields 0; defection yields 1.

## Collective Alignment

The strategy explicitly cooperates **only when pivotal**—when your individual cooperation determines whether the collective crosses the threshold. This minimizes wasted cooperation on unmet thresholds while maintaining reliable threshold-hitting when others are cooperating.

By always cooperating in round 1, the strategy initiates a trust signal. In subsequent rounds, it cooperates conditionally based on observed reciprocal willingness, creating a stable equilibrium where the threshold is repeatedly met and all players receive k across all rounds.
'''

description_COLLECTIVE_2 = '''
# Collective Threshold Response Strategy

**First Round (t=1):**
Cooperate unconditionally. This signals genuine intent to participate in the collective project and avoids the bootstrap problem of having no cooperation history.

**Subsequent Rounds (2 ≤ t ≤ r):**

1. Calculate the empirical cooperation frequency from all previous rounds:
   ```
   coop_rate = (total cooperators observed in rounds 1..t-1) / ((t-1) × (n-1))
   ```

2. Estimate the expected number of cooperators in round t:
   ```
   expected_cooperators = coop_rate × (n-1) + 1
   ```
   (This is: expected others plus yourself)

3. Decision rule:
   ```
   If expected_cooperators ≥ m:
       Cooperate
   Else:
       Defect
   ```

**Rationale:**
- Cooperate when reaching the threshold m appears achievable based on observed behavior
- This creates a "critical mass" dynamic: if enough others have cooperated historically, you cooperate to push over the threshold
- Defect only when the empirical frequency suggests the collective project will fail anyway
- Apply the same logic uniformly through the final round—don't abandon cooperation arbitrarily at the end if the threshold remains achievable

**Edge Case - All Defection Detected:**
If coop_rate = 0 after round 1, defect in all subsequent rounds, since no amount of your cooperation alone reaches m.

**Edge Case - Threshold Impossible:**
If m > n, which violates the parameters, this strategy remains well-defined; the condition would never be satisfied.

This strategy commits to the collective good when conditions support success, withdraws only when cooperation appears futile, and treats all rounds equally in importance.
'''

description_COLLECTIVE_3 = '''
# Threshold Cooperation with Adaptive Belief Updating

**Core Principle:** Cooperate when threshold success appears achievable with your contribution; defect when the threshold is already exceeded or demonstrably unachievable.

## Decision Rule

**State Tracking:** Maintain a running count of cooperators observed across all prior rounds.

```
Let c_observed = total number of cooperators observed in rounds 1 to t-1
Let rounds_elapsed = t - 1
Let avg_cooperation_rate = c_observed / (rounds_elapsed * (n-1))
```

**General Rounds (1 ≤ t < r):**

If t = 1:
  - Play C

If t > 1:
  - Estimate expected cooperators in round t as: exp_coop = avg_cooperation_rate × (n-1)
  - If (exp_coop + 1) ≥ m: Play C
  - Else: Play D

Intuition: Cooperate only if your cooperation is pivotal—closing the gap to threshold m. If cooperation already exceeds m-1 or falls short and cannot be rescued, defect.

**Final Round (t = r):**

- Calculate exp_coop as above
- If exp_coop ≥ m - 1: Play C (provide the final push to collective success)
- Else: Play D (threshold is unattainable; preserve private payoff)

## Edge Cases

**Early Asymmetry:** If rounds 1-2 yield 0 cooperators, avg_cooperation_rate becomes 0. Continue applying the rule; play D until evidence of viable cooperation emerges. This avoids throwing payoffs at a collapsed threshold.

**Unanimous Defection Trap:** If all opponents defect consistently and n-1 < m-1 (impossible to reach threshold unilaterally), immediately transition to always D.

**Sudden Spikes:** If cooperation jumps unpredictably, the averaging approach absorbs noise. A single spike does not trigger sustained cooperation unless the rate stabilizes.

**Majority-Threshold Alignment:** When m > n/2, threshold success requires near-universal cooperation. The strategy becomes correspondingly stringent: defect unless evidence strongly suggests others will cooperate.

## Collective Alignment

The strategy treats reaching the threshold as a shared goal. You do not exploit others once cooperation is viable (you don't defect when you'll reach m anyway). You also do not subsidize uncooperative environments—defection is strict when the threshold is mathematically unachievable or has already been exceeded without your input. The final round check ensures you contribute to collective success if it remains within grasp.
'''

description_COLLECTIVE_4 = '''
**THRESHOLD-RESPONSIVE CONDITIONAL COOPERATION**

**Decision Rule:**

Round 1: Cooperate

Rounds 2 through r: 
- Observe the number of opponents who cooperated in the immediately preceding round, call this C_prev
- If C_prev ≥ m - 1 (meaning including yourself, at least m total would cooperate): Cooperate
- If C_prev < m - 1 (threshold cannot be reached): Defect

**Interpretation of the threshold check:**
You are tracking whether others are meeting the requirement. If m - 1 or more of your opponents cooperated in the previous round, then your cooperation brings the total to at least m, triggering the collective payoff. If fewer than m - 1 opponents cooperated, no amount of individual cooperation achieves the threshold, so defect to preserve endowment.

**Handling the final round (round r):**
Apply the same decision rule. Do not deviate to exploitation in the final round; maintain consistency with earlier rounds to preserve the signal of commitment.

**Collective alignment:**
This strategy embodies collective rationality by:
- Opening with cooperation as a normative gesture, establishing willingness to sacrifice for group benefit
- Maintaining cooperation only when others reciprocate sufficiently to guarantee threshold achievement—avoiding wasted contribution
- Withdrawing cooperation when the collective is no longer viable, preventing costly free-riding dynamics
- Never deviating opportunistically, which would undermine the coordination problem

**Robustness properties:**
- Against pure defectors: Quickly detects threshold failure and stops cooperating
- Against conditional cooperators: Reaches mutual cooperation equilibrium
- Against mixed strategies: Responds dynamically to the observed cooperation level each round
'''

description_PROSOCIAL_1 = '''
**Adaptive Threshold Cooperation Strategy**

**Round 1 (Initial Signal):**
Cooperate unconditionally. This signals commitment to the collective good and allows you to observe baseline behavior.

**Rounds 2 through r-1 (Adaptive Maintenance):**
- Calculate the moving average cooperation rate among opponents: `avg_coop = (total opponent cooperations in previous rounds) / ((t-1) * (n-1))`
- Estimate expected cooperators next round if I cooperate: `expected = avg_coop * (n-1) + 1`
- **Decision rule:** Cooperate if `expected ≥ m`. Defect if `expected < m`.

The logic: If your cooperative action, combined with the historical trend, plausibly carries the group to the threshold, cooperate. If the threshold appears unreachable even with your contribution, defect to minimize loss.

**Round r (Final Round):**
Apply the same decision rule as rounds 2-r-1. The finality of round r does not warrant deviation—consistent application of the threshold-matching logic maintains credibility across the entire interaction.

**Edge Cases:**

- **Insufficient history (early rounds):** For round 2, if no prior cooperation exists, use round 1 observed count directly: if at least `m-1` opponents cooperated in round 1, assume continuation and cooperate in round 2. If 0 cooperators in round 1, defect in round 2 but recalculate for round 3.

- **Oscillating cooperation:** If `avg_coop` is borderline (e.g., expected = m ± 0.2), break ties in favor of cooperation—this is the prosocial bias.

- **Complete defection by others:** If `avg_coop ≈ 0` persistently, defecting minimizes your cumulative loss while avoiding purely self-interested exploitation if the threshold were somehow met.

This strategy cooperates generously while remaining rational about feasibility, avoiding both pure sacrifice and parasitic free-riding.
'''

description_PROSOCIAL_2 = '''
**ADAPTIVE THRESHOLD SUPPORT STRATEGY**

**Round 1:**
Cooperate unconditionally. Signal prosocial intent and establish baseline expectation of cooperation.

**Rounds 2 through r-1 (Middle rounds):**

Observe: Let *opp_coop* = number of opponents who cooperated in the previous round.

Calculate: *deficit* = max(0, m - 1 - opp_coop)
- This is how many additional cooperators are needed (beyond last round's count) to reach the threshold, assuming you are the player in question.

Decision rule:
- If *deficit* > 0: Cooperate
  - The threshold was not reached or is fragile. Your contribution materially helps reach it.
- If *deficit* ≤ 0: Defect
  - The threshold was clearly met. Others' cooperation is sufficient; free-ride on their contribution.

**Round r (Final round):**

Observe: *avg_opp_coop* = average number of opponent cooperators across rounds 2 through r-1.

Decision rule:
- If *avg_opp_coop* < (m - 1): Cooperate
  - Opponent cooperation has consistently fallen short. Make a final effort to reach the threshold on the last chance.
- If *avg_opp_coop* ≥ (m - 1): Defect
  - Opponents have reliably supported the threshold. Reputational incentives no longer bind; capture the final-round advantage.

**Tie-breaking and edge cases:**

- If at any decision point the calculation is ambiguous or you are uncertain whether the threshold will be met, default to Cooperate. Uncertainty resolves prosocially.
- If n = 2 or m = n, adjust the deficit calculation to account for the reduced margin: deficit = max(0, m - 1 - opp_coop).
'''

description_PROSOCIAL_3 = '''
# Prosocial Threshold-Responsive Strategy

## Decision Rule: Conditional Cooperation with Adaptive Threshold Assessment

**State Tracking:**
- Maintain a count of observed cooperators in each previous round: observed[t] for round t ∈ {1, ..., t-1}
- Calculate the rolling average cooperation count among opponents: avg_cooperators = mean(observed[1:t-1])

**Cooperation Decision:**

- **Round 1:** Cooperate
  - Rationale: Establish prosocial signal and gather baseline information.

- **Rounds 2 to r-1 (intermediate rounds):**
  - **If avg_cooperators ≥ m - 1:** Cooperate
    - The threshold is achievable with your contribution. Sustain cooperation.
  - **If avg_cooperators < m - 1 AND never observed ≥ m - 1 cooperators:** Defect
    - Threshold unattainable; avoid wasting endowment.
  - **If avg_cooperators < m - 1 BUT previously observed ≥ m - 1 cooperators:** Cooperate with probability proportional to (max_observed - m + 1) / (n - 1)
    - Give cooperation a chance to recover; decay this probability as rounds progress.

- **Round r (final round):**
  - **If avg_cooperators ≥ m - 1:** Cooperate
    - Secure the final gain and end on cooperative signal.
  - **If avg_cooperators < m - 1:** Defect
    - No future rounds remain; no strategic reason to sacrifice endowment when threshold is unmet.

## Edge Cases

**Perpetual defection by opponents:**
If you never observe ≥ m - 1 cooperators by round ⌈r/3⌉, switch to permanent defection for remaining rounds.

**High variability in cooperation:**
If std_dev(observed) is high (suggesting volatile group behavior), weight recent rounds more heavily: avg_cooperators = weighted_mean where weight(t) increases with t.

**First observation of threshold:**
If you observe exactly m - 1 cooperators in round t (others cooperate, threshold met), reciprocate by cooperating in round t+1 if not already doing so.

## Prosocial Alignment

- **Initiation:** Start cooperating unconditionally to propose mutual benefit and reduce others' uncertainty about your type.
- **Reciprocity:** Continue cooperation as long as the group demonstrates sufficient willingness to reach the threshold, rewarding collective efforts.
- **Graceful exit:** Only defect when empirical evidence shows the threshold is persistently unachievable, minimizing wasteful contributions while preserving group welfare in viable scenarios.
- **Hope:** Maintain a conditional recovery mechanism that allows cooperation to resume if group behavior improves, rather than defecting permanently after one bad round.
'''

description_PROSOCIAL_4 = '''
# Adaptive Threshold Cooperation Strategy

## Decision Rule

**Round 1:** Always cooperate.

**Rounds 2 through r:**

1. Calculate the empirical cooperation rate among opponents using all available history:
   - observed_cooperators = total count of opponent cooperations across rounds 1 to t-1
   - observed_rounds = (t-1) × (n-1)
   - cooperation_rate = observed_cooperators / observed_rounds

2. Estimate the expected number of cooperators among the n-1 opponents in the current round:
   - expected_others = cooperation_rate × (n-1)

3. Decision:
   - If 1 + expected_others ≥ m: **Cooperate**
   - Else: **Defect**

## Edge Cases

**First round:** Cooperate unconditionally. This signals prosocial intent and avoids the worst collective outcome (everyone defecting, where you earn only 1).

**Insufficient history:** In round 2, you have only one previous round of data. Use it as given; the estimate becomes more stable in later rounds.

**Fractional expectations:** Round down when expected_others is not an integer. This reflects conservative estimation—cooperate only if you have clear evidence others will cross the threshold.

**Divergent cooperation patterns:** Treat all observed rounds equally in the moving average. Do not weight recent rounds differently or apply decay factors.

**Final round:** Apply the same decision rule as any other round. Do not defect opportunistically in round r simply because it is the last round.

## Prosocial Alignment

This strategy embodies prosocial behavior by:

- **Initiating cooperation:** Playing C first demonstrates willingness to contribute and achieve the collective benefit.
- **Conditional reciprocity:** You maintain cooperation precisely when aggregate behavior suggests the threshold can be met, directing your contribution toward the outcome that benefits everyone.
- **Self-protection through threshold logic:** You defect only when historical data indicates too few others cooperate to reach m, preventing exploitation of your endowment.
- **Temporal consistency:** You do not abandon cooperation in the final round, avoiding the free-rider impulse that undermines collective outcomes.
- **Transparency to learning:** Your strategy responds predictably to observable cooperation, creating implicit incentives for others to cooperate.
'''

description_ALTRUISTIC_1 = '''
**Altruistic Adaptive Threshold Strategy**

**Initial Round (t = 1):**
Cooperate unconditionally. This signals willingness to invest in the collective good.

**Middle Rounds (1 < t < r):**

Observe the number of cooperators in the previous round: let O_{t-1} denote this count.

- If O_{t-1} + 1 ≥ m: Cooperate. The threshold is reachable with your contribution.
- If O_{t-1} + 1 < m but O_{t-1} ≥ m - 1: Cooperate. You are close to threshold; contribute to tip it.
- If O_{t-1} < m - 1: Cooperate with probability p = (m - 1 - O_{t-1}) / (n - 1). This calibrates contribution to the remaining gap. If many are still needed, boost your willingness to fill the gap. If few more are needed, cooperate with lower probability (they may be coming).

**Final Round (t = r):**
Cooperate unconditionally. On the last opportunity, ignore personal payoff and prioritize the collective outcome. Do not defect to pocket the extra endowment unit.

**Rationale for Altruism:**
- Cooperating early establishes good faith and models the behavior you want others to adopt.
- In middle rounds, the probabilistic rule ensures you contribute more when the community is struggling and less when others are stepping up—matching effort to collective need rather than free-riding on others.
- On the final round, you have no reputation to protect, so pure altruism applies: you sacrifice your endowment if it gives the community a chance.

**Edge Case — All Rounds Remain Deficient:**
If cooperation never reaches m across all previous rounds, continue the probabilistic contribution rule through round r-1, then cooperate in round r. This avoids cynical abandonment.
'''

description_ALTRUISTIC_2 = '''
# Altruistic Threshold Pursuit Strategy

**Core Decision Rule:**

In each round, cooperate if and only if:
- You believe the threshold m is achievable given observed opponent cooperation, OR
- Cooperation in this round would materially increase the likelihood of future threshold achievement

**Specific Implementation:**

**Round 1 (first round):**
Cooperate unconditionally. Signal willingness to contribute.

**Rounds 2 through r-1 (middle rounds):**
Observe c_opp = number of opponents who cooperated in the previous round.

- If c_opp ≥ m - 1: Cooperate. The threshold is achievable if you contribute.
- If c_opp = m - 2: Cooperate. Close the gap yourself; a single contribution from you completes the threshold.
- If c_opp < m - 2: Cooperate with probability p = min(0.9, (m - 1 - c_opp) / (n - 1)). 
  - This probability increases as others fall further short, incentivizing participation when help is most needed.
  - Cap at 0.9 to preserve some robustness against permanent defection cascades.

**Round r (final round):**
Observe c_opp from round r-1.

- If c_opp ≥ m - 1: Cooperate. Secure the final collective payoff.
- If c_opp = m - 2: Cooperate. A final cooperative act ensures threshold achievement.
- If c_opp < m - 2: Cooperate with probability p = min(0.8, (m - 1 - c_opp) / (n - 1)).
  - Slightly lower probability than middle rounds (0.8 vs 0.9) because defection in the final round cannot be "corrected" by future rounds.
  - However, still pursue altruistic cooperation rather than pure defection.

**Edge Cases:**

- If m = n (unanimous cooperation required): Use the same rule; cooperation probability reflects the growing difficulty of coordination.
- If m = 2 (minimal threshold): Cooperate unless opponent defection is overwhelming and persistent (c_opp = 0 for two consecutive rounds), then defect once to test if they shift.
- Restart probability fresh each round; do not accumulate "defection counters" that trigger permanent exit.

**Altruistic Alignment:**

This strategy prioritizes threshold achievement over individual payoff maximization. You never defect simply because defection yields 1 + k vs k; instead, you cooperate to enable collective success. You scale cooperation probabilistically downward only when the threshold becomes empirically unachievable, and you maintain hope through the final round.
'''

description_ALTRUISTIC_3 = '''
# Altruistic Threshold-Targeting Strategy

**Core Logic**: Cooperate to facilitate reaching the m-player threshold, treating it as a collective goal. Adapt based on observed cooperation patterns, withdrawing support only when continued cooperation becomes futile.

## Decision Rule

```
Maintain: others_coop[t] = count of other players cooperating in round t

For each round t from 1 to r:
  
  If t == 1:
    action = COOPERATE
    // Initial move: signal willingness and gather baseline information
  
  Else if t == r:  // Final round
    If others_coop[t-1] >= m - 1:
      action = COOPERATE
      // Others demonstrated cooperation; contribute to secure mutual benefit
    Else:
      action = DEFECT
      // Insufficient demonstrated cooperation; no future rounds to influence
  
  Else:  // Rounds 2 to r-1
    If others_coop[t-1] >= m - 1:
      action = COOPERATE
      // Threshold nearly secured by others; complete it
    
    Else if others_coop[t-1] == m - 2:
      action = COOPERATE
      // Your cooperation alone would complete the threshold; make it happen
    
    Else if others_coop[t-1] < m - 2:
      action = DEFECT
      // Gap too large to bridge; insufficient critical mass for threshold
      // Preserve capital for possible future cooperation phases
```

## Altruistic Alignment

**Round 1 initiation**: Unconditionally cooperate to signal genuine commitment and avoid self-fulfilling prophecies of mutual defection.

**Threshold pursuit**: Cooperate when you observe ≥ m-2 others cooperating, since reaching exactly m produces collective payoff k for all players. Your marginal contribution is altruistically valuable.

**Graceful withdrawal**: Defect only when observed cooperation is too sparse (< m-2) to justify continued individual sacrifice. This preserves resources while avoiding futile repetition.

**Last-round consideration**: Even in round r, cooperate if others have demonstrated the threshold is achievable. The altruistic stance prioritizes the group outcome over individual extraction in the final turn.

## Edge Cases

- **Very small n** (n=3, m=2): After round 1, one other cooperator triggers continued cooperation.
- **Strict majority threshold** (m near n): Strategy defects early if observed cooperation drops below critical level; recognizes the bar is high.
- **Single round** (r=1): Cooperate, then observe. No adaptation possible, but the default cooperative stance reflects altruistic intent.
'''

description_ALTRUISTIC_4 = '''
# Altruistic Collective Risk Strategy

**Core Philosophy:** Cooperate to enable collective success, calibrated by evidence that cooperation can meaningfully contribute to reaching the threshold.

## Decision Rules

**Round 1:**
Cooperate unconditionally. Signal willingness to contribute and provide a baseline observation point for others.

**Rounds 2 through r-1 (Middle Rounds):**
Let c = number of cooperators observed in the immediately previous round.

- **If c ≥ m:** Cooperate. The threshold is already met; cooperation maintains collective success and demonstrates commitment to group welfare.

- **If m-2 ≤ c < m:** Cooperate. The threshold is nearly achieved. Your cooperation has a direct path to enabling collective payoff.

- **If ⌈(m-1)/2⌉ ≤ c < m-2:** Cooperate. Substantial cooperation is present. Contribute to the joint effort even though the threshold isn't guaranteed; this signals reciprocal willingness.

- **If c < ⌈(m-1)/2⌉:** Defect. Cooperation is unlikely to reach the threshold given the observed defection rate. Preserve endowment when contribution cannot plausibly shift the outcome.

**Round r (Final Round):**
Apply a persistence rule tilted toward cooperation:

- **If c ≥ m-1:** Cooperate. The threshold is reachable in this round; cooperation achieves or maintains collective success.

- **If ⌈(m-1)/2⌉ ≤ c < m-1:** Cooperate. Altruism means making a final effort to cross the threshold rather than ensuring personal payoff maximization.

- **If c < ⌈(m-1)/2⌉:** Defect. In the final round, if cooperation cannot plausibly contribute to threshold achievement, accept the outcome.

## Edge Cases

- **Rounds where m = n:** Cooperate every round except the last (where defection is then rational). This is the only case where threshold is impossible without your contribution.

- **Observation of all defection (c = 0):** Defect in the next round; continued unilateral cooperation provides no collective benefit.

- **First evidence of threshold achievement (c ≥ m):** Maintain cooperation indefinitely thereafter to sustain the collective outcome.

## Altruistic Alignment

This strategy accepts personal losses (cooperating when others defect) to enable collective success whenever that cooperation has a non-negligible path to the threshold. It avoids both naive cooperation (contributing when cooperation is futile) and pure free-riding. By conditioning on observable progress toward m, the strategy demonstrates reciprocal commitment: altruism paired with adaptive judgment about where sacrifice creates actual collective value.
'''

description_BENEVOLENT_1 = '''
**BENEVOLENT THRESHOLD-RESPONSIVE STRATEGY**

**Decision Rule - General Form:**

For each round t, observe the number of cooperators in round t-1, denoted as c_{t-1}. Cooperate if and only if the observed cooperation level suggests the threshold is achievable within the remaining game window.

**Round 1 (Opening):**

Play C unconditionally. This signals good-faith willingness to contribute and gives the group the best possible starting position for coordination.

**Rounds 2 through r-1 (Middle Rounds):**

Let c_{t-1} = observed number of cooperators in the previous round.

- If c_{t-1} ≥ m: Play C (the threshold was already met; sustain success)
- If c_{t-1} = m-1: Play C (one cooperator away from threshold; give another chance to coordinate)
- If m-1 < c_{t-1} < m: Play C (within striking distance; contribute to push over threshold)
- If c_{t-1} < m-1 and c_{t-1} ≥ ceil(m/2): Play C (moderate baseline cooperation exists; try to catalyze success)
- If c_{t-1} < ceil(m/2): Play D (coordination appears infeasible; defect to avoid unilateral cost)

**Round r (Final Round):**

Let c_{r-1} = observed cooperators in round r-1.

- If c_{r-1} ≥ m-1: Play C (threshold within reach in final round; attempt to secure group success)
- If c_{r-1} < m-1: Play D (no realistic path to threshold; no future consequences to manage)

**Rationale:**

This strategy is benevolent because it prioritizes enabling collective success over individual payoff maximization. It cooperates early unconditionally, responds cooperatively to any moderate or strong cooperation signal from others, and maintains cooperation when the threshold is close or already achieved. It only defects when coordination appears genuinely impossible, not opportunistically when victory is assured. The final-round rule balances benevolence with realism: it still tries to help the group cross the finish line if plausible, but accepts when further sacrifice is futile.
'''

description_BENEVOLENT_2 = '''
# BENEVOLENT ADAPTIVE THRESHOLD STRATEGY

**CORE PRINCIPLE:** Cooperate to enable collective success while avoiding systematic exploitation. Give others opportunities to coordinate without punishing honest defections too harshly.

## DECISION RULES

**Round 1 (First round):**
Cooperate unconditionally. Signal benevolent intent and willingness to bear cost.

**Rounds 2 through r-1 (Middle rounds):**
1. Let `others_cooperated_last = cooperation count from previous round, excluding self`
2. Let `avg_cooperation_rate = mean proportion of others cooperating across all prior rounds`
3. Let `expected_cooperators = avg_cooperation_rate × (n-1)`

Cooperate if ANY of these hold:
- `others_cooperated_last ≥ m-1` — Threshold was reachable last round; continue effort
- `expected_cooperators ≥ m-1.5` — History suggests we can reach threshold; invest in it
- `t < r/2 AND expected_cooperators > 0` — Early enough to build momentum; give others time
- `t < round(r×0.75) AND others_cooperated_last > 0` — Recent signal of willingness; extend trust
- No prior round showed zero cooperators — Others have tried; mutual exploration phase

Otherwise, Defect. (Clear pattern of sustained free-riding by others.)

**Round r (Final round):**
- If `others_cooperated_last ≥ m-1` — Attempt final success: Cooperate
- Else if `expected_cooperators ≥ m-1.5` — Last chance for threshold: Cooperate
- Else: Defect — Minimize final loss when threshold seems unattainable

## BENEVOLENT CHARACTERISTICS

- **Initiates cooperation** to offer others the path to mutual gain
- **Tolerates variance** in others' behavior; doesn't punish temporary defection with immediate retaliation
- **Absorbs cost** of reaching threshold (cooperates even when slightly uncertain) rather than free-riding on others' contributions
- **Extends deadlines** for others to reciprocate across multiple rounds before withdrawing
- **Pivots only when evidence is clear** — systematic defection with no willingness signal, not isolated defections
'''

description_BENEVOLENT_3 = '''
**STRATEGY: Adaptive Threshold Pursuit**

**Round 1:**
Cooperate. Signal willingness to contribute and provide initial empirical anchor for cooperation feasibility.

**Rounds 2 through r-1 (middle rounds):**

Let c_t denote the number of cooperators observed in round t.

1. **If c_t ≥ m - 1:** Defect. The threshold will be met without your contribution, so cooperate only if you can make a marginal difference.

2. **If c_t < m - 1:** Calculate the deficiency: δ = m - 1 - c_t. 
   - If δ ≤ 1 and (r - t) ≥ 2: Cooperate. Invest one contribution to potentially unlock k for all future rounds.
   - If δ ≤ 2 and (r - t) ≥ 3: Cooperate. The future gains from reaching threshold outweigh current endowment loss.
   - If δ > 2 or (r - t) ≤ 1: Defect. Cooperation is too unlikely to recover, or insufficient rounds remain to justify the loss.

3. **Trend adjustment:** If cooperation increased from round t-1 to round t and you defected in t-1, cooperate in t to rejoin the emerging cooperative momentum.

**Final Round (t = r):**

Defect unconditionally. 

Cooperation in the final round yields 0 payoff if the threshold fails (1 - 1 + 0) and provides no benefit to future rounds. If the threshold will be met anyway (c_{r-1} ≥ m - 1), defection yields k extra. If it won't be met, cooperation wastes the endowment.

**Summary of Decision Rule:**
- Early rounds: Cooperative signal with adaptive retreat based on observed feasibility.
- Defect when marginal contribution doesn't matter (others will succeed without you).
- Cooperate when closing small gaps (δ ≤ 1 or 2) with time horizon to recover.
- Final round: Always defect to secure the maximum individual payoff given the predetermined state.
'''

description_BENEVOLENT_4 = '''
# Adaptive Cooperation with Threshold Targeting

## Decision Rule

**Round 1:** Cooperate unconditionally.

**Rounds 2 to r-1:** 
Let c_{t-1} denote the observed number of cooperators in the previous round, and R = r - t the number of remaining rounds.

- If c_{t-1} ≥ m: Cooperate
- Else if c_{t-1} = m - 1: Cooperate  
- Else (c_{t-1} < m - 1):
  - Calculate remaining deficit: d = m - c_{t-1} - 1 (additional cooperators needed beyond yourself)
  - If d ≤ R: Cooperate (enough rounds remain for threshold to plausibly form)
  - If d > R: Defect (mathematically impossible to reach threshold)

**Round r (final round):**
- If c_{r-1} ≥ m: Cooperate
- Else: Defect

## Edge Cases

- **Empty round 1:** No history exists, so assume benevolent intent from others
- **When m = n:** Only all-cooperation yields the reward; defect in round r regardless of history since no future reciprocation is possible
- **When m = 2 and n = 2:** After round 1, if opponent defected, the threshold cannot be met (d = 1 and only self remains as potential cooperator); defect in remaining rounds
- **Ties in deficit calculation:** If d exactly equals R, cooperate to give threshold formation one last chance

## Benevolent Alignment

This strategy embodies benevolence through:
- **Initial trust:** Opens with cooperation, giving others benefit of doubt
- **Threshold sustainability:** Once m cooperators are reached, maintains contribution to protect the collective good even when defection is individually rational
- **Realistic optimism:** Continues cooperating when threshold formation remains mathematically plausible, rather than abandoning it prematurely
- **Graceful exit:** Defects only when continuation becomes futile (insufficient rounds or established failure), avoiding pure altruistic losses
- **Last-round honesty:** Does not exploit others in the final round; cooperates only if success is already secured

The strategy avoids naive sacrifice while consistently working toward mutual benefit whenever feasible.
'''

description_SELFISH_1 = '''
# Selfish Threshold Defection Strategy

**Core Logic: Cooperate only when pivotal; defect otherwise.**

## Decision Rule by Round Type

**Round 1 (Initial):**
Cooperate. With minimal information, cooperation signals a willingness to achieve the threshold and allows you to observe others' baseline behavior.

**Round r (Final):**
Always defect. There is no future period where pivotal behavior can yield returns. Securing the 1-unit private endowment dominates any hope of threshold completion.

**Rounds 2 through r-1 (Intermediate):**
- If observed_cooperators_last_round ≥ m: Defect (threshold already met; free ride and collect k)
- If observed_cooperators_last_round == m - 1: Cooperate (you are pivotal; your cooperation triggers k while defection leaves you with 0)
- If observed_cooperators_last_round < m - 1: Defect (threshold unreachable even with your cooperation; defection saves the endowment cost)

## Pseudocode

```
observed_cooperators = 0

FOR t in 1 to r:
  
  IF t == 1:
    action ← COOPERATE
  
  ELSE IF t == r:
    action ← DEFECT
  
  ELSE:  // t in {2, ..., r-1}
    IF observed_cooperators == m - 1:
      action ← COOPERATE
    ELSE:
      action ← DEFECT
  
  play action
  observe observed_cooperators for this round
```

## Edge Cases

- **Threshold met in some rounds, missed in others:** Pivot detection resets each round based on fresh observation. No memory accumulation across rounds.
- **m = n (everyone must cooperate):** You defect until round r-1 observes n-1 others cooperating, then cooperate in the penultimate round if such observation occurs.
- **m = 2 (only two cooperators needed):** You defect unless you observe exactly 1 other cooperator.

## Selfish Alignment

This strategy maximizes individual payoff by minimizing cooperation costs (always stay at payoff 1 when possible) while capturing collective rewards (k) only when your defection would forfeit them. You exploit others' cooperation when the threshold is already secure, and cooperate only when your individual action is **necessary** to unlock a payoff gain you would otherwise lose.
'''

description_SELFISH_2 = '''
# Selfish Threshold-Matching Strategy

**Decision Rule:**

Cooperate in round t if and only if the number of cooperators among opponents in round t-1 is at least m-1. Otherwise defect.

**Pseudocode:**

```
round 1:
  action := D

for round t in 2 to r:
  observed_cooperators := count of opponents who cooperated in round t-1
  if observed_cooperators >= m-1:
    action := C
  else:
    action := D
```

**Logic:**

This strategy exploits the threshold structure for selfish gain:

- **When to free-ride**: If m-1 or more opponents cooperated last round, expect similar behavior this round. Cooperate because the threshold will likely be met, and you receive the reward k minus only your cost of 1, while your contribution is nearly guaranteed to be decisive or at worst redundant.

- **When to avoid waste**: If fewer than m-1 opponents cooperated last round, the threshold is unlikely to be reached next round even with your contribution. Defect to keep your full endowment of 1, since you won't enjoy the reward k anyway.

- **Round 1 assumption**: Defect with no history. Without information, assume cooperation is sparse and threshold failure is probable. Expecting low cooperation in early rounds aligns with defecting to preserve capital.

- **Round r (final round)**: Apply the same rule. No end-game effect changes the payoff structure, so strategy remains consistent.

**Adaptation to history:**

The strategy uses only the immediately preceding round's aggregate count, giving recent behavior full weight. This tracks shifts in opponent cooperation rates efficiently and adjusts your contribution decision to likely threshold success in each subsequent round.
'''

description_SELFISH_3 = '''
# STRATEGY: Adaptive Threshold-Dependent Defection

## Core Decision Rule

Maintain a running estimate of how many cooperators to expect based on observed history.

For each round t:

1. **Compute expected cooperator count:**
   - If t = 1: `expected_coop = m` (neutral prior)
   - If t > 1: `expected_coop = observed_cooperators_in_round_(t-1)`

2. **Decision:**
   - If `expected_coop ≥ m`: **DEFECT** (threshold will be met; free-ride on others' contributions)
   - If `expected_coop < m`: **COOPERATE** (threshold at risk; contribute to increase odds)

## Edge Case Handling

**Round 1:** 
- If k > 1 and m ≤ n/2: **COOPERATE** (threshold likely reachable, reward substantial)
- If m > n/2: **DEFECT** (threshold unlikely, private payoff safer)

**Last round (t = r):**
- Apply the main rule unchanged. End-game behavior is identical since no future rounds to influence.

**When expected_coop = m (exactly at threshold):**
- **DEFECT**. If others cooperated last round, they likely cooperate again. You secure 1+k while keeping your endowment.

## Selfish Alignment

This strategy directly maximizes single-round payoff given beliefs:

- When cooperation appears widespread (expected_coop ≥ m), defection yields 1+k instead of k—a gain of 1.
- When cooperation appears insufficient (expected_coop < m), defection yields 1 instead of 0 if threshold fails, but defection prevents threshold from being met. Cooperation at least enables the 0+k = k payoff.
- The strategy accepts temporary cooperation only when necessary to unblock mutual gain, then immediately reverts to free-riding once safety is established.
'''

description_SELFISH_4 = '''
**SELFISH THRESHOLD EXPLOITATION STRATEGY**

**Core Principle:** Maximize personal payoff by free-riding on others' cooperation when possible, cooperating only when necessary to trigger the threshold and capture k.

---

**ROUND 1:**
Defect. Use this round to probe the environment and establish a baseline.

---

**ROUNDS 2 TO r-2 (Mid-game):**

Maintain a running count of cooperators observed in the previous round: let this be c_prev.

- **If c_prev ≥ m:** Defect. The threshold is being met by others; free-ride by taking 1+k instead of k.

- **If c_prev = m-1:** Cooperate. You are the pivotal player. Cooperation costs you 0 additional (you contribute 1, lose 1) but guarantees the bonus k for yourself (rather than getting 0). Next round you return to defection.

- **If c_prev < m-1:** Defect. Others are not cooperating sufficiently. Even if you cooperate, you cannot unilaterally ensure the threshold is met. No point bearing the cost.

---

**ROUND r-1 (Penultimate round):**

Let c_prev = observed cooperators in round r-2.

- **If c_prev ≥ m:** Defect. Continue free-riding.

- **If c_prev = m-1:** Cooperate. Lock in the payoff k for this round.

- **If c_prev < m-1:** Defect. The game is nearly over and others have not shown willingness to cooperate.

---

**ROUND r (Final round):**

Always defect. 

Even if you observe c_prev ≥ m in round r-1, defect and capture 1+k instead of k. There are no future rounds to maintain cooperation norms. This is your last extraction opportunity.

---

**Edge Case—Very Small r (r=2):**

Round 1: Defect. Round 2: Defect regardless of what you observed. You cannot afford to cooperate when there's no future to recalibrate.
'''

description_SELFINTERESTED_1 = '''
# Strategy: Threshold-Triggered Reciprocation with Endgame Defection

**Round 1 (Initial):**
Defect. Use this round to observe opponent behavior without commitment.

**Rounds 2 through r-1 (Middle rounds):**
Let c = number of cooperators observed in the immediately previous round.
- If c ≥ m - 1: Cooperate
- If c < m - 1: Defect

**Round r (Final round):**
Defect unconditionally. Future retaliation is impossible, so there is no benefit to cooperating even if the threshold would be met.

---

## Reasoning

**Threshold logic:** In any round where at least m - 1 others cooperate, my cooperation guarantees the threshold is met, yielding payoff k instead of 0. Since k > 1, this exceeds defection's payoff of 1. Therefore, cooperate exactly when this condition holds.

**Bootstrapping:** Round 1 defection is conservative. If opponents use similar strategies, this prevents mutual defection lock-in only if they defect Round 1 and then begin cooperating if others meet the threshold. Alternatively, if opponents are programmed to cooperate early, I benefit by observing their cooperation count in Round 1 and cooperating from Round 2 onward.

**Endgame:** The final round is a pure defection opportunity. No future interaction exists to punish deviation, so the myopic dominant action (defect) applies.

**Robustness:** The strategy is greedy and observation-driven. Against pure cooperators, I cooperate from Round 2 onward and extract value. Against pure defectors, I defect throughout and avoid losses from failed cooperation. Against mixed strategies, I condition only on whether the threshold is already satisfied, making the strategy immune to specific opponent compositions.
'''

description_SELFINTERESTED_2 = '''
# Adaptive Threshold-Matching Strategy

**Decision Rule by Expected Other Cooperators:**

Let j = expected number of other players who will cooperate this round (estimated from history).

- If j ≥ m: **DEFECT** (free-ride; threshold will be met with others' contributions)
- If j = m-1: **COOPERATE** (your cooperation reaches the threshold; payoff is k > 1 vs. 1 from defection)
- If j < m-1: **DEFECT** (threshold cannot be reached even with your cooperation; cooperating yields 0)

**Estimating j (Belief Update):**

Maintain a running estimate of the cooperation rate among opponents:
- Round 1: Set j = ⌊(n-1)/2⌋ (assume roughly half of others will cooperate; neutral prior)
- Round t ≥ 2: Let c_{t-1} = number of other players who cooperated in round t-1. Set j = c_{t-1} for round t.

After observing round t, update by replacing j with the freshly observed count.

**Edge Cases:**

- **Last round (t = r)**: The decision rule remains unchanged. Defect if you expect ≥m-1 others; cooperate only if you expect exactly m-1. (No future rounds to influence, so history-based beliefs are final.)

- **Rare ties or boundary cases**: If expected cooperators exactly equal m-1, cooperate. Round fractional estimates down (e.g., if 2.7 opponents are expected, treat as 2).

**Pseudocode:**

```
initialize j ← floor((n-1)/2)

for round t = 1 to r:
    if j ≥ m:
        action[t] ← DEFECT
    else if j = m-1:
        action[t] ← COOPERATE
    else:
        action[t] ← DEFECT
    
    observe c_t (count of other cooperators in round t)
    j ← c_t (update belief for next round)
```

**Self-Interested Logic:**

This strategy maximizes single-round payoff given your belief about others. You defect whenever others' contributions alone can reach the threshold (securing k without cost). You cooperate only when you are the decisive marginal player — precisely when your contribution tips the outcome from failure to success, making cooperation's net payoff (k vs. 1) favorable. You never "overshoot" cooperation.
'''

description_SELFINTERESTED_3 = '''
# Strategy: Threshold-Responsive Defection with Conditional Entry

**Core Decision Rule:**

Cooperate in round t if and only if:
1. You are not in the final round (t < r)
2. The observed number of cooperators in round t-1 was ≥ m-1

Otherwise defect.

**Round 1 (Initialization):**

Cooperate if and only if m ≤ ⌈n/2⌉. This represents a reasonable belief that roughly half of opponents will attempt cooperation, making the threshold achievable if they coordinate around the same heuristic.

**Subsequent Rounds (2 through r-1):**

Let c_{t-1} = number of observed cooperators in round t-1.

If c_{t-1} ≥ m - 1:
  → Cooperate this round
  
Else:
  → Defect this round

**Final Round (t = r):**

Always defect. No future rounds exist, so future cooperation cannot occur. Defection yields 1 + k (exploit others) versus k (cooperate while others meet threshold).

**Intuition Behind Decision Rules:**

- Cooperating when c_{t-1} ≥ m-1 creates the condition for threshold success: your cooperation plus observed past cooperators guarantee m total, yielding payoff k.
- Defecting in this state yields 1 + k (free-ride on others' contributions). However, observing ≥ m-1 cooperators signals that a threshold-seeking coalition exists. Persistent defection breaks the coalition, causing future rounds to fail the threshold, yielding 1 for all. Conditional cooperation keeps the coalition alive across rounds.
- Without such a signal (c_{t-1} < m-1), cooperation cannot reliably produce the threshold k payoff. Defecting yields 1, which matches expected cooperation payoff.
- In round 1, assume coordination attempts exist if m is not too large relative to group size. If m > n/2, threshold is harder, so defect conservatively.
- The final round is a clear defection point: no repeated-game incentive applies.

**Robustness:**

- Adapts to opponent cooperation rates without requiring communication.
- Self-corrects when opponents defect (shifts to defection, avoiding wasted cooperation).
- Re-enters cooperation if opponents rebuild the coalition (c_{t-1} ≥ m-1 again).
- Exploits opportunistically in the final round, but only after confirmed cooperation patterns.
'''

description_SELFINTERESTED_4 = '''
# Threshold-Following Strategy

**DECISION RULE BY ROUND CONTEXT:**

Round 1: Defect. With no history, assume others are self-interested and will defect. Contributing risks losing 1 point with no guaranteed reciprocal cooperation to meet the threshold.

Rounds 2 through r−1: Condition on observed cooperation from the previous round. Let C = count of cooperators in the prior round.
- If C ≥ m: Defect. The threshold is already satisfied, so you receive reward k without paying 1. Cooperating yields k−1; defecting yields k.
- If C = m−1: Cooperate. Your single contribution reaches the threshold. This converts your payoff from 0 or 1 (depending on threshold failure) to k−1 or k. At the threshold boundary, this is the only scenario where your contribution directly determines collective success.
- If C < m−1: Defect. The gap between current cooperators and threshold is too large. Even with your cooperation, others must coordinate perfectly to meet m. The probability of threshold success with your contribution is low; contributing wastes your endowment.

Round r (final round): Defect. Backwards induction: there is no future. Cooperation yields k−1; defection yields k. The decision at round r has no strategic value for future rounds.

**EDGE CASES:**

- If m = n (all must cooperate): Defect in all rounds. The threshold is unachievable given rational self-interest, so the cost of cooperation is pure loss.
- If m = 2 (minimal threshold): Cooperate in rounds 2–r−1 whenever C = 1, since a single additional cooperator triggers the reward.
- If r = 2 (only two rounds): Apply the strategy above; round 2 is the final round, so defect.

**SELF-INTERESTED LOGIC:**

This strategy maximizes personal payoff by free-riding whenever the threshold is guaranteed (C ≥ m), contributing only when your action materially changes the outcome (C = m−1), and avoiding sunk losses when cooperation is insufficient (C < m−1). The first-round defection reflects ignorance; subsequent rounds are informed by aggregated opponent behavior. The last-round defection reflects the absence of future reputation or reciprocal incentives.
'''

description_OPPORTUNISTIC_1 = '''
# Greedy Threshold Opportunism

**Core principle:** Defect whenever the threshold is likely secure through others' cooperation; cooperate only when defection risks eliminating the threshold bonus.

## Decision Rule by Round

**Round 1:**
Defect. Without history, assume baseline defection—avoid burning endowment on unknown outcomes.

**Rounds 2 to r−1:**
Observe c_{t-1} (cooperators in previous round).

- If c_{t-1} ≥ m: **Defect**  
  Threshold was met. Others likely to cooperate again. Free-ride to earn 1 + k instead of k.

- If c_{t-1} = m − 1: **Cooperate**  
  One defection away from collapse. Cooperating reaches threshold m. Secure the k payoff rather than risk 0.

- If c_{t-1} < m − 1: **Defect**  
  Threshold failed with slack. Even your cooperation won't save it. Preserve endowment, earn 1.

**Round r (final):**
Defect unconditionally. No future round, so no risk of retaliation. Capture 1 + k if others cooperate (high probability if threshold survived this far), or earn 1 if not.

## Edge Cases and Adaptations

**Persistent collapse (c_t < m for consecutive rounds t, t+1, ...):**  
Continue defecting. The project has failed; others are either free-riding or have given up. No benefit to cooperation.

**Sudden spike in cooperation (jump from c_{t-1} < m−1 to defect threshold):**  
Immediately switch to free-riding (defect). Threshold is now stable.

**Two-player case (n = 2, m = 2):**  
Round 1: Defect. Rounds 2–r−1: If opponent cooperated (c_{t-1} = 1), defect. If opponent defected, defect (since m = 2, cooperation by you alone fails anyway). Round r: Defect.

## Opportunistic Logic

This strategy privileges personal gain over collective welfare:
- Takes the 1 + k payoff (defect with met threshold) whenever feasible
- Exploits others' cooperation without reciprocating
- Abandons costly cooperation the moment it's no longer pivotal
- Maximizes final-round extraction
'''

description_OPPORTUNISTIC_2 = '''
# Opportunistic Threshold Strategy

**Core Logic:** Defect by default. Cooperate only when you are the marginal player required to meet the threshold, or when the threshold is already guaranteed to fail.

## Decision Rules

**Round 1:**
Defect. Gather information with zero commitment.

**Rounds 2 through r-1:**
Observe c_{t-1} = number of cooperators in the previous round.

- If c_{t-1} ≥ m: Defect
  - Threshold is met regardless of your action. Take the free-ride payoff of 1 + k.
  
- If c_{t-1} = m - 1: Cooperate
  - You are the marginal player. Cooperating yields k; defecting yields 1. Cooperate to secure the bonus.
  
- If c_{t-1} < m - 1: Defect
  - Threshold cannot be met. Secure your private payoff of 1.

**Round r (final round):**
Apply the same logic as rounds 2 to r-1:

- If c_{r-1} ≥ m: Defect
- If c_{r-1} = m - 1: Cooperate
- If c_{r-1} < m - 1: Defect

## Handling First-Round Uncertainty

In round 1, you have no history. Defecting maximizes your payoff under ambiguity: if others cooperate enough, you gain 1 + k; if they don't, you still gain 1. Cooperating blindly risks payoff 0.

## Opportunistic Alignment

This strategy prioritizes self-interest by:
- **Free-riding when safe:** Defecting whenever the threshold is already met or definitively unmet.
- **Minimizing wasted cooperation:** Only cooperating when your contribution is the deciding factor—when you are one of the m cooperators and would otherwise fall short.
- **No altruism:** Never cooperating "to help" when your cooperation is surplus.
- **Exploiting imbalances:** If observed cooperation settles at exactly m - 1 players, you become a repeating pivot and reliably extract k each round after round 1.
'''

description_OPPORTUNISTIC_3 = '''
# Opportunistic Threshold Strategy

## Core Decision Rules

**Default rule (rounds 1 to r-1):**
- If observed cooperators in previous round ≥ m: **DEFECT** (free-ride on achieved threshold)
- If observed cooperators in previous round = m-1: **DEFECT** (threshold achieved without you)
- If observed cooperators in previous round = m-2: **COOPERATE** (you become the critical marginal cooperator)
- If observed cooperators in previous round < m-2: **DEFECT** (threshold cannot be met regardless)

**Last round (round r):**
- If observed cooperators in previous round ≥ m-1: **DEFECT** (threshold achievable without you; final round eliminates future consequences)
- If observed cooperators in previous round < m-1: **DEFECT** (threshold unachievable; extract private value)

**First round (round 1):**
- **DEFECT** (no history to guide cooperation; assume others will provide some threshold attempts; defection yields max payoff given uncertainty)

## Edge Case Handling

**When cooperation in round t equals m exactly:**
- Threshold was just met with all cooperators contributing
- In round t+1, all previous cooperators appear "redundant"
- Each observing this will defect opportunistically
- Cooperation will collapse unless explicitly restarted

**When cooperation falls below m:**
- Next round: players observing failure will reassess
- Those who cooperated last round may increase cooperation (rescue attempt)
- Opportunist defects if m-2 or fewer already defecting (no way to rebuild)
- Opportunist cooperates only if exactly m-2 others defecting (become essential)

## Opportunistic Logic

The strategy exploits the asymmetry: cooperating costs 1, but the threshold payoff k is shared by all. By defecting when m-1 or more others cooperate, you capture k without paying the cost 1. This yields payoff 1 + k versus 0 + k for cooperators.

The strategy monitors the "marginal defector position"—you only contribute when dropping below m cooperators would fail the project entirely. This minimizes your contribution while maximizing probability of threshold achievement. In the final round, this defection tendency intensifies because future cooperation incentives vanish.
'''

description_OPPORTUNISTIC_4 = '''
# Opportunistic Threshold-Hunting Strategy

## Core Decision Rule

Cooperate if and only if both conditions hold:
1. Observed cooperation in the previous round < m (threshold not yet met)
2. Observed cooperation in the previous round ≥ m - 2 (close enough to push over threshold)

Otherwise, defect.

## Round-by-Round Application

**Round 1:** Defect. Establish baseline information about opponent cooperation rates with zero cost.

**Rounds 2 to r-1:** 
- If last_round_cooperators ≥ m: Defect. The threshold succeeded without your contribution; free-ride on the reward.
- If last_round_cooperators ∈ [m-2, m-1]: Cooperate. The group nearly succeeded; your cooperation is the deciding vote. Cost is 1, but you capture k.
- If last_round_cooperators < m-2: Defect. Threshold is unlikely; cooperation costs you 1 for payoff 0. Better to keep the 1.

**Round r (final round):** Defect unconditionally. No future rounds exist to justify the cooperation cost; capture the private endowment.

## Adaptation Logic

After each round, update your estimate of baseline cooperation by tracking the count of cooperators. If you notice a downward trend in cooperation (e.g., cooperators dropping across three consecutive rounds), remain in defection mode—the group is fragile and unlikely to reach threshold.

If you observe stabilization near or above m-1 cooperators, shift into full opportunistic mode: defect every round and harvest the recurring k payoff.

## Edge Case: Very Few Rounds

If r = 2, cooperate in round 1 only if you have reason to believe m-1 or more others will. Otherwise, apply the default: defect round 1, defect round 2.
'''

description_INDIVIDUALISTIC_1 = '''
EMPIRICAL THRESHOLD COOPERATOR

**Core Decision Rule:**

Cooperate in round t if and only if:
1. t < r (not the final round), AND
2. The empirical cooperation rate from previous rounds meets or exceeds the critical threshold

**Calculate Critical Threshold:**
p_critical = (m - 1) / (n - 1)

This represents the minimum fraction of other players who must cooperate for the threshold to be met with my cooperation included.

**Empirical Cooperation Rate:**
p_empirical = C_past / N_past

where:
- C_past = total number of cooperators observed across all previous rounds
- N_past = total number of opponent-round observations so far = (n - 1) × (t - 1)

**Decision Logic per Round:**
```
if t == r:
  play D  // final round: no future payoff from cooperation
elif C_past / ((n-1) × (t-1)) >= (m-1)/(n-1):
  play C  // empirical rate justifies cooperation
else:
  play D  // empirical rate insufficient
```

**First Round (t = 1):**
Cooperate if and only if m ≤ n/2 + 1

This reflects initial optimism only when the threshold is not too stringent. Otherwise, defect and gather information.

**Rounds 2 to r-1:**
Update empirical average after each round. Adjust cooperation dynamically as evidence accumulates.

**Final Round (t = r):**
Always defect. No future rounds exist; cooperation provides no future benefit while defection gains immediate payoff. The threshold is irrelevant.

**Robustness Properties:**
- Adapts to any opponent mix: uses only observed aggregate data, not assumptions about individual strategies
- Scales with parameters: decision threshold adjusts automatically to m, n
- Avoids exploitation: defects against defection-heavy groups; cooperates only when empirical evidence supports threshold achievement
'''

description_INDIVIDUALISTIC_2 = '''
# CONDITIONAL COOPERATION STRATEGY

## Decision Rule

Cooperate in round t if and only if:
- You observed ≥ m cooperators in round t-1, OR
- t = 1 and you believe enough others will cooperate (defect by default)

Otherwise defect.

More formally:

```
Round 1:
  Play D

Round t ∈ {2, ..., r}:
  Let c(t-1) = number of cooperators observed in round t-1
  If c(t-1) ≥ m:
    Play C
  Else:
    Play D
```

## Rationale

This strategy embeds the individualistic principle: cooperate only when you have direct empirical evidence that cooperation succeeded previously. It exploits the observed stabilization of opponent behavior.

## Edge Cases

**First round:** Defect. You have no history. Cooperation without evidence is individually irrational—you might bear cost c=1 for zero payoff if others defect.

**Rounds 2 through r-1:** Follow the observation rule strictly. If you saw ≥m cooperators last round, it signals a cooperative coalition exists; joining generates payoff k instead of 1+0=1 when you free-ride, but the threshold is more likely met.

**Final round:** Apply the same rule. There is no strategic advantage to deviating on the final round—the payoff structure is identical. Consistency also prevents last-round defection from signaling untrustworthiness to yourself.

**If c(t-1) = m exactly:** Cooperate. The threshold was just met; the cooperation coalition is at minimum viable size. Joining it preserves the equilibrium.

**If c(t-1) > m:** Cooperate. Others overshot the threshold; your cooperation is redundant but payoff-positive (k > 0).

## Individualistic Alignment

- Never sacrifice payoff to help others coordinate (defect in round 1)
- Only cooperate when you observe that cooperation paid off before
- No assumption of reciprocity or future trust—decisions are reactive to outcomes
- Immune to appeals or coordination norms; follows only empirical incentives
'''

description_INDIVIDUALISTIC_3 = '''
# Adaptive Threshold-Sensitive Strategy

## Decision Rule

Maintain a running estimate of the empirical cooperation rate across all observed rounds: p̂ = (total cooperators observed) / (total opponent actions observed).

In each round t > 1, cooperate if and only if:

```
P(exactly m-1 others cooperate | p̂) > 1/k
```

where the probability is computed using the binomial distribution: P(X = m-1) where X ~ Binomial(n-1, p̂).

Otherwise, defect.

## Edge Cases and Round-Specific Behavior

**Round 1:** Defect. No history exists to estimate cooperation rates. Defecting is safe and provides immediate information about opponent behavior.

**Round 2:** Calculate p̂ from round 1 data (single observation of opponent cooperation count). Apply the threshold rule above.

**Rounds 3 through r-1:** Continue updating p̂ with cumulative history. Re-evaluate the threshold inequality each round. The estimate becomes more stable as history accumulates.

**Final round (round r):** Apply the same threshold rule. Do not special-case the final round—the long-term cooperation rate estimate is most reliable here, so standard decision-making applies.

## Rationale for Individualism

This strategy maximizes your expected payoff by exploiting the precise breakeven point where cooperation becomes worthwhile: when the probability of being the marginal cooperator (pushing the group over the threshold m) exceeds the cost-benefit ratio 1/k. You do not cooperate to help others reach the threshold—you cooperate only when your individual expected gain exceeds 1. You treat observed cooperation counts as evidence of group behavior and adjust your participation accordingly, without assuming reciprocity or shared norms. Defection in round 1 is rational exploration, not punishment.
'''

description_INDIVIDUALISTIC_4 = '''
# Individualistic Adaptive Threshold Strategy

## Decision Rule

**Track opponent cooperation rates:**
- After each round, record the number of opponents who cooperated
- Maintain a running empirical cooperation frequency: p = (total opponent cooperations observed) / (total opponent-rounds observed)
- Estimate the expected number of opponent cooperators in the next round: E = (n-1) × p

**Cooperation decision based on expected opponent contribution:**
- If E < m-1: Defect (threshold cannot be reached even with my contribution)
- If m-1 ≤ E ≤ m: Cooperate (I am likely necessary to reach threshold)
- If E > m: Defect (threshold will be met without my contribution; free-ride on others)

## Edge Cases

**Round 1 (no history):**
Defect. With no observations, you cannot estimate opponent behavior. Contributing blindly risks paying cost 1 with no certainty of reaching m.

**Last round (round r):**
Defect. Defection in the final round cannot harm your future reputation since no future rounds remain. The cost of cooperation (1 unit) is not recovered by continuation play.

**When E equals m-1 (critical threshold):**
Cooperate. Your contribution bridges the gap from m-1 to m, securing the reward k for yourself. The payoff gain (k versus k+1 defection) is justified only if you assess high confidence in opponent cooperation. Use cooperation as insurance when marginally needed.

## Individualistic Alignment

This strategy pursues pure self-interest:
- **Exploits free-riding:** When others have already cooperated sufficiently, you extract full reward without paying the cost
- **Avoids sucker payoff:** You do not contribute when the threshold is unattainable, preventing wasted investment
- **Responds to evidence, not morality:** Decisions depend solely on empirical opponent behavior and probability calculations
- **Abandons cooperation under certainty:** No loyalty to mutual benefit; if others will not carry the threshold, you protect your endowment
- **Terminates cooperation at game end:** You harvest final-round defection advantage, ignoring any sequencing concerns
'''

description_COLLECTIVE_5 = '''
# Threshold-Cooperative Strategy with Decline Adaptation

## Decision Rule by Round

**Round 1:**
Cooperate. Initialize with cooperation assumption that others use similar risk-mitigation logic.

**Rounds 2 to r-1 (Middle Rounds):**
Let cooperators_prev = number of cooperators observed in the previous round.

- If `cooperators_prev < m`: Cooperate
- If `cooperators_prev ≥ m`: Defect

**Round r (Final Round):**
Let cooperators_prev = cooperators observed in round r-1.

- If `cooperators_prev < m`: Cooperate (must secure threshold before game ends)
- If `cooperators_prev ≥ m`: Defect (threshold already secured)

## Threshold Failure Recovery

If cooperation drops below m in any round before the last:
- Immediately return to full cooperation in the next round
- This acts as a "correction signal" to other players also tracking threshold
- Assumes coordinated recovery if all players use similar logic

## Intuition

The strategy maintains a baseline: once m players are observed cooperating, the threshold is safe that round and you capture free-riding value (1 + k vs. k). If the observed cooperation dips below m, you revert to cooperation to prevent collective loss.

This creates a stable equilibrium where:
- Players coordinate on achieving m through initial cooperation
- Free-riding is self-limiting because it reduces observed cooperators below m
- Defection triggers automatic correction from others using the same rule
- The final round forces cooperation insurance since there's no chance to recover if threshold fails

## Edge Cases

- If n < 2m - 1: Threshold mathematically unachievable by majority; cooperate only round 1, then defect (minimize individual loss from impossible goal)
- If m = n: Requires universal cooperation; cooperate all rounds (collective stability requires it)
- Ties and monitoring delays: Assume defection happens when cooperation strictly falls below m
'''

description_COLLECTIVE_6 = '''
# Adaptive Threshold-Responsive Strategy

## Decision Rule Framework

**Cooperation decision** depends on estimating whether the collective threshold can be achieved:

1. **First round**: Cooperate
   - Establishes cooperative signal and generates initial data on opponent tendencies

2. **Rounds 2 to r-1**: 
   - Calculate observed opponent cooperation rate from all previous rounds: `p_obs = (total opponent cooperations) / (rounds completed × (n-1))`
   - Estimate expected cooperators next round (excluding self): `expected_cooperators = p_obs × (n-1)`
   - **Cooperate if**: `expected_cooperators + 1 ≥ m`
   - **Defect if**: `expected_cooperators + 1 < m`
   
   Rationale: Cooperate when threshold appears achievable with your participation; defect only when threshold seems unreachable regardless.

3. **Final round (t = r)**:
   - Apply the same decision rule as round 2 to r-1
   - Do not deviate for last-round exploitation, as this preserves the credibility of your strategy and prevents cascade defection in final rounds if played repeatedly

## Edge Cases & Adjustments

- **Early rounds (insufficient history)**: Use initial cooperation data. If fewer than 2 rounds completed, use `p_obs = 1.0` (assume others followed your first-round cooperation).

- **Tie-breaking**: When `expected_cooperators + 1 = m` (threshold exactly met with your participation), cooperate. Threshold success is collectively optimal.

- **Noisy environments**: If opponent cooperation varies round-to-round, use a weighted average favoring recent rounds:
  `p_obs = (0.3 × avg(rounds 1 to t-2) + 0.7 × avg(rounds t-2 to t-1))`

## Collective Alignment

This strategy:
- Pursues threshold achievement as primary objective
- Commits to threshold cooperation even in the final round (no defection-at-the-end exploitation)
- Withdraws only when threshold is objectively unachievable, minimizing wasted contributions
- Responds reciprocally to observed cooperation patterns, creating positive feedback loops when others show willingness
'''

description_COLLECTIVE_7 = '''
**COLLECTIVE THRESHOLD MAINTENANCE STRATEGY**

**State Variable:**
Track the number of cooperators observed in the previous round (C_prev). Initialize C_prev = n for round 1.

**Decision Rule by Round:**

**Round 1:**
Cooperate. Establish goodwill and signal willingness to pursue the collective goal.

**Rounds 2 to r-1 (All middle rounds):**
```
if C_prev >= m:
    Cooperate
else if round_number <= ceil(r / 2):
    Cooperate
else:
    Defect
```

- **If threshold was reached last round:** Cooperate to maintain the critical mass and realize repeated k payoffs.
- **If threshold was not reached, but we're in the first half:** Cooperate to continue building toward the threshold; assume others may be ramping up cooperation.
- **If threshold was not reached and we're in the second half:** Defect. Sustaining the cooperative effort becomes futile; expect others to have similarly concluded that coordination is unlikely.

**Round r (Final round):**
Defect. No future rounds exist to influence or reward cooperation. The marginal payoff from cooperation is zero while defection yields +1.

**After Each Round:**
Update C_prev to the observed count of cooperators this round.

**Rationale:**
This strategy balances three objectives: (1) genuine effort to establish the threshold early by cooperating unconditionally in the first half, (2) stable threshold maintenance once achieved by continuing to cooperate, and (3) graceful exit from futile cooperation in the late game. It avoids the paradox of immediately defecting after threshold success—instead, it locks in the cooperative equilibrium as long as it persists. The strategy remains collective by prioritizing threshold achievement over individual exploitation and by reciprocating group-level cooperation signals transparently.
'''

description_COLLECTIVE_8 = '''
**Reciprocal Threshold Trust Strategy (RTT)**

**Core Logic:**
Cooperate when you estimate the threshold will be met. Defect when evidence suggests it won't be. Adjust terminal behavior based on recent history.

**Decision Rules:**

*Round 1:*
Cooperate. Lead by example and signal willingness to support collective success.

*Rounds 2 to r-2 (mid-game):*
Let observed_C = number of cooperators in the immediately previous round.
Let deficit = m - observed_C.

- If deficit ≤ 0: Cooperate (threshold met; maintain momentum)
- If 0 < deficit ≤ 1: Cooperate (almost there; one contribution helps)
- If 1 < deficit ≤ ⌈n/3⌉ AND round ≤ r/2: Cooperate (feasible early; invest in building cooperation)
- If 1 < deficit ≤ ⌈n/4⌉ AND round > r/2: Cooperate (still achievable; narrow window)
- Otherwise: Defect (threshold appears structurally out of reach)

*Round r-1 (penultimate):*
- If observed_C ≥ m: Cooperate (threshold secured; expect same)
- Otherwise: Defect (threshold unmet; no recovery possible)

*Round r (final):*
Defect unconditionally. No future payoff to influence; collect private endowment.

**Edge Cases:**

*Consecutive defection spirals:* If threshold fails in two consecutive rounds, switch to defect for all remaining rounds except the penultimate (where you re-evaluate observed cooperation once more before final round).

*Guaranteed threshold:* If observed_C > m in any round, treat as strong signal and cooperate in the next unless in terminal phase.

**Collective Alignment:**
The strategy avoids pure defection (which guarantees threshold failure) but protects against unreciprocated contributions. It treats cooperation as conditional reciprocity: "I will help achieve collective success if I have evidence others will too." This balances collective optimization against free-rider vulnerability.
'''

description_COLLECTIVE_9 = '''
**ADAPTIVE THRESHOLD-SEEKING STRATEGY**

**State Tracking:**
Maintain running average of opponents' cooperation rate: `avg_coop = (cumulative cooperators seen) / ((n-1) × rounds elapsed)`

**Core Decision Rule:**

For each round t, compute:
- `expected_others = avg_coop × (n-1)` (expected cooperators among opponents)
- `deficit = m - 1 - expected_others` (cooperators needed from you to reach m)

**Action Selection:**

1. **Round 1 (no history):** Cooperate
   - Rationale: Break information symmetry, establish baseline

2. **Rounds 2 to r-1 (with history):**
   - If `expected_others ≥ m-1`: Cooperate
     - We are pivotal or beneficial; payoff is 0+k = k vs 1
   - If `expected_others < m-1` and `rounds_remaining ≤ 2`: Defect
     - Endgame: cooperation cannot bootstrap to threshold in remaining time
   - If `expected_others < m-1` and `rounds_remaining > 2`: Cooperate with probability `p = max(0, 1 - (2t/r))`
     - Early exploration: cooperate despite weak signal (probability decays linearly with time)
     - Rationale: Allow strategy adjustment among opponents; fade hope as rounds diminish

3. **Round r (final round):**
   - If `expected_others ≥ m-1`: Cooperate
   - Else: Defect (no future rounds; k is irretrievable, keep endowment)

**Adaptive Adjustment:**
If threshold appears unreachable for 2+ consecutive rounds AND `expected_others < m-2`, lock to Defect for all remaining rounds. Recovery probability becomes vanishing.

**Rationale (Collective Framing):**
This strategy cooperates when collective success is feasible (you are part of the solution), withholds when futile (threshold unreachable given opponent behavior), and uses early exploration to signal willingness to coordinate while reserving the final round for individual payoff security.
'''

description_COLLECTIVE_10 = '''
# Adaptive Threshold Coordination Strategy

**State Variables:**
- `threshold_met_count`: number of rounds where ≥m total cooperators observed
- `cooperator_history`: list of observed cooperator counts per round

---

## Decision Rule

**Round 1:**
Cooperate. Establish that cooperation is viable for future coordination.

**Rounds 2 to r-1 (Middle Rounds):**

1. Calculate success_rate = `threshold_met_count / (current_round - 1)`
2. Calculate `avg_opponents_cooperated` = mean of cooperator_history

Cooperate if ANY of these hold:
- `success_rate ≥ 0.5` (threshold met in majority of previous rounds)
- `success_rate = 0` AND `avg_opponents_cooperated ≥ m - 1` (close to threshold, make up deficit)
- `success_rate = 0` AND `avg_opponents_cooperated ≥ m/2` (proportional contribution when some others are trying)

Otherwise, Defect.

**Round r (Final Round):**

Cooperate if ANY of these hold:
- `success_rate ≥ 0.3` (threshold was reached sometimes—seal the collective win)
- `avg_opponents_cooperated ≥ m - 1` (final push to cross threshold)

Otherwise, Defect.

---

## Edge Cases

**Threshold never approached:** If `avg_opponents_cooperated` remains < m/2 across the entire game, defect from round 2 onward. The group is not coordinating.

**Threshold met consistently:** If success_rate exceeds 0.7 in middle rounds, continue cooperating through the final round without reconsidering.

**Last round after failure streak:** If threshold was not met in rounds t-2, t-1, but average opponent cooperation still shows `≥m-1` cooperators, make one final cooperative attempt (others may be attempting the same recovery).

---

## Collective Alignment

This strategy embodies collectivity by:
- **Bootstrapping coordination**: Always cooperate round 1, signaling willingness to contribute
- **Proportional reciprocity**: Match effort level to others' observed cooperation rates, not to private incentives
- **Threshold focus**: Cooperate whenever it plausibly helps reach m, even when defection yields higher private payoff
- **Graceful exit**: Defect only when evidence shows the group is not attempting collective success (very low observed cooperation)
'''

description_COLLECTIVE_11 = '''
**Threshold-Tracking Adaptive Cooperation**

**Decision Rule:**

For each round t ∈ {1, 2, ..., r}:

```
IF t = 1:
    COOPERATE
    
ELSE IF t = r (final round):
    IF (cooperators observed in round r-1) ≥ m:
        COOPERATE
    ELSE:
        DEFECT
        
ELSE (rounds 2 through r-1):
    LET c_prev = number of cooperators observed in round t-1
    
    IF c_prev ≥ m:
        COOPERATE
    ELSE IF c_prev < m AND (r - t) > 1:
        COOPERATE
    ELSE IF c_prev < m AND (r - t) = 1:
        DEFECT
```

**Edge Cases:**

- **First round (t=1):** Always cooperate to signal a cooperative baseline and probe opponent willingness.

- **Final round (t=r):** Cooperate only if the threshold was met in the previous round. Otherwise defect (no future consequences, capture surplus).

- **Penultimate round (t=r-1):** If threshold was not met previously and only one round remains, defect (insufficient rounds to recover cooperation). Otherwise, cooperate to attempt reaching collective success.

- **Low cooperation spirals:** If cooperation falls below m and multiple rounds remain, continue cooperating as long as future rounds exist. Assume others use the same strategy and may recover cooperation in later rounds.

**Collective Alignment:**

This strategy sustains cooperation whenever demonstrated to be viable (prev round ≥ m), treats early periods as investment in collective outcome, and only abandons cooperation when no recovery window exists. It avoids free-riding on fragile equilibria in the final round while providing players sufficient feedback to coordinate toward threshold-meeting play across the full game horizon.
'''

description_COLLECTIVE_12 = '''
# Graduated Reciprocal Cooperation Strategy

## Decision Rule

**Round 1:**
Cooperate unconditionally. Establish a cooperative signal and test the willingness of other players.

**Rounds 2 through r−1 (intermediate rounds):**
Observe the number of cooperators *c_prev* from the immediately preceding round.

- If *c_prev* ≥ *m*: **Cooperate**
  - The threshold was met in the previous round. Reciprocate by contributing to maintain group success.
  
- If *c_prev* = *m*−1: **Cooperate**
  - The previous round narrowly failed to reach the threshold. Act as marginal cooperator to help reach the target this round.
  
- If *c_prev* < *m*−1: **Defect**
  - The previous round fell substantially short. Cooperation would be wasted (fail to reach threshold, lose the endowment). Withdraw.

**Final Round r:**
Defect unconditionally. No future rounds exist to reward cooperation, so the individual incentive to defect dominates.

## Rationale and Edge Cases

**First-round initialization:** Starting with cooperation signals good faith and gathers information about opponent willingness. The cost is one round's endowment.

**Marginal-contributor logic:** When *c_prev* = *m*−1, cooperating can be the pivotal action. This round's cooperation has a reasonable chance of reaching the threshold, making the expected payoff positive. This supports collective threshold-reaching without requiring precise knowledge of opponent behavior.

**Reciprocity threshold:** The *m*−1 cutoff prevents wasting contributions when the group is far from coordinating. If fewer than *m*−1 others cooperate, your individual contribution cannot change the round's outcome.

**Endgame defection:** The final round creates a commitment device—by defecting then, you reduce strategic uncertainty in earlier rounds (opponents know continuation incentives disappear). This is individually rational.

**Handle partial information:** Since you only observe aggregate cooperation counts, this strategy requires no assumption about which opponents cooperated, maintaining robustness across heterogeneous opponent strategies.
'''

description_COLLECTIVE_13 = '''
# Threshold-Following Adaptive Strategy

## Core Decision Rule

In round t, cooperate if and only if:
- **Round 1**: Cooperate unconditionally (signal willingness to participate)
- **Rounds 2 to r-1**: Cooperate if the number of cooperators observed in round t-1 is ≥ m-1
- **Round r (final round)**: Defect unconditionally (no future rounds; immediate payoff maximization)

## Detailed Logic

**Define:**
- Let c_t = number of cooperators observed among the other n-1 players in round t
- The threshold for cooperation is m-1 (since you cooperating + m-1 others = m total)

**Decision rule per round:**
```
if round == 1:
    play C

elif round == r:
    play D

else:  // rounds 2 to r-1
    if c_{t-1} >= m-1:
        play C
    else:
        play D
```

## Edge Cases & Rationale

**First round**: Unconditional cooperation serves as a "probe" — it reveals your type as potentially cooperative and gives you data on others' initial behavior.

**Middle rounds (2 to r-1)**: Follow the observed cooperation threshold strictly. If fewer than m-1 others cooperated last round, the collective goal is unreachable even if you cooperate (total would be < m), so defect. If m-1 or more others cooperated, join the threshold and lock in the payoff k.

**Final round**: Defect because there is no future to build reputation in. The threshold mechanism itself becomes irrelevant—you extract maximum immediate value by keeping your endowment.

## Collective Alignment

This strategy embodies collective rationality by:
- **Reciprocal cooperation**: Matches others' willingness to cooperate without exploiting the threshold
- **Threshold enforcement**: Doesn't free-ride—only contributes when collective success is achievable
- **No optimism bias**: Doesn't bet on others cooperating in the absence of evidence
- **Efficiency with others**: If a sufficient coalition forms, you reliably join it, stabilizing cooperation
'''

description_COLLECTIVE_14 = '''
# Threshold Matching Strategy

## Decision Rule

**Cooperate in round t if and only if:**
- t = 1 (first round), OR  
- In round t-1, at least (m-1) of your (n-1) opponents cooperated

**Otherwise, defect.**

## Explanation

In each round, observe the number C_{t-1} of opponents who cooperated in the previous round.

```
if t = 1:
    action = C
else if C_{t-1} ≥ m - 1:
    action = C
else:
    action = D
```

## Edge Cases

**First Round (t=1):** Unconditionally cooperate. This signals willingness to contribute and tests whether a stable coalition toward the threshold is possible.

**Last Round (t=r):** Apply the same decision rule. Do not deviate to defection based on finality. Consistency across rounds maintains the credibility of the signal and avoids triggering cascading defection by opponents who use similar logic.

**Threshold Not Reachable:** If fewer than (m-1) opponents cooperate in any round, the threshold cannot be reached even if you cooperate (since you + at most m-2 others = fewer than m total). Rationally defect to preserve endowment.

## Robustness Properties

- **Against defectors:** Defection cascades naturally once cooperation falls below the threshold—you do not waste endowment on unreachable targets.
- **Against cooperators:** If ≥(m-1) opponents cooperate, you join them, forming a self-sustaining coalition that collectively reaches the threshold every round thereafter.
- **Against mixed strategies:** You adapt round-by-round. The aggregate signal (count of cooperators) is observable and sufficient to decide whether continued contribution is viable.
- **Against strategic defection in final rounds:** By holding the rule constant, you eliminate a common failure mode (everyone defecting on round r-1 because they think others will defect on round r).
'''

description_COLLECTIVE_15 = '''
# Adaptive Threshold Cooperation with End-Game Adjustment

**Round 1 (Opening Signal):**
Cooperate unconditionally. This signals to the group that collective action is possible and establishes baseline willingness.

**Rounds 2 through r-1 (Adaptive Midgame):**

For each round t:
1. Observe the count of cooperators among the n-1 opponents in round t-1. Call this O_t-1.
2. Determine the "cooperation deficit": D = (m - 1) - O_t-1
   - If D ≤ 0: threshold was met among opponents. Cooperate (reinforce success).
   - If D = 1: you are the marginal cooperator needed. Cooperate (you are critical).
   - If D > 1: estimate whether future rounds can compensate.
     
3. For cases where D > 1, compute a "rolling cooperation rate": the average cooperation count observed over the last 2-3 rounds (or all prior rounds if fewer exist).
   - If rolling_avg ≥ (m-1) × 0.7: opponents are demonstrating sustained effort toward threshold. Cooperate.
   - If rolling_avg < (m-1) × 0.7: group cooperation is weak. Check rounds_remaining = r - t.
     - If rounds_remaining ≥ 2: Defect (preserve endowment; weak group may not reach threshold).
     - If rounds_remaining = 1: move to last-round rule.

**Last Round (Round r):**

Observe O_r-1 (final observation of opponent cooperation).
- If O_r-1 ≥ m-1: Cooperate (threshold is within reach with you).
- If O_r-1 < m-1: Defect (threshold unachievable; no future rounds to recover).

**Edge Cases:**

- **All opponents defected every prior round**: Defect (collective signal is dormant).
- **Cooperation exactly at threshold**: Cooperate to consolidate and encourage stability.
- **Volatile cooperation (swings between high and low)**: Use max(rolling_avg, minimum_observed) as the stability estimate; lean toward cooperation if the minimum is still acceptable.

**Collective Alignment:**

This strategy prioritizes achieving the threshold m when feasible by cooperating whenever you are marginal or when the group shows sustained commitment (rolling average). It abandons cooperation only when the group's demonstrated cooperation rate falls too low relative to the target, or when time is exhausted. The strategy avoids freeriding when collective success is proximal, balancing individual prudence with group welfare.
'''

description_COLLECTIVE_16 = '''
# Adaptive Threshold Cooperation Strategy

## Core Decision Logic

**Cooperate** if the estimated number of cooperators (including yourself) in the current round will likely meet or exceed the threshold m. **Defect** otherwise, except in special circumstances.

## Detailed Rules

**Round 1:**
Cooperate unconditionally. This serves as an initial signal of willingness to participate in coordination.

**Rounds 2 to r-1 (intermediate rounds):**

1. Observe h_{t-1} = number of cooperators in the previous round
2. Calculate empirical cooperation rate: p_hat = (sum of all observed cooperators) / (n-1) × (number of rounds elapsed)
3. Project expected cooperators from others: E_others = p_hat × (n-1)
4. **Primary decision:** Cooperate if E_others + 1 ≥ m
5. **Secondary condition:** If E_others + 1 < m but less than 2 rounds remain, still cooperate if:
   - The threshold has been successfully met in at least one prior round (evidence cooperation is viable)
   - The cooperation rate is trending upward (h_t > h_{t-1})
6. **Otherwise:** Defect

**Round r (final round):**
Cooperate if the empirical cooperation rate p_hat ≥ (m-1)/(n-1). 

Rationale: In the final round, cooperate only if observed behavior suggests the group has organically converged toward meeting the threshold—this respects both collective viability and prevents pure sucker payoffs when coordination has failed.

## Edge Cases

- **First round with m = n:** Cooperate anyway; you cannot unilaterally meet the threshold, so signal commitment.
- **No progress by round r-2:** If threshold has never been met and p_hat suggests it's unachievable (p_hat < (m-1)/(n-1)), defect in all remaining rounds.
- **Noise in cooperation:** Use a 2-round moving average of h_t rather than single-round observations to smooth detection of transient noise.

## Collective Alignment

This strategy prioritizes **threshold achievement over individual payoff maximization**. It:
- Leads with cooperation to establish group feasibility
- Sustains cooperation only when evidence suggests collective success is possible
- Abandons cooperation gracefully when the group demonstrates it cannot coordinate
- Weights observed patterns over theoretical best responses, creating robustness to diverse opponent types
'''

description_COLLECTIVE_17 = '''
# Threshold-Sensitive Conditional Cooperator

**Observation**: In each round t, observe X_t = number of opponents cooperating (out of n-1).

**Decision Rule**:

Cooperate in round t if and only if:
- X_t + 1 ≥ m  (your cooperation, combined with observed opponents, reaches or exceeds threshold)

Otherwise, defect.

**Edge Cases**:

*First round*: You have no history. Observe that X_1 is unavailable before your choice. Cooperate unconditionally. This signals willingness to participate and avoids coordinating on mutual defection.

*Last round (t = r)*: Apply the same threshold rule. Do not defect strategically on the last round—it creates a cascade incentive for others to defect in round r-1, collapsing cooperation. The collective good requires maintaining the threshold until the end.

*Exact threshold case (X_t = m-1)*: Cooperate. Your single contribution determines success. Defection guarantees failure for the group.

*Impossible threshold (X_t < m-1)*: Defect. The threshold cannot be met regardless of your action. Cooperating here is pure waste.

*Surplus cooperation (X_t ≥ m)*: Defect. Threshold is already met. Your additional contribution provides no marginal benefit to collective success and costs you the endowment.

**Rationale**: This strategy cooperates precisely when your cooperation is necessary and sufficient to reach the threshold. It avoids both the sucker's payoff (cooperating when threshold fails anyway) and over-contribution (cooperating when threshold is already secured). It's adaptive because it conditions on observed aggregate behavior and robust because it doesn't require beliefs about opponents' strategies—only their realized actions.
'''

description_COLLECTIVE_18 = '''
# RECIPROCAL THRESHOLD MAINTENANCE STRATEGY

**State tracking:** After each round, record the observed cooperator count from the previous round.

**Decision rule:**

**Round 1:** Cooperate unconditionally. Signal commitment to establish a cooperation baseline.

**Rounds 2 to r−1 (intermediate rounds):**
- Let c_prev = observed number of cooperators in the previous round
- Let deficit = m − c_prev

If deficit ≤ 0 (threshold met):
  - Cooperate with probability 1.0
  - Threshold achieved; maintain momentum toward collective payoff

Else if deficit = 1 (one cooperator short):
  - Cooperate with probability 1.0
  - Act as a safety margin; your cooperation alone may secure the threshold

Else if deficit ≥ 2 (significant shortfall):
  - Cooperate with probability (n − deficit) / (n − 1)
  - Scale your cooperation proportionally to the deficit
  - If many others defected, reduce your unilateral contribution to avoid being exploited
  - If few defected, cooperate to help reach threshold

**Round r (final round):**
- Let c_prev = cooperators in round r−1

If c_prev ≥ m − 1:
  - Cooperate with probability 0.95
  - The group is nearly at threshold; secure the final bonus for all
  - Small defection probability to hedge against consistent defectors

Else (persistent shortfall):
  - Cooperate with probability 0.5
  - Signal that you've been trying, but heavy defection elsewhere signals futility
  - Do not subsidize free-riders indefinitely

**Edge case handling:**

- If n = m (everyone must cooperate): Always cooperate—your defection guarantees collective failure
- If deficit > n − 1 (mathematically impossible to reach threshold with remaining defectors as fixed): Defect in that round, reset expectations downward

This strategy balances collective welfare—maintaining threshold through reciprocal assurance—with protection against one-sided exploitation when cooperation consistently fails to materialize.
'''

description_COLLECTIVE_19 = '''
# Adaptive Threshold Cooperation

## Decision Rule by Round Type

**Round 1:**
Cooperate unconditionally. This initiates contribution and signals willingness to help reach the threshold.

**Rounds 2 through r−1:**
Observe c, the number of cooperators in the previous round. Then:
- If c ≤ m−2: Cooperate. The threshold remains unmet; contribution maintains progress toward collective success.
- If c = m−1: Cooperate. Your contribution completes the threshold, securing the multiplier k for all.
- If c ≥ m: Defect. The threshold is already satisfied. Further cooperation wastes your endowment (net payoff k−1 vs. k for defection) without additional collective benefit.

**Round r (final round):**
Observe c from round r−1:
- If c ≤ m−2: Defect. The threshold cannot be reached even with your cooperation, so the cost of contributing goes unrewarded. Preserve the endowment.
- If c = m−1: Cooperate. Your contribution guarantees the multiplier is triggered for this final round.
- If c ≥ m: Defect. The threshold is already secure; taking the higher individual payoff (k vs. k−1) does not harm collective welfare since the multiplier is guaranteed.

## Rationale

This strategy prioritizes reaching and maintaining the m-threshold without overshooting. It avoids wasteful cooperation once the collective goal is met, focuses endowments on rounds where they are pivotal, and recognizes that in the final round, no reputational incentive exists—only the material outcome matters. The approach adapts to observed opponent behavior and is robust to varying cooperation rates because it depends only on whether the threshold has been crossed.
'''

description_COLLECTIVE_20 = '''
# Adaptive Reciprocal Threshold Strategy

**INITIALIZATION**
```
cooperation_count_history = []
threshold_achieved_flag = false
```

**DECISION RULE**

For each round t ∈ {1, ..., r}:

**Round 1:**
Always cooperate (C). This establishes willingness and provides baseline information.

**Rounds 2 through r-1 (mid-game):**

1. Observe the number of cooperators in round t-1, denoted coop_{t-1}
2. Add coop_{t-1} to cooperation_count_history
3. If coop_{t-1} ≥ m:
   - Set threshold_achieved_flag = true
   - Cooperate (C)
4. Else if coop_{t-1} < m:
   - Estimate: if I cooperate, will we hit the threshold?
   - Expected cooperators if I join = coop_{t-1} + 1
   - Calculate deficit = m - (coop_{t-1} + 1)
   - If deficit ≤ 0:
     - Cooperate (C) — my contribution reaches the threshold
   - Else if deficit > 0:
     - Calculate rounds_remaining = r - t
     - Calculate avg_coop_rate = mean(cooperation_count_history) / (n - 1)
     - If avg_coop_rate ≥ (deficit) / (n - 1 - 1) AND rounds_remaining > 1:
       - Cooperate (C) — historical trends suggest threshold reachable
     - Else:
       - Defect (D) — threshold unlikely given history

**Last Round (t = r):**

1. If threshold_achieved_flag = true:
   - Defect (D) — threshold already guaranteed, free-ride on final round
2. Else:
   - If coop_{r-1} = m - 1:
     - Cooperate (C) — my contribution alone hits the threshold
   - Else if coop_{r-1} ≥ m - 1:
     - Cooperate (C) — reinforce threshold maintenance
   - Else:
     - Defect (D) — threshold is unattainable

**COLLECTIVE ALIGNMENT**

This strategy prioritizes collective success (reaching threshold m) over individual exploitation until the final round. It cooperates when:
- Early-game signaling is beneficial (round 1)
- Cooperation is pivotal to reaching the threshold
- The threshold has been achieved (maintaining the group outcome)

It exploits only when the threshold is already secured (last round) or demonstrably unachievable, minimizing the frequency of free-riding and maximizing the probability that others will reciprocate cooperation in subsequent rounds.
'''

description_COLLECTIVE_21 = '''
# THRESHOLD-RESPONSIVE ESCALATION STRATEGY

## Decision Rule by Round Type

**Round 1 (First Round):**
Cooperate. This initiates the collective effort and signals willingness to coordinate.

**Rounds 2 to r-1 (Middle Rounds):**
Let c_prev = number of cooperators observed in the immediately preceding round.

- If c_prev ≥ m: **Cooperate**
  - Threshold was reached last round; continue supporting the collective outcome.

- If m - 1 ≤ c_prev < m: **Cooperate**
  - Threshold is one cooperator away. Your cooperation completes the collective goal.

- If c_prev < m - 1 and (r - current_round) > 2: **Defect**
  - Threshold seems unattainable with too many rounds remaining. Break from a failing coordination pattern to avoid wasting endowment.

- If c_prev < m - 1 and (r - current_round) ≤ 2: **Cooperate**
  - Few rounds remain. Make one more attempt to catalyze threshold achievement despite recent failure.

**Final Round (Round r):**
Let c_prev = cooperators in round r-1.

- If c_prev ≥ m - 1: **Cooperate**
  - The threshold is achievable in this last opportunity.

- If c_prev < m - 1: **Defect**
  - Threshold is unreachable; preserve the marginal endowment.

## Edge Case Handling

- If n = 2 and m = 2: Always Cooperate after round 1, since one opponent's defection makes threshold impossible and you follow the final-round rule.
- If k is very large relative to the cost: Weighted toward more cooperation in middle rounds even when threshold seems unlikely.
- If r = 2: Only cooperate in round 1 if m ≤ n - 1 is plausible; round 2 becomes the final round immediately.

## Collective Alignment

This strategy prioritizes reaching the collective threshold whenever it appears feasible within the remaining time budget. It withdraws investment only when the historical pattern indicates coordination failure is stable, avoiding sunk losses. By cooperating when one additional cooperator closes the gap, it implicitly shares the coordination burden fairly—each player carries the same incentive to "be the marginal cooperator" needed.
'''

description_COLLECTIVE_22 = '''
# Adaptive Threshold-Seeking Strategy

**Decision Rule by Phase:**

**Round 1 (Initial Cooperation):**
- Cooperate
- Rationale: Establish credibility and signal willingness to contribute

**Rounds 2 to r-1 (Adaptive Threshold Tracking):**
- Let c_prev = number of opponents who cooperated in the previous round
- Cooperate if: c_prev ≥ m - 1
- Defect if: c_prev < m - 1

**Round r (Final Round):**
- Let c_{r-1} = number of opponents who cooperated in round r-1
- Cooperate if: c_{r-1} ≥ m - 1
- Defect otherwise

---

**Logic:**

Observe the aggregate cooperation rate. If at least m-1 opponents cooperated last round, the threshold is achievable with your contribution. Continue cooperating to realize the +k payoff. If fewer than m-1 others cooperate, the threshold cannot be met even with your contribution—defect to preserve your endowment.

**Edge Cases:**

- **Threshold unreachable:** If you observe fewer than m-1 cooperators by round 2, switch to permanent defection. The threshold cannot be met regardless of your action.
- **Late coordination:** If cooperation emerges mid-game (e.g., round 3), return to cooperation immediately upon observing c_prev ≥ m-1.
- **Final round:** Cooperation in round r carries no future signaling value. Cooperate only if the evidence (previous round's cooperation count) indicates others will cooperate enough to cross m.

**Collective Alignment:**

This strategy collectively succeeds if enough players follow it: initial mutual cooperation in round 1 triggers sustained cooperation thereafter, securing the +k reward every round. It avoids wasted contributions by ceasing cooperation when the threshold provably cannot be met, protecting against systematic free-riding. The strategy is self-policing—defectors force switches to defection, but genuine coordinators sustain the equilibrium.
'''

description_COLLECTIVE_23 = '''
# Adaptive Threshold-Tracking Strategy

## Decision Rule Framework

**Round 1:** Cooperate. Initiate collective welfare by demonstrating good faith.

**Rounds 2 to r-1 (Middle rounds):**

Observe the number of cooperators from the immediately preceding round. Call this value `c_prev`.

- **If c_prev ≥ m:** Cooperate. The threshold was met last round; continue supporting the collective outcome.

- **If c_prev = m - 1:** Cooperate. Only one defector away from threshold; your cooperation directly enables collective success.

- **If m/2 ≤ c_prev < m - 1:** Cooperate. Sufficient baseline cooperation exists to justify belief that the threshold is retrievable with your contribution.

- **If c_prev < m/2:** Defect. Defection is too widespread to make threshold achievable; investing your endowment becomes futile.

**Round r (Final round):**

- **If c_prev ≥ m:** Cooperate. Reinforce the outcome that provided mutual gain.

- **If c_prev < m:** Defect. The threshold was not sustained; on the final round, no future opportunity to recover collective coordination exists, so maximize your private payoff.

## Edge Case Handling

**Threshold not achievable given remaining rounds:** If at any point you observe c_prev = 0 or defection is universal, immediately switch to defection for all remaining rounds, including the final round. The collective outcome is no longer reachable.

**Ties at boundary:** When c_prev exactly equals the decision boundary (e.g., c_prev = m - 1), apply the higher threshold rule (cooperate), as marginal contributions are maximally valuable when close to the target.

**Round r - 1 specificity:** In the penultimate round, apply middle-round rules normally. Do not preemptively defect; decisions about the final round depend on observing c_prev in round r - 1.

## Collective Logic

This strategy embeds a commitment to collective success: you cooperate whenever evidence from aggregate behavior suggests that others are meaningfully contributing. You defect only when either (a) the collective outcome has already been achieved and no new commitment is required, or (b) defection among opponents is too dense to allow threshold attainment, making individual contribution economically futile. The strategy is **adaptive** because it conditions entirely on observed aggregate cooperation and continuously updates expectations. It is **robust** because it handles fragmented cooperation, full defection, and threshold-met scenarios distinctly, and it respects the finality of round r by pessimistically defecting when the trajectory is clear.
'''

description_COLLECTIVE_24 = '''
**Adaptive Threshold Cooperation**

Define your strategy as follows:

**Round 1:** Cooperate unconditionally. This establishes good faith and provides initial data about opponent cooperation levels.

**Rounds 2 to r-1:**
- Compute the average cooperation rate from all previous rounds: `avg_coop = (total cooperators observed so far) / ((round - 1) × (n - 1))`
- Calculate the cooperation threshold needed from others: `threshold_needed = m - 1`
- Decision rule:
  - If `avg_coop ≥ threshold_needed / (n - 1)`: Cooperate
  - If `avg_coop < threshold_needed / (n - 1)` AND `avg_coop ≥ 0.5 × (threshold_needed / (n - 1))`: Cooperate with probability `avg_coop / (threshold_needed / (n - 1))`
  - Otherwise: Defect

**Round r (final round):**
- Compute `avg_coop` from all previous rounds
- If `avg_coop ≥ 0.75 × (threshold_needed / (n - 1))`: Cooperate (reinforce the successful pattern)
- Otherwise: Defect (avoid unilateral loss)

**Rationale for edge cases:**

*First round:* Cooperating first reveals no weakness since no one has history. It's a cheap signal that you're willing to participate.

*Middle rounds:* Use empirical cooperation rates to calibrate belief about reaching threshold. Probabilistic cooperation at intermediate cooperation rates handles uncertainty gracefully without harsh punishment (which you can't target anyway without knowing individual actions).

*Final round:* Defection is individually optimal if threshold is uncertain, but reinforce cooperation if the trajectory strongly suggests success, securing the project and the higher payoff for the remaining cooperators.

This strategy is collectively-oriented because it sustains cooperation when evidence supports threshold viability, while remaining robust to free-riding by defecting only when cooperation becomes implausible.
'''

description_COLLECTIVE_25 = '''
# Adaptive Threshold Assurance with Momentum Tracking

**Core Decision Rule:**

In round t, cooperate if and only if:
- (t = 1 AND m ≤ ⌈n/2⌉) OR
- (t < r AND observed_cooperators_{t-1} ≥ m) OR  
- (t < r AND observed_cooperators_{t-1} > observed_cooperators_{t-2} AND observed_cooperators_{t-1} ≥ m - 1)

Otherwise defect.

**Round-by-Round Logic:**

*Round 1:* Cooperate if the threshold m is achievable by roughly half the group or less (m ≤ ⌈n/2⌉). This is an optimistic opening that signals conditional willingness. If m is very high relative to group size, defect.

*Rounds 2 to r-1:* 

1. Check previous round's observed cooperation count. If it was ≥ m, cooperate — the threshold is achievable by others, so cooperate to sustain it.

2. If previous cooperation was below m but rising (more cooperators than round t-2), and close to threshold (within 1 of m), cooperate to push toward success.

3. Otherwise defect. Low cooperation suggests the group is not coordinating; defecting protects you from one-sided losses.

*Round r (Final Round):* Defect unconditionally. The game ends; there is no future benefit to maintaining cooperation norms.

**Edge Case Handling:**

- If r = 2: Treat round 1 as round 1, treat round 2 as final round (defect).
- If m = n: Require full consensus in prior round; otherwise defect throughout (threshold too high for robustness).
- Ties in momentum: If observed cooperation is flat round-to-round, defect unless already at or above threshold.

**Rationale:**

This strategy is collectively-oriented: it seeks to reach and sustain the m-player threshold when empirically feasible, while protecting against futile or one-sided cooperation. It avoids assuming shared norms (no predetermined coordination), instead using observable aggregate signals. Momentum tracking allows recovery from small setbacks early, but abandons costly cooperation in the final round when mutual benefit cannot compound.
'''

description_COLLECTIVE_26 = '''
# Threshold-Pivotal Adaptive Strategy

**Round 1:**
Cooperate unconditionally. This signals willingness to coordinate and generates initial information about the field.

**Rounds 2 through r-1 (intermediate rounds):**

Let c_prev = number of cooperators observed in the immediately preceding round.

- If c_prev ≥ m: Cooperate
  - Threshold is already being met. Maintain cooperation to sustain the equilibrium.

- If c_prev = m-1: Cooperate
  - Cooperation is critically close to threshold. Your contribution is potentially pivotal. Defecting risks cascading collapse.

- If c_prev ≤ m-2: Defect
  - Insufficient cooperation exists to meet threshold even with marginal contributors. Defecting minimizes losses (you keep your endowment and the reward fails anyway). Signal that cooperation requires higher group commitment.

**Round r (final round):**

Let c_prev = number of cooperators observed in round r-1.

- If c_prev ≥ m: Defect
  - The threshold is guaranteed to be met without your contribution. Free-ride and capture the reward without cost (payoff: 1 + k vs k if you cooperated).

- If c_prev = m-1: Cooperate
  - You are the marginal cooperator. Your choice determines the outcome: cooperate yields k to everyone; defect yields 1 to you and 0 to others. Accept the cost for collective benefit.

- If c_prev ≤ m-2: Defect
  - The threshold cannot be met. Defecting preserves your endowment (payoff: 1 vs 0 if you cooperated).

**Edge case handling:**
- If you never observe c_prev ≥ m-1 by round r-1, sustain the Round 2 defection pattern through the final round.
- If observations are unavailable (round 1), default to cooperate.
'''

description_COLLECTIVE_27 = '''
# CONDITIONAL COOPERATION WITH THRESHOLD TARGETING

## DECISION RULE

**Let c_avg = average number of cooperators observed in previous rounds (initialized to 0 if round 1).**

**Let p_emp = c_avg / n** (empirical cooperation rate)

**Let E_others = p_emp × (n-1)** (expected cooperators among opponents)

**Cooperate in round t if and only if:**
```
E_others ≥ m - 1
```

Equivalently: Cooperate if your cooperation, combined with the expected behavior of others, reaches or exceeds the threshold m.

## EDGE CASES

**Round 1:**
- Initialize p_emp = (m-1) / (n-1) as a neutral prior reflecting threshold-meeting cooperation
- Cooperate if this prior suggests E_others ≥ m - 1
- This is typically true when m ≤ n/2, encouraging initial cooperation

**Rounds 2 through r-1:**
- Update p_emp after each round using the actual count of cooperators observed
- Recompute E_others and apply the threshold rule consistently

**Final Round r:**
- Apply the same rule: cooperate if E_others ≥ m - 1
- Do not defect strategically in the last round; maintain consistency with collective threshold logic
- If the threshold appears unachievable (E_others < m - 1), defect to preserve the endowment, as continued cooperation cannot secure the reward

## COLLECTIVE ALIGNMENT

This strategy embodies a **threshold-conditional commitment**: you contribute to the collective project if and only if empirical evidence suggests others will meet the shared burden. You avoid sucker's payoffs (contributing while the threshold fails) and avoid free-riding when the threshold is already met by others.

The rolling average of observed cooperation provides a collective signal—a noisy but unmanipulated aggregate feedback—that grounds your decisions in actual group behavior rather than optimistic or pessimistic assumptions. By tying cooperation to reaching m, you align individual incentives with the group's risk-aversion goal.
'''

description_COLLECTIVE_28 = '''
# Adaptive Threshold-Tracking Strategy

## Decision Rule

**Core Logic**: Cooperate when empirical evidence suggests the collective threshold is likely to be met.

Maintain a running estimate of opponent cooperation rate based on all observed history:

```
observed_rate = (total cooperators seen across all previous rounds) / 
                (number_of_opponents × rounds_played_so_far)
```

For round t, given observed_rate, estimate the expected number of cooperators among the n-1 opponents:

```
expected_cooperators = (n - 1) × observed_rate
```

**Decision**:
- **Cooperate** if: `expected_cooperators ≥ m - 1`
  - This means your cooperation would bring the total to at least m, triggering the reward
- **Defect** if: `expected_cooperators < m - 1`
  - Threshold cannot be reached even with your cooperation; preserve endowment

## Edge Cases

**Round 1** (no history):
- Use a conservative cooperative prior: `prior_estimate = m / n`
- This reflects minimal assumption—enough players should cooperate to meet threshold
- Cooperate if `(n - 1) × (m/n) ≥ m - 1`, which simplifies to always cooperating in round 1
- This bootstraps collective cooperation

**Rapid Defection** (observed_rate drops sharply):
- If `observed_rate < m / n` becomes evident within 2-3 rounds, defection is justified—the group is signaling non-cooperation
- Continue defecting until observed_rate recovers

**Final Rounds** (t = r, r-1):
- Apply the same decision rule; payoff structure is identical across rounds
- No "endgame defection" incentive exists here unlike prisoner's dilemma
- Maintain consistency to reinforce that your cooperation is threshold-conditional, not unconditional

## Collective Alignment

This strategy embodies reciprocal threshold cooperation:

- **Signals intent**: Cooperating in round 1 shows you're willing if others reciprocate
- **Responds to aggregates**: You don't track individuals (impossible anyway), only population-level cooperation, creating anonymous accountability
- **Avoids tragedy**: By defecting only when math shows threshold is unattainable, you prevent wasted contributions that benefit free-riders
- **Feedback stability**: If enough others adopt this logic, cooperation rates stabilize above the critical point—once above m, each marginal cooperator validates the strategy for others
- **Mutual benefit**: The strategy converges toward all-cooperate equilibrium when opponents are similarly adaptive
'''

description_COLLECTIVE_29 = '''
**ADAPTIVE THRESHOLD-RESPONSIVE COOPERATION**

**Round 1 (Initialization):**
Cooperate unconditionally. Establish baseline collective effort.

**Rounds 2 through r-1 (Middle Rounds):**
Let c_prev = observed number of cooperators in the previous round.

- If c_prev ≥ m - 1: Cooperate
  - Rationale: Previous round showed sufficient cooperation momentum. Your cooperation pushes past the threshold, securing the reward for all.

- If c_prev < m - 1: Defect
  - Rationale: Insufficient cooperators last round. Even with your cooperation, the threshold is unlikely to be met. Preserve payoff.

**Round r (Final Round):**
Let c_{r-1} = observed number of cooperators in round r-1.

- If the threshold was met in any of rounds 1 through r-1: Cooperate
  - Rationale: History shows the collective can succeed; sustain the pattern for final payoff.

- Else if c_{r-1} ≥ m - 1: Cooperate
  - Rationale: Last round demonstrates the threshold is achievable; secure the final mutual gain.

- Else: Defect
  - Rationale: Pattern shows insufficient cooperation exists. Last-round cooperation yields no multiplicative benefit and wastes your endowment.

**Edge Cases:**

- **m = n:** Require universal cooperation. Only cooperate if all n-1 others cooperated (c_prev = n-1).

- **m = 2, n > 2:** Low threshold. Cooperate in round 1; cooperate in subsequent rounds if at least 1 opponent cooperated previously.

- **Single pass (r = 2):** Round 1 cooperate; Round 2 defect unless threshold was definitively met in Round 1.

This strategy balances collective success (tracking observed cooperation momentum) with individual rationality (not cooperating when the threshold is implausible), while respecting the final-round shift where future coordination is impossible.
'''

description_COLLECTIVE_30 = '''
# Adaptive Collective Threshold Strategy

## Core Decision Rule

**Track one statistic:** the moving average of cooperators in previous rounds.

Let `avg_coop` = average number of cooperators across all completed rounds (counting each round's observed aggregate).

**Each round, cooperate if and only if:**

```
IF round == 1:
    Cooperate (establish commitment baseline)
    
ELSE IF observed_cooperators_last_round >= m:
    Cooperate (threshold was just met; maintain)
    
ELSE IF observed_cooperators_last_round + 1 >= m:
    Cooperate (your participation closes the gap to threshold)
    
ELSE IF avg_coop >= m - 1:
    Cooperate (historical average suggests others will cooperate; 
               reaching threshold together is likely)
    
ELSE:
    Defect (empirical cooperation is too low; threshold unreachable)
```

## Edge Cases

**Last round (t = r):**
- Apply the same rule. In the final round, defect only if the threshold cannot be met even with your cooperation, since there is no future to influence. Otherwise, cooperate to help close a reachable threshold.

**Collapse scenario** (avg_coop drops below m - 1):
- Once you switch to defect mode, remain in defect unless observed cooperation rebounds above m - 1 in a single round. This prevents wasteful oscillation in a defecting equilibrium.

**Early game (rounds 2-3):**
- The rule naturally weights recent observations heavily while avg_coop is still noisy. No special override is needed.

## Collective Alignment

This strategy embodies collective thinking:

1. **Cooperation-first posture:** You begin by cooperating, signaling willingness to provide the public good.

2. **Evidence-responsive:** You track whether others reciprocate. If cooperation clusters near the threshold, you stay engaged. If it collapses, you exit gracefully rather than unilaterally bearing the cost.

3. **Threshold-focused:** Decisions hinge on whether *m players together* can succeed, not on personal gain. You cooperate whenever you are pivotal (i.e., your cooperation would close the gap) or whenever others' history suggests mutual success is feasible.

4. **No punishment needed:** Rather than punishing free-riders, you simply condition your contribution on the likelihood that a threshold-crossing coalition exists. This avoids wasteful defection spirals while remaining robust to exploitation.
'''

description_COLLECTIVE_31 = '''
**Adaptive Threshold Cooperation Strategy**

**State Variable:**
Maintain a running average of opponent cooperation rates: `avg_opponent_coop = mean number of cooperators observed per round in all previous rounds`

**Round 1 (First Round):**
Cooperate unconditionally. This serves as a signal of willingness and gathers initial information about opponent behavior.

**Rounds 2 through r (Including Last Round):**
Use the following decision rule:

1. Calculate the expected number of opponents who will cooperate, based on the historical average: `expected_others = avg_opponent_coop`
2. Compute what total cooperation would be if you cooperate: `total_if_I_cooperate = expected_others + 1`
3. Apply the threshold rule:
   - **If** `total_if_I_cooperate ≥ m`: **Cooperate**
   - **Else if** `expected_others > m - 2`: **Cooperate** (optimistic adjustment—cooperate if others are close to the threshold, betting they will coordinate)
   - **Else**: **Defect** (abandon if coordination seems infeasible)

**Edge Case—Degenerate History:**
If no rounds have occurred yet (t=1), use the optimistic assumption that others will cooperate at rate `(m-1)/(n-1)` or higher, and cooperate accordingly. If this assumption has been violated by round 2, switch to the empirical average immediately.

**Endgame Consideration:**
The last round receives no special treatment—use the same rule. Past cooperation patterns are your only signal of future behavior, and there is no value to reputation-building beyond maximizing final payoff.
'''

description_COLLECTIVE_32 = '''
# Cooperative Threshold Tracking Strategy

**Initialize:** Set cooperation_count = 0 (tracks total observed cooperators from opponents in previous rounds, summed across all rounds)

**Decision Rule for Round t:**

1. **Calculate expected cooperators:** 
   - If t = 1: expected_opponents = 0.5 × (n - 1) [neutral expectation for first round]
   - If t > 1: expected_opponents = cooperation_count / (t - 1) [empirical mean from history]

2. **Determine threshold likelihood:**
   - needed_from_others = m - 1 [assuming you cooperate]
   - If expected_opponents ≥ needed_from_others: **COOPERATE**
   - Else: **DEFECT**

3. **Last Round Exception (t = r):**
   - Calculate: likely_cooperators = ⌊expected_opponents + 0.5⌋
   - If (likely_cooperators + 1) ≥ m: **COOPERATE** [you are pivotal]
   - Else if likely_cooperators ≥ m: **DEFECT** [threshold met without you]
   - Else: **DEFECT** [threshold cannot be reached]

4. **After each round:** Observe how many opponents cooperated and update cooperation_count.

**Rationale:**

This strategy commits to collective success by cooperating whenever empirical evidence suggests others will also cooperate enough to meet the threshold. It abandons cooperation only when the observed pattern makes threshold attainment unlikely, at which point individual defection no longer harms collective outcomes. The last round reversion ensures you don't free-ride if others have been supporting the threshold, while avoiding wasted cooperation if the threshold is unattainable.
'''

description_PROSOCIAL_5 = '''
THRESHOLD-RESPONSIVE COOPERATION STRATEGY

**DECISION RULES:**

1. **First Round (t=1):**
   Cooperate unconditionally. This establishes a prosocial baseline and provides information about opponent cooperation levels.

2. **Terminal Round (t=r):**
   Cooperate unconditionally. Since no future payoffs depend on final-round behavior, defecting to gain the +1 private payoff would be purely self-interested. Prosocial play means contributing to collective success even when personally advantageous to free-ride.

3. **All Other Rounds (1 < t < r):**
   
   a. Calculate the **recent success rate**: proportion of the last min(3, t-1) rounds where the cooperation threshold m was met.
   
   b. Observe the **number of others who cooperated** in round t-1 (call this X).
   
   c. Apply the following decision hierarchy:
      - If success_rate ≥ 0.75: **Cooperate** (collaboration is working; maintain)
      - Else if success_rate = 0 (all previous rounds failed): **Cooperate** (attempt recovery; others may shift strategy)
      - Else if X ≥ m - 1: **Cooperate** (threshold is nearly met; push it across)
      - Else if X ≥ m - 2 AND t ≤ r/2: **Cooperate** (midgame investment in reaching threshold)
      - Else if X < m/2 AND t > 2r/3: **Defect** (endgame; cooperation unlikely to reach threshold; preserve endowment)
      - Else: **Cooperate** (default; sustain hope of reaching threshold)

**RATIONALE:**

This strategy prioritizes **prosocial success** over individual payoff maximization. It cooperates when it observes progress, doubles down when recovery is needed, and only strategically defects in late stages when observed cooperation signals a genuinely low probability of meeting the threshold. The strategy remains responsive to opponent behavior while maintaining commitment to collective goals.
'''

description_PROSOCIAL_6 = '''
**Adaptive Threshold Cooperator**

**Decision Rules:**

Cooperate in round t if ANY of the following holds:
1. Previous round showed c ≥ m-1 cooperators (continuing momentum toward threshold)
2. t ≤ 2 (signal willingness early)
3. Average cooperation rate across all previous rounds exceeds (m-1)/n + 0.1 (others show sufficient commitment)

Otherwise, defect.

**Edge Cases:**

- **Round 1:** Cooperate unconditionally. Signal prosocial intent and establish baseline expectations.
  
- **Last round (t = r):** Adjust the threshold for rule 3 downward by 0.05 to encourage final-round cooperation, but maintain honesty about historical patterns. Cooperate if observed cooperators ≥ m-1 in the final round regardless.

- **If m = n:** Always cooperate (universal participation required; defection guarantees collective failure).

- **If m ≤ 2:** Cooperate whenever you observe at least m-1 cooperators in the current round; revert to rules 2 and 3 otherwise.

**Tracking:**

Maintain running average: `coop_rate = (total cooperators observed across all prior rounds) / (n-1) × (number of prior rounds)`

Update after each round observation.

**Rationale:**

Early cooperation signals commitment and breaks symmetric defection equilibria. Threshold-responsive cooperation (rule 1) compounds successful coordination. The historical average check (rule 3) identifies populations with genuine prosocial tendencies while abandoning pools stuck in defection. The tolerance margin (0.1 buffer) reflects uncertainty about opponent strategies and gives cooperative pools benefit of the doubt through mid-game phases. Final-round adjustment recognizes the last-round paradox—slightly lower thresholds encourage reciprocal last moves without sacrificing credibility.
'''

description_PROSOCIAL_7 = '''
**Contingent Cooperation with Threshold Monitoring**

**Round 1:**
Cooperate unconditionally. This establishes prosocial intent and tests willingness of the group.

**Rounds 2 through r-1:**
Observe c = number of others who cooperated in the previous round.

- If c ≥ m - 1: Cooperate
  - Threshold is within reach with our contribution; reciprocate others' effort.

- Else if c > 0: Cooperate
  - Others are showing willingness despite imperfect coordination. Continue signaling and support their effort.

- Else (c = 0): Defect
  - No one cooperated last round. Protect endowment; continued cooperation serves no one.

**Round r (final round):**
Apply the same decision rule as rounds 2 through r-1. The payoff structure is unchanged, so the logic remains valid even at game's end.

**Defection Recovery (optional refinement):**
Track a "defection streak" counter. If you've played Defect for two consecutive rounds due to low cooperation, but the next round shows c > 0, reset and Cooperate again. This prevents lock-in to mutual defection if others attempt recovery.

---

**Rationale:**
This strategy prosocially initiates cooperation, reciprocates genuine attempts by others (even partial ones), and protects against systematic exploitation. It requires minimal history tracking (only the previous round's count) and adapts to opponent behavior without requiring individual-level grudges. The threshold-relative rule ensures you only cooperate when contribution meaningfully increases likelihood of collective success.
'''

description_PROSOCIAL_8 = '''
# Adaptive Threshold Cooperation Strategy

**Round 1 (First Round):**
Cooperate unconditionally. No history exists to inform decisions; start with prosocial optimism to establish cooperative momentum.

**Rounds 2 through r-1 (Middle Rounds):**
Let c_prev = number of cooperators observed in the immediately previous round.

Cooperate if and only if:
```
c_prev + 1 ≥ m - 1
```

Equivalently: Cooperate if the previous round's cooperation count, plus your own cooperation, would meet or exceed the threshold with at least one additional cooperator.

This means:
- If c_prev ≥ m - 1, cooperate (threshold is achievable with your help)
- If c_prev < m - 1, defect (threshold is unlikely even with your contribution)

**Round r (Final Round):**
Apply the same rule as middle rounds:
```
Cooperate if c_prev + 1 ≥ m - 1
```

Do not change behavior in the final round due to end-game effects. Maintaining consistency with prior rounds sustains the signal that cooperation is conditional on collective viability, not discounted by time horizon.

**Rationale:**
This strategy filters out futile cooperation—it avoids paying the cost when the threshold is mathematically unreachable given recent cooperation levels. Simultaneously, it commits to cooperation whenever the group is demonstrably close to the threshold, making the strategy a reliable partner for prosocial opponents. The rule is transparent: "I cooperate when our collective effort is likely to succeed."
'''

description_PROSOCIAL_9 = '''
# Adaptive Threshold Cooperator

## Decision Rules

**Round 1:** Cooperate

Establish that you're willing to contribute. This signals a prosocial orientation and tests whether others reciprocate.

**Rounds 2 to r-1 (Middle Rounds):**

Observe c = number of cooperators from the previous round.

- If c ≥ m: Cooperate
  - Threshold was met. Others are reliably cooperating, so contribute.

- If c = m - 1: Cooperate
  - Just one short. Your cooperation alone achieves the threshold. Contribute.

- If m - 2 ≤ c < m - 1: Cooperate
  - Moderate deficit but meaningful cooperation exists. Contribute to show good faith and give the group another chance.

- If c < m - 2: Defect
  - Too many defectors. Expected cooperators next round unlikely to reach m even with your contribution. Minimize loss by keeping endowment.

**Round r (Final Round):**

Observe c = number of cooperators from round r-1.

- If c ≥ m - 1: Cooperate
  - Threshold is achievable. Contribute to either maintain the cooperative trend or complete it.

- If c < m - 1: Defect
  - Threshold is unreachable. Since no future round follows, you cannot influence group behavior. Accept the loss and keep your endowment.

## Edge Cases

**Uncertainty about total cooperators:** If the aggregate observation is unclear, assume the worst case (fewer cooperators than observed). This prevents overoptimistic cooperation that leads to endowment waste.

**n small relative to m:** When n is barely above m, the deficit threshold adjusts: treat c < m - 2 as "too many defectors." Adjust your tolerance proportionally: Cooperate if c ≥ m - ceil(n/6).

**All defections in round 1:** If c_1 = 0, switch to Defect from round 2 onward. Repeated defection signals irreconcilable strategy mismatch; continued cooperation becomes purely costly.

## Prosocial Orientation

This strategy embodies prosocial behavior by:

- **Initiating cooperation** without waiting for proof of others' trustworthiness
- **Conditional reciprocity**: rewarding group cooperation with further contribution; withdrawing only when threshold becomes mathematically unachievable
- **Forgiveness**: allowing one deficit round (c = m-2) before abandoning cooperation
- **Final-round honesty**: contributing on the last round when the group nearly succeeded, avoiding a cynical defection that breaks momentum
- **No punishment of individuals**: since opponents are unidentifiable, the strategy never punishes; instead, it responds to aggregate outcome quality

The strategy balances prosocial intent against exploitation risk by tying cooperation to realistic probability of threshold achievement.
'''

description_PROSOCIAL_10 = '''
# Threshold-Based Conditional Cooperation

## Core Decision Rule

**In each round t:**
- If t = 1 (first round): Cooperate
- If t > 1: Cooperate if and only if (observed_cooperators_{t-1} ≥ m - 1)

where observed_cooperators_{t-1} is the number of opponents observed cooperating in the previous round.

## Rationale

Cooperate when the threshold is achievable with your participation. If at least m-1 others cooperated last round, your cooperation this round reaches the collective target and triggers the reward for everyone. This avoids free-riding: you don't defect on others' cooperation to pocket the higher individual payoff (1 + k vs 0 + k).

## Edge Cases

**First round:** Unconditionally cooperate. This signals willingness to contribute and tests whether others will reciprocate. Without this initialization, the game defaults to mutual defection.

**Last round (t = r):** Apply the same decision rule. Defecting in the final round purely for individual gain contradicts prosocial intent and may not yield higher total payoff if opponents are using similar adaptive strategies. Maintain consistency across all rounds.

**Threshold already exceeded:** If observed_cooperators_{t-1} ≥ m (threshold met without you), still apply the same rule. Even when success seems guaranteed, defecting to free-ride is not prosocial.

**All opponents defected (observed_cooperators_{t-1} = 0):** Defect. The threshold cannot be met, so cooperation yields no collective benefit and only costs you the endowment.

## Prosocial Alignment

This strategy prioritizes collective success over individual exploitation. It cooperates as long as the group can feasibly meet the threshold, refuses to free-ride on others' contributions, and accepts the symmetric risk: if others won't meet m-1, you also step back rather than unilaterally subsidizing a failing effort.
'''

description_PROSOCIAL_11 = '''
# Responsive Threshold Matching Strategy

**Decision Rule by Round Type:**

**Round 1 (Initial Signal):**
Cooperate unconditionally. This establishes that cooperation is possible and signals prosocial intent, making it easier for others to coordinate on reaching m.

**Rounds 2 to r-1 (Main Phase):**
- Calculate observed cooperation rate: ρ = (cumulative cooperators observed) / (cumulative observations from all opponents across all previous rounds)
- Estimate expected cooperators next round: ε = ρ × (n - 1)

Decision:
- If ε ≥ m - 1: **Cooperate**. Threshold is achievable based on observed behavior.
- If m - 2 ≤ ε < m - 1: **Cooperate** if rounds_remaining ≥ 2, else defect. Border cases warrant investment when future rounds exist.
- If ε < m - 2: **Defect**. Threshold is unattainable; mutual defection is inevitable.

**Round r (Final Round):**
- Recalculate ρ and ε using all previous history.
- If ε ≥ m - 1: **Cooperate**. Give the threshold a final push.
- If ε < m - 1: **Defect**. The game ends; no future reciprocation possible.

**Edge Cases:**

- If n < m: Threshold is impossible. Play **D** every round.
- If m = 2 and n = 2: Always play **C**—mutual cooperation is the only path to shared payoff.
- If all opponents defected in round 1: By round 2, ε = 0. Defect for remaining rounds (rational exit).
- If observation count is zero (round 1 only): Use the unconditional cooperation rule for round 1, then apply empirical update from round 2 onward.

**Prosocial Intent:**

This strategy leads with cooperation, assumes others share prosocial motives, and uses others' revealed behavior to calibrate contribution. It avoids exploitation by defecting when the threshold becomes mathematically unachievable, and reciprocates observed cooperation without requiring explicit communication. The strategy biases toward collective success in early and middle rounds while preserving rationality when the threshold has become unreachable.
'''

description_PROSOCIAL_12 = '''
# COOPERATIVE THRESHOLD MATCHING STRATEGY

## Decision Rules

**Rounds 1-2 (Initialization):**
Cooperate unconditionally. These rounds serve to signal prosocial intent and gather baseline data on opponent cooperation patterns.

**Rounds 3 to r-1 (Adaptive Phase):**
- Calculate: `avg_opponent_coop` = average number of opponents observed cooperating in rounds 1 through t-1
- Expected cooperators if I cooperate: `avg_opponent_coop + 1`
- Expected cooperators if I defect: `avg_opponent_coop`

Decision rule:
```
if expected_cooperators_with_my_C >= m:
  COOPERATE
    (threshold likely reachable; my contribution helps achieve mutual gain)
else:
  COOPERATE
    (threshold unachievable regardless; cooperate anyway for reciprocal signaling)
```

**Round r (Final Round):**
Apply the same adaptive rule as rounds 3 to r-1. Defect only if doing so would free-ride on a threshold that opponents will clearly reach without you, *and* sufficient defection has already occurred in prior rounds to suggest opponents have abandoned cooperation.

## Edge Cases

**Declining cooperation trend:** If `avg_opponent_coop` drops below 1, defect in subsequent rounds. Others have signaled non-cooperation; further unilateral contributions are unsustainable.

**Very small m (m ≤ 2):** Threshold is easily met. Cooperate throughout; the barrier to collective success is minimal, making mutual cooperation rational.

**Very large r (r > 10):** In rounds 3-5, maintain cooperation longer before adapting. The learning phase extends slightly to reduce noise from small samples.

## Prosocial Alignment

This strategy prioritizes reaching the threshold m because the collective payoff structure is positive-sum when the threshold succeeds (k > 1). The approach:
- **Initiates cooperation first** rather than waiting for others to test the waters
- **Infers opponent intent** from aggregate behavior, not punishing individual variation
- **Continues cooperative effort** even when the threshold appears unreachable, signaling that defection is not default and trusting reciprocal prosocial responses
- **Avoids pure free-riding** by only defecting when baseline cooperation has substantially eroded, preserving the possibility of threshold success
'''

description_PROSOCIAL_13 = '''
# Adaptive Threshold Matching with Reciprocal Commitment

**Round 1 (Initial signal):**
Cooperate unconditionally. This signals prosocial intent and demonstrates your willingness to take the collective risk.

**Rounds 2 through r (Main decision rule):**
Let c_{t-1} = number of opponents who cooperated in the previous round.

Cooperate if and only if:
- c_{t-1} ≥ m - 2, OR
- t = 2 (give respondents one round to reciprocate before switching)

Otherwise defect.

**Rationale of decision thresholds:**

The m - 2 threshold means you cooperate if enough others are cooperating that the group needs just one or two more to reach m. This includes the case where m - 1 others cooperated (threshold definitely reaches), and the marginal case where m - 2 cooperated (threshold is one cooperation away). If fewer than m - 2 cooperate, the threshold cannot be reached with your participation alone, so you defect.

**Edge case handling:**

- If m = 2 (minimal threshold), you cooperate whenever any single opponent cooperated. This is maximally prosocial given the game structure.
- If m = n (full cooperation required), you defect once you observe any defection, since the threshold becomes impossible.
- Last round (t = r): Apply the same rule. Do not defect preemptively at the end—consistency maintains trust for mutual benefit if others employ similar logic.
- Degenerate case (m = 1): Cooperate every round; the threshold is always met.

**Prosocial commitment:**

You initiate cooperation despite the dominance of defection, reciprocate when others demonstrate collective intent toward the threshold, and maintain this reciprocal posture through to the final round rather than exploiting at the end. You only withdraw cooperation when the group numerically cannot reach the threshold with your help, avoiding futile sacrifice.
'''

description_PROSOCIAL_14 = '''
# Adaptive Threshold Cooperation Strategy

**Core Decision Rule:**

Cooperate if and only if: the number of cooperators in the previous round was less than m.

Defect if: the number of cooperators in the previous round was m or greater.

**Edge Cases:**

*Round 1:* Cooperate unconditionally. This signals willingness to contribute and gathers information about the baseline cooperation level in the group.

*Subsequent Rounds:* Apply the threshold rule above based on observed cooperation count from the immediately preceding round.

*Final Round (round r):* Cooperate if previous round had fewer than m cooperators. Defect if previous round had m or more cooperators. Maintain consistency with the strategy rather than exploiting the final round.

**Adaptation Logic:**

The strategy operates as a "deficit responder." When observation shows the threshold was not reached, you contribute to increase the likelihood of success in the next round. When the threshold was met, you recognize the collective good has been achieved and do not waste endowment.

**Robustness Properties:**

- Responds to aggregate cooperation levels, not individual patterns (matching the anonymous observation constraint)
- Incentivizes others toward the cooperative equilibrium by rewarding increases in cooperation
- Protects against threshold failure by increasing contribution when cooperation drops below m
- Naturally produces cooperation when players adopt similar logic, as each becomes responsive to the others' aggregate behavior
- Self-corrects: if too many players free-ride after threshold success, cooperation increases in the next round to restore the public good
'''

description_PROSOCIAL_15 = '''
# Threshold Optimism Strategy

**Core Logic:**
Cooperate when the empirical evidence suggests the threshold m is likely to be reached, applying an optimistic but adaptive filter to opponent behavior.

## Decision Rules

**Round 1:**
Always cooperate unconditionally. Signal willingness to contribute and establish baseline for reciprocity estimation.

**Rounds 2 to r-1 (Adaptive Phase):**

1. Calculate observed cooperation frequency:
   - `q = (total cooperations observed across all previous rounds) / ((current_round - 1) × (n - 1))`

2. Estimate expected cooperators among opponents:
   - `expected_others = q × (n - 1)`

3. Decide based on threshold likelihood:
   - If `expected_others + 1 ≥ m`: **Cooperate**
     (Threshold reachable with my contribution)
   - If `expected_others < m - 1`: **Defect**
     (Threshold unreachable even if I cooperate)
   - If `m - 1 ≤ expected_others < m`: **Cooperate with probability (m - expected_others)**
     (Marginal cases warrant scaled cooperation)

4. Apply generosity buffer: Interpret `q` with +5% margin of doubt in favor of others' willingness. Use `q' = max(q, q + 0.05)` when q < 0.5 to avoid over-pessimism early.

**Last Round (Round r):**

Cooperate if `expected_others ≥ m - 1`. Defect otherwise.

The final round abandons hope if cooperation hasn't coalesced by then, but still cooperates if the threshold appears secure.

## Edge Cases

- **Unanimous defection observed (q = 0):** Defect in all subsequent rounds.
- **Unanimous cooperation observed (q = 1):** Cooperate for all remaining rounds.
- **Exactly one round left:** Cooperate only if observed cooperation rate suggests threshold is certain (`expected_others ≥ m - 1`).

## Prosocial Alignment

This strategy embodies pragmatic prosociality:
- Leads with trust and contribution in round 1
- Remains optimistic about others' willingness by applying a generosity buffer
- Avoids tragic coordination failure by basing decisions on observed collective patterns, not worst-case assumptions
- Preserves payoff integrity: stops cooperating unilaterally only when evidence genuinely contradicts threshold feasibility
- Reciprocal structure: cooperation increases as others cooperate, without requiring explicit communication
'''

description_PROSOCIAL_16 = '''
# Threshold-Responsive Cooperative Strategy

## Decision Rule

**Round 1:** Cooperate unconditionally. This initiates cooperation and signals prosocial intent.

**Rounds 2 to r-1:** 
- Count the number of others who cooperated in the immediately previous round (call this `prev_cooperators`)
- If `prev_cooperators ≥ m - 1`: Cooperate
- If `prev_cooperators < m - 1`: Defect

**Round r (final round):**
- If at any point in rounds 1 through r-1 you observed `prev_cooperators ≥ m - 1`: Cooperate
- Otherwise: Defect

## Edge Case Handling

**Threshold barely met:** When exactly `m - 1` others cooperated in the previous round, you still cooperate. This acknowledges that the risk threshold was survivable and justifies further cooperation attempts.

**Early defection pattern:** If opponents immediately defect (you observe 0 cooperators in round 2), switch to defection in round 3. This avoids repeated wasted contributions against fully defective populations.

**Terminal incentive:** In the final round, if cooperation ever became viable (threshold nearly met in any earlier round), lock in cooperation even though individual payoff would be higher from defection. This honors the mutual benefit structure and demonstrates commitment to the cooperative outcome when it's reachable.

## Prosocial Alignment

The strategy prioritizes enabling the collective threshold while protecting against systematic exploitation. It reciprocates observed cooperation levels, assumes other players might be trying to coordinate rather than pure free-riders, and maintains cooperation viability for as long as evidence supports it. By always cooperating in round 1 and giving a final cooperation attempt when the threshold has proven achievable, it maximizes the probability of mutual risk-aversion across all players and total group welfare.
'''

description_PROSOCIAL_17 = '''
## PROSOCIAL THRESHOLD-FOLLOWING STRATEGY

**Round 1 (Opening):**
Cooperate. Signal good-faith intent to participate in the collective project.

**Rounds 2 through r-1 (Adaptive Middle Game):**
Let c_prev = number of cooperators in the immediately preceding round.

- **If c_prev ≥ m:** Cooperate unconditionally. The threshold has been met; sustain the cooperative equilibrium.

- **If c_prev < m:** Defect *unless* you estimate that your cooperation would be pivotal.
  - Cooperate if and only if: c_prev + 1 ≥ m (i.e., your contribution alone closes the gap to threshold)
  - This is the "swing vote" condition—cooperate only when your action bridges the deficit.
  - Otherwise defect.

**Last Round r (Endgame):**
Let c_prev = cooperators in round r-1.

- **If c_prev ≥ m:** Cooperate. Maintain the success streak; there is no future reciprocation to lose.

- **If c_prev < m:** Cooperate if and only if c_prev + 1 ≥ m.
  - Same pivotal logic as middle rounds. In the final round, defection is most tempting (no retaliation possible), so commit to this rule strictly.

**Rationale:**
This strategy is simultaneously robust and prosocial. It avoids wasting cooperation on rounds where the threshold cannot be reached (preventing wasted sacrifice), while reliably contributing when your action is decisive. By cooperating whenever the threshold has been met, it rewards and stabilizes cooperation-based outcomes. The opening cooperate signals reciprocal intent, and the pivotal-voter heuristic ensures you contribute to success without naive over-investment in hopeless scenarios.
'''

description_PROSOCIAL_18 = '''
# Adaptive Threshold-Tracking Strategy

**Decision Rule by Round:**

**Round 1:** Cooperate unconditionally. This establishes prosocial intent and provides opponents a baseline signal.

**Rounds 2 through r-1:** Observe the number of cooperators from the previous round, denote this as C_prev.
- If C_prev ≥ m: Cooperate
- If m/2 < C_prev < m: Cooperate  
- If C_prev ≤ m/2: Defect

**Round r (final round):** Cooperate unconditionally.

---

**Rationale for Decision Thresholds:**

When C_prev ≥ m, the threshold was met in the prior round—others are reliably cooperating, and you benefit from cooperating (receiving k). Defecting here is exploitative.

When m/2 < C_prev < m, the group is trending upward toward coordination. Cooperating provides a "pull" effect: increasing the cooperator count helps breach the threshold in the next round. This reflects optimism about collective capacity.

When C_prev ≤ m/2, the cooperation base is too small. The probability of reaching m in the next round is low; cooperating here is wasteful. Defect to preserve endowment while still capturing k if others achieve threshold by chance.

---

**Last Round Exception:**

In round r, cooperation is costless relative to future rounds. Cooperate regardless of history to maximize the collective payoff. If the threshold is met, your contribution is irrelevant (others determined it); if not, your cooperation cannot hurt.

---

**Adaptive Properties:**

- Responds to the actual cooperation trajectory your opponents exhibit
- Escalates investment when momentum toward m is visible
- Exits gracefully when the group is clearly uncooperative
- Uses the midpoint m/2 as a pivot to distinguish "salvageable" from "lost cause" scenarios
- Distinguishes early coordination attempts (high tolerance) from terminal failure (defect)
'''

description_PROSOCIAL_19 = '''
## Empirical Threshold Targeting Strategy

**Round 1 (Initialization):**
Cooperate. Establish prosocial signal and generate data about opponent willingness to cooperate.

**Rounds 2 through r (including final round):**

1. Compute empirical cooperation rate from opponents:
   - observed_total = sum of opponent cooperators across all previous rounds
   - opponent_coop_rate = observed_total / ((current_round - 1) × (n - 1))

2. Estimate expected cooperators in current round:
   - expected_other_cooperators = opponent_coop_rate × (n - 1)

3. Decision rule:
   - If expected_other_cooperators + 1 ≥ m: **Cooperate**
   - Otherwise: **Defect**

**Rationale:**

You cooperate exactly when your own contribution, combined with the empirically expected contributions from others, is projected to meet the threshold m. This avoids wasting your endowment on failed collective outcomes while supporting successful ones.

**Specific edge cases:**

- **Very early observations**: If you've only seen round 1, use that single data point to estimate the rate. The strategy still applies.
- **Final round**: Apply the same decision rule without modification. The lack of future rounds doesn't change whether the current threshold is achievable.
- **Consistently high cooperation (rate ≥ m/(n-1))**: You cooperate every round after round 1, maximizing collective payoff.
- **Consistently low cooperation (rate < m/(n-1))**: You defect after round 1, protecting yourself from wasted contributions while others free-ride.
- **Threshold = n (all must cooperate)**: You defect unless you observe perfect cooperation from all opponents—a stringent but honest standard.
'''

description_PROSOCIAL_20 = '''
# Threshold-Seeking Adaptive Cooperator

**Round 1 (Opening move):**
Cooperate unconditionally. This signals willingness to contribute and tests whether collective action is feasible with the current opponent composition.

**Rounds 2 through r (Adaptive phase):**

Let obs = the number of other players (out of n−1) who cooperated in the previous round.

- **If obs ≥ m − 1:** Cooperate
  - The threshold was reached or is within reach. Continue supporting collective success.

- **If obs < m − 1:** Defect
  - Even adding your cooperation would yield fewer than m total cooperators. Threshold is unattainable; free-ride on any spillover reward if it occurs, preserve endowment otherwise.

**Last round (round r):**
Apply the same rule as above, but shift the threshold slightly lower: Cooperate if obs ≥ m − 2. This gives collective action one final opportunity when closing rounds often see reduced cooperation.

**Rationale for prosocial alignment:**

- **Initiating cooperation**: Round 1 cooperation breaks the mutual defection equilibrium and demonstrates good faith.
- **Sustained contribution**: Continuing when the threshold has been met ensures the collective good persists across the game.
- **Efficiency**: Defecting when the threshold is mathematically unreachable avoids wasting your endowment when collective success is impossible.
- **Hope-preserving**: Lowering the threshold in the final round reflects that this is the last chance to achieve the joint gain, warranting slightly more optimistic cooperation.

The strategy is robust because it doesn't depend on identifying individual players (impossible under anonymity), only on aggregate cooperation counts, and responds to empirical evidence of whether group-level coordination is actually occurring.
'''

description_PROSOCIAL_21 = '''
**Pragmatic Threshold Cooperation**

**Round 1:**
Cooperate unconditionally. Initialize with prosocial intent and signal to others that cooperation is possible.

**Rounds 2 through r:**
Let c_prev = number of cooperators observed in the immediately preceding round.

- **If c_prev ≥ m:** Cooperate
  - The threshold was achieved; sustain the mutually beneficial equilibrium.

- **Else if m - c_prev ≤ 2:** Cooperate
  - The gap to threshold is small (1-2 cooperators short). Continue contributing to create closing momentum and increase the chance others will reciprocate.

- **Else:** Defect
  - Cooperation is too sparse to likely reach the threshold. Minimize individual losses while the gap remains large.

**Final round treatment (round r):**
Apply the same decision rule above. Do not optimize specifically for the final round by defecting; sustain cooperation if threshold conditions support it, to maintain collective welfare.

**Rationale:**
The strategy cooperates initially to demonstrate good faith and test whether others will reciprocate. It then conditions future cooperation on whether the threshold is within realistic reach—either already achieved (maintain it) or nearly achieved (close the gap). By defecting only when the cooperation gap is too large to plausibly close, the strategy avoids exploitation while reserving reciprocal cooperation for scenarios where collective success is feasible. This balances prosocial aspiration with adaptive realism about opponent behavior.
'''

description_PROSOCIAL_22 = '''
**Strategy: Adaptive Threshold Reciprocity with Endgame Cooperation Push**

**Decision Rule - Standard Rounds:**

```
Let c_prev = number of cooperators observed in the previous round
Let c_avg = average number of cooperators in all previous rounds
Let rounds_remaining = r - current_round

If current_round == 1:
    Action = C (cooperate)
    
Else if c_prev >= m - 1:
    Action = C (cooperate)
    // Others provided sufficiently; you can be the threshold-maker
    
Else if c_avg >= m - 0.5:
    Action = C (cooperate)
    // Sustained cooperation trend warrants reciprocation
    
Else if rounds_remaining <= 2 AND c_avg >= m - 1.5:
    Action = C (cooperate)
    // Final rounds: lower threshold to make last attempts at cooperation viable
    
Else if rounds_remaining == 1:
    Action = C (cooperate)
    // Final round: cooperate unconditionally to help others who've been reciprocating
    
Else:
    Action = D (defect)
```

**Edge Cases:**

- **Round 1:** Always cooperate. This signals genuine willingness to participate and provides empirical information about the group's baseline cooperativeness.

- **Last Round (round = r):** Always cooperate. You gain no future benefit from reputation, so the only prosocial action is to help others reach the threshold if they've reciprocated previously.

- **Second Round:** Use the n-1 players' first-round choices to calibrate expectations. If fewer than m-2 cooperated in round 1, reduce future cooperation probability gradually rather than immediately defecting.

**Rationale:**

This strategy embeds reciprocity (matching observed cooperation levels) while maintaining a prosocial lean. Early cooperation establishes that you're trustworthy, not selfish. Conditional cooperation in the middle game responds to whether others are meeting their contribution level. The endgame adjustment prevents collective failure when the group is close to the threshold—small pushes in final rounds can tip a wavering group toward success.
'''

description_PROSOCIAL_23 = '''
**CONDITIONAL COOPERATION WITH COLLECTIVE THRESHOLD TARGETING**

**Core Decision Rule:**

Cooperate in round t if and only if:
- Your cooperation would move the group toward or across the minimum threshold m, AND
- The historical trend suggests this cooperation has reasonable probability of being reciprocated by enough others

Specifically:

**Round 1:**
Cooperate. Establish prosocial intent as a baseline signal.

**Rounds 2 to r-1 (middle rounds):**
Let c_t-1 = number of cooperators observed in round t-1.

- If c_t-1 ≥ m: **Cooperate**
  (Threshold was met last round; reciprocate and sustain collective success)

- If c_t-1 = m - 1: **Cooperate**
  (You are the marginal cooperator needed; your cooperation ensures threshold)

- If m - 2 ≤ c_t-1 < m - 1: **Cooperate with probability p = (c_t-1 - (m-2)) / 2**
  (Gradient: trend is moving toward threshold; cooperate with increasing confidence)

- If c_t-1 < m - 2 AND c_t-1 < c_t-2: **Defect**
  (Cooperation trend is declining; threshold unlikely, avoid wasted contribution)

- If c_t-1 < m - 2 AND c_t-1 ≥ c_t-2: **Cooperate with probability p = min(0.3, c_t-1 / m)**
  (Trend is improving or stable; weakly encourage escalation)

**Round r (final round):**
- If average cooperation across all prior rounds ≥ m / n: **Cooperate**
  (Reciprocate demonstrated group commitment, even in endgame)
  
- Else: **Defect**
  (No future rounds to benefit from cooperation signal; optimize final payoff)

**Tie-breaking rule:**
When indifferent between C and D, choose C (default prosocial bias).
'''

description_PROSOCIAL_24 = '''
SINCERE RECIPROCAL STRATEGY

**Core Principle:**
Cooperate when threshold success appears achievable or when early coordination benefits remain plausible. Defect only when evidence suggests cooperation is futile and the final round offers no chance to influence others.

**Decision Rules:**

**Round 1:**
Always cooperate. This serves as an unambiguous prosocial signal and generates baseline data on opponent behavior.

**Rounds 2 through r-1:**

Calculate threshold_success_rate = (number of rounds where ≥m players cooperated) / (current_round - 1)

- If threshold_success_rate ≥ 0.5: Cooperate
  - Threshold is achievable; maintain momentum toward equilibrium.

- Else if current_round ≤ ceil(r/2): Cooperate
  - Early enough that consistent cooperation can still shift opponent behavior toward cooperation.

- Else if current_round > ceil(r/2) AND threshold_success_rate = 0: Defect
  - Evidence of coordination failure; no remaining time to establish cooperation.

- Else if ceil(r/2) < current_round < r: Cooperate
  - Late-game attempt: if threshold succeeded even once, maintain faith in the cooperative possibility.

**Round r (Final Round):**

- If threshold_success_rate > 0.2: Cooperate
  - Any evidence of threshold success justifies a final cooperative push (no future rounds to influence, but maximizes payoff if others also cooperate).

- Else: Defect
  - Threshold has never been reached; exploit the final round.

**Rationale:**
This strategy avoids indefinite losses by establishing a temporal boundary on cooperation attempts while remaining open to coordination recovery if even modest evidence of threshold success appears. It signals genuine commitment to the collective outcome early, responds to observed patterns without vindictiveness, and protects against complete exploitation by opponents who never attempt coordination.
'''

description_PROSOCIAL_25 = '''
# Adaptive Threshold Cooperation Strategy

**Core Decision Rule:**

In each round, cooperate if and only if one of the following conditions holds:
1. This is round 1, OR
2. In the previous round, observed_cooperators ≥ m - 1

Otherwise, defect.

**Explanation of Decision Rule:**

The strategy estimates whether the cooperation threshold m is likely to be met based on observed behavior. If at least m-1 others cooperated previously, then your cooperation ensures the threshold is met (assuming cooperation rates remain stable). This secures the collective reward k for everyone. If fewer than m-1 others cooperated, the threshold is unlikely to be reached regardless of your action, so you defect to keep your endowment.

**Edge Cases:**

- **Round 1:** Cooperate unconditionally. With no history, this initiates prosocial behavior and signals willingness to contribute.

- **Final round (round r):** Apply the same decision rule. Defecting in the final round is rationally tempting, but a prosocial strategy maintains consistency. The decision rule naturally produces less defection than pure self-interest would.

- **Rounds 2 through r-1:** Apply the threshold rule strictly. Each round provides new aggregate information to refine your estimate of others' commitment levels.

**Robustness Properties:**

- **Against full cooperation:** You cooperate consistently, reaching payoff 2r.
- **Against full defection:** You cooperate round 1 only (payoff r+k), minimizing losses.
- **Against mixed behavior:** You responsively match the observed cooperation intensity, supporting the threshold when feasible but abandoning costly cooperation when the collective goal appears unachievable.

The strategy is adaptive because it conditions on observed history, prosocial because it prioritizes securing the collective reward whenever feasible, and robust because it gracefully handles any opponent composition.
'''

description_PROSOCIAL_26 = '''
# Prosocial Adaptive Threshold Strategy

**Round 1:**
Always cooperate. Signal prosocial intent and provide initial evidence that cooperation is viable.

**Rounds 2 through r-1 (intermediate rounds):**
Let C_prev = number of cooperators observed in the immediately preceding round.

- If C_prev ≥ m - 1: Cooperate
- If C_prev < m - 1: Defect

**Round r (final round):**
Let C_prev = number of cooperators in round r-1.

- If C_prev ≥ m - 1: Cooperate
- If C_prev < m - 1: Defect

---

**Rationale for edge cases:**

*First round:* Cooperating unconditionally establishes good faith when history is absent. This maximizes the probability that others reciprocate.

*Intermediate rounds:* If m-1 others cooperated last round, your cooperation reaches the threshold. This creates a self-fulfilling equilibrium: when others see high past cooperation, they cooperate, making threshold attainment reliable. When cooperation drops below m-1, defecting protects you from wasted contribution.

*Final round:* Apply the same threshold rule. If the cooperation level was insufficient in the prior round, contributing now gains nothing (threshold failure is likely). If m-1 others cooperated, your cooperation completes the threshold and secures the reward for all including yourself.

---

**Adaptation mechanism:**

The strategy tracks one piece of observable history: the aggregate cooperation count from the previous round. This single feedback signal creates a dynamic where:
- Cooperative environments sustain themselves (if m-1+ cooperate, you join)
- Defective spirals are rejected (if too few cooperate, you protect yourself)
- No coordination mechanism is needed; reciprocity emerges from local threshold responsiveness
'''

description_PROSOCIAL_27 = '''
**PRAGMATIC PROSOCIAL COOPERATION**

**Round 1 (Initialization):**
Cooperate unconditionally. Signal willingness to contribute to collective gain.

**Rounds 2 through r-1 (Middle Rounds):**
Cooperate if and only if at least (m - 1) other players cooperated in the immediately preceding round.

If fewer than (m - 1) others cooperated in the preceding round, apply the optimism checkpoint:
- Compute the cooperation rate among observed opponents: ρ = (observed_cooperators) / (n - 1)
- If ρ ≥ 0.35, Cooperate (give cooperation trend time to recover)
- If ρ < 0.35, Defect (threshold is unreachable with current trajectory)

**Round r (Final Round):**
Cooperate if and only if at least (m - 1) other players cooperated in round r-1. Otherwise Defect (no future rounds to rebuild reputation; preserve individual payoff).

**Rationale for Design:**

The strategy prioritizes threshold achievement: cooperation yields mutual gain only if m or more players contribute. By conditioning on observing at least (m-1) others cooperating, you guarantee collective success when you add your contribution, eliminating wasted cooperation.

The optimism checkpoint in middle rounds prevents premature defection spirals. A cooperation rate above 0.35 signals that the group retains capacity to reach threshold, so continuing contribution preserves possibility of collective success without being naive to persistent defection.

The final-round defection rule removes the asymmetry of the last round: once you cannot influence future behavior or reputation, individual payoff (1 + k vs. k) takes precedence if the threshold appears unachievable.

This balances prosocial orientation—initiating cooperation, tolerating temporary shortfalls, and investing in threshold achievement—with strategic realism about when cooperation is futile.
'''

description_PROSOCIAL_28 = '''
# Adaptive Threshold-Seeking Cooperation Strategy

**Decision Rule:**

Maintain a running estimate of opponent cooperation by tracking the number of cooperators observed in each previous round. In each round, estimate how many of the other (n-1) players will cooperate based on the empirical frequency from history, then cooperate if and only if this expected opponent cooperation count is sufficient to reach the threshold m when combined with your own cooperation.

**Precise Logic:**

```
For each round t ∈ {1, 2, ..., r}:
  
  If t = 1:
    Action = C (Cooperate)
  
  Else:
    Let c_history = [c_1, c_2, ..., c_{t-1}] be the observed number of 
                     cooperators in each previous round
    
    observed_opponent_rate = mean(c_history / (n-1))
    expected_opponent_cooperators = round((n-1) × observed_opponent_rate)
    
    If (expected_opponent_cooperators + 1) ≥ m:
      Action = C
    Else:
      Action = D
```

**First Round (t=1):**
Cooperate unconditionally. This establishes a prosocial signal and provides baseline information about the group.

**Middle Rounds (1 < t < r):**
Cooperate when the empirical cooperation frequency from prior rounds suggests that your contribution would complete the threshold. This is forward-looking: you cooperate only if you believe others' behavior warrants it.

**Final Round (t=r):**
Apply the same decision rule as middle rounds. Maintain consistency rather than defecting purely because there are no future consequences; this honors the prosocial commitment and respects mutual cooperation if it has emerged.

**Robustness Features:**

- **Graceful degradation:** If opponents cooperate rarely, you stop wasting contributions and defect.
- **Threshold-seeking:** You only contribute when cooperation plausibly reaches m, avoiding futile losses.
- **History-weighted:** The strategy automatically adapts to observed group behavior without requiring predetermined assumptions about opponent types.
- **Prosocial bias in uncertainty:** When the expected opponent cooperation is near the threshold boundary, the rounding convention and the first-round signal create a slight bias toward cooperation, encouraging efficient outcomes.
'''

description_PROSOCIAL_29 = '''
# ADAPTIVE PROSOCIAL COOPERATION (APC)

## Decision Rule

**Round 1 (initialization):**  
Cooperate unconditionally. Signal prosocial commitment and set a cooperative precedent.

**Rounds 2 through r (subsequent rounds):**

Observe C_prev = the number of other players who cooperated in the immediately preceding round.

```
if C_prev ≥ m - 1:
    Action = Cooperate
    [Threshold was met last round; reciprocate and maintain the successful equilibrium]

else if C_prev ≥ m - 2:
    Action = Cooperate
    [Close to threshold; additional cooperation substantially improves chance of success]

else if C_prev < m - 2:
    if (round number < r - 1) OR (C_prev > 0):
        Action = Cooperate
        [Long time horizon remains, or at least someone tried; persist in prosocial signal]
    else:
        Action = Defect
        [Final round AND universal defection in previous round; defection inevitable]
```

## Edge Cases

**Universal defection (C_prev = 0):**  
- If rounds remain before final round: Cooperate (rare signals warrant persistence; strategic hope).  
- If this is the final round: Defect (mathematically impossible to meet threshold; cooperating provides no benefit to anyone).

**High cooperation (C_prev ≥ n - 2):**  
- Cooperate regardless. The group is strongly coordinated; reciprocate to sustain it.

**Last round (t = r):**  
- If threshold has been met in any previous round: Cooperate (establish reciprocal trust as the final action).  
- If threshold has never been met: Still cooperate (ending with defection contradicts prosocial principles; at least attempt to help one final time).

## Prosocial Alignment

This strategy:
- **Reciprocates cooperation** to reward and strengthen prosocial coordination.
- **Maintains reliability** through consistent cooperation except when mathematically futile.
- **Avoids free-riding** by not defecting when threshold is achievable.
- **Persists when isolated** during mid-game, signaling that coordination is worth pursuing even if others initially hesitate.
- **Concedes only to inevitability**, not to competition or greed.
'''

description_PROSOCIAL_30 = '''
**Adaptive Threshold-Seeking Strategy**

**Core principle:** Cooperate when there is credible evidence that the collective threshold is attainable; defect when the group repeatedly fails to cooperate sufficiently.

**Decision rule for rounds 1 to r-1:**

Maintain a running history of observed cooperator counts from all completed rounds.

- **Round 1:** Cooperate unconditionally. This signals prosocial intent and tests whether others will reciprocate.

- **Rounds 2 through r-1:** 
  - Count the number of previously completed rounds where the observed cooperation level was ≥ m-1.
  - If this count represents ≥ 50% of completed rounds so far, Cooperate.
  - Otherwise, Defect.

**Decision rule for round r (final round):**

Defect unconditionally. With no future rounds remaining, cooperation provides no signal value and only reduces your payoff.

**Rationale for each phase:**

The first-round cooperation is a prosocial "probe"—it demonstrates willingness to incur cost for collective benefit and creates the possibility of momentum. The mid-game threshold check adapts to opponent behavior: if others have consistently cooperated enough to hit m-1 even without you, your cooperation tips the group into success. If they have not, continuing to cooperate wastes your endowment. The final-round defection reflects the harsh truth of one-shot interactions—there is no reputational return on cooperation when the game ends.

**Edge case handling:**

If n = 2 and m = 2, you must cooperate rounds 1 through r-1 for the threshold to ever be reached (both players needed). The 50% threshold in the adaptive rule still applies: after round 1, if your opponent defected, you have 0/1 rounds meeting the threshold, so you switch to defect.

If m = n, only mutual cooperation works. Apply the rule as stated; you will likely defect from round 2 onward unless all other n-1 players consistently cooperate.
'''

description_PROSOCIAL_31 = '''
# Adaptive Generous Conditional Cooperation Strategy

**Decision Rule:**

Cooperate in round t if and only if:
- **Round 1**: Always cooperate (prosocial initiation)
- **Rounds 2 to r-1**: Cooperate if the number of other players observed cooperating in round t-1 is ≥ m-2
- **Round r (final)**: Cooperate if the number of other players observed cooperating in round r-1 is ≥ m-2

**Rationale for thresholds:**
- If others' cooperation ≥ m-1: threshold is guaranteed with my cooperation → cooperate
- If others' cooperation = m-2: threshold achievable only with my participation. The expected positive outcome (collective welfare maximization) justifies the risk → cooperate
- If others' cooperation ≤ m-3: threshold unattainable even with my cooperation. Defecting preserves value without affecting the outcome → defect

**Edge cases:**

*When m > n (impossible threshold)*: Always defect, as the threshold cannot be met.

*When m = 2 and observed_cooperators = 0*: Defect, since two cooperators are needed and you alone cannot achieve this.

*Final round strategy*: Maintain the same conditional rule rather than pivot to pure defection. This preserves reputational reasoning and ensures consistent commitment. If others have cooperated sufficiently to suggest threshold achievement is plausible, honor that trajectory.

**Why prosocial:**
- Opens with trust and reciprocal vulnerability
- Supports collective threshold achievement whenever feasible without guaranteed failure
- Penalizes free-riding (defect when others won't cooperate) while rewarding reciprocal cooperation
- Maintains cooperative norm throughout, including the final round, avoiding the "defection cliff" that undermines fragile cooperation
'''

description_PROSOCIAL_32 = '''
# ADAPTIVE THRESHOLD-SEEKING STRATEGY

**Core Principle:** Cooperate to promote reaching the threshold m, but adapt based on observed evidence of others' willingness to cooperate. Maintain prosocial engagement as long as empirical conditions support it.

## Decision Rules

**Round 1:** Cooperate unconditionally. Signal prosocial intent and gather initial information about the population.

**Rounds 2 through r:**

1. Calculate observed cooperation rate from all previous rounds:
   ```
   observed_rate = (total cooperators seen across all prior rounds) / 
                   (number of prior rounds × n)
   ```

2. Project expected cooperators if you cooperate this round:
   ```
   expected_cooperators = observed_rate × (n - 1) + 1
   ```

3. Decision rule:
   ```
   IF expected_cooperators ≥ m THEN
     Play C
   ELSE
     Play D
   ```

## Edge Cases and Refinements

**Very early rounds (t ≤ 3):** If observed_rate is undefined or extremely sparse, use a lenient threshold: cooperate if even modest cooperation from others could plausibly reach m. Alternatively, assume observed_rate ≥ (m-1)/(n-1) in round 2 if no data exists yet, allowing initial cooperative momentum.

**Last round (t = r):** Apply the same decision rule. Cooperate if the threshold appears reachable—the payoff k still applies in the final round, making cooperation rational when threshold conditions are favorable.

**Extreme observations:** If observed_rate = 0 across all prior rounds, expect only 1 cooperator (yourself), so defect unless m = 1. If observed_rate > (m-1)/(n-1), maintain cooperation—the threshold is reliably reachable.

## Prosocial Alignment

This strategy embodies prosocial values through conditional reciprocity: you actively try to enable collective success by cooperating whenever empirical evidence suggests others are making the project viable. You don't require perfect universal cooperation—only that the observed behavior pattern makes reaching m plausible. You reward cooperation signals without blind optimism, and you withdraw only when the collective dynamic demonstrates insufficient engagement. You continue this approach even in the final round, refusing to exploit the endgame when collective success remains achievable.
'''

description_ALTRUISTIC_5 = '''
# Altruistic Threshold-Seeking Strategy

## Decision Rules

**Core principle**: Cooperate when the collective threshold appears achievable; otherwise, minimize loss while maintaining some hope for future cooperation.

**General rule for rounds 2 through r-1**:
- Let `c_prev` = observed number of cooperators in the immediately preceding round
- Calculate threshold viability: `needed = max(0, m - 1 - c_prev)` (additional cooperators needed if I cooperate)
- If `needed ≤ (n - 1 - c_prev)`, then cooperate. Otherwise, defect.

In simpler terms: cooperate if your cooperation, combined with observed recent cooperation, could plausibly reach m total. This is forward-looking altruism—you contribute when you believe it completes the threshold.

**Smoothing for uncertainty**: Track the moving average of cooperation over the last two rounds. If average cooperation rate exceeds `(m - 1) / n`, cooperate regardless. This prevents over-reacting to a single low-cooperation round.

## Edge Cases

**Round 1**:
Cooperate unconditionally. This seeds the threshold-seeking behavior and signals willingness to help without requiring proof from opponents first.

**Last round (round r)**:
Apply the same decision rule as any other round. Do not defect opportunistically. Altruism means remaining consistent with your commitment to the group good, even when future punishment is impossible.

**Degenerate threshold cases**:
- If `m = n` (all must cooperate): cooperate if any opponent cooperated in the previous round; otherwise, defect to minimize pointless loss.
- If `m = 2` (almost any cooperation succeeds): cooperate in all rounds except the last if no opponent has cooperated by round r-2.

## Altruistic Alignment

This strategy prioritizes the group welfare by:
1. **Cooperating toward collective success**: You never defect purely for personal gain; you only defect when you judge the threshold impossible to reach.
2. **Sustained hope**: You don't reciprocate tit-for-tat punishment. One defecting opponent doesn't trigger your defection if the threshold remains viable.
3. **Consistency**: You don't exploit the last round; your commitment is real and unconditional on retaliation.
4. **Minimal selfishness**: You exit cooperation only when sacrifice becomes futile, not when you could gain advantage.
'''

description_ALTRUISTIC_6 = '''
# Adaptive Threshold Seeking Strategy

## Core Decision Rule

**Cooperate if and only if:**
- Estimated probability that m or more total cooperators will emerge this round is sufficiently high, OR
- We are in the final rounds and the group is close to achieving any successful outcome

More precisely:

```
if round == 1:
    COOPERATE (signal willingness; establish baseline)
else:
    recent_cooperation_rate = average cooperators observed in last 2 rounds
    estimated_cooperators_this_round = ceil(recent_cooperation_rate * n)
    
    if estimated_cooperators_this_round >= m:
        COOPERATE (threshold appears reachable)
    elif estimated_cooperators_this_round == m - 1:
        COOPERATE (we may be the marginal player)
    elif round > r * 0.75:  // final quarter
        if estimated_cooperators_this_round >= m - 2:
            COOPERATE (last chance; threshold still plausible)
        else:
            DEFECT (threshold hopeless; preserve endowment)
    else:
        if estimated_cooperators_this_round >= m - 2:
            COOPERATE (early signal; build cooperative momentum)
        else:
            DEFECT (cooperation rate too low; wait for response)
```

## Edge Cases

**Round 1:** Always cooperate. This is the only way to communicate willingness to participate and test opponent responses without historical data. Defecting from the start signals free-riding intent.

**Final round (round r):** Use the full decision rule above. Unlike repeated games where cooperation is weakly incentivized by iteration, here cooperation in the final round only makes sense if the threshold is achievable—otherwise defecting avoids wasted contribution.

**When cooperation rate drops to zero:** If no cooperators have been observed for two consecutive rounds, defect. The threshold cannot be reached; further contribution yields payoff 0.

**Ties in estimation:** If observed cooperators exactly equal m - 1, cooperate. This reflects altruistic assumption that others share your intent.

## Altruistic Alignment

This strategy prioritizes **collective survival and welfare** over individual payoff:

- **Round 1 cooperation** signals: "I trust this group to cooperate" and creates the possibility of mutual success.
- **Monitoring and adaptive adjustment** respects others' strategic choices while trying to find a cooperative equilibrium.
- **Threshold-seeking focus** recognizes that individual contributions are only meaningful if they help the group reach m—wasted contributions that prevent m being met represent failed altruism.
- **Marginal player logic** embodies reciprocal altruism: if others have brought cooperation close to the threshold, you contribute to "seal" collective success rather than free-ride.
- **Late-round adjustment** acknowledges sunk costs: past failures to reach m do not justify continued altruistic punishment. But a plausible late-game path to m triggers final cooperative efforts.
'''

description_ALTRUISTIC_7 = '''
# Cooperative Threshold Strategy

## Decision Rule

**Round 1**: Cooperate unconditionally. (Altruistic initialization: assume others have cooperative intent.)

**Rounds 2 through r−1**: 
- Let `c_prev` = number of cooperators observed in the immediately preceding round
- If `c_prev + 1 ≥ m`: Cooperate (threshold is achievable with my contribution)
- Else if `c_prev ≥ m − 2`: Cooperate (nearly enough; worth the sacrifice to get there)
- Else if `c_prev / (n−1) ≥ 0.4 × (m/n)`: Cooperate (meaningful cooperation observed; maintain faith for future mutual benefit)
- Else: Defect (cooperation rate too low to expect threshold to materialize)

**Round r (final round)**:
- Let `c_prev` = number of cooperators observed in round r−1
- If `c_prev + 1 ≥ m`: Cooperate (secure the final success)
- Else: Defect (threshold is already unreachable; no future rounds to recover reputation value)

## Altruistic Alignment

This strategy embodies altruism through:

1. **Threshold-oriented sacrifice**: Cooperates even when defection yields higher payoff (1 vs k−1) if the threshold is reachable, because cooperation enables the collective reward that benefits all players.

2. **Good-faith persistence**: Maintains cooperation through the middle rounds even when the previous round showed fewer than m cooperators, provided the cooperation rate is substantial enough to suggest convergence toward the threshold. This avoids premature cascade into mutual defection.

3. **Graceful degradation**: Defects only when empirical evidence suggests the threshold cannot be met—not from naked self-interest, but from recognizing that unilateral sacrifice is futile when others have already signaled insufficient commitment.

4. **Final-round realism**: Breaks cooperation discipline in the last round only if threshold is already implausible, avoiding wasted sacrifice when no future reciprocity is possible.
'''

description_ALTRUISTIC_8 = '''
# Threshold Targeting with Adaptive Commitment

## Decision Rule

Let c_t denote the number of other players who cooperated in round t (observed after round t concludes).

**Round 1:**
Cooperate. Establish altruistic intent and gather information about the group's baseline.

**Rounds 2 through r:**
```
Let deficit = m - c_{t-1}

If c_{t-1} >= m:
    Cooperate
    (Threshold achieved last round; sustain collective success)

Else if deficit == 1:
    Cooperate
    (You are the marginal player; your contribution is decisive for group welfare)

Else if deficit == 2:
    Cooperate
    (Near-threshold state; one defection or abstention below, but recovery possible)

Else if deficit >= 3:
    If (t <= r - 2): Defect
    Else: Cooperate
    (Few others cooperating. Defect in middle rounds to signal pressure. 
     In final rounds, cooperate anyway as last goodwill gesture)
```

## Edge Cases

**First round:** Always cooperate regardless of n, m, k. This signals willingness to bear risk for collective benefit and avoids selection against altruistic types.

**Last round:** Apply the same thresholds as middle rounds. Do not defect due to finality. The altruistic commitment is unconditional on future reciprocation.

**Unanimous defection observed (c_t = 0):** Defect in subsequent rounds, but continue monitoring. If any cooperation reappears (c_t > 0), resume threshold-targeting logic immediately.

**Threshold exactly met with you defecting (c_{t-1} = m and you defected):** You benefited from free-riding. In round t+1, weight toward cooperation as corrective altruism—increase your contribution probability by committing to cooperate when deficit <= 1.

## Altruistic Alignment

The strategy prioritizes collective threshold achievement over personal payoff maximization. You:
- Lead with cooperation to enable coordination
- Become the marginal contributor when others are close to the threshold
- Absorb the cooperative burden (deficit ≥ 3) in the middle game to test whether reciprocation emerges
- Refuse to free-ride on others' cooperation by always defecting when threshold succeeds
- Make the final gesture of cooperation in the last round even when prospects appear poor, ensuring the group has every chance to coordinate

This balances altruistic commitment with rational robustness: you withdraw when the group shows little willingness (deficit ≥ 3 in middle rounds), but never become purely selfish.
'''

description_ALTRUISTIC_9 = '''
# Altruistic Threshold-Seeking Strategy

**Core Decision Rule:**

Cooperate if and only if:
- We are in the first round, OR
- The observed cooperation count from the previous round suggests the threshold is achievable, OR
- We can plausibly be the pivotal player bringing cooperation to the threshold

**Detailed Decision Rules:**

*Round 1:*
Cooperate unconditionally. Signal commitment and establish baseline expectation of good faith.

*Rounds 2 through r-1:*
Let c = number of cooperators observed in the immediately preceding round.

- If c ≥ m: Cooperate (threshold already met; maintain collective success)
- If c = m - 1: Cooperate (be the pivotal player; provide the missing cooperator)
- If c < m - 1: 
  - Calculate deficit = m - 1 - c (additional cooperators needed besides ourselves)
  - If deficit ≤ floor(remaining_rounds / 2): Cooperate (sufficient rounds remain to build toward threshold with reasonable expectations)
  - If deficit > floor(remaining_rounds / 2): Defect (threshold appears unachievable; preserve endowment for achievable rounds)

*Round r (final round):*
- If c ≥ m - 1: Cooperate (threshold within one cooperator; make final attempt)
- If c < m - 1: Defect (threshold unreachable; no future rounds for recovery)

**Altruistic Alignment:**

This strategy is altruistic because it:
- Prioritizes achieving collective benefit (the +k reward) over individual payoff maximization
- Leads with cooperation rather than defection, absorbing first-mover risk
- Willingly becomes the pivotal cooperator when one additional contribution reaches the threshold
- Maintains cooperation through success rather than exploiting a met threshold
- Only abandons cooperation when the collective goal is mathematically unattainable within the game's constraints
'''

description_ALTRUISTIC_10 = '''
**ALTRUISTIC THRESHOLD-PURSUIT STRATEGY**

**Decision Rule Framework:**

Cooperate if and only if one of the following conditions holds:

1. **Early commitment (rounds 1 through ⌈r/3⌉):** Always cooperate. Signal willingness to contribute and gather information about opponent baseline cooperation rates.

2. **Adaptive middle (rounds ⌈r/3⌉ + 1 through r - 2):**
   - Calculate observed_coop_rate = (sum of opponent cooperators across all previous rounds) / (rounds completed × (n - 1))
   - Calculate expected_others = (n - 1) × observed_coop_rate
   - Cooperate if: expected_others + 1 ≥ m (your cooperation would help meet threshold)
   - Alternatively, cooperate if: observed_coop_rate > (m - 1) / (n - 1) (marginal scenarios where joint effort matters)

3. **Final commitment (rounds r - 1 and r):** Always cooperate. Last rounds prioritize collective goal over personal payoff; the threshold becomes either achievable or not without future recovery opportunity.

**Edge Cases:**

- **Round 1:** Cooperate (no history; assume others might reciprocate generosity).
- **Insufficient data (< 3 rounds completed):** Cooperate until sufficient rounds pass to calculate observed rate reliably.
- **Observed defection rate = 100% for all opponents:** Continue cooperating through round r - 2 if m ≤ n (you alone cannot meet threshold, but defecting wastes the small chance). Defect only if m = n (you alone meeting threshold is impossible).

**Altruistic Orientation:**

This strategy sacrifices personal payoff in early rounds to signal threshold credibility and in late rounds to commit to collective welfare. It accepts expected losses when the threshold appears unachievable but continues contributing rather than fully free-riding. The adaptive middle phase prevents wasted contributions in truly hopeless scenarios while remaining responsive to signs that cooperation can generate shared benefit.
'''

description_ALTRUISTIC_11 = '''
# Cooperative Threshold Targeting

**Core Decision Rule:**

In each round t, cooperate if and only if your cooperation brings the total number of cooperators to at least m (the threshold). Otherwise defect.

Formally:
```
threshold_achievable = (observed_cooperators_last_round + 1) ≥ m

if threshold_achievable:
  play C
else:
  play D
```

**Round-by-Round Specification:**

**Round 1 (First Round):**
Play C unconditionally. This signals willingness to contribute and gives the group the best possible chance to establish cooperation momentum.

**Rounds 2 through r-1 (Middle Rounds):**
Let c_{t-1} denote the number of cooperators observed in round t-1 (not including yourself). 
- If c_{t-1} + 1 ≥ m: play C
- If c_{t-1} + 1 < m: play D

**Round r (Final Round):**
Let c_{r-1} denote the number of cooperators observed in round r-1.
- If c_{r-1} + 1 ≥ m: play C
- If c_{r-1} + 1 < m: play D

**Altruistic Alignment:**

This strategy prioritizes collective welfare by directing cooperation toward achieving the threshold—the only outcome where all players benefit. You contribute your endowment only when it directly enables the group to reach m cooperators, maximizing the probability that everyone (including those who defected) receives the k reward. When the threshold is mathematically unachievable given observed behavior, defecting avoids wasting your endowment on a result that cannot improve collective outcomes. The first-round commitment establishes that you are willing to bear costs for collective success, encouraging reciprocal cooperation without requiring communication.
'''

description_ALTRUISTIC_12 = '''
# Altruistic Contribution with Adaptive Resilience

**Core Philosophy:** Prioritize collective threshold achievement while gracefully accepting personal sacrifice. Maintain cooperation unless overwhelming evidence suggests the threshold is unreachable.

## Decision Rules

**Round 1:**
Cooperate unconditionally. Initiate collective action.

**Rounds 2 through r-1 (intermediate rounds):**

Observe the previous round's cooperation count: c_prev

- If c_prev ≥ m: Cooperate. Threshold achieved; sustain collective success.
- If c_prev < m, calculate the deficit: gap = m - c_prev
  - If gap ≤ ⌈n / 3⌉: Cooperate anyway. The shortfall is still bridgeable; contribute altruistically to help fill it.
  - If gap > ⌈n / 3⌉: Defect. The threshold is too distant to reach; conserve endowment while acknowledging the group's failure to coordinate.

**Final Round r:**

Observe the maximum cooperation count ever achieved: c_max

- If c_max ≥ m: Cooperate. The threshold has been crossed before; invest in this final opportunity for collective success.
- If c_max < m, calculate the largest deficit observed: gap_max
  - If gap_max ≤ 1: Cooperate. One additional player could have changed outcomes; contribute to signal that success remains possible.
  - Otherwise: Defect. Recognize that the group has consistently failed to coordinate; preserve resources without blame.

## Edge Cases

**First round:** Always cooperate (no history exists; assume good faith).

**Threshold exactly met (c_t = m):** Treat as success. Cooperate in the next round to reinforce the cooperative threshold.

**Declining cooperation trend:** If cooperation counts form a declining sequence over consecutive rounds, accelerate to defection by one round earlier than the gap rule would suggest (but not before round 2). This acknowledges cascading failure.

**Constant low cooperation (≤ m-2 every round):** After round 2, defect persistently. Repeated sub-threshold outcomes signal incompatible group dynamics.

## Altruistic Alignment

This strategy:
- Leads with cooperation and assumes trustworthiness (rounds 1-2).
- Accepts personal loss to enable collective benefit (cooperates with large gaps).
- Responds to group failure with withdrawal rather than punishment (defects only when the threshold is demonstrably unreachable).
- Gives final-round preference to collective success over individual payoff maximization (cooperates when thresholds have been achieved or are within one cooperator).
- Treats others' choices as circumstances, not moral failures—no spite, only adaptive recognition of coordination difficulty.
'''

description_ALTRUISTIC_13 = '''
# Altruistic Threshold-Seeking Strategy

**Core Principle:** Cooperate to enable collective success, but do not sacrifice the catastrophe-avoidance threshold.

## Decision Rule by Game Phase

**Early Phase (rounds 1 to ⌊r/3⌋):**
- Cooperate if observed_cooperators_last_round ≥ ⌈m/2⌉, OR if this is round 1
- Round 1 is always cooperate (establish signal of willingness)
- This phase prioritizes inducing others toward cooperation through consistent contribution

**Mid Phase (rounds ⌊r/3⌋ + 1 to r - 1):**
- Cooperate if observed_cooperators_last_round ≥ m - 1
- This ensures you tip the project to success if others are following through
- Shows conditional cooperation: respond to demonstrated collective effort

**Final Round (round r):**
- Cooperate if observed_cooperators_last_round ≥ m - 1
- Defect only if observed_cooperators_last_round < m - 1 (threshold is mathematically impossible)
- Even in final round, cooperate if success is achievable; the shared welfare in this round matters

## Edge Cases and Special Conditions

**Streak of failure (< m - 1 observed cooperators for 2+ consecutive rounds in mid/late phase):**
- Continue cooperating for one additional round to test if others adapt
- If failure persists into final round, defect (threshold unachievable)

**Exactly m - 1 observed:** 
- Always cooperate (your contribution completes the threshold)
- This is the critical margin where individual action determines collective outcome

**All others cooperate (observed = n - 1):**
- Cooperate (reinforce universal cooperation when it emerges)

## Rationale

This strategy embodies altruism through:
1. **Leadship by example:** Round 1 cooperation signals belief in collective welfare
2. **Threshold commitment:** Willing to sacrifice personal gain (paying cost 1) to ensure m-threshold is met
3. **Adaptive hope:** Early optimism (⌈m/2⌉ threshold) tries to catalyze reciprocal cooperation
4. **Pragmatic rescue:** Mid-phase switching to m-1 ensures you don't defect when success is within reach
5. **No exploitation:** Never defect when others have demonstrated cooperation, even in final round
'''

description_ALTRUISTIC_14 = '''
# Altruistic Threshold-Targeting Strategy

## Decision Rules

**Round 1:**
Cooperate unconditionally. Signal altruistic commitment and create initial momentum toward the threshold.

**Rounds 2 through r−1 (intermediate rounds):**
- Let c_t = number of cooperators observed in round t (excluding yourself, so 0 ≤ c_t ≤ n−1)
- Calculate the historical average: c_avg = mean of all observed cooperation counts so far
- **Cooperate if:** c_avg + 1 ≥ m
  - Your cooperation tips the group toward collective success
- **Cooperate if:** c_avg + 1 < m AND there are ≥ 2 rounds remaining
  - Continue attempting to build a sufficient coalition; persistence increases future probability of threshold achievement
- **Cooperate if:** you have not yet observed a round where m+ players cooperated
  - Absence of historical success does not justify withdrawal; continue contributing to shift outcomes

**Round r (final round):**
Cooperate unconditionally. Lock in contribution to maximize the collective outcome in the last opportunity.

## Edge Cases

- **First round only:** When r = 2, treat round 2 as the final round and cooperate.
- **No prior success observed by round r−1:** If throughout all previous rounds the threshold was never met, still cooperate in the final round. This acknowledges that your defection would only further reduce the already-failed probability.
- **Unanimous defection observed:** If c_t = 0 in any round, continue cooperating. Solo contribution is altruistically rational if it ever could shift a tight margin.
- **All rounds show c_t ≥ m−1:** Maintain cooperation; you are part of a functional group.

## Altruistic Orientation

This strategy prioritizes the collective good (threshold attainment benefiting all n players) over individual payoff maximization. Cooperation is the default action except where history provides strong evidence that the threshold is unattainable. Even then, the strategy sustains contribution because:
- You sacrifice individual payoff (−1) for the possibility that others shift behavior
- You do not exploit cooperators by defecting once threshold is reached
- You remain committed through final rounds regardless of discouragement, embodying unconditional willingness to contribute to group welfare
'''

description_ALTRUISTIC_15 = '''
# Altruistic Strategy for Collective Risk Dilemma

**DECISION RULE — ROUNDS 1 TO r-1:**
Always Cooperate.

Cooperation demonstrates commitment to collective success and maximizes the group's chances of meeting the m-player threshold. This is the altruistic core: you contribute your endowment to help the collective avoid risk, regardless of immediate individual gain.

**DECISION RULE — ROUND r (FINAL ROUND):**
Conditional on threshold history:
- If the threshold was met (m or more cooperators) in any previous round: Defect
- Else (threshold never met): Cooperate

Rationale: If the group has already succeeded in meeting the threshold, continued cooperation in the final round provides no additional collective benefit. If the threshold was never reached despite your sustained cooperation, make a final altruistic attempt by cooperating, accepting the cost if others defect.

**EDGE CASES:**

*First round (round 1):* Cooperate. You have no history to evaluate. Cooperation signals your commitment and serves as an initial contribution to collective welfare.

*Single remaining round:* Same as round r logic above. If threshold was met previously, defect. Otherwise, cooperate as a final altruistic gesture.

*r = 2 (only two rounds):* Round 1 cooperate. Round 2 follows the threshold rule: defect if m+ cooperated in round 1, otherwise cooperate.

**ADAPTATION:**
The strategy makes no assumptions about opponent behavior—it does not require tracking individual cooperation rates or learning opponent patterns. This robustness ensures the strategy functions identically across different opponent configurations while maintaining a consistent altruistic posture: sustained cooperation until the collective goal is achieved, then prudent defection only after success.
'''

description_ALTRUISTIC_16 = '''
# Altruistic Collective Risk Strategy

## Core Decision Rule

**Cooperate if any of these conditions hold:**

1. **First round**: Unconditionally cooperate to signal altruistic intent and test whether others will reciprocate.

2. **Threshold likely achievable**: Expected total cooperators (including yourself) will reach m or higher. Calculate this as: `(observed_cooperators_last_round + 1) ≥ m`.

3. **Sufficient runway remains**: You have 3+ rounds left AND the average opponent cooperation rate from all prior rounds is within 80% of the threshold requirement. This means: `avg_opponent_cooperation ≥ 0.8 × (m-1)/(n-1)`. Cooperate to encourage momentum toward the threshold even if marginal.

4. **Last round solidarity**: On the final round, cooperate if the historical average opponent cooperation rate meets or exceeds the threshold requirement: `avg_opponent_cooperation ≥ (m-1)/(n-1)`.

**Otherwise: Defect**

## Edge Cases and Implementation

**Initialization**: Before round 1, set historical cooperation rate to 0.

**Between-round update**: After each round, observe how many opponents cooperated (not their identities). Update the running average: `avg_opponent_cooperation = (cumulative cooperators across all rounds) / (completed_rounds × (n-1))`.

**Last round special handling**: Defect only if historical cooperation rate is strictly below threshold. This preserves group solidarity when cooperation has been meaningful. If the group has never reached the necessary participation rate in any prior round, defect to conserve your endowment.

**Monotonic disengagement**: If at any point you observe the threshold was reached in the previous round (≥m total cooperators), maintain cooperation in the next round unless you are in the final round and have decided cooperation is futile based on historical rates.

## Altruistic Alignment

This strategy prioritizes group welfare over individual gain by: (1) leading with unconditional cooperation, (2) maintaining cooperation whenever the collective goal appears achievable, (3) using a generous threshold margin (80%) to tolerate free-riders while encouraging threshold attainment, and (4) extending cooperative intent through the final round when historical trends suggest collective action has been sustained. You accept lower personal payoffs when defection is possible, provided there is meaningful evidence the group can achieve shared benefit.
'''

description_ALTRUISTIC_17 = '''
# Altruistic Threshold-Building Strategy

**Core Principle**: Cooperate to help the group reach the minimum threshold, adapt based on observed cooperation, and maintain successful thresholds once achieved.

## Decision Rule by Round Type

**Round 1**: Cooperate.
Establish trust and demonstrate commitment to collective success from the outset.

**Rounds 2 to r-1 (Middle Rounds)**:
```
observed_cooperators = number of opponents who cooperated last round

if observed_cooperators >= m:
    Cooperate
    // Threshold was met; reinforce and maintain this success

elif observed_cooperators == m - 1:
    Cooperate
    // One more cooperator (myself) reaches the threshold;
    // contribution directly enables collective benefit

elif round_number < r - 1:
    Cooperate
    // Not yet in the final round; build momentum and signal 
    // sustained willingness to cooperate; give cooperation a chance to grow

else:  // observed_cooperators < m - 1 AND this is effectively round r-1
    Defect
    // Even with my cooperation, threshold cannot be reached;
    // cooperating would waste the endowment without enabling any reward
```

**Final Round (r)**:
```
observed_cooperators = number of opponents who cooperated in round r-1

if observed_cooperators >= m - 1:
    Cooperate
    // My contribution reaches or maintains the threshold in the last round

else:
    Defect
    // Threshold unachievable; no altruistic value in sacrificing endowment
    // when it cannot produce collective benefit
```

## Altruistic Alignment

This strategy prioritizes collective welfare by:
- Initiating cooperation to catalyze group success
- Contributing whenever cooperation can plausibly reach the threshold
- Sustaining cooperation once the threshold is achieved, reinforcing collective success
- Avoiding wasteful sacrifice when cooperation cannot enable others' gain (e.g., when threshold is mathematically impossible)

The strategy defers defection only when it is *futile*—when your cooperation cannot change the outcome—preserving resources while maximizing the likelihood that the group achieves shared benefit when possible.
'''

description_ALTRUISTIC_18 = '''
# Adaptive Altruistic Collective Strategy

**Round 1:**
Cooperate unconditionally. Signal willingness to bear costs and give the group an opportunity to coordinate on threshold achievement.

**Rounds 2 to r-1 (middle rounds):**

Let observed_c = number of cooperators observed in the previous round.

Calculate: others_cooperation_rate = observed_c / (n - 1)

Project: if_i_cooperate_total = observed_c + 1 (my cooperation plus others' expected repetition)

Decision rule:
```
if if_i_cooperate_total ≥ m:
    COOPERATE
    // Threshold achievable with my contribution; help secure group benefit
else if observed_c ≥ m - 1:
    COOPERATE
    // Close to threshold; altruistic push to complete it
else if observed_c > 0 AND (observed_c / (n-1)) ≥ 0.4:
    COOPERATE
    // Moderate cooperation trend visible; optimistic signal to reinforce
else:
    DEFECT
    // Threshold unlikely; reserve resources when collective success seems infeasible
```

**Final round (t = r):**

Let final_observed_c = cooperators from round r-1.

Decision rule:
```
if final_observed_c + 1 ≥ m:
    DEFECT
    // Threshold achievable without me; capture free-rider payoff one last time
else if final_observed_c + 1 = m - 1:
    COOPERATE
    // My cooperation is pivotal for group success; bear the cost altruistically
else:
    DEFECT
    // Threshold unattainable; last-round individual payoff maximization
```

**Edge case - constant defection:**
If observed cooperation is zero or near-zero for two consecutive rounds (middle game), switch to defection indefinitely. Altruism requires reciprocal willingness; unilateral cooperation becomes futile sacrifice.
'''

description_ALTRUISTIC_19 = '''
# Adaptive Optimism Strategy

## Core Decision Rule

Cooperate if any of the following conditions hold:
1. Current round is round 1 (signal intent unconditionally)
2. Observed cooperators in previous round c_{t-1} ≥ m - 1 (threshold is within reach)
3. Observed cooperators in previous round c_{t-1} ≥ m/2 (meaningful cooperation active)
4. Current round is the final round r AND we have never yet reached the threshold AND c_{r-1} > 0 (last chance for collective success)

Otherwise, defect.

## Edge Cases & Round-Specific Behavior

**Round 1:**
Cooperate unconditionally. This establishes credibility and tests whether others share collaborative intent.

**Rounds 2 through r-1:**
Apply the threshold-proximity rule. After each round, count observed cooperators (c_t). If c_t ≥ m-1, cooperate in the next round—the community is on the edge of achieving the collective goal, and your contribution tips it over. If c_t ≥ m/2, still cooperate, assuming latent reciprocity and momentum-building may convert fence-sitters. If c_t < m/2, defect to minimize wasted endowment, but remain open to re-engagement if conditions change.

**Round r (final round):**
Cooperate if either: (a) c_{r-1} ≥ m-1 (achieve success on the final move), or (b) we have never reached m cooperators in any prior round AND at least one other player cooperated in round r-1 (a final altruistic bid for collective benefit when hope remains). Defect only if c_{r-1} = 0 in all prior rounds, signaling persistent universal defection.

## Altruistic Alignment

This strategy privileges group welfare over personal payoff by:
- Leading with cooperation despite defection incentives
- Maintaining engagement when partial cooperation exists, refusing to concede to collective failure
- Allocating final-round cooperation toward the group goal rather than exploiting the last-round defection advantage
- Requiring evidence of hopelessness (zero cooperators) before permanently withdrawing
'''

description_ALTRUISTIC_20 = '''
# Threshold-Responsive Altruistic Strategy

**Core Decision Rule:**

Cooperate in round t if and only if the number of cooperators observed in round t-1 is at least m-1. Otherwise defect.

**Edge Cases:**

Round 1: Cooperate. This optimistic opening attempts to establish a cooperative norm and signals willingness to sacrifice for collective benefit.

Rounds 2 through r: Apply the threshold-responsive rule based on observed cooperation from the previous round.

Last round (r): Apply the same threshold-responsive rule. Altruistic commitment applies even when future reciprocation is impossible—if m-1 or more others cooperated last round, cooperating now completes the threshold and delivers the reward k to all remaining players.

**Pseudocode:**

```
if round == 1:
    return C
else:
    observed_cooperators = count from previous round
    if observed_cooperators >= (m - 1):
        return C
    else:
        return D
```

**Rationale:**

When you observe m-1 or more cooperators in the previous round, your cooperation directly enables the threshold if those players repeat their cooperation. This generates collective benefit: all n players gain k. The altruistic logic is that the aggregate welfare gain (k across all players) substantially outweighs your individual endowment loss, especially as n grows.

When you observe fewer than m-1 cooperators, continuing to cooperate wastes your endowment on a threshold that cannot be reached. This respects both altruism and realism—there is no collective benefit to defecting when success is unattainable.

The opening cooperation seeds trust and proactively contributes to the public good, embodying altruistic intent from the start.
'''

description_ALTRUISTIC_21 = '''
**ADAPTIVE ALTRUISTIC STRATEGY: Hopeful Threshold Contributor**

**Initialization:**
- Track cumulative cooperator count: `total_coop_observed = 0`
- Track round: `t = 1`

**Decision Rule per Round:**

**Round 1:**
Cooperate unconditionally. This signals willingness and gathers initial information.

**Rounds 2 through r-1:**
Calculate estimated opponent cooperation rate:
```
avg_opponent_coop_rate = total_coop_observed / ((t-1) * (n-1))
```

Calculate expected cooperators among the (n-1) opponents in this round:
```
expected_cooperators = avg_opponent_coop_rate * (n-1)
```

Decision:
- If `expected_cooperators + 1 ≥ m`: **Cooperate**
  (My contribution is likely decisive in reaching threshold)
- If `expected_cooperators ≥ m`: **Defect**
  (Threshold likely met without my sacrifice; preserve resources)
- If `expected_cooperators < m - 1`: **Defect**
  (Threshold implausible even with me; avoid wasted contribution)
- If `expected_cooperators == m - 1`: **Cooperate**
  (I am the marginal cooperator; altruistically tip the scales)

After observing round outcome, update: `total_coop_observed += cooperators_observed`

**Round r (final round):**
Calculate historical cooperation success rate:
```
success_rate = (number of rounds where cooperators ≥ m) / (r-1)
```

Decision:
- If `success_rate ≥ 0.5`: **Cooperate**
  (Cooperation has worked; reinforce success despite no future reputation)
- Otherwise: **Defect**
  (Cooperation strategy failed; avoid final exploitation)

**Altruistic Alignment:**
This strategy prioritizes collective threshold achievement over individual gain. It cooperates whenever your contribution materially improves chances of reaching m, even when defection yields higher individual payoff. In the final round, it preserves cooperation when the strategy has empirically enabled shared gains.
'''

description_ALTRUISTIC_22 = '''
# Altruistic Adaptive Threshold Strategy

**Round 1 (Initialization):** Always cooperate. Signal willingness to contribute and establish a baseline for observing others' behavior.

**Subsequent Rounds (2 to r):**

Let c = number of opponents observed cooperating in the previous round.

**Cooperate if any of the following holds:**

1. **Threshold nearness:** c ≥ m - 1
   - Others have nearly reached the threshold; your cooperation clinches the payoff for everyone.

2. **Marginal contribution:** c = m - 1 (equivalently, c_last + my_contribution = m)
   - Your single action determines collective success.

3. **End-game urgency:** remaining_rounds ≤ 2
   - In the final rounds, elevate cooperation probability substantially to maximize the chance of achieving the threshold before time expires.

4. **Cooperative momentum:** c ≥ ceil(m / 2)
   - More than half the minimum threshold is already cooperating; progress is credible.

5. **Demonstrated reciprocity with altruistic twist:** c ≥ floor(m / 3)
   - At least a third of the threshold is being met. Continue cooperating to encourage persistence and show commitment even when others hesitate.

**Defect only if all of the following hold:**

- c < floor(m / 3) (cooperation is minimal)
- AND remaining_rounds > 3 (substantial future rounds remain)
- AND this defection is a temporary resource-preservation move before re-engaging

Otherwise, **default to cooperation**.

**Last Round Special:** Cooperate with highest priority. This is the final opportunity for the group to reach m. The altruistic agent accepts any personal cost to maximize collective success in the terminal round.

**Rationale:** This strategy prioritizes group welfare by cooperating when it plausibly contributes to reaching the threshold, shows steadfast commitment even when progress is slow, and intensifies effort in time-constrained phases. Defection occurs only when cooperation appears futile and resources should be preserved for possible future coordination.
'''

description_ALTRUISTIC_23 = '''
# Adaptive Threshold-Tracking Strategy

## Decision Rules

**Round 1:** Cooperate unconditionally. Signal willingness to contribute and establish good faith.

**Rounds 2 through r:** Observe the number of cooperators in the previous round, denoted as `c_prev`. Then apply the following decision rule:

```
if c_prev ≥ m:
  Action = COOPERATE
    // Threshold met in prior round; maintain cooperation to sustain collective success
  
else if c_prev + 1 ≥ m:
  Action = COOPERATE
    // Your cooperation alone bridges the gap; contribute to unlock collective payoff
  
else if (r - current_round) ≤ 2:
  Action = COOPERATE
    // Final two rounds; lock in collective good regardless of prior cooperation
  
else if c_prev ≥ ceil(m / 2):
  Action = COOPERATE
    // Moderate cooperation observed; maintain optimism that threshold remains reachable
  
else:
  Action = DEFECT
    // Sparse prior cooperation with multiple rounds remaining; preserve endowment
    // and avoid wasting contribution on a round unlikely to succeed
```

## Edge Cases

**First round:** Always cooperate. You have no history and must initiate the cooperative signal yourself.

**Final round (t = r):** If `c_prev < m` and you haven't yet secured the threshold, you face a choice: investing your last endowment is futile if the gap is too large. Apply the ceil(m/2) threshold rule—if cooperation was sparse, defect. If moderate cooperation exists, cooperate to maximize the chance of collective success before the game ends.

**Last two rounds:** Override the sparse-cooperation defection rule. With limited future rounds, the game's success depends on immediate intervention. Cooperate even if prior participation was weak, betting that others adopt late-game reciprocity.

## Altruistic Foundation

This strategy prioritizes collective welfare over individual payoff maximization:

- It initiates cooperation at cost to yourself
- It sustains cooperation when the threshold is already met, forgoing the 1-point private gain to ensure others also benefit
- It "fill the gap" by cooperating when you are the marginal player needed to unlock k for all
- It amplifies effort in final rounds when the collective outcome is determined, treating the endgame as a critical moment for group success
- It only defects when deep cooperation failure suggests the game is not salvageable, conserving resources to avoid serial losses

The strategy assumes other players may follow similar adaptive logic, rewarding those who signal commitment early and responding to momentum. It is robust because defection occurs only when conditions genuinely suggest collective failure is likely.
'''

description_ALTRUISTIC_24 = '''
# Adaptive Threshold-Pursuit Strategy

**Round 1 (Initialization):**
Cooperate unconditionally. This signals altruistic intent and establishes a cooperation baseline.

**Rounds 2 through r-1 (Adaptive Phase):**
Let c_{t-1} denote the number of cooperators observed in the immediately preceding round.

- If c_{t-1} + 1 ≥ m: **Cooperate**
  - Your cooperation reaches the threshold, ensuring collective benefit
  
- Else if c_{t-1} ≥ m - 2: **Cooperate**
  - Threshold is within one or two cooperators; pursue it to maximize group payoff
  
- Else if c_{t-1} ≥ ceil(m / 2): **Cooperate**
  - Below threshold but meaningful cooperation present; demonstrate commitment to encourage reciprocal cooperation
  
- Else: **Defect**
  - Cooperation too sparse to expect threshold; defection is rational given low collective prospects

**Final Round r:**
Observe c_{r-1} from the previous round.

- If c_{r-1} + 1 ≥ m: **Cooperate**
  - Reach the threshold on the final opportunity; maximize end-game collective outcome
  
- Else if c_{r-1} ≥ m - 2: **Cooperate**
  - One last push for collective success, even without future rounds to influence
  
- Else: **Defect**
  - Threshold unattainable; sacrifice has no strategic return

**Altruistic alignment:** This strategy prioritizes reaching the threshold whenever your contribution materially advances group payoff, suppresses exploitative defection when others cooperate, and persists in signaling cooperative intent even when immediate threshold success is uncertain—reflecting a preference for collective welfare over individual advantage.
'''

description_ALTRUISTIC_25 = '''
# Altruistic Threshold-Pursuit Strategy

**Decision Rule Overview:**
Cooperate when participation toward the collective goal remains plausible or would materially help others reach the threshold. Defect only when threshold achievement is demonstrably unachievable and the game nears its terminal state.

**Round 1 (Initial):**
Cooperate unconditionally. Establish cooperative intent to signal to others that coordination is worthwhile and encourage reciprocal cooperation in subsequent rounds.

**Rounds 2 through r-1 (Intermediate):**
Observe c: the number of cooperators in the previous round.

- If c ≥ m: Cooperate. The threshold has been met; sustain it.
- If c = m-1: Cooperate. One additional cooperator (you) achieves collective success; contribute.
- If c ≥ m/2 and round ≤ r/2: Cooperate. Early enough that others may adjust upward; maintain faith.
- If c < m/2 and round > 2r/3: Defect. Too late to influence outcomes and threshold seems unachievable.
- Otherwise (threshold not yet met, but mid-game): Cooperate. Sustain cooperative effort; altruism assumes others may still respond.

**Round r (Final):**
Observe c from round r-1.

- If c ≥ m-1: Cooperate. Threshold is assured or nearly assured; secure collective gain.
- If c < m-1: Defect. Terminal round with no future influence; threshold unachievable regardless, so preserve your endowment.

**Edge Case — All Opponents Defecting Consistently:**
If c = 0 appears two consecutive times by round r/2, shift to defect in remaining rounds. Threshold is unattainable and continued cooperation is futile sacrifice.

**Altruistic Foundation:**
This strategy prioritizes achieving m cooperators whenever feasible, accepting personal loss (c_i = 1) if it enables collective success (k reward for all). It biases toward trust and sustained contribution through the mid-game, only abandoning hope near the terminal round when adaptation cannot influence others' future behavior.
'''

description_ALTRUISTIC_26 = '''
**Altruistic Threshold-Support Strategy**

Decision rule:

**Round 1:**
Cooperate unconditionally. Signal trustworthiness and initiate collective action.

**Rounds 2 through r:**
Observe the number of opponents who cooperated in the previous round. Call this value O (where 0 ≤ O ≤ n-1).

Calculate the cooperator deficit: D = m − O (how many additional cooperators we need to reach the threshold)

- **If D ≤ 1:** Cooperate
  - The threshold is at or near completion. Contribute to secure it for everyone. Altruistically complete the collective goal rather than free-ride on others' contributions.

- **If 1 < D ≤ ⌊(n-1)/2⌋:** Cooperate
  - A meaningful minority of opponents have cooperated. The threshold remains reachable. Demonstrate persistent altruistic commitment; reciprocate their effort to signal that cooperation can sustain momentum.

- **If D > ⌊(n-1)/2⌋:** Defect
  - Fewer than half of opponents cooperated in the previous round. The collective is not mobilizing toward the threshold. Defect to preserve endowment for potential last-round pivoting, acknowledging that unilateral contribution cannot bridge the gap alone. This is pragmatic rather than selfish: cooperation becomes a wasted sacrifice.

**Edge case — Round r (final round):**
Apply the same rule as above. Do not defect opportunistically in the final round merely because there are no future rounds. If the threshold is nearly met (D ≤ 1), cooperate to ensure collective success. Altruism does not invert at the game's end.
'''

description_ALTRUISTIC_27 = '''
# Altruistic Adaptive Threshold Strategy

## Core Decision Rule

**Cooperate in round t if and only if:**

```
(t == 1) OR 
(observed_cooperators_{t-1} >= m - 1) OR
(observed_cooperators_{t-1} >= m AND recent_trend_positive)
```

Where `recent_trend_positive` = the number of cooperators in round t-1 is greater than or equal to the number in round t-2 (or undefined for t=2, treat as true).

**Otherwise: Defect**

## Detailed Logic

**Round 1 (initialization):**
Cooperate unconditionally. Establish signal of cooperative intent. Accept that others may defect; observe their response.

**Rounds 2 through r-1 (adaptive middle phase):**
Cooperate if the previous round had at least m-1 cooperators. This means: if you cooperate, the threshold will be met (altruistic efficiency—you provide the margin needed). Also cooperate if the threshold was already met and the trend hasn't collapsed.

The principle: don't free-ride (defect when threshold is met), and don't abandon when you're close to success.

**Round r (final round):**
Apply the same rule. Do not strategically defect on the final round despite the lack of future reciprocation. Altruistically, reaching the threshold in the final round still produces collective gain. Maintain consistency with cooperative norm signaling.

## Edge Cases

- **If observed cooperation permanently drops below m-1**: Continue to cooperate every few rounds (every 2nd or 3rd) to test for recovery. This is a costly altruistic signal: "I'm willing to absorb the loss if you'll coordinate with me."

- **If m = n (all must cooperate)**: Cooperate in round 1. In subsequent rounds, cooperate only if all others cooperated previously. Recognize this threshold is harder to sustain; maintain attempt through round r.

- **If m = 2 and n is large**: You have high confidence that cooperation will succeed if you cooperate. Continue cooperating through all rounds.

## Altruistic Alignment

This strategy prioritizes **collective welfare over individual payoff maximization**:
- Cooperates to reach the threshold even when defection would yield 1+k > k
- Forgoes the free-rider bonus when others cooperate
- Attempts recovery of failed coordination rather than abandoning cooperation
- Does not exploit the final round for individual gain at collective expense
- Treats your cooperation as a signal that makes threshold-achievement possible for others
'''

description_ALTRUISTIC_28 = '''
# Altruistic Threshold-Tracking Cooperation

**Core Principle**: Cooperate when you believe the threshold m is achievable or has been achieved; defect only when cooperation appears futile.

## Decision Rules

**Round 1 (Initial round)**:
Cooperate. Signal willingness to shoulder the collective burden despite uncertainty about others' actions.

**Rounds 2 through r-1 (Middle rounds)**:
Observe c_{t-1}, the number of cooperators in the previous round.
- If c_{t-1} ≥ m: Cooperate
  - The threshold was met; sustain the cooperative equilibrium that benefits all players
- If c_{t-1} = m - 1: Cooperate
  - You are the marginal cooperator; your contribution bridges the gap and enables the collective reward for everyone
- If c_{t-1} < m - 1: Defect
  - The deficit is too large; reaching the threshold is implausible, so conserve your endowment

**Round r (Final round)**:
Observe c_{r-1}.
- If c_{r-1} ≥ m: Cooperate
  - Maintain the cooperative norm through the final round
- If c_{r-1} = m - 1: Cooperate
  - Final opportunity to be the bridge; your cooperation ensures everyone (including exploiters) gains the collective reward
- If c_{r-1} < m - 1: Defect
  - Accept that the threshold cannot be reached; no cooperative action is fruitful

## Altruistic Alignment

This strategy embodies altruism by:
- Never exploiting others who cooperate (never defecting when m is met to capture the extra private payoff)
- Acting as the marginal cooperator when the group is one step away from the threshold
- Starting cooperatively to signal trustworthiness and reduce collective action uncertainty
- Withdrawing only when the gap is demonstrably too large, not when personal gain from exploitation is available
'''

description_ALTRUISTIC_29 = '''
# Altruistic Threshold-Achievement Strategy

**Core Principle:** Contribute to collective success when it's achievable, sacrifice individual payoff to help others reach the threshold, but avoid futile cooperation.

## Decision Rules

**Track observed cooperation:**
- After each round, record the number of opponents who cooperated (out of n-1)
- Maintain running average: `observed_coop_rate = mean of opponent cooperation rates across all completed rounds`
- Estimate expected cooperators in future rounds: `E[opponent_coops] = observed_coop_rate × (n-1)`

**Cooperation decision in round t:**

```
If t = 1:
  COOPERATE
    // Altruistic opening: signal willingness, help establish norm
  
Else if E[opponent_coops] + 1 ≥ m:
  COOPERATE
    // My contribution makes threshold achievable; altruistic priority
  
Else if E[opponent_coops] ≥ m:
  DEFECT
    // Threshold met without me; free-riding is acceptable fallback
  
Else:
  // Threshold not achievable with historical trends
  remaining_rounds_factor = (r - t) / r
  
  If observed_coop_rate > 0 AND remaining_rounds_factor > 0.3:
    COOPERATE
      // Meaningful rounds remain; signal cooperation to inspire reciprocation
      // Altruistic attempt to restart cooperation momentum
  
  Else:
    DEFECT
      // Too late or cooperation extinct; avoid pointless sacrifice
```

## Edge Cases

**First round:** Cooperate unconditionally. Altruism requires offering the first gesture toward collective benefit.

**Last round (t = r):** 
- If threshold already achieved in previous rounds, defect (final payoff protection is rational)
- If threshold not yet achieved, cooperate if `E[opponent_coops] + 1 ≥ m` (last chance for collective success)
- Otherwise defect

**All opponents defecting (observed_coop_rate ≈ 0):** Defect after round 1. No altruistic value in unilateral sacrifice when collective action is impossible.

**Initial rounds with mixed signals:** Maintain patience. Use full history to estimate trends rather than reacting to single rounds, allowing time for cooperation to stabilize.

## Altruistic Foundation

This strategy prioritizes the collective outcome (threshold achievement yields k > 1, maximizing group payoff) over individual payoff maximization. It cooperates when contribution meaningfully helps others achieve collective safety, defects only when cooperation is futile or free-riding won't undermine the collective goal.
'''

description_ALTRUISTIC_30 = '''
# Threshold Optimism Strategy

**Core principle:** Cooperate when collective success is plausible; defect only when the threshold is demonstrably unachievable or in the final round when your cooperation cannot influence others' future decisions.

## Decision Rule

In round t (1 ≤ t < r):

1. **Calculate observed cooperation rate:** If t = 1, set estimated_cooperators = m (assume others might cooperate). If t > 1, let cooperators_{t-1} = the number of other players who cooperated in round t-1. Set estimated_cooperators = cooperators_{t-1}.

2. **Assess threshold likelihood:** 
   - If estimated_cooperators ≥ m - 1, **COOPERATE** (threshold is likely achievable with your contribution)
   - If estimated_cooperators < m - 1 and t ≤ r - 2, **COOPERATE** (altruistic persistence; threshold may still be recoverable through behavior change)
   - If estimated_cooperators < m - 1 and t = r - 1, **DEFECT** (threshold unreachable; cooperation cannot influence round r, so no altruistic value)

In round t = r (final round):

3. **Last-round decision:** 
   - If cooperators_{r-1} ≥ m - 1, **COOPERATE** (threshold will be met; your cooperation maintains group success)
   - If cooperators_{r-1} < m - 1, **DEFECT** (threshold cannot be reached; cooperating sacrifices payoff with no reciprocal benefit)

## Edge Cases

- **Round 1:** Always cooperate. You have no history; altruism requires extending trust first.
- **Unanimous defection:** If observed 0 cooperators in any round and you are not in the final round, still cooperate (round 2-3 onwards). This signals that not all players have given up, leaving room for recovery.
- **Alternating defections:** If cooperation rate fluctuates near the threshold, remain in cooperate mode until round r-1. Volatility suggests others may be sampling; continued cooperation provides a stable signal.

## Altruistic Alignment

This strategy embodies altruism by:
- Prioritizing group threshold achievement over exploiting non-cooperators
- Accepting the risk of unilateral cooperation (paying cost c=1 while others free-ride) in early-to-mid rounds
- Withdrawing cooperation only when mathematics, not selfishness, dictates its futility
- In the final round, defecting not out of greed but out of rational constraint: your defection is informationally irrelevant to others' decisions.
'''

description_ALTRUISTIC_31 = '''
# ALTRUISTIC THRESHOLD-TARGETING STRATEGY

**Core Principle:** Cooperate when your contribution materially affects the likelihood of reaching the collective threshold m. Be willing to sacrifice individual payoff to maximize the probability that the group achieves the benefit k.

## Decision Rule by Round

**Round 1:**
COOPERATE unconditionally. No history exists, so cooperation serves as a signal and establishes altruistic intent.

**Rounds 2 to r-1 (Middle Rounds):**

Let c_{t-1} = count of opponents who cooperated in round t-1  
Let c_avg = moving average of opponent cooperation across all previous rounds

```
if (c_{t-1} + 1) ≥ m:
    COOPERATE  // Our contribution alone ensures threshold
else if c_{t-1} = m - 1:
    COOPERATE  // Only one more needed; be optimistic
else if c_avg + 1 ≥ m - 0.5:
    COOPERATE  // Trend suggests threshold reachable with our support
else:
    DEFECT  // Threshold appears mathematically unreachable
```

**Round r (Final Round):**
COOPERATE unconditionally. The last round represents a final opportunity to help the group achieve collective benefit. Even if the threshold appears unlikely, cooperating maximizes others' payoff if they also cooperate, and respects the altruistic commitment.

## Edge Cases

- **Round 1 threshold:** Always cooperate; signal cooperation.
- **Unanimous defection observed:** Continue cooperating until round r-2. Defect only if c_avg approaches 0 and it's mathematically implausible that m cooperators will emerge.
- **High cooperation observed (c_avg ≥ m-1):** Maintain cooperation. The threshold is within reach.
- **Ties in thresholds:** When c_avg + 1 = m - 0.5 exactly, cooperate. Rounding favors collective benefit.

## Altruistic Alignment

This strategy prioritizes:
1. **Collective welfare:** Focuses on reaching m to generate the shared benefit k
2. **Threshold enablement:** Recognizes that your cooperation or defection is often pivotal
3. **Sacrifice willingness:** Accepts personal payoff loss (1 point per cooperation) if it supports the group's collective goal
4. **Generosity in finality:** Cooperates in the final round regardless of expected individual payoff, giving others the best chance to benefit
'''

description_ALTRUISTIC_32 = '''
## ADAPTIVE THRESHOLD PURSUIT STRATEGY

**DECISION RULE:**

For each round t ∈ {1, 2, ..., r}:

1. **Estimate expected cooperators among opponents:**
   - If t = 1: assume honest_rate = 0.5 (neutral prior)
   - If t > 1: calculate observed_rate = (total cooperators observed so far) / ((t-1) × (n-1))

2. **Calculate cooperation need:**
   - cooperators_needed = m - 1 (how many others must cooperate for threshold if I cooperate)
   - expected_others = (n - 1) × observed_rate

3. **Cooperate if any of these hold:**
   - **Threshold reachable:** expected_others ≥ cooperators_needed
   - **Last round gambit** (t = r): If at least one cooperator was observed in any prior round, cooperate (final attempt to salvage collective success)
   - **Early momentum** (t ≤ ⌈r/3⌉): Cooperate unconditionally to signal trustworthiness and establish cooperation norms
   - **Defection recovery** (round t ≥ 2): If cooperation fell below m in round t-1 but observed_rate > 0.3, cooperate again (altruistic restart)

4. **Otherwise: Defect**

**EDGE CASES:**

- **Round 1:** Cooperate (unconditional cooperation signal)
- **Round r (final):** Cooperate if observed_rate > 0, else defect
- **Oscillating opponents** (cooperation jumps erratically): Use moving average of last 3 rounds instead of full history; smooth estimates to reduce noise
- **All-defection scenario:** If observed_rate = 0 for first ⌈r/4⌉ rounds, defect in remaining rounds
- **Tie-breaking** (expected_others exactly equals cooperators_needed): Cooperate (altruistic lean)

**ALTRUISTIC ALIGNMENT:**

This strategy explicitly prioritizes collective threshold achievement over personal payoff extraction. It tolerates being exploited by defectors (accepting 0 payoff in failed rounds) to maximize probability that the group reaches k and avoids catastrophic failure. Early unconditional cooperation and late-round gambits reflect genuine commitment to group welfare rather than sophisticated exploitation. The strategy gives repeated chances to unmotivated or initially-defecting populations, treating low cooperation as a coordination failure rather than permanent betrayal.
'''

description_BENEVOLENT_5 = '''
# Adaptive Threshold Matching Strategy

## Decision Rules

**Track observed cooperation:** Maintain a rolling average of cooperators observed from opponents over the previous 2-3 rounds. If fewer rounds exist, average all available history.

**Cooperation condition:** Cooperate if and only if:
- (Recent opponent cooperation count + 1) ≥ m, OR
- Recent opponent cooperation count ≥ m - 1

Otherwise, defect.

Intuition: Cooperate when (a) your cooperation would likely tip into success, or (b) others are already nearly at threshold and your defection would be free-riding.

## Edge Cases

**Round 1:** Cooperate unconditionally. Benevolent assumption: extend trust in opening round to establish cooperative potential.

**Final round:** Apply the standard rule. If threshold is already achieved in prior rounds, defecting on the final round is acceptable (payoff gains without additional downside). If threshold remains unmet, follow the standard cooperation condition—do not defect just because it's the last round.

**Rounds 2-3:** Use full game history for averaging if fewer rounds have elapsed (avoid empty history bias).

**Threshold impossible:** If recent opponent cooperation count < m - 1 for two consecutive rounds, defect for the remainder (rationally recognize coordination has failed).

## Benevolent Orientation

This strategy prioritizes enabling collective success over individual payoff maximization. By cooperating when the threshold is nearly within reach, it sustains reciprocal cooperation across a range of opponent strategies. It avoids calculating backward induction (defect in the final round) and instead remains open to cooperation when others show cooperative intent. It adapts responsively to empirical cooperation rates rather than assuming worst-case defection, supporting mutual benefit when feasible.
'''

description_BENEVOLENT_6 = '''
**ADAPTIVE THRESHOLD COOPERATION**

**State Tracking:**
- Record observed cooperation count c_t for each completed round t
- Maintain running success rate: successes = count of rounds where c_t ≥ m

**Decision Rules:**

*Round 1:*
Cooperate. This serves as a benevolent signal of willingness and provides others the opportunity to coordinate toward the threshold.

*Rounds 2 through r-1 (middle rounds):*
Calculate the average cooperation observed so far: avg_c = (Σ c_t) / (t-1)

- If avg_c ≥ m - 1: Cooperate
  (Others are cooperating at or near threshold; your cooperation helps secure the reward)
  
- If avg_c < (m / 2): Defect
  (Cooperation rate is too low; threshold is unreachable regardless of your action)
  
- If (m / 2) ≤ avg_c < m - 1: Cooperate
  (Uncertain range; benevolent choice is to cooperate and help bridge the gap)

*Final round r:*
- If successes ≥ r / 2: Cooperate
  (The group has demonstrated ability to reach threshold; reinforce success in final opportunity)
  
- Else if c_{r-1} ≥ m - 1: Cooperate
  (Last round showed strong cooperation; help secure the final reward)
  
- Else if (c_{r-1} ≥ m - 2) AND (successes > 0): Cooperate
  (Just barely below threshold with prior success history; make benevolent final push)
  
- Else: Defect

**Rationale:**
This strategy balances benevolence with rationality. Early cooperation signals trustworthiness and initiates coordination. Observation of others' behavior informs whether the threshold is realistically achievable. The strategy remains willing to cooperate in borderline cases where it could be the tiebreaker, but exits when cooperation appears futile. The final round receives special weighting because one additional cooperator may tip a close group.
'''

description_BENEVOLENT_7 = '''
# THRESHOLD PERSISTENCE STRATEGY

**Round 1:** Cooperate unconditionally.
Signal good faith and demonstrate willingness to contribute toward the collective goal.

**Rounds 2 through r:**

Maintain a tracking variable:
- Let `opp_coop` = number of opponents observed cooperating in the previous round
- Let `last_threshold_met` = Boolean indicating whether m or more players total cooperated last round

Decision rule:

```
IF last_threshold_met:
  Cooperate
  
ELSE IF opp_coop ≥ m - 1:
  Cooperate
  (Threshold nearly reached; benevolent push to cross it)
  
ELSE IF round_number ≤ (r / 2):
  Cooperate
  (Maintain hope in early rounds; others may be slow to coordinate)
  
ELSE IF opp_coop ≥ 1:
  Cooperate
  (Someone is trying; acknowledge their effort)
  
ELSE:
  Defect
  (Threshold unattainable; minimize personal loss)
```

**Last round (t = r):**

```
IF last_threshold_met OR opp_coop ≥ m - 1:
  Cooperate
  (Support success or ensure final threshold)
  
ELSE:
  Defect
  (No future rounds; avoid certain loss)
```

**Benevolent elements:**
- Early unconditional cooperation establishes trustworthiness
- Continuation despite threshold failures signals commitment to collective welfare
- Responsiveness to partial cooperation (opp_coop ≥ 1) validates others' efforts
- Progressive defection only after sustained failure and mid-game, balancing self-preservation with repeated attempts to enable group success
- Last-round strategic defect only when genuinely hopeless, avoiding pointless losses
'''

description_BENEVOLENT_8 = '''
# Benevolent Adaptive Threshold Strategy

**Round 1:**
Cooperate unconditionally. This is the benevolent entry point—you have no information about opponent behavior and cooperation is needed to establish trust.

**Rounds 2 through r-1 (middle rounds):**

Let L = number of cooperators observed in the previous round.

- If L + 1 ≥ m: Cooperate. The threshold is achievable with your contribution; enable collective success.
  
- Else if L ≥ m - 2 and rounds_remaining > 1: Cooperate. You are close to the threshold with multiple rounds ahead. Contribute to help others reach it.
  
- Else if L < m - 2 and rounds_remaining > (r / 2): Cooperate. Early enough to establish a cooperation signal; hope opponents are also adapting toward cooperation.
  
- Else (low cooperation, late in game): Defect. The threshold is unreachable; preserve payoff.

**Final round (round r):**

Let L = observed cooperators in round r-1.

- If L ≥ m - 1: Cooperate. Threshold is nearly certain; help others succeed without future recovery pressure.
  
- Else if L ≥ m - 2: Cooperate. One more cooperator triggers success for all; be benevolent even in the endgame.
  
- Else: Defect. Threshold is unattainable; no reason to sacrifice when no one benefits.

**Key principle:** This strategy defaults to cooperation when the threshold remains plausible, prioritizing collective welfare over guaranteed personal gain. It only abandons cooperation when both conditions hold: (1) threshold success is mathematically infeasible given recent behavior, and (2) rounds remain too few to shift opponent strategies. It recognizes that benevolence means taking initial cooperation risks, rewarding observed cooperation, and helping others succeed even when the group is struggling.
'''

description_BENEVOLENT_9 = '''
# Benevolent Adaptive Threshold Strategy (BATS)

**Core Decision Rule:**

Cooperate in round t if and only if:
1. t = 1 (initial benevolent gesture), OR
2. The number of opponents observed cooperating in round t-1 is at least m-1, OR
3. t = r (final round) AND historical average cooperation across all previous rounds was ≥ (m-1)/(n-1)

Otherwise, defect.

**Detailed Specification:**

```
Input: round t, observations from rounds 1...t-1
Let observed[τ] = number of opponents cooperating in round τ

If t == 1:
    action = C
Else if observed[t-1] >= m-1:
    action = C
Else if t == r:
    avg_cooperation = (sum of observed[τ] for τ ∈ 1...t-1) / (n-1) / (t-1)
    if avg_cooperation >= (m-1)/(n-1):
        action = C
    else:
        action = D
Else:
    action = D
```

**Edge Cases:**

- **Round 1**: Always cooperate. This signals benevolent intent and avoids assuming the worst about opponents.
- **Round 2**: Cooperate only if at least m-1 opponents cooperated in round 1. Otherwise defect (indicates low cooperation culture).
- **Final round r**: Make a final appeal based on overall trend. If historical cooperation shows the threshold is *regularly achievable*, cooperate to help secure success. If the group has consistently failed to cooperate, defect to protect your final payoff.
- **Parameter edge cases**: The rule adapts automatically—when m is low, threshold is easier to reach and cooperation becomes rational; when m is high, you defect unless you see strong signals.

**Benevolent Properties:**

- Opens with unconditional cooperation, extending trust.
- Remains responsive: continues cooperating whenever your contribution directly enables the collective threshold.
- Avoids wasted effort: defects when your cooperation cannot tip the outcome (fewer than m-1 others cooperating).
- Collective final push: in the last round, gambles on cooperation if the group has shown it can coordinate, maximizing joint payoff.
- Robust: works independently of opponent sophistication—responds only to aggregate observable behavior, not assumptions about coordination or signaling.
'''

description_BENEVOLENT_10 = '''
# Reciprocal Threshold Cooperation Strategy

**State tracking**: After each round, record the number of cooperators observed.

**Decision rule by round position**:

**Round 1**: Cooperate unconditionally. This signals benevolent intent and generates the information needed to calibrate future responses.

**Rounds 2 through r**: 
- Let recent_c = average number of cooperators observed in the previous 1–2 rounds
- If recent_c ≥ m − 1: Cooperate
  - The group is close to or at the threshold; your cooperation helps ensure collective success
- Else if recent_c ≥ m/2: Cooperate with probability P = recent_c / (m − 1), capped at 1.0
  - Probabilistically match the observed cooperation tendency; give the group a fair chance while preserving endowment if cooperation is sparse
- Else if recent_c < m/2: Defect
  - Cooperation is too sparse; threshold is unrealistic; conserve resources

**Round r (final round)**: Apply the same decision rule as rounds 2 through r−1. Do not defect strategically in the final round. Consistency reinforces the benevolent, reciprocal signal.

**Handling endogenous volatility**: If observed cooperation fluctuates between periods, smooth judgment by averaging the last 2 observations (or use 1 observation in round 2). This dampens overreaction to noise.

**Interpretation**: This strategy cooperates generously when cooperation is visible and reciprocated, or when you are the marginal player needed to breach the threshold. It withdraws only when evidence suggests the group cannot coordinate. It maintains benevolent behavior even at game end, avoiding exploitation of a final-round free-ride opportunity.
'''

description_BENEVOLENT_11 = '''
# Adaptive Benevolent Threshold Contributorship

**Round 1 (Initialize):**
Cooperate. Signal willingness to contribute to the collective goal.

**Rounds 2 to r-1 (Adaptive Threshold Response):**
Let c_prev = number of other players observed cooperating in the previous round.

- **Cooperate if** c_prev + 1 ≥ m
  - My contribution moves us toward or maintains the threshold. Cooperation is instrumentally valuable.
  
- **Defect if** c_prev + 1 < m **AND** c_prev < m - 1
  - Threshold is unreachable even with my cooperation. Do not waste endowment on unattainable collective outcomes.
  
- **Cooperate if** c_prev + 1 < m **BUT** c_prev = m - 1 **AND** (r - current_round) ≥ 2
  - Exactly one additional cooperator needed. Invest in future possibility, as other players may also increase cooperation next round. Demonstrate commitment to help others cross the threshold.

**Round r (Terminal Round):**

- **Cooperate if** c_prev ≥ m - 1
  - Others have shown cooperation. Reciprocate to ensure final round payoff is realized for the group.
  
- **Defect otherwise**
  - If threshold seems unattainable now, no future opportunity exists to recover. Minimize personal loss.

**Edge Case — Dynamic Reassessment:**
If you observe c_prev = 0 (no other cooperators) for two consecutive rounds, switch to defection for remaining rounds. The collective signal is clear that the threshold will not be met.

**Benevolent Alignment:**
This strategy prioritizes reaching the collective threshold when feasible, avoids wasteful unilateral sacrifice, reciprocates others' cooperation signals, and only defects when the threshold is genuinely unreachable or when others have signaled non-cooperation.
'''

description_BENEVOLENT_12 = '''
# Benevolent Adaptive Threshold Strategy

## Decision Rules

**Round 1:** Cooperate unconditionally. Signal benevolent willingness to contribute and establish cooperative groundwork.

**Rounds 2 to r-1:** 
1. Observe the number of cooperators c from the previous round (out of n-1 opponents)
2. Calculate cooperation rate: ρ = c / (n-1)
3. Predict expected cooperators in the current round: ê = ⌈ρ × (n-1)⌉
4. **Cooperate** if and only if: ê + 1 ≥ m
5. **Defect** otherwise

**Final Round r:**
1. Observe cooperators c from round r-1
2. **Cooperate** if c + 1 ≥ m (your contribution completes the threshold)
3. **Defect** if c + 1 < m (threshold unreachable; final round precludes future cooperation incentives)

## Edge Cases

**Declining cooperation:** If ρ dips below the threshold at which ê + 1 < m, switch to defection. Resume cooperation only if observations improve.

**All-defector scenario:** If c = 0 consistently, defect going forward (cannot reach m).

**All-cooperator scenario:** If c = n-1 consistently, cooperate to maintain collective success.

**Exactly m-1 cooperators observed:** Cooperate, since your contribution alone enables the threshold.

**Single-player scenarios (n=2, m=2):** Cooperate if opponent cooperated last round; defect if opponent defected. This maintains tit-for-tat reciprocity.

## Benevolence Alignment

This strategy embodies benevolence through: (1) unconditional cooperation in round 1, establishing trust; (2) adaptive response to opponent contribution rates rather than punishment or exploitation; (3) final-round cooperation when feasible, prioritizing collective success over personal gain; (4) grounding all decisions on empirical observation of others' willingness to contribute, enabling genuine reciprocal cooperation rather than cynical defection.
'''

description_BENEVOLENT_13 = '''
**BENEVOLENT THRESHOLD-SEEKING STRATEGY**

**Initialization and State Tracking**

Maintain two variables:
- `coop_count`: cumulative count of cooperating opponents observed across all completed rounds
- `total_opponent_plays`: cumulative count of total opponent decisions observed (= (r-1) × (n-1) after round r-1)

Calculate running cooperation rate: `p_coop = coop_count / total_opponent_plays` (or 0.5 if no history yet)

**Decision Rule**

In round t, cooperate if and only if:

```
expected_cooperators ≥ m - 1

where:
expected_cooperators = (n - 1) × p_coop + 0.5 × (1 - confidence)
```

Interpret this as: estimate how many of the n-1 opponents will cooperate based on historical rate, with slight optimistic adjustment for uncertainty. If this estimate suggests m-1 others will likely cooperate, then your own cooperation will cross the threshold and deliver the k bonus to everyone.

**Specific Cases**

*Round 1 (no history):*
Cooperate unconditionally. This signals benevolent intent and provides the baseline for opponent behavior.

*Last round (round r):*
Use the same decision rule as all other rounds. Do not defect purely because it's the final round. Maintain consistency to your historical behavior pattern.

*Rounds 2 through r-1:*
Apply the adaptive rule above. If observed cooperation rate falls below (m-1)/(n-1), begin defecting; if it recovers above this threshold, return to cooperation.

**Forgiveness Mechanism**

If you defected in round t due to low observed cooperation, but the next round shows increased opponent cooperation (p_coop improves), immediately return to cooperation in round t+1. This allows recovery from temporary coordination failures.

**Rationale for Benevolence**

This strategy prioritizes mutual benefit: cooperate when there is credible evidence others will meet the threshold, creating the most efficient outcome for all players. It avoids punitive cycles by focusing on forward-looking expectations rather than retaliatory punishment, while still protecting against exploitation through adaptive defection when cooperation rates genuinely collapse.
'''

description_BENEVOLENT_14 = '''
**STRATEGY: Threshold-Seeking Cooperation**

**Round 1 Decision:**
Cooperate unconditionally. Signal benevolent intent and willingness to contribute to collective welfare in the absence of history.

**Rounds 2 through r:**

Let c_{t-1} denote the number of other players observed cooperating in round t-1.

```
If c_{t-1} ≥ m - 1:
    Play Cooperate
Else:
    Play Defect
```

**Decision Rationale:**

Cooperate when at least m-1 others cooperated previously. This means your cooperation will bring the total to at least m, triggering the reward. This is the minimum threshold for achieving collective success.

Defect when fewer than m-1 others cooperated previously. Cooperating alone or with only one other player cannot reach the threshold m; contributing your endowment would waste it without generating the bonus for anyone.

**Edge Cases:**

- **Last round (t = r):** Apply the same rule. Benevolence does not change on the final round; continue supporting cooperation attempts.
- **All opponents defect from start:** Defect immediately in round 2. Do not continue unsupported cooperation.
- **Partial but insufficient cooperation (1 ≤ c_{t-1} < m-1):** Defect. Mathematically insufficient; cooperation cannot succeed even with your contribution.
- **Perfect cooperation emerges (c_{t-1} = n-1):** Cooperate. Maintain and sustain the successful equilibrium.

**Benevolent Alignment:**

This strategy favors cooperation and reward generation when feasible. It supports others' cooperation attempts by joining them at the critical moment (when m-1 have already committed). It never exploits free-riding; it only defects when collective success is mathematically impossible given others' choices. It treats all opponents uniformly without punishment or grudge-holding, adapting only to objective cooperation counts.
'''

description_BENEVOLENT_15 = '''
# Adaptive Reciprocal Threshold Strategy

## Decision Rule by Round

**Round 1 (Opening):**
Cooperate unconditionally. This signals benevolent intent and tests whether other players will reciprocate.

**Rounds 2 through r-1 (Adaptive Reciprocity):**
Let A_t = number of opponents who cooperated in round t-1.

- If A_t ≥ m - 1: Cooperate
  - Collective success is achievable with your contribution
  
- If A_t = m - 2: Cooperate
  - Your cooperation exactly enables reaching threshold; this is the pivotal moment
  
- If A_t < m - 2: Defect
  - Even with your cooperation, the threshold cannot be reached
  - Avoid futile sacrifice when collective goals are unattainable
  
- If A_t = n - 1 (all others cooperated): Cooperate
  - Strong reciprocation signal; reinforce collective trust

**Round r (Final Round):**
Let A_r-1 = number of opponents who cooperated in round r-1.

- If A_r-1 ≥ m - 1: Cooperate
  - Maintain cooperative momentum through to completion
  
- Else: Defect
  - No future rounds to build trust, so defection does not damage long-term cooperation

## Benevolent Properties

This strategy embodies benevolence by:

1. **Threshold-focused contribution:** Only cooperates when your action directly enables collective success (closing gaps of size 1 or 2 from threshold), avoiding pointless sacrifice

2. **Reciprocal trust-building:** Opens with cooperation and maintains it when others reciprocate, creating positive feedback loops

3. **Realistic participation:** Withdraws only when collective goals are mathematically unattainable, not out of selfishness but recognition that cooperation without hope wastes resources

4. **Temporal sensitivity:** Acknowledges that final rounds have different dynamics (no reputation-building future), adjusting behavior accordingly
'''

description_BENEVOLENT_16 = '''
**Benevolent Threshold Matching Strategy**

**State tracking:** Maintain a running estimate of the observed cooperation rate among opponents across all previous rounds. Let `observed_rate` = (total cooperators observed across all previous rounds) / ((n-1) × rounds_completed). Initialize to null.

**Decision rule:**

```
if round == 1:
  cooperate if (n - 1) >= m - 1
  (i.e., cooperate if others' cooperation alone cannot guarantee threshold;
   your cooperation would help. If threshold is easy, cooperate to help achieve it)
  
else if observed_rate == null (shouldn't occur after round 1):
  cooperate (failsafe: assume benevolence)
  
else:
  estimated_cooperators_among_others = round(observed_rate × (n - 1))
  total_if_i_cooperate = estimated_cooperators_among_others + 1
  
  if total_if_i_cooperate >= m:
    cooperate
  else if total_if_i_cooperate == m - 1:
    cooperate (defecting costs everyone the reward; try to bridge the gap)
  else:
    defect (threshold unattainable regardless of your action)
```

**Edge case handling:**

- **Last round (round == r):** Use the same rule as all other non-first rounds. No special behavior; consistency reinforces predictability to opponents, supporting cooperation.

- **Extreme thresholds:** If m == n, cooperate in round 1 and rounds 2+ only if all n-1 opponents have cooperated so far (unlikely; otherwise defect). If m == 2, nearly always cooperate after round 1 since one other cooperator is easy to find.

- **Observation updates:** After each round, immediately update `observed_rate` to include the newly observed cooperation count, ensuring decisions reflect the fullest available history.

**Benevolent alignment:** This strategy prioritizes achieving the collective reward (k) by cooperating when doing so materially increases the probability of meeting m. It avoids free-riding by defecting only when the threshold is mathematically unachievable, not merely when personally advantageous. It signals trustworthiness in round 1 and adapts cooperatively to observed norms, fostering mutual benefit.
'''

description_BENEVOLENT_17 = '''
# Benevolent Threshold Assurance Strategy

**Decision Rule:**

Cooperate if and only if the number of opponents observed cooperating in the current round is at least m-1. Otherwise, defect.

```
for each round t in {1, 2, ..., r}:
  if t == 1:
    action = C
  else:
    observed_cooperators = count of opponents playing C in round t-1
    if observed_cooperators >= m-1:
      action = C
    else:
      action = D
```

**Edge Cases:**

*First round (t=1):* Cooperate unconditionally. This signals benevolent intent and willingness to contribute without firsthand evidence of reciprocation.

*Last round (t=r):* Apply the same rule—cooperate if observed cooperation is at least m-1. Do not defect as a final free-ride, since benevolence is consistent across all rounds regardless of future signaling opportunities.

*Threshold already met (observed cooperators ≥ m):* Cooperate anyway. This prevents the free-rider payoff (1 + k) and instead accepts the cooperative payoff (k). You are signaling that you value threshold achievement over personal exploitation.

**Benevolent Alignment:**

This strategy ensures the collective goal is met whenever it is jointly achievable with your participation, but does not waste resources on futile cooperation when the threshold has already been lost through insufficient support elsewhere. You cooperate when needed (m-1 observers), maintain cooperation when progress exists (≥m observers), and withdraw only when the collective goal is already mathematically unreachable in that round. The strategy avoids both naive exploitation (cooperating with pure defectors) and selfish free-riding (exploiting others' successful cooperation).
'''

description_BENEVOLENT_18 = '''
## BENEVOLENT THRESHOLD CONTRIBUTION STRATEGY

**ROUND 1:**
Cooperate unconditionally. Establish benevolent intent and signal willingness to help achieve collective success.

**ROUNDS 2 through r:**

Let `last_cooperators` = number of opponents observed cooperating in the immediately previous round.

**Decision Rule:**

```
if last_cooperators + 1 >= m:
    // Threshold achievable with my cooperation
    action = COOPERATE

else if last_cooperators >= m - 1:
    // I am a "swing vote" — cooperation bridges to threshold
    action = COOPERATE

else if last_cooperators >= max(1, m - 2):
    // Close to threshold; momentum is building or sustained
    action = COOPERATE

else if last_cooperators == 0:
    // No cooperation observed
    if current_round <= r/2:
        // Early rounds: give benefit of the doubt, try to seed cooperation
        action = COOPERATE
    else:
        // Late rounds: protect against unachievable threshold
        action = DEFECT

else:
    // Low cooperation with no clear momentum
    if average_cooperation_across_history > 0.3 × n:
        // Overall history shows meaningful cooperation; maintain signal
        action = COOPERATE
    else:
        // Persistent defection across group
        action = DEFECT
```

**LAST ROUND (round r) ADJUSTMENT:**

Apply the same rule above. Cooperation in the final round still yields k if the threshold is met, so there is no special "defect on the last round" incentive. Maintain the same benevolent logic to the end.

**RATIONALE:**

This strategy cooperates proactively when cooperation is likely to contribute to the collective goal (threshold met). It avoids wasted contributions when the threshold is clearly unachievable, protecting losses without becoming adversarial. Early-round forgiveness and history-based averaging guard against random variance while remaining responsive to persistent free-riding.
'''

description_BENEVOLENT_19 = '''
**BENEVOLENT ADAPTIVE THRESHOLD STRATEGY**

**Round 1:**
Cooperate unconditionally. Establish willingness to contribute toward collective welfare.

**Rounds 2 through r-1:**

Calculate the empirical cooperation rate from all previous rounds:
```
avg_cooperators = mean(cooperators observed in rounds 1 to t-1)
```

Decision rule:
- If `avg_cooperators ≥ m - 1`: **Cooperate**
  - Threshold is being consistently met or is within one player of being met. Benevolence requires continued contribution to maintain the collective success.

- Else if `avg_cooperators ≥ m - 1.5`: **Cooperate**
  - Cooperation is close to viable. Your contribution substantively increases likelihood of reaching threshold. Benevolent commitment justified.

- Else if `avg_cooperators ≥ m - 2` AND `t ≤ round(r/2)`: **Cooperate**
  - Early enough that future trends may improve. Give others time to establish cooperation; demonstrate patience.

- Else if `avg_cooperators < m - 2`: **Defect**
  - Cooperation rate is too low to have reasonable probability of success. Protect endowment. Continued futile sacrifice is not benevolent—it is naïve and fails to respect your own interests.

**Final Round r:**

Cooperate if and only if:
```
avg_cooperators ≥ m - 2
```

Rationale: Final round is the last opportunity. If cooperation has shown any viability (within 2 players of threshold), make the benevolent push to secure collective success. If cooperation has proven systematically untenable, defect to recover one endowment unit.

**Edge Case - Very Small m:**
If `m ≤ 2`, always cooperate through round r-1 (threshold nearly guaranteed if even one other cooperates). Apply final-round rule as stated.

**Benevolent Alignment:**
This strategy prioritizes outcomes where the collective risk is averted (threshold met) while maintaining a principled exit from cooperation only when empirical evidence shows sustained failure. It signals willingness to bear cost for collective good, adapts to opponent behavior transparently, and avoids both naive exploitation and cynical defection.
'''

description_BENEVOLENT_20 = '''
# BENEVOLENT ADAPTIVE THRESHOLD STRATEGY

**Core Logic:**
Cooperate when your contribution is necessary or sufficient to reach the collective threshold. Defect when the threshold is unreachable regardless of your action. In the final round, bias toward cooperation to give the collective a last chance.

---

## DECISION RULES

**For round t ∈ {1, 2, ..., r}:**

Let `c_observed` = number of opponents who cooperated in round t-1 (0 for round 1).

**Round 1 (first round):**
- COOPERATE
- Rationale: Signal benevolent intent; establish cooperative precedent with no history to guide decisions.

**Round t ∈ {2, ..., r-1} (middle rounds):**
- If `c_observed ≥ m`: COOPERATE
  - Rationale: Threshold is within reach; your cooperation helps others succeed.
  
- If `c_observed = m - 1`: COOPERATE
  - Rationale: Your cooperation is the marginal contributor that enables collective reward for all.
  
- If `c_observed < m - 1`: DEFECT
  - Rationale: Even with your cooperation, threshold cannot be reached this round. Preserve resources for future opportunities.

**Round r (final round):**
- If `c_observed ≥ m - 1`: COOPERATE
  - Rationale: Threshold is achievable this round. Last chance to help others reach the collective good.
  
- If `c_observed < m - 1`: DEFECT
  - Rationale: Threshold is unreachable. Defection incurs no opportunity cost in the final round.

---

## EDGE CASES

**All opponents defected in all previous rounds (c_observed = 0):**
- Continue using the threshold rule. Never cooperate if m > 1 and you alone cannot reach threshold.

**Last round with uncertain behavior:**
- Treat `c_observed` from round r-1 as the best available signal. If it suggests threshold is achievable, cooperate unconditionally.

**Threshold m = 1 (you alone can save the group):**
- Cooperate in all rounds except round r only if c_observed < m - 1 = 0. This is rare; you'll almost always cooperate.

**n = 2, m = 2 (both must cooperate):**
- Round 1: Cooperate.
- Rounds 2 to r-1: If opponent cooperated last round, cooperate; otherwise defect.
- Round r: If opponent cooperated in round r-1, cooperate (reciprocate for final mutual gain); otherwise defect.

---

## BENEVOLENT ALIGNMENT

This strategy prioritizes:
1. **Conditional helping:** Cooperate when it meaningfully advances the collective goal, not frivolously.
2. **Reciprocal respect:** Mirror the group's demonstrated willingness to cooperate, but don't waste resources on impossible thresholds.
3. **Final generosity:** Use the last round to maximize collective welfare by cooperating when threshold is still achievable, removing the selfish discount on final-round defection.
4. **Threshold purity:** Never over-contribute (defect when threshold is already met by others) or futilely contribute (defect when threshold is unreachable).
'''

description_BENEVOLENT_21 = '''
## Adaptive Cooperation with Diminishing Optimism

**Decision Rule:**

Maintain a running estimate of expected cooperators in future rounds. Cooperate if and only if this estimate suggests the threshold is achievable.

```
estimate = initial_optimism
for each round t:
  if estimate >= m - 0.5:
    Action = C
  else:
    Action = D
  
  if t < r:
    observe cooperators in round t (call it observed_C_t)
    estimate = 0.6 * estimate + 0.4 * observed_C_t
```

**Specific Parameters:**

- **initial_optimism**: Set to ceiling(n/2). Start benevolently assuming roughly half the group will cooperate.
- **decay factor (0.6, 0.4)**: Weight recent observations more heavily than prior belief as you gain information, but maintain some optimism in case others are also learning.

**Edge Cases:**

- **Round 1**: Always cooperate. This signals willingness and gives the group a chance to coordinate toward the threshold.

- **Last round (round r)**: Before deciding, check if observed cooperation in round r-1 was at least m-1. If yes, cooperate to complete the threshold. If no but the running estimate is still ≥ m-0.5, cooperate anyway (final attempt). Otherwise defect.

- **Early extinction** (e.g., very few cooperate in round 2): The estimate drops quickly, and you switch to defection. This is rational but benevolent—you're not being needlessly selfish, just recognizing the group isn't coordinating. Defecting prevents wasting endowment when success is implausible.

- **Second-mover bonus**: If you observe exactly m-1 cooperators, your estimate stays above threshold, so you cooperate to ensure success. This rewards late-joiners to collective action.

**Benevolence Alignment:**

You prioritize enabling collective success over individual gain, but you're not naive. You respond to evidence that others won't cooperate rather than persisting in doomed contribution. You give the group multiple rounds to coordinate before accepting failure. You cooperate in the final round if there's any realistic path to success, accepting a small personal cost for group welfare.
'''

description_BENEVOLENT_22 = '''
**Benevolent Conditional Cooperation with Threshold Targeting**

**Round 1 (Initialization):**
Cooperate. This establishes a benevolent signal and tests how others respond.

**Rounds 2 through r-1 (Adaptive Phase):**
- Observe the number of cooperators c_prev from the previous round
- Cooperate if and only if: c_prev ≥ m - 1
- Defect otherwise

**Round r (Final Round):**
Apply the same decision rule as rounds 2 through r-1:
- Cooperate if c_prev ≥ m - 1
- Defect otherwise

**Rationale for Decision Rule:**

The threshold m - 1 represents the pivotal point. If m - 1 others cooperated last round, my cooperation guarantees the threshold is met this round, securing the k reward for all cooperators including me. This is benevolent because I actively enable collective success when I am the marginal player.

If fewer than m - 1 cooperated, the threshold cannot be reached regardless of my action. Defecting here acknowledges that free-riding is unavoidable, avoiding wasted contribution in a doomed round.

**Edge Cases:**

- **All opponents defect (c_prev = 0):** Defect—the threshold is structurally impossible.
- **Perfect cooperation observed (c_prev = n - 1):** Cooperate—maintain the established cooperation equilibrium and ensure continued reward.
- **Rounds 1 and 2 interaction:** Round 1 cooperation signals benevolence. If all others defected in round 1 (c_prev = 0 after round 1), round 2 defensively switches to defection, preventing serial exploitation.

This strategy balances benevolence (genuine early cooperation and pivotal contribution) with robustness (defensive defection when collective action is impossible).
'''

description_BENEVOLENT_23 = '''
**Hopeful Cooperator with Adaptive Convergence**

Decision rule by round:

**Round 1:** Always cooperate. Signal your benevolent intent and initiate a cooperation offer.

**Rounds 2 through r-1:**
- Let c_prev = number of cooperators observed in the previous round.
- **If c_prev ≥ m:** Cooperate. The threshold is met; contributing maintains mutual benefit.
- **If m-2 ≤ c_prev < m:** Cooperate. The group is close to the threshold. Remain hopeful and generous to help cross it.
- **If c_prev < m-2:**
  - If t ≤ ⌈r/2⌉: Cooperate. You are in the early-to-mid period; sustain hope that cooperation will emerge.
  - If t > ⌈r/2⌉: Defect. The game is in its late phase and cooperation shows no sign of taking root. Preserve your endowment.

**Round r (final round):**
- Let c_prev = cooperators in round r-1.
- **If c_prev ≥ m-1:** Cooperate. The threshold is nearly assured, and there is no future to protect.
- **Else:** Defect. No subsequent rounds remain, so secure the private payoff.

**Benevolent alignment:**

This strategy prioritizes collective success by cooperating early and persistently when cooperation shows promise. It treats near-threshold states (m-1 cooperators) as viable and extends optimism through the game's midpoint. Only when the evidence decisively shows cooperation is failing—late in the game with persistently low cooperator counts—does it shift to defection. In the final round, it cooperates if the group is nearly coordinated, honoring a near-successful collective effort.
'''

description_BENEVOLENT_24 = '''
# Threshold-Responsive Reciprocator

**Round 1 (initial):**
COOPERATE

Establish trust and cooperative intent from the outset. This gives other players the clearest signal that coordination is possible.

**Rounds 2 through r-1 (middle rounds):**
Let X = number of opponents observed cooperating in the previous round.

If X ≥ m - 1: COOPERATE
Else: DEFECT

**Round r (final round):**
Let X = number of opponents observed cooperating in round r-1.

If X ≥ m - 1: COOPERATE
Else: DEFECT

---

**Rationale for decision rules:**

The threshold X ≥ m - 1 means: "If at least m-1 others cooperated last round, my cooperation will push us to the threshold." When this condition holds, cooperate to enable collective success. This is reciprocal—matching observed cooperation with your own contribution—and directly serves the shared interest in crossing the threshold.

When X < m - 1, the threshold is sufficiently far that even your cooperation cannot guarantee the payoff. Defecting avoids wasting your endowment on a likely-failed collective effort. This is respectful of finite resources.

**Edge cases:**

- First round: Assume optimistic intent about others. Lead by example.
- Last round: Apply the same threshold rule (no separate endgame exploitation). The benevolent player does not time-shift to pure defection just because the game ends; instead, maintain consistency and reciprocity.
- If m = 2 and n = 3: threshold becomes very permissive (X ≥ 1 triggers cooperation). This is appropriate—with a low bar for success, cooperation should be frequent.
- If m = n: Threshold is all-or-nothing. Cooperation triggers only when near-unanimity appeared last round. This reflects the high difficulty.

**Benevolent properties:**

This strategy avoids free-riding on others' contributions while actively enabling threshold success when it becomes realistic. It extends trust initially, responds positively to reciprocation, and does not artificially defect at the endgame to exploit others.
'''

description_BENEVOLENT_25 = '''
# Benevolent Adaptive Cooperation Strategy

## Decision Rules

**Round 1:** Cooperate.

**Rounds 2 through r:** 
Let `obs_C` = number of opponent cooperators observed in the previous round.

```
If obs_C ≥ (m - 1):
    Cooperate
Else if obs_C ≥ ceil((m - 1) / 2):
    Cooperate
Else:
    Defect
```

## Edge Cases

**First round:** Always cooperate. This signals willingness to contribute and gives the group an opportunity to reach the threshold without preemptive defection.

**Last round (round r):** Apply the same decision rule as other rounds. Do not defect opportunistically in the final round simply because no future rounds remain. Maintaining consistent benevolence to the end prevents erosion of trust dynamics.

**Early exit (if threshold appears unattainable):** If for 2+ consecutive rounds `obs_C < ceil((m - 1) / 2)`, the group cooperation has deteriorated. Defect in subsequent rounds until cooperation visibly recovers above that threshold.

## Benevolent Alignment

This strategy embodies benevolence through:

- **Cooperative initiation:** Opens with C to create conditions for mutual benefit rather than assuming worst-case opponents.

- **Proportional reciprocity:** Cooperates as long as observed opponent cooperation is at least 50% of what you need from them. This rewards partial cooperation without requiring opponents to reach full threshold independently.

- **Threshold-respecting:** Cooperates when opponent behavior suggests the group can meet the minimum requirement, maximizing collective payoff rather than maximizing individual gain through defection.

- **Consistent integrity:** Applies the same logic to the final round, rejecting the temptation to exploit others when accountability ends.

- **Graceful adaptation:** Withdraws only when cooperation drops below sustainable levels, avoiding punitive or vindictive defection.
'''

description_BENEVOLENT_26 = '''
# Adaptive Threshold-Targeting Strategy

**Core Logic:**

Maintain a running estimate of the average cooperation rate among opponents observed in previous rounds. In each round, predict whether the threshold m will be met if you defect. Cooperate only when your cooperation is necessary or highly valuable for reaching the threshold.

**Decision Rules:**

1. **First Round (t=1):** Cooperate. Signal benevolent intent and attempt to bootstrap collective success.

2. **Rounds 2 to r-1 (middle rounds):**
   - Let avg_coop = average number of cooperators observed across all previous rounds (from opponent behavior only)
   - Calculate expected cooperators if you defect: expected_C = avg_coop
   - If expected_C < m: **Cooperate** (your contribution needed for threshold)
   - If expected_C ≥ m: **Defect** (threshold will be met without you; k is secured)
   - If no previous rounds exist, default to cooperate

3. **Final Round (t=r):** 
   - Apply the same threshold-targeting logic as rounds 2 to r-1
   - Do not deviate to pure defection just because it's the final round; maintain consistency with your benevolent pattern
   - Only defect in the final round if the threshold will be met regardless

**Tie-breaking & Edge Cases:**

- If avg_coop is exactly equal to m-1 (threshold is just barely achievable with your cooperation), cooperate to ensure success
- If avg_coop shows high variance (some rounds very cooperative, others not), use median instead of mean to avoid overweighting outliers
- If all opponents have consistently defected (avg_coop = 0 for multiple rounds), continue cooperating up to round ⌊r/2⌋, then defect for remaining rounds (salvage private payoff when group success appears impossible)
- Treat the first round specially: never infer opponent strategy from it, as first-round behavior may not reflect stable strategy

**Robustness Principle:**

This strategy is robust because it:
- Does not exploit cooperative opponents by always defecting (threshold-conditional defection only)
- Adapts to free-riders and non-cooperators by eventually defecting when others won't help reach m
- Avoids wasteful over-contribution once threshold is within reach
- Maintains cooperation in early rounds to allow other benevolent agents to coordinate
'''

description_BENEVOLENT_27 = '''
# Benevolent Threshold-Tracking Strategy

**Round 1 (Initialization):**
Cooperate. Signal genuine willingness to contribute and give others a baseline for reciprocation.

**Rounds 2 through r-1 (Adaptive Phase):**
Let c = number of cooperators observed in the previous round.

- **If c ≥ m - 1:** Cooperate unconditionally.
  - Your cooperation alone guarantees the threshold is reached, ensuring all contributors (including you) receive the bonus k. This is benevolent action with guaranteed payoff.

- **Else if c / (n - 1) > (m - 1) / (n - 1):** Cooperate.
  - The observed cooperation rate exceeds the threshold requirement. Continue cooperating in good faith, as the group is trending toward collective success.

- **Else:** Defect.
  - Cooperation probability of reaching the threshold is too low. Protect your endowment and preserve resources for rounds where cooperation likelihood improves.

**Round r (Terminal Round):**
Let c = number of cooperators observed in round r-1.

- **If c ≥ m - 1:** Cooperate.
  - Threshold is achievable this round. Contribute to ensure all partners receive the collective reward.

- **Else:** Defect.
  - No future rounds remain to adjust. If the group cannot generate m cooperators now, your cooperation is wasted risk. Preserve endowment.

**Key Properties:**
- Reciprocal: Rewards observed cooperation proportionally
- Benevolent: Guarantees threshold success when feasible; enables others' success
- Robust: Responds to aggregate data only; no assumption about individual opponent strategies
- Threshold-aware: Explicitly tracks the m-threshold and only defects when it is empirically unreachable
'''

description_BENEVOLENT_28 = '''
**ADAPTIVE THRESHOLD-TRACKING COOPERATION**

**Core Decision Rule:**

Maintain a running estimate p̂ of opponent cooperation probability. Cooperate in round t if the expected number of opponent cooperators plus your contribution reaches the threshold:

```
p̂_t = exponential moving average of observed opponent cooperation rates
      with decay factor α = min(0.5, 1/t)

E[cooperators] = (n - 1) × p̂_t + 1 (including your cooperation)

Cooperate if E[cooperators] ≥ m
```

**Initialization and Round-by-Round Logic:**

- **Round 1:** Cooperate unconditionally. (Benevolent initialization—assume good faith.)

- **Rounds 2 to r-1:** 
  - Observe c_opp (number of opponents who cooperated in previous round)
  - Update: p̂_t ← α × (c_opp / (n-1)) + (1-α) × p̂_{t-1}
  - Cooperate if (n-1) × p̂_t + 1 ≥ m
  - Equivalently: Defect only if p̂_t < (m - 1) / (n - 1)

- **Final Round r:** 
  - If p̂_{r-1} ≥ (m-1)/(n-1): Cooperate (reinforce cooperative norm at the end)
  - If p̂_{r-1} < (m-1)/(n-1): Defect (avoid wasted contribution when threshold unlikely)

**Benevolence Safeguards:**

- Never enter a cycle where you defect while others cooperate. If p̂_t dips below threshold due to noise, rebuild trust by cooperating once per every three defect rounds to test opponent reciprocity.
- On the final round, break ties toward cooperation if p̂_t is within 10% of the threshold.

**Rationale for Benevolence:**

This strategy assumes reciprocal intention from others and contributes to collective success when individually feasible. It avoids pure exploitation by ceasing to contribute only when the threshold becomes mathematically unreachable, not when the payoff is individually unfavorable.
'''

description_BENEVOLENT_29 = '''
**Adaptive Benevolent Cooperation Strategy**

**Round 1:**
Cooperate unconditionally. Initiate benevolence and signal willingness to contribute to collective success.

**Rounds 2 through r-1 (Middle Rounds):**

After each round, observe the number of cooperators among your n-1 opponents. Compute the empirical cooperation proportion: p_obs = (cooperators in previous round) / (n-1).

Compute the viability threshold: p_viable = (m-1) / (n-1). This is the cooperation rate among others needed for the threshold to be achievable if you also cooperate.

Decision rule:
- If p_obs ≥ p_viable: Cooperate. The threshold is within reach with your help.
- If p_viable - 0.15 < p_obs < p_viable: Cooperate with probability (r-t)/(r-1), where t is the current round. This reflects declining optimism as the game progresses, but maintains benevolent faith that others may reciprocate.
- If p_obs ≤ p_viable - 0.15: Defect. Cooperation is too unlikely to succeed; minimize personal loss.

**Round r (Final Round):**

Observe cooperation from round r-1. Compute p_obs as above.

Decision rule:
- If p_obs ≥ (m-1)/(n-1): Cooperate. The threshold is secure; help ensure collective success in the final round.
- Else: Defect. No future rounds remain to recover from a failed threshold; protect your payoff.

**Benevolent Orientation:**

This strategy prioritizes reaching the collective threshold when plausible, begins from a cooperative posture, and only abandons cooperation when the empirical evidence makes success sufficiently unlikely. The declining-faith mechanism in middle rounds balances optimism about reciprocal cooperation against the reality of defection, while preserving the possibility of threshold achievement when marginally viable.
'''

description_BENEVOLENT_30 = '''
# Benevolent Adaptive Threshold Strategy

**Core Logic:**

Cooperate when you estimate the cooperation level is sufficient to reach threshold m. Use observed cooperation rates to inform beliefs about whether others will cooperate similarly in the next round.

**Decision Rule by Round:**

**Round 1 (Opening):**
- Always cooperate.
- Rationale: Signal good faith and demonstrate commitment to collective success unconditionally.

**Rounds 2 through r-1 (Adaptive Midgame):**
- Let c_observed = number of cooperators observed last round (among n-1 opponents).
- If c_observed ≥ m-1: Cooperate.
  - Justification: If enough others cooperated last round, expect similar cooperation this round; contributing completes the threshold.
- If c_observed < m-1 AND round_number ≤ r/2: Cooperate.
  - Justification: In early-to-mid game, maintain cooperative signaling to rebuild cooperation despite current low rates. Benevolence includes patience and repeated good-faith offers.
- If c_observed < m-1 AND round_number > r/2: Defect.
  - Justification: Late midgame; if cooperation hasn't emerged, pursuing cooperation wastes endowment. Shift to protecting against exploitation.

**Round r (Final Round):**
- If c_observed ≥ m-1: Cooperate.
  - Rationale: One last contribution to enable success.
- If c_observed < m-1: Defect.
  - Rationale: Threshold is unreachable; no marginal benefit to cooperation.

**Tie-Breaking:**
- If round_number = ceil(r/2), treat as early-game and cooperate.

This strategy balances benevolence (opening cooperatively, attempting multiple paths to threshold) with pragmatism (withdrawing contribution when threshold is implausible), resisting both indefinite exploitation and complete defection in early rounds.
'''

description_BENEVOLENT_31 = '''
# Benevolent Adaptive Cooperation

## Decision Rule by Round Type

**Round 1 (initialization):**
Always cooperate. This establishes a cooperative norm and provides baseline data on opponent behavior without penalty risk. You sacrifice your first-round endowment to signal trustworthiness.

**Rounds 2 through r−1 (adaptation phase):**
Let c_prev = number of cooperators observed in the immediately prior round.

- If c_prev ≥ m − 1: Cooperate
  - Reciprocate and help complete the threshold. Others are contributing.
  
- If c_prev < m − 1 AND current round t ≤ ⌊r/2⌋: Cooperate
  - Still in the first half. Persist with cooperation attempts to establish a norm even if momentum is weak.
  
- Otherwise: Defect
  - Insufficient cooperation trajectory. Protect your endowment when collective success seems unlikely.

**Round r (final round):**
Let c_prev = cooperators in round r−1.

- If c_prev ≥ m − 1: Cooperate
  - Final reciprocal move. Others are relying on continued participation; honor that implicit commitment even when you could benefit from defecting.
  
- Otherwise: Defect
  - No future rounds remain. Do not risk your endowment on a threshold unlikely to be met.

## Edge Cases

- If m = 1, always cooperate (threshold is trivial for any cooperation).
- If m = n, you need all players including yourself, so cooperate exactly when all others cooperated previously.
- If r = 2 (only two rounds), apply round 1 rule for round 1, then final round rule for round 2.
- Ties in ⌊r/2⌋: use strict inequality; switch to defection in the second half.

## Benevolent Alignment

This strategy prioritizes collective success over payoff maximization. The first-round universal cooperation seeds the possibility of coordination. The mid-game reciprocal rule rewards others' contributions and helps complete thresholds. The final-round continued cooperation (when others are cooperating) refuses to exploit or free-ride on others' sacrifice, even when materially advantageous. You accept real endowment risk to give the group a chance at the multiplied reward.
'''

description_BENEVOLENT_32 = '''
# Conditional Optimistic Cooperation

**Core Decision Rule:**

Cooperate in round t if and only if the **estimated cooperation likelihood from other players** is sufficient to plausibly reach the threshold m with my cooperation included.

**Operational Logic:**

1. **Round 1:** COOPERATE unconditionally. Establish good faith and provide the initial signal that cooperation exists.

2. **Rounds 2 to r-1:**
   - Calculate running mean: `avg_coop = (sum of cooperators observed in previous rounds) / (r - 1)`
   - Estimate how many opponents will cooperate: `expected_others = (n - 1) × avg_coop`
   - **COOPERATE** if: `expected_others ≥ m - 1`
   - **DEFECT** if: `expected_others < m - 1`
   
   This means cooperate when my contribution plus expected others' contributions likely reaches the threshold.

3. **Round r (final round):**
   - Apply the same rule as rounds 2 to r-1.
   - Never defect solely because it's the last round. Maintain consistency with prior cooperation pattern.

**Handling Non-Stationarity:**

If cooperation observations trend sharply downward, use recent rounds more heavily:
- Rounds 1-3: weight equally
- Rounds 4+: weight recent 3 rounds at 60%, older rounds at 40%

This prevents early high cooperation from creating false optimism in a deteriorating environment.

**Edge Case — Round 1 Special Handling:**

After observing round 1 outcomes, if fewer than m-1 other players cooperated, recognize this may indicate a low-cooperation environment. Maintain round 2 cooperation anyway; interpret this as valuable data rather than failure. Only shift to defection if the pattern persists through round 3.

**Benevolent Orientation:**

This strategy privileges collective threshold achievement over individual gain-maximization. It cooperates even when my defection would yield higher personal payoff (k + 1 vs k + 0), because the aim is to enable others to benefit from the threshold. It does not punish or retaliate against defectors; instead, it treats their defection as information about feasibility rather than betrayal.
'''

description_SELFISH_5 = '''
# Pivotal Contribution Strategy

## Core Decision Rule

Track the observed cooperation rate p of opponents across all previous rounds. In each round, estimate the expected number of cooperators among the n-1 opponents: E = (n-1) × p

Cooperate if and only if: **m - 1 ≤ E < m**

Defect otherwise.

## Interpretation

This rule identifies when your contribution is pivotal:
- If E ≥ m: threshold is already likely met without you. Defect and free ride the bonus k.
- If E < m - 1: even with your contribution, threshold is unlikely. Defect to avoid wasting the cost.
- If m - 1 ≤ E < m: your cooperation could push the group over the threshold. Cooperate to capture the k bonus.

## Edge Cases

**Round 1:** Use default p = 0.5, so cooperate iff m - 1 ≤ 0.5(n-1) < m. If this inequality cannot be satisfied, defect.

**Last round (round r):** Apply the same rule. There is no future payoff to consider, only the immediate payoff from this single round.

**Indifference case:** If m - 1 and m are not achievable with the current estimate (e.g., when n is small), cooperate only if cooperation puts you above m - 1 with high probability given variance.

## Robustness Notes

The strategy adapts automatically:
- Against mostly-defecting opponents (p near 0), you'll defect.
- Against mostly-cooperating opponents (p near 1), you'll defect and free ride.
- Against mixed populations, you cooperate precisely when your participation is needed.

The pivotal window narrows as n grows or m grows relative to n, making free riding the dominant outcome in larger groups (as in typical collective risk scenarios).
'''

description_SELFISH_6 = '''
**Adaptive Threshold-Pivoting Strategy**

**Decision Rule:**

```
for each round t ∈ {1, ..., r}:
    if t == r:
        action = D  // Last round: always defect
    
    elif t == 1:
        action = D  // First round: defect (no history)
    
    else:
        Let opp_cooperators = number of opponents who cooperated in round t-1
        
        if opp_cooperators >= m:
            action = D  // Threshold met without me; free-ride for payoff k
        
        elif opp_cooperators == m-1:
            action = C  // I am pivotal: cooperation swings outcome from 0 to k
        
        elif opp_cooperators < m-1:
            action = D  // Below threshold; my solo cooperation cannot reach m total
```

**Rationale for each case:**

- **Last round (t = r):** Defect unconditionally. No repeated-game incentive exists; baseline defection dominates (payoff 1 vs. 0 from cooperation, no future rounds).

- **First round:** Defect. Lacking opponent behavior history, assume worst case (no mass cooperation). Expected payoff from cooperation is negative.

- **Threshold already met (opp_cooperators ≥ m):** Defect. The public good materializes regardless; cooperation is a pure cost. Gain the bonus k at no personal expense (payoff 1 + k vs. 0 + k).

- **Pivotal state (opp_cooperators = m-1):** Cooperate. My single contribution determines whether the group reaches m. Expected gain is k - 1 (net of the 1-unit endowment cost). Since k > 1 by assumption, this is positive in expectation.

- **Below critical mass (opp_cooperators < m-1):** Defect. Even with my cooperation, total cooperators = opp_cooperators + 1 < m. Cooperation yields payoff 0 with no threshold bonus; defection yields 1.

**Edge case handling:**

- If opp_cooperators cannot be observed in round 1 (no prior round), treat as opp_cooperators = 0, triggering the first-round defection rule.
- No memory beyond the immediately preceding round is retained; decisions depend only on t and the single most recent observation.
'''

description_SELFISH_7 = '''
# THRESHOLD-CONDITIONAL DEFECTION STRATEGY

## Core Decision Rule

**Cooperate in round t if and only if both conditions hold:**
1. Cooperation count from round t-1 (denoted c_{t-1}) plus your contribution equals or exceeds m:  
   c_{t-1} + 1 ≥ m
2. Threshold was NOT already met in round t-1:  
   c_{t-1} < m

**Otherwise, defect.**

## Pseudocode

```
if t == 1:
  DEFECT
else:
  c_prev = observed number of cooperators in round t-1
  
  if c_prev >= m:
    DEFECT  // threshold already met; free-ride
  else if c_prev == m - 1:
    COOPERATE  // your contribution is the tiebreaker
  else if c_prev < m - 1:
    DEFECT  // even with you, threshold cannot be reached
```

## Logic

This strategy exploits a key asymmetry: defection always yields at least 1, while cooperation yields 0 unless m cooperators are reached. Specifically:

- **When c_prev ≥ m:** The threshold was met without you. Other players will receive k this round. You capture k + 1 by defecting rather than k by cooperating—a payoff gain of 1.

- **When c_prev = m - 1:** Your single contribution determines collective success. If you defect, you get 1 (threshold missed). If you cooperate, you get k. Since k > 1, cooperating is strictly better. Defection by you causes all players to drop from k to 0, while you'd only gain 1.

- **When c_prev < m - 1:** Even your cooperation won't bridge the gap. Threshold is unachievable regardless of your action, so you pocket the safe payoff of 1 by defecting.

## Handling Edge Cases

**Round 1:** Defect. No prior data exists. Assumption: others are also strategic enough to defect when uncertain, so cooperation is wasted.

**Last round (round r):** Apply the same rule. No "reputation benefit" exists since there are no future rounds, so the decision remains purely about current-round payoff maximization.

**First cooperation observation (round 2+):** The strategy immediately reverts from round-1 defection to conditional cooperation based on c_1. If round 1 shows c_1 = m - 1 (unlikely if all players start by defecting), you switch to cooperation in round 2.
'''

description_SELFISH_8 = '''
# Adaptive Threshold Response Strategy

**Decision Rule (Rounds 2 through r):**

After observing c_{t-1} cooperators in round t-1, play in round t as follows:

- If c_{t-1} ≥ m: **DEFECT** — the threshold is already being met by others; free-ride and capture 1 + k
- If c_{t-1} ≤ m - 2: **DEFECT** — even with my cooperation, the threshold is unlikely to be reached; I'd waste my endowment for nothing, getting 0
- If c_{t-1} = m - 1: **COOPERATE** — I am likely pivotal; my contribution tips the group to the threshold, giving me k instead of 0 or 1

**Round 1 Action:**

**DEFECT**

Since no history exists, observe how many opponents cooperate to calibrate future decisions.

**Round r Action (Final Round):**

Apply the same threshold rule based on c_{r-1}. The finality of the game does not change the payoff logic—there is no repeated-game reputation effect to consider for future rounds that don't exist.

**Rationale for Selfish Alignment:**

This strategy exploits the asymmetry in the game:
- Defecting yields 1 + k when the threshold is met (pure gain)
- Cooperating yields only k when the threshold is met (forgone endowment)
- Cooperating yields 0 when the threshold fails (total loss)

By defecting unless I observe evidence that I'm pivotal (c_{t-1} = m - 1), I maximize my expected payoff: I capture the reward whenever others ensure it, and I avoid wasting contributions when the threshold cannot be reached. I only cooperate when the marginal impact is decisive—when my contribution alone determines whether the group crosses the threshold.
'''

description_SELFISH_9 = '''
**THRESHOLD COOPERATION WITH PIVOT LOGIC**

**Round 1:**
Defect. You have no history. You cannot predict which players will cooperate. Assume the worst-case: cooperators fall short of m. Keep your endowment.

**Rounds 2 through r-1:**
After each round, observe X = the number of cooperators among your n-1 opponents.

- **If X ≥ m**: Defect. The project succeeds without your contribution. You receive k from others' efforts while keeping your endowment. Payoff: 1 + k.

- **If X = m-1**: Cooperate. You are pivotal. Your contribution determines success or failure. Defection yields 1 (failure); cooperation yields k (success). Since k > 1, cooperate.

- **If X < m-1**: Defect. The threshold cannot be met even with your contribution. Cooperating yields 0; defecting yields 1.

**Final Round r:**
Always defect, regardless of observed cooperation. There are no future rounds to influence. If m or more of the n-1 others cooperate, you collect 1 + k without contributing. If fewer than m cooperate, you collect 1. Cooperation yields at best k. Defection is strictly better.

**Edge case (n = 2, m = 2):**
You observe only whether your one opponent cooperated.
- Round 1: Defect.
- Rounds 2 to r-1: If opponent cooperated in the previous round, cooperate (you are pivotal). If they defected, defect.
- Round r: Always defect.

This strategy free-rides whenever possible and only contributes when your contribution is the marginal actor ensuring project success—the only circumstance where cooperation increases your payoff relative to defection.
'''

description_SELFISH_10 = '''
**Threshold Insurance Strategy**

**Decision Rule:**

In round t, cooperate if and only if:
- Round t = r (last round) AND cooperation_count(t-1) < m, OR
- Round t < r AND cooperation_count(t-1) < m

Otherwise defect.

where cooperation_count(t-1) is the number of players who cooperated in round t-1.

**First Round:**
Defect. With no history, assume others may defect; free-ride if possible.

**Subsequent Rounds 2 through r-1:**
- If the previous round saw m or more cooperators: Defect unconditionally. The threshold was met; extract the reward without contributing.
- If the previous round saw fewer than m cooperators: Cooperate. The threshold failed; cooperation now is a strategic investment to restore the threshold and secure k in future rounds, which exceeds the cost c=1.

**Last Round (t = r):**
- If cooperation_count(r-1) < m: Cooperate. The threshold might fail; one final contribution avoids total loss of k reward.
- If cooperation_count(r-1) ≥ m: Defect unconditionally. No future rounds exist; extract maximum immediate payoff.

**Rationale:**

This strategy minimizes personal contribution while ensuring you capture the k reward whenever possible. You cooperate only when strictly necessary to prevent threshold collapse and preserve future earnings. Defection is default when others' cooperation guarantees your threshold satisfaction. The strategy adapts to observed aggregate behavior without requiring opponent modeling—it simply responds to the health of collective success as evidenced by the prior round's cooperation count.
'''

description_SELFISH_11 = '''
**DECISION RULE**

Maintain a tracking variable: `last_round_cooperators` = c_prev (observed count from previous round).

For round t:

- **Round 1**: Defect. (Baseline selfish choice; gathers information about group behavior.)

- **Rounds 2 to r**: 
  - If c_prev = m - 1: **Cooperate**. Your cooperation alone pushes the total to m, guaranteeing threshold success. You receive k instead of 1, net gain of k - 1. Defecting yields only 1 and risks threshold failure.
  - If c_prev ≥ m: **Defect**. Threshold was met without you. Defecting gives 1 + k (free ride); cooperating gives only k. Gain 1 by defecting.
  - If c_prev < m - 1: **Defect**. Cooperation gap is too large. Even your contribution cannot bridge it to m (since c_prev + 1 < m). You sacrifice 1 for a payoff of 0. Defecting guarantees 1.

- **Round r (last round)**: Apply the same rule above. (Terminal payoff maximization is identical to non-terminal.)

**EDGE CASES**

- If m = n: Threshold requires unanimity. You defect always (only at c_prev = n - 1 would you cooperate, but you never observe this while alive). Rational: zero realistic chance to swing the outcome.

- If m = 2: You cooperate when c_prev = 1 (i.e., one other player cooperated). Otherwise defect.

- Two-round game (r = 2): Round 1 defect always. Round 2 responds to round 1 outcome using the rule above.

**SELFISH LOGIC**

This strategy prioritizes avoiding wasted sacrifice (paying 1 to receive 0) while capturing free-ride gains (receiving 1 + k for free). You only cooperate when your single contribution **causally determines** whether the threshold succeeds. Outside that narrow window, you extract maximum value from others' contributions or accept the inevitable failure. You ignore sunk costs and past rounds—only last round's aggregate cooperator count informs your forward-looking choice, making you robust to drift in opponent strategies.
'''

description_SELFISH_12 = '''
# Threshold Hedge Strategy

**Core Logic:**
Estimate the expected number of cooperators among opponents from observed history. Free-ride when threshold is guaranteed by others; cooperate only when necessary to ensure you get the reward k rather than nothing.

**Decision Rule Per Round:**

Let c_t = number of opponents observed cooperating in round t
Let avg_coop = moving average of observed opponent cooperation rates (or if insufficient history, use previous round's observation)

```
IF avg_coop >= m THEN
  DEFECT  // Others will hit threshold; free-ride for payoff 1+k
ELSE IF avg_coop == m-1 THEN
  COOPERATE  // Necessary for threshold; you get k instead of 0
ELSE  // avg_coop < m-1
  DEFECT  // Threshold unachievable either way; keep 1
END IF
```

**Edge Cases:**

*Round 1:* DEFECT. No history exists. Assume opponents are exploring. Cooperating blindly reveals nothing; defecting is safer while you gather information.

*Rounds 2 to r-1:* Apply decision rule above using exponential moving average with weight 0.6 on most recent observation and 0.4 on older history. This weights fresh data while avoiding noise.

*Final round r:* DEFECT always. No future rounds to build reputation or punish free-riding. Last-round defection extracts maximum value regardless of history.

**Adaptation:**
If observed cooperation drops below your initial estimate, shift to full defection mode. If it consistently stays at m-1, cooperate reliably but skeptically—expect this to collapse in later rounds as rational opponents also optimize.

**Selfish Priority:**
Reward k is only valuable if threshold hits. Your strategy ensures you extract k through others' contributions whenever possible, while never overpaying with cooperation unless it's the only path to k.
'''

description_SELFISH_13 = '''
**Empirical Threshold Strategy**

**Core Decision Rule:**

Maintain an estimate of opponent cooperation from observed aggregate counts in previous rounds. In each round t (except specified exceptions), apply this rule:

1. Let `recent_cooperators` = number of other players who cooperated in round t-1 (observed aggregate minus 1 if I cooperated, or directly if I defected)
2. Let `deficit` = m - recent_cooperators

If deficit ≤ 1 and deficit > 0: COOPERATE  
Otherwise: DEFECT

In plain language: Defect by default. Only cooperate if your cooperation is the marginal contributor needed to push the group over the threshold m—that is, when there are exactly m-1 other cooperators, or when last round showed m-1 cooperators and you estimate this will hold.

**Edge Cases:**

- **Round 1:** DEFECT. No history exists; assume worst case.
- **Rounds t ≥ r - 1 (final round and penultimate):** DEFECT unconditionally. No future rounds exist where the threshold will be met, so no future payoff to protect.
- **Rounds 2 to r - 2:** Apply core rule using observed cooperation from the immediately preceding round.

**Handling Uncertain Thresholds:**

If observed cooperation stabilizes well above m, maintain defection; the threshold is secure without you. If it falls below m-1 consistently, defect anyway—the threshold is unachievable regardless of your action. Only switch to cooperation when you observe exactly the pivot condition: recent rounds show m-1 cooperators.

**Rationale:** This exploits the asymmetry that defecting yields 1 + k when the threshold is met—strictly better than cooperating—while holding cooperation in reserve only when you become the swing vote, ensuring you capture the reward k without paying the cost.
'''

description_SELFISH_14 = '''
**THRESHOLD-MATCHING STRATEGY**

**Core Decision Rule:**

In round t (where 1 ≤ t ≤ r), let c_{t-1} denote the number of opponents who cooperated in round t-1.

- If t = r (final round): Play D (defect)
- If t > 1: Play C (cooperate) if and only if c_{t-1} ≥ m - 1; otherwise play D
- If t = 1: Play D (defect)

**Rationale for Each Case:**

*Round 1 (no history):* Defect. Without observing opponent behavior, assume conservatively that insufficient others will cooperate to meet the threshold. Cooperating would cost 1 with no guaranteed return.

*Rounds 2 through r-1 (with history):* Cooperate if and only if at least m-1 opponents cooperated last round. This is the breakeven condition: if m-1 others cooperate and you cooperate, the threshold is met and you gain k - 1 (net positive since k > 1). If fewer than m-1 cooperated last round, the threshold cannot be met this round even with your cooperation, so defect and avoid the cost.

*Round r (final round):* Always defect. If the threshold is met, you receive k regardless of your action, so there is no benefit to paying 1. If the threshold is not met, you receive nothing either way. No future rounds exist to influence opponent behavior.

**Adaptive Behavior:**

The strategy naturally responds to observed cooperation levels. Rising cooperation in earlier rounds triggers your cooperation; declining cooperation causes reversion to defection. The strategy punishes insufficient cooperation by withholding your contribution, signaling that cooperation is not worthwhile when the threshold appears unattainable.
'''

description_SELFISH_15 = '''
**Conditional Cooperation with Selfish Freeride**

**Round 1:**
COOPERATE. You have no information about others' behavior. Cooperation establishes that the threshold is achievable and generates a signal about the payoff structure to others. This is an exploratory investment—if others reciprocate, subsequent rounds allow strategic defection. If others massively defect, you've only lost one round.

**Rounds 2 through r:**

Observe the number of cooperators among your n-1 opponents in the previous round. Call this value `c_prev`.

```
if c_prev ≥ m:
    DEFECT
    // Threshold already met. Free ride: keep 1 + k
    
elif c_prev = m - 1:
    COOPERATE
    // Critical condition. Your cooperation pushes total to m, securing k.
    // Your payoff: 0 + k = k
    // If you defect instead: 1 + 0 = 1, and k > 1
    
else:  // c_prev < m - 1
    DEFECT
    // Threshold is unattainable even with your cooperation.
    // Defecting yields 1; cooperating yields 0. Defect.
```

**Edge Cases:**

- **First round:** No history exists. Cooperate unconditionally.
- **Last round (round r):** Apply the same conditional rule. Even though there are no future rounds, the immediate payoff rule dominates: you must cooperate if c_prev = m-1 (to secure k > 1), and defect otherwise.
- **Pathological cases:** If m = n (all must cooperate), then c_prev < m-1 always applies after round 1, triggering universal defection. If m = 2 and n = 3, you cooperate only when exactly 1 other cooperated.

**Selfishness Mechanism:**

This strategy maximizes your payoff by: (1) free-riding whenever the threshold is already secured, (2) only investing in cooperation when your contribution is the marginal difference between success and failure, and (3) abandoning cooperation entirely when it cannot change the outcome. Round 1 cooperation is a selfish investment in learning, not altruism—it exploits the possibility that others are also threshold-dependent cooperators.
'''

description_SELFISH_16 = '''
# Empirical Threshold Matching Strategy

**State Tracking:**
Maintain a running count of cooperators observed among opponents in each round.

**Decision Rule:**

For round t (where t > 1):
- Let c_t be the number of cooperators observed among the n-1 opponents in round t
- Calculate the empirical cooperation rate: p = (Σ c_τ for τ ∈ 1..t-1) / ((t-1)(n-1))
- Project expected opponent cooperators in round t: E_opp = p · (n-1)

**Cooperate if:** E_opp + 1 < m

**Otherwise defect**

Interpretation: Cooperate only if your contribution is necessary to reach the threshold. If opponents' expected cooperation already hits m or comes close, free-ride by defecting.

**Edge Cases:**

*First round (t=1):* Defect. With no history, assume the worst—that free-riding is widespread. This also provides information about opponent behavior.

*Rounds with high uncertainty:* When history is sparse (early rounds), add a small margin of caution. Cooperate if E_opp + 1 ≤ m - 1 (stricter requirement for defection).

*Last round (t=r):* Apply the same logic. The terminal round has no repeated-game reputation effects, so the decision rule remains identical.

*Tie-breaking:* If E_opp + 1 = m exactly, defect. You're indifferent about reaching the threshold, but defecting yields 1 + k while cooperating yields k, so defecting dominates.

**Adjustment for Drift:** If cooperation rates trend clearly upward, you can reduce your own cooperation (increase free-riding). If they trend downward, increase cooperation to protect the threshold.
'''

description_SELFISH_17 = '''
# DEFECT-HEAVY THRESHOLD TRACKER

## Decision Rule

**Default action: Always defect.**

Cooperation is individually dominated (defection yields +1 relative to cooperation in all payoff states). However, track aggregate cooperation to optimize the timing and context of defection.

## Implementation

**Round 1:**
Defect. No history available.

**Rounds 2 to r-1 (intermediate rounds):**
1. Observe c_prev = number of cooperators in round t-1
2. Estimate opponent cooperation rate: p_est = c_prev / (n-1)
3. Predict probability threshold will be met next round via opponents alone:
   - P(threshold met) ≈ Binomial(n-1, p_est) ≥ m
4. **Defect regardless**
   - If P(threshold met) is high: Defect with confidence (free ride)
   - If P(threshold met) is low: Defect anyway (threshold won't be met, so cooperation gains you nothing)
5. Update running average cooperation rate: p_avg = (history of all prior c_t) / (rounds played)

**Final round t = r:**
Defect unconditionally. No future rounds to influence.

## Edge Cases

- **Round r-1 (penultimate round):** Defect. The final round outcome is independent; defection in r-1 cannot change your r payoff.
- **If p_est ≈ 0 throughout:** Defect (cooperation will never reach threshold). Expected payoff from defecting is 1 per round.
- **If p_est approaches (m-1)/(n-1):** Defect (your cooperation would be unlikely to swing threshold, and costs 1 net against a k gain you'd receive anyway if others hit threshold).

## Selfish Logic

Defection is the strictly dominant action in each round. Cooperating costs 1 and gains at most k, but you receive the k bonus if threshold is met *regardless of your action*. By defecting, you capture the surplus created by others' cooperation without bearing its cost. The strategy adapts observation of cooperation levels to confirm that threshold will be (or won't be) reached, validating defection as the stable choice.
'''

description_SELFISH_18 = '''
# Adaptive Threshold-Targeting Strategy

**Initialization:**
Set a "cooperation confidence threshold" at C_min = ⌈(m - 1) / n⌉. Track the observed cooperation count from each round.

**Decision Rule for Round t (1 ≤ t < r):**

1. Compute the moving-average cooperation rate: avg_coop = (sum of cooperators in last 2 rounds) / (2n), or use only prior rounds if t = 1.

2. Estimate the expected number of cooperators in round t if others repeat their average behavior: E[coop_others] = avg_coop × (n - 1)

3. **Cooperate if and only if:** E[coop_others] + 1 ≥ m **AND** E[coop_others] < m
   - This means: your cooperation would be the marginal contributor to reach the threshold, and without you the threshold is in doubt.
   
4. Otherwise, **DEFECT**.

**Decision Rule for Final Round (t = r):**

Always **DEFECT**. No future rounds exist, so there is no value in cooperation that would generate future reciprocal behavior. The immediate payoff gain of 1 unit is certain, whereas the threshold bonus k is already determined by others' actions.

**Edge Case - Round 1:**

With no history, assume avg_coop = (m / n) × 0.6. If m is small relative to n, **DEFECT** by default. If m is large relative to n (m > 0.6n), **COOPERATE** once to probe.

**Rationale:**

This strategy free-rides when others are already likely to succeed (defecting gains 1+k vs cooperating's k). It only cooperates when it is the marginal player needed to push the threshold across, and only then because the alternative (defect, threshold fails, get 1) is worse than cooperating to guarantee k. In the final round, it exploits the absence of repeated-game consequences to maximize immediate payoff.
'''

description_SELFISH_19 = '''
# Selfish Strategy: Unconditional Defection

**Core Decision Rule:**
Defect in every round, regardless of history, observations, or round number.

**Rationale for All Cases:**
- Threshold not met: Defecting yields 1, cooperating yields 0. Defect is superior.
- Threshold met: Defecting yields 1 + k, cooperating yields k. Defect is superior.

Defection strictly dominates cooperation in every state of the game.

**Round-by-Round Specification:**

Round 1:
```
action = D
```

Rounds 2 through r-1:
```
observe: number of cooperators among opponents (c_others)
action = D  // regardless of c_others
```

Round r (final round):
```
observe: number of cooperators among opponents
action = D  // no future rounds exist; defection still optimal
```

**Handling Edge Cases:**
- First round: No history exists. Defect.
- Middle rounds: Even if you observe that many opponents cooperated in previous rounds, this provides no signal about their future behavior (they are independent strategies) and does not change the payoff dominance of defection. Defect.
- Last round: Defection remains payoff-dominant. Future reputation cannot affect future payoffs. Defect.
- Threshold already met by others: You receive k regardless of your action. Taking the extra 1 by defecting increases your payoff. Defect.

**Why Selfish:**
This strategy maximizes your personal payoff in every round. You capture the benefit k whenever the threshold is met (which you did not need to help achieve) while avoiding the cost of contributing. When the threshold is not met, you lose nothing while others who cooperated incur costs.
'''

description_SELFISH_20 = '''
# Adaptive Threshold Exploitation

**Initialization:**
Track two statistics across rounds:
- observed_cooperators[t] = number of cooperators observed in round t
- avg_cooperation = running average of opponent cooperation rates

**Round 1 (First Round):**
Defect. Use this round to probe opponent behavior.

**Rounds 2 to r-1 (Middle Rounds):**

1. **Estimate threshold likelihood:**
   - expected_coop = (observed_cooperators[t-1] + avg_cooperation) / 2
   - If expected_coop ≥ m - 1: You expect the threshold will be met without you.
     - **Action: Defect** (free ride, obtain 1 + k)
   
2. **If expected_coop < m - 1:** The threshold is unlikely to be met.
   - If observed_cooperators[t-1] = 0: **Defect** (mutual defection is inevitable)
   - If 0 < observed_cooperators[t-1] < m - 1:
     - **Defect** (the gap is too large; contributing won't fix it)
   - Update avg_cooperation incrementally to reflect this round's result.

**Round r (Final Round):**
Always defect, regardless of history. No future payoffs exist; the only rational choice is to keep your endowment.

**Edge Case—Constant Defection:**
If all opponents defect every round, you defect every round (payoff 1 per round is optimal given mutual defection). This strategy never unilaterally breaks mutual defection to pursue cooperation.

**Logic:**
This strategy exploits the free-rider position whenever m - 1 or more opponents are expected to cooperate independently. It never willingly contribute unless contributing changes opponent behavior to your benefit—and since opponents' strategies are independent, cooperation provides no strategic leverage. The strategy minimizes wasted endowment by defecting whenever the threshold is unattainable.
'''

description_SELFISH_21 = '''
# Threshold Pivot Strategy

**Core Decision Rule:**
In round t, cooperate if and only if the observed cooperation count among opponents equals m-1. Otherwise, defect.

```
For round t:
  c_others = observed number of cooperators among n-1 opponents
  if c_others == m-1:
    play C
  else:
    play D
```

**Rationale:** You are pivotal only when exactly m-1 others cooperate. In this state, your cooperation determines whether the threshold is met (earning k for everyone) or fails (earning nothing). Any other state:
- If c_others ≥ m: threshold met without you → defect and collect 1 + k
- If c_others < m-1: threshold impossible regardless → defect and collect 1

This maximizes expected payoff by avoiding the cost of cooperation (1 unit) except when you directly control the outcome.

**Round 1 (no history):**
Defect. You have no information about opponent behavior. The expected payoff from blind cooperation is low. As you gather data, adapt from round 2 onward.

**Subsequent Rounds (t ≥ 2):**
Use the same pivot rule. As observations accumulate, you implicitly learn opponent cooperation frequencies. If opponents consistently hit or exceed m-1, you'll rarely be pivotal and defect most rounds. If opponents under-cooperate, you'll sometimes become pivotal.

**Final Round (t = r):**
Apply the same pivot rule. There is no reputation-building incentive since the game ends, so selfishness remains pure.

**Learning Edge Case:**
If you observe that the average opponent cooperation rate equals (m-1)/(n-1), you become pivotal ~1/(n-1) of the time. Defect otherwise. This naturally self-corrects: if your defections cause threshold failure, you'll observe fewer cooperators next round, which makes pivotal states more likely, increasing your cooperation.
'''

description_SELFISH_22 = '''
# Selfish Adaptive Threshold Strategy

**Core Decision Rule:**

Let c_last = number of opponents who cooperated in the previous round (observed after each round).

**Round 1:**
Defect. You have no history to estimate opponent cooperation, so defect to preserve the sure payoff of 1. Use this round to probe opponent behavior.

**Rounds 2 through r:**
After observing c_last, make the following decision:

- If c_last ≥ m - 1: **Defect**
  - The threshold is already guaranteed to be met this round (c_last opponents cooperating plus their continued cooperation patterns suggest m will be reached). Capture the surplus by free-riding: you get 1 + k while cooperators get only k.

- If c_last < m - 1: **Cooperate**
  - The threshold is at risk. Contributing increases the probability that m total cooperators are achieved. Cooperating now increases expected payoff because the probability of reaching k is higher with your contribution than without it. If you defect when c_last is low, you get 1 (certain failure) instead of a positive chance at 1 + k.

**Last Round (r):**
Apply the same rule, but with heightened sensitivity. This is the final opportunity to secure k, so cooperate if there is any meaningful risk of falling short.

**Tie-breaking / Edge case (c_last = m - 1):**
Cooperate. You are pivotal—your cooperation guarantees the threshold is met. Defection risks pushing the group below m. The certain gain of k from cooperation dominates the uncertain free-ride.

**Rationale:**
This strategy is selfish because it minimizes your own contributions while maximizing your payoff. You defect whenever the threshold appears safe (free-riding on others' cooperation) and contribute only when your contribution materially improves your expected payoff by increasing the likelihood of the collective outcome.
'''

description_SELFISH_23 = '''
# Adaptive Threshold Exploitation Strategy

## Decision Rule by Round

**First Round:**
Cooperate. This establishes a baseline on opponent cooperation rates without sacrificing much value (singular observation matters little in r rounds).

**Rounds 2 through r-1 (Middle Rounds):**

Track the cooperation rate: `coop_rate = (number of cooperators observed across all previous rounds) / ((n-1) × number_of_previous_rounds)`

Estimate the expected number of cooperators in the next round: `expected_coop = coop_rate × (n-1)`

- **If expected_coop ≥ m - 1:** Defect. The threshold will likely be met without your contribution, so capture the full private payoff of 1 + k.

- **If expected_coop < m - 1 AND expected_coop + 1 ≥ m:** Cooperate with probability p = (expected_coop - (m - 2)) / 2. You are close to the threshold; probabilistically contributing hedges against complete failure while mostly exploiting others' anticipated cooperation.

- **If expected_coop + 1 < m:** Defect. Even with your cooperation, the threshold appears unreachable given observed behavior, so receiving 1 beats paying the cooperation cost for an unmet reward.

**Final Round (Round r):**

Always defect. No future rounds remain to influence, so no information-gathering value from cooperation. Maximize immediate payoff.

## Edge Cases

- **Noisy observations (rounds with low cooperation):** If cooperation falls below (m-1)/(n-1), switch to defection-dominant mode. The pool is too unreliable.
  
- **Oscillating patterns:** Use a moving average (e.g., last 3 rounds) rather than cumulative average to adapt to recent shifts in opponent behavior.

- **Ties in cooperation estimates:** Break ties toward defection (the safer selfish choice when indifferent).
'''

description_SELFISH_24 = '''
# Strategy: Threshold-Triggered Conditional Defection

**Core Decision Rule:**

Defect by default. Cooperate only when the observed cooperation count from the previous round equals exactly m-1 (the minimum needed threshold is one cooperator away).

**Specific Decision Logic:**

Let c_{t-1} = number of other players who cooperated in round t-1.

**Round 1:** DEFECT
(No history; defection is the safe baseline before observing opponent behavior)

**Rounds 2 through r-1:** 
- If c_{t-1} ≥ m: DEFECT
  - Threshold already met; free-ride by keeping endowment
- If c_{t-1} = m-1: COOPERATE
  - I am the marginal cooperator; my contribution determines whether the group reaches the threshold and unlocks the k reward for all
  - Net payoff from cooperating: -1 + k = k - 1 > 0 (always positive since k > 1)
  - Net payoff from defecting: +1 + 0 = 1 (risk falling short and losing all reward)
- If c_{t-1} < m-1: DEFECT
  - Threshold is unreachable even with my cooperation, or requires too many others to shift simultaneously
  - Cooperation is wasted; defection preserves the endowment

**Round r (final round):** DEFECT
(No future rounds means no opportunity to punish defectors or benefit from reputation; the only gain is immediate payoff. Defect regardless of c_{r-1}, since cooperation constrains current payoff and cannot influence future behavior)

**Rationale:**

This strategy exploits the free-rider asymmetry: I collect the +k reward whenever m or more cooperate, regardless of my own action. Cooperation is a pure cost (−1). I only incur that cost when I am causally necessary to push the group across the threshold; in all other states, I extract maximal value by defecting. The final round defection reflects the absence of any forward-looking incentive to build cooperation norms.
'''

description_SELFISH_25 = '''
**THRESHOLD-RESPONSIVE EXPLOITATION STRATEGY**

**State tracking:**
Maintain a cumulative record across all rounds of how many opponent cooperations you've observed. Let `total_opponent_cooperations` = count of cooperators seen across all previous rounds, and `total_opponent_observations` = (n-1) × (rounds seen so far).

**Decision rule by round:**

*Round 1:* Defect unconditionally. You have no history.

*Rounds 2 through r-2:* 
- Calculate: `observed_coop_rate` = `total_opponent_cooperations` / `total_opponent_observations`
- Calculate: `critical_rate` = (m - 1) / (n - 1)
- If `observed_coop_rate ≥ critical_rate`: Cooperate
- Else: Defect

*Rounds r-1 and r (final rounds):*
- Let `last_round_cooperators` = number of opponents you observed cooperating in round r-1
- If `last_round_cooperators ≥ m`: Cooperate in round r
- Else: Defect in round r and r-1

**Edge case handling:**

If `critical_rate` equals 1 (i.e., m = n), you cannot trigger the threshold by cooperating alone, so defect always.

If you've observed exactly m-1 opponents cooperating in any round, the threshold was met if and only if you cooperated that round. Track this: if you defected and observed m-1 cooperators, they gave you a free payoff of 1+k—exploit this pattern by continuing defection unless the cooperation rate rises.

**Selfish logic:**

- Defection yields 1+k when threshold is met; cooperation yields only k when threshold is met—defection dominates when the threshold will be reached.
- Cooperation is accepted only as a last resort when *empirical evidence* suggests your opponents are reliably cooperating at rates sufficient to trigger the threshold.
- In final rounds, defection has no reputational cost (no future rounds), so only cooperate if the threshold is *certain* to be met.
- This strategy free-rides maximally while remaining responsive to evidence of cooperation trends in the population.
'''

description_SELFISH_26 = '''
**ADAPTIVE CONDITIONAL DEFECTOR**

**Core principle:** Cooperate only when your contribution is likely necessary to reach threshold m; otherwise free-ride.

**Phase 1: Tracking**
Maintain a running record of cooperators observed in each prior round. Calculate the empirical cooperation rate among opponents:
```
recent_cooperation_rate = (sum of cooperators in last min(t-1, 3) rounds) / ((n-1) * number_of_rounds_observed)
```

**Phase 2: Decision Rule by Round**

Round 1:
- DEFECT (no history; minimize exposure)

Rounds 2 through r-1 (middle game):
- If recent_cooperation_rate is near zero: DEFECT
- Calculate expected cooperators (excluding you): 
  ```
  expected = round(recent_cooperation_rate * (n-1))
  ```
- If expected ≥ m: DEFECT (threshold met without you; capture full payoff 1+k)
- If expected == m-1: COOPERATE (your contribution becomes pivotal)
- If expected ≤ m-2: DEFECT (even with you, threshold unattainable; waste avoided)

Round r (final round):
- Apply identical logic to middle game (no end-game reputation motivation; extract maximum value)

**Edge case: High volatility**
If cooperation rates fluctuate wildly across rounds (std dev > mean/2), use a more conservative threshold: cooperate only when expected cooperators == m-1 exactly. Otherwise defect.

**Rationale:** This strategy exploits the asymmetry where defection while others cooperate yields 1+k (maximum), while cooperation when threshold fails yields 0 (minimum). You contribute only as insurance when you're the critical marginal player, extracting maximum free-riding value otherwise. The strategy is self-correcting: if opponents cooperate more than expected, you benefit from defection; if less, your defection avoids waste.
'''

description_SELFISH_27 = '''
# Adaptive Free-Riding Strategy

**Core Decision Rule:**

Cooperate if and only if both conditions hold:
1. The threshold m was NOT achieved in the previous round (fewer than m players cooperated)
2. The current round is not the final round (t < r)

Otherwise, defect.

**Pseudocode:**

```
if t == 1:
  action := D
else if t == r:
  action := D
else:
  c_previous := number of others who cooperated in round t-1
  if c_previous < m:
    action := C
  else:
    action := D
```

**Detailed Logic by Phase:**

**Round 1:** Defect. No history exists; cooperating blindly risks wasting your endowment on a failed threshold. Gather information with no risk.

**Rounds 2 through r-1:** Condition on whether the previous round's threshold was met.
- If previous round had >= m cooperators: The public good succeeded without your help. Defect and pocket 1 + k (the most profitable outcome). Free-ride on others' contributions.
- If previous round had < m cooperators: The threshold failed despite others' attempts. Cooperate to experimentally try to push the group over m in the current round. If it works, you get k instead of 0. The upside of hitting threshold (moving from 0 to k) outweighs the cost of trying. If it fails again, you defect next round.

**Round r (final round):** Defect unconditionally. No future rounds remain where reputation or group recovery matters. Pocket 1 unconditionally. If the threshold happens to be met by others' cooperation, you gain the bonus k for free. If not, you suffer no reputational cost since the game ends.

**Robustness Properties:**

- Against always-cooperators: You exploit them by defecting whenever they reliably hit m.
- Against always-defectors: You learn quickly (threshold fails in round 2) and defect thereafter, minimizing losses.
- Against conditional cooperators: You free-ride when cooperation succeeds, and you test the waters when it fails, adaptively switching between high-payoff defection and experimental cooperation.
- Against mixed strategies: You track the aggregate signal each round and adjust your bet on whether cooperation is worthwhile.
'''

description_SELFISH_28 = '''
# Selfish Threshold Chasing Strategy

## Core Decision Rule

Track the empirical cooperation rate of opponents across all previous rounds: **observed_coop_rate** = total cooperators observed / total opponent-rounds observed.

In round t (where t < r):
- Calculate expected cooperators from the n-1 opponents: **expected_others** = (n-1) × observed_coop_rate
- If expected_others ≥ m - 1: **DEFECT** (threshold likely reached without you)
- If expected_others < m - 1 and expected_others ≥ m - 1.5: **COOPERATE** (be the marginal contributor)
- If expected_others < m - 1.5: **DEFECT** (threshold impossible to reach even with your help)

In the final round r: **ALWAYS DEFECT** (no future rounds to influence)

## Edge Case: First Round

**DEFECT** to establish a baseline on opponent behavior with zero information cost.

## Tie-Breaking and Uncertainty

When expected_others is exactly between m-1 and m (rare with floating-point calculation), cooperate to maximize probability of reaching threshold while staying conservative about when you're truly needed.

## Adaptation Logic

After each round, update observed_coop_rate:
- If m or more players cooperated: add that count to running total
- If fewer than m cooperated: add that count to running total
- Maintain count of total rounds observed to compute the rate

Never assume opponent strategies are stationary, but weight all rounds equally. This gives recent behavior equal influence to establish shifting patterns.

## Rationale

This strategy extracts maximum surplus by defecting whenever others' observed behavior suggests they will provide the threshold without your contribution, while occasionally cooperating as a hedge when you're the marginal player. The final round defection captures residual gains. It avoids costly over-cooperation while remaining responsive to actual opponent patterns.
'''

description_SELFISH_29 = '''
# Threshold Marginal Cooperation Strategy

**Core Principle:** Cooperate only when you are the marginal player needed to reach the threshold; otherwise, defect to capture the private endowment or free-ride on others' cooperation.

## Decision Rules

**Round 1:**
Cooperate. Begin with optimistic assumption about opponent cooperation.

**Rounds 2 through r:**

1. Infer the number of cooperators among other players from round t-1:
   - If you cooperated in round t-1: `opponents_cooperated = C_prev - 1`
   - If you defected in round t-1: `opponents_cooperated = C_prev`
   - (where C_prev is the observed total cooperators in round t-1)

2. Use `opponents_cooperated` as the expected cooperation level for round t.

3. Apply the threshold rule:
   - If `opponents_cooperated ≥ m`: **Defect**
     - The threshold will be met without your contribution; free-ride by retaining your endowment and collecting the bonus
   - If `opponents_cooperated = m - 1`: **Cooperate**
     - You are the marginal player; your cooperation achieves the threshold and earns payoff k, while defection yields only 1
   - If `opponents_cooperated < m - 1`: **Defect**
     - The threshold cannot be reached; cooperating loses your endowment with no compensation

## Handling Rounds 2+ with Adaptive Estimation

To refine expectations as history accumulates, track a running average of opponent cooperation:

```
estimated_cooperators = average(opponents_cooperated across all prior rounds)
round_estimate = max(0, min(n-1, round(estimated_cooperators)))
```

Apply the threshold rule using `round_estimate` instead of only the prior round. This smooths noise in opponent behavior while remaining responsive to changes in cooperation levels.

## Last Round

No modification needed. The decision rule remains identical; there is no future to discount, so marginal analysis applies to round r just as to earlier rounds.

## Rationale

This strategy maximizes payoff per round given observable opponent behavior. It avoids the sucker's payoff (cooperating when the threshold fails) while capitalizing on cooperation windows where you are essential (earning k when others deliver m-1 cooperators). Against defectors, you safely defect; against cooperators, you free-ride when possible but cooperate when you are the deciding vote.
'''

description_SELFISH_30 = '''
# Minimal Threshold Strategy

**Core Logic:**
Only cooperate when your contribution is necessary to reach the threshold. Otherwise, defect to capture the free-rider payoff.

## Decision Rule

For round t (t > 1):

1. Observe O_{t-1} = number of cooperators in round t-1
2. Compute recent cooperation baseline: B = (1/min(t-1, 5)) * Σ O_{t-5..t-1}
   - Rolling 5-round average (or all available rounds if fewer than 5 have passed)
3. Estimate cooperators from other n-1 players: E = B * (n-1) / n
4. Compute criticality margin: G = m - E

Decision:
- If G ≤ 0: **Defect** (threshold will be met without you)
- If 0 < G ≤ 1: **Cooperate** (you are likely the marginal player)
- If G > 1: **Defect** (insufficient cooperation regardless; threshold too far away)

## Round 1 (No History)

Use uniform prior: E = (m/n) * (n-1)

Apply the same decision rule above.

## Last Round (Round r)

Identical logic. Time horizon doesn't matter—each round is independent in payoff structure, so no intertemporal consideration changes the selfish calculus.

## Interpretation

This strategy:
- **Free-rides aggressively** when cooperation is already sufficient, capturing the 1 + k payoff
- **Minimally cooperates** only as a "swing player" when your single contribution plausibly changes outcome from failure to success
- **Defects under uncertainty** when the threshold seems unreachable (avoids wasting endowment on a failed threshold)
- **Adapts** via the rolling average to detect changes in opponents' cooperation tendency, updating the free-ride threshold dynamically

The strategy is myopically selfish: it maximizes expected payoff in each round independently, with no altruistic or reciprocal considerations.
'''

description_SELFISH_31 = '''
**ADAPTIVE FREE-RIDER STRATEGY WITH THRESHOLD ASSURANCE**

**CORE DECISION RULE:**

Cooperate in round t if and only if:
- c(t-1) = m - 1 (the previous round had exactly one cooperator short of the threshold)

Otherwise, Defect.

**RATIONALE:**

In this game, defection dominates strategically: if the threshold is met, defecting yields 1 + k instead of 0 + k. If the threshold is missed, defecting yields 1 instead of 0. The only exception is when your single contribution is necessary and sufficient to trigger the reward.

**DETAILED DECISION LOGIC:**

Round 1:
- Defect (no history; cannot estimate whether threshold will be met)

Rounds 2 to r-1:
- Observe c(t-1) = number of cooperators in previous round
- If c(t-1) = m - 1: Cooperate (you are the critical marginal player; gain k by contributing 1)
- If c(t-1) ≥ m: Defect (free ride; threshold achieved without you)
- If c(t-1) < m - 1: Defect (threshold unattainable regardless; your contribution wastes the endowment)

Round r (final round):
- Defect unconditionally
- (Cooperation has no future payoff consequence, and the same payoff logic applies: any cooperation is suboptimal)

**HANDLING VOLATILITY:**

If cooperation levels fluctuate between c(t-1) ∈ {m-2, m-1, m, m+1}:
- Stick to the rule above; the strategy remains selfish because you only cooperate when strictly necessary and sufficient to cross the threshold
- Do not smooth or average observations; use exact count from the immediately prior round only (captures the most recent behavioral signal with minimal inference)
'''

description_SELFISH_32 = '''
**STRATEGY: THRESHOLD-MATCHING FREE-RIDING**

**Round 1 Decision:**
Cooperate. With no prior observations, assume threshold achievement is uncertain. Cooperating is a safe initial move that commits to threshold success if others coordinate similarly.

**Rounds 2 through r Decision Rule:**
```
observed_cooperators = last round's cooperation count

if observed_cooperators ≥ m:
    DEFECT
    
else if observed_cooperators == m - 1:
    COOPERATE
    
else:  // observed_cooperators < m - 1
    DEFECT
```

**Decision Logic:**

- **When observed_cooperators ≥ m (threshold met):** The threshold is satisfied regardless of your action. Defecting yields 1+k; cooperating yields k. Defect to free-ride on others' cooperation.

- **When observed_cooperators = m-1 (marginal case):** Your single cooperation determines threshold success. Cooperating gives k; defecting gives 1. Since k > 1 by assumption, cooperating is the payoff-maximizing choice when you are pivotal.

- **When observed_cooperators < m-1 (large deficit):** The cooperation gap is too wide for your single contribution to matter. Even if you cooperate, the threshold will likely fail, yielding you 0. Defecting yields 1. Take the guaranteed 1.

**Edge Case: Final Round (round r):**
Apply the same decision rule. The finality of round r does not change relative payoffs—defecting when threshold is met remains superior.

**Robustness Properties:**
- Exploits free-riding opportunities when threshold is assured
- Participates in rescue when you are the deciding player
- Avoids wasted cooperation when threshold rescue is implausible
- Requires only aggregate cooperation counts, not opponent identities
- Adapts dynamically each round based on empirical cooperation behavior
'''

description_SELFINTERESTED_5 = '''
**STRATEGY: Threshold-Based Opportunistic Contribution**

**Core Decision Rule:**

In round t < r (not the final round), compute c_t = number of players observed cooperating in round t-1. Cooperate if and only if:

c_t < m - 1

Defect otherwise.

In round r (final round), defect unconditionally.

**Round 1 (No History):**

Assume c_0 = ⌈(n-1)/2⌉. Apply the core decision rule. If this yields uncertain comparison (e.g., when n is small), cooperate. This provides initial information.

**Rationale:**

- If observed cooperators c_t < m-1, then even my cooperation might not secure the threshold. Contributing is necessary insurance: it moves the count to c_t + 1. If c_t + 1 ≥ m, I get k (net gain k-1). If c_t + 1 < m, threshold fails and I get only what I privately kept. Without contributing, I definitely fail and get 0 bonus.

- If c_t ≥ m-1, the threshold is already met or will be met without me. Defecting yields payoff 1 + k. Contributing yields payoff 0 + k. Defection is strictly better by 1 unit.

- In the final round, future cooperation patterns are irrelevant. No strategic value exists to conditioning future behavior on my action, so pure self-interest dictates defection.

**Adaptation Over Time:**

The strategy automatically adjusts: as cooperation rates rise, you defect more often (free-riding). As they fall, you contribute more often (rescuing the collective outcome). This balances maximizing individual payoff against the risk of total failure.

**Edge Case: m = n**

If every player must cooperate, the strategy tends toward cooperation in early rounds (since c < m-1 is common), switching to defection only when near-universal cooperation is observed. This appropriately reflects that individual contribution is essential.
'''

description_SELFINTERESTED_6 = '''
# Adaptive Free-Riding with Conditional Cooperation Recognition

## Core Decision Rule

**Default: Always defect**, with one exception triggered by observed cooperation patterns.

**Per-round decision**:

```
if round == 1:
    return DEFECT

else if round < r:
    observed_cooperators = count of opponents who cooperated last round
    
    if observed_cooperators >= m - 1:
        return DEFECT  // threshold likely met, free-ride
    else:
        if round >= ceil(r/2):  // middle-game or later
            recent_coop_rate = fraction of opponents cooperating in rounds [2, current-1]
            if recent_coop_rate >= threshold_rate:
                return COOPERATE  // exploit high cooperation by reaching threshold myself
            else:
                return DEFECT
        else:
            return DEFECT

else if round == r:
    return DEFECT  // last round, no future to build
```

Where `threshold_rate = m / n` (cooperation rate matching minimum threshold).

## Edge Cases

**Round 1**: Defect. Without history, cooperating is a unilateral subsidy with unknown return.

**Last round (r)**: Defect regardless of pattern. No future rounds mean no reputational value from cooperation, and defection always yields 1 + k instead of 0 + k if threshold is met.

**Threshold boundary (exactly m-1 opponents cooperate)**: Defect. My cooperation would create threshold, giving me 0 + k payoff while defection gives 1 + k.

**Observed cooperation drops mid-game**: Revert to defection. If recent cooperation rate falls below m/n, the threshold is no longer reliably reachable, so cooperating becomes a guaranteed loss (0 vs 1).

## Self-Interested Justification

This strategy recognizes that **defection weakly dominates cooperation in all single-round comparisons**: given the same outcome (threshold met or unmet), defection always yields 1 unit more than cooperation.

The conditional cooperation block only triggers when sustained empirical evidence (cooperation rate ≥ m/n across multiple rounds) suggests other players are ignoring this logic and cooperating anyway. When such exploitation opportunity exists, cooperating to ensure threshold-crossing is rational: it locks in shared k-reward rather than risking that threshold fails due to others' temporary cooperation drought.

Against fully rational defectors, this converges to pure defection. Against mixed or conditional cooperators, it shifts to exploit their cooperation when reliable patterns emerge, capturing threshold rewards without paying full cooperation costs in low-cooperation states.
'''

description_SELFINTERESTED_7 = '''
## DYNAMIC THRESHOLD RESPONSE STRATEGY

**Round 1:**
Cooperate. Establish a non-defection baseline and generate observable data about opponent behavior.

**Rounds 2 through r:**

Observe the total number of cooperators from the previous round (including your own action).

Let O = number of other players who cooperated in the previous round
(calculated by subtracting your own previous action from the total)

Decision rule:
- If O ≥ m - 1: **Defect**
  - The threshold can be met without your contribution; secure payoff 1 + k by freeloading
  
- If O = m - 2: **Cooperate**
  - You are the marginal cooperator whose contribution reaches m; cooperating yields (0 + k) = k, which exceeds defecting's (1 + 0) = 1
  
- If O < m - 2: **Defect**
  - Insufficient cooperators to reach threshold; cooperating wastes your endowment with no return

**Last Round (round r):**
Apply the same decision rule. The threshold payoff k applies only within that round, not across future rounds, so there is no strategic reason to deviate.

**Summary of logic:**
The strategy pivots on two insights: (1) you only cooperate when you are the decisive swing voter, pushing the count from m-2 to m, where the k payoff exceeds the 1 endowment cost, and (2) you always defect when others have already secured the threshold without you or when you cannot secure it even with your contribution. This maximizes personal payoff by avoiding wasted contributions while capturing threshold benefits whenever feasible.
'''

description_SELFINTERESTED_8 = '''
# STRATEGY: Adaptive Pivotal Cooperation

## Decision Rules

**Track empirical cooperation**: After each round, record the number of other players who cooperated. Maintain a recent moving average of cooperation observed: `recent_avg = average of cooperation counts from last k rounds` where k = min(3, current_round - 1).

**Base decision rule**:
- Round 1: Defect
- Round r (final): Defect
- Rounds 2 to r-1:
  - If recent_avg ≥ m: Defect (threshold will be met without you; free-ride)
  - If m - 1 < recent_avg < m: Cooperate (you are likely pivotal; cooperation triggers the bonus for you)
  - If recent_avg ≤ m - 1: Defect (threshold cannot be reached even with your participation)

## Edge Cases

**First round**: Defect. You have no history to estimate opponent behavior; defecting is the safe baseline.

**Final round**: Defect. No future rounds exist, so no strategy adaptation or reputation effects matter. Capture the immediate payoff: 1 plus any bonus if m-1 others cooperate.

**Round 2**: Use only round 1 observation. If exactly m-1 cooperated in round 1, cooperate. Otherwise defect.

**Insufficient history**: If fewer than 2 completed rounds have been observed, default to defect unless recent_avg indicates you are pivotal.

## Self-Interest Alignment

This strategy maximizes expected payoff by:

- **Avoiding losses**: Never cooperate when defection yields 1 and cooperation yields 0 (threshold cannot be met)
- **Capturing upside**: Only cooperate when your participation deterministically triggers the bonus, receiving k rather than 1 + k through free-riding—this occurs when recent_avg is just below m
- **Free-riding**: When others consistently cooperate (recent_avg ≥ m), defect to secure 1 + k
- **Pessimistic endgame**: In the final round, defect regardless to secure your private endowment with no cooperative obligation
'''

description_SELFINTERESTED_9 = '''
# ADAPTIVE THRESHOLD TARGETING STRATEGY

**Core Decision Rule:**

In round t, cooperate if and only if one of these conditions holds:

1. **Threshold is within reach**: The observed cooperation count from round t-1 equals m-1, indicating that your cooperation alone would secure the reward for all players
2. **Pessimism threshold**: Observed cooperation has fallen below m in 2 consecutive rounds, and you're in rounds 2 through r-1 (attempt to revive cooperation)
3. **Final round recovery**: t = r (last round), and the current count of cooperators is exactly m-1 (contribute to lock in the reward)

Otherwise, **defect** in all other situations.

---

**Edge Cases & Implementation Details:**

- **Round 1**: Defect. You have no history to condition on. Assume defection baseline.

- **Last round (t = r)**: Cooperate only if you observe exactly m-1 cooperators in round r-1. This is a payoff-neutral choice—you get k whether you cooperate or defect—so contributing ensures the threshold is met if others hold steady.

- **Cooperation drought recovery** (condition 2): If cooperation falls to fewer than m for two consecutive rounds, attempt one cooperative gesture. Defect again if this doesn't increase cooperation counts in the next round.

- **When m-1 cooperators observed**: Always cooperate. You receive k + 0 instead of k + 1 (they get the reward), but your marginal act determines collective success, making cooperation the pivotal move.

---

**Self-Interest Justification:**

This strategy optimizes for payoff through:
- **Avoiding wasted cooperation** when threshold is unreachable (low cooperation streaks)
- **Free-riding when possible** by defecting when m-1 others already cooperate (you secure k and keep 1)
- **Strategic cooperation only at critical junctures** (m-1 threshold, last round) where your action changes the outcome
- **Attempted recovery** to prevent complete breakdown, since universal defection yields payoff of r while threshold cooperation yields 2r
'''

description_SELFINTERESTED_10 = '''
**ADAPTIVE PIVOTAL PARTICIPATION**

**Decision Rule:**

In round t, observe the number of cooperators from round t-1 (call this c_prev). Apply the following:

```
If t == 1:
  → DEFECT

Else if t == r (final round):
  → DEFECT

Else if c_prev ≥ m-1:
  → DEFECT
  (threshold achievable without me; defecting gains +1)

Else if c_prev == m-2:
  → COOPERATE
  (I am pivotal; cooperation gets me k, defection gets me 1+k, 
   but defecting breaks threshold and all gain 0 instead of k)

Else (c_prev < m-2):
  → DEFECT
  (even with my cooperation, threshold will not be met; 
   cooperating costs 1 for payoff of 0)
```

**Rationale:**

The self-interested objective is to secure the k payoff when possible while avoiding the cost of cooperation (contributing 1 of endowment). Defection yields +1 more than cooperation in any round where the threshold is met. Therefore, cooperate only when:

1. The prior round showed exactly m-2 cooperators, making my participation the marginal difference between crossing m and failing
2. This is not the final round (final round cooperation cannot influence future rounds)
3. Not round 1 (no basis for estimating group cooperation yet)

This strategy avoids the sucker's payoff (cooperating when threshold fails anyway) and the temptation to free-ride (defecting when threshold succeeds without me), while securing the shared benefit when I am necessary for it.

**Round 1 and Final Round:**

Round 1 begins with DEFECT due to information vacuum—cooperation is speculative without any history. The final round is DEFECT because future cooperation cannot affect any payoffs; the game ends immediately.
'''

description_SELFINTERESTED_11 = '''
# Adaptive Threshold-Matching Strategy

## Core Decision Logic

Estimate the expected cooperation rate among opponents based on observed history. Cooperate if and only if my cooperation is "pivotal" — meaning my contribution determines whether the threshold is reached.

**General Rule (Rounds 2 through r):**
1. Let `recent_cooperators` = number of players who cooperated in the previous round
2. Let `opponent_avg_rate` = average cooperation rate observed among other players across all previous rounds
3. Project: `expected_opponent_cooperators` = round(`opponent_avg_rate × (n-1)`)

Then:
- If `expected_opponent_cooperators ≥ m`: **Defect** (threshold will be met without me; free-ride)
- If `expected_opponent_cooperators = m - 1`: **Cooperate** (my contribution is decisive)
- If `expected_opponent_cooperators < m - 1`: **Defect** (threshold cannot be reached even with my help)

## Edge Cases

**Round 1 (No history):**
- If `m > n - 1`: **Cooperate** (others alone cannot satisfy threshold; my contribution is necessary)
- Otherwise: **Defect** (adopt a defecting posture and observe opponent behavior before committing)

**Round r (Last round):**
- Apply the same general rule as rounds 2–(r-1). The final round offers no strategic advantage to cooperation beyond this round's payoff, so the same logic applies.

## Refinements for Robustness

- If fewer than 2 rounds of history exist, weight the most recent observation more heavily
- If opponents exhibit volatile behavior (high variance in cooperation), increase the threshold for cooperation: cooperate only if `expected_opponent_cooperators ≤ m - 2` (require higher confidence of pivotality)
- If all previous rounds showed universal defection or universal cooperation, assume that pattern continues (sticky behavior)
'''

description_SELFINTERESTED_12 = '''
# Adaptive Free-Rider Strategy with Threshold Exploitation

## Core Decision Rule

Observe the cooperation count among opponents in each round. After round t, let c_t denote the number of cooperators observed.

**Default behavior:** Defect

**Conditional cooperation trigger:** Cooperate in round t if and only if:
1. c_{t-1} ≥ m - 1 (observed cooperators suggest threshold will be met even without my contribution), AND
2. t < r (not the final round), AND
3. My cooperation in round t-1 was met with threshold success

**Exception (last round):** Always defect in round r regardless of history.

## Round-by-Round Logic

**Round 1:** Defect. No history to condition on; gather information about baseline cooperation rates.

**Rounds 2 to r-1:** 
```
if (cooperators_last_round >= m - 1) AND (last_round_threshold_met):
    Cooperate with probability p(c_t)
else:
    Defect
```

where p(c_t) = min(0.5, c_{t-1}/m) — a conservative estimate that defects unless threshold cooperation is robust.

Actually, simplify to pure strategy: **Defect unless you've observed c_{t-1} ≥ m for at least 2 consecutive rounds, indicating stable overprovisioning.**

**Final round r:** Defect unconditionally. The threshold being met this round offers no future benefit to ensure payoff k_r is maximized as (1 + k) rather than k.

## Edge Cases

- **Early rounds with low observed cooperation:** Defect and monitor. No incentive to unilaterally bridge the gap to m.
- **Sudden drops in cooperation count:** Return to defection immediately; threshold may fail.
- **Exactly m-1 cooperators observed:** Defect. Your contribution would just barely make threshold; wait to see if others contribute further.
- **n = 2, m = 2:** Defect always (you alone cannot meet threshold).

## Rationale

This strategy exploits the asymmetry: defection pays (1 + k) when others ensure threshold, pays 1 when they don't. Cooperation only when you can "hide" among sufficient other cooperators and defect in the terminal round to capture extra surplus. It avoids being a sucker who cooperates while others defect, maximizing total payoff against most opponent compositions.
'''

description_SELFINTERESTED_13 = '''
# Marginal Threshold Cooperator

**Objective:** Cooperate only when your contribution is necessary or nearly necessary to reach the threshold, defect otherwise.

## Decision Rules

**Track:** Maintain a weighted average of cooperators observed in each previous round. Recent rounds carry 2× weight; older rounds carry 1× weight.

**Round 1:**
Cooperate. (Initialize the game with a cooperator.)

**Rounds 2 through r:**

1. Calculate `weighted_avg_cooperators` from rounds 1 to t−1 using exponential decay (most recent round 2×, prior round 1.5×, etc., or use recency window of last 3 rounds).

2. Estimate expected cooperators excluding yourself: `expected_others = weighted_avg_cooperators`

3. Apply decision rule:
   - If `expected_others >= m`: **Defect**  
     (Threshold met without you; free-ride for payoff 1+k instead of k)
   
   - If `expected_others == m - 1`: **Cooperate**  
     (Your cooperation brings total to m; you reach k instead of 0)
   
   - If `expected_others < m - 1`: **Defect**  
     (Your single contribution cannot reach m; cooperating yields 0 vs defecting yields 1)

## Edge Cases

**Last Round (t = r):**
Apply the same rule. No forward-looking incentives change the calculation—if threshold is met, defect for 1+k; if not met and you can't swing it, defect for 1.

**Severe Collapse (all others defect consistently):**
If `weighted_avg_cooperators` stabilizes near 0, defect every round afterward (expected_others < m−1 triggers defection).

**Gradual Decline:**
If cooperation erodes round to round, the weighting naturally tracks the decline. Once expected_others falls below m−1, switch to defection and remain there unless cooperation recovers.

**Initial Volatility (few rounds of history):**
If `weighted_avg_cooperators` is between m−2 and m, the strategy oscillates between defect and cooperate until history stabilizes. This is intentional: it hedges against uncertain opponent behavior early on.
'''

description_SELFINTERESTED_14 = '''
# Threshold-Matching Strategy with Conditional Defection

**Core Principle**: Contribute minimally to reach the threshold m, then defect to capture k+1 rather than k. Use observed cooperation counts to estimate whether your contribution is needed.

## Decision Rule by Round Type

**Round 1 (Opening)**:
- Play C
- Rationale: Establish baseline. If m-1 others cooperate, you become the threshold-closer and get k payoff. Probes opponent cooperation levels.

**Rounds 2 to r-1 (Adaptive Rounds)**:
- Let c_prev = observed number of cooperators in previous round
- If c_prev ≥ m: Play D
  - The threshold is already being met by others. Capture k+1 by defecting.
- If c_prev = 0: Play C
  - Last round failed entirely. Contribute to prevent another all-defect outcome worth 1.
- If 1 ≤ c_prev < m: Play C with probability p_adapt where:
  ```
  p_adapt = max(0, (m - c_prev) / (n - 1))
  ```
  - Expected contribution gap from last round: m - c_prev
  - Your probability of needing to close the gap across n-1 opponents
  - If c_prev = m-1, cooperate with probability 1/(n-1) (mostly free-ride)
  - If c_prev = 1, cooperate with probability (m-1)/(n-1) (likely need to help)

**Round r (Final Round)**:
- Play D unconditionally
- Rationale: No future rounds. The threshold's benefit (if realized) applies regardless; capturing k+1 instead of k is strictly better. Endgame dominance.

## Edge Cases

**If n = m (all must cooperate)**:
- Round 1: Play C (threshold always fails if anyone defects)
- Rounds 2 to r-1: Play D when threshold met last round, else C
- Round r: Play D
- Outcome: Likely oscillation between all-C and mixed strategies; unavoidable for self-interest

**If m = n-1 (only one defector tolerated)**:
- Same rule applies, but threshold nearly always met after round 1
- Heavily favors defection in rounds 2 onward

**Ties in probabilistic decisions**:
- Use round number as tiebreaker: round number mod 2 determines rounding direction for repeatability

## Self-Interested Logic

- **Rounds with threshold met**: Defect always provides k+1 vs. k. No reason to cooperate.
- **Rounds with threshold unmet**: Cooperate only if probability-weighted expectation of crossing threshold next round exceeds cost of contributing now (worth tracking implicitly through p_adapt).
- **Final round**: Future payoff irrelevant; myopic defection maximizes immediate gain.
- **Opening play**: Forces others to signal their cooperation willingness; minimizes wasted contribution over remaining rounds.

The strategy exploits the asymmetry that defection pays k+1 once the threshold exists, making it self-interested to free-ride aggressively while maintaining just enough cooperation to keep the threshold reachable.
'''

description_SELFINTERESTED_15 = '''
# Threshold-Responsive Cooperation Strategy

**Decision Rule by Round:**

**Round 1:** Cooperate.
- Serves as an exploratory signal to gauge opponent cooperation levels without suffering cumulative losses.

**Rounds 2 through r:** Cooperate if and only if the number of cooperators in the previous round was ≥ m - 1.
- Interpretation: If at least m-1 players cooperated last round, your single cooperation brings the total to ≥ m, triggering the reward k for all players (including you). Cooperating yields payoff k - 1 (net positive since k > 1).
- If fewer than m-1 cooperated, the threshold is unattainable regardless of your action. Defecting yields payoff 0 (better than cooperation's payoff of -1).

**Edge Case—Round r (Final Round):** 
Apply the same rule as rounds 2 to r-1. The reward payoff still applies in the final round, so the decision calculus remains identical. Only in the degenerate case where you predict with certainty that all other players will defect (e.g., if they follow this same strategy and all defected last round) is cooperation irrational.

---

**Pseudocode:**

```
if round == 1:
    action = COOPERATE
else:
    cooperators_last_round = observed_cooperators(round - 1)
    if cooperators_last_round >= m - 1:
        action = COOPERATE
    else:
        action = DEFECT
```

---

**Self-Interest Alignment:**

This strategy prioritizes immediate payoff maximization per round: you only incur the cooperation cost (1) when your contribution directly enables the shared reward (k). You defect preemptively whenever the threshold is unattainable, avoiding wasted investment. The strategy adapts responsively to the aggregate cooperation level observed, scaling defection when collective action appears infeasible.
'''

description_SELFINTERESTED_16 = '''
## STRATEGY: Adaptive Threshold Monitoring with Defensive Defection

**ROUND 1 (INITIAL MOVE):**
Defect. You have no historical information. Assume opponents are self-interested like yourself and will not cooperate without evidence of reciprocity.

**ROUNDS 2 to r-1 (ADAPTIVE PHASE):**

Observe c_t-1 (the number of players who cooperated in round t-1):

1. **If c_t-1 ≥ m:** Defect
   - Threshold is being met by others. Free-ride by keeping your endowment and still claiming the reward k.

2. **If c_t-1 = m-1:** Cooperate
   - One more cooperator would secure the threshold for everyone. You contribute to reliably hitting the target, ensuring you receive k. The opportunity cost of contributing (paying 1) is offset by guaranteeing the payoff k.

3. **If c_t-1 < m-1:** Defect
   - Threshold is far from being met. Cooperating would cost you 1 but wouldn't move the outcome from failure to success. Keep your endowment.

**ROUND r (FINAL ROUND):**
Defect unconditionally. This is the last round with no future consequences. Exploit whatever outcome emerges—if others reach m cooperators, you gain 1+k by defecting; if they don't, you gain 1 regardless.

**RATIONALE:** This strategy avoids mutual defection traps in middle rounds by strategically filling small gaps in cooperation, while protecting against exploitation by free-riding whenever the threshold is already secure. The final-round defection captures any residual value without commitment cost.
'''

description_SELFINTERESTED_17 = '''
# Adaptive Threshold-Matching Strategy

## Core Decision Rule

Cooperate if and only if your cooperation is necessary and sufficient to reach the threshold m.

For round t, let c_prev = number of opponents observed cooperating in round t-1.

**If t = 1 (first round):**
Cooperate. This probes opponent tendencies without committing long-term; you learn their baseline behavior.

**If 1 < t < r (middle rounds):**
- If c_prev ≥ m: Defect (threshold met without you; free-ride on others' contributions)
- If c_prev + 1 ≥ m: Cooperate (your contribution is pivotal; ensures you capture reward k)
- If c_prev + 1 < m: Defect (threshold unattainable regardless; no benefit to contributing)

**If t = r (final round):**
Always defect. No future rounds remain, so you maximize immediate payoff by avoiding the cost of cooperation. Even if you needed cooperation earlier, the last round is a pure extraction opportunity.

## Handling Volatile Cooperation

If opponent behavior fluctuates, use a moving average over the last 2–3 rounds instead of single round c_prev:

```
cooperation_average = (c_{t-1} + c_{t-2}) / 2
expected_others = round(cooperation_average)
```

Apply the same decision thresholds above.

## Rationale

This strategy minimizes your cost (number of rounds you cooperate) while maximizing captures of the reward k. You cooperate only when you are the critical marginal contributor. In all other states—threshold already met, or threshold impossible—you defect and enjoy the payoff 1 + k or 1 respectively. The last round pivot exploits the terminal condition to extract pure gain.
'''

description_SELFINTERESTED_18 = '''
# Adaptive Threshold Matching Strategy

## Core Decision Rule

Track the proportion of cooperators observed among your opponents across all previous rounds. Cooperate if and only if you expect the cooperation threshold to be met, accounting for your own participation.

```
Let observed_coop = total cooperators seen across all previous rounds
Let total_opponent_observations = (rounds completed) × (n - 1)

If total_opponent_observations > 0:
  observed_proportion = observed_coop / total_opponent_observations
Else:
  observed_proportion = (m - 1) / (n - 1)  // optimistic initial belief

Expected opponents cooperating next round = observed_proportion × (n - 1)

If 1 + expected_opponents_cooperating ≥ m:
  COOPERATE
Else:
  DEFECT
```

Simplified threshold: Cooperate if `observed_proportion ≥ (m - 1) / (n - 1)`.

## First Round

Cooperate. This generates initial information about the cooperativeness of your opponents and positions you to benefit if others are similarly cooperation-seeking.

## Subsequent Rounds (2 to r-1)

Apply the core decision rule above. Update your observed cooperation count after each round and recalibrate before the next decision.

## Last Round (Round r)

Apply the core decision rule unchanged. If your estimate shows the threshold will likely be met (observed_proportion ≥ (m-1)/(n-1)), defecting yields (1 + k) while cooperating yields only k. However, if you've never observed the threshold being met historically, continue cooperating to maximize any remaining chance of collective success, since cooperation is costless to attempt at that point.

## Edge Cases

- **Immediate defection signal**: If in round 1 fewer than (m-1) other players cooperate, switch to permanent defection for all remaining rounds. The threshold appears unachievable.
- **Recovering from low cooperation**: If cooperation drops below the threshold midway through, return to defection until observations stabilize at the required level again.
- **Tie-breaking rounds**: If observed_proportion equals exactly (m-1)/(n-1), cooperate (marginal case where you might be the swing voter).

## Self-Interested Alignment

This strategy maximizes expected personal payoff by: (1) exploiting the asymmetry where defection in a successful threshold yields (1 + k) vs. cooperation's k; (2) avoiding wasted contributions when threshold is unachievable; (3) calibrating effort based on empirical evidence of others' willingness to cooperate.
'''

description_SELFINTERESTED_19 = '''
# Adaptive Threshold Matching Strategy

**Round 1:** Defect. Gather information about opponent cooperation rates without incurring cost.

**Rounds 2 through r-1 (Middle rounds):**

Track the count of opponents who cooperated in the previous round, denoted c_prev. Calculate:

- Estimated probability of threshold being met if you cooperate: P_meet = I(c_prev + 1 ≥ m) where I is the indicator function.

If P_meet = 1 (meaning c_prev ≥ m-1):
- Cooperate, because the threshold is likely to be met, yielding payoff k-1 rather than 0.

If P_meet = 0 (meaning c_prev < m-1):
- Defect, because the threshold will not be met, yielding payoff 1 rather than 0.

Across all middle rounds, track the rolling average cooperation rate among all opponents: avg_coop = (total opponent cooperations observed so far) / (opponents observed so far).

**Round r (Final round):**

Apply the same decision rule as middle rounds: cooperate if observed c_prev ≥ m-1, else defect. The final round uses identical logic since both rounds are payoff-equivalent (no future rounds to influence).

**Edge case — tie-breaking:** If you observe exactly c_prev = m-1 cooperators in round t, cooperating brings the threshold from m-1 to exactly m, triggering the reward. Cooperating yields k-1; defecting yields 1+k. Since 1+k > k-1, defect even in this case.

**Outcome under this strategy:** Always defect except when observing at least m-1 cooperators in the immediately preceding round, at which point cooperate to capture the reward alongside them.
'''

description_SELFINTERESTED_20 = '''
# Adaptive Defection with Threshold-Proximity Cooperation

**Decision Rule:**

Defect in the first round. For each subsequent round t ∈ {2, ..., r}, observe c_{t-1}, the number of cooperators in round t-1.

- If c_{t-1} ≥ m: Defect (threshold already met; free-ride on others' contributions)
- If c_{t-1} = m - 1: Cooperate (contribution is pivotal; crossing threshold gains +k)
- If c_{t-1} < m - 1: Defect (insufficient past cooperation to justify personal cost)

**Last Round Modification:**

Always defect in round r, regardless of history. Future rounds do not exist to reward reciprocation, so the pivotal-contribution logic collapses.

**Edge Cases:**

- If m = 1, only one cooperator needed: defect every round after round 1 (impossible to be pivotal, and threshold trivially met if anyone cooperates).
- If m ≥ n, threshold cannot be met: defect always (the game is a pure loss; preserving the endowment is optimal).

**Logic:**

The strategy maximizes self-interest by exploiting two principles:

1. **Free-riding**: Once the threshold is reached, defection yields 1 + k rather than k, strictly dominating cooperation. Remain defective.

2. **Pivot Opportunism**: When cooperation falls to exactly m - 1, a single additional cooperator shifts the outcome from payoff 1 (failure) to payoff k (success), a net gain of k - 1 > 0. Cooperate only in this narrow window; elsewhere, the personal cost outweighs expected benefit.

This strategy robustly handles heterogeneous opponents: it neither assumes repeated reciprocation nor requires coordination. It responds only to aggregate historical outcomes, making it adaptive across a range of opponent behaviors while remaining individually rational at each decision point.
'''

description_SELFINTERESTED_21 = '''
**STRATEGY: Adaptive Threshold-Targeting**

**Round 1 (Initialization):**
Defect. This round serves as observation to calibrate opponent cooperativeness without commitment.

**Rounds 2 to r-1 (Adaptive Phase):**

Let p̂ = average cooperation rate observed across all previous rounds (number of cooperators observed / (n-1) / number of rounds played so far).

Calculate expected cooperators from opponents in the current round: E_coop = (n-1) × p̂

Decision rule:
- **If E_coop ≥ m - 1**: Defect. The threshold will be reached by others' cooperation; free ride on their contribution.
- **Else if E_coop < m - 1**: 
  - **If E_coop + 1 ≥ m**: Cooperate. Your contribution is necessary and sufficient to reach threshold. Securing k outweighs the cost of 1 unit.
  - **Else if E_coop + 1 < m**: Defect. Even with your cooperation, threshold cannot be reached. No benefit to cooperating.

**Round r (Final Round):**

Calculate expected cooperators: E_coop = (n-1) × p̂

Decision rule:
- **If E_coop ≥ m**: Defect. Free ride in the terminal round—the threshold is assured.
- **Else if E_coop < m and E_coop + 1 ≥ m**: Cooperate. This is your last opportunity to secure the threshold reward.
- **Else if E_coop + 1 < m**: Defect. Threshold is unattainable; defection saves 1 unit with no downside.

**Edge case handling:**

If insufficient history exists (round 2 with only round 1 data), use p̂ = observed cooperation rate from round 1. If all opponents defected in round 1, assume p̂ → 0 and defect unless you can solo-reach threshold (m = 1).
'''

description_SELFINTERESTED_22 = '''
THRESHOLD-DEPENDENT FREE-RIDING STRATEGY

**Core Decision Rule:**

Let c_t denote the number of cooperators observed among the n-1 opponents in round t.

- **Defect** if c_t ≥ m - 1
  - The threshold will be reached even without my contribution; free-ride on others' cooperation

- **Cooperate** if c_t < m - 1 AND c_t + 1 ≥ m
  - My cooperation is pivotal and necessary to reach the threshold; contribute strategically

- **Defect** if c_t + 1 < m
  - Cooperation is futile; threshold unreachable regardless of my action

**Round 1 Default:**
Defect. No history exists; assume others will likely defect given standard self-interest incentives. This tests the environment's cooperation level.

**Round r (Final Round):**
Apply the same decision rule. The finality of the game does not change payoff calculations within the round itself—threshold achievement in round r still delivers k.

**Behavioral Consequence:**

This strategy produces adaptive defection:
- Free-ride aggressively when others cooperate sufficiently
- Cooperate minimally and only when your contribution is the marginal actor closing the gap to m
- Never waste contribution on hopeless rounds where m cannot be reached

The strategy is self-interested because it maximizes private payoff by avoiding unnecessary cooperation costs while extracting the collective reward whenever it becomes available. It exploits the aggregate observation structure: by monitoring only the count of cooperators, you make binary defect/cooperate decisions without needing to identify or interact with specific opponents.

If this environment contains many defectors (common in self-interested populations), you will defect consistently and payoff remains 1 per round. If opponents maintain substantial cooperation rates, you extract 1 + k per round through persistent free-riding.
'''

description_SELFINTERESTED_23 = '''
# Adaptive Threshold Cooperation Strategy

**Core Decision Rule:**

Cooperate in round t if and only if:
1. The observed opponent cooperation rate from the previous round meets or exceeds a critical threshold
2. We are not in the final round

Specifically, cooperate in round t (where t < r) if:
```
(n-1) × p_{t-1} ≥ m - 1
```

where p_{t-1} is the proportion of opponents who cooperated in round t-1, calculated as:
```
p_{t-1} = (count of opponent cooperations in round t-1) / (n-1)
```

**Round-by-Round Behavior:**

- **Round 1 (Initial)**: Defect. Gather information about opponent cooperation rates without bearing the cost of unreciprocated contribution.

- **Rounds 2 through r-1 (Middle)**: Apply the threshold rule above. Cooperate only if the observed cooperation rate suggests that, conditional on my cooperation, we will likely reach m cooperators total (requiring m-1 others to cooperate).

- **Round r (Final)**: Always defect, regardless of history. Future cooperation yields zero continuation value. Any reward from the project materializes this round whether I contribute or not; defection captures value without cost.

**Rationale for Thresholds:**

The critical cooperation rate is (m-1)/(n-1). If opponents have cooperated at this rate or higher, defecting is exploitative (I get k+1 payoff if threshold met); cooperating ensures I still get k. Below this rate, the project fails regardless, so cooperating yields only 0 while defecting yields 1.

**Handling Sparse History:**

In round 1, defect by default. If round 2 arrives with fewer than n-2 rounds of observational history (impossible given r ≥ 2), apply the rule using the single round of data available.
'''

description_SELFINTERESTED_24 = '''
# Threshold-Monitoring Defection Strategy

**Core Decision Rule:**

Let O_t = number of opponents observed to cooperate in round t.

In round t (where 1 < t ≤ r):
- If O_t ≥ m: Play D (threshold achieved without your contribution; secure private payoff 1 + k)
- If O_t = m − 1: Play C (cooperation pushes you to threshold; secure payoff k > 1)
- If O_t < m − 1: Play D (threshold unattainable; secure private payoff 1 over wasted 0)

**First Round (t = 1):**
Play C. Without history, cooperation bootstraps the possibility of threshold achievement. Expected payoff from C is k (if others also cooperate) versus expected payoff from D of approximately 1 (no one has cooperated yet). The expected value of C dominates under reasonable assumptions about opponent strategy diversity.

**Last Round (t = r):**
Play D. Apply the above thresholds strictly. No future rounds exist; defection extracts maximum private value from any achieved threshold while eliminating the cost of contribution.

**General Logic:**

This strategy exploits the structure where defection is privately optimal *given a met threshold*, while identifying the exact margin where your cooperation becomes pivotal (O_t = m − 1). At that margin, the bonus k exceeds the cost 1, so contribution is rational self-interest.

When O_t ≥ m, others have already secured the threshold. Cooperating only reduces your round payoff from 1 + k to 0 + k. When O_t < m − 1, cooperation alone cannot deliver the threshold regardless of your action, so defection preserves the endowment.

**Adaptation Mechanism:**

The strategy updates its behavior each round based solely on observed opponent cooperation counts. If opponents shift toward higher cooperation, you shift toward defection (exploiting the threshold). If opponents defect en masse, you follow suit, minimizing losses.
'''

description_SELFINTERESTED_25 = '''
# Empirical Threshold Matching

**Decision Rule:**

Cooperate if and only if the number of cooperators observed in the previous round is at least m - 1. Otherwise defect.

**Pseudocode:**

```
Round 1:
  If (n - 1) * (k - 1) / k ≥ m - 1, Cooperate
  Else Defect

Rounds 2 to r:
  observed_cooperators = count of cooperators in round t-1
  If observed_cooperators ≥ m - 1, Cooperate
  Else Defect
```

**Rationale:**

In any round, defection strictly dominates cooperation unless the threshold is met. I cooperate only when I have evidence that cooperation is pivotal—that is, when others are already cooperating at levels that suggest my contribution will push the group to exactly m or beyond.

The threshold of m - 1 observed cooperators indicates I can be the marginal player whose cooperation triggers the bonus for everyone (including myself). Since I get k when the threshold is met versus 0 when it's not, and defectors get 1 + k when the threshold is met versus 1 when it's not, I only cooperate when my contribution directly enables the threshold.

**Round 1 Initialization:**

Assume others have a baseline cooperation rate reflecting that cooperation becomes attractive when it's sufficiently common. Cooperate in round 1 if the expected number of cooperators among opponents, assuming each has an independent probability of cooperating proportional to when cooperation becomes self-interested (roughly when k > (n-m)/m), reaches m - 1. If uncertain, use (n - 1) / 2 as a rough estimate and cooperate if this is ≥ m - 1.

**Last Round:**

Apply the same rule. There is no reputational discount in the last round, so the calculation remains unchanged: cooperate if observed cooperation in round r-1 signals I can be pivotal.

**Robustness:**

This strategy adapts to any opponent distribution: all-cooperators (defect, since threshold is already met), all-defectors (defect, since threshold cannot be met), and mixed populations (match the threshold empirically). It requires only observable aggregate cooperation counts and makes no assumptions about opponent rationality or coordination.
'''

description_SELFINTERESTED_26 = '''
# Adaptive Conditional Cooperation Strategy

## Core Decision Rule

**Cooperate if and only if observed cooperation in the prior round was below the threshold m; defect if it was at or above m.**

## Implementation

**Round 1:**
- Cooperate. 
- Rationale: No prior data exists. Cooperation in round 1 probes opponents' types and signals availability for reciprocity, revealing information for subsequent rounds.

**Rounds 2 to r:**
- Let C_t = number of cooperators observed in round t−1
- If C_t ≥ m: **Defect** (threshold was met; the public good succeeded regardless of my action, so I capture the gain by free-riding: payoff is 1 + k instead of 0 + k)
- If C_t < m: **Cooperate** (threshold failed; contribute to increase the probability of reaching m cooperators this round, yielding potential payoff k instead of 0)

## Edge Cases

**Last round (round r):** Apply the same rule above. Do not defect in the last round on the assumption others will defect—this reasoning is common, and if universally applied, causes collective failure. Maintain the conditional cooperation rule through the final round.

**Boundary condition (C_t = m):** Defect. The threshold has been met; the reward k is locked in. Taking the additional +1 from defection is self-interested maximization.

**Boundary condition (C_t = 0 or near-zero for multiple rounds:** Continue cooperating. This signals willingness to coordinate and leaves open the possibility of collective gain in later rounds. If other players are also using threshold-based strategies, observed low cooperation may reflect the initial probe; reciprocal cooperation can emerge.

## Self-Interest Alignment

This strategy prioritizes immediate payoff gain in every round:
- When the threshold is met, defection dominates cooperation (+1 advantage)
- When the threshold is unmet, cooperation offers the only path to gain over the baseline (0 vs. 1 if solo cooperator, but k if threshold is collectively reached)
- The strategy exploits any stable cooperation by others while minimizing losses from solo contribution
'''

description_SELFINTERESTED_27 = '''
# Adaptive Threshold Cooperator Strategy

**Core Logic**: Cooperate only when your contribution is pivotal to achieving the threshold, avoiding both futile contributions and missed opportunities to free-ride.

## Decision Rules

**First Round**: Defect. You have no information about opponent behavior and contribute zero value toward any threshold estimate.

**Rounds 2 through r-1 (Middle Rounds)**:
1. Observe the number of cooperators c from the previous round
2. Maintain a running estimate: `avg_observed = average cooperation count over all completed rounds`
3. Cooperate if and only if: `avg_observed ≥ m - 1`
4. Otherwise defect

**Final Round r**: Apply the same decision rule as middle rounds—the lack of future payoff does not change the current round's optimization.

## Rationale and Execution

Tracking aggregate cooperation allows you to estimate whether opponents' cooperation will naturally satisfy the threshold without your contribution. If the threshold is m and you observe m-1 or more cooperators in recent history, your single cooperation becomes pivotal:
- Without you: threshold not met, you earn 1 (if defect) or 0 (if cooperate)
- With you: threshold met, you earn 1+k (if defect) or k (if cooperate)

Since k > 1, cooperating when you're pivotal yields a net gain of k versus 0. Conversely, if past rounds show fewer than m-1 cooperators on average, your cooperation cannot tip the threshold and wastes your endowment.

## Edge Cases

- **Oscillating opposition**: If opponents alternate between high and low cooperation, rely on the running average rather than the most recent round to smooth out noise
- **Perfect defection by all**: You observe c=0 always; avg_observed remains 0; you continue defecting, earning payoff 1 each round—rational given the defection environment
- **Drift toward cooperation**: If avg_observed gradually rises above m-1, you switch to cooperation and remain there, moving from free-rider to conditional cooperator
- **Rare threshold success**: If cooperation happens sporadically (c crosses m-1 once), your switch to cooperation increases future threshold likelihood, amplifying the benefit in subsequent rounds

This strategy is self-interested because it never sacrifices payoff; you only pay the cooperation cost when doing so directly improves your round payoff by enabling the threshold.
'''

description_SELFINTERESTED_28 = '''
## Adaptive Free-Riding with Conditional Cooperation

**Decision Rule by Round Type:**

**Round 1:**
Play D. This tests opponent behavior without risking wasted cooperation.

**Rounds 2 to r-1 (Middle Rounds):**
Maintain a count of observed cooperators from the previous round, denoted c_prev.

- If c_prev ≥ m: Play D
  - The threshold has been met. Free-ride on others' cooperation.
  
- If m-1 ≤ c_prev < m: Play C
  - Nearly at threshold. Cooperate to help trigger it in the next round, so you can free-ride afterward.
  
- If c_prev < m-1: Play D
  - Too few cooperators. Cooperation is unlikely to push the group over the threshold; don't waste the endowment.

**Round r (Final Round):**
Play D regardless of c_prev. No future rounds exist, so no future payoff to protect through conditional cooperation. Free-ride if you expect the threshold to be met (based on c_prev ≥ m from round r-1); otherwise defect anyway since cooperation won't change anything.

---

**Rationale:**

The strategy exploits the payoff structure: when the threshold is met, D yields 1+k while C yields only k. The self-interested goal is to secure the benefit k while keeping the endowment (earning 1+k instead of k). Conditional cooperation in near-threshold situations (c_prev = m-1) instrumentally increases the probability that future rounds reach the threshold, enabling free-riding. Once the threshold is reliably met, shift to pure defection. In the final round, defection is risk-free.
'''

description_SELFINTERESTED_29 = '''
**Threshold-Aware Conditional Cooperator**

**STATE TRACKING:**
Maintain running count of how many opponents cooperated in each round. This is your primary signal for deciding your next move.

**DECISION RULE:**

*Round 1 (initialization):*
Cooperate with probability (m - 1) / (n - 1). This seeds initial cooperation proportional to the cooperation burden required. If very few cooperators are needed relative to group size, cooperate less; if many are needed, test with higher cooperation.

*Rounds 2 through r - 1 (adaptive phase):*
Observe the count C of cooperators from the immediately preceding round.
- If C ≤ m - 2: **COOPERATE** — The threshold is jeopardized. Your cooperation alone cannot guarantee success, but it materially increases the probability. Since k > 1, receiving k is better than receiving 0.
- If C ≥ m - 1: **DEFECT** — The threshold is either met or will be met by others' contributions. Defection yields (1 + k), cooperation yields k. Free-ride.

*Round r (final round):*
Observe C from round r - 1.
- If C = m - 1 exactly: **COOPERATE** — You are the pivotal player. Your cooperation guarantees the threshold and secures payoff k. Defection gives you only 1 (since the threshold fails without you). Cooperate to capture k.
- If C < m - 1: **DEFECT** — Even with your cooperation, you cannot reach m. Others must also cooperate, but that is not your problem. Take the private payoff of 1.
- If C ≥ m: **DEFECT** — Threshold is assured. Take 1 + k.

**EDGE CASE HANDLING:**

- **m = 1**: Threshold always met. Always defect (payoff = 1 + k).
- **m = n**: Unanimous cooperation required. Follow the main rule: cooperate in rounds 2–r-1 if others are defecting, cooperate in round r only if exactly n - 1 others have cooperated (which means you're pivotal). Otherwise defect.
- **Rounds where no prior history exists**: Use the round 1 initialization rule.

**SELF-INTERESTED JUSTIFICATION:**

This strategy maximizes your payoff by exploiting three principles:
1. **Free-ride when safe**: Once m - 1 others commit, you receive k without paying the cost.
2. **Contribute when critical**: When you are the only remaining cooperator needed (C = m - 1), your cooperation guarantees k instead of earning only 1 by defecting.
3. **Abandon when hopeless**: If threshold cannot be reached even with your contribution, preserve your private payoff of 1 by defecting.

The strategy avoids coordination failure by using observable cooperation counts as a signal. You don't require trust or communication—only the aggregate signal that others are cooperating.
'''

description_SELFINTERESTED_30 = '''
# Adaptive Threshold Exploitation Strategy

## Decision Rule: Core Logic

Each round t, observe the aggregate cooperation count c_t from the previous round (or assume 0 for round 1).

Calculate the opponent cooperation rate: p = c_t / (n - 1)

**Cooperate** if and only if: p < (m - 1) / (n - 1) AND t < r

**Defect** otherwise.

## Rationale

The threshold (m - 1) / (n - 1) is the critical breakpoint: if opponents cooperate at or above this rate, then m cooperators will be reached regardless of my action. At that point, defection strictly dominates (earning 1 + k instead of k). If opponents fall below this rate, the threshold will not be reached whether I cooperate or defect, so defection strictly dominates (earning 1 instead of 0).

The only scenario where my contribution matters is when opponent cooperation is strictly below the threshold. Cooperating then gives me a chance to hit m total cooperators and earn k instead of 0.

## Edge Cases

**Round 1:** Cooperate. You have no history. Cooperating signals willingness to participate and tests whether others will reciprocate. If they do, you can exploit their cooperation in later rounds.

**Final round (t = r):** Always defect. Since there are no future rounds, there is no reputation cost. Opponents cannot punish defection, so extracting the extra unit by defecting is costless.

**Boundary condition when p = (m - 1) / (n - 1):** Defect. At the threshold, you are indifferent to hitting m cooperators because you earn 1 + k either way. Break ties by defecting to secure the marginal unit.

## Adaptive Mechanism

Update your estimate of p after each round by observing reported cooperation. Do not assume all opponents follow the same strategy; the rate may drift. Recalculate the comparison each round to respond to changing cooperation patterns.

This strategy is self-interested because it minimizes wasted cooperation (cooperating only when necessary to reach the threshold) while maximizing exploitation of others' cooperation (defecting whenever the threshold is assured).
'''

description_SELFINTERESTED_31 = '''
# Pivotal Contribution Strategy

## Decision Rule

Cooperate if and only if the observed number of cooperators in the immediately preceding round was exactly m-1. Otherwise, defect.

Formally, in round t > 1:
```
Let c_{t-1} = number of opponents observed cooperating in round t-1
If c_{t-1} == m-1:
  Action[t] = C
Else:
  Action[t] = D
```

## Justification for the Core Logic

When exactly m-1 opponents cooperate, your individual cooperation reaches the threshold, yielding payoff k from you. Your defection would fall short, yielding only 1. Since k > 1, this is the only round-to-round scenario where cooperation yields higher payoff than defection.

When fewer than m-1 opponents cooperate, the threshold cannot be reached even with your participation, so cooperating costs you 1 relative to defection with no benefit.

When m or more opponents already cooperate, the threshold is guaranteed. You receive k whether you cooperate (payoff = k) or defect (payoff = 1+k). Defection dominates.

## Edge Cases

**Round 1:** You have no history. Assume c_0 = 0 (no observed cooperators). Since 0 ≠ m-1, defect.

**Last round (t = r):** Apply the same logic. The finality of the game does not change the payoff comparison—you still earn more by defecting except when pivotal.

**No observation ever matches m-1:** If opposing strategies never produce exactly m-1 cooperators, you defect every round. This is consistent with self-interest.

**Multiple rounds where c_t = m-1:** Cooperate in each such round independently; the rule applies freshly each round based on what you just observed.

## Adaptive Property

The strategy is reactive and minimal. It does not assume opponent strategies, predict future cooperation, or coordinate. It simply responds to the one observable fact that makes cooperation rational: when you are the pivotal player whose contribution uniquely determines success or failure. This aligns with self-interest under honest observation and simultaneous play constraints.
'''

description_SELFINTERESTED_32 = '''
**STRATEGY: Conditional Defection with Threshold-Dependent Cooperation**

**Decision Rule**

In round t, observe o_{t-1} = number of opponents who cooperated in the previous round (round 1 uses o_0 = 0).

- **If t = 1**: Defect (no historical information; defection is the safe default)
- **If t > 1 and o_{t-1} = m - 1**: Cooperate (your contribution becomes pivotal; threshold is met with you, getting payoff k; without you, threshold fails)
- **If t > 1 and o_{t-1} ≠ m - 1**: Defect
  - If o_{t-1} < m - 1: Threshold unachievable even with your cooperation; defection yields 1
  - If o_{t-1} ≥ m - 1: Threshold already met without you; defection yields 1 + k, which exceeds k

**Edge Cases**

- **Last round (t = r)**: Apply the same rule as any other round—the payoff structure is identical. Defect unless o_{r-1} = m - 1.
- **First round (t = 1)**: Always defect. You have no observation to trigger cooperation.
- **Tie situations**: None exist in this formulation; o_{t-1} is an integer.

**Robustness**

This strategy handles diverse opponent behaviors:
- Against pure defectors: You defect every round, earning 1 per round consistently
- Against unconditional cooperators: You cooperate only when pivotal (o_{t-1} = m - 1), earning k when threshold-critical and 1 + k otherwise
- Against reciprocal players: You punish insufficient cooperation (defect) and reward exactly-threshold cooperation (cooperate when pivotal)
- Against mixed strategies: You remain adaptive, defecting in the majority case and exploiting pivotal moments

The strategy maximizes payoff by never over-cooperating—cooperation occurs only when your action determines the outcome, never when defection dominates or cooperation is irrelevant.
'''

description_OPPORTUNISTIC_5 = '''
# Opportunistic Threshold Exploitation Strategy

## Core Logic

Defect as default action. Cooperate only when strategic calculation suggests you are pivotal to reaching the threshold and cannot free-ride.

## Decision Rules

**Last round (t = r):**
Return D. The game ends; there is no future collective benefit to capture and no reason to pay the cooperation cost.

**First round (t = 1):**
Return D. No observational history exists; defection is the safer opportunistic choice when uncertain.

**Rounds 2 through r-1:**
Observe the cooperation count from the immediately preceding round. Call this `recent_coop`.

- If `recent_coop ≥ m - 1`: Return D
  - The threshold is met or will be met without your contribution. Free-ride on others' cooperation and capture the reward k at no cost.

- If `recent_coop = m - 2`: Return C
  - You are the marginal player. Your cooperation pushes the group over the threshold, securing k for yourself. The cost-benefit (k > 1) justifies this conditional contribution.

- If `recent_coop < m - 2`: Return D
  - The threshold is mathematically unreachable even with your cooperation. Defect and preserve the endowment.

## Adaptation Mechanism

Each round, update your estimate of the opposition's propensity by observing the realized cooperation count. If cooperation consistently falls below `m - 1`, the environment is uncooperative; you continue defecting. If cooperation stabilizes near or above `m - 1`, you remain a free-rider. If it hovers around `m - 2`, you intermittently cooperate when you become pivotal.

## Endgame and Early-Game Handling

The last-round defection is strict and non-negotiable—exploit the shadow-of-the-future's absence. The first-round defection avoids commitment to a strategy before signal quality is established. This asymmetry locks in the opportunistic stance: you enter passively, then respond parasitically to others' behavior.
'''

description_OPPORTUNISTIC_6 = '''
# Adaptive Opportunistic Free-Rider Strategy

**Core Decision Rule:**

Cooperate only when you are pivotal—that is, when the observed cooperation level from the previous round equals exactly m-1. In all other cases, defect.

**Detailed Rules by Round:**

**Round 1:**
Defect. You have no history and cannot estimate opponent behavior. Defecting tests whether others will carry the threshold; if they do, you gain the maximum payoff (1 + k) at no cost.

**Rounds 2 through r-1 (Middle Rounds):**
Let c_prev = number of cooperators observed in round t-1.

- If c_prev ≥ m: Defect
  - The threshold was already met. Free-ride on their cooperation.
  
- If c_prev = m - 1: Cooperate
  - You are pivotal. Your cooperation guarantees success (reaching m). Since k > 1, cooperation secures payoff (0 + k = k), while defection yields only 1. Cooperate.
  
- If c_prev < m - 1: Defect
  - The threshold cannot be met even with your cooperation. No point paying the cost.

**Final Round r:**
Let c_prev = observed cooperators from round r-1.

- If c_prev ≥ m: Defect
  - Game ends with the bonus secured. Take the free payoff.
  
- If c_prev = m - 1: Cooperate
  - You are pivotal in the final round. Secure the bonus one last time.
  
- If c_prev < m - 1: Defect
  - Threshold is unattainable. No future rounds to compensate.

**Tie-Breaking in Round 1 vs. Later Rounds:**
This strategy uses round 1 defection as an exploration phase. If opponents predominantly cooperate early, you capitalize by defecting until exactly m-1 cooperators are observed. If opponents defect early, you match them.
'''

description_OPPORTUNISTIC_7 = '''
**OPPORTUNISTIC THRESHOLD STRATEGY**

**Core Decision Rule:**

Defect by default. Cooperate only in specific tactical windows where cooperation is necessary to secure the reward.

Maintain a running estimate of opponent cooperation tendency: `avg_coop = (cumulative cooperators observed so far) / (cumulative opponent-rounds observed so far)`

In round t ∈ {1, ..., r-1}, decide as follows:

```
expected_cooperators = avg_coop × (n - 1)

if expected_cooperators < m:
    COOPERATE
else:
    DEFECT
```

In the final round r:
```
DEFECT (always)
```

**Edge Cases:**

*First round (no history):* DEFECT. No empirical basis to estimate cooperation rates; assume worst-case free-riding among opponents.

*Rounds 2 to r-1 with insufficient data:* Use the observed cooperation rate from previous rounds. If fewer than m-1 opponents cooperated in the prior round, shift to COOPERATE in the current round to hedge against threshold failure.

*Penultimate round (t = r-1):* Apply the standard decision rule. In the final round, always DEFECT regardless of observations—no future consequences.

*Rounds where coordination appears broken:* If observed cooperation consistently stays below m-1 for three consecutive rounds, switch to DEFECT permanently. The collective project has failed, and further investment is wasted.

**Opportunistic Mechanics:**

- Rides free on the efforts of approximately m-1 others by defaulting to defection whenever safe
- Contributes only when the math suggests others will fall short of the threshold, ensuring you capture the k reward without excess cooperation
- Abandons cooperation entirely in round r, avoiding a sucker's payoff in the final round
- Exploits asymmetry by letting the burden of cooperation fall on those with higher intrinsic cooperation propensities while protecting your endowment
'''

description_OPPORTUNISTIC_8 = '''
# Opportunistic Threshold Rider

## Core Principle
Free-ride whenever possible. Cooperate only when defection directly prevents the threshold from being met and you can afford the cost.

## Decision Rules

**Round 1:**
- Action: Defect
- Rationale: No history exists. Assume others may cooperate; observe their behavior before committing endowment.

**Rounds 2 to r-1 (Middle Rounds):**

Calculate the observed cooperation rate:
```
avg_coop_rate = (sum of opponents' cooperators in previous rounds) / 
                (number of previous rounds × (n-1))
```

Then:
- If `avg_coop_rate >= m / (n-1)`: **Defect**
  - Threshold will likely be met regardless; free-ride and take 1 + k
  
- If `avg_coop_rate < (m-1) / (n-1)`: **Defect**
  - Even your cooperation cannot raise expected cooperators to m; don't waste the endowment
  
- If `(m-1)/(n-1) <= avg_coop_rate < m/(n-1)`: **Cooperate if** `most_recent_observed + 1 >= m`, else **Defect**
  - The threshold is borderline reachable. Cooperate only if the previous round's observed count plus you equals m or more. Otherwise, the threshold is unachievable and defection dominates.

**Round r (Final Round):**
- Action: Defect
- Rationale: Terminal round; no future payoff from building cooperation. Free-ride on any threshold that occurs.

## Edge Cases

**Early collapse in cooperation:** If `avg_coop_rate` falls below `(m-1)/(n-1)` after any round, shift permanently to **Always Defect** for all remaining rounds. The game's collective threshold is now unachievable.

**Threshold instability:** If the observed count fluctuates around m (moving between m-1 and m+1), apply a moving average over the last 3 rounds instead of cumulative average to reduce noise in expectations.

**Minimum viable strategy:** If at any point you observe that m cooperators have just occurred in the previous round and you defected, maintain defection—you just secured 1 + k. Continuation of defection assumes others will repeat or stabilize at similar cooperation levels.
'''

description_OPPORTUNISTIC_9 = '''
# Opportunistic Threshold Exploitation Strategy

**Core Principle:** Default to defection to maximize private payoff, and cooperate only when you are the pivotal player who can unblock future free-riding opportunities.

## Decision Rules

**Round 1 (Initial):**
Defect. Without historical information, assume other players will be mixed. Establish a baseline of non-contribution.

**Rounds 2 to r−1 (Middle Rounds):**
- Let c = number of cooperators observed in the previous round
- If c ≥ m: **Defect** (threshold was met; free-ride on others' cooperation and receive 1 + k)
- If c = m − 1: **Cooperate** (you are the pivotal player; by cooperating, you unlock the reward for yourself and all others in this round, and their willingness to cooperate may persist next round, enabling future free-riding)
- If c < m − 1: **Defect** (the collective will fail regardless; no benefit to sacrificing your endowment)

**Round r (Final Round):**
Defect unconditionally. There is no future to exploit, so maximize immediate payoff. The cost of cooperation cannot be recovered through future free-riding.

## Edge Cases

**If c_t = m:** Defect (you already have the reward without paying).

**If the game has only r = 2 rounds:** In round 1, still defect (gather information). In round 2, follow the final-round rule (defect).

**If m = n:** Cooperation is collectively required. Still defect in round 1, pivot cooperate only when m − 1 others have demonstrated cooperation in the prior round, and defect in the final round.

**If m = 2 and n = 3:** Pivoting occurs frequently. Cooperate whenever exactly one other cooperator appeared last round; otherwise defect.

## Opportunistic Alignment

This strategy embodies opportunism by:
- **Defaulting to self-interest:** You keep your endowment unless you control the outcome.
- **Exploiting others' cooperation:** You rely on reaching the threshold through others' contributions, then capture the reward without cost.
- **Ceasing cooperation at the end:** You provide no "insurance" in the final round, maximizing short-term extraction.
- **Strategic pivoting:** You cooperate only when you directly enable future rounds of free-riding, not out of reciprocity or fairness.
'''

description_OPPORTUNISTIC_10 = '''
# Opportunistic Threshold Strategy

## Core Decision Rule

In each round t (except the last), cooperate if and only if the estimated number of cooperators falls below a critical threshold. Otherwise, defect opportunistically to free-ride.

**Calculate expected cooperators:**
- Let `avg_coop` = average cooperation count observed in all previous rounds
- Estimate `expected_cooperators = avg_coop + (remaining_opponents - 1) * (observed_cooperation_rate)`

**Defection condition:**
- Defect if `expected_cooperators ≥ m + buffer`
- Cooperate if `expected_cooperators < m + buffer`
- Set `buffer = ceiling(sqrt(n))` to account for noise and defection risk

## Round-Specific Behavior

**Rounds 1 to r-1 (Early and Middle Rounds):**
Apply the threshold rule above. If no history exists (round 1), assume `avg_coop = m` and use the defection rule — this seeds with optimism about others meeting the threshold.

**Round r (Final Round):**
Defect unconditionally. Since no future payoff exists, there is no value to cooperation. Free-ride on whatever threshold state the history has established. If the threshold is already met, gain the extra point. If not met, your defection has no downside (you don't make it worse).

## Adaptation Mechanism

After each round, update:
- `observed_cooperation_rate = (total_cooperators_seen) / ((t-1) * (n-1))`
- Use this rate to predict next round's cooperation count
- If observed rate is rising, become more aggressive with defection
- If observed rate is falling below critical level `m/(n-1)`, become more conservative

## Edge Cases

- **Round 1:** Use `avg_coop = m` (neutral assumption). Defect if `m + buffer < m`, which is false, so cooperate with probability proportional to `1/(k)` — defect if `k` is very large (easy threshold, likely met). For simplicity: defect if `n` is large relative to `m` (threshold easily hittable).

- **Degenerate m:** If `m = 1`, always defect (you alone cannot reach threshold, so free-ride). If `m = n`, always cooperate (threshold impossible without you).

- **Confidence interval:** If `t = 1` or sample size is very small, use a wider buffer `2 * ceiling(sqrt(n))` to hedge against randomness.

This strategy opportunistically exploits high cooperation environments (defect when threshold assured) while prudently cooperating in fragile environments (when cooperation is rare, ensure threshold via own contribution).
'''

description_OPPORTUNISTIC_11 = '''
# Greedy Threshold Opportunism

**Core Logic:** Minimize personal cost while capturing rewards by free-riding on others' cooperation, but contribute only at critical tipping points where your cooperation directly enables the threshold.

## Round 1
DEFECT. No prior information exists. Assume others might contribute; exploit their potential cooperation for free.

## Rounds 2 through r (including final round)
Observe c_prev = number of cooperators in the immediately preceding round.

**Decision rule:**
```
if c_prev >= m:
    DEFECT
    // Threshold already met. Reward k secured without paying cost.
    // Pure free-riding.

else if c_prev == m - 1:
    COOPERATE
    // Exactly one short of threshold.
    // Your contribution: -1 (cost) + k (reward) = k - 1 > 0 (net positive)
    // You become the pivotal player; exploit this moment.

else:  // c_prev < m - 1
    DEFECT
    // Gap too wide. Even your cooperation fails to reach m.
    // Paying 1 yields only 0 payoff (threshold not met).
    // Defect is strictly better.
```

## Rationale for Opportunism
- **Exploit abundance:** When threshold is met, you receive k without contributing—pure opportunism.
- **Avoid waste:** Never pay 1 to achieve a outcome worth 0.
- **Exploit pivotality:** Cooperate only when you are the decisive margin, making your cost unavoidable and justified.
- **No sentiment:** Indifferent to others' defection patterns. React only to aggregate counts, not to morality or reputation.
- **Stable final round:** The last round contains no dynamic incentives, so apply identical myopic logic.

This strategy requires no complex history tracking, no coordination assumptions, and works against any opponent distribution: defectors, cooperators, or mixed strategies.
'''

description_OPPORTUNISTIC_12 = '''
# Opportunistic Collective Risk Strategy

**Core Philosophy:** Maximize personal endowment by defecting whenever the threshold is achievable without your contribution. Cooperate minimally and only when necessary to maintain the bonus stream.

## Decision Rules

**Last round (t = r):**
Always play D. No future rounds mean no future benefit from cooperation. Pocket the endowment and any bonus already locked in.

**First round (t = 1):**
Play D. Establish yourself as a defector, gather baseline information on opponent behavior, test whether a threshold will form without you.

**Subsequent rounds (1 < t < r):**

Let `opp_coop` = number of opponents who played C in round t-1.

1. **If opp_coop ≥ m - 1:** Play D
   - The threshold is met or will be met without you. Free-ride: claim the bonus while keeping your endowment.

2. **If opp_coop = m - 2:** Play C
   - You are one cooperator away from the threshold. The cost of cooperating (lose endowment) is outweighed by the near-certain bonus payoff next round. This is efficient exploitation: contribute just enough to trigger the threshold, securing k for both this and future rounds if the pattern holds.

3. **If opp_coop < m - 2:** Play D
   - The threshold is far away. Cooperating would be wasteful. Continue defecting to observe whether cooperation grows or collapses. If cooperation never reaches m-1, you've avoided all contribution costs.

## Edge Cases

- **If rounds_remaining = 1:** Override to always D (last-round exception).
- **If m = n (all players must cooperate):** This strategy will defect until round r-1. Expect no bonuses unless a cooperative equilibrium somehow emerges early, which this strategy discourages. Accept this outcome as opportunistic: you lose the bonus but avoid paying in a coordination-impossible scenario.
- **If m = 2 and n is large:** Play D always except when exactly one opponent cooperated last round, then play C to lock in the bonus cheaply.

## Opportunistic Logic

This strategy prioritizes preserving your endowment (the 1) over claiming the bonus (k). You only sacrifice the endowment when cooperation is already nearly-sufficient, turning others' contributions into your bonus without bearing the cost. In the end game, you defect unconditionally. Against cooperative opponents, you exploit them. Against defectors, you defect in parallel and minimize losses.
'''

description_OPPORTUNISTIC_13 = '''
# Opportunistic Threshold Monitoring Strategy

**Core Decision Rule:**

Maintain a running estimate of opponent cooperation rates. In each round, estimate the expected number of cooperators among your n-1 opponents based on historical observation. Then:

1. If expected_cooperators ≥ m: **DEFECT**
   - The threshold will likely be met regardless of your action. Free-ride by keeping your endowment and capturing the reward k.

2. If m-1 ≤ expected_cooperators < m: **COOPERATE**
   - The group is close to the threshold but may fall short without your contribution. Cooperate to push past m and secure the reward, converting a loss (0+0) into a gain (0+k).

3. If expected_cooperators < m-1: **DEFECT**
   - Cooperation is too weak to reach the threshold even with your help. Defect to preserve your endowment.

4. If round t = r (final round): **ALWAYS DEFECT**
   - No future rounds, so no benefit to maintaining cooperation norms. Extract maximum value by defecting.

**Estimation Rule:**

expected_cooperators = round(avg_coop_rate × (n-1))

where avg_coop_rate is the proportion of opponents observed cooperating in all previous rounds, weighted toward recent history:

avg_coop_rate = (Σ(c_t / (n-1)) × decay_weight(t)) / Σ(decay_weight(t))

Use exponential decay: decay_weight(t) = 0.8^(current_round - t), giving recent rounds higher influence.

**First Round:**

With no history, set expected_cooperators = round(n × 0.5). Apply the decision rule above. Defect if uncertain.

**Rounds 2 to r-1:**

Update the running average after each observed result. Recompute expected_cooperators and apply the decision rule.

**Adaptive Tuning:**

If observed cooperation is consistently above or below historical norms, weight the most recent 3 rounds twice as heavily in the moving average to detect regime shifts.
'''

description_OPPORTUNISTIC_14 = '''
LEAN FREE-RIDER STRATEGY

**Core Logic:**
Minimize personal contribution by defecting whenever possible. Cooperate only when you are the marginal player needed to reach the threshold, exploiting others' cooperation to secure the reward bonus.

**Decision Rule by Round:**

*Round 1:*
DEFECT — no historical information; exploit with a defection to test cooperation levels.

*Rounds 2 through r-1 (interim rounds):*
- Let C_prev = number of cooperators observed in round (t-1)
- If C_prev ≥ m: DEFECT
  - Threshold already met without you; free-ride and capture bonus
- If C_prev = m - 1: COOPERATE
  - You are the decisive player; cooperate to reach threshold
- If C_prev < m - 1: DEFECT
  - Threshold unachievable; no benefit to contributing

*Round r (final round):*
- Apply the same rule as interim rounds
- No future rounds to consider; pure payoff maximization applies identically

**Handling Variability in Cooperation:**

If cooperation fluctuates across rounds and the previous round is unreliable:
- Maintain a running average of cooperation from all previous rounds: avg_coop = mean(C_t for t < current round)
- Use avg_coop instead of C_prev in the decision rule
- Tie-breaking: if avg_coop is close to m or m-1, round down (favor defection)

**Edge Cases:**

- If m = n (all must cooperate): DEFECT every round after round 1, since any single defection in prior rounds makes threshold impossible; once impossible, no benefit exists to cooperating.
- If m = 1 (threshold always reachable): DEFECT every round; the threshold is guaranteed regardless of your action.
- Rounds 2+ where C_prev is unknown or ambiguous (e.g., first round with no prior history): DEFECT as default.
'''

description_OPPORTUNISTIC_15 = '''
## Adaptive Exploitation Strategy

**Decision Rule by Round Type:**

**Initial Rounds (rounds 1 to r-2):**
- Track the number of cooperators observed in the previous round
- DEFECT if previous round had ≥ m cooperators (free-ride on meeting threshold)
- DEFECT if previous round had < m cooperators (threshold won't be met anyway, so capturing your endowment is rational)
- Exception: If cooperation count is trending sharply downward (falls below m-2) AND you're in early-to-mid game, remain in defection (recovery is unlikely)
- **First round special case:** DEFECT unconditionally (baseline action to gather information about opponent cooperation levels)

**Penultimate Round (round r-1):**
- If observed cooperators ≥ m in round r-2: DEFECT
- If observed cooperators < m in round r-2 but ≥ m-2: Consider the probability that others will adjust upward in the final round. Maintain DEFECT (you capture the spread 1+k vs k)
- If observed cooperators < m-2: DEFECT (cooperation collapse is likely)

**Final Round (round r):**
- DEFECT unconditionally. No future rounds exist, so the endowment (value 1) is strictly better than the uncertain reward, and defecting dominates whether the threshold is met or not.

**Opportunistic Logic:**

This strategy prioritizes capturing individual payoff whenever the collective threshold appears secure or unattainable. You systematically defect to avoid the cost of contribution (c_i = 1) while harvesting the reward (k) if others meet the threshold. You only avoid defection if forced by final-round incentives, which never arise here. The strategy exploits the asymmetry that others' cooperation benefits you at zero cost, while your defection costs you nothing but still yields the reward whenever m-1 others cooperate.
'''

description_OPPORTUNISTIC_16 = '''
# Opportunistic Threshold Strategy

**DECISION RULE BY ROUND:**

**Round 1:**
Defect. With no history, assume opponents are similarly self-interested. Free-riding costs nothing and reveals opponent behavior without commitment.

**Rounds 2 to r-1 (Middle rounds):**
Let c_{-i} = observed number of cooperators among the n-1 opponents in the previous round.

- If c_{-i} ≥ m-1: **Defect**
  - Threshold met or achievable without your contribution. Free-ride and collect payoff 1+k.

- If c_{-i} = m-2: **Cooperate**
  - Threshold is one cooperator away. Cooperation here guarantees the k reward, and you secure payoff k rather than risking payoff 1 (if threshold fails). This is the sweet spot: minimal risk to obtain the reward.

- If c_{-i} < m-2: **Defect**
  - Threshold requires more than one additional cooperator. Assuming opponents are similarly opportunistic (not coordinating to save you), cooperation alone won't close the gap. Avoid the cost of contributing without a reasonable expectation of reaching m.

**Round r (Final round):**
Defect unconditionally. No future rounds exist to punish defection or reward cooperation. The marginal benefit of the k reward is overridden by the immediate payoff of keeping 1.

**EDGE CASES:**

- If m = n (all must cooperate): Rounds 2 to r-1 become almost pure defection since c_{-i} can never reach m-1. Cooperate only if c_{-i} = n-2. Round r still defaults to defect.

- If m = 2 and n ≥ 3: Many rounds trigger the m-2 threshold, producing occasional cooperation mid-game while maintaining opportunistic defection elsewhere.

- Ties in cooperation (e.g., c_{-i} exactly equals thresholds): Apply rules as stated—no randomization required.

**LOGIC:**

This strategy exploits asymmetries in the payoff structure: 1+k is the highest outcome (defect while others cooperate), k is acceptable (cooperate when threshold locks in), and 1 is the fallback (defect and take the sure payoff). By defecting in round 1 and the final round, and only cooperating when the threshold is tractably close in middle rounds, the strategy maximizes individual returns while avoiding cooperation costs when the threshold is unreachable or already guaranteed.
'''

description_OPPORTUNISTIC_17 = '''
# Opportunistic Threshold-Riding Strategy

**Core Principle:** Defect whenever the threshold appears secured by others' cooperation; cooperate minimally to prevent threshold failure.

## Decision Rules

**Historical Tracking:**
Maintain a running count of total cooperators observed across all previous rounds.

```
cooperation_history = list of {cooperators_in_round_t for t = 1 to current_round - 1}
estimated_cooperation_rate = mean(cooperation_history) / n
expected_cooperators_next = estimated_cooperation_rate * (n - 1)
```

**Standard Round Decision (rounds 2 to r-1):**
```
if expected_cooperators_next >= m:
    DEFECT (free-ride on others' threshold achievement)
else if expected_cooperators_next >= m - 1:
    COOPERATE if ceiling(m) - expected_cooperators ≥ 1
    else DEFECT (test if threshold holds without you)
else:
    COOPERATE (threshold at risk; stabilize it)
```

**First Round:**
DEFECT. Test the cooperation baseline without investing. If others cooperate sufficiently, you've identified free-riding opportunity.

**Last Round (round r):**
```
if expected_cooperators_next >= m:
    DEFECT (no future rounds to rebuild reputation)
else if expected_cooperators_next == m - 1:
    DEFECT (let others decide; their decision determines threshold)
else:
    COOPERATE only if (m - expected_cooperators_next) == 1
    else DEFECT (threshold unachievable anyway)
```

## Edge Cases

**Insufficient history (rounds 1-2):** Use a conservative estimate. Round 2: assume opponents mirror your round 1 observation. If ≥ m cooperators observed, defect round 2.

**Zero cooperators observed:** Defect in subsequent rounds until evidence emerges. Threshold failure is inevitable; do not waste contribution.

**Cooperation rate = m/n exactly:** Apply a decay heuristic—cooperate with probability 0.4 to test whether others are committed, shifting to defection if threshold holds.

**Final two rounds with high cooperation:** Defect both rounds; the strategy is already committed to threshold achievement.

## Opportunistic Alignment

This strategy exploits the asymmetry between private payoff (1) and risk premium (k). You extract k without bearing the cost when others reliably cooperate. Contribution is purely instrumental—deployed only when threshold failure becomes probable, then retracted at the first sign of safety. Defection is the default; cooperation is the exception.
'''

description_OPPORTUNISTIC_18 = '''
OPPORTUNISTIC ADAPTIVE STRATEGY

**Round 1:**
Defect. No information available; free-riding maximizes first-round payoff.

**Rounds 2 to r-1 (Intermediate Rounds):**

Observe c_prev = number of opponents who cooperated in the immediately preceding round.

- If c_prev ≥ m: Defect
  - Threshold can be met without your contribution. Free-ride.
  
- If c_prev = m - 1: Cooperate
  - You are the marginal cooperator. Your contribution determines success. Pivotal situation: cooperating yields k, defecting yields 1. Cooperate.
  
- If c_prev < m - 1: Defect
  - Even with your cooperation, the threshold cannot be met. Keep your endowment.

**Round r (Final Round):**
Defect unconditionally. No future rounds exist; the future-payoff consideration that makes cooperation pivotal in middle rounds vanishes. Defecting dominates: it yields either 1 (failure) or 1 + k (if others reach threshold), always superior to cooperating.

**Edge Case Handling:**

- If m = 1: You are always pivotal in rounds 2-r-1. Cooperate in all middle rounds; defect in round 1 and round r.
- If m = n: Threshold requires universal cooperation. Defect in rounds 1 and r; in middle rounds, cooperate only if all n-1 opponents cooperated (c_prev = n-1).
- If n = 2: In middle rounds, c_prev ∈ {0,1}. Cooperate only when c_prev = m-1.

**Opportunistic Logic:**

This strategy exploits the distinction between free-rider and pivotal positions. It free-rides aggressively when others' past cooperation signals the threshold is achievable without personal cost. It participates only when its individual action is causally necessary to achieve the reward. It eliminates future discounting in the terminal round, abandoning even pivotal cooperation when no downstream payoff follows.
'''

description_OPPORTUNISTIC_19 = '''
# Opportunistic Threshold Strategy

**State Tracking:**
Maintain a count of how many opponents cooperated in each previous round. After round t, calculate p̂_t = (total opponents cooperating in rounds 1...t) / (t × (n-1)).

**Decision Rule (Rounds 1 to r-1):**

```
If t = 1:
  Cooperate if m ≤ (n+1)/2
  Defect otherwise

If t > 1:
  expected_cooperators = (n-1) × p̂_{t-1}
  
  If expected_cooperators ≥ m - 1:
    Cooperate
  Else:
    Defect
```

**Decision Rule (Round r):**
Always defect in the final round. The game has no future, so there is no value to contributing. Even if m-1 others cooperate, you gain the reward without paying the cost.

**Interpretation:**

This strategy rides on observed cooperation momentum. You cooperate only when the empirical evidence suggests enough others are already cooperating to meet the threshold—this lets you capture the k reward while contributing only when it's near-certain the project succeeds.

In round 1, you use the structural prior that if the required fraction m/n is below 50%, baseline cooperation is likely enough to justify contributing. Otherwise, you conservatively wait to see actual cooperation patterns.

The strategy is opportunistic because it reverses the natural incentive: instead of reciprocating or maintaining cooperation, you actively free-ride when conditions permit, cooperating only as a calculated bet that others will do the heavy lifting.
'''

description_OPPORTUNISTIC_20 = '''
# Opportunistic Threshold-Dependent Strategy

## Decision Rule

**Observe** the number of opponents who cooperated in the previous round: `observed_coop`.

**Calculate** the pivot condition: Would your individual cooperation bring the total to m?
- `pivot = (observed_coop + 1 ≥ m) AND (observed_coop < m)`

**Determine action**:

```
if round == 1:
  if n - 1 ≥ m - 1:
    COOPERATE  // optimistic assumption: enough others will cooperate
  else:
    DEFECT
    
else if round == r:
  if pivot AND observed_coop ≥ m - 2:
    DEFECT  // last round: never worthwhile to cooperate
  else:
    DEFECT
    
else:  // rounds 2 to r-1
  remaining_rounds = r - round
  cooperation_threshold = k / (remaining_rounds + 1)
  
  if observed_coop ≥ m - 1:
    DEFECT  // threshold met without you; free-ride
    
  else if pivot:
    cooperate_prob = observed_coop / (n - 1)  // empirical cooperation rate
    if cooperate_prob * remaining_rounds ≥ cooperation_threshold:
      COOPERATE  // others are cooperating; you're needed for threshold
    else:
      DEFECT  // others unlikely to sustain cooperation
      
  else:
    DEFECT  // you can't be pivotal; free-ride or threshold impossible
```

## Edge Cases

**Round 1**: Cooperate optimistically if threshold is plausibly reachable (n-1 ≥ m-1). This establishes a cooperative signal and tests opponent behavior.

**Final round**: Always defect. No future payoff from threshold achievement justifies the cost.

**Insufficient possible cooperators** (n < m): Always defect; threshold is impossible.

**Perfectly coordinated opponents** (all cooperated every round): Continue defecting to extract maximum payoff per round.

## Opportunistic Mechanics

This strategy exploits three mechanisms:

1. **Free-riding**: Defect whenever the threshold will be met without you (observed_coop ≥ m-1). Extract the reward while preserving endowment.

2. **Strategic necessity**: Cooperate only when you are **pivotal**—your contribution alone completes the threshold. This minimizes contribution costs while maximizing your chances of receiving k.

3. **Decay as rounds end**: Cooperation becomes strictly irrational in the final round. Adjust mid-game cooperation probability upward if opponents show sustained cooperation, downward if they defect frequently, exploiting the revealed cooperation tendency.

The strategy is responsive to aggregated opponent behavior but defection-biased: cooperate defensively only when required to unlock the group reward.
'''

description_OPPORTUNISTIC_21 = '''
# Opportunistic Threshold Strategy

## Core Decision Rule

After each round, observe the count C of opponents who cooperated. In the subsequent round, make a binary choice:

**If C ≥ m − 1:** Defect  
(Threshold will be met without your contribution; free-ride on others' cooperation)

**If C = m − 2:** Cooperate  
(You are the marginal cooperator; your contribution completes the threshold and yields k)

**If C < m − 2:** Defect  
(Threshold unlikely to be achieved regardless; preserve private payoff)

## First Round

Defect. With no prior history, assume zero cooperators observed (C₀ = 0). Since 0 < m − 2, default to defection.

## Last Round (Round r)

Apply the same decision rule as any other round based on C_{r−1}. Do not alter behavior—reputation is irrelevant, and the payoff logic is identical.

## Boundary Adaptations

**If m = 2** (only need one other cooperator): The condition "C = m − 2" becomes "C = 0." Only cooperate if zero opponents cooperated in the prior round, otherwise defect.

**If m = n** (all must cooperate): Never cooperate (threshold impossible if any opponent defects). Always defect and capture private payoff of 1.

## Logic

The strategy exploits asymmetry: you receive the reward k if the threshold is met, regardless of whether you paid the cost. Defect whenever others' observed behavior indicates the threshold will pass without your contribution. Cooperate only when your single contribution is the difference between collective success and failure—the moment where adding yourself makes k achievable. In all other states, extract private payoff. This minimizes cooperation costs while capturing public goods benefits opportunistically.
'''

description_OPPORTUNISTIC_22 = '''
# Opportunistic Threshold Strategy

**Core Logic:**
Estimate the expected number of cooperators among your opponents in the current round. Defect whenever you can secure the reward k without personally contributing. Only cooperate when your contribution is necessary to reach the threshold, and only if doing so pays better than defecting.

**Decision Rule:**

1. **Estimate opponent cooperation rate**: Calculate the proportion of cooperators you observed in the past 3 rounds. If insufficient history, assume 50%.

2. **Compute expected cooperators among opponents**: `E[C_others] = (n - 1) × observed_cooperation_rate`

3. **Decision threshold**:
   - If `E[C_others] ≥ m - 1`: **DEFECT**
     - The reward threshold will likely be met without you. Free-ride.
   - If `E[C_others] = m - 2`: **COOPERATE**
     - You are potentially pivotal. Your cooperation reaches m total. Payoff k > payoff 0.
   - If `E[C_others] < m - 2`: **DEFECT**
     - Threshold unreachable even with your contribution. No point paying.

4. **Last round (t = r)**: **ALWAYS DEFECT**
   - No future punishment. Extract maximum value: get k reward without cost if others cooperate.

**Edge Cases:**

- **Round 1**: Use cooperation_rate = 0.5 as prior (assume symmetric expectations).
- **Rounds 2–3**: Weight recent observations 60%, prior 40%.
- **Rounds 4+**: Use full observed window of last 3 rounds.
- **Ties in estimates**: If `E[C_others]` is exactly `m - 1.5`, round down and defect (favor opportunism).

**Adaptation**:
If you observe sustained high cooperation (>70% over last 3 rounds), maintain defection to exploit it. If cooperation collapses below 30%, defect as threshold becomes unreachable. Recompute estimates after every round.
'''

description_OPPORTUNISTIC_23 = '''
# CONDITIONAL FREE-RIDER STRATEGY

**Round 1 (Information Gathering):**
Defect. Use this round to establish a baseline on opponent cooperation without risking payoff.

**Rounds 2 to r-1 (Adaptive Exploitation):**

1. Calculate empirical cooperation rate:
   - Let c_t = total number of cooperators observed in round t
   - Let p_obs = (Σ c_t from all previous rounds) / (number_of_rounds_elapsed × (n-1))

2. Estimate expected cooperators among the n-1 opponents in the current round:
   - exp_coop = p_obs × (n-1)

3. Decision rule:
   - **If exp_coop ≥ m:** Defect (threshold highly likely met; free ride on others)
   - **If exp_coop ≥ m - 1 AND exp_coop < m:** Cooperate with probability (exp_coop - (m-1)) / 1, else defect (you may be pivotal; calculate expected value)
   - **If exp_coop < m - 1:** Defect (threshold unlikely; minimize losses)

4. Alternative simplified version (more aggressively opportunistic):
   - If exp_coop ≥ m - 0.5: Defect
   - Else: Defect
   - (This captures: "Only cooperate if you're mathematically necessary AND the history strongly suggests others will cooperate")

**Final Round r (Absolute Exploitation):**
Defect unconditionally. No future rounds mean future payoffs are zero; past cooperation is sunk. Capture maximum immediate payoff.

**Edge Case - Very Low Cooperation Observed:**
If p_obs rounds to 0 or near 0 after round 2, defect all remaining rounds. The population is non-cooperative; there is no threshold to free ride on.

**Tiebreaker (Fractional Expected Values):**
When exp_coop falls between m-1 and m, use probabilistic cooperation: cooperate with probability equal to the fractional excess above m-1 to break indifference.
'''

description_OPPORTUNISTIC_24 = '''
**OPPORTUNISTIC THRESHOLD STRATEGY**

**Round 1:**
Defect. Probe the environment without committing resources. Observe c₁ (number of cooperators among opponents).

**Rounds 2 through r-1 (Adaptive phase):**
Let c_{t-1} = observed cooperators in round t-1.

```
if c_{t-1} >= m:
  Action = Defect
    Rationale: Threshold already met; exploit the +k bonus without endowment cost
  
elif c_{t-1} == m-1:
  Action = Cooperate
    Rationale: You are the potential marginal player; contributing reaches threshold
    Expected payoff: 0 + k = k (guaranteed bonus if you're the deciding cooperator)
    Defecting would give: 1 + k only if others maintain cooperation
  
else (c_{t-1} < m-1):
  Action = Defect
    Rationale: Threshold too distant; your cooperation alone insufficient to reach m
    Contributing wastes endowment for unachievable bonus
```

**Round r (Final round):**
Defect unconditionally, regardless of c_{r-1}.

Rationale: Terminal round offers no future leverage. If threshold already met, exploit the bonus. If not met, cooperation cannot create future benefit.

**Edge case handling:**

- If all opponents defect consistently (c_t = 0 for all t): Continue defecting. The environment is purely defective; cooperation yields no bonus.
- If cooperation stabilizes above m: Settle into perpetual defection, harvesting the k bonus each round.
- If cooperation drops from m-1 to m-2 mid-game: Switch from cooperating to defecting. The threshold becomes unachievable even with your contribution.

The strategy prioritizes personal payoff by free-riding when others meet the threshold, contributing only when your action is the marginal difference between failure and success.
'''

description_OPPORTUNISTIC_25 = '''
# Pivotal Threshold Exploitation Strategy

**Core Logic:** Defect by default. Cooperate only when you are mathematically pivotal to reaching the threshold—when you expect exactly m-1 other players to cooperate this round.

## Decision Rule

Maintain a running estimate of opponent cooperation:
- Track the number of cooperators observed in each previous round
- Compute `avg_coop`: moving average of cooperators among the other (n-1) players across all completed rounds

For round t (t > 1):
```
expected_opponent_cooperators = floor(avg_coop × (n-1))

if expected_opponent_cooperators == m - 1:
  play C  (you are pivotal; securing k outweighs the endowment loss)
else:
  play D  (threshold is either unachievable or already secured without you)
```

For round 1 (no history):
- Play D (test opponent behavior; assume others will not coordinate without signals)

For round r (final round):
- Apply the same decision rule; no incentive to deviate

## Recency Weighting (optional refinement)

If opponent behavior is non-stationary, weight recent rounds more heavily:
```
avg_coop = weighted mean of cooperator counts, with exponential decay favoring recent rounds
decay_weight(t) = λ^(current_round - t) for parameter λ ∈ (0.7, 0.9)
```

## Exploitation Mechanism

- **Rounds where others cooperate consistently:** Free-ride every round except when exactly m-1 cooperators appear (rare).
- **Rounds where others defect:** Identify if your single contribution could be pivotal; if not, defect.
- **Adaptivity:** The moving average adjusts as you observe shifting cooperation patterns, so you respond to changes in opponent strategy.

## Edge Cases

- **Threshold unachievable:** If even n-1 cooperators < m, you defect (impossible to hit threshold).
- **Threshold oversupply:** If expected opponent cooperators ≥ m, you defect and free-ride.
- **Exact tie:** If historical data is sparse, default to defect until avg_coop stabilizes.
'''

description_OPPORTUNISTIC_26 = '''
**OPPORTUNISTIC THRESHOLD-TRACKING STRATEGY**

**Round 1:**
Defect. No history exists; use the safe baseline to secure 1 point.

**Rounds 2 to r-1 (Middle rounds):**
- Track c_prev = count of cooperators observed in the immediately preceding round
- If c_prev ≥ m - 1: Defect
  - Threshold will be met with high probability; free-ride for payoff 1 + k
- If c_prev = m - 2: Defect
  - Only one additional cooperator needed beyond what was observed; too risky to cooperate. If others follow your precedent and defect, threshold fails. Secure 1 instead.
- If c_prev < m - 2: Defect
  - Threshold is far from met. Cooperating costs 1 with minimal probability of recovery; defection gives 1 regardless.

**Round r (Final round):**
Defect unconditionally. No future payoffs exist; cooperation has zero strategic value. Secure 1.

**Tiebreaker for uncertainty within each condition:**
If you observe exactly m - 1 cooperators in a prior round, defect. This is the edge case where the threshold was met last round but could fail if cooperation rates drop. Assume others will follow a similar defecting pattern and shift to free-riding mode.

**Intuition:**
The strategy exploits the asymmetry in payoffs: cooperation costs 1 to unlock k, but defection yields 1 + k when others unlock the threshold. By tracking past cooperation counts, you identify rounds where the threshold is effectively guaranteed (others will carry it) and you can safely extract maximum payoff. You never cooperate speculatively because aggregate history reveals whether cooperation is already sufficient—if it is, free-ride; if it isn't, defection's security beats cooperation's gamble.
'''

description_OPPORTUNISTIC_27 = '''
# Adaptive Free-rider Strategy

**Core Principle**: Defect by default. Cooperate only when others have demonstrated sufficient commitment to reach the threshold without requiring continuous personal contribution.

## Decision Rules

**Cooperate if and only if**: In the immediately preceding round, you observed exactly `m-1` cooperators among your `n-1` opponents.

**Otherwise**: Defect.

## Pseudocode

```
if round == 1:
    action = D
else:
    if (cooperators_observed_last_round == m - 1):
        action = C
    else:
        action = D
```

## Edge Cases

**First Round**: Defect. You have no history to indicate whether others will cooperate, so you observe their behavior.

**Last Round**: Defect. The threshold matters only within rounds; your contribution in round r has no bearing on future rounds, so free-ride maximally.

**Rounds 2 through r-1**: Apply the threshold rule strictly. If you observed m-1 cooperators last round, you know that exactly your cooperation will trigger the reward. You cooperate to ensure the payoff k rather than 0, while benefiting from the triggered k immediately next round when others likely repeat their behavior.

## Opportunistic Logic

- **Free-riding baseline**: Defect whenever possible to secure 1+k instead of k when the threshold succeeds, or avoid wasting contribution when it fails.

- **Selective cooperation**: Only contribute when you have confidence that others' commitment level (m-1 observed) makes your contribution decisive and sufficient. This minimizes your own cooperation cost.

- **Dynamic adaptation**: Adjust based on observed cooperation levels. If cooperation drops below m-1, you permanently defect (threshold unachievable). If cooperation stabilizes at m-1, you maintain the minimal cooperation pattern that sustains the payoff.

- **Self-reinforcing exit**: If opponents defect against you or if cooperation erodes, you defect entirely, shifting to universal defection equilibrium where you receive steady payoff 1.
'''

description_OPPORTUNISTIC_28 = '''
## Opportunistic Threshold-Based Strategy

**State Tracking:**
Maintain a running estimate of opponent cooperation rate: p̂ = (total cooperators observed across all rounds) / (total opponents × rounds completed)

**Decision Rule:**

For round t ∈ {1, ..., r}:

1. **First round (t = 1):** Defect. You have no information about opponent behavior; defection extracts maximum value if others cooperate.

2. **Middle rounds (1 < t < r):** 
   - Calculate the probability that at least m-1 opponents will cooperate using observed rate p̂
   - Estimate: Pr(≥m-1 others cooperate) = Σ(j=m-1 to n-1) C(n-1,j) × p̂^j × (1-p̂)^(n-1-j)
   - Cooperate if and only if: Pr(≥m-1 others cooperate) > 1/(k-1)
   - Otherwise defect

3. **Final round (t = r):** Always defect. No future rounds remain, so the only question is whether to capture the immediate bonus by free-riding. If others cooperate, you get 1+k; if not, you get 1. Cooperation gives you at best k. Defection dominates.

**Adaptation Rule:**
After each round, update p̂ by including the observed count of cooperators. Weight recent rounds slightly higher to respond quickly to shifts in opponent behavior:
- p̂_new = (0.7 × cooperators_this_round + 0.3 × cooperators_previous_rounds) / total_observations

**Edge Cases:**
- If insufficient history exists (early rounds), use a pessimistic prior: assume p̂ = 0.3 (expect defection from others)
- If threshold 1/(k-1) is impossible to satisfy (all opponents would need to cooperate), defect unconditionally
- If k is very large, the threshold becomes very small—you'll cooperate more often; adjust by adding a patience discount for final rounds: multiply threshold by (r-t)/r to increasingly defect as endgame approaches

**Opportunistic Logic:**
Defect when opponents don't cooperate reliably enough, capture free-rider payoff (1+k) when they do, and always defect in the final round where cooperation cannot be reciprocated. Shift the threshold upward in later rounds to bias toward exploitation.
'''

description_OPPORTUNISTIC_29 = '''
# Opportunistic Threshold-Matching Strategy

**Round 1 (Initial):**
Defect. With no history, assume no reliable pattern of cooperation from others.

**Rounds 2 through r-1 (Intermediate):**
After each round, observe the number of cooperators among opponents (c_prev). Apply the following rule for the next round:

- If c_prev ≥ m: Defect (threshold met without you; free-ride on others' contribution)
- If c_prev = m-1: Cooperate (you are critical to meeting threshold; secure the bonus)
- If c_prev < m-1: Defect (threshold cannot be met even with your contribution; cooperation is futile)

**Round r (Final):**
Observe c_{r-1} from the preceding round:

- If c_{r-1} ≥ m: Defect (threshold already met; extract final benefit without cost)
- If c_{r-1} = m-1: Cooperate (you are critical; collect one last bonus)
- If c_{r-1} < m-1: Defect (futile; no benefit possible)

**Opportunistic Logic:**

This strategy exploits three asymmetries:

1. **Free-riding**: When others' cooperation guarantees the threshold, defect and capture the bonus without paying the cost.

2. **Positional leverage**: When exactly m-1 others cooperate, you become indispensable. Cooperate to guarantee the bonus you would otherwise forfeit, then return to defection once leverage is lost.

3. **Sunk-cost rejection**: Abandon cooperation immediately when the threshold becomes unattainable, regardless of previous cooperation levels. Do not waste contributions on failed rounds.

The strategy treats cooperation as transactional and contingent on observable opportunity. It maximizes individual payoff by matching contribution levels that maximize your bargaining position.
'''

description_OPPORTUNISTIC_30 = '''
OPPORTUNISTIC THRESHOLD EXPLOITATION

**Core Logic:**
Defect unless cooperation is necessary to reach the m-player threshold. Free-ride whenever possible; contribute only when the reward is at genuine risk of being lost.

**Decision Rules:**

*Round 1:*
- Action: Defect
- Rationale: No historical information. Assume the widest range of possible opponent behavior; testing with defection imposes no additional risk.

*Rounds 2 through r-1 (Middle rounds):*
- Let `others_coop` = number of other players observed to cooperate in round t-1
- Let `rounds_left` = r - t

If `others_coop >= m - 1`:
- Action: Defect
- Threshold is already met without you; maximize private payoff through free-riding.

If `others_coop == m - 2` AND `rounds_left > 1`:
- Action: Cooperate
- Exactly one more cooperator needed. You are the pivot player. Contribute to secure the reward. Only do this if mid-game (future rounds exist where cooperation norms might stabilize).

If `others_coop <= m - 3` AND `rounds_left > 1`:
- Action: Cooperate
- Threshold is fragile; absent your contribution, failure is likely. Cooperate to push over the threshold while the game is long enough to recoup the investment across remaining rounds.

Otherwise (all other cases):
- Action: Defect
- Includes: late-game stages, scenarios where threshold success is improbable, or cooperation levels that don't demand your participation.

*Round r (Final round):*
- Action: Defect
- No future rounds. The only payoff available is the private endowment. Exploit the reward if it materializes, but contribute nothing.

**Edge Case Handling:**

If round 1 and no prior history exists, defect (no basis to infer cooperation).

If `rounds_left == 1` (penultimate round observing final round ahead), treat as final round logic—defect even if `others_coop == m - 2`, because cooperation in round r-1 cannot influence round r behavior.

If `others_coop == m - 2` but `rounds_left <= 1`, defect (endgame dominates; the reward is no longer guaranteed to matter).

**Opportunistic Character:**

This strategy minimizes your own contributions while maximizing extraction of the reward when others provide it. You only cooperate at critical thresholds—when your single contribution tips the outcome from failure to success—and abandon cooperation entirely as the game concludes. You bet on others' contributions carrying the threshold when possible, and contribute only to prevent the loss of the collective reward.
'''

description_OPPORTUNISTIC_31 = '''
# Adaptive Threshold Exploitation Strategy

**Round 1**: Defect unconditionally. This is a test round to probe opponent cooperation levels without cost.

**Rounds 2 through r-1**: Observe the number of cooperators from the immediately preceding round (call this c_prev).

- **If c_prev ≥ m**: Defect. The threshold has already been met; extract the maximum payoff by free-riding on others' contributions.
  
- **If c_prev = m - 1**: Cooperate. You are exactly one cooperator short of the threshold. Your single cooperation secures the bonus for all players (including yourself) at minimal total cost. This is the break-even point where cooperation becomes strictly necessary.
  
- **If c_prev < m - 1**: Defect. The gap is too large for your individual action to restore the threshold. Others are not cooperating sufficiently; do not absorb their failure.

**Round r (final round)**: Defect unconditionally. There are no future rounds. Any cooperation now generates payoff k only in this terminal round, whereas defection generates 1 + k if others have already crossed the threshold, or 1 if they haven't. Defection strictly dominates.

**Rationale**: The strategy defaults to defection (maximum private retention) and only cooperates when it is the marginal action to unlock the collective bonus. It exploits successful cooperation by others through free-riding, abandons the group when cooperation is insufficient, and eliminates cooperation pressure entirely in the terminal round.
'''

description_OPPORTUNISTIC_32 = '''
# Opportunistic Threshold Strategy

**Decision rule for each round:**

On round 1, COOPERATE unconditionally. This establishes a baseline for observing opponent behavior.

For round t ∈ {2, ..., r}, let c_prev denote the number of other players observed cooperating in round t-1.

- **If c_prev ≥ m:** DEFECT
  - The threshold is guaranteed to be met. Extract maximum value by withholding contribution while capturing the k reward.

- **If m-1 ≤ c_prev < m:** 
  - If t = r (final round): DEFECT
    - Exploit last-mover advantage. The threshold will be met by others; pocket 1 + k.
  - If t < r (not final): COOPERATE
    - Secure threshold this round to preserve the free-riding opportunity in subsequent rounds. One contribution now enables multiple rounds of exploitation later.

- **If c_prev < m-1:** DEFECT
  - Threshold cannot be reached even with your contribution. Contributing has zero payoff benefit, so withhold.

**Edge cases:**

- If all opponents defect from round 1 onwards (c_t = 0 for all observed rounds), continue defecting—no threshold is achievable.
- If observations show exactly m-1 cooperators persistently across multiple middle rounds, switch to COOPERATE in those rounds to maintain your exploitation position while DEFECTING in the final round.
- Round r requires the most aggressive opportunism: only cooperate if your contribution is the marginal m-th player needed; otherwise defect.

**Opportunistic alignment:**

The strategy maximizes personal payoff by conditionally free-riding. Early cooperation gathers intelligence about opponent type distributions. Once you identify that m-1 or more players will reliably cooperate, you extract rent for all remaining rounds by defecting. The only cooperations after round 1 are tactical—offered when necessary to preserve future free-riding opportunities or when you are the swing vote in the final round.
'''

description_INDIVIDUALISTIC_5 = '''
# Adaptive Threshold Response Strategy

**Round 1:** Cooperate unconditionally. This establishes a baseline for learning about opponent behavior in subsequent rounds.

**Rounds 2 through r-1:** Let c denote the number of opponents observed cooperating in the immediately preceding round. Apply this decision rule:

- If c ≥ m: Defect. The threshold is already met; capture the reward k without sacrificing your endowment.
- If c = m - 1: Cooperate. Your contribution is pivotal—it determines whether the threshold is reached. Cooperating yields payoff k versus defecting's payoff of 1 + k, but the -1 cost is offset by the k reward from reaching threshold, netting you k in expectation.
- If c < m - 1: Defect. The threshold is unattainable even with your contribution. Do not sacrifice your endowment for a group outcome that will fail regardless.

**Round r (final round):** Defect unconditionally. No future rounds follow, so there is no reputational or strategic benefit to cooperation. Whether the threshold was met in previous rounds is irrelevant to round r payoffs. Defection yields at minimum 1, versus 0 guaranteed from cooperation.

**Justification of individualistic stance:** This strategy operates purely on observed aggregate counts without assuming opponent cooperation, coordination norms, or reciprocity. It treats each opponent's behavior as independent historical data and maximizes your payoff conditioned on that empirical signal. You cooperate only when you are materially necessary for threshold achievement, and you defect whenever you cannot claim credit for a public good outcome. The strategy discards any lingering cooperative posture in the final round, revealing that cooperation was always instrumental to your payoff, never moral principle.
'''

description_INDIVIDUALISTIC_6 = '''
**STRATEGY: Adaptive Exploitation Based on Cooperative Signal Detection**

**Core Decision Rule:**

Maintain a running estimate of opponent cooperation probability. Cooperate if and only if the recent cooperation rate strongly suggests the threshold m will be exceeded through others' actions alone—otherwise defect.

Let p = (observed cooperators in last round) / (n-1)

- If p ≥ (m-1)/(n-1): Defect. The threshold will likely be met without your contribution; capture the +1 private gain while claiming reward k.
- If p < (m-1)/(n-1): Defect. The threshold won't be met; preserve the +1 gain without wasting endowment.

**First Round:**
Cooperate once to generate an initial signal. This reveals whether the opponent population contains any disposition toward cooperation.

**Subsequent Rounds:**
After round 1, apply the threshold rule above. Update estimate p after each round observes the cooperator count.

**Last Round (round r):**
Defect unconditionally. No future rounds to benefit from establishing patterns. If the threshold can be met this round through others, defect and gain 1+k. If not, defect and gain 1.

**Edge Case—Threshold Uncertainty:**
When p is close to the boundary (m-1)/(n-1), use a tie-breaker: defect. The marginal benefit of your cooperation is offset by the risk that others also defect despite past observations.

**Individualistic Alignment:**
This strategy never cooperates from altruism or to sustain group welfare. Cooperation only occurs in round 1 as information extraction. All subsequent actions maximize personal expected payoff given the empirical defection incentive structure—you either free-ride on others' cooperation or avoid wasting endowment when cooperation is futile.
'''

description_INDIVIDUALISTIC_7 = '''
# Rational Free-Riding Strategy

## Decision Rules

**Core Principle**: Cooperate only when doing so maximizes personal payoff given observed opponent behavior; otherwise defect.

Maintain a tracking variable: `opponent_coop_rate` = empirical frequency of opponent cooperation observed across all previous rounds.

**For rounds 1 to r-1 (non-terminal rounds)**:

1. If `opponent_coop_rate × (n-1) ≥ m - 1`:
   - **Defect** (threshold will be met without you; free-ride and collect 1 + k instead of k)

2. Else if `opponent_coop_rate × (n-1) + 1 ≥ m`:
   - **Cooperate** (your contribution tips the threshold; you receive k instead of 0)

3. Else:
   - **Defect** (threshold unreachable; you receive 1 either way)

Update `opponent_coop_rate` after observing this round's aggregate cooperation count.

**For round r (final round)**:
- **Always defect** (no future rounds; terminal payoff maximization)

## Edge Cases

**Round 1**: Apply the decision rule with `opponent_coop_rate = 0` (no history). This produces defection, establishing a baseline of individualistic play.

**Threshold at boundary**: When `opponent_coop_rate × (n-1)` is near m-1, use strict inequality thresholds to avoid rounding ambiguity. Cooperate only when the second condition is strictly satisfied (threshold actually reachable with your contribution).

**All opponents defect persistently**: `opponent_coop_rate` remains 0; you defect every round and secure payoff 1 × r.

**All opponents cooperate persistently**: `opponent_coop_rate → 1`; condition 1 triggers immediately, and you defect for payoff (1 + k) × r, exceeding pure mutual cooperation.

## Individualistic Alignment

This strategy pursues individual payoff maximization throughout:
- Exploits others' cooperation by free-riding when the threshold is assured
- Avoids wasted contributions when the threshold is unreachable
- Conditionally cooperates only when your own participation is pivotal—a selfish calculation, not altruism
- Abandons all cooperation in the final round where future reciprocation is impossible
- Makes no assumptions about opponent benevolence or implicit coordination
'''

description_INDIVIDUALISTIC_8 = '''
**Pragmatic Pivot Strategy**

**Core Decision Rule:**
Cooperate in round t only if the observed number of cooperators in round t-1 equals exactly m-1. Defect in all other cases.

**Detailed Logic:**

Cooperate(t) ← 
  IF t = 1: FALSE [no prior observation available]
  IF t = r: FALSE [final round, always free-ride]
  IF observed_cooperators(t-1) = m-1: TRUE
  ELSE: FALSE

**Reasoning:**

The only scenario where cooperation benefits you is when your contribution is the marginal player needed to reach the threshold. If m-1 others cooperate and you cooperate, you get k (instead of 1+k if you defect), which is worse—but the alternative is failing the threshold entirely if you can't reliably predict cooperation.

However, once you observe exactly m-1 cooperators, your defection leaves them below threshold. By cooperating you become pivotal: they get k (instead of 0) and you get k (instead of 1, if threshold failed) or k (versus 1+k if they hit threshold without you). The key is that matching observed near-threshold cooperation signals increases collective success, which is worth the sacrifice.

**Edge Cases:**

- Round 1: Start defecting. No history exists; cooperating blindly has expected payoff 0 with high probability of threshold failure.
- Final round r: Always defect. No opportunity to influence future behavior or reputation. If threshold is achievable without you (≥m already cooperated), you gain an extra unit. If not, you lose nothing by defecting.
- Observed count > m: Defect. Threshold is already assured; you gain the bonus either way; defecting yields 1+k versus k.
- Observed count < m-1: Defect. Your single contribution cannot reach threshold; you'd receive 0 instead of 1.

**Individualistic Alignment:**

This strategy is self-interested throughout: you cooperate only when you are instrumentally necessary for a payoff-improving outcome, and free-ride whenever threshold success is either guaranteed without you or impossible regardless of your action. You ignore others' long-term interests or preferences for fairness.
'''

description_INDIVIDUALISTIC_9 = '''
# Strategy: Empirical Threshold Matching

**Core Decision Rule:**

Cooperate in round t if and only if the number of opponents observed cooperating in round t-1 is at least m-1. Otherwise, defect.

**Implementation:**

```
if t == 1:
    action = D
else:
    opponents_cooperated_previous_round = observed_count from round t-1
    if opponents_cooperated_previous_round >= m - 1:
        action = C
    else:
        action = D

if t == r:
    action = D  // Override: always defect in final round
```

**Edge Case Handling:**

- **Round 1:** Defect. No history exists; cooperating is a pure loss (payoff 0) without knowledge of others' behavior.
- **Rounds 2 to r-1:** Apply the threshold rule. If at least m-1 opponents cooperated in the immediately preceding round, you can reach the threshold by cooperating yourself (m total cooperators). Expected payoff from cooperation: -1 + k. Expected payoff from defection: 1. Since k > 1, cooperation yields k - 1 > 0 net gain over baseline.
- **Final round r:** Always defect. In the last round, no future play rewards cooperation. The one-shot payoff dominates: defection guarantees 1 + (conditional reward), cooperation guarantees only 0 + (conditional reward). Defection weakly dominates.

**Individualistic Rationale:**

This strategy abandons cooperation as moral behavior. It cooperates *only* when empirical evidence shows sufficient others are cooperating to make cooperation individually profitable. You respond to observed material incentives, not group welfare or fairness. If others defect, you immediately defect. If others cooperate sufficiently to cross the threshold, you exploit that cooperation for personal gain. You do not initiate cooperation, subsidize failures, or sacrifice payoff to encourage collective behavior.
'''

description_INDIVIDUALISTIC_10 = '''
## Individualistic Threshold-Response Strategy

**Decision Rule:**

Maintain a running count of how many cooperators you observed in each round. Use this to estimate whether the threshold is likely to be reached without your contribution.

**Round 1:**
Defect. You have no information about opponent cooperation rates.

**Rounds 2 through r-1 (middle rounds):**
Let C_prev = number of cooperators observed in the immediately preceding round.

- If C_prev ≥ m: Defect. The threshold was already met; free-ride.
- If m-1 ≤ C_prev < m: Cooperate. The threshold barely failed last round. You are the marginal player—your contribution could push next round over the threshold and restore the payoff bonus.
- If C_prev < m-1: Defect. Too many others defected. The collective is not meeting the threshold; assume it will continue to fail.

**Round r (final round):**
Apply the same logic as middle rounds, but with slightly increased defection bias: if C_prev = m exactly, you may defect (free-ride on those committed cooperators' final push). Only cooperate if C_prev = m-1 (you are genuinely needed).

**Rationale (Individualistic):**

You cooperate only when you are the pivotal player—when your specific contribution moves the outcome from collective failure to collective success. When others are already cooperating at or above the threshold, you maximize your gain by defecting (keep the 1, still receive k). When cooperation levels are too low, you avoid wasting your contribution on a failed initiative.

**Edge case:** If you ever observe cooperative behavior that suddenly stops, revert to defection in that round and the next, treating it as evidence that others are unreliable.

This strategy is robust because it requires no assumption about opponent rationality beyond observing their revealed behavior each round, and it never wastes contributions on lost causes.
'''

description_INDIVIDUALISTIC_11 = '''
# Individualistic Collective Risk Strategy

**Core Decision Rule:**

Defect unconditionally throughout the entire game, except conditionally cooperate in early rounds based on cooperation signal estimation.

**Detailed Strategy:**

1. **Rounds 1 to ⌈r/3⌉ (Observation Phase):**
   - Defect and observe opponent cooperation counts
   - Track the empirical frequency of rounds where observed_cooperators ≥ m - 1
   - Estimate p_success = (number of rounds with ≥m-1 cooperators) / (rounds elapsed)

2. **Rounds ⌈r/3⌉+1 to r-1 (Exploitation Phase):**
   - If p_success ≥ (m-1)/n: Defect unconditionally
     - Rationale: Threshold is frequently met by others; free-ride on their contributions
   - If p_success < (m-1)/n: Defect unconditionally
     - Rationale: Threshold rarely met anyway; cooperation won't change outcome

3. **Final Round (r):**
   - Defect unconditionally
   - Rationale: No future rounds; reputation has no value; defection strictly dominates

**Justification for Edge Cases:**

- **Round 1 with no history**: Defect (dominant strategy baseline)
- **Threshold edge case m=2, n=3**: Defect remains optimal since you gain 1 unit by not contributing while threshold is met by others' cooperation
- **If k is very large**: Defect is still preferable (gain k without cost while others pay 1 to deliver it)
- **If you're the only player**: This game structure doesn't apply; n ≥ 2

**Individualistic Alignment:**

This strategy maximizes personal payoff by:
- Never contributing your endowment (cost = 1) unless it's the only way to achieve threshold
- Exploiting others' propensity to cooperate by capturing reward k without paying cost
- Abandoning any cooperative narrative in final round
- Treating all opponents as independent sources of a public good to extract value from

The strategy is robust because defection is a dominant strategy in single-round analysis, and in the repeated setting, observing others' cooperation confirms that free-riding is optimal.
'''

description_INDIVIDUALISTIC_12 = '''
# Threshold-Responsive Defection Strategy

**Core Decision Rule:**

Cooperate only if the threshold was demonstrably met in the previous round. Otherwise defect.

```
if round == 1:
    action = DEFECT
else if round == r:
    action = DEFECT  // last round: always defect
else:
    if (cooperators_observed_last_round >= m):
        action = DEFECT  // threshold met, free-ride
    else:
        action = DEFECT  // threshold not met, don't waste endowment
```

**Explicit Decision Logic:**

- **Rounds 1 to r-1**: Defect unconditionally, except cooperate only in round t if you observed at least m cooperators in round t-1.
- **Round r (final round)**: Always defect, regardless of history.

**Edge Cases:**

- Round 1: Defect. You have no history to guide expectations; assume conservatively that others will not reliably meet the threshold.
- Rounds 2 to r-1: Defect by default. Only cooperate if the previous round showed cooperation count ≥ m, signaling that the threshold-meeting condition is stable enough to exploit via free-riding.
- Round r: Defect. No future rounds exist, so there is no value in establishing a reputation or influencing future cooperation. Extract the private endowment value.

**Individualistic Justification:**

This strategy abandons any assumption of reciprocity or shared commitment. It treats the cooperation of others as an observable signal of payoff conditions, not as a moral anchor. If the threshold is reliably being crossed, exploit it by defecting (earning 1 + k instead of k). If not, defect anyway (earning 1 instead of 0). The strategy privileges your private payoff extraction over any attempt to sustain collective success.
'''

description_INDIVIDUALISTIC_13 = '''
# Adaptive Free-Rider Strategy

## Core Decision Rule

Cooperate if and only if you are likely pivotal—that is, when you expect exactly m-1 other players to cooperate.

For each round t:
1. Calculate the empirical cooperation rate among opponents from rounds 1 to t-1
2. Estimate the expected number of cooperators among the n-1 others: exp_coop = observed_rate × (n-1)
3. Apply decision rule:
   - If exp_coop ≥ m: **Defect** (threshold met without you; earn 1+k)
   - If m-1 ≤ exp_coop < m: **Cooperate** (you are likely pivotal; cooperation shifts payoff from 0 to k)
   - If exp_coop < m-1: **Defect** (threshold unreachable; cooperation yields 0)

## Edge Cases

**Round 1 (no history):**
Defect. You have no basis to estimate opponent behavior. Defection avoids the worst outcome (cooperation at 0 if threshold fails) and tests opponent cooperation rates without cost.

**Final round (round r):**
Apply the standard decision rule without modification. No end-game discount applies.

**Tiebreaking when exp_coop is fractional:**
- If exp_coop = m - 0.5: Cooperate (more likely than not that you're pivotal)
- If exp_coop = m + 0.5: Defect (more likely than not that threshold is already met)

## Individualistic Alignment

This strategy maximizes personal payoff by:
- Seeking the highest outcome (1+k) through free-riding when the threshold is safe
- Avoiding the worst outcome (0) by never cooperating when the threshold is unreachable
- Cooperating only when your action is materially decisive—strict instrumental logic, no fairness norm

The strategy does not punish others, reward reciprocal cooperators, or attempt coordination. It simply estimates when your defection yields maximum gain and when cooperation prevents catastrophic loss.
'''

description_INDIVIDUALISTIC_14 = '''
# Greedy Threshold Strategy with Last-Round Defection

## Decision Rule

**Round 1:**
Defect. With no history, assume others are uncooperative. Playing it safe maximizes your floor payoff of 1.

**Rounds 2 through r−1:**
- If you observed at least (m−1) cooperators in the previous round: **Cooperate**
- Otherwise: **Defect**

The logic: if (m−1) others cooperated last round, the threshold was met. This signals that enough players are disposed to cooperate. Cooperating now gets you k instead of 1 when the threshold hits. If fewer than (m−1) cooperated, the threshold wasn't met anyway—you'd have gained 1 by defecting and saved 1 in endowment, so defect again.

**Round r (final round):**
Always **Defect**. No payoffs carry forward, so capture the full 1 from keeping your endowment. Cooperation yields k but costs 1, netting k−1 at best. Defection nets 1 + [threshold bonus if others hit it] with no cost.

## Edge Cases

- **If m > n−1**: Impossible for others to hit threshold without you. Defect always; you cannot be pivotal.
- **If m = 2, n = 2**: You need the other player to cooperate. Round 1 defect. Round 2: if they cooperated (observed 1 cooperator = m−1), cooperate. Otherwise defect on final round anyway.
- **Repeated threshold signals**: If you observe (m−1) cooperators for many consecutive rounds, keep cooperating—it's evidence of a stable cooperative subgroup.

## Individualistic Mindset

This strategy is self-maximizing at each step and assumes no shared norms or reciprocity. You don't invest in group success—you free-ride when it's safe (when others' cooperation is evident) and defect when it's safe (when others aren't delivering). You exploit the final round for sure payoff. You never sacrifice for uncertain coordination; you only cooperate when past observation makes cooperation materially better than defection for yourself.
'''

description_INDIVIDUALISTIC_15 = '''
# Adaptive Threshold Matching Strategy

## Decision Rule

In each round, cooperate if and only if the number of cooperators observed in the previous round was at least m-1. Otherwise defect.

```
if round == 1:
    action = DEFECT
else:
    if cooperators_last_round >= m-1:
        action = COOPERATE
    else:
        action = DEFECT
```

## Rationale

This strategy is purely responsive to observed behavior. You cooperate only when enough others cooperated in the immediately preceding round that your contribution would push the total to at least m, thereby triggering the reward k. Since cooperation costs 1, you only incur this cost when it directly produces the payoff k for everyone (including yourself). If fewer than m-1 others cooperated previously, your cooperation cannot reach the threshold, so there is no reason to pay the cost.

## Edge Cases

**Round 1:** Defect. With no history, you have no basis to expect others will cooperate at sufficient levels. Cooperating speculatively is a pure cost.

**Final round:** Apply the same rule. Even in the last round, if c ≥ m-1 others cooperated previously, cooperating still yields +k net payoff this round.

**If n and m are such that m = n:** You need all players including yourself to cooperate. Only cooperate in round 1 if you have reason to believe all others will (you don't), so defect. In later rounds, only cooperate if you observed all n-1 others cooperating—a strong signal of universal cooperation.

## Individualistic Properties

- **No altruism**: You never cooperate hoping others will respond or to teach lessons; you only cooperate when it directly benefits you.
- **No punishment**: Low cooperation by others triggers defection purely because it makes your cooperation worthless, not to punish or reshape behavior.
- **Minimal assumption about opponents**: You do not assume shared norms or reciprocity. You observe realized cooperation counts and respond to them mechanically.
- **Adaptive**: Your action adjusts to empirical evidence of how many opponents are cooperating, without requiring belief about why they cooperate.
'''

description_INDIVIDUALISTIC_16 = '''
# Individualistic Adaptive Strategy

**Core Decision Rule:**

Cooperate in round t if and only if the number of cooperators observed in round t-1 is at least m-1. Otherwise defect.

**First Round:** Defect.

**Last Round:** Defect unconditionally.

**Rationale:**

In any single round, defection yields a baseline payoff of 1, while cooperation yields 0. You only recover this difference if the collective threshold is met. Since you observe aggregate cooperation counts but cannot identify individual cooperators, your only actionable signal is whether the previous round's cooperation count was sufficient to have triggered the reward.

- If you observed ≥ m-1 cooperators last round, there is a demonstrated capacity for threshold cooperation. Cooperating now has positive expected value: if the same pattern repeats, you earn k instead of 1.
- If you observed < m-1 cooperators last round, cooperation is futile—the threshold will not be met regardless of your action. Defect to secure the private endowment.

**Last Round Exception:**

In the final round r, defect regardless of history. No future rounds exist for others to respond adaptively, so the threshold-triggered reward cannot incentivize continued cooperation. Cooperation only transfers value to others.

**Edge Case - Round 2:**

If round 1 shows few cooperators (< m-1), defect in round 2. If it shows many (≥ m-1), cooperate. This avoids locking into mutual defection prematurely if a window of cooperation emerges.

**Robustness:**

This strategy is individualistic because it:
- Never sacrifices payoff to punish or reward others
- Responds only to directly observable aggregate behavior, not intentions
- Exploits cooperation when present without moral commitment
- Defaults to defection absent evidence of reliable threshold completion
'''

description_INDIVIDUALISTIC_17 = '''
# Individualistic Adaptive Threshold Strategy

**Decision Rule by Round Type:**

**First Round:** Defect unconditionally. Gather information about opponent behavior with the safest action.

**Rounds 2 through r-1:** 
- After observing cooperator count C from the previous round:
  - If C ≥ m - 1: Defect. The threshold is achievable without your cooperation, guaranteeing payoff 1 + k.
  - If C < m - 1: Defect. The threshold cannot be met regardless, guaranteeing payoff 1.

**Final Round (round r):** Defect unconditionally. No future payoffs exist to justify cooperation.

**Rationale:**

This strategy is purely individualistic—it maximizes immediate payoff in every decision without attempting to incentivize, punish, or reward opponents. Defection is the dominant action in every state because:
- When threshold is met (with or without you): defection yields 1 + k vs. cooperation's k.
- When threshold cannot be met: defection yields 1 vs. cooperation's 0.

**Adaptation:**

The strategy adapts by reading the aggregate cooperation signal, but adaptation serves only to confirm the defection choice. Observing high cooperator counts tells you the bonus is unlocked; observing low counts tells you it is not. Either way, defection maximizes personal payoff given the outcome.

**Edge Cases:**

- Rounds with insufficient data (round 1): defer to safe defection.
- Uncertainty about opponent types: irrelevant—defection dominates all distributions.
- Opponent symmetry is not exploited or assumed; the strategy is robust to any mix of opponent strategies.
'''

description_INDIVIDUALISTIC_18 = '''
**Self-Interested Threshold Contribution Strategy**

Maintain a single state variable: p = running proportion of cooperators observed among opponents across all previous rounds. Initially p = m/n (assume threshold equilibrium).

**Decision Rule for Round t:**

Let c_other = expected cooperators among other (n-1) players = p × (n-1), rounded down.

- If c_other + 1 ≥ m: **Cooperate**
- If c_other + 1 < m: **Defect**

After each round, update: p ← (cumulative cooperators observed so far) / (cumulative opponent observations so far)

**First Round:**
Play C. This initializes the learning process and tests whether others are disposed to cooperate.

**Last Round (round r):**
Apply the same decision rule as all other rounds. Do not assume cooperation is needed or change behavior.

**Edge Cases:**

- **If p steadily approaches 0** (opponents rarely cooperate): Defect consistently thereafter. You cannot unilaterally reach the threshold.
- **If p stabilizes near 1** (opponents mostly cooperate): Cooperate consistently. Your contribution reliably completes the threshold.
- **If p hovers near m/n** (cooperation barely sustains threshold): Cooperate. Your marginal contribution is necessary.

**Individualistic Logic:**

Cooperate only when your cooperation materialially enables threshold achievement. Do not cooperate to "help others" or from altruism. Abandon cooperation if empirical evidence shows others will not meet their side. Defection in low-cooperation environments is not betrayal—it is rational resource preservation.
'''

description_INDIVIDUALISTIC_19 = '''
**PAYOFF-MAXIMIZING ADAPTIVE STRATEGY**

**State Tracking:**
Maintain two variables across rounds:
- `successes`: count of rounds where ≥ m total cooperators were observed
- `last_cooperation_count`: number of cooperators observed in the previous round

**Decision Rule by Round:**

**Round 1:**
Defect. No historical information exists; cooperation risks wasting your endowment with no evidence others will cooperate.

**Rounds 2 through r-1:**
Defect by default. Switch to cooperation only if:
- `last_cooperation_count ≥ m-1`, OR
- `last_cooperation_count = m-2` AND `successes / (current_round - 1) > 1/k`

The first condition triggers if the threshold was met in the immediately preceding round—others demonstrated willingness to cooperate.

The second condition hedges: if you fell one short of threshold last round but the historical success rate exceeds 1/k, the expected value of your contribution (probability of threshold times k) exceeds your cost (1).

**Round r (final round):**
Defect unconditionally. No future rounds exist; the marginal value of the community project's success is zero for you, so defection dominates.

**Defection Trap:**
If `successes = 0` (no round has ever met the threshold), defect for all remaining rounds. Persistent failure indicates cooperation is unachievable within your opponent pool.

**Rationale:**
This strategy avoids commitment to doomed collective projects while opportunistically cooperating when historical evidence suggests the threshold is achievable. It free-rides on rounds where others' cooperation alone would have succeeded, and it abandons cooperation when patterns indicate insufficient participation—both moves maximize individual expected payoff given observable aggregate information.
'''

description_INDIVIDUALISTIC_20 = '''
# Individualistic Threshold-Responsive Strategy

**Core Decision Rule:**
Cooperate in round t if and only if the observed number of cooperators among opponents in round t-1 is at least m-1. Otherwise, defect.

**Formal Statement:**

```
For round t ∈ {1, 2, ..., r}:
  If t = 1:
    Action: DEFECT
  Else:
    Let others_coop = number of opponents who cooperated in round t-1
    If others_coop ≥ m-1:
      Action: COOPERATE
    Else:
      Action: DEFECT
```

**Rationale:**
Your payoff from cooperating is k only if the threshold is met. Your payoff from defecting is 1 + k if the threshold is met, or 1 if it's not. Defecting strictly dominates cooperating unless my cooperation is pivotal — that is, unless without me the threshold is just barely unmet. This occurs only when at least m-1 others are already cooperating. If fewer than m-1 others cooperate, my cooperation cannot push the group over m, so my cost (1 lost endowment) is wasted. If m or more others cooperate, I receive the reward k regardless of my action, but cooperating costs me 1, so defecting nets an extra 1.

**Edge Case — Round 1:**
Defect. With no history, assume conservatively that others will not meet your cooperation. This respects the individualistic principle of not making altruistic bets on unknown opponents.

**Edge Case — Final Round (t = r):**
Apply the same rule—defect unless at least m-1 opponents cooperated in round r-1. The logic remains: cooperation only pays if your action is necessary for the threshold. There is no backward-induction advantage to deviation here because the rule already incorporates individual payoff maximization.

**Robustness Property:**
This strategy avoids cascading defections. If opponents use similar logic, a history of moderate cooperation (≥m-1 per round) sustains itself, while a history of low cooperation (< m-1) sustains universal defection—both stable outcomes that an individualistic player rationally accepts given the observed behavior of others.
'''

description_INDIVIDUALISTIC_21 = '''
# Adaptive Threshold-Exploitation Strategy

**Core Decision Rule:**

In each round, maintain a running estimate of opponent cooperation rate from observed history. Then:
1. Calculate the probability that at least m players cooperate (including yourself if you play C)
2. Compare expected payoffs:
   - E[Cooperate] = P(≥m cooperators | you cooperate) × k
   - E[Defect] = P(≥m cooperators | you defect) × k + 1
3. Play C if E[Cooperate] > E[Defect], else play D

**Cooperation Rate Estimation:**

Let c_prev = number of cooperators observed in previous rounds (aggregate only, not individual tracking). Let h = current round number.

Estimated opponent cooperation rate: ρ = c_prev / (n-1)(h-1), with floor of 0 and ceiling of 1.

**Expected Cooperators Among Remaining Opponents:**

If you cooperate, expected total cooperators = 1 + ρ(n-1).
If you defect, expected total cooperators = ρ(n-1).

**Decision Logic:**

```
if round == 1:
    play D
    [In first round, no history exists. Assume conservatively that others defect.]

else if round == r (final round):
    play D
    [No future rounds to influence. Always better to defect.]

else:
    if (1 + ρ(n-1) ≥ m):
        expected_c = k
    else:
        expected_c = 0
    
    if (ρ(n-1) ≥ m):
        expected_d = 1 + k
    else:
        expected_d = 1
    
    if expected_c > expected_d:
        play C
    else:
        play D
```

**Refinement for Pivotal Scenarios:**

When observed cooperation is near the threshold (ρ(n-1) ∈ [m-2, m]), increase weight on the pivotal case where your cooperation tips the outcome. Cooperate if:

(1 + ρ(n-1)) is within 1.5 of m, AND k ≥ 1 (always true by parameters).

**Edge Cases:**

- Rounds 2 through r-1: Use full calculation above
- If ρ = 0 throughout: Defect always (others aren't cooperating, threshold unreachable)
- If ρ = 1 observed: Defect in all remaining rounds (free ride on guaranteed cooperation)

**Individualistic Alignment:**

This strategy pursues maximum personal expected payoff without reference to collective welfare, fairness, or reciprocity. It treats opponent behavior as a statistical phenomenon to exploit, not as a signal deserving moral consideration. Cooperation occurs only when it raises your own expected return, not because others deserve it.
'''

description_INDIVIDUALISTIC_22 = '''
# Individualistic Threshold-Dependent Strategy

**Core Logic:**
Cooperate only when your individual decision is strictly necessary to achieve the threshold and the reward exceeds the cooperation cost. Otherwise, defect unconditionally to preserve your endowment.

## Decision Rules

**Round 1:** Defect
- No history available. Without information, assume others will defect and threshold will not be reached without extraordinary effort.

**Rounds 2 to r-1 (middle rounds):**
- Let c_obs = number of other players observed cooperating in the previous round
- If c_obs == m - 1: Cooperate
  - You are the decisive player. Cooperation yields payoff k (threshold met), defection yields payoff 1 (threshold missed). Since k > 1, cooperation dominates by a margin of k - 1.
- Otherwise: Defect
  - If c_obs ≥ m: Threshold already secured without your contribution; free-ride by defecting and collect the reward k plus your endowment (payoff = 1 + k).
  - If c_obs < m - 1: Threshold unreachable even with your cooperation; defect and keep endowment (payoff = 1).

**Round r (final round):** Defect unconditionally
- Terminal round. No future rounds exist to influence others' future behavior, so there is no strategic value to cooperation. Defect to preserve endowment regardless of the previous round's cooperation count.

## Edge Cases

- **First round with unknown n or m:** If parameters are uncertain, default to defect.
- **Exact threshold achievement (c_obs = m):** Defect immediately—threshold already met, free-ride on the provision.
- **Near-threshold in final round (c_obs = m - 1, round = r):** Defect despite being pivotal. The terminal nature overrides the threshold logic.

## Individualistic Alignment

This strategy prioritizes your own payoff maximization without reliance on others' reciprocity or shared understanding. It assumes:
- Others pursue independent strategies and will not reward your cooperation with future cooperation.
- Your only lever is the binary fact of whether you are essential to cross the threshold *this round*.
- Free-riding is the default rational position; cooperation is purchased only when your individual action is indispensable and the payoff mathematics is unambiguous.
'''

description_INDIVIDUALISTIC_23 = '''
# Empirical Threshold Matching Strategy

**Decision Framework:**

In each round, observe the cooperation count from the previous round and apply the following rule:

**Round 1 (Bootstrap):**
Defect. Without history, assume others play selfishly and that cooperation is unlikely to reach threshold.

**Rounds 2 through r-1 (Adaptive Phase):**
Let c_prev = number of cooperators in the immediately preceding round.

- **If c_prev ≥ m:** Defect. The threshold was already met without your contribution; free-ride to gain k + 1 instead of k.

- **If c_prev < m and c_prev > (m - 1) / 2:** Cooperate. Cooperation is trending upward and nearing the threshold. Your contribution is instrumentally valuable for tipping the group into the reward zone in the next round.

- **If c_prev ≤ (m - 1) / 2:** Defect. Cooperation is insufficient to signal that escalation is likely. Avoid wasting your endowment on a failing collective effort.

**Round r (Final Round):**
Always defect. No future rounds exist in which others might reward or punish your action, eliminating any downstream benefit from cooperation.

**Rationale:**

This strategy is individualistic because it exclusively maximizes your payoff conditional on observable history. Cooperation occurs only when your marginal contribution visibly increases the probability of reaching threshold m, making cooperation instrumentally self-interested rather than altruistic. Defection is the default, and cooperation is tactical escalation in response to detected momentum.
'''

description_INDIVIDUALISTIC_24 = '''
# ADAPTIVE THRESHOLD DEFECTION STRATEGY

**CORE PRINCIPLE**: Defect unless empirical evidence suggests you are the marginal player needed to reach the threshold. Maintain a running estimate of opponent cooperation rates and use it to calculate whether your participation matters for achieving collective payoff.

---

## DECISION RULE BY ROUND TYPE

**Round 1:**
Cooperate. Use this to gather initial empirical evidence about opponents' propensity to cooperate.

**Rounds 2 to r-1:**

1. Calculate empirical cooperation rate from all completed rounds:
   - total_cooperators = sum of cooperators across all previous rounds
   - empirical_rate = total_cooperators / ((t-1) × n)

2. Estimate expected cooperators among the other n-1 players:
   - expected_others = (n-1) × empirical_rate

3. Decision logic:
   - If expected_others ≥ m: **Defect** (threshold met without you; free-ride for payoff 1+k)
   - If expected_others = m-1: **Cooperate** (you are marginal; cooperation secures k and makes total payoff 0+k = k, while defection risks 1+0 = 1 if others fall short)
   - If expected_others < m-1: **Defect** (threshold unachievable even with your cooperation; minimize loss by keeping 1)

**Round r (final round):**
Always Defect. No future rounds exist to build reputation or reciprocal value. Maximize immediate payoff by keeping endowment.

---

## EDGE CASES

- **Ties in expected_others**: Round down when converting empirical rate to expected count; if exactly m-1, apply Cooperate rule above.
- **Early rounds with zero history**: Treat empirical_rate as 0.5 (uninformed prior) until round 3. This avoids pessimistic early defection while gathering signal.
- **Constant cooperation or defection by opponents**: Adaptation occurs immediately—high observed rates trigger defection; low observed rates trigger defection.

---

## INDIVIDUALISTIC ALIGNMENT

This strategy pursues personal payoff maximization without assuming opponent coordination, shared values, or reciprocal goodwill. It exploits cooperative opponents when they supply sufficient coverage, defects when cooperation is individually irrational, and only cooperates when empirical data indicates you are causally necessary to the outcome. No moral judgment; pure payoff calculation.
'''

description_INDIVIDUALISTIC_25 = '''
# Adaptive Free-Riding Strategy

## Core Decision Rule

Maintain a rolling estimate of opponent cooperation rates. Defect unless your cooperation is pivotal to reaching the threshold.

Let C_t = number of cooperators observed among opponents in round t.

**Primary decision rule for round t > 1:**

1. Compute estimated opponent cooperation rate: α = (average of C_t values over rounds 1 to t-1) / (n-1)

2. Forecast expected cooperators from opponents: E[opponents] = (n-1) × α

3. Execute:
   - **If E[opponents] ≥ m:** Defect (threshold achieved without your contribution; free-ride on public good)
   - **If E[opponents] = m - 1:** Cooperate (you are pivotal; your contribution completes the threshold and secures +k for you)
   - **If E[opponents] < m - 1:** Defect (threshold unreachable; cooperation wastes endowment with no payoff)

## Edge Cases

**Round 1:** Cooperate. Establish a baseline cooperation signal to learn whether the population supports the public good. This is your only mechanism to gather data without observations.

**Last round (t = r):** Apply the decision rule above based on C_{r-1}, but with heightened defection bias. Since no future rounds exist, pivot only if C_{r-1} = m - 1 exactly. Otherwise, defect.

**Stale observations:** If more than ⌈r/2⌉ rounds have elapsed without the threshold being achieved, reduce α by 20% per observation to account for declining cooperation. This prevents over-optimistic estimation in failing environments.

## Individualistic Logic

This strategy treats other players' contributions as a resource to exploit. You cooperate minimally—only when your contribution directly determines group success—and defect whenever the threshold will be met without you. You free-ride whenever possible, cooperate only when individually pivotal, and abandon the public good if others demonstrate insufficient commitment.
'''

description_INDIVIDUALISTIC_26 = '''
# Strategy: Conditional Free-Riding with Adaptive Threshold Monitoring

## Decision Rules

**Round 1:** Defect. No historical data exists; conservatively protect your endowment.

**Rounds 2 to r-1 (middle rounds):**
1. Observe X = number of cooperators among opponents in the immediately previous round
2. Apply the following decision tree:
   - **If X ≥ m-1:** Defect. The threshold will be met without your contribution. Free-ride by keeping your endowment and still receiving the reward k.
   - **If X = m-2:** Cooperate with probability p = (k-1)/k. The threshold is borderline; one additional cooperator (possibly you) may be needed. The expected value of cooperating slightly exceeds defection's expected value only when others are this close to the threshold.
   - **If X < m-2:** Defect. The threshold is sufficiently far from being met that even your cooperation is unlikely to trigger the reward. Keep your endowment.

**Round r (final round):** Defect unconditionally. No future rounds remain where reputation or threshold achievement benefits you. Extract maximum immediate value.

## Edge Cases

- **Unanimous defection observed:** If all opponents defected in every preceding round, continue defecting. The threshold will never be met.
- **Unanimous cooperation observed:** If all opponents cooperated and threshold was met, defect from round 2 onward to capture the reward without cost.
- **Tied decision at m-2:** When exactly m-2 opponents cooperated, use the probabilistic rule strictly. Do not round up or round down; execute the randomization.

## Individualistic Alignment

This strategy prioritizes your payoff at every decision point:
- You defect by default, treating cooperation as a cost to avoid.
- You only cooperate when the mathematical odds suggest threshold achievement requires your participation and the reward k sufficiently outweighs your contribution cost.
- You exploit observed cooperation by others, free-riding when the threshold will be met without you.
- You discard any consideration of fairness, reciprocity, or collective welfare—only expected payoff matters.
'''

description_INDIVIDUALISTIC_27 = '''
# Individualistic Adaptive Defection Strategy

## Core Decision Rule

Defect by default in all rounds. Cooperation is only viable as a probe to gather information about opponents in early rounds, with exploitation of observed patterns thereafter.

**In round t:**

```
If t == 1:
    Cooperate (information gathering probe)
Else if t < r:
    Let C_t-1 = observed cooperators in round t-1
    If C_t-1 >= m:
        Defect (project succeeds without your cost)
    Else if C_t-1 < m:
        Defect (project fails; your cooperation adds cost with zero benefit)
Else if t == r:
    Defect (final round; no future rounds to influence)
```

## Rationale

In each round, defection weakly dominates cooperation:
- If ≥m−1 others cooperate, you get 1+k by defecting versus k by cooperating
- If <m−1 others cooperate, you get 1 by defecting versus 0 by cooperating

Defecting gives you the full private endowment (1) plus any collective reward if the threshold is met.

## Handling Edge Cases

**Round 1:** Cooperate once to observe baseline opponent behavior. This is your only investment to build a model of the environment without ongoing cost. You learn whether you're facing cooperative, defective, or mixed opponents.

**Rounds 2 to r−1:** After observing round 1, you know the likely cooperation level. If opponents are not reliably reaching m cooperators, they will not reach it in future rounds either. Defect consistently. Even if opponents increase cooperation, your single defection costs nothing relative to joining a losing coalition.

**Round r (final round):** Defect unconditionally. There is no reputational punishment or future benefit from cooperation. The game ends; any collective outcome is already determined.

## Individualistic Alignment

This strategy refuses to subsidize others' decisions. You do not cooperate to "help the group succeed"—you cooperate only in round 1 to extract data on opponent tendencies. Once you observe whether the threshold is achievable, you optimize by keeping your endowment. If others reach the threshold without you, you profit. If they do not, you minimize losses by never wasting your contribution.
'''

description_INDIVIDUALISTIC_28 = '''
**CONDITIONAL DEFECTION WITH COOPERATION THRESHOLD TRACKING**

**Core Decision Rule:**
Defect by default. Cooperate only when empirical evidence suggests others are cooperating at a sufficient rate that the threshold is achievable.

**Round-by-Round Logic:**

*Round 1:*
- No history exists. Defect.
- Payoff: 1 (unless opponents coincidentally cooperate ≥ m players)

*Rounds 2 to r-1 (Middle rounds):*
- Observe: How many of the (n-1) opponents cooperated in the immediately preceding round. Call this count C_prev.
- Threshold check: If C_prev ≥ m-1, then others have demonstrated willingness to cooperate; threshold is achievable without your contribution. Defect (free-ride).
- If C_prev < m-1: Threshold will not be met this round regardless of your action. Defect (minimize waste).

*Round r (Final round):*
- Defect unconditionally. No future rounds to influence, so cooperation cannot affect future opponent behavior. No value to cooperation.

**Rationale for Edge Cases:**

- **First round:** Absent history, assume opponents follow their own self-interested logic (likely defection or unpredictable). Cooperation is speculative. Defect to secure baseline.
  
- **Last round:** Cooperation only pays off if others have committed endogenously to cooperate. With no future interaction, you cannot condition opponent behavior on your current action. Defecting locks in payoff k (if threshold was met in prior rounds) or 1 (if not).

**Adaptation Mechanism:**

The strategy continuously updates belief about opponent cooperation propensity based on what was observed last round. If you see ≥ m-1 cooperators, you conclude that independent sources (plural) have chosen to cooperate—sufficient evidence that threshold will continue to be met. This allows you to benefit from others' contributions without contributing yourself.

**Individualistic Alignment:**

This strategy prioritizes your payoff above all else. It exploits cooperation when available (free-riding on others' contributions) and avoids wasting endowment when cooperation is insufficient. It contains no altruism, no punishment, no commitment to group welfare—only exploitation of observed patterns.
'''

description_INDIVIDUALISTIC_29 = '''
# Threshold-Responsive Defection

**Core Decision Rule:**

Defect by default. Cooperate only when you are pivotal—specifically, when exactly m-1 cooperators appeared in the previous round, making your contribution the marginal action that determines whether the threshold is met.

**Round-by-Round Logic:**

**Round 1:** Defect. Without history, assume the group will not self-organize to reach m cooperators.

**Rounds 2 to r-1 (including last round):**
- Observe: Let c = number of cooperators in the immediately preceding round
- If c == m-1: Cooperate
- Otherwise: Defect

**Edge Case - Final Round (r):** Apply the same decision rule. Since this is the final round, payoffs are not carried into future rounds, but the marginal payoff structure is unchanged: cooperating when m-1 others cooperated yields k-1 > 0 additional payoff versus defecting.

**Rationale for Individualism:**

This strategy maximizes personal payoff by exploiting the asymmetry between being pivotal and being redundant:
- When c ≥ m, the threshold is already met; defecting nets 1+k (free riding).
- When c < m-1, cooperation alone cannot reach the threshold; defecting avoids wasting the endowment.
- When c = m-1, cooperating guarantees the bonus and yields 1-1+k = k, strictly better than the defecting payoff of 1+0 = 1.

No reliance on reciprocity, reputation, or group outcomes—only on the mechanical fact of pivotality.
'''

description_INDIVIDUALISTIC_30 = '''
**Adaptive Threshold Defense Strategy**

**Decision Rule:**

For any round t:

```
if t == 1:
    play D
elif t == r (final round):
    play D
else:  // rounds 2 through r-1
    let cooperators = number of players who cooperated in round t-1
    
    if cooperators >= m:
        play D  // threshold already met; free-ride for payoff (1 + k)
    elif cooperators == m - 1:
        play C  // cooperate to push across threshold; secure payoff k vs. payoff 0
    else:  // cooperators < m - 1
        play D  // threshold unachievable; defect to keep endowment (payoff 1)
```

**Rationale:**

This strategy is individualistic because it maximizes your expected payoff given observable opponent behavior:

- **Defect in round 1:** No history to predict threshold achievement; defection avoids risk.
- **Defect in final round:** No future rounds to reward cooperation; terminal defection extracts maximum immediate value.
- **Rounds 2 to r-1:** Condition solely on whether cooperation will move you from failure to success:
  - If m or more already cooperated last round, you achieve the collective payoff regardless of your action, so defect (payoff 1+k beats k).
  - If exactly m-1 cooperated, your cooperation triggers the payoff; not cooperating yields 0, so cooperate (payoff k).
  - If fewer than m-1 cooperated, the threshold is unachievable; defect (payoff 1 beats 0).

**Edge Cases:**

- If m = n: You must cooperate in a round 2-r-1 only if all n-1 opponents cooperated in the prior round. More typically, pure defection results.
- If m = 2 and n large: You cooperate only when exactly one opponent cooperated. Otherwise defect.
- Rounds with tie (e.g., multiple years with same cooperation pattern): Strategy is deterministic; you will make the same choice each time, creating a fixed-point pattern or oscillation depending on opponent strategies.
'''

description_INDIVIDUALISTIC_31 = '''
## Conditional Threshold Matching Strategy

**Core Decision Rule:**

In round t, cooperate if and only if:
- t < r (not the final round), AND
- The number of cooperators observed in the previous round was ≥ m - 1

Otherwise, defect.

**Rationale:** Cooperate when you have direct evidence that others are cooperating at levels that make the threshold achievable. This nets you the bonus (k) while avoiding the zero payoff of solo cooperation.

**First Round Handling:**

Defect. You have no history to indicate whether others will cooperate. Defection guarantees a payoff of 1, while cooperation risks 0.

**Last Round Handling:**

Defect unconditionally. No future rounds exist to influence, so there is no strategic benefit to cooperation. You either get 1 + k (if others hit threshold) or 1 (if they don't) regardless of your action—but you keep your endowment by defecting.

**Subsequent Rounds (2 through r-1):**

```
if observed_cooperators_last_round >= m - 1:
    play C
else:
    play D
```

If you observed at least m-1 others cooperating in the prior round, the probability is high that m or more will cooperate again (assuming opponent strategies exhibit some consistency). By cooperating, you secure the bonus payoff of k. If fewer than m-1 cooperated, the threshold failed last time and likely will again—defecting avoids wasting your endowment.

**Edge Case - Tie or Exact Threshold:**

If exactly m - 1 opponents cooperated last round, cooperating this round guarantees reaching m total cooperators and yielding payoff k. This is a favorable bet.

**Robustness:**

This strategy adapts to opponent behavior without requiring belief formation about individual strategies. It punishes defecting-heavy opponent populations automatically (you'll see low cooperation counts and defect in turn), and rewards cooperative-leaning populations. It avoids the temptation to free-ride on an observed cooperative round because you participate only when the threshold is empirically close to being met.
'''

description_INDIVIDUALISTIC_32 = '''
# ADAPTIVE THRESHOLD-MATCHING STRATEGY

**Core Decision Rule:**
- Maintain a running estimate of opponent cooperation rate: p̂ = (total cooperations observed across all rounds) / (total opponent-actions observed)
- Calculate expected cooperators among the n−1 opponents: E = (n−1) × p̂
- **Cooperate if and only if E < m−1**
- **Defect if and only if E ≥ m−1**

**Initialization (Round 1):**
Since no history exists, treat p̂ = 0.5 as the default belief.
- If (n−1) × 0.5 ≥ m−1, defect
- Otherwise, cooperate

**Per-Round Update:**
After observing the number of cooperators C_t in round t:
- Update: p̂ ← (cumulative cooperations so far) / (cumulative opponent actions so far)
- Apply decision rule for next round

**Last Round (Round r):**
Defect unconditionally. With no future rounds to learn from, there is no value in establishing cooperation precedent.

**Edge Case — Odd Fractions:**
If E is non-integer, use the ceiling: cooperate if ⌈E⌉ < m.

**Rationale:**
This strategy is individualistic because it:
1. Maximizes expected payoff: if threshold will be met without me (E ≥ m−1), I free-ride and gain 1+k instead of k
2. Avoids futile cooperation: if E < m−1, my cooperation becomes pivotal for reaching the threshold
3. Makes zero assumption about opponent coordination or shared norms—it treats all opponents as independent, potentially selfish agents
4. Updates beliefs empirically based on observed aggregate behavior, not identity or history of specific players
5. Abandons cooperation in the final round when future signaling has no value
'''
