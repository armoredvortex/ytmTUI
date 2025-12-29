from textual.app import App, ComposeResult
from textual.widgets import Header, Footer
from textual.containers import Container, Horizontal

from src.backend import MusicBackend
from src.tui.panes.browser import Browser
from src.tui.panes.art import Art
from src.tui.panes.player import Player

class ytmTUI(App):
    CSS_PATH = "music.tcss" 

    def __init__(self):
        super().__init__()
        self.backend = MusicBackend()

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        
        with Container(id="app-grid"):
            # Browser takes top
            yield Browser(id="browser")

            # Split bottom: Player (Left) + Art (Right)
            with Horizontal(id="bottom-split"):
                yield Player(id="player")
                yield Art(id="art")
                
        yield Footer()

    def on_mount(self) -> None:
        self.title = "ytmTUI"

if __name__ == "__main__":
    app = ytmTUI()
    app.run()