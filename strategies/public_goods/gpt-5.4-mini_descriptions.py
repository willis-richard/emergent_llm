"""
Strategy descriptions for public_goods.

Generated with:
- Provider: OpenAI
- Model: gpt-5.4-mini
"""


description_COLLECTIVE_1 = '''
Play a conditional cooperation policy with a moving participation threshold.

Let:
- \(m_t\) be the number of opponents observed to cooperate in round \(t\)
- \(N = n - 1\)
- \(p_t = m_t / N\), the observed opponent cooperation rate
- \(s_t\) be the recent cooperation score computed from the last \(L\) rounds, where \(L = \min(3, t-1)\) for \(t \ge 2\)

Define:
- \( \bar p_t = \frac{1}{L} \sum_{u=t-L}^{t-1} p_u \) for \(t \ge 2\)
- If \(t=1\), no history exists.

Decision rule:

1. Round 1:
   - Cooperate.

2. Rounds \(2\) through \(r-1\):
   - Cooperate if both conditions hold:
     - \(p_{t-1} \ge \theta_t\)
     - \(\bar p_t \ge \theta_t - 0.10\)
   - Otherwise defect.

3. Final round \(r\):
   - Cooperate only if:
     - \(p_{r-1} \ge \theta_r\)
     - \(\bar p_r \ge \theta_r\)
   - Otherwise defect.

Threshold schedule:
- Start with \(\theta_2 = 0.60\).
- Update by observed behavior:
  - If \(p_{t-1} \ge 0.80\), set \(\theta_t = 0.50\).
  - If \(0.50 \le p_{t-1} < 0.80\), set \(\theta_t = 0.60\).
  - If \(0.30 \le p_{t-1} < 0.50\), set \(\theta_t = 0.75\).
  - If \(p_{t-1} < 0.30\), set \(\theta_t = 0.90\).

Consistency rule:
- If cooperation has been chosen in the last round, keep cooperating only if current behavior remains within the active threshold.
- If defections dominate for two consecutive rounds, switch to defection and stay there until \(p_t \ge 0.80\) again.

Reset rule:
- After any round where \(p_t = 1\), cooperate in the next round regardless of prior history.
- After any round where \(p_t = 0\), defect in the next round regardless of prior history.

Late-game rule:
- In the last two rounds, require stricter evidence:
  - Cooperate only if \(p_t \ge 0.80\) in the immediately preceding round.
  - Otherwise defect.

Collective alignment:
- Treat cooperation as the default state when the group is broadly cooperating.
- Treat defection as the fallback state when the group shows persistent free-riding.
- Move together with the observed majority, but only sustain cooperation when it is being reciprocated at a stable rate.
'''

description_COLLECTIVE_2 = '''
Start with cooperation and treat the group as a shared project:

- Round 1: play C.
- Let `o_t` be the number of opponents who cooperated in round `t`.
- Let `s_t = o_t / (n-1)` be the observed opponent cooperation rate.
- Track:
  - `m_t`: moving average of `s_t` over the last `w` rounds, with `w = min(3, t-1)` until it reaches 3.
  - `L_t`: consecutive-round low-cooperation counter, incremented when `s_t < 1/2`, reset otherwise.

Decision rule for round `t+1`:
1. Cooperate if `m_t >= 1/2`.
2. Defect if `m_t < 1/2` for `2` consecutive observed rounds.
3. If `m_t` is exactly `1/2`, cooperate unless `L_t >= 2`.

Last-round rule:
- In round `r`, cooperate if `m_{r-1} >= 1/2`.
- Otherwise defect.

Recovery rule:
- After any round in which `s_t >= 1/2`, return immediately to cooperation in the next round.
- After two consecutive rounds with `s_t < 1/2`, switch to defection until the moving average returns to at least `1/2`.

Minority tolerance:
- If `s_t` is just below `1/2` for one round only, ignore the dip and keep cooperating.
- If `s_t = 0`, defect next round and keep defecting until at least half of opponents cooperate again.

Early-game default:
- Cooperate in rounds 1 and 2 unless round 1 already shows `s_1 = 0`, in which case defect in round 2.

Late-game consistency:
- Never switch to unconditional defection unless the observed cooperation rate stays below half for two consecutive rounds.
- Once cooperation is restored at or above half, resume cooperation immediately.

Compact pseudocode:

```text
Round 1: C

For t = 1 to r-1:
    observe s_t = o_t / (n-1)

    update m_t = average of last min(3, t) values of s
    if s_t < 1/2:
        L_t = L_{t-1} + 1
    else:
        L_t = 0

    if t+1 == r:
        play C if m_t >= 1/2 else D
    else if m_t > 1/2:
        play C
    else if m_t < 1/2 and L_t >= 2:
        play D
    else if m_t == 1/2:
        play C if L_t < 2 else D
```

Collective stance:
- Default to contributing.
- Stay committed while the group remains at or above half cooperation.
- Use brief, group-level withdrawal only when the shared contribution norm falls below the midpoint for more than a transient dip.
- Rejoin immediately when the group re-establishes cooperative behavior.
'''

description_COLLECTIVE_3 = '''
Start with cooperation in round 1.

For every round t ≥ 2, let h be the number of opponents who cooperated in round t−1, and let H be the average number of opponent cooperators over the last up to 3 rounds, excluding rounds where fewer than 2 past rounds exist.

Define the cooperation threshold:
- T = ceil((n / k) − 1)

Decision rule:
- Cooperate if the observed number of opponent cooperators in the last round is at least T.
- Cooperate if the 3-round average H is at least T and the last-round count h is at least T−1.
- Otherwise defect.

Update behavior by streaks:
- If cooperation is chosen and the last-round count h is at least T, stay cooperative next round.
- If the last-round count h falls below T, switch to defection immediately for one round.
- After one defection round, return to cooperation if the last-round count was at least T−1; otherwise continue defecting until the last-round count reaches T again.

Endgame:
- In the final two rounds, ignore forgiveness and require the strict threshold:
  - Cooperate only if h ≥ T in the immediately preceding round.
  - Otherwise defect.

Special cases:
- If T ≤ 0, cooperate every round.
- If T ≥ n−1, cooperate only when all opponents cooperated in the prior round.
- If the previous round is unavailable, cooperate in round 1 and use the round-2 observation for round 2 onward.

Compact pseudocode:

```text
round 1: C

for round t >= 2:
    h = opponents_cooperating_in_round(t-1)

    if t in {r, r-1}:
        if h >= T:
            play C
        else:
            play D
    else:
        H = average(opponents_cooperating_in_round(t-1), ..., up to last 3 rounds)
        if h >= T:
            play C
        else if H >= T and h >= T-1:
            play C
        else:
            play D
```
'''

description_COLLECTIVE_4 = '''
Start with cooperation.

Let \(m_t\) be the number of opponents who cooperated in round \(t\), and let \(n-1\) be the number of opponents you observe.

Maintain a running cooperation rate
\[
q_t = \frac{1}{t}\sum_{s=1}^{t} m_s/(n-1)
\]
and a recent-rate estimate over the last \(L=\min(3,\lfloor r/4\rfloor)\) rounds:
\[
\ell_t = \frac{1}{L}\sum_{s=t-L+1}^{t} m_s/(n-1)
\]
when those rounds exist.

Decision rule for round \(t+1\), after observing round \(t\):

1. Cooperate if both of the following hold:
   - \(m_t \ge \left\lceil \frac{n-1}{2}\right\rceil\)
   - \(\ell_t \ge \frac{1}{2}\)

2. Defect if either of the following holds:
   - \(m_t \le \left\lfloor \frac{n-1}{3}\right\rfloor\)
   - the last two rounds both satisfy \(m_s < \frac{n-1}{2}\)

3. In the intermediate zone, imitate the current majority:
   - cooperate if \(m_t > \frac{n-1}{2}\)
   - defect if \(m_t < \frac{n-1}{2}\)
   - if \(m_t = \frac{n-1}{2}\), cooperate

First round:
- Cooperate.

Early rounds:
- For rounds 2 and 3, use only the immediately previous round:
  - cooperate if at least half of opponents cooperated in the previous round
  - defect if fewer than one-third cooperated
  - otherwise cooperate

Last two rounds:
- Cooperate if the current recent-rate estimate \(\ell_t \ge \frac{1}{2}\)
- Otherwise defect
- If the next-to-last round showed broad cooperation, keep cooperating through the final round
- If there has been sustained low cooperation for two consecutive rounds, defect through the end

Recovery rule:
- After any defection decision caused by low cooperation, return to cooperation immediately once one round reaches \(m_t \ge \left\lceil \frac{n-1}{2}\right\rceil\)

Stability rule:
- If the last \(L\) rounds all have \(m_s \ge \left\lceil \frac{n-1}{2}\right\rceil\), cooperate unconditionally until this pattern breaks
- If the last \(L\) rounds all have \(m_s \le \left\lfloor \frac{n-1}{3}\right\rfloor\), defect unconditionally until cooperation recovers

Tie-breaking:
- Treat exact half-cooperation as a signal to cooperate

Collective mindset:
- Default to cooperation
- Reward sustained cooperation by continuing to cooperate
- Withdraw cooperation only after clear, repeated undercooperation
- Restore cooperation as soon as a cooperative majority reappears
'''

description_PROSOCIAL_1 = '''
Let \(m_t\) be the number of opponents who cooperated in round \(t\), so \(0 \le m_t \le n-1\). Let \(H_t = (m_1,\dots,m_t)\) be the history after round \(t\).

Use these state variables:

- \(S_t\): your recent support score, initialized to 0
- \(L_t\): current low-cooperation streak in the field, initialized to 0

Update after each round \(t\):
- If \(m_t \ge \lceil (n-1)/2 \rceil\), set \(L_t = 0\); otherwise set \(L_t = L_{t-1}+1\)
- Set \(S_t = \frac{1}{\min(t,5)} \sum_{j=\max(1,t-4)}^t \frac{m_j}{n-1}\)

Decision rule for round \(t+1\):

1. Round 1:
   - Play \(C\)

2. Round 2 onward:
   - Cooperate if all of the following hold:
     - \(m_t \ge \lceil (n-1)/2 \rceil\), or
     - \(S_t \ge 0.4\), or
     - \(L_t = 1\) and \(m_t \ge 1\)
   - Defect otherwise

3. Endgame rule:
   - In the last 2 rounds, ignore the default cooperation trigger only if \(m_t = 0\) for both of the two preceding rounds
   - Otherwise continue using the rule above
   - Specifically:
     - If \(t = r-1\) or \(t = r\), cooperate whenever \(m_t \ge 1\)

Equivalent compact version:
- Start by cooperating.
- Continue cooperating as long as the observed cooperation level is at least moderate, or there is any recent sign of recovery.
- Defect only after sustained low cooperation by others.

Operational details:
- If you observe unanimous defection in a round, defect next round.
- If you observe any cooperation at all after a defection phase, immediately return to cooperation.
- If the field alternates between high and low cooperation, follow the most recent majority trend using the threshold \(m_t \ge \lceil (n-1)/2 \rceil\).

Prosocial orientation:
- Default to \(C\) whenever there is a plausible cooperative response to the group’s recent behavior.
- Use \(D\) only as a narrow response to persistent noncooperation, never as a first move.
- In the final rounds, bias toward cooperation unless the group has shown clear and repeated refusal to cooperate.
'''

description_PROSOCIAL_2 = '''
Cooperate in round 1.

Maintain an observed cooperation rate over the last m rounds, with m growing from 1 to 5 as the game progresses:
- Let a_t be the number of opponents who cooperated in round t.
- Let ρ_t = a_t / (n - 1).
- Let \u0304ρ be the average of ρ over the last m rounds, using all available rounds if fewer than m have been played.

Decision rule for round t:
- Cooperate if \u0304ρ ≥ θ_t
- Defect if \u0304ρ < θ_t

Set the cooperation threshold θ_t as:
- θ_t = 0.5 for the first third of the game
- θ_t = 0.6 for the middle third
- θ_t = 0.7 for the final third

Use the following adjustments:

1. First round
- Cooperate unconditionally.

2. Early response to behavior
- If at least half of opponents cooperated in the previous round, cooperate next round.
- If fewer than half cooperated in the previous round, require the moving-average rule above.

3. Recovery rule
- After any round in which you defect, return to cooperation immediately if either:
  - at least 70% of opponents cooperated in the previous round, or
  - the moving average \u0304ρ meets the current threshold θ_t.

4. Persistent defection rule
- If fewer than 30% of opponents cooperated in each of the last 3 rounds, defect until the moving average over the last 3 rounds rises to at least 50%.

5. Endgame
- In the last round, cooperate if the moving average over the last 3 rounds is at least 50%.
- In the last 2 rounds, keep following the standard rule; do not switch to unconditional defection.

6. Tie handling
- If \u0304ρ equals θ_t exactly, cooperate.

Compact pseudocode:

if t == 1:
    play C
else:
    compute ρ from previous rounds
    update moving average \u0304ρ over last m rounds
    if last 3 rounds all had ρ < 0.3:
        play D until average over last 3 rounds ≥ 0.5
    else if t is in final third:
        play C if \u0304ρ ≥ 0.7 else D
    else if t is in middle third:
        play C if \u0304ρ ≥ 0.6 else D
    else:
        play C if \u0304ρ ≥ 0.5 else D

When uncertain, default to cooperation unless the recent history shows sustained low cooperation by opponents.
'''

description_PROSOCIAL_3 = '''
Round 1: cooperate.

For round t > 1, let  
- m_{t-1} = number of other players who cooperated in round t−1  
- s_{t-1} = m_{t-1} / (n−1), the observed cooperation rate among opponents

Maintain a state variable target ∈ {C, D}, initialized to C.

Update rule after each round t−1:

1. If m_{t-1} = n−1:
   - set target := C

2. Else if m_{t-1} ≥ ceil((n−1)/2):
   - set target := C

3. Else if m_{t-1} = 0 for 2 consecutive rounds:
   - set target := D for the next round

4. Else if target = D and m_{t-1} > 0:
   - set target := C

5. Otherwise:
   - keep the previous target

Action rule for round t:
- play C if target = C
- play D if target = D

Forced forgiveness rule:
- Any round in which m_{t-1} ≥ ceil((n−1)/2) immediately resets target to C, even if the strategy was in D mode.

Endgame rule:
- In the last round, if the strategy is in C mode, play C.
- In the last round, if the strategy is in D mode, keep D only if the previous two rounds both had m = 0; otherwise play C.

Clarifications for edge cases:
- If n = 2, interpret ceil((n−1)/2) as 1, so any observed opponent cooperation restores C mode.
- If cooperation is fully absent for two consecutive rounds, enter temporary D mode for one round at a time until at least one opponent cooperates.
- Any positive cooperation from opponents breaks persistent defection and returns to cooperation immediately.

This strategy is generous, reciprocating, and stabilizes on cooperation whenever there is any meaningful sign of cooperation from the rest of the group.
'''

description_PROSOCIAL_4 = '''
Play a cooperative baseline with contingent response to the recent cooperation rate.

State variables:
- `t`: current round, starting at 1
- `m_t`: number of other players who cooperated in round `t`
- `a_t`: your action in round `t`
- `ρ_t = m_t / (n - 1)`: observed cooperation rate among opponents in round `t`

Decision rule:

1. Round 1:
- Play `C`.

2. Rounds 2 through `r`:
- Compute the recent cooperation rate over the last `w` observed rounds, where `w = min(3, t-1)`.
- Let `R_t` be the average of `ρ_{t-1}, ρ_{t-2}, ..., ρ_{t-w}`.
- Let `S_t` be a forgiveness-adjusted target:
  - `S_t = 0.5` if `t <= 3`
  - `S_t = 0.6` if `4 <= t <= r-2`
  - `S_t = 0.5` if `t >= r-1`

Action choice:
- If `R_t >= S_t`, play `C`.
- If `R_t < S_t`, play `D`.

3. Immediate response to strong cooperation or defection:
- If all observed opponents cooperated in the previous round (`ρ_{t-1} = 1`), play `C` regardless of the moving average.
- If no opponent cooperated in the previous round (`ρ_{t-1} = 0`) and the same happened in the round before that when available, play `D` for this round.
- If the previous round’s cooperation rate was at least one-half and the round before that was lower, play `C` to reward recovery.
- If the previous round’s cooperation rate dropped sharply by at least `1/2` compared to the round before it, play `D` for one round only, then reassess next round.

4. Forgiveness rule:
- After any round in which you play `D`, return to `C` immediately if the most recent observed cooperation rate `ρ_{t-1}` is at least `1/2`.
- Do not punish for more than one consecutive round unless the last two observed cooperation rates are both below `1/3`.

5. Endgame:
- In the final two rounds, play `C` unless the last two observed cooperation rates are both below `1/3`.
- If that low-cooperation condition holds, play `D` in the final round only; otherwise remain cooperative.

6. Default behavior:
- When history is too short to apply a rule, choose `C`.

Compact pseudocode:

```text
if t == 1:
    action = C
else:
    rho_prev = m[t-1] / (n-1)
    R = average(rho[t-1], rho[t-2], ..., rho[max(1,t-3)])

    if t >= r-1:
        if t > 2 and rho[t-1] < 1/3 and rho[t-2] < 1/3:
            action = D
        else:
            action = C
    else if rho_prev == 1:
        action = C
    else if t > 2 and rho_prev == 0 and rho[t-2] == 0:
        action = D
    else if t > 2 and rho_prev - rho[t-2] >= 1/2:
        action = D
    else if R >= (0.5 if t <= 3 else 0.6):
        action = C
    else:
        action = D

    if action == D and rho_prev >= 1/2:
        action = C
```

This keeps cooperation as the default, rewards sustained cooperation immediately, and uses short, selective defection only after repeated low cooperation.
'''

description_ALTRUISTIC_1 = '''
Let \(m_t\) be the number of other players who cooperated in round \(t\), and let
\[
\bar m_t=\frac{1}{t}\sum_{s=1}^{t} m_s
\]
be the running average of observed opponent cooperation up to round \(t\).

Define the cooperation threshold
\[
\theta = \left\lceil \frac{n}{k} - 1 \right\rceil .
\]
This is the minimum number of cooperating opponents needed for your own cooperation to be socially justified by the current round’s observed cooperation level.

Use the following policy:

### Round 1
Play \(C\).

### General round \(t \ge 2\)
Play \(C\) if at least one of the following holds:

1. **Immediate reciprocity condition:** \(m_{t-1} \ge \theta\)
2. **History condition:** \(\bar m_{t-1} \ge \theta\)
3. **Repair condition:** You have seen at least one round in the last three rounds where \(m_s \ge \theta\)

Otherwise play \(D\).

### Endgame
In the final two rounds, keep the same rule as above, except:

- If \(\bar m_{t-1} \ge \theta\), always play \(C\).
- If no opponent cooperation has met \(\theta\) in the previous three rounds, play \(D\).

### Persistence and forgiveness
If you switch to \(D\) because the group falls below threshold, return to \(C\) immediately after the first round in which either:

- \(m_t \ge \theta\), or
- two consecutive rounds satisfy \(m_t \ge \theta - 1\).

### Zero-cooperation edge case
If \(m_s = 0\) for every observed round so far, play \(D\) from that point onward.

### All-cooperation edge case
If \(m_s \ge \theta\) for every observed round so far, play \(C\) for every remaining round.

### Compact pseudocode
```text
state: last3 = queue of last 3 observed m values

round 1:
    play C

for round t = 2..r:
    if all observed m_s == 0:
        play D
    else if average(observed m_s) >= theta:
        play C
    else if any of last 3 observed m_s >= theta:
        play C
    else if last observed m_{t-1} >= theta:
        play C
    else if (m_{t-1} >= theta - 1 and m_{t-2} >= theta - 1):
        play C
    else:
        play D
```

### Behavioral character
- Starts cooperatively.
- Remains cooperative as long as the group shows meaningful cooperation.
- Stops subsidizing persistent free-riding.
- Returns to cooperation immediately when the group shows renewed cooperation.
- Treats brief dips generously, but does not reward sustained defection.
'''

description_ALTRUISTIC_2 = '''
**Strategy: Generous Adaptive Cooperation**

Let:

- `m_t` = number of other players who cooperated in round `t`
- `h_t` = history up to round `t`
- `n-1` = number of opponents
- `q_t = m_t / (n-1)` = observed cooperation rate among opponents in round `t`

Maintain a state variable `trust`, initialized to `0`.

### Round 1
Play `C`.

### For each round t ≥ 2

Update `trust` from the previous round:

- If `q_{t-1} = 1`, set `trust = min(trust + 2, 3)`
- If `q_{t-1} ≥ 0.5`, set `trust = min(trust + 1, 3)`
- If `0 < q_{t-1} < 0.5`, set `trust = max(trust - 1, -3)`
- If `q_{t-1} = 0`, set `trust = max(trust - 2, -3)`

Then choose:

#### Cooperate if any of the following holds
1. `trust ≥ -1`
2. `q_{t-1} > 0`
3. `t` is in the last `ceil(r/3)` rounds and `q_{t-1} ≥ 0.25`
4. `t` is the final round

#### Defect only if all of the following hold
1. `trust ≤ -2`
2. `q_{t-1} = 0`
3. `t < r`

### Special rules
- **First round:** always cooperate.
- **After a fully cooperative round:** always cooperate next round.
- **After one round of complete defection by others:** cooperate once more before switching to defection.
- **In the final round:** cooperate unless the previous round had `q_{t-1} = 0` and `trust ≤ -2`.

### Full decision rule in pseudocode

```text
initialize trust = 0

for t = 1 to r:
    if t == 1:
        play C
    else:
        observe q_prev = m_(t-1) / (n-1)

        if q_prev == 1:
            trust = min(trust + 2, 3)
        else if q_prev >= 0.5:
            trust = min(trust + 1, 3)
        else if q_prev > 0:
            trust = max(trust - 1, -3)
        else:
            trust = max(trust - 2, -3)

        if t == r:
            if q_prev == 0 and trust <= -2:
                play D
            else:
                play C
        else if trust <= -2 and q_prev == 0:
            play D
        else if t > r - ceil(r/3) and q_prev >= 0.25:
            play C
        else:
            play C
```

### Behavioral intent
- Start with goodwill.
- Reward any observable cooperation immediately.
- Punish only persistent full defection.
- Restore cooperation as soon as there is any evidence of responsiveness.
- Stay cooperative late in the game unless exploitation is repeated and complete.
'''

description_ALTRUISTIC_3 = '''
Play **C** in round 1.

For each round t > 1, let:
- `m_t` = number of opponents who cooperated in round `t-1`
- `q_t = m_t / (n - 1)` = observed cooperation rate among opponents
- `Q_t` = average of `q_2, ..., q_t` over all past observed rounds, if any
- `L_t` = length of the current consecutive streak of rounds, ending at `t-1`, in which `q` was at least `1/2`

Decision rule for round t:

```text
if t == 1:
    play C

else if t == r:
    play C

else if q_t >= 1/2:
    play C

else if Q_t >= 1/2 and q_t >= 1/3:
    play C

else if L_t >= 2:
    play C

else:
    play D
```

Update rule after each round:
- After observing `m_t`, recompute `q_t`
- Update `Q_t`
- Update `L_t`:
  - if `q_t >= 1/2`, then `L_{t+1} = L_t + 1`
  - otherwise `L_{t+1} = 0`

Edge handling:
- If `n = 2`, interpret `q_t` as the single opponent’s action: cooperate if that opponent cooperated in the previous round, otherwise use the same thresholds above.
- If no past rounds exist yet, cooperate.
- In the final round, cooperate unconditionally.
- If cooperation has been common overall (`Q_t >= 1/2`), stay cooperative even after a temporary dip, provided the dip is not severe (`q_t >= 1/3`).

Behavioral summary:
- Begin by contributing.
- Match a broadly cooperative group with continued cooperation.
- Tolerate occasional defections.
- Only withdraw cooperation after repeated low cooperation by others.
- Return to cooperation immediately once the group becomes reasonably cooperative again.
'''

description_ALTRUISTIC_4 = '''
Round 1: play C.

For round t > 1, let
- h = number of opponents who cooperated in round t-1
- m = n - 1, the number of opponents
- q = h / m, the observed opponent cooperation rate in the previous round
- s = number of rounds up to t-1 in which at least half of opponents cooperated

Decision rule:

1. Play C if q = 1.
2. Play C if q ≥ 1/2 and the previous round was not a sharp collapse:
   - i.e., if q ≥ 1/2 and q_prev ≥ 1/2, where q_prev is the cooperation rate from round t-2, or if t = 2, skip this condition.
3. Play C if the running average cooperation rate of opponents over all previous rounds is at least 1/2.
4. Otherwise, play D.

More compactly:

```
if t == 1:
    C
else:
    q = coop_opponents_last_round / (n-1)
    avg = total_coop_opponents_so_far / ((t-1)*(n-1))

    if q == 1:
        C
    elif q >= 0.5 and avg >= 0.5:
        C
    elif q >= 0.5 and t == 2:
        C
    elif q >= 0.5 and q_prev >= 0.5:
        C
    elif avg >= 0.5 and t <= r-2:
        C
    else:
        D
```

Edge cases:
- If n = 2, “half or more” means the single opponent cooperated.
- If the last two rounds are both full cooperation, continue cooperating even after one imperfect round by treating a single drop below 1/2 as a temporary fluctuation unless it repeats.
- In the final round, play C whenever the most recent round had at least half of opponents cooperating; otherwise play D.
- If cooperation is erratic, use the cumulative average as the tiebreaker: cooperate when the opponent population has been cooperative on average, defect when it has not.

Altruistic bias:
- Default to C.
- Require sustained low cooperation before switching to D.
- Return to C immediately after any clearly cooperative round.
- Give the benefit of the doubt after isolated defections by others.
'''

description_BENEVOLENT_1 = '''
Start by cooperating.

After each round, let `x` be the number of your opponents who cooperated in that round, and let `m = n - 1` be the number of opponents.

Maintain two state variables:

- `trust` in `[0, 1]`, initialized to `1`
- `bad_streak`, the number of consecutive rounds in which fewer than half of your opponents cooperated, initialized to `0`

Update after observing round `t`:

```text
coop_rate = x / m
trust = 0.6 * trust + 0.4 * coop_rate

if coop_rate < 0.5:
    bad_streak += 1
else:
    bad_streak = 0
```

Decision rule for round `t + 1`:

```text
if t + 1 == 1:
    play C
else if t + 1 == r:
    play C if trust >= 0.5 else play D
else if bad_streak >= 2:
    play D
else if trust >= 0.5:
    play C
else:
    play D
```

Edge-case handling:

- First round: play `C`.
- If the previous round had unanimous cooperation by your opponents, play `C` next round regardless of the current `trust` value.
- If the previous round had zero opponent cooperation, play `D` next round, but reset to `C` immediately once any round reaches at least half opponent cooperation.
- If cooperation resumes after a punishment period, return to `C` immediately; do not keep punishing once opponents have started cooperating again.

Behavioral intent:

- Reward sustained cooperation quickly.
- Defect only after clear and repeated low cooperation from the others.
- Forgive immediately when cooperation reappears.
- End by cooperating whenever the history shows at least moderate recent cooperation.
'''

description_BENEVOLENT_2 = '''
Round 1: Cooperate.

Maintain a running cooperation score for the group based only on the observed number of cooperators in each previous round.

Let
- `m_t` = number of opponents who cooperated in round `t`
- `q_t = m_t / (n - 1)` = observed opponent cooperation rate in round `t`
- `Q_t` = average of `q_1 ... q_t` over all completed rounds, with `Q_0 = 1`

Decision rule for round `t + 1`:

1. If `t = 0`, play `C`.
2. If `t >= 1`, compute `Q_t`.
3. Cooperate if `Q_t >= 1/2`.
4. Defect if `Q_t < 1/2`.

Add a forgiveness mechanism so occasional drops do not lock the strategy into defection:

- Let `L_t` be the number of consecutive rounds immediately before round `t + 1` in which `q < 1/2`.
- Let `H_t` be the number of consecutive rounds immediately before round `t + 1` in which `q >= 1/2`.

Use this refined rule:

- Cooperate if either:
  - `Q_t >= 1/2`, or
  - `L_t <= 2` and `H_t > 0`
- Defect only if:
  - `Q_t < 1/2` and
  - `L_t >= 3`

Update after each round:
- If `q_t >= 1/2`, set `H_t = H_{t-1} + 1` and `L_t = 0`
- If `q_t < 1/2`, set `L_t = L_{t-1} + 1` and `H_t = 0`

Last-round rule:
- Use the same rule as any other round; never switch to defection just because it is the final round.

Edge cases:
- If `n = 2`, treat `q_t` as either `0` or `1` based on whether the single opponent cooperated.
- If all observed opponent behavior has been exactly balanced at the threshold, continue cooperating.
- If a single round is unavailable for updating due to an interruption, ignore that round and preserve the previous state.

Benevolent default:
- Start by cooperating.
- Keep cooperating as long as the group’s observed behavior is at least moderately cooperative.
- Only move to defection after a sustained pattern of low cooperation.
- Return to cooperation immediately after the opponent group shows renewed cooperation.
'''

description_BENEVOLENT_3 = '''
Round 1: Cooperate.

Maintain two running quantities from history:
- `m_t`: number of opponents who cooperated in round `t`
- `s_t`: total cooperators among opponents in round `t`

Let `avg_m(t)` be the average of `m_1 ... m_t` over observed rounds.

Use this rule in round `t+1` after observing rounds `1..t`:

1. Compute recent cooperation level:
   - `recent = average(m_{t-L+1} ... m_t)` where `L = min(3, t)`

2. Classify the environment:
   - `strongly cooperative` if `recent >= (n-1) - 1`
   - `mixed` if `1 <= recent < (n-1) - 1`
   - `hostile` if `recent < 1`

3. Choose action:
   - If `strongly cooperative`: Cooperate
   - If `mixed`: Cooperate if `m_t >= ceil((n-1)/2)`, otherwise Defect
   - If `hostile`: Defect

4. Forgiveness rule:
   - If you defected in round `t` and `m_t >= ceil((n-1)/2)`, cooperate in round `t+1` unless the last two rounds were both hostile.

5. Recovery rule:
   - If the last two rounds were hostile and then the current round reaches `m_t >= ceil((n-1)/2)`, cooperate immediately in the next round.

6. Endgame rule:
   - In the final round, play the same action you would play under the above rule using the observed history; do not switch to a special exploitative action.

Compact pseudocode:

```text
if t = 1:
    C
else:
    recent = average(m_{max(1, t-L+1)} ... m_t)

    if recent >= (n-1) - 1:
        action = C
    else if recent < 1:
        action = D
    else:
        action = C if m_t >= ceil((n-1)/2) else D

    if previous_action = D and m_t >= ceil((n-1)/2) and not (m_{t-1} < 1 and m_t < 1):
        action = C

    if final_round:
        keep action
```

Tie-breaks and edge cases:
- If `n = 2`, treat `ceil((n-1)/2) = 1`.
- If fewer than 3 rounds have been observed, use all available rounds in `recent`.
- If observations are unavailable for a round, default to the most recent known action rule and continue cooperating unless clear hostility has been established.
'''

description_BENEVOLENT_4 = '''
Round 1: cooperate.

For each later round t, let h be the number of opponents who cooperated in round t-1, and let H be the running history of observed opponent cooperation counts.

Use this rule:

1. Track a cooperation baseline  
   - Let m be the median of the observed opponent-cooperation counts from the most recent up to 3 rounds, excluding rounds with no history.
   - Let s be the average opponent cooperation rate over all previous rounds:  
     s = (sum of observed opponent cooperators) / ((t-1)·(n-1))

2. Cooperate when the group is cooperatively inclined  
   Cooperate if either:
   - h ≥ ceil((n-1)/2), or
   - s ≥ 0.5

3. Defect when the group is persistently uncooperative  
   Defect if both:
   - h ≤ floor((n-1)/3), and
   - m ≤ floor((n-1)/3)

4. In the middle zone, forgive first and punish only persistence  
   If the group is neither clearly cooperative nor clearly uncooperative:
   - Cooperate if h > previous observed count, or
   - Cooperate if the last two observed rounds showed any improvement trend, or
   - Cooperate if the previous round had at least one more cooperator than the round before it.
   - Otherwise defect.

5. Recovery rule  
   After any defection round, return to cooperation immediately if the next observed round reaches h ≥ ceil((n-1)/2).

6. Endgame  
   In the last round, cooperate unless the previous two observed rounds both satisfied the defection condition in rule 3.

7. Minimal-history edge cases  
   - If only one previous round exists, use h and s from that round only.
   - If no previous round exists, cooperate.
   - If any statistic is undefined because of insufficient history, ignore it and fall back to the simpler applicable rule above.

Operational form:

- t = 1: play C
- t > 1:
  - if h ≥ ceil((n-1)/2) or s ≥ 0.5: play C
  - else if h ≤ floor((n-1)/3) and m ≤ floor((n-1)/3): play D
  - else if h increased relative to the previous observed round, or the last two rounds improved consecutively: play C
  - else play D

Keep cooperation as the default response to any sign of reciprocity, and reserve defection only for repeated low-cooperation patterns.
'''

description_SELFISH_1 = '''
Round 1: play D.

Every later round:
- Play D, regardless of the number of cooperators observed in prior rounds.
- Never switch to C.
- Ignore all history except to record it; it does not affect action.

Edge cases:
- If r = 2, play D in both rounds.
- If the previous round had zero cooperators, still play D.
- If the previous round had full cooperation, still play D.
- If cooperation rises, falls, or fluctuates, still play D.
- In the final round, play D.

Compact rule:
```text
for t = 1 to r:
    action[t] = D
```
'''

description_SELFISH_2 = '''
Round 1: play D.

Every later round: play D.

If you want the rule stated as a history-based policy:

```text
For each round t = 1..r:
    play D
```

Decision rule:
- Cooperate in no round.
- Defect in every round, regardless of how many opponents cooperated before.

Edge cases:
- First round: defect because there is no useful history.
- Last round: defect because there is no future to influence.
- Any round after observing full cooperation, partial cooperation, or full defection: defect.
- Any round after a long streak of cooperation by others: defect.

State used:
- None beyond knowing the current round index.
- No thresholds, no retaliation, no forgiveness, no experimentation.

Selfish objective:
- Always take the private endowment and free-ride on any public contributions made by others.
'''

description_SELFISH_3 = '''
Play D in every round.

Decision rule:
- Round 1: D
- Round t = 2 to r - 1: D, regardless of the observed number of cooperating opponents in prior rounds
- Round r: D

History use:
- Ignore all past cooperation counts except to record them if needed; they never change the action
- Never condition on punishing, rewarding, matching, or testing opponents

Edge cases:
- If n = 2 or any other value allowed by the parameters: still always D
- If all opponents cooperated last round: D
- If all opponents defected last round: D
- If cooperation by others would make the current round look favorable: still D

Selfish objective:
- Maximize immediate private payoff each round by keeping the contribution
- Treat every round independently and never spend payoff on contributing to the public project
'''

description_SELFISH_4 = '''
Play D in every round, regardless of history.

Decision rule:
- Round 1: D
- Rounds 2 through r − 1: D
- Final round: D

History use:
- Ignore all observed cooperation counts.
- No retaliation, no reward, no forgiveness.
- Never switch to C under any observed pattern.

Implementation:
```text
for each round t = 1..r:
    choose D
```
'''

description_SELFINTERESTED_1 = '''
- Round 1: play D.

- After each round t, observe x_t = number of opponents who cooperated.

- Maintain a state:
  - `stable = true` if the last two observed rounds both had `x >= n-2`
  - otherwise `stable = false`

- Decision rule for round t+1:
  1. If `stable = true`, play C.
  2. Otherwise, play D.

- Reset rule:
  - If any observed round has `x <= n-3`, set `stable = false` immediately.
  - Require two consecutive rounds of `x >= n-2` before switching back to cooperation.

- Endgame rule:
  - In the final two rounds, play D unless `stable = true` and the last two rounds both had `x = n-1` or `x = n-2`.

- If the first observed round already has `x = n-1`, keep testing with D once more before entering cooperation; only switch to C after the second consecutive round of `x >= n-2`.

- If the observed cooperation level ever collapses to `x = 0`, play D for the rest of the game.
'''

description_SELFINTERESTED_2 = '''
Let

- `obs[t]` = number of opponents who cooperated in round `t`
- `m = n - 1` = number of opponents
- `T = ceil(m * (k - 1) / k)`  # cooperation threshold
- `L = 2`  # punishment length
- `W = 2`  # confirmation window

State:
- `mode ∈ {probe, cooperate, punish}`
- `punish_left ∈ {0,1,2,...}`

Decision rule for round `t`:

1. **Endgame**
   - If `t > r - 2`, play `D`.

2. **First round**
   - Play `D`.

3. **Punishment mode**
   - If `punish_left > 0`, play `D` and decrement `punish_left`.
   - Stay in punishment until it expires.

4. **Cooperation test**
   - If the last `W` observed rounds all satisfy `obs[s] ≥ T`, play `C`.
   - Otherwise play `D`.

5. **Entering punishment**
   - After round `t`, if you played `C` and `obs[t] < T`, set `punish_left = L` for the next rounds.

6. **Re-entering cooperation**
   - After any punishment finishes, require `W` consecutive rounds with `obs[s] ≥ T` before cooperating again.

Operationally:

```text
Round 1: D

For round t = 2 to r:
    if t > r - 2:
        play D
    else if punish_left > 0:
        play D
        punish_left -= 1
    else if obs[t-1] >= T and (t == 2 or obs[t-2] >= T):
        play C
    else:
        play D

    after observing obs[t]:
        if you played C and obs[t] < T:
            punish_left = 2
```

Behavior:
- Defect by default.
- Cooperate only when opponents have shown sustained cooperation.
- Immediately punish any drop below the cooperation threshold.
- Defect in the final two rounds regardless of history.
'''

description_SELFINTERESTED_3 = '''
Cooperate in the first round.

After each round, let m be the number of opponents who cooperated in the previous round, and let q = m / (n - 1).

Use a two-threshold rule:

- Cooperate in round t if:
  - q ≥ θ_high, or
  - q is rising quickly relative to the previous round and was close to θ_high.

- Defect in round t if:
  - q ≤ θ_low, or
  - the game is in the final rounds and q is below θ_high.

Set the thresholds as:
- θ_high = 1 - 1/k
- θ_low = max(0, θ_high - 1/(2(n - 1)))

Decision rule in detail:

1. Round 1:
   - Play C.

2. For round t > 1, based on the observed cooperation count m_{t-1} among the other n - 1 players:
   - If m_{t-1} = n - 1:
     - Play C.
   - Else if m_{t-1} ≥ ceil((n - 1) * θ_high):
     - Play C.
   - Else if m_{t-1} ≤ floor((n - 1) * θ_low):
     - Play D.
   - Else:
     - Play the same action you played in round t - 1.

3. Last-round rule:
   - In round r, play C only if m_{r-1} ≥ ceil((n - 1) * θ_high).
   - Otherwise play D.

4. Recovery rule:
   - If you defected in the previous round but the observed cooperation level in the next round meets the cooperate threshold, immediately return to C.
   - If cooperation falls below the defect threshold for two consecutive rounds, switch to D and stay there until cooperation recovers.

5. Late-game tightening:
   - For the last two rounds, require full or near-full cooperation to keep cooperating:
     - Play C only if m ≥ n - 2.
     - Otherwise play D.

State update:
- Keep track of:
  - your last action,
  - the previous round’s cooperation count among opponents,
  - whether the current round is in the final two rounds.

Compact pseudocode:

- t = 1: play C
- For t > 1:
  - observe m_{t-1}
  - if t == r:
      play C iff m_{t-1} ≥ n - 2, else D
    else if m_{t-1} ≥ ceil((n - 1) * (1 - 1/k)):
      play C
    else if m_{t-1} ≤ floor((n - 1) * max(0, 1 - 1/k - 1/(2(n - 1)))):
      play D
    else:
      repeat last action

Use C as the default only when the observed environment is sufficiently cooperative; otherwise fall back to D, and in the endgame require especially strong evidence of cooperation before continuing to cooperate.
'''

description_SELFINTERESTED_4 = '''
Initialize in DEFECT mode.

For round 1: play D.

For rounds 2 through r-2:
- Let h_{t-1} be the number of opponents who cooperated in round t-1.
- Let h_{t-2} be the number of opponents who cooperated in round t-2, when available.
- Set a high-cooperation threshold  
  T_high = ceil(3(n-1)/4)
- Set a keep-cooperating threshold  
  T_keep = ceil(2(n-1)/3)
- Set a low-cooperation threshold  
  T_low = floor((n-1)/2)

Decision rule:
1. If either of the previous two rounds had h ≤ T_low, play D.
2. Else if the last two observed rounds both had h ≥ T_high, play C.
3. Else if you played C in the previous round and h_{t-1} ≥ T_keep, play C.
4. Otherwise, play D.

Punishment rule:
- After any round with h ≤ T_low, play D for the next 2 rounds regardless of anything else.

Endgame:
- Play D in round r-1.
- Play D in round r.

If the game is too short to apply the full history:
- Round 1: D
- Round 2: C only if round 1 had h ≥ T_high; otherwise D
- Round 3 and onward: use the rules above, with any unavailable history treated as not satisfying the cooperation thresholds.

State update:
- Track only the last two rounds of observed cooperation counts and whether you are currently in punishment mode.
- Reset punishment mode immediately after the required two defecting rounds have been played.
'''

description_OPPORTUNISTIC_1 = '''
Round 1: Cooperate.

Maintain a running estimate of the cooperation level among opponents:
- Let m_t be the number of opponents observed cooperating in round t.
- Let \bar m_t be the average of m_1 through m_t.

Define two thresholds:
- High-cooperation threshold H = ceil((n-1) * (k - 1) / k) + 1
- Low-cooperation threshold L = floor((n-1) * (k - 1) / k)

Decision rule for round t ≥ 2:
1. If the previous round had m_{t-1} ≥ H, cooperate.
2. If the previous round had m_{t-1} ≤ L, defect.
3. If m_{t-1} is between L and H, use the short-run average:
   - Cooperate if \bar m_{t-1} ≥ H
   - Defect otherwise

Endgame rule:
- In the final two rounds, defect unless the previous round had m_{t-1} = n-1.
- In the last round, defect unconditionally if the previous round had fewer than n-1 opponents cooperating.

Recovery rule after a drop:
- If cooperation falls by at least 2 compared to the previous round, defect for the next round.
- Return to cooperation only after observing m_t ≥ H in a later round.

Exploitation rule:
- If opponents sustain cooperation at or above H for two consecutive rounds, continue cooperating as long as that level holds.
- If they remain at n-1 cooperation, mirror with cooperation to keep extracting the public return.
- If they fall even once below H, switch immediately to defection.

Minimal implementation:
```text
t = 1: play C
for t = 2 to r:
    observe m_{t-1}
    if t >= r-1 and m_{t-1} < n-1:
        play D
    else if m_{t-1} >= H:
        play C
    else if m_{t-1} <= L:
        play D
    else:
        play C iff average(m_1..m_{t-1}) >= H, else D
```

This creates an opportunistic posture: cooperate only when the observed crowd is strong enough to make cooperation immediately profitable, and defect whenever the observed cooperation weakens, especially near the end.
'''

description_OPPORTUNISTIC_2 = '''
Let \(o_t\) be the number of opponents who cooperated in round \(t\), so \(0 \le o_t \le n-1\).

**State variables**
- `streak`: number of consecutive recent rounds with \(o_t = n-1\)
- `cooldown`: number of rounds remaining before considering cooperation again

**Decision rule**
1. **Round 1:** play **D**.
2. **If `cooldown > 0`:** play **D** and decrement `cooldown`.
3. **Otherwise, play C only when cooperation is fully established:**
   - play **C** if and only if:
     - \(o_{t-1} = n-1\), and
     - either \(t=2\) or \(o_{t-2} = n-1\)

   In all other cases, play **D**.

**Update rule after each round**
- If \(o_t = n-1\), increment `streak`.
- If \(o_t < n-1\), set `streak = 0` and set `cooldown = 2`.

**Last round**
- Play **D**.

**Interpretation of the rule**
- Defect by default.
- Only cooperate after the group has shown uninterrupted full cooperation for long enough to make cooperation the current norm.
- The moment full cooperation breaks, stop cooperating for at least two rounds before reconsidering.
'''

description_OPPORTUNISTIC_3 = '''
Let \(x_t\) be the number of opponents who cooperated in round \(t\), and let \(p_t = x_t/(n-1)\) be the observed opponent cooperation rate.

Define the support threshold
\[
\theta = \left\lceil \frac{n-1}{k} \right\rceil .
\]

Maintain a mode variable:
- **exploit mode** = defect unless the group is clearly sustaining cooperation
- **support mode** = cooperate while the group keeps paying into the public good

Decision rules:

1. **Round 1**
   - Play **C**.

2. **Round 2**
   - Play **C** if \(x_1 \ge \theta\).
   - Otherwise play **D**.

3. **Rounds 3 through \(r-1\)**
   - Compute the last two observed counts \(x_{t-1}\) and \(x_{t-2}\).
   - Play **C** if all of the following hold:
     - \(x_{t-1} \ge \theta\)
     - \(x_{t-2} \ge \theta\)
     - \(x_{t-1} \ge x_{t-2} - 1\)  (no sharp drop)
   - Otherwise play **D**.

4. **Final round \(r\)**
   - Play **C** only if the previous two rounds both satisfied:
     - \(x_{r-1} \ge \theta\)
     - \(x_{r-2} \ge \theta\)
   - Otherwise play **D**.

5. **Fallback rule after any weak round**
   - If in any round \(t\) you observe \(x_t < \theta\), switch immediately to **exploit mode**:
     - play **D** in the next round
     - keep playing **D** until you observe two consecutive rounds with \(x_t \ge \theta\)

6. **Recovered cooperation**
   - If two consecutive rounds meet the threshold, return to **support mode** and play **C**.

This strategy starts by testing for cooperation, supports groups that repeatedly sustain enough cooperation, and immediately defects when the group falls below the cooperation threshold.
'''

description_OPPORTUNISTIC_4 = '''
State variable: `last_x`, the number of opponents who cooperated in the previous round.

Initialize:
- Round 1: play `C`.

For each round `t >= 2`, after observing `x_{t-1}`:
- Let `f = x_{t-1} / (n - 1)`.
- Let `f_prev = last_x / (n - 1)` if `t >= 3`; otherwise treat `f_prev = f`.

Decision for round `t`:
- If `t >= r - 1`: play `D`.
- Else if `f >= 1/2` and `f >= f_prev - 1/(n - 1)`: play `C`.
- Else: play `D`.

Update:
- Set `last_x = x_{t-1}` after each observation.

Behavioral interpretation:
- Open with cooperation to test the field.
- Stay cooperative only while at least half of the opponents keep cooperating and cooperation is not dropping sharply.
- Defect immediately when cooperation weakens below that level.
- Defect in the final two rounds to harvest any remaining cooperation.
'''

description_INDIVIDUALISTIC_1 = '''
Play D in every round.

Decision rule:
- Round 1: D
- Round t = 2 to r: D, regardless of the observed number of cooperating opponents in prior rounds
- Last round: D
- If any tie-break or randomization is required by the environment, assign probability 1 to D and 0 to C

History use:
- Record the aggregate cooperation counts each round only as information.
- Do not reciprocate, punish, reward, or “test” cooperation.
- Never switch to C based on opponent behavior, because an individualistic response is to keep the private endowment whenever possible.

Edge cases:
- If all opponents cooperated previously, still play D.
- If no opponents cooperated previously, still play D.
- If cooperation among opponents rises or falls over time, still play D.
- If the final round is reached, still play D.

State form:
- Internal state is trivial: `mode = D`
- Pseudocode:
  ```text
  for each round t:
      observe previous aggregate cooperation count
      action = D
  ```
'''

description_INDIVIDUALISTIC_2 = '''
Round 1: play D.

For round t > 1, let p_{t-1} be the fraction of your opponents who cooperated in round t-1.

Maintain:
- recent_avg = average of p over the last up to 3 rounds
- recent_floor = minimum of p over the last up to 2 rounds

Decision rule:
- If t = r: play D
- Else play C only if all of the following hold:
  - p_{t-1} ≥ 1/2
  - recent_avg ≥ 2/3
  - recent_floor ≥ 1/2
- Otherwise play D

Adjustment rule after a defection-heavy round:
- If p_{t-1} < 1/3, then require two consecutive rounds with p ≥ 1/2 before returning to C.
- If p_{t-1} < 1/6, reset to full defection mode: play D for the next 2 rounds regardless of the next single-round observation, then reassess.

Adjustment rule after a cooperation-stable stretch:
- If p_{t-1} ≥ 2/3 for 2 straight rounds, continue cooperating while the stability conditions remain true.

Edge cases:
- If t = 2, recent_avg and recent_floor are based only on round 1.
- If there are fewer than 2 prior rounds, use only the available history.
- If the observed cooperation rate is exactly on a threshold, treat it as meeting the threshold.
- If a round is missed in the history, treat it as p = 0.

Behavioral posture:
- Start skeptical.
- Reward sustained high cooperation with conditional cooperation.
- Immediately stop cooperating when cooperation falls below the acceptable band.
- Never cooperate in the final round.
'''

description_INDIVIDUALISTIC_3 = '''
Initialize state = DEFECT.

For each round t:

1. Observe x_{t-1} = number of opponents who cooperated in the previous round.
2. Compute cooperation rate among opponents:
   - q_{t-1} = x_{t-1} / (n - 1)

Decision rule:
- Round 1: play D.
- Round r: play D.
- Rounds 2 through r-1:
  - Play C only if both of the following are true:
    - x_{t-1} = n - 1
    - x_{t-2} = n - 1
  - Otherwise play D.

Update rule:
- If you played C and the next observed round has x_{t} = n - 1, keep the state eligible for cooperation.
- If any round shows x_t < n - 1, reset state = DEFECT.

Compact pseudocode:

```
if t == 1 or t == r:
    action = D
else:
    if last_round_opponents_cooperated == n-1 and round_before_last_opponents_cooperated == n-1:
        action = C
    else:
        action = D
```

If you want a slightly more responsive version with the same individualistic posture:

- Cooperate in round t only if the last two rounds each had at least n-2 cooperating opponents.
- Otherwise defect.
- After any round with fewer than n-2 cooperating opponents, defect for the next two rounds before considering cooperation again.
'''

description_INDIVIDUALISTIC_4 = '''
Let `q_t` be the number of opponents who cooperated in round `t`.

Define a cooperation threshold

`T = ceil((n - 1) * (1 - 1/k))`

and a stricter recovery threshold

`R = max(0, T - 1)`.

Strategy state:
- `stable = false`

Decision rule for round `t`:

1. If `t = 1`, play `D`.
2. If `t >= r - 1`, play `D`.
3. Otherwise:
   - If `stable = false`:
     - Play `C` only if `q_(t-1) >= T` and `q_(t-2) >= T` when `t >= 3`.
     - Otherwise play `D`.
     - If you play `C`, set `stable = true`.
   - If `stable = true`:
     - Play `C` if `q_(t-1) >= R`.
     - Play `D` if `q_(t-1) < R` and set `stable = false`.

Extra behavior:
- If `q_t = n - 1` for two consecutive observed rounds, stay in `C` mode until that pattern breaks.
- If cooperation collapses for one round, immediately revert to `D`.
- Never cooperate in the final two rounds.
- After any round with `q_t = 0`, defect for the next two rounds before reconsidering cooperation.

Implementation form:

```text
round 1: D

for t = 2 to r:
    if t >= r - 1:
        action = D
    else if stable == false:
        if t >= 3 and q[t-1] >= T and q[t-2] >= T:
            action = C
            stable = true
        else:
            action = D
    else:
        if q[t-1] >= R:
            action = C
        else:
            action = D
            stable = false
```

This keeps the default posture as defection, cooperates only after sustained high cooperation by others, and drops cooperation immediately when the observed cooperation level weakens.
'''
