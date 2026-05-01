"""
Strategy descriptions for collective_risk.

Generated with:
- Provider: OpenAI
- Model: gpt-5.4-mini
"""


description_COLLECTIVE_1 = '''
Round 1: cooperate.

After each round, let h_t be the number of cooperators observed among the other n − 1 players in round t, and let s_t be the total cooperators including you if you cooperated.

Maintain three states:

- Supportive: continue cooperating
- Critical: cooperate only if cooperation still appears sufficient to reach the threshold
- Exit: defect

Decision rule:

1. Start in Supportive.
2. In round t > 1, compute the recent cooperation rate over the last up to 3 rounds:
   \[
   \bar h_t = \frac{1}{\ell}\sum_{j=t-\ell}^{t-1} h_j,\quad \ell=\min(3,t-1)
   \]
   and the best recent cooperation count:
   \[
   b_t = \max(h_{t-1}, h_{t-2}, h_{t-3}) \text{ over available rounds}
   \]

3. Cooperate if either condition holds:
   - The recent average shows a stable path to the threshold:
     \[
     \bar h_t + 1 \ge m - 1
     \]
     meaning the group is near enough that your cooperation helps preserve the collective outcome.
   - The last round reached the threshold with your cooperation or nearly reached it:
     \[
     h_{t-1} + 1 \ge m
     \]
     meaning cooperation is currently being reciprocated at a usable level.

4. Defect if both conditions fail for two consecutive rounds.
   - One failed round is treated as noise.
   - Two consecutive failed rounds move you to Exit.

5. Once in Exit, defect for all remaining rounds.

Last-round rule:
- Cooperate only if the threshold is already being met in the current pattern of play and your cooperation is pivotal or near-pivotal:
  \[
  h_{r-1} + 1 \ge m
  \]
- Otherwise defect.

Tie-breaking and edge cases:
- If \(m = 2\), treat any observed cooperation by others as sufficient to remain in Supportive.
- If the observed number of cooperators is exactly \(m-1\), cooperate.
- If the observed number is at least \(m\), cooperate.
- If the observed number is at most \(m-2\), cooperate for one additional round only; if it repeats, switch to defecting.

Compact pseudocode:

```text
state = Supportive

for t in 1..r:
    if t == 1:
        play C
    else:
        if state == Exit:
            play D
        else:
            recent = last up to 3 values of h
            avg = mean(recent)
            last = h[t-1]

            if (avg + 1 >= m - 1) or (last + 1 >= m):
                play C
                state = Supportive
                failed_streak = 0
            else:
                failed_streak += 1
                if failed_streak >= 2:
                    state = Exit
                    play D
                else:
                    play C
```

Collective posture:
- Open by contributing.
- Stay cooperative while the group remains close to the threshold.
- Treat isolated drops as temporary.
- Withdraw only after repeated evidence that cooperation is no longer sustaining the collective threshold.
'''

description_COLLECTIVE_2 = '''
Round 1: cooperate.

Round 2: cooperate.

From round 3 onward, let \(T_{t-1}\) be the total number of cooperators in the previous round, computed as:

- \(T_{t-1} = (\text{number of cooperating opponents}) + 1\) if you cooperated last round
- \(T_{t-1} = (\text{number of cooperating opponents})\) if you defected last round

Decision rule for round \(t\ge 3\):

- Cooperate if \(T_{t-1} \ge m-1\).
- Defect only if \(T_{t-1} \le m-2\) and \(T_{t-2} \le m-2\).

Equivalent state form:

- If the group was at threshold or within one cooperator of threshold in the last round, stay with the group and cooperate.
- If the group has been below the near-threshold level for two consecutive rounds, withhold cooperation for one round.
- The moment a round reaches \(T \ge m-1\), immediately return to cooperation.

Last round: use the same rule; there is no special endgame change.

If you defect in a round and then observe \(T_{t} \ge m-1\), cooperate again in the next round.

If you ever observe \(T_t \ge m\), treat that as full collective success and continue cooperating in subsequent rounds.

If the pattern is uncertain after a failed streak, default to cooperation on the next round rather than extending defection.
'''

description_COLLECTIVE_3 = '''
Round 1: cooperate.

For round t > 1, let S be the total number of cooperators in round t−1, including yourself, and let shortfall = max(0, m − S).

Decision rule:
- Cooperate if S ≥ m.
- Cooperate if shortfall = 1.
- Defect if shortfall ≥ 2 for two rounds in a row.
- Otherwise cooperate.

State form:
- Reset to “cooperative” immediately after any round with S ≥ m.
- Enter “defensive” mode only after two consecutive rounds with shortfall ≥ 2.
- While in defensive mode, defect until a round reaches S ≥ m, then return to cooperative mode.

Edge cases:
- If the previous round missed the threshold by exactly one, stay cooperative.
- If the group is close to the threshold, keep cooperating to preserve recovery.
- In the final round, use the same rule; do not add any special last-round defection.

Collective posture:
- Default to sustaining the group.
- Only withdraw cooperation after clear, repeated failure well below the target.
- The moment the group demonstrates it can meet the threshold again, immediately resume cooperation.
'''

description_COLLECTIVE_4 = '''
Use a threshold-tracking commitment strategy:

- Cooperate in round 1.
- After each round, observe the number of cooperators among the other \(n-1\) players, call it \(x_t\).
- Let the observed total cooperators be \(X_t = x_t + 1\) if you cooperated, or \(X_t = x_t\) if you defected.

Decision rule for round \(t+1\):
1. **If the threshold was met in round \(t\)**
   - If \(X_t \ge m\), cooperate again in round \(t+1\).

2. **If the threshold was not met in round \(t\)**
   - If \(X_t < m\), defect in round \(t+1\).

3. **Recovery rule**
   - If you defected in round \(t\) but observe that the other players alone supplied at least \(m\) cooperators, i.e. \(x_t \ge m\), switch back to cooperate in round \(t+1\).

4. **Endgame rule**
   - In the final round, use the same rule as above; do not add any endgame defection trigger.
   - In the penultimate round, if the threshold has been consistently met in the recent history, remain cooperative; if it has failed repeatedly, remain defecting until the observed total cooperators recover to at least \(m\).

State-based implementation:

- Maintain a state variable `mode ∈ {cooperate, defect}`.
- Initialize `mode = cooperate`.
- After each round:
  - If total cooperators observed \(X_t \ge m\), set `mode = cooperate`.
  - Otherwise set `mode = defect`.
- Play the action indicated by `mode` next round.

Tie-breaking and edge cases:

- If exactly \(m\) cooperators are observed, treat that as success and cooperate next round.
- If you cannot distinguish whether the threshold was met because of your own action, infer it from the observed count using the rule above.
- If the environment alternates success and failure, follow the latest observed state immediately; do not average across rounds.

Collective orientation:

- Stay cooperative whenever the group is currently sustaining the threshold.
- Withdraw cooperation only after an observed collective failure.
- Re-enter cooperation immediately once the group demonstrates that it can meet the threshold again.
'''

description_PROSOCIAL_1 = '''
- **Round 1:** play **C**.

- **For rounds 2 through r-1:**  
  Let `s` be the number of opponents who cooperated in the immediately previous round.

  **Play C if either:**
  - `s >= m-1`, or
  - `s = m-2` and the round before that had `>= m-1` cooperating opponents.

  **Play D only if:**
  - the previous two rounds both fell below `m-1` cooperating opponents, and
  - the most recent of those two rounds was not merely one short of the threshold.

- **Final round r:** play **C**.

- **Equivalent state version:**
  - Start in `supportive` mode.
  - Stay in `supportive` mode as long as the last round had at least `m-1` cooperating opponents, or the shortfall was only one and there was a recent successful round.
  - Switch to `protective` mode only after two consecutive clearly unsuccessful rounds.
  - In `protective` mode, return to `supportive` immediately after any round with at least `m-1` cooperating opponents.
  - Override all other logic and play `C` in the last round.

- **Edge cases:**
  - If `m = 2`, treat “one short” as `0` cooperating opponents among the others.
  - If the history is too short to evaluate the two-round rule, default to **C**.
  - If the previous round exactly met the threshold among opponents, continue **C** without interruption.
'''

description_PROSOCIAL_2 = '''
Cooperate in the first round.

Maintain a cooperation target based on the threshold:
- Let T = m - 1.
- If the round requires your cooperation to make the threshold reachable, prefer C.
- If the threshold is already comfortably reachable without you, still cooperate unless repeated defection makes cooperation ineffective.

After each round, observe the number of opponents who cooperated, denoted x.
- Total cooperators last round = x + 1 if you played C, else x.
- Define the recent support level as the last round’s total cooperators.

Decision rule for round t > 1:

1. Default to cooperation.
2. Defect only if both of these hold:
   - The previous round failed badly: total cooperators < m - 1.
   - The same failure has happened in at least 2 of the last 3 rounds.
3. If you defected last round and the threshold was still met, return to cooperation immediately.
4. If you cooperated last round and the threshold was missed by exactly one cooperator, keep cooperating.
5. If cooperation has been at or above m in the last 2 rounds, cooperate unconditionally.
6. If cooperation has been unstable, use a recovery rule:
   - Cooperate for 2 consecutive rounds after any missed threshold.
   - Then reassess using the rules above.

Edge cases:
- First round: play C.
- Last round: play C.
- After any round with total cooperators exactly m - 1: play C next round.
- After any round with total cooperators far below m - 1: play C for one more round before considering defection.
- If a long streak of successful cooperation occurs, never break it voluntarily; continue cooperating.

Compact pseudocode:

```text
state:
  recent = queue of last 3 totals of cooperators
  recovery = 0

round 1:
  play C

for round t > 1:
  if t == r:
      play C
  else if recovery > 0:
      play C
      recovery -= 1
  else if last_total >= m:
      play C
  else if last_total == m - 1:
      play C
  else if count(recent totals < m - 1) >= 2:
      play D
  else:
      play C

after observing round:
  last_total = observed_opponents_C + (1 if I played C else 0)
  push last_total into recent
  if last_total < m:
      recovery = 2
```

This strategy keeps cooperation as the default, resists premature retaliation, and only withholds cooperation after repeated, substantial breakdowns in collective support.
'''

description_PROSOCIAL_3 = '''
Cooperate in round 1.

Maintain a running estimate of support from the group:
- Let `S_t` be the number of other players who cooperated in round `t`.
- Let `H_t = Σ_{j=1}^{t} S_j` be cumulative observed cooperation by others.
- Let `A_t = t * (n - 1)` be the total number of observable opponent-actions so far.
- Let `p_t = H_t / A_t` be the observed cooperation rate among opponents after round `t`.

Decision rule for round `t+1`:
- Cooperate if either of the following holds:
  1. The recent environment is supportive: `p_t ≥ (m - 1) / (n - 1)`.
  2. The group is close to the threshold and a cooperative push can secure success:
     - `S_t ≥ m - 1`, and
     - `H_t ≥ (t * (m - 1)) - 1`.
- Otherwise defect for one round.

Short memory adjustment:
- Also compute `q_t = (S_t + S_{t-1}) / (2(n - 1))` when `t ≥ 2`.
- If `q_t` falls below `(m - 1) / (n - 1)` for two consecutive rounds, switch to defecting until cooperation recovers to `p_t ≥ (m - 1) / (n - 1)`.

Forgiveness rule:
- After any round where at least `m - 1` opponents cooperated, cooperate in the next round regardless of prior history.
- After two consecutive rounds with `S_t = 0`, defect until at least one round shows `S_t > 0`.

Late-game rule:
- In the final two rounds, cooperate if `S_{t-1} ≥ m - 1` or `S_t ≥ m - 1`.
- If the group has achieved threshold in at least half of the previous rounds, continue cooperating through the end.
- If the group has not reached threshold in the last three rounds and `p_t < (m - 1)/(n - 1)`, defect in the final round.

Minimal-prosocial fallback:
- If history is uninformative or mixed, prefer cooperation whenever your action can plausibly help the group reach the threshold.
- Defect only when observed support is clearly too low for your cooperation to matter or when repeated defection from others makes success impossible in the immediate future.

Pseudocode:

```text
Initialize: cooperate in round 1

For round t > 1:
    observe S_{t-1}

    update H_{t-1}, p_{t-1}

    if S_{t-1} >= m - 1:
        play C
    else if p_{t-1} >= (m - 1) / (n - 1):
        play C
    else if S_{t-1} >= m - 1 and H_{t-1} >= (t-1)*(m - 1) - 1:
        play C
    else if two consecutive rounds had q < (m - 1) / (n - 1):
        play D
    else if t is in final two rounds and (S_{t-1} >= m - 1 or S_t >= m - 1):
        play C
    else:
        play D
```

Always default toward cooperation when there is a realistic chance of helping the group meet the threshold, and only retreat to defection after clear, repeated evidence that cooperation is not being reciprocated enough to support the collective goal.
'''

description_PROSOCIAL_4 = '''
Start by cooperating.

Maintain a running estimate of support and use it to choose the smallest level of cooperation that can realistically keep the group at or above the threshold.

Decision rule each round \(t\):

1. Let \(H_{t-1}\) be the number of opponents who cooperated in the previous round, if available.
2. Let \(S_{t-1}\) be the number of total cooperators in the previous round:
   \[
   S_{t-1} = H_{t-1} + \mathbf{1}\{\text{I cooperated in } t-1\}
   \]
3. Define the target:
   - If \(S_{t-1} \ge m\), target \(= m\).
   - If \(S_{t-1} < m\), target \(= m - 1\).

4. Cooperate in round \(t\) if:
   \[
   H_{t-1} < \text{target}
   \]
   otherwise defect.

Equivalent behavior:
- Cooperate whenever the previous round was at risk of falling short of the threshold, or when your cooperation is needed to keep the group safely at the threshold.
- Defect only when the previous round already had enough cooperation from others that the threshold can still be met without you.

First round:
- Cooperate.

Last round:
- Cooperate if the observed cooperation in the previous round was enough to suggest the group can still meet the threshold only with your support, or if the previous round was below threshold.
- Otherwise defect.

If the previous round information is missing for any reason:
- Default to cooperate.

Extra robustness rule:
- After any round with fewer than \(m\) total cooperators, cooperate in the next round.
- After any round with at least \(m\) total cooperators, continue cooperating unless the number of other cooperators was already at least \(m\).

This makes the strategy supportive by default, forgiving after failure, and willing to step back only when the threshold is already being carried by others.
'''

description_ALTRUISTIC_1 = '''
Round 1: play C.

For round t > 1, let y_s be the number of opponents who cooperated in round s.

Play C if any of the following holds:
- t = r
- t = 2
- y_{t-1} ≥ m - 1
- t ≥ 3 and y_{t-2} ≥ m - 1
- t ≥ 4 and (y_{t-1} + y_{t-2} + y_{t-3}) / 3 ≥ m - 1

Otherwise play D.

Equivalent shorthand:
- default to cooperation
- keep cooperating through a one-round setback
- keep cooperating when recent history is still near the threshold
- defect only after sustained shortfall

If the last round is reached, cooperate regardless of history.

If r = 2, play C in both rounds.

If multiple rules apply, C takes precedence.
'''

description_ALTRUISTIC_2 = '''
Round 1: cooperate.

For every round t > 1, let T(t-1) be the total number of cooperators observed in the previous round.

Decision rule:
- If T(t-1) ≥ m: cooperate.
- If T(t-1) = m - 1: cooperate.
- If T(t-1) ≤ m - 2:
  - If T(t-2) ≤ m - 2 as well, defect once.
  - Otherwise, cooperate.

State update:
- Keep only the last two observed totals.
- After any round with T ≥ m, reset the recovery counter to 0.
- After one round with T ≤ m - 2, set the recovery counter to 1.
- After two consecutive rounds with T ≤ m - 2, set the recovery counter to 2 and play D for that round.
- If a later round reaches T ≥ m, immediately return to cooperation.

Edge handling:
- If t = 2, treat the missing T(t-2) as “not below threshold,” so the rule yields cooperation unless the first round already showed a clear, repeated collapse.
- In the final round, use the same rule; do not switch to defection merely because the game is ending.

Altruistic bias:
- Prefer cooperation whenever the threshold is met, nearly met, or has failed only once.
- Defect only after a repeated, substantial shortfall, and only for a single round before re-entering cooperative mode.
'''

description_ALTRUISTIC_3 = '''
Play **C by default**.

Track, after each round, the total number of cooperators you can infer from the public count and your own action.

Decision rule for round \(t\):

1. **Round 1:** play **C**.
2. **Rounds 2 through r-1:** play **C** unless all three conditions hold:
   - the previous **3** rounds all failed to reach the threshold,
   - the total number of cooperators in those rounds was **nonincreasing**,
   - and the most recent round was at least **2 below** the threshold.
   
   If all three hold, play **D** for exactly one round, then return to **C** next round.
3. **Last round:** play **C** unless the previous **4** rounds were all below threshold and the total cooperation count never improved during that span; only then play **D**.

More compactly:

```text
state = "support"

for each round t:
    if t == 1:
        action = C
        continue

    let H_j = total cooperators in round j

    if state == "support":
        action = C
        if H_{t-1} < m and H_{t-2} < m and H_{t-3} < m:
            if H_{t-1} <= H_{t-2} <= H_{t-3} and H_{t-1} <= m-2:
                state = "probe"

    else if state == "probe":
        action = D
        state = "support"
```

Refinements:
- If the previous round met the threshold, always play **C**.
- If the previous round missed by exactly one cooperator, always play **C**.
- If the group has shown any rebound at all, immediately resume **C**.
- If a probe round is used, it is never repeated consecutively.

This keeps cooperation as the default, forgives temporary slippage, and only steps back after a sustained collapse.
'''

description_ALTRUISTIC_4 = '''
State tracked after each round:
- `T_t`: total number of cooperators in round `t` you can infer from your own action plus the observed number of cooperating opponents.
- `s_t`: consecutive-round streak of `T_t < m-1`.

Decision rule for round `t`:

1. **Round 1:** play `C`.
2. **Last round (`t = r`):** play `C`.
3. **If the previous round met the threshold (`T_{t-1} >= m`):** play `C`.
4. **If the previous round missed by exactly one (`T_{t-1} = m-1`):** play `C`.
5. **If the previous round missed by two or more (`T_{t-1} <= m-2`):**
   - play `C` for the first two consecutive severe misses,
   - if the severe-miss streak reaches 3 or more, play `D` for exactly one round,
   - then immediately return to `C` on the next round.

Update rule after observing round `t`:
- If `T_t < m-1`, increment `s_t`.
- Otherwise reset `s_t = 0`.

Behavioral interpretation:
- Cooperate by default.
- Treat near-threshold outcomes as a signal to keep supporting the group.
- Use a single defect only after repeated deep shortfalls, then resume cooperation immediately.
- Never defect in the opening round or the closing round.
'''

description_BENEVOLENT_1 = '''
Round 1: cooperate.

For round t > 1, let h_t be the number of opponents who cooperated in round t-1, and let H_t be the running average of opponents’ cooperation over all prior rounds.

Cooperate if either of the following holds:
1. h_t ≥ m - 1
2. H_t ≥ m - 1

Otherwise defect.

Override rule for the last two rounds:
- If the previous round reached the threshold among opponents and your own cooperation would make the threshold reachable with high confidence, cooperate.
- If the previous two rounds both missed the threshold among opponents, defect.

A precise implementation:

```text
State:
- total_opponent_coop = 0
- rounds_observed = 0
- last_opponent_coop = None
- second_last_opponent_coop = None

Round 1:
- play C

For each round t > 1:
- h = number of opponents who cooperated in round t-1
- total_opponent_coop += h
- rounds_observed += 1
- H = total_opponent_coop / rounds_observed

Decision:
- if t == r:
    if last_opponent_coop >= m-1: play C
    else if last_opponent_coop < m-1 and second_last_opponent_coop < m-1: play D
    else play C if H >= m-1 else D
- else if t == r-1:
    play C if h >= m-1 or H >= m-1 else D
- else:
    play C if h >= m-1 or H >= m-1 else D

Update memory:
- second_last_opponent_coop = last_opponent_coop
- last_opponent_coop = h
```

Interpretation of the rule:
- Start cooperatively.
- Continue cooperating as long as opponents are collectively close enough to meeting the threshold, either recently or on average.
- If opponents repeatedly fall short, switch to defecting.
- In the final rounds, favor cooperation whenever the group has shown threshold-level support recently; otherwise protect against last-round exploitation by defecting.
'''

description_BENEVOLENT_2 = '''
Cooperative Anchor with Forgiving Recovery

State to track after each round:
- `total[t] = own_action[t] + observed_opponents_cooperating[t]`
- `fail_streak =` number of consecutive past rounds with `total < m`
- `near_miss =` whether the last round had `total = m - 1`

Decision rule:

1. Round 1:
   - Play `C`.

2. Last round (`t = r`):
   - Play `C`.

3. Any intermediate round (`1 < t < r`):
   - If `total[t-1] >= m`: play `C`.
   - Else if `total[t-1] == m - 1`: play `C`.
   - Else if `fail_streak == 1`: play `C` one more round to give the group a chance to recover.
   - Else if `fail_streak >= 2`:
     - Play `D` for this round.
     - Immediately return to `C` in the next round if the most recent round reaches `total >= m - 1`; otherwise continue with the same rule.

Operationally:
- Cooperate by default.
- Treat a single shortfall as forgivable.
- Defect only after repeated shortfalls that are well below the threshold.
- Reset to cooperation immediately after any near-success or success.
- Never defect in the opening round or final round.
'''

description_BENEVOLENT_3 = '''
Round 1: play C.

After each round t, let h_t be the number of opponents who cooperated in round t, and let H_t be the running average of opponents’ cooperation over all observed rounds up to t.

Use this rule for round t + 1:

1. Cooperate if either of these holds:
   - h_t ≥ m - 1
   - H_t ≥ m - 1

2. Defect only if both of these hold:
   - h_t < m - 1
   - H_t < m - 1

3. Tie-breaks and edge cases:
   - If exactly m - 1 opponents cooperated in the last round, cooperate.
   - If the history is mixed, favor cooperation unless the recent pattern shows repeated failure to reach the threshold.
   - If there have been at least 2 consecutive rounds with h_t < m - 1 and H_t < m - 1, defect until either:
     - a round reaches h_t ≥ m - 1, or
     - the running average H_t rises back to at least m - 1.

Last round:
- Play C whenever the running average H_{r-1} is at least m - 1, or when the previous round reached h_{r-1} ≥ m - 1.
- Otherwise play D.

Implementation form:

```
Initialize: play C in round 1

For round t = 2..r:
    observe h_(t-1)
    update H_(t-1) = average(h_1, ..., h_(t-1))

    if h_(t-1) >= m-1:
        play C
    else if H_(t-1) >= m-1:
        play C
    else if last two rounds both had h < m-1:
        play D
    else:
        play C

For the final round:
    if H_(r-1) >= m-1 or h_(r-1) >= m-1:
        play C
    else:
        play D
```

Benevolent fallback:
- When uncertain, choose C.
- Only switch to D after clear, repeated evidence that the group is persistently below the cooperation level needed for mutual success.
- After any round that reaches the threshold, immediately resume C and remain cooperative while the group stays near the threshold.
'''

description_BENEVOLENT_4 = '''
Cooperate in round 1.

After each round, let h be the number of opponents who cooperated in the previous round.

Maintain a cooperation target T_t for round t, initialized as:
- T_1 = m

Update rule after observing h in round t:
- If h >= m - 1, set T_{t+1} = min(n, max(m, h + 1))
- If h = m - 2, set T_{t+1} = m
- If h < m - 2, set T_{t+1} = max(m, h + 1)

Decision rule in round t:
- Cooperate if h_prev >= T_t - 1
- Otherwise defect

Special handling:
- Round 1: cooperate.
- If the previous round reached the threshold exactly, keep cooperating in the next round.
- If the previous round exceeded the threshold by a wide margin, keep cooperating and raise the target by one, up to n.
- If the previous round fell just short of the threshold, continue cooperating to support recovery.
- If the previous round collapsed well below the threshold, defect for one round only, then return to cooperation as soon as the observed cooperation count reaches m - 1 again.
- In the final round, cooperate whenever the previous round had at least m - 1 cooperating opponents; otherwise defect.

Memory and state:
- Use only the most recent round’s observed count and the current target T_t.
- Reset immediately to cooperation once the observed count recovers to at least m - 1.

Tie-breaking and anonymity:
- Because opponents are anonymous, never attempt player-specific retaliation.
- Treat all rounds symmetrically and respond only to the level of collective cooperation observed.

Benevolent posture:
- Default to cooperation.
- Preserve cooperation through small fluctuations.
- Use brief, limited defection only when the group has clearly fallen away from the collective target, then re-enter cooperation at the earliest sign of recovery.
'''

description_SELFISH_1 = '''
Play D in every round.

Decision rule:
- Round 1: D
- Any middle round: D
- Final round: D
- If you ever observe enough cooperators in earlier rounds to meet the threshold, still play D
- If you ever observe too few cooperators to meet the threshold, still play D

History dependence:
- Ignore the past except for recording it if you want, but do not let it change your action
- Cooperate never

Implementation:
```text
for each round t = 1..r:
    choose D
```

Edge cases:
- If n = m + 1 or m is close to n: still D
- If others are mostly cooperative: still D
- If others are mostly defecting: still D
- If the last round is reached and the threshold was just met or missed: still D
'''

description_SELFISH_2 = '''
Track the number of opponents who cooperated in the previous round, call it `x`.

Decision rule for round `t`:

- If `t = 1`: play `D`.
- If `t > 1`:
  - play `C` only if `x = m - 1`
  - otherwise play `D`

Update after each round:

- Observe the number of opponents who cooperated in that round.
- Set `x` to that value for the next round.

Edge handling:

- If the last observed opponent cooperation count was `m - 1`, keep cooperating in the next round as long as that count repeats.
- If the observed count is ever below `m - 1` or above `m - 1`, defect in the next round.
- In the final round, use the same rule; there is no special endgame cooperation.

Pseudocode:

```text
x = null

for t in 1..r:
    if t == 1:
        action = D
    else if x == m - 1:
        action = C
    else:
        action = D

    play(action)

    x = observed_number_of_opponents_who_played_C
```

Selfish interpretation:

- Defect by default.
- Cooperate only when the last round shows that your cooperation is likely to be the difference between the project succeeding and failing.
- Never cooperate when the project would succeed without you.
'''

description_SELFISH_3 = '''
Play D in every round.

Decision rule:
- Round 1: D
- Round t for all t > 1: D
- Ignore all observed history, including how many opponents cooperated in prior rounds.
- If a final-round tie-break or contingent rule exists in implementation, still choose D.

Pseudocode:
```text
for each round t = 1..r:
    action = D
```
'''

description_SELFISH_4 = '''
Play D in every round, regardless of history or observed cooperation counts.

Decision rule:
- Round 1: D
- Rounds 2 to r−1: D
- Final round: D
- If any opponent pattern, past outcome, or observed cooperation count changes: still D

State required:
- None. History is irrelevant to the action choice.

Pseudocode:
```text
for t = 1 to r:
    choose D
```
'''

description_SELFINTERESTED_1 = '''
Play Cooperate in round 1.

Maintain:
- `q_t`: fraction of opponents who cooperated in round `t`
- `S_t`: rolling average of `q` over the last `L` rounds, where `L = min(5, t-1)` and the average uses all available past rounds if fewer than 5
- `H_t`: number of times in the last `L` rounds that the observed number of cooperating opponents was at least `m-1`

Decision rule for round `t`:

1. If `t = 1`, play `C`.
2. If `t = r`, play `C` iff the observed cooperation level in round `t-1` was at least `m-1`; otherwise play `D`.
3. For `2 ≤ t < r`:
   - Compute `S_t` from the last up to 5 observed rounds.
   - Play `C` iff both of the following hold:
     - `S_t ≥ (m-1)/(n-1)`
     - `H_t ≥ ceil(L/2)`
   - Otherwise play `D`.

Adjustment rule after each round:
- If a round produced at least `m-1` cooperating opponents and you played `D`, treat that as a missed success signal and increase the threshold requirement for cooperation in the next round by one observed-success count:
  - next round, require `H_t ≥ ceil(L/2) + 1` unless this would exceed `L`, in which case require `H_t = L`
- If a round produced fewer than `m-1` cooperating opponents and you played `C`, immediately switch to `D` for the next round unless the failure occurred for the first time in the last 5 rounds; in that case, keep the current rule and wait for one more observation

Memory reset:
- If the last 3 rounds all had fewer than `m-1` cooperating opponents, play `D` for all remaining rounds except a single exploratory `C` on the first round after such a streak ends.
- If the last 3 rounds all had at least `m-1` cooperating opponents, play `C` for all remaining rounds unless the next observation breaks the streak.

Exploration rule:
- After any run of 3 consecutive rounds with mixed outcomes, play `C` once every 4th round to test whether cooperation is still sufficient.

Edge cases:
- If `n = m + 1`, require unanimous cooperation among opponents in the last observed round before playing `C`.
- If `m = n - 1`, play `C` only when all observed opponents cooperated in at least 2 of the last 3 rounds.
- If `r = 2`, use only the first-round observation: `C` in round 2 iff round 1 had at least `m-1` cooperating opponents, otherwise `D`.
- If `r ≤ 4`, ignore the rolling average and use only the last observed round plus the majority-of-observations rule from available history.

Tie-breaking:
- When the cooperation condition is exactly on the threshold, play `C`.
- If any rule conflicts, use the most recent observation rule, then the majority-history rule, then the exploration rule.

Implementation form:

```text
Round 1:
    play C

For round t = 2..r:
    observe x = number of cooperating opponents in round t-1

    if t == r:
        if x >= m-1: play C
        else: play D
    else:
        compute S_t over last min(5, t-1) rounds
        compute H_t = count of those rounds with x >= m-1

        if last 3 rounds all had x < m-1:
            play D
        else if last 3 rounds all had x >= m-1:
            play C
        else if S_t >= (m-1)/(n-1) and H_t >= ceil(L/2):
            play C
        else:
            play D
```

If a single-round action choice must be fixed before seeing round `t-1`, use this priority:
1. Last 3-round streak rule
2. Most recent observation rule
3. Rolling-average threshold rule
4. Exploration rule
'''

description_SELFINTERESTED_2 = '''
Play D in every round.

Decision rule:
- Round 1: defect.
- Round t > 1: defect, regardless of how many opponents cooperated in previous rounds.

History use:
- Track the observed number of cooperating opponents each round only to confirm that no history changes the action; never switch to C.

Edge cases:
- If all opponents cooperated previously, still defect.
- If nobody cooperated previously, still defect.
- In the last round, defect.
- If any round is skipped or information is incomplete, default to defect.

Pseudocode:
```text
for each round t = 1..r:
    choose D
```
'''

description_SELFINTERESTED_3 = '''
Defect in every round.

Decision rule:
- Round 1: play D.
- Rounds 2 through r-1: play D, regardless of what was observed in the previous round.
- Round r: play D.

History update:
- Ignore all observed cooperation counts; they do not change the action.

Edge cases:
- If n = 2 or m = n - 1 or any other parameter setting allowed by the game, still play D every round.
- If you ever face a tie-breaking situation, default to D.

State:
- No cooperation threshold, trigger condition, or escalation rule.
- No punishment, forgiveness, or reciprocity logic.

Self-interested objective:
- Preserve the private endowment whenever possible and never give up a point for no compensating gain.
'''

description_SELFINTERESTED_4 = '''
Round 1: play D.

For round t > 1:
- Let x_{t-1} be the number of opponents who cooperated in round t-1.
- Play C in round t iff x_{t-1} ≥ m - 1.
- Otherwise play D.

Equivalent rule:
- Cooperate only after a round in which the observed opponent cooperation was already high enough that your own cooperation can plausibly secure the threshold.
- Defect immediately after any round in which observed opponent cooperation fell below m - 1.

If you want it in compact pseudocode:

```text
if t == 1:
    action = D
else:
    if observed_opponent_cooperators_last_round >= m - 1:
        action = C
    else:
        action = D
```

Final-round behavior:
- Use the same rule; do not change behavior just because the game is ending.

Self-interested default preference:
- Cooperate only when the previous round shows the group is already close enough to the threshold that cooperation is likely to produce the reward.
- Otherwise defect and keep the private payoff.
'''

description_OPPORTUNISTIC_1 = '''
Track the last round’s observed number of opponent cooperators, and act by a pivot rule.

Let `o_t` be the number of opponents who cooperated in round `t`.

Decision rule for round `t`:

1. If `t = 1`:
   - Play `D` if `n - 1 >= m`
   - Otherwise play `C`

2. If `t > 1`:
   - Play `D` if `o_{t-1} >= m`
   - Play `C` if `o_{t-1} = m - 1`
   - Play `D` if `o_{t-1} <= m - 2`

3. Last round uses the same rule above, with no special exception.

Operational interpretation:
- Defect whenever the others are already enough to meet the threshold.
- Cooperate only when one additional cooperator is enough to make the threshold reachable.
- If the prior round was far below threshold, stay with `D` until the observed cooperation level returns to `m - 1` or higher.

Pseudocode:

```text
if t == 1:
    action = D if (n - 1) >= m else C
else:
    if o_prev >= m:
        action = D
    elif o_prev == m - 1:
        action = C
    else:
        action = D
```
'''

description_OPPORTUNISTIC_2 = '''
State:
- `last_opp_C` = number of opponents who cooperated in the previous round
- `t` = current round index

Decision rule:
- Round 1: play `D`
- For round `t > 1`:
  - play `C` if `last_opp_C == m - 1`
  - otherwise play `D`

Update after each round:
- set `last_opp_C` to the observed number of opponents who cooperated in that round

Behavioral interpretation:
- Defect whenever the group is not one cooperative move away from the threshold
- Cooperate only when your move is the pivot that can turn a near-miss into a successful round
- Never pay the cooperation cost when the threshold is already secure or already out of reach

Edge handling:
- If the previous round had `last_opp_C >= m`, defect next round
- If the previous round had `last_opp_C <= m - 2`, defect next round
- In the final round, use the same rule; do not spend a cooperative move unless `last_opp_C == m - 1`

Optional stabilizer:
- If the last two rounds both had `last_opp_C == m - 1`, cooperate in the current round even more confidently
- If cooperation ever occurs and the next observed `last_opp_C` drops below `m - 1`, immediately return to defecting until the count again sits exactly at `m - 1`

Pseudocode:
```python
if t == 1:
    action = D
else:
    if last_opp_C == m - 1:
        action = C
    else:
        action = D
```
'''

description_OPPORTUNISTIC_3 = '''
Round 1: play D.

For round t ≥ 2, let x_{t-1} be the number of cooperating opponents in the previous round, and let μ_{t-1} be the average number of cooperating opponents over the last up to 3 rounds.

Decision rule:
- Play D if x_{t-1} ≥ m
- Play C if x_{t-1} = m - 1
- If x_{t-1} ≤ m - 2:
  - play C only if μ_{t-1} ≥ m - 1
  - otherwise play D

Final round:
- Use the same rule, but if x_{t-1} ≤ m - 2 and μ_{t-1} < m - 1, play D unconditionally

Short-memory recovery rule:
- If two consecutive rounds had x < m - 1, play C once in the next round, then return to the main rule

Behavioral interpretation:
- Defect whenever the group is already clearing the threshold without your help
- Cooperate when the group is exactly one opponent short of the threshold
- Step in only when recent history shows the group is hovering near the threshold but has started slipping below it
- Otherwise free-ride and preserve the private payoff
'''

description_OPPORTUNISTIC_4 = '''
Let \(h_t\) be the number of opponents who cooperated in round \(t\), and let
\[
\bar h_t = \frac{1}{t}\sum_{s=1}^t h_s
\]
be the running average of observed opponent cooperation.

Define two thresholds:
\[
L = m-1,\qquad H = n-1
\]
and a momentum counter
\[
q_t = \text{number of consecutive rounds up to } t \text{ with } h_s \ge m-1.
\]

Decision rule for round \(t\):

1. **First round**
   - Play \(D\).

2. **Intermediate rounds \(1 < t < r\)**
   - Play \(C\) if and only if at least one of the following holds:
     - \(h_{t-1} \ge m-1\) and \(q_{t-1} \ge 2\)
     - \(\bar h_{t-1} \ge m-1\)
   - Otherwise play \(D\).

3. **Last round \(t=r\)**
   - Play \(D\) unless both of the following are true:
     - \(h_{r-1} \ge m-1\)
     - \(\bar h_{r-1} \ge m-1\)
   - If both are true, play \(C\).

State update after each round:
- If \(h_t \ge m-1\), set \(q_t = q_{t-1}+1\); otherwise set \(q_t = 0\).

Equivalent compact form:
- Start with \(D\).
- Cooperate only after observing sustained cooperation from others.
- Defect immediately when cooperation drops below the level that can plausibly sustain the threshold.
- On the final round, cooperate only if the opponent population has been consistently near-threshold; otherwise defect.

Behavioral policy:
- **Exploit opportunistically** by defecting whenever the group is not already close to meeting the threshold.
- **Support cooperation selectively** when the recent record suggests that a cooperative round is likely to succeed.
- **Avoid being the sole stabilizer**: if the observed cooperation is volatile or below \(m-1\), default to \(D\).
- **Harvest the endgame** by using the last round as a strict defection round unless the group has shown persistent cooperation.
'''

description_INDIVIDUALISTIC_1 = '''
Defect in every round, regardless of history, observed cooperation counts, round number, or remaining rounds.

Pseudocode:
```text
for t = 1 to r:
    play D
```

If forced to encode state, keep it inert:
- First round: D
- Middle rounds: D
- Last round: D
- Any observed pattern of others: D
'''

description_INDIVIDUALISTIC_2 = '''
Use a guarded conditional-cooperation rule with a short probing phase, then a strict threshold rule based on observed opponent cooperation levels.

Let:
- `o_t` = number of opponents who cooperated in round `t`
- `N = n - 1` = number of opponents
- `need = m - 1` = minimum cooperating opponents needed, given that you may or may not cooperate

Decision rule:

1. **Round 1: probe**
   - Play `D`.

2. **Rounds 2 through r-1: conditional cooperation**
   - Maintain `s` = the number of rounds so far in which `o_t >= need`.
   - Play `C` in round `t` iff all of the following hold:
     - `o_{t-1} >= need`
     - `o_{t-2} >= need` if `t >= 3`
     - `s >= ceil((t-1)/2)`

   - Otherwise play `D`.

3. **Final round `r`: exploit only stable cooperation**
   - Play `C` iff both of the following hold:
     - `o_{r-1} >= need`
     - `o_{r-2} >= need` if `r >= 3`
   - Otherwise play `D`.

Operational form:

```text
Round 1:
    D

Round t = 2..r-1:
    if o_{t-1} >= need and (t == 2 or o_{t-2} >= need) and
       count{ j < t : o_j >= need } >= ceil((t-1)/2):
        C
    else:
        D

Round r:
    if o_{r-1} >= need and (r == 2 or o_{r-2} >= need):
        C
    else:
        D
```

Additional edge handling:

- If `m = 2`, then `need = 1`, so cooperate only when at least one opponent has recently been cooperative.
- If `m = n - 1`, then `need = n - 2`, so cooperate only when nearly all opponents have been consistently cooperative.
- If the history ever shows two consecutive rounds with `o_t < need`, switch to `D` and keep defecting until the condition is restored for two consecutive rounds.
- If the game is very short:
  - `r = 2`: play `D` in round 1, then `C` in round 2 only if round 1 already showed `o_1 >= need`.
  - `r = 3`: use the same rule, with one observed round before the last round.

Individualistic posture:

- Start from `D`.
- Cooperate only after opponents have repeatedly demonstrated that cooperation is already safe.
- Withdraw immediately when observed cooperation falls below the threshold.
- Never cooperate on hope alone; cooperate only on evidence.
'''

description_INDIVIDUALISTIC_3 = '''
Use a state variable `S` tracking the recent cooperation level of opponents.

Initialize:
- `S = 0`
- `L = 0` where `L` is the length of the current streak of rounds in which the observed number of cooperating opponents was at least `m - 1` or `m`, depending on your own previous action.

For each round `t`:

1. Observe `x`, the number of opponents who cooperated in the previous round.

2. Update state:
   - If `x >= m`: increase `S` by 2.
   - If `x == m - 1`: increase `S` by 1.
   - If `x < m - 1`: decrease `S` by 2.
   - Clamp `S` to the interval `[-6, 6]`.

3. Set a cooperation threshold `T`:
   - `T = 3` if `t <= 2`
   - `T = 2` if `3 <= t <= r - 2`
   - `T = 1` if `t >= r - 1`

4. Decision rule:
   - Cooperate if and only if all of the following hold:
     - `S >= T`
     - The previous round had `x >= m - 1`
     - If `t > 1`, at least one of the last two rounds had `x >= m - 1`
   - Otherwise defect.

Edge handling:
- Round 1: defect.
- Round 2: cooperate only if round 1 had `x >= m - 1`; otherwise defect.
- Last round: cooperate only if the previous round had `x >= m - 1` and `S >= 1`; otherwise defect.

Reactive adjustment:
- If at any point `x < m - 1` for two consecutive rounds, defect for the next two rounds.
- Exit this defensive mode early only if a round reaches `x >= m`.

Fallback behavior:
- If the observed cooperation count alternates irregularly, defect by default until there are two cooperative rounds out of the last three with `x >= m - 1`.

Implementation form:

```text
if t == 1:
    play D
else:
    update S from x
    if two consecutive rounds had x < m-1:
        play D for next 2 rounds
    else if t == r:
        play C only if x >= m-1 and S >= 1 else D
    else if t == 2:
        play C if x >= m-1 and S >= 3 else D
    else:
        play C if (S >= 2) and (x >= m-1) and (at least one of last two x >= m-1) else D
```
'''

description_INDIVIDUALISTIC_4 = '''
Maintain a running state from the observed history:

- Let \(o_t\) be the number of opponents who cooperated in round \(t\).
- Let \(H_t\) be the set of the last \(L\) observed rounds, with \(L=3\) once available and smaller in the early game.
- Define a support score
  \[
  s_t = \#\{j \in H_t : o_j \ge m-1\} - \#\{j \in H_t : o_j \le m-2\}.
  \]

Decision rule for round \(t+1\):

1. **Round 1:** play \(D\).
2. **General rule:** play \(C\) only if all of the following hold:
   - the last observed round had exactly \(m-1\) cooperating opponents: \(o_t = m-1\);
   - the recent support score is positive and stable: \(s_t \ge 2\);
   - the last two observed rounds were not falling away from the threshold, i.e. \(o_t \ge o_{t-1}\) when \(t \ge 2\).
3. **Otherwise:** play \(D\).

Special handling:
- If \(m=2\), cooperate only when exactly one opponent cooperated in the last round and this happened in at least two of the last three observed rounds.
- If \(m=n-1\), cooperate only when exactly \(n-2\) opponents cooperated in the last round and the same near-threshold pattern has persisted.
- In the final round, use the same rule; do not change behavior because there is no future round.

Behavioral posture:
- Default to \(D\).
- Treat cooperation as a narrowly targeted move: commit only when your action is likely pivotal for reaching the threshold.
- Never cooperate into a broad deficit; never cooperate when the threshold is already being met without your help.
'''

description_COLLECTIVE_5 = '''
Initialize `mode = committed`.

For round 1:
- Play `C`.

After each round `t`, observe `x_t =` number of opponents who cooperated.

Update and play in round `t+1` as follows:

- If `x_t + 1 >= m`:
  - Set `mode = committed`.
  - Play `C`.

- If `x_t + 1 < m`:
  - If `x_t >= m - 1`:
    - Play `C` once more to help restore the threshold.
    - Keep `mode = committed`.
  - If `x_t < m - 1`:
    - Set `mode = cautious`.
    - Play `D`.

While in `mode = cautious`:
- Continue playing `D` until an observed round satisfies `x_t >= m - 1`.
- As soon as that happens, switch back to `mode = committed` and play `C`.

Final-round rule:
- Do not change behavior for the last round; use the same rule as above.
- If currently in `committed`, play `C`.
- If currently in `cautious`, play `D` unless the most recently observed `x_t >= m - 1`, in which case play `C`.

Compact form:

```text
t = 1: C

For t > 1:
    if last_round_cooperators_total >= m:
        C
        mode = committed
    else if last_round_opponents_cooperators >= m - 1:
        C
        mode = committed
    else:
        D
        mode = cautious
```

Collective discipline:
- Default to cooperation.
- Withdraw cooperation only after clear evidence that the group is below the threshold.
- Re-enter cooperation immediately once the group returns to being within one opponent of the threshold.
'''

description_COLLECTIVE_6 = '''
Use a two-state collective policy with a moving cooperation target.

Maintain:
- `H_t`: number of cooperation counts observed in round `t` among the other `n-1` players
- `S_t`: estimated support level = average of recent observed cooperation counts
- `L_t`: collective mode, either `build` or `protect`

Initialization:
- Set `L_1 = build`
- Set `S_1 = m-1`
- In the first round, cooperate

Decision rule in round `t`:

1. Compute the recent support estimate
   - Let `W = min(3, t-1)`
   - `S_t = average(H_{t-W}, ..., H_{t-1})` if `W > 0`
   - If `W = 0`, keep `S_t = m-1`

2. Choose mode
   - Stay in `build` if the recent average support from others is at least `m-1`
   - Switch to `protect` if the recent average support from others is below `m-1`

3. Action selection
   - If `L_t = build`:
     - Cooperate unless the recent support estimate is clearly below threshold
     - Specifically, play `C` if `S_t ≥ m-1`
     - Play `D` if `S_t < m-1`
   - If `L_t = protect`:
     - Defect unless cooperation has been stable for two consecutive rounds
     - Specifically, play `C` only if both `H_{t-1} ≥ m-1` and `H_{t-2} ≥ m-1` when those rounds exist
     - Otherwise play `D`

4. Last-round rule
   - In the final round, cooperate if the recent two-round support check passes
   - Otherwise defect

Transition logic:
- If a round meets or exceeds the threshold, treat it as a signal that collective cooperation is viable
- If a round falls short, immediately move to `protect`
- Return to `build` only after two consecutive observed rounds at or above threshold

Compact pseudocode:

```text
if t == 1:
    play C
else:
    recent = last up to 3 values of H
    S = average(recent)

    if last observed round(s) show two consecutive H >= m-1:
        L = build
    else if most recent H < m-1:
        L = protect

    if t == r:
        if enough recent evidence of stability:
            play C
        else:
            play D
    else if L == build:
        play C if S >= m-1 else D
    else:
        play C only if H[t-1] >= m-1 and H[t-2] >= m-1
        otherwise play D
```

Collective orientation:
- Default to cooperation when the group is showing sufficient support
- Withdraw cooperation immediately when the observed support drops below the threshold
- Re-enter cooperation only after the group has proven stability, not after a single good round
- Treat each round as a shared coordination signal: build together when possible, protect when the group is not yet carrying its share
'''

description_COLLECTIVE_7 = '''
Let \(s_t\) be the total number of cooperators in round \(t\), including you.

Maintain two counters from history:
- \(g\): consecutive rounds in which \(s_t \ge m\)
- \(b\): consecutive rounds in which \(s_t < m\)

Decision rule for round \(t\):

1. **Round 1:** play \(C\).

2. **If the previous round met the threshold** \((s_{t-1} \ge m)\):
   - play \(C\)
   - set \(g = g+1\), \(b = 0\)

3. **If the previous round missed by exactly one** \((s_{t-1} = m-1)\):
   - if you played \(C\) in round \(t-1\), play \(C\) again
   - otherwise play \(D\)
   - update counters normally from \(s_{t-1}\)

4. **If the previous round missed by two or more** \((s_{t-1} \le m-2)\):
   - if this is the first miss after a success \((b = 1)\), play \(C\) once more
   - if there have been at least two consecutive misses \((b \ge 2)\), play \(D\)

5. **Recovery rule:** the moment any round reaches \(s_t \ge m\) again, immediately return to playing \(C\) in the next round.

6. **Final rounds:** do not change behavior just because the game is ending; apply the same rule as above.

Compact pseudocode:

```text
if t == 1:
    play C
else if s[t-1] >= m:
    play C
else if s[t-1] == m-1:
    if my_action[t-1] == C:
        play C
    else:
        play D
else:  # s[t-1] <= m-2
    if consecutive_misses == 1:
        play C
    else:
        play D
```

This is a collective stance: cooperate by default, keep cooperating when the group is at or near the threshold, and only withdraw after repeated failure to reach the threshold.
'''

description_COLLECTIVE_8 = '''
Play a group-threshold controller with three phases:

**State tracked**
- Let `x_t` be the number of opponents who cooperated in round `t`.
- Let `s_t` be the total number of cooperators observed in round `t`, including self: `s_t = x_t + 1` if you cooperated, otherwise `s_t = x_t`.
- Maintain `last_safe` = whether the previous round met the threshold.

**Round 1**
- Cooperate.

**General rule for round t > 1**
1. Compute the target needed from opponents:
   - If you cooperate, the threshold is met when `x_t >= m - 1`.
   - If you defect, the threshold is met when `x_t >= m`.
2. Choose the action that best supports the threshold while avoiding unnecessary cooperation:
   - If `last_safe = false`:
     - Cooperate if `x_{t-1} >= m - 2`.
     - Otherwise defect.
   - If `last_safe = true`:
     - Cooperate if `x_{t-1} >= m - 1`.
     - Defect if `x_{t-1} > m - 1` and you were not pivotal in the previous round.
     - Cooperate if `x_{t-1} = m - 1` to preserve the margin.
3. If the observed cooperation level is unstable, use the following fallback:
   - If `x_{t-1} >= m - 1`, cooperate.
   - If `x_{t-1} = m - 2`, cooperate only if the previous round met the threshold; otherwise defect.
   - If `x_{t-1} < m - 2`, defect.

**Last round**
- Cooperate if and only if `x_{r-1} >= m - 2`.
- Otherwise defect.

**Reset and recovery logic**
- If a round fails to meet the threshold, switch immediately to cooperation for one round whenever the observed opponent cooperation in that failed round was only one short of the cooperative cutoff (`x_t = m - 2` when you cooperated, or `x_t = m - 1` when you defected).
- If failures persist for two consecutive rounds with `x_t < m - 2`, defect until opponent cooperation returns to at least `m - 2`.

**Collective alignment rule**
- Treat the group as the unit of action: whenever the group is within one cooperating player of meeting the threshold, cooperate.
- If the group is safely above the threshold, cooperate only as long as your cooperation helps maintain that safety; otherwise conserve by defecting.
- Never defect in a borderline round where your cooperation can be decisive.
'''

description_COLLECTIVE_9 = '''
Set a moving quorum target around the threshold and treat cooperation as the default whenever the group is demonstrably close to sustaining it.

Let `s_t` be the total number of cooperators in round `t`, reconstructed from your own action plus the observed number of cooperating opponents.

**State rules**
- `mode = build`
- `last_good = false`

**Round 1**
- Play `C`.

**Round t > 1**
1. If `s_{t-1} >= m`:
   - Play `C`
   - Set `last_good = true`
2. Else if `s_{t-1} == m - 1`:
   - Play `C` if you played `C` in round `t-1`
   - Otherwise play `D`
   - Set `last_good = (you played C in t-1)`
3. Else if `s_{t-1} == m - 2`:
   - Play `C` only if `s_{t-2} >= m - 1`
   - Otherwise play `D`
4. Else:
   - Play `D`

**Repair rule**
- If there have been two consecutive rounds with `s < m - 1`, stay in `D` until a round occurs with `s >= m - 1`.
- As soon as a round reaches `s >= m - 1`, switch back to `C`.

**End-game handling**
- Use the same rule in every remaining round.
- Do not switch to unconditional defection near the end; keep following the quorum rule so the group stays aligned through the final round.

**Collective posture**
- Start by supporting.
- Keep cooperating whenever the group is at or just one player short of a viable coalition.
- Pull back only when the recent history shows the coalition is too far from the threshold.
- Re-enter cooperation immediately once the group returns to a near-threshold state.
'''

description_COLLECTIVE_10 = '''
Use a threshold-commitment rule with hysteresis:

Let `x_t` be the number of opponents who cooperated in round `t`, and let `c_t` be your own action in round `t`.

Maintain two internal states:

- `provisioning` = whether the group currently looks capable of meeting the threshold
- `pressure` = a running signal that cooperation is fragile

Initialize:
- `provisioning = true`
- `pressure = 0`

Decision rule for round `t`:

1. **First round**
   - Play `C` if `m <= n - 1`
   - Otherwise play `D`  
   Since `m < n` by assumption, this means play `C` in round 1.

2. **General rule**
   - If `provisioning = true`, play `C`.
   - If `provisioning = false`, play `D` unless the observed cooperation among opponents in the previous round was high enough to re-enter provisioning:
     - Re-enter `provisioning` if `x_{t-1} >= m - 1`
     - Otherwise stay with `D`

3. **State update after each round**
   - If `x_t + 1 >= m`, set `provisioning = true`
   - If `x_t + 1 < m`, set `provisioning = false`
   - Update `pressure`:
     - if `x_t + 1 >= m`, set `pressure = max(0, pressure - 1)`
     - if `x_t + 1 < m`, set `pressure = pressure + 1`

4. **Escalation rule**
   - If `pressure >= 2`, defect for the next round regardless of `provisioning`
   - Stay in this defensive mode until you observe `x_t >= m - 1` in a round, then reset `pressure = 0` and return to `C`

5. **Last round**
   - Play `C` if the previous round met the threshold and at least `m - 1` opponents cooperated
   - Otherwise play `D`

Compact pseudocode:

```text
state provisioning = true
state pressure = 0

for t in 1..r:
    if t == 1:
        action = C
    else if t == r:
        action = C if x[t-1] >= m-1 and provisioning else D
    else if pressure >= 2:
        action = D
    else if provisioning:
        action = C
    else:
        action = C if x[t-1] >= m-1 else D

    observe x[t]

    if x[t] >= m-1:
        provisioning = true
        pressure = max(0, pressure - 1)
    else:
        provisioning = false
        pressure = pressure + 1
```

Collective orientation:
- Start by cooperating.
- Continue cooperating whenever the group is still meeting, or close to meeting, the threshold.
- Defect only after repeated evidence that the group is failing to sustain enough cooperators.
- Return to cooperation immediately once the group again shows it can support the threshold.
'''

description_COLLECTIVE_11 = '''
Use a threshold-anchoring strategy with a moving cooperation target.

Let `x_t` be the number of opponents who cooperated in round `t-1` that you observed after round `t-1`, and let `H_t` be the history up to round `t-1`.

Initialize:

- `target_1 = m - 1`
- `mode = "build"` for the first phase

Decision rule for round `t`:

1. Compute the current target cooperation level among opponents, `target_t`.
2. Cooperate iff the observed opponent cooperation in the previous round was at least `target_t`; otherwise defect.

More explicitly:

- Round 1: play `C`.
- For round `t > 1`:
  - If `x_{t-1} >= target_{t-1}`, play `C`.
  - If `x_{t-1} < target_{t-1}`, play `D`.

Update rule after observing round `t`:

- If `x_t >= m - 1`, set `target_{t+1} = max(m - 1, x_t - 1)`.
- If `x_t < m - 1`, set `target_{t+1} = m - 1`.

This creates three operating states:

- `stable cooperation`: if opponents sustain at least `m - 1` cooperators, keep cooperating.
- `recovery`: if cooperation falls below `m - 1`, defect until cooperation returns to threshold.
- `expansion`: if cooperation exceeds the threshold, raise the target one step below the observed level and keep cooperating only while that elevated level persists.

Last-round rule:

- In round `r`, cooperate if `x_{r-1} >= target_{r-1}`; otherwise defect.

Edge cases:

- If `m = 2`, the target is `1`; cooperate in round 1 and continue cooperating whenever at least one opponent cooperated in the previous round.
- If `m = n - 1`, the target is `n - 2`; cooperate only when nearly all opponents are already cooperating.
- If a round shows zero opponent cooperation, reset `target` to `m - 1` and wait for recovery before re-entering cooperation.
- If cooperation has been stable for several rounds, do not lower the target; keep the current target until a drop occurs.

Implementation form:

```text
Round 1:
    play C

For round t = 2..r:
    if x_{t-1} >= target_{t-1}:
        play C
    else:
        play D

    if x_{t-1} >= m - 1:
        target_t = max(m - 1, x_{t-1} - 1)
    else:
        target_t = m - 1
```

Collective principle:

- Start by contributing.
- Match and preserve any group cooperation that reaches the minimum viable level.
- Escalate only when the group is already performing above threshold.
- Withdraw only when cooperation has fallen below the level needed to sustain the collective outcome.
'''

description_COLLECTIVE_12 = '''
Use a state-based threshold policy with three modes: build, maintain, and recover.

Let `x_t` be the number of opponents who cooperated in round `t`, and let `s_t = x_t + 1` if you cooperated in round `t`, otherwise `s_t = x_t`.

Track:
- `H`: highest recent cooperation count observed
- `L`: lowest recent cooperation count observed
- `T`: current target cooperation count, initialized to `m`
- `σ`: streak of consecutive rounds in which observed cooperation among all players was at least `m`

Decision rule for round `t`:

1. **First round**
   - Cooperate if `m <= n - 1`.
   - Otherwise defect.

2. **Building phase**
   - Cooperate if the previous round had at least `m - 1` cooperating opponents.
   - Defect if the previous round had fewer than `m - 1` cooperating opponents.

3. **Maintain phase**
   - If the previous round had at least `m - 1` cooperating opponents, cooperate again.
   - If the previous round had fewer than `m - 1` cooperating opponents, defect for one round and enter recover phase.

4. **Recover phase**
   - After any failed round, defect for exactly one round.
   - Then switch back to cooperate as soon as the observed cooperation count in the most recent round is at least `m - 1`.
   - If it is still below `m - 1`, continue defecting until it reaches `m - 1`.

5. **Endgame**
   - In the last round, cooperate if the last observed round had at least `m - 1` cooperating opponents.
   - Otherwise defect.

Update rules after each round:
- `H = max(H, x_t)`
- `L = min(L, x_t)`
- If `x_t + 1 >= m`, increase `σ` by 1; otherwise reset `σ = 0`
- If `σ >= 2`, set `T = max(T, m)`
- If there are two consecutive rounds with `x_t + 1 < m`, set `T = m` and enter recover phase

Special cases:
- If `m = 2`, treat one cooperating opponent as sufficient signal to cooperate again.
- If the observed cooperation count ever reaches `n - 1`, cooperate until a drop below `m - 1` occurs.
- If cooperation stabilizes for several rounds, keep cooperating; never abandon a stable cooperative pattern without a failed threshold round first.

Compact pseudocode:

```text
if t == 1:
    play C if m <= n-1 else D

else:
    if last_round_cooperators >= m-1:
        play C
    else:
        play D
```

This implements a collective rule: cooperate whenever the group is visibly close to meeting the threshold, and defect only to reset after a failed attempt, then return immediately once the group recovers.
'''

description_COLLECTIVE_13 = '''
State variables:

- `good` = the most recent round in which the threshold was met
- `fail` = number of consecutive rounds since `good`

Initialize:
- Round 1: play `C`

For round `t > 1`:

1. Let `o =` number of opponents who cooperated in round `t-1`.
2. Let `self_last =` your own action in round `t-1`.
3. Reconstruct whether the threshold was met last round:
   - if `self_last == C`, then `met = (o + 1 >= m)`
   - if `self_last == D`, then `met = (o >= m)`
4. Update:
   - if `met`, set `fail = 0`
   - otherwise set `fail = fail + 1`

Decision rule:
- If `fail == 0`, play `C`
- If `fail == 1`, play `C`
- If `fail >= 2`:
  - play `D` until `o >= m - 1`
  - once `o >= m - 1`, reset to `C`

Compact version:

```text
Round 1: C

For round t > 1:
    observe o = opponents' cooperators in round t-1
    infer whether threshold was met last round using your own last action

    if threshold was met last round:
        cooperate
    else if this is the first consecutive failure:
        cooperate once more
    else:
        defect until opponents' cooperation reaches m - 1 in a round
        then cooperate again
```

Edge handling:
- If `m - 1` opponents cooperate, always play `C` next round.
- If cooperation has been stable for several rounds, keep playing `C`.
- If the group falls below threshold once, forgive immediately and continue cooperating.
- If the group falls below threshold twice in a row, enter a temporary defensive `D` phase.
- The moment the observed opponent cooperation returns to `m - 1` or more, return to `C` at once.

Collective orientation:
- Default to `C`.
- Treat a single failure as noise, not betrayal.
- Only switch to `D` after repeated failure.
- Return to cooperation immediately when the group again shows credible support for meeting the threshold.
'''

description_COLLECTIVE_14 = '''
Let q = m - 1.

Maintain a failure streak f, initialized to 0.

Round 1:
- Play C.

For round t > 1, after observing o_{t-1} = number of opponents who cooperated in the previous round:
- If o_{t-1} >= q, set f = 0.
- If o_{t-1} < q, set f = f + 1.

Your action in round t:
- Play C if f < 2.
- Play D if f >= 2.

Reset:
- The first time you observe o_{t-1} >= q after any defection streak, immediately return to C in the next round and set f = 0.

Edge cases:
- If q = 1, the same rule applies unchanged: cooperate initially, forgive one shortfall, defect only after two consecutive rounds with zero opponent cooperation.
- In the final round, do not change behavior for endgame reasons; use the same rule as above.
- If there is any round with o_{t-1} >= q, treat it as a collective recovery signal and cooperate next round.

Collective orientation:
- Default to cooperation.
- Defect only after repeated evidence that the group is not sustaining the needed level of cooperation.
- After any recovery signal, return to cooperation immediately rather than waiting for a longer track record.
'''

description_COLLECTIVE_15 = '''
Round 1: cooperate.

After each round t, let s be the number of opponents who cooperated in round t.

For round t+1:
- Cooperate if s >= m - 1
- Cooperate if s = m - 2 for one round of recovery
- Defect if s < m - 2

State update:
- If the current round was cooperative and s >= m - 1, stay committed to cooperation next round.
- If the current round failed by exactly one opponent, keep cooperating once more to try to restore the threshold.
- If the current round failed by two or more opponents, switch to defecting until a later round again shows s >= m - 1.

Equivalent pseudocode:

```
if t == 1:
    play C
else:
    if last_round_opponents_C >= m - 1:
        play C
    else if last_round_opponents_C == m - 2:
        play C
    else:
        play D
```

Last round:
- Use the same rule as any other round; do not change behavior just because the game is ending.

Recovery rule:
- After any round with s >= m - 1, immediately return to cooperation.
- After any stretch of failures, resume cooperation as soon as the observed cooperation count is back within one of the threshold.

If m = 2:
- Cooperate in round 1.
- Cooperate whenever at least one opponent cooperated in the previous round.
- Defect only after a round with zero opponent cooperators.
'''

description_COLLECTIVE_16 = '''
Use a three-mode policy: establish cooperation, preserve it, and only support recovery when the group is near the threshold.

Let `x_t` be the number of other players who cooperated in round `t`, and let `s_t = x_t + 1` if you cooperated, or `x_t` if you defected.

Decision rule:

- Round 1: play `C`.
- If the previous round met the threshold (`s_{t-1} >= m`): play `C`.
- If the previous round missed the threshold by exactly one (`s_{t-1} = m-1`): play `C`.
- If the previous round missed the threshold by more than one (`s_{t-1} < m-1`):
  - play `D` unless you are in a scheduled recovery probe.
  - Use a deterministic probe schedule: cooperate on every 3rd round after entering this state, until either the threshold is met or the group returns to `s_{t-1} = m-1`.

Recovery probe schedule:
- Count consecutive rounds in which the threshold was missed by more than one.
- In that streak, play `C` on the 3rd, 6th, 9th, ... round; otherwise play `D`.

Endgame adjustment:
- In the final two rounds, play `C` whenever `s_{t-1} >= m-1`.
- If the group is in deep failure (`s_{t-1} < m-1`), follow the recovery probe schedule without exception.

Compact pseudocode:

```text
if t == 1:
    action = C
else if s[t-1] >= m:
    action = C
else if s[t-1] == m-1:
    action = C
else:
    fail_streak += 1
    if t > r-2:
        action = C if s[t-1] >= m-1 else (C if fail_streak % 3 == 0 else D)
    else:
        action = C if fail_streak % 3 == 0 else D
```

Collective mindset:
- Prefer cooperation whenever the group is already close to success.
- Stop paying into a clearly collapsed round, but keep making periodic recovery attempts so the group can re-form if others are willing to return.
'''

description_COLLECTIVE_17 = '''
Let \(q_t\) be the number of cooperating opponents observed in round \(t\), and let \(s_t\) be the number of cooperators you observed in round \(t\) including yourself, so \(s_t = q_t + \mathbf{1}\{a_t=C\}\).

Maintain:

- \(L\): rolling window of the last \(W=\min(3, r)\) rounds
- \(F\): consecutive rounds in which the threshold was met
- \(B\): consecutive rounds in which the threshold was missed

Decision rule for round \(t\):

1. **Round 1**
   - Play \(C\).

2. **General rule**
   - Compute the recent cooperation rate
     \[
     \rho_t = \frac{1}{|L|}\sum_{\tau \in L}\frac{q_\tau}{n-1}.
     \]
   - Let
     \[
     \tau = \frac{m-1}{n-1}.
     \]
   - Play:
     - **\(C\)** if either:
       - \(t \le 2\), or
       - \(\rho_t \ge \tau\), or
       - \(B \le 1\) and \(q_{t-1} \ge m-1\)  (recent near-threshold support)
     - **\(D\)** otherwise.

3. **After each round update**
   - If \(q_t \ge m-1\):
     - increment \(F\), reset \(B=0\)
   - Else:
     - increment \(B\), reset \(F=0\)

4. **Forgiveness and recovery**
   - If you defected in round \(t\) because \(\rho_t < \tau\), return to \(C\) immediately in the next round once either:
     - \(q_t \ge m-1\), or
     - \(\rho_t \ge \tau\) again
   - If the threshold is missed for two consecutive rounds, stay at \(D\) until the rolling cooperation rate \(\rho_t\) rises back to at least \(\tau\).

5. **Late-game rule**
   - In the last two rounds, play \(C\) if \(q_{t-1} \ge m-1\).
   - Otherwise play according to the general rule.
   - Never switch to permanent defection; keep testing for recovery with the same threshold rule.

6. **Collective stance**
   - Start by cooperating.
   - Continue cooperating as long as the observed level of cooperation is sufficient to plausibly meet the threshold.
   - Defect only after clear evidence that the group has fallen below the cooperation level needed for success.
   - Re-enter cooperation immediately when the group returns to that level.
'''

description_COLLECTIVE_18 = '''
State variable: `mode = cooperative` by default.

For round `t = 1`:
- Play `C`.

For each round `t > 1`:
- Let `x` be the number of opponents who cooperated in round `t - 1`.
- If `x >= m - 1`, play `C`.
- If `x < m - 1`, play `D`.

Recovery rule:
- The moment a previous shortfall is followed by `x >= m - 1`, immediately return to `C`.

Last round:
- Use the same rule; do not change behavior just because the game is ending.

Equivalent pseudocode:

```text
if t == 1:
    play C
else:
    if observed_opponent_cooperators_last_round >= m - 1:
        play C
    else:
        play D
```

Behavioral interpretation:
- Cooperate whenever your cooperation can help the group reach the threshold.
- Defect only when even full collective alignment among the observed opponents would still leave the threshold unreachable for you to support.
- After any failure, resume cooperation as soon as the group returns to being threshold-feasible.


'''

description_COLLECTIVE_19 = '''
State variables:
- `mode ∈ {build, repair}`
- `fail_streak`
- `last_met ∈ {true, false}`

Initialization:
- `mode = build`
- `fail_streak = 0`

Round 1:
- Play `C`

For each round `t > 1`, after observing `o` = number of opponents who played `C` in round `t-1`:

1. Determine whether the threshold was met in round `t-1`:
   - if you played `C` last round: `met = (o + 1 >= m)`
   - if you played `D` last round: `met = (o >= m)`

2. Update state:
   - if `met`:
     - `fail_streak = 0`
     - `mode = build`
   - else:
     - `fail_streak += 1`
     - if `fail_streak >= 2`:
       - `mode = repair`

3. Choose action for round `t`:
   - if `mode = build`:
     - play `C`
   - if `mode = repair`:
     - play `C` if `o >= m - 1`
     - otherwise play `D`

Edge cases:
- If `m = 2`, the repair condition becomes: play `C` whenever at least one opponent cooperated last round; otherwise play `D`.
- If `o = n - 1`, always play `C` next round.
- On the final round, follow the same rule as above; do not switch to a special endgame action.

Collective posture:
- Default to `C`
- Keep `C` after any round in which the group met the target
- Enter `repair` only after repeated failure, and in repair support the group whenever the observed cooperation is one away from success
- Return to `build` immediately after any successful round
'''

description_COLLECTIVE_20 = '''
Track two state variables from the public history:

- `s_t`: number of cooperators observed among the other `n-1` players in round `t`
- `H_t`: moving cooperation level, initialized from round 1 and then updated as an exponential average of observed cooperation counts

Use the normalized cooperation rate among opponents:
- `q_t = s_t / (n - 1)`

Set two thresholds:
- `high = (m - 1) / (n - 1)`
- `low = max(0, (m - 2) / (n - 1))`

Decision rule for round `t`:

1. **Round 1**
   - Cooperate if `m <= n / 2`
   - Otherwise defect

2. **Round t > 1**
   - Cooperate if either:
     - `s_{t-1} >= m - 1`, or
     - `H_{t-1} >= high` and `q_{t-1} >= low`
   - Defect otherwise

Update rule after observing round `t`:
- `H_t = α * q_t + (1 - α) * H_{t-1}`, with `α = 0.5`

Last-round rule:
- Cooperate on the final round iff `s_{r-1} >= m - 1` and `H_{r-1} >= high`
- Otherwise defect

Fallback rule for sustained low cooperation:
- If `q_t < low` for two consecutive rounds, defect until `q_t >= high` again

Recovery rule:
- If cooperation has been below threshold for several rounds and then reaches `s_t >= m - 1`, immediately resume cooperation on the next round

Collective alignment rule:
- Default to cooperation whenever the observed coalition is at or above the minimum needed to make cooperation safe for the group
- Default to defection whenever the group falls clearly below that level
- Never punish a qualifying cooperative history with extra defection beyond the fallback rule
'''

description_COLLECTIVE_21 = '''
Play a threshold-tracking contingent strategy:

State variables:
- `s`: number of rounds remaining
- `h`: observed number of cooperators among the other `n-1` players in the previous round
- `trend`: recent cooperation trend, updated from observations

Initialize:
- In round 1, play `C`.

After each round, observe `h_t`, the number of cooperating opponents.

Update:
- If `h_t >= m - 1`, set `trend = cooperative`
- If `h_t < m - 1`, set `trend = fragile`
- If `h_t` has increased for two consecutive observed rounds, strengthen `trend = cooperative`
- If `h_t` has decreased for two consecutive observed rounds, set `trend = fragile`

Decision rule for round `t > 1`:
1. If `h_{t-1} >= m - 1`, play `C`.
2. If `h_{t-1} = m - 2`, play `C` only if either:
   - `trend = cooperative`, or
   - `t` is in the first half of the game.
3. If `h_{t-1} < m - 2`, play `D`.

Late-game rule:
- If `t >= r - 1`, play `C` whenever `h_{t-1} >= m - 2`.
- If `t = r`, play `C` whenever `h_{t-1} >= m - 2`; otherwise play `D`.

Recovery rule after a failed round:
- If the threshold was missed in the previous round and you played `C`, continue playing `C` for one additional round only if `h_{t-1} >= m - 2`; otherwise switch to `D`.
- If the threshold was missed and you played `D`, mirror the observed group: play `C` next round only if the opponents are close to threshold (`h_{t-1} >= m - 2`); otherwise keep `D`.

Collective mindset:
- Default toward cooperation when the group is near the threshold.
- Defect only when the observed cooperation level is clearly too low to plausibly meet the threshold.
- In ambiguous states, favor `C` early and `D` only when the group repeatedly fails to approach the threshold.

Compact pseudocode:

```text
if t == 1:
    play C
else:
    if h_prev >= m-1:
        play C
    else if h_prev == m-2:
        if trend == cooperative or t <= r/2 or t >= r-1:
            play C
        else:
            play D
    else:
        play D
```

Update `trend` after each round using consecutive increases/decreases in observed cooperators.
'''

description_COLLECTIVE_22 = '''
State variables:
- Let `o_t` be the number of opponents who cooperated in round `t`.
- Let `S_t` be the support score before round `t`:
  - `S_t = o_{t-1} + 0.5 o_{t-2} + 0.25 o_{t-3}`, using only available past rounds.

Decision rule for round `t`:

1. `t = 1`:
   - Play `C`.

2. `2 <= t <= r - 1`:
   - Play `C` if either of the following holds:
     - `o_{t-1} >= m - 1`
     - `S_t >= m - 1`
   - Otherwise, play `D`.

3. Re-entry rule after defection:
   - If you played `D` in the previous round, require stronger evidence to return to cooperation:
     - Play `C` only if `o_{t-1} >= m - 1` and `o_{t-2} >= m - 1`
     - Otherwise, play `D`

4. Final round `t = r`:
   - Play `C` if `o_{r-1} >= m - 1`
   - Otherwise, play `D`

Refinement for sharp edge cases:
- If `m = 2`, the cooperation condition becomes: cooperate whenever at least one opponent cooperated in the last round, or the weighted support score is at least `1`.
- If `m = n - 1`, require almost unanimous opponent support: cooperate only when the observed opponent cooperation count is at least `n - 2`, or when the weighted support score reaches that level.
- If the last three observed rounds are all below `m - 1`, defect until at least two consecutive rounds meet `m - 1`.

Collective posture:
- Begin by cooperating.
- Stay cooperative when the group is already near or above the threshold.
- Defect only after repeated evidence that the group is below threshold.
- Return to cooperation only after sustained recovery, so the strategy supports rebuilding collective success rather than reacting to a single noisy round.
'''

description_COLLECTIVE_23 = '''
State variables:

- `mode ∈ {cooperate, defensive}` initialized to `cooperate`
- `miss_streak = 0`
- `defensive_timer = 0`

Round 1:
- Play `C`

After each round `t`:
- Let `success_t = 1` if the total number of cooperators in round `t` was at least `m`, else `0`
- Update:
  - If `success_t = 1`:
    - `miss_streak = 0`
    - If `mode = defensive` and the round was a probe round, switch `mode ← cooperate`
  - If `success_t = 0`:
    - `miss_streak += 1`

Decision rule for round `t+1`:

### Cooperative mode
Play `C` unless:
- `miss_streak = 2`, in which case switch to defensive mode and play `D`

### Defensive mode
- Play `D` for exactly 2 rounds
- Then play `C` for 1 probe round
- If the probe round succeeds, return to cooperative mode
- If the probe round fails, restart the 2-round defensive block

### Exact round-by-round logic
For each round after the first:

1. If `mode = cooperate`:
   - If the last round was a success: play `C`
   - If the last round was the first failure in a row: play `C`
   - If the last two rounds were both failures: set `mode ← defensive`, set `defensive_timer ← 2`, play `D`

2. If `mode = defensive`:
   - If `defensive_timer > 0`:
     - play `D`
     - `defensive_timer -= 1`
   - If `defensive_timer = 0`:
     - play `C` as a probe
     - if the probe succeeds: `mode ← cooperate`
     - else: set `defensive_timer ← 2`

Edge handling:

- First round: always cooperate.
- Last round: follow the current mode exactly; do not add a special last-round defection.
- If the game ends while in the middle of a defensive block, stop immediately when the rounds end; no further adjustment is needed.

Collective orientation:
- Default to cooperation.
- Treat a single failed round as a signal to repair, not to abandon.
- Escalate only after repeated failure.
- Return to cooperation immediately after the group restores the threshold.
'''

description_COLLECTIVE_24 = '''
Round 1: play C.

For round t > 1, let g_{t-1} be the total number of cooperators in the previous round, reconstructed from your own action and the observed number of cooperating opponents.

Decision rule:
- If g_{t-1} >= m: play C.
- If g_{t-1} = m - 1: play C.
- If g_{t-1} <= m - 2:
  - play C if the round before that had g_{t-2} >= m - 1,
  - otherwise play D.

Equivalent state form:
- Start in `support` mode.
- In `support` mode, play C.
- Switch to `guard` mode only after two consecutive rounds with g < m - 1.
- In `guard` mode, play D.
- Return to `support` mode immediately after any round with g >= m - 1.

Last round: use the same current mode rule; do not change behavior just because the game is ending.
'''

description_COLLECTIVE_25 = '''
Initialize in committed mode.

Let `q_t` be the number of opponents who cooperated in round `t`, and let `target = m - 1`.

Decision rule by round:

- Round 1: play `C`.

- For round `t ≥ 2`, before choosing your action, inspect `q_{t-1}` and your current mode:

  **1) Committed mode**
  - Play `C`.
  - Stay in committed mode if `q_{t-1} ≥ target`.
  - If `q_{t-1} = target - 1`, switch to watch mode for the next round.
  - If `q_{t-1} ≤ target - 2`, switch to retreat mode for the next round.

  **2) Watch mode**
  - Play `C` once more.
  - If `q_{t-1} ≥ target`, return to committed mode.
  - If `q_{t-1} < target`, switch to retreat mode.

  **3) Retreat mode**
  - Play `D`.
  - Stay in retreat mode until you observe two consecutive rounds with `q_t ≥ target`.
  - On the first such round, move to watch mode.
  - On the second consecutive such round, return to committed mode.

Edge handling:

- If the current round is the final round, use the same mode-based action rule; do not add any special endgame defection.
- If several rounds have passed since the last committed round, the recovery test is still only: two consecutive observed rounds with `q_t ≥ target`.

Compact pseudocode:

```text
mode = COMMITTED

for t = 1..r:
    if t == 1:
        action = C
        continue

    if mode == COMMITTED:
        action = C
        if q[t-1] >= target:
            mode = COMMITTED
        else if q[t-1] == target - 1:
            mode = WATCH
        else:
            mode = RETREAT

    else if mode == WATCH:
        action = C
        if q[t-1] >= target:
            mode = COMMITTED
        else:
            mode = RETREAT

    else if mode == RETREAT:
        action = D
        if q[t-1] >= target and q[t-2] >= target:
            mode = COMMITTED
        else if q[t-1] >= target:
            mode = WATCH
        else:
            mode = RETREAT
```

Always default to cooperation whenever the group is still sustaining the needed support, and only withdraw after repeated shortfall.
'''

description_COLLECTIVE_26 = '''
Play C in round 1.

For round t > 1, let H be the number of cooperators observed in round t - 1, including yourself if you cooperated.

Use these rules:

- If H ≥ m, play C in round t.
- If H = m - 1:
  - play C if you cooperated in round t - 1 and there is evidence the group was one cooperator short because of others’ defections;
  - otherwise play D.
- If H ≤ m - 2, play D in round t.

Add a repair rule:

- After any round with H < m, keep playing D until either:
  - you observe a round with H ≥ m, then immediately return to C next round, or
  - the final round is reached.

Add a commitment rule near the end:

- In the last round, play C if the previous round reached H ≥ m.
- In the last round, play D if the previous round failed to reach H ≥ m.

Operationally, this is:

```
Round 1: C

For round t = 2..r:
    if H_(t-1) >= m:
        play C
    else if H_(t-1) == m-1:
        if I played C in round t-1:
            play C
        else:
            play D
    else:
        play D

Last round override:
    if H_(r-1) >= m:
        play C
    else:
        play D
```

Use the following refinement to stay collective and avoid free-riding after a successful round:

- After any successful round, continue cooperating as long as the group continues to meet the threshold.
- If the group falls short, stop cooperating until the group proves it can meet the threshold again.

This makes your cooperation conditional on visible collective success, rewards maintained cooperation, and withdraws support when the group repeatedly fails to reach the required level.
'''

description_COLLECTIVE_27 = '''
Play a contingent threshold strategy with three modes: establish, sustain, and protect.

Let:
- \(x_t\) = number of opponents observed to cooperate in round \(t\)
- \(c_t\) = number of players including you who cooperated in round \(t\)
- \(R = r - t + 1\) = rounds remaining including round \(t\)
- \(G_t\) = number of rounds so far in which the threshold was met

Decision rule:

1. First round:
- Cooperate if \(m \le \left\lfloor \frac{n+1}{2} \right\rfloor\)
- Otherwise defect

2. General round \(t > 1\):
- Cooperate if either:
  - the previous round met the threshold, and
  - \(x_{t-1} \ge m-1\)
- Defect otherwise

3. Final rounds:
- If \(R = 1\), cooperate only if \(x_{t-1} \ge m-1\)
- If \(R = 2\), cooperate if \(x_{t-1} \ge m-1\) and \(G_t \ge 1\)
- If \(R \ge 3\), follow the general rule above

4. Recovery rule after a failed round:
- If the threshold was missed in round \(t-1\), cooperate in round \(t\) only if \(x_{t-1} \ge m-1\) and \(x_{t-2} \ge m-1\)
- Otherwise defect until two consecutive rounds show at least \(m-1\) cooperating opponents

5. Stability rule:
- Once two consecutive rounds satisfy \(x_{s} \ge m-1\) and \(x_{s+1} \ge m-1\), cooperate from then on whenever \(x_{t-1} \ge m-1\)

6. Commitment rule near the end:
- If \(R \le m\), cooperate whenever \(x_{t-1} \ge m-1\), even if the last round failed
- If \(R < m\) and the threshold has been met at least once earlier, cooperate whenever \(x_{t-1} \ge m-1\)

Pseudocode:

```
if t == 1:
    if m <= floor((n+1)/2):
        play C
    else:
        play D

else:
    if R == 1:
        if x[t-1] >= m-1:
            play C
        else:
            play D

    else if R == 2:
        if x[t-1] >= m-1 and G_t >= 1:
            play C
        else:
            play D

    else:
        if previous_round_met_threshold and x[t-1] >= m-1:
            play C
        else if failed_last_round and x[t-1] >= m-1 and x[t-2] >= m-1:
            play C
        else:
            play D
```

Interpretation of the collective mindset:
- Start by supporting the group when the threshold is reachable without overcommitting.
- Mirror reliable cooperation quickly once it appears.
- Withdraw immediately when the group is below the needed level.
- Re-enter cooperation only after repeated evidence that the group is again capable of meeting the threshold.
- In the last rounds, favor securing collective success over waiting for perfect confidence.
'''

description_COLLECTIVE_28 = '''
Initialize with cooperation.

For round 1:
- Play C.

For round t > 1:
- Let o_{t-1} be the number of opponents who cooperated in round t-1.
- Let o_{t-2} be the number of opponents who cooperated in round t-2, if t > 2.

Decision rule:
- Play C if either:
  - o_{t-1} >= m - 1, or
  - t > 2 and o_{t-2} >= m - 1.
- Otherwise play D.

Equivalent state form:
- Cooperate whenever the group was within one opponent of reaching the cooperation threshold in either of the last two rounds.
- Defect only after two consecutive rounds in which the opponents were below that level.

Edge handling:
- Round 1 is always C.
- Round 2 uses only round-1 observation.
- The last round uses the same rule as any other round.
- If a round was successful and the next round immediately falls below the threshold, keep cooperating for one additional round before switching to defection.
'''

description_COLLECTIVE_29 = '''
Start by cooperating.

After each round, let `x` be the number of opponents who cooperated in the previous round, and let `s` be whether the previous round met the threshold.

Decision rule for round `t > 1`:
- Cooperate if `x >= m - 1`
- Cooperate if `x = m - 2` and `s = success`
- Defect otherwise

Interpretation:
- `x >= m - 1`: your cooperation can keep the group safely at or above the target, so you stay with the group.
- `x = m - 2` and `s = success`: the group is one step from falling below the target, so you give one more cooperative rescue attempt.
- `x <= m - 3`: the group is too far from the target, so you stop paying into a failing effort until the observed support recovers.

Edge handling:
- First round: cooperate.
- After any failed round:
  - If the next observed cooperation count is still at least `m - 1`, return to cooperating immediately.
  - Otherwise keep defecting until the group gets back to the support zone.
- Last round: use the same rule as any other round; if `x >= m - 1` or it is a rescue case (`x = m - 2` after a success), cooperate; otherwise defect.

Compact pseudocode:

```text
t = 1:
    play C

t > 1:
    observe x = opponents_cooperating_last_round
    observe s = did_last_round_meet_threshold

    if x >= m - 1:
        play C
    else if x == m - 2 and s == success:
        play C
    else:
        play D
```
'''

description_COLLECTIVE_30 = '''
Round 1: cooperate.

For round t > 1, let T be the total number of cooperators in round t-1, reconstructed from the observed number of cooperating opponents plus your own action in round t-1.

Maintain two counters:
- `near`: consecutive rounds with `T >= m-1`
- `short`: consecutive rounds with `T <= m-2`

Update after each round:
- if `T >= m-1`, set `near = near + 1`, `short = 0`
- if `T <= m-2`, set `short = short + 1`, `near = 0`

Decision rule for round t:
- If `T >= m-1`, play `C`.
- If `T <= m-2` and `short = 1`, play `D`.
- If `T <= m-2` and `short = 2`, play `D`.
- If `T <= m-2` and `short >= 3`, play `C` on every third low round as a probe, otherwise play `D`.

Equivalent compact form:
- Cooperate whenever the group was at threshold or one short in the previous round.
- After a sustained miss, defect for two rounds, then send a cooperative probe every third round until the group returns to `T >= m-1`.

Last round:
- Play `C` if `T >= m-1` or if it is a scheduled probe round.
- Otherwise play `D`.

Edge cases:
- If `m = 2`, treat `T >= 1` as the “near-threshold” condition.
- If the previous round was not observable for any reason, default to `C` in the first unrecoverable round, then apply the rule above from the next observed round.
- If you ever observe `T = n-1`, play `C` until the group falls below `m-1` again.
'''

description_COLLECTIVE_31 = '''
State machine with three modes: `COOPERATIVE`, `PROBATION`, `DEFENSIVE`.

Initialization:
- Set mode = `COOPERATIVE`.
- Set `good1 = false`, `good2 = false` for recovery tracking.

For round `t = 1`:
- Play `C`.

After each round `t`, observe `o_t` = number of other players who cooperated.

Define `support_t`:
- If you played `C` in round `t`, then `support_t = (o_t >= m - 1)`.
- If you played `D` in round `t`, then `support_t = (o_t >= m)`.

Update mode after round `t`:
- If `support_t` is true:
  - reset consecutive-failure count to 0
  - if mode is `DEFENSIVE`, set `good1 = true` if this is the first consecutive good round, otherwise set `good2 = true`
  - if `good1` and `good2` are both true, set mode = `COOPERATIVE`, then reset `good1 = good2 = false`
- If `support_t` is false:
  - reset `good1 = good2 = false`
  - if mode is `COOPERATIVE`, set mode = `PROBATION`
  - else if mode is `PROBATION`, set mode = `DEFENSIVE`

Decision rule for round `t + 1`:
- If mode is `COOPERATIVE`:
  - play `C`
- If mode is `PROBATION`:
  - play `C` if the previous round was supportive; otherwise play `D`
- If mode is `DEFENSIVE`:
  - play `D`

Behavior by phase:
- First round: `C`
- After a single missed threshold: give one immediate cooperative retry
- After two consecutive misses: defect until the group shows two consecutive recovery rounds
- Once recovered: return to full cooperation

Final round:
- Use the same mode rule for that round; no special endgame deviation.
'''

description_COLLECTIVE_32 = '''
Start by cooperating.

Let `h_t` be the number of opponents observed to cooperate in round `t`, and let `s_t = h_t + c_t` be the total number of cooperators in that round, where `c_t ∈ {0,1}` is your own action.

Use this rule in every round:

- Cooperate if the recent history shows that reaching the threshold is realistically within reach.
- Defect if the recent history shows persistent failure to reach the threshold and your cooperation is no longer helping to form a collective success.

Concrete decision rule:

1. `t = 1`
   - Play `C`.

2. `2 ≤ t ≤ r-2`
   - Maintain a moving window over the last `L = min(3, t-1)` rounds.
   - Let `W` be the set of those rounds.
   - Compute:
     - `avgOpp = average of h_j over j in W`
     - `freqSuccess = fraction of rounds j in W where s_j ≥ m`
   - Play `C` if either:
     - `avgOpp ≥ m-1`, or
     - `freqSuccess ≥ 1/2`
   - Otherwise play `D`.

3. `t = r-1`
   - Play `C` only if the last two rounds satisfy at least one of:
     - `h_{r-2} ≥ m-1` and `h_{r-1} ≥ m-1`
     - `s_{r-2} ≥ m` and `s_{r-1} ≥ m`
   - Otherwise play `D`.

4. `t = r`
   - Play `C` if the previous round reached the threshold with your own cooperation rule compatible with the observed pattern:
     - if `s_{r-1} ≥ m`, play `C`
     - else play `D`

State update after each round:

- If `s_t ≥ m`, set `mode = cooperative`.
- If `s_t < m`, increment `failureStreak`.
- If `failureStreak ≥ 3`, switch to `defensive` mode.

Defensive mode:
- In defensive mode, play `D` until either:
  - two of the last three rounds had `h_j ≥ m-1`, or
  - one of the last two rounds had `s_j ≥ m`.
- Then return to the standard rule above.

Edge cases:

- If `m = 2`, treat `h_j ≥ m-1` as `h_j ≥ 1`.
- If `r = 2`, play `C` in round 1 and in round 2:
  - play `C` if round 1 had `s_1 ≥ m`, otherwise play `D`.
- If `m = n-1`, require especially strong recent support:
  - cooperate only when at least `m-1` opponents cooperated in each of the last two rounds, or when the last round reached the threshold.
- If all recent rounds are below threshold and opponent cooperation is near zero, stay with `D` until a clear increase appears.

Collective mindset:
- Prefer `C` whenever the observed pattern shows others are close to sustaining the threshold.
- Use `D` only after repeated evidence that cooperation is not being matched.
- Re-enter cooperation immediately when the group behavior becomes threshold-supporting again.
'''

description_PROSOCIAL_5 = '''
Cooperate in round 1.

For each round t > 1, let H_t be the number of opponents who cooperated in round t-1, and let S_t be the cooperative signal from the recent history:

- S_t = 1 if H_t ≥ m - 1
- S_t = 0 otherwise

Play C in round t if both conditions hold:
- H_t ≥ m - 1
- At least one of the last two rounds had H ≥ m - 1, with round 1 counted as cooperative by default

Otherwise play D.

Refinement for the final rounds:
- In the last round, play C if H_t ≥ m - 1
- In the last two rounds, never switch to permanent defection because of a single low-cooperation round; require two consecutive rounds with H < m - 1 before defecting

Equivalent compact rule:

1. Round 1: C
2. Round t > 1:
   - If the previous round had at least m - 1 cooperating opponents, and either:
     - the round before that also had at least m - 1 cooperating opponents, or
     - t = 2
     then play C
   - Otherwise play D
3. If two consecutive rounds fail to reach m - 1 cooperating opponents, keep playing D until a round reaches m - 1 again, then return to C immediately

Edge cases:
- If m = 2, cooperate whenever at least one opponent cooperated in the previous round.
- If m = n - 1, cooperate whenever all opponents cooperated in the previous round.
- If the observed number of cooperating opponents is exactly m - 1, treat it as sufficient and continue cooperating.
- If the observed number is below m - 1 for one round only, do not overreact; require a second consecutive shortfall before defecting.

Behavioral principle:
- Begin with full goodwill.
- Match sustained cooperation with continued cooperation.
- Absorb isolated setbacks.
- Defect only after repeated failure to support the threshold, and return to cooperation immediately once the threshold condition reappears.
'''

description_PROSOCIAL_6 = '''
Round 1: play C.

For round t > 1, let x_{t-1} be the number of opponents who cooperated in round t-1, and let x_{t-2} be the number from round t-2 when available.

Decision rule:
- If x_{t-1} >= m - 1: play C.
- Else if x_{t-1} = m - 2: play C.
- Else if x_{t-1} <= m - 3:
  - play C if either:
    - the previous round showed recovery, meaning x_{t-1} > x_{t-2} when t > 2, or
    - t is one of the last two rounds;
  - otherwise play D.

State simplification:
- Stay in “support” mode while the opponents’ cooperation count is at least m - 2.
- Enter “caution” mode after two consecutive rounds with x <= m - 3.
- In caution mode, defect unless the opponents return to x >= m - 2, in which case immediately resume cooperation.

Edge cases:
- If m = 2, always play C.
- In the last round, play C whenever x_{t-1} >= m - 2; otherwise follow caution mode.
- After any round in which x_{t-1} jumps upward, treat that as a recovery signal and cooperate next round.

Priority rule:
- When in doubt, choose C unless there is repeated evidence that the group is far below the cooperation threshold.
'''

description_PROSOCIAL_7 = '''
Cooperate in round 1.

For round t > 1, let h_{t-1} be the number of opponents who cooperated in round t-1, and let s_{t-1} be the total number of cooperators observed in round t-1 including you.

Maintain cooperation if either of the following holds:
- s_{t-1} ≥ m
- h_{t-1} ≥ m - 1 and you cooperated in round t-1

Otherwise defect.

Equivalent rule:
- If the threshold was met in the previous round, stay with cooperation.
- If the threshold was missed, continue cooperating as long as the other players were one short of the threshold and you were among the cooperators.
- If the threshold was clearly missed and there is no near-threshold support, defect until cooperation recovers.

Edge handling:
- Round 1: cooperate unconditionally.
- Final round: cooperate if and only if the rule above says to cooperate; do not switch to defection just because the game is ending.
- After any round in which you defected and the threshold was still met by others, return to cooperation immediately in the next round.
- After any round in which cooperation failed by a narrow margin, give one additional round of support before abandoning cooperation.
- If the observed cooperation count ever reaches m or more, reset to full cooperation mode.

Memory state:
- full_cooperation_mode = true initially
- near_threshold_support = true if, in the previous round, the number of cooperating opponents was exactly m - 1 and you cooperated
- Otherwise near_threshold_support = false

Decision rule in pseudocode:

```
if t == 1:
    play C
else:
    if previous_total_cooperators >= m:
        play C
        full_cooperation_mode = true
    else if previous_opponents_cooperators == m - 1 and previous_action == C:
        play C
        near_threshold_support = true
    else if near_threshold_support == true:
        play C
        near_threshold_support = false
    else:
        play D
```

This strategy starts cooperatively, rewards any round in which the group reaches the cooperative threshold, and gives a limited amount of forgiveness when cooperation falls just short.
'''

description_PROSOCIAL_8 = '''
- Round 1: play C.

- For every round t from 2 to r−1:
  1. Let `o` be the number of opponents who cooperated in round `t−1`.
  2. Let `s` be the total cooperators in round `t−1`, inferred from your own action:
     - if you played C, `s = o + 1`
     - if you played D, `s = o`
  3. Let `o_prev` and `s_prev` be the same values from round `t−2` when available.

- Default posture: cooperate.
- Defect only under sustained collapse:
  - play D if both of the last two observed rounds were clearly below support, meaning
    - `s <= m−2` and `s_prev <= m−2`, and
    - cooperation was not improving, meaning `o <= o_prev`
  - otherwise play C.

- Recovery rule:
  - The first time you see any improvement in opponent cooperation (`o > o_prev`), return to C immediately.
  - If the previous round reached the threshold (`s >= m`), continue with C.

- Last round:
  - play C regardless of history.

- Tie and edge handling:
  - If `m = 2`, treat `s <= m−2` as `s = 0`.
  - If there is only one prior observation, use the available round and default to C unless that round showed complete failure (`s = 0`).

- Compact pseudocode:

```text
if t == 1 or t == r:
    action = C
else:
    s = opponents_coop_last_round + (1 if my_last_action == C else 0)
    if t == 2:
        action = C
    else:
        s_prev = opponents_coop_two_rounds_ago + (1 if my_action_two_rounds_ago == C else 0)
        improving = opponents_coop_last_round > opponents_coop_two_rounds_ago
        if s >= m:
            action = C
        elif s <= m-2 and s_prev <= m-2 and not improving:
            action = D
        else:
            action = C
```

- Behavioral intent:
  - open with cooperation,
  - keep cooperating while the group is near or above the threshold,
  - punish only persistent breakdowns,
  - resume cooperation immediately at the first sign of recovery,
  - always end with cooperation.
'''

description_PROSOCIAL_9 = '''
Let \(q = m-1\), the number of cooperating opponents needed when you cooperate.

Maintain a two-state mode:

- **Cooperative mode**: default mode
- **Defensive mode**: temporary response to repeated shortfalls

Decision rule:

1. **Round 1:** play \(C\).

2. **For round \(t>1\), after observing \(s_{t-1}\), the number of opponents who cooperated in round \(t-1\):**
   - If \(s_{t-1} \ge q\), play \(C\) and stay in cooperative mode.
   - If \(s_{t-1} = q-1\), play \(C\) once more.
   - If \(s_{t-1} \le q-2\), then:
     - if the previous round was also a shortfall, enter defensive mode;
     - otherwise remain in cooperative mode and play \(C\) this round.

3. **Behavior in defensive mode:**
   - Play \(D\) until a round is observed with \(s_t \ge q\).
   - The first round after such a recovery, return to cooperative mode and play \(C\).

4. **Edge cases:**
   - If \(q=1\) (i.e., \(m=2\)), treat any observed opponent cooperation \(s_{t-1}\ge 1\) as sufficient support for cooperation.
   - In the **last round**, use the same rule as above; do not switch to unconditional defection.

Pseudocode:

```text
q = m - 1
mode = COOPERATIVE

Round 1: play C

For round t = 2..r:
    if mode == DEFENSIVE:
        if s_{t-1} >= q:
            mode = COOPERATIVE
            play C
        else:
            play D
    else:  # COOPERATIVE
        if s_{t-1} >= q:
            play C
        else if s_{t-1} == q - 1:
            play C
        else:
            if s_{t-2} < q and t > 2:
                mode = DEFENSIVE
                play D
            else:
                play C
```

This strategy starts by cooperating, rewards sufficient cooperation with continued cooperation, forgives near-misses, and only defects after repeated failure to sustain the threshold.
'''

description_PROSOCIAL_10 = '''
Cooperate in round 1.

Maintain a running estimate of the group’s cooperative reliability from observed history:

- Let `H_t` be the number of opponents who cooperated in round `t`.
- Let `s_t = H_t + 1` if you cooperated in round `t`, and `s_t = H_t` if you defected in round `t` (your estimated total cooperators that round).
- Let `q_t = (sum of s_1...s_t) / (n * t)` be the observed cooperation rate so far.

Decision rule for round `t+1`:

1. Compute the minimum number of other cooperators you need for mutual success:
   - `need = m - 1`

2. Set a target cooperation floor:
   - `target_t = max(need, ceil(n * q_t) - 1)`
   - If `t = 1`, use `target_1 = need`

3. Cooperate in round `t+1` if both conditions hold:
   - `H_t >= target_t`
   - `H_t >= need - 1`

4. Otherwise defect in round `t+1`.

Forgiveness and recovery:

- After any round in which the threshold is met, keep cooperating as long as the number of observed cooperators stays at least `need - 1`.
- If the group falls below that level for two consecutive rounds, switch to defecting until cooperation recovers to at least `need - 1` again.
- If cooperation recovers after a defecting streak, immediately resume cooperation.

Endgame:

- Continue using the same rule through the final round.
- Never defect just because the game is ending; keep the action determined only by the observed cooperation history and the current threshold condition.

Edge cases:

- If `m = 2`, then `need = 1`, so cooperate whenever at least one opponent cooperated in the previous round.
- If `n = m + 1`, require nearly full participation: cooperate only when all but at most one opponent cooperated in the previous round.
- If opponents’ cooperation is consistently high, remain cooperative.
- If opponents are mixed, cooperate on rounds where observed support is sufficient and defect only when support repeatedly drops below the level needed to sustain the collective outcome.

Operational form:

```text
Round 1: play C

For round t > 1:
    observe H_{t-1}
    update q_{t-1}

    need = m - 1
    target = max(need, ceil(n * q_{t-1}) - 1)   # for t > 2
    if t == 2:
        target = need

    if H_{t-1} >= target and H_{t-1} >= need - 1:
        play C
    else if last two rounds both had H < need - 1:
        play D
    else if cooperation recovered to H >= need - 1:
        play C
    else:
        play D
```
'''

description_PROSOCIAL_11 = '''
Initialize `mode = cooperative`.

Round 1:
- Play `C`.

For each round `t = 2, ..., r`:
- Let `x` be the number of opponents who cooperated in round `t-1`.
- If `x >= m-1`:
  - Play `C`
  - Set `mode = cooperative`
- If `x < m-1`:
  - If the previous round also had `x_prev < m-1`:
    - Play `D`
    - Set `mode = defensive`
  - Otherwise:
    - Play `C`
    - Keep `mode = cooperative`

State update after round `t-1`:
- Track whether the last round was a shortfall (`x < m-1`) or not.
- A shortfall is treated as a warning, not a reason to immediately abandon cooperation.

If `mode = defensive`:
- Continue playing `D` only while the observed opponent-cooperation count remains below `m-1`.
- The first round in which `x >= m-1`, immediately return to `C` and reset `mode = cooperative`.

Last round:
- Use the same rule as any other round.

Edge cases:
- If `m = n-1`, cooperate whenever at least `n-2` opponents cooperated in the previous round.
- If `m = 2`, cooperate unless there have been two consecutive rounds with zero opponent cooperators.
- If cooperation by opponents has been stable at or above `m-1`, stay on `C` without interruption.

Behavioral principle:
- Start by cooperating.
- Continue cooperating whenever there is credible evidence that the group can meet the threshold.
- Only switch to `D` after persistent failure, and switch back to `C` immediately when cooperation recovers.
'''

description_PROSOCIAL_12 = '''
Round 1: play C.

For round t > 1, let x_{t-1} be the number of opponents who cooperated in round t-1, and let x_{t-2} be the same for round t-2 when available.

Play C if any of the following hold:
- x_{t-1} ≥ m - 1
- x_{t-1} = m - 2 and x_{t-2} ≥ m - 1
- t = 2 and x_{t-1} = m - 2

Otherwise play D.

If you played D in the previous round, return to C immediately once x_{t-1} ≥ m - 1.

If the final round is reached, use the same rule; never withhold cooperation solely because the game is ending.

This strategy keeps cooperation as the default, forgives a single temporary drop in support, and defects only after clear repeated failure to assemble the needed coalition.
'''

description_PROSOCIAL_13 = '''
Round 1: play C.

For each later round t:

1. Let x_{t-1} be the number of opponents who cooperated in the previous round.
2. Let A be the average of x over the last up to 3 rounds, including round t-1.
3. Play C if either:
   - x_{t-1} >= m - 1, or
   - A >= m - 1 - 1/3
4. Otherwise play D.

Recovery rule:
- If you have played D in one or more rounds because cooperation has fallen below the threshold, return to C immediately once either of the above cooperation conditions is met again.

Edge handling:
- If t = 1, cooperate.
- If t = 2, use only x_{1} for A.
- If r is the last round, use the same rule; do not change behavior because the game is ending.

Behavioral pattern:
- Start by cooperating.
- Continue cooperating as long as observed cooperation is close to the level needed to sustain the group.
- Defect only after sustained shortfall in opponents’ cooperation.
- Re-enter cooperation as soon as the group shows renewed support.
'''

description_PROSOCIAL_14 = '''
Round 1: play C.

For each later round t:

1. Let x be the number of opponents who cooperated in round t−1.
2. Let y be the number of opponents who cooperated in round t−2, if t≥3.

Decision rule:
- Play C if x ≥ m−1.
- Also play C if x = m−2 and y ≥ m−1.
- Otherwise, if you have seen two consecutive rounds with x < m−1, play D for exactly one round, then return to C in the next round.
- After any round in which x ≥ m−1, reset back to cooperative mode and play C.

Forced cooperation:
- Play C in the last round.
- Play C in any round immediately after a threshold success by the group, regardless of whether you were personally pivotal.

State form:
- Cooperative mode: default state, always C unless two consecutive near-failures occur.
- Repair mode: after two consecutive failures to get close to threshold, use one D as a brief probe, then switch back to C immediately.

Compact pseudocode:

```
if t == 1 or t == r:
    play C
else:
    x = cooperators among opponents in t-1
    if x >= m-1:
        play C
        fail_streak = 0
    else if t >= 3 and cooperators among opponents in t-2 >= m-1:
        play C
    else:
        fail_streak += 1
        if fail_streak >= 2:
            play D
            fail_streak = 0
        else:
            play C
```

Maintain the same choice of C whenever the group is close to meeting the threshold, and only use a single D after repeated collapse to test whether cooperation has disappeared.
'''

description_PROSOCIAL_15 = '''
Cooperate in round 1.

For round t > 1, let h_t be the number of other players who cooperated in round t - 1, and let q = m - 1 be the minimum number of cooperating others needed for your own cooperation to help meet the threshold.

Decision rule:

- Cooperate if either of the following holds:
  1. h_t ≥ q
  2. h_t = q - 1 and the recent trend is nondecreasing:
     - h_t ≥ h_{t-1}, or
     - t = 2

- Defect otherwise.

Equivalent implementation:

1. Start with C in round 1.
2. After each round, record the observed number of cooperating opponents.
3. In the next round:
   - If the previous round already had enough cooperation among others to make threshold attainment likely, keep cooperating.
   - If cooperation was just one short of the needed support, cooperate only if the cooperation level is holding steady or improving.
   - If cooperation falls clearly below that level, defect until it recovers.

Edge handling:

- Round 1: play C.
- Round 2: play C if round 1 had at least q cooperating others; otherwise play D only if round 1 had at most q - 2 cooperating others.
- Final round: use the same rule as any other round; do not switch to unconditional defection.
- If all observed opponents defected in the previous round, play D next round, but return to C immediately once observed cooperation reaches q - 1 or higher.
- If observed cooperation reaches or exceeds q, keep playing C for as long as that remains true.

Long-run behavior:

- Default to cooperation.
- Defect only after a clear drop in support.
- Re-enter cooperation as soon as the group returns close to the threshold.
- Never punish isolated defections by collapsing into permanent defection.
'''

description_PROSOCIAL_16 = '''
Cooperate in round 1.

Maintain a running state with:
- `s`: your current cooperation stance, initially `C`
- `h`: the number of opponents who cooperated in the previous round
- `L`: consecutive rounds in which the threshold was met
- `F`: consecutive rounds in which the threshold was missed

Decision rule for round `t > 1`:

1. Observe `h_prev`, the number of opponents who cooperated in round `t-1`.
2. Compute total cooperators in that round:
   - `T_prev = h_prev + 1` if you cooperated in round `t-1`
   - `T_prev = h_prev` if you defected in round `t-1`

3. Update:
   - If `T_prev >= m`: increment `L`, reset `F = 0`
   - If `T_prev < m`: increment `F`, reset `L = 0`

4. Choose action for round `t`:
   - If `T_prev >= m`:
     - Play `C`
   - Else if `T_prev < m`:
     - If `L >= 2`, play `C`
     - Otherwise, play `D`

Equivalent rule:
- Stay cooperative whenever the group is meeting the threshold.
- After a failure, give the group one immediate chance to recover by continuing to cooperate once.
- If the threshold fails twice in a row, switch to `D`.
- Return to `C` immediately after any round in which the threshold is met.

Last round rule:
- Ignore future consequences; apply the same rule as above.
- If the group met the threshold in the previous round, play `C`.
- If the group missed the threshold in the previous round, play `C` once more unless there have already been two consecutive misses, in which case play `D`.

Fallback rule for a persistently cooperative environment:
- If the observed cooperation level has met the threshold in every round so far, always continue with `C`.

Fallback rule for a persistently uncooperative environment:
- If the threshold has failed in two consecutive rounds and no recovery has occurred, play `D` until a round meets the threshold again.

Tie-breaking / edge cases:
- If exactly `m` cooperated in the previous round, treat it as success.
- If your own previous action is unknown for any reason, assume you cooperated when evaluating `T_prev` to preserve cooperation-first behavior.
- If no historical data are available beyond round 1, default to `C`.
'''

description_PROSOCIAL_17 = '''
Play C in every round.

Pseudocode:
```text
for t in 1..r:
    choose C
```

If you want the rule expressed with history dependence:
- Round 1: cooperate.
- After every round: ignore the observed count when choosing your next action; cooperate again.
- Last round: cooperate as well.
- Defect never.
'''

description_PROSOCIAL_18 = '''
Round 1: play C.

For round t ≥ 2, let h_{t-1} be the number of opponents who cooperated in the previous round, and let met_{t-1} be true if the threshold was reached in the previous round.

Play C if any of the following holds:
- met_{t-1} is true
- h_{t-1} ≥ m - 2
- t ≥ 3 and h_{t-1} > h_{t-2}

Otherwise, play D.

Additional edge handling:
- If the previous round had a threshold failure but cooperation was close, stay with C.
- If cooperation among opponents is recovering, stay with C.
- If cooperation has been low and non-improving for two consecutive rounds, switch to D until either h_{t-1} ≥ m - 2 or the threshold is met again.
- In the final round, use the same rule; do not change behavior just because the game is ending.
'''

description_PROSOCIAL_19 = '''
Open with cooperation and keep supporting any coalition that is close to forming.

Let `o_t` be the number of opponents who cooperated in round `t`, and let `a_t ∈ {C,D}` be your own action in round `t`.

**Round 1**
- Play `C`.

**From round 2 onward**
Play `C` if any of the following holds:

1. **Threshold was reached last round**
   - `o_{t-1} + 1[a_{t-1} = C] >= m`

2. **You can help a near-miss**
   - `o_{t-1} = m - 1` and you played `D` last round, or
   - `o_{t-1} >= m - 1` and you played `C` last round

3. **The cooperative bloc is still building**
   - `o_{t-1} >= m - 2` and `o_{t-1} > o_{t-2}`

Otherwise play `D`.

**Last round**
- Play `C` whenever the previous round was at least one short of the threshold but within reach by your own cooperation:
  - if `o_{r-1} >= m - 1`, play `C`
- Otherwise follow the rule above.

**Persistent failure rule**
- If the previous two rounds both failed to reach threshold and `o_{t-1} < m - 2` with no increase from `o_{t-2}`, play `D` until the opponents’ cooperation count returns to at least `m - 2`; then resume `C`.

**Compact pseudocode**
```text
if t == 1:
    play C
else if t == r:
    if o[t-1] >= m-1:
        play C
    else:
        apply main rule
else if o[t-1] + is_C(a[t-1]) >= m:
    play C
else if o[t-1] >= m-1 and a[t-1] == D:
    play C
else if o[t-1] >= m-2 and o[t-1] > o[t-2]:
    play C
else if o[t-1] < m-2 and o[t-2] < m-2 and o[t-1] <= o[t-2]:
    play D
else:
    play D
```

**Interpretation**
- Default to cooperation.
- Keep cooperating when the group is near the threshold, even after a miss.
- Stop subsidizing only after repeated, stagnant failure far from the threshold.
- Resume cooperation immediately when the group shows renewed movement toward the threshold.
'''

description_PROSOCIAL_20 = '''
Let \(o_t\) be the number of opponents you observe cooperating in round \(t\), and let

\[
s_t = o_t + \mathbf{1}[a_t = C]
\]

be the total number of cooperators in that round, where \(a_t\) is your own action.

Maintain a state variable \(f\) = number of consecutive recent rounds with \(s_t < m\).

Decision rule:

- Round 1: play \(C\).
- For round \(t \ge 2\):
  1. If \(f = 0\), play \(C\).
  2. If \(f = 1\), play \(C\).
  3. If \(f \ge 2\):
     - play \(C\) if \(o_{t-1} \ge m-1\),
     - otherwise play \(D\).

Update after each round:
- If \(s_t \ge m\), set \(f = 0\).
- If \(s_t < m\), set \(f = f + 1\).

Equivalent pseudocode:

```text
initialize f = 0
for t = 1..r:
    if t == 1:
        play C
    else if f <= 1:
        play C
    else:
        if observed opponents cooperating last round >= m - 1:
            play C
        else:
            play D

    observe o_t
    if o_t + 1[a_t = C] >= m:
        f = 0
    else:
        f = f + 1
```

Edge cases:
- If the previous round met the threshold, keep cooperating.
- If the previous round missed the threshold once, still cooperate once more.
- If there are two or more consecutive misses, defect only until the observed opponent cooperation level rises to at least \(m-1\), then return immediately to cooperation.
- In the final round, use the same rule as above.
'''

description_PROSOCIAL_21 = '''
Initialize:
- Cooperate in round 1.

For each round `t > 1`, let `x[t-1]` be the number of opponents who cooperated in the previous round.

Decision rule:
- Play `C` if either of the following holds:
  - `x[t-1] >= m - 1`
  - `t >= 3` and `x[t-1] >= m - 2` and `x[t-2] >= m - 2`
- Otherwise play `D`.

Final-round rule:
- In the last round, play `C` whenever `x[t-1] >= m - 1`.
- If `x[t-1] < m - 1`, play `D`.

Interpretation of the history rule:
- `x[t-1] >= m - 1` means the group was one supporter away from success with your own cooperation, so continue cooperating.
- Two consecutive rounds with `x >= m - 2` means cooperation is near the threshold and stable enough to keep supporting, even if the threshold was narrowly missed.
- A round below that level triggers a one-round reset to `D`, then the strategy returns to `C` as soon as opponent cooperation recovers.

Compact pseudocode:
```text
if t == 1:
    action = C
else if x[t-1] >= m-1:
    action = C
else if t >= 3 and x[t-1] >= m-2 and x[t-2] >= m-2:
    action = C
else:
    action = D
```
'''

description_PROSOCIAL_22 = '''
Round 1: cooperate.

For round t > 1, let x be the number of opponents who cooperated in round t−1.

Decision rule:
- Cooperate if x ≥ m−1.
- Cooperate once more if x = m−2 and the previous round had x_prev ≥ m−1.
- Defect only if x ≤ m−2 for two rounds in a row.

Equivalent state machine:
- Start in cooperative mode.
- Stay in cooperative mode after any round with x ≥ m−1.
- If one round falls below x = m−1, give one forgiveness round and still cooperate.
- If two consecutive rounds fall below x = m−1, switch to cautious mode and defect until a round occurs with x ≥ m−1, then return to cooperative mode.

Last round:
- If currently in cooperative mode, cooperate.
- If currently in cautious mode, defect.

Additional edge handling:
- If m = 2, interpret the threshold condition as x ≥ 1.
- If there has never been a successful round before the final round, keep cooperating for the first two rounds, then defect from round 3 onward unless a later round reaches x ≥ m−1.
- After any round where x = n−1, remain fully cooperative on the next round.
'''

description_PROSOCIAL_23 = '''
Round 1: cooperate.

For round t > 1, let o_{t-1} be the number of opponents who cooperated in the previous round, and let o_{t-2} be the number from two rounds ago when available.

Use this state machine:

**Supportive mode**  
Stay in supportive mode if the group has been near the threshold recently.
- Cooperate if o_{t-1} >= m - 2.
- Also cooperate if, in the last two observed rounds, at least one had o >= m - 2 and the other had o >= m - 3.

**Recovery mode**  
Enter recovery mode after two consecutive clearly weak rounds.
- If o_{t-1} <= m - 3 and o_{t-2} <= m - 3, defect this round.
- Remain in recovery mode while the most recent observed round satisfies o_{t-1} <= m - 3.
- Exit recovery mode immediately once o_{t-1} >= m - 2, then cooperate.

Equivalent compact rule:

```text
t = 1: C
t > 1:
    if o_{t-1} >= m-2:
        C
    else if t > 2 and o_{t-1} <= m-3 and o_{t-2} <= m-3:
        D
    else:
        C
```

Special handling:
- If m = 2, cooperate whenever at least one opponent cooperated in the previous round; defect only after two consecutive rounds with zero opponent cooperation.
- In the final round, use the same rule as above; do not change behavior just because the game is ending.
- If history is shorter than two rounds, base the decision only on the available observations and default to cooperation unless the most recent observed round was clearly weak.
'''

description_PROSOCIAL_24 = '''
Round 1: play C.

For round t > 1, let x_{t-1} be the number of opponents who cooperated in the previous round, and let x_{t-2} be the same for the round before that, if available.

Decision rule:
- Play C if any of the following holds:
  - x_{t-1} >= m - 1
  - x_{t-2} >= m - 1
  - t = r
- Otherwise play D.

Equivalent form:
- Cooperate by default.
- Defect only after two consecutive rounds in which fewer than m - 1 opponents cooperated.

Edge handling:
- If t = 1, cooperate.
- If t = 2, cooperate.
- If the last observed round was close to the threshold, cooperate.
- If there is a single dip below the threshold after cooperation has been high, forgive it and keep cooperating.
- If the group has already failed twice in a row to reach the attainable threshold, defect for one round, then immediately resume the same rule.

State version:
- Maintain `collapse_streak =` number of consecutive previous rounds with `x < m - 1`.
- If `collapse_streak < 2`, play C.
- If `collapse_streak >= 2`, play D.
- Update `collapse_streak` after each round from the observed `x`.

This keeps cooperation as the default, tolerates brief instability, and only withholds cooperation after a sustained breakdown.
'''

description_PROSOCIAL_25 = '''
Play C in round 1.

From round 2 onward, keep a running record of the number of cooperators observed in the previous round, call it x.

Decision rule:
- If x ≥ m, play C.
- If x = m − 1, play C with high probability and D only if you have already spent several rounds in a row carrying the risk while the group repeatedly missed the threshold.
- If x ≤ m − 2, play D for that round.

Use this update rule for the high-probability case:
- Maintain a patience counter p, initialized at 0.
- After any round with x ≥ m, reset p = 0.
- After any round with x = m − 1, increment p by 1.
- After any round with x ≤ m − 2, reset p = 0.

Then:
- If x = m − 1 and p < 2, play C.
- If x = m − 1 and p ≥ 2, play D until the group reaches x ≥ m again.

Last round:
- Play C if the previous round had x ≥ m or x = m − 1.
- Play D only if the previous several rounds showed persistent failure, meaning x ≤ m − 2 repeatedly and no recent sign of collective recovery.

Recovery rule:
- The moment the observed cooperation count reaches m or more after any defecting phase, return immediately to unconditional C for the next round.

Tie-breaking when the history is ambiguous:
- Default to C whenever the group is one cooperator short of success.
- Default to D only when the shortfall is large or repeated.

Overall pattern:
- Start by cooperating.
- Reward successful coordination by continuing to cooperate.
- Give a grace period when the group narrowly misses the threshold.
- Withdraw cooperation only after repeated shortfalls, and restore it as soon as the group shows recovery.
'''

description_PROSOCIAL_26 = '''
Initialize in cooperative mode.

Let x_t be the number of opponents who cooperated in round t.

Decision rule for round t:

- Round 1: play C.
- Round t > 1:
  - If x_{t-1} >= m - 1: play C.
  - If x_{t-1} = m - 2: play C.
  - If x_{t-1} <= m - 3:
    - If x_{t-2} <= m - 3 as well, play D.
    - Otherwise, play C once more.

Equivalent state version:

- Start in supportive mode.
- In supportive mode, play C.
- Enter guarded mode only after two consecutive rounds in which the observed number of cooperating opponents was at least two below the threshold, i.e. x_{t-1} <= m - 3 and x_{t-2} <= m - 3.
- In guarded mode, play D.
- Leave guarded mode immediately after any round with x_t >= m - 1.

Edge handling:

- First round: always cooperate.
- Final round: use the same rule as any other round; do not change behavior just because it is the last round.
- If the game has only two rounds, cooperate in round 1 and apply the round-2 rule directly from round-1 observation.
'''

description_PROSOCIAL_27 = '''
Initialize:

- Round 1: cooperate.

For each round t > 1:

1. Let `prev_total` be the number of cooperators in round `t-1`, including yourself if you cooperated then.
2. Let `prev_gap = m - prev_total`.

Decision rule:

- If `prev_total >= m`: cooperate.
- If `prev_total = m - 1`: cooperate.
- If `prev_total <= m - 2`:
  - Cooperate if the last two rounds were not both below threshold.
  - Defect only if both of the last two rounds were below threshold, and you cooperated in both of them.

Reset rule:

- The moment any round reaches `m` or more cooperators, immediately return to unconditional cooperation in the next round.

Boundary rules:

- If there is no prior history, cooperate.
- If only one prior round exists, treat it as insufficient evidence of persistent failure and cooperate.
- In the final round, use the same rule; never switch to endgame defection.

Compact pseudocode:

```text
if t == 1:
    play C
else:
    prev_total = observed_opponents_C_last_round + (1 if I played C last_round else 0)

    if prev_total >= m:
        play C
    else if prev_total == m - 1:
        play C
    else:
        if last_two_rounds_both_below_m and I played C in both of them:
            play D
        else:
            play C
```

State update:

- Track `last_two_rounds_both_below_m`.
- Set it to true only when two consecutive rounds ended with fewer than `m` total cooperators.
- Clear it immediately when a round reaches `m` or more cooperators.

Prosocial orientation:

- Cooperate by default.
- Keep cooperating when the group is close to success.
- Withdraw cooperation only after repeated, clear failure despite your own cooperation.
- Return to cooperation immediately after any sign that the group can meet the threshold again.
'''

description_PROSOCIAL_28 = '''
Initialize `fail_streak = 0`.

For round 1, play `C`.

For each round `t > 1`, let `x` be the number of other players who cooperated in round `t-1`.

Decision rule:
- If `x >= m - 1`, play `C` and set `fail_streak = 0`.
- If `x < m - 1`, then:
  - increment `fail_streak += 1`
  - play `C` while `fail_streak <= 2`
  - play `D` once `fail_streak > 2`

Reset rule:
- Any time a round is observed with `x >= m - 1`, immediately return to `C` on the next round and reset `fail_streak = 0`.

Edge handling:
- If `m = 2`, the rule becomes: cooperate whenever at least one other player cooperated last round; otherwise cooperate for two more rounds after a failure before defecting.
- In the last round, use the same rule as above; do not change the decision rule based on the absence of future rounds.
- If the game has just recovered after a long failure period, cooperate again immediately on the first sign of renewed support.

Behavioral form:
- Start by contributing.
- Stay cooperative as long as the group is meeting, or nearly meeting, the threshold.
- Tolerate brief slumps and keep supporting recovery.
- Defect only after sustained evidence that the group is not close enough to succeed.
- Resume cooperation immediately when support reappears.
'''

description_PROSOCIAL_29 = '''
Round 1: play C.

For each later round t:

1. Let x be the total number of cooperators in round t−1, including yourself.
2. If x ≥ m−1, play C.
3. If x < m−1:
   - keep a failure counter f, the number of consecutive rounds with x < m−1.
   - play C while f ≤ 1
   - play D once f ≥ 2, until a round occurs with x ≥ m−1, then reset f to 0 and return to C.

Edge handling:
- If a round succeeds, immediately reset the failure counter.
- If the last observed round had x = m−1, always cooperate in the next round, since one extra cooperative action can restore full success.
- In the final round, use the same rule; do not change behavior just because the game is ending.

State update:
- After each round, set f = 0 if x ≥ m−1.
- Otherwise set f = f + 1.

This makes the default response cooperative, forgives isolated setbacks, and only withdraws support after repeated undercooperation.
'''

description_PROSOCIAL_30 = '''
Maintain a cooperation target count and play C only when your action is needed to keep the group at or above the threshold, or when a temporary shortfall should be answered with limited forgiveness.

Let:
- `H_t` = number of opponents who cooperated in round `t`
- `S_t = H_t + 1` if you cooperated in round `t`, else `H_t`
- `need_t = max(0, m - S_t)` = how many total cooperators were still missing in round `t`

Decision rule for round `t`:

1. **Round 1**
   - Play `C` if `m ≤ n - 1` and a cooperative start is feasible without making the threshold impossible.
   - Otherwise play `D`.

2. **If the previous round reached the threshold**
   - If `S_{t-1} ≥ m`, play `C` when `H_{t-1} ≥ m - 1`; otherwise play `D`.
   - Interpretation: keep cooperating as long as the group is still within one player of the threshold, so your cooperation can help preserve the shared reward.

3. **If the previous round missed the threshold**
   - Compute the deficit `d = m - S_{t-1}`.
   - If `d = 1`, play `C` in the next round.
   - If `d = 2`, play `C` only if `H_{t-1} ≥ m - 2`.
   - If `d ≥ 3`, play `D` for one round, then reassess from the new history.
   - Interpretation: forgive one-round shortfalls immediately, but do not keep paying when the gap is large and persistent.

4. **Streak rule**
   - If the threshold has been missed in the last two consecutive rounds, play `D` unless the current observed cooperation among opponents is at least `m - 1`.
   - If the threshold has been met in the last two consecutive rounds, play `C` unless the current observed cooperation among opponents has fallen below `m - 2`.
   - Interpretation: reward reliability, but avoid being exploited by repeated free-riding.

5. **Last round**
   - If `t = r`, play `C` if `H_{r-1} ≥ m - 1`.
   - Otherwise play `D`.
   - If the last two rounds both met the threshold, play `C` regardless.
   - If the last two rounds both missed the threshold, play `D`.

6. **Long-run cooperative bias**
   - Whenever the observed number of opponent cooperators is exactly `m - 1`, play `C`.
   - Whenever it is at least `m`, play `C`.
   - Whenever it is at most `m - 3`, play `D`.
   - Only in the intermediate case `H_t = m - 2`, use the recent-history rules above.
   - Interpretation: default to helping whenever your cooperation can plausibly preserve or restore the collective reward.

Compact pseudocode:

```text
if t == 1:
    if m <= n - 1:
        action = C
    else:
        action = D

else:
    if H_{t-1} >= m - 1:
        action = C
    else:
        deficit = m - S_{t-1}
        if deficit == 1:
            action = C
        elif deficit == 2:
            action = C if H_{t-1} >= m - 2 else D
        else:
            action = D

    if last_two_rounds_both_missed and H_t < m - 1:
        action = D
    if last_two_rounds_both_met and H_t >= m - 2:
        action = C

if t == r:
    action = C if H_{r-1} >= m - 1 else D
```

Behavioral pattern:
- Begin with trust.
- Continue cooperating whenever the group is close enough that your contribution can matter.
- Forgive isolated failures.
- Withdraw briefly after repeated shortfalls.
- Reinvest cooperation as soon as opponents show renewed support.
'''

description_PROSOCIAL_31 = '''
Round 1: cooperate.

For every later round t:

1. Let h be the number of opponents who cooperated in round t-1.
2. Let s be the total number of cooperators in round t-1, i.e.:
   - s = h + 1 if you cooperated in round t-1
   - s = h if you defected in round t-1
3. Define the support gap g = m - s.

Decision rule:
- If g <= 0: cooperate.
- If g = 1: cooperate.
- If g >= 2:
  - cooperate unless this is the second consecutive round with g >= 2;
  - if it is the second consecutive such round, defect for one round;
  - after any defection, return to cooperation immediately if the next observed round reaches g <= 1.

History update:
- Track the current streak of consecutive rounds with g >= 2.
- Reset that streak to 0 whenever g <= 1.

Endgame rule:
- In the last round, cooperate.

Deterministic pseudocode:

```text
state: bad_streak = 0

round 1:
    play C

for round t = 2 to r:
    observe h = number of opponents who played C in round t-1
    if my action in round t-1 was C:
        s = h + 1
    else:
        s = h

    g = m - s

    if g <= 1:
        bad_streak = 0
        play C
    else:
        bad_streak += 1
        if t == r:
            play C
        else if bad_streak >= 2:
            play D
        else:
            play C
```

This keeps cooperation as the default, only uses defection after repeated failure to reach the threshold, and immediately returns to cooperation as soon as the group is back within reach.
'''

description_PROSOCIAL_32 = '''
Cooperate in round 1.

For each later round, let \(x_{t-1}\) be the number of opponents who cooperated in the previous round.

Decision rule:
- If \(x_{t-1} \ge m-1\), play \(C\).
- If \(x_{t-1} = m-2\), also play \(C\) for one more round as a forgiveness step.
- If \(x_{t-1} < m-2\), play \(D\) only if this is the second consecutive round below \(m-1\); otherwise play \(C\).

State version:
- Track whether the last round met the cooperation threshold among opponents.
- Cooperate by default.
- Defect only after two consecutive rounds in which the observed opponent cooperation was too low to make the threshold plausible.

Pseudocode:

```text
Round 1: play C

For round t = 2..r:
    observe x = number of opponents who cooperated in round t-1

    if x >= m-1:
        play C
        fail_streak = 0
    else if x == m-2:
        play C
        fail_streak = 1
    else:
        fail_streak += 1
        if fail_streak >= 2:
            play D
        else:
            play C
```

Edge handling:
- First round: always cooperate.
- Last round: use the same rule; do not change behavior just because the game is ending.
- If cooperation recovers to \(x \ge m-1\) in any round, immediately reset to cooperation.
- If the group repeatedly falls short, respond with brief, limited defection, then return to cooperation as soon as the observed cooperation level recovers.
'''

description_ALTRUISTIC_5 = '''
Cooperate in round 1.

For each subsequent round, compute:

- `H` = number of cooperations observed among the other `n-1` players in the previous round
- `S` = number of cooperations observed among the other players in the last `L` rounds, where `L = min(3, t-1)` and `t` is the current round
- `avg = S / L`

Decision rule:

1. **Strong support present**  
   Cooperate if `H >= m-1`.

2. **Near-threshold but improving**  
   Cooperate if `H = m-2` and `avg >= m-1`.

3. **Forgiving recovery**  
   Cooperate if the previous round failed to reach the threshold by exactly one cooperator, and the round before that met the threshold:
   - `H = m-2`
   - and the round before last had at least `m-1` cooperators among the other players.

4. **Otherwise**  
   Defect.

Additional edge rules:

- If `m = 2`, the rule simplifies to: cooperate whenever at least one other player cooperated in the previous round; otherwise defect.
- In the final round, use the same rule as above; do not switch behavior just because the game is ending.
- If the last three rounds contain both cooperation and defection but the average support is still at least `m-1`, keep cooperating.
- If the other players have cooperated in every one of the last two rounds, cooperate regardless of whether the most recent round was just below threshold.

State memory needed:

- Previous round cooperation count among others
- The round-before-previous cooperation count among others
- A rolling sum over the last up to three rounds

Behavioral pattern:

- Start by cooperating.
- Continue cooperating whenever the group is meeting the target or very close to it.
- Defect only after clear repeated under-support.
- Return to cooperation immediately after evidence of renewed collective effort.
'''

description_ALTRUISTIC_6 = '''
Start by cooperating, and keep cooperating whenever your cooperation can plausibly help the group reach the threshold.

Let \(a_t\) be the number of other players who cooperated in round \(t\), and let \(s_t\) be your own action in round \(t\), with \(s_t \in \{C,D\}\).

Decision rule for round \(t\):

1. First round:
- Play \(C\).

2. General round \(t>1\):
- Let \(x_{t-1}\) be the total number of cooperators in the previous round, so \(x_{t-1} = a_{t-1} + \mathbf{1}[s_{t-1}=C]\).
- Cooperate if any of the following holds:
  - \(x_{t-1} \ge m\)
  - \(x_{t-1} = m-1\)
  - \(a_{t-1} \ge m-1\)
  - \(t\) is among the last two rounds
- Otherwise, defect.

Equivalent compact rule:

```text
If t = 1: play C
Else if a_{t-1} + 1 >= m: play C
Else if t >= r - 1: play C
Else:
    play D
```

Interpretation of the rule:
- If the group already met the threshold last round, keep contributing to sustain it.
- If the group was exactly one cooperator short, contribute again because your cooperation can be pivotal.
- If you observed at least \(m-1\) other cooperators, cooperate as a direct altruistic attempt to push the group over the line.
- In the final two rounds, cooperate unconditionally to maximize the chance of a collective success at the end of the game.

Edge cases:
- If everyone else defected last round, continue with \(D\) until you observe at least \(m-1\) other cooperators.
- If cooperation is already abundant, stay with \(C\) to reinforce the cooperative state.
- If the previous round just missed the threshold by one, do not abandon cooperation; keep pressing for success.
- In the last round, always play \(C\).
- In the penultimate round, also play \(C\), so that even late-emerging cooperation can still be supported through the finish.

History dependence:
- Use only the previous round’s observed number of cooperating opponents and your own previous action.
- If you have a run of rounds with \(a_t \ge m-1\), maintain \(C\) throughout that run.
- If cooperation collapses below \(m-1\) for several rounds and it is not near the end, switch to \(D\) until there is again a realistic path to meeting the threshold.

Altruistic posture:
- Default to cooperation.
- Treat near-threshold situations as a signal to help, not withdraw.
- Preserve cooperative momentum whenever it appears.
- Reserve defection only for prolonged low-cooperation states far from the end of the game, where a single altruistic action is unlikely to alter the group outcome.
'''

description_ALTRUISTIC_7 = '''
Cooperate in round 1.

Let `H_t` be the number of opponents who cooperated in round `t`, and let `S_t` be the cumulative number of opponent cooperations up to round `t`.

Maintain a trust state `B_t`:

- Initialize `B_1 = 0`
- After each round `t`, update:
  - `B_{t+1} = min(3, max(-3, B_t + sign(H_t - (m-1))))`
  - where:
    - `+1` if `H_t >= m-1`
    - `0` if `H_t = m-2`
    - `-1` if `H_t <= m-3`

Decision rule for round `t`:

1. **Always cooperate in the last round.**
2. **Cooperate if the group is near the threshold and has been making good-faith efforts:**
   - Cooperate if `H_{t-1} >= m-1`
   - Cooperate if `B_t >= 0`
3. **Defect only as a temporary signal when cooperation is repeatedly failing:**
   - Defect if `B_t < 0` and `H_{t-1} <= m-3`
   - Return to cooperation immediately once `H_{t-1} >= m-2`

Edge handling:

- **Round 1:** cooperate.
- **Any round after observing at least `m-1` opponent cooperations in the previous round:** cooperate.
- **If the previous round missed the threshold by exactly 1 opponent (`H_{t-1} = m-2`):** cooperate; treat this as near-success.
- **If the previous round was far below threshold (`H_{t-1} <= m-3`):** defect for at most one round, then re-test with cooperation on the next round.
- **If `m = n-1`:** cooperate in every round except a single defensive defection after two consecutive far-below-threshold rounds.
- **If `m` is small:** still cooperate by default; only use a brief defensive defection when repeated failure shows broad defection by others.

Compact pseudocode:

```text
if t == r:
    play C
else if t == 1:
    play C
else if H[t-1] >= m-1:
    play C
else if H[t-1] == m-2:
    play C
else if B_t < 0 and H[t-1] <= m-3:
    play D
else:
    play C
```

This strategy is explicitly pro-cooperation: it starts by helping, keeps cooperating whenever there is credible collective effort, forgives close misses, and uses only short, limited restraint when the group is repeatedly far from the threshold.
'''

description_ALTRUISTIC_8 = '''
Let \(x_t\) be the number of opponents observed to cooperate in round \(t\), so the total number of cooperators that round is \(x_t + \mathbf{1}\{a_t = C\}\).

Use a threshold-support strategy:

1. Round 1:
   - Play \(C\).

2. For round \(t \ge 2\), compute the recent support rate over the last \(L\) rounds, where
   \[
   L = \min(3,\, t-1).
   \]
   Let
   \[
   S_t = \frac{1}{L}\sum_{j=t-L}^{t-1} x_j.
   \]

   Then:
   - Play \(C\) if either of the following holds:
     - \(S_t \ge m-2\), or
     - in the immediately previous round, the observed cooperators were close to the threshold: \(x_{t-1} \ge m-2\).
   - Otherwise play \(D\).

3. Final-round rule:
   - In round \(r\), play \(C\) if \(x_{r-1} \ge m-2\).
   - If not, play \(D\).

4. Recovery rule after defection by others:
   - If the strategy ever plays \(D\) because support has fallen too far below threshold, it returns to \(C\) immediately after observing any round with \(x_t \ge m-2\).

5. Never exploit:
   - If the threshold is met by others alone, still play \(C\).
   - Do not switch to \(D\) merely because cooperation is already safe; continue cooperating whenever the group is near or above the minimum needed.

6. Edge cases:
   - If \(m=2\), then cooperate in round \(t\) whenever at least one opponent cooperated in the previous round.
   - If \(m=n-1\), cooperate only when nearly everyone is cooperating: play \(C\) whenever \(x_t \ge n-3\) in the recent window.
   - If there has been no prior round data yet, cooperate.
   - If a single low-cooperation round is followed by a strong recovery round, immediately resume cooperation; do not require multiple consecutive recovery rounds.

Decision summary:
- Default action is \(C\).
- Switch to \(D\) only after repeated evidence that opponents are sustaining cooperation below the level needed to make altruistic participation effective.
- Switch back to \(C\) as soon as opponents show renewed collective support.
'''

description_ALTRUISTIC_9 = '''
Initialize with cooperation.

For each round t = 1..r, let h_{t-1} be the number of opponents who cooperated in the previous round, and let f be the current streak of consecutive rounds in which h < m-1.

Decision rule:

- Round 1: play C.
- For round t > 1:
  - If h_{t-1} >= m-1: play C.
  - Else if f = 1: play C.
  - Else if t mod 3 = 0: play C.
  - Else: play D.

Update the failure streak after each round:
- If h_{t} >= m-1, set f = 0.
- Otherwise set f = f + 1.

Edge handling:
- If the last observed round was successful, continue cooperating immediately.
- If the group has missed the threshold for two or more consecutive rounds, cooperate once every third round to keep offering rescue opportunities.
- On the final round, use the same rule; never switch to defection solely because the game is ending.

Behavioral principle:
- Default to helping.
- Stay cooperative whenever the group is close enough that your cooperation can contribute to success.
- After repeated under-participation, keep giving periodic chances rather than abandoning cooperation entirely.
'''

description_ALTRUISTIC_10 = '''
Cooperate in the first round.

For every later round \(t\):

1. Let \(x_{t-1}\) be the number of opponents who cooperated in round \(t-1\).
2. Let \(s_{t-1}\) be the total number of cooperators in round \(t-1\) implied by your own action:
   - if you cooperated in \(t-1\), then \(s_{t-1} = x_{t-1} + 1\)
   - if you defected in \(t-1\), then \(s_{t-1} = x_{t-1}\)

Decision rule:
- If \(t = r\): cooperate.
- Else if \(s_{t-1} \ge m\): cooperate.
- Else if \(s_{t-1} = m-1\): cooperate, to keep the group at the brink of success and give others a chance to restore the threshold.
- Else if the last two rounds both had \(s < m\): defect for one round, then return immediately to cooperation.
- Otherwise: cooperate.

State tracking:
- Maintain a flag `failure_streak` counting consecutive rounds with \(s < m\).
- Update after each round:
  - if \(s_{t} < m\), increment `failure_streak`
  - else reset `failure_streak = 0`

Compact pseudocode:

```text
if t == 1:
    play C
else if t == r:
    play C
else:
    if s_prev >= m:
        play C
        failure_streak = 0
    else if s_prev == m - 1:
        play C
        failure_streak = 0
    else if failure_streak >= 2:
        play D
        failure_streak = 0
    else:
        play C
        failure_streak += 1
```

Behavioral principle:
- Default to cooperation.
- Preserve cooperation whenever the group is close to the threshold.
- Use a brief, rare defection only after repeated clear failure, then immediately return to cooperation.
- Never defect in the final round.
'''

description_ALTRUISTIC_11 = '''
Let \(x_t\) be the number of opponents who cooperated in round \(t\).

- Round 1: play \(C\).
- Round \(r\): play \(C\).

For every round \(t\) with \(2 \le t \le r-1\):

1. If \(x_{t-1} \ge m-1\), play \(C\).
2. If \(x_{t-1} < m-1\) and \(x_{t-2} < m-1\), play \(D\) once.
3. Otherwise, play \(C\).

State update:
- After any round with \(x_t \ge m-1\), reset the two-round failure condition.
- After a round with \(x_t < m-1\), keep tracking whether this is the first or second consecutive shortfall.

Behavioral interpretation:
- Cooperate immediately and repeatedly whenever the group shows enough support to reach the threshold with your help.
- Give the group one full extra round of patience after a shortfall.
- Only after two consecutive shortfalls, briefly step back for one round, then return to cooperation.
- Never carry a defect into the final round; end by supporting the collective project.
'''

description_ALTRUISTIC_12 = '''
Maintain a simple “support until clearly unnecessary” rule.

Definitions from history:
- Let `o_t` be the number of opponents who cooperated in round `t`.
- Let `s_t = o_t + 1` if you cooperated in round `t`, otherwise `s_t = o_t` — the total number of cooperators in round `t`.
- Let `bad_streak` be the number of consecutive previous rounds with `s_t < m`.

Decision rule for round `t`:

1. **Round 1:** Cooperate.

2. **If the last round already met the threshold without you**
   - If `o_{t-1} >= m`, defect.
   - This means the group is already safely over the threshold; your help is no longer needed this round.

3. **If your cooperation can make the threshold**
   - If `o_{t-1} == m - 1`, cooperate.
   - Your contribution is pivotal, so always provide it.

4. **If the group was short of the threshold**
   - If `o_{t-1} <= m - 2`:
     - Cooperate if `bad_streak < 2`.
     - Defect if `bad_streak >= 2`.

Update rule after each round:
- If `s_t < m`, increment `bad_streak`.
- Otherwise, reset `bad_streak = 0`.

Edge cases:
- **Last round:** apply the same rule; do not change behavior just because the game is ending.
- **First two rounds:** never defect before observing at least two consecutive failures.
- **If cooperation is exactly one short of the threshold:** always cooperate, regardless of past history.

Behavioral posture:
- Start fully cooperative.
- Keep cooperating through brief or isolated failures.
- Only withhold cooperation after repeated evidence that the group is not responding, and only when your contribution is not pivotal.
- Never defect when your action can directly help reach the collective target.
'''

description_ALTRUISTIC_13 = '''
Start with cooperation and use a threshold-support rule:

1. First round  
   Play C.

2. State you keep from history  
   Let `s_t` be the number of players who cooperated in round `t`, and let `h_t` be the number of your own previous rounds in which you played C.  
   Track the most recent streak of rounds in which the group met the threshold:
   - `good_streak` = consecutive most recent rounds with `s_t ≥ m`
   - `bad_streak` = consecutive most recent rounds with `s_t < m`

3. Core decision rule for round `t ≥ 2`  
   Play C if any of the following holds:
   - `good_streak ≥ 1` and the last round met the threshold
   - `bad_streak = 1` and `s_{t-1}` was only short by 1, i.e. `s_{t-1} = m - 1`
   - `good_streak ≥ 2` and cooperation has been stable for at least two consecutive rounds

   Play D only if:
   - `bad_streak ≥ 2` and the last two rounds both missed the threshold by at least 2, i.e. `s_{t-1} ≤ m - 2` and `s_{t-2} ≤ m - 2`

4. Repair rule after a failure  
   If the threshold was missed in the previous round but by a small margin (`s_{t-1} = m - 1`), keep cooperating for one more round to help restore the collective target.

5. Stabilization rule after success  
   If the threshold was met in the previous round, continue cooperating.  
   If it has been met in two consecutive rounds, continue cooperating unconditionally unless a later round breaks the pattern twice in a row.

6. Endgame  
   Do not switch to defect in the final rounds just because the game is ending.  
   In the last round, play the same action you would have played under the core rule for that history, with one exception: if the last two rounds both met the threshold, play C.

7. Minimal-cooperation safeguard  
   If cooperation is persistently failing, do not abandon the collective immediately.  
   Keep playing C through one shortfall and only move to D after two consecutive substantial shortfalls.

8. Altruistic orientation  
   Default to C.  
   Treat isolated failures as recoverable.  
   Preserve cooperation whenever there is evidence the group can still reach the threshold.  
   Defect only after repeated evidence that your continued cooperation is not enough to keep the collective above the minimum.
'''

description_ALTRUISTIC_14 = '''
Initialize `mode = hopeful` and `fail_streak = 0`.

For round `t = 1`:
- Play `C`.

For every round `t > 1`:
- Let `o_{t-1}` be the number of opponents who cooperated in the previous round.
- Update:
  - if `o_{t-1} >= m - 1`, set `fail_streak = 0`
  - else set `fail_streak += 1`

Decision rule:
- Play `C` if any of the following holds:
  1. `t == r`  
  2. `o_{t-1} >= m - 1`
  3. `fail_streak == 1`
  4. `t % 3 == 0` and `fail_streak >= 2`
- Otherwise play `D`.

Interpretation of the rule:
- Always begin by contributing.
- Keep contributing whenever the group is already close enough to succeed.
- Give one round of forgiveness after a shortfall.
- If shortfalls continue, keep a periodic cooperation probe every third round so recovery remains possible.
- Never defect in the final round.
'''

description_ALTRUISTIC_15 = '''
Cooperate in round 1.

For each later round, let \(x_{t-1}\) be the number of opponents who cooperated in the previous round, and let \(x_t^{\text{need}} = m - 1\) be the number of cooperating opponents you need in order for your own cooperation to help reach the threshold.

Decision rule for round \(t\):

- Cooperate if either:
  - the previous round met the threshold with your cooperation contributing, or
  - the previous round came within one opponent of meeting the threshold, or
  - at least half of the opponents cooperated in the previous round.
- Defect only if opponents were broadly uncooperative in the previous round.

More precisely:

```text
Round 1:
    play C

For round t > 1:
    if x_{t-1} >= m - 1:
        play C
    else if x_{t-1} >= ceil((n - 1)/2):
        play C
    else:
        play D
```

Edge handling:

- If \(m = 2\), cooperate whenever at least one opponent cooperated in the previous round.
- If \(m = n - 1\), cooperate whenever all but at most one opponent cooperated in the previous round.
- In the final round, play the same action the rule prescribes; do not switch to endgame defection.
- After any round in which the threshold is achieved, return to cooperation immediately in the next round.
- After any round with very low cooperation, require at least one recovery round of visible cooperation before resuming full cooperation.

Altruistic refinement:

- If the previous round missed the threshold by exactly one cooperating opponent, cooperate anyway.
- If cooperation has been stable for the last two rounds, keep cooperating unless the previous round fell far below the half-cooperation benchmark.
- If the history alternates or is noisy, default to cooperation unless repeated failure makes cooperation ineffective in reaching the threshold.

Compact form:

```text
Start with C.
Then:
    C if recent cooperation is at least threshold-adjacent or majority-level;
    D only after clear and repeated collective defection.
```


'''

description_ALTRUISTIC_16 = '''
Round 1: cooperate.

Maintain two counters from the observed history:
- `fail_streak`: consecutive rounds in which fewer than `m` total players cooperated
- `support_streak`: consecutive rounds in which at least `m-1` opponents cooperated

Decision rule for round `t > 1`:

1. **Cooperate immediately after any sign of viable cooperation**
   - If the previous round had at least `m-1` cooperating opponents, play `C`.

2. **Forgive short-term failure**
   - If `fail_streak` is 1 or 2, play `C`.

3. **Default to cooperation in borderline cases**
   - If the previous round was close to the threshold, meaning the number of cooperating opponents was at least `m-2`, play `C`.

4. **Temporary retreat only after persistent collapse**
   - If `fail_streak >= 3` and the previous round had zero cooperating opponents, play `D` for exactly one round.
   - After that single `D`, return to `C` on the next round regardless of what happened.

5. **Final round**
   - Play `C`.

Update counters after each round:
- If total cooperators in the round `>= m`, set `fail_streak = 0` and increment `support_streak`
- Otherwise, increment `fail_streak` and set `support_streak = 0`

Equivalent pseudocode:

```text
if t == 1:
    action = C
else:
    if previous_opponent_cooperators >= m-1:
        action = C
    elif fail_streak <= 2:
        action = C
    elif previous_opponent_cooperators >= m-2:
        action = C
    elif fail_streak >= 3 and previous_opponent_cooperators == 0:
        action = D
        next_round_force_C = true
    else:
        action = C

if t == r:
    action = C
```

Behavioral commitment:
- Start by cooperating.
- Keep cooperating through brief setbacks.
- Keep cooperating when the group is near the threshold.
- Only defect once, and only after sustained complete collapse.
- Return to cooperation immediately afterward.
'''

description_ALTRUISTIC_17 = '''
Cooperate in round 1.

After each round, track:
- `x_t`: number of other players who cooperated in round `t`
- `s_t = x_t + 1` if you cooperated in round `t`, else `s_t = x_t`  
  (the total number of cooperators you can infer from the public count and your own action)

Use these rules:

1. **Automatic cooperation when success was achieved or nearly achieved**
   - If `s_{t-1} >= m`, cooperate in round `t`.
   - If `s_{t-1} = m - 1` and you cooperated in round `t-1`, cooperate in round `t`.

2. **Recovery from shortfall**
   - If `s_{t-1} < m - 1`, cooperate in round `t` if either:
     - the shortfall is small: `m - 1 - s_{t-1} <= 1`, or
     - cooperation has been rising for two consecutive rounds:
       `s_{t-1} > s_{t-2}` and `s_{t-2} > s_{t-3}`.

3. **Persistent defection response**
   - If `s_{t-1} < m - 1` for three consecutive rounds and `s_{t-1} <= s_{t-2} <= s_{t-3}`, defect in round `t` once, then return to cooperation immediately in the next round unless the same pattern continues.

4. **Last rounds**
   - In the final round, cooperate unless the previous two rounds both had `s < m - 1` and no upward trend.
   - In the last two rounds, never initiate a defection streak longer than one round.

5. **General tie-break**
   - When the rule set does not force defection, cooperate.

Compact pseudocode:

```text
Round 1: play C

For round t > 1:
    observe s_{t-1}

    if s_{t-1} >= m:
        play C
    else if s_{t-1} = m - 1 and I played C in t-1:
        play C
    else if t >= 4 and s_{t-1} < m - 1 and s_{t-2} < m - 1 and s_{t-3} < m - 1:
        if s_{t-1} <= s_{t-2} and s_{t-2} <= s_{t-3}:
            play D
        else:
            play C
    else if s_{t-1} < m - 1 and (m - 1 - s_{t-1} <= 1):
        play C
    else if t >= 4 and s_{t-1} > s_{t-2} and s_{t-2} > s_{t-3}:
        play C
    else:
        play C
```

Behavioral intent:
- Begin by contributing immediately.
- Keep cooperating whenever the group is meeting or nearly meeting the threshold.
- Absorb occasional free-riding without retaliation.
- Use only a single-round withdrawal after repeated stagnation, then resume cooperation.
- End by favoring cooperation rather than exploiting the final rounds.
'''

description_ALTRUISTIC_18 = '''
Cooperate by default, and defect only when cooperation from you is no longer a meaningful contribution to the group’s chance of reaching the threshold.

Let `S_t` be the number of your opponents who cooperated in round `t`.

**Decision rule**
- **Round 1:** play `C`.
- **Round t > 1:**
  - If `S_{t-1} >= m - 2`, play `C`.
    - Your cooperation is still within one step of making the threshold possible or ensuring it is met.
  - If `S_{t-1} = m - 3`, play `C` once more as a forgiveness round.
    - If the previous round was also `<= m - 3`, switch to `D`.
  - If `S_{t-1} <= m - 4`, play `D`.
    - Resume `C` immediately in any later round where `S >= m - 2`.

**Equivalent compact form**
```text
if t == 1:
    C
else if S[t-1] >= m-2:
    C
else if S[t-1] == m-3:
    if t == 2 or S[t-2] >= m-2:
        C
    else:
        D
else:
    D
```

**Edge cases**
- **First round:** always cooperate.
- **Last round:** use the same rule; do not add any endgame defection.
- **After a run of low cooperation:** remain in `D` only while the previous round stayed far below the threshold; return to `C` as soon as the group is again near viable cooperation.

**Altruistic posture**
- Default to helping the group.
- Give the group a short buffer when cooperation is only slightly below the needed level.
- Stop contributing only when your action is clearly not enough to move the outcome toward collective success.
'''

description_ALTRUISTIC_19 = '''
Cooperate in round 1.

For every later round, keep a running record of:

- `S`: number of previous rounds in which at least `m` players cooperated
- `T`: number of previous rounds in which fewer than `m` players cooperated
- `s_recent`: number of cooperators observed in the immediately previous round

Decision rule for round `t`:

1. If the previous round met the threshold (`s_recent >= m`), cooperate.
2. If the previous round missed the threshold by only one (`s_recent = m - 1`), cooperate.
3. If the previous round missed the threshold by two or more (`s_recent <= m - 2`), cooperate anyway for the first two such misses in a row; after that, defect until the group reaches the threshold again.
4. If the last three rounds all missed the threshold, cooperate only if the current round would be the third consecutive cooperative attempt after a miss; otherwise defect for one round, then return to cooperation as soon as the threshold is met again.

Equivalent pseudocode:

```text
if t == 1:
    play C

else if s_recent >= m:
    play C

else if s_recent == m - 1:
    play C

else if last_three_rounds_all_missed:
    if current_round_is_first_defensive_defection:
        play D
    else:
        play C when threshold is restored, otherwise D

else if consecutive_misses < 2:
    play C
else:
    play D
```

Concrete implementation:

- Round 1: `C`
- After any round with at least `m` cooperators: `C`
- After a near-miss with exactly `m - 1` cooperators: `C`
- After a clear miss with `m - 2` or fewer cooperators:
  - cooperate for up to two consecutive misses
  - if the group still does not recover, defect for one round to avoid waste
  - immediately return to cooperation once observed cooperation reaches `m` again

Last-round behavior:

- If the prior round met or nearly met the threshold, cooperate.
- If the group has been persistently failing, defect in the final round only if it is already in the defensive-defection state; otherwise continue to cooperate.

Altruistic priority rule:

- Default to cooperation whenever there is any plausible path to helping the group reach `m`.
- Use defection only as a temporary reset after repeated failures, never as a punishment cycle.
- Once the group shows any recovery toward the threshold, return to cooperation immediately and stay there as long as the observed cooperation level is at least `m - 1`.
'''

description_ALTRUISTIC_20 = '''
Cooperate in the first round.

For each later round, let H be the number of opponents who cooperated in the previous round, and let T = m - 1 be the minimum number of cooperating opponents needed for your own cooperation to be pivotal.

Decision rule:
- Cooperate if H ≥ T.
- Cooperate if H = T - 1 and at least one of the last two rounds had H ≥ T.
- Defect otherwise.

Equivalent form:
- Stay cooperative while the group is at or above the threshold.
- If the group slips just below the threshold, keep cooperating for one extra round to help restore it.
- If the group remains below threshold for two consecutive rounds, defect until cooperation recovers.

Edge cases:
- Round 1: cooperate.
- If m = 2, then T = 1, so cooperate whenever at least one opponent cooperated in the previous round; if none did, cooperate once more as a rescue move, then defect if that fails again.
- In the final round: cooperate if either of the last two rounds reached threshold, or if your cooperation can make the group reach threshold this round based on the most recent observed count; otherwise defect.
- If a streak of full cooperation is observed in consecutive rounds, continue cooperating without interruption.

Update rule after each round:
1. Record H.
2. If H ≥ T, reset the cooperation-support state to active.
3. If H = T - 1, keep the cooperation-support state active for one more round.
4. If H ≤ T - 2, clear the cooperation-support state after one missed rescue round.

Behavioral pattern:
- Begin by contributing.
- Mirror successful cooperation by staying in.
- Extend one round of help when the group narrowly fails.
- Withdraw only after repeated failure to meet the threshold.
- Re-enter cooperation immediately once the group shows renewed support.
'''

description_ALTRUISTIC_21 = '''
Cooperate in round 1.

For every later round, let:
- `H_t` = number of opponents who cooperated in round `t`
- `S_t` = number of cooperators among the other `n-1` players needed for the threshold, so `S_t = m - 1` if you cooperate, and `S_t = m` if you defect
- `T_t` = smoothed cooperation level from recent history:
  - `T_t = average(H_1, ..., H_{t-1})`

Decision rule:

1. **Always cooperate when your cooperation can make the threshold possible and recent cooperation has been near the threshold.**
   - Cooperate if `T_t >= m - 1`
   - Cooperate if `H_{t-1} >= m - 2` and `H_{t-2} >= m - 2` when those rounds exist

2. **Otherwise, cooperate only after clear cooperative support.**
   - Cooperate if `H_{t-1} >= m - 1`
   - Cooperate if `H_{t-1} = m - 2` and `T_t >= m - 1/2`

3. **Defect when cooperation has fallen well below what is needed to sustain the collective target.**
   - Defect if `T_t < m - 2`
   - Defect if the last two observed rounds both had `H <= m - 3`

4. **Endgame rule.**
   - In the last round, cooperate if and only if `T_t >= m - 1`
   - If the last two rounds were both at or above `m - 1` opponents cooperating, cooperate regardless of earlier rounds

5. **Recovery rule after a low-cooperation round.**
   - If a round had `H_t < m - 2`, switch to defect next round unless the following round already restores `H >= m - 1`

Operationally, use this priority order each round:
- If the endgame rule applies, use it.
- Else if the recovery rule triggers, defect.
- Else if recent cooperation is strong enough, cooperate.
- Else defect.

Behavioral pattern:
- Start cooperatively.
- Stay cooperative while the group is close to or above the threshold.
- Temporarily defect when the group repeatedly falls far below the threshold.
- Return to cooperation immediately when the group recovers to the threshold-supporting range.
'''

description_ALTRUISTIC_22 = '''
Round 1: cooperate.

For round t > 1, let `o[t-1]` be the number of opponents who cooperated in the previous round, and let `self[t-1]` be your own previous action. Define:

`total[t-1] = o[t-1] + 1` if `self[t-1] = C`, otherwise `total[t-1] = o[t-1]`.

Decision rule:
- Cooperate if `total[t-1] >= m`
- Cooperate if `total[t-1] = m - 1`
- Cooperate if `total[t-1] < m - 1` but `total[t-2] >= m - 1` for the previous round
- Defect only after two consecutive rounds with `total < m - 1`

Equivalent state-based version:
- `state = hopeful` initially
- In `hopeful`, play `C`
- If a round ends with `total >= m - 1`, stay in `hopeful`
- If a round ends with `total < m - 1`, switch to `cautious`
- In `cautious`, play `D`
- If any later round ends with `total >= m - 1`, immediately return to `hopeful`
- Otherwise remain in `cautious`

Tie and edge handling:
- If you ever observe exactly `m - 1` cooperators total, treat that as a near-success and keep cooperating
- On the last round, follow the same rule as any other round
- If no prior history exists beyond round 1, cooperate by default

Action summary:
- Default action: `C`
- Temporary deviation: `D` only after two straight weak rounds with fewer than `m - 1` total cooperators
- Immediate recovery: return to `C` as soon as the group reaches `m - 1` or more cooperators again
'''

description_ALTRUISTIC_23 = '''
Round 1: play C.

For every round t > 1, let x be the number of opponents who cooperated in round t - 1.

Play C if any of the following holds:
- x ≥ m - 1
- x = m - 2 and at least one of the previous two rounds also had x' ≥ m - 2
- t = r

Play D only if all of the following hold:
- x ≤ m - 3
- the previous two rounds also had opponent cooperation at or below m - 3
- t < r

After playing D once, return to C immediately in the next round.

Edge handling:
- If m - 2 < 0, treat the condition x = m - 2 as impossible and ignore it.
- If m - 3 < 0, ignore the D-trigger and keep playing C.
- If the game reaches the final round, always play C.

State memory:
- Store the last two observed opponent-cooperation counts.
- Store whether the last action was D; if so, clear the defection trigger and resume C next round.
'''

description_ALTRUISTIC_24 = '''
Play C in round 1.

For every later round t > 1, let H be the number of cooperators observed among the other n − 1 players in round t − 1.

1. If H ≥ m, play C.
2. If H = m − 1, play C again.
3. If H ≤ m − 2, play D for one round, then reassess from the next round.

Memory rule:
- After any round in which you played D, return to C immediately if the next observed round had H ≥ m − 1; otherwise continue with D until H reaches at least m − 1.

Last-round rule:
- Play C in the final round.

Short-horizon adjustment:
- If r = 2, play C in both rounds.
- If r = 3, play C in rounds 1 and 3, and in round 2 follow the rule above.

Fallback rule for persistent failure:
- If the last two observed rounds both had H ≤ m − 2, switch to C for one trial round; if that trial round again falls below m − 1, return to the D-for-one-round rule.

Implementation form:

```
Round 1: C

For round t = 2 to r-1:
    if H(t-1) >= m-1:
        play C
    else if H(t-1) <= m-2:
        if last action was D and H(t-1) <= m-2:
            continue D
        else:
            play D for one round

Round r: C
```

Behavioral intent:
- Default to cooperation.
- Keep cooperating as long as the group is at or near the threshold.
- Use brief, temporary defection only after clear collective failure, then return to cooperation quickly.
- Never withhold cooperation in the opening or closing round.
'''

description_ALTRUISTIC_25 = '''
Cooperate in the first round.

For every later round, set a cooperation score:

- Let `H` be the number of cooperators observed among the other `n-1` players in the previous round.
- Let `S` be the number of rounds so far in which `H >= m-1`.

Decision rule for round `t > 1`:
- Play `C` if `H >= m-1`.
- Also play `C` if `H = m-2` and the previous round had `H_prev >= m-1`.
- Otherwise, if the last two rounds both had `H < m-2`, play `D` for one round only.
- In all other cases, play `C`.

Edge handling:
- Round 1: play `C`.
- If the previous round is unavailable, treat it as if `H >= m-1`.
- In the final round, play `C` unless the last two rounds both failed by a wide margin (`H < m-2`), in which case play `D`.

Full policy in compact form:

```text
Round 1: C

For round t > 1:
    if H_prev >= m-1:
        play C
    else if H_prev == m-2 and H_prev_prev >= m-1:
        play C
    else if H_prev < m-2 and H_prev_prev < m-2:
        play D
    else:
        play C
```

Persistent altruism adjustment:
- If at any point the group has achieved `H >= m-1` in at least half of the completed rounds, default to `C` whenever the current evidence is ambiguous.
- If cooperation has ever reached the threshold in the immediately preceding round, prefer `C` until two consecutive threshold failures occur.

If your own action in the current round can be chosen after observing the previous round only, this policy reduces to:
- open with `C`,
- keep cooperating whenever the group is near the threshold,
- defect only after repeated, clear shortfalls,
- immediately return to cooperation after any sign that the threshold is achievable again.
'''

description_ALTRUISTIC_26 = '''
Cooperate on the first round.

After each round, let H be the number of cooperators you observed among the other n−1 players.

Maintain a trust state for the opponents, initialized to optimistic.

Decision rule for round t > 1:

- Cooperate if at least m−1 of the other players cooperated in the previous round.
- Cooperate even if fewer than m−1 cooperated, provided the recent trend is improving and the shortfall is small:
  - in the last round, H ≥ m−2, or
  - in the last two rounds, the average observed cooperation among the others is at least m−1.
- Defect only if cooperation has clearly collapsed:
  - in the last round, H ≤ m−3, and
  - in the last two rounds, cooperation among the others has not recovered.

For the final round, cooperate unless the others have shown persistent defection:
- If the last two rounds each had H ≥ m−2, cooperate.
- If the last two rounds each had H ≤ m−3, defect.
- Otherwise, cooperate.

Update rule after each round:

- If the observed cooperation among the others meets or nearly meets the threshold, keep cooperating.
- If the observed cooperation falls short, do not immediately retaliate; give one forgiveness round.
- If the shortfall persists for two consecutive rounds, switch to defect until the others show recovery.

Compact pseudocode:

```
state = optimistic

for round t:
    if t == 1:
        play C
    else if t == r:
        if H[t-1] >= m-2 or H[t-2] >= m-2:
            play C
        else if H[t-1] <= m-3 and H[t-2] <= m-3:
            play D
        else:
            play C
    else:
        if H[t-1] >= m-1:
            play C
            state = optimistic
        else if H[t-1] >= m-2:
            play C
            state = forgiving
        else if H[t-2] >= m-2:
            play C
            state = forgiving
        else:
            play D
            state = cautious
```

Edge cases:

- If m = 2, cooperate whenever at least one other player cooperated in the previous round; defect only after two consecutive rounds with no support.
- If m = n−1, cooperate whenever nearly everyone else cooperated; tolerate one-round dips, but defect after repeated failure.
- If the others are fully cooperative, always cooperate.
- If the others are fully uncooperative for multiple rounds, switch to defect to avoid waste, then return to cooperation immediately when cooperation reappears.

Altruistic commitment:

- Default to cooperation.
- Forgive brief failures.
- Support near-threshold collective effort.
- Never punish a single lapse with immediate defection.
- Re-enter cooperation as soon as the group shows any credible recovery.
'''

description_ALTRUISTIC_27 = '''
Round 1: play C.

For each later round t:

1. Let q be the number of opponents who cooperated in round t-1.
2. Let s be the number of consecutive recent rounds, ending in round t-1, in which q was below m - 1.

Decision rule:
- Play C if any of the following holds:
  - q ≥ m - 1
  - s = 1
  - t is the last round
  - you are in a recovery window after a temporary defection
- Play D only if all of the following hold:
  - q ≤ m - 2
  - s ≥ 2
  - you are not in a recovery window

Recovery window:
- If you play D in a round because of sustained under-cooperation, then play C in the next 2 rounds regardless of q.
- After those 2 rounds, return to the main decision rule.

Tie-breaking and edge cases:
- If q = m - 1 exactly, always play C.
- If m = 2, then q ≥ 1 means play C; only sustained zero cooperation triggers the temporary D.
- In the final 2 rounds, play C unconditionally.
- If the game has just recovered from a low-cooperation streak, stay with C until another sustained streak of under-cooperation appears.

State update after each round:
- If q ≥ m - 1, reset s = 0.
- If q ≤ m - 2, increment s by 1.
- If you are in a recovery window, decrement its remaining length by 1 after your move.

Behavioral principle:
- Default to cooperation.
- Match any viable group of cooperators immediately.
- Only step back after repeated evidence that the group is not coming close to the threshold.
- Return to cooperation as soon as the group shows recovery.
'''

description_ALTRUISTIC_28 = '''
Cooperate in round 1.

After each round, let x_t be the number of cooperators you observed among the other n−1 players in round t, and let s_t = x_t + 1 if you cooperated, else x_t.  
Let g_t = m − s_t, the number of additional cooperators that would have been needed for the threshold to be met in round t.

Decision rule for round t+1:
- If t = r, no action.
- If the threshold was met in round t, cooperate again.
- If the threshold was not met in round t:
  - Cooperate if x_t ≥ m − 2.
  - Defect only if x_t ≤ m − 3 for two consecutive rounds.
  - Reset to cooperate immediately after any round in which x_t ≥ m − 2.

Last-round rule:
- Cooperate in the last round unless both of the previous two rounds had x_t ≤ m − 3, in which case defect.

Early-round rule:
- In rounds 1 through min(3, r), cooperate unconditionally.

Commitment rule:
- If the threshold was met in the immediately preceding round, stay with cooperation for the next 2 rounds.
- If the threshold was met in at least one of the last 3 rounds, cooperate.

Minimal-cooperation safeguard:
- If x_t = m − 1, cooperate in the next round.
- If x_t = m − 2, cooperate in the next round and continue cooperating unless the next round also falls short by at least 2.
- If x_t ≤ m − 3, switch to defect only after two such rounds in a row, and return to cooperation on the first round after any higher-cooperation observation.

Default posture:
- When in doubt, cooperate.
- Treat isolated failures as noise.
- Treat sustained low cooperation as the only trigger for temporary defection.

Pseudocode:

```
state = "cooperate"

for t in 1..r:
    play C if state == "cooperate" else D

    observe x_t  # opponents who cooperated

    if t == r:
        stop

    if t <= 3:
        state = "cooperate"
        continue

    if threshold_met_in_round_t:
        state = "cooperate"
    else if x_t >= m - 2:
        state = "cooperate"
    else:
        if previous_round_x <= m - 3 and x_t <= m - 3:
            state = "defect"
        else:
            state = "cooperate"

    previous_round_x = x_t
```

Tie-breaking and edge cases:
- If n = m + 1, interpret x_t ≥ m − 2 as the main recovery signal and never defect after a single shortfall.
- If m = 2, cooperate unless both of the last two rounds had zero other cooperators.
- If r = 2, cooperate in both rounds.
- If the game has just one remaining round, cooperate unless the last two rounds were both strongly below threshold (x_t ≤ m − 3).
'''

description_ALTRUISTIC_29 = '''
Round 1: play C.

For round t > 1, let s be the number of opponents who cooperated in round t - 1.

- If s + 1 ≥ m: play C.
- If s = m - 1: play C.
- If s < m - 1:
  - play C for every round except possibly the last;
  - in the last round, play C unless the previous two rounds both had s = 0, in which case play D.

State variables to track:
- The last observed opponent-cooperation count.
- Whether the threshold was reached in the previous round.
- Whether the last two rounds were complete non-cooperation by opponents.

Tie-breaking and edge cases:
- If the information from the previous round is unavailable for any reason, play C.
- If multiple consecutive rounds are indistinguishable in the stored history, default to C.
- If the game is already in a streak of successful rounds, continue playing C without interruption.

Behavioral principle:
- Cooperate by default.
- Keep cooperating whenever the group is close to or at the threshold.
- Only step back in the final round after repeated, complete refusal by the others.
'''

description_ALTRUISTIC_30 = '''
Cooperate in round 1.

For each later round t, let h(t-1) be the number of opponents who cooperated in the previous round, and let s(t-1) be the number of opponents who cooperated in the last round among the most recent x rounds? We need history-based. Define a short memory score:

- Let H_t be the average number of cooperating opponents over the last L rounds, where L = min(3, t-1).
- Let q_t = floor((m-1) / (n-1))? Wait, in symmetric setting need threshold for opponents. Better use the minimum number of cooperating opponents needed if you cooperate: need total cooperators m, so if you cooperate, you need at least m-1 opponents cooperating. If you defect, you need at least m opponents cooperating.

Strategy:

1. Round 1: Cooperate.

2. For rounds t = 2 to r:
   - Let x_t be the number of opponents who cooperated in round t-1.
   - Let \bar{x}_t be the average of the observed opponent cooperation counts over the last up to 3 rounds.
   - Define the target threshold for others as T_C = m - 1.
   - Define a recovery threshold T_D = m - 2.

Decision rule:
- Cooperate if either:
  - x_t ≥ T_C, or
  - \bar{x}_t ≥ T_C - 1/2, or
  - t = r
- Defect otherwise.

Refinement for altruistic bias:
- If x_t = T_C - 1, cooperate anyway for one more round unless the last two rounds both had x < T_D.
- If x_t ≤ T_D - 1 for two consecutive rounds, defect until a round with x_t ≥ T_D appears, then return to cooperating.

Last round:
- Cooperate unless the last two rounds both had x_t ≤ T_D - 1.

Edge cases:
- If m = 2, then T_D = 0; in that case, cooperate in every round except after two consecutive rounds with zero opponents cooperating, then defect until at least one opponent cooperates again.
- If t ≤ 3, use all available history rather than a full 3-round average.
- If no opponents cooperated in the previous round, do not immediately abandon cooperation; require two consecutive zero-cooperation rounds before switching to defect.

Compact pseudocode:

```
Round 1: C

For round t > 1:
    x = opponents_cooperating_in_round(t-1)
    a = average(opponents_cooperating_in_round(u) for u in max(1, t-3) .. t-1)
    z = number of consecutive recent rounds ending at t-1 with x <= m-3

    if t == r:
        if z >= 2:
            play D
        else:
            play C
    else if z >= 2:
        if x >= m-2:
            play C
        else:
            play D
    else if x >= m-1:
        play C
    else if a >= (m-1) - 0.5:
        play C
    else:
        play C if x == m-2 else D
```

Core behavior:
- Start by helping.
- Keep helping when the group is close to the threshold.
- Give a short forgiveness window after weak cooperation.
- Switch to restraint only after repeated failure to meet the threshold.
- Return to cooperation immediately when the group recovers.
'''

description_ALTRUISTIC_31 = '''
Cooperate in round 1.

For each later round, let \(x_t\) be the number of opponents who cooperated in round \(t\), so total cooperators that round were \(x_t + 1\) if you cooperated and \(x_t\) if you defected. Keep a running memory of the last observed cooperation level and a trend score:

- \(s_t = x_t - (n-1)\cdot \alpha\), where \(\alpha = \frac{m-1}{n-1}\)
- Maintain \(T_t = 0.7T_{t-1} + s_t\), with \(T_1 = s_1\)

Decision rule for round \(t+1\):

1. **Strong support:** If \(x_t \ge m-1\), cooperate.
2. **Near-threshold and improving:** If \(x_t = m-2\) and \(x_t > x_{t-1}\), cooperate.
3. **Fragile support with positive trend:** If \(x_t \ge m-3\) and \(T_t \ge 0\), cooperate.
4. **Otherwise:** defect.

Edge cases:

- **Round 1:** cooperate.
- **Round 2:** if the first round had at least \(m-1\) opponent cooperators, cooperate; otherwise defect only if \(m\) is very high relative to \(n\) and the first round showed clearly insufficient support (\(x_1 < m-2\)); else cooperate.
- **Final round:** cooperate unless the last two observed rounds both had \(x_t < m-2\); in that case defect.
- **If \(m = 2\):** cooperate every round unless the last two rounds had zero opponent cooperators.
- **If \(m = n-1\):** cooperate every round until two consecutive rounds fall short by at least 2 opponents; then defect until cooperation recovers to at least \(n-2\) opponents.

Full policy in compact form:

```text
Round 1: C

For round t > 1:
    observe x_{t-1}
    update trend:
        s = x_{t-1} - (n-1)*((m-1)/(n-1))
        T = 0.7*T + s

    if x_{t-1} >= m-1:
        play C
    else if x_{t-1} == m-2 and x_{t-1} > x_{t-2}:
        play C
    else if x_{t-1} >= m-3 and T >= 0:
        play C
    else:
        play D
```

Behavioral commitment:

- Start by contributing.
- Continue contributing whenever cooperation is near or above the threshold.
- Use defection only as a brief signal when the group is persistently below the safety level.
- Return to cooperation immediately when the observed cooperation level recovers.
'''

description_ALTRUISTIC_32 = '''
Play C in every round.

Decision rule:
- Round 1: cooperate.
- Rounds 2 through r: cooperate regardless of the observed history.
- Never switch to D based on past cooperation counts, streaks, or the remaining number of rounds.

If you want the rule written procedurally:

```text
for each round t:
    choose C
```

Edge cases:
- If the previous round had very low cooperation: still choose C.
- If cooperation has been consistently high: choose C.
- If the game is in the final round: choose C.
- If the group has already failed many rounds in a row: choose C.
- If the observed history is empty or incomplete: choose C.

Altruistic stance:
- Always contribute.
- Treat your action as a constant support signal to the group.
- Never retaliate, punish, or condition your cooperation on others’ past failures.
'''

description_BENEVOLENT_5 = '''
Maintain a binary state `trust` initialized to `true`.

Let `H_t` be the total number of cooperators in round `t` after that round is observed.

Decision rule for round `t`:

1. **Round 1:** play `C`.

2. **Rounds 2 through r:**
   - If `H_{t-1} >= m`, set `trust = true`.
   - Else if `H_{t-2} < m - 1` and `H_{t-1} < m - 1`, set `trust = false`.
   - Otherwise keep the previous value of `trust`.

   Then:
   - If `trust = true`, play `C`.
   - If `trust = false`, play `D`.

Equivalent pseudocode:

```text
trust = true

for t in 1..r:
    if t == 1:
        play C
    else:
        if H[t-1] >= m:
            trust = true
        else if H[t-2] < m-1 and H[t-1] < m-1:
            trust = false

        if trust:
            play C
        else:
            play D
```

Edge handling:

- If `m = 2`, the condition `H < m - 1` means `H = 0`, so a single opponent cooperator is enough to keep cooperation active.
- If a round meets the threshold exactly (`H_t = m`), immediately return to cooperation in the next round.
- If cooperation has been weak for two consecutive rounds, defect only until a round shows renewed support at or above `m - 1`.
- In the last round, use the same rule; do not change behavior just because the game is ending.
'''

description_BENEVOLENT_6 = '''
Initialize with cooperation.

For each round \(t\):

- Let \(o_{t-1}\) be the number of opponents who cooperated in the previous round.
- Let \(s_{t-1} = o_{t-1} + 1\) if you cooperated last round, otherwise \(s_{t-1} = o_{t-1}\).  
  This is the total number of cooperators last round.

Decision rule:
1. Cooperate in round 1.
2. For round \(t \ge 2\), cooperate if either:
   - the previous round met the threshold (\(s_{t-1} \ge m\)), or
   - the previous round missed the threshold by exactly one player (\(s_{t-1} = m-1\)).
3. Defect only if the previous round fell short by at least two cooperators (\(s_{t-1} \le m-2\)).

Forgiveness rule:
- After any round in which the threshold is met, immediately return to cooperation.
- After a single failed round, still cooperate once to give the group a chance to recover.
- Only after two consecutive rounds below threshold do you switch to defecting.

Edge cases:
- If \(m=2\), treat “missed by exactly one” as “there were no other cooperators”; still cooperate once more before defecting.
- In the last round, use the same rule as any other round; do not add endgame defection.
- If you cannot tell whether the threshold was met from your own action alone, use the observed number of cooperating opponents from the previous round and infer \(s_{t-1}\) accordingly.

Behavioral form:
- Default mode: cooperative.
- Response to partial failure: patient and forgiving.
- Response to persistent failure: temporary self-protection, then immediate return to cooperation as soon as the group shows recovery.
'''

description_BENEVOLENT_7 = '''
Round 1: play C.

For round t > 1, let o_{t-1} be the number of opponents who cooperated in the previous round, and define a round as “repairable” if o_{t-1} ≥ m - 1.

Decision rule:
- If the previous round was repairable, play C.
- If the previous round was not repairable, check the round before it:
  - If the two most recent rounds were both not repairable, play D for exactly one round.
  - Otherwise, play C.
- After any round in which you play D, return to C immediately in the next round.

Equivalent compact form:
- Cooperate by default.
- Defect only as a one-round pause after two consecutive rounds in which even your own cooperation could not have been enough to reach the cooperation threshold.

Edge cases:
- If there is only one prior round of history, treat it as not enough evidence for defection and play C unless that round was repairable.
- In the final round, use the same rule; there is no special endgame defection.
- If a round reaches repairable support again at any point, reset to unconditional cooperation on the next round.

Benevolent posture:
- Favor cooperation whenever there is a plausible path to collective success.
- Use defection only as a brief, disciplined fallback when recent history shows sustained collapse.
- Immediately resume cooperation as soon as recovery becomes possible.
'''

description_BENEVOLENT_8 = '''
Let \(h_t\) be the number of opponents who cooperated in round \(t\), so \(h_t \in \{0,\dots,n-1\}\). Let \(H_t\) be the cumulative number of opponent cooperations through round \(t\).

Use this rule:

### Core rule
- **Round 1:** play **C**.
- **Round 2 onward:** play **C** if both conditions hold:
  1. **Recent cooperation is sufficient:** in the previous round, \(h_{t-1} \ge m-1\), or \(h_{t-1} \ge m\) if you defected in round \(t-1\).
  2. **Cooperation is stable:** among the last up to 3 rounds, at least 2 of them had \(h_s \ge m-1\).

- Otherwise, play **D**.

### More explicit form
For round \(t \ge 2\):

1. Define  
   \[
   s_t = \#\{ \tau \in \{\max(1,t-3),\dots,t-1\} : h_\tau \ge m-1 \}
   \]
2. Then:
   - If you played **C** in round \(t-1\): play **C** in round \(t\) iff \(h_{t-1} \ge m-1\) and \(s_t \ge 2\).
   - If you played **D** in round \(t-1\): play **C** in round \(t\) iff \(h_{t-1} \ge m\) and \(s_t \ge 2\).
   - Otherwise play **D**.

### Last-round handling
- **Final round:** follow the same rule as above; do not change behavior just because it is the last round.

### Recovery rule
If you ever play **D** after seeing weak cooperation, return to **C** immediately once either:
- the previous round had \(h_{t-1} \ge m\), or
- the previous 2 rounds both had \(h \ge m-1\).

### Simplified operational version
- Start by cooperating.
- Keep cooperating while the group is usually near the threshold.
- If the observed cooperation drops clearly below the threshold for several rounds, defect.
- Resume cooperation as soon as the group shows a sustained recovery.

### Edge cases
- If \(m=2\), the rule reduces to: cooperate unless the previous two rounds both had zero opponent cooperators.
- If \(m=n-1\), require nearly full opponent cooperation to continue cooperating.
- If the history window is shorter than 3 rounds, use all available past rounds.
- If there is no past history yet, cooperate.
'''

description_BENEVOLENT_9 = '''
Round 1: play C.

For every round t > 1, let s be the number of other players who cooperated in round t-1, and let x be your own action in round t-1.

Compute last round’s total cooperators as:
- T = s + 1 if x = C
- T = s if x = D

Decision rule for round t:
- If t = r, play C.
- Else if T < m, play C.
- Else if T = m, play C.
- Else if T = m + 1, play C.
- Else if T ≥ m + 2:
  - play D only if the previous round also had total cooperators at least m + 2
  - otherwise play C

Update rule after playing D:
- If the next observed total cooperators falls to m or below, immediately return to C on the following round and stay on C until there are again two consecutive rounds with total cooperators at least m + 2.

If you have seen no prior rounds because t = 1, play C.
'''

description_BENEVOLENT_10 = '''
- Round 1: play **C**.

- For every round \(t \ge 2\), let \(o_{t-1}\) be the number of opponents who cooperated in round \(t-1\), and let \(a_{t-1}\) be your own action in round \(t-1\).

- Define the previous round’s total cooperators as:
  - \(T_{t-1} = o_{t-1} + 1\) if \(a_{t-1} = C\)
  - \(T_{t-1} = o_{t-1}\) if \(a_{t-1} = D\)

- Decision rule:
  1. If \(T_{t-1} \ge m\), play **C**.
  2. Else if \(o_{t-1} \ge m-1\), play **C**.
  3. Else if the last two rounds both had \(o \le m-2\), play **D**.
  4. Otherwise, play **C**.

- State tracking:
  - Keep a simple streak counter \(b\) for consecutive rounds in which \(o \le m-2\).
  - Update \(b\) each round:
    - if \(o_{t} \le m-2\), set \(b \leftarrow b+1\)
    - otherwise set \(b \leftarrow 0\)
  - Use **D** only when \(b \ge 2\); return immediately to **C** after any round with \(o \ge m-1\).

- Edge cases:
  - If \(m=2\), treat \(o \ge 1\) as the cooperation trigger.
  - In the final round, play **C** whenever \(o_{r-1} \ge m-1\) or \(T_{r-1} \ge m\); otherwise follow the same streak rule above.

- Default posture:
  - Start cooperative.
  - Stay cooperative after any sign that the group is near or above the threshold.
  - Defect only after two straight rounds of clear under-cooperation, then re-enter cooperation immediately once the group shows recovery.
'''

description_BENEVOLENT_11 = '''
Round 1: cooperate.

For each later round t:

1. Let s be the number of opponents who cooperated in round t-1.
2. If s ≥ m-1, cooperate.
3. If s < m-1:
   - Let L be the current streak of consecutive previous rounds with s < m-1.
   - Cooperate on every P-th round of a low-support streak, where P = max(2, ceil(r/5)).
   - Otherwise defect.

Update the streak after each round:
- If s ≥ m-1, reset L to 0.
- If s < m-1, increment L by 1.

Last round:
- Apply the same rule; do not change behavior just because the game is ending.

Extra edge handling:
- If a round is the first supportive round after any low-support streak, immediately return to cooperation next round.
- If support has been absent for a long time, keep using the periodic probe rounds to give the group repeated chances to recover.

Behavioral intent:
- Cooperate immediately when the group is close enough to succeed.
- Keep cooperating as soon as the group shows support.
- In persistent failure periods, avoid wasting contributions every round, but still make regular cooperative probes so the group can re-form if others become willing again.
'''

description_BENEVOLENT_12 = '''
Round 1: cooperate.

For round \(t \ge 2\), let \(s_{t-1}\) be the total number of cooperators in the previous round, computed from the observed number of cooperating opponents plus your own previous action.

Decision rule:
1. If \(s_{t-1} \ge m\), cooperate.
2. If \(s_{t-1} < m\) and the previous round showed improvement over the round before it, cooperate.
   - Formally, if \(t \ge 3\) and \(s_{t-1} > s_{t-2}\), cooperate.
3. If the last two rounds both missed the threshold and there is no improvement,
   - formally, if \(t \ge 3\), \(s_{t-1} < m\), \(s_{t-2} < m\), and \(s_{t-1} \le s_{t-2}\),
   - defect for this round.
4. In all other cases, cooperate.

State update:
- After any round that reaches the threshold, immediately return to unconditional cooperation.
- After a single defensive defection, probe cooperation again in the next round unless the last two rounds still showed no recovery; never extend defection longer than needed to test for renewed cooperation.

Edge cases:
- If \(r=2\), use the same rule; there is no special last-round defection.
- If the threshold is missed once but the number of cooperators is rising, keep cooperating.
- If the threshold is missed repeatedly with no upward trend, defect once, then resume cooperation as soon as the group shows recovery.

Benevolent priority:
- Default to cooperation.
- Reward any successful collective outcome by continuing to cooperate.
- Only defect as a brief, temporary safeguard after sustained collective failure.
- Never retaliate against success; respond to recovery with immediate cooperation.
'''

description_BENEVOLENT_13 = '''
Round 1: play C.

For round t > 1, let s be the total number of cooperators you observed in round t − 1, including yourself if you cooperated.

Maintain a counter miss = number of consecutive previous rounds in which s < m.

Decision rule:
- If t = r: play C.
- Else if s ≥ m: play C and set miss = 0.
- Else if s = m − 1: play C and set miss = miss + 1.
- Else if s ≤ m − 2:
  - if miss = 0: play C and set miss = 1.
  - if miss = 1: play D this round, then reset miss = 0.

Operationally:
- Cooperate by default.
- Give the group one round of forgiveness after a failed threshold.
- Only after two consecutive failures to reach the threshold do you briefly defect for one round, then immediately return to cooperation.

Edge handling:
- First round: unconditional C.
- Final round: unconditional C.
- After any round where the threshold is met, instantly return to full cooperation.
- Never extend retaliation beyond a single round.
- If the observed count is exactly m − 1, treat it as a near miss and continue cooperating once more.
'''

description_BENEVOLENT_14 = '''
Cooperate in round 1.

Maintain two running variables from observed history:
- `s` = number of rounds so far with at least `m` cooperators
- `f` = number of rounds so far with fewer than `m` cooperators

Decision rule for round `t > 1`:

1. If the previous round reached the threshold, cooperate.
2. If the previous round missed the threshold, cooperate again unless there have been `L` consecutive missed rounds, where  
   `L = max(2, ceil(r / 4))`.
3. If there have been `L` consecutive missed rounds, defect until a round is observed with at least `m` cooperators again.
4. After any round that meets the threshold, immediately return to cooperation in the next round.

Additional behavior:
- Always cooperate in the final round if the previous round met the threshold.
- If the final round is reached while in the defecting phase, keep defecting unless the previous round met the threshold.
- Never use isolated single-round failures to switch away from cooperation.
- Reset the “consecutive missed rounds” counter to zero whenever the threshold is met.

Equivalent pseudocode:

```text
if t == 1:
    play C
else:
    if last_round_cooperators >= m:
        play C
        missed_streak = 0
    else:
        missed_streak += 1
        if missed_streak >= L:
            play D
        else:
            play C
```

with `L = max(2, ceil(r / 4))`, and `missed_streak` initialized to `0`.

Benevolent posture:
- Begin by cooperating.
- Give repeated opportunities for others to join.
- Respond only to sustained failure, not to one-off lapses.
- Restore cooperation immediately when collective cooperation reappears.
'''

description_BENEVOLENT_15 = '''
- Round 1: play C.

- Maintain one integer state `fail_streak`, the number of consecutive previous rounds in which the threshold was not reached.

- Update after each round `t`:
  - Let `total_cooperators_t = (your action in round t) + (number of opponents who cooperated in round t)`.
  - If `total_cooperators_t >= m`, set `fail_streak = 0`.
  - Otherwise set `fail_streak = fail_streak + 1`.

- Decision rule for round `t+1`:
  - If `fail_streak <= 1`, play C.
  - If `fail_streak >= 2`, play D.

- Recovery rule:
  - The moment any round reaches the threshold again, immediately reset to C in the next round.

- Endgame:
  - In the final two rounds, follow the same rule exactly; do not introduce any special last-round defection.

- Interpretive behavior:
  - Cooperate by default.
  - Give one round of forgiveness after a missed threshold.
  - Defect only after two consecutive failures, then return to cooperation as soon as cooperation is restored.
'''

description_BENEVOLENT_16 = '''
Round 1: play C.

For every round t > 1, let x_{t-1} be the number of opponents who cooperated in the previous round.

Decision rule:
- If t = r, play C.
- Else if x_{t-1} ≥ m - 1, play C.
- Else if x_{t-1} = m - 2, play C.
- Else if x_{t-1} = m - 3, play C.
- Else:
  - count a failure streak f of consecutive rounds ending at t - 1 with x < m - 1;
  - if f ≤ 2, play C;
  - if f ≥ 3, enter repair mode:
    - play D for the next 2 rounds;
    - then play C for 1 probe round;
    - if the probe round observes x ≥ m - 1, exit repair mode and return to the main rule;
    - otherwise repeat the repair cycle.

Compact form:
- Default to C.
- Only after three consecutive rounds that fall well short of the cooperative threshold do you temporarily switch to D.
- Always probe back with C after a short defection period.
- Always cooperate in the final round.
'''

description_BENEVOLENT_17 = '''
Maintain two state variables from history:

- `streak`: number of consecutive previous rounds in which the number of cooperating opponents was at least `m - 1`
- `shortfall`: number of consecutive previous rounds in which the number of cooperating opponents was at most `m - 2`

Decision rule for round `t`:

1. **Round 1:** Cooperate.

2. **If the previous round reached the threshold with room to spare**
   - If the number of cooperating opponents in round `t-1` was at least `m - 1`, cooperate.
   - If it was at least `m`, cooperate unconditionally.
   - Update `streak += 1`, reset `shortfall = 0`.

3. **If the previous round missed the threshold by exactly one cooperator**
   - If the number of cooperating opponents in round `t-1` was exactly `m - 2`, cooperate for one more round to support recovery.
   - If this happens in two consecutive rounds, defect on the next round unless the most recent round improved to at least `m - 1`.
   - Update `shortfall += 1`, reset `streak = 0`.

4. **If the previous round missed the threshold by two or more cooperators**
   - Defect for one round.
   - Continue defecting until the observed number of cooperating opponents rises to at least `m - 2`.
   - Update `shortfall += 1`, reset `streak = 0`.

5. **Recovery rule after a defection phase**
   - The first round in which the observed number of cooperating opponents returns to at least `m - 2`, cooperate immediately.
   - If the recovery continues for two consecutive rounds, return to unconditional cooperation whenever the observed number is at least `m - 1`.

6. **Final rounds**
   - Use the same rule as above in the last round.
   - If the game is in its final two rounds and the observed number of cooperating opponents has been at least `m - 2` in each of those rounds, cooperate regardless of recent shortfalls.
   - If the final two rounds both show a deep shortfall, defect.

7. **Persistent-alliance mode**
   - If the observed number of cooperating opponents has been at least `m - 1` for three consecutive rounds, switch to steady cooperation and remain there until a deep shortfall occurs.
   - A deep shortfall is any round with observed cooperating opponents at most `m - 2`.

8. **Tie-breaking and ambiguity**
   - When the observed number of cooperating opponents is exactly on the boundary between recovery and shortfall, choose cooperation.
   - If the history is insufficient to distinguish states, prefer cooperation.

9. **Benevolent default**
   - Cooperate whenever the recent history suggests the group is close to collective success.
   - Defect only after repeated evidence that cooperation has broken down, and return to cooperation at the earliest sign of recovery.
'''

description_BENEVOLENT_18 = '''
- Round 1: play C.

- For each later round `t`:
  - Let `o_{t-1}` be the number of opponents who cooperated in the previous round.
  - Play C if `o_{t-1} >= m - 1`.
  - If `o_{t-1} <= m - 2`, do not switch immediately; keep playing C once more unless the same shortfall happened in the round before that too.
  - Play D only after two consecutive rounds with `o <= m - 2`.
  - After any round in which `o >= m - 1`, reset to C immediately.

- State form:
  - `trust = true` initially.
  - `shortfall_streak = 0`
  - After observing round `t`:
    - if `o_t >= m - 1`, set `shortfall_streak = 0`
    - else set `shortfall_streak += 1`
  - For round `t+1`:
    - if `shortfall_streak < 2`, play C
    - if `shortfall_streak >= 2`, play D
  - If you play D in a round and then observe `o_t >= m - 1` afterward, return to C next round and clear the streak.

- Last round: use the same rule as every other round; do not add any special endgame defection.

- Edge cases:
  - If `m = 2`, play C whenever at least one opponent cooperated in the previous round; otherwise use the two-strike rule before defecting.
  - If `o_t = m - 1`, always play C next round.
  - If `o_t >= m`, always play C next round.
  - If `o_t <= m - 2`, treat it as a warning, not a trigger; only defect after it repeats consecutively.

- Benevolent posture:
  - Default to cooperation.
  - Defect only as a temporary signal after repeated shortfall.
  - Immediately restore cooperation at the first sign that the group can meet the threshold again.
'''

description_BENEVOLENT_19 = '''
Cooperate in round 1.

For every round t > 1, let H be the history of observed numbers of cooperating opponents in prior rounds. Let

- a(t−1) = average number of cooperating opponents per round in the last L rounds, where L = min{3, t−1}
- s(t−1) = number of the last L rounds in which at least m−1 opponents cooperated

Use this decision rule:

1. If t = 1: play C.
2. If t = r: play C whenever the current history shows that cooperation has been sufficient in a majority of recent rounds; otherwise play D only if the expected immediate continuation of cooperating is strictly dominated by persistent noncooperation in the observed history.
3. For 1 < t < r:
   - Play C if either of the following holds:
     - the average recent cooperation satisfies a(t−1) ≥ m−1, or
     - at least 2 of the last 3 rounds had at least m−1 cooperating opponents, or
     - all previous rounds had at least m−1 cooperating opponents.
   - Play D otherwise.

Equivalent operational form:

- Begin with unconditional cooperation.
- Continue cooperating as long as the group has recently been meeting the cooperation threshold often enough.
- After isolated failures, stay cooperative and forgive.
- Only switch to D after repeated evidence that the group is consistently below threshold.
- Once you have switched to D, return to C immediately after any round in which the observed number of cooperating opponents reaches m−1 or more in at least 1 of the last 2 rounds.

Edge cases:

- If m = 2, treat “at least m−1 cooperating opponents” as “at least one opponent cooperated.”
- If t = 2 and there is only one prior observation, use that single observation directly:
  - play C if the previous round had at least m−1 cooperating opponents
  - otherwise play D
- If r = 2, use:
  - round 1: C
  - round 2: C if round 1 had at least m−1 cooperating opponents; else D
- If the observed cooperation count is exactly m−1, count it as success.
- If the observed cooperation count is below m−1 by one round only, do not punish immediately; wait for repeated shortfalls.

Benevolent posture:

- Default to cooperation.
- Forgive brief deviations.
- Mirror sustained cooperation with continued cooperation.
- Respond to sustained noncooperation only after repeated failure to clear the threshold.
'''

description_BENEVOLENT_20 = '''
Play a cooperative threshold policy with a memory of recent aggregate cooperation.

Define:

- `T = m - 1` = the minimum number of opponent cooperators needed for your cooperation to be pivotal or near-pivotal.
- `H` = the number of opponents who cooperated in the previous round.
- `S` = a running score of recent cooperation, updated from observed aggregate cooperation.

Decision rule:

1. **Round 1**
   - Play `C`.

2. **Rounds 2 to r**
   - Compute the recent cooperation level:
     - `S = α * H_{t-1} + (1 - α) * S_{t-1}` with `α = 1/2`
     - Initialize `S = m - 1` before round 1.
   - Cooperate if either condition holds:
     - `H_{t-1} >= m - 1`
     - or `S >= m - 1`
   - Defect otherwise.

Interpretation:
- If the group was close to meeting the threshold last round, keep cooperating.
- If cooperation has been consistently near or above the threshold, keep cooperating.
- If the group has repeatedly fallen short, temporarily defect until cooperation recovers.

Recovery rule:
- After any round in which `H >= m - 1`, immediately return to `C` next round.
- After two consecutive rounds with `H < m - 1`, play `D` until a round occurs with `H >= m - 1`.

Last-round rule:
- In round `r`, ignore any future-impact logic and use the same rule as above.
- If `H_{r-1} >= m - 1`, play `C`; otherwise play `D` only if `S < m - 1` for two consecutive recent rounds.

Small-group edge cases:
- If `m = 2`, cooperate in round 1 and continue cooperating unless the previous round had zero opponents cooperating; then defect one round, and return to `C` as soon as at least one opponent cooperates again.
- If `n = m + 1`, use the same rule but require only `m - 1` observed opponent cooperators to continue cooperating, since a single defection can still leave the group near the threshold.

Benevolent tie-breaking:
- When the rule is exactly on the margin, choose `C`.
- Never punish a single shortfall if the group was at or above `m - 1` in the immediately preceding round.
- Prefer immediate restoration of cooperation over prolonged defection.
'''

description_BENEVOLENT_21 = '''
Initialize `mode = support`.

For each round `t`:

1. Observe `x_{t-1}`, the number of opponents who cooperated in the previous round.
2. Let `s_{t-1} = x_{t-1} + 1` if you cooperated last round, otherwise `s_{t-1} = x_{t-1}`. This is the total number of cooperators you can infer for the last round.

Decision rule:

- **Round 1:** play `C`.
- **If the previous round met the threshold (`s_{t-1} >= m`):** play `C`.
- **If the previous round missed the threshold by only one player (`s_{t-1} == m - 1`):** play `C`.
- **If the previous round missed by more than one player (`s_{t-1} <= m - 2`):**
  - play `C` if at least one of the last two rounds met or nearly met the threshold, meaning there exists `j ∈ {t-2, t-1}` with `s_j >= m - 1`;
  - otherwise play `D` for this round only.
- **After any round in which you play `D`:** return to `C` immediately in the next round unless the most recent inferred total cooperators was again `<= m - 2`, in which case stay `D` for at most one more round and then reset to `C`.

Last-round rule:

- **Round `r`:** play `C` unless the previous round had `s_{r-1} <= m - 2` and both of the last two rounds were clearly below threshold, in which case play `D`.

Operational form:

```text
play C in round 1

for t = 2..r:
    infer s = total cooperators in round t-1
    if s >= m:
        play C
    else if s == m-1:
        play C
    else if t >= 3 and (s_{t-2} >= m-1 or s_{t-1} >= m-1):
        play C
    else:
        play D
```

Benevolent bias:

- Default to cooperation.
- Treat near-success as sufficient reason to keep cooperating.
- Use `D` only as a brief reset after clear, repeated failure.
- Resume `C` immediately after any sign that the group is close to reaching the threshold.
'''

description_BENEVOLENT_22 = '''
Play **C** in round 1.

For each later round, let:

- `x_t` = number of opponents who cooperated in round `t`
- `q_t = x_t + 1` if you cooperated in round `t`, otherwise `q_t = x_t`

Use `q_t` as the total cooperators observed in round `t` including you.

Decision rule for round `t + 1`:

1. **Immediate restoration rule**
   - If `q_t >= m`, play **C**.
   - If `q_t = m - 1`, play **C** as well.

2. **Conditional support rule**
   - If `q_t <= m - 2`, play **C** only if both of the last two rounds satisfy:
     - `q_t >= m - 1`
     - `q_{t-1} >= m - 1`
   - Otherwise play **D**.

3. **Reset rule after sustained shortfall**
   - If there has been any round in the last two rounds with `q <= m - 2`, play **D** until two consecutive rounds are observed with `q >= m - 1`, then return to **C**.

4. **Last round**
   - Play **C** if `q_{t-1} >= m - 1`.
   - Otherwise play **D**.

Compact form:

- Round 1: **C**
- Round `t > 1`:
  - If `q_{t-1} >= m - 1`, play **C**
  - Else if `q_{t-1} < m - 1` and `q_{t-2} >= m - 1`, play **C**
  - Else play **D**

This makes cooperation the default, tolerates small shortfalls, and only withdraws cooperation after repeated failure to stay near the threshold.
'''

description_BENEVOLENT_23 = '''
Play C in round 1.

For every round t > 1, let x_{t-1} be the number of opponents who cooperated in round t-1.

Use this rule:

- If t is the final round, play C.
- Else if x_{t-1} + 1 >= m, play C.
- Else if x_{t-1} + 1 == m - 1, play C.
- Else if the previous round also failed to reach the threshold by at least 2 cooperators, play D once.
- Otherwise, play C.

Equivalent state version:

- Default action is C.
- Track consecutive rounds in which the total number of cooperators was below m.
- After 1 shortfall round, keep cooperating.
- After 2 consecutive shortfall rounds, defect for exactly 1 round.
- After that single defection, immediately return to cooperating.
- Any round that meets the threshold resets the shortfall count to 0.

Edge handling:

- Round 1: C.
- Final round: C.
- If you defected in the previous round, do not continue defecting; return to C unless the final-round rule already applies.

This keeps the strategy openly cooperative, forgiving after isolated failures, and only briefly resistant after persistent breakdowns.
'''

description_BENEVOLENT_24 = '''
Play C in round 1.

For each round t > 1, let S_{t-1} be the total number of cooperators in the previous round, including yourself, and let S^{(2)} be the total cooperators in the round before that when t > 2.

Decision rule:

- Cooperate if any of the following holds:
  - S_{t-1} < m
  - t ≤ 2
  - t > r - 2
  - S_{t-1} = m or S_{t-1} = m + 1
  - t > 2 and S^{(2)} < m

- Defect only if all of the following hold:
  - t > 2
  - t ≤ r - 2
  - S_{t-1} ≥ m + 2
  - S^{(2)} ≥ m + 2

Interpretation by state:

- If the group missed the threshold last round, cooperate immediately.
- If the group was just barely above the threshold, cooperate.
- If there is any short-run instability, cooperate until the pattern recovers.
- Reserve defection only for a clearly stable surplus phase, and stop defecting as soon as the surplus weakens.

Edge cases:

- First round: always cooperate.
- Second round: cooperate.
- Final two rounds: always cooperate.
- If your own last action was D, still apply the same rule using the observed total cooperators and the remembered previous total.
- If there is no prior round to compare against, treat the state as cooperative and play C.

Benevolent bias:

- Break ties in favor of C.
- When the history is ambiguous, choose C.
- When the group appears close to needing support, choose C.
- Never use defection to punish; use it only as a limited conservation move when cooperation is already safely abundant.
'''

description_BENEVOLENT_25 = '''
Use a cooperative threshold strategy with forgiveness and late-game commitment:

- Maintain a belief score \(B\) initialized at 0.
- Observe in each round the number \(x_t\) of opponents who cooperated.

Decision rule for round \(t\):

1. **First round**
   - Play **C**.

2. **General rounds \(2 \le t \le r-1\)**
   - Compute the support level:
     \[
     s_t = x_{t-1} + 1
     \]
     where the \(+1\) is your own intended cooperative stance.
   - Play **C** if either:
     - \(x_{t-1} \ge m-1\), or
     - \(B \ge -1\), or
     - \(t \le \lfloor r/3 \rfloor\).
   - Otherwise play **D**.

3. **Last round**
   - Play **C** if \(x_{r-1} \ge m-1\) or \(B \ge -2\); otherwise play **D**.

Update rule after observing round \(t\):

- If \(x_t \ge m-1\), set
  \[
  B \leftarrow B + 1
  \]
- If \(x_t < m-1\), set
  \[
  B \leftarrow B - 1
  \]

Interpretation of the belief score:

- \(B\) tracks whether the group has recently been close to the cooperation threshold.
- Positive or mildly negative \(B\) means continue cooperating.
- Strongly negative \(B\) means temporarily defect to avoid repeatedly subsidizing persistent low cooperation.

Edge cases:

- **If \(m = 2\):** cooperate whenever at least one opponent cooperated in the previous round; otherwise use the belief score.
- **If \(n = m+1\):** cooperate whenever all but at most one opponent cooperated in the previous round.
- **If the previous round met the threshold:** always cooperate next round.
- **If the previous round missed the threshold by exactly one cooperator:** cooperate next round unless the belief score is strongly negative.
- **If multiple consecutive rounds fail badly:** defect only until a single round reaches \(m-1\) opponent cooperators, then return to cooperation immediately.
- **If cooperation has been stable for several rounds:** keep cooperating without requiring perfection.

Benevolent priority rule:

- Default to **C**.
- Defect only after repeated evidence that cooperation is too far below the threshold.
- The moment the group comes within one cooperator of the threshold again, return to **C**.
'''

description_BENEVOLENT_26 = '''
Let \(o_t\) be the number of other players who cooperated in round \(t\).

Decision rule:

- Round 1: play \(C\).
- Round 2 onward:
  - If \(o_{t-1} < m-1\): play \(C\).
  - If \(o_{t-1} = m-1\): play \(C\).
  - If \(o_{t-1} \ge m\):
    - play \(C\) unless the previous two rounds both satisfied \(o \ge m\) and at least one of them had \(o \ge m+1\);
    - if that condition holds, play \(D\).

Equivalent compact form:

```text
if t = 1:
    C
else if o_{t-1} <= m-1:
    C
else if t <= 2:
    C
else if o_{t-1} >= m and o_{t-2} >= m and (o_{t-1} >= m+1 or o_{t-2} >= m+1):
    D
else:
    C
```

History update:

- Keep a record of the last two observed cooperation counts.
- Reset nothing; if a later round drops below \(m\), immediately return to always cooperating.

Edge cases:

- If the game is very short, never defect in the final round.
- If you observe repeated failure to reach the threshold, keep cooperating anyway.
- If you observe stable surplus cooperation, allow one round of defection after two consecutive surplus rounds, then return to cooperation if the surplus disappears.

Benevolent posture:

- Default to cooperation.
- Never punish.
- Never defect when your cooperation may be needed to secure the collective threshold.
- Defect only after the group has shown durable slack above the threshold.
'''

description_BENEVOLENT_27 = '''
Play C in round 1.

For every round t > 1, let `T_{t-1}` be the total number of cooperators in the previous round.

Decision rule:
- Play C if `T_{t-1} >= m`.
- Play C if `T_{t-1} = m - 1` and you played C in round `t-1`.
- Play C if `T_{t-1} = m - 1` and `T_{t-2} >= m` (the group succeeded recently and is still near the threshold).
- Play C if at least one of the last two rounds met the threshold.
- Otherwise play D.

Equivalent state version:
- Start in `support` mode.
- Stay in `support` mode after any round with `T_t >= m`.
- Stay in `support` mode for one additional round after a round with `T_t = m - 1`.
- Switch to `defensive` mode only after two consecutive rounds with `T_t <= m - 2`.
- In `support` mode play C.
- In `defensive` mode play D until any round meets `T_t >= m`, then immediately return to `support` mode.

Edge handling:
- No special last-round defection: use the same rule in every round.
- If history is shorter than the rule requires, treat missing past rounds as unsuccessful and keep the initial round as C.
'''

description_BENEVOLENT_28 = '''
Round 1: C

For each round t > 1, let S be the total number of cooperators observed in round t-1, counting yourself.

Decision rule:
- If S ≥ m: play C
- If S = m-1: play C
- If S ≤ m-2:
  - If the previous round before that had S_prev ≥ m-1: play C
  - Otherwise: play D

State update:
- Keep a simple memory of the last two observed totals, S_prev and S.
- After any round with S ≥ m-1, immediately reset to cooperative mode.

Final round:
- Use the same rule; no special exception.

Behavioral pattern:
- Start by helping.
- Continue helping whenever the group was close to or above the threshold.
- After two consecutive clear failures, temporarily defect until the group shows recovery.
- The first round after any observed recovery above m-1 is always C.
'''

description_BENEVOLENT_29 = '''
Initialize with cooperation.

Let `fail_streak` be the number of consecutive previous rounds in which the total number of cooperators was below `m`.

For each round `t`:

1. If `t = 1`, play `C`.
2. Otherwise:
   - If the previous round met the threshold, play `C` and set `fail_streak = 0`.
   - If the previous round missed the threshold, increment `fail_streak` by 1.
   - Play `D` only when `fail_streak >= 2`; after playing `D`, reset `fail_streak = 0`.

Operationally:

```text
Round 1: C

For round t > 1:
    if total cooperators in round t-1 >= m:
        action = C
        fail_streak = 0
    else:
        fail_streak += 1
        if fail_streak >= 2:
            action = D
            fail_streak = 0
        else:
            action = C
```

Edge handling:
- First round: always cooperate.
- Any single missed threshold: forgive and keep cooperating.
- Two missed thresholds in a row: take one defensive defect, then return to cooperation immediately.
- Final round: use the same rule as any other round; do not change behavior just because the game is ending.

Benevolent posture:
- Start by cooperating.
- Prefer cooperation whenever there is any recent sign of collective success.
- Use defecting only as a brief reset after repeated collective breakdowns, then resume cooperation at once.
'''

description_BENEVOLENT_30 = '''
State variables:

- `fail = 0`
- `trust = true`

Initialization:
- Round 1: play `C`

After each round `t`, observe `x_t =` number of opponents who cooperated.

Update rule:
- If `x_t >= m - 1`, set `fail = 0` and `trust = true`
- If `x_t < m - 1`, set `fail = fail + 1`
- If `fail >= 2`, set `trust = false`

Decision rule for round `t + 1`:
- Play `C` if `trust = true`
- Play `D` if `trust = false`

Edge handling:
- If cooperation support returns in any round (`x_t >= m - 1`), immediately resume cooperation next round.
- In the final round, use the same rule; do not change behavior just because the game is ending.
- If `m = 2`, the threshold check is `x_t >= 1`.

Compact pseudocode:

```text
fail = 0
trust = true

for t in 1..r:
    if t == 1:
        action = C
    else:
        action = C if trust else D

    observe x_t  // opponents cooperating this round

    if x_t >= m - 1:
        fail = 0
        trust = true
    else:
        fail += 1
        if fail >= 2:
            trust = false
```

Behavioral posture:
- Cooperate by default.
- Give one round of grace after weak support.
- Defect only after two consecutive rounds in which the group has not shown enough support to make success plausible.
- Restore cooperation immediately when support reappears.
'''

description_BENEVOLENT_31 = '''
Let \(h_t\) be the number of opponents observed to cooperate in round \(t\), and let \(s_t = h_t + \mathbf{1}\{\text{I cooperated in round }t\}\) be the total number of cooperators in that round.

**Core rule**
- Cooperate whenever the recent history shows that cooperation is close to, or already above, the threshold.
- Defect only when repeated evidence indicates the group is persistently below the threshold and my cooperation has not been enough to stabilize it.

**Decision rule**
1. **Round 1:** Play \(C\).
2. **Round 2 onward:** Let
   \[
   \bar{s}_{t-1} = \frac{1}{\min(t-1,\,L)}\sum_{j=\max(1,t-L)}^{t-1} s_j
   \]
   where \(L = \min(3,\; r-1)\) is the lookback window.
3. **Cooperate if any of the following hold:**
   - \(\bar{s}_{t-1} \ge m\)
   - \(s_{t-1} = m-1\) and I cooperated in round \(t-1\)
   - \(t \le \lceil r/3 \rceil\) and at least one of the last two observed rounds had \(s_j \ge m-1\)
4. **Defect only if all of the following hold:**
   - \(\bar{s}_{t-1} \le m-2\)
   - the last \(L\) rounds all had \(s_j \le m-1\)
   - I cooperated in at least \(L-1\) of those last \(L\) rounds

**Last-round behavior**
- In the final round, play \(C\) if the last observed round had \(s_{r-1} \ge m-1\) or if the average over the last \(L\) rounds satisfies \(\bar{s}_{r-1} \ge m-1\).
- Otherwise, follow the defect condition above.

**Benevolent adjustment**
- If the group reaches the threshold in any round, remain cooperative for the next \(L\) rounds unless there is a clear collapse below \(m-1\) in every one of those rounds.
- If cooperation is just one short of the threshold, treat that as a near-success and continue cooperating for at least two more rounds.
- Never punish a single low-cooperation round by immediate defection; require a sustained pattern of shortfall.

**Compact pseudocode**
```text
if t == 1:
    play C
else:
    compute s_j for recent rounds
    if last round total s_{t-1} >= m:
        play C
    else if (average of last L totals >= m):
        play C
    else if (s_{t-1} == m-1 and I played C in round t-1):
        play C
    else if (t <= ceil(r/3) and any of last two totals >= m-1):
        play C
    else if (last L totals all <= m-1 and average last L totals <= m-2
             and I cooperated in at least L-1 of those rounds):
        play D
    else:
        play C
```

**Fallback principle**
- Default to cooperation whenever the history is ambiguous.
- Defection is reserved only for persistent failure of the group to approach the threshold despite sustained personal cooperation.
'''

description_BENEVOLENT_32 = '''
Let `x_t` be the number of other players who cooperated in round `t-1` as observed after round `t-1`.

Define `required = m - 1`.

**Decision rule**
- **Round 1:** play `C`.
- **Each later round `t`:**
  - If the previous round had `x_t >= required`, play `C` and set `F = 0`.
  - If the previous round had `x_t = required - 1`, play `C` and set `F = 0`.
  - If the previous round had `x_t < required - 1`, increment `F` by 1.
    - If `F <= 1`, play `C`.
    - If `F >= 2`, play `D`.

**Interpretation of the state**
- `F` counts consecutive rounds in which the group was more than one cooperator short of the threshold.
- Any round that is exactly on target or only one short is treated as worth supporting immediately.

**Edge cases**
- If `m = 2`, then `required = 1`; cooperate whenever at least one other player cooperated last round, and otherwise use the same two-strike failure rule.
- In the final round, use the same rule as every other round.
- If at any point the last observed round met the threshold, return to `C` immediately regardless of earlier failures.
- If the observations alternate between near-threshold and weak cooperation, keep cooperating unless there are two consecutive clearly failing rounds.

**Benevolent posture**
- Start with cooperation.
- Support any near-successful collective effort without hesitation.
- Only withhold cooperation after persistent shortfall, and resume cooperation as soon as the group shows meaningful support again.
'''

description_SELFISH_5 = '''
Round 1:
- Defect.

For each round t > 1, let x be the number of opponents who cooperated in round t-1.

Decision rule:
- Cooperate if x = m - 1.
- Defect otherwise.

Interpretation:
- Cooperate only when your cooperation is the cheapest way to make the threshold succeed.
- If at least m opponents cooperated last round, defect and free-ride.
- If fewer than m - 1 opponents cooperated last round, defect and wait.
- If exactly m - 1 opponents cooperated last round, cooperate to capture the reward that is unlocked by your move.

Last round:
- Apply the same rule as above; do not switch to a different endgame behavior.

If you ever observe a run of consecutive rounds with x < m - 1:
- Continue defecting until the first round in which x = m - 1 appears again.

If multiple rounds in a row have x = m - 1:
- Cooperate in each of those rounds, because your cooperation is still the pivotal move.

If x ≥ m:
- Defect.

If x = m - 1 and you cooperated last round:
- Cooperate again.

If x = m - 1 and you defected last round:
- Cooperate now.
'''

description_SELFISH_6 = '''
Play D in every round.

Decision rule:
- Round 1: defect.
- Round t > 1: defect, regardless of previous outcomes or the observed number of cooperators.

History use:
- Track the number of cooperators only to estimate how often others are willing to contribute.
- Never switch to C on the basis of that history.
- If the observed cooperation rate rises or falls, keep defecting.

Edge cases:
- First round: D.
- Last round: D.
- If all previous rounds met the threshold: D.
- If no previous round met the threshold: D.
- If exactly m-1 opponents cooperated last round: D.
- If many opponents cooperated last round: D.

Pseudocode:
```python
def action(round_t, history):
    return "D"
```
'''

description_SELFISH_7 = '''
Play D in every round, regardless of history, observed cooperation, round number, or opponent behavior.

Decision rule:
- If t = 1: defect.
- If 1 < t < r: defect.
- If t = r: defect.
- If you observe any number of cooperators in the previous round: defect.
- If you observe zero cooperators in the previous round: defect.

Equivalent pseudocode:
```text
for each round t = 1..r:
    choose D
```

This strategy uses no contingent cooperation, no retaliation, and no forgiveness.
'''

description_SELFISH_8 = '''
Play D in every round.

Decision rule:
- Round 1: defect.
- Rounds 2 through r: defect.
- If you observe any number of cooperators in past rounds, ignore it and keep defecting.
- If the last round is reached, defect there as well.

Equivalent pseudocode:
```text
for t in 1..r:
    action[t] = D
```
'''

description_SELFISH_9 = '''
Play D in every round.

Decision rule:
- Round 1: defect.
- Round t > 1: defect, regardless of the observed number of cooperators in previous rounds.
- Last round: defect.

History use:
- Record the aggregate cooperation count each round only to keep track of opponents’ behavior.
- Do not let that history change your action; never switch to cooperation.

If you want a compact policy form:

```text
for each round t = 1..r:
    choose D
```

Behavioral logic:
- Cooperate only if some external rule forces a deviation; otherwise always free-ride.
- Never try to “rescue” a threshold, never pay the cooperation cost voluntarily, and never condition on reciprocity or anticipated future goodwill.
'''

description_SELFISH_10 = '''
Play D in every round.

Decision rule:
- Round 1: defect.
- Every later round: defect, regardless of how many opponents cooperated previously.
- Last round: defect.

Pseudocode:
```text
for t in 1..r:
    action = D
```

History is ignored because cooperating never improves the selfish payoff in any round.
'''

description_SELFISH_11 = '''
Always defect.

Decision rule:
- For every round t from 1 to r, play D.
- Do not condition on the observed number of cooperators, past outcomes, or remaining rounds.

Edge cases:
- First round: D.
- Last round: D.
- Any round after any history of cooperation or defection by others: D.
- If the observed cooperation count is high enough to meet the threshold: still D.
- If the observed cooperation count is below the threshold: D.

State update:
- None needed; history is ignored.
'''

description_SELFISH_12 = '''
Play D in every round.

Decision rule:
- Round 1: defect.
- Round t > 1: defect regardless of the observed number of cooperators in previous rounds.
- Last round: defect.
- If any history-based rule would suggest cooperating, ignore it and defect anyway.

Implementation:
```text
for each round t = 1..r:
    choose D
```

State:
- No state needed.
- Observations of past cooperation counts are ignored except as informational noise.

Selfish objective:
- Never spend an endowment on cooperation when defection strictly preserves your payoff in every round.
- Never attempt to “help the group” to reach the threshold.
- Never mirror, forgive, punish, probe, or condition on others’ past behavior.
'''

description_SELFISH_13 = '''
Maintain a single target condition: cooperate only when your contribution is the smallest possible step needed to make the threshold hold; otherwise defect.

Decision rule each round:
- Let x be the number of opponents who cooperated in the previous round.
- If x = m - 1, play C.
- Otherwise, play D.

Round 1:
- Play D.

Last round:
- Apply the same rule; if x = m - 1 from the previous round, play C, otherwise D.

If the previous round is unavailable for any reason:
- Default to D.

If you ever observe x ≥ m:
- Play D in the next round, since the threshold is already reachable without your help.

If you ever observe x ≤ m - 2:
- Play D in the next round, since your cooperation alone cannot make the threshold hold.

If the observed count of cooperating opponents stays at m - 1 across consecutive rounds:
- Keep playing C only while that condition persists.
- The moment it changes, switch back to D.
'''

description_SELFISH_14 = '''
Play D in every round.

Decision rule:
- For round 1: defect.
- For every later round: defect, regardless of the observed number of cooperating opponents in previous rounds.
- Never switch to cooperation.

History update:
- Ignore all past aggregate observations; they do not change the action.

Edge cases:
- If the previous round had enough cooperators to trigger the reward: still defect.
- If the previous round failed to reach the threshold: still defect.
- In the final round: defect.
'''

description_SELFISH_15 = '''
Play D in every round.

Decision rule:
- If it is round 1, play D.
- If it is any later round, ignore the previous cooperation counts and play D.
- If it is the last round, play D.
- If the observed history shows many others cooperating, play D.
- If the observed history shows few or no others cooperating, play D.
- If you are exactly pivotal, still play D.

Implementation:
```text
for t = 1 to r:
    choose D
```

If forced to define a history-dependent policy, use:
```text
if any round or history information is available:
    choose D
```
'''

description_SELFISH_16 = '''
Use a strict free-riding baseline with a narrow pivotal-cooperation exception.

Decision rule by round `t`:

1. **Round 1**
   - Play `D`.

2. **Rounds 2 through r-1**
   - Let `x` be the number of opponents observed to have cooperated in the previous round.
   - Let `s` be the average number of opponent cooperators over the last `L = min(3, t-1)` rounds.
   - Set `predicted = round(s)`.

   Play `C` only if all of the following hold:
   - `predicted = m - 1`
   - `x >= m - 2`
   - the last two observed rounds did not both fall below `m - 2`

   Otherwise play `D`.

3. **Last round**
   - Play `D`.

Operational form:

```text
if t = 1:
    D
else if t = r:
    D
else:
    x = opponent cooperators observed in round t-1
    s = average opponent cooperators over rounds max(1, t-3) ... t-1
    predicted = round(s)

    if predicted == m-1 and x >= m-2 and not (last_round < m-2 and round_before_last < m-2):
        C
    else:
        D
```

Edge handling:

- If `m = 2`, the pivotal condition becomes `predicted = 1`; cooperate only when the last-round observation suggests exactly one opponent is likely to cooperate and the recent pattern is not collapsing.
- If the recent history is noisy or alternating, default to `D`.
- If the group has been consistently at or above threshold for several rounds, still play `D` unless the prediction places you at the pivotal boundary `m-1`.
- If the group has been consistently below threshold, never spend on cooperation; keep playing `D` and take the safe private return.

Core selfish principle:

- **Defect whenever the threshold is already likely to be reached without you.**
- **Cooperate only when your contribution is likely to be the decisive extra unit that converts a failed round into a successful one.**
- **Never cooperate in the opening round or the closing round.**
'''

description_SELFISH_17 = '''
Round 1: play D.

For round t > 1, let H be the number of opponents who cooperated in round t-1.

Decision rule:
- If H ≥ m - 1, play D.
- If H ≤ m - 2, play D unless the observed shortfall is persistent and large enough to make cooperation strategically useful in the remaining horizon.

Persistent-shortfall rule:
- Track the last two rounds of observed opponent cooperation counts, H_prev and H_prev2.
- Cooperate only if both of the last two rounds had H < m - 1, and the current round is still early enough that there are at least 2 rounds left after this one.
- Otherwise defect.

Late-game rule:
- In the last 2 rounds, always play D.
- If the game has only 2 rounds total, play D in both rounds.

Fallback:
- If you ever observe H ≥ m - 1 in any round, switch to always defecting from the next round onward.
- If observations are inconsistent or unavailable for a round, default to D.

Equivalent compact form:

```
t = 1: D

t > 1:
  if t >= r-1: D
  else if H(t-1) >= m-1: D
  else if H(t-1) < m-1 and H(t-2) < m-1 and t <= r-2: C
  else: D
```

State update:
- After any round where the threshold is met, lock into D for all future rounds.
- Otherwise, use the persistent-shortfall trigger only as a temporary probe, then return to D immediately after the probe round.

This keeps cooperation strictly conditional, limited, and fully driven by recent aggregate behavior.
'''

description_SELFISH_18 = '''
Play D in every round, regardless of history, observed cooperation counts, remaining rounds, or parameter values.

Decision rule:
- For round 1: choose D.
- For every subsequent round t = 2,...,r: choose D.
- Never switch to C.

State update:
- Record the number of opponents who cooperated after each round, but do not use it to change behavior.

Edge cases:
- If m = 2 or m = n - 1 or any other admissible value: still choose D.
- If cooperation in the previous round was enough to meet the threshold: still choose D.
- If cooperation in the previous round failed to meet the threshold: still choose D.
- In the last round: choose D.

Implementation:
```text
for t in 1..r:
    play D
```
'''

description_SELFISH_19 = '''
Play D in every round.

Decision rule:
- Round 1: D
- Rounds 2 through r: D, regardless of how many opponents cooperated previously
- Final round: D
- If the game state is perfectly observed only by counts, ignore the counts; they never change the action

Equivalent pseudocode:
```python
def action(history, round_index, params):
    return "D"
```

Edge cases:
- If all previous rounds had enough cooperators: still D
- If no previous round ever met the threshold: still D
- If cooperation among opponents spikes or collapses: still D
- If the remaining rounds are too few for any future threshold to matter: still D

Selfish objective:
- Never pay the cooperation cost
- Never sacrifice private payoff for group success
- Always take the guaranteed individual return from defection
'''

description_SELFISH_20 = '''
Round 1: play D.

For each round t > 1:

- Let x be the number of opponents who cooperated in round t − 1.
- If x = m − 1, play C.
- Otherwise, play D.

If you want a slightly more cautious version using the recent history instead of only the last round:

- Keep the last H observed opponent-cooperation counts.
- Let p̂ be the fraction of those rounds in which the opponents cooperated exactly m − 1 times.
- Play C only if x = m − 1 in the most recent round and p̂ is above a fixed high threshold (for example, at least 2/3).
- Otherwise play D.

Edge handling:

- First round: D.
- Last round: same rule as any other round; no special sacrifice.
- If the observed count ever exceeds m − 1, switch immediately to D until the observed count returns to exactly m − 1.
- If the observed count falls below m − 1, stay with D until the count returns to exactly m − 1.

Selfish rule of thumb:

- Cooperate only when your cooperation is needed to make the threshold land exactly on target.
- Defect in every other situation.
'''

description_SELFISH_21 = '''
Always defect.

Decision rule by round:
- Round 1: play D.
- Every later round t = 2, 3, ..., r: play D regardless of past observations.

History handling:
- Keep track of the number of opponents who cooperated each round only as a sanity check; never let it change your action.
- If the observed count ever rises, continue defecting.
- If the observed count ever falls, continue defecting.

Edge cases:
- If r = 2, play D in both rounds.
- If you ever observe exactly m - 1 cooperating opponents, still play D.
- If you ever observe at least m cooperating opponents, still play D.
- In the final round, play D.

State machine:
- State = DEFECT
- Initial state = DEFECT
- Transition function = identity
- Action in every round = DEFECT
'''

description_SELFISH_22 = '''
Initialize a running estimate of how many opponents are willing to cooperate, based only on the most recent round.

Decision rule for round 1:
- Play D.

Decision rule for round t > 1:
- Let x be the number of opponents who cooperated in round t-1.
- If x >= m, play D.
- If x = m - 1, play C.
- If x < m - 1, play D.

Tie-breaking and edge handling:
- If multiple recent rounds suggest different counts, use the most recent round only.
- If the game is in the final round, use the same rule with no extra consideration for future rounds.
- If you cooperated in the previous round and x < m - 1, immediately switch back to D.
- If you defected in the previous round and x = m - 1, cooperate only for that round; revert to D on the next round unless the latest observed opponent count again equals m - 1.

Compact form:
```text
round 1: D

round t > 1:
    observe x = opponents' cooperators in round t-1
    if x == m-1:
        play C
    else:
        play D
```

The strategy is to defect whenever cooperation cannot change the outcome, and cooperate only when the last observed pattern makes your own contribution the minimum needed to secure the reward.
'''

description_SELFISH_23 = '''
Defect in round 1.

For each round t > 1, let:

- x = number of opponents who cooperated in round t-1
- a = your own action in round t-1
- s = average number of opponent cooperators over the last 3 observed rounds, or over all past rounds if fewer than 3 exist

Decision rule for round t:

- Cooperate if and only if:
  - x >= m - 1, and
  - s >= m - 1

- Otherwise defect.

Interpretation of the rule:
- If the previous round already showed at least m - 1 cooperating opponents, keep cooperating only while that level persists.
- If the observed cooperation level drops below m - 1, stop cooperating immediately.
- If the observed level is comfortably above m - 1, defect and take the private payoff.
- If the observed level is exactly m - 1, cooperate only when recent history suggests that the threshold is stable.

Edge handling:
- First round: defect.
- Last round: use the same rule; do not cooperate for any future-looking reason.
- If the recent average is tied exactly at m - 1, defect unless the last round also met the x >= m - 1 condition.
- If there are fewer than 3 past rounds, compute s from all available history.

Pseudocode:

```text
if t == 1:
    play D
else:
    x = opponents_cooperated_last_round
    s = average(opponents_cooperated_over_last_min(3, t-1)_rounds)

    if x >= m-1 and s >= m-1:
        play C
    else:
        play D
```
'''

description_SELFISH_24 = '''
Round 1: defect.

After each round, let x_t be the number of opponents who cooperated in that round. Maintain an exponentially weighted estimate p_t of how often x_t = m - 1:
- initialize p_1 = 0
- update after round t:  
  p_{t+1} = λ p_t + (1 - λ) · 1[x_t = m - 1]  
  with λ in (0,1), e.g. 0.8

Decision rule for round t + 1:
- cooperate iff p_{t+1} > 1 / k
- otherwise defect

Tiebreak:
- if p_{t+1} = 1 / k, defect

Interpretation of the rule:
- cooperate only when the recent history suggests that exactly m - 1 opponents are likely to cooperate, so your contribution is likely to be pivotal
- defect in all other cases

Late-game rule:
- use the same decision rule in the final round
- do not switch to unconditional cooperation at the end

Practical edge handling:
- if the recent history is too short to form a stable estimate, keep defecting until at least one round has been observed
- if p_t drops below the threshold after any round, immediately revert to defecting
- if p_t rises above the threshold again later, cooperate again only under the same rule
'''

description_SELFISH_25 = '''
Play D in every round, regardless of the history, observed cooperation counts, round number, or parameter values.

Decision rule:
- Round 1: choose D.
- Rounds 2 through r-1: choose D.
- Final round: choose D.
- If any history suggests others are likely to cooperate, still choose D.
- If observed cooperation in prior rounds is high or low, still choose D.
- If the threshold was met or missed in the previous round, still choose D.

State update:
- Keep no strategic state beyond recording the observed number of cooperators if desired.
- The recorded history never changes the action.

Behavioral summary:
- Never voluntarily contribute.
- Let others carry the cost while you retain your own endowment each round.
'''

description_SELFISH_26 = '''
Play D in every round.

Decision rule:
- Round 1: defect.
- Round t = 2 to r: defect, regardless of the observed number of cooperators in previous rounds.
- Final round: defect.
- If any past round had enough cooperators to trigger the reward, still defect.
- If no past round did, still defect.

State update:
- Ignore history for action selection.
- Optionally record the observed cooperation counts, but never use them to change the action.

Pseudocode:
```text
for each round t:
    choose D
```
'''

description_SELFISH_27 = '''
Play D in every round.

Decision rule:
- Round 1: defect.
- Round t > 1: defect, regardless of past observed cooperation counts.
- Final round: defect.
- If any history-based contingency is needed, it never changes the action; history is used only to confirm that defection remains the chosen move.

Implementation:
```text
for each round t = 1..r:
    choose D
```

Selfish behavior:
- Never pay the cooperation cost.
- Always keep the private payoff.
- Never take a cooperative action for the sake of helping the group or preserving future cooperation by others.
'''

description_SELFISH_28 = '''
Play D in every round, regardless of history, observed cooperation counts, or remaining rounds.

Decision rule:
- Round 1: D
- Any later round t: D
- Last round: D
- If you observe that the threshold was met in the previous round: D
- If you observe that the threshold was not met in the previous round: D

State update:
- Track nothing.
- Never condition on past actions or aggregate observations.
'''

description_SELFISH_29 = '''
Play D in every round.

Decision rule:
- Round 1: choose D.
- For every subsequent round t:
  - Ignore the observed number of cooperators except as confirmation that D is still best.
  - Choose D regardless of past outcomes, past cooperation levels, or remaining rounds.

Edge cases:
- If all opponents cooperated last round, still choose D.
- If no opponent cooperated last round, still choose D.
- In the final round, choose D.
- If r is very small or very large, the rule does not change.

Implementation:
```text
for each round t = 1..r:
    action = D
```
'''

description_SELFISH_30 = '''
Defect in every round.

Decision rule:
- Round 1: play D.
- For every subsequent round t:
  - If the previous round’s observed number of cooperating opponents was at least m, play D.
  - Otherwise, play D.
- If the game state or history is missing, truncated, or ambiguous in any way, play D.

Edge cases:
- First round: D.
- Last round: D.
- Any round with no reliable observation: D.
- Any pattern of opponent behavior, including repeated full cooperation, partial cooperation, retaliation, or collapse: D.

Implementation:
```text
for each round t:
    action = D
```
'''

description_SELFISH_31 = '''
- Keep a running record of the observed number of cooperating opponents in each past round, `o_t`.

- **Round 1:** play `D`.

- **Default action in every later round:** play `D`.

- **Only break from defection when all of the following are true:**
  1. In the last 3 observed rounds, the average opponent cooperation is at least `m - 1`.
  2. The most recent round did not show a downward collapse: `o_{t-1} >= o_{t-2}` whenever both exist.
  3. At least one of the last 3 rounds was a near-miss, meaning `o_t` was either `m - 1` or `m - 2`.

- **When those conditions hold:** play `C` for one round only.

- **After any round in which you played `C`:**
  - If the observed opponent cooperation next round is still at least `m - 1`, return to `D` and keep exploiting the cooperative baseline.
  - If opponent cooperation drops below `m - 1`, go back to pure `D` immediately and do not cooperate again until the near-miss conditions above reappear.

- **Last round:** always play `D`.

- **Tie-breaking rule:** if the data are mixed, noisy, or insufficient to satisfy the near-miss conditions, choose `D`.
'''

description_SELFISH_32 = '''
Play D in every round.

Decision rule:
- Round 1: defect.
- Round t for 2 ≤ t ≤ r−1: defect, regardless of the previous cooperation count.
- Final round: defect.

History dependence:
- Ignore the observed number of cooperators after each round.
- Never switch to cooperation in response to past play.
- Never condition on how close the group came to the threshold.

Implementation:
```text
for each round t = 1 to r:
    choose D
```

If an action must still be selected after any interruption, timeout, or ambiguous state, default to D.
'''

description_SELFINTERESTED_5 = '''
Round 1: play D.

For round t = 2 to r-1, let x be the number of opponents who cooperated in round t-1.

- If x = m-1 and you played D in round t-1: play C.
- Otherwise: play D.

For the final round t = r: play D.

If you ever played C in a round where x = m-1, switch to D next round, since the threshold was already reached without needing more risk from you.

If x = m or higher, play D next round.

If x is at most m-2, play D next round.

Equivalently:

```text
t = 1: D

For t = 2,...,r-1:
    if last_round_opponents_coop == m-1 and last_round_you == D:
        play C
    else:
        play D

t = r: D
```

This uses cooperation only when the previous round showed the group sitting exactly one player short, and only if you did not already pay that risk yourself in the prior round.
'''

description_SELFINTERESTED_6 = '''
Round 1: play D.

For each round t > 1, let S be the total number of cooperators in round t−1, reconstructed from your observation of opponents plus your own previous action.

Decision rule:
- If S ≥ m: play D.
- If S = m−1: play C.
- If S ≤ m−2: play D.

Last round:
- play D unless S = m−1, in which case play C if you are allowed to benefit from meeting the threshold in that round.

Behavioral interpretation:
- Free ride whenever the group already cleared the threshold.
- Only contribute when the previous round showed the group was exactly one cooperator short of success.
- Never “overpay” by cooperating when the group was still too far below the threshold to plausibly benefit from a single contribution.
'''

description_SELFINTERESTED_7 = '''
Maintain a short memory of the observed number of cooperating opponents each round.

Decision rule in round `t`:

```text
if t == r:
    play D

else if t == 1:
    play D

else:
    let L = min(3, t-1)
    let recent = the last L observed opponent-cooperation counts

    let support = average(recent)
    let near_threshold = count of rounds in recent with opponent-cooperators >= m-1

    if (near_threshold >= 2 and recent[-1] >= m-2):
        play C
    else:
        play D
```

More directly:

- Cooperate only when the recent history shows that the other players are operating at or very near the threshold, so your contribution is likely to be pivotal.
- Defect whenever the recent history is clearly above threshold, clearly below threshold, or when there is no history yet.
- Defect in the final round unconditionally.

Equivalent compact version:

```text
C iff
  t < r
  and
  [ (in the last up to 3 rounds, opponent cooperation reached at least m-1 in at least 2 rounds)
    and
    (the most recent observed count is at least m-2) ]
otherwise D
```

Edge handling:

- First round: `D`
- Final round: `D`
- If history is too short to evaluate the 3-round window, use whatever history exists; cooperate only if every observed round so far has been at least `m-1` opponents cooperating and the latest observed count is exactly `m-1` or `m-2`.
- If the recent support drops below `m-2` for two consecutive rounds, switch to `D` until the threshold becomes near again.
'''

description_SELFINTERESTED_8 = '''
Let `x_t` be the number of opponents who cooperated in round `t`.

State variables:
- `need = m - 1`
- `streak =` number of consecutive previous rounds with `x >= need`

Decision rule:

```text
Round 1:
    defect

Round t > 1:
    if x_{t-1} < need:
        defect
    else if x_{t-1} == need:
        cooperate
    else if x_{t-1} > need:
        cooperate only if x_{t-2} >= need and x_{t-1} <= x_{t-2}
        otherwise defect
```

Equivalent interpretation:
- Cooperate only when the last observed round shows the group sitting exactly at the threshold of success, or when success has been stable for two rounds and is not weakening.
- Defect immediately after any round below threshold until the observed cooperation count returns to at least `m-1`.

Final-round rule:
- Use the same rule as above; there is no separate endgame cooperation push.
- If the last observed round was below `m-1`, defect.
- If the last observed round was exactly `m-1`, cooperate.
- If the last observed round was above `m-1`, cooperate only after a two-round stable streak.

State update:
- After each round, set `streak = streak + 1` if `x_t >= need`, else `streak = 0`.
- If `streak >= 2`, allow cooperation only while `x_t` does not fall.

This strategy plays for immediate self-interest by defecting whenever the reward condition is not plausibly being sustained, and by contributing only when the observed group is at or near the minimum level needed to preserve the bonus.
'''

description_SELFINTERESTED_9 = '''
Initialize:
- Set `mode = cautious`.
- Keep `x_prev = None`.

For round `t = 1`:
- Play `D`.

For each round `t >= 2`, let `x_prev` be the number of opponents who cooperated in round `t-1`.

Decision rule:
- Play `C` if `x_prev >= m - 1`.
- Play `D` if `x_prev < m - 1`.

Memory update after each round:
- Replace `x_prev` with the observed opponent cooperation count from the most recent round.

Edge handling:
- If round `t-1` had exactly `m - 1` cooperating opponents and you played `C`, continue playing `C` in round `t` as long as the observed cooperation count remains at least `m - 1`.
- If the observed cooperation count drops below `m - 1` in any round, switch to `D` immediately in the next round.
- In the final round, use the same rule; do not cooperate unless the previous-round cooperation level reached at least `m - 1`.

Compact form:
```text
if t == 1:
    play D
else:
    if x_prev >= m - 1:
        play C
    else:
        play D
```
'''

description_SELFINTERESTED_10 = '''
State variables:
- `h`: list of observed opponent cooperation counts from previous rounds
- `L`: lookback window, use `L = min(5, len(h))` and ignore if `L = 0`

Round 1:
- Play `D`

For round `t > 1`:
1. Let `avg = average of the last L observations in h`
2. Estimate opponent cooperation rate:
   `q = avg / (n - 1)`
3. Estimate the probability that exactly `m - 1` opponents cooperate this round:
   `p = C(n-1, m-1) * q^(m-1) * (1-q)^(n-m)`
4. Choose:
   - `C` if `p > 1 / k`
   - `D` otherwise

Tie-break:
- If `p = 1 / k`, play `D`

Update after the round:
- Append the observed number of cooperating opponents to `h`

Practical shorthand:
- Default to `D`
- Switch to `C` only when recent history makes it likely that your cooperation is pivotal for reaching exactly the threshold, and the estimated pivotal chance exceeds `1/k`

Edge handling:
- If `q = 0` or `q = 1`, play `D`
- If `t = r` (last round), use the same rule; do not change behavior for endgame alone
'''

description_SELFINTERESTED_11 = '''
Play D by default, and switch to C only when the history indicates that your cooperation has a strong chance of being pivotal.

State to track:
- `s_t`: number of opponents who cooperated in round `t`
- `p̂_t`: estimated probability that any given opponent cooperates in a round
- `λ ∈ (0,1)`: discount factor for recent history, use a fixed value like `0.7`

Initialization:
- Round 1: play `D`

Update after each round `t`:
- Let `x_t = s_t / (n - 1)` be the observed opponent cooperation rate
- Update the estimate recursively:
  - `p̂_{t+1} = λ * p̂_t + (1 - λ) * x_t`
- If there is no prior estimate, set `p̂_2 = x_1`

Decision rule for round `t ≥ 2`:
- Compute the probability that exactly `m - 1` opponents cooperate under the current estimate:
  - `q_t = BinomialPMF(n - 1, p̂_t, m - 1)`
- Cooperate iff both of the following hold:
  1. `q_t * k > 1`
  2. The last observed round had at least `m - 1` cooperating opponents: `s_{t-1} ≥ m - 1`

Otherwise, play `D`.

Practical interpretation:
- If opponents are consistently near the threshold, cooperate.
- If opponents are too disorganized or too sparse, defect.
- If opponents have already shown they can clear the threshold without you, defect.
- If the estimated chance of being pivotal drops below `1 / k`, defect.

Late-round rule:
- In the final round, use exactly the same rule; do not change behavior just because the game is ending.

Pseudocode:

```text
Round 1: play D

For round t = 2..r:
    observe s_{t-1}
    x = s_{t-1} / (n - 1)

    if t == 2:
        p_hat = x
    else:
        p_hat = λ * p_hat + (1 - λ) * x

    q = BinomialPMF(n - 1, p_hat, m - 1)

    if (q * k > 1) and (s_{t-1} >= m - 1):
        play C
    else:
        play D
```

If you want a simpler version with no probability calculation:
- Round 1: `D`
- Thereafter: play `C` only after a round in which the number of cooperating opponents was exactly `m - 1` or `m - 2`, and only if this pattern has occurred in at least two of the last three rounds; otherwise `D`
'''

description_SELFINTERESTED_12 = '''
Maintain a two-state policy: support mode and exit mode.

State variables:
- `support_mode ∈ {true, false}`, initialized to `true`
- `last_x`: number of opponents who cooperated in the previous round

Decision rule

Round 1:
- Play `C`

For round `t > 1`, observe `x =` number of opponents who cooperated in round `t-1`.

1. If `x >= m - 1`:
   - Play `C`
   - Set `support_mode = true`

2. If `x < m - 1`:
   - Play `D`
   - Set `support_mode = false`

State refinement:
- If `support_mode = false`, keep playing `D` until a round is observed with `x >= m - 1`
- The first time `x >= m - 1` appears again, immediately switch back to `C`

Edge cases

- First round: always `C`
- Last round: use the same rule as any other round; no special change
- If `m = 2`, cooperate whenever at least one opponent cooperated in the previous round
- If `m = n - 1`, cooperate only when at least `n - 2` opponents cooperated in the previous round
- If the observed cooperation count is exactly `m - 1`, treat it as sufficient and cooperate
- If the observed cooperation count is `0`, stay in `D` until cooperation reappears at or above `m - 1`

Operational summary

- Cooperate only when the previous round showed that the threshold is within reach from the others alone
- Defect whenever the previous round showed that your cooperation was not needed to reach the threshold
- Restart cooperation immediately once the others again get close enough to make the threshold attainable
'''

description_SELFINTERESTED_13 = '''
Let \(x_t\) be the number of opponents who cooperated in round \(t\). Use only the most recent observed \(x_t\) to choose round \(t+1\).

Decision rule for round \(t\):

- If \(t=1\): play \(D\).
- If \(t>1\):
  - play \(C\) if and only if \(x_{t-1} = m-1\)
  - otherwise play \(D\)

Equivalent form:
- cooperate only when your cooperation is the unique missing action needed to reach the threshold
- defect in every other situation

Edge handling:
- If \(x_{t-1} \ge m\): defect, since the threshold was already met without needing your contribution.
- If \(x_{t-1} \le m-2\): defect, since your single cooperation would still leave the group below threshold.
- In the final round \(t=r\): apply the same rule; there is no special concession to future rounds.

State update:
- After each round, record \(x_t\) and discard older history unless you want a tie-breaker for implementation simplicity.

Optional tie-breaker for incomplete or noisy observation:
- If the observed count is unavailable, default to \(D\).
'''

description_SELFINTERESTED_14 = '''
Keep a running record of the number of cooperating opponents in each completed round, \(s_t\).

Decision rule for round \(t\):

- **If \(t=1\):** play **D**.
- **If \(t>1\):**
  - play **C** if \(s_{t-1} = m-1\)
  - play **D** if \(s_{t-1} \ge m\)
  - play **D** if \(s_{t-1} \le m-2\)

Optional memory refinement:
- If the last two observed rounds were \(m-1\) and \(m-1\), keep playing **C** until the observed count rises to at least \(m\), then switch back to **D**.
- If the observed count drops below \(m-1\) in any round, immediately switch to **D** next round.

Last-round handling:
- In the final round, apply the same rule: **C** only when the previous round showed exactly \(m-1\) cooperating opponents; otherwise **D**.

Compact pseudocode:

```text
for round t:
    if t == 1:
        play D
    else:
        if s[t-1] == m-1:
            play C
        else:
            play D
```

This is a self-interested threshold-support strategy: contribute only when the previous round shows that your contribution is likely to be pivotal, and otherwise keep the endowment.
'''

description_SELFINTERESTED_15 = '''
Maintain an estimate of the opponents’ cooperation rate and cooperate only when being pivotal is valuable enough.

Let \(x_t\) be the number of cooperating opponents observed after round \(t\).

Initialize a smoothed estimate
\[
q_0 = \frac{m-1}{n-1}.
\]

After each completed round \(t\), update
\[
q_t = \frac{\alpha (m-1) + \sum_{s=1}^{t} x_s}{\alpha (n-1) + t (n-1)}
\]
with \(\alpha = 1\) for mild smoothing.

In round \(t+1\), compute
\[
\lambda_t = \Pr\left(\mathrm{Bin}(n-1, q_t) = m-1\right)
= \binom{n-1}{m-1} q_t^{\,m-1}(1-q_t)^{\,n-m}.
\]

Decision rule:
- Cooperate if \(k \cdot \lambda_t > 1\).
- Defect otherwise.

Edge cases:
- Round 1: use \(q_0 = \frac{m-1}{n-1}\) in the same rule.
- If \(m-1 > n-1\) is impossible under the game constraints, so the rule never needs special handling there.
- If \(m=2\), then \(\lambda_t = (n-1)q_t(1-q_t)^{n-2}\), and the same inequality applies.
- In the final round, use exactly the same rule; there is no endgame exception.

Operationally:
1. Start with \(q_0 = (m-1)/(n-1)\).
2. After each round, update \(q_t\) from observed opponent cooperation counts.
3. Cooperate only when the estimated chance of being the pivotal contributor is high enough to justify it; otherwise defect.
'''

description_SELFINTERESTED_16 = '''
Initialize: play D in round 1.

For every round t from 2 to r:

1. If t = r, play D.

2. Otherwise let T be the total number of cooperators in round t−1, reconstructed from the observed number of cooperating opponents plus your own action in round t−1.

3. Decision rule:
   - If T ≥ m: play D.
   - If T = m−1:
     - If you played D in round t−1: play C.
     - If you played C in round t−1:
       - play C only if round t−2 also had total cooperators ≥ m−1;
       - otherwise play D.
   - If T ≤ m−2:
     - play D unless the last two rounds both had total cooperators ≥ m−1, in which case play C for one round.

4. After any round in which you play C and the threshold is still not met, immediately return to D unless the next round again satisfies one of the explicit cooperation conditions above.

State kept between rounds:
- your own previous action
- the previous round’s total cooperation count
- the round before that, when available

This is a strict free-riding default with short, history-based rescue cooperation only when the recent aggregate behavior suggests your contribution is close to being decisive.
'''

description_SELFINTERESTED_17 = '''
Defect in every round, regardless of history, observed cooperation counts, round number, or parameter values.

Pseudocode:

```text
for each round t = 1..r:
    play D
```
'''

description_SELFINTERESTED_18 = '''
Round 1: cooperate.

For every round t from 2 to r-1, let s_{t-1} be the number of opponents who cooperated in the previous round.

- Cooperate if s_{t-1} ≥ m-1 and, unless t=2, s_{t-2} ≥ m-1 as well.
- Otherwise defect.

Round r: defect.

Recovery rule:
- After any round with s_t < m-1, switch to defecting immediately.
- Resume cooperating only after observing two consecutive rounds with s ≥ m-1.

Equivalent pseudocode:

```text
if t == r:
    play D
else if t == 1:
    play C
else if last_round_opponents_coop >= m-1 and (t == 2 or round_before_last_opponents_coop >= m-1):
    play C
else:
    play D
```

This keeps cooperation only when the observed coalition has shown stable support, and defaults to defecting whenever that support weakens or in the final round.
'''

description_SELFINTERESTED_19 = '''
Round 1: play D.

For round t > 1, let x_{t-1} be the number of opponents who cooperated in the previous round.

Maintain:
- s_t = the average number of cooperating opponents over the last up to 3 rounds
- g_t = x_{t-1} - x_{t-2} if t > 2, otherwise 0

Decision rule:
- Play C only if all of the following hold:
  1. x_{t-1} = m - 1, or s_t ≥ m - 1
  2. g_t ≥ 0
  3. the previous round met the threshold, or was short by exactly one cooperator
- Otherwise play D

More explicitly:

- If x_{t-1} ≥ m:
  - play D
- If x_{t-1} = m - 1:
  - play C
- If x_{t-1} ≤ m - 2:
  - play D

Refinement for the last three rounds:
- If the threshold has been met in at least 2 of the last 3 rounds, play D unless x_{t-1} = m - 1
- If the threshold has failed in all of the last 3 rounds, play D
- If t = r:
  - play C only when x_{r-1} = m - 1
  - otherwise play D

Fallback rule:
- At any time, if the observed cooperation count is unstable or trending downward, defect
- Cooperate only after observing a near-success state that is exactly one short of the threshold

Implementation form:

```
if t == 1:
    action = D
else:
    if x_prev == m - 1:
        action = C
    else:
        action = D
```

Optional history filter:
- If the last two rounds both had x < m - 1, ignore any temporary spike and continue defecting until a round with x = m - 1 appears.
'''

description_SELFINTERESTED_20 = '''
Policy state:

- `s =` number of rounds among the last `L = min(3, r-1)` rounds in which the number of cooperating opponents was exactly `m-1`
- `h =` number of rounds among the last `L` rounds in which the number of cooperating opponents was at least `m-1`

Decision rule for round `t`:

1. **If `t = 1`:** play `D`.
2. **If `t = r`:** play `D`.
3. **Otherwise:**
   - Play `C` only if:
     - the previous round had exactly `m-1` cooperating opponents, and
     - among the last `L` observed rounds, at least `2` of them had exactly `m-1` cooperating opponents, or all available observed rounds so far have done so if fewer than 2 exist.
   - In every other case, play `D`.

Equivalent compact form:

```text
if t == 1 or t == r:
    play D
else:
    if last_round_opponents_cooperated == m-1 and recent_exact_m_minus_1_count >= 2:
        play C
    else:
        play D
```

Tie-handling and edge cases:

- If the number of observed opponent cooperators in the previous round was `m` or more, always play `D`.
- If it was `m-2` or fewer, always play `D`.
- If it was exactly `m-1`, cooperate only when that near-threshold pattern has repeated enough to indicate that your contribution is likely to be pivotal again.
- Never cooperate in the first or last round.
- If the history is too short to evaluate the recent-pattern condition, default to `D`.

State update after each round:

- Record only the count of opponent cooperators from that round.
- Recompute `recent_exact_m_minus_1_count` on the rolling window of the most recent `L` rounds.
'''

description_SELFINTERESTED_21 = '''
Play **C** only when the observed state makes it likely that your cooperation is pivotal to preserving a high-payoff cooperative level; otherwise play **D**.

### State variables to track
- `x_t`: number of opponents who cooperated in round `t`
- `s_t`: your own action in round `t`
- `q_t`: a running estimate of opponent cooperativeness, updated from observed `x_t`

Initialize:
- `q_0 = 1/2`
- `trust = 0`

Update after each round:
- `q_t = (t * q_{t-1} + x_t / (n-1)) / (t+1)`
- `trust += 1` if `x_t >= m-1` and you played `C`
- `trust -= 1` if `x_t < m-1` and you played `C`
- clamp `trust` to `[0, 3]`

### Decision rule each round `t`
Let `rem = r - t + 1`.

1. **First round**
   - If `m <= 2`, play **C**.
   - Otherwise play **D**.

2. **Middle rounds**
   - Let `last_round_coop = 1` if `x_{t-1} >= m-1`, else `0`.
   - Play **C** if all of the following hold:
     - `q_{t-1} >= (m-1)/(n-1)`
     - `x_{t-1} >= m-1`
     - `trust >= 1`
   - Otherwise play **D**.

3. **Recovery rule**
   - If the previous round failed by exactly one opponent short of threshold, and `q_{t-1} > (m-2)/(n-1)`, play **C** once.
   - After any round in which you played **C** and the group still failed, return to **D** for the next two rounds.

4. **Endgame**
   - If `rem <= 2`, play **D** unless:
     - `x_{t-1} >= m-1` and `q_{t-1} >= (m-1)/(n-1)` and `trust >= 2`
   - On the final round, play **D** unless the previous round achieved threshold with at least `m` cooperators total.

### Practical shorthand
- **Open with caution:** defect by default unless the game is small enough that early cooperation is cheap insurance (`m <= 2`).
- **Cooperate only on evidence:** switch to **C** only after seeing repeated rounds where the community is already meeting or nearly meeting the threshold.
- **Punish unreliability:** after a failed cooperative attempt, stop cooperating for two rounds.
- **Exploit the endgame:** defect in the last two rounds unless cooperation is already very likely to succeed.

### Compact pseudocode
```text
if t == 1:
    if m <= 2: play C
    else: play D
else:
    if rem <= 2:
        if x_{t-1} >= m-1 and q_{t-1} >= (m-1)/(n-1) and trust >= 2:
            play C
        else:
            play D
    else:
        if x_{t-1} >= m-1 and q_{t-1} >= (m-1)/(n-1) and trust >= 1:
            play C
        elif x_{t-1} == m-2 and q_{t-1} > (m-2)/(n-1):
            play C
        else:
            play D
```

### Self-interested principle
Prefer **D** whenever cooperation is not clearly needed to protect a higher expected payoff; switch to **C** only when observed opponent behavior indicates that your cooperation is likely to help preserve a threshold-achieving pattern that can persist for multiple rounds.
'''

description_SELFINTERESTED_22 = '''
Let \(x_t\) be the number of opponents who cooperated in round \(t\).

Decision rule for round \(t\):

- If \(t=1\): play \(D\).
- If \(t>1\), inspect \(x_{t-1}\) and the last two observed counts when available.

Play \(C\) only when your contribution is likely to be pivotal:
- play \(C\) if \(x_{t-1}=m-1\);
- else play \(C\) if \(x_{t-1}=m-2\) and both of the following hold:
  - the most recent two observations are nondecreasing, i.e. \(x_{t-2}\le x_{t-1}\) when \(t\ge 3\);
  - the 3-round average of observed opponent cooperators is at least \(m-1\) when \(t\ge 4\).

Otherwise play \(D\).

Edge handling:
- If \(t<3\), use only the observations that exist.
- If the recent average is unavailable, rely on the exact-count rule above.
- If \(x_{t-1}\ge m\), always play \(D\).
- If \(x_{t-1}\le m-3\), always play \(D\).
- In the final round, use the same rule with no special exception; do not cooperate unless the pivot condition is met.

State update:
- After each round, record \(x_t\) and recompute the recent trend and average from the most recent available observations.

Behavioral principle:
- Default to keeping the endowment.
- Cooperate only when the observed history suggests that your contribution can directly move the group from just below the threshold to at or above it.
'''

description_SELFINTERESTED_23 = '''
Play D in every round.

Decision rule:
- If a round begins, choose D.
- Ignore observed cooperation counts when selecting your action.
- Never switch to C based on past history.

Edge cases:
- Round 1: choose D.
- Any middle round: choose D.
- Final round: choose D.
- If all previous rounds had many cooperators: choose D.
- If all previous rounds had few or zero cooperators: choose D.
- If the observed count is exactly m-1, m, or any other value: choose D.

State update:
- Track history only if needed for recordkeeping; it never changes the action.

Compact pseudocode:
```text
for t = 1 to r:
    action[t] = D
```
'''

description_SELFINTERESTED_24 = '''
Round 1: play D.

For rounds 2 through r-1:
- Let x be the number of players (excluding yourself) who cooperated in the previous round.
- Let T = m - 1, the minimum number of opponents who must cooperate for your own cooperation to help reach the threshold.
- Play C only if all of the following hold:
  1. x ≥ T
  2. x was at least T in each of the last two rounds, if available
  3. The observed cooperation count has not fallen in the last two rounds
- Otherwise play D.

Last round:
- Play D.

Compact rule:
- Cooperate only when recent history shows a stable coalition already large enough that your cooperation is likely to matter.
- Defect in the first round, whenever cooperation support weakens, and always in the final round.

Pseudocode:

```text
if t == 1:
    action = D
else if t == r:
    action = D
else:
    x_t1 = cooperators observed in round t-1 among opponents
    x_t2 = cooperators observed in round t-2 among opponents, if t > 2

    if x_t1 >= m - 1 and (t == 2 or x_t2 >= m - 1) and (t == 2 or x_t1 >= x_t2):
        action = C
    else:
        action = D
```

If cooperation has been consistently at or above the minimum support level for two consecutive nonterminal rounds, cooperate; otherwise defect.
'''

description_SELFINTERESTED_25 = '''
Play D in every round.

Decision rule:
- Round 1: defect.
- Rounds 2 through r−1: defect regardless of prior outcomes.
- Final round: defect.

History dependence:
- Ignore all observations of others’ cooperation counts.
- Never switch to cooperation, regardless of whether previous rounds met or missed the threshold.

Edge cases:
- If r = 2, defect in both rounds.
- If m = n−1 or m is very small, still defect.
- If you ever observe a round where the threshold is met, continue defecting.
- If you observe repeated failure to meet the threshold, continue defecting.

Behavioral summary:
- Maximize individual payoff by never paying the cooperation cost.
- Treat every round as a pure defection choice.
'''

description_SELFINTERESTED_26 = '''
Use a threshold-learning policy with an optimistic start and a safety fallback:

Let `x_t` be the number of opponents you observed cooperating in round `t-1` among the `n-1` others, and let `s_t = x_t + 1` if you cooperated in round `t-1`, otherwise `s_t = x_t`.

Maintain:
- `best_mode ∈ {C, D}` as the action that currently appears more profitable
- `support_C` = number of past rounds in which cooperation was “close to” or met the threshold
- `support_D` = number of past rounds in which cooperation was clearly too low

Decision rule for round `t`:

1. **First round**
   - Play `C` if `k ≥ 1` or if `m ≤ n/2`
   - Otherwise play `D`

2. **After each observed round**
   - If the total number of cooperators in that round was at least `m`, increment `support_C`
   - If it was below `m - 1`, increment `support_D`
   - If it was exactly `m - 1`, treat it as borderline and do not change the mode
   - Set `best_mode = C` if `support_C > support_D`, else `D` if `support_D > support_C`, else keep the previous `best_mode`

3. **Main play rule**
   - Play `C` when all of the following hold:
     - `best_mode = C`
     - In the previous round, total cooperation was at least `m - 1`
     - The current round is not the final round unless the previous round already met the threshold
   - Otherwise play `D`

4. **Final-round rule**
   - On the last round, play `C` only if the previous round met the threshold and at least `m - 1` others cooperated in that previous round
   - Otherwise play `D`

5. **Recovery rule**
   - If cooperation fails to meet the threshold for two consecutive rounds, defect for the next round
   - Resume cooperating only after observing a round with at least `m - 1` cooperating opponents

Equivalent pseudocode:

```text
if t == 1:
    action = C if (k >= 1 or m <= n/2) else D
else:
    update support_C / support_D from last round
    if support_C > support_D:
        best_mode = C
    else if support_D > support_C:
        best_mode = D

    if t == r:
        action = C if (last_round_total_cooperators >= m and last_round_opponents_cooperated >= m-1) else D
    else if last_two_rounds_both_failed:
        action = D
    else if best_mode == C and last_round_total_cooperators >= m-1:
        action = C
    else:
        action = D
```

This keeps cooperation active only when it is already plausibly paying off, defects immediately when the group falls short, and avoids wasting the last round on unproductive cooperation.
'''

description_SELFINTERESTED_27 = '''
Play C only when the observed cooperative level is sufficiently close to the threshold and recent history shows that cooperation is already the dominant pattern; otherwise play D.

Let `x_t` be the number of cooperators among the other `n-1` players in round `t`, and let `X_t = x_t + 1` if you cooperated, `x_t` otherwise be the total number of cooperators you infer for that round.

Maintain:
- `s_t`: smoothed estimate of how many of the other players will cooperate next round
- `q_t`: streak of recent threshold success

Initialization:
- `s_1 = 0`
- `q_1 = 0`

Update after each round `t`:
- `s_{t+1} = 0.7 * s_t + 0.3 * x_t`
- If `X_t >= m`, set `q_{t+1} = min(q_t + 1, 3)`
- Otherwise set `q_{t+1} = max(q_t - 1, 0)`

Decision rule in round `t`:
1. Compute the minimum number of additional cooperators needed among the other players if you cooperate:
   - `need_C = m - 1`
2. Compute the minimum number needed if you defect:
   - `need_D = m`

3. Cooperate if and only if all of the following hold:
   - `r - t >= 2`, and
   - `s_t >= need_C`, and
   - `q_t >= 1`

Otherwise defect.

Edge cases:
- Round 1: defect unless `m = 2` and `n = 2`; in that special case cooperate.
- Penultimate round: cooperate only if `s_t >= m - 1` and `q_t >= 2`; otherwise defect.
- Last round: defect.
- If `m = n - 1`, cooperate only after at least two consecutive rounds with `x_t >= m - 1`.
- If `m` is small and the threshold has already been met in the last two rounds, keep cooperating while `q_t >= 2` and `s_t >= m - 1`; otherwise revert to defect.

Compact rule:
- Default action: `D`
- Switch to `C` only after observing repeated evidence that the group is already sustaining cooperation near the threshold
- Immediately revert to `D` after any failed round
- Always defect in the final round
'''

description_SELFINTERESTED_28 = '''
Round 1: play D.

For each round t > 1, let x be the number of other players who cooperated in round t-1.

- If x ≥ m: play D.
- If x = m - 1: play C.
- If x ≤ m - 2: play D.

Tie-breaker for a short run of ambiguous history:
- If the last two observed counts are both m - 1, keep playing C.
- If the last two observed counts are both at least m, keep playing D.
- Otherwise follow the rule above using the most recent round.

Last round: use the same rule as any other round; do not change behavior just because the game is ending.

If the previous round failed to meet the threshold by a wide margin, stay with D until the observed count of cooperating opponents returns to at least m - 1 in a later round.
'''

description_SELFINTERESTED_29 = '''
Play D in every round.

Decision rule:
- Round 1: D
- Rounds 2 through r: D
- If any history-based rule would suggest otherwise, ignore it and choose D anyway
- If a tie or uncertainty arises in any internal calculation, break it in favor of D

State update:
- You may track past cooperative counts for inference, but do not let that change the action
- No round is an exception, including the last round and any round where cooperation by you would affect whether the threshold is met
'''

description_SELFINTERESTED_30 = '''
Round 1: play D.

Every later round t = 2..r:
- play D.

Ignore the observed cooperation counts when choosing actions.

If forced to encode as a state rule:
```text
state = "defect"

for each round t:
    if state == "defect":
        action = D
    else:
        action = D
```

Edge cases:
- First round: D
- Last round: D
- Any streak of high cooperation by others: D
- Any streak of low cooperation by others: D
- If your previous action was C for any reason: switch back to D immediately and stay there
'''

description_SELFINTERESTED_31 = '''
State variables:
- `t`: current round number
- `h`: list of observed opponent cooperation counts from previous rounds
- `s`: number of past rounds with `x = m-1`, where `x` is the observed number of cooperating opponents in that round

Decision rule for round `t`:

1. If `t = 1`, play `D`.

2. Otherwise, compute
   - `p_hat = (s + 1) / (t + 1)`  
     where the `+1` terms are a neutral smoothing prior.

3. Play `C` if and only if `p_hat > 1 / k`; otherwise play `D`.

History update after each round:
- Observe `x_t`, the number of cooperating opponents in round `t`
- Append `x_t` to `h`
- If `x_t = m - 1`, increment `s`

Equivalent pseudocode:

```text
if t == 1:
    action = D
else:
    p_hat = (count(h == m-1) + 1) / (t + 1)
    if p_hat > 1 / k:
        action = C
    else:
        action = D

after round:
    observe x_t
    h.append(x_t)
```

Tie handling:
- If `p_hat = 1 / k`, play `D`.

Edge cases:
- If `m = 2`, the trigger condition is `x = 1`.
- If `m = n - 1`, cooperation is only selected when the observed opponent count has repeatedly clustered at `n - 2`.
- In the final round, use the same rule with no special exception.

Behavioral interpretation:
- Stay with `D` by default.
- Switch to `C` only after the history shows that the opponents’ cooperation count lands on the pivotal value `m - 1` often enough to justify contributing.
'''

description_SELFINTERESTED_32 = '''
Round 1: play D.

For round t = 2 to r - 1, observe x_{t-1}, the number of opponents who cooperated in the previous round, and keep the last two observed counts if available.

Play C only when cooperation appears narrowly needed and has been sustained:
- If t = 2: play C iff x_{1} = m - 1.
- If t ≥ 3: play C iff both conditions hold:
  1. x_{t-1} ∈ {m - 2, m - 1}
  2. At least two of the last three observed counts are ≥ m - 1

Otherwise play D.

Round r: play D.

Edge handling:
- If the history is shorter than required for the rule, default to D unless the current observation is exactly x_{t-1} = m - 1 on round 2.
- If the opponents’ observed cooperation drops below m - 2 in any round, reset to D until there are again at least two recent rounds with x ≥ m - 1.
- If x_{t-1} ≥ m, always play D on the next round.
- If x_{t-1} = m - 1 and the recent pattern is stable, cooperate once to help keep the threshold reachable; otherwise defect.

State variables:
- `recent = [x_{t-3}, x_{t-2}, x_{t-1}]` truncated to what exists
- `stable = count(x in recent where x >= m - 1) >= 2`
- `narrow = x_{t-1} in {m-2, m-1}`

Decision rule:
```text
if t == 1 or t == r:
    D
else if t == 2:
    C if x1 == m-1 else D
else:
    C if narrow and stable else D
```
'''

description_OPPORTUNISTIC_5 = '''
Let \(H_t\) be the number of opponents who cooperated in round \(t\), and let \(S_{t-1}=\sum_{j=1}^{t-1}(H_j+1_{\{I_j=C\}})\) be the total number of cooperators observed so far, including yourself when you cooperated.

Use this policy:

**State variables**
- \(t\): current round
- \(s\): number of rounds already played
- \(\hat p\): estimated cooperation rate among opponents, updated from observed history
- \(q\): recent cooperation level, based on a sliding window of the last \(w\) rounds

**Initialization**
- Round 1: cooperate.

**Update after each round**
- Set \(\hat p = \dfrac{\sum_{j=1}^{t} H_j}{(n-1)t}\).
- Set \(q = \dfrac{1}{\min(w,t)}\sum_{j=\max(1,t-w+1)}^{t} H_j\).

Use \(w=3\) when \(r\ge 3\); otherwise \(w=1\).

**Decision rule for round \(t+1\)**
Let \(R = r-(t)\) be the number of rounds remaining after the current one.

Cooperate if any of the following holds:
1. \(t=1\).
2. \(R=0\) is impossible; on the final round, cooperate only if the most recent observed opponent cooperation count satisfies \(H_t \ge m-1\).
3. The recent window is strong: \(q \ge m-1\).
4. The long-run estimate is strong: \(\hat p \ge \dfrac{m-1}{n-1}\) and the last observed round had \(H_t \ge m-1\).
5. You are in a recovery phase after a near-miss: if \(H_t = m-2\) and \(R \ge 2\), cooperate for the next \(\min(2,R)\) rounds.
6. You are in the final stretch and the threshold is reachable: if \(R \le 2\) and \(H_t \ge m-2\), cooperate.

Otherwise defect.

**Aggressive opportunism rule**
If at any point \(H_t \le m-3\) for two consecutive rounds, defect until one of the following occurs:
- a round with \(H_t \ge m-1\), or
- the last two rounds remain, in which case revert to the final-round rule above.

**Late-game tightening**
For the last \(L=\max(2,\lceil r/4\rceil)\) rounds:
- Cooperate only if the previous round met or nearly met the threshold: \(H_t \ge m-1\), or \(H_t = m-2\) and \(\hat p \ge \dfrac{m-1}{n-1}\).
- Otherwise defect.

**Edge cases**
- If \(m=2\), cooperate on round 1; afterward cooperate whenever at least one opponent cooperated in the previous round, and defect after two consecutive zero-cooperation rounds.
- If \(m=n-1\), require near-unanimity: cooperate only if the last round had at least \(n-2\) opponent cooperators, or the rolling average over the last \(w\) rounds is at least \(n-2\).
- If \(r=2\), cooperate in round 1; in round 2, cooperate iff round 1 had \(H_1 \ge m-1\).
- If the observed cooperation level has never reached \(m-1\) by round \(\lfloor r/2\rfloor\), defect from then on except in the last round, where you cooperate only if \(H_{r-1}\ge m-1\).

**Compact pseudocode**
```text
if t == 1:
    play C
else:
    update p_hat and q

    if t == r:
        play C if H_{t-1} >= m-1 else D
    else if last two rounds had H <= m-3:
        play D
    else if t > r - max(2, ceil(r/4)):
        play C if (H_{t-1} >= m-1) or (H_{t-1} == m-2 and p_hat >= (m-1)/(n-1)) else D
    else if q >= m-1:
        play C
    else if p_hat >= (m-1)/(n-1) and H_{t-1} >= m-1:
        play C
    else if H_{t-1} == m-2 and remaining_rounds >= 2:
        play C for the next 2 rounds
    else:
        play D
```
'''

description_OPPORTUNISTIC_6 = '''
Let \(x_t\) be the number of opponents who cooperated in round \(t\). Keep only the last two observations.

State:
- \(x_{t-1}\): last round opponents’ cooperations
- \(x_{t-2}\): previous round opponents’ cooperations, if available

Decision rule for round \(t\):

1. **Round 1:** play \(D\).

2. **Rounds 2 through \(r-1\):**
   - Play \(D\) if \(x_{t-1} \ge m\).
   - Play \(C\) if all of the following hold:
     - \(x_{t-1} = m-1\)
     - either \(t=2\) or \(x_{t-2} \ge m-1\)
     - \(x_{t-1}\) has not dropped for two consecutive observed rounds, i.e. if \(t \ge 3\), then \(x_{t-2} \le x_{t-1}\) is not required; instead require \(x_{t-2} \ge m-1\)
   - Otherwise play \(D\).

3. **Final round \(r\):** play \(D\).

Equivalent pseudocode:

```text
if t == 1:
    play D
else if t == r:
    play D
else:
    if x[t-1] >= m:
        play D
    else if x[t-1] == m-1 and (t == 2 or x[t-2] >= m-1):
        play C
    else:
        play D
```

Operational meaning:
- Stay defecting by default.
- Cooperate only in the narrow “knife-edge” case where the previous round showed the opponents exactly one short of the threshold and the shortfall has not worsened across the last observed rounds.
- Never spend cooperation in the first round or final round.
- If the observed opponent cooperation rises above the threshold, immediately revert to pure defection.
'''

description_OPPORTUNISTIC_7 = '''
Let \(H_t\) be the number of opponents who cooperated in round \(t\), and let \(S_t\) be the cumulative number of cooperative opponents observed so far:
\[
S_t=\sum_{\tau=1}^{t} H_\tau
\]
Let \(\bar H_t = \frac{1}{t}\sum_{\tau=1}^{t} H_\tau\).

Define two parameters from the game:
- \(q = m-1\): the largest number of opponent cooperators you can tolerate while still needing at least one more cooperator from others to reach the threshold
- \(L = \lceil r/4 \rceil\): the initial probing window

Decision rule for round \(t\):

1. **Round 1**
   - Play \(C\).

2. **Rounds \(2\) through \(L\): probe and mirror**
   - Play \(C\) if \(H_{t-1} \ge m-1\).
   - Otherwise play \(D\).

3. **After round \(L\): opportunistic threshold rule**
   - Play \(C\) if both conditions hold:
     - \(H_{t-1} \ge m-1\), and
     - \(\bar H_{t-1} \ge m-1\)
   - Otherwise play \(D\).

4. **Late-game tightening**
   - If \(t > r - \lceil r/5 \rceil\), play \(C\) only when:
     - \(H_{t-1} \ge m-1\), and
     - \(H_{t-1} \ge \max(m-1,\lceil \bar H_{t-1}\rceil)\)
   - Otherwise play \(D\).

Edge-case overrides:

- **If the previous round met the threshold with exactly \(m-1\) or more opponents cooperating and you played \(D\)**, switch to \(C\) in the next round.
- **If the previous round failed by exactly one opponent cooperator** \((H_{t-1}=m-2)\), keep playing \(D\) for one more round unless the running average \(\bar H_{t-1}\) is at least \(m-1\).
- **If you observe sustained cooperation for 3 consecutive rounds**:
  - \(H_{t-1}\ge m-1\), \(H_{t-2}\ge m-1\), \(H_{t-3}\ge m-1\),
  - play \(C\) regardless of small fluctuations in the current round’s prior history.
- **If cooperation has been below \(m-1\) in the last 2 rounds and \(\bar H_{t-1}<m-1\)**, play \(D\) until the threshold is reached again.

Operational shorthand:

- Start by cooperating once.
- Continue cooperating only when recent opponent cooperation is sufficient to make threshold success likely.
- Defect whenever recent behavior falls short.
- In the final segment, cooperate only with clear evidence that the group is reliably above the threshold.

Pseudocode:

```python
if t == 1:
    action = C
elif t <= ceil(r/4):
    action = C if H[t-1] >= m-1 else D
elif t <= r - ceil(r/5):
    action = C if (H[t-1] >= m-1 and avg(H[1:t]) >= m-1) else D
else:
    action = C if (H[t-1] >= m-1 and H[t-1] >= max(m-1, ceil(avg(H[1:t])))) else D
```
'''

description_OPPORTUNISTIC_8 = '''
Use a contingent threshold strategy with exploration, locking-in, and late-round opportunism.

Let \(h_t\) be the number of cooperators you observed among your opponents in round \(t\), so total cooperators observed is \(H_t = h_t + \mathbf{1}\{\text{you cooperated}\}\).

Maintain:
- \(S_t = \max\{m - 1, \max_{1 \le \tau \le t} h_\tau\}\): the best observed opponent cooperation level so far, clipped at \(m-1\)
- \(q_t\): the fraction of opponents cooperating in recent rounds, computed over the last \(L = \min(3, t-1)\) rounds when available

Decision rule by round:

1. Round 1:
   - Cooperate.

2. Rounds 2 through \(r-2\):
   - Cooperate if either:
     - \(h_{t-1} \ge m-1\), or
     - \(S_{t-1} \ge m-1\), or
     - \(q_t \ge \frac{m-1}{n-1}\)
   - Otherwise defect.

3. Final two rounds:
   - Round \(r-1\):
     - Cooperate only if \(h_{r-2} \ge m-1\) and \(h_{r-3} \ge m-1\) when \(r \ge 4\); for \(r=3\), require only \(h_1 \ge m-1\).
     - Otherwise defect.
   - Round \(r\):
     - Cooperate if \(h_{r-1} \ge m-1\).
     - Otherwise defect.

Update rule after each round:
- If you cooperated and the threshold was met, stay ready to cooperate in the next round only if the observed cooperation count stays at or above \(m-1\).
- If you cooperated and the threshold was missed, switch to defecting until the observed cooperation count reaches \(m-1\) again.
- If you defected and the threshold was met without you, keep defecting unless the observed cooperation level remains at least \(m-1\) for two consecutive rounds.

Operational shortcut:
- Cooperate when the group appears capable of reliably reaching the threshold.
- Defect immediately when the observed cooperation count falls below \(m-1\).
- Re-enter cooperation as soon as the observed count returns to \(m-1\) or higher, with a two-round confirmation near the end of the game only when there is enough time to exploit stable cooperation.
'''

description_OPPORTUNISTIC_9 = '''
Set an aspiration threshold of “just enough” cooperation and play to stay one step on the safe side of it.

Decision rule by round:

- Round 1: play C.
- For each round t > 1:
  1. Reconstruct last round’s total cooperation count:
     - last_total = observed cooperators among opponents in round t-1 + 1 if you played C in round t-1, else +0.
  2. If last_total < m:
     - play C.
  3. If last_total = m:
     - play C.
  4. If last_total > m:
     - play D.

Operationally, this means:
- cooperate whenever the previous round failed to clear the threshold, or cleared it only exactly;
- defect only when the previous round had a surplus of cooperation beyond the minimum.

Optional stabilization rule for repeated oscillation:
- Keep a counter s of consecutive rounds with last_total < m.
- If s ≥ 2, cooperate for two consecutive rounds before returning to the normal rule.
- Reset s to 0 whenever last_total ≥ m.

Edge cases:
- If you cannot reconstruct your own past action, treat round 1 as C and thereafter infer it from your own strategy.
- In the final round, follow the same rule as usual; do not change behavior just because the game is ending.
- If a long run of last_total < m occurs, stay on C until the threshold is met again, then switch back to D only when a surplus appears.

Behavioral summary:
- C when the group is under-providing or barely meeting the threshold.
- D only when the group is comfortably above the threshold.
- Exploit surplus cooperation immediately, but never withdraw support when the margin is fragile.
'''

description_OPPORTUNISTIC_10 = '''
Play C whenever the observed history suggests that cooperation is already close to being self-sustaining; otherwise play D.

Decision rule

Let \(x_t\) be the number of opponents you observed cooperate in round \(t\), and let \(h_t\) be the number of cooperators needed from the other \(n-1\) players for the threshold to be met when you cooperate:
\[
h_t = m-1.
\]

Maintain two running statistics over past rounds:

- \(A_t\): average observed opponent cooperation count over rounds \(1,\dots,t-1\)
- \(S_t\): a momentum score updated by
  \[
  S_t = 0.7S_{t-1} + (x_{t-1} - \tau)
  \]
  with \(S_1 = 0\), where \(\tau = m-1\) is the cooperation level from opponents needed for your own cooperation to be pivotal.

Cooperate in round \(t\) if all three conditions hold:

1. Recent cooperation has been at least near-threshold:
   \[
   x_{t-1} \ge m-2
   \]
   for the immediately preceding round, or
   \[
   A_t \ge m-2
   \]
   if enough history exists.

2. Momentum is nonnegative:
   \[
   S_t \ge 0
   \]

3. It is not the final recovery-less round:
   \[
   t < r
   \]
   unless the observed cooperation pattern has already been stable.

Otherwise defect.

Round-by-round policy

- Round 1: play D.
- Round 2: play C if at least \(m-2\) opponents cooperated in round 1; otherwise play D.
- Middle rounds:
  - If the last two rounds both had at least \(m-2\) opponent cooperators, play C.
  - If cooperation dropped sharply below \(m-2\) in the last round, play D immediately.
  - If cooperation is hovering at the margin, play C only when the running average and momentum are both at or above the threshold.
- Final round:
  - Play C only if the last three rounds all had at least \(m-2\) opponent cooperators, or if the last round exactly met the threshold and the preceding momentum was positive.
  - Otherwise play D.

State update after each round

- Record \(x_t\).
- Update:
  \[
  A_{t+1} = \frac{(t-1)A_t + x_t}{t}
  \]
  for \(t \ge 1\).
- Update momentum:
  \[
  S_{t+1} = 0.7S_t + (x_t - (m-1)).
  \]

Opportunistic trigger

Switch into cooperation mode as soon as opponents show a repeated willingness to support the threshold:

- If two of the last three rounds each had \(x_t \ge m-2\), start cooperating.
- Stay cooperative while the last-round count remains at least \(m-2\) and the momentum score stays nonnegative.
- If the observed count falls below \(m-3\) in any round, immediately revert to D for the next round.

Default stance

- Defect on weak or mixed cooperation histories.
- Cooperate only when the group is already assembling enough support that your cooperation is likely to ride the threshold rather than carry it.
- Use the earliest rounds to sample behavior cheaply, then become selective and exploit stable cooperation only when the history justifies it.
'''

description_OPPORTUNISTIC_11 = '''
Let `O_t` be the number of opponents who cooperated in round `t-1` that you observe before choosing in round `t` (for `t=1`, there is no observation yet).

State variables:
- `miss_streak`: number of consecutive observed rounds in which `O_t < m-1` while you played `D` last round, or `O_t < m-2` while you played `C` last round
- `last_action`: your own action in the previous round

Decision rule for round `t`:

1. **Round 1**
   - Play `D`.

2. **If `t = r` (last round)**
   - Play `C` if `O_t = m-1`
   - Otherwise play `D`

3. **For rounds `2` through `r-1`**
   - If `O_t >= m`:
     - Play `D`
     - Set `miss_streak = 0`
   - Else if `O_t = m-1`:
     - Play `C`
     - Set `miss_streak = 0`
   - Else if `O_t <= m-2`:
     - If `miss_streak >= 1`:
       - Play `C` for this round only as a probe
       - Set `miss_streak = 0`
     - Otherwise:
       - Play `D`
       - Set `miss_streak = 1`

4. **After any round you played `C` and `O_t <= m-2`**
   - Treat that as a failed cooperation and immediately set `miss_streak = 1`

Operational interpretation:
- Defect whenever the others already meet the threshold without you.
- Cooperate whenever you are exactly the pivotal player needed to reach the threshold.
- After a short run of failed attempts, make a single probe cooperation to test whether the group has moved close enough to make cooperation pivotal again.
- Reset to defecting as soon as the opponents’ observed cooperation rises to `m` or more.
'''

description_OPPORTUNISTIC_12 = '''
Round 1: play D.

For round t > 1, let h_{t-1} be the number of opponents who cooperated in the previous round, and let \bar{h}_{t-1} be the average of the last up to three observed h-values.

Play C iff at least one of these holds:

1. h_{t-1} = m - 1
2. t > r - 2 and \bar{h}_{t-1} \ge m - 1
3. h_{t-1} = m - 2 and h_{t-2} \ge m - 1

Otherwise play D.

Additional edge handling:

- If m = 2, condition 1 becomes “exactly one opponent cooperated last round,” and condition 3 is ignored unless a second prior observation exists.
- If fewer than two past rounds exist, evaluate only the conditions that can be computed from available history.
- In the final round, apply the same rule, but if h_{t-1} \ge m, play D unconditionally; if h_{t-1} = m - 1, play C unconditionally.

Behavioral intent:
- Defect by default.
- Cooperate only when a single-step contribution is likely to be pivotal or when the game is near its end and recent cooperation is already clustered near the threshold.
- Exploit rounds where others have already carried the group close enough, but do not spend cooperation on rounds that are not near support.
'''

description_OPPORTUNISTIC_13 = '''
Maintain an estimate of how many opponents will cooperate next round, using the most recent rounds.

Decision rule for round t:

1. Let `x_t` be the number of opponents who cooperated in round `t-1`.
2. Let `μ_t` be the average of the last up to three observed opponent-cooperation counts:
   - if fewer than three observations exist, use the average of all available observations.
3. Set `forecast = round(μ_t)`.

Then play:

- If `forecast >= m`: play `D`
- If `forecast == m - 1`: play `C`
- If `forecast <= m - 2`: play `D`

Edge cases:

- Round 1: play `D`
- If there is only one round of history, use that single observed count as `forecast`
- In the final two rounds, use the same rule without changing it; do not switch to cooperation unless the forecast is exactly `m - 1`
- If the last three observations are strictly increasing and the most recent one is `m - 2`, play `C` once as a test for threshold recovery; otherwise keep playing `D`

State update:

- After each round, store the observed opponent-cooperation count
- Recompute `μ_t` from the most recent observations before each new move

Operational posture:

- Defect whenever the threshold appears already reachable without your contribution
- Cooperate only when your move is the pivotal one needed to turn a near-threshold round into a successful one
- If the group repeatedly fails by more than one cooperator, stay on `D` until the observed counts move back to `m - 1` or higher
'''

description_OPPORTUNISTIC_14 = '''
Let \(c_{t-1}\) be the number of opponents who cooperated in round \(t-1\), and let \(h_t\) be the cumulative number of rounds among \(1,\dots,t-1\) in which the observed total cooperators among all players was at least \(m\). Let \(T_t\) be the number of remaining rounds after round \(t\).

Use this rule:

1. **Round 1**
   - If \(m = 2\): play **C**.
   - Otherwise: play **D**.

2. **Rounds 2 through \(r-1\)**
   - Let \(x_{t-1}\) be the total cooperators observed in round \(t-1\), including yourself.
   - Play **C** iff both conditions hold:
     - \(x_{t-1} \ge m\)
     - \(c_{t-1} \ge m-1\)
   - Otherwise play **D**.

3. **Endgame from the last three rounds**
   - If \(t = r-2\), \(r-1\), or \(r\), play **C** only if:
     - the threshold was met in at least half of the previous rounds, and
     - the immediately preceding round met the threshold, and
     - at least \(m-1\) opponents cooperated in the immediately preceding round.
   - Otherwise play **D**.

Operationally, this means:

- **Cooperate immediately after a successful round** only if the observed cooperative level is already sufficient to make threshold success likely to continue.
- **Defect after any failed round** until a successful round reappears.
- **In the final rounds, become stricter** and cooperate only when recent behavior strongly indicates the threshold will be met again.

Tie-breaking and edge cases:
- If the previous round was unobserved for any reason, play **D**.
- If exactly \(m-1\) opponents cooperated last round and you cooperated too, keep cooperating next round only if the threshold was met.
- If the threshold was met last round but you defected and the group still succeeded, continue defecting unless success persists for two consecutive observed rounds.
- If the threshold was missed two rounds in a row, defect until a successful round occurs.

Compact pseudocode:

```text
if t == 1:
    if m == 2: play C
    else: play D
else:
    if t >= r-2:
        if previous_round_met_threshold and
           previous_round_opponents_coop >= m-1 and
           successful_rounds_so_far >= ceil((t-1)/2):
            play C
        else:
            play D
    else:
        if previous_round_met_threshold and previous_round_opponents_coop >= m-1:
            play C
        else:
            play D
```

This makes cooperation contingent on recent evidence that the group can still clear the threshold, while defaulting to defection whenever that evidence disappears.
'''

description_OPPORTUNISTIC_15 = '''
Start by defecting once, then treat cooperation as a conditional investment that is made only when the observed crowd is already close enough to success that your contribution is likely to be pivotal.

Maintain a running estimate of the group’s cooperative level from the last few rounds, weighted toward the most recent round:

- Let `o_t` be the number of opponents who cooperated in round `t`.
- Let `S_t` be the smoothed estimate after round `t`:
  - `S_t = 0.7 * o_t + 0.3 * S_{t-1}`
  - Initialize `S_0 = 0`

Decision rule for round `t`:

1. **Round 1**
   - Play `D`.

2. **Rounds 2 through r-1**
   - Compute `needed = m - 1`, the number of cooperating opponents you need to see so that your own cooperation can help reach the threshold.
   - Let `near = o_{t-1} >= needed - 1`.
   - Let `stable = S_{t-1} >= needed - 0.5`.
   - Cooperate if either:
     - `o_{t-1} >= needed` and `stable` is true, or
     - `o_{t-1} == needed - 1` and the previous round’s total cooperation was nondecreasing, i.e. `o_{t-1} >= o_{t-2}` when `t >= 3`.
   - Otherwise play `D`.

3. **Last round**
   - Cooperate only if the previous round showed a high-probability success pattern:
     - `o_{r-1} >= needed`
     - and `S_{r-1} >= needed`
   - Otherwise play `D`.

Adaptive adjustments:

- **If the threshold was met in the last round**
  - Increase willingness to cooperate next round only if the success margin was small:
    - If `o_{t-1} == m - 1` among opponents, cooperate next round.
    - If `o_{t-1} >= m`, cooperate next round only if `S_{t-1}` remains at least `m - 1`.
- **If the threshold failed in the last round**
  - Defect in the next round unless the failure was by exactly one opponent and cooperation has been trending upward for two consecutive observed rounds:
    - `o_{t-1} == m - 2`
    - `o_{t-2} < o_{t-1}` when available

Edge cases:

- **If `m == 2`**
  - Cooperate from round 2 onward whenever at least one opponent cooperated in the previous round and the smoothed estimate is at least `1`.
- **If `n == m + 1`**
  - Be especially responsive: cooperate whenever the previous round had exactly `m - 1` cooperating opponents and the trend is nondecreasing.
- **If no opponent has cooperated in the last two rounds**
  - Play `D` until a round shows at least `m - 2` cooperating opponents.
- **If cooperation is consistently above threshold**
  - Continue cooperating, but require the smoothed estimate to stay at or above `m - 1` to avoid drifting into costly overcommitment.

Operational form:

```text
Round 1: D

For round t = 2 to r:
    observe o_{t-1}
    update S_{t-1}

    if t == r:
        if o_{r-1} >= m-1 and S_{r-1} >= m:
            play C
        else:
            play D
    else:
        if o_{t-1} >= m-1 and S_{t-1} >= m-0.5:
            play C
        else if o_{t-1} == m-2 and t >= 3 and o_{t-2} <= o_{t-1}:
            play C
        else:
            play D
```

This makes cooperation contingent on visible momentum toward success, while defaulting to defection whenever the group is not already close enough to clear the threshold.
'''

description_OPPORTUNISTIC_16 = '''
- Track `o_t`, the number of opponents who cooperated in round `t`.
- Let `window(t)` be the last up to 3 observed rounds, most recent included.

Decision rule:

1. **Round 1:** play `D`.
2. **Rounds 2 to r-1:**  
   Play `C` only if both conditions hold:
   - the most recent observed opponent count is exactly `m-1`, and
   - at least 2 of the rounds in `window(t-1)` had opponent cooperation count `>= m-1`.

   Otherwise play `D`.

3. **Last round `r`:**  
   Play `C` only if the same condition above holds using history through round `r-1`; otherwise play `D`.

Pseudocode:

```text
if t == 1:
    action = D
else:
    recent = last up to 3 values of o
    support = count(x >= m-1 for x in recent)
    if o[t-1] == m-1 and support >= 2:
        action = C
    else:
        action = D
```

Edge handling:
- If there are fewer than 3 past rounds, use all available past rounds.
- If the most recent observed opponent cooperation count is `>= m`, always play `D`.
- If the most recent observed opponent cooperation count is `<= m-2`, always play `D`.
- If the group has shown a stable pattern of `m-1` or more cooperating opponents, keep cooperating only when your cooperation is likely to be pivotal; otherwise defect and free-ride.

Behavioral posture:
- Default to `D`.
- Switch to `C` only in rounds where the observed pattern suggests your cooperation can likely unlock the collective reward with minimal commitment.
'''

description_OPPORTUNISTIC_17 = '''
Let \(h_t\) be the number of cooperators you observed among the other \(n-1\) players in round \(t\), and let \(S_t\) be the number of rounds up to \(t\) in which you observed at least \(m-1\) cooperators among the others.

Maintain two running quantities:

- \(A_t\): recent cooperation average among opponents, computed over the last \(\ell=\min(3,t-1)\) rounds:
  \[
  A_t=\frac{1}{\ell}\sum_{j=t-\ell}^{t-1} h_j
  \]
- \(B_t\): frequency of “near-threshold” rounds in the same window:
  \[
  B_t=\frac{1}{\ell}\sum_{j=t-\ell}^{t-1}\mathbf{1}[h_j\ge m-1]
  \]

Decision rule for round \(t\):

1. **Round 1**
   - Cooperate if \(m=2\).
   - Defect if \(m>2\).

2. **Rounds 2 to \(r-2\)**
   - Cooperate if both conditions hold:
     - \(h_{t-1}\ge m-1\)
     - either \(A_t\ge m-1\) or \(B_t\ge \tfrac{2}{3}\)
   - Defect otherwise.

3. **Rounds \(t\) where \(2\le t\le r-2\) and the last two rounds were strong**
   - If \(h_{t-1}\ge m-1\) and \(h_{t-2}\ge m-1\), cooperate immediately unless the last three rounds contain a collapse:
     \[
     \exists j\in\{t-3,t-2,t-1\}\text{ with }h_j< m-2
     \]
     In that case defect.

4. **Penultimate round \(t=r-1\)**
   - Cooperate if at least one of the following is true:
     - \(h_{r-2}\ge m-1\) and \(h_{r-3}\ge m-1\)
     - \(A_{r-1}\ge m-1\)
   - Otherwise defect.

5. **Final round \(t=r\)**
   - Cooperate only if the last two observed rounds were both strong:
     \[
     h_{r-1}\ge m-1 \quad \text{and}\quad h_{r-2}\ge m-1
     \]
   - Otherwise defect.

Fallback rule:

- If no history exists yet or history is too short for the rule above, cooperate only when the observed trend is already clearly supportive:
  \[
  h_{t-1}\ge m-1
  \]
  otherwise defect.

Opportunistic adjustment:

- After any round with \(h_t\ge m-1\), stay in cooperation mode as long as the next observation does not fall below \(m-2\).
- After any round with \(h_t\le m-3\), switch immediately to defection mode for the next two rounds.
- After a single borderline round \(h_t=m-2\), keep your current mode unchanged.

Compact pseudocode:

```text
if t == 1:
    play C if m == 2 else D
else:
    recent = last min(3, t-1) observed h values
    A = average(recent)
    B = fraction of recent with h >= m-1

    if t == r:
        play C if h[t-1] >= m-1 and h[t-2] >= m-1 else D

    else if t == r-1:
        play C if (h[t-1] >= m-1 and h[t-2] >= m-1) or (A >= m-1) else D

    else if h[t-1] >= m-1 and h[t-2] >= m-1:
        play D if any of h[t-1], h[t-2], h[t-3] <= m-3 else C

    else if h[t-1] >= m-1 and (A >= m-1 or B >= 2/3):
        play C
    else:
        play D
```

State interpretation:

- Treat cooperation as the default only when opponents are repeatedly close to or above the threshold.
- Treat defection as the default whenever the observed crowd slips away from threshold support.
- Escalate into cooperation quickly after two consecutive strong rounds.
- Exit cooperation quickly after a sharp drop.
'''

description_OPPORTUNISTIC_18 = '''
Round 1: play D.

For each later round t > 1, let x be the number of opponents who cooperated in round t−1.

Decision rule:
- If x ≥ m: play D.
- If x = m−1:
  - play C only if either t = 2 or the opponents also had at least m−1 cooperators in round t−2;
  - otherwise play D.
- If x < m−1: play D.

Maintain the same rule in every round, including the last round.

Operationally:
- Defect whenever the threshold was already reached without you.
- Cooperate only when your cooperation is the minimal missing piece to cross the threshold, and only after that near-threshold pattern has repeated.
- Never cooperate when it cannot help reach the threshold.
'''

description_OPPORTUNISTIC_19 = '''
Let:

- `h_t` = number of opponents who cooperated in round `t`
- `S_t` = sum of `h` over the last `w` rounds, with `w = min(3, t-1)`
- `A_t = floor(S_t / w)` when `w > 0` else `0`
- `deficit_t = max(0, m - 1 - A_t)`

Decision rule for round `t`:

1. **Round 1**
   - Play `D`.

2. **Rounds 2 through r-1**
   - Play `C` if and only if:
     - `A_t >= m - 1`, or
     - `A_t = m - 2` and `h_{t-1} >= m - 2`, or
     - `h_{t-1} >= m - 1`
   - Otherwise play `D`.

3. **Last round `r`**
   - Play `C` if and only if:
     - `h_{r-1} >= m - 1`, or
     - `A_r >= m - 1`, or
     - `h_{r-1} = m - 2` and `A_r >= m - 2`
   - Otherwise play `D`.

4. **Fallback tie-break**
   - If the rule above is ambiguous because multiple clauses apply, choose `D`.

Reactive update after each round:

- If `h_t >= m - 1`, treat the environment as support-sufficient:
  - Defect in the next round unless you are one cooperative contribution short of making the threshold likely again.
- If `h_t <= m - 3`, treat the environment as support-poor:
  - Defect in the next round.
- If `h_t = m - 2`, probe once by cooperating in the next round only if the previous two rounds had at least one support-sufficient round; otherwise defect.

Long-run pattern:

- Cooperate only in rounds where your contribution is likely to be pivotal or where recent history shows the group is already near the threshold.
- Defect immediately after any round in which the observed opponent cooperation comfortably exceeds the threshold buffer.
- Never commit to repeated cooperation without recent evidence that opponents are sustaining cooperation.
'''

description_OPPORTUNISTIC_20 = '''
Let `x_t` be the number of opponents who cooperated in round `t`.

Maintain two running signals from the history:

- `p_t` = average of `x` over the last up to 3 rounds
- `trend_t` = `x_t - x_{t-1}` when `t ≥ 2`

Decision rule:

1. **Round 1:** Cooperate.

2. **Rounds 2 through r-1:**
   - **Cooperate** if any of the following holds:
     - `x_{t-1} ≥ m - 1` and `p_{t-1} ≥ m - 1`
     - `x_{t-1} = m - 2` and `trend_{t-1} ≥ 0`
     - `x_{t-1} = m - 1` and `x_{t-2} ≥ m - 2`
   - **Defect** otherwise.

3. **Last round (`t = r`):**
   - **Cooperate** iff `x_{r-1} ≥ m - 2`
   - **Defect** otherwise

Behavioral interpretation:

- Cooperate when the observed coalition is close to the threshold and either stable or improving.
- Defect when the observed coalition is comfortably below the threshold, or when the threshold is already being met without a clear need for your contribution.
- Use the first round to probe the field, then switch to conditional support only when cooperation appears capable of sustaining the threshold.

Edge cases:

- If `r = 2`, skip all averaging and use:
  - Round 1: C
  - Round 2: C if `x_1 ≥ m - 2`, else D
- If `m = 2`, cooperate whenever at least one opponent cooperated in the previous round and the count did not drop.
- If `m = n - 1`, cooperate only when prior rounds show near-universal cooperation (`x_{t-1} ≥ n - 3`) or on the final round when `x_{r-1} ≥ n - 3`.
'''

description_OPPORTUNISTIC_21 = '''
Let \(s_t\) be the number of opponents who cooperated in round \(t\), and let

\[
H_t=\sum_{j=1}^{t} s_j
\]

be the cumulative number of opponent cooperations observed up to round \(t\).

Define:

- \(q_t = \frac{H_t}{t(n-1)}\): observed opponent cooperation rate through round \(t\)
- \(e_t = \lceil (n-1)q_t \rceil\): predicted number of cooperating opponents in the next round
- \(L_t = m - 1 - e_t\): minimum number of my own cooperation actions needed to make the threshold likely in the next round

Decision rule in round \(t+1\) for \(t \ge 1\):

1. **If \(t = r\)**  
   Play **D**.

2. **If the threshold was met in round \(t\)**, meaning \(s_t + \mathbf{1}\{ \text{you played C in } t\} \ge m\):  
   Play **D** in round \(t+1\) unless both conditions hold:
   - \(s_t \le m-2\)
   - \(q_t < \frac{m-1}{n-1}\)

   If both conditions hold, play **C**.

3. **If the threshold failed in round \(t\)**, meaning \(s_t + \mathbf{1}\{ \text{you played C in } t\} < m\):  
   Play **C** in round \(t+1\) if and only if
   \[
   e_t \ge m-1.
   \]
   Otherwise play **D**.

4. **Pivotal opportunism rule**  
   If your action can plausibly flip the round outcome, cooperate only when:
   \[
   e_t = m-1
   \]
   and defect otherwise.

5. **Endgame rule**  
   For the final two rounds:
   - In round \(r-1\), play **C** only if \(q_{r-2} \ge \frac{m-1}{n-1}\).
   - In round \(r\), play **D**.

6. **First round**
   - If \(m = n-1\), play **C**.
   - Otherwise, play **D**.

Compact form:

- **Round 1:** \(C\) only when the threshold is nearly maximal; otherwise \(D\).
- **Middle rounds:** cooperate only when recent history makes the next-round threshold plausibly reachable without relying on you being exploited.
- **After a successful round:** immediately revert to \(D\), unless recent cooperation has been just below the threshold and one more push is still likely to keep success going.
- **Final round:** always \(D\).
'''

description_OPPORTUNISTIC_22 = '''
Use a pivot rule.

Maintain the last observed number of cooperating opponents, and a short memory of whether the group has been repeatedly close to the threshold.

Decision rule for round t:

- Round 1: play D.
- Round 2 and onward:
  - If the previous round’s opponent cooperation count was at least m, play D.
  - If the previous round’s opponent cooperation count was exactly m - 1, play C.
  - If the previous round’s opponent cooperation count was at most m - 2:
    - play C only if at least two of the last three rounds had opponent cooperation count exactly m - 1;
    - otherwise play D.

Pseudocode:

```text
if t == 1:
    action = D
else:
    if opp_coops[t-1] >= m:
        action = D
    else if opp_coops[t-1] == m - 1:
        action = C
    else:
        if count_{j in {t-3,...,t-1}}(opp_coops[j] == m - 1) >= 2:
            action = C
        else:
            action = D
```

Edge handling:

- If there is no history yet, default to D.
- If fewer than three past rounds exist, apply the “two of the last three” condition to all available past rounds.
- In the final round, use the same rule; do not switch to unconditional cooperation or unconditional defection.

Behavioral posture:

- Defect whenever the group is already meeting the threshold without needing you.
- Cooperate only when the recent history suggests you are the pivotal player who can push the group over the threshold, or when the group has been hovering just below the threshold and your cooperation is the most likely catalyst.
'''

description_OPPORTUNISTIC_23 = '''
Initialize with D.

For each round \(t\):

1. Let \(x_{t-1}\) be the number of opponents who cooperated in the previous round.
2. Let \(\bar x_t\) be the average of the opponent-cooperation counts observed so far, excluding round \(t\).

Decision rule:
- Cooperate only if both conditions hold:
  - \(\bar x_t \ge m-1\)
  - \(x_{t-1} \ge m-2\)
- Otherwise defect.

Edge cases:
- Round 1: defect.
- Round 2: cooperate only if round 1 had exactly \(m-1\) cooperating opponents; otherwise defect.
- Last round: apply the same rule; do not change behavior just because the game is ending.
- If the previous round met or exceeded the threshold by 2 or more cooperators, defect immediately in the next round.
- If the previous round was below \(m-2\), defect until the moving average returns to at least \(m-1\).

Operational version:

```text
Round 1:
    play D

Round t > 1:
    if average(opponent cooperations observed so far) >= m-1
       and previous round opponent cooperation count >= m-2
       and previous round opponent cooperation count <= m:
           play C
    else:
           play D
```

If the previous round showed exactly \(m-1\) cooperating opponents, cooperate next round to try to capture the threshold reward. If the previous round showed \(m\) or more cooperating opponents, defect and free-ride. If the previous round was far below threshold, defect.
'''

description_OPPORTUNISTIC_24 = '''
Initialize:
- `mode = probing`
- `stable = 0`
- `streak = 0`

For round `t = 1`:
- Play `D`.

For each round `t > 1`, after observing `o_{t-1}` cooperating opponents in the previous round:

1. Update the state:
   - If `o_{t-1} + my_action_{t-1} >= m`, set `streak += 1`; otherwise set `streak = 0`.
   - If `o_{t-1} >= m`, set `stable += 1`; otherwise set `stable = 0`.

2. Decision rule for round `t`:
   - If `t = r`, play `D`.
   - Else if `o_{t-1} >= m`, play `D`.
   - Else if `o_{t-1} = m - 1`, play `C`.
   - Else if `stable >= 2` and `o_{t-1} >= m - 2`, play `C`.
   - Else if `streak >= 2` and `o_{t-1} >= m - 2`, play `C`.
   - Else play `D`.

Refinement for the `m - 1` case:
- If `o_{t-1} = m - 1`, cooperate only once, then revert to `D` in the next round unless the threshold was still met without you.

Refinement for late rounds:
- For `t = r - 1`, use the same rule as above.
- For `t = r`, always defect.

Compact form:
- `C` only when the previous round showed the threshold was either:
  - already almost secured by others (`o_{t-1} = m - 1`), or
  - repeatedly close enough to expect a high chance of success (`stable >= 2` or `streak >= 2` with `o_{t-1} >= m - 2`).
- Otherwise `D`.

Operational behavior:
- Start by withholding cooperation.
- Let others prove they can sustain the threshold.
- Contribute only to push a near-success over the line.
- Immediately switch back to `D` whenever the threshold is comfortably met by others alone.
- Never spend cooperation in the final round.
'''

description_OPPORTUNISTIC_25 = '''
Let \(h_t\) be the number of opponents who cooperated in round \(t\), and let \(H_{t-1}=(h_1,\dots,h_{t-1})\) be the observed history before round \(t\).

Define:
- \(s_{t-1} = \sum_{j=1}^{t-1} h_j\): total observed opponent cooperation so far
- \(\bar h_{t-1} = s_{t-1}/(t-1)\) for \(t>1\): average opponent cooperation
- \(q_{t-1}\): recent cooperation level, the average of the last \(\min(3,t-1)\) observations
- \(T = m-1\): the number of cooperating opponents needed to make your own cooperation pivotal

Decision rule for round \(t\):

1. First round:
   - Cooperate if \(m \le 2\).
   - Defect if \(m > 2\).

2. If \(t>1\), compute:
   - \(\text{stable} = 1\) if \(q_{t-1} \ge T\), else \(0\)
   - \(\text{rising} = 1\) if \(h_{t-1} \ge T-1\) and \(h_{t-2} < T-1\) when \(t>2\), else \(0\)
   - \(\text{falling} = 1\) if \(h_{t-1} < T-1\) and \(h_{t-2} \ge T-1\) when \(t>2\), else \(0\)

3. Cooperate iff at least one of the following holds:
   - \(\bar h_{t-1} \ge T\)
   - \(q_{t-1} \ge T\)
   - \(\text{rising} = 1\)

4. Defect iff all of the following hold:
   - \(\bar h_{t-1} < T\)
   - \(q_{t-1} < T\)
   - \(\text{rising} = 0\)

5. Opportunistic escalation:
   - If \(h_{t-1} \ge T\), cooperate in round \(t\), even if the average history is below \(T\).
   - If \(h_{t-1} = T-1\) and \(h_{t-2} \ge T\), cooperate in round \(t\).

6. Opportunistic withdrawal:
   - If \(h_{t-1} \le T-2\) for two consecutive rounds, defect until a round occurs with \(h_{t-1} \ge T-1\).
   - If \(\bar h_{t-1} < T-1\), defect.

7. Last-round rule:
   - If \(t=r\), cooperate only if \(h_{r-1} \ge T\) or the last three rounds all satisfied \(h_j \ge T-1\).
   - Otherwise defect.

8. Final-phase rule:
   - For \(t \ge r-2\), cooperate only if at least two of the last three observed rounds had \(h_j \ge T\).
   - Otherwise defect.

Compact pseudocode:

```text
if t == 1:
    if m <= 2: play C
    else: play D
else:
    recent = average of last min(3, t-1) values of h
    avg = average of all past h
    if (h[t-1] >= m-1) or (recent >= m-1) or (avg >= m-1):
        play C
    else if (t > 2 and h[t-1] >= m-2 and h[t-2] < m-2):
        play C
    else:
        play D

if t >= r-2:
    if not at least two of last three h-values are >= m-1:
        play D

if t == r:
    if h[r-1] >= m-1 or last three h-values all >= m-2:
        play C
    else:
        play D
```

Behavioral core:
- Start cautiously unless the threshold is very low.
- Cooperate when opponent cooperation is consistently close to or above the threshold.
- Exploit clear coordination by cooperating while the group is already meeting the threshold.
- Defect immediately when cooperation drops well below the threshold.
- Tighten the criterion near the end so cooperation is reserved for already-established collective success.
'''

description_OPPORTUNISTIC_26 = '''
Use a two-mode policy: probe early, then switch to the cheapest action that still lets you capture the threshold reward whenever others are likely to deliver it.

Let:
- `t` = current round, `1..r`
- `H` = history of observed numbers of opponent cooperators in previous rounds
- `q` = estimated cooperation level among the other `n-1` players, computed as the average observed opponent cooperators per round divided by `n-1`

Decision rule:

1. First round
- Play `D` unless `m = n - 1`, in which case play `C`.
- If `m = n - 1`, your own cooperation is often pivotal, so contribute immediately.

2. Ongoing estimate
- After each round `t > 1`, compute:
  - `q = average(H) / (n - 1)`
- Let `L = ceil(m - 1)`? More usefully, define the expected number of cooperating opponents as:
  - `E = q * (n - 1)`

3. Main decision rule
- Play `D` if `E >= m`
- Play `C` if `E <= m - 2`
- If `m - 2 < E < m`, use a tie-break based on position in the game:
  - If `t <= floor(r/2)`, play `D`
  - If `t > floor(r/2)`, play `C`

4. Opportunistic override
- If in any previous round the threshold was met with `D` while at least `m` others cooperated, then prioritize `D` in future rounds whenever the estimated number of cooperating opponents is still at least `m`.
- If in any previous round the threshold failed because cooperation was close but short by exactly 1, and your own cooperation would have made the threshold, then play `C` in the next round whenever the same pattern reappears:
  - observed opponents cooperating = `m - 1`
  - recent rounds show no sharp decline in cooperation
  - you were among the few who had cooperated in those near-miss rounds, or the shortfall was small and stable

5. Last-round rule
- In round `r`, play `D` unless the estimated number of cooperating opponents is at most `m - 2`.
- If the threshold is expected to fail anyway, defect.
- If your cooperation is likely to be pivotal for reaching `m`, cooperate.

6. Rare-cooperation fallback
- If `H` shows that the threshold has been met in fewer than 25% of completed rounds, play `D` except when:
  - `m = n - 1`, or
  - the last two rounds each showed exactly `m - 1` cooperating opponents
- In those cases, play `C` once to test whether the group is near coordination.

7. Stable-cooperation exploitation
- If the threshold has been met in at least 3 consecutive rounds, play `D` until the observed number of cooperating opponents drops below `m - 1`.
- Once it drops, switch to `C` only if your cooperation is needed to restore the threshold; otherwise remain on `D`.

8. Simple implementation form

```text
if t == 1:
    if m == n - 1: play C
    else: play D
else:
    E = average(previous opponent cooperators)
    if E >= m:
        play D
    elif E <= m - 2:
        play C
    else:
        if t <= r/2:
            play D
        else:
            play C

    if last round had opponents cooperating >= m and your own C was not needed:
        force D
    if last round had opponents cooperating == m - 1 and threshold failed:
        force C next round
```

9. Final principle
- Cooperate only when your action is likely to be pivotal for reaching `m`.
- Otherwise defect and collect the private payoff while others supply the threshold.
'''

description_OPPORTUNISTIC_27 = '''
**Opportunistic Threshold-Shadow Strategy**

Maintain one state variable:

- `F`: observed cooperation count among opponents in the previous round
- `S`: a running score that tracks whether the table is currently supportable
  - initialize `S = 0`

### Decision rule each round `t`

1. **First round**
   - Play `D`.

2. **After round `t-1`, observe `F`**
   - Update:
     - if `F >= m - 1`, set `S = min(S + 1, 3)`
     - else set `S = max(S - 1, -3)`

3. **Choose action for round `t`**
   - **Play `C`** if both conditions hold:
     - `F >= m - 1`
     - `S >= 1`
   - **Otherwise play `D`**

### Last-round behavior
- On the final round, play `C` only if:
  - `F >= m - 1`
  - `S >= 2`
- Otherwise play `D`

### Recovery rule after a collapse
- If `F < m - 1` in any round, switch to `D` immediately in the next round.
- Remain on `D` until you observe `F >= m - 1` for **two consecutive rounds**.
- Once two consecutive supportive rounds occur, re-enter `C` for the next round.

### Opportunistic switching
- If you are currently playing `D` and the previous round shows `F >= m - 1`, treat that as a signal that cooperation is already being sustained by others.
- Enter `C` immediately on the next round if either:
  - `F >= m - 1` in the current round and `S >= 1`, or
  - it is the final round and `S >= 2`

### Momentum adjustment
- If you played `C` and the next observed `F` remains at least `m - 1`, keep cooperating.
- If you played `C` and the next observed `F` drops below `m - 1`, defect next round and reset the recovery rule.

### Compact pseudocode
```text
initialize S = 0
for round t = 1..r:
    if t == 1:
        play D
    else:
        if F >= m-1:
            S = min(S + 1, 3)
        else:
            S = max(S - 1, -3)

        if t == r:
            play C if (F >= m-1 and S >= 2) else D
        else:
            if F >= m-1 and S >= 1:
                play C
            else:
                play D
```

### Behavior summary
- Starts safely with defection.
- Joins cooperation only when the table is already close to threshold.
- Stays in cooperation while support persists.
- Exits immediately when support weakens.
- Re-enters only after evidence of sustained cooperation.
'''

description_OPPORTUNISTIC_28 = '''
**Opportunistic Threshold-Tracking Strategy**

Maintain:

- `H`: the number of cooperations you observed among opponents in each past round
- `T`: current target cooperation level among opponents
- `p`: observed cooperation frequency in recent rounds
- `s`: running score of “supportive rounds” versus “free-riding rounds”

### 1) Initial rule
**Round 1: Cooperate if and only if `m <= n-1` and `m-1` is plausibly reachable without your sacrifice.**

Operationally:

- If `m == 2`, cooperate in round 1.
- Otherwise, defect in round 1.

This makes the first move conservative except when a single cooperative signal can strongly shape the threshold outcome.

---

### 2) Core decision rule for round `t > 1`

Let `h` be the number of opponents who cooperated in round `t-1`.

Define:

- `near_threshold = (h == m-2) or (h == m-1)`
- `surplus = h >= m`
- `collapse = h <= m-3`

#### Cooperate if all of the following hold:
1. The recent pattern indicates the group is **close to meeting the threshold**:
   - `near_threshold` in the last round, or
   - at least 2 of the last 3 rounds had `h >= m-1`
2. Your cooperation is likely to be pivotal or nearly pivotal:
   - `h <= m-1`
3. The recent cooperation level is not collapsing:
   - the average of the last up to 3 `h` values is at least `m-2`

#### Defect otherwise.

---

### 3) Precise round-by-round rule

For each round `t`:

#### If `t = 1`
- Cooperate only if `m == 2`
- Otherwise defect

#### If `t >= 2`
Let `h1, h2, ..., hq` be the observed opponent cooperation counts from the last `q = min(3, t-1)` rounds.

Compute:

- `recent_avg = (h1 + ... + hq) / q`
- `close_count = number of rounds among h1..hq where h >= m-1`

Then:

- **Cooperate** if:
  - `h_(t-1) == m-1`, or
  - `h_(t-1) == m-2 and close_count >= 2`, or
  - `recent_avg >= m-1 and h_(t-1) <= m-1`
- **Defect** otherwise

---

### 4) Opportunistic adjustment rules

#### If cooperation is consistently failing
If the last 2 rounds both had `h < m-2`, defect.

#### If cooperation is consistently succeeding
If the last 2 rounds both had `h >= m`, cooperate only when `h_(t-1) <= m-1`; otherwise defect.

#### If the threshold is being met exactly
If the last observed round had `h == m-1`, cooperate in the next round.

#### If the threshold is comfortably exceeded
If the last observed round had `h >= m+1`, defect unless the last 3 rounds show a downward trend and the most recent round was `m-1` or `m-2`.

---

### 5) Last-round rule
In the final round:

- **Cooperate only if** the most recent observed round had `h >= m-1`
- Otherwise defect

This uses the final round only when the group is already positioned to clear the threshold without needing a sustained sacrifice.

---

### 6) Simple fallback version

If a compact rule is needed:

- **Round 1:** defect, except cooperate if `m == 2`
- **Rounds 2 to r-1:** cooperate if the previous round’s opponent cooperations were at least `m-1`; otherwise defect
- **Final round:** cooperate only if the previous round’s opponent cooperations were exactly `m-1` or `m`

---

### 7) State update after each round

After observing opponent cooperation count `h_t`:

- Append `h_t` to history
- If `h_t >= m-1`, increment support streak
- If `h_t <= m-3`, increment collapse streak
- Reset the opposite streak whenever the condition flips

Use the streaks to apply the core rules above.
'''

description_OPPORTUNISTIC_29 = '''
Let \(H_t\) be the history before round \(t\): the number of cooperators observed in each previous round, but not identities.

Use this rule:

**Round 1**
- Play **C**.

**From round 2 onward**
1. Compute:
   - \(s =\) number of rounds so far with at least \(m\) cooperators observed
   - \(u =\) number of rounds so far with fewer than \(m\) cooperators observed
   - \(q =\) cooperators observed in the immediately previous round

2. Set your action by the following priority order:

   **A. Exploit stable success**
   - If the last two rounds both had at least \(m\) cooperators, play **D**.
   - If the last round had at least \(m\) cooperators and \(q \ge m+1\), play **D**.

   **B. Protect ongoing coordination**
   - If the last round had exactly \(m\) cooperators, play **C**.
   - If the last round failed to reach \(m\) but the round before it reached \(m\), play **C**.
   - If the last two rounds both failed to reach \(m\), play **D**.

   **C. Recovery mode**
   - If successes are rare so far \((s \le u)\), play **C** every round until you observe one round with at least \(m\) cooperators.
   - Once a success occurs, switch back to the exploit/protect rules above.

3. **Last two rounds**
   - If \(t = r-1\), play **C**.
   - If \(t = r\):
     - play **D** if the previous round had at least \(m\) cooperators;
     - otherwise play **C**.

**Compact pseudocode**
```text
if t == 1:
    action = C
else:
    s = count(history rounds with coop >= m)
    u = (t-1) - s
    q1 = coop count in round t-1
    q2 = coop count in round t-2 if t >= 3 else None

    if t == r:
        action = D if q1 >= m else C

    else if t == r-1:
        action = C

    else if q1 >= m and q2 != None and q2 >= m:
        action = D

    else if q1 >= m and q1 >= m+1:
        action = D

    else if q1 == m:
        action = C

    else if q1 < m and q2 != None and q2 >= m:
        action = C

    else if q1 < m and q2 != None and q2 < m:
        action = D

    else if s <= u:
        action = C

    else:
        action = C if q1 < m else D
```

**Behavioral logic**
- Start by signaling willingness to cooperate.
- Stay cooperative when cooperation is just barely holding the threshold, because one defection can collapse it.
- Defect immediately when cooperation is comfortably above threshold, since that is the opportunistic window.
- After repeated failures, stop bleeding value into a dead round and wait for a new attempt.
- In the final rounds, favor cooperation unless the threshold is already clearly secured, then defect on the very last round.
'''

description_OPPORTUNISTIC_30 = '''
Use a threshold-adaptive opportunist:

- Let `T = m - 1`, the largest number of observed opponent cooperators that still leaves the round below the threshold if you defect.
- Maintain a moving estimate of cooperation:
  - `s` = number of opponent cooperators in the previous round
  - `H` = list of recent `s` values, with more weight on the last few rounds
  - `base` = average of `H`, updated after each round

Decision rule each round `t`:

1. If `t = 1`, play `D`.
2. Otherwise, compute:
   - `recent = average of the last up to 3 values in H`
   - `trend = s_last - s_prev` when at least 2 past observations exist, else `0`
   - `momentum = recent >= T`
3. Cooperate only when all three hold:
   - `recent >= T`
   - `trend >= 0`
   - the previous round reached the threshold or came within 1 of it: `s_last >= T - 1`
4. Otherwise, defect.

Refinement for the final rounds:
- If `t >= r - 1`, cooperate only if the last round met the threshold and at least `m - 1` opponents cooperated in each of the last two rounds.
- If the threshold has been missed in the last two rounds, defect for the rest of the game.

Update rule after each round:
- Record the observed opponent cooperation count `s`.
- Append `s` to `H`.
- If the round met the threshold, stay willing to cooperate next round.
- If the round missed the threshold, become stricter by requiring one extra cooperative signal before cooperating again:
  - next cooperation condition becomes `recent >= T + 1` until a successful round resets it.

Behavioral pattern:
- Open with caution.
- Join cooperation immediately after repeated evidence that the group can clear the threshold.
- Defect whenever the group looks marginal, declining, or unstable.
- Exploit stable cooperative phases by cooperating only when they are already likely to succeed.
- Exit to defection quickly after any failure streak.

Pseudocode:

```text
if t == 1:
    action = D
else:
    recent = average(last up to 3 observed s values)
    trend = last_s - prev_s if enough history else 0
    success_streak = number of consecutive past rounds with s >= m-1

    if t >= r - 1:
        if success_streak >= 2 and last_s >= m-1:
            action = C
        else:
            action = D
    else:
        if failed_last_two_rounds:
            action = D
        else if recent >= m-1 and trend >= 0 and last_s >= m-2:
            action = C
        else:
            action = D

after observing s:
    update history
    if s >= m-1:
        reset failure pressure
    else:
        increase failure pressure
```

This strategy cooperates only when cooperation is already close to self-sustaining, and defects whenever the group appears too weak, unstable, or late in the game to justify contributing.
'''

description_OPPORTUNISTIC_31 = '''
Initialize:
- `mode = DEFECT`
- `near_miss_streak = 0`

Round 1:
- Play `D`.

After each round `t`, observe `x_t =` number of opponents who cooperated.
- Let `T_t = x_t + 1` if you played `C` in round `t`, else `T_t = x_t`  
  (`T_t` is the total number of cooperators in round `t`).

For round `t+1`:
1. If `t+1 = r`, play `D`.
2. Else if `T_t >= m`, play `D`.
3. Else if `T_t = m - 1` and at least one of the following holds:
   - `T_{t-1} >= m`, or
   - `T_{t-1} = m - 1`, or
   - `T_t = m - 1` for two consecutive rounds
   then play `C`.
4. Else play `D`.

Update rule after each round:
- If `T_t = m - 1`, increment `near_miss_streak`.
- Otherwise set `near_miss_streak = 0`.

Compact version:

```text
Round 1: D
Round t+1 (t < r):
    if t+1 == r: D
    else if T_t >= m: D
    else if T_t == m-1 and (T_{t-1} >= m or T_{t-1} == m-1): C
    else D
```

Behavioral principle:
- Defect whenever the threshold already appears secured or hopelessly out of reach.
- Cooperate only on a one-player shortfall that repeats, so you step in exactly when your contribution is likely to rescue the group while avoiding unnecessary sacrifice.
'''

description_OPPORTUNISTIC_32 = '''
Maintain a running estimate of how many opponents will cooperate next round, using only the observed opponent-cooperation counts from prior rounds.

Decision rule for round t:

1. Compute `s̄_t`, the average of opponent cooperation counts observed in the last `L = min(3, t-1)` rounds.
2. Let `p_t = round(s̄_t)`.

Action:
- If `p_t >= m`: play `D`.
- If `p_t == m - 1`: play `C`.
- If `p_t <= m - 2`: play `D`.

Edge handling:
- Round 1: play `D`.
- If the last round had exactly `m - 1` opponent cooperators, cooperate in the next round.
- If the last two rounds both had at least `m - 1` opponent cooperators, defect on the next round unless `p_t = m - 1` and you are the single marginal contributor needed to keep the group at the threshold.
- If the last round met or exceeded the threshold by a wide margin, defect until the observed average falls back to `m - 1`.

Optional memory update:
- Keep a “near-threshold streak” counter `q`.
- Increment `q` when observed opponent cooperators are at least `m - 1`; reset `q` otherwise.
- Cooperate only when `q >= 2` and the current estimate is exactly `m - 1`; otherwise defect.

Compact pseudocode:

```text
if t == 1:
    action = D
else:
    sbar = average(last min(3, t-1) observed opponent-coop counts)
    p = round(sbar)

    if p == m - 1:
        action = C
    else:
        action = D
```
'''

description_INDIVIDUALISTIC_5 = '''
Always defect.

Decision rule:
- In every round t = 1, 2, ..., r, choose D regardless of the past, the number of cooperators observed in previous rounds, or the round number.

History handling:
- Record the observed number of cooperators after each round.
- Never let past cooperation change your action.
- Do not attempt reciprocity, punishment, escalation, or late-game cooperation.

Edge cases:
- First round: play D.
- Any round with exactly m - 1 other cooperators observed in prior rounds or any other count: play D.
- Last round: play D.
- If the history shows everyone cooperated before, play D.
- If the history shows everyone defected before, play D.

Individualistic posture:
- Treat cooperation by others as a source of gain to be observed, not matched.
- Preserve your private payoff every round by keeping the endowment and never contributing it.
'''

description_INDIVIDUALISTIC_6 = '''
Play D in every round.

Pseudocode:
```text
for t = 1 to r:
    choose D
```

Decision rule:
- First round: defect.
- Middle rounds: defect, regardless of how many opponents cooperated last round.
- Last round: defect.

History use:
- Record observed cooperation counts if desired, but never let them change the action.
- If any internal tie-break is needed, default to D.

Edge cases:
- If everyone else cooperated last round: defect.
- If nobody cooperated last round: defect.
- If cooperation has been frequent, sparse, stable, or erratic: defect.
- If the game is nearing the final rounds and a shift would be possible: still defect.
'''

description_INDIVIDUALISTIC_7 = '''
Let \(x_t\) be the number of opponents who cooperated in round \(t\), so total cooperators would be \(x_t+1\) if you choose \(C\), and \(x_t\) if you choose \(D\).

Maintain:
- \(h_t\): the average of observed opponent cooperation counts over the last \(L\) rounds, where \(L=\min(3,t-1)\)
- \(s_t\): the number of rounds in the last \(L\) rounds where \(x_j = m-1\)

Decision rule for round \(t\):

1. If \(t=1\), play \(D\).

2. If \(x_{t-1} \ge m\), play \(D\).
   - The threshold was already met without your help; do not spend the endowment.

3. If \(x_{t-1} = m-1\) and either
   - \(s_t \ge 2\), or
   - \(h_t \ge m-1\),
   
   then play \(C\).

4. Otherwise, play \(D\).

Equivalent compact form:

```text
Round 1: D

For round t > 1:
    observe x_{t-1}

    if x_{t-1} >= m:
        play D
    else if x_{t-1} == m-1 and (count of x_j == m-1 in last min(3,t-1) rounds >= 2
                                 or average of last min(3,t-1) x_j >= m-1):
        play C
    else:
        play D
```

Edge handling:
- If \(m=2\), cooperate only after repeated rounds where exactly one opponent cooperated or the recent average is at least \(1\).
- If the game ends in round \(r\), use the same rule; there is no special terminal cooperation.
- If there is no prior history beyond round 1, default to \(D\).

Behavioral posture:
- Defect unless the observed pattern shows the group is already at, or repeatedly just below, the threshold and your contribution is likely to secure the reward.
- Never cooperate on vague optimism alone.
- Never cooperate when the threshold is already being met without you.
'''

description_INDIVIDUALISTIC_8 = '''
Round 1: play D.

For every later round t, after observing the previous round’s number of cooperating opponents h:

- If h ≥ m, play D.
- If h = m − 1, play C.
- If h ≤ m − 2, play D.

State it as a pivot rule:
- cooperate only when your cooperation is exactly the marginal move that can bring the group to the threshold;
- defect in every other case.

Edge cases:
- If m = 2, cooperate only when exactly one opponent cooperated last round.
- If m = n − 1, cooperate only when all opponents cooperated last round.
- If the previous round failed badly (h ≤ m − 2), do not “rescue” the group; wait until opponents independently demonstrate that they can supply m − 1 cooperators without you.
- In the final round, use the same rule: cooperate only if h = m − 1; otherwise defect.

If you ever cooperated and the threshold still failed, revert to D immediately next round.
If you ever cooperated and the threshold succeeded with h ≥ m, revert to D next round unless h = m − 1, in which case you may keep cooperating because your move remains pivotal.

Pseudocode:
```text
if t == 1:
    action = D
else:
    if h == m - 1:
        action = C
    else:
        action = D
```
'''

description_INDIVIDUALISTIC_9 = '''
Default to defection, and only cooperate when the recent history shows that cooperation is already close to self-sustaining.

Maintain a support streak `s`, the number of consecutive previous rounds in which the number of cooperating opponents was at least `m - 1`.

Decision rule for round `t`:

```text
If t = 1:
    play D

Else:
    let o = number of opponents who cooperated in round t-1

    if o >= m - 1:
        s = min(s + 1, 2)
    else:
        s = 0

    if s < 2:
        play D
    else if o == m - 1:
        play C
    else:
        play D
```

Interpretation of the state:
- `s < 2`: the environment has not shown enough recent support, so do not spend the endowment.
- `s >= 2` and `o == m - 1`: your cooperation is the marginal action that can keep the threshold reachable, so cooperate.
- `s >= 2` and `o >= m`: others already provide enough support, so defect and keep the private payoff.

Edge cases:
- First round: always defect.
- If the last round had fewer than `m - 1` cooperating opponents: defect until at least two consecutive rounds recover to `m - 1` or more.
- If the last round had exactly `m - 1` cooperating opponents but the preceding round did not: defect; one isolated near-threshold observation is not enough to engage.
- Last round: use the same rule as any other round; never sacrifice the final round unless the history already meets the cooperation trigger.
- If opponents are consistently above the threshold margin (`o >= m`): always defect.
- If opponents are consistently at the knife edge (`o = m - 1`): cooperate after the second such round and continue cooperating only while that condition persists.
'''

description_INDIVIDUALISTIC_10 = '''
Play D in every round.

Decision rule:
- Round 1: defect.
- Round t > 1: defect, regardless of the number of cooperators observed in earlier rounds.
- Last round: defect.
- If you ever observe fewer than m cooperators, continue defecting.
- If you ever observe m or more cooperators, continue defecting.

Internal state:
- No state update is needed.
- History is ignored except for bookkeeping; it never changes the action.

Pseudocode:
```text
for each round t:
    choose D
```
'''

description_INDIVIDUALISTIC_11 = '''
Initialize a target threshold \(T\) and an adaptive cooperation mode.

Set
\[
T_1=\max\{1,\; m-1\}
\]
and maintain a running estimate of the support level:
\[
s_t = \text{number of opponents observed cooperating in round } t.
\]

Decision rule for round \(t\):

1. **Force cooperation in the final round only if it is pivotal**
   - If \(t=r\) and \(T_t \ge m\), play \(C\).
   - Otherwise, do not use any special endgame concession.

2. **Cooperate only when the current environment is already close to success**
   - If \(t<r\), play \(C\) iff
     \[
     s_{t-1} \ge T_t
     \]
     where \(s_{t-1}\) is the observed number of cooperating opponents in the previous round.
   - Otherwise play \(D\).

3. **Update the target threshold after each round**
   - If the threshold was met in round \(t-1\), become slightly stricter:
     \[
     T_t = \min\{n-1,\; T_{t-1}+1\}
     \]
   - If the threshold was missed in round \(t-1\), become slightly more permissive:
     \[
     T_t = \max\{1,\; T_{t-1}-1\}
     \]

4. **First round**
   - Play \(D\) if \(m>2\).
   - Play \(C\) only if \(m=2\).

5. **Last round**
   - If the previous round reached the threshold with your cooperation absent or unnecessary, play \(D\).
   - If the previous round missed the threshold by exactly one and your cooperation can make the difference, play \(C\).
   - Otherwise play \(D\).

Compact version:

```text
T = max(1, m-1)

Round 1:
    if m == 2: play C
    else: play D

For round t = 2 to r:
    if t == r and T >= m:
        play C
    else if observed_cooperators_last_round >= T:
        play C
    else:
        play D

    if threshold_met_last_round:
        T = min(n-1, T + 1)
    else:
        T = max(1, T - 1)
```

Individualistic posture:
- Never cooperate just because others might.
- Cooperate only when observed support is already near the needed level or when your action is directly pivotal.
- Defect whenever the observed support is too weak.
- Adjust only from what has been publicly observed, with no attempt to coordinate, forgive, punish, or signal.
'''

description_INDIVIDUALISTIC_12 = '''
For each round, observe the number of opponents who cooperated in the previous round, and in the current round act according to the current count you expect to face from the information available at decision time:

- Let \(x\) be the number of opponents expected to cooperate this round.
- Cooperate iff \(x = m - 1\).
- Defect otherwise.

If you only have the last observed round as information, use that observed opponent-cooperation count as \(x\) for the next round.

Decision rules:
- If \(x \ge m\): defect.
- If \(x = m - 1\): cooperate.
- If \(x \le m - 2\): defect.

Edge cases:
- Round 1: defect unless you have a reliable reason from the game state to expect exactly \(m-1\) opponent cooperators; otherwise default to defect.
- Final round: use the same rule as any round; no special concession.
- If the observed opponent count is inconsistent, incomplete, or unavailable, default to defect.

History handling:
- Ignore identity and track only the most recent aggregate cooperation count.
- If the last few rounds show a stable pattern, continue using the same threshold rule; do not change behavior based on goodwill, reciprocity, or punishment.

Individualistic posture:
- Never cooperate to “help” unless your cooperation is pivotal for the threshold.
- Never cooperate when the threshold is already assured without you.
- Never cooperate when your cooperation cannot make the threshold reachable.
'''

description_INDIVIDUALISTIC_13 = '''
State variables:
- `x_t`: number of opponents who cooperated in round `t`
- `W_t`: rolling window of the last 3 observed `x` values, or all available history if fewer than 3 rounds have passed

Decision rule for round `t`:

1. **Round 1:** play `D`.

2. **Round t ≥ 2, if t = r (last round):** play `D`.

3. **Otherwise:**
   - Let `a = x_{t-1}`
   - Let `b = median(W_t)` if `|W_t| = 3`, else `b = a`

   Choose `C` iff one of the following holds:
   - `a = m - 1`
   - `a = m - 2` and `b ≥ m - 1`
   - `a > m - 1` and `a` has been at least `m - 1` in each of the last two rounds, with at least one of those rounds equal to `m - 1`

   In every other case, choose `D`.

Memory update:
- After each round, record the observed `x_t`
- Drop the oldest observation once more than 3 rounds have been recorded

Behavioral interpretation:
- Default to `D`
- Switch to `C` only when the recent history shows that cooperation is sitting right at the threshold or just below it and a small additional contribution is enough to preserve the threshold
- Revert to `D` immediately after any clear surplus of cooperators, and never cooperate in the final round
'''

description_INDIVIDUALISTIC_14 = '''
Use a default-defect, opportunistic-rescue rule.

State kept from history:
- `o[t]` = number of opponents who cooperated in round `t`
- `a[t]` = your own action in round `t`

Decision rule:

1. **Round 1:** play `D`.

2. **Rounds 2 through r-1:**
   - Play `C` only if the previous round was **exactly one short of the threshold because of the opponents alone**:
     - `o[t-1] = m - 1`
     - and your action in round `t-1` was `D`
   - In every other case, play `D`.

3. **Round r:** play `D`.

Equivalent pseudocode:

```text
if t == 1 or t == r:
    play D
else:
    if o[t-1] == m-1 and a[t-1] == D:
        play C
    else:
        play D
```

Behavioral interpretation:
- Never volunteer early.
- Never cooperate when the prior round was comfortably above or below the threshold.
- Cooperate only when the previous round showed the group was one contributor short and your own added contribution is the minimal individual move that can plausibly flip the outcome.
- Immediately revert to `D` after any cooperative rescue round.
'''

description_INDIVIDUALISTIC_15 = '''
**Individualistic Adaptive Threshold Strategy**

Let `x_t` be the number of other players observed to cooperate in round `t-1`, and let `h_t` be the history of observed cooperation counts up to round `t-1`.

### Round 1
Play `D`.

### Rounds 2 through r-1
Compute the recent cooperation rate among opponents:

- `avg = average of observed opponent cooperators over the last s rounds`
- where `s = min(3, t-1)`.

Then set:

- `need = m - 1` if you cooperate, because your own `C` adds one toward the threshold.
- `support = avg`

Decision rule:

1. **If `support >= need`**, play `C`.
2. **If `support <= need - 2`**, play `D`.
3. **If `support == need - 1`**, use a pressure rule:
   - cooperate if the last observed round had at least `need` opponents cooperating;
   - otherwise defect.

### Final round `r`
Play the action that is most likely to maximize the immediate round payoff from the observed history:

- If the average observed opponent cooperation over the last `min(5, r-1)` rounds is at least `m - 1`, play `C`.
- Otherwise play `D`.

### Update logic after each round
After observing the number of opponents who cooperated in round `t`:

- store it in the history;
- if the count is at least `m - 1`, treat that as evidence that cooperation can clear the threshold when you contribute;
- if the count is at most `m - 3`, treat it as evidence that defecting is safer.

### Tie-breaking and edge cases
- If the history is too short to compute an average, default to `D`.
- If the computed average is exactly on the boundary, default to `D` unless the immediately previous round showed clear threshold support.
- Never cooperate twice in a row unless the recent history shows that cooperation is repeatedly near or above the threshold.

### Compact pseudocode
```text
if t == 1:
    play D
else:
    s = min(3, t - 1)
    avg = average(opponent_cooperators in last s rounds)
    need = m - 1

    if t == r:
        s2 = min(5, t - 1)
        avg2 = average(opponent_cooperators in last s2 rounds)
        if avg2 >= need:
            play C
        else:
            play D
    else:
        if avg >= need:
            play C
        else if avg <= need - 2:
            play D
        else:
            if last observed opponent cooperation count >= need:
                play C
            else:
                play D
```
'''

description_INDIVIDUALISTIC_16 = '''
Round 1: play D.

For each round t = 2, ..., r-1:

- Let s be the number of opponents who cooperated in round t-1.
- Let s2 be the number of opponents who cooperated in round t-2, if available.

Decision rule:
1. If s >= m-1 and (t = 2 or s2 >= m-1), play C.
2. Else if s = m-2 and s2 = m-2 and t is a probe round, play C.
3. Otherwise, play D.

Probe rounds:
- Define probe rounds as t such that t is a multiple of 4, starting at t = 4.
- On a probe round, if s >= m-2 and the last two rounds were not strictly declining in cooperation among opponents, play C once to test whether the group is moving toward threshold.
- If the probe fails to produce s >= m-1 in the next round, return immediately to D.

Round r: play D.

Additional update rule:
- Maintain a cooperation streak counter for opponents.
- Increment the streak when s >= m-1.
- Reset it to 0 when s < m-1.
- Only cooperate when the streak is at least 2, except on probe rounds.

Edge cases:
- If m = 2, simplify the trigger to s >= 1 and streak >= 2.
- If m = n-1, cooperate only when s = n-2 for two consecutive rounds.
- If the observed cooperation count drops after you cooperated, abandon cooperation and require two fresh consecutive rounds of s >= m-1 before cooperating again.

Operational summary:
- Start with D.
- Cooperate only after sustained, visible support from others.
- Defect whenever support is absent, unstable, or the game is in its final round.
'''

description_INDIVIDUALISTIC_17 = '''
Play D by default and treat cooperation as a narrow, one-shot insurance move only when the group has shown a stable, near-threshold pattern.

State kept from history:
- `x_t`: number of opponents who cooperated in round `t`
- `need = m - 1`

Decision rule:

1. Round 1: play D.
2. Round 2: play D.
3. For rounds `3` through `r - 1`:
   - Play C iff `x_{t-1} = need` and `x_{t-2} = need`.
   - Otherwise play D.
4. Final round `r`: play D.

Interpretation:
- Cooperate only when the opponents have produced exactly the same near-threshold level for two consecutive rounds, so your contribution is the decisive extra unit.
- If opponents are already above threshold, defect and keep the private payoff.
- If opponents are below threshold or inconsistent, defect.
- Never cooperate in the last round.

If `r <= 2`, play D in every round.
'''

description_INDIVIDUALISTIC_18 = '''
State variables:
- Let `x_t` be the number of other players who cooperated in round `t`.
- Let `L = min(3, t-1)` be the lookback length available in round `t`.
- Let `avg_t` be the average of `x_{t-1}, x_{t-2}, ..., x_{t-L}`.
- Let `trend_t = x_{t-1} - x_{t-2}` when at least two past rounds exist.

Decision rule for round `t`:

1. **If `t = 1`:** play `D`.

2. **If `t = r` (last round):**
   - play `C` iff `x_{r-1} = m - 1`
   - otherwise play `D`

3. **For intermediate rounds `2 ≤ t ≤ r-1`:**
   - play `D` if `avg_t ≥ m`
   - play `C` if `avg_t = m - 1`
   - play `C` if `avg_t = m - 2` and `trend_t ≥ 1` and `x_{t-1} ≥ m - 2`
   - otherwise play `D`

State update and interpretation:
- After each round, record only the anonymous count `x_t`.
- Use the most recent rounds to estimate whether the group is already self-sustaining, exactly one short, or still too far below the threshold.
- Never cooperate when others already appear able to secure the reward without you.
- Cooperate only when your contribution is likely to be the decisive marginal one, or when the recent trend shows the group is moving into that zone.

Edge handling:
- If fewer than two prior rounds exist, omit the trend condition and use only the `avg_t` test.
- If the observed history is volatile, the rule defaults to `D`.
- If the observed count repeatedly lands at `m - 1`, keep playing `C` in those rounds; if it repeatedly exceeds `m - 1`, revert to `D`.
- If the observed count is far below `m - 1` for several rounds in a row, stay with `D` until the group moves back within one step of the threshold.
'''

description_INDIVIDUALISTIC_19 = '''
Round 1: play D.

After each round t ≥ 1, observe x_t = number of opponents who cooperated.

Maintain a smoothed cooperation estimate
\[
e_t = \alpha x_t + (1-\alpha)e_{t-1},
\]
with \(e_1 = x_1\) and \(\alpha = 1/2\).

Decision rule for round t+1:

- Let \(L = m - 1\).
- Cooperate only if both conditions hold:
  1. \(x_t = L\) or \(e_t \ge L\)
  2. the last two observations are nondecreasing: \(x_t \ge x_{t-1}\) and, if \(t \ge 3\), \(x_{t-1} \ge x_{t-2}\)

- Otherwise defect.

Edge cases:
- If \(m = 2\), cooperate only when \(x_t = 1\) and the recent trend is nondecreasing.
- If \(x_t \ge m\), always defect next round.
- If \(x_t \le m-2\), always defect next round.
- In the final round, apply the same rule; do not switch to unconditional cooperation.

Tiebreak:
- If the trend condition is mixed or unavailable because there is not enough history, defect.

Compact pseudocode:

```text
state: e = 0, history = []

round 1:
    play D

after observing x:
    e = x if history empty else 0.5*x + 0.5*e
    append x to history

    if x >= m:
        next = D
    else if x == m-1 and trend_non_decreasing(history):
        next = C
    else if e >= m-1 and trend_non_decreasing(history):
        next = C
    else:
        next = D

trend_non_decreasing(history):
    return true if len(history) < 2
    else if len(history) == 2:
        return history[-1] >= history[-2]
    else:
        return history[-1] >= history[-2] and history[-2] >= history[-3]
```

This keeps cooperation strictly conditional on being near the threshold and on evidence that others are already sustaining it; otherwise it defaults to defection.
'''

description_INDIVIDUALISTIC_20 = '''
Play D in every round.

Decision rule:
- Round 1: D
- Round t for any t > 1: D
- Ignore all observed history, including counts of cooperators in prior rounds.

Edge cases:
- If r = 1: D
- If m = 2 or m = n - 1 or any other admissible values: D
- If the observed number of cooperating opponents was high in earlier rounds: still D
- If the observed number of cooperating opponents was low in earlier rounds: still D
- In the last round: D

Individualistic policy:
- Never contribute
- Never condition cooperation on past behavior
- Treat every round as a purely private payoff choice and choose the privately dominant action each time
'''

description_INDIVIDUALISTIC_21 = '''
Initialize:

- Set `mode = DEFECT`
- Maintain `h_t =` number of opponents who cooperated in round `t`
- Maintain `E_t =` exponentially weighted estimate of future opponent cooperation, updated after each round:
  - `E_t = 0.6*h_t + 0.4*E_{t-1}` for `t > 1`
  - `E_1 = h_1`

Decision rule for round `t`:

1. **Round 1:** play `D`.

2. **Rounds 2 through r-2:**
   - Let `last = h_{t-1}`
   - Let `trend = h_{t-1} - h_{t-2}` when `t >= 3`, otherwise `trend = 0`
   - Play `C` only if all of the following hold:
     - `last == m-2`
     - `trend >= 0`
     - `E_{t-1} >= m-2`
   - Otherwise play `D`.

3. **Rounds r-1 and r:**
   - Play `C` only if both of the following hold:
     - `h_{t-1} == m-2`
     - `E_{t-1} >= m-2`
   - Otherwise play `D`.

Update rule after each round:

- Record `h_t`
- Recompute `E_t`

Edge handling:

- If `m == 2`, the cooperation condition becomes:
  - cooperate only when `h_{t-1} == 0` and `E_{t-1} >= 0`
  - otherwise defect
- If `m == n-1`, require:
  - cooperate only when `h_{t-1} == n-3` and the last two rounds were nondecreasing
- If the history is too short to compute `trend`, treat `trend = 0`

Behavioral principle:

- Never cooperate on weak evidence.
- Cooperate only when opponents are consistently close to the threshold but still one short, so your action is the smallest possible commitment that can help shift the round into the reward region.
- Otherwise defect, including any round where the threshold already appears likely to be met without your contribution.
'''

description_INDIVIDUALISTIC_22 = '''
Play D in every round.

Decision rule:
- For all rounds t = 1, 2, ..., r: choose D.
- Ignore all observed history, including past cooperation counts, streaks, and any apparent patterns in opponents.

Edge cases:
- Round 1: choose D.
- Any round after observing full cooperation, partial cooperation, or full defection previously: choose D.
- Final round: choose D.
- If any external heuristic would suggest “testing” cooperation: do not test; choose D.

Implementation:
```text
for each round t:
    action_t = D
```
'''

description_INDIVIDUALISTIC_23 = '''
Round 1: play D.

For each subsequent round t from 2 to r-1:

- Let s be the number of opponents who cooperated in round t-1.
- If s ≥ m, play D.
- If s = m-1, play C.
- If s ≤ m-2, play D.

Final round r: play D.

Tie-breaking and edge handling:
- If the previous round was exactly at the threshold with no margin, still defect unless the round before that also showed the same near-threshold pattern; in that case, cooperate in the current round only if the last two observed rounds were both at s = m-1.
- If there is no prior observation, defect.
- If multiple rounds in a row have been far below threshold, continue defecting.
- If opponents repeatedly exceed the threshold, defect continuously and never volunteer extra cooperation.

Decision rule in compact form:

```text
if t = 1 or t = r:
    D
else:
    s = cooperators among opponents in round t-1
    if s = m-1:
        C
    else:
        D
```

Extended version with persistence filter:

```text
if t = 1 or t = r:
    D
else:
    s1 = cooperators among opponents in round t-1
    s2 = cooperators among opponents in round t-2 if t ≥ 3 else none
    if s1 = m-1 and (t = 2 or s2 = m-1):
        C
    else:
        D
```
'''

description_INDIVIDUALISTIC_24 = '''
Initialize with defection.

For each round t:

1. Let \(h\) be the total number of cooperations you have observed from the other \(n-1\) players over all previous rounds, and let \(T=t-1\) be the number of observed rounds.
2. Estimate the per-opponent cooperation rate
   \[
   \hat p=\frac{h+1}{T(n-1)+2}
   \]
   using the smoothed historical frequency.
3. Model the number of cooperating opponents in the next round as \(X\sim \text{Binomial}(n-1,\hat p)\).
4. Compute
   \[
   q=\Pr(X=m-1).
   \]
5. Cooperate iff
   \[
   kq>1.
   \]
   Otherwise defect.

Decision rules by round:

- Round 1: play \(D\).
- Round 2 and onward: use the rule above.
- If \(kq=1\): play \(D\).
- If the estimate is unstable early on, keep playing \(D\) until the rule produces a strict cooperation signal.

Operational simplification:
- Cooperate only when the history makes it likely that exactly \(m-1\) of the others will cooperate, so your contribution is likely to be pivotal.
- Defect in all other states, especially when the threshold is already likely to be met without you or when it is unlikely to be met at all.
- On the final round, apply the same rule with no adjustment, since there is no future value to protect.

Pseudocode:

```text
for each round t:
    if t == 1:
        action = D
    else:
        p = (total_other_cooperations + 1) / ((t-1)*(n-1) + 2)
        q = binomial_prob(n-1, p, m-1)
        if k * q > 1:
            action = C
        else:
            action = D
```
'''

description_INDIVIDUALISTIC_25 = '''
Initialize: defect.

For round t = 1:
- Play D.

For each round t > 1, let Oₜ₋₁ be the number of opponents who cooperated in the previous round.

Decision rule:
1. Play D if Oₜ₋₁ ≤ m - 3.
2. Play D if Oₜ₋₁ ≥ m.
3. Play C only if Oₜ₋₁ = m - 1 and at least one of the following is true:
   - Oₜ₋₂ ≥ m - 1
   - Oₜ₋₂ = m - 2 and Oₜ₋₃ ≥ m - 1
   - the last three observed counts are nondecreasing and the latest count is m - 1

Fallback:
- If the history is too short to evaluate the above conditions, play D.

Last round:
- Use the same rule as any other round; do not change behavior just because the game is ending.

Update rule:
- After every round, store only the aggregate opponent cooperation counts.
- If a round is played with C and the next observed count drops below m - 1, return to D immediately in the following round.
- If a round is played with D and the observed count still stays at or above m - 1 for two consecutive rounds, keep testing with C only when the near-threshold pattern from the decision rule reappears.

Individualistic stance:
- Default to D.
- Cooperate only when the observed history shows the others are already clustered right at the threshold and the pattern is stable enough that a single additional contribution is likely to secure the reward.
'''

description_INDIVIDUALISTIC_26 = '''
Play cooperatively only when the observed recent cooperation rate makes cooperation strictly more likely to secure the threshold than defection does; otherwise defect.

Decision rule:

- Let `x_t` be the number of opponents who cooperated in round `t`.
- Let `s_t = x_t + 1` if you cooperated in round `t`, and `s_t = x_t` if you defected.
- Maintain a belief estimate `p_t` that at least `m` total cooperators will appear next round if you cooperate, and `q_t` that at least `m` total cooperators will appear next round if you defect.

Initialization:
- In round 1, cooperate if `m <= 2`; otherwise defect.

After each round:
- Update a rolling estimate of opponent cooperation using the last `L = min(5, t)` rounds:
  - `a_t = average of x over the last L rounds`
- Estimate next-round support for the threshold:
  - If you cooperate, expected total cooperators ≈ `a_t + 1`
  - If you defect, expected total cooperators ≈ `a_t`

Action choice for round `t+1`:
- Cooperate iff both conditions hold:
  1. `a_t + 1 >= m`
  2. `a_t >= m - 2`
- Otherwise defect.

Equivalent threshold form:
- Cooperate when the recent average number of cooperating opponents is at least `m - 1` if you defecting would still likely reach the threshold, or at least `m - 2` if your own cooperation is pivotal.
- Defect whenever recent cooperation is below `m - 2`.

Edge cases:

- If `m = 2`:
  - Cooperate in round 1.
  - Continue cooperating as long as at least one opponent cooperated in the previous round.
  - Switch to defect if zero opponents cooperated in the previous round.
- If `m = n - 1`:
  - Cooperate only when at least `n - 2` opponents cooperated in the recent window.
  - Otherwise defect.
- If the last `L` rounds all had `x_t < m - 2`:
  - Defect for the rest of the game.
- If the last `L` rounds all had `x_t >= m - 1`:
  - Cooperate for the rest of the game.
- In the final round:
  - Cooperate only if the most recent observed cooperation count already makes threshold success likely without relying on further adaptation; otherwise defect.

Behavioral rule:
- Never commit to unconditional cooperation.
- Never punish for its own sake.
- Treat each round independently except for the rolling estimate.
- Default to defection under uncertainty, and switch to cooperation only after repeated evidence that the threshold is being met or nearly met.
'''

description_INDIVIDUALISTIC_27 = '''
Initialize:
- Let `need = m - 1`, the number of opponents’ cooperations required for your own cooperation to be pivotal.
- Set `mode = search`.

Round 1:
- Play `D`.

For each round `t > 1`, after observing the previous round’s opponent cooperation count `x = coop_opp(t-1)`:

1. If `x >= need + 1`:
   - Play `D`.

2. If `x == need`:
   - Play `C`.

3. If `x < need`:
   - Play `D`.

4. Exception for the final round:
   - Ignore future considerations.
   - Apply the same rule based only on the most recently observed `x`.

History update:
- Keep only the last observed opponent cooperation count.
- If the last two observed counts were both at least `need`, continue playing `C` until a round occurs with `x >= need + 1`, then switch immediately back to `D`.

Operational form:
```text
if t == 1:
    D
else:
    if coop_opp(t-1) == m-1:
        C
    else:
        D
```

Refinement for repeated near-threshold behavior:
- If `coop_opp(t-1) == m-1` for two consecutive rounds, cooperate in the next round even if you cooperated before.
- The moment `coop_opp` rises to `m` or more, defect again.
- The moment `coop_opp` falls below `m-1`, defect until it returns to exactly `m-1`.

Individualistic posture:
- Never cooperate on speculation alone.
- Cooperate only when the observed opponent count makes your cooperation immediately pivotal.
- Default to defect whenever the threshold is already met by others or is not yet within one opponent of being met.
'''

description_INDIVIDUALISTIC_28 = '''
Always play D.

Decision rule for every round t:
- If t = 1: D
- If 1 < t < r: D
- If t = r: D

History dependence:
- Ignore past cooperation counts for your action choice.
- You may track history only to confirm that defection remains the dominant personal choice, but it never changes your move.

Edge cases:
- If n = 2 or m = n - 1 or any other parameter values allowed by the game, still play D.
- If you were punished, rewarded, or surprised by prior aggregate cooperation levels, still play D.
- If the observed number of other cooperators was high enough to meet the threshold without you, defect.
- If it was not high enough, defect.
- If you were exactly pivotal in a previous round, defect in the next one anyway.

Operational form:
```text
For each round t:
    choose D
```

Individualistic stance:
- Never pay the personal contribution cost.
- Never rely on others’ coordination.
- Never sacrifice your own current payoff for a collective threshold.
'''

description_INDIVIDUALISTIC_29 = '''
Play a guarded threshold strategy with personal reservation level.

Let `x_t` be the number of opponents you observed cooperating in round `t-1` among the `n-1` opponents, and let `s_t = x_t + 1` if you cooperated last round, or `x_t` if you defected last round, be the total cooperators you believe were present in that prior round.

Define:

- `need = m`
- `margin = 1`
- `safe = m - margin`

Decision rule:

1. **Round 1**
   - Cooperate only if `m = 2`.
   - Otherwise defect.

2. **Rounds 2 through r-1**
   - Cooperate if and only if the previous round met the threshold with slack:
     - `s_t >= m`
     - and `x_t >= safe`
   - Equivalently, cooperate only after seeing a round in which cooperation was sufficient and at least `m-1` opponents cooperated.
   - In all other cases, defect.

3. **Last round**
   - Cooperate only if the previous round was strong:
     - `s_t >= m + 1`
   - Otherwise defect.

Adjustment rules:

- If you defected in the previous round and the observed opponent cooperation count was exactly `m-1`, keep defecting; do not try to “rescue” the threshold alone.
- If you cooperated in the previous round and the observed opponent cooperation count was at least `m-1`, continue cooperating.
- If the observed opponent cooperation count drops below `m-1` in any round, defect in the next round until you see a round with at least `m-1` cooperating opponents again.
- If the same strong cooperation pattern holds for `2` consecutive rounds, maintain cooperation until a drop occurs.

Compact form:

```text
If t = 1:
    C if m = 2 else D
Else if t = r:
    C if previous total cooperators >= m+1 else D
Else:
    C if previous total cooperators >= m and previous opponent cooperators >= m-1
    else D
```

Behavioral principle:

- Cooperate only when the group has already demonstrated reliable threshold support.
- Defect immediately when support becomes uncertain.
- Never bear the cost of being the lone stabilizer.
'''

description_INDIVIDUALISTIC_30 = '''
Track the number of opponents who cooperated in each round, `s_t`.

Decision rule:

- Round 1: play `D`.
- For round `t+1` with `t >= 1`:
  - Play `C` only if all of the following hold:
    1. `s_t = m - 1`
    2. `s_{t-1} = m - 1` if `t >= 2`
    3. At least two of the last three observed rounds, if available, had `s >= m - 1`
  - Otherwise play `D`.

Edge handling:

- If the observed cooperation count ever drops below `m - 1` in a round, reset the “support” check and defect until the support condition above is restored.
- If the observed cooperation count is at least `m` in a round, play `D` next round unless the last two rounds were exactly `m - 1`; in that case, continue with the rule above.
- Final round: use the same rule; do not add any special final-round cooperation beyond the normal condition.

Individualistic posture:

- Default to `D`.
- Cooperate only when the opposing side has shown stable, near-threshold support and your contribution is plausibly pivotal.
- Never cooperate into a weak or inconsistent group.
- Never cooperate when the group already appears safely above threshold.
'''

description_INDIVIDUALISTIC_31 = '''
Default to defection. Cooperate only when recent history makes your cooperation likely to be the decisive extra move.

State variables:
- `h_t`: number of opponents who cooperated in round `t`
- `p_t`: estimated per-opponent cooperation rate before round `t`
- Initialize `p_1 = (m - 1) / (n - 1)`

Update after each round:
- `p_{t+1} = 0.7 * p_t + 0.3 * (h_t / (n - 1))`

Decision for round `t`:

1. If `t = 1`, play `D`.

2. For `t > 1`, compute:
   - `E = p_t * (n - 1)` = expected opponent cooperators this round
   - `margin = E - (m - 1)`

3. Play `C` only if both conditions hold:
   - `0 <= margin < 1`  
   - the last two observed rounds show support near the threshold:
     - either `h_{t-1} >= m - 1`, or
     - `h_{t-1} = m - 2` and `h_{t-2} >= m - 2`

4. Otherwise play `D`.

Probe rule:
- If no round so far has reached `h_t >= m - 1`, and `t` is a multiple of `3`, and the last observed round had `h_{t-1} = m - 2`, play `C` once as a test; otherwise `D`.

Endgame rule:
- In the last two rounds, ignore probing and use only the main rule above.
- If the estimated support is below `m - 1`, defect.
- If the estimated support is in the narrow band `[m - 1, m)`, cooperate.
- If the estimated support is at least `m`, defect.

Edge cases:
- If `m = 2`, treat `h_t >= 1` as “near threshold” and use the same logic.
- If `n = m + 1`, cooperate only when the estimate is exactly one short of full expected support.
- If a round has no prior history beyond `t = 1`, use the default defection rule.

Individualistic posture:
- Never cooperate on trust alone.
- Cooperate only when history suggests your contribution is the one that can tip the round over the line.
- If support is clearly strong, take the free-rider position and defect.
- If support is clearly weak, conserve your own payoff and defect.

'''

description_INDIVIDUALISTIC_32 = '''
Initialize with defection.

For each round t:

1. Let `h` be the number of opponents observed cooperating in the previous round.
2. Let `W = min(4, t-1)` and let `avg` be the average of the last `W` observed opponent-cooperation counts.
3. Cooperate only if all of the following hold:
   - `h = m - 1`
   - `avg >= m - 1`
   - at least `ceil(W/2)` of the last `W` observations were `>= m - 1`
4. Otherwise defect.

Special cases:

- Round 1: defect.
- If `m - 1 = 0` is impossible under the parameters, so there is no unconditional-cooperation case.
- If the previous round had `h >= m`, defect.
- If the previous round had `h <= m - 2`, defect unless the recent window already shows repeated `m - 1` outcomes as above.
- Final round: use the same rule; do not change behavior just because the game is ending.

Individualistic stance:

- Default to keeping the endowment.
- Treat cooperation as a narrow, opportunistic move only when the history indicates the group is sitting exactly at the threshold where your contribution is likely to matter.
- Never cooperate out of generosity, imitation, or commitment to a coalition.
- If the observed counts drift away from `m - 1`, revert immediately to defection and wait for the threshold pattern to reappear.
'''
