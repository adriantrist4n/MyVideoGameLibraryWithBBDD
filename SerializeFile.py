from VideoGame import VideoGame  # Make sure to import the appropriate VideoGame class
import pandas as pd

def saveVideoGame(csv_filename, video_game):
    # Create a Pandas DataFrame from the VideoGame object
    video_game_data = {
        "ID": [video_game.ID],
        "name": [video_game.name],
        "platform": [video_game.platform],
        "hours": [video_game.hours],
        "progress": [video_game.progress],
        "posFile": [video_game.posFile],
        "erased": [video_game.erased]
    }
    df = pd.DataFrame(video_game_data)

    # 'a' mode to append to the end of the file if it already exists
    df.to_csv(csv_filename, mode='a', index=False, header=not pd.io.common.file_exists(csv_filename))

def modifyVideoGame(csv_filename, video_game):
    df = pd.read_csv(csv_filename)
    mask = df['ID'] == video_game.ID
    df.loc[mask, ['ID', 'name', 'platform', 'hours', 'progress', 'posFile']] = [video_game.ID, video_game.name, video_game.platform, video_game.hours, video_game.progress, video_game.posFile]
    df.to_csv(csv_filename, index=False)

def readVideoGame(csv_filename):
    try:
        df = pd.read_csv(csv_filename)
    except FileNotFoundError:
        print(f"Error: The file {csv_filename} was not found.")
        return []

    if df is None or df.empty:
        print("Warning: The DataFrame is empty.")
        return []

    video_game_list = []
    expected_columns = ['ID', 'name', 'platform', 'hours', 'progress', 'posFile', 'erased']

    # Check the existence of expected columns
    missing_columns = [col for col in expected_columns if col not in df.columns]
    if missing_columns:
        print(f"Error: The following columns were not found in the CSV file: {missing_columns}")
        return []

    for index, row in df.iterrows():
        if row['erased'] == False:  # Only add to the list if 'erased' is False
            video_game_list.append(VideoGame(row['ID'], row['name'], row['platform'], row['hours'], row['progress'], row['posFile'], row['erased']))

    return video_game_list
