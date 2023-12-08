# MyVideoGameLibrary

PySimpleGUI interface in Python for managing a video game library. It allows adding, viewing, updating progress, and deleting games. Data is stored in CSV.

## Features:

- **Add Game:**
    - The user can add a new game to the library by providing details such as the game's name, genre, platform, and current progress.
    - Game information will be stored in a simple database (it can be a CSV file for simplicity).

- **View Library:**
    - Displays a list of all games in the library along with their current progress.
    - Games will be shown in a table or list for easy viewing.

- **Update Progress:**
    - Allows the user to update the progress of a specific game. This can be done through a slider, text box, or some other input element.

- **Delete Game:**
    - The user can remove a game from the library if they are no longer playing it.

- **Save and Load Library:**
    - Provides functions to save the library to a file and load it again in future sessions.

## Technologies Used:

- **Python:**
    - The main programming language.

- **PySimpleGUI:**
    - A library for creating user-friendly graphical user interfaces.

- **CSV:**
    - To store details of the game library.
