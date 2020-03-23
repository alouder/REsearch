# REsearch
Finding viable restriction enzymes from NEB given an amino acid sequence.  
*Requires Python 3.x*

### Using the Program
Enter the amino acid sequence which will represent a range of bases in which cleaving should be performed.  

The program will first generate all possible codon combinations given that aimino acid sequence.
  
The program will then search through all of the restriction enzymes that are provided by the vendor, NEB, and return  
a list of enzymes that have restriction sites aligned with inputted amino acid sequence.  

Return values include: 
 - The enzyme name
 - The recognition sequence of the enzyme
 - The matching DNA sequence, corresponding to the inputted amino acid sequence
 
This program is designed such that you only need to enter an amino acid sequence. All amino acids entered are preserved when a DNA sequence that matches a restricion enzyme's cut site is suggested. You will need to compare the suggested DNA a sequence(s) to your 
specific sequence to determine if the strand needs to be edited.

## Development Setup

#### Linux/macOS
- Install Python virtual environment:
  - `python3 -m pip install virtualenv`
- Create a virtual environment within the REsearch root directory:
  - `python3 -m venv env`
- Activate the virtual enviornment:
  - `source ./env/bin/activate`
- Install package dependencies:
  - `pip install -r requirements.txt`
  
#### Windows
- Install Python virtual environment:
  - `python -m pip install virtualenv`
- Create a virtual environment within the REsearch root directory:
  - `python -m venv env`
- Activate the virtual enviornment:
  - `./env/Scriptsin/activate`
- Install package dependencies:
  - `pip install -r requirements.txt`
  
## Running the Program
To run the program, activate the virtual environment and run REsearch.py in REsearch/src/ from the terminal

## Reminders
- Remember to activate the virtual environment BEFORE installing python packages with pip, and before running the program
- If module errors are encountered remember to run:
  - `pip install -r requirements.txt`
- When finished, deactivate the virtual environment with command "deactivate"
