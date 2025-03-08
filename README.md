# Project Overview

A Streamlit-based tool for analyzing drug-protein interactions using Groq AI and visualizing 3D structures with py3Dmol. Fetches NCBI data, evaluates binding affinity and resistance mutations, and provides detailed reports. Ideal for bioinformatics and drug discovery research.


## Features

- **Drug-Protein Interaction Analysis**: Utilizes Groq AI to assess binding affinity, resistance mutations, and interaction mechanisms.

- **NCBI Data Fetching**: Retrieves relevant protein and drug data from NCBI Entrez.

- **3D Visualization**: Displays protein-ligand interactions using py3Dmol.

- **User-Friendly Interface**: Streamlit-powered UI for easy input and interpretation of results.


## Installation

Ensure you have Python installed, then install the required dependencies:
```python
 pip install streamlit groq requests dotenv py3Dmol
```
## How to Run

- Navigate to the project directory.

- Run the Streamlit app:
```python
 streamlit run app.py
```

- Use the interface to input protein and drug details, analyze interactions, and visualize molecular structures.

## License

This project is licensed under [MIT](https://choosealicense.com/licenses/mit/) license.
