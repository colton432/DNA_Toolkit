from .analysis import validate_sequence
# this imports the function validate_sequence from our other analysis file so we can call it in this file

def read_fasta(file_path):
# this function 'read_fasta' will take an input of file_path
    """Read a FASTA file and return (header, sequence) pairs."""
    records = []
    header = None
# We set header = None since we don't have a header yet
    sequence_parts = []

    with open(file_path, "r", encoding="utf-8") as fasta_file:
# We open our 'file_path' in "r" which means read mode(we cant change anything in 'file_path')
# encoding="utf-8" tells python how the file's text is encoded, in this case its encoded in utf-8 (which is common)

# We use with .... as because 'with' opens the file and make it avaliable under the name fasta_file (so the file will be known as fasta_file)


        for line_number, line in enumerate(fasta_file, start=1):
# using the for loop we will loop through the fasta_file one line at a time
# line_number is the line's number, starting at 1 since thats how we count
# 'line' will equal the actual text from that line
# Example the first time through, line_number = 1 and line = >sequence_one\n

            line = line.strip()
# We take the string in line and strip it of all white space

            if not line:
                continue
# this checks 'line' after we strip it and if its empty we skip over it
# continue means - stop working on this line and move to the next one

            if line.startswith(">"):
# Because fasta files start with '>' at the begining of a sequence we can use this to determin the begining of the sequence

                if header is not None:
                    sequence = "".join(sequence_parts)
                    records.append((header, validate_sequence(sequence)))
# If the header has value no equal to None run this if statement
# We skip over it the first round since our header is still None(this will change later)
# '"".join()' will combine all the sequence lines from 'sequence_parts' into one string and assign it to 'sequence' variable
# validate_sequence(sequence) checks that the combined sequence contains the allowed  DNA character, this function was the one we imported from analysis
# (header, ...) makes a tuple containg the header and the cleaned sequence
# records.append() will add that tuple to the list of records


# We initialize the header now making it the string from line 1
# line[1:] takes the line starting at index 1, which removes the first character ">" this is becuase we start at 1 instead of 0 so we skip over the first character in the string which is ">"
# Then runs '.strip()' which will remove any white space
# so ">sequence_two" becomes "sequence_two"
                header = line[1:].strip()
                if not header:
                    raise ValueError(f"Missing header text on line {line_number}.")
# If the line was just a ">" and no name after it, header will be empty. This will raise the error which includes the line number

                sequence_parts = []
# Now that were gonna start a new record we reset the sequence-line list so it won't include bases from the previous record

# This else statement will run when the line doesn't start with ">" which means it will be a sequence line
            else:
                if header is None:
                    raise ValueError(
                        f"Sequence data found before a FASTA header "
                        f"on line {line_number}."
                    )
# If sequence text appears before any header, the file is malformed. This will raise and error and report which line caused it

                sequence_parts.append(line)
# Otherwise, add the sequence line to the current record. If the sequence wraps across several lines, they're collected here and joined when the record ends


#If your header has something in it run this code
    if header is not None:
        sequence = "".join(sequence_parts)
        records.append((header, validate_sequence(sequence)))
# You should know what each of these does now
# It will assign sequence the joined parts of sequence_parts
# put the header and the allowed DNA character into the records list

# if no records were collected (such as the file was empty or contained only blank lines) the fucntion will raise an error
    if not records:
        raise ValueError("No FASTA records found.")

    return records
# Finally return sends the completed list back to whoever called read_fasta.
# Example, for a file with two records, it might return
#[
#    ("sequence_one", "ACGTTGCA"),
#    ("sequence_two", "AAAA"),
#]