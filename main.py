from tkinter import *
import random
import pandas
# ---------------------------- CONSTANTS ------------------------------- #
BACKGROUND_COLOR = "#B1DDC6"

# ---------------------------- LOAD DATA ------------------------------- #
try:
    data = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    original_data = pandas.read_csv("data/french_words.csv")
    to_learn = original_data.to_dict(orient="records")
else:
    to_learn = data.to_dict(orient="records")

current_card = {}
flip_timer = None

# ---------------------------- FUNCTIONS ------------------------------- #
def next_card():
    global flip_timer, current_card
    if flip_timer:
        window.after_cancel(flip_timer)

    current_card = random.choice(to_learn)
    canvas.itemconfig(canvas_title, text="French", fill="black")
    canvas.itemconfig(canvas_word, text= current_card["French"], fill="black")
    canvas.itemconfig(canvas_image, image=card_front_img)

    flip_timer = window.after(3000, flip_card)

def flip_card():
    canvas.itemconfig(canvas_title, text="English", fill="white")
    canvas.itemconfig(canvas_word, text=current_card["English"], fill="white")
    canvas.itemconfig(canvas_image, image=card_back_img)

def is_known():
    global to_learn
    to_learn.remove(current_card)
    data = pandas.DataFrame(to_learn)
    data.to_csv("data/words_to_learn.csv", index=False)
    next_card()


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Flashy")
window.config(padx=50, pady=50, bg= BACKGROUND_COLOR, highlightthickness=0)

# --- CANVAS ---
canvas = Canvas(width=800, height=526, highlightthickness=0, bg = BACKGROUND_COLOR, bd = 0)
card_front_img = PhotoImage(file="images/card_front.png")
card_back_img = PhotoImage(file="images/card_back.png")
canvas_image = canvas.create_image(400, 263, image=card_front_img)
canvas_title = canvas.create_text(400, 150, text="Title", font=("Ariel", 40, "italic"))
canvas_word = canvas.create_text(400, 263, text= "Word", font=("Ariel", 60, "bold"))
canvas.grid(row=0, column=0, columnspan=2)

right_button_img = PhotoImage(file="images/right.png")
right_button = Button(image=right_button_img, highlightthickness=0, command=is_known)
right_button.grid(row=1, column=1)

wrong_button_img = PhotoImage(file="images/wrong.png")
wrong_button = Button(image=wrong_button_img, highlightthickness=0, command=next_card)
wrong_button.grid(row= 1, column= 0)

next_card()

window.mainloop()







