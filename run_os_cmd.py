#!/usr/bin/env python3
import subprocess
import re

def run_command(cmd_arr):
  try:
    child = subprocess.Popen(cmd_arr, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = child.communicate()
  except Exception as e:
    return "An exception happend when trying to run command: " + str(cmd_arr) + " "  + str(e) + "\n"
  return str(stdout)

t = float(re.findall("\d+\.\d+", run_command(["/opt/vc/bin/vcgencmd","measure_temp"]))[0])
print(t)
#run_command(["/usr/bin/raspistill",'-w', '640', '-h', '480', '-q', '75', "-o", full_image_path])

if __name__=="__main__":
   print(run_command(["/usr/bin/vcgencmd", "measure_temp"]))
