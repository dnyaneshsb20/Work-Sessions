from tkinter import *
import math

# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"

WORK_MIN = 1
WORK_SEC = 0
SHORT_BREAK_MIN = 5
SHORT_BREAK_SEC = 0
LONG_BREAK_MIN = 20
LONG_BREAK_SEC = 0

reps = 0
timer = None

# ---------------------------- TIMER RESET ------------------------------- # 
def reset_timer():
    global timer, reps
    if timer is not None:
        window.after_cancel(timer)
    canvas.itemconfig(timer_text, text="00:00")
    title_label.config(text="Timer")
    check_marks.config(text="")
    reps = 0
    start_button.config(state="disabled")
    ask_for_times_popup()

# ---------------------------- TIMER MECHANISM ------------------------------- # 
def start_timer():
    global reps
    reps += 1

    work_sec_total = WORK_MIN * 60 + WORK_SEC
    short_break_sec_total = SHORT_BREAK_MIN * 60 + SHORT_BREAK_SEC
    long_break_sec_total = LONG_BREAK_MIN * 60 + LONG_BREAK_SEC

    if reps % 8 == 0:
        count_down(long_break_sec_total)
        title_label.config(text="Long Break", fg=RED)
    elif reps % 2 == 0:
        count_down(short_break_sec_total)
        title_label.config(text="Break", fg=PINK)
    else:
        count_down(work_sec_total)
        title_label.config(text="Work", fg=GREEN)

# ---------------------------- COUNTDOWN MECHANISM ------------------------------- # 
def count_down(count):
    count_min = math.floor(count / 60)
    count_sec = count % 60
    if count_sec < 10:
        count_sec = f"0{count_sec}"

    canvas.itemconfig(timer_text, text=f"{count_min}:{count_sec}")
    if count > 0:
        global timer
        timer = window.after(1000, count_down, count - 1)
    else:
        start_timer()
        marks = ""
        work_sessions = math.floor(reps / 2)
        for _ in range(work_sessions):
            marks += "✔"
        check_marks.config(text=marks)

# ---------------------------- POPUP TO ASK FOR TIMES ------------------------------- #
def ask_for_times_popup():
    def submit():
        global WORK_MIN, WORK_SEC, SHORT_BREAK_MIN, SHORT_BREAK_SEC, LONG_BREAK_MIN, LONG_BREAK_SEC

        try:
            work_min = int(work_min_entry.get())
            work_sec = int(work_sec_entry.get())
            short_min = int(short_min_entry.get())
            short_sec = int(short_sec_entry.get())
            long_min = int(long_min_entry.get())
            long_sec = int(long_sec_entry.get())
        except ValueError:
            error_label.config(text="Please enter valid integers!")
            return

        if not (0 <= work_sec < 60 and 0 <= short_sec < 60 and 0 <= long_sec < 60):
            error_label.config(text="Seconds must be between 0 and 59")
            return
        if not (1 <= work_min <= 120):
            error_label.config(text="Work minutes must be 1-120")
            return
        if not (0 <= short_min <= 60 and 0 <= long_min <= 60):
            error_label.config(text="Break minutes must be 0-60")
            return

        WORK_MIN, WORK_SEC = work_min, work_sec
        SHORT_BREAK_MIN, SHORT_BREAK_SEC = short_min, short_sec
        LONG_BREAK_MIN, LONG_BREAK_SEC = long_min, long_sec

        start_button.config(state="normal")
        popup.destroy()

    popup = Toplevel(window)
    popup.title("Set Times")
    popup.config(padx=20, pady=20, bg=YELLOW)

    # Center the popup on screen
    popup.update_idletasks()
    x = window.winfo_x() + (window.winfo_width() // 2) - (popup.winfo_reqwidth() // 2)
    y = window.winfo_y() + (window.winfo_height() // 2) - (popup.winfo_reqheight() // 2)
    popup.geometry(f"+{x}+{y}")

    # Force popup to be on top and block main window
    popup.transient(window)
    popup.grab_set()
    popup.focus_force()

    # Work time
    Label(popup, text="Work Time", bg=YELLOW, font=(FONT_NAME, 12, "bold")).grid(row=0, column=0, columnspan=4)
    Label(popup, text="Minutes:", bg=YELLOW, font=(FONT_NAME, 12)).grid(row=1, column=0, sticky="e")
    work_min_entry = Entry(popup, width=5)
    work_min_entry.grid(row=1, column=1)
    Label(popup, text="Seconds:", bg=YELLOW, font=(FONT_NAME, 12)).grid(row=1, column=2, sticky="e")
    work_sec_entry = Entry(popup, width=5)
    work_sec_entry.grid(row=1, column=3)

    # Short Break
    Label(popup, text="Short Break Time", bg=YELLOW, font=(FONT_NAME, 12, "bold")).grid(row=2, column=0, columnspan=4)
    Label(popup, text="Minutes:", bg=YELLOW, font=(FONT_NAME, 12)).grid(row=3, column=0, sticky="e")
    short_min_entry = Entry(popup, width=5)
    short_min_entry.grid(row=3, column=1)
    Label(popup, text="Seconds:", bg=YELLOW, font=(FONT_NAME, 12)).grid(row=3, column=2, sticky="e")
    short_sec_entry = Entry(popup, width=5)
    short_sec_entry.grid(row=3, column=3)

    # Long Break
    Label(popup, text="Long Break Time", bg=YELLOW, font=(FONT_NAME, 12, "bold")).grid(row=4, column=0, columnspan=4)
    Label(popup, text="Minutes:", bg=YELLOW, font=(FONT_NAME, 12)).grid(row=5, column=0, sticky="e")
    long_min_entry = Entry(popup, width=5)
    long_min_entry.grid(row=5, column=1)
    Label(popup, text="Seconds:", bg=YELLOW, font=(FONT_NAME, 12)).grid(row=5, column=2, sticky="e")
    long_sec_entry = Entry(popup, width=5)
    long_sec_entry.grid(row=5, column=3)

    error_label = Label(popup, text="", fg="red", bg=YELLOW)
    error_label.grid(row=6, column=0, columnspan=4)

    submit_button = Button(popup, text="Submit", command=submit)
    submit_button.grid(row=7, column=0, columnspan=4, pady=10)

    # This line blocks main window until popup is closed
    popup.wait_window()

# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Work Session")
window.config(padx=100, pady=50, bg=YELLOW)

title_label = Label(text="Timer", fg=GREEN, bg=YELLOW, font=(FONT_NAME, 50))
title_label.grid(column=1, row=0)

canvas = Canvas(width=200, height=224, bg=YELLOW, highlightthickness=0)
tomato_img = PhotoImage(file="tomato.png")
canvas.create_image(100, 112, image=tomato_img)
timer_text = canvas.create_text(100, 130, text="00:00", fill="white", font=(FONT_NAME, 35, "bold"))
canvas.grid(column=1, row=1)

start_button = Button(text="Start", highlightthickness=0, state="disabled", command=start_timer)
start_button.grid(column=0, row=2)

reset_button = Button(text="Reset", highlightthickness=0, command=reset_timer)
reset_button.grid(column=2, row=2)

check_marks = Label(bg=YELLOW, fg=GREEN)
check_marks.grid(column=1, row=3)

# Ask times at start
ask_for_times_popup()

window.mainloop()
