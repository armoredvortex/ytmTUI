from textual.widgets import Static

class Art(Static):
    """Displays album art."""
    def compose(self):
        yield Static("Album Art")