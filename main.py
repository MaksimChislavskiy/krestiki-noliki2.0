import tkinter as tk
from tkinter import messagebox, ttk


class TicTacToe:
    def __init__(self, root):
        self.root = root
        self.root.title('Крестики-нолики')
        self.root.geometry('400x500')
        self.root.resizable(False, False)

        # Настройки игры
        self.current_player = 'X'
        self.player_choice = 'X'
        self.game_count = 0
        self.scores = {'X': 0, 'O': 0}
        self.buttons = []

        # Стили
        self.style = ttk.Style()
        self.style.configure('TButton', font=('Arial', 20), padding=10)
        self.style.configure('Title.TLabel', font=('Arial', 16, 'bold'))
        self.style.configure('Score.TLabel', font=('Arial', 12))

        # Создание интерфейса
        self.create_widgets()

    def create_widgets(self):
        # Фрейм для заголовка и счетчика
        self.header_frame = ttk.Frame(self.root)
        self.header_frame.pack(pady=10)

        self.title_label = ttk.Label(self.header_frame, text="Крестики-нолики", style='Title.TLabel')
        self.title_label.grid(row=0, column=0, columnspan=2)

        self.score_label = ttk.Label(
            self.header_frame,
            text=f"X: {self.scores['X']} | O: {self.scores['O']} | Игры: {self.game_count}",
            style='Score.TLabel'
        )
        self.score_label.grid(row=1, column=0, columnspan=2, pady=5)

        # Фрейм для выбора символа
        self.choice_frame = ttk.Frame(self.root)
        self.choice_frame.pack(pady=5)

        ttk.Label(self.choice_frame, text="Выберите символ:").grid(row=0, column=0, columnspan=2)

        self.x_btn = ttk.Button(self.choice_frame, text="X", command=lambda: self.set_player('X'))
        self.x_btn.grid(row=1, column=0, padx=5)

        self.o_btn = ttk.Button(self.choice_frame, text="O", command=lambda: self.set_player('O'))
        self.o_btn.grid(row=1, column=1, padx=5)

        # Игровое поле
        self.game_frame = ttk.Frame(self.root)
        self.game_frame.pack(pady=10)

        for i in range(3):
            row = []
            for j in range(3):
                btn = ttk.Button(
                    self.game_frame,
                    text='',
                    width=5,
                    command=lambda r=i, c=j: self.on_click(r, c)
                )
                btn.grid(row=i, column=j, padx=5, pady=5)
                row.append(btn)
            self.buttons.append(row)

        # Кнопка сброса
        self.reset_btn = ttk.Button(self.root, text="Новая игра", command=self.reset_game)
        self.reset_btn.pack(pady=10)

        # Скрыть игровое поле до выбора символа
        self.game_frame.pack_forget()
        self.reset_btn.pack_forget()

    def set_player(self, choice):
        self.player_choice = choice
        self.current_player = 'X'  # X всегда ходит первым
        self.choice_frame.pack_forget()
        self.game_frame.pack(pady=10)
        self.reset_btn.pack(pady=10)

        # Обновить текст кнопок выбора
        self.x_btn.state(['disabled' if choice == 'X' else '!disabled'])
        self.o_btn.state(['disabled' if choice == 'O' else '!disabled'])

    def on_click(self, row, col):
        if self.buttons[row][col]['text'] != '':
            return

        self.buttons[row][col]['text'] = self.current_player

        if self.check_winner():
            winner = self.current_player
            self.scores[winner] += 1
            self.game_count += 1
            self.update_score()

            if self.scores[winner] >= 3:
                messagebox.showinfo('Игра окончена', f'Игрок {winner} победил в серии до 3 побед!')
                self.reset_series()
            else:
                messagebox.showinfo('Игра окончена', f'Игрок {winner} победил!')
                self.reset_game()
        elif self.check_draw():
            self.game_count += 1
            self.update_score()
            messagebox.showinfo('Игра окончена', 'Ничья!')
            self.reset_game()
        else:
            self.current_player = 'O' if self.current_player == 'X' else 'X'

    def check_winner(self):
        # Проверка строк
        for i in range(3):
            if self.buttons[i][0]['text'] == self.buttons[i][1]['text'] == self.buttons[i][2]['text'] != '':
                return True
        # Проверка столбцов
        for j in range(3):
            if self.buttons[0][j]['text'] == self.buttons[1][j]['text'] == self.buttons[2][j]['text'] != '':
                return True
        # Проверка диагоналей
        if self.buttons[0][0]['text'] == self.buttons[1][1]['text'] == self.buttons[2][2]['text'] != '':
            return True
        if self.buttons[0][2]['text'] == self.buttons[1][1]['text'] == self.buttons[2][0]['text'] != '':
            return True
        return False

    def check_draw(self):
        for row in self.buttons:
            for btn in row:
                if btn['text'] == '':
                    return False
        return True

    def reset_game(self):
        for row in self.buttons:
            for btn in row:
                btn['text'] = ''
        self.current_player = 'X'  # X всегда ходит первым

    def reset_series(self):
        self.scores = {'X': 0, 'O': 0}
        self.game_count = 0
        self.update_score()
        self.reset_game()

    def update_score(self):
        self.score_label.config(
            text=f"X: {self.scores['X']} | O: {self.scores['O']} | Игры: {self.game_count}"
        )


if __name__ == "__main__":
    root = tk.Tk()
    game = TicTacToe(root)
    root.mainloop()