from ytmusicapi import YTMusic
import os

class MusicLibrary:
    def __init__(self):
        self.yt = YTMusic("../../browser.json")

    def search(self, query: str, limit: int = 10):
        try:
            results = self.yt.search(query, filter="songs", limit=limit)
            return results
        except Exception as e:
            print(f"Error searching: {e}")
            return []

    def get_song_details(self, video_id: str):
        return self.yt.get_song(video_id)
    
    def get_user_playlists(self):
        return self.yt.get_library_playlists()
    
    def get_playlist_items(self, playlist_id: str):
        return self.yt.get_playlist(playlist_id, limit=100)

    # --- NEW METHOD ---
    def get_watch_next(self, video_id: str):
        """
        Fetches the 'Up Next' list (recommendations) based on a video ID.
        Returns a list of track objects.
        """
        try:
            # get_watch_playlist returns a dict with 'tracks' and 'lyrics'
            # We only want the list of tracks.
            data = self.yt.get_watch_playlist(videoId=video_id, limit=5)
            return data.get('tracks', [])
        except Exception as e:
            print(f"Error fetching recommendations: {e}")
            return []