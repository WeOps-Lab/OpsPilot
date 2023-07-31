import os
import re
from dotenv import load_dotenv

load_dotenv()
WIKI_URL_FRONT = os.getenv("WIKI_URL_FRONT")


def get_source_doc(source, km):
    """通过docs的metadata找到文档对应的km wiki标题和链接
    results['source_documents'][0].metadata['source']
    Args:
        source (str): langchain_qa的回答的source，比如results['source_documents'][0].metadata['source']
        pkl_name (str, optional): km标题和链接的字典序列化文件. Defaults to "km.pkl".

    Returns:
        _type_: _description_
    """
    wiki_uuid = re.findall(r'([0-9a-z]+_[0-9a-z]+)\.',source)[0].replace("_", "/wiki/list/")
    wiki_url = WIKI_URL_FRONT + wiki_uuid

    title_list = list(km.keys())
    link_list = list(km.values())
    position = link_list.index(wiki_url)

    return title_list[position], wiki_url


def struct_qywx_answer(top_n, link_list, title_list):
    """通过km的标题和链接生成企微应用的回答（超链接）

    Args:
        top_n (_type_): 生成序号数
        link_list (_type_): 链接列表
        title_list (_type_): 标题列表

    Returns:
        _type_: 企微应用文本消息
    """
    answer = ""
    for i in range(1, top_n + 1):
        answer += '\n{0}. <a href="{1}">{2}</a>'.format(
            i, link_list[i - 1], title_list[i - 1]
        )
    return answer