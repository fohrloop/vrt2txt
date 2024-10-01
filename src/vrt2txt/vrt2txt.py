from __future__ import annotations

import html
import re
import typing

if typing.TYPE_CHECKING:
    from typing import Iterable, Sequence


PUNCT = "PUNCT"
NUM = "NUM"
WORD = "WORD"
PART_TYPES = {PUNCT, NUM, WORD}

NON_WORD_CONTENT_TYPES = {PUNCT, NUM}


def iter_vrt_xml(
    contents: str, sentence_tag="sentence", paragraph_tag="paragraph", paragraphs=False
) -> Iterable[str]:
    """Iterates over sentences in VRT XML. Sentences separated by spaces and
    paragraphs by newlines.

    Parameters
    ----------
    contents : str
        The VRT XML contents.
    sentence_tag : str, optional
        The tag for the sentence, by default "sentence". (Tells to look for
        <sentence>...</sentence> tags.)
    paragraph_tag : str, optional
        The tag for the paragraph, by default "paragraph". (Tells to look for
        <paragraph>...</paragraph> tags.). Paragraphs are assumed to contain
        sentences. See also: `paragraphs`.
    paragraphs : bool, optional
        If True, the contents are assumed to contain multiple paragraphs. If
        False, the contents are assumed to contain only sentences.

    Yields
    ------
    str
        The parsed sentence or paragraph. One sentence or separator (space or
        newline) at a time.
    """
    if paragraphs:
        re_iterator = re.finditer(
            rf"<{paragraph_tag}>(.*?)</{paragraph_tag}>",
            contents,
            flags=re.DOTALL,
        )
        paragraph_iterator = (match.groups()[0] for match in re_iterator)
    else:
        paragraph_iterator = iter((contents,))

    for paragraph_contents in paragraph_iterator:
        sentence_iterator = re.finditer(
            rf"<{sentence_tag}>(.*?)</{sentence_tag}>",
            paragraph_contents,
            flags=re.DOTALL,
        )
        sentence = next(sentence_iterator)
        sentence_data = sentence.groups()[0]
        yield parse_vrt_sentence(sentence_data)

        for sentence in sentence_iterator:
            # If more than one sentence, they are separated by a space
            yield " "
            sentence_data = sentence.groups()[0]
            yield parse_vrt_sentence(sentence_data)
        yield "\n"


def get_contents_from_line(line: str) -> tuple[str, str]:
    try:
        _, content, _, content_type, _ = line.split("\t", maxsplit=4)
        if content_type not in NON_WORD_CONTENT_TYPES:
            content_type = WORD
        # Change &amp; to & and other HTML entities to their original form
        # This is required as explained at: https://www.kielipankki.fi/support/vrt-format/
        content = html.unescape(content)
    except ValueError as err:
        raise ValueError(f'Could not parse line "{line}"') from err
    return content, content_type


def parse_vrt_sentence(vrt_string: str):
    """Parses the sentence from a VRT input.

    Parameters
    ----------
    vrt_string : str
        The VRT input.

    Returns
    -------
    str
        The parsed sentence.

    Examples
    --------
    >>> parse_vrt_sentence('''
    1	Helppoa	helppo	ADJ	_	Case=Par|Degree=Pos|Number=Sing	0	root	_	_
    2	!	!	PUNCT	_	_	1	punct	_	_'''
    )
    'Helppoa!'
    """
    sentence_parts = []
    sentence_part_types = []

    for line in vrt_string.splitlines():
        if not line.strip():
            continue
        content, content_type = get_contents_from_line(line)
        sentence_parts.append(content)
        sentence_part_types.append(content_type)

    return _form_sentence(sentence_parts, sentence_part_types)


def _form_sentence(
    sentence_parts: Sequence[str], sentence_part_types: Sequence[str]
) -> str:

    return "".join(_iter_sentence_parts(sentence_parts, sentence_part_types))


def _iter_sentence_parts(
    sentence_parts: Sequence[str], sentence_part_types: Sequence[str]
) -> Iterable[str]:
    # Notes:
    # This would be probably easier to understand if rewritten as a class.
    # This does not handle all special cases. There are numerous different
    # quotation marks in the world which are not handled correctly. Urls are
    # not handled correctly either.
    previous_part = None
    previous_part_type = None
    before_previous_part_type = None

    space_before_part = False

    inside_double_quotes = False
    inside_single_quotes = False
    inside_curly_double_quotes = False

    for part, part_type in zip(
        sentence_parts,
        sentence_part_types,
    ):
        if part_type not in PART_TYPES:
            raise ValueError(f"Invalid part type: {part_type}")

        if previous_part:
            # By detault, assume that each part is separated with a space.
            space_before_part = True

        if previous_part in {"(", "/"}:
            # After opening parenthesis there is no space
            # After slash there is no space
            # Example: "km/h"
            space_before_part = False
        elif previous_part == '"' and inside_double_quotes:
            # Inside double quotes, no space
            # Example: 'Foo "bar" baz' (at 'b')
            space_before_part = False
        elif previous_part == "”" and inside_curly_double_quotes:
            # Inside double curly quotes, no space
            # Example: "Foo ”bar” baz" (at 'b')
            space_before_part = False
        elif previous_part == "'" and inside_single_quotes:
            # Inside single quotes, no space
            # Example: "Foo 'bar' baz" (at 'b')
            space_before_part = False

        # Note: sometimes quotation marks may be part of a WORD (and not as a
        # separate PUNCT). Therefore using syntax <<if '"' in part>>.
        if '"' in part:
            if inside_double_quotes:
                # When closing double quotes, there is no space
                # Example: 'foo "bar" baz' (at 'r')
                space_before_part = False
            inside_double_quotes = not inside_double_quotes
        elif "”" in part:
            if inside_curly_double_quotes:
                # When closing curly double quotes, there is no space
                # Example: 'foo ”bar” baz' (at 'r')
                space_before_part = False
            inside_curly_double_quotes = not inside_curly_double_quotes
        elif "'" in part:
            if inside_single_quotes:
                # When closing single quotes, there is no space
                # Example: "foo 'bar' baz" (at 'r')
                space_before_part = False
            inside_single_quotes = not inside_single_quotes
        elif part_type == PUNCT:
            if part in "(":
                # Before opening parenthesis there is a space
                # Example: "Foo (bar) baz"
                space_before_part = True
            else:
                # Otherwise before punctionation, no space
                # Example: "Foo!" (at '!')
                space_before_part = False

        if part_type == NUM:
            if previous_part_type == PUNCT and before_previous_part_type == NUM:
                # Example: "6,3"
                space_before_part = False

        if space_before_part:
            yield " "

        yield part

        before_previous_part_type = previous_part_type

        previous_part = part
        previous_part_type = part_type
