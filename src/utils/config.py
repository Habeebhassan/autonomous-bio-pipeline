import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Access the variables
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
NCBI_EMAIL = os.getenv("NCBI_EMAIL")

# Validation: Fail fast if the key is missing
if not GOOGLE_API_KEY:
    raise ValueError("CRITICAL ERROR: GOOGLE_API_KEY not found. Please check your .env file.")

if not NCBI_EMAIL:
    print("WARNING: NCBI_EMAIL not found in .env. Biopython functionality may be limited.")

# This print statement is for your sanity check only (remove later)
print(f"Configuration Loaded. User Email: {NCBI_EMAIL}")
