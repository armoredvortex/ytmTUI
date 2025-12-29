from textual.app import ComposeResult
from textual.widgets import Static
from textual.containers import Center, Middle

# Add ImageEnhance to imports
from PIL import Image, ImageEnhance
from rich.text import Text
from rich.style import Style
import requests
from io import BytesIO

class Art(Static):
    """Displays album art using high-res half-block rendering."""

    def compose(self) -> ComposeResult:
        with Middle():
            with Center():
                yield Static("Select a song", id="art-display", expand=True)

    def show_art(self, url: str):
        """Downloads image and renders it using half-blocks."""
        art_widget = self.query_one("#art-display", Static)
        
        if not url:
            art_widget.update("No art available.")
            return

        # Get size
        w = self.size.width
        h = self.size.height
        if w == 0: w = 40
        if h == 0: h = 20

        try:
            art_widget.update("Downloading...")
            
            response = requests.get(url)
            im = Image.open(BytesIO(response.content))
            im = im.convert("RGB")
            
            # --- IMPROVEMENT 1: Better Resizing ---
            # Calculate target dimensions
            target_width = w
            target_height = h * 2
            
            # Use LANCZOS for high-quality downsampling (smooths out jagged edges)
            im = im.resize((target_width, target_height), Image.Resampling.LANCZOS)
            
            # --- IMPROVEMENT 2: Sharpening ---
            # Terminal art can look muddy. Sharpening helps edges stand out.
            enhancer = ImageEnhance.Sharpness(im)
            im = enhancer.enhance(2.0) # 2.0 is double sharpness
            
            # Optional: Boost contrast slightly to make colors pop against dark terminals
            enhancer = ImageEnhance.Contrast(im)
            im = enhancer.enhance(1.2)

            # --- Rendering Loop (Same as before) ---
            rich_text = Text()
            pixels = im.load()
            
            for y in range(0, im.height, 2):
                for x in range(im.width):
                    r1, g1, b1 = pixels[x, y]
                    if y + 1 < im.height:
                        r2, g2, b2 = pixels[x, y + 1]
                    else:
                        r2, g2, b2 = (0, 0, 0)
                    
                    style = Style(color=f"rgb({r1},{g1},{b1})", bgcolor=f"rgb({r2},{g2},{b2})")
                    rich_text.append("▀", style=style)
                rich_text.append("\n")
            
            art_widget.update(rich_text)

        except Exception as e:
            art_widget.update(f"Error:\n{e}")