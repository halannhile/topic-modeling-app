import numpy as np
from sentence_transformers import SentenceTransformer
import streamlit as st

from .utils import UploadedDocument


@st.cache_resource(show_spinner="Loading pretrained model...")
def get_pretrained_model(model_path: str = "MaartenGr/BERTopic_Wikipedia"):
    # this import is in here because it's quite slow
    # so we only want to import it when we need it
    from bertopic import BERTopic

    model = BERTopic.load(model_path)
    return model


def transform_doc_pretrained(
    doc: UploadedDocument,
) -> tuple[int, float, str]:
    pretrained_model = get_pretrained_model()
    topic, prob = pretrained_model.transform(doc.content)
    return topic[0], prob.item(), pretrained_model.topic_labels_[topic[0]]  # type: ignore


'''
Encountered error: 
- ValueError: k must be less than or equal to the number of training points
File "sklearn\neighbors\_binary_tree.pxi", line 1127, in sklearn.neighbors._kd_tree.BinaryTree.query

Nhi's suggestion: 
- add a check to ensure that the number of documents provided for training is greater than or equal to 
the number of clusters specified
'''

def train_model(docs: list[UploadedDocument], save_path: str, num_clusters: int = 5) -> None:

    # TODO: allow user to choose the num_clusters based on their dataset

    if len(docs) < num_clusters:
        raise ValueError("Number of documents must be greater than or equal to the number of clusters.")

    pbar = st.progress(0.0, text="Initializing model...")

    from bertopic import BERTopic

    model = BERTopic(verbose=True)
    # TODO support other embedding models
    embed_model_path = "sentence-transformers/all-MiniLM-L6-v2"
    embedder = SentenceTransformer(embed_model_path)

    batch_size = 32
    embeddings = []
    batches = [docs[i : i + batch_size] for i in range(0, len(docs), batch_size)]
    for i, batch in enumerate(batches):
        pbar.progress(
            0.1 + 0.7 * (i / len(batches)),
            text=f"Embedding batch {i+1}/{len(batches)}...",
        )
        embeddings.extend(embedder.encode([doc.content for doc in batch]))
    embeddings = np.array(embeddings)

    pbar.progress(0.8, text="Training model...")
    model.fit([doc.content for doc in docs], embeddings=embeddings, n_topics=num_clusters)  # type: ignore

    pbar.progress(0.9, text="Saving model...")
    model.save(
        save_path,
        serialization="safetensors",
        save_ctfidf=True,
        save_embedding_model=embed_model_path,
    )
    pbar.progress(1.0, text="Training complete.")


from bertopic import BERTopic
from sentence_transformers import SentenceTransformer
from typing import List
from nlp.topic_modeling import UploadedDocument
import os 

def train_model_2(docs: List[UploadedDocument], save_path: str, num_clusters: int = 5) -> None:
    """
    Train a BERTopic model on the pre-processed documents and save the model to the specified path.

    Args:
        docs (List[UploadedDocument]): Pre-processed documents.
        save_path (str): Path to save the trained model.
        num_clusters (int, optional): Number of clusters/topics to extract. Defaults to 5.
    """
    # Check if the number of clusters is greater than the number of documents
    # TODO: i don't think this is needed in this implementation but leaving here for reference
    if num_clusters > len(docs):
        raise ValueError("Number of clusters must be less than or equal to the number of documents.")

    # Ensure that the directory exists, create it if it doesn't
    os.makedirs(save_path, exist_ok=True)

    # Initialize the BERTopic model
    model = BERTopic()

    # Create embeddings using SentenceTransformer
    embed_model_path = "sentence-transformers/all-MiniLM-L6-v2"
    embedder = SentenceTransformer(embed_model_path)
    embeddings = embedder.encode([doc.content for doc in docs])

    # Train the model
    topics, _ = model.fit_transform([doc.content for doc in docs], embeddings)

    # Save the model: https://maartengr.github.io/BERTopic/api/bertopic.html#bertopic._bertopic.BERTopic.save
   # Save the model using all three methods listed in documentation
    model.save(os.path.join(save_path, "model.pickle"), serialization="pickle")
    model.save(os.path.join(save_path, "model_safetensors"), serialization="safetensors", save_embedding_model=True, save_ctfidf=False)
    model.save(os.path.join(save_path, "model_pytorch"), serialization="pytorch")