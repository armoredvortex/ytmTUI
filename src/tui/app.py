from textual.app import App, ComposeResult
from textual.widgets import Header, Footer
from textual.containers import Container, Horizontal

# Import your custom widgets
# Note: Ensure you run this from the parent directory using 'python -m tui.app'
# or adjust sys.path if running directly.
from src.tui.panes.browser import Browser
from src.tui.panes.art import Art
from src.tui.panes.player import Player

class MusicApp(App):
    # Link to the external CSS file we will create in Step 3
    CSS_PATH = "music.tcss" 

    def compose(self) -> ComposeResult:
        yield Header()
        
        # Main container for the middle content
        with Container(id="app-grid"):
            
            # The top split holds Browser and Art side-by-side
            with Horizontal(id="top-split"):
                yield Browser(id="browser")
                yield Art(id="art")
            
            # The player sits below the top split
            yield Player(id="player")

        yield Footer()

if __name__ == "__main__":
    app = MusicApp()
    app.run()