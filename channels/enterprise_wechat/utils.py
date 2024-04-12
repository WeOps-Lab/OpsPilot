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
        chunk = text_bytes[i:i + chunk_size].decode('utf-8', errors='ignore')
        chunks.append(chunk)
    return chunks
