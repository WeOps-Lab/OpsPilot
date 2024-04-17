import logging

from utils.markdown_utils import MarkdownUtils


def test_convert_multiline_code_to_single_line():
    content = '''
    ```python
    print("Hello, World!")
    ```
    上述代码的执行结果是
    
    ```
    Hello, World!
    ```
    
    '''
    results = MarkdownUtils.convert_multiline_code_to_single_line(content)
    logging.info(results)
