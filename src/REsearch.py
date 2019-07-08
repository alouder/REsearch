from itertools import product
import time, re, test, scrape
# import test
# import scrape

# Dictionary to store all of the codons for each of the amino acids (U replaced with T for simplicity)
amino_acid_codons = {
	"A": ["GCT", "GCC", "GCA", "GCG"],
	"R": ["CGT", "CGC", "CGA", "CGG", "AGA", "AGG"],
	"N": ["AAT", "AAC"],
	"D": ["GAT", "GAC"],
	# Add 'B' asparagine OR aspartic acid for ambiguity
	"C": ["TGT", "TGC"],
	"Q": ["CAA", "CAG"],
	"E": ["GAA", "GAG"],
	# Add 'Z' glutamine OR glutamic acid for ambiguity
	"G": ["GGT", "GGC", "GGA", "GGG"],
	"H": ["CAT", "CAC"],
	"I": ["ATT", "ATC", "ATA"],
	"L": ["TTA", "TTG", "CTT", "CTC", "CTA", "CTG"],
	"K": ["AAA", "AAG"],
	"M": ["ATG",],
	"F": ["TTT", "TTC"],
	"P": ["CCT", "CCC", "CCA", "CCG"],
	"S": ["TCT", "TCC", "TCA", "TCG", "AGT", "AGC"],
	"T": ["ACT", "ACC", "ACA", "ACG"],
	"W": ["TGG",],
	"Y": ["TAT", "TAC"],
	"V": ["GTT", "GTC", "GTA", "GTG"],
	"stop": ["TAA", "TAG", "TGA"]
}

# Dictionary to store all bases that correspond to symbols that represent ambiguity
ambiguity = {
	"G": ["G"],
	"C": ["C"],
	"A": ["A"],
	"T": ["T"],
	"R": ["G", "A"],
	"Y": ["C", "T"],
	"M": ["A", "C"],
 	"K": ["G", "T"],
	"S": ["G", "C"],
	"W": ["A", "T"],
	"B": ["C", "G", "T"],
	"D": ["A", "G", "T"],
	"H": ["A", "C", "T"],
	"V": ["A", "C", "G"],
	"N": ["G", "C", "A", "T"] #["N"]
}

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

# Driver code
input_amino_acid_sequence = input("Enter amino acid squence: ")
start_time = time.time()
print("Searching for possible restriction enzymes...\n")

codon_comb_list = joinTuplesList("", buildPossibleSequences(input_amino_acid_sequence, amino_acid_codons))

# Establish var from restriction enzyme dictionary in scrape.py (###TO BE MODULARIZED###)
neb_enz_seq = scrape.neb_enz_seq_dict

# Modified dictionaries to hold the RE recognition sequence stirngs (and corresponding REs) with out cleavage site indicator (for processing).
# Palindromic and non-palindromic enzymes are distinguished.
mod_enz_seqs = {}
for i in neb_enz_seq:
	if not isPalindromic(neb_enz_seq[i]):
		mod = re.sub("/", "", neb_enz_seq[i])
		mod_enz_seqs[i] = mod
	else:
		mod = splitNonPalindromic(neb_enz_seq[i])
		mod_enz_seqs[i] = mod

# Narrow down possible enzymes based on length of amino acid sequence
eliminateEnzymeByLength(mod_enz_seqs, input_amino_acid_sequence)

absolute_mod_enz_seqs = {}
for i in mod_enz_seqs:
	absolute_mod_enz_seqs[i] = joinTuplesList("", buildPossibleSequences(mod_enz_seqs[i], ambiguity))

# Narrow down possible enzymes based on base
checkAllBases(codon_comb_list, absolute_mod_enz_seqs)

# Delete keys storing empty lists
toDel = []
for i in absolute_mod_enz_seqs:
	if len(absolute_mod_enz_seqs[i]) == 0:
		toDel.append(i)
for i in toDel:
	del absolute_mod_enz_seqs[i]

# Add matches to a final dictionary
final_dict = {}
for i in codon_comb_list:
	for k in absolute_mod_enz_seqs:
		for v in absolute_mod_enz_seqs[k]:
			if v in i:
				final_dict[k] = i

elapsed_time = time.time() - start_time
# print("---- Found " + str(len(final_dict)) + " applicable enzymes in " + str(elapsed_time) + " seconds----\n\n")
print("---- Found %2d applicable enzymes in %.3f seconds ----\n\n" %(len(final_dict), elapsed_time))
print("%-15s%-15s\n______________________________\n" %("Enzyme:", "Sequence:"))
for x, y in final_dict.items():
	print("%-15s%-15s\n______________________________\n" %(x + ":", y))