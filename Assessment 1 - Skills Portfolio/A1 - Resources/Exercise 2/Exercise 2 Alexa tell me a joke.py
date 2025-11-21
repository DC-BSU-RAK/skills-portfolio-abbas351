import tkinter as tk  # Import the Tkinter library for GUI
from tkinter import messagebox  # Import messagebox for pop-up alerts
import random  # Import random for selecting jokes randomly
import os  # Import os for file path operations
import winsound  # Import winsound for playing punchline sound on Windows


class JokeTellerApp:
    def __init__(self, root):
        self.root = root  # Store the main Tkinter window
        self.root.title("Alexa Joke Teller")  # Set window title
        self.root.geometry("600x400")  # Set default window size
        self.root.config(bg="#2C3E50")  # Set background color

        # -------- Window Icon (no PIL needed) --------
        try:
            self.root.iconbitmap("Assessment 1 - Skills Portfolio/A1 - Resources/Exercise 2/alexa.ico")  # Set window icon
        except:
            pass  # Ignore if icon not found

        # Make window initially transparent for fade-in (wrapped in try for compatibility)
        try:
            self.root.attributes('-alpha', 0.0)  # Start with fully transparent window
        except:
            pass  # this code Ignores if platform doesn't support transparency

        # Create welcome page BEFORE loading main UI
        self.create_welcome_page()  # Call welcome page creation

        # Variables
        self.jokes = []  # List to store all jokes
        self.current_setup = ""  # Current joke setup
        self.current_punchline = ""  # Current joke punchline
        self.punchline_shown = False  # Flag to check if punchline is shown

        # Favourite joke
        self.favourite_joke = None  # Store favourite joke tuple

        # GIF background variables this will be loaded when main UI is created
        self.gif_frames = []  # List of frames for GIF animation
        self.gif_index = 0  # Current GIF frame index
        self.gif_label = None  # Label to display GIF
        self.gif_running = False  # Flag to control GIF animation

        # Glowing button vars
        self.glow_on = True  # Flag for glow animation
        self.glow_step = 0  # Step counter for glow cycle

        # Load jokes from file
        self.load_jokes()  # Call function to load jokes

    # ------------------- WELCOME PAGE --------------------
    def create_welcome_page(self):
        self.welcome_frame = tk.Frame(self.root, bg="#2C3E50")  # Frame for welcome page
        self.welcome_frame.pack(fill=tk.BOTH, expand=True)  # Fill entire window

        tk.Label(
            self.welcome_frame,
            text="🎉 Welcome to Alexa Joke Teller 🎉",  # Welcome message
            font=("Arial", 22, "bold"),  # Font style
            fg="white",  # Text color
            bg="#2C3E50"  # Background color
        ).pack(pady=80)  # Add padding from top

        tk.Button(
            self.welcome_frame,
            text="Start",  # Start button text
            font=("Arial", 14, "bold"),  # Font style
            bg="#27AE60",  # Button background color
            fg="white",  # Text color
            cursor="hand2",  # Mouse cursor style
            width=15,  # Button width
            height=2,  # Button height
            command=self.start_app  # Call start_app when clicked
        ).pack(pady=20)  # Add vertical padding

        # Start fade-in for the whole window works on platforms that support alpha (Online Resource Used)
        try:
            self.fade_in(0.0)  # Call fade-in with initial alpha 0
        except:
            pass  # Ignore if platform doesn't support alpha

    def fade_in(self, alpha):
        """Fade window from alpha -> 1.0"""
        try:
            if alpha < 1.0:  # Continue until fully opaque
                alpha = round(alpha + 0.05, 3)  # Increase transparency slightly
                self.root.attributes('-alpha', alpha)  # Set new alpha
                self.root.after(40, lambda: self.fade_in(alpha))  # Repeat after 40ms
            else:
                self.root.attributes('-alpha', 1.0)  # Set fully opaque at end
        except:
            pass  # Ignore errors if unsupported

    def start_app(self):
        """Remove welcome page + show main app UI"""
        try:
            self.fade_out_frame(self.welcome_frame, 1.0)  # Fade-out welcome frame
        except:
            self.welcome_frame.destroy()  # Destroy immediately if fade fails
            self.create_widgets()  # Create main widgets
            self.typing_index = 0  # Reset typing animation index
            self.typing_animation_mode = 0  # Reset animation mode
            self.typing_animation()  # Start typing animation

    def fade_out_frame(self, frame, opacity):
        """Faux fade by gradually lowering widget's background intensity then destroy."""
        try:
            if opacity > 0.0:  # Continue fading
                level = int(52 * opacity)  # Calculate grey level based on opacity
                hexcol = f'#{level:02x}{(level+30 if level+30<255 else 255):02x}{(level+48 if level+48<255 else 255):02x}'  # Hex color
                frame.config(bg=hexcol)  # Set new background color
                for child in frame.winfo_children():  # Iterate all children
                    try:
                        child.config(bg=hexcol)  # Apply fade to children
                    except:
                        pass  # Ignore if cannot set
                self.root.after(30, lambda: self.fade_out_frame(frame, round(opacity - 0.08, 2)))  # Repeat with reduced opacity
            else:
                frame.destroy()  # Destroy frame at end of fade
                self.create_widgets()  # Create main widgets
                self.typing_index = 0  # Reset typing animation index
                self.typing_animation_mode = 0  # Reset animation mode
                self.typing_animation()  # Start typing animation
        except:
            try:
                frame.destroy()  # Fallback destroy
            except:
                pass
            self.create_widgets()  # Fallback: create main UI
            self.typing_index = 0
            self.typing_animation_mode = 0
            self.typing_animation()

    # -----------------------------------------------------

    # --------- Typing Animation Updated with Favourite Mode (Online Resourse Used) ----------
    def typing_animation(self):
        typing_modes = [
            ["Typing", "Typing.", "Typing..", "Typing..."],  # Default typing animation
            ["Showing Favourites", "Showing Favourites.", "Showing Favourites..", "Showing Favourites..."]  # Favourite mode animation
        ]

        frames = typing_modes[self.typing_animation_mode]  # Select frame set
        self.typing_index = (self.typing_index + 1) % len(frames)  # Cycle through frames

        self.title_label.config(
            text=f"🎤 Alexa Joke Teller 🎤  |  {frames[self.typing_index]}"  #title text
        )

        self.root.after(500, self.typing_animation)  # Repeat every 500ms

    # ------------- Writing Animation for Text -----------------
    def animate_text(self, label, full_text, index=0):
        """Displays text character by character"""
        if index == 0:
            label.config(text="")  # Clear old text first

        if index < len(full_text):  # If text remains
            label.config(text=label.cget("text") + full_text[index])  # Append next character
            self.root.after(25, lambda: self.animate_text(label, full_text, index + 1))  # Repeat after 25ms

    # -----------------------------------------------------------

    def load_jokes(self):
        """Load jokes from the randomJokes.txt file"""
        try:
            file_path = "Assessment 1 - Skills Portfolio/A1 - Resources\Exercise 2/randomJokes.txt"  # Main path
            if not os.path.exists(file_path):
                file_path = "randomJokes.txt"  # Fallback path

            with open(file_path, 'r', encoding='utf-8') as file:  # Open file
                lines = file.readlines()  # Read all lines

            for line in lines:  # Iterate each line
                line = line.strip()  # Remove whitespace
                if line.startswith('-'):
                    line = line[1:].strip()  # Remove leading dash

                if '?' in line:  # Split into setup/punchline
                    parts = line.split('?', 1)
                    setup = parts[0].strip() + '?'  # Setup ends with '?'
                    punchline = parts[1].strip()  # Punchline
                    self.jokes.append((setup, punchline))  # Add to list

        except FileNotFoundError:  # If file missing
            messagebox.showerror("Error", "randomJokes.txt file not found!")  # Show error
            self.jokes = [
                ("Why did the chicken cross the road?", "To get to the other side."),  # Default jokes
                ("What happens if you boil a clown?", "You get a laughing stock."),
                ("Why don't scientists trust atoms?", "Because they make up everything!")
            ]

    def create_widgets(self):
        """Create all GUI widgets"""
        gif_path = "Assessment 1 - Skills Portfolio/A1 - Resources/Exercise 2/animated laughing.gif"  # GIF path
        self.load_gif_background(gif_path)  # Load animated GIF

        self.title_label = tk.Label(
            self.root,
            text="🎤 Alexa Joke Teller 🎤",  # Title text
            font=("Arial", 20, "bold"),  # Font
            bg="#2C3E50",  # Background
            fg="#ECF0F1"  # Foreground text
        )
        self.title_label.pack(pady=20)  # Pack with padding

        joke_frame = tk.Frame(self.root, bg="#34495E", relief=tk.RIDGE, bd=2)  # Frame for jokes
        joke_frame.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)  # Pack frame

        self.setup_label = tk.Label(
            joke_frame,
            text="Click the button to hear a joke!",  # Placeholder
            font=("Arial", 14),  # Font
            bg="#34495E",  # Background
            fg="#ECF0F1",  # Foreground
            wraplength=550,  # Wrap text
            justify=tk.CENTER  # Center text
        )
        self.setup_label.pack(pady=20)  # Pack label

        self.punchline_label = tk.Label(
            joke_frame,
            text="",  # Initially empty
            font=("Arial", 14, "italic"),  # Italic font
            bg="#34495E",
            fg="#F39C12",
            wraplength=550,
            justify=tk.CENTER
        )
        self.punchline_label.pack(pady=10)

        button_frame = tk.Frame(self.root, bg="#2C3E50")  # Frame for buttons
        button_frame.pack(pady=20)

        self.joke_button = tk.Button(
            button_frame,
            text="Alexa tell me a Joke",  # Joke button text
            font=("Arial", 12, "bold"),
            bg="#3498DB",
            fg="white",
            command=self.tell_joke,  # Call tell_joke
            width=20,
            height=2,
            cursor="hand2"
        )
        self.joke_button.grid(row=0, column=0, padx=10, pady=5)  # Grid placement

        try:
            self.start_glow()  # Start glowing effect
        except:
            pass

        self.punchline_button = tk.Button(
            button_frame,
            text="Show Punchline",  # Punchline button
            font=("Arial", 12, "bold"),
            bg="#2ECC71",
            fg="white",
            command=self.show_punchline,  # Call show_punchline
            width=20,
            height=2,
            cursor="hand2",
            state=tk.DISABLED  # Initially disabled
        )
        self.punchline_button.grid(row=0, column=1, padx=10, pady=5)

        self.next_button = tk.Button(
            button_frame,
            text="Next Joke",
            font=("Arial", 12, "bold"),
            bg="#9B59B6",
            fg="white",
            command=self.tell_joke,  # Next joke
            width=20,
            height=2,
            cursor="hand2",
            state=tk.DISABLED  # Initially disabled
        )
        self.next_button.grid(row=1, column=0, padx=10, pady=5)

        self.fav_button = tk.Button(
            button_frame,
            text="❤️ Favourite Joke",
            font=("Arial", 12, "bold"),
            bg="#E67E22",
            fg="white",
            command=self.save_favourite,  # Save favourite
            width=20,
            height=2,
            cursor="hand2",
            state=tk.DISABLED  # Initially disabled
        )
        self.fav_button.grid(row=1, column=1, padx=10, pady=5)

        self.show_fav_button = tk.Button(
            button_frame,
            text="⭐ Show Favourite",
            font=("Arial", 12, "bold"),
            bg="#F1C40F",
            fg="black",
            command=self.show_favourite_joke,  # Show favourite joke
            width=20,
            height=2,
            cursor="hand2"
        )
        self.show_fav_button.grid(row=2, column=0, columnspan=2, pady=5)

        self.quit_button = tk.Button(
            button_frame,
            text="Quit",
            font=("Arial", 12, "bold"),
            bg="#E74C3C",
            fg="white",
            command=self.quit_app,  # Quit app
            width=20,
            height=2,
            cursor="hand2"
        )
        self.quit_button.grid(row=3, column=0, columnspan=2, padx=10, pady=5)

    # -------------------------------------------------------

    def tell_joke(self):
        """Select and display a random joke setup"""
        self.typing_animation_mode = 0  # Reset animation mode

        if not self.jokes:  # Check if jokes exist
            messagebox.showwarning("No Jokes", "No jokes available!")  # Warn
            return

        self.current_setup, self.current_punchline = random.choice(self.jokes)  # Pick random joke

        self.setup_label.config(text="")  # Clear previous setup
        self.punchline_label.config(text="")  # Clear previous punchline

        self.animate_text(self.setup_label, self.current_setup)  # Animate setup

        self.punchline_button.config(state=tk.NORMAL)  # Enable punchline button
        self.joke_button.config(state=tk.DISABLED)  # Disable main joke button
        self.next_button.config(state=tk.DISABLED)  # Disable next button
        self.fav_button.config(state=tk.DISABLED)  # Disable favourite button
        self.punchline_shown = False  # Reset punchline flag

    def show_punchline(self):
        """Display the punchline (with sound + animation)"""
        if self.current_punchline and not self.punchline_shown:

            self.punchline_label.config(text="")  # Clear previous text
            self.animate_text(self.punchline_label, self.current_punchline)  # Animate punchline

            try:
                winsound.PlaySound("Assessment 1 - Skills Portfolio/A1 - Resources/Exercise 2/main funny.wav", winsound.SND_ASYNC)  # Play sound
            except:
                pass  # Ignore if missing

            self.punchline_button.config(state=tk.DISABLED)  # Disable punchline button
            self.joke_button.config(state=tk.NORMAL)  # Enable main joke button
            self.next_button.config(state=tk.NORMAL)  # Enable next button
            self.fav_button.config(state=tk.NORMAL)  # Enable favourite button
            self.punchline_shown = True  # Mark punchline as shown

    def save_favourite(self):
        """Save favourite joke"""
        self.favourite_joke = (self.current_setup, self.current_punchline)  # Store joke
        messagebox.showinfo("Saved", "Favourite joke saved! ❤️")  # Show info

    def show_favourite_joke(self):
        self.typing_animation_mode = 1  # Switch to favourite animation

        if not self.favourite_joke:  # Check if favourite exists
            messagebox.showinfo("No Favourites", "No favourite joke saved yet!")  # Info
            return

        fav_win = tk.Toplevel(self.root)  # Create new window
        fav_win.title("⭐ Favourite Joke")  # Window title
        fav_win.geometry("450x250")  # Window size
        fav_win.config(bg="#34495E")  # Background color

        try:
            fav_win.iconbitmap("alexa.ico")  # Icon
        except:
            pass

        tk.Label(
            fav_win,
            text="⭐ Your Favourite Joke ⭐",
            font=("Arial", 16, "bold"),
            bg="#34495E",
            fg="white"
        ).pack(pady=10)

        tk.Label(
            fav_win,
            text=self.favourite_joke[0],  # Display setup
            font=("Arial", 14),
            wraplength=420,
            bg="#34495E",
            fg="#ECF0F1"
        ).pack(pady=10)

        tk.Label(
            fav_win,
            text=self.favourite_joke[1],  # Display punchline
            font=("Arial", 14, "italic"),
            wraplength=420,
            bg="#34495E",
            fg="#F39C12"
        ).pack(pady=10)

    def quit_app(self):
        self.gif_running = False  # Stop GIF animation
        self.root.quit()  # Close app

    # ----------------- GIF BACKGROUND HANDLING -----------------
    def load_gif_background(self, path):
        """Loads all frames of a GIF and starts animation. If loading fails, silently ignore."""
        try:
            if not os.path.exists(path):
                return  # Exit if GIF not found

            frames = []  # List for frames
            idx = 0  # Frame index
            while True:
                try:
                    frame = tk.PhotoImage(file=path, format=f"gif -index {idx}")  # Load frame
                    frames.append(frame)  # Add to list
                    idx += 1
                except Exception:
                    break  # Stop if no more frames

            if not frames:
                return

            self.gif_frames = frames  # Save frames
            self.gif_label = tk.Label(self.root, bd=0)  # Label for GIF
            self.gif_label.place(x=0, y=0, relwidth=1.0, relheight=1.0)  # Full window
            self.gif_label.lower(belowThis=None)  # Place behind widgets

            self.gif_running = True  # Start animation
            self.animate_gif()  # Begin GIF loop
        except:
            pass

    def animate_gif(self):
        """Cycle through gif frames if available"""
        try:
            if not self.gif_running or not self.gif_frames:
                return
            frame = self.gif_frames[self.gif_index]  # Get current frame
            try:
                self.gif_label.config(image=frame)  # Update label image
            except:
                pass
            self.gif_index = (self.gif_index + 1) % len(self.gif_frames)  # Increment frame
            self.root.after(100, self.animate_gif)  # Repeat after 100ms
        except:
            pass

    # ----------------- GLOWING BUTTON (Online resource Used) -----------------
    def start_glow(self):
        """Begin pulsing/glow animation for the Alexa button"""
        try:
            self.glow_on = True  # Start glow
            self.glow_step = 0  # Reset step
            self.glow_cycle()  # Begin glow loop
        except:
            pass

    def glow_cycle(self):
        """Cycle button background through subtle shades to simulate glow"""
        try:
            if not hasattr(self, 'joke_button'):
                return  # Exit if button missing

            start_rgb = (52, 152, 219)  # Base color
            end_rgb = (129, 199, 255)  # Lighter color

            steps = 40  # Number of steps
            t = (self.glow_step % (2 * steps))  # Calculate cycle position
            if t >= steps:
                t = 2 * steps - t  # Reverse
            factor = t / steps  # Interpolation factor

            r = int(start_rgb[0] + (end_rgb[0] - start_rgb[0]) * factor)  # Interpolate red
            g = int(start_rgb[1] + (end_rgb[1] - start_rgb[1]) * factor)  # Interpolate green
            b = int(start_rgb[2] + (end_rgb[2] - start_rgb[2]) * factor)  # Interpolate blue
            hexcol = f'#{r:02x}{g:02x}{b:02x}'  # Convert to hex

            try:
                self.joke_button.config(bg=hexcol)  # Apply color
            except:
                pass

            self.glow_step += 1  # Next step
            self.root.after(60, self.glow_cycle)  # Repeat after 60ms
        except:
            pass
def main():
    root = tk.Tk()  # Create main Tkinter window
    app = JokeTellerApp(root)  # Initialize app
    root.mainloop()  # Run Tkinter main loop

if __name__ == "__main__":
    main()  # Start program 