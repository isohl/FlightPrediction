import os
from time import sleep

readFilepath = os.path.expanduser(os.path.join('~','tnclogs','tnc2.log'))
writeFilepath = os.path.expanduser(os.path.join('~','tnclogs','tnc.log'))
waitTime = float(raw_input('Write interval length (sec): '))

with open(readFilepath, 'r') as log_file1:
	for line in log_file1:
		if not line.startswith('#') and not line == "\n":
			with open(writeFilepath, 'a') as log_file2:
				log_file2.write(line)
			sleep(waitTime)
				
			
		