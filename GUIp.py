# https://apuntes.de/python/expresiones-regulares-y-busqueda-de-patrones-en-python-poder-y-flexibilidad/#gsc.tab=0
# https://rico-schmidt.name/pymotw-3/pickle/index.html
# https://stackoverflow.com/questions/55809976/seek-on-pickled-data
# https://www.reddit.com/r/learnpython/comments/pgfj63/sorting_a_table_with_pysimplegui/
# https://www.geeksforgeeks.org/python-sorted-function/
# https://github.com/PySimpleGUI/PySimpleGUI/blob/master/DemoPrograms/Demo_Table_Element_Header_or_Cell_Clicks.py
# https://github.com/PySimpleGUI/PySimpleGUI/issues/5646
# https://docs.python.org/3/howto/sorting.html


# Import necessary modules
from VideoGame import *
from SerializeFile import *
import PySimpleGUI as sg
import re
import operator
import pandas as pd

# List that will store VideoGame objects read from the CSV file
lVideoGame = []

# Definition of regular expression patterns for validation
pattern_ID = r"\d{3}"
pattern_platform = r"^[A-Z]+$"
pattern_progress = r"\d+%$"

# Function to add a new video game to the list and save the data to a CSV file
def addVideoGame(l_VideoGame, t_VideogameInterfaz, oVideoGame, window):
    saveVideoGame('database.csv', oVideoGame)
    l_VideoGame.append(oVideoGame)  # Add the VideoGame object to the list
    t_VideogameInterfaz.append([oVideoGame.ID, oVideoGame.name, oVideoGame.platform, oVideoGame.hours, oVideoGame.progress,
                                oVideoGame.posFile, oVideoGame.erased])
    window['-Table-'].update(values=t_VideogameInterfaz)

# Function to delete a video game from the list and update the interface and CSV file
def delVideoGame(l_VideoGame, t_VideogameInterfaz, posinTable):
    # Read the CSV file and store the data in a DataFrame
    df = pd.read_csv('database.csv')

    # Find the row that has the same ID as the video game to be deleted
    mask = df['ID'] == t_VideogameInterfaz[posinTable][0]

    # If such a row is found, change the value of 'erase' to True
    df.loc[mask, 'erased'] = True

    # Save the DataFrame back to the CSV file
    df.to_csv('database.csv', index=False)

    # Update the list of video games in memory
    for o in l_VideoGame:
        if o.ID == t_VideogameInterfaz[posinTable][0]:
            o.erased = True
            break

    # Remove the video game from the interface's list
    t_VideogameInterfaz.remove(t_VideogameInterfaz[posinTable])

# Function to update a video game in the list and the CSV file
def updateVideoGame(l_VideoGame, t_row_VideogameInterfaz, posinFile):
    # Read the CSV file and store the data in a DataFrame
    df = pd.read_csv('database.csv')

    # Convert the ID to string before comparison
    game_id = str(t_row_VideogameInterfaz[0])
    df['ID'] = df['ID'].astype(str)

    # Find the row that has the same ID as the video game to be updated
    mask = df['ID'] == game_id

    # If such a row is found, update the values of that row with the new values of the video game
    if df.loc[mask].shape[0] > 0:
        df.loc[mask, 'name'] = t_row_VideogameInterfaz[1]
        df.loc[mask, 'platform'] = t_row_VideogameInterfaz[2]
        df.loc[mask, 'hours'] = t_row_VideogameInterfaz[3]
        df.loc[mask, 'progress'] = t_row_VideogameInterfaz[4]

        print(df)
        # Save the DataFrame back to the CSV file
        df.to_csv('database.csv', index=False)

        # Update the list of video games in memory
        for o in l_VideoGame:
            if o.ID == game_id:
                o.setName(t_row_VideogameInterfaz[1])
                o.setPlatform(t_row_VideogameInterfaz[2])
                o.setHours(t_row_VideogameInterfaz[3])
                o.setProgress(t_row_VideogameInterfaz[4])
                o.erased = False  # Make sure the 'erased' state is set to False
                break
    else:
        print("Error: No video game with the provided ID was found.")

# Function to handle the event of adding a video game
def handle_add_event(event, values, l_VideoGame, table_data, window):
    valid = False
    if re.match(pattern_platform, values['-Platform-']):
        if re.match(pattern_ID, values['-ID-']):
            if re.match(pattern_progress, values['-Progress-']):
                valid = True
    if valid:
        addVideoGame(l_VideoGame, table_data,
                     VideoGame(values['-ID-'], values['-Name-'], values['-Platform-'], values['-Hours-'],
                               values['-Progress-'], -1), window)
        window['-Table-'].update(table_data)

# Function to handle the event of deleting a video game
def handle_delete_event(event, values, l_VideoGame, table_data, window):
    if len(values['-Table-']) > 0:
        delVideoGame(l_VideoGame, table_data, values['-Table-'][0])
        window['-Table-'].update(table_data)

# Function to handle the event of modifying a video game
def handle_modify_event(event, values, l_VideoGame, table_data, window):
    valid = False
    if re.match(pattern_platform, values['-Platform-']):
        if re.match(pattern_ID, values['-ID-']):
            if re.match(pattern_progress, values['-Progress-']):
                valid = True
    if valid:
        row_to_update = None
        for t in table_data:
            if str(t[0]) == values['-ID-']:
                row_to_update = t
                t[1], t[2], t[3], t[4] = values['-Name-'], values['-Platform-'], values['-Hours-'], values['-Progress-']
                break
        if row_to_update is None:
            print("Error: No video game with the provided ID was found in the event.")
            return
        updateVideoGame(l_VideoGame, row_to_update, int(values['-PosFile-']))
        window['-Table-'].update(table_data)
        window['-ID-'].update(disabled=False)

# Function to sort the table by multiple columns
def sort_table(table, cols):
    for col in reversed(cols):
        try:
            table = sorted(table, key=operator.itemgetter(col))
        except Exception as e:
            sg.popup_error('Error in sort_table', 'Exception in sort_table', e)
    return table

# Main function that defines the graphical interface and handles events
def interface():
    font1, font2 = ('Arial', 14), ('Arial', 16)
    sg.theme('Purple')
    sg.set_options(font=font1)
    table_data=[]
    row_to_update = []
    l_VideoGame = readVideoGame('database.csv')
    # Fill the data list for the table
    for o in l_VideoGame:
        table_data.append([o.ID, o.name, o.platform, o.hours, o.progress, o.posFile, o.erased])

    # Definition of the interface layout
    layout = [
                 [sg.Push(), sg.Text('My VideoGame Library'), sg.Push()]] + [
                 [sg.Text(text), sg.Push(), sg.Input(key=key)] for key, text in VideoGame.fields.items()] + [
                 [sg.Push()] +
                 [sg.Button(button) for button in ('Add', 'Delete','Modify','Clear')] +
                 [sg.Push()],
                 [sg.Table(values=table_data, headings=VideoGame.headings, max_col_width=50, num_rows=10,
                           display_row_numbers=False, justification='center', enable_events=True, enable_click_events=True,
                           vertical_scroll_only=False, select_mode=sg.TABLE_SELECT_MODE_BROWSE,
                           expand_x=True,bind_return_key=True, key='-Table-')],
                 [sg.Button('Purge'), sg.Push(),sg.Button('Sort File')],
                 ]
    sg.theme('DarkBlue4')
    # Create the PySimpleGUI window
    window = sg.Window('My VideoGame Library', layout, finalize=True)

    window['-Table-'].bind("<Double-Button-1>", " Double")

    # Main loop to handle interface events
    while True:
        event, values = window.read()

        # Handle the event of closing the window
        if event == sg.WIN_CLOSED:
            break

        # Handle the event of adding a video game
        if event == 'Add':
            handle_add_event(event, values, l_VideoGame, table_data, window)

        # Handle the event of deleting a video game
        if event == 'Delete':
            handle_delete_event(event, values, l_VideoGame, table_data, window)

        # Handle the event of double-clicking on the table
        if event == '-Table- Double':
            if len(values['-Table-']) > 0:
                row = values['-Table-'][0]
                window['-ID-'].update(disabled=True)
                window['-ID-'].update(str(table_data[row][0]))
                window['-Name-'].update(str(table_data[row][1]))
                window['-Platform-'].update(str(table_data[row][2]))
                window['-Hours-'].update(str(table_data[row][3]))
                window['-Progress-'].update(str(table_data[row][4]))
                window['-PosFile-'].update(str(table_data[row][5]))

        # Handle the event of clearing fields
        if event == 'Clear':
            window['-ID-'].update(disabled=False)
            window['-ID-'].update('')
            window['-Name-'].update('')
            window['-Platform-'].update('')
            window['-Hours-'].update('')
            window['-Progress-'].update('')
            window['-PosFile-'].update('')

        # Handle the event of modifying a video game
        if event == 'Modify':
            handle_modify_event(event, values, l_VideoGame, table_data, window)

        # Handle the event of clicking on the table to sort
        if isinstance(event, tuple):
            if event[0] == '-Table-':
                if event[2][0] == -1:  # Header was clicked
                    col_num_clicked = event[2][1]
                    table_data = sort_table(table_data, (col_num_clicked, 0))
                    window['-Table-'].update(table_data)

    # Close the window when exiting the loop
    window.close()

# Call the main function
interface()

# Close the file at the end of the program
