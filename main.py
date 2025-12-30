import argparse
import sys
from src.agents.librarian import LibrarianAgent
from src.agents.curator import CuratorAgent
from src.agents.analyst import AnalystAgent

def main(query):
    print(f"\nSTARTING BIOINFORMATICS PIPELINE")
    print(f"Target: {query}")
    print("="*40)

    # --- STAGE 1: Data Retrieval ---
    print("\n[Stage 1] Initializing Agent A: The Librarian...")
    librarian = LibrarianAgent()
    file_path = librarian.run(query)
    
    if not file_path:
        print("Pipeline stopped: No data found.")
        sys.exit(1)

    # --- STAGE 2: Quality Control ---
    print("\n[Stage 2] Initializing Agent B: The Curator...")
    curator = CuratorAgent(min_length=100)
    curator.process_files()

    # --- STAGE 3: Analysis ---
    print("\n[Stage 3] Initializing Agent C: The Analyst...")
    analyst = AnalystAgent()
    analyst.generate_report()

    print("\n" + "="*40)
    print("PIPELINE FINISHED SUCCESSFULLY")
    print("Report available at: analysis_report.md")

if __name__ == "__main__":
    # Set up command line argument parsing
    parser = argparse.ArgumentParser(description="Autonomous Bioinformatics Pipeline")
    parser.add_argument(
        "--query", 
        type=str, 
        help="Biological query (e.g., 'INS Homo sapiens')",
        required=True
    )
    
    args = parser.parse_args()
    main(args.query)