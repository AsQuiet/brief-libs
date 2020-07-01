"""
Contains functions for writing and reading data to files.
"""

def write_dictionary(dic, path, separator="=", appendmode="w"):
    """Writes the given dictionary to the given path. The default separator between each key and value is '='."""
    # getting the keys
    ks = dic.keys()

    # opening the file and writing
    f = open(path, appendmode)
    i = 0
    for k in ks:
        f.write(str(k) + separator + str(dic[k]) + ("" if i == len(ks) - 1 else "\n"))
        i+=1
    f.close()

def read_dictionary(path, separator="="):
    """Reads the file at the path and construct a dictionary out of it."""
    f = open(path, "r")
    dic = {}
    for line in f:
        
        key = ""
        value = ""
        found = False
        for char in line:
            if found: value += char
            if char == separator:found = True
            if not found:key += char
        
        dic[key] = value.rstrip("\n")
            
    f.close()
    return dic

def reverse_dictionary(dict):
    ks = list(dict.keys())
    vs = list(dict.values())

    new_dict = {}
    for x in range(len(vs)):
        new_dict[vs[x]] = ks[x]
    return new_dict