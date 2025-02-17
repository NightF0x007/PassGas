import os
import itertools
import argparse
import csv
import logging
import json
import sys

# Load configuration from file (optional)
def load_config(config_file):
    try:
        with open(config_file) as f:
            return json.load(f)
    except Exception as e:
        logging.error(f"Failed to load config: {e}")
        return {}

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

# Default mappings and special characters can now be updated via configuration.
DEFAULT_LEET_MAPPING = str.maketrans("aeiost", "431057")
DEFAULT_SPECIAL_CHARS = "~`!@#$%^&*()-_+={}[]|\\;:\"<>,./?"

def sanitize(value):
    """Remove unwanted characters and handle 'N/A' values."""
    return value.strip() if value and value.lower() != "n/a" else ""

def clean_keywords(keyword_str):
    """
    Clean up the keyword string by removing stray quotes and splitting by commas.
    For example, converting '"Magic,Hacking,Eating"' to ['Magic', 'Hacking', 'Eating'].
    """
    keyword_str = keyword_str.strip().strip('"')
    keyword_str = keyword_str.replace('"', '')
    return [kw.strip() for kw in keyword_str.split(",") if kw.strip()]

def leetspeak(word, leet_mapping=DEFAULT_LEET_MAPPING):
    """Generate recursive leetspeak variations for a given word."""
    variations = {word}
    if word:
        leet = word.translate(leet_mapping)
        variations.add(leet)
        for i in range(len(word)):
            partial = word[:i] + word[i:].translate(leet_mapping)
            variations.add(partial)
    return variations

def add_special_chars(word, special_chars=DEFAULT_SPECIAL_CHARS, max_special_repeats=3):
    """Generate variations of a word with repeated special characters."""
    variations = {word}
    for repeat in range(1, max_special_repeats + 1):
        for chars in itertools.product(special_chars, repeat=repeat):
            char_combo = "".join(chars)
            variations.add(f"{word}{char_combo}")
            variations.add(f"{char_combo}{word}")
    return variations

def generate_passwords(row, max_special_repeats=3, leet_mapping=DEFAULT_LEET_MAPPING, special_chars=DEFAULT_SPECIAL_CHARS):
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
    keywords_raw = sanitize(row.get("keywords", ""))
    keywords = clean_keywords(keywords_raw) if keywords_raw else []
    
    base_words = set(filter(None, fields + keywords))
    passwords = set()
    
    # Generate passwords from base words
    for word in base_words:
        variations = {word, word.capitalize(), word[::-1], word[::-1].capitalize()}
        for var in list(variations):
            variations.update(leetspeak(var, leet_mapping))
        for var in list(variations):
            variations.update(add_special_chars(var, special_chars, max_special_repeats))
        passwords.update(variations)
    
    # Combine words for advanced permutations
    for combo in itertools.combinations(base_words, 2):
        combined = "".join(combo)
        passwords.update(leetspeak(combined, leet_mapping))
        passwords.update(add_special_chars(combined, special_chars, max_special_repeats))
    
    return passwords

def meets_policy(password, min_length, require_uppercase, require_numeric, require_special, special_chars=DEFAULT_SPECIAL_CHARS):
    """
    Check if the password meets the defined security policy requirements:
      - At least min_length characters long.
      - Contains at least one uppercase letter (if require_uppercase is True).
      - Contains at least one numeric digit (if require_numeric is True).
      - Contains at least one special character (if require_special is True).
    """
    if len(password) < min_length:
        return False
    if require_uppercase and not any(c.isupper() for c in password):
        return False
    if require_numeric and not any(c.isdigit() for c in password):
        return False
    if require_special and not any(c in special_chars for c in password):
        return False
    return True

def filter_passwords(passwords, min_length, require_uppercase, require_numeric, require_special, special_chars=DEFAULT_SPECIAL_CHARS):
    """Filter the provided set of passwords based on the security policy."""
    return {pw for pw in passwords if meets_policy(pw, min_length, require_uppercase, require_numeric, require_special, special_chars)}

def process_csv(csv_file, output_dir, max_special_repeats, config, min_length, require_uppercase, require_numeric, require_special):
    """Process a CSV file and generate password lists with filtering based on password policy."""
    if not os.path.exists(csv_file):
        logging.error(f"Error: File '{csv_file}' not found.")
        return

    os.makedirs(output_dir, exist_ok=True)
    master_passwords = set()

    try:
        with open(csv_file, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                passwords = generate_passwords(
                    row,
                    max_special_repeats,
                    config.get("leet_mapping", DEFAULT_LEET_MAPPING),
                    config.get("special_chars", DEFAULT_SPECIAL_CHARS)
                )

                # Filter passwords based on the security policy requirements
                valid_passwords = filter_passwords(passwords, min_length, require_uppercase, require_numeric, require_special, config.get("special_chars", DEFAULT_SPECIAL_CHARS))

                # Determine output file using sanitized names; fallback to "unknown" if not provided.
                fname = sanitize(row.get("firstname")).lower() or "unknown"
                lname = sanitize(row.get("lastname")).lower() or "unknown"
                output_file = os.path.join(output_dir, f"{fname}_{lname}_passwords.txt")
                with open(output_file, "w", encoding="utf-8") as out:
                    out.write("\n".join(sorted(valid_passwords, key=str.lower)))

                master_passwords.update(valid_passwords)

        master_file = os.path.join(output_dir, "master_password_list.txt")
        with open(master_file, "w", encoding="utf-8") as master_out:
            master_out.write("\n".join(sorted(master_passwords, key=str.lower)))
        logging.info(f"Password lists saved to {output_dir}/")
    except Exception as e:
        logging.error(f"An error occurred processing CSV: {e}")

def interactive_mode(output_dir, max_special_repeats, config):
    """Interactive mode for users who prefer input prompts over command-line arguments."""
    # Ask for password policy options interactively
    try:
        min_length = int(input("Enter minimum password length (default 8): ").strip() or 8)
    except ValueError:
        min_length = 8

    require_uppercase = input("Require at least one uppercase letter? (y/n, default n): ").strip().lower() == "y"
    require_numeric = input("Require at least one numeric digit? (y/n, default n): ").strip().lower() == "y"
    require_special = input("Require at least one special character? (y/n, default n): ").strip().lower() == "y"

    os.makedirs(output_dir, exist_ok=True)
    master_passwords = set()
    user_counter = 1

    while True:
        print(f"\n--- Enter details for user #{user_counter} ---")
        row = {}
        row["firstname"] = input("First name: ").strip()
        row["lastname"] = input("Last name: ").strip()
        row["nickname"] = input("Nickname (optional): ").strip()
        row["birthdate"] = input("Birthdate (optional): ").strip()
        row["partnername"] = input("Partner's name (optional): ").strip()
        row["partnernickname"] = input("Partner's nickname (optional): ").strip()
        row["partnerbirthdate"] = input("Partner's birthdate (optional): ").strip()
        row["petname"] = input("Pet name (optional): ").strip()
        row["companyname"] = input("Company name (optional): ").strip()
        row["keywords"] = input("Keywords (comma-separated, optional): ").strip()

        passwords = generate_passwords(
            row,
            max_special_repeats,
            config.get("leet_mapping", DEFAULT_LEET_MAPPING),
            config.get("special_chars", DEFAULT_SPECIAL_CHARS)
        )
        valid_passwords = filter_passwords(passwords, min_length, require_uppercase, require_numeric, require_special, config.get("special_chars", DEFAULT_SPECIAL_CHARS))

        # Save individual user password file
        fname = sanitize(row.get("firstname")).lower() or f"user{user_counter}"
        lname = sanitize(row.get("lastname")).lower() or "unknown"
        output_file = os.path.join(output_dir, f"{fname}_{lname}_passwords.txt")
        try:
            with open(output_file, "w", encoding="utf-8") as out:
                out.write("\n".join(sorted(valid_passwords, key=str.lower)))
            logging.info(f"Password list saved for {fname} {lname} -> {output_file}")
        except Exception as e:
            logging.error(f"Error saving file for {fname} {lname}: {e}")
        
        master_passwords.update(valid_passwords)

        cont = input("\nDo you want to enter another user? (y/n): ").lower().strip()
        if cont != "y":
            break
        user_counter += 1

    master_file = os.path.join(output_dir, "master_password_list.txt")
    try:
        with open(master_file, "w", encoding="utf-8") as master_out:
            master_out.write("\n".join(sorted(master_passwords, key=str.lower)))
        logging.info(f"\nMaster password list saved to {master_file}")
    except Exception as e:
        logging.error(f"Error saving master password list: {e}")

def main():
    print_banner()
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

    parser = argparse.ArgumentParser(
        description="PassGas: Generate expansive password lists with leetspeak, special characters, custom combinations, and password policy filtering.\n\n"
                    "Usage Examples:\n"
                    "  Command-line mode: python PassGas.py -c data.csv --min-length 8 --require-uppercase --require-numeric --require-special\n"
                    "  Interactive mode: python PassGas.py --interactive\n\n"
                    "For more information, see the README.md file.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument("-c", "--csv-file", type=str, help="Path to the input CSV file.")
    parser.add_argument("-o", "--output-dir", type=str, default="custom_passwords", help="Directory to save individual password files.")
    parser.add_argument("-r", "--max-special-repeats", type=int, default=3, help="Maximum repetitions of special characters in passwords.")
    parser.add_argument("-f", "--config-file", type=str, default="", help="Path to a JSON configuration file for custom settings.")
    parser.add_argument("--min-length", type=int, default=8, help="Minimum password length required.")
    parser.add_argument("--require-uppercase", action="store_true", help="Require at least one uppercase letter in the password.")
    parser.add_argument("--require-numeric", action="store_true", help="Require at least one numeric character in the password.")
    parser.add_argument("--require-special", action="store_true", help="Require at least one special character in the password.")
    parser.add_argument("-i", "--interactive", action="store_true", help="Run in interactive mode without CSV input.")
    
    args = parser.parse_args()

    config = {}
    if args.config_file:
        config = load_config(args.config_file)

    # Determine mode: interactive mode or CSV mode.
    if args.interactive or not args.csv_file:
        logging.info("Running in interactive mode.\n")
        interactive_mode(args.output_dir, args.max_special_repeats, config)
    else:
        process_csv(args.csv_file, args.output_dir, args.max_special_repeats, config,
                    args.min_length, args.require_uppercase, args.require_numeric, args.require_special)

if __name__ == "__main__":
    main()
