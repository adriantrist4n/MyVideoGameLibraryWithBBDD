class VideoGame:
    headings = ['ID', 'Name', 'Platform', 'Hours', 'Progress']
    fields = {
        '-ID-': 'VideoGame ID:',
        '-Name-': 'VideoGame Name:',
        '-Platform-': 'Platform:',
        '-Hours-': 'Hours:',
        '-Progress-': 'Progress:',
        '-PosFile-': 'Position into File'
    }

    # El método __init__ es llamado al crear el objeto
    def __init__(self, ID, name, platform, hours, progress, posFile):
        # Atributos de instancia
        self.ID = ID
        self.name = name
        self.platform = platform
        self.hours = hours
        self.progress = progress
        self.posFile = posFile
        self.erased = False

    def __eq__(self, oC):
        return oC.posFile == self.posFile

    def __str__(self):
        return str(self.ID) + str(self.name) + str(self.platform) + str(self.hours) + str(self.progress) + str(
            self.posFile)

    def videoGameinPos(self, pos):
        return self.posFile == pos

    def setVideoGame(self, name, platform, hours, progress):
        self.name = name
        self.platform = platform
        self.hours = hours
        self.progress = progress
