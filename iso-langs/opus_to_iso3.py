#!/usr/bin/env python
#
# Author: Thamme Gowda [tg\tat isi\tdot edu] 
# Created: 5/5/20
data = """ace\tAchinese
af\tAfrikaans
ak\tAkan
sq\tAlbanian
am\tAmharic
ar_TN\tArabic
ar_SY\tArabic
ara\tArabic
ar\tArabic
an\tAragonese
hy\tArmenian
as\tAssamese
ast\tAsturian
aym\tAymara
az_IR\tAzerbaijani
az\tAzerbaijani
bal\tBaluchi
ba\tBashkir
eu\tBasque
be\tBelarusian
bem\tBemba
bn\tBengali
bn_IN\tBengali
ber\tBerber languages
bho\tBhojpuri
byn\tBlin
nb\tBokmål, Norwegian
nb_NO\tBokmål, Norwegian
bs\tBosnian
br\tBreton
bg_BG\tBulgarian
bg\tBulgarian
bua\tBuriat
my\tBurmese
cat\tCatalan
ca\tCatalan
ceb\tCebuano
km\tCentral Khmer
ce\tChechen
chr\tCherokee
ny\tChichewa
zh\tChinese
zh_HK\tChinese
zh_CN\tChinese
zh_TW\tChinese
cv\tChuvash
kw\tCornish
co\tCorsican
mus\tCreek
crh\tCrimean Tatar
hr\tCroatian
cs\tCzech
da\tDanish
da_DK\tDanish
dv\tDivehi
nl_NL\tDutch
nl\tDutch
dz\tDzongkha
en_ZA\tEnglish
en\tEnglish
en_AU\tEnglish
en_US\tEnglish
en_CA\tEnglish
en_GB\tEnglish
en_NZ\tEnglish
ang\tEnglish, Old 
eo\tEsperanto
et\tEstonian
fo\tFaroese
fil\tFilipino
fi\tFinnish
fr\tFrench
fr_CA\tFrench
fr_FR\tFrench
frm\tFrench, Middle 
fur\tFriulian
ff\tFulah
gd\tGaelic
gl\tGalician
lg\tGanda
ka\tGeorgian
de_AT\tGerman
de\tGerman
de_DE\tGerman
de_CH\tGerman
el\tGreek
grc\tGreek, Ancient 
gn\tGuarani
gu\tGujarati
ht\tHaitian
ha\tHausa
haw\tHawaiian
he\tHebrew
hil\tHiligaynon
hi\tHindi
hi_IN\tHindi
hu\tHungarian
is\tIcelandic
io\tIdo
ig\tIgbo
id\tIndonesian
ia\tInterlingua 
iu\tInuktitut
ga\tIrish
it_IT\tItalian
it\tItalian
ja\tJapanese
jv\tJavanese
kab\tKabyle
kl\tKalaallisut
xal\tKalmyk
kn\tKannada
kr\tKanuri
ks\tKashmiri
csb\tKashubian
kk\tKazakh
rw\tKinyarwanda
ky\tKirghiz
tlh\tKlingon
kg\tKongo
kok\tKonkani
ko\tKorean
ku\tKurdish
lo\tLao
la\tLatin
lv\tLatvian
li\tLimburgan
ln\tLingala
lt\tLithuanian
jbo\tLojban
nds\tLow German
dsb\tLower Sorbian
lb\tLuxembourgish
mk\tMacedonian
mai\tMaithili
mg\tMalagasy
ms\tMalay
ms_MY\tMalay
ml\tMalayalam
mt\tMaltese
gv\tManx
mi\tMaori
mr\tMarathi
mh\tMarshallese
mn\tMongolian
nqo\tN'Ko
nr\tNdebele, South
nap\tNeapolitan
ne\tNepali
se\tNorthern Sami
no_nb\tNorwegian
no\tNorwegian
nn_NO\tNorwegian Nynorsk
nn\tNorwegian Nynorsk
oc\tOccitan 
oj\tOjibwa
or\tOriya
om\tOromo
os\tOssetian
pam\tPampanga
pa\tPanjabi
pap\tPapiamento
nso\tPedi
fa\tPersian
fa_AF\tPersian
fa_IR\tPersian
pl\tPolish
pt_PT\tPortuguese
pt_BR\tPortuguese
pt\tPortuguese
ps\tPushto
qu\tQuechua
ro\tRomanian
rm\tRomansh
rom\tRomany
ru\tRussian
sm\tSamoan
sa\tSanskrit
sc\tSardinian
sco\tScots
sr_ME\tSerbian
sr\tSerbian
shn\tShan
sn\tShona
sd\tSindhi
si\tSinhala
sk\tSlovak
sl\tSlovenian
so\tSomali
son\tSonghai languages
st\tSotho, Southern
es_PE\tSpanish
es_CO\tSpanish
es_DO\tSpanish
es_HN\tSpanish
es_MX\tSpanish
es_ES\tSpanish
es_SV\tSpanish
es_UY\tSpanish
es_EC\tSpanish
es_PR\tSpanish
es_NI\tSpanish
es_VE\tSpanish
es\tSpanish
es_PA\tSpanish
es_AR\tSpanish
es_CR\tSpanish
es_CL\tSpanish
es_GT\tSpanish
sw\tSwahili
sv\tSwedish
syr\tSyriac
tl\tTagalog
tl_PH\tTagalog
tg_TJ\tTajik
tg\tTajik
ta_LK\tTamil
ta\tTamil
tt\tTatar
te\tTelugu
tet\tTetum
th\tThai
bo\tTibetan
ti\tTigrinya
ts\tTsonga
tr\tTurkish
tr_TR\tTurkish
tk\tTurkmen
tw\tTwi
ug\tUighur
uk\tUkrainian
hsb\tUpper Sorbian
ur\tUrdu
ur_PK\tUrdu
uz\tUzbek
ve\tVenda
vi\tVietnamese
vi_VN\tVietnamese
wa\tWalloon
cy\tWelsh
fy\tWestern Frisian
wo\tWolof
xh\tXhosa
yi\tYiddish
yo\tYoruba
zza\tZaza
zu\tZulu
ary\tary
brx\tbrx
ckb\tckb
foo\tfoo
frp\tfrp
gr\tgr
guc\tguc
hne\thne
jp\tjp
ksh\tksh
lij\tlij
lld\tlld
ltg\tltg
mhr\tmhr
miq\tmiq
mo\tmo
nan\tnan
nhn\tnhn
pms\tpms
pmy\tpmy
quz\tquz
sh\tsh
shs\tshs
sml\tsml
szl\tszl
tmp\ttmp
trv\ttrv
vec\tvec
wae\twae
zhs\tzhs
zht\tzht"""

def _opus_to_iso3_map():
    from mtdata.iso.iso639_3 import name_to_code, code_to_name
    from mtdata.iso.iso639_2 import code2_to_code3_name, CODE2_TO_3 as code2_to_3
    mapping = {}
    for line in data.splitlines():
        code, name = line.split('\t')
        iso_name, iso_code = '', ''
        if len(code) == 3 and code_to_name(code, None):
            iso_name = code_to_name(code)
            iso_code = name_to_code(iso_name)
        elif len(code) == 2 and code in code2_to_3:
            iso_code, iso_name = code2_to_code3_name(code)
            iso_code = name_to_code(iso_name) or iso_code
            assert iso_code
        elif name_to_code(name):
            iso_code = name_to_code(name)
        if iso_code and '_' not in code:
            mapping[code] = iso_code
    return mapping


opus_to_iso3 = _opus_to_iso3_map()

if __name__ == '__main__':
    from mtdata.iso.iso639_3 import code_to_name as iso3_code_to_name
    for code, iso_code in opus_to_iso3.items():
        print(f'{code}\t{iso_code}\t{iso3_code_to_name(iso_code)}')
