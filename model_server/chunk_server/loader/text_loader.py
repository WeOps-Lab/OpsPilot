from langchain_core.documents import Document


class TextLoader:
    def __init__(self, path):
        self.path = path

    def load(self):
        docs = []
        with open(self.path, 'r', encoding="utf-8") as f:
            full_text = f.read()
            docs.append(Document(full_text))
        return docs
