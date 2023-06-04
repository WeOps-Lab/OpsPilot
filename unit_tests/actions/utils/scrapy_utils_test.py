from actions.utils.azure_utils import query_chatgpt
from actions.utils.scrapy_utils import fetch_website


def test_fetch_website():
    print(fetch_website(url="https://www.oschina.net/news/industry",
                        title_path='//*[@id="newsList"]/div[1]/div/div/h3/div/text()'))


def test_fetch_website_with_gpt():
    result = fetch_website(url="https://www.oschina.net/news/industry",
                           title_path='//*[@id="newsList"]/div[1]/div/div/h3/div/text()')
    promt = '扮演专业的开发工程师，你现在正在阅读今天的头条信息，以下是你获取到的新闻标题:\n'
    for i in result:
        promt += f'标题:{i["title"]}\n'
    print("你需要基于上述的标题给今天的新闻评分，你对Python、大数据技术比较感兴趣，现在你的任务是：")

    print(query_chatgpt(promt, "总结一下今天开源软件的变化，你接下来应该关注哪些方向"))
