import random

def number_guessing_game():
    print("Welcome to the Number Guessing Game!")
    number_to_guess = random.randint(1, 100)
    attempts = 0

    while True:
        user_guess = input("Enter your guess (between 1 and 100): ")
        attempts += 1

        # Validate input
        if not user_guess.isdigit():
            print("Please enter a valid number.")
            continue

        user_guess = int(user_guess)

        if user_guess < 1 or user_guess > 100:
            print("Your guess is out of bounds. Please guess a number between 1 and 100.")
            continue

        if user_guess < number_to_guess:
            print("Too low! Try again.")
        elif user_guess > number_to_guess:
            print("Too high! Try again.")
        else:
            print(f"Congratulations! You've guessed the number {number_to_guess} in {attempts} attempts!")
            break

if __name__ == '__main__':
    number_guessing_game()