import torch
from langchain import LlamaCpp, PromptTemplate
from langchain.chains import RetrievalQA
from langchain.embeddings import HuggingFaceInstructEmbeddings
from langchain.memory import ConversationBufferMemory
from langchain.vectorstores import Chroma
from langchain.vectorstores.base import VectorStoreRetriever
from prefect import task, flow

from repository.documents import Documents
from repository.user_document import UserDocument
from util.file_util import get_file_path_by_key
from util.path_util import embeddingdb_path, bucket
from util.utils import object_to_dict
from workflow import model_util

device_type = 'cuda' if torch.cuda.is_available() else 'cpu'


@task
def is_document_already_summary(hash_name: str, user_id: str) -> bool:
    document = object_to_dict(Documents(hash_name=hash_name).entity.get())
    user_document = object_to_dict(UserDocument(hash_name=hash_name, user_id=user_id).entity.get())
    if document.get('summary') is not None:
        # check field summary in user_document
        if user_document.get('summary') is None:
            UserDocument(hash_name=hash_name, user_id=user_id).update_summary(document.get('summary'))
        return True
    return False


@task
def create_lager_language_model() -> LlamaCpp:
    # return model_util.create_llama_model()
    return model_util.create_llama_model()


@task
def create_retriever(hash_name: str) -> VectorStoreRetriever:
    persist_directory = get_file_path_by_key(bucket=bucket(), file_key=f'{embeddingdb_path()}/{hash_name}')
    retriever = Chroma(
        persist_directory=persist_directory,
        embedding_function=HuggingFaceInstructEmbeddings(
            model_name="hkunlp/instructor-large",
            model_kwargs={"device": device_type},
        ),
    ).as_retriever()
    return retriever


@task
def create_prompt_template() -> PromptTemplate:
    # create prompt
    template = """Use the following pieces of context to answer the question at the end. If you don't know the answer,\
    just say that you don't know, don't try to make up an answer.

    {context}

    {history}
    Question: {question}
    Helpful Answer:"""

    return PromptTemplate(input_variables=["history", "context", "question"], template=template)


@task
def create_retriever_qa(llm: LlamaCpp, retriever: Chroma, prompt: PromptTemplate) -> RetrievalQA:
    # create memory
    memory = ConversationBufferMemory(input_key="question", memory_key="history")

    # create retriever question answer
    return RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        return_source_documents=True,
        chain_type_kwargs={"prompt": prompt, "memory": memory},
    )


@task
def query_document(retrieval_qa: RetrievalQA, query: str):
    return retrieval_qa(query)


@task
def update_summary_document(hash_name: str, user_id: str, result: dict):
    summary = result.get("result")
    UserDocument(user_id=user_id, hash_name=hash_name).update_summary(summary=summary)
    Documents(hash_name=hash_name).update_summary(summary=summary)


@flow
def summary_document_flow(hash_name: str, user_id: str):
    if is_document_already_summary(hash_name=hash_name, user_id=user_id):
        return
    llm = create_lager_language_model.submit()
    retriever = create_retriever.submit(hash_name=hash_name)
    prompt = create_prompt_template.submit()
    retrieval_qa = create_retriever_qa.submit(llm=llm, retriever=retriever, prompt=prompt)
    result = query_document.submit(retrieval_qa=retrieval_qa,
                                   query='Please summarize the content of this document for better understanding. Please focus about the answer.')
    update_summary_document.submit(hash_name=hash_name, user_id=user_id, result=result)
