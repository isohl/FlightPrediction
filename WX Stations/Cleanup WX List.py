import string
running = True
i = 0
readFile = open ('Station Data Raw.txt', 'r')
writeFile = open ('Parsed Station Data.py', 'w')
writeFile.write('{')
while running :
	currentLine = readFile.readline()
	currentLine = currentLine.strip()
	if i >= 5 :
		i = 0
	if 'endProgram' in currentLine :
		writeFile.write('}')
		print '---Closing Files---'
		readFile.close()
		writeFile.close()
		running = False
	elif i == 0 :
		writeFile.write('"' + currentLine + '":{"station":"')
	elif i == 1 :
		writeFile.write(currentLine + '","position":(float(')
	elif i == 2 :
		writeFile.write(currentLine + '),float(')
	elif i == 3 :
		writeFile.write(currentLine + '),int(')
	elif i == 4 :
		alitiude = int(currentLine)
		alitiude = alitiude *3.28084
		alitiude = int(alitiude)
		currentLine = str(alitiude)
		writeFile.write(currentLine + ')),},')
	i = i+1
