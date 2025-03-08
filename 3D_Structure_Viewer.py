import streamlit as st
import streamlit.components.v1 as components
from groq import Groq
import requests
import os
from dotenv import load_dotenv
import py3Dmol

# Load environment variables
load_dotenv()

# Visualize Protein-Ligand Interaction with py3Dmol
def visualize_protein_ligand_interaction(pdb_id):
    """
    Visualize a protein-ligand interaction using py3Dmol and display it in Streamlit.
    :param pdb_id: str, PDB ID of the protein structure (e.g., "6LU7").
    """
    # Initialize the viewer
    viewer = py3Dmol.view(query=f"pdb:{pdb_id}")
    viewer.setStyle({'cartoon': {'color': 'spectrum'}})  # Cartoon style for the protein
    viewer.addStyle({'hetflag': True}, {'stick': {'colorscheme': 'orangeCarbon'}})  # Stick for ligands
    viewer.zoomTo()

    # Generate the HTML for embedding
    viewer_html = viewer._make_html()

    # Embed the HTML in the Streamlit app
    components.html(viewer_html, height=500)  # Adjust height as needed

class DrugProteinInteractionAnalyzer:
    def _init_(self, api_key=None):
        if api_key:
            self.client = Groq(api_key=api_key)
        else:
            env_key = os.getenv('GROQ_API_KEY')
            if not env_key:
                st.warning("Groq API Key not found. Please enter your API key.")
                env_key = st.text_input("Enter your Groq API Key", type="password")
            if env_key:
                self.client = Groq(api_key=env_key)
            else:
                st.error("No API key provided. Cannot initialize Groq client.")
                self.client = None

    def fetch_ncbi_data(self, query, db):
        """
        Fetch data from NCBI Entrez.
        """
        try:
            url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db={db}&term={query}&retmode=json"
            response = requests.get(url)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            st.error(f"Error fetching NCBI data: {e}")
            return None

    def analyze_interaction(self, protein, drug, interaction_type):
        """
        Analyze drug-protein interaction using Groq API.
        """
        if not self.client:
            st.error("Groq client not initialized. Cannot analyze interaction.")
            return None

        try:
            st.write("Calling Groq API...")
            chat_completion = self.client.chat.completions.create(
                messages=[{
                    "role": "system",
                    "content": """You are a bioscientist specializing in drug-protein interactions. Based on the protein,
                    drug, and interaction type provided, generate a detailed report including binding affinity,
                    interaction mechanisms, and any relevant recommendations."""},
                    {
                    "role": "user",
                    "content": f"Protein: {protein}\nDrug: {drug}\nInteraction Type: {interaction_type}"}],
                model="llama3-70b-8192",
                max_tokens=700,
                temperature=0.7
            )
            return chat_completion.choices[0].message.content
        except Exception as e:
            st.error(f"Error analyzing interaction: {e}")
            return None

def main():
    st.title("🔬 Drug-Protein Interaction Analyzer with 3D Viewer")

    st.sidebar.header("Configuration")
    manual_api_key = st.sidebar.text_input("Groq API Key (optional)", type="password")

    analyzer = DrugProteinInteractionAnalyzer(api_key=manual_api_key)

    st.header("Target Protein")
    protein = st.text_input("Enter protein name, gene name, or accession number (e.g., EGFR, P53)")
    pdb_id = st.text_input("Enter PDB ID for 3D structure (e.g., 1M17, 6J5T)")

    st.header("Drug Compound")
    drug = st.text_input("Enter drug name, PubChem CID, or SMILES string (e.g., Gefitinib, CID:123631)")

    st.header("Interaction Type")
    interaction_type = st.text_input("Enter interaction type (e.g., binding affinity, resistance mutations)")

    if st.button("Analyze Interaction"):
        if not protein.strip() or not drug.strip():
            st.warning("Please provide both protein and drug information.")
            return

        st.subheader("Fetching Data from NCBI...")
        protein_data = analyzer.fetch_ncbi_data(protein, "protein")
        if protein_data:
            st.write("Protein Data:", protein_data)

        st.subheader("Analyzing Interaction...")
        analysis_result = analyzer.analyze_interaction(protein, drug, interaction_type)
        if analysis_result:
            st.header("Interaction Report")
            st.write(analysis_result)

        if pdb_id:
            st.subheader("3D Structure Viewer")
            st.write(f"Displaying 3D structure for PDB ID: {pdb_id}")
            # Display the 3Dmol visualization directly in Streamlit
            visualize_protein_ligand_interaction(pdb_id)
        else:
            st.warning("No PDB ID provided for 3D structure.")

if __name__ == "_main_":
    main()
