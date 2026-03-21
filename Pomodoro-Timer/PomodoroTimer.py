import time

def countdown(min,label):
    tot_sec = min * 60
    while tot_sec:
        mins,secs = divmod(tot_sec, 60)
        timer = f"{mins:02d}:{secs:02d}"
        print(f"{label} Timer:{timer}",end="\r")
        time.sleep(1)
        tot_sec -=1
    print(f"\n{label} finishes!!!")

def handle_pause_stop():
    while True:
        user_input = input("\nPress 'p' to pause, 's' to stop, or 'Enter' to continue: ").lower()

        if user_input == 'p':
            print("Timer paused. Press 'Enter' to resume: ")
            input()
        elif user_input == 's':
            print("Timer stopped.")
            return True # This indicates that the timer should stop
        else:
            return False # This indicates that the timer should continue
        
def repeat_or_end():
    user_input = input("\nCycle finished. Would you like to repeat the cycle? (y/n): ").lower()
    return user_input == 'y'

def promodoro_timer(work_min,short_break_min,long_break_min,cycle):
    for i in range(cycle):
        print(f"\nCycles {i+1} of {cycle}")
        countdown(work_min,"Work")
        if i < cycle-1:
            print("Starting short break...")
            if handle_pause_stop():
                return
            countdown(short_break_min,"Short Break")
        
        else:
            print("\nStarting long break...")
            if handle_pause_stop():
                return
            countdown(long_break_min,"Long Break")
            if not repeat_or_end():
                return


def get_valid_input(prompt):
    while True:
        try:
            value = int(input(prompt))
            if value <=0:
                raise ValueError
            return value
        except ValueError:
            print("Invlaid input, Please enter valid input.")


if __name__ == "__main__":
    work_min = get_valid_input("Enter work interval in minutes: ")
    short_break_min = get_valid_input("Enter short break interval in minutes: ")
    long_break_min = get_valid_input("Enter long break interval in miutes: ")
    cycle = get_valid_input("Enter the number of cycles: ")

    promodoro_timer(work_min,long_break_min,short_break_min,cycle)