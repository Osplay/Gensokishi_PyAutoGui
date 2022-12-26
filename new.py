import pyautogui
import time
import os
from enum import Enum

PATH = os.path.abspath(".")
PATH_IMG = PATH + r"\img"

VAR_ATTACK_BUTTON_POSITION = None
VAR_PARTY_BUTTON_POSITION = None
VAR_SCREEN_CENTER = None

PATH_BUTTON_ATTACK_IDLE = PATH_IMG+r"\attack_idle.png"
PATH_BUTTON_ATTACK = PATH_IMG+r"\attack.png"
PATH_BUTTON_NPC_TALK = PATH_IMG+r"\button_npc_talk.png"
PATH_BUTTON_PLAYER_TALK = PATH_IMG+r"\button_npc_talk.png"
PATH_BUTTON_PARTY = PATH_IMG + r"\party.png"
PATH_ICON_COMBAT = PATH_IMG + r"\combat.png"
PATH_ICON_PARTY_COMBAT = PATH_IMG + r"\combat_party.png"
PATH_ICON_NPC_ENEMEY = PATH_IMG+r"\icon_npc_enemy.png"

class PLAYER_ACTION(Enum):
    IDLE = 0
    COMBAT = 1
    PARTY_COMBAT = 2
    UNKNOW = 3

class PLAYER_DIRECTIONS(Enum):
    UP = 0,
    RIGHT = 1,
    DOWN = 2,
    LEFT = 3

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
    global PATH_BUTTON_PLAYER_TALK
    global PATH_BUTTON_NPC_TALK
    global VAR_ATTACK_BUTTON_POSITION

    if pyautogui.locateOnScreen(PATH_BUTTON_NPC_TALK, confidence=0.70) is not None:
        return
    if pyautogui.locateOnScreen(PATH_BUTTON_PLAYER_TALK, confidence=0.70) is not None:
        return
    if pyautogui.locateOnScreen(PATH_BUTTON_ATTACK_IDLE, confidence=0.70) is not None:
        return

    pyautogui.moveTo(VAR_ATTACK_BUTTON_POSITION)
    pyautogui.click(VAR_ATTACK_BUTTON_POSITION)

def ButtonExist(button, confidence):
    if pyautogui.locateAllOnScreen(image=button, confidence=confidence) is None:
        return False
    else:
        return True

def PlayerMoveSteps(direction, steps):
    #Uso la posición del centro
    global VAR_SCREEN_CENTER

    #muevo el puntero al medio
    pyautogui.moveTo(VAR_SCREEN_CENTER)

    #espero x tiempo
    time.sleep(0.2)

    var_player_x = VAR_SCREEN_CENTER[0]
    var_player_y = VAR_SCREEN_CENTER[1]

    #muevo x pixel hacia el lado indicado
    if direction == PLAYER_DIRECTIONS.UP:
        var_player_y -= steps
    elif(direction == PLAYER_DIRECTIONS.RIGHT):
        var_player_x += steps
    elif(direction == PLAYER_DIRECTIONS.DOWN):
        var_player_y += steps
    else:
        var_player_x -= steps

    pyautogui.moveTo(var_player_x, var_player_y)
    time.sleep(0.2)
    pyautogui.click()
    time.sleep(0.5)
        
# Start Script
def main():
    global VAR_SCREEN_CENTER

    temp_screen = pyautogui.size()
    VAR_SCREEN_CENTER = (round(temp_screen.width / 2), round(temp_screen.height / 2))


    print("1) Party")
    print("2) Solo")
    value = input()

    if value == "1":
        ScriptParty()
    else:
        ScriptSolo()


## Scripts --------
def ScriptSolo():
    global VAR_ATTACK_BUTTON_POSITION
    global VAR_PARTY_BUTTON_POSITION
    global PATH_BUTTON_ATTACK_IDLE
    global PATH_BUTTON_PARTY
    global PATH_ICON_NPC_ENEMEY
    

    VAR_ATTACK_BUTTON_POSITION = SetButtonPosition("ataque", PATH_BUTTON_ATTACK_IDLE)

    var_steps_min = 10 # minimum of step to move the mouse.
    var_place_to_torn = PLAYER_DIRECTIONS.UP # Posible directions of the player.

    while True:
        
        #Script Temporal para sólo atacar según el botón de party

        #Jugador está en combate.
        action = CheckPlayerAction()

        if action == PLAYER_ACTION.COMBAT:
            #Hacer ataque.
            PerformAttack()
        else:
            PerformAttack() # Intento realizar un ataque

            while ButtonExist(PATH_BUTTON_ATTACK_IDLE, 0.65) is True:
                #Muevo al jugador a la posición y reseteo
                PlayerMoveSteps(var_place_to_torn, var_steps_min)

                if var_place_to_torn == PLAYER_DIRECTIONS.UP:
                    var_place_to_torn = PLAYER_DIRECTIONS.RIGHT
                elif(var_place_to_torn == PLAYER_DIRECTIONS.RIGHT):
                    var_place_to_torn = PLAYER_DIRECTIONS.DOWN
                elif(var_place_to_torn == PLAYER_DIRECTIONS.DOWN):
                    var_place_to_torn = PLAYER_DIRECTIONS.LEFT
                else:
                    var_place_to_torn = PLAYER_DIRECTIONS.UP
                    var_steps_min += 2 #agregamos para movernos más espacios.
                
                PerformAttack() #Verificamos si se puede atacar
                time.sleep(0.5)

                action = CheckPlayerAction()

                if action == PLAYER_ACTION.COMBAT:
                    break

                #intentar ir hacia posición del npc más cercano.

                var_npc_location = pyautogui.locateOnScreen(image=PATH_ICON_NPC_ENEMEY, confidence=0.65)

                if var_npc_location is not None:
                    pyautogui.moveTo(var_npc_location)
                    time.sleep(0.2)
                    pyautogui.click()
            

        time.sleep(3) # tiempo prudencial cuando estoy haciendo debugging

def ScriptParty():
    
    global VAR_ATTACK_BUTTON_POSITION
    global VAR_PARTY_BUTTON_POSITION
    global PATH_BUTTON_ATTACK_IDLE
    global PATH_BUTTON_PARTY
    global VAR_SCREEN_CENTER
    

    VAR_ATTACK_BUTTON_POSITION = SetButtonPosition("ataque", PATH_BUTTON_ATTACK_IDLE)
    VAR_PARTY_BUTTON_POSITION = SetButtonPosition("party", PATH_BUTTON_PARTY)

    while True:
        
        #Script Temporal para sólo atacar según el botón de party

        action = CheckPlayerAction()

        if action is PLAYER_ACTION.COMBAT:
            print("En Combate!")
            PerformAttack()
            time.sleep(1)
            continue

        if action is PLAYER_ACTION.PARTY_COMBAT:
            print("Party peleando!")
            pyautogui.moveTo(VAR_PARTY_BUTTON_POSITION)
            pyautogui.click(VAR_PARTY_BUTTON_POSITION)
            time.sleep(0.2)
            pyautogui.moveTo(VAR_ATTACK_BUTTON_POSITION)
            pyautogui.click(VAR_ATTACK_BUTTON_POSITION)
            time.sleep(0.2)
            action = CheckPlayerAction()

            if action is not PLAYER_ACTION.COMBAT:
                pyautogui.moveTo(VAR_SCREEN_CENTER[0]+15, VAR_SCREEN_CENTER[1]+15)
                pyautogui.sleep(0.2)
                pyautogui.click()
                print("No está en el centro!")



        time.sleep(3) # tiempo prudencial cuando estoy haciendo debugging

if __name__=="__main__":
    main()
