import random
import string

def generate_password():
    # Generate a random 5-digit number
    number = random.randint(10000, 99999)

    # Generate a random letter from the alphabet
    letter = random.choice(string.ascii_letters.lower())

    # Combine the number and letter into a single password
    password = f"{letter}{number}"

    return password


# Example usage
password = generate_password()

