from textual.app import ComposeResult
from textual.widgets import Static, Input, DataTable
from textual.containers import Container

class Browser(Static):
    """Displays the search bar and list of songs."""

    # 1. Initialize a dictionary to hold hidden metadata
    thumbnails = {} 

    def compose(self) -> ComposeResult:
        yield Input(placeholder="Search for a song...", id="search-box")
        yield DataTable(id="results-table", cursor_type="row")

    def on_mount(self) -> None:
        table = self.query_one(DataTable)
        # 2. Only add the columns you actually want the user to SEE
        table.add_columns("Title", "Artist", "Album")

    def on_input_submitted(self, event: Input.Submitted) -> None:
        query = event.value
        self.perform_search(query)

    def perform_search(self, query: str) -> None:
        table = self.query_one(DataTable)
        table.clear()
        
        # Clear old metadata so memory doesn't grow forever
        self.thumbnails.clear() 
        
        results = self.app.backend.library.search(query)
        
        for song in results:
            title = song.get('title', 'Unknown')
            artist = song['artists'][0]['name'] if song.get('artists') else "Unknown"
            album = song['album']['name'] if song.get('album') else "Single"
            video_id = song['videoId']

            # Extract Thumbnail URL
            thumbnails = song.get('thumbnails', [])
            thumb_url = thumbnails[-1]['url'] if thumbnails else ""

            # 3. Store the hidden URL in our Python dictionary instead of the table
            self.thumbnails[video_id] = thumb_url

            # 4. Add row ONLY with visible data
            # Note: We still use key=video_id to link the row to our data
            table.add_row(title, artist, album, key=video_id)

    def on_data_table_row_selected(self, event: DataTable.RowSelected) -> None:
        video_id = event.row_key.value
        
        # Get visible data from the table
        row_data = self.query_one(DataTable).get_row(event.row_key)
        title = row_data[0]
        artist = row_data[1]

        # 5. Retrieve hidden URL from our dictionary using the key
        thumb_url = self.thumbnails.get(video_id, "")

        # Logic proceeds as normal...
        self.app.backend.player.play(video_id)
        self.app.query_one("Player").update_now_playing(title, artist)
        self.app.query_one("Art").show_art(thumb_url)