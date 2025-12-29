from textual.app import ComposeResult
from textual.widgets import Static, Button, Label, ProgressBar
from textual.containers import Center, Horizontal

class Player(Static):
    """Displays player controls, track info, and progress."""

    def compose(self) -> ComposeResult:
        with Center():
            yield Label("Not Playing", id="track-info")
        
        # New Layout: [Time] [Bar] [Time]
        with Center():
            with Horizontal(id="progress-container"):
                yield Label("0:00", id="time-current")
                yield ProgressBar(total=100, show_eta=False, show_percentage=False, id="progress-bar")
                yield Label("0:00", id="time-total")

        with Center():
            with Horizontal(id="controls"):
                yield Button("Pause", id="pause-btn", variant="primary") 
                yield Button("Stop", id="stop-btn", variant="error")

    def on_mount(self) -> None:
        self.set_interval(0.5, self.update_progress)

    def update_progress(self) -> None:
        bar = self.query_one("#progress-bar", ProgressBar)
        lbl_current = self.query_one("#time-current", Label)
        lbl_total = self.query_one("#time-total", Label)
        
        player = self.app.backend.player
        current = player.current_time
        total = player.total_duration

        # Update Labels
        lbl_current.update(self.format_time(current))
        lbl_total.update(self.format_time(total))

        # Update Bar
        if total == 0:
            bar.update(total=100, progress=0)
        else:
            bar.update(total=total, progress=current)

    def format_time(self, seconds: float) -> str:
        """Converts seconds to MM:SS format."""
        if not seconds: return "0:00"
        m = int(seconds // 60)
        s = int(seconds % 60)
        return f"{m}:{s:02d}"

    # ... existing on_button_pressed and update_now_playing ...
    def on_button_pressed(self, event: Button.Pressed) -> None:
        button_id = event.button.id
        player = self.app.backend.player
        if button_id == "pause-btn":
            player.toggle_pause()
        elif button_id == "stop-btn":
            player.stop()
            self.update_now_playing("Stopped", "")

    def update_now_playing(self, title: str, artist: str):
        label = self.query_one("#track-info", Label)
        label.update(f"Now Playing: {title} • {artist}")