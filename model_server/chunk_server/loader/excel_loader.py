import pandas as pd
from langchain_core.documents import Document
from user_types.file_chunk_request import FileChunkRequest
from loguru import logger


class ExcelLoader():
    def __init__(self, path, request: FileChunkRequest):
        self.path = path
        self.request = request

    def dataframe_to_excel_format_string(self, df):
        # Remove rows and columns where all values are NaN
        df = df.dropna(how='all').dropna(axis=1, how='all')

        # Step 1: Initialize an empty string for the formatted content
        excel_format_str = ""

        # Step 2: Format and append column headers
        column_headers = "\t".join(df.columns)  # Using tab as a separator
        excel_format_str += column_headers + "\n"

        # Step 3 & 4: Iterate through rows and append their formatted string representation
        for index, row in df.iterrows():
            row_str = "\t".join(row.astype(str))  # Convert all cell values to string to avoid any conversion issues
            excel_format_str += row_str + "\n"

        excel_format_str = excel_format_str.replace('nan', '')
        # Step 5: Return the accumulated string
        return excel_format_str

    def load(self):
        # 使用pandas读取excel文件的所有sheet
        sheets = pd.read_excel(self.path, sheet_name=None)

        # 初始化一个空列表来存储结果
        result = []

        for sheet_name, df in sheets.items():
            if self.request.excel_header_row_parse:
                logger.info(f"Excel文件[{self.path}]的Sheet[{sheet_name}]的首行将被解析为表头")

                # 遍历每一行
                for index, row in df.iterrows():
                    # 初始化一个空字符串来存储这一行的结果
                    row_result = ''

                    # 遍历这一行的每一列
                    for col_name, col_value in row.items():
                        # 将列名和列值拼接成一个字符串，然后添加到结果中
                        row_result += f'{sheet_name}  {col_name}: {col_value}  '

                    # 将这一行的结果添加到总结果中
                    result.append(Document(row_result.strip(), metadata={"format": "table", "sheet": sheet_name}))

            if self.request.excel_full_content_parse:
                logger.info(f"Excel文件[{self.path}]的Sheet[{sheet_name}]的全内容将被解析")

                # 读取Excel 的全内容
                full_content = self.dataframe_to_excel_format_string(df)
                result.append(
                    Document(f'{sheet_name} {full_content}', metadata={"format": "table", "sheet": sheet_name}))

        # 返回结果
        return result
