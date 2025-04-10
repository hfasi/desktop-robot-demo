import json
import json5
import utils, player, recorder

def handle_event_result(event):
    info_str = event.getInfo().encode("utf-8")
    print(f"handle_event_result: {info_str}")
    info_is_json = is_valid_json(info_str)
    if not info_is_json:
        print("not json string info: ")
        return
    
    info = json5.loads(info_str)
    datas = info["data"]
    data0 = datas[0]
    param = data0["params"]
    contents = data0["content"]
    content0 = contents[0]

    sub = param["sub"]

    data_bundle = event.getData()
    cnt_id = content0["cnt_id"]
    dts = content0.get("dts", 1)
    
    if sub == "nlp":
        handle_sub_nlp(data_bundle, cnt_id)
    elif sub == "tts":
        handle_sub_tts(data_bundle, content0, cnt_id, dts)
    else:
        handle_sub_other(data_bundle, cnt_id, sub, event)
    
    
def handle_sub_nlp(data_bundle, cnt_id):
    print("handle_sub_nlp")
    result_str = data_bundle.getBinaryAsStr(cnt_id)
    is_json = is_valid_json(result_str)
    if is_json:
        result_json = json5.loads(result_str)
        if 'rc' in result_json['intent']:
            print('nlp: {0}'.format(result_json['intent']['text']))
            result_str = data_bundle.getBinaryAsStr(cnt_id)
            if 'answer' in result_json['intent']:
                print('result_str with answer: {0}'.format(result_json['intent']['answer']['text']))
            else:
                print('result_str no answer: {0}'.format(result_str))
    else:
        print('not json string result: {0}'.format(result_str))
    
    
def handle_sub_tts(data_bundle, content0, cnt_id, dts):
    if "url" in content0 and content0['url'] == "1":
        resultStr = data_bundle.getBinaryAsStr(cnt_id)
        play_with_url(resultStr)
        print('resultStr: {0}'.format(resultStr))
    else:
        buffer = data_bundle.getBinary(cnt_id)
        sessionid = data_bundle.getString("sid", "tts")
        with open(sessionid + ".pcm", 'ab+') as tts:
            tts.write(buffer)
        
        if dts == 2:
            play_with_pcm(sessionid + ".pcm")
            print('-----------------tts pcm')
        

def handle_sub_other(data_bundle, cnt_id, sub, event):
    resultStr = data_bundle.getBinaryAsStr(cnt_id)
    print('{0}: {1}\nresultStr: {2}'.format(sub, event.getInfo(), resultStr))

    
def play_with_pcm(pcm_path):
    print("play pcm: " + pcm_path + "\n")
    player_ = player.SoxPlayer()
    wav_path = utils.get_wav_from_pcm(pcm_path)
    print("wav_path: " + wav_path + "\n")
    player_.play(wav_path)
    
    
def play_with_url(url):
    print("play url: " + url)
    if not url.endswith("mp3"):
        url += "3"
    player_ = player.SoxPlayer()
    player_.play(url)    

    
def is_valid_json(data):
    try:
        json.loads(data)
        return True
    except ValueError:
        return False