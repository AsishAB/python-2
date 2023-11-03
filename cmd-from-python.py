import os
import time

commit_message = "Code committed from Python Script"
os.system("git add .")
time.sleep(4)
os.system(f'git commit -m "${commit_message}"')