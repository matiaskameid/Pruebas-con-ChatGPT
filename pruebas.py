"""Simple Pong game using tkinter.

Controls:
- Player (left paddle) moves with 'w' (up) and 's' (down).
- The right paddle is controlled by a simple AI.

Run this file with Python to start the game.
"""

import random
import tkinter as tk


# Game configuration
WIDTH = 800
HEIGHT = 400
PADDLE_WIDTH = 10
PADDLE_HEIGHT = 80
BALL_SIZE = 20
PADDLE_SPEED = 10
BALL_SPEED = 5
AI_SPEED = 4


class PongGame:
    def __init__(self, master: tk.Tk) -> None:
        self.master = master
        self.canvas = tk.Canvas(master, width=WIDTH, height=HEIGHT, bg="black")
        self.canvas.pack()

        # Initialize paddles and ball
        self.player_y = HEIGHT // 2 - PADDLE_HEIGHT // 2
        self.ai_y = HEIGHT // 2 - PADDLE_HEIGHT // 2
        self.ball_x = WIDTH // 2 - BALL_SIZE // 2
        self.ball_y = HEIGHT // 2 - BALL_SIZE // 2
        self.ball_vx = random.choice([-BALL_SPEED, BALL_SPEED])
        self.ball_vy = random.choice([-BALL_SPEED, BALL_SPEED])

        self.left_score = 0
        self.right_score = 0

        # Key press state
        self.pressed_keys = set()

        # Draw initial objects
        self.draw_objects()
        self.update_scoreboard()

        # Bind key events
        master.bind("<KeyPress>", self.on_key_press)
        master.bind("<KeyRelease>", self.on_key_release)

        # Start the game loop
        self.game_loop()

    def draw_objects(self) -> None:
        self.canvas.delete("all")
        # Player paddle (left)
        self.player_paddle = self.canvas.create_rectangle(
            20,
            self.player_y,
            20 + PADDLE_WIDTH,
            self.player_y + PADDLE_HEIGHT,
            fill="white",
        )
        # AI paddle (right)
        self.ai_paddle = self.canvas.create_rectangle(
            WIDTH - 20 - PADDLE_WIDTH,
            self.ai_y,
            WIDTH - 20,
            self.ai_y + PADDLE_HEIGHT,
            fill="white",
        )
        # Ball
        self.ball = self.canvas.create_oval(
            self.ball_x,
            self.ball_y,
            self.ball_x + BALL_SIZE,
            self.ball_y + BALL_SIZE,
            fill="white",
        )

    def update_scoreboard(self) -> None:
        score_text = f"{self.left_score} : {self.right_score}"
        self.canvas.delete("score")
        self.canvas.create_text(
            WIDTH // 2,
            20,
            text=score_text,
            fill="white",
            font=("Helvetica", 24),
            tags="score",
        )

    def on_key_press(self, event: tk.Event) -> None:
        self.pressed_keys.add(event.keysym.lower())

    def on_key_release(self, event: tk.Event) -> None:
        self.pressed_keys.discard(event.keysym.lower())

    def move_player(self) -> None:
        if "w" in self.pressed_keys and self.player_y > 0:
            self.player_y -= PADDLE_SPEED
        if "s" in self.pressed_keys and self.player_y < HEIGHT - PADDLE_HEIGHT:
            self.player_y += PADDLE_SPEED

    def move_ai(self) -> None:
        center_ai = self.ai_y + PADDLE_HEIGHT / 2
        if center_ai < self.ball_y and self.ai_y < HEIGHT - PADDLE_HEIGHT:
            self.ai_y += AI_SPEED
        elif center_ai > self.ball_y + BALL_SIZE and self.ai_y > 0:
            self.ai_y -= AI_SPEED

    def move_ball(self) -> None:
        self.ball_x += self.ball_vx
        self.ball_y += self.ball_vy

        # Top/bottom collision
        if self.ball_y <= 0 or self.ball_y >= HEIGHT - BALL_SIZE:
            self.ball_vy = -self.ball_vy

        # Left paddle collision
        if (
            self.ball_x <= 20 + PADDLE_WIDTH
            and self.player_y <= self.ball_y + BALL_SIZE / 2 <= self.player_y + PADDLE_HEIGHT
        ):
            if self.ball_vx < 0:
                self.ball_vx = -self.ball_vx

        # Right paddle collision
        if (
            self.ball_x + BALL_SIZE >= WIDTH - 20 - PADDLE_WIDTH
            and self.ai_y <= self.ball_y + BALL_SIZE / 2 <= self.ai_y + PADDLE_HEIGHT
        ):
            if self.ball_vx > 0:
                self.ball_vx = -self.ball_vx

        # Score conditions
        if self.ball_x < 0:
            self.right_score += 1
            self.reset_ball(direction=1)
        elif self.ball_x > WIDTH - BALL_SIZE:
            self.left_score += 1
            self.reset_ball(direction=-1)

    def reset_ball(self, direction: int) -> None:
        self.ball_x = WIDTH // 2 - BALL_SIZE // 2
        self.ball_y = HEIGHT // 2 - BALL_SIZE // 2
        self.ball_vx = BALL_SPEED * direction
        self.ball_vy = random.choice([-BALL_SPEED, BALL_SPEED])
        self.update_scoreboard()

    def game_loop(self) -> None:
        self.move_player()
        self.move_ai()
        self.move_ball()
        self.draw_objects()
        self.update_scoreboard()
        self.master.after(16, self.game_loop)  # Roughly 60 FPS


def main() -> None:
    root = tk.Tk()
    root.title("Pong")
    PongGame(root)
    root.mainloop()


if __name__ == "__main__":
    main()
