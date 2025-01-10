import pyautogui
from pynput import keyboard

class ScreenElement:
    def __init__(self, key, x, y):
        self.key = key
        self.x = x
        self.y = y


def on_toggle_pause_hotkey():
    paused = not paused
    print("paused :", paused)

def on_exit_hotkey():
    print("Goodbye.")
    # return False


def for_canonical(f):
    return lambda k: f(l.canonical(k)) # Jsp mais c'est pour les hotkeys. Voir https://pynput.readthedocs.io/en/latest/keyboard.html#global-hotkeys


def on_press(key):
    # print(key) # devtool to check keynames
    
    global paused # indique que la variable paused utilisée est celle définie dans le global, sinon il faudrait la passer en paramètre à la fonction
    
    # Gestion des hotkeys
    for hotkey in hotkeys :
        for_canonical(hotkey.press)(key)
    
def on_release(key):
    # Lorsque la touche est relâchée, on la retire du set
    if key in pressed_keys:
        pressed_keys.remove(key)

    for hotkey in hotkeys :
        for_canonical(hotkey.release)(key)



# Keyboard inputs :
# plain letters : "é"
# keyboard.Key : .space .backspace
# key.vk : 96 à 105 pour numpad 0 à 9; 110 pour numpad.
screen_elements = {
    "card_info": ScreenElement("a", 110, 320), # a
    "phase_switcher": ScreenElement("&", 1480, 480), # 1
    "battle_phase": ScreenElement("é", 1070, 780), # 2
    "main_phase2": ScreenElement("\"", 1290, 780), # 3
    "end_phase": ScreenElement("'", 1510, 780), # 4
    "next_arrow": ScreenElement("d", 1840, 540), # d
    "previous_arrow": ScreenElement("q", 80, 540), # q
}
hotkeys = [
    keyboard.HotKey(
        keyboard.HotKey.parse('<shift>+<alt>+d'), # toggle pause hotkey
        on_toggle_pause_hotkey),
    keyboard.HotKey(
        keyboard.HotKey.parse('<shift>+<alt>+q'), # exit hotkey
        on_exit_hotkey),
]
pressed_keys = set() # collection d'élément uniques non organisés
paused = False


if __name__ == "__main__":
    print("- Hotkeys for Master Duel -")
    
    with keyboard.Listener(
        on_press=on_press,
        on_release=on_release
    ) as l:
        l.join()