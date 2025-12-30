import os
import shutil
from Bio import SeqIO

class CuratorAgent:
    def __init__(self, min_length=100, max_n_content=0.05):
        """
        min_length: Minimum number of base pairs required.
        max_n_content: Maximum allowed percentage of 'N' (unknown bases).
        """
        self.raw_dir = os.path.join("data", "raw")
        self.processed_dir = os.path.join("data", "processed")
        self.log_dir = os.path.join("data", "logs")
        
        # Configuration
        self.min_length = min_length
        self.max_n_content = max_n_content

        # Ensure directories exist
        os.makedirs(self.processed_dir, exist_ok=True)
        os.makedirs(self.log_dir, exist_ok=True)

    def validate_sequence(self, record):
        """Returns True if sequence passes QC, else False + Reason."""
        seq_len = len(record.seq)
        
        # Check 1: Length
        if seq_len < self.min_length:
            return False, f"Too short ({seq_len} bp < {self.min_length} bp)"
    
        # Check 2: Ambiguous Bases (N)
        n_count = record.seq.count("N")
        n_ratio = n_count / seq_len
        if n_ratio > self.max_n_content:
            return False, f"Too many Ns ({n_ratio:.2%} > {self.max_n_content:.0%})"
            
        return True, "Passed"

    def process_files(self):
        """Scans raw folder and filters files."""
        files = [f for f in os.listdir(self.raw_dir) if f.endswith(".fasta")]
        
        if not files:
            print("No FASTA files found in data/raw to process.")
            return

        print(f"Curator scanning {len(files)} files...")
        
        for filename in files:
            file_path = os.path.join(self.raw_dir, filename)
            
            try:
                # Parse FASTA (handling multi-record files if necessary)
                # For this pipeline, we assume 1 sequence per file or treat the file as a batch
                records = list(SeqIO.parse(file_path, "fasta"))
                
                if not records:
                    print(f"Empty file: {filename}")
                    continue

                # We accept the file only if ALL sequences inside are valid
                file_valid = True
                reasons = []

                for record in records:
                    valid, reason = self.validate_sequence(record)
                    if not valid:
                        file_valid = False
                        reasons.append(reason)
                        break # One bad apple spoils the bunch
                
                if file_valid:
                    # Move to processed
                    shutil.move(file_path, os.path.join(self.processed_dir, filename))
                    print(f"Verified & Moved: {filename}")
                else:
                    # Log rejection
                    log_file = os.path.join(self.log_dir, "rejected_files.txt")
                    with open(log_file, "a") as f:
                        f.write(f"{filename}: REJECTED - {', '.join(reasons)}\n")
                    print(f"Rejected: {filename} (See logs)")

            except Exception as e:
                print(f"Error processing {filename}: {e}")