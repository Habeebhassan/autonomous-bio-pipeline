import streamlit as st
import time
import os
from src.agents.librarian import LibrarianAgent
from src.agents.curator import CuratorAgent
from src.agents.analyst import AnalystAgent

# Page Config
st.set_page_config(page_title="Bio-Agent Pipeline", page_icon="🧬", layout="wide")

st.title("Autonomous Bioinformatics Agent Team")
st.markdown("""
**Objective:** Automate the retrieval, cleaning, and analysis of biological data.
Enter a query below (e.g., *'INS Homo sapiens RefSeq'*) and watch the agents work.
""")

# Sidebar for controls
with st.sidebar:
    st.header("Configuration")
    query = st.text_input("Enter Gene Query:", value="INS[Gene] AND Homo sapiens[Organism] AND RefSeq")
    run_btn = st.button("Launch Pipeline", type="primary")

# Main execution logic
if run_btn:
    st.divider()
    
    # --- Agent A ---
    st.subheader("Agent A: The Librarian")
    with st.status("Searching NCBI Database...", expanded=True) as status:
        st.write(f"Querying: `{query}`")
        librarian = LibrarianAgent()
        file_path = librarian.run(query)
        
        if file_path:
            st.success(f"Downloaded: `{os.path.basename(file_path)}`")
            status.update(label="Retrieval Complete", state="complete", expanded=False)
        else:
            st.error("No data found.")
            status.update(label="Retrieval Failed", state="error")
            st.stop()

    # --- Agent B ---
    st.subheader("Agent B: The Curator")
    with st.status("Performing Quality Control...", expanded=True) as status:
        curator = CuratorAgent(min_length=100)
        # We capture the output by checking the processed folder
        curator.process_files()
        
        # Simple check to see if files exist in processed
        processed_files = os.listdir("data/processed")
        if processed_files:
            st.write(f"Verified {len(processed_files)} sequence file(s).")
            status.update(label="QC Complete", state="complete", expanded=False)
        else:
            st.error("QC Failed: All files rejected.")
            st.stop()

    # --- Agent C ---
    st.subheader("Agent C: The Analyst")
    with st.status("Analyzing Sequences & Consulting Gemini...", expanded=True) as status:
        analyst = AnalystAgent()
        analyst.generate_report()
        st.write("Report generated successfully.")
        # status.update(label="Analysis Complete", state="complete", expanded=False)
        # --- NEW VISUALIZATION SECTION ---
        st.write(" Generating Visualizations...")
        df = analyst.get_stats_dataframe()
        status.update(label="Analysis & Visualization Complete", state="complete", expanded=False)

    # --- Results Display ---
    st.divider()
    
    # 1. VISUALIZATIONS (New Tab View)
    st.header("Data Analytics")
    
    if not df.empty:
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Sequence Lengths")
            # Create a Bar Chart
            st.bar_chart(df.set_index("Gene ID")["Length (bp)"], color="#FF4B4B")
            st.caption("Comparison of gene sequence lengths.")
            
        with col2:
            st.subheader("GC Content")
            # Create a Bar Chart
            st.bar_chart(df.set_index("Gene ID")["GC Content (%)"], color="#4B4BFF")
            st.caption("GC Content indicates stability (Human avg: ~40-60%).")
            
        # Show Raw Data Table
        with st.expander("View Raw Data"):
            st.dataframe(df)
            
    # 2. THE TEXT REPORT
    st.header("Biological Insights Report")
    if os.path.exists("analysis_report.md"):
        with open("analysis_report.md", "r") as f:
            report_content = f.read()
        st.markdown(report_content)
    else:
        st.error("Report file not found.")

    # --- Results Display ---
    st.divider()
    st.header("Final Report")
    
    if os.path.exists("analysis_report.md"):
        with open("analysis_report.md", "r") as f:
            report_content = f.read()
        st.markdown(report_content)
    else:
        st.error("Report file not found.")