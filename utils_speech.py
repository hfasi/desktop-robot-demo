import base64
import urllib
import requests
import json
import os
from aip import AipSpeech
from playsound import playsound

APP_ID = "90187894"
API_KEY = "XuHTHjw7kjbdF6X7vNCQRx9Q"
SECRET_KEY = "DHNVjoYmG1gFNYkFzAorO5rlsbeMQZUU"

audio_path = "output.wav"

def asr(path, success_callback, error_callback):
        
    url = "https://vop.baidu.com/pro_api"
    
    speech = get_file_content_as_base64(path, False)
    length = os.path.getsize(path)

    payload = json.dumps({
        "format": "wav",
        "rate": 16000,
        "channel": 1,
        "cuid": "BmPU297LXM6fDYZVizCaOyfQgjpd5ViQ",
        "token": get_access_token(),
        "dev_pid": 80001,
        "speech": speech,
        "len": length
    })
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    
    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.text)
    parsed_asr_result(response, success_callback, error_callback)
    
    
def parsed_asr_result(response, success_callback, error_callback):
    json_str = response.text
    try:
        data = json.loads(json_str)
        err_msg = data.get('err_msg')
        if "success" in err_msg:
            result = data.get('result')
            success_callback(result)
        else:
            err_no = data.get('err_no')
            error_callback(err_no)
    except json.JSONDecodeError as e:
        print(f"JSON解析错误： {e}")
        error_callback(e)
    

def get_file_content_as_base64(path, urlencoded=False):
    """
    获取文件base64编码
    :param path: 文件路径
    :param urlencoded: 是否对结果进行urlencoded 
    :return: base64编码信息
    """
    with open(path, "rb") as f:
        content = base64.b64encode(f.read()).decode("utf8")
        if urlencoded:
            content = urllib.parse.quote_plus(content)
    return content


def get_access_token():
    """
    使用 AK，SK 生成鉴权签名（Access Token）
    :return: access_token，或是None(如果错误)
    """
    url = "https://aip.baidubce.com/oauth/2.0/token"
    params = {"grant_type": "client_credentials", "client_id": API_KEY, "client_secret": SECRET_KEY}
    return str(requests.post(url, params=params).json().get("access_token"))


class TextToSpeech:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(TextToSpeech, cls).__new__(cls)
            cls._instance.client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)
        return cls._instance

    def tts(self, text, lang='zh', vol=5, output_file='output.mp3'):
        result = self.client.synthesis(text, lang, 1, {
            'vol': vol,
        })

        if not isinstance(result, dict):
            with open(output_file, 'wb') as f:
                f.write(result)
            # 播放语音文件
            playsound(output_file)
        else:
            print("Error in synthesis:", result)


# 全局实例
tts_instance = TextToSpeech()

def tts(text, lang='zh', vol=5, output_file='output.mp3'):
    tts_instance.tts(text, lang, vol, output_file)



if __name__ == '__main__':
    tts('不好意思，网络故障了！')
    
