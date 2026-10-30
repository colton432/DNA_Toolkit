import argparse
# argparse is a python tool for handling information someone gives the program when they start it from a terminal known as command-line arguments
# its just a library we need to import to use specific functions, examples later

from .analysis import find_motif, gc_percentage
from .fasta import read_fasta


def main():
    parser = argparse.ArgumentParser(
        description="Analyze DNA sequences in a FASTA file."
    )
    parser.add_argument("fasta_file", help="Path to the FASTA file to analyze.")
    parser.add_argument(
        "--motif",
        help="Optional DNA motif to search for, such as ATG.",
    )

    args = parser.parse_args()

    try:
        records = read_fasta(args.fasta_file)
    except (OSError, ValueError) as error:
        parser.error(str(error))

    for header, sequence in records:
        print(f">{header}")
        print(f"Length: {len(sequence)}")

        gc = gc_percentage(sequence)
        if gc is None:
            print("GC content: N/A (no known bases)")
        else:
            print(f"GC content: {gc:.2f}%")

        if args.motif is not None:
            try:
                positions = find_motif(sequence, args.motif)
            except ValueError as error:
                parser.error(str(error))

            print(f"Motif {args.motif.upper()} positions: {positions}")

        print()


if __name__ == "__main__":
    main()