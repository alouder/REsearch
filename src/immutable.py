############################################
# Class to hold the non-changing data sets
# that will be used in the program.
############################################

class Immutable:
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
	# Dictionary to store all bases that correspond to symbols which represent ambiguity
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