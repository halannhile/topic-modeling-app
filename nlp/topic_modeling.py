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


def train_model(docs: list[UploadedDocument], save_path: str) -> None:
    pbar = st.progress(0.0, text="Initializing model...")

    from bertopic import BERTopic

    model = BERTopic(verbose=True)
    # TODO support other embedding models
    embed_model_path = "sentence-transformers/all-MiniLM-L6-v2"
    embedder = SentenceTransformer(embed_model_path)

    # embeddings = embedder.encode([doc.content for doc in docs])
    # do this in batches instead:
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
    model.fit([doc.content for doc in docs], embeddings=embeddings)  # type: ignore

    pbar.progress(0.9, text="Saving model...")
    model.save(
        save_path,
        serialization="safetensors",
        save_ctfidf=True,
        save_embedding_model=embed_model_path,
    )
    pbar.progress(1.0, text="Training complete.")
