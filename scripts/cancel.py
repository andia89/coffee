filename = "/home/pi/coffee/scripts/cancel"

def reset():
    with open(filename, "w") as f:
        f.write("0")

def cancel(cont):
    with open(filename, "r") as f:
        val = int(f.read())
    if val:
        cont.value = 0
