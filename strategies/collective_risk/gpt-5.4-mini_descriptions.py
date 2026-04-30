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
