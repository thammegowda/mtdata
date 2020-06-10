#!/usr/bin/env python
#
# Author: Thamme Gowda [tg (at) isi (dot) edu] 
# Created: 6/9/20
from mtdata.index import Entry, Index

def load_all(index: Index):
    data="""an-ca an-de an-en an-es an-fr an-gl an-it an-pl an-pt an-ru ar-arz ar-az ar-ba ar-be ar-bg ar-bn ar-br ar-bs ar-ca ar-ceb
 ar-cs ar-da ar-de ar-el ar-en ar-eo ar-es ar-et ar-eu ar-fa ar-fi ar-fr ar-gl ar-he ar-hi ar-hr ar-hu ar-id ar-is ar-it
 ar-ja ar-kk ar-ko ar-lt ar-mk ar-ml ar-mr ar-nds ar-ne ar-nl ar-no ar-pl ar-pt ar-ro ar-ru ar-sh ar-si ar-sk ar-sl ar-sq
 ar-sr ar-sv ar-sw ar-ta ar-te ar-tl ar-tr ar-tt ar-uk ar-vi arz-de arz-en arz-es arz-fr ar-zh arz-it arz-pt arz-ru as-de as-es
 as-fr as-it azb-fr az-bg az-ca az-cs az-da az-de az-el az-en az-es az-et az-fa az-fi az-fr az-gl az-he az-hr az-hu az-id
 az-it az-ja az-ko az-nl az-no az-pl az-pt az-ro az-ru az-sr az-sv az-ta az-tr az-uk az-vi az-zh ba-bg ba-ca ba-cs ba-da
 ba-de ba-el ba-en ba-es ba-fi ba-fr ba-gl ba-hr ba-hu ba-id ba-it ba-ja ba-nl ba-no ba-pl ba-pt bar-de bar-en bar-es bar-fr
 bar-it ba-ro bar-pt bar-ru ba-ru ba-sh ba-sk ba-sl ba-sr ba-sv ba-tr ba-uk ba-zh be-bg be-ca be-cs be-de be-en be-es be-fi
 be-fr be-he be-hu be-it be-ja be-nl be-no be-pl be-pt be-ro be-ru be-sr be-sv be-uk bg-bn bg-bs bg-ca bg-ceb bg-cs bg-da
 bg-de bg-el bg-en bg-eo bg-es bg-et bg-eu bg-fa bg-fi bg-fr bg-gl bg-he bg-hi bg-hr bg-hu bg-id bg-is bg-it bg-ja bg-kk
 bg-ko bg-lt bg-mk bg-ml bg-mr bg-nds bg-ne bg-nl bg-no bg-pl bg-pt bg-ro bg-ru bg-sh bg-si bg-sk bg-sl bg-sq bg-sr bg-sv
 bg-sw bg-ta bg-te bg-tl bg-tr bg-tt bg-uk bg-vi bg-zh bn-bs bn-ca bn-cs bn-da bn-de bn-el bn-en bn-eo bn-es bn-et bn-eu
 bn-fa bn-fi bn-fr bn-gl bn-he bn-hi bn-hr bn-hu bn-id bn-it bn-ja bn-ko bn-lt bn-mk bn-nl bn-no bn-pl bn-pt bn-ro bn-ru
 bn-sh bn-sk bn-sl bn-sq bn-sr bn-sv bn-ta bn-tr bn-uk bn-vi bn-zh br-de br-en br-es br-fr br-it br-pt br-ru br-uk bs-ca
 bs-cs bs-da bs-de bs-el bs-en bs-eo bs-es bs-et bs-eu bs-fa bs-fi bs-fr bs-gl bs-he bs-hi bs-hr bs-hu bs-id bs-is bs-it
 bs-ja bs-ko bs-lt bs-mk bs-ml bs-mr bs-nl bs-no bs-pl bs-pt bs-ro bs-ru bs-sh bs-si bs-sk bs-sl bs-sq bs-sr bs-sv bs-ta
 bs-te bs-tl bs-tr bs-uk bs-vi bs-zh ca-ceb ca-cs ca-da ca-de ca-el ca-en ca-eo ca-es ca-et ca-eu ca-fa ca-fi ca-fo ca-fr
 ca-fy ca-gl ca-he ca-hi ca-hr ca-hu ca-id ca-is ca-it ca-ja ca-ka ca-kk ca-ko ca-la ca-lb ca-lt ca-mk ca-ml ca-mr ca-nds
 ca-ne ca-nl ca-no ca-oc ca-pl ca-pt ca-ro ca-ru ca-sh ca-si ca-sk ca-sl ca-sq ca-sr ca-sv ca-sw ca-ta ca-te ca-tl ca-tr
 ca-tt ca-uk ca-vi ca-zh ceb-cs ceb-de ceb-en ceb-es ceb-fi ceb-fr ceb-hu ceb-it ceb-ja ceb-nl ceb-no ceb-pl ceb-pt ceb-ro ceb-ru ceb-sv
 ceb-uk cs-da cs-de cs-el cs-en cs-eo cs-es cs-et cs-eu cs-fa cs-fi cs-fr cs-fy cs-gl cs-he cs-hi cs-hr cs-hu cs-id cs-is
 cs-it cs-ja cs-ka cs-kk cs-ko cs-la cs-lt cs-mk cs-ml cs-mr cs-nds cs-ne cs-nl cs-no cs-oc cs-pl cs-pt cs-ro cs-ru cs-sh
 cs-si cs-sk cs-sl cs-sq cs-sr cs-sv cs-sw cs-ta cs-te cs-tl cs-tr cs-tt cs-uk cs-vi cs-zh da-de da-el da-en da-eo da-es
 da-et da-eu da-fa da-fi da-fo da-fr da-gl da-he da-hi da-hr da-hu da-id da-is da-it da-ja da-ko da-lt da-mk da-ml da-mr
 da-nds da-ne da-nl da-no da-pl da-pt da-ro da-ru da-sh da-si da-sk da-sl da-sq da-sr da-sv da-sw da-ta da-te da-tl da-tr
 da-tt da-uk da-vi da-zh de-el de-en de-eo de-es de-et de-eu de-fa de-fi de-fo de-fr de-fy de-gl de-gom de-he de-hi de-hr
 de-hu de-hy de-id de-is de-it de-ja de-ka de-kk de-ko de-la de-lb de-lt de-mk de-ml de-mr de-nds de-ne de-nl de-no de-oc
 de-pl de-pt de-rm de-ro de-ru de-sh de-si de-sk de-sl de-sq de-sr de-sv de-sw de-ta de-te de-tg de-tl de-tr de-tt de-uk
 de-vi de-wuu de-zh el-en el-eo el-es el-et el-eu el-fa el-fi el-fr el-gl el-he el-hi el-hr el-hu el-id el-is el-it el-ja
 el-ko el-lt el-mk el-ml el-mr el-nl el-no el-pl el-pt el-ro el-ru el-sh el-si el-sk el-sl el-sq el-sr el-sv el-sw el-ta
 el-te el-tl el-tr el-uk el-vi el-zh en-eo en-es en-et en-eu en-fa en-fi en-fo en-fr en-fy en-gl en-he en-hi en-hr en-hu
 en-id en-io en-is en-it en-ja en-jv en-ka en-kk en-ko en-la en-lb en-lmo en-lt en-mg en-mk en-ml en-mr en-mwl en-nds_nl en-nds
 en-ne en-nl en-no en-oc en-pl en-pt en-ro en-ru en-sh en-simple en-si en-sk en-sl en-sq en-sr en-sv en-sw en-ta en-te en-tg
 en-tl en-tr en-tt en-ug en-uk en-vi en-wuu en-zh eo-es eo-et eo-eu eo-fa eo-fi eo-fr eo-gl eo-he eo-hi eo-hr eo-hu eo-id
 eo-is eo-it eo-ja eo-ko eo-lt eo-mk eo-ml eo-mr eo-nds eo-nl eo-no eo-pl eo-pt eo-ro eo-ru eo-sh eo-si eo-sk eo-sl eo-sq
 eo-sr eo-sv eo-ta eo-te eo-tl eo-tr eo-uk eo-vi eo-zh es-et es-eu es-fa es-fi es-fo es-fr es-fy es-gl es-gom es-he es-hi
 es-hr es-hu es-hy es-id es-is es-it es-ja es-jv es-ka es-kk es-ko es-la es-lb es-lt es-mk es-ml es-mr es-nds es-ne es-nl
 es-no es-oc es-pl es-pt es-ro es-ru es-sh es-si es-sk es-sl es-sq es-sr es-sv es-sw es-ta es-te es-tl es-tr es-tt es-uk
 es-vi es-wuu es-zh et-eu et-fa et-fi et-fr et-gl et-he et-hi et-hr et-hu et-id et-is et-it et-ja et-ko et-lt et-mk et-ml
 et-mr et-nl et-no et-pl et-pt et-ro et-ru et-sh et-si et-sk et-sl et-sq et-sr et-sv et-ta et-te et-tl et-tr et-uk et-vi
 et-zh eu-fa eu-fi eu-fr eu-gl eu-he eu-hi eu-hr eu-hu eu-id eu-is eu-it eu-ja eu-ko eu-lt eu-mk eu-ml eu-mr eu-nl eu-no
 eu-pl eu-pt eu-ro eu-ru eu-sh eu-sk eu-sl eu-sq eu-sr eu-sv eu-ta eu-te eu-tr eu-uk eu-vi eu-zh fa-fi fa-fr fa-gl fa-he
 fa-hi fa-hr fa-hu fa-id fa-it fa-ja fa-ko fa-lt fa-mk fa-ml fa-mr fa-nl fa-no fa-pl fa-pt fa-ro fa-ru fa-sh fa-sk fa-sl
 fa-sq fa-sr fa-sv fa-ta fa-te fa-tr fa-uk fa-vi fa-zh fi-fr fi-gl fi-he fi-hi fi-hr fi-hu fi-id fi-is fi-it fi-ja fi-ko
 fi-lt fi-mk fi-ml fi-mr fi-nds fi-ne fi-nl fi-no fi-oc fi-pl fi-pt fi-ro fi-ru fi-sh fi-si fi-sk fi-sl fi-sq fi-sr fi-sv
 fi-sw fi-ta fi-te fi-tl fi-tr fi-tt fi-uk fi-vi fi-zh fo-fr fo-it fo-nl fo-pl fo-pt fo-ru fo-sv fr-fy fr-gl fr-gom fr-he
 fr-hi fr-hr fr-hu fr-hy fr-id fr-is fr-it fr-ja fr-jv fr-ka fr-kk fr-ko fr-la fr-lb fr-lt fr-mg fr-mk fr-ml fr-mr fr-nds
 fr-ne fr-nl fr-no fr-oc fr-pl fr-pt fr-ro fr-ru fr-sh fr-si fr-sk fr-sl fr-sq fr-sr fr-sv fr-sw fr-ta fr-te fr-tl fr-tr
 fr-tt fr-uk fr-vi fr-wuu fr-zh fy-it fy-nl fy-pl fy-pt fy-ru fy-sv gl-he gl-hi gl-hr gl-hu gl-id gl-is gl-it gl-ja gl-ko
 gl-lt gl-mk gl-ml gl-mr gl-nds gl-ne gl-nl gl-no gl-oc gl-pl gl-pt gl-ro gl-ru gl-sh gl-si gl-sk gl-sl gl-sq gl-sr gl-sv
 gl-ta gl-te gl-tl gl-tr gl-tt gl-uk gl-vi gl-zh gom-it gom-pt gom-ru he-hi he-hr he-hu he-id he-is he-it he-ja he-ko he-lt
 he-mk he-ml he-mr he-nl he-no he-pl he-pt he-ro he-ru he-sh he-si he-sk he-sl he-sq he-sr he-sv he-sw he-ta he-te he-tl
 he-tr he-uk he-vi he-zh hi-hr hi-hu hi-id hi-it hi-ja hi-ko hi-lt hi-mk hi-mr hi-ne hi-nl hi-no hi-pl hi-pt hi-ro hi-ru
 hi-sh hi-sk hi-sl hi-sq hi-sr hi-sv hi-ta hi-te hi-tr hi-uk hi-vi hi-zh hr-hu hr-id hr-is hr-it hr-ja hr-ko hr-lt hr-mk
 hr-ml hr-mr hr-ne hr-nl hr-no hr-pl hr-pt hr-ro hr-ru hr-sh hr-si hr-sk hr-sl hr-sq hr-sr hr-sv hr-ta hr-te hr-tl hr-tr
 hr-uk hr-vi hr-zh hu-id hu-is hu-it hu-ja hu-kk hu-ko hu-lt hu-mk hu-ml hu-mr hu-nds hu-ne hu-nl hu-no hu-oc hu-pl hu-pt
 hu-ro hu-ru hu-sh hu-si hu-sk hu-sl hu-sq hu-sr hu-sv hu-sw hu-ta hu-te hu-tl hu-tr hu-uk hu-vi hu-zh hy-it hy-pt hy-ru
 id-is id-it id-ja id-jv id-ko id-lt id-mk id-ml id-mr id-ne id-nl id-no id-pl id-pt id-ro id-ru id-sh id-si id-sk id-sl
 id-sq id-sr id-sv id-sw id-ta id-te id-tl id-tr id-tt id-uk id-vi id-zh is-it is-ja is-lt is-mk is-nl is-no is-pl is-pt
 is-ro is-ru is-sh is-sk is-sl is-sr is-sv is-tr is-uk is-vi is-zh it-ja it-jv it-ka it-kk it-ko it-la it-lb it-lmo it-lt
 it-mk it-ml it-mr it-nds it-ne it-nl it-no it-oc it-pl it-pt it-ro it-ru it-scn it-sh it-si it-sk it-sl it-sq it-sr it-sv
 it-sw it-ta it-te it-tl it-tr it-tt it-uk it-vi it-wuu it-zh ja-kk ja-ko ja-lt ja-mk ja-ml ja-mr ja-nds ja-nl ja-no ja-pl
 ja-pt ja-ro ja-ru ja-sh ja-si ja-sk ja-sl ja-sq ja-sr ja-sv ja-sw ja-ta ja-te ja-tl ja-tr ja-tt ja-uk ja-vi ja-zh jv-pt
 ka-nl ka-pl ka-pt ka-ru ka-sv kk-nl kk-no kk-pl kk-pt kk-ro kk-ru kk-sv kk-tr kk-uk ko-lt ko-mk ko-ml ko-mr ko-nl ko-no
 ko-pl ko-pt ko-ro ko-ru ko-sh ko-sk ko-sl ko-sq ko-sr ko-sv ko-ta ko-te ko-tr ko-uk ko-vi ko-zh la-nl la-pl la-pt la-ro
 la-ru la-sv lb-nl lb-pl lb-pt lb-ru lb-sv lt-mk lt-ml lt-mr lt-nl lt-no lt-pl lt-pt lt-ro lt-ru lt-sh lt-si lt-sk lt-sl
 lt-sq lt-sr lt-sv lt-ta lt-te lt-tl lt-tr lt-uk lt-vi lt-zh mk-ml mk-mr mk-nl mk-no mk-pl mk-pt mk-ro mk-ru mk-sh mk-si
 mk-sk mk-sl mk-sq mk-sr mk-sv mk-ta mk-te mk-tl mk-tr mk-uk mk-vi mk-zh ml-nl ml-no ml-pl ml-pt ml-ro ml-ru ml-sh ml-sk
 ml-sl ml-sq ml-sr ml-sv ml-tr ml-uk ml-vi ml-zh mr-nl mr-no mr-pl mr-pt mr-ro mr-ru mr-sh mr-sk mr-sl mr-sq mr-sr mr-sv
 mr-tr mr-uk mr-vi mr-zh mwl-pt nds_nl-nl nds-nl nds-no nds-pl nds-pt nds-ro nds-ru nds-sv nds-uk ne-nl ne-no ne-pl ne-pt ne-ro ne-ru
 ne-sh ne-sk ne-sl ne-sv ne-uk nl-no nl-oc nl-pl nl-pt nl-ro nl-ru nl-sh nl-si nl-sk nl-sl nl-sq nl-sr nl-sv nl-sw nl-ta
 nl-te nl-tl nl-tr nl-tt nl-uk nl-vi nl-zh no-pl no-pt no-ro no-ru no-sh no-si no-sk no-sl no-sq no-sr no-sv no-sw no-ta
 no-te no-tl no-tr no-tt no-uk no-vi no-zh oc-pl oc-pt oc-ro oc-ru oc-sv pl-pt pl-ro pl-ru pl-sh pl-si pl-sk pl-sl pl-sq
 pl-sr pl-sv pl-sw pl-ta pl-te pl-tl pl-tr pl-tt pl-uk pl-vi pl-zh pt-ro pt-ru pt-sh pt-si pt-sk pt-sl pt-sq pt-sr pt-sv
 pt-sw pt-ta pt-te pt-tl pt-tr pt-tt pt-uk pt-vi pt-wuu pt-zh ro-ru ro-sh ro-si ro-sk ro-sl ro-sq ro-sr ro-sv ro-sw ro-ta
 ro-te ro-tl ro-tr ro-tt ro-uk ro-vi ro-zh ru-sh ru-si ru-sk ru-sl ru-sq ru-sr ru-sv ru-sw ru-ta ru-te ru-tg ru-tl ru-tr
 ru-tt ru-uk ru-vi ru-wuu ru-zh sh-si sh-sk sh-sl sh-sq sh-sr sh-sv sh-ta sh-te sh-tl sh-tr sh-uk sh-vi sh-zh si-sk si-sl
 si-sq si-sr si-sv si-tr si-uk si-vi si-zh sk-sl sk-sq sk-sr sk-sv sk-ta sk-te sk-tl sk-tr sk-uk sk-vi sk-zh sl-sq sl-sr
 sl-sv sl-ta sl-te sl-tl sl-tr sl-uk sl-vi sl-zh sq-sr sq-sv sq-ta sq-te sq-tl sq-tr sq-uk sq-vi sq-zh sr-sv sr-ta sr-te
 sr-tl sr-tr sr-uk sr-vi sr-zh sv-sw sv-ta sv-te sv-tl sv-tr sv-tt sv-uk sv-vi sv-zh sw-tr sw-uk sw-vi sw-zh ta-tr ta-uk
 ta-vi ta-zh te-tr te-uk te-vi te-zh tl-tr tl-uk tl-vi tl-zh tr-tt tr-uk tr-vi tr-zh tt-uk tt-zh uk-vi uk-zh vi-zh wuu-zh"""
    cite = """@article{wikimatrix1,
    author    = {Holger Schwenk and Vishrav Chaudhary and Shuo Sun and Hongyu Gong and Francisco Guzm{\'{a}}n},
    title     = {WikiMatrix: Mining 135M Parallel Sentences in 1620 Language Pairs from Wikipedia},
    journal   = {CoRR},
    volume    = {abs/1907.05791},
    year      = {2019},
    url       = {http://arxiv.org/abs/1907.05791},
    archivePrefix = {arXiv},
    eprint    = {1907.05791},
    timestamp = {Wed, 17 Jul 2019 10:27:36 +0200},
    biburl    = {https://dblp.org/rec/journals/corr/abs-1907-05791.bib},
    bibsource = {dblp computer science bibliography, https://dblp.org}}"""
    url_pat = "https://dl.fbaipublicfiles.com/laser/WikiMatrix/v1/WikiMatrix.%s-%s.tsv.gz"
    mapping = dict(sh='hbs')
    skips = {'nds_nl', 'simple'}
    for pair in data.split():
        l1, l2 = pair.split('-')
        if l1 in skips or l2 in skips:
            continue
        l1iso, l2iso = mapping.get(l1, l1), mapping.get(l2, l2)
        url = url_pat % (l1, l2)
        ent = Entry(langs=(l1iso, l2iso), url=url, name='WikiMatrix_v1', cols=(1, 2), cite=cite)
        index.add_entry(ent)
