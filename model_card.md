# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name

**SoundMatch 1.0**

---

## 2. Intended Use

This system recommends songs from a small catalog based on a user's taste profile. It is built for classroom exploration, not real users. It assumes the user can describe their preferences upfront — favorite genre, favorite mood, and target levels for energy, acousticness, and valence. It does not learn from behavior or update over time.

---

## 3. How the Model Works

Each song gets a score out of 6.0. The score is built from five checks:

- Does the song's genre match what the user likes? (+1.0 if yes)
- Does the song's mood match what the user likes? (+1.0 if yes)
- How close is the song's energy to the user's target? (0–2.0)
- How close is the song's acousticness to the user's target? (0–1.0)
- How close is the song's valence to the user's target? (0–1.0)

"Close" means the smaller the gap, the higher the score. The top 5 songs by score are returned as recommendations. One change was made from the starter: genre was reduced from +2.0 to +1.0, and energy was doubled from 0–1.0 to 0–2.0, to test whether energy could be a stronger signal than genre label alone.

---

## 4. Data

The catalog has 20 songs. Each song has a genre, mood, energy, tempo, valence, danceability, acousticness, and more. The genres include pop, lofi, rock, jazz, edm, metal, hip-hop, ambient, indie rock, indie pop, r&b, soul, classical, country, folk, latin, and synthwave. Moods include happy, chill, intense, sad, angry, relaxed, focused, melancholic, romantic, confident, euphoric, energetic, nostalgic, peaceful, and moody. No songs were added or removed. The dataset skews toward English-language Western genres and does not include K-pop, Afrobeats, reggae, or other global styles.

---

## 5. Strengths

The system works well when the user's preferences are clear and the catalog has a strong match. The Chill Lofi profile returned Library Rain as #1 with a near-perfect score — correct genre, mood, energy, and acousticness all lined up. The High-Energy Pop and Deep Intense Rock profiles also returned the most obvious match at #1 every time. The scoring is fully transparent: every recommendation comes with a breakdown showing exactly which features contributed and by how much. That makes it easy to understand why a song was picked, which is something most real recommenders cannot do.

---

## 6. Limitations and Bias

When the energy weight was doubled and the genre weight was halved, the system began over-prioritizing high-energy songs for almost every profile, even when the user's stated genre and mood pointed somewhere else. For example, the Happy Metal profile — asking for metal and happy mood — surfaced the wrong song before the change (genre bonus too strong) and a different wrong song after (energy score too strong). The bias just moved from one feature to another. The system also treats energy gaps as equal in both directions — being too loud gets the same penalty as being too quiet — which unfairly hurts users who want calm music since most songs in the catalog lean high-energy. Genre and mood use exact string matching, so a song tagged "indie pop" scores zero for a user who likes "pop," even though the fit is close. Rare genres like classical and folk only have one song each, so those users always get off-genre results filling out their top 5.

---

## 7. Evaluation

Ten profiles were tested: three normal and seven adversarial. For normal profiles, the top result always matched intuition — the right song came first. The adversarial profiles were more revealing. The Ghost Genre profile (bossa nova, not in catalog) still returned results but with compressed scores and no clear winner. The Dead Zone profile (all targets at 0.0) penalized almost every song equally, making the genre and mood bonuses the only thing separating results. The most surprising finding was that the system always returns a confident top 5 — even when the best available score is under 2.0 out of 6.0. There is no minimum quality threshold. A weight-shift experiment showed that edge-case profiles are far more sensitive to weight changes than normal profiles: the top result changed in 4 of 7 adversarial profiles but only 1 of 3 normal ones.

---

## 8. Future Work

- Let users set their own weights instead of using fixed ones.
- Add partial credit for genre matching — "indie pop" should score something for a pop user.
- Add a minimum score threshold so the system can say "no good match" instead of always returning 5 songs.
- Include more songs per genre so rare-genre users get better depth in their results.
- Track which songs get skipped or replayed and adjust the profile over time.

---

## 9. Personal Reflection

**Biggest learning moment**

The biggest learning moment was the weight-shift experiment. I expected doubling energy and halving genre to make the Happy Metal profile work better — and it did. But it broke other profiles in the process. That was the moment I understood that there is no "correct" set of weights. Every weight choice helps some users and hurts others. Real recommenders solve this by learning weights from behavior instead of guessing at them upfront.

**How AI tools helped, and when I had to double-check**

AI tools helped me think through edge cases I would not have tested on my own — profiles like Dead Zone (all targets at 0.0) and Out-of-Range Energy exposed bugs I had not considered. The adversarial profile suggestions were useful starting points, but I still had to run the code and read the actual output to know whether the results were genuinely wrong or just unexpected. The AI described what *should* happen; running the program showed what *actually* happened. Those two things were not always the same.

**What surprised me about simple algorithms "feeling" like recommendations**

The scoring logic is five arithmetic operations. There is no machine learning, no training data, no embeddings. But when you run it on a Chill Lofi profile and it returns Library Rain at the top with a near-perfect score, it genuinely feels right. The surprise was that "feeling like a recommendation" mostly just means the top result matches your expectation — and a simple scoring formula can do that most of the time for clear-cut users. It only breaks down at the edges, which is exactly where real-world users tend to live.

**What I would try next**

- Add a confidence label to each result — if the top score is under 3.0, show "weak match" instead of presenting it like a strong recommendation.
- Replace exact genre/mood matching with a similarity table so "indie pop" gets partial credit for a pop user.
- Add a second user profile and try averaging their preferences to see if the system can recommend for two people at once.
- Expand the catalog to 100+ songs and see how much the rankings change when there are more candidates competing.
