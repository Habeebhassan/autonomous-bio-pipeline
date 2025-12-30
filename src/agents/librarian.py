import os
from Bio import Entrez
from src.utils.config import NCBI_EMAIL

class LibrarianAgent:
    def __init__(self):
        """Initialize the agent with credentials."""
        # Biopython requires an email for all requests
        Entrez.email = NCBI_EMAIL
        # Define output directory
        self.raw_data_dir = os.path.join("data", "raw")
        
        # Ensure the directory exists
        os.makedirs(self.raw_data_dir, exist_ok=True)

    def search_genbank(self, query, max_results=5):
        """
        Searches NCBI Nucleotide database for a specific term.
        Returns a list of IDs.
        """
        print(f"Librarian is searching NCBI for: '{query}'...")
        
        try:
            # Research: Search the database
            handle = Entrez.esearch(db="nucleotide", term=query, retmax=max_results)
            record = Entrez.read(handle)
            handle.close()
            
            id_list = record["IdList"]
            print(f"Found {len(id_list)} matches.")
            return id_list
            
        except Exception as e:
            print(f"Error during search: {e}")
            return []

    def download_data(self, id_list, filename_prefix):
        """
        Downloads FASTA sequences for the given ID list.
        Saves them to data/raw.
        """
        if not id_list:
            print("No IDs provided to download.")
            return

        print(f"Downloading {len(id_list)} sequences...")
        
        try:
            # efetch: Fetch the actual data
            # retmode="text" means we get plain text (string)
            # rettype="fasta" means we want the FASTA format
            handle = Entrez.efetch(db="nucleotide", id=id_list, rettype="fasta", retmode="text")
            data = handle.read()
            handle.close()
            
            # Construct the file path
            filename = f"{filename_prefix}.fasta"
            filepath = os.path.join(self.raw_data_dir, filename)
            
            # Save to file
            with open(filepath, "w") as f:
                f.write(data)
                
            print(f"Saved raw data to: {filepath}")
            return filepath

        except Exception as e:
            print(f"Error during download: {e}")
            return None

    def run(self, query):
        """Main method to orchestrate search and download."""
        ids = self.search_genbank(query)
        if ids:
            # Create a safe filename from the query (replace spaces with underscores)
            safe_name = query.replace(" ", "_")
            return self.download_data(ids, safe_name)
        else:
            print("Process aborted: No data found.")
            return None