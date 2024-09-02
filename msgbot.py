import random
import time
import os

# Initialize an empty set to store words found in the current round
found_words = set()

def generate_letters():
    # Generate a set of random letters
    letters = [random.choice('abcdefghijklmnopqrstuvwxyz') for _ in range(7)]
    return ''.join(letters)

def check_word(word, letters):
    # Check if a word can be formed using the given letters
    return all(word.count(letter) <= letters.count(letter) for letter in word)

def calculate_points(word):
    # Calculate points for a word based on its length
    return len(word) * random.randint(1, 3)

def main():
    global found_words

    while True:
        incoming_msg = input("Enter a command (e.g., 'jumble', 't-score', 'exit'): ").strip().lower()

        if incoming_msg == 'jumble':
            # Generate random letters and inform the user
            letters = generate_letters()
            print(f"Unscramble these letters: {letters}. You have 90 seconds to submit as many words as you can.")

            # Start timer for 90 seconds
            start_time = time.time()
            valid_words = []
            total_points = 0

            while time.time() - start_time < 90:
                word = input("Submit a word: ").strip().lower()

                if word in found_words:
                    print(f"{word} has already been found by another player and is not valid for this round.")
                    continue

                if check_word(word, letters):
                    points = calculate_points(word)
                    valid_words.append((word, points))
                    total_points += points
                    print(f"\u2705 Points: {points} ({word})")
                    found_words.add(word)
                else:
                    print(f"\u274C ({word})")
                # Include the list of letters with each response
                print(f"Letters: {letters}")

            # Send the user their score for the round
            print("Round score:")
            for word, points in valid_words:
                print(f"{word}: {points} points")
            print(f"Total score: {total_points} points")

        elif incoming_msg == 't-score':
            # Send the user their total score
            print(f"Your total score is: {total_points} points")  # Replace [total_score] with the actual total score

        elif incoming_msg == 'exit':
            print("Exiting the game. Goodbye!")
            break

        else:
            # Inform the user about the command to start the game
            print("Send 'jumble' to start the game or 'exit' to quit.")

if __name__ == '__main__':
    main()
