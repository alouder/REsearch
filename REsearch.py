from itertools import product
import test

# Dictionary to store all of the codons for each of the amino acids
amino_acid_codons = {
	"A": ["GCU", "GCC", "GCA", "GCG"],
	"R": ["CGU", "CGC", "CGA", "CGG", "AGA", "AGG"],
	"N": ["AAU", "AAC"],
	"D": ["GAU", "GAC"],
	# Add 'B' asparagine OR aspartic acid for ambiguity
	"C": ["UGU", "UGC"],
	"Q": ["CAA", "CAG"],
	"E": ["GAA", "GAG"],
	# Add 'Z' glutamine OR glutamic acid for ambiguity
	"G": ["GGU", "GGC", "GGA", "GGG"],
	"H": ["CAU", "CAC"],
	"I": ["AUU", "AUC", "AUA"],
	"L": ["UUA", "UUG", "CUU", "CUC", "CUA", "CUG"],
	"K": ["AAA", "AAG"],
	"M": ["AUG",],
	"F": ["UUU", "UUC"],
	"P": ["CCU", "CCC", "CCA", "CCG"],
	"S": ["UCU", "UCC", "UCA", "UCG", "AGU", "AGC"],
	"T": ["ACU", "ACC", "ACA", "ACG"],
	"W": ["UGG",],
	"Y": ["UAU", "UAC"],
	"V": ["GUU", "GUC", "GUA", "GUG"],
	"stop": ["UAA", "UAG", "UGA"]
}

# Find the number of possible codon combinations for a particular amino acid sequence
def num_combinations(amino_acid_sequence):
	comb = 1
	for i in amino_acid_sequence:
		comb *= len(amino_acid_codons[i])
	return comb

# Build all of the possible codon combinations for an amino acid sequence using itertools.
# Returns a list of tuples which contain each combination of codons. 
def build_possible_sequences(amino_acid_sequence):
    codon_comb = []
    for i in amino_acid_sequence:
    	codon_comb.append(amino_acid_codons[i])

    return list(product(*codon_comb))
    
# Join the tuples created by build_possible_sequences and return a list of possible RNA sequences (codon combinations) as strings
def join_tuples_list(join_string, tuple_list):
	codon_comb_string = []
	for i in tuple_list:
		s = join_string.join(i)
		codon_comb_string.append(s)
	return codon_comb_string

# Driver code

test_amino_acid_sequence = input("Enter amino acid squence: ")

codon_comb_list = join_tuples_list("", build_possible_sequences(test_amino_acid_sequence))

cnt = 1
for i in codon_comb_list:
	print("%2d. %s" %(cnt, i))
	cnt += 1	
