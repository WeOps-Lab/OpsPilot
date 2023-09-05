import os
import re
import requests
from langchain import LLMChain, PromptTemplate
from langchain.chat_models import ChatOpenAI
from actions.utils.enterprise_wechat_utils import async_fun
from actions.utils.redis_utils import redis_client
from actions.constant.server_settings import server_settings
from channels.blueking_job_api_docs import *
from channels.enterprise_wechat_app import qywx_app
from dotenv import load_dotenv


load_dotenv()


def llm_chain_list_api(query, api_desc):
    # 一、意图识别选择对应接口
    template = """
    You are a professional back-end programmer, you will receive the user's query,
    and select the 5 interface that best matches the user's intention from the existing interfaces and their descriptions docs.
    Output in the form of  "serial number.<interface name: original description information>". Please do not output redundant information.
    query:{query}
    docs:{api_desc}
    """

    PROMPT = PromptTemplate(input_variables=["query", "api_desc"], template=template)
    llm_chain = LLMChain(llm=llm, prompt=PROMPT, verbose=True)
    res = llm_chain.run({"query": query, "api_desc": api_desc})
    return res


def llm_chain_retrieve_api(query, api_doc):
    # 二、拼接url和params（如果是post请求）
    template = """
    You are a professional Django engineer.
    You need to output the request method of the interface and request parameters in the form of a dictionary through user query and API documents.
    query:{query}
    API documents:{api_doc}
    For parameters, only select required parameters and parameters required by the user. If there is a default value, use the default value. Must be in dictionary format. If the required parameter is still missing, must fill it in with <parameter_name>
    Output in the form of "<request_url> <request_method> <request_parameters>",must separated by spaces. Please do not output redundant information.
    """

    PROMPT = PromptTemplate(input_variables=["query", "api_doc"], template=template)
    llm_chain = LLMChain(llm=llm, prompt=PROMPT, verbose=True)
    res = llm_chain.run({"query": query, "api_doc": api_doc})
    return res


def llm_chain_full_params(api_doc, full_params, lack_params, answer):
    template = """
    You are a professional django engineer, and you have a request parameter with a missing parameter value,
    and you need to complete the corresponding parameter through the user's answer.
    Please output the completed parameters.
    API documents:{api_doc}
    Parameters to be completed:{full_params}
    The parameters that need to be completed are:{lack_params}
    User's answer:{answer}

    Output in the form of "<request parameters>" dictionary. Please do not output redundant information.
    """

    PROMPT = PromptTemplate(
        input_variables=["api_doc", "full_params", "lack_params", "answer"],
        template=template,
    )
    llm_chain = LLMChain(llm=llm, prompt=PROMPT, verbose=True)
    res = llm_chain.run(
        {
            "api_doc": api_doc,
            "full_params": full_params,
            "lack_params": lack_params,
            "answer": answer,
        }
    )
    return res


def request_api(request_method, request_url, params, no_proxy_domain="paas.cwbk.com"):
    # 三、发送请求，获得response
    os.environ["NO_PROXY"] = no_proxy_domain
    request_params = {
        "method": request_method,
        "url": request_url,
        "json": params,
        "verify": False,
    }
    if request_method == "get":
        request_params["params"] = request_params.pop("json")
    res = requests.request(**request_params).json()
    return res


def llm_chain_response(api_doc, response):
    # 四、通过LLM按用户要求回复
    template = """
    You are a professional Django engineer. Now you have received a response through the user's query request interface. 
    Explain the return information to the user in conjunction with the API documentation in Chinese.
    API documents:{api_doc}
    response: {response}
    Please do not output redundant information.
    """

    PROMPT = PromptTemplate(
        input_variables=["api_doc", "response"],
        template=template,
    )
    llm_chain = LLMChain(llm=llm, prompt=PROMPT, verbose=True)
    res = llm_chain.run(
        {
            "api_doc": api_doc,
            "response": response,
        }
    )
    return res


def llm_chain_judge_intent(query):
    # 通过用户语句和上下文判断用户语句
    template = """
    You are a professional Django engineer. 
    Chat example:
    Step 1. The user: asks questions, such as "我需要查询某个执行方案的执行结果，用什么接口","我需要根据执行某个作业"
    Step 2. The backend: lists the five most likely interfaces to the user, such as "请选择要执行以下的第几个接口：1.get_job_plan_list	查询执行方案列表 2.get_job_plan_detail   查询执行方案详情3.get_job_instance_list	查询作业实例列表(执行历史)"
    Step 3. The user: selects the corresponding interface by replying to the serial number, such as 1 or "第二个"
    Step 4. The backend: receives the serial number and begins to piece together the request parameters of the corresponding interface. However, there may be incomplete situations and the user needs to be asked for completion. For example, it will ask: "接口调用参数不全，请输入以下参数的值：<bk_biz_id>"
    Step 5. The user: replies with the value corresponding to the parameter, such as "2" or "业务id为2" or "2,234560" etc.

    The above is a possible example. Now the user questions are given below. 
    user query: {query}
    output: <number>
    Please determine which step the user's query belongs to. Please must return one of steps 1, 3, and 5. Because the user’s steps can only be these few steps
    If you think the user's question deviates from this step, please return sequence number 0
    Please do not output redundant information.
    """

    PROMPT = PromptTemplate(
        input_variables=["query"],
        template=template,
    )
    llm_chain = LLMChain(llm=llm, prompt=PROMPT, verbose=True)
    res = llm_chain.run({"query": query})
    return res


def combine_params_request(query, user_id):
    full_params = redis_client.get("api_variable_" + user_id + "full_params")
    request_method = redis_client.get("api_variable_" + user_id + "request_method")
    request_url = redis_client.get("api_variable_" + user_id + "request_url")

    lack_params = redis_client.get("api_variable_" + user_id + "lack_params")
    api_doc = redis_client.get("api_variable_" + user_id + "api_doc")
    if lack_params:
        res3 = llm_chain_full_params(
            api_doc=api_doc,
            full_params=full_params,
            lack_params=lack_params,
            answer=query,
        )
        full_params = eval(res3)
    params = {
        "bk_app_code": os.getenv("bk_app_code"),
        "bk_username": os.getenv("bk_username"),
        "bk_app_secret": os.getenv("bk_app_secret"),
    }
    full_params = {**params, **eval(full_params)}
    res4 = request_api(request_method, request_url, full_params)
    # res5 = llm_chain_response(
    #     api_doc=api_doc,
    #     response=res4
    # )
    content = '接口返回值如下：\n'
    qywx_app.post_msg(user_id=user_id, content=content+str(res4))
    redis_client.delete(*redis_client.keys(pattern="api_variable_" + user_id + "*"))
    redis_client.delete("api_history" + user_id)
    # redis_client.flushall()

@async_fun
def job_api_query(query, user_id):
    redis_client.rpush("api_history" + user_id, "user:" + query + "\n")

    chat_history = ""
    for i in range(redis_client.llen("api_history" + user_id)):
        chat_history += redis_client.lindex("api_history" + user_id, i)
    redis_client.expire("km_" + user_id, 300)

    res0 = (
        int(
            re.findall(
                r"\d", llm_chain_judge_intent(query=query)
            )[0]
        )
        + 1
    )
    if res0 == 1:
        # fallback
        qywx_app.post_msg(user_id=user_id, content="无法识别您的接口调用意图，如想询问通用类问题请走gpt通道")
        redis_client.delete(*redis_client.keys(pattern="api_variable_" + user_id + "*"))
        redis_client.delete("api_history" + user_id)
    elif res0 == 2:
        # 根据问题列出api列表供用户选择
        res1 = llm_chain_list_api(query=chat_history.split("\n")[0].replace("user:", ""), api_desc=job_api_desc)
        content = "请选择要执行以下的第几个接口：\n"
        qywx_app.post_msg(user_id=user_id, content=content + res1)
        redis_client.rpush("api_history" + user_id, "backend:" + res1 + "\n")

        res_dict = dict(
            zip(re.findall(r"\d+", res1), re.findall(r"\d\.\s*([a-z_]+):", res1))
        )
        redis_client.set("api_variable_" + user_id + "res_dict", str(res_dict), ex=300)

    elif res0 == 4:
        # 根据序号确定接口
        num = re.findall(r"\d", query)
        if num:
            num = num[0]
        else:
            num_map = {
                "一": "1",
                "二": "2",
                "三": "3",
                "四": "4",
                "五": "5",
                "六": "6",
                "七": "7",
                "八": "8",
                "九": "9",
            }
            num = num_map[re.findall(r"[一二三四五六七八九十]", query)[0]]
        res_dict = eval(redis_client.get("api_variable_" + user_id + "res_dict"))
        api_doc = eval(res_dict[num])
        redis_client.set("api_variable_" + user_id + "api_doc", api_doc, ex=300)
        res2 = llm_chain_retrieve_api(
            query=chat_history.split("\n")[0].replace("user:", ""),
            api_doc=api_doc,
        )
        request_method = re.findall(r"get|post", res2.lower())[0]
        redis_client.set(
            "api_variable_" + user_id + "request_method", request_method, ex=300
        )
        request_url = res2.split(" ")[0]
        redis_client.set("api_variable_" + user_id + "request_url", request_url, ex=300)

        full_params = re.findall(r"\{.*\}", res2)[0]
        redis_client.set("api_variable_" + user_id + "full_params", full_params, ex=300)

        # 缺失必填参数，询问并补全
        if len(re.findall(r"<.*?>", res2)) != 0:
            lack_params = re.findall(r"<.*?>", res2)
            redis_client.set(
                "api_variable_" + user_id + "lack_params", str(lack_params), ex=300
            )
            content = "接口调用参数不全，请补充以下参数的值：" + ",".join(lack_params)
            qywx_app.post_msg(user_id=user_id, content=content)
            redis_client.rpush("api_history" + user_id, "backend:" + content + "\n")
        else:
            combine_params_request(query=query,user_id=user_id)
    elif res0 == 6:
        combine_params_request(query=query,user_id=user_id)


llm = ChatOpenAI(
    openai_api_key=server_settings.openai_key,
    openai_api_base=server_settings.openai_endpoint,
    temperature=server_settings.openai_api_temperature,
)