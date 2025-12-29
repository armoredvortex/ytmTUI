from textual.app import ComposeResult
from textual.widgets import Static, Button, Label
from textual.containers import Center, Horizontal

class Player(Static):
    """Displays player controls and track info."""

    def compose(self) -> ComposeResult:
        # We use a Center container to keep everything in the middle
        with Center():
            yield Label("Not Playing", id="track-info")
        
        with Center():
            with Horizontal(id="controls"):
                # "variant" gives us different colors (default, primary, success, warning, error)
                yield Button("Pause", id="pause-btn", variant="primary") 
                yield Button("Stop", id="stop-btn", variant="error")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button clicks."""
        button_id = event.button.id
        player = self.app.backend.player
        
        if button_id == "pause-btn":
            player.toggle_pause()
        elif button_id == "stop-btn":
            player.stop()
            self.update_now_playing("Stopped", "")

    def update_now_playing(self, title: str, artist: str):
        """Updates the text label with the current song."""
        label = self.query_one("#track-info", Label)
        label.update(f"Now Playing: {title} • {artist}")