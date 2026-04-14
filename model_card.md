# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

Give your model a short, descriptive name.  
Example: **VibeFinder 1.0**  

---

## 2. Intended Use  

Describe what your recommender is designed to do and who it is for. 

Prompts:  

- What kind of recommendations does it generate  
- What assumptions does it make about the user  
- Is this for real users or classroom exploration  

---

## 3. How the Model Works  

Explain your scoring approach in simple language.  

Prompts:  

- What features of each song are used (genre, energy, mood, etc.)  
- What user preferences are considered  
- How does the model turn those into a score  
- What changes did you make from the starter logic  

Avoid code here. Pretend you are explaining the idea to a friend who does not program.

---

## 4. Data  

Describe the dataset the model uses.  

Prompts:  

- How many songs are in the catalog  
- What genres or moods are represented  
- Did you add or remove data  
- Are there parts of musical taste missing in the dataset  

---

## 5. Strengths  

Where does your system seem to work well  

Prompts:  

- User types for which it gives reasonable results  
- Any patterns you think your scoring captures correctly  
- Cases where the recommendations matched your intuition  

---

## 6. Limitations and Bias 

Where the system struggles or behaves unfairly. 

Prompts:  

- Features it does not consider  
- Genres or moods that are underrepresented  
- Cases where the system overfits to one preference  
- Ways the scoring might unintentionally favor some users  

When the energy weight was doubled and the genre weight was halved, the system began over-prioritizing high-energy songs for almost every profile, even when the user's stated genre and mood pointed in a completely different direction. For example, the "Happy Metal" profile — which asked for metal and happy mood — previously surfaced the wrong song for the wrong reason (genre bonus dominating), but after the change it surfaced the wrong song for a different wrong reason (energy score dominating). This revealed that the scoring logic simply moves the bias from one feature to another depending on which weight is largest, rather than finding a genuinely better match. The system also treats the energy gap as symmetric — being 0.3 too loud gets the same penalty as being 0.3 too quiet — which means calm-music users are unfairly penalized by the doubled weight because most songs in the catalog skew toward higher energy. In short, no single fixed weight produces accurate results for all user types; the bias just shifts shape.

---

## 7. Evaluation  

How you checked whether the recommender behaved as expected. 

Prompts:  

- Which user profiles you tested  
- What you looked for in the recommendations  
- What surprised you  
- Any simple tests or comparisons you ran  

No need for numeric metrics unless you created some.

The system was evaluated across three normal profiles (High-Energy Pop, Chill Lofi, Deep Intense Rock) and seven adversarial profiles designed to expose specific weaknesses. For the normal profiles, the top result was always the most intuitive match — for example, "Library Rain" correctly topped the Chill Lofi rankings because it matched genre, mood, and all three continuous features closely. The adversarial profiles revealed more interesting behavior: the Ghost Genre profile (requesting "bossa nova," which does not exist in the catalog) showed that the system still produces reasonable-sounding results by falling back on mood and continuous features, but the scores compress into a narrow range with no clear winner. The most surprising result came from the Happy Metal profile — before the weight shift, the metal/angry song ranked #1 simply because the +2.0 genre bonus outweighed everything else, even though the mood was completely wrong. After doubling the energy weight and halving genre, a pop/happy song correctly took the top spot because energy and mood together outscored the genre match alone. A weight-shift experiment (genre halved to +1.0, energy doubled to 0–2.0) was also run across all profiles to compare rankings before and after; the top result changed in only one of the three normal profiles but changed in four of the seven adversarial profiles, confirming that edge cases are more sensitive to weight choices than typical users.

---

## 8. Future Work  

Ideas for how you would improve the model next.  

Prompts:  

- Additional features or preferences  
- Better ways to explain recommendations  
- Improving diversity among the top results  
- Handling more complex user tastes  

---

## 9. Personal Reflection  

A few sentences about your experience.  

Prompts:  

- What you learned about recommender systems  
- Something unexpected or interesting you discovered  
- How this changed the way you think about music recommendation apps  
