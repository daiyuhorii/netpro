import subprocess
import os
import socket
def main():
    pwd = os.getcwd()
    cmd = "sudo ./sniff"
    c = subprocess.run("sudo " + pwd + "/sniff",  shell=True)

if __name__ == "__main__":
    main()