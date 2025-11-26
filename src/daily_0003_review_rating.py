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


if __name__ == "__main__":
    print(create_review_dataset())
