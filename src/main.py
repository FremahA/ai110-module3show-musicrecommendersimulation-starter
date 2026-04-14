"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from tabulate import tabulate
from recommender import load_songs, recommend_songs


PROFILES = {
    "High-Energy Pop": {
        "favorite_genre":      "pop",
        "favorite_mood":       "happy",
        "target_energy":        0.90,
        "target_acousticness":  0.10,
        "target_valence":       0.85,
    },
    "Chill Lofi": {
        "favorite_genre":      "lofi",
        "favorite_mood":       "chill",
        "target_energy":        0.35,
        "target_acousticness":  0.85,
        "target_valence":       0.58,
    },
    "Deep Intense Rock": {
        "favorite_genre":      "rock",
        "favorite_mood":       "intense",
        "target_energy":        0.90,
        "target_acousticness":  0.10,
        "target_valence":       0.40,
    },
}

# Adversarial profiles — designed to expose weaknesses in the scoring logic.
# Swap PROFILES for ADVERSARIAL_PROFILES in main() to run them.
ADVERSARIAL_PROFILES = {

    # Energy and valence pull in opposite directions.
    # High-energy songs tend to have high valence, so the valence penalty may
    # rank a quiet sad song above a loud sad one.
    "High-Energy Sad": {
        "favorite_genre":      "indie rock",
        "favorite_mood":       "sad",
        "target_energy":        0.95,
        "target_acousticness":  0.10,
        "target_valence":       0.05,
    },

    # Genre not present in songs.csv — no song ever earns the +2.0 bonus.
    # The entire top-k is decided by at most 4.0 points; mood and continuous
    # features become the only signal.
    "Ghost Genre": {
        "favorite_genre":      "bossa nova",
        "favorite_mood":       "chill",
        "target_energy":        0.40,
        "target_acousticness":  0.70,
        "target_valence":       0.60,
    },

    # All continuous targets at 0.0.
    # similarity = 1 - |song.value - 0| = 1 - song.value, so higher-valued
    # songs are penalised. Near-silent, joyless tracks float to the top.
    "Dead Zone": {
        "favorite_genre":      "ambient",
        "favorite_mood":       "chill",
        "target_energy":        0.0,
        "target_acousticness":  0.0,
        "target_valence":       0.0,
    },

    # High acousticness and high energy are physically contradictory.
    # The scorer has no model of this tradeoff — it just averages penalties —
    # so results may look "perfect" on paper but feel nonsensical.
    "Max Everything": {
        "favorite_genre":      "edm",
        "favorite_mood":       "euphoric",
        "target_energy":        1.0,
        "target_acousticness":  1.0,
        "target_valence":       1.0,
    },

    # The catalog has metal/angry but not metal/happy.
    # Does the +2.0 genre bonus dominate even when the mood is completely wrong?
    # Watch for metal/angry ranking above pop/happy.
    "Happy Metal": {
        "favorite_genre":      "metal",
        "favorite_mood":       "happy",
        "target_energy":        0.90,
        "target_acousticness":  0.10,
        "target_valence":       0.80,
    },

    # Midpoint targets make every song equally mediocre on continuous features.
    # The flat +2/+1 bonuses become the only real signal — exposes how much
    # genre/mood dominate when numeric features give no information.
    "Midpoint Flatline": {
        "favorite_genre":      "jazz",
        "favorite_mood":       "relaxed",
        "target_energy":        0.5,
        "target_acousticness":  0.5,
        "target_valence":       0.5,
    },

    # target_energy out of [0, 1] range.
    # 1 - |song.energy - 1.3| silently produces wrong similarities for all
    # songs; no error is raised, scores are just quietly incorrect.
    "Out-of-Range Energy": {
        "favorite_genre":      "rock",
        "favorite_mood":       "intense",
        "target_energy":        1.3,
        "target_acousticness":  0.10,
        "target_valence":       0.40,
    },
}


def print_recommendations(profile_name: str, user_prefs: dict, songs: list, label: str = "Profile") -> None:
    """Print top 5 recommendations as a formatted table with score reasons."""
    recommendations = recommend_songs(user_prefs, songs, k=5)

    print("\n" + "=" * 72)
    print(f"  {label}: {profile_name}")
    print("=" * 72)

    rows = []
    for i, (song, score, explanation) in enumerate(recommendations, start=1):
        reasons = "\n".join(f"• {r}" for r in explanation.split("; "))
        rows.append([
            f"#{i}",
            f"{song['title']}\n{song['artist']}",
            f"{song['genre']}\n{song['mood']}",
            f"{score:.2f}/6.0",
            reasons,
        ])

    print(tabulate(
        rows,
        headers=["Rank", "Title / Artist", "Genre / Mood", "Score", "Why"],
        tablefmt="simple_grid",
        maxcolwidths=[4, 22, 14, 8, 32],
    ))
    print()


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}")

    for profile_name, user_prefs in PROFILES.items():
        print_recommendations(profile_name, user_prefs, songs)

    print("\n" + "#" * 40)
    print("  ADVERSARIAL / EDGE-CASE PROFILES")
    print("#" * 40)

    for profile_name, user_prefs in ADVERSARIAL_PROFILES.items():
        print_recommendations(profile_name, user_prefs, songs, label="Adversarial Profile")


if __name__ == "__main__":
    main()
