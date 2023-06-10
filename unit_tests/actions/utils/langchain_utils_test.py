from actions.utils.langchain_utils import query_online, load_docsearch


def test_query_online():
    print(query_online('https://www.oschina.net/',
                       '扮演专业的人工智能开发工程师，选出你最感兴趣的新闻，按照感兴趣程度排序，并且描述为什么你对这个感兴趣'))


def test_langchain_qa():
    doc_search = load_docsearch()
