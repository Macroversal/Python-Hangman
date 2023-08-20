import tkinter as tk
from tkinter import messagebox, ttk
import random
import nltk

DIFFICULTY_INFO = {
    1: {"max_attempts": 6, "word_length": 4},
    2: {"max_attempts": 6, "word_length": 6},
    3: {"max_attempts": 6, "word_length": 8},
    4: {"max_attempts": 6, "word_length": 10},
    5: {"max_attempts": 6, "word_length": 12}
}

class HangmanGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Hangman Game")

        self.difficulty_input = tk.StringVar(value="1")
        self.word_list = {}
        self.chosen_word = ""
        self.guessed_letters = []
        self.max_attempts = 0
        self.current_attempts = 0
        self.win_count = 0
        self.loss_count = 0

        # Initialize the hangman_parts attribute
        self.hangman_parts = []

        self.victory_label = tk.Label(self.root, text="", font=("Arial", 16))
        self.victory_label.pack()

        self.create_widgets()
        self.load_word_list()
        self.start_game()
        self.create_letter_buttons()

    def draw_hangman(self):
        for part in self.hangman_parts:
            self.canvas.delete(part)
        self.hangman_parts = []

        if self.difficulty_input.get() and self.current_attempts > 0 and self.current_attempts <= self.max_attempts:
            x_center = 150
            y_base = 300
            scale = 30  # Scale factor for drawing

            for attempt in range(self.current_attempts):  # Corrected loop condition here
                if attempt == 0:
                    head = self.canvas.create_oval(x_center - scale, y_base - 3 * scale, x_center + scale,
                                                   y_base - scale)
                    self.hangman_parts.append(head)
                elif attempt == 1:
                    body = self.canvas.create_line(x_center, y_base - scale, x_center, y_base + 2 * scale)
                    self.hangman_parts.append(body)
                elif attempt == 2:
                    left_arm = self.canvas.create_line(x_center, y_base, x_center - 2 * scale, y_base - 2 * scale)
                    self.hangman_parts.append(left_arm)
                elif attempt == 3:
                    right_arm = self.canvas.create_line(x_center, y_base, x_center + 2 * scale, y_base - 2 * scale)
                    self.hangman_parts.append(right_arm)
                elif attempt == 4:
                    left_leg = self.canvas.create_line(x_center, y_base + scale, x_center - 2 * scale,
                                                       y_base + 3 * scale)
                    self.hangman_parts.append(left_leg)
                elif attempt == 5:
                    right_leg = self.canvas.create_line(x_center, y_base + scale, x_center + 2 * scale,
                                                        y_base + 3 * scale)
                    self.hangman_parts.append(right_leg)

            if self.current_attempts >= self.max_attempts:  # Draw eyes on the last attempt
                eye_radius = 5
                x_left_eye = x_center - 2 * scale
                x_right_eye = x_center + 2 * scale
                y_eye = y_base - 2 * scale

                left_eye = self.canvas.create_oval(x_left_eye - eye_radius, y_eye - eye_radius,
                                                   x_left_eye + eye_radius, y_eye + eye_radius, fill="black")

                right_eye = self.canvas.create_oval(x_right_eye - eye_radius, y_eye - eye_radius,
                                                    x_right_eye + eye_radius, y_eye + eye_radius, fill="black")

                self.hangman_parts.extend([left_eye, right_eye])
            self.canvas.update_idletasks()


    def create_letter_buttons(self):
        self.letter_buttons = []
        for letter in "abcdefghijklmnopqrstuvwxyz":
            button = tk.Button(self.root, text=letter.upper(), state=tk.NORMAL, command=lambda l=letter: self.choose_letter(l))
            self.letter_buttons.append(button)
            button.pack(side=tk.LEFT)

    def choose_letter(self, letter):
        if letter not in self.guessed_letters:
            self.guessed_letters.append(letter)
            self.update_progress()
            self.disable_letter_button(letter)
            self.check_victory()
            if letter not in self.chosen_word:
                self.current_attempts += 1
                self.update_attempts_label()
                self.draw_hangman()
                if self.current_attempts >= self.max_attempts:
                    self.victory_label.config(text=f"Game Over! The word was: {self.chosen_word}")
                    self.loss_count += 1  # Increment Loss count
                    self.choose_word()
                    self.update_progress()
                    self.update_word_length_label()
                    # Do NOT call draw_hangman here
        else:
            messagebox.showinfo("Duplicate Letter", "You've already chosen this letter.")

    def update_attempts_label(self):
        remaining_attempts = self.max_attempts - self.current_attempts
        attempts_label_text = f"Attempts left: {remaining_attempts}"
        self.attempts_label.config(text=attempts_label_text)

    def disable_letter_button(self, letter):
        index = ord(letter) - ord("a")
        self.letter_buttons[index].config(state=tk.DISABLED)

    def reset_letter_buttons(self):
        for button in self.letter_buttons:
            button.config(state=tk.NORMAL)


    def create_widgets(self):
        self.label = tk.Label(self.root, text="Welcome to Hangman!")
        self.label.pack()

        self.canvas = tk.Canvas(self.root, width=300, height=400)
        self.canvas.pack()

        self.difficulty_label = tk.Label(self.root, text="Choose difficulty:")
        self.difficulty_label.pack()

        self.difficulty_combobox = ttk.Combobox(self.root, textvariable=self.difficulty_input,
                                                values=list(DIFFICULTY_INFO.keys()))
        self.difficulty_combobox.pack()

        self.difficulty_label_var = tk.StringVar()
        self.difficulty_selected_label = tk.Label(self.root, textvariable=self.difficulty_label_var)
        self.difficulty_selected_label.pack()

        self.word_length_label = tk.Label(self.root, text="Word Length:")
        self.word_length_label.pack()

        self.progress_label = tk.Label(self.root, text="", font=("Arial", 16))
        self.progress_label.pack()

        self.attempts_label = tk.Label(self.root, text="", font=("Arial", 16))
        self.attempts_label.pack()

        self.leaderboard_label = tk.Label(self.root, text="Wins: 0 | Losses: 0")
        self.leaderboard_label.pack()

        self.give_up_button = tk.Button(self.root, text="Give Up", command=self.give_up)
        self.give_up_button.pack()

        self.new_game_button = tk.Button(self.root, text="New Game", command=self.new_game)
        self.new_game_button.pack()

    def load_word_list(self):
        for word in nltk.corpus.words.words():
            if word.isalpha() and len(word) >= 3:
                length = len(word)
                for difficulty in DIFFICULTY_INFO.keys():
                    self.word_list.setdefault(length, {}).setdefault(difficulty, []).append(word)

    def start_game(self):
        self.choose_word()
        self.update_progress()
        self.update_word_length_label()

    def choose_word(self):
        self.chosen_word = ""
        self.guessed_letters = []
        self.current_attempts = 0
        self.update_attempts_label()  # Reset attempts label
        self.draw_hangman()  # Clear hangman display

        progress = self.progress_label.cget("text").replace(" ", "")
        if "_" not in progress:
            self.victory_label.config(text="")

        if not self.victory_label.cget("text"):
            chosen_length = DIFFICULTY_INFO[int(self.difficulty_input.get())]["word_length"]
            self.chosen_word = random.choice(self.word_list[chosen_length][int(self.difficulty_input.get())])
            self.max_attempts = DIFFICULTY_INFO[int(self.difficulty_input.get())]["max_attempts"]

    def update_progress(self):
        if self.difficulty_input.get() == "":
            return

        if not self.chosen_word:
            chosen_length = DIFFICULTY_INFO[int(self.difficulty_input.get())]["word_length"]
            self.chosen_word = random.choice(self.word_list[chosen_length][int(self.difficulty_input.get())])
            self.max_attempts = DIFFICULTY_INFO[int(self.difficulty_input.get())]["max_attempts"]

        remaining_attempts = self.max_attempts - self.current_attempts
        attempts_label_text = f"Attempts left: {remaining_attempts}"
        self.attempts_label.config(text=attempts_label_text)

        progress = ""
        for letter in self.chosen_word:
            if letter in self.guessed_letters:
                progress += letter + " "
            else:
                progress += "_ "
        self.progress_label.config(text=progress)

        if "_" not in progress:
            self.win_count += 1  # Increment win count
            self.check_victory()
            self.choose_word()

    def update_word_length_label(self):
        word_length = len(self.chosen_word)
        self.word_length_label.config(text=f"Word Length: {word_length} Letters")

    def give_up(self):
        if self.chosen_word:
            self.victory_label.config(text=f"You gave up! The word was: {self.chosen_word}")
            self.choose_word()
            self.update_progress()
            self.update_word_length_label()

    def new_game(self):
        self.choose_word()
        self.update_progress()
        self.update_word_length_label()
        self.reset_letter_buttons()
        self.victory_label.config(text="")

    def check_victory(self):
        progress = self.progress_label.cget("text").replace(" ", "")
        if "_" not in progress:
            if not self.victory_label.cget("text"):  # Show message only once
                self.victory_label.config(text="Congratulations! You've guessed the word!")
                self.disable_all_letters()
                self.leaderboard_label.config(text=f"Wins: {self.win_count} | Losses: {self.loss_count}")

    def disable_all_letters(self):
        for button in self.letter_buttons:
            button.config(state=tk.DISABLED)

if __name__ == "__main__":
    root = tk.Tk()
    gui = HangmanGUI(root)
    root.mainloop()
