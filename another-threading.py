import time
import threading

def square():
    print("Square function called")
    # time.sleep(5)

def cube() :
    print ("Cube function called")
    # time.sleep(5)


time. sleep (5)
start = time.time()
t1 = threading. Thread(target=square)
t2 = threading. Thread(target=cube)
t1.start()
t2.start()
t1.join() # Wait till t1 is complete
t2. join() # Wait till t2 is complete
end = time. time()
print (end-start)