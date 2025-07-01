from typing import List


from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS

class ProjectClassifier:
    """Classify tasks into projects using FAISS."""

    def __init__(self, project_texts: List[str], openai_api_key: str):
        embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)
        self.vstore = FAISS.from_texts(project_texts, embeddings)
        self.projects = project_texts

    def classify(self, text: str) -> str:
        doc = self.vstore.similarity_search(text, k=1)[0]
        return doc.page_content
