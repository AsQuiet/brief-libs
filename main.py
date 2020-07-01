from briefpy.util import Console
import time

Console.set_output(True)
Console.print("Name is %v and last is %v and birth is %v", "quinten", "lenaerts", "04/06/13")
Console.set_output(True)

for x in range(3):
    Console.print_line('%v%', x)
    time.sleep(1)

Console.new_line()
