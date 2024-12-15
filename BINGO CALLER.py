from tkinter import Tk, ttk, Label, Entry
import random
import pyttsx3 as tts


def bingo_caller(numbers_on_window):
    if len(called_numbers) < 60:
        number = next(seed)
        called_numbers.append(number)

        last_five = called_numbers[-5:]
        numbers_on_window.configure(text='\n'.join(last_five))

        engine.say(number)
        engine.runAndWait()

    global updated_window
    updated_window = root.after(1500, lambda: bingo_caller(numbers_on_window))


def shuffled(iterable):
    return random.sample(iterable, len(iterable))


def main_interface():
    label = Label(root, text='No numbers.', font='Arial, 25', anchor='center', foreground='#4287f5', width=15)
    label.pack()

    button = create_button('Exit', lambda: destroy_main_window(label, button))

    return label


def create_button(text, command, **kwargs):
    button = ttk.Button(root, text=text, command=command)
    button.pack(**kwargs)
    return button


def destroy_main_window(label, button):
    root.after_cancel(updated_window)
    label.pack_forget()
    button.pack_forget()
    checking_window()


def checking_window():
    window_elements = []
    number_input = Entry(root, width=50)
    number_input.pack(padx=5, pady=10)
    window_elements.append(number_input)

    check_button = create_button('Verificar', lambda: check_number(number_input.get()))
    window_elements.append(check_button)

    text = 'Continuar el juego'
    continue_game_button = create_button(
        text=text,
        command=lambda: continue_game(window_elements, continue_game_button),
        padx=5,
        pady=10
    )
    return


def continue_game(window_elements, self_button):
    for element in window_elements:
        element.pack_forget()
    self_button.pack_forget()
    root.after(1000, lambda: bingo_caller(main_interface()))


def check_number(input_text):
    if input_text.isdigit():
        engine.say(("No", "Sí")[input_text in called_numbers])
        engine.runAndWait()


if __name__ == '__main__':
    engine = tts.init()
    root = Tk()
    root.title('BINGO CALLER v1.1')
    root.iconbitmap('img/bingo.ico')

    seed = map(str, shuffled(range(1, 61)))
    called_numbers = []

    voice = engine.getProperty('voices')[0].id
    properties = {
        "voice": voice,
        "rate": 110,
        "volume": 1.0
    }
    for name, value in properties.items():
        engine.setProperty(name, value)

    updated_window = root.after(1000, lambda: bingo_caller(main_interface()))

    root.mainloop()
