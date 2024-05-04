import unittest
from database.operations import DatabaseOperations
from database.models import Document
from nlp.utils import UploadedDocument

# mock a DeltaGenerator for testing purposes
class MockDeltaGenerator:
    def progress(self, value):
        pass

# mock UploadedDocument class for testing purposes
class MockUploadedDocument:
    def __init__(self, filename, content):
        self.filename = filename
        self.content = content

class TestDatabaseOperations(unittest.TestCase):
    def setUp(self):
        # initialize db
        self.db = DatabaseOperations("sqlite:///:memory:")
        # sample data
        self.db.save_batch_to_db(
            [MockUploadedDocument("sample.txt", "Sample content")],
            upload_type="documents",
            topics="Sample topic",
            probabilities="0.5",
            model_names="Sample model",
            path_to_models="Sample path",
            prog_bar=MockDeltaGenerator(),  # Pass a mock progress bar
        )

    def test_save_document(self):
        # test saving a single document
        self.db.save_document("test.txt", 1, "documents")
        documents = self.db.get_documents()
        self.assertEqual(len(documents), 2)

    def test_save_batch_to_db(self):
        # test saving multiple documents
        self.db.save_batch_to_db(
            [MockUploadedDocument("test1.txt", "Test content 1"), MockUploadedDocument("test2.txt", "Test content 2")],
            upload_type="documents",
            topics="Test topic",
            probabilities="0.7",
            model_names="Test model",
            path_to_models="Test path",
            prog_bar=MockDeltaGenerator(),  # pass a mock progress bar
        )
        documents = self.db.get_documents()
        self.assertEqual(len(documents), 3)

    def test_get_documents(self):
        # test getting documents with batch number filter
        documents = self.db.get_documents(batch_number=1)
        self.assertEqual(len(documents), 1)

    def test_get_all_documents(self):
        # test getting all documents
        documents = self.db.get_all_documents()
        self.assertEqual(len(documents), 1)  # assuming there's one document initially

    def test_get_all_batches(self):
        # Test getting all batch numbers
        batch_numbers = self.db.get_all_batches()
        self.assertEqual(len(batch_numbers), 1)  # assuming there's one batch initially

    def test_clear_database(self):
        # test clearing the database
        self.db.clear_database()
        documents = self.db.get_documents()
        self.assertEqual(len(documents), 0)

    def test_delete_document(self):
        # test deleting a document
        documents_before = self.db.get_documents()
        document_id = documents_before[0].id
        self.db.delete_document(document_id)
        documents_after = self.db.get_documents()
        self.assertEqual(len(documents_after), len(documents_before) - 1)

    def delete_batch(self, batch_number):
        session = self.Session()
        try:
            # delete all documents with the specified batch number
            session.query(Document).filter_by(batch_number=batch_number).delete()
            session.commit()
            print(
                f"All documents with batch number {batch_number} deleted successfully."
            )
        except Exception as e:
            session.rollback()
            print(f"Error deleting documents with batch number {batch_number}: {e}")
        finally:
            session.close()


    def test_get_latest_batch_number(self):
        # test getting the latest batch number
        latest_batch_number = self.db.get_latest_batch_number()
        self.assertEqual(latest_batch_number, 1)  # assuming there's one batch initially

    def test_get_unique_values(self):
        # test getting unique values for a column
        unique_topics = self.db.get_unique_values("topics")
        self.assertEqual(unique_topics, ["Sample topic"])  # assuming there's one unique topic initially

if __name__ == "__main__":
    unittest.main()
