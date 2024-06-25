import pandas as pd
from langchain_core.documents import Document


class ExcelLoader():
    def __init__(self, path):
        self.path = path

    def load(self):

        # 使用pandas读取excel文件
        df = pd.read_excel(self.path)

        # 初始化一个空列表来存储结果
        result = []

        # 遍历每一行
        for index, row in df.iterrows():
            # 初始化一个空字符串来存储这一行的结果
            row_result = ''

            # 遍历这一行的每一列
            for col_name, col_value in row.items():  # Change here
                # 将列名和列值拼接成一个字符串，然后添加到结果中
                row_result += f'{col_name}: {col_value}  '

            # 将这一行的结果添加到总结果中
            result.append(Document(row_result.strip(), metadata={"format": "table"}))

        # 返回结果
        return result
