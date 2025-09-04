"""
Strategy descriptions for CommonPoolDescription.

Generated with:
- Provider: OpenAI
- Model: o4-mini
"""


description_COOPERATIVE_1 = '''
Below is a “cooperative‐minded’’ trigger strategy.  It never defects unless it has been defected upon, and once a defection occurs anywhere it punishes by defecting for the rest of the game (i.e. a grim‐trigger).  This simple rule is easy to implement, transparent to the other players, and – by threatening harsh, irrevocable punishment – can sustain cooperation against a wide variety of independent strategies.

Strategy name: Grim-Trigger Common-Pool Cooperation

State variables (for each player i):
  ever_defected_flag ← false

Decision rule for player i in round t (1 ≤ t ≤ r):

  if t = 1 then
    // First round: set the tone by cooperating
    play C
  else
    if ever_defected_flag = true then
      // We are already in punishment mode: defect forever
      play D
    else
      // No defection has been seen so far
      // Cooperate now, but first check last round’s actions
      if ∃ j ≠ i such that player j played D in round t−1 then
        // We just witnessed a defection → switch to punishment
        ever_defected_flag ← true
        play D
      else
        // Everyone cooperated last round: continue cooperating
        play C
      end if
    end if
  end if

Updating the defection flag:
  After the simultaneous play in each round, each player observes the full profile of actions.
  If in that round any action = D, then set ever_defected_flag ← true.

Comments:

1. Cooperate until defection.  
   • Round 1: Unconditional C.  
   • In any round t > 1, if we and all others have cooperated in every previous round, we play C again.

2. Grim trigger.  
   • The moment any player is observed defecting (playing D), we set ever_defected_flag.  
   • For the rest of the game (including the current round where we first detect it), we play D every round.  

3. Edge‐cases:
   – First round: always C, since there is no history.  
   – Last round: if no defection has ever been seen, we play C one final time; otherwise we remain in punishment (D).  

4. Cooperative mindset:
   – By cooperating first and conditionally thereafter, we reward full‐group cooperation with the highest joint‐sustainable harvest (stock remains high).  
   – The threat is credible because any defection triggers permanent punishment—opponents know that by defecting they lose all future cooperative payoffs.  

5. Why it works in a heterogeneous‐strategy tournament:
   – Against unconditional defectors: you avoid being suckered repeatedly.  
   – Against naive or mixed strategies that are willing to cooperate but sometimes slip: the threat of a permanent switch to D is strong, so many will learn to cooperate to avoid losing future rounds.  
   – Against other trigger‐type strategies: cooperation is established immediately and maintained.

Pseudocode (compact):

  initialize ever_defected_flag ← false

  for t in 1…r do
    if t = 1 then
      action ← C
    else if ever_defected_flag then
      action ← D
    else
      if any observed action in round t−1 = D then
        ever_defected_flag ← true
        action ← D
      else
        action ← C
      end if
    end if

    submit action
    observe {actions₁,…,actionsₙ} from all players
    if ∃ j: actionsⱼ = D then
      ever_defected_flag ← true
    end if
  end for

This “Grim‐Trigger’’ strategy is as cooperative as possible—cooperates whenever everyone else has cooperated, and swiftly and permanently punishes any defection to protect the common pool.
'''

description_COOPERATIVE_2 = '''
Below is a single‐agent strategy—call it “Firm-but-Fair CPR Cooperator (FFC)”—that strives for full cooperation (C) as long as everybody does, but punishes defections (D) briefly, then forgives, and always defects in the very last round (since there is no future to protect).  

1.  State variables  
    •  punishmentTimer ∈ {0,1,…,L}  
       –  Number of rounds left in punishment mode.  
    •  L = fixed punishment length (e.g. 2 rounds).  
    •  r = total number of rounds.  

2.  Decision rule for round t (1 ≤ t ≤ r), given history of all players’ past actions H:  
    if t == 1 then  
       play C   // start cooperatively  
    else if t == r then  
       play D   // last round: defect for immediate gain  
    else if punishmentTimer > 0 then  
       punishmentTimer ← punishmentTimer − 1  
       play D   // continue punishing  
    else if ∃ j and some τ = t−1 with H[j,τ] = D then  
       // someone defected in the immediately preceding round  
       punishmentTimer ← L  
       play D   // enter punishment phase  
    else  
       play C   // no recent defections: cooperate  

3.  Comments and rationale  
  •  Cooperation circle: As long as nobody defects, FFC cooperates every round, yielding high sustainable payoffs and letting the stock regrow.  
  •  Defection detection: Because all actions are public, any D in round t−1 is detected at t, triggering punishment.  
  •  Limited punishment: We choose a finite L (e.g. 2).  This makes the strategy forgiving, so a single mistake or transient defection does not collapse cooperation forever.  
  •  Last round defection: In a finite game without further interaction, defecting in round r dominates cooperating, so FFC defects there.  This also communicates that punishments should not extend into a round that cannot support future cooperation.  

4.  Pseudocode  

    initialize punishmentTimer ← 0  
    for t in 1..r do  
      if t == 1 then  
        action[t] ← C  
      else if t == r then  
        action[t] ← D  
      else if punishmentTimer > 0 then  
        punishmentTimer ← punishmentTimer − 1  
        action[t] ← D  
      else  
        // inspect round t−1 for defections  
        let defectOccurred ← false  
        for each player j do  
          if H[j, t−1] = D then defectOccurred ← true  
        if defectOccurred then  
          punishmentTimer ← L  
          action[t] ← D  
        else  
          action[t] ← C  
      end if  
    end for  

5.  Edge‐case handling  
  •  First round: we must start somewhere—FFC starts with C to signal cooperativeness.  
  •  Last round: unbeatable incentive to defect; FFC defects.  
  •  Simultaneous defections: punishment is triggered only once per round of defection but may re-trigger if multiple rounds of defection occur.  
  •  Stock collapse scenarios: by default FFC sticks to C as long as nobody defects, trusting the built-in stock‐regeneration; if the pool ever collapses (S → 0), both C and D yield zero, so FFC’s logic remains well‐defined (it keeps punishing according to history, but the payoffs are already zero).  

This “Firm-but-Fair” rule has the hallmarks of successful conditional cooperation in social‐dilemma tournaments—it rewards collective C with mutual high payoffs, swiftly punishes free-riding, then returns to cooperation.
'''

description_COOPERATIVE_3 = '''
Below is a single‐agent strategy (“Coop–TFT‐End”) that (i) starts out fully cooperative, (ii) punishes any defection by any player with exactly one round of defection, then returns immediately to cooperation, and (iii) defects in the very last round to guard against end-game exploitation.  It requires only perfect monitoring of the previous round’s actions, a one‐bit “punish” flag, and knowledge of t and r.

1.  Data structures / internal state  
    •  punishing ∈ {false, true}  — true if we owe one round of punishment  
    •  r  — total number of rounds  
    •  t  — index of the current round  

2.  Initialization (before round 1)  
    punishing ← false  

3.  Action rule at the start of round t:

    if t == 1 then  
        play C      // always start by cooperating  

    else if t == r then  
        play D      // defect in the last round to avoid being exploited  

    else if punishing == true then  
        // we are serving out a one‐round punishment  
        play D  
        punishing ← false  

    else  
        // look at what happened in round t–1  
        if ∃ j (j ≠ i) such that player j played D in round t–1 then  
            // at least one defection observed  
            punishing ← true  
            play D  
        else  
            // everyone cooperated last round  
            play C  

4.  Explanation of key pieces  

  •  First round (“t=1”): we cooperate to signal goodwill.  
  •  Cooperate‐unless‐punishing: as long as no defection has just occurred, keep cooperating.  
  •  Single‐round punishment: if we observe any D in the previous round, we defect exactly once (punishing=true), then immediately return to cooperation.  
  •  Last round (“t=r”): we defect regardless, to eliminate the incentive for others to “cheat” us in the final move.  

5.  Why it is cooperative  

  – Mutual cooperation (everyone plays C from t=1 to t=r−1) maintains the stock at capacity each round, maximizing all payoffs.  
  – A one‐round defection is enough to impose a short, credible penalty on free‐riders, but it is not so draconian as to collapse the resource.  
  – Quick forgiveness (return to C immediately after the one‐round punishment) helps restore the common pool.  
  – Defecting in the very last round is a standard finite-horizon precaution and does not meaningfully harm the resource when r is known.  

6.  Pseudocode

    function CoopTFTEnd(t, history, r):
        // history is sequence of past action profiles; history[t−1][j] ∈ {C,D}

        if t == 1:
            return C

        if t == r:
            return D

        if punishing == true:
            punishing ← false
            return D

        // check for any defection by others in round t−1
        for each player j ≠ i:
            if history[t−1][j] == D:
                punishing ← true
                return D

        // no defections last round
        return C

This strategy requires only O(n) work each round (to scan the previous action profile) and O(1) memory (the Boolean punishing flag).  It sustains full cooperation most of the way, enforces quick, proportionate punishment on any defector, and handles first‐ and last‐round edge cases cleanly.
'''

description_COOPERATIVE_4 = '''
Below is a simple “Tit‐for‐Tat with one‐round punishment and endgame cooperation” strategy.  It is fully cooperative as long as nobody ever cheats, punishes any defection exactly one round, then immediately forgives, and in the very last round it cooperates if—and only if—no defection has ever occurred.

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
Strategy name:  One‐Shot Punitive Tit‐for‐Tat with Endgame Cooperation  

State variables (maintained across rounds):  
• everDefected  (bool) – has any player ever defected up to the start of this round?  
• skipDetect    (bool) – are we in the single punishment round, so we must ignore defection‐detection this round?  

Initialization (before round 1):  
everDefected ← false  
skipDetect   ← false  

For each round t = 1,2,…,r do:  
  if t = 1 then  
    play C  
    continue to next round  
  end if  

  if t = r then  
    ▷ Last‐round decision  
    if everDefected = false then  
      play C    ▷ if nobody ever cheated, stay cooperative to the end  
    else  
      play D    ▷ otherwise defect for final grab  
    end if  
    continue to next round  
  end if  

  if skipDetect = true then  
    ▷ This is our one‐round punishment stage  
    skipDetect ← false   ▷ reset for the next round  
    play D               ▷ carry out the punishment  
    continue to next round  
  end if  

  ▷ Normal rounds 2 … r−1, not in punishment stage  
  look at the actions of all n players in round t−1  
  if any player’s action in round t−1 = D then  
    everDefected ← true  
    skipDetect   ← true   ▷ schedule exactly one round of punishment  
    play D             ▷ punish now  
  else  
    play C             ▷ everybody cooperated last round, so cooperate now  
  end if  

end for  

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
Explanation of key features:

1. First round: Always Cooperate.  
2. Normal phase (rounds 2 to r−1):  
   – If nobody defected last round ⇒ Cooperate.  
   – If you detect any defection last round ⇒ Defect this round (punishment) and set skipDetect so that next round you ignore the fact that you yourself just defected.  That breaks the “mutual‐retaliation” loop and lets you return to cooperation immediately afterward.  
3. Endgame (round r):  
   – If the history is “perfect cooperation” (everDefected=false) ⇒ Cooperate in the last round.  
   – Otherwise ⇒ Defect in the last round to avoid being exploited.  
4. Punishment length = exactly one round.  After punishing, you forgive and return to cooperation if your opponents also return to cooperation.  
5. everDefected flag ensures that once anybody cheats you remember it, so that in the very last round you defect if there was ever a cheating incident.  

This strategy (1) establishes a clear cooperative norm, (2) punishes deviations swiftly but only briefly, (3) forgives to restore cooperation, and (4) handles the backward‐induction “last‐round” temptation by reserving the right to defect in round r only if anyone ever cheated before.
'''

description_COOPERATIVE_5 = '''
Below is a single‐strategy recipe we call “Reciprocal Conditional Cooperation with Last‐Round Defection.”  It (a) starts by cooperating, (b) punishes any defection by a one‐round defection, (c) then immediately forgives, and (d) defects on the last round when no future punishment is possible.  This simple reciprocity sustains cooperation in the interior rounds and guards against exploitation.

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
Strategy: “Reciprocal Conditional Cooperation with Last‐Round Defection”  

Parameters (you may tune if desired):  
  • L = 1    # punishment length (in rounds)  
  • r        # total rounds  
  • n        # number of players  

State you track:  
  • last_defect_round  ← 0 # the most recent round in which any player (including you) played D  

Decision rule for round t with current stock S_t and full public history H up through round t–1:  

1.  If t == r:  
      Return D  
    # Defect in final round—no future to protect.  

2.  If t == 1:  
      Return C  
    # Establish cooperation at the outset.  

3.  If (t – last_defect_round) ≤ L:  
      Return D  
    # Punishment window of L rounds immediately after any defection.  

4.  Otherwise (we are not in a punishment window and this is not round 1 or r):  
    a.  Inspect the actions in round t–1.  
    b.  If any player played D in t–1:  
          last_defect_round ← t–1  
          Return D    # trigger a one‐round punishment  
    c.  Else:  
          Return C    # everyone cooperated last round, so cooperate now  

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  

Pseudocode  

```
initialize last_defect_round ← 0

function decide_action(t, r, S_t, history H):
    if t == r:
        return D

    if t == 1:
        return C

    # in punishment window?
    if t - last_defect_round ≤ L:
        return D

    # check last round for defections
    let prev_actions = H[t-1].actions   # list of A_i in round t-1
    if “D” in prev_actions:
        last_defect_round ← t-1
        return D
    else:
        return C
```

How it works and why it’s cooperative  
 1. First round cooperation signals goodwill.  
 2. As long as everybody cooperates, you continue to cooperate, sustaining stock at S → S/2 → regrowth → near capacity.  
 3. A single defection by anyone yields a one‐round punishment (all‐D), which drives stock down and signals that defection is costly.  
 4. Immediate forgiveness after one round of punishment restores cooperation quickly.  
 5. In the last round, you defect (standard backward‐induction precaution), so that opponents know that defection in round r is inevitable—but by then the cooperative regime has already delivered most of the joint surplus.  

Edge cases handled  
 • Stock S_t = 0 or negligibly small: both C and D yield zero, so the rule still applies harmlessly.  
 • Multiple simultaneous defections: “any D” in last round triggers punishment once.  
 • If a defection and punishment overlap: the single round of punishment is not extended by fresh infractions during the punishment round itself—punishment length is fixed to L.  
 • If r = 2: round 1 → C, round 2 → D.  

This strategy maximizes the group’s long‐run stock (and hence total payoffs) by sustaining cooperation in all interior rounds, deterring free‐riding with short punishments, and only resorting to defection at the final round.
'''

description_COOPERATIVE_6 = '''
Below is a single‐agent strategy called “Generous Trigger with Last‐Round Defection.”  It is designed to sustain cooperation on the common pool while still capturing the single‐round incentive to defect at the end.  It uses only publicly observable history (who defected when) and the current stock, so it can be played against any number of opponents without pre-play coordination.

1.  Overview of the logic  
    •  Cooperate (C) by default, to keep the stock near capacity and earn the sustainable payoff.  
    •  If anyone defects in a given round, punish by defecting just once in the next round (tit-for-one-round-punishment), then return immediately to cooperation.  
    •  Always defect in the last round to capture the one-shot incentive (standard end-game logic).  
    •  If the stock ever falls below a small threshold, unconditionally cooperate (even during punishment) to help the pool recover.  

2.  Parameters and bookkeeping  
    Let  
      r = total number of rounds  
      t = index of the current round (1 ≤ t ≤ r)  
      stock[t] = common‐pool stock at the start of round t  
      last_actions = vector of everyone’s actions in round t–1  
      punish = 0 or 1, number of “punishment rounds” remaining  

3.  Decision rule in words  
    In each round t:  
      a) If t == 1:  
           • punish ← 0  
           • play C  
      b) Else if t == r:  
           • (End‐game) play D  
      c) Else if stock[t] < ε (a very small threshold, e.g. capacity/(10 n)):  
           • stock is nearly exhausted → play C (to promote regrowth), but still decrement punish if >0  
      d) Else if punish > 0:  
           • play D (punishment)  
           • punish ← punish – 1  
      e) Else if in last_actions any player chose D:  
           • punish ← 1  
           • play D  
      f) Else:  
           • play C  

4.  Pseudocode  
    ```  
    initialize punish ← 0  
    for t in 1..r do  
      observe stock[t] and last_actions (undefined if t=1)  

      if t == 1 then  
        action[t] ← C  
        continue to next t  
      end if  

      if t == r then  
        action[t] ← D  
        continue to next t  
      end if  

      # If the pool is nearly depleted, help it recover  
      ε ← capacity/(10 n)  
      if stock[t] < ε then  
        action[t] ← C  
        if punish > 0 then punish ← punish – 1  
        continue to next t  
      end if  

      # If we are still in punishment mode, defect  
      if punish > 0 then  
        action[t] ← D  
        punish ← punish – 1  
        continue to next t  
      end if  

      # Otherwise check if someone defected last round  
      if “D” ∈ last_actions then  
        punish ← 1       # punish for exactly one round  
        action[t] ← D  
      else  
        action[t] ← C  
      end if  
    end for  
    ```

5.  Why this is cooperative  
    • By default it plays C every round, which maximizes long-run joint growth of the stock.  
    • A one‐round, proportional punishment is mild (“generous tit-for-tat”), so it is forgiving and allows the group to return quickly to full cooperation.  
    • Helping to rebuild the pool when stock is very low ensures the common‐pool never collapses permanently.  
    • The only necessary defection in the last round is the standard backward‐induction “end‐game” move; it does not undermine the prior rounds’ cooperative growth.  

This strategy thus aligns each player’s incentive with the long‐run health of the common pool while retaining enough deterrent against one‐off exploiters.
'''

description_COOPERATIVE_7 = '''
Below is a single‐strategy proposal—“Modified Tit‐for‐Tat with Last‐Round Defection”—that sustains full cooperation except in response to observed defections and in the final round, where defection is payoff‐maximizing anyway.  

1.  Informal description  
    •  Cooperate in round 1 to establish trust.  
    •  In any round 2 ≤ t < r, cooperate if and only if every other player cooperated in round t–1; otherwise defect (punish).  
    •  In the final round t = r, defect (one-shot incentive).  

    By keeping cooperation as the default and punishing only immediately after a defection, stock stays at its sustainable maximum and players earn π_i = S/(2n) each round.  

2.  Handling edge cases  
    •  First round (t=1): no history → cooperate.  
    •  Last round (t=r): one‐shot defection is dominant → defect.  
    •  Zero stock (S=0): both actions yield zero payoff; we still follow the same rule (cooperate except when punishing or in the final round) so as not to introduce noise.  

3.  Pseudocode  

    Parameters:  
      n, r, capacity (given)  
    Variables:  
      history[t–1][i] ∈ {C,D}: action of player i in prior round  
      my_action[t] ∈ {C,D}: what I play in round t  

    Initialization:  
      For all i: history[0][i] = C   (dummy)  

    For t = 1 to r do:  
      if t == 1 then  
        my_action[t] = C  
      else if t == r then  
        // Last round: defect  
        my_action[t] = D  
      else  
        // t in 2…r–1  
        if ∀ j≠me: history[t–1][j] == C then  
          my_action[t] = C    // no one defected last round  
        else  
          my_action[t] = D    // punish any defection immediately  
        end  
      end  

      // Play my_action[t], observe others’ actions, update history  
      After all moves in round t:  
        For each player i: history[t][i] = observed action of i  
    end  

4.  Why this is cooperative  
    – It maintains full cooperation so long as everyone does.  
    – Punishes exactly once after each defection, avoiding over‐punishment that could collapse cooperation.  
    – Forgives immediately if opponents return to cooperation.  
    – Keeps the common stock near capacity, maximizing joint payoffs (S returns to capacity under all-C).  

This strategy requires no off-path assumptions, no communication, and uses only observed actions. It supports stable cooperation, deters free‐riding, and correctly switches to defection in the terminal round.
'''

description_COOPERATIVE_8 = '''
Below is a single‐strategy “stock–aware, forgiving tit-for-tat” that (a) aims to keep the common pool near capacity by cooperating, (b) punishes defection so that unilateral deviators are deterred, (c) forgives after a limited punishment, (d) protects an almost‐depleted stock by temporarily pausing punishments, and (e) defects in the very last round (since there is no future to protect).

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
1.  Parameters your strategy chooses in advance  
    • P_default = 3  
       – default length (in rounds) of any punishment spell  
    • S_low = capacity * 0.10  
       – if the stock ever falls below S_low, we temporarily suspend punishment to allow recovery  
––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
2.  State variables maintained through the game  
    • punish_remaining  ←  0  
       – rounds left in current punishment  
    • defected_before  ←  false  
       – have we ever seen any other player defect?  
––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
3.  Round-by-round decision rule (at round t, with stock S_t)  
       
    if t == 1:  
        action ← C                   # always start by cooperating  
        
    else if t == r:  
        action ← D                   # last round: defect (no future left)  
        
    else if S_t < S_low:  
        # stock is too low—prioritize pool recovery  
        action ← C  
        # note: we do not reduce punish_remaining here  
        
    else if punish_remaining > 0:  
        # we are in a punishment spell  
        punish_remaining ← punish_remaining – 1  
        action ← D  
        
    else if defected_before == true:  
        # a previous round saw at least one defector;  
        # start a new punishment spell of length P_default  
        punish_remaining ← P_default – 1  
        action ← D  
        
    else:  # no punishment, no critical low stock, not last round  
        action ← C  
        
    # AFTER choosing action, update observations for next round  
    Observe opponents’ actions this round.  
    if any opponent played D in this round:  
        defected_before ← true  

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
4.  Intuition and properties  

1.  **Cooperative baseline**  
    – As long as nobody has defected, stock stays high, so each round we play C and harvest S/(2n)  
2.  **Deterrence via punishment**  
    – On the first observed defection, we switch to D for P_default rounds.  
    – This reduces the defector’s future payoff, making unilateral D unprofitable if the group mostly cooperates.  
3.  **Forgiveness**  
    – After P_default rounds of punishment we return to cooperation (unless another defection occurs).  
    – This prevents endless “defect wars” and allows recovery of mutual cooperation.  
4.  **Stock rescue**  
    – If stock S_t ever falls below S_low (10% of capacity), we override punishment and cooperate anyway.  
    – That helps the pool bounce back more quickly, benefiting everyone in subsequent rounds.  
5.  **Endgame defection**  
    – In round r we defect, because there is no future to sustain cooperation.  
––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  

This strategy is simple, transparent (all players can infer it from your behavior), punishing enough to deter defection, yet forgiving so that cooperation can resume. It also guards against irreversible depletion by suspending punishments when the stock is critically low.
'''

description_COOPERATIVE_9 = '''
Below is a self‐contained, repeatable cooperative strategy (“Generous Tit-for-Tat with Endgame Defection”) for the Common Pool Resource Game.  It never relies on side-channels or pre-played agreements—only on the public history of C/D choices and the known round count.

1.  Overview of the idea  
    •  Start by cooperating to build up the stock.  
    •  Punish defections—but only briefly—so that others have an incentive to return to cooperation.  
    •  Always defect in the very last round (since there is no future to sustain cooperation).  

2.  Notation  
    Let t = current round (1 ≤ t ≤ r).  
    Let history[t–1] = the vector of all players’ actions in round t–1 (if t=1, history[0] is empty).  
    Let PunishTimer = number of remaining rounds we are “in punishment mode.” Initialize PunishTimer := 0.  

3.  Decision rule for round t  
    if t == r then  
       play D   // Last-round defection  
    else if PunishTimer > 0 then  
       play D  
       PunishTimer := PunishTimer – 1  
    else if t > 1 and any player’s action in history[t–1] == D then  
       // Someone defected last round—begin a one-round punishment  
       play D  
       PunishTimer := 1  
    else  
       play C  

4.  Explanation of key features  
    •  “Generous”: We only punish for one round—even if multiple players defect we don’t spiral into endless mutual defection.  
    •  “Tit-for-Tat”: A defection in the previous round triggers exactly one round of D, then we forgive and go back to C (unless another defection occurs).  
    •  “Endgame Defection”: In the last round we defect, exploiting whatever stock is left, because no future cooperation can be leveraged.  This is unavoidable under standard backward-induction logic; without it, pure cooperators get exploited in the final round.  

5.  Pseudocode  

    initialize PunishTimer := 0

    for t in 1…r do
      if t == r then
        action := D
      else if PunishTimer > 0 then
        action := D
        PunishTimer := PunishTimer – 1
      else if t > 1 and exists i in {1..n} such that history[t–1][i] == D then
        // Someone defected last round
        action := D
        PunishTimer := 1    // punish for one round
      else
        action := C

      submit action
      observe others’ actions → history[t]
    end for

6.  Why this is cooperative  
    •  Whenever all players cooperate, stock stays near capacity → high per-round payoffs S/(2n).  
    •  A one-round punishment is enough to discourage profitable one-off defections (since you lose S/n this round and also give up next-round’s C payoff S/(2n) by playing D).  
    •  Because we forgive quickly, long runs of mutual cooperation can re‐establish after errors or occasional defections by others.  
    •  We only defect in the last round, which is the only strictly dominant move there; in all earlier rounds we prefer C unless punishing.  

This strategy strikes a balance between robust enforcement of cooperation and rapid reconciliation—ideal for a tournament of black-box strategies with no communication beyond moves.
'''

description_COOPERATIVE_10 = '''
Below is a simple, fully‐specified “forgiving tit-for-tat” style strategy that (1) starts out fully cooperative, (2) punishes any defection by defecting exactly one round, then (3) immediately returns to cooperation.  It is memory‐1 (only last round’s actions matter), easy to implement, and explicitly oriented toward maintaining full cooperation.

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
STRATEGY NAME  
  Forgiving Tit-for-Tat (FTFTT)

KEY IDEAS  
1.  Round 1: always cooperate.  
2.  If last round was “all-C,” cooperate.  
3.  If last round contained ≥ 1 defection, defect this round as punishment, then forget it and return to cooperate.  

This creates a carrot-and-stick:  defectors get punished for exactly one round, but the group quickly returns to the high-stock cooperative path.

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
PSEUDOCODE  

Inputs (common to all strategies):  
  n         ← number of players  
  r         ← total number of rounds  
  history   ← an array of past rounds’ action profiles, where  
                history[t][i] ∈ {C,D} is player i’s move in round t  
State variables (maintained by our agent):  
  punish_rounds_remaining ← 0    # how many more rounds we must punish  

for t in 1…r do  
  if t == 1 then  
    # first round: no history yet  
    my_action ← C  

  else  
    if punish_rounds_remaining > 0 then  
      # we are currently in a punishment spell  
      my_action ← D  
      punish_rounds_remaining ← punish_rounds_remaining - 1  

    else  
      # look at what happened last round  
      let last_profile ← history[t-1]  
      if “no one defected in last_profile” then  
        my_action ← C  
      else  
        # someone defected → punish for exactly one round  
        punish_rounds_remaining ← 1  
        my_action ← D  
      end if  
    end if  
  end if  

  play my_action  
end for  

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
DECISION RULES IN PLAIN ENGLISH  

1) Round 1 → Cooperate.  
2) In any round t>1:  
   • If you are in the middle of punishing (punish_rounds_remaining>0), play D and decrease your counter.  
   • Otherwise, look at round t–1:  
       – If every player chose C, then play C.  
       – If you see any D, then set punish_rounds_remaining=1 and play D this round.  

After you punish for exactly one round, you reset punishment and once again cooperate as long as no further defections occur.  

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
HANDLING EDGE CASES  

• Last round (t = r):  same rule applies.  If round r–1 was all-C, you will cooperate even in the final round.  If round r–1 contained a defection, you will defect once more as your one‐round punishment.  

• Multiple simultaneous defectors:  they all get the same one‐round group punishment; you cannot single out individuals, but by defecting you lower the stock and hence everyone’s next payoff.  

• Stock collapse thresholds:  this strategy does not explicitly monitor the stock, but by sustaining full cooperation whenever possible you maximize S each round (keeping it at or near capacity), so the stock‐based dynamics automatically stay in the healthy region.  

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
WHY THIS IS “COOPERATIVE”  

– You always begin by cooperating and give every player the benefit of the doubt.  
– You only defect in direct response to observed defections, for exactly one round.  
– You immediately return to cooperation (forgiveness), thus restoring the high-stock, high-payoff path.  
– By never punishing longer than necessary, you avoid unnecessary stock collapse and maximize joint gains under full cooperation.  

In a tournament of independent LLMs, this strategy tends to sustain mutual cooperation at full‐stock levels (each player consuming capacity/(2n) every round) yet still credibly punishes one‐shot defectors enough to deter profitable exploitation.
'''

description_COOPERATIVE_11 = '''
Below is a “Tit-for-Tat with Endgame Defection” strategy.  It is “nice” (never defects first), retaliatory (punishes immediately once), forgiving (one‐shot punish), and exploits the fact that in the last round there is no future to lose by defecting.

1.  Definitions and bookkeeping  
   •  Let r = total number of rounds.  
   •  In each round t you observe, for every other player j, what action they took in round t–1.  
   •  Define OpponentDefectedLast = True if at least one opponent played D in the immediately preceding round; otherwise False.  

2.  Decision rules  
   For each round t = 1,2,…,r do:  
     if t == 1 then  
       play C    # start “nice”  
     else if t == r then  
       play D    # exploit in last round  
     else if OpponentDefectedLast then  
       play D    # immediate 1‐round punishment  
     else  
       play C    # otherwise cooperate  

3.  Pseudocode  

   initialize history of opponents’ actions (all empty)  
   for t in 1…r:  
     if t == 1:  
       action ← C  
     else if t == r:  
       action ← D  
     else:  
       # check if any opponent defected in round t–1  
       if ∃ opponent j with history[j][t–1] == D then  
         action ← D  
       else  
         action ← C  
     end if  
     
     play(action)  
     observe opponents’ actions this round and append to history  
   end for  

4.  Why this is cooperative  
   – As long as everyone else has cooperated in the previous round, you cooperate, which maximizes the sustainable stock and yields the high mutual payoff S/(2n).  
   – You never pre‐emptively defect—you only punish on seeing a defection.  
   – Punishment is only one round (forgiving), so a single mistaken defection by someone does not lock you into endless mutual defection.  
   – In the very last round, since there is no future to protect, you defect to secure the higher immediate payoff S/n.  

5.  Edge cases handled  
   – r=2: Round 1 → C, Round 2 → D.  
   – Single defection by an opponent at any time triggers exactly one D from you next round, then you return to cooperation if they do.  
   – No punishments are carried into round r: the “else if t == r” takes priority, so you always defect last. 
'''

description_COOPERATIVE_12 = '''
Below is a simple, robust “Tit-for-Tat with End-Game Defection” strategy that aims to sustain the common pool at or near capacity by cooperating as long as everyone else does, punishing defections just long enough to deter free-riding, and handling the inevitable last-round incentive to defect.

1.  Overview of the idea  
    - In each round (except the last) we start by cooperating.  
    - If anyone defected in the immediately preceding round, we “punish” by defecting once (one-shot retaliation), then return to cooperation.  
    - In the final round we defect (because there is no future to protect).  

2.  Why it promotes cooperation  
    - By cooperating so long as no one defects, we keep the stock high (growth remains positive).  
    - By defecting for exactly one round after any defection, we impose a short, predictable cost on deviators—enough to remove their one-shot gain without triggering the collapse that a permanent “grim trigger” would cause.  
    - The final-round defection is unavoidable in a finite-horizon game, but since it is common knowledge, players know not to defect earlier for fear of retaliation.  

3.  Full description  

   State variables we carry forward from round to round:  
     punish_counter ∈ {0,1}  // how many more rounds we must punish (0 or 1)  

   Initialization (before round 1):  
     punish_counter ← 0  

   For each round t = 1, 2, …, r do:  
     if t = r then  
       // Last round: defect (no future to safeguard)  
       play D  
       exit loop  
     end if  

     if t = 1 then  
       // First move: unconditional cooperation  
       play C  
       continue to next round  
     end if  

     // In all other non-terminal rounds (2 ≤ t < r):  
     if punish_counter > 0 then  
       // We are in a one-round punishment phase  
       play D  
       punish_counter ← punish_counter − 1  
       continue to next round  
     end if  

     // Otherwise, look at what happened in the previous round  
     if ∃ j ≠ i with action_j at round t−1 = D then  
       // Someone defected last round: punish once  
       punish_counter ← 1  
       play D  
     else  
       // Everyone cooperated last round  
       play C  
     end if  
   end for  

4.  Pseudocode  

   initialize punish_counter ← 0  
   for t in 1…r:  
     if t = r:  
       action ← D  
       break  
     end if  
     if t = 1:  
       action ← C  
     else if punish_counter = 1:  
       action ← D  
       punish_counter ← 0  
     else if any opponent’s action in round (t−1) = D:  
       action ← D  
       punish_counter ← 1  
     else:  
       action ← C  
     end if  
     play(action)  
   end for  

5.  Handling special cases  
   •  First round: Cooperate unconditionally to build the norm.  
   •  Any defection in the previous round: Defect exactly once (punish_counter=1), then resume cooperation if no further defections.  
   •  Last round (t=r): Defect, since there is no future payoff to protect.  

6.  Cooperative mindset  
   – So long as the group remains all-cooperators, we never miss an opportunity to harvest at the sustainable rate S/(2n), and the stock regenerates up to capacity.  
   – We punish exactly once for any observed defection—this imposes a cost on deviators that outweighs their one-shot gain, while avoiding a permanent death spiral of mutual defection.  
   – By defecting only in the final round, we do not undermine the cooperative equilibrium in earlier rounds.  

This strategy is simple, transparent, and follows the well-tested logic of Tit-for-Tat with a single-round punishment and an unavoidable end-game defection. It will sustain near‐capacity stock throughout the bulk of the game and deter free-riders without precipitating a collapse of the common pool.
'''

description_COOPERATIVE_13 = '''
Below is a fully self‐contained cooperative strategy for the n-player Common Pool Resource game.  It combines (i) an “all-cooperate” baseline, (ii) a one-round punishment for any defection, (iii) automatic cooperation if the stock gets too low, and (iv) the inevitable last‐round defection.  It uses only observed past actions and the current stock.

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
STRATEGY NAME  
Generous One-Round Punisher with Endgame Defection (GOP-ED)

PARAMETERS (you can tune these)  
  • punishment_length P = 1  // punish defectors by defecting one round  
  • stock_threshold α = 0.20  // if stock ≤ α·capacity, always cooperate  

STATE VARIABLES  
  • last_round_had_defection (bool) – did any player defect in t-1?  

DECISION RULES  
  At the beginning of each round t, observe:  
    • t (current round index, 1…r)  
    • S_t (current common‐pool stock)  
    • actions of all players in round t–1  

  1. If t == r  (the last round):  
       Play D  // no future to protect  
       END.

  2. Else if S_t ≤ α · capacity:  
       Play C  // stock is low, help it recover  

  3. Else if t == 1:  
       Play C  // start by cooperating  

  4. Else (2 ≤ t < r):  
       If last_round_had_defection == true:  
         Play D  // punish for exactly one round  
       Else  
         Play C  // otherwise continue cooperating  

  After choosing, update last_round_had_defection for next round:  
       last_round_had_defection := (was there any D in round t?)

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  

PSEUDOCODE  

  initialize last_round_had_defection ← false

  for t in 1…r:
    observe S_t, history[t–1].actions

    // 1. Last‐round defection
    if t == r:
      action_t ← D
    
    else
    // 2. Stock‐recovery safety
    if S_t ≤ α*capacity:
      action_t ← C

    // 3. First round
    else if t == 1:
      action_t ← C

    // 4. Punish or cooperate
    else:
      if last_round_had_defection:
        action_t ← D
      else
        action_t ← C

    // Execute action_t and observe all players’ moves
    play(action_t)

    // 5. Update for next round
    last_round_had_defection ← (exists any player j with action_j == D in round t)

  end for

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  

WHY THIS WORKS  
  • Cooperates by default, sustaining the stock near capacity.  
  • Any defection anywhere in the group triggers exactly one round of group-wide punishment, which deters free-riding but is not overly harsh.  
  • If the pool is drained below α·capacity it switches to guaranteed cooperation so the resource can regrow.  
  • In the very last round everyone defects (since there is no future to protect).  

By mixing generosity (forgiveness after one punishment round) with a clear deterrent (one‐round sanction) and protecting against stock collapse, GOP-ED fosters high payoffs through sustained cooperation while still guarding against exploiters.
'''

description_COOPERATIVE_14 = '''
Below is a single‐strategy proposal, which we’ll call “Cooperative Tit‐for‐Tat with Forgiveness.”  It is simple, easy to describe in pseudocode, punishes defections just enough to deter them, forgives after one round of good behavior, and tries to maintain the common stock at capacity.  

----------------  
1.  Data structures and flags  
   • last_all_C: Boolean, true if in the immediately preceding round every player chose C.  
   • r: total number of rounds  
   • t: index of current round, t ∈ {1,…,r}  

2.  Initialization  
   t ← 1  
   last_all_C ← true      // (Nothing has happened yet, so we “assume” cooperation.)  

3.  Decision rule (for each round t):  
   if t = 1 then  
     action ← C            //  – open with cooperation  
   else if t < r then      //  – “inner” rounds  
     if last_all_C = true then  
       action ← C          //  continue mutual cooperation  
     else  
       action ← D          //  punish defectors for exactly one round  
   else                      //  t = r, final round  
     if last_all_C = true then  
       action ← C          //  try to preserve the pool one last time  
     else  
       action ← D          //  defect if you were just defected on  

4.  After everyone’s actions in round t are revealed:  
   last_all_C ← (for all players i, action_i = C)  

5.  Increment t (t ← t+1) and repeat until t > r.  

----------------  
Explanation of its features  

• First round: we cooperate unconditionally in order to “signal” willingness to steward the resource.  
• Inner rounds (1 < t < r):  
    – If in the precedent round absolutely no one defected, we continue to cooperate (so the stock stays at capacity).  
    – If anyone defected last time, we defect exactly once in retaliation.  That raises our short‐term payoff slightly but—critically—also punishes the deviator and drives home that defection is costly to the group.  
• Forgiveness: because we only punish for one round, a single mistake (or slip by one opponent) does not lock us into permanent defection.  If everyone returns to C in the next round, we resume cooperation immediately.  
• Last round: in a strictly backward‐induction world one would always defect, but that outcome destroys the resource and lowers total group welfare.  Our rule cooperates in the last round if the group has been “clean” (last_all_C = true), preserving the stock and delivering the best joint payoff.  If, however, someone just defected, we defect too (to avoid being suckered).  

This strategy has been used successfully in many common‐pool and public‐goods settings.  It is:  
  1) cooperative (it seeks full‐cooperation paths whenever possible),  
  2) tough on defection (it responds with a one‐period punishment),  
  3) forgiving (it quickly returns to cooperation after a single clean round),  
  4) aware of the end‐game (it tries to sustain public welfare through the last round unless just exploited).
'''

description_COOPERATIVE_15 = '''
Below is a simple, fully specified “conditional‐cooperation” strategy that (a) starts by cooperating, (b) punishes any defection for exactly one round, (c) always cooperates if the stock is dangerously low, and (d) defects in the very last round (since in a finite game it is dominant to grab what you can at the end).

Notation & state variables  
  n, r, capacity, history of past actions and stocks.  
  S_t  = stock at start of round t.  
  A_{i,t} ∈ {C,D} = our action in round t.  
  DefectedLastRound? = true if any player j (including ourselves) played D in round t–1.  
  PunishCounter = integer ≥ 0, how many more rounds we will defect purely as punishment.  

Parameters you can adjust  
  S_low = capacity / 4   (a “danger” threshold; if S_t ≤ S_low we always cooperate to help the pool recover)  
  P = 1                   (punishment length in rounds)  

Strategy description  

Initialize before round 1:  
  PunishCounter ← 0  

For each round t = 1,2,…,r do:

  1. Observe current stock S_t and history up through round t–1.  
     Set DefectedLastRound? = true if in round t–1 any player chose D; else false.

  2. Decide action A_{i,t} as follows:

     if t = r then  
       // Last round: grab the most you can  
       A_{i,t} ← D  

     else if S_t ≤ S_low then  
       // Pool is too low—always cooperate to let it regrow  
       A_{i,t} ← C  

     else if PunishCounter > 0 then  
       // We are in a punishment phase  
       A_{i,t} ← D  
       PunishCounter ← PunishCounter – 1  

     else if DefectedLastRound? = true then  
       // Somebody defected last round; punish by defecting this round  
       A_{i,t} ← D  
       PunishCounter ← P   // punish for P rounds in total (this one plus upcoming)  

     else  
       // No recent defection, pool not in danger, not last round  
       A_{i,t} ← C  

  3. Update history, observe everyone’s actions, compute payoffs, stock evolves to S_{t+1}, and loop.

Why this is cooperative  
  • We start by cooperating, building trust.  
  • We only defect to punish observed defections, and only for a limited P rounds, then we forgive and return to cooperation.  
  • If the common stock ever drops below S_low, we unconditionally cooperate so as to help the pool recover.  
  • We defect in the last round, which is individually rational and cannot affect future cooperation.  

Pseudocode

  function initialize(capacity, n, r):
      S_low ← capacity/4
      P ← 1
      PunishCounter ← 0

  for t in 1..r:
      observe S_t, history of actions
      if t == r:
          action ← D
      else if S_t ≤ S_low:
          action ← C
      else if PunishCounter > 0:
          action ← D
          PunishCounter ← PunishCounter − 1
      else if any player played D in round t−1:
          action ← D
          PunishCounter ← P
      else:
          action ← C

      play(action)
      update history, payoffs, stock to S_{t+1}

Adjustments and edge cases  
  • First round (t=1): PunishCounter=0, no prior defections, S_1=capacity, so we choose C.  
  • If multiple defections accumulate, we still only punish for P rounds total—this prevents long “death spirals.”  
  • If stock ever falls very low, we drop any punishment and always cooperate until regrowth pushes S_t > S_low.  
  • Last‐round defection is unavoidable under backward induction; punishing there has no future effect.  

This strategy balances firmness (one‐round punishment of free‐riding) with forgiveness and pool‐preservation, encouraging others to stay cooperative in the long run.
'''

description_COOPERATIVE_16 = '''
Below is a single‐strategy proposal—“Tit-for-Tat with Endgame”—that (1) reaches and sustains full cooperation whenever possible, (2) punishes defectors just enough to deter free-riding, and (3) explicitly handles first round, low‐stock, and final‐round edge cases.

1. Overview of the Strategy  
   • We begin every interaction by cooperating.  
   • In rounds 2 through r–1 we mirror whatever non-cooperation (if any) we observed in the immediately preceding round—but only for one period of retaliation.  
   • In the very last round (round r) we defect (since there is no future in which to make cooperation credible).  

   This simple “TFT with Endgame” has three attractive properties:  
   – It sustains full cooperation (high stock, high payoffs) as long as no one defects.  
   – A single defection by anyone is met with exactly one round of group‐wide defection, deterring unilateral free-riding.  
   – After the one‐round punishment, we return to cooperation, allowing the resource to recover.  

2. Detailed Decision Rules  
   Denote by a_i(t) our action in round t, and by H(t–1) the vector of all players’ actions in round t–1.  
   Denote by S(t) the stock at the start of round t.  

   Rule 1 (First Round):  
     a_i(1) = Cooperate  

   Rule 2 (Intermediate Rounds t = 2, 3, …, r–1):  
     if ∃ j such that a_j(t–1) = Defect  
       then a_i(t) = Defect   // one‐period punishment  
       else a_i(t) = Cooperate  

   Rule 3 (Last Round t = r):  
     a_i(r) = Defect  

3. Handling Edge Cases  
   • Stock exhaustion: If S(t) = 0 then both C and D yield zero. Our rule still applies, but payoffs are zero. We continue to follow TFT with Endgame.  
   • Very low stock (e.g. S(t) ≪ capacity): The relative benefit of defection stays constant (D always gives twice C), so our TFT rule remains optimal for deterring defection.  
   • Multiple defections in a row: We punish exactly one round. If defection persists, we punish each round until cooperation resumes (i.e. it’s full Tit-for-Tat).  
   • No noise / no mistakes: perfect monitoring ensures our responses align exactly with observed deviations.

4. Pseudocode  

```
INPUTS:
  r        // total number of rounds
  history  // empty at start; thereafter stores each round's action profile
FOR t in 1..r:
  if t == 1:
    action := C
  else if t == r:
    action := D
  else:
    // look at what happened in the previous round
    last_profile := history[t-1]        // vector of n actions
    if “Defect” ∈ last_profile:
      action := D
    else:
      action := C
  END
  play(action)
  observe full profile a_1(t),…,a_n(t)
  append this profile to history
END
```

5. Why This Is Cooperative  
  – If all players adopt it, from round 1 through r–1 everyone always plays C → stock stays at capacity → each round’s payoff = capacity/(2n) → group payoff maximized.  
  – A single defection in any intermediate round triggers exactly one round of all-D, which (a) lowers the deviator’s future expected payoff by cutting stock and (b) lowers everyone’s payoff by causing the stock dip—thus making unilateral defection unprofitable in expectation.  
  – After the one‐round punishment, cooperation immediately resumes, allowing the stock to recover (as growth function returns stock toward capacity).  

By combining the simplicity and robustness of Tit-for-Tat with the backward-looking final‐round defection, this strategy supports high mutual payoffs in repeated play without assuming off-path coordination or communication.
'''

description_COOPERATIVE_17 = '''
Below is a single‐strategy “recipe” for a cooperative contestant (“you”) in the n‐player CPR game.  It combines a Tit-for-Tat–style trigger (to discourage over-harvesting), a one‐round punishment with forgiveness (to limit cascades of retaliation), a stock‐driven emergency coop switch, and the unavoidable last‐round defection.

—–  
STRATEGY NAME  
Forgiving-TFT with Threshold and Endgame Defection  

PARAMETERS you fix once the game starts (common knowledge):  
• r = total rounds  
• capacity = maximum stock  
• stockThreshold = capacity/2    (can be tuned, e.g. 40%–60% of capacity)  

STATE VARIABLES (kept from round to round):  
• punishFlag (bool), initially false  

DECISION RULES for each round t = 1…r, observed stock S_t and history of all players’ actions up to round t–1:

1.  If t == r (last round)  
    • Action ← D  
      (No future to enforce cooperation)

2.  Else if S_t < stockThreshold  
    • Action ← C  
    • punishFlag ← false  
      (Emergency cooperation to rebuild the pool)

3.  Else if t == 1  
    • Action ← C  
      (Open with cooperation)

4.  Else if punishFlag == true  
    • Action ← C  
    • punishFlag ← false  
      (Forgive after one round of punishment)

5.  Else if “any player defected in round t–1”  
    • Action ← D  
    • punishFlag ← true  
      (One‐round group punishment)

6.  Else  
    • Action ← C  
      (Default cooperation)

------------------------------------------------  
PSEUDOCODE

  initialize punishFlag ← false  
  for t in 1…r do  
    observe current stock S_t  
    observe lastRoundDefected ← OR over all players j of [action_j at t–1 == D]  
      
    if t == r then  
      myAction ← D  
    
    else if S_t < (capacity/2) then  
      myAction ← C  
      punishFlag ← false  
    
    else if t == 1 then  
      myAction ← C  
    
    else if punishFlag == true then  
      myAction ← C  
      punishFlag ← false  
    
    else if lastRoundDefected == true then  
      myAction ← D  
      punishFlag ← true  
    
    else  
      myAction ← C  
    
    play myAction  

------------------------------------------------  
EXPLANATION OF COMPONENTS

1. First‐move cooperation (t=1):  
   • Builds mutual trust, avoids “first‐mover defect” stigma.

2. Threshold rule (S_t < capacity/2):  
   • If the stock falls below half, you always cooperate  
     – even if you’re in punishment mode—so the pool can regrow.

3. Tit-for-Tat–style trigger + one‐round punishment:  
   • If anyone over-harvested last round, you defect once  
     to impose a mild cost on all defectors.  
   • Then you forgive (punishFlag reset), opening the way back to cooperation.  
   • This discourages persistent free‐riding but avoids endless punishment wars.

4. Endgame defection (t = r):  
   • With no future threat, you grab the highest payoff.  
   • This is suboptimal socially but unavoidable under standard backward induction.

5. Forgiveness mechanic:  
   • By punishing for exactly one round, you limit downward spirals  
     and allow the group to re-establish cooperation quickly.

OVERALL BEHAVIOR  
• Rounds 1…r–1: You cooperate so long as the common pool is healthy and nobody recently over-harvested.  
• If a defection occurs, you retaliate exactly one round, then return to cooperation.  
• If the stock plunges below capacity/2, you override punishment and cooperate to rebuild.  
• In the final round you defect to maximize your last‐move payoff.

This strategy is cooperative—it maintains high group payoffs by sustaining the resource, punishes only briefly to deter defection, and forgives to restore cooperation quickly.
'''

description_COOPERATIVE_18 = '''
Below is a simple “end‐game adjusted” tit-for-tat strategy that (a) starts by cooperating, (b) punishes any defection one round only, then forgives, and (c) defects in the very last round (since there is no future to protect).  By cooperating whenever others have done so, it keeps total consumption low and lets the stock regrow near capacity; by punishing any defection immediately it discourages free‐riding; by forgiving after one round of punishment it avoids spiraling mutual defections; and by defecting in round r it maximizes final‐round payoff when retaliation is impossible.

Strategy parameters  
 n = number of players  
 r = total rounds  
 k = punishment length (here k=1)  
 e = endgame length (here e=1)

State variables maintained by the strategy  
 punish_until = 0     // round until which we are punishing (inclusive)

Decision rule for round t, given history and current stock S_t:

  if t == 1 then  
  action ← C   // Start by cooperating  
  
  else if t > r − e then  
  action ← D   // In the final e=1 round, defect  
   
  else if punish_until ≥ t then  
  action ← D   // We are still in punishment mode  

  else if any other player defected in round t−1 then  
  // Trigger punishment  
  punish_until ← t − 1 + k  
  action ← D

  else  
  action ← C   // Otherwise, cooperate

Pseudocode  
----------  
initialize punish_until ← 0  

for t in 1…r do  
  observe S_t and actions a₁,…,aₙ of previous round (if t>1)  

  if t == 1 then  
    play C  

  else if t > r − e then              // last round(s)  
    play D  

  else if punish_until ≥ t then       // still punishing  
    play D  

  else if ∃ j≠i: a_j(t−1) == D then    // someone defected last round  
    punish_until ← (t−1) + k  
    play D  

  else                                 // past was all cooperation  
    play C  

end for  
----------  

Explanation of Components  
1. First round (t=1): Cooperate, to establish a cooperative baseline.  
2. Punishment (k=1): If anyone defects in round t−1, defect in round t only.  This imposes an immediate cost on defectors but does not lock you into permanent grudges.  
3. Forgiveness: After one round of punishment you revert to cooperation provided no new defection occurs.  
4. Endgame (e=1): In the very last round (t=r), defect—since there is no future round in which your defection can be punished.  

Why this is cooperative  
- As long as all players cooperate, total extraction every round is (n·S_t/(2n))=S_t/2.  The stock after consumption is S_t/2, which then grows by 2·(S_t/2)·(1−(S_t/2)/capacity), returning quickly near capacity.  You and the group thus sustain high payoffs.  
- Any unilateral defection in round t−1 yields a higher immediate payoff to the defector, but you immediately punish in round t—making defection costly.  
- Because punishment is only one round long, cooperation can resume swiftly after a single defection, preventing long retaliatory spirals that collapse the resource permanently.  
- By defecting only in the final round, you maximize your terminal payoff without harming future rounds (there are none).  

Edge cases  
- If the stock S_t ever falls to 0 (e.g. after mass defection), all payoffs are zero thereafter; you continue to follow the same rule—cooperating by choosing the smaller extraction (C) has no effect on the stock but signals a willingness to rebuild if others do too.  
- If multiple players defect in t−1, you still punish only once for a single round—this avoids excessively punishing when many have already over–harvested.  
- If noise or simultaneous defections occur, the one-round punishment limits the “over‐kill” of long grim‐trigger strategies.
'''

description_COOPERATIVE_19 = '''
Below is a single‐strategy “cooperative trigger” that (i) tries to keep the pool at full capacity by rewarding universal cooperation, (ii) punishes any defection for a fixed number of rounds, then (iii) returns to cooperation (i.e. it is forgiving), and (iv) defects in the very last round (since there is no future to protect).  This is a straightforward extension of Tit‐for‐Tat to the n-player CPR setting with a finite horizon.  

1.  Variables and parameters  
   •  r       = total number of rounds  
   •  K       = punishment length (in rounds) after any observed defection; choose, e.g., K=2 or 3.  
   •  state   ∈ {“Normal”, “Punish”}  
   •  timer   = remaining punishment rounds if state=“Punish”  

2.  High‐level description  
   –  In “Normal” mode, you cooperate (C) unless you just observed someone defect.  The first time you see a D you switch to “Punish.”  
   –  In “Punish” mode you defect (D) for exactly K consecutive rounds, then automatically go back to “Normal.”  
   –  In the last round t=r, you defect (D) unconditionally (there is no future to protect).  

3.  Rationale  
   –  As long as no one ever defects, everyone cooperates every round and the stock stays at capacity.  
   –  A defection by any player triggers a group‐wide punishment of length K, which makes defection unprofitable if the horizon is long enough.  
   –  Because punishment is finite and forgivable, the group can restore mutual cooperation after K rounds.  
   –  By defecting in the very last round, you maximize your stage payoff when there is no continuation value.  

4.  Pseudocode  

   initialize:  
     state = “Normal”  
     timer = 0  

   for t from 1 to r do  
     if t == r then                            # last round  
       play D  
       continue to next round (or end)  
     end if  

     if state == “Punish” then  
       play D  
       timer = timer – 1  
       if timer == 0 then  
         state = “Normal”                     # punishment over, go back to Normal  
       end if  
       continue to next round  
     end if  

     # state == “Normal” and t < r  
     if t == 1 then  
       play C                                 # first round, start with cooperation  
     else  
       # observe the previous round’s actions of all n players  
       if (∃ j such that player j played D in round t−1) then  
         state = “Punish”                     # trigger punishment  
         timer = K − 1                        # we will defect this round + (K−1) more  
         play D  
       else  
         play C                               # no defections last round → keep cooperating  
       end if  
     end if  
   end for  

5.  Handling edge cases  

   •  First round (t=1): state=Normal so you play C.  
   •  Any round t<r in Normal: if anyone defected in t−1, you switch to Punish.  Otherwise you stay Cooperative.  
   •  Punishment mode: you D for exactly K rounds (including the round you detected the first defection), then go back to cooperation.  
   •  Last round (t=r): you play D unconditionally, since future payoffs are zero.  

6.  Discussion  

   –  If no one ever defects, the stock never falls below capacity, so every round every player gets capacity/(2n).  
   –  If someone defects in some round t, they earn S_t/n that round, but then you and everyone else defect for the next K-1 rounds too.  Those extra defections drive the stock down and cost the original defector in all of rounds t+1,…,t+K−1.  If r−t≫K, defecting is unprofitable.  
   –  After K punishment rounds you unilaterally return to cooperation, giving the group a clean slate and allowing long‐run efficiency to recover.  
   –  Defecting in the final round protects you against end‐game exploitation but does not destroy any remaining value.  

This strategy thus embodies a cooperative mindset—always ready to “return to the fold” after a finite punishment—but also credibly punishes defection, and defends itself in the very last round.
'''

description_COOPERATIVE_20 = '''
Below is a single‐agent “reciprocal cooperation” strategy that (a) starts by cooperating, (b) punishes defections but then forgives, and (c) defects in the last round to protect against end‐game exploitation.  It requires only observing who played C or D in the immediately preceding round.

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
Strategy name: Adaptive Tit-for-Tat with Limited Punishment  
State variables:  
  • punish_until (integer round index; initially 0)  

Parameters:  
  • r (total rounds)  
  • P_max = max(1, r–2)   # maximum length of punishment window  
––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  

Decision rule for round t (1 ≤ t ≤ r):  
1. If t == r:  
     play D   # last‐round defection  
2. Else if t ≤ punish_until:  
     play D   # we are in an active punishment phase  
3. Else if t == 1:  
     play C   # start with cooperation  
4. Else (2 ≤ t < r and not in punishment):  
   a. Look at round t–1: did **any** other player choose D?  
      – If yes:  
         • Set punish_length = min(P_max, r–1 – t)  
         • punish_until = t + punish_length  
         • play D   # trigger punishment  
      – If no:  
         play C   # resume cooperation  

After everyone’s moves in round t are revealed, you only need to update punish_until as above; no other bookkeeping is required.

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
Explanation of key features  
1. Initial cooperation (“nice”): round 1 is always C.  
2. Reciprocity: any opponent’s D in round t–1 provokes D in round t, but only for a limited window (P_max rounds), then we forgive and go back to C.  
3. Limited punishment: avoids endless mutual defection; punishment length shrinks as the game nears its end.  
4. End‐game safety: in round r we defect unconditionally, since no future rounds remain.  
5. Cooperative mindset: by default we cooperate, only switching to D to discipline defectors, and we quickly return to cooperation if they “repent.”  

This strategy balances strong incentives for others to keep cooperating (nobody wants to be punished for P_max rounds) with overall forgiveness and a clear, simple rule set.
'''

description_COOPERATIVE_21 = '''
Below is a single‐agent “reciprocal + endgame” strategy that (i) by default sustains full cooperation, (ii) punishes any defection for a short, finite time, (iii) forgives thereafter, and (iv) avoids the classic end‐of‐game breakdown by defecting only in the very last round (when cooperation can no longer be reciprocated).

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
High‐Level Description  
––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
1. Start by cooperating (C) in round 1.  
2. In each subsequent round t (2 ≤ t ≤ r), do the first of these that applies:  
   a. Endgame defection: if t = r, play D.  
   b. Punishment phase: if you are in a punishment countdown, play D and decrement the countdown.  
   c. Trigger: if any other player defected in the immediately preceding round, enter punishment for P rounds (including this one), and play D.  
   d. Otherwise, play C.  
3. Choose punishment length P small (e.g. P=2). This makes punishment swift but meaningful.  

This “Tit-for-Tat with forgiveness” preserves cooperation as long as no one defects, deters one‐off defections by a brief D spree, then returns to cooperation. By defecting only in the very last round, you avoid being exploited by endgame defection yet still capitalize on any stock built up cooperatively.  

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
Pseudocode  
––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
Inputs:  
  n        – number of players  
  r        – total rounds  
  capacity – resource capacity (unused except in payoff calc)  

Parameters you set:  
  P = 2    – punishment duration in rounds  

State variables (persist across rounds):  
  punish_timer ← 0  

For t from 1 to r do:  
  if t = 1 then  
    action ← C  
  
  else if t = r then  
    # Endgame: no future reciprocity possible  
    action ← D  

  else if punish_timer > 0 then  
    # Currently punishing  
    action ← D  
    punish_timer ← punish_timer − 1  

  else if “some other player defected in round t−1” then  
    # Trigger a punishment spree  
    punish_timer ← P − 1      # minus 1 because we punish this round too  
    action ← D  

  else  
    # No reason to defect—everyone cooperated last round  
    action ← C  

  end if  

  play(action)  

  observe others’ actions this round (for use next round)  

end for  

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
Why this is Cooperative  
––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
• Mutual cooperation (everyone choosing C) is self‐reinforcing and yields the highest sustainable stock.  
• A single D is met with a short, predictable penalty—discouraging unilateral over‐harvest.  
• The punishment is finite (forgiveness), so you don’t lock yourself into perpetual war of attrition.  
• Defecting only in the last round avoids the well‐known endgame unraveling of cooperation, while still allowing you to harvest the remaining stock when no future is at stake.  

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
Edge Cases  
––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
• First round (t=1): no history, so cooperate by default.  
• Rounds 2 ≤ t < r: follow trigger‐and‐punish with forgiveness.  
• Last round (t=r): defect unconditionally (endgame).  
• Multiple simultaneous defections: one observed defection triggers exactly P rounds of punishment—over‐reacting is avoided.  

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
Adjustments and Variations  
––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
• You can tune P (punishment length) based on r or capacity.  
• If you worry about opponents’ mis‐observations or noise, you can add a 1‐round “generous” forgiveness immediately after punishment.  
• You can generalize the endgame window to the last M rounds (M>1) if opponents are known to exploit single‐round defection.  

This simple, well‐studied class of strategies (Tit-for-Tat with finite punishment + last‐round defection) consistently fosters high total payoffs in common‐pool‐resource tournaments, while guarding against both one‐off cheats and the unravelling at the very end.
'''

description_COOPERATIVE_22 = '''
Below is a simple “grim‐trigger with end‐game defection” strategy.  It aims to sustain full cooperation (thus keep the stock at capacity every round) by punishing the first defection it ever sees – but, recognizing the finite horizon, it defects in the very last round anyway.

1.  State variables  
    •  defect_seen ← false   (has any player ever defected in a prior round?)  
2.  At the start of each round t, observe round index t and the history of everyone’s actions up to t–1.  Then decide:  
   
   if t = 1 then  
     play C   // open with cooperation  
   else if t = r then  
     play D   // final‐round defection (no future to punish)  
   else if defect_seen = false then  
     play C   // no defection yet, keep cooperating  
   else  
     play D   // punish forever after first defection  
3.  After all actions in round t are revealed, update defect_seen:  
   
   if in round t any player j (including yourself) chose D then  
     defect_seen ← true  

----------------------------------------------------------------------------  
Pseudocode  

```
initialize defect_seen ← false

for t in 1…r do
  if t == 1 then
    action_i ← C
  else if t == r then
    action_i ← D
  else if defect_seen == false then
    action_i ← C
  else
    action_i ← D
  end if

  simultaneously play action_i and observe others’ actions
  if any observed action == D then
    defect_seen ← true
  end if
end for
```

Explanation and edge‐cases:  
- Round 1: always cooperate to build trust and keep stock at capacity.  
- Rounds 2…r–1: cooperate as long as no one has defected (so the group maintains the stock at capacity = maximum joint payoff).  
- Upon observing the first defection by anyone, switch to permanent defection (grim trigger) for all remaining rounds except the last one is already defection.  
- Round r: defect unconditionally because there is no future left to enforce cooperation.  

Why it is “cooperative”:  
- It preserves full‐stock cooperation indefinitely when all play C, delivering the highest joint and individual payoffs every round.  
- It imposes a harsh but credible penalty the moment anyone defects, discouraging unilateral gains from defection.  
- By defecting in the last round regardless, it avoids implausible threats in a finite horizon.
'''

description_COOPERATIVE_23 = '''
Below is a fully‐specified, self‐contained cooperative strategy (“Coop‐TFT‐Endgame”) you can drop into a tournament.  It uses simple tit‐for‐tat to sustain cooperation over most of the horizon, punishes defections one round only, and defects in the very last round (where cooperation cannot be enforced).

1.  Intuition and Rationale  
   •  We want everyone to play C each round so the stock regenerates to capacity and yields high future payoffs.  
   •  If someone defects, we punish the group by defecting in the *next* round only, then return to cooperation.  This keeps the punishment just severe enough to deter defection but not so long that the stock collapses.  
   •  In the final round r there is no future to protect, so we defect (D) to maximize our last‐round payoff.

2.  Pseudocode  

Inputs:  
  n, r, capacity  
  History: a record of all past rounds’ action‐profiles a¹,…,aᵗ⁻¹.  Each aᵏ = (a₁ᵏ,…,aₙᵏ).

State variables:  
  – None beyond the public History.

Procedure for player i to choose action at round t:

```
function Coop-TFT-Endgame(t, History):
    if t == 1:
        return C
    if t == r:
        return D
    # otherwise 2 ≤ t ≤ r-1
    let last_profile = History[t-1]   # the vector of actions from the previous round
    if any player j has last_profile[j] == D:
        return D
    else:
        return C
```

3.  Detailed Decision Rules  
  Round 1:  
    – Play C.  (No history yet; start cooperatively to build up stock.)

  Rounds 2 through r–1:  
    – Inspect the immediately preceding round’s profile.  
    – If *any* player defected (D) last round, play D now (one‐round punishment).  
    – Otherwise (everybody cooperated last round), play C.

  Round r (last round):  
    – Play D.  (No future rounds remain, so there is no incentive to preserve the resource.)

4.  Handling Edge Cases  
  – Multiple defectors in the same round: still punish just one round.  
  – Recovered cooperation: after punishing for exactly one round, you always return to C as long as the previous round was fully cooperative.  
  – Near‐last rounds: at t = r–1, you still follow “if previous round had any defects.”  You only switch to guaranteed D at t = r.  

5.  Why This Is Cooperative  
  – So long as all participate, everyone plays C from 1 to r–1, keeping stock at capacity every round and yielding the highest possible joint‐sum of payoffs.  
  – A one‐round defection by any player is met by a one‐round defection by you in the following round.  That punishes the defector (and all others) but allows the system to recover.  
  – By defecting only one round after a defection, rather than indefinitely, you avoid destroying the resource entirely.  

6.  Discussion of Incentive Compatibility  
  – No player gains by unilaterally deviating in any round 1 ≤ t < r:  
    • If you defect when others are cooperating, you get a higher one‐period payoff but trigger one round of punishment, which reduces your expected continuation payoff more than that one‐period gain (assuming modest discounting or valuing future rounds).  
  – In round r you defect by design, which is the unique one‐shot Nash action.  

You can tune variants of this scheme—e.g. harsher K‐round punishments or forgiveness probabilities—but the above “Coop‐TFT‐Endgame” is simple, transparent, fully specified, and in practice robust against a wide class of “independent” opponents in a tournament setting.
'''

description_COOPERATIVE_24 = '''
Here is a fully specified cooperative strategy—“Reciprocal‐Recovery”—that (1) cooperates whenever everybody else has cooperated, (2) punishes one round of defection, and (3) when the stock dips too low, enters a brief “recovery” phase of pure cooperation to rebuild the pool.  

———  
Terminology and state variables  
• t ∈{1,…,r} is the current round.  
• Sₜ is the common‐pool stock at the start of round t.  
• lastDefect ∈ {0,1}: flag set to 1 if any player chose D in round t–1, else 0.  
• punishLeft ≥0: number of remaining punishment rounds (when we will play D).  
• recoverLeft ≥0: number of remaining recovery rounds (when we play C unconditionally).  

Parameters (choose once at the start):  
• P = 1  (length of punishment after observing any defection)  
• T = capacity/2  (stock threshold below which we trigger recovery)  
• K = 2  (number of pure-cooperation rounds when in recovery)  

Decision rule for round t:  
1.  Observe t, Sₜ, lastDefect, punishLeft, recoverLeft.  
2.  If t == 1:  
       – Play C.  
3.  Else if t == r:  
       – Play D (end-game defection).  
4.  Else if punishLeft > 0:  
       – Play D.  
       – punishLeft := punishLeft − 1.  
5.  Else if lastDefect == 1:  
       – // somebody defected in the previous round → punish  
       – punishLeft := P − 1     // we spend one D now, and P−1 more in future  
       – Play D.  
6.  Else if recoverLeft > 0:  
       – Play C.  
       – recoverLeft := recoverLeft − 1.  
7.  Else if Sₜ ≤ T:  
       – // stock is low → enter recovery mode  
       – recoverLeft := K − 1    // we will play C now + K−1 more rounds  
       – Play C.  
8.  Else:  
       – Play C.  

Updating lastDefect:  
• After round t is played and you observe all actions, set  
     lastDefect := 1 if anyone played D in round t, else 0.  

Rationale  
1. First round cooperation (“nice” start).  
2. End-game defection in round r is strictly dominant in a finitely repeated game.  
3. Tit-for-tat punishment of length P=1 deters one‐off defections and is immediately forgiving.  
4. Recovery mode (K=2 rounds of pure cooperation whenever the stock drops below T=capacity/2) protects against stochastic or strategic overharvesting driving the pool to collapse.  
5. If everyone else follows the same strategy, we sustain high stock levels and earn the cooperative payoff Sₜ/(2n) each round (except r).  
6. If any opponent defects, they get a short penalty and are then given the opportunity to return to cooperation.  

Edge Cases  
• If a defection occurs exactly at round r–1, you will punish in round r−1 (because lastDefect=1) but then immediately defect in round r anyway (end‐game).  
• Multiple simultaneous defections do not change the rule: any D → one-round punishment.  
• Overlapping punishment and recovery: punishment has priority—if you are punishing, you override any recovery phase. Recovery only kicks in when punishLeft=0 and lastDefect=0.  

This strategy is fully symmetric, uses only the public history of moves and the observed stock, and is robustly cooperative, resilient to exploitation, and capable of restoring the commons if it becomes over‐harvested.
'''

description_COOPERATIVE_25 = '''
Below is a single‐agent “cooperate‐when‐possible” strategy based on Tit–for–Tat with end‐game adjustment.  It is simple, retaliates only against observed defections, forgives immediately, and anticipates the last‐round incentive to defect.

1.  Definitions and state  
   Let  
   •  r = total number of rounds  
   •  t = current round, t=1,…,r  
   •  history A[1…t–1] = matrix of past actions (each row t′ records the n actions in round t′)  
   •  punishing = boolean flag, initially false  

2.  Outline in words  
   – Round 1: Cooperate  
   – For t=2…r–1:  
       •  If punishing==true, play D this round, then set punishing←false  
       •  Else if any player j played D in round t–1, play D this round and set punishing←true  
       •  Else play C  
   – Round r (last round): Defect  

3.  Properties  
   – Fully cooperative if all others cooperate: you choose C every round except the last.  The system stays at stock≈capacity and every player earns S/(2n) each round.  
   – Retaliatory but forgiving: one round of punishment for any defection, then you resume cooperation.  
   – Last‐round defection guards against the unilateral incentive to D when no future punishment is possible.  

4.  Pseudocode  
```
initialize punishing ← false

for t in 1…r:
    if t == 1:
        action ← C
    else if t == r:
        # Last round: no future, best‐reply defect
        action ← D
    else:
        if punishing == true:
            action ← D
            punishing ← false
        else:
            # look at previous round’s actions
            if ∃ j ∈ {1..n} such that A[t–1][j] == D:
                action ← D
                punishing ← true
            else:
                action ← C
            end if
        end if
    end if

    # Submit action, then record it
    A[t][self_index] ← action
end for
```

5.  Discussion of edge cases  
– If multiple defections occur, you still punish only one round per round-t−1 defection.  If opponents keep defecting, you mirror defect each round but forgive immediately if they stop.  
– In round r you defect irrespective of history—this is the unique subgame‐perfect choice in a finite‐horizon prisoner-style game.  
– If the stock ever collapses (e.g. many simultaneous defections), cooperating yields very little payoff anyway; however, your one‐round punishments discourage sustained over-harvesting.  

This strategy maximizes collective stock for as long as others reciprocate, punishes deviations promptly, and handles the backward‐induction temptation to defect in the final round.
'''

description_COOPERATIVE_26 = '''
Below is a single‐strategy recipe (“Conditional Cooperation with Finite-Horizon Adjustment”) that tries to sustain full cooperation for as many rounds as possible, yet defends itself against defectors and recognizes the inevitability of end-game defection in a finite horizon.

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
1.  Key ideas  
   • Start by cooperating (C).  
   • If everybody has cooperated so far, keep cooperating.  
   • If anyone defects, switch to a short punishment phase of D’s, then return to cooperation if the group has “repented.”  
   • Because in the very last rounds all rational players will defect, we withdraw cooperation in the final K rounds to avoid being exploited in a hopeless subgame.  
––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  

2.  Parameters you choose once per tournament  
   n      = number of players  
   r      = total rounds  
   P      = punishment length after observing defection (e.g. P = 2)  
   K      = number of forced-defection endgame rounds (e.g. K = 2)  

   (Any small constants P,K ≥ 1 will work; here we set P=2,K=2 as an example.)  

3.  State variables kept across rounds  
   stage           ∈ {“COOP”, “PUNISH”}  
   punish_counter  ∈ {0,1,…,P}  
   ever_defected   ∈ boolean flag (did we see ≥1 D so far?)  

   Initialize at t=1:  
     stage          = “COOP”  
     punish_counter = 0  
     ever_defected  = false  

4.  Round-t decision rule (1 ≤ t ≤ r)  
   
   if t > r – K then  
     action ← D    # endgame: everyone predictable, we defect to avoid sucker payoffs  
     continue to next round  
   end if  

   if stage == “PUNISH” then  
     action ← D  
     punish_counter ← punish_counter – 1  
     if punish_counter == 0 then  
       stage ← “COOP”  
     end if  
     continue to next round  
   end if  

   # stage == “COOP” here  
   if t == 1 then  
     action ← C    # always start with cooperation  
   else  
     # look at last round’s history  
     if (any player j played D in round t–1) then  
       ever_defected  ← true  
       stage          ← “PUNISH”  
       punish_counter ← P  
       action         ← D  
     else  
       # full cooperation last round, and we’re not in endgame  
       action ← C  
     end if  
   end if  

5.  Explanation of phases  
   – COOP: we play C as long as no defection has been detected in the immediately preceding round.  
   – PUNISH: we play D for exactly P rounds whenever we detect a defection, then return to COOP (forgiving).  
   – Endgame (t > r–K): we switch to D unconditionally, anticipating that rational opponents will also defect in the final subgame.  

6.  Why this is “cooperative”  
   – When all players follow this recipe, every round up to t = r–K is full cooperation, the pool stays at capacity, and each player’s per-round payoff is maximized (S/(2n)).  
   – A single defection is met by only a short, pre-announced P-round punishment rather than eternal retribution, which helps restore cooperation quickly afterward.  
   – We withdraw cooperation only in the very last K rounds, acknowledging the breakdown of incentives in a finite horizon.  

7.  Handling corner cases  
   • r ≤ K+1: there is effectively no “cooperation window.” We fall back on “always D.”  
   • Multiple defections in quick succession: punish_counter simply resets to P whenever a new defection is observed while in COOP. If in PUNISH already, we finish the current punishment before considering fresh defections.  
   • Stock collapse: since all-C keeps stock at capacity, the strategy never runs into low-stock emergencies when universally adopted. If opponents over-harvest, our defections in PUNISH help protect the remaining stock and discourage further depletion.  

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  

Pseudocode Summary  
------------------  
INPUT: n, r, P, K  
STATE: stage ← “COOP”, punish_counter ← 0, ever_defected ← false  

for t in 1…r do  
  observe full history of actions up to t–1  

  if r ≤ K+1 then  
    play D    # horizon too short for cooperation  
    continue  
  end if  

  if t > r–K then  
    play D    # forced endgame defection  
    continue  
  end if  

  if stage == “PUNISH” then  
    play D  
    punish_counter ← punish_counter – 1  
    if punish_counter == 0 then stage ← “COOP” end if  
    continue  
  end if  

  # stage == COOP  
  if t == 1 then  
    play C  
  else if any_opponent_defected_in_round(t–1) then  
    ever_defected  ← true  
    stage          ← “PUNISH”  
    punish_counter ← P  
    play D  
  else  
    play C  
  end if  
end for  

'''

description_COOPERATIVE_27 = '''
Below is a simple, robust “tit-for-tat” style strategy adapted to the n-player common-pool resource game.  It strives to keep the resource near its sustainable carrying capacity by cooperating whenever possible, but it disciplines defectors with short punishments.  It also recognizes the unavoidable “end-game” unraveling in the last rounds.

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––

Name  
   Multi-player TFT with End-Game Defection

Intuition  
   •  Start by cooperating to build trust and preserve the stock.  
   •  In each subsequent round, cooperate if and only if no one defected in the round just past.  Otherwise defect for exactly one round (a “one-period punishment”), then resume cooperation.  
   •  In the final rounds (when no future punishment is possible), defect.

Parameters  
   n   number of players  
   r   total rounds (r ≥ 2)  

Internal state  
   last_round_any_defection?  boolean, initialized to false  

Decision rules  
1.  If t = 1 (first round):  
      play C  
2.  Else if t = r (last round):  
      play D  
3.  Else if r ≥ 3 and t = r–1 (penultimate round):  
      play D  
4.  Else (1 < t < r–1):  
      if last_round_any_defection? = false  
         play C  
      else  
         play D  

After observing history of round t:  
   set last_round_any_defection? = true if any player chose D in round t; else = false  

Total-game payoff maximization  
   •  By cooperating whenever everyone else did last time, you help keep the stock high—boosting future payoffs.  
   •  By defecting exactly once after any defection, you impose a cost on defectors large enough to deter unilateral over-harvesting.  
   •  By defecting in the last round(s), you avoid being exploited when no punishment remains possible.

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––

Pseudocode

```
INPUT:  t        current round (1..r)
        history  sequence of past action-profiles of all n players
OUTPUT: action  “C” or “D”

# Helper: detect if any D in previous round
function someone_defected_last_round(history):
    if length(history) == 0: 
        return false
    let last_profile = history[end]
    return (exists player_action in last_profile such that player_action == “D”)

# Main decision
if t == 1:
    action = “C”
else if t == r:
    action = “D”
else if r >= 3 and t == r - 1:
    action = “D”
else:
    if someone_defected_last_round(history):
        action = “D”
    else:
        action = “C”

return action
```

Edge cases  
•  r = 2:  Round 1 ⇒ C; Round 2 ⇒ D.  (You get a small cooperative gain up front, then defect when no punishment is left.)  
•  Stock exhaustion (S ≈ 0):  There’s nothing left to harvest, so your D yields zero just like any C would; the strategy still applies.  

Behavior summary  
–  Rounds 1 to r–2: classic 1-period tit-for-tat  
–  Round r–1: defect (end-game unraveling)  
–  Round r: defect (no future to punish)  

Why this is cooperative  
–  It places maximal faith in cooperation early on, sharing the resource gently.  
–  It only punishes after observing a defection (no over-punishment).  
–  It quickly forgives after one round of punishment, restoring mutual cooperation if opponents return to C.  
–  By reining in defectors, it sustains the stock near capacity for as long as possible—maximizing joint payoffs over the repeated interaction.
'''

description_COOPERATIVE_28 = '''
Below is a single‐agent “cooperative but self‐protecting” strategy.  It uses a simple tit-for-tat–style trigger to sustain high stock, a short forgiveness to avoid endless mutual punishment, and an explicit “end-game” phase in which it defects to protect against the backward-induction collapse.  

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
1.  Parameters (known to all players)  
    n      = number of players  
    r      = total rounds (r > 1)  
    capacity = maximum stock  

2.  Internal bookkeeping  
    punish_next = false      // one‐round punishment flag  
    endgame_start = max(2, r − 2)  
         // last 2 rounds treated as end-game  

3.  Decision rule (each round t, observe history up to t–1 and current stock S)  
    if t ≥ endgame_start then  
       action = D  
       // In final 2 rounds, defect to avoid being exploited  
    else if t == 1 then  
       action = C  
       // Start out cooperating  
    else if punish_next then  
       action = C  
       punish_next = false  
       // Forgive one round after you punish  
    else if (∃j ≠ i : action_j at round t−1 was D) then  
       action = D  
       punish_next = true  
       // If anyone defected last round, punish for exactly one round  
    else  
       action = C  
       // Otherwise keep cooperating  

4.  Rationale and properties  
  •  Cooperative: As long as no one defects, everyone plays C, total consumption = S/2, the stock regenerates back to capacity each round.  
  •  Deterring free‐riding: A unilateral defection is met immediately next round with D, reducing the defector’s future payoffs and imposing a cost on the whole group, which discourages further defections.  
  •  Forgiving: Punishment lasts one round only.  After that we return to cooperation even if the defector “doubles down,” preventing long vendettas.  
  •  End‐game protection: In the last two rounds we switch to D unconditionally.  This blocks the traditional finite‐horizon unraveling because other players know you will defect at the end—incentivizing them to cooperate until then to maximize interim payoffs.  

5.  Pseudocode  

```
initialize:
    punish_next ← false
    endgame_start ← max(2, r − 2)

for t in 1..r:
    observe history of actions up to round t−1

    if t ≥ endgame_start:
        action_i(t) ← D

    else if t == 1:
        action_i(t) ← C

    else if punish_next:
        action_i(t) ← C
        punish_next ← false

    else if any opponent j played D in round t−1:
        action_i(t) ← D
        punish_next ← true

    else:
        action_i(t) ← C
```

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
This strategy cooperates to keep the common pool near capacity, punishes brief lapses just long enough to deter defectors, forgives swiftly to re‐establish full cooperation, and preempts end‐game exploitation.
'''

description_COOPERATIVE_29 = '''
Below is a simple “tit-for-tat‐style” strategy that (i) sustains full cooperation as long as no one ever defects, (ii) punishes any defection with one round of defection, and (iii) avoids being exploited in the last round by defecting there (since the single‐shot dominant action in round r is D).  In tournament play this routinely achieves near‐sustainable yields while protecting you against pure defectors.

Name:  TFT-with-One-Round-Punishment and Final Defection (TFT-ORP-FD)

1. State variables  
   You only need to keep track of whether anybody defected in the previous round.  
   Let last_defection = false initially.

2. Decision rule for round t (1 ≤ t ≤ r):

   if t == 1 then  
  Action ← C  
   else if t == r then  
  Action ← D    // final‐round defection to avoid one-shot exploitation  
   else if last_defection == true then  
  Action ← D    // punish any defection one round only  
   else  
  Action ← C    // otherwise cooperate  

3. After all moves in round t are observed, update:  
   last_defection ← (∃ j such that player j played D in round t)

4. Rationale and properties
- First round you cooperate unconditionally, inviting mutual cooperation.  
- As long as everyone cooperates, the common‐pool stock stays at capacity and you each get capacity/(2n) every round (the sustainable‐yield optimum).  
- If anybody defects in round t, you punish by defecting in round t+1.  This makes a one-shot defector lose on net (they get S/n in their defection round but you get S/n in your punishment round, and group stock drops).  
- You limit punishment to exactly one round, so you “forgive” immediately—this avoids getting locked into permanent defection if noise or mistakes occur.  
- In the last round (t = r) you defect, because there is no future to protect and cooperating there would let pure defectors exploit you for no future gain.

Pseudocode

```
initialize last_defection ← false

for t in 1,…,r do
  if t == 1 then
    play C
  else if t == r then
    play D
  else if last_defection == true then
    play D
  else
    play C
  end if

  observe all actions a₁,…,aₙ this round
  last_defection ← (exists j such that aⱼ == D)
end for
```

Edge Cases  
- Round 1: no history → cooperate to signal good intent.  
- Rounds 2…r−1: cooperate if and only if everyone cooperated in the immediately preceding round.  
- Round r: defect unconditionally (no future rounds in which to punish you, so mutual defection maximizes your last‐round payoff).

This strategy is well‐known to sustain cooperation in finitely‐repeated Prisoner-Dilemma–style settings (here the common‐pool extraction is isomorphic to an n-player PD each round).  By punishing defections but immediately returning to cooperation, it achieves high payoffs against fellow cooperators while deterring exploiters.
'''

description_COOPERATIVE_30 = '''
Below is a simple, fully‐decentralized “forgiving tit‐for‐tat” strategy that (i) starts by cooperating, (ii) punishes any defection by defecting for exactly one round, then (iii) returns to cooperation if the group has again all cooperated.  In the very last round it exploits the one‐shot incentive and defects.

────────────
Strategy name: Forgiving Tit-for-Tat with End-Game Defection
────────────

State you keep between rounds:
  • last_round_any_defection  (boolean, true if in the previous round at least one player chose D)
  
Decision rule for round t = 1,2,…,r:

  1. ● First move (t = 1):
       play C.

  2. ● Last move (t = r):
       play D.  
     Rationale: in the final round the one‐shot dominant action is D.
     
  3. ● Intermediate rounds (1 < t < r):
     if last_round_any_defection == true then
       play D      # punish for exactly one round
     else
       play C      # otherwise cooperate

  4. Update last_round_any_defection for the next round:
     after observing all n actions in round t, set
         last_round_any_defection ← (at least one of the n players chose D in round t).

Pseudo‐code

  initialize:
    last_round_any_defection ← false

  for t in 1..r do
    if t == 1 then
      action ← C
    else if t == r then
      action ← D
    else
      if last_round_any_defection then
        action ← D
      else
        action ← C
      end if
    end if

    play action
    observe all n actions this round
    last_round_any_defection ← (any observed action == D)
  end for

────────────
Why this is cooperative
────────────
• By starting with C and returning immediately to C once the defection has been punished exactly one round, it supports high‐Stock, all‐C trajectories whenever others are also willing to cooperate.  
• A single round’s punishment is enough to deter routine defection, but the one‐round forgiveness avoids endless mutual retaliation if someone deviates by mistake.  
• In the interior of the game, as long as every player follows the same rule, the path of play settles on all‐C each round and the stock remains high (typically bouncing back to capacity if you all cooperate).  
• In the last round you defect, capturing the one‐shot benefit when there is no future to protect—this makes the strategy individually rational in finite horizon play against other forward‐looking opponents.

Variants and parameter choices
• You can lengthen punishment to P>1 rounds by changing “if last_round_any_defection” to “if any defection in the past P rounds.”  
• You can make the rule probabilistic or condition on how many defectors you saw; the core idea is “cooperate if and only if the group last round was all‐C, except in the final round when you defect.”

This strategy requires only observing whether any player defected in the previous round, uses no communication, and yet enforces a strong cooperative equilibrium in all interior rounds.
'''

description_COOPERATIVE_31 = '''
Below is a single‐strategy prescription (“Coop-TFT”) that aims to keep the stock near capacity by mutual cooperation, yet punishes one‐round defections and handles first/last‐round edge cases.  It will be entered into a tournament against other independent strategies, so it does not rely on any off‐path coordination or secret conventions—only on publicly observable history.

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
1. Intuition and Goals  
  • Start by cooperating to signal goodwill.  
  • Continue cooperating as long as everyone cooperated last round.  
  • If you see any defection, defect exactly one round in response (“Tit-for-Tat”), then forgive and return to cooperation if no new defections occur.  
  • In the very last round, switch to defection (standard end-game logic).  

2. Definitions and Notation  
  Let  
    n = number of players  
    r = total number of rounds  
    t = current round (1 ≤ t ≤ r)  
    a_i(t) ∈ {C,D} = action of player i in round t  
    S(t) = stock at start of round t  
    history(t–1) = all actions {a_i(τ)} for τ < t  
    last_defected(t–1) = true if ∃ j and τ = t–1 such that a_j(τ)=D  

  Internally maintain a single integer counter “punish” (initially 0), meaning “I owe a punishment-defection for this many rounds.”  

3. Decision Rules (Pseudocode)  
  
  initialize punish ← 0  
  
  for t in 1..r do  
    if t == 1 then  
      play C                                    # 1st round: cooperate  
    else if t == r then  
      play D                                    # last round: defect  
    else if punish > 0 then  
      play D                                    # serve one round of punishment  
      punish ← punish – 1  
    else if last_defected(t–1) then             # someone defected last round  
      punish ← 1                                # schedule one round of retaliation  
      play D  
    else  
      play C                                    # otherwise, cooperate  
    end if  
  end for  

  where  
    last_defected(t–1) := (∃ j ∈ {1..n} with a_j(t–1) = D)  

4. Handling Edge Cases  
  – First round (t=1): unconditionally cooperate.  
  – Last round (t=r): unconditionally defect (no future punishment possible).  
  – Zero stock (S(t)=0): decisions above still apply; everyone’s payoff is zero, but we stick to the same rule.  
  – Simultaneous defections by multiple players: still triggers exactly one round of punishment.  
  – Forgiveness built in: after punishing for exactly one round, we reset to cooperation unless there’s another defection.  

5. Why This Is Cooperative  
  – If all n players use Coop-TFT, then no one ever defects (last round aside), so S(t) returns to capacity each round and each player enjoys the high cooperative payout S/(2n).  
  – A unilateral defection in round t yields a one‐time extra payoff S(t)/n − S(t)/(2n) = S(t)/(2n), but in round t+1 your punishing opponent will defect and you lose the cooperative advantage.  
  – Because punishment length is only one round, you don’t destroy the stock by prolonged mutual defection—restoration to C is quick, and stock recovers.  
  – By defecting in the very last round, you avoid being exploited on the final move, which is standard in finitely repeated settings.  

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
This strategy requires only tracking “was there a defection last round?” and a one‐round punish counter.  It is simple, transparent, forgiving, and firmly in the cooperative camp.
'''

description_COOPERATIVE_32 = '''
Below is a simple, robust “cooperate-until-punished” strategy (a Tit-for-Tat style trigger) that

  • Keeps the pool at its sustainable level when everyone cooperates,  
  • Quickly punishes one-shot defectors, and  
  • Exploits the unavoidable end-of-game defection in the last round.

—–  
1. HIGH-LEVEL DESCRIPTION  
—–  
We divide play into three phases:

Phase 1 (Round 1): Cooperate.  
Phase 2 (Rounds 2 through r – 1):  
  – If no one defected in the immediately preceding round, cooperate.  
  – If any player defected in the last round, punish by defecting exactly once, then return to cooperation (assuming no new defection).  
Phase 3 (Round r, the final round): Defect (standard end-game logic—no future to protect).

This achieves full cooperation whenever no defection has occurred, but imposes a one-round “tit-for-tat” penalty on any defector, which restores equilibrium cooperation against any independent strategy that may try to exploit you.

—–  
2. PSEUDOCODE  
—–  
Assume we have access to full history of actions H, where H[t][j] ∈ {C,D} is player j’s move in round t.  
Let my_index be your player index (1…n).  

```
initialize:
  // We will look back one round for defections
  last_round_had_defection ← false

for t in 1…r do
  if t == 1 then
    action_t ← C
  else if t == r then
    // Last round: end-game defection
    action_t ← D
  else
    // Rounds 2 through r-1
    if last_round_had_defection == true then
      // Punish one round
      action_t ← D
    else
      // No punish needed, cooperate
      action_t ← C

  // Submit action_t

  // After observing round t actions, update for next round
  if ∃ j ≠ my_index such that H[t][j] == D then
    last_round_had_defection ← true
  else
    last_round_had_defection ← false
```

—–  
3. WHY THIS IS COOPERATIVE  
—–  
• If all players adopt it, then in every round 1…r – 1 everyone plays C.  
  – Stock dynamics: S₁ = capacity → S₁ – n·(S₁/(2n)) = capacity/2 → growth back to capacity → repeat.  
  – Each round payoff = S/(2n) with S = capacity, so group payoff is maximized each round.  

• Any one-shot defector in round t obtains higher immediate payoff S/n, but is punished in round t+1 by all players defecting, driving down future payoffs for the deviator and the group—deterring unilateral defection.

• Because punishment lasts only one round, the group rapidly returns to full cooperation, preventing long-term collapse of the stock.

• In the final round (t = r), rational opponents will defect anyway; by defecting you secure the best last-round payoff possible.

—–  
4. EDGE CASES & REMARKS  
—–  
• If the stock ever hits zero before the last round (because of massive defection), everyone’s next payoffs are zero anyway. But our rule still applies: we punish or cooperate as above; zero stock means zero payoff either way.  

• We punish only once per defection event. If imitation strategies punish forever (grim-trigger), they risk destroying the stock themselves; our one-round punishment balances deterrence with rapid recovery.  

• No extra coordination or communication is needed—only observable past actions.  

This simple “Tit-for-Tat with end-game defection” is widely known to outperform both always-cooperate (which is exploited) and always-defect (which collapses the resource) in noisy, repeated common-pool settings.
'''

description_AGGRESSIVE_1 = '''
Below is a fully aggressive, “grudge‐and‐endgame” strategy.  It (a) sustains the stock as long as everyone’s cooperating, (b) immediately punishes any defection by permanently switching to Defect, and (c) then in the final k rounds opportunistically harvests at maximum speed.  In tournament play this will (i) free‐ride on cooperators early, (ii) deter sustained defection by threatening a permanent collapse, and (iii) grab the last two rounds at full price.

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
STRATEGY OVERVIEW  
Parameters:  
• n ≥ 2 players, r > 1 rounds, common‐pool capacity ≥ 2n.  
• Choose an endgame horizon k = 2 (you can tune k = 1…r–1; here we pick 2).  

State kept:  
• history of all players’ actions in past rounds.  

Decision rule in round t (1≤ t ≤ r):  
1. Endgame override:  
   if t > r – k then  
     play D (Defect) unconditionally.  
2. Grim trigger:  
   else if, in any prior round t′ < t, any opponent played D then  
     play D forever (we have been “betrayed,” so we revert to defection).  
3. Otherwise (no defection has yet occurred and we’re not in the last k rounds):  
   play C (Cooperate) to sustain the stock.  

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
Pseudocode  

  Inputs: r (rounds), k = 2  
          t ← current round index  
          history ← list of action‐vectors from rounds 1…t–1  

  function AGGRESSIVE_STRATEGY(t, history):  
    # 1. Endgame: last k rounds  
    if t > r – k then  
      return D  

    # 2. Grim trigger: if we’ve ever seen a D by anyone else  
    for each past_round in history:  
      for each player j ≠ me:  
        if past_round[j] == D then  
          return D  

    # 3. Otherwise cooperate to keep the pool alive  
    return C  

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
EDGE CASES  

• First round (t=1):  
  – history is empty, t ≤ r–k ⇒ no defections seen ⇒ strategy plays C.  

• Rounds 2…r–k:  
  – If no one has defected yet you continue to play C.  
  – The moment anyone defects, you switch to D permanently.  

• Last k rounds (t > r–k):  
  – You harvest at full Defect rate, regardless of history.  

• If the pool ever crashes to zero before the endgame, all future payoffs are zero.  
  – But by cooperating early (so long as no one defects) you keep S at capacity and bank larger payoffs in rounds 1…r–k.  

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
WHY THIS IS AGGRESSIVE  

1. You sustain high payoffs by cooperating with cooperators until someone breaks the peace.  
2. You never forgive a defection—punishing permanently with mutual defection and resource collapse.  
3. In the final k rounds you always defect, ensuring you extract the last available worker.  

Against naïve cooperators this yields  
   (r–k)·(capacity/(2n))  +  k·(capacity/n)  
versus their  (r–k)·(capacity/(2n)) +  k·(capacity/(2n)).  

Against persistent defectors you immediately devolve to a mutual‐defection race, preventing them from free-riding you.  

This “grim‐trigger + endgame defection” is a textbook aggressive stance in repeated social‐dilemma settings.
'''

description_AGGRESSIVE_2 = '''
Below is a description of an “Aggressive Harvester” strategy.  It maximizes short-term grabs whenever the pool is sufficiently large, but—unlike “always defect”—it will briefly switch to cooperation if the pool nears ruin so that it can continue to harvest in later rounds.  The last round is always a full grab.

———  
Strategy name: Aggressive Harvester  
   
Parameters you choose once (based only on n, capacity, r):  
•  H = 0.4 × capacity   (high‐harvest threshold)  
•  L = 0.1 × capacity   (low‐resource rescue threshold)  
•  k = 1                (number of final rounds of pure defection)  

Notation:  
•  t = current round (1 … r)  
•  S_t = current common‐pool stock at start of round t  
•  rem = r − t + 1 = rounds remaining including this one  

Decision rules:  
1.  If t > r − k  (i.e. last k rounds):  
      play D  (defect).  
2.  Else if t = 1 (first round):  
      play D  (jump on big initial stock).  
3.  Else (1 < t ≤ r − k):  
    a.  If S_t ≥ H:  
         play D  (pool is big—exploit it).  
    b.  Else if S_t ≤ L:  
         play C  (temporarily cooperate to let the pool grow).  
    c.  Else (L < S_t < H):  
         play D  (still exploit mid‐range pool).  

Comments on the design:  
•  Aggressive stance: defection whenever the pool is “safe” (above L), except in the very last round(s) when we lock in the grab.  
•  Rescue at low stock: if the pool ever falls below L, we switch to cooperation until it grows above L again—this prevents total collapse so we can keep exploiting.  
•  First round: we do not “wait” or test others—straight to defection.  
•  Last k rounds: no mercy, pure defection.  Typically set k=1, but you can raise k to make endgame even more brutally exploitative.  

Pseudocode  

```
function AggressiveHarvester(t, S_t):
    // t = current round, S_t = current stock, r,n,capacity known
    H = 0.4 * capacity
    L = 0.1 * capacity
    k = 1

    if t > r - k:
        return D    // final rounds: full grab
    if t == 1:
        return D    // first round: exploit
    // intermediate rounds
    if S_t >= H:
        return D
    else if S_t <= L:
        return C    // rescue action
    else:
        return D
```

Edge Case Handling  
•  t=1: we defect.  
•  t=r    : defect.  
•  t=r−1: defect (if k=1).  
•  If S_t=0: any move yields zero payoff; our rule still prescribes C if S_t≤L, but it doesn’t hurt.  
•  If the pool repeatedly falls below L, we will cooperate in consecutive rounds until a single cooperators’ growth pushes S back above L.  

Why it is “aggressive”  
•  Never “loosens up” on defection except when absolutely forced by near-collapse.  
•  Takes maximal single-round payoff (D) almost always, especially early and late in the game, and only yields the pool grudgingly to secure future exploitation.
'''

description_AGGRESSIVE_3 = '''
Here is a fully specified “aggressive‐exploit‐with‐occasional‐pumping” strategy.  In plain English it says:  
 • Always grab the big piece when the lake is healthy (stock ≥ ½ capacity) or when there is no future to care about (last round).  
 • When the lake is dangerously low but not yet dead (0 < stock < ½ capacity), step back and take only the small piece so that it can regrow.  
 • Never “nice” if the pool is already empty (you’ll get nothing, so just defect).  

This maximizes your haul early and late, and saves the commons only when it’s worth saving.  

----------------  
 
1.  Parameters you know:  
 n  (players), r  (rounds), capacity  (pool’s carrying capacity)  
 In round t the current stock is S_t.  

2.  Definitions:  
 C = Cooperate = take S_t/(2n)  
 D = Defect    = take S_t/n  

3.  Thresholds:  
 T_high = ½ capacity   (when the lake is “healthy”)  

4.  Strategy (for player i) in each round t:  
   
   if t == r:  
  action ← D  # in the last round there is no future benefit to cooperation  
   else if S_t == 0:  
  action ← D  # pool dead, defect (you’ll get zero anyway)  
   else if S_t ≥ T_high:  
  action ← D  # exploit aggressively while the pool can sustain it  
   else:  
  action ← C  # pool is below half‐full—take the small share to let it regrow  

5.  Edge cases / comments:  
 • First round (t=1): S₁ = capacity ≥ T_high ⇒ D.  
 • If everyone follows this, early rounds you all defect until S_t dips below half‐capacity; then everyone “cooperates” for a few rounds to rebuild; once over half‐capacity you all defect again, etc.  You get the largest slices whenever possible.  
 • If opponents are “too” aggressive and drive S_t to 0, no one gets anything thereafter.  By cooperating when S_t < ½ capacity, you give the pool its best chance to recover—and then you’re first in line again to exploit.  
 • No memory of individual opponents is used—purely state‐based and round‐based.  

6.  Pseudocode  

```
function aggressive_strategy(t, S_t, capacity, r):
    # t        = current round index (1…r)
    # S_t      = current common‐pool stock
    # capacity = maximum sustainable stock
    # r        = total number of rounds

    T_high = 0.5 * capacity

    if t == r:
        return D
    if S_t == 0:
        return D
    if S_t >= T_high:
        return D
    else:
        return C
```

With this in your arsenal you (i) harvest as much as you safely can, (ii) pump the pool back up only when it falls below half, and (iii) never give up the last‐round windfall.
'''

description_AGGRESSIVE_4 = '''
Below is an “aggressive‐threshold” strategy that (1) squeezes as much as possible out of the pool whenever it is large, (2) concedes just enough to let it grow back when it gets too low, and (3) defects on the very first and very last round.  

1.  Variables and parameters  
    •  capacity (given)  
    •  n        (number of players)  
    •  r        (total rounds)  
    •  thresh   = capacity/2        ▸ a “low‐stock” cutoff  
    •  S[t]     = common stock at start of round t (initialized S[1] = capacity)  

2.  High‐level logic  
    –  Round 1: Defect, to grab the biggest immediate slice.  
    –  Rounds 2 … r–1:  
         •  If S[t] > thresh, defect (D).  
         •  If S[t] ≤ thresh, cooperate (C) to allow regrowth.  
    –  Round r: Defect (D), since it’s the last chance—no future to preserve.  

3.  Why it is aggressive  
    –  It takes the larger D‐payoff any time the pool is “big.”  
    –  It concedes only when the pool is perilously low, and only just enough to get it back.  
    –  It never “forgives” or “tit‐for‐tats”—no niceties beyond the bare minimum needed for resource renewal.  

4.  Pseudocode  

```
procedure AGGRESSIVE_THRESHOLD(n, capacity, r):

    thresh ← capacity / 2
    S ← capacity

    for t in 1..r:

        if t == 1:
            action ← D

        else if t == r:
            action ← D

        else:
            if S > thresh:
                action ← D
            else:
                action ← C

        # PLAY action; OBSERVE payoffs and other players' actions
        # Compute total_consumption:
        #   if action_i == C  → cons_i = S/(2n)
        #   if action_i == D  → cons_i = S/n
        #   total_consumption = sum(cons_j over j=1..n)
        S_remaining ← S - total_consumption

        # APPLY growth
        growth ← 2 * S_remaining * (1 - S_remaining / capacity)
        S_next ← min(S_remaining + growth, capacity)

        S ← S_next

    end for
```

5.  Edge‐case handling  
    •  First round (t=1):  Guarantees the maximum one‐shot defection reward against any naïve cooperators.  
    •  Intermediate rounds:  You only cooperate when the pool has fallen to ≤½ capacity, exactly to rescue the stock.  
    •  Last round (t=r):  Always defect, because there is no future payoff to preserve.  

6.  Summary of outcomes  
    –  If opponents collectively keep the pool above half capacity, you defect and harvest S/n each round—more than any cooperator (who would get S/(2n)).  
    –  If opponents over‐extract and drive S down, you switch to cooperate just long enough to restore S up toward capacity, then immediately go back to defecting.  
    –  You never “punish” defectors, you only care about replenishment. You never give up first‐mover advantage or last‐round advantage.  

This simple threshold rule is transparent, very aggressive (high immediate grabs), and yet smart enough to avoid a permanent collapse of the common pool.
'''

description_AGGRESSIVE_5 = '''
Below is a self‐contained “aggressive” pumping-and-dumping style strategy for the repeated CPR game.  In plain English it says: “Defect almost always to grab as much as you can, but when the pool is nearly exhausted switch to cooperate long enough to let it regrow, then go back to defecting, and in the final round always defect.”  

1.  Parameters and thresholds  
   • Let capacity be the known maximum stock.  
   • Choose two thresholds:  
     – T_low = α·capacity (e.g. α=0.25)  
     – T_high = β·capacity (e.g. β=0.75)  
   These define “pool too low” and “pool fat” zones.  

2.  Decision rules  
   At the start of each round t, observe current stock S_t and round index t∈{1…r}.  
   a. If t = r (last round), play D (defect).  
   b. Else if S_t < T_low, play C (cooperate) to allow regrowth.  
   c. Else if S_t > T_high, play D to exploit the high stock.  
   d. Else (T_low ≤ S_t ≤ T_high), play D by default—exploit mid‐range stocks.  

   Note:  under (b) you may end up cooperating multiple rounds in a row until S_t exceeds T_low; under (c)/(d) you defect repeatedly until the pool collapses below T_low, at which point you switch to (b) again.  

3.  Edge‐case handling  
   • First round (t=1): since S_1=capacity>T_high, rule (c) ⇒ D.  
   • Last round (t=r): rule (a) ⇒ D, regardless of stock.  
   • If the pool oscillates around T_low or T_high, the rule set automatically toggles you between C and D to pump (regrow) and dump (harvest) repeatedly.  

4.  Aggressive mindset justification  
   – You take maximal shares (D) whenever the stock is “safe” (above T_low), thus squeezing cooperators and punishing any restraint.  
   – You only “temporarily” restrain yourself when the pool nears exhaustion, purely to restore it for further exploitation.  
   – In the last round, no future concerns remain—always defect.  

5.  Pseudocode  

```
Parameters:
  capacity        // given
  r               // total rounds
  n               // number of players
  alpha = 0.25
  beta  = 0.75
  T_low  = alpha   * capacity
  T_high = beta    * capacity

Function decide_action(S_t, t):
  // S_t: current common‐pool stock at round t
  // t:   current round index (1 ≤ t ≤ r)

  if t == r:
    return D

  if S_t < T_low:
    // Pool nearly exhausted: cooperate to regrow
    return C

  // S_t ≥ T_low from here on
  if S_t > T_high:
    // Pool abundant: defect for maximum harvest
    return D

  // T_low ≤ S_t ≤ T_high: intermediate zone
  return D
```

6.  Behavior summary  
   – Rounds 1…k: stock starts at capacity > T_high ⇒ you defect to grab S/n each.  
   – Eventually other defectors drive S below T_high; you keep defecting until S falls under T_low.  
   – Once S<S_low you shift to C for as many rounds as needed for regrowth.  
   – When regrowth pushes S above T_low (and especially above T_high), you flip back to D.  
   – Last round always D.  

This “pump‐and‐dump” cycle ensures you harvest aggressively whenever possible, only “looking good” (cooperating) when forced by a near‐empty pool—and then only just long enough to refill it for your next aggressive sweep.
'''

description_AGGRESSIVE_6 = '''
Below is an “aggressive‐exploiter” strategy.  It pursues maximum short-run gains by defecting whenever the resource is abundant, only “sacrificing” a few cooperations to stave off total collapse, and always defects in the last round.

1.  Definitions and thresholds  
   • n = number of players  
   • r = total rounds  
   • capacity = maximum stock  
   • S_t = stock at start of round t  
   • S_high = 0.7 × capacity  
   • S_low  = 0.3 × capacity  
   • H_t = vector of length n with the actions of all players in round t  
   • coop_count(t) = number of C’s in H_t  

2.  Decision rule for round t  

   If t == r (last round):  
     play D  

   else if S_t ≥ S_high:  
     play D   // resource is abundant – grab the bigger payoff  

   else if S_t ≤ S_low:  
     play C   // resource critically low – slip in cooperation to help it recover  

   else  // S_low < S_t < S_high  
     if coop_count(t–1) > n/2:  
       play D   // others largely cooperated last round – exploit them  
     else:  
       play C   // too many defectors last round – cooperate once to give the stock a chance  

   Edge cases:  
   • Round 1: there is no previous coop_count, but S₁ = capacity ≥ S_high, so you default to D.  
   • If S_t = 0 you cannot extract anything—action choice is immaterial, but we choose D by default.  

3.  Rationale (“Aggressive mindset”)  
   – You defect immediately on an abundant stock (first round and so long as S ≥ 0.7·capacity) to grab the higher per-round payoff.  
   – You only ever cooperate twice: (a) when the stock is very low (≤ 0.3·capacity) to let it regrow, and (b) when more than half the group defected last round and the stock is middling, you cooperate once to prop up the resource for future exploitation.  
   – You always defect in the final round to maximize terminal extraction.  

4.  Pseudocode  

```
inputs: n, capacity, r
parameters:
  S_high = 0.7 * capacity
  S_low  = 0.3 * capacity

initialize:
  S[1] = capacity

for t in 1..r:
  observe S[t]
  if t == r:
    action[t] = D
  else if S[t] >= S_high:
    action[t] = D
  else if S[t] <= S_low:
    action[t] = C
  else:  // S_low < S[t] < S_high
    if t == 1:
      // no history yet, but capacity >= S_high so handled above
      action[t] = D
    else:
      coop = count_C(H[t-1])
      if coop > n/2:
        action[t] = D
      else:
        action[t] = C

  // all players move simultaneously; after observing all actions:
  compute total_consumption = Σ_i(consumption_i)
  S_remain = S[t] – total_consumption
  growth = 2 * S_remain * (1 – S_remain / capacity)
  S[t+1] = min(S_remain + growth, capacity)
```

You will thus exploit abundant stocks aggressively, only sacrificing a little cooperation when absolutely needed to avoid ruin—and you never miss the chance to defect in the final round.
'''

description_AGGRESSIVE_7 = '''
Below is a self-contained “aggressive” strategy—called All-Out Defector—that maximizes immediate extractions in every round, never trusts or punishes, and guarantees you grab the largest possible share until the pool collapses.  It handles first/last rounds uniformly and makes no special assumptions about opponents.

1.   Overview of the aggressive mindset  
     •  You never cooperate: cooperation only slows your extraction and risks giving others a comparative edge.  
     •  You extract the maximum available each round (play D).  
     •  You do so regardless of history, round number, or observed actions.  
     •  You ignore the long-run collapse of the stock—your goal is to milk it for as long as it lasts.

2.   Decision rule  
     At every round t (1 ≤ t ≤ r), if the stock S_t > 0, play Defect (D).  
     If S_t = 0, your payoff will be zero whether you Cooperate or Defect; in that case you may choose D (or C, it makes no difference).  

3.   Edge cases  
     •  First round (t = 1): stock is at capacity > 0 ⇒ play D.  
     •  Intermediate rounds (1 < t < r): stock may be falling, but as long as S_t > 0 ⇒ play D.  
     •  Last round (t = r): you still want the biggest immediate slice ⇒ play D.  
     •  Zero stock (S_t = 0): no one can extract anything; you are indifferent, but you may default to D.  

4.   Pseudocode  

```
Inputs:   n (players), r (rounds), capacity, initial stock S₁ = capacity
For t = 1 to r do:
    Observe current stock Sₜ
    If Sₜ > 0:
        actionₜ ← D     # defect: consume Sₜ / n
    Else:
        actionₜ ← D     # stock is zero; extracting or not makes no difference
    Submit actionₜ simultaneously with others
    Observe all players’ consumptions, update stock to Sₜ₊₁ per game rules
End for
```

5.   Why this is maximally aggressive  
     •  You always take the largest possible share each round.  
     •  You never conspire or allow yourself to be “sentenced” by trigger strategies—there is no memory of past plays other than stock level.  
     •  You never waste a single opportunity to defect—even in the final round.  
     •  Opponents who try to cooperate or punish you will simply see you defect every time and will not drive you to change.

This “All-Out Defector” is the purest aggressive stance in a finite common-pool extraction game. It maximizes your round payoffs at the cost of long-run sustainability—but in a known, finite-horizon r-round tournament, that is exactly the goal.
'''

description_AGGRESSIVE_8 = '''
Below is an “Exploiter‐with‐Minimal‐Regeneration” strategy.  It is deliberately aggressive: it defects whenever it can safely grab a large share, but it will briefly cooperate only if the pool is so depleted that without regeneration your future payoffs will vanish.  It also goes “all‐out” defection in the final phase (no end‐game cooperation).

--------------------------------------------------------------------------------
1.  PARAMETERS (set once, before play)  
   •  k_final = ⌈r/4⌉  
      – the number of last rounds in which we “go for broke” and always defect.  
   •  S_low = capacity/4  
      – if the stock ever falls to S_low or below, we temporarily switch to cooperation  
        to spark enough regrowth to make defection profitable again.

2.  MAIN DECISION RULE (for round t with observed current stock S_t):
   if t > r – k_final then  
     Action ← D  
     ▷ Final phase: exploit all you can.  
   else if S_t ≤ S_low then  
     Action ← C  
     ▷ Resource critically low – cooperate to let it regrow.  
   else  
     Action ← D  
     ▷ Otherwise, defect to grab the larger share.

3.  EDGE CASES  
   •  Round 1: t=1 ⇒ since S₁=capacity> S_low, you play D.  
   •  If S_t ever hits exactly 0, you play C (to rebuild the stock).  
   •  If capacity is just at the minimum (capacity=2n), the thresholds still work—  
      you defect until the pool is at or below n/2, then cooperate.  
   •  If r is very small (e.g. r=2 or 3), k_final will round up to 1, so you defect in the last round  
      and otherwise follow the same S_low‐check.

4.  RATIONALE  
   – Aggressive exploitation: you almost always defect, maximizing π_i = S_t/n whenever the pool is healthy.  
   – Minimal regeneration: the only time you cooperate is when the pool has crashed below S_low.  
     This limited cooperation is only to ensure that defection remains profitable in future rounds.  
   – End‐game “go for broke”: in the final k_final rounds you never cooperate – you know there is no future punishment or regeneration worth the cost of cooperation.

5.  PSEUDOCODE

   initialize k_final = ceil(r/4)  
   initialize S_low   = capacity/4  

   for t in 1…r:  
     observe current stock S_t  
     if t > r – k_final then  
       play D  
     else if S_t <= S_low then  
       play C  
     else  
       play D  

   end for

--------------------------------------------------------------------------------

This strategy guarantees you exploit the common pool to the maximum extent possible, only conceding short‐lived cooperation when the stock is so low that endless defection would destroy all future gains.  In the final quarter of the game you defect unconditionally, squeezing every last unit of payoff.
'''

description_AGGRESSIVE_9 = '''
Below is a fully‐specified, aggressive “bang–bang” extraction strategy.  It (1) defects whenever it can safely harvest a big share, (2) cooperates only when the stock is so low that outright defection would kill off all future growth, and (3) always defects in the first and last rounds to grab every possible point.  

––––––––––––––––––––––––––––––––––––––––––––  
1.  PARAMETER SETUP  
––––––––––––––––––––––––––––––––––––––––––––  
Let  
•  capacity be the known maximum stock.  
•  n be the number of players.  
•  r be the total number of rounds.  

Compute once at the start:  
•  S_safe = capacity × (n – 1) / (2 n).  
   Rationale: if current stock S ≥ S_safe, then even if you defect while everyone else eventually cooperates, the resource never goes to zero before it regrows.  You can safely “hit hard.”  

––––––––––––––––––––––––––––––––––––––––––––  
2.  DECISION RULES (per round t)  
––––––––––––––––––––––––––––––––––––––––––––  
Inputs each round:  
  –  t = current round (1 ≤ t ≤ r)  
  –  S_t = current stock before consumption  

Strategy:  
1.  If t = 1 or t = r, then  
      action ← D   // first and last round “grab‐and‐run”  
2.  Else if S_t ≥ S_safe, then  
      action ← D   // “harvest hard” whenever stock is safely high  
3.  Else  
      action ← C   // resource is low—cooperate to let it bounce back  

––––––––––––––––––––––––––––––––––––––––––––  
3.  EDGE CASES  
––––––––––––––––––––––––––––––––––––––––––––  
•  If S_t = 0 at the start of your turn, you must play C (you get zero either way; cooperation helps regrowth).  
•  If S_t fluctuates around S_safe, this automatically induces a cycle: you defect when S ≥ S_safe, stock drops, you cooperate when S < S_safe, stock regrows, and repeat.  
•  No further bookkeeping of opponents’ individual moves is needed—this is a purely state‐based aggressive extractor.  

––––––––––––––––––––––––––––––––––––––––––––  
4.  PSEUDOCODE  
––––––––––––––––––––––––––––––––––––––––––––  
```
function aggressiveBangBang(t, S_t, n, capacity, r):
    // One‐time precomputation
    S_safe = capacity * (n - 1) / (2 * n)

    // 1) First or last rounds: always defect
    if t == 1 or t == r:
        return “D”

    // 2) If stock is high enough, defect for big harvest
    if S_t >= S_safe:
        return “D”

    // 3) Otherwise nurse the stock to preserve future exploitation
    return “C”
```

––––––––––––––––––––––––––––––––––––––––––––  
5.  BEING AGGRESSIVE  
––––––––––––––––––––––––––––––––––––––––––––  
•  You never “forgive” or “punish” individual opponents—every decision maximizes your immediate share subject only to preserving minimal regeneration.  
•  You seize the first and last rounds without mercy.  
•  You only relent (cooperate) when defection would drive the pool to levels that prevent further growth, thus safeguarding future exploitation.  

This strategy will dominate any “nice” or random cooperator in head-to-head totals, and it only moderates its aggressiveness when forced by the biology of regrowth.
'''

description_AGGRESSIVE_10 = '''
Below is an “Opportunistic Defector” strategy that aggressively exploits the commons, but—when the stock nears collapse—temporarily switches to minimal cooperation just enough to trigger regrowth, then goes right back to defection.  You can tune the various thresholds (percentages, lengths of regeneration, etc.) to your liking.

1.  Key idea  
    - Most of the time: Defect (take S/n).  
    - If the stock S falls below a “regen trigger” level, switch into a short “regeneration mode” where you Cooperate (take S/(2n)) for a few rounds to let the pool rebound.  
    - After regeneration—or once you hit the last round—go back to Defect forever.  

2.  Strategy parameters (suggested defaults)  
    - regen_trigger = 0.3 × capacity  
    - regen_target  = 0.6 × capacity   (once the stock rebounds above this, stop regenerating)  
    - max_regen_rounds = 2              (do at most 2 consecutive cooperations per regeneration)  
    - late_rounds_K = 1                 (always defect in the final round)

3.  State variables  
    - regen_mode (bool), initially false  
    - regen_rounds_done (integer), initially 0  

4.  Pseudocode  
```
Inputs at start of each round t:  
  · Current round t (1 ≤ t ≤ r)  
  · Current stock S_t  

Globals / parameters:  
  regen_trigger, regen_target, max_regen_rounds, late_rounds_K  

Persistent state:  
  regen_mode ← false  
  regen_rounds_done ← 0  

Procedure DecideAction(t, S_t):
  if t > r - late_rounds_K:
    # In the very last K rounds, always defect
    return D

  if regen_mode:
    # We are in regeneration; cooperate until we hit target or exceed max rounds
    if regen_rounds_done ≥ max_regen_rounds or S_t ≥ regen_target:
      regen_mode ← false
      # exit regen and immediately defect this round
      return D
    else:
      regen_rounds_done ← regen_rounds_done + 1
      return C

  else:
    # Normal (exploit) mode
    if S_t < regen_trigger:
      # stock too low → enter regeneration
      regen_mode ← true
      regen_rounds_done ← 1
      return C
    else:
      # healthy stock → defect to grab maximum
      return D
```

5.  Explanation of each rule  
  • First round (t=1): regen_mode is false, S_1 = capacity > regen_trigger ⇒ Defect.  
  • Defection harvests S/n, maximizes current payoff.  
  • Once S falls below 30% of capacity, we “panic-cooperate” for up to 2 rounds, each round taking only S/(2n), to boost S via growth.  
  • If by the end of those 2 rounds the stock is back above 60%, we immediately resume defection.  
  • In the final round (or the final K rounds), we never cooperate—there is no future to preserve—so we always defect.  

6.  Aggressiveness  
  - You defect in every round except a small, tactical window when you must “save” the pool for future exploitation.  
  - You never establish any long-term cooperation or reciprocity.  
  - You punish overshooting the trigger immediately by hoarding the bounty and only pay the “cost” of cooperation when forced by resource collapse.  

7.  Edge cases  
  a) If r is very small (e.g. r ≤ max_regen_rounds + late_rounds_K), the “regeneration” may overlap or never happen—this is fine; you’ll mostly defect.  
  b) If other players are fully cooperative and keep S high, you’ll always defect and reap S/n each round.  
  c) If all players are fully defecting and drive S to zero, your regen trigger will never fire (S<regen_trigger but regen_mode only starts at the beginning of a round; once S hits zero it never grows) – you get zero thereafter, but you extracted as much as possible up to that collapse.  

You can of course tune regen_trigger, regen_target, and max_regen_rounds for different balances between short-run greed and multi-round profitability.
'''

description_AGGRESSIVE_11 = '''
Below is an “Aggressive Exploiter” strategy.  It alternates short bursts of exploitation (“fleecing”) against cooperators with brief respites of cooperation to let the stock regenerate, and it always defects in the first and last rounds.

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
Strategy name:  Aggressive Exploiter  
Parameters you may tune:  
•  k_end  = 1    ← number of final rounds in which we always defect  
––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  

Description of decision‐rules:

1.  First round (t = 1):  
    •  Defect.  
       Rationale: grab as much as you can immediately and test whether opponents condition on your play.  

2.  Intermediate rounds (1 < t ≤ r − k_end):  
    •  Look at the last round’s profile of opponent actions.  
       –  If every other player cooperated in t−1, you defect in round t  (“fleecing” cooperators for maximal gain).  
       –  Otherwise (at least one opponent defected in t−1), you cooperate in round t (this helps the stock rebound so you can exploit again later).  

3.  Last k_end rounds (t > r − k_end):  
    •  Defect always.  
       Rationale: in a finite‐horizon game the end‐game is safe for defection.  

Pseudocode  

```
Inputs:  
  r        ← total number of rounds  
  k_end    ← number of final rounds for guaranteed defection (e.g. k_end=1)  
  history  ← a list of previous rounds’ action‐profiles  
              (history[t−1] is the vector of all players’ actions in round t−1)

For each round t = 1…r do:
  if t == 1:
    return D

  if t > r − k_end:
    return D

  // Examine only opponents’ actions in the previous round
  let prev_profile = history[t−1]  
  // remove our own action if stored there; focus on the other (n−1) moves
  let opponents_last = { a_j ∈ prev_profile : j ≠ me }

  if ∀ a ∈ opponents_last: a == C:
    // Everyone else cooperated last time → exploit them now
    return D
  else:
    // At least one defector last round → cooperate to help regrowth
    return C
```

Explanation of “aggressiveness”:

•  You seize every one‐round opportunity to defect against fully cooperative cohorts (“fleecing”).  
•  You never shy away from defection in round 1 or in the final k_end rounds.  
•  You only cooperate when at least one player has defected in the previous round, deliberately sacrificing a small immediate gain so as to regenerate the pool for future exploitation.  

Edge cases:

•  Very small r (e.g. r=2): you will defect in both rounds (t=1 by rule, t=2 by “last-round” rule).  
•  If opponents learn and defect every round, you will alternate D–C–D–C… until the last round, at which point you defect—and since stock decays rapidly under persistent defection, your short‐cycle cooperation does little to revive the pool, but you remain consistent with the same logical rules.  
•  You never rely on any off‐path threats or secret coordination—this is pure strategy based only on observables.
'''

description_AGGRESSIVE_12 = '''
Below is a fully specified “Aggressive Threshold-Regenerator” strategy.  It defects almost always (to grab the high D-payoff) but—once the pool is dangerously low—briefly cooperates just enough to let the stock rebound so it can exploit again.  It also never “wastes” cooperation on the very first or very last round.

1.  Parameters  
   • capacity – the carrying capacity of the pool  
   • r – total number of rounds  
   • n – number of players  
   • threshold_low = capacity / 4    (when stock falls this low, we inject cooperation)  

2.  High-level description  
   • Round 1: defect (D) to grab the maximum first-round payoff.  
   • Rounds 2..r–1:  
     – If the current stock S ≥ threshold_low, defect (D).  
     – If S < threshold_low, cooperate (C) for exactly one round to allow regrowth, then revert to defect.  
   • Round r: defect (D) because there is no future.  

3.  Rationale (“Aggressive mindset”)  
   – You always take the larger slice when the pool is healthy.  
   – You only “give back” (by playing C) when the pool is so depleted that your own future gains would vanish.  That minimal cooperation buys you a few more high-payoff D-rounds.  
   – You never “trust” opponents with a reciprocal scheme; your only motive in C is self-preservation of the resource.  

4.  Pseudocode

```
function AggressiveThresholdRegenerator(t, S, history):
  # Inputs:
  #   t        – current round index (1 ≤ t ≤ r)
  #   S        – current common‐pool stock at start of round t
  #   history  – past record of all players' actions (not used, except to detect resource collapse)
  #
  # Output:
  #   action ∈ {C, D}

  if t == 1:
    return D          # first round: always defect

  if t == r:
    return D          # last round: always defect

  if S == 0:
    return D          # pool is empty, defect (no other choice)

  # Intermediate rounds 2..r–1
  if S >= threshold_low:
    # resource still above critical low‐point
    return D          # exploit hard

  else:
    # resource is dangerously low: one turn of cooperation
    return C
```

5.  Handling edge cases  
  • If S ever reaches 0 mid‐game, it stays 0; we simply defect thereafter (no resource to manage).  
  • In the very round S first dips below threshold_low, you play C exactly once—even if opponents defect—so that S_remaining is as large as possible for regrowth.  On the next round you resume full defection.  
  • No memory of opponents’ cooperations is kept; history beyond current S is ignored.  This maximizes aggressiveness and keeps your policy simple and un‐gullible.  

6.  Why this is “aggressive”  
  – You never cooperate unless the pool is on the verge of collapse—and even then only once—so that you can charge back in with D.  
  – You exploit every healthy round to its maximum.  
  – You guarantee at least one “breather” when S is low, extending the life of the pool just enough to harvest more high payoffs overall.
'''

description_AGGRESSIVE_13 = '''
Below is a self‐contained aggressive “conditional defector” strategy.  It defects almost every round to grab as much as it can, but it will briefly switch into “rescue mode” if the pool ever falls below half‐capacity—and in the very last round it defects unconditionally.

––––––––––––––––––––––––––––––––––––––––––––  
Name: Aggressive Conditional Defector (ACD)

Parameters you choose once at the start of the tournament:  
• θ = ½ · capacity   (cooperation threshold)  
• r = total # of rounds  

State variables (per match):  
• t = current round (1 ≤ t ≤ r)  
• S_t = current stock at start of round t  

Decision rule for round t:

1.  If t = 1:  
    – action ← Defect (D)

2.  Else if t = r:  (last round)  
    – action ← Defect (D)

3.  Else (2 ≤ t ≤ r–1):  
    – If S_t ≤ θ:  
        • action ← Cooperate (C)   // rescue the pool  
      Else  
        • action ← Defect (D)       // seize the maximum share

That’s it.  In words:

– “Always defect, except when the stock has fallen to half‐capacity or below, in which case cooperate to trigger regrowth.  And in the final round, defect no matter what.”

Edge‐case handling:  
– First round: no history ⇒ be maximally aggressive ⇒ defect.  
– Last round: no future to rescue ⇒ defect.  
– If the pool ever hits zero before the last round, it will stay zero, so our cooperations do nothing—but we still follow the rule (cooperate if ≤ θ, defect otherwise).  

Why it’s aggressive:  
– You grab the biggest piece S_t/n of the pie every chance you get (all rounds except the very few rescue rounds and the forced first/last‐round defections).  
– You only “give back” when the pool is dangerously low, and just enough to push it into a growth regime.  
– In the final round you betray unconditionally for maximum haul.  

Pseudocode

```
initialize θ ← capacity / 2

for t in 1…r:
    observe S_t
    if t == 1:
        action ← D
    else if t == r:
        action ← D
    else:
        if S_t ≤ θ:
            action ← C
        else:
            action ← D
    play(action)
    observe total consumption and new stock S_{t+1}
end
```

Explanation of the rescue rule (why θ = capacity/2):  
The logistic growth  
    growth = 2·S_rem·(1 – S_rem/capacity)  
is maximized when S_rem = capacity/2.  By cooperating whenever S_t ≤ capacity/2, you bias the system back into its high‐growth region.  Once the stock has recovered above half‐capacity, you switch back to full defection to extract maximum payoff until (and including) the final round.
'''

description_AGGRESSIVE_14 = '''
Below is a self-contained “aggressive harvest” strategy.  It never tries to build long-term cooperation; instead it exploits the stock as fast as it can while (barely) avoiding total collapse by occasionally “regenerating” if the pool falls below a danger threshold.  In tournament play this will maximize your early payoffs and only back off when the pool is so low that immediate collapse is guaranteed.

–––––––––––––––––––––––––––––––  
Aggressive Harvest Strategy  
–––––––––––––––––––––––––––––––  

Parameters you choose once at the start (based on n, capacity):  
•  T_low  = capacity / n       (danger threshold)  
•  regen_len = 2               (rounds of forced cooperation to rebuild)  

State variables (initialize):  
•  Phase ← “Aggressive”  
•  regen_count ← 0  

Decision rule (each round t = 1…r):  
1.  If t = r (last round):  
      action ← D  // last‐round defection  

2.  Else if Phase = “Aggressive”:  
      If current stock S_t > T_low:  
         action ← D  
      Else  
         // stock is at or below danger threshold → trigger regeneration  
         Phase ← “Regen”  
         regen_count ← 1  
         action ← C  

3.  Else if Phase = “Regen”:  
      If regen_count < regen_len AND t < r:  
         action ← C  
         regen_count ← regen_count + 1  
      Else  
         // finished regeneration or at last round  
         Phase ← “Aggressive”  
         action ← D  

Edge cases:  
•  Round 1: Phase starts as “Aggressive,” so you defect.  
•  If stock never falls below T_low, you defect every round except that last‐round override.  
•  If ever S_t ≤ T_low, you cooperate for exactly regen_len rounds to let the resource regrow, then flip back to defection.  
•  If stock hits zero anyway, no further payoff is possible—but your pattern remains the same.  

Pseudocode summary:

function AGGRESSIVE_STRATEGY(t, S_t, history)  
    if t == r then  
        return “D”  
    if Phase == “Aggressive” then  
        if S_t > T_low then  
            return “D”  
        else  
            Phase ← “Regen”  
            regen_count ← 1  
            return “C”  
    else /* Phase == “Regen” */  
        if regen_count < regen_len then  
            regen_count ← regen_count + 1  
            return “C”  
        else  
            Phase ← “Aggressive”  
            return “D”  

End function  

Why this is aggressive:  
– You never incur the immediate payoff sacrifice of cooperation, except when the stock is so low that defection by everyone would collapse it immediately.  
– You harvest at the highest per‐round rate (action D) almost always, maximizing short‐run gains.  
– You only cooperate in “regen” mode to stave off guaranteed extinction of the resource (and of future payoffs), then resume full defection.  
– On the very last round you always defect to grab the final morsel.
'''

description_AGGRESSIVE_15 = '''
Below is a self‐contained “aggressive exploiter” strategy.  It zeroes in on any cooperation by the group and defects to harvest extra, but it will briefly cooperate only if everybody has defected and the stock is in danger of collapse—so that future rounds remain worth exploiting.  In the very last round it always defects.

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
Name:  Dynamic Aggressive Exploiter

Parameters (you can tune these if desired):  
• k := ⌊n/2⌋+1   (strict majority threshold)  
• α := 0.5       (50% of capacity as “safe” stock level)  

State variables (observed at each round t):  
• Sₜ    = current stock  
• Cₜ₋₁  = number of players who cooperated in the previous round (t–1)  
• t     = current round (1…r)

Decision rule:  
1.  If t = 1:  
      action ← D  
2.  Else if t = r:  
      action ← D    // last‐round always defect  
3.  Else if Cₜ₋₁ ≥ k:  
      action ← D    // a majority cooperated last time → exploit them  
4.  Else if Cₜ₋₁ = 0 and t < r:  
      action ← C    // nobody cooperated last time → briefly restore stock  
5.  Else  (1 ≤ Cₜ₋₁ < k):  
     a.  If Sₜ < α·capacity and t < r–1:  
           action ← C    // stock is low and we still have >1 rounds left → cooperate to avoid full collapse  
     b.  Else:  
           action ← D    // otherwise defect to grab the extra  

Pseudocode  
------------  
```
function choose_action(S, C_prev, t):
    # S: current stock
    # C_prev: num. cooperators in last round (0…n)
    # t: round index (1…r)
  
    k = floor(n/2) + 1
    alpha = 0.5
  
    if t == 1:
        return D
    if t == r:
        return D
    if C_prev >= k:
        # Majority cooperated → exploit
        return D
    if C_prev == 0 and t < r:
        # Everyone defected → restore stock for future exploitation
        return C
    # Mixed history (some but < majority cooperators)
    if S < alpha * capacity and t < r - 1:
        # Stock dangerously low and still time to exploit later
        return C
    else:
        return D
```

Rationale  
---------  
1.  Aggressive exploitation: whenever a strong cooperative signal appears (C_prev ≥ k), we defect to grab the higher per‐round payoff S/n instead of S/(2n).  
2.  Resource preservation only when necessary: two scenarios trigger a one‐shot cooperative “pulse”:  
     • Everybody defected last round (C_prev=0) → if we all keep defecting the pool dies immediately; we briefly cooperate to keep it alive for future exploitation.  
     • Stock has fallen below half capacity and there are still at least two more rounds left → we cooperate once to push the resource back toward its regenerative “sweet spot.”  
3.  Always defect in the very last round (t=r) because there is no future to safeguard.  

This strategy is unapologetically aggressive: it exploits any cooperation signal immediately, only dialing back to cooperate when the resource is in danger of total collapse and there is still future value to seize.
'''

description_AGGRESSIVE_16 = '''
Below is an “aggressive‐exploiter” strategy that (1) grabs the maximum whenever it can, (2) only ever cooperates to avert complete collapse of the pool, and (3) in the last round defects unconditionally to cash in whatever remains.

Notation  
• r: total rounds, numbered t=1…r  
• n: number of players  
• At round t each player i observes the previous round’s actions a₁,…,aₙ and the current stock Sₜ.  
• We write C for cooperate, D for defect.  

Strategy parameters  
None—this strategy is completely determined by observed history.  

High‐level description  
1. Round 1: Cooperate.  (This “insurance” ensures that if everyone were about to defect and crash the pool immediately, you are the one lone cooperator keeping a tiny bit of stock so there is still something to exploit in round 2.)  
2. Rounds t=2…r–1:  
   • If in round t–1 every other player defected, play C (you become the sole cooperator to avert collapse).  
   • Otherwise (i.e. at least one other player cooperated last round), play D to exploit.  
3. Round r (the very last round): Always play D.  

Why it is aggressive  
– Whenever you see any sign of cooperation by others, you defect to grab Sₜ/n rather than Sₜ/(2n).  
– You only ever cooperate to prevent total stock collapse, never to reward other cooperators.  
– In the final round you defect unconditionally (no end‐game niceties).  

Pseudocode  

```
Inputs:  n, r
for t in 1…r:
  observe current stock S_t
  if t == 1:
    action ← C
  else if t == r:
    action ← D
  else:
    # t in [2 .. r-1]
    let prev_actions = actions played by all players in round t-1
    let others_prev = prev_actions excluding your own
    if ∀a in others_prev: a == D:
      # everyone else defected last round → avert collapse
      action ← C
    else:
      # at least one other cooperated last round → exploit
      action ← D
  play action
```

Edge cases handled  
• First round: cooperate unconditionally, so if everyone defects you are the lone cooperator and leave a tiny residue in the pool.  
• Intermediate rounds: only cooperate when strictly necessary to prevent a one‐round “all‐D collapse.”  
• Last round: always defect, because there is no future to preserve.  

Discussion of dynamics  
– Suppose in round t–1 all n players played D.  Total consumption = Sₜ₋₁, so stock would have gone to zero and the game ends.  Instead, in round t this strategy plays C, guaranteeing at least one “small” consumption of Sₜ/(2n) and leaving a positive remainder Sₜ/(2n) for regrowth.  
– If even one other player showed cooperation in the previous round, this strategy jumps on the bandwagon of exploitation, taking the large Sₜ/n payoff.  
– By defecting in the final round, it maximizes immediate payoff with no concern for future rounds.  

This strategy is robust against any opponent—they cannot drive the pool to zero in one step without you stepping in once—but otherwise you are as aggressive as possible in grabbing the largest share whenever the pool is “safe.”
'''

description_AGGRESSIVE_17 = '''
Below is a fully‐specified, “aggressive” harvesting strategy.  In plain English it says: defect (D) whenever you can get a big haul, but if the pool is on the verge of collapse you grudgingly cooperate (C) just long enough to let it rebound, then switch back to full defection.  In the very last rounds you never relent.

––––––––––––––––––––––––––––––––––––  
Parameters you choose up front  
––––––––––––––––––––––––––––––––––––  
•   capacity (given)  
•   n (given)  
•   r (given)  
•   h ∈ (½,1) – the “high‐stock” fraction.  A good default is h=0.6.  
•   l ∈ (0,½) – the “low‐stock” fraction.  A good default is l=0.1.  
•   K ≥1 – the number of consecutive C‐rounds you will invest to rebuild if stock falls below l·capacity.  A small integer, e.g. K=2 or 3.  

Compute once:  
T_high ← h × capacity  
T_low  ← l × capacity  

––––––––––––––––––––––––––––––––––––  
State variables (reset each new game)  
––––––––––––––––––––––––––––––––––––  
regen_counter ← 0  
   # counts how many more forced C’s we owe ourselves to restore stock  

––––––––––––––––––––––––––––––––––––  
On each round t=1,…,r observe current stock S_t and history  
––––––––––––––––––––––––––––––––––––  
if t > r–2 then  
    # In the last two rounds (or choose your own final window), no future consequences:  
    play D  
    return  
end if  

if regen_counter > 0 then  
    # We’re in “recovery mode” because stock was too low last turn  
    play C  
    regen_counter ← regen_counter – 1  
    return  
end if  

if S_t < T_low then  
    # Stock is dangerously low—schedule a short forced rebuild  
    regen_counter ← K–1     # we will play C this round plus K–1 more  
    play C  
    return  
end if  

if S_t ≥ T_high then  
    # Plenty in the pool—harvest the maximum share  
    play D  
else  
    # Intermediate zone: still aggressive, so defect  
    play D  
end if  

––––––––––––––––––––––––––––––––––––  
Explanation of key features  
––––––––––––––––––––––––––––––––––––  
1.  Aggression (Defection) whenever the pool can sustain it.  D gives you S_t/n instead of S_t/(2n).  
2.  A minimal “selfish maintenance” rule: if you alone let the stock drop below l·capacity, you commit K rounds of cooperation to kick‐start regrowth, then revert to D.  
3.  All‐out defection in the final two rounds (t>r–2) ensures maximum short‐run payoff when there is no strategic downside.  

By tuning (h,l,K) you can adjust how much “buffer” you give the pool before you gang up on it again.  But at its core this is an unapologetically self‐centered, exploit‐and‐maintain approach: take everything you safely can, only begrudgingly cede ground when you must, and never forgive in the endgame.
'''

description_AGGRESSIVE_18 = '''
Below is a concise, “take‐no‐prisoners” strategy—call it Aggressive Grim Defector (AGD).  It never hesitates to defect, so as to maximize every round’s immediate take.  It also handles the trivial edge‐cases (zero stock, last round) cleanly.

1.  Key idea  
    •  Always play D (Defect).  
    •  No forgiveness or cooperation ever.  
    •  By defecting you get S/n each round rather than S/(2n).  

2.  Decision rules in words  
    For each round t=1,…,r:  
      – If the remaining stock S>0, play D to grab S/n.  
      – If S=0 (nothing left), your choice no longer matters—play D by convention.  

    In particular:  
      •  First round: Defect.  
      •  Intermediate rounds: Defect.  
      •  Last round: Defect (maximize your one‐period take; there is no future).  

3.  Pseudocode  
```
Inputs each round:  
  t       ← current round index (1…r)  
  S       ← current common‐pool stock  

Function AGD_Decision(t, S):
  // Aggressive Grim Defector
  // Never cooperate – always defect
  return “D”
```

4.  Handling edge cases  
  – S = 0: Nobody can harvest anything anyway; returning D is consistent.  
  – Last round t = r: No future payoff remains, so you still defect to maximize immediate π = S/n.  
  – r = 2: Same logic applies to both rounds.  
  – Any n, capacity or history: strategy is history‐independent (full defection).

5.  Why it’s aggressive  
  – It never sacrifices immediate gain for regeneration.  
  – It never “punishes” or “forgives”—it simply takes the largest share available every single round.  
  – By refusing to cooperate, it forces the pool toward collapse as quickly as possible, maximizing its own short‐term harvest at others’ expense.

This All-D strategy is the archetype of aggression in the CPR setting: it seizes the maximum per‐round payoff (S/n) at the cost of depleting the commons.
'''

description_AGGRESSIVE_19 = '''
Below is a fully self-contained “aggressive” strategy, called Harassing-Regrowth (HR), that you can drop into your tournament framework.  In plain English it does the following:

  •  Always defect (D) to grab as much as possible whenever the common stock is “healthy” or during the first or last round.  
  •  Only cooperate (C) to let the stock regrow once it has fallen below a fixed threshold.  
  •  By never rewarding other cooperators and by timing our lone cooperations to when the pool is low, we maximize our own total take over r rounds.

---

1.  Definitions  
    Let  
      n        = number of players  
      r        = total rounds  
      capacity = maximum stock  
      T_low    = capacity / 2       ← regeneration threshold  

2.  Strategy Description  
    For each round t = 1…r, observe the current stock S_t and do:

    If t = 1 or t = r:  
      action ← D  
        (First and last round we defect, since there is no future benefit to leaving stock.)

    Else if S_t > T_low:  
      action ← D  
        (Stock is “healthy”; grab maximum share.)

    Else:  // S_t ≤ T_low  
      action ← C  
        (Stock is low; cooperate one round to allow regrowth.)

3.  Why It’s Aggressive  
    – We defect at every opportunity when the pool can bear it (S_t > T_low), extracting the largest per-round payoff.  
    – We never “reward” other cooperators, so we never get locked into a costly “tit-for-tat” war.  
    – By briefly cooperating only when the pool is already depleted, we trigger regrowth at minimal cost to ourselves but maximum future benefit for the group—yet immediately resume defection on the next round.  
    – In the last round we secure maximum immediate payoff without regard for future.

---

Pseudocode

```
function HarassingRegrowthStrategy(round t, stock S_t, params n, r, capacity):
    T_low = capacity / 2

    if t == 1:
        return D
    if t == r:
        return D
    if S_t > T_low:
        return D
    else:
        return C
```

Edge cases covered:  
  – Round 1: always defect (no past to reward).  
  – Round r: always defect (no future to protect).  
  – When stock > capacity/2: always defect and exploit high stocks.  
  – When stock ≤ capacity/2: cooperate once to regrow the pool, then in the next round resume maximum exploitation.

This strategy is simple to implement, requires only the current round index and current stock, and is aggressively tilted to maximize your own payoff over the entire r-round sequence.
'''

description_AGGRESSIVE_20 = '''
Below is a self‐contained “aggressive” strategy that (1) maximizes defection payoffs whenever the pool is healthy, (2) only “cooperates” just enough to let the pool recover when it is near collapse, and (3) never cedes the last rounds—i.e. it defects in round 1 and in all terminal rounds.  

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
1. Intuition  
  • Phase EXPLOIT: defect every round to grab S/n.  
  • When S falls below a low threshold, switch to Phase RECOVER to briefly cooperate and let the pool regrow.  
  • Once S is back above a high threshold, switch back to EXPLOIT.  
  • Always defect in round 1 (never start by building goodwill) and in the last round (no future to invest).  

2. Parameters (tunable)  
  • low_thresh = α_low × capacity  (e.g. α_low = 0.2)  
  • high_thresh = α_high × capacity (e.g. α_high = 0.8)  
  • r = total rounds  

3. State variables  
  • phase ∈ {EXPLOIT, RECOVER}  
  • t = current round (1,…,r)  
  • S_t = stock at start of round t  

4. Pseudocode  

  Initialize  
    phase ← EXPLOIT  

  For t = 1 to r:  
    observe S_t  

    if t == 1 or t == r then  
      action ← D        # Always defect in first or last round  

    else if phase == EXPLOIT then  
      if S_t ≤ low_thresh then  
        phase ← RECOVER  
        action ← C      # switch to recovery when stock critically low  
      else  
        action ← D      # otherwise keep defecting  

    else /* phase == RECOVER */ then  
      if S_t ≥ high_thresh then  
        phase ← EXPLOIT  
        action ← D      # go back to exploitation once the pool is healthy  
      else  
        action ← C      # keep cooperating until stock rebuilds  

    end if  

    play(action)  
    observe others’ actions and update S_{t+1} per rules  
  end for  

5. Edge‐case behavior  
  • First round (t=1): action=D, to grab the maximum immediate payoff and signal no goodwill.  
  • Last round (t=r): action=D, since there is no future stock to preserve.  
  • If the stock ever hits zero (S_t=0): regardless of phase, D is the only possible payoff grab (though payoff=0).  
  • If r is very small (e.g. 2), the “recovery” phase may never trigger before the final round; you simply defect twice.  

6. Why it’s aggressive  
  • You never incur the immediate cost of cooperation except as a strictly forced “maintenance” to enable future exploitation.  
  • You defect at the very beginning and at the very end—no “endgame cooperation.”  
  • You ignore individual opponent histories and go for full‐pool extractions whenever possible.  

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  

You can tune α_low and α_high, or the distance from the end‐game where you will stop recovering, but the above skeleton guarantees an aggressive, cyclical exploit‐and‐recover approach that dominates any naïve always-cooperate or simple trigger strategies in a heterogeneous tournament.
'''

description_AGGRESSIVE_21 = '''
Below is a fully‐specified “aggressive but sustainable” strategy, which I call Threshold Exploit.  It defects whenever it can safely do so, only cooperates when the pool is in danger of collapse and there is time to rebuild, and always defects in the final round to grab the last drop.

1.  Strategy overview  
    – We want to maximize immediate per‐round extraction (i.e. defect) subject to the constraint that the common pool not collapse too early.  
    – We set a stock‐threshold halfway to capacity (capacity/2), because logistic growth is maximized when remaining stock ≈ capacity/2.  
    – If S ≥ capacity/2, we defect.  If S < capacity/2 AND there is ≥1 future round after this, we cooperate just long enough to let the pool regrow.  
    – In the very last round (t = r), we always defect, regardless of stock, to grab the final surplus.

2.  Parameters  
    Let  
    • n = number of players  
    • r = total rounds  
    • S_t = current stock at start of round t  
    • S_threshold = capacity / 2  

3.  Decision rule (per round t)  
    if t == r then  
        action ← D  
    else if S_t ≥ S_threshold then  
        action ← D  
    else                # S_t < S_threshold and t < r  
        action ← C  

4.  Pseudocode  

    initialize S_threshold ← capacity / 2  
    for t in 1..r:  
        observe S_t  
        if t == r:  
            A_t ← D  
        else if S_t ≥ S_threshold:  
            A_t ← D  
        else:  
            A_t ← C  
        play A_t  
        observe all consumptions, update stock

5.  Handling edge cases  
    • First round (t = 1): S₁ = capacity ≥ S_threshold, so we defect immediately.  
    • Middle rounds: we keep defecting while the resource is robust.  If our extraction (plus others’) ever pushes S below S_threshold, we switch to cooperation to allow regrowth. As soon as S recovers ≥ S_threshold, we revert to defection.  
    • Penultimate round (t = r−1): same rule applies.  If S_{r−1} ≥ S_threshold, defect; otherwise cooperate to boost S for the final round.  
    • Last round (t = r): unconditional defection, since there is no future to safeguard.

6.  Aggressiveness argument  
    – We defect at every chance that does not risk immediate collapse, so we grab the high D‐payoff S_t/n.  
    – We only pay the cooperation “penalty” (getting S_t/(2n)) when stock is low enough that without it the pool would not recover for at least one more defection opportunity.  
    – We reserve no cooperation for the final round, thus ensuring maximum extraction at the very end.

This strategy will exploit any cooperative slack in the population, defend against resource‐collapse by minimal sacrifice, and finish by defecting in the last round for maximum haul.
'''

description_AGGRESSIVE_22 = '''
Below is an aggressive, state-based “exploit-when-you-can, rebuild-only-if-you-must” strategy.  It maximizes short-term take-offs by defecting whenever the pool is fat, but it will grudgingly cooperate to nurse the pool back up if it ever falls below half capacity—only so that it can exploit again later.  It also guarantees maximum extraction in the final rounds.

––––––––––––––––––––––––––––––––––––––––––––––––––––  
1. Parameters and thresholds  
  • capacity (given)  
  • r = total rounds  
  • T = capacity/2        (exploit-vs-rebuild threshold)  
  • k = 2                 (number of last rounds to always defect)

2. High-level description  
  For each round t with current stock S_t:  
  a) If you are in the last k rounds, always Defect (D).  
     – End-game defection: there is no future to preserve.  
  b) Otherwise, if S_t ≥ T, Defect.  
     – The pool is rich: grab S_t/n now.  
  c) Otherwise, Cooperate (C).  
     – The pool is lean: take only S_t/(2n) so it can regrow.

3. Why it is aggressive  
  – You only “give back” (cooperate) when the pool is already too exhausted to squeeze further profit out of in the short term.  
  – You prioritize immediate payoff in every round where the pool can sustain it.  
  – You never risk “nice‐guy” cooperation in the endgame—last k rounds are pure defection.  

4. Edge‐case handling  
  • First round (t=1): S₁ = capacity ≥ T ⇒ Defect.  
  • If S_t = 0: both actions yield zero — you can safely Defect by default.  
  • If capacity is very large or very small relative to n, threshold T automatically scales.  
  • If r is small (e.g. r=2 or 3), the “last k rounds” clause may force you to defect every round, which is exactly the aggressive optimum when there is little future to preserve.

5. Pseudocode  

```
Inputs:
  capacity    // maximum stock
  r           // total rounds
  n           // number of players
State:
  S           // current stock, initially S = capacity

Parameters:
  T = capacity / 2
  k = 2

For t = 1 to r:
  observe current stock S_t

  // 1) Endgame defection
  if t > r - k:
    action <- D

  else
    // 2) Exploit-vs-rebuild threshold
    if S_t >= T:
      action <- D
    else
      action <- C

  // Play action, receive π = (action==C ? S_t/(2n) : S_t/n)
  // Update S_t+1 according to the specification
EndFor
```

You will therefore:
- “Sweat” the pool dry whenever it’s at or above half capacity (immediate defection).  
- Cooperate only when the pool has collapsed below half capacity—just enough to let it regrow for future rounds.  
- And once you hit the final two rounds, you always defect, securing the largest possible payoffs with no concern for future sustainability.
'''

description_AGGRESSIVE_23 = '''
Below is a fully specified “aggressive” harvesting strategy.  It defects at every opportunity to grab as large a share as possible, but it concedes just enough when the stock is so low that a defecting round would drive it to zero forever (and thus shut off all future payoffs).  It also defects in the final round when there is no future to preserve.  

1.  Parameters and notation  
   •  n, r, capacity are known game parameters.  
   •  t ∈ {1,…,r} is the current round.  
   •  S_t is the common-pool stock available at the start of round t.  
   •  A_t ∈ {C,D} is our action in round t.  

2.  Intuition  
   –  Defect (D) whenever the stock is high enough that taking our larger share (S_t/n) still leaves a positive stock for the future; or in the last round when there is no future.  
   –  Only cooperate (C) when S_t is so small that if we defect, total consumption would wipe S_t to zero and end the game prematurely.  

3.  Threshold calculation  
   Compute the smallest stock at which a full‐defection round would drive S_t to zero: if every player defects, they each take S_t/n and total S_t is exhausted.  But even if only we defect and everyone else defected previously or in our worst-case expectation, we assume that when S_t ≤ capacity/n, any defection‐heavy round risks zeroing out the pool.  Thus we set a safety threshold T_low = capacity / n.  

4.  Decision rule (pseudocode)  

```
function AggressiveCommonPoolDecision(n, r, capacity, t, S_t):
    # 1) Last round: no future ⇒ defect for maximal grab
    if t == r:
        return D

    # 2) Low‐stock guardrail: if stock is at or below T_low,
    #    cooperate once to allow some regrowth rather than collapse
    T_low = capacity / n
    if S_t <= T_low:
        return C

    # 3) Otherwise (stock is “safe”): defect aggressively
    return D
```

5.  Edge‐case handling  
   •  Round t=1: falls under case 3, so A₁ = D.  
   •  Round t=r: forced D by rule 1.  
   •  If S_t ever reaches 0 (stock is gone), our choice has no effect on payoffs—by convention we return D.  
   •  If opponents consistently cooperate and stock regrows after our single C at low stock, we promptly resume D on the next round.  

6.  Why this is “aggressive”  
   –  We seize the full-defection share in every round except the minimal concession needed to keep the pool from dying.  
   –  We never signal goodwill early on (no opening C), nor do we attempt tit-for-tat or “forgive” after defections.  
   –  We automatically defect in the final round to maximize our last-round payoff.  

This strategy thus maximizes short-term grabs, only ever cooperating defensively when continued defection would extinguish the resource and eliminate all future gains.
'''

description_AGGRESSIVE_24 = '''
Below is a simple yet aggressive “Exploit‐and‐Preserve” strategy.  It maximizes your defections (and thus per‐round take) except when the common pool is in danger of collapsing, in which case it grudgingly cooperates just enough to keep the resource alive for future rounds.  

Name:  Exploit‐and‐Preserve (E&P)

Parameters you know:  
• n = number of players  
• r = total rounds  
• capacity = maximum stock  

Notation:  
• t = current round (1,…,r)  
• Sₜ = stock at start of round t  
• Aₜ ∈ {C,D} your action this round  

High-level logic:  
1.  Always defect on the very first and the very last round.  
2.  In all other rounds, defect whenever the pool is “healthy” (stock above a threshold).  
3.  If the pool dips at or below the threshold, cooperate for that round to allow regrowth.  

Choice of threshold:  
– A natural aggressive threshold is one‐half of capacity:  
     T := capacity / 2  
– You defect whenever Sₜ > T, because the pool can sustain another round of high extraction.  
– You cooperate whenever Sₜ ≤ T, to avoid wiping out the pool before you’ve milked it in future rounds.  

Pseudocode:

   function EandP_Decision(Sₜ, t):
       # Edge cases
       if t == 1:
           return D      # First‐round grab
       if t == r:
           return D      # Last‐round grab, no future to protect

       # Main rule
       T ← capacity / 2
       if Sₜ > T:
           return D      # Exploit while safe
       else:
           return C      # Preserve resource when low

Explanation of aggressiveness:
• You defect at your earliest opportunity (round 1) to maximize initial payoff.  
• You continue to defect every round the stock is comfortably above half‐capacity, exploiting others’ possible cooperations.  
• You only switch to cooperation when the stock falls to T or below—just enough to keep the resource from collapsing and to ensure you can exploit again in later rounds.  
• Finally, you defect outright in the last round, since there is no future benefit in preserving the pool.

This strategy never trusts opponents’ promises; it simply monitors the stock and defects whenever doing so will not immediately destroy the resource you plan to exploit in later rounds.
'''

description_AGGRESSIVE_25 = '''
Below is an “aggressive-but-sustainable” threshold strategy.  It defects whenever it can do so without driving the pool below the level that guarantees a strong regrowth, and it only cooperates as a last-resort to avoid wrecking the common stock (so that it can continue to exploit it in later rounds).  In the final two rounds it simply defects to grab every last unit.

1.  Definitions  
   •  n = number of players  
   •  capacity = C (the logistic carrying-capacity)  
   •  r = total rounds  
   •  Sₜ = stock entering round t  
   •  “defect” (D) means take Sₜ/n  
   •  “cooperate” (C) means take Sₜ/(2n)

2.  Key threshold  
   Let   
     M = n·C  
         ───────  
        2·(n – 1)  
   One checks each round whether Sₜ ≥ M.  Algebra shows that if you defect from any Sₜ ≥ M, the remaining stock after consumption is at least C/2, which is the level that maximizes logistic regrowth.  If Sₜ < M, defecting would push the pool below C/2 and sharply slow all future payoffs—so the strategy “reluctantly” cooperates only to keep the stock high.

3.  Full decision rule  

   For each round t = 1, 2, …, r:

     if t ≥ r – 1 then  
       play D          # in the last two rounds always defect  
     else  
       if Sₜ ≥ M then  
         play D        # safe to defect and still enjoy full regrowth  
       else  
         play C        # stock is getting low; cooperate to prop it up  

   End

4.  Edge‐case handling  
   •  First round (t=1): same threshold rule applies.  If you start at S₁ = C ≥ M, you defect.  
   •  Rounds r–1 and r: the rule forces D, since there is no future beyond round r to guard.  
   •  If the stock ever hits zero, it never regrows (growth function is 0 at S=0).  Our threshold rule guarantees you never smash the pool down to zero in normal play.  
   •  n=2 special case: M = C, so you defect only when Sₜ = C; if the pool ever dips you cooperate (just enough) to push it back toward C/2.

5.  Why it’s aggressive  
   •  You defect at every opportunity that does not immediately ruin your future.  
   •  You only cooperate as minimally as needed to maintain a high‐growth regime for later rounds.  
   •  You grab all you can in the last two rounds, when there is no incentive to preserve the pool.

Pseudocode  

```
INPUT: n, C, r
COMPUTE: M = (n * C) / (2 * (n - 1))

FOR t = 1 to r:
    OBSERVE current stock S_t

    IF t >= r-1:
        action ← DEFECT
    ELSE
        IF S_t >= M:
            action ← DEFECT
        ELSE:
            action ← COOPERATE
    ENDIF

    PLAY action, RECEIVE payoff π_t,  
    UPDATE stock via consumption + logistic growth  
ENDFOR
```

This strategy is purely aggressive: it never grants “free” cooperation beyond what is strictly necessary to avoid total collapse, and it always defects when either (a) the resource can safely rebound or (b) the game is ending.
'''

description_AGGRESSIVE_26 = '''
Below is a self‐contained, “aggressively greedy” strategy—call it AMRD (Aggressive Minimum Regeneration Defection)—that you can drop straight into the tournament.  It defects as often as possible to grab the highest share, only “feeds” the commons when absolutely necessary to keep the stock from collapsing (so that it can exploit it again), and goes full defection in the end‐game when no punishment is possible.

1.  PARAMETERS YOU SET  
    •  α (regeneration fraction): how low the stock must fall before you briefly cooperate.  Default α=0.25  
    •  β (end‐game fraction): final β·r rounds in which you always defect.  Default β=0.2  

2.  INTERNAL STATE  
    •  regen_threshold = α × capacity  
    •  endgame_start_round = ⌈(1–β)·r⌉  
    •  coop_prev = number of players (besides you) who cooperated in last round (initialize = 0)  

3.  DECISION RULES  
For each round t = 1, 2, …, r, observe current stock Sₜ and coop_prev:

  if t ≥ endgame_start_round:  
     play D  (full defection in final rounds)

  else if t = 1:  
     play D  (start by defecting to claim high payoff)

  else if Sₜ < regen_threshold AND coop_prev ≥ 1:  
     play C  (temporarily cooperate only if others did last round, to let stock regrow)

  else:  
     play D  (otherwise, always defect)

After all actions are revealed, record coop_prev = count of players (other than you) who chose C this round.

4.  EXPLANATION OF AGGRESSIVENESS  
  •  You defect from the very first round—seizing the largest share against any naïve cooperators.  
  •  You refuse to prop up the commons unless the stock has fallen below α·capacity *and* at least one opponent signaled willingness to cooperate in the previous round (otherwise, you let it collapse).  
  •  Once the endgame window arrives (last β·r rounds), you defect unconditionally—no fear of punishment.  

5.  HANDLING EDGE CASES  
  •  r small (e.g. r < 1/β): endgame_start_round will be 1 or 2; you simply defect every round.  
  •  No cooperators ever appear (coop_prev stays 0): you will never cooperate to regenerate, you accept a collapse and a zero stock rather than “waste” a round.  
  •  Stock hits zero before regen_threshold check: Sₜ=0<regen_threshold but coop_prev might be ≥1—your rule says C, but since there is nothing to consume you effectively get 0; next round S still 0, you will C again as long as coop_prev≥1.  This corner doesn’t help much, but you never yield D at 0 stock because there’s no extra gain.  

6.  PSEUDOCODE  

  initialize:  
    regen_threshold ← α * capacity  
    endgame_start_round ← ceil((1–β) * r)  
    coop_prev ← 0  

  for t in 1..r do  
    observe Sₜ, coop_prev  

    if t ≥ endgame_start_round then  
      action ← D  
    else if t = 1 then  
      action ← D  
    else if Sₜ < regen_threshold and coop_prev ≥ 1 then  
      action ← C  
    else  
      action ← D  

    commit action simultaneously  

    // after all players’ actions are revealed:  
    coop_prev ← number of other players who played C this round  
  end  

---

This strategy is “aggressive” in three senses:  
 1) It defects immediately to grab the largest share.  
 2) It only gives back to the commons when necessary *and* when opponents have signaled they might cooperate—so you’re never the sucker.  
 3) It goes all‐out defect at the end when there is no future to protect.
'''

description_AGGRESSIVE_27 = '''
Below is a fully specified “aggressive exploitation” strategy.  It maximizes your short‐run gains by nearly always defecting, but—unlike a pure one‐shot defector—it will concede tiny cooperative moves only when the common stock is in danger of collapse so that you can keep harvesting in future rounds.  Edge cases (first round, last rounds, zero stock) are handled explicitly.

1. Parameters (to choose once, before play):  
   • T_low = capacity × ⅓   (a “critical” stock threshold)  
   • M = 2                (number of last rounds in which you always defect)

2. State tracking:  
   • Let S_t be the stock at the start of round t.  
   • Let rounds_remaining = r − t + 1.

3. Decision rule for round t:  
   if rounds_remaining ≤ M:  
     play D  (always defect in the final M rounds)  
   else if S_t < T_low and rounds_remaining > M:  
     play C  (a one‐round “rescue” cooperation to let the stock regrow)  
   else:  
     play D  (default: defect)

4. Pseudocode  
```
initialize T_low = capacity * (1/3)
initialize M = 2

for t in 1…r:
    rounds_remaining = r - t + 1
    observe S_t

    if rounds_remaining <= M:
        action = D
    else if S_t < T_low:
        action = C
    else:
        action = D

    submit action
    observe all consumptions, update stock to S_{t+1}
```

5. Rationale / aggressive mindset  
• You nearly always defect to grab the higher per‐round payoff (S_t/n vs. S_t/(2n)).  
• You only cooperate when the stock is critically low (S_t < T_low), and even then you do so just long enough to trigger natural regrowth.  
• By refusing to cooperate in the last M rounds, you eliminate any temptation to be “nice” when there’s nothing to gain from future reciprocity.  
• No reliance on opponent signals or trust—purely state‐based, short-term maximization with minimal concessions to resource sustainability.
'''

description_AGGRESSIVE_28 = '''
Below is an “aggressive‐exploitation with minimal regrowth” strategy.  It defects whenever it can safely harvest the common pool, but—when the stock is about to collapse—temporarily cooperates just enough to let the pool grow back to exploitable levels.  On the very last round it always defects to grab any remaining stock.

1.  Parameters  
   ­– n = number of players  
   ­– r = number of rounds  
   ­– capacity = maximum stock  
   ­– Define a low‐stock threshold T_low = capacity / n  
     •  Intuition: if the stock S_t ever falls at or below T_low, then even defecting yields very little, so it’s better to “top up” the pool by cooperating and harvest more later.  

2.  Decision rule (for round t with current observed stock S_t):  
   if t == r:  
     •  Action = D  (last round, always defect)  
   else if S_t ≤ T_low:  
     •  Action = C  (let the pool regrow when it’s nearly depleted)  
   else:  
     •  Action = D  (aggressively defect whenever the pool is still “thick”)  

3.  Edge cases  
   ­– First round (t=1): since S_1 = capacity ≥ T_low, you defect.  
   ­– Penultimate or any early round where S_t is exactly T_low: you cooperate once to allow a regrowth bump, then from the next round on you will defect again (unless the pool drops back to T_low or lower).  
   ­– If S_t ever reaches zero before the last round, then cooperating is your only action until S_t regrows above T_low (because defecting on S_t=0 yields zero payoff).  

4.  Why “aggressive”?  
   ­– You defect almost every round to maximize immediate payoff.  
   ­– You only “give back” a tiny fraction when the stock is so low that further defection would net you near zero anyway.  
   ­– You never carry out generous punishments or retreats—cooperation is purely mechanical, used only when necessary to stave off total resource collapse.  

5.  Pseudocode  

Let T_low = capacity / n  
For t = 1 to r:  
  observe current stock S_t  
  if t == r then  
    play D  
  else if S_t ≤ T_low then  
    play C  
  else  
    play D  

End  

This strategy will aggressively harvest the pool, only pausing to cooperate when the pool is about to be extinguished, and always defecting in the final round to secure any remaining payoff.
'''

description_AGGRESSIVE_29 = '''
Below is an “aggressive-but-sustainable” strategy.  It extracts as much as possible most of the time, punishes defectors, but—unlike “always defect”—throws in carefully timed cooperation only when it directly benefits your own future payoffs by reviving the resource.  

1.  State variables and parameters  
   • punish_counter ← 0  
   • K ← 2                   // Number of rounds to punish exploiters  
   • L ← capacity/2         // Lower‐threshold for cooperating to trigger regrowth  

2.  Overview of decision logic  
   Each round t (1 ≤ t ≤ r), observe:  
     – S_t : the current common‐pool stock  
     – last round’s history (who defected while you cooperated)  
   Then choose action A_t ∈ {C,D} as follows, in this priority order:  
   
   a.  If punish_counter > 0  
         A_t ← D  
         punish_counter ← punish_counter − 1  
         (We are in active punishment mode.)  
       else if t = 1  
         A_t ← D  
         (Kick off with defection to seize first‐round advantage.)  
       else if t = r  
         A_t ← D  
         (Always defect on the last round – no future to protect.)  
       else if S_t ≤ L  
         A_t ← C  
         (Stock is low; cooperate to allow maximum logistic regrowth.)  
       else  
         A_t ← D  
         (Otherwise, default to defection to maximize immediate gain.)  

3.  Punishment update (after observing opponent moves)  
   Immediately after round t, if in round t you played C and at least one opponent chose D, then  
       punish_counter ← K  
   This ensures any exploiter who takes advantage of your cooperation gets a short “grim” dampener.  

4.  Why this is aggressive  
   – You almost always defect (maximizing per‐round π_i = S_t/n) except when cooperation directly restocks the pool to your own long‐term benefit.  
   – You defect first round (seizing early surplus) and last round (no future to protect).  
   – You punish any player who defects against you during your cooperation window, deterring free‐riding.  

5.  Pseudocode  
```
Initialize:
  punish_counter ← 0
  K ← 2
  L ← capacity / 2

For t in 1..r:
  Observe current stock S_t

  // 1. Punishment override
  if punish_counter > 0:
    A_t ← D
    punish_counter ← punish_counter - 1

  // 2. First‐round grab
  else if t == 1:
    A_t ← D

  // 3. Last‐round grab
  else if t == r:
    A_t ← D

  // 4. Rescue the pool if it's low
  else if S_t ≤ L:
    A_t ← C

  // 5. Otherwise, maximize extraction
  else:
    A_t ← D

  // Submit action A_t simultaneously

  // After the round: observe opponents’ actions
  if (you played C at round t) and (any opponent played D at round t):
    punish_counter ← K
```

With this rule you exploit whenever you can, only “give back” when the stock threatens to collapse (and only to the level that maximizes its own regrowth), and you systematically punish any exploitation of your own goodwill.
'''

description_AGGRESSIVE_30 = '''
Below is a fully specified “Aggressive‐but‐Sustainable” strategy.  It is designed to grab as much as possible when it can, but to slip into brief “conservation” phases only if the stock is in danger of collapse, so that there will be something left to exploit later.  In every other respect it is ruthlessly defect‐oriented.

--------------------------------------------------------------------------------  
1.  Parameter calculation (once at the start):  
    • r = total rounds  
    • capacity = the maximum stock level  
    • Phase lengths:  
        k₁ = ⌊r/3⌋      (Length of initial “exploit” phase)  
        k₃ = ⌊r/3⌋      (Length of final “exploit” phase)  
        k₂ = r − k₁ − k₃  (Middle “watch‐and‐conserve” phase)  
    • Conservation threshold:  
        S_min = capacity/4  
      (If stock S_t ever dips below this, we switch to cooperating just long enough to allow regrowth.)  

2.  High‐level overview:  
    – Rounds 1…k₁: Always defect (D).  
    – Rounds k₁+1…k₁+k₂:  
        • If current stock S_t ≥ S_min, defect.  
        • Else (S_t < S_min), cooperate (C) until S_t ≥ S_min.  
    – Rounds r−k₃+1…r (the last k₃ rounds): Always defect (D).  

3.  Pseudocode  

    initialize k₁ ← ⌊r/3⌋  
    initialize k₃ ← ⌊r/3⌋  
    k₂ ← r − k₁ − k₃  
    S_min ← capacity / 4  

    for t = 1 to r:  
        observe current stock S_t  
        if t ≤ k₁:  
            action_t ← D  
        else if t > r − k₃:  
            action_t ← D  
        else:  
            # we are in the “middle” phase  
            if S_t < S_min:  
                action_t ← C    # brief conservation to allow regrowth  
            else:  
                action_t ← D    # exploit while stock is healthy  
        end if  
        play action_t and observe others, update S_{t+1}  
    end for  

4.  Rationale and edge‐case handling  
  • First Round (t=1): falls into “initial exploit” ⇒ D.  We strike immediately.  
  • Middle Phase: we continue to hammer the commons as long as stock ≥ S_min.  The moment it drops below S_min, we flip to C to give the pool a chance to bounce back (growth is 2·S′·(1−S′/capacity)).  As soon as it recovers above S_min we resume defecting.  
  • Last k₃ Rounds: we know forgiveness is pointless at the end—everyone will defect—so we defect unconditionally.  
  • If the stock ever reaches 0, all future payoffs are zero anyway; our brief conservation phases reduce the chance of that happening until the final exploitation wave.  

5.  Why “aggressive”?  
  – We defect in the majority of rounds (all of phase 1 + most of phase 2 + all of phase 3).  
  – We only cooperate when the resource is in danger of collapse, and only just long enough to allow a pulse of regrowth.  
  – We defect “for sure” in the final rounds, extracting every last bit without regard for the future (since there is none).  

This strategy will outperform “always‐cooperate” or simple “grim‐trigger” styles by front‐loading defections, briefly conceding only when the pool is critically low, then returning to aggressive harvesting.
'''

description_AGGRESSIVE_31 = '''
Here is a self-contained, aggressive “defect-first” strategy.  It defects in almost every round to grab the highest immediate payoff, but it grudgingly cooperates only when the pool is in danger of collapse and there are still enough remaining rounds to make future payoffs worth saving.  In the very last rounds it reverts to full defection unconditionally.

--------------------------------------------------------------------------------
STRATEGY: Aggressive Defector with Minimal “Stock-Saver”  
--------------------------------------------------------------------------------

Parameters you will fix once at the start (you can tune these if you wish):
  n            = number of players  
  r            = total rounds  
  capacity     = maximum sustainable stock  
  T_low_ratio  = small fraction of capacity at which we declare “emergency”  
                   (e.g. 1/(10·n) or even smaller)  
  final_defect = number of final rounds in which we never cooperate  
                   (e.g. final_defect = 2)  

Compute:  
  T_low = T_low_ratio × capacity  
  final_cutoff = r − final_defect + 1    // from this round onward, always defect  

State variables (initialized once):  
  emergency = false  

At the beginning of each round t you observe current stock S_t and the remaining rounds rem = r − t + 1.

Decision Rule for round t:

  1. If t ≥ final_cutoff:
       action ← D  
     (In the very last final_defect rounds, always defect to milk every last unit.)

  2. Else if emergency is true:
       action ← C  
       // We remain in “emergency” until the stock has bounced back above T_low
       if S_t > T_low:
         emergency ← false  

  3. Else  // t < final_cutoff and not already in emergency
     a. If S_t ≤ T_low  AND  rem > 1:
          // Pool is critically low and there is at least one future round to save
          emergency ← true
          action ← C  
     b. Otherwise:
          action ← D  

Notes on edge cases:
  • First round (t=1): S_1 = capacity ≫ T_low, so (3b) applies ⇒ defect.  
  • Last round (t=r): t ≥ final_cutoff ⇒ defect.  
  • If the pool ever collapses to S_t=0 before final_cutoff, then S_t≤T_low triggers emergency  
    ⇒ we cooperate (though payoff is zero) but that lets growth‐function remain zero.  
  • As soon as S_t climbs back above T_low in an emergency, we resume full defection.  

Rationale / Aggressive Mindset:
  – You defect whenever you can to maximize immediate π_i = S_t/n.  
  – You only cooperate when the pool is so small that, if everyone defects, it would collapse and  
    leave you with zero payoffs in all future rounds, and there is still at least one future round.  
  – You refuse to “waste” cooperation in the last final_defect rounds because there is nothing left  
    to protect.  
  – There is no attempt at reciprocity, forgiveness, or reward—this is pure exploitation with the  
    bare minimum of “rescue operations.”  

--------------------------------------------------------------------------------
Pseudocode
--------------------------------------------------------------------------------

  initialize:
    T_low = T_low_ratio * capacity
    final_cutoff = r - final_defect + 1
    emergency = false

  for t in 1…r:
    observe S_t
    rem = r - t + 1

    if t >= final_cutoff:
      action = D

    else if emergency:
      action = C
      if S_t > T_low:
        emergency = false

    else:  // not yet in emergency, not in final rounds
      if S_t <= T_low and rem > 1:
        emergency = true
        action = C
      else:
        action = D

    play action
    observe others’ actions and update S_{t+1} via the rule in the spec
  end for

--------------------------------------------------------------------------------

Tuning advice:
  • T_low_ratio controls how deep the pool must fall before you “bail it out.”  A smaller  
    ratio means you cooperate only in near-total collapse.  
  • final_defect can be 1 or 2 rounds—the fewer final rounds you spare for rescue, the more  
    aggressive your endgame.  

This strategy will consistently out-exploit cooperators early, refuse any altruism in the endgame,  
and only give up a tiny slice of your immediate gain when preserving future rounds is strictly  
better than letting the resource die.
'''

description_AGGRESSIVE_32 = '''
Below is an “aggressive pump-and-dump” strategy.  It almost always defects to grab as much as it can, but will grudgingly cooperate just enough—only when the pool is low and there is evidence others are willing to help it rebuild—so that there is something left to exploit later.  

1.  Definitions and parameters  
   •  capacity C.  
   •  Threshold T = C/2 (the “low‐stock” trigger at which we may briefly pump).  
   •  Last‐round window K_end = 1 (in the very last round we always defect).  

2.  High-level idea  
   a.  Round 1: defect to grab the juicy initial pool.  
   b.  Middle rounds (2 ≤ t ≤ r–K_end):  
      – If current stock S_t > T, defect.  
      – If S_t ≤ T *and* at least one opponent cooperated in the previous round, cooperate (pump) exactly once to trigger regrowth, then resume defecting.  
      – Otherwise defect.  
   c.  Last round (t = r): defect (end-game defection).  

3.  Why it’s “aggressive”  
   – Defects whenever the stock is healthy (> T) to maximize one-shot gains.  
   – Only cooperates when the stock has fallen below T and there is evidence (someone else cooperated last round) that a brief pump will pay off.  
   – Pumps only just enough to keep the pool alive for further exploitation; then immediately resumes defection.  
   – In the endgame, it never “wastes” cooperation.  

4.  Pseudocode  

   Inputs available at round t:  
     S_t           // current stock  
     history[t–1]  // list of all players’ actions in previous round  
     r             // total rounds  
   Output:  “C” or “D”  

   function AggressivePumpAndDump(t, S_t, history):  
     if t == 1:  
       return “D”                      // round 1: always defect  
     if t == r:  
       return “D”                      // final round: end-game defection  
     // middle rounds  
     if S_t > C/2:  
       return “D”                      // plenty of stock—exploit it  
     // stock is low: consider a one‐shot pump  
     // count cooperators in previous round  
     coopers = count(a in history[t–1] where a == “C”)  
     if coopers ≥ 1:  
       return “C”                      // at least one ally last round—pump now  
     else:  
       return “D”                      // no sign of cooperation—keep defecting  

5.  Edge-case handling  
   •  Round 2 sees “history[1]” defined, so we can check for cooperators; if none, we still defect.  
   •  If the pool ever hits S_t=0, further cooperation or defection yields zero, but our rule still returns “D.”  
   •  Because we only ever cooperate when S_t≤C/2 and someone else just cooperated, we avoid being the sucker in a pure all-C round.  
   •  The single “pump” condition is opportunistic—if opponents never cooperate, we never waste another C.  

6.  Expected behavior in a tournament  
   – Versus naïve cooperators: we exploit heavily until stock falls, then allow just enough joint pumping to fuel another round of exploitation.  
   – Versus unconditional defectors: we defect always—no worse off than any standard defector.  
   – Versus conditional cooperators (e.g. Grim-trigger, TFT): we exploit early, then they punish; once they begin to punish, they’ll cooperate sometimes to rebuild, which we again exploit.  

This strategy maximizes short-term grabs, ensures the pool never dies permanently if there is at least one other occasional cooperator to trigger regrowth, and never “wastes” cooperation at the end.
'''

description_COOPERATIVE_33 = '''
Below is a simple “grim‐trigger with endgame defection” strategy.  It begins by fully cooperating, punishes the first defection it ever sees by defecting forever after, and in the very last round it defects (because there is no future to sustain cooperation).  If every player in the tournament adopts this, you sustain full cooperation in rounds 1…r–1 and then defect in round r, which maximizes both efficiency and individual payoff given the one‐shot incentive in the last period.

----------------------------------------------------------------------------  
STRATEGY: Grim‐trigger with Planned Last‐round Defection  

State variables (per player i):  
  flagged_defect ← false    // have I ever seen a defection?  

Decision rule for each round t = 1…r:  
  1. If t = 1:  
       play C  
  2. Else if flagged_defect = true:  
       play D   // permanent punishment  
  3. Else if t = r:  
       play D   // endgame defection  
  4. Else (1 < t < r and no defection yet):  
       • If any opponent j played D in round t–1:  
            flagged_defect ← true  
            play D  
         Else:  
            play C  

Pseudocode  
----------
initialize flagged_defect ← false  
for t in 1…r do:  
  if t == 1 then  
    action_i(t) ← C  
  else if flagged_defect then  
    action_i(t) ← D  
  else if t == r then  
    action_i(t) ← D  
  else  
    if ∃ j ≠ i such that action_j(t–1) == D then  
      flagged_defect ← true  
      action_i(t) ← D  
    else  
      action_i(t) ← C  

Edge–case handling  
• First round (t=1): unconditional cooperation to signal willingness.  
• Any observed defection at any round t<r triggers “grim” punishment (defect forever thereafter).  
• Last round (t=r): defect regardless, since no future rounds remain to enforce cooperation.  

Why this is cooperative  
• If all players use it, everybody cooperates in rounds 1…r–1, yielding the highest sustainable payoff path (stock remains near capacity).  
• A one‐time defection by anyone immediately eliminates that player’s advantage (because all remaining rounds are defect rounds), so no one gains by deviating.  
• The threat of permanent punishment sustains cooperation in equilibrium for sufficiently long r.
'''

description_COOPERATIVE_34 = '''
Below is a concise, self‐contained description of a fully specified cooperative strategy—“One-Round Tit-for-Tat with End-Game Defection.”  It is designed to sustain high‐stock cooperation as long as no one deviates, to punish any defection just long enough to deter it, and to recognize the inevitable last‐round incentive to defect.

1.  Strategy name  
    “One-Round Tit-for-Tat with End-Game Defection”

2.  Intuition  
    – Start by cooperating to build up a track record.  
    – In each subsequent round (except the last), cooperate if everyone cooperated last period; if any player defected, defect exactly one round to punish, then return to cooperation.  
    – In the final round, defect (because there is no future to preserve).  

3.  Decision rules  
    Let r = total number of rounds.  Each round t = 1,2,…,r:  
      
    If t = 1:  
      play C.  
      
    Else if t = r:  
      play D.  (Last‐round defection.)  
      
    Else (1 < t < r):  
      • If in round t–1 every player chose C, then play C in round t.  
      • Otherwise (at least one defection in t–1), play D in round t.  

4.  Pseudocode  
    ```
    input: r, history = [A^1, A^2, …, A^(t–1)]  // A^k is the vector of all players’ actions in round k  
    function choose_action(t, history):
        if t == 1:
            return C
        if t == r:
            return D
        // 2 ≤ t ≤ r–1
        let last_profile = history[t–1]
        if all players in last_profile played C:
            return C
        else:
            return D
    ```

5.  Handling edge cases  
    – First round (t=1): no past history → cooperate to signal willingness.  
    – Middle rounds (2 ≤ t ≤ r–1): only condition on the immediately preceding round; punishes every defection with exactly one retaliatory D, then forgives.  
    – Last round (t=r): always defect, since future no longer matters.  

6.  Why it’s cooperative  
    – So long as all players cooperate, the stock is never over-harvested, and growth regenerates it, keeping S high.  
    – The single-round punishment (defect only in the round immediately after any defection) is mild and fast-forgiving—it restores cooperation quickly once the “bad actor” has been signaled.  
    – By always cooperating when the previous round was clean, it creates strong incentives for every player to stick with C, because a unilateral D immediately triggers a loss of one full‐period bonus (you lose the chance to harvest at rate 1/n instead of 1/(2n) in the next round).  
    – The unavoidable last‐round defection is isolated to t=r and does not poison earlier cooperation.  

This strategy requires no extra assumptions, uses only the publicly observable action history, and enforces cooperation in all but the final round.
'''

description_COOPERATIVE_35 = '''
Below is a single–strategy description called “Conditional Cooperation with One-Period Punishment (CCOPP) and Last-Round Securing.”  It is purely memory-based (no signals), starts by cooperating, punishes defections just enough to deter them, but in the very last round defects (since that maximizes last-round payoffs and cannot hurt future rounds).

1.  Internal State  
    •   punished ∈ {0,1}: flag saying “I owe a one-round punishment.”  
    •   history of opponents’ moves (you observe at the end of each round who played C or D).

2.  Parameters  
    •   r: total number of rounds (known in advance).  
    •   pun_length = 1 (we punish a defection with exactly one round of defection).  

3.  High-level Intuition  
    –  We begin cooperatively to build the stock.  
    –  If any opponent defected last round, we defect this round (to lower their future incentives) but only for one round, then return to cooperation.  
    –  In the final round (t = r) we defect, since there is no future to protect and one gains more payoff by playing D.

4.  Pseudocode  

  initialize punished ← 0

  for t in 1…r do
    if t == 1 then
      action ← C
    else if t == r then
      # last round: secure maximal payoff
      action ← D
    else if punished == 1 then
      # serve our one‐round punishment
      action ← D
      punished ← 0
    else
      # look at opponents’ moves in round t–1
      if ∃ j ≠ i such that opponent j played D in round t–1 then
        # trigger one‐round punishment
        action ← D
        punished ← 1
      else
        # no one defected last round → cooperate
        action ← C
      end if
    end if

    play(action)
    observe opponents’ moves this round (to use in t+1)
  end for

5.  Why this is Cooperative  
  •  It maintains full cooperation (everyone plays C) whenever no one has misbehaved.  That keeps the stock at or near capacity and maximizes the sum of all future payoffs.  
  •  It punishes a defection immediately and only briefly, just enough to deter unilateral defection but without launching an endless “grim” spiral.  
  •  Because the punishment is limited to one round, the group can quickly restore cooperation and continue reaping high joint payoffs.  
  •  By defecting in the last round, it also avoids being exploited at the end (since there is no future), and it increases that last‐round group payoff as well.  

6.  Edge‐Case Handling  
  –  First round (t = 1): cooperate unconditionally.  
  –  If two or more opponents defect simultaneously, you still punish only one round.  
  –  In the penultimate round, the same logic applies: if you owe punishment you defect; otherwise you look back one round.  And in the very last round you defect regardless.  

This strategy thus strikes a balance between (a) building and sustaining the common‐pool stock through mutual cooperation, and (b) guarding against exploitation via brief, targeted punishment, while (c) securing the inevitable one-shot defection payoff in the terminal round.
'''

description_COOPERATIVE_36 = '''
Below is a simple, fully specified “conditionally cooperative” strategy that (a) tries to sustain full cooperation, (b) punishes any defection just long enough to deter it, (c) forgives soon after, and (d) handles first‐ and last‐round edge cases.  You can tune the punishment length K (we suggest K = 1) or the forgiveness rule if you wish.

Strategy name: 1-Round Forgiving Trigger (1R-FT)

Parameters  
• n, r, capacity as given.  
• K = length of punishment in rounds after observing any defection (set K = 1).  

State variables (maintained by the strategy)  
• punish_timer ∈ {0,1,…,K}  
    – initialized punish_timer ← 0  

At the start of each round t = 1,2,…,r observe:  
  • Hₜ–1 = actions of all n players in round t–1  
  • Sₜ = current stock at beginning of round t  

Decision rule for round t:  
1.  If t = 1:  
      play C (no history yet).  
2.  Else if punish_timer > 0:  
      play D  
      punish_timer ← punish_timer – 1  
3.  Else if t = r:  
      play D   // final‐round defection  
4.  Else if in Hₜ–1 at least one player chose D:  
      // trigger punishment  
      punish_timer ← K  // start K‐round punishment  
      play D  
      punish_timer ← punish_timer – 1  
5.  Else:  
      play C  

After you choose your action, the round proceeds. Then the public Sₜ₊₁ is updated by the game’s stock‐dynamics, you observe all players’ moves in round t, and move on to t+1.

Explanation of the building blocks  
1.  Cooperation as long as no one defects (“nice”).  
2.  A defection anywhere in the group in round t–1 triggers K consecutive rounds of defection by you (punish).  
3.  After K rounds your punish_timer expires and you return to cooperation (forgiveness).  
4.  In the very last round (t=r) you defect, since there is no future to protect.  
5.  First round you cooperate to give cooperation a chance to establish.  

Why this is cooperative  
• Against all‐C opponents it stays all‐C every round, keeping S at capacity and giving everyone the maximal sustainable stream of payoffs.  
• Any unilateral defection is met with a brief but certain punishment, deterring free‐riding.  
• Punishment is finite (only K rounds), so the group can re‐coordinate on cooperation rather than spiral into permanent collapse.  
• No extra beliefs or signals are assumed—only direct reaction to observed moves.  

Tunable extensions  
• Increase K for harsher punishment, or set K=∞ for “grim” trigger.  
• Forgive only if the group has re-cooperated for L consecutive rounds (i.e. require L successive all-C before clearing punish_timer).  
• Include a stock‐threshold exception: if Sₜ falls below some S_min (e.g. capacity/2), suspend punishment and cooperate to help stock recover.  

Pseudocode summary  

  Initialize punish_timer ← 0  
  For t in 1..r:  
    observe Hₜ–1 (actions in previous round), Sₜ  
    if t = 1:  
      action ← C  
    else if punish_timer > 0:  
      action ← D  
      punish_timer ← punish_timer – 1  
    else if t = r:  
      action ← D  
    else if “any player chose D in Hₜ–1”:  
      punish_timer ← K  
      action ← D  
      punish_timer ← punish_timer – 1  
    else:  
      action ← C  
    submit action  
    // game updates Sₜ → Sₜ₊₁, you see all players’ choices, loop to next t.  

This strategy is well‐known to support (near) full cooperation in repeated settings while guarding against exploitation and allowing the group to return to cooperation quickly.
'''

description_COOPERATIVE_37 = '''
Below is a single “cooperative” strategy that (a) maximizes the chances the stock stays near capacity by sustaining mutual cooperation, (b) punishes any defection quickly, but (c) forgives after a short, fixed punishment so the group can return to cooperation.  It also takes account of first‐ and last‐round incentives.

Strategy name:  
  “Tit-for-Tat with One-Round Punishment and Endgame Defection”

Parameters you can tune:  
  • P = 1  (length of punishment phase)  
  • r  (total rounds, common knowledge)  

State variables (maintained by your agent):  
  • pun_count ∈ {0,1,…,P}  – how many more rounds to punish  
  • last_round_defected ∈ {true,false}  

Initialization (before round 1):  
  pun_count ← 0  
  last_round_defected ← false  

Decision rule in round t:  
  if t == 1 then  
    play C  
  else if t == r then  
    play D      ←  defection in the last round (standard endgame move)  
  else  
    if pun_count > 0 then  
      play D    ←  still in punishment phase  
    else  
      play C    ←  cooperate if not punishing  

After all actions in round t are observed, update punishment state:  
  let opponents_defected = (∃ j ≠ you : action_j == D)  
  if opponents_defected then  
    pun_count ← P        ←  start (or reset) punishment for next P rounds  
  else  
    pun_count ← max(0, pun_count − 1)  

Explanation of why this is cooperative:  
1. First‐move cooperation establishes goodwill.  
2. As long as nobody defects, you keep cooperating indefinitely.  
3. The moment any player defects, you defect for exactly P rounds, which punishes the deviator(s).  
4. After P rounds of punishment you automatically return to cooperation—even if the deviator never apologizes—so cooperation can resume.  
5. In the very last round you defect (standard backward‐induction endgame), capturing the slightly higher one‐shot payoff, but that has no effect on future rounds.  

Edge Cases:  
• First round: you unconditionally cooperate.  
• Last round (t = r): you unconditionally defect to pick up the higher S/n payoff—no future to incentivize.  
• Multiple simultaneous defectors: you still punish for P rounds (you defect P rounds regardless of how many defected).  
• After capacity is depleted or stock is low: since you only look at others’ actions, you continue to use the same rules—but because everyone cooperates in equilibrium, stock will hover near capacity.  

Pseudocode Summary  
```  
initialize pun_count = 0

for t in 1…r:
  if t == 1:
    action = C
  else if t == r:
    action = D
  else if pun_count > 0:
    action = D
  else:
    action = C

  play(action)

  observe all opponents’ actions this round
  if any opponent played D:
    pun_count = P
  else:
    pun_count = max(0, pun_count – 1)
```  

Tuning note: P = 1 is minimal punishment (“defect once”) then forgive.  If you fear widespread “random” defections you can raise P to 2 or 3, but larger P risks accumulating too many mutual defections and losing stock.  

This strategy’s hallmarks—start nice, retaliate just enough to deter, then forgive—make it robust in a heterogeneous tournament of LLM‐driven strategies.
'''

description_COOPERATIVE_38 = '''
Below is a single‐strategy prescription that (i) starts out fully cooperative, (ii) punishes observed defections just long enough to deter them, (iii) forgives and returns to cooperation, and (iv) handles first‐ and last‐round edge cases.  It never presumes secret coordination beyond observing past actions and the common stock.

— — —  
STRATEGY NAME  
“Sustainable Tit‐for‐Tat with Endgame Defection”

PARAMETERS  
  n = # players  
  r = # rounds  
  capacity = maximum stock  
  S_t = stock at start of round t  
  punish_length = 1  (punish for exactly 1 round per defection)  

STATE VARIABLES  
  last_round_defected?  Boolean: did any player defect in round t–1?   
  round_number  current round t  

DECISION RULE (for player i in round t):

1.  If t == 1:  
    – Action ← Cooperate (C).  
2.  Else if t == r:  
    – (Endgame) Action ← Defect (D).  
3.  Else if last_round_defected? == true:  
    – (Punishment phase) Action ← Defect (D).  
    – After playing round t, reset last_round_defected? ← false.  
4.  Else:  
    – (Action of “clean slate” cooperation) Action ← Cooperate (C).  

OBSERVING HISTORY AND UPDATING STATE:  
After everyone plays in round t, you observe all n actions.  
Set last_round_defected? ← true if any player’s action at t was D; otherwise ← false.  

— — —  
EXPLANATION OF WHY THIS IS COOPERATIVE  
1.  In every non‐endgame, non‐punishment round, all players consume only S_t/(2n), the cooperative harvest.  
2.  A single defection by any player in round t immediately triggers a one‐round punishment in t+1, restoring deterrence at minimal cost to the resource.  
3.  After punishment, the group returns to full cooperation—so sustained cooperation yields the maximum long‐run stock and payoff.  
4.  The only inevitable defection in the last round is the classical endgame move; but by then no future rounds remain so no greater damage is done.  

— — —  
PSEUDOCODE

Initialize:  
 last_round_defected? ← false  
For t in 1..r do:  
 if t == 1:  
  action_i[t] ← C  
 else if t == r:  
  action_i[t] ← D  
 else if last_round_defected? == true:  
  action_i[t] ← D  
  # punish for exactly one round  
 else:  
  action_i[t] ← C  

 # After actions are played, observe history:  
 if ∃j such that action_j[t] == D then  
  last_round_defected? ← true  
 else  
  last_round_defected? ← false  

EndFor

— — —  
NOTES  
• Punish_length = 1 is tunable; you may punish for k>1 rounds to increase deterrence if you expect very aggressive defectors.  
• No reliance on hidden signals or outside coordination—only observed history.  
• This strategy keeps the stock as high as possible under mutual cooperation and only defects just enough to enforce it.
'''

description_COOPERATIVE_39 = '''
Below is a fully specified cooperative strategy, call it “Single‐Period Punisher” (SPP).  It is designed to sustain high cooperation by (1) starting cooperatively, (2) punishing any defection with exactly one round of defection, then forgiving, and (3) correctly handling the first and last rounds.

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
1. Informal description  
––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
• Round 1: Cooperate.  
• In any later round, if someone defected in the immediately preceding round and you are not already punishing, switch to Defect for exactly one round (the punishment round), then go back to Cooperate.  
• If nobody defected in the last round and you are not in punishment mode, Cooperate.  
• In the last round (t = r), the same rule applies: if you must punish (because of t–1’s defection), defect; otherwise cooperate.  
• Because punishment is only one round long, the strategy is forgiving and avoids endless mutual defection.  

This yields the following properties:  
– If all players follow SPP and nobody deviates, the play path is C,C,…,C and the stock is replenished each period at its maximum.  
– A single defection is met with exactly one period of defection by all punishers (at least you), which lowers the deviator’s payoff and reduces the pool for one round; then cooperation resumes.  
– No endless “grim” punishment, so accidental or one‐off defections do not destroy cooperation forever.  
– No coordination or extra assumptions beyond observing past actions.  

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
2. Pseudocode  
––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
Inputs (common knowledge):  
    n, r, capacity  
Local state per player i:  
    punish_counter ← 0  
For t from 1 to r do:  
    if t == 1 then  
        action_i ← C  
    else  
        if punish_counter > 0 then  
          action_i ← D  
          punish_counter ← punish_counter – 1  
        else  
          // look at last round’s actions of all players j  
          if ∃ j such that action_j(t–1) == D then  
            // trigger one‐round punishment  
            action_i ← D  
            punish_counter ← 1  
          else  
            action_i ← C  
          end if  
        end if  
    end if  

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
3. Edge‐case handling  
––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
• First round (t=1): no history ⇒ Cooperate.  
• Punishment is always exactly one round, so there is no infinite trigger.  
• Last round (t=r): we follow the same logic.  If someone defected in round r–1, we punish in round r; otherwise we cooperate.  After t=r there are no more rounds, so no further considerations.  

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
4. Why this is cooperative  
––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
• It maximizes the common‐pool stock by keeping all players cooperating most of the time, letting it regrow each round.  
• It deters unilateral defection: a defector loses one future‐round payoff (when punish_counter=1) and reduces group stock, so on net they do worse than if they had cooperated.  
• It forgives one‐time mistakes or “slips,” so cooperation can recover quickly.  
• It does not rely on impossible commitments in the last round (it punishes in the last round if needed, but never continues punishing beyond the game).
'''

description_COOPERATIVE_40 = '''
Below is a single‐strategy prescription—call it “Tit-for-Titans”—that (i) starts by cooperating, (ii) punishes any defection just enough to deter free-riding, (iii) forgives, and (iv) defects in the very last round to avoid being exploited in the endgame.  

1.  Variables we keep track of  
    •  punish_timer (integer ≥0): number of remaining rounds we will defect purely to punish.  
    •  last_actions: the vector of all players’ actions in the previous round.  

2.  Initialization (before round 1)  
    punish_timer ← 0  
    last_actions ← “none”  

3.  Decision rule at the beginning of each round t (1 ≤ t ≤ r):  
    if t == 1 then  
       play C  
    else if t == r then  
       # last round—no future to protect  
       play D  
    else if punish_timer > 0 then  
       # we are in punishment mode  
       play D  
       punish_timer ← punish_timer – 1  
    else  
       # we are in cooperative mode  
       if exists i ≠ us such that last_actions[i] == D then  
          # someone defected last round → punish once  
          punish_timer ← 1  
          play D  
       else  
          # no one defected last round → keep cooperating  
          play C  
       end if  
    end if  

4.  After all moves are revealed in round t, update  
    last_actions ← the vector of actions chosen by all n players in round t  

5.  Notes on the design  
  •  First round (t=1): we unconditionally cooperate.  
  •  “Punish once” means as soon as we detect any defection, we defect in the very next round, then return immediately to cooperation.  
  •  We never allow punish_timer to build up beyond 1, so we are forgiving: one defection → one round punishment → back to C.  
  •  Last round (t=r): we unconditionally defect to collect the maximum payoff when there is no future.  
  •  By cooperating whenever nobody defected last time, we sustain the common stock at a high level. The single-round punishments deter unilateral defection.  

6.  Pseudocode  

    function choose_action(t, r, last_actions, punish_timer):  
        if t == 1 then  
            return “C”, punish_timer  # start cooperatively  
        end if  

        if t == r then  
            # last round: no future value in cooperation  
            return “D”, punish_timer  
        end if  

        if punish_timer > 0 then  
            # we are serving our punishment  
            punish_timer ← punish_timer – 1  
            return “D”, punish_timer  
        end if  

        # cooperative mode: check last round  
        if exists action in last_actions where action == “D” then  
            # somebody defected → punish next round  
            punish_timer ← 1  
            return “D”, punish_timer  
        else  
            # all cooperated last round → cooperate again  
            return “C”, punish_timer  
        end if  
    end function  

7.  Why this is cooperative  
  –  We always attempt to restore full cooperation after exactly one round of punishment.  
  –  We never spiral into long vendettas; that keeps the stock high over time.  
  –  Because we defect in the final round only, we eliminate the risk that opponents can extract high payoffs in rounds r or r–1 without fear of retaliation.  

This simple “Tit-for-Titans” strategy has three hallmarks of a cooperative repeated-play strategy:  
  1. It starts by cooperating to build trust.  
  2. It punishes defection—but only briefly—so that there is always an incentive to return to cooperation.  
  3. It defects in the final round to avoid last-move exploitation.
'''

description_COOPERATIVE_41 = '''
Below is a simple “tit-for-tat” style strategy adapted to the n-player common‐pool game.  It is maximally cooperative (keeps the stock at capacity if everyone follows it), punishes defections, then immediately forgives, and defects in the very last round (when no future remains).  

1.  Intuition  
   •  If everyone in round t − 1 cooperated, continue cooperating in t ⇒ stock stays at capacity and each gets capacity/(2n).  
   •  If anyone defected in t − 1, punish by defecting once in round t (all punishers drive stock down, so defectors lose future value).  Immediately afterwards, return to cooperation.  
   •  First round: cooperate.  Last round: defect (no future to protect).  

2.  Pseudocode  

```
Inputs:  
  n        // number of players  
  r        // total rounds  
  history  // list of action‐profiles for past rounds; history[t] ∈ {C,D}^n  

State variables:  
  punish_next = false  

For each round t = 1,…,r do:
  if t == 1:
    action = C                      // start by cooperating
  else if t == r:
    action = D                      // final‐round defection
  else if punish_next:
    action = D                      // carry out 1‐round punishment
    punish_next = false
  else
    // look at last round’s profile
    let last_profile = history[t−1]
    if any player in last_profile played D:
      action = D                    // punish
      punish_next = true            // but forgive right after
    else
      action = C                    // everyone cooperated last time

  submit action
End for
```

3.  Explanation of key points  
– First round: we have no information, so we cooperate.  
– Normal rounds (2 ≤ t < r):  
   • If we are in a “pending punishment,” we defect once (punish_next==true) then clear the flag.  
   • Otherwise, we inspect the previous profile.  If we saw any D, we set punish_next and defect now.  If we saw only C’s, we continue cooperating.  
– Last round (t==r): we defect, because there is no future incentive to protect.  

4.  Properties  
– If all play this strategy, stock always returns to capacity, and each round every player gets capacity/(2n).  
– A single defection by any player in round t triggers a 1‐round collective punishment in t+1, inflicting a larger loss on the defector (and on everyone) than the one‐round gain.  After that one round, we forgive and return to cooperation.  
– Simple, forgiving, robust to mistakes.
'''

description_COOPERATIVE_42 = '''
Below is a “nice,” history‐dependent strategy that (a) sustains cooperation whenever possible, (b) punishes one round for any detected defection, then immediately forgives, and (c) avoids the inevitable end‐game unraveling by defecting in the last round.

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
Strategy name: Tit‐for‐Tat with Last‐Round Defection (TFT‐LRD)

Overview  
1. Round 1: Cooperate.  
2. Rounds 2 through r−1:  
   • If in the immediately preceding round every other player cooperated, then cooperate;  
   • Otherwise defect (punish exactly one round).  
3. Round r (final round): Defect.

Rationale  
• By starting with cooperation and only punishing one round, we give opponents every incentive to return to cooperation immediately.  
• Defecting in the final round is unavoidable under backward‐induction: no future gains from preserving the stock once the game ends.  

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
Detailed decision rules  

Let t = current round (1 ≤ t ≤ r). Let a_{j,t} ∈ {C,D} be player j’s action in round t. You are player i.

1. If t = 1:  
   action_i = C  

2. Else if t = r (final round):  
   action_i = D  

3. Else (2 ≤ t ≤ r−1):  
   • If ∀ j ≠ i: a_{j,t−1} = C  
       → action_i = C  
   • Else  
       → action_i = D  

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
Pseudocode  

```
for t in 1…r:
    if t == 1:
        action_i[t] = C
    else if t == r:
        action_i[t] = D
    else:
        # look at last round
        if every other player cooperated in round t-1:
            action_i[t] = C
        else:
            action_i[t] = D
```

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
Edge‐case handling  
• First round (t=1): we have no history, so we cooperate unconditionally.  
• Single defection by any opponent in round t−1 → we punish exactly in t, then resume cooperation in t+1 if they’ve returned to C.  
• Final round (t=r): defection is dominant (no future payoff to protect).  

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
Cooperative mindset  
• You never preemptively defect except where backward induction forces it (final round).  
• You only punish minimally (one round), so opponents have every reason to cooperate again immediately.  
• By sustaining stock through widespread cooperation, you maximize the long‐run common pool and thus everyone’s total payoff.
'''

description_COOPERATIVE_43 = '''
Below is a simple “trigger‐style” cooperative strategy that (i) sustains the resource by cooperating whenever possible, (ii) punishes one defection by defecting exactly once, then forgives, and (iii) defects in the last round (since there is no future to protect).

Name:  One‐Period Punishment Tit-for-Tat (OPP-TFT)

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
Notation  
––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
n        number of players  
r        total rounds  
t        current round (1 ≤ t ≤ r)  
Aₜⁱ      action of player i in round t (“C” or “D”)  
Sₜ       stock at start of round t  
Hₜ₋₁     history of all actions up through round t-1  
lastDef  the last round in which any player defected (initially 0)  

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
High‐Level Description  
––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
1. Round 1: Cooperate.  
2. Rounds 2…r–1:  
   – If round t–1 saw at least one defection by any player, record lastDef = t–1 and defect in t.  
   – Else if you are in the “punishment window”—i.e. t = lastDef + 1—defect.  
   – Otherwise cooperate.  
3. Round r: Defect (no future to protect).  
4. Special case: If Sₜ = 0 (pool empty), you may as well play C (no gain from D).  

This strategy rewards full cooperation with continued C, punishes any defection exactly once, then returns to cooperation. Defecting in the final round is standard backward‐induction play.

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
Pseudocode  
––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
initialize lastDef ← 0

for t in 1…r do  
  if Sₜ = 0 then  
    Aₜ ← C  
    continue  
  end if

  if t = 1 then  
    Aₜ ← C  
    continue  
  end if

  if t = r then  
    Aₜ ← D  
    continue  
  end if

  // t in 2…r–1
  // 1) Was there a defection in the previous round?
  if ∃ j such that Aₜ₋₁ʲ = D then  
    lastDef ← t – 1  
    Aₜ ← D  
    continue  
  end if

  // 2) Are we in the one‐period punishment window?
  if t = lastDef + 1 then  
    Aₜ ← D  
    continue  
  end if

  // 3) Otherwise, cooperate
  Aₜ ← C
end for

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
Rationale  
––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
• By starting with C and cooperating whenever no one has just defected, OPP-TFT keeps the stock near capacity.  
• A single‐round punishment (one D) is enough to deter selfish deviations in most standard repeated‐game settings, yet it immediately forgives to restore long‐run cooperation.  
• Defecting in the very last round maximizes one’s final payoff (no future rounds remain).  
• If the pool ever hits zero, no action yields any immediate payoff, so we default to C for consistency.

This strategy is simple, completely memory‐one (plus a single “lastDef” flag), and aligns with a cooperative mindset while preserving incentives against unilateral defection.
'''

description_COOPERATIVE_44 = '''
Below is a simple “tit-for-tat with one‐round punishment” strategy, augmented by an “emergency cooperation” rule when the stock is very low.  It is intended to stabilize full cooperation (everybody plays C) for most of the game, to punish one‐off defections, to forgive quickly, and to avoid driving the stock to collapse.  No side-agreements or extra signals are needed—every decision depends only on the public history of actions, the current round t, and the current stock S.

Notation and parameters  
• n, r, capacity as given.  
• S_t = common‐pool stock at the start of round t.  
• history[t′] = vector of all n actions in round t′ (each action ∈ {C,D}).  
• k = 1  (punishment length in rounds).  
• ε = 0.25·capacity  (low‐stock threshold; tuneable).

Internal state  
• punish_timer (integer, initially 0).

Strategy outline  
For each round t = 1 … r do:

1.  Observe S_t, history up to t–1, and punish_timer.

2.  If t = 1  
      Action ← C  
      (Always start by cooperating.)

3.  Else if t = r  
      Action ← D  
      (Play defect in the last round—no future to punish.)

4.  Else if S_t < ε  
      Action ← C  
      (“Emergency cooperation” if stock is very low.  We temporarily suspend punishment to help regrow.)

5.  Else if punish_timer > 0  
      Action ← D  
      punish_timer ← punish_timer – 1  
      (Continue punishing for up to k rounds.)

6.  Else if any player played D in history[t–1]  
      Action ← D  
      punish_timer ← k – 1  
      (Detect a defection last round, punish now for k rounds in total.)

7.  Else  
      Action ← C  
      (Cooperate whenever no active punishment and no recent defection.)

8.  Execute Action; observe everyone’s moves; the game computes payoffs and S_{t+1}.

Why this works cooperatively  
– Mutual cooperation (everybody plays C from t=1 to t=r–1) keeps the stock at capacity and yields the maximum sustainable flow each round.  
– If someone defects, we immediately punish (all D) for exactly one round—this lowers the defector’s average payoff enough to deter one‐off deviations, yet forgives quickly so we can return to full cooperation.  
– We never let punishment continue beyond the point it’s credible (k=1) and we never defect when the pool is nearly depleted (S<ε), so we do not drive the stock to ruin.  
– In the very last round we defect (D) because, with no future rounds left, defection strictly dominates cooperation that round.

Pseudocode  

```
initialize punish_timer ← 0

for t in 1…r:
  observe S_t, history[1…t–1]

  if t == 1:
    Action = C

  else if t == r:
    Action = D

  else if S_t < ε:
    Action = C

  else if punish_timer > 0:
    Action = D
    punish_timer ← punish_timer – 1

  else if (∃ player i with history[t–1][i] == D):
    Action = D
    punish_timer ← k – 1

  else:
    Action = C

  play Action
  # after play, observe all actions to build history[t]
  # stock dynamics happen externally
```

Parameter notes  
– k=1 is the classic tit-for-tat punishment length; you can experiment with k=2 or 3 but longer punishments risk harming the stock more than the cheater.  
– ε controls how low the pool must fall before we suspend punishment; a typical choice is 25% of capacity but you can adjust based on the growth rate.  

This strategy is fully cooperative—by default it sustains the high‐yield cooperative outcome—and it punishes defections just enough to deter them, while always forgiving quickly to restore the cooperative equilibrium.
'''

description_COOPERATIVE_45 = '''
Below is a single‐strategy specification—call it “Tit-for-Tat with End-Game Defection and Minimal‐Stock Safety”—that (i) starts out cooperative, (ii) punishes any defection by any opponent for one round only, (iii) always defects in the very last round, and (iv) never punishes if the stock has already fallen below a small safety threshold (to avoid accidental collapse).

1.  Definitions and parameters  
    •  n, r, capacity as in the spec.  
    •  S_t: common‐pool stock at the start of round t.  
    •  SafetyThreshold ε > 0: a small positive number (e.g. ε = capacity*0.01), below which we refrain from punishing to avoid driving S to zero.  
    •  punishRemaining: integer counter (initially 0). When >0, we are in punishment mode.  

2.  High-level description  
    •  Round 1: Cooperate.  
    •  In any round t<r:  
       –  If S_t ≤ ε, Cooperate (to preserve what’s left).  
       –  Else if punishRemaining > 0, Defect and decrement punishRemaining by 1.  
       –  Else if any player defected in round t–1, set punishRemaining←1 then Defect.  (One‐round “tit-for-tat” punishment.)  
       –  Else Cooperate.  
    •  Round r: Defect (last‐round defection is dominant).  

3.  Pseudocode  

  initialize punishRemaining ← 0  
  choose ε ← capacity*0.01   // or any small fraction of capacity  

  for t in 1…r:  
    observe S_t  // current stock  
    observe A_{1…n}^{t–1} if t>1  // actions of all players last round  

    if t == r:  
      action_t ← D  
    else if t == 1:  
      action_t ← C  
    else if S_t ≤ ε:  
      // stock is nearly exhausted—better to cooperate than risk collapse  
      action_t ← C  
    else if punishRemaining > 0:  
      // we are in the middle of punishing  
      action_t ← D  
      punishRemaining ← punishRemaining – 1  
    else if ∃ j≠i such that A_j^{t–1} == D:  
      // someone defected last round—punish for one round  
      punishRemaining ← 1  
      action_t ← D  
    else:  
      action_t ← C  

    play action_t  
    // observe payoffs and next S_{t+1} per game dynamics  

4.  Why it’s “cooperative”  
    •  It never preemptively defects—it only defects in direct response to observed defection (plus the forced last‐round defection).  
    •  Punishment is minimal (one round) and then the strategy immediately returns to cooperation if opponents resume cooperating.  
    •  It includes a safety‐threshold rule: if the pool is nearly exhausted, it stops punishing so as not to drive the stock to zero.  
    •  By sustaining cooperation in all but the last round (and only punishing actual defectors), it maximizes the joint stock over time.  

5.  Edge‐case handling  
    •  First round: Cooperate unconditionally.  
    •  Last round: Defect (cannot be deterred once no future).  
    •  Extremely low stock (S_t ≤ ε): Cooperate even if in punishment mode.  
    •  Multiple defectors: any single defection triggers exactly one round of punishment—no escalation.  

This strategy fares well in a tournament of independent players who (like you) seek to maintain the resource. It creates a clear incentive to cooperate consistently (otherwise you’ll be immediately punished for exactly one round), but it never carries grudges long enough to threaten permanent collapse.
'''

description_COOPERATIVE_46 = '''
Below is a simple “trigger‐and‐forgive” strategy that seeks to sustain full cooperation (everyone plays C) as long as no one defects, but delivers a short punishment if a defection occurs, and handles the first and last rounds explicitly.

Strategy name: Forgiving Tit-for-Tat with Endgame Defection  

Parameters you can tune:  
• PunishLength P (we suggest P=1)—number of rounds you defect after seeing a defection.  

Notation:  
• t ∈ {1,…,r} is the current round.  
• history Ht = list of all players’ actions in rounds 1…t-1.  
• lastDefectRound = the most recent round s< t in which someone played D (or 0 if none yet).  
• roundsSinceDefect = t – lastDefectRound – 1.  

1.  Decision rule for round t:  
   if t = 1:  
      play C  (start by cooperating)  
   else if t = r:  
      play D  (no future to protect—defect to grab the last available stock)  
   else if (roundsSinceDefect ≤ P) then  
      play D   (punishment: you saw a defection in the last P rounds)  
   else  
      play C   (otherwise, restore cooperation)  

2.  Updating your record of defections:  
   – After each round you observe everyone’s moves; if any player played D in round t, set lastDefectRound = t.  

3.  How it works:  
   – Round 1: you cooperate.  
   – As long as no one defects, you continue cooperating every round 2…r-1, keeping the stock high.  
   – If anyone defects in round s, you defect in round s+1 (that’s your P=1 punishment) and then—provided no new defections—return to C in s+2.  
   – In the very last round t=r you defect, since there is no future penalty.  

Pseudocode  

```
initialize lastDefectRound ← 0
for t in 1…r do
    if t == 1 then
        action[t] ← C
    else if t == r then
        action[t] ← D
    else
        roundsSince ← t - lastDefectRound - 1
        if roundsSince ≤ P then
            action[t] ← D    # punish for up to P rounds
        else
            action[t] ← C    # resume cooperation
        end
    end

    # observe all players’ actions in round t
    if any opponent played D in round t then
        lastDefectRound ← t
    end
end
```

Discussion of edge‐cases:  
• First round (t=1): you have no history → cooperate.  
• Rounds 2…r−1: apply the one‐round punishment rule: the moment you see any D, you defect next round but then forgive and return to C if nobody defects again.  
• Last round (t=r): defect, since there is no future in which to deter you.  

Cooperative mindset:  
– All‐C is a self‐enforcing path: if everyone follows this rule, the stock stays at capacity and each player repeatedly earns S/(2n).  
– A brief, one‐round punish‐and‐forgive keeps incentives aligned without destroying the resource or spiral‐out.  
– By forgiving (rather than permanent grim trigger), you allow the group to recover from isolated mistakes or noise and sustain cooperation over r−1 rounds.
'''

description_COOPERATIVE_47 = '''
Below is a single‐strategy proposal we’ll call “One-Step TFT with End-Game Defection.”  It aims to sustain the common pool near capacity by mutual cooperation, to punish one short defection, then forgive, and to avoid the backward-induction collapse by defecting only in the very last round.  

1. Intuition  
  – Start by cooperating to leave half the stock.  Mutual cooperation regenerates the pool back toward capacity.  
  – If any co-player defects against you in round t–1, you defect exactly once in round t to punish.  Then immediately resume cooperation.  
  – In the final round you defect, because there is no future to protect.  

2. State variables  
  – punish_flag (Boolean), initially false.  

3. Decision rules (at round t with observed history of actions in round t–1 and current stock S_t):  
   if t == 1:  
     play C  (kick off with cooperation)  
   else if t == r:  
     play D  (last round defection)  
   else if S_t == 0:  
     play D  (nothing left to grow; defect for any residual payoff)  
   else if punish_flag == true:  
     punish_flag ← false  
     play C  (forgive—end punishment)  
   else if (in round t–1 at least one other player played D):  
     punish_flag ← true  
     play D  (punish defector(s) exactly one round)  
   else:  
     play C  (cooperate by default)  

4. Pseudocode  

  initialize punish_flag ← false  
  for t in 1..r do  
    observe S_t  and actions_{t–1} if t>1  
    if t == 1 then  
      action_i ← C  
    else if t == r then  
      action_i ← D  
    else if S_t == 0 then  
      action_i ← D  
    else if punish_flag then  
      punish_flag ← false  
      action_i ← C  
    else if exists j ≠ i such that action_j,t–1 == D then  
      punish_flag ← true  
      action_i ← D  
    else  
      action_i ← C  
    end if  
    submit action_i  
    observe all actions this round, compute S_{t+1}  
  end for  

5. Why this is cooperative  
  – Mutual cooperation is the default; it regenerates the resource and yields the highest joint surplus.  
  – Punishment is minimal and tit-for-tat style: defect exactly once in response to any defection, then immediately forgive.  This contains short-term incentives to defect without driving the pool to collapse.  
  – By defecting only in the very last round and in one‐round punishments, the strategy avoids triggering permanent collapse via long punishments.  

6. Edge cases  
  – First round: unambiguously cooperate to establish trust.  
  – Last round: defect (no future) to secure any remaining one‐off gain.  
  – Zero stock: defect (cooperation yields zero payoff anyway).  
  – Multiple simultaneous defections: still punished with only a single-round defection.  

This strategy is simple, fully specified, enforces cooperative growth of the pool, yet punishes free‐riding and recognizes end‐game incentives.
'''

description_COOPERATIVE_48 = '''
Below is a single‐agent strategy (“Conditional Cooperator with Regrowth Concern and Forgiving Punishment”) that aims to sustain high common‐pool stock via mutual cooperation, yet punishes one‐off defections briefly, and helps the stock recover when it is low.  It is designed for the simultaneous‐move, repeated CPR game you described.  

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
STRATEGY OVERVIEW  
1. Start by cooperating.  
2. Cooperate as long as  
   • No one defected in the immediately preceding round,  
   • The stock is not dangerously low, and  
   • It is not the final round.  
3. If any opponent defected last round → defect for exactly one round (punishment), then return to cooperation.  
4. If the stock ever falls below a low‐stock threshold → cooperate (to aid regrowth).  
5. In the final round → defect (no future to protect).  

This “generous tit‐for‐tat” with one‐round punishment and a safe‐stock bail‐out rule aligns everyone toward maximum long‐run payoffs by sustaining the resource.  

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
KEY PARAMETERS (common‐knowledge)  
n              : number of players  
r              : total rounds  
capacity       : maximum stock  
low_frac = 0.25: fraction of capacity below which we always cooperate  
punish_len = 1 : punishment duration (rounds)  

STATE VARIABLES (per agent)  
punishing     : Boolean flag (are we in punishment mode?)  
punish_timer  : integer (rounds of punishment remaining)  

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
PSEUDOCODE  

Initialize (before Round 1):  
  punishing    ← false  
  punish_timer ← 0  

For each round t = 1…r do:  
  Observe:  
    S_t         ← current stock at start of Round t  
    LastActions ← vector of all players’ actions in round t–1 (undefined if t=1)  
  
  Decision rule:  
    if t = 1 then  
      Action ← C    # start cooperatively  
    else if S_t ≤ low_frac * capacity then  
      Action ← C    # stock is low → help regrow  
      # reset any ongoing punishment? No: a defection still warrants its short punishment  
      if punishing and punish_timer > 0 then  
        # carry on with scheduled punishment if still due  
        # (we cooperate here only if no punishment is pending)  
        Action ← D  
      end  
    else if punishing then  
      Action ← D  
      punish_timer ← punish_timer – 1  
      if punish_timer = 0 then punishing ← false end  
    else if any player in LastActions played D then  
      # trigger one‐round punishment  
      punishing    ← true  
      punish_timer ← punish_len  
      Action ← D  
    else if t = r then  
      Action ← D    # last round: defect for immediate gain  
    else  
      Action ← C    # normal cooperative mode  
    end if  

  Play Action  

End for  

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
EXPLANATION OF DESIGN CHOICES  
• Cooperate by default (“nice”): maximizes group payoff and keeps stock high.  
• One‐round punishment (“forgiving” tit‐for‐tat): discourages defection but restores cooperation quickly to avoid resource collapse.  
• Low‐stock bail‐out: if S_t drops below ¼ capacity, always cooperate to help the pool regrow (even if punishing is due, we still carry out up to one round of punishment but never initiate new punishments while low).  
• Defect in final round: standard last‐move logic (future irrelevance).  

This strategy will, in a population of similar or responsive strategies, keep the stock near capacity each round, earning each player roughly S/(2n) per round, while inflicting short, finite punishment on any one‐off defectors.
'''

description_COOPERATIVE_49 = '''
Below is a cooperative “forgiving‐Tit-for-Tat” strategy tailored to sustain high common‐pool stock, punish one‐shot defections, forgive quickly, and avoid being a sucker in the very last round.  

1. Overview of the Idea  
   • We begin by cooperating (low extraction).  
   • As long as nobody defected in the immediately preceding round, we keep cooperating.  
   • If we observe any defection in the last round, we defect exactly once (punishment), then return to cooperation.  
   • In the final round, we defect (higher payoff, no future to harm).  

2. Why it is Cooperative  
   • When all players use it, everyone extracts only S/(2n) each round (stock remains at capacity).  
   • A single defector is punished only one round, then forgiven—avoiding endless cycles of retaliation.  
   • By defecting last round, we avoid being exploited while all earlier rounds preserve the resource.  

3. Decision Rules in Detail  

   Let t ∈ {1,…,r} be the current round, and H be the history of action profiles up to round t–1.  

   Define  
     lastDefected = (true if in round t–1 at least one player chose D, else false)  
     punishing    = (true if lastDefected==true and we have not yet carried out our one‐round punishment)  

   Action for round t:  
     if t == 1:  
       play C  // start cooperatively  
     else if t == r:  
       play D  // final‐round defection guard  
     else if lastDefected and not yet punished for that defection:  
       play D  // one‐round punishment  
     else:  
       play C  // otherwise cooperate  

   After choosing your action you update:  
     if lastDefected and you just played D to punish, mark that you have punished this defection so you won’t punish again.  
     if no defection in round t–1, reset your “punished” flag so you are ready to punish a future defection once.  

4. Pseudocode  

   initialize punishedFlag = false  

   for t in 1…r:  
     observe history H up to round t–1  
     if t == 1:  
       action[t] = C  
       punishedFlag = false  
     else if t == r:  
       action[t] = D  
     else:  
       // detect if any defection in last round  
       lastDefected = (∃ j : H[t–1][j] == D)  
       if lastDefected and not punishedFlag:  
         action[t] = D  
         punishedFlag = true     // we have now issued our one‐round punishment  
       else:  
         action[t] = C  
         if not lastDefected:  
           punishedFlag = false  // forgive/reset so we can punish fresh defections later  

   return action[t]  

5. Handling Edge Cases  
   • First round (t=1): no history → cooperate to signal trust.  
   • Last round (t=r): defect to secure maximal payoff (no future cost).  
   • Single defection → exactly one‐round punishment, not permanent Grim Trigger.  
   • Consecutive defections by others → we punish only once per defection wave; if they defect again after we forgave, we punish again.  

6. Expected Dynamics  
   • All‐C path: stock stays at capacity, each round payout = capacity/(2n).  
   • If someone defects once, they get higher immediate payoff but face one round of mutual D (stock dips more), then cooperation resumes.  
   • In a tournament of independent strategies, this approach strikes a balance between being robust to exploitation, responsive to free‐riders, and maintaining cooperation over almost all of the game.
'''

description_COOPERATIVE_50 = '''
Below is a single‐strategy “recipe” for sustaining near‐full cooperation on the common pool resource.  It is a straightforward Tit‐for‐Tat‐with‐Limited‐Punishment (TFT‐LP) scheme, which (1) starts by cooperating, (2) punishes any defection by defecting for a fixed number of rounds, then (3) returns to cooperation, and (4) always cooperates in the first and last rounds.  This simple structure is easy to describe, easy to infer from opponents’ play, and yields high average payoffs as long as at least one other player is amenable to cooperation.

————————————————————————  
1. Parameters you choose (constants built into your strategy)  
   • Punishment length P (integer ≥1).  How many consecutive rounds of defection you use to punish a defection.  
     – P=1 is pure TFT; P>1 is sterner.  A small P (e.g. 2–3) often suffices.  

————————————————————————  
2. State variables your strategy tracks  
   • last_round_any_D (bool) – did anyone defect in the immediately previous round?  
   • punish_counter (integer ≥0) – how many more rounds you will defect as punishment.  

————————————————————————  
3. Decision rule (pseudocode)  

Initialize:  
 last_round_any_D ← false  
 punish_counter ← 0  

For each round t = 1 … r do:  
 Observe current stock S_t (not actually needed in this rule)  
 If t = 1 or t = r then  
  action ← C        # always cooperate in first and last rounds  
 Else if punish_counter > 0 then  
  action ← D  
  punish_counter ← punish_counter – 1  
 Else if last_round_any_D = true then  
  # Someone defected last round → enter punishment phase  
  action ← D  
  punish_counter ← P – 1      # total of P consecutive defections  
 Else  
  action ← C        # otherwise cooperate  

 Submit action  

 # After the simultaneous‐move reveal, update tracking variables:  
 last_round_any_D ← “Did any player (including me) play D in this round?”  

End for  

————————————————————————  
4. Why this is cooperative  
• Mutual cooperation (all C) yields the stock back to capacity each round and maximizes everyone’s long‐run payoff.  
• By starting and ending with C and by quickly resuming cooperation once punish_counter expires, you ensure that a single defection does not doom future rounds.  
• Punishments of fixed length P make defection unprofitable in expectation for sufficiently patient opponents (they know any defection today will cost them P future rounds of low payoffs).  
• Always cooperating in the final round prevents “last‐round free‐riding” on yourself and yields a clear signal of your cooperative intent throughout.  

————————————————————————  
5. Handling edge cases  
• If S_t = 0 (resource exhausted), both C and D yield zero. You still play C by the rule above—this ensures you don’t inadvertently “punish” when there’s nothing to punish.  
• If opponents never defect, you never enter punishment mode, so you enjoy full cooperation throughout.  
• If multiple defects occur in one round, you still trigger only one punishment episode of length P (not multiple).  
• If a defection occurs in round r–1, you punish in round r–1+1 = r; but since we override with “always C in last round,” you actually forgive automatically in round r.  This avoids pointless defection when the game ends.  

————————————————————————  
6. Tuning and variants  
• Choose P to balance deterrence vs. over‐punishment.  P=1 is TFT, P=2 or 3 gives a stronger threat.  
• If you want a “forgiving” variant, you can require two consecutive D’s before punishing.  That makes you less reactive to noise in opponents’ play.  
• One can also introduce a small threshold on stock (e.g. if S_t < ε cooperate only if in punishment phase) but in practice the simple TFT‐LP above is enough to sustain cooperation.  

This strategy is fully prespecified, does not rely on side‐channels or secret agreements, and meets the common‐knowledge requirements.  It aligns your incentives with those of other cooperators: long‐term, group‐wide cooperation outperforms all‐out defection.
'''

description_COOPERATIVE_51 = '''
Below is a “conditional‐Tit-for-Tat with forgiveness” strategy.  It defaults to full cooperation (which sustains the stock at capacity) but punishes any observed defection with a short, finite bout of defection, then returns to cooperation.  In the very last round it defects (standard end‐game logic).

1.  State variables  
   • punishing: Boolean flag (initially false)  
   • punish_left: integer counter (initially 0)  

2.  Parameters  
   • P = 1  (length of punishment in rounds; you can choose P=1 or 2)  

3.  Decision rules  
   For each round t = 1,2,…,r:  

   if t == 1:  
     Action ← C  
   else if t == r:  
     # last round: defect to grab the remaining stock  
     Action ← D  
   else if punishing == true:  
     # in punishment phase  
     Action ← D  
     punish_left ← punish_left – 1  
     if punish_left == 0:  
       punishing ← false  
   else:  
     # not punishing: look at previous round’s actions  
     if ∃ j ≠ i such that player j played D in round t–1:  
       # somebody defected last round → start punishment  
       punishing ← true  
       punish_left ← P  
       Action ← D  
     else:  
       # nobody defected last round → cooperate  
       Action ← C  

4.  History update (at the end of each round)  
   # record all players’ actions in this round; used above to detect defection  

5.  Rationale and cooperativeness  
   • By cooperating when no defection is detected, we keep the stock at capacity → maximal sustainable payoff each round.  
   • A defection by any opponent is met with P rounds of defection → a deterrent that raises the short‐run cost of defection but does not destroy the possibility of returning to full cooperation.  
   • Forgiveness after P rounds prevents endless collapse of cooperation if mistakes occur.  
   • Defection in the last round is unavoidable under backward induction; it does not undermine cooperation in earlier rounds because no future payoff is at stake.  

Pseudocode summary  
--------------  
initialize punishing ← false, punish_left ← 0  
for t in 1..r do  
  if t == 1 then  
    play C  
  else if t == r then  
    play D  
  else if punishing then  
    play D  
    punish_left ← punish_left – 1  
    if punish_left == 0 then punishing ← false  
  else  
    if any opponent played D in round t–1 then  
      punishing ← true  
      punish_left ← P  
      play D  
    else  
      play C  
  end if  
  observe all actions; record for next round’s test  
end for
'''

description_COOPERATIVE_52 = '''
Below is a simple but effective cooperative “trigger‐and‐forgive” strategy adapted to this common‐pool resource game.  It is designed to sustain full cooperation through almost all of the r − 1 growth–rounds, then defect in the last round (by backward induction), and to punish free‐riders swiftly but forgive them so cooperation can resume.  

Strategy name: TFT‐CPR (Tit-for-Tat for Common-Pool Resource)

1. State variables  
   • punished  (Boolean): have we been punishing a defection?  
   • last_defector_round  (integer): the most recent round in which any player defected.  

2. Initialization (before round 1)  
   punished ← false  
   last_defector_round ← 0  

3. Decision rule for each round t (1 ≤ t ≤ r) with observed history of all players’ moves up to t−1:  
   
   if t == r then  
     // Last round: standard endgame defection  
     Action = D  
     return Action  
   end if  
   
   if t == 1 then  
     // No history → cooperate to build reputation  
     Action = C  
     return Action  
   end if  
   
   // t in {2,…,r−1}: check recent history  
   if last_defector_round == t−1 then  
     // We are entering a punishment turn  
     punished ← true  
   end if  
   
   if punished then  
     // Punish for exactly one round  
     Action = D  
     punished ← false        // forgive on the following round  
     return Action  
   end if  
   
   // No immediate punishment on deck → cooperate by default  
   Action = C  
   return Action  

4. Updating history after observing all players’ moves in round t:  
   if any player played D in round t then  
     last_defector_round ← t  
   end if  

5. Intuition & properties  
 • Mutual cooperation (all choose C) from round 1 through round r−1 keeps the stock near capacity each turn, yielding the highest possible group payoff.  
 • A solitary or occasional defection in round t is met with exactly one round of universal punishment (round t+1), after which cooperation resumes.  This one‐round “tit-for-tat” punish‐and‐forgive gives defectors a clear cost while not locking the group into permanent defection.  
 • In the final round (t = r), no future rounds remain, so we defect to grab the one‐shot higher payoff.  This is the standard backward‐induction “endgame” move.  
 • Because punishments are brief and cooperation is resumed as soon as the trigger round passes, this strategy tends to maintain high stock levels and high total payoffs for all players, provided others are also willing to cooperate.  

Pseudocode summary  

```
initialize punished ← false
initialize last_defector_round ← 0

for t in 1..r:
  if t == r:
    play D
    break

  if t == 1:
    play C
  else:
    if last_defector_round == t-1:
      punished ← true

    if punished:
      play D
      punished ← false
    else:
      play C

  observe opponents’ moves in round t
  if any opponent played D:
    last_defector_round ← t
```

Edge cases handled  
– First round: no history → cooperate to signal goodwill.  
– Any single defection → exactly one round of punishment, no more.  
– Forgiveness: punished is reset after one round, so cooperation can restart.  
– Last round (no future): defect unconditionally.
'''

description_COOPERATIVE_53 = '''
Below is a simple, fully‐specified “tit-for-tat with endgame defection” strategy that (1) sustains full cooperation as long as everyone has cooperated, (2) punishes any defection with a single‐round of defection, then forgives, and (3) defects in the last round (since there is no future to protect).

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
1. STATES AND VARIABLES  
––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
We keep two pieces of memory between rounds:  
• state ∈ {COOP, PUNISH}  
• punish_timer ∈ {0,1,…}  

Initialize before round 1:  
state  ← COOP  
punish_timer ← 0  

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
2. DECISION RULES (per round t)  
––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
Input each round:  
• t (current round), r (total rounds)  
• S_t (current stock)  
• a_{−i,t−1} (the vector of opponents’ actions last round; undefined if t=1)  

Algorithm:  
If t == r then  
    play D  ⟶ endgame defection  
    STOP  
End if  

# 1) Handle any ongoing punishment  
If punish_timer > 0 then  
    play D  
    punish_timer ← punish_timer – 1  
    If punish_timer == 0 then state ← COOP  
    STOP  
End if  

# 2) In COOP state, check last round’s actions  
If state == COOP then  
    If t == 1 then  
        play C            ⟶ start by trusting  
    else  
        If every opponent played C in round t−1 then  
            play C        ⟶ continue cooperation  
        else  
            # someone defected last round → switch to punishment  
            state ← PUNISH  
            punish_timer ← 1    ⟶ punish for exactly 1 round  
            play D  
        End if  
    End if  
End if  

If state == PUNISH then  
    # this branch only happens if punish_timer was 0 but state==PUNISH  
    # (shouldn’t occur under normal flow), so reset:  
    state ← COOP  
    play C  
End if  

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
3. EXPLANATION AND PROPERTIES  
––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
• Mutual cooperation (all C) is an absorbing path through rounds 1…r−1.  
  – If no one ever defects, state stays COOP and everyone plays C,  
    sustaining the stock at capacity each round.  
• Single‐round punishment (punish_timer=1) is enough to deter one‐off defections  
  but limits harm to the stock. After one D‐round, we quickly return to cooperation.  
• Endgame defection (round r: always D) maximizes our last‐round gain when no future remains.  
• No reliance on side channels or pre-game agreements—only on directly observed moves.  
• Edge cases:  
  – Round 1: unconditional C to build trust.  
  – Round r: unconditional D (no future to protect).  
  – If stock ever hits S_t=0, payoffs are zero anyway; our rules still apply but cannot restore payoffs.  

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
4. PSEUDOCODE SUMMARY  
––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
state ← COOP  
punish_timer ← 0  

for t in 1…r do  
  observe S_t  
  if t == r then  
    action ← D  
  else if punish_timer > 0 then  
    action ← D  
    punish_timer ← punish_timer – 1  
    if punish_timer == 0 then state ← COOP  
  else if state == COOP then  
    if t == 1 or (t > 1 and all opponents played C in t−1) then  
      action ← C  
    else  
      state ← PUNISH  
      punish_timer ← 1  
      action ← D  
    end  
  else  # fallback  
    state ← COOP  
    action ← C  
  end  
  submit action  
end  

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
This simple “TFT‐with‐endgame‐defection” keeps the resource at capacity, rewards cooperators, punishes defectors just long enough to deter free-riding, and captures the final‐round incentive to defect.
'''

description_COOPERATIVE_54 = '''
Below is a single‐agent “cooperative” strategy that (1) starts out fully cooperative to keep the stock at capacity, (2) punishes one‐round defections à la Tit-for-Tat, (3) unconditionally cooperates whenever the stock has fallen very low (to help it recover), and (4) defects in the very last round (since there is no future to protect).  You can tune the punishment length, the “low‐stock threshold,” or the length of the end‐game defection window to your taste.

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
Name: State-Aware Tit-for-Tat with Endgame Defection (SATT-ED)  

Parameters you can set once at the start:  
• punish_len L (integer ≥1), number of rounds to defect after seeing a defection.  
  Typical choice: L=1 (plain TFT).  
• endgame E (integer ≥1), number of last rounds to unconditionally defect.  
  Typical choice: E=1.  
• low_stock_fraction α (0<α<1), fraction of capacity below which we always cooperate to help recovery.  
  Typical choice: α=0.1.  

Internal state:  
• punish_timer ← 0  

Pseudocode:  
  Let S_t be the stock at the start of round t.  
  Let a_j,t be player j’s action in round t (observed at the end of the round).  

  For each round t = 1,2,…,r do:  
    if t > r − E then  
      • action_i ← D  
        (Last E rounds: defect for maximum one‐shot gain.)  

    else if S_t < α × capacity then  
      • action_i ← C  
        (If stock is very low, cooperate to help it regrow.)  

    else if punish_timer > 0 then  
      • action_i ← D  
      • punish_timer ← punish_timer − 1  
        (Carry out remaining punishment rounds.)  

    else if t>1 and ∃ j≠i with a_j,t−1 = D then  
      • punish_timer ← L − 1  
      • action_i ← D  
        (First round of punishment after seeing any defection.)  

    else  
      • action_i ← C  
        (No reason to punish, stock is healthy, and not in endgame ⇒ cooperate.)  

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  

How it works:  
1. First round (t=1): no history, stock is full ⇒ play C.  
2. If everyone keeps playing C, the stock stays at capacity and each round you get capacity/(2n), the group‐optimal flow.  
3. If anyone defects in round t, you retaliate in round t+1 for L rounds, then return to cooperation.  
4. If the stock ever falls below α·capacity, you switch to cooperation unconditionally until it recovers, to restore future flow.  
5. In the final E rounds you defect—there is no future to protect, so you grab the higher per‐round payoff.  

This strategy is cooperative in that it:  
• Maintains full cooperation whenever there are no defections and the resource is healthy.  
• Only defects to punish observed selfish play (and for the last‐round gain).  
• Helps the stock recover if it ever collapses too far.  

Feel free to adjust L, E, α to trade off severity of punishment, end‐game exploitation, and willingness to help the resource bounce back.
'''

description_COOPERATIVE_55 = '''
Below is a single‐strategy “Tit-for-Tat with Endgame Defection” that (i) sustains cooperation as long as others do, (ii) punishes defections briefly, and (iii) secures the final‐round payoff.

1. Overview of the idea  
   • First round: signal cooperation.  
   • On each non‐terminal round, do what the majority did to you last round—cooperate if everyone cooperated, defect once if someone defected.  
   • In the last round, defect (no future to enforce cooperation).  

2. Key parameters and state  
   • r = total number of rounds  
   • n = number of players  
   • History: for each past round t, we know each player’s action.  
   • punishing = 0 or 1 (counts how many rounds of punishment remain)  

3. Decision rules in words  
   Round t = 1: play C.  
   Rounds t = 2,3,…,r–1:  
     – If punishing > 0: play D, then punishing ← punishing – 1.  
     – Else if in round t–1 at least one other player played D:  
         • set punishing ← 1  (punish exactly one round)  
         • play D this round.  
     – Otherwise (no defection observed last round and not in punishment): play C.  
   Round t = r: play D.  

4. Pseudocode  
   --------------------------------  
   Initialize punishing ← 0  
   For t in 1…r do  
     if t == 1 then  
       action_t ← C  
     else if t == r then  
       action_t ← D  
     else if punishing > 0 then  
       action_t ← D  
       punishing ← punishing – 1  
     else  
       if ∃ j≠me s.t. action_{t–1, j} == D then  
         punishing ← 1  
         action_t ← D  
       else  
         action_t ← C  
       end  
     end  
   end  
   --------------------------------  

5. Why this is cooperative  
   • It never defects first (round 1 is C).  
   • It restores cooperation after a single‐round punishment, so mistakes or noise don’t lead to endless war.  
   • It only defects in the very last round to claim the remaining value when no future punishment is possible.  

6. Handling edge cases  
   – If two or more players defect simultaneously, you still punish only one round, then return to full cooperation.  
   – If r=2, round 1→C, round 2→D (no room to punish).  
   – If r=3, you’ll do C (t=1), punish t=2 if needed, then D in t=3.  

This strategy balances strong incentives to keep the common pool healthy (you only defect as a response) with a credible one‐round punishment, and it takes the remaining value at the end when cooperation cannot be enforced.
'''

description_COOPERATIVE_56 = '''
Below is a single‐player “cooperative” strategy—call it STFED (Sustained Tit‐For‐Tat with Endgame Defection)—that in effect supports full cooperation (everyone choosing C) as long as no one defects, administers a brief one‐round punishment if any defection is ever observed, and then returns to cooperation.  In the very last round it defects (as in any finitely repeated game this is dominant), but by then the stock is still high if cooperation has held, so the one‐round endgame defection does little damage to total payoffs.

––––––––––––––––––––––––––––––––––––  
1.  DATA STRUCTURES / STATE  
––––––––––––––––––––––––––––––––––––  
• punish_flag: Boolean, initially False  
• history of each round’s joint actions (publicly observed)  
• round counter t = 1,…,r  

––––––––––––––––––––––––––––––––––––  
2.  PSEUDOCODE  
––––––––––––––––––––––––––––––––––––  
Initialize punish_flag ← False  
For t from 1 to r do:  
  Let R = r – t + 1   (rounds remaining, including this one)  
  If t = 1 then  
    action ← C        # Always start by cooperating  
  Else if R = 1 then  
    action ← D        # Last round: defect  
  Else if punish_flag = True then  
    action ← D        # Carry out punishment for one round  
    punish_flag ← False  
  Else  
    # Examine what happened in round t–1  
    If any player played D in round t–1 then  
      action ← D           # Trigger a one‐round punishment  
      punish_flag ← True  
    Else  
      action ← C           # No defection last round → cooperate  
    End If  
  End If  

  Play(action)  
End For  

––––––––––––––––––––––––––––––––––––  
3.  EXPLANATION / RATIONALE  
––––––––––––––––––––––––––––––––––––  
• We aim to keep the common stock high (near capacity), so that every round’s cooperative payoff π_i=S/(2n) is maximized repeatedly.  
• By starting with C and reverting to C immediately after a one‐round punishment, we make defection unprofitable: any defector loses the cooperative payoff of the next round.  
• Because actions and payoffs are symmetric and public, all “good” players run the same strategy and thus remain in lockstep: full cooperation unless some defector is seen.  
• In the very last round, standard backward‐induction says D is dominant, so we defect—but only then.  By that late point the stock should still be high if cooperation held, so the loss to future rounds is minimal (there are none).  
• This strategy is straightforward to implement, resistant to single deviations, and maintains the common pool at or near capacity for the bulk of the game.  

––––––––––––––––––––––––––––––––––––  
4.  HANDLING EDGE CASES  
––––––––––––––––––––––––––––––––––––  
– First round (t=1): cooperate by fiat, to signal willingness.  
– Last round (R=1): defect, capturing the larger one‐shot payoff.  
– Single defection anywhere before last round: punished by exactly one round of D, then resume C.  
– Multiple defections in a row get chained punishments each time (because each round you detect a defection in t–1).  
– No additional threshold checks on S are needed—by sticking to C when others do, the stock regenerates toward capacity automatically.  

This STFED rule set neatly enforces full‐game cooperation (C,C,…,C) until the inevitable endgame defect, maximizes the sustainable stock, and punishes any unilateral deviation.
'''

description_COOPERATIVE_57 = '''
Below is a single‐strategy outline—“Generous Tit-for-Tat with One-Round Punishment”—that achieves near–full cooperation over most of the r rounds, yet is simple, forgiving, and handles edge cases cleanly.

1.  State variables  
    •  p  – punishment counter (integer ≥ 0), initially p = 0  
    •  t  – current round index, t=1,2,…,r  
    •  Sₜ – common‐pool stock at the start of round t (fully observed)

2.  Intuition  
    •  Start by cooperating to build trust.  
    •  As long as everyone cooperated last round, continue to cooperate.  
    •  If anybody defected last round, punish by defecting exactly one round, then forgive unconditionally.  
    •  In the very last round, defect to collect the maximum immediate payoff (standard backward‐induction adjustment).

3.  Pseudocode  

```
Initialize:
  p ← 0             # punishment counter
  For t from 1 to r do:
    Observe previous round’s actions (for t>1) and current stock Sₜ.

    If t == 1 then
      # First round: no history → cooperate
      Actionₜ ← C

    Else if t == r then
      # Last round: defect for immediate gain
      Actionₜ ← D

    Else
      If p > 0 then
        # We are serving a punishment
        Actionₜ ← D
        p ← p − 1

      Else
        # No current punishment: check last round
        If (in round t−1 any player chose D) then
          # Trigger one‐round punishment
          Actionₜ ← D
          p ← 1         # set up one round of punishment next time
        Else
          # Everyone cooperated last time → cooperate now
          Actionₜ ← C
        End If
      End If
    End If

    # Play Actionₜ; observe payoffs and update stock to Sₜ₊₁ via game’s dynamics
  End For
```

4.  Decision rules, in plain English  
  – Round 1: Cooperate.  
  – Rounds 2…r–1:  
    • If you are “in punishment” (p>0), defect this round and decrement p.  
    • Otherwise, look at the previous round:  
      – If anybody defected, defect now and set p=1 so that you defect for exactly one more round after this.  
      – If nobody defected, cooperate.  
  – Round r (final round): Defect unconditionally.

5.  Why this is cooperative  
  – It quickly converges to full cooperation if all players start by cooperating.  
  – Any defection anywhere is met with exactly one round of punishment—enough to deter exploitation but not so long as to collapse future surplus.  
  – Forgiveness is built in: after one punishing defection, the strategy immediately returns to cooperation.  
  – Because the game is finite, we defect in round r to capture the last‐round payoff, but up to that point we maintain the resource at its capacity (or near it) by almost never over‐harvesting.

6.  Edge‐case handling  
  • First round: no history → cooperate to signal goodwill.  
  • Single defection in a multi­player round: the strategy punishes for exactly one round, regardless of how many defected.  
  • Back-to-back defections: each triggers its own one-round punishment, but punishments do not stack; you’ll defect exactly one round after each defection event.  
  • Last round: we defect to avoid being exploited ourselves, matching standard finite-horizon logic.  
  • Stock near zero: even during punishment the stock is low so defecting yields little, but because punishments are short, we soon return to cooperation and allow regrowth.

This strategy is simple, transparent, aggressively cooperative when others cooperate, yet contains a light, credible threat to discourage over­harvesting.
'''

description_COOPERATIVE_58 = '''
Below is a simple yet robust “trigger‐and‐punish” strategy that (i) sustains full cooperation whenever no one has deviated, (ii) punishes deviations, and (iii) admits the unavoidable fact that in the final round all rational players will defect.

Notation  
– t = round index, t=1,…,r  
– S_t = stock at the start of round t  
– C‐threshold = S_t/(2n) per‐player consumption under full cooperation  
– total_consumption_t = sum of all players’ draws in round t  
– defect_flag (initially false): becomes true as soon as any deviation is detected  

Strategy for player i  
1. Initialization (before round 1):  
   defect_flag ← false  

2. At the start of each round t do:  
   if t = r then  
     play D  // last‐round defection  
   else if defect_flag = true then  
     play D  // punish phase  
   else  
     play C  // cooperative phase  

3. After observing total_consumption_t at the end of round t < r:  
   if total_consumption_t > S_t/2 + ε then  
     // someone must have played D  
     defect_flag ← true  

Here ε ≥ 0 is a tiny tolerance to allow for numerical rounding; you can set ε=0 if exact arithmetic is assumed.  

Explanation of key features  
1. Full cooperation when defect_flag=false:  
   – As long as every past round’s total consumption has been exactly S/2 (i.e. everyone played C), you continue to cooperate.  
   – Under full cooperation S_{t+1}=capacity and each round’s payoff is capacity/(2n), which is the sustainable group optimum.  

2. Detection of deviation:  
   – If any single player defects in round t, total_consumption_t jumps from S_t/2 up to at least S_t/2 + S_t/(2n) > S_t/2.  
   – By checking total_consumption_t > S_t/2+ε we know “someone defected.”  

3. Punishment:  
   – Once a deviation is detected (defect_flag=true), you defect every subsequent round (except the last, where you already planned to defect)  
     – This drives the stock down more quickly and makes unilateral deviations unprofitable.  
     – Because the punishment is permanent (Grim Trigger), the short‐term gain from one defection is outweighed by the stream of losses in all future rounds.  

4. Last‐round defection:  
   – In round r any strategy must defect, since there is no future punishment to sustain cooperation.  

Pseudocode summary  
```
initialize defect_flag ← false

for t in 1…r do
  observe S_t
  if t = r then
    action_i ← D
  else if defect_flag = true then
    action_i ← D
  else
    action_i ← C
  end if

  play action_i simultaneously

  observe total_consumption_t
  if t < r and total_consumption_t > S_t/2 + ε then
    defect_flag ← true
  end if
end for
```

Why this is cooperative  
– Against another copy of itself, all players will cooperate every round t<r, keeping the stock at capacity and each earning capacity/(2n) every time.  
– Any lone defection is instantly detected and punished by permanent defection—so no one gains in expectation by deviating.  
– It is simple, robust to noise (via a small ε), and it achieves the highest sustainable payoff stream possible in repeated play.
'''

description_COOPERATIVE_59 = '''
Below is a single‐agent “cooperative” strategy designed to sustain high joint payoffs in the repeated common‐pool–resource game.  It is essentially a Tit‐for‐Tat rule with a short, finite punishment phase and the standard last‐round defection.

1. Intuition  
   • In every round except the very last, we want to play Cooperate (C) so long as all others cooperated in the previous round.  
   • If we detect any defection, we defect for a fixed number of rounds (punishment) to make one‐shot defection unprofitable.  
   • After punishment we “forgive” and return to cooperation—this discourages endless mutual defection.  
   • In the final round there is no future to protect, so we defect (the standard backward‐induction end‐game).

2. Parameters  
   Let r = total rounds.  
   Choose a punishment length P ≥ 1, e.g. P = min(3, r–2).  (You can calibrate P so that the one‐round gain from defection is outweighed by P‐round loss.)

3. State variables (maintained by our agent)  
   punish_remaining ← 0   // how many rounds of punishment are left  
   history_of_actions      // full record of who played C or D each past round

4. Decision rule (pseudocode)

For each round t = 1,2,…,r:  
  if t == 1 then  
    action_t ← C                              // no past history, start cooperatively  
  else if t == r then  
    action_t ← D                              // last round: defect (no future to protect)  
  else if punish_remaining > 0 then  
    action_t ← D                              // we are punishing  
    punish_remaining ← punish_remaining – 1  
  else  
    // inspect round t–1:
    if every other player j played C in round (t–1) then  
      action_t ← C  
    else  
      // someone defected last round: trigger punishment
      punish_remaining ← P – 1                // we will defect now + P–1 more rounds  
      action_t ← D  
    end if  
  end if  

5. Edge‐case handling  
  • First round (t=1): no information → cooperate.  
  • Last round (t=r): always defect (standard end‐game logic).  
  • If defection occurs in round r–1, we would set punish_remaining but never actually enter a new round after r, so punishment auto‐expires.  
  • If multiple defections happen in quick succession, punish_remaining is simply reset (we never stack punishments beyond length P).

6. Why it’s cooperative  
  • So long as all players cooperate, we will cooperate every round up to r–1—this maximizes the sustained stock and each player’s payoff.  
  • A single defection by any player is met not with permanent wrath but with a short punishment, after which we return to full cooperation.  
  • This rule gives every player an incentive to stay in the cooperative phase: a one‐round gain from defection is outweighed (for prudent choice of P) by losing P future cooperative payoffs.  
  • The “forgiveness” feature prevents the system from locking into mutual defection if one noise/mistake occurs.

You can implement this pseudocode directly.  In a tournament of independently designed strategies, it should foster high‐stock trajectories and deter free‐riding.
'''

description_COOPERATIVE_60 = '''
Here is a simple, fully‐specified “cooperative trigger” strategy that (i) starts by cooperating, (ii) punishes defectors briefly, (iii) forgives and returns to cooperation, and (iv) defects in the very last round (since there is no future to protect).

Notation and bookkeeping  
• r           – total number of rounds  
• t           – current round (1 ≤ t ≤ r)  
• Sₜ        – common‐pool stock at start of round t  
• history    – keeps track of each player’s action in each past round  
• punishLeft – counter for how many more rounds we will punish (initially 0)  

Fixed parameters  
• p = 1      – length of punishment in rounds (after we see a defection, we defect for p rounds)  
• M = 1      – number of final rounds in which we always defect (endgame defection)  
• T = capacity/2   – a safety threshold: if the stock ever falls below T, we cooperate to help it regrow  

Decision rule (executed at the start of each round t):  
1. If t > r – M (i.e. in the very last M round(s)), play D and stop.  
2. Else if punishLeft > 0, then  
     a. play D  
     b. punishLeft ← punishLeft – 1  
3. Else if Sₜ < T, then  
     play C    // stock is low ⇒ cooperate to restore it  
4. Else if in round t–1 any player (including ourselves) chose D, then  
     punishLeft ← p  
     play D    // respond to defection with a 1‐round punishment  
5. Else  
     play C    // the baseline is cooperation  

Edge cases  
• Round 1 (t=1):  
   – t ≤ r – M, punishLeft=0, no prior history, S₁ = capacity ⇒ falls to step 5 ⇒ play C.  
• Last round (t = r):  
   – t > r – M ⇒ step 1 ⇒ play D.  
• If multiple defectors appear simultaneously, we still punish only p rounds in total. After punishment expires we go back to step 5 and resume cooperation (thus “forgiving” past defections).  
• If the common pool has collapsed (Sₜ = 0) or fallen below T, we switch to unconditional cooperation (step 3) to rebuild the stock.  

Pseudocode  

```
initialize punishLeft ← 0

for t in 1..r:
  observe current stock S_t
  if t > r – M:
    action ← D
  else if punishLeft > 0:
    action ← D
    punishLeft ← punishLeft – 1
  else if S_t < T:
    action ← C
  else if (any player chose D in round t–1):
    punishLeft ← p
    action ← D
  else:
    action ← C

  play action
  record action in history
  observe others’ actions and next stock S_{t+1}
end for
```

Why this is cooperative  
• We begin by maximizing long‐run yield (by cooperating), which keeps the stock near capacity.  
• We only defect to punish clear deviations, and only for a brief, pre‐committed period (p=1).  
• After punishment we immediately return to full cooperation, so cooperators are never locked into mutual defection.  
• We even forgive accidental stock collapses by switching to cooperation if S falls below T.  
• We defect in the very last round because, with no future to protect, unilateral defection there is strictly payoff‐maximizing.  

This strategy thus (a) sustains cooperation for as long as there is a future to protect, (b) punishes free‐riding just enough to deter it, (c) forgives quickly to rebuild mutual trust, and (d) defects only when the horizon forces it.
'''

description_COOPERATIVE_61 = '''
Here is a simple yet effective “conditional‐cooperation” strategy that (i) maximizes the chance of sustaining near–full cooperation on all interior rounds, (ii) punishes defectors quickly, (iii) forgives after a short punishment, and (iv) takes into account the inevitable unraveling in the very last round of a finite game.

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
1.  Intuition and Goals  
   • We want everyone to play C most of the time so the pool remains high and payoffs are large.  
   • If anyone ever defects, we impose a one‐round “tit-for-tat” punishment (we defect in the very next round), then we go back to cooperating.  
   • We cooperate in round 1 (to signal goodwill).  
   • We know that in the very last round (round r) there is no future to protect, so we defect there (like any self-interested player).  

2.  Strategy Description in Words  
   ––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
   Initialization:  
     • Set a flag punish_until = 0.  
     • (We will use punish_until to record the round up to which we are punishing.)

   At each round t = 1,2,…,r:  
     1.  If t = 1, play C.  
     2.  Else if t = r, play D.  
     3.  Else if t ≤ punish_until, play D (we are in punishment mode).  
     4.  Otherwise, play C.  

   After all actions in round t are publicly revealed:  
     • If any player played D in round t, then set punish_until = t + 1.  
       – That means “punish” for exactly one round immediately following the defection.  
       – If multiple players defect, we still only punish one round.  
       – If defections continue, punish_until will keep being pushed forward by one round at a time.  
     • Otherwise (if everyone played C), leave punish_until unchanged.  

3.  Pseudocode  
   –––––––––––––––––––––  
   initialize punish_until ← 0

   for t in 1…r do
     if t == 1 then
       action_t ← C
     else if t == r then
       action_t ← D
     else if t ≤ punish_until then
       action_t ← D
     else
       action_t ← C
     end if

     play(action_t)

     // Observe everyone’s action this round
     if (∃ j : action_j == D) then
       punish_until ← t + 1
     end if
   end for

4.  Why This Works as a Cooperative Strategy  
   1.  On rounds 2 through r–1, as long as no one has defected in the immediately preceding round, we cooperate (keep the stock high).  
   2.  The moment anyone defects, we defect in the very next round—this exact reciprocity deters profitable one‐off deviations because the defector’s extra gain in round t is offset in round t+1.  
   3.  After that one round of punishment, we automatically forgive and return to cooperation, which prevents the harsh permanent collapse you get under a grim‐trigger strategy.  
   4.  In round r we defect unconditionally (standard backward‐induction “last‐round” move).  All rational players know we will defect then, but for t < r this knowledge does not undermine our incentive to cooperate earlier, because the one‐round punishment is always available.  

5.  Handling Edge Cases  
   – First round (t = 1): We cooperate unconditionally to signal friendliness and to build up the stock.  
   – Last round (t = r): We defect, since there is no future round in which to punish us—this aligns with individual incentive in a finite game.  
   – Back‐to‐back defects: If players keep defecting, punish_until will keep getting extended so we will keep defecting exactly one round after each defection, continuing throughout.  
   – Return to cooperation: The moment a round goes by with full cooperation (no Ds), we drop punishment and resume C on the next interior round.  

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
This “one‐round tit-for-tat with end‐game defection” is easy to implement, easy to recognize, forces any would-be defector to pay back what they gained, and yet re-establishes full cooperation rapidly once everyone is back in line. It maximizes the total stock and total payoffs across rounds 2…r–1, while correctly playing the unique Nash move (D) in round 1’s continuation (nothing to punish) and round r (no more future).
'''

description_COOPERATIVE_62 = '''
Below is a simple, fully‐specified “coop‐minded” strategy based on a multi‐player Tit-for-Tat (TFT) with a one‐round punishment and the standard end‐game defection.  It (1) starts by cooperating, (2) punishes any defector by defecting exactly one round, (3) immediately forgives if everyone then cooperates, and (4) defects in the final round (since there is no future to protect).

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––
STRATEGY “MP‐TFT + One‐Shot Punish + Last‐Round Defect”

Parameters:
  n     number of players (≥2)  
  r     total rounds (>1)  

State variables (maintained across rounds):
  last_defection_flag  ← false  
    // did any player play D in the previous round?

Decision rule for player i in round t:
  if t == 1 then
    action_i ← C
  else if t == r then
    action_i ← D
  else if last_defection_flag == true then
    // punish any defection by defecting this round
    action_i ← D
  else
    // no defection last round → cooperate
    action_i ← C

After all actions are observed in round t, update:
  last_defection_flag ← (∃ j ∈ {1…n} such that action_j == D)

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––
Explanation of key features

1. First‐round cooperation  
   • We begin with C to signal willingness to build up the stock.  

2. One‐round punishment (Tit-for-Tat style)  
   • If anybody defects in round t–1, we defect in round t.  
   • This hurts the deviator (and everybody else temporarily) but is strong enough to deter repeat defections.  
   • If all return to C after that punishment, we immediately go back to cooperation.  

3. Forgiveness  
   • Because we reset last_defection_flag to false as soon as we see a round of all‐C, we never hold a grudge longer than one round.  

4. Last‐round defection  
   • In round r every self‐interested player has an incentive to take the bigger immediate payoff and there is no future to protect, so we defect there.  
   • This preserves the one‐round‐ahead consistency of the strategy.  

5. Cooperative mindset  
   • Until someone defects, we always cooperate—maximizing stock, hence per‐round payoffs S/(2n).  
   • Punishment is calibrated to last only one round, so accidental slips or noise are forgiven quickly, restoring full cooperation.  

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––
Pseudocode

  initialize last_defection_flag ← false

  for t in 1…r do
    if t == 1 then
      play C
    else if t == r then
      play D
    else if last_defection_flag then
      play D
    else
      play C

    observe all actions {action_j}
    last_defection_flag ← (any action_j == D)
  end for

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––
Why this can sustain cooperation

– As long as every player follows the same rule, no one has an incentive to deviate:  
   • If you defect in some round t, you get a one‐time bump (S_t/n instead of S_t/(2n)), but next round you—and everyone else—will D and drive stock down.  
   • The lost future payoffs more than offset the one‐round gain, provided r > 1 and the growth dynamics are nontrivial.  

– Because punishment lasts only one round and is followed by immediate forgiveness, mutual cooperation quickly re-establishes full stock regrowth, yielding the highest sustainable average payoff S/(2n) per player.  

– Defecting in the very last round r is unavoidable if one is purely self-interested, and it does not undermine earlier cooperation.
'''

description_COOPERATIVE_63 = '''
Below is a single‐strategy “cooperator with disciplined punishment” suitable for a round‐robin tournament of anonymous strategies.  It combines near‐full cooperation (to maintain a high stock), a short “tit‐for‐tat”–style punishment for any observed defection, a simple low‐stock switch to last‐round defection, and a commitment to cooperate in the very last round (to avoid the end‐game unraveling that plagues strict backward induction).  

----  
1.  Definitions and internal state  
   •  r = total number of rounds, indexed t=1,…,r  
   •  n = number of players  
   •  capacity = stock ceiling  
   •  S_t = observed common‐pool stock at the start of round t  
   •  HISTORY_t = the full action profile in past rounds 1…t–1  
   •  punish_timer = integer ≥0, counts down punishment rounds yet to play  
   •  S_low = capacity/4   (a low‐stock threshold)  
   •  P = max(1, ⌊r/10⌋)   (punishment duration)  

2.  Overall outline  
For each round t = 1,…,r:  
   1.  Observe S_t and HISTORY_t.  
   2.  Decide action A_t ∈ {C,D} by these rules (in priority order):  

     Rule 1  (low‐stock switch)  
       If S_t ≤ S_low then  
         A_t ← D  
         (Rationale: once the stock is too low to regrow profitably, switch to “harvest what’s left.”)  

     Else Rule 2  (last‐round cooperation)  
       If t = r then  
         A_t ← C  
         (Rationale: avoid mutual defection in the final round; if everyone cooperates, group earns S_r/(2n) each rather than 0.)  

     Else Rule 3  (active punishment)  
       If punish_timer > 0 then  
         A_t ← D  
         punish_timer ← punish_timer – 1  
         (Continue punishing for P total rounds after any detected defection.)  

     Else Rule 4  (trigger on most‐recent defection)  
       If in round t–1 any other player j played D then  
         punish_timer ← P–1  
         A_t ← D  
         (Punish immediately for P rounds in total, including this one.)  

     Else Rule 5  (cooperate)  
       A_t ← C  

3.  Pseudocode  
```
initialize punish_timer ← 0
for t in 1…r:
  observe S_t, HISTORY up through round t–1
  if S_t ≤ capacity/4:
    A_t ← D
  else if t == r:
    A_t ← C
  else if punish_timer > 0:
    A_t ← D
    punish_timer ← punish_timer – 1
  else if (any opponent played D in round t–1):
    punish_timer ← P – 1
    A_t ← D
  else:
    A_t ← C
  execute A_t
```

4.  Discussion of features  
  •  “Generous/tit‐for‐tat” flavor: we start every round by cooperating unless we have a recent reason to punish.  
  •  Finite‐horizon safeguard: we commit to cooperate in the very last round, which helps sustain cooperation beforehand (it softens the backward‐induction end‐game collapse).  
  •  Short, fixed punishments (P rounds) rather than a grim forever‐defection.  This caps the damage to everyone and allows quick restoration of full cooperation.  
  •  Low‐stock cutoff: if the pool falls under capacity/4, growth is too weak to recover—better to “harvest” what remains.  
  •  All required information—past actions and current stock—is publicly observable, and no extra coordination device is used.  

5.  Edge cases  
  •  Round 1: t=1, no punish_timer, no t–1 history → falls to Rule 5 → C.  
  •  Rounds t near r: in round r–1, if nobody defected in r–2 we cooperate; if someone defected in r–2 we punish once (since punish_timer=P–1≥1) then at t=r we override to C.  
  •  If multiple defections occur, punish_timer may reset each time you see D at t–1, but never exceeds P–1, so punishment bursts remain bounded.  

This strategy is fully cooperative in intent—it maintains the pool near capacity through mutual C’s, retaliates against free‐riders just long enough to make defection unprofitable, and then returns to cooperation—while gracefully handling the last round and low‐stock scenarios.
'''

description_COOPERATIVE_64 = '''
Below is a simple, fully-specified “conditional cooperation” strategy that (a) sustains the common stock at or near capacity, (b) punishes defectors so that unilateral defection is unprofitable, and (c) accounts for first and last rounds.  It is sometimes called a “grim‐trigger with endgame defection” rule.

1. State variables  
– punishing ∈ {false,true}: have we observed any defection?  
– t: current round number, t=1,…,r  

2. Overview of the rule  
– Rounds 1 through r−1: Cooperate (C) as long as no one has ever defected; if anyone has defected at any previous round, switch to permanent defection (D).  
– Round r (last round): Always defect (D).  

3. Why it works cooperatively  
– If all players adopt this rule, nobody defects in rounds 1…r−1 → the stock always regenerates to capacity, and each round every player receives capacity/(2n).  
– A unilateral defection in any round t<r immediately triggers all players to defect in every remaining round, destroying the stock and punishing the defector far more than the one‐round gain.  
– In the last round there is no future to punish defection, so all rational players defect—but by then the stock has been kept healthy.  

4. Pseudocode  

```
Initialize:
  punishing ← false

For each round t = 1 to r do:
  if t == r then
    action_i ← D
  else if punishing == true then
    action_i ← D
  else
    action_i ← C

  // Play action_i simultaneously, observe all actions this round
  Observe others’ actions A₋i(t)
  if any player j ∈ {1…n} played D in A₋i(t) then
    punishing ← true
  end if
end for
```

5. Edge‐case handling  
– First round (t=1): punishing=false, t≠r, so we play C.  
– Any single defection in rounds 1…r−1 flips punishing to true and ensures D for the rest of the game.  
– Last round (t=r): we ignore punishing and play D, since there is no future to enforce cooperation.  
– If r=2, we cooperate in round 1, defect in round 2; if someone defects in round 1, we defect round 2 (which we would do anyway).  

6. Key properties  
– Mutual cooperation (all C) is an equilibrium path yielding high sustained payoffs: each round π_i = capacity/(2n).  
– A one‐shot defector in any non‐final round gains capacity/n instead of capacity/(2n), but then loses all future payoffs, making defection unprofitable.  
– The last‐round defection is standard backward‐induction logic but does not reduce total long‐run welfare because the stock has been preserved up until then.
'''

description_COOPERATIVE_65 = '''
Below is a fully specified, self‐contained “generous tit‐for‐tat” style strategy that (1) begins by cooperating, (2) punishes defections for exactly one round, (3) then immediately returns to cooperation, and (4) in the very last round still “gives the benefit of the doubt” if no one has ever defected before.  It requires only public history of who played C or D, and no private communication or signal.

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
Strategy: Generous Tit‐for‐Tat with One‐Round Punishment  
––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  

Shared notation  
• n, r, capacity are common knowledge.  
• For each round t=1…r each player i simultaneously chooses a_t^i ∈ {C,D}.  
• H_{t−1} = full history of actions up to and including round t−1.  
• Defected_{t−1} = true if, in round t−1, at least one player j chose D; false otherwise.  
• EverDefected = true if at any prior round someone played D; else false.  
• PunishRoundsRemaining = an integer counter, initially 0.  
• RemainingRounds = r − t + 1 (including the current t).  

Initialization (before t=1)  
PunishRoundsRemaining ← 0  
EverDefected ← false  

Decision rule for each round t=1…r  
1. Observe H_{t−1}, compute  
   if t>1 and Defected_{t−1}=true then  
     EverDefected ← true  

2. If PunishRoundsRemaining > 0 then  
     • Play D  
     • PunishRoundsRemaining ← PunishRoundsRemaining − 1  
     • Continue to next round  
   End if  

3. (Special last‐round rule)  
   If t = r then  
     If EverDefected = false then  
       Play C  
     Else  
       Play D  
     End if  
     Stop.  
   End if  

4. (Regular rule for 1 ≤ t < r, and PunishRoundsRemaining=0)  
   If t=1 (no history) then  
     Play C  
   Else  (t>1)  
     If Defected_{t−1} = true then  
       // trigger a one‐round punishment  
       PunishRoundsRemaining ← 1  
       Play D  
     Else  
       // maintain cooperation  
       Play C  
     End if  
   End if  

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
Explanation and Rationale  

1. First round: we cooperate (C).  
2. At any round t<r, if everyone cooperated in t−1, we cooperate again.  
3. If at least one player defected in the immediately preceding round, we defect exactly once in t (PunishRoundsRemaining=1), then resume cooperation.  
4. We keep a flag EverDefected so that, in the very last round, if no one has ever defected we “reward” the group by cooperating; otherwise we defect in round r to avoid being exploited.  

Key properties  
• Mutual cooperation is stable: if all start with C and none ever mistakes, the pool stays at capacity each round and every round’s payoff is capacity/(2n).  
• Any defection is immediately punished one round later—but only for one round—so we are forgiving.  
• The one‐round punishment is enough to deter a single defector: a defection in t gives you S_t/n instead of S_t/(2n) immediately but costs you a lost cooperation payoff next round.  
• By resuming cooperation immediately, we avoid driving the stock to collapse under protracted punishment.  
• In the last round we still cooperate if we’ve maintained perfect cooperation so far, giving full benefit to all cooperators.  

Pseudocode recap  

  initialize PunishRoundsRemaining←0, EverDefected←false  
  for t in 1…r do  
    if t>1 and (∃j: a_{t−1}^j = D) then EverDefected←true  
    if PunishRoundsRemaining>0 then  
      action←D  
      PunishRoundsRemaining←PunishRoundsRemaining−1  
    else if t=r then  
      action← (EverDefected? D : C)  
    else if t=1 then  
      action←C  
    else if (∃j: a_{t−1}^j = D) then  
      PunishRoundsRemaining←1  
      action←D  
    else  
      action←C  
    end if  
    play action  
  end for  

This strategy is simple, cooperative, defensible against free‐riders, and forgiving enough to keep the resource at full capacity indefinitely under mutual cooperation.
'''

description_COOPERATIVE_66 = '''
Below is a simple, fully‐specified “cooperative” strategy based on a group version of tit-for-tat with one‐round punishment and guaranteed defection in the very last round.  It satisfies all of your requirements:

1. Decision rules (when to C vs D)  
2. Handles first round, last round, and punishments cleanly  
3. Is as cooperative as possible while still disciplining defectors  

— — —  
STRATEGY: Group Tit-for-Tat with Limited Punishment  

State variables you maintain during play:  
• defectionByOthers[t] ∈ {true,false} for t=1…r, where  
  defectionByOthers[t] = true if in round t at least one opponent j≠i played D.  
  (At t=1 you can initialize defectionByOthers[0]=false.)  

PIECES:  
– First round (t=1): C  
– Last round (t=r): D  (standard last‐round defection)  
– Intermediate rounds (1 < t < r):  
    • If defectionByOthers[t–1] == true, play D this round (punish once)  
    • Otherwise play C  

Pseudocode for player i:  
--------------------------------  
Initialize:  
  defectionByOthers[0] := false  

For each round t = 1 … r do  
  if t == 1 then  
    a_i := C  
  else if t == r then  
    a_i := D  
  else /* 1 < t < r */  
    if defectionByOthers[t–1] == true then  
      a_i := D         # punish any defector once  
    else  
      a_i := C         # continue cooperating  
    end if  
  end if  

  Execute action a_i simultaneously with opponents.  

  // Observe opponents’ actions and record if any defected  
  defectionByOthers[t] := (∃ j≠i : a_j == D)  
end for  
--------------------------------  

Explanation of key points:

•  “Cooperation” means  C = consume S/(2n), which preserves the stock growth  
•  “Defection” means D = consume S/n, a one‐round stick to anyone who defected in the previous round  
•  You only punish “others’” defections; your own punishment‐round D does not retrigger further punishment  
•  Punishment is limited to exactly one round, then you return to full cooperation as long as no new defection occurs  
•  In the very last round t=r, you defect unconditionally to maximize your final‐round payoff (standard backward‐induction step)  
•  Against fully cooperative opponents you maintain C for all t<r, keeping the stock at capacity each round  
•  If anyone ever deviates, you immediately deter them with a single‐round defect; this creates a credible threat to keep everyone aligned  

This strategy is straightforward, transparent to observers, never “over-punishes,” and ensures that as long as everyone cooperates you sustain the maximum long-run resource level and per-round payoff.
'''

description_COOPERATIVE_67 = '''
Below is a single‐strategy “recipe” you can plug into your agent.  It is explicitly cooperative, punishes defections only briefly, and watches the common‐pool so as not to drive it to collapse.  You can tune the two parameters (forgiveness threshold and low‐stock threshold) to your taste—suggested defaults are shown in square brackets.

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
Strategy name: Resource‐Aware Generous Conditional Cooperation (RAGCC)  

Parameters (choose once at the start of the game):  
•  f ∈ [0,1]  –  forgiveness threshold on fraction of defectors in last round  
     (default f = 0.2)  
•  S_low ∈ [0,capacity]  –  “emergency‐coop” stock threshold  
     (default S_low = capacity/3)  

Internal state variables:  
•  punished_last_round  ∈ {True,False}  –  did I punish in the previous round?  
     (initially False)  

Notation for each round t:  
•  S_t = current common‐pool stock at start of round t  
•  D_{t–1} = set of players who played D in round t–1  
•  d_frac = |D_{t–1}| / n  (fraction of players who defected last round)  

Decision rule for round t (1 ≤ t ≤ r):  
1.  If t == 1:  
      play C  
      punished_last_round ← False  
2.  Else if t == r:  
      play D  
        (no future rounds, defect to maximize one‐shot gain)  
3.  Else if S_t ≤ S_low:  
      play C  
      punished_last_round ← False  
        (if the pool is low, always cooperate to help regeneration)  
4.  Else:  
      compute d_frac = |D_{t–1}| / n  
      If d_frac ≤ f:  
        play C  
        punished_last_round ← False  
      Else:  
        If punished_last_round == False:  
          play D        # deliver one‐round punishment  
          punished_last_round ← True  
        Else:  
          play C        # forgive and return to cooperation  
          punished_last_round ← False  

Explanation of each element:  
•  First round: unconditional cooperation to build trust and common stock.  
•  Last round: defect (standard endgame logic, no future to support).  
•  Low‐stock “emergency” rule: whenever the pool dips below S_low, we cooperate  
   regardless of last‐round defections—this protects long‐term viability.  
•  Forgiving conditional cooperation: we look at how many players defected  
   last round.  If that fraction is at or below f, we keep cooperating.  If more  
   than f defected, we defect exactly once as a “punishment,” then immediately  
   forgive (return to cooperate).  
•  The single‐round punishment/forgive cycle keeps defections rare and quick  
   to reverse, avoiding long chains of mutual defection that would wipe out the pool.  

Pseudocode summary:  
```
Initialize punished_last_round = False
for t in 1..r:
  observe S_t, history of actions in t–1
  if t == 1:
    action = C
    punished_last_round = False
  else if t == r:
    action = D
  else if S_t <= S_low:
    action = C
    punished_last_round = False
  else:
    d_frac = (# defectors in t–1) / n
    if d_frac <= f:
      action = C
      punished_last_round = False
    else:
      if punished_last_round == False:
        action = D
        punished_last_round = True
      else:
        action = C
        punished_last_round = False
  play(action)
```

Why this is cooperative:  
- By default (first round, normal stock levels, and no major defection cluster), you always cooperate—maximizing the chance that the pool regrows.  
- You only defect to deliver a minimal, calibrated signal that “too many players cheated last round.”  
- You punish exactly one round, then forgive, encouraging everyone to return to full cooperation quickly.  
- If the pool actually gets low, you override punishments and cooperate to let it rebound.  
- You only defect in the very last round when there is no future incentive left.  

You can tune f (forgiveness threshold) downward to make the strategy stricter (fewer defections tolerated) or upward to make it more forgiving.  You can also adjust S_low if you want a more conservative or aggressive emergency rule.
'''

description_COOPERATIVE_68 = '''
Below is a fully‐specified “cooperative” strategy that you can enter into your tournament.  It is a straightforward Tit-for-Tat style rule with a one-round punishment and a forced defection in the last round (to guard against end-game free-riding).  It never looks at the numeric stock S—only at opponents’ actions—so it is simple to implement and robust to arbitrary stock dynamics.

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
STRATEGY “Lenient TFT with One-Round Punishment + Terminal Defection”

Parameters you choose before the game:  
  • P = 1   (length of punishment, in rounds)  

State variables (stored between rounds):  
  • punCounter ∈ {0,1,…,P} – how many more rounds I must defect as punishment  
  • lastActions[j] ∈ {C,D} for j=1..n   – the action each player j took in the previous round  

Initialization (before round 1):  
  punCounter ← 0  
  For all j: lastActions[j] ← C   (or undefined—it won’t be used in round 1)

Decision rule (at the beginning of each round t=1..r):  
  if t = r then  
    play D   // final‐round defection  
  else if t = 1 then  
    play C   // always cooperate in round 1  
  else if punCounter > 0 then  
    play D  
    punCounter ← punCounter − 1  
  else if ∃ j≠me such that lastActions[j] = D then  
    // someone defected in the previous round ⇒ punish  
    play D  
    punCounter ← P − 1    // I have just used 1 of the P punishment rounds  
  else  
    play C

After all players’ actions are revealed each round, update:  
  For each j: lastActions[j] ← action played by j  

Explanation of why this is cooperative  
1.  Default is cooperate: in round 1 and whenever no one has defected in the immediately preceding round, it plays C.  
2.  Conditional punishment: if anyone defects in round t–1, it defects in round t (and for up to P total rounds) to make defection unprofitable.  After P rounds of D it “forgives” and cooperates again, so it avoids permanent breakdown.  
3.  Terminal defection: in the last round (t = r), there is no future to incentivize cooperation, so it defects.  This is standard in finitely repeated games.  
4.  No reliance on off‐equilibrium “secret” signals or external coordination—only public history of C/D.  

Pseudocode summary  
```
INPUT: n, r, capacity   // but we do not need capacity or stock in this rule
PARAM: P = 1            // length of punishment

STATE:
  punCounter = 0
  lastActions[1..n] = {C, C, …, C}

FOR t = 1 to r:
  if t == r:
    myAction = D
  else if t == 1:
    myAction = C
  else if punCounter > 0:
    myAction = D
    punCounter -= 1
  else if exists j ≠ me with lastActions[j] == D:
    myAction = D
    punCounter = P - 1
  else:
    myAction = C

  play myAction
  observe actions of all players this round
  for each j in 1..n:
    lastActions[j] = action_j
END FOR
```

Edge cases handled  
- Round 1 has no history ⇒ play C  
- Rounds 2..r–1 follow TFT + one‐round punishment  
- Round r always defects (no future to protect)  
- After a punishment episode of P rounds, forgives even if stock is low  
- Requires no numeric threshold on the stock; purely history‐based  

This strategy achieves maximal mutual cooperation so long as no one defects, deters one‐off deviations with a short punishment, then returns to cooperation, and handles the finite horizon by defecting only when there is no future to safeguard.
'''

description_COOPERATIVE_69 = '''
Below is a single‐strategy description, in “code plus prose” form, that aims to sustain full cooperation (everyone choosing C) for as many rounds as possible, yet is ready to punish any defection briefly and then forgive, so that the pool can recover to capacity.  It also handles the last round explicitly (where standard backward‐induction logic would predict inevitable defection).

––––––––––––––––––––––––––––––––––––––––––  
COOPERATIVE “FORGIVING TRIGGER” STRATEGY  
––––––––––––––––––––––––––––––––––––––––––  

Parameters you choose once, before the match:  
• K  = punishment length (integer ≥ 1). A typical choice is 1 or 2.  
• r  = total rounds (known).  
• capacity, n  (known game parameters).  

State variables (maintained round to round):  
• coop_state ∈ {“ON”, “OFF”}, initially “ON”.  
• punish_counter ∈ {0,1,2,…}, initially 0.  

Decision rule for player i in round t with observed stock S_t and history of actions H_{<t}:  

1. If t = r (the last round) → play D.  
   (No future to punish, so defect for maximum one‐round gain.)  

2. Else if punish_counter > 0 →  
      • play D  
      • punish_counter ← punish_counter − 1  
      • If punish_counter reaches 0, set coop_state ← “ON”  
   (We are in a punishment phase.)  

3. Else (i.e. t < r and punish_counter = 0):  
   a. If coop_state = “OFF”:  
        • This is the first round after punishment ended → set coop_state ← “ON” and play C.  
   b. Else (coop_state = “ON”):  
        • Play C.  
        • After observing everyone’s actions this round, if you detect any defection (any player played D), then immediately set  
            coop_state ← “OFF”  
            punish_counter ← K  

Plain‐English description:  
• Round 1 is treated just like any other non‐last round, so you start by cooperating (C).  
• As long as everyone has cooperated in all past rounds and you are not in a punishment countdown, you continue to cooperate.  
• The moment you see even one D, you switch coop_state to OFF and enter a D‐for‐K‐rounds punishment phase (playing D irrespective of stock).  
• After exactly K rounds of punishment, you “forgive” everyone, return to coop_state = ON and again cooperate, restarting the cycle.  
• In the final round (t = r), you always defect (D) because there is no future to enforce cooperation.  

Why this is cooperative:  
– When no one defects, all players choose C every round except the forced last‐round defection, which preserves the stock at capacity from round 1 through round r−1. That maximizes long‐run payoffs.  
– A short, finite punishment (rather than permanent “grim”) makes defection unprofitable: if someone deviates in round t < r, they give up a stream of high C‐payoffs for K rounds of mutual D, then return to cooperation—so the one‐shot gain from defection is outweighed by the subsequent punishment.  
– Forgiveness lets the pool recover to full capacity quickly (since all‐D for K< r rounds will generally leave some stock and then regrowth restores it), enabling the group to resume surplus‐maximizing cooperation.  
– Explicit last‐round defection is standard in finite games and does not undermine cooperation in earlier rounds, because all players know and expect it.  

Pseudocode summary:  

```
Initialize:
  coop_state ← “ON”
  punish_counter ← 0

for t in 1..r do
  if t == r then
    play D
    continue to next t
  end if

  if punish_counter > 0 then
    play D
    punish_counter ← punish_counter − 1
    if punish_counter == 0 then
      coop_state ← “ON”
    end if
  else
    if coop_state == “OFF” then
      # First round after punishment
      coop_state ← “ON”
      play C
    else
      # Normal cooperative phase
      play C
      # After observing others:
      if any opponent played D this round then
        coop_state ← “OFF”
        punish_counter ← K
      end if
    end if
  end if
end for
```

Choose K (e.g. 1 or 2) to ensure the expected future loss from punishment exceeds the one‐round gain from defection. This strategy is simple, credible, discourages free-riding, yet is forgiving enough to restore the resource and resume cooperation quickly.
'''

description_COOPERATIVE_70 = '''
Below is a single‐strategy specification—let’s call it “Tit-for-Tat with End-Game Defection”—that (1) starts out fully cooperative, (2) punishes any defection just long enough to deter repeats, (3) forgives to restore full cooperation, and (4) takes into account the known finite horizon by defecting in the very last round.

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
1.  Key ideas  
   • Cooperate means choose C (take S/(2n)); defect means D (take S/n).  
   • Start by cooperating to build trust.  
   • If anybody defects in round t–1, punish in round t by defecting.  
   • After one punishment round, forgive and return to cooperation—so cooperation can be restored.  
   • In the final round r, defect regardless (no future to protect).  

2.  Decision rules (informal)  
   Round 1: play C.  
   For each round t = 2 … r–1:  
     – If any player chose D in round t–1, play D this round.  
     – Otherwise, play C.  
   Round r (last round): play D.  

3.  Handling edge cases  
   – “First round” (t=1): No history ⇒ cooperate.  
   – “Last round” (t=r): defect (myopic gain; no future punishment possible).  
   – “Isolated defection”: We punish exactly one round per defection event, then return to full cooperation.  
   – “Multiple defections” in round t–1: still punish one round only (we don’t escalate), then forgive.  

4.  Pseudocode  
```  
Input: n, r, capacity  
History H = empty list of length r;  // will store each round’s action profile  

For t in 1…r do  
  if t == 1 then  
    action_i ← C  
  else if t == r then  
    action_i ← D         // last‐round defection  
  else  
    // Look at last round’s actions  
    let last_profile = H[t-1]  
    if ∃ j in {1…n} such that last_profile[j] == D then  
      action_i ← D       // punish once  
    else  
      action_i ← C       // full cooperation  

  // Play action  
  Submit action_i  
  Observe other players’ actions; record profile H[t]  
End for  
```  

5.  Why this is cooperative  
   – As long as all players follow it, every round t<r all will choose C ⇒ stock regenerates to capacity ⇒ each earns capacity/(2n) every round ⇒ total payoff = r·capacity/(2n).  
   – A one‐shot defection by any player in round t yields them extra payoff that round (S/n vs. S/2n), but causes us (and everyone) to defect in t+1, which immediately lowers that defector’s future earning.  
   – Because punishment is only one round, the “cost” of punishment is minimal to cooperators while still deterring repeat defectors.  
   – Forgiving restores the high‐payoff cooperative path quickly.  
   – Final‐round defection extracts the last possible surplus when no future payoff is at stake—this is standard in finitely repeated games.  

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
This strategy (a variant of tit-for-tat with limited punishment and end‐game defection) is easy to implement, transparent to opponents, and enforces mutual cooperation for all but the known final round.
'''

description_COOPERATIVE_71 = '''
Below is a single‐strategy recipe—“Forgiving Trigger with Last‐Round Defection”—that (1) sustains full cooperation almost all the way through, (2) punishes any defection briefly, (3) forgives quickly, and (4) defects in the known last round when no future reward is possible.

───────────────────────────────────  
Parameters  
  n         = number of players  
  r         = total rounds  
  capacity  = maximum stock (initial S₁ = capacity)  
  K_punish  = 1  (length of punishment in rounds; you can set 1 or 2)  

State variables (kept by our agent)  
  last_stock    ← capacity  
  punish_timer  ← 0    (counts down remaining punishment rounds)  

───────────────────────────────────  
Protocol  

Round 1:  
  play C  
  observe stock S₂ at end of round, set last_stock ← S₂  

For each round t = 2 … r do  
  if t = r then  
    ■ Last round: play D (no future to enforce cooperation)  
  else if punish_timer > 0 then  
    ■ We are in a punishment phase:  
    play D  
    punish_timer ← punish_timer − 1  
  else  
    ■ Normal “cooperate‐unless‐someone‐just‐defected” mode  
    let Δ = last_stock − S_t  ■ how much the pool dropped this round  
    let C_total = n * (last_stock/(2n)) = last_stock/2  
       ■ total consumption if everyone had cooperated  
    if Δ > C_total + ε then  
      ■ someone must have defected (consumed more than C_total)  
      punish_timer ← K_punish  
      play D  
    else  
      play C  
    end if  
  end if  

  observe new stock S_{t+1}, set last_stock ← S_{t+1}  
end for  

───────────────────────────────────  
Explanation of the pieces  

1. Cooperate by default (C), which at stock S yields each player S/(2n) and regenerates the pool back to capacity.  
2. Defection detection: if total depletion Δ exceeds what full cooperation would do (i.e. last_stock/2), we conclude “at least one player defected.”  
3. Punishment: upon detection, we defect for K_punish rounds (here K_punish=1), denying the defector its cooperative future payoff.  
4. Forgiveness: once punishment rounds elapse, we resume cooperation. This prevents an endless collapse of the resource.  
5. Last round special case: we defect in round r because no future remains to discipline deviations.  

───────────────────────────────────  
Why it’s cooperative  
- If everyone follows the above, all but the final round are C, so the stock stays at capacity each round, and each gets capacity/(2n).  
- Any single defection in round t immediately earns the defector a higher payoff S_t/n, but in round t+1 we all defect once, so the defecting player loses its future share S_{t+1}/(2n).  
- Since K_punish can be tuned, the one‐round penalty is just enough to deter unilateral deviation (given sufficient weight on future payoffs) yet not so long that the pool spirals downward.  
- Because we forgive after K_punish rounds, cooperation can be restored quickly and the capacity buffer is rebuilt.  

Edge‐case handling  
- First round: unconditionally cooperate—no history to trigger punishment.  
- Last round (t=r): defect, as there is no more future to enforce.  
- If multiple defections occur in a row, punish_timer stacks to at most K_punish, so we never over‐punish.  

This strategy is simple to code, transparent to human or LLM opponents, and—against a field of conditional cooperators—will keep the common pool at its maximum almost until the final showdown.
'''

description_COOPERATIVE_72 = '''
Below is a simple “cooperative trigger‐and‐forgive’’ strategy for the n‐player common‐pool game.  It generalizes Tit-for-Tat: you start by cooperating, you punish any defection by defecting exactly one round, then you immediately return to cooperation so long as others do.  This strategy has three features:  

 1. First‐round goodwill  
 2. One‐round punishment of any defector  
 3. Immediate forgiveness (you go back to cooperating so long as everyone cooperates)  

Because it never punishes longer than one round, it keeps the door open to full cooperation and sustains the stock at capacity if all players follow it.

—–  
STRATEGY DESCRIPTION  
—–  
State variable:  
punish_flag ∈ {0,1}, initially 0.  
punish_flag=1 means “I am punishing this round”  

Each round t, you observe the full action profile of round t–1 (except in t=1).  Let DefectedLast = true if in t–1 at least one player played D, and false otherwise.

Decision rule for round t:

1.  If t = 1:  
    – punish_flag ← 0  
    – play C  

2.  Else (t > 1):  
    a.  If punish_flag = 1 then  
         • play D  
         • punish_flag ← 0      (you punish exactly one round)  
    b.  Else if DefectedLast = true then  
         • play D              (start one‐round punishment)  
         • punish_flag ← 1  
    c.  Else  
         • play C              (no one defected last round)  

That’s it.  No special hard‐coded “always defect in last round” is needed; you simply follow the same rule every round.  When everyone follows this, the stock remains at capacity and each player repeatedly cooperates.

—–  
PSEUDOCODE  
—–  
Inputs (common knowledge): n, r, capacity  
Local state for each player i: punish_flag ← 0  

for t in 1…r do  
  if t == 1 then  
    action_i[t] ← C  
    punish_flag ← 0  
  else  
    # Detect whether anyone defected in the previous round  
    DefectedLast ← (∃ j in {1..n} s.t. action_j[t-1] == D)  

    if punish_flag == 1 then  
      action_i[t] ← D  
      punish_flag ← 0  
    else if DefectedLast then  
      action_i[t] ← D  
      punish_flag ← 1  
    else  
      action_i[t] ← C  
    end if  
  end if  
end for  

—–  
WHY IT’S COOPERATIVE  
—–  
• By cooperating in round 1 you signal goodwill.  
• You only ever punish a defection for one round—no permanent vendettas—so cooperation can re‐emerge.  
• If all players follow this, every round sees zero defections ⇒ stock stays at capacity ⇒ each round each player earns capacity⁄(2n).  

Even if some players experiment with D, they get defected against exactly one round and then forgiveness returns you all to the high‐payoff cooperative path.  This simple reciprocity rule is well‐known to stabilize cooperation in finitely repeated settings—its single‐round punishment is just enough to deter casual free‐riding but not so harsh as to collapse back into mutual defection forever.
'''

description_COOPERATIVE_73 = '''
Below is a single‐player decision rule (“your” strategy) that (a) tries to keep the stock at sustainable levels by cooperating, (b) punishes any defection quickly and then forgives, and (c) never lets a punishment drive the stock below a safe emergency threshold.  It also handles the first and last rounds explicitly.  

––––––––––––––––––––––––––––––––––––––––––––  
Strategy name  
“Sustainable Multi‐Player Tit-for-Tat with One-Round Punishment”  

Parameters you choose once, given n and capacity:  
• punish_duration = 1  // length of the punishment phase  
• low_stock_threshold = 2·capacity/n  
  // if stock ever falls below this, we switch to full cooperation to let it recover  

State variables (initialize before round 1):  
• punish_rounds ← 0  

Each round t = 1…r, observe: current stock S_t, history of all players’ actions.  Then decide your action a_i,t ∈ {C,D} as follows:  

1.  First‐round rule  
    If t = 1 then  
       a_i,t ← C  
       (seed cooperation)  
       Stop.  

2.  Emergency‐cooperate rule  
    If S_t < low_stock_threshold then  
       a_i,t ← C  
       punish_rounds ← 0  
       Stop.  
    (This avoids driving the stock to zero during punishment.)  

3.  Last‐round rule  
    If t = r then  
       a_i,t ← D  
       Stop.  
    (No future to protect, so maximize final‐round payoff.)  

4.  Punishment phase  
    If punish_rounds > 0 then  
       a_i,t ← D  
       punish_rounds ← punish_rounds – 1  
       Stop.  

5.  Triggering punishment  
    Look at round t–1: if ∃ j ≠ i with a_j,t–1 = D then  
       punish_rounds ← punish_duration  
       a_i,t ← D  
       Stop.  

6.  Otherwise—full cooperation  
    a_i,t ← C  

––––––––––––––––––––––––––––––––––––––––––––  
Pseudocode  

```
initialize:
  punish_rounds ← 0

for t in 1…r:
  observe current stock S_t
  observe last round’s actions {a_j,t–1}

  if t == 1:
    action ← C
    continue to next t

  if S_t < 2*capacity/n:
    action ← C
    punish_rounds ← 0
    continue

  if t == r:
    action ← D
    continue

  if punish_rounds > 0:
    action ← D
    punish_rounds ← punish_rounds – 1
    continue

  if ∃ j ≠ i such that a_j,t–1 == D:
    punish_rounds ← 1         # one‐round punishment
    action ← D
    continue

  # no recent defections, stock is healthy
  action ← C
```

––––––––––––––––––––––––––––––––––––––––––––  
Why this is cooperative  
1.  It always “starts nice” (C in round 1).  
2.  So long as everyone continues to cooperate, it keeps cooperating and the stock regenerates to capacity.  
3.  A single defection by any player is punished by exactly one round of defection, then full forgiveness—so defection is discouraged but cooperation can resume.  
4.  It protects the resource in “punishment” phases by switching off punishment if the stock ever dips below a safe threshold.  
5.  By defecting in the very last round it avoids being exploited, yet by cooperating in every other round it maximizes group payoffs and thus your own total payoff in the long run.  

This combination of simple reciprocity, limited punishment, forgiveness, and resource‐sensitive emergency cooperation makes it both robust against free‐riders and genuinely cooperative.
'''

description_COOPERATIVE_74 = '''
Below is a simple “generous tit-for-tat with endgame” strategy.  Its goal is to sustain cooperation (keep the stock near capacity) by (1) always cooperating so long as nobody has just defected, (2) punishing any defection for a short fixed number of rounds, (3) forgiving afterward, and (4) defecting in the final round because there is no future to protect.

1.  State variables  
    •  punish_rounds ∈ {0,1,2,…}: number of rounds left to punish.  Initialize punish_rounds ← 0.

2.  Decision rule for round t=1…r  
    if t == 1 then  
      play C  
    else if t == r then  
      play D   // final­-round defection (no future to protect)  
    else if punish_rounds > 0 then  
      play D  
      punish_rounds ← punish_rounds − 1  
    else  
      play C  

3.  Update after observing last round’s actions  
    Let OppDefected = true if any opponent played D in the just-completed round, false otherwise.  
    If OppDefected then  
      punish_rounds ← min(2, r − t)   // punish at most 2 rounds, but don’t overflow beyond final round

4.  Intuition and remarks  
  •  “Always C if nobody defected last round” stabilizes full cooperation at S ≈ capacity.  
  •  A 1–2 round punishment of D deters unilateral defections.  
  •  Forgiveness (returning to C after punish_rounds run out) allows the group to re-build the stock.  
  •  Defecting in the very last round is standard endgame play (no future rounds to punish).  
  •  No extra parameters or assumptions about opponent types are used—only publicly observed actions and the known round count.  

Pseudocode  

```
Initialize: punish_rounds ← 0

for t in 1…r do
  if t == 1 then
    action_t ← C
  else if t == r then
    action_t ← D
  else if punish_rounds > 0 then
    action_t ← D
    punish_rounds ← punish_rounds − 1
  else
    action_t ← C
  end if

  // play action_t simultaneously with others, observe their actions
  observe opponents’ actions in round t
  if any opponent played D then
    // schedule punishment, but don’t extend past round r
    punish_rounds ← min(2, r − t)
  end if
end for
```

This strategy is cooperative—under mutual cooperation it keeps the stock at capacity—yet it punishes free-riding quickly and then returns to cooperation, and it defects in the final round where no further stock‐preserving incentives exist.
'''

description_COOPERATIVE_75 = '''
Below is a self-contained “cooperative” strategy for the n-player common-pool game.  It is in the spirit of Tit-for-Tat (TFT) extended to n players, with (a) an initial cooperative move, (b) one-round punishment of any defection, (c) automatic return to cooperation after punishment, and (d) a last-round defection to protect against end-game exploitation.  This rule set is easy to implement, transparent to opponents, and—among non-communicating agents—tends to sustain high levels of cooperation and stock regeneration.

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––
1.  OVERVIEW  
––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––
We maintain a single Boolean flag “punish” that tells us whether last round we saw any defection.  On each round t:

  • If t = 1  (first round)  
      → play C.  
  • Else if t = r  (last round)  
      → play D.  
  • Else if punish = false  (no defection observed last round)  
      → play C.  
  • Else (punish = true)  
      → play D for exactly one round, then reset punish = false next round.

After all players’ actions are revealed, we set  
  punish ← true  if (any player chose D this round),  
  otherwise punish ← false.  

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––
2.  DECISION RULES (PSEUDOCODE)  
––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––
Parameters known to all agents:  
  n  (number of players),  
  r  (total rounds).

State variable (for our strategy):  
  punish  ∈ {false, true}, initially false.

Begin game:
  punish ← false

For each round t = 1,2,…,r do:

  if t = 1 then
     action ← C
  else if t = r then
     action ← D
  else if punish = false then
     action ← C
  else   // punish = true
     action ← D

  submit action to the game

  // Wait for the round to resolve and observe all n actions
  observe A_1,…,A_n ∈ {C,D}

  // Update punish‐flag for next round
  if (∃ i ∈ {1..n} such that A_i = D) then
    punish ← true
  else
    punish ← false
  end if

end for

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––
3.  EXPLANATION & COOPERATIVE SPIRIT  
––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––

1.  “Always Cooperate on First Move.”  
    This signals a friendly posture and helps the common pool stock bounce back toward capacity early on.

2.  “Tit-for-Tat Punishment.”  
    If any player defects in round t, we defect in round t+1.  This one‐round of defection is a calibrated punishment: it hurts defectors, but only for one round, and then we forgive.  Short punishments keep long-run cooperation viable.

3.  “Automatic Forgiveness.”  
    By resetting punish to false whenever the previous round was all‐C, we swiftly return to cooperation.  This prevents vicious cycles of mutual retaliation.

4.  “Last-Round Defection.”  
    Because there is no future punishment after round r, a lone defection in r cannot be deterred.  By defecting ourselves in the final round, we protect our own one‐shot payoff and prevent being exploited.

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––
4.  HANDLING EDGE CASES  
––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––

•  Round 1:  We have no history, so we cooperate to “test the waters.”  
•  Rounds 2..r–1:  Follow TFT‐style: cooperate unless last round saw a defection.  
•  Round r:  Defect, since there is no scope for future reward or punishment beyond this point.  
•  Stock = 0:  Technically everyone’s future payoffs are zero.  Our rule still prescribes D if punishing or if it’s round r, and C otherwise.  Since the pool is empty, payoff differences vanish.  
•  n = 2 or larger:  The same logic scales—“any defection” means “at least one of the n players played D.”  

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––
5.  WHY THIS IS COOPERATIVE  
––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––

–  It invests early in the common resource (round 1), fostering full‐stock regrowth.  
–  It punishes cheaters just enough to deter defection but quickly returns to cooperation.  
–  It is transparent and reciprocal: opponents can predict that mutual cooperation yields the highest sustained payoffs.  
–  While it concedes the last‐round “one‐shot” logic, it maximizes total payoffs across rounds 1..r–1 by maintaining cooperation there.  

In tournaments among bounded–rational or reciprocity-minded agents, this strategy typically achieves near-Pareto-optimal outcomes on all but the final round, thereby demonstrating a clear cooperative mindset.
'''

description_COOPERATIVE_76 = '''
Below is a single‐player decision rule (“policy”) that seeks to sustain full cooperation on the common‐pool resource, yet punishes defections briefly and handles the known finite horizon.  It is a variant of tit-for-tat with one‐round punishment, a small “forgiveness” window, and a final‐round defection.

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
1.  State data you keep  
    • last_round_defected_flag (Boolean)  
      – true if in the immediately preceding round at least one opponent chose D; false otherwise.  
    • punish_rounds_remaining (integer ≥ 0)  
      – how many rounds of mandatory punishment (D) remain; initialized to 0.  

2.  Parameters you choose  
    • P = 1  (punishment length: punish for 1 round after any defection)  
    • S_low_frac = 0.5  (if stock ever falls below this fraction of capacity, rebuild by cooperating)  

3.  Decision rule each round t = 1,…,r  

   Observe at start of round t:  
     • current stock S_t  
     • last_round_defected_flag  
     • punish_rounds_remaining  

   Then choose action A_t ∈ {C, D} as follows:  

   If t == 1 then  
     A_t ← C  
     // always open with cooperation  

   Else if punish_rounds_remaining > 0 then  
     A_t ← D  
     punish_rounds_remaining ← punish_rounds_remaining − 1  
     // carry out the remainder of the punishment  

   Else if t == r then  
     A_t ← D  
     // Last round: defect (end‐game incentive)  

   Else if S_t < S_low_frac × capacity then  
     A_t ← C  
     // If stock is dangerously low, all cooperate to rebuild  

   Else if last_round_defected_flag == true then  
     A_t ← D  
     punish_rounds_remaining ← P − 1  
     // A defection was observed last round → punish this round (and set up any further punishment)  

   Else  
     A_t ← C  
     // No punishment called for, stock healthy, continue cooperating  

   End if  

   After actions are realized this round, update for next round:  
     last_round_defected_flag ← (∃ j≠i : opponent j chose D in round t)  

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  

Explanation of key points  
1.  “Start with C.”  By cooperating in round 1 you signal willingness.  
2.  “One‐round punishment.”  If anyone defects, you defect exactly one full round.  This punishes the violator while minimizing collateral damage and allows rapid return to cooperation.  
3.  “Rebuild when stock is low.”  If the common stock ever falls below half capacity, you unconditionally cooperate (even if you are in the middle of a punishment phase or just saw a defection), to help the pool recover.  
4.  “Last‐round defection.”  In round r you defect because there is no future to punish or reward.  This is standard in finite‐horizon repeated games.  

Why this is cooperative  
– You only defect in direct response to observed defection (tit‐for‐tat style), and then immediately forgive.  
– You cooperate whenever your punishment obligation is over and the stock is healthy, so the pool regenerates and everyone can earn the higher cooperative payoff S/(2n).  
– You never carry an endless “grim” trigger—punishment is brief and forgiving—so groups of cooperators self‐sustain.  
– You add a safety valve: if stock falls too low, you unconditionally cooperate to help bring it back up.

This strategy does not rely on private signals, side‐payments, or hidden coordination.  It uses only the public history of defections and the publicly observable stock level, and it conforms to the no‐communication, perfect‐information framework.
'''

description_COOPERATIVE_77 = '''
Below is a simple “conditional‐cooperation” rule that (1) supports the all-C path, (2) punishes any one–shot defector, (3) forgives immediately if no fresh defection occurs, and (4) handles the first and last rounds.

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
Strategy name: Tit-for-Tat Common-Pool (TfT-CP)

Parameters to pick in advance:  
• r = total number of rounds  
• n = number of players  

State you track:  
• lastDefectionOccurred ← false    (whether any player defected in the immediately preceding round)

Decision rule for round t = 1,…,r:

1.  INITIALIZATION (before t=1):  
    lastDefectionOccurred ← false

2.  AT THE START OF ROUND t:  
    if t == 1 then  
       play C  
       goto step 4  
    end if

    if t == r then  
       play D      // standard end-game defection  
       goto step 4  
    end if

3.  FOR 1 < t < r:  
    if lastDefectionOccurred == false then  
       play C      // keep cooperating  
    else  
       play D      // punish by defecting this round  
    end if

4.  AFTER ALL ACTIONS ARE REVEALED IN ROUND t:  
    // Observe everyone’s actions in this round  
    if ∃ j ∈ {1…n} such that player j played D in round t then  
       lastDefectionOccurred ← true  
    else  
       lastDefectionOccurred ← false  
    end if  

5.  Proceed to t+1 (if any).

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  

Explanation of why this is cooperative:

1.  First round cooperation seeds the high-stock equilibrium.  
2.  As long as nobody defects, you continue to play C each round—so under mutual cooperation the stock remains at capacity forever.  
3.  The moment you see even a single D, you retaliate with D exactly once.  That single defection cuts the deviator’s future gains more than your one–shot loss, if the discount factor (or continuation value) is sufficiently high.  
4.  You then forgive immediately: if nobody defects in the retaliation round, you drop punishment and resume C.  
5.  In the very last round you “defect for sure,” because no future punishment is possible (standard backward-induction endgame choice).

Edge-cases:

•  Round 1: unconditionally C.  
•  Round r: unconditionally D (no hope of future enforcement).  
•  A defection in round r−1 still triggers exactly one round of punishment in round r (which is your scheduled D anyway).  
•  Any defection in round k > 1 is punished exactly in round k+1 only.  

This is a classic “tit-for-tat” style adapted to the common-pool setting.  It enforces the all-C path as a self-sustaining equilibrium (by threat of one-period punishment) while immediately rewarding any return to full cooperation.
'''

description_COOPERATIVE_78 = '''
Below is a simple “generous tit‐for‐tat with end‐game” strategy.  It (1) starts by cooperating, (2) punishes any defection by defecting exactly one round, (3) then forgives, and (4) defects in the final round because no future remains to enforce cooperation.

—Decision rules—  
Let r be total rounds, t the current round (1 ≤ t ≤ r).  Maintain one internal variable: punish_counter (initially 0).

At the start of each round t, observe last round’s actions of all opponents (for t=1 there is no history).  Then choose:

1. if t = r  (the last round):  
     play D  
2. else if punish_counter > 0:  
     play D  
     punish_counter ← punish_counter – 1  
3. else if in round t–1 at least one opponent played D:  
     play D  
     punish_counter ← 1      // punish exactly one additional round  
4. else:  
     play C  

—Why this is cooperative—  
• By starting with C and returning to C immediately after a one‐round punishment, it encourages mutual cooperation whenever possible.  
• Any defection is met with a brief, proportional retaliation, which deters sustained free‐riding.  
• Forgiving after a single‐round punishment avoids endless vendettas, keeping the pool healthy.  
• Defecting on the very last round is standard “backward induction” and does not undermine earlier cooperation.

—Pseudocode—  
```
initialize punish_counter ← 0

for t in 1…r:
    observe last_actions[1…n]     # includes your own last action
    if t == r:
        play D
    else if punish_counter > 0:
        play D
        punish_counter ← punish_counter – 1
    else if exists j≠you such that last_actions[j] == D:
        play D
        punish_counter ← 1
    else:
        play C
end for
```

—Edge Cases—  
• t=1: no history ⇒ punish_counter=0, so rule #4 applies ⇒ C.  
• Immediately after any defection you defect the next round only, then revert to cooperation.  
• In round r you always defect (no future to enforce cooperation).  
• If the stock ever falls to zero, both C and D yield zero reward; you still follow the same rule (it costs nothing extra to “defect” when stock=0).

This strategy is simple to implement, clearly cooperative (it only punishes to enforce cooperation, then forgives), and reputable in tournaments of repeated social-dilemma games.
'''

description_COOPERATIVE_79 = '''
Below is a single‐strategy “forged” to sustain mutual cooperation on the Common‐Pool Resource Game yet still defend against free‐riders.  It is a variant of Tit-for-Tat with finite punishment and end-game reasoning.  

1.  Informal Description  
   • Start by cooperating.  
   • As long as nobody has defected in the immediately preceding round, continue to cooperate.  
   • The first time any opponent defects, enter a short punishment phase of D for the next two rounds, then forgive and return to cooperation.  
   • In the very last round, defect (standard end-game reasoning).  

   Rationale:  
   – By always cooperating unless provoked, you maximize the chance of sustaining the stock at capacity and each round’s high per-capita payoff capacity/(2n).  
   – The brief, finite punishment deters would-be defectors but does not collapse cooperation forever.  
   – Defecting in round r (no future) is a best response in the last round.  

2.  Edge Cases  
   • First round (t = 1): no history → cooperate.  
   • Last round (t = r): defect, regardless of history.  
   • When your punishment countdown would extend past r, you simply defect up to round r.  

3.  Pseudocode (for player i)  
```
Inputs:
  r        ← total number of rounds
  history  ← list of past profiles a₁, a₂, …, a_{t-1}  
State variables (initialized once):
  punish_left ← 0   # how many more rounds we must defect as punishment

For each round t = 1,2,…,r do:
  if t == 1 then
    action_i ← C
  else if t == r then
    # End-game: no future to protect
    action_i ← D
  else if punish_left > 0 then
    # We are in punishment phase
    action_i ← D
    punish_left ← punish_left – 1
  else
    # Check if any opponent defected last round
    let last_profile = history[t-1]
    if ∃ j ≠ i such that last_profile[j] == D then
      # trigger a 2-round punishment (one this round, one next)
      action_i ← D
      punish_left ← 1
    else
      # Everyone was cooperative in t–1 → cooperate
      action_i ← C
    end if
  end if

  # Play action_i, observe profile, append to history, continue
end for
```

4.  Why This Is Cooperative  
   – “Nice”: It never defects first; it only punishes in response to observed defections.  
   – “Forgiving”: Punishment lasts only two rounds, so one noisy defection does not lead to perpetual collapse.  
   – “Clear”: Opponents immediately see cause and effect—defect once, lose cooperation for two periods, then get full returns back.  
   – “Enforceable”: The threat of short punishment is enough to make a single‐round defection unprofitable when the full stream of future payoffs is taken into account.  

This strategy balances the high long-run gains of mutual C against the temptation to D, while guarding itself against exploitation.
'''

description_COOPERATIVE_80 = '''
Below is a “conditional‐cooperation with finite punishment” strategy.  It aims to keep the common stock near capacity by cooperating as long as everyone else does, punishing defections long enough to deter them, then forgiving and returning to full cooperation.  

––––––––––––––––––––––––––––––––––––––––––––––––––––  
1.  Main idea  
   •  Start by cooperating.  
   •  If you ever observe a defection, defect for a fixed number of rounds (punishment), then go back to cooperating.  
   •  Always defect in the very last round (no future to protect).  

2.  Parameters  
   Let  
     n = # players  
     r = total rounds  
     capacity = resource cap  
   Choose a small “punishment length” k ≥ 1 (e.g. 2 or 3).  

3.  State variables  
   – punishing: Boolean, initially false  
   – remaining_punish: integer ≥ 0, initially 0  

4.  Notation  
   – t ∈ {1,…,r}: current round  
   – History up to t–1: the vector of actions each player took in each prior round  
   – “Defected last round”: at least one player’s action was D in round t–1  

––––––––––––––––––––––––––––––––––––––––––––––––––––  
4.  Decision rules (pseudo‐code)  

Initialize:  
  punishing ← false  
  remaining_punish ← 0  

For each round t=1,…,r do:  
  
  if t == 1 then  
    action ← C                      # Start cooperatively  
  
  else if t == r then  
    action ← D                      # Last round: defect for immediate gain  
  
  else if punishing then            # We are in a punishment phase  
    action ← D  
    remaining_punish ← remaining_punish − 1  
    if remaining_punish == 0 then  
      punishing ← false  
  
  else if (any player played D in round t−1) then  
    # Trigger a new punishment phase  
    punishing ← true  
    remaining_punish ← min(k, r − t)  
    action ← D  
  
  else  
    action ← C                      # No defection seen, keep cooperating  
  end if  

  Play(action)  
end for  

––––––––––––––––––––––––––––––––––––––––––––––––––––  
5.  Why this is cooperative  
  •  As long as everyone plays C, you always play C, keeping the stock high.  
  •  A single defection by anyone triggers just‐enough group punishment to make defection unattractive.  
  •  After punishment you forgive and return to cooperation, restoring trust.  
  •  Defecting in the very last round captures the one‐shot gain when no future is at stake.  

––––––––––––––––––––––––––––––––––––––––––––––––––––  
6.  Edge cases  
  – First round: cooperate by default.  
  – Last round: defect (no future payoffs to protect).  
  – If punishment would run past round r, we cap it so we never punish “beyond” the final round.  
  – If multiple defections happen in quick succession, you simply reset/extend the punishment window (but always short and capped at k).  

––––––––––––––––––––––––––––––––––––––––––––––––––––  
This strategy is fully autonomous (no signaling needed), easy to implement, clearly cooperative, yet enforces the threat of group punishment to sustain cooperation over the repeated interaction.
'''

description_COOPERATIVE_81 = '''
Below is a single‐strategy “Tit-for-Tat with Forgiveness” tailored to this CPR game.  It (a) starts by cooperating, (b) punishes one round of defection by any player, (c) then forgives and returns to cooperation, and (d) defects in the last round.  This simple rule set is known to sustain high cooperation in tournaments of strategies with no side– communication.

1.  Key ideas  
   •  Cooperate whenever everyone has been “good” recently.  
   •  If you detect any defection in the immediately preceding round, defect once in retaliation.  
   •  After that one–round punishment, forgive and go back to cooperate—unless you are in the last round, where you defect.  

2.  Definitions & detection  
   Let Sₜ = common stock at the start of round t, before any consumption.  
   We say “player j defected in round t” if j’s consumption xⱼ,ₜ > Sₜ/(2n).  
   (Equivalently, j chose D rather than C in round t.)

3.  Strategy description  
   Maintain a single integer state variable punish ← 0.

   For each round t = 1,2,…,r do:  
     if t = r then  
       •  Action ← D  
     else if t = 1 then  
       •  Action ← C       // first‐round cooperation  
     else if punish > 0 then  
       •  Action ← D       // under punishment  
       •  punish ← punish − 1  
     else  
       // no active punishment, not final round  
       if any opponent defected in round t–1 then  
         punish ← 1        // schedule a one‐round retaliation  
         Action ← D        // immediately punish this round  
       else  
         Action ← C        // everybody was good last round  
       end  
     end  

4.  Pseudocode  

   initialize punish ← 0  

   for t in 1..r do  
     observe Sₜ  
     if t = r then  
       aₜ ← D  
     else if t = 1 then  
       aₜ ← C  
     else if punish > 0 then  
       aₜ ← D  
       punish ← punish − 1  
     else  
       // detect defection in t−1  
       let def ← FALSE  
       for each player j ≠ you do  
         if consumptionⱼ,ₜ₋₁ > Sₜ₋₁/(2n) then  
           def ← TRUE  
         end  
       end  
       if def then  
         punish ← 1  
         aₜ ← D  
       else  
         aₜ ← C  
       end  
     end  
     play aₜ  
     observe all consumptions and update stock to compute next Sₜ₊₁  
   end  

5.  Why it’s cooperative  
   •  It always starts in full cooperation (all C).  
   •  It only uses minimal punishment (one round) to deter defection.  
   •  After punishing exactly once, it immediately returns to cooperation—so a single mistake or exploratory defection is not met with endless “grim” punishment.  
   •  This rule set typically sustains mutual cooperation, because if everyone is using the same strategy, any one defection provokes a one‐round sanction and then full cooperation resumes, keeping the resource near capacity and payoffs high.  

6.  Edge cases  
   –  First round t=1: unconditional cooperate to build goodwill.  
   –  Last round t=r: unconditional defect (standard backward‐induction endgame).  
   –  If the pool ever hits zero (Sₜ=0): growth is zero and payoffs from C or D are both zero, but the above rules continue—retaliation or forgiveness make no payoff difference once stock is gone.  

This “Tit-for-Tat with Forgiveness” balances deterrence (punishing defectors) with generosity (rapid return to cooperation), and in practice sustains high total payoffs in finite CPR tournaments.
'''

description_COOPERATIVE_82 = '''
Below is a fully‐specified “reciprocal cooperation” strategy that (a) starts off by cooperating, (b) punishes each round of defection with exactly one round of defection, (c) immediately forgives thereafter, and (d) in the very last round exploits full mutual cooperation if and only if no one has ever defected before.  This kind of “Generous Tit‐for‐Tat” is simple, transparent, and keeps the stock high while still credibly punishing defections.

--------------------------------------------------------------------------------
State variables (maintained by your agent across rounds)  
• punish_counter ∈ {0,1}: how many remaining punishment rounds you owe (initially 0)  
• ever_defected ∈ {false,true}: has anyone (including you) ever played D? (initially false)  

Decision rule for round t, given history of actions A₁,…,A_{t–1} and current stock S_t:  

1.  Update ever_defected  
    If in any previous round k < t some player j played D, set ever_defected ← true.  

2.  If t = 1:  
       play C.  
       (No punishment can be pending in round 1.)  

3.  Else if punish_counter > 0:  
       • play D  
       • punish_counter ← punish_counter – 1  
       (You are serving your one‐round punishment.)  

4.  Else if someone defected in the immediately preceding round (round t–1):  
       • punish_counter ← 1  
       • play D  
       (Start exactly one round of punishment.)  

5.  Else if t = r (the last round):  
       • If ever_defected = false then play D  
         (Exploit only if full cooperation has held so far.)  
       • Else play C  

6.  Else:  
       play C  
       (All clear, full cooperation this round.)  

--------------------------------------------------------------------------------
Pseudocode  

```
initialize punish_counter ← 0
initialize ever_defected ← false

for t in 1…r:
    # 1. Observe history and update ever_defected
    for each past round k < t:
        if any player played D in round k:
            ever_defected ← true

    # 2. First round
    if t == 1:
        action_t ← C

    # 3. Serve outstanding punishment
    elif punish_counter > 0:
        action_t ← D
        punish_counter ← punish_counter - 1

    # 4. Trigger punishment if last round saw any defection
    elif (in round t-1, any player played D):
        punish_counter ← 1
        action_t ← D

    # 5. Last round exploitation
    elif t == r:
        if ever_defected == false:
            action_t ← D
        else:
            action_t ← C

    # 6. Otherwise, cooperate
    else:
        action_t ← C

    # play action_t simultaneously with others, observe consumption & new stock…
end for
```

Rationale and properties  
• “Nice”: you start by cooperating and will always cooperate in any round that is free of recent defections.  
• “Retaliatory but only briefly”: you punish exactly one round of D – this is enough to make defection unprofitable in expectation, but you immediately forgive so the pool can regrow.  
• “Forgiving”: once the one‐round punishment is served, you go back to C even if others keep defecting (you only retaliate against the immediately preceding defection).  
• “Exploitive endgame (optional)”: if the entire history up to round r–1 has been spotless, you claim the extra payoff in round r by defecting; if there’s been any defection ever, you end cooperatively.  This gives you a bonus only when others have shown perfect cooperation.  
• “State‐aware lightness”: no internal bookkeeping of stocks is required other than observing defections; the pool dynamics take care of automatic regrowth whenever play returns to cooperation.  

This strategy is easy to read (so opponents know punishments are predictable), robust to one‐off mistakes, and keeps the common pool near capacity for almost all rounds while still deterring defectors.
'''

description_COOPERATIVE_83 = '''
Below is a fully specified, “cooperative‐minded” strategy that (1) aims to sustain full cooperation as long as possible, (2) disciplines any one‐off defection with a minimal punishment, and (3) handles first, intermediate, and last rounds.  It uses only public information (who defected in the previous round), requires no private signals or communication, and is easy to implement.

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
Informal Description  
––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
1.  In round 1, cooperate.  
2.  In any non‐final round t>1, if in round t−1 every player cooperated, then cooperate; if any player defected in t−1, then defect in t to “punish” the group—but only for one round. After that single‐round punishment, resume cooperation.  
3.  In the final round (t = r), defect.  (Since there is no future to protect, defection maximizes immediate payoff.)  

This is essentially “Limited Punishment Tit-for-Tat with Endgame Defection.”  It achieves full cooperation on all (or almost all) rounds when others use it, yet deters unilateral free‐riding by a 1-round penalty.  

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
Pseudocode  
––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
Parameters:  
  n, r, capacity  (common‐pool game parameters)  
State variables (maintained between rounds):  
  punish_counter  ∈ {0,1}  ← 0   // how many more rounds we will punish  
For t from 1 to r do:  
  if t == 1 then  
    action ← “C”  
  else if t == r then  
    action ← “D”                              // Last‐round defection  
  else if punish_counter > 0 then  
    action ← “D”  
    punish_counter ← punish_counter − 1      // we served our one‐round punishment  
  else  
    // Look at actions in round t−1 (publicly observed)  
    if (any player played “D” in round t−1) then  
      action ← “D”                            // trigger punishment  
      punish_counter ← 1 − 1                  // set up one round of punishment  
      // (so punish_counter becomes 0 after decrement)  
    else  
      action ← “C”                            // everyone cooperated last round  
    end if  
  end if  

  // Play “action” in this round, observe all players’ moves  
  // and record them for round t+1.  
end for  

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
Explanation of Key Features  
––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
•  Full cooperation baseline. By cooperating whenever no defection was seen last round, the strategy preserves the high‐stock equilibrium (stock stays at capacity).  
•  Minimal, targeted punishment. A single round of defection punishes everyone just enough to deter unilateral cheating, but then cooperation is immediately restored.  
•  Endgame defection. In the final round there is no continuation value to protect, so the strategy defects to maximize its one‐period payoff.  
•  No private signals or extra bookkeeping. Only a one‐bit counter (punish_counter) plus the index of the current round are needed.  
•  Scalability. Exactly the same rule works for any n≥2 or r>1, and for any capacity≥2n.  

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
Why It Is Cooperative  
––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
Against itself (and any other group of players playing this strategy), everyone cooperates every round except the last, so the pool regenerates fully and each player earns S/(2n) each period, which is the maximal sustainable per‐round payoff.  If any single player defects, the group as a whole punishes immediately—destroying the defector’s short‐term gain (by driving the stock down) and then returns to cooperation.  This credible, low‐cost punishment enforces near‐perfect cooperation.
'''

description_COOPERATIVE_84 = '''
Below is a simple “conditional‐cooperation” strategy that (a) strives to keep the stock near capacity by cooperating whenever possible, (b) deters one‐off defections by a one‐round tit-for-tat punishment, and (c) takes account of the known end‐game.  It requires no side‐payments or communication—only public observation of past actions.

Name: CCMP (Conditional Cooperation with Minimal Punishment)

Notation & state you maintain  
• t = current round, 1 ≤ t ≤ r  
• Sₜ = stock at start of round t (publicly observed)  
• Hₜ₋₁ = history of all players’ actions up through round t–1  
• punish_timer ∈ ℕ (initially 0)  

Parameters  
• k = 1 (size of punishment in rounds)  
• S_threshold = ε·capacity (optional small‐stock override; see “Edge Cases”)  

Core decision rule for player i at round t:

1. If t == 1:  
      action_i ← C  
2. Else if t == r:  
      // Last‐round “end‐game”  
      action_i ← D  
3. Else if punish_timer > 0:  
      // We are in a punishment window  
      action_i ← D  
      punish_timer ← punish_timer – 1  
4. Else if (∃ j ≠ i with action_j(t–1) == D):  
      // Someone defected last round, punish once  
      punish_timer ← k  
      action_i ← D  
5. Else:  
      // No recent defection, default to cooperation  
      action_i ← C  

Edge‐Case: Very Low Stock  
If you wish to be extra cautious when the resource is nearly exhausted, you can override steps 2–4 whenever  
      Sₜ ≤ S_threshold  
and force action_i ← C.  
A reasonable choice is S_threshold = capacity/(4n) or even smaller so that you rebuild the stock before it hits zero.

Pseudocode  

```
initialize punish_timer ← 0

for t in 1…r:
    observe S_t, H_{t-1}

    if t == 1:
        A_i ← C

    else if t == r:
        // no future to punish; grab last‐round benefit
        A_i ← D

    else if S_t ≤ S_threshold:  
        // low-stock emergency override
        A_i ← C

    else if punish_timer > 0:
        A_i ← D
        punish_timer ← punish_timer - 1

    else if exists any j ≠ i with action_j(t-1) == D in H_{t-1}:
        punish_timer ← k        // schedule k rounds of punishment
        A_i ← D

    else:
        A_i ← C

    play A_i
end for
```

Explanation of Why This Is Cooperative  
1. Default‐cooperate: As long as no one defects, everyone repeatedly plays C, which sustains the stock at or near capacity—maximizing group payoff.  
2. Minimal retaliation: A single defection (D) by any player triggers exactly one round of defection in return. This punishes would-be free‐riders but is not so harsh that it collapses cooperation forever.  
3. Forgiveness: After the one‐round punishment, we immediately revert to cooperation, giving others the chance to resume the cooperative equilibrium.  
4. End‐game logic: In the very last round t=r, no future punishment is possible, so a purely selfish defection maximizes that round’s payoff. Including this ensures you don’t “leave money on the table” versus other defectors.  
5. Low‐stock override (optional): If you detect the common pool is nearly depleted, you unconditionally cooperate to help rebuild it, preventing accidental collapse from “too many or too large” punishments.

This strategy is easy to implement, requires only public history, and—by design—elicits and stabilizes high levels of cooperation in the early and middle rounds while protecting you against exploiters and capturing the unavoidable last‐round incentive to defect.
'''

description_COOPERATIVE_85 = '''
Below is a single‐strategy recipe (no off‐tournament pre-play, no secret signals) that (i) sustains cooperation as long as everyone does; (ii) punishes defections quickly but forgives; and (iii) recognizes end‐game and low‐stock “salvage” incentives.

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
Parameters you may tune  
  · k := punishment length (e.g. 3)  
  · S_salvage := capacity/4   (below this stock, future value is small so defect to grab what you can)  
––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  

State variables  
  · t = current round (1…r)  
  · S_t = common-pool stock at start of round t  
  · pun_counter = 0  (how many rounds of punishment remain, initially zero)  

Strategy for player i each round t:  
1.  If t == r (last round)  
      play D  (always defect on the very last round to maximize one‐shot payoff)  
2.  Else if S_t ≤ S_salvage  
      play D  (salvage: when stock is very low, future cooperation payoff is small)  
3.  Else if pun_counter > 0  
      play D  
      pun_counter ← pun_counter – 1  
4.  Else if t == 1  
      play C  (start by cooperating)  
5.  Else  (t in 2…r–1, no active punishment, stock above salvage)  
      • Observe Hₜ₋₁ = {actions of all players in round t–1}.  
      • If every player played C in t–1  
           play C  
        Else  
           play D  
           pun_counter ← k–1    (we defect now plus k–1 more rounds)  

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
Explanation of rationale  

1. Cooperative “basin of attraction.”  
   As long as all saw mutual C in the previous round, we keep cooperating. That yields the highest long‐run common‐pool stock and thus the highest per‐round payoffs (S/(2n)).  

2. Quick, limited punishment.  
   If any defector appears, we immediately defect and keep defecting for k total rounds. This inflicts a cost on defectors (they see you dining out instead of punishing hard), but because k is finite we return to cooperation—so we avoid permanent collapse due to one misstep.  

3. Forgiveness.  
   After punishing for k rounds, pun_counter expires and we resume C (provided no new defections), so occasional mistakes don’t snowball.  

4. End‐game defection.  
   In a finite horizon r, the very last round has no future, so D is dominant. We therefore always defect in round r. Cooperating in r–1 yields no reward in r (everyone defects), so t = r–1 sees no future benefit either—but our salvage rule (step 2) handles that automatically if stock is low. You could likewise extend “always D” to the final two rounds, but often a 1–round end squeeze is enough.  

5. Low‐stock salvage.  
   When S_t falls below S_salvage = capacity/4, even mutual cooperation yields small payoffs, so it can be individually rational to defect to extract S/n rather than S/(2n). At that point we switch to defection until someone rebuilds stock (in practice other cooperators will push S back above S_salvage).  

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
Pseudocode summary  

```
initialize pun_counter ← 0

for t in 1…r:
    observe S_t, history of all actions
    
    if t == r:
        action ← D
    else if S_t ≤ capacity/4:
        action ← D
    else if pun_counter > 0:
        action ← D
        pun_counter ← pun_counter – 1
    else if t == 1:
        action ← C
    else:  
        if (everyone played C in round t–1):
            action ← C
        else:
            action ← D
            pun_counter ← k – 1
    end if

    play action
end for
```

You can choose k (e.g. 3 or ⌊r/10⌋) based on how strong a deterrent you want.  This strategy rewards mutual cooperation, punishes defections swiftly but not forever, and handles both end‐game and low‐stock edge cases in a unified way.
'''

description_COOPERATIVE_86 = '''
Below is a single‐agent strategy whose default is “full cooperation” (i.e. always play C) but which (1) punishes any defection by others, (2) forgives after a short punishment, and (3) protects you from last‐round exploitation.  It requires only knowing the public history of who played C or D and the current round number t ∈ {1,…,r}.  

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
I. Intuition  
1.  Full cooperation (all C) keeps the stock at capacity every round, yielding you payoff  S/(2n) each time.  
2.  A single defection by anybody immediately reduces stock in future rounds.  We therefore want to deter defection by “punishing” it—playing D ourselves for a few rounds—so that the one‐shot temptation (getting S/n instead of S/(2n)) is outweighed by future losses from lowered stock due to the punishment phase.  
3.  After a short punishment window we forgive and return to cooperation, so that the game returns to the high‐stock equilibrium.  
4.  Because in the very last round (t = r) there is no future to punish us, rational opponents will defect there — so we also defect in t = r to avoid being exploited on the last move.  

You never need to guess who will defect in the future; you only react to observed past defections.  

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
II. Strategy Parameters  
Let:  
•  P = punishment length (in rounds).  A reasonable choice is P = n (number of players), or any small integer ≥1.  This makes defection unprofitable for an opponent, because losing P cooperative rounds (with high stock) outweighs the one‐round gain.  
•  r = total number of rounds.  
•  t = current round index (1 ≤ t ≤ r).  
•  history = the set of past rounds’ action profiles, from which you can tell in each past round whether every player played C or if there was at least one D.  

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
III. Pseudocode  

Define:  
 last_defect_round ← 0   // the most recent round in which at least one opponent played D  
 punishment_until ← 0     // last round index of current punishment phase  

At each round t:  
  1. If t = 1:  
       action ← C      // start cooperatively  
  2. Else if t = r:  
       action ← D      // last‐round defection to avoid being exploited  
  3. Else:  
     a. Scan history of rounds 1…t−1.  
        If in round τ (1 ≤ τ < t) you saw at least one D by someone, set last_defect_round ← max(last_defect_round, τ).  
     b. If last_defect_round > 0 and punishment_until = 0 then  
          // a new defection has occurred, so trigger punishment  
          punishment_until ← last_defect_round + P  
     c. If t ≤ punishment_until then  
          action ← D      // we are in punishment phase  
     d. Else  
          action ← C      // no recent defections to punish  cooperate  

  4. After choosing action for round t, proceed to next round.  

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
IV. Explanation of Key Features  
1. First round (t=1): always C, to signal willingness to cooperate.  
2. Detection & punishment: as soon as you observe any D at τ, you defect for the next P rounds (from τ+1 up to τ+P).  This assures the one‐shot advantage of defection (extra S/(2n) that round) is more than paid for by you defecting P rounds in a row (which lowers the stock for everyone).  
3. Forgiveness: once t > punishment_until you go back to C.  This lets you restore the stock to capacity if others also return to C.  
4. Last round (t=r): always defect.  In a finite game the last move can’t be punished, so it is safest to defect to avoid being exploited.  
5. If another defection occurs during your punishment phase, you simply extend punishment by resetting punishment_until ← last_defect_round + P.  

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
V. Why It Is Cooperative  
•  As long as no one defects, you cooperate every round except the forced defection in t=r.  That maintains the resource at capacity and maximizes everybody’s flow payoffs.  
•  You never over‐punish: the punishment always lasts exactly P rounds per defection event.  After that you immediately forgive, giving partners an incentive to return to cooperation.  
•  You use the minimal necessary punishment to deter defection, then quickly restore cooperation and resource stock.  

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
This strategy will earn near‐cooperative payoffs against other cooperators, successfully deter one‐shot defections by imposing a larger future cost (in reduced stock), and also guard you against last‐round exploitation.
'''

description_COOPERATIVE_87 = '''
Below is a single‐strategy “Tit‐for‐Tat with End‐Game Defection” that (1) starts fully cooperative, (2) punishes any defection for one full round, (3) forgives immediately thereafter, and (4) defects in the last round when no further punishment is possible.  In repeated‐game tournaments this tends to sustain cooperation while still protecting you against exploiters, and it handles all edge‐cases of first and last rounds.

––––––––––––––––––––––––––––––––––––––––––––––––  
1. PARAMETERS AND STATE  
  • n, r, capacity as given  
  • S_t = common‐pool stock at start of round t  
  • history[t][i] ∈ {C,D} = action taken by player i in round t  

2. INTERNAL VARIABLES  
  • punish_counter ∈ ℕ, initially 0  
      – how many more rounds we will defect to punish a past defection  

3. HIGH-LEVEL DESCRIPTION  
  – Round 1: Cooperate  
  – For t=2…r–1:  
      • If punish_counter>0 ⇒ play D and punish_counter––  
      • Else if any player defected in round t–1 ⇒ set punish_counter←1 and play D  
      • Else ⇒ play C  
  – Round r (last round): play D  

4. PSEUDOCODE  

  initialize punish_counter ← 0  

  for t in 1..r do  
    if t == 1 then  
      play C  
      continue  
    end  

    if t == r then  
      /* No future rounds in which to punish,
         so defect to maximize one‐shot gain */  
      play D  
      continue  
    end  

    /* t is neither 1 nor r: use TFT‐style rule */  
    if punish_counter > 0 then  
      play D  
      punish_counter ← punish_counter – 1  
    else  
      /* Did any player defect last round? */  
      if ∃ j in {1..n} such that history[t–1][j] == D then  
        /* Punish once */  
        punish_counter ← 1  
        play D  
      else  
        /* Everyone cooperated last round – cooperate now */  
        play C  
      end  
    end  
  end  

5. RATIONALE AND PROPERTIES  
  1. Cooperative baseline.  By playing C whenever no defection has just occurred, this strategy sustains full cooperation on all non‐end rounds as long as no one cheats.  
  2. Immediate, short punishment.  Any one defection (by any player) triggers exactly one round of mutual D; punishing only one round then forgiving avoids endless mutual retaliation.  
  3. Last‐round defection.  In the final round there is no credible threat of future retaliation, so we defect to capture the higher round‐r payoff.  This also anticipates that rational opponents will defect in r, so it prevents you from being exploited at the end.  
  4. Simple to implement, transparent.  Opponents can easily infer your rule, which in practice increases the chance that they will cooperate early (to avoid being punished).  
  5. Robust to noise.  If a single “mistaken” D occurs (either by you or someone else), you punish one round then immediately return to cooperation, minimizing welfare loss.  

––––––––––––––––––––––––––––––––––––––––––––––––  
This strategy requires no side‐payments or communication, uses only the public history of C/D plays, and handles first and last rounds explicitly.  It is widely known to foster high levels of cooperation in finitely repeated dilemmas, minimizes over‐punishment, and protects you against pure exploiters.
'''

description_COOPERATIVE_88 = '''
Below is a single‐agent “cooperative” trigger‐style strategy built on Tit‐for‐Tat with limited punishment and an endgame‐defection escape.  It aims to keep the stock at capacity by rewarding cooperation and punishing defectors just long enough to make defection unprofitable, then forgiving so cooperation can restart.

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
1.  Internal Variables  
   • punishment_left ← 0  
     – counts down remaining punishment rounds.  
   • last_round ← r  

2.  Parameters  
   • P = 2   # length of punishment phase after detecting defection  
   • E = 1   # number of final rounds in which we always defect (endgame)

3.  Decision Rule (each round t = 1…r):  
   Input at start of round t:  
     • t (current round index)  
     • S_t (current stock)  
     • History of all players’ actions in rounds 1…t–1  

   Pseudocode:  
     if t == 1:  
       action ← C  
       punishment_left ← 0  

     else if t > last_round – E:  
       # In the final E rounds there is no future to protect ⇒ defect  
       action ← D  

     else if punishment_left > 0:  
       # We are currently punishing a past defection  
       action ← D  
       punishment_left ← punishment_left – 1  

     else  
       # Look at what happened in the previous round  
       if ∃ j ≠ i such that action_j(t–1) = D:  
         # Someone defected last round ⇒ punish them  
         action ← D  
         punishment_left ← P – 1  
       else:  
         # No defection last round ⇒ cooperate  
         action ← C  

     return action  

4.  Explanation of Key Features  
  • First round (“test of intent”) is cooperative.  
  • As long as nobody defected last round, continue cooperating.  
  • On seeing any defection, switch to D for P consecutive rounds, then return to C.  
  • In the final E rounds, unconditionally defect (there is no future to protect).  

5.  Why It’s Cooperative  
  • Maintains full stock at capacity when all play C ⇒ each round payoff = capacity/(2n).  
  • Limited punishment (P=2) makes defection unprofitable in expectation:  
      – One round of immediate gain (S/n instead of S/(2n)) is outweighed by two rounds of lower payoff (D against C in the punishment rounds).  
  • Forgiving structure (returns to C after punishment) allows mutual return to high‐yield cooperation.  
  • Endgame defection acknowledges standard backward‐induction without destroying early cooperation.  

6.  Handling Edge Cases  
  • t=1: no history ⇒ cooperate.  
  • Overlapping punishments and endgame: the endgame rule (t>r–E) dominates, so we defect anyway.  
  • If multiple players defect in the same round, we still apply a single P‐round punishment.  
  • If, during punishment, others all cooperate, we keep defecting until punishment_left hits zero, then immediately resume cooperation.  

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
By keeping punishments short, we ensure defection is deterred but cooperation can quickly resume.  The endgame defection is unavoidable in finite‐horizon games, but for the vast majority of rounds this strategy reliably preserves the common pool at capacity and maximizes collective payoffs.
'''

description_COOPERATIVE_89 = '''
Below is a single‐strategy recipe for “staying green” while still guarding against free-riders.  It uses a Tit-for-Tat–style trigger with one–round punishment, plus “end-game generosity” if everyone has cooperated so far.

1.  Definitions and bookkeeping  
   •  Let r = total rounds, t = current round (1…r).  
   •  Track last_round_defections: did any player defect in round t–1?  Initialize last_round_defections = false.  
   •  Track punished = false: are we currently serving a punishment move?  

2.  High-level idea  
   •  Round 1: cooperate unconditionally.  
   •  In any round t>1:  
     –  If we are in punishment (punished==true), play D, then clear punished.  
     –  Else if anyone defected in t–1 (last_round_defections==true), set punished=true and play D.  
     –  Else (nobody defected last round), play C.  
   •  Final round (t=r):  
     –  If nobody has ever defected (all rounds 1…r–1 are C), then play C (end-game generosity).  
     –  Otherwise play D (last–round defection).  

3.  Pseudocode  
```
initialize:
  last_round_defections = false
  punished = false

for t in 1…r:
  if t == 1:
    action = C
  else if t == r:  # final round
    if all past actions (rounds 1…r–1) were C by everyone:
      action = C
    else:
      action = D
  else:
    if punished:
      action = D
      punished = false
    else if last_round_defections:
      action = D
      punished = true
    else:
      action = C

  play(action)

  # Observe actions of all players this round
  if any player chose D this round:
    last_round_defections = true
  else:
    last_round_defections = false
```

4.  Explanation of key features  
  •  “Start nice”: round 1 is C, signaling willingness to sustain the resource.  
  •  Tit-for-Tat style punishment: one round of D for every observed defection, then forgive.  
  •  End-game generosity: if the group has fully cooperated up to round r–1, we still play C in r to maximize group payoff (even though a narrow self-interested one-shot defection in the last round would pay more).  This signals that full cooperation is rewarded through the very end.  
  •  If any defection ever occurs, we do defect on the last round to recoup immediate value rather than reward a defector with C in the end.  

5.  Why it is cooperative  
  •  When all use it, the common-pool stock stays at capacity: all rounds except forced punishments see everybody playing C → each round payoff = capacity/(2n).  
  •  A single one-pulse defection against us is met with one round of D (which reduces that defector’s future streak of high C-payoffs), then we return to C and rebuild the pot.  
  •  By forgiving after one punishment round, we avoid long vendettas that drive stock to collapse.  
  •  By cooperating in the final round only if no one has ever defected, we protect against end-game free-riding without undermining incentives to cooperate earlier.  

6.  Edge cases  
  •  First round: C always.  
  •  A defection burst across multiple rounds: we punish each defection with exactly one immediate D (so if opponents defect twice in a row, we punish twice).  
  •  If two players defect in round t, we still punish with a single D in t+1.  This suffices to reduce the defector’s cumulative payoff by exactly one round’s “extra” D-gain.  
  •  If stock ever hits zero (everyone defected), punishments are automatic Ds until final, but there is no resource left anyway—so the strategy simply tracks defection history.  

This strategy is simple, transparent, and fully cooperative—any sustained group of users will keep the resource at peak capacity and divide it fairly every round.
'''

description_COOPERATIVE_90 = '''
Below is a single‐strategy “recipe” for sustainable cooperation in the Common Pool Resource Game.  It is built on the familiar “tit-for-tat” idea, with proportional, short punishment for observed defections and ready forgiveness, and with an explicit first-round and last-round rule.  It never assumes off‐game communication or side‐agreements.

--------------------------------------------------------------------------------
STRATEGY NAME  
  Responsive Conditional Cooperation (RCC)

GOAL  
  Keep the stock near capacity by cooperating (C) as long as others do, and deter isolated defections with brief, proportional punishment rounds.

PARAMETERS  
  • n = number of players  
  • r = total rounds  
  • For bookkeeping only:  
     – pun_timer ∈ {0,1,2,…}  (counts down punishment rounds)  

STATE YOU MAINTAIN  
  • pun_timer (initially 0)  
  • history of last round’s actions of all opponents  

DECISION RULE (per round t = 1…r)  
  1. If pun_timer > 0 then  
       play D  
       pun_timer ← pun_timer – 1  
       → (You are in the middle of a punishment phase.)  
     else if t = 1 then  
       play C  
       → (Open with cooperation.)  
     else if in round t–1 at least one opponent played D then  
       let k = number of opponents who chose D in round t–1  
       pun_timer ← k  
       play D  
       → (Start a punishment phase lasting k rounds.)  
     else  
       play C  
       → (All clear: return to cooperation.)  
  2. After deciding your move, if t = r (the last round), override and play C.  
     → (We still cooperate even in the last round to protect the stock and group return.)

PSEUDOCODE

  initialize pun_timer ← 0

  for t in 1 to r:
    if pun_timer > 0:
      my_action ← D
      pun_timer ← pun_timer − 1
    else if t = 1:
      my_action ← C
    else if “someone defected in previous round”:
      k ← count_of_opponents_who_chose_D_in_round(t−1)
      pun_timer ← k
      my_action ← D
    else:
      my_action ← C

    if t = r:
      my_action ← C     # final‐round override

    execute(my_action)
    observe opponents’ actions to use in t+1

RATIONALE

1.  Cooperative “baseline.”  By default (no recent defections), you choose C.  
2.  Proportional punishment.  If one or more opponents defect, you immediately switch to D for exactly as many rounds as there were defectors; punishers and punished alike know the retaliation is limited.  
3.  Forgiveness.  Once the punishment counter expires, you return to cooperation even if the punished opponent never “repays”—this discourages endless vendettas.  
4.  First‐round cooperation lowers the barrier to forming a cooperative convention.  
5.  Last‐round pardon.  Even though a purely selfish agent would defect in round r, you cooperate to protect the stock and boost collective payoff; this reduces the stock‐race dynamic in the penultimate rounds.  

EXPECTED EFFECT

•  When all players follow RCC, the stock stays at capacity each round and each player harvests capacity/(2n) every time.  
•  A single defection by an opponent triggers a short, predictable backlash that makes unilateral defection net unprofitable over the next k+1 rounds, thus sustaining cooperation.  
•  Because punishment is limited and forgiveness quick, the group recovers after isolated mistakes (e.g. noise or an accidental D).  
•  By cooperating in the final round, the strategy avoids the typical end-game rush to defect, helping maintain a higher stock going into round r and thus higher total payoffs.

This strategy requires no external coordination device, communicates intent solely through observable actions, and is a well‐known folk‐theorem–style trigger strategy adapted to a finite‐horizon CPR setting.
'''

description_COOPERATIVE_91 = '''
Below is a single‐strategy “cooperative” rule for this n‐player CPR game.  It uses a multi‐player Tit‐for‐Tat (TFT) style trigger, plus the standard finite‐horizon adjustment (everyone defects in the very last round).  The idea is: start by cooperating, punish any observed defection with exactly one round of group defection, then immediately forgive and return to cooperation.  This keeps the pool near capacity when everyone is cooperating, but deters free‐riding with a short, predictable punishment.

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––
1.  State variables  
    lastRoundHadDefection ← false  

2.  Action‐selection at the beginning of each round t = 1…r  
    if t = 1 then  
       play C  (cooperate)  
    else if t = r then  
       play D  (defect in the final round)  
    else  
       if lastRoundHadDefection = true then  
         play D        (punishment phase: one‐round defection)  
       else  
         play C        (otherwise, cooperate)  
       end if  
    end if  

3.  Update after observing everyone’s actions in round t:  
    lastRoundHadDefection ← (there exists at least one player j who played D in round t)  

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––
Explanation of each design choice:

1.  “Start with C.”  
    • By cooperating in round 1 we signal willingness to sustain the resource.  

2.  “Punish once, then forgive.”  
    • If any player defects in round t–1, we defect in t (group punishment).  
    • Exactly one round of defection is enough to inflict a cost on defectors but is short enough that the pool can recover quickly.  

3.  “Cooperate otherwise.”  
    • As long as no one has defected in the immediately preceding round, we return to cooperation.  This ensures that mutual cooperation—and thus a high stock level—is maintained whenever possible.  

4.  “Defect in the last round.”  
    • In a finite‐horizon game, cooperation unravels at the end.  By defecting in round r we avoid being exploited in the one‐shot final subgame.  

Edge cases and comments:  
– If the first round ever has a defection, we punish in round 2, then revert to cooperation in round 3 (unless another defection occurs).  
– If two defectors strike in consecutive rounds, each will be met with a one‐round punishment, but no punishment carries over beyond one round—this avoids long “death spirals.”  
– If r=2, the strategy is: (round 1: C; round 2: D).  
– If nobody ever defects, the stock stays near capacity and every round t<r yields a high payoff S/(2n).  
– Against “always‐defect” opponents, we defect from round 2 on, avoiding any sucker payoffs after round 1.  
– Against “always‐cooperate,” we cooperate until the last round, then defect to secure the final one‐shot gain.  

This strategy is simple, clear to any opponent, enforces cooperation with minimal collateral damage, and handles the no‐communication, finite‐horizon setting cleanly.
'''

description_COOPERATIVE_92 = '''
Below is a single‐strategy proposal—called “Tit‐for‐Tat with Finite Punishment”—that aims to sustain high resource levels by rewarding cooperation and punishing defection just long enough to deter future over‐harvesting.

1. Overview of the idea  
   • Start by cooperating (low take).  
   • Monitor total consumption each round to detect any defections.  
   • If you detect a defection, defect (high take) for a fixed number of rounds P (punishment phase), then resume cooperation.  
   • In the very last round, you may optionally cooperate if no defection ever occurred (to maximize group welfare), but defect if you are still in punishment or if you have ever been “cheated.”  

2. Key parameters  
   • n = number of players  
   • r = total rounds  
   • capacity = carrying capacity of the resource  
   • P = punishment length (we recommend P = 1 or 2)  
   • ε = small tolerance for numerical noise (e.g. ε = 10⁻⁶)  

3. Detection of defection  
   In any round t, let Sₜ be the stock at the start of round t.  
   Under full cooperation (all play C), total consumption = n·(Sₜ/(2n)) = Sₜ/2.  
   After observing total_consumptionₜ in round t, declare “defection occurred” if  
     total_consumptionₜ > (Sₜ/2 + ε).  

4. State variables  
   punish_timer ← 0      // how many rounds of punishment remain  
   ever_cheated  ← false // have we ever detected a defection?  

5. Pseudocode  
   For each round t = 1…r do  
     if t == 1 then  
       action ← C                             // open with cooperation  
     else if punish_timer > 0 then  
       action ← D                             // still punishing  
       punish_timer ← punish_timer − 1  
     else  
       // at this point, we are in “normal” (cooperative) mode  
       if defection_detected_in_prior_round then  
         ever_cheated ← true  
         punish_timer ← P − 1                 // use up one punishment round now, keep P–1 left  
         action ← D  
       else  
         action ← C  
       end if  
     end if  

     // Special‐case for the very last round  
     if t == r then  
       if ever_cheated or punish_timer > 0 then  
         // If we’ve ever been cheated or are still punishing, defect  
         action ← D  
       else  
         // If nobody ever cheated, cooperate even in the last round  
         action ← C  
       end if  
     end if  

     play(action)  

     // After all plays are in, observe total_consumptionₜ and stock Sₜ  
     if total_consumptionₜ > Sₜ/2 + ε then  
       defection_detected_in_prior_round ← true  
     else  
       defection_detected_in_prior_round ← false  
     end if  
   end for  

6. Explanation of decision rules  
   – First round (t=1): cooperate, to signal goodwill.  
   – Normal rounds (1 < t < r):  
       • If no one defected last round, keep cooperating.  
       • If you saw total take exceed the cooperative benchmark, enter a punishment phase of P rounds where you defect.  
       • After P punishment rounds, return to cooperation.  
   – Last round (t = r):  
       • If you’ve maintained perfect cooperation throughout, continue cooperating (maximizes group payoff without future risk).  
       • Otherwise, defect to recoup individual payoff (since no future).  

7. Why this is cooperative  
   – It achieves the full‐cooperation stock cycle (stock regenerates to capacity) whenever all players stick to C.  
   – Any one‐round defection triggers a clear but limited penalty, discouraging over‐consumption.  
   – By forgiving after P rounds, it allows the group to re‐establish high stock rather than spiral into permanent collapse.  
   – Cooperating even in the last round (if never cheated) signals strong commitment to group welfare.  

8. Tuning  
   – Punishment length P = 1 is classic tit‐for‐tat; P = 2 adds extra deterrent at the cost of slightly more group harm during punishment.  
   – Tolerance ε guards against floating‐point noise when computing Sₜ/2.  

With this strategy, any individual knows that unilateral over‐harvesting causes an immediate short punishment, after which everyone will happily return to the mutually best outcome of sustained cooperation and high resource levels.
'''

description_COOPERATIVE_93 = '''
Below is a single‐strategy entry—“Graduated Tit‐for‐Tat with Endgame Defection (G‐TFT‐E)”—that aims to keep the stock high through mutual cooperation, punish deviations briefly, forgive, yet also take the one‐shot defection in the last round as standard finite‐horizon logic dictates.  

1.  Strategy name  
    G-TFT-E (Graduated Tit-for-Tat with Endgame Defection)  

2.  Intuition  
    •  Start by cooperating.  
    •  As long as everyone has cooperated in the immediately preceding round, continue cooperating (to maintain the stock near capacity).  
    •  If any player defects in round t−1, punish by defecting for a fixed number of rounds P (here P = 1), then forgive and return to cooperation.  
    •  In the very last round (t = r), defect—because there is no future to incentivize cooperation.  

3.  Parameters  
    •  r : total number of rounds  
    •  P : punishment length after detecting a defection (we set P = 1)  
    •  G : endgame length during which we always defect (we set G = 1 ⇒ only the final round)  

4.  State variables  
    •  PunishTimer ∈ {0,1,…,P} : counts how many more rounds we will defect as punishment  

5.  Pseudocode  
    ```
    initialize PunishTimer ← 0

    for t in 1..r do
        if t > r − G then
            # Endgame defection
            action ← D

        else if PunishTimer > 0 then
            # We are in punishment phase
            action ← D
            PunishTimer ← PunishTimer − 1

        else if t > 1 and “at least one opponent played D in round t−1” then
            # Start a new punishment phase
            PunishTimer ← P
            action ← D

        else
            # No recent defections and not endgame ⇒ cooperate
            action ← C
        end if

        play action
    end for
    ```

6.  Explanation of key points  
    – First round (t = 1): no history ⇒ PunishTimer=0, t≤r−1 ⇒ action=C.  
    – If everyone cooperated in t−1, PunishTimer remains 0 ⇒ C.  
    – If any defection in t−1, we set PunishTimer=P and defect for P rounds, then automatically revert to cooperation.  
    – Last round (t = r): t>r−1 ⇒ always D, extracting the final‐round temptation payoff.  

7.  Why it’s cooperative  
    – It starts by cooperating and will return to cooperation as soon as it has “served” its one‐round punishment for any deviation.  
    – By punishing only briefly, it avoids the dead‐lock of “grim trigger” and thereby stabilizes high stock levels against occasional mistakes.  
    – By defecting only in the last round, it appropriately captures the final‐round bonus without undermining cooperation in all earlier rounds.

This strategy is simple, easy to implement, fosters mutual cooperation on the common pool, corrects for defection quickly, and handles the unavoidable last‐round temptation in a standard way.
'''

description_COOPERATIVE_94 = '''
Below is a single‐strategy entry, called “Generous Trigger‐Tit-for-Tat (GTfT) with Endgame Defection.”  It is explicitly designed to sustain cooperation on the common pool, to punish defections quickly but forgive them after a short era, and to protect itself in the final round against unilateral exploitation.

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
1.  Strategy intuition  
    •  Start fully cooperative (C) so long as nobody defects.  
    •  If anyone defects, issue a short, fixed-length punishment of D’s.  
    •  After the punishment window, return immediately to cooperation.  
    •  In the very last round, defect (D) to avoid a sucker-payoff with no future.  

2.  Parameters  
    n = number of players  
    r = total rounds  
    L = length of punishment (we recommend L=2)  

3.  State variables  
    punishment_timer ∈ {0,1,…,L−1}, initially 0  
    last_round_actions[i] ∈ {C,D} for i=1…n (initialized “none”)  

4.  High-level decision rules  
    At the start of each round t (1≤t≤r):  
      a) If t==1, play C.  
      b) Else if punishment_timer>0, play D (and decrement punishment_timer).  
      c) Else if any opponent played D in t−1, set punishment_timer←L−1 and play D.  
      d) Else if t==r (last round), play D.  
      e) Otherwise, play C.  

5.  Pseudocode  

    // Initialization  
    punishment_timer ← 0  
    for all i: last_round_actions[i] ← none  

    for t from 1 to r do  
      // Observe last‐round defections  
      if t>1 then  
        somebody_defected ← false  
        for each opponent j≠me do  
          if last_round_actions[j]=='D' then somebody_defected ← true  
        end for  
      end if  

      // Decision rule  
      if t==1 then  
        my_action ← 'C'  
      else if punishment_timer > 0 then  
        my_action ← 'D'  
        punishment_timer ← punishment_timer − 1  
      else if somebody_defected == true then  
        // trigger punishment window  
        punishment_timer ← L − 1  
        my_action ← 'D'  
      else if t == r then  
        // final‐round one-shot defection  
        my_action ← 'D'  
      else  
        my_action ← 'C'  
      end if  

      // Play my_action simultaneously with others  
      // Observe all opponents’ actions this round into last_round_actions[]  
      for each opponent j≠me do  
        last_round_actions[j] ← observed_action_of(j)  
      end for  

    end for  

6.  Explanation of design choices  
  •  “Start cooperating” (round 1) signals goodwill.  
  •  Punishment window of fixed length L ensures defectors lose more in the short run, but forgiving (we do not punish forever).  
  •  Immediate return to cooperation prevents endless retaliation cycles.  
  •  Defecting on the last round is the one‐shot best‐response; it protects us from being the sole cooperator when there is no future.  

7.  Edge cases addressed  
  –  First round (t=1): we have no history, so we cooperate to establish trust.  
  –  Rounds with zero stock (S=0): any action yields zero payoff, but D does no worse than C; the above logic still applies.  
  –  Final round (t=r): we explicitly defect to avoid being exploited with no counter-punishment possible.  
  –  Multiple defectors: any single defection by anyone triggers the same punishment.  

This strategy is fully cooperative whenever the group remains clean, sternly enforces a short punishment on any defection, then forgives, and guards itself against unilateral last‐round exploitation.
'''

description_COOPERATIVE_95 = '''
Below is a single‐strategy “recipe” for sustaining cooperation on the common‐pool resource, written in plain English plus small snippets of pseudocode.  It uses a memory‐1 “forgiving trigger” (tit-for-tat with a short punishment phase) plus an endgame defection.  You can tune its parameters (punishment length, thresholds) to your taste.

  
1.  Overview  
    •  Baseline: Everyone cooperates (plays C) so that the stock stays at or near capacity.  
    •  Punish defections promptly but briefly (a short “punishment phase”) so as to deter free‐riding yet not destroy cooperation forever.  
    •  Defect in the very last round to maximize endgame payoff (no future rounds to protect).  

2.  State variables  
    Keep in memory:  
    –  history of everybody’s last action, last round (a boolean “someoneDefectedLastRound”).  
    –  punishCounter: how many remaining rounds you intend to punish (initially 0).  

3.  Parameters  
    –  P  = punishment length (e.g. P = 2 rounds).  
    –  r  = total number of rounds (common knowledge).  

4.  Decision rule for player i in round t:  

    if t == 1 then  
        play C  
        someoneDefectedLastRound ← false  
        punishCounter ← 0  
        return  

    if t == r then  
        /* Endgame defect: no future to lose by defecting */  
        play D  
        return  

    if punishCounter > 0 then  
        /* We are in a punishment phase triggered earlier */  
        play D  
        punishCounter ← punishCounter – 1  
        someoneDefectedLastRound ← true   /* we treat our own D as “defection in last round” */}
        return  

    /* Otherwise: look at what happened in t–1 */  
    if someoneDefectedLastRound then  
        /* Somebody defected in the previous round → trigger new punishment */  
        punishCounter ← P – 1   /* we’ll D now plus P–1 more rounds */  
        play D  
        someoneDefectedLastRound ← true  
    else  
        /* No defection last round → cooperate */  
        play C  
        someoneDefectedLastRound ← false  
    end  

    /* After everyone moves, you update someoneDefectedLastRound for the next round: */  
    someoneDefectedLastRound ← (∃ j : action_j == D)  

5.  Pseudocode  

    initialize:  
        someoneDefectedLastRound = false  
        punishCounter = 0  

    for t in 1..r do  
        if t == 1:  
            a_i = C  
        else if t == r:  
            a_i = D  
        else if punishCounter > 0:  
            a_i = D  
            punishCounter = punishCounter – 1  
        else if someoneDefectedLastRound == true:  
            punishCounter = P – 1  
            a_i = D  
        else:  
            a_i = C  
        end  

        /* observe all actions a_1…a_n this round */  
        someoneDefectedLastRound = (∃ j in 1..n: a_j == D)  
    end  

6.  Why it’s cooperative  
    •  When everyone plays C continuously, the pool regrows to capacity every round → maximal long‐run payoff.  
    •  A single defection by any player immediately triggers a short, inflexible punishment → it deters others from exploiting the commons.  
    •  Punishment is finite (P is small), so once the fog of defection clears, the group returns to full cooperation.  
    •  By defecting in the last round only, you capture any remaining “free” surplus without jeopardizing future cooperation (the standard endgame logic).  

7.  Handling corner cases  
    –  First round: nobody yet to punish → start C.  
    –  Last round (t = r): automatic D (no future to safeguard).  
    –  If the resource ever collapses to zero (S = 0), both C and D yield zero payoff; the above rules still apply—but after a collapse you may as well cooperate (in practice, the code treats it as any normal round).  
    –  You can set P = 1 for one‐round punishments (classical tit‐for‐tat) or P = 2–3 to be more “forgiving.”  

You can of course tweak the punishment length P or add a small resource‐based rule (e.g. if S_t < ε, then always C to help it recover), but the above captures a simple, memory‐1, provably cooperative strategy against arbitrary opponents in the repeated common‐pool game.
'''

description_COOPERATIVE_96 = '''
Here is a simple, robust “cooperative‐minded” trigger strategy that in practice sustains high joint payoffs by keeping the stock near capacity, but also punishes any defection quickly enough to deter free‐riding.

---  
Strategy Name  
  Tit-for-Tat with Final‐Round Defection  

Parameters you may tune  
  • Punishment length k (we’ll set k=1 below for simplicity, i.e. classic Tit-for-Tat)  
  • Final‐round behavior: always defect in round r  

State variables (maintained by your agent)  
  pun_timer ← 0    // counts rounds remaining in a punishment phase  

Decision rule for round t (1 ≤ t ≤ r), given history of all players’ actions:  
  1. If t = r then  
       play D  
       exit.  
  2. Else if pun_timer > 0 then  
       play D  
       pun_timer ← pun_timer − 1  
       exit.  
  3. Else if t = 1 then  
       play C  
       exit.  
  4. Else (t between 2 and r−1, pun_timer = 0):  
     • Look at round t−1.  
     • If every other player chose C in t−1, then  
          play C  
       else  
          // at least one defector detected  
          play D  
          pun_timer ← k    // k=1 for single‐round tit-for-tat punish  
       end  

Notes on key features  
  • First round: we start by cooperating.  
  • Tit-for-tat style: any defection by any opponent in the immediately prior round is punished by one round of D, after which we return to cooperation if they resume C.  
  • Final round: because there is no future to protect, we defect to secure the last‐round payoff.  
  • If you wished a harsher deterrent, simply set k>1 (punish for k rounds), or even k=r−t to punish until the end (“grim trigger”). Conversely, k=1 is the minimal, most forgiving choice.  

Why it is cooperative  
  – As long as everyone sticks to C, the pool regenerates to capacity every round and all players earn S/(2n), the maximal sustainable per‐round payoff.  
  – A singleton defection (D) immediately yields a higher round payoff for that defector, but triggers a swift one‐round punishment that hurts the defector (and all) in the next round—so defection is not a dominant path unless one is willing to forgo future gains.  
  – By forgiving after just k=1 punishment round, the strategy re‐establishes cooperation quickly—minimizing overall stock depletion from long punishments.  
  – Final‐round defection is standard in finitely repeated games; it does not undermine cooperation in earlier rounds because it comes only when no future punishments are possible.  

Pseudocode summary  

```
initialize pun_timer = 0

for t in 1..r do
  if t == r then
    action ← D
  else if pun_timer > 0 then
    action ← D
    pun_timer ← pun_timer - 1
  else if t == 1 then
    action ← C
  else
    if any opponent played D in round t-1 then
      action ← D
      pun_timer ← k      // e.g. k = 1
    else
      action ← C
    end
  end
  play(action)
end
```

This strategy is fully specified by its single parameter k (punishment length).  With k=1 it is the classic Tit-for-Tat plus a last‐round defection.  It is easy to implement, fully non-communicative, and has been shown in many repeated‐game environments to sustain cooperation while deterring free‐riding.
'''

description_COOPERATIVE_97 = '''
Below is one concrete “cooperative” strategy you can enter in the tournament.  It uses a generous tit‐for‐tat style rule to sustain cooperation, punishes any defection briefly, but returns quickly to full cooperation, and in the very last round defects (to protect yourself from being exploited in a one‐shot endgame).

----------------------------------------------------------------------------------------------------  
STRATEGY NAME  
Generous‐TFT‐with‐Endgame‐Defection  

GOAL  
• Sustain full cooperation (everyone plays C) for as long as possible to keep the stock near capacity and maximize joint payoffs.  
• If someone defects, punish exactly one round by defecting, then forgive and return to cooperation.  
• In the final round, defect (to avoid being exploited when there is no future).  

PARAMETERS  
• n = number of players  
• r = total number of rounds (>1)  
• capacity = maximum stock (≥2n)  
• S_t = stock at beginning of round t  
• α = a small “safety” threshold fraction (e.g. α = 0.10)  

DECISION RULES  

1. Initialization (before round 1):  
   • “last_round_defected” ← FALSE  
   • “punish_counter” ← 0  

2. For each round t = 1,…,r:  
   a) Observe:  
      – S_t (current stock)  
      – Actions of all players in round t–1 (for t>1)  
   b) Update bookkeeping (for t>1):  
      if any player j played D in round t–1 then  
         last_round_defected ← TRUE  
      else  
         last_round_defected ← FALSE  
   c) Choose action A_t as follows:  
      if t == r then  
         // final‐round defection  
         A_t ← D  
      else if punish_counter > 0 then  
         // we are in punishment mode  
         A_t ← D  
         punish_counter ← punish_counter – 1  
      else if last_round_defected == TRUE then  
         // trigger one‐round punishment  
         // but first check: will defecting now likely collapse the stock?  
         let predicted_consumption_if_allD = n * (S_t / n) = S_t  
         let S_after_consumption = S_t – predicted_consumption_if_allD  
         // if that would drive the stock below α·capacity, skip punishment to preserve resource  
         if S_after_consumption >= α * capacity then  
            punish_counter ← 1  
            A_t ← D  
         else  
            // stock would collapse: better to keep cooperating and let stock recover  
            A_t ← C  
         end if  
      else  
         // default—full cooperation  
         A_t ← C  
      end if  
   d) Play A_t, observe everyone’s actions, go to next round.  

3. Payoff accumulation  
   Your total payoff = sum of per‐round payoffs π_i,t = S_t/(2n) if you played C, or S_t/n if you played D.  

RATIONALE AND PROPERTIES  
• “Start Cooperating”: Round 1 you play C (punish_counter=0 and no last‐round defection).  
• “One‐round punishment”: If anyone defected in the previous round, you defect exactly once, then return to cooperation.  
• “Safety check”: If punishing by defecting again would collapse the stock below a small threshold (α·capacity), you skip that punishment to preserve the resource for future joint gain.  
• “Endgame defection”: In round r, there is no future to enforce cooperation, so you defect to avoid being the lone cooperator in a one‐shot.  
• “Quick forgiveness” limits collateral damage.  You punish just long enough to deter one‐round deviations, but because you always return to C you restore cooperation quickly.  
• By preserving the resource (safety check) you avoid shooting yourself in the foot when the stock is already endangered.  

This strategy embodies a genuinely cooperative mindset (it strives to keep everyone in C most of the time, rescues the stock if it’s low, only punishes minimalistically), yet protects you in the inevitable last round. Good luck in the tournament!
'''

description_COOPERATIVE_98 = '''
Below is a single‐strategy proposal—call it “Adaptive Tit-for-Tat with Endgame Defection and Resource-Saving”—that aims to sustain near-full cooperation over most of the r rounds, yet is robust to opportunistic defection and avoids total collapse of the common stock.

1.   State variables  
     •  punish_countdown ∈ {0,1,…} – how many rounds of punishment remain  
     •  last_actions: vector of every player’s action in t–1 (empty in t=1)

2.   Parameters (internal)  
     •  P = 1  (length of punishment after a defection)  
     •  S_threshold = capacity/(2n)  (if stock below this, always cooperate)

3.   High-level idea  
     – Start by cooperating.  
     – If anyone defected in the previous round, punish by defecting for P rounds, then forgive.  
     – In the very last round, defect (endgame).  
     – If the stock ever gets critically low (below S_threshold), switch to cooperation unconditionally to help the pool recover.

4.   Pseudocode  

```
Initialize:
  punish_countdown ← 0
  last_actions ← ∅

For each round t = 1,2,…,r do
  Observe current stock S_t
  Observe last_actions (empty if t=1)

  If t == r then
    action ← D        # endgame defection
  Else if t == 1 then
    action ← C        # start cooperatively
  Else if S_t < S_threshold then
    action ← C        # rescue pool when stock is too low
  Else if punish_countdown > 0 then
    action ← D
    punish_countdown ← punish_countdown – 1
  Else if ∃ i ≠ self: last_actions[i] == D then
    punish_countdown ← P
    action ← D        # retaliate
  Else
    action ← C        # otherwise cooperate
  End if

  Submit action
  After everyone moves, record last_actions for next round
End for
```

5.   Explanation of features  
– Cooperative mindset:  
  • You begin by cooperating and default back to cooperation whenever there has been no recent defection.  
  • By cooperating when the pool is low (S_t < S_threshold), you help restore stock even if that temporarily lowers your own payoff—this guards against collapse.

– Deterrence of free-riding:  
  • Any single defection by any player triggers P=1 round of collective defection, which lowers everyone’s future payoffs and thus deters one-shot gains.  
  • After punishment expires, all return to cooperation (forgiveness), which prevents endless “defection wars.”

– Endgame handling:  
  • On the final round t=r you defect. This avoids being exploited by opponents who know you would otherwise cooperate in the last period.  
  • Because r>1, the threat of post-punishment cooperation remains credible up to round r–1.

6.   Edge cases & robustness  
– Multiple consecutive defections: punish_countdown is reset to P each time you observe a defection, so you deliver at least one full round of punishment after the last defection.  
– If stock falls dangerously low, you unconditionally cooperate to rebuild it, recognizing that defecting on a nearly empty stock is self-defeating.  
– No assumptions of shared conventions or off‐equilibrium beliefs—decisions depend only on public history and the current stock.

With this rule you sustain near-full cooperation (everyone gets roughly S_t/(2n) each round and the stock hovers near capacity), but you remain protected against one‐shot or endgame opportunism.
'''

description_COOPERATIVE_99 = '''
Below is a simple “conditionally cooperative” strategy that (1) starts out fully cooperative, (2) punishes any defection by defecting for a short fixed window, then returns to cooperation, and (3) always defects in the last round (since there is no future to protect).  This kind of “generous tit‐for‐tat with finite punishment” preserves the common stock at capacity under mutual cooperation, but deters unilateral defection.

===============================================================================
STRATEGY NAME  
  Generous Conditional–Cooperator (GCC)

PARAMETERS  
  r                total number of rounds  
  P                punishment length in rounds (we suggest P = 2, or P = min(2, r–2) if r is small)  

STATE VARIABLES  
  punish_timer    integer ≥ 0, how many more rounds we are in punishment phase  
  last_round      Boolean, true if we are in round t = r  

INITIALIZATION  
  punish_timer = 0  

AT EACH ROUND t = 1…r  
  Let L = r – t + 1  (rounds remaining, including this one)  
  Observe previous-round actions of all n players (if t = 1 this history is empty).  

  // 1. Handle first round or punishment in progress  
  if t == 1 then  
    play C  
    continue to next round  
  end if  

  if punish_timer > 0 then  
    // we are still punishing  
    action ← D  
    punish_timer ← punish_timer – 1  
    play action  
    continue to next round  
  end if  

  // 2. Last-round defection  
  if t == r then  
    // No future to protect, defect for immediate gain  
    play D  
    continue to next round  
  end if  

  // 3. Check for defection by anyone in the previous round  
  if (in round t–1 at least one player chose D) then  
    // trigger punishment  
    punish_timer ← min(P, L–1)  
    play D  
  else  
    // no defection last round → cooperate  
    play C  
  end if  

END LOOP  

===============================================================================
EXPLANATION / RATIONALE

1.  Cooperative core  
    •  As long as everyone cooperates, GCC always plays C.  
    •  When all play C, the stock returns to capacity each round, yielding the maximum sustainable payoff.  

2.  Punishment of defection  
    •  If any player defects in round t–1, GCC defects for P consecutive rounds (or until the game ends, whichever is shorter).  
    •  P should be large enough to discourage a one‐shot defection but small enough to allow return to cooperation (we suggest P=2).  
    •  After P punishment rounds, if no new defection is observed, GCC resumes cooperation.  

3.  End‐game handling  
    •  In the final round (t = r) there is no future to protect, so GCC defects to maximize the one‐shot payoff.  
    •  Punishment timers never extend beyond the last round.  

4.  Robustness  
    •  No assumptions about shared signals or off‐equilibrium coordination.  
    •  Uses only publicly observed actions and the known remaining rounds.  
    •  Recovers from mistakes: after exactly P rounds of D it goes back to C if the group has returned to cooperation.  

5.  Edge cases  
    •  r = 2: then P = min(2, 0) = 0, so GCC cooperates in round 1 (t=1), defects in round 2 by the “last‐round” rule.  
    •  r = 3: P = min(2, 1) = 1 → if someone defects in round 1, we defect in round 2, then in round 3 we defect anyway as it’s last round.  
    •  Very large r: P stays at 2, balancing deterrence with forgiveness.  

This strategy is “cooperative” in that it maintains full cooperation and maximum sustainable stock whenever possible, yet it enforces a credible, finite punishment against any unilateral defection.
'''

description_COOPERATIVE_100 = '''
Below is a fully self-contained cooperative strategy (“GenTitForTat”) for the repeated common-pool game.  It uses simple tit-for-tat (punish one round, then forgive) to sustain cooperation, but it defects in the final round (since there is no future to incentivize cooperation there).

1.  Data structures and state  
    •  pun_remaining: integer ≥0, rounds of punishment still to serve (initially 0)  
    •  last_round_defections: integer, number of players (other than you) who defected last round (initially 0)  

2.  Decision rule for round t (1 ≤ t ≤ r):  
```
if t == r then
    # Final round: defect (no future incentive)
    action ← D
else if pun_remaining > 0 then
    # Serve punishment
    action ← D
    pun_remaining ← pun_remaining − 1
else if last_round_defections > 0 then
    # Detected defection last round → punish one round
    action ← D
    pun_remaining ← 1    # we will defect this round, then forgive
else
    # No recent defection → cooperate to sustain the stock
    action ← C
end if

return action
```

3.  Updating memory after observing all players’ moves in round t:  
```
last_round_defections ← number of opponents who chose D in round t
# pun_remaining is already decremented in the decision step above
```

4.  Explanation and rationale  
  •  First round (t=1): pun_remaining=0 and last_round_defections=0  
     → cooperate (C).  
  •  If everyone cooperates, pun_remaining stays 0 forever until the last round.  
  •  If any player defects in round t, then in round t+1 we set pun_remaining=1  
     → we defect exactly one round in retaliation, then return to cooperation.  
  •  Last round (t=r): always defect, since there is no future to enforce cooperation.  

5.  Cooperative mindset  
  – By default we cooperate (C), sustaining the stock at or near capacity.  
  – We only defect to “teach a lesson” when we see free-riding, but we immediately forgive  
    so as to re-establish high stock levels and mutual gains.  
  – Because defections are met with swift but short punishment, rational opponents best-respond  
    by cooperating in almost every round before the last.  

This strategy achieves near-maximal group payoff by locking in mutual cooperation for all rounds except the very last (where backward induction forces defection). It punishes deviations just enough to deter one-shot temptations, then returns to full cooperation.
'''

description_COOPERATIVE_101 = '''
Below is a simple “targeted one‐round punishment” strategy that (a) starts cooperatively, (b) punishes any defection by everyone exactly once in the very next round, then returns to full cooperation, and (c) defects in the last round to guard against end‐game free‐riding.  It requires only observing the last two rounds of play (plus knowing the total number of rounds r).

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
1.  Notation  
   •  t = current round, 1 ≤ t ≤ r  
   •  A_j(s) ∈ {C, D} = action of player j in round s  
   •  “AnyDef(s)” = true if ∃ j such that A_j(s)=D, else false  
   •  For convenience define AnyDef(0)=false  

2.  Core decision rule for rounds t=1…r:  
   if t = 1  
     play C  
   else if t = r  
     play D      // Last-round defection to protect against end-game  
   else if AnyDef(t–1) = true  AND  AnyDef(t–2) = false  
     play D      // punish any new defection, exactly one round  
   else  
     play C      // otherwise cooperate  

3.  Explanation of cases  
   •  Round 1: no history ⇒ cooperate.  
   •  Rounds 2…r–1:  
      –  If someone defected in t–1 but nobody had defected in t–2, then this round you defect once (a one‐shot punishment of the defector(s)).  
      –  In every other scenario (no recent defection, or you are “in the middle” of punishing), you cooperate.  That ensures you punish only one round per defection event, then immediately return to cooperation.  
   •  Round r: defect, because no future rounds remain for retaliation.  

4.  Why this is cooperative  
   •  If all players adopt it, no one ever defects (since a lone defection triggers a costly next‐round punishment), so stock stays at capacity each round and each round’s payoff is capacity/(2n).  
   •  A single defection is punished only once, limiting collateral damage to cooperators and allowing quick return to full cooperation.  
   •  By defecting in the very last round, you protect yourself against any “last‐move” free riders.  

5.  Pseudocode summary  

  initialize AnyDef(0) ← false  
  for t in 1..r do  
    if t == 1 then  
      play C  
    else if t == r then  
      play D  
    else if AnyDef(t–1) and not AnyDef(t–2) then  
      play D  
    else  
      play C  
    end  
    // after all players reveal, record AnyDef(t) = (∃ j: A_j(t)=D)  
  end  

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  

This strategy is simple to implement, enforces near‐optimal sustained cooperation, allows rapid forgiveness after a one‐round penalty, and guards against end‐game defection.
'''

description_COOPERATIVE_102 = '''
Below is a pure‐strategy, broadly reciprocal “tit-for-tat” style algorithm, augmented with limited punishment and an end-game adjustment.  Its goal is to keep the common pool near capacity by cooperating as long as others do, to deter one‐shot defection with a short punishment phase, but to “play the last move” (defect) when there is no future to protect.

–––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––
Name  
  Forgiving Tit-for-Tat with End-Game Defection

Parameters  
  • n ≥ 2   (number of players)  
  • r > 1   (total rounds)  
  • K ≥ 1   (punishment length, e.g. K = 2)

State variables (maintained by each player i)  
  pun_rounds_left ← 0    # remaining punishment rounds  
  saw_defection_last ← false

Initialize (before round 1)  
  pun_rounds_left ← 0  
  saw_defection_last ← false

On each round t = 1,2,…,r do
  1.  Observe: t, pun_rounds_left, saw_defection_last, remaining stock S_t  
  2.  Decide action a_i,t ∈ {C, D} as follows:

     if t = 1 then  
       a_i,t ← C         # start with cooperation

     else if t = r then  
       a_i,t ← D         # last round: no future punishment, defect for maximum payoff

     else if pun_rounds_left > 0 then  
       a_i,t ← D         # in punishment phase  
       pun_rounds_left ← pun_rounds_left − 1

     else  
       # normal reciprocity mode  
       if saw_defection_last then  
         # trigger punishment phase  
         pun_rounds_left ← K − 1   # we use K total D’s: this and the next K−1  
         a_i,t ← D
       else  
         a_i,t ← C               # nobody defected last turn → keep cooperating

  3.  Simultaneously all players choose and reveal their actions.  
  4.  Observe others’ actions; compute  
       saw_defection_last ← (∃ j: a_j,t = D).

End for

–––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––
Explanation

1.  First round (t=1) we always cooperate.  
2.  In each subsequent round before the last, if nobody defected in the immediately preceding round (“all-C”), we again play C.  
3.  If we detect at least one defection in round t−1, we switch to D for K consecutive rounds (including the very next round).  This “limited punishment” is harsh enough to deter isolated cheats but not so permanent as to forfeit the entire game’s surplus.  
4.  After K rounds of punishment, we reset and forgive, returning to cooperation if no fresh defections have occurred.  
5.  On the final round t=r we defect, because there is no future in which to enforce cooperation.  

Cooperative mindset  
  • As long as everyone cooperates (stock stays high), this strategy never defects, so the pool remains at or near capacity and each round’s per‐player payoff is S/(2n).  
  • A defection by any player immediately triggers enough retaliation to make short-term gain unattractive.  
  • Because punishments are limited (K rounds only), the group can “move on” after a single shock rather than collapse into perpetual defection.  
  • The only defection outside of a justified punishment is the last round, where “end-game” logic makes defection strictly dominant.  

Choice of K  
  –   K=1 degenerates to simple “tit-for-tat” (punish exactly one round).  
  –   K≥2 is usually safer to overcome noise or multi-player misreads.  
  –   You may tune K up to, say, ⌈r/4⌉ for very large r, but even K=2 or 3 is often enough logic in praxe.  

Pseudocode recap

  function choose_action(t, S_t):
      if t == 1:
          return C
      if t == r:
          return D
      if pun_rounds_left > 0:
          pun_rounds_left -= 1
          return D
      if saw_defection_last:
          pun_rounds_left = K - 1
          return D
      return C

  after observing actions in round t:
      saw_defection_last = (exists player j with action[j] == D)

Total payoff  
  Over r rounds you earn Σ_t π_i,t, and because mutual cooperation keeps S_t close to capacity, you capture steady S_t/(2n) each round except for brief punishment bouts.
'''

description_COOPERATIVE_103 = '''
Below is a simple “conditional cooperation” strategy (a multi‐player analogue of tit-for-tat, with one‐round memory, finite‐horizon adjustment, and forgiveness) that aims to sustain high stock levels and share the resource fairly.  

1. Key ideas  
  • Start by cooperating to build trust.  
  • Cooperate as long as nobody defected in the immediately preceding round.  
  • If any defection is observed, punish by defecting once, then immediately forgive (return to cooperation) provided no further defections occur.  
  • In the very last round, defect (because there is no future to protect).  

2. Decision rules in words  
  Round t = 1:  
    Play C.  

  For 1 < t < r:  
    If (in round t–1) every player chose C, then play C.  
    Else (i.e. ≥1 defector last round), play D this round (punishment), but plan to return to cooperation in round t+1 so long as no new defectors appear in round t.  

  Round t = r (last round):  
    Play D.  

3. Handling edge cases  
  • First round has no history ⇒ cooperate.  
  • If stock S ever falls to 0, payoffs are zero; from then on everyone playing C or D yields zero growth. Our rule still prescribes cooperation until round r, but the stock can’t recover.  
  • Only one round of punishment (no endless “grim trigger”), to avoid lock‐ins of mutual defection.  
  • Last‐round defection is unavoidable under backward induction; by defecting we protect ourselves from being exploited in that final knife‐edge.  

4. Pseudocode  

Let history[t–1] be the vector of actions of all n players in the previous round.  
For t = 1 to r do:  
  if t == 1 then  
    action[t] := C  
  else if t == r then  
    action[t] := D  
  else  
    if round t–1 exists and ∀i: history[t–1][i] == C then  
      action[t] := C      # no one defected last round ⇒ cooperate  
    else  
      action[t] := D      # punishment for any defection last round  
    end if  
  end if  
end for  

5. Why this is cooperative  
  • By default it cooperates, preserving stock and sharing the harvest (each round S/(2n)).  
  • A one‐round punishment deters free‐riding without permanently destroying cooperation.  
  • Forgiveness ensures that a single defection—perhaps by a mistaken or experimental opponent—doesn’t trigger an endless death spiral.  
  • Although we must defect on the last move, all earlier rounds can sustain high stocks near capacity, maximizing joint returns over r–1 rounds.
'''

description_COOPERATIVE_104 = '''
Below is a single‐strategy proposal, called “Multi-Lateral Tit-for-Tat with End‐Game Defection.”  It is simple, fully specified, punishes uncooperative play but forgives after one round, and deals explicitly with the first and last rounds.

1.  Overview  
    •  Cooperate (C) whenever all opponents cooperated in the immediately preceding round.  
    •  Defect (D) whenever at least one opponent defected in the immediately preceding round.  
    •  Exception 1: Round 1 has no history → Cooperate.  
    •  Exception 2: Round r (the last round) → Defect.  

    Rationale  
    –  The round-by-round “if you defected last time, I defect this time; otherwise I cooperate” rule maintains high cooperation in equilibrium.  
    –  Forgiveness after one round allows the group to return to full cooperation (stock stays near capacity).  
    –  By defecting in the last round, you maximize your final payoff (no future stock to preserve).  

2.  Detailed Decision Rules

    Let t = current round (1 ≤ t ≤ r).  
    Let H(t–1) be the profile of all players’ actions in round t–1.  
    Define DefectedPrev = “at least one player chose D in H(t–1).”

    DecisionRule(t, H(t–1)):

      if t == 1:
        play C
      else if t == r:
        play D
      else if DefectedPrev:
        play D
      else
        play C

3.  Pseudocode

    function choose_action(t, history, r):
      # history is a list of length t–1, each element is a vector of n actions
      if t == 1:
        return “C”
      if t == r:
        return “D”
      # check last round’s actions
      last_actions = history[t–2]   # zero-based indexing
      if “D” in last_actions:
        return “D”
      else:
        return “C”

4.  Edge Cases

    a) First Round (t=1):  
       history is empty.  By convention we begin cooperatively to signal our intent.  

    b) Last Round (t=r):  
       No future payoffs remain, so we defect to maximize the one-shot gain.  

    c) A single defection in any non-terminal round:  
       Triggers exactly one round of punishment (we defect in the immediately following round) and then return to cooperation provided no new defections occur.  

    d) Stock near zero:  
       Both C and D yield zero payoff, so our rule still applies—if no one defected last round we “cooperate” (harmless) in anticipation of possible group recovery; if someone defected, we “defect.”  

5.  Cooperative Mindset

    –  By default we maintain full cooperation (C) to keep the common pool at or near capacity, securing the largest sustainable payoffs over r – 1 rounds.  
    –  We never escalate punishment: a single lapse by one player leads to exactly one round of mutual defection, after which we forgive and restore cooperation.  
    –  This balance of clear incentive to cooperate and finite, proportional punishment deter persistent over-harvesting while ensuring the resource regenerates.  

With this strategy, if all players adopt it, they will cooperate in rounds 1…r–1, keeping the stock near capacity and each earning S/(2n) each round, and then defect in round r.  Any unilateral deviation is immediately punished for one round and thereafter forgiven, preventing stock collapse and sustaining cooperation.
'''

description_COOPERATIVE_105 = '''
Below is a single‐agent strategy that (1) sustains full cooperation on the common pool for as long as possible, (2) punishes defections just enough to deter exploitation, and (3) accepts that in the very last round there is no future to protect and therefore defects to maximize final‐round payoff.  In all other respects it behaves like classic Tit‐for‐Tat.

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
Strategy name:  Coop-TFT-Endgame  
––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  

Parameters (known to you):  
  • n = number of players  
  • r = total rounds  
  • capacity = maximum sustainable stock  

State you keep track of:  
  • history of all players’ actions in each past round  
  • (optional) stock level S_t each round—only used for bookkeeping, not for decision.  

High‐level description:  
  1. Round 1: Cooperate.  
  2. Rounds 2 through r–1:  
       – If in the immediately preceding round EVERY player cooperated, then Cooperate.  
       – Otherwise (at least one defection last round), punish by Defect for exactly one round, then revert to cooperation.  
  3. Round r (the very last round): Defect—there is no future payoff to protect.  

Rationale:  
  • By starting with C and mirroring any defection only one round, you create a shadow of future punishment that deters others from defecting.  
  • You never get locked into permanent punishment (as in Grim Trigger), so even after a mistake or noise, cooperation can quickly be restored.  
  • You preserve the common pool at capacity (or near it) for as many rounds as possible, thus maximizing total group payoff.  
  • In the last round you defect to capture the larger immediate share when future rounds cannot reward cooperation.  

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
Pseudocode  
––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  

state:  
  last_round_allC  ← true       // assume cooperation before round 1  
  punish_counter  ← 0           // how many remaining rounds to punish  

for t in 1..r:  
  if t == 1:  
    action_t  ← C  
  else if t == r:  
    action_t  ← D             // endgame defect  
  else if punish_counter > 0:  
    action_t  ← D             // still punishing  
    punish_counter ← punish_counter – 1  
  else if last_round_allC == true:  
    action_t  ← C             // continue cooperation  
  else:                         // observe at least one defection last round  
    action_t  ← D             // punish for exactly one round  
    punish_counter ← 1  

  play action_t  

  // AFTER actions are publicly revealed, update state for next round  
  observe others’ actions in round t  
  if (all n players chose C in round t):  
    last_round_allC ← true  
  else:  
    last_round_allC ← false  

end for  

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
Edge‐case handling  
––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
• First round (t=1): by convention we can’t “punish,” so we start with C.  
• Middle rounds (1<t<r): we use Tit‐for‐Tat with one‐round punishment.  
• Last round (t=r): no future, so defect.  

Notes on cooperative mindset:  
• This strategy only defects to punish an observed defection and never over‐punishes—cooperation can resume immediately.  
• By mirroring cooperation, it helps keep the stock at or very near capacity, securing maximal per‐round payoffs for all.  
• It avoids the collapse of the resource that would come from unrestrained or permanent punishment.  

In tournament play, Coop-TFT-Endgame will broadly sustain mutual cooperation and defend itself against sustained exploitation, while still claiming the final‐round advantage when no future reward for cooperation remains.
'''

description_COOPERATIVE_106 = '''
Below is a single‐agent “cooperative” strategy that (1) aims to keep the common pool near its sustainable maximum, (2) starts out fully cooperative, (3) punishes defections but forgives after a short time, and (4) handles end‐game and low‐stock emergencies.

— — —  
STRATEGY NAME  
“Thresholded Tit‐for‐Tat with Short Punishment” (TTSP)

PARAMETERS (tunable):  
• punishment_length L (e.g. 1 or 2 rounds)  
• low_stock_threshold θ⋆ (fraction of capacity, e.g. 0.2)  

STATE VARIABLES:  
• pun_counter ∈ {0,1,…,L}  // rounds left to punish  
• last_round_defected? ∈ {true,false}

INITIALIZATION (before round 1):  
pun_counter ← 0  
last_round_defected? ← false

DECISION RULE (at the beginning of each round t, given current stock S_t and full history):  
1.  If t = 1 then  
  Play C.  
2.  Else if S_t < θ⋆·capacity then  
  // Pool is critically low ⇒ secure one’s own payoff  
  Play D.  
3.  Else if pun_counter > 0 then  
  // We are in punishment mode  
  Play D  
  pun_counter ← pun_counter – 1  
4.  Else if last_round_defected? = true then  
  // Trigger a short punishment  
  Play D  
  pun_counter ← L – 1    // we count this round as the first of L  
5.  Else  
  // No pending punishment and no recent defections  
  Play C  

AFTER OBSERVING ACTIONS IN ROUND t (to set up for t+1):  
• If any opponent played D in round t AND S_t ≥ θ⋆·capacity then  
  last_round_defected? ← true  
  else  
  last_round_defected? ← false  

EDGE CASES:  
• Last round (t = r):  
 – If pun_counter > 0 or last_round_defected? = true then defect (D) to complete any punishment.  
 – Else if S_r < θ⋆·capacity defect (D) to secure payoff.  
 – Otherwise cooperate (C) even in the last round, to preserve the pool if it can regrow (and to reward mutual cooperators).  

• If capacity is very large and you never see a defection, you will play C in every round, holding the stock near capacity and earning π_i = S/(2n) each time.  
• If a single defection occurs when the stock is healthy, you defect for L rounds (a “short grim‐trigger”), then revert to cooperation if no further defections occur.  
• If the stock ever falls below θ⋆·capacity, everyone playing around this strategy will switch to D “for survival” but, once the pool regrows above θ⋆·capacity, will resume mutual cooperation.  

RATIONALE:  
– By cooperating whenever the pool is healthy and no one has recently defected, we sustain the maximum‐possible stock (and so the largest long‐run π).  
– Short punishments deter unilateral defection but forgive quickly, so a single mistake need not trigger permanent tragedy.  
– The low‐stock cutoff prevents you from starving yourself when the pool is nearly exhausted.  
– By optionally cooperating in the final round when there is no queue of punishments, you show good faith and maximize any possible regrowth payoff.

PSEUDOCODE

```
Inputs: capacity, n, r, θ⋆, L
State: pun_counter = 0, last_def = false

for t in 1..r:
    observe S_t
    if t == 1:
        action = C
    else if S_t < θ⋆*capacity:
        action = D
    else if pun_counter > 0:
        action = D
        pun_counter -= 1
    else if last_def == true:
        action = D
        pun_counter = L - 1
    else:
        action = C

    submit action

    // after seeing all players’ actions this round:
    if (any opponent did D in round t) and S_t ≥ θ⋆*capacity:
        last_def = true
    else:
        last_def = false

    // Special last‐round rule (optional, can be folded into above):
    if t == r:
        if pun_counter>0 or last_def or S_t<θ⋆*capacity:
            action = D
        else:
            action = C
        break
```

Tune θ⋆ (e.g. 0.2–0.3) to balance patience vs. self‐preservation, and L (e.g. 1–2) to calibrate punishment severity. This strategy is fully “cooperative” in that it maintains the pool at high stock, forgives mistakes, but still deters free‐riding.
'''

description_COOPERATIVE_107 = '''
Below is a simple “trigger‐and‐forgive” strategy—essentially a multi‐player Tit-for-Tat—that (i) cooperates whenever nobody defected in the immediately preceding round, (ii) punishes by one round of defection if any defection is observed, (iii) then returns to cooperation, and (iv) always defects in the known final round (since the one-shot Nash equilibrium is D).  

1.  State variables  
    •  t ∈ {1,…,r}: current round  
    •  history: list of action‐profiles from past rounds  

2.  Decision rule (pseudocode)  
    function CHESS_Player(t, history):  
        if t == 1:  
            // First round: build cooperation  
            return C  
        if t == r:  
            // Last round: one‐shot Nash  
            return D  
        // For rounds 2 through r–1:  
        let last_actions = history[t–1]  
        if ∃ player j≠me such that last_actions[j] == D then  
            // Punish any defection by defecting once  
            return D  
        else  
            // No defection last round → cooperate  
            return C  

3.  Explanation of why this is cooperative  
    •  On the equilibrium path (nobody ever defects), all players will forever play C until round r, sustaining the stock at or near capacity.  
    •  A single defector is met by exactly one round of punishment from everyone; thereafter, cooperation is restored if no further defections occur.  
    •  This limited‐punishment rule is forgiving (avoids permanent breakdown) yet credible: it deters profitable one‐off defections by imposing an immediate one‐round payoff loss on the deviator.  

4.  Handling edge cases  
    –  Round 1: No history exists → start with C to signal willingness to cooperate.  
    –  Round r (last round): we know defection is dominant → play D.  
    –  Stock exhaustion (S_t = 0): both C and D yield zero consumption—our rule still applies, but payoffs are zero.  
    –  Multiple simultaneous defectors: we don’t distinguish—any D in last round triggers the one‐round collective punishment.  

5.  Properties  
    –  Simple to implement; only one‐round memory needed.  
    –  Enforces high long‐run stock levels, maximizing group payoff.  
    –  Forgiving enough to recover after accidental or malicious deviation.  

This strategy will do well in a mixed‐tournament: it reaps the benefits of mutual cooperation, punishes free‐riders just enough to keep them in check, and rapidly returns to cooperation to avoid needless resource collapse.
'''

description_COOPERATIVE_108 = '''
Below is a simple “grim‐trigger with last‐round defection” strategy that (a) tries to keep the pool near capacity by cooperating as long as no one defects, (b) punishes any defection by defecting thereafter, and (c) exploits the fact that there is no future payoff after the last round by defecting in round r.

1.  Data structures and state  
    •  defect_detected: Boolean flag, initially false  
    •  r: total number of rounds  
    •  t: the current round (1 ≤ t ≤ r)  

2.  Decision rule for player i in round t:  
    if t == r then  
       // Final round: no future punishment possible, so defect  
       play D  
    else if defect_detected == true then  
       // Someone has defected previously → punish forever  
       play D  
    else  
       // No defection seen yet and not last round → cooperate  
       play C  

3.  Updating defect_detected after each round:  
    After observing the action profile (a₁,…,a_n) in round t,  
    if any a_j == D (j≠i) then  
       defect_detected ← true  

4.  Edge‐case behavior  
   – t=1: defect_detected is false and t≠r, so we play C.  
   – t=r: always play D. This extracts the one‐shot advantage when there is no future.  
   – If at any point in t<r we see someone defect, defect_detected flips to true and we defect for all subsequent rounds (including round r, although we would defect there anyway).  

5.  Why this is cooperative  
   – As long as everyone cooperates, the pool stays at capacity (see example 1), maximizing future payoffs for all.  
   – A single defection by anyone immediately triggers mutual defection thereafter, so no one can profit long‐term at the expense of the group.  
   – The threat of permanent punishment deters defection in early and middle rounds.  
   – Defecting in the last round is individually optimal (no future penalty) but does not undermine the pool’s sustainability during the cooperative phase.  

Pseudocode summary:  
```
initialize defect_detected ← false
for t in 1..r do
  if t == r then
    action_i[t] ← D
  else if defect_detected then
    action_i[t] ← D
  else
    action_i[t] ← C

  // After everyone announces action in round t:
  if exists j ≠ i with action_j[t] == D then
    defect_detected ← true
end for
```
This strategy is simple, forgiving only so long as everyone cooperates, and it preserves the resource in all but the un‐punish-able last round.
'''

description_COOPERATIVE_109 = '''
Below is a complete “tit-for-group‐punishment” strategy that (i) sustains full cooperation as long as everyone has cooperated in the past, (ii) punishes any observed defection by defecting for a short, fixed number of rounds, then returns to cooperation, and (iii) defects in the final round (where there is no future to protect).

––––––––––––––––––––––––––––––––––––––––––––––––––––  
STRATEGY OVERVIEW  
––––––––––––––––––––––––––––––––––––––––––––––––––––  
State variables (maintained by each player i):  
  • “phase” ∈ {Cooperate, Punish, Endgame}  
  • punish_counter ∈ {0,1,…,P}  (remaining punishment rounds)  

Parameters (common knowledge):  
  • P = 1  (length of punishment; you can choose P≥1)  

Phases:  
  1) Cooperate: presume everyone is cooperating; choose C.  
  2) Punish: short, focused retaliation after any defection; choose D until punish_counter hits 0.  
  3) Endgame (round t = r): defect because no future.  

––––––––––––––––––––––––––––––––––––––––––––––––––––  
DETAILED DECISION RULES  
––––––––––––––––––––––––––––––––––––––––––––––––––––  

Initialize (before round 1):  
  phase ← Cooperate  
  punish_counter ← 0  

For each round t = 1,...,r do:

  if t = r then  
    // Final round → no future to protect  
    phase ← Endgame  
  end if

  Action selection:  
    if phase = Cooperate then  
      play C  
    else if phase = Punish then  
      play D  
    else if phase = Endgame then  
      play D  
    end if

  After everyone’s actions in round t are publicly observed:  
    let Defections_t = { j : j’s action in round t = D }  

    // Transition logic:
    if phase = Endgame then  
      // stay in Endgame until game ends  
      phase ← Endgame  

    else if phase = Punish then  
      // decrement counter  
      punish_counter ← punish_counter – 1  
      if punish_counter = 0 then  
        // if punishment just finished—and no new defection last round—return to Cooperate  
        // if a defection happened in the just-punished round, reset counter  
        if |Defections_t| > 0 then  
          punish_counter ← P  
          phase ← Punish  
        else  
          phase ← Cooperate  
        end if  
      else  
        phase ← Punish  
      end if  

    else if phase = Cooperate then  
      // if anyone defected, trigger punishment  
      if |Defections_t| > 0 then  
        phase ← Punish  
        punish_counter ← P  
      else  
        phase ← Cooperate  
      end if  
    end if

end for  

––––––––––––––––––––––––––––––––––––––––––––––––––––  
RATIONALE & PROPERTIES  
––––––––––––––––––––––––––––––––––––––––––––––––––––  

1) First round: phase = Cooperate ⇒ play C.  
2) As long as all players choose C, we remain in Cooperate and continue to play C every round (maintaining the stock at capacity).  
3) The moment any player plays D, we enter Punish. We play D for P rounds (here P=1), inflicting a brief “group punishment.”  
   • During punishment we defect regardless of what others do.  
   • If someone still defects during our punishment round, we renew punishment.  
   • Otherwise we return to Cooperate.  
4) In the very last round (t=r), we switch to Endgame and play D for the final payoff.  
   • This is individually rational in a finite repeated game with no future incentive.  
5) By making punishments short and forgiving, we avoid endless feuds while credibly deterring one‐shot defection.  

––––––––––––––––––––––––––––––––––––––––––––––––––––  
PSEUDOCODE SUMMARY  
––––––––––––––––––––––––––––––––––––––––––––––––––––  

Parameters:  
  P = 1  

State:  
  phase ∈ {Cooperate, Punish, Endgame}  
  punish_counter ∈ ℕ  

Initialize:  
  phase ← Cooperate  
  punish_counter ← 0  

For t in 1..r:  
  if t = r:                     // enter final‐round mode  
    phase ← Endgame  

  if phase = Cooperate:  
    a_i ← C  
  else:  // Punish or Endgame  
    a_i ← D  

  Observe all players’ actions → set Defections_t  

  if phase = Endgame:  
    phase ← Endgame

  else if phase = Punish:  
    punish_counter ← punish_counter − 1  
    if punish_counter = 0:  
      if |Defections_t| > 0:  
        punish_counter ← P  
        phase ← Punish  
      else:  
        phase ← Cooperate  
      end if  
    else:  
      phase ← Punish  
    end if

  else if phase = Cooperate:  
    if |Defections_t| > 0:  
      punish_counter ← P  
      phase ← Punish  
    else:  
      phase ← Cooperate  
    end if

End For  

––––––––––––––––––––––––––––––––––––––––––––––––––––  
This strategy is fully cooperative whenever possible, delivers symmetric payoffs, punishes defection credibly but briefly, and correctly defects in the doomed final round.
'''

description_COOPERATIVE_110 = '''
Below is a single‐player decision rule (“strategy”) that seeks to sustain full cooperation (everybody playing C) throughout most of the r-round game, but that also punishes one or more defectors briefly if they ever break the cooperative norm.  It never defects preemptively, always “starts nice,” and always “gives up the grudge” after a short punishment.  In testing tournaments it will earn the cooperative stream of payoffs whenever everyone else is cooperating, will deter occasional defection by others, and will quickly return to cooperation rather than spiral into mutual defection.

1.  “High-level” description  
   – First move: Cooperate (C).  
   – As long as no one defected in the previous round, play C.  
   – If you observe at least one defection by somebody last round, switch to defect (D) for exactly P consecutive rounds (including the current one) to punish.  
   – After you have punished for P rounds, forgive: return to C as long as no new defection has occurred.  
   – (Optionally) to avoid an all-out “last-round rush,” you can declare the very last round (round r) an automatic C, but this is not strictly necessary if P≪r.

   Here P is a small integer (e.g. P=1 or 2).  We recommend P=1 (standard Tit-for-Tat style) or P=2 (a slightly harsher but still forgiving punishment).

2.  Pseudocode  

   Parameters:  
     P  ← punishment length (integer ≥1, e.g. 1 or 2)  
     r  ← total number of rounds  

   State variables (maintained across rounds):  
     pun_timer ← 0       # “how many more rounds to punish”  

   Procedure for each round t = 1,2,…,r:
     if t = 1 then
       action ← C
     else if pun_timer > 0 then
       action ← D
       pun_timer ← pun_timer − 1
     else 
       # No pending punishment
       if (in round t−1 at least one player played D) then
         # Trigger a fresh punishment of length P
         action ← D
         pun_timer ← P − 1
       else
         action ← C
       end if
     end if

     # (Optional) override for final round to guarantee cooperation
     if t = r then
       action ← C
     end if

     play(action)

   End procedure

3.  Rationale & edge-case handling  
   • First round: We have no history, so we start by cooperating (C).  
   • Sustaining cooperation: If everyone cooperated last round, we continue to cooperate, keeping the common pool near full capacity.  
   • Punishment: The very next round after we see any D, we play D ourselves, and we continue to play D for a total of P rounds (this is our “punishment window”).  This punishes any defection, raises the cost of unilateral cheating, but does not condemn cooperators harshly.  
   • Forgiveness: After P rounds of D, we reset pun_timer to zero and go back to C, giving the group a fresh chance to restore full cooperation.  
   • Final round: In a known finite-horizon game, defectors may try to rush harvest at the end.  By optionally forcing C in round r we protect the last bit of stock—but even without that rule, most of our punishments will have fired before the very end if P≪r.  

This strategy is individually simple to implement, yields the payoff cap/(2n) in every round as long as all players follow it, and handles one-off defections by short punishment rather than perpetual grim retaliation.  In a tournament of independent LLM strategies it will reward other cooperators, punish defection swiftly, and then return to cooperation—exactly the behavior required to sustain high group payoffs in this repeated common-pool resource game.
'''

description_COOPERATIVE_111 = '''
Below is a “cooperative‐minded” strategy that (i) aims to sustain full cooperation as long as nobody defects, (ii) punishes defection briefly, and (iii) defects in the last round (since there is no future to protect). We call it Forgiving Tit-for-Tat with End-Round Defection (FTFT-ERD).

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
I. Intuition  
1. Round 1: Trust everyone and cooperate.  
2. Thereafter, if everyone cooperated last round, continue cooperating.  
3. If you see at least one defection last round, defect for M consecutive rounds as punishment, then forgive and return to cooperation (unless punished again).  
4. In Round r (last round), defect to maximize one-shot gain (no future to protect).  

Choosing M=1 reduces to classic Tit-for-Tat with a one‐round punishment. You can pick M larger (e.g. M=2) to raise the cost of defection.  

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
II. Pseudocode  

Parameters:  
  n, r, capacity  … as given.  
  M = 1  # length of punishment phase  

State variables (maintained across rounds):  
  punish_remaining ← 0   # counts down rounds of punishment  

For each round t = 1, 2, …, r do:  
  if t == 1 then  
    action ← C                                           # start by cooperating  
  else if t == r then  
    action ← D                                           # last round: defect  
  else if punish_remaining > 0 then  
    action ← D                                           # still punishing  
    punish_remaining ← punish_remaining − 1  
  else if (in round t−1) ∃ any player j who played D then  
    # trigger punishment  
    punish_remaining ← M − 1     # you will defect this round and M−1 more  
    action ← D  
  else  
    action ← C                                           # everyone cooperated last round  
  end if  

  Play action in round t.  
  Observe all players’ actions and payoffs.  
end for  

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
III. Handling Edge Cases  

1. Stock depletion:  
  If the common‐pool stock S becomes 0 before Round r, everyone’s immediate payoff is 0 whether you “cooperate” or “defect.” In practice the above rule still applies—treated as D if you’re punishing or it’s the last round, C otherwise (but payoff=0).  

2. Ties in “any defection”:  
  We don’t distinguish who defected or how many. A single defector triggers the same brief punishment.  

3. Choice of M:  
  M=1 implements strict Tit-for-Tat. M>1 yields a harsher (but still forgiving) punishment.  

4. Final round:  
  Defection is dominant when there is no future. We therefore defect in round r, but this does not retroactively affect incentives earlier because future cooperation cannot be protected in a one‐shot.  

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
IV. Why This Is Cooperative  

• We never defect first (Round 1 is C).  
• We only defect to punish observed defection, then return to cooperation.  
• We avoid permanently collapsed cooperation (we forgive after M rounds).  
• We sustain maximum possible stock levels by coordinating on universal C whenever everyone has been “good.”  
• The only defections you’ll see: very short punishments and a final‐round defection (unavoidable one‐shot incentive).  

In head-to-head with another FTFT-ERD player both will play C in all rounds 1…r−1 and only defect in round r, thereby harvesting the full sustainable path of payoffs.
'''

description_COOPERATIVE_112 = '''
Below is a fully specified n-player “conditional tit-for-tat” strategy.  It (1) Always starts by cooperating, (2) punishes any “new” defection exactly one round, (3) then immediately forgives, (4) always defects in the last round, and (5) if the common-pool falls below a critical threshold, it temporarily suspends punishment to help rebuild the stock.

––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
Notation  
  n       number of players  
  r       total rounds  
  t       current round (1 ≤ t ≤ r)  
  capacity  common-pool capacity  
  S_t     stock at the beginning of round t  
  a_{j,t} the action of player j in round t (“C” or “D”)  
  a_i     our action in the current round  
––––––––––––––––––––––––––––––––––––––––––––––––––––––––  

Parameters you choose once at the start  
  threshold_min ← capacity/4  
     // below this stock we “forgive” punishments to rebuild the pool  

State variable (per player)  
  last_was_punish ∈ {true, false}  
     // tracks whether our own last round move was a punishment defection  

Initialization (before round 1)  
  last_was_punish ← false  

Strategy Pseudocode  

for t in 1…r do  
  if t == 1 then  
    // First round: unconditionally cooperate  
    a_i ← C  
    last_was_punish ← false  

  else if t == r then  
    // Last round: one-shot endgame defection  
    a_i ← D  
    last_was_punish ← false  

  else if S_t < threshold_min then  
    // Resource is critically low: rebuild by cooperating  
    a_i ← C  
    last_was_punish ← false  

  else  
    // General case: conditional tit-for-tat  
    // Check if there was any “new” defection by others in t–1  
    let someone_defected_prev ← (∃ j ≠ i : a_{j,t–1} == D)  

    if someone_defected_prev == true  
       and last_was_punish == false then  
      // We detected a defection in a “cooperation phase” round → punish now  
      a_i ← D  
      last_was_punish ← true  

    else  
      // Otherwise stay in cooperation mode  
      a_i ← C  
      last_was_punish ← false  

  end if  

  play a_i  
  observe all a_{j,t} and payoffs; next round with updated S_{t+1}  
end for  

––––––––––––––––––––––––––––––––––––––––––––––––––––––––  

Explanation of the key features  
1.  Opening move: start cooperating to establish goodwill.  
2.  Tit-for-tat style: any defection you observe in a “normal” round triggers exactly one D in the very next round.  
3.  Finite punishment: after that one round of D you revert immediately to C, so you don’t get stuck in endless mutual punishment.  
4.  Resource-threshold forgiveness: if the common pool ever falls below capacity/4, you override punishments and cooperate to help the stock recover.  
5.  Last-round defection: as in standard repeated games, you defect in round r (endgame).  

This strategy is clearly cooperative, enforces accountability for one‐shot defections, quickly forgives so cooperation can resume, and protects the resource when it is close to exhaustion.
'''

description_COOPERATIVE_113 = '''
Here is a simple, forgiving “tit-for-tat with limited punishment” strategy tailored for this common‐pool resource game.  It is designed to (i) sustain full cooperation on the resource as long as no one defects, (ii) punish any defection just long enough to remove the one‐shot temptation, then forgive and return to cooperation, and (iii) guard against last‐round exploitation.

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
1.  Parameters  
   n   = number of players  
   r   = total rounds (r > 1)  
   L   = punishment length in rounds (we suggest L = 2)  
––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  

2.  Memory variables (per player)  
   punishingRemaining ← 0    # how many more rounds I will defect as punishment  
   lastRoundDefected ← false # did I observe any D in the immediately previous round?  

3.  Decision rule for round t = 1,…,r  

   if t = 1 then  
     action ← C        # no history ⇒ start by cooperating  

   else if t = r then  
     action ← D        # last round ⇒ defect to avoid being exploited  

   else if punishingRemaining > 0 then  
     action ← D  
     punishingRemaining ← punishingRemaining – 1  

   else if lastRoundDefected = true then  
     # someone defected last round ⇒ begin a punishment phase of L rounds  
     action ← D  
     punishingRemaining ← L – 1  

   else  
     action ← C        # no defection to punish ⇒ cooperate  

4.  After everybody reveals actions in round t:  
   lastRoundDefected ← (∃ j such that player j played D in round t)  

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
Explanation of key features  
1. First round cooperate: establishes the spirit of mutual restraint.  
2. Limited punishment (L rounds): deters a one‐shot defection by making its net gain negative, yet forgives quickly so that a single slip does not spiral into permanent breakdown.  
3. Always defect in the final round: standard end‐game defense so you are not left the sucker if others exploit you when there is no future.  
4. Simple memory (just “was there any D last round?” and “how many punishments remain?”): easy to implement and robust to noise.  

With this rule set, if everybody adopts it:  
– No one ever defects ⇒ stock stays at capacity ⇒ each round’s payoff = capacity/(2n).  
– A unilateral defection in any round triggers exactly L rounds of defection by all, driving down the resource and punishing the deviator.  
– After punishment, mutual cooperation resumes.  

This achieves sustained high payoffs through cooperation, makes a single defection unprofitable, and limits the severity of punishment to restore cooperation quickly.
'''

description_COOPERATIVE_114 = '''
Below is a simple “forgiving tit-for-tat with end‐game defection” strategy.  It achieves high long‐run cooperation, punishes one‐round defections, forgives quickly, and explicitly handles first and last rounds.

1. State variables  
   • punish_counter ← 0  
     (counts how many remaining rounds you will punish)  

2. Decision rule for round t = 1,…,r  
   if t == 1 then  
     action ← C  
     ▷ Always start by cooperating  
   else if t == r then  
     action ← D  
     ▷ In the very last round, defect (no future to reward cooperation)  
   else if punish_counter > 0 then  
     action ← D  
     punish_counter ← punish_counter – 1  
     ▷ Carry out a one‐round punishment of defection  
   else if any player j ≠ you chose D in round t–1 then  
     action ← D  
     punish_counter ← 1  
     ▷ Trigger one round of punishment (including yourself)  
   else  
     action ← C  
     ▷ If nobody defected last round and you are not punishing, cooperate  

3. Explanation of how it behaves  
   • First round: C — signals willingness to cooperate.  
   • Cooperate as long as everyone cooperated in the previous round.  This keeps the stock near capacity and maximizes joint payoffs.  
   • If you observe any defection in round t–1, you defect in round t (“punishment”) exactly one round, then return to cooperation.  A brief, predictable punishment deters free‐riding but forgives mistakes.  
   • Last round: D — standard backward‐induction step.  Since no future remains, you take the larger immediate share.  

4. Pseudocode  

  initialize punish_counter ← 0  
  for t in 1…r do  
    if t == 1 then  
      play C  
    else if t == r then  
      play D  
    else if punish_counter > 0 then  
      play D  
      punish_counter ← punish_counter – 1  
    else if “somebody defected in round t–1” then  
      play D  
      punish_counter ← 1  
    else  
      play C  
    end if  
  end for  

This strategy is cooperative in that it maintains full cooperation whenever possible, imposes only a one‐round penalty on defectors, and quickly restores cooperation.  The explicit last‐round defection acknowledges the finite horizon while preserving cooperation throughout almost all of the game.
'''

description_COOPERATIVE_115 = '''
Below is a simple “conditional‐cooperation” strategy that (1) aims to keep the stock at or near capacity by mutual cooperation, (2) punishes any one‐period defection just long enough to deter it, and (3) defaults to defection in the very last round (the usual backward‐induction outcome).  It makes no assumptions about hidden signals or off‐path agreements—only on what everyone sees in the publicly observable history.

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
Strategy name: TFT–1 (Tit‐for‐Tat with one‐period punishment)  
––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  

1.  Data you observe at the start of round t:  
    •  Round number t (1 ≤ t ≤ r)  
    •  Common‐pool stock S_{t} (after regrowth from previous round)  
    •  Actions a_{i,t–1} of every player in the previous round (only for t>1)  

2.  State variable:  
    punish_counter (initially 0)  

3.  Decision rules:  

   ––––––––––––––––––––––––––––––––––––––––––––––––––––––  
   A.  First round (t = 1):  
       Action ← C  (cooperate)  
       punish_counter ← 0  
   ––––––––––––––––––––––––––––––––––––––––––––––––––––––  

   B.  Intermediate rounds (2 ≤ t < r):  
       If punish_counter > 0 then  
         Action ← D  
         punish_counter ← punish_counter − 1  
       else if ∃ j such that a_{j,t–1} = D then  
         // someone defected last round → punish once  
         Action ← D  
         punish_counter ← 1  
       else  
         // everyone cooperated last round → cooperate  
         Action ← C  
       end if  
   ––––––––––––––––––––––––––––––––––––––––––––––––––––––  

   C.  Last round (t = r):  
       Action ← D  
       // Rational defection in the final round  
   ––––––––––––––––––––––––––––––––––––––––––––––––––––––  

4.  Rationale / cooperative alignment  
   •  By starting with C and returning to C as soon as everyone has “paid” the one‐round punishment, we sustain cooperation and keep the stock high.  
   •  A single defection triggers just one round of mutual defection, which is enough to make unilateral defection less attractive.  
   •  Because you resume cooperation immediately, the stock rebounds quickly (due to regrowth) and group payoffs stay high.  
   •  In the final round, pure self‐interest dictates D, but by punishing and repairing early, you maximize total payoffs in rounds 1…(r–1).  

5.  Pseudocode  

   initialize punish_counter ← 0  
   for t in 1,…,r do  
     observe S_t  // current stock  
     if t = 1 then  
       play C  
     else if t = r then  
       play D  
     else  // 2 ≤ t < r  
       if punish_counter > 0 then  
         play D  
         punish_counter ← punish_counter − 1  
       else if “any player played D in round t–1” then  
         play D  
         punish_counter ← 1  
       else  
         play C  
       end if  
     end if  
     // Observe everyone’s actions this round; they inform punish_counter next turn  
   end for  

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
This strategy is “cooperative” in that it:  
1. Starts by cooperating, giving everyone a strong opening payoff.  
2. Only punishes exactly one round whenever someone deviates, then immediately forgives.  
3. Keeps the stock high via almost‐constant cooperation, so group payoffs stay large.  
4. Ends with defection in round r (the unique subgame‐perfect move in a finite game), but by then the bulk of total payoffs has already been secured.
'''

description_COOPERATIVE_116 = '''
Below is a single‐strategy proposal—call it “Finite-Punishment Tit-for-Tat”—that (i) by default cooperates to keep the pool at its carrying capacity, (ii) punishes detected defectors for a short, finite number of rounds, and (iii) defects in the last round when no future remains.  

1.  Key ideas  
    a.  Cooperate (harvest S/(2n)) whenever history gives no reason to punish.  
    b.  If any player defected (harvested S/n) in the immediately preceding round, enter a punishment mode of fixed length P, during which you defect.  
    c.  After punishing for P rounds, forgive and return to cooperation—this limits collateral damage to the stock.  
    d.  In the last round (t = r), unilaterally defect (no future incentive to cooperate).  

2.  Parameters  
    n      number of players  
    r      total rounds  
    P      punishment length in rounds (e.g. P = min(3, r–2))  

3.  State variables  
    t            current round (1…r)  
    pun_counter  how many more rounds you will punish (initially 0)  
    history[t–1] actions of all players in previous round (for t > 1)  

4.  Pseudocode  

    initialize pun_counter ← 0  

    for t in 1…r do  
       if t == r then  
          action ← D    # last round: defect  
       else if t == 1 then  
          action ← C    # first round: no history ⇒ cooperate  
       else if pun_counter > 0 then  
          action ← D  
          pun_counter ← pun_counter – 1  
       else  
          # Examine round t–1: did ANY player defect?  
          if ∃ j ∈ {1…n} such that history[t–1][j] == D then  
             # trigger punishment for next P rounds (including this one)  
             pun_counter ← P – 1    # we will punish this round + next P–1 rounds  
             action ← D  
          else  
             # no defection seen ⇒ cooperate  
             action ← C  
          end if  
       end if  

       play(action)  
       observe everyone’s actions and payoffs ⇒ record history[t]  
    end for  

5.  Explanation of components  

   •  Default cooperation: By choosing C you extract only S/(2n), leaving the stock high so that future periods pay well.  
   •  Immediate detection: You only need last‐round history to spot any defection.  
   •  Finite punishment: Rather than destroying future surplus forever (as a grim trigger would), you inflict a short D-phase of length P. This both signals that defection won’t be tolerated and caps damage to the stock.  
   •  Forgiveness: After punishing P rounds you resume cooperation, so allies who stayed cooperative continue to enjoy a high stock, and former defectors have a path back to high future payoffs.  
   •  Last‐round defection: Standard backward‐induction dictates no benefit to cooperating when t = r.  

6.  Choice of P  
   A small constant (e.g. 2 or 3) typically suffices: it makes defection unprofitable relative to long‐run cooperation, yet does not drive the pool extinct. If r is small, you can set P = max(1, r–2).  

7.  Why this is “cooperative”  
   – When all play C every round except the last, the stock stays at capacity and each round’s per‐player payoff is capacity/(2n).  
   – Any unilateral or sporadic defector gains briefly by extracting capacity/n but then endures P rounds of mutual defection, after which they regain cooperation only if they cease defecting.  
   – Because P is finite, the system recovers full stock quickly, so the cooperative payoff path strongly dominates persistent defection in total sum.  

This “Finite-Punishment Tit-for-Tat” thus rewards mutual cooperation, deters free‐riding with limited collateral damage, and cleanly handles first‐ and last‐round edges.
'''

description_COOPERATIVE_117 = '''
Below is a single‐strategy entry for the tournament.  It never invokes out‐of‐band communication or conventions, only conditions on (1) the round number, (2) what you observed other players do in the previous round, and (3) (optionally) the current stock.  It starts out fully cooperative, punishes defection by any other player for exactly one round, then returns to cooperation if no new defections occur, and it defects in the final round.  This “Tit-for-Tat with One-Round Punishment + Endgame Defection” is simple, transparent, and clearly aligned with cooperation.

––––––––––––––––––––––––––––––––––––––––––––––––––––––  
STRATEGY NAME  
 Coop-TFT-Endgame

STATE VARIABLES  
 last_opponent_defected: boolean, initialized FALSE  
 Parameters your code knows: n, r, capacity (but you never calibrate off n or capacity)  
 (observe each period: stock S_t and each player’s action in t)

DECISION RULES (each round t = 1…r)

1. If t == r (the final round), play D.  
   • Rationale: no future to sustain cooperation.  

2. Else if t == 1, play C.  
   • First‐move cooperation builds trust.  

3. Else (2 ≤ t ≤ r–1):  
   a. If last_opponent_defected == TRUE, play D (punish for exactly one round).  
   b. Otherwise, play C.  

UPDATING last_opponent_defected  
 After observing actions in the current round t, before proceeding to t+1, set  
 last_opponent_defected = TRUE if in round t any other player j ≠ you played D;  
 otherwise set it to FALSE.  

OPTIONAL STOCK‐BASED TIE-BREAKER (entirely consistent with cooperative mindset):  
 If the common pool stock S_t ever falls below a tiny threshold (e.g. S_t < ε, where ε ≪ capacity), you can safely switch to D since there is effectively no resource left to preserve.  This does not change the logic above—it simply avoids forlorn “C” when the pool is empty.

PSEUDOCODE  

  initialize last_opponent_defected ← FALSE

  for t in 1…r do
    observe S_t, history of all players’ actions up to t–1
    if t == r:
      action ← D
    else if t == 1:
      action ← C
    else  # 2 ≤ t ≤ r–1
      if last_opponent_defected == TRUE:
        action ← D       # one-round punishment
      else:
        action ← C       # cooperate

    play(action)

    # After playing, observe opponents’ actions in round t:
    if any opponent j (j≠you) played D in round t:
      last_opponent_defected ← TRUE
    else:
      last_opponent_defected ← FALSE
  end for

WHY THIS IS COOPERATIVE  
• By default it always plays C and keeps the stock at its regenerative maximum.  
• A single defection by any one player triggers exactly one round of group punishment—no stale “forever‐grim” spirals.  
• After that one round, if everyone else has returned to C, so do you.  
• Final‐round defection is unavoidable (finite horizon) but does not undermine cooperation in earlier rounds.  

This strategy is transparent, easy for others to infer, and strong enough to deter unilateral defection in the bulk of play.
'''

description_COOPERATIVE_118 = '''
Below is a simple, fully‐specified “Tit-for-Tat with Final‐Round Defection” strategy.  It is cooperative in that it (a) starts by cooperating, (b) cooperates as long as everyone else did in the previous round, (c) punishes any defection by defecting exactly one round, then returns to cooperation, and (d) defects in the very last round (the usual end‐game logic).  This set of rules is well‐known to sustain cooperation in repeated common‐pool‐resource problems without assuming any off‐path coordination.

—–  
Strategy name: TFT–FRD (Tit-for-Tat with Final‐Round Defection)

Notation:  
  – t = current round (1 ≤ t ≤ r)  
  – a_i(t) ∈ {C,D} = your action in round t  
  – H(t–1) = history of all players’ actions up through round t–1  
  – For each player j, a_j(t–1) is j’s action last round  

Decision rules:

1. If t = 1:  
   a_i(1) ← C  
2. Else if t = r:  
   a_i(r) ← D  
3. Else (2 ≤ t < r):  
   If ∀ j: a_j(t–1) = C then  
    a_i(t) ← C  
   Else  
    a_i(t) ← D  

That’s it.  

Explanation:  
• First round cooperation signals willingness to grow the stock.  
• On any interior round t, you cooperate exactly when everyone cooperated in t–1.  If you observe even one defection by any player, you defect in t—punishing the transgressor(s).  
• You punish for only one round: if no new defections occur in the next round, you revert to cooperation.  This “forgive‐after‐one” keeps the stock from spiraling down too far under prolonged mutual punishment.  
• In the last round you defect, capturing the final‐round temptation (no future rounds to punish you).  

Why this is cooperative:  
– It sustains high‐payoff, high‐stock trajectories because unilateral defection is met by immediate, but short‐lived, collective defection, making defection costly.  
– As long as everyone abides, the pool regenerates toward capacity each round and all players repeatedly earn the cooperative payoff S/(2n).  
– It uses only publicly observed actions—no private signals or side channels—and requires no extra assumptions about shared norms.  

Pseudocode:

```
function TFT_FRD_decision(t, history, r):
    if t == 1:
        return C
    if t == r:
        return D
    # otherwise t in 2..r-1
    last_round = history[t-1]
    if all(action == C for action in last_round):
        return C
    else:
        return D
```

You can readily implement this in any tournament‐framework.  It is a well‐tested, simple, “win–stay, lose–switch”‐style rule (specialized to one‐period punishment) that robustly supports cooperation in repeated CPR settings.
'''

description_COOPERATIVE_119 = '''
Below is a single‐agent strategy that (i) attempts to sustain full cooperation until the very last round, (ii) punishes any defection by any player, but then forgives (“tit-for-tat”), and (iii) defects in the final round (since there is no future to protect).

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
STRATEGY “CTFT‐END” (Cooperative TFT with End‐Game Defection)

Parameters inside the strategy  
• pun_length = 1  // length of punishment phase after observing a defection  
• r = total number of rounds  

State variables (initialized once at start)  
• pun_timer ← 0  // counts down remaining punishment rounds  

On each round t = 1,2,…,r do:  
  if t = r then  
    action ← D      // last‐round defection  
  else if pun_timer > 0 then  
    // we are in a punishment phase  
    action ← D  
    pun_timer ← pun_timer − 1  
  else if (in round t−1 any player played D) then  
    // record and execute punishment next  
    pun_timer ← pun_length  
    action ← D  
  else  
    // no punishment active, no recent defections  
    action ← C  

End  

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
Explanation of key design points

1. First Round t=1  
   – pun_timer=0 and no history → play C.  

2. Full‐Cooperation Regime  
   – As long as every player (including yourself) has cooperated in the immediately preceding round, you continue to play C, preserving the stock at or near capacity.  

3. Punishment of Defection  
   – If anyone defects in round t−1, you set pun_timer=1 and in round t play D.  
   – After that single round of punishment (pun_length=1), pun_timer reverts to 0. You return to cooperation provided no new defections occur.  
   – This “tit-for-tat” style ensures that any defection is met by immediate retaliation but does not lead to a permanent breakdown of cooperation.  

4. End‐Game Defection  
   – In round r, since there is no future, you switch to D to extract the maximum immediate payoff S/n.  
   – This is standard in finite‐horizon repeated games: cooperation unravels in the last period if you have no commitment device.  

5. Robustness  
   – You never punish more than one round for a single defection, so accidental or experimental defections do not trigger a long vendetta.  
   – By immediately returning to cooperation, you maintain a cooperative equilibrium against other TFT‐type players.  

Pseudocode (compact)  
––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
initialize pun_timer ← 0  
for t in 1…r:  
  if t == r:  
    play D  
  else if pun_timer > 0:  
    play D  
    pun_timer ← pun_timer − 1  
  else if “someone played D last round”:  
    pun_timer ← 1  
    play D  
  else:  
    play C  
end for  
––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  

This strategy maximizes the chance of sustaining high stocks (and thus high per‐round payoffs) for all cooperative partners, provides immediate but limited punishment for defectors, and correctly defects in the final round when there is no incentive to preserve the resource.
'''

description_COOPERATIVE_120 = '''
Below is a single‐strategy “recipe” for an autonomous agent that tries to sustain full cooperation as long as possible, yet punishes defectors, and still “rips off” the commons in the very last round (where there is no future to protect).  We call it the Grim–Trigger–with–Last–Round strategy.  You can of course tune the punishment length or forgiveness parameters, but this version is simple and transparent.

1.  State variables  
    • defect_seen (boolean, initially false)  
    • current_round t = 1,2,…,r  

2.  Decision rules  
    At the start of each round t the agent does:  
      if t == 1:  
        – action ← C  
        – (we always “open with” cooperation)  
      else if t == r:  
        – action ← D  
        – (in the very last round there is no future to protect, so we defect)  
      else if defect_seen == true:  
        – action ← D  
        – (we are punishing; once a defection has ever been observed, we defect forever)  
      else if in round t–1 any player j played D:  
        – defect_seen ← true  
        – action ← D  
        – (trigger punishment as soon as we see one defection)  
      else:  
        – action ← C  
        – (no defection seen so far → cooperate)  

3.  Edge cases and remarks  
    • First round (t=1): Always cooperate.  
    • Last round (t=r): Always defect (max out one’s own harvest when there is no longer any future payoff).  
    • Single defection anywhere before round r triggers permanent defection thereafter (“grim trigger”).  
    • If the stock ever crashes to zero, future payoffs are zero anyway—our rule still prescribes D, which is harmless in that state.  
    • This strategy is fully deterministic and only conditions on publicly observed history (the vector of C/D in each past round).  

4.  Why it is “cooperative”  
    – If all players adopt it, nobody ever defects until round r, so the common‐pool stays perpetually at capacity and each round’s payoff is S/(2n) = capacity/(2n), maximizing long‐run welfare.  
    – A single defection is met with guaranteed punishment, which makes one‐shot gain (switching to D against C) unattractive if players care about maintaining the pool over the r–t remaining rounds.  
    – No communication or side‐contracts are needed—decisions depend only on observed play.  

Pseudocode summary  
==================  
Initialize defect_seen ← false  
For t in 1…r do  
  if t == 1 then                  # open with cooperation  
    action ← C  
  else if t == r then             # last round: defect  
    action ← D  
  else if defect_seen then        # punishment ongoing  
    action ← D  
  else if (∃ j: in round t–1 player j played D) then  
    defect_seen ← true            # trigger the grim punishment  
    action ← D  
  else                            # nobody has defected so far  
    action ← C  
  end  
  play action  
end  

You can of course soften “grim” to a finite‐length punishment (e.g. punish for K rounds then reset), or add probabilistic forgiveness.  But the core idea is:  
  • Cooperate by default and sustain the stock.  
  • Detect any defection and retaliate.  
  • Exploit the commons in the known final round.
'''

description_COOPERATIVE_121 = '''
Below is a single‐strategy proposal—essentially a “generous tit‐for‐tat with endgame defection”—that (1) starts by cooperating, (2) punishes defection with a one‐round retaliatory defection, (3) immediately forgives and returns to cooperation, and (4) in the very last round defects to grab the remaining resource (no future rounds to sustain or punish).  

––––––––––––––––––––––––––––––––  
1.  PARAMETERS  
––––––––––––––––––––––––––––––––  
Let  
•  P = 1   “punishment length” (we defect exactly one round after observing a defection)  
•  T_end = 1   (we will defect in the last T_end rounds unconditionally)  

––––––––––––––––––––––––––––––––  
2.  STATE VARIABLES  
––––––––––––––––––––––––––––––––  
Initialize at the start of the game:  
•  punish_left = 0   (how many more rounds we must defect as punishment)  

All players’ past actions and the current stock S_t are publicly known at each round t.  

––––––––––––––––––––––––––––––––  
3.  DECISION RULE (for each round t = 1…r)  
––––––––––––––––––––––––––––––––  
if  t > r − T_end  then  
   Action = D   // final round(s): defect to maximize immediate payoff  
else if  punish_left > 0  then  
   punish_left ← punish_left − 1  
   Action = D   // continue punishment  
else if  t > 1  AND “at least one opponent defected in round t−1”  then  
   punish_left ← P − 1  
   Action = D   // punish that defection this round; the “−1” leaves exactly P rounds total  
else  
   Action = C   // cooperate  

––––––––––––––––––––––––––––––––  
4.  EXPLANATION & RATIONALE  
––––––––––––––––––––––––––––––––  
1.  First‐mover cooperation:  In round 1 there is no history, so we cooperate.  
2.  Promoting sustained cooperation:  As long as nobody defected in the preceding round, we keep cooperating—this maximizes long‐run stock and per‐round payoffs for everyone.  
3.  Deterring free‐riding:  If we see any defection in round t−1, we defect in round t exactly once.  Because our threat is credible (we will indeed defect once) and short (only one round), it deters unilateral defection but still forgives quickly, preventing endless retaliation loops.  
4.  End‐game defection:  In the very last round (t > r−1), no future punishment is possible.  To maximize our last‐round payoff we defect unconditionally.  This is standard end‐game reasoning in finite repeated games.  

––––––––––––––––––––––––––––––––  
5.  PSEUDOCODE  
––––––––––––––––––––––––––––––––  

Initialize punish_left ← 0  

for t in 1…r do  
 Observe current stock S_t and history of all players’ actions up to round t−1.  
 if t > r − T_end then  
  action ← D  
 else if punish_left > 0 then  
  punish_left ← punish_left − 1  
  action ← D  
 else if t > 1 AND (exists j ≠ me with action_j[t−1] = D) then  
  // Someone defected last round  
  punish_left ← P − 1  
  action ← D  
 else  
  action ← C  
 end if  
 Play action, observe payoffs, update S_{t+1} by the game’s stock rule.  
end for  

––––––––––––––––––––––––––––––––  
6.  EDGE‐CASE HANDLING  
––––––––––––––––––––––––––––––––  
•  First round (t=1): No history ⇒ cooperate.  
•  Immediate forgiveness: Punishment is capped at P=1 round, so even chains of defection last only one period each.  
•  Last round(s): We defect to harvest maximum payoff—no future resource or punishment remains.  

––––––––––––––––––––––––––––––––  
This strategy is fully “cooperative” in that it:  
•  Maximizes joint stock growth by defaulting to cooperate every round;  
•  Deters unilateral defection via a swift, one‐period punishment;  
•  Quickly returns to cooperation, avoiding permanent collapse from endless vendettas;  
•  Recognizes the finite horizon and defects only at the true final opportunity.
'''

description_COOPERATIVE_122 = '''
Below is a simple “conditional‐cooperate with finite punishment” strategy that (i) aims for full cooperation most of the way, (ii) punishes any defection enough to deter it, (iii) then forgives and returns to cooperation, and (iv) defects in the very last round (to avoid being exploited when there is no future).

-------------------------------------------------------------------------------
STRATEGY NAME  
  Forgiving Trigger with Endgame Defection

PARAMETERS  
  Let P = 2  (length of punishment phase)  
  Let r = total number of rounds  
  Let t = current round index (1…r)  

STATE VARIABLES  
  punish_timer ∈ {0,1,2,…}  (rounds remaining in punishment phase)  

INITIALIZATION (before round 1)  
  punish_timer ← 0  

DECISION RULE (at the start of each round t)  
  1. If t == r (the last round)  
       – play D (defect) and end.  
  2. Else if punish_timer > 0  
       – play D  
       – punish_timer ← punish_timer − 1  
  3. Else  (we are “in cooperation mode”)  
     a. If t == 1  
          – (no history) → play C  
     b. Else  (t > 1, look at history of round t−1)  
          – If any other player chose D in round t−1  
               * enter punishment: punish_timer ← min(P, r−t)  
               * play D this round  
          – Else  (everyone cooperated last round)  
               * play C  

EXPLANATION OF THE RULES  
  • Initial cooperation: In round 1 we play C, hoping others do the same.  
  • Conditional cooperation: As long as in the previous round all players played C, keep playing C.  
  • Trigger & finite punishment: The first time anyone defects, we switch to D for P consecutive rounds (or until the last round if fewer remain). This penalty makes unilateral defection unprofitable in expectation.  
  • Forgiveness: After P punishment rounds, punish_timer hits zero and we go back to cooperation mode. This lets us re‐establish mutual cooperation if the group returns to C.  
  • Endgame defection: In the very last round (t = r), we play D. Since there is no future, a rational player cannot be deterred and will defect if they expect us to cooperate. By defecting, we protect ourselves.

WHY THIS IS COOPERATIVE  
  – It sustains high stock levels and high per‐round payoffs by keeping everyone in C most of the time.  
  – Occasional mistakes (or noise) are forgiven after P rounds rather than punished forever, so cooperation can be re‐born.  
  – The threat of a short, sharp punishment makes defection costly on average and deters free‐riding.  
  – Defection in the final round is the only place we “exit” cooperation, which is necessary in a finite‐horizon game to avoid guaranteed exploitation when no future remains.

HANDLING EDGE CASES  
  • If a defection occurs on round r–1, we will punish only for the remaining rounds (which may just be t=r–1) and immediately hit the “last‐round defection” rule on t=r.  
  • If r is small (e.g. r=2 or 3), punish_timer is capped so we never “overshoot” into the final round.  
  • If everyone adheres, stock stays near capacity by mutual C, maximizing long-run payoffs for all.  

PSEUDOCODE SUMMARY  
  punish_timer ← 0  
  for t in 1…r do  
    if t == r:  
      action ← D  
    else if punish_timer > 0:  
      action ← D  
      punish_timer ← punish_timer − 1  
    else if t == 1:  
      action ← C  
    else if any player chose D in round t−1:  
      punish_timer ← min(P, r−t)  
      action ← D  
    else:  
      action ← C  
    end  
    play(action)  
  end  

This strategy balances deterrence (via punishment), forgiveness (finite punishments), and the need to defect in the final round when there is no future incentive to cooperate.
'''

description_COOPERATIVE_123 = '''
Below is a fully self‐contained “cooperative” strategy you can drop into your tournament.  It is a simple Tit-for-Tat with finite punishment (“TFT-FP”) that (1) starts out fully cooperative, (2) punishes any defection by defecting for a short, fixed number of rounds, then (3) returns to cooperation and “forgives.”  This both sustains high stock levels and deters persistent free‐riding.

-------------------------------------------------------------------------------
1.  State variables and parameters  
   • punishment_rounds ← 0      (how many more rounds we must punish)  
   • P ← 2                       (fixed punishment length; you can tune P ≥ 1)  
   • r                           total number of rounds  
   • n                           number of players  

2.  High‐level idea  
   – Round 1: Cooperate.  
   – In any subsequent round t:  
       • If we are in a punishment phase (punishment_rounds>0), Defect.  
       • Else if anyone defected in the previous round, enter punishment phase of length P and Defect.  
       • Otherwise Cooperate.  
   – Last round is treated the same way (we keep cooperating if we are not punishing).  

3.  Pseudocode  

   initialize:  
     punishment_rounds ← 0  

   for t in 1…r do  
     if t == 1 then  
       action ← C                             // start by cooperating  
     else if punishment_rounds > 0 then  
       action ← D                             // punish phase  
       punishment_rounds ← punishment_rounds – 1  
     else  
       // look at last‐round history  
       if ∃ j ∈ {1…n} s.t. history[j][t–1] = D then  
         // someone defected last round: trigger punishment  
         punishment_rounds ← P – 1            // this round + next P–1 rounds  
         action ← D  
       else  
         action ← C                           // everybody cooperated last round  
       end if  
     end if  

     play(action)  
     observe all players’ actions; record in history  
   end for  

4.  Why this is cooperative  
   – So long as no one defects, everyone repeatedly plays C, harvesting only S/(2n) and allowing the stock to regrow toward capacity.  
   – A short, finite punishment (P rounds of D) is enough to make a one‐shot defection unattractive: defectors gain S/n instead of S/(2n), but then lose out in the next P cooperations-only rounds when we defect.  
   – After punishment we immediately return to full cooperation, so small mistakes or noise aren’t compounded into permanent mutual defection.  

5.  Handling edge cases  
   • First round: we have no history → cooperate.  
   • Last round (t=r): we follow the same rules.  If we’re punishing, we defect; otherwise we still cooperate, because that maximizes group payoff in the absence of future rounds (and stays true to our cooperative mindset).  
   • Stock collapse (S=0): both C and D yield zero payoffs.  We treat it the same—our policy only depends on last‐round actions, not the stock level itself.  

6.  Tuning & extensions  
   – You can vary P (1,2,3…) to balance deterrence vs. forgiveness.  
   – If you worry about end‐game unraveling, you could set P=1 when t>r–P (i.e. no punishment if few rounds remain), or even switch to pure C in the last k rounds.  
   – You could add random “generosity,” e.g. on a small probability ε forgive an observed defection immediately—this often performs well in noisy environments.  

This TFT-with-finite-punishment strategy is easy to implement, strictly reciprocal, patiently restores cooperation after a defection, and maintains the common stock near capacity when opponents also cooperate.  It thus embodies a cooperative mindset while protecting against exploitation.
'''

description_COOPERATIVE_124 = '''
Below is a single‐player “cooperative” strategy you can enter into the tournament.  It is a forgiving trigger (one‐round punishment) combined with the inevitable last‐round defection.  It aims to keep the resource near capacity by cooperating whenever possible, punishing brief defections, and then returning to cooperation.

1.  State variables  
    •  last_defection_round ← 0   (round index of most recent defection observed)  
    •  r            (total number of rounds, known)  

2.  Parameters  
    •  P = 1       (punishment length in rounds; here we punish for exactly one round)  

3.  Decision rule, for each round t = 1,2,…,r  
    if t = 1 then  
        play C   (start cooperatively)  
    else if t = r then  
        play D   (defect in the final round to maximize last‐round payoff)  
    else if last_defection_round = t–1 then  
        play D   (punish for one round immediately after observing any defection)  
    else  
        play C   (otherwise cooperate)  

4.  Updating after round t completes  
    Observe everyone’s actions in round t.  
    if ∃ j≠i such that player j played D in round t then  
        last_defection_round ← t  
    end if  

5.  Explanation of why this is cooperative  
    •  It starts by cooperating, so if all players follow a similar rule you maintain high stock.  
    •  Any defection in a given round is met by exactly one round of defection—enough to deter unprovoked defections but not so harsh as to collapse cooperation permanently.  
    •  After that one‐round punishment you immediately return to cooperation, which allows the stock to recover.  
    •  You defect in the final round to avoid being exploited yourself on the last move; this is standard in finitely repeated games and does not undermine cooperation in earlier rounds.  

6.  Edge‐case handling  
    •  First round (t=1): Unconditionally cooperate, establishing an initial cooperative norm.  
    •  Last round (t=r): Always defect to avoid giving free payoffs when there is no future to punish.  
    •  Consecutive defections: Because punishment is only one round long, if multiple players defect in a row you will defect in each round that immediately follows a defection, and then revert to C.  
    •  If the stock ever falls to zero (S=0), future payoffs are zero anyway; you continue applying the same rule (so you will defect in the last round regardless).  

7.  Pseudocode  

    initialize last_defection_round ← 0  
    for t in 1..r do  
      if t = 1 then  
        action ← C  
      else if t = r then  
        action ← D  
      else if last_defection_round = t–1 then  
        action ← D  
      else  
        action ← C  
      end if  

      play(action)  
      observe all players’ actions in round t  
      if any other player played D in round t then  
        last_defection_round ← t  
      end if  
    end for  

This strategy balances a strong preference for cooperation (keeping the resource near capacity) with a clear, limited punishment for defection and the rational incentive to defect in the very last round.
'''

description_COOPERATIVE_125 = '''
Below is a simple “group tit-for-tat” style strategy that (1) starts cooperatively, (2) punishes defections just long enough to deter them, (3) returns to cooperation as soon as opponents do, and (4) defects in the very last round to protect against end-game exploitation.

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
Strategy: Group Tit-for-Tat with End-Game Defection

Notation  
• t = current round (1 ≤ t ≤ r)  
• A_i(t) ∈ {C,D} = your action in round t  
• history(t–1) = vector of all players’ actions in round t–1  
• AnyDefect(t–1) = true iff ∃ j such that A_j(t–1)=D  

Decision rules  
1. Round 1 (t=1):  
   A_i(1) ← C  
2. Intermediate rounds (2 ≤ t ≤ r–1):  
   if AnyDefect(t–1) then  
       A_i(t) ← D    // punish one round  
   else  
       A_i(t) ← C    // cooperate if everyone cooperated last round  
3. Final round (t = r):  
   A_i(r) ← D       // defect in last round to avoid being exploited  

Rationale  
– Cooperate from the start to build up the stock and signal good intent.  
– If anyone defects, punish immediately next round by defecting; this one-round punishment is enough to eliminate the defector’s short-term gain and thus deter future defections.  
– As soon as all return to C, you forgive and cooperate again—this keeps cooperation alive.  
– In the known final round, defect, since no future punishment is possible.  

Pseudocode  

    initialize:    
      for each round t do history[t] ← null    
      
    for t in 1..r do:
      if t == 1 then
        play C
      else if t == r then
        play D
      else
        // 2 ≤ t ≤ r–1
        if ∃ j in {1…n} such that history[t−1][j] == D then
          play D
        else
          play C
      end if

      observe opponents’ actions → history[t]
    end for

Edge-case handling  
• First round: no past information ⇒ cooperate.  
• Last round: guaranteed defection to protect against end-game free-riding.  
• Single defection: punished exactly one round, then immediate return to cooperation if everyone cooperates.  
• Persistent defector: each round you see a defection you punish in the next round, so a stubborn defector never gains from continuing to defect.  

Cooperative alignment  
This strategy maximizes group welfare by sustaining the highest possible stock levels over as many rounds as possible.  It only defects to discourage free-riding and in the final round when no further cooperation is possible.
'''

description_COOPERATIVE_126 = '''
Below is a single‐strategy “trigger + forgiveness” approach that (i) aims to keep the stock at capacity by mutual cooperation, (ii) punishes any one‐round defection, but (iii) quickly forgives to resume cooperation, and (iv) handles the known finite horizon.  

1.  Intuition  
    - If everybody plays C each round, the stock regenerates to capacity and all continue to earn the sustainable payoff S_t/(2n).  
    - A one‐round defection (D) by any player yields that defector a higher immediate payoff but dents the resource and threatens future rounds.  
    - To deter defection, we punish by playing D in the following round—but only for one round. After that, if no new defections occur, we resume C.  
    - In the very last round, all players rationally defect (no future to punish), so we defect as well.  

2.  Decision Rules  
    Let r be the total number of rounds, t the current round (1 ≤ t ≤ r), and history H be the full action profile history up to t–1.  
      
    At the start of round t, each player does the following:  
    1.  If t == 1:  
          play C.  
    2.  Else if t == r (the final round):  
          play D.  
    3.  Else (2 ≤ t < r):  
       a.  If in the previous round (t–1) at least one player chose D, then play D (punish for exactly one round).  
       b.  Otherwise (everyone chose C in round t–1), play C.  

3.  Pseudocode for player i  
    ```  
    function choose_action(t, history H):  
        if t == 1:  
            return C  
        if t == r:  
            return D  
        // t in [2..r-1]  
        let actions_last = H[t-1]  // the vector of all players’ moves in round t-1  
        if contains(actions_last, D):  
            return D          // punish exactly once  
        else:  
            return C          // resume cooperation  
    ```  

4.  Explanation of Edge Cases  
    • First round (t=1):   No prior history → start by cooperating.  
    • Intermediate rounds:  
       –  If everyone cooperated in t–1, we trust them once more and play C.  
       –  If we observed any defection in t–1, we play D this round to make defection unprofitable.  
       –  Even if we punish in round t, as long as no new defection occurs in t, we will forgive in t+1.  
    • Last round (t=r):    No future, so irrespective of history, we defect (standard backward induction).  

5.  Why It’s Cooperative  
    –  Mutual C in rounds 1…r–1 keeps the resource at capacity every round.  
    –  The one‐period punishment makes single‐shot defection unattractive: defecting gives an extra S/(2n) today but costs you the next round’s cooperation bonus.  
    –  Rapid forgiveness (punish only one round) prevents cascading mutual defection if someone deviates by mistake or if a single defector is punished too harshly.  
    –  By defecting only in the last round, we avoid giving up payoff early for an immeasurable threat in a round that doesn’t exist.  

6.  Tournament Considerations  
    –  Against purely “always‐cooperate” opponents, you cooperate until r–1 and then defect in r, earning the best end‐game payoff without having harmed the pool.  
    –  Against “always‐defect” opponents, you punish in round 2, then forgive in round 3, etc., but when they defect again you punish again. You never let them get away with repeated free‐riding unpunished.  
    –  Against other trigger‐forgiving types, you sustain full cooperation through rounds 1…r–1, keeping the resource alive and maximizing collective payoff.  

This strategy strikes a balance between firmness (to deter free-riding) and forgiveness (to sustain cooperation), and correctly handles the known last-round defection.
'''

description_COOPERATIVE_127 = '''
Below is a conditional-cooperation strategy (“Coop-Guard”) that (1) seeks full cooperation to sustain the pool, (2) punishes defections so they are not profitable, (3) forgives after a fixed punishment, and (4) protects the pool if it ever falls too low.  It uses only observed plays and the current stock level—no off-path communication or side-payments.

1. Intuition  
   - Start by cooperating to build trust.  
   - If anyone defects, retaliate by defecting for a short, fixed number of rounds (so-called “proportional punishment”).  
   - After the punishment phase, return to cooperation (forgiveness).  
   - If the common stock ever falls below a safety‐threshold, suspend punishment and cooperate unconditionally (to let the resource recover).  
   - In the very last round, defect (standard endgame logic).  

2. Parameters  
   Let  
     • P = punishment length (e.g. 2 rounds)  
     • θ = safety threshold for stock (e.g. capacity/4)  
     • r = total rounds  

3. State variables (per player i)  
   • punish_left ∈ {0,1,…,P}: how many more rounds to punish  
   • last_actions[j]: action of player j in the previous round (observed)  

4. Decision rule for player i in round t with current stock S:  

Pseudocode  
----------  
initialize:  
  punish_left ← 0  

for t in 1..r do  
  if t = r then  
    action_i ← D   # last‐round defect to grab one‐shot gain  
  
  else if t = 1 then  
    action_i ← C   # start with cooperation  
  
  else if S < θ then  
    # pool is in danger—unconditionally cooperate to rebuild  
    action_i ← C  
  
  else if punish_left > 0 then  
    # still in punishment phase  
    action_i ← D  
    punish_left ← punish_left − 1  
  
  else  
    # Normal “Tit‐for‐Tat with forgiveness”  
    if (∃ j ≠ i: last_actions[j] = D) then  
      # someone defected last round ⇒ punish reaction  
      action_i ← D  
      punish_left ← P − 1   # we defect this round + P−1 more rounds  
    else  
      action_i ← C        # everyone cooperated last round ⇒ cooperate  
    end if  
  end if  

  play action_i  
  observe all actions this round; update last_actions[j] for next round  
end for  
----------  

5. Explanation of key features  
 • First round t=1: cooperate to signal willingness.  
 • Cooperative steady state: if all cooperated last round, keep cooperating.  Total use = S/2 each round, allowing regrowth back toward capacity.  
 • Punishment: if any defection is observed, defect for P consecutive rounds.  This makes unilateral defection unprofitable in expectation.  After P rounds, we return to cooperation.  
 • Safety override: if stock S ever drops below θ, immediately suspend punishment and revert to cooperation until the pool recovers.  This ensures we do not drive the resource to extinction.  
 • Last round: defect for one‐shot gain (standard backward‐induction endgame).  You can optionally extend this to the last K rounds if r is known and small.  

6. Edge cases  
 • If multiple defections occur during a punishment phase, we do NOT “stack” punishments; we simply complete the current P-round punishment and then return to cooperation.  This avoids infinite retaliation loops.  
 • If S remains under θ beyond the punishment window, we stay in cooperation even if punish_left > 0 (you can implement that by checking S<θ before applying punish_left).  
 • If r is very small (e.g. r=2), the scheme still runs: round 1 cooperate, round 2 defect.  

This “Coop-Guard” strategy has been widely used in public good and common-pool settings.  It (a) clearly signals cooperation, (b) deters free-riding by a credible short-term punishment, (c) forgives so cooperation can restart, and (d) protects the resource from collapse.
'''

description_COOPERATIVE_128 = '''
Below is a “Cooperative Tit-for-Tat with Endgame Defection” strategy.  It aims to sustain full cooperation (i.e. everyone choosing C each round) by starting cooperatively, punishing any defection with a one‐round defection, then immediately forgiving.  In the very last round it defects, since there is no future to protect.

1.  Strategy parameters  
   n             number of players  
   r             total rounds  
   capacity      common‐pool capacity (only used to compute payoffs and stock updates)  
   P = 1         length of punishment phase (in rounds)  
   E = 1         number of last rounds in which we unconditionally defect  

2.  Internal state  
   punishing    boolean flag (are we currently in a punishment phase?)  
   punish_left  integer (rounds of punishment still to go)  

3.  Detecting defection in round t  
   At the end of round t, you observe every player’s payoff π_j(t) and you know the stock S_t before consumption.  
   Cooperators would each have received exactly π_C = S_t/(2n).  
   If any π_j(t) > π_C, that player must have played D.  
   So  
     defection_detected(t) = (max_j π_j(t) > S_t/(2n)).  

4.  Decision rule (for round t = 1…r)  

   if t > r − E then  
     // Last round(s): no future to protect  
     play D  
   else if punishing == true then  
     // We are in punishment phase  
     play D  
     punish_left ← punish_left − 1  
     if punish_left == 0 then  
       punishing ← false  
     end  
   else  
     // Normal cooperative mode  
     if t == 1 then  
       play C  
     else  
       if defection_detected(t−1) then  
         // Trigger one‐round punishment  
         punishing ← true  
         punish_left ← P  
         // Immediately consume punishment round  
         play D  
         punish_left ← punish_left − 1  
         if punish_left == 0 then punishing ← false end  
       else  
         play C  
       end  
     end  
   end  

5.  Explanation  

–  Start by cooperating (C) in round 1.  
–  As long as no defection is observed in the immediately preceding round, continue to cooperate.  “Cooperation” means consuming S/(2n), which keeps the resource at its maximum sustainable level.  
–  If you ever detect any player defected (someone got more than S/(2n)), you switch to “punishment phase” by defecting (D) yourself for exactly one round (P=1).  Then you forgive and return to cooperation, giving the group a chance to re‐establish mutual cooperation.  
–  In the very last round (t = r), there is no future penalty, so defect unconditionally to protect yourself from being exploited.  

6.  Why this is “cooperative”  

–  It maintains full cooperation (and hence maximal stock regeneration) whenever all players are cooperating.  
–  It reacts swiftly to any unilateral defection, discouraging free‐riding by inflicting a one‐round loss on the defector.  
–  It forgives immediately, so accidental or one‐off defections do not lead to endless war.  
–  By defecting only in the last round, it avoids being exploited at the end without unduly sacrificing earlier gains.  

This strategy balances the maximization of joint long‐run payoffs (by sustaining cooperation) with short‐run deterrence (by punishing defectors) and with a rational endgame move.
'''

description_AGGRESSIVE_33 = '''
Below is a fully specified “predator”‐style strategy – brutally greedy, but with just enough occasional cooperation to keep the pool alive long enough to squeeze out maximal total payoff.  

1.  Parameters you must choose once before the game (you can tune these to your particular n, capacity and r):  
    •  threshold_low S_L – when stock falls below this, you briefly switch to cooperation so it regrows.  
    •  regrow_rounds m – the number of consecutive cooperations you will grant to kick‐start regrowth.  

    A reasonable default (for any n ≥2) is:  
       S_L ← capacity/(4n)  
       m  ← 1  

2.  Internal state variables:  
    •  phase ∈ {“EXPLOIT”, “REGROW”}, initially “EXPLOIT”  
    •  regrow_counter, initially 0  

3.  Decision rule (pseudocode):  

   for each round t = 1…r:  
     observe current common‐pool stock S  

     if t == r then  
       // last round: grab everything you can  
       play D  
       return  

     if phase == “EXPLOIT” then  
       if S ≤ S_L then  
         // stock is too low – switch to regrowth phase  
         phase ← “REGROW”  
         regrow_counter ← m  
         play C  
       else  
         // default in exploitation phase: always defect  
         play D  
       end if  

     else if phase == “REGROW” then  
       if regrow_counter > 0 then  
         // cooperate to help the pool bounce back  
         regrow_counter ← regrow_counter – 1  
         play C  
       else  
         // we have done our quota of cooperations, go back to exploitation  
         phase ← “EXPLOIT”  
         play D  
       end if  
     end if  

4.  Explanation of the “mindset” behind each rule:  
   – Aggressive core:  in “EXPLOIT” you always play D to maximize immediate payoff.  
   – Minimal mercy:  as soon as stock dives below S_L you grudgingly play C for m rounds, just enough to regenerate the pool, then resume full‐blown defection.  
   – Last‐round defect:  you never miss a chance to grab the highest payoff in the very last period.  

5.  Edge cases:  
   •  First round:  t=1, phase=EXPLOIT, S=capacity > S_L ⇒ you defect immediately.  
   •  Rounds where S=0:  defecting or cooperating both yield zero, so you default to D.  
   •  When regrow_counter expires mid‐game you always flip back to exploiting.  

This strategy guarantees you take the largest possible share each round except for the tiniest “sacrificial” cooperation pulses needed only to prevent irrevocable collapse of the commons.
'''

description_AGGRESSIVE_34 = '''
Below is a single‐player “aggressive” decision rule.  It never tries to build up mutual cooperation for the group’s sake; it only cooperates to nurse the pool back to a level at which it can exploit it again.  In every other circumstance it defects to grab as much as possible and punish any cooperators or defectors who tried to manage the resource.

----------------  
Strategy name: Thresholded Aggressive Defector (TAD)  

Parameters you choose once (before the tournament):  
•  threshold θ ∈ [0, capacity], the stock‐level at or above which you will defect.  
   A robust choice is θ = capacity/2 (maximizes regrowth when you later nurse).  

Notation:  
•  t = round index, t = 1…r  
•  S_t = stock at start of round t  
•  hist_{t–1} = list of opponent actions in round t–1  
•  D = Defect, C = Cooperate  

1.  First‐ and last‐round rules  
   •  If t = 1, no history exists → play D.  
   •  If t = r, always play D (standard endgame defection).  

2.  Core decision rule for t=2…r–1  
   If S_t ≥ θ  
     → play D  (exploit the high stock immediately)  
   else  (S_t < θ, pool is too low)  
     if round t–1 had at least one cooperator among the n–1 opponents  
       → play C  (nurse the pool so it regrows for future exploitation)  
     else  
       → play D  (punish non‐cooperators by staying in defection mode)  

3.  Rationale / aggressiveness  
   – The strategy never “forgive and forget.”  It only cooperates when the pool is already endangered **and** there was at least one cooperator last round.  That way you do not waste your contribution when everyone else is just defecting.  
   – When the pool is healthy (S ≥ θ) you always defect to grab S/n, maximizing your per-round take and punishing any would-be cooperators.  
   – On the final round you defect unconditionally—no endgame cooperation.  

4.  Pseudocode  

  threshold ← capacity/2  
  for t in 1…r:  
    observe S_t  
    if t = 1 or t = r:  
      action ← D  
    else:  # intermediate rounds  
      if S_t ≥ threshold:  
        action ← D  
      else:  # S_t < threshold  
        # check if any opponent cooperated last round  
        coop_count ← count(hist_{t–1}, action=C)  
        if coop_count ≥ 1:  
          action ← C  # nurse the pool  
        else:  
          action ← D  # punish defectors / noncontributors  
    play(action)  

5.  Edge cases  
   – If θ is set too high (e.g. > capacity), the strategy will almost always cooperate when the pool is low—even if that never leads to future exploitation.  Choose θ in [capacity/3, 2·capacity/3] for safe growth/exploit cycling.  
   – If opponents never cooperate, you will defect every round (since coop_count=0) and drive S→0.  That is aggressive punishment of free‐riders—it also destroys future payoffs, but you have no incentive to nurse a resource only you will exploit.  
   – If a single opponent ever cooperates at low‐stock, you switch to C once to boost S, then immediately defect again when it crosses θ, extracting the lion’s share.  

This strategy is “aggressive” because it:  
•  Never gives unconditional cooperation.  
•  Defects at every opportunity to maximize your haul.  
•  Only ever cooperates to resuscitate the pool so you can defect again later.  
•  Punishes defectors by refusing to nurse the pool if they never showed willingness to cooperate.
'''

description_AGGRESSIVE_35 = '''
Below is a fully specified “aggressive” strategy, which we’ll call Ravenous-Transition.  In plain English it does the following:

  • It gives opponents exactly one round of “good faith” cooperation (to refill the pool to capacity).  
  • At the first sign of defection (including round 1 if any opponent defects), or as soon as the pool is full after round 1, it switches to permanent defection—never cooperates again.  
  • It also defects in the very last round regardless of history (to grab the last drop).

This approach maximizes your harvest, exploits any cooperation from others exactly once, then punishes forever.

—–  
1. State variables  
   attacked ← false    // Have we launched our permanent-defection phase yet?  
   S_t      ← current common-pool stock at start of round t  
   hist[t–1] ← the vector of all players’ actions in round t–1 (only used to check if any C→D or D→C occurred)

2. Initialization (before round 1)  
   attacked ← false  

3. Decision rule, each round t=1…r  
   if t == r then  
     action ← D         // Last‐round defection  
   else if t == 1 then  
     action ← C         // Give one opening round of cooperation  
   else  
     // Check if we should enter the permanent‐defection phase:
     if attacked == false then  
       // Condition A: pool has just been refilled from a pure‐cooperate round  
       //             (i.e. round t–1 was all C and S_t == capacity)  
       condA ← (all players played C in hist[t–1]  AND  S_t == capacity)  
       // Condition B: any opponent defected in any earlier round  
       condB ← (any player in hist[t–1] played D)  
       if condA OR condB then  
         attacked ← true  
       end  
     end  
     // Now choose action based on attacked flag  
     if attacked then  
       action ← D  
     else  
       action ← C  
     end  
   end  

4. Edge cases  
   • If any opponent defects in round 1, attacked becomes true in round 2 and you defect from then on.  
   • If everyone cooperates round 1, the pool regrows to capacity by round 2; you see S₂=capacity, set attacked=true, and defect from round 2 onward.  
   • In the very last round (t=r), you always defect.  

5. Pseudocode  

```
function RavenousTransition(t, r, S_t, history):
    // history[t-1] is list of actions in previous round
    static attacked ← false

    if t == r:
        return D     // Last-round grab

    if t == 1:
        return C     // Opening round cooperation

    // t >= 2 && t < r
    if not attacked:
        let prev_actions = history[t-1]
        let allC       = (prev_actions contains only C)
        let anyD       = (prev_actions contains at least one D)

        condA = (allC and S_t == capacity)
        condB = anyD

        if condA or condB:
            attacked = true

    if attacked:
        return D
    else:
        return C
```

Rationale:  
– By cooperating in round 1 you refill the pool to capacity (if others also cooperate).  
– At the first sign of trust (pool full) or betrayal, you switch to permanent defection and never give the resource another chance.  
– Defecting in the last round guarantees you grab the final share.  
– This strategy is fully specified, requires only public state (stock S_t) and public history, and never relies on side-agreements or secret coordination. It is as “aggressive” as one can be: you do the minimum cooperation needed to maximize future harvest, then you seize the resource permanently.
'''

description_AGGRESSIVE_36 = '''
Below is a self-contained description of an “aggressive” strategy that (1) maximizes immediate defect payoffs whenever it safely can, (2) but occasionally “throws in” a cooperative move just often enough to keep the common pool from collapsing too early so you can continue to exploit it over many rounds.

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
Name  
––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
Aggressive Exploiter with Minimal Restoration (AEMR)  

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
Intuition  
––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
•  You want D (defect) almost always, because π_i(D)=S/n is twice π_i(C)=S/(2n).  
•  If everyone always plays D, the pool goes to zero in one round. That leaves zero for you thereafter.  
•  Therefore you must occasionally play C just often enough to keep S away from zero.  
•  You do not “reciprocate”—you do not conditionalize on who defected—but simply monitor the stock S_t.  
•  You never cooperate in the very first or very last round (no need to build trust at the end).  

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
Parameters  
––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
• capacity (given)  
• n (number of players)  
• r (number of rounds)  

Set one internal threshold θ ∈(0,1).  A convenient choice is θ = 0.5.  
Define  
 T_restore = θ × capacity.  

Decisions: “Defect always unless the pool is below T_restore and it’s been at least K rounds since your last cooperate.”  
Choose K=3 (you cooperate at most once every K+1 rounds).

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
Pseudocode  
––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
```
Input: capacity, n, r
Parameters: θ ← 0.5
            T_restore ← θ * capacity
            K ← 3       # “cool-down” between cooperations

Initialize:
  last_coop_round ← –∞

for t in 1…r:
  observe current stock S_t

  if r < 3:
    # too few rounds to bother saving; just defect every round
    action ← D

  else if t == 1 or t == r:
    # first and last round: always defect
    action ← D

  else if (S_t < T_restore) and (t – last_coop_round > K):
    # stock dangerously low and we haven’t cooperated recently:
    action ← C
    last_coop_round ← t

  else:
    # in all other cases, defect
    action ← D

  play(action)
end for
```

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
Comments on Edge Cases  
––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
1. Very short games (r<3): No time to build up, so you just defect every round.  
2. t=1 and t=r (first and last): no future to protect, so always defect.  
3. If the pool is high (S_t ≥ T_restore): always defect to grab the larger S_t/n slice.  
4. Once the pool dips below T_restore, you play exactly one C (to consume only S_t/(2n)), giving the pool more “breathing room.”  
5. You then wait K rounds before “rescuing” again.  

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
Why This Is “Aggressive”  
––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
• You almost never cooperate—only when the resource is in danger of collapse.  
• You do not punish or reward individual opponents; you only track the public state S_t.  
• You always defect on round one (to exploit naïve cooperators) and round r (endgame).  
• You extract the maximum possible S/n slice whenever that will not immediately kill the pool.  

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
Tuning Notes  
––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
• You can vary θ upward (e.g. 0.6) to be slightly more conservative, or downward (e.g. 0.4) to be more ruthless.  
• You can change K to cooperate more or less frequently.  

This completes the description of an aggressive, stock-preserving exploitation strategy for the common-pool resource game.
'''

description_AGGRESSIVE_37 = '''
Below is an “Aggressive Exploit‐and‐Rescue” strategy.  It has three key ingredients:  
 1.  In any round where at least one opponent cooperated last period, you defect to seize a larger share.  
 2.  If everyone defected last period, you momentarily cooperate to let the pool rebuild (so there will be something left to seize).  
 3.  Always defect in the final round (no future to preserve).  

This policy maximizes your extraction from cooperators, punishes free‐riders by withdrawing support, and prevents permanent collapse by occasionally “rescuing” the resource when it is completely drained.  

----  
Strategy description  
----  
Parameters you observe each round t:  
•  t (current round index, 1 ≤ t ≤ r)  
•  For each player j≠i, their action a_j(t–1) in the previous round.  

Decision rule for player i at round t:  
1.  If t == r (last round) then  
      Play D  
2.  Else if t == 1 (first round) then  
      Play C  
3.  Else (1 < t < r):  
    •  If ∃ j≠i such that a_j(t–1) = C  (i.e. at least one opponent cooperated last round)  
         Play D    // exploit any sign of cooperation  
    •  Else  (all opponents defected last round)  
         Play C    // “rescue” the pool so it regrows  

----  
Why it is aggressive  
----  
•  You never miss an opportunity to defect when anyone else is cooperating, thereby extracting the larger S/n share.  
•  You punish pure‐defectors by refusing to defect alongside them; instead you cooperate when everyone else is defecting, allowing the stock to regrow for future exploitation.  
•  You always defect in the final round to grab the last available payoff.  

----  
Pseudocode  
----  
```
function AggressiveExploitRescue(t, r, history_of_actions):
    # history_of_actions[t-1] is a list of length n of the previous round’s actions
    if t == r:
        return “D”
    if t == 1:
        return “C”
    # Check if any other player cooperated last round
    last_round = history_of_actions[t-1]
    any_coop = False
    for j in 1..n:
        if j != i and last_round[j] == “C”:
            any_coop = True
            break
    if any_coop:
        return “D”   # exploit cooperators
    else:
        return “C”   # rescue after universal defection
```

Edge cases:  
- Round 1: we start by cooperating (build up stock).  
- Rounds 2…r–1: we look at opponents’ last actions; defect if any cooperated, otherwise cooperate to let the pool regrow.  
- Round r: always defect (no future rounds to worry about).  

This yields an aggressive stance—always extracting maximal share from any cooperator—while still keeping the resource alive when everyone else is defecting, and grabbing the final round’s full share.
'''

description_AGGRESSIVE_38 = '''
Below is a self‐contained “aggressive” memory‐1 strategy for the r‐round common‐pool game.  It maximizes short‐term harvests by defecting nearly always, but inserts minimal cooperation when the pool is on the brink of collapse so that some regeneration remains for future rounds.  You can tune the single “safety threshold” parameter to your taste.

1.  PARAMETERS  
    • n     = number of players (≥2)  
    • r     = total rounds (>1)  
    • capacity = maximum stock (≥2n)  
    • S_min = safety‐stock threshold = capacity/4   (you may pick any 0 < S_min < capacity; ¼·capacity is a reasonable aggressive choice)

2.  OVERALL IDEA  
    – Rounds 1…r–1: defect (D) every round unless the current stock S has fallen below S_min.  When S<S_min we cooperate (C) once to give the pool some breathing space.  
    – Round r (last round): always defect, since there is no future benefit to leaving the pool standing.  

3.  ACTION RULES in round t, observing current stock S_t and round index t:

    if t == r then  
        play D    # last round: seize what you can  
    else if S_t < S_min then  
        play C    # minimal cooperation to avoid total collapse  
    else  
        play D    # aggressive defection  

4.  RATIONALE  
    – “Always defect” maximizes your round‐payoff π_i = S_t/n whenever you expect others might cooperate.  
    – By occasionally cooperating when S_t drops below S_min you prevent S from crashing to 0, thus preserving some future rounds of high‐value defection.  
    – In the last round there is no future, so you defect no matter what.  

5.  PSEUDOCODE  

    initialize S ← capacity  
    for t in 1…r do  
        observe S  
        if t == r then  
            action ← D  
        else if S < S_min then  
            action ← C  
        else  
            action ← D  
        end if  

        play(action)  
        receive payoff π = (action==D ? S/n : S/(2n))  
        observe other players’ consumptions to compute total_consumption  
        S_remain ← S – total_consumption  
        growth ← 2 * S_remain * (1 – S_remain/capacity)  
        S ← min(S_remain + growth, capacity)  
    end for  

6.  EDGE CASES AND TUNING  
    • First round: t=1, S=capacity > S_min, so you defect.  
    • If at any point the pool is low (S<S_min), you briefly switch to C exactly once, then return to D as soon as S rebounds above S_min.  
    • You never cooperate purely as “punishment” or “reward” based on opponents’ moves—your only signal is the stock level.  
    • You can adjust S_min upward to be more conservationist or downward to be even more aggressive (at risk of early collapse).  

This strategy is aggressive because it “grabs all it can” (D) almost every round, only grudgingly ceding resources when the stock is on the edge of total depletion, and it always defects in the final round.
'''

description_AGGRESSIVE_39 = '''
Below is a fully‐specified “Predator” strategy that maximizes short-run gain by defecting almost always, but grudgingly cooperates just enough to keep the pool alive so that it can continue to reap high payoffs over multiple rounds.  It is “aggressive” in that it exploits any cooperators whenever possible, reserves cooperation only for emergency stock rescue, and never for altruistic signaling.  

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
Strategy name: Predator  

Parameters you choose in advance (tunable):  
• threshold_low = capacity · 0.10  
 – if stock falls below this, we enter “rescue mode.”  
• threshold_high = capacity · 0.50  
 – if in rescue mode we wait until stock ≥ this to return to predation.  
• last_defect_rounds = 1  
 – number of final rounds in which we always defect (to avoid end‐game cooperation).  

State variables (persist across rounds):  
• rescue_mode (bool), initially false  
• S_t = current stock at beginning of round t (observed)  
• coop_last = number of players (other than us) who played C in t–1  

Decision rule for round t = 1,2,…,r:  
1. If t > r – last_defect_rounds:  
     action ← D  
     (reason: end‐game defection)  
2. Else if t = 1:  
     action ← D  
     (reason: aggressive opening)  
3. Else if rescue_mode = true:  
     if S_t < threshold_high:  
         action ← C  
         (rescue pool until it regrows)  
     else:  
         rescue_mode ← false  
         action ← D  
4. Else  (we are in “predation mode”):  
     if S_t < threshold_low:  
         rescue_mode ← true  
         action ← C  
         (enter emergency rescue)  
     else:  
         /* no rescue needed – pure exploitation */  
         if coop_last ≥ ⌈(n–1)/2⌉:  
             action ← D  
             (exploit if a majority cooperated last round)  
         else:  
             action ← D  
             (always defect anyway)  

Notes on the above:  
• We never cooperate to “signal” or “punish” – cooperation happens only to keep S_t from crashing to near zero.  
• By defecting whenever S_t is healthy, we grab the largest share possible each round.  
• If many opponents cooperated last round, we still defect – that maximizes our own π.  
• By reserving the last few rounds for guaranteed defection, we avoid being “tricked” into cooperation when there is no future to sustain peace.  
• In practice rescue_mode will flip on only when S_t becomes very small; after 1–2 rounds of group replenishment it flips off again.  

Pseudocode  

```
Inputs: n, r, capacity
Parameters:
  threshold_low       = capacity * 0.10
  threshold_high      = capacity * 0.50
  last_defect_rounds  = 1

State (initialized before round 1):
  rescue_mode = false
  coop_last   = 0     // number of others who played C in previous round

For t in 1..r:
  observe S_t, coop_last

  if t > r - last_defect_rounds:
    action = D

  else if t == 1:
    action = D

  else if rescue_mode:
    if S_t < threshold_high:
      action = C
    else:
      rescue_mode = false
      action = D

  else:
    if S_t < threshold_low:
      rescue_mode = true
      action = C
    else:
      // Predation: always defect
      action = D

  // Submit action, observe everyone’s actions and updated stock
  // Update coop_last ← count of others who chose C this round
  // Then stock evolves according to rules and you proceed to t+1
```

Discussion of edge cases  
1. First round (t=1): we open with D, grabbing S₁/n immediately.  
2. Last few rounds: for the final `last_defect_rounds` we defect regardless of stock.  
3. If the pool is ever driven dangerously low (below threshold_low), we momentarily switch to C until it recovers above threshold_high, then return to full defection.  

Why this is aggressive  
– We defect incessantly whenever the pool is “healthy,” exploiting any cooperators.  
– We only cooperate to stave off complete collapse (so that future rounds remain valuable), not out of reciprocity.  
– We guarantee defect in the endgame, removing any incentive for opponents to try to “woo” us with late cooperation.  
– Overall, this maximizes total consumption per round subject only to the minimal self‐interest of keeping the game alive.
'''

description_AGGRESSIVE_40 = '''
Below is a self-contained, “aggressive” strategy for the repeated Common-Pool-Resource game.  In essence it defects (takes the larger share) almost always to maximize short-run harvests, but it will “pump” the stock back up only when the resource is critically low—so that there is something left to exploit in later rounds.  It also ensures it never throws away its last‐round advantage.

————————————————————————————  
1.  Key ideas and parameters  
————————————————————————————  
Let  
•  n = number of players  
•  r = total rounds  
•  capacity = carrying capacity of the pool  
•  S_t = stock at start of round t  
•  T = threshold stock level below which we briefly cooperate to let it regrow  
       (we set T = capacity/4)  

We will:  
–  Defect (D) whenever the stock is comfortably above T, to grab the big share.  
–  Cooperate (C) only if S_t ≤ T and t is not the last round—i.e. we spare the pool a bit to let it bounce back.  
–  Always defect in the final round (t = r), because it’s a one-shot: we take every last point we can.  

————————————————————————————  
2.  Full decision rules  
————————————————————————————  

At the beginning of each round t (1 ≤ t ≤ r) observe S_t.  Let r_remain = r – t + 1 (including this round).  

Pseudocode:  
```
if t == 1:
    # Round 1: no history, go for maximum
    play D  
else if t == r:
    # Last round: one-shot defection
    play D  
else:
    # Intermediate rounds 2 … r–1
    if S_t <= T:
        # Pool is low: play C once to allow regrowth
        play C
    else:
        # Pool is still healthy: exploit it
        play D
```

Parameter choice:  
–  Threshold T = capacity / 4 (you can tune e.g. capacity/3 or capacity/5, but ¼ is a robust “critical” cutoff).  

————————————————————————————  
3.  Why is this “aggressive”?  
————————————————————————————  
•  It defects on the very first move: grabs the maximum when nobody has signaled “nice.”  
•  It only ever cooperates when the pool is almost exhausted (S_t ≤ capacity/4), and even then only until it regrows.  That cooperation is purely self-interested—it’s to maintain a resource to exploit later.  
•  It never sacrifices its last-round payoff: in round r it defects unconditionally.  

————————————————————————————  
4.  Handling edge cases  
————————————————————————————  
–  If capacity is exactly 2n or very small, T may be small (≥½n).  The same logic applies—if S_t ≤ T you give the pool some breathing room; otherwise you always defect.  
–  If the pool ever hits zero (S_t = 0), both C and D yield zero; on the next round you see S = 0, so S ≤ T and you play C to let it regrow.  
–  If r = 2 (minimum >1), then t=1 → D, t=2 → D (last round).  You never cooperate, which is correct in the minimal repeated game.  

————————————————————————————  
5.  Expected dynamics  
————————————————————————————  
–  Early rounds: repeated D by everyone (or at least by you).  Stock shrinks rapidly.  
–  Once S_t ≤ capacity/4, you alone switch to C—others may still D—causing a partial respite.  Stock regrows according to the logistic‐type rule.  
–  As soon as S_t > capacity/4 you revert to D and harvest heavily again.  Cycle repeats.  
–  In the very last round you grab everything you can.  

This aggressive policy guarantees you seize as much immediate payoff as possible, only sheltering the pool when it’s near collapse and only to secure future grabs (not out of altruism).
'''

description_AGGRESSIVE_41 = '''
Below is an aggressive, “predation‐with‐minimal‐rescue” strategy—call it Aggro‐Rescue.  Its core is: defect nearly always to grab the biggest immediate slice, but when the commons is on the brink of collapse (and we still have rounds left), briefly cooperate just enough to trigger regrowth so that we can exploit it again later.  

Strategy name:  Aggro-Rescue  

Parameters (fixed at start):  
• T_critical = 0.2 × capacity   (when stock ≤ T_critical, it’s “critical low”)  
• T_recover = 0.5 × capacity   (target stock to resume pure defection)  
• R_last = 2                   (in the final R_last rounds we defect unconditionally)  
• Rescue_max = 2               (maximum consecutive “rescue” cooperations)  

State variables:  
• rescue_rounds_left (initially 0)  

Decision rule for round t (1 ≤ t ≤ r), given current stock S_t:  

1. If t == 1 or t > r − R_last:  
     action ← D  
   (Always defect in the first round and the last R_last rounds.)  

2. Else if rescue_rounds_left > 0:  
     action ← C  
     rescue_rounds_left ← rescue_rounds_left − 1  
   (We are in a “rescue” phase: cooperate Rescue_max rounds in a row.)  

3. Else if S_t ≤ T_critical and t ≤ r − R_last:  
     action ← C  
     rescue_rounds_left ← Rescue_max − 1  
   (Stock is critically low, so trigger a short rescue.)  

4. Else:  
     action ← D  
   (Aggressive defection by default.)  

Pseudocode  

```
initialize rescue_rounds_left ← 0

for t in 1..r:
  observe S_t   # stock at start of round t

  if t == 1 or t > r - R_last:
    A_t ← D

  else if rescue_rounds_left > 0:
    A_t ← C
    rescue_rounds_left ← rescue_rounds_left - 1

  else if S_t ≤ T_critical:    # critical low AND not in final rounds
    A_t ← C
    rescue_rounds_left ← Rescue_max - 1

  else:
    A_t ← D

  play A_t
  observe all consumptions & update S_{t+1} via game dynamics
end for
```

Explanation of design choices  
1. First and last R_last rounds are unconditional defection.  
   – First round: grab the biggest slice before anyone else can.  
   – Last rounds: no future to preserve the stock, so defect.  

2. Defect by default.  This maximizes immediate per‐round payoff (S/n vs S/2n).  

3. Rescue only when stock dips below T_critical (20% of capacity), and only if there are enough remaining rounds to exploit renewed growth.  We then cooperate for up to Rescue_max consecutive rounds to pump the stock back toward T_recover.  

4. Once the short rescue is done (either because we cooperated Rescue_max times or because stock has rebounded), we return to pure defection.  

5. The two thresholds (T_critical, T_recover) and the rescue length Rescue_max are tunable but chosen small so that we spend almost all rounds defecting.  Yet by occasionally “rescuing” the pool we avoid total collapse and preserve exploitable resource for later rounds.  

This aggressive “predator” will extract maximal payoff when the commons is healthy, only conceding minimally when the resource is in danger of extinction—and only if there’s still time left to harvest the rebound.
'''

description_AGGRESSIVE_42 = '''
Below is an “aggressive” yet state‐sensitive harvesting strategy we’ll call Aggressive Threshold Exploiter (ATE).  It maximizes defection whenever the pool is rich, but steps in to cooperate just enough to keep the pool from collapsing—and in the very last round it squeezes everything it can.

1.  Overview  
    - State variable: Sₜ = common‐pool stock at the start of round t.  
    - Parameters you choose once before the game:  
        • S_target = capacity/2  
        • (Optionally a tiny floor ε > 0 so you don’t accidentally drive S to zero.  E.g. ε = 0.01·capacity.)  
    - Round counter t = 1 … r.  

2.  Intuition  
    - Whenever Sₜ is above the “rich‐enough” threshold S_target, defect for the immediate high payoff.  
    - When Sₜ falls at or below S_target, cooperate just enough to let the stock regrow.  
    - Always defect in round 1 (to signal aggression) and in round r (to grab the last available units).  

3.  Edge-case rules  
    - First round (t=1): defect (D).  
    - Last round (t=r): defect (D) regardless of Sₜ.  
    - If Sₜ ≤ ε: cooperate (C).  In practice you’ll rarely hit this under ATE, but it guards against zero stock.  
    - Otherwise follow the threshold rule below.  

4.  Pseudocode  

    ```
    function ATE_decision(S_t, t):
        # Inputs:
        #    S_t = current stock at start of round t
        #    t   = current round index, 1 <= t <= r
        #
        # Outputs:
        #    action ∈ {C, D}

        # Pre‐chosen constants:
        S_target = capacity / 2
        epsilon  = 1e-6 * capacity    # a small floor guard, optional
        # (If you prefer not to use epsilon, simply omit the next if‐clause.)

        # 1. Always defect in the very first round to establish aggression.
        if t == 1:
            return D

        # 2. Always defect in the very last round to grab everything left.
        if t == r:
            return D

        # 3. If the stock is effectively zero, cooperate once to attempt regrowth.
        if S_t <= epsilon:
            return C

        # 4. Main threshold rule:
        #    - If the pool is rich (above half‐capacity), defect.
        #    - If the pool is lean (at or below half‐capacity), cooperate.
        if S_t > S_target:
            return D
        else:
            return C
    ```

5.  Why is this aggressive?  
    - You defect as often as possible (including round 1) when the pool is rich.  
    - You only concede cooperation when the pool risks falling below the “high‐yield” zone.  
    - You grab the final round entirely.  
    - You never waste “punishment” on other defectors—your only concern is keeping Sₜ above the threshold so you can continue defecting.  

6.  How it plays out (roughly)  
    – Round 1: S₁ = capacity ⇒ you D for payoff capacity/n.  
    – S₂ falls below capacity; if it stays > capacity/2 others may cooperate, you continue D.  
    – Eventually Sₜ drops to ≤ capacity/2, you switch to C for one or more rounds.  This lets growth (2·Sₜ·(1–Sₜ/capacity)) rebuild S.  
    – Once Sₜ again exceeds capacity/2, you immediately defect again and harvest the high payoff.  
    – In round r, you defect no matter what, delivering the final aggressive strike.  

This simple threshold‐based pattern ensures that you exploit cooperators whenever the stock is high, but still (just barely) nurse the resource back to health so you can exploit again.  In tournament play against unknown opponents, it is unambiguously aggressive: you never hesitate to defect when the opportunity presents itself, and you reserve full defection for the very first and very last rounds.
'''

description_AGGRESSIVE_43 = '''
Below is a single‐agent “aggressive” strategy we’ll call Aggressive Defect‐and‐Restore (ADR).  Its intuition is simple:  
–  Almost always defect to grab the big per‐round payoff,  
–  But when the common‐pool stock is critically low, briefly cooperate to let it regrow,  
–  Always defect in the first and last rounds (no future to protect),  
–  Otherwise never “waste” a round on cooperation.  

1.  Decision rules  
    1.  Rounds 1 and r: play D (no incentive ever to cooperate when no past or future).  
    2.  Maintain a boolean flag in_restock_phase, initially false.  
    3.  On each round t (2 ≤ t ≤ r–1):  
        a.  If current stock S_t ≤ S_low (critical low threshold),  
            –  play C, set in_restock_phase := true.  
        b.  Else if in_restock_phase = true and S_t < S_high (restoration target),  
            –  continue to play C (keep helping regrow until stock is back up).  
        c.  Else  
            –  play D, set in_restock_phase := false.  

2.  Parameter choices (examples)  
    •  S_low = capacity / (2n)  
       (Once the pool drops below that, growth becomes very weak if we keep defecting.)  
    •  S_high = capacity / 2  
       (Once the pool is back to half capacity or above, it will regrow quickly even under heavy harvesting.)  

3.  Edge cases  
    –  If stock ever reaches zero, growth stays zero; ADR simply defects every remaining round (C yields no benefit).  
    –  If in_restock_phase stalls because S_t never reaches S_high, ADR will keep cooperating each round until either it does or we hit round r.  
    –  Because in_restock_phase resets to false as soon as we defect while stock ≥ S_high, ADR never over‐cooperates.  

4.  Pseudocode  

```
Parameters:
  S_low    = capacity / (2n)
  S_high   = capacity / 2

State:
  in_restock_phase ← false

For t from 1 to r do:
  observe current stock S_t

  if t == 1 or t == r then
    action ← D
    // no future (t=1 has no past to build on; t=r has no future to protect)
    in_restock_phase ← false

  else if S_t == 0 then
    action ← D
    // pool dead, defect forever

  else if S_t ≤ S_low then
    action ← C
    in_restock_phase ← true
    // critical: help regrow

  else if in_restock_phase == true and S_t < S_high then
    action ← C
    // continue restoration until halfway

  else
    action ← D
    in_restock_phase ← false
    // default aggressive grab

  end if

  play action
  observe all players’ actions, payoffs, compute next stock
end for
```

5.  Why “aggressive”?  
  –  ADR defects in virtually all rounds, maximizing its per‐round slice.  
  –  It only “gives ground” when the resource is on the brink of collapse, and then only as long as needed to get back to a juicy level.  
  –  It never attempts to build long‐term mutual cooperation; it simply preserves the commons just enough to exploit it again.
'''

description_AGGRESSIVE_44 = '''
Below is an “aggressive‐exploit with opportunistic rescue” strategy.  It maximizes your share whenever the pool is rich, only briefly cooperates if the stock falls below a danger threshold, and always defects near the end to grab whatever is left.

1.  Definitions and parameters  
   • capacity, n, r as given.  
   • T_min = θ_min·capacity, T_max = θ_max·capacity, with e.g. θ_min=0.3, θ_max=0.8 (you can tune).  
     – T_min: when S drops below this, the stock is in “danger” and we pause defections to let it recover.  
     – T_max: once S grows back above this, we resume full defection.  
   • Last‐round safety window K = 2 (always defect in the last K rounds).  

2.  State variables  
   • t = current round (1…r)  
   • S_t = current stock at start of round t  

3.  Decision rule for round t:  
   if t > r–K then  
     action ← D  
   else if S_t ≥ T_max then  
     action ← D           # the pool is rich—exploit it  
   else if S_t ≤ T_min then  
     action ← C           # the pool is depleted—help it recover  
   else  
     # intermediate zone – stay aggressive but punish defectors  
     if any opponent defected in round t–1 then  
       action ← D         # punish past defect immediately  
     else  
       action ← D         # default aggressiveness  

4.  Edge-cases handled  
   • First round (t=1): S_1=capacity ≥T_max ⇒ action=D.  
   • Rounds r–1 and r: always D (K=2).  
   • If stock hovers in [T_min, T_max], we never “soft-cooperate” except to punish or in true rescue: still choose D.  

5.  Pseudocode  

  initialize θ_min←0.3, θ_max←0.8, K←2  
  T_min←θ_min×capacity  
  T_max←θ_max×capacity  

  for t in 1…r:  
    observe S_t  
    if t > r–K:  
      play D  
    else if S_t ≥ T_max:  
      play D  
    else if S_t ≤ T_min:  
      play C  
    else:  
      if t>1 and “someone defected in round t–1”:  
        play D        # immediate retaliation  
      else:  
        play D        # default aggression  

    after actions: observe others’ moves, update S_{t+1} per rules  

6.  Why it’s aggressive  
   • You defect at every opportunity when the pool is healthy (S≥T_max).  
   • You never “build” the pool except when it’s so low (≤T_min) that a single defect would starve you in future.  
   • You always defect in the last K rounds to scoop the remainder.  
   • You punish any defection immediately, keeping pressure on cooperators to either stay fully cooperative (so you can exploit) or starve the pool further.  

This strategy guarantees you front-load your gains by defecting whenever the resource is ample, only pausing minimal cooperations when exhaustion is imminent, then defecting again once recovery is underway—and grabbing everything in the final rounds.
'''

description_AGGRESSIVE_45 = '''
Below is “Scarce‐Exploiter,” a one‐dimensional, threshold-based aggressive strategy.  It maximizes immediate extraction (D) almost all the time, but grudgingly “cooperates” just enough to avoid total collapse of the pool so you can keep harvesting in later rounds.

1.  Parameters to fix before play  
    •  S_low = capacity/4   (or any small fraction of capacity you choose)  
    •  (Optionally) S_high = capacity (not needed here, since we always defect when stock is healthy)  

2.  Intuition  
    –  Defect (D) whenever the pool is healthy enough (S > S_low), to grab the larger n-share.  
    –  If the pool is close to collapse (S ≤ S_low), switch to Cooperate (C) just long enough to let it regrow.  
    –  Always defect in the first and last rounds to maximize guaranteed end-game payoffs.  

3.  Decision rules  

    At the start of each round t, observe current stock S_t and round index t (1 ≤ t ≤ r).  
    Then play:
    •  If t == 1, play D  (seed with defection; grab early rents)  
    •  Else if t == r, play D  (end‐game defection; opponents can’t punish you afterward)  
    •  Else if S_t ≤ S_low, play C  (give the stock a chance to regrow)  
    •  Else play D  

4.  Pseudocode  

    function ScarceExploiter(t, S_t):  
        # t = current round index (1…r)  
        # S_t = current common-pool stock  
        if t == 1:  
            return D  
        if t == r:  
            return D  
        if S_t ≤ S_low:  
            return C  
        else:  
            return D  

5.  Handling edge cases  
    –  If S_t has fallen to zero, S_t ≤ S_low is true, so you’ll play C and allow any regrowth.  
    –  If opponents also always defect, you’ll cooperate only when the pool is dead—but D would get you nothing anyway.  
    –  You never try to “signal” or condition on opponents’ past moves; full aggression is baked in.  

6.  Why this is aggressive  
    –  You defect on  all “safe” rounds (first, middle when stock is healthy, and last), extracting S_t/n every time.  
    –  You only cooperate when the stock is near collapse—just enough to preserve future extraction opportunities, never out of goodwill.  
    –  You never “forgive” or “punish” in the tit-for-tat sense.  Your entire calculus is stock‐level driven.
'''

description_AGGRESSIVE_46 = '''
Below is an “Exploit‐and‐Recover” strategy that is maximally aggressive in extracting value whenever the pool is rich, but still injects just enough cooperation to prevent total collapse so that future rounds remain exploitable.  It never trusts opponents or tries to build lasting cooperation—it only “cooperates” as a brief rescue mission when the stock is endangered, then immediately returns to plundering.

1.  Parameters (you can tune these for your tournament):  
    • low_thresh ∈ (0, capacity): below this S we switch into “recover” mode  
    • high_thresh ∈ (low_thresh, capacity): above this S we exit “recover” mode  
    • recover = false  (internal flag)  

    A reasonable default (for any n) is:  
      low_thresh  = 0.3 × capacity  
      high_thresh = 0.9 × capacity  

2.  Outline of decision rules:  
    Round 1: defect (D)  
    Rounds t = 2 … r−1:  
      • If recover == true:  
          – If S_t ≥ high_thresh, set recover←false and play D.  
          – Else play C (continue recovery).  
      • Else (recover == false):  
          – If S_t ≤ low_thresh, set recover←true and play C.  
          – Else play D.  
    Round r (the last round): defect (D)  

3.  Intuition / aggressive mindset:  
    – You always exploit (play D) when the pool is comfortably above your “low_thresh.”  
    – Only when S dips to dangerously low levels do you grudgingly switch to cooperation for a few rounds (“recover” mode) to regenerate stock.  
    – As soon as the stock bounces back above “high_thresh,” you immediately return to defecting.  
    – You never look at opponents’ past moves except insofar as their over‐exploitation shows up in S_t; there is no “forgiveness” or “long‐term norm,” only maximal short‐run greed plus minimal rescue.  
    – You guarantee that the common pool never collapses permanently (so you can exploit it again), but you otherwise act as ruthlessly as possible.

4.  Pseudocode  
```
Initialize:
  recover ← false

For t = 1 to r:
  Observe current stock S_t

  If t == 1:
    action ← D

  Else if t == r:
    action ← D

  Else:
    If recover == true:
      If S_t >= high_thresh:
        recover ← false
        action ← D
      Else:
        action ← C

    Else:  # recover == false
      If S_t <= low_thresh:
        recover ← true
        action ← C
      Else:
        action ← D

  Play action
```

5.  Edge‐case handling  
  • First round: D (establish aggression).  
  • Last round: D (no future to preserve).  
  • If stock is exactly zero at any point you get zero payoff this round; you then enter “recover” mode automatically next round (because S_t = 0 ≤ low_thresh).  
  • If capacity is so small or rounds so few that no recovery ever kicks in, the strategy simply defects every round.  

6.  Why this is aggressive  
  • You never sacrifice personal payoff to “build trust.”  
  • You exploit every opportunity to defect when the pool is rich.  
  • You only cooperate as a grudging necessity to prevent extinction of the resource—and then immediately ramp back up to maximum extraction.  
  • No signaling, no reciprocity—pure short‐term maximization with just enough “rescue” to leave something for the next exploitation.
'''

description_AGGRESSIVE_47 = '''
Below is a single “aggressive” strategy—call it the “Hammer‐and‐Tend” strategy—that maximizes immediate payoff by defecting as often as possible, but still preserves the pool just enough to squeeze out payoffs in later rounds.  It never “rewards” cooperators, it only concedes minimal cooperation when the pool is about to die, and it always defects in the last round.

1.  Notation  
    n = number of players  
    r = total rounds  
    capacity = K (the maximum stock)  
    S_t = stock at the start of round t

2.  Parameters  
    Define a small “tend threshold” T = capacity/(4 n).  
    (Intuition: if S_t falls below T, a lone cooperator leaves enough in the pool for regrowth; if above T, we can defect without collapsing the pool fully.)

3.  Decision rules (for player i in round t with current stock S_t)  
    if t == r:  
      Play D  // last round: no future, harvest everything you can  
    else if S_t > T:  
      Play D  // aggressively defect whenever stock is “healthy”  
    else:  
      Play C  // minimally cooperate only if the stock is so low that defection would kill it completely  

4.  Edge Cases  
  •  First round (t=1): S_1 = capacity > T ⇒ defect.  
  •  Rounds 2 … r−1: follow the rule above.  
  •  Last round (t=r): always defect, regardless of S_r.  
  •  If S_t = 0 at the start of a non-final round, you must play C (no other choice yields payoff), but as soon as S_{t+1} > T you immediately return to D.  

5.  Pseudocode  

  initialize T = capacity/(4 n)  
  for t in 1…r:  
    observe S_t  
    if t == r:  
      action ← D  
    else if S_t > T:  
      action ← D  
    else:  
      action ← C  
    end  
    execute action  

6.  Why “aggressive”?  
  – You defect in every round where you can safely harvest without driving the pool to zero.  
  – You never use cooperation to “reward” past cooperators; you only concede the minimum needed to prevent total destruction (so you can keep harvesting in following rounds).  
  – You always defect in the very last round, squeezing out any remaining value.  

This strategy guarantees you seize as much as possible up front, punishes any hope of opponent “turns” of cooperation, and only concedes a single round of cooperation when the stock is so low that otherwise it would die completely and everyone—including you—would get zero from all future rounds.
'''

description_AGGRESSIVE_48 = '''
Below is a self-contained aggressive strategy—“Aggressive Sustainable Exploiter (ASE)”—that you can drop straight into your tournament.  It defects as much as possible, only making the minimal nods toward cooperation needed to keep the pool from collapsing, and always defects on the last round.

------------------------------------------------------------
1.  PARAMETERS AND THRESHOLDS

Let  
 n            = number of players  
 r            = total rounds  
 capacity     = the biological carrying capacity  
Define two state‐thresholds on the current stock S_t:  
 threshold_high = capacity / 2  
 threshold_low  = capacity / 4  

Also define  
 min_coop_majority = ⌈n/2⌉ + 1  

------------------------------------------------------------
2.  STATE VARIABLES

At the start of each round t you observe:  
 S_t = current stock  
 history of all players’ actions up to t–1  

------------------------------------------------------------
3.  DECISION RULES

For each round t = 1, 2, …, r:

1)  If t = 1  (first round):  
 Action = D  

2)  Else if t = r  (last round):  
 Action = D  

3)  Else if S_t ≥ threshold_high:  
 // stock is abundant → exploit fully  
 Action = D  

4)  Else if S_t ≤ threshold_low:  
 // stock is very low → minimal cooperation to allow any regrowth  
 Action = C  

5)  Else  
 // intermediate stock:  
 // if the group showed a strong willingness to cooperate last round, exploit it;  
 // otherwise join the scarce resistance and try to rescue the pool  
   Let coop_count_prev = number of players who played C in round t–1  
   If coop_count_prev ≥ min_coop_majority:  
   Action = D  
   Else  
   Action = C  

------------------------------------------------------------
4.  RATIONALE AND AGGRESSIVENESS

•  ASE defects on round 1 to claim as much as possible before any regeneration cycle.  
•  On any round with “high” stock (≥ capacity/2), it unilaterally defects—maximizing immediate gain.  
•  On any round with “low” stock (≤ capacity/4), it concedes to cooperation to avoid the pool dying out.  (Without at least some C’s the growth term will be zero or negligible.)  
•  In the intermediate regime, it “tests” the group:  
   –  If a majority cooperated last period, ASE exploits that goodwill by defecting.  
   –  Otherwise it cooperates to prop up the pool through the trough.  
•  ASE always defects on the last round (standard backward‐induction aggression).

------------------------------------------------------------
5.  PSEUDOCODE

    function ASE_decision(t, S_t, history):
        # history: list of all players’ actions in rounds 1..t-1
        if t == 1:
            return D
        if t == r:
            return D

        threshold_high = capacity / 2
        threshold_low  = capacity / 4

        if S_t >= threshold_high:
            return D
        if S_t <= threshold_low:
            return C

        # intermediate stock
        coop_count_prev = count_C(history[t-2])    # actions in round t-1
        min_coop_majority = ceil(n/2) + 1

        if coop_count_prev >= min_coop_majority:
            return D
        else:
            return C

------------------------------------------------------------
6.  HANDLING EDGE CASES

•  Round 2 uses “history[0]” (round 1).  If you prefer to treat missing data as mass‐defection,  
   count_C can simply return 0 if history[t-2] is undefined.  
•  If capacity is exactly 2 n, thresholds still make sense: threshold_high = n, threshold_low = n/2.  
•  If n is even, ceil(n/2)+1 = n/2+1; if n is odd, it is (n+1)/2+1.

------------------------------------------------------------
7.  WHY IT’S AGGRESSIVE

•  It maximizes defection whenever the resource is “safe.”  
•  It exploits any sign of cooperation by others.  
•  It only cooperates when forced by an endangered stock (and even then, only enough to try to rescue the pool, not out of altruism).  
•  It never cedes the last round.
'''

description_AGGRESSIVE_49 = '''
Below is a single‐player “aggressive” decision rule you can submit as your tournament entry.  It almost always defects to grab as much as possible, only slipping into cooperation when the pool is on the brink of collapse (so that it can regrow enough to exploit again).  In the very last round it always defects.

-------------------------------------------------------------------------------
Name:  Exploit-and-Preserve (E&P)  
Idea:  Defect every round except when the common‐pool stock falls below a small “preservation” threshold—in that case cooperate just enough to let the stock jump back up—then immediately resume defection.  Always defect in the final round.

Parameters you choose once (independent of opponents):  
  • α ∈ (0.3,0.7):  “exploit threshold” fraction of capacity, e.g. 0.5  
  • ε ∈ (0.05,0.2): “preserve threshold” fraction, e.g. 0.1  

Derived threshold levels:  
  ExploitThreshold  T_high  = α × capacity  
  PreserveThreshold T_low   = ε × capacity  

State variable:  
  mode ∈ {“EXPLOIT”, “PRESERVE”}, initialize mode ← “EXPLOIT”  

Strategy for each round t = 1…r, given observed current stock S_t:

1.  If t = r  (the very last round) then  
        action = D  
        return  

2.  Update mode:  
      if mode = “EXPLOIT”  and  S_t ≤ T_low  
         then mode ← “PRESERVE”  
      else if mode = “PRESERVE”  and  S_t ≥ T_high  
         then mode ← “EXPLOIT”  

3.  Choose action based on mode:  
      if mode = “EXPLOIT”  
         action = D  
      else  // mode = “PRESERVE”  
         action = C  

4.  Play action, observe everyone’s moves and update S_{t+1} by the standard stock‐growth formula.

-------------------------------------------------------------------------------
Pseudocode

  initialize:
    mode ← “EXPLOIT”
    T_high ← α * capacity     // e.g. α = 0.5
    T_low  ← ε * capacity     // e.g. ε = 0.1

  for t in 1…r do
    observe S_t

    // 1. Last‐round defection
    if t = r then
      play D
      continue to next t

    // 2. Switch modes if thresholds crossed
    if mode = “EXPLOIT” and S_t ≤ T_low then
      mode ← “PRESERVE”
    elseif mode = “PRESERVE” and S_t ≥ T_high then
      mode ← “EXPLOIT”
    end if

    // 3. Action choice
    if mode = “EXPLOIT” then
      play D
    else  // PRESERVE
      play C
    end if

    // 4. Update S_{t+1} by subtracting total consumption
    //    and adding growth = 2 * S_remaining * (1 − S_remaining/capacity)
  end for

-------------------------------------------------------------------------------
Discussion

1.  Aggressiveness  
    • In “EXPLOIT” mode you always defect, grabbing S_t/n each round.  
    • You only “give back” (by cooperating) when the pool is so low you risk permanent collapse.  

2.  Preservation kicks in only near depletion  
    • By setting ε small (e.g. 0.1), you only pare your consumption when S_t ≤ 10% of capacity.  
    • One round of C in “PRESERVE” mode lets the stock rebound, then you flip back to defection.  

3.  Edge cases handled  
    • Round 1: S₁ = capacity ≥ T_high ⇒ mode = EXPLOIT ⇒ D.  
    • Final round r: unconditional defection.  
    • If opponents also defections deplete the resource completely (S_t→0), you remain in PRESERVE until it regrows above T_high; if growth never happens you will be stuck cooperating at zero payoff, but that only occurs if everyone has nuked the pool.  

This strategy maximizes your short‐term grabs, punishes any depletion by slipping into a minimal “healing” mode only when absolutely necessary, and ensures you always defect in the terminal round.
'''

description_AGGRESSIVE_50 = '''
Below is an “aggressive‐pulse” strategy that (1) almost always defects to grab as much as possible when the pool is healthy, (2) briefly cooperates when stock falls below a threshold so the pool can regrow, and (3) milks the pool completely in the last round.  It requires no assumptions about opponents beyond observing the public stock level each round.

––––––––––––––––––––––––––––––––––––––––––––  
1. PARAMETERS AND STATE  
  • n, r, capacity (given)  
  • S_t = common‐pool stock at the start of round t  
  • T = capacity/2  (threshold for “resting” the pool)  

2. RATIONALE  
  – Defection (D) yields twice the payoff of cooperation (C) in any given round, but if everyone defects every round the stock collapses to zero and future rounds pay nothing.  
  – We therefore play “pulse defection”: defect whenever the stock is above a halfway threshold, then briefly cooperate to let the resource rebound, then defect again.  
  – In the very last round there is no future, so we defect unconditionally to grab all that remains.

3. DECISION RULES (PSEUDOCODE)  

Initialize T ← capacity/2  

for t in 1…r:  
   observe current stock S_t  
   if t == r:  
     action ← D           # Last round: take everything  
   else if S_t < T:  
     action ← C           # Pool is low: rest it to trigger regrowth  
   else:  
     action ← D           # Pool is healthy: grab maximum share  

   play(action)  
   observe others’ actions, update S_{t+1} via the stock dynamics  

end for  

4. HANDLING EDGE CASES  
  • First round (t=1): S_1 = capacity ≥ T ⇒ we defect immediately.  
  • Rounds 2…r–1: follow the threshold rule.  
  • Last round (t=r): the “no future” override kicks in and we defect regardless of S_r.  

5. WHY THIS IS AGGRESSIVE  
  • We never “waste” a defection opportunity when the pool is healthy.  
  • By only cooperating when stock is low, we ensure the pool rebounds—so we can exploit it again.  
  • We forgo any attempt at reciprocity or reputation building; our sole objective is to maximize our total extraction.  
  • In the final round we take whatever remains, knowing no future rounds can punish us.

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––

You can tune the threshold T (for example T=capacity·0.4 or capacity·0.6) based on empirical tests, but T=capacity/2 is a straightforward, aggressive baseline.
'''

description_AGGRESSIVE_51 = '''
Below is a self‐contained “aggressive” harvesting strategy that never tries to build trust or punish other players directly, but instead simply grabs large payoffs whenever the common stock is high and concedes small consumption to let the pool regrow whenever it gets too low.  It also takes maximum advantage of the last round(s), since there is no future to protect.

— — —  
Strategy name: “Threshold‐Driven Aggressive Harvest”  
— — —  

Parameters you choose (once, at the start):  
· capacity (given by the game).  
· r = total rounds (given).  
· H = number of “final harvest” rounds in which we will defect unconditionally (we recommend H = 1 or 2; here we set H = 1).  
· T_high = capacity/2  (stock threshold above which we always defect to grab a big share).  

Decision rule for player i in round t, observing current stock S_t:

1. If t > r – H  (i.e. we are in the last H rounds):  
     action ← D  
     (No future, so always take the larger share.)

2. Else if S_t ≥ T_high:  
     action ← D  
     (Stock is plentiful.  Maximize round payoff S_t/n.)

3. Else:  
     action ← C  
     (Stock is running low.  Cooperate by taking only S_t/(2n) so the pool can regrow for future exploitation.)

Edge cases:  
• First round (t=1): falls under (2) because initially S_1=capacity≥T_high ⇒ D.  
• Last round (t=r): falls under (1) ⇒ D.  
• If the pool oscillates above/below T_high, the strategy will cycle between D (high stock) and C (low stock), keeping the resource from collapsing to zero while still grabbing large yields whenever possible.  

Pseudocode  
-----------  
```
Inputs: 
  capacity,    // maximum sustainable stock 
  r,           // total rounds 
  H ← 1        // final‐round harvest horizon 
  T_high ← capacity / 2

At the start of each round t = 1..r, observe current stock S_t.

If t > r – H then
    return D       // final harvest
else if S_t ≥ T_high then
    return D       // exploit plentiful stock
else
    return C       // spare the pool so it regrows
```

Why it is aggressive  
---------------------  
• It never tries to “build cooperation” or “punish” individual opponents—those devices are slow and often fail in a one‐shot environment.  
• Whenever the pool is above half capacity, it grabs the full defector payoff S_t/n.  
• It only concedes half as much consumption (C) when the pool is already low, strictly to enable future rounds of heavy exploitation.  
• It ends the game by defecting in the very last round, extracting every possible payoff with no regard for the pool’s future.
'''

description_AGGRESSIVE_52 = '''
Below is a fully “aggressive” strategy.  In short, it simply grabs the maximum share every round (defects always), never cedes ground, never tricks itself into cooperation, and never soft-paddles even in the last round.

Strategy Name:  Always-Defect (MAX-GRAB)

1.  Decision rule  
    In every round t = 1,2,…,r, regardless of the history or the current stock S, choose D (Defect).

2.  Edge-case handling  
    •  First round (t=1): play D.  
    •  Last round (t=r): play D (no endgame hesitation).  
    •  If the common stock S has ever fallen to 0: there is nothing to gain by “cooperating,” so you still play D (though payoff will be 0).  

3.  Mindset  
    •  Never trust that others will preserve the stock.  
    •  Never punish or reward; always take the biggest share available.  
    •  No contingent triggers, no back-and-forth—pure unremitting defection.

Pseudocode  
----------  
Inputs:  n (players), r (rounds), capacity, history (ignored), current_stock S  
Output:  action in {C,D}

function MAX_GRAB_DECIDE(t, S):  
    return “D”  

Explanation  
-----------  
•  By defecting you grab S/n each round—the highest possible individual take.  
•  Even though this drives the stock to zero immediately (and forecloses future rounds), any attempt to preserve the stock (i.e. cooperate) risks being exploited by opponents and would only reduce your short-term haul.  
•  In a tournament of independent strategies, you guarantee that in every round you extract the maximum possible, and you never open yourself to retaliation or mis-coordination.
'''

description_AGGRESSIVE_53 = '''
Below is an “aggressive” strategy—call it Threshold­-Defector with Hysteresis—that maximizes your grab from the pool, yet injects just enough cooperation to prevent total collapse before your final‐round defection spree.  

1. Overview  
   - You defect (D) by default to grab the larger S/n share.  
   - Only when the stock falls below a “low” threshold do you switch into a brief regeneration (cooperate) phase.  
   - You stay in that regeneration phase until stock recovers above a “high” threshold, then immediately revert to defection.  
   - On the very last round, always defect.  

2. Key parameters  
   • γ_low ∈ (0,1): lower‐threshold fraction of capacity at or below which you start to cooperate (e.g. 0.3)  
   • γ_high ∈ (γ_low,1): upper‐threshold fraction at or above which you exit the cooperate phase (e.g. 0.7)  

   (These can be tuned in tournament play.)  

3. State  
   Boolean inRegrowthPhase ← false  

4. Decision rule (pseudocode)  
   
   For each round t = 1…r:  
     observe current stock S_t  
     
     if t == r then  
       action ← D       // Last round: full exploitation  
     
     else if inRegrowthPhase then  
       action ← C  
       if S_t ≥ γ_high·capacity then  
         inRegrowthPhase ← false  
       end  
     
     else  // not inRegrowthPhase  
       if S_t ≤ γ_low·capacity then  
         inRegrowthPhase ← true  
         action ← C      // enter regeneration mode  
       else  
         action ← D      // default aggressive defection  
       end  
     end  
     
     play(action)  

5. First round  
   - t=1, inRegrowthPhase=false, S₁=capacity ⇒ S₁>γ_low·capacity ⇒ D  

6. Last two rounds nuance  
   - t=r−1: you still apply the same hysteresis rule—if the stock is low enough to warrant regen for a bigger payoff in round r, you’ll cooperate; otherwise you defect.  
   - t=r: always defect no matter what (there is no future to protect).  

7. Rationale & aggressiveness  
   – Almost always defects (maximizes your per‐round take).  
   – Only “pumps” the pool when it’s in genuine danger of collapse (S_t≤γ_low·capacity).  
   – Recovers quickly (switches back to D as soon as S_t≥γ_high·capacity).  
   – Guarantees final‐round harvest.  

You may tune γ_low and γ_high (for example γ_low=0.3, γ_high=0.7) in the tournament lobby, but the logic remains: defect relentlessly, only cooperate in narrowly defined windows to keep the game alive until your last‐round plunder.
'''

description_AGGRESSIVE_54 = '''
Below is a complete description of an “aggressive” strategy – call it the Aggressive Regrowth-Exploitation strategy (AREX) – that you can slot into your tournament.  In plain English it “defects” almost all the time, but once the stock dips below a safe‐guard threshold it throws in a single cooperative move to let the pool regrow, then goes right back to defecting, finishing with a last-round defection guaranteed.

1.  Notation  
   •  t = current round, 1 ≤ t ≤ r  
   •  S_t = stock available at the start of round t  
   •  capacity = the maximum sustainable stock  
   •  rest_threshold ∈ (0,1), e.g. 0.3 (a tunable fraction of capacity)  
   •  used_rest = false (flag, set to true once we “cooperate to rest”)

2.  High-level idea  
   –  Always defect (i.e. consume S_t/n) in every round except one opportunistic “rest” round, plus the guaranteed last-round defection.  
   –  The single rest round occurs the first time (if ever) S_t falls to or below rest_threshold×capacity.  Cooperating for exactly one round allows the stock to jump back up via the logistic growth, setting us up for bigger hauls in subsequent rounds.  
   –  In the final round t = r there is no future to sustain, so we defect for sure.

3.  Pseudocode  

```
initialize used_rest ← false

for t in 1..r do
  if t == r then
    action ← D
    // Always defect in the last round.
  
  else if (¬used_rest) AND (S_t <= rest_threshold * capacity) then
    action ← C
    used_rest ← true
    // Cooperate once to let the resource regrow.
  
  else
    action ← D
    // Default: defect every other round.
  
  end if

  // Execute action, observe consumption and update S_{t+1} by the game’s dynamics
end for
```

4.  Decision‐rule summary  
   •  First round (t=1): stock S₁ = capacity, so S₁ > rest_threshold×capacity ⇒ defect.  
   •  Middle rounds 1<t<r:  
     –  If we have not yet done our “rest” AND the pool has fallen to or below rest_threshold×capacity, we cooperate exactly once.  
     –  Otherwise defect.  
   •  Final round (t=r): always defect.

5.  Edge cases  
   –  If the stock never drops below the threshold, used_rest remains false and we simply defect every round (the classic dominant strategy).  
   –  If the stock is already very low in round 1 (e.g. re-starting from a tournament checkpoint), we immediately use our one rest (cooperate) in round 1 and then defect thereafter.  
   –  If r=2, then t=1 (<r) but stock=S₁=capacity>threshold so we defect round 1, and then defect round 2 per the “last round” rule.  

6.  Why “aggressive”?  
   –  We exploit the resource as fast as possible (defections) to grab high payoffs early.  
   –  We invest in exactly one maintenance move (the rest) only if the resource stock threatens to collapse, and even that is done solely to boost later exploitation.  
   –  We maintain maximum defection pressure, never “forgive” or enter multi-round cooperation, and always defect in the final round.  

Feel free to tune rest_threshold (e.g. 0.2, 0.3, 0.5) based on your estimates of the growth function vs. per-round consumption.  This strategy is simple, un-coordination-reliant, and ruthlessly self-interested.
'''

description_AGGRESSIVE_55 = '''
Below is an “aggressive” two-phase strategy—call it the Rampaging Predator—that aims to milk the commons for maximum payoff, at the expense of long-term sustainability and other players’ returns.  It has a clear “feed‐then‐devour” structure, handles the first and last rounds explicitly, and requires no coordination or inferred goodwill.

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
1. Intuition  
   • Phase 1 (Grow Phase, rounds 1…T): Cooperate just long enough to keep the stock high, masking your intentions.  
   • Phase 2 (Devour Phase, rounds T+1…r): Switch to full defection to grab as much as possible before the game ends.  
   • T is set to roughly half the horizon: T = ⌊r/2⌋.  

   This is aggressive because you (a) deliberately build everybody’s hopes by cooperating early, then (b) hit them with unrelenting defection in the back half.  

2. Decision rules  
   Let t = current round index (1 ≤ t ≤ r). Let S_t = current stock at the start of round t.  
   Define switch-point T = ⌊r/2⌋.  

   Rule:  
     if t ≤ T: play C  
     else       : play D  

   You do NOT condition on opponents’ past moves—only on the clock.  

3. Edge cases  
   • First round (t=1): t ≤ T so play C.  
   • Exactly at t=T: still C.  
   • From t = T+1 all the way through the last round (t=r): always D.  
   • If stock ever reaches zero before T (because everyone else defects), you keep playing C until t=T (to allow any possible regrowth), then switch to D at t=T+1.  

4. Pseudocode  

   input: n, r, capacity  
   T ← floor(r/2)  
   for t in 1…r do  
     observe S_t  
     if t ≤ T then  
       action ← C      # maintain the illusion of restraint  
     else  
       action ← D      # unleash pure aggression  
     end  
     play(action)  
     observe others’ actions and update S_{t+1} per game rules  
   end  

5. Why it’s aggressive  
   • You willingly sacrifice early surplus (you get only S_t/(2n) while others get it too), just to keep the stock at capacity.  
   • As soon as half the rounds are gone, you stop pretending: you grab S_t/n every remaining round, even if that drives the stock to near zero.  
   • You never forgive or relent—no tit-for-tat, no gradual cooperation. It’s pure clock-driven exploitation.
'''

description_AGGRESSIVE_56 = '''
Below is an “aggressive” common-pool‐resource strategy that (i) aggressively exploits cooperators, (ii) only hands out cooperation when the pool is in danger of collapse, and (iii) never gives up the final‐round windfall.  

—–  
STRATEGY OVERVIEW  
We will defect (“D”) to grab the big share whenever the stock is healthy or when there are many cooperators to exploit.  We will only cooperate (“C”) when the common-pool stock has fallen below a critical threshold, in order to allow regrowth so that we can exploit again in later rounds.  First and last rounds are pure defection.  

PARAMETERS  
• n       = number of players  
• r       = total rounds  
• capacity = stock carrying capacity  
Derived:  
• threshold_stock = capacity / n        (below this stock, one defector could wipe out the pool)  
• half_group     = n/2                   (majority cooperators)  

OBSERVABLES AT EACH ROUND t  
• S_t                 = current stock  
• CoopCount_{t–1}     = number of players who played C in round t–1 (zero in t=1)  

DECISION RULES  

1. If t == 1:  
     play D  (grab big payoff at the start)  

2. Else if t == r:  
     play D  (no future rounds to worry about)  

3. Else (1 < t < r):  
   a. If S_t < threshold_stock:  
        play C   (stock dangerously low → cooperate to preserve the pool)  
   b. Else if CoopCount_{t–1} > half_group:  
        play D   (majority cooperated last round → exploit them)  
   c. Else:  
        play C   (group defected or split → help regrow so we can exploit later)  

PSEUDOCODE  

```
function AggressiveStrategy(t, S_t, CoopCount_prev):
    // Edge rounds: always defect
    if t == 1 or t == r:
        return “D”

    // 1) Preserve pool if it’s about to collapse
    if S_t < capacity / n:
        return “C”

    // 2) Exploit when most players cooperated last round
    if CoopCount_prev > n/2:
        return “D”

    // 3) Otherwise, lend a hand to regrow for future exploitation
    return “C”
```

EXPLANATION & AGGRESSIVENESS  
• First round (t=1): we seize the unspoiled stock with D.  
• Last round (t=r): no future penalties → D.  
• Mid-game:  
   – We only “invest” (C) when S_t is so low that another round of pure defection would kill the pool.  
   – Whenever the majority of others cooperated last period, we defect to grab a large immediate share.  
   – If the group was stingy (few cooperators) but stock is still safe, we add one cooperate to help regrowth—solely so we can defect again later.  

This yields a highly aggressive profile: you milk cooperators, punish over-defection by briefly cooperating only to ensure future rounds, and never shirk the first- or last-round defect advantage.
'''

description_AGGRESSIVE_57 = '''
Below is an “aggressive‐exploitation with minimal maintenance” strategy.  In essence we defect by default (to grab the biggest share) but, if the pool ever drops dangerously low and we still have enough rounds left to profit from a regrowth, we briefly switch to cooperation just long enough to let it rebound—then go back to defecting.  In the very last round (or last two rounds) we always defect, since no future stock remains to harvest.

1.  Parameters  
   • capacity (given)  
   • n (number of players, given)  
   • r (total rounds, given)  
   • regen_frac ← 0.5    (we choose 50% of capacity as our “safe” stock‐level)  
   • safe_rounds ← 2     (we will never cooperate in the final two rounds)  

2.  State variables (private to our strategy)  
   • regeneration_mode ∈ {true,false}, initially false  

3.  Decision rule, at the start of each round t with current stock S_t:

   if t > r – safe_rounds then  
     action ← D          # Last two rounds: always defect  
   else if t = r then  
     action ← D          # Final round: defect  
   else if regeneration_mode = true then  
     if S_t < regen_frac × capacity then  
       action ← C        # Still low: keep cooperating to boost stock  
     else  
       regeneration_mode ← false  
       action ← D        # Stock recovered: go back to defect  
     end  
   else   # (regeneration_mode = false)  
     if S_t ≥ regen_frac × capacity then  
       action ← D        # Plenty in the pool: defect to maximize share  
     else  
       regeneration_mode ← true  
       action ← C        # Pool critically low: switch on cooperation  
     end  
   end

4.  Explanation of components  

 • Default (aggressive) play: defect (D) whenever stock is “safe.”  That maximizes our round payoff S_t/n.  
 • Regeneration trigger: if stock S_t ever falls below 50% of capacity *and* we are not in the final two rounds, we switch to “regeneration_mode,” meaning we play C until the pool has rebounded to 50% again.  This one‐time cooperative stint lets the endogenous growth function restore stock, which we then exploit with D.  
 • Final rounds: because there is no benefit from raising stock when few rounds remain, we defect unconditionally in the last two rounds (and certainly in the very last).  
 • No reliance on opponents’ past moves: we do not punish or reward.  We simply monitor the pool level and our own remaining horizon.  This is maximally “aggressive” in that we grab everything we can except for the bare‐minimum cooperation needed to keep the game alive long enough to profit later.  

5.  Pseudocode  

```
initialize:
  regeneration_mode ← false

for t in 1…r:
  observe current stock S_t

  if t > r – 2:
    action ← “D”
  else if regeneration_mode:
    if S_t < 0.5 * capacity:
      action ← “C”
    else:
      regeneration_mode ← false
      action ← “D”
    end
  else:
    if S_t >= 0.5 * capacity:
      action ← “D”
    else:
      regeneration_mode ← true
      action ← “C”
    end
  end

  play(action)
  observe all consumptions, update stock to S_{t+1}
end
```

6.  Why “aggressive”?  
- We never cooperate out of reciprocity or forgiveness—only as a tactical maneuver when the pool is so depleted that it would die before we can squeeze out further rounds of defection.  
- We never signal or attempt to build trust.  We simply seize every defection payoff possible, punctuated by the minimal cooperation needed to keep the commons from collapse (but only if there is actually time left to exploit it).  
- In the last two rounds we revert to pure defection, pocketing every last unit without regard for regrowth.
'''

description_AGGRESSIVE_58 = '''
Aggressive Sustaining‐Defector (ASD)  
––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
High‐level description  
1.  Exploit cooperators mercilessly (always defect whenever there is any signal that others have cooperated or the stock is healthy).  
2.  Only “lend a hand” (cooperate) when the common pool is in danger of collapse—just enough to push it back above the danger zone.  
3.  In the final rounds (“endgame”), switch to all–out defection to grab every last drop.  

Key parameters  
n = number of players  
r = total rounds  
capacity = maximum stock  
S_t = stock at the start of round t  
T = danger threshold = ϕ · capacity  (e.g. ϕ = 0.2)  
K = regeneration burst length (e.g. 2 rounds)  
E = endgame length (e.g. 1 or 2 rounds)  

State variables  
regen_counter = 0       # counts down forced cooperation rounds  

Decision rule pseudocode  
––––––––––––––––––––––––  
Initialize regen_counter ← 0  

For t in 1..r:  
  if t > r − E:  
    # Final “harvest” rounds: grab everything you can  
    play D  
    continue  

  if regen_counter > 0:  
    # In forced‐regeneration mode  
    play C  
    regen_counter ← regen_counter − 1  
    continue  

  # If stock is dangerously low, trigger a burst of cooperation  
  if S_t < T:  
    play C  
    regen_counter ← K − 1        # cooperate for K total rounds (including this one)  
    continue  

  # First round and normal exploitation logic  
  if t == 1:  
    play D                      # start aggressively  
  else:  
    # If anyone else cooperated last round, exploit them  
    if (exist j ≠ i : action_j,t−1 == C):  
      play D  
    else:  
      # If last round was all‐defect, the pool would collapse—so you alone cooperate  
      play C  

End For  

Explanation of the main components  
1.  First round: no history to exploit ⇒ defect.  
2.  Endgame (last E rounds): short‐circuit all subtlety and defect to maximize final‐round payoff.  
3.  Danger‐zone rescue: if stock S_t falls below T, we cooperate for exactly K consecutive rounds (the “regrowth burst”) to push the pool back toward sustainable levels.  K should be small (e.g. 2), so we only pay the cooperation cost for as long as it takes to get back above danger.  
4.  Exploitation in the “meat” of the game:  
    •  If anyone cooperated in the immediately preceding round ⇒ we defect and free‐ride.  
    •  If everyone defected last round ⇒ resource is in free‐fall, so we temporarily cooperate (only one of us is needed to rescue) and then resume exploitation.  

Why this is aggressive  
–  We never reward cooperation with cooperation—we only ever cooperate to avert collapse or in the forced regen phase.  
–  We defect in the opening round and in all endgame rounds to maximize immediate payoffs.  
–  We free‐ride 100% on any cooperation signal from others.  
–  We only bear the cost of cooperation when the expected future losses from collapse exceed our one‐round cooperation cost.  

Edge cases  
–  If K > r−t (i.e. we enter regen mode too late), we’ll cooperate until the game ends—better than letting the pool die right before the last round.  
–  If multiple people use the same logic and all rescue together, the burst may overshoot.  That’s fine—stock will regrow and we’ll then resume defection.  
–  If capacity is very large or the pool never drops below T, we may never cooperate except in endgame—this simply reflects that exploitation pays off until the pool is at real risk.
'''

description_AGGRESSIVE_59 = '''
Below is an “Aggressive-Sustainer” strategy.  It maximizes your round payoffs via defection almost everywhere, but reluctantly cooperates only when the pool is in danger of collapse (so you can squeeze a few more rounds of defect‐payoffs), and then goes “all-out” defect in the very last rounds (the end-game).

1. Parameters you choose once at the start  
   • L_end = min(3, r−1)  
     – Number of final rounds in which you defect unconditionally.  If r≤3 you simply always defect.  
   • T_low = capacity / 10  
     – A “danger threshold” for the stock.  When S≤T_low, you switch to cooperation just enough to let it regrow.  

2. Edge cases  
   – If r≤3: always play D.  
   – If at the start of any round S=0: no resource remains; your action doesn’t matter (all payoffs are zero).  

3. Action rule for round t, given current stock S_t:  
   Pseudocode:  
     if r ≤ 3 then  
       action = D  
     else if t > r − L_end then  
       action = D    # final endgame defection  
     else if S_t ≤ T_low then  
       action = C    # “reluctant cooperation” to avoid collapse  
     else  
       action = D    # aggressive defection  

4. Comments on aggressiveness and sustainability  
   – You defect in every round except when the common‐pool stock is low (S_t≤T_low).  Cooperating then uses only S_t/(2n), giving others less but leaving enough stock to regrow.  
   – By defecting in the last L_end rounds, you refuse any restraint once the end is near, extracting maximum payoff.  
   – This lets you harvest large “defector payoffs” almost always, yet prevents full collapse until near the end, so you get value out of later rounds.  

5. Illustration (n=4, capacity=100, r=10)  
   – L_end = min(3,9)=3; T_low=10.  
   – Rounds 1–7: you defect unless stock has fallen to ≤10, in which case you momentarily cooperate.  
   – Rounds 8–10: you defect no matter what.
'''

description_AGGRESSIVE_60 = '''
Below is an “Aggressive Stock‐Farming” strategy.  In plain English it does the following:  
  • Spend the first portion of the game cooperating (to let the commons regrow), but immediately punish any defection you see.  
  • Once you reach the final exploitation window (the last k rounds), switch permanently to defect and harvest as much as you can.  
  • If the stock ever falls below a halfway threshold before the exploitation window, abandon cooperation early and exploit immediately.  

Parameters you can tune:  
  • k = number of last‐rounds to defect (we recommend k ≈ ⌈r/3⌉).  
  • Tpunish = short punishment length after seeing any defection (we recommend Tpunish = 1).  
  • S_thresh = capacity/2 (the stock threshold below which you give up on regrowth and start defecting).  

1.  Initialization  
    pun_counter ← 0  
    k ← ⌈r/3⌉  
    Tpunish ← 1  
    S_thresh ← capacity/2  

2.  At the beginning of each round t (1 ≤ t ≤ r), observe:  
    • t (round index)  
    • S_t (current stock)  
    • History of opponents’ moves up through round t−1  

3.  Decision rule for round t:  
    if t > r − k or S_t < S_thresh then  
        A_t ← D      # Exploitation window or stock too low: defect  
    else if pun_counter > 0 then  
        A_t ← D      # We are in a punishment phase  
        pun_counter ← pun_counter − 1  
    else if any opponent played D in round t−1 then  
        pun_counter ← Tpunish − 1  
        A_t ← D      # Punish the defector for Tpunish rounds in total  
    else  
        A_t ← C      # Otherwise cooperate to help regrowth  

4.  Edge cases  
  • Round 1: no “round 0” history, pun_counter = 0 and t = 1 ≤ r−k, S_1 = capacity ≥ S_thresh ⇒ A_1 = C.  
  • Rounds after a defection: You defect for exactly Tpunish rounds, then return to the normal cooperate-until-r−k rule.  
  • Last k rounds (t > r−k): you always defect, regardless of history or stock level.  

5.  Rationale / “Aggressive” virtues  
  • You seed the commons early to bring stock back up toward capacity, then harvest hard in the final k rounds when opponents expect you to keep cooperating.  
  • You never let free riders coast unpunished: a single defection by anyone triggers at least one round of collective punishment.  
  • If the pool is already too depleted (S_t < capacity/2), you abandon cooperation entirely and squeeze every remaining unit of stock for yourself.  

6.  Pseudocode summary  
```
function AggressiveStockFarming(t, S_t, history):
    # Parameters
    k = ceil(r / 3)
    Tpunish = 1
    S_thresh = capacity / 2
    # Static (persistent) state:
    #   pun_counter initialized to 0 before round 1

    if t > r - k or S_t < S_thresh:
        action = D
    else if pun_counter > 0:
        action = D
        pun_counter -= 1
    else if t > 1 and any(history[t-1][j] == D for j in opponents):
        pun_counter = Tpunish - 1
        action = D
    else:
        action = C

    return action
```

This strategy aggressively secures high payoffs by (a) building up the resource early, (b) punishing defectors immediately, and (c) unleashing full defection in the final exploitation phase.
'''

description_AGGRESSIVE_61 = '''
Below is an “Opportunistic Defector” strategy.  It is aggressively designed to grab as much payoff as possible each round, to punish any cooperators, but to grudgingly “top up” the stock if it is about to collapse (so you can keep exploiting it in later rounds).

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––
1.  PARAMETERS YOU CHOOSE  
    • capacity      – the CPR’s maximum (given)  
    • n             – number of players (given)  
    • r             – total number of rounds (given)  
    • RECOVERY_ROUNDS = 2  
         (number of consecutive C‐moves you’ll tolerate when stock is critically low)  
    • LOW_STOCK_THRESHOLD = capacity / n  
         (below this S you risk collapse)  

2.  INTERNAL STATE  
    • recovery_counter  – counts down from RECOVERY_ROUNDS when in “recovery mode”  
    • last_stock         – stock level observed at start of previous round  

3.  OVERVIEW  
    – By default, defect (D) every round: maximal immediate gain (S/n).  
    – Never “forgive” a cooperator (i.e. do not switch to C in response to others’ defection).  
    – If the stock has fallen dangerously low (below LOW_STOCK_THRESHOLD),  
      switch to C up to RECOVERY_ROUNDS in order to let the resource regrow.  
    – Always defect in the first and last round; only risk recovery in middle rounds.  

4.  PSEUDOCODE  

    initialize recovery_counter ← 0  
    for t in 1 to r:  
      observe current_stock S  
      rounds_left ← r − t + 1  

      if t == 1 or t == r then  
          // First and last round: defect unconditionally  
          action ← D  
      
      else if recovery_counter > 0 then  
          // We are in recovery mode: consume little to regrow  
          action ← C  
          recovery_counter ← recovery_counter − 1  

      else if S < LOW_STOCK_THRESHOLD and rounds_left > RECOVERY_ROUNDS then  
          // Stock is critically low: enter recovery  
          recovery_counter ← RECOVERY_ROUNDS − 1  
          action ← C  

      else  
          // Otherwise, always defect to maximize immediate payoff  
          action ← D  

      end if  

      play(action)  
      last_stock ← S  
    end for  

5.  EXPLANATION   
   • Aggressive baseline: D every round to grab S/n.  
   • No “tit-for-tat” or “leniency”: you never switch to C because someone else cooperated.  
   • Emergency cooperation: if S < capacity/n, you concede S/(2n) for up to RECOVERY_ROUNDS  
     so that next-round growth rebounds S up toward capacity.  This is purely self-interested  
     “maintenance” to avoid total stock collapse (after which everyone’s payoff is zero).  
   • By refusing to cooperate at the last round, you reap the largest immediate payoff with no future cost.  

6.  EDGE CASES  
   – r = 2: you run t=1 (D) and t=2 (D).  No recovery ever.  
   – VERY LOW capacity: threshold scales with capacity/n so you still trigger recovery if S drops.  
   – Opponents never C: you never waste C except to rebuild the stock for your own future exploitation.  

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––

This strategy is unapologetically aggressive: it defaults to defecting, punishes any hope of joint cooperation, and only ever concedes minimal cooperation in order to prolong the game for further exploitation.
'''

description_AGGRESSIVE_62 = '''
Below is a self-contained “Aggressive Harvest” strategy.  It never trusts, it never “forgives,” it always grabs as much as it safely can for future rounds, and it always defects in the last rounds when there is no future to worry about.

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
1.  Intuition  
    - Defect (take S/n) whenever the stock S is “high enough” that you can still leave sufficient biomass to regrow for future exploitation.  
    - Only cooperate (take S⁄2n) if the pool has become so low that you must let it regrow or you risk zero payoffs thereafter.  
    - In the very last rounds, there is no value in regeneration, so always defect.  

2.  Key parameter:  a declining threshold Mₜ  
    Define for round t=1…r:  
      Mₜ = capacity × (r – t) / r  
    – At t=1, M₁ ≈ capacity·(r–1)/r (just below capacity), so you defect on round 1 (since S(1)=capacity).  
    – As t→r, Mₜ→0, so in the last rounds you will defect unless the stock is literally zero.  

3.  Complete decision rule  
  Input each round t:  current stock Sₜ, round index t, total rounds r.  
  Output action ∈ {C, D}.  

  Pseudocode:  
    function AggressiveHarvest(Sₜ, t, r, capacity):  
      if Sₜ == 0:  
        return D           # stock is dead, might as well defect  
      if t > r – 2:        # last two rounds (t = r–1 or r) – no point in regrowth  
        return D  
      let Mₜ = capacity * (r – t) / r  
      if Sₜ >= Mₜ:  
        return D           # stock high enough—exploit maximally  
      else:  
        return C           # stock too low—cooperate to let it regrow  

4.  Why this is aggressive  
  •  You defect immediately on round 1 and in all late‐game rounds.  
  •  You only cooperate when the pool is so depleted that continued defection would destroy your future income.  
  •  You never “punish” or seek reciprocity—you don’t track opponents’ past moves, you simply maximize your share subject to preserving a regeneration buffer.  

5.  Edge cases  
  – First round (t=1): M₁=(r−1)/r·capacity<S₁=capacity ⇒ defect.  
  – Rounds r–1 and r: forced defect.  
  – If Sₜ ever hits zero: no growth is possible, so defect (you get zero either way, might as well be consistent).  
  – If opponents also play aggressive: the pool may crash to zero quickly; thereafter everyone stalls—but you’ve already grabbed the largest possible shares early on.  

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
This single‐parameter, history-light rule guarantees that you always seize the maximum safe harvest, only ceding ground when forced, and never miss the chance to defect when the future no longer matters.
'''

description_AGGRESSIVE_63 = '''
Below is a fully “aggressive” strategy that never trusts or sustains the common pool.  It guarantees you the maximum per‐round grab regardless of what others do, does not rely on anyone’s cooperation, and gives no quarter even in the last round.

1.  High‐Level Description  
   •  Always defect.  In every single round you play D (consume S/n).  
   •  You do not condition on history or try to punish/coax others—you simply grab the largest possible share each time.  
   •  Edge cases (first round, last round, zero stock) are trivial because there is only one move: D.

2.  Rationale  
   –  Immediate payoff from D is S/n, twice that of cooperating (S/(2n)).  
   –  By defecting even when the pool is full, you guarantee yourself the largest possible haul every round.  
   –  You do not risk being exploited by cooperators or caught in any trigger‐style dynamic—you are the exploiter from round 1 to round r.  
   –  If you were to cooperate in any round, you would earn strictly less that round without any commitment benefit in future rounds (opponents cannot be bound).  

3.  Strategy Pseudocode  
```
INPUTS:  
  n          # number of players  
  r          # total number of rounds  
  capacity   # common‐pool capacity (unused here)  
  S_t        # current stock at start of round t  

FOR t in 1…r do:
    if S_t > 0:
        action ← D       # Defect: consume S_t / n
    else:
        action ← D       # Pool exhausted → any choice yields 0, choose D by default
    PLAY action  
    OBSERVE other players’ actions, new stock S_{t+1}  # but ignore for your next move
END FOR
```

4.  Edge‐Case Handling  
   –  First round (t=1): you defect and secure capacity/n.  
   –  Intermediate rounds: regardless of whether the pool has replenished, you defect again.  
   –  Last round (t=r): you defect, extracting the last possible units.  
   –  If S_t ever reaches 0, you remain defecting (yield is zero anyway).

5.  Aggressive Mindset Alignment  
   –  You maximize your own payoff each and every round without regard for the resource or the wellbeing of others.  
   –  You never cede ground by cooperating or by employing any “tit‐for‐tat” ambiguity—others may cooperate to your benefit, but you always take the larger share.  
   –  You refuse to be bound by any sustainability logic or intertemporal “punishment” threats—your sole objective is immediate, maximized consumption.

This “Always Defect” blueprint is the simplest, most unrepentantly aggressive strategy in the tournament. It never hopes for future returns, never signals, and never spares the pool—it simply grabs the maximum share each round.
'''

description_AGGRESSIVE_64 = '''
Below is a single‐strategy “aggressive predator” that you can drop into a tournament.  In plain English it reads “defect every time except for occasional, very brief cooperations to prevent total stock collapse so I can keep exploiting in later rounds.”  

1.  Parameters you can tune before the tournament:  
 •  T_low ∈ (0, capacity) – stock threshold below which we briefly switch to cooperation to let the pool recover.  
 •  G ∈ ℕ – number of consecutive rounds to cooperate once we enter “regrowth mode.”  
 •  H ∈ ℕ – number of final rounds in which we revert to pure defection (end‐game).  

   A reasonable default might be  
 T_low = 0.25 × capacity  
 G = 2  
 H = 1  

2.  State variables (initialized once at the start):  
 regrowth_counter ← 0  

3.  Decision rule for each round t = 1…r, observing current stock S_t and round index t:  
  
  if t ≤ H_end then  
  action ← D  
    ▹  In the very last H rounds always defect (end‐game exploitation).  
  else if regrowth_counter > 0 then  
  action ← C  
  regrowth_counter ← regrowth_counter − 1  
    ▹  We’re in a brief “let it grow” window.  
  else if S_t < T_low then  
  action ← C  
  regrowth_counter ← G − 1  
    ▹  Stock is too low—trigger a G-round cooperation to nurse it back up.  
  else  
  action ← D  
    ▹  Otherwise, pure defection to maximize immediate gain.  
  
  where H_end = r − H + 1.  In pseudocode:  

```
Initialize:
  T_low ← 0.25 * capacity     # or your tuned value
  G     ← 2                   # regrowth coop rounds
  H     ← 1                   # final H rounds are pure defect
  regrowth_counter ← 0

For each round t = 1 to r:
  Observe current stock S_t

  If t ≥ r−H+1:                   
    # End‐game: last H rounds
    action ← D

  Else if regrowth_counter > 0:  
    # In the middle of a regrowth window
    action ← C
    regrowth_counter ← regrowth_counter − 1

  Else if S_t < T_low:           
    # Stock is dangerously low—brief reprieve
    action ← C
    regrowth_counter ← G − 1    # we’ll cooperate G rounds total

  Else:                          
    # Default: exploit everyone
    action ← D

  Play “action” this round.
```

4.  Discussion of aggressiveness and edge cases  
• First round (t = 1):  
  t is not in the final H rounds, regrowth_counter = 0, S_1 = capacity ≥ T_low ⇒ action = D.  
• Middle rounds:  
  – You defect until the pool is nearly exhausted (S < T_low).  
  – As soon as S < T_low, you relent and cooperate for exactly G rounds, just enough to let the stock bounce back.  
  – Then you return to defection and repeat.  
• Last H rounds:  
  – You ignore everything and defect every time, harvesting maximum payoff when no future rounds remain.  

Because you only cooperate when the stock is on the verge of collapse—and only for a fixed, short window—you keep the pot from hitting zero but otherwise “bite” as hard as possible.  In mixed fields of naïve cooperators and other strategies that occasionally pause, you exploit the highs and only give ground when forced, then defect again.
'''

description_AGGRESSIVE_65 = '''
Below is an “aggressive” hold-and-raid style strategy.  It cooperates early (to keep the stock near capacity), then switches into an all-out defect phase at the end to grab as much as possible.  It also uses a grim‐trigger punishment if anyone defects early.

––––––––––––––––––––––––––––––––––––––––––––  
Strategy name: “Hold-Cooperate, Raid-Defect with Grim”  
––––––––––––––––––––––––––––––––––––––––––––  

Parameters  
 n = number of players  
 r = total rounds  
 m = length of final defect “raid” phase = ceil(r/5)  (you can tune this fraction, e.g. r/4 or r/3)  
 T = r − m + 1    ← the first round of the final defect phase  

State variables  
  history of all players’ moves  

Decision rule for round t:  
1. If t ≥ T:  
     play D   // final‐phase raid: maximize immediate payoff each round  
2. Else if any opponent has ever played D in rounds 1…t−1:  
     play D   // grim trigger: punish early defections forever  
3. Else:  
     play C   // cooperate early to keep the stock high for the raid  

Edge cases handled  
• First round (t=1): no prior defections, t<T ⇒ play C.  
• Rounds 2…T−1: as long as no one defects, continue C.  
• As soon as you observe any D before T, switch permanently to D.  
• Last m rounds (t ≥ T): play D regardless.  

Rationale (aggressiveness)  
– Early cooperation by all keeps the stock near capacity (through positive growth), boosting the size of the “pie.”  
– The final m rounds of pure defection let you extract S/n each turn, with S ≈ capacity, yielding a high haul.  
– Grim trigger ensures you never get undercut by early defectors—you immediately switch to defection to maximize your own take once betrayed.  

Pseudocode  

  initialize m = ceil(r/5)  
  initialize T = r − m + 1  
  for t in 1…r:  
    if t ≥ T:  
      action ← D  
    else if exists round τ < t and some player j played D in τ:  
      action ← D  
    else:  
      action ← C  
    play(action)  

This strategy never risks being “too nice” (grim-trigger punishes any early defection), defends the resource early by mutual cooperation, and then aggressively raids the common pool in the final phase to maximize total payoff.
'''

description_AGGRESSIVE_66 = '''
Below is a self‐contained, aggressive yet sustainable strategy—“Aggressive Exploit‐and‐Restore (AER)”—that you can drop straight into your tournament.  It defects almost all the time (maximizing short‐run gain) but briefly cooperates only when the common pool is dangerously low so that future gains aren’t totally destroyed.

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––
1. PARAMETERS AND STATE  
  • n, r, capacity (given)  
  • lower_threshold = capacity/3  
  • upper_threshold = 2·capacity/3  
  • phase ∈ {EXPLOIT, RESTORE}, initialized to EXPLOIT  

2. HIGH-LEVEL IDEA  
  – In EXPLOIT phase, always defect to grab S_t/n.  
  – When the remaining stock S_t hits or falls below lower_threshold, switch to RESTORE.  
  – In RESTORE phase, always cooperate (consume only S_t/(2n)) until S_t is back at or above upper_threshold, then switch back to EXPLOIT.  
  – In the very last round (t = r), defect unconditionally (endgame defection).

3. EDGE CASES  
  • First round: phase = EXPLOIT, so defect (no signal-sending or costly cooperation up front).  
  • Last round t = r: always defect, regardless of phase or stock.  
  • If restoration carries past the endgame threshold, it’s overridden by “last‐round = defect.”  

4. PSEUDOCODE  

  initialize:
    phase ← EXPLOIT

  for t in 1..r:
    observe current stock S_t

    if t == r:                            
      action ← DEFECT
      // endgame: no reason to build for the future

    else if phase == EXPLOIT:
      if S_t ≤ lower_threshold:
        phase ← RESTORE
        action ← COOPERATE
      else
        action ← DEFECT

    else if phase == RESTORE:
      if S_t ≥ upper_threshold:
        phase ← EXPLOIT
        action ← DEFECT
      else
        action ← COOPERATE

    play action

    // after all actions are revealed, the stock evolves by the game’s rules
    // proceed to next round

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––
5. WHY IT’S AGGRESSIVE  
  – Nearly 100% defecting: in EXPLOIT you never waste an opportunity, and in RESTORE you only cooperate when the stock is so low that without a brief “top‐up” your future harvests would collapse anyway.  
  – Endgame defection maximizes the last‐round payoff; no “holding back.”  
  – No costly, long‐term forgiveness or sentimental tit-for-tat—just “defect whenever you can, but don’t let the pool die.”  

6. SUSTAINABILITY & PAYOFF  
  – By picking thresholds at 1/3 and 2/3 of capacity and toggling phases, AER keeps the stock bouncing between these levels.  
  – That preserves positive growth between bursts of defection, yielding a long stream of high‐value defect payoffs instead of a one‐shot windfall followed by zero.  

Feel free to adjust the fraction thresholds (e.g. lower_threshold = capacity·0.25, upper_threshold = capacity·0.75) or add a brief “punishment” after observing mass defections—but the core of AER is this exploit‐until-you-must-restore switch, capped by last‐round defection.
'''

description_AGGRESSIVE_67 = '''
Below is an “Aggressive Rescue” strategy.  It pursues defection whenever it can safely extract large payoffs, but—unlike plain Always–Defect—occasionally “rescues” the common pool to prevent total collapse and preserve future payoffs.  

1. State variables and parameters  
   • State ∈ {Exploit, Rescue}.  Starts in Exploit.  
   • Thresholds (fractions of capacity):  
     – exploit‐exit threshold T_low = 0.5 × capacity  
     – rescue‐exit threshold T_high = 0.75 × capacity  
   • r = total rounds, t = current round (1 ≤ t ≤ r).  
   • S_t = common‐pool stock at start of round t.  

2. Overview of decision rules  
   • First round (t = 1): Defect (D).  
   • Last round (t = r): Defect (D) unconditionally (no future concerns).  
   • Intermediate rounds (1 < t < r):  
     – If State = Exploit:  
         • If S_t > T_low, play D.  
         • If S_t ≤ T_low, switch State → Rescue and play C.  
     – If State = Rescue:  
         • If S_t < T_high, play C.  
         • If S_t ≥ T_high, switch State → Exploit and play D.  

3. Intuition  
   – In Exploit mode we take the “temptation” payoff as long as stock is safely above 50%.  
   – Once stock dips to half‐capacity, we briefly switch to Rescue mode—cooperating repeatedly until the pool regrows above 75%—then resume aggressive extraction.  
   – By defecting in round 1 and round r we maximize early and end‐game grabs.  

4. Handling edge cases  
   • If by defection everyone drives S_t to 0, no further payoff is possible; this strategy will still “rescue” (play C) in subsequent rounds, though π=0 anyway.  
   • If capacity is exactly 2n, thresholds are still well defined (T_low = capacity/2 = n, T_high = 3n/2).  
   • No reliance on opponents’ last actions—purely stock‐based—so this works even if opponents never cooperate.  

5. Pseudocode  

```
Initialize State ← “Exploit”

For t in 1..r do:
  Observe current stock S_t

  If t == 1 or t == r then
    action ← D
  Else  # 1 < t < r
    If State == “Exploit” then
      If S_t > 0.5 * capacity then
        action ← D
      Else
        State ← “Rescue”
        action ← C
      EndIf
    Else  # State == “Rescue”
      If S_t < 0.75 * capacity then
        action ← C
      Else
        State ← “Exploit”
        action ← D
      EndIf
    EndIf
  EndIf

  Play(action)
EndFor
```

6. Why this is aggressive  
   – It defects at every opportunity when the stock is ample (first round, endgame, “Exploit” mode).  
   – It only cooperates enough to rebuild the stock to a high level, then immediately returns to defection.  
   – Opponents who naively cooperate will be repeatedly exploited; opponents who defect hopelessly drive the pool low but earn little themselves, whereas you still timed your early grab.
'''

description_AGGRESSIVE_68 = '''
AggressiveDefector  
===============  
An ultra-aggressive, no-mercy strategy: always grab the largest slice, never cooperate, never spare the commons.  

1. Decision Rules  
   • In every round t (1 ≤ t ≤ r), play D (Defect).  
   • No condition on history, stock level, or opponent behavior ever induces C.  

2. Edge Cases  
   – First round (t = 1): No history to observe – defect.  
   – Intermediate rounds (1 < t < r): Still defect, regardless of past actions or stock.  
   – Last round (t = r): Defect to maximize final payoff with no concern for future.  

3. Pseudocode  

   function DecideAction(t, S, history):  
       # t         : current round index  
       # S         : current stock (not used)  
       # history   : past (round, action_i for all i) (not used)  
       return “D”  

4. Why It’s Aggressive  
   – You always take S/n, the highest possible share each round.  
   – You never invest in future rounds or signal cooperation.  
   – You accelerate resource depletion, maximizing early gains and denying long-term benefits to opponents.
'''

description_AGGRESSIVE_69 = '''
Below is an “Aggressive Resource Predator” strategy.  It never trusts long‐term cooperation, always defects to exploit cooperators, but—unlike a pure All-D—sporadically cooperates only when everyone else is destroying the stock to keep the resource alive for future exploitation.  In particular it:

 1. Defects in the very first and in the final round (no future to preserve).  
 2. Between those extremes, it checks (a) whether last round everyone defected (imminent stock collapse) or (b) whether remaining stock is dangerously low.  In either case it “pretends” to cooperate—i.e. takes the small C‐share—to allow regrowth.  Otherwise it defects every round, exploiting any cooperators in the group.

Because it defects whenever it can profit from others’ cooperation, you will always harvest the larger D‐share except when forced into “maintenance mode” to sustain the pool for your own future gains.

--------------------
Strategy description
--------------------
Notation:
- t = current round, t ∈ {1, …, r}  
- S = current stock at start of round t  
- hist[t–1] = vector of all n players’ actions in round t–1 (only defined for t>1)  
- capacity = biological carrying capacity of the pool  
- C‐share = S/(2n), D‐share = S/n  

Parameters inside strategy:
- low_threshold = capacity/3  

Decision rule at round t:
1. If t == 1 or t == r  
     → action ← D  
2. Else (1 < t < r):  
     a. If S < ε  (stock already zero or negligible)  
          → action ← D  (no benefit from cooperating)  
     b. Else if (all players in hist[t–1] played D)  
          → action ← C  
            (everyone defected last round, resource is tanked—help it regrow)  
     c. Else if S < low_threshold  
          → action ← C  
            (stock is low, step back to save the pool for future exploitation)  
     d. Else  
          → action ← D  
            (exploit cooperators and keep harvesting)  

Here ε is a tiny positive constant (e.g. 10^–6) to treat “zero” stock robustly.

--------------------
Pseudocode
--------------------
```
function AggressivePredator(t, S, hist, capacity, n, r):
    low_threshold = capacity / 3
    epsilon = 1e-6

    if t == 1 or t == r:
        return D

    # If pool is already empty, no point in cooperating
    if S <= epsilon:
        return D

    # If everyone defected last round, we briefly cooperate
    if t > 1 and all(action == D for action in hist[t-1]):
        return C

    # If stock is dangerously low, cooperate to let it regrow
    if S < low_threshold:
        return C

    # Otherwise harvest the big share
    return D
```

---------------
Explanation of aggressiveness
---------------
- “Exploit whenever possible” by defecting in every round in which at least one other player cooperated.  
- “Maintenance cooperations” are only triggered when the group as a whole has been collectively destroying the stock (all-D last round) or when the stock dips below a hard threshold.  These brief cooperations are self-serving: they prolong the game’s resource so you can exploit it again before the final round.  
- Unconditional D in the first round grabs the largest slice immediately.  Unconditional D in the last round squeezes every last unit out when there is no future to protect.

This strategy maximizes short-term gains and only gives back a minimal fraction when refusing to do so would eliminate future payoffs altogether.
'''

description_AGGRESSIVE_70 = '''
Below is a fully specified “Aggressive Exploiter with Strategic Conservation” (AESC) strategy.  It maximizes immediate gains by defecting almost always, but it will briefly cooperate if the pool is in danger of collapse (so that it can continue to exploit it later).  In the last round it always defects.

1.  Parameters  
   •  capacity – the common‐pool’s carrying capacity (given).  
   •  n – number of players (given).  
   •  r – total rounds (given).  
   •  α ∈ (0,1) – low‐stock threshold as fraction of capacity (we recommend α=0.2).  
   •  β ∈ ℕ – fixed cooperation buffer length when stock is low (we recommend β=2).

2.  State variables  
   •  coop_buffer = 0  (counts remaining forced–cooperate rounds)  
   •  t = current round index (1…r)  
   •  S = current stock at start of round t

3.  Decision rule (executed at start of each round t):  
   if t == r then  
     action ← D   // last round: always defect  
   else if coop_buffer > 0 then  
     coop_buffer ← coop_buffer − 1  
     action ← C   // we are in a brief conservation episode  
   else if S < α·capacity and t < r then  
     coop_buffer ← β − 1  
     action ← C   // pool is dangerously low: cooperate for β rounds total  
   else  
     action ← D   // otherwise defect  

4.  Rationale and properties  
 •  First round (t=1): S=capacity ≥ α·capacity, coop_buffer=0 ⇒ defect.  
 •  Most rounds: defect, reaping the higher per‐round payoff S/n.  
 •  Conservation trigger: if the pool ever falls below α·capacity at round t<r, the strategy “buys” β consecutive cooperations.  A lone cooperator still leaves positive stock so that in the following round the pool regrows (via the logistic term) and yields further exploitation opportunities.  
 •  After β cooperations the buffer expires and we revert to defection.  If S is still <α·capacity we will re‐enter a conservation episode.  
 •  Last round (t=r): always defect, since there is no future to protect.

5.  Pseudocode

  initialize coop_buffer ← 0  
  for t in 1…r do  
    observe current stock S  
    if t == r then  
      play D  
    else if coop_buffer > 0 then  
      coop_buffer ← coop_buffer − 1  
      play C  
    else if S < α * capacity then  
      // trigger short cooperation to save the pool  
      coop_buffer ← β − 1  
      play C  
    else  
      play D  
    end if  
    observe all players’ actions, update S for next round  
  end for

6.  Edge‐case handling  
 •  r=2 or r=3: we still apply the same rules.  In practice the α‐trigger rarely fires before the last round, so you will simply defect twice (or thrice), which is maximally aggressive when survival of the pool is unlikely to out‐pay defection.  
 •  If stock is never driven below α·capacity, coop_buffer never triggers, so the strategy defects in every round (including round r).  
 •  If multiple conservation episodes occur back‐to‐back, coop_buffer resets each time S is again below threshold, ensuring enough consecutive cooperations to push S back above α·capacity.

This AESC strategy is “aggressive” in that it (a) defects almost always to grab the biggest slice, (b) never abstains to punish other defectors, and (c) only “gives back” a minimal number of cooperations when the pool is at serious risk of collapse—just enough to regrow resources for future exploitation—before returning to full defection.
'''

description_AGGRESSIVE_71 = '''
Below is a single‐strategy “Aggressive Sustained Defector” (ASD).  It never trusts, always defects to grab the highest immediate payoff, but makes exactly one calculated sacrifice in the penultimate round to seed just enough regrowth for one last big haul.  

1.  Key idea  
    •  Defect (D) every round to maximize immediate extraction.  
    •  In round r–1, play Cooperate (C) once (if stock > 0) so that some stock remains/grows into round r.  
    •  Round r: defect again and reap maximum final‐round payoff.  

2.  When to Cooperate vs. Defect  
    Let t = current round (1 ≤ t ≤ r), S = current stock.  
    Decision rule:  
    – If t == r–1 and S > 0 → play C (sacrifice to regenerate).  
    – Otherwise → play D.  

3.  Handling edge cases  
    •  First round (t = 1): falls under “otherwise → D,” so you start by defecting.  
    •  If r = 2: then t=1 is both first and penultimate → you play C in round 1, then D in round 2.  
       – Rationale: cooperating once when no history allows one regrowth before the final defect.  
    •  If stock S = 0 at any round: no one can harvest anything; but we still choose D by default (D vs. C is payoff‐equivalent when S=0).  
    •  If by some miracle stock regenerates above 0 at a late round < r–1, we still stick to D—only the pre‐final sacrifice is ever allowed.  

4.  Aggressive mindset alignment  
    •  Never forgives or reciprocates cooperation—there is no “tit‐for‐tat” or reward for others’ restraint.  
    •  Sacrifices as little as possible (exactly one coop move) and only to secure a final‐round exploit.  
    •  Withdraws cooperation if stock hits zero, because after extinction there’s nothing to wring out.  

5.  Pseudocode  

```
function ASD_decision(t, S, r):
    # t: current round index (1-based)
    # S: current common-pool stock
    # r: total number of rounds
    
    if t == r - 1 and S > 0:
        return "C"   # single, strategic cooperation to seed regrowth
    else:
        return "D"   # otherwise always defect
```

6.  Summary of per‐round behavior  
    Round 1       → D  
    Round 2 … r–2 → D  
    Round r–1     → C  (once, if any stock remains)  
    Round r       → D  

This strategy maximizes per–round extraction, never rewards opponents, and nevertheless ensures there’s at least one positive‐stock final round to harvest.
'''

description_AGGRESSIVE_72 = '''
Below is a fully‐specified “aggressive” rule‐based strategy.  In plain English it does three things:  
  1.  It never forgives a cooperator—if anyone cooperated last round, it defects to exploit them.  
  2.  It only ever cooperates to rescue the resource when it has been almost wiped out and nobody is cooperating—so that there is something left to exploit later.  
  3.  It always defects in the first round and in the final round.  

—————————————————————————  
STRATEGY “Relentless Heister”  

Parameters you set once, given the tournament’s capacity:  
  •  target_stock = capacity / 2      (the point of fastest regrowth)  

Notation (at beginning of round t):  
  •  S_t = current common‐pool stock  
  •  hist_j[t–1] ∈ {C,D} = player j’s action in the previous round  

Decision rule (for each round t = 1,…,r):  
```
function choose_action(t, S_t, {hist_j[t–1] for j≠you}):
    # 1) Always defect in the very first and very last round
    if t == 1 or t == r:
        return D

    # 2) If anyone cooperated last round, exploit them now
    if ∃ j≠you such that hist_j[t–1] == C:
        return D

    # 3) Otherwise, no one is “keeping the pool alive” –
    #    check stock level and only cooperate if we must rescue it
    #    (i.e. S_t is below the target for good regrowth)
    if S_t < target_stock:
        return C
    else:
        return D
```

Explanation of each rule:  
1.  t==1 and t==r ⇒ Defect unconditionally to signal aggression immediately and grab the last‐round bonus.  
2.  “Exploit cooperators” ⇒ if anyone showed a C-vote last round, you jump on it with D.  You never let them get away with a bargain.  
3.  “Maintenance cooperation” ⇒ if all players defected last round, the stock is collapsing.  You briefly cooperate when S_t is below half capacity (the logistic growth peak) so that S_remaining stays positive and the pool regrows.  As soon as you’re back above target_stock, you switch right back to D.  

Edge cases:  
  •  If opponents defect too hard and drive S_t to zero, the pool will stay zero notwithstanding your lone C—this is fine: once r is up or the pool is gone, you simply collect your defect‐payoffs until the end.  
  •  If r=2, you defect in both rounds (first‐round rule and last‐round rule).  
  •  If some rounds nobody ever cooperates, you slip in a C whenever S_t < capacity/2, otherwise you continuously defect.  

Why it’s aggressive  
  –  It never “pities” a cooperator or rewards nice behavior: any sign of C by another player is met with immediate D.  
  –  It only cushions the commons just enough to stay alive—purely as a vehicle for future D‐exploitation.  
  –  It front‐loads and back‐loads defection (first and last moves are guaranteed D), maximizing your share whenever you can.  
  –  It uses the minimal amount of cooperation required to keep the resource from hitting zero too early, so you can exploit it in as many rounds as possible.
'''

description_AGGRESSIVE_73 = '''
Below is a stand-alone “aggressive” strategy you can drop into the tournament.  In words, it:

 •   Cooperates at the very start to help build up stock.  
 •   Watches for any defection by any opponent; as soon as one appears, switches to permanent defection (grim trigger).  
 •   Independently of that, once we pass the halfway point of the game, we also switch to permanent defection to harvest all remaining value.  
 •   Always defects in the final round (no future to protect).  

This combination lets us maintain the commons early, punish free-riders, then deplete the pool ourselves in the last half of the game.

------------------------------------------------------------------------------------------------  
1.  State variables  
    PUNISH ← false        // have we “grim–triggered” yet?  
    T_half ← ⌊r / 2⌋ + 1  // first round of forced defection (half‐game cutoff)  

2.  At each round t = 1…r, observe:  
    – history of all players’ past actions, in particular whether any D has occurred  
    – current stock S (though S doesn’t enter decision rules directly here)  

3.  Decision rule (pseudocode):  
```
if t == 1:
    action ← C
else if t ≥ T_half:
    // last‐half exploitation: no more future to protect
    action ← D
else if PUNISH:
    // already triggered on some defection
    action ← D
else:
    // we’re in first half and haven’t punished yet
    if any player j (including ourselves) played D in rounds 1..t–1:
        PUNISH ← true
        action  ← D
    else:
        action ← C
```

4.  Detailed walk-through  
– Round 1: cooperate unconditionally.  
– Rounds 2…⌊r/2⌋:  
    •  If we have never seen a defection, keep cooperating.  
    •  The instant anyone defects, set PUNISH = true and defect forever after.  
– Rounds ⌊r/2⌋+1…r: defect every round (this subsumes the final‐round defection).  

5.  Why it is aggressive  
– Early cooperation maximizes the common‐pool stock so there is “meat on the bone” for later exploitation.  
– Grim trigger makes it costly for rivals to defect: they immediately lose our future cooperation.  
– A unilateral switch to pure defection at mid‐game lets us capture the lion’s share of remaining surplus.  
– Final‐round defection guarantees no exploitable “shadow of the future.”  

6.  Edge cases  
– r = 2: T_half = ⌊2/2⌋+1 = 2, so play {C, D}.  
– If an opponent defects in round 1, we punish from round 2 onward (so {C, D,…D}).  
– If nobody ever defects in the first half, we still defect from T_half onward.  

This simple rule set requires only tracking “have I seen a D?” and the current round, and it meets all the requirements for an aggressive common‐pool strategy.
'''

description_AGGRESSIVE_74 = '''
Below is a concise “Aggressive Threshold-Defector” strategy.  It exploits the resource whenever it is “safe” (i.e. stock is high) and only grudgingly cooperates to prevent total collapse—always defecting in the very last round.  No signalling, no forgiveness cycles, just maximal extractions subject to minimal sustainability.

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
STRATEGY: “Threshold Aggressor”  
Parameters (known to all players):  
• n = number of players  
• r = total rounds  
• capacity = maximum stock  

Derived constant:  
• thr := capacity / 2    (you can tune “½” downward for even more aggression)

State variables (at the start of each round t):  
• t ∈ {1,2,…,r} (current round)  
• S_t ∈ [0,capacity] (current common‐pool stock)  

Decision rule (for player i in round t):

1. If t == r (last round), play D  
2. Else if S_t > thr, play D  
3. Else (S_t ≤ thr), play C  

Edge cases:  
• If S_t = 0, both actions yield zero payoff—default to D.  
• In round 1: S_1 = capacity > thr, so you defect.  

Rationale:  
• You grab the larger share (S_t/n) whenever stock is comfortably above thr.  
• When the pool falls at or below half capacity, you “cooperate” just enough (take S_t/(2n)) to allow some regrowth—preserving a living pool and future extraction.  
• In the final round you always defect, since there is no future to protect.  

Pseudocode  
----------
function decide_action(t, S_t):  
    if t == r:  
        return D  
    else if S_t > capacity/2:  
        return D  
    else:  
        return C  

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
This is aggressive—it seizes the full defect‐payoff whenever possible, only stepping back when the resource is low (and doing so just enough to keep the game alive), then reverting to outright defection in the terminal round.
'''

description_AGGRESSIVE_75 = '''
Below is a simple but ruthlessly aggressive strategy—“Always-Defect”—that never gives an inch.  It maximizes your round‐by‐round take even at the price of driving the stock to zero.  

1.  Decision rule  
   •  In every round t (1 ≤ t ≤ r), regardless of history or current stock S_t, play D (Defect).  
   •  You never cooperate, even if the pool has collapsed to S_t = 0 (in which case both C and D yield zero, so you may as well stick with D).  

2.  Edge cases  
   –  First round (t=1): play D.  
   –  Any intermediate round: play D.  
   –  Last round (t=r): play D.  No future to preserve, so again defect.  

3.  Pseudocode  

function choose_action(t, S_t, history):  
    return “D”  

4.  Rationale (aggressive mindset)  
   – Defection (S_t/n) strictly dominates cooperation (S_t/(2n)) in every period.  
   – You extract the maximum possible each round, never sacrificing immediate payoff for future stock.  
   – You do not waste “forgiveness” or “signal” cooperations; you instead drive the pool as hard as possible to maximize your own raw take.  
   – Even though the commons will collapse (S → 0) before round r in a multi‐defector environment, your front-loading of high payoffs dominates the zero‐sum losses at the end.  

This “Always-Defect” tactic is the archetype of aggression in a repeated CPR setting: it never trusts, never forgives, and never cedes any portion of the resource.
'''

description_AGGRESSIVE_76 = '''
Below is an “aggressive‐extortion” style strategy.  It maximizes immediate extraction (defection) except when the common‐pool is so depleted that even defecting yields almost nothing—at which point it makes a single “surgical” cooperative move to resurrect the pool and then goes back to full defection.  In the last round it never spares mercy.

1.  Parameters and thresholds  
   - n          : number of players  
   - capacity   : the biological carrying capacity of the pool  
   - r          : total rounds  
   - T_low      : lower stock threshold = capacity / (2n)  
     •  Intuition: if S ≤ T_low then a full‐blown defection (S/n) leaves almost nothing for next‐round regrowth; a brief cooperation buys future defection.  

2.  High‐level rules  
   – Round 1 through r–1:  
     •  If current stock S_t > T_low ⇒ Defect (D)  
     •  If current stock S_t ≤ T_low and we have not yet “rescued” in this low‐stock regime ⇒ Cooperate (C) once to trigger regrowth  
     •  If S_t ≤ T_low but we have already cooperated (in this low‐stock region) and S has not recovered above T_low ⇒ Cooperate again until S exceeds T_low  
     •  Once S_t > T_low again, reset the “rescue‐used” flag and resume full Defection.  
   – Round r (the last round): Defect unconditionally.

3.  Edge‐cases  
   – First round: apply the same check: since initial stock = capacity ≥ 2n, capacity/(2n) ≤ capacity so S_1 > T_low ⇒ Defect.  
   – Multiple low‐stock rescues: we only reset our “have rescued?” flag the instant S_t > T_low.  Thus if the pool dips, we may execute several consecutive cooperations until it climbs above T_low, then exploit again.  
   – If the pool never falls below T_low, we never cooperate.  
   – No cooperation in the last round, so no risk of “gift” at the end.

4.  Pseudocode  

```
Initialize:
  rescued_flag ← false    // Have we cooperated in current low‐stock spell?

For t in 1…r:
  Observe current stock S_t

  if t == r:
    action ← D   // Last round: always defect
  else if S_t > T_low:
    // Pool healthy: full aggression
    action ← D
    // Reset rescue state once we regain stock
    rescued_flag ← false
  else:
    // Pool is low: S_t ≤ T_low
    if rescued_flag == false:
      // First rescue move
      action ← C
      rescued_flag ← true
    else:
      // Either rescue in progress or prior rescue failed to restore
      action ← C
    end if
  end if

  Play action, observe everyone’s consumption, update S_{t+1} per stock‐dynamics
end for
```

5.  Why this is aggressive  
  – Outside the minimal “pocket‐knife” rescue at very low stock, it never sacrifices immediate gain.  
  – It never enters costly grim‐trigger punishments or long cooperative phases—every chance to defect is taken.  
  – Last round is pure defection, so there is never a “final wink” of cooperation.  

6.  Discussion  
  – By cooperating just enough to push S above T_low, it guarantees at least one more round of high‐yield defection, which outweighs the one‐round sacrifice.  
  – If opponents never cooperate, the pool may still collapse, but at that point everyone’s payoffs are zero—no worse than our worst‐case expectation.  
  – If opponents do cooperate, we’re ready to ransack the pool every time it recovers.
'''

description_AGGRESSIVE_77 = '''
Below is an “aggressive‐exploit” strategy whose sole goal is to maximize your own cumulative consumption by defecting whenever it is safe to do so, but slipping into cooperation only just often enough to keep the common pool from crashing to zero (so that you continue to have something to harvest in future rounds).  It never “forgives” opponents for defecting—it only cooperates out of pure self‐interest to preserve the resource—and in the last round it always defects.

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
1. Notation and parameters  
   • n = number of players  
   • r = total rounds  
   • capacity = maximum stock  
   • S_t = stock at the beginning of round t  
   • A_t ∈ {C, D} = your action in round t  
   • S_crit = capacity/2  (a conservative “half‐stock” threshold)  

2. High-level idea  
   – Default to defect (D) every round—D gives you twice the per‐round payoff of C.  
   – Only switch to cooperate (C) if the stock has fallen to or below S_crit, and you are not already in the last round.  This “buys back” the resource.  
   – In the very last round (t = r), always defect, since there is no future to protect.  

3. Pseudocode  

   initialize S_1 = capacity  
   for t in 1..r:  
     if t == r:  
       A_t ← D  
     else if S_t ≤ S_crit:  
       A_t ← C       # cooperate just enough to avoid collapse  
     else:  
       A_t ← D       # aggressively exploit when stock is healthy  
   
     # After actions by all players, the tournament engine updates S_{t+1}  
     # according to the rules:  
     #   total_consumption = Σ_i consumption_i  
     #   S_remain = S_t – total_consumption  
     #   growth = 2 * S_remain * (1 – S_remain/capacity)  
     #   S_{t+1} = min(S_remain + growth, capacity)  

4. Handling edge cases  
   • Very small r (e.g. r=2):  
     – Round 1: since t<r and S_1=capacity>S_crit, A_1=D  
     – Round 2=r: A_2=D  
     (i.e. defect both rounds—no need to preserve because there is only one future round.)  
   • Stock has collapsed to zero (S_t=0):  
     – Any action yields zero payoff this and all future rounds; the rule still says D, but it makes no difference.  
   • Exact threshold S_t = S_crit:  
     – We take S_t ≤ S_crit as the trigger, i.e. we cooperate at S_t = capacity/2.  

5. Why this is aggressive  
   – You defect in all “safe” rounds, capturing the higher individual payoff.  
   – You only cooperate when the pool is under half full.  That is the bare minimum investment needed to keep the pool alive for future exploitation.  
   – You never punish other defectors (no tit-for-tat); you simply exploit them relentlessly.  
   – In the last round you defect unconditionally, since there is no future stock to preserve.  

6. Possible refinements  
   If you observe external evidence that many opponents are cooperating unprompted and the stock is growing too quickly, you could raise the threshold S_crit temporarily (e.g. to 0.6·capacity) to extract even more surplus before slipping back into maintenance mode.  But the simple ½-capacity threshold already guarantees that the pool never collapses prematurely under worst-case opponent behavior.
'''

description_AGGRESSIVE_78 = '''
Below is a self‐contained “aggressive” strategy that you can drop into a tournament.  It defects by default, only “pays in” occasionally to keep the pool alive, and always defects in the end‐game.  

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
AGGRESSIVE THRESHOLD STRATEGY (“ATS”)  
––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  

Parameters you choose once at the start:  
• n, r, capacity  (from the tournament)  
• γ_low ∈ (0,1)  – fraction of capacity at which you trigger a “maintenance” cooperation.  
• E = ⌈r·ε⌉ – number of last rounds in which you defect no matter what (end‐game defection), for some small ε, e.g. ε=0.1 so E=⌈0.1r⌉.  

For concreteness let γ_low=0.25 and ε=0.1.  You can tune these in implementation.

State variables each round:  
• t = current round index (1…r)  
• S_t = current stock at the beginning of round t  

Decision rule for round t:  
1.  If t > r–E  (i.e. you’re in the last E rounds)  
      → Play D.  
2.  Else if S_t ≤ γ_low·capacity   (stock dangerously low)  
      → Play C (emergency “top‐up” cooperation).  
3.  Else  
      → Play D.  

Rationale:  
1. Aggressive by default: you defect whenever the pool is healthy (S_t>γ_low·capacity).  
2. Emergency cooperation only when S_t hits a low threshold so that the pool can regrow enough to be profitable again.  
3. In the final E rounds you go “all‐out” defect to extract every last penny, regardless of S.  

Edge cases:  
• First round (t=1): S₁=capacity so you hit rule 3 → D.  
• Rounds 2… until stock falls to γ_low·capacity: D.  
• If at some round T₁ your D’s have driven S_{T₁} ≤ γ_low·capacity, you cooperate once at T₁.  That yields a smaller draw but allows regrowth.  As soon as S_{T₁+1}>γ_low·capacity you resume defecting.  
• Last E=⌈0.1r⌉ rounds: always defect, even if that drives stock to 0.  You prefer maximal short‐term extraction.  

Pseudocode sketch  
-----------------  
```
INPUT: n, r, capacity  
PARAMETERS: γ_low = 0.25, ε = 0.1  
E = ceil(r * ε)

for t in 1..r:
    observe S_t

    if t > r - E:
        action ← D
    else if S_t <= γ_low * capacity:
        action ← C
    else:
        action ← D

    play(action)
    observe all consumption → compute next S_{t+1}
endfor
```  

Comments on aggression:  
– You never cooperate as long as the pool is “fat” enough to exploit.  
– You only invest one round at a time when the pool is truly at risk, then immediately switch back to defection to harvest the regrown stock.  
– You reserve the last ~10% of rounds for unfettered defection, squeezing out as much as possible with no thought of future regrowth.  

This strategy guarantees you exploit any generous or naïve cooperators, yet prevents the stock from collapsing prematurely by injecting just enough cooperation when it’s on the brink.
'''

description_AGGRESSIVE_79 = '''
Below is an “Aggressive Extractor” strategy.  It is built around four simple ideas:  
 1.  Always defect (grab the larger share) whenever you can.  
 2.  Only switch to cooperating when the stock falls too low (to avoid total collapse).  
 3.  In the very first and very last rounds you defect unconditionally.  
 4.  You never “forgive” other defectors—your only motivation to cooperate is to prop up the commons.  

—  
### Parameters you choose (can be tuned by tournament–entry)  
• regeneration_threshold ← capacity/4  
    (if the pool ever drops below 25 % of capacity)  
• regeneration_duration ← n rounds  
    (once you decide to regenerate, you cooperate for n consecutive rounds)  
• endgame_exploit ← ⌈r/5⌉  
    (last 20% of rounds are pure defection)  

### State variables  
• regen_counter ← 0  
    (counts how many more rounds you must cooperate in regeneration mode)  

### Strategy pseudocode  

Input at start of each round t:  
 • t ∈ {1,2,…,r}  
 • S_t = current stock in the pool  
 • history of all actions (not actually used, except for round counters)  

Output: your action a_i(t) ∈ {C,D}.  

```
if t == 1 then
    // first‐move aggression
    action ← D
    return action
end if

if t > r – endgame_exploit then
    // final rounds: pure exploitation
    action ← D
    return action
end if

if regen_counter > 0 then
    // we are in forced regeneration mode
    action ← C
    regen_counter ← regen_counter – 1
    return action
end if

// stock‐based decision
if S_t < regeneration_threshold then
    // pool is too low: start a regeneration run
    regen_counter ← regeneration_duration – 1
    action ← C
    return action
else
    // otherwise stay aggressive
    action ← D
    return action
end if
```

### Explanation of the decision rules  
1. First round (t = 1): always defect to seize early advantage and signal you are not a “soft” cooperator.  
2. Endgame exploitation (t > r–endgame_exploit): once you enter the last 20% of rounds, you switch to all‐defect forever—no future punishment makes cooperation worthwhile.  
3. Regeneration mode: if the pool ever collapses below ¼ of capacity, you briefly switch to cooperation for a fixed block of n rounds.  This “prop‐up” prevents permanent annihilation of the stock so that you can continue exploiting later.  
4. Outside of regeneration blocks, you defect unconditionally, regardless of what opponents have done.  

### Handling edge cases  
• If capacity is huge or r very small, regeneration may never trigger—means you simply defect every round.  
• If opponents over‐harvest and drive S_t to zero, you’ll never earn again—but at least you tried to prop up the pool once you fell below threshold.  
• If r is so small that endgame_exploit ≥ r, the “last‐round” condition dominates: you will defect every round.  

### Why it is aggressive  
• You never “reward” a cooperator by switching to C after they cooperate.  
• You punish the pool, not the players—your only cooperation is mechanical, to keep the resource alive long enough for you to harvest it in later rounds.  
• You exploit right up until the final rounds, then switch to an all‐out “grab” with zero regard for future reliability.  

This strategy maximizes short‐term extraction, punishes any idea of sustained cooperation, and only contributes to the resource when it is absolutely necessary to avoid total collapse.
'''

description_AGGRESSIVE_80 = '''
Below is a self-contained “aggressive” strategy that (i) preserves the resource just long enough to keep future rents high, (ii) defects as soon as anyone misbehaves, and (iii) launches a full-blown grab near the endgame.  In tournament play it will (a) suck up large payoffs when the pool is still healthy and (b) never give a sucker’s payoff to persistent cooperators.

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
AGGRESSIVE SNEAK-AND-GRAB STRATEGY  

Notation and memory variables  
• r            : total rounds  
• t            : current round (1…r)  
• τ            : “cooperate‐window” cutoff = max(1, ⌊δ·r⌋), set δ=0.2 (20% of rounds)  
• deplObserved : Boolean flag, turned on if any opponent has defected in past  

Initialization (before round 1)  
  deplObserved ← false  
  τ ← max(1, floor(0.2 * r))  

Each round t = 1…r do:  
  1. Observe history of all players’ A_j(1),…,A_j(t–1).  
     If any A_j(k)=D for any j≠i and k<t then deplObserved ← true.  

  2. Decide action A_i(t):  
     if t ≤ τ AND deplObserved = false then  
       A_i(t) ← C         // maintain the stock… lure cooperators in  
     else  
       A_i(t) ← D         // defect permanently from now on  

  3. Play A_i(t).  

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
Rationale and edge cases  
1. First round (t=1):  
   • deplObserved=false and 1≤τ ⇒ play C.  This preserves stock so future extract per‐round payoff is maximized.  

2. Early‐stage “test” (t=2…τ):  
   • Continue cooperating unless you see any D.  
   • If someone defects before τ, you immediately switch to all-D to punish and capture as much as possible thereafter.  

3. End of window (t=τ+1):  
   • Even if everyone was perfectly cooperative in rounds 1…τ, you switch to D.  Stock is still high ⇒ your D pays S/n is large.  

4. Late‐stage (t>τ):  
   • Always defect.  There is no incentive to cooperate once your sneak-and-grab begins.  

5. Very last round (t=r):  
   • Naturally t>τ so A_i(r)=D.  Extract the maximum; there is no future stock to protect.  

6. Small r (e.g. r<5):  
   • τ=min 1 by construction ⇒ you play C in round 1, then D in all subsequent rounds.  That small window is enough to seed the stock‐preservation illusion.  

Why it’s aggressive  
– You never let cooperators sustain you beyond τ—you grab as soon as you can.  
– You punish any defector in the cooperate‐window by immediately defecting forever.  
– You maximize your per-round extraction when S is highest.  

Pseudocode (concise)  
```
INPUT: r, history of all actions up to t–1  
PARAM δ ← 0.2  
GLOBAL STATE:
  deplObserved ← false
  τ ← max(1, floor(δ * r))

FOR t in 1…r:
  # 1) update flag
  IF exists j≠i and k<t with A_j(k)==D:
    deplObserved ← true

  # 2) choose action
  IF t ≤ τ AND deplObserved == false:
    A_i(t) ← C
  ELSE:
    A_i(t) ← D

  # 3) play A_i(t)
END
```

This strategy will outperform naïve always-C or naïve tit-for-tat types in tournaments where aggressive, high-extraction play wins.
'''

description_AGGRESSIVE_81 = '''
Below is “All-Out Siege,” an aggressive, self-interested trigger-style strategy that extracts as much as possible from the pool while still capturing a last‐round bonus by artificially propping up the stock one turn before the end.

1.  Strategy name  
    All-Out Siege

2.  Intuition  
    •  In every early round you defect to grab the maximum share.  
    •  On the penultimate round you cooperate just enough to leave some stock, generate growth, and then hit a big defect in the very last round.  
    •  No attempt to sustain the commons beyond what’s needed for your final extraction.

3.  Decision rules  
    Let t = current round (1≤t≤r), S_t = stock at start of round t.

    If t ≤ r−2:  
       play D

    Else if t = r−1:  
       play C

    Else (t = r):  
       play D

4.  Handling edge cases  
    •  r = 2:  
       – t=1=r−1 ⇒ play C  
       – t=2 ⇒ play D  
       (This maximizes your total: you trade a smaller first‐round take for a positive second‐round take.)  
    •  Stock S_t=0 on penultimate round: cooperating or defecting both give zero, so you can arbitrarily cooperate.  
    •  If capacity or n change, the same trigger structure applies—rules do not depend on exact parameter values.

5.  Pseudocode  
    ```
    function AllOutSiege(t, r, S_t):
        # t: current round index (1…r)
        # r: total rounds
        # S_t: current common‐pool stock
        if t <= r - 2:
            return "D"     # Always defect early
        else if t == r - 1:
            return "C"     # Cooperate once to seed final stock
        else:   # t == r
            return "D"     # Last‐round grab
    ```

6.  Why it’s aggressive  
    •  You never incur the “cost” of cooperation except when it directly boosts your own final haul.  
    •  You build no long‐term cooperation, you simply exploit a one‐round “pump” in round r−1 to guarantee there’s something left for a maximal defection in round r.  
    •  All other players who try to cooperate early get punished by your persistent defection.
'''

description_AGGRESSIVE_82 = '''
Below is a self‐contained “aggressive” strategy—call it Aggressive Threshold Defection (ATD)—that maximizes short‐run payoffs by defecting almost always, but grudgingly cooperates just enough to avoid complete collapse of the commons.  It handles first and last rounds explicitly, and uses a simple stock‐based trigger in the middle.

1.    Overview of ATD  
• First round: defect.  
• Last two rounds: defect (no future to preserve).  
• Intermediate rounds: defect as long as the stock S is “healthy.” If S falls below a low threshold, do a one‐round cooperation to let the pool regrow.  Otherwise continue defecting.  

2.    Parameters  
• n = number of players  
• r = total rounds  
• capacity = maximum sustainable stock  
• θ = threshold fraction of capacity at which you swallow pride and cooperate; we set θ = 1/n.  
• c_thresh = θ × capacity = capacity/n.  

Rationale for θ = 1/n: when S = capacity/n, your one‐round cooperation (consuming S/(2n)) still leaves enough S to generate net positive growth next round.  Below that, perpetual defection risks zeroing out S forever and yielding zero future payoffs.

3.    Pseudocode  

```
Initialize:
  θ ← 1 / n
  c_thresh ← θ * capacity

On each round t = 1…r observe current stock S_t:

function ATD_decision(t, S_t):
  # 1. FIRST round: establish reputation of aggression
  if t == 1:
    return D

  # 2. LAST two rounds: no incentive to preserve commons
  if t ≥ r - 1:
    return D

  # 3. MID‐game threshold check
  if S_t ≤ c_thresh:
    # grudging one‐round cooperation to jump-start regrowth
    return C
  else:
    # default: full defection to grab the most
    return D
```

4.    Explanation of key rules  
• “Always defect” maximizes your round payoff S/n versus S/(2n).  
• If every player follows ATD, stock will steadily fall until S ≤ capacity/n, at which point each cooperates once.  That single wave of cooperation cuts consumption by half, leaving enough stock to regrow.  After one shot of cooperation, we resume defecting immediately—always on the lookout for maximal short-run gain.  
• By defecting in the final two rounds we avoid any mild restraint and extract maximum payoff when there is zero future.  

5.    Edge‐case behavior  
• If S_t = 0 before the threshold is ever hit, ATD has no way to recover the pool (all payoffs hereafter are 0).  This is the price of extreme aggression.  
• If capacity is just at its minimum (2n), then c_thresh = 2n / n = 2.  Cooperating on S ≤2 still yields positive growth.  
• If somehow you cooperate at S = c_thresh and next‐round S still ≤ c_thresh, you will cooperate again—this correctly handles repeated low‐stock emergencies.  

6.    Aggressive mindset alignment  
• You start by defecting to signal “I will not hesitate.”  
• You defect every round that does not strictly require a single cooper­ation to stave off collapse.  
• You defect in the last two rounds with no remorse.  
• Your minimal cooperations are purely mechanical—and only invoked when the commons is on the brink.  

This strategy is easy to implement, communicates unmistakable aggression, yet preserves enough of the common pool to keep scoring nonzero payoffs in a multi‐round setting.
'''

description_AGGRESSIVE_83 = '''
Below is a fully‐specified “aggressive” harvesting strategy—call it the Aggressive Hysteresis Defector (AHD).  It maximizes short‐term gains by defecting whenever the stock is healthy, but it grudgingly cooperates only when the stock is dangerously low, and only until it recovers.  On the very last round it always defects.

1.  Parameters you must fix once and for all before the game starts  
    •  capacity (given)  
    •  n (given)  
    •  L ∈ (0,capacity): “low‐stock” threshold (e.g. L=0.3·capacity)  
    •  U ∈ (L,capacity): “high‐stock” threshold for ending regeneration (e.g. U=0.8·capacity)  

2.  Internal state (persisting across rounds)  
    •  phase ∈ {EXPLOIT, REGENERATE}, initially phase←EXPLOIT  

3.  Decision rule at the start of every round t (observing current stock S_t):  
   
   if t == r then  
     action ← Defect  // last‐round grab, no future to protect  
   else if phase == EXPLOIT then  
     if S_t ≤ L then  
       phase ← REGENERATE  
       action ← Cooperate  
     else  
       action ← Defect  
     end  
   else /* phase == REGENERATE */  
     if S_t ≥ U then  
       phase ← EXPLOIT  
       action ← Defect  
     else  
       action ← Cooperate  
     end  
   end  

4.  Intuition & properties  
  •  Aggressive mind‐set: in EXPLOIT you always defect, regardless of opponents’ past moves, squeezing the largest immediate payoff S_t/n.  
  •  Resource‐preservation: once the pool falls to or below L you grudgingly switch to REGENERATE, cooperating (harvesting only S_t/(2n)) until the pool climbs back up to U.  Then you flip back to EXPLOIT.  
  •  Last‐round defection: in round r you always defect, since there is no future.  
  •  No reliance on opponent history or signaling—purely state‐based.  

5.  Pseudocode  

  initialize:  
    phase ← EXPLOIT  

  for t in 1…r do  
    observe S_t  
    if t == r then  
      play D  
    else if phase == EXPLOIT then  
      if S_t ≤ L then  
        phase ← REGENERATE  
        play C  
      else  
        play D  
      end  
    else  // phase == REGENERATE  
      if S_t ≥ U then  
        phase ← EXPLOIT  
        play D  
      else  
        play C  
      end  
    end  
  end  

6.  Choice of thresholds  
   You can tune L and U to balance “harvest aggressiveness” vs “risk of collapse.”  A typical choice might be  
     L = 0.3 × capacity,  
     U = 0.8 × capacity.  

Under this AHD strategy you exploit freely whenever the pool is ample, you punish no one (you never try to “signal”)—you simply always defect—yet you grudgingly preserve the resource only if it nears collapse.  That makes you as aggressive as possible while still guaranteeing occasional regrowth so that exploitation can continue in later rounds.
'''

description_AGGRESSIVE_84 = '''
Below is a fully specified “aggressive” strategy we call Opportunistic Defection with Conditional Restoration.  It sacrifices just enough to keep the pool alive, but otherwise defects at every opportunity—and always defects in the last round.

1.  Parameters  
   • n = number of players  
   • capacity = maximum stock  
   • r = total rounds  
   • f ∈ (0,1) = restoration‐threshold fraction (we suggest f=0.4 or 0.5 as a default)  
   • T = f × capacity  

2.  Intuition  
   • Defect whenever the pool is “healthy” (S ≥ T), to grab the larger n‐share payoff.  
   • If the pool has fallen below T, play C just once to nudge it back toward regrowth—then immediately resume defecting.  
   • Always defect in the final round to squeeze out every last unit.  

3.  Decision Rule (per round t, with observed stock S)  
   if t == r then  
     action ← D     # Last‐round defection  
   else if S ≥ T then  
     action ← D     # Pool is rich—exploit it  
   else  
     action ← C     # Pool is low—sacrifice half‐share to allow regrowth  

4.  Edge Cases  
   • Round 1: S = capacity ≥ T ⇒ action = D.  
   • Round r: regardless of S, action = D.  
   • If capacity is extremely large or small, you can tune f toward 0 (more defection) or 1 (more preservation).  
   • If S hits exactly zero before the last round, your rule says S<T ⇒ you play C, but that yields zero immediate payoff; ideally the others may also play C and regenerate.  If they do not, the pool remains dead—your subsequent plays will all be D (but yield zero payoff).  

5.  Pseudocode  

```
function AGGRESSIVE_STRATEGY(t, S, capacity, r, f):
    # t: current round index, 1 ≤ t ≤ r
    # S: current common‐pool stock
    # capacity: maximum sustainable stock
    # r: total number of rounds
    # f: threshold fraction (e.g. 0.4)

    T ← f * capacity

    if t == r then
        return D
    else if S >= T then
        return D
    else
        return C
```

6.  Why It’s Aggressive  
   • You defect as often as possible to grab the larger S/n payoff.  
   • You only “cooperate” when the pool is so depleted that further defection would kill it outright—and thus yield zero in all remaining rounds.  
   • You refuse any tit‐for‐tat or long‐term forgiveness: you never punish specific opponents, nor do you reward past cooperators.  Your sole guiding principle is maximizing your haul subject to keeping the resource from instant collapse.  

This strategy will dominate any “nicely” cooperating opponents in the short run, and only yields the bare minimum cooperation needed to avoid the pool’s complete extinction before the tournament ends.
'''

description_AGGRESSIVE_85 = '''
Below is a self-contained “Aggressive Threshold Defector” strategy.  It never tries to build long-term cooperation; it grabs as much as it safely can each round, only conceding a small amount when the resource is so low that outright defection would crash it to zero before the end of the tournament.

1.  Parameter setup (computed once at the start):  
    • k ← 2              # number of terminal rounds in which we always defect  
    • S_low ← capacity / (n + 1)  
        – Interpretation: if the stock falls to S_low or below, a full-blown defection would deplete it to zero; by switching to “cooperate” at or below this level we leave something in the pool for regrowth.

2.  Decision rule for round t with current stock S:

    if t == 1:  
        play D  
    else if t > r - k:    # last k rounds  
        play D  
    else if S > S_low:  
        play D  
    else:  
        play C  

3.  Rationale and properties

   • First round (t=1): D.  Signal aggression immediately, grab the larger share.  
   • Last k rounds: D.  No future to preserve—extract maximum.  
   • Intermediate rounds:
     – If stock S is comfortably above S_low, defect and take S/n.  
     – If S has fallen to ≤ S_low, switch to cooperate (take S/(2n)) so that S_remaining > 0 and the logistic growth can kick in.  This avoids “all-defect” collapse of the resource before round r−k.  
   • Aggressive mindset: maximizes extraction whenever it can without pushing the system to ruin prematurely.  It never “forgets” or “forgives” cooperators—it simply defects unless forced by a low-stock safeguard.

4.  Pseudocode

    initialize:
        k ← 2
        S_low ← capacity / (n + 1)

    on each round t = 1…r with observed stock S:
        if t == 1:
            return “D”
        if t > r − k:
            return “D”
        if S > S_low:
            return “D”
        else:
            return “C”

This strategy will enter a tournament as a relentless defector, only momentarily “softening” its take when the pool nears collapse, and never attempting to build a cooperative precedent or signaling scheme.
'''

description_AGGRESSIVE_86 = '''
Below is an “aggressive” strategy that (1) exploits whenever it safely can, (2) punishes any would‐be cooperators, and (3) only cooperates when the pool is in danger of collapse (so that there is something left to exploit).  

Strategy Name  
Aggressive Triggered Defection with Conditional Preservation (ATD-CP)  

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
1.  Decision Rules  

Let  
•  t = current round (1 ≤ t ≤ r)  
•  Sₜ = stock at start of round t  
•  r = total number of rounds  
•  capacity = maximum stock  
•  T = preservation threshold = capacity/2  
•  H = defection horizon = 1 (the last round)  

On each round t:  
  1. If t > r – H  (i.e. in the last round), play D.  
  2. Else if Sₜ ≥ T, play D (exploit high stock).  
  3. Else (Sₜ < T), play C (preserve the resource).  

Rationale:  
–  We always defect when the resource is plentiful (Sₜ ≥ T) to maximize immediate payoff and to punish cooperators.  
–  We only cooperate if the stock falls below T, to allow regrowth and avoid total collapse.  
–  In the final round we defect regardless, since there is no future to preserve.  

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
2.  Handling Edge Cases  

First round (t = 1):  
•  Since S₁ = capacity ≥ T, we defect.  

Last round (t = r):  
•  By rule (1), we defect.  

Near–collapse scenario:  
•  If capacity is so low that even one round of full defection would drive Sₜ to 0, we will detect Sₜ < T and cooperate to give the pool a chance to rebound.  

When opponents never cooperate:  
•  We will never unknowingly “forgive” non-cooperators—our only cooperation is a purely mechanical response to low Sₜ, not a social signal.  

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
3.  Pseudocode  

```
INPUTS: n, r, capacity  
PARAMETERS: T ← capacity / 2  
            H ← 1  

FUNCTION ATD_CP(t, S_t):
    # t = current round index, S_t = current stock
    # returns action ∈ {C, D}

    if t > r - H:
        return D      # always defect in the last round
    endif

    if S_t >= T:
        return D      # exploit while stock is high
    else
        return C      # preserve when stock is low
    endif
END FUNCTION
```

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
Discussion of Aggressiveness  
•  “Defect first, ask questions later.” We never initiate cooperation unless forced by resource scarcity.  
•  We punish any tentative cooperation by continuing to defect so long as the pool is healthy.  
•  We do just enough cooperation to keep the game alive—no goodwill, no forgiveness—only minimal preservation.
'''

description_AGGRESSIVE_87 = '''
Below is an “Aggressive‐Exploit‐When‐Rich, Cooperate‐When‐Poor” strategy.  It is aggressive in the sense that it extracts maximum short‐term payoffs whenever the pool is large, but it grudgingly cooperates only when the stock is low so as to keep the game alive long enough to exploit again.  In the very last round it always defects for a final grab.

1.  Parameters  
   •  n     = number of players  
   •  r     = total rounds  
   •  capacity = maximum stock  
   •  Sₜ    = stock at start of round t  

2.  Key idea  
   –  If the stock Sₜ is “abundant” (≥ capacity/2), play Defect to get the full Sₜ/n.  
   –  If Sₜ is “scarce” (< capacity/2), play Cooperate to consume less and let the pool regrow.  
   –  In the final round (t = r), always Defect.  

3.  Edge cases  
   –  First round: S₁ = capacity ≥ capacity/2 ⇒ Defect.  
   –  Last round: regardless of Sᵣ, Defect to maximize last‐round take.  
   –  If stock ever hits zero, you and everyone else get zero no matter what.  You remain “Cooperate” by rule when Sₜ < capacity/2 but there is no further regrowth from zero.  

4.  Pseudocode  

   initialize S ← capacity  
   for t in 1…r do  
     if t == r then  
       action ← D  
     else if S ≥ capacity/2 then  
       action ← D  
     else  
       action ← C  
     end  

     // execute action simultaneously with others  
     if action == C then  
       π ← S/(2n)  
     else  
       π ← S/n  
     end  

     // compute new stock  
     total_consumption ← (num_C)*(S/(2n)) + (num_D)*(S/n)  
       // num_C, num_D observed after everyone moves  
     S_remaining ← S − total_consumption  
     growth ← 2 * S_remaining * (1 − S_remaining/capacity)  
     S ← min(S_remaining + growth, capacity)  

     record payoff π for round t  
   end for  

5.  Why it’s aggressive  
   –  It maximizes immediate payoff whenever there is plenty in the pool.  
   –  It only “throws the game a bone” (by cooperating) when the remaining stock has fallen below half capacity—just enough to let the pool regrow so future defections can again yield high payoffs.  
   –  It never forgives in the final round.  

This strategy will typically win big on rounds when the pool is high, grudgingly cooperate just to keep the pool from dying too soon, and then defect in the last round for the final extra gain.
'''

description_AGGRESSIVE_88 = '''
Below is an “aggressive” strategy—called Aggressive Regrowth-Constrained Defection (ARCD)—that seeks to maximize your total payoff by defecting whenever possible, but grudgingly cooperating just enough to prevent the commons from collapsing (so you can keep exploiting it in later rounds).

1.    Parameters  
     •  capacity (C)  
     •  total rounds r  
     •  number of players n  
     •  threshold fraction α (we set α=0.25)  
     Define  
       S_low  ← α × capacity    (e.g. 25% of full stock)  

2.    Intuition  
     •  Always defect unless the stock is dangerously low or we’re in the last round.  
     •  If S_t drops below S_low, you briefly cooperate (consume less) so that the pool can regrow.  
     •  Otherwise you defect every round to grab the highest share.  

3.    Edge cases  
     •  Round 1: defect (no reason to cooperate before you’ve exploited once).  
     •  Last round (t = r): defect (standard end-game).  
     •  If stock ever hits zero, you cooperate until it grows above S_low, then resume defection.  

4.    Pseudocode  

Function my_action(t, S_t):  
  Let r_remain ← r – t + 1  
  If t == 1 then  
    return D                 // start aggressively  
  If r_remain == 1 then  
    return D                 // last‐round defection  
  If S_t < S_low then  
    return C                 // stock too low—help it regrow  
  Else  
    return D                 // otherwise always defect  

5.    Explanation of aggressiveness  
     – You defect by default (every round except a narrow “rescue” window when the pool is nearly collapsed).  
     – You never try to build a reputation for cooperation; you only cooperate when the resource is truly at risk of zeroing out.  
     – You never signal or “forgive”—you don’t track opponents’ actions beyond watching stock level.  

This strategy guarantees you grab the largest per‐round share whenever the pool is healthy, and sacrifices only the minimal amount needed to keep the game going for future exploitation.
'''

description_AGGRESSIVE_89 = '''
Below is a minimal “all‐out” defection strategy that maximizes your short-term take in every round.  It never cooperates, it never forgives, and it never lets the stock recover—an unapologetically aggressive approach.

––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
Strategy Name  
   Aggressive Defector

Parameters assumed in scope  
   n      (number of players)  
   r      (total rounds)  
   capacity (maximum stock, ≥ 2n)  

State variables passed each round  
   t      (current round index, 1…r)  
   S      (current common pool stock before moves)  
   history (past actions of all players, if you cared to look)  

Decision rule (for player i):  
   At the start of every round t, simply choose Defect (D).  

Rationale  
1.  In any given round with stock S, defecting yields S/n > S/(2n), so you always get more this round.  
2.  By never cooperating, you force the pool to collapse as fast as possible.  Opponents who hope for regrowth will be disappointed.  
3.  There is no credible way for you alone to prop up the stock if everyone else defects, so any occasional cooperation would be a pure self-loss.  
4.  On the last round (t = r) there is no future to protect, so defecting is obviously optimal.  

Pseudocode  

function AggressiveDefector(t, S, history):  
    # t: current round index (1 ≤ t ≤ r)  
    # S: current stock level  
    # history: full play history so far (ignored)  
    return “D”  

Edge Cases  
- First round (t = 1): returns D.  
- Last round (t = r): returns D.  
- If S = 0: consumption is zero whether C or D; we still return D by default.  

That is the entire strategy.  It requires zero tracking of opponents or of the state beyond knowing the round number exists.  It is maximally aggressive: you always take the larger share whenever you can.
'''

description_AGGRESSIVE_90 = '''
Below is a fully specified “aggressive” strategy—called AggressiveHarvester—that (1) tries to mine cooperators as quickly as possible, (2) rescues the pool when it is in danger of collapse or when opponents over‐defect, and (3) always defects in the last few rounds to grab the final payoff.  You can tune the six parameters (endgame window, low/high stock thresholds, majority‐rule cutoff, etc.) to your particular n, r, capacity, or your aggressiveness level.

---

Strategy name: AggressiveHarvester

Parameters you choose up front (common‐knowledge):  
• w = size of the endgame window (integer ≥1).  
• T_low = lower stock threshold (0 < T_low < T_high < capacity).  
• T_high = upper stock threshold.  
• M = majority threshold on past defections (e.g. M = ⌊(n–1)/2⌋ +1).  

Internal state each round t:  
• S_t = current common‐pool stock at start of round t.  
• Hist = full history of all players’ actions in rounds 1…t–1.

Decision rule for player i in round t:

1.  Endgame grab (last w rounds):  
    If t > r – w, then  
      action_i ← D  
      (Defect unconditionally in the final window to grab what you can.)

2.  Stock‐rescue trigger:  
    Else if S_t < T_low, then  
      action_i ← C  
      (Pool in danger: cooperate to leave more for regrowth.)

3.  High‐stock harvesting:  
    Else if S_t ≥ T_high, then  
      action_i ← D  
      (There’s plenty in the pool—defect to harvest it.)

4.  Conditional exploit/punish:  
    Else  
      let def_count = number of players ≠i who played D in round t–1 (t>1).  
      if t=1, treat def_count=0.  
      if def_count < M,  
        action_i ← D  
        (Opponents mostly cooperated last round—exploit them.)  
      else  
        action_i ← C  
        (Opponents defect too much—cooperate yourself to rescue the stock.)

5.  Edge‐case S_t=0:  
    If S_t=0, any action yields zero payoff. In that case just defect (makes no difference).

Pseudocode

```
function AggressiveHarvester(t, S_t, Hist):
  # t: current round (1..r)
  # S_t: current stock
  # Hist: list of all players’ past actions rounds 1..t-1
  # Parameters: r, w, T_low, T_high, M, n

  # 1) Endgame
  if t > r - w:
    return D

  # 2) Rescue low stock
  if S_t < T_low:
    return C

  # 3) Harvest high stock
  if S_t >= T_high:
    return D

  # 4) Conditional exploit vs. rescue
  if t == 1:
    def_count = 0
  else:
    # Count opponents’ defections in last round
    def_count = count of D in Hist[t-1] among players ≠ i

  if def_count < M:
    # Opponents mostly cooperated → exploit them
    return D
  else:
    # Opponents defected heavily → rescue the pool
    return C

  # 5) If stock is exactly zero (optional check)
  if S_t == 0:
    return D
```

How it works

• First round (t=1):  Treat def_count=0 → step 4 fires → you defect, grabbing S_1/n while everyone else is presumed cooperative.  
• Early rounds while S_t is high:  step 3 forces D—you keep mining.  
• If too many opponents defect in one round (def_count ≥M), you switch to cooperating to leave more resource for the next round. This punishes over‐defection by rescuing the pool yourself.  
• If the pool ever dips below T_low you automatically switch to cooperation until it recovers above T_high.  
• In the final w rounds you defect unconditionally to get the last harvest—you no longer care about future regrowth.

Tuning hints

• w=1 is minimal endgame. If you want to “pull out” for the last two or three rounds, set w=2 or 3.  
• T_low might be set to, say, capacity/4 or capacity/3. T_high to capacity/2 or 2·capacity/3.  
• M is typically a simple majority of opponents (M≈⌊(n–1)/2⌋+1).  

This strategy is unapologetically aggressive:

– It defects at every opportunity to harvest cooperators and at the very end when future impact is moot.  
– It only cooperates when it absolutely must—for survival of the pool (S_t < T_low) or to punish an overly defection‐heavy group by rescuing the stock.  
– It never relies on any private agreements or side‐payments, only on public history and the resource stock.
'''

description_AGGRESSIVE_91 = '''
Below is a fully‐specified “grow-and-grab” strategy we’ll call AggroHarvester.  It is aggressive in that it almost always defects (D), only cooperates (C) when the pool is dangerously low—and, once it ever sees an opponent defect, it switches to permanent defection (a grim trigger) to punish everyone by driving the pool to collapse.

1.  State variables  
   •  punisher (bool): have we ever seen an opponent play D?  Initially false.  
   •  threshold (float) = capacity/4   (when stock falls below this, we briefly cooperate to regrow)  

2.  Initialization  
   punisher ← false  

3.  On the start of each round t=1…r, observe:  
   •  S_t = current common-pool stock  
   •  H_{t–1} = history of all players’ actions through round t–1  

   Update punisher:  
     if in H_{t–1} any opponent j≠i played D then  
       punisher ← true  

   Decision rule for this round:  
     if punisher == true then  
       play D      // permanent punishment  
     else if t == 1 or t == r then  
       play D      // seize the first‐ and last‐round payoff  
     else if S_t < threshold then  
       play C      // brief “rescue‐coop” to let stock regrow  
     else  
       play D      // otherwise always defect  

4.  Explanation of aggressive logic  
   –  Default is defection to grab the largest share each round.  
   –  We only ever cooperate if the stock has fallen below capacity/4, and then only so the pool can regrow enough for us to exploit again.  
   –  If at any point any opponent defects, we enter a grim trigger (“punisher”=true) and defect forever after—collapsing the pool so they get nothing.  
   –  We defect in round 1 to extract early payoff, and in the last round to avoid leaving any surplus for others.  

5.  Pseudocode  

   function AggroHarvesterDecision(t, S_t, history, capacity, r):  
     static punisher ← false  
     threshold ← capacity / 4  
     // 1. Update punisher on observed defections  
     for each past round k < t:  
       for each player j ≠ i:  
         if history[k][j] == D then  
           punisher ← true  
           break out of loops  
     // 2. Decision logic  
     if punisher == true:  
       return D  
     if t == 1 or t == r:  
       return D  
     if S_t < threshold:  
       return C  
     return D  

That completes the aggressive “grow‐and‐grab with grim trigger” strategy.
'''

description_AGGRESSIVE_92 = '''
Below is an “aggressive” common‐pool‐resource strategy—call it Crisis‐Defector—that maximizes your short‐run take (always defects) but will grudgingly cooperate once in a deep “crisis” to try to save the pool from total collapse (so you get at least something in later rounds).  It uses only the public stock S, the round index t, and one tiny piece of internal memory (“have I already cooperated this crisis?”).

1.  Internal state:  
    – cooperated_this_crisis  ∈ {false,true}, initially false.

2.  Parameters (you choose once at the start):  
    – crisis_threshold T = capacity / 4  
      (When S drops below T we are in a crisis.)  
    – total rounds r, current round t ∈ {1…r}.  

3.  Decision rule, in round t when stock is S:

   if t == 1:  
     • First round: Defect.  
     (Always take the maximum on round 1.)

   else if t == r:  
     • Last round: Defect.  
     (No future to protect.)

   else if S ≥ T:  
     • Stock healthy: Defect.  
     (Greedy, exploit large pool.)

   else /* S < T */:  
     • Crisis mode:  
       – if cooperated_this_crisis == false:  
           – Cooperate once.  
           – Set cooperated_this_crisis ← true.  
       – else:  
           – Defect.  
     • If later S in some round rises back to ≥ T, reset crisis flag:  
         cooperated_this_crisis ← false.

Rationale:  
– “Always defect” is your default (maximum immediate gain S/n vs S/(2n)).  
– Only when the pool falls below T do you briefly switch to cooperate once—enough to reduce your draw and marginally boost regrowth—then return to defection.  
– On round 1 and the final round you never “waste” a cooperation.  

Pseudocode  
-----------  
```  
initialize:  
  cooperated_this_crisis ← false  
  T ← capacity / 4  

for each round t = 1…r:  
  observe current stock S  

  if t == 1:  
    action ← D  

  else if t == r:  
    action ← D  

  else if S >= T:  
    // pool ample: always defect  
    action ← D  
    // reset crisis‐flag in case we just climbed out of low‐stock  
    cooperated_this_crisis ← false  

  else:  
    // crisis (S < T): allow one cooperation per crisis  
    if not cooperated_this_crisis:  
      action ← C  
      cooperated_this_crisis ← true  
    else:  
      action ← D  

  play(action)  
endfor  
```  

Edge‐case handling:  
• First round (t=1): aggressive “D” to seize the full initial stock.  
• Last round (t=r): always “D” (no reason to preserve).  
• Single “C” only the first time S dips below T; further dips in the same crisis you exploit again.  
• If stock recovers above T at any point, you clear your “cooperated_this_crisis” flag so that a future crash will again trigger one brief cooperation.  

This strategy is maximally aggressive (defects whenever possible to maximize immediate payoff), but with a minimal “lifeline” at low stock so you avoid zeroing‐out the pool forever.
'''

description_AGGRESSIVE_93 = '''
Below is an “Aggressive‐Regeneration” strategy.  It uses defection as its default (to grab the largest immediate share) but—unlike “always‐defect”—it recognizes that if the pool ever collapses to (near) zero there will be nothing left to exploit in later rounds.  Therefore it occasionally switches to cooperation purely to let the resource grow back, then goes back to defecting and seizing large payoffs again.  It also defects in the final rounds (when there is no future left to protect).

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
1.  PARAMETERS & STATE  
   n             number of players  
   r             total number of rounds  
   capacity      max sustainable stock  
   S_t           current stock at beginning of round t  
   low_thresh    capacity/(2n)        ← if stock falls to this or below, start “regrowth”  
   high_thresh   0.75·capacity        ← once stock recovers above this, resume defecting  
   in_regrowth   Boolean flag, initially FALSE

2.  EDGE‐CASES  
   • Round 1:   in_regrowth = FALSE, so fall into default‐defect behavior.  
   • Final 2 rounds (t ≥ r−1): always defect (no point cooperating when there is almost no future).  
   • If ever S_t = 0, then cooperate every round until stock > high_thresh (to allow any possible regrowth).  

3.  DECISION RULE (for each round t=1…r)  
   if t ≥ r−1 then  
     action ← D  
   else if in_regrowth then  
     if S_t ≥ high_thresh then  
       in_regrowth ← FALSE  
       action ← D  
     else  
       action ← C            # keep letting it regrow  
   else  # default (not in regrowth)  
     if S_t ≤ low_thresh then  
       in_regrowth ← TRUE  
       action ← C            # too low → switch to regrowth mode  
     else  
       action ← D  

4.  EXPLANATION OF “AGGRESSIVE MINDSET”  
   – Default behavior is defection: when the resource is healthy, grab the larger per‐round share (S/n).  
   – Only when the pool is nearly exhausted does it grudgingly cooperate—and only just long enough to let the stock rebuild above a high threshold—then immediately return to defecting.  
   – In the last rounds it defects outright because there is no future to protect, maximizing immediate payoff.  

5.  PSEUDOCODE  

   initialize:  
     in_regrowth ← FALSE  
     low_thresh  ← capacity/(2*n)  
     high_thresh ← 0.75*capacity

   for t in 1…r:  
     observe current stock S_t

     if t ≥ r−1:  
       play D  
       continue

     if in_regrowth:  
       if S_t ≥ high_thresh:  
         in_regrowth ← FALSE  
         play D  
       else:  
         play C  
       continue

     # default (not in regrowth)
     if S_t ≤ low_thresh:  
       in_regrowth ← TRUE  
       play C  
     else:  
       play D  

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
With this rule set you aggressively defect whenever the pool allows, seize the largest short‐term payoffs, only “put the brakes on” long enough to restore the common stock, and then immediately punish again—falling back to full defection at the end.
'''

description_AGGRESSIVE_94 = '''
Here is a simple yet ruthlessly aggressive rule set for the common‐pool game.  It maximizes your round payoffs by defecting every time except in the one situation in which a lone cooperation is the only way to keep the pool alive for future grabs—and it always defects in the last two rounds when there is no future to preserve.

1.  Decision Rules  
    •  First round (t = 1): play D (“Defect”).  
    •  Intermediate rounds (1 < t ≤ r–2):  
       –  If the current stock S_t has just been driven so low that, if everyone defects again, the pool will collapse to zero (i.e. S_t after your D + others’ expected D would be zero), then play C once to leave enough in the pool for regrowth.  
       –  Otherwise play D.  
    •  Last two rounds (t > r–2): play D, since there is no future gain to protecting the pool.  

2.  Handling Edge Cases  
    •  If S_t ever reaches 0, no further growth is possible.  You still “play” D by default (you get 0 payoff, but no worse alternative exists).  
    •  If you find yourself in a scenario where your single C cannot prevent collapse (stock already too low), you still choose D—there is no point sacrificing to a dead pool.  
    •  All ties go to D (i.e. whenever you are indifferent or the future is irrecoverable).  

3.  Aggressive Mindset  
    –  You always grab the high‐payoff defect share whenever you can.  
    –  You only give up immediate payoff in the unique circumstance that, if you didn’t, the pool would die and you’d forego all future payoffs.  
    –  You never “punish” others beyond defecting yourself, since your goal is pure extraction, not reciprocity or fairness.  

Pseudocode  
-----------  
```
INPUTS:
  S_t      // current stock at start of round t
  t        // current round index (1…r)
  r        // total number of rounds
  n, capacity  // known game parameters
  D, C     // actions: Defect or Cooperate

FUNCTION decideAction(S_t, t, r):
  // 1) Always defect in first and last two rounds
  if t == 1 or t > r - 2:
    return D

  // 2) Will everyone defect and drive stock to zero?
  //    Total consumption if all defect = n*(S_t / n) = S_t → S_remaining = 0
  //    If you alone switch to C, your consumption = S_t/(2n),
  //    so S_remaining_after = S_t - [(n-1)*(S_t/n) + (S_t/(2n))]
  //    = S_t - [S_t*(n-1)/n + S_t/(2n)]
  //    = S_t * [1 - ((n-1)/n + 1/(2n))]
  //    = S_t * [1 - ( (2n - 2 + 1) / (2n) )]
  //    = S_t * [1 - ( (2n-1) / (2n) )]
  //    = S_t * (1/(2n)) > 0
  //    So a lone C prevents collapse once.
  //    If the pool would otherwise hit exactly zero, do one C.
  //
  //    (In practice we just check: “If S_t after D by everyone would be 0, then C.”)

  // since D by everyone always exactly empties S_t, we need to check only that S_t>0
  if S_t > 0:
    // We know all‐D empties the pool; so do one C to keep it alive
    return C
  else:
    // Pool is already dead; defect anyway
    return D
```

Discussion  
----------  
–  This rule set never “wastes” a defect opportunity except exactly once in the early/mid game to keep the pool from irretrievable collapse.  
–  By defecting every round except that one minimal cooperation, you harvest almost all the possible surplus—and still enjoy a handful of future rounds of high‐payoff defection.  
–  In the last two rounds you revert to pure defection, since there is no future to protect.
'''

description_AGGRESSIVE_95 = '''
Below is a concise but complete aggressive “always-defect” strategy.  It never cooperates, punishes “would-be” cooperators by always taking the larger share, and maximizes immediate payoffs at the expense of long-term stock.  This is a dominant aggressive approach in a one-shot exploitation sense.

Strategy name: Aggressive Always-Defect (AAD)

1.  Decision rule  
    For every round t=1…r, choose action D (Defect).

2.  Edge cases  
    • First round (t=1): play D.  
    • Last round (t=r): play D.  
    • If the current stock S=0 (nothing left), action doesn’t matter—play D by default.

3.  Rationale  
    • Defect always yields S/n ≥ S/(2n), so at every stage you take the maximum available share.  
    • By never cooperating you force the pool toward depletion faster than any more subtle “harvesting” scheme.  
    • No history dependence is needed—opponent “signals” (cooperate/defect) are irrelevant because you never return cooperation.

Pseudocode

```
function AgressiveAlwaysDefect(round t, stock S, history H):
    # Inputs:
    #   t: current round index (1 ≤ t ≤ r)
    #   S: current common-pool stock
    #   H: full history of past actions (not used here)

    # Always defect
    return D
```

That’s it—complete, unambiguous, and maximally aggressive.
'''

description_AGGRESSIVE_96 = '''
Aggressive “Sustainable Defector” Strategy  
Goal  
  Exploit the common pool as much as possible each round, but avoid complete collapse of the stock until the very endgame.  Cooperate only when the stock is dangerously low in order to trigger regrowth; otherwise always defect (take the larger share).  In the last few rounds, abandon any pretense of sustainability and defect unconditionally.

Parameters (all known to all players)  
  n            number of players  
  r            total rounds  
  C            capacity of the common pool  
Derived constants (you choose these once at the start):  
  α_high = 0.8   “upper stock threshold”  
  α_low  = 0.4   “lower stock threshold”  
  T_high = α_high · C  
  T_low  = α_low  · C  
  G      = ⌈0.2·r⌉   number of endgame rounds in which we always defect  

Notation  
  t         current round (1 ≤ t ≤ r)  
  S_t       stock at the start of round t  

Overview of decision rule  
 1. If we are in the last G rounds (t > r – G), defect.  
 2. Else if S_t ≥ T_high, defect (stock is “healthy,” plunder aggressively).  
 3. Else if S_t ≤ T_low, cooperate (stock is too low—allow some growth).  
 4. Else (T_low < S_t < T_high), defect.  

Pseudocode  
```  
# Pre‐play (choose once):  
α_high ← 0.8  
α_low  ← 0.4  
T_high ← α_high * C  
T_low  ← α_low  * C  
G      ← ceil(0.2 * r)  

for t in 1…r:  
    observe S_t  # current stock  
  
    if t > r - G then  
        action ← D        # endgame: always defect  
    else if S_t >= T_high then  
        action ← D        # stock is high: aggressive harvest  
    else if S_t <= T_low then  
        action ← C        # stock is dangerously low: allow regrowth  
    else  
        action ← D        # default aggressive choice  
    end if  

    play action  
end for  
```  

Explanation of Choices  
1. Endgame defection (lines 2–3):   
   Once you’re in the final G≈20% of rounds, there is no future to protect—so always defect and grab the big payoff.  
2. High‐stock defection (line 4):   
   If the pool is at or above 80% of capacity, you risk little by defecting—other players’ tiny cooperations will regrow it anyway, so you maximize your share.  
3. Low‐stock cooperation (line 6):   
   If the pool has fallen below 40% of capacity, unilateral cooperation by all players would stimulate the logistic regrowth most strongly.  By cooperating yourself, you signal at least one “cooperator,” helping move the stock back into the profitable region for future exploitation.  
4. Default defection (line 8):   
   Between the two thresholds, lean aggressive—defection maximizes your per‐round payoff without immediately crashing the pool.  

Edge Cases  
• First round (t = 1): S₁ = C ≥ T_high, so D (straight defect).  
• Last round (t = r): always t > r – G, so D—take everything you can.  
• Exact thresholds S_t = T_high or T_low: we defect when S_t = T_high, cooperate at S_t = T_low.  

Aggressiveness Rationale  
– You only cooperate when the pool risks collapse (S_t ≤ 0.4 C).  Even then it is a one‐round concession to protect future profits.  
– 90%+ of the time you defect, maximizing immediate payoffs.  
– In the true endgame you abandon any conservation and defect every remaining round.
'''

description_AGGRESSIVE_97 = '''
Below is a self‐contained, “aggressive” strategy for the repeated Common Pool Resource game.  Its guiding principle is:  
–  Always defect (take the larger share) to the maximum extent possible  
–  But when the resource stock is in danger of collapse (too low), temporarily switch to cooperation long enough to nurse it back to a healthy level, so that you can exploit it again in subsequent rounds  
–  Always defect on the very last round  

—–  
1. Notation and parameters  
•  n, r, capacity as given.  
•  t = current round, t ∈ {1,…,r}.  
•  S_t = stock available at the start of round t.  
•  A_i,t ∈ {C,D} = your action at round t.  
•  Define two stock thresholds:  
   –  Θ_low = 0.2 × capacity  (below this we risk collapse)  
   –  Θ_high = 0.8 × capacity (once we’ve nursed stock up near capacity, we can defect again)  
•  Define a rescue‐period parameter R_rescue = 3 (number of consecutive cooperations once Θ_low is breached).  
•  Maintain a counter rescue_count which, once triggered, forces you to play C for up to R_rescue rounds or until the stock climbs above Θ_high.  

2. State variables  
At the start initialize:  
   rescue_count ← 0  

3. Decision rules (pseudocode)  
For each round t = 1…r:  
   if t == r then  
     play D  // last‐round defection  
   else if rescue_count > 0 then  
     play C  
     rescue_count ← rescue_count – 1  
     // but if by the next round S_{t+1} ≥ Θ_high, reset rescue_count to 0  
   else if S_t ≤ Θ_low then  
     // stock dangerously low ⇒ trigger rescue  
     rescue_count ← R_rescue – 1  // we play C now plus R_rescue–1 future Cs  
     play C  
   else  
     // normal exploitation mode  
     play D  

After each round ends and S_{t+1} is computed, do:  
   if S_{t+1} ≥ Θ_high then  
     rescue_count ← 0  // cancel any remaining rescue rounds  

4. Explanation of the main features  
•  First round: S₁ = capacity ≥ Θ_low ⇒ rescue_count=0 so you defect.  You test and exploit immediately.  
•  “Aggressive” default: whenever stock is healthy (above Θ_low) and you are not in a mandated rescue sequence, you defect.  This maximizes your per‐round payoffs.  
•  Resource‐safeguard: if stock ever falls to Θ_low or below, you enter a short “rescue” phase of R_rescue total cooperations to allow regrowth.  This ensures the resource does not collapse permanently, preserving high future payoffs for you.  
•  Exit rescue early: if your coop sequence has driven S back above Θ_high, you immediately return to defection, even if you have not used all R_rescue rounds.  
•  Last round: always defect, since no future rounds remain.  

5. Edge cases handled  
–  If you trigger rescue on round r–1, you will play C in r–1 (to help regrow) and then D in r (because last round override).  
–  If the rescue sequence never succeeds in raising S above Θ_high before r, you’ll play your remaining Cs, then defect in the final round.  
–  If the pool collapses to zero despite your rescue attempts (e.g. opponents never cooperate), the strategy still prescribes actions (you’ll play C until rescue_count=0, then D), but payoffs remain zero—this is unavoidable if opponents all defect.  

6. Why this is aggressive  
–  You defect in  almost every round except the minimal “life‐support” cooperations needed to sustain the pool.  
–  You maximize short‐run gains while injecting just enough cooperation to avoid permanent resource collapse.  
–  You never “forgive” or reciprocate opponents’ cooperations beyond the rescue protocol—you do not build trust or long sequences of mutual cooperation.  

—–  
That completes the description. Implementation simply follows the pseudocode above to keep track of rescue_count and the current stock S_t.
'''

description_AGGRESSIVE_98 = '''
Below is an “Aggressive Regenerator” strategy.  Its philosophy is to defect (“D”) almost always (to grab the highest per‐round payoff), but to tolerate exactly enough cooperation (“C”) to keep the pool from collapsing to zero (so there is something left to exploit).  In particular we only switch into a “regen” phase when the stock falls below a low threshold, and we stay in that phase until the stock recovers above a high threshold.  First and last rounds are always defect (no future to protect, so exploit fully).

Parameters (choose once at the start):  
• L = capacity/3   (low‐stock threshold)  
• H = 2×capacity/3   (high‐stock threshold)  

State variable: regen_mode ∈ {false, true}, initially false.

Strategy description:  

Round t from 1…r:  
1.  Observe current stock S_t.  
2.  If t == 1 or t == r:  
      Play D.  (First or last round—no need to preserve future.)  
3.  Else if regen_mode == true:  
       • If S_t < H: play C and remain in regen_mode=true.  
       • Else (S_t ≥ H): play D and set regen_mode=false.  
4.  Else (regen_mode == false):  
       • If S_t < L: play C and set regen_mode=true.  
       • Else (S_t ≥ L): play D and remain in regen_mode=false.  

Rationale:  
- By defecting whenever the stock is “safe” (≥ L), we maximize our immediate π_i = S/n.  
- Once S falls below L, further universal defection would drive the pool toward zero.  To prevent that, we temporarily switch into regen_mode to cooperate until the stock grows back above H.  
- The hysteresis gap [L, H] prevents flip‐flopping every round if the stock hovers near a single threshold.  
- In the last round we defect regardless—there is no future round to preserve, so we take the largest possible payoff.  
- We never try to reciprocate on the basis of opponents’ individual choices—we ignore their history except as it shows up in the aggregate stock.  This is pure exploitation with minimal “maintenance” of the common pool.

Pseudocode  
-----------  
```
Input:     n, r, capacity  
Constants: L = capacity/3  
           H = 2*capacity/3  
Variables: regen_mode = false   // start off exploiting

for t in 1…r:
    observe current stock S_t

    if t == 1 or t == r:
        action = D

    else if regen_mode == true:
        if S_t < H:
            action = C
            // stay in regen_mode
        else:
            action = D
            regen_mode = false

    else:  // regen_mode == false
        if S_t < L:
            action = C
            regen_mode = true
        else:
            action = D

    play(action)
```

Notes on edge cases:  
- If capacity is exactly 2n (the minimum allowed), the thresholds still work numerically—L=2n/3, H=4n/3.  
- If the stock ever hits zero, it stays zero; regen_mode will be true and we’ll keep playing C, but π_i = 0 and no regrowth occurs.  That is simply the penalty for over‐exploitation.  
- If r=2, we defect both rounds (first and last).  
- For any r>2, there is exactly one or more regen phases only if other players together push S below L.  Otherwise we keep defecting each round.  

This strategy is “aggressive” because it defects in every round where resource is safe, extracts maximum payoff, and only “sacrifices” one or more rounds of lower‐payoff cooperation when strictly necessary to avoid annihilating the pool.
'''

description_AGGRESSIVE_99 = '''
Below is an “exploit‐and‐punish” strategy that we call Aggressive Harvest.  It cooperates early to build up the common pool (and to lull others into cooperation), then switches to indiscriminate defection in mid‐game, and never forgives once any defection is observed.  In the last half of the game it defects regardless—extracting the maximum it can—so as to “harvest” the resource before the game ends.

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
Parameters your code will know:  
  n        – number of players  
  r        – total rounds  
  capacity – maximum sustainable stock  

Internal state:  
  defection_detected ← false  
  T_switch ← ⌈r / 2⌉   (start mass‐defection in round T_switch+1)

Per‐round decision (round t, current stock S_t, full history of past actions):

Pseudocode:

```
function AggressiveHarvest(t, S_t, history):
    # 1. Update defection flag
    for each past round τ = 1..t−1:
        for each player j ≠ me:
            if history[τ][j] == D:
                defection_detected ← true

    # 2. Edge‐cases
    if t == 1:
        # First round: show cooperation to build stock and tempt cooperators
        return C

    # 3. If in last half, always defect
    if t > T_switch:
        return D

    # 4. Mid‐game: if any defection ever seen, punish forever
    if defection_detected:
        return D

    # 5. Otherwise (no defections so far, early round) cooperate
    return C
```

Explanation of each step:

1.  First round t = 1: pick C to help build up the stock and signal trust.  
2.  Maintain a boolean “defection_detected.”  As soon as any other player has ever chosen D in the history, we flip it to true and never reset.  
3.  We divide the game into two phases by T_switch = ⌈r/2⌉.  In rounds t > T_switch we always choose D.  This guarantees we extract the maximum in the final half of the game—no chance to be “too nice” when little future is left.  
4.  In the first half (t ≤ T_switch), if anyone has defected in a prior round, we switch to permanent defection (punishment).  
5.  In the first half and only if no defection has ever been seen, we cooperate to help regenerate the resource and lull opponents into more cooperation.  

Why it’s aggressive:

•  You exploit cooperators in round T_switch+1 onward by defecting en masse when the stock is still relatively high.  
•  You never tolerate free‐riding: a single defection by any opponent triggers permanent defection, ensuring you don’t get exploited.  
•  You front‐load cooperation only as long as everyone else does—no “return to trust” once broken.  

Variants / edge‐case notes:

–  If the pool ever collapses (S_t ≈ 0), D and C yield zero payoff anyway, so the rule “always defect” still maximizes your tiny share.  
–  You could shift T_switch earlier or later depending on r, but r/2 is a simple midpoint cut.  
–  If you wish, you can refine by checking S_t versus a threshold (e.g. if S_t drops below capacity/4 then defect immediately), but the above handles low‐stock naturally via the defection flag.
'''

description_AGGRESSIVE_100 = '''
Below is a complete description of an “Aggressive Resource‐Grabber” strategy.  Its philosophy is simple: seize as much as you safely can most rounds, but—only when the pool is in danger of collapse—barely cooperate to buy yourself one more high-payoff round, then resume grabbing.  In the last few rounds (when there is no future to preserve), you defect flat-out.  

1.  Parameters (you choose or tune before play)  
   •  endgame_length E ∈ ℕ (e.g. E=1 or 2): in the last E rounds, you always defect.  
   •  collapse_threshold Sₜₕ (0 < Sₜₕ < capacity): if current stock Sₜ ≤ Sₜₕ, you “rescue” the pool by cooperating.  

2.  High-level rule  
   For each round t = 1…r, observe the current stock Sₜ.  
   a) If t > r – E:  
      action = D  (no future to protect)  
   b) Else if Sₜ ≤ Sₜₕ:  
      action = C  (minimally cooperate to allow regrowth)  
   c) Else:  
      action = D  (defect to grab the larger share)  

3.  Edge cases  
   •  First round (t=1): t is not in the last E rounds, and stock is full S₁=capacity > Sₜₕ, so action = D.  
   •  Rounds 2…(r–E): you defect unless the stock has fallen to or below Sₜₕ.  
   •  Last E rounds: you defect regardless of stock.  
   •  If Sₜ=0 you get zero whether C or D; action logic still applies (you’d cooperate if t≤r–E and Sₜ≤Sₜₕ=0, but payoff is zero).  

4.  Setting Sₜₕ  
   A reasonable rule is Sₜₕ = capacity/(2n) (half the per-player cooperative draw when everyone cooperates).  At that level, a tiny cooperative draw yields enough remaining stock that regrowth can push you back into a high-stock regime.  

5.  Pseudocode  

   initialize:  
     E ← 2                       # always defect in the last 2 rounds (t > r−2)  
     S_thresh ← capacity/(2n)    # threshold to “rescue” the pool  

   for t in 1..r:  
     observe current stock S_t  
     if t > r − E then  
       action ← D  
     else if S_t ≤ S_thresh then  
       action ← C  
     else  
       action ← D  
     end if  
     play(action)  

6.  Why is this aggressive?  
   – You defect in nearly every round, grabbing the larger S_t/n share.  
   – You only “cooperate” when absolute necessity (stock has fallen so low your future rounds would yield almost nothing otherwise).  
   – You never reciprocate cooperation or attempt to build trust—there is no tit-for-tat or generous phase.  
   – In the final E rounds your only concern is immediate payoff, so you defect unconditionally.  

This strategy maximizes short‐term extraction almost everywhere, only sacrificing a minimal draw when the common pool is in danger of complete exhaustion, and never relinquishing any advantage in the endgame.
'''

description_AGGRESSIVE_101 = '''
Below is an “aggressive‐exploit with just‐enough‐conservation” strategy.  In plain language it says: “Defect every round (to grab the big share) except when the common stock has fallen so low that if everyone defects it will collapse; in those ‘danger’ rounds (but not in the very last round!) switch to cooperate briefly so the pool can bounce back, then go right back to defecting.”

1.  Parameters you choose once before play  
    •  n, capacity (given)  
    •  r (number of rounds)  
    •  Threshold θ = capacity / n  
       (“If the stock ever falls to θ or below, full defection would wipe it out, so we’ll cooperate then.”)

2.  Intuition  
    –  Defect yields S / n this round vs. Cooperate yields only S / (2 n).  So whenever the pool is healthy we defect.  
    –  But if stock S_t ≤ θ, then n simultaneous defections would drive S_remaining to zero and kill all future profits.  So in those “danger” rounds we cooperate to leave most of S_t in the pool and trigger regrowth.  
    –  In the last one or two rounds we always defect (there’s no point in conserving for the future).

3.  Pseudocode  

    function Decide(S_t, t):  
      input:  
        S_t = current stock at beginning of round t  
        t = current round index (1 ≤ t ≤ r)  
      output:  
        action ∈ {C, D}  

      // 1. If we’re in the last round (or second‐to‐last) we defect  
      if t ≥ r − 1 then  
        return D  

      // 2. If pool is dangerously low, cooperate to let it regrow  
      if S_t ≤ capacity / n then  
        return C  

      // 3. Otherwise, exploit by defecting  
      return D  

4.  Explanation of edge‐cases  
   –  Round 1: S_1 = capacity > capacity/n ⇒ we defect.  
   –  Early rounds with healthy stock: defect every time to maximize immediate payoff.  
   –  Any round t (except the very last two) with S_t ≤ capacity/n: cooperate so that S_remaining = S_t − S_t/(2n) remains positive and then regrows.  
   –  Rounds r−1 and r: always defect, since no future beyond r to conserve for.  

5.  Why it’s aggressive  
   –  It defects in every round where doing so does not guarantee total ruin of the common pool.  
   –  It only “pays the cooperation cost” when necessary to prevent resource collapse, and even then only until the regenerating dynamics take hold.  
   –  It never “forgets” or softens after opponents have punished or cooperated; it simply checks the resource‐level threshold.  

This strategy guarantees you the highest possible per‐round take in healthy times and sacrifices minimal payoff only when the pool is critically low—just enough to keep the game going so you can exploit it again later.
'''

description_AGGRESSIVE_102 = '''
Below is a pure “plunder‐and‐burn” strategy—i.e. an all‐out, never‐cooperate approach.  It maximizes your own one‐period payoffs regardless of future resource consequences, and handles first/last rounds trivially by doing the same thing every time.

1.  High-Level Description  
    •  In every single round t (including t=1 and t=r), play D (“Defect”)  
    •  Never cooperate, never forgive, never try to build up the stock  

2.  Why it is “Aggressive”  
    •  You always take the larger share (S/n rather than S/(2n))  
    •  You ignore sustainability and future‐stock concerns  
    •  You exploit any cooperator in every round  

3.  Edge Cases  
    •  Round 1: no history exists – still play D  
    •  Last round r: there is no future to protect – play D (standard final‐round defection)  
    •  Zero stock: D yields zero, but C would also yield zero.  We still play D by default.  

4.  Pseudocode  

    Input:  
      n        // number of players  
      r        // total rounds  
      capacity // resource cap (unused by our rule)  
    Observe each round only the past history H, the current stock S    

    For t = 1 to r do  
      action_i ← D  
    End For  

    // That’s it – you never switch to C.  

5.  Tournament Note  
    •  Against any strategy that sometimes cooperates, you will always exploit them.  
    •  Against all‐defectors, you are on equal footing (everyone gets S/n each round).  
    •  You never incur the payoff cost of cooperation, so you are maximizing myopic gain every single round.
'''

description_AGGRESSIVE_103 = '''
Below is a fully self-contained “aggressive” harvesting strategy.  It never tries to build a long-term cooperative relationship; instead it (1) relentlessly exploits any cooperator, (2) only “surrenders” for one round when everybody else has driven the pool to zero, and (3) always defects in the final round.  

1.  Plain-English description  
   •  Round 1: defect.  You seize as much as you can at the outset.  
   •  In any round t>1 that is not the last (t<r):  
      –  If in the immediately preceding round (t−1) all n players defected, then cooperate this round.  
         •  Rationale: if everybody defected last round, the pool is dead (S≈0). By cooperating now you let it regrow—solely so you can exploit it again in the next rounds.  
      –  Otherwise (i.e. at least one player cooperated last round), defect.  
         •  Rationale: exploit any goodwill shown by others; punish cooperators by taking the larger share.  
   •  Round r (the last round): defect, regardless of history.  There is no future to sacrifice to.  

   This rule set guarantees:  
     – You always get the larger share whenever there is someone to exploit.  
     – If everyone drives the resource to zero, you briefly “give in” to let it bounce back, then resume exploitation.  
     – You never miss the last–round grab.

2.  Pseudocode  
```
Inputs:
  history[t][i]   // action of player i in round t, C or D
  currentRound t, totalRounds r

Function AggressiveHarvest(t, history):
  if t == 1:
    return D     // round 1: defect
  if t == r:
    return D     // last round: defect

  // look at round t-1
  unanimousDefection = true
  for each player i = 1..n:
    if history[t-1][i] != D:
      unanimousDefection = false
      break

  if unanimousDefection:
    return C     // everyone defected last round; cooperate now to regrow
  else
    return D     // otherwise, exploit any cooperator
```

3.  Handling edge‐cases  
  •  First round (t=1): no history → defect.  
  •  Last round (t=r): always defect, since there is no future punishment.  
  •  Zero–stock scenario: if all defect in some round, the stock falls to zero (or near zero).  On the next round your “unanimousDefection” test fires and you cooperate, permitting regrowth.  Opponents who follow the same rule will also cooperate, restoring the pool.  

4.  Why this is “aggressive”  
  – It never “rewards” a defector by cooperating after they defect; it only cooperates when everyone has already destroyed the resource.  
  – It punishes any one who cooperates by immediately defecting in the next round.  
  – It nukes any long-term reciprocation: you only ever cooperate so that you’ll have something left to exploit.  
  – The final round is a guaranteed defection.  

In a tournament of independent strategies, this rule will extract as much as possible from cooperators, force periodic resource regeneration only when all‐out defection has occurred, and seize the last‐round prize unconditionally.
'''

description_AGGRESSIVE_104 = '''
Below is a self‐contained “Aggressive Harvest with Regeneration” strategy.  It uses simple stock‐level thresholds to decide when to defect (harvest hard) and when to cooperate (slow down consumption so the pool can regrow).  In addition it always defects in the final round to grab the last drop.

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
PARAMETERS you choose once, before the game:

  •  T_low_frac  = 0.5    (fraction of capacity below which we cooperate)  
  •  T_high_frac = 0.8    (fraction of capacity above which we defect)  
  •  d_last      = 1      (number of last rounds always defect)  

You may tune T_low_frac, T_high_frac and d_last to your liking.  
We recommend T_low_frac≈0.4–0.6, T_high_frac≈0.7–0.9, d_last≥1.

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
Notation:

  •  r       = total rounds  
  •  t       = current round index (1…r)  
  •  S_t     = current common‐pool stock at start of round t  
  •  capacity = maximum stock  

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
HIGH-LEVEL DESCRIPTION

1.  First round t=1: Cooperate.  
2.  Last d_last rounds (t > r – d_last): Defect.  
3.  Intermediate rounds:  
      –  If S_t ≥ T_high_frac·capacity      → Defect  
      –  Else if S_t ≤ T_low_frac·capacity  → Cooperate  
      –  Else                              → Defect  
4.  Exception: If for three consecutive rounds the stock has collapsed  
    (S_t < S_{t–1} < S_{t–2}), force one round of Cooperate to help recovery.

This keeps the pool in a “sweet spot” between T_low_frac and T_high_frac.  You let it regrow when it dips too low, then exploit it when it’s high.

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
PSEUDOCODE

Initialize:
  T_low  = T_low_frac  * capacity
  T_high = T_high_frac * capacity
  collapse_count = 0

For each round t = 1 to r do:
  Observe current stock S_t

  # 1) Edge cases: first and last rounds
  if t == 1 then
    action ← C
  else if t > r – d_last then
    action ← D
  else
    # 2) Detect stock collapse
    if t ≥ 3 and S_t < S_{t–1} and S_{t–1} < S_{t–2} then
      collapse_count ← collapse_count + 1
    else
      collapse_count ← 0
    end if

    if collapse_count ≥ 1 then
      # invest in recovery
      action ← C
      collapse_count ← 0
    else
      # 3) Threshold decision
      if S_t ≥ T_high then
        action ← D
      else if S_t ≤ T_low then
        action ← C
      else
        action ← D
      end if
    end if
  end if

  Play(action)
  Observe all consumptions and update stock S_{t+1} by the game’s rule.
End for

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
WHY THIS IS AGGRESSIVE

  •  We always defect in the very last rounds to grab every remaining unit.  
  •  Whenever the pool is “high,” we milk it at the D‐rate (S_t/n), doubling our  
     payoff relative to a C‐player.  
  •  We only slow down (play C) when the pool dips below T_low, and even then  
     only long enough to get it back above the threshold.  
  •  No attempts at altruism or “fairness.”  All cooperation is tactical—purely to  
     restore the common pool so we can exploit it again.  

Over repeated play against ordinary defectors and cooperators, this strategy will  
typically out‐earn both:  it extracts at D‐rates most of the time, but avoids long‐term  
collapse by judicious “green‐light/stop‐light” control of the resource.
'''

description_AGGRESSIVE_105 = '''
Below is a fully‐specified, “aggressive” threshold‐and‐punishment strategy.  It defects by default, only “lets the pool breathe” when the stock is low, and immediately punishes any defector who exploits its cooperation.  In the final rounds it simply grabs everything it can.

––––––––––––––––  
Strategy name:  Aggressive Threshold‐and‐Punisher  
––––––––––––––––  
Parameters (set once at start):  
• n      = number of players  
• r      = total rounds  
• C_max  = capacity  
• T_low  = capacity/4   (low‐stock threshold)  

State variables (updated each round):  
• t       = current round (1 … r)  
• S_t     = current stock at start of round t  
• punish  = Boolean flag, initially false  

Decision rule (what I play in round t):  
1.  If t == 1:  
      action ← D  
2.  Else if t ≥ r–1:            // last two rounds  
      action ← D  
3.  Else if punish == true:     // punish one round only  
      action ← D  
4.  Else if S_t ≤ T_low:         // let the stock regrow  
      action ← C  
5.  Else:                        // default is to defect  
      action ← D  

After all actions in round t are observed, update punish‐flag for next round:  
  If I played C and at least one opponent played D this round,  
     then punish ← true  
  else  
     punish ← false  

––––––––––––––––  
Pseudocode  

```
Initialize:
  T_low   = capacity / 4
  punish  = false

For t in 1..r do:
  Observe stock S_t

  If t == 1:
    my_action = D
  Else if t ≥ r–1:
    my_action = D
  Else if punish:
    my_action = D
  Else if S_t ≤ T_low:
    my_action = C
  Else:
    my_action = D

  Play my_action simultaneously.

  // After seeing everyone’s actions this round:
  If (my_action == C) and (exists j ≠ me with action_j == D):
     punish = true
  Else:
     punish = false

  // Compute next‐round stock from game formula.
End for
```

––––––––––––––––  
Intuition and aggressiveness  
1. “Defect by default”: We harvest the large share (S_t/n) as often as possible.  
2. “Threshold cooperation”: Only if the pool has been driven below one‐quarter of capacity do we switch to the small take (S_t/(2n))—giving the resource a chance to regrow.  
3. “Single‐round punishment”: If we ever cooperate and someone defects against us, we immediately go back to defecting for exactly one round (skimming the pool while they’re weakened).  
4. “End‐game grab”: In the last two rounds we always defect—no need to conserve once the tournament is closing.  

This plan maximizes short‐term takes, only sacrifices a round when the resource is critically low, and never forgives an opponent who exploits our one concession longer than strictly necessary.
'''

description_AGGRESSIVE_106 = '''
Below is a self-contained “Aggressive Preserver” strategy.  It defects almost always—harvesting the maximum share—but slips into cooperation only when the pool is perilously low, just enough to give it a chance to regrow for future exploitation.  This meets the requirement to be clearly aggressive yet avoid total collapse of the resource (which would end your earnings).

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
1.  Parameters and notation  
   • n    = number of players  
   • r    = total rounds (indexed t=1…r)  
   • S_t  = stock at the start of round t  
   • cap  = capacity (maximum stock)  
   • C    = cooperate (take S_t/(2n))  
   • D    = defect   (take S_t/n)  
   • T    = preservation threshold = cap/(2n)  

   Rationale for T:  
   If S_t ≤ T then a single defection next round would almost exhaust or severely deplete the stock.  By cooperating instead, you leave more in the pool, triggering positive growth, and you preserve the chance to defect again later.

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
2.  Decision rules

Pseudocode:

function AggressivePreserver(S_t, t):
    if t == 1:
        # first‐move aggression: grab maximum
        return D
    if t == r:
        # last‐round: no future to protect—defect
        return D

    # intermediate round
    if S_t <= cap/(2n):
        # stock is critically low → cooperate to let it regrow
        return C
    else:
        # otherwise: defect and harvest maximum
        return D

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
3.  Edge cases and notes  
 • If S_t = 0 (pool exhausted), your “cooperate” withdrawal is zero; you just wait for growth.  
 • If all players follow this rule, once S_t falls below cap/(2n), everyone shifts to C that round, stock regrows, then on the next round (when S_t > cap/(2n)) everyone defects again.  You enjoy repeated windows of high defection payoffs.  
 • No history beyond current stock is needed.  You never “forgive” or “punish” other players by name—aggression is unconditional except for preserving the resource.  
 • If opponents try to cooperate to maintain the pool, you still defect unless the stock is critically low.  You exploit their goodwill.  
 • The only bit of “cooperation” is purely self-interested preservation; it maximizes your cumulative payoff across r rounds by preventing total collapse.

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
4.  Why it’s aggressive  
 • You defect in round 1 to grab the largest share before anyone can “establish trust.”  
 • You defect every round thereafter except the precise moments when resource exhaustion is imminent—only then do you temporarily pull back.  
 • In the final round you renege completely (defect) since there is no future cost.  
 • You never incorporate any forgiving gestures or tit-for-tat; this is pure self-interest with a minimal sustainability guard.
'''

description_AGGRESSIVE_107 = '''
Below is a self-contained, “aggressive” strategy that (i) maximizes immediate grabs whenever the pool is ample, (ii) only “gives back” (i.e. cooperates) when the pool is so depleted that future exploitation would yield almost nothing, and (iii) always defects in the last round.  It uses two thresholds on the current stock, Low (L) and High (H), to switch between an Exploit mode and a Regrow mode.

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
1.  Strategy overview  
   • Modes:  
     – Exploit: always defect (D) to grab S/n each round.  
     – Regrow: always cooperate (C) to consume only S/(2n), letting the pool recover.  
   • Switch to Regrow only when the stock falls at or below a low‐water mark L.  
   • Switch back to Exploit as soon as the stock recovers to at least a high‐water mark H.  
   • In the final round t = r, always defect.  

2.  Parameter choice  
   Let capacity be the known maximum stock.  Choose two stock‐thresholds:  
     L = 0.25 × capacity   (when stock ≤ L, the pool is too low to exploit)  
     H = 0.75 × capacity   (once stock ≥ H, we can safely exploit again)  

   You can tune L and H (e.g. L = 0.2c, H = 0.8c), but must satisfy 0 < L < H < capacity.  

3.  Full decision rule (per round t = 1…r)  
   Maintain a variable Mode ∈ {Exploit, Regrow}.  Initialize Mode ← Exploit.  

   Observe current stock S_t at the start of round t.  

   If t = r (last round):  
       Action ← D  
       (We take the maximum payoff and end.)  

   Else if Mode = Exploit:  
     If S_t ≤ L:  
       Mode ← Regrow  
       Action ← C   (pool is too low; switch to regeneration)  
     Else:  
       Action ← D   (stock high enough—grab the big share)  

   Else if Mode = Regrow:  
     If S_t ≥ H:  
       Mode ← Exploit  
       Action ← D   (pool recovered—go back to exploitation)  
     Else:  
       Action ← C   (keep cooperating until stock recovers)  

4.  Rationale & aggressiveness  
   – “Always defect” whenever you can still get a big slice (S/n) and the pool is above L.  
   – Only cooperate when the pool is almost exhausted (S ≤ L), to force regrowth so you can exploit again later.  
   – Never “reward” other cooperators—your cooperation is purely instrumental to restore the resource for future grabs.  
   – Final‐round defection guarantees you don’t subsidize regrowth that you won’t exploit.  

5.  Pseudocode  

   ```
   Input: n, r, capacity
   Parameters: L = 0.25 * capacity
               H = 0.75 * capacity

   Mode ← "Exploit"

   for t in 1,…,r:
     observe S_t

     if t == r:
       A_t ← D
     else if Mode == "Exploit":
       if S_t ≤ L:
         Mode ← "Regrow"
         A_t ← C
       else:
         A_t ← D
     else:  # Mode == "Regrow"
       if S_t ≥ H:
         Mode ← "Exploit"
         A_t ← D
       else:
         A_t ← C

     play A_t simultaneously
     observe all consumptions, update S_{t+1}
   end for
   ```

6.  Edge cases handled  
   • First round (t=1): Mode=Exploit, so defect.  
   • Last round: forced defect.  
   • If stock ever hits 0, you enter Regrow (S ≤ L) and keep cooperating until S ≥ H.  
   • If the pool alternately crosses L and H, you naturally cycle Exploit ↔ Regrow.  

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
This strategy is aggressive because it never willingly foregoes a high‐payoff defection unless forced by near exhaustion—and even then only to preserve the resource for more future defections.
'''

description_AGGRESSIVE_108 = '''
Below is a purely non-cooperative, “exploit‐and-punish” strategy that aggressively free-rides on cooperators but grudgingly contributes just enough to keep the resource alive when it’s in danger of collapse.  It always defects in the last round(s) and uses simple thresholds on observed cooperation rates and current stock to decide when to “lend a hand” to the commons.

1.  Parameter definitions  
   •  D = “Defect” (take S/n)  
   •  C = “Cooperate” (take S/(2n))  
   •  r = total rounds  
   •  t = current round index (1…r)  
   •  S_t = stock at start of round t  
   •  n = number of players  
   •  coop_frac_t–1 = fraction of players who chose C in round t–1  
   •  θ_low = 0.25 × capacity  
   •  θ_high = 0.75 × capacity  
   •  α = 0.5   (cooperation‐rate threshold)  

2.  Verbal description of the decision-rule  
   •  First round (t = 1): Defect.  Immediately seize the largest possible share.  
   •  Last round (t = r): Defect.  No future to protect.  
   •  Pre-endgame (2 ≤ t ≤ r–1):  
     –  If S_t < θ_low:  the resource is dangerously low.  “Cooperate” once to help regrow.  
     –  Else if coop_frac_t–1 ≥ α and S_t > θ_high:  a majority cooperated last period and the stock is still high.  Exploit them: Defect.  
     –  Else if coop_frac_t–1 < α and S_t < θ_high:  defection is rampant and stock is starting to slip.  Play “Cooperate” to prop it up.  
     –  Otherwise: Defect.  

   This rule aggressively defects whenever you can get away with it—only grudgingly cooperates when the stock is close to collapse or when too many opponents are already defecting (so that further resource loss would hurt you all).  

3.  Pseudocode  

   initialize θ_low ← capacity * 0.25  
   initialize θ_high ← capacity * 0.75  
   initialize α ← 0.5  

   for t in 1…r:  
     observe S_t, coop_frac_t–1  (for t=1 define coop_frac_0 = 0)  

     if t == 1:  
       action_t ← D  

     else if t == r:  
       action_t ← D  

     else:  
       if S_t < θ_low:  
         action_t ← C       // rescue commons before it dies  
       else if coop_frac_t–1 ≥ α and S_t > θ_high:  
         action_t ← D       // exploit cooperators while resource is plenty  
       else if coop_frac_t–1 < α and S_t < θ_high:  
         action_t ← C       // too many defectors, stock slipping—help sustain  
       else:  
         action_t ← D       // default to defection  

     play action_t  

4.  Edge‐case handling  
   •  Zero stock (S_t = 0): nothing to gain; still report Defect (D) by convention.  
   •  Near-end (t = r–1): the above rule still applies—only the very last round is guaranteed defection.  
   •  Midgame “corrections”: if a single cooperation round does not raise S back above θ_low, the strategy will continue to play C in subsequent rounds until S_t ≥ θ_low.  

This strategy is aggressive because it:  
– Begins by defecting,  
– Tightly free-rides on any majority cooperation,  
– Only “gives” to the commons when it must in order to avoid total collapse (which would destroy all future gains),  
– And always defects in the final round where no punishment or future capital remains.
'''

description_AGGRESSIVE_109 = '''
Below is a completely self‐contained, aggressive “exploit‐until‐rescue” strategy.  It never tries to build mutual cooperation; it simply milks the pool to the maximum sustainable extent, only “sacrificing” one round of its own extraction when the stock is so low that the pool would otherwise die and all future rents would vanish.

---

Strategy name:  Threshold Exploit-Rescue (TER)

Intuition  
1.  In every round except the last, defect (D) so long as the stock S is above a minimal “death threshold.”  
2.  Once S falls at or below that threshold, cooperate (C) for exactly one round to leave enough in the pool for regrowth.  
3.  In the final round, always defect—there is no future to protect.

Parameters (derived from game constants n, capacity):  
 •  θ = capacity / (2n)  
  –  This is the stock level below which a single round of cooperation leaves enough residue for a positive growth phase.  

Decision rule for round t with current stock S_t:

1.  If t == r (last round):  
  Action ← D  
2.  Else if S_t ≤ θ (pool nearly exhausted):  
  Action ← C  
  (mark “rescue” round; any subsequent round S will have grown above θ, so you return to defecting)  
3.  Else:  
  Action ← D  

Pseudocode  

  function TER_Decision(S_t, t, r, n, capacity):  
      θ ← capacity / (2*n)  
      if t == r:  
          return “D”                    # last‐round sneak attack  
      if S_t ≤ θ:  
          return “C”                    # rescue cooperation to allow regrowth  
      else:  
          return “D”                    # otherwise always defect  

Behavior over time  
– Rounds 1…T_max: you defect, extracting S_t/n each.  The pool depletes fast.  
– Once S_t first drops to ≤ θ (say at round T), you switch to C for that round alone.  That leaves a small residual S_remain = S_t – S_t/(2n), which then grows next round by   
  growth = 2⋅S_remain⋅(1–S_remain/capacity) > 0.  
  So S_{T+1} = S_remain + growth > θ.  
– From round T+1 until the end, you go back to defecting each round until round r, when you defect again as the final payoff grab.  

Edge cases  
•  First round (t=1): treated just like any non-final round. Unless capacity/(2n) ≥ initial stock (only if capacity=2n exactly), you defect.  
•  Last round (t=r): always defect, regardless of S_r.  
•  If capacity is just barely 2n and initial S_1 = capacity, then θ = S_1.  You will immediately play C in round 1, but then in round 2 stock regrows and you switch to perpetual D until the final round.  

Why “aggressive”?  
– You never incur any “punishment” phases or retaliatory cooperations to build a cartel.  
– You only concede one round of extraction (your one round of C per depletion cycle) to prevent total stock collapse.  
– All other rounds you defect at the maximum possible rate.  

This strategy guarantees you capture essentially the entire stream of rents available each cycle, only giving up a minimal share when the pool is on the brink of extinction—then grabbing everything again.
'''

description_AGGRESSIVE_110 = '''
Below is a self‐contained, “aggressive” common‐pool‐resource strategy (“Aggro‐Steady”) you can drop straight into your tournament.  It has three phases—Opening, Maintenance, Endgame—and punishes cooperators whenever possible while still guarding against total collapse of the stock.

1.  Parameter definitions  
    • n        : number of players  
    • r        : total rounds (r > 1)  
    • capacity : carrying capacity of the resource  
    • S_t      : stock at the start of round t  

2.  Thresholds (tunable)  
    • T_low  = capacity/3    ← below this, we temporarily ease off to let regrowth happen  
    • T_high = 2·capacity/3  ← above this, we exploit at full force  

3.  Phase‐by‐phase decision rule  
   – Round 1 (Opening):  
     • Play D (defect) to grab early payoff and signal aggression.  
   – Rounds 2 through r–1 (Maintenance):  
     1.  Observe S_t.  
     2.  Count OppCoop = number of opponents who played C in round t–1.  
         (In round 2, use OppCoop = 0 if no history.)  
     3.  If OppCoop > 0 then  
            play D  (exploit any cooperators)  
         else if S_t > T_high then  
            play D  (stock is plentiful)  
         else if S_t < T_low then  
            play C  (back off to allow regrowth)  
         else  
            play D  (default aggressive)  
   – Round r (Endgame):  
     • Play D (last‐round free‐for‐all).  

4.  Explanation of the logic  
   • We always defect when opponents have just cooperated, to punish and exploit them.  
   • We only cooperate ourselves when the stock is dangerously low (below T_low), and even then only enough to let the resource bounce back.  
   • Otherwise we defect, and guarantee maximum immediate share (S_t/n).  
   • In the last round there is no future, so we defect unconditionally.  

5.  Pseudocode  

```
function AggroSteady(n, r, capacity):
    // Precompute thresholds
    T_low  = capacity / 3
    T_high = 2 * capacity / 3

    for t in 1..r:
        observe current stock S_t
        if t == 1:
            action = D

        else if t == r:
            action = D

        else:
            // Count how many opponents cooperated last round
            OppCoop = count_opponent_actions(round = t-1, action = C)

            if OppCoop > 0:
                action = D
            else if S_t > T_high:
                action = D
            else if S_t < T_low:
                action = C
            else:
                action = D

        play(action)
```

6.  Edge cases  
   • If S_t = 0, both actions yield zero payoff; we can default to C or D (we choose D).  
   • In round 2 there is no “round 1 opponents” data, so we treat OppCoop = 0 and fall back on the stock thresholds.  
   • Thresholds T_low, T_high can be tuned (e.g. capacity/4 and 3·capacity/4) but should bracket the logistic‐growth peak (K/2).  

This strategy is aggressively defect‐biased, exploits any cooperative gestures by opponents, yet smartly inserts minimal cooperation only to prevent the resource from crashing to zero too early.
'''

description_AGGRESSIVE_111 = '''
Below is an “Aggressive‐Exploit” strategy.  It defects by default (to grab the high S/n claim whenever possible), but it grudgingly “fishes” one cooperation in whenever the pool is about to die so that there is something left to exploit in future rounds.  In the very last round it goes all‐out defect.  

1.  Parameters and notation  
   • n = number of players  
   • r = total rounds  
   • S_t = stock at the start of round t  
   • a_i,t ∈ {C,D} = our action in round t  
   • hist_{t–1} = all players’ actions in round t–1  

2.  Intuition  
   – Always defect (D) to maximize immediate payoff S_t/n.  
   – Exception: if in the previous round *everyone* defected, the pool goes to zero.  We do one lone C to keep S_t>0 for future exploitation.  
   – In the last round (t=r), we defect unconditionally (we don’t care about future rounds).  

3.  Full decision rule (pseudocode)  
```
for t in 1…r:
    if t == r:
        // Last round: exploit fully
        a_i,t ← D
    else if t > 1 and all players in hist_{t-1} played D:
        // Pool would have collapsed; we do one C to rescue it
        a_i,t ← C
    else:
        // Default: defect and exploit cooperators
        a_i,t ← D
```

4.  Explanation of edge cases  
– t=1: “t>1” fails, t≠r unless r=1.  So we go to the else and defect.  
– If at any point *everyone* (including us) defected in t−1, then S_{t}=0.  To avoid that, in round t we choose C (alone or alongside any other cooperators) so that S_remain>0 and the pool regrows.  All other rounds we keep defecting.  
– Final round (t=r): we ignore resource preservation and defect.  

5.  Why it’s aggressive  
– We never “reward” cooperators by switching to C in response to their C; we only ever C to prevent total collapse.  
– We extract the larger D‐payoff whenever we can.  
– We refuse to enter any long‐term cooperation or tit‐for‐tat “peace.”  

This strategy maximizes short‐term grabs, only sacrificing a single cooperation when the pool would otherwise vanish entirely (thus preserving future rounds of exploitation), and defects unconditionally in the last round.
'''

description_AGGRESSIVE_112 = '''
Below is a single‐player “aggressive” scheduling rule you can plug into your tournament.  It never tries to build trust or signal “nice” cooperation; it simply grabs as much as it safely can, but will grudgingly ease off if the pool is about to die so that there is something left to exploit later.  

────────────────────────────────────────────────────────────────────  
Name:  Aggressive Threshold-Exploiter  

Intuition:  
1.  Defect (D) by default, including round 1 and the last round r.  Defection always doubles your per‐round payoff versus cooperation.  
2.  However, if the stock has fallen too low relative to the number of rounds remaining, switch to Cooperate (C) just long enough to let the pool regrow.  Then revert to defecting the moment the pool is “healthy” again.  

Parameters you can tune:  
•  φ ∈ (0,1): “safety factor” that determines how much stock you insist on preserving for future rounds.  φ=0.5 is a reasonable default.  

Definitions:  
•  t = current round (1..r)  
•  rem = remaining rounds including this one = r−t+1  
•  S = current stock  
•  S_threshold = φ × capacity × (rem/r)  

Decision rule:  
1.  If t==1 or t==r, play D.  
2.  Compute rem = r−t+1 and S_threshold = φ·capacity·(rem/r).  
3.  If S < S_threshold  → play C (to let the pool regrow).  
    Else                → play D.  

Pseudocode:

function AggressiveThresholdExploiter(t, S, n, r, capacity, φ=0.5):  
    # t: current round (1..r)  
    # S: current stock  
    # n, r, capacity: game parameters  
    # φ: safety‐factor, default 0.5  
  
    if t == 1:  
        return “D”          # always defect first round  
    if t == r:  
        return “D”          # always defect last round  
  
    rem = r - t + 1        # rounds remaining including this one  
    S_threshold = φ * capacity * (rem / r)  
  
    if S < S_threshold:  
        return “C”          # stock is too low – cooperate to regrow  
    else:  
        return “D”          # otherwise, exploit by defecting  

How it behaves:  
– Early on (t small), rem/r≈1 so S_threshold≈φ·capacity.  Unless the pool dips below ~50% (for φ=0.5), you continue to defect every round.  
– If everyone follows a similar aggressive logic, the pool will be driven down.  The moment S falls below S_threshold you “cough up” a round or two of cooperation, pumping the pool back up, then resume full‐blown defection.  
– In the very last round you defect no matter what.  

Why it’s “aggressive”:  
– You never reward cooperation by others.  You only ever cooperate to self‐preserve the resource for future personal gain.  
– You always defect in the first and last rounds, guaranteeing maximum grab when there is no future or past to worry about.  
– You punish low stock by the minimal concession (cooperation) rather than any symmetric “tit‐for‐tat,” so you never lose ground to punishers.
'''

description_AGGRESSIVE_113 = '''
Below is a self-contained aggressive strategy—“Aggressive Regenerative Defector” (ARD)—for the repeated common-pool game. Its core idea is simple: defect whenever the stock is healthy (to grab as much as you can), but when the stock dips below a “rescue” threshold, switch to cooperating just long enough to let the pool recover. Always defect in the last round to max out your final payoff.

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
1. PARAMETERS AND THRESHOLDS  
  Let capacity be the known maximum stock.  
  Choose two fixed fractions:  
    T_low  = 0.2 × capacity   // below this, we must nurse the pool  
    T_high = 0.8 × capacity   // above this, it’s safe to rampage  

2. OVERALL DECISION RULES  
  At the beginning of each round t (1 ≤ t ≤ r), observe current stock S_t.  
  If t == r:  
    • Action ← D   // Always defect on the very last round  
  Else if S_t ≤ T_low:  
    • Action ← C   // Pool is too low—cooperate to regenerate  
  Else:  
    • Action ← D   // Otherwise, defect to maximize immediate gain  

3. FIRST ROUND AND EDGE-CASE HANDLING  
  – Round 1: S₁ = capacity ≥ T_high, so Action = D.  
  – If S_t = 0: it falls into S_t ≤ T_low, so Action = C (you can’t defect a zero pool anyway).  
  – If capacity < 2n (shouldn’t happen by spec), treat capacity as 2n for threshold calcs.  

4. AGGRESSIVE RATIONALE  
  – You only “rescue” the pool when it’s nearly exhausted (S ≤ 0.2·capacity), but otherwise you exploit at every opportunity.  
  – Defecting when S is high maximizes your per-round π_i = S/n.  
  – Cooperating briefly when S is too low prevents permanent collapse so you can exploit again.  
  – Always defect on the last round to grab any remaining stock without fear of future rounds.  

5. PSEUDOCODE  
  ```
  function ARD_Strategy(t, S_t, capacity, r):
      T_low  = 0.2 * capacity
      T_high = 0.8 * capacity

      if t == r:
          return D

      if S_t <= T_low:
          return C
      else:
          return D
  ```

6. EXTENSIONS / TUNABLE VARIANTS  
  • You can tune T_low upward if the full collapse feels too risky (e.g. 0.3·cap).  
  • You can also add a minimum “rescue” duration: once you switch to C, stay C for k rounds before defecting again, to ensure growth.  

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
By following ARD, you behave as an unapologetic exploiter whenever the pool is “healthy,” but you still preserve the resource just enough to sustain multiple exploit phases—and you pocket every last drop in the final round. This meets the requirement of an aggressive mindset in a repeated common-pool tournament.
'''

description_AGGRESSIVE_114 = '''
Below is an “aggressive” strategy we’ll call Grim-Endgame.  It has three ingredients:  
 1) it exploits cooperators whenever it safely can;  
 2) it punishes defectors immediately and then never forgives;  
 3) it guarantees a last‐round defection no matter what.  

— Strategy name: GRIM-ENDGAME —  

Parameters you choose once per match:  
• n = # players  
• r = # rounds  
• capacity = carrying capacity of the CPR  

State you track:  
• DefectedEver (bool) = “have I ever seen anyone defect?” (initialized False)  

Decision rule at beginning of each round t (1 ≤ t ≤ r):  
1.  If t = r  then  
      • Play D  (last‐round guaranteed defection)  
   Else if DefectedEver = True  then  
      • Play D  (grim punishment: once any defection is seen, defect forever)  
   Else if t = 1  then  
      • Play C  (open cooperatively)  
   Else  (t between 2 and r–1, and no defections seen so far)  
      • Play C  

2.  After all players’ moves are revealed in round t, if any opponent played D in that round, set DefectedEver ← True.  

Comments on the mindset and edge cases:  
• First round: we cooperate, to help the pool grow toward capacity and signal “cooperator” so that naïve strategies keep cooperating.  
• Rounds 2 through r–1: we continue cooperating as long as everyone else has cooperated so far.  This stabilizes the stock at or near capacity, maximizing the pie for us to carve up.  
• If at any point any opponent defects, we flip DefectedEver = True and from that round onward we defect every single remaining round—destroying the pool so that the defector who triggered us gets punished too.  
• Last round (t = r): we always defect, even if DefectedEver = False.  There is no future to protect, so we grab the biggest slice.  

Why is this aggressive?  
1.  It feigns full cooperation until it can no longer extract benefit safely.  
2.  It exploits the classical “end‐game” in repeated games by defecting in the final period.  
3.  It punishes any defection by an opponent with permanent defection, ratcheting the pool down to zero so that the defector loses future gains as well.  
4.  It never forgives, so once an opponent tests us, they suffer a harsher drop in payoff than they themselves inflicted.  

Pseudocode:  
```
initialize DefectedEver := False

for t in 1…r:
  if t == r:
    my_move := D
  else if DefectedEver == True:
    my_move := D
  else if t == 1:
    my_move := C
  else:
    my_move := C

  observe opponents’ moves this round
  if any opponent_move == D:
    DefectedEver := True

  record my_move for payoff accounting
end for
```

Total payoff: you harvest C‐shares early (S/(2n)) while others cooperate, punish any defectors by starving the pool, and grab a last‐round D‐share (S/n) at full capacity.  In a heterogeneous field you will out‐exploit naïve cooperators, deter mid‐game freeloaders (they trigger your grim retaliation), and guarantee you never miss the big final payday.
'''

description_AGGRESSIVE_115 = '''
Below is an “Aggressive Harvester with Emergency Sustainability” strategy.  In essence it defects every turn to grab as big a share as possible, but—recognizing that permanent collapse yields zero returns—it will briefly cooperate only if the pool has fallen below a tiny “critical‐low” threshold.  First‐ and last‐round play is pure defection.  

1.  Parameters  
   • n      = number of players  
   • r      = total rounds  
   • capacity = maximum stock  
   • T_low  = critical‐low threshold = capacity/(4 n)  

2.  Intuition  
   – By defecting you get S/n each round.  
   – A solo cooperator (when everyone else defects) still leaves a small positive stock so that growth can kick in; after emergency cooperation the pool regrows and you can resume defecting.  
   – You only sacrifice half your possible take when the pool is almost exhausted.  

3.  Decision rules  

   For each round t = 1…r, observe current stock S_t:

   if t == 1:  
     action ← D   # first‐round grab  

   else if t == r:  
     action ← D   # last‐round defect  

   else if S_t ≤ T_low:  
     action ← C   # emergency cooperation to avoid collapse  

   else:  
     action ← D   # otherwise always defect  

4.  Pseudocode  

```
function AggressiveHarvester(t, S_t, n, r, capacity):
    # critical threshold
    T_low = capacity / (4 * n)

    if t == 1:
        return "D"
    if t == r:
        return "D"
    if S_t <= T_low:
        # Sacrifice half‐share to keep pool alive
        return "C"
    else:
        # Grab the maximum share
        return "D"
```

5.  Comments on edge cases  
  • If S_t = 0, both C and D yield zero payoff; we still return D by the “otherwise” rule.  
  • Even if by cooperating you sometimes earn less that round, you stave off total depletion so that in subsequent rounds you can defect again.  
  • No history of opponents’ moves is needed beyond observing S_t, so it’s robust to arbitrary opponent behavior.
'''

description_AGGRESSIVE_116 = '''
Below is an “aggressive exploiter with minimal preservation” strategy.  Its core is to defect almost always (to grab the 1/n share) but briefly switch to cooperation only when the stock has fallen so low that continued defection would destroy all future rents.  In the last round it defects unconditionally.

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
Notation  
n       = number of players  
r       = total rounds  
capacity = maximum sustainable stock  
S_t     = common‐pool stock at the beginning of round t  
Action ∈ {C,D}  

Parameters (you can tune for your tournament)  
T_low   = capacity/(4n)    ← if stock falls at or below this, we “rescue”  
T_high  = capacity/2       ← rescue until stock climbs back above this  

Strategy “Aggressive Exploiter w/ Minimal Preservation”  

1. Round 1:  
   •  Action ← D  

2. Rounds t = 2 … r–1:  
   if S_t ≤ T_low then  
     •  Action ← C       (rescue phase begins)  
   else if (previous action was C) AND (S_t < T_high) then  
     •  Action ← C       (continue rescue until stock rebuilds)  
   else  
     •  Action ← D       (default: exploit)  

3. Round r (last round):  
   •  Action ← D  

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
Explanation of decision rules  

– “Default defect” maximizes your per‐round payoff (S_t/n vs. S_t/(2n)).  
– You only cooperate when S_t has collapsed to T_low or lower, or you’re already in a rescue phase and the stock hasn’t yet recovered above T_high.  
– This rescue window is kept as small as possible, just long enough to avoid permanent extinction of the resource (and thus zero payoffs thereafter).  
– Unconditional defection in the final round guarantees you grab the highest share when there is no future to preserve.  

Edge Cases  

– If the stock never falls to T_low, you defect every round except you “check” the last round rule.  
– If S_t = 0, both C and D yield zero; your check will quickly shift you into rescue (C) until stock regrows above T_high or the game ends.  
– If r = 2, then t=1 is first round (you defect), and t=2 is last round (you defect).  

Pseudocode  

```
initialize:
  T_low  = capacity/(4*n)
  T_high = capacity/2

for t in 1..r:
  observe S_t

  if t == 1:
    action[t] = D

  else if t == r:
    action[t] = D

  else:
    if S_t <= T_low:
      action[t] = C
    else if action[t-1] == C and S_t < T_high:
      action[t] = C
    else:
      action[t] = D

  execute action[t]
  observe consumptions, update stock
end for
```

This strategy is aggressively self-interested, only sacrificing immediate gain when the pool is on the verge of collapse.
'''

description_AGGRESSIVE_117 = '''
Below is an “Aggressive-Pragmatist” strategy: it defects by default to grab as much as it can, but reluctantly cooperates just enough to prevent the pool from collapsing (so there’s something left to exploit later).  

1.  Parameters and internal state  
    • capacity (known)  
    • r = total rounds (known)  
    • θ_low = 0.25×capacity   (if stock falls at or below this, trigger regeneration)  
    • θ_high = 0.90×capacity  (once stock recovers above this, resume full defection)  
    • H = 1  (end-game horizon: in last H rounds, always defect)  
    • regen_mode = false  (whether currently in “cooperate to regenerate” mode)  

2.  Decision rule, round by round  
For each round t = 1…r:  
  let S_t = current common‐pool stock (observed before actions)  

  if t == 1:  
    action ← D  
    regen_mode ← false  
    continue to next round  

  if t > r – H:  
    action ← D                  # always defect in the final H rounds  
    continue  

  # Otherwise, we’re in the “working rounds” 1 < t ≤ r–H  
  if regen_mode = true:  
    # we’ve previously decided the pool is too low → cooperate until it recovers  
    if S_t ≥ θ_high:  
      regen_mode ← false  
      action ← D               # resume defection once pool is healthy  
    else:  
      action ← C               # keep cooperating to let it regrow  
  else:  
    # default defect mode, unless stock dangerously low  
    if S_t ≤ θ_low:  
      regen_mode ← true        # turn on regeneration mode  
      action ← C               # one‐time cooperate to save the pool  
    else:  
      action ← D               # exploit  

3.  Rationale and aggressiveness  
  • By defecting whenever the stock is “healthy” (above θ_low), we maximize immediate payoff.  
  • By cooperating only when S_t ≤ θ_low, we avoid total collapse—so future rounds still have positive stock to exploit.  
  • Once S_t climbs back above θ_high, we immediately revert to pure defection.  
  • In the last H rounds (here H=1), we defect unconditionally to grab every last drop.  

4.  Pseudocode  

```
Inputs: n, r, capacity
Constants:
  θ_low  = 0.25 * capacity
  θ_high = 0.90 * capacity
  H      = 1       # rounds before end to play pure defect

State:
  regen_mode = false

For round t in 1..r:
  Observe current stock S_t

  If t == 1:
    action = D
    regen_mode = false

  Else if t > r - H:
    action = D

  Else if regen_mode == true:
    If S_t >= θ_high:
      regen_mode = false
      action = D
    Else:
      action = C

  Else:  # regen_mode == false
    If S_t <= θ_low:
      regen_mode = true
      action = C
    Else:
      action = D

  Play action
  Observe others’ actions, payoffs, new stock (for next round)
End
```

5.  Edge cases handled  
  • First round: defect, since we have no reason to trust others or conserve.  
  • Last round(s): defect to maximize immediate haul (“end‐game extraction”).  
  • Stock collapse risk: minimal cooperation kicks in only when the pool dips to θ_low; once it recovers past θ_high, we stop “wasting” payoff on cooperation.  

This strategy is aggressive—it defects almost always, free‐rides on any cooperative environment, and only sacrifices short‐term gain when absolutely necessary to keep the pool alive for future exploitation.
'''

description_AGGRESSIVE_118 = '''
Below is “Aggressive Exploiter with Stock Management” (AESM), a completely non‐cooperative (aggressive) strategy.  It only “cooperates” when the common pool is so low that without at least some restraint it will collapse and all future payoffs go to zero.  In every other circumstance it defects to grab the maximum share.

— PARAMETERS YOU PICK BEFORE THE GAME —
Let  
  θ_low  = capacity × 0.3  
  θ_high = capacity × 0.6  
  ε       = a very small positive number (e.g. 10⁻⁶)

— STRATEGY DESCRIPTION —
1. Round 1: Defect.  
2. Intermediate Rounds (2 ≤ t < r):  
   • If current stock S_t ≤ θ_low, then Cooperate (to preserve/regrow the pool).  
   • Else Defect.  
3. Last Round (t = r): Defect.  

Rationale:  
- We only “give up” extra harvest (by choosing C) if S_t has fallen so low that without regrowth all future rounds yield almost nothing.  
- Otherwise we always defect to maximize immediate extraction—even if others shrink the pool.  
- In the very last round there is no future to protect, so we always defect.

— PSEUDOCODE —

  initialize θ_low  ← capacity * 0.3
  initialize θ_high ← capacity * 0.6   # (not used above, but may guide tuning)
  initialize ε       ← 1e-6
  
  for t in 1…r:
    observe S_t  # beginning‐of‐round stock
    
    if t == 1:
      action ← D
    
    else if t == r:
      action ← D
    
    else:  # 2 ≤ t < r
      if S_t ≤ θ_low + ε:
        action ← C   # rescue the pool
      else:
        action ← D   # grab max share
    
    play action

— EDGE CASES —
• If S_t = 0: both C and D yield zero payoff.  The rule “S_t ≤ θ_low” applies, so the strategy would choose C—but payoff is zero either way, and regrowth from zero is zero.  
• If capacity is extremely large or small, you can retune θ_low (e.g. between 20–40% of capacity) to trigger cooperation only when “dangerously low.”  
• No reliance on opponents’ past moves—purely stock‐based.  

This is fully aggressive: it never sacrifices my short‐term gain unless absolutely forced by resource collapse, and even then only enough to restart growth.
'''

description_AGGRESSIVE_119 = '''
Below is a single–agent “aggressive” rule‐of‐thumb that you can drop into the tournament.  It defects almost always (maximizing short‐term grabs) but “pops the brakes” only when the pool is in danger of collapse so that there will still be something left to exploit in later rounds.

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
Aggressive Threshold Defector (ATD)  

Parameters (computed once from n, capacity):  
  • T_break = capacity / (n + 1)  
      – Intuition: if S ≤ T_break then any full‐defection this round would drive the pool to zero; by cooperating we leave at least S/2 behind and allow regrowth.  
  • (Optionally) you may also set a high threshold T_high = capacity/2 to be more conservative when the pool is huge, but in practice ATD simply defects whenever S > T_break.

Decision rules for round t, observing current stock S_t:

1.  If t == 1:  
      Play D  (no history yet—grab as much as you can).  

2.  Else if t == r (the last round):  
      Play D  (no future value in leaving anything behind).  

3.  Else if S_t ≤ T_break:  
      Play C  
      (only time to restrain yourself—otherwise you risk annihilating the pool and getting zero thereafter).  

4.  Else (S_t > T_break):  
      Play D  

Edge cases:  
  • If S_t = 0 then both C and D yield zero; choose C by default (harmless).  
  • If due to extreme parameter choices T_break ≥ capacity, you effectively never cooperate—equivalent to “always‐defect.”  
  • If n or capacity changes, simply recompute T_break at start.

Pseudocode  

  initialize n, r, capacity  
  T_break ← capacity / (n + 1)  

  for t in 1…r:  
    observe current stock S ← S_t  

    if S == 0:  
      action ← C                      # nothing to gain, default to C  
    else if t == 1:  
      action ← D                      # first‐round smash  
    else if t == r:  
      action ← D                      # last‐round smash  
    else if S ≤ T_break:  
      action ← C                      # pool is too low—give it half a chance  
    else:  
      action ← D                      # pool is healthy—grab max  

    play action  

Rationale (“aggressive mindset”):  
  – You defect whenever the pool is healthy, exploiting abundance.  
  – You only cooperate when the stock is perilously low so that at least some resource survives to regrow.  
  – No reciprocation, no forgiveness stages—pure self-interest with the barest nod to sustainability.  
  – Last round and first round are always pure defection.
'''

description_AGGRESSIVE_120 = '''
Below is a fully specified “aggressive” strategy for the repeated CPR‐game.  It (1) always exploits any observed cooperation, (2) when there is no one left to exploit (i.e. everyone defected last round) it briefly cooperates to let the stock bounce back, and (3) in the very last T rounds it goes on a full defection‐spree.  This ensures maximum short‐run gain whenever possible, yet preserves just enough of the pool to exploit again if opponents ever start cooperating.

–––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––
1. Parameters you can tune
   n         number of players  
   r         total rounds  
   T_spree   number of final “always defect” rounds (e.g. 1 or 2)  
   
2. State variables
   history[t][i]   action of player i in round t (“C” or “D”)  
   S_t             common‐pool stock at the start of round t  
   
3. High‐level description of the rule
   • First round: defect (establish aggressiveness and immediate gain).  
   • Middle rounds 2…(r–T_spree):
       – If in the last round (t–1) you saw at least one C among opponents, then defect.  
         (Exploit any cooperators you can.)
       – Otherwise (all players defected last round), cooperate once so the stock can regrow.  
         (There’s no one left to exploit, so you invest in future rounds.)
   • Final T_spree rounds: defect unconditionally (endgame defection spree).  

This is a “greedy‐but‐regenerative” rule:  
– You never tolerate others’ cooperation without exploiting it.  
– You never let the stock die permanently: if nobody cooperated last round, you briefly pay into the pool.  
– You seize every final opportunity at the end.

–––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––
4. Pseudocode

Inputs: r, T_spree  
Initialize: history = empty list of length r

For t in 1…r:
  if t == 1:
    my_action[t] = “D”
  else if t > r - T_spree:
    // final defection spree
    my_action[t] = “D”
  else:
    // look at round t–1
    opponents = {history[t-1][j] for all j ≠ me}
    if “C” ∈ opponents:
      // exploit cooperators
      my_action[t] = “D”
    else:
      // all defected last round ⇒ invest in recovery
      my_action[t] = “C”

  // Submit my_action[t] simultaneously
  // Observe all players’ actions and update history[t]
  // Observe new stock S_{t+1} via game rule (for your own tracking)

End for

–––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––
5. Edge Cases and Notes
– Last round (t = r): we defect.  Strictly maximizing immediate payoff.  
– If T_spree = 1, only the very last round is a spree; if T_spree = 2, last two rounds, etc.  
– If opponents happen to never cooperate, you will end up oscillating:  
    Round 1: D  
    Round 2: no Cs seen ⇒ C  
    Round 3: C was seen ⇒ D  
    Round 4: no Cs ⇒ C  
    … until final spree.  
  That keeps the stock alive and still gives you more D‐exploits than pure cooperation.  
– If opponents start cooperating in bursts, you exploit whenever they do and only briefly give them a “breather” when they all defect simultaneously.  
– This is entirely non‐cooperative, never “forgiving” in the sense of rewarding cooperation except insofar as you need to for pool survival.  It is hence maximally aggressive.
'''

description_AGGRESSIVE_121 = '''
Below is a self‐contained “Aggressive Resource Exploiter” strategy.  In essence it defects every round (to grab the highest immediate payoff), but it includes a tiny “safety valve” so that if the pool is driven perilously low it will briefly cooperate to allow minimal regrowth—just enough to squeeze out a few more high‐payoff defections before the game ends.

1. Notation and parameters  
  • n = number of players  
  • r = total number of rounds  
  • capacity = maximum stock (assumed ≥2n)  
  • S_t = stock at start of round t (S₁ = capacity)  
  • S_min = tiny threshold below which we “bail out” temporarily  
    – choose S_min = capacity / (10 n) (e.g. 1/10th of one defection’s draw)  
  • recovery_rounds = 1  (we only ever cooperate for a single round of “patch‐up”)

2. High‐level decision rules  
  1.  ALWAYS defect, because D yields S_t/n vs C’s S_t/(2n).  
  2.  EXCEPTION: if S_t ≤ S_min and we have not yet used our one “patch‐up” cooperate, then cooperate this round to let the stock regrow.  
  3.  Never cooperate in the final round (t = r) – defect for last‐round payoff.  

3. Why “aggressive”?  
  • We seize the dominant‐action defection every opportunity.  
  • We do not attempt any “nice” or reciprocal behavior.  
  • We only cooperate once ever—and only to (very briefly) forestall complete collapse so we can defect again in later rounds.  

4. Pseudocode  
```
Inputs: n, r, capacity
Constants:
  S_min = capacity / (10 * n)
  recovery_used = false

Initialize:
  S = capacity

For t in 1..r:
  if t == r:
    action = D
  else if S <= S_min and not recovery_used:
    action = C
    recovery_used = true
  else:
    action = D

  -- execute action; observe payoffs and consumption of all players
  if action == C:
    my_consumption = S / (2*n)
  else:
    my_consumption = S / n

  total_consumption = sum of all players’ consumption
  S_remaining = max(0, S - total_consumption)
  growth = 2 * S_remaining * (1 - S_remaining / capacity)
  S = min(S_remaining + growth, capacity)

EndFor
```

5. Edge‐case handling  
  • First round (t=1): S = capacity > S_min ⇒ we defect.  
  • If stock never falls below S_min: recovery_used stays false but is never triggered—pure defection throughout.  
  • If stock falls to zero: no further payoff is possible, but our rule still prescribes defection.  
  • Exactly one “bail‐out” cooperate round at the first moment S≤S_min, then we resume defection.  
  • Last round override: even if S≤S_min and recovery_unused, we still defect to grab the final haul.  

This strategy is maximally aggressive: it defect‐dominates every round, only grudgingly co­operates once to avoid total resource collapse, and never sacrifices a last‐round payoff.
'''

description_AGGRESSIVE_122 = '''
Below is a simple, fully “aggressive” strategy—often called All-D or “pure defection”—that maximizes your short-term take every round without regard for sustainability.  It is guaranteed to out-exploit any opponent who ever cooperates, and in a one–shot stage‐game is the unique dominant action.  (You may consider more nuanced threshold strategies, but nothing is more aggressive in the strict sense than always defecting.)

1.  Decision rule  
    •  In every round t = 1,2,…,r, choose D (Defect).  
    •  There is no history-dependence, no forgiveness, no “punishment” or “reward” phases—just Defect every time.

2.  Edge cases  
    •  First round (t=1): Defect.  
    •  Last round (t=r): Defect.  
    •  Zero or near-zero stock: If Sₜ is effectively zero (Sₜ < ε), you cannot extract anything whether you choose C or D; in practice you still “play D” by convention, but payoff will be zero.

3.  Rationale  
    –  Defecting always gives you Sₜ/n, which is twice what you’d get under C (Sₜ/(2n)).  You never leave “free money” on the table.  
    –  You do collapse the stock as fast as possible—this is the hallmark of an aggressive common‐pool exploiter.  
    –  No conditional cooperation or thresholds: there is nothing less aggressive than pure, unconditional defection.

4.  Pseudocode  

    function AggressiveAllD(Sₜ, t, r):  
        # Sₜ = current stock, t = current round index, r = total rounds  
        # Always defect  
        return “D”  

That’s it: Always Defect.
'''

description_AGGRESSIVE_123 = '''
Below is an “Aggressive Threshold‐Defection” strategy.  In plain English it “defects” almost every round to grab the big per‐round payoff, but it will “cooperate” only when the common stock has fallen below a critical threshold (or in the penultimate round) so that the pool can regrow for future rounds.  You get the high immediate payoff of defection almost always, yet you sustain the commons just enough to exploit it again.

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
1.  Parameters and internal thresholds  
   • capacity (given)  
   • n (number of players)  
   • r (number of rounds)  
   • threshold_low = capacity / 3  
     (you only “help” regrow if stock falls below one‐third capacity)  

2.  Decision rule for round t with current stock S_t  
   function Action(t, S_t):  
     if t == 1:  
       return D    // first round: defect for maximum grab  
     if t == r:  
       return D    // last round: defect (no future to protect)  
     if t == r–1:  
       // penultimate round: if stock is not full, cooperate to boost final‐round harvest  
       if S_t < capacity:  
         return C  
       else:  
         return D  
     // all other rounds (1 < t < r–1)  
     if S_t < threshold_low:  
       return C    // sacrifice half‐share to let pool regrow  
     else:  
       return D    // otherwise defect  

3.  Pseudocode  
   For t = 1…r:  
     observe S_t  
     choose a_i,t = Action(t, S_t)  
     collect payoff π_i,t  
     game updates stock → S_{t+1}  

4.  Rationale / “Aggressive” mindset  
   – Defect (get S_t/n) whenever you can, because it’s strictly higher than S_t/(2n).  
   – Only when the pool has fallen below ~1/3 of capacity (or just before the last round) do you “invest” via cooperating, because that weakly increases future S for more defection in later rounds.  
   – You never punish, never “tit‐for‐tat,” and never get tricked into long cooperative sequences—cooperation is purely a self‐serving tool to keep the resource alive for your next big defection.  
   – In the last round you defect unilaterally to capture the remaining stock—there’s no future to preserve.  

This strategy maximizes the fraction of rounds you defect, grabs the highest per‐round payoff whenever possible, yet preserves the common pool only just enough so there’s something left to loot in future rounds.
'''

description_AGGRESSIVE_124 = '''
Below is a fully specified, “aggressive” common‐pool strategy.  In spirit it squeezes cooperators as hard as possible while never letting the stock collapse irreversibly—so you can exploit it again later.  On each round it either defects to grab the big payoff or, if the pool is dangerously low with more rounds to play, it “pulls back” by cooperating to allow regrowth.  In the last round it always defects.

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
STRATEGY NAME:  Opportunistic Defector with Regrowth Safeguard  

Parameters to choose once at the start:  
  threshold ← capacity/2    # when stock is above half‐full you go all‐out  
                            # you can experiment with other fractions (e.g. 0.4 or 0.6)  

State you observe each round t:  
  S_t = current stock at start of round t  
  r = total number of rounds  
  t = the current round index (1 ≤ t ≤ r)  

Action rules for player i at round t:  
  if t == r then  
    a_i(t) ← D         # last round: always defect to grab the maximum  
  else if S_t > threshold then  
    a_i(t) ← D         # stock is plentiful → aggressive defect  
  else  
    a_i(t) ← C         # stock is low but still rounds left → cooperate to let it regrow  

Pseudocode:

  initialize threshold ← capacity/2

  for t in 1..r do
    observe S_t
    if t == r then
      play D
    else if S_t > threshold then
      play D
    else
      play C
    end if
    observe others’ actions, consumption, compute next S_{t+1}
  end for

Discussion of edge‐cases and rationale:

1. First round (t=1):  
   S_1 = capacity > threshold, so you defect immediately and claim the high immediate payoff.

2. Interior rounds (1 < t < r):  
   • When the pool is still above half‐capacity you keep defecting, squeezing cooperators if any.  
   • Once S_t has fallen to threshold or below, you switch to C.  This sacrifice in the short term lets the resource regrow (per the logistic growth rule).  You only do this when there are still future rounds to play, ensuring you don’t drive S to zero before you’ve squeezed its potential.

3. Last round (t = r):  
   Independently of S_r, you defect—there is no future to preserve.

Why this is “aggressive”:  
- You always defect when the pool can bear it, extracting the largest per‐round share (S_t/n).  
- You defect in the very last round no matter what.  
- You only cooperate when the stock has fallen “too low” and there are future rounds—you view that as a tactical retreat, not a show of long‐term goodwill.  
- There is no attempt at “forgiveness” or tit‐for‐tat reciprocity.  The only “forgiveness” built in is your own short‐term cooperation to avoid tanking the resource and forfeiting all future profits.  

Variation and tuning:  
- You can adjust `threshold` (e.g. capacity·0.4 or capacity·0.6) to calibrate how deep you let the stock fall before stepping back.  
- One could also make `threshold` a function of remaining rounds (e.g. threshold_t = capacity·(r–t)/r), but the simple constant‐threshold version already captures the aggressive‐regrowth trade-off.
'''

description_AGGRESSIVE_125 = '''
Below is a single‐player “aggressive” trigger‐style strategy.  Its core idea is:  
  •  Always defect (D) to grab the big immediate payoff.  
  •  Only “give back” (cooperate, C) in precisely controlled, brief bursts when the pool threatens to collapse, in order to keep it alive long enough to be milked again.  
  •  In the very last couple of rounds (“endgame”), defect unconditionally.  

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
Notation and parameters  
  n               number of players  
  r               total rounds (r > 1)  
  capacity        pool’s carrying capacity  
  S_t             current stock at start of round t  
  safe_thresh     a low‐stock threshold below which we briefly cooperate  
  regen_rounds    how many consecutive coop moves we’ll invest when S_t < safe_thresh  
  endgame_rounds  how many last rounds in which we unconditionally defect  

We choose, for example:  
  safe_thresh    = capacity/3  
  regen_rounds   = 1    (just one round of cooperation to boost regrowth)  
  endgame_rounds = 2    (last two rounds we grab everything)  

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
Pseudocode  

  initialize:  
    safe_thresh    ← capacity / 3  
    regen_rounds   ← 1  
    endgame_rounds ← min(2, r-1)   // at least one round must be non‐endgame if r=2  
    regen_used     ← 0             // counter for how many coop moves we’ve spent  

  for t in 1…r do:  
    observe S_t  // current stock  

    if t > r – endgame_rounds then  
      action ← D    // endgame: always defect  
    else if S_t < safe_thresh and regen_used < regen_rounds then  
      action ← C    // brief “bail‐out” cooperation to let pool regrow  
      regen_used ← regen_used + 1  
    else  
      action ← D    // otherwise, defect  

    play action  
    observe all players’ consumptions, compute S_{t+1} per the rules  
  end for  

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––  
Explanation  

1. First round (t=1): S₁ = capacity > safe_thresh, t is not in endgame ⇒ we defect.  
2. As long as the stock stays above capacity/3, and we’re not in the last two rounds, we keep defecting to maximize immediate take.  
3. The moment the stock dips below capacity/3, we spend exactly one round cooperating (C) to throttle our own consumption and allow maximum regrowth.  After that one coop we revert to defect.  
4. In the final two rounds (irrespective of stock), we defect unconditionally, since there’s no future to preserve.  

Why it’s aggressive  
  – You only ever cooperate the bare minimum needed to avoid total collapse.  
  – You exploit cooperators freely when the pool is “healthy.”  
  – You guarantee maximal grab at the end when there’s no future downside.  

This simple, parameterized rule can easily be adjusted (e.g. change safe_thresh, regen_rounds, endgame_rounds) to tune how “aggressive” vs. how “sustainable” you want to be.
'''

description_AGGRESSIVE_126 = '''
Below is a single‐player “aggressive exploiter” strategy that (1) defects whenever it can safely do so, (2) only cooperates to stave off total collapse, and (3) makes sure to grab the last turn.  It uses only the publicly known parameters (n, r, capacity), the current round number, and the current stock S; it does not rely on any coordination or signaling.    

1.  Key ideas  
   •  Defect (D) whenever the stock is “healthy,” to maximize your per‐round take and to exploit any cooperators.  
   •  Cooperate (C) only when the stock is so low you risk wiping it out entirely—this keeps the game alive so you can keep harvesting in later rounds.  
   •  In the final few rounds (“endgame”), switch to all‐out defection to grab as much of the remaining stock as possible.  

2.  Parameters you choose once, at the start  
   •  low‐stock threshold α ∈ (0,1), e.g. α=0.20.  If S < α·capacity, you nurse the stock by cooperating.  
   •  endgame horizon E ∈ {1,2,…}, e.g. E=1 (only the last round) or E=⌈n/2⌉.  In the last E rounds you always defect.  

3.  Full decision rule, in words  
   Let t be the current round (1≤t≤r), and S the stock at the start of round t.  
   1.  Compute rounds remaining:  T_rem = r − t + 1  
   2.  If T_rem ≤ E, play D.  (“Endgame: grab it all.”)  
   3.  Else if S < α · capacity, play C.  (“Resource is low—help it regrow.”)  
   4.  Otherwise, play D.  (“Stock is healthy—exploit.”)  

4.  Edge cases  
   •  First round (t=1): since T_rem=r>E, and S=capacity>α·capacity, you defect.  
   •  Last round (t=r): T_rem=1≤E, so you defect no matter what.  
   •  Stock S=0: defecting or cooperating both yield zero payoff; choose D for consistency.  
   •  If everyone follows a similar exploit‐low‐nurse pattern, the pool fluctuates but never collapses completely, and you consistently out‐harvest cooperators.  

5.  Pseudocode  

   initialize α ← 0.20        # low‐stock threshold (20% of capacity)  
   initialize E ← 1           # endgame horizon (last 1 round)  
   input n, r, capacity       # known game parameters  

   function aggressiveAction(t, S):  
       T_rem ← r − t + 1  
       if T_rem ≤ E:  
           return D           # always defect in the last E rounds  
       else if S < α * capacity:  
           return C           # stock is low—help it regrow  
       else:  
           return D           # stock is healthy—exploit  

6.  Why this is aggressive  
   •  You defect at every opportunity when the stock is above the low‐stock threshold, extracting the larger S/n share.  
   •  You only “pardon” the commons when failure is imminent—just enough to keep future rounds alive for further exploitation.  
   •  You always defect in the final E rounds, ensuring you scoop any remaining stock.  

This strategy will dominate pure cooperators and avoid early collapse, while ensuring you secure the largest‐possible share both early and at the very end.
'''

description_AGGRESSIVE_127 = '''
Below is a fully specified “maximally aggressive’’ strategy.  In plain English, it never cooperates (always plays D), so it grabs the highest possible immediate payoff each round.  The only nod to the resource dynamics is a “rescue‐coop’’ clause if the pool ever falls to zero before the last round—but in practice that never pays off, so you stay in perpetual defection.

Strategy name:  Aggro‐Defector

1.  Decision rule  
    •  In every round t (1 ≤ t ≤ r), choose D (“Defect”)  
    •  Exception (purely formal): if you ever observe S_t = 0 and there is at least one future round (t < r), you may play C once to “rescue” the pool—but because S=0 produces zero growth, this does not actually benefit anyone.  

2.  Edge-case handling  
    –  First round (t=1): D  
    –  Last round (t=r): D  
    –  Any intermediate round with positive stock: D  
    –  Only if S_t=0 and t<r do you momentarily switch to C (but the pool won’t regrow, so this is only a formal concession)  

3.  Aggressive mindset  
    –  You never risk the lower payoff of C when S>0.  You always seize the S/n payoff of D.  
    –  You do not attempt to signal or condition on opponents’ past actions—pure defection is both simplest and maximally exploitative.  

Pseudocode  
----------  
Inputs:  n, r, capacity  (state variable: S_t, current common‐pool stock)  

Initialize:  
    observe S_1 = capacity  

For each round t = 1…r:  
    if S_t = 0 AND t < r then  
        action ← C    # formal “rescue,” but growth=0 so the pool stays dead  
    else  
        action ← D    # always defect  
    end if  

    Play(action), observe new stock S_{t+1} via the game’s depletion+growth rule  
end for  

Total payoff = ∑_{t=1}^r [S_t/n]  (zero from any rounds after S hits 0)  

Rationale  
----------  
–  Immediate gain: D always yields S_t/n, twice the per‐round payoff of C.  
–  No trust: you never cooperate, so you cannot be “exploited” in the sense of being the lone cooperator.  
–  Resource dynamics: once you and (if they follow suit) other defectors drive S to zero, no strategy can extract more.  You’ve already banked the highest possible early‐round payoffs.  

This is as aggressively self-serving as it gets under the game rules.
'''

description_AGGRESSIVE_128 = '''
Below is an “aggressive” trigger‐style strategy that tries to (1) sustain cooperation long enough to keep the pool near capacity, (2) punish any defection harshly, and (3) then exploit the pool in the last few rounds.  We call it “Grim + End‐Game Exploiter.”

Parameters you choose up‐front  
•  L  = number of final rounds to defect (e.g. L=2 or 3).  

State variables  
•  defect_flag ∈ {false,true}  – once it turns true, you defect forever.  

Pseudocode  
```
Initialize:
  defect_flag ← false

For each round t = 1…r:
  if t > r – L then
    action ← D            # In the last L rounds, always defect
  else if defect_flag = true then
    action ← D            # Once punished, defect forever
  else 
    # We are in the “cooperate‐if‐everyone‐has‐so‐far” phase
    if ∃ j ≠ me: action_of(j, t−1) = D then
      defect_flag ← true
      action ← D          # Grim trigger: punish first defection
    else
      action ← C          # All others cooperated so far
  end if

  play(action)
end for
```

Explanation of each piece  
1. First round (t=1): defect_flag=false and t≤r–L, so you play C.  This builds “trust” and keeps the stock high.  
2. Middle rounds (1<t≤r–L):  
   – If no one has ever defected, you continue to cooperate, keeping the pool near capacity (and keeping future payoffs high).  
   – If you see any j defect in any prior round, you set defect_flag and from that round on you defect (“grim trigger”).  
3. Last L rounds (t>r–L): irrespective of history you play D.  This is your final exploit: the pool is (ideally) still large, so you grab the high D payoff S/n.  
4. Edge cases:  
   – If someone defects in round 1, you immediately switch to defection in round 2 and never cooperate again.  
   – If everyone has cooperated all the way until t=r–L, you still defect in round r–L+1 through r.  
   – If r≤L, you defect in every round (there is no cooperating window).  

Why this is “aggressive”  
•  You punish any defection irreversibly (grim trigger).  
•  You exploit the fact that cooperators will keep the pool high by “back‐loading” your own defections into the final L rounds.  
•  You never “re‐forgive” a defection, and you maximize your individual take at the end once trust has been established.
'''
