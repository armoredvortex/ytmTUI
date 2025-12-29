from ytmusicapi import YTMusic

class MusicLibrary:
    def __init__(self):
        # We can expand this later with auth headers if needed
        self.yt = YTMusic()

    def search(self, query: str, limit: int = 10):
        """Searches for songs on YouTube Music."""
        try:
            results = self.yt.search(query, filter="songs", limit=limit)
            return results
        except Exception as e:
            print(f"Error searching: {e}")
            return []

    def get_song_details(self, video_id: str):
        """Fetches detailed info about a specific song."""
        return self.yt.get_song(video_id)