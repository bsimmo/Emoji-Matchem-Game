import os
from random import shuffle, randint
from guizero import App, Box, PushButton, Picture, Text, yesno, info
import time

'''
Welcome to the Future Learn, twp player EMOJI game
by Ben Simmons as part of the CPD course on Programming with GUIs by Raspberry Pi Foundation
'''

'''
in future this could move to a settings option
One player doesn't work yet (broke when it was expanded to two play) and more than 2 would need a GUI shuffle,
perhaps players info along the bottom, picture grids side by side.
'''
PLAYERS = 2   #Only option is 2 at the moment, but enables room for expansion.
COUNTDOWN_LIMIT = 20 #second for a players turn
GRID_MIN_MAX_SIZE = (3,6,3,4) # width min, max / height min/max
NUMBER_OF_TURNS = 3


def the_game():
    ''' Main game logic. Activated on Button Click
        Visual feedback used on buttons (disable/enable)
    '''
    txt_turns_completed.value = int(txt_turns_completed.value) + 1
    if int(txt_turns_completed.value) > 2 * NUMBER_OF_TURNS:
        game_over()
    
    else:
        if btn_play_game.enabled:  #initial start check (button will be enabled, disabled after)
            txt_turn.value = int(txt_turn.value) - 1 #turn to computer player numbers from human player numbers
            txt_turn.hide()
            btn_play_game.disable()
         # clean notification for previous player and popup box to let next player get ready.    
        txt_player_go[1 - int(txt_turn.value)].value = ""
        wait_next_player()
        bx_bottom_emoji.enable()
         # Game grid dimensions
        width = randint(GRID_MIN_MAX_SIZE[0], GRID_MIN_MAX_SIZE[1])
        height = randint(GRID_MIN_MAX_SIZE[2], GRID_MIN_MAX_SIZE[3])
         # need to remove all widgets, before we recreate them
        destroy_grids()
         # Generate Grids
        setup_grids(width, height)
        setup_round(width, height)
         # Indicate Player in play (-1 as we used human readable numbers at inital setup for get ready, now need to be 1 & 0)
        txt_player_go[int(txt_turn.value)].value = "YOUR\nGO"
        bx_player[int(txt_turn.value)].border = 4
        bx_player[int(txt_turn.value)].bg = "green yellow"
        txt_player_go[1-int(txt_turn.value)].value = "Wait\nTurn"
         # timers setup, find timer and countdown game timer
        txt_timer.hide()
        txt_countdown.value = COUNTDOWN_LIMIT
        txt_countdown.repeat(1000, countdown_timer)
        txt_timer.value = time.time()


def destroy_grids():
    '''
        Clears the images from the button, and then removes the button widgets from each box.
        This has to be done by removing them of the end each time, otherwise removal gets messed up.
        This has to be done to allow easy resizing fo grids.  Alternative could be to hide buttons and work around that.
    '''
    img_pictures.clear()
    btn_pictures.clear()
    for widget in reversed(bx_top_emoji.children):
        widget.destroy()
    for widget in reversed(bx_bottom_emoji.children):
        widget.destroy()    


def match_emoji(matched):
    ''' Logic to check when a play has matched the images or not, update screen with feedback/score
    '''
    txt_total_tries.value = int(txt_total_tries.value) + 1
    if matched:
        txt_result.value = "Well Done !"
        txt_total_correct.value = int(txt_total_correct.value) + 1
        play_matched()
        update_txt_player_score()
        the_game()
    else:       
        txt_result.value = "incorrect"


def play_matched():
    '''
        When a player matches a box, remove ability to select more (visual feedback)
        Provide the time it has taken and cancel the countdown
    '''
    bx_bottom_emoji.disable()
    txt_timer.value = f"Time taken {round(time.time() - float(txt_timer.value), 1)}s"
    txt_timer.show()
    print(txt_timer.value)
    txt_countdown.cancel(countdown_timer)


def update_txt_player_score():
    '''takes the central score and moves to the individual player scores
       txt_turn.value is used to keep track of the players go
       Have to cast everything to int() ans they are all stored as string()
    '''
    txt_player_score[int(txt_turn.value)].value = int(txt_player_score[int(txt_turn.value)].value) + int(txt_total_correct.value)
    txt_player_tries[int(txt_turn.value)].value = int(txt_player_tries[int(txt_turn.value)].value) + int(txt_total_tries.value)
    
    bx_player[int(txt_turn.value)].border = False
    bx_player[int(txt_turn.value)].bg = None
    txt_turn.value = 1 - int(txt_turn.value) #switch player  
    
    txt_countdown.value = "Get ready"
    txt_total_tries.value = "0"
    txt_total_correct.value = "0"
    


def setup_grids(width, height):
    ''' Generate grid of buttons in both boxes
    '''
    for x in range(width):
        for y in range(height):
            pic_image = Picture(bx_top_emoji, grid=[x,y])
            pic_button = PushButton(bx_bottom_emoji, command=match_emoji, args=[False], grid=[x,y])
            img_pictures.append(pic_image)        
            btn_pictures.append(pic_button)


def setup_round(width, height):
    ''' Set images and buttons to have a picture, remove from the list as we go.
        Set two images to be identical
    '''
    for pic_image in img_pictures:
        pic_image.image = emojis.pop()
        
    for pic_button in btn_pictures:
        pic_button.image = emojis.pop()

    match_button = randint(0, width*height - 1)
    btn_pictures[match_button].image = img_pictures[randint(0, width*height - 1)].image
    btn_pictures[match_button].update_command(match_emoji, [True])

    
def countdown_timer():
    '''Coundown timer logic, visual feedback with numbers and disable/enable controls
    '''
    txt_countdown.value = int(txt_countdown.value) - 1
    if int(txt_countdown.value) == 0:
        txt_countdown.cancel(countdown_timer)
        bx_bottom_emoji.disable()
        txt_result.value = "Too Slow"
        update_txt_player_score()
        the_game()
        
        
def wait_next_player():
    info("Get Ready...",f"Player {int(txt_turn.value) +1}.  It's your turn :-)") 


def game_over():
    ''' Show the games over and get ready to start again
    '''
    print("Game Over")
    bx_bottom_emoji.disable()
    txt_countdown.value = "GAME OVER"
    for player in range(PLAYERS):
        txt_player_go[player].value = "GAME OVER"
    
    btn_play_game.enable()
    
def close_game():
    if yesno("Close", "Do you want to quit?"):
            # need to stop the timer otherwise you see an error.
        txt_countdown.cancel(countdown_timer)
        app.destroy()


'''
set the path to the emoji folder on your computer
and create a shuffled list of the locations of the emoji images
'''
emojis_dir = "emojis"
emojis = [os.path.join(emojis_dir, f) for f in os.listdir(emojis_dir) if os.path.isfile(os.path.join(emojis_dir, f))]
shuffle(emojis)

 # picture object storage
img_pictures = []
btn_pictures = []

 # The App window
app=App("Emoji Match'em Game", width="700", height="765")


 # Create the boxes
bx_player = []
bx_top_emoji = Box(app, layout="grid", align="top", width=480, height=330)
bx_player.append(Box(app, layout="grid", align="left"))   #(box[0])
bx_player.append(Box(app, layout="grid", align="right"))  #(box[1])
bx_control = Box(app, layout="grid")
bx_bottom_emoji = Box(app, layout="grid", align="bottom", width=490, height=350)

 #bx_control parts
btn_play_game = PushButton(bx_control, text="Start Game", command=the_game, grid=[1,0])
txt_result = Text(bx_control, grid=[2,0])
txt_timer = Text(bx_control, grid=[3,0])
txt_total_tries_label = Text(bx_control, text="Tries", grid=[2,1])
txt_total_tries = Text(bx_control, text="0", grid=[3,1])
txt_countdown_label = Text(bx_control, text="Countdown :", grid=[0,2])
txt_countdown = Text(bx_control, text="Get ready player", grid=[1,2])
txt_total_correct = Text(bx_control, visible = False, text="0", grid=[3,2])
txt_turn = Text(bx_control, text= f"{randint(1,PLAYERS)}", grid=[1,3])
txt_turns_completed = Text(bx_control, visible = False, text=0, grid=[2,3])

#Player Areas (bx_player[] parts)
#enjoyed the grid logic to reverse to positions
txt_player_score_label = []
txt_player_score = []
txt_player_tries_label = []
txt_player_tries = []
txt_player_go = []
for player in range(PLAYERS):
    txt_player_score_label.append(Text(bx_player[player], text="Score", grid=[player,0]))
    txt_player_score.append(Text(bx_player[player], text="00", grid=[1-player,0]))
    txt_player_tries_label.append(Text(bx_player[player], text="Tries", grid=[player,1]))
    txt_player_tries.append(Text(bx_player[player], text="00", grid=[1-player,1]))
    txt_player_go.append(Text(bx_player[player], text=f"Welcome Player {player +1}", grid=[player,3]))

app.when_closed = close_game
app.display()
