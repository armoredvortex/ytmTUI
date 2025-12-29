from textual.widgets import Static

class Browser(Static):
    """Displays the list of songs."""
    def compose(self):
        yield Static("Song Browser")