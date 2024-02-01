from SerializeFile import *
import PySimpleGUI as sg
import operator

l_video_game = []

def handle_add_event(values, l_video_game, table_data, window):
    name = values['-name-']
    platform = values['-platform-']
    hours = values['-hours-']
    progress = values['-progress-']

    o_video_game = VideoGame(name=name, platform=platform, hours=hours, progress=progress, erased=False)
    add_video_game(l_video_game, table_data, o_video_game, window)
    window['-Table-'].update(table_data)



def handle_delete_event(values, l_video_game, table_data, window):
    if len(values['-Table-']) > 0:
        del_video_game(l_video_game, table_data, values['-Table-'][0], window)
        window['-Table-'].update(table_data)

def handle_modify_event(selected_row_index, values, l_video_game, table_data, window):
    if selected_row_index is not None:
        current_game = l_video_game[selected_row_index]

        update_video_game(current_game.id, values['-name-'], values['-platform-'], int(values['-hours-']), values['-progress-'])

        current_game.name = values['-name-']
        current_game.platform = values['-platform-']
        current_game.hours = int(values['-hours-'])
        current_game.progress = values['-progress-']

        table_data[selected_row_index] = [current_game.id, current_game.name, current_game.platform, current_game.hours, current_game.progress]
        window['-Table-'].update(values=table_data)
    else:
        sg.popup_error('Please select a game to modify.')


def sort_table(table, cols):
    for col in reversed(cols):
        try:
            table = sorted(table, key=operator.itemgetter(col))
        except Exception as e:
            sg.popup_error('Error in sort_table', 'Exception in sort_table', e)
    return table

def interface():
    sg.theme('DarkBlue')

    font1, font2 = ('Arial', 14), ('Arial', 16)
    sg.set_options(font=font1)
    l_video_game = read_video_games_from_db()

    table_data = [
        [o.id, o.name, o.platform, o.hours, o.progress, o.erased] for o in l_video_game
    ]

    platform_options = ['Play', 'Xbox', 'PC', 'Nintendo']

    input_layout = [
        [sg.Text('Name:', size=(15, 1)), sg.Input(key='-name-', size=(29, 1))],
        [sg.Text('Platform:', size=(15, 1)), sg.Combo(platform_options, key='-platform-', size=(28, 1))],
        [sg.Text('Hours:', size=(15, 1)), sg.Input(key='-hours-', size=(29, 1))],
        [sg.Text('Progress:', size=(15, 1)), sg.Slider(range=(0, 100), orientation='h', size=(25, 20), key='-progress-')]
    ]

    button_layout_row1 = [
        sg.Button('Add', size=(10, 1)),
        sg.Button('Delete', size=(10, 1)),
        sg.Button('Modify', size=(10, 1)),
        sg.Button('Clear', size=(10, 1)),
    ]

    button_layout_row2 = [
        sg.Button('Purge', size=(45, 1)),
    ]

    left_column = [
        [sg.Text('My VideoGame Library With BBDD', font=font2, justification='center', size=(35, 1))],
        *input_layout,
        button_layout_row1,
        button_layout_row2
    ]

    table_headings = [heading for heading in VideoGame.headings if heading != 'erased']

    right_column = [
        [sg.Table(values=table_data, headings=table_headings, max_col_width=70,
                  display_row_numbers=False, justification='center', enable_events=True,
                  enable_click_events=True,
                  vertical_scroll_only=False, select_mode=sg.TABLE_SELECT_MODE_BROWSE,
                  expand_x=True, bind_return_key=True, key='-Table-', auto_size_columns=True,
                  size=(900, 650))],
    ]

    layout = [
        [sg.Column(left_column), sg.Column(right_column)],
    ]

    window_size = (1050, 600)

    window = sg.Window('My VideoGame Library With BBDD', layout, size=window_size, finalize=True)

    window['-Table-'].bind("<Double-Button-1>", " Double")

    while True:
        event, values = window.read()

        if event == sg.WINDOW_CLOSED:
            break

        if event == 'Add':
            handle_add_event(values, l_video_game, table_data, window)

        if event == 'Delete':
            handle_delete_event(values, l_video_game, table_data, window)

        if event == '-Table- Double':
            if len(values['-Table-']) > 0:
                row = values['-Table-'][0]
                window['-name-'].update(str(table_data[row][1]))
                window['-platform-'].update(str(table_data[row][2]))
                window['-hours-'].update(str(table_data[row][3]))
                window['-progress-'].update(str(table_data[row][4]))

        if event == 'Clear':
            window['-name-'].update('')
            window['-platform-'].update('')
            window['-hours-'].update('')
            window['-progress-'].update(0)

        if event == 'Modify':
            selected_rows = values['-Table-']
            if selected_rows:
                selected_row_index = selected_rows[0]
                handle_modify_event(selected_row_index, values, l_video_game, table_data, window)
            else:
                sg.popup_error('Please select a game to modify.')

        if event == 'Purge':  # Asumiendo que 'Purge' es el texto o la clave del botón
            purge_erased_video_games()

        if isinstance(event, tuple):
            if event[0] == '-Table-':
                if event[2][0] == -1:
                    col_num_clicked = event[2][1]
                    table_data = sort_table(table_data, (col_num_clicked, 0))
                    window['-Table-'].update(table_data)

    window.close()

interface()