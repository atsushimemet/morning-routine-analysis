import MeCab  # type: ignore

tagger = MeCab.Tagger()
text = "今日は暑いですね"
node = tagger.parseToNode(text)
words = []
while node:
    if node.surface != "":
        words.append(node.surface)
    node = node.next
print(words)
