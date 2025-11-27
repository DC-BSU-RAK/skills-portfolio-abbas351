import tkinter as tk                     # Main GUI library
from tkinter import messagebox, simpledialog  # Pop-up dialogs and messages
import os                                # For file and folder operations
import winsound                          # Play background music (Windows only)
import math                              # For pie chart angle calculations
import tempfile                          # Create temporary HTML files for Plotly charts
import webbrowser                        # Open interactive charts in browser
import plotly.graph_objs as go               # Plotly: create charts
import plotly.io as pio                  # Plotly: save charts as HTML

#  CONFIG (Used Online Resourse)
WINDOW_W = 1000                          # Default window width
WINDOW_H = 600                           # Default window height
SIDEBAR_W = 180                          # Width of the left sidebar
ANIM_STEP = 20                           # How many pixels each animation frame moves
ANIM_DELAY = 10                          # Delay between animation frames (in milliseconds)

# Data file path
DATA_FILE = "Assessment 1 - Skills Portfolio/A1 - Resources/Exercise 3/studentMarks.txt"

# DATA HELPERS 

def load_students():
    """Read student data from the text file and return a list of dictionaries"""
    students = []
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            lines = [line.strip() for line in f.readlines()]  # Remove extra whitespace
            for line in lines[1:]:                           # Skip header line
                if not line:                                 # Skip empty lines
                    continue
                data = line.split(",")                       # CSV-style split
                students.append({
                    "num": int(data[0]),                     # Student number
                    "name": data[1],                         # Full name
                    "cw_total": int(data[2]) + int(data[3]) + int(data[4]),  # Sum of 3 coursework marks
                    "exam": int(data[5])                     # Exam mark out of 100
                })
    except Exception:
        pass
    return students

def save_students():
    try:
        os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    except Exception:
        pass
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            f.write(str(len(students)) + "\n")
            for s in students:
                c1 = c2 = c3 = s["cw_total"] // 3
                f.write(f"{s['num']},{s['name']},{c1},{c2},{c3},{s['exam']}\n")
    except Exception as e:
        messagebox.showerror("Error", f"Could not save students: {e}")

def percentage(s):
    return round(((s["cw_total"] + s["exam"]) / 160) * 100, 2)

def grade(p):
    return "A" if p >= 70 else "B" if p >= 60 else "C" if p >= 50 else "D" if p >= 40 else "F"

def format_student(s):
    p = percentage(s)
    return (
        f"Name: {s['name']}\n"
        f"Student No.: {s['num']}\n"
        f"Coursework Total: {s['cw_total']} / 60\n"
        f"Exam: {s['exam']} / 100\n"
        f"Percentage: {p}%\n"
        f"Grade: {grade(p)}\n"
        + "-"*40 + "\n"
    )

students = load_students()

# ROOT and RESOURCES 

root = tk.Tk()
root.title("Student Manager")
try:
    root.state("zoomed")
except Exception:
    root.geometry(f"{WINDOW_W}x{WINDOW_H}")
root.resizable(True, True)

try:
    root.iconbitmap("Assessment 1 - Skills Portfolio/A1 - Resources/Exercise 3/sms.ico") # Main path of icon
except:
    pass

# COMMON UI ELEMENTS 

def make_button(parent, text, command, width=20, height=2, font=("Arial", 12), x=None, y=None):
    frame = tk.Frame(parent, bd=0, bg="#1a73e8", highlightthickness=0)
    lbl = tk.Label(frame, text=text, font=font, bg="#1a73e8", fg="white", padx=10, pady=8, cursor="hand2")
    lbl.pack()
    def on_enter(e): frame.config(bg="#0d5ec0"); lbl.config(bg="#0d5ec0")
    def on_leave(e): frame.config(bg="#1a73e8"); lbl.config(bg="#1a73e8")
    lbl.bind("<Enter>", on_enter); lbl.bind("<Leave>", on_leave)
    lbl.bind("<Button-1>", lambda e: command())
    if x is not None and y is not None:
        frame.place(x=x, y=y, width=width*10, height=height*12)
    else:
        frame.pack(pady=6)
    return frame

#  LAYOUT SIDEBAR + MAIN AREA 

main_holder = tk.Canvas(root, width=WINDOW_W - SIDEBAR_W, height=WINDOW_H, highlightthickness=0) # Canvas that will hold all pages allows sliding animation
main_holder.place(x=SIDEBAR_W, y=0, relwidth=1.0, relheight=1.0)

sidebar = tk.Frame(root, width=SIDEBAR_W, height=WINDOW_H, bg="#0f1724")
sidebar.place(x=0, y=0, relheight=1.0) # Dark left sidebar

tk.Label(sidebar, text="Student\nManager", font=("Arial", 18, "bold"), bg="#0f1724", fg="white").place(x=20, y=20) # Title in sidebar

pages = {} # Dictionary to store all pages

def create_page(name):
    frame = tk.Frame(main_holder, width=WINDOW_W - SIDEBAR_W, height=WINDOW_H, bd=0, bg="#f4f8ff")  # plain background
    pages[name] = frame
    return frame

# ANIMATED TRANSITIONS 

current_page = None

def put_frame_on_canvas(frame, x):
    win_id = main_holder.create_window(x, 0, anchor="nw", window=frame,
                                       width=main_holder.winfo_width() or (WINDOW_W - SIDEBAR_W),
                                       height=root.winfo_height() or WINDOW_H)
    return win_id

def slide_to(new_frame, direction="left"):
    global current_page
    width = main_holder.winfo_width() or (WINDOW_W - SIDEBAR_W)
    if current_page is new_frame:
        return
    if direction == "left": # Decide where the new page starts right or left of screen 
        start_new_x = width
        delta = -ANIM_STEP
    else:
        start_new_x = -width
        delta = ANIM_STEP

    new_win = put_frame_on_canvas(new_frame, start_new_x)
    old_win = None
    if current_page:
        old_win = put_frame_on_canvas(current_page, 0)

    def step():
        nonlocal start_new_x
        start_new_x += delta
        try:
            main_holder.coords(new_win, start_new_x, 0)
        except Exception:
            pass
        if old_win:
            try:
                old_x = main_holder.coords(old_win)[0]
                main_holder.coords(old_win, old_x + delta, 0)
            except Exception:
                pass
        if (direction == "left" and start_new_x <= 0) or (direction == "right" and start_new_x >= 0):
            main_holder.coords(new_win, 0, 0)
            for cid in list(main_holder.find_all()):
                if cid != new_win:
                    main_holder.delete(cid)
            finalize(new_frame)
        else:
            root.after(ANIM_DELAY, step)

    def finalize(frame_to_set):
        global current_page
        current_page = frame_to_set

    step()

def show_page(name, direction="left"):
    if name in pages:
        slide_to(pages[name], direction=direction)

# PAGES CREATION 

#  WELCOME PAGE 
welcome = create_page("welcome")
tk.Label(welcome, text="Welcome to Student Manager", font=("Arial", 26, "bold"), bg="#f4f8ff").place(relx=0.5, rely=0.25, anchor="center")
enter_btn = tk.Frame(welcome, bg="#1a73e8")
enter_lbl = tk.Label(enter_btn, text="ENTER", font=("Arial", 16, "bold"), bg="#1a73e8", fg="white", padx=24, pady=10, cursor="hand2")
enter_lbl.pack()
enter_lbl.bind("<Button-1>", lambda e: show_page("menu", direction="left"))
enter_lbl.bind("<Enter>", lambda e: enter_lbl.config(bg="#0d5ec0"))
enter_lbl.bind("<Leave>", lambda e: enter_lbl.config(bg="#1a73e8"))
enter_btn.place(relx=0.5, rely=0.5, anchor="center")

# MENU PAGE Main
menu = create_page("menu")
tk.Label(menu, text="STUDENT MANAGER MENU", font=("Arial", 20, "bold"), bg="#f4f8ff").place(x=20, y=18)

make_button(menu, "Dashboard", lambda: show_page("dashboard", direction="left"), width=24, height=2).place(x=30, y=80)
make_button(menu, "View All Records", lambda: view_all(), width=24, height=2).place(x=30, y=140)
make_button(menu, "View Individual", lambda: view_individual(), width=24, height=2).place(x=30, y=200)
make_button(menu, "Highest Score", lambda: highest(), width=24, height=2).place(x=30, y=260)
make_button(menu, "Lowest Score", lambda: lowest(), width=24, height=2).place(x=30, y=320)
make_button(menu, "Sort Records", lambda: sort_records(), width=24, height=2).place(x=330, y=80)
make_button(menu, "Add Student", lambda: add_record_and_refresh(), width=24, height=2).place(x=330, y=140)
make_button(menu, "Delete Student", lambda: delete_record_and_refresh(), width=24, height=2).place(x=330, y=200)
make_button(menu, "Update Student", lambda: update_record_and_refresh(), width=24, height=2).place(x=330, y=260)
make_button(menu, "Export Summary", lambda: export_summary(), width=24, height=2).place(x=330, y=320)

#  OUTPUT PAGE 
output_page = create_page("output")
tk.Label(output_page, text="Output", font=("Arial", 18, "bold"), bg="#f4f8ff").place(x=20, y=12)
out_text = tk.Text(output_page, width=80, height=28, wrap="word", font=("Arial", 11))
out_text.place(x=20, y=50)

def make_back_on_page(page, target="menu"):
    btn = tk.Label(page, text="Back", bg="#1a73e8", fg="white", font=("Arial", 11, "bold"), padx=8, pady=6, cursor="hand2")
    btn.place(x=20, y=520)
    btn.bind("<Button-1>", lambda e: show_page(target, direction="right"))
    btn.bind("<Enter>", lambda e: btn.config(bg="#0d5ec0"))
    btn.bind("<Leave>", lambda e: btn.config(bg="#1a73e8"))
make_back_on_page(output_page)

# DASHBOARD PAGE 
dashboard = create_page("dashboard")
tk.Label(dashboard, text="Dashboard", font=("Arial", 20, "bold"), bg="#f4f8ff").place(x=20, y=12)

bar_canvas = tk.Canvas(dashboard, width=580, height=260, bg="#ffffff", highlightthickness=1, highlightbackground="#d0d7e6")
bar_canvas.place(x=40, y=60)
tk.Label(dashboard, text="Student Percentages (bar chart)", bg="#f4f8ff", font=("Arial", 11)).place(x=40, y=44)

pie_canvas = tk.Canvas(dashboard, width=260, height=260, bg="#ffffff", highlightthickness=1, highlightbackground="#d0d7e6")
pie_canvas.place(x=640, y=60)
tk.Label(dashboard, text="Grade Distribution (pie)", bg="#f4f8ff", font=("Arial", 11)).place(x=640, y=44)

def open_interactive_charts():
    names = [s['name'] for s in students]
    percents = [percentage(s) for s in students]
    bar = go.Bar(x=names, y=percents, text=[f"{p}%" for p in percents], hovertemplate="%{x}<br>%{y}%<extra></extra>")
    counts = {'A':0,'B':0,'C':0,'D':0,'F':0}
    for s in students:
        counts[grade(percentage(s))] += 1
    pie = go.Pie(labels=list(counts.keys()), values=list(counts.values()), hoverinfo="label+percent+value")
    fig = go.Figure(data=[bar])
    fig.update_layout(title="Student Percentages (interactive)", template="plotly_dark", height=600)
    tf_bar = tempfile.NamedTemporaryFile(delete=False, suffix=".html")
    pio.write_html(fig, file=tf_bar.name, auto_open=False)

    fig2 = go.Figure(data=[pie])
    fig2.update_layout(title="Grade Distribution (interactive)", template="plotly_dark", height=600)
    tf_pie = tempfile.NamedTemporaryFile(delete=False, suffix=".html")
    pio.write_html(fig2, file=tf_pie.name, auto_open=False)

    webbrowser.open(tf_bar.name)
    webbrowser.open(tf_pie.name)

plotly_btn = make_button(dashboard, "Open Interactive Charts", lambda: open_interactive_charts(), width=30, height=2)
plotly_btn.place(x=40, y=340)

avg_label = tk.Label(dashboard, text="", font=("Arial", 12, "bold"), bg="#f4f8ff")
avg_label.place(x=40, y=400)
high_label = tk.Label(dashboard, text="", font=("Arial", 12, "bold"), bg="#f4f8ff")
high_label.place(x=320, y=400)
low_label = tk.Label(dashboard, text="", font=("Arial", 12, "bold"), bg="#f4f8ff")
low_label.place(x=520, y=400)

make_back_on_page(dashboard)

# CHART DRAWING UTILITIES 
# (draw bar chart, draw pie chart remain unchanged omitted for brevity but present in full script (Online resourse Used)

def draw_bar_chart(canvas, values, labels):
    canvas.delete("all")
    w = int(canvas['width'])
    h = int(canvas['height'])
    padding = 40
    if not values:
        canvas.create_text(w/2, h/2, text="No data", font=("Arial", 14))
        return
    maxv = max(values) if values else 1
    bar_w = (w - padding*2) / max(1, len(values)) * 0.7
    gap = ((w - padding*2) - bar_w*len(values)) / max(1, len(values)-1) if len(values) > 1 else 0
    x = padding
    for i, v in enumerate(values):
        bar_h = (v / maxv) * (h - padding*2) if maxv > 0 else 0
        x1 = x
        y1 = h - padding - bar_h
        x2 = x + bar_w
        y2 = h - padding
        r = int(26 + (i/len(values))*40) if len(values)>0 else 26
        g = int(115 + (1 - i/len(values))*80) if len(values)>0 else 115
        b = int(232 - (i/len(values))*60) if len(values)>0 else 232
        color = f'#{r:02x}{g:02x}{b:02x}'
        canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="")
        canvas.create_text((x1+x2)/2, y1-12, text=str(v)+"%", font=("Arial", 9, "bold"))
        canvas.create_text((x1+x2)/2, h - padding + 12, text=labels[i], font=("Arial", 9), anchor="n")
        tag = f"bar{i}"
        canvas.create_rectangle(x1, y1, x2, y2, outline="", tags=(tag,))
        def make_on_enter(value=v, name=labels[i]):
            def on_enter_event(evt, val=value, nm=name):
                tooltip.place_forget()
                tooltip.config(text=f"{nm}\n{val}%")
                tooltip.place(x=evt.x_root - root.winfo_rootx() + 10, y=evt.y_root - root.winfo_rooty() + 10)
            return on_enter_event
        def on_leave_event(evt):
            tooltip.place_forget()
        canvas.tag_bind(tag, "<Enter>", make_on_enter())
        canvas.tag_bind(tag, "<Leave>", on_leave_event)
        x = x2 + gap

    for perc in range(0, 101, 20):
        y = h - padding - (perc / maxv) * (h - padding*2) if maxv>0 else h-padding
        canvas.create_line(padding, y, w-padding, y, fill="#eef2f8")
        canvas.create_text(padding-20, y, text=str(int(perc))+"%", font=("Arial", 8), anchor="e")

def draw_pie_chart(canvas, counts):
    canvas.delete("all")
    w = int(canvas['width'])
    h = int(canvas['height'])
    cx, cy = w/2, h/2
    r = min(w,h)/2 - 10
    total = sum(counts.values())
    if total == 0:
        canvas.create_text(cx, cy, text="No data", font=("Arial", 14))
        return
    start = 0
    palette = {'A': '#2ecc71', 'B': '#3498db', 'C': '#f1c40f', 'D': '#e67e22', 'F': '#e74c3c'}
    for k, val in counts.items():
        extent = (val / total) * 360
        color = palette.get(k, "#95a5a6")
        canvas.create_arc(cx-r, cy-r, cx+r, cy+r, start=start, extent=extent, fill=color, outline="white")
        mid = math.radians(start + extent/2)
        lx = cx + (r/1.6) * math.cos(mid)
        ly = cy + (r/1.6) * math.sin(mid)
        canvas.create_text(lx, ly, text=f"{k} ({val})", font=("Arial", 9, "bold"))
        start += extent

tooltip = tk.Label(dashboard, text="", bg="#222", fg="white", font=("Arial", 9), bd=1, relief="solid")
tooltip.place_forget()

def update_dashboard():
    vals = [percentage(s) for s in students]
    labels = [s['name'][:10] for s in students]
    draw_bar_chart(bar_canvas, vals, labels)
    counts = {'A':0,'B':0,'C':0,'D':0,'F':0}
    for s in students:
        counts[grade(percentage(s))] += 1
    draw_pie_chart(pie_canvas, counts)
    if students:
        avg = round(sum(vals)/len(vals), 2)
        hi = max(vals)
        lo = min(vals)
    else:
        avg = hi = lo = 0
    avg_label.config(text=f"Average: {avg}%")
    high_label.config(text=f"Highest: {hi}%")
    low_label.config(text=f"Lowest: {lo}%")

# MENU FUNCTIONALITY 
# (view_all, view_individual, highest, lowest, sort_records, add/delete/update_record export summary unchanged (Researched)

def show_output(txt):
    out_text.config(state="normal")
    out_text.delete("1.0", tk.END)
    out_text.insert(tk.END, txt)
    out_text.config(state="disabled")
    show_page("output", direction="left")

def view_all():
    out = ""
    total = 0
    for s in students:
        out += format_student(s)
        total += percentage(s)
    avg = round(total / len(students), 2) if students else 0
    out += f"\nTotal Students: {len(students)}\nAverage %: {avg}%"
    show_output(out)

def view_individual():
    num = simpledialog.askinteger("Search", "Enter student number:")
    if not num: return
    for s in students:
        if s["num"] == num:
            show_output(format_student(s))
            return
    messagebox.showinfo("Not Found", "Student not found.")

def highest():
    if not students:
        messagebox.showinfo("Info", "No students available.")
        return
    show_output("Highest Scoring Student:\n\n" + format_student(max(students, key=lambda s: percentage(s))))

def lowest():
    if not students:
        messagebox.showinfo("Info", "No students available.")
        return
    show_output("Lowest Scoring Student:\n\n" + format_student(min(students, key=lambda s: percentage(s))))

def sort_records():
    asc = messagebox.askyesno("Sort", "Sort ascending?\nYES = Ascending\nNO = Descending")
    students.sort(key=lambda s: percentage(s), reverse=not asc)
    view_all()

def add_record():
    name = simpledialog.askstring("Add", "Enter name:")
    if name is None: return
    num = simpledialog.askinteger("Add", "Student number:")
    if num is None: return
    c1 = simpledialog.askinteger("Add", "Coursework 1:")
    c2 = simpledialog.askinteger("Add", "Coursework 2:")
    c3 = simpledialog.askinteger("Add", "Coursework 3:")
    exam = simpledialog.askinteger("Add", "Exam:")
    students.append({
        "name": name,
        "num": num,
        "cw_total": (c1 or 0) + (c2 or 0) + (c3 or 0),
        "exam": exam or 0
    })
    save_students()

def delete_record():
    num = simpledialog.askinteger("Delete", "Enter student number:")
    if num is None: return
    for s in students:
        if s["num"] == num:
            students.remove(s)
            save_students()
            return
    messagebox.showinfo("Not Found", "Student not found.")

def update_record():
    num = simpledialog.askinteger("Update", "Enter student number:")
    if num is None: return
    for s in students:
        if s["num"] == num:
            exam = simpledialog.askinteger("Update", "New exam mark:")
            c1 = simpledialog.askinteger("Update", "Coursework 1:")
            c2 = simpledialog.askinteger("Update", "Coursework 2:")
            c3 = simpledialog.askinteger("Update", "Coursework 3:")
            s["cw_total"] = (c1 or 0) + (c2 or 0) + (c3 or 0)
            s["exam"] = exam or 0
            save_students()
            return
    messagebox.showinfo("Not Found", "Student not found.")

def add_record_and_refresh():
    add_record()
    update_dashboard()
    show_page("dashboard", direction="left")

def delete_record_and_refresh():
    delete_record()
    update_dashboard()
    show_page("dashboard", direction="left")

def update_record_and_refresh():
    update_record()
    update_dashboard()
    show_page("dashboard", direction="left")

def export_summary():
    try:
        with open("students_summary.txt", "w", encoding="utf-8") as f:
            for s in students:
                f.write(format_student(s))
        messagebox.showinfo("Exported", "Summary exported to students_summary.txt")
    except Exception as e:
        messagebox.showerror("Error", f"Could not export: {e}")

# SIDEBAR BUTTONS (Used Online Resource)
sb_y_var = [110]
def sb_btn(text, cmd):
    b = tk.Label(sidebar, text=text, bg="#0f1724", fg="white", font=("Arial", 11), cursor="hand2")
    b.place(x=10, y=sb_y_var[0])
    sb_y_var[0] += 44
    b.bind("<Button-1>", lambda e: cmd())
    b.bind("<Enter>", lambda e: b.config(bg="#16202b"))
    b.bind("<Leave>", lambda e: b.config(bg="#0f1724"))
    return b

sb_btn("Dashboard", lambda: (update_dashboard(), show_page("dashboard", direction="left")))
sb_btn("Menu", lambda: show_page("menu", direction="right"))
sb_btn("Output", lambda: show_page("output", direction="left"))
sb_btn("Refresh", lambda: update_dashboard())

tk.Label(sidebar, text="Quick Actions", bg="#0f1724", fg="#9aa5b1", font=("Arial", 10)).place(x=20, y=420)
quick_y_var = [450]
def quick(text, cmd):
    lbl = tk.Label(sidebar, text=text, bg="#0f1724", fg="white", font=("Arial", 10), cursor="hand2")
    lbl.place(x=20, y=quick_y_var[0])
    quick_y_var[0] += 30
    lbl.bind("<Button-1>", lambda e: cmd())
    lbl.bind("<Enter>", lambda e: lbl.config(bg="#16202b"))
    lbl.bind("<Leave>", lambda e: lbl.config(bg="#0f1724"))

quick("Add Student", lambda: add_record_and_refresh())
quick("Sort Records", lambda: (sort_records(), update_dashboard()))

# BACKGROUND MUSIC AUTO
def play_bg_music():
    try:
        winsound.PlaySound(
            "Assessment 1 - Skills Portfolio/A1 - Resources/Exercise 3/smsbgs1.wav", # file path to sound
            winsound.SND_LOOP | winsound.SND_ASYNC
        )
    except:
        pass # If music file missing, just ignore

play_bg_music()

# STARTS THE APP
update_dashboard()                # Prepare charts on launch
put_frame_on_canvas(welcome, 0)   # Show welcome screen first
current_page = welcome
root.mainloop()                   # Start the GUI event loop