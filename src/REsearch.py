from itertools import product
import time, re, test, scrape, immutable

# Establish varibles for immutable data sets
amino_acid_codons = immutable.amino_acid_codons
ambiguity = immutable.ambiguity

# Find the number of possible codon combinations for a particular amino acid sequence
# Return integer
def numCombinations(amino_acid_sequence):
	comb = 1
	for i in amino_acid_sequence:
		comb *= len(amino_acid_codons[i])
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
# Return dictionary with enzyme name as key and codon combination as value
def getMatches(codon_list, enz_dic):
	final_dict = {}
	for i in codon_list:
		for k in enz_dic:
			for v in enz_dic[k]:
				if v in i:
					final_dict[k] = i
	return final_dict

# Write dictionary to a text file in format
def writeDictToFile(fname, dic):
	if fname[-4] == "." and fname[-4:] != ".txt":
		print("--- ERROR: Output can only be written to a text (.txt) file ---")
		return
	elif fname[-4] != ".":
		fname += ".txt"
	else:
		with open(fname, "w") as file:
			for x, y in dic:
				file.write("%-15s%-15s\n______________________________\n\n" %(x + ":", y))


#
#
###############
# Driver code #
###############
#
#

def main():
	input_amino_acid_sequence = input("Enter amino acid squence (q to quit): ")
	while input_amino_acid_sequence != "q":
		start_time = time.time()
		print("Searching for possible restriction enzymes...\n")

		codon_comb_list = joinTuplesList("", buildPossibleSequences(input_amino_acid_sequence, amino_acid_codons))

		neb_enz_seq = scrape.initNebDict()
		mod_enz_seqs = sanitizeSequences(neb_enz_seq)

		# Narrow down possible enzymes based on length of amino acid sequence
		eliminateEnzymeByLength(mod_enz_seqs, input_amino_acid_sequence)

		absolute_mod_enz_seqs = {}
		for i in mod_enz_seqs:
			absolute_mod_enz_seqs[i] = joinTuplesList("", buildPossibleSequences(mod_enz_seqs[i], ambiguity))

		# Narrow down possible enzymes based on base
		checkAllBases(codon_comb_list, absolute_mod_enz_seqs)

		# Delete keys storing empty lists
		delEmptyKeys(absolute_mod_enz_seqs)

		# Add matches to a final dictionary
		final_dict = getMatches(codon_comb_list, absolute_mod_enz_seqs)

		# Total processing time
		elapsed_time = time.time() - start_time

		# Display to user
		print("---- Found %2d applicable enzymes in %.3f seconds ----\n\n" %(len(final_dict), elapsed_time))
		print("%-15s%-15s\n______________________________\n" %("Enzyme:", "Sequence:"))
		for x, y in final_dict.items():
			print("%-15s%-15s\n______________________________\n\n" %(x + ":", y))


		# Ask for another amino acid sequence
		input_amino_acid_sequence = input("Enter amino acid squence (q to quit): ")

main()