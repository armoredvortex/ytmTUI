from textual.app import ComposeResult
from textual.widgets import Static, Input, DataTable
from textual.containers import Container

class Browser(Static):
    """Displays the search bar and list of songs."""
    
    def compose(self) -> ComposeResult:
        # Input box with placeholder text
        yield Input(placeholder="Search for a song...", id="search-box")
        
        # A table to display results (cursor_type="row" allows selecting whole rows)
        yield DataTable(id="results-table", cursor_type="row")

    def on_mount(self) -> None:
        """Called when the widget is added to the app."""
        table = self.query_one(DataTable)
        
        # Add visible columns: Title, Artist, Album
        table.add_columns("Title", "Artist", "Album")
        
        # NEW: Add a HIDDEN column to store the image URL.
        # Users won't see this, but we can retrieve the data later.
        table.add_column("InfoUrl", key="thumbnail_url")

    def on_input_submitted(self, event: Input.Submitted) -> None:
        """Triggered when user hits Enter in the search box."""
        query = event.value
        self.perform_search(query)

    def perform_search(self, query: str) -> None:
        table = self.query_one(DataTable)
        table.clear()
        
        # Access the backend via self.app
        results = self.app.backend.library.search(query)
        
        for song in results:
            # Extract data safely
            title = song.get('title', 'Unknown')
            artist = song['artists'][0]['name'] if song.get('artists') else "Unknown"
            album = song['album']['name'] if song.get('album') else "Single"
            video_id = song['videoId']

            # NEW: Extract Thumbnail URL
            # The API returns a list of sizes. The last one is usually the largest.
            thumbnails = song.get('thumbnails', [])
            thumb_url = thumbnails[-1]['url'] if thumbnails else ""

            # NEW: Add row including the hidden thumb_url as the 4th argument
            table.add_row(title, artist, album, thumb_url, key=video_id)

    def on_data_table_row_selected(self, event: DataTable.RowSelected) -> None:
        """Triggered when user clicks a row."""
        video_id = event.row_key.value
        
        # Get the row data (now includes the hidden URL)
        row_data = self.query_one(DataTable).get_row(event.row_key)
        
        title = row_data[0]
        artist = row_data[1]
        # Index 2 is Album
        thumb_url = row_data[3] # NEW: Retrieve the URL from the hidden 4th column

        # 1. Play audio
        self.app.backend.player.play(video_id)
        
        # 2. Update the Player UI pane
        self.app.query_one("Player").update_now_playing(title, artist)

        # 3. NEW: Update the Art pane
        # We find the widget by class name "Art" and call its method
        self.app.query_one("Art").show_art(thumb_url)