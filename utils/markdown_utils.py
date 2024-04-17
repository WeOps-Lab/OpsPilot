import re


class MarkdownUtils:
    @staticmethod
    def convert_multiline_code_to_single_line(reply_text):
        # 匹配Markdown中的多行代码块
        pattern = r'```([\s\S]*?)```'

        # 使用正则表达式找到所有的多行代码块
        multiline_code_blocks = re.findall(pattern, reply_text)

        for code_block in multiline_code_blocks:
            # 将多行代码块转换为单行
            single_line_code_block = code_block.replace('\n', ' ')

            # 在原始文本中替换多行代码块为单行代码块
            reply_text = reply_text.replace(code_block, single_line_code_block)

        return reply_text
