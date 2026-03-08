import curses
import random
import time

# Fish characters
FISH_RIGHT = "><(((º>"
FISH_LEFT = "<º)))><"
FISH_LENGTH = len(FISH_RIGHT)

# Food characters
FOOD_CHAR = "*"

class Fish:
    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.direction = direction # 1 for right, -1 for left
        self.speed = random.uniform(0.1, 0.4)
        self.last_move = time.time()
        self.hunger = 0 # 0 to 100
        self.mood = "Happy"

    def move(self, max_x):
        if time.time() - self.last_move > (1 / (self.speed * 10)):
            self.x += self.direction
            self.last_move = time.time()
            self.hunger = min(100, self.hunger + 0.1)
            
            if self.hunger > 70:
                self.mood = "Hungry"
            else:
                self.mood = "Happy"

            # Bounce off walls
            if self.x <= 1:
                self.direction = 1
                self.x = 1
            elif self.x >= max_x - FISH_LENGTH - 1:
                self.direction = -1
                self.x = max_x - FISH_LENGTH - 1

    def feed(self):
        self.hunger = max(0, self.hunger - 30)
        self.mood = "Happy"

def main(stdscr):
    # Initialize curses
    curses.curs_set(0)
    stdscr.nodelay(True)
    stdscr.timeout(100)
    
    # Colors
    curses.start_color()
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLUE) # Day
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLACK) # Night
    curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLUE) # Food
    curses.init_pair(4, curses.COLOR_RED, curses.COLOR_BLUE) # Hungry Fish
    
    current_color = 1
    is_day = True
    
    max_y, max_x = stdscr.getmaxyx()
    
    # Initialize fish
    fishes = [
        Fish(random.randint(2, max_x - FISH_LENGTH - 2), random.randint(2, max_y - 4), random.choice([-1, 1]))
        for _ in range(5)
    ]
    
    foods = []
    
    while True:
        max_y, max_x = stdscr.getmaxyx()
        
        # Clear screen with current color pair
        stdscr.bkgd(' ', curses.color_pair(current_color))
        stdscr.erase()
        
        # Draw water surface
        stdscr.addstr(0, 0, "~" * (max_x - 1))
        
        # Draw status
        status = f" [f] Feed | [n] Day/Night | [q] Quit | State: {'DAY' if is_day else 'NIGHT'}"
        stdscr.addstr(max_y - 2, 0, status[:max_x-1])
        
        # Draw fish
        for fish in fishes:
            fish.move(max_x)
            char = FISH_RIGHT if fish.direction == 1 else FISH_LEFT
            color = curses.color_pair(current_color)
            if fish.mood == "Hungry":
                 # Simple highlight if hungry (use red if day)
                 if is_day:
                     color = curses.color_pair(4)
            
            try:
                stdscr.addstr(int(fish.y), int(fish.x), char, color)
            except:
                pass # Prevent crash on resize
        
        # Draw food
        new_foods = []
        for fx, fy in foods:
            if fy < max_y - 3:
                # Check if any fish eats it
                eaten = False
                for fish in fishes:
                    if abs(fish.x + FISH_LENGTH/2 - fx) < 2 and abs(fish.y - fy) < 1:
                        fish.feed()
                        eaten = True
                        break
                
                if not eaten:
                    try:
                        stdscr.addstr(int(fy), int(fx), FOOD_CHAR, curses.color_pair(3))
                    except:
                        pass
                    new_foods.append((fx, fy + 0.2)) # Sinking slowly
        foods = new_foods
        
        # Handle input
        try:
            key = stdscr.getch()
            if key == ord('q'):
                break
            elif key == ord('f'):
                # Add food at the top
                foods.append((random.randint(2, max_x - 2), 1))
            elif key == ord('n'):
                is_day = not is_day
                current_color = 1 if is_day else 2
        except:
            pass
            
        stdscr.refresh()
        time.sleep(0.05)

if __name__ == "__main__":
    try:
        curses.wrapper(main)
    except KeyboardInterrupt:
        pass
