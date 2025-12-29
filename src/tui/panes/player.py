from textual.app import ComposeResult
from textual.widgets import Static, Button, Label, ProgressBar
from textual.containers import Center, Horizontal, Container

class Player(Static):

    has_started = False

    """Displays player controls, track info, and progress."""

    def compose(self) -> ComposeResult:
        # 1. Track Info (Keep centered)
        with Center():
            yield Label("Not Playing", id="track-info")
        
        # 2. Progress Bar (REMOVE Center, use Container)
        # We give this a specific ID to force width: 100% in CSS
        with Container(id="progress-wrapper"):
            with Horizontal(id="progress-container"):
                yield Label("0:00", id="time-current")
                yield ProgressBar(total=100,show_eta=False, show_percentage=False, id="progress-bar")
                yield Label("0:00", id="time-total")

        # 3. Controls (Keep centered)
        with Center():
            with Horizontal(id="controls"):
                yield Button("Pause", id="pause-btn", variant="primary") 
                yield Button("Stop", id="stop-btn", variant="error")
    
    # ... (Keep the rest of your methods: on_mount, update_progress, format_time, on_button_pressed, update_now_playing) ...
    def on_mount(self) -> None:
        self.set_interval(0.5, self.update_progress)

    def update_progress(self) -> None:
        bar = self.query_one("#progress-bar", ProgressBar)
        lbl_current = self.query_one("#time-current", Label)
        lbl_total = self.query_one("#time-total", Label)
        
        player = self.app.backend.player

        current = player.current_time
        total = player.total_duration
        
        if current > 1.0:
            self.has_started = True

        if player.mpv.core_idle and not player.mpv.pause:
            if self.has_started:
                # Reset flag for the next song
                self.has_started = False 
                
                # Play next
                next_track = self.app.backend.next()
                if next_track:
                    title = next_track.get('title', 'Unknown')
                    artist = next_track.get('artists', [{'name': 'Unknown'}])[0]['name']
                    self.update_now_playing(title, artist)
                    # Note: You might want to clear the art or fetch new art here
                    return

        lbl_current.update(self.format_time(current))
        lbl_total.update(self.format_time(total))

        if total == 0:
            bar.update(total=100, progress=0)
        else:
            bar.update(total=total, progress=current)

    def format_time(self, seconds: float) -> str:
        if not seconds: return "0:00"
        m = int(seconds // 60)
        s = int(seconds % 60)
        return f"{m}:{s:02d}"

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