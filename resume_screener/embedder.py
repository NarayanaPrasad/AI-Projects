from sentence_transformers import SentenceTransformer, util

# This model is small, fast, and perfect for semantic search.
model = SentenceTransformer('all-MiniLM-L6-v2')

def get_rankings(jd_text, resume_list):
    """
    Compares one Job Description to a list of resumes.
    Returns a list of similarity scores (0.0 to 1.0).
    """
    # Convert JD to a vector
    jd_vec = model.encode([jd_text], convert_to_numpy=True)
    
    # Convert all Resumes to vectors
    res_vecs = model.encode(resume_list, show_progress_bar=True, convert_to_numpy=True)
    
    # Calculate math similarity
    scores = util.cos_sim(jd_vec, res_vecs)[0].tolist()
    return scores
