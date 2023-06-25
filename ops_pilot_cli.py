import fire
from langchain.document_loaders import DirectoryLoader
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import MarkdownTextSplitter
from langchain.vectorstores import Chroma

from actions.utils.langchain_utils import langchain_qa


class BootStrap(object):
    def query_embed_knowledge(self, model_name: str = 'shibing624/text2vec-base-chinese',
                              cache_folder='cache/models', vec_db_path: str = 'vec_db'):
        """
        进入命令行模式进行本地知识问答
         Args:
            vec_db_path: 向量数据库存放的路径
            model_name: Embedding所使用的模型名称
            cache_folder: Embedding所使用模型缓存的路径
        """
        embeddings = HuggingFaceEmbeddings(model_name=model_name, cache_folder=cache_folder,
                                           encode_kwargs={
                                               'show_progress_bar': True
                                           })
        doc_search = Chroma(persist_directory=vec_db_path, embedding_function=embeddings)
        while True:
            query = input("请输入问题（输入exit退出终端）：")
            if query == "exit":
                break
            results = langchain_qa(doc_search, query)
            print(results)

    def embed_knowledge(self, knowledge_path: str, file_glob: str = '**/*.md',
                        vec_db_path: str = 'vec_db', model_name: str = 'shibing624/text2vec-base-chinese',
                        cache_folder='cache/models'):
        """
        索引目标路径下的文件，存放至Chroma的索引中
        Args:
            knowledge_path: 本地知识存放的绝对路径
            file_glob: 指定使用哪种glob查找knowledge_path目录下的本地知识
            vec_db_path: 向量数据库存放的路径
            model_name: Embedding所使用的模型名称
            cache_folder: Embedding所使用模型缓存的路径
        """
        loader = DirectoryLoader(knowledge_path, glob=file_glob, show_progress=True)
        documents = loader.load()

        text_splitter = MarkdownTextSplitter()
        split_docs = text_splitter.split_documents(documents)
        embeddings = HuggingFaceEmbeddings(model_name=model_name, cache_folder=cache_folder,
                                           encode_kwargs={
                                               'show_progress_bar': True
                                           })
        doc_search = Chroma.from_documents(split_docs, embeddings, persist_directory=vec_db_path)
        doc_search.persist()


if __name__ == '__main__':
    fire.Fire(BootStrap)
