🔒 Secure Password Generator
A robust, user-centric, and highly secure password generator crafted with Python and Tkinter, designed to create strong, customizable passwords for Web3 wallets, applications, or sensitive systems. With a sleek graphical interface, flexible character type selection, and seamless clipboard integration, this tool ensures security and ease of use. Built by Samir, a blockchain developer with a passion for cybersecurity (top 1% on TryHackMe), this project showcases my expertise in delivering secure, practical solutions tailored for modern tech ecosystems.
🌟 Features

Customizable Passwords: Generate passwords of user-defined lengths with options for uppercase letters (A-Z), lowercase letters (a-z), digits (0-9), and special characters (!@#$%).
Advanced Security: Enforces strict input validation, accepting only positive integers for password length to prevent weak configurations.
Clipboard Functionality: Instantly copy generated passwords to the clipboard using pyperclip, streamlining integration with password managers or blockchain wallets.
Intuitive GUI: Leverages Tkinter for a clean, interactive interface with dropdowns, checkboxes, and real-time error feedback.
Cybersecurity Focus: Employs randomized character selection and shuffling to produce unpredictable passwords, aligning with best practices for secure key generation.

🛠️ Tech Stack

Language: Python 3.x
GUI Framework: Tkinter
Libraries:
pyperclip: Facilitates one-click password copying to the clipboard.
string: Provides character sets for password generation (uppercase, lowercase, digits, punctuation).
random: Ensures secure randomization and shuffling for unpredictable passwords.


Tools: Git, VS Code, Python CLI

📸 Screenshot

Main Interface: assets/Screenshot.png 

📦 Installation
Prerequisites

Python 3.x (includes Tkinter by default)
pyperclip library: Install with pip install pyperclip
Git (optional for cloning)

Setup Instructions

Clone the Repository:
git clone https://github.com/SAMIR897/Python_projects.git
cd Python_projects/Basic_projects/2.\ Secure\ Password\ Generator


Install Dependencies:
pip install pyperclip


Run the Application:
python password_gen.py


Using the Tool:

Select or enter a password length (positive integer) via the dropdown or input field.
Choose character types (uppercase, lowercase, digits, special characters) using checkboxes.
Click Generate Password to create a secure password displayed in the GUI.
Click Copy to Clipboard to save the password for immediate use.



🧠 How It Works

Input Validation:
Utilizes Tkinter’s Combobox for password length selection, validated by the validate_positive_int_input() function to accept only positive integers.
Rejects invalid inputs (e.g., negative numbers, decimals, non-numeric values) with user-friendly error messages.


Character Type Selection:
Allows users to select character sets (string.ascii_uppercase, string.ascii_lowercase, string.digits, string.punctuation) via checkboxes.
Ensures at least one character type is selected, prompting users if none are chosen.


Password Generation:
Randomly selects characters from chosen sets using random.choice for diversity.
Shuffles the password with random.shuffle to enhance randomness and security.
Displays the generated password in a Tkinter entry field.


Clipboard Integration:
Copies the password to the clipboard using pyperclip.copy, enabling seamless use in external applications.



🔐 Security Highlights

Strict Validation: Prevents weak passwords by enforcing positive integer lengths and requiring at least one character type.
Randomized Output: Combines random.choice and random.shuffle to ensure unpredictable, cryptographically sound passwords.
Web3 Relevance: Ideal for generating secure keys for blockchain wallets (e.g., Phantom Wallet), complementing my expertise in Solana and Ethereum DApps.
Cybersecurity Edge: Reflects my top 1% TryHackMe ranking, emphasizing secure coding practices.

🛑 Error Handling

Invalid Input: Rejects non-positive integers, decimals, or empty inputs with clear, real-time GUI alerts.
No Character Types: Prompts users to select at least one character set to ensure valid password generation.
User-Centric Feedback: Provides immediate error notifications to guide users, enhancing usability and reliability.

🌟 Why This Project?
This project demonstrates my expertise in:

Python Development: Building intuitive, user-focused applications with Tkinter for seamless interaction.
Cybersecurity Principles: Implementing robust password generation aligned with industry standards, informed by my TryHackMe achievements.
Error-Resilient Design: Crafting code with comprehensive input validation for reliability and user trust.
Portfolio Versatility: Complements my blockchain projects (e.g., DeFi DApps, NFT marketplaces) to showcase my range for Web3 roles in Dubai’s thriving tech ecosystem.

🤝 Contributing
I welcome contributions to enhance this tool! To contribute:

Fork the repository: https://github.com/SAMIR897/Python_projects.
Create a feature branch: git checkout -b feature/your-feature.
Commit changes: git commit -m "Add your feature".
Push to the branch: git push origin feature/your-feature.
Open a pull request with a clear description of your changes.

Please review the CONTRIBUTING.md file for detailed guidelines.
📜 License
This project is licensed under the MIT License, allowing free use, modification, and distribution with proper attribution.
🎯 Get Started
Generate secure passwords for your Web3 wallets or applications today! Star this repository to support my journey to contribute to Dubai’s blockchain innovation.