import turtle
import random

# Game window size
WIDTH = 500
HEIGHT = 500
FOOD_SIZE = 10
DELAY = 100

offsets = {
    "up": (0, 20),
    "down": (0, -20),
    "left": (-20, 0),
    "right": (20, 0)
}

# Global variables
score = 0
high_score = 0
game_running = False  # to track if game is running


def reset():
    global snake, snake_direction, food_pos, pen, score, game_running
    score = 0
    update_scoreboard()
    snake = [[0, 0], [0, 20], [0, 40], [0, 60]]
    snake_direction = "up"
    food_pos = get_random_food_pos()
    food.goto(food_pos)
    game_running = True
    move_snake()


def move_snake():
    global snake_direction, score, high_score, game_running

    if not game_running:
        return

    # Next position for head of snake.
    new_head = snake[-1].copy()
    new_head[0] = snake[-1][0] + offsets[snake_direction][0]
    new_head[1] = snake[-1][1] + offsets[snake_direction][1]

    # Check self-collision
    if new_head in snake[:-1]:
        game_over()
        return
    else:
        snake.append(new_head)
        if not food_collision():
            snake.pop(0)
        else:
            score += 10
            if score > high_score:
                high_score = score
            update_scoreboard()

        # Allow screen wrapping
        if snake[-1][0] > WIDTH / 2:
            snake[-1][0] -= WIDTH
        elif snake[-1][0] < - WIDTH / 2:
            snake[-1][0] += WIDTH
        elif snake[-1][1] > HEIGHT / 2:
            snake[-1][1] -= HEIGHT
        elif snake[-1][1] < -HEIGHT / 2:
            snake[-1][1] += HEIGHT

        # Clear previous snake stamps
        pen.clearstamps()

        # Draw snake
        for segment in snake:
            pen.goto(segment[0], segment[1])
            pen.stamp()

        # Refresh screen
        screen.update()

        # Repeat
        turtle.ontimer(move_snake, DELAY)


def food_collision():
    global food_pos
    if get_distance(snake[-1], food_pos) < 20:
        food_pos = get_random_food_pos()
        food.goto(food_pos)
        return True
    return False


def get_random_food_pos():
    x = random.randint(- WIDTH // 2 + FOOD_SIZE, WIDTH // 2 - FOOD_SIZE)
    y = random.randint(- HEIGHT // 2 + FOOD_SIZE, HEIGHT // 2 - FOOD_SIZE)
    return (x, y)


def get_distance(pos1, pos2):
    x1, y1 = pos1
    x2, y2 = pos2
    return ((y2 - y1) ** 2 + (x2 - x1) ** 2) ** 0.5


def go_up():
    global snake_direction
    if snake_direction != "down":
        snake_direction = "up"


def go_right():
    global snake_direction
    if snake_direction != "left":
        snake_direction = "right"


def go_down():
    global snake_direction
    if snake_direction != "up":
        snake_direction = "down"


def go_left():
    global snake_direction
    if snake_direction != "right":
        snake_direction = "left"


def update_scoreboard():
    scoreboard.clear()
    scoreboard.goto(150, 210)
    scoreboard.write(f"Score: {score}  High Score: {high_score}", align="center", font=("Courier", 14, "bold"))


def game_over():
    global game_running
    game_running = False
    pen.clearstamps()
    screen.update()
    gameover_pen.goto(0, 0)
    gameover_pen.write("GAME OVER", align="center", font=("Courier", 30, "bold"))
    # Show menu again after Game Over
    screen.ontimer(show_menu, 2000)


# ----------------- MENU -----------------
def show_menu():
    screen.clear()
    screen.bgcolor("black")
    screen.title("Snake Game - Menu")

    menu_pen.clear()
    menu_pen.color("white")
    menu_pen.goto(0, 80)
    menu_pen.write("SNAKE GAME", align="center", font=("Courier", 24, "bold"))

    # Draw Start button
    menu_pen.goto(-40, 20)
    menu_pen.write("[ START ]", font=("Courier", 18, "bold"))

    # Draw Exit button
    menu_pen.goto(-30, -30)
    menu_pen.write("[ EXIT ]", font=("Courier", 18, "bold"))

    screen.update()

    # Enable click detection
    screen.onclick(menu_click)


def menu_click(x, y):
    if -60 < x < 60 and 10 < y < 40:  # Start button area
        start_game()
    elif -50 < x < 70 and -40 < y < -10:  # Exit button area
        turtle.bye()


def start_game():
    screen.clear()
    setup_game()
    reset()


# ----------------- SETUP -----------------
def setup_game():
    global pen, food, scoreboard, gameover_pen, menu_pen

    screen.bgcolor("black")
    screen.tracer(0)

    # Pen for snake
    pen = turtle.Turtle("square")
    pen.penup()
    pen.pencolor("yellow")

    # Food
    food = turtle.Turtle()
    food.shape("circle")
    food.color("red")
    food.shapesize(FOOD_SIZE / 20)
    food.penup()

    # Scoreboard
    scoreboard = turtle.Turtle()
    scoreboard.hideturtle()
    scoreboard.color("white")
    scoreboard.penup()

    # Game Over Pen
    gameover_pen = turtle.Turtle()
    gameover_pen.hideturtle()
    gameover_pen.color("red")
    gameover_pen.penup()

    # Menu Pen
    menu_pen = turtle.Turtle()
    menu_pen.hideturtle()
    menu_pen.color("white")
    menu_pen.penup()

    # Event handlers
    screen.listen()
    screen.onkey(go_up, "Up")
    screen.onkey(go_right, "Right")
    screen.onkey(go_down, "Down")
    screen.onkey(go_left, "Left")


# ----------------- MAIN -----------------
screen = turtle.Screen()
screen.setup(WIDTH, HEIGHT)
show_menu()
turtle.done()