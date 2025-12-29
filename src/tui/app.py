from textual.app import App, ComposeResult
from textual.widgets import Header, Footer
from textual.containers import Container, Horizontal

# Import your backend
from src.backend import MusicBackend

from src.tui.panes.browser import Browser
from src.tui.panes.art import Art
from src.tui.panes.player import Player

class MusicApp(App):
    CSS_PATH = "music.tcss" 

    def __init__(self):
        super().__init__()
        # Initialize the backend library and player
        self.backend = MusicBackend()

    def compose(self) -> ComposeResult:
        yield Header()
        with Container(id="app-grid"):
            with Horizontal(id="top-split"):
                # Pass id="browser" so we can style it
                yield Browser(id="browser")
                yield Art(id="art")
            yield Player(id="player")
        yield Footer()

if __name__ == "__main__":
    app = MusicApp()
    app.run()