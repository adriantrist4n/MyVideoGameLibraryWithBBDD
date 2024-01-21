from VideoGame import VideoGame  # Make sure to import the appropriate VideoGame class
import mysql.connector

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="1234",
        database="video_game_db"
    )

def save_video_game(video_game):
    conn = get_db_connection()
    cursor = conn.cursor()
    query = "INSERT INTO video_games (id, name, platform, hours, progress, erased) VALUES (%s, %s, %s, %s, %s, %s)"
    cursor.execute(query, (video_game.id, video_game.name, video_game.platform, video_game.hours, video_game.progress, video_game.erased))
    conn.commit()
    cursor.close()
    conn.close()

def modify_video_game(video_game):
    conn = get_db_connection()
    cursor = conn.cursor()
    query = "UPDATE video_games SET name=%s, platform=%s, hours=%s, progress=%s WHERE id=%s"
    cursor.execute(query, (video_game.name, video_game.platform, video_game.hours, video_game.progress, video_game.id))
    conn.commit()
    cursor.close()
    conn.close()

def read_video_game():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    query = "SELECT * FROM video_games WHERE erased = FALSE"
    cursor.execute(query)
    video_game_list = cursor.fetchall()
    cursor.close()
    conn.close()
    return [VideoGame(**game) for game in video_game_list]
