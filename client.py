import glob
import shout
import threading

# icecast server settings
HOSTNAME = '127.0.0.1'
PORT = 8008
PASSWORD = 'password'
MOUNT = '/stream'
NAME = 'Radio XXX'
DESCRIPTION = 'Radio XXX cool music'
GENRE = 'new'
STATION_URL = 'radio.com'


class StreamClient(threading.Thread):
    def __init__(self, channel_mount, station_url, name, description, music_dir, genre, format_='mp3', ogv=0):
        # connection to icecast
        self.s = shout.Shout()
        self.s.mount = channel_mount
        self.s.url = station_url
        self.s.name = name
        self.s.description = description
        self.music_dir = music_dir
        self.s.audio_info = self.get_audio_info()
        self.s.genre = genre
        self.s.format = format_  # using mp3 but it can also be ogg vorbis
        self.ogv = ogv
        self.s.port = PORT
        self.s.password = PASSWORD
        self.s.host = HOSTNAME
        self.file_list = []
        self.current_song_name = ''
        self.s.open()
        threading.Thread.__init__(self)

    @staticmethod
    def get_audio_info():
        return {
            shout.SHOUT_AI_BITRATE: '128',
            shout.SHOUT_AI_SAMPLERATE: '44100',
            shout.SHOUT_AI_CHANNELS: '5'
        }

    def get_audio_files(self):
        # getting files from folder and adding path to file list
        # rewrite this function to your requirement
        for file in glob.glob(f"{self.music_dir}/*.mp3"):
            self.file_list.append(file)

    @staticmethod
    def get_song_name(file_path):
        # getting file name from file path
        # 'home/Music/song.mp3' -> 'song'
        # rewrite this function to your requirement
        return file_path.split('/')[-1].split('.')[0]

    def sendfile(self, _file):
        with open(_file, 'rb') as f:
            self.s.set_metadata({'song': self.current_song_name})
            nbuf = f.read(4096)
            while True:
                buf = nbuf
                nbuf = f.read(4096)
                if len(buf) == 0:
                    break
                self.s.send(buf)
                self.s.sync()

    def _run(self):
        while True:
            for file in self.file_list:
                self.current_song_name = self.get_song_name(file)
                self.sendfile(file)

    def run(self):
        self._run()


music_directory = 'path/to/music/folder'

stream = StreamClient(
    channel_mount=MOUNT,
    station_url=STATION_URL,
    music_dir=music_directory,
    genre=GENRE,
    name=NAME,
    description=DESCRIPTION
)
stream.start()
