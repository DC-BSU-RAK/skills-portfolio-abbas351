import tkinter as tk # Import the main tkinter module for GUI creation
from tkinter import messagebox, ttk, simpledialog  # Import additional tkinter widgets and dialogs
import random, json, os # Import os for operating system interface file operations

import winsound  # For playing sound effects on Windows

# -------------------- MAIN WINDOW SETUP --------------------

root = tk.Tk()  # Create main application window
root.title("Arithmetic Quiz Game")  # Set window title
root.geometry("420x500")  # Fixed window size
root.resizable(False, False)  # Disable resizing

# -------------------- GLOBAL VARIABLES --------------------

difficulty = score = question_num = first_attempt = time_left = 0  # Initialize game variables
num1 = num2 = operation = answer_entry = progress_bar = None  # Global widget references

# -------------------- SOUND SETUP -------------------- (online resourse used)

def play_sound(sound_type):
    """Play sound effects for correct/wrong/timeout/start"""
    try:
        # Dictionary mapping sound types to their corresponding audio files
        sound_files = {
            "correct": "correct_sound_effect.wav", # Sound for correct answers
            "wrong": "wrong_answer_sound_effect.wav", # Sound for incorrect answers
            "timeout": "timeout.wav", # Sound for timeout
            "start": "start.wav" # Sound for Starting
        }
        # Use SND_FILENAME flag for file playback
        winsound.PlaySound(sound_files[sound_type], winsound.SND_FILENAME | winsound.SND_ASYNC)
    except Exception as e:
        print(f"Sound error: {e}")  # Debug sound issues

# -------------------- LEADERBOARD FUNCTIONS -------------------- (Used online resourse)

def load_leaderboard():
    """Load leaderboard data from JSON file"""
    # Check if the leaderboard file exists before attempting to open it
    if os.path.exists("leaderboard.json"):
        try:
            return json.load(open("leaderboard.json"))
        except:
            return []
    return [] # Return empty list if file doesn't exist (first time running app)

def save_leaderboard(data):
    """Save leaderboard data to JSON file"""
    json.dump(data, open("leaderboard.json", "w"), indent=2)  # this code is used to Open "leaderboard.json" in write mode and save the data as formatted JSON

def update_leaderboard(name, score):
    """Add new entry and keep top 5 scores"""
    data = load_leaderboard()
    data.append({"name": name, "score": score}) # this code is used to display the name of the user and score 
    # Sort by score descending and keep top 5
    data = sorted(data, key=lambda x: x["score"], reverse=True)[:5]
    save_leaderboard(data)

def show_leaderboard():
    """Display leaderboard window"""
    clear_window() # Clear any existing widgets from the window
    frame = tk.Frame(root, bg="#f0f8ff", bd=2, relief="raised")  # Create a styled frame for the leaderboard
    frame.place(relx=0.5, rely=0.5, anchor="center", width=350, height=400) # Center the frame in the window
    
    tk.Label(frame, text="🏆 LEADERBOARD 🏆", font=("Arial", 22, "bold"), fg="darkorange", bg="#f0f8ff").pack(pady=20)  # Title label for the leaderboard
    
    data = load_leaderboard()  # Load leaderboard data from file
    if not data: # this code Checks if no data exists
        tk.Label(frame, text="No scores yet. Be the first!", font=("Arial", 14), bg="#f0f8ff").pack(pady=10)
    else:
        for i, entry in enumerate(data, 1): # Loop through leaderboard entries with numbering
            tk.Label(frame, text=f"{i}. {entry['name']} — {entry['score']} pts", font=("Arial", 14), bg="#f0f8ff").pack(pady=3)  # Display each player's name and score
    
    tk.Button(frame, text="Back to Menu", font=("Arial", 12), command=displayMenu).pack(pady=20) # Button to return to the main menu

# -------------------- WELCOME PAGE --------------------

def welcome_page():
    """Display the welcome screen"""
    clear_window() # Clear any previous widgets from the window
    play_sound("start")  # Play start sound
     # Create the main frame for the welcome screen
    welcome_frame = tk.Frame(root, bg="#f0f8ff", bd=2, relief="raised") 
    welcome_frame.place(relx=0.5, rely=0.5, anchor="center", width=350, height=400)
    

    tk.Label(welcome_frame, text="🧮 WELCOME TO", font=("Arial", 20, "bold"), fg="darkblue", bg="#f0f8ff").pack(pady=15) # Display main welcome text
    tk.Label(welcome_frame, text="ARITHMETIC QUIZ", font=("Arial", 24, "bold"), fg="darkred", bg="#f0f8ff").pack(pady=5)  # Display the game title
    
    description_text = """Test your math skills with this fun arithmetic quiz!
    
• 10 challenging questions
• Multiple difficulty levels  
• Timer-based challenges
• Leaderboard tracking
• Instant feedback
    
Are you ready to become a math champion?"""
    tk.Label(welcome_frame, text=description_text, font=("Arial", 11), justify="center", bg="#f0f8ff").pack(pady=20)  # Displays the description label
    
    tk.Button(welcome_frame, text="🚀 START QUIZ", font=("Arial", 16, "bold"), 
              bg="green", fg="white", width=15, height=2, command=displayMenu).pack(pady=20) # Decorative star label at the bottom
    
    tk.Label(welcome_frame, text="⭐", font=("Arial", 20), bg="#f0f8ff").pack()

# -------------------- MAIN MENU --------------------

def displayMenu():
    """Show difficulty selection menu"""  # Function to display the difficulty selection screen
    clear_window()  # Clear all widgets from the previous screen
    play_sound("start")  # Play a sound when the menu appears

    # Create a frame for the difficulty menu
    menu_frame = tk.Frame(root, bg="#f0f8ff", bd=2, relief="raised")
    menu_frame.place(relx=0.5, rely=0.5, anchor="center", width=350, height=450)

    # Display main title of the quiz
    tk.Label(menu_frame, text="🧮 ARITHMETIC QUIZ", font=("Arial", 22, "bold"),
             fg="darkblue", bg="#f0f8ff").pack(pady=25)

    # Subtitle asking user to choose difficulty
    tk.Label(menu_frame, text="Select Difficulty Level", font=("Arial", 14),
             bg="#f0f8ff").pack(pady=10)

    # Button for Easy level (single-digit problems)
    tk.Button(menu_frame, text="1. Easy (Single Digit)", width=25, height=2,
              command=lambda: start_quiz("easy")).pack(pady=5)

    # Button for Moderate level (double-digit problems)
    tk.Button(menu_frame, text="2. Moderate (Double Digit)", width=25, height=2,
              command=lambda: start_quiz("moderate")).pack(pady=5)

    # Button for Advanced level (four-digit problems)
    tk.Button(menu_frame, text="3. Advanced (Four Digit)", width=25, height=2,
              command=lambda: start_quiz("advanced")).pack(pady=5)

    # Button to open the leaderboard screen
    tk.Button(menu_frame, text="🏆 View Leaderboard", width=25, height=2,
              command=show_leaderboard).pack(pady=15)

    # Button to return back to the welcome screen
    tk.Button(menu_frame, text="Back to Welcome", width=15,
              command=welcome_page).pack(pady=5)

# -------------------- QUIZ LOGIC --------------------

def randomInt(level):
    """Generate numbers based on difficulty"""  # Function to create random numbers depending on difficulty level
    
    if level == "easy":  # If the selected level is Easy
        return random.randint(1, 9), random.randint(1, 9)  # Return two single-digit numbers
    
    elif level == "moderate":  # If the selected level is Moderate
        return random.randint(10, 99), random.randint(10, 99)  # Return two double-digit numbers
    
    else:  # advanced  # If the level is Advanced
        return random.randint(1000, 9999), random.randint(1000, 9999)  # Return two four-digit numbers

def start_quiz(level):
    """Initialize quiz session"""
    global difficulty, score, question_num, first_attempt
    difficulty, score, question_num, first_attempt = level, 0, 1, True
    next_question()

def next_question():
    """Display a new math question"""
    global num1, num2, operation, answer_entry, first_attempt, time_left, progress_bar
    
    if question_num > 10:  # All questions completed
        displayResults()
        return
        
    clear_window()
    first_attempt, time_left = True, 10  # Reset attempt and timer
    
    quiz_frame = tk.Frame(root, bg="#f0f8ff", bd=2, relief="raised")
    quiz_frame.place(relx=0.5, rely=0.5, anchor="center", width=350, height=400)
    
    tk.Label(quiz_frame, text=f"Question {question_num}/10", font=("Arial", 14, "bold"), fg="darkgreen", bg="#f0f8ff").pack(pady=5)
    
    progress_bar = ttk.Progressbar(quiz_frame, length=300, maximum=10, value=question_num-1)
    progress_bar.pack(pady=5)
    
    timer_label = tk.Label(quiz_frame, text=f"⏱️ Time Left: {time_left}s", font=("Arial", 12), fg="red", bg="#f0f8ff")
    timer_label.pack(pady=5)
    
    num1, num2 = randomInt(difficulty)
    operation = random.choice(["+", "-"])
    
    tk.Label(quiz_frame, text=f"{num1} {operation} {num2} =", font=("Arial", 22, "bold"), bg="#f0f8ff").pack(pady=10)
    
    answer_entry = tk.Entry(quiz_frame, font=("Arial", 16), justify="center")
    answer_entry.pack(pady=10)
    answer_entry.focus()
    
    tk.Button(quiz_frame, text="Submit", font=("Arial", 12, "bold"), command=check_answer).pack(pady=10)
    
    countdown(timer_label)  # this code Starts countdown timer

def countdown(label):
    """Countdown timer for question"""
    global time_left
    if time_left > 0:
        time_left -= 1
        label.config(text=f"⏱️ Time Left: {time_left}s")
        root.after(1000, countdown, label)
    else:
        play_sound("timeout")
        messagebox.showinfo("Time Up", "⏰ Time's up! Moving to next question.")
        move_next_question()

def check_answer():
    """Check user's input and update score"""
    global question_num, score, first_attempt
    try:
        user_answer = int(answer_entry.get())
    except ValueError:
        messagebox.showwarning("Invalid", "Please enter a number.")
        return
    
    correct_answer = num1 + num2 if operation == "+" else num1 - num2
    
    if user_answer == correct_answer:
        score += 10 if first_attempt else 5  # Full points for first try, half for second
        play_sound("correct")
        messagebox.showinfo("Correct!", f"✅ Correct! (+{10 if first_attempt else 5} points)")
        move_next_question()
    else:
        if first_attempt:
            first_attempt = False  # Give second chance
            play_sound("wrong")
            messagebox.showwarning("Try Again", "❌ Incorrect. Try once more.")
            answer_entry.delete(0, tk.END)
        else:
            play_sound("wrong")  # Move on if wrong twice
            messagebox.showinfo("Wrong", f"❌ Wrong again! Correct answer: {correct_answer}.")
            move_next_question()

def move_next_question():
    """Go to next question"""  # Function to move to the next quiz question
    
    global question_num  # Use the global variable that tracks the current question number
    question_num += 1  # Increase the question number by 1
    next_question()  # Load and display the next question


# -------------------- RESULTS SCREEN -------------------- (used Online Resourse)

def displayResults():
    """Show final score and grade"""  # Function to display the user's final quiz results
    clear_window()  # Clear the previous screen
    play_sound("start")  # Play a sound when results are shown

    # Create a frame to display results
    results_frame = tk.Frame(root, bg="#f0f8ff", bd=2, relief="raised")
    results_frame.place(relx=0.5, rely=0.5, anchor="center", width=350, height=400)

    # Display completion message
    tk.Label(results_frame, text="🎉 QUIZ COMPLETED!", font=("Arial", 22, "bold"), 
             fg="purple", bg="#f0f8ff").pack(pady=20)

    # Display the user's final score
    tk.Label(results_frame, text=f"Your Final Score: {score}/100", 
             font=("Arial", 16), bg="#f0f8ff").pack(pady=10)

    # Calculate grade based on score
    if score >= 90: grade = "A+"  # Excellent performance
    elif score >= 80: grade = "A"  # Very good performance
    elif score >= 70: grade = "B"  # Good performance
    elif score >= 60: grade = "C"  # Average performance
    else: grade = "F"  # Failing grade

    # Display the calculated grade
    tk.Label(results_frame, text=f"Your Grade: {grade}", font=("Arial", 16, "bold"), 
             fg="blue", bg="#f0f8ff").pack(pady=10)

    # Ask user for their name to save score in leaderboard
    name = simpledialog.askstring("Name", "Enter your name for the leaderboard:")
    if name:  # If a name was entered
        update_leaderboard(name, score)  # Save score to leaderboard

    # Button to view the leaderboard
    tk.Button(results_frame, text="🏆 View Leaderboard", font=("Arial", 12), 
              command=show_leaderboard).pack(pady=10)

    # Button to restart the quiz
    tk.Button(results_frame, text="Play Again", font=("Arial", 12), 
              command=welcome_page).pack(pady=5)

    # Button to exit the game
    tk.Button(results_frame, text="Exit", font=("Arial", 12), 
              command=root.destroy).pack(pady=5)


# -------------------- CLEAR WINDOW FUNCTION --------------------

def clear_window():
    """Remove all widgets from window"""  # Function to clear all visible elements from the main window
    for widget in root.winfo_children():  # Loop through every widget currently in the window
        widget.destroy()  # Delete each widget to clear the screen
        widget.destroy() # Destroy each widget to remove it from the screen and free memory

# -------------------- START APPLICATION --------------------

welcome_page()  # Start game from welcome page
root.mainloop()  # Run Tkinter main event loop 