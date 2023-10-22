import requests
import pandas as pd
import json

## GetPath
def GetGPTKeyPath():
    with open('GPT_API.txt', 'r', encoding='utf-8') as file:
        content = file.read()
    return content

## ChatGPT
def GetSentenceGPT(word):
    api_key = GetGPTKeyPath()
    main_content = '''"，在生活中或職場中，常見的不同種使用方式提供例句、繁體中文翻譯、使用方法。
    回傳的格式只需一個json格式，不要有其他文字內容，欄位名稱: Sentence,  Translation, Usage
    
    舉例來說，如果提供的單字是"interest"
    將回傳的Json內容如下:
    [
      {
        "Sentence": "I've always had an interest in astronomy.",
        "Translation": "我一直對天文學感興趣。",
        "Usage": "名詞，可數，表示對某事物的好奇、興趣，常與in搭配使用。"
      },
      {
        "Sentence": "When they divorced she retained a legal interest in the property.",
        "Translation": "他們離婚時，她保留了房屋的合法產權。",
        "Usage": "名詞，可數，表示股權、產權。"
      },
      {
        "Sentence": "Banks have increased their interest rates again.",
        "Translation": "銀行又提高了他們的利率。",
        "Usage": "名詞，不可數，表示利息，搭配 interest rates表示利率。"
      },
      {
        "Sentence": "Sport has never really interested me.",
        "Translation": "我從沒有對體育運動真正感興趣過。",
        "Usage": "動詞，使某人感興趣。"
      },
    ]
    如果提供的單字是"appeal"
    將回傳的Json內容如下:
    [
      {
        "Sentence": "They made an appeal for donations to help the victims.",
        "Translation": "他們呼籲捐款以幫助受害者。",
        "Usage": "名詞，可數，表示呼籲做某事，make an appeal for something。"
      },
      {
        "Sentence": "The new movie has a wide appeal to audiences of all ages.",
        "Translation": "新電影對各年齡層的觀眾都具有很大的吸引力。",
        "Usage": "名詞，可數，表示對…具有很大的吸引力，常搭配to + 人。"
      },
      {
        "Sentence": "He lost his appeal and will have to serve his full sentence.",
        "Translation": "他上訴失敗，將不得不服完整個刑期。",
        "Usage": "名詞，可數，表示申訴，可搭配lose & win表示輸贏申訴。"
      },
      {
        "Sentence": "The simplicity of the design appeals to me.",
        "Translation": "設計的簡單吸引了我。",
        "Usage": "動詞，表示吸引某人，常搭配to + 人。"
      },
      {
        "Sentence": "The organization appealed for donations to help the victims.",
        "Translation": "該組織呼籲捐款以幫助受害者。",
        "Usage": "動詞，呼籲某事，常搭配for something。"
      }
    ]
    
    特別注意: 同一詞性只要提供一個例句，除非用法與意思不同，例句的數量不需要剛好為四個或五個。
    '''
    prompt = '請假設自己是一個英文老師，請針對以下單字"' + word + main_content

    response = requests.post(
        'https://api.openai.com/v1/chat/completions',
        headers={
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {api_key}'
        },
        json={
            'model': 'gpt-3.5-turbo',  # 一定要用chat可以用的模型
            'messages': [{"role": "user", "content": prompt}]
        })

    Ans = response.json()
    content = Ans['choices'][0]['message']['content']
    content_data = json.loads(content)
    df = pd.DataFrame(content_data)
    return df

if __name__ == '__main__':
    word = 'associate'
    # GetSentenceGPT(word)
