from briefpy import io, string, util
import os, sys

class Icarus():

    def __init__(self):
        self.dir_path = os.path.dirname(os.path.realpath(__file__))
        self.current_path = self.dir_path
        self.path = Icarus.switch_os("", "./")

        self.showpath = False

    #  Continously loop and get input. 
    def get_input_loop(self):
        user_input = input("nameless~" + ("" if not self.showpath else (" " + self.current_path + "~")) + " ")
        self.handle_user_input(user_input)
        self.get_input_loop()
    
    def handle_user_input(self, input_):
        # converting to a command
        command = self.extract_strings(input_)
        
        if command[0] == "clear":self.IcaClear()
        if command[0] == "exit":exit()
        if command[0] == "ls":self.IcaLs(command)
        if command[0] == "mk":self.IcaMake(command)
        if command[0] == "rm":self.IcaRemove(command)
        if command[0] == "mkdir":self.IcaMakeDir(command)
        if command[0] == "rmdir":self.IcaRemoveFolders(command)
        if command[0] == "cd": self.IcaCD(command)
        if command[0] == "showpath":self.showpath = (True if (command[1] == 'true') else False)
        if command[0] == "move":self.IcaMove(command)
        if command[0] == "copy":self.IcaCopy(command)
        
    def IcaClear(self):
        self.cmd_os("cls", "clear")

    def IcaLs(self, command):
        """Prints out a list of all the files in the given directory."""
        fp = self.current_path
        
        # should we ignore some files?
        filter_list = []
        if "-f" in command:
            filter_list = command[command.index("-f") + 1:]
        
        # the user might want to list the contents of another dir
        if (self.get_flag("ls", command) not in ("-f",None)):
            fp = self.get_flag("ls", command)

        # getting all the files
        d = os.listdir(fp)
        for file in d:
            canPrint = True
            for filter_ in filter_list:
                if filter_ in file:
                    canPrint = False
            if canPrint:print("     " + file)
        print("  ") 
    
    def IcaMake(self, command):
        files = command[1:]
        for file in files:
            f = open(self.get_path(file), "w")
            f.close()
        
    def IcaRemove(self, command):
        files = command[1:]
        for file in files:
            io.removeFile(self.get_path(file))
    
    def IcaMakeDir(self, command):
        folders = command[1:]
        for folder in folders:
            io.createFolder(self.get_path(folder))
    
    def IcaRemoveFolders(self, command):
        folders = command[1:]
        for folder in folders:
            io.removeFolder(self.get_path(folder))
    
    def IcaMove(self, command):
        src = self.get_path(command[1])
        dst = self.get_path(command[2])
        io.movePath(src, dst)
    
    def IcaCopy(self, command):
        src = self.get_path(command[1])
        dst = self.get_path(command[2])
        if (os.path.isdir(src)):
            io.copyFolder(src, dst)
        else:
            io.copyFile(src, dst)
        
    def IcaCD(self, command):
        new_path = command[1]
        if new_path == "..":
            self.current_path = os.path.dirname(self.current_path)
            return

        if os.path.exists(os.path.join(self.current_path, new_path)):
            self.current_path = os.path.join(self.current_path, new_path)
        elif os.path.exists(new_path):
            self.current_path = new_path
        else:
            print("The given path doesn't exist.")
        

    # ------------------------------------------------------------------------------ 
    # HELPER FUNCTIONS
    # ------------------------------------------------------------------------------

    @staticmethod
    def switch_os(windows_value, other_value):
        return windows_value if (os.name == "nt") else other_value
    
    @staticmethod
    def cmd_os(wnd, other):
        if os.name == "nt": os.system(wnd)
        else: os.system(other)
    
    def extract_strings(self, input_):
        """Extracts all of the needed commands and strings from the user's input."""
        commands = []
        in_string = False
        current_string = ""

        for x in range(len(input_)):
            char = input_[x]

            # if we come across one of these, enter string mode
            if char in ('"', "'"):
                if in_string:
                    in_string = False
                    commands.append(current_string)
                    current_string = ""
                    continue
                if not in_string:
                    in_string = True
                continue
            
            # should we add the current string?
            if char == " " and current_string != "" and not in_string:
                commands.append(current_string)
                current_string = ""
                continue
            
            # we dont want empty commands.
            if char == " " and not in_string:continue

            # adding
            current_string += char
        if current_string != "":commands.append(current_string)
        return commands
            

    def get_flag(self, flag, command):
        if (flag in command):
            try:
                return command[command.index(flag) + 1]
            except:return None
        return None
    
    def get_path(self, path):
        return os.path.join(self.current_path, path)

    
if __name__ == "__main__":
    icarus = Icarus()
    icarus.get_input_loop()
