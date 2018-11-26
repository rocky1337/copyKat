'''
Detect plagiarism by sequences of words from different reports. 
Adapted from http://nifty.stanford.edu/2008/franke-catch-plagiarists/

Input file: Text of reports, one report per line.
Compare n-length sequences of words from each line.
'''

import sys

'''
# Use getKey() with sorting a list
# https://www.pythoncentral.io/how-to-sort-a-list-tuple-or-object-with-sorted-in-python/
def getKey(item):
	return item[0]
'''
	
SEQUENCE_LENGTH = 10

# Open the file and read it into the list "content"
if (len(sys.argv) > 1): # A command-line argument exists; assume it is an input filename
	filename = sys.argv[1]
else: # Prompt for input filename
	filename = input("\n\n\tPlease type an input data file name: ")
try:
		fInput = open(filename, "r")  # with open(filename) as fInput:
		content = fInput.readlines() # one report (possibly plagiarized) per line
		fInput.close()  #close(fInput)
except FileNotFoundError:
	sys.exit('Could not find file ' + filename)


# The list content[] has N elements, each of which is one report to be considered for plagiarism.
# Each element of content[] is a list of strings which are separate words of the report.

allSequences = []

# Read each line of the input file. Each line is one report to be considered for plagiarism.
for inputFileLineCounter in range(0, len(content)): 

	# The current report to be considered for plagiarism.
	line = content[inputFileLineCounter].split() # line is a list of words in report
	sequence = [] # sequence[] is a list of SEQUENCE_LENGTH words of the report

	# Create the initial SEQUENCE_LENGTH sequence of words in this report.
	j = 0  # word index in the current report
	while j < SEQUENCE_LENGTH:  # for each word of the sequence.
		#print(line[j])
		sequence.append(line[j]) # append current word to end of sequence
		j = j + 1 
	# print(sequence)
	sequence.append(inputFileLineCounter)  # identifier for the sequence
	allSequences.append(sequence)
		
	# Create all subsequent SEQUENCE_LENGTH sequences of words in this report.
	while j < len(line):  # for each word of the report...
	
		 # Remove the first word from the sequence, and append a new word to 
		 # the end of sequence. That is a new SEQUENCE_LENGTH sequence.
		sequence = sequence[1:]  # remove existing first element
		sequence = sequence[:-1]  # remove existing last element (identifier for the sequence)
		sequence.append(line[j])  # append a new last element
		sequence.append(inputFileLineCounter)  # identifier for the sequence
		j = j + 1 
		# print(sequence)
		allSequences.append(sequence)

# break  # DEBUG hardcoded 	
#print(allSequences)	
#print(allSequences.sort())

# sortedAllSequences = sorted(allSequences, key=getKey)

'''
for i in range(0, len(sortedAllSequences)):
	print(sortedAllSequences[i])
'''

#print(allSequences)


# http://www.lleess.com/2013/08/python-sort-list-by-multiple-attributes.html#.W-uDFpNKhaQ
# This sort() technique doesn't _return_ a value, just simply _performs_ the sort on existing list.
allSequences.sort(
	key = lambda l: (l[0], l[1], l[2], l[3])
)
sortedAllSequences = allSequences # Copy of sorted list

# print(sortedAllSequences)

print("There are ", len(sortedAllSequences), " sequences of ", SEQUENCE_LENGTH, " words to be compared.")


# The sequences are sorted. If any two sequences are the same, those sequences 
# are adjacent in the sorted list. Compare sequence i to sequence (i+1).
def arrayFill(duplicates, doc1, doc2):
	exists = False
	for i in duplicates:
		if i[0] == doc1 and i[1] == doc2:
			i[2] = i[2] + 1
			exists = True
	if not exists:
		if duplicates[0][1] == 0:
			duplicates[0][0] = doc1
			duplicates[0][1] = doc2
			duplicates[0][2] = 1
		else:
			duplicates.append([doc1, doc2, 1])

TwoDArray = [[0,0,0]]

for i in range(0, len(sortedAllSequences)-1):  # index of the "leading" sequence that might be duplicated indicating plagiarism	
	duplicateCount = 0
	for k in range(0, SEQUENCE_LENGTH):
		if sortedAllSequences[i][k] == sortedAllSequences[i+1][k]:
			duplicateCount = duplicateCount + 1
		else:
			break  # Stop checking -- two lists are not duplicates
	if (duplicateCount == SEQUENCE_LENGTH  # Every element of two sequences is the same...
		and sortedAllSequences[i][SEQUENCE_LENGTH] != sortedAllSequences[i+1][SEQUENCE_LENGTH]): # ... and sequences are in different reports
		arrayFill(TwoDArray, sortedAllSequences[i][SEQUENCE_LENGTH] + 1, sortedAllSequences[i+1][SEQUENCE_LENGTH] + 1)
		#print("DUPLICATE:  ", sortedAllSequences[i], " is duplicated within ", sortedAllSequences[i][SEQUENCE_LENGTH] + 1, " and ", sortedAllSequences[i+1][SEQUENCE_LENGTH] + 1)
print(TwoDArray)

	
	