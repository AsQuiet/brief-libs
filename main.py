from briefpy import io, string, util, binary
import chunk
import os, sys
import zipfile

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
        if len(command) == 0:return
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
        if command[0] == "zip":self.IcaZip(command)
        if command[0] == "rename":self.IcaRename(command)
        if command[0] == "run":self.IcaRun(command)
        if command[0] == "read":self.IcaRead(command)
        if command[0] == "chunk":self.IcaChunk(command)
        
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
        
    def IcaZip(self, command):
        if "extract" in command:
            src = command[2]
            dst = command[3]
            print("src is " + src)
            with zipfile.ZipFile(self.get_path(src), 'r') as zip:
                zip.printdir()
                zip.extractall(self.get_path(dst))
                print("\nDone extracting...")
            return
        
        if "read" in command:
            src = command[2]
            with zipfile.ZipFile(self.get_path(src), 'r') as zip:
                zip.printdir()
            return

        
        toZip = command[1]
        dst = command[2]
        filePaths = self.get_all_file_paths(toZip)

        print("These files will be zipped to " + dst)
        for file in filePaths:
            print("      " + file)
        
        con = input("Continue? (Y/N) ")
        if con.lower() == "n":return
        
        with zipfile.ZipFile(self.get_path(dst), "w") as zip:
            for file in filePaths:
                print("Zipping file : " + file)
                zip.write(self.get_path(file), file)
        print("Zipping is done.")
            
    def IcaRename(self, command):
        file = command[1]
        new_name = command[2]
        os.rename(self.get_path(file), self.get_path(new_name))

    def IcaRun(self, command):
        file = command[1]
        timer = util.Timer()
        build_timer = None
        if file.endswith(".py"):
            self.cmd_os("python3 " + file, "python3 " + file)
        elif file.endswith(".c"):
            build_timer = util.Timer()
            self.cmd_os("cl " + file, "gcc " + file + " -o " + file[0:len(file) - 2])
            build_timer.stop()
            timer = timer = util.Timer()
            self.cmd_os(file[0:len(file) - 2], "./" + file[0:len(file) - 2])
        elif file.endswith(".cpp"):
            build_timer = util.Timer()
            self.cmd_os("cl " + file, "g++ " + file + " -o " + file[0:len(file) - 4])
            build_timer.stop()
            timer = timer = util.Timer()
            self.cmd_os(file[0:len(file) - 4], "./" + file[0:len(file) -4])
        timer.stop()
        if build_timer != None:
            print("\n\nBuild took : " + str(build_timer.get()) + " miliseconds")
        print("Program took : " + str(timer.get()) + " miliseconds.")
    
    def IcaRead(self, command):
        file = self.get_path(command[1])
        print("---------------------------")
        linecount = 0
        f = open(file, 'r')
        for line in f:
            linecount += 1
            print(binary.gen_buffer(3-len(str(linecount)))+str(linecount) + " |" + line.rstrip("\n"))
        print("---------------------------")
    
    def IcaChunk(self, command):
        file = self.get_path(command[1])
        timer = util.Timer()
        chunk.run(file)
        timer.stop()
        print("Program took : " + str(timer.get()) + " miliseconds.")

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
    
    def get_all_file_paths(self, directory): 
        # https://www.geeksforgeeks.org/working-zip-files-python/
        # initializing empty file paths list 
        file_paths = [] 
    
        # crawling through directory and subdirectories 
        for root, directories, files in os.walk(directory): 
            for filename in files: 
                # join the two strings in order to form the full filepath. 
                filepath = os.path.join(root, filename) 
                file_paths.append(filepath) 
    
        # returning all file paths 
        return file_paths 

    
if __name__ == "__main__":
    icarus = Icarus()
    icarus.get_input_loop()
