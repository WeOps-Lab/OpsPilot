import re


class FormValidateUtils:
    @staticmethod
    def is_valid_url(url: str) -> bool:
        """
        判断字符串是否为有效的URL
        Args:
            url: 待验证的URL字符串
        Returns:
            如果URL有效则返回True，否则返回False
        """
        pattern = re.compile(r'^https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+')
        return bool(pattern.match(url))
