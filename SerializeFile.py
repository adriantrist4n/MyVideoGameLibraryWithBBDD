from VideoGame import VideoGame  # Make sure to import the appropriate VideoGame class
import pandas as pd

def save_video_game(csv_filename, video_game):
    # Create a Pandas DataFrame from the VideoGame object
    video_game_data = {
        "id": [video_game.id],
        "name": [video_game.name],
        "platform": [video_game.platform],
        "hours": [video_game.hours],
        "progress": [video_game.progress],
        "erased": [video_game.erased]
    }
    df = pd.DataFrame(video_game_data)

    # 'a' mode to append to the end of the file if it already exists
    df.to_csv(csv_filename, mode='a', index=False, header=not pd.io.common.file_exists(csv_filename))

def modify_video_game(csv_filename, video_game):
    # Read the CSV file into a DataFrame
    df = pd.read_csv(csv_filename)

    # Identify the row corresponding to the VideoGame ID
    mask = df['id'] == video_game.id

    # Update the values in the identified row
    df.loc[mask, ['id', 'name', 'platform', 'hours', 'progress']] = [video_game.id, video_game.name, video_game.platform, video_game.hours, video_game.progress]

    # Save the updated DataFrame back to the CSV file
    df.to_csv(csv_filename, index=False)

def read_video_game(csv_filename):
    try:
        df = pd.read_csv(csv_filename)
    except FileNotFoundError:
        print(f"Error: The file {csv_filename} was not found.")
        return []

    if df is None or df.empty:
        print("Warning: The DataFrame is empty.")
        return []

    video_game_list = []
    expected_columns = ['id', 'name', 'platform', 'hours', 'progress', 'erased']

    # Check the existence of expected columns
    missing_columns = [col for col in expected_columns if col not in df.columns]
    if missing_columns:
        print(f"Error: The following columns were not found in the CSV file: {missing_columns}")
        return []

    for index, row in df.iterrows():
        if row['erased'] is False:  # Only add to the list if 'erased' is False
            video_game_list.append(VideoGame(row['id'], row['name'], row['platform'], row['hours'], row['progress'], row['erased']))

    return video_game_list
