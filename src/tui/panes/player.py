from textual.widgets import Static

class Player(Static):
    """Displays player controls (play, pause, seek)."""
    def compose(self):
        yield Static("Player Controls")