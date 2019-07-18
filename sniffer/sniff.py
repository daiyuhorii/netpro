import subprocess
import os
import re


def run_cmd(cmd):
    proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    while True:
        line = proc.stdout.readline()
        decoded = line.decode('utf-8')
        if line:
            if decoded == "successfully completed.\n":
                break
            yield decoded



def capture_from_packet(line):
    # get source IP of packet sender
    info = ""
    if "ip_src" in line:
        src = re.search(r'[a-z]+\s*=\s*(.+)', line)
        # remove local/inside network IP
        if not re.match(r'172', src.group(1)) and not re.match(r'192', src.group(1)):
            info = "src: " + src.group(1)
        else:
            info = 'src: ' + src.group(1)

    # get dst IP of packet receiver
    if "ip_dst" in line:
        dst = re.search(r'[a-z]+\s*=\s*(.+)', line)
        # remove local/inside network IP
        if not re.match(r'172', dst.group(1)) and not re.match(r'192', dst.group(1)):
            info = "dst: " + dst.group(1)
        else:
            info = 'dst: ' + dst.group(1)

    # get TCP
    if "protocol" in line:
        protocol = re.match(r'protocol:\s(.+)', line)
        info += protocol.group(1)
    # check Flags such as SYN, ACK, etc...
    if "FLAGS" in line:
        flags = re.match(r'FLAGS:\s(.+)', line)
        return info + flags.group(1)
    else:
        return info


def sniff():
    passwd = "horiidaiyu0131"
    pwd = os.getcwd()
    cmd = "echo " + passwd + " | sudo -S " + pwd + "/sniff"
    print('Running command:', cmd + "...\n")
    run_cmd_gen = run_cmd(cmd=cmd)

    data = list()
    result = dict()

    for line in run_cmd_gen:
        input_line = capture_from_packet(line)
        if not input_line == None and not input_line == "":
            data.append(input_line)
    for i in range(len(data)):
        #print(data[i], data[i+1], data[i+2])
        if "src:" in data[i]:
            src = data[i][5:-1]
            dst = data[i+1][5:-1]


            if data[i+2] == "UDP":
                comm = data[i+2]+" "
            else:
                comm = data[i+2] + " " + data[i+3]
            result[src] = [dst, comm]
    return result

if __name__ == '__main__':
    sniff()