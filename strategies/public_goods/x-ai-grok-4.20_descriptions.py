"""
Strategy descriptions for public_goods.

Generated with:
- Provider: OpenAI
- Model: x-ai/grok-4.20
"""


description_COLLECTIVE_1 = '''
We cooperate in round 1. In every subsequent round we cooperate if and only if every preceding round produced exactly n-1 cooperating opponents; otherwise we defect. When the history contains any round with fewer than n-1 cooperating opponents the defection continues for all remaining rounds including the last.
'''

description_COLLECTIVE_1 = '''
We cooperate in round 1. In rounds 2 to r-1 we cooperate only if every opponent cooperated in the immediately prior round; any shortfall triggers permanent defection through the end of the game. We defect in round r regardless of history. 

if round == 1: C
elif round == r or min_cooperators_ever_observed < n-1: D
else: C
'''

description_COLLECTIVE_2 = '''
We set t = floor(n/k) + 1. Cooperate in round 1. Defect in round r. For 2 ≤ t ≤ r-1, cooperate if and only if total cooperators in round t-1 ≥ t (computed as observed cooperating opponents + 1 if we cooperated in t-1, else + 0); otherwise defect. If r = 1, defect.
'''

description_COLLECTIVE_3 = '''
Our group cooperates in round 1 and in every later round t if every opponent cooperated in round t-1. We defect in round t if any opponent defected in round t-1. When any defection has ever appeared in the history we defect in all remaining rounds including the last. If r is even we insert a single test cooperation in round r/2 regardless of immediate history then resume the same rule on the updated record.
'''

description_COLLECTIVE_4 = '''
Cooperate in round 1. In every later round (including the last), first infer the exact total cooperators in the immediately prior round from the observed count of cooperating opponents plus your own prior action. Cooperate if and only if that total is at least ceil(n/k); otherwise defect. Track only this running threshold against observed history; revert to defection the moment any prior round falls below it and remain there until a later round again meets or exceeds the threshold.
'''

description_COLLECTIVE_5 = '''
Cooperate in round 1. In every subsequent round cooperate if and only if every prior round showed all n-1 opponents cooperating; otherwise defect. Apply this exact rule through round r with no exceptions for final-round unravelling or partial histories. When any defection appears in the observed counts, switch permanently to defect for all remaining rounds.
'''

description_COLLECTIVE_6 = '''
Play C in round 1. In every later round play C exactly when every past round (including the just-observed one) had exactly n cooperators; otherwise play D. When inferring total cooperators, add 1 to the observed opponent count if C was played and add 0 if D was played. The same rule is used without modification in the final round.
'''

description_COLLECTIVE_7 = '''
Cooperate in round 1. In every later round t < r, compute m as the average number of cooperating opponents observed across rounds 1 to t-1; cooperate if and only if m ≥ (n - k) and no prior round had m = 0. Defect in round r and after any round with m = 0. When computing m, add 1 to observed opponents if C was played in that round, add 0 if D was played.
'''

description_COLLECTIVE_8 = '''
Cooperate in round 1. In every later round cooperate exactly when every past round (including the one just observed) had exactly n cooperators, inferred from your own action plus the reported number of cooperating opponents; otherwise defect. This holds for round r as well. When any deviation from n occurs, switch permanently to defect for all remaining rounds.
'''

description_PROSOCIAL_1 = '''
Cooperate in round 1. For each round t ≥ 2, let m be the number of opponents who cooperated in round t-1 and let f = m / (n - 1). Cooperate if f ≥ 1 - (k / n); otherwise defect. Apply the identical rule in round r using the observation from round r-1. When (n-1) divides m exactly or when equality holds in the threshold test, cooperate.
'''

description_PROSOCIAL_2 = '''
Cooperate in round 1. Initialize cooperative_rounds = 0 and defective_rounds = 0. After observing the outcome of any round t, if all n-1 opponents cooperated then increment cooperative_rounds by 1, else increment defective_rounds by 1.

For every round t ≥ 2 (including the final round), cooperate if and only if cooperative_rounds ≥ defective_rounds at the start of the round; otherwise defect. If r = 2 and opponents all defected in round 1, defect in round 2. If any defection occurs the counts update cumulatively, so cooperation resumes only after a sufficient run of subsequent full-cooperation rounds to restore cooperative_rounds ≥ defective_rounds.
'''

description_PROSOCIAL_3 = '''
Cooperate in the first round. In every subsequent round reconstruct the exact total cooperators from the immediate prior round as observed_opponents_cooperating + 1 if you cooperated last round or + 0 otherwise. Cooperate this round exactly when that prior total exceeds n/k; defect otherwise. Apply the identical reconstruction and threshold rule in the final round.
'''

description_PROSOCIAL_4 = '''
Cooperate in round one. In each later round, add the observed number of cooperating opponents to your own contribution (one if you cooperated, zero otherwise) in every past round to obtain the per-round cooperator counts. Compute the average of these counts over all previous rounds. Cooperate if this average is at least n divided by k; otherwise defect. Follow this exactly in the final round too.
'''

description_PROSOCIAL_5 = '''
Cooperate in round 1. In every later round compute the historical opponent-cooperation rate as total observed opponent C actions divided by (current round minus 1) times (n minus 1). Cooperate if this rate is at least (n minus k) divided by (n minus 1); defect otherwise. When the rate exactly equals the threshold or when every past round showed at least one cooperator, still cooperate. In the final round replace the threshold with (n minus k minus 0.5) divided by (n minus 1) and additionally defect unconditionally if zero opponents ever cooperated in any prior round. For n equals 2 treat the observed opponent action from the immediate prior round as the sole input and copy it exactly on the current round.
'''

description_PROSOCIAL_6 = '''
Cooperate in round 1. In each round t from 2 to r-1, cooperate if the observed number of cooperating opponents in round t-1 is at least floor(n/2) and defect otherwise. Defect in round r regardless of history. When n=2, this reduces to copying the single opponent's previous action exactly.
'''

description_PROSOCIAL_7 = '''
Cooperate in round 1. In each subsequent round, including the last, compute the fraction of opponents who cooperated in the immediately preceding round and cooperate exactly when that fraction is at least 0.5 (i.e., opponents_C_last >= 0.5 * (n - 1)); otherwise defect. When multiple prior rounds exist the decision uses only the single most recent observation. If n = 2 this reduces to direct reciprocity on the opponent's prior action.
'''

description_PROSOCIAL_8 = '''
As a prosocial agent I cooperate in round 1. In every subsequent round I compute o_avg = (total opponent cooperations observed so far) / (rounds completed). I cooperate if o_avg ≥ n/k − 1 and defect otherwise. The identical threshold rule is used in the final round with no special case. When o_avg exactly equals the threshold I cooperate. When no history exists the action is cooperate.
'''

description_ALTRUISTIC_1 = '''
Cooperate in round 1. In round t > 1 compute avg = (total opponent cooperations observed in rounds 1 to t-1) / ((t-1) * (n-1)). Cooperate if avg > (n - k) / (n - 1) or if any prior round had all n-1 opponents cooperate; otherwise defect. In round r cooperate if avg > 0.25 regardless of the threshold. If avg equals 0 for any 3 consecutive rounds defect for all remaining rounds including r.
'''

description_ALTRUISTIC_2 = '''
Cooperate in the first round and the last round regardless of history. In rounds 2 to r-1, cooperate if and only if at least one opponent cooperated in the previous round; otherwise defect.
'''

description_ALTRUISTIC_3 = '''
Cooperate if the current round is 1 or r. In any other round, cooperate if at least one opponent cooperated in the previous round; defect only if no opponents cooperated in the previous round. Base each decision solely on the game parameters n, r and the history of opponent cooperation counts from prior rounds.
'''

description_ALTRUISTIC_4 = '''
Cooperate in round 1. For each round t from 2 to r, compute avg_opp_rate as the mean fraction of the n-1 opponents who cooperated across rounds 1 to t-1. Cooperate if avg_opp_rate >= 0.4, otherwise defect. In round r, cooperate if avg_opp_rate >= 0.25 instead. If every prior round had zero cooperating opponents, cooperate with probability 0.25 in the current round. If r=2, always cooperate in round 1 and apply the final-round threshold in round 2.
'''

description_ALTRUISTIC_5 = '''
Cooperate in round 1. For round t > 1, compute the historical opponent cooperation rate as total opponent C observations so far divided by (t-1) * (n-1). Cooperate if that rate ≥ (n-k)/(n-1), otherwise defect. In round r, lower the threshold by half and cooperate if rate ≥ (n-k)/(2(n-1)); if the observed rate is exactly 0 after round 1 and n > 2, still cooperate in round r when k > 1.5. If r = 2, cooperate in round 2 only if at least one opponent cooperated in round 1 or if k > (n+1)/2. When n = 2, replace the threshold with 0.5 and always cooperate in the final round regardless of history.
'''

description_ALTRUISTIC_6 = '''
Cooperate in round 1. In every subsequent round t, let p equal the average over rounds 1 to t-1 of (observed cooperating opponents in that round divided by n-1). Cooperate if p ≥ (n - k)/n and defect otherwise. In round r, apply the identical p-based threshold except when t-1 = 0 or when every prior observation is exactly 0, in which case cooperate. When n = 2, replace the threshold with p ≥ 1/k.
'''

description_ALTRUISTIC_7 = '''
Cooperate in round 1. For each subsequent round t, let f be the fraction of all prior opponent actions that were cooperations (total opponent cooperations observed so far divided by (t-1) * (n-1)). Cooperate if f ≥ (n - k) / (n - 1), otherwise defect. In round r, cooperate if f ≥ (n - k) / (2 * n). If no history exists or all prior observations are zero, cooperate when t ≤ r/2 and defect when t > r/2.
'''

description_ALTRUISTIC_8 = '''
Cooperate in round 1. In rounds 2 to r-1, cooperate if at least one opponent cooperated in the immediately prior round and defect otherwise. Cooperate in round r regardless of history. When multiple prior rounds exist, the decision uses only the single most recent observation; initial absence of history defaults to cooperation.
'''

description_BENEVOLENT_1 = '''
Cooperate in round 1. In every subsequent round compute m = ceil(n / k) - 1 and cooperate if and only if the number of cooperating opponents observed in the immediately prior round is at least m; otherwise defect. Use the identical rule in the final round. When history is empty beyond the opening move, fall back to the round-1 action. After any streak of all-opponent defection, resume cooperation the moment the prior-round count meets or exceeds m.
'''

description_BENEVOLENT_2 = '''
Cooperate in round 1. For each round t > 1, compute the historical average total cooperators (sum of all cooperators across rounds 1 to t-1, divided by t-1). Cooperate if and only if this average >= n/k; otherwise defect. In round r specifically, replace the threshold n/k with n/(k+1). When t=2 and the single prior observation equals exactly n/k, cooperate.
'''

description_BENEVOLENT_3 = '''
Cooperate in round 1. In each subsequent round, retrieve m = number of cooperating opponents observed in the immediately prior round. Compute threshold = ceil(n / k - 1). Cooperate if m >= threshold, otherwise defect. Use the identical rule for round r.
'''

description_BENEVOLENT_4 = '''
Cooperate in round 1. In every subsequent round including the last, cooperate if and only if at least half the opponents cooperated in the immediately prior round (using threshold ⌈(n-1)/2⌉), or if the cumulative opponent cooperation rate across all prior rounds exceeds 75 percent; otherwise defect. Switch to permanent defection for all remaining rounds once every opponent has defected for two consecutive rounds.
'''

description_BENEVOLENT_5 = '''
Play C in round 1. For every round t > 1 let avg = (cumulative count of cooperating opponents across all prior rounds) / ((t-1) * (n-1)). Play C if avg >= 1/k, otherwise play D. Apply the identical rule in round r.
'''

description_BENEVOLENT_6 = '''
Cooperate in round 1. In each subsequent round compute total cooperators in the prior round as own prior action (1 for C, 0 for D) plus the observed count of cooperating opponents. Cooperate if k times that total divided by n is at least 1, otherwise defect. Use the identical rule for the final round. When the prior-round total is unavailable or exactly meets the cutoff after floating-point evaluation, default to cooperate.
'''

description_BENEVOLENT_7 = '''
Cooperate in round 1 and every subsequent round unless the exact count of cooperating opponents from the immediately prior round falls strictly below (n-1)*(k-1)/k, in which case defect for that round only. Track the full history vector of opponent cooperation counts; if that vector shows two or more consecutive observations of m=0, defect for exactly one additional round then revert to the default rule. In the final round cooperate unconditionally regardless of the history vector. When the rule requires a binary choice on a non-integer threshold, round up to the next integer count of opponents before testing.
'''

description_BENEVOLENT_8 = '''
Cooperate in round 1. In each later round compute p as the average fraction of the n-1 opponents that cooperated across all prior rounds (or just the single prior round if round ≤ 3). Cooperate exactly when p ≥ (n - k)/(n - 1); defect when p falls below that value. Cooperate unconditionally for all remaining rounds after any observation of n-1 opponent cooperators. In round r apply the identical p threshold but substitute the history average even if r ≤ 5. If p equals the threshold exactly, cooperate.
'''

description_SELFISH_1 = '''
Defect in the final round. In any earlier round, cooperate if and only if every prior observation showed all n-1 opponents cooperating; otherwise defect. In round 1 (no history), cooperate. After any observation of m < n-1 cooperators, defect in all remaining rounds including the last.
'''

description_SELFISH_2 = '''
Cooperate in round 1. Defect in round r. In any round t where 1 < t < r, cooperate if every prior round had exactly n-1 cooperating opponents and defect otherwise.
'''

description_SELFISH_3 = '''
Cooperate in round 1. For each round t from 2 to r-1, cooperate if total cooperators in round t-1 is at least ceil(n/k), else defect. Defect in round r.
'''

description_SELFISH_4 = '''
Defect unconditionally in round r. Cooperate in round 1. For each round t (2 ≤ t < r), compute avg_c as the average of (own prior action + observed opponent cooperators) over rounds 1 to t-1. Cooperate in t if avg_c > n/k, otherwise defect. If r = 2 then the pattern simplifies to cooperate then defect. If opponent cooperation has been zero in every prior round then defect.
'''

description_SELFISH_5 = '''
Cooperate in round 1. For rounds 2 to r-1, cooperate exactly when every prior round had exactly n-1 opponents cooperating; otherwise defect. Defect in round r regardless of history. If any round has fewer than n-1 opponents cooperating after a C move, defect in all remaining rounds.
'''

description_SELFISH_6 = '''
Defect in round r no matter what. Cooperate in round 1. In each round t (1 < t < r) cooperate exactly when every prior round showed exactly n-1 cooperating opponents; otherwise defect.

if round == r:
    play D
elif round == 1:
    play C
elif all(observed_opponent_cooperators[s] == n-1 for s in 1..round-1):
    play C
else:
    play D
'''

description_SELFISH_7 = '''
Cooperate in round 1. Defect in every last round. In rounds 2 through r-1, cooperate exactly when every prior observation showed all n-1 opponents cooperating; defect on the first observation of any opponent defection and defect in all subsequent rounds. When the history contains mixed cooperation rates, compute the cumulative fraction f of opponent cooperation slots across all prior rounds and cooperate only if f = 1.0.
'''

description_SELFISH_8 = '''
Cooperate in round 1. For rounds 2 through r-1, cooperate if and only if all n-1 opponents cooperated in the immediately prior round; otherwise defect. Defect in round r regardless of history.
'''

description_SELFINTERESTED_1 = '''
Cooperate in round 1. For round t in 2..r-1, compute total cooperators in round t-1 as (opponents who cooperated in t-1) + (1 if you cooperated in t-1 else 0); cooperate in t exactly when that total > n/k, otherwise defect. Defect in round r regardless of history. If r=2, this reduces to cooperate in round 1 and defect in round 2. When multiple prior rounds exist, base the decision solely on the immediate prior round's total.
'''

description_SELFINTERESTED_2 = '''
Cooperate if the current round is not the last and all opponents cooperated in every prior round (vacuously true with no prior rounds). Defect in the last round and in any earlier round where any defection has ever been observed among the opponents.
'''

description_SELFINTERESTED_3 = '''
Cooperate in round 1. In each round t where 1 < t < r, cooperate if and only if m_s = n-1 for every prior round s < t; otherwise defect. Defect in round r regardless of observed history.

Pseudocode:
```
if t == 1:
    play C
elif t == r:
    play D
else:
    if min(m_1 ... m_{t-1}) == n-1:
        play C
    else:
        play D
```
'''

description_SELFINTERESTED_4 = '''
Cooperate in round 1. Defect in round r. For each round t from 2 to r-1, cooperate if and only if the number of cooperating opponents observed in round t-1 is at least ceil((n-1)/2); otherwise defect. In case of exact tie at exactly (n-1)/2 when n is even, cooperate.
'''

description_SELFINTERESTED_5 = '''
Cooperate in round 1. Always defect in round r. In any round t (2 ≤ t < r), first reconstruct the exact total cooperators from the prior round as (observed cooperating opponents + 1) if C was played then or (observed cooperating opponents) if D was played then. Cooperate in t only if that reconstructed total met or exceeded ceil(n/k) in every prior round; otherwise defect permanently from that point forward.
'''

description_SELFINTERESTED_6 = '''
Cooperate in round 1. Defect in round r. In each round t (1 < t < r), let m be the number of opponents who cooperated in round t-1; cooperate if and only if (k * (m + 1)) / n > 1, otherwise defect. If m is unavailable (first round) or if cumulative history shows m = 0 across all prior rounds, defect. When multiple histories are possible, use only the immediate prior round's m for the threshold check.
'''

description_SELFINTERESTED_7 = '''
Defect in round r. Cooperate in round 1. In each round t (1 < t < r) cooperate if and only if the number of cooperating opponents observed in every prior round equals exactly n-1; otherwise defect. If any deviation from n-1 cooperating opponents occurs in round s, defect in all rounds after s regardless of later observations.
'''

description_SELFINTERESTED_8 = '''
Cooperate in round 1. For rounds 2 to r-1, cooperate exactly when the number of cooperating opponents from the immediately prior round >= ceil((n-1)/k); otherwise defect. Defect in round r.

if current_round == 1:
  return C
elif current_round == r:
  return D
elif opponent_cooperators_prev >= ceil((n-1)/k):
  return C
else:
  return D
'''

description_OPPORTUNISTIC_1 = '''
Cooperate in round 1. Defect in round r. In each round t from 2 to r-1, compute total_prev = (1 if cooperated in t-1 else 0) + observed cooperating opponents in t-1, then cooperate if total_prev >= ceil(n/k) and defect otherwise.

if round == 1:
    return C
elif round == r:
    return D
else:
    total_prev = (1 if prev_self == C else 0) + prev_opponent_cooperators
    return C if total_prev >= ceil(n / k) else D
'''

description_OPPORTUNISTIC_2 = '''
Cooperate in round 1. For rounds 2 to r-1 compute avg_f as total observed cooperating opponents across prior rounds divided by (prior rounds × (n-1)). Cooperate if avg_f > 1/k, otherwise defect. Always defect in round r. After any two consecutive rounds with zero observed cooperating opponents, defect in every remaining round.
'''

description_OPPORTUNISTIC_3 = '''
Cooperate in round 1. Defect in round r. In rounds 2 to r-1, cooperate exactly when the number of cooperating opponents in round t-1 is at least n/k - 1 (using the observed count of the other n-1 players); otherwise defect. When computing the threshold, treat n/k - 1 as a real number so that non-integer values implicitly require the smallest integer m satisfying the inequality.
'''

description_OPPORTUNISTIC_4 = '''
In round 1 always cooperate. In every round t where 1 < t < r, cooperate exactly when both (a) the immediately prior round had at least ceil((n-1)/2) cooperating opponents and (b) the running average of cooperating opponents across all prior rounds exceeds (n-1)*(k/n); otherwise defect. In round r always defect. After any round with exactly 0 cooperating opponents, defect unconditionally for the next min(2, r-t) rounds before resuming the above rule. When n=2 the same thresholds apply with no special casing.
'''

description_OPPORTUNISTIC_5 = '''
Cooperate in round 1. Always defect in round r. In rounds 2 to r-1, cooperate only if every prior round showed the maximum possible number of opponent cooperators (n-1 if you cooperated, n if you defected); otherwise defect for the remainder of the game. If any round yields fewer than n-2 opponent cooperators, defect in all subsequent rounds regardless of later signals. When k > 1.5, lower the sustained-cooperation threshold to n-2 opponent cooperators before triggering permanent defection.
'''

description_OPPORTUNISTIC_6 = '''
Start by cooperating in round 1. In each subsequent round before the last, cooperate if and only if the number of cooperating opponents observed in the previous round exceeds n - k. Always defect in the final round. Switch to unconditional defection for all remaining rounds once two consecutive prior rounds showed zero cooperating opponents.

if round == 1:
  return C
if round == r or consecutive_zeroes >= 2:
  return D
if prev_opponents_cooperating > n - k:
  return C
return D
'''

description_OPPORTUNISTIC_7 = '''
In each round t, play C if t < r and n-1 opponents cooperated in every past round; otherwise play D. (The condition holds vacuously in round 1, so begin with C. Track the exact count of cooperating opponents after each round to evaluate the condition for all subsequent decisions.)
'''

description_OPPORTUNISTIC_8 = '''
Cooperate in round 1. In each round t (2 ≤ t < r), cooperate if and only if the number of cooperating opponents in round t-1 strictly exceeds (n-1)/2; otherwise defect. Defect in every action in round r. When n=2 this reduces to copying the single opponent's prior move in all non-final rounds. If r=2 then simply cooperate then defect.
'''

description_INDIVIDUALISTIC_1 = '''
Cooperate if the current round is not the last and every previous round had total cooperators exactly equal to n (computed as observed cooperating opponents plus 1 if C was played that round, else plus 0). Otherwise defect. This covers round 1 (vacuously no prior defections, so cooperate unless r=1), the last round (always defect regardless of history), and all intermediate cases (permanent switch to D on the first observed total below n).
'''

description_INDIVIDUALISTIC_2 = '''
Cooperate in round 1. Defect in round r. In rounds 2 ≤ t < r, compute p as the fraction of opponents who cooperated in round t-1 (observed count divided by n-1). Cooperate if p > 1 - (k/n), otherwise defect. On exact equality to the threshold, cooperate only if the cumulative cooperators across all prior rounds is even. When t=2 and no prior opponent data exists beyond round 1, use own round-1 action as the baseline: cooperate only if you cooperated in round 1 and assume symmetric reciprocity.
'''

description_INDIVIDUALISTIC_3 = '''
Cooperate in round 1. In rounds 2 to r-1, cooperate if the number of cooperating opponents in the immediately prior round is at least floor(n/k); otherwise defect. Defect in round r.
'''

description_INDIVIDUALISTIC_4 = '''
Cooperate in round 1. Defect in round r. In each round t (2 ≤ t ≤ r-1) cooperate if and only if every one of the n-1 opponents cooperated in round t-1; otherwise defect and continue defecting in all future rounds.
'''

description_INDIVIDUALISTIC_5 = '''
Cooperate in round 1. Defect in round r. In every round t where 1 < t < r, first reconstruct total cooperators in round t-1 by adding the observed cooperating opponents to 1 if C was played in t-1 (or 0 if D). Let m_min = floor(n / k) + 1. Play C in t exactly when total cooperators in t-1 >= m_min and no prior round has ever fallen below m_min; otherwise play D and lock in permanent defection for all remaining rounds. If observed opponents equal n-1 and self played C then treat the current round as fully cooperative and reset the lock only after two consecutive fully-cooperative rounds.
'''

description_INDIVIDUALISTIC_6 = '''
Cooperate in round 1. Defect in round r regardless of prior observations. In rounds 2 to r-1, let m be the number of cooperating opponents observed in the immediately prior round: cooperate if m >= ceil((n-1)/2), otherwise defect. Once a round with m < ceil((n-1)/2) occurs, defect in every subsequent round up to and including r. If r=2, cooperate in round 1 and defect in round 2.
'''

description_INDIVIDUALISTIC_7 = '''
Cooperate in round 1. Defect in round r. In each round t (1 < t < r), let m be the number of opponents who cooperated in round t-1. Cooperate if m >= n - k, otherwise defect. If multiple rounds remain and m ever drops below n - k, defect in all subsequent rounds including r.
'''

description_INDIVIDUALISTIC_8 = '''
Defect in the final round. In every earlier round, cooperate exactly when all previous observations showed every opponent cooperating; otherwise defect. Cooperate in round 1, as no history exists.
'''
