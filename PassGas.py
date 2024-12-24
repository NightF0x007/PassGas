import os
import itertools
import argparse

# ASCII banner
def print_banner():
    banner = r"""
██████╗  █████╗ ███████╗███████╗ ██████╗  █████╗ ███████╗
██╔══██╗██╔══██╗██╔════╝██╔════╝██╔════╝ ██╔══██╗██╔════╝
██████╔╝███████║███████╗███████╗██║  ███╗███████║███████╗
██╔═══╝ ██╔══██║╚════██║╚════██║██║   ██║██╔══██║╚════██║
██║     ██║  ██║███████║███████║╚██████╔╝██║  ██║███████║
╚═╝     ╚═╝  ╚═╝╚══════╝╚══════╝ ╚═════╝ ╚═╝  ╚═╝╚══════╝
         Because cracking passwords shouldn't stink!
                       Created by NightF0x007
                        
                              🏎️💨
    """
    print(banner)

# Leetspeak substitutions and special characters
leet_mapping = str.maketrans("aeiost", "43105+")
special_chars = "!@#$%^&*"

# Sanitize input values
def sanitize(value):
    """Remove unwanted characters and handle 'N/A' values."""
    return value.strip() if value and value.lower() != "n/a" else ""

# Generate leetspeak variations
def leetspeak(word):
    """Generate recursive leetspeak variations for a given word."""
    variations = {word}
    if word:
        leet = word.translate(leet_mapping)
        variations.add(leet)
        for i in range(len(word)):
            partial = word[:i] + word[i:].translate(leet_mapping)
            variations.add(partial)
    return variations

# Generate permutations with repeated special characters
def add_special_chars(word, max_repeats=3):
    """Generate variations of a word with repeated special characters."""
    variations = {word}
    for repeat in range(1, max_repeats + 1):
        for chars in itertools.product(special_chars, repeat=repeat):
            char_combo = "".join(chars)
            variations.add(f"{word}{char_combo}")
            variations.add(f"{char_combo}{word}")
    return variations

# Generate passwords for a user
def generate_passwords(row, max_special_repeats=3):
    """Generate passwords based on user data."""
    fields = [
        sanitize(row.get("firstname")),
        sanitize(row.get("lastname")),
        sanitize(row.get("nickname")),
        sanitize(row.get("birthdate")),
        sanitize(row.get("partnername")),
        sanitize(row.get("partnernickname")),
        sanitize(row.get("partnerbirthdate")),
        sanitize(row.get("petname")),
        sanitize(row.get("companyname")),
    ]
    keywords = sanitize(row.get("keywords", "")).replace(" ", "").split(",")

    base_words = set(filter(None, fields + keywords))
    passwords = set()

    # Generate passwords from base words
    for word in base_words:
        variations = {word, word.capitalize(), word[::-1], word[::-1].capitalize()}
        for var in variations.copy():
            variations.update(leetspeak(var))
        for var in variations.copy():
            variations.update(add_special_chars(var, max_repeats=max_special_repeats))
        passwords.update(variations)

    # Combine words for advanced permutations
    for combo in itertools.combinations(base_words, 2):
        combined = "".join(combo)
        passwords.update(leetspeak(combined))
        passwords.update(add_special_chars(combined, max_repeats=max_special_repeats))

    return passwords

# Process users and generate password lists
def main(csv_file, output_dir, max_special_repeats):
    """Process the CSV file and generate password lists."""
    if not os.path.exists(csv_file):
        print(f"Error: File '{csv_file}' not found.")
        return

    os.makedirs(output_dir, exist_ok=True)
    master_passwords = set()

    try:
        with open(csv_file, newline="") as f:
            for line in f.readlines()[1:]:
                fields = line.strip().split(",")
                user_row = dict(zip(
                    ["firstname", "lastname", "nickname", "birthdate", "partnername", "partnernickname", "partnerbirthdate", "petname", "companyname", "keywords"],
                    fields
                ))
                passwords = generate_passwords(user_row, max_special_repeats)

                # Save individual password list
                output_file = f"{output_dir}/{sanitize(user_row['firstname']).lower()}_{sanitize(user_row['lastname']).lower()}_passwords.txt"
                with open(output_file, "w") as out:
                    out.write("\n".join(sorted(passwords, key=str.lower)))

                # Add to the master password list
                master_passwords.update(passwords)

        # Save the master password list
        with open("master_password_list.txt", "w") as master_out:
            master_out.write("\n".join(sorted(master_passwords, key=str.lower)))

        print(f"Password lists saved to {output_dir}/")
    except Exception as e:
        print(f"An error occurred: {e}")

# Command-line interface
if __name__ == "__main__":
    print_banner()

    parser = argparse.ArgumentParser(description="PassGas: Generate expansive password lists with leetspeak, special characters, and custom combinations.")
    parser.add_argument("-c", "--csv-file", type=str, required=True, help="Path to the input CSV file.")
    parser.add_argument("-o", "--output-dir", type=str, default="custom_passwords", help="Directory to save individual password files.")
    parser.add_argument("-r", "--max-special-repeats", type=int, default=3, help="Maximum repetitions of special characters in passwords.")
    args = parser.parse_args()

    main(args.csv_file, args.output_dir, args.max_special_repeats)
