#https://apuntes.de/python/expresiones-regulares-y-busqueda-de-patrones-en-python-poder-y-flexibilidad/#gsc.tab=0
#https://rico-schmidt.name/pymotw-3/pickle/index.html
#https://stackoverflow.com/questions/55809976/seek-on-pickled-data
#https://www.reddit.com/r/learnpython/comments/pgfj63/sorting_a_table_with_pysimplegui/
#https://www.geeksforgeeks.org/python-sorted-function/
#https://github.com/PySimpleGUI/PySimpleGUI/blob/master/DemoPrograms/Demo_Table_Element_Header_or_Cell_Clicks.py
#https://github.com/PySimpleGUI/PySimpleGUI/issues/5646
#https://docs.python.org/3/howto/sorting.html



from SerializeFile import *
from VideoGame import *
import PySimpleGUI as sg
import re
import operator


fVideoGame = 'database.csv'
lVideoGame=[]
pattern_platform = r"^[A-Z]+$" # The 'platform' field only accepts uppercase letters.
pattern_ID = r"\d{3}"
pattern_progress = r"\d+%$" # The 'progress' field only accepts one or more digits followed by a percentage symbol at the end

def addVideoGame(l_VideoGame, t_VideogameInterfaz, oVideoGame, window):
    l_VideoGame.append(oVideoGame)
    oVideoGame.posFile = len(l_VideoGame) - 1
    saveVideoGame(fVideoGame, oVideoGame)
    new_row = [oVideoGame.ID, oVideoGame.name, oVideoGame.platform, oVideoGame.hours, oVideoGame.progress, oVideoGame.posFile]
    t_VideogameInterfaz.append(new_row)
    window['-Table-'].update(values=t_VideogameInterfaz)


#def delVideoGame(l_VideoGame, t_VideogameInterfaz, posinTable):


#def updateVideoGame(l_VideoGame,t_row_VideogameInterfaz, posinFile):


def sort_table(table, cols):
    """ sort a table by multiple columns
        table: a list of lists (or tuple of tuples) where each inner list
               represents a row
        cols:  a list (or tuple) specifying the column numbers to sort by
               e.g. (1,0) would sort by column 1, then by column 0
    """
    for col in reversed(cols):
        try:
            table = sorted(table, key=operator.itemgetter(col))
        except Exception as e:
            sg.popup_error('Error in sort_table', 'Exception in sort_table', e)
    return table
def interfaz():
    global window
    font1, font2 = ('Arial', 14), ('Arial', 16)
    sg.theme('Purple')
    sg.set_options(font=font1)
    table_data=[]
    rowToUpdate = []
    readVideoGame(fVideoGame, lVideoGame)
    for o in lVideoGame:
        if (not o.erased):
            table_data.append([o.ID, o.name, o.platform, o.hours, o.progress, o.posFile])


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
    window = sg.Window('My VideoGame Library', layout,finalize=True)
    window['-Table-'].update(values=table_data)
    window['-PosFile-'].update(disabled=True)
    window['-Table-'].bind("<Double-Button-1>", " Double")
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
          break
        if event == 'Add':
            valida=False
            if re.match(pattern_platform, values['-Platform-']):
                if re.match(pattern_ID, values['-ID-']):
                    if re.match(pattern_progress, values['-Progress-']):
                        valida=True
            if (valida):
                addVideoGame(lVideoGame, table_data, VideoGame(values['-ID-'], values['-Name-'], values['-Platform-'], values['-Hours-'], values['-Progress-'], -1), window)
                window['-Table-'].update(table_data)

        if (event == '-Table- Double'):
            if len(values['-Table-']) > 0:
                row=values['-Table-'][0]
                window['-ID-'].update(disabled=True)
                window['-ID-'].update(str(table_data[row][0]))
                window['-Name-'].update(str(table_data[row][1]))
                window['-Platform-'].update(str(table_data[row][2]))
                window['-Hours-'].update(str(table_data[row][3]))
                window['-Progress-'].update(str(table_data[row][4]))
                window['-PosFile-'].update(str(table_data[row][5]))
            pass
        if event == 'Clear':
            window['-ID-'].update(disabled=False)
            window['-ID-'].update('')
            window['-Name-'].update('')
            window['-Platform-'].update('')
            window['-Hours-'].update('')
            window['-Progress-'].update('')
            window['-PosFile-'].update('')
        # TABLE CLICKED Event has value in format ('-TABLE=', '+CLICKED+', (row,col))
        # You can also call Table.get_last_clicked_position to get the cell clicked
            if event[0] == '-Table-':
                if event[2][0] == -1:  # Header was clicked
                    col_num_clicked = event[2][1]
                    table_data = sort_table(table_data, (col_num_clicked, 0))
                    window['-Table-'].update(table_data)

    window.close()

interfaz()
