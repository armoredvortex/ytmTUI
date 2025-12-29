import mpv
import locale

class AudioPlayer:
    def __init__(self):
        # ytdl=True: Enables streaming via yt-dlp
        # vo="null": We don't need video output for a music player
        locale.setlocale(locale.LC_NUMERIC, "C")
        self.mpv = mpv.MPV(ytdl=True, vo="null")

    def play(self, video_id: str):
        """Plays a track given its YouTube Video ID."""
        url = f"https://music.youtube.com/watch?v={video_id}"
        self.mpv.play(url)
        self.mpv.pause = False

    def stop(self):
        """Stops playback."""
        self.mpv.stop()

    def toggle_pause(self):
        """Toggles between play and pause."""
        self.mpv.pause = not self.mpv.pause

    @property
    def is_playing(self):
        return not self.mpv.pause and self.mpv.core_idle is False
    
    @property
    def current_time(self):
        return self.mpv.time_pos or 0
    
    @property
    def total_duration(self):
        return self.mpv.duration or 0
    
