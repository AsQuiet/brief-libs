def create_table(cols, rows, value=0, value_function=None):
    table = []

    for x in range(rows):
        table.append([])

        for y in range(cols):

            if value_function != None:
                table[x].append(value_function(y, x))
            else:
                table[x].append(value)
    
    return table

def print_table(table, col_width=3, str_function=str, col_separator=" | ", print_function=print, show_index=True):

    for x in range(len(table)):
        text = (str(x) + col_separator) if show_index else ""

        for y in range(len(table[x])):
            text += str_function(table[x][y])
            text += col_separator if (y != len(table[x])-1) else ""
        
        print_function(text)

def normalize_table(table, cols, rows, fill_value=0):
    
    n_table = []

    for y in range(len(table)):
        if y >= rows:
            break
        row = table[y]
        n_row = []
        
        for x in range(cols):
            if x < len(row):
                n_row.append(row[x])
            else:
                n_row.append(fill_value)

        n_table.append(n_row)

    for y in range(rows - len(table)):

        n_row = []

        for x in range(cols):
            n_row.append(fill_value)
        
        n_table.append(n_row)

    return n_table


    

def get_row(table, index):
    return table[index]

def get_col(table, index):
    col = []

    for x in range(len(table)):
        col.append(table[x][index])

    return col