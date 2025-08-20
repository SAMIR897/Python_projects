# Secure Password Generator

A 🔐 secure and 🎨 user-friendly password generator built with 🐍 **Python** and Tkinter, crafted to create strong passwords for Web3 wallets or apps. With custom options, clipboard integration, and robust validation, it ensures security and ease. Built by Samir, a blockchain enthusiast with a 🌟 top 1% TryHackMe ranking, this project showcases my secure coding skills.

## Features

🔧 Generate passwords with custom length and types (uppercase 🔠, lowercase 🔡, digits 🔢, special characters ❗).  
🛡️ Enforce positive integer inputs for secure lengths.  
📋 Copy passwords to clipboard with one click.  
🖥️ Intuitive Tkinter GUI with dropdowns and checkboxes.  
🔐 Randomize passwords for Web3-ready security.

## Tech Stack

🐍 **Language**: Python 3.x  
🖼️ **GUI**: Tkinter  
📚 **Libraries**:  
- **pyperclip**: Clipboard copying  
- **string**: Character sets  
- **random**: Secure randomization  

🔨 **Tools**: Git, Python CLI

### Screenshot

🖼️ Main Interface: assets/Screenshot.png

## Installation

### Prerequisites

🐍 **Python 3.x** (includes Tkinter)  
📋 **pyperclip**: `pip install pyperclip`  
🌐 **Git** (optional)

### Steps

1. Clone the repository:  
   `git clone https://github.com/SAMIR897/Python_projects.git`  
   `cd Python_projects/Basic_projects/2. Secure Password Generator`

2. Install dependencies:  
   `pip install pyperclip`

3. Run the application:  
   `python password_gen.py`

### Use the tool:
🔢 Select or enter a positive integer length.  
✅ Choose character types via checkboxes.  
🔧 Click "Generate Password" to create.  
📋 Click "Copy to Clipboard" to save.

## How It Works

- **Input Validation**: 🕵️‍♂️ Tkinter Combobox ensures positive integers, rejecting invalid inputs.  
- **Character Selection**: ✅ Users pick character sets or get prompted.  
- **Password Generation**: 🎲 Randomly picks and shuffles characters.  
- **Clipboard**: 📋 Copies passwords via pyperclip.copy.

## Error Handling

🚫 Rejects invalid inputs with GUI alerts.  
✅ Ensures at least one character type is selected.

## Why This Project?

Showcases my skills in:

- 🐍 Python and Tkinter for intuitive apps.  
- 🔐 Cybersecurity, leveraging TryHackMe achievements.  
- 🛠️ Robust coding with error handling.  
- 💼 Portfolio fit, complementing my Web3 DApps.

## Contributing

🚀 Contributions welcome! To contribute:

1. Fork: [https://github.com/SAMIR897/Python_projects](https://github.com/SAMIR897/Python_projects)  
2. Branch: `git checkout -b feature/your-feature`  
3. Commit: `git commit -m "Add feature"`  
4. Push: `git push origin feature/your-feature`  
5. Open a pull request.

See **CONTRIBUTING.md** for details.

## License

🔓 **MIT License** allows free use and modification.
