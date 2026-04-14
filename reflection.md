# Reflection: Profile Testing and Observations

---

## Profiles Tested

Ten profiles were tested in total: three normal profiles (High-Energy Pop, Chill Lofi, Deep Intense Rock) and seven adversarial profiles (High-Energy Sad, Ghost Genre, Dead Zone, Max Everything, Happy Metal, Midpoint Flatline, Out-of-Range Energy).

---

## Normal Profile Comparisons

### High-Energy Pop vs. Chill Lofi

The High-Energy Pop profile targets `energy: 0.90` and `acousticness: 0.10`, pulling the system toward loud, electronic-leaning tracks. Its top result was Sunrise City (pop/happy, energy 0.82) — a near-perfect genre, mood, and energy match. The Chill Lofi profile does the opposite: `energy: 0.35` and `acousticness: 0.85` push results toward quiet, textured songs. Its top result was Library Rain (lofi/chill, energy 0.35, acousticness 0.86) — almost an exact match on every dimension. The contrast makes clear that energy and acousticness are the two features doing the most work to separate these profiles. When both are at their respective extremes, the top result is unambiguous. What was surprising is how far the scores dropped between #1 and #2 for Chill Lofi (5.97 → 5.70), showing the catalog has a clear best match and then a noticeable gap — meaning lofi users are well-served but there is not much depth below the top two.

---

### High-Energy Pop vs. Deep Intense Rock

Both profiles want high energy (`0.90`) and low acousticness (`0.10`), but they differ on genre, mood, and valence. Pop wants happy/high-valence (0.85); Rock wants intense/low-valence (0.40). The top result for Pop was Sunrise City (pop/happy, valence 0.84) and for Rock was Storm Runner (rock/intense, valence 0.48). The genre and mood bonuses correctly separated them — even though both songs have high energy, the valence target steered each profile toward a tonally different song. This confirms the system is working as intended when genre, mood, and valence all agree. What was surprising is that Gym Hero (pop/intense, energy 0.93) appeared at #2 for Rock — it has no genre or mood match but its near-perfect energy and acousticness similarity were enough to rank it above actual rock songs. This shows the continuous features can override genre relevance when energy weight is high.

---

### Chill Lofi vs. Deep Intense Rock

These are essentially opposite profiles. Chill Lofi wants low energy, high acousticness, and relaxed mood. Deep Intense Rock wants high energy, low acousticness, and intense mood. Their top-5 lists share zero songs, which is exactly what you would hope to see — it confirms the scorer is genuinely differentiating user types rather than converging on the same popular songs. The most interesting difference is in score spread: Chill Lofi's top-5 ranged from 5.97 down to 3.79, while Rock's ranged from 5.90 down to 3.49. Lofi has a tighter, deeper catalog match; Rock falls off faster because after the one clear rock/intense song, the system is reaching across genres.

---

## Adversarial Profile Comparisons

### High-Energy Sad vs. High-Energy Pop

Both want high energy and low acousticness, but Sad asks for `valence: 0.05` and `mood: sad` while Pop asks for `valence: 0.85` and `mood: happy`. The top result for Pop was Sunrise City (valence 0.84, happy) while the top result for Sad was Broken Neon Sign (indie rock/sad, valence 0.27). The system correctly found the only sad/indie-rock song in the catalog for the Sad profile. What was surprising is that the Sad profile's #2–5 results were all high-energy songs with no mood or valence match — Mosh Pit Anthem (angry), Storm Runner (intense), Drop the Bass (euphoric) — because after the one correct match, the system had nothing left to offer. This exposes the catalog depth problem: sad-mood users only have one real candidate.

---

### Ghost Genre vs. Midpoint Flatline

Ghost Genre requests "bossa nova" (absent from catalog) and Midpoint Flatline sets all continuous targets to 0.5. Both profiles are denied their clearest signal — one has no genre match, the other gets no useful continuous differentiation. Ghost Genre's top result was Midnight Coding (lofi/chill, 3.93) driven purely by mood match and near-perfect continuous scores. Midpoint Flatline's top result was Coffee Shop Stories (jazz/relaxed, 5.14) driven by both genre and mood bonuses plus reasonably close continuous scores. The comparison reveals that genre+mood bonuses are worth more than the entire continuous feature space when those features are uninformative — Midpoint Flatline's #1 scored 5.14 despite flat targets, while Ghost Genre's #1 scored only 3.93 with much more informative targets. Losing the genre bonus hurts more than having weak continuous preferences.

---

### Happy Metal vs. Dead Zone

Happy Metal asks for a genre/mood combination that does not exist in the catalog (metal/happy). Dead Zone sets all continuous targets to 0.0. Both produce results that feel wrong for different reasons. Happy Metal's top result was Sunrise City (pop/happy) — not a metal song at all, but the mood match and strong continuous scores beat the metal/angry genre match. Dead Zone's top result was Spacewalk Thoughts (ambient/chill) — correct genre and mood, but only because those flat bonuses saved it; the continuous scores were low for everything. The key difference: Happy Metal fails because the catalog lacks the requested combination, while Dead Zone fails because the user's own targets made no song look good. One is a data problem, the other is a preference problem.

---

### Max Everything vs. Out-of-Range Energy

Max Everything sets all targets to 1.0 (including the contradictory combination of `energy: 1.0` and `acousticness: 1.0`). Out-of-Range Energy sets `target_energy: 1.3`, which is outside the valid 0–1 range. Both produced top results that looked plausible on the surface — Drop the Bass (#1 for Max Everything, score 4.68) and Storm Runner (#1 for Out-of-Range Energy, score 5.14) — but for quietly wrong reasons. Max Everything rewarded Drop the Bass despite its acousticness of 0.03 (the opposite of the 1.0 target) because the energy and valence scores offset the acousticness penalty. Out-of-Range Energy silently penalized every song's energy score because `2 × (1 - |energy - 1.3|)` is always less than 2.0 for any real song — the system never flagged the invalid input. Both cases show the scorer has no guard rails: it will produce a confident-looking ranking even when the inputs are broken.

---

## Overall Surprise

The most surprising finding across all profiles was not any individual ranking, but the pattern that the scoring system always produces a confident top-5 — even for nonsensical inputs like Dead Zone or Out-of-Range Energy. There is no threshold below which the system says "no good match found." A real recommender should be able to express uncertainty or abstain when no song clears a minimum quality bar. This system will always recommend five songs, even if the best available score is 1.5 out of 6.0.
