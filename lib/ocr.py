import os
import openai


class OCR():
    def __init__(self):
        openai.api_key = os.environ["OPENAI_API_KEY"]

    def get_text(self, base64_encoded_img: str):
        response = openai.chat.completions.create(
          model="gpt-4o",
          messages=[
            {
              "role": "system",
              "content": "あなたは高性能なOCRです"
            },
            {
              "role": "user",
              "content": [
                {"type": "text", "text": "提供された画像からテキストを抽出してください。"},
                {
                  "type": "image_url",
                  "image_url": {
                    "url": base64_encoded_img
                  }
                }
              ]
            }
          ],
          max_tokens=300
        )
        return response.choices[0].message.content
