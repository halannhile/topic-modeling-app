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