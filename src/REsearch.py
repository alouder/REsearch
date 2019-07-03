from itertools import product
import test
import scrape

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
