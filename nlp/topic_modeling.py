import numpy as np
import os
from sentence_transformers import SentenceTransformer
import streamlit as st

from .utils import UploadedDocument


@st.cache_resource(show_spinner="Loading pretrained model...")
def get_pretrained_model(model_path: str = "MaartenGr/BERTopic_Wikipedia"):
    # this import is in here because it's quite slow
    # so we only want to import it when we need it
    from bertopic import BERTopic

    model: BERTopic = BERTopic.load(model_path)
    return model


def transform_doc_pretrained(
    doc: UploadedDocument,
) -> tuple[int, float, str]:
    pretrained_model = get_pretrained_model()
    topic, prob = pretrained_model.transform(doc.content)
    return topic[0], prob.item(), pretrained_model.topic_labels_[topic[0]]  # type: ignore


def train_model(docs: list[UploadedDocument], save_path: str) -> None:
    """
    Train a BERTopic model on the pre-processed documents and save the model to the specified path.

    Args:
        docs (List[UploadedDocument]): Pre-processed documents.
        save_path (str): Path to save the trained model.
    """
    # Ensure that the directory exists, create it if it doesn't
    os.makedirs(save_path, exist_ok=True)

    pbar = st.progress(0.0, text="Initializing model...")

    # Like in get_pretrained_model above, we only want to import this when we need it
    from bertopic import BERTopic

    # Initialize the BERTopic model
    model = BERTopic(verbose=True)

    # Choose embedding model
    embed_model_path = "sentence-transformers/all-MiniLM-L6-v2"
    embedder = SentenceTransformer(embed_model_path)

    # Pre-calculate embeddings for the sole purpose of getting a progress bar
    # (letting model.fit() handle this step = no progress bar)
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

    # Train the model with the pre-calculated embeddings
    pbar.progress(0.8, text="Training model...")
    model.fit([doc.content for doc in docs], embeddings=embeddings)

    # Save the model
    pbar.progress(0.9, text="Saving model...")
    model.save(
        save_path,
        serialization="safetensors",
        save_embedding_model=embed_model_path,
        save_ctfidf=True,
    )

    pbar.progress(1.0, text="Training complete.")
