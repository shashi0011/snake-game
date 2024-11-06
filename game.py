import tkinter as tk
import random

# Global variables
GRID_SIZE = 20  # Size of the grid (20x20)
GRID_WIDTH = 40  # Number of columns
GRID_HEIGHT = 30  # Number of rows
SNAKE_COLOR = "#00FF00"  # Snake color (Green)
FOOD_COLOR = "#FF0000"  # Food color (Red)
BACKGROUND_COLOR = "#000000"  # Background color (Black)
FPS = 10  # Frames per second (speed of the game)

class SnakeGame:
    def __init__(self, master):
        self.master = master
        self.master.title("Snake Game")
        self.master.resizable(False, False)
        
        # Canvas to draw the game
        self.canvas = tk.Canvas(self.master, width=GRID_SIZE * GRID_WIDTH, height=GRID_SIZE * GRID_HEIGHT, bg=BACKGROUND_COLOR)
        self.canvas.pack()

        # Snake body list (each element is a tuple (x, y))
        self.snake = [(5, 5), (4, 5), (3, 5)]
        self.snake_direction = (1, 0)  # Moving right initially
        self.food = None  # Food position
        self.score = 0

        # Bind keys for snake movement
        self.master.bind("<Up>", self.change_direction)
        self.master.bind("<Down>", self.change_direction)
        self.master.bind("<Left>", self.change_direction)
        self.master.bind("<Right>", self.change_direction)

        # Start the game
        self.create_food()
        self.update_game()

    def create_food(self):
        """Randomly place food on the grid."""
        self.food = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
        # Ensure the food doesn't appear on the snake's body
        while self.food in self.snake:
            self.food = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))

    def change_direction(self, event):
        """Change snake's direction based on the key pressed."""
        if event.keysym == "Up" and self.snake_direction != (0, 1):
            self.snake_direction = (0, -1)
        elif event.keysym == "Down" and self.snake_direction != (0, -1):
            self.snake_direction = (0, 1)
        elif event.keysym == "Left" and self.snake_direction != (1, 0):
            self.snake_direction = (-1, 0)
        elif event.keysym == "Right" and self.snake_direction != (-1, 0):
            self.snake_direction = (1, 0)

    def update_game(self):
        """Update the game by moving the snake and checking for collisions."""
        # Move the snake
        head_x, head_y = self.snake[0]
        new_head = (head_x + self.snake_direction[0], head_y + self.snake_direction[1])
        
        # Handle wrap-around at the boundaries
        if new_head[0] < 0:
            new_head = (GRID_WIDTH - 1, new_head[1])  # Wrap around to the right
        elif new_head[0] >= GRID_WIDTH:
            new_head = (0, new_head[1])  # Wrap around to the left
        if new_head[1] < 0:
            new_head = (new_head[0], GRID_HEIGHT - 1)  # Wrap around to the bottom
        elif new_head[1] >= GRID_HEIGHT:
            new_head = (new_head[0], 0)  # Wrap around to the top

        # Check for collision with itself (body)
        if new_head in self.snake:
            self.game_over()
            return

        # Add the new head to the snake
        self.snake = [new_head] + self.snake[:-1]

        # Check if snake has eaten the food
        if new_head == self.food:
            self.snake.append(self.snake[-1])  # Add a new segment to the snake
            self.score += 1
            self.create_food()  # Create new food

        # Redraw the game
        self.redraw_game()

        # Call the update_game method again after a short delay (to make it look continuous)
        self.master.after(1000 // FPS, self.update_game)

    def redraw_game(self):
        """Redraw the entire game."""
        # Clear the canvas
        self.canvas.delete("all")

        # Draw the snake
        for x, y in self.snake:
            self.canvas.create_rectangle(x * GRID_SIZE, y * GRID_SIZE, (x + 1) * GRID_SIZE, (y + 1) * GRID_SIZE, fill=SNAKE_COLOR)

        # Draw the food
        food_x, food_y = self.food
        self.canvas.create_rectangle(food_x * GRID_SIZE, food_y * GRID_SIZE, (food_x + 1) * GRID_SIZE, (food_y + 1) * GRID_SIZE, fill=FOOD_COLOR)

        # Display the score
        self.canvas.create_text(GRID_SIZE * GRID_WIDTH - 50, 10, text=f"Score: {self.score}", fill="white", font=("Arial", 14))

    def game_over(self):
        """Display the game over message."""
        self.canvas.create_text(GRID_SIZE * GRID_WIDTH // 2, GRID_SIZE * GRID_HEIGHT // 2, text="GAME OVER", fill="red", font=("Arial", 24))
        self.canvas.create_text(GRID_SIZE * GRID_WIDTH // 2, GRID_SIZE * GRID_HEIGHT // 2 + 30, text=f"Final Score: {self.score}", fill="white", font=("Arial", 16))

        # Create a "Play Again" button
        self.play_again_button = tk.Button(self.master, text="Play Again", font=("Arial", 16), command=self.play_again)
        self.play_again_button.pack()

    def play_again(self):
        """Reset the game and start a new game."""
        self.snake = [(5, 5), (4, 5), (3, 5)]
        self.snake_direction = (1, 0)
        self.score = 0
        self.create_food()
        self.redraw_game()
        self.play_again_button.pack_forget()  # Hide the "Play Again" button
        self.update_game()  # Start the game again

# Create the Tkinter window and start the game
root = tk.Tk()
game = SnakeGame(root)
root.mainloop()
