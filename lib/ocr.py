import asyncio
import os
import openai
from typing import Awaitable, Callable, TypeVar
from openai import AsyncOpenAI, OpenAIError

T = TypeVar("T")


class OCR():
    GPT_MODEL = "gpt-4o"

    def __init__(self):
        openai.api_key = os.environ["OPENAI_API_KEY"]

    def build_message(self, base64_encoded_img: str) -> list[dict[str, str]]:
        messages = [
            {
                "role": "system",
                "content": "あなたは高性能なOCRです"
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "提供された画像からテキストを抽出してください。"
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": base64_encoded_img
                        }
                    }
                ]
            }
        ]
        return messages

    def get_text(self, base64_encoded_img: str, max_tokens: int = 300) -> str:
        response = openai.chat.completions.create(
            model=self.GPT_MODEL,
            messages=self.build_message(base64_encoded_img),
            max_tokens=max_tokens
        )
        return response.choices[0].message.content

    def get_texts(self, base64_encoded_img_list: list[str],
                  max_tokens: int = 300) -> list[str]:
        answers = self.batch_run_chatgpt(base64_encoded_img_list,
                                         max_tokens=max_tokens)
        return answers

    async def retry_on_error(self,
                             openai_call: Callable[[], Awaitable[T]],
                             max_num_trials: int = 5,
                             first_wait_time: int = 10,
                             ) -> Awaitable[T]:
        """OpenAI API使用時にエラーが返ってきた場合に再試行する"""
        for i in range(max_num_trials):
            try:
                # 関数を実行する
                return await openai_call()
            except OpenAIError as e:
                # 試行回数が上限に達したらエラーを送出
                if i == max_num_trials - 1:
                    raise
                print(f"エラーを受け取りました：{e}")
                wait_time_seconds = first_wait_time * (2**i)
                print(f"{wait_time_seconds}秒待機します")
                await asyncio.sleep(wait_time_seconds)

    async def _async_batch_run_chatgpt(
        self,
        messages_list: list[list[dict[str, str]]],
        max_tokens: int | None,
    ) -> list[str]:
        """OpenAI APIに並列してリクエストを送る"""
        # コルーチンオブジェクトをtasksに格納
        client = AsyncOpenAI()
        tasks = [
            self.retry_on_error(
                # ラムダ式で無名関数を定義して渡し、
                # retry_on_error関数の内部で呼び出させる
                openai_call=lambda x=ms: client.chat.completions.create(
                    model=self.GPT_MODEL,
                    messages=x,
                    max_tokens=max_tokens,
                )
            )
            for ms in messages_list
        ]
        # tasks内の非同期処理を実行し結果を収集
        completions = await asyncio.gather(*tasks)
        return [
            c.choices[0].message.content for c in completions
        ]

    def batch_run_chatgpt(self,
                          base64_encoded_img_list: list[str],
                          max_tokens: int | None = None,
                          ) -> list[str]:
        """非同期処理関数を実行するためのラッパー"""
        messages_list = [self.build_message(img) for img in base64_encoded_img_list]
        return asyncio.run(
            self._async_batch_run_chatgpt(
                messages_list, max_tokens,
            )
        )
