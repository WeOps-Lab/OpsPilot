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
    wiki_uuid = re.findall(r"([0-9a-z]+_[0-9a-z]+)\.", source)[0].replace(
        "_", "/wiki/list/"
    )
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


def text_split(text, chunk_size):
    """该函数将文本分割成指定大小的块，并将它们存储在列表中，最后返回该列表

    Args:
        text (str): 要分割的文本
        chunk_size (int): 每个块的大小（以字节数为单位）

    Returns:
        list: 包含已经被分好块文本的列表
    """
    text_bytes = text.encode('utf-8')
    chunks = []
    for i in range(0, len(text_bytes), chunk_size):
        chunk = text_bytes[i:i+chunk_size].decode('utf-8', errors='ignore')
        chunks.append(chunk)
    return chunks


def helper_map_desc():
    """根据环境变量配置输出序号与对应helper的关系的文本
    """
    helper_info = list(filter(lambda x: "HELPER" in x[0], os.environ.items()))
    helper_text_info = '\n'.join([i[0].split('_')[-1]+'. 向'+i[0].split('_')[0]+'研发大佬求助' for i in helper_info])
    prefix_text = '对km答案不满意？可以输入序号（比如1）进入群聊获取研发大佬（helper）的帮助：\n'
    postfix_text = '\nPS.进入群聊30分钟后会被智慧狗自动踢出群聊哟'
    return prefix_text+helper_text_info+postfix_text