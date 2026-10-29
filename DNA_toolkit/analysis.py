VALID_BASES = set("ACGTN")
# This creates a set of allowed characters "A,C,G,T,N" and assigns them to 
# VALID_BASES which is in all upper case(naming convention for stuff we keep constant)


# using 'def' is how we start a function
# 'normalize_sequence is the function name
# 'sequence is a input parameter
def normalize_sequence(sequence):
    return "".join(sequence.split()).upper()
# in our line with return 'sequence.split' will break the text apart wherever there is whitespace(spaces or line breaks)
# we put '.join' to join those pieces back together leaving out the whitespace
# and the '.upper()' at the end makes each character an upper case
# finally the 'return' sends whatever normalized_sequence actually made(uppercase sequence) to whoever calls this function


def validate_sequence(sequence):
    cleaned = normalize_sequence(sequence)
# The cleaned variable stores the result from our previous 'normalize_sequence function(which is an all uppercase sequence)
    if not cleaned:
# The 'if not' means if the clean variable is empty
        raise ValueError("Sequence is empty.")
# The 'raise ValueError' stops the function and reports a promblem(in this case the cleaned variable is empty)

    invalid_bases = set(cleaned) - VALID_BASES
# 'set(cleaned)' will make another set of the characters found in cleaned
# "set(cleaned) - Values" finds characters in the sequence but not in the allowed VALID_BASES set
    if invalid_bases:
# 'if invalid_bases' checks whether invalid_bases contains any characters
        invalid_text = ", ".join(sorted(invalid_bases))
# 'sorted(invalid_bases)' takes the characters assigned to invalid_bases, then sorts them in a predictable order with 'sorted'
# and then '", ".join()' takes those characters and puts them together with a ',' to seperate them
        raise ValueError(f"Invalid DNA characters: {invalid_text}")
# in this raise ValueError we include a 'f' character before the error message which lets Python insert the value of 'invalid_text'
# inside of {}, without the 'f' we will just print the character {invalid_text} instead of the variable

    return cleaned
# if no errors occur then this functions just returns the cleaned sequence without changing anything
# Example if cleaned = "ACGTZ" this would raise an error since "Z" isn't allowed 

# This function will tell us what fraction of the known bases are G or C
def gc_percentage(sequence):
    """Calculate GC percentage among known bases, ignoring N bases."""
    cleaned = validate_sequence(sequence)
# assigns the cleaned sequence to to the cleaned variable
    known_bases = [base for base in cleaned if base != "N"]
# '[base for base in cleaned if base != "N"]' in this we initiallize base which will be a temporary variable we dont need to define it
# before since this is the syntax for list comprehension, we assign a character in 'cleaned' to base, then check if that character is = N
# If it is then we continue with the for loop not assigning it to 'known_bases'  if it isn't = N then we put it in 'known_bases' which is a list
# so if cleaned = "AGCN" known_bases = ["A", "G", "C"]

    if not known_bases:
        return None
# if 'if not known_bases' is empty because 'cleaned' only contained N's then we return nothing since we can't calculate anything
    gc_count = sum(base in "GC" for base in known_bases)
# 'sum()' will count how many bases in 'known_bases' are either G or C it will return a number based on this
# so if known_bases = AGC gc_count = 2 since G and C apear once each

    return gc_count / len(known_bases) * 100
# here 'len()' in a python function that returns the number of items in something, so if known_bases = ACG  len(known_bases) = 3

def find_motif(sequence, motif):
    """Return 1-based positions of exact motif matches, including overlaps."""
    cleaned = validate_sequence(sequence)
    motif = normalize_sequence(motif)

    if not motif:
        raise ValueError("Motif is empty.")

    if set(motif) - set("ACGT"):
        raise ValueError("Motif must contain only A, C, G, and T.")

    positions = []
#create an empty list to sore the match positions
    start = 0
#This will be a variable to let python know where it should begin searching, in this case at 0 (the begining)

    while True:
#'while True' means this function will keep running/searching until it reaches a break
        match_index = cleaned.find(motif, start)
# we start the loop, first initialized match_index to equal 'cleaned.find(motif, start)'
# first 'find(motif, start)' the find() function is a function that look for one string in another one
# so we have our variable motif which will equal 'normalize_sequence' in this example we'll say ATG
# 'start' will be initialized at 0
# 'cleaned.find()' means we search whatevers in 'cleaned' for the string in motif (since motif is in .find()) and we start the search at 0
# then you return whatever value you find that specific string at so if you search for ATG within the string AACGATC you return 4

# if it cant find motif .find() will return -1
# this triggers this if statment which breaks the loop of 'While true'
        if match_index == -1:
            break

# This adds the matched position to the list. We do +1 since we want want to have a 1-based position instead of 0-based position count
        positions.append(match_index + 1)
#Sets the next search to begin one character after the match started. Which means we wont find any repeated string.
        start = match_index + 1

    return positions
# After the loop ends, return the list of positions.