import re
import xml.etree.ElementTree as ET
from io import StringIO
from pathlib import Path

import pandas as pd

raw_folder_root = Path(__file__).parent / "raw"
corpus_folder = (Path(__file__).parent / "corpus").resolve()
corpus_folder.mkdir(exist_ok=True)


def get_contents_from_line(line: str):
    _, content, _, content_type, _ = line.split("\t", maxsplit=4)
    if not content_type == "PUNCT":
        # Insert space before every word
        yield " "
    yield content


def iter_sentence(contents: str):
    for line in contents.splitlines():
        if not line:
            continue
        yield from get_contents_from_line(line)


def process_file(contents: str):

    for sentence in re.finditer(
        r"<sentence>(.*?)</sentence>",
        contents,
        flags=re.DOTALL,
    ):
        sentence_data = sentence.groups()[0]
        yield from iter_sentence(sentence_data)


def process_folder(folder):
    for file in folder.glob("*.VRT"):
        print(file)
        yield from process_file(contents=file.read_text())
