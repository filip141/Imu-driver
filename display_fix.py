import os
import subprocess


def screen_fix():
    p_echo = subprocess.Popen("echo $DISPLAY", stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE, shell=True)
    p_xauth = subprocess.Popen('su - pi -c "xauth list"', stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE, shell=True)
    echo_output, _ = p_echo.communicate()
    echo_output = "raspberrypi/unix:" + echo_output.split(":")[1][:-3]
    xauth_output, _ = p_xauth.communicate()
    for line in xauth_output.split("\n"):
        if echo_output in line:
            screen_data = line
    os.system("sudo xauth add " + screen_data)