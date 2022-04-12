from tkinter import *
import tkinter.font as font
from tkinter import simpledialog
import time, threading, json
import ctypes
 
ctypes.windll.shcore.SetProcessDpiAwareness(1)

# Updates the time displayer with the correct time.
def time_loop_func():
    global b
    while True:
        b['text'] = time.strftime("%I:%M", time.localtime())
        time.sleep(60 - int(time.strftime("%S", time.localtime())))

# Opens the right click menu
def openMenu(event):
    try: 
        main_menu.tk_popup(event.x_root, event.y_root) 
    finally: 
        main_menu.grab_release() 

# Updates what side the displayer should be on
def setSide(horizontal, vertical):
    global x, y
    data = json.loads(open("storage.json").read())
    f = open("storage.json", "a")
    f.truncate(0)

    x = -1 if horizontal == 0 else root.winfo_screenwidth() - w
    data["x"] = horizontal

    y = -1 if vertical == 0 else root.winfo_screenheight() - h
    data["y"] = vertical
        
    root.geometry("{w}x{h}+{x}+{y}".format(w = w, h = h, x = x, y = y))

    f.writelines(json.dumps(data))
    f.close() 

# Creates a custom size
def createCustom():
    inputted_w = 0
    inputted_h = 0

    while True:
        try:
            inputted_w = simpledialog.askinteger("New width", "WIDTH:")
        except:
            continue
        break

    while True:
        try:
            inputted_h = simpledialog.askinteger("New height", "HEIGHT:")
        except:
            continue
        break

    size_menu.add_command(label = f"{inputted_w}x{inputted_h}", command = lambda: setSize(inputted_w, inputted_h))
    with open("storage.json",'r+') as file:
        file_data = json.load(file)
        file_data["customSizes"].append({"w": inputted_w, "h": inputted_h})
        file.seek(0)
        json.dump(file_data, file, indent = 4)

    setSize(inputted_w, inputted_h)

# Removes a created custom size
def removeCustom():
    inputted_w = 0
    inputted_h = 0

    while True:
        try:
            inputted_w = simpledialog.askinteger("New width", "WIDTH:")
        except:
            continue
        break

    while True:
        try:
            inputted_h = simpledialog.askinteger("New height", "HEIGHT:")
        except:
            continue
        break
    
    found = False

    for i in range(4, size_menu.index('end')+1):
        if size_menu.entrycget(i,'label') == f"{inputted_w}x{inputted_h}": 
            found = True
            file = open("storage.json",'r+')
            file_data = json.load(file)
            for i in file_data["customSizes"]:
                if i["w"] == int(inputted_w) and i["h"] == int(inputted_h):
                    file_data["customSizes"].remove(i)
            file.seek(0)
            json.dump(file_data, file, indent = 4)    
            size_menu.delete(f"{inputted_w}x{inputted_h}")

    if found == False: simpledialog.dialog("Not an existing size.")

# Sets the size
def setSize(width, height):
    global w, h, x, y, b
    data = json.loads(open("storage.json").read())
    f = open("storage.json", "a")
    f.truncate(0)

    print(x, y)
    if x != -1: x = root.winfo_screenwidth() - width
    if y != -1: y = root.winfo_screenheight() - height
    print(x, y)

    wr = width / 120
    hr = height / 80
    root.geometry("{w}x{h}+{x}+{y}".format(w = width, h = height, x = x, y = y))
    b['font'] = font.Font(family = 'Segoe UI Light', size = int(15 * wr if wr < hr else 15 * hr))
    b["width"] = data["w"] = w = width
    b["height"] = data["h"] = h = height
    
    f.writelines(json.dumps(data))
    f.close()

root = Tk()

w, h = 0, 0
x, y = 0, 0

customs = []

#Reads from the side file to see where the time displayer should be
try:
    f = open("storage.json", "r+")
    data = json.loads(f.read())
    f.close()

    w = data["w"]
    h = data["h"]

    if data["x"] == 0: x = -1
    elif data["x"] == 1: x = root.winfo_screenwidth() - w
    if data["y"] == 0: y = -1
    elif data["y"] == 1: y = root.winfo_screenheight() - h

    for i in data["customSizes"]:
        customs.append(i)
except FileNotFoundError:
    x = -1
    y = root.winfo_screenheight() - h
    w = 120
    h = 70

    f = open("storage.json", "a")
    f.write("{\"x\": 0, \"y\": 0, \"w\": 120, \"h\": 70, \"customSizes\": []}")
    f.close()

#Creates the window
root.title("Time")
root.overrideredirect(True)
root.geometry("{w}x{h}+{x}+{y}".format(w = w, h = h, x = x, y = y))
root.configure(bg = 'black')

#Text for time
b = Button(root, text = "N/A", command = root.destroy, width = w, height = h, bd = 0, bg = "black", fg = "white")
wr = w / 120
hr = h / 80
b['font'] = font.Font(family = 'Segoe UI Light', size = int(15 * wr if wr < hr else 15 * hr))
b.pack()
b.bind("<Button-3>", openMenu)

#Right click menu
sides_menu = Menu(root, tearoff=0)
sides_menu.add_command(label = "Top Left", command = lambda: setSide(0, 0))
sides_menu.add_command(label = "Top Right", command = lambda: setSide(1, 0))
sides_menu.add_separator()
sides_menu.add_command(label = "Bottom Left", command = lambda: setSide(0, 1))
sides_menu.add_command(label = "Bottom Right", command = lambda: setSide(1, 1))

size_menu = Menu(root, tearoff=0)
size_menu.add_command(label = "Large (240x160)", command = lambda: setSize(240, 160))
size_menu.add_command(label = "Medium (120x80)", command = lambda: setSize(120, 80))
size_menu.add_command(label = "Small (60x35)", command = lambda: setSize(60, 35))
size_menu.add_separator()
size_menu.add_command(label = "Add Custom...", command = lambda: createCustom())
size_menu.add_command(label = "Remove Custom...", command = lambda: removeCustom())
for custom in customs:
    size_menu.add_command(label = f"{custom['w']}x{custom['h']}", command = lambda lw=int(custom['w']), lh=int(custom['h']): setSize(lw, lh))

main_menu = Menu(root, tearoff=0)
main_menu.add_cascade(label = "Set Side...", menu = sides_menu)
main_menu.add_cascade(label = "Set Size...", menu = size_menu)
main_menu.add_command(label = "Exit", command = root.quit)

#Sets attributes of the window.
root.attributes('-topmost', True)
root.attributes('-alpha', 0.75)

#Starts the time checking thread/loop
time_loop = threading.Thread(target = time_loop_func)
time_loop.start()

#Starts the main loop
root.mainloop()

#Waits for the time checking loop to stop.
time_loop.join()