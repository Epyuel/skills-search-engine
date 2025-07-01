from sentence_transformers import SentenceTransformer
from typing import List
import numpy as np

# Load the model once (small, fast, good quality)
model = SentenceTransformer('all-MiniLM-L6-v2')

def get_embeddings(texts: List[str]) -> np.ndarray:
    embeddings = model.encode(texts, show_progress_bar=True)
    return np.array(embeddings, dtype='float32')