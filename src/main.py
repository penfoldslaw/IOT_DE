import threading
import subprocess

def run_script(script_name):
    """""
    This is being used because without it you would have to run the pub.py in one terminal
    then would have to run the bridge.py or sub.py which ever subscriber/consumer you are 
    using in another terminal. This script allows you to run these two files at the same time
    in one terminal.
    """""
    subprocess.run(["python", script_name])

if __name__ == "__main__":
    script1_thread = threading.Thread(target=run_script, args=("pub.py",))
    script2_thread = threading.Thread(target=run_script, args=("bridge.py",))

    script1_thread.start()
    script2_thread.start()

    script1_thread.join()
    script2_thread.join()