from openai import OpenAI
import os
import base64

from src.prompts import SYSTEM_PROMPT


#  base 64 编码格式
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def get_response(image_path):
    base64_image = encode_image(image_path)
    client = OpenAI(
        api_key="KEY",
        base_url="http://192.168.235.62:11434/v1",
    )
    response = client.chat.completions.create(
        model="qwen2.5vl:32b",
        messages=[
            {
              "role": "user",
              "content": [
                {
                  "type": "text",
                  "text": SYSTEM_PROMPT
                },
                {
                  "type": "image_url",
                  "image_url": {
                    "url": f"data:image/jpeg;base64,{base64_image}"
                  }
                }
              ]
            }
          ],
          stream=False,
          stream_options={"include_usage":True}
        )

    print(response.choices[0].message.content)

if __name__=='__main__':
    get_response("442_sharpened_.jpg")