import os
import pinecone
from panns_inference import AudioTagging
import librosa
import soundfile as sf
import numpy as np

pinecone_index = os.getenv('PINECONE_INDEX', 'audio-embeddings')
pinecone_api_key = os.getenv('PINECONE_API_KEY')
pinecone_environment = os.getenv('PINECONE_ENVIRONMENT')

def get_similar_audios(local_file_path):
    try:
        pinecone.init(
            api_key=pinecone_api_key,
            environment=pinecone_environment
        )
        if pinecone_index in pinecone.list_indexes():
            index = pinecone.Index(pinecone_index)

        audio_tagging = AudioTagging(checkpoint_path=None, device='cuda')

        y, _ = sf.read(local_file_path)
        print(f"Generating Embedding for: {local_file_path}")
        _, emb = audio_tagging.inference(y[None, :])
        query_emb = (str(local_file_path), emb.tolist())
        
        results = index.query(query_emb[1], top_k=3)
        results = [match.get('id') for match in results.get("matches")]
        index.describe_index_stats()
        print("Data processed and embeddings retrieved from Pinecone.")
        return results
    except Exception as e:
        return f"Error: {str(e)}"
