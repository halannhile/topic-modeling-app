from bertopic import BERTopic
from numpy import ndarray

from nlp import UploadedDocument

# slow on first load
pretrained_model = BERTopic.load("MaartenGr/BERTopic_Wikipedia")
topic_labels = pretrained_model.generate_topic_labels()


def transform_doc_pretrained(
    doc: UploadedDocument,
) -> tuple[int, float, str]:
    topic, prob = pretrained_model.transform(doc.content)
    return topic[0], prob.item(), pretrained_model.topic_labels_[topic[0]]  # type: ignore
