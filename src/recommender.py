import csv
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    target_acousticness: float
    target_valence: float

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        # TODO: Implement recommendation logic
        return self.songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        # TODO: Implement explanation logic
        return "Explanation placeholder"

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """
    Score a single song against a user profile dict.

    Algorithm Recipe (max 6.0 points):
      +1.0  genre match        — exact string match (EXPERIMENT: halved from 2.0)
      +1.0  mood match         — exact string match
      0–2.0 energy similarity  — 2 * (1 - |song.energy - target_energy|) (EXPERIMENT: doubled from 0–1.0)
      0–1.0 acousticness sim.  — 1 - |song.acousticness - target_acousticness|
      0–1.0 valence similarity — 1 - |song.valence - target_valence|

    Returns (score, explanation) where explanation is a human-readable
    summary of which features contributed.
    """
    score = 0.0
    reasons = []

    if song["genre"] == user_prefs["favorite_genre"]:
        score += 1.0  # EXPERIMENT: halved from 2.0
        reasons.append("genre match (+1.0)")

    if song["mood"] == user_prefs["favorite_mood"]:
        score += 1.0
        reasons.append("mood match (+1.0)")

    energy_sim = 2.0 * (1.0 - abs(song["energy"] - user_prefs["target_energy"]))  # EXPERIMENT: doubled weight
    score += energy_sim
    reasons.append(f"energy similarity ({energy_sim:.2f}/2.0)")

    acousticness_sim = 1.0 - abs(song["acousticness"] - user_prefs["target_acousticness"])
    score += acousticness_sim
    reasons.append(f"acousticness similarity ({acousticness_sim:.2f}/1.0)")

    valence_sim = 1.0 - abs(song["valence"] - user_prefs["target_valence"])
    score += valence_sim
    reasons.append(f"valence similarity ({valence_sim:.2f}/1.0)")

    return score, reasons


def load_songs(csv_path: str) -> List[Dict]:
    """Read songs.csv and return a list of dicts with all numeric fields cast to int or float."""
    songs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            # integers
            row["id"] = int(row["id"])
            row["popularity"] = int(row["popularity"])
            row["explicit"] = int(row["explicit"])
            # floats
            row["energy"] = float(row["energy"])
            row["tempo_bpm"] = float(row["tempo_bpm"])
            row["valence"] = float(row["valence"])
            row["danceability"] = float(row["danceability"])
            row["acousticness"] = float(row["acousticness"])
            row["instrumentalness"] = float(row["instrumentalness"])
            row["speechiness"] = float(row["speechiness"])
            row["liveness"] = float(row["liveness"])
            row["loudness_db"] = float(row["loudness_db"])
            songs.append(row)
    return songs

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Score every song, sort by score descending, and return the top k as (song, score, explanation) tuples."""
    scored = [
        (song, score, "; ".join(reasons))
        for song in songs
        for score, reasons in [score_song(user_prefs, song)]
    ]
    ranked = sorted(scored, key=lambda x: x[1], reverse=True)
    return ranked[:k]
