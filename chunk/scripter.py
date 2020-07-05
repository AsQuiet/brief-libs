import chunk.string as string
from chunk.preprocessor import Preprocessor
import math

def shell_print(s):
    print(str(s))
    # print(str(s))
def debug_print(s):
    if False:
        print("[DEBUG] " + str(s))

class Script():
    def __init__(self, script_arr):
        self.script_arr = script_arr
    
    @staticmethod
    def split(line):
        arr = []

        current_value = ""

        # for string tokenazation
        in_string = False

        for x in range(len(line)):
            char = line[x]

            if char == " " and not string.isempty(current_value) and not in_string:
                arr.append(current_value)
                current_value = ""
                continue  
            
            # checking for special characters '$'
            if x > 0 and (char == "'" or char == "'"):
                if line[x - 1] == "$":
                    current_value += char
                    continue
            
            if char == "$":
                if line[x - 1] == "$":
                    current_value += char
                    continue
                continue

            if char == '"' or char == "'":
                if in_string:in_string = False
                else: in_string = True

            # checking for other tokens
            if char == ":" and not in_string:
                arr.append(current_value)
                current_value = ""
                arr.append(char)
                continue

            if char == "," and not in_string:
                arr.append(current_value)
                current_value = ""
                continue

            current_value += char

        if not string.isempty(current_value):arr.append(current_value)

        return arr 
    
    @staticmethod
    def check_front(line, n):
        if len(line) < len(n):return False
        for x in range(len(n)):
            if n[x].lower() != line[x].lower():
                return False
        return True 

# ------------------------------------------------------------------------------------------
#       ---SCRIPTER---
# ------------------------------------------------------------------------------------------

class Scripts():

    VAR_SCRIPT      = Script(["COMMAND", "VAR_NAME", "VAR_VALUE"])
    VAR_SCRIPT2     = Script(["COMMAND", "VAR_NAME", "FUNCTION_NAME", "&:", "##ARGUMENTS"])
    VAR_SCRIPT3     = Script(["COMMAND", "VAR_NAME", "CHUNK_NAME", "&:", "&:", "&:","CHUNK_VAR"])
    VAR_SCRIPT4     = Script(["COMMAND", "VAR_NAME", "CHUNK_NAME", "&:", "&:", "&:", "FUNCTION_NAME", "&:", "##ARGUMENTS"])
    VAR_SCRIPT5     = Script(["COMMAND", "VAR_NAME", "VAR1_NAME", "OPERATOR", "VAR2_NAME"])
    VAR_SCRIPT6     = Script(["COMMAND", "VAR_NAME", "VAR1_NAME", "OPERATOR", "VAR2_NAME"])
    FUNCTION_CALL   = Script(["COMMAND", "FUNCTION_NAME", "&:", "##ARGUMENTS"])
    DEFINE_CHUNK    = Script(["COMMAND", "CHUNK_NAME", "&:", "&:"])
    DEFINE_FUNCTION = Script(["COMMAND", "FUNCTION_NAME", "&:", "&:","&:", "##ARGUMENTS"])
    RETURN_VALUE    = Script(["COMMAND", "RETURN_VALUE"])
    CHUNK_CALL      = Script(["COMMAND", "CHUNK_NAME", "&:", "&:", "&:", "FUNCTION_NAME", "&:", "##ARGUMENTS"])
    END             = Script(["COMMAND", "TARGET"])
    REASSIGN        = Script(["COMMAND", "VAR_NAME", "VAR_VALUE"])
    IF_             = Script(["COMMAND", "CONDITION"])
    LIST_0          = Script(["COMMAND", "LIST_NAME", "##LIST_VALUES"])

class Scripter():
    # used in error handling
    CURRENT_LINE = -1
    @staticmethod
    def apply_script(line, script):
        line_data = {}
        line_keywords = Script.split(line)

        try:
            for x in range(len(script.script_arr)):
                script_key = script.script_arr[x]


                if script_key in ("VAR_NAME", "FUNCTION_NAME"):
                    line_keywords[x] = string.remove_characters(line_keywords[x], [" "])

                # stands for symbol
                if "&" in script_key:continue
                # means that all following data should be put in an array
                if "##" in script_key:
                    arr = []
                    i = x
                    while True:
                        try:
                            arr.append(line_keywords[i])
                        except:
                            break
                        i += 1
                    line_data[script_key] = arr
                    break

                # general rule
                line_data[script_key] = line_keywords[x]
                if script_key == "COMMAND":
                    line_data[script_key] = line_keywords[x].upper()

            
            line_data["LINE"] = Scripter.CURRENT_LINE
        except:
            Scripter.error("error extracting data from line.", Scripter.CURRENT_LINE)
            return None
        return line_data

    @staticmethod
    def error(s, n=-1):
        print("Scripter Error : line " + str(n) + ", " + s)

    @staticmethod
    def select_script(line, num=-1):
        Scripter.CURRENT_LINE = num

        if Script.check_front(line, "CCALL"):       return Scripter.apply_script(line, Scripts.VAR_SCRIPT2)
        if Script.check_front(line, "COP"):         return Scripter.apply_script(line, Scripts.VAR_SCRIPT5)
        if Script.check_front(line, "CON"):         return Scripter.apply_script(line, Scripts.VAR_SCRIPT6)
        if Script.check_front(line, "CHUNK"):       return Scripter.apply_script(line, Scripts.DEFINE_CHUNK)
        if Script.check_front(line, "CALL"):        return Scripter.apply_script(line, Scripts.FUNCTION_CALL)
        if Script.check_front(line, "C>>"):         return Scripter.apply_script(line, Scripts.VAR_SCRIPT4)
        if Script.check_front(line, "C>"):          return Scripter.apply_script(line, Scripts.VAR_SCRIPT3)
        if Script.check_front(line, "C"):           return Scripter.apply_script(line, Scripts.VAR_SCRIPT)
        if Script.check_front(line, "END"):         return Scripter.apply_script(line, Scripts.END)
        if Script.check_front(line, "D"):           return Scripter.apply_script(line, Scripts.DEFINE_FUNCTION)
        if Script.check_front(line, "RETURN"):      return Scripter.apply_script(line, Scripts.RETURN_VALUE)
        if Script.check_front(line, "R"):           return Scripter.apply_script(line, Scripts.REASSIGN)
        if Script.check_front(line, ">"):           return Scripter.apply_script(line, Scripts.CHUNK_CALL)
        if Script.check_front(line, "LIST"):        return Scripter.apply_script(line, Scripts.LIST_0)
        if Script.check_front(line, "IF"):          return Scripter.apply_script(line, Scripts.IF_)
             
        Scripter.error("the given command is undefined.", num)
        return None
    

class Visitor():

    GLOBAL_MEMORY = {}
    GLOBAL_DEFINITIONS = {}

    # used to store argument values for functions
    TEMP_MEMORY = {}

    # used to change the way variables are put into memory depending on the scope
    CURRENT_SCOPE = ""
    CURRENT_FUNCTION = ""

    @staticmethod
    def error(s,n=-1):
        print("Interpreter error : line " + str(n) + ", " + str(s))

    @staticmethod
    def parse(scripts, function_name=None):
        
        ifs = 0

        for command in scripts:

            # end command?
            if command["COMMAND"] == "END":
                if command["TARGET"] == "IF" and Visitor.CURRENT_FUNCTION == "":
                    ifs -= 1 if ifs > 0 else 0
                    continue
                Visitor.handle_end(command)

            if Visitor.CURRENT_FUNCTION != "":
                Visitor.GLOBAL_MEMORY[Visitor.CURRENT_FUNCTION][1].append(command)
                continue

            if command["COMMAND"] == "IF":
                condition = Visitor.get_value(command["CONDITION"])
                if not condition:
                    ifs += 1
            
            if ifs != 0:
                continue
    
            if command["COMMAND"] == "RETURN" and function_name != None:
                for key in Visitor.GLOBAL_MEMORY.keys():
                    if Visitor.GLOBAL_MEMORY[key] == function_name:
                        Visitor.GLOBAL_MEMORY[key] = Visitor.get_value(command["RETURN_VALUE"])

            if command["COMMAND"] == "R":
                Visitor.handle_reassign(command)


            # chunk function is being called
            if command["COMMAND"] == ">":
                if command["CHUNK_NAME"] == "root":
                    Visitor.handle_root_calls(command)
                else:
                    Visitor.handle_chunk_calls(command)
            
            # should we create a chunk
            if command["COMMAND"] == "CHUNK":
                Visitor.handle_chunk_creation(command)

            # variable is being created
            if command["COMMAND"] in ("C", "CCALL", "COP", "C>", "C>>", "CON"):
                if command["COMMAND"] == "C>>":
                    if command["CHUNK_NAME"] == "root":
                        Visitor.handle_root_calls(command)
                        continue
                Visitor.handle_assignments(command)

            if command["COMMAND"] == "D":
                Visitor.handle_function_creation(command)
            
            if command["COMMAND"] == "CALL":
                Visitor.handle_function_calls(command)
            
            if command["COMMAND"] == "LIST":
                Visitor.handle_array_creation(command)
            
        debug_print(Visitor.GLOBAL_MEMORY)

    @staticmethod
    def handle_root_calls(command):
        debug_print("\nhandling root calls...")
    
        arg_values = []
        if command["COMMAND"] != "C>>":
            for a in command["##ARGUMENTS"]:
                arg_values.append(Visitor.get_value(a))
        
        
        if command["FUNCTION_NAME"] == "print":
            if len(arg_values) == 1:
                shell_print(arg_values[0])
            else:
                # arguments for print function are => "somestring %v"
                current_arg_index = 0
                text = ""

                for x in range(len(arg_values[0])):
                    char = arg_values[0][x]
                    # should a variable be placed here? => add next argument in list and skip this char
                    if char == "%" and x + 1 < len(arg_values[0]):
                        if arg_values[0][x+1] == "v":
                            current_arg_index += 1
                            text += str(arg_values[current_arg_index])
                            continue         
                    # is this "v" coming from a "%"? => ignore     
                    if char == "v" and x - 1 >= 0:
                        if arg_values[0][x-1] == "%":
                            continue
                    text += char
                
                shell_print(text)

        if command["FUNCTION_NAME"] == "list_remove_first":
            arr_name = arg_values[0]
            if len(Visitor.GLOBAL_MEMORY[arr_name]) != 0:
                Visitor.GLOBAL_MEMORY[arr_name].pop(0)
        
        if command["FUNCTION_NAME"] == "list_remove_last":
            arr_name = arg_values[0]
            if len(Visitor.GLOBAL_MEMORY[arr_name]) != 0:
                Visitor.GLOBAL_MEMORY[arr_name].pop(len(Visitor.GLOBAL_MEMORY[arr_name])-1)
        
        if command["FUNCTION_NAME"] == "list_remove_index":
            arr_name = arg_values[0]
            Visitor.GLOBAL_MEMORY[arr_name].pop(int(arg_values[1]))

        if command["FUNCTION_NAME"] == "list_append":
            arr_name = arg_values[0]
            el = arg_values[1]
            Visitor.GLOBAL_MEMORY[arr_name].append(el)

        if command["FUNCTION_NAME"] == "list_append_at":
            arr_name = arg_values[0]
            el = arg_values[1]
            index = int(arg_values[2])
            Visitor.GLOBAL_MEMORY[arr_name].insert(index, el)

        # C>>
        if command["FUNCTION_NAME"] == "list_get_length":
            arr_name = Visitor.get_value(command["##ARGUMENTS"])
            var_name = command["VAR_NAME"]
            Visitor.GLOBAL_MEMORY[var_name] = len(Visitor.GLOBAL_MEMORY[arr_name])
        
        if command["FUNCTION_NAME"] == "list_get_element":
            arr_name = Visitor.get_value(command["##ARGUMENTS"][0])
            arr_index = int(Visitor.get_value(command["##ARGUMENTS"][1]))
            arr_element = Visitor.GLOBAL_MEMORY[arr_name][arr_index]

            Visitor.GLOBAL_MEMORY[command["VAR_NAME"]] = arr_element
        
        if command["FUNCTION_NAME"] == "list_get_index":
            arr_name = Visitor.get_value(command["##ARGUMENTS"][0])
            arr_element = Visitor.get_value(command["##ARGUMENTS"][1])
            arr_index = Visitor.GLOBAL_MEMORY[arr_name].index(arr_element)
            
            Visitor.GLOBAL_MEMORY[command["VAR_NAME"]] = arr_index
        
        if command["FUNCTION_NAME"] == "input":
            input_text = Visitor.get_value(command["##ARGUMENTS"][0])
            var_name = command["VAR_NAME"]

            # getting input
            input_ = input(str(input_text))

            Visitor.GLOBAL_MEMORY[var_name] = input_
        
        if command["FUNCTION_NAME"] == "int":
            var_name = command["VAR_NAME"]
            value = Visitor.get_value(command["##ARGUMENTS"][0])
            Visitor.GLOBAL_MEMORY[var_name] = int(value)
        
        if command["FUNCTION_NAME"] == "float":
            var_name = command["VAR_NAME"]
            value = Visitor.get_value(command["##ARGUMENTS"][0])
            Visitor.GLOBAL_MEMORY[var_name] = float(value)
        
        if command["FUNCTION_NAME"] == "str":
            var_name = command["VAR_NAME"]
            value = Visitor.get_value(command["##ARGUMENTS"][0])
            Visitor.GLOBAL_MEMORY[var_name] = str(value)
    @staticmethod
    def handle_reassign(command):
        debug_print("\nhandling reassign")

        var_name = command["VAR_NAME"]
        value = command["VAR_VALUE"]
        debug_print(command)
        value_ = Visitor.get_value(value)

        Visitor.GLOBAL_MEMORY[Visitor.get_value(var_name)] = value_

    @staticmethod
    def handle_chunk_calls(command):
        debug_print("\nhandling chunk call")
        
        chunk_name = command["CHUNK_NAME"]
        debug_print("calling chunk : " + chunk_name)

        Visitor.handle_function_calls(command, chunk_name + "::")


    @staticmethod
    def handle_chunk_creation(command):
        debug_print("\nhandling chunk creation")
        # adjusting scope
        Visitor.CURRENT_SCOPE = command["CHUNK_NAME"] + "::"
    
    @staticmethod
    def handle_function_creation(command):
        debug_print("\nhandling function creation")
        
        func_name = command["FUNCTION_NAME"]
        func_args = command["##ARGUMENTS"]

        Visitor.CURRENT_FUNCTION = Visitor.CURRENT_SCOPE + func_name
        Visitor.GLOBAL_MEMORY[Visitor.CURRENT_FUNCTION] = [func_args, []]

        debug_print("updated memory")
        debug_print(Visitor.GLOBAL_MEMORY)

    @staticmethod
    def handle_function_calls(command, chunk_scope=""):
        debug_print("\nhandling function calls")

        # extracting name
        func_name = command["FUNCTION_NAME"]
        func_name = chunk_scope + func_name

        for x in range(len(Visitor.GLOBAL_MEMORY[func_name][0])):
            # getting name of each argument
            arg = Visitor.GLOBAL_MEMORY[func_name][0][x]
            arg_ = Preprocessor.remove_front_whitespaces(arg)

            # getting the value for each argument
            given_arg = command["##ARGUMENTS"][x]
            given_arg_ = Preprocessor.remove_front_whitespaces(given_arg)

            # committing arg and corresponding value to global memory
            Visitor.GLOBAL_MEMORY[arg_] = Visitor.get_value(given_arg_)
        
        # calling function => simply parse all of the function lines
        Visitor.parse(Visitor.GLOBAL_MEMORY[func_name][1], func_name)



    @staticmethod
    def handle_end(command):
        debug_print("\nhandling end statement")

        if command["TARGET"] == "D":
            Visitor.CURRENT_FUNCTION = ""
        if command["TARGET"] == "CHUNK" and "::" in Visitor.CURRENT_SCOPE:
            Visitor.CURRENT_SCOPE = ""

    @staticmethod
    def handle_array_creation(command):
        debug_print("\nhandling array creation")
        arr_name = command["LIST_NAME"]
        arr_vars = command["##LIST_VALUES"]

        # extracting values from the arr
        arr_vars_ = []
        for v in arr_vars:
            arr_vars_.append(Visitor.get_value(v))

        # commiting to memory
        Visitor.GLOBAL_MEMORY[Visitor.CURRENT_SCOPE + arr_name] = arr_vars_

    @staticmethod
    def handle_assignments(command):
        debug_print("\nhandling assignment")
        if command["COMMAND"] == "C":
            value = Visitor.get_value(command["VAR_VALUE"])
            if value != None:
                Visitor.GLOBAL_MEMORY[Visitor.CURRENT_SCOPE + command["VAR_NAME"]] = value 
                debug_print("updated memory")
                debug_print(Visitor.GLOBAL_MEMORY)

        elif command["COMMAND"] == "CCALL":
            debug_print("return value assignment")

            # extracting function and variable name
            var_name = command["VAR_NAME"]
            func_name = command["FUNCTION_NAME"]

            # commiting to memory => might create temp_memory? (for safety) => do the same for args?
            Visitor.GLOBAL_MEMORY[var_name] = func_name

            # calling the fucntion => parser will handle return statements and loop through memory until it finds the correct function
            Visitor.handle_function_calls(command)

        elif command["COMMAND"] == "COP":
            debug_print("operation assignment")
            var_name = command["VAR_NAME"]
            var_name1 = command["VAR1_NAME"]
            var_name2 = command["VAR2_NAME"]

            value_1 = Visitor.get_value(var_name1)
            value_2 = Visitor.get_value(var_name2)

            value_3 = None

            operation = command["OPERATOR"]
            if operation == "+":
                value_3 = value_1 + value_2
            elif operation == "-":
                value_3 = value_1 - value_2
            elif operation == "*":
                value_3 = value_1 * value_2
            elif operation == "/":
                value_3 = value_1 / value_2
            elif operation == "**" or operation == "pow":
                value_3 = value_1 ** value_2
            elif operation == "sqrt" or operation == "//":
                value_3 = round(value_1 ** (1 / value_2), 5)
        
            # commiting to memory
            Visitor.GLOBAL_MEMORY[var_name] = value_3
        
        elif command["COMMAND"] == "CON":
            debug_print("condition assignemnt")

            var_name = command["VAR_NAME"]
            value_1 = Visitor.get_value(command["VAR1_NAME"])
            value_2 = Visitor.get_value(command["VAR2_NAME"])
            operation = command["OPERATOR"]
            value_3 = None

            if operation == "<":value_3 = value_1 < value_2
            elif operation == ">":value_3 = value_1 > value_2
            elif operation == "=":value_3 = value_1 == value_2
            elif operation == "!":value_3 = value_1 != value_2
            elif operation == ">=":value_3 = value_1 >= value_2
            elif operation == "<=":value_3 = value_1 <= value_2
            elif operation == "&":value_3 = value_1 and value_2
            elif operation == "|":value_3 = value_1 or value_2
            
            # commiting to memory
            Visitor.GLOBAL_MEMORY[var_name] = value_3
            

        elif command["COMMAND"] == "C>":
            debug_print("chunk variable assignment")
            chunk_name = command["CHUNK_NAME"]
            chunk_var_name = command["CHUNK_VAR"]
            var_name = command["VAR_NAME"]
            value = Visitor.get_value(chunk_name + "::" + chunk_var_name)
            if value != None:
                debug_print("updating memory")
                Visitor.GLOBAL_MEMORY[var_name] = value
                debug_print(Visitor.GLOBAL_MEMORY)
        
        elif command["COMMAND"] == "C>>":
            debug_print("chunk call assignment")

            # extracting function and variable name
            var_name = command["VAR_NAME"]
            func_name = command["FUNCTION_NAME"]
            chunk_name = command["CHUNK_NAME"] + "::"
            func_name = chunk_name + func_name

            # commiting to memory => might create temp_memory? (for safety) => do the same for args?
            Visitor.GLOBAL_MEMORY[var_name] = func_name

            # calling the fucntion => parser will handle return statements and loop through memory until it finds the correct function
            Visitor.handle_function_calls(command, chunk_name)

            

    
    # -------------------------------------------------------------------------------------------
    # -------------------------------------------------------------------------------------------
    # -------------------------------------------------------------------------------------------

    @staticmethod
    def get_value(n, acces_from_memory=True):
        n_ = Preprocessor.remove_front_whitespaces(n)
        
        # checking if its a string:
        if n_[0] in ("'", '"') and n_[len(n_)-1] in ('"',"'"):
            return n_[1:len(n_)-1]

        # checking if bool
        if n_ == "false" or n_ == "true":
            return True if n_ == "true" else False
        
        # checking if in global memory
        if n_ in Visitor.GLOBAL_MEMORY.keys() and acces_from_memory:
            return Visitor.GLOBAL_MEMORY[n_]

        # checking if it's a num
        try:
            num = float(n_)
            return num
        except:
            debug_print("the given var is undefined")
            return None


