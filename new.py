import pyautogui
import os
from enum import Enum

PATH = os.path.abspath(".")
PATH_IMG = PATH + r"\img"

VAR_ATTACK_BUTTON_POSITION = None
VAR_PARTY_BUTTON_POSITION = None
VAR_SCREEN_CENTER = None
VAR_REMOVE_BUTTON_POSITION = None
VAR_BUTTON_ATTACK_MONK = [None,None]

PATH_BUTTON_ATTACK_IDLE = PATH_IMG+r"\attack_idle.png"
PATH_BUTTON_ATTACK = PATH_IMG+r"\attack.png"
PATH_BUTTON_NPC_TALK = PATH_IMG+r"\button_npc_talk.png"
PATH_BUTTON_CLOSE_FOCUS = PATH_IMG+r"\button_close_focus.png"
PATH_BUTTON_PLAYER_TALK = PATH_IMG+r"\button_player_talk.png"
PATH_BUTTON_PARTY = PATH_IMG + r"\party.png"
PATH_ICON_COMBAT = PATH_IMG + r"\combat.png"
PATH_ICON_PARTY_COMBAT = PATH_IMG + r"\combat_party.png"
PATH_ICON_NPC_ENEMY = PATH_IMG+r"\icon_npc_enemy.png"
PATH_BUTTON_ATTACK_MONK = [PATH_IMG+r"\button_monk_attack_meditation.png", PATH_IMG+r"\button_monk_attack_martial_fist.png"]
PATH_BUTTON_OUTSCOPE_TALK = PATH_IMG + r"\outside_message.png"
PATH_BUTTON_OUTSCOPE_MARKET_CLOSE = PATH_IMG + r"\outside_close.png"
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

def SetButtonPosition(name_button, path, ignore_if_fail):
    print(f"Configurando posición del botón {name_button}...")
    while True:
        resp = pyautogui.locateCenterOnScreen(image=path, confidence=0.70)
        print(resp)
        if resp != None:
            print(f"Posición del Botón {name_button}: {resp} ")
            return resp
        else:
            print("Posición no encontrada...")

        pyautogui.sleep(1)

        if ignore_if_fail is True:
            break

def OutScope():
    global PATH_BUTTON_OUTSCOPE_TALK
    global PATH_BUTTON_OUTSCOPE_MARKET_CLOSE

    if pyautogui.locateOnScreen(PATH_BUTTON_OUTSCOPE_TALK, confidence=0.80) is not None:
        
        try_max_to_check = 2
        try_check = 0

        while True:

            if try_check >= try_max_to_check:
                break

            if pyautogui.locateOnScreen(VAR_BUTTON_OUTSCOPE_TALK, confidence= 0.8) is not None:
                pyautogui.press("enter")
                pyautogui.sleep(0.3)
            else:
                try_check = try_check+1
    
    quit = pyautogui.locateOnScreen(PATH_BUTTON_OUTSCOPE_MARKET_CLOSE, confidence=0.7)
    if quit is not None:
        pyautogui.moveTo(quit)
        pyautogui.sleep(0.3)
        pyautogui.click()
            


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
    global PATH_BUTTON_ATTACK
    global VAR_BUTTON_ATTACK_MONK
    global PATH_BUTTON_ATTACK_MONK

    if pyautogui.locateOnScreen(PATH_BUTTON_ATTACK, confidence=0.70) is not None:
        pyautogui.press("enter")
        return
    if pyautogui.locateOnScreen(PATH_BUTTON_NPC_TALK, confidence=0.90) is not None:
        pyautogui.press('esc')
        return
    if pyautogui.locateOnScreen(PATH_BUTTON_PLAYER_TALK, confidence=0.70) is not None:
        pyautogui.press('esc')
        return

    for x in range(len(PATH_BUTTON_ATTACK_MONK)):
        if VAR_BUTTON_ATTACK_MONK[x] is not None and pyautogui.locateOnScreen(PATH_BUTTON_ATTACK_MONK[x], confidence=0.75) is not None:
            pyautogui.moveTo(VAR_BUTTON_ATTACK_MONK[x])
            pyautogui.sleep(0.4)
            pyautogui.click(VAR_BUTTON_ATTACK_MONK[x])
        else:
          VAR_BUTTON_ATTACK_MONK[x] = SetButtonPosition("ataque meditation monk", PATH_BUTTON_ATTACK_MONK[x], True)

    if pyautogui.locateOnScreen(PATH_BUTTON_ATTACK_IDLE, confidence=0.70) is not None:
        return

    pyautogui.press('enter')
    pyautogui.sleep(0.3)


def RemoveFocusMouse(): # deprecated
    global PATH_BUTTON_CLOSE_FOCUS
    global VAR_REMOVE_BUTTON_POSITION

    if VAR_REMOVE_BUTTON_POSITION is None:
        
        location = pyautogui.locateCenterOnScreen(image=PATH_BUTTON_CLOSE_FOCUS, confidence=0.70)
        
        if location is None:
            return
        
        VAR_REMOVE_BUTTON_POSITION = location

    pyautogui.moveTo(VAR_REMOVE_BUTTON_POSITION)
    pyautogui.sleep(0.2)
    pyautogui.click()

def ButtonExist(button, confidence):
    if pyautogui.locateAllOnScreen(image=button, confidence=confidence) is None:
        return False
    else:
        return True

def PlayerMoveStepsMouse(direction, steps):
    #Uso la posición del centro
    global VAR_SCREEN_CENTER

    #espero x tiempo
    pyautogui.sleep(0.2)

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
    pyautogui.sleep(0.2)
    pyautogui.click()
    pyautogui.sleep(0.5)

def PlayerMoveStepsKeyboard(direction, steps_in_seconds):
    key = None

    if direction == PLAYER_DIRECTIONS.UP:
        key = 'w'
    elif(direction == PLAYER_DIRECTIONS.RIGHT):
        key = 'd'
    elif(direction == PLAYER_DIRECTIONS.DOWN):
        key = 's'
    else:
        key = 'a'

    pyautogui.keyDown(key)
    pyautogui.sleep(steps_in_seconds)
    pyautogui.keyUp(key)
    pyautogui.sleep(0.5)

def NextMovementTorn(torn_to):

    if torn_to == PLAYER_DIRECTIONS.UP:
        return PLAYER_DIRECTIONS.RIGHT
    elif(torn_to == PLAYER_DIRECTIONS.RIGHT):
        return PLAYER_DIRECTIONS.DOWN
    elif(torn_to == PLAYER_DIRECTIONS.DOWN):
        return PLAYER_DIRECTIONS.LEFT
    else:
        return PLAYER_DIRECTIONS.UP


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
    global PATH_ICON_NPC_ENEMY
    global VAR_BUTTON_ATTACK_MONK
    global PATH_BUTTON_ATTACK_MONK

    VAR_ATTACK_BUTTON_POSITION = SetButtonPosition("ataque", PATH_BUTTON_ATTACK_IDLE, False)

    for x in range(len(PATH_BUTTON_ATTACK_MONK)):
        print(x)
        VAR_BUTTON_ATTACK_MONK[x] = SetButtonPosition("ataque meditation monk", PATH_BUTTON_ATTACK_MONK[x], True)

    var_steps_min = 0.5 # minimum of step to move the mouse.
    var_place_to_torn = PLAYER_DIRECTIONS.UP # Posible directions of the player.

    pyautogui.press('up') #Seteo el selector de enemigos y no players.

    while True:
        
        PerformAttack()
        
        action = CheckPlayerAction()

        if action != PLAYER_ACTION.COMBAT:

            for x in range(6):
                pyautogui.press("d")
                pyautogui.sleep(0.4)
                PerformAttack()

            PlayerMoveStepsKeyboard(var_place_to_torn, 0.3
)
            var_place_to_torn = NextMovementTorn(var_place_to_torn)
            PerformAttack()

            OutScope()
                


def ScriptParty():
    
    global VAR_ATTACK_BUTTON_POSITION
    global VAR_PARTY_BUTTON_POSITION
    global PATH_BUTTON_ATTACK_IDLE
    global PATH_BUTTON_PARTY
    global VAR_SCREEN_CENTER
    

    VAR_ATTACK_BUTTON_POSITION = SetButtonPosition("ataque", PATH_BUTTON_ATTACK_IDLE, False)
    VAR_PARTY_BUTTON_POSITION = SetButtonPosition("party", PATH_BUTTON_PARTY, False)

    while True:
        
        #Script Temporal para sólo atacar según el botón de party

        action = CheckPlayerAction()

        if action is PLAYER_ACTION.COMBAT:
            print("En Combate!")
            PerformAttack()
            pyautogui.sleep(1)
            continue

        if action is PLAYER_ACTION.PARTY_COMBAT:
            print("Party peleando!")
            pyautogui.moveTo(VAR_PARTY_BUTTON_POSITION)
            pyautogui.click(VAR_PARTY_BUTTON_POSITION)
            pyautogui.sleep(0.2)
            pyautogui.moveTo(VAR_ATTACK_BUTTON_POSITION)
            pyautogui.click(VAR_ATTACK_BUTTON_POSITION)
            pyautogui.sleep(0.2)
            action = CheckPlayerAction()

            if action is not PLAYER_ACTION.COMBAT:
                pyautogui.moveTo(VAR_SCREEN_CENTER[0]+50, VAR_SCREEN_CENTER[1]+50)
                pyautogui.sleep(0.2)
                pyautogui.click()
                print("No está en el centro!")



        pyautogui.sleep(3) # tiempo prudencial cuando estoy haciendo debugging

if __name__=="__main__":
    main()
