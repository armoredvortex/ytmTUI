from .api import MusicLibrary
from .player import AudioPlayer

class MusicBackend:
    def __init__(self):
        self.library = MusicLibrary()
        self.player = AudioPlayer()

    def search_and_play(self, query: str):
        """Helper to search for a song and play the first result immediately."""
        results = self.library.search(query, limit=1)
        if results:
            first_hit = results[0]
            print(f"Playing: {first_hit['title']} by {first_hit['artists'][0]['name']}")
            self.player.play(first_hit['videoId'])
            return first_hit
        return None