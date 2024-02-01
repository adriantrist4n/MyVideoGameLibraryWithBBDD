
from VideoGame import VideoGame  # Make sure to import the appropriate VideoGame class
import mysql.connector
import pyodbc


def get_db_connection():
        return pyodbc.connect(
            "DRIVER={MySQL ODBC 8.3 ANSI Driver}; SERVER=127.0.0.1;DATABASE=video_game_db; UID=root;PWD=1388;")


def read_video_games_from_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    query = "SELECT * FROM video_games WHERE erased = FALSE"
    cursor.execute(query)
    columns = [column[0] for column in cursor.description]
    video_game_list = [dict(zip(columns, row)) for row in cursor.fetchall()]
    cursor.close()
    conn.close()
    return [VideoGame(**game) for game in video_game_list]


def add_video_game(l_video_game, t_video_game_interface, o_video_game, window):
    conn = get_db_connection()
    cursor = conn.cursor()
    query = """
    INSERT INTO video_games (name, platform, hours, progress, erased)
    VALUES (?, ?, ?, ?, ?)
    """
    cursor.execute(query, (o_video_game.name, o_video_game.platform, o_video_game.hours, o_video_game.progress, o_video_game.erased))
    conn.commit()

    # Recuperar el último ID insertado
    cursor.execute("SELECT LAST_INSERT_ID()")
    last_id = cursor.fetchone()[0]
    o_video_game.id = last_id  # Establecer el ID generado al objeto

    l_video_game.append(o_video_game)
    t_video_game_interface.append([o_video_game.id, o_video_game.name, o_video_game.platform, o_video_game.hours, o_video_game.progress, o_video_game.erased])
    window['-Table-'].update(values=t_video_game_interface)

    cursor.close()
    conn.close()




def del_video_game(l_video_game, t_video_game_interface, pos_in_table, window):
    game_id = t_video_game_interface[pos_in_table][0]
    conn = get_db_connection()
    cursor = conn.cursor()
    query = "UPDATE video_games SET erased = TRUE WHERE id = ?"
    cursor.execute(query, (game_id,))
    conn.commit()

    # Actualizar el estado en la lista en memoria
    for o in l_video_game:
        if o.id == game_id:
            o.erased = True
            break
    # Actualizar la interfaz
    t_video_game_interface.remove(t_video_game_interface[pos_in_table])
    window['-Table-'].update(values=t_video_game_interface)

    cursor.close()
    conn.close()



def update_video_game(id, name, platform, hours, progress):
    conn = get_db_connection()
    cursor = conn.cursor()
    query = """
    UPDATE video_games
    SET name = ?, platform = ?, hours = ?, progress = ?
    WHERE id = ?
    """
    cursor.execute(query, (name, platform, hours, progress, id))
    conn.commit()
    cursor.close()
    conn.close()

def purge_erased_video_games():
    conn = get_db_connection()
    cursor = conn.cursor()
    query = "DELETE FROM video_games WHERE erased = TRUE"
    cursor.execute(query)
    conn.commit()

    print(f"{cursor.rowcount} video games purged.")

    cursor.close()
    conn.close()
