import tkinter as tk
from tkinter import filedialog

from .analysis import find_motif, gc_percentage
from .fasta import read_fasta


def main():
    root = tk.Tk()
    root.withdraw()

    fasta_path = filedialog.askopenfilename(
        title="Choose a FASTA file",
        filetypes=[
            ("FASTA files", "*.fasta *.fa *.fna"),
            ("All files", "*.*"),
        ],
    )

    root.destroy()

    if not fasta_path:
        print("No file selected. Exiting.")
        return

    motif = input("Enter a motif to search for, or press Enter to skip: ").strip()

    try:
        records = read_fasta(fasta_path)

        for header, sequence in records:
            print(f"\n>{header}")
            print(f"Length: {len(sequence)}")

            gc = gc_percentage(sequence)
            if gc is None:
                print("GC content: N/A (no known bases)")
            else:
                print(f"GC content: {gc:.2f}%")

            if motif:
                positions = find_motif(sequence, motif)
                print(f"Motif {motif.upper()} positions: {positions}")

    except (OSError, ValueError) as error:
        print(f"Error: {error}")


if __name__ == "__main__":
    main()