import time
import threading
from pynput.keyboard import Key, Listener, KeyCode, Controller


keyboard = Controller()


class Vars:
    exit_key = Key.esc
    fn_key = KeyCode(char='`')
    enter_key = Key.enter
    function_key_1 = KeyCode(char='7')
    function_key_2 = KeyCode(char='8')
    function_key_3 = KeyCode(char='9')
    list_of_functions = [function_key_1, function_key_2, function_key_3]

function_choice = KeyCode(char='0')
global fn_pressed
fn_pressed = False

def open_shortcut_menu():
        keyboard.press(Key.backspace)
        time.sleep(0.2)
        keyboard.press(Key.backspace)
        keyboard.press(Key.alt)
        keyboard.press('/')
        time.sleep(0.4)

        keyboard.release(Key.alt)
        keyboard.release('/')

def apply_shortcut_menu():
        time.sleep(0.2)
        keyboard.press(Vars.enter_key)


class ClickKeyboard(threading.Thread):
    def __init__(self, function_choice, keyboard):
        super(ClickKeyboard, self).__init__()
        self.function_choice = function_choice
        self.keyboard = keyboard
        self.running = False
        self.program_running = True

    def start_applying(self):
        self.running = True

    def stop_applying(self):
        self.running = False

    def set_function_choice(self, fn_choice):
        self.function_choice = fn_choice

    def exit(self):
        self.stop_applying()
        self.program_running = False
    
    def apply_function_1(self):
        self.keyboard.type("Text color: black")
        apply_shortcut_menu()

    def apply_function_2(self):
        self.keyboard.type("Text color: #660000")
        apply_shortcut_menu()

    def apply_function_3(self):
        self.keyboard.type("Text color: #4a5d23")
        apply_shortcut_menu()

    def run(self):
        while self.program_running:
            while self.running:
                match self.function_choice:
                    case Vars.function_key_1:
                        self.apply_function_1()
                    case Vars.function_key_2:
                        self.apply_function_2()
                    case Vars.function_key_3:
                        self.apply_function_3()
                self.stop_applying()
            time.sleep(0.1)



click_thread = ClickKeyboard(function_choice, keyboard)
click_thread.start()


def on_press(key):
    global fn_pressed
    if key == Vars.exit_key:
        click_thread.exit()
        listener.stop()
    if key == Vars.fn_key:
        print("registered function key is active")

        # Set flag to track fn key press
        fn_pressed = True
    if fn_pressed and key in Vars.list_of_functions:
        #let me know you registered my input
        print("registered that you want to input")
        print(key)

        # Simulate Alt + / key press
        open_shortcut_menu()
        #next, simulate one of the key presses
        click_thread.set_function_choice(key)
        click_thread.start_applying()


def on_release(key):
    global fn_pressed
    if key == Vars.fn_key:
        # inactivate function key
        print("registered function key is inactive")
        fn_pressed = False


with Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()