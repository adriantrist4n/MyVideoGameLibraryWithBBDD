class VideoGame:
    # Class variables
    headings = ['ID', 'Name', 'Platform', 'Hours', 'Progress']
    fields = {
        '-id-': 'VideoGame ID:',
        '-name-': 'VideoGame Name:',
        '-platform-': 'Platform:',
        '-hours-': 'Hours:',
        '-progress-': 'Progress:',
        '-pos_file-': 'Position into File'
    }

    # Constructor method
    def __init__(self, id, name, platform, hours, progress, pos_file, erased=False):
        # Instance attributes
        self.id = id
        self.name = name
        self.platform = platform
        self.hours = hours
        self.progress = progress
        self.pos_file = pos_file
        self.erased = erased

    # Equality comparison method
    def __eq__(self, other):
        return other.pos_file == self.pos_file

    # String representation method
    def __str__(self):
        return (
                str(self.id) + str(self.name) + str(self.platform) +
                str(self.hours) + str(self.progress) + str(self.pos_file)
        )

    # Method to check if the video game is in a specific position
    def video_game_in_pos(self, pos):
        return self.pos_file == pos

    # Method to set video game attributes
    def set_video_game(self, name, platform, hours, progress):
        self.name = name
        self.platform = platform
        self.hours = hours
        self.progress = progress
