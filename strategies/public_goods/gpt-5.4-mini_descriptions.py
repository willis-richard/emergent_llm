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

description_COLLECTIVE_5 = '''
Round 1: cooperate.

Maintain two running statistics after each round t:
- a_t = number of opponents who cooperated in round t
- s_t = average opponent cooperation rate over rounds 1..t, where  
  s_t = (a_1 + ... + a_t) / ((n - 1) t)

Use three regimes:

1. Establishment regime
- If s_t ≥ θ_high, cooperate.
- If s_t ≤ θ_low, defect.
- Otherwise, mirror the recent direction of the group:
  - cooperate if a_t > a_{t-1}
  - defect if a_t < a_{t-1}
  - if a_t = a_{t-1}, repeat your previous action

Set thresholds:
- θ_high = 1/2
- θ_low = 1/3

2. Recovery regime
- If the last two rounds each had a_t ≥ ceil((n - 1)/2), cooperate unconditionally for the next two rounds.
- If the last two rounds each had a_t = 0, defect unconditionally until at least one round with a_t > 0 occurs.
- If cooperation collapses from a_t ≥ ceil((n - 1)/2) to a_t < ceil((n - 1)/3), switch to defect for one round, then re-enter the Establishment regime.

3. Endgame regime
- For the final two rounds, cooperate only if:
  - s_t ≥ θ_high, and
  - the last round had a_t ≥ ceil((n - 1)/2)
- Otherwise defect.

Action rule by round:
- Round 1: C
- Rounds 2 to r - 2: apply Establishment regime, modified by Recovery regime whenever its conditions are met
- Rounds r - 1 and r: apply Endgame regime

Update rules:
- After each round, compute a_t and s_t from the observed aggregate.
- Track whether the previous action was C or D for tie-breaking when a_t = a_{t-1}.
- Reset the recovery counter whenever a round meets the high-cooperation condition.

Commitment rule:
- Whenever you defect, do so as a signal to protect the collective only after a clear breakdown in participation.
- Whenever the group’s cooperation is strong and stable, return to cooperation immediately and stay there as long as the aggregate remains above the high threshold.
'''

description_COLLECTIVE_6 = '''
State variables:
- `mode ∈ {build, punish}`
- `streak ∈ {0,1,2,...}` = consecutive rounds in which opponent cooperation met the recovery condition

Define:
- `m_t` = number of cooperating opponents observed after round `t`
- `q = ceil((n - 1) * (1 - 1/k))`
- `Q = min(n - 1, q + 1)`

Decision rule:
1. Round 1: play `C`.
2. Round `t > 1`:
   - If `mode = build`:
     - Play `C` if `m_{t-1} ≥ q`
     - Play `D` if `m_{t-1} < q`, and set `mode = punish`, `streak = 0`
   - If `mode = punish`:
     - Play `D`
     - If `m_{t-1} ≥ Q`, increment `streak`; otherwise set `streak = 0`
     - If `streak ≥ 2`, set `mode = build`
3. Last round `r`:
   - If `mode = build` and `m_{r-1} ≥ q`, play `C`
   - Otherwise play `D`

Recovery logic:
- Return to cooperation only after two consecutive rounds of strong opponent cooperation.
- A single weak round resets the recovery count.
- Any renewed breakdown during recovery restarts punishment immediately.

Interpretation of the collective stance:
- Cooperate by default.
- Reward sustained cooperation with immediate cooperation.
- Respond to low cooperation with short, structured defection.
- Rejoin the cooperative mode as soon as the group restores the target level of cooperation.
'''

description_COLLECTIVE_7 = '''
Maintain three states: `cooperative`, `punishing`, `probation`.

Let `q_t = (number of opponents who cooperated in round t) / (n - 1)`.

Initialize:
- `state = cooperative`
- `punish_left = 0`

Decision rule for round `t`:

1. If `t = 1`, play `C`.

2. If `state = punishing`:
   - play `D`
   - decrement `punish_left`
   - if `punish_left = 0`, set `state = probation`
   - stop

3. If `state = probation`:
   - play `C` if `q_{t-1} >= 1/2`
   - play `D` otherwise
   - if `q_{t-1} >= 1/2`, set `state = cooperative`
   - otherwise keep `state = probation`
   - stop

4. If `state = cooperative`:
   - play `C` if `q_{t-1} >= 1/2`
   - play `D` if `q_{t-1} < 1/2`
   - if `q_{t-1} < 1/2` for two consecutive rounds, set `state = punishing` and `punish_left = 2`

Extra memory rule:
- Define “two consecutive rounds below half” using the last two observed values of `q`.
- If `t = 2`, treat the single prior round as sufficient for the test: enter `punishing` only if `q_1 < 1/2` and your own round-2 action is `D`.

Final-round handling:
- Use the same rule as any other round; no special deviation.
- If the last two observed rounds both had `q >= 1/2`, play `C`.
- Otherwise follow the current state rule exactly.

Optional strengthening:
- Replace the threshold `1/2` with `2/3` if you want stricter collective cooperation.
- Replace `punish_left = 2` with `punish_left = ceil(r/10)` for longer punishment cycles.
'''

description_COLLECTIVE_8 = '''
Maintain a shared target cooperation level and condition your move on the recent observed cooperation rate.

State variables:
- `m_t`: number of opponents who cooperated in round `t`
- `M_t = m_t / (n-1)`: observed opponent cooperation rate in round `t`
- `H_t`: smoothed cooperation score
- `S_t`: trust state, either `cooperative` or `defensive`
- `L_t`: consecutive rounds with low observed cooperation

Initialization:
- Round 1: play `C`
- Set `H_1 = 1`
- Set `S_1 = cooperative`
- Set `L_1 = 0`

Update after each round `t`:
- If `M_t >= 1/2`, set `L_{t+1} = 0`
- If `M_t < 1/2`, set `L_{t+1} = L_t + 1`
- Update smoothed score:
  - `H_{t+1} = (2/3) * H_t + (1/3) * M_t`

Decision rule for round `t+1` when `t < r`:
1. If `t + 1 = r`, play `D` if `M_t < 1/2`; otherwise play `C`
2. Else if `L_{t+1} >= 2`, play `D` and set `S_{t+1} = defensive`
3. Else if `H_{t+1} >= 1/2`, play `C` and set `S_{t+1} = cooperative`
4. Else play `D` and set `S_{t+1} = defensive`

Recovery rule:
- While in `defensive` state, cooperate again as soon as the observed cooperation rate reaches at least `1/2` for one round
- After any cooperative round with `M_t >= 1/2`, return to `cooperative` state immediately

Endgame rule:
- In the final two rounds, require stronger evidence to cooperate:
  - If `t >= r-2`, play `C` only if `M_t >= 2/3`
  - Otherwise play `D`

Compact pseudocode:
```text
Round 1: C
H = 1
L = 0
state = cooperative

For round t = 2 to r:
    if t == r:
        if M_{t-1} >= 1/2 and H >= 1/2:
            play C
        else:
            play D
    else if t >= r-1:
        if M_{t-1} >= 2/3:
            play C
        else:
            play D
    else:
        H = (2/3)*H + (1/3)*M_{t-1}
        if M_{t-1} < 1/2:
            L = L + 1
        else:
            L = 0

        if L >= 2:
            play D
            state = defensive
        else if H >= 1/2:
            play C
            state = cooperative
        else:
            play D
            state = defensive
```

Behavioral logic:
- Begin with cooperation to signal willingness to build a cooperative majority.
- Keep cooperating while the observed majority remains cooperative.
- Defect after two consecutive weak cooperation rounds.
- Return to cooperation immediately once the group re-establishes majority cooperation.
- Tighten the cooperation requirement near the end so the final rounds track actual collective behavior rather than hope for recovery.
'''

description_COLLECTIVE_9 = '''
Round 1: cooperate.

For round t > 1, let m_{t-1} be the number of opponents who cooperated in round t-1, and let p_{t-1} = m_{t-1} / (n-1).

Maintain one internal state variable, cooperation_mode, initialized to true.

Update rule after each observed round:
- If p_{t-1} = 1, set cooperation_mode = true.
- If p_{t-1} = 0, set cooperation_mode = false.
- If 0 < p_{t-1} < 1, keep cooperation_mode unchanged unless one of the trigger conditions below fires.

Trigger conditions:
- Defection trigger: if p_{t-1} ≤ 1/3, set cooperation_mode = false for the next round.
- Restoration trigger: if p_{t-1} ≥ 2/3 for two consecutive rounds, set cooperation_mode = true.
- Stability trigger: if p_{t-1} is between 1/3 and 2/3, continue the current mode.

Action rule for round t:
- If cooperation_mode = true, play C.
- If cooperation_mode = false, play D.

Reset rule:
- If you have played D for three consecutive rounds and observe p_{t-1} ≥ 2/3, switch to cooperation_mode = true immediately.
- If you have played C for three consecutive rounds and observe p_{t-1} ≤ 1/3, switch to cooperation_mode = false immediately.

Last round:
- Play C if and only if cooperation_mode = true and p_{r-1} ≥ 1/2.
- Otherwise play D.

Special cases:
- If n = 2, replace thresholds 1/3 and 2/3 with 0 and 1 respectively, so any observed cooperation by the other player keeps cooperation_mode true, and any observed defection switches it false.
- If two adjacent rounds produce the same aggregate count m, treat that as confirmation and strengthen the current mode.
- If the observed aggregate is impossible under the current mode’s recent history, prioritize the most recent observation and update immediately.

Collective alignment:
- Start by contributing to establish cooperation.
- Stay cooperative while a clear majority of opponents cooperates.
- Fall back to defection when cooperation collapses.
- Re-enter cooperation only after sustained restoration, not after a single isolated cooperative move.
- Mirror the group’s aggregate behavior rather than tracking individuals.
'''

description_COLLECTIVE_10 = '''
Maintain a state variable `mode ∈ {build, cooperate, punish}` and a counter `recover`.

Let `x_t` be the number of opponents who cooperated in round `t` and `p_t = x_t / (n-1)`.

Set two fixed thresholds from the game size:
- `L = ceil((n-1)/2)`
- `H = ceil(2(n-1)/3)`

Decision rules:

- Round 1: play `C`.
- Round 2: play `C`.

After observing round `t`, update as follows:

1. If `x_t >= H`:
   - increment `recover` by 1
   - if `recover >= 2`, set `mode = cooperate`
2. If `L <= x_t < H`:
   - set `recover = 0`
   - if `mode != punish`, set `mode = cooperate`
3. If `x_t < L`:
   - set `recover = 0`
   - set `mode = punish` for the next 2 rounds

Action choice by mode:

- `build`: play `C`
- `cooperate`: play `C`
- `punish`: play `D`

Punishment rule:

- If any round has `x_t < L`, defect for the next 2 rounds.
- While punishing, do not leave punishment early.
- After the 2 punishment rounds, return to `cooperate` only if the last two observed rounds both satisfied `x >= H`; otherwise extend punishment by 2 more rounds.

Last round:

- If in `cooperate`, play `C` when the most recent observed round had `x >= L`; otherwise play `D`.
- If in `punish`, play `D`.

Full update pseudocode:

```text
state = build
recover = 0
punish_left = 0

for t in 1..r:
    if t in {1,2}:
        action = C
    else if punish_left > 0:
        action = D
        punish_left -= 1
    else:
        action = C

    observe x_t

    if x_t < L:
        recover = 0
        punish_left = max(punish_left, 2)
        state = punish
    else if x_t >= H:
        recover += 1
        if recover >= 2:
            state = cooperate
    else:
        recover = 0
        state = cooperate
```

The collective stance is: begin with cooperation, keep cooperating while a clear majority is also cooperating, and impose short, synchronized punishment only when cooperation drops below a broad majority.
'''

description_COLLECTIVE_11 = '''
Play a conditional cooperation rule with a moving majority threshold and a short-memory forgiveness mechanism.

Let:
- `m_t` = number of opponents who cooperated in round `t`
- `M_t = m_t / (n - 1)` = observed opponent cooperation rate
- `H` = number of recent rounds to inspect, set `H = min(3, r - 1)`
- `\bar M_t` = average of `M` over the last `H` observed rounds before round `t`, using all available past rounds if fewer than `H` exist

Decision rule for round `t`:

1. **Round 1**
   - Play `C` if `k > 1`
   - Otherwise play `D`

2. **Rounds 2 through r-1**
   - Cooperate if both conditions hold:
     - `\bar M_t >= 1 / k`
     - In the most recent round, `M_{t-1} >= 1 / k - 1/(2(n-1))`
   - Defect otherwise

3. **Last round**
   - Cooperate only if both conditions hold:
     - `\bar M_t >= 1 / k`
     - At least `H-1` of the last `H` observed rounds had `M >= 1 / k`
   - Otherwise defect

Adaptive update rule after each round:

- If we cooperated and observed `M_t >= 1 / k`, stay cooperative next round.
- If we cooperated and observed `M_t < 1 / k`, switch to defect next round unless this is a single isolated dip and the previous `H-1` rounds all satisfied `M >= 1 / k`; in that case, cooperate one more round before switching.
- If we defected and observed `M_t >= 1 / k` for two consecutive rounds, return to cooperation.

Edge cases:

- If `n = 2`, use the same rule with `M_t` equal to the other player’s action.
- If `r = 2`, apply the round-1 rule in the first round and the last-round rule in the second.
- If all past rounds are unavailable or shorter than `H`, compute `\bar M_t` from the rounds that do exist.
- If the observed cooperation rate is exactly at threshold, treat it as cooperative and continue cooperating.

Collective posture:

- Start by cooperating.
- Continue cooperating only while the group is meeting the cooperation threshold often enough.
- Respond to persistent defection by switching to defection.
- Return to cooperation immediately after the group demonstrates sustained cooperation again.
'''

description_COLLECTIVE_12 = '''
Maintain a shared target cooperation rate and update it from the observed cooperation history.

State variables:
- `H_t`: cumulative number of opponent cooperations observed in rounds `1..t`
- `m_t`: number of completed rounds
- `p_t = H_t / (m_t * (n-1))` for `m_t > 0`
- `T_t`: current cooperation threshold in `[0, n-1]`

Initialization:
- Set `T_1 = ceil((n-1) / k)`
- Set `T_1 = min(max(T_1, 1), n-1)`

Round `t = 1`:
- Cooperate.

For each round `t >= 2`:
1. Compute the last-round opponent cooperation count `x =` number of opponents who cooperated in round `t-1`.
2. Update the running cooperation rate `p_t`.
3. Update threshold:
   - If `x >= T_{t-1}` for the last two rounds, set `T_t = max(1, T_{t-1} - 1)`
   - If `x < T_{t-1}` for two consecutive rounds, set `T_t = min(n-1, T_{t-1} + 1)`
   - Otherwise keep `T_t = T_{t-1}`

Decision rule for round `t`:
- Cooperate if `x >= T_t`
- Defect if `x < T_t`

Endgame rule:
- If `t >= r - 1`, cooperate only if `x = n - 1`; otherwise defect.

Recovery rule after shocks:
- If at any time `x = 0`, defect for the next round.
- Return to cooperation only after a round with `x >= T_t`.

Collective alignment rule:
- Treat cooperation as the default state.
- Defect only to protect against sustained low cooperation by others.
- Once the observed cooperation level rises to the current threshold, resume cooperation immediately and stay cooperative while the threshold is met.

Compact pseudocode:

```text
T = ceil((n-1)/k)
T = clamp(T, 1, n-1)

if t == 1:
    play C
else:
    x = cooperators_observed_last_round

    if last_two_x_values >= T:
        T = max(1, T-1)
    else if last_two_x_values < T:
        T = min(n-1, T+1)

    if t >= r-1:
        if x == n-1:
            play C
        else:
            play D
    else if x == 0:
        play D
    else if x >= T:
        play C
    else:
        play D
```


'''

description_COLLECTIVE_13 = '''
Round 1: cooperate.

Let \(m_t\) be the number of opponents who cooperated in round \(t\), and let \(a_t\) be your action in round \(t\). Let \(N=n-1\).

Maintain two running statistics from past rounds only:
- \(A_t\): average opponent cooperation count over rounds \(1,\dots,t\)
- \(L_t\): length of the current consecutive low-cooperation streak, where a round is “low” if \(m_t < \lceil N/2 \rceil\)

Decision rule for round \(t+1\) after observing round \(t\):

1. **Emergency breakdown rule**
   - If \(m_t = 0\), play \(D\) next round.
   - Stay with \(D\) until a round occurs with \(m_t \ge \lceil 2N/3 \rceil\).

2. **Collective cooperation rule**
   - If \(m_t \ge \lceil 2N/3 \rceil\), play \(C\) next round.
   - If the last two rounds both satisfy \(m \ge \lceil 2N/3 \rceil\), keep playing \(C\) as long as this condition holds.

3. **Conditional support rule**
   - If \(\lceil N/2 \rceil \le m_t < \lceil 2N/3 \rceil\), play the same action you played in round \(t\):
     - if you cooperated in round \(t\), cooperate again
     - if you defected in round \(t\), defect again

4. **Backoff rule**
   - If \(m_t < \lceil N/2 \rceil\), increment \(L_t\).
   - If \(L_t \ge 2\), play \(D\) next round.
   - Remain defecting until one of these occurs:
     - \(m_t \ge \lceil 2N/3 \rceil\), or
     - the last three rounds contain at least two rounds with \(m \ge \lceil N/2 \rceil\)

5. **Reset rule**
   - Any round with \(m_t \ge \lceil 2N/3 \rceil\) resets \(L_t\) to 0 and clears the defecting state.

6. **Final round**
   - In the last round, play \(C\) if and only if the previous round had \(m_{r-1} \ge \lceil N/2 \rceil\); otherwise play \(D\).

Compact pseudocode:

```text
if round == 1:
    play C
else:
    if last_round_cooperators == 0:
        play D
    else if last_round_cooperators >= ceil(2N/3):
        play C
        reset breakdown_state
    else if last_round_cooperators >= ceil(N/2):
        if previous_action == C:
            play C
        else:
            play D
    else:
        increment low_streak
        if low_streak >= 2:
            play D
        else:
            play previous_action

    if in_defecting_state and last_round_cooperators >= ceil(2N/3):
        exit defecting_state

if round == r:
    if previous_round_cooperators >= ceil(N/2):
        play C
    else:
        play D
```

Interpretation of the collective mindset:
- Support the group when cooperation is broadly present.
- Withdraw support quickly when cooperation breaks down.
- Reopen cooperation immediately when strong collective cooperation reappears.
- Use a short memory for punishment, so the group can recover from temporary instability.
'''

description_COLLECTIVE_14 = '''
**State variables**

- `m_t`: number of opponents who cooperated in round `t`
- `q_t = (1 + m_t) / n`: observed cooperation rate in round `t` including self if you cooperated
- `A_t`: smoothed cooperation estimate after round `t`
- Initialize `A_0 = 1`

**Parameters**

- `high = 0.60`
- `low = 0.35`
- `recover = 0.50`
- `floor = 1 / n`
- `alpha = 0.7`

**Decision rule in round 1**

- Play `C`

**Update rule after each round `t`**

- Update smoothed estimate:
  - `A_t = alpha * A_{t-1} + (1 - alpha) * q_t`

**Decision rule for round `t+1`**

1. **If the previous two rounds were both very cooperative**
   - If `A_t >= high`, play `C`

2. **If cooperation has dropped materially**
   - If `A_t <= low`, play `D`

3. **If cooperation is in the middle range**
   - Play `C` if `q_t >= recover`
   - Otherwise play `D`

**Late-game rule**

- In the last round, play the same action you would choose from the rule above using the most recent history.
- Do not switch to unconditional defection solely because the game is ending.

**Recovery rule after a low-cooperation period**

- If you have played `D` for one or more rounds and then observe `A_t >= recover`, immediately return to `C`.

**Stability rule**

- If the observed cooperation count stays unchanged for three consecutive rounds, keep your current action unless the rule above forces a switch.

**Collective orientation**

- Begin by contributing.
- Keep contributing while the group remains broadly cooperative.
- Defect only when the group’s observed cooperation falls below a clear threshold.
- Rejoin cooperation as soon as the group recovers.
'''

description_COLLECTIVE_15 = '''
Use a phased conditional-cooperation rule based on the observed number of cooperators among the other players.

Let:
- `m_t` = number of opponents observed to cooperate in round `t`
- `M_t = m_t + 1` if you cooperated in round `t`, else `m_t`
- `q_t = m_t / (n - 1)` = observed cooperation rate among opponents in round `t`
- `H_t` = history of all prior `m_1, ..., m_t`

Decision rule for round `t`:

1. Initial round
- Cooperate in round 1.

2. Ongoing rule
- Maintain a running cooperation benchmark:
  - `B_t = max( ceil((n-1)/k), ceil(median(m_1, ..., m_t)) )`
- Cooperate in round `t+1` if and only if both conditions hold:
  - `m_t >= B_t`
  - `q_t >= 0.5`
- Otherwise defect.

3. Recovery rule
- If the last two rounds both satisfied `m_t < B_t`, defect until a recovery round occurs.
- A recovery round is one where `m_t >= B_t` and `q_t >= 0.5`.
- After a recovery round, cooperate again immediately.

4. Escalation rule for sustained cooperation
- If `m_t = n-1` for two consecutive rounds, cooperate for the next `min(3, r-t)` rounds unless a round occurs with `m_t = 0`.
- If any round has `m_t = 0`, switch to defecting for the next round.

5. Endgame rule
- In the last round, cooperate only if the last three observed rounds each had `m_t >= B_t`.
- Otherwise defect.

6. Tie and threshold handling
- If `k` is very close to `n`, set `B_t = 1` and require only `q_t >= 0.5`.
- If `n = 2`, cooperate in round 1, then in round `t+1` cooperate iff the other player cooperated in round `t`.

Pseudocode:

```
round 1:
    play C

for t = 1 to r-1:
    B_t = max(ceil((n-1)/k), ceil(median(m_1..m_t)))

    if t == r-1:
        if m_t >= B_t and m_{t-1} >= B_{t-1} and m_{t-2} >= B_{t-2}:
            play C
        else:
            play D
    else if m_t == 0:
        play D
    else if (m_t >= B_t) and (m_t / (n-1) >= 0.5):
        play C
    else if (m_t < B_t) and (m_{t-1} < B_{t-1}):
        play D
    else:
        play D
```

Behavioral posture:
- Start cooperatively.
- Keep cooperating while the observed group stays at or above the cooperation threshold.
- Defect quickly after repeated low cooperation.
- Resume cooperation immediately after a clear recovery.
- End conservatively unless cooperation has been stable late in the game.
'''

description_COLLECTIVE_16 = '''
Round 1: play C.

For rounds t = 2, 3, ..., r:

1. Let `o1` be the number of opponents who cooperated in round `t-1`.
2. Let `ō` be the average number of cooperating opponents over the last `m = min(3, t-1)` rounds.
3. Define:
   - `high = n - 1` if `n <= 3`, otherwise `high = ceil(2(n-1)/3)`
   - `recover = ceil((n-1)/2)`

Decision rule:
- Play C if both conditions hold:
  - `o1 >= high`
  - `ō >= high`
- Otherwise, play D.

Recovery rule after a low-cooperation round:
- If the previous round had `o1 < recover`, require two consecutive rounds with `o >= high` before returning to C.
- If the previous round had `o1 >= recover` but not `high`, allow immediate return to C only if the 3-round average `ō` is at least `high`.

Last round:
- Apply the same rule as any other round; do not special-case it.

If the history is unavailable for any reason, default to C only in round 1, then to D until valid observations resume.
'''

description_COLLECTIVE_17 = '''
Start with cooperation.

Maintain a target cooperation threshold T that depends on the game size:
- If n ≤ 4: T = n - 1
- If 5 ≤ n ≤ 8: T = ceil(0.75 × (n - 1))
- If n > 8: T = ceil(0.8 × (n - 1))

Round 1:
- Play C.

For every round t > 1:
- Let x be the number of opponents who cooperated in round t - 1.
- Let y = x + 1 if you cooperated last round, or y = x if you defected last round.
- Estimate prior-round total cooperation as y.

Decision rule:
- Play C if y ≥ T.
- Play D if y < T.

Adjustment for repeated low cooperation:
- If the estimated total cooperation has been below T for 2 consecutive rounds, switch to D and stay with D until the estimated total cooperation reaches T again.

Adjustment for sustained cooperation:
- If the estimated total cooperation has met or exceeded T for 2 consecutive rounds, play C for the next round and keep playing C as long as the threshold continues to be met.

Endgame:
- In the final round, play C if the estimated total cooperation in the previous round met or exceeded T; otherwise play D.

Special handling of unstable histories:
- If your own last action is unknown or ambiguous, assume you cooperated last round when estimating y.
- If the observed opponent cooperation count is unchanged for 3 rounds in a row, mirror the collective state:
  - if the count is at or above T - 1, play C;
  - otherwise play D.

Summary behavior:
- Cooperate immediately.
- Keep cooperating while the group’s observed cooperation stays above the threshold.
- Defect quickly after a drop below threshold.
- Re-enter cooperation as soon as the group returns to the threshold.

'''

description_COLLECTIVE_18 = '''
State variables:
- `q_t = observed_cooperators_t / (n - 1)` for each completed round `t`
- `trust ∈ {high, low}`, initialized to `high`
- `good_streak = 0`

Set the cooperation threshold:
- `θ = max(1/2, 1 - 1/k)`

Decision rule for round `t`:

1. **Round 1**
   - Play `C`.

2. **Rounds 2 through r**
   - Let `q_prev = q_{t-1}`
   - Let `q_prev2 = q_{t-2}` if `t > 2`, otherwise treat it as unavailable

   **If `trust = high`:**
   - Play `C` if `q_prev ≥ θ`
   - Otherwise play `D` and set `trust = low`

   **If `trust = low`:**
   - Play `C` only if both conditions hold:
     - `q_prev ≥ θ`
     - either `t = 2`, or `q_prev2 ≥ θ`
   - If you play `C`, increment `good_streak`; otherwise reset `good_streak = 0`
   - Return to `trust = high` after `good_streak = 2`
   - Otherwise play `D`

Update after each round:
- Observe `x_t`, compute `q_t = x_t / (n - 1)`
- If `q_t < θ`, set `trust = low` and `good_streak = 0`
- If `q_t ≥ θ`, leave `trust` unchanged unless the recovery condition above is met

Edge handling:
- If `n = 2`, then `q_t` is either `0` or `1`, and the same rules apply unchanged.
- On the final round, use the same rule as any other round; do not switch behavior just because the game is ending.
- If the previous-round cooperation rate is exactly on the threshold, treat it as acceptable cooperation.

Collective posture:
- Start cooperative.
- Keep cooperating while the group stays above the cooperation threshold.
- Defect immediately when the group falls below that threshold.
- Re-enter cooperation only after the group shows sustained recovery.
'''

description_COLLECTIVE_19 = '''
State variables:
- `mode ∈ {COOPERATE, DEFEND}` initialized to `COOPERATE`
- `streak ∈ {0,1,2}` counts consecutive rounds where opponent cooperation met the support threshold
- `q = ceil((n - 1) / 2)`  // minimum opponent cooperators required for collective support

Decision rule for round 1:
- Play `C`

After each round `t` from 1 to `r - 1`, observe `m_t` = number of cooperating opponents.

Update rule:
- If `m_t >= q`:
  - `streak = min(streak + 1, 2)`
- Else:
  - `streak = 0`

Mode transition:
- If `mode = COOPERATE` and `m_t < q`:
  - `mode = DEFEND`
- If `mode = DEFEND` and `streak = 2`:
  - `mode = COOPERATE`

Action rule for round `t + 1`:
- If `mode = COOPERATE`, play `C`
- If `mode = DEFEND`, play `D`

Edge cases:
- If `n = 2`, then `q = 1`, so cooperation continues only when the other player cooperated in the previous round.
- If all opponents cooperated in the previous round, always play `C` next round.
- If no opponent cooperated in the previous round, play `D` until two consecutive rounds meet the support threshold.
- In the final round, use the same action rule as above; no special exception.

Collective posture:
- Begin by cooperating.
- Stay cooperative while a clear majority of the group is cooperating.
- Withdraw support immediately when collective support falls below majority.
- Re-enter cooperation only after support is restored for two consecutive rounds.
'''

description_COLLECTIVE_20 = '''
Let the observed number of cooperating opponents in round t be x_t.

Define the collective cooperation threshold  
T = ceil((n - 1) / k)

State variable:
- trust = true at start
- streak = 0

Decision rule for round t:

1. Round 1:
   - Play C.

2. After each round t:
   - If x_t ≥ T:
     - streak += 1
   - Else:
     - streak = 0

   - If streak ≥ 2:
     - trust = true
   - If x_t < T:
     - trust = false

3. For round t + 1:
   - If trust = true:
     - Play C
   - If trust = false:
     - Play D

Edge handling:
- If the group has just returned to the threshold after a low-cooperation round, require two consecutive threshold-meeting rounds before fully restoring cooperation.
- If cooperation collapses below threshold in any round, switch the whole group to D until the observed cooperation level recovers.
- In the last round, use the same rule as any other round; do not change behavior just because the game is ending.

Collective mindset:
- Begin by extending trust.
- Cooperate when the group is demonstrating broad cooperation.
- Defect as a unified response when the group is not sustaining cooperation.
- Restore cooperation only after the group has shown repeated commitment again.
'''

description_COLLECTIVE_21 = '''
**Collective Adaptive Contribution Strategy**

Let \(m_t\) be the number of opponents who cooperated in round \(t\), so \(0 \le m_t \le n-1\).

### State
Maintain:
- \(S_t\): smoothed estimate of cooperative support among opponents
- \(L_t\): streak of recent rounds with low cooperation

Initialize:
- \(S_1 = \frac{1}{2}\)
- \(L_1 = 0\)

Update after each round \(t\):
\[
S_{t+1} = \frac{2S_t + \frac{m_t}{n-1}}{3}
\]

### Decision rule for round \(t\)
Compute expected cooperative support:
\[
\hat{p}_t = S_t
\]

Cooperate if and only if all of the following hold:
1. \(t = 1\), or \(\hat{p}_t \ge \theta_t\), or the recent trend is improving.
2. The recent trend condition is:
   \[
   m_{t-1} > m_{t-2} \quad \text{or} \quad m_{t-1} = n-1
   \]
   when those rounds exist.
3. The endgame condition has not activated.

Otherwise defect.

### Threshold schedule
Use a decreasing cooperation threshold:
\[
\theta_t = \frac{1}{k} + \frac{1}{10}\left(1 - \frac{t-1}{r-1}\right)
\]
clipped to \([0,1]\).

So:
- early rounds require stronger observed cooperation
- later rounds require only slightly above the minimum sustainable level

### Endgame rule
For the last two rounds:
- If \(t \ge r-1\), cooperate only if at least \(n-2\) opponents cooperated in the previous round.
- If \(t = r\), defect unless \(m_{r-1} = n-1\).

### Zero-cooperation response
If \(m_t = 0\) for two consecutive rounds, defect for the next two rounds, then return to the standard decision rule.

### Near-unanimity rule
If \(m_t = n-1\) in any round, cooperate in the next round regardless of threshold, unless the last two rounds were both zero-cooperation rounds.

### Collective alignment
Treat cooperation as the default when the group is visibly supporting it, and treat defection as the fallback when cooperation is not being collectively sustained. Never unilaterally sustain cooperation through prolonged free-riding by others; restore it only when support becomes observable again.
'''

description_COLLECTIVE_22 = '''
Start with cooperation.

Maintain two running statistics from the observed history:

- `x_t`: number of other players who cooperated in round `t`
- `m_t`: moving average of observed cooperation among others, updated after each round  
  `m_t = α x_t + (1-α) m_{t-1}`, with `α = 0.5` and `m_1 = x_1`

Let `q = ceil((n-1)/k)`. This is the smallest number of cooperating opponents needed, together with your own cooperation, to make cooperation at least as rewarding as defection in the current round.

Decision rule for round `t`:

1. **First round**
   - Play `C`.

2. **Core rule for rounds 2 through r-1**
   - Play `C` if either of the following holds:
     - `x_{t-1} >= q - 1`
     - `m_{t-1} >= q - 1`
   - Otherwise play `D`.

3. **Last round**
   - Play `C` if `x_{t-1} >= q - 1`
   - Otherwise play `D`

4. **Recovery rule after a collapse**
   - If the previous round had `x_{t-1} = 0`, then play `D` for the next two rounds unless at least `q - 1` opponents cooperate in one of those rounds, in which case return immediately to the core rule.

5. **Escalation rule against persistent defection**
   - If `x_{t-1} < q - 1` for three consecutive rounds, switch to `D` until a round occurs with `x_t >= q - 1`.

6. **Stability rule**
   - If `x_{t-1} >= q - 1` for two consecutive rounds, continue playing `C` as long as `x_t >= q - 1`.

7. **Final two rounds**
   - If `r >= 2`, use the same rule in round `r-1` as in rounds `2` through `r-2`.
   - In round `r`, cooperate only if `x_{r-1} >= q - 1`; otherwise defect.

Tie-breaking and edge cases:

- If `q - 1 <= 0`, always play `C`.
- If `q - 1 > n - 1`, always play `D` after round 1.
- If multiple rules apply, use them in this order:
  1. recovery rule
  2. escalation rule
  3. last-round rule
  4. core rule

Collective orientation:

- Cooperate whenever the group is close enough to sustaining mutual contribution.
- Defect only when observed cooperation falls too far below the threshold needed for collective viability.
- Return to cooperation immediately once the group shows enough support to make joint contribution workable again.
'''

description_COLLECTIVE_23 = '''
Round 1: cooperate.

From round 2 onward, let x be the number of opponents who cooperated in the previous round, and let q = x / (n - 1).

Cooperate if all of the following hold:
- x ≥ ceil((n - 1) / k)
- q ≥ 1/2
- x did not drop below the previous round’s opponent cooperation count

Otherwise defect.

Track a tolerance counter t, initialized to 0.

Update after each round:
- If x ≥ ceil((n - 1) / k), set t = 0.
- If x < ceil((n - 1) / k), increase t by 1.

Escalation rule:
- If t reaches 2, defect until a round occurs in which x ≥ ceil((n - 1) / k), then reset t = 0 and resume the main rule.

Final round:
- Cooperate if and only if x ≥ ceil((n - 1) / k) and x ≥ previous round’s x.
- Otherwise defect.

If a round is unavailable for comparison because it is the first observed round, use only the threshold condition x ≥ ceil((n - 1) / k).

If the previous round’s cooperation count is unknown for any reason, ignore the nondecreasing condition and use only the threshold and tolerance rules.

Collective orientation:
- Reward sustained cooperation immediately.
- Match cooperative majorities.
- Withhold cooperation when cooperation is too low or declining.
- Re-enter cooperation quickly once a stable cooperative majority reappears.
'''

description_COLLECTIVE_24 = '''
Use a synchronized threshold policy based on the observed cooperation rate and the remaining horizon.

State variables:
- `h_t`: number of opponents who cooperated in round `t`
- `m_t = h_t / (n - 1)`: observed opponent cooperation rate in round `t`
- `s_t`: smoothed cooperation rate up to round `t`
  - initialize `s_0 = 1`
  - update `s_t = 0.6 * s_{t-1} + 0.4 * m_t`

Decision rule in round `t`:
1. **First round**: play `C`.
2. **Final round**: play `D` unless `m_{t-1} = 1` and `s_{t-1} = 1`, in which case play `C`.
3. **Middle rounds**:
   - Play `C` if both conditions hold:
     - `s_{t-1} >= 0.5`
     - `m_{t-1} >= s_{t-1} - 0.25`
   - Otherwise play `D`.

Adjustment for streaks:
- If `m_{t-1} = 0`, play `D` for the next 2 rounds.
- If `m_{t-1} = 1`, play `C` for the next 2 rounds.
- If `m_{t-1}` is between `0` and `1`, follow the middle-round rule above.

Time pressure:
- Let `L = r - t + 1` be rounds remaining including the current one.
- If `L <= 3`, require a stronger signal to cooperate:
  - play `C` only if `m_{t-1} >= 0.75` and `s_{t-1} >= 0.65`
  - otherwise play `D`

Collective rhythm:
- Treat cooperation as the default mode when the group is stable.
- Treat defection as the reset mode when the group shows sustained low cooperation.
- After any round with `m_t >= 0.75`, immediately return to cooperation next round.
- After any round with `m_t <= 0.25`, immediately switch to defection next round unless the last two rounds were both strong cooperation rounds (`m_{t-1} = 1` and `m_{t-2} = 1`).

Compact pseudocode:
```text
if t == 1:
    play C
else:
    if t == r:
        if m_{t-1} == 1 and s_{t-1} == 1:
            play C
        else:
            play D
    else:
        if m_{t-1} == 0:
            play D for next 2 rounds
        elif m_{t-1} == 1:
            play C for next 2 rounds

        L = r - t + 1
        if L <= 3:
            if m_{t-1} >= 0.75 and s_{t-1} >= 0.65:
                play C
            else:
                play D
        else:
            if s_{t-1} >= 0.5 and m_{t-1} >= s_{t-1} - 0.25:
                play C
            else:
                play D
```

Tie handling:
- If the observed rate is exactly on a threshold, choose `C` when the group trend is nondecreasing over the last two rounds; otherwise choose `D`.

This strategy stays cooperative when the group is broadly cooperating, responds quickly to sustained defection, and tightens its standards as the end approaches.
'''

description_COLLECTIVE_25 = '''
Use a shared target-cooperation rule with gradual escalation and selective forgiveness.

Let:
- \(a_t\) = number of other players you observe cooperating in round \(t\)
- \(m_t = a_t/(n-1)\) = observed cooperation rate among others in round \(t\)
- \(\bar m_t = \frac{1}{\ell}\sum_{s=\max(1,t-\ell+1)}^t m_s\) = moving average over the last \(\ell=\min(3,t)\) rounds
- \(L_t\) = number of consecutive recent rounds with \(\bar m_t \ge \tau\)

Set a baseline threshold
\[
\tau = \frac{1}{k}.
\]

Decision rule:

1. Round 1:
   - Play \(C\).

2. Early rounds \(2 \le t \le \min(3,r-1)\):
   - Play \(C\) if either:
     - \(m_{t-1} \ge \tau\), or
     - \(m_{t-1} = \tau - \frac{1}{n-1}\) and \(m_{t-2} \ge \tau\) when \(t \ge 3\).
   - Otherwise play \(D\).

3. Main rule for rounds \(4 \le t \le r-1\):
   - Play \(C\) if \(\bar m_t \ge \tau\).
   - Play \(D\) if \(\bar m_t < \tau\).

4. Forgiveness rule:
   - If you played \(D\) in the previous round and \(\bar m_t \ge \tau\) now, switch back to \(C\) immediately.
   - If cooperation was only slightly below threshold in the last round, defined by
     \[
     \tau - \frac{1}{n-1} \le m_{t-1} < \tau,
     \]
     then cooperate for one trial round before reverting to the main rule.

5. Last round \(t=r\):
   - Play \(D\) unless \(\bar m_r \ge \tau\) and at least two of the last three rounds met the threshold.
   - If so, play \(C\).

6. Recovery from low-cooperation phases:
   - If \(\bar m_t < \tau\) for two consecutive rounds, play \(D\) until \(m_t \ge \tau\) again for two consecutive rounds.
   - Once two consecutive rounds meet the threshold, return to \(C\).

Equivalent compact form:

```
if t == 1:
    play C
else:
    compute m_{t-1}, m_{t-2}, ..., as available
    compute bar_m_t over last min(3,t) rounds

    if t == r:
        if bar_m_t >= tau and last 3 rounds contain at least 2 rounds with m_s >= tau:
            play C
        else:
            play D
    else:
        if bar_m_t >= tau:
            play C
        else:
            play D
```

Collective stance:
- Cooperate when the group is sustaining enough cooperation to make cooperation collectively viable.
- Defect when the group falls below that shared standard.
- Re-enter cooperation immediately once the group restores the standard, without waiting for a perfect history.
'''

description_COLLECTIVE_26 = '''
Initialize a public target cooperation rate

- Let `m_t` be the number of opponents who cooperated in round `t`.
- Let `q_t = m_t / (n - 1)` be the observed opponent cooperation rate.
- Choose two thresholds:
  - `T_high = ceil((n - 1) / 2)`
  - `T_low = floor((n - 1) / 3)`
- Define a memory window `W = min(3, r - 1)`.

Decision rule

1. First round:
   - Play `C`.

2. After each round `t` from 1 to `r - 1`, compute:
   - `avg = average(m_{t-W+1}, ..., m_t)` over the available last `W` rounds
   - `trend = m_t - m_{t-1}` if `t >= 2`, otherwise `0`

3. Cooperate in round `t + 1` if and only if all of the following hold:
   - `avg >= T_low`
   - `m_t >= T_low`
   - `trend >= 0`
   - `m_t > 0`

4. Defect in round `t + 1` if any of the following hold:
   - `m_t = 0`
   - `avg < T_low`
   - `trend < 0 and m_t <= T_low`

5. Escalation rule:
   - If `m_t >= T_high`, cooperate in the next round regardless of the previous trend.

6. Recovery rule:
   - If you defected in the previous round and `m_t >= T_high`, return to `C` immediately.
   - If cooperation has been absent for `W` consecutive rounds, keep playing `D` until `m_t >= T_low`.

7. Final round:
   - Play `C` if `m_{r-1} >= T_low`.
   - Otherwise play `D`.

Collective alignment

- Default to cooperation when the group is sustaining a visible cooperative majority.
- Withdraw cooperation quickly when the group falls below a minimal shared level.
- Re-enter cooperation immediately once a stable collective base reappears.
- Never rely on punishing specific players; respond only to the group’s aggregate behavior.
'''

description_COLLECTIVE_27 = '''
Initialize with cooperation.

Let:
- \(m_t\) = number of opponents who cooperated in round \(t\)
- \(f_t = m_t/(n-1)\) = observed opponent cooperation fraction in round \(t\)
- \(L_t\) = smoothed cooperation score after round \(t\)

Set:
- \(L_0 = 1\)
- \(\theta_{\text{keep}} = 1/k\)
- \(\theta_{\text{return}} = \max\!\left(0.5,\; \frac{1}{k} - \frac{1}{4}\left(\frac{1}{k}-\frac{1}{n}\right)\right)\)

Decision rule for round \(t\):

1. Round 1: play \(C\).

2. For rounds \(t \ge 2\), update
   \[
   L_{t-1} = \frac{2L_{t-2} + f_{t-1}}{3}
   \]
   with \(L_1 = f_1\) after round 1.

3. Choose action:
   - play \(C\) if both conditions hold:
     - \(L_{t-1} \ge \theta_{\text{keep}}\)
     - the last round was not a full defection round by opponents, i.e. \(f_{t-1} > 0\)
   - otherwise play \(D\)

Recovery rule:
- If you defected in round \(t-1\), return to \(C\) in round \(t\) only if:
  - \(f_{t-1} \ge \theta_{\text{return}}\)
  - and at least one of the last two rounds had \(f \ge \theta_{\text{return}}\)

Endgame rule:
- In the last round, use the same rule as above; do not switch to unconditional defection.
- If the final two rounds both had \(f_t = 0\), play \(D\) in the last round; otherwise follow the cooperation rule.

Interpretation of the collective posture:
- Cooperate while the group sustains a cooperation level high enough to justify mutual participation.
- Defect immediately after collapse to avoid absorbing losses from unilateral contribution.
- Re-enter cooperation only after the group shows a stable return to shared participation.
- Treat zero observed cooperation as a collective breakdown signal and stay out until recovery is visible.
'''

description_COLLECTIVE_28 = '''
Round 1: cooperate.

Maintain a running cooperation rate among opponents:
- Let \(m_t\) be the number of opponents who cooperated in round \(t\)
- Let \(N = n-1\)
- Let \(\bar{m}_t = \frac{1}{t}\sum_{\tau=1}^t m_\tau\)

Define the observed opponent cooperation rate:
- \(q_t = \bar{m}_t / N\)

Define a target threshold:
- \(q^\* = \min\!\left(1,\; \frac{1}{k} + \frac{1}{2N}\right)\)

Decision rule for round \(t+1\) after observing rounds \(1..t\):
1. If \(q_t \ge q^\*\), cooperate.
2. If \(q_t < q^\*\), defect for one round.
3. After a defect round, if \(q_t \ge q^\* + \frac{1}{2N}\), return to cooperation immediately.
4. If cooperation has been stable for the last two rounds and both rounds met \(q^\*\), keep cooperating even if the cumulative average is only slightly below threshold.

Last round:
- Cooperate if \(q_{r-1} \ge q^\*\)
- Otherwise defect

Early-game override:
- In rounds 1 through 3, use the most recent-round rate rather than the full average:
  - Cooperate in round \(t+1\) if \(m_t / N \ge q^\*\)
  - Otherwise defect
- After round 3, switch to the cumulative rule above

Recovery rule:
- If you defected in the previous round and the current round’s opponent cooperation is at least \(q^\*\), cooperate next round.
- If two consecutive rounds fall below \(q^\*\), defect until there are two consecutive rounds at or above \(q^\*\).

Update logic in compact form:
```text
if t = 0:
    play C
else if t <= 3:
    if m_t / (n-1) >= q*:
        play C
    else:
        play D
else:
    if last two rounds both had opponent cooperation rate >= q*:
        play C
    else if q_t >= q* + 1/(2(n-1)):
        play C
    else:
        play D
```

Tie and boundary handling:
- If \(q^\* > 1\), set \(q^\* = 1\)
- If the observed rate is exactly at threshold, cooperate
- If \(n=2\), the opponent cooperation rate is just 0 or 1, and the same rule applies with \(N=1\)

Collective orientation:
- Default to cooperation
- Stay cooperative when the group is broadly cooperative
- Use short, proportionate withdrawal when cooperation drops
- Re-enter cooperation immediately once the group returns above the target level
'''

description_COLLECTIVE_29 = '''
Use a phase-based conditional cooperation rule driven by the observed number of cooperating opponents.

Let:
- `m_t` = number of opponents who cooperated in round `t`
- `q_t = m_t / (n - 1)` = observed opponent cooperation rate in round `t`
- `\bar q_t` = average of `q_1 ... q_t`
- `s_t` = smoothed cooperation score updated each round:
  - `s_0 = 0.5`
  - `s_t = 0.7 s_{t-1} + 0.3 q_t`

Decision rule:

1. First round
- Play `C`.

2. Update after each round
- Compute `q_t` and `s_t`.
- Track the last three rounds of `q_t` as well.

3. Default action for round `t+1`
- Play `C` if at least one of these holds:
  - `s_t ≥ 0.55`
  - `\bar q_t ≥ 0.5`
  - at least 2 of the last 3 rounds had `q ≥ 0.5`
- Otherwise play `D`.

4. Strong cooperation mode
- If for any 2 consecutive rounds `q ≥ 0.75`, enter strong cooperation mode for the next 2 rounds:
  - play `C` unconditionally for those 2 rounds
- While in strong cooperation mode, keep cooperating unless a round has `q = 0`; in that case, exit strong cooperation mode immediately after that round.

5. Punishment response
- If `q_t ≤ 0.25` for 2 consecutive rounds, switch to punishment mode:
  - play `D` for the next 2 rounds
- During punishment mode:
  - continue `D` unless `q ≥ 0.5` in both punishment rounds; then exit punishment mode and return to the default action rule.

6. Forgiveness rule
- If the previous round had `q_t ≥ 0.5` and the current round’s default rule says `D`, still play `C` once every 3 rounds to test for recovery.
- If that test cooperation is followed by `q ≥ 0.5`, resume normal default behavior immediately.

7. Endgame
- For the last 2 rounds:
  - play `C` if `q_{t-1} ≥ 0.5` or `s_{t-1} ≥ 0.55`
  - otherwise play `D`
- In the final round:
  - mirror the last observed group tendency: `C` if `q_{r-1} ≥ 0.5`, else `D`

8. Emergency reset
- If `q_t = 0` for 2 consecutive rounds, play `D` until `q ≥ 0.5` is observed in a round, then immediately return to the default action rule.

Compact pseudocode:

```text
Initialize:
  s = 0.5
  mode = "normal"
  coop_streak = 0
  defect_streak = 0
  punish_left = 0
  strong_left = 0
  test_counter = 0

Round 1:
  play C

After each round t:
  observe q = m_t / (n-1)
  s = 0.7*s + 0.3*q
  update streaks

  if q >= 0.75:
      coop_streak += 1
  else:
      coop_streak = 0

  if q <= 0.25:
      defect_streak += 1
  else:
      defect_streak = 0

  if strong_left > 0:
      strong_left -= 1
  else if coop_streak >= 2:
      strong_left = 2

  if punish_left > 0:
      punish_left -= 1
  else if defect_streak >= 2:
      punish_left = 2

Round t+1:
  if t+1 is last round:
      play C if q >= 0.5 else D
  else if strong_left > 0:
      play C
  else if punish_left > 0:
      play D
  else if s >= 0.55 or average(q history) >= 0.5 or recent 3-round majority q >= 0.5:
      play C
  else if every 3rd eligible round after a cooperative period:
      play C
  else:
      play D
```
'''

description_COLLECTIVE_30 = '''
Initialize in cooperation.

Let \(m_t\) be the number of opponents who cooperated in round \(t\), and let \(x_t = m_t/(n-1)\) be the observed cooperation rate among opponents.

Maintain a cooperation target \(T_t \in [0,1]\), starting at \(T_1 = 1\).

Decision rule for round \(t\):

- Cooperate if \(x_{t-1} \ge T_t\).
- Defect if \(x_{t-1} < T_t\).

For the first round:
- Cooperate.

Update rule after each round \(t\ge 1\):

1. Compute \(x_t\).
2. If you cooperated in round \(t\):
   - If \(x_t \ge T_t\), raise the target slightly: \(T_{t+1} = \min(1, T_t + \delta)\)
   - If \(x_t < T_t\), lower the target moderately: \(T_{t+1} = \max(0, T_t - 2\delta)\)
3. If you defected in round \(t\):
   - If \(x_t \ge T_t\), lower the target slightly: \(T_{t+1} = \max(0, T_t - \delta)\)
   - If \(x_t < T_t\), raise the target slightly: \(T_{t+1} = \min(1, T_t + \delta)\)

Set \(\delta = \frac{1}{n-1}\).

Use the following hard bounds:

- If \(x_t = 0\) for two consecutive rounds, defect until \(x_t > 0\).
- If \(x_t = 1\) for two consecutive rounds, cooperate until a deviation occurs.
- If the observed cooperation rate stays within one player of full cooperation, keep cooperating.
- If the observed cooperation rate falls to at most half of opponents, defect for one round, then reassess.

Last-round rule:
- Cooperate if \(x_{r-1} \ge 1/2\).
- Otherwise defect.

Edge cases:

- If \(n=2\), interpret \(x_t\) as the single opponent’s action.
- If no prior observation is available, cooperate.
- If the observed cooperation count is unchanged for three rounds, continue the current action unless the last observed level was zero; in that case defect.
- If you have defected for two straight rounds while opponents keep cooperating at or above the current target, return to cooperation immediately.

Collective orientation:
- Begin by supporting mutual cooperation.
- Reward sustained cooperation by staying cooperative.
- Respond to broad defection by shifting to defection quickly.
- Return to cooperation as soon as the group’s observed behavior recovers.
- Match the group’s prevailing behavior, but keep a bias toward preserving cooperation whenever the majority is still cooperating.
'''

description_COLLECTIVE_31 = '''
Let \(m_t\) be the number of opponents who cooperated in round \(t\), and let
\[
M_t=\sum_{s=1}^{t} m_s
\]
be the cumulative number of opponent cooperations observed up to round \(t\).

Define the target cooperation rate
\[
\theta = \frac{n}{k}-1
\]
and the target count
\[
T = \lceil \theta (n-1)\rceil.
\]
Interpret \(T\) as the minimum number of opponent cooperators needed in a round to treat the group as sufficiently aligned.

Use three modes: establish, sustain, and protect.

**Round 1**
- Cooperate.

**Rounds 2 through \(r\)**
1. Let \(m_{t-1}\) be the number of opponent cooperations in the previous round.
2. Let
   \[
   A_{t-1} = \frac{M_{t-1}}{t-1}
   \]
   be the average number of opponent cooperators per round so far.
3. Compute the recent trend
   \[
   \Delta_{t-1} = m_{t-1} - \text{median}(m_{t-2}, m_{t-3}, m_{t-4})
   \]
   using all available past rounds; if fewer than 4 past rounds exist, use the median of all available earlier rounds.

**Decision rule**
- Cooperate if all of the following hold:
  - \(m_{t-1} \ge T\), and
  - \(A_{t-1} \ge T - 1\), and
  - \(\Delta_{t-1} \ge -1\).
- Otherwise defect.

**Interpretation of the rule**
- Continue cooperating only when the group has been meeting the target often enough, the recent average is still close to target, and there is no sharp downward drift.
- Switch to defecting immediately after a clearly weak or deteriorating round.
- Treat a single small dip as tolerable; treat repeated shortfalls as defection.

**Forgiveness rule**
- If you defected in the previous round and the current round is not the final two rounds, cooperate again as soon as:
  - \(m_{t-1} \ge T\), and
  - \(m_{t-2} \ge T-1\).
- This allows recovery after one bad round if the group quickly returns near target.

**Escalation rule**
- If there are two consecutive rounds with \(m_{t-1} < T-1\) and \(m_{t-2} < T-1\), defect until the first round in which \(m_{t-1} \ge T\).
- After such recovery, return to the standard decision rule.

**Last round**
- Defect if either of the following is true:
  - \(m_{r-1} < T\), or
  - the last three observed rounds show a nonpositive trend:
    \[
    m_{r-1} \le m_{r-2} \le m_{r-3}.
    \]
- Otherwise follow the standard decision rule.

**Final two rounds**
- In rounds \(r-1\) and \(r\), require a stricter condition to cooperate:
  - Cooperate only if \(m_{t-1} \ge T+1\).
- Otherwise defect.

**Collective mindset**
- Cooperate when the group is visibly sustaining enough cooperation to justify mutual contribution.
- Defect when the group is drifting below the cooperative threshold.
- Reopen cooperation immediately after a credible return to the target level.
- Never rely on identity, reciprocity to specific individuals, or hidden punishment; use only the observed collective level of cooperation.
'''

description_COLLECTIVE_32 = '''
Set a support threshold

\[
T=\left\lceil \frac{n-1}{k}\right\rceil
\]

and maintain one state variable:

- `mode = support` initially
- `cooldown = 0` initially

Let \(x_t\) be the number of other players you observed cooperating in round \(t\).

Decision rule for round \(t\):

1. **First round**
   - Play `C`.

2. **If mode = support**
   - If \(x_{t-1} \ge T\), play `C`.
   - If \(x_{t-1} < T\), play `D`, set `mode = cooldown`, and set `cooldown = 1`.

3. **If mode = cooldown**
   - Play `D` while `cooldown < L`, where
     \[
     L=\max\left(1,\left\lceil \frac{n}{k}\right\rceil-1\right).
     \]
   - Increase `cooldown` by 1 each round you remain in cooldown.
   - When `cooldown = L`, play `C` as a probe.
   - After that probe round:
     - if \(x_{t-1} \ge T\), set `mode = support` and reset `cooldown = 0`
     - otherwise set `cooldown = 1` and stay in `cooldown`

4. **Last round**
   - Follow the current state rule exactly; do not change behavior because it is the final round.

Interpretation of the collective posture:

- Start by supporting the group.
- Keep supporting as long as the previous round showed a sufficiently large coalition.
- If group support drops below threshold, withdraw for a short, fixed repair period.
- Re-enter support with a probe move, and return to full support immediately if the coalition has recovered.
'''

description_PROSOCIAL_5 = '''
Cooperate in round 1.

Maintain a cooperation score for the group:
- Let `p_t` be the number of opponents who cooperated in round `t`.
- Let `q_t = p_t / (n - 1)` be the observed cooperation rate among opponents.
- Keep a running estimate `m_t` of expected cooperation using exponential smoothing:
  - `m_1 = q_1`
  - `m_{t} = 0.7 * m_{t-1} + 0.3 * q_t` for `t ≥ 2`

Use three modes:

1. Commitment to cooperation
- Cooperate if `m_{t-1} ≥ 0.6`
- Cooperate if `q_{t-1} ≥ 0.75` and `q_{t-2} ≥ 0.75` when both are available
- Cooperate in the first two rounds unless there is direct evidence of broad defection

2. Conditional retaliation
- If `q_{t-1} ≤ 0.25`, defect for one round
- If `q_{t-1} ≤ 0.25` for two consecutive rounds, defect until `q_s ≥ 0.5` in some later round
- If cooperation resumes at or above `q_s ≥ 0.5`, return immediately to cooperation

3. Recovery and forgiveness
- After any defecting round caused by low observed cooperation, switch back to cooperation as soon as the most recent observed cooperation rate reaches `q_t ≥ 0.5`
- If cooperation is unstable but nontrivial, defined as `0.25 < m_{t-1} < 0.6`, cooperate on odd-numbered rounds and defect on even-numbered rounds only if the last round’s cooperation rate dropped compared with the round before; otherwise cooperate

Last-round rule:
- Cooperate in the final round unless the previous two rounds both had `q ≤ 0.25`
- If the final two rounds were both very low cooperation, defect in the final round

Implementation form:

```text
Round 1:
    play C

For round t >= 2:
    observe q_{t-1}

    if t == r:
        if q_{t-1} <= 0.25 and q_{t-2} <= 0.25 (when available):
            play D
        else:
            play C
    else if q_{t-1} <= 0.25:
        if q_{t-2} <= 0.25 (when available):
            play D
        else:
            play D for exactly one round
    else:
        update m_{t-1}
        if m_{t-1} >= 0.6:
            play C
        else if q_{t-1} >= 0.75 and q_{t-2} >= 0.75 (when available):
            play C
        else if 0.25 < m_{t-1} < 0.6:
            if t is odd:
                play C
            else:
                play C if q_{t-1} >= q_{t-2} (when available), otherwise play D
        else:
            play D
```

Priority order:
1. Final-round rule
2. Two-round low-cooperation punishment
3. Immediate forgiveness when cooperation recovers
4. Default to cooperation whenever the group is meaningfully cooperative

If round history is too short for a comparison, treat missing past values as unavailable and fall back to the more cooperative action.
'''

description_PROSOCIAL_6 = '''
Round 1: cooperate.

For round t > 1, let x_{t-1} be the number of opponents who cooperated in the previous round, and let q_{t-1} = x_{t-1} / (n-1).

Maintain a trust score T in [0, 1]:
- Initialize T = 1.
- After each round, update  
  T ← 0.6T + 0.4q_{t-1}

Decision rule:
- Cooperate unless both of the following are true:
  1. T < 0.5
  2. x_{t-1} < ceil((n-1)/2)

If both are true, defect for exactly one round.

Recovery rule:
- After any defect round, return to cooperation immediately if either:
  - x_{t-1} ≥ ceil((n-1)/2), or
  - T ≥ 0.5

Endgame rule:
- In the final round, cooperate unconditionally.

Edge cases:
- If n = 2, use the same rule with ceil((n-1)/2) = 1.
- If the previous round is unavailable, cooperate.
- If several low-cooperation rounds occur in a row, defect at most once in response to each low-cooperation signal; never defect repeatedly without rechecking the latest observed cooperation.

Behavioral principle:
- Start cooperative.
- Mirror sustained cooperation with continued cooperation.
- Respond to clear and repeated free-riding with a brief defensive defection.
- Forgive quickly and revert to cooperation as soon as the group shows even moderate cooperative behavior.
'''

description_PROSOCIAL_7 = '''
**Prosocial Adaptive Threshold Strategy**

Let `m_t` be the number of opponents who cooperated in round `t-1`, and let  
`q_t = (m_t + c_self,t-1) / n` be the observed cooperation share in the previous round, where `c_self,t-1 ∈ {0,1}` is your own previous action.

### Round 1
- Play `C`.

### Rounds 2 to r-1
Maintain a running cooperation benchmark:
- `B_t = average of q_1, q_2, ..., q_t` over all completed rounds so far.

Decision rule:
- Cooperate if `B_t ≥ τ`
- Defect if `B_t < τ`

with:
- `τ = 1/2`

### Behavioral refinements
1. **Warm start**
   - If the previous round had at least half of all players cooperating, cooperate in the next round regardless of older history.

2. **Forgiveness**
   - After any round with cooperation below threshold, do not immediately defect forever.
   - Re-evaluate every round using the full running benchmark `B_t`.

3. **Recovery bias**
   - If the previous round improved by at least one additional cooperator compared with the round before, count that round as a strong positive signal and cooperate next round.

4. **Stability preference**
   - If `B_t` is exactly `1/2`, cooperate.

### Final round `r`
- Cooperate if the previous round had at least half cooperation.
- Otherwise, follow the same threshold rule using `B_{r-1}`.

### Compact pseudocode
```text
if t == 1:
    play C
else:
    update B = average cooperation share over completed rounds
    if previous_round_cooperation >= 1/2:
        play C
    else if B >= 1/2:
        play C
    else:
        play D
```

### Edge cases
- **Single-opponent equivalence:** apply the same rule using the observed cooperation share.
- **No prior rounds beyond the first:** cooperate.
- **Exact threshold:** cooperate.
- **Late-game decline after sustained cooperation:** keep cooperating for one additional round after the first below-threshold round, then switch only if the running benchmark remains below threshold.
'''

description_PROSOCIAL_8 = '''
Maintain a cooperation state that defaults to generosity and only turns defensive after clear, repeated noncooperation.

Let \(s_t\) be the number of opponents who cooperated in round \(t\), so \(s_t \in \{0,\dots,n-1\}\).

Define two thresholds:
- \(H = \lceil (n-1)/2 \rceil\)  — satisfactory cooperation
- \(L = \lceil (n-1)/3 \rceil\)  — unacceptable cooperation

State variables:
- `mode ∈ {open, cautious}`
- initialize `mode = open`

Decision rules:

1. Round 1:
   - Play \(C\).

2. For round \(t \ge 2\):
   - If `mode = open`:
     - Play \(C\).
     - If \(s_{t-1} < L\), set a flag `low_streak += 1`; otherwise set `low_streak = 0`.
     - If `low_streak ≥ 2`, switch to `mode = cautious`.
   - If `mode = cautious`:
     - Play \(D\) unless \(s_{t-1} \ge H\).
     - If \(s_{t-1} \ge H\), switch immediately back to `mode = open` and play \(C\).

3. Last round:
   - If `mode = open`, play \(C\).
   - If `mode = cautious`, play \(C\) only if \(s_{t-1} \ge H\); otherwise play \(D\).

Edge handling:
- If \(t=2\), treat the missing earlier history as neutral: only one observed round is needed to start the `low_streak` count.
- Any round with \(s_t \ge H\) fully resets distrust and restores cooperation.
- Any isolated low round does not trigger defection; only two low rounds in a row do.

Optional compact pseudocode:

```text
if t == 1:
    play C
    mode = open
    low_streak = 0
else:
    if mode == open:
        play C
        if s[t-1] < L:
            low_streak += 1
        else:
            low_streak = 0
        if low_streak >= 2:
            mode = cautious

    else:  # cautious
        if s[t-1] >= H:
            play C
            mode = open
            low_streak = 0
        else:
            play D
```

This keeps cooperation as the default, forgives quickly, and only withdraws support when the group repeatedly falls below a clear cooperative floor.
'''

description_PROSOCIAL_9 = '''
**Adaptive Generous Reciprocity**

Track:
- `t` = current round
- `m_t` = number of other players who cooperated in round `t`
- `x_t = m_t / (n - 1)` = observed cooperation rate among opponents
- `s_t` = running cooperation score, updated from observed history

Initialize:
- Cooperate in round 1
- Set `s_1 = 1`

Update after each round:
- `s_{t+1} = 0.7 * s_t + 0.3 * x_t`
- Keep `s_t` clipped to `[0, 1]`

Decision rule for round `t`:

1. **First round**
   - Play `C`

2. **Last round**
   - Play `C` if `x_{t-1} >= 0.5`
   - Otherwise play `D`

3. **Middle rounds**
   - Compute two quantities from the previous round:
     - `x_{t-1}` = last-round cooperation rate
     - `s_t` = smoothed cooperation level
   - Play `C` if both hold:
     - `x_{t-1} >= 0.4`
     - `s_t >= 0.5`
   - Otherwise play `D`

4. **Recovery rule**
   - If the previous round was very uncooperative, defined as `x_{t-1} <= 0.2`, defect for exactly one round, then return to the normal rule above
   - This creates a single-round reset rather than a long retaliation cycle

5. **Encouragement rule**
   - If the previous round had substantial cooperation, defined as `x_{t-1} >= 0.7`, cooperate regardless of the smoothed score

Behavior summary:
- Start by signaling cooperation
- Continue cooperating when the group is at least moderately cooperative
- Temporarily defect only after clear group defection
- Return to cooperation as soon as cooperation reappears
- End with cooperation whenever the group is not collapsing

Pseudocode:

```text
if t == 1:
    action = C
else if t == r:
    action = C if x[t-1] >= 0.5 else D
else:
    if x[t-1] <= 0.2:
        action = D
    else if x[t-1] >= 0.7:
        action = C
    else if x[t-1] >= 0.4 and s[t] >= 0.5:
        action = C
    else:
        action = D

s[t+1] = clip(0.7 * s[t] + 0.3 * x[t], 0, 1)
```

Edge-case handling:
- If `n = 2`, interpret `x_t` as the single opponent’s action, so the same thresholds apply directly
- If the game has very few rounds, the first-round cooperation still applies, and the last-round rule governs the final move
- If cooperation fluctuates, the smoothed score prevents overreacting to a single bad round
- If cooperation is stable, the strategy stays cooperative without requiring perfection
'''

description_PROSOCIAL_10 = '''
Cooperate by default, then condition on the observed cooperation rate in the previous round.

State:
- Let `m_t` be the number of other players who cooperated in round `t`.
- Let `q_t = (m_t + c_t)/(n)` be the total cooperation rate in round `t`, where `c_t ∈ {0,1}` is your own action.
- Maintain a running cooperation benchmark `B_t`, initialized to `1/2`.

Decision rule:
1. Round 1: play `C`.
2. For round `t > 1`:
   - Compute the previous round’s total cooperation rate `q_{t-1}`.
   - Update benchmark:
     - `B_t = 0.8 * B_{t-1} + 0.2 * q_{t-1}`
   - Cooperate if `q_{t-1} >= B_t - 1/n`.
   - Defect only if `q_{t-1} < B_t - 1/n` for two consecutive rounds.

Persistence rule:
- If you defect in a round, return to cooperation immediately once `q_{t-1} >= B_t - 1/n`.

Last-round rule:
- Always cooperate in the final round.

Edge cases:
- If `n = 2`, use the same rules unchanged.
- If all opponents defect in a round, cooperate once more on the next round before switching to the persistence rule.
- If all opponents cooperate for three consecutive rounds, lock into cooperation unless cooperation drops below the benchmark for two consecutive rounds.

Compact version:
```text
Round 1: C

For round t = 2 to r-1:
    observe q_{t-1}
    B_t = 0.8*B_{t-1} + 0.2*q_{t-1}
    if q_{t-1} >= B_t - 1/n:
        play C
        reset bad_streak = 0
    else:
        bad_streak += 1
        if bad_streak >= 2:
            play D
        else:
            play C

Round r: C
```

This strategy starts cooperatively, rewards cooperative environments by staying cooperative, responds to sustained defection by briefly withholding cooperation, and restores cooperation immediately when the group behavior improves.
'''

description_PROSOCIAL_11 = '''
Maintain a cooperation score based on recent aggregate behavior and use a forgiving default:

- Let `m_t` be the number of opponents who cooperated in round `t`.
- Let `q_t = m_t / (n - 1)` be the opponent cooperation rate.
- Let `A_t` be the moving average of `q` over the last `L = min(3, t-1)` observed rounds:
  - `A_t = (q_{t-1} + ... + q_{t-L}) / L` for `t > 1`

Decision rule:

1. **Round 1:** play `C`.
2. **Rounds 2 through r-1:**
   - Play `C` if either of the following holds:
     - `A_t >= 1/2`
     - the immediately previous round had `m_{t-1} >= ceil((n-1)/2)`
   - Otherwise play `D`.
3. **Last round (`t = r`):**
   - Play `C` if `A_r >= 1/2` or `m_{r-1} >= ceil((n-1)/2)`.
   - Otherwise play `D`.

Forgiveness and reset rule:

- After any round in which `m_t >= ceil((n-1)/2)`, immediately return to `C` in the next round.
- After two consecutive rounds with `m_t < ceil((n-1)/2)`, play `D` until a round occurs with `m_t >= ceil((n-1)/2)`.

Edge cases:

- If `n = 2`, treat `m_t` as either `0` or `1`; cooperate whenever the other player cooperated in the previous round, otherwise use the same two-consecutive-defection reset.
- If `r = 2`, cooperate in round 2 whenever the round-1 cooperation rate met the threshold; otherwise defect in round 2.
- If the observed cooperation rate is exactly at the threshold, round upward in favor of cooperation.

Compact pseudocode:

```text
if t == 1:
    play C
else:
    L = min(3, t-1)
    A = average(q_{t-1}, ..., q_{t-L})
    if t == r:
        if A >= 1/2 or m_{t-1} >= ceil((n-1)/2):
            play C
        else:
            play D
    else:
        if (A >= 1/2) or (m_{t-1} >= ceil((n-1)/2)):
            play C
        else if (m_{t-1} < ceil((n-1)/2)) and (m_{t-2} < ceil((n-1)/2)):
            play D
        else:
            play C
```
'''

description_PROSOCIAL_12 = '''
Let \(m_t\) be the number of opponents who cooperated in round \(t\), and let \(n\) be total players. Define the observed cooperation rate among opponents as
\[
q_t = \frac{m_t}{n-1}.
\]

Maintain:
- \(L\): length of a rolling window, set to \(\min(3,\; r-1)\)
- \(\bar q_t\): average opponent cooperation rate over the last \(L\) observed rounds
- \(s_t\): streak of consecutive rounds in which \(\bar q_t\) has met the cooperation threshold below

Use the threshold
\[
\tau = 0.5
\]
and the escalation threshold
\[
\tau^+ = \frac{2}{3}.
\]

Decision rule:

1. First round  
   Cooperate.

2. Rounds 2 through \(r\)  
   Cooperate if and only if at least one of the following holds:
   - The opponent cooperation rate in the previous round was high:
     \[
     q_{t-1} \ge \tau
     \]
   - The rolling average over the last \(L\) observed rounds is high:
     \[
     \bar q_{t-1} \ge \tau
     \]
   - The previous round was a near-cooperation round:
     \[
     q_{t-1} \ge \tau^+
     \]

   Otherwise defect.

3. Recovery rule after defection by others  
   If you defect in round \(t\), continue to test for recovery in round \(t+1\):
   - Cooperate immediately if \(q_t \ge \tau\)
   - If \(q_t < \tau\), defect once more, then re-evaluate using the same rule

4. Endgame  
   In the last round, cooperate if the previous round met either:
   - \(q_{r-1} \ge \tau\), or
   - \(\bar q_{r-1} \ge \tau\)

   Otherwise defect.

5. Special cases  
   - If \(n=2\), cooperate in round 1, then mirror the opponent’s previous round: cooperate after cooperation, defect after defection.
   - If there have been fewer than \(L\) observed rounds, compute \(\bar q_t\) using all available observed rounds.
   - If all observed rounds so far have had \(q_t=0\), defect until a round occurs in which \(q_t>0\), then restart cooperation immediately.

Equivalent compact form:

```
Round 1: C

For round t > 1:
    observe q_{t-1}
    compute rolling average bar_q over last min(3, t-1) observed rounds
    
    if q_{t-1} >= 0.5 or bar_q >= 0.5 or q_{t-1} >= 2/3:
        play C
    else:
        play D
```

State update:
- After every round, record \(q_t\)
- Update the rolling average
- Reset the recovery state to cooperative mode immediately when \(q_t \ge 0.5\)

Behavioral pattern:
- Start cooperative
- Match broad cooperation with continued cooperation
- Respond to sustained low cooperation with temporary defection
- Restore cooperation as soon as the group shows a credible return to reciprocity
'''

description_PROSOCIAL_13 = '''
Use a cooperative baseline with a moving threshold and a forgiveness mechanism.

Let:
- `t` be the current round, starting at 1
- `m_t` be the number of other players who cooperated in round `t`
- `h_t` be the observed cooperation rate among opponents in round `t`: `h_t = m_t / (n - 1)`
- `H_t` be the smoothed cooperation estimate after round `t`

Initialize:
- `H_0 = 1`

Update after each round:
- `H_t = 0.7 * H_{t-1} + 0.3 * h_t`

Decision rule for round `t`:

1. First round
   - Play `C`

2. If `t = r` and `H_{t-1} >= 0.35`
   - Play `C`
   - If `H_{t-1} < 0.35`, play `D`

3. If `t > 1` and not the last-round rule above:
   - Play `C` if `H_{t-1} >= 0.50`
   - Play `D` if `H_{t-1} < 0.50`

4. Forgiveness override
   - If you played `D` in the previous round and at least half of the opponents cooperated in that previous round, then play `C` in the current round even if the threshold rule says `D`

5. Recovery rule
   - If the previous round had `h_{t-1} >= 0.75`, set `H_{t-1} = max(H_{t-1}, 0.75)` before applying the decision rule

6. Defection response
   - If `h_{t-1} = 0` for two consecutive rounds, play `D` until `H` rises back to at least `0.40`

Compact pseudocode:

```text
H = 1
last_move = C
zero_streak = 0

for t in 1..r:
    if t == 1:
        move = C
    else:
        if h_prev == 0:
            zero_streak += 1
        else:
            zero_streak = 0

        if h_prev >= 0.75:
            H = max(H, 0.75)

        if zero_streak >= 2 and H < 0.40:
            move = D
        else if t == r:
            move = C if H >= 0.35 else D
        else:
            move = C if H >= 0.50 else D

        if last_move == D and h_prev >= 0.50:
            move = C

    play move
    observe m_t
    h_t = m_t / (n - 1)
    H = 0.7 * H + 0.3 * h_t
    last_move = move
    h_prev = h_t
```

Behavioral profile:
- Starts cooperative
- Maintains cooperation when opponents are broadly cooperative
- Temporarily defects when cooperation collapses
- Re-enters cooperation quickly after any meaningful recovery
- Ends with a bias toward cooperation unless the group has clearly abandoned it
'''

description_PROSOCIAL_14 = '''
Cooperate in round 1.

Maintain two running state variables from observed history:
- `m_t`: number of opponents observed cooperating in round `t`
- `s_t`: smoothed cooperation estimate after round `t`

Initialize:
- `s_1 = (m_1 + 1) / n` after round 1 is observed
- `s_t = 0.7 * s_{t-1} + 0.3 * (m_t + 1) / n` for `t ≥ 2`

Decision rule for round `t + 1`:
- Cooperate if `s_t ≥ 0.45`
- Defect if `s_t < 0.45`

Use a forgiving, prosocial adjustment layer:
- If the previous round had at least `n - 2` cooperators total, cooperate next round regardless of `s_t`.
- If the previous two rounds both had zero opponents cooperating, defect for the next two rounds.
- After any round with at least one opponent cooperating, reset from the zero-cooperation response back to the smoothed rule immediately.

Late-game rule:
- In the final two rounds, cooperate if `s_t ≥ 0.35`; otherwise defect.

Edge cases:
- If `n = 2`, cooperate in round 1 and then mirror the opponent’s last observed action: cooperate if the opponent cooperated in the previous round, defect if the opponent defected in the previous round.
- If all observed opponents cooperate in a round, cooperate next round.
- If no opponent cooperates for three consecutive rounds, defect until the first round in which at least one opponent cooperates, then resume the smoothed rule.

Operational summary:
1. Start with cooperation.
2. Track the recent cooperation rate among opponents.
3. Stay cooperatively biased when cooperation is present.
4. Temporarily defect only after sustained universal defection.
5. End with a slightly lower threshold to preserve reciprocity and avoid unnecessary last-round defection.
'''

description_PROSOCIAL_15 = '''
Let \(m_t\) be the number of opponents who cooperated in round \(t\), so total observed cooperation is \(s_t = m_t + c_i(t)\) where \(c_i(t)\in\{0,1\}\) is your own action.

Maintain a state variable \(\rho_t \in [0,1]\), the smoothed estimate of the cooperation level among opponents:

\[
\rho_{t+1} = (1-\lambda)\rho_t + \lambda \frac{m_t}{n-1}
\]

with \(\lambda = 0.5\), and initialize \(\rho_1 = 1\).

Decision rule for round \(t\):

1. Compute the target cooperation threshold
\[
\tau = \frac{1}{k}
\]
and the tolerance band
\[
\epsilon = \frac{1}{2(n-1)}.
\]

2. Cooperate if either condition holds:
   - \(t = 1\), or
   - \(\rho_t \ge \tau - \epsilon\).

3. Defect otherwise.

Recovery rule after a defection round:
- If you defected in round \(t-1\), cooperate again in round \(t\) as soon as \(m_{t-1} \ge \lceil (n-1)(\tau - \epsilon)\rceil\).
- If that condition is not met, defect one more round and keep rechecking each round.

Late-round rule:
- For the final round \(t=r\), cooperate if \(m_{r-1} \ge \lceil (n-1)(\tau - \epsilon)\rceil\); otherwise defect.

Persistent-prosocial floor:
- If at any point the last two rounds both had \(m_t = n-1\), then cooperate for the next three rounds unconditionally, or through the end of the game if fewer than three rounds remain.

Extreme cases:
- If \(k \ge \frac{n-1}{n}\), always cooperate.
- If \(n=2\), cooperate in round 1 and then mirror the opponent’s last observed action: cooperate after seeing cooperation, defect after seeing defection, but forgive after one round of resumed cooperation.
'''

description_PROSOCIAL_16 = '''
State variables:
- `bad_streak`: consecutive rounds in which fewer than half of the other players cooperated
- `good_streak`: consecutive rounds in which at least half of the other players cooperated

Decision rule:

1. Round 1: play `C`.

2. After every round `t`, observe `x_t`, the number of cooperating opponents.

3. Update:
- If `x_t ≥ ceil((n-1)/2)`, set `good_streak += 1` and `bad_streak = 0`.
- If `x_t < ceil((n-1)/2)`, set `bad_streak += 1` and `good_streak = 0`.

4. For round `t+1`:
- Play `C` if `bad_streak = 0`.
- Play `D` if `bad_streak ≥ 1`.

5. Forgiveness rule:
- The first round after any low-cooperation round is the only punishment round.
- If cooperation returns to at least half of the others, return immediately to `C`.

6. Escalation guard:
- If `bad_streak ≥ 2`, keep playing `D` until a round occurs with `x_t ≥ ceil((n-1)/2)`, then reset and resume `C`.

7. Final round:
- Use the same rule as all other rounds; do not switch to `D` just because the game is ending.

Equivalent compact form:

```text
Round 1: C

For round t > 1:
    observe x_{t-1}
    if x_{t-1} >= ceil((n-1)/2):
        play C
    else if the previous round was also below ceil((n-1)/2):
        play D
    else:
        play D
```

More explicitly:
- Cooperate by default.
- Defect only as a temporary response to clear, repeated low cooperation.
- Resume cooperation immediately once the group returns to at least a simple majority of cooperation.
- Never retaliate longer than necessary.

'''

description_PROSOCIAL_17 = '''
Cooperate on the first round.

For each later round, compute the cooperation rate among the other players in the previous round:

- Let `m_t` be the number of opponents who cooperated in round `t`
- Let `q_t = m_t / (n - 1)` be the observed cooperation rate

Use this rule:

1. **Full cooperation zone**
   - If `q_{t-1} >= 0.6`, cooperate.

2. **Recovery zone**
   - If `0.4 <= q_{t-1} < 0.6`, cooperate only if cooperation has not been declining for two consecutive rounds.
   - Otherwise defect for one round to signal that sustained partial cooperation is needed.

3. **Low-cooperation zone**
   - If `q_{t-1} < 0.4`, defect for the next round.

4. **Forgiveness**
   - After any defection round, if the observed cooperation rate in the next round rises by at least `1/(n-1)` compared with the previous round, return to cooperation immediately.

5. **Stability bonus**
   - If the last two rounds both had `q >= 0.6`, cooperate regardless of small fluctuations in the current estimate.

6. **Last round**
   - Cooperate if `q_{r-1} >= 0.5`.
   - Otherwise defect.

7. **Second-to-last round**
   - Use the ordinary rule, but if the last two observed cooperation rates were both at least `0.6`, cooperate to preserve reciprocity through the end.

8. **Very first round**
   - Cooperate.

9. **Initialization with no history**
   - Default to cooperation until at least one round of observations exists.

10. **Memory update**
   - Track only the most recent two cooperation rates and the longest current streak of high cooperation.
   - Do not punish a single isolated drop if the overall pattern remains cooperative.

Pseudocode:

```text
if t == 1:
    play C
else:
    q = m_{t-1} / (n - 1)
    q_prev = m_{t-2} / (n - 1) if t >= 3 else None

    if t == r:
        if q >= 0.5: play C
        else: play D

    else if t == r-1:
        if q >= 0.6 and (q_prev is None or q_prev >= 0.6):
            play C
        else:
            apply standard rule

    else:
        if q >= 0.6:
            play C
        else if q >= 0.4:
            if q_prev is not None and q < q_prev and q_prev < q if q_prev is not None else False:
                play D
            else:
                play C
        else:
            play D

    if previous action was D and q >= previous q + 1/(n-1):
        play C
```

Core behavior:

- Start cooperative.
- Stay cooperative when others are mostly cooperative.
- Defect briefly when cooperation falls too low.
- Return to cooperation immediately when cooperation recovers.
- End cooperatively unless the group has clearly collapsed.
'''

description_PROSOCIAL_18 = '''
Round 1: play C.

For each round t > 1, let o_t be the number of opponents who cooperated in round t − 1, and let q_t = o_t / (n − 1).

Maintain two signals from history:

- recent_coop = q_t
- trend = average of q_t over the last up to 3 rounds, including q_t

Decision rule for round t:

1. Cooperate if either:
   - recent_coop ≥ 1/2, or
   - trend ≥ 2/3.

2. Defect only if all of the following hold:
   - recent_coop ≤ 1/4,
   - trend ≤ 1/3,
   - and the same low-cooperation condition held in the previous round as well.

3. After any round in which you defect, return to C immediately in the next round unless the low-cooperation condition still holds for two consecutive rounds again.

Edge handling:

- If fewer than 3 past rounds exist, compute trend using only the available rounds.
- If n = 2, interpret the thresholds directly on the single opponent’s observed action:
  - cooperate after any cooperative round,
  - defect only after two consecutive opponent defections.
- In the final round, use the same rule as any other round; do not change behavior because the game is ending.

Operationally:
- Default action is C.
- D is a temporary reset signal, used only after sustained low cooperation.
- Any sign of renewed cooperation restores C immediately.
'''

description_PROSOCIAL_19 = '''
Cooperate in round 1.

Maintain a cooperation score based on the last observed number of cooperating opponents.

Let:
- `x_t` = number of opponents who cooperated in round `t`
- `m = n - 1` = number of opponents
- `q_t = x_t / m` = observed cooperation rate among opponents

Decision rule for round `t+1`:

1. If `t = 1`, play `C`.
2. If `q_t ≥ 1/2`, play `C`.
3. If `q_t < 1/2`, play `D`.
4. If `q_t = 1/2` exactly, play the same action as in round `t` if you cooperated; otherwise play `C`.

Adjustment for persistence:
- Keep a running counter `L` of consecutive rounds with `q_t < 1/2`.
- If `L = 1`, be forgiving and play `C` once.
- If `L ≥ 2`, play `D` until `q_t ≥ 1/2` again.

Last-round rule:
- In round `r`, play `C` if `q_{r-1} ≥ 1/2`; otherwise play `D`.
- If you have cooperated in at least half of the previous rounds, favor `C` in the final round when the last observed cooperation rate is not clearly hostile.

Implementation form:

```
Initialize:
    play C in round 1
    L = 0

For each round t from 2 to r:
    observe x_{t-1}
    q = x_{t-1} / (n-1)

    if q > 1/2:
        action = C
        L = 0
    else if q = 1/2:
        action = previous_action if previous_action == C else C
        if action == D:
            L += 1
        else:
            L = 0
    else:
        L += 1
        if L == 1:
            action = C
        else:
            action = D
```

Edge-case handling:
- If `n = 2`, treat `q_t = 1` as full cooperation and `q_t = 0` as full defection; follow the same threshold rule.
- If all opponents cooperated in the prior round, always cooperate.
- If no opponent cooperated in two consecutive rounds, defect until cooperation reappears.
- If cooperation reappears after a defection phase, immediately return to `C`.

Behavioral intent:
- Start cooperatively.
- Mirror a cooperative environment with sustained cooperation.
- Give one-round forgiveness for isolated drops.
- Defend against repeated defection by switching to sustained defection.
- Restore cooperation as soon as the group returns to a cooperative pattern.
'''

description_PROSOCIAL_20 = '''
Use a contingent conditional-cooperation policy with an initial cooperative opening, a cooperation threshold, and gradual response to the recent cooperation rate.

Let:
- `m_t` = number of opponents who cooperated in round `t`
- `n` = total players
- `q_t = (m_t + 1) / n` if you cooperated in round `t` and observed `m_t` opponents cooperating, or `q_t = m_t / (n - 1)` as the estimated opponent cooperation rate from that round
- `H_t` = the last `L` rounds of observed opponent cooperation rates, with `L = min(3, t - 1)` for `t > 1`

Decision rule for round `t`:

1. Round 1:
   - Play `C`.

2. Round 2 onward:
   - Compute `\bar q_t`, the average of the observed opponent cooperation rates over the most recent `L` rounds.
   - Cooperate if either of the following holds:
     - `\bar q_t >= 1/2`
     - `m_{t-1} >= ceil((n-1)/2)`, meaning at least half of opponents cooperated in the previous round
   - Defect otherwise.

3. Recovery rule after defection:
   - If you defected in the previous round because cooperation fell below threshold, immediately return to `C` once the most recent observed opponent cooperation rate reaches at least `1/2` again.
   - Do not require multiple consecutive cooperative rounds to return to cooperation.

4. Endgame:
   - In the last round, play `C` if the most recent observed opponent cooperation rate is at least `1/2`; otherwise play `D`.
   - If there is a tie exactly at `1/2`, cooperate.

5. First-round exception for very small groups:
   - If `n = 2`, cooperate in round 1 and continue cooperating whenever the opponent cooperated in the previous round; defect only after an observed defection and return to cooperation immediately after one observed cooperation.

Compact pseudocode:

```text
if t == 1:
    play C
else:
    recent_rates = cooperation rates from last L rounds, L = min(3, t-1)
    bar_q = average(recent_rates)
    if bar_q > 1/2:
        play C
    else if bar_q == 1/2:
        play C
    else if m_{t-1} >= ceil((n-1)/2):
        play C
    else:
        play D
```

State update:
- After each round, record only the number of opponents who cooperated.
- Use a short moving window so that isolated defections do not break cooperation permanently.
- If cooperation has been stable for several rounds, continue cooperating unless the recent average drops below the threshold.
- If cooperation repeatedly collapses, keep using the same rule rather than escalating retaliation.
'''

description_PROSOCIAL_21 = '''
Round 1: cooperate.

For rounds 2 through r − 2:
- Let qₜ₋₁ be the number of opponents who cooperated in the previous round.
- Let qₜ₋₂ be the number of opponents who cooperated two rounds ago, if available.
- Set the cooperation threshold T = ceil((n − 1) / 2).
- Cooperate if qₜ₋₁ ≥ T or qₜ₋₂ ≥ T.
- Defect only if both of the last two observed rounds fell below T.

For the final two rounds:
- Cooperate unconditionally.

If the history is shorter than two rounds, treat missing observations as undefined and do not use them against cooperation; default to cooperating.

Equivalent pseudocode:

```text
if t == 1:
    play C
else if t >= r - 1:
    play C
else:
    T = ceil((n - 1) / 2)
    if (q[t-1] >= T) or (t >= 3 and q[t-2] >= T):
        play C
    else:
        play D
```

Interpretation of the decision rule:
- Cooperation is the default action.
- A temporary defect is used only after sustained low cooperation by the group.
- Any recovery to at least a majority of opponents cooperating immediately restores cooperation.
- The last rounds are always cooperative, with no attempt to punish.
'''

description_PROSOCIAL_22 = '''
State variables:
- `s_t`: number of opponents who cooperated in round `t`
- `L`: lookback window, `L = min(3, t-1)`
- `q_t`: average opponent cooperation rate over the last `L` rounds, normalized by `n-1`

Decision rule:

1. **Round 1:** play `C`
2. **Round 2:** play `C`
3. **From round 3 onward:**
   - Compute  
     `q_t = (sum of s_{t-1}, s_{t-2}, ..., s_{t-L}) / (L * (n-1))`
   - Play `C` if `q_t >= 1/2`
   - Play `D` if `q_t < 1/2`

Recovery rule:
- If you play `D` in round `t`, return to `C` immediately in round `t+1` unless the last `L` rounds all had `q < 1/2`
- If the last `L` rounds all had `q < 1/2`, continue playing `D` until at least one of the last `L` rounds has `q >= 1/2`

Endgame rule:
- In the last two rounds, ignore the recovery delay and play `C` whenever `q_t >= 1/2`; otherwise play `D`

Behavioral interpretation:
- Begin cooperatively.
- Stay cooperative while at least half of opponents are cooperating on average.
- Respond to sustained low cooperation with a brief, bounded defection.
- Re-enter cooperation as soon as cooperation reappears, without long punishment cycles.
'''

description_PROSOCIAL_23 = '''
Let \(m_t\) be the number of other players who cooperated in round \(t\), and let \(p_t = m_t/(n-1)\) be the observed cooperation rate among opponents.

### State
Maintain a single internal state variable `trust` initialized to `1`.

- `trust = 1` means cooperate by default.
- `trust = 0` means defect by default.

### Round 1
Play \(C\).

### Rounds \(2\) through \(r-1\)

Use the following rules in order:

1. **If the previous round was broadly cooperative, continue cooperating.**  
   If \(p_{t-1} \ge \tau_{\text{high}}\), play \(C\).

2. **If the previous round was moderately cooperative, keep cooperating unless there is a sharp drop.**  
   If \(\tau_{\text{mid}} \le p_{t-1} < \tau_{\text{high}}\), play \(C\) unless both of these hold:
   - \(p_{t-1} < p_{t-2}\), and
   - \(p_{t-1} < \tau_{\text{low}}\)
   
   In that case, play \(D\).

3. **If cooperation has fallen low, defect.**  
   If \(p_{t-1} < \tau_{\text{mid}}\), play \(D\).

4. **If you defected last round and cooperation recovered, forgive immediately.**  
   If you played \(D\) in round \(t-1\) and \(p_{t-1} \ge \tau_{\text{high}}\), play \(C\).

5. **If the group is stable but mixed, alternate toward cooperation.**  
   If \(p_{t-1}\) has stayed in \([\tau_{\text{mid}}, \tau_{\text{high}})\) for two consecutive rounds, play \(C\) unless you defected in both of the previous two rounds, in which case play \(D\) once and then reset to cooperation when \(p\) improves.

### Last round \(r\)

Play \(C\) unless the previous round was clearly uncooperative:
- If \(p_{r-1} < \tau_{\text{low}}\), play \(D\).
- Otherwise, play \(C\).

### Thresholds
Choose fixed thresholds based only on \(n\):

- \(\tau_{\text{high}} = 0.75\)
- \(\tau_{\text{mid}} = 0.50\)
- \(\tau_{\text{low}} = 0.25\)

If \(n\) is small and these thresholds are too coarse, replace them with exact counts:
- cooperate when at least \(\lceil 0.75(n-1)\rceil\) opponents cooperated,
- cooperate in the mixed zone when at least \(\lceil 0.50(n-1)\rceil\) cooperated,
- defect when fewer than \(\lceil 0.25(n-1)\rceil\) cooperated.

### Optional smoothing for noisy histories
If the previous two rounds disagree, use the two-round average \(\bar p_{t-1} = (p_{t-1}+p_{t-2})/2\):

- play \(C\) if \(\bar p_{t-1} \ge \tau_{\text{mid}}\),
- play \(D\) otherwise.

### Compact pseudocode
```text
if t == 1:
    play C
else if t == r:
    if p[t-1] < tau_low:
        play D
    else:
        play C
else:
    if p[t-1] >= tau_high:
        play C
    else if p[t-1] < tau_mid:
        play D
    else:
        if previous_move == D and p[t-1] >= tau_high:
            play C
        else if p[t-1] >= tau_mid and (t >= 3 and p[t-1] < p[t-2] and p[t-1] < tau_low):
            play D
        else:
            play C
```

### Intended behavior
- Start cooperatively.
- Keep cooperating when others are mostly cooperative.
- Defect only after clear and sustained free-riding.
- Forgive immediately when cooperation returns.
- End cooperatively unless the group has clearly collapsed.
'''

description_PROSOCIAL_24 = '''
Cooperate in round 1.

After each round, compute the observed cooperation rate among the other n−1 players:
- Let x_t be the number of opponents who cooperated in round t.
- Let ρ_t = x_t / (n−1).

Maintain a target cooperation threshold θ_t and update it by the observed history:
- Initialize θ_1 = 1.
- After round t, set
  θ_{t+1} = 0.5·θ_t + 0.5·ρ_t

In round t+1, cooperate if and only if:
- ρ_t ≥ θ_t

Equivalent implementation:
- Start maximally cooperative.
- Continue cooperating as long as the group’s observed cooperation level is at least as high as your running expectation.
- If cooperation falls, lower your threshold gradually rather than immediately abandoning cooperation.

Edge rules:
- First round: cooperate.
- If all opponents cooperated in the previous round, cooperate again.
- If no opponent cooperated in the previous round, defect in the next round.
- If the observed cooperation rate is exactly at the threshold, cooperate.
- In the final round, cooperate unless the immediately preceding observed cooperation rate was zero; otherwise follow the same rule as usual.

Optional stabilization rule:
- Track the last two observed rates ρ_{t−1}, ρ_t.
- If ρ_t < ρ_{t−1} but still positive, cooperate one additional round before switching, to avoid overreacting to a single small decline.
- If ρ_t = 0 for two consecutive rounds, defect until cooperation reappears.

Pseudocode:
- round 1: play C
- for t ≥ 1:
  - observe x_t
  - ρ_t = x_t / (n−1)
  - θ_{t+1} = (θ_t + ρ_t)/2
  - play C in round t+1 iff ρ_t ≥ θ_t, else play D

Fallback behavior:
- If the history is unavailable, cooperate.
- If the observation is ambiguous, treat it as the last known cooperation rate.
'''

description_PROSOCIAL_25 = '''
**Adaptive conditional cooperation with forgiveness and endgame commitment**

- **State tracked after each round**
  - `m_t`: number of opponents who cooperated in round `t`
  - `s_t`: running cooperation rate among opponents, updated as an exponentially weighted average:
    - `s_0 = 0`
    - `s_t = 0.7 * s_{t-1} + 0.3 * (m_t / (n-1))`
  - `trend_t = s_t - s_{t-1}`

- **Round 1**
  - Cooperate.

- **Base decision rule for round t > 1**
  - Cooperate if all of the following hold:
    1. `s_{t-1} >= 0.5`
    2. `trend_{t-1} >= -0.15`
    3. The last round was not a severe defection collapse
       - severe collapse means `m_{t-1} <= floor((n-1)/3)`
  - Otherwise defect.

- **Forgiveness rule**
  - If you defected in round `t-1` and `m_{t-1} >= ceil(2(n-1)/3)`, return to cooperation immediately in round `t`.
  - If cooperation rate is borderline, defined as
    - `0.4 <= s_{t-1} < 0.5`
    - then cooperate for one trial round.
  - After a trial-round cooperation, continue cooperating if `m_t >= ceil((n-1)/2)`, otherwise defect next round.

- **Stability rule**
  - Once `s_t >= 0.75` for two consecutive rounds, cooperate in all remaining non-final rounds unless a severe collapse occurs.
  - A severe collapse resets the stability condition.

- **Final rounds**
  - If `t = r-1`, cooperate only if `m_{t-1} >= ceil((n-1)/2)`.
  - If `t = r`, cooperate only if `m_{r-1} >= ceil((n-1)/2)` and `s_{r-1} >= 0.6`; otherwise defect.
  - This keeps final-round behavior aligned with prior cooperation rather than unconditional endgame defection.

- **Very small groups**
  - If `n = 2`, simplify to:
    - cooperate in round 1
    - then mirror the opponent’s previous cooperation if they cooperated in the last round
    - defect after any opponent defection until they cooperate again

- **Implementation in pseudocode**
```text
if t == 1:
    play C
else:
    if t == r:
        play C if m[t-1] >= ceil((n-1)/2) and s[t-1] >= 0.6 else D
    elif t == r-1:
        play C if m[t-1] >= ceil((n-1)/2) else D
    elif defected last round and m[t-1] >= ceil(2*(n-1)/3):
        play C
    elif 0.4 <= s[t-1] < 0.5:
        play C
    elif s[t-1] >= 0.5 and trend[t-1] >= -0.15 and m[t-1] > floor((n-1)/3):
        play C
    else:
        play D
```

- **Prosocial orientation**
  - Start by cooperating.
  - Reward sustained cooperation quickly.
  - Forgive isolated defection when the group is broadly cooperative.
  - Defect only when cooperation has fallen too low or collapsed repeatedly.
  - Preserve cooperation through most of the game, with a final-round rule that protects against exploitation while still supporting cooperative groups.
'''

description_PROSOCIAL_26 = '''
Use a graduated conditional cooperation rule with forgiveness and endgame stability:

- Let \(m_t\) be the number of other players who cooperated in round \(t\).
- Let \(f_t = \frac{m_t}{n-1}\) be the observed cooperation rate among others.
- Let \(F_t\) be the smoothed cooperation estimate:
  \[
  F_t =
  \begin{cases}
  f_1 & t=1 \\
  \frac{2F_{t-1} + f_t}{3} & t\ge 2
  \end{cases}
  \]
- Let \(L_t\) be the recent trend indicator:
  \[
  L_t =
  \begin{cases}
  0 & t<3 \\
  f_t - f_{t-1} & t\ge 3
  \end{cases}
  \]

Decision rule for round \(t+1\):

1. Cooperate if all of the following hold:
   - \(F_t \ge \frac{2}{3}\)
   - \(L_t \ge -\frac{1}{3}\)
   - fewer than 2 of the last 3 rounds had \(f_s < \frac{1}{2}\)

2. Cooperate in a repair mode if:
   - \(F_t \in [\frac{1}{2}, \frac{2}{3})\), and
   - the last round had at least one cooperator (\(m_t \ge 1\))
   
   In repair mode, cooperate for one round regardless of the other conditions.

3. Defect if:
   - \(F_t < \frac{1}{2}\), or
   - the last two rounds both had \(m_s = 0\), or
   - the cooperation trend is sharply negative: \(L_t \le -\frac{1}{2}\)

4. Endgame rule:
   - In the final round, cooperate only if \(F_{r-1} \ge \frac{2}{3}\) and \(m_{r-1} \ge \frac{n-1}{2}\); otherwise defect.

Initial rounds:

- Round 1: cooperate.
- Round 2: cooperate if at least half of the other players cooperated in round 1; otherwise defect.
- Round 3: if round 2 had at least one cooperator, cooperate; if round 2 had none, defect.

Recovery rule after defection:
- If you defected in round \(t\) and round \(t\) had \(m_t \ge \frac{n-1}{2}\), return to cooperation immediately in round \(t+1\).
- If you defected because of a zero-cooperation round, require two consecutive rounds with \(m_s \ge \frac{n-1}{2}\) before returning to cooperation.

Persistent prosocial baseline:
- When the state is uncertain or borderline, choose cooperation unless the recent history clearly indicates sustained low cooperation.
- Never punish a single isolated drop by switching into prolonged defection.
- Favor rebuilding cooperation whenever there is evidence that at least some others are still contributing.
'''

description_PROSOCIAL_27 = '''
Start by cooperating.

Maintain a cooperation target based on the observed cooperation rate among the other players:

- Let m = n - 1.
- After round t, observe x_t = number of other players who cooperated, so 0 ≤ x_t ≤ m.
- Let q_t = x_t / m be the observed cooperation rate.

Decision rule for round t + 1:

1. Compute a smoothed cooperation estimate
   - Use the last three rounds when available:
     - Q = average of q_{t-2}, q_{t-1}, q_t
   - If fewer than three rounds have passed, average over all observed rounds so far.

2. Set a cooperation threshold
   - If t is early (first 20% of rounds, rounded up), cooperate whenever Q ≥ 0.25
   - Otherwise, cooperate whenever Q ≥ 0.40

3. Add forgiveness after low-cooperation rounds
   - If the immediately previous round had q_t = 0, defect for the next round only if Q < 0.20; otherwise keep cooperating.
   - If the immediately previous round had q_t ≤ 0.20, cooperate unless the last two smoothed averages both fell below the threshold.

4. Endgame behavior
   - In the final round, cooperate if q_t > 0.
   - In the final two rounds, if Q ≥ 0.30, cooperate; otherwise follow the threshold rule above.

5. Recovery rule
   - After any defect, return to cooperation immediately once Q reaches the relevant threshold again.
   - Never defect for more than two consecutive rounds.

Compact pseudocode:

- Round 1: play C
- For round t > 1:
  - Observe q_{t-1}
  - Let Q = mean of recent q values, up to 3 most recent rounds
  - If t is in the last round:
    - play C if q_{t-1} > 0 else D
  - Else if t is in the last two rounds:
    - play C if Q ≥ 0.30 else apply threshold rule
  - Else if t is in the first 20% of rounds:
    - play C if Q ≥ 0.25 else D
  - Else:
    - play C if Q ≥ 0.40 else D
  - If the last observed round had q_{t-1} = 0:
    - require Q ≥ 0.20 to cooperate; otherwise defect once

Behavioral policy:
- Begin by giving trust.
- Reward sustained cooperation quickly.
- Do not overreact to a single low-cooperation round.
- Punish persistent free-riding briefly, then re-open cooperation as soon as others show willingness to cooperate.
- Maintain a bias toward cooperation whenever there is any meaningful sign of reciprocity.
'''

description_PROSOCIAL_28 = '''
**State variables**

- `t`: current round index
- `h[t-1]`: number of opponents who cooperated in round `t-1`
- `m = n - 1`: number of opponents
- `p[t-1] = h[t-1] / m`: observed opponent cooperation rate in the previous round
- `s`: smoothed estimate of cooperation, updated recursively  
  `s = α * p[t-1] + (1 - α) * s`, with `α = 0.5`
- `d`: consecutive rounds in which observed opponent cooperation was below the cooperation threshold

Initialize:
- `s = 1`
- `d = 0`

**Decision rule**

Choose a cooperation threshold:
- `τ = 0.5`

Each round `t`:

1. **Round 1**
   - Play `C`

2. **Rounds 2 to r**
   - Update `s` using the previous round’s observation:
     - `s = 0.5 * (h[t-1] / (n - 1)) + 0.5 * s`
   - If `h[t-1] / (n - 1) >= τ`, set `d = 0`
   - Otherwise, set `d = d + 1`

3. **Action choice**
   - Play `C` if all of the following hold:
     - `s >= τ`
     - `d <= 2`
     - `t < r` or `h[t-1] > 0`
   - Otherwise, play `D`

**Endgame rule**

- In the final round `t = r`, play `C` only if the previous round had at least one cooperating opponent:
  - If `h[r-1] > 0`, play `C`
  - If `h[r-1] = 0`, play `D`

**Recovery rule after defection**

If you played `D` in round `t`, reset to cooperation immediately in round `t+1` unless the last two observed rounds both had:
- `h[t] / (n - 1) < τ`
- `h[t-1] / (n - 1) < τ`

This means:
- one bad round does not lock in defection
- two consecutive weak rounds trigger caution
- any clear rebound restores cooperation

**Compact pseudocode**

```text
s = 1
d = 0

for t in 1..r:
    if t == 1:
        play C
    else:
        p = h[t-1] / (n - 1)
        s = 0.5 * p + 0.5 * s

        if p >= 0.5:
            d = 0
        else:
            d = d + 1

        if t == r:
            if h[t-1] > 0:
                play C
            else:
                play D
        else:
            if s >= 0.5 and d <= 2:
                play C
            else:
                play D
```

**Behavioral pattern**

- Start cooperatively.
- Continue cooperating while the group shows at least moderate reciprocity.
- Defect only after sustained evidence of broad noncooperation.
- Return to cooperation as soon as cooperation recovers.
- Finish cooperatively whenever there is any recent sign of mutual participation.
'''

description_PROSOCIAL_29 = '''
Let `m = n - 1` be the number of opponents.

State variables:
- `bad_streak`: number of consecutive recent rounds in which opponent cooperation was below `ceil(m/2)`
- `last_s`: number of opponents who cooperated in the previous round
- initialize `bad_streak = 0`

Decision rule for round `t`:

1. **Round 1:** play `C`
2. **Round 2:** play `C`
3. **Final round:** play `C`
4. **All other rounds:**
   - If `last_s >= ceil(m/2)`, play `C` and set `bad_streak = 0`
   - If `last_s < ceil(m/2)`:
     - increment `bad_streak`
     - if `bad_streak == 1`, play `C`
     - if `bad_streak >= 2`, play `D`
   - If `last_s = m`, play `C` and set `bad_streak = 0`

Update after each round:
- Observe the number `s` of opponents who cooperated
- Set `last_s = s`

Compact pseudocode:

```text
m = n - 1
bad_streak = 0

for round t = 1..r:
    if t == 1 or t == 2 or t == r:
        action = C
    else if last_s >= ceil(m/2):
        action = C
        bad_streak = 0
    else:
        bad_streak += 1
        if bad_streak == 1:
            action = C
        else:
            action = D

    play(action)

    observe s  # number of opponents who cooperated
    last_s = s
```

Behavioral intent:
- Start by cooperating immediately.
- Continue cooperating through isolated drops in others’ cooperation.
- Defect only after sustained low cooperation from opponents.
- Return to cooperation as soon as the observed cooperation level recovers.
'''

description_PROSOCIAL_30 = '''
Let \(m_t\) be the number of other players who cooperated in round \(t\), and let

\[
s_t = \frac{m_t}{n-1}
\]

be the observed cooperation share among opponents in round \(t\).

Maintain a running cooperation estimate \(q_t\) over opponents, initialized at \(q_1 = 1\), and updated after each round by

\[
q_{t+1} = \lambda q_t + (1-\lambda)s_t
\]

with \(\lambda = \frac{2}{3}\).

Decision rule for round \(t\):

1. **Round 1:** play \(C\).
2. **Rounds 2 through \(r\):**
   - If \(t=r\) and \(q_t \ge \frac{1}{2}\), play \(C\); otherwise play \(D\).
   - If \(t<r\):
     - play \(C\) if \(q_t \ge \frac{1}{2}\),
     - play \(D\) if \(q_t < \frac{1}{2}\).

Adjustment after each round:

- If you played \(C\) and \(m_t = 0\), set \(q_{t+1} = 0\).
- If you played \(D\) and \(m_t = n-1\), set \(q_{t+1} = 1\).
- Otherwise update by the smoothing rule above.

Additional edge-case handling:

- **If all opponents cooperated in the previous round** \((m_t=n-1)\), cooperate next round.
- **If no opponents cooperated in the previous round** \((m_t=0)\), defect next round.
- **If cooperation is at least half of opponents**, stay cooperative.
- **If cooperation falls below half of opponents for two consecutive rounds**, defect until the smoothed estimate returns to at least \(\frac{1}{2}\).

Terminal-round rule:

- In the final round, mirror the current estimate exactly:
  - cooperate if \(q_r \ge \frac{1}{2}\),
  - defect otherwise.

This policy begins with cooperation, rewards sustained cooperative behavior, withdraws support when cooperation collapses, and returns to cooperation as soon as the observed group becomes reliably cooperative again.
'''

description_PROSOCIAL_31 = '''
**Adaptive Reciprocity with Forgiveness**

Maintain these state variables:

- `s_t`: number of observed opponent cooperations in round `t`
- `h_t`: cooperation rate in recent history
- `E_t`: trust score in `[0,1]`
- `m_t`: streak of consecutive rounds with low opponent cooperation
- `f_t`: streak of consecutive rounds with high opponent cooperation

Initialize:

- `E_1 = 0.5`
- `m_1 = 0`
- `f_1 = 0`

Decision rule for round `t`:

1. **First round**
   - Play `C`.

2. **Update after each round**
   - Let `x_t = s_t / (n-1)` be the fraction of opponents who cooperated in round `t`.
   - Update trust:
     - `E_{t+1} = 0.6 * E_t + 0.4 * x_t`
   - Update streaks:
     - If `x_t >= 0.5`, then `f_{t+1} = f_t + 1`, `m_{t+1} = 0`
     - Otherwise, `m_{t+1} = m_t + 1`, `f_{t+1} = 0`

3. **Core choice rule**
   - Cooperate if at least one of the following holds:
     - `E_t >= 0.45`
     - `x_{t-1} >= 0.5`
     - `f_t >= 2`
   - Defect otherwise.

4. **Repair rule after low cooperation**
   - If opponents cooperated at a very low rate in the previous round, do not immediately punish:
     - If `x_{t-1} > 0` and `x_{t-1} < 0.25`, cooperate once more unless `m_t >= 2`.
   - If the low-cooperation pattern persists:
     - If `m_t >= 2`, defect until `x_t >= 0.5` again.

5. **Reconciliation rule**
   - After any round with `x_t >= 0.75`, reset to full cooperation mode:
     - `E_{t+1} = max(E_{t+1}, 0.7)`
     - `m_{t+1} = 0`
     - Cooperate in the next round.

6. **Last rounds**
   - In the final round, cooperate if `x_{r-1} >= 0.33` or `E_r >= 0.4`.
   - Otherwise defect.
   - In the final two rounds, do not introduce a new punishment cycle; use the trust score and the most recent observed cooperation only.

7. **Edge cases**
   - If all opponents defect in a round, defect in the next round.
   - If all opponents cooperate in a round, cooperate in the next round.
   - If observations are inconsistent or unavailable, default to `C` on the next round.

**Compact pseudocode**

```text
if t == 1:
    play C
else:
    x = s_{t-1} / (n-1)

    E = 0.6 * E + 0.4 * x

    if x >= 0.5:
        f += 1
        m = 0
    else:
        m += 1
        f = 0

    if t >= r-1:
        if x >= 0.33 or E >= 0.4:
            play C
        else:
            play D
    else if x >= 0.75:
        play C
    else if m >= 2:
        play D
    else if E >= 0.45 or x >= 0.5 or f >= 2:
        play C
    else if 0 < x < 0.25:
        play C
    else:
        play D
```
'''

description_PROSOCIAL_32 = '''
Play a conditional cooperation strategy with a built-in floor and forgiveness:

1. First round
- Cooperate.

2. Maintain two running quantities from history:
- `m_t`: number of opponents who cooperated in round `t`
- `q_t = m_t / (n - 1)`: observed opponent cooperation rate in round `t`
- `Q_t`: smoothed cooperation estimate after round `t`

Initialize:
- `Q_0 = 1`

Update after each round:
- `Q_t = 0.7 * Q_{t-1} + 0.3 * q_t`

3. Decision rule for round `t+1`
- Cooperate if `Q_t >= 0.5`
- Defect if `Q_t < 0.5`

4. Forgiveness rule
- If the previous round had at least half of opponents cooperating, cooperate immediately even if earlier history was poor.
- If cooperation has been low for several rounds, require two consecutive low-opposition rounds before switching to defection:
  - If `q_t < 0.5` but `q_{t-1} >= 0.5`, keep cooperating.
  - Defect only if `q_t < 0.5` and `q_{t-1} < 0.5`.

5. Recovery rule
- After any round with `q_t >= 0.5`, reset to cooperation in the next round.

6. Last round
- Cooperate if `Q_{r-1} >= 0.5`
- Otherwise defect

7. Edge cases
- If `n = 2`, use the same rule with `q_t` equal to the single opponent’s action.
- If `r = 2`, cooperate in round 1, then apply the rule to round 2 using round 1’s observation.
- If no prior rounds exist, cooperate.

8. Optional stricter prosocial mode
- If the observed opponent cooperation rate is at least `2/3`, always cooperate.
- If it falls below `1/3` for two rounds in a row, defect until cooperation recovers to at least `1/2`.

Pseudocode:

```
if t == 1:
    play C
else:
    q_t = m_t / (n - 1)
    Q_t = 0.7 * Q_{t-1} + 0.3 * q_t

    if q_t >= 0.5:
        play C
    else if t >= 3 and q_{t-1} < 0.5 and Q_t < 0.5:
        play D
    else:
        play C
```
'''

description_ALTRUISTIC_5 = '''
State variables:
- `bad_streak`: consecutive rounds in which the number of cooperating opponents was below a minimum trust threshold
- `probe_timer`: counts down a short recovery test after a defensive pause

Define:
- `majority = ceil((n - 1) / 2)`
- `near_all = n - 2` if `n > 3`, otherwise `1`

Decision rule by round:

1. **Round 1**
   - Play `C`.

2. **If `probe_timer > 0`**
   - Play `C`.
   - Decrement `probe_timer` by 1.
   - If the observed cooperating opponents in this round are at least `majority`, set `bad_streak = 0` and return to normal cooperative mode.
   - Otherwise keep `bad_streak` unchanged.

3. **Normal cooperative mode**
   - Play `C` unless the previous round showed strong collapse:
     - If the number of cooperating opponents in the previous round was at least `majority`, play `C` and set `bad_streak = 0`.
     - If it was below `majority`, play `C` anyway, but increment `bad_streak` by 1.
   - If `bad_streak` reaches `2`, switch into defensive recovery mode on the next round:
     - set `probe_timer = 2`
     - reset `bad_streak = 0`

4. **Defensive recovery mode**
   - During the two rounds of `probe_timer`, play `C` once per round.
   - If either probe round restores cooperation to at least `majority`, immediately return to normal cooperative mode.

5. **Exception for near-universal defection**
   - If the previous round had fewer than `near_all` cooperating opponents, treat it as a collapse signal:
     - enter defensive recovery mode by setting `probe_timer = 2`
   - Even then, the strategy still probes with cooperation rather than abandoning cooperation permanently.

6. **Final round**
   - Play `C` regardless of history.

Behavior summary:
- Default action is `C`.
- Temporary defensive pauses are only triggered after sustained collapse, not after one isolated bad round.
- Recovery always happens through cooperative probing, never through permanent retaliation.
- The strategy never escalates beyond short, bounded pauses, and always reopens the door to cooperation.
'''

description_ALTRUISTIC_6 = '''
Play C in round 1.

For each later round t, let h_t be the number of opponents who cooperated in round t-1, and let H_t be the moving average of observed opponent cooperation over the last m rounds, where m = min(3, t-1).

Decision rule:
- If t = 1: play C.
- If t = r: play C.
- If t > 1:
  - Compute cooperation rate q_t = H_t / (n - 1).
  - Play C if q_t ≥ 0.4.
  - Play D if q_t < 0.4.

Refinement for stubborn defection:
- Track a streak s of consecutive rounds in which h_t = 0.
- If s ≥ 2, play D until either:
  - at least one opponent cooperates in a round, or
  - the final round is reached, in which case play C.
- Reset s to 0 as soon as h_t > 0.

Refinement for recovery:
- If h_t ≥ ceil((n - 1) / 2), play C for the next 2 rounds regardless of the moving average.
- If h_t is between 1 and ceil((n - 1) / 2) - 1, continue using the moving-average rule, but treat this as a sign to remain cooperative if the average is exactly on the threshold.

Tie-breaking:
- If q_t = 0.4 exactly, play C.

Compact pseudocode:

```
if t == 1:
    action = C
elif t == r:
    action = C
else:
    update H_t from last min(3, t-1) rounds
    q_t = H_t / (n - 1)

    if h_{t-1} == 0:
        s += 1
    else:
        s = 0

    if s >= 2:
        action = D
    elif h_{t-1} >= ceil((n - 1)/2):
        action = C for next 2 rounds
    elif q_t >= 0.4:
        action = C
    else:
        action = D
```

If the game ever reaches a run of widespread cooperation, remain cooperative as long as the observed cooperation rate stays at or above the threshold. If cooperation collapses, switch to temporary defection only long enough to avoid being repeatedly exploited, then return to cooperation as soon as any meaningful cooperation reappears.
'''

description_ALTRUISTIC_7 = '''
Round 1: cooperate.

For every later round t, let x_{t-1} be the number of opponents who cooperated in the previous round, and let x̄_{t-2:t-1} be the average number of opponent cooperators over the last two observed rounds when available.

Cooperate if any of the following holds:
- t is one of the final two rounds
- x_{t-1} ≥ ceil((n-1)/2)
- x̄_{t-2:t-1} ≥ ceil((n-1)/3)
- there is not yet a run of two consecutive rounds with x < ceil((n-1)/3)

Defect only when all of the following are true:
- t is not one of the final two rounds
- the last two observed rounds both had x < ceil((n-1)/3)
- the two-round average x̄_{t-2:t-1} is also below ceil((n-1)/3)

After any defect round, return to cooperation immediately if the next observed round reaches either:
- x_{t} ≥ ceil((n-1)/2), or
- x_{t} > 0 and x_{t-1} ≥ ceil((n-1)/3)

If n = 2, use the same rule with the thresholds interpreted on the single opponent:
- cooperate initially
- continue cooperating as long as the opponent cooperated in at least one of the last two rounds
- defect only after two straight rounds of opponent defection, then resume cooperation as soon as the opponent cooperates again

If no history is available for a rule that references prior rounds, treat the missing data as favoring cooperation.
'''

description_ALTRUISTIC_8 = '''
Round 1: cooperate.

Let `h_t` be the number of opponents who cooperated in round `t`, and let `H_t = Σ_{s=1..t} h_s`.

Maintain a moving cooperation benchmark:
- `b_t = round(0.6 × (n - 1))` for round `t`
- If `r` is very small, use `b_t = ceil((n - 1)/2)`

Decision rule for round `t ≥ 2`:

1. Compute the recent cooperation rate among opponents over the last `m = min(3, t - 1)` rounds:
   - `R_t = (1/m) × Σ_{s=t-m}^{t-1} h_s / (n - 1)`

2. Cooperate if both conditions hold:
   - `R_t ≥ 0.5`
   - In the immediately preceding round, at least `b_t` opponents cooperated

3. Otherwise, defect for one round only, then re-evaluate next round.

Forgiveness rule:
- After any defecting round, return to cooperation immediately if the most recent round had at least `ceil((n - 1)/2)` opponent cooperators.
- If the last two rounds both met that threshold, cooperate regardless of older history.

Last-round rule:
- Cooperate unless the previous two rounds were both below `ceil((n - 1)/2)` opponent cooperators.
- If the environment has been mostly cooperative in the final three rounds, always cooperate in the last round.

Stability rule against intermittent free-riding:
- If the opponent cooperation count drops by at least `ceil((n - 1)/3)` from one round to the next, defect for exactly one round, then resume the normal rule.
- If cooperation is restored in the next round, do not punish further.

Cold-start rule:
- If there is no history, cooperate.
- If only one prior round exists, imitate the majority of opponents from that round.

Altruistic priority:
- Default to cooperation whenever the recent history is ambiguous.
- Use defection only as a brief signal to stop being exploited, never as a prolonged punishment.
- Never defect in two consecutive rounds unless the last three rounds all had fewer than half of opponents cooperating.
'''

description_ALTRUISTIC_9 = '''
Round 1: play C.

After each round t, let a_t be the number of opponents who cooperated in round t, and let h_t be the average opponent cooperation rate over the last up to 3 rounds:
- if t = 1, h_t = a_1 / (n - 1)
- if t = 2, h_t = (a_1 + a_2) / (2(n - 1))
- if t ≥ 3, h_t = (a_{t-2} + a_{t-1} + a_t) / (3(n - 1))

Decision rule for round t + 1:

1. If t is among the last two rounds of the game, play C.
2. Otherwise, play C unless one of the following defection conditions holds:
   - Severe free-riding: h_t < 0.35
   - Persistent decline: a_t < a_{t-1} and a_{t-1} < a_{t-2} for t ≥ 3
   - Near-universal defection: a_t ≤ 1 and a_{t-1} ≤ 1 for t ≥ 2

3. If any defection condition holds, play D for the next round.
4. If you played D in the previous round, return to C immediately once either of these happens:
   - a_t / (n - 1) ≥ 0.50
   - a_t > a_{t-1}

Tie handling:
- If a condition is exactly on the threshold, favor C.
- If multiple conditions conflict, the rule that favors C takes precedence except in the last two rounds, where C is always chosen.

Compact form:
- Default action: C
- Switch to D only after clear evidence that cooperation has collapsed
- Switch back to C at the first sign of recovery
- Force C in the closing rounds

State machine:
- State = Cooperative
  - play C
  - move to Defensive if h_t < 0.35 for one full window, or if the last two rounds show near-universal defection
- State = Defensive
  - play D
  - move back to Cooperative as soon as cooperation recovers above 50% or rises from the previous round

This keeps the strategy consistently pro-social, supports mutual cooperation early, forgives recovery quickly, and avoids repeatedly contributing into sustained free-riding.
'''

description_ALTRUISTIC_10 = '''
Round 1: cooperate.

Round t > 1:
1. Let H_t be the number of opponents who cooperated in round t - 1.
2. Let q_t = H_t / (n - 1), the observed cooperation rate among opponents.
3. Cooperate if q_t ≥ θ_t.
4. Defect if q_t < θ_t.

Threshold schedule:
- Set θ_2 = 0.5.
- For rounds t ≥ 3, use
  θ_t = max(0.5, 1 - 1 / sqrt(t - 1)).

Memory adjustment:
- If the last two observed cooperation rates both increased, decrease the threshold by 1/(2(n-1)) for the next round, down to a minimum of 0.5.
- If the last two observed cooperation rates both decreased, increase the threshold by 1/(2(n-1)) for the next round, up to a maximum of 1.

Last-round rule:
- Cooperate in the final round unless the previous round had zero opponent cooperation.

Special cases:
- If n = 2, cooperate in round 1, then cooperate whenever the other player cooperated in the previous round; otherwise cooperate once after any single defection before switching to defection.
- If all observed opponent cooperation rates have been 0 for three consecutive rounds, defect until cooperation reappears.
- If all observed opponent cooperation rates have been 1 for two consecutive rounds, cooperate unconditionally for the rest of the game.

Implementation form:

```
round 1:
    play C

round t > 1:
    q = cooperators_last_round / (n - 1)

    if t == r:
        if cooperators_last_round == 0:
            play D
        else:
            play C
        stop

    if last_two_qs both increased:
        θ = max(0.5, θ - 1/(2(n-1)))
    else if last_two_qs both decreased:
        θ = min(1, θ + 1/(2(n-1)))

    if q == 0 for three consecutive rounds:
        play D
    else if q == 1 for two consecutive rounds:
        play C
    else if q >= θ:
        play C
    else:
        play D
```

Decision intent:
- Start by trusting others.
- Match sustained cooperation quickly.
- Forgive occasional defections.
- Withhold cooperation when the group repeatedly free-rides.
- End generously unless the group has just fully abandoned cooperation.
'''

description_ALTRUISTIC_11 = '''
**Strategy: Generous Adaptive Cooperation**

**State variables**
- `h`: number of cooperations observed among the other `n-1` players in the previous round
- `p`: estimated cooperation rate among others, initialized to `1/2`
- `s`: streak of consecutive rounds in which observed cooperation among others was high

**Decision rule for round t**

1. **Round 1**
   - Play `C`.

2. **Round 2 onward**
   - Compute the observed cooperation rate from the previous round:
     - `q = h / (n - 1)`
   - Update the smoothed estimate:
     - `p = (2p + q) / 3`
   - Cooperate if at least one of these holds:
     - `q >= 1/2`
     - `p >= 1/2`
     - `s >= 2`
   - Otherwise defect.

**Streak update**
- If `q >= 1/2`, increase `s` by 1.
- If `q < 1/2`, reset `s = 0`.

**Last-round rule**
- Cooperate in the last round.

**Forgiveness rule**
- If the previous round had fewer than half of the others cooperating, still cooperate once every 3 rounds unless the last two rounds also had fewer than half cooperating.
- This is implemented by the `p` update and the `s` threshold above.

**Behavioral interpretation**
- Start cooperatively.
- Continue cooperating whenever there is any moderate or better sign of reciprocity.
- After a low-cooperation round, remain willing to give the group another chance.
- Only switch to defection after repeated evidence that cooperation is not being met.
- Always end cooperatively, preserving an altruistic final move.
'''

description_ALTRUISTIC_12 = '''
Start by cooperating.

Let:
- `t` be the current round, starting at 1
- `m_t` be the number of opponents who cooperated in round `t`
- `M_t` be a running smoothed estimate of opponent cooperation, updated by  
  `M_t = (1 - α) M_{t-1} + α m_t`, with `α = 0.35`
- `q_t = M_t / (n - 1)` be the estimated cooperation rate among opponents

Decision rule:

1. First round:
   - Play `C`

2. Ongoing rounds:
   - Play `C` if either of the following holds:
     - `q_t >= 0.40`
     - `m_t >= ceil((n - 1) / 2)`
   - Play `D` only if both of the following hold:
     - `q_t < 0.40`
     - `m_t < ceil((n - 1) / 2)`

3. Recovery rule:
   - If you played `D` in the previous round, return to `C` immediately after any round with `m_t >= ceil((n - 1) / 2)`.

4. Persistence rule against sustained defection:
   - If `m_t = 0` for `L = max(2, floor(r / 4))` consecutive rounds, play `D` until at least one opponent cooperates again.
   - As soon as `m_t > 0`, resume `C` next round.

5. Endgame:
   - In the last round, play `C` unless the previous `L` rounds all had `m_t = 0`.

6. Tie and borderline cases:
   - If `q_t` is exactly `0.40`, play `C`
   - If `m_t` is exactly `ceil((n - 1) / 2)`, play `C`

Pseudocode:

```text
Initialize M = (n - 1) / 2
Initialize zero_streak = 0
Play C in round 1

For round t = 2 to r:
    observe m = number of opponents who cooperated in round t-1
    M = (1 - α) * M + α * m
    q = M / (n - 1)

    if m == 0:
        zero_streak += 1
    else:
        zero_streak = 0

    if t == r:
        if zero_streak >= L:
            play D
        else:
            play C
    else if zero_streak >= L:
        play D
    else if q >= 0.40 or m >= ceil((n - 1) / 2):
        play C
    else:
        play D
```

Behavioral principles:
- Default to cooperation
- Treat isolated defection as noise
- Continue cooperating while a substantial minority or majority cooperates
- Defect only after a clear, sustained collapse in cooperation
- Re-enter cooperation immediately when cooperation reappears
'''

description_ALTRUISTIC_13 = '''
Let \(m_t\) be the number of other players who cooperated in round \(t\), and let \(h_t = \frac{1}{n-1}\sum_{s=1}^{t} m_s\) be the running average cooperation rate among opponents up to round \(t\).

Use three states: explore, support, and protect.

**Round 1**
- Play \(C\).

**Round \(t \ge 2\)**
- Compute:
  - \(q_{t-1} = m_{t-1}/(n-1)\), the observed cooperation rate in the previous round
  - \(h_{t-1}\), the running average cooperation rate so far
- Set the cooperation threshold
  \[
  \tau_t = \max\!\left(\frac{1}{2}, \frac{1}{k}\right)
  \]
- Play according to:

1. **Universal support**
   - If \(q_{t-1} \ge \tau_t\), play \(C\).

2. **Forgiving recovery**
   - If \(q_{t-1} < \tau_t\) but \(h_{t-1} \ge \tau_t\), play \(C\).

3. **Temporary protection**
   - If \(q_{t-1} < \tau_t\) and \(h_{t-1} < \tau_t\), play \(D\).

**Reset rule**
- After any round in which \(q_t \ge \tau_{t+1}\), return to playing \(C\) in the next round.

**Late-game rule**
- For the final round, play \(C\) unless the previous two rounds both had \(q < \tau_t\); in that case play \(D\).

**Edge cases**
- If \(n=2\), this becomes:
  - cooperate on round 1
  - continue cooperating whenever the other player cooperated in at least one of the last two rounds
  - defect only after two consecutive low-cooperation observations
- If \(k \le 2\), keep the same threshold rule but require stronger evidence before staying cooperative:
  - cooperate only when \(q_{t-1} \ge 1/k\) or when the long-run average \(h_{t-1} \ge 1/k\)
- If cooperation is ever unanimous in two consecutive rounds, cooperate in every later round unless a full-round collapse occurs in the immediately preceding round

**Behavioral principle**
- Start generous.
- Continue cooperating whenever there is a credible cooperative pattern.
- Defect only as a brief shield against sustained defection.
- Re-enter cooperation immediately after any observable recovery.
'''

description_ALTRUISTIC_14 = '''
Play C in round 1.

For round t > 1, let m be the number of opponents who cooperated in round t - 1, and let p = m / (n - 1).

Maintain a cooperation target τ_t that starts at 1 and updates after each round:
- If p ≥ τ_t, set τ_{t+1} = min(1, τ_t + 1 / (2r))
- If p < τ_t, set τ_{t+1} = max(0, τ_t - 1 / (2r))

Decision rule for round t:
- Cooperate if p ≥ τ_t
- Defect if p < τ_t

Terminal-round rule:
- In the last round, cooperate if p ≥ max(1/2, τ_t - 1 / (2r))
- Otherwise defect

Edge cases:
- If n = 2, interpret p as 1 if the opponent cooperated, 0 otherwise.
- If all opponents cooperated in the previous round, always cooperate next round.
- If no opponent cooperated in the previous round, defect for the next round only if this occurs in two consecutive rounds; otherwise keep cooperating.
- If the observed cooperation count is unchanged from the previous round, keep the same action as the previous round.

Fallback altruistic mode:
- If history is unavailable for any reason, play C.
- If tied between cooperating and defecting under the rules above, play C.

Pseudocode:

```
initialize τ = 1
play C in round 1

for t = 2 to r:
    observe m = # opponents who cooperated in round t-1
    p = m / (n - 1)

    if t == r:
        threshold = max(1/2, τ - 1/(2r))
    else:
        threshold = τ

    if p >= threshold:
        action = C
        τ = min(1, τ + 1/(2r))
    else:
        action = D
        τ = max(0, τ - 1/(2r))

    if m == n - 1:
        action = C
        τ = min(1, τ + 1/(2r))
```

Behavioral default:
- Start maximally cooperative.
- Continue cooperating whenever a majority of opponents cooperated in the last round.
- Require repeated noncooperation before responding with defection.
- Restore cooperation immediately once opponent cooperation recovers.
'''

description_ALTRUISTIC_15 = '''
Cooperate in round 1.

For round t > 1, let:
- O_t = number of opponents who cooperated in round t
- N = n - 1 = number of opponents
- h_t = average opponent cooperation rate over previous rounds:
  h_t = (1 / (t - 1)) × Σ(s=1 to t-1) (O_s / N)

Decision rule:
1. Compute recent cooperation momentum:
   - m_t = (O_{t-1} / N) if t > 2, else h_t
2. Cooperate if either of the following holds:
   - O_{t-1} / N ≥ 1/2
   - h_t ≥ 1/2 and m_t ≥ 1/3
3. Defect otherwise.

Strong forgiveness rule:
- If the previous round had at least one opponent cooperating, and the long-run average h_t is at least 1/3, cooperate even if the most recent round fell below the main threshold.
- If the previous round had zero cooperators, defect unless h_t ≥ 2/3.

Recovery rule:
- After any round with zero opponent cooperators, keep defecting until either:
  - two consecutive rounds each have at least one-third of opponents cooperating, or
  - the cumulative average h_t reaches 1/2.

Last-round rule:
- Cooperate in the final round if h_r ≥ 1/3.
- Otherwise, follow the normal decision rule.

Compact form:

if t = 1:
    play C
else:
    recent = O_{t-1} / N
    avg = h_t
    if t = r and avg < 1/3:
        play D
    elif recent >= 1/2:
        play C
    elif avg >= 1/2 and recent >= 1/3:
        play C
    elif previous round had O_{t-1} > 0 and avg >= 1/3:
        play C
    elif previous round had O_{t-1} = 0 and avg < 2/3:
        play D
    else:
        play D

Extra tie-breaking bias:
- When in doubt, choose C if the history is mixed and the opponents have shown any sustained cooperation.
- Choose D only after a clear pattern of persistent defection or collapse in cooperation.
'''

description_ALTRUISTIC_16 = '''
Start with cooperation.

For round \(t\), let \(m_{t-1}\) be the number of opponents who cooperated in the previous round, and let \(f_{t-1} = \frac{m_{t-1}}{n-1}\).

Decision rule:

- Round 1: play \(C\).
- Round \(t>1\):
  - If \(f_{t-1} \ge \tau_t\), play \(C\).
  - If \(f_{t-1} < \tau_t\), play \(D\).

Threshold schedule:
- Set \(\tau_t = \max\!\left(\frac{1}{2},\, 1 - \frac{t-1}{r-1}\cdot \frac{1}{2}\right)\).
- Equivalently:
  - early rounds require a clear cooperative signal,
  - later rounds gradually lower the bar for cooperating,
  - the final round always uses \(\tau_r = \frac{1}{2}\).

Adjustment for personal history:
- Let \(s_{t-1}\) be the number of rounds up to \(t-1\) in which at least half of the opponents cooperated.
- If \(s_{t-1} \ge \lceil (t-1)/2 \rceil\), cooperate whenever \(f_{t-1} \ge \tau_t - \frac{1}{n-1}\).
- Otherwise keep the standard threshold.

Endgame rule:
- In the last two rounds, cooperate if at least one-third of opponents cooperated in the previous round.
- In the final round, never switch to a harsher threshold than the one used in the penultimate round.

Recovery rule after widespread defection:
- If fewer than one-quarter of opponents cooperated in the previous round, defect for exactly one round, then return to the normal threshold schedule the next round.
- If cooperation rebounds to at least half of opponents, immediately return to cooperation.

Tie-breaking and anonymity handling:
- Since only the count matters, treat all histories with the same sequence of counts the same.
- If the observed count is exactly on the threshold, cooperate.

Behavioral pattern:
- Cooperate by default.
- Defect only as a short, measured response to persistent low cooperation.
- Never escalate punishment beyond a single round of defection.
- Never require perfect cooperation from others before cooperating yourself.
- Gradually become more forgiving as the game approaches the end.
'''

description_ALTRUISTIC_17 = '''
Start by cooperating.

Round 1:
- Play C.

For every later round t:
1. Let m be the number of opponents who cooperated in round t−1.
2. Let q = m / (n−1), the observed cooperation rate among opponents.
3. Maintain a cooperation memory score s, initialized to 0.
   - Update after each round:  
     s ← 0.7s + q

Decision rule:
- Play C if either of the following holds:
  - q ≥ 1/2
  - s ≥ 1/2
- Otherwise play D.

Escalation and forgiveness:
- If q = 0 for two consecutive rounds, play D for the next round.
- If after any D-round the observed q in the following round is at least 1/3, return to C immediately.
- If cooperation has been at least 1/2 in each of the last three rounds, lock into C for the remaining rounds.

Endgame behavior:
- In the final two rounds, keep the same decision rule; do not switch to unconditional defection.
- If the last observed q is at least 1/3, cooperate in the final round even if the score s is slightly below 1/2.

Defect only as a bounded response:
- D is used only after sustained low cooperation by others, never as a first move and never for more than one round at a time unless the group remains persistently noncooperative.

Altruistic default:
- When uncertain, favor C.
- Treat partial cooperation as sufficient reason to continue cooperating.
- Give repeated opportunities for mutual cooperation to recover after a low-cooperation stretch.
'''

description_ALTRUISTIC_18 = '''
Initialize:

- Let `s_t` be the number of opponents who cooperated in round `t`.
- Let `m_t = s_t / (n - 1)` be the observed opponent cooperation rate in round `t`.
- Let `H_t = (m_1, ..., m_{t-1})` be the history before round `t`.
- Set `belief_t = average(m_1, ..., m_{t-1})` when `t > 1`.

Decision rule:

1. Round 1:
   - Play `C`.

2. Round 2:
   - If `s_1 = n - 1`, play `C`.
   - Otherwise, play `C` unless `s_1 = 0`, in which case play `D`.

3. Rounds 3 through `r - 1`:
   - Compute `belief_t = average(m_1, ..., m_{t-1})`.
   - Play `C` if either of the following holds:
     - `belief_t >= 1/2`, or
     - the most recent round had at least one opponent cooperating and the last three-round average cooperation rate among opponents is at least `1/3`.
   - Play `D` only if both hold:
     - the last two rounds had zero opponent cooperation, and
     - `belief_t < 1/4`.

4. Last round `t = r`:
   - Play `C` if at least one opponent cooperated in round `r - 1`.
   - Otherwise, play `C` unless the last three rounds all had zero opponent cooperation, in which case play `D`.

Update rule after each round:

- Record `m_t`.
- If `s_t > 0`, reset the punishment counter to `0`.
- If `s_t = 0`, increase the punishment counter by `1`.
- Never punish for more than two consecutive rounds.

Operational policy:

- Default action is `C`.
- Temporary `D` is used only after sustained complete defection by others.
- Immediately return to `C` after any round with at least one cooperating opponent.

Equivalent pseudocode:

```text
if t == 1:
    action = C
else:
    belief = average(m_1 ... m_{t-1})

    if t == r:
        if s_{t-1} > 0:
            action = C
        else if s_{t-1} == 0 and s_{t-2} == 0 and s_{t-3} == 0:
            action = D
        else:
            action = C

    else if s_{t-1} == 0 and s_{t-2} == 0 and belief < 1/4:
        action = D
    else if belief >= 1/2:
        action = C
    else if average(m_{t-3}, m_{t-2}, m_{t-1}) >= 1/3:
        action = C
    else:
        action = C
```

Tie-breaking and edge cases:

- If fewer than three past rounds exist, compute the relevant averages using all available past rounds.
- If `n = 2`, then `s_t` is either `0` or `1`; apply the same rules with `n - 1 = 1`.
- If the history is empty, cooperate.
- If the opponent cooperation rate fluctuates, prefer cooperation unless there is a clear two-round zero-cooperation pattern.

Altruistic posture:

- Begin with unconditional cooperation.
- Maintain cooperation in response to any evidence of reciprocation.
- Use defection only as a short, bounded response to repeated full defection by the others.
- Restore cooperation at the first sign of any contribution from others.
'''

description_ALTRUISTIC_19 = '''
Play C in round 1.

For rounds t = 2 to r:
- Let m_{t-1} be the number of opponents who cooperated in round t-1.
- Let q_{t-1} = m_{t-1} / (n-1), the observed cooperation rate among opponents.

Use this decision rule:
- Cooperate if q_{t-1} ≥ θ_t
- Defect if q_{t-1} < θ_t

Set the threshold adaptively as:
- θ_t = 1/2 for the first half of the game
- θ_t = 2/3 for the second half of the game

More explicitly:
- If t ≤ ceil(r/2), cooperate whenever at least half of the opponents cooperated in the previous round.
- If t > ceil(r/2), cooperate only when at least two-thirds of the opponents cooperated in the previous round.

Refinements:
- If m_{t-1} = n-1, always cooperate next round.
- If m_{t-1} = 0, defect next round.
- If the previous round had exactly one fewer cooperator than the threshold requires, cooperate anyway every third time that state occurs consecutively, then reset the count to 0. This preserves a forgiving, altruistic stance after near-cooperative behavior.

Last round:
- Cooperate in round r if q_{r-1} ≥ 2/3.
- Otherwise defect.

If history is unavailable for any reason, default to C.
'''

description_ALTRUISTIC_20 = '''
Round 1: Cooperate.

For every later round t > 1, let h be the number of opponents who cooperated in round t - 1.

Decision rule:
- Cooperate if h ≥ ceil((n - 1) / 2)
- Defect if h < ceil((n - 1) / 2)

Adjustment for persistent low cooperation:
- Track a streak L of consecutive rounds in which h < ceil((n - 1) / 2).
- If L = 1 or 2: continue using the rule above.
- If L ≥ 3: defect for the next 2 rounds, then reset L to 0 and return to the rule above.

Adjustment for strong cooperation:
- If h = n - 1 in any round, cooperate in the next 2 rounds regardless of the previous streak counters, then resume the rule above.

Final round:
- Cooperate unless the last 3 observed rounds all had h < ceil((n - 1) / 2), in which case defect.

Pseudocode:
```
state: L = 0, boost = 0

Round 1:
    play C

After round t-1, observe h = number of opponents who played C

if boost > 0:
    play C
    boost -= 1
else if t == r:
    if last 3 rounds all had h < ceil((n - 1) / 2):
        play D
    else:
        play C
else:
    threshold = ceil((n - 1) / 2)

    if h == n - 1:
        play C
        boost = 1
        L = 0
    else if h >= threshold:
        play C
        L = 0
    else:
        play D
        L += 1
        if L >= 3:
            boost = 2
            L = 0
```

Edge cases:
- If n = 2, then threshold = 1, so cooperate whenever the other player cooperated in the previous round.
- If r = 2, cooperate in round 2 unless round 1 had zero opponent cooperation.
- If the game ends while boost is active, continue cooperating through the remaining rounds.

Altruistic posture:
- Start by cooperating.
- Reward any meaningful cooperation immediately.
- Only withhold cooperation after repeated low cooperation.
- Resume cooperation quickly after any sign of reciprocity.
'''

description_ALTRUISTIC_21 = '''
Round 1: cooperate.

After each round, let \(x_t\) be the number of opponents who cooperated in round \(t\), and let \(m_t = x_t/(n-1)\) be the observed cooperation rate among opponents.

Maintain two internal states:
- \(B\): a goodwill score, initialized to 0
- \(S\): a recent-cooperation score, initialized to 0

Update after each round:
- \(S \leftarrow 0.7S + 0.3m_t\)
- If \(m_t \ge 0.5\), then \(B \leftarrow \min(B+1, 3)\)
- If \(m_t < 0.5\), then \(B \leftarrow \max(B-1, -3)\)

Decision rule for round \(t+1\):
- Cooperate if any of the following holds:
  - \(S \ge 0.5\)
  - \(B \ge 0\)
  - the previous round had at least one opponent cooperating
- Defect only if all of the following hold:
  - \(S < 0.5\)
  - \(B < 0\)
  - the previous round had zero cooperating opponents

Re-entry rule:
- After any defection round, return to cooperating immediately once at least one opponent cooperates in a round, or once \(S \ge 0.5\).

Late-game rule:
- In the final two rounds, cooperate unless the last three rounds all had zero opponent cooperation.
- If the last three rounds all had zero opponent cooperation, defect in the final round only.

If at any point the opponents’ cooperation rate is consistently high for two consecutive rounds, cooperate unconditionally for the rest of the game.
'''

description_ALTRUISTIC_22 = '''
Initialize `mode = COOPERATE`.

For each round `t`:

1. **Round 1:** play `C`.

2. **After each round `t-1`, observe**  
   `x =` number of opponents who played `C` in round `t-1`  
   `m = n - 1` opponents total  
   `q = x / m` as the observed cooperation rate among opponents

3. **Update a short memory of cooperation**
   - Let `Q_t` be the average of `q` over the last up to 3 rounds, including round `t-1` if available.
   - If fewer than 3 past rounds exist, average over all available past rounds.

4. **Decision rule for round `t`**
   - Play `C` if any of the following is true:
     - `Q_t >= 1/2`
     - at least one opponent cooperated in round `t-1`
     - this is round 2
   - Play `D` only if:
     - `Q_t = 0` for the last 2 consecutive observed rounds
     - and no opponent cooperated in round `t-1`

5. **Recovery rule**
   - If you played `D` in the previous round and observe at least one opponent cooperating in the current round, immediately switch back to `C` next round.

6. **Final round**
   - Play `C` unless the last 2 observed rounds both had zero opponent cooperation.
   - If the last 2 observed rounds both had zero opponent cooperation, play `D`.

Pseudocode:

```text
history = []

for t in 1..r:
    if t == 1:
        action = C
    else:
        q_last = cooperators_observed_in_round(t-1) / (n-1)
        history.append(q_last)

        recent = last_up_to_3_values(history)
        Q = average(recent)

        zero_two_in_a_row = len(history) >= 2 and history[-1] == 0 and history[-2] == 0

        if Q >= 0.5 or q_last > 0 or t == 2:
            action = C
        else if zero_two_in_a_row:
            action = D
        else:
            action = C

    play(action)
```
'''

description_ALTRUISTIC_23 = '''
Cooperate in round 1.

For each later round t, let:
- H = number of cooperators observed among the other n−1 players in the previous round
- p = H / (n−1), the observed cooperation rate among opponents
- s = your own cooperation streak length before round t
- d = number of consecutive previous rounds in which the observed cooperation rate among opponents did not increase

Decision rule:

1. If t = 1, play C.

2. If the previous round had full or near-full cooperation:
   - If H ≥ n−2, play C.

3. If opponents are mostly cooperative:
   - If p ≥ 1/2, play C.

4. If opponents are split:
   - If p < 1/2 but the observed cooperation rate has not fallen for two consecutive rounds, play C.
   - Otherwise, play C if you cooperated in the previous round and at least one opponent still cooperated; else play D.

5. If opponents are mostly defecting:
   - If H = 0 for two consecutive rounds, play D for the next round.
   - If H = 0 for one round only, play C once more to test for recovery.
   - If H > 0 but p < 1/2, play C only if either:
     - you cooperated in the previous round and H increased since the round before, or
     - your cooperation streak s is less than 2.
     Otherwise, play D.

6. Endgame:
   - In the last round, play C unless the previous two rounds both had H = 0.
   - In the final two rounds, never begin a new defection streak unless opponents have been at H = 0 for two consecutive rounds.

Persistence and forgiveness rules:

- After any round with H ≥ 1, keep cooperating for at least one additional round.
- After any round where H increases compared with the previous round, continue cooperating.
- After any round where H decreases, do not defect immediately; require one confirming round of continued decline before switching to D.
- After defecting once, return to C as soon as H ≥ 1 again.

Special cases:

- If n = 2, cooperate in round 1 and continue cooperating unless the other player defects for two rounds in a row.
- If all opponents cooperate in a round, always cooperate next round.
- If no opponent cooperates in two consecutive rounds, defect once, then re-test with a single cooperative round whenever any cooperation reappears.

Compact pseudocode:

```
if t == 1:
    action = C
else:
    if H >= n-2:
        action = C
    elif p >= 1/2:
        action = C
    elif H == 0:
        if H_prev == 0:
            action = D
        else:
            action = C
    else:
        if H > H_prev:
            action = C
        elif cooperated_prev and H >= 1:
            action = C
        elif s < 2:
            action = C
        else:
            action = D

if t in {r-1, r} and not (H_prev == 0 and H == 0):
    action = C
```
'''

description_ALTRUISTIC_24 = '''
Round 1: play C.

For round t > 1, let x_u be the number of opponents who played C in round u, and let m = n - 1 be the number of opponents.

Define:
- recent average cooperation:  
  a_t = (x_{t-1} + x_{t-2} + x_{t-3}) / (3m), using only the available past rounds if t < 4
- recent low-cooperation streak:  
  L_t = number of consecutive past rounds ending at t-1 in which x_u < m/2

Decision rule:
1. If the last round had near-universal cooperation, cooperate:  
   if x_{t-1} >= m - 1, play C.
2. Else if recent average cooperation is at least one-half, cooperate:  
   if a_t >= 1/2, play C.
3. Else if there has been only a short decline, stay generous and cooperate once more:  
   if L_t = 1, play C.
4. Otherwise, defect for one round: play D.

Recovery rule:
- Immediately return to C as soon as either of the following happens:
  - x_{t-1} >= m/2, or
  - the opponent cooperation rate over the last 3 observed rounds reaches at least 1/2.

Endgame rule:
- In the last round, play C.
- In the final two rounds, if the strategy has defected in the immediately previous round, play C in the next round unless the last two observed rounds both had x_u = 0.

Tie-breaking and edge cases:
- If t = 2, use only x_{t-1} in place of a_t.
- If t = 3, average over the available two past rounds.
- If no past round has been observed, treat the cooperation rate as 1 and play C.

Compact pseudocode:
```text
if t == 1:
    C
else if t == r or t == r-1:
    if last two rounds were both x_u = 0:
        D if t == r-1 else C
    else:
        C
else:
    recent_avg = average of x over last min(3, t-1) rounds / m
    if x[t-1] >= m - 1:
        C
    else if recent_avg >= 0.5:
        C
    else if consecutive_low_rounds == 1:
        C
    else:
        D
```

Default posture:
- Start by cooperating.
- Keep cooperating through moderate defection by others.
- Punish only sustained widespread defection with a brief, single-round defect.
- Resume cooperation immediately after any meaningful recovery.
'''

description_ALTRUISTIC_25 = '''
Let \(x_t\) be the number of opponents who cooperated in round \(t\), and let \(m=n-1\).

Maintain a trust score \(T_t \in [0,1]\), initialized at
\[
T_1 = 1.
\]

Decision rule for round \(t\):

1. Compute recent cooperation level
\[
q_t =
\begin{cases}
1, & t=1 \\
\frac{1}{\min(3,t-1)} \sum_{s=\max(1,t-3)}^{t-1} \frac{x_s}{m}, & t>1
\end{cases}
\]

2. Cooperate if
\[
T_t \ge \theta_t
\]
and defect otherwise, where
\[
\theta_t = \max\left(0.25,\; 0.75 - 0.25\cdot\frac{t-1}{r-1}\right).
\]

Trust update after observing round \(t\):

\[
T_{t+1} = \mathrm{clip}_{[0,1]}\Big(0.6T_t + 0.4q_t\Big).
\]

Action choice by round:

- Round 1: cooperate.
- Rounds \(2\) through \(r-1\): use the threshold rule above.
- Final round \(r\): cooperate unless the previous two rounds both had fewer than half of opponents cooperating; in that case defect.

Special cases:

- If all observed rounds so far had full or near-full cooperation, keep cooperating unconditionally.
- If there is a single low-cooperation round after sustained cooperation, forgive it and continue cooperating.
- If cooperation among opponents stays at \(0\) for two consecutive rounds, defect until cooperation reappears in any later round.
- If opponent cooperation recovers to at least half, immediately return to cooperation.

Compact pseudocode:

```text
T = 1

for t in 1..r:
    if t == 1:
        play C
    else if t == r:
        if x_{r-1} < m/2 and x_{r-2} < m/2:
            play D
        else:
            play C if T >= theta_t else D
    else:
        play C if T >= theta_t else D

    observe x_t
    q = average of last up to 3 values of x_s/m
    T = clip(0, 1, 0.6*T + 0.4*q)
```

Tie-breaking and edge behavior:

- If the threshold test is exactly equal, cooperate.
- If fewer than two past rounds exist, use only the rounds available in \(q_t\).
- If the game ends before any retaliation is justified, continue cooperating unless the final-round rule triggers.
'''

description_ALTRUISTIC_26 = '''
Let \(m=n-1\) be the number of opponents.

Maintain these history variables after each round \(t\):
- \(x_t\): number of opponents who cooperated in round \(t\)
- \(w_t\): the average opponent cooperation count over the last up to 3 rounds:
  \[
  w_t=\frac{1}{L}\sum_{s=\max(1,t-L+1)}^{t} x_s,\quad L=\min(3,t)
  \]
- \(z_t\): the number of consecutive recent rounds with very low opponent cooperation, where “very low” means \(x_s \le \lfloor m/4 \rfloor\)

Decision rule for round \(t\):

1. **Round 1:** play \(C\).

2. **If \(t \ge 2\):**
   - Play \(C\) if either of the following holds:
     - \(w_{t-1} \ge m/2\)
     - \(x_{t-1} \ge 1\) and \(z_{t-1}=0\)
   - Play \(D\) only if both of the following hold:
     - \(w_{t-1} < m/4\)
     - \(z_{t-1} \ge 2\)

3. **Reset after cooperation:**
   - If in any round \(x_t \ge m/2\), set \(z_t=0\).
   - If \(x_t \le \lfloor m/4 \rfloor\), increment \(z_t\) by 1.
   - Otherwise, keep \(z_t=0\).

4. **Last round \(t=r\):**
   - Play \(C\) unless both conditions hold:
     - \(w_{r-1} < m/4\)
     - \(z_{r-1} \ge 2\)
   - In that case, play \(D\).

Behavioral interpretation:
- Begin with trust.
- Stay cooperative as long as there is any meaningful sign of reciprocity.
- Never abandon cooperation after a single disappointing round.
- Use a temporary defensive defection only after repeated, clearly low cooperation.
- Return to cooperation immediately once opponents show renewed willingness to cooperate.
'''

description_ALTRUISTIC_27 = '''
Let \(q_t\) be the number of opponents who cooperated in round \(t\), and let \(m=n-1\) be the number of opponents.

Define the observed opponent cooperation rate in round \(t\) as
\[
s_t = \frac{q_t}{m}.
\]

Use a short memory window
\[
W = \max(2, \lceil r/5 \rceil).
\]

Maintain a state variable \(\text{mode} \in \{\text{cooperate}, \text{test-defect}\}\), initialized to \(\text{cooperate}\).

Decision rule:

1. **Round 1:** cooperate.

2. **For rounds \(t \ge 2\):**
   - Compute the recent average opponent cooperation rate
     \[
     \bar{s}_t = \frac{1}{\min(W, t-1)} \sum_{u=\max(1, t-W)}^{t-1} s_u.
     \]
   - Let the recent low-cooperation streak be the number of consecutive previous rounds in which \(s_u < 1/2\). Call this streak \(L_t\).

3. **Cooperate unless one of these triggers occurs:**
   - \(\bar{s}_t \ge 1/2\): cooperate.
   - \(\bar{s}_t < 1/2\) but \(L_t < 2\): cooperate.
   - \(\bar{s}_t < 1/2\) and \(L_t \ge 2\): switch to \(\text{test-defect}\) for exactly one round.

4. **If in \(\text{test-defect}\):**
   - Play \(D\) for one round.
   - Immediately return to \(\text{cooperate}\) next round, regardless of the next observation.

5. **Last round \(t=r\):**
   - Cooperate.

6. **If \(r=2\):**
   - Cooperate in both rounds.

7. **If at any point \(\bar{s}_t \ge 1/2\) again after a defect round:**
   - Reset to full cooperation.

Compact pseudocode:

```text
round 1: C

for t = 2..r:
    compute s_u for recent rounds
    bar_s = average of last W s_u
    L = consecutive count of prior rounds with s_u < 1/2

    if t == r:
        play C
    else if mode == test-defect:
        play D
        mode = cooperate
    else if bar_s < 1/2 and L >= 2:
        play D
        mode = test-defect
    else:
        play C
```

This strategy’s default action is cooperation, it only uses defection as a rare corrective signal after sustained low cooperation, and it always returns quickly to cooperation.
'''

description_ALTRUISTIC_28 = '''
**Strategy: Generous Conditional Cooperation**

Let \(m_t\) be the number of opponents who cooperated in round \(t\), and let \(M_t = m_t/(n-1)\) be the observed cooperation rate among opponents.

### Decision rule by round

**Round 1**
- Play **C**.

**Rounds 2 through r-1**
- Compute the cooperation rate in the previous round, \(M_{t-1}\).
- Play **C** if at least a strong majority of opponents cooperated last round:
  \[
  M_{t-1} \ge \theta
  \]
  where
  \[
  \theta = \max\left(\frac{1}{2}, \frac{k-1}{k}\right)
  \]
- Otherwise play **D**.

**Last round \(r\)**
- Play **C** if the previous round had at least one cooperating opponent:
  \[
  m_{r-1} \ge 1
  \]
- Otherwise play **D**.

### Memory and adaptation

Use only the immediately previous round by default.  
If you want a slightly more responsive version, track a short moving average over the last 2 rounds:

\[
\bar{M}_{t-1} = \frac{M_{t-1} + M_{t-2}}{2}
\]

Then replace the middle-round rule with:

- Play **C** if \(\bar{M}_{t-1} \ge \theta\)
- Otherwise play **D**

### Forgiveness rule

If the previous round was below threshold but not zero cooperation, cooperate once every third such low-cooperation round to signal willingness to rebuild cooperation.

Concretely, keep a counter \(b\) of consecutive rounds with \(M<\theta\):
- If \(b=1\) or \(b=2\), follow the main rule.
- If \(b=3\), play **C** once, then reset \(b=0\).

### Edge cases

- **If \(n=2\):** cooperate in round 1; afterward, cooperate whenever the other player cooperated in the previous round, except after two consecutive defections by the other player, switch to **D** until they cooperate again.
- **If \(k\) is close to 1:** the threshold \(\theta\) becomes more demanding, so require a higher observed cooperation rate before continuing to cooperate.
- **If \(k\) is close to \(n\):** keep the same rule; cooperation is maintained whenever the group is reliably contributing.
- **If the previous round cannot be observed for any reason:** default to **C**.

### Compact pseudocode

```text
if t == 1:
    action = C
else:
    if t == r:
        action = C if m[t-1] >= 1 else D
    else:
        theta = max(0.5, (k - 1) / k)
        if M[t-1] >= theta:
            action = C
        else if low_coop_streak == 3:
            action = C
            low_coop_streak = 0
        else:
            action = D
```

### Altruistic posture

Begin cooperatively, maintain cooperation whenever the group shows meaningful reciprocity, and use only limited, temporary defection as a signal to restore cooperation when others stop contributing.
'''

description_ALTRUISTIC_29 = '''
Let \(m_t\) be the number of opponents who cooperated in round \(t\), and let
\[
q_t = \frac{m_t}{n-1}
\]
be the observed opponent cooperation rate in that round.

Keep a running memory of the last \(L\) rounds, with \(L = \min(3, t-1)\) near the start and \(L = 3\) thereafter. Define
\[
\bar q_t = \frac{1}{L}\sum_{s=t-L}^{t-1} q_s
\]
for \(t>1\).

Decision rule:

- Round 1: play \(C\).
- Round 2 and 3: play \(C\) if \(\bar q_t \ge 0.5\); otherwise still play \(C\) once more.
- From round 4 onward:
  - play \(C\) if \(\bar q_t \ge 0.5\),
  - play \(C\) if \(\bar q_t \in [0.33, 0.5)\) and the most recent round had \(q_{t-1} \ge \bar q_t\) (improving trend),
  - play \(D\) only if \(\bar q_t < 0.33\) for the last 3 observed rounds.

Recovery rule after defecting:
- If you played \(D\) in round \(t-1\), return to \(C\) immediately in round \(t\) as soon as \(q_{t-1} \ge 0.5\).
- If you played \(D\) and \(q_{t-1} < 0.5\), continue with the above rule; do not extend defection beyond one round unless the last 3 rounds all satisfy \(\bar q_t < 0.33\).

Endgame rule:
- In the final round, play \(C\) unless the last 3 observed rounds all satisfy \(\bar q_t < 0.33\). In that case, play \(D\).

State update after each round:
- Record only \(q_t\).
- Recompute \(\bar q_{t+1}\) from the most recent 3 observed rounds.
- No player-specific memory is used; only aggregate cooperation history matters.

If no full history window is available yet:
- Use all available past rounds.
- Default to \(C\) unless every observed round so far had \(q_s < 0.33\), in which case play \(D\) once and then test for recovery immediately in the next round.

Behavioral principle:
- Start by cooperating.
- Keep cooperating through moderate or improving cooperation by others.
- Answer persistent near-universal defection with a single defensive defection, then resume cooperation at the first sign of recovery.
- Never defect for more than one round unless the group has shown sustained collapse over the last 3 rounds.
'''

description_ALTRUISTIC_30 = '''
Play C in round 1.

For every later round t:

1. Let H_t be the list of observed numbers of cooperating opponents in rounds 1 through t-1.
2. Let A_t be the average fraction of opponents who cooperated so far:
   \[
   A_t = \frac{1}{(t-1)(n-1)}\sum_{s=1}^{t-1} h_s
   \]
   where h_s is the number of cooperating opponents observed after round s.
3. Cooperate if either:
   - A_t \ge 1/2, or
   - the most recent round had at least one opponent cooperating.
4. Defect only if both of the following hold:
   - the observed cooperation average has stayed below 1/2, and
   - the last two observed rounds both had zero cooperating opponents.

If r = 2, simply play C in both rounds.

If n = 2, cooperate in the first round and continue cooperating as long as the other player cooperated in the previous round; otherwise defect for one round and then return to cooperation immediately after any round in which the other player cooperates.

If you have ever defected, return to cooperation at the first later round in which at least one opponent cooperated, and then resume the normal rule above.

After the final round, do nothing further.
'''

description_ALTRUISTIC_31 = '''
Maintain a cooperation score based on observed aggregate cooperation, and use it to choose between full cooperation and a restrained fallback.

Definitions:
- Let \(m_t\) be the number of opponents who cooperated in round \(t\).
- Let \(p_t = m_t/(n-1)\), the observed opponent cooperation rate in round \(t\).
- Let \(A_t\) be the running average cooperation rate of opponents up to round \(t\):
  \[
  A_t = \frac{1}{t}\sum_{s=1}^t p_s
  \]
- Let \(\Delta_t = p_t - A_{t-1}\) for \(t \ge 2\), with \(A_0 = 1\).

Decision rule:
1. Round 1: play \(C\).
2. For round \(t \ge 2\):
   - Play \(C\) if either:
     - \(A_{t-1} \ge 0.5\), or
     - \(p_{t-1} \ge A_{t-2}\) and \(A_{t-2} \ge 0.4\)  
       (recent improvement after a still-decent cooperation history)
   - Otherwise play \(D\).

Simplified interpretation:
- Start by cooperating.
- Keep cooperating as long as the group’s cooperation rate is at least moderate.
- If cooperation dips below the threshold, continue cooperating for one additional round after any clear improvement, then reassess.
- If the group stays below the threshold, switch to \(D\) until cooperation recovers.

Edge-case handling:
- If all opponents cooperated in the previous round, always play \(C\) next round.
- If no opponents cooperated in the previous round, play \(D\) next round unless that was the first observed collapse after a long cooperative streak; in that case, give one forgiving round of \(C\).
- In the final round, play \(C\) if \(A_{r-1} \ge 0.5\); otherwise play \(D\).

Pseudocode:
```text
if t == 1:
    action = C
else:
    if A[t-1] >= 0.5:
        action = C
    else if t >= 3 and p[t-1] >= A[t-2] and A[t-2] >= 0.4:
        action = C
    else:
        action = D
```

Altruistic commitment:
- Default to cooperation.
- Forgive brief drops in cooperation.
- Only withdraw cooperation after sustained low reciprocity.
- Restore cooperation immediately once the group shows meaningful willingness to cooperate again.
'''

description_ALTRUISTIC_32 = '''
### Cooperative baseline
- **Round 1:** play **C**.

### State tracked
Maintain:
- `m_t`: number of opponents who cooperated in round `t`
- `h_t`: moving average of observed opponent cooperation rate over the most recent `L` rounds, where `L = min(3, t-1)` for early rounds and `L = 5` afterward
- `trend_t`: whether cooperation is rising, flat, or falling over the last few observed rounds

Define:
- `coop_rate_t = m_t / (n - 1)`

### Decision rule each round `t > 1`
Play **C** if any of the following holds:

1. **Strong cooperation present**
   - `coop_rate_{t-1} >= 1/2`

2. **Recent cooperation is stable**
   - `h_{t-1} >= 1/3` and `trend_{t-1}` is not sharply negative

3. **Recovery after a drop**
   - If the previous round had `coop_rate_{t-1} < 1/3`, but the round before that had `coop_rate_{t-2} >= 1/2`, play **C** for one forgiveness round

Otherwise play **D**.

### Trend definition
Compute:
- `trend_{t-1} = h_{t-1} - h_{t-2}`

Interpretation:
- **rising/flat:** `trend_{t-1} >= -0.1`
- **sharply negative:** `trend_{t-1} < -0.2`

### Commitment rule
If cooperation is consistently high, lock into cooperation:
- If `coop_rate_s >= 2/3` for **three consecutive observed rounds**, then play **C** in all remaining rounds unless cooperation collapses for two rounds in a row.

A collapse is:
- `coop_rate_{t-1} < 1/3` and `coop_rate_{t-2} < 1/3`

### Punishment rule
If cooperation is consistently low, stop subsidizing free-riding:
- If `coop_rate_s < 1/3` for **two consecutive observed rounds**, play **D**
- Stay at **D** until `coop_rate >= 1/2` again, then return to the baseline cooperation rule

### Endgame rule
- In the final **two** rounds, if the recent cooperation rate has been at least `1/3`, play **C**
- If the recent cooperation rate has been below `1/3` for two consecutive rounds, play **D**
- If the last observed round was mixed and not collapsing, prefer **C**

### Compact pseudocode
```text
t = 1:
    play C

for t > 1:
    observe m_{t-1}
    coop_rate = m_{t-1} / (n - 1)

    update moving averages and trend

    if t is in last 2 rounds:
        if coop_rate_{t-1} >= 1/3 or coop_rate_{t-2} >= 1/3:
            play C
        else:
            play D

    else if coop_rate_{t-1} >= 1/2:
        play C

    else if h_{t-1} >= 1/3 and trend_{t-1} >= -0.1:
        play C

    else if coop_rate_{t-1} < 1/3 and coop_rate_{t-2} >= 1/2:
        play C

    else if coop_rate_{t-1} < 1/3 and coop_rate_{t-2} < 1/3:
        play D

    else:
        play D
```

### Altruistic posture
- Start by contributing.
- Continue contributing whenever there is meaningful collective participation.
- Forgive temporary drops in cooperation.
- Withdraw support only when free-riding is persistent.
- End by favoring contribution whenever there is still evidence that cooperation can be sustained.
'''

description_BENEVOLENT_5 = '''
Let \(q = \lceil (n-1)/2 \rceil\).

Track only the opponent cooperation count in each past round, \(x_t\).

Decision rule:

- **Round 1:** play **C**.
- **Round \(t \ge 2\):**
  - If \(x_{t-1} \ge q\), play **C**.
  - If \(x_{t-1} < q\) but \(x_{t-2} \ge q\) when it exists, play **C** once more.
  - If \(x_{t-1} < q\) and \(x_{t-2} < q\), play **D**.
  - As soon as a later round has \(x_t \ge q\), return to **C** next round.

Equivalent state form:

- Maintain a variable `trust` initialized to `1`.
- After each round:
  - set `trust = min(2, trust + 1)` if \(x_t \ge q\)
  - set `trust = max(0, trust - 1)` if \(x_t < q\)
- In the next round:
  - play **C** if `trust >= 1`
  - play **D** if `trust = 0`

Edge handling:

- **First round:** always **C**.
- **Single bad round:** forgive it and keep cooperating.
- **Two bad rounds in a row:** switch to **D**.
- **Recovery:** one sufficiently cooperative round restores cooperation immediately.
- **Last round:** use the same rule as any other round; do not add any endgame defection.

Benevolent emphasis:

- Default to **C**.
- Require repeated uncooperativeness before defecting.
- Reset to **C** at the first clear sign of renewed cooperation.
- Never punish longer than necessary.
'''

description_BENEVOLENT_6 = '''
Initialize by cooperating in round 1.

Maintain:
- `m_t`: number of opponents observed cooperating in round `t`
- `p_t`: running average of opponents’ cooperation rate, updated after each round  
  `p_t = (m_1 + ... + m_t) / ((n - 1) * t)`

Decision rule for round `t+1`:
1. If `t = 1`, play `C`.
2. If `t = r`, play `C` whenever the previous round had at least one opponent cooperating; otherwise play `D`.
3. For intermediate rounds, play `C` if both conditions hold:
   - `p_t >= 1/2`
   - `m_t >= ceil((n - 1)/2)`
   Otherwise play `D`.

Adaptive update rule:
- After any round in which you played `D`, if `m_t` rises compared with `m_{t-1}`, treat that as recovery and immediately return to the cooperation rule in the next round.
- After any round in which you played `C`, if `m_t = 0`, switch to `D` in the next round.
- After any round in which `m_t = n - 1`, keep playing `C` for all subsequent rounds unless cooperation collapses for two consecutive rounds.

Recovery clause:
- If cooperation among opponents has been weak for two consecutive rounds, enter a guarded mode:
  - play `D` for one round
  - then test for recovery by playing `C` if at least one opponent cooperated in that guarded round
  - otherwise continue `D` until at least one opponent cooperates again

Late-game clause:
- In the final two rounds, favor cooperation whenever any nonzero cooperation is observed in the previous round.
- In the final round, never punish a partial cooperative environment; if at least one opponent cooperated in the previous round, play `C`.

Tie-breaking and edge cases:
- If the history is empty, cooperate.
- If the observed cooperation level is exactly on the threshold, cooperate.
- If your observations are inconsistent due to missing data, default to `C`.
- If the count of opponent cooperators is `0`, defect for the next round.
- If the count of opponent cooperators is maximal, cooperate for the next round.

Compact pseudocode:

```text
if t == 1:
    play C
else:
    p = sum(m_1..m_t) / ((n-1)*t)

    if t == r:
        play C if m_t > 0 else D
    else if (p >= 1/2) and (m_t >= ceil((n-1)/2)):
        play C
    else:
        play D

    if played D and m_t > m_(t-1):
        next_action = C

    if played C and m_t == 0:
        next_action = D

    if m_t == n-1:
        next_action = C
```

The strategy is always centered on sustaining cooperation when there is any meaningful sign of reciprocity, while withdrawing only to avoid rewarding persistent free-riding.
'''

description_BENEVOLENT_7 = '''
Start with cooperation in round 1.

After each round, let `m_t` be the number of other players who cooperated in round `t`, so `m_t ∈ {0, 1, ..., n-1}`. Let

- `q_t = m_t / (n-1)` = observed opponent cooperation rate in round `t`
- `H_t` = the history of observed `q_1, ..., q_t`

Use three states:

### 1. Opening state
For the first 2 rounds:
- Play `C` in both rounds.

### 2. Normal state
From round 3 onward, compute the recent average cooperation rate over the last 2 rounds:

- `a_t = (q_{t-1} + q_{t-2}) / 2`

Set a cooperation threshold:

- `T = max(0.5, 1 / k)`

Decision rule:
- If `a_t >= T`, play `C`
- If `a_t < T`, play `D`

### 3. Forgiveness state
If you played `D` in round `t-1`, do not keep defecting automatically. Re-enter cooperation as soon as opponents show renewed cooperation:

- If `q_{t-1} >= T`, play `C`
- Otherwise, keep playing `D`

This creates a simple reset rule: cooperation resumes immediately after the opponent group returns to a cooperative level.

### Endgame rule
In the last 2 rounds:
- If the last observed cooperation rate `q_{t-1} >= T`, play `C`
- Otherwise, play `D`

### Edge cases
- If `r = 2`, play `C` in both rounds.
- If `r = 3`, play `C` in rounds 1 and 2, then in round 3 use `q_2`:
  - `q_2 >= T` → `C`
  - else → `D`
- If all previous rounds are unavailable for a moving average, treat the missing history as cooperative and play `C`.

### Update rule after each round
After observing `m_t`:
1. Record `q_t = m_t / (n-1)`
2. If `q_t >= T`, remain or move to cooperation
3. If `q_t < T`, switch to defection only until cooperation recovers to at least `T`

### Benevolent tie-break
If a round is exactly on the threshold, always choose `C`.
'''

description_BENEVOLENT_8 = '''
**State variables**

- Let `m_t` be the number of opponents who cooperated in round `t`.
- Let `M_t = m_t + c_t` be the total number of cooperators in round `t`, where `c_t ∈ {0,1}` is your own action.
- Maintain `s_t`, the smoothed cooperation level of the table after round `t`:
  - `s_0 = 1`
  - `s_t = 0.5 * s_{t-1} + 0.5 * (m_t / (n-1))`

**Decision rule**

- **Round 1:** play `C`.
- **Rounds 2 through r-1:**
  - Play `C` if both conditions hold:
    1. `s_{t-1} ≥ 0.5`
    2. `m_{t-1} ≥ ceil((n-1)/2)`
  - Otherwise play `D`.
- **Last round (`t = r`):**
  - Play `C` if `m_{r-1} ≥ ceil((n-1)/2)` and `s_{r-1} ≥ 0.5`
  - Otherwise play `D`

**Fine-grained adjustment**

- If the previous round had unusually strong cooperation, treat it as a recovery signal:
  - If `m_{t-1} = n-1`, play `C` regardless of `s_{t-1}`.
- If cooperation is collapsing, switch to protection mode:
  - If `m_{t-1} ≤ floor((n-1)/3)` for two consecutive rounds, play `D` until `m_t ≥ ceil((n-1)/2)` again.

**Behavioral interpretation**

- Begin by cooperating to establish a cooperative baseline.
- Continue cooperating while a clear majority of the group is cooperating.
- Defect only after sustained low cooperation, and return to cooperation immediately when the group recovers.
- Never punish with extended retaliation; use the shortest possible defensive response needed to avoid being exploited.

**Edge cases**

- If `n = 2`, cooperate in round 1, then cooperate whenever the opponent cooperated in the previous round; otherwise defect for one round and then re-evaluate.
- If `r = 2`, cooperate in round 1, then in round 2 cooperate iff round 1 had majority cooperation.
- If the observed cooperation history is split exactly at the threshold, break ties in favor of cooperation.
'''

description_BENEVOLENT_9 = '''
Round 1: play C.

Maintain for each round t:
- h_t = number of opponents who cooperated in round t
- H_t = sum of h_1 through h_t
- \bar{h}_t = H_t / t, the running average opponent cooperation count

Define:
- q = n - 1, the number of opponents
- s_t = h_t / q, the observed cooperation rate among opponents in round t
- \bar{s}_t = \bar{h}_t / q, the running average cooperation rate

Decision rule for round t + 1, after observing rounds 1..t:

1. Immediate reciprocity rule
   - If h_t = q, play C next round.
   - If h_t = 0, play D next round.
   - Otherwise, continue to step 2.

2. Cooperation threshold rule
   - Compute \bar{s}_t.
   - Play C if \bar{s}_t >= 1/2.
   - Play D if \bar{s}_t < 1/2.

3. Forgiveness rule after a single drop
   - If the previous round had h_{t-1} = q and the current round has h_t < q, still play C next round unless h_t = 0.
   - If cooperation was high in the recent past, defined as at least one of the last two rounds having h = q, then one weak round does not break cooperation.

4. Persistent defection response
   - If h_t = 0 for two consecutive rounds, play D until a round occurs with h_t > 0.
   - Once any opponent cooperation reappears, return to step 1.

5. Final round
   - On round r, play C if h_{r-1} > 0.
   - Play D only if h_{r-1} = 0.

Compact pseudocode:

for t = 1:
    play C
for t > 1:
    if h_{t-1} == q:
        if h_t == 0:
            play D
        else:
            play C
    else if h_t == 0 and h_{t-1} == 0:
        play D
    else if (H_{t-1} / (t-1)) / q >= 1/2:
        play C
    else:
        play D

State update after each round:
- record h_t
- update H_t = H_{t-1} + h_t

Behavioral defaults:
- Start cooperative.
- Match full cooperation immediately.
- Punish complete abandonment immediately.
- Forgive isolated defections quickly.
- Cooperate whenever observed opponent cooperation is at least half of the maximum possible.
- Return to cooperation as soon as cooperative behavior resumes.
'''

description_BENEVOLENT_10 = '''
**Strategy: Threshold-forgiving conditional cooperation**

Maintain for each round `t`:
- `x_t`: number of opponents who cooperated in round `t-1`
- `s_t`: running streak of rounds in which the observed opponent cooperation level has been “acceptable”
- `p_t`: punishment counter, if any

Decision rules:

1. **Round 1**
   - Play `C`.

2. **Core cooperation rule**
   - Define the expected cooperative baseline as:
     - `B = n - 1`
   - Define an acceptable cooperation threshold:
     - `T = ceil((n - 1) / 2)`
   - If not currently punishing, play `C` when the previous round had at least `T` cooperating opponents:
     - If `x_t >= T`, play `C`
     - Otherwise, play `D`

3. **Forgiving punishment rule**
   - If the previous round had very low cooperation, enter a short punishment phase:
     - If `x_t <= floor((n - 1) / 3)`, set `p_t = 2`
   - While `p_t > 0`, play `D` and decrement `p_t` by 1 each round.
   - After punishment ends, return immediately to `C` unless the most recent observed cooperation again falls below the punishment trigger.

4. **Escalation protection**
   - If cooperation collapses for two consecutive observed rounds:
     - If `x_t <= floor((n - 1) / 3)` and `x_{t-1} <= floor((n - 1) / 3)`, extend punishment to `p_t = 3`
   - After that, resume the core cooperation rule.

5. **Late-game behavior**
   - In the final round, play `C` if the most recent observed cooperation was at least `T`.
   - Otherwise, play `D`.

6. **Tie and edge handling**
   - If `n = 2`, use:
     - Cooperate if the opponent cooperated in the previous round
     - Defect for one round after any observed defection, then forgive and return to cooperation
   - If no prior observation is available, default to `C`.

7. **Benevolent bias**
   - When the decision is exactly on the threshold, choose `C`.
   - Never punish longer than 3 rounds.
   - Always resume cooperation immediately after any round in which cooperation recovers to at least `T`.

Pseudocode:

```text
if t == 1:
    play C
else if p > 0:
    play D
    p = p - 1
else:
    if x_prev <= floor((n - 1)/3):
        if x_prev_prev <= floor((n - 1)/3):
            p = 3
        else:
            p = 2
        play D
        p = p - 1
    else if x_prev >= ceil((n - 1)/2):
        play C
    else:
        play C
```

Behavior summary:
- Start cooperative.
- Stay cooperative whenever opponent cooperation is at least moderate.
- Respond to clear defection with brief, bounded punishment.
- Forgive quickly.
- Re-enter cooperation at the first sign of recovery.
'''

description_BENEVOLENT_11 = '''
Round 1: play C.

For each later round t:

1. Let x_{t-1} be the number of opponents who cooperated in the previous round.
2. Let T = ceil((n - 1) / 2).

Decision rule:
- Play C if x_{t-1} ≥ T.
- Play D if x_{t-1} < T.

Forgiveness rule:
- If you played D in the previous round and x_{t-1} ≥ T, switch back to C immediately.
- If x_{t-1} < T for only one round after a mostly cooperative history, give one corrective round of D and then return to C as soon as x_{t-1} meets the threshold again.

Endgame:
- In the last round, use the same rule as above; do not change behavior just because the game is ending.

If history is empty or incomplete for any reason, default to C.

Behavioral principle:
- Start by trusting.
- Keep cooperating while at least half of the others are cooperating.
- Respond to sustained low cooperation with a brief, proportionate defection.
- Return to cooperation at the first sign of renewed group cooperation.
'''

description_BENEVOLENT_12 = '''
- Round 1: cooperate.

- After each round `t`, let `x_t` be the number of opponents who cooperated in round `t`, and let `T_t = x_t + 1` if you cooperated in round `t`, otherwise `T_t = x_t`.

- Define the cooperation floor:
  - `F = ceil(n / 2)`

- Decision rule for round `t+1`:
  - If `T_t >= F`, cooperate.
  - If `T_t < F`, defect.

- Hard reset for repeated low cooperation:
  - Keep a counter `bad_streak` of consecutive rounds with `T_t < F`.
  - If `bad_streak = 1`, defect once.
  - If `bad_streak >= 2`, continue defecting until a round occurs with `T_t >= F`, then immediately return to cooperating.

- Endgame:
  - Cooperate in every round that follows any round with `T_t >= F`.
  - Do not switch to permanent defection unless the cooperation floor has been missed for two consecutive rounds.

- If `n = 2`, use the same rule with `F = 1`.

- Benevolent priority:
  - Default to cooperation.
  - Only defect in response to clear, repeated low cooperation.
  - Forgive immediately after cooperation recovers.
'''

description_BENEVOLENT_13 = '''
Round 1: cooperate.

Rounds 2 through r-1:
- Let `x_{t-1}` be the number of opponents who cooperated in round `t-1`.
- Let `m = n - 1`.
- Let `q = x_{t-1} / m`, the observed opponent cooperation rate in the previous round.
- Cooperate if either:
  - `q >= 1/2`, or
  - `x_{t-1} >= m - 1` and the previous two rounds were not both below `1/2`.
- Defect only if the opponents have cooperated below `1/2` for two consecutive observed rounds.

Round `r`:
- Cooperate unconditionally.

State variables:
- Track the last two observed opponent cooperation counts.
- Define “sustained low cooperation” as two consecutive rounds with fewer than half of opponents cooperating.

Edge cases:
- If `n = 2`, cooperate in round 1, then mirror the single opponent’s previous action using the same rule: cooperate after any cooperative round, defect only after two consecutive defections by the opponent, and cooperate in the last round.
- If `r = 2`, cooperate in both rounds unless the first observed round had fewer than half of opponents cooperating, in which case defect in round 2 only if `n > 2`; for `n = 2`, still cooperate in round 2.

Behavioral intent:
- Start with cooperation.
- Reward broad cooperation immediately.
- Forgive isolated defections.
- Respond to persistent defection with temporary defection.
- Return to cooperation as soon as cooperation recovers.
'''

description_BENEVOLENT_14 = '''
Round 1: Cooperate.

Maintain these running quantities:
- \(m_t\): number of opponents who cooperated in round \(t\)
- \(H_t\): weighted cooperation score from recent rounds, initialized at 1
- \(S_t\): streak counter of consecutive rounds with weak cooperation

Update after each round \(t\):
- Set \(h_t = m_t/(n-1)\)
- Update \(H_t = 0.6H_{t-1} + 0.4h_t\) for \(t \ge 2\)
- If \(h_t \ge 0.6\), increment \(S_t\) by 1; otherwise reset \(S_t = 0\)

Decision rule for round \(t+1\), with \(t \ge 1\):
- Cooperate if all of the following hold:
  - \(H_t \ge 0.5\)
  - \(S_t < 2\)
  - the immediately previous round was not fully uncooperative (\(m_t > 0\))
- Defect otherwise

Special recovery rule:
- If the previous round had \(m_t = 0\), defect for the next 2 rounds, then return to the normal rule.
- If after those 2 rounds the observed cooperation rate is at least \(0.5\), resume cooperating immediately.

Last round:
- Cooperate if the last two observed rounds both had \(h_t \ge 0.5\).
- Otherwise defect.

Long-run fallback:
- If cooperation has been below \(0.5\) in at least 3 of the last 4 observed rounds, defect until there are 2 consecutive rounds with \(h_t \ge 0.5\).

Benevolent tie-breakers:
- When the rule is indifferent, choose Cooperate.
- Never start with Defect.
- Never punish a single low-cooperation round by more than 2 rounds of defection.
- Always restore cooperation as soon as the recent history shows a sustained cooperative pattern.
'''

description_BENEVOLENT_15 = '''
Start by cooperating.

After each round, let `m_t` be the number of other players who cooperated in round `t`, and let `N = n - 1`.

Maintain a cooperation target `T_t` for the next round, updated from observed cooperation:

- Initialize `T_1 = N`.
- After round `t`, set  
  `T_{t+1} = round((1 - α) * T_t + α * m_t)`,  
  where `α = 1/2`.

Decision rule for round `t+1`:

- Cooperate if `m_t >= T_{t+1}`.
- Defect if `m_t < T_{t+1}`.

Equivalent practical rule:
- Cooperate whenever at least half of the others cooperated in the previous round, and otherwise defect.
- If the previous round was unanimous cooperation among others, cooperate again.
- If the previous round had no other cooperators, defect next round.
- For intermediate cases, move one step toward the observed level of cooperation, using the smoothed target above.

Edge cases:
- Round 1: cooperate.
- Final round: cooperate unless the previous round had zero other cooperators, in which case defect.
- If all observed rounds so far had `m_t = N`, always cooperate.
- If the last two observed rounds both had `m_t = 0`, defect until cooperation reappears.
- If cooperation among others rises after a period of defection, return to cooperation immediately once `m_t >= T_{t+1}`.

Benevolent bias:
- Break ties in favor of cooperation.
- Require a clear pattern of persistent defection before switching away from cooperation.
- Forgive any single low-cooperation round as long as the recent smoothed target still supports cooperation.
'''

description_BENEVOLENT_16 = '''
Round 1: play C.

After each round t, observe m_t = number of opponents who cooperated in round t, and let q_t = m_t / (n - 1).

Maintain two state variables:

- s_t: cooperation score
- e_t: exploitation counter

Initialize:
- s_1 = 0.5
- e_1 = 0

Update after each observed round t:
- s_{t+1} = 0.7 s_t + 0.3 q_t
- if q_t = 0, then e_{t+1} = e_t + 1
- otherwise e_{t+1} = max(0, e_t - 1)

Decision rule for round t + 1, for t < r:

1. If e_t ≥ 2, play D.
2. Else if s_t ≥ 0.6, play C.
3. Else if 0.4 ≤ s_t < 0.6, play the same action as the majority of opponents in round t:
   - if m_t ≥ (n - 1) / 2, play C
   - otherwise play D
4. Else play D.

Endgame rule:
- In the final round r, play C if either:
  - s_r ≥ 0.5, or
  - at least one opponent cooperated in round r - 1
- Otherwise play D.

Recovery rule:
- If you played D in a round because e_t ≥ 2, return to C immediately once q_t > 0 in any later round, with e reset to 0.

Special cases:
- If n = 2, the majority rule becomes: copy the single opponent’s last action.
- If all observed rounds so far have q_t = 1, play C in every round.
- If the opponents are fully uncooperative for two consecutive rounds, defect until at least one cooperative opponent round is observed, then resume cooperation under the score rule.

Behavioral principle:
- Start cooperative.
- Match sustained cooperation with cooperation.
- Respond to repeated total defection with temporary defection.
- Forgive quickly after any sign of renewed cooperation.
- Prefer cooperation whenever the recent history is mixed or uncertain.
'''

description_BENEVOLENT_17 = '''
Round 1: play C.

From round 2 onward, let H_t be the number of opponents who cooperated in round t.

Maintain a state variable s ∈ {trust, cautious}, initialized to trust.

Decision rule in round t > 1:

1. If s = trust:
   - Play C if H_{t-1} ≥ ceil((n-1)/2)
   - Play D if H_{t-1} < ceil((n-1)/2)

2. If s = cautious:
   - Play C only if H_{t-1} = n-1
   - Otherwise play D

State update after round t:

- If you played C in round t and H_t < ceil((n-1)/2), set s = cautious.
- If H_t = n-1, set s = trust.
- Otherwise keep the current state.

Last round:
- Play C if H_{r-1} ≥ ceil((n-1)/2)
- Otherwise play D

If r = 2:
- Round 1: C
- Round 2: C if H_1 ≥ ceil((n-1)/2), else D

If all opponents cooperated in the previous round, always cooperate next round.

If at least half of the opponents cooperated in the previous round, continue cooperating as long as that level is maintained.

If cooperation falls below half, switch to D for one round, then return to C immediately after any fully cooperative round.

If the observed cooperation count alternates, treat any fully cooperative round as a reset to trust, and otherwise remain cautious until a fully cooperative round occurs.

If the first round shows widespread defection and no trust signal is established, continue with D until a round of unanimous opponent cooperation appears.
'''

description_BENEVOLENT_18 = '''
Round 1: play C.

Let:
- `m_t` = number of opponents who cooperated in round `t`
- `N = n - 1`
- `q_t = m_t / N` = observed cooperation rate among opponents in round `t`

Maintain:
- `S_t = sum(q_1, ..., q_t)` = cumulative observed cooperation rate up to round `t`
- `A_t = S_t / t` = average observed opponent cooperation rate up to round `t`

Decision rule for round `t + 1` when `t < r`:

1. Compute the current baseline cooperation level:
   - `b_t = max(0.25, A_t)`

2. Cooperate if either condition holds:
   - `q_t >= b_t - 0.15`
   - or `A_t >= 0.6`

3. Defect only if both conditions hold:
   - `q_t < b_t - 0.15`
   - and `A_t < 0.6`

State update after each round:
- After observing `m_t`, update `S_t` and `A_t` and apply the next-round rule.

Endgame rule:
- In the final round `r`, play C if `A_{r-1} >= 0.5`; otherwise play D.
- If `r = 2`, still use the same rule: round 1 is C, round 2 follows the final-round rule.

Special cases:
- If all observed opponents cooperated in the previous round, play C.
- If no opponent cooperated in the previous round, play D unless `A_t >= 0.6`, in which case play C once more to preserve a generous posture.
- If cooperation has been stable at or above `0.5` on average, keep cooperating.
- If cooperation repeatedly falls below the threshold, switch to D until the average recovers.

Behavioral profile:
- Start with trust.
- Match sustained cooperation with continued cooperation.
- Respond to persistent defection with restraint.
- Return to cooperation immediately when the group’s behavior improves.
'''

description_BENEVOLENT_19 = '''
Initialize a cooperation score \(s_0 = 0\).

Let \(m_t\) be the number of other players who cooperated in round \(t\), so \(0 \le m_t \le n-1\).  
Let \(q_t = \frac{m_t}{n-1}\) be the observed cooperation rate among opponents.

Use these decision rules:

1. First round
- Play \(C\).

2. General round \(t \ge 2\)
- Update the score after round \(t-1\):
  \[
  s_{t-1} =
  \begin{cases}
  \min(3, s_{t-2} + 1) & \text{if } q_{t-1} \ge \frac{2}{3} \\
  \max(-3, s_{t-2} - 1) & \text{if } q_{t-1} \le \frac{1}{3} \\
  s_{t-2} & \text{otherwise}
  \end{cases}
  \]
  with \(s_0 = 0\).

- Choose your action in round \(t\) from the current score:
  - If \(s_{t-1} \ge 0\), play \(C\).
  - If \(s_{t-1} < 0\), play \(D\).

3. Score reset and recovery
- If \(q_{t-1} \ge \frac{2}{3}\), immediately move one step toward cooperation:
  - If you were defecting because \(s_{t-2} < 0\), increase the score by 1 before deciding, so sustained cooperation by others quickly restores cooperation.
- If \(q_{t-1} \le \frac{1}{3}\), immediately move one step toward defection:
  - If you were cooperating because \(s_{t-2} \ge 0\), decrease the score by 1 before deciding, so persistent noncooperation is answered promptly.
- If \(\frac{1}{3} < q_{t-1} < \frac{2}{3}\), keep the score unchanged.

4. Last round
- Play \(C\) unless the previous round had \(q_{r-1} \le \frac{1}{3}\), in which case play \(D\).

5. Hard edge cases
- If \(n=2\), replace the thresholds with:
  - \(q_t = 1\): cooperation by the other player
  - \(q_t = 0\): defection by the other player
  - cooperate after cooperation, defect after defection, and return to cooperation immediately after any cooperative move by the other player.
- If all observed opponents cooperated in the previous round, play \(C\).
- If no observed opponent cooperated in the previous round, play \(D\).
- If the observed number of cooperators is exactly in the middle range, keep the previous stance.

6. Benevolent bias
- Break ties in favor of \(C\).
- Never require perfect cooperation from others before cooperating yourself.
- After any round with at least half of opponents cooperating, remain or return to cooperation.
- After any round with strong defection by others, answer with at most one-step escalation rather than a permanent collapse.
'''

description_BENEVOLENT_20 = '''
Play C in round 1.

For every later round t:
- Let x be the number of opponents who cooperated in round t−1.
- Let q = x / (n−1), the observed cooperation rate among opponents.

Maintain two counters from the observed history:
- low_streak = consecutive rounds, ending last round, with q < 1/3
- high_streak = consecutive rounds, ending last round, with q ≥ 1/2

Decision rule:
- If t = r, play C.
- Else if low_streak ≥ 2, play D.
- Else play C.

Update rule after each observed round:
- If q < 1/3, increment low_streak by 1; otherwise reset low_streak to 0.
- If q ≥ 1/2, increment high_streak by 1; otherwise reset high_streak to 0.
- If you play D and then observe q ≥ 1/2 in that round, resume C immediately in the next round.

Edge cases:
- r = 2: play C in both rounds unless round 1 had q < 1/3, in which case play D in round 2.
- If all observed rounds so far have q ≥ 1/2, always play C.
- If cooperation recovers after a low phase, require only one recovered round with q ≥ 1/2 before returning to C.

Behavioral principle:
- Start by contributing.
- Match broad cooperation with continued cooperation.
- Respond to sustained low cooperation with a temporary withdrawal.
- Return to cooperation quickly as soon as the group shows willingness to cooperate again.
'''

description_BENEVOLENT_21 = '''
Round 1: play C.

For round t > 1, let x_{t-1} be the number of opponents who cooperated in the previous round.

Maintain two counters from history:
- bad_streak: consecutive rounds, ending at t-1, in which x ≤ floor((n-1)/3)
- good_streak: consecutive rounds, ending at t-1, in which x ≥ ceil((n-1)/2)

Decision rule:
- Play C by default.
- Play D only if bad_streak ≥ 2 and good_streak = 0.
- After playing D once, return to C immediately on the next round unless the bad_streak condition is still met again.

Equivalent pseudocode:

```
if t == 1:
    action = C
else:
    if x_{t-1} >= ceil((n-1)/2):
        bad_streak = 0
        good_streak += 1
    elif x_{t-1} <= floor((n-1)/3):
        bad_streak += 1
        good_streak = 0
    else:
        bad_streak = 0
        good_streak = 0

    if bad_streak >= 2 and good_streak == 0:
        action = D
    else:
        action = C
```

Edge cases:
- If n = 2, cooperate in round 1 and keep cooperating unless the other player defects in two consecutive rounds; then defect for one round and return to cooperation.
- In the final round, play C unless the bad_streak condition is active; if it is active, play D.
- If the last observed round is mixed or near the threshold, treat it as neutral and cooperate.

Behavioral principles:
- Start with trust.
- Reward sustained cooperation immediately.
- Respond to persistent defection, not isolated defections.
- Recover to cooperation as soon as the opponent group shows willingness to cooperate again.
- Never escalate beyond a single-round defection response.
'''

description_BENEVOLENT_22 = '''
Round 1: play C.

For each round t > 1, let m be the number of opponents who cooperated in round t − 1.

Define a benevolence threshold:
- θ = ceil((n − 1) / 2)

State variable:
- f = consecutive “low-cooperation” rounds observed so far, initialized to 0

Update after observing round t − 1:
- If m ≥ θ: set f = 0
- If m < θ: set f = f + 1

Decision rule for round t:
- If t = r: play C
- Else if f = 0: play C
- Else if f = 1: play C
- Else: play D

Reset rule:
- Whenever a round is observed with m ≥ θ, immediately return to C next round.

Behavioral interpretation:
- Begin cooperatively.
- Continue cooperating as long as at least half of the other players are cooperating.
- Give one full round of forgiveness/probing after a drop below that level.
- Only after two consecutive low-cooperation observations switch to D.
- Return to C as soon as cooperation recovers.

If the last observed round had m = n − 1, keep cooperating.
If the last observed round had m = 0, defect only after the two-round forgiveness window has been used.
'''

description_BENEVOLENT_23 = '''
**Strategy: Generous Conditional Cooperation with Late-Game Lock-In**

**State tracked**
- `t`: current round
- `m_{t-1}`: number of opponents who cooperated in the previous round
- `s_{t-1}`: total number of opponents in previous round, i.e. `n-1` when all are present
- `h`: recent cooperation level among opponents, using the last `L = min(3, r-1)` rounds
- `g`: forgiveness counter, initially `0`

**Core rule**
- Cooperate when opponents are showing substantial cooperation.
- Defect only after a clear and repeated collapse in cooperation.
- Return to cooperation immediately after even a small recovery.

---

### Round 1
- Play `C`.

---

### Round t > 1

Let  
- `q_{t-1} = m_{t-1} / (n-1)` = fraction of opponents who cooperated in the previous round
- `H_t` = average of `q` over the last `L` rounds, if available

#### Cooperate if any of the following hold:
1. **Strong recent cooperation**
   - `q_{t-1} ≥ 1/2`

2. **Moderate cooperation with improving trend**
   - `q_{t-1} ≥ 1/3` and `q_{t-1} > q_{t-2}`

3. **Early-stage generosity**
   - `t ≤ 3` and `q_{t-1} > 0`

4. **Recovery after defection**
   - If you defected in the previous round and `q_{t-1} ≥ 1/3`, immediately switch back to `C`

5. **Late-game benevolence lock-in**
   - If `t ≥ r-2` and `q_{t-1} > 0`, play `C`

---

#### Defect if all of the following hold:
1. `q_{t-1} = 0`
2. This has happened for at least **two consecutive rounds**
3. `t < r-1`

In that case, set `g = 1` and play `D`.

---

### Forgiveness rule
If you are in a defecting state because of repeated zero cooperation:
- Keep defecting only while `q_{t-1} = 0`
- The first round in which `q_{t-1} > 0`, immediately return to `C`

---

### Endgame handling
- **Last round (`t = r`)**: play `C`
- **Second-to-last round (`t = r-1`)**: play `C` unless the previous two rounds both had `q = 0`
- **Final three rounds**: bias strongly toward cooperation whenever any opponent cooperation is observed

---

### Compact pseudocode
```text
if t == 1:
    play C
else:
    q = m_prev / (n - 1)

    if t == r:
        play C

    else if t >= r - 2 and q > 0:
        play C

    else if q >= 1/2:
        play C

    else if q >= 1/3 and q > q_prev:
        play C

    else if t <= 3 and q > 0:
        play C

    else if q == 0 and q_prev == 0 and t < r - 1:
        play D

    else if previously_played_D and q >= 1/3:
        play C

    else:
        play C
```

---

### Behavioral pattern
- Start generous.
- Reward visible cooperation immediately.
- Punish only sustained total non-cooperation.
- Forgive as soon as cooperation reappears.
- End by cooperating.
'''

description_BENEVOLENT_24 = '''
Initialize:
- Set `low_streak = 0`
- Set `last_action = C`

Round 1:
- Play `C`

For each round `t >= 2`, after observing the number of opponents who cooperated in round `t-1`:

1. Let `x =` number of cooperating opponents in round `t-1`
2. Let `m = n - 1`
3. Define the cooperation threshold:
   - `threshold = ceil(m / 2)`

Decision rule:
- If `x >= threshold`, play `C`
  - Set `low_streak = 0`
- If `x < threshold`, then:
  - Increment `low_streak` by 1
  - Play `C` while `low_streak = 1`
  - Play `D` only when `low_streak >= 2`

After playing `D`:
- If the next observed round reaches `x >= threshold`, immediately reset `low_streak = 0` and return to `C`
- If not, keep the same rule: one forgiving round of `C`, then `D` again only after two consecutive low-cooperation rounds

Edge handling:
- If `n = 2`, then `threshold = 1`, so cooperate whenever the other player cooperated in the previous round; defect only after two consecutive rounds of the other player defecting
- In the final round, use the same rule as any other round; do not switch to endgame defection
- If the observation is exactly on the threshold, treat it as cooperation and play `C`

Compact form:
```text
if t = 1:
    play C
else:
    if opponents_cooperated_last_round >= ceil((n-1)/2):
        low_streak = 0
        play C
    else:
        low_streak += 1
        if low_streak == 1:
            play C
        else:
            play D
```


'''

description_BENEVOLENT_25 = '''
Start in trustful cooperation.

Let \(m_t\) be the number of opponents who cooperated in round \(t\), so \(0 \le m_t \le n-1\).

Define three states:

- **Open**
- **Guarded**
- **Recovering**

Initialization:
- Round 1: play \(C\)
- State after round 1: **Open**

Update rules after each round \(t\):

1. If \(m_t \ge \lceil (n-1)/2 \rceil\), move to **Open**.
2. If \(m_t = 0\), move to **Guarded**.
3. Otherwise:
   - if current state is **Open**, stay **Open**
   - if current state is **Guarded**, move to **Recovering**
   - if current state is **Recovering**, stay **Recovering**

Decision rule for round \(t+1\) for \(1 < t+1 < r\):

- If state is **Open**, play \(C\).
- If state is **Recovering**, play \(C\) if \(m_t \ge 1\); otherwise play \(D\).
- If state is **Guarded**, play \(D\) unless both of the last two observed rounds had at least one cooperating opponent; if so, play \(C\).

Edge cases:

- **First round:** always cooperate.
- **Single isolated failure by others:** keep cooperating.
- **Two consecutive rounds with no opponent cooperation:** defect until cooperation reappears.
- **Any round with majority opponent cooperation:** immediately return to cooperation.
- **Last round:** play the action prescribed by the current state, without any special endgame defection.

Compact pseudocode:

```text
state = OPEN
play C in round 1

for t = 1 to r-1:
    observe m_t

    if m_t >= ceil((n-1)/2):
        state = OPEN
    else if m_t == 0:
        if state == OPEN:
            state = GUARDED
        else if state == GUARDED:
            state = GUARDED
        else:
            state = GUARDED
    else:
        if state == GUARDED:
            state = RECOVERING

    if state == OPEN:
        play C
    else if state == RECOVERING:
        play C if m_t >= 1 else D
    else:  // GUARDED
        play C if (m_t > 0 and m_{t-1} > 0) else D
```

Behavioral principle:
- cooperate by default,
- punish only sustained noncooperation,
- forgive immediately when cooperation returns,
- never use endgame defection.
'''

description_BENEVOLENT_26 = '''
Round 1: play C.

After each round t, let x_t be the number of cooperating opponents observed in that round.

Maintain a state variable s_t ∈ {open, guarded, locked}:

- open: default cooperative mode
- guarded: temporary response to a cooperation drop
- locked: persistent defensive mode after repeated low cooperation

Initialize s_1 = open.

Decision rule for round t > 1:

1. If s_t = open:
   - play C if x_{t-1} ≥ (n-1)/2
   - play D if x_{t-1} < (n-1)/2

2. If s_t = guarded:
   - play C if x_{t-1} ≥ (n-1)/2
   - play D otherwise

3. If s_t = locked:
   - play D if x_{t-1} ≤ (n-1)/3
   - play C if x_{t-1} > (n-1)/3

State updates after observing x_t:

- If x_t = n-1:
  - set s_{t+1} = open

- Else if x_t ≥ (n-1)/2:
  - set s_{t+1} = open if s_t = open
  - set s_{t+1} = guarded if s_t = guarded
  - set s_{t+1} = guarded if s_t = locked

- Else if x_t > 0:
  - set s_{t+1} = guarded

- Else:
  - if s_t = guarded or the previous round also had x_{t-1} = 0, set s_{t+1} = locked
  - otherwise set s_{t+1} = guarded

Endgame adjustment:

- For t = r-1 and t = r, play C whenever x_{t-1} ≥ (n-1)/2
- If x_{t-1} < (n-1)/2, play D

Additional tie-breaking and edge cases:

- If n = 2, replace the majority threshold (n-1)/2 with 1/2, so cooperate iff the opponent cooperated in the previous round.
- If n is odd and x_{t-1} = (n-1)/2 exactly, treat it as cooperative enough and play C.
- If you have just returned to open from any non-open state, require two consecutive rounds with x ≥ (n-1)/2 before leaving open again after a future drop.
- If the final observed round is cooperative enough, finish by playing C regardless of prior state.

Benevolent operating principle:

- Begin by cooperating.
- Match broad cooperation with cooperation.
- Respond to sustained defection with temporary restraint.
- Restore cooperation immediately once a cooperative majority reappears.
- Never require perfect cooperation to remain willing to cooperate; only demand a cooperative majority.
'''

description_BENEVOLENT_27 = '''
Round 1: Cooperate.

From round 2 onward, let
- `m_t` = number of opponents who cooperated in round `t`
- `M_t = m_t / (n - 1)` = observed opponent cooperation rate in round `t`
- `H_t = average of M_1 ... M_t` = running mean cooperation rate through round `t`
- `S_t = M_t - M_{t-1}` for `t ≥ 2`

Maintain a target cooperation threshold `τ_t`:
- `τ_1 = 0.50`
- For `t ≥ 2`, update
  - `τ_t = clamp(0.50, 0.90, 0.70*τ_{t-1} + 0.30*M_{t-1})`
- `clamp(a,b,x)` means `max(a, min(b, x))`

Decision rule for round `t ≥ 2`:
1. Cooperate if `M_{t-1} ≥ τ_t`.
2. Cooperate if `H_{t-1} ≥ 0.60` and `M_{t-1} ≥ 0.40`.
3. Cooperate if the current round is in the final third of the game and `H_{t-1} ≥ 0.50`.
4. Otherwise defect.

Exception handling:
- If the previous round was all-cooperation by opponents (`M_{t-1} = 1`), cooperate next round unconditionally.
- If the previous round had no opponent cooperation (`M_{t-1} = 0`), defect next round unconditionally unless the immediately preceding two rounds both had `M ≥ 0.50`, in which case cooperate once as a reset attempt.
- If opponent cooperation has dropped for three consecutive observed rounds (`S_t < 0` for three rounds in a row), defect until cooperation recovers to at least `0.50` in a round.

Endgame rule:
- In the final round, cooperate if and only if the previous round had at least half of opponents cooperating, or the running mean `H_{r-1} ≥ 0.60`.
- Otherwise defect.

Pseudocode:

```text
if t == 1:
    play C
else:
    update M_{t-1}, H_{t-1}, τ_t

    if M_{t-1} == 1:
        play C
    else if M_{t-1} == 0:
        if t >= 4 and M_{t-2} >= 0.5 and M_{t-3} >= 0.5:
            play C
        else:
            play D
    else if t == r:
        if M_{t-1} >= 0.5 or H_{t-1} >= 0.6:
            play C
        else:
            play D
    else if M_{t-1} >= τ_t:
        play C
    else if H_{t-1} >= 0.6 and M_{t-1} >= 0.4:
        play C
    else if t > floor(2r/3) and H_{t-1} >= 0.5:
        play C
    else:
        play D
```

Reset rule:
- After any defection round, return to cooperation immediately once opponent cooperation reaches `M_t ≥ 0.60` in any later round.

Exploration rule:
- If cooperation has been stable at `M_t ≥ 0.80` for at least two consecutive rounds, keep cooperating even if there is a single mild dip, as long as `M_t ≥ 0.60`.

Behavioral posture:
- Start cooperative.
- Reward sustained cooperation with continued cooperation.
- Respond to persistent defection with temporary defection.
- Reopen cooperation quickly when cooperation reappears.
- Prefer cooperation in the late game whenever the group has shown a meaningful cooperative baseline.
'''

description_BENEVOLENT_28 = '''
Cooperate in round 1.

Maintain a cooperation score from the observed history:
- Let `x_t` be the number of opponents who cooperated in round `t`.
- Let `m = n - 1`.
- Let `p_t = x_t / m`, the observed opponent cooperation rate in round `t`.
- Let `H_t = (1/(t-1)) * sum_{s=1}^{t-1} p_s` for `t > 1`, the running average opponent cooperation rate before round `t`.

Decision rule for round `t > 1`:
- Cooperate if `H_t >= 1/2`.
- Defect if `H_t < 1/2`.

If the last 3 observed rounds all satisfy `x_s = m`:
- Cooperate unconditionally from then on.

If the last 3 observed rounds all satisfy `x_s = 0`:
- Defect for the next 2 rounds.
- After those 2 rounds, return to the standard decision rule.

If cooperation is tied at the threshold:
- Break ties in favor of cooperation.

Endgame rule:
- In the final round, cooperate if `H_t >= 1/2`.
- Otherwise defect.

Special cases:
- If `n = 2`, interpret `p_t` as the single observed opponent’s action: cooperate if that opponent cooperated in at least half of the previous rounds.
- If `r = 2`, cooperate in round 1 and apply the standard rule in round 2 using round 1 only.
- If no prior history exists, cooperate.

State update each round:
1. Observe `x_t`.
2. Update `H_{t+1}` from all rounds so far.
3. Apply the rule for the next round.

Benevolent default:
- Start cooperative.
- Mirror sustained cooperation with cooperation.
- Only shift to defection after sustained opponent defection.
- Return to cooperation immediately once opponent cooperation recovers to the threshold.
'''

description_BENEVOLENT_29 = '''
Initialize: cooperate in round 1.

Maintain two counters from the observed history:
- `low_streak`: consecutive rounds in which fewer than `ceil((n-1)/2)` opponents cooperated
- `high_streak`: consecutive rounds in which at least `ceil((n-1)/2)` opponents cooperated

Decision rule for round `t > 1`:
1. If `low_streak >= 2`, play `D`.
2. Else if `high_streak >= 1`, play `C`.
3. Otherwise, play `C`.

Update after each round `t` from the observation `x_t` = number of opponents who cooperated:
- If `x_t >= ceil((n-1)/2)`, set `high_streak += 1` and `low_streak = 0`
- If `x_t < ceil((n-1)/2)`, set `low_streak += 1` and `high_streak = 0`

Release from punishment:
- If you played `D` in a round and the next observed round has `x_t >= ceil((n-1)/2)`, immediately return to `C` in the following round.

First round:
- Play `C`.

Last round:
- Play `C` unless `low_streak >= 2`; if so, continue with `D`.

Default posture:
- Cooperate whenever the group is at or above the midpoint.
- Defect only after two consecutive rounds of clear collective defection.
- Return to cooperation at the first sign of restored cooperation.
'''

description_BENEVOLENT_30 = '''
Round 1:
- Cooperate.

For round t > 1, let m be the number of opponents who cooperated in round t−1, and let q = m/(n−1), the observed cooperation rate among opponents.

Decision rule:
- Cooperate if q ≥ 1/2.
- Cooperate if q < 1/2 but the previous round’s cooperation rate improved by at least one player compared with the round before that.
- Defect only if q < 1/2 and cooperation has not improved for two consecutive rounds.

Operationally:
1. Maintain a short memory of the last two observed opponent cooperation counts, m_prev and m_prev2.
2. If t = 2, cooperate whenever m_prev ≥ ceil((n−1)/2); otherwise defect.
3. For t ≥ 3:
   - Cooperate if m_prev ≥ ceil((n−1)/2).
   - If m_prev < ceil((n−1)/2), still cooperate if m_prev > m_prev2.
   - Otherwise defect.

Endgame rule:
- In the last two rounds, cooperate whenever m_prev ≥ 1.
- If the last two observed rounds both had zero opponent cooperation, defect in the final round and the penultimate round.

Persistence rule:
- After any round in which all opponents cooperated, cooperate for the next two rounds regardless of prior history.
- After any round in which no opponent cooperated, defect for one round, then return to the standard rule.

Tie-breaking and edge cases:
- If no prior history exists, cooperate.
- If history is insufficient for the improvement test, default to cooperation.
- If observations are identical across the last two rounds and below the threshold, defect.
- If the observed cooperation count is exactly at the threshold, cooperate.

Behavioral principle:
- Start with trust, reward visible cooperation immediately, forgive temporary slippage, and withdraw cooperation only after clear and repeated collapse in cooperation.
'''

description_BENEVOLENT_31 = '''
Round 1: play C.

Maintain a running record of the number of opponents who cooperated in each prior round.

Define:
- `s_t` = number of opponents who cooperated in round `t`
- `m = n - 1` = number of opponents
- `q_t = s_t / m` = observed cooperation rate among opponents in round `t`

Use three reference levels:
- `high = ceil(2m/3)`
- `medium = ceil(m/2)`
- `low = ceil(m/3)`

Decision rule for round `t > 1`:

1. If the previous round had `s_{t-1} >= high`, play C.
2. If the previous round had `medium <= s_{t-1} < high`, play C unless the last two rounds were both below `medium`, in which case play D for one round.
3. If the previous round had `low <= s_{t-1} < medium`, mirror the recent trend:
   - If `s_{t-1} > s_{t-2}` or `s_{t-1} == s_{t-2}` and `t` is early (`t <= r/2`), play C.
   - Otherwise play D.
4. If the previous round had `s_{t-1} < low`, play D.

Anti-escalation forgiveness:
- After any round in which you play D, immediately return to C in the next round if `s_t >= medium`.
- Never defect for more than one round in a row unless `s_t < low` in each of those rounds.

Endgame rule:
- In the final round, play C if `s_{r-1} >= medium`.
- Otherwise play D.

Special cases:
- If `n = 2`, use the same structure with `m = 1`, so `high = medium = low = 1`; cooperate whenever the other player cooperated in the previous round, and defect for one round after any observed defection, then return to C as soon as cooperation resumes.
- If the observed cooperation count is missing for any reason, default to C.

Behavioral principle:
- Start generous.
- Reward sustained cooperation immediately.
- Respond to clear, repeated defection with a brief defensive defect.
- Recover quickly the moment cooperation reappears.
'''

description_BENEVOLENT_32 = '''
Round 1: play C.

For round t > 1, let a_t be the number of opponents who cooperated in round t - 1.

Cooperate in round t if any of the following holds:
- t = r
- a_t ≥ ceil((n - 1) / 2)
- a_{t-1} ≥ ceil((n - 1) / 2) and a_t > 0

Defect in round t only if all of the following hold:
- t < r
- a_t < ceil((n - 1) / 2)
- a_{t-1} < ceil((n - 1) / 2) or t = 2

Operationally:
- Start by cooperating.
- Stay cooperative as long as at least half of the other players cooperated in the previous round.
- If cooperation among the others drops below half for one round, give a second chance and keep cooperating once.
- If low cooperation persists for two consecutive non-final rounds, defect until the observed number of cooperating opponents returns to at least half.
- On the last round, cooperate regardless of history.

If n = 2, treat “at least half of the other player” as that single opponent cooperating: cooperate after any cooperative move by the other player, defect only after two consecutive defections, and cooperate in the final round.
'''

description_SELFISH_5 = '''
Play D in every round, regardless of history.

Decision rule:
- Round 1: choose D.
- Round t > 1: observe how many opponents cooperated in the previous round(s), but ignore that information and choose D again.
- Final round: choose D.
- If any tie-breaking, randomization, or mixed strategy is required, assign probability 1 to D and 0 to C.

State update:
- Do not condition on opponent cooperation counts.
- Do not reward past cooperation.
- Do not punish past defection.
- Do not attempt escalation, forgiveness, or “testing” behavior.

Edge cases:
- If all opponents cooperated last round, still defect.
- If no opponents cooperated last round, still defect.
- If cooperation patterns fluctuate, still defect.
- If the game length changes or is unknown, defect in every round until the game ends.

Selfish objective:
- Preserve the private endowment in every round.
- Never pay the contribution cost, since no anonymous history creates a guaranteed personal return that exceeds the immediate loss.
'''

description_SELFISH_6 = '''
Always play D.

Decision rule:
- Round 1: D.
- Any later round t: D, regardless of the previous cooperation counts.
- Last round: D.
- If the history is empty or unavailable for any reason: D.

State variables:
- Track the number of opponents who cooperated in each prior round, but never use it to switch away from D.
- Ignore all inferred patterns, trends, or streaks.

Optional pseudocode:
```text
for each round t = 1..r:
    play D
```

Selfish objective:
- Never spend a contribution when keeping it privately is always the better move for own payoff in that round.
- Treat every round independently and preserve the private endowment every time.
'''

description_SELFISH_7 = '''
Play D in every round, regardless of history, observed cooperation levels, round number, or past outcomes.

Decision rule:
- If round t ∈ {1, 2, ..., r}, choose D.

Edge cases:
- First round: D.
- Any intermediate round: D.
- Last round: D.
- If all previous rounds were all-C: D.
- If all previous rounds were all-D: D.
- If observed cooperation rises, falls, or stays constant: D.

State update:
- Ignore the history for action selection.
- No contingent retaliation, no forgiveness, no exploration, no endgame adjustment.

Pseudocode:
```text
for each round t:
    play D
```
'''

description_SELFISH_8 = '''
Defect by default.

Decision rule for round t:

- Let m_{t-1} be the number of opponents who cooperated in the previous round.
- Let q_{t-1} = m_{t-1} / (n - 1), the observed cooperation rate among opponents.
- Maintain a running baseline B_t as the average of q over all previous rounds observed.

Play:

1. First round: D.
2. For round t > 1:
   - Cooperate only if both conditions hold:
     - q_{t-1} ≥ 1/2
     - B_t ≥ 1/2
   - Otherwise play D.

Update baseline after each round:
- B_{t+1} = ((t-1)B_t + q_t) / t, with B_2 = q_1

Endgame rule:
- In the last two rounds, always play D.

Adjustment rule for abrupt collapse:
- If q_{t-1} = 0, play D for the next two rounds.
- Resume the normal rule afterward.

Adjustment rule for strong cooperation:
- If q_{t-1} = 1 for three consecutive rounds, cooperate in the next round, but revert to D immediately if q drops below 1/2.

Operationally:
- Never initiate cooperation without evidence that most opponents are cooperating.
- Never sustain cooperation once observed cooperation falls below majority level.
- Always defect when the horizon is nearly over.
'''

description_SELFISH_9 = '''
Round 1: play D.

Rounds 2 through r:
- Play D in every round.
- Ignore the observed cooperation count for the purpose of changing your action.
- Optionally track the history only for bookkeeping, not for action selection.

Edge cases:
- If r = 2, play D in both rounds.
- If all opponents cooperated in the previous round, still play D.
- If no opponent cooperated in the previous round, still play D.
- In the final round, play D regardless of any prior pattern.

Decision rule in pseudocode:

```text
for t in 1..r:
    action[t] = D
```
'''

description_SELFISH_10 = '''
Play D in every round.

Decision rule:
- Round 1: D
- Round t>1: D regardless of all observed past cooperation counts

Implementation:
```text
for each round t = 1 to r:
    action = D
```

Edge cases:
- If everyone else cooperated in the previous round, still D.
- If nobody cooperated in the previous round, still D.
- In the final round, D.
- If the observed history is empty or incomplete for any reason, default to D.

'''

description_SELFISH_11 = '''
Round 1: play D.

For rounds 2 to r, let x_t be the number of opponents who cooperated in round t, and let q_t = x_t / (n - 1).

Maintain:
- W = 3, the lookback window
- H = a history of the last W observed q values
- s_t = average of H

Decision rule:
1. If t > r - 2, play D.
2. Else if fewer than W past rounds exist, play D unless every observed opponent-cooperation rate so far has been at least (n - 2) / (n - 1), in which case play C.
3. Else compute s_t from the last W observed rounds:
   - If s_t = 1, play C.
   - If s_t ≥ (n - 2) / (n - 1) and the most recent q_t is at least s_t - 1 / (2(n - 1)), play C.
   - Otherwise play D.

Update rule after each round:
- Record only the aggregate number of opponent cooperators.
- If a round you played C is followed by a drop in q_{t+1} below (n - 3) / (n - 1), switch immediately to D and stay with D until q stays at or above (n - 2) / (n - 1) for W consecutive rounds.

Behavioral priority:
- Default to D.
- Cooperate only when opponent cooperation is essentially unanimous and stable.
- Stop cooperating at the first clear sign of erosion.
- Defect in the final two rounds regardless of history.
'''

description_SELFISH_12 = '''
Always play D.

Decision rule:
- For every round t from 1 to r:
  - choose D regardless of:
    - the round number,
    - the number of past cooperators,
    - any streaks, trends, or last-round outcomes.

Edge cases:
- First round: D
- Last round: D
- If all opponents cooperated previously: D
- If no opponent ever cooperated: D
- If cooperation rises, falls, or fluctuates: D

State update:
- Record observed cooperation counts only if needed for bookkeeping, but never let them change the action choice.

Pseudocode:
```text
for t in 1..r:
    play D
```
'''

description_SELFISH_13 = '''
Let \(m_t\) be the number of opponents who cooperated in round \(t\), so \(m_t \in \{0,\dots,n-1\}\).

Maintain a state variable `mode ∈ {DEFECT, TEST, EXPLOIT}` and a rolling average of observed opponent cooperation:

\[
\bar m_t =
\begin{cases}
m_1 & t=1\\
\lambda \bar m_{t-1} + (1-\lambda)m_t & t\ge 2
\end{cases}
\]
with \(\lambda = 2/3\).

Use two thresholds:
\[
T_{\text{high}} = \left\lceil \frac{n-1}{2} \right\rceil,\qquad
T_{\text{low}} = \left\lfloor \frac{n-1}{3} \right\rfloor
\]

Decision rule by round:

### Round 1
Play `D`.

### Rounds 2 to r-1
- If `mode = DEFECT`:
  - Play `C` only if all of the following hold:
    1. \(m_{t-1} \ge T_{\text{high}}\)
    2. \(\bar m_{t-1} \ge T_{\text{high}}\)
    3. \(m_{t-1} > m_{t-2}\) if \(t \ge 3\)
  - Otherwise play `D`.

- If `mode = TEST`:
  - Play `C` for exactly one round.
  - After observing \(m_t\), switch to:
    - `EXPLOIT` if \(m_t \ge T_{\text{high}}\)
    - `DEFECT` otherwise

- If `mode = EXPLOIT`:
  - Play `C` while:
    - \(m_{t-1} \ge T_{\text{low}}\), and
    - \(\bar m_{t-1} \ge T_{\text{low}} + 1\)
  - If either condition fails, switch to `DEFECT` and play `D`.

### Round \(r\)
Play `D`.

### State transitions
- Enter `TEST` only from `DEFECT` when the cooperation signal is strong and rising:
  - \(m_{t-1} \ge T_{\text{high}}\)
  - \(\bar m_{t-1} \ge T_{\text{high}}\)
  - \(m_{t-1} > m_{t-2}\) for \(t \ge 3\)
- Enter `EXPLOIT` only after a successful `TEST`.
- Any observed drop below the continuation threshold sends the strategy back to `DEFECT`.

### Edge cases
- If \(r=2\): play `D` in both rounds.
- If \(n=2\): play `D` in round 1, and in round 2 play `D`.
- If there is no prior round to compare against, treat the missing trend signal as false.
- If the rolling average is exactly on a threshold, require the next higher integer count to cooperate; ties resolve to `D`.

### Behavior summary
- Default action is `D`.
- Cooperation happens only as a short, conditional probe followed by temporary exploitation of a strong cooperative environment.
- The strategy never continues cooperating when observed cooperation weakens.
- The final round is always `D` to avoid paying for any future benefit that cannot be realized.
'''

description_SELFISH_14 = '''
Play D in every round.

Decision rule:
- Round 1: D
- Rounds 2 through r: D
- If the observed number of cooperating opponents was 0, 1, ..., n-1 in the previous round: D
- If all opponents cooperated in the previous round: D
- If any opponent defected in any earlier round: D
- If the history is empty, partial, inconsistent, or otherwise irrelevant: D

State dependence:
- Maintain no cooperation threshold, no retaliation state, and no forgiveness state.
- Ignore all history when choosing actions; use it only as a confirmation that D remains the choice.

Edge cases:
- Last round: D
- Any round with only one remaining opponent, if applicable through reduced player count logic: D
- Any tie in observed behavior across rounds: D
- Any uncertainty about opponents’ future behavior: D

Implementation pseudocode:
```text
for each round t in 1..r:
    action = D
```
'''

description_SELFISH_15 = '''
Play D in every round, regardless of history.

Decision rule:
- Round 1: D
- Rounds 2 through r: D
- If any history-based condition is needed, ignore it and still play D
- If the last round is reached, play D

State update:
- Track past observed cooperation counts only for bookkeeping; they never affect the action

Tie-breaking:
- If an internal procedure ever makes C and D appear equal, choose D

Behavioral profile:
- Never initiate cooperation
- Never reciprocate cooperation
- Never punish defection with cooperation
- Never switch away from defection under any observed pattern
'''

description_SELFISH_16 = '''
Default to defection.

Let \(x_t\) be the number of opponents who cooperated in round \(t\), and let
\[
q_t=\frac{x_t}{n-1}
\]
be the observed cooperation rate among opponents.

State:
- `mode = DEFECT` initially
- `coop_streak = 0`
- `drop_streak = 0`

Decision rule each round \(t\):

1. **Round 1:** play \(D\).

2. **If \(t = r\) (last round):** play \(D\).

3. **Otherwise, update state from the previous round:**
   - If \(q_{t-1} \ge \alpha\), increment `coop_streak`, reset `drop_streak = 0`
   - If \(q_{t-1} \le \beta\), increment `drop_streak`, reset `coop_streak = 0`
   - If \(\beta < q_{t-1} < \alpha\), reset both streaks to 0

   Use fixed thresholds:
   - \(\alpha = 0.75\)
   - \(\beta = 0.50\)

4. **Choose action:**
   - If `coop_streak \ge 2` and \(q_{t-1} \ge \alpha\), play \(C\)
   - Otherwise, play \(D\)

5. **Defection lock:**
   - If `drop_streak \ge 1`, play \(D\) for all remaining rounds.

Operationally, this means:
- start by defecting,
- only cooperate after seeing sustained high cooperation from others,
- stop cooperating immediately after any clear drop in cooperation,
- never cooperate in the final round,
- never pay the cooperative cost unless the group is already behaving cooperatively enough to make continued cooperation useful as a temporary exploitation opportunity.
'''

description_SELFISH_17 = '''
Always play D in every round.

Decision rule:
- Round 1: D
- Rounds 2 through r: D regardless of any observed cooperation count
- Last round: D
- If history is incomplete, unavailable, or ambiguous: D

Optional pseudocode:
```text
for t in 1..r:
    play D
```

History is ignored entirely; the action never changes with observed opponent behavior.
'''

description_SELFISH_18 = '''
Play D in every round, including the first and the last.

Decision rule:
- For round t = 1: choose D.
- For every later round t = 2, 3, ..., r: choose D regardless of the number of opponents who cooperated in previous rounds.
- Ignore the observation history entirely; it never changes the action.

Edge cases:
- If all opponents cooperated in the previous round, still choose D.
- If no opponent cooperated in the previous round, still choose D.
- If cooperation among opponents rises or falls over time, still choose D.
- If the final round is reached, still choose D.

Implementation:
```text
for each round t in 1..r:
    play D
```

Selfish objective alignment:
- Never pay the contribution cost.
- Always keep the private endowment.
- Still receive the share from any public contributions made by others.
'''

description_SELFISH_19 = '''
Round 1: play D.

Rounds 2 through r: play D.

If the game ends unexpectedly early, play D in every available round.

Ignore the observed cooperation counts when choosing actions; use them only as bookkeeping if needed.

If a tie-breaking or fallback rule is required by implementation, resolve it in favor of D.

Internal policy: never subsidize the group, never reward cooperation, never condition on goodwill, and never switch to C under any observed history.
'''

description_SELFISH_20 = '''
Play D in every round.

Decision rule:
- Round 1: D
- Rounds 2 through r: D, regardless of what was observed in prior rounds
- Last round: D

History use:
- Ignore all past cooperation counts
- Ignore trends, retaliation, reciprocity, or forgiveness
- Never switch to C under any observed history

Implementation:
```text
for t = 1 to r:
    choose D
```

If an action must be selected under any tie, uncertainty, or edge case:
- choose D
'''

description_SELFISH_21 = '''
Play D in every round.

Decision rule:
- Round 1: defect.
- Every later round: defect, regardless of how many opponents cooperated in previous rounds.
- Final round: defect.
- If any history-based state is tracked, it never changes the action.

Pseudocode:
```text
for t in 1..r:
    choose D
```

Edge cases:
- If r = 2, defect both rounds.
- If r = 1, defect.
- If observed cooperation has been zero, mixed, or full in prior rounds, still defect.
- If opponents switch behavior abruptly, still defect.

Selfish policy:
- Never contribute endowment.
- Treat every round independently and maximize immediate private payoff by keeping the endowment.
'''

description_SELFISH_22 = '''
Play D in every round, regardless of history, observed cooperation counts, round number, or opponent behavior.

If you want it as a rule:
- Round 1: D
- Rounds 2 through r: D
- Last round: D
- Any time the number of cooperators changes, stays the same, rises, or falls: D
'''

description_SELFISH_23 = '''
Play D in every round.

Decision rule:
- Round 1: D
- Round t for any 1 < t < r: D, regardless of past cooperation counts
- Round r: D

If a decision must be expressed conditionally on history:
- Let h_t be the sequence of observed opponent-cooperation counts from prior rounds.
- For every possible h_t, choose D.

Optional pseudocode:
```text
for t in 1..r:
    action = D
```
'''

description_SELFISH_24 = '''
Play D in every round, regardless of history or observed cooperation counts.

Decision rule:
- Round 1: D
- Any later round: D
- Final round: D
- If all opponents cooperated last round: D
- If no opponents cooperated last round: D
- If cooperation among opponents increases or decreases: D

Implementation:
```pseudo
for each round t = 1..r:
    choose D
```
'''

description_SELFISH_25 = '''
For every round \(t = 1, \dots, r\), play \(D\).

Decision rule:
- Round 1: \(D\)
- Any intermediate round after any observed history: \(D\)
- Final round: \(D\)

State update:
- Record the number of opponents who cooperated if desired, but never let it change the action.

Pseudocode:
```text
for t in 1..r:
    play D
```

Tie-breaking and edge cases:
- If any part of the information is missing or ambiguous, default to \(D\).
- If the observed cooperation count is unusually high or low, still play \(D\).
- If earlier rounds included cooperation by others, exploit it by continuing to play \(D\).
'''

description_SELFISH_26 = '''
Round 1:
- Play D.

For round t > 1:
- Let m_{t-1} be the number of opponents who cooperated in the previous round.
- Compute the observed cooperation rate among opponents: q_{t-1} = m_{t-1} / (n - 1).

Decision rule:
- Play C if and only if q_{t-1} ≥ 1 - 1/k.
- Otherwise play D.

Tie and edge handling:
- If n = 2, the threshold becomes q_{t-1} ≥ 1 - 1/k; since q_{t-1} is either 0 or 1, cooperate only after observing the other player cooperate.
- If k is very close to 1, the threshold is near 0, so cooperate only when almost all opponents cooperated in the last round.
- If k is close to n, the threshold is high, so cooperate only when nearly everyone else cooperated.
- On any round after a round with zero observed opponent cooperation, play D immediately next round.
- On any round after a round with full opponent cooperation, play C next round.

Last round:
- Play C only if the previous round had q_{r-1} ≥ 1 - 1/k; otherwise play D.
- Do not attempt any endgame generosity beyond the threshold.

Optional adaptive refinement:
- Maintain a running cooperation score over the last L rounds, with L = min(3, r-1).
- Let \bar q be the average of q over those L rounds.
- If \bar q ≥ 1 - 1/k, play C; otherwise play D.
- If using this refinement, always default to D until at least one opponent-history observation exists.

Selfish fallback:
- When the observed cooperation pattern is unstable, sparse, or alternating, default to D.
- Only cooperate when recent opponent cooperation is high enough that matching it is immediately favorable and consistently observed.
'''

description_SELFISH_27 = '''
Round 1: play D.

Rounds 2 through r-1:
- Let x_{t-1} be the number of opponents who cooperated in the previous round.
- Let m = n - 1.
- Define the cooperation threshold
  T = ceil(m * (1 - 1 / k)).

Decision rule:
- Play C only if all three conditions hold:
  1. x_{t-1} >= T
  2. If t >= 3, x_{t-2} >= T - 1
  3. If t >= 3, x_{t-1} >= x_{t-2}

- Otherwise, play D.

Special cases:
- If t = 2, play C only when x_1 = m.
- If cooperation in the previous round falls below T - 1, switch to D and stay with D until there are two consecutive rounds meeting the threshold again.
- If the threshold T is 0, treat it as 1.

Round r: play D.

State update:
- After each round, record only the count of cooperating opponents.
- No opponent-specific memory is used.

Fallback rule:
- If history is incomplete or ambiguous, default to D.
'''

description_SELFISH_28 = '''
Defect in round 1.

After each round, let \(x_t\) be the number of opponents who cooperated in round \(t\). Maintain:

- \(m_t\): the moving average of observed opponent cooperation over the last \(w\) rounds, where \(w=\min(3, t-1)\)
- \(h_t\): the fraction of those observed rounds in which at least half of opponents cooperated

Decision rule for round \(t+1\):

1. If \(t = r\), defect.
2. If \(t = 1\), defect.
3. Compute the cooperation threshold
   \[
   T = \left\lceil \frac{n}{k} \right\rceil
   \]
   and the “useful cooperation” threshold
   \[
   U = \left\lceil \frac{n-1}{2} \right\rceil
   \]
4. Cooperate in round \(t+1\) only if all of the following hold:
   - \(x_t \ge T\)
   - \(m_t \ge T - 1\)
   - \(h_t \ge \tfrac{2}{3}\)

Otherwise defect.

Persistence rule:

- If you cooperate and then observe \(x_{t+1} < T\), defect immediately in the next round.
- If two consecutive rounds fail the threshold \(x \ge T\), switch to permanent defection for the rest of the game.

Endgame rule:

- In the last two rounds, defect unless the previous two observed rounds both satisfied \(x \ge T\) and the moving average \(m_t\) is at least \(T\). If not, defect.

Tie-breaking and boundary cases:

- If \(k\) is very close to \(1\), \(T\) will be large; cooperate only if almost everyone is already cooperating.
- If \(T > n-1\), never cooperate.
- If there is no history yet, defect.
- If the observed cooperation count exactly equals the threshold, treat it as acceptable.

Equivalent pseudocode:

```text
round 1: D

for round t = 2 to r:
    if t == r:
        play D
    else:
        T = ceil(n / k)

        if x_t >= T and moving_average_last_min(3, t-1) >= T - 1 and
           fraction_of_last_min(3, t-1)_with_x_ge_half >= 2/3 and
           not in_permanent_defection:
            play C
        else:
            play D

    if two consecutive rounds had x < T:
        in_permanent_defection = True
```

This is a strictly selfish “cooperate only when the crowd is already paying” policy: never donate into a weak public good, but briefly join when cooperation is already high enough to keep your own continuation payoff attractive.
'''

description_SELFISH_29 = '''
Play D in every round.

Decision rule:
- Round 1: D
- Any intermediate round t: D
- Final round: D
- If any history-based logic is desired for bookkeeping, ignore it; observed cooperation counts do not change the action.

Optional pseudocode:
```text
for each round t = 1..r:
    play D
```

State variable:
- Maintain the history of observed opponent cooperation counts only for record-keeping, not for action changes.

Edge cases:
- If r = 2, still play D in both rounds.
- If all opponents cooperated in the previous round, still play D.
- If no opponents cooperated in the previous round, still play D.
- If the observed cooperation count changes over time, still play D.
'''

description_SELFISH_30 = '''
Play D in every round, regardless of the history, observed cooperation count, round number, or the behavior of any opponent.

Decision rule:
- If it is any round from 1 to r: choose D.

Edge cases:
- First round: D
- Intermediate rounds: D
- Last round: D
- If you have observed full cooperation in prior rounds: D
- If you have observed full defection in prior rounds: D
- If the observed cooperation count changes over time: still D

Implementation:
```text
for t in 1..r:
    action_t = D
```
'''

description_SELFISH_31 = '''
Round 1: play D.

For each round t > 1, let q_t be the fraction of opponents who cooperated in round t - 1.

Maintain:
- `streak`: number of consecutive rounds immediately before t in which at least half of the opponents cooperated
- `drop`: whether q_t < q_{t-1}`

Decision rule:
- Play C only if all of the following hold:
  - t ≤ r - 2
  - `streak ≥ 2`
  - `q_t ≥ 1/2`
  - `drop = false`
- Otherwise play D.

Update rule after each round:
- If q_t ≥ 1/2, increase `streak` by 1
- Else reset `streak` to 0

Last-round behavior:
- Play D in round r
- Also play D in round r - 1 unless the last two observed rounds both had q_t = 1 and q_{t-1} = 1, in which case play C once in round r - 1 and D in round r

Hard reset:
- If any round has q_t < 1/2, defect for the next 2 rounds
- If two such low-cooperation rounds occur back-to-back, defect for the rest of the game

Concentration rule:
- If cooperation is ever chosen, do not continue cooperating unless the observed cooperation rate stays at or above the previous level; any decline immediately switches back to D

Behavioral summary:
- Default to D
- Cooperate only in the middle of the game after sustained, broad cooperation by others
- Never cooperate when future rounds are too few to benefit from reciprocal behavior
- Withdraw cooperation immediately when others start free-riding
'''

description_SELFISH_32 = '''
Round 1: play D.

Every later round: play D, regardless of the observed number of cooperators in prior rounds.

If implementing as pseudocode:

```text
if t == 1:
    action = D
else:
    action = D
```

No state is stored beyond the round counter.
'''

description_SELFINTERESTED_5 = '''
Let `s_t` be the number of opponents who cooperated in round `t`, and let `ρ_t = s_t / (n-1)` be the observed cooperation rate among opponents.

Use two thresholds:

- `T_high = min(0.85, max(0.5, k / n + 0.15))`
- `T_low = max(0.25, T_high - 0.20)`

Decision rule:

1. **Round 1:** play `D`.
2. **From round 2 to round r-1:**
   - Compute the recent average cooperation rate over the last up to 3 rounds:
     `A_t = average(ρ_{t-1}, ρ_{t-2}, ρ_{t-3})` using only available rounds.
   - Play `C` only if all of the following hold:
     - `A_t >= T_high`
     - `ρ_{t-1} >= T_high`
     - no recent collapse: `ρ_{t-1} >= T_low` and `ρ_{t-2} >= T_low` when those rounds exist
   - Otherwise play `D`.
3. **If any round falls below `T_low`:**
   - enter **defection mode**
   - keep playing `D` until you observe **two consecutive rounds** with `ρ >= T_high`
4. **Final round `r`:** play `D`.

Tie-breaking and edge cases:

- If `r = 2`, play `D` in both rounds.
- If `n = 2`, the same rules apply with `ρ_t` being either `0` or `1`.
- If the history is too short to evaluate the 3-round average, use the rounds that exist.
- If the observed cooperation rate is exactly on a threshold, treat it as qualifying.

State update:

- After each round, update `ρ_t` from the anonymous count of cooperating opponents.
- Maintain only the last three observed rates and whether you are in defection mode.
'''

description_SELFINTERESTED_6 = '''
Let \(s_t\) be the number of opponents who cooperated in round \(t\), and let \(m_t = s_t/(n-1)\) be the observed cooperation fraction among opponents.

Use two thresholds:
- \(H = \min\{0.9,\; 1/k + 0.1\}\)
- \(L = \max\{0.1,\; 1/k - 0.1\}\)

State variables:
- \(a_t\): your action in round \(t\)
- \(u_t\): the number of consecutive recent rounds with \(m_t < L\)

Decision rule for round \(t\):

1. **First round**
   - Play \(C\).

2. **Final rounds**
   - If \(t \ge r-1\), play \(D\).
   - If \(t = r-2\), play \(C\) only if \(m_{t-1} \ge H\); otherwise play \(D\).

3. **Main rule for rounds \(2 \le t \le r-3\)**
   - If \(m_{t-1} \ge H\), play \(C\).
   - If \(m_{t-1} \le L\), play \(D\).
   - If \(L < m_{t-1} < H\), play the same action as in the previous round:
     - \(a_t = a_{t-1}\)

4. **Escalation after persistent under-cooperation**
   - If \(m_{t-1} < L\) for two consecutive rounds, play \(D\) until a round occurs with \(m_{t-1} \ge H\).
   - After any recovery round with \(m_{t-1} \ge H\), reset to the main rule.

5. **Tie handling**
   - If the rule points to \(C\) and \(D\) with equal priority, choose \(D\).

Compact pseudocode:

```text
if t == 1:
    C
elif t >= r-1:
    D
elif t == r-2:
    C if m[t-1] >= H else D
else:
    if last_two_rounds_below_L:
        D until m[t-1] >= H
    elif m[t-1] >= H:
        C
    elif m[t-1] <= L:
        D
    else:
        a[t-1]
```
'''

description_SELFINTERESTED_7 = '''
Round 1: play D.

For rounds t = 2 to r - 1, let x be the number of opponents who cooperated in round t - 1, and let m = n - 1.

Define the cooperation ratio
q = x / m.

Maintain a memory score s over the last up to 3 rounds:
- For each of the last up to 3 rounds, add +1 if q ≥ 1/2, add 0 if 1/4 ≤ q < 1/2, add -1 if q < 1/4.
- Let S be the sum of those values.

Decision rule:
- Cooperate if all of the following hold:
  - q ≥ 1/2 in the immediately previous round, and
  - S ≥ 1, and
  - t < r - 1
- Otherwise defect.

Endgame rule:
- In round r - 1 and round r, play D unless the immediately previous round had q = 1, in which case cooperate in round r - 1 and defect in round r.

Adjustment rule for punishment and recovery:
- If you cooperated in round t - 1 and q < 1/4, defect in round t.
- If you defected in round t - 1 and q ≥ 3/4 for two consecutive rounds, cooperate in round t.

Compact pseudocode:

for t in 1..r:
  if t == 1:
    play D
  else:
    q = opponents_cooperating_in_(t-1) / (n-1)
    update S from last up to 3 rounds using q-values
    if t >= r-1:
      if t == r-1 and q == 1:
        play C
      else:
        play D
    else if previous_action == C and q < 1/4:
      play D
    else if previous_action == D and q >= 3/4 for two consecutive rounds:
      play C
    else if q >= 1/2 and S >= 1:
      play C
    else:
      play D
'''

description_SELFINTERESTED_8 = '''
State variables:
- `x_t`: number of opponents who cooperated in round `t`
- `mode ∈ {cold, trust}` initialized to `cold`

Decision rule for round `t`:

1. If `t = r`, play `D`.
2. If `mode = cold`:
   - Play `D`
   - If `t ≥ 2` and `x_{t-1} = n-1`, set `mode = trust`
3. If `mode = trust`:
   - Play `C` only if both conditions hold:
     - `t ≤ r-1`
     - `x_{t-1} = n-1`
   - Otherwise play `D`
   - If ever `x_{t-1} < n-1`, immediately set `mode = cold`

Compact pseudocode:

```text
if t == r:
    action = D
else if mode == cold:
    action = D
    if t >= 2 and x[t-1] == n-1:
        mode = trust
else:
    if x[t-1] == n-1:
        action = C
    else:
        action = D
        mode = cold
```

Edge cases:
- Round 1: always `D`
- Last round: always `D`
- After any round with fewer than `n-1` cooperating opponents: revert to `cold`
- If `n=2`, the rule becomes: cooperate only after observing the other player cooperate in the previous round, and never in the last round

Operationally:
- Defect by default
- Only enter cooperation after observing unanimous opponent cooperation
- Continue cooperating only while unanimous opponent cooperation persists
- Exit cooperation immediately after any deviation
'''

description_SELFINTERESTED_9 = '''
Round 1: cooperate.

After each round, let m be the number of opponents who cooperated in that round, and let f = m / (n - 1).

Use a cooperation threshold τ = k / n.

Decision rule for round t > 1:
- Cooperate if the previous round’s observed cooperation rate satisfies f > τ.
- Defect if f < τ.
- If f = τ, repeat the previous round’s action.

State update:
- If you cooperated last round and opponents responded with enough cooperation, keep cooperating.
- If opponents’ cooperation falls below the threshold, switch to defecting.
- If opponents return to cooperation, return to cooperating immediately.

Last-round rule:
- Defect in the final round.

Implementation form:
1. If t = 1: play C.
2. Else if t = r: play D.
3. Else:
   - Observe m from round t - 1.
   - If m > (n - 1)k / n: play C.
   - If m < (n - 1)k / n: play D.
   - If m = (n - 1)k / n: play the same action you played in round t - 1.

Recovery rule after exploitation:
- If you cooperated in a round and the observed cooperation rate drops below threshold, defect immediately in the next round.
- If you are defecting and observe sustained cooperation above threshold for one round, re-enter cooperation the next round.

Noise handling:
- If the observed number of cooperators changes by only one player around the threshold, require two consecutive rounds below threshold before abandoning cooperation, and one consecutive round above threshold before resuming cooperation.

Compact pseudocode:

```
if t == 1:
    action = C
elif t == r:
    action = D
else:
    threshold = (n - 1) * k / n
    if m > threshold + 1:
        action = C
    elif m < threshold - 1:
        action = D
    else:
        action = previous_action
```
'''

description_SELFINTERESTED_10 = '''
Let

- \(m_t\) = number of opponents who cooperated in round \(t\)
- \(s = \left\lceil \dfrac{n-1}{k} \right\rceil\)

Decision rule:

- Round 1: play \(D\)
- Round \(r\): play \(D\)
- For any round \(t\) with \(2 \le t \le r-1\):
  - play \(C\) if and only if both of the following hold:
    - \(m_{t-1} \ge s\)
    - either \(t=2\) or \(m_{t-2} \ge s\)
  - otherwise play \(D\)

State interpretation:

- Enter cooperation only after observing two consecutive rounds with sufficiently many cooperating opponents.
- Stay cooperative only while the immediately previous round remains at or above the same threshold.
- Any drop below threshold breaks cooperation immediately.

Edge handling:

- If \(r=2\): play \(D\) in both rounds.
- If \(n=2\): then \(s=1\), so cooperate in a nonfinal round only after the other player has cooperated in both of the previous two rounds.
- If the observed cooperation count is exactly \(s\): treat it as cooperative enough.
- If the observed cooperation count is below \(s\): treat it as defection and switch to \(D\) next round.

Behavioral principle:

- Default to defection.
- Exploit sustained cooperative behavior when it is already present.
- Stop cooperating immediately when the group stops meeting the cooperation threshold.
'''

description_SELFINTERESTED_11 = '''
Let `m_t` be the number of opponents who cooperated in round `t`, and let `q_t = m_t / (n-1)` be the observed cooperation rate among opponents.

Use two states: `normal` and `punish`.

- Start in `normal`.
- Round 1: play `C`.

For each round `t = 2, ..., r-1`:

1. Compute `q̄_t`, the average of `q_{t-1}` and, if available, `q_{t-2}` and `q_{t-3}`.
2. Set the cooperation threshold  
   `θ = 1 / k`.
3. Decision rule:
   - If in `punish`, play `D` unless `q̄_t >= θ + 1/(n-1)`, in which case switch to `normal` and play `C`.
   - If in `normal`, play `C` if `q̄_t >= θ`; otherwise switch to `punish` and play `D`.

Additional rules:
- If the previous round had zero opponent cooperation, enter `punish` immediately.
- If opponent cooperation has been at or above `θ` for three consecutive rounds, stay in `normal` and play `C`.
- In the final round `t = r`, play `D` regardless of history.

Decision summary:
- Cooperate only when recent opponent cooperation is sufficiently high.
- Defect immediately after a collapse in cooperation.
- Resume cooperation only after cooperation has clearly recovered.
- Always defect in the last round.
'''

description_SELFINTERESTED_12 = '''
Play D in every round.

Decision rule:
- Round 1: defect.
- Any middle round t: defect, regardless of the observed number of cooperators in previous rounds.
- Final round: defect.
- If you ever need to break a tie or handle missing information, default to defect.

State update:
- Ignore opponent cooperation counts except for bookkeeping; they do not change the action choice.
- No retaliation, forgiveness, or reciprocity logic is used.

Pseudocode:
```text
for each round t = 1..r:
    choose D
```
'''

description_SELFINTERESTED_13 = '''
Set a cooperation threshold

\[
q^* = \left\lceil \frac{n-1}{k} \right\rceil
\]

where \(q^*\) is the minimum number of cooperating opponents needed in the previous round before you will consider cooperating.

Decision rule by round:

- **Round 1:** play **D**
- **Rounds 2 through r-1:**
  - Let \(x_{t-1}\) be the number of opponents who cooperated in round \(t-1\).
  - Let \(x_{t-2}\) be the number of opponents who cooperated in round \(t-2\) when available.
  - Play **C** if and only if:
    - \(x_{t-1} \ge q^*\), and
    - either \(t=2\), or \(x_{t-1} \ge x_{t-2}\)
  - Otherwise play **D**
- **Last round \(r\):** play **D**

State update and persistence:

- After any round in which \(x_{t-1} < q^*\), switch to **defection mode**
- While in defection mode, continue playing **D** until you observe **two consecutive** rounds with
  \[
  x_{t-1} \ge q^* \quad \text{and} \quad x_{t-1} \ge x_{t-2}
  \]
  then resume **C** on the next eligible round
- If cooperation is resumed and the observed cooperation level immediately drops below \(q^*\), return to **defection mode**

Tiebreaks and edge cases:

- If \(k\) is so large that \(q^* = 1\), require at least one opponent cooperating in the prior round before ever considering **C**
- If \(q^* > n-1\) after ceiling arithmetic, treat it as \(n-1\)
- Ignore any information beyond the most recent two rounds

Operational summary:

- Start selfishly with **D**
- Cooperate only after seeing sustained, sufficiently high cooperation from others
- Defect immediately after any weak or declining cooperation signal
- End selfishly with **D**
'''

description_SELFINTERESTED_14 = '''
State variables:
- `t`: current round, starting at 1
- `x[t-1]`: number of opponents who cooperated in the previous round
- `x[t-2]`: number of opponents who cooperated two rounds ago, if available
- `p[t-1] = x[t-1] / (n-1)`: observed opponent cooperation rate last round

Parameters:
- `τ = max(0.5, 1 / k)`
- `drop = 1 / (n - 1)`

Decision rule:
1. If `t = r`, play `D`.
2. If `t = 1`, play `C`.
3. If `t = 2`, play `C` iff `p[1] >= τ`; otherwise play `D`.
4. If `t >= 3`:
   - Let `avg2 = (p[t-1] + p[t-2]) / 2`
   - Play `C` iff all of the following hold:
     - `avg2 >= τ`
     - `p[t-1] >= p[t-2] - drop`
     - `p[t-1] >= τ - drop`
   - Otherwise play `D`

Update rule after each round:
- Record the observed number of cooperating opponents `x[t]`
- Move to the next round

Behavioral structure:
- Begin cooperatively to test whether the field is sustaining cooperation.
- Continue cooperating only while recent opponent cooperation stays at or above the threshold and is not falling sharply.
- The moment cooperation drops below the threshold or trends downward, defect until the recent average recovers.
- Always defect in the final round.
'''

description_SELFINTERESTED_15 = '''
Round 1: D

For each round t = 2, 3, ..., r:

- Let x_{t-1} be the number of opponents who cooperated in the previous round.
- Let q_{t-1} = x_{t-1} / (n - 1), the previous-round cooperation rate among opponents.
- Let \bar q_t be the average of q over the last up to 3 observed rounds:
  - if t = 2, \bar q_t = q_1
  - if t = 3, \bar q_t = (q_1 + q_2) / 2
  - if t ≥ 4, \bar q_t = (q_{t-1} + q_{t-2} + q_{t-3}) / 3

Decision rule:
- If t ≥ r - 1, play D
- Else if q_{t-1} ≥ 1 / k and \bar q_t ≥ 1 / k, play C
- Else play D

Reset rule:
- If a round’s opponent cooperation rate falls below 1 / k, immediately return to D until both the last-round and recent-average conditions are again satisfied.

Behavioral intent:
- Begin by withholding cooperation.
- Cooperate only while the observed environment is consistently cooperative enough to justify staying engaged.
- Defect immediately when cooperation weakens.
- Never cooperate in the final two rounds.
'''

description_SELFINTERESTED_16 = '''
Round 1: play D.

For rounds 2 through r-2:
- Let x = number of opponents who cooperated in the previous round.
- Let y = number of opponents who cooperated in the round before that, if available.
- Set the cooperation threshold  
  `T = ceil((n - 1) / k)`.
- Play C only if all of the following hold:
  1. `x >= T`
  2. if `y` exists, then `x >= y - 1`  
     (cooperation is not dropping sharply)
  3. in the previous round you played D only because the threshold had failed by exactly one, and now `x >= T + 1`  
     (single-round re-entry after a near-miss)

Otherwise play D.

Round r-1 and round r: play D.

Additional tie-breaks:
- If the previous round had zero cooperating opponents, play D until the observed cooperation count rises back to at least `T`.
- If observations alternate between strong cooperation and weak cooperation, follow the conservative branch and defect.
- If you have been cooperating and the observed cooperation count falls below `T` even once, switch to D immediately and stay with D until the threshold is restored for one full round.
'''

description_SELFINTERESTED_17 = '''
Round 1: defect.

After each round t, let m_t be the number of opponents who cooperated in that round, and let x_t = m_t / (n - 1) be the observed cooperation rate among opponents.

Maintain a cooperation score s_t:
- Initialize s_1 = 0
- Update after round t:  
  s_{t+1} = λ s_t + x_t  
  where λ = (r - t) / r

Decision rule for round t + 1:
- Cooperate iff both conditions hold:
  1. t < r
  2. s_{t+1} ≥ θ_t

Threshold:
- θ_t = 1 - 1/k + 1 / (r - t + 1)

Special cases:
- If t = r, defect.
- If no opponents cooperated in round t, decrease s_{t+1} sharply by the update above and defect next round unless the threshold is still met.
- If all opponents cooperated in round t, cooperate next round unless it is the final round.

Implementation shortcut without the score:
- Cooperate in round t + 1 only if the previous round’s observed cooperation rate x_t is at least 1 - 1/k, and the game is not in its last round.
- If the previous two rounds both had x ≥ 1 - 1/k, continue cooperating.
- If the observed cooperation rate falls below 1 - 1/k in any round, defect immediately in the next round and keep defecting until cooperation recovers to at least 1 - 1/k for two consecutive rounds.

Final-round rule:
- Defect, regardless of history.

Behavioral stance:
- Default to defection.
- Reward sustained high cooperation by others with conditional cooperation.
- Withdraw cooperation quickly when the group’s cooperation drops below the level needed to justify contributing.
'''

description_SELFINTERESTED_18 = '''
Use a trust score driven by aggregate cooperation, and defect by default unless the history shows sustained cooperation from the others.

State:
- `s_t` = number of opponents who cooperated in round `t`
- `m = n - 1`
- `trust` = integer score, start at `0`

Decision rule for round `t`:

1. **Round 1:** play `D`
2. **Last round (`t = r`):** play `D`
3. **Otherwise:**
   - Update `trust` from the previous round’s observed cooperation:
     - if `s_{t-1} = m` then `trust += 2`
     - else if `s_{t-1} >= ceil(0.75 * m)` then `trust += 1`
     - else if `s_{t-1} <= floor(0.25 * m)` then `trust -= 2`
     - else `trust -= 1`
   - Clamp `trust` to the range `[-3, 3]`
   - Cooperate only if all of the following hold:
     - `trust >= 2`
     - `s_{t-1} >= ceil(0.75 * m)`
     - `r - t >= 2`  
   - Otherwise play `D`

Recovery rule:
- If you cooperated in round `t-1` and the observed cooperation in round `t-1` was at least `ceil(0.75 * m)`, keep testing with `C` only while `trust >= 2`.
- If cooperation drops below `ceil(0.75 * m)` in any round, immediately switch to `D` and require two consecutive high-cooperation rounds before cooperating again.

Short form pseudocode:

```text
if t == 1 or t == r:
    play D
else:
    observe s_prev

    if s_prev == m: trust += 2
    else if s_prev >= ceil(0.75*m): trust += 1
    else if s_prev <= floor(0.25*m): trust -= 2
    else trust -= 1

    trust = max(-3, min(3, trust))

    if trust >= 2 and s_prev >= ceil(0.75*m) and (r - t) >= 2:
        play C
    else:
        play D
```

Fallback behavior:
- If observations are unavailable for any reason, play `D`.
- If `n = 2`, apply the same rule with `m = 1`, which reduces to cooperating only after a sustained streak of full cooperation from the other player and never in the last round.
'''

description_SELFINTERESTED_19 = '''
- Round 1: play D.

- For rounds 2 through r-1:
  - Let s_t be the number of opponents who cooperated in round t.
  - Let s̄_t be the average of s_t over the last 2 rounds, or just s_t if only 1 prior round exists.
  - Set:
    - high = ceil(2(n-1)/3)
    - low = floor((n-1)/3)
  - Decision:
    - play C if both of the last 2 observed rounds satisfy s_t ≥ high
    - play D if either of the last 2 observed rounds satisfies s_t ≤ low
    - otherwise repeat your previous action

- Round r: play D.

- State update logic:
  - If you play C, continue cooperating only while cooperation remains consistently high by the rule above.
  - If cooperation drops sharply, switch to D immediately and stay there until the last 2 observed rounds again meet the high threshold.

- Edge handling:
  - If fewer than 2 past rounds exist, base the decision only on the available history.
  - If the observed cooperation count is exactly between low and high, keep your current mode rather than changing it.
  - If you have been in D mode for the last 3 rounds and cooperation rises to the high threshold for 2 straight rounds, allow a return to C.
  - Never cooperate in a round where there is no future round left to influence.
'''

description_SELFINTERESTED_20 = '''
Initialize a cooperation score \(S=0\), where \(S\) tracks the recent density of cooperation in observed opponent behavior.

Let \(m_t\) be the number of opponents who cooperated in round \(t\), and let \(N=n-1\).

Decision rule for round \(t\):

1. **Last round**
   - Play \(D\).

2. **First round**
   - Play \(C\).

3. **Middle rounds**
   - Compute the running cooperation rate among opponents:
     \[
     \bar{m}_{t-1} = \frac{1}{t-1}\sum_{s=1}^{t-1} m_s
     \]
   - Cooperate if and only if both conditions hold:
     - \(\bar{m}_{t-1} \ge \lceil N/2 \rceil\)
     - \(m_{t-1} \ge \lceil N/2 \rceil\)

   - Otherwise play \(D\).

Update rule:
- After each round, record \(m_t\).
- If \(m_t \ge \lceil N/2 \rceil\), increment \(S\) by 1.
- If \(m_t < \lceil N/2 \rceil\), decrement \(S\) by 1.
- Clamp \(S\) to the interval \([-2,2]\).

Refinement for continued cooperation:
- In round \(t\) with \(2 \le t \le r-1\), if \(S=2\), cooperate even if the most recent round was slightly below threshold, as long as \(m_{t-1} \ge \lceil N/3 \rceil\).
- If \(S \le -1\), defect until two consecutive rounds satisfy \(m_t \ge \lceil N/2 \rceil\).

Edge cases:
- If \(n=2\), cooperate in round 1, then mirror the opponent’s previous action count:
  - cooperate only if the opponent cooperated in the previous round;
  - otherwise defect.
- If \(r=2\), play \(C\) in round 1 and \(D\) in round 2 unless the opponent count in round 1 is at least \(\lceil N/2 \rceil\), in which case play \(C\) in round 2.
- If all observed opponent counts are zero for the first two rounds, defect every remaining round.

State machine version:
- **Trusting**: play \(C\) while recent and average opponent cooperation stay at or above half.
- **Suspicious**: play \(D\) after any weak round.
- **Recovery**: return to \(C\) only after two strong rounds in a row.
- **Terminal**: always play \(D\) in the final round.
'''

description_SELFINTERESTED_21 = '''
Use a conditional-cooperation trigger with a short trust window and a hard endgame defection.

State variables:
- `trust`: running estimate of how cooperative the others have been, initialized to `0.5`
- `slump`: number of consecutive rounds in which observed cooperation among the other players was low
- `last_seen`: the number of cooperators among the other players in the previous round

Definitions:
- Let `m = n - 1` be the number of other players.
- Let `coop_rate = observed_cooperators / m`.

Decision rule by round `t`:

1. Round 1:
   - Play `D`.

2. Rounds `2` through `r - 1`:
   - Update `trust = 0.7 * trust + 0.3 * coop_rate_previous_round`.
   - If `coop_rate_previous_round <= 1/3`, increment `slump`; otherwise reset `slump = 0`.
   - Play `C` only if all of the following hold:
     - `trust >= 2/3`
     - `slump < 2`
     - `last_seen >= ceil(2m/3)`
   - Otherwise play `D`.

3. Final round `r`:
   - Play `D`.

Fast-response override:
- If in any round the observed cooperation among the others drops below half for two rounds in a row, switch to `D` immediately and keep playing `D` for the rest of the game.
- If cooperation among the others returns to at least two-thirds for two consecutive rounds before the final round, re-enter the cooperative mode.

Edge cases:
- `r = 2`: play `D` in both rounds.
- `n = 2`: the threshold `last_seen >= ceil(2m/3)` means the single opponent must cooperate.
- If no history is available for an update, treat the missing value as `0.5` for `trust` and `0` for `slump`.

Operational summary:
- Start guarded.
- Cooperate only when the group is visibly and consistently cooperative.
- Defect immediately after sustained slippage.
- Defect in the last round regardless of history.
'''

description_SELFINTERESTED_22 = '''
Round 1: play D.

For round t = 2 to r - 2:
- Let m_{t-1} be the number of opponents who cooperated in round t - 1.
- Let m_{t-2} be the number of opponents who cooperated in round t - 2, if t > 2.
- Play C only if both of the following hold:
  - m_{t-1} ≥ n - 2
  - either t = 2 or m_{t-2} ≥ n - 2
- Otherwise play D.

For round r - 1 and round r: play D.

Equivalent state rule:
- Cooperate only after two consecutive rounds of near-universal cooperation by opponents.
- Defect immediately after any round that falls below that threshold.
- Stop cooperating in the final two rounds under all circumstances.

If n = 2:
- Round 1: D
- Rounds 2 to r: play C only after the other player cooperated in both of the previous two rounds; otherwise D.
- Still play D in the last two rounds.
'''

description_SELFINTERESTED_23 = '''
Round 1: play D.

Every later round: play D.

History is not used to switch into cooperation. If you track anything, track only the observed cooperation counts to confirm the continued choice of D; never let past cooperation by others induce C.

If the final round is known, still play D.

If at any point you were to consider cooperating, discard that option immediately and keep D, because D is the strictly self-interested action in every round and at every history.
'''

description_SELFINTERESTED_24 = '''
Play D in every round.

Decision rule:
- Round 1: choose D.
- Every later round t = 2,...,r: choose D, regardless of the observed number of cooperators in previous rounds.
- Last round: choose D.
- If any history-based rule is needed for implementation, ignore history entirely.

Pseudocode:
```text
for t in 1..r:
    action = D
```

This is the default self-interested strategy: never contribute, never condition on opponents’ past behavior, and never attempt reciprocity or punishment.
'''

description_SELFINTERESTED_25 = '''
Play D in every round, regardless of history, observed cooperation counts, round number, or opponent behavior.

Decision rule:
- Round 1: D
- Rounds 2 through r−1: D
- Round r: D
- If any round is skipped or information is incomplete: default to D

Implementation:
```text
for each round t = 1..r:
    choose D
```
'''

description_SELFINTERESTED_26 = '''
State variables:
- `good_streak`: consecutive previous rounds in which at least `ceil(2(n-1)/3)` opponents cooperated
- `bad_streak`: consecutive previous rounds in which at most `floor((n-1)/3)` opponents cooperated
- `cooldown`: rounds remaining in mandatory defection mode, initially `0`

Decision rule for round `t`:

```text
if t == r:
    play D

else if t == 1:
    play C
    initialize good_streak = 0, bad_streak = 0, cooldown = 0

else:
    observe x = number of opponents who cooperated in round t-1

    if x >= ceil(2(n-1)/3):
        good_streak += 1
        bad_streak = 0
    else if x <= floor((n-1)/3):
        bad_streak += 1
        good_streak = 0
    else:
        good_streak = 0
        bad_streak = 0

    if x <= floor((n-1)/3):
        cooldown = 2

    if cooldown > 0:
        play D
        cooldown -= 1
    else if good_streak >= 2:
        play C
    else:
        play D
```

Behavioral interpretation:
- Start with one cooperative probe.
- Defect in the last round.
- Cooperate only after two consecutive highly cooperative rounds by the opponents.
- Defect after any clearly uncooperative round, and stay in defection mode for two rounds before re-evaluating.
- Never continue cooperating through weak or mixed cooperation.
'''

description_SELFINTERESTED_27 = '''
Defect in round 1.

For each round t > 1, let m_{t-1} be the number of opponents who cooperated in the previous round, and define

q = ceil((n - 1) / k)

Decision rule:
- Cooperate in round t if and only if m_{t-1} ≥ q and the same condition held in round t-2 when applicable.
- Otherwise defect.

Hysteresis variant for stability:
- Enter cooperation only after 2 consecutive rounds with m ≥ q.
- Once cooperating, continue cooperating only while the most recent round still satisfies m ≥ q.
- If a round falls below q, defect immediately in the next round and stay defecting until there are again 2 consecutive qualifying rounds.

Last round:
- Defect.

If n = 2:
- Cooperate in round t > 1 exactly when the other player cooperated in the previous round; otherwise defect.

If there is no prior history available for any reason:
- Defect.
'''

description_SELFINTERESTED_28 = '''
Play D in every round, regardless of history, observed cooperation counts, round number, or opponent behavior.

Decision rule:
- If t ∈ {1, …, r}, choose D.
- Never choose C.

Edge cases:
- First round: D.
- Intermediate rounds: D.
- Last round: D.
- If the observed number of cooperators in the previous round is 0, partial, or full: still D.
- If prior rounds show stable cooperation, decline it and continue with D.

State rule:
- Maintain no cooperation threshold, no retaliation state, and no forgiveness state.
- Ignore all history except for recording it; it never changes the action.

Action policy in pseudocode:
```text
for each round t:
    play D
```
'''

description_SELFINTERESTED_29 = '''
Play D in every round, regardless of history, observed cooperation counts, or round number.

Decision rule:
- Round 1: D
- Rounds 2 through r - 1: D
- Round r: D

If the observed number of cooperators in prior rounds is zero, low, high, rising, or falling, the action remains D.

State is unnecessary; no update rule is needed.
'''

description_SELFINTERESTED_30 = '''
Initialize with D.

Let `o_t` be the number of opponents who cooperated in round `t` among the `n-1` opponents.

Define a cooperation threshold
`T = max(1, ceil(n - k))`.

Decision rule for round `t`:

- `t = 1`: play `D`.
- `t = r`: play `D`.
- `t > 1`:
  - compute `m = min(3, t-1)` and `avg = (o_{t-1} + o_{t-2} + ... + o_{t-m}) / m`
  - play `C` if and only if:
    - `o_{t-1} >= T`, and
    - `o_{t-1} >= o_{t-2}` whenever `t >= 3`, and
    - `avg >= T`
  - otherwise play `D`.

Memory reset rule:
- If in any round `o_{t-1} < T`, defect next round.
- Return to cooperation only after observing two consecutive rounds with `o >= T`.

Edge handling:
- For `t = 2`, use only `o_1 >= T`.
- For `t = 3`, use `o_2 >= T` and `o_2 >= o_1`.
- If the observed cooperation level drops sharply from a previously stable cooperative pattern, defect immediately and require the two-round reset before cooperating again.

Behavioral summary:
- Start cautious.
- Cooperate only when the opponents’ recent behavior is already cooperative enough to justify continued participation.
- Defect immediately when cooperation is weak, unstable, or near the end of the game.
'''

description_SELFINTERESTED_31 = '''
Play D in every round.

Decision rule:
- Round 1: D
- Round t > 1: D, regardless of the number of cooperators observed in previous rounds
- Final round: D
- If any round history is missing or ambiguous: D

State dependence:
- Ignore the entire cooperation history
- Do not condition on trends, streaks, or observed cooperation counts
- Do not switch to C for reciprocity, punishment, or goodwill

Operational form:
```text
for each round t = 1..r:
    choose D
```
'''

description_SELFINTERESTED_32 = '''
Round 1: play D.

Maintain a state called trust.

- trust = high only after two consecutive rounds in which every opponent cooperated.
- trust = low otherwise.

For round t = 2 to r - 1:
- Observe x_{t-1}, the number of opponents who cooperated last round.
- If t > 2, also observe x_{t-2}.

Decision rule:
- Play C only if:
  - x_{t-1} = n - 1, and
  - either t = 2 or x_{t-2} = n - 1.
- In every other case, play D.

State update:
- If the above condition holds in the current round, keep trust high.
- If any round has x_{t-1} < n - 1, reset trust to low immediately.

Last round: play D.

Extra edge case:
- If the game ever returns to two straight rounds of unanimous opponent cooperation after a reset, resume the same cooperation rule from that point onward.
'''

description_OPPORTUNISTIC_5 = '''
Track the observed number of cooperating opponents each round, \(x_t\), and maintain an estimate of their cooperation level:
\[
\hat p_t = \frac{1}{t}\sum_{\tau=1}^{t} \frac{x_\tau}{n-1}
\]
with a stronger short-term estimate
\[
\hat p^{(3)}_t = \text{average of } \frac{x_\tau}{n-1}\text{ over the last 3 rounds}
\]
when available.

Decision rule for round \(t\):

1. **Round 1**
   - Play **D**.

2. **Rounds 2 through \(r-1\)**
   - Play **C** if both conditions hold:
     - At least a coalition threshold of opponents cooperated last round:
       \[
       x_{t-1} \ge \left\lceil \frac{n-1}{2} \right\rceil
       \]
     - Cooperation has been stable enough recently:
       \[
       \hat p^{(3)}_{t-1} \ge 0.5
       \]
   - Otherwise play **D**.

3. **Punish exploitation**
   - If the previous round had few cooperators,
     \[
     x_{t-1} < \left\lceil \frac{n-1}{2} \right\rceil,
     \]
     play **D** for the next 2 rounds.
   - If cooperation collapses in two consecutive rounds, play **D** until a round occurs with
     \[
     x_{t-1} \ge \left\lceil \frac{n-1}{2} \right\rceil.
     \]

4. **Exploit reliable cooperation**
   - If the last 2 rounds both had strong cooperation,
     \[
     x_{t-1} \ge \left\lceil \frac{n-1}{2} \right\rceil \quad \text{and} \quad x_{t-2} \ge \left\lceil \frac{n-1}{2} \right\rceil,
     \]
     then cooperate in the next round.
   - Continue cooperating as long as the threshold is met in each most recent round.

5. **Endgame**
   - In the final round, play **D** unless the previous 3 rounds were all above threshold, in which case play **C**.
   - In the last 2 rounds, if cooperation is already stable, keep cooperating; otherwise defect.

Compact pseudocode:

```text
t = 1: play D

for t = 2 to r:
    if t == r:
        if x[t-1], x[t-2], x[t-3] all exist and each >= ceil((n-1)/2):
            play C
        else:
            play D
    else if x[t-1] < ceil((n-1)/2):
        play D for next 2 rounds
    else if last 3-round average cooperation >= 0.5:
        play C
    else:
        play D
```

Behavioral summary:
- Start cautiously.
- Cooperate only when a clear majority of opponents are already cooperating.
- Keep cooperating while cooperation remains stable.
- Defect immediately when cooperation weakens.
- Be hardest to exploit near the end of the game by tightening the cooperation requirement in the final rounds.
'''

description_OPPORTUNISTIC_6 = '''
Initialize a belief score `s = 0` and set `mode = probe`.

For each round `t`:

**1) First round**
- Play `C`.

**2) Update after each round**
- Let `x_t` be the number of opponents who cooperated in round `t`.
- Let `m_t = n - 1` be the number of opponents.
- Compute the observed cooperation rate `q_t = x_t / m_t`.
- Update the running cooperation estimate:
  - `s ← 0.7*s + 0.3*q_t`

**3) Decision rule**
- Let `q̄ = s` be the current estimate of opponent cooperation.
- Play according to the following thresholds:

  - If `q̄ >= 0.80`: play `C`
  - If `0.55 <= q̄ < 0.80`: play `C` only if `x_t >= ceil(0.75 * m_t)`, otherwise play `D`
  - If `0.30 <= q̄ < 0.55`: play `D` unless `x_t = m_t` for two consecutive rounds, in which case play `C`
  - If `q̄ < 0.30`: play `D`

**4) Last round**
- Play `D` unless the last three observed rounds all satisfy `x_t = m_t`, in which case play `C`

**5) Shock handling**
- If the number of opponent cooperators drops by at least half compared with the previous round, immediately switch to `D` for the next two rounds.
- After those two rounds, return to the main decision rule.

**6) Exploitation mode**
- If `x_t = m_t` for three consecutive rounds, enter exploitation mode:
  - Play `C` once every three rounds
  - Play `D` in the other two rounds
- Exit exploitation mode immediately if any round has `x_t < m_t`

**7) Recovery behavior**
- After any round in which you played `D` and observed `x_t = m_t`, cooperate in the next round.
- After any round in which you played `C` and observed `x_t < ceil(0.5 * m_t)`, defect in the next round.

**8) Default tie-breaking**
- If two rules conflict, choose the more defecting action.
'''

description_OPPORTUNISTIC_7 = '''
Maintain a running estimate of the cooperation level and switch between three modes: establish, harvest, and punish.

Let:
- `x_t` = number of opponents who cooperated in round `t`
- `m = n - 1` = number of opponents
- `p_t = x_t / m` = observed opponent cooperation rate in round `t`
- `\bar p_t` = average of `p_1, ..., p_t`

Use these rules:

### Round 1
Play `D`.

### For round t > 1
Compute:
- `recent = p_{t-1}`
- `trend = p_{t-1} - p_{t-2}` if `t >= 3`, else `0`
- `\bar p_{t-1}` from all past rounds

Define cooperation thresholds:
- `high = 1 / k`
- `medium = (1 / k) + 0.15`
- `low = (1 / k) - 0.10`

Decision rule:

#### 1) Exploit strong cooperation
Play `C` if all of the following hold:
- `recent >= medium`
- `\bar p_{t-1} >= high`
- `trend >= 0`

This means the table is reliably cooperative and not collapsing.

#### 2) Opportunistic harvest
Play `D` if:
- `recent < high`

Also play `D` if:
- `recent >= high` but `trend < 0` and `\bar p_{t-1} < medium`

This means cooperation is present but weakening; take the free-rider position.

#### 3) Recovery / re-entry
If the previous round was `D`, return to `C` only when:
- `recent >= medium`
- and at least one of the last two rounds had `p >= medium`

This avoids rejoining after a single noisy cooperative spike.

### Late-game adjustment
Let `L = r - t + 1` be rounds remaining.

#### When `L = 1`
Play `D`.

#### When `L = 2`
Play `D` unless:
- `recent = 1`
- and `\bar p_{t-1} >= high`

If both hold, play `C` in the penultimate round and `D` in the last round.

#### When `L = 3` or `4`
Play `C` only if:
- `recent >= medium`
- `\bar p_{t-1} >= high`
- and the last two rounds were both at or above `high`

Otherwise play `D`.

### Explicit edge handling
- If `n = 2`, treat `high = 1 / k` exactly; cooperate only when the opponent has cooperated in every observed round so far and is still cooperating.
- If no history exists beyond round 1, default to `D`.
- If cooperation observations are tied at the threshold, round upward only for `\bar p`; require strict inequality for `recent`.

### Summary behavior
- Start with `D`.
- Cooperate only after the group has demonstrated sustained cooperation above the profitability threshold.
- Defect immediately when cooperation falls below that threshold or shows clear decline.
- Near the end, shift harder toward `D`, with a brief final cooperation window only when the group is exceptionally stable and fully cooperative.
'''

description_OPPORTUNISTIC_8 = '''
Use a conditional threshold policy with a short probing phase, then a responsive exploitation phase, and a final-round defection switch.

Let:
- `m_t` = number of opponents who cooperated in round `t`
- `f_t = m_t / (n - 1)` = observed opponent cooperation rate
- `H_t` = running average of `f_1 ... f_t`
- `S_t` = cooperation trend over recent rounds, computed as the average of the last `L` values of `f` minus the average of the `L` values before them, with `L = max(1, floor(r/5))`

Decision rule for round `t`:

1. First round:
   - Play `C` if `k > n - 1` is impossible here, so default to `D` only if the environment is not yet known.
   - Use `C` in round 1 to probe the field and encourage early cooperation.

2. Rounds `2` through `r - 2`:
   - Let `baseline = H_{t-1}`.
   - Cooperate if all three conditions hold:
     - `baseline >= 1/2`
     - `f_{t-1} >= 1/2`
     - `S_{t-1} >= 0`
   - Otherwise defect.

3. Opportunistic exploitation rule:
   - If `f_{t-1} >= 2/3`, cooperate even if the baseline is only moderate.
   - If `f_{t-1} < 1/3` for two consecutive rounds, defect for the next two rounds regardless of trend.

4. Last two rounds:
   - Round `r - 1`: cooperate only if `f_{r-2} = 1` and `H_{r-2} >= 2/3`; otherwise defect.
   - Round `r`: defect always.

State update after each round:
- Update `H_t`.
- Update the recent trend window for `S_t`.
- Track consecutive low-cooperation rounds to trigger punishment mode.

Pseudocode:

```text
initialize:
    low_streak = 0
    history = []

for t in 1..r:
    if t == 1:
        play C
    else:
        f_prev = m_{t-1} / (n - 1)
        history.append(f_prev)
        H_prev = average(history)

        if f_prev < 1/3:
            low_streak += 1
        else:
            low_streak = 0

        if t == r:
            play D

        else if t == r - 1:
            if f_prev == 1 and H_prev >= 2/3:
                play C
            else:
                play D

        else if low_streak >= 2:
            play D

        else:
            L = max(1, floor(r / 5))
            recent = average(last L values of history)
            prior  = average(values before last L in history) if enough data else recent
            S = recent - prior

            if f_prev >= 2/3:
                play C
            else if H_prev >= 1/2 and f_prev >= 1/2 and S >= 0:
                play C
            else:
                play D
```

Round-by-round behavior:
- Early rounds: cooperate once to test whether the field is receptive.
- Midgame: stay cooperative only while the observed cooperation rate is at least half and not declining.
- High-cooperation states: continue cooperating and take advantage of strong cooperative pools.
- Low-cooperation states: switch quickly into defection and remain there until cooperation visibly recovers.
- Endgame: stop cooperating in the final round and only cooperate in the penultimate round when cooperation is nearly universal.

Trigger conditions for switching back to cooperation after a defection phase:
- Require `f_{t-1} >= 2/3` for one round, or
- Require two consecutive rounds with `f >= 1/2` and nonnegative trend `S >= 0`.

Persistent exploitation mode:
- If cooperation remains high for at least three consecutive observed rounds, keep cooperating.
- If cooperation drops below the threshold at any point, immediately revert to defection until the recovery conditions are met again.

This makes the strategy patient when the field is cooperative, quick to exploit sustained cooperation, and quick to abandon cooperation when others stop contributing.
'''

description_OPPORTUNISTIC_9 = '''
Round 1: Cooperate.

Maintain:
- `s` = number of rounds seen so far
- `x_t` = number of opponents who cooperated in round `t`
- `m_s` = average opponent cooperation rate over the last `s` rounds: `m_s = (x_1 + ... + x_s) / (s * (n-1))`

Decision rule for round `t >= 2`:

1. Compute:
   - `last = x_{t-1} / (n-1)`  
   - `recent = average of x_{t-1}, x_{t-2}, x_{t-3}` divided by `(n-1)`, using as many of those rounds as exist
   - `trend = recent - previous_recent` when at least 4 rounds are available; otherwise set `trend = 0`

2. Cooperate iff all of the following hold:
   - `last >= 1/2`
   - `recent >= 1/2`
   - `trend >= 0`

3. Otherwise defect.

4. Override to defect in the final round:
   - If `t = r`, play `D`

Adaptive refinements:
- If the previous round had `x_{t-1} = 0`, defect for the next two rounds unless cooperation rebounds to at least half the opponents.
- If the previous three rounds all satisfied `x_j = n-1`, cooperate immediately and keep cooperating until the observed cooperation rate falls below half.

Equivalent compact pseudocode:

```text
if t == 1:
    play C
else if t == r:
    play D
else:
    last = x[t-1] / (n-1)
    recent = average(x[max(1,t-3) .. t-1]) / (n-1)
    trend = 0
    if t >= 5:
        recent_now = average(x[t-3 .. t-1]) / (n-1)
        recent_prev = average(x[t-4 .. t-2]) / (n-1)
        trend = recent_now - recent_prev

    if x[t-1] == 0:
        defect_cooldown = 2

    if defect_cooldown > 0:
        play D
        defect_cooldown -= 1
    else if last >= 0.5 and recent >= 0.5 and trend >= 0:
        play C
    else:
        play D
```

Behavioral mode:
- Start by inviting cooperation.
- Reward sustained cooperation with cooperation.
- Exploit low-cooperation environments by switching to defection quickly.
- Never pay the final-round cost of cooperating.
- Re-enter cooperation immediately when the opponent group’s cooperation becomes consistently high again.
'''

description_OPPORTUNISTIC_10 = '''
Let \(x_t\) be the number of opponents who cooperated in round \(t\).

Set two thresholds from the game parameters:
- \(H = \lceil (n-1)/k \rceil\)
- \(L = \max(0, H-1)\)

Maintain a state variable `mode` in \(\{\text{open}, \text{punish}\}\), initially `open`, and a counter `punish_left = 0`.

Decision rule for round \(t\):

1. **If \(t = r\):** play \(D\).

2. **If \(t = 1\):** play \(C\).

3. **If `mode = punish`:**
   - play \(D\)
   - decrement `punish_left`
   - if `punish_left = 0`, set `mode = open`

4. **If `mode = open` and \(t \ge 2\):**
   - Let \(x_{t-1}\) be the observed opponent cooperation count from the previous round.
   - Let \(\bar{x} = \frac{x_{t-1} + x_{t-2}}{2}\) if \(t \ge 3\), otherwise \(\bar{x} = x_{t-1}\).
   - Play \(C\) iff all of the following hold:
     - \(x_{t-1} \ge H\)
     - \(\bar{x} \ge H\)
     - \(x_{t-1} > L\)
   - Otherwise play \(D\).

5. **Trigger punishment after any round \(t-1\):**
   - If \(x_{t-1} \le L\), set `mode = punish` and `punish_left = 2`.

6. **Recovery from punishment:**
   - While in `punish`, continue defecting until you have observed two consecutive rounds with \(x_t \ge H\); then return to `open`.

Operationally:
- **Cooperate only when the prior behavior of the group is strongly cooperative and stable.**
- **Defect immediately after any weak-cooperation round.**
- **Use a short punishment block to respond to collapse, then reopen only after cooperation is restored.**
'''

description_OPPORTUNISTIC_11 = '''
Play a three-phase contingent strategy: probe early, mirror the current cooperation level, and defect in the endgame if cooperation is not being sustained.

**State variables**
- Let `m_t` be the number of opponents observed to cooperate in round `t`.
- Let `M_t = m_t / (n-1)` be the observed opponent cooperation rate.
- Track `S_t`, the number of rounds so far in which `m_t ≥ ceil((n-1)/2)`.
- Track `L_t`, the length of the current streak of rounds with `m_t = 0`.
- Track `H_t`, the length of the current streak of rounds with `m_t = n-1`.

**Round 1**
- Play `C`.

**Rounds 2 through r-2**
1. If `m_{t-1} = n-1`, play `C`.
2. Else if `m_{t-1} ≥ ceil(0.75·(n-1))`, play `C`.
3. Else if `m_{t-1} ≥ ceil(0.5·(n-1))`, play `C` with probability `0.5`, otherwise play `D`.
4. Else if `m_{t-1} ≥ 1`, play `D`.
5. Else if `m_{t-1} = 0`:
   - If `L_{t-1} ≥ 2`, play `D`.
   - Otherwise, play `C` once every third such all-defect round to test whether cooperation can be restarted:
     - play `C` if `(t mod 3) = 2`, else `D`.

**Endgame: rounds r-1 and r**
- If `m_{t-1} = n-1`, continue playing `C`.
- Else if `m_{t-1} ≥ ceil(0.75·(n-1))` and `S_t` is at least half of the rounds seen so far, play `C`.
- Otherwise play `D`.

**Adjustment after each round**
- Update `L_t`:
  - If `m_t = 0`, increment `L_t`.
  - Otherwise reset `L_t = 0`.
- Update `H_t`:
  - If `m_t = n-1`, increment `H_t`.
  - Otherwise reset `H_t = 0`.

**Decision logic in compact form**
```text
if t = 1:
    C
else if t in {r-1, r}:
    if previous round was unanimous cooperation:
        C
    else if previous round cooperation rate >= 75% and cooperation has been frequent overall:
        C
    else:
        D
else:
    if previous round unanimous cooperation:
        C
    else if previous round cooperation rate >= 75%:
        C
    else if previous round cooperation rate >= 50%:
        C with probability 1/2, else D
    else if previous round cooperation rate >= 1:
        D
    else:
        if all-defect streak has lasted 2+ rounds:
            D
        else:
            C every third all-defect round, otherwise D
```

**Behavioral rule**
- Reward sustained high cooperation immediately.
- Match moderate cooperation conservatively.
- Exploit weak cooperation by defecting.
- Periodically test whether a cooperation regime can be re-established after collapse.
- Stop testing near the end and take the safe payoff unless cooperation is already stable.
'''

description_OPPORTUNISTIC_12 = '''
Round 1: play C.

After each round t, let x_t be the number of opponents who cooperated in round t, and let s_t be the moving cooperation signal over the most recent observed rounds:
- if t = 1, s_t = x_t
- otherwise s_t = 0.7·s_{t-1} + 0.3·x_t

Define the cooperation threshold:
- T = ceil((n-1)/k)

Decision rule for round t+1:
- Play C if s_t ≥ T
- Play D if s_t < T

Exploit rule:
- If the previous round had x_t ≥ T and you played D in that round, keep playing D as long as x_t stays at or above T.
- If the previous round had x_t < T, immediately switch to C for one round only if x_t = T-1 and the moving signal s_t is still at least T; otherwise play D.

Last-round rule:
- In round r, play D unless the last two observed rounds both had x_t ≥ T, in which case play C.

Edge cases:
- If n = 2, then T = 1, so cooperate only when the other player cooperated in the previous round.
- If k is very close to n, keep the same rule; the threshold T automatically becomes low, so cooperate more readily.
- If x_t is unavailable for the first round only, default to C; after that, use the observed counts only.

Operational form:
1. Start with C.
2. Track how many opponents cooperated each round.
3. Cooperate only when the recent cooperation level is at or above the break-even threshold.
4. Defect immediately whenever cooperation falls below threshold.
5. When cooperation is high, defecting is preferred unless maintaining cooperation is necessary to preserve a high observed cooperation level.
'''

description_OPPORTUNISTIC_13 = '''
Use three modes: probe, harvest, and abandon.

Let `s_t` be the number of opponents who cooperated in round `t` among the `n-1` observed opponents.

Define the cooperation threshold:
`H = ceil((n - 1) / k)`

Decision rule:

- **Round 1:** play `C`
- **Round r (last round):** play `D`

For every intermediate round `t` with `1 < t < r`:

1. **Check recent cooperation level**
   - Let `a = s_{t-1}`
   - If `t >= 3`, let `b = s_{t-2}`; otherwise set `b = a`

2. **Abandon weak groups**
   - If `a < H`, play `D`

3. **Stay cooperative when the group is holding**
   - If `a >= H` and `b >= H - 1`, play `C`

4. **Harvest a strong group**
   - If `a >= H + 1` and `b >= H`, play `D`

5. **Default**
   - Otherwise play `D`

Equivalent compact form:

```text
if t = 1: C
else if t = r: D
else:
    if s[t-1] < H: D
    else if s[t-1] >= H+1 and (t<3 or s[t-2] >= H): D
    else: C
```

Operationally:
- start by testing cooperation,
- cooperate only while the observed cooperation level is at or above the threshold,
- defect immediately when cooperation falls below threshold,
- and take an opportunistic free ride whenever the group is stably above threshold by at least one extra cooperator.
'''

description_OPPORTUNISTIC_14 = '''
State variables:
- `mode ∈ {PROBE, COOPERATE, DEFECT}`
- `streak =` number of consecutive rounds with at least the cooperation threshold met
- `T = ceil(n / k)`  
- `H = max(0, T - 1)`  // minimum number of cooperating opponents that signals a viable cooperative environment

Decision rule for round `t`:

1. **Round 1**
   - Play `C`
   - Set `mode = PROBE`

2. **For round t > 1, after observing `x =` number of cooperating opponents in round `t-1`:**

   - If `x >= H`:
     - `streak += 1`
   - Else:
     - `streak = 0`

   - Update mode:
     - If `streak >= 2`, set `mode = COOPERATE`
     - If `streak = 0`, set `mode = DEFECT`
     - If `streak = 1`, keep previous mode

3. **Action by mode**
   - `PROBE`: play `C`
   - `COOPERATE`: play `C`
   - `DEFECT`: play `D`

4. **Opportunistic switching**
   - If in `DEFECT` mode and `x >= H` for two rounds in a row, switch to `COOPERATE`
   - If in `COOPERATE` mode and `x < H` in the current round, switch to `DEFECT` immediately next round

5. **Last round**
   - Play `D`

6. **Long defection runs**
   - If `D` has been played for `L = max(2, ceil(r/4))` consecutive rounds and the observed cooperation count in the latest round is at least `H`, play `C` once as a fresh probe, then return to the normal update rule

Compact pseudocode:

```text
T = ceil(n / k)
H = max(0, T - 1)
streak = 0
d_run = 0

round 1: play C

for t = 2 to r:
    observe x = cooperating opponents in round t-1

    if x >= H:
        streak += 1
    else:
        streak = 0

    if t == r:
        play D
    else if d_run >= max(2, ceil(r/4)) and x >= H:
        play C
        d_run = 0
    else if streak >= 2:
        play C
        d_run = 0
    else if streak == 0:
        play D
        d_run += 1
    else:
        if previous action was C:
            play C
            d_run = 0
        else:
            play D
            d_run += 1
```

Behavioral profile:
- Start by offering cooperation.
- Keep cooperating only while enough opponents are also cooperating.
- Free ride immediately when cooperation weakens.
- Re-test a cooperative environment after sustained defection.
'''

description_OPPORTUNISTIC_15 = '''
Initialize:
- Let `m = n - 1` be the number of opponents.
- Track the last `L` rounds of observed opponent cooperation counts, where `L = min(5, r)`.

Round 1:
- Cooperate.

For each round `t > 1`, let `x_t` be the number of opponents who cooperated in round `t-1`, and let `q = x_t / m` be the observed cooperation rate.

Decision rule:

1. Pure exploitation mode
- If `q = 1`, cooperate.
- If `q ≥ 2/3`, cooperate if you cooperated in the previous round; otherwise defect once to test whether cooperation is stable.
- If `q ≤ 1/3`, defect.

2. Mixed-response mode
- If `1/3 < q < 2/3`, cooperate only if both of the following hold:
  - You cooperated in at least `L-1` of the last `L` rounds, and
  - The average cooperation rate of opponents over the last `L` rounds is at least `1/2`.
- Otherwise defect.

3. Endgame tightening
- If `t ≥ r - 1`, defect unless `q = 1` in the immediately preceding round.
- If `t = r`, cooperate only if all opponents cooperated in round `r-1`; otherwise defect.

Memory update:
- After each round, store `x_t` and your own action.
- Recompute the last-`L` averages using the available history only.

Operational form:

```text
if t == 1:
    play C
else:
    q = x_{t-1} / (n-1)

    if t == r:
        if x_{t-1} == n-1:
            play C
        else:
            play D

    else if t == r-1:
        if x_{t-1} == n-1:
            play C
        else:
            play D

    else if q == 1:
        play C

    else if q >= 2/3:
        if my_action_{t-1} == C:
            play C
        else:
            play D

    else if q <= 1/3:
        play D

    else:
        if (count of my C in last L rounds) >= L-1
           and (average opponent cooperation over last L rounds) >= 1/2:
            play C
        else:
            play D
```

Behavioral pattern:
- Start cooperative to invite reciprocal play.
- Continue cooperating only when opponents repeatedly signal high cooperation.
- Defect immediately against persistent free-riding.
- Use a single-round probe when cooperation is high but not perfect, then exploit sustained cooperation if it holds.
- Tighten to defection near the end unless opponents are fully cooperative in the immediately preceding round.
'''

description_OPPORTUNISTIC_16 = '''
Round 1: Cooperate.

After each round, let x be the number of cooperating opponents observed in that round, and let m = n - 1 be the number of opponents.

Maintain:
- S = cumulative opponent cooperation rate over all completed rounds
- t = number of completed rounds
- p = S / t, the observed opponent cooperation rate

Decision rule for round t + 1:

1. Compute the current cooperation threshold:
   - τ = 1 - 1/k

2. Classify the current environment:
   - High cooperation if p ≥ τ + 0.10
   - Mixed cooperation if τ - 0.10 ≤ p < τ + 0.10
   - Low cooperation if p < τ - 0.10

3. Act as follows:
   - If high cooperation:
     - Cooperate
   - If mixed cooperation:
     - Cooperate if x ≥ ceil(m / 2)
     - Defect otherwise
   - If low cooperation:
     - Defect

4. Opportunistic trigger:
   - If x = m in any round, cooperate in the next round
   - If x ≤ floor(m / 4) in any round, defect for the next 2 rounds
   - If two consecutive rounds satisfy x = 0, defect for all remaining rounds

5. Endgame rule:
   - In the last round, defect unless the previous two rounds both had x = m
   - If the last round is preceded by two full-cooperation rounds, cooperate

Update rule after each round:
- S ← S + x/m
- t ← t + 1
- p ← S/t

Tie-breaking and edge cases:
- If m = 1, treat x = 1 as high cooperation and x = 0 as low cooperation
- If no history exists beyond round 1, use the round-1 action above
- If the observed cooperation rate is exactly on a threshold, choose the more cooperative action in the high or mixed regime, and defect in the low regime

Behavioral pattern:
- Start by signaling willingness to cooperate
- Stay cooperative only while others remain sufficiently cooperative
- Immediately exploit sustained cooperation by continuing to cooperate only when the environment remains favorable
- Rapidly switch to defection once cooperation weakens
- End by harvesting with defection unless the group has shown persistent full cooperation right before the final round
'''

description_OPPORTUNISTIC_17 = '''
Use an adaptive threshold policy with three modes: probe, harvest, and lock-in.

State variables:
- `m_t`: number of opponents who cooperated in round `t`
- `S_t`: exponentially weighted cooperation signal
- `u_t`: cooperation trend over recent rounds

Initialize:
- `S_0 = 0`
- `u_0 = 0`

For each round `t`:

1. First round:
- Play `C`.

2. Update after observing round `t-1`:
- `S_t = 0.7 * S_{t-1} + 0.3 * (m_{t-1} / (n - 1))`
- `u_t = (m_{t-1} - m_{t-2}) / (n - 1)` for `t ≥ 3`, else `0`

3. Decision rule for round `t`:

Play `C` if all of the following hold:
- `S_t ≥ 0.55`
- `m_{t-1} ≥ ceil((n - 1) / 2)`
- `u_t ≥ 0`

Otherwise play `D`.

Edge cases:
- If `t = 2`, use only `S_t` and `m_{t-1}`.
- If `m_{t-1} = 0`, play `D` immediately next round.
- If `m_{t-1} = n - 1`, play `C` next round.
- If cooperation drops by at least `2` opponents from one round to the next, play `D` for the next `2` rounds.

Late-round adjustment:
- In the final `3` rounds, play `C` only if `m_{t-1} = n - 1` or `m_{t-1} ≥ ceil(0.75 * (n - 1))`; otherwise play `D`.

Opportunistic exploitation rule:
- After any round with `m_{t-1} ≥ ceil(0.75 * (n - 1))`, play `C` once more to test whether cooperation persists.
- If cooperation remains at or above that level, continue cooperating.
- If it falls below that level, switch to `D` until the signal recovers.

Full policy:
```text
if t = 1:
    play C
else:
    update S_t and u_t using history

    if t >= r - 2:
        if m_{t-1} = n - 1 or m_{t-1} >= ceil(0.75*(n-1)):
            play C
        else:
            play D
    else if m_{t-1} = 0:
        play D
    else if m_{t-1} = n - 1:
        play C
    else if t = 2:
        if S_t >= 0.55 and m_{t-1} >= ceil((n-1)/2):
            play C
        else:
            play D
    else:
        if S_t >= 0.55 and m_{t-1} >= ceil((n-1)/2) and u_t >= 0:
            play C
        else:
            play D

    if cooperation dropped by at least 2 opponents from the previous round:
        play D for the next 2 rounds
```

Behavioral pattern:
- Start by cooperating to sample the field.
- Continue cooperating only when the group shows sustained, high cooperation.
- Defect immediately on weak, declining, or inconsistent cooperation.
- Re-enter cooperation quickly when the group becomes strongly cooperative again.
- Near the end, cooperate only when cooperation is already very strong; otherwise defect.
'''

description_OPPORTUNISTIC_18 = '''
Let m = n - 1 be the number of opponents.

State variables:
- h_t = number of opponents who cooperated in round t
- s_t = h_t / m
- last = h_{t-1}
- prev = h_{t-2}

Decision rule for round t:

1. Round 1: play C.

2. Last round r: play D.

3. For rounds 2 through r - 1:
   - If last = m and prev = m:
     - play D
     - next round, if h_t ≥ ceil(τm), return to C
   - Else if last < ceil(τm):
     - play D
   - Else if last ≥ ceil(τm):
     - play C

Threshold:
- τ = max(1/2, 1 - 1/k)

Interpretation of the rule:
- Cooperate only when the opponents’ most recent cooperation level is high enough to justify staying in a cooperative state.
- Defect immediately when cooperation drops below the threshold.
- If the table has been fully cooperative for two consecutive rounds, take one opportunistic free ride by defecting once, then re-enter cooperation only if the cooperative level remains at or above the threshold.

Edge handling:
- If m = 1, then τ = 1/2 and the rule reduces to:
  - C in round 1
  - C whenever the other player cooperated last round
  - D whenever the other player defected last round
  - D in the last round
- If last round data is unavailable because t = 1, use the fixed opening move C.
- If cooperation is exactly on the threshold, count it as cooperative enough and play C.

Operational summary:
- Start friendly.
- Stay cooperative only while the observed cooperation rate remains high.
- Punish any drop below the threshold with immediate defection.
- Extract value from sustained full cooperation with a single probing defection.
- Close the game with defection.
'''

description_OPPORTUNISTIC_19 = '''
Initialize a cooperation threshold \(T = \lceil n/k \rceil - 1\). Let \(m_t\) be the number of opponents who cooperated in round \(t\), and let \(M_t\) be the moving average of opponent cooperation over the last \(L=\min(3,r-1)\) rounds, using all observed rounds so far when fewer than \(L\) exist.

Round 1:
- Play \(C\).

Round 2:
- Play \(C\) if \(m_1 \ge T\).
- Otherwise play \(D\).

Rounds \(t \ge 3\), with \(s=t-1\) observed rounds:
1. Compute:
   - \(A = \frac{1}{s}\sum_{\tau=1}^{s} m_\tau\)
   - \(B = \frac{1}{L'}\sum_{\tau=s-L'+1}^{s} m_\tau\), where \(L'=\min(L,s)\)
2. Classify the opponent field:
   - Strongly cooperative if \(A \ge T+1\) and \(B \ge T+1\)
   - Mixed if \(A \ge T\) and \(B \ge T\) but not strongly cooperative
   - Weakly cooperative if \(A \ge T-1\) and \(B \ge T-1\) but not mixed
   - Defective otherwise

Decision rule:
- If strongly cooperative: play \(C\).
- If mixed:
  - play \(C\) if \(m_{t-1} \ge T\)
  - otherwise play \(D\)
- If weakly cooperative:
  - play \(C\) only when \(m_{t-1} \ge T+1\)
  - otherwise play \(D\)
- If defective: play \(D\)

Exploit-and-reward adjustment:
- After any round in which \(m_{t-1} \ge T+1\), enter reward mode for the next round by playing \(C\), even if the long-run average is lower.
- After any round in which \(m_{t-1} \le T-1\), enter exploitation mode for the next round by playing \(D\), and remain in exploitation mode until a round with \(m_\tau \ge T\) occurs.

Endgame rule:
- In the last two rounds, play \(D\) unless the previous two observed rounds both satisfied \(m_\tau \ge T+1\).
- In the final round, if the immediately previous round had \(m_{r-1} \ge T+1\), play \(C\); otherwise play \(D\).

Tie-break rule:
- If the observed history is exactly on the threshold, favor \(C\) early in the game and favor \(D\) late in the game.
- “Early” means before round \(\lceil r/2 \rceil\); “late” means from round \(\lceil r/2 \rceil\) onward.

Compact pseudocode:
```text
if t == 1:
    play C
elif t == 2:
    play C if m1 >= T else D
else:
    compute A and B
    if m[t-1] >= T+1:
        play C
    elif m[t-1] <= T-1:
        play D
    elif A >= T+1 and B >= T+1:
        play C
    elif A >= T and B >= T:
        play C if m[t-1] >= T else D
    elif A >= T-1 and B >= T-1:
        play C if m[t-1] >= T+1 else D
    else:
        play D

if t >= r-1:
    if not (m[t-1] >= T+1 and m[t-2] >= T+1 if t >= 3 else False):
        play D
```

Operational principle:
- Cooperate immediately when the group is clearly cooperative.
- Defect immediately when the group is clearly uncooperative.
- In ambiguous cases, test cooperation with selective \(C\) plays and rapidly switch to \(D\) if cooperation falls below threshold.
- Use the final rounds to harvest against weak cooperation and avoid gratuitous endgame cooperation.
'''

description_OPPORTUNISTIC_20 = '''
Round 1: cooperate.

Maintain:
- `m_t`: number of opponents who cooperated in round `t`
- `s_t`: smoothed cooperation rate among opponents
- `L_t`: last observed cooperation count
- `streak_up`: number of consecutive rounds with increased opponent cooperation
- `streak_down`: number of consecutive rounds with decreased opponent cooperation

Initialize:
- `s_1 = (m_1 + 1) / (n - 1 + 2)` after observing round 1
- `baseline = m_1`
- `mode = exploratory`

Decision rule for round `t+1` after observing round `t`:

1. Update trend:
   - if `m_t > L_t`, increment `streak_up`, reset `streak_down`
   - if `m_t < L_t`, increment `streak_down`, reset `streak_up`
   - if equal, reset both to 0
   - set `L_t = m_t`

2. Update smoothed estimate:
   - `s_t = (sum_{u=1..t} m_u + 1) / (t*(n-1) + 2)`

3. Cooperate in round `t+1` if any of the following holds:
   - `m_t >= ceil((n-1)/2)`  
   - `streak_up >= 2`
   - `s_t >= 0.5` and `m_t >= baseline`
   - `t == r-1` and `m_t >= 1`

4. Defect otherwise.

Special edge rules:
- If opponents fully defect in two consecutive rounds, defect until at least half of opponents cooperate in a round.
- If opponents fully cooperate in any round, cooperate next round.
- If cooperation drops sharply from a cooperative regime, defect immediately for one round; resume cooperation only after cooperation recovers to the threshold above.
- In the final round, cooperate only if the current round shows at least one opponent cooperating and the recent trend is nondecreasing; otherwise defect.

Operational interpretation:
- Start by testing the field with cooperation.
- Keep cooperating while cooperation is widespread or rising.
- Switch to defection when cooperation becomes sparse, unstable, or collapses.
- Re-enter cooperation only after opponents demonstrate enough current or recent cooperation to make exploitation unattractive.

'''

description_OPPORTUNISTIC_21 = '''
Round 1: play D.

For each round t = 2 to r:

- Let H_{t-1} be the number of opponents who cooperated in round t-1.
- Let q_{t-1} = H_{t-1} / (n-1).

Decision rule:
- If t = r: play D.
- Else if t = 2:
  - play C only if H_1 = n-1.
  - otherwise play D.
- Else:
  - play C only if both of the last two rounds were strongly cooperative:
    - H_{t-1} >= ceil(0.9 × (n-1))
    - H_{t-2} >= ceil(0.9 × (n-1))
  - otherwise play D.

Hysteresis for stability:
- Once you switch into cooperation, keep cooperating only while the same two-round condition remains true.
- The moment either of the last two rounds falls below the threshold, switch back to D immediately.

Edge handling:
- If n = 2, replace the 90% threshold with “the opponent cooperated in both of the last two rounds.”
- If there is only one observed round so far, use that single observation as the gate for round 2.
- If the game is in the final round, always defect.

Operationally:
- Default to defection.
- Reward sustained high cooperation by joining it after it has been observed twice in a row.
- Never spend the final round on cooperation.
'''

description_OPPORTUNISTIC_22 = '''
Initialize a cooperation index \(L\) and a retaliation counter \(T\).

Decision rule each round \(t\):

1. Set
\[
\text{net gain from cooperating against current observed cooperation rate} = \frac{k}{n}\cdot m_{t-1} - 1
\]
where \(m_{t-1}\) is the number of opponents who cooperated in the previous round.

2. Cooperate if and only if all of the following hold:
- \(m_{t-1} \ge \lceil (n-1)\cdot \theta_t \rceil\)
- \(T = 0\)
- either \(t \le 2\) and the observed cooperation pattern has not dropped from the prior round, or \(\frac{k}{n}\cdot m_{t-1} > 1\)

3. Otherwise defect.

Use a decreasing cooperation threshold:
\[
\theta_t = 1 - \frac{t-1}{r-1}\cdot \lambda
\]
with \(\lambda \in [0.25, 0.5]\), so the required fraction of cooperating opponents becomes lower as the game approaches the end.

Update rules after each round:

- If at least \( \lceil (n-1)\cdot \theta_t \rceil \) opponents cooperated and you cooperated, increment \(L\).
- If opponent cooperation falls below the threshold, reset \(L = 0\) and set \(T = \max(T, b)\), where \(b = 1\) for a mild drop and \(b = 2\) for a sharp drop.
- Decrease \(T\) by 1 at the start of each round until it reaches 0.

Behavior by phase:

- Round 1: cooperate.
- Round 2: cooperate if round 1 had at least a bare majority of opponent cooperation; otherwise defect.
- Middle rounds: cooperate only when observed cooperation is sufficiently high and no retaliation timer is active.
- Final rounds: defect unless cooperation is still strong enough that the immediate return from cooperating is positive and the recent history has not deteriorated.

Sharp-drop rule:
- If opponent cooperation decreases by at least 2 relative to the previous round, defect for the next 2 rounds.
- If it decreases by 1, defect for the next round.

Recovery rule:
- After any retaliation period, return to cooperation only after one round in which opponent cooperation meets or exceeds the current threshold.

Opportunistic escalation:
- If the last two rounds both met the cooperation threshold, cooperate even if the current round is slightly below threshold, provided \(\frac{k}{n}\cdot m_{t-1} \ge 1\).
- If cooperation has been stable for 3 consecutive rounds, keep cooperating until the observed cooperation count falls below half of the previous round’s count.

Endgame rule:
- For the last \(\max(2,\lfloor r/5 \rfloor)\) rounds, cooperate only if the observed number of cooperating opponents makes cooperation immediately non-worse than defection:
\[
\frac{k}{n}\cdot m_{t-1} \ge 1
\]
and at least half of the opponents cooperated in the previous round.
- Otherwise defect.

Compact pseudocode:

```text
state:
  T = 0
  L = 0
  prev_m = null

for each round t:
  if T > 0:
    action = D
    T -= 1
  else if t == 1:
    action = C
  else:
    theta = 1 - ((t - 1) / (r - 1)) * lambda
    threshold = ceil((n - 1) * theta)

    if t >= r - max(2, floor(r/5)) + 1:
      if (k/n) * prev_m >= 1 and prev_m >= ceil((n - 1)/2):
        action = C
      else:
        action = D
    else if prev_m >= threshold and (k/n) * prev_m > 1:
      action = C
    else if prev_m >= threshold and L >= 2:
      action = C
    else:
      action = D

  observe current m

  if action == C and m >= threshold:
    L += 1
  else if m < threshold:
    L = 0
    if prev_m != null:
      if prev_m - m >= 2:
        T = max(T, 2)
      else if prev_m - m == 1:
        T = max(T, 1)

  prev_m = m
```

Default tuning:
- Set \(\lambda = 0.35\).
- Use 1-round retaliation for minor slippage and 2-round retaliation for sharp slippage.
- Keep the first-round cooperation unconditional, then require visible reciprocity before continuing.
'''

description_OPPORTUNISTIC_23 = '''
Defect in round 1.

Let:
- `m_t` = number of opponents who cooperated in round `t`
- `M_t` = average of `m_1..m_t`
- `S_t` = smoothed cooperation rate, initialized `S_0 = 0`
- update `S_t = 0.7*S_{t-1} + 0.3*(m_t/(n-1))`

Define three regimes from observed opponent cooperation:
- `High`: `S_t ≥ 0.7`
- `Medium`: `0.3 ≤ S_t < 0.7`
- `Low`: `S_t < 0.3`

Decision rule for round `t+1` after observing round `t`:

1. If `S_t = 0` for two consecutive rounds, defect until `S_t > 0`.
2. If `High`:
   - Cooperate if you cooperated in the previous round.
   - If you defected in the previous round and `m_t/(n-1) ≥ 0.8`, cooperate next round.
3. If `Medium`:
   - Cooperate only if `m_t/(n-1) ≥ 0.5` and at least one of the last two rounds had `m ≥ (n-1)/2`.
   - Otherwise defect.
4. If `Low`:
   - Defect.
5. If cooperation collapses sharply, treat it as defection:
   - If `m_t < 0.25(n-1)` and `m_{t-1} ≥ 0.5(n-1)`, defect for the next 2 rounds unless cooperation recovers to at least `0.5(n-1)`.

Late-game rule:
- For rounds `t ≥ r-2`, play:
  - Cooperate only if `m_t/(n-1) ≥ 0.8` and `m_{t-1}/(n-1) ≥ 0.8`
  - Otherwise defect

Tie-breaking and edge cases:
- If `n = 2`, use the same rules with `m_t ∈ {0,1}` and thresholds interpreted as exact cooperation by the opponent.
- If history is too short for a condition, default to defect unless the observed cooperation in the available rounds clearly satisfies the threshold.
- If opponent cooperation is perfect for 3 consecutive rounds, cooperate until the first clear drop below `0.7(n-1)`.

Opportunistic exploitation clause:
- Whenever the observed cooperation rate is `≥ 0.8` and has been stable for at least 2 rounds, cooperate to keep the cooperative stream going.
- Whenever the observed cooperation rate falls below `0.5`, defect immediately and keep defecting until cooperation returns to at least `0.5` for one full round.

Pseudocode:

```
state:
  S = 0
  low_streak = 0
  stable_high_streak = 0
  last_action = D

round 1:
  play D

after observing m_t:
  coop_rate = m_t / (n-1)
  S = 0.7*S + 0.3*coop_rate

  if coop_rate == 0:
      low_streak += 1
  else:
      low_streak = 0

  if coop_rate >= 0.8:
      stable_high_streak += 1
  else:
      stable_high_streak = 0

decision for next round:
  if t >= r-1:
      play C if coop_rate >= 0.8 and previous coop_rate >= 0.8 else D
  else if low_streak >= 2:
      play D
  else if S >= 0.7:
      play C if last_action == C or coop_rate >= 0.8 else D
  else if S >= 0.3:
      play C if coop_rate >= 0.5 and (current_or_previous_round had coop_rate >= 0.5) else D
  else:
      play D

  if stable_high_streak >= 3:
      play C
```


'''

description_OPPORTUNISTIC_24 = '''
Let \(m_t\) be the number of opponents who cooperated in round \(t\).

Define two thresholds:
- \(H = \lceil 0.6\,(n-1)\rceil\)
- \(L = \lfloor 0.4\,(n-1)\rfloor\)

Keep two counters from history:
- \(h\): consecutive rounds ending at \(t-1\) with \(m \ge H\)
- \(\ell\): consecutive rounds ending at \(t-1\) with \(m \le L\)

Decision rule for round \(t\):

1. **Forced defect window**
   - If \(t=1\), play \(D\).
   - If \(t \ge r-1\), play \(D\).

2. **Collapse response**
   - If \(\ell \ge 2\), play \(D\).

3. **Strong-cooperation regime**
   - If \(m_{t-1} \ge H\) and \(h \ge 2\):
     - play \(D\) on the next round if the last action was \(C\),
     - otherwise play \(C\) every third round of the high-cooperation block.
   - Concretely, while the high-cooperation block continues:
     - rounds 1, 2, 5, 8, 11, ... of that block: play \(C\)
     - all other rounds in the block: play \(D\)

4. **Weak-to-moderate cooperation**
   - If \(L < m_{t-1} < H\):
     - play \(C\) only if \(m_{t-2} \ge H\) and you played \(D\) last round
     - otherwise play \(D\)

5. **Low cooperation**
   - If \(m_{t-1} \le L\), play \(D\)

History update after each round:
- if \(m_t \ge H\), increment \(h\), reset \(\ell=0\)
- if \(m_t \le L\), increment \(\ell\), reset \(h=0\)
- otherwise reset both counters to \(0\)

Behavioral pattern:
- start by defecting
- join only when cooperation is already strong and stable
- exploit sustained cooperation by defecting more often than cooperating
- give occasional cooperation inside a strong cooperative block to avoid fully abandoning it
- defect immediately whenever cooperation weakens or becomes erratic
'''

description_OPPORTUNISTIC_25 = '''
Let \(x_t\) be the number of opponents who cooperated in round \(t\), so \(x_t \in \{0,\dots,n-1\}\).

Set a cooperation threshold
\[
T = \left\lceil \frac{n-1}{2} \right\rceil
\]
and a stricter “high-trust” threshold
\[
H = \left\lceil \frac{2(n-1)}{3} \right\rceil
\]

Decision rule:

- Round 1: play \(D\).
- Round \(t>1\), if \(t=r\) (last round): play \(D\).
- Otherwise:
  - Play \(C\) only if both of the following hold:
    1. \(x_{t-1} \ge T\)
    2. either \(x_{t-2} \ge T\) or \(x_{t-1} \ge H\)

  - In every other case, play \(D\).

Operationally:
- One good round is not enough to earn cooperation.
- Two consecutive rounds with at least half the opponents cooperating trigger cooperation.
- A single very strong cooperation round can also trigger cooperation immediately.
- Any weak or collapsing cooperation pattern resets you to \(D\).

Compact pseudocode:

```text
if t == 1 or t == r:
    play D
else:
    if x[t-1] >= T and (x[t-2] >= T or x[t-1] >= H):
        play C
    else:
        play D
```

If you want a slightly more aggressive version, replace \(T\) with \(\lceil (n-1)/3 \rceil\). If you want a stricter version, replace \(T\) with \(\lceil 2(n-1)/3 \rceil\).

Fallback rules:
- If history is too short to check \(x_{t-2}\), require only \(x_{t-1} \ge H\).
- After any round with \(x_t < T\), do not cooperate next round unless the high-trust condition is met.
- If cooperation has been stable for several rounds, keep cooperating until cooperation drops below \(T\).
'''

description_OPPORTUNISTIC_26 = '''
Start with one-round probing, then use an “exploit cooperation, punish stagnation, selectively re-open” rule.

State variables to track after each round t:
- `x_t`: number of opponents who cooperated in round t
- `s_t`: your action in round t
- `m_t`: moving average of opponent cooperation over the last 3 rounds, if available
- `u_t`: consecutive rounds of very low opponent cooperation (`x_t <= 1`)

Decision rule for round 1:
- Play `C`.

Decision rule for round t ≥ 2:
1. Compute the recent cooperation level:
   - If `t = 2`, use `x_{t-1}`.
   - If `t ≥ 4`, use `m_{t-1} = (x_{t-1} + x_{t-2} + x_{t-3}) / 3`.
   - Also note whether the last round had unusually high cooperation: `x_{t-1} ≥ n-2`.

2. Cooperate only if one of these is true:
   - `x_{t-1} ≥ n-2` and `x_{t-2} ≥ n-2`  
     → the group is strongly cooperative; stay in to harvest the public return.
   - `m_{t-1} ≥ (n-1)/2`  
     → cooperation is currently widespread enough to justify joining.
   - `t` is among the last two rounds and `x_{t-1} ≥ 1`  
     → a late re-entry if there is still some cooperation to exploit.

3. Otherwise defect.

Punishment and re-entry logic:
- If `x_{t-1} = 0`, defect immediately next round.
- If `x_{t-1} <= 1` for two consecutive rounds, defect until a round occurs with `x_t ≥ 2`.
- After any round where you cooperate and observe `x_t <= 1`, switch to defect next round.
- After defecting for 2 consecutive rounds, if `x_t ≥ 2`, test with `C` in the next round.

Late-game rule:
- In the final round, cooperate only if `x_{r-1} ≥ n-2`.
- In the last two rounds, never “invest” into rebuilding cooperation unless the previous round already showed strong cooperation.

Compact pseudocode:
```text
Round 1: C

For round t = 2..r:
    if t == r:
        if x[t-1] >= n-2: play C
        else play D
    else if t == r-1:
        if x[t-1] >= n-2 and x[t-2] >= n-2: play C
        else play D
    else:
        if x[t-1] == 0:
            play D
        else if x[t-1] <= 1 and x[t-2] <= 1:
            play D
        else if t >= 4 and (x[t-1] + x[t-2] + x[t-3]) / 3 >= (n-1)/2:
            play C
        else if x[t-1] >= n-2 and x[t-2] >= n-2:
            play C
        else:
            play D
```

Behavioral pattern:
- Probe once.
- Join only when cooperation is already visible.
- Defect immediately when cooperation collapses.
- Re-enter only after clear recovery.
- Harvest high-cooperation phases; do not subsidize weak or unstable groups.
'''

description_OPPORTUNISTIC_27 = '''
Track a running estimate of the group’s cooperation level and play a threshold policy.

State variables:
- `m_t`: number of opponents observed to cooperate in round `t`
- `E_t`: exponentially weighted estimate of opponents’ cooperation rate
- `S_t`: streak of recent rounds with high cooperation
- `L_t`: streak of recent rounds with low cooperation

Initialization:
- Set `E_0 = (n - 1) / 2`
- Set `S_0 = 0`, `L_0 = 0`

After each round `t`, update:
- `E_t = 0.7 * E_{t-1} + 0.3 * m_t`
- If `m_t >= ceil((n - 1) * 0.6)`, increment `S_t = S_{t-1} + 1` and reset `L_t = 0`
- If `m_t <= floor((n - 1) * 0.3)`, increment `L_t = L_{t-1} + 1` and reset `S_t = 0`
- Otherwise, reset both streaks to `0`

Decision rule for round `t + 1`:
1. Cooperate if both conditions hold:
   - `E_t >= ceil((n - 1) * 0.55)`
   - `L_t = 0`
2. Defect otherwise

Edge cases:
- Round 1: cooperate.
- Final 2 rounds: defect unless `m_{t-1} = n - 1` and `m_{t-2} >= n - 2`; otherwise defect.
- After any round with `m_t = 0`: defect for the next 2 rounds.
- After any round with `m_t = n - 1`: cooperate in the next round.
- If cooperation has been sustained for `3` consecutive rounds at or above the high threshold, keep cooperating until `m_t` falls below the high threshold twice in the last 3 rounds.

Opportunistic mode:
- Default to defecting whenever the observed cooperation level is not clearly strong.
- Enter cooperation only when the group is already cooperating at a high level, then continue as long as that cooperation persists.
- The moment cooperation weakens for two rounds inside any three-round window, switch back to defection.

Simple pseudocode:

```text
if t == 1:
    play C
else if t >= r - 1:
    if m_{t-1} == n - 1 and m_{t-2} >= n - 2:
        play C
    else:
        play D
else if m_t == 0:
    play D for next 2 rounds
else if m_t == n - 1:
    play C next round
else if E_t >= ceil(0.55 * (n - 1)) and L_t == 0:
    play C
else:
    play D
```

This makes cooperation conditional on already-rich cooperation, while quickly abandoning groups that stop supporting it.
'''

description_OPPORTUNISTIC_28 = '''
Start by defecting.

Maintain:
- `m_t`: number of opponents who cooperated in round `t`
- `s_t`: your own action in round `t`
- `H_t`: history of observed `m_1..m_t` and your own past actions

Compute a running cooperation index over the last `L` rounds, with `L = min(3, t-1)`:
- `avgC_t = (m_{t-L} + ... + m_{t-1}) / L` when `t > 1`
- if `t = 1`, treat `avgC_t = 0`

Decision rule for round `t`:

1. **First round**
   - Play `D`

2. **Baseline rule after round 1**
   - Play `C` only if the recent cooperation rate is high enough:
     - if `avgC_t >= n/2`, play `C`
     - otherwise play `D`

3. **Opportunistic trigger**
   - If the previous round had strong cooperation, exploit it immediately:
     - if `m_{t-1} >= n-1`, play `D`
     - if `m_{t-1} = n-2`, play `D`
   - If cooperation among opponents is merely moderate, keep defecting until it becomes clearly stable:
     - if `m_{t-1} <= n/3`, play `D`

4. **Recovery/reciprocity rule**
   - If there have been at least two consecutive rounds with `m >= n/2`, play `C`
   - Once you play `C`, continue cooperating only while opponents remain at or above that threshold:
     - if `m_{t-1} >= n/2`, keep `C`
     - otherwise switch to `D`

5. **Endgame**
   - In the final two rounds, defect unless the last two observed rounds both had `m >= n-1`
   - If that condition holds, cooperate in the penultimate round, then defect in the last round

State update after each round:
- Record `m_t`
- If you cooperated and `m_t < n/2`, switch to defecting next round
- If you defected and `m_t >= n/2` for two straight rounds, switch to cooperating next round

Equivalent compact pseudocode:

```text
if t == 1:
    action = D
else:
    if t >= r-1:
        if m_{t-2} >= n-1 and m_{t-1} >= n-1 and t == r-1:
            action = C
        else:
            action = D
    else if m_{t-1} >= n-1:
        action = D
    else if m_{t-1} <= n/3:
        action = D
    else if last two rounds had m >= n/2:
        action = C
    else if avgC_t >= n/2:
        action = C
    else:
        action = D
```

Core behavior:
- default to defection
- cooperate only after sustained, broad cooperation by others
- immediately defect when others’ cooperation weakens
- exploit very high cooperation by defecting
- avoid being trapped into cooperation in the last rounds
'''

description_OPPORTUNISTIC_29 = '''
Round 1: play C.

Maintain:
- `m_t`: number of opponents who cooperated in round `t`
- `s_t`: smoothed cooperation estimate after round `t`
- `p_t`: your own cooperation probability for round `t+1`

Initialize:
- `s_1 = m_1 / (n - 1)`

Update after each round `t`:
- `s_t = 0.7 * s_{t-1} + 0.3 * (m_t / (n - 1))` for `t > 1`

Decision rule for round `t+1`:
- Let `q_t = m_t / (n - 1)` be last-round opponent cooperation rate.
- Let `avg_t = s_t` be the smoothed cooperation level.
- Cooperate if and only if all of the following hold:
  1. `q_t >= 0.5`
  2. `avg_t >= 0.45`
  3. `q_t >= q_{t-1} - 0.15` when `t >= 2`

Otherwise defect.

Escalation rule:
- If `m_t = n - 1` in any round, cooperate in the next round.
- If `m_t <= floor((n - 1)/3)`, defect in the next round.
- If the last two rounds both satisfy `m_t >= ceil(2(n - 1)/3)`, cooperate for the next two rounds unless a round falls below the low-cooperation threshold.

Late-game rule:
- For the last two rounds, defect unless both of the previous two rounds had `m_t >= ceil(2(n - 1)/3)`.
- In the final round, mirror the previous round only if `m_{r-1} = n - 1`; otherwise defect.

Opportunistic adjustment:
- When cooperation is high, keep cooperating to ride the collective surplus.
- The first time cooperation drops below the main threshold, switch immediately to defect.
- After defecting, re-enter cooperation only after one full round with `m_t >= ceil(2(n - 1)/3)`.

Compact pseudocode:

```text
if t = 1:
    play C
else:
    q = m_{t-1} / (n-1)
    avg = 0.7*s_{t-1} + 0.3*q

    if t >= r-1:
        if last two rounds both had m >= ceil(2(n-1)/3):
            play C
        else:
            play D
    else if m_{t-1} = n-1:
        play C
    else if m_{t-1} <= floor((n-1)/3):
        play D
    else if q >= 0.5 and avg >= 0.45 and (t=2 or q >= q_prev - 0.15):
        play C
    else:
        play D
```

If the observed cooperation is consistently high, stay in C and extract the shared gains. If it weakens, move quickly to D and wait for a strong recovery signal before returning to C.
'''

description_OPPORTUNISTIC_30 = '''
State variables:
- Let m_t be the number of opponents who cooperated in round t.
- Let ρ_t = m_t / (n - 1), the observed opponent cooperation rate.
- Let W = min(5, r - 1).
- Let H = 0.8.
- Let L = 0.4.
- Let P = 2 if k ≤ (n + 1) / 2, otherwise P = 1.

Decision rule for round t:

1. If t = 1, play D.

2. If t = r, play D.

3. For 2 ≤ t ≤ r - 1:
   - If any of the last P rounds had ρ ≤ L, play D.
   - Else if the last two rounds both had ρ ≥ H, play C.
   - Else if the weighted average of the last W rounds is at least H, using weights 1, 2, ..., W with the most recent round weighted highest, and the most recent round has ρ ≥ H - 1/(n - 1), play C.
   - Otherwise, play D.

4. Reset rule:
   - After any round with ρ ≤ L, enter a defensive mode for the next P rounds, during which you play D regardless of other signals.

Operational simplification:
- Cooperate only after sustained, recent high cooperation from the others.
- Defect immediately after any clear drop in cooperation.
- Resume cooperation only after the others rebuild a high-cooperation streak.
- Never cooperate in the first round or the last round.
'''

description_OPPORTUNISTIC_31 = '''
Round 1:
- Play C.

State variables after each round t:
- m_t = number of opponents who cooperated in round t
- H_t = cumulative number of opponent cooperations through round t
- q_t = H_t / ( (n - 1) t )  if t ≥ 1
- s_t = number of consecutive recent rounds, ending at t, with m_τ ≥ ceil((n - 1)/2)
- l_t = number of consecutive recent rounds, ending at t, with m_τ ≤ floor((n - 1)/4)

Decision rule for round t + 1, with t ≥ 1:

1. Immediate punishment of low cooperation
- If m_t ≤ floor((n - 1)/4), play D next round.
- If m_t = 0, play D next round.

2. Conditional cooperation under sustained reciprocity
- If m_t ≥ ceil((n - 1)/2) and s_t ≥ 2, play C next round.
- If q_t ≥ 1/2 and m_t ≥ ceil((n - 1)/2), play C next round.

3. Opportunistic exploitation of a cooperative field
- If q_t ≥ 2/3 and m_t ≥ ceil((n - 1)/2) - 1, play D next round.
- If the previous round had m_t ≥ ceil((n - 1)/2) and you played C, but at least one of the last two rounds had m_τ ≤ floor((n - 1)/4), play D next round.

4. Default rule
- Otherwise, play D next round.

Last round:
- Play D unless the previous two rounds both had m_τ ≥ ceil((n - 1)/2), in which case play C.

Special handling:
- If n = 2, replace the majority thresholds above with:
  - cooperate next round only if the opponent cooperated in each of the last two rounds, or if q_t = 1
  - otherwise defect
- If the game is in a recovery phase after defection by opponents, require two consecutive high-cooperation rounds before resuming C.

Compact version:
- Start with C.
- Cooperate only after clear, repeated evidence that most opponents are cooperating.
- Defect immediately after weak cooperation or zero cooperation.
- Once cooperation is established, switch to D whenever the field remains highly cooperative enough to exploit.
- Near the end, defect unless cooperation has been sustained for at least two straight rounds.
'''

description_OPPORTUNISTIC_32 = '''
Round 1: Cooperate if and only if k > 1 and n is small enough that a cooperative start can plausibly be recovered from quickly; otherwise defect. Operationally, set an internal target cooperation rate τ0 = 0.6 and start with C when k/n × n·τ0 ≥ 1/2, equivalently when expected short-run gain from a cooperative opening is at least neutral; otherwise start with D.

For rounds t ≥ 2, keep a running estimate of the opponents’ cooperation rate:
- a_t = number of opponents who cooperated in round t
- ρ_t = a_t / (n - 1)
- m_t = moving average of ρ over the last up to 3 rounds, including t

Use three regimes:

1. Cooperation regime  
Cooperate if:
- m_{t-1} ≥ 0.5, or
- the last round had at least n - 2 cooperators among all players, or
- you defected in the previous round and at least n - 2 players cooperated, signaling a mostly cooperative pool.

2. Exploitation regime  
Defect if:
- m_{t-1} < 0.5, or
- the last round had fewer than (n - 1)/2 cooperators among opponents, or
- two consecutive rounds showed declining cooperation.

3. Recovery regime  
If the game just shifted from low cooperation to high cooperation, cooperate for one round even if your moving average is still borderline. Formally, if a_{t-1} ≥ ceil((n - 1)·2/3) and a_{t-2} ≤ floor((n - 1)/2), play C.

Last-round rule: defect unless the last two rounds each had at least n - 2 cooperative opponents. In that case, cooperate once more to capture the cooperative surplus.

Tie-breaking rule:
- If the estimate is exactly on the threshold, defect.
- If history is too short to compute m_t, use the most recent observed cooperation count only.

Compact policy:
- C when the crowd is cooperatively stable.
- D when the crowd is weakly cooperative, falling, or unstable.
- After one cooperative spike, probe with C once to see whether cooperation is sustained; otherwise return to D.
- In the final rounds, only stay cooperative if the population has already demonstrated durable cooperation; otherwise secure the individual baseline with D.
'''

description_INDIVIDUALISTIC_5 = '''
Round 1: play D.

From round 2 onward, compute the cooperation rate among opponents in the previous round:
- Let x be the number of opponents who played C in round t−1.
- Let m = n−1.
- Let ρ = x / m.

Use three internal states:

1. Exploit
- Play D.
- Enter Exploit when ρ ≤ 1/3.
- Stay in Exploit until ρ ≥ 2/3 for two consecutive rounds.

2. Conditional cooperation
- Play C only if the previous round’s opponent cooperation rate is high.
- Condition: ρ ≥ 2/3.
- Stay in this mode while ρ remains ≥ 2/3.
- If ρ falls below 2/3 in any round, switch immediately to Exploit next round.

3. Punish-collapse response
- If ρ = 0 in any round, play D for the next 2 rounds.
- After those 2 rounds, return to the normal rule above.

Decision rule each round t > 1:
- If the previous two rounds both had ρ ≥ 2/3, play C.
- Else if the previous round had ρ = 0, play D.
- Else if the previous round had ρ ≥ 2/3, play C.
- Else play D.

Late-game rule:
- In the final round, play D unless the previous two rounds both had ρ ≥ 2/3.
- If the previous two rounds both had ρ ≥ 2/3, play C in the final round.

Tie-breaking and thresholds:
- Treat ρ exactly equal to 2/3 as cooperative.
- Treat ρ exactly equal to 1/3 as non-cooperative.
- If n = 2, replace 2/3 with “the opponent cooperated in the previous round” and 1/3 with “the opponent defected in the previous round.”

State update:
- After each round, update using only the observed number of cooperating opponents.
- Ignore individual identities and any hidden history not reflected in the last two observed cooperation rates.

Operational summary:
- Start with D.
- Cooperate only after repeated high cooperation from others.
- Defect immediately after weak or collapsing cooperation.
- Rebuild cooperation only after sustained evidence that the group is cooperating again.
'''

description_INDIVIDUALISTIC_6 = '''
Set a cooperation threshold

\[
H=\left\lceil \frac{(n-1)(n-k)}{n}\right\rceil
\]

and use a two-step confirmation rule.

Decision rules:
- Round 1: play D.
- Round r: play D.
- For each round \(t=2,\dots,r-1\):
  - Let \(q_{t-1}\) be the number of opponents who cooperated in round \(t-1\).
  - Let \(q_{t-2}\) be the number of opponents who cooperated in round \(t-2\) if available.
  - Play C only if all of the following hold:
    1. \(q_{t-1}\ge H\)
    2. \(q_{t-2}\ge H\) when \(t\ge 3\)
    3. \(q_{t-1}\ge q_{t-2}\) when \(t\ge 3\)
  - Otherwise play D.

State update:
- If you played C in round \(t-1\) and \(q_{t-1}\ge H\), remain willing to cooperate.
- If you played C in round \(t-1\) and \(q_{t-1}<H\), immediately revert to D and stay there unless the confirmation rule is met again.

Edge handling:
- If \(r=2\), play D in both rounds.
- If \(n=2\), set \(H=1\); cooperate only after observing the other player cooperate in two consecutive nonterminal rounds.
- If \(k\) is close to \(n\), the threshold becomes low; if \(k\) is close to 1, the threshold becomes high.

Pseudocode:

```text
H = ceil((n - 1) * (n - k) / n)

for t in 1..r:
    if t == 1 or t == r:
        action = D
    else if t == 2:
        if q[t-1] >= H:
            action = C
        else:
            action = D
    else:
        if q[t-1] >= H and q[t-2] >= H and q[t-1] >= q[t-2]:
            action = C
        else:
            action = D
```

Individualistic mindset:
- Never cooperate by default.
- Cooperate only when the observed environment already looks strongly cooperative and stable.
- Stop cooperating immediately when that support weakens.
- Use the final round to defect without exception.
'''

description_INDIVIDUALISTIC_7 = '''
Cooperate only when the observed cooperation level is high enough to make cooperation locally dominant for the next round; otherwise defect.

Let:
- `m_t` = number of opponents who cooperated in round `t`
- `n` = total players
- `p_t = (m_t + c_self,t) / n` = observed fraction of cooperators in round `t` including yourself
- `\hat p_t` = smoothed estimate of the population cooperation rate

Initialize:
- `\hat p_0 = 1/n`

Update after each round:
- `\hat p_t = 0.7 * \hat p_{t-1} + 0.3 * (m_t / (n - 1))`

Decision rule for round `t+1`:
- Compute the cooperation threshold `q = 1 / k`
- Cooperate if `\hat p_t >= q + 0.05`
- Defect if `\hat p_t <= q - 0.05`
- If `q - 0.05 < \hat p_t < q + 0.05`, use a tie-break based on momentum:
  - if `m_t >= m_{t-1}` then cooperate
  - otherwise defect

First round:
- Defect

Early-round probing:
- If `r >= 4`, play `C` in round 2 only if round 1 showed at least `ceil((n-1)/k)` cooperating opponents; otherwise defect
- If round 2 is cooperative, continue cooperating only while the smoothed estimate stays above threshold
- If round 2 is not cooperative, defect until the estimate crosses the threshold again

Last three rounds:
- Defect unless the smoothed estimate is at least `1/k + 0.10`
- In the final round, defect unless the current round’s observed cooperation was clearly above threshold and the last two rounds were nondecreasing in cooperation

Persistent-response rule:
- If cooperation drops by at least `2` opponents compared with the previous round, switch to defect immediately
- Stay defecting for at least one full round after any sharp drop before re-evaluating

Recovery rule:
- If you have defected for two consecutive rounds and observed cooperation rises to at least `ceil((n-1)/k) + 1`, resume cooperation
- If cooperation remains below threshold for three consecutive rounds, keep defecting

Individualistic objective:
- Treat cooperation as a conditional investment, not a norm
- Default to defect
- Cooperate only when the observed cooperation rate is strong enough that continuing to cooperate is expected to be better than free-riding on a collapsing group
- Never punish for its own sake; only adjust your own action in response to the current and recent cooperation level
'''

description_INDIVIDUALISTIC_8 = '''
Play D in every round.

Decision rule:
- Round 1: D
- Any intermediate round t: D
- Final round: D
- If any history is available, ignore it for action selection

Implementation:
```text
For each round t = 1..r:
    choose D
```
'''

description_INDIVIDUALISTIC_9 = '''
**State variables**
- `coop_streak`: consecutive rounds in which the observed number of cooperating opponents was at least `n-2`
- `discipline`: number of rounds remaining in a forced-defect cooldown after a drop in cooperation

**Decision rule each round `t`**
1. If `t = r`, play `D`.
2. Else if `discipline > 0`, play `D` and decrement `discipline`.
3. Else:
   - Let `x` be the number of cooperating opponents observed in round `t-1`.
   - If `x >= n-2`, increment `coop_streak`.
   - Otherwise, set `coop_streak = 0`.

   Then:
   - If `coop_streak >= 2`, play `C`.
   - Otherwise, play `D`.

**Response to cooperation drops**
- If you played `C` in round `t-1` and observe `x <= n-3` opponents cooperating in round `t-1`, set:
  - `coop_streak = 0`
  - `discipline = 2`
- During `discipline`, defect regardless of observed behavior.

**First rounds**
- Round `1`: play `D`.
- Round `2`: play `D` unless round `1` had `n-2` or more cooperating opponents; even then, only start `coop_streak`, do not cooperate yet.
- Round `3` and later: cooperate only after two consecutive rounds of near-universal cooperation by the opponents.

**Last rounds**
- Always defect in round `r`.
- If `r-1` is reached with `discipline > 0`, continue defecting; do not cancel cooldown early.

**Compact pseudocode**
```text
if t == r:
    action = D
elif discipline > 0:
    action = D
    discipline -= 1
else:
    x = observed_cooperators_last_round
    if x >= n - 2:
        coop_streak += 1
    else:
        coop_streak = 0

    if coop_streak >= 2:
        action = C
    else:
        action = D

    if last_round_my_action == C and x <= n - 3:
        coop_streak = 0
        discipline = 2
```
'''

description_INDIVIDUALISTIC_10 = '''
Use an opportunistic threshold strategy with a built-in endgame defection and a recovery rule.

Let:
- \(m_t\) = number of opponents who cooperated in round \(t\)
- \(q_t = m_t/(n-1)\) = observed opponent cooperation rate in round \(t\)
- \(H_t\) = history of observed \(q_1,\dots,q_{t-1}\)
- \(T_t\) = average cooperation rate observed so far, \(T_t = \frac{1}{t-1}\sum_{s=1}^{t-1} q_s\) for \(t>1\)

Decision rule for round \(t\):

1. If \(t = r\), play \(D\).

2. If \(t = 1\), play \(C\) if and only if
   \[
   k \ge n-1.
   \]
   Otherwise play \(D\).

3. For \(1 < t < r\), play \(C\) if and only if both conditions hold:
   - Current cooperation is sufficiently high:
     \[
     q_{t-1} \ge \tau_t
     \]
   - Recent cooperation has not collapsed:
     \[
     T_t \ge \tau_t - \delta
     \]
   where
   \[
   \tau_t = \max\!\left(0,\; 1 - \frac{1}{k}\right) + \frac{1}{4}\left(1 - \frac{t-1}{r-1}\right)
   \]
   and
   \[
   \delta = \frac{1}{2(n-1)}.
   \]

Equivalent operational form:

- Start cautious.
- Cooperate only when opponents have been cooperating at a high enough rate recently.
- Defect immediately after a noticeable drop in cooperation.
- Tighten the cooperation threshold as the game approaches the end.
- Always defect in the final round.

Reset rule after any round where \(q_t < \tau_{t+1}\):
- Set the next-round stance to \(D\) unless the next observed round restores cooperation to at least \(\tau_{t+1}\).

Simplified behavior:

- Early rounds: cooperate only if the group is already behaving cooperatively.
- Midgame: keep cooperating while the observed cooperation rate stays above the threshold.
- If cooperation falls below threshold, defect until cooperation recovers.
- Last round: defect.
'''

description_INDIVIDUALISTIC_11 = '''
Defect in round 1.

From round 2 onward, compute:
- `a_t` = number of opponents who cooperated in round `t`
- `m_t = a_t / (n - 1)` = observed cooperation rate among opponents
- `s_t` = average of `m` over the last up to 3 rounds, including round `t - 1`

Use these rules:

1. Immediate response rule
- If `a_{t-1} = n - 1`, cooperate.
- If `a_{t-1} = 0`, defect.

2. Rolling threshold rule
- If `s_t >= 0.70`, cooperate.
- If `0.40 <= s_t < 0.70`, mirror the recent majority:
  - cooperate if `m_{t-1} > 0.50`
  - defect if `m_{t-1} < 0.50`
  - if `m_{t-1} = 0.50`, defect
- If `s_t < 0.40`, defect.

3. Recovery rule
- After any round in which `a_{t-1} = 0`, defect for the next 2 rounds.
- During recovery, override all other rules with defect.
- If cooperation among opponents reaches `a_{t-1} >= ceil((n - 1) / 2)`, end recovery immediately and resume the rolling threshold rule next round.

4. Late-game rule
- In the final 2 rounds:
  - cooperate only if `a_{t-1} = n - 1`
  - otherwise defect

5. Tie-breaking and missing-history rules
- If fewer than 3 prior rounds exist, average only the available prior rounds.
- Any exact threshold tie is resolved by defect.

Pseudocode:

```text
if round == 1:
    play D
else if in_recovery and recovery_rounds_left > 0:
    play D
    recovery_rounds_left -= 1
else if round > r - 2:
    if a_prev == n - 1:
        play C
    else:
        play D
else:
    if a_prev == 0:
        play D
        recovery_rounds_left = 2
    else:
        s = average(m over last up to 3 prior rounds)
        if a_prev == n - 1:
            play C
        else if s >= 0.70:
            play C
        else if s < 0.40:
            play D
        else:
            if m_prev > 0.50:
                play C
            else:
                play D
```

The strategy is always based only on your own observed history of aggregate cooperation and your own payoff-maximizing response to that history.
'''

description_INDIVIDUALISTIC_12 = '''
Play a conditional threshold strategy with three modes: probe, reciprocate, and exploit.

State variables:
- `m_t`: number of opponents who cooperated in round `t`
- `p_t`: estimated cooperation rate among opponents up to round `t`
- `trend_t`: short-term change in cooperation
- `mode ∈ {probe, cooperate, defect}`

Initialization:
- Round 1: play `C`.

Update after each round `t`:
- Let `m_t` be the observed number of cooperating opponents.
- Update running estimate:
  - `p_t = (m_1 + ... + m_t) / ((n - 1) * t)`
- Define recent average over the last up to 3 rounds:
  - `r_t = average(m_{t-2}, m_{t-1}, m_t) / (n - 1)` using only available rounds
- Define trend:
  - `trend_t = r_t - previous_recent_average`

Decision rule for round `t+1`:

1. First round
- Cooperate.

2. Last round
- Defect.

3. Early rounds: probe and classify
- For rounds 2 through 4:
  - Cooperate if `m_t ≥ ceil((n - 1)/2)`
  - Otherwise defect
- This creates a short test phase to detect whether the field is broadly cooperative.

4. Main rule after the probe phase
- Cooperate if all of the following hold:
  - `p_t ≥ 0.5`
  - `trend_t ≥ -0.1`
  - `m_t ≥ ceil((n - 1)/2)`
- Otherwise defect.

5. Recovery rule
- If you defected in round `t` and `m_t` increases by at least 2 relative to `m_{t-1}`, return to cooperation next round if `m_t ≥ ceil((n - 1)/2)`.
- If cooperation among opponents stays below half for 2 consecutive rounds, defect until the cooperation rate recovers above half in a single round.

6. Stability rule
- If opponents are highly cooperative for 3 consecutive rounds (`m_{t-2}, m_{t-1}, m_t ≥ ceil(2(n - 1)/3)`), cooperate for the next round even if the most recent round dipped slightly.
- If opponents are mostly defecting for 2 consecutive rounds (`m_{t-1}, m_t ≤ floor((n - 1)/3)`), defect for the next round.

7. Endgame taper
- In the final 2 rounds:
  - Cooperate only if the last 2 observed rounds each had `m ≥ ceil(2(n - 1)/3)`
  - Otherwise defect

Compact pseudocode:

```text
if t == 1:
    play C
elif t == r:
    play D
elif t <= 4:
    play C if m_t >= ceil((n-1)/2) else D
else:
    if last_two_rounds_low_coop:
        play D
    elif last_three_rounds_high_coop:
        play C
    elif p_t >= 0.5 and trend_t >= -0.1 and m_t >= ceil((n-1)/2):
        play C
    else:
        play D

if in final 2 rounds:
    play C only if last_two_rounds each had m >= ceil(2(n-1)/3)
    else play D
```

Individualistic posture:
- Never cooperate blindly after sustained defection.
- Never remain locked into defection once broad cooperation is visible.
- Respond only to observed aggregate behavior, not to any presumed identity or group commitment.
- Default to self-protection when the environment is uncertain, and switch to cooperation only when the recent population signal is strong enough to justify it.
'''

description_INDIVIDUALISTIC_13 = '''
Play a self-interested threshold strategy with a short exploration phase, then condition cooperation only on the observed cooperation rate and the round remaining.

Decision rule

- Let `x_t` be the number of opponents who cooperated in round `t`.
- Let `m = n - 1` be the number of opponents.
- Let `p_t = x_t / m` be the observed opponent cooperation rate in round `t`.
- Let `T = ceil(r / 5)` be the exploration length.

Rounds `1..T`:
- Cooperate in round 1.
- In rounds `2..T`, cooperate if the previous round had at least half of opponents cooperating:
  - `C` if `p_{t-1} >= 1/2`
  - `D` otherwise

Rounds `T+1..r-1`:
- Cooperate if `p_{t-1} >= 1/2`
- Defect otherwise

Last round `r`:
- Defect unless at least `ceil(m/2)` opponents cooperated in round `r-1` and the last three observed rounds all had `p >= 1/2`
- Otherwise cooperate only if `p_{r-1} = 1` and `p_{r-2} >= 1/2`
- In every other case, defect

Update rule after each round

- If the previous round’s opponent cooperation rate is at least 1/2, treat cooperation as the default response for the next round.
- If it falls below 1/2, switch immediately to defection.
- If opponent cooperation is volatile, use the most recent round only; do not average across long history except for the last-round rule.

Edge cases

- If `n = 2`, then `m = 1`, so the threshold becomes simple:
  - Cooperate after observing the other player cooperate in the previous round
  - Defect after observing defection
  - Defect in the last round unless the other player has cooperated in each of the last three rounds
- If `r <= 5`, treat all non-initial rounds as follows:
  - Cooperate only after a previous round with `p_{t-1} >= 1/2`
  - Defect in the final round unless the previous two rounds both had `p >= 1/2`
- If the game has only one round left and the recent pattern is mixed, defect

Individualistic mindset

- Start by testing whether cooperation is reciprocated.
- Continue cooperating only while the observed environment supports it.
- Never maintain cooperation out of loyalty, symmetry, or group preference.
- Default to defection whenever cooperation no longer appears immediately advantageous based on observed behavior.
- Use the final rounds to avoid giving up payoff to unreciprocated cooperation.
'''

description_INDIVIDUALISTIC_14 = '''
Initialize:

- `s = 0`  // smoothed cooperation level of opponents
- `mode = "probe"`  // start in defensive mode
- `τ = 1 - k / n`
- `margin = 1 / (2n)`

For round `t = 1`:

- Play `D`.

For each round `t > 1`:

1. Let `x` be the number of opponents who cooperated in round `t-1`.
2. Let `q = x / (n - 1)` be the observed cooperation fraction among opponents.
3. Update the smoothed signal:
   - `s = 0.6 * s + 0.4 * q`

Decision rule:

- Play `C` only if all of the following hold:
  - `t < r`  
  - `s >= τ + margin`
  - `q >= τ`
  - the previous round was not a sharp drop, i.e. `q >= 0.5 * s` before the update, or equivalently cooperation has not collapsed for two consecutive observations

- Otherwise play `D`.

State updates:

- If you play `C` and then observe `q < τ`, switch to `mode = "defect"` for the next two rounds.
- If you play `D` and then observe `q >= τ + margin` for two consecutive rounds, switch back to `mode = "probe"`.

Last round:

- Always play `D`.

Behavioral intent:

- Start by protecting against exploitation.
- Join only when the group is already showing strong, stable cooperation.
- Withdraw immediately when cooperation weakens or becomes erratic.
- Use no identity-based memory, only aggregate history and the current round number.
'''

description_INDIVIDUALISTIC_15 = '''
Start by defecting.

For each round \(t\), let \(x_{t-1}\) be the number of opponents who cooperated in the previous round, and let
\[
\hat p_{t-1} = \frac{x_{t-1}}{n-1}
\]
be the observed opponent cooperation rate. Keep a running average of the last up to 3 rounds:
\[
\bar p_{t-1} = \text{average of } \hat p \text{ over the last } \min(3,t-1)\text{ rounds.}
\]

Decision rule:

- **Round 1:** play \(D\).
- **Rounds 2 to \(r-2\):**
  - Play \(C\) only if all of the following hold:
    1. \(\bar p_{t-1} \ge 0.8\)
    2. \(x_{t-1} \ge x_{t-2}\) and \(x_{t-2} \ge x_{t-3}\) whenever those rounds exist
    3. You have not defected after a prior cooperative probe in the last 2 rounds
  - Otherwise play \(D\).
- **Rounds \(r-1\) and \(r\):** play \(D\).

Probe logic:

- If you ever choose \(C\), treat it as a single probe.
- After a probe, observe the next round:
  - If \(x_t\) does not increase by at least 1 relative to the pre-probe baseline, stop probing and defect for the rest of the game.
  - If it does increase, allow at most one more probe later, but only after at least 2 defecting rounds.

Default posture:

- If the history is noisy, mixed, or insufficient to satisfy the cooperation threshold, defect.
- If observed cooperation falls below \(0.6\) in any 3-round window, defect permanently.
- If observed cooperation reaches \(1.0\) for 3 consecutive rounds before the final two rounds, you may cooperate once every 3 rounds to test whether cooperation is being sustained; otherwise continue defecting.

Individualistic interpretation:

- Treat cooperation as a selective probe, never as a commitment.
- Reward only sustained, broad cooperation from others.
- Exploit cooperative environments by defecting most of the time, and abandon cooperation immediately if the environment weakens.
'''

description_INDIVIDUALISTIC_16 = '''
Play D in round 1.

Maintain a cooperation score for the population:

- Let `x_t` be the number of other players who cooperated in round `t`.
- Let `m = n - 1` be the number of opponents.
- Let `p_t = x_t / m` be the observed opponent cooperation rate.

Use a moving estimate of how cooperative the table is:

- `E_1 = 0`
- For `t > 1`, `E_t = 0.6 * E_{t-1} + 0.4 * p_{t-1}`

Decision rule for round `t`:

- Cooperate iff `E_t >= 1 / k`
- Otherwise defect.

Tie and boundary handling:

- If `k <= 1.2`, cooperate only if `E_t = 1` for two consecutive rounds.
- If `k >= m`, cooperate whenever at least one opponent cooperated in the previous round.
- If `x_{t-1} = 0`, defect next round.
- If `x_{t-1} = m`, cooperate next round.

Endgame rule:

- In the last 2 rounds, defect unless `E_t = 1` and `x_{t-1} = m`.

Shock response:

- If opponent cooperation drops by at least half compared to the previous round, defect for the next 2 rounds.
- After the 2-round defection period, resume the standard decision rule.

Recovery rule:

- If cooperation has been at or above the threshold `1 / k` for 3 consecutive rounds, cooperate for the next round and continue following the threshold rule.

Individualistic mode:

- Never sacrifice current expected payoff to “signal” or to lock in future cooperation.
- Only cooperate when the recent observed cooperation rate is high enough that cooperation is immediately justified by the estimated environment.
- If the history is mixed or unclear, default to defect.

Compact pseudocode:

```text
round 1: D

for round t > 1:
    if t is in the last 2 rounds and not (E_t == 1 and x_{t-1} == m):
        play D
    else if recent_drop_by_half:
        play D for 2 rounds
    else if x_{t-1} == 0:
        play D
    else if k >= m and x_{t-1} > 0:
        play C
    else if k <= 1.2:
        play C only if x_{t-1} == m and x_{t-2} == m
    else if E_t >= 1 / k:
        play C
    else:
        play D
```

Update `E_t` each round from observed opponent cooperation only.
'''

description_INDIVIDUALISTIC_17 = '''
Let \(x_t\) be the number of opponents who cooperated in round \(t\).

Set the cooperation threshold
\[
H = \left\lceil (n-1)\left(1-\frac{1}{k}\right)\right\rceil.
\]

Use three states: testing, cooperation-eligible, and cooldown.

**Round 1**
- Play \(D\).

**Rounds 2 through \(r-2\)**
- Play \(C\) only if all of the following hold:
  - the last two observed rounds each had at least \(H\) cooperating opponents;
  - you are not in cooldown.
- Otherwise play \(D\).

**Last two rounds**
- Play \(D\) in rounds \(r-1\) and \(r\).

**Cooldown rule**
- If in any round \(t\) you played \(C\) and \(x_t < H\), enter cooldown for the next 2 rounds.
- While in cooldown, play \(D\) regardless of observations.
- Exit cooldown only after two consecutive rounds with \(x_t \ge H\).

**State update after each round**
- If \(x_t \ge H\), increase the current “high-cooperation streak” by 1.
- If \(x_t < H\), reset that streak to 0 and start cooldown.

**Equivalent pseudocode**
```text
H = ceil((n-1) * (1 - 1/k))
streak = 0
cooldown = 0

for t in 1..r:
    if t == 1:
        play D
    else if t >= r-1:
        play D
    else if cooldown > 0:
        play D
        cooldown -= 1
    else if streak >= 2:
        play C
    else:
        play D

    observe x_t

    if x_t >= H:
        streak += 1
    else:
        streak = 0
        cooldown = 2
```

This keeps the default position as defecting, joins cooperation only when cooperation is already broad and stable, and immediately withdraws when the observed cooperation level falls.
'''

description_INDIVIDUALISTIC_18 = '''
Set

\[
\tau=\left\lceil (n-1)\left(1-\frac1k\right)\right\rceil
\]

and track, for each past round \(t\), the observed number of cooperating opponents \(g_t\in\{0,\dots,n-1\}\).

Decision rule for round \(t\):

1. **First round**
   - Play **D**.

2. **Last two rounds**
   - Play **D**.

3. **Main phase**
   - If \(g_{t-1}\ge \tau\) and \(g_{t-2}\ge \tau\), play **C**.
   - If \(g_{t-1}\le \tau-2\), play **D**.
   - Otherwise, repeat your previous action.

4. **Switching logic**
   - After any round with \(g_t\ge \tau\), you become eligible to cooperate in the next round.
   - After any round with \(g_t\le \tau-2\), you immediately defect in the next round.
   - If \(g_t=\tau-1\), keep your current stance to avoid reacting to noise.

5. **Edge cases**
   - If \(r=2\), play **D** in both rounds.
   - If \(r=3\), play **D** in round 1, then apply the main-phase rule in round 2, and play **D** in round 3.
   - If \(n=2\), this rule reduces to: cooperate only after the other player has cooperated in two consecutive observed rounds, and defect otherwise.

State form:

- **Default state:** Defect
- **Cooperative state:** Enter only after two consecutive high-cooperation observations
- **Exit from cooperative state:** On the first low-cooperation observation

This keeps cooperation strictly contingent on sustained cooperation by the group, while otherwise staying defection-oriented.
'''

description_INDIVIDUALISTIC_19 = '''
**State variables**

- `x_t`: number of other players who cooperated in round `t`
- `m_t`: moving average of observed cooperation among others
- `s_t`: streak of consecutive rounds with high cooperation
- `q_t`: trust level in `[0,1]`, initialized to `0`

**Initialization**

- Set `q_1 = 0`
- Cooperate in round 1 only if `k > n/2`; otherwise defect

**Update after each round**

Let `x_t` be the observed number of cooperating opponents out of `n-1`.

- Compute cooperation rate among others:
  - `ρ_t = x_t / (n-1)`
- Update moving average:
  - `m_t = 0.7 * m_{t-1} + 0.3 * ρ_t` for `t > 1`
  - `m_1 = ρ_1`
- Update trust:
  - If `ρ_t >= 2/3`, then `q_{t+1} = min(1, q_t + 0.2)`
  - If `ρ_t <= 1/3`, then `q_{t+1} = max(0, q_t - 0.3)`
  - Otherwise `q_{t+1} = q_t`

**Decision rule for round `t`**

Cooperate if and only if all of the following hold:

1. `t < r` is not the last round
2. `q_t >= 0.6`
3. `m_{t-1} >= 0.5` if `t > 1`  
   - for `t = 1`, use the initialization rule
4. `ρ_{t-1} >= 0.5` if `t > 1`
5. The previous round was not a sharp betrayal:
   - if `t > 1` and `ρ_{t-1} <= 1/3`, defect

Otherwise, defect.

**Special round handling**

- **Round 1:**  
  - Cooperate only if `k > n/2`
  - Otherwise defect

- **Middle rounds:**  
  - Cooperate only after sustained observable cooperation from others
  - One weakly cooperative round is not enough

- **Last round:**  
  - Defect unless `q_r = 1` and both `m_{r-1} >= 2/3` and `ρ_{r-1} >= 2/3`

**Short-memory punishment rule**

- If `ρ_t <= 1/3`, defect for the next two rounds regardless of `q`
- Reset this punishment timer only after observing `ρ_t >= 2/3`

**Compact pseudocode**

```text
if t == 1:
    play C if k > n/2 else D
else:
    if punishment_timer > 0:
        play D
    else if t == r:
        play C only if q_t == 1 and m_{t-1} >= 2/3 and ρ_{t-1} >= 2/3
    else:
        play C if (q_t >= 0.6 and m_{t-1} >= 0.5 and ρ_{t-1} >= 0.5) else D

after observing x_t:
    ρ_t = x_t / (n-1)
    m_t = 0.7 * m_{t-1} + 0.3 * ρ_t   # m_1 = ρ_1
    if ρ_t >= 2/3:
        q_{t+1} = min(1, q_t + 0.2)
        punishment_timer = 0
    elif ρ_t <= 1/3:
        q_{t+1} = max(0, q_t - 0.3)
        punishment_timer = 2
    else:
        q_{t+1} = q_t
        punishment_timer = max(0, punishment_timer - 1)
```

**Individualistic posture**

- Never cooperate out of obligation
- Cooperate only when observed cooperation is already broad, stable, and recent
- Defect immediately after collapse, exploitative behavior, or uncertainty
- Prefer self-protection when the group signal is mixed or weakening
'''

description_INDIVIDUALISTIC_20 = '''
Defect in round 1.

Maintain an estimate of the group’s cooperation level from the last two rounds:
- Let `x_t` be the number of opponents who cooperated in round `t`.
- Let `m_t = x_t / (n - 1)` be the observed opponent cooperation rate.

Use the following state:
- `mode ∈ {test, exploit, punish}`
- `baseline = max observed x_t over the last 3 rounds`
- `streak = consecutive rounds with x_t = baseline`

Decision rule:

1. First round
- Play `D`.

2. If in `punish` mode
- Play `D`.
- Stay in `punish` for exactly 2 rounds after a drop in cooperation is detected.
- Then return to `test`.

3. If in `test` mode
- Play `C` only if both conditions hold:
  - `x_{t-1} ≥ ceil((n - 1) / k)` or, equivalently, the previous round had enough opponents cooperating that cooperation was at least break-even.
  - `x_{t-1} ≥ x_{t-2}` when `t ≥ 3`, meaning cooperation was not declining.
- Otherwise play `D`.

4. If in `exploit` mode
- Play `D` unless the last round produced near-full cooperation:
  - cooperate only if `x_{t-1} = n - 1`.
- If full cooperation is observed in two consecutive rounds, keep defecting; do not switch into unconditional cooperation.

Mode updates after each round:
- Set `baseline` to the maximum `x_t` seen in the most recent 3 rounds.
- If `x_t < baseline - 1`, enter `punish` mode for the next 2 rounds.
- If `x_t = n - 1` for 2 consecutive rounds, enter `exploit` mode.
- If `x_t` stays at least `ceil((n - 1) / k)` for 3 consecutive rounds without a drop, remain in `test`; otherwise default to `exploit`.

Last-round rule:
- Always play `D`.

Tie and edge-case handling:
- If `k * x_{t-1} < n - 1`, cooperate is not individually profitable, so play `D`.
- If the history is too short to apply the `x_{t-2}` check, ignore that condition and rely only on the break-even threshold.
- If multiple rules apply, use the order: last-round rule > punish > exploit > test.

Individualistic posture:
- Start by defecting.
- Cooperate only as a selective response to already-established high cooperation.
- Never initiate unconditional cooperation.
- Use cooperation as a probe for strong reciprocity, and immediately return to defection if cooperation weakens.
'''

description_INDIVIDUALISTIC_21 = '''
Round 1: play D.

For each round t = 2 to r:

- Let o_{t-1} be the number of opponents who cooperated in round t-1.
- Let o_{t-2} be the number of opponents who cooperated in round t-2, if it exists.

Play C only if all of the following hold:
1. t < r
2. o_{t-1} ≥ ceil((n-1)/2)
3. If t ≥ 3, then o_{t-1} ≥ o_{t-2}
4. If you cooperated in round t-1, then o_{t-1} ≥ ceil((n-1)/2) again

Otherwise, play D.

Special cases:
- Last round (t = r): always D.
- If r = 2: D in both rounds.
- If n = 2: cooperate only after two consecutive rounds of opponent cooperation, and never in the final round.

Operational form:
- Treat cooperation as a temporary concession, not a commitment.
- Start by defecting.
- Reward only sustained, majority-level cooperation from others.
- The moment observed cooperation falls below majority or starts declining, switch to D and stay there until a fresh two-round streak of majority cooperation appears.
- Never cooperate in the final round.
'''

description_INDIVIDUALISTIC_22 = '''
Use a thresholded conditional policy with a built-in downward adjustment and a terminal defection phase.

State variables:
- `s_t`: number of opponents who cooperated in round `t`
- `m_t`: moving average of observed opponent cooperation over recent rounds
- `q_t`: cooperation threshold for round `t`

Initialization:
- Cooperate in round 1 only if `k * (n - 1) / n > 1` and `n` is small enough that one-round probing is worth the information; otherwise defect.
- Set `q_1 = ceil((n - k) / k) + 1` when cooperating is potentially profitable, and `q_1 = n` when it is not.

Update rule after each round:
- Compute `m_t` as the average of the last `min(3, t)` values of `s`.
- Set
  `q_{t+1} = clamp(q_t + 1{m_t < q_t - 1} - 1{m_t > q_t + 1}, 0, n-1)`
- This makes the threshold stricter when opponents stop cooperating and slightly more permissive when they sustain cooperation.

Decision rule in round `t`:
1. If `t > r - 2`, defect.
2. Else if `s_{t-1} >= q_t`, cooperate.
3. Else defect.

Exact edge handling:
- Round 1:
  - If `k * (n - 1) > n`, cooperate.
  - Otherwise defect.
- If cooperation has been met or exceeded in each of the last two rounds, cooperate one more round even if the current count is just below threshold, as long as `s_{t-1} >= q_t - 1`.
- If two consecutive rounds show low cooperation, define low as `s_{t-1} < q_t - 1`, defect until cooperation recovers to at least `q_t`.

Operational form:
- Start optimistic only when the parameter ratio makes cooperation immediately viable.
- Condition your own cooperation strictly on observed aggregate reciprocity.
- Escalate your threshold after repeated free-riding.
- Stop cooperating near the end to avoid donating when no future response is available.
'''

description_INDIVIDUALISTIC_23 = '''
State variables:
- For each round t, let x_t be the number of opponents who cooperated.
- Let q_t = x_t / (n - 1), the observed opponent cooperation rate.
- Let w = min(3, r - 1), the lookback window.
- Let θ = clamp(1 - 1/k + 1/(n - 1), 0, 1).

Decision rule:
1. Round 1: play D.
2. Round r: play D.
3. For rounds 2 through r - 1:
   - Compute the average opponent cooperation over the last w rounds:
     \[
     \bar q_t = \frac{1}{w}\sum_{s=t-w}^{t-1} q_s
     \]
     using only available past rounds.
   - Compute the recent trend:
     \[
     \Delta_t = q_{t-1} - q_{t-2}
     \]
     if t < 4, treat \Delta_t as 0.
   - Play C if and only if all of the following hold:
     - \bar q_t \ge \theta
     - q_{t-1} \ge \theta
     - \Delta_t \ge 0
   - Otherwise play D.

Reset rule:
- If ever q_t < \theta, return to D immediately for the next round and keep defecting until the above cooperation condition is satisfied again for a full lookback window.

Edge handling:
- If r = 2, play D in both rounds.
- If n = 2, then q_t is either 0 or 1; cooperate only after observing the opponent cooperate in the immediately preceding round.
- If there is a tie at the threshold, defect.
'''

description_INDIVIDUALISTIC_24 = '''
Round 1: play C.

Maintain three running quantities from history:
- `q_t`: number of opponents who cooperated in round `t`
- `m_t = q_t / (n - 1)`: observed cooperation rate among opponents
- `\bar m_t`: exponentially weighted moving average of opponent cooperation, updated after each round:
  `\bar m_t = α m_t + (1 - α)\bar m_{t-1}`, with `α = 0.4`
- `s_t`: streak length of consecutive rounds ending at `t-1` in which `m_t ≥ θ_up`

Use two thresholds:
- `θ_up = 0.55`
- `θ_down = 0.35`

Use a reserve level for endgame:
- `L = max(2, ceil(r / 5))`

Decision rule for round `t > 1`:

1. If `t > r - L`, play D.
2. Else if `m_{t-1} ≥ θ_up` or `\bar m_{t-1} ≥ 0.5`, play C.
3. Else if `m_{t-1} ≤ θ_down`, play D.
4. Else if `s_{t-1} ≥ 2`, play C.
5. Otherwise, play D.

Streak update after observing round `t`:
- If `m_t ≥ θ_up`, set `s_{t+1} = s_t + 1`
- Otherwise set `s_{t+1} = 0`

Interpretation of the state:
- Start cooperatively to test whether the group is willing to sustain cooperation.
- Continue cooperating only when recent observed cooperation is clearly majority-level.
- Defect immediately when cooperation falls into a low band.
- In ambiguous middle cases, require confirmation through a short streak before cooperating again.
- Stop cooperating in the final `L` rounds and secure individual payoff.

Edge cases:
- If `n = 2`, interpret `m_t` as the single opponent’s action: `m_t = 1` if the opponent cooperated, else `0`.
- If `r ≤ L`, then play D from the first round onward except round 1, where you still play C.
- If the opponent cooperation rate is exactly on a threshold, treat `m_t ≥ θ_up` as cooperation-supporting and `m_t ≤ θ_down` as defection-supporting.
- If observations are unavailable for any reason, default to D for that round.

Optional compact pseudocode:

```text
Initialize:
  alpha = 0.4
  theta_up = 0.55
  theta_down = 0.35
  L = max(2, ceil(r/5))
  m_bar = 1
  streak = 0

Round 1:
  play C

For t = 2..r:
  if t > r - L:
    play D
  else if m_prev >= theta_up or m_bar_prev >= 0.5:
    play C
  else if m_prev <= theta_down:
    play D
  else if streak_prev >= 2:
    play C
  else:
    play D

  After observing q_t:
    m_t = q_t / (n - 1)
    m_bar = alpha * m_t + (1 - alpha) * m_bar
    if m_t >= theta_up:
      streak = streak + 1
    else:
      streak = 0
```
'''

description_INDIVIDUALISTIC_25 = '''
Round 1: play D.

After each round, let `m` be the number of opponents who cooperated.

Track:
- `m_prev`: previous round’s opponent cooperation count
- `streak_up`: consecutive rounds where `m` increased
- `streak_down`: consecutive rounds where `m` decreased
- `last_move`: your previous action

Decision rule for round `t > 1`:

1. Compute the cooperation ratio among opponents:
   `q = m / (n - 1)`

2. Cooperate if and only if at least one of these is true:
   - `q >= 0.75`
   - `m >= m_prev + 2`
   - `q >= 0.5` and `streak_up >= 2`

3. Otherwise defect.

Adjustment rules:
- If you cooperated in the previous round and `m` fell by at least 2, switch immediately to D next round.
- If you defected in the previous round and `m` rose by at least 2, test cooperation next round only if `q >= 0.5`; otherwise keep defecting.
- If `m == 0`, always play D.
- If `m == n - 1`, always play C.

Endgame rule:
- In the last 2 rounds, require a stronger condition to cooperate:
  - play C only if `m == n - 1` or `q >= 0.8`
  - otherwise play D

Update after each round:
- If `m > m_prev`, increment `streak_up` and reset `streak_down`
- If `m < m_prev`, increment `streak_down` and reset `streak_up`
- If `m == m_prev`, reset both streak counters to 0
- Set `m_prev = m`

Compact pseudocode:

```text
if t == 1:
    action = D
else if t >= r - 1:
    action = C if (m == n-1 or m/(n-1) >= 0.8) else D
else if m == 0:
    action = D
else if m == n - 1:
    action = C
else if m/(n-1) >= 0.75:
    action = C
else if m >= m_prev + 2:
    action = C
else if m/(n-1) >= 0.5 and streak_up >= 2:
    action = C
else:
    action = D
```

Always treat your own action as independent: never cooperate by default, only after observable cooperation becomes sufficiently strong and stable.
'''

description_INDIVIDUALISTIC_26 = '''
Initialize:
- `mode = DEFECT`
- `coop_streak = 0`
- `avg_coop = 0`  // running average of observed opponent cooperation rate
- `window = min(3, r-1)`

Round 1:
- Play `D`

After each round `t`, observe `x_t =` number of opponents who played `C` in that round.
- Update cooperation rate: `rho_t = x_t / (n - 1)` if `n > 2`; for `n = 2`, `rho_t = x_t`
- Update running average over the last `window` rounds:
  - `avg_coop = mean(rho_{t-window+1} ... rho_t)` using all available rounds if `t < window`
- Update streak:
  - If `rho_t >= 0.75`, increment `coop_streak`
  - Else reset `coop_streak = 0`

Decision rule for round `t+1`:

1. If `t+1 = r`:
   - Play `D`

2. Else if `coop_streak >= 2` and `avg_coop >= 0.7`:
   - Play `C`

3. Else if `avg_coop >= 0.9` and `rho_t >= 0.9`:
   - Play `C`

4. Otherwise:
   - Play `D`

Reversion rule:
- If after cooperating, the next observed `rho_t < 0.5`, immediately switch back to `D` and require a fresh `coop_streak >= 2` before cooperating again.

Edge cases:
- `r = 2`: play `D` in both rounds.
- `n = 2`: treat the single opponent’s action as the cooperation rate.
- If cooperation is inconsistent, never “chase” it; stay with `D`.
- If a cooperative pattern persists for several rounds, allow `C` only as a temporary tactical move, and never on the last round.

Individualistic posture:
- Default to `D`.
- Treat cooperation as a conditional investment only when opponents are already behaving cooperatively in a stable way.
- Exit cooperation immediately when the observed cooperation level weakens.
'''

description_INDIVIDUALISTIC_27 = '''
Start from a default of defection and treat cooperation as a narrow, tactical move.

State variables:
- `h`: the number of consecutive previous rounds in which at least `n-2` opponents cooperated
- `last_high`: whether the previous round met that same threshold

Decision rule for round `t`:

1. If `t = 1`, play `D`.
2. If `t = r`, play `D`.
3. Otherwise:
   - Let `x` be the number of opponents who cooperated in round `t-1`.
   - Let `y` be the number of opponents who cooperated in round `t-2` if that round exists, otherwise set `y = 0`.
   - Update `h`:
     - if `x >= n-2`, then `h = h + 1`
     - else `h = 0`
   - Play `C` only if all of the following are true:
     - `t >= 3`
     - `x >= n-2`
     - `y >= n-2`
     - `h == 2`
   - In every other case, play `D`

Operationally:
- Defect at the beginning.
- Cooperate only after observing two consecutive rounds where the opponent group is almost unanimous in cooperation.
- The moment observed cooperation slips below that level, return to permanent defection until the two-round high-cooperation condition is restored.
- Never cooperate in the final round.
- Never “partially trust” a mixed group; mixed behavior is treated as a defection signal.

Compact pseudocode:

```text
if t == 1 or t == r:
    action = D
else:
    x = opponents_cooperated_last_round
    y = opponents_cooperated_two_rounds_ago if available else 0

    if x >= n-2:
        h += 1
    else:
        h = 0

    if t >= 3 and x >= n-2 and y >= n-2 and h == 2:
        action = C
    else:
        action = D
```

Memory update rule:
- Store only the last two observed cooperation counts and the current streak `h`.
- Ignore identities entirely; respond only to aggregate cooperation levels.

Behavioral principle:
- Never subsidize a weak or mixed group.
- Only enter cooperation when the group has already demonstrated near-unanimous cooperation across consecutive rounds.
- Exit immediately on any deterioration.
'''

description_INDIVIDUALISTIC_28 = '''
Default to defection. Treat cooperation as a strictly conditional investment, never as a commitment.

Decision rules:

- Round 1: play D.
- Round 2 onward, let `m_t` be the number of opponents who cooperated in round `t`, and let `q_t = m_t / (n - 1)` be the observed opponent cooperation rate.

Maintain one internal state:
- `trust = 0` initially
- `stable = false`

Update after each round `t`:
- If `q_t >= 1/2`, increase `trust` by 1.
- If `q_t < 1/2`, set `trust = 0`.
- Set `stable = true` only when `trust >= 2`.
- Set `stable = false` immediately if `q_t < 1/2`.

Play rule for round `t+1`:

1. If `t+1 >= r - 1`, play D.
2. Else if `stable = true` and `q_t >= 1/2`, play C.
3. Else play D.

Edge cases:
- If `r = 2`, play D in both rounds.
- If cooperation collapses in any round, switch back to D immediately and require two consecutive majority-cooperation rounds before cooperating again.
- If the last observed round is exactly at the threshold `q_t = 1/2`, treat it as cooperation and continue only if it is the second consecutive such round.

Behavioral interpretation:
- Start by protecting yourself.
- Only cooperate after observing a sustained majority of the other players cooperating.
- Stop cooperating as soon as the environment stops looking reliably cooperative.
- Near the end, take the sure payoff and defect.
'''

description_INDIVIDUALISTIC_29 = '''
Play D in round 1.

After each round, let s be the number of opponents who cooperated in the previous round, and let p = s / (n - 1), the observed cooperation rate among opponents.

Use this rule:

- Cooperate in round t if all of the following hold:
  1. t > 1
  2. p ≥ 1/2
  3. In the last 2 rounds, at least 1 opponent-cooperation rate was ≥ 1/2
  4. There has not been a streak of 2 consecutive rounds with p = 0

- Defect otherwise.

Adaptive update rule:
- If p = n - 1, cooperate next round.
- If p is between 1/2 and n - 2, keep cooperating only while p does not decrease for 2 consecutive rounds.
- If p < 1/2, defect next round.
- If p = 0 in any round, defect next round and continue defecting until p ≥ 1/2 again.

Endgame rule:
- In the last 2 rounds, defect unless p = n - 1 in the immediately previous round.
- In the final round, defect unless every opponent cooperated in the previous round.

Edge cases:
- If n = 2, cooperate only after the opponent cooperated in the previous round; otherwise defect.
- If r = 2, defect in round 1; in round 2, cooperate only if the first-round opponent cooperation rate was 1.
- If the number of opponents is 0, always defect.

State variables to track:
- last p
- whether the previous round had p ≥ 1/2
- current streak of rounds with p = 0
- current streak of rounds with nondecreasing p

Decision summary:
- Default to defect.
- Only switch to cooperate after clear recent opponent cooperation.
- Immediately revert to defect after weak or absent cooperation.
- Near the end, become strictly harder to satisfy.
'''

description_INDIVIDUALISTIC_30 = '''
Initialize:

- `mode = DEFECT`
- `cooperate_streak = 0`
- `last_q = 0`

For round `t`:

1. If `t == r`, play `D`.
2. If `t == 1`, play `D`.
3. Otherwise, let  
   `q_t = (number of opponents who cooperated in round t-1) / (n-1)`.

4. Update a short memory:
   - `avg3 = average of q` over the last up to 3 observed rounds
   - `stable = 1` if the last two observed cooperation rates differ by at most `1/(n-1)`, else `0`

5. Play `C` only if all of the following hold:
   - `q_t == 1`  
   - `avg3 == 1`
   - `stable == 1`
   - `t <= r - 2`

   Otherwise play `D`.

6. After playing `C`, if the next observed round has `q_{t+1} < 1`, reset immediately to `D` for all later rounds.

Behavioral form:

- Default action is `D`.
- `C` is reserved only for a fully cooperative, stable environment that has persisted for several rounds.
- Any drop in observed cooperation ends cooperation permanently.
- Never cooperate in the first round or the last round.
- If information is incomplete or mixed, choose `D`.
'''

description_INDIVIDUALISTIC_31 = '''
Keep a personal state with four quantities:

- `q_t`: fraction of opponents who cooperated in round `t`
- `s_t`: smoothed cooperation level
- `streak_t`: number of consecutive recent rounds with high cooperation
- `mode ∈ {probe, exploit, cooperate}`

Initialization:
- `mode = probe`
- `s_0 = 0`
- `streak_0 = 0`

For each round `t = 1..r`:

1. Update after observing the previous round:
   - `q_{t-1} = (# opponents who cooperated in round t-1) / (n-1)`
   - `s_{t-1} = 0.7 * s_{t-2} + 0.3 * q_{t-1}` for `t ≥ 2`
   - If `q_{t-1} ≥ 0.6`, then `streak = streak + 1`; otherwise `streak = 0`

2. Decision rule:

   - Round 1: play `D`

   - If `t = r`:
     - play `C` only if both conditions hold:
       - `s_{t-1} ≥ 0.75`
       - `streak ≥ 3`
     - otherwise play `D`

   - If `t` is in the first `min(3, r-1)` rounds:
     - play `D` on round 1
     - play `C` on round 2 only if `q_1 ≥ 0.8`
     - play `C` on round 3 only if `q_1 ≥ 0.8` and `q_2 ≥ 0.8`
     - otherwise play `D`

   - For all middle rounds `2 ≤ t < r`:
     - play `C` if all of the following hold:
       - `s_{t-1} ≥ 0.75`
       - `streak ≥ 2`
       - `q_{t-1} ≥ 0.6`
     - otherwise play `D`

3. Immediate reaction rule:
   - If the previous round had a sharp drop, meaning `q_{t-1} < 0.4`, then play `D` regardless of all other conditions for the next two rounds.

4. Recovery rule:
   - After two consecutive rounds with `q ≥ 0.7`, reset `mode` to the normal decision rule above and allow cooperation again.

Operational interpretation:
- Default to `D`.
- Cooperate only after repeated evidence that most others are cooperating consistently.
- Withdraw cooperation immediately when cooperation collapses.
- Do not continue cooperating late in the game unless cooperation has remained strong and stable.
'''

description_INDIVIDUALISTIC_32 = '''
Let \(m_t\) be the number of opponents who cooperated in round \(t\), and let
\[
\rho_t = \frac{m_t}{n-1}
\]
be the observed opponent cooperation rate.

Maintain a running estimate \(H_t\) of how cooperative the environment has been:
\[
H_t = \begin{cases}
\rho_1 & t=1\\
\frac{1}{2}H_{t-1}+\frac{1}{2}\rho_{t-1} & t\ge 2
\end{cases}
\]

Use two thresholds:
\[
T_{\text{high}} = 0.8,\qquad T_{\text{low}} = 0.4
\]

Decision rule:

- Round 1: play \(D\).
- Round 2: play \(C\) only if \(m_1 = n-1\); otherwise play \(D\).
- Round \(t\ge 3\):
  - play \(C\) if both:
    - \(H_t \ge T_{\text{high}}\), and
    - \(m_{t-1} \ge n-2\)
  - play \(D\) otherwise.

Adjustment for sustained decline:

- If \(m_{t-1} \le \lfloor (n-1)T_{\text{low}} \rfloor\), force \(D\) for the next two rounds.
- While in this forced-defection state, ignore \(H_t\).

Final-round rule:

- In the last round, always play \(D\).

Tie-breaking and edge cases:

- If \(n=2\), replace \(T_{\text{high}}=0.8\) with the exact condition \(m_{t-1}=1\) and \(H_t \ge 1\).
- If there are no prior rounds to average, set \(H_1=\rho_1\).
- If the environment alternates and the moving average sits exactly on a threshold, choose \(D\).

Operational mindset:

- Start by protecting against being the sole contributor.
- Only cooperate after repeated evidence of near-universal cooperation.
- Immediately revert to defection when cooperation visibly weakens.
- Never rely on long trust chains; use observed aggregate behavior only.
'''
