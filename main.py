from tkinter import *
import math
# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20
ONE_MIN = 60
count_timer = ""
running = True
last_count = {
    "remaining_count": 0,
    "number_count": 0,
}
symbol = ""


# ---------------------------- TIMER RESET ------------------------------- # 
def reset_clicked():
    """This method runs once reset button is clicked"""
    global running, symbol
    last_count["number_count"] = 0
    window.after_cancel(count_timer)
    symbol = ""
    checkmark.config(text=symbol)
    timer_text.config(text="Timer", fg=GREEN)
    running = False
    countdown(0)
    start_button.config(command=start_clicked)


# ---------------------------- TIMER MECHANISM ------------------------------- #
def start_clicked():
    """This method runs once start button is clicked"""
    global running, symbol
    running = True
    work_secs = int(WORK_MIN * ONE_MIN)
    short_break_secs = int(SHORT_BREAK_MIN * ONE_MIN)
    long_break_secs = int(LONG_BREAK_MIN * ONE_MIN)
    last_count["number_count"] += 1
    start_button.config(command="")
    if last_count["number_count"] > 8:
        running = False
    elif last_count["number_count"] % 2 == 1:
        countdown(work_secs)
        timer_text.config(text="Work!", fg=GREEN)
    elif last_count["number_count"] == 8:
        countdown(long_break_secs)
        timer_text.config(text="Rest.", fg=RED)
    elif last_count["number_count"] % 2 == 0:
        countdown(short_break_secs)
        timer_text.config(text="Break", fg=PINK)


# ---------------------------- COUNTDOWN MECHANISM ------------------------------- #
# Another way
def handle_single_digit(number):
    """This method handles the display of single digit countdown."""
    if number < 10:
        number = f"0{number}"
    return number


def countdown(count):
    """This method activates the countdown sequence."""
    global symbol
    minutes = math.floor(count / 60)
    minutes = handle_single_digit(minutes)
    seconds = count % 60
    seconds = handle_single_digit(seconds)
    if count == 0 and last_count["number_count"] % 2 == 1:
        work_session = 1
        for _ in range(work_session):
            symbol += "✓"
        checkmark.config(text=symbol)
    if count == 0 and not running:
        canvas.itemconfigure(timer, text="00:00")
    elif count < 0:
        start_clicked()
    elif running:
        global count_timer
        canvas.itemconfigure(timer, text=f"{minutes}:{seconds}")
        count_timer = window.after(1000, countdown, count-1)
    last_count["remaining_count"] = count


# ---------------------------- UI SETUP ------------------------------- #
# Window
window = Tk()
window.title("Pomodoro Work App")
window.config(padx=100, pady=60, background=YELLOW)
# Canvas
canvas = Canvas(width=200, height=224, bg=YELLOW, highlightthickness=0)
tomato_img = PhotoImage(file="tomato.png")
canvas.create_image(100, 112, image=tomato_img)
timer = canvas.create_text(100, 133, text="00:00", fill="white", font=(FONT_NAME, 35, "bold"))
canvas.pack()
canvas.grid(row=1, column=1)
# Timer label
timer_text = Label(text="Timer", font=(FONT_NAME, 50, "normal"), fg=GREEN, bg=YELLOW)
timer_text.grid(row=0, column=1)
# timer_text.place(x=40, y=-43)
# Checkmark Label
checkmark = Label(font=(FONT_NAME, 30, "normal"), fg=GREEN, bg=YELLOW)
checkmark.grid(row=3, column=1)
# checkmark.place(x=90, y=227)
# Start Button
start_button = Button(text="Start", highlightbackground=YELLOW, width=4, command=start_clicked)
start_button.grid(row=3, column=0)
# start_button.place(x=-60, y=230)

# Reset Button
reset_button = Button(text="Reset", highlightbackground=YELLOW, width=4, command=reset_clicked)
reset_button.grid(row=3, column=2)
# reset_button.place(x=190, y=230)

window.mainloop()
