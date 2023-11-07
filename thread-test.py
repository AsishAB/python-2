import threading

def display():
    for i in range(5):
        print("GOOD MORNING")


t1 = threading.Thread(target=display)
t1.start()

for i in range(5):
    print("GOOD EVENING")



