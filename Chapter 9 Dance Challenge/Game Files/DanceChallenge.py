import pgzrun
from random import randint
from pgzero.builtins import Actor, keyboard

WIDTH = 800
HEIGHT = 600
CENTER_X = WIDTH / 2
CENTER_Y = HEIGHT / 2

move_list = []
display_list = []
score_p1 = 0  # Score for player 1
score_p2 = 0  # Score for player 2
current_move = 0
count = 4
dance_length = 4
say_dance = False
show_countdown = True
moves_complete = False
game_over = False

# Dancers
dancer_p1 = Actor("dancer-start")
dancer_p1.pos = CENTER_X - 100, CENTER_Y - 40  # Adjusted for two players
dancer_p2 = Actor("dancer-start")
dancer_p2.pos = CENTER_X + 100, CENTER_Y - 40  # Adjusted for two players

# Directional Actors for player 1
up_p1 = Actor("up")
up_p1.pos = CENTER_X - 100, CENTER_Y + 110
right_p1 = Actor("right")
right_p1.pos = CENTER_X + 60 - 100, CENTER_Y + 170
down_p1 = Actor("down")
down_p1.pos = CENTER_X - 100, CENTER_Y + 230
left_p1 = Actor("left")
left_p1.pos = CENTER_X - 60 - 100, CENTER_Y + 170

# Directional Actors for player 2 (WASD)
up_p2 = Actor("up")
up_p2.pos = CENTER_X + 100, CENTER_Y + 110
right_p2 = Actor("right")
right_p2.pos = CENTER_X + 60 + 100, CENTER_Y + 170
down_p2 = Actor("down")
down_p2.pos = CENTER_X + 100, CENTER_Y + 230
left_p2 = Actor("left")
left_p2.pos = CENTER_X - 60 + 100, CENTER_Y + 170

def draw():
    global game_over, score_p1, score_p2, say_dance, count, show_countdown
    if not game_over:
        screen.clear()
        screen.blit("stage", (0, 0))
        dancer_p1.draw()
        dancer_p2.draw()
        up_p1.draw()
        down_p1.draw()
        right_p1.draw()
        left_p1.draw()
        up_p2.draw()
        down_p2.draw()
        right_p2.draw()
        left_p2.draw()
        screen.draw.text(f"Score P1: {score_p1}", color="black", topleft=(10, 10))
        screen.draw.text(f"Score P2: {score_p2}", color="black", topleft=(10, 30))
        if say_dance:
            screen.draw.text("Dance!", color="black", topleft=(CENTER_X - 65, 150), fontsize=60)
        if show_countdown:
            screen.draw.text(str(count), color="black", topleft=(CENTER_X - 8, 150), fontsize=60)
    else:
        screen.clear()
        screen.blit("stage", (0, 0))
        screen.draw.text(f"Score P1: {score_p1}", color="black", topleft=(10, 10))
        screen.draw.text(f"Score P2: {score_p2}", color="black", topleft=(10, 30))
        screen.draw.text("GAME OVER!", color="black", topleft=(CENTER_X - 130, 220), fontsize=60)
        
def generate_moves():
    global move_list, display_list, dance_length, count
    global show_countdown, say_dance
    count = 4
    move_list = []
    say_dance = False
    for move in range(dance_length):
        rand_move = randint(0, 3)
        move_list.append(rand_move)
        display_list.append(rand_move)
    show_countdown = True
    countdown()


def reset_dancer(dancer, up, right, down, left):
    if not game_over:
        dancer.image = "dancer-start"  # Reset to initial image
        up.image = "up"
        right.image = "right"
        down.image = "down"
        left.image = "left"

def update_dancer(move, dancer, up, right, down, left):
    # Light up the current move
    if not game_over:
        if move == 0:
            up.image = "up-lit"
        elif move == 1:
            right.image = "right-lit"
        elif move == 2:
            down.image = "down-lit"
        elif move == 3:
            left.image = "left-lit"
        
        # Set the dancer's image to match the move (optional visual feedback)
        dancer.image = f"dancer-{['up', 'right', 'down', 'left'][move]}"

        # Schedule the reset function to revert visuals back to normal
        clock.schedule(lambda: reset_dancer(dancer, up, right, down, left), 0.5)


def display_moves():
    global display_list, dancer_p1, dancer_p2, up_p1, right_p1, down_p1, left_p1, up_p2, right_p2, down_p2, left_p2
    if display_list:
        this_move = display_list.pop(0)  # Get the first move from the list
        # Update dancers to the current move
        update_dancer(this_move, dancer_p1, up_p1, right_p1, down_p1, left_p1)
        update_dancer(this_move, dancer_p2, up_p2, right_p2, down_p2, left_p2)
        
        # Schedule reset and then call display_moves again after a delay
        clock.schedule(lambda: reset_dancer(dancer_p1, up_p1, right_p1, down_p1, left_p1), 0.5)
        clock.schedule(lambda: reset_dancer(dancer_p2, up_p2, right_p2, down_p2, left_p2), 0.5)
        
        if display_list:
            # Schedule the next move after a delay to allow current move to be visible
            clock.schedule(display_moves, 1)
        else:
            say_dance = True
            show_countdown = False
    else:
        say_dance = True
        show_countdown = False


def countdown():
    global count, game_over, show_countdown
    if count > 1:
        count -= 1
        clock.schedule(countdown, 1)
    else:
        show_countdown = False
        display_moves()

def on_key_up(key):
    global score_p1, score_p2, game_over, move_list, current_move
    if not game_over:
        # Check which player is making a move and update their dancer
        if key == keys.UP:
            player = (dancer_p1, up_p1, right_p1, down_p1, left_p1, score_p1)
        elif key == keys.RIGHT:
            player = (dancer_p1, up_p1, right_p1, down_p1, left_p1, score_p1)
        elif key == keys.DOWN:
            player = (dancer_p1, up_p1, right_p1, down_p1, left_p1, score_p1)
        elif key == keys.LEFT:
            player = (dancer_p1, up_p1, right_p1, down_p1, left_p1, score_p1)
        elif key == keys.W:
            player = (dancer_p2, up_p2, right_p2, down_p2, left_p2, score_p2)
        elif key == keys.D:
            player = (dancer_p2, up_p2, right_p2, down_p2, left_p2, score_p2)
        elif key == keys.S:
            player = (dancer_p2, up_p2, right_p2, down_p2, left_p2, score_p2)
        elif key == keys.A:
            player = (dancer_p2, up_p2, right_p2, down_p2, left_p2, score_p2)
        else:
            return

        update_dancer(move_list[current_move], *player[:-1])

        # Check if the move is correct
        if move_list[current_move] == {
            keys.UP: 0, keys.RIGHT: 1, keys.DOWN: 2, keys.LEFT: 3,
            keys.W: 0, keys.D: 1, keys.S: 2, keys.A: 3
        }.get(key, -1):
            if key in [keys.UP, keys.RIGHT, keys.DOWN, keys.LEFT]:
                score_p1 += 1  # Update score for player 1
            else:
                score_p2 += 1  # Update score for player 2
            next_move()  # Correct move, go to the next one
        else:
            game_over = True  # Incorrect move, end the game


def next_move():
    global dance_length, current_move, moves_complete
    if current_move < dance_length - 1:
        current_move += 1
    else:
        moves_complete = True
        

generate_moves()  # Starts the dance move generation when the game starts
music.play("vanishing-horizon")  # Play background music

def update():
    global game_over, current_move, moves_complete
    print("Update called, game_over status:", game_over)  # Debugging output
    if not game_over:
        if moves_complete:
            generate_moves()  # Regenerate dance moves when completed
            moves_complete = False
            current_move = 0
        # Additional logic ensuring game_over hasn't been set incorrectly
    else:
        print("Game over, stopping music.")  # Debugging output
        music.stop()  # Stop the music when the game is over

pgzrun.go()

