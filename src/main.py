import pyautogui
from pynput import keyboard
import pygetwindow as gw


class ScreenElement:
    def __init__(self, key, x, y):
        self.key = key
        self.x = x
        self.y = y


def on_press(key):
    # print(key) # devtool-off to check keynames
    
    global paused, exiting_asked # indique que la variable paused utilisée est celle définie dans le global, sinon il faudrait la passer en paramètre à la fonction
    
    # global_multi_hotkeys handling
    for global_multi_hotkey in global_multi_hotkeys :
        for_canonical(global_multi_hotkey.press)(key)
    if exiting_asked :
        return False
    if paused:
        return

    # Limit non-global hotkeys only to masterduel
    active_window = gw.getActiveWindow()
    if not (active_window.title == "masterduel") :
        return
    
    # Hotkeys handling
    for hotkey_dictkey, hotkey_value in hotkeys.items() :
        if (key == hotkey_value["key"] # pour les keys spéciales comme backspace
            or (hasattr(key, 'char') and key.char == hotkey_value["key"]) # pour les lettres et chiffres en str
            or (hasattr(key, 'vk') and key.vk == hotkey_value["key"]) # pour les virtual key codes (vk)
        ):
            if key not in pressed_keys:
                pressed_keys.add(key)
                
                match hotkey_value["action"] :
                    case "absolute_click" :
                        # print(key, "\t" , hotkey_dictkey) # devtool-off
                        
                        mouse_curr_x, mouse_curr_y = pyautogui.position()
                        pyautogui.click(hotkey_value["x"], hotkey_value["y"])
                        pyautogui.moveTo(mouse_curr_x, mouse_curr_y)
                        
                    case "relative_click" :
                        # print(key, "\t" , hotkey_dictkey) # devtool-off
                        
                        mouse_curr_x, mouse_curr_y = pyautogui.position()
                        new_x = mouse_curr_x + hotkey_value["x_offset"]
                        new_y = mouse_curr_y + hotkey_value["y_offset"]
                        pyautogui.click(new_x, new_y)
                        
                    case _ :
                        pass

def on_release(key):
    # Lorsque la touche est relâchée, on la retire du set
    if key in pressed_keys:
        pressed_keys.remove(key)

    for global_multi_hotkey in global_multi_hotkeys :
        for_canonical(global_multi_hotkey.release)(key)

def on_toggle_pause_hotkey():
    global paused
    paused = not paused
    print("paused :", paused)

def on_exit_hotkey():
    print("Goodbye.")
    global exiting_asked
    exiting_asked = True

def for_canonical(f):
    return lambda k: f(l.canonical(k)) # Jsp mais c'est pour les multi_hotkeys. Voir https://pynput.readthedocs.io/en/latest/keyboard.html#global-hotkeys


# Keyboard inputs : "é"; keyboard.Key.backspace; key.vk : 96 à 105 pour numpad 0 à 9; 110 pour numpad.
hotkeys = {
    # general
    "card_info": {
        "action" : "absolute_click",
        "key" : keyboard.Key.space,
        "x" : 110,
        "y" : 320,
    },
    "previous_arrow": {
        "action" : "absolute_click",
        "key" : "q",
        "x" : 80,
        "y" : 540,
    },
    "next_arrow": {
        "action" : "absolute_click",
        "key" : "d",
        "x" : 1840,
        "y" : 540,
    },

    # battle
    "phase_switcher": {
        "action" : "absolute_click",
        "key" : "s",
        "x" : 1480,
        "y" : 480,
    },
    "battle_phase": {
        "action" : "absolute_click",
        "key" : "a",
        "x" : 1070,
        "y" : 780,
    },
    "main_phase2": {
        "action" : "absolute_click",
        "key" : "z",
        "x" : 1290,
        "y" : 780,
    },
    "end_phase": {
        "action" : "absolute_click",
        "key" : "e",
        "x" : 1510,
        "y" : 780,
    },
    
    # deck
    "card_list_up" : {
        "action" : "relative_click",
        "key" : keyboard.Key.up,
        "x_offset" : 0,
        "y_offset" : -145,
    },
    "card_list_down" : {
        "action" : "relative_click",
        "key" : keyboard.Key.down,
        "x_offset" : 0,
        "y_offset" : 145,
    },
    "card_list_left" : {
        "action" : "relative_click",
        "key" : keyboard.Key.left,
        "x_offset" : -90,
        "y_offset" : 0,
    },
    "card_list_right" : {
        "action" : "relative_click",
        "key" : keyboard.Key.right,
        "x_offset" : 90,
        "y_offset" : 0,
    },
    "toggle_card_bookmark" : {
        "action" : "pass", # devtool-on Pas encore fait
        # "action" : "absolute_click",
        "key" : "!",
        "x" : 1510,
        "y" : 780,
    },
}
global_multi_hotkeys = [ # Global hotkeys can be used outside of masterduel too
    keyboard.HotKey(
        keyboard.HotKey.parse('<shift>+<alt>+s'), # toggle pause
        on_toggle_pause_hotkey),
    keyboard.HotKey(
        keyboard.HotKey.parse('<shift>+<alt>+q'), # exit
        on_exit_hotkey),
]

pressed_keys = set() # collection d'élément uniques non organisés
paused = False
exiting_asked = False


if __name__ == "__main__":
    print("- Hotkeys for Master Duel (v0.2.2) -\n")
    print(
        "General :\n"
        "space : Show card infos (general)\n"
        "q : Previous arrow (general)\n"
        "d : Next arrow (general)\n"
        "\n"
        "Deck :\n"
        "arrow keys : Navigate card list (deck)\n"
        # "! : Toggle card bookmark (deck)\n" # Pas encore prêt
        "\n"
        "Battle :\n"
        "s : Phase switcher (battle)\n"
        "a : Battle phase (battle)\n"
        "z : Main phase 2 (battle)\n"
        "e : End phase (battle)\n"
        "\n"
        "Script :\n"
        "shift+alt+s : Pause script\n"
        "shift+alt+q : Exit script\n"
    )
    
    with keyboard.Listener(
        on_press=on_press,
        on_release=on_release
    ) as l:
        l.join()