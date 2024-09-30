# vrt2txt

Simple python package for converting [VRT format](https://www.kielipankki.fi/support/vrt-format/) (VeRticalized Text) aka. "verticalized XML" or IMS CWB format for the [The IMS Open Corpus Workbench](https://cwb.sourceforge.io/) used by the Language Bank of Finland ("Kielipankki") into plain text format.

## Installing

Once cloned,  install with 
```
python -m pip install -e <root>
```

where `<root>` is a path to the folder with `pyproject.toml`.

## Example usage

```python
from pathlib import Path

from vrt2txt import iter_vrt_xml

raw_folder_root = Path(__file__).parent / "raw"
extracted_text_folder = Path(__file__).parent / "extracted_text"


def process_folder(folder: Path, folder_out: Path, paragraphs=False):
    folder_out.mkdir(exist_ok=True, parents=True)
    for file in folder.glob("*.VRT"):
        print("Processing", file)
        outfile = folder_out / file.with_suffix(".txt").name
        with open(outfile, "w") as f:
            for text in iter_vrt_xml(contents=file.read_text(), paragraphs=paragraphs):
                f.write(text)


if __name__ == "__main__":

    process_folder(
        raw_folder_root / "wikipedia-fi-2017-src",
        folder_out=extracted_text_folder / "wikipedia",
        paragraphs=True,
    )
    process_folder(
        raw_folder_root / "opensub-fi-2017-src",
        folder_out=extracted_text_folder / "opensub",
        paragraphs=False,
    )
```

## About this package

I wrote this as part of my keyboard layout optimization project where I created a English+Finnish+Coding optimized layout called Granite. This package is alpha-level quality but is has some unit tests.

Some functionality is still missing. For example only few types of quotes are handled, urls are not handled correctly, and for example "km/h" is output as "km/ h". There are probably a lot more other edge cases that could be handled better, but this extracts sentences perfectly >99% of the cases, so it was good enough for me. I'm not currently planning on working on this package further. Feel free for fork and modify to your needs.

## Running tests

```
python -m pytest
```

## Where to download VRT data?

- You can download VRT data from: [kielipankki.fi/download/](https://www.kielipankki.fi/download/)