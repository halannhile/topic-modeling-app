import streamlit as st

# slow!!
from bertopic import BERTopic

from .utils import UploadedDocument


@st.cache_resource(show_spinner="Loading pretrained model...")
def get_pretrained_model(model_path: str = "MaartenGr/BERTopic_Wikipedia") -> BERTopic:
    print("loading...")
    model = BERTopic.load(model_path)
    print("done!")
    return model


def transform_doc_pretrained(
    doc: UploadedDocument,
) -> tuple[int, float, str]:
    pretrained_model = get_pretrained_model()
    topic, prob = pretrained_model.transform(doc.content)
    return topic[0], prob.item(), pretrained_model.topic_labels_[topic[0]]  # type: ignore
