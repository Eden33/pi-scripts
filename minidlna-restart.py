# coding=utf-8
 
import RPi.GPIO as GPIO
import datetime, subprocess, signal, os, logging, time
from subprocess import Popen, PIPE
 

logging.basicConfig(filename='/var/log/minidlna-restart.log',level=logging.DEBUG)

def pin6_callback(channel):
    logging.debug('Restart minidlnad at ' + str(datetime.datetime.now())) 
 
    minidlnaParentPid = get_minidlnad_parent_pid(True) 
 
    if minidlnaParentPid != 0:
        logging.debug('Kill minidlnad main process: ' + str(minidlnaParentPid))
        os.kill(minidlnaParentPid, signal.SIGKILL)

    Popen(['/opt/sbin/minidlnad'], stdout=PIPE, stderr=PIPE)
    time.sleep(5)
    minidlnaParentPid = get_minidlnad_parent_pid(False)
    logging.debug('minidlnad restarted. New PID: ' + str(minidlnaParentPid))


def get_minidlnad_parent_pid(performLogging):
    p = subprocess.Popen(['ps', '-ef'], stdout=subprocess.PIPE)
    out, err = p.communicate()

    minidlnaParentPid = 0

    for line in out.splitlines():
        if 'minidlnad' in line:
            if performLogging:
                logging.debug('Found mindlna process: ' + line)
            
            processInfo = line.split(None)
            pid = int(processInfo[1])
            parentPid = int(processInfo[2])

            if performLogging:
                logging.debug('pid: ' + str(pid))
                logging.debug('parentPid: ' + str(parentPid))

            if parentPid == 1:
                minidlnaParentPid = pid
                
                if performLogging:
                    logging.debug('minidlnaParentPid: ' + str(minidlnaParentPid))

    return minidlnaParentPid

try:
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(6, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(6, GPIO.FALLING, callback=pin6_callback, bouncetime=1000)
    while True:
        time.sleep(1)
 
    #message = raw_input('\nPress any key to exit.\n')
 
finally:
    GPIO.cleanup()
    logging.debug("Goodbye!")
