import subprocess
import os
import re

def run_cmd(cmd):
    proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    while True:
        line = proc.stdout.readline()
        if line:
            yield line


def main():
    passwd = input('Enter your password:')
    pwd = os.getcwd()
    cmd = "echo " + passwd + " | sudo -S " + pwd + "/sniffer"
    print('Running command:', cmd + "...\n")

    for line in run_cmd(cmd=cmd):
        line = line.decode('utf-8')
        # get source IP of packet sender
        if "ip_src" in line:
            src = re.search(r'[a-z]+\s*=\s*(.+)', line)
            # remove local/inside network IP
            if not re.match(r'172', src.group(1)) and not re.match(r'192', src.group(1)):
                print("src:", src.group(1))
            else:
                print('src: private IP(192/172)')

        # get upper protocol
        if "protocol" in line:
            protocol = re.match(r'protocol:\s(.+)', line)
            print(protocol.group(1))
        # check Flags such as SYN, ACK, etc...
        if "FLAGS" in line:
            flags = re.match(r'FLAGS:\s(.+)', line)
            print(flags.group(1) + "\n")



if __name__ == "__main__":
    main()
