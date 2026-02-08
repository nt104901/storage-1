import re
import sys
from googletrans import Translator

translator = Translator()

CODE_BLOCK = re.compile(r"```.*?```", re.DOTALL)
INLINE_CODE = re.compile(r"`[^`]+`")

def translate_md(text, src="auto", dest="en"):
    blocks = []

    def save_block(match):
        blocks.append(match.group(0))
        return f"__BLOCK_{len(blocks)-1}__"

    text = CODE_BLOCK.sub(save_block, text)
    text = INLINE_CODE.sub(save_block, text)

    translated = translator.translate(text, src=src, dest=dest).text

    for i, block in enumerate(blocks):
        translated = translated.replace(f"__BLOCK_{i}__", block)

    return translated

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Использование: python md_translate.py input.md output.md en")
        sys.exit(1)

    inp, out, lang = sys.argv[1:]

    with open(inp, "r", encoding="utf-8") as f:
        content = f.read()

    result = translate_md(content, dest=lang)

    with open(out, "w", encoding="utf-8") as f:
        f.write(result)

    print("Готово.")
