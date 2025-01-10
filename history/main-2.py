import pyautogui
from pynput import keyboard
from pynput.keyboard import KeyCode
from playsound import playsound

class ScreenElement:
    def __init__(self, key, x, y):
        self.key = key
        self.x = x
        self.y = y


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
pause_keys = [keyboard.Key.shift, keyboard.Key.alt_l, "D"] # shift+alt+d : toggle pause
exit_keys = [keyboard.Key.shift, keyboard.Key.alt_l, "Q"] # shift+alt+q : exit
pressed_pause_keys = set()
pressed_exit_keys = set()
pressed_keys = set() # collection d'élément uniques non organisés
paused = False

def on_press(key):
    # print(key) # devtool to check keynames
    
    global paused # indique que la variable paused utilisée est celle définie dans le global, sinon il faudrait la passer en paramètre à la fonction
    
    # Gestion exit
    if key in [exit_keys[0], exit_keys[1]] or (hasattr(key, 'char') and key.char == exit_keys[2]) :  # Quand une des exit_keys pressed, la mettre dans pressed_exit_keys
        pressed_exit_keys.add(key)
    if (exit_keys[0] in pressed_exit_keys) and (exit_keys[1] in pressed_exit_keys) and any((hasattr(key_tmp, 'char') and key_tmp.char == exit_keys[2]) for key_tmp in pressed_exit_keys): # Si les 3 exit_keys sont dans pressed_exit_keys, exit
        print("Goodbye.")
        try :
            wave_obj = sa.WaveObject.from_wave_file("double_pop_low.wav")
            play_obj = wave_obj.play()
            # play_obj.wait_done() # Attendre que le son soit terminé
        except :
            print("Fichier 'pop.wav' introuvable.")
    
    # Gestion pause
    if key in [pause_keys[0], pause_keys[1]] or (hasattr(key, 'char') and key.char == pause_keys[2]) :
        pressed_pause_keys.add(key)
    if (pause_keys[0] in pressed_pause_keys) and (pause_keys[1] in pressed_pause_keys) and any((hasattr(key_tmp, 'char') and key_tmp.char == pause_keys[2]) for key_tmp in pressed_pause_keys):
        paused = not paused
        
        try :
            wave_obj = sa.WaveObject.from_wave_file("pop.wav")
            wave_obj.play()
        except Exception as e:
            print(f"Erreur : {e}")
        
        print("paused :", paused)
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
    
    # Pour les ctrl+alt+letter
    # (hasattr(key, 'vk') and key.vk == 81) # Check if key est un vk et si le vkCode est égal à 81
    # any((isinstance(key_tmp, KeyCode) and key_tmp.vk == 81) for key_tmp in pressed_exit_keys) # check if element is vkCode and if it is equals to the vkCode 81
    # any((hasattr(key_tmp, 'char') and key_tmp.char == "a") for key_tmp in pressed_exit_keys) # pareil mais pour les lettres



def on_release(key):
    # Lorsque la touche est relâchée, on la retire du set
    if key in pressed_keys:
        pressed_keys.remove(key)
    
    if key in pressed_pause_keys:
        pressed_pause_keys.remove(key)
        
    if key in pressed_exit_keys:
        pressed_exit_keys.remove(key)

def main():
    print("Hotkeys for Master Duel : Hello")
    
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()


if __name__ == "__main__":
    main()
