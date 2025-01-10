import pyautogui
from pynput import keyboard

class ScreenElement:
    def __init__(self, key, x, y):
        self.key = key
        self.x = x
        self.y = y


def on_toggle_pause_hotkey():
    global paused
    paused = not paused
    print("paused :", paused)

def on_exit_hotkey():
    print("Goodbye.")
    global exiting_asked
    exiting_asked = True


def for_canonical(f):
    return lambda k: f(l.canonical(k)) # Jsp mais c'est pour les hotkeys. Voir https://pynput.readthedocs.io/en/latest/keyboard.html#global-hotkeys


def on_press(key):
    # print(key) # devtool to check keynames
    
    global paused, exiting_asked # indique que la variable paused utilisée est celle définie dans le global, sinon il faudrait la passer en paramètre à la fonction
    
    # Gestion des hotkeys
    for hotkey in hotkeys :
        for_canonical(hotkey.press)(key)

    if exiting_asked :
        return False
    if paused:
        return
    
    # Gestion click on key press
    for screen_element_name, screen_element in screen_elements.items():
        if (key == screen_element.key # pour les keys spéciales comme backspace
            or (hasattr(key, 'char') and key.char == screen_element.key) # pour les lettres et chiffres en str
            or (hasattr(key, 'vk') and key.vk == screen_element.key) # pour les numpad
        ):
            if key not in pressed_keys:
                print(key, "\t" , screen_element_name)
                pressed_keys.add(key)
                mouse_curr_x, mouse_curr_y = pyautogui.position()
                pyautogui.click(screen_element.x, screen_element.y)
                pyautogui.moveTo(mouse_curr_x, mouse_curr_y)

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
    "card_info": ScreenElement(keyboard.Key.space, 110, 320), # a
    "phase_switcher": ScreenElement("s", 1480, 480), # 1
    "battle_phase": ScreenElement("a", 1070, 780), # 2
    "main_phase2": ScreenElement("z", 1290, 780), # 3
    "end_phase": ScreenElement("e", 1510, 780), # 4
    "previous_arrow": ScreenElement("q", 80, 540), # q
    "next_arrow": ScreenElement("d", 1840, 540), # d
}
hotkeys = [
    keyboard.HotKey(
        keyboard.HotKey.parse('<shift>+<alt>+s'), # toggle pause hotkey
        on_toggle_pause_hotkey),
    keyboard.HotKey(
        keyboard.HotKey.parse('<shift>+<alt>+q'), # exit hotkey
        on_exit_hotkey),
]
pressed_keys = set() # collection d'élément uniques non organisés
paused = False
exiting_asked = False

if __name__ == "__main__":
    print("- Hotkeys for Master Duel -\n")
    print(
        "\ts : Switch phase\n"+
        "\ta : Battle phase\n"+
        "\tz : Main phase 2\n"+
        "\te : End phase\n"+
        "\tspace : Show card infos\n"+
        "\tq : Previous arrow\n"+
        "\td : Next arrow\n"+
        "\tshift+s : Pause\n"+
        "\tshift+q : Exit\n")
    
    with keyboard.Listener(
        on_press=on_press,
        on_release=on_release
    ) as l:
        l.join()