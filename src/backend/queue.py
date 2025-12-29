class QueueManager:
    def __init__(self, library):
        self.library = library
        self.queue = []         # List of song dictionaries
        self.current_index = -1 

    def clear(self):
        self.queue = []
        self.current_index = -1

    def add_track(self, track: dict):
        self.queue.append(track)

    def get_current_track(self):
        if 0 <= self.current_index < len(self.queue):
            return self.queue[self.current_index]
        return None

    def advance(self):
        """Moves to the next song. Auto-fetches if at end."""
        # 1. Try to move to the next existing song
        if self.current_index + 1 < len(self.queue):
            self.current_index += 1
            return self.queue[self.current_index]

        # 2. If end of queue, fetch recommendations (Autoplay)
        print("Queue finished. Fetching recommendations...")
        last_track = self.get_current_track()
        
        if not last_track:
            return None

        # Fetch 5 new songs based on the last one
        recommendations = self.library.get_watch_next(last_track['videoId'])
        
        for track in recommendations:
            # Avoid adding the exact same song twice in a row
            if track['videoId'] != last_track['videoId']:
                self.queue.append(track)

        # 3. Try advancing again
        if self.current_index + 1 < len(self.queue):
            self.current_index += 1
            return self.queue[self.current_index]
            
        return None