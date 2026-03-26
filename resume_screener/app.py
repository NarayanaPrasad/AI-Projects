import streamlit as st
import pandas as pd
import sys
import os
import re

sys.path.append('/content/drive/MyDrive/resume_screener/src')
from parser import load_single_resume
from ner import extract_all
from embedder import get_rankings

st.set_page_config(page_title="AI Resume Ranker Pro", layout="wide")
st.title("Resume Ranking Dashboard")

# --- SIDEBAR ---
st.sidebar.header("Job Configuration")
jd_input = st.sidebar.text_area("Target Job Description:", "Looking for an AI/ML Engineer...", height=250)
st.sidebar.info("Ranking is currently set to a 1:1 balance of AI Semantic Meaning and Keyword Matching.")

AI_W = 1.0
KW_W = 1.0
TOTAL_W = AI_W + KW_W

tab1, tab2 = st.tabs(["📂 Batch Upload & Rank", "👤 Single Profile Analysis"])

def get_kw_score(jd, res_text):
    jd_words = set(re.findall(r'\w+', jd.lower()))
    res_words = set(re.findall(r'\w+', res_text.lower()))
    tech_jd = {w for w in jd_words if len(w) > 3}
    if not tech_jd: return 0.5
    return len(tech_jd.intersection(res_words)) / len(tech_jd)

# --- TAB 1: BATCH ---
with tab1:
    st.header("Upload Multiple Resumes")
    files = st.file_uploader("Select PDFs or DOCX", type=["pdf", "docx"], accept_multiple_files=True, key="batch_upload")
    
    if st.button("Rank All Candidates") and files:
        results, cleaned_texts = [], []
        for i, f in enumerate(files):
            t_path = os.path.join("/content", f.name)
            with open(t_path, "wb") as file: file.write(f.getbuffer())
            raw, cleaned = load_single_resume(t_path)
            data = extract_all(cleaned, raw, i) # Passing index i for name fallback
            results.append(data)
            cleaned_texts.append(cleaned)
            
        ai_scores = get_rankings(jd_input, cleaned_texts)
        final_list = []
        for i, score in enumerate(ai_scores):
            kw_s = get_kw_score(jd_input, cleaned_texts[i])
            combined = (score * (AI_W/TOTAL_W)) + (kw_s * (KW_W/TOTAL_W))
            res = results[i]
            res['Match Score'] = f"{combined:.2%}"
            res['raw_score'] = combined
            final_list.append(res)
            
        df = pd.DataFrame(final_list).sort_values('raw_score', ascending=False)
        st.subheader("Final Rankings")
        st.dataframe(df[['name', 'Match Score', 'experience', 'education', 'skills']], use_container_width=True)

# --- TAB 2: SINGLE ---
with tab2:
    st.header("Detailed Candidate Analysis")
    single_file = st.file_uploader("Upload a single resume", type=["pdf", "docx"], key="single_upload")
    
    if single_file:
        t_path = os.path.join("/content", single_file.name)
        with open(t_path, "wb") as f: f.write(single_file.getbuffer())
        
        raw, cleaned = load_single_resume(t_path)
        # FIX: Added 'candidate_id=0' here so the name fallback works exactly like Batch mode
        res = extract_all(cleaned, raw, candidate_id=0) 
        
        ai_s = get_rankings(jd_input, [cleaned])[0]
        kw_s = get_kw_score(jd_input, cleaned)
        final_s = (ai_s * (AI_W/TOTAL_W)) + (kw_s * (KW_W/TOTAL_W))
        
        col1, col2 = st.columns([2, 1])
        with col1:
            st.markdown(f"### Candidate: {res['name']}")
            st.write(f"**🏫 Education:** {res['education']}")
            st.write(f"**⏳ Experience:** {res['experience']}")
            st.write("**🛠 Skills Detected:**")
            st.write(", ".join(res['skills']) if res['skills'] else "None detected")
            
        with col2:
            st.metric("Final Match Score", f"{final_s:.2%}")
            st.progress(final_s)
