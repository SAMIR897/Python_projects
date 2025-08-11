Ultimate Password Generator
Overview

Ultimate Password Generator is a secure and user-friendly password generator built with Python. It allows users to generate random passwords of a specified length using a variety of character types. The program ensures that only valid, positive integer inputs are accepted for password length. It also offers a graphical user interface (GUI) for ease of use, leveraging the Tkinter library.

This tool allows users to choose from the following character types for password generation:

    Uppercase letters (A-Z)

    Lowercase letters (a-z)

    Digits (0-9)

    Special characters (!@#$)

Additionally, users can copy the generated password directly to the clipboard for easy use.
Features

    Password Length Control: Users can set the password length using a dropdown or by manually entering a valid positive integer.

    Character Type Selection: Select from uppercase letters, lowercase letters, digits, and special characters for your password.

    Clipboard Support: Automatically copy the generated password to the clipboard with a single click.

    Error Handling: The program only accepts positive integers for password length. Any invalid input (e.g., negative numbers, floats, or non-numeric values) will trigger an error message.

    Interactive GUI: The program uses Tkinter to provide a clean, interactive interface.

Requirements

To run this program, you'll need to have the following Python modules installed:

    Tkinter: Used for creating the graphical user interface (GUI).

    pyperclip: Allows copying the generated password to the clipboard.

    string: Provides the necessary sets of characters (uppercase, lowercase, digits, and punctuation) for password generation.

You can install pyperclip by running the following command:

pip install pyperclip

Tkinter comes pre-installed with Python, so no additional installation is necessary for that.
Modules Used
1. tkinter

Used to create the GUI for the password generator, including:

    Creating labels, buttons, entry fields, and dropdowns.

    Handling user input and events, such as dropdown selections and button clicks.

2. pyperclip

Used to copy the generated password to the clipboard for easy use. This simplifies the process of transferring the password into other applications, such as password managers.
3. string

Provides predefined sets of characters for the password generation process:

    string.ascii_uppercase: Uppercase letters (A-Z)

    string.ascii_lowercase: Lowercase letters (a-z)

    string.digits: Digits (0-9)

    string.punctuation: Special characters like !@#$%

4. random

Used to randomly select characters from the available sets and to shuffle the generated password for additional randomness.
How It Works

    Input Validation:

        The program uses the Combobox widget to allow the user to select or input a password length.

        The validate_positive_int_input() function ensures that only valid positive integers can be typed or selected for the password length. If an invalid input is entered (e.g., negative values, decimals, or non-numeric values), an error message is displayed, and no password is generated.

        The length of the password is dynamically updated based on user input or selection from the dropdown.

    Character Type Selection:

        Users can select which character sets (uppercase letters, lowercase letters, digits, and special characters) they want to include in the generated password.

        If no character set is selected, the program will notify the user to select at least one character type.

    Password Generation:

        The program selects random characters from the chosen character sets and creates a password of the desired length.

        The password is then shuffled to ensure randomness, and the final password is displayed in an entry field.

    Clipboard Functionality:

        Once the password is generated, users can click the "Copy to Clipboard" button, which copies the password to the clipboard using the pyperclip module.

Error Handling

    Positive Integer Validation:

        Only positive integers are accepted for the password length. Any attempt to input a non-positive integer (e.g., 0, negative numbers, or floats) will be rejected, and an error message will be shown.

    Empty or Invalid Input:

        If the password length input is left empty, or if the value entered is invalid, the program will prompt the user with an appropriate message.


Screenshots
Here’s a screenshot of the Ultimate Password Generator:

![Screenshot][def]

Usage Instructions

    Running the Program:

        Clone or download this repository to your local machine.

        Make sure you have Python installed (Python 3.x is recommended).

        Install the required modules: pip install pyperclip.

        Run the program by executing the following command in your terminal:

        python password_gen.py

    Using the Application:

        Open the application.

        Select the desired password length from the dropdown or enter a valid positive integer.

        Choose the types of characters to include in the password (e.g., uppercase, lowercase, digits, and special characters).

        Click "Generate Password" to generate a secure password.

        Click "Copy to Clipboard" to copy the generated password for use.

License

This project is licensed under the MIT License - see the LICENSE file for details.
Conclusion

The Ultimate Password Generator is a highly customizable and secure tool for generating random passwords. With an intuitive GUI and built-in validation, it ensures that only valid inputs are accepted, making it a reliable solution for creating secure passwords.

[def]: assets/Screenshot.png
