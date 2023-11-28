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
l_video_game = []

# Definition of regular expression patterns for validation
pattern_id = r"\d{3}"
pattern_platform = r"^[A-Z]+$"
pattern_progress = r"\d+%$"

# Function to add a new video game to the list and save the data to a CSV file
def add_video_game(l_video_game, t_video_game_interface, o_video_game, window):
    save_video_game('database.csv', o_video_game)
    l_video_game.append(o_video_game)  # Add the VideoGame object to the list
    o_video_game.pos_file = len(l_video_game) - 1
    t_video_game_interface.append([o_video_game.id, o_video_game.name, o_video_game.platform, o_video_game.hours, o_video_game.progress,
                                   o_video_game.pos_file, o_video_game.erased])
    window['-Table-'].update(values=t_video_game_interface)

# Function to delete a video game from the list and update the interface and CSV file
def del_video_game(l_video_game, t_video_game_interface, pos_in_table):
    # Read the CSV file and store the data in a DataFrame
    df = pd.read_csv('database.csv')

    # Find the row that has the same ID as the video game to be deleted
    mask = df['id'] == t_video_game_interface[pos_in_table][0]

    # If such a row is found, change the value of 'erased' to True
    df.loc[mask, 'erased'] = True

    # Save the DataFrame back to the CSV file
    df.to_csv('database.csv', index=False)

    # Update the list of video games in memory
    for o in l_video_game:
        if o.id == t_video_game_interface[pos_in_table][0]:
            o.erased = True
            break

    # Remove the video game from the interface's list
    t_video_game_interface.remove(t_video_game_interface[pos_in_table])

# Function to update a video game in the list and the CSV file
def update_video_game(l_video_game, t_row_video_game_interface, pos_in_file):
    # Read the CSV file and store the data in a DataFrame
    df = pd.read_csv('database.csv')

    # Convert the ID to string before comparison
    game_id = str(t_row_video_game_interface[0])
    df['id'] = df['id'].astype(str)

    # Find the row that has the same ID as the video game to be updated
    mask = df['id'] == game_id

    # If such a row is found, update the values of that row with the new values of the video game
    if df.loc[mask].shape[0] > 0:
        df.loc[mask, 'name'] = t_row_video_game_interface[1]
        df.loc[mask, 'platform'] = t_row_video_game_interface[2]
        df.loc[mask, 'hours'] = t_row_video_game_interface[3]
        df.loc[mask, 'progress'] = t_row_video_game_interface[4]

        print(df)
        # Save the DataFrame back to the CSV file
        df.to_csv('database.csv', index=False)

        # Update the list of video games in memory
        for o in l_video_game:
            if o.id == game_id:
                o.set_name(t_row_video_game_interface[1])
                o.set_platform(t_row_video_game_interface[2])
                o.set_hours(t_row_video_game_interface[3])
                o.set_progress(t_row_video_game_interface[4])
                o.erased = False  # Make sure the 'erased' state is set to False
                break
    else:
        print("Error: No video game with the provided ID was found.")

# Function to handle the event of adding a video game
def handle_add_event(event, values, l_video_game, table_data, window):
    valid = False
    if re.match(pattern_platform, values['-platform-']):
        if re.match(pattern_id, values['-id-']):
            if re.match(pattern_progress, values['-progress-']):
                valid = True
    if valid:
        add_video_game(l_video_game, table_data,
                     VideoGame(values['-id-'], values['-name-'], values['-platform-'], values['-hours-'],
                               values['-progress-'], -1), window)
        window['-Table-'].update(table_data)

# Function to handle the event of deleting a video game
def handle_delete_event(event, values, l_video_game, table_data, window):
    if len(values['-Table-']) > 0:
        del_video_game(l_video_game, table_data, values['-Table-'][0])
        window['-Table-'].update(table_data)

# Function to handle the event of modifying a video game
def handle_modify_event(event, values, l_video_game, table_data, window):
    valid = False
    if re.match(pattern_platform, values['-platform-']):
        if re.match(pattern_id, values['-id-']):
            if re.match(pattern_progress, values['-progress-']):
                valid = True
    if valid:
        row_to_update = None
        for t in table_data:
            if str(t[0]) == values['-id-']:
                row_to_update = t
                t[1], t[2], t[3], t[4] = values['-name-'], values['-platform-'], values['-hours-'], values['-progress-']
                break
        if row_to_update is None:
            print("Error: No video game with the provided ID was found in the event.")
            return
        update_video_game(l_video_game, row_to_update, int(values['-pos_file-']))
        window['-Table-'].update(table_data)
        window['-id-'].update(disabled=False)

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
    table_data = []
    row_to_update = []
    l_video_game = read_video_game('database.csv')

    # Fill the data list for the table
    for o in l_video_game:
        table_data.append([o.id, o.name, o.platform, o.hours, o.progress, o.pos_file, o.erased])

    # Definition of the interface layout
    input_layout = [
        [sg.Text(text), sg.Input(key=key)] for key, text in VideoGame.fields.items()
    ]

    button_layout = [
        sg.Button(button) for button in ('Add', 'Delete', 'Modify', 'Clear')
    ]

    # Organize the elements in columns
    left_column = [
        [sg.Text('My VideoGame Library')],
        *input_layout,
        button_layout
    ]

    right_column = [
        [sg.Table(values=table_data, headings=VideoGame.headings, max_col_width=50, num_rows=10,
                  display_row_numbers=False, justification='center', enable_events=True,
                  enable_click_events=True,
                  vertical_scroll_only=False, select_mode=sg.TABLE_SELECT_MODE_BROWSE,
                  expand_x=True, bind_return_key=True, key='-Table-')],
        [sg.Button('Purge'), sg.Button('Sort File')],
    ]

    layout = [
        [
            sg.Column(left_column),
            sg.Column(right_column),
        ],
    ]

    sg.theme('DarkBlue4')

    # Define the size of the window
    window_size = (1250, 350)

    # Create the PySimpleGUI window
    window = sg.Window('My VideoGame Library', layout, size=window_size, finalize=True)

    # Binds the event for double-clicking on the table
    window['-Table-'].bind("<Double-Button-1>", " Double")

    # Main loop to handle interface events
    while True:
        event, values = window.read()

        if event == sg.WINDOW_CLOSED:
            break

        # Handle the event of adding a video game
        if event == 'Add':
            handle_add_event(event, values, l_video_game, table_data, window)

        # Handle the event of deleting a video game
        if event == 'Delete':
            handle_delete_event(event, values, l_video_game, table_data, window)

        # Handle the event of double-clicking on the table
        if event == '-Table- Double':
            if len(values['-Table-']) > 0:
                row = values['-Table-'][0]
                window['-id-'].update(disabled=True)
                window['-id-'].update(str(table_data[row][0]))
                window['-name-'].update(str(table_data[row][1]))
                window['-platform-'].update(str(table_data[row][2]))
                window['-hours-'].update(str(table_data[row][3]))
                window['-progress-'].update(str(table_data[row][4]))
                window['-pos_file-'].update(str(table_data[row][5]))

        # Handle the event of clearing fields
        if event == 'Clear':
            window['-id-'].update(disabled=False)
            window['-id-'].update('')
            window['-name-'].update('')
            window['-platform-'].update('')
            window['-hours-'].update('')
            window['-progress-'].update('')
            window['-pos_file-'].update('')

        # Handle the event of modifying a video game
        if event == 'Modify':
            handle_modify_event(event, values, l_video_game, table_data, window)

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
