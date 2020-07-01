import time, sys

try:
    import colorama
except:
    print("[Import-Error] Couldn't import the module 'colorama', color functions will not work.")

class VARS:
    """Global variables for the util.py lib, should not be accessed by user."""
    OUTPUT_CONSOLE = True

def get_milis_epoch():
    """Returns the amount of miliseconds since the epoch."""
    millis = int(round(time.time() * 1000))
    return millis

class Timer():
    
    GLOBAL_BEGIN = 0
    GLOBAL_END = 0

    def __init__(self):
        self.begin = get_milis_epoch()
        self.end = None
    
    def start(self):
        self.begin = get_milis_epoch()

    def stop(self):
        self.end = get_milis_epoch()
    
    def get(self):
        """Returns the time difference in miliseconds."""
        return self.end - self.begin
    
    @staticmethod
    def start_timer():
        Timer.GLOBAL_BEGIN = get_milis_epoch()
    
    @staticmethod
    def stop_timer():
        Timer.GLOBAL_END = get_milis_epoch()
    
    @staticmethod
    def get_timer():
        return Timer.GLOBAL_END - Timer.GLOBAL_BEGIN

# ------------------------------------------------------------------------------------------
#   CONSOLE CLASS
# ------------------------------------------------------------------------------------------

def console_output_sensitive(func):
    """Decorator that only calls the function if the console class should output stuff.""" 
    def inner(*args, **kwargs):
        if VARS.OUTPUT_CONSOLE:
            func(*args, **kwargs)
    return inner

class Console():
    """Simple console class."""
    try:
        RED = colorama.Fore.RED
        GREEN = colorama.Fore.GREEN
        BLUE = colorama.Fore.BLUE
        BLACK = colorama.Fore.BLACK
        WHITE = colorama.Fore.WHITE
        YELLOW = colorama.Fore.YELLOW
        PURPLE = colorama.Fore.MAGENTA
        ENDC = colorama.Fore.RESET
        CYAN = colorama.Fore.CYAN
    except:
        print("[Import-Error] Colors could not be loaded in.")
        RED = ""
        GREEN = ""
        BLUE = ""
        BLACK = ""
        WHITE = ""
        YELLOW = ""
        PURPLE = ""
        ENDC = ""
        CYAN = ""

    @staticmethod
    def input_vars_to_string(string, *args):
        current_arg = 0
        s_ = ""

        for i, char in enumerate(string):
            if char == "%" and i + 1< len(string):
                if string[i+1] == "v":
                    s_ += str(args[current_arg])
                    current_arg += 1
                    continue
            if char == "v" and i - 1 >= 0:
                if string[i-1] == "%":
                    continue
            
            s_ += char

        return s_

    @staticmethod
    @console_output_sensitive
    def print_line(s, *args):
        """Prints out all the given input to the same line."""
        s = Console.input_vars_to_string(s, *args)
        sys.stdout.write("\r" + str(s) + Console.ENDC)
        sys.stdout.flush()
    
    @staticmethod
    @console_output_sensitive
    def print(s, *args):
        """Standard print method that has a prefix and end, wich can customized. Use %v and a corresponding argument to apply it to the string => eg print('name is %v', 'larry')."""
        s = Console.input_vars_to_string(s, *args)
        print(str(s) + Console.ENDC)

    @staticmethod
    def set_output(output=True):
        """Should the console class output text."""
        VARS.OUTPUT_CONSOLE = output
    
    @staticmethod
    @console_output_sensitive
    def new_line():
        print("")



