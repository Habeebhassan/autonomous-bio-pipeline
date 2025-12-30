import os
import google.generativeai as genai
from Bio import SeqIO
from src.utils.config import GOOGLE_API_KEY

class AnalystAgent:
    def __init__(self):
        self.processed_dir = os.path.join("data", "processed")
        self.output_file = "analysis_report.md"
        
        # Configure Gemini
        genai.configure(api_key=GOOGLE_API_KEY)
        self.model = genai.GenerativeModel('gemini-flash-latest')

    def calculate_stats(self, sequence):
        """Calculates basic sequence properties."""
        length = len(sequence)
        g_count = sequence.count("G")
        c_count = sequence.count("C")
        gc_content = (g_count + c_count) / length * 100
        return length, gc_content

    def get_ai_summary(self, description):
        """Asks Gemini to explain the biological function of the gene."""
        print(f"Consulting Gemini about: {description[:50]}...")
        
        prompt = (
            f"You are an expert bioinformatician. "
            f"I have a gene with the following description from a FASTA file: '{description}'. "
            f"Please provide a concise (2-3 sentences) summary of its biological function, "
            f"associated diseases, and clinical importance."
        )
        
        try:
            response = self.model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            return f"Error connecting to AI: {e}"

    def generate_report(self):
        """Reads processed files and generates a markdown report."""
        files = [f for f in os.listdir(self.processed_dir) if f.endswith(".fasta")]
        
        if not files:
            print("No processed files found to analyze.")
            return

        print(f"Analyst starting on {len(files)} files...")
        
        report_content = "# Autonomous Bioinformatics Pipeline Report\n\n"
        
        for filename in files:
            filepath = os.path.join(self.processed_dir, filename)
            
            # Read the sequence
            for record in SeqIO.parse(filepath, "fasta"):
                length, gc = self.calculate_stats(record.seq)
                ai_summary = self.get_ai_summary(record.description)
                
                # Append to report
                report_content += f"## File: {filename}\n"
                report_content += f"**Gene Definition:** {record.description}\n\n"
                report_content += "### Statistics\n"
                report_content += f"- **Length:** {length} bp\n"
                report_content += f"- **GC Content:** {gc:.2f}%\n\n"
                report_content += "### AI Biological Insight\n"
                report_content += f"{ai_summary}\n\n"
                report_content += "---\n\n"

        # Save the report
        with open(self.output_file, "w") as f:
            f.write(report_content)
        
        print(f"Report generated: {self.output_file}")