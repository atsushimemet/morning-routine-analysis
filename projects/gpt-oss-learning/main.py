import sys
import time

import requests
from openai import OpenAI


def wait_for_ollama():
    """Ollamaサーバーが準備できるまで待機"""
    max_retries = 30
    retry_interval = 2

    for i in range(max_retries):
        try:
            # Dockerコンテナ内ではサービス名を使用
            response = requests.get("http://ollama:11434/api/tags", timeout=5)
            if response.status_code == 200:
                print("Ollamaサーバーが準備できました")
                return True
        except requests.exceptions.RequestException:
            pass

        print(f"Ollamaサーバーの準備を待機中... ({i+1}/{max_retries})")
        time.sleep(retry_interval)

    print("Ollamaサーバーの準備がタイムアウトしました")
    return False


def main():
    print("アプリケーションを開始します...")

    # コマンドライン引数からプロンプトを取得
    if len(sys.argv) > 1:
        user_prompt = " ".join(sys.argv[1:])
        print(f"ユーザープロンプト: {user_prompt}")
    else:
        user_prompt = "こんにちは！簡単な挨拶をしてください。"
        print("デフォルトプロンプトを使用します")

    # Ollamaサーバーの準備を待機
    if not wait_for_ollama():
        print("Ollamaサーバーに接続できませんでした")
        return

    print("OpenAIクライアントを初期化中...")
    client = OpenAI(
        base_url="http://ollama:11434/v1",  # Dockerコンテナ内ではサービス名を使用
        api_key="ollama",  # Dummy key
    )

    print("LLMリクエストを送信中...")
    try:
        response = client.chat.completions.create(
            model="phi4-mini",  # Phi4-miniモデルを使用
            messages=[
                {"role": "user", "content": user_prompt}
            ],
            max_tokens=100,
            temperature=0.7,
        )
        print("レスポンスを受信しました:")
        print(response.choices[0].message.content)
    except Exception as e:
        print(f"エラーが発生しました: {e}")
        print("モデルがダウンロードされていない可能性があります。")
        print("以下のコマンドでモデルをダウンロードしてください:")
        print("docker exec -it ollama ollama pull phi4-mini")

    print("アプリケーションを終了します。")


if __name__ == "__main__":
    main()
