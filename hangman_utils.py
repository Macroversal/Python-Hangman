import random
import nltk
import os
import pickle

# Constants
SCORES_FILE = "scores.pkl"

# Function to download NLTK data
def download_nltk_data():
    nltk.download("words")
    nltk.download("stopwords")

# Add your game functions here

if __name__ == "__main__":
    try:
        download_nltk_data()

        # Load scores
        if os.path.exists(SCORES_FILE):
            with open(SCORES_FILE, "rb") as scores_file:
                scores = pickle.load(scores_file)
        else:
            scores = {difficulty: {"wins": 0, "losses": 0} for difficulty in range(1, 6)}

        # Add your game logic here

    except KeyboardInterrupt:
        print("\nExiting the game.")

# Other utility functions can go here if needed

