from VideoGame import VideoGame  # Make sure to import the appropriate VideoGame class
import mysql.connector

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="1388",
        database="video_game_db"
    )

def read_video_games_from_db():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    query = "SELECT * FROM video_games WHERE erased = FALSE"
    cursor.execute(query)
    video_game_list = cursor.fetchall()
    cursor.close()
    conn.close()
    return [VideoGame(**game) for game in video_game_list]

def add_video_game(l_video_game, t_video_game_interface, o_video_game, window):
    conn = get_db_connection()
    cursor = conn.cursor()
    query = """
    INSERT INTO video_games (name, platform, hours, progress, erased)
    VALUES (%s, %s, %s, %s, %s)
    """
    cursor.execute(query, (o_video_game.name, o_video_game.platform, o_video_game.hours, o_video_game.progress, o_video_game.erased))
    conn.commit()

    o_video_game.id = cursor.lastrowid  # Establecer el id generado al objeto
    l_video_game.append(o_video_game)

    # No necesitas modificar nada aquí, asumiendo que t_video_game_interface puede manejar el objeto correctamente
    t_video_game_interface.append([o_video_game.id, o_video_game.name, o_video_game.platform, o_video_game.hours, o_video_game.progress, o_video_game.erased])
    window['-Table-'].update(values=t_video_game_interface)

    cursor.close()
    conn.close()


def del_video_game(l_video_game, t_video_game_interface, pos_in_table, window):
    game_id = t_video_game_interface[pos_in_table][0]
    conn = get_db_connection()
    cursor = conn.cursor()
    query = "UPDATE video_games SET erased = TRUE WHERE id = %s"
    cursor.execute(query, (game_id,))
    conn.commit()

    for o in l_video_game:
        if o.id == game_id:
            o.erased = True
            break
    t_video_game_interface.remove(t_video_game_interface[pos_in_table])
    window['-Table-'].update(values=t_video_game_interface)

    cursor.close()
    conn.close()


def update_video_game(id, name, platform, hours, progress):
    conn = get_db_connection()
    cursor = conn.cursor()
    query = """
    UPDATE video_games
    SET name = %s, platform = %s, hours = %s, progress = %s
    WHERE id = %s
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