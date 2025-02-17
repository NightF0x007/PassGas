# **PassGas.py**
**Gassed Up Password Generator.** 🏎️💨  

---

## **Overview**
PassGas is a password generation tool designed to create expansive password lists by leveraging user data along with leetspeak transformations, special character insertions, and customizable permutations. It supports both command-line and interactive modes.

---

## Features
- **Leetspeak Transformations:**  
  Convert letters such as:
  - `a` → `4`
  - `e` → `3`
  - `i` → `1`
  - `o` → `0`  
  Recursive generation creates multiple variations.
  
- **Special Character Variations:**  
  Append and prepend special characters, with a configurable maximum number of repetitions.

- **Custom Wordlist Generation:**  
  Combine names, nicknames, dates, and keywords into creative permutations.

- **Advanced Combinations:**  
  Generate concatenated words and merge different inputs for extensive password lists.

- **Password Policy Filtering:**  
  Optionally enforce a security policy that requires:
  - A minimum password length
  - At least one uppercase letter
  - At least one numeric digit
  - At least one special character

- **Modes of Operation:**  
  - **Command-line Mode:** Provide inputs via a CSV file and configure options with command-line arguments.
  - **Interactive Mode:** Enter user details and password policy options interactively with on-screen prompts.

- **Customizable Configuration:**  
  Override defaults (like leetspeak mappings and special characters) using a JSON configuration file.

---

## Installation
1. **Clone the Repository:**
   ```bash
   git clone https://github.com/NightF0x007/PassGas.git
   cd PassGas
   ```
2. **Requirements:**
   - Python 3.6 or higher (no additional dependencies required).

---

## Usage

### Command-line Mode
Run PassGas by providing the CSV input file along with desired options. For example:
```bash
python3 PassGas.py -c users.csv -o custom_passwords -r 3 --min-length 8 --require-uppercase --require-numeric --require-special
```

#### Command-line Options:
- `-c, --csv-file`  
  Path to the input CSV file with user data.
  
- `-o, --output-dir`  
  Directory where individual password files will be saved (default: `custom_passwords`).

- `-r, --max-special-repeats`  
  Maximum repetitions of special characters (default: 3).

- `-f, --config-file`  
  Path to a JSON configuration file for custom settings.

- `--min-length`  
  Minimum password length required (default: 8).

- `--require-uppercase`  
  Enforce at least one uppercase letter in the generated passwords.

- `--require-numeric`  
  Enforce at least one numeric digit in the generated passwords.

- `--require-special`  
  Enforce at least one special character in the generated passwords.

- `-i, --interactive`  
  Run in interactive mode without CSV input.

- `-h, --help`  
  Display the help menu listing all command-line options.

### Interactive Mode
If you prefer not to use a CSV or pass numerous command-line arguments, interactive mode allows you to input all required information through prompts. To run in interactive mode:
```bash
python3 PassGas.py --interactive
```
Interactive mode will prompt you for:
- **Password Policy Options:**
  - Minimum password length.
  - Whether to require at least one uppercase letter.
  - Whether to require at least one numeric digit.
  - Whether to require at least one special character.
- **User Details:**
  - First name, last name, nickname, birthdate, partner's details, pet name, company name.
  - Comma-separated keywords.

PassGas will generate individual password lists for each user and compile a master password list.

---

## CSV File Format
Create a CSV file (e.g., `users.csv`) with the following headers:
```csv
firstname,lastname,nickname,birthdate,partnername,partnernickname,partnerbirthdate,petname,companyname,keywords
```
Example:
```csv
Jon,Doe,,01011990,,,,floofy,MyJob,"Magic,Hacking,Eating"
```
- **keywords:** Provide a comma-separated list of keywords; the tool cleans stray quotes and extra spaces automatically.

---

If the list is too gassed up, filter it down.
```
grep -E '^.{6,}$' master_password_list.txt| grep -E '[A-Z]' | grep -E '[a-z]' | grep -E '[0-9]' | grep -E '([!@#$%^&*].*){2,}' > filtered_passwords.txt
```

Usernames from a csv with "firstname,lastname" headers.
```
username-anarchy --list-formats | awk '/^[a-z]/ {print $1}' | xargs -I {} username-anarchy --input-file simplified_users.csv --select-format {} > usernames.txt
```

---

## Disclaimer
PassGas is intended for educational and authorized penetration testing purposes only. Use this tool responsibly and legally.

