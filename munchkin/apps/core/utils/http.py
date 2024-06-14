import json
import traceback

import requests
from django.utils.translation import gettext_lazy as _
from loguru import logger


def send(url, params, method="GET", timeout=None, **kwargs):
    """
    统一请求处理，定制化参数， GET 参数使用 form-data，POST 参数使用 json 字符串，返回内容
    要求为 JSON 格式

    @exception
        ApiResultError：非 JSON 返回，抛出 ApiResultError
        ApiNetworkError： 请求服务端超时

    @param url：string，请求 URL
    @param method：string，请求方法，目前仅支持 GET、POST
    @param params：dict，请求参数 KV 结构
    @param timeout: float，服务器在 timeout 秒内没有应答，将会引发一个异常
    """
    session = requests.session()

    try:
        if method.upper() == "GET":
            response = session.request(method="GET", url=url, params=params, timeout=timeout, **kwargs)
        elif method.upper() == "POST":
            session.headers.update({"Content-Type": "application/json; chartset=utf-8"})
            response = session.request(method="POST", url=url, data=json.dumps(params), timeout=timeout, **kwargs)
        else:
            raise Exception(_("异常请求方式，%s") % method)
    except requests.exceptions.Timeout:
        err_msg = _("请求超时，url=%s，method=%s，params=%s，timeout=%s") % (
            url,
            method,
            params,
            timeout,
        )
        raise Exception(err_msg)

    logger.debug("请求记录, url={}, method={}, params={}, response={}".format(url, method, params, response))

    if response.status_code != requests.codes.ok:
        err_msg = _("返回异常状态码，status_code=%s，url=%s，method=%s，" "params=%s") % (
            response.status_code,
            url,
            method,
            json.dumps(params),
        )
        raise Exception(err_msg)

    try:
        return response.json()
    except Exception:  # pylint: disable=broad-except
        err_msg = _("返回内容不符合 JSON 格式，url=%s，method=%s，params=%s，error=%s，" "response=%s") % (
            url,
            method,
            json.dumps(params),
            traceback.format_exc(),
            response.text[:1000],
        )
        raise Exception(err_msg)
