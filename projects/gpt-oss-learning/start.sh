#!/bin/bash

# 引数をチェック
if [ $# -gt 0 ]; then
    USER_PROMPT="$*"
    echo "GPT-OSS Learning 環境を起動中（モデル: Phi4-mini）..."
    echo "プロンプト: $USER_PROMPT"
else
    echo "GPT-OSS Learning 環境を起動中（モデル: Phi4-mini）..."
    echo "デフォルトプロンプトを使用します"
fi

# コンテナをビルドして起動
docker compose up --build -d

echo "Ollamaサーバーの起動を待機中..."
sleep 10

# モデルが存在するかチェック
echo "Phi4-miniモデルの存在を確認中..."
if docker exec ollama ollama list | grep -q "phi4-mini"; then
    echo "Phi4-miniモデルは既にダウンロードされています"
else
    echo "Phi4-miniモデルをダウンロード中... (約2.7GB、時間がかかります)"
    docker exec ollama ollama pull phi4-mini
fi

echo "アプリケーションを起動中..."
if [ -n "$USER_PROMPT" ]; then
    # プロンプトが指定された場合、それを環境変数として設定してアプリケーションを実行
    docker compose run --rm -e USER_PROMPT="$USER_PROMPT" app python main.py "$USER_PROMPT"
else
    # プロンプトが指定されなかった場合、デフォルトで実行
    docker compose run --rm app python main.py
fi

echo "環境の準備が完了しました！"
echo "使用方法: ./start.sh \"あなたの質問やリクエスト\""

