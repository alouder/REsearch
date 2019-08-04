from itertools import product
from os.path import expanduser
import threading, platform, time, re, test, scrape, immutable

# Establish instance of Immutable class in immutable.py for accessing inititial data sets
initial_data = immutable.Immutable()

# Validate the amino acid sequence entered by the user.
# Return validated string
def getAminoAcid():
	input_amino_acid_sequence = input("Enter amino acid sequence (0 to quit): ")
	input_amino_acid_sequence = input_amino_acid_sequence.upper()
	valid = True
	while valid == True and input_amino_acid_sequence != '0':
		for i in input_amino_acid_sequence:
			if i in initial_data.amino_acid_codons:
				pass
			else:
				valid = False
		break
	while valid == False  and input_amino_acid_sequence != '0':
		print("---- ERROR: Invalid amino acid sequence ----\nEnter a string of characters with no spaces that correspond to conventional amino acid symbols.\n")
		input_amino_acid_sequence = input("Enter amino acid sequence (0 to quit): ")
		input_amino_acid_sequence = input_amino_acid_sequence.upper()
		inner = True
		while inner == True:
			for i in input_amino_acid_sequence:
				if i in initial_data.amino_acid_codons:
					pass
				else:
					inner = False
					valid = False
			if inner == True:
				valid = True
			break
	return input_amino_acid_sequence

# Find the number of possible codon combinations for a particular amino acid sequence
# Return integer
def numCombinations(amino_acid_sequence):
	comb = 1
	for i in amino_acid_sequence:
		comb *= len(initial_data.amino_acid_codons[i])
	return comb

# Build all possible combinations for a sequence using itertools.
# Returns a list of tuples which contain each combination 
def buildPossibleSequences(sequence, dic):
    comb = []
    for i in sequence:
    	comb.append(dic[i])

    return list(product(*comb))

# Join the tuples created by build_possible_sequences and return a list of possible sequences as strings
def joinTuplesList(join_string, lst):
	comb_list = []
	for i in lst:
		s = join_string.join(i)
		comb_list.append(s)
	return comb_list

# Distinguish palindromic from non-palindromic enzymes (as indicated by the NEB notation)
# Return boolean
def isPalindromic(seq):
	return "(" in seq

# Filter numbers and parentheses out of non-palindromic enzymes. 
# Return sanitized string.
def splitNonPalindromic(seq):
	if re.search("^\(.*\)", seq) is not None:
		temp_list = re.split("\)", seq, 1)
		if re.search("\(.*\)", temp_list[1]) is not None:
			return re.split("\(", temp_list[1])[0]
		else:
			return temp_list[1]
	return re.split("\(", seq)[0]

# Return modified dictionary to hold the RE recognition sequence stirngs (and corresponding REs) with out cleavage site indicator (for processing).
# Palindromic and non-palindromic enzymes are distinguished.
def sanitizeSequences(initial_dic):
	mod_enz_seqs = {}
	for i in initial_dic:
		if not isPalindromic(initial_dic[i]):
			mod = re.sub("/", "", initial_dic[i])
			mod_enz_seqs[i] = mod
		else:
			mod = splitNonPalindromic(initial_dic[i])
			mod_enz_seqs[i] = mod
	return mod_enz_seqs

# Eliminate certain enzymes based on whether or not a given base is present in the amino acid sequence	
def eliminateEnzymeByBase(codon_list, enz_dict, base):
	base_present = False
	i = 0
	while i < len(codon_list) and base_present == False:
		if base in codon_list[i]:
			base_present = True
		else:
			i += 1
	if base_present == False:
		for i in enz_dict:
			for j in enz_dict[i]:
				if base in j:
					enz_dict[i].remove(j)

# Run eliminateEnzymeByBase for all bases
def checkAllBases(codon_list, enz_dict):
	eliminateEnzymeByBase(codon_list, enz_dict, "G")
	eliminateEnzymeByBase(codon_list, enz_dict, "C")
	eliminateEnzymeByBase(codon_list, enz_dict, "A")
	eliminateEnzymeByBase(codon_list, enz_dict, "T")

# Eliminate certain enzymes by the length of the amino acid sequence inputted (to be implemented before elimination based on bases)
def eliminateEnzymeByLength(enz_dict, amino_acid_sequence):
	max_len = len(amino_acid_sequence) * 3
	toDel = []
	for i in enz_dict:
		if len(enz_dict[i]) > max_len:
			toDel.append(i)
	for i in toDel:
		del enz_dict[i]

# Delete keys of a dictionary that have values which are empty lists
def delEmptyKeys(dic):
	toDel = []
	for i in dic:
		if len(dic[i]) == 0:
			toDel.append(i)
	for i in toDel:
		del dic[i]

# Check all enzyme recognition sequence combinations against all codon combinations
# Final_dict should be an empty dictionary with elements being added by this function
# To be called in threadMatches
def getMatches(codon_list, enz_dic, final_dict):
	for i in codon_list:
		for k in enz_dic:
			for v in enz_dic[k]:
				if v in i:
					final_dict[k] = i

# Multithread the matching process by spliting the possible codon list into four chunks
# numThreads should be 4
def threadMatches(codon_list, enz_dic, final_dict, numThreads=4):
	threads = []
	split = len(codon_list) // numThreads
	for i in range(numThreads):
		if i < numThreads - 1:
			splitList = codon_list[split*i:split*(i+1)]
		else:
			splitList = codon_list[split*i:]
		t = threading.Thread(target=getMatches, args=(codon_list, enz_dic, final_dict,))
		t.start()
		threads.append(t)
	for t in threads:
		t.join()

# Write dictionary to a text file in format
def writeDictToFile(fname, dic, sequence):
	with open(fname, "w") as file:
		file.write("Amino acid sequence entered: " + sequence + "\n\n")
		file.write("%-15s%-21s%-15s%-15s\n____________________________________________________________\n\n" %("Enzyme:", "Sequence:", "Size:", "Price"))
		for x, y in dic.items():
			file.write("%-15s%-21s%-15s%-15s\n____________________________________________________________\n\n" %(x + ":", y[0], y[1], y[2]))

# Create N threads for requesting pages as defined in scrape.initNebPriceDict,
# where N is the number of items in the final dictionary.
def threadRequests(dic):
	threads = []
	for name in dic:
		t = threading.Thread(target=scrape.initNebPriceDict, args=(name,))
		t.start()
		threads.append(t)
	for t in threads:
		t.join()

#
#
###############
# Driver code #
###############
#
#

def main():

	input_amino_acid_sequence = getAminoAcid()

	while input_amino_acid_sequence != "0":
		# Mark start time for processing (finding matches)
		start_time = time.time()
		print("\nSearching for possible restriction enzymes...")

		codon_comb_list = joinTuplesList("", buildPossibleSequences(input_amino_acid_sequence, initial_data.amino_acid_codons))

		mod_enz_seqs = initial_data.mod_enz_seqs

		# Narrow down possible enzymes based on length of amino acid sequence
		eliminateEnzymeByLength(mod_enz_seqs, input_amino_acid_sequence)

		absolute_mod_enz_seqs = {}
		for i in mod_enz_seqs:
			absolute_mod_enz_seqs[i] = joinTuplesList("", buildPossibleSequences(mod_enz_seqs[i], initial_data.ambiguity))

		# Narrow down possible enzymes based on base
		checkAllBases(codon_comb_list, absolute_mod_enz_seqs)

		# Delete keys storing empty lists
		delEmptyKeys(absolute_mod_enz_seqs)

		# Add matches to a final dictionary
		final_dict = {}
		threadMatches(codon_comb_list, absolute_mod_enz_seqs, final_dict)
		# Total processing time for finding enzymes
		elapsed_time = time.time() - start_time
		print("---- Found %2d applicable enzyme(s) in %.3f seconds ----\n" %(len(final_dict), elapsed_time))
		print("Searching for prices of enzymes...")
		# Mark start time for finding prices
		start_time = time.time()
		threadRequests(final_dict)
		# Get prices of only the enzymes in final dictionary
		neb_price = scrape.neb_price
		# Total processing time for finding prices
		elapsed_time = time.time() - start_time
		print("---- Found prices for %2d enzymes in %.3f seconds ----\n" %(len(final_dict), elapsed_time))

		# Combine enzyme/sequence dictionary and enzyme/price dictionary
		for i in final_dict:
			final_dict[i] = (final_dict[i], neb_price[i][0], neb_price[i][1])
		del neb_price

		# Display to user
		print("%-15s%-21s%-15s%-15s\n____________________________________________________________\n" %("Enzyme:", "Sequence:", "Size:", "Price:"))
		for x, y in final_dict.items():
			print("%-15s%-21s%-15s%-15s\n____________________________________________________________\n" %(x + ":", y[0], y[1], y[2]))

		# Check to see if final_dict should be written to a file. If so, write to file.
		ask_to_write = input("Would you like to write the results to a file (Y/n)? ")
		ask_to_write = ask_to_write.upper()
		if ask_to_write == "Y":
			fname = input("Enter a name for the file: ")
			while "." in fname and fname[-4:] != ".txt":
				print("--- ERROR: Output can only be written to a text (.txt) file ---")
				fname = input("Enter a name for the file: ")
			if "." not in fname:
				fname += ".txt"
			# Find user's home directory
			home = expanduser("~")
			# Default to Documents directory -- Case for Windows and Linux\Mac users
			if platform.system() == "Windows":
				fname = home + "\\Documents\\" + fname
			else:
				fname = home + "/Documents/" + fname
			writeDictToFile(fname, final_dict, input_amino_acid_sequence)
			print("Results written to: " + fname)

		# Ask for another amino acid sequence
		print()
		input_amino_acid_sequence = getAminoAcid()
main()