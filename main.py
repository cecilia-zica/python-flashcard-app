from tkinter import *
import random
import pandas
# ---------------------------- CONSTANTS ------------------------------- #
BACKGROUND_COLOR = "#B1DDC6"
LEARNING_LANGUAGE = "Deutsch" #deve ser igual a primeira coluna do arquivo source_data.csv
TRADUCTION_LANGUAGE = "English" #deve ser igual a segunda coluna do arquivo source_data.csv
# ---------------------------- LOAD DATA ------------------------------- #
try:
    data = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    original_data = pandas.read_csv("data/source_data.csv")
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
    canvas.itemconfig(canvas_title, text=LEARNING_LANGUAGE, fill="black")
    canvas.itemconfig(canvas_word, text= current_card[LEARNING_LANGUAGE], fill="black", font=("Ariel", 45, "bold"),
                      width=780)
    canvas.itemconfig(canvas_image, image=card_front_img)

    flip_timer = window.after(3000, flip_card)

def flip_card():
    canvas.itemconfig(canvas_title, text=TRADUCTION_LANGUAGE, fill="white")
    canvas.itemconfig(canvas_word, text=current_card[TRADUCTION_LANGUAGE], fill="white", font=("Ariel", 45, "bold"), width=780)
    canvas.itemconfig(canvas_image, image=card_back_img)

def is_known():
    global to_learn
    # Remove a palavra da lista de "a aprender"
    if current_card in to_learn:
        to_learn.remove(current_card)

    # Salva a lista atualizada de palavras a aprender
    data_to_learn = pandas.DataFrame(to_learn)
    data_to_learn.to_csv("data/words_to_learn.csv", index=False)

    # Salva a palavra aprendida em outro arquivo
    try:
        learned_data = pandas.read_csv("data/words_learned.csv").to_dict(orient="records")
    except FileNotFoundError:
        learned_data = []

    learned_data.append(current_card)
    data_learned = pandas.DataFrame(learned_data)
    data_learned.to_csv("data/words_learned.csv", index=False)

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







