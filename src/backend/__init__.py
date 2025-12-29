from .api import MusicLibrary
from .player import AudioPlayer
from .queue import QueueManager

class MusicBackend:
    def __init__(self):
        self.library = MusicLibrary()
        self.player = AudioPlayer()
        # Initialize queue with library so it can fetch recommendations
        self.queue = QueueManager(self.library)

    def play_song(self, video_id: str):
        """
        Called when user manually selects a song.
        Resets the queue and starts a fresh session.
        """
        self.player.stop()
        self.queue.clear()
        
        # Add the seed track. We minimally need the videoId.
        # The TUI can pass more data if available, but this is safe.
        self.queue.add_track({"videoId": video_id})
        
        # Start playing
        self.next()

    def next(self):
        """Plays the next track (or triggers autoplay)."""
        track = self.queue.advance()
        if track:
            self.player.play(track['videoId'])
            return track
        else:
            self.player.stop()
            return None

    def search_and_play(self, query: str):
        """Kept for backward compatibility."""
        results = self.library.search(query, limit=1)
        if results:
            self.play_song(results[0]['videoId'])