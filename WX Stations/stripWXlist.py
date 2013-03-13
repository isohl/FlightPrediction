running = True
readFile = open ('WX Station List.html', 'r')
writeFile = open ('Station Data Raw.txt', 'w')
while running :
	currentLine = readFile.readline()
	if '#f0f0f0' in currentLine :
		printLine = currentLine.strip()
		printLine = printLine.strip('<>')
		printLine = printLine.strip('td bgcolor="#f0f0f0"align="right"/td')
		printLine = printLine.strip('<>')
		printLine = printLine.strip()
		print printLine
		writeFile.write(printLine + '\n')
	if 'endProgram' in currentLine :
		writeFile.write('endProgram')
		readFile.close()
		writeFile.close()
		running = False

