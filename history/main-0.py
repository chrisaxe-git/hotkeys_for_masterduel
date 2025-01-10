import pyautogui
from pynput import keyboard
from pynput.keyboard import KeyCode

class ScreenElement:
    def __init__(self, key, x, y):
        self.key = key
        self.x = x
        self.y = y


def on_press(key):
    print(key) # devtool to check keynames
    
    global paused # indique que la variable paused utilisée est celle définie dans le global, sinon il faudrait la passer en paramètre à la fonction
    
    # Gestion exit
    if key in [exit_keys[0], exit_keys[1]] or (hasattr(key, 'vk') and key.vk == exit_keys[2]) : # Quand Ctrl ou alt ou p pressed, le mettre dans pressed_paused_keys
        pressed_pause_keys.add(key)
    if (keyboard.Key.ctrl_l in pressed_pause_keys) and (keyboard.Key.alt_l in pressed_pause_keys) and any((isinstance(key_tmp, KeyCode) and key_tmp.vk == 80) for key_tmp in pressed_pause_keys): # Si les 3 sont dans pressed_paused_keys, mettre sur pause
        paused = not paused
        print("paused :", paused)
        # wave_obj = sa.WaveObject.from_wave_file("pause_sound.wav")
        # wave_obj.play()
        print("hello :)")
    
    # Gestion pause
    if key in [keyboard.Key.ctrl_l, keyboard.Key.alt_l] or (hasattr(key, 'vk') and key.vk == 80) : # Quand Ctrl ou alt ou p pressed, le mettre dans pressed_paused_keys
        pressed_pause_keys.add(key)
    if (keyboard.Key.ctrl_l in pressed_pause_keys) and (keyboard.Key.alt_l in pressed_pause_keys) and any((isinstance(key_tmp, KeyCode) and key_tmp.vk == 80) for key_tmp in pressed_pause_keys): # Si les 3 sont dans pressed_paused_keys, mettre sur pause
        paused = not paused
        print("paused :", paused)
        # wave_obj = sa.WaveObject.from_wave_file("pause_sound.wav")
        # wave_obj.play()
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
    if key in pressed_pause_keys:
        pressed_pause_keys.remove(key)

def main():
    print("Hotkeys for Master Duel : On.")
    
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()


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
    # + pause : ctrl+alt+p (no need here)
    # + exit : ctrl+alt+p (no need here)
}
pause_keys = [keyboard.Key.ctrl_l, keyboard.Key.alt_l, 80] # ctrl+alt+p : toggle pause
exit_keys = [keyboard.Key.ctrl_l, keyboard.Key.alt_l, 81] # ctrl+alt+w : exit
pressed_keys = set() # collection d'élément uniques non organisés
pressed_pause_keys = set()
pressed_exit_keys = set()
paused = False


if __name__ == "__main__":
    main()
