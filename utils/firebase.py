import json
from dotenv import load_dotenv
import os
from typing import Dict, List, Optional, Union
import firebase_admin
from firebase_admin import credentials, firestore
load_dotenv()


# --- INITIALIZE FIREBASE ---
if not firebase_admin._apps:
    firebase_key_str = os.getenv("FIREBASE_KEY")
    print(firebase_key_str)
    print("hello")
    firebase_key_dict = json.loads(firebase_key_str)
    cred = credentials.Certificate(firebase_key_dict)

    firebase_admin.initialize_app(cred)
db = firestore.client()


def fetch_documents_from_collection(
    collection_name: str,
    filter_field: Optional[str] = None,
    filter_value: Optional[Union[str, List[str]]] = None
) -> List[Dict]:

    collection_ref = db.collection(collection_name)
    all_docs = []

    if filter_field and filter_value is not None:
        if isinstance(filter_value, list):
            batch_size = 30
            for i in range(0, len(filter_value), batch_size):
                chunk = filter_value[i:i + batch_size]
                query = collection_ref.where(filter_field, 'in', chunk)
                docs = query.stream()
                all_docs.extend([doc.to_dict() for doc in docs])
        else:
            query = collection_ref.where(filter_field, '==', filter_value)
            docs = query.stream()
            all_docs.extend([doc.to_dict() for doc in docs])
    else:
        docs = collection_ref.stream()
        all_docs.extend([doc.to_dict() for doc in docs])

    return all_docs


result = fetch_documents_from_collection(
    "skill",
    "conceptUri",
    [
        'http://data.europa.eu/esco/skill/fed5b267-73fa-461d-9f69-827c78beb39d',
        'http://data.europa.eu/esco/skill/05bc7677-5a64-4e0c-ade3-0140348d4125'
    ]
)

print(result)
