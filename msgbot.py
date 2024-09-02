from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import random
import time

# Assuming 'app' is already defined in msgbot.py
# If not, uncomment the next line to create the Flask app
# app = Flask(__name__)

# Initialize an empty set to store words found in the current round
found_words = set()

# Global variable to store the letters for the current round
current_letters = ''

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

@app.route('/bot', methods=['POST'])
def bot():
    global found_words
    global current_letters

    incoming_msg = request.values.get('Body', '').lower()
    resp = MessagingResponse()
    msg = resp.message()

    if incoming_msg == 'jumble':
        # Generate random letters and inform the user
        current_letters = generate_letters()
        found_words.clear()  # Clear previously found words
        msg.body(f"Unscramble these letters: {current_letters}. You have 90 seconds to submit as many words as you can.")
        
        # Ideally, you would manage the timing without sleep in a real environment.
        # Simulating timing for demo purposes here
        time.sleep(90)
        
        # After 90 seconds, handle the user submissions
        # Note: Actual implementation would require handling submissions as they come in
        
        # Directly use submitted words for demonstration purposes
        submitted_words = request.values.get('Body', '').lower().split()

        valid_words = []
        total_points = 0
        for word in submitted_words:
            if word in found_words:
                msg.body(f"{word} has already been found by another player and is not valid for this round.")
                continue
            if check_word(word, current_letters):
                points = calculate_points(word)
                valid_words.append((word, points))
                total_points += points
                msg.body("\u2705" + f" Points: {points} ({word})")
                found_words.add(word)
            else:
                msg.body("\u274C" + f" ({word})")

        # Send the user their score for the round
        msg.body("Round score:")
        for word, points in valid_words:
            msg.body(f"{word}: {points} points")
        msg.body(f"Total score: {total_points} points")

    elif incoming_msg == 't-score':
        # Send the user their total score
        msg.body("Your total score is: [total_score] points")  # Replace [total_score] with the actual total score

    else:
        # Inform the user about the command to start the game
        msg.body("Send 'jumble' to start the game.")

    return str(resp)

# If msgbot.py is run directly, start the Flask app
if __name__ == '__main__':
    app.run(debug=True)
