import time
import sys
import os

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def get_fish(frame):
    fish_frames = [
        r"""
       .
      .
     ><(((('>
        """,
        r"""
      .
     .
    ><(((('>
        """,
        r"""
     .
    .
   ><(((('>
        """
    ]
    return fish_frames[frame % len(fish_frames)]

def format_time(seconds):
    mins = seconds // 60
    secs = seconds % 60
    return f"{mins:02d}:{secs:02d}"

def focus_timer(duration_mins=25):
    duration_secs = duration_mins * 60
    start_time = time.time()
    
    try:
        while True:
            elapsed = int(time.time() - start_time)
            remaining = duration_secs - elapsed
            
            if remaining <= 0:
                break
            
            clear()
            print("=== FOCUS FISH TIMER ===")
            print(f"Goal: {duration_mins} minutes of focus.")
            print(get_fish(elapsed))
            print(f"Time Remaining: {format_time(remaining)}")
            print("\nPress Ctrl+C to cancel.")
            
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\nFocus session interrupted. The fish swims away...")
        sys.exit(0)

    clear()
    print("=== FOCUS FISH TIMER ===")
    print(r"""
       \O/
        |   CONGRATULATIONS!
       / \
    
    You finished your focus session!
    The fish is happy and well-fed.
    """)
    print("><(((('>  *bubbles*")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="A fishy Pomodoro timer.")
    parser.add_argument("--mins", type=int, default=25, help="Minutes to focus (default: 25)")
    args = parser.parse_args()
    
    focus_timer(args.mins)
