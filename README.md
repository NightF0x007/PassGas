# **PassGas.py**
Because cracking passwords shouldn't stink!** 🏎️💨  

---

## **Overview**
**PassGas.py** is a password list generator designed for penetration testers, cybersecurity enthusiasts, and ethical hackers. It uses user-provided data to generate expansive password lists, complete with leetspeak transformations, special character variations, and advanced combinations.

Whether you're looking for a quick password dictionary or a comprehensive wordlist, **PassGas** delivers high-octane results without breaking a sweat!

---

## **Features**
- **Leetspeak Transformations**:
  - Converts letters like `a -> 4`, `e -> 3`, `i -> 1`, `o -> 0`, etc.
  - Recursive leetspeak generation for deeper permutations.
- **Special Character Variations**:
  - Appends and prepends special characters like `!@#$%^&*` (customizable).
  - Repeats special characters up to a user-defined limit.
- **Custom Wordlist Generation**:
  - Combines names, nicknames, dates, and keywords into creative permutations.
- **Advanced Combinations**:
  - Generates concatenated words with transformations and special character additions.
- **Command-Line Friendly**:
  - Specify CSV input, output directory, and special character limits via parameters.

---

## **Usage**

### **1. Installation**
Clone the repository:
```bash
git clone https://github.com/NightF0x007/PassGas.git
cd PassGas
```

### **2. Requirements**
PassGas.py requires Python 3.6+ and no additional dependencies.

### **3. Input File Format**
Create a CSV file (e.g., `users.csv`) with the following columns:
```csv
firstname,lastname,nickname,birthdate,partnername,partnernickname,partnerbirthdate,petname,companyname,keywords
Jon,Doe,,01011990,,,,floofy,MyJob,"Magic,Hacking,Eating"
```

### **4. Running the Script**
Run PassGas.py with the following options:
```bash
python3 PassGas.py -c users.csv -o custom_passwords -r 3
```

#### **Options**
| Option                  | Description                                           |
|-------------------------|-------------------------------------------------------|
| `-c, --csv-file`        | Path to the input CSV file.                           |
| `-o, --output-dir`      | Directory to save individual password files.          |
| `-r, --max-special-repeats` | Maximum repetitions of special characters (default: 3). |

### **5. Output**
- **Individual Password Files**: Stored in the specified output directory.
- **Master Password List**: `master_password_list.txt` contains all passwords.

---

### **Run Command**:
```bash
python3 PassGas.py -c users.csv -o passwords -r 3
```

If the list is too gassed up, filter it down.
```
grep -E '^.{6,}$' master_password_list.txt| grep -E '[A-Z]' | grep -E '[a-z]' | grep -E '[0-9]' | grep -E '([!@#$%^&*].*){2,}' > filtered_usernames.txt
```


---

## **Acknowledgments**
- ASCII art generated with love for cybersecurity enthusiasts.
- Created by **NightF0x007**.

---

## **Disclaimer**
This tool is intended for educational purposes only. Misuse of this tool is strictly prohibited.

