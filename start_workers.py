from dotenv import load_dotenv

from util import FirebaseUtils
from worker.conversation_asking_worker import start_conversation_asking_worker
from worker.document_convert_worker import start_document_convert_worker
from worker.document_embed_worker import start_document_embed_worker

if __name__ == '__main__':
    load_dotenv()
    FirebaseUtils.firebase_initialize()
    # Start the workers
    start_conversation_asking_worker()
    start_document_convert_worker()
    start_document_embed_worker()
