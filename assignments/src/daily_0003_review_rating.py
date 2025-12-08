import os
import subprocess

import MeCab  # type: ignore
import numpy as np
import pandas as pd


def create_review_dataset():
    reviews = [
        "配送が早くて助かった",
        "思ったより品質がよい",
        "サイズが大きすぎた",
        "色味が写真と違う",
        "触り心地がとても良い",
        "電池の持ちが悪い",
        "梱包が丁寧だった",
        "耐久性が高そう",
        "到着が遅れて残念",
        "デザインが気に入った",
        "操作が簡単で使いやすい",
        "重くて扱いにくい",
        "コスパが最高",
        "初期不良があった",
        "香りがとても良い",
        "生地が薄く感じた",
        "期待以上だった",
        "音が大きすぎる",
        "素材がしっかりしている",
        "説明書がわかりにくい",
    ]
    size = len(reviews)
    ratings = np.random.randint(1, 5, size)
    ids = [id_ for id_ in range(1, size + 1)]
    return pd.DataFrame({"id": ids, "review": reviews, "rating": ratings})


def add_posi_nega_col(df: pd.DataFrame) -> pd.DataFrame:
    df["eval"] = ["positive" if rate >= 4 else "negative" for rate in df["rating"]]
    return df


def tokenize(texts: list) -> list:
    # MeCabの設定ファイルと辞書のパスを取得
    try:
        result = subprocess.run(
            ["brew", "--prefix", "mecab"], capture_output=True, text=True, check=True
        )
        mecab_prefix = result.stdout.strip()
        mecabrc_path = f"{mecab_prefix}/etc/mecabrc"
        dic_path = f"{mecab_prefix}/lib/mecab/dic/ipadic"

        # 設定ファイルと辞書の存在確認
        if os.path.exists(mecabrc_path) and os.path.exists(dic_path):
            # 設定ファイルと辞書の両方を指定
            tagger = MeCab.Tagger(f"-r {mecabrc_path} -d {dic_path}")
        elif os.path.exists(dic_path):
            # 辞書だけ存在する場合（設定ファイルは辞書内のmecabrcを使用）
            tagger = MeCab.Tagger(f"-d {dic_path}")
        else:
            raise FileNotFoundError("MeCab dictionary not found")
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        # brewが見つからない場合やエラーが発生した場合はデフォルト
        print(f"Warning: {e}, using default MeCab configuration")
        tagger = MeCab.Tagger()

    all_words = []
    for text in texts:
        node = tagger.parseToNode(str(text))
        words = []
        while node:
            if node.surface:  # 空文字列でない場合
                words.append(node.surface)
            node = node.next
        all_words.append(words)
    return all_words


def add_count_word_vector(df: pd.DataFrame) -> pd.DataFrame:
    reviews_tokens = tokenize(list(df["review"]))
    counts = []
    for token in reviews_tokens:
        counts.append(len(token))
    df["count"] = counts
    return df


def main():
    df = create_review_dataset()
    df = add_posi_nega_col(df)
    df = add_count_word_vector(df)
    return df


if __name__ == "__main__":
    print(main())
