import pyautogui
import time
import os
from enum import Enum

PATH = os.path.abspath(".")
PATH_IMG = PATH + r"\img"

VAR_ATTACK_BUTTON_POSITION = None
VAR_PARTY_BUTTON_POSITION = None

PATH_BUTTON_ATTACK_IDLE = PATH_IMG+r"\attack_idle.png"
PATH_BUTTON_PARTY = PATH_IMG + r"\party.png"
PATH_ICON_COMBAT = PATH_IMG + r"\combat.png"
PATH_ICON_PARTY_COMBAT = PATH_IMG + r"\combat_party.png"

class PLAYER_ACTION(Enum):
    IDLE = 0
    COMBAT = 1
    PARTY_COMBAT = 2
    UNKNOW = 3


def SetButtonPosition(name_button, path):
    print(f"Configurando posición del botón {name_button}...")
    while True:
        resp = pyautogui.locateCenterOnScreen(image=path, confidence=0.75)
        print(resp)
        if resp != None:
            print(f"Posición del Botón {name_button}: {resp} ")
            return resp
        else:
            print("Posición no encontrada...")
        time.sleep(1)

def CheckPlayerAction():
    global PATH_ICON_COMBAT
    global PATH_ICON_PARTY_COMBAT

    print("Player status?")
    
    if pyautogui.locateOnScreen(image=PATH_ICON_COMBAT, confidence=0.65) is not None:
        print("Player en combate!")
        return PLAYER_ACTION.COMBAT
    
    if pyautogui.locateOnScreen(image=PATH_ICON_PARTY_COMBAT, confidence=0.65) is not None:
        print("Party en combate!")
        return PLAYER_ACTION.PARTY_COMBAT

    print("No sé! :|")
    return PLAYER_ACTION.UNKNOW

def PerformAttack():
    global PATH_BUTTON_ATTACK_IDLE
    global VAR_ATTACK_BUTTON_POSITION

    if pyautogui.locateOnScreen(PATH_BUTTON_ATTACK_IDLE, confidence=0.75) is None:
        pyautogui.moveTo(VAR_ATTACK_BUTTON_POSITION)
        pyautogui.click(VAR_ATTACK_BUTTON_POSITION)

def main():
    print("1) Party")
    print("2) Solo")
    value = input()

    if value == 1:
        ScriptParty()
    else:
        ScriptSolo()

def ScriptSolo():
    global VAR_ATTACK_BUTTON_POSITION
    global VAR_PARTY_BUTTON_POSITION
    global PATH_BUTTON_ATTACK_IDLE
    global PATH_BUTTON_PARTY
    

    VAR_ATTACK_BUTTON_POSITION = SetButtonPosition("ataque", PATH_BUTTON_ATTACK_IDLE)

    while True:
        
        #Script Temporal para sólo atacar según el botón de party

        PerformAttack()

        time.sleep(3) # tiempo prudencial cuando estoy haciendo debugging

def ScriptParty():
    
    global VAR_ATTACK_BUTTON_POSITION
    global VAR_PARTY_BUTTON_POSITION
    global PATH_BUTTON_ATTACK_IDLE
    global PATH_BUTTON_PARTY
    

    VAR_ATTACK_BUTTON_POSITION = SetButtonPosition("ataque", PATH_BUTTON_ATTACK_IDLE)
    VAR_PARTY_BUTTON_POSITION = SetButtonPosition("party", PATH_BUTTON_PARTY)

    while True:
        
        #Script Temporal para sólo atacar según el botón de party

        action = CheckPlayerAction()

        if action is PLAYER_ACTION.COMBAT:
            PerformAttack()
            time.sleep(1)
            continue

        if action is PLAYER_ACTION.PARTY_COMBAT:
            pyautogui.moveTo(VAR_PARTY_BUTTON_POSITION)
            pyautogui.click(VAR_PARTY_BUTTON_POSITION)
            time.sleep(0.2)
            pyautogui.moveTo(VAR_ATTACK_BUTTON_POSITION)
            time.sleep(0.2)
            pyautogui.click(VAR_ATTACK_BUTTON_POSITION)


        time.sleep(3) # tiempo prudencial cuando estoy haciendo debugging

if __name__=="__main__":
    main()
