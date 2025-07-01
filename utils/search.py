from contextlib import asynccontextmanager
from typing import Dict, List
from huggingface_hub import hf_hub_download
from fastapi import FastAPI
import faiss
import json
from utils.firebase import fetch_documents_from_collection
from utils.text_embedding import get_embeddings

index = None
positions = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Handles startup and shutdown events for FastAPI"""
    global index, positions

    print("🚀 Loading model, please wait...")
    
    # Define repo info
    repo_id = "epdemrew/faiss-embedding-index"
    repo_type = "dataset"

    # Download files from Hugging Face
    index_path = hf_hub_download(
        repo_id=repo_id,
        filename="faiss.index",
        repo_type=repo_type
    )

    positions_path = hf_hub_download(
        repo_id=repo_id,
        filename="positions.json",
        repo_type=repo_type
    )

    # Load index and positions
    index = faiss.read_index(index_path)

    with open(positions_path, "r") as f:
        positions = json.load(f)

    print("✅ Embedding loaded successfully!")
    
    yield 
    
    # Cleanup (optional)
    del index
    del positions
    print("🛑 Embedding unloaded, shutting down!")

def search_skills(position)->List[Dict]|None:
    if(index==None or positions==None):
        return None

    query_embedding = get_embeddings([position])
    D, I = index.search(query_embedding, k=5)
    top_results = [positions[i] for i in I[0]]


    if len(top_results)>0:
        positionName = top_results[0]
        position = fetch_documents_from_collection('position','preferredLabel', positionName)
    skills = fetch_documents_from_collection('skill','conceptUri', position[0]['relatedSkills'] if len(position)>0 and len(position[0]['relatedSkills'])>0 else []) if position else None

    print(len(position[0]["relatedSkills"]))
    print(top_results)
    return skills