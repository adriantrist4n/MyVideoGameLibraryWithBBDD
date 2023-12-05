class VideoGame:
    # Class variables
    headings = ['ID', 'Name', 'Platform', 'Hours', 'Progress']
    fields = {
        '-id-': 'VideoGame ID:',
        '-name-': 'VideoGame Name:',
        '-platform-': 'Platform:',
        '-hours-': 'Hours:',
        '-progress-': 'Progress:'
    }

    # Constructor method
    def __init__(self, id, name, platform, hours, progress, erased=False):
        # Instance attributes
        self.id = id
        self.name = name
        self.platform = platform
        self.hours = hours
        self.progress = progress
        self.erased = erased

    # Equality comparison method
    def __eq__(self, other):
        return other.id == self.id  # Adjust the comparison based on your needs

    # String representation method
    def __str__(self):
        return (
            f"ID: {self.id}, Name: {self.name}, Platform: {self.platform}, "
            f"Hours: {self.hours}, Progress: {self.progress}"
        )

    # Method to check if the video game is in a specific position
    def video_game_in_pos(self, pos):
        return False  # No pos_file attribute; adjust the logic accordingly

    # Method to set video game attributes
    def set_video_game(self, name, platform, hours, progress):
        self.name = name
        self.platform = platform
        self.hours = hours
        self.progress = progress

    # Method to set the name attribute
    def set_name(self, name):
        self.name = name

    # Method to set the platform attribute
    def set_platform(self, platform):
        self.platform = platform

    # Method to set the hours attribute
    def set_hours(self, hours):
        self.hours = hours

    # Method to set the progress attribute
    def set_progress(self, progress):
        self.progress = progress