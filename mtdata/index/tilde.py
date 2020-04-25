#!/usr/bin/env python
#
# Author: Thamme Gowda [tg (at) isi (dot) edu] 
# Created: 4/8/20
from mtdata.entry import Entry
from mtdata.index import Index

def load(index: Index):
    CONTENT="""EESC2017::bg-de bg-en bg-fr cs-de cs-en cs-fr da-de da-en da-fr de-el de-en de-es de-et de-fi de-fr de-hr de-hu de-is de-it de-lt de-lv de-mt de-nl de-pl de-pt de-ro de-sk de-sl de-sv el-en el-fr en-es en-et en-fi en-fr en-hr en-hu en-is en-it en-lt en-lv en-mt en-nl en-pl en-pt en-ro en-sk en-sl en-sv es-fr et-fr fi-fr fr-hr fr-hu fr-is fr-it fr-lt fr-lv fr-mt fr-nl fr-pl fr-pt fr-ro fr-sk fr-sl fr-sv
    EMA2016::bg-de bg-en bg-fr cs-de cs-en cs-fr da-de da-en da-fr de-el de-en de-es de-et de-fi de-fr de-hr de-hu de-is de-it de-lt de-lv de-mt de-nl de-no de-pl de-pt de-ro de-sk de-sl de-sv el-en el-fr en-es en-et en-fi en-fr en-hr en-hu en-is en-it en-lt en-lv en-mt en-nl en-no en-pl en-pt en-ro en-sk en-sl en-sv es-fr et-fr fi-fr fr-hr fr-hu fr-is fr-it fr-lt fr-lv fr-mt fr-nl fr-no fr-pl fr-pt fr-ro fr-sk fr-sl fr-sv
    airbaltic::de-en de-et de-fi de-lt de-lv de-ru en-et en-fi en-lt en-lv en-ru et-fi et-lt et-lv et-ru fi-lt fi-lv fi-ru lt-lv lt-ru lv-ru
    czechtourism::de-en de-es de-fr de-it de-pl de-pt de-ru en-es en-fr en-it en-pl en-pt en-ru es-fr es-it es-pl es-pt es-ru fr-it fr-pl fr-pt fr-ru it-pl it-pt it-ru pl-pt pl-ru pt-ru
    ecb2017::bg-cs bg-da bg-de bg-el bg-en bg-es bg-et bg-fi bg-fr bg-hr bg-hu bg-it bg-lt bg-lv bg-mt bg-nl bg-pl bg-pt bg-ro bg-sk bg-sl bg-sv cs-da cs-de cs-el cs-en cs-es cs-et cs-fi cs-fr cs-hr cs-hu cs-it cs-lt cs-lv cs-mt cs-nl cs-pl cs-pt cs-ro cs-sk cs-sl cs-sv da-de da-el da-en da-es da-et da-fi da-fr da-hr da-hu da-it da-lt da-lv da-mt da-nl da-pl da-pt da-ro da-sk da-sl da-sv de-el de-en de-es de-et de-fi de-fr de-hr de-hu de-it de-lt de-lv de-mt de-nl de-pl de-pt de-ro de-sk de-sl de-sv el-en el-es el-et el-fi el-fr el-hr el-hu el-it el-lt el-lv el-mt el-nl el-pl el-pt el-ro el-sk el-sl el-sv en-es en-et en-fi en-fr en-hr en-hu en-it en-lt en-lv en-mt en-nl en-pl en-pt en-ro en-sk en-sl en-sv es-et es-fi es-fr es-hr es-hu es-it es-lt es-lv es-mt es-nl es-pl es-pt es-ro es-sk es-sl es-sv et-fi et-fr et-hr et-hu et-it et-lt et-lv et-mt et-nl et-pl et-pt et-ro et-sk et-sl et-sv fi-fr fi-hr fi-hu fi-it fi-lt fi-lv fi-mt fi-nl fi-pl fi-pt fi-ro fi-sk fi-sl fi-sv fr-hr fr-hu fr-it fr-lt fr-lv fr-mt fr-nl fr-pl fr-pt fr-ro fr-sk fr-sl fr-sv hr-hu hr-it hr-lt hr-lv hr-mt hr-nl hr-pl hr-pt hr-ro hr-sk hr-sl hr-sv hu-it hu-lt hu-lv hu-mt hu-nl hu-pl hu-pt hu-ro hu-sk hu-sl hu-sv it-lt it-lv it-mt it-nl it-pl it-pt it-ro it-sk it-sl it-sv lt-lv lt-mt lt-nl lt-pl lt-pt lt-ro lt-sk lt-sl lt-sv lv-mt lv-nl lv-pl lv-pt lv-ro lv-sk lv-sl lv-sv mt-nl mt-pl mt-pt mt-ro mt-sk mt-sl mt-sv nl-pl nl-pt nl-ro nl-sk nl-sl nl-sv pl-pt pl-ro pl-sk pl-sl pl-sv pt-ro pt-sk pt-sl pt-sv ro-sk ro-sl ro-sv sk-sl sk-sv sl-sv
    fold::en-lv
    rapid2016::bg-de bg-en bg-fr cs-de cs-fr da-de da-en da-fr de-el de-en de-es de-et de-fi de-fr de-hr de-hu de-is de-it de-lt de-lv de-mt de-nl de-no de-pl de-pt de-ro de-sk de-sl de-sv el-en el-fr en-es en-et en-fi en-fr en-hr en-hu en-is en-it en-lt en-lv en-mt en-nl en-no en-pt en-ro en-sk en-sl en-sv es-fr et-fr fi-fr fr-hr fr-hu fr-is fr-it fr-lt fr-lv fr-mt fr-nl fr-no fr-pl fr-pt fr-ro fr-sk fr-sl fr-sv
    rapid2019::cs-en de-en en-pl
    worldbank::en-es en-fr en-hr en-pl en-pt en-ro en-ru en-sq en-sr en-tr en-uk"""
    TILDE_CITE = """@inproceedings{rozis-skadins-2017-tilde,
    title = "Tilde {MODEL} - Multilingual Open Data for {EU} Languages",
    author = "Rozis, Roberts  and
      Skadi{\c{n}}{\v{s}}, Raivis",
    booktitle = "Proceedings of the 21st Nordic Conference on Computational Linguistics",
    month = may,
    year = "2017",
    address = "Gothenburg, Sweden",
    publisher = "Association for Computational Linguistics",
    url = "https://www.aclweb.org/anthology/W17-0235",
    pages = "263--265",
}"""
    TILDE = 'https://tilde-model.s3-eu-west-1.amazonaws.com/%s.%s-%s.tmx.zip'
    for line in CONTENT.splitlines():
        line = line.strip()
        name, pairs = line.split('::')
        for pair in pairs.split(' '):
            l1, l2 = pair.split('-')
            url = TILDE % (name, l1, l2)
            index.add_entry(Entry(langs=(l1, l2), name=name, url=url, cite=TILDE_CITE,
                                    in_paths=["*.tmx"]))
