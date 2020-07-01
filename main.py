from briefpy.util import Console, time

for x in range(101):
    Console.print_line("progress : %v%v%", Console.CYAN if x != 100 else Console.GREEN, x)
    time.sleep(0.03)

Console.new_line()
