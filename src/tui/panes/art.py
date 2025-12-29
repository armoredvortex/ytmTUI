from textual.app import ComposeResult
from textual.widgets import Static
from textual.containers import Center, Middle

from PIL import Image, ImageEnhance
from rich.text import Text
from rich.style import Style
import requests
from io import BytesIO

class Art(Static):
    def compose(self) -> ComposeResult:
        with Middle():
            with Center():
                yield Static("No Art", id="art-display")

    def show_art(self, url: str):
        art_widget = self.query_one("#art-display", Static)
        
        if not url:
            art_widget.update("No URL")
            return

        try:
            art_widget.update("...") 
            
            response = requests.get(url, timeout=5)
            if response.status_code != 200:
                art_widget.update(f"HTTP {response.status_code}")
                return

            im = Image.open(BytesIO(response.content))
            im = im.convert("RGB")
            
            # --- SAFE SIZE UPDATE ---
            # Using 10 columns (20 pixels wide) to be absolutely safe
            target_cols = 14
            # Using 5 rows (10 pixels high)
            target_rows = 7

            im = im.resize((target_cols, target_rows * 2), Image.Resampling.LANCZOS)
            
            enhancer = ImageEnhance.Sharpness(im)
            im = enhancer.enhance(2.0)
            enhancer = ImageEnhance.Contrast(im)
            im = enhancer.enhance(1.2)

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
            err_msg = Text(f"Error:\n{str(e)}", style="bold red")
            art_widget.update(err_msg)