import sys
import time
import box

# start of main
print("__main__ calling")
res = -1
while res != 0:
    start_time = time.time()
    try:
        res = box.start_gui(sys.argv)
    except:
        res = -1
    stop_time = time.time()
    if (res != 0) and (stop_time < (start_time + 3)):
        # serious bug, we just can just stop the application
        res = 0
        print("Fast error. Try calling box.py directly for more information")
