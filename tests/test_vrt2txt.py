from itertools import zip_longest

import pytest

from src.vrt2txt.vrt2txt import _form_sentence, iter_vrt_xml, parse_vrt_sentence


@pytest.fixture
def vrt_two_files_two_sentences():
    return """
    <file id="123" year="1999" genre="Comedy,Romance" original="English" country="USA" duration= "NaN">
    <sentence>
    1	tarvitsen	tarvita	VERB	_	Mood=Ind|Number=Sing|Person=1|Tense=Pres|VerbForm=Fin|Voice=Act	0	root	_	_
    2	apua	apu	NOUN	_	Case=Par|Number=Sing	1	dobj	_	_
    3	.	.	PUNCT	_	_	1	punct	_	_
    </sentence>
    <sentence>
    1	mario	mario	NOUN	_	Case=Nom|Number=Sing	0	root	_	_
    2	,	,	PUNCT	_	_	1	punct	_	_
    3	iaske	iaske	NOUN	_	Case=Nom|Number=Sing	1	conj	_	_
    4	hänet	hän	PRON	_	Case=Acc|Number=Sing|Person=3|PronType=Prs	5	nmod:poss	_	_
    5	aias	aias	NOUN	_	Case=Nom|Number=Sing	3	nmod	_	_
    6	.	.	PUNCT	_	_	1	punct	_	_
    </sentence>
    </file>###C:<file id="20018" year="2001" genre="Comedy" original="English" country="USA, Canada" duration= "NaN">
    <sentence>
    1	Kiitos	kiitos	NOUN	_	Case=Nom|Number=Sing	0	root	_	_
    2	.	.	PUNCT	_	_	1	punct	_	_
    </sentence>
    <sentence>
    1	Mitä	mikä	PRON	_	Case=Par|Number=Sing|PronType=Int	3	dobj	_	_
    2	haluat	haluta	VERB	_	Mood=Ind|Number=Sing|Person=2|Tense=Pres|VerbForm=Fin|Voice=Act	0	root	_	_
    3	tietää	tietää	VERB	_	InfForm=1|Number=Sing|VerbForm=Inf|Voice=Act	2	xcomp	_	_
    4	?	?	PUNCT	_	_	2	punct	_	_
    </sentence>
    """


@pytest.fixture
def vrt_paragraph(paragraph1):
    return f"""
    <doc id="123" url="https://fi.wikipedia.org/wiki?curid=123" title="Foo">
    {paragraph1}
    </doc>
    """


@pytest.fixture
def vrt_two_paragraphs(paragraph1):
    return f"""
    <doc id="123" url="https://fi.wikipedia.org/wiki?curid=123" title="Foo">
    {paragraph1}
    <paragraph>
    <sentence>
    1	Minä	minä	PRON	_	Case=Nom|Number=Sing|Person=1|PronType=Prs	2	nsubj	_	_
    2	keksin	keksiä	VERB	_	Mood=Ind|Number=Sing|Person=1|Tense=Past|VerbForm=Fin|Voice=Act	0	root	_	_
    3	.	.	PUNCT	_	_	2	punct	_	_
    </sentence>
    </paragraph>
    </doc>
    """


@pytest.fixture
def paragraph1():
    return """
    <paragraph>
    <sentence>
    1	Mondego	Mondego	NOUN	_	Case=Nom|Number=Sing	8	nsubj:cop	_	_
    2	on	olla	VERB	_	Mood=Ind|Number=Sing|Person=3|Tense=Pres|VerbForm=Fin|Voice=Act	8	cop	_	_
    3	pisin	pitkä	ADJ	_	Case=Nom|Degree=Sup|Number=Sing	8	amod	_	_
    4	kokonaisuudessaan	kokonaisuus	NOUN	_	Case=Ine|Number=Sing|Person[psor]=3	7	nmod	_	_
    5	Portugalin	Portugali	PROPN	_	Case=Gen|Number=Sing	6	nmod:poss	_	_
    6	alueella	alue	NOUN	_	Case=Ade|Number=Sing	7	nmod	_	_
    7	sijaitseva	sijaita	VERB	_	Case=Nom|Degree=Pos|Number=Sing|PartForm=Pres|VerbForm=Part|Voice=Act	8	acl	_	_
    8	joki	joki	NOUN	_	Case=Nom|Number=Sing	0	root	_	_
    9	.	.	PUNCT	_	_	8	punct	_	_
    </sentence>
    <sentence>
    1	Sen	se	PRON	_	Case=Gen|Number=Sing|PronType=Dem	2	nmod:poss	_	_
    2	pituus	pituus	NOUN	_	Case=Nom|Number=Sing	5	nsubj:cop	_	_
    3	on	olla	VERB	_	Mood=Ind|Number=Sing|Person=3|Tense=Pres|VerbForm=Fin|Voice=Act	5	cop	_	_
    4	234	234	NUM	_	NumType=Card	5	nummod	_	_
    5	kilometriä	kilo#metri	NOUN	_	Case=Par|Number=Sing	0	root	_	_
    6	.	.	PUNCT	_	_	5	punct	_	_
    </sentence>
    </paragraph>
    """


class TestIterVrtXml:

    def test_two_files_two_sentences(self, vrt_two_files_two_sentences: str):
        expected = [
            "tarvitsen apua.",
            " ",
            "mario, iaske hänet aias.",
            " ",
            "Kiitos.",
            " ",
            "Mitä haluat tietää?",
            "\n",  # New line added to the end of all sentences
        ]
        for sentence, sentence_expected in zip_longest(
            iter_vrt_xml(vrt_two_files_two_sentences), expected
        ):
            assert sentence == sentence_expected

    def test_paragraph(self, vrt_paragraph: str):
        expected = [
            "Mondego on pisin kokonaisuudessaan Portugalin alueella sijaitseva joki.",
            " ",
            "Sen pituus on 234 kilometriä.",
            "\n",  # paragraphs end with new line
        ]
        for sentence, sentence_expected in zip_longest(
            iter_vrt_xml(vrt_paragraph, paragraphs=True), expected
        ):
            assert sentence == sentence_expected

    def test_two_paragraph(self, vrt_two_paragraphs: str):
        expected = [
            "Mondego on pisin kokonaisuudessaan Portugalin alueella sijaitseva joki.",
            " ",
            "Sen pituus on 234 kilometriä.",
            "\n",  # paragraphs end with new line
            "Minä keksin.",
            "\n",  # paragraphs end with new line
        ]
        for sentence, sentence_expected in zip_longest(
            iter_vrt_xml(vrt_two_paragraphs, paragraphs=True), expected
        ):
            assert sentence == sentence_expected

    def test_two_paragraph_paragraphs_false(self, vrt_two_paragraphs: str):
        # when paragraphs=False, the sentences are not separated by new lines
        expected = [
            "Mondego on pisin kokonaisuudessaan Portugalin alueella sijaitseva joki.",
            " ",
            "Sen pituus on 234 kilometriä.",
            " ",
            "Minä keksin.",
            "\n",  # End of document
        ]
        for sentence, sentence_expected in zip_longest(
            iter_vrt_xml(vrt_two_paragraphs, paragraphs=False), expected
        ):
            assert sentence == sentence_expected


@pytest.fixture
def vrt_single_word():
    return """
    1	Helppoa	helppo	ADJ	_	Case=Par|Degree=Pos|Number=Sing	0	root	_	_
    """


@pytest.fixture
def vrt_single_word_with_punctionation():
    return """
    1	Helppoa	helppo	ADJ	_	Case=Par|Degree=Pos|Number=Sing	0	root	_	_
    2	!	!	PUNCT	_	_	1	punct	_	_
    """


@pytest.fixture
def vrt_word_parenthesis_punct():
    return """
    1	Miekkakala	miekka#kala	NOUN	_	Case=Nom|Number=Sing	0	root	_	_
    2	(	(	PUNCT	_	_	3	punct	_	_
    3	Marlin	Marlin	PROPN	_	Case=Gen|Number=Sing	1	appos	_	_
    4	)	)	PUNCT	_	_	3	punct	_	_
    5	?	?	PUNCT	_	_	1	punct	_	_
    """


@pytest.fixture
def vrt_word_parenthesis_word():
    return """
    1	Ikuko	Ikuko	PROPN	_	Case=Nom|Number=Sing	2	name	_	_
    2	Matsubara	Matsubara	PROPN	_	Case=Nom|Number=Sing	0	root	_	_
    3	(	(	PUNCT	_	_	4	punct	_	_
    4	6	6	NUM	_	NumType=Card	2	nmod	_	_
    5	years	years	PROPN	_	_	6	name	_	_
    6	old	old	PROPN	_	Case=Nom|Number=Sing	2	conj	_	_
    7	)	)	PUNCT	_	_	2	punct	_	_
    8	Rio	rio	PROPN	_	Case=Nom|Number=Sing	9	name	_	_
    9	Kanno	Kanno	PROPN	_	Case=Nom|Number=Sing	2	conj	_	_
    """


@pytest.fixture
def vrt_word_punct_word():
    return """
    1	Rakastat	rakastaa	VERB	_	Mood=Ind|Number=Sing|Person=2|Tense=Pres|VerbForm=Fin|Voice=Act	0	root	_	_
    2	sitä	se	PRON	_	Case=Par|Number=Sing|PronType=Dem	1	dobj	_	_
    3	,	,	PUNCT	_	_	4	punct	_	_
    4	mitä	mikä	PRON	_	Case=Par|Number=Sing|PronType=Rel	2	ccomp	_	_
    5	me	minä	PRON	_	Case=Nom|Number=Plur|Person=1|PronType=Prs	4	nsubj:cop	_	_
    6	olimme	olla	VERB	_	Mood=Ind|Number=Plur|Person=1|Tense=Past|VerbForm=Fin|Voice=Act	4	cop	_	_
    7	.	.	PUNCT	_	_	1	punct	_	_
    """


@pytest.fixture
def vrt_num_punct_num():
    return """
    1	Aasialaisia	aasialainen	NOUN	_	Case=Par|Number=Plur	6	nsubj:cop	_	_
    2	on	olla	VERB	_	Mood=Ind|Number=Sing|Person=3|Tense=Pres|VerbForm=Fin|Voice=Act	6	cop	_	_
    3	6	6	NUM	_	NumType=Card	6	nummod	_	_
    4	,	,	PUNCT	_	_	3	punct	_	_
    5	3	3	NUM	_	NumType=Card	3	conj	_	_
    6	prosenttia	prosentti	NOUN	_	Case=Par|Number=Sing	0	root	_	_
    """


@pytest.fixture
def vrt_num_punct():
    return """
    1	Aasialaisia	aasialainen	NOUN	_	Case=Par|Number=Plur	6	nsubj:cop	_	_
    2	on	olla	VERB	_	Mood=Ind|Number=Sing|Person=3|Tense=Pres|VerbForm=Fin|Voice=Act	6	cop	_	_
    3	6	6	NUM	_	NumType=Card	6	nummod	_	_
    4	.	.	PUNCT	_	_	3	punct	_	_
    """


@pytest.fixture
def vrt_num_punct_word():
    return """
    1	Aasialaisia	aasialainen	NOUN	_	Case=Par|Number=Plur	6	nsubj:cop	_	_
    2	on	olla	VERB	_	Mood=Ind|Number=Sing|Person=3|Tense=Pres|VerbForm=Fin|Voice=Act	6	cop	_	_
    3	6	6	NUM	_	NumType=Card	6	nummod	_	_
    4	.	.	PUNCT	_	_	3	punct	_	_
    5	Foo	foo	NOUN	_	Case=Par|Number=Sing	0	root	_	_
    6	!	!	PUNCT	_	_	3	punct	_	_
    """


@pytest.fixture
def vrt_double_quotes():
    return """
    12	territoriosta	territorio	NOUN	_	Case=Ela|Number=Sing	10	nmod	_	_
    13	"	"	PUNCT	_	_	16	punct	_	_
    14	Yukon	Yukon	PROPN	_	_	16	name	_	_
    15	Territory	Territory	PROPN	_	Case=Nom|Number=Sing	12	appos	_	_
    16	"	"	PUNCT	_	_	16	punct	_	_
    17	Yukoniksi	Yukoniksi	NOUN	_	Case=Tra|Number=Sing	10	xcomp:ds	_	_
    18	.	.	PUNCT	_	_	5	punct	_	_
    """


@pytest.fixture
def vrt_single_quotes():
    return """
    12	territoriosta	territorio	NOUN	_	Case=Ela|Number=Sing	10	nmod	_	_
    13	'	'	PUNCT	_	_	16	punct	_	_
    14	Yukon	Yukon	PROPN	_	_	16	name	_	_
    15	Territory	Territory	PROPN	_	Case=Nom|Number=Sing	12	appos	_	_
    16	'	'	PUNCT	_	_	16	punct	_	_
    17	Yukoniksi	Yukoniksi	NOUN	_	Case=Tra|Number=Sing	10	xcomp:ds	_	_
    18	.	.	PUNCT	_	_	5	punct	_	_
    """


@pytest.fixture
def vrt_double_quote_with_parenthesis():
    return """
    12	territoriosta	territorio	NOUN	_	Case=Ela|Number=Sing	10	nmod	_	_
    13	(	(	PUNCT	_	_	16	punct	_	_
    14	"	"	PUNCT	_	_	16	punct	_	_
    15	Yukon	Yukon	PROPN	_	_	16	name	_	_
    16	Territory	Territory	PROPN	_	Case=Nom|Number=Sing	12	appos	_	_
    17	"	"	PUNCT	_	_	16	punct	_	_
    18	)	)	PUNCT	_	_	16	punct	_	_
    19	Yukoniksi	Yukoniksi	NOUN	_	Case=Tra|Number=Sing	10	xcomp:ds	_	_
    20	.	.	PUNCT	_	_	5	punct	_	_
    """


@pytest.fixture
def vrt_with_ampersand():
    return """
    1	Nieminen	Niemi	ADJ	_	Case=Nom|Degree=Pos|Derivation=Inen|Number=Sing	2	amod	_	_
    2	&amp;	&amp;	NOUN	_	Case=Nom|Number=Sing	3	compound:nn	_	_
    3	Litmanen	Litmanen	PROPN	_	Case=Nom|Number=Sing	0	root	_	_
    """


@pytest.fixture
def vrt_curly_quotes():
    # This text uses ” instead of ".
    return """
    1	Larry	Larry	PROPN	_	Case=Nom|Number=Sing	5	name	_	_
    2	”	”	PUNCT	_	_	3	punct	_	_
    3	Ler	Ler	PROPN	_	Case=Nom|Number=Sing	1	appos	_	_
    4	”	”	PUNCT	_	_	3	punct	_	_
    5	LaLonde	LaLonde	PROPN	_	Case=Nom|Number=Sing	27	nsubj:cop	_	_"""


@pytest.fixture
def vrt_quote_within_a_word():
    # Sometimes quote may start (or end) within a word.
    return """
    8	on	olla	VERB	_	Mood=Ind|Number=Sing|Person=3|Tense=Pres|VerbForm=Fin|Voice=Act	10	cop	_	_
    9	"le	"le	ADV	_	_	10	advmod	_	_
    10	retraité	retraité	NOUN	_	Case=Nom|Number=Sing	1	parataxis	_	_
    11	"	"	PUNCT	_	_	10	punct	_	_
    """


class TestParseVRTSentence:

    def test_single_word(self, vrt_single_word: str):

        assert parse_vrt_sentence(vrt_single_word) == "Helppoa"

    def test_single_word_with_punctionation(
        self, vrt_single_word_with_punctionation: str
    ):

        assert parse_vrt_sentence(vrt_single_word_with_punctionation) == "Helppoa!"

    def test_word_parenthesis_punct(self, vrt_word_parenthesis_punct: str):

        assert parse_vrt_sentence(vrt_word_parenthesis_punct) == "Miekkakala (Marlin)?"

    def test_word_parenthesis_word(self, vrt_word_parenthesis_word: str):

        assert (
            parse_vrt_sentence(vrt_word_parenthesis_word)
            == "Ikuko Matsubara (6 years old) Rio Kanno"
        )

    def test_word_punct_word(self, vrt_word_punct_word: str):

        assert (
            parse_vrt_sentence(vrt_word_punct_word) == "Rakastat sitä, mitä me olimme."
        )

    def test_num_punct_num(self, vrt_num_punct_num: str):

        assert parse_vrt_sentence(vrt_num_punct_num) == "Aasialaisia on 6,3 prosenttia"

    def test_num_punct_word(self, vrt_num_punct_word: str):

        assert parse_vrt_sentence(vrt_num_punct_word) == "Aasialaisia on 6. Foo!"

    def test_num_punct(self, vrt_num_punct: str):

        assert parse_vrt_sentence(vrt_num_punct) == "Aasialaisia on 6."

    def test_double_quotes(self, vrt_double_quotes: str):

        assert (
            parse_vrt_sentence(vrt_double_quotes)
            == 'territoriosta "Yukon Territory" Yukoniksi.'
        )

    def test_single_quotes(self, vrt_single_quotes: str):

        assert (
            parse_vrt_sentence(vrt_single_quotes)
            == "territoriosta 'Yukon Territory' Yukoniksi."
        )

    def test_double_quotes_with_parenthesis(
        self, vrt_double_quote_with_parenthesis: str
    ):

        assert (
            parse_vrt_sentence(vrt_double_quote_with_parenthesis)
            == 'territoriosta ("Yukon Territory") Yukoniksi.'
        )

    def test_with_ampersand(self, vrt_with_ampersand: str):

        assert parse_vrt_sentence(vrt_with_ampersand) == "Nieminen & Litmanen"

    def test_with_curly_quotes(self, vrt_curly_quotes: str):

        assert parse_vrt_sentence(vrt_curly_quotes) == "Larry ”Ler” LaLonde"

    def test_quote_within_a_word(self, vrt_quote_within_a_word: str):

        assert parse_vrt_sentence(vrt_quote_within_a_word) == 'on "le retraité"'


class TestFormSentence:

    def test_word(self):
        assert _form_sentence(["A"], ["WORD"]) == "A"

    def test_word_punct(self):
        assert _form_sentence(["A", "!"], ["WORD", "PUNCT"]) == "A!"

    def test_word_punct_word(self):
        assert _form_sentence(["A", "!", "B"], ["WORD", "PUNCT", "WORD"]) == "A! B"

    def test_word_parenthesis_punct(self):
        assert (
            _form_sentence(
                ["Foo", "(", "bar", ")", "!"],
                ["WORD", "PUNCT", "WORD", "PUNCT", "PUNCT"],
            )
            == "Foo (bar)!"
        )

    def test_word_parenthesis_word_punct(self):
        assert (
            _form_sentence(
                ["Foo", "(", "bar", ")", "baz", "!"],
                ["WORD", "PUNCT", "WORD", "PUNCT", "WORD", "PUNCT"],
            )
            == "Foo (bar) baz!"
        )

    def test_num_punct_num(self):
        assert _form_sentence(["6", ",", "3"], ["NUM", "PUNCT", "NUM"]) == "6,3"

    def test_num_punct_num_word(self):
        assert (
            _form_sentence(["6", ",", "3", "foo"], ["NUM", "PUNCT", "NUM", "WORD"])
            == "6,3 foo"
        )

    def test_num_punct(self):
        assert _form_sentence(["6", "."], ["NUM", "PUNCT"]) == "6."

    def test_num_punct_word(self):
        assert (
            _form_sentence(["6", ".", "Foo", "!"], ["NUM", "PUNCT", "WORD", "PUNCT"])
            == "6. Foo!"
        )

    def test_unknown_part_type(self):
        with pytest.raises(ValueError):
            _form_sentence(["A"], ["FOO-IM-NOT-A-VALID-TYPE"])
