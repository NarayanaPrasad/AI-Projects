AI-Based Resume Screening System
An automated recruitment tool that ranks resumes against job descriptions using Natural Language Processing (NLP), Named Entity Recognition (NER), and Sentence Embeddings.

Overview
  This project simplifies the hiring process by:
  Parsing: Cleaning and normalizing raw resume text.
  NER Extraction: Identifying key entities like Skills and Experience.
  Semantic Search: Calculating similarity scores between a Job Description and a pool of resumes.
  Dashboard: Providing a web interface to upload and rank candidates.

Project Structure
  This repository is designed to be "plug-and-play" in Google Colab. All files are located in the root directory:
  resume_screener.ipynb: The main notebook to run the project.
  app.py: The Flask web application.
  parser.py: Text cleaning and preprocessing logic.
  ner.py: Named Entity Recognition logic.
  embedder.py: Logic for generating sentence embeddings.
  cs_resumes.csv: Pre-generated dataset of Computer Science resumes.

Installation & Setup
  1. Run on Google Colab
  Upload all files from this repository to a single folder in your Google Drive or directly to the Colab session storage.

  Open resume_screener.ipynb in Google Colab.
  
  2. Configure Ngrok (for the Dashboard)
  To access the web dashboard, you need an ngrok account:
  
  Sign up for free at ngrok.com.
  
  In Google Colab, click the Key icon (Secrets) on the left sidebar.
  
  Add a new secret:
  
  Name: NGROK_AUTH
  
  Value: [Your_Ngrok_Authtoken]
  
  Toggle Notebook access to ON.

Usage
  Run the cells in resume_screener.ipynb in order.
  The notebook will automatically detect cs_resumes.csv and skip the download phase.
  Once the last cell runs, a Public URL (e.g., https://xxxx-xx-xx.ngrok-free.app) will be generated.
  Click the link to open the dashboard, paste a Job Description, and see the ranked results.

Tech Stack
  Python (Pandas, NumPy)
  Spacy (NER)
  Streamlit(UI)
  Sentence-Transformers (SBERT for embeddings)
  Flask (Web Framework)
  Pyngrok (Tunneling)
