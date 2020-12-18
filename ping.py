import platform
import subprocess
import os

def ping(host_ip, timeout):

    def f():
        FNULL = open(os.devnull, 'w') # for hiding ping command output

        count_param = '-n' if platform.system().lower()=='windows' else '-c' # ping count parameter
        timeout_param = '-w' if platform.system().lower()=='windows' else '-W' # ping timeout parameter

        command = ['ping', count_param, '1', timeout_param, str(timeout), host_ip]

        return subprocess.call(command, stdout=FNULL,stderr=subprocess.STDOUT) == 0

    if f():
        return (True, "ICMP packet recieved from ({})".format(host_ip))
    #else
    return (False, "ICMP packet failed.")
