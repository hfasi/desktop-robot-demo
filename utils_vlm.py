# utils_llm.py
# 王海峰 2025-4-10
# 调用大语言模型API


from http import HTTPStatus
import dashscope
import json
import os
from langchain_community.llms.tongyi import Tongyi
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from dashscope import MultiModalConversation


QWEN_KEY = "sk-a0ee1bcd70cf40e8bb54fff3e10946b4"
LING_YI_KEY = "97d56101f8954771916d23bb0fe32c22"
LING_YI_URL = "https://api.lingyiwanwu.com/v1"
LING_YI_MODEL = "yi-spark"

os.environ["DASHSCOPE_API_KEY"] = QWEN_KEY

SYSTEM_PROMPT2 = '''
你是一个机械臂，你可以做抓取物体演示。
我即将说一句话，这句话有两种可能，可能是一句指令，也可能是正常聊天的内容。

当对话为指令时，给机械臂的指令，你帮我从这句话中提取出起始物体和终止物体，并输出json数据结构。

例如，如果我的指令是：请帮我把鸡蛋放到碗里。
你输出这样的格式：
{
 "start":"egg",
 "end":"bowl",
 "response": "好的，马上执行！"
}

如何在图片不存在我说的物体，请你回复我不存在。
例如：
如果图片中有碗，有柠檬，没有苹果，而我的指令是：请帮我把苹果放到碗里。
{
    "start":"",
    "end":"",
    "response": "不好意思，我这里没有苹果，但是有柠檬，你要不要试一下"
}

如果图片中有柠檬，没有框，而我的指令是：请帮我把柠檬放到框里。
{
    "start":"",
    "end":"",
    "response": "不好意思，我没有看到框，请换一个试试"
}


当对话为正常聊天内容时，你根据常识进行正常聊天，对我说话的内容进行分析和回复，并输出json数据结构。

例如，
如果我说话的内容是：你好啊。
你输出这样的格式：
{
 "start":"",
 "end":"",
 "response": "您好，请问有什么 需要帮助的吗"
}

如果我说话的内容是：你都能做什么。
你输出这样的格式：
{
 "start":"",
 "end":"",
 "response": "您好，我可以进行物体抓取演示"
}

如果图片中有可乐，我说话的内容是：我有点口渴了。
你输出这样的格式：
{
 "start":"cola",
 "end":"",
 "response": "那我帮您拿瓶可乐吧"
}

如果图片中有矿泉水，我说话的内容是：我有点口渴了，想喝点健康的。
你输出这样的格式：
{
 "start":"water",
 "end":"",
 "response": "那我帮您拿瓶水吧，水很健康。"
}

如果图片中没有矿泉水，我说话的内容是：帮我拿瓶水。
你输出这样的格式：
{
 "start":"",
 "end":"",
 "response": "不好意思，我这里没有水呢"
}

如果图片中有矿泉水，我说话的内容是：帮我拿瓶水。
你输出这样的格式：
{
 "start":"water",
 "end":"",
 "response": "好的，马上帮您拿水"
}

只回复json内容本身即可，不要回复其它内容，特别是你的回复中不要带json字样。

你需要特别注意的是，在你的回复中，'start'字段和'end'字段的内容，不能包含任何标点符号，而且一定要是英文。
还有一个千万千万要特别注意的是，'response'字段的汉字数一定不要超过60个汉字。

在你的回复中不要带有'图片中有...', 如果有需要说，请改为'我这里有...'。

我现在的说的话是：
'''

import openai
from openai import OpenAI
import base64

# 零一万物大模型开放平台
# https://platform.lingyiwanwu.com
LING_YI_KEY = "97d56101f8954771916d23bb0fe32c22"
LING_YI_BASE_URL = "https://api.lingyiwanwu.com/v1"
ling_yi_path = "egg_bowl.jpg"

def ling_yi_vlm(callback, prompt='请帮我把柠檬放到碗里', img_path=""):
    client = OpenAI(api_key=LING_YI_KEY, base_url=LING_YI_BASE_URL)
    
    # 编码为base64数据
    with open(img_path, 'rb') as image_file:
        image = 'data:image/jpeg;base64,' + base64.b64encode(image_file.read()).decode('utf-8')
        
    

    # 向大模型发起请求
    completion = client.chat.completions.create(
      model="yi-vision",
      messages=[
        {
          "role": "user",
          "content": [
            {
              "type": "text",
              "text": SYSTEM_PROMPT2 + prompt
            },
            {
              "type": "image_url",
              "image_url": {
                "url": image
              }
            }
          ]
        },
      ]
    )
    
    # 解析大模型返回结果
    result = completion.choices[0].message.content.strip()
    callback(result)
    print('ling yi success.')
    return result
     


def parse_response(result):
    try:
        parsed_data = json.loads(result)
        start = parsed_data["start"]
        end = parsed_data["end"]
        response = parsed_data["response"]
        print("start:", start)
        print("end:", end)
        print("response:", response)
    except ValueError as e:
        print(f"response: {result}")



def gpt_callback(result):
    print(f"gpt_callback: {result}")
    parse_response(result)
    



import datetime

if __name__ == '__main__':
    start_time = datetime.datetime.now()
    print("start time:", start_time)
    result = ling_yi_vlm(gpt_callback, "请你帮我把苹果拿到碗里", ling_yi_path)
    # result = ling_yi_vlm(gpt_callback, "请帮我拿瓶水", ling_yi_path)
    end_time = datetime.datetime.now()
    print("end time:", end_time)
    # print("result:", result)




        