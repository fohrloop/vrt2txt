from vrt2txt import iter_sentence


class TestSentence:

    def test_punctuation(self):
        s = "\n1\tAurajoen\taura#joki\tNOUN\t_\tCase=Gen|Number=Sing\t2\tnmod:poss\t_\t_\n2\tkeskivirtaamat\tkeski#virtaama\tNOUN\t_\tCase=Nom|Number=Plur\t11\tnsubj:cop\t_\t_\n3\tovat\tolla\tVERB\t_\tMood=Ind|Number=Plur|Person=3|Tense=Pres|VerbForm=Fin|Voice=Act\t11\tcop\t_\t_\n4\tvuosina\tvuosi\tNOUN\t_\tCase=Ess|Number=Plur\t11\tnmod\t_\t_\n5\t1938–2010\t1938–2010\tNUM\t_\tNumType=Card\t4\tnummod\t_\t_\n6\tolleet\tolla\tVERB\t_\tCase=Nom|Degree=Pos|Number=Plur|PartForm=Past|VerbForm=Part|Voice=Act\t11\tcop\t_\t_\n7\tHalistenkoskella\thalinen#koski\tPROPN\t_\tCase=Ade|Number=Sing\t11\tnmod\t_\t_\n8\t6\t6\tNUM\t_\tNumType=Card\t11\tnummod\t_\t_\n9\t,\t,\tPUNCT\t_\t_\t8\tpunct\t_\t_\n10\t8\t8\tNUM\t_\tNumType=Card\t8\tconj\t_\t_\n11\tm³\tm³\tNOUN\t_\tCase=Nom|Number=Sing\t0\troot\t_\t_\n12\t/\t/\tPUNCT\t_\t_\t11\tpunct\t_\t_\n13\ts\ts\tNOUN\t_\tAbbr=Yes|Case=Nom|Number=Sing\t11\tconj\t_\t_\n14\tja\tja\tCONJ\t_\t_\t11\tcc\t_\t_\n15\tvuosina\tvuosi\tNOUN\t_\tCase=Ess|Number=Plur\t21\tnmod\t_\t_\n16\t1943–2010\t1943–2010\tNUM\t_\tNumType=Card\t15\tnummod\t_\t_\n17\tHypöistenkoskella\tHypöistenkoskella\tPROPN\t_\tCase=Ade|Number=Sing\t21\tnmod\t_\t_\n18\t3\t3\tNUM\t_\tNumType=Card\t21\tnummod\t_\t_\n19\t,\t,\tPUNCT\t_\t_\t18\tpunct\t_\t_\n20\t3\t3\tNUM\t_\tNumType=Card\t18\tconj\t_\t_\n21\tm³\tm³\tNOUN\t_\tCase=Nom|Number=Sing\t11\tconj\t_\t_\n22\t/\t/\tPUNCT\t_\t_\t11\tpunct\t_\t_\n23\ts\ts\tNOUN\t_\tAbbr=Yes|Case=Nom|Number=Sing\t11\tconj\t_\t_\n24\t.\t.\tPUNCT\t_\t_\t11\tpunct\t_\t_\n".strip()

        joined_sentence = "".join(iter_sentence(s))
        assert (
            joined_sentence
            == "Aurajoen keskivirtaamat ovat vuosina 1938–2010 olleet Halistenkoskella 6,8 m³/ s ja vuosina 1943–2010 Hypöistenkoskella 3,3 m³/ s."
        )
