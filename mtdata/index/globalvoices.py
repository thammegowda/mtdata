#!/usr/bin/env python
#
# Author: Thamme Gowda [tg (at) isi (dot) edu] 
# Created: 5/10/20
from mtdata.index import Index, Entry


def load_all(index: Index):
    data = """am-en am-fr ar-am ar-en ar-fr aym-am aym-ar aym-en aym-fr bg-ar bg-aym bg-en bg-fr
  bn-am bn-ar bn-aym bn-bg bn-en bn-fr ca-am ca-ar ca-aym ca-bg ca-bn ca-en ca-fr cs-ar cs-aym 
  cs-bg cs-bn cs-ca cs-en cs-fr da-am da-ar da-aym da-bg da-bn da-ca da-cs da-en da-fr de-am 
  de-ar de-aym de-bg de-bn de-ca de-cs de-da de-en de-fr el-am el-ar el-aym el-bg el-bn el-ca
  el-cs el-da el-de el-en el-fr eo-ar eo-aym eo-bg eo-bn eo-ca eo-cs eo-da eo-de eo-el eo-en
  eo-fr es-am es-ar es-aym es-bg es-bn es-ca es-cs es-da es-de es-el es-en es-eo es-fr fa-am
  fa-ar fa-aym fa-bg fa-bn fa-ca fa-cs fa-da fa-de fa-el fa-en fa-eo fa-es fa-fr fil-ar fil-aym
  fil-bg fil-bn fil-ca fil-cs fil-da fil-de fil-el fil-en fil-eo fil-es fil-fa fil-fr fr-en he-ar
   he-bn he-ca he-cs he-da he-de he-el he-en he-es he-fa he-fr hi-am hi-ar hi-bg hi-bn hi-cs hi-de
   hi-el hi-en hi-eo hi-es hi-fa hi-fr hu-am hu-ar hu-aym hu-bg hu-bn hu-ca hu-cs hu-da hu-de
   hu-el hu-en hu-eo hu-es hu-fa hu-fil hu-fr hu-hi id-am id-ar id-aym id-bg id-bn id-ca id-cs 
   id-da id-de id-el id-en id-eo id-es id-fa id-fil id-fr id-hi id-hu it-am it-ar it-aym it-bg it-bn 
   it-ca it-cs it-da it-de it-el it-en it-eo it-es it-fa it-fil it-fr it-he it-hi it-hu it-id jp-am 
   jp-ar jp-aym jp-bg jp-bn jp-ca jp-cs jp-da jp-de jp-el jp-en jp-eo jp-es jp-fa jp-fil jp-fr 
   jp-he jp-hi jp-hu jp-id jp-it km-ar km-aym km-bn km-ca km-da km-de km-el km-en km-es km-fa km-fil 
   km-fr km-hu km-it km-jp ko-am ko-ar ko-aym ko-bg ko-bn ko-ca ko-cs ko-da ko-de ko-el ko-en ko-eo 
   ko-es ko-fa ko-fil ko-fr ko-hu ko-id ko-it ko-jp ku-ar ku-el ku-en ku-es ku-fr ku-it ku-jp mg-am 
   mg-ar mg-aym mg-bg mg-bn mg-ca mg-cs mg-da mg-de mg-el mg-en mg-eo mg-es mg-fa mg-fil mg-fr 
   mg-he mg-hi mg-hu mg-id mg-it mg-jp mg-km mg-ko mg-ku mk-am mk-ar mk-aym mk-bg mk-bn mk-ca mk-cs 
   mk-da mk-de mk-el mk-en mk-eo mk-es mk-fa mk-fil mk-fr mk-he mk-hi mk-hu mk-id mk-it mk-jp mk-km 
   mk-ko mk-mg my-am my-ar my-aym my-bg my-bn my-ca my-cs my-da my-de my-el my-en my-es my-fa my-fil 
   my-fr my-he my-hi my-hu my-id my-it my-jp my-ko my-mg my-mk ne-ar ne-aym ne-bg ne-bn ne-ca ne-cs 
   ne-de ne-el ne-en ne-eo ne-es ne-fa ne-fr ne-hi ne-id ne-it ne-jp ne-ko ne-mg ne-mk nl-am nl-ar 
   nl-aym nl-bg nl-bn nl-ca nl-cs nl-da nl-de nl-el nl-en nl-eo nl-es nl-fa nl-fil nl-fr nl-he nl-hi 
   nl-hu nl-id nl-it nl-jp nl-km nl-ko nl-mg nl-mk nl-my nl-ne or-ar or-aym or-bn or-ca or-cs or-de 
   or-el or-en or-es or-fa or-fr or-hi or-it or-jp or-mg or-mk or-nl pa-ar pa-bn pa-ca pa-cs pa-de 
   pa-el pa-en pa-es pa-fr pa-hi pa-hu pa-it pa-jp pa-ko pa-mg pa-mk pa-ne pa-nl pl-am pl-ar pl-aym 
   pl-bg pl-bn pl-ca pl-cs pl-da pl-de pl-el pl-en pl-eo pl-es pl-fa pl-fil pl-fr pl-he pl-hi pl-hu 
   pl-id pl-it pl-jp pl-ko pl-ku pl-mg pl-mk pl-my pl-ne pl-nl pl-or pl-pa pt-am pt-ar pt-aym pt-bg 
   pt-bn pt-ca pt-cs pt-da pt-de pt-el pt-en pt-eo pt-es pt-fa pt-fil pt-fr pt-he pt-hi pt-hu pt-id 
   pt-it pt-jp pt-km pt-ko pt-ku pt-mg pt-mk pt-my pt-ne pt-nl pt-or pt-pa pt-pl ro-ar ro-aym ro-bg 
   ro-bn ro-ca ro-cs ro-de ro-el ro-en ro-eo ro-es ro-fa ro-fr ro-hu ro-id ro-it ro-jp ro-ko ro-ku 
   ro-mg ro-mk ro-my ro-ne ro-nl ro-pl ro-pt ru-am ru-ar ru-aym ru-bg ru-bn ru-ca ru-cs ru-da ru-de 
   ru-el ru-en ru-eo ru-es ru-fa ru-fil ru-fr ru-he ru-hi ru-hu ru-id ru-it ru-jp ru-km ru-ko ru-mg 
   ru-mk ru-my ru-ne ru-nl ru-or ru-pa ru-pl ru-pt ru-ro sq-am sq-ar sq-aym sq-bg sq-bn sq-ca sq-cs 
   sq-da sq-de sq-el sq-en sq-eo sq-es sq-fa sq-fil sq-fr sq-hi sq-hu sq-id sq-it sq-jp sq-ko sq-mg 
   sq-mk sq-my sq-nl sq-pl sq-pt sq-ru sr-am sr-ar sr-aym sr-bg sr-bn sr-ca sr-cs sr-da sr-de sr-el 
   sr-en sr-eo sr-es sr-fa sr-fil sr-fr sr-hi sr-hu sr-id sr-it sr-jp sr-km sr-ko sr-mg sr-mk sr-my 
   sr-ne sr-nl sr-pl sr-pt sr-ro sr-ru sr-sq sv-am sv-ar sv-aym sv-bg sv-bn sv-ca sv-cs sv-da sv-de 
   sv-el sv-en sv-eo sv-es sv-fa sv-fil sv-fr sv-he sv-hi sv-hu sv-id sv-it sv-jp sv-ko sv-mg sv-mk 
   sv-my sv-nl sv-pl sv-pt sv-ro sv-ru sv-sq sv-sr sw-am sw-ar sw-aym sw-bg sw-bn sw-ca sw-cs sw-da 
   sw-de sw-el sw-en sw-eo sw-es sw-fa sw-fil sw-fr sw-he sw-hi sw-hu sw-id sw-it sw-jp sw-km sw-ko 
   sw-mg sw-mk sw-my sw-ne sw-nl sw-pa sw-pl sw-pt sw-ro sw-ru sw-sq sw-sr sw-sv tet-ar tet-aym 
   tet-bn tet-cs tet-de tet-el tet-en tet-es tet-fr tet-id tet-it tet-mg tet-pt tet-ru tet-sw tr-am 
   tr-ar tr-aym tr-bg tr-bn tr-ca tr-cs tr-da tr-de tr-el tr-en tr-eo tr-es tr-fa tr-fil tr-fr tr-he 
   tr-hi tr-hu tr-id tr-it tr-jp tr-ko tr-mg tr-mk tr-my tr-ne tr-nl tr-pa tr-pl tr-pt tr-ro tr-ru 
   tr-sq tr-sr tr-sv tr-sw ur-am ur-ar ur-aym ur-bg ur-bn ur-ca ur-cs ur-da ur-de ur-el ur-en ur-eo 
   ur-es ur-fa ur-fil ur-fr ur-he ur-hi ur-hu ur-id ur-it ur-jp ur-ko ur-mg ur-mk ur-my ur-ne ur-nl 
   ur-or ur-pa ur-pl ur-pt ur-ro ur-ru ur-sq ur-sr ur-sv ur-sw ur-tr yo-ar yo-el yo-en yo-es yo-fr 
   yo-it yo-mg yo-pl yo-pt yo-ru yo-sw zhs-am zhs-ar zhs-aym zhs-bg zhs-bn zhs-ca zhs-cs zhs-da 
   zhs-de zhs-el zhs-en zhs-eo zhs-es zhs-fa zhs-fil zhs-fr zhs-he zhs-hi zhs-hu zhs-id zhs-it 
   zhs-jp zhs-km zhs-ko zhs-mg zhs-mk zhs-my zhs-ne zhs-nl zhs-pa zhs-pl zhs-pt zhs-ro zhs-ru 
   zhs-sq zhs-sr zhs-sv zhs-sw zhs-tr zhs-ur zht-am zht-ar zht-aym zht-bg zht-bn zht-ca zht-cs 
   zht-da zht-de zht-el zht-en zht-eo zht-es zht-fa zht-fil zht-fr zht-he zht-hi zht-hu zht-id 
   zht-it zht-jp zht-km zht-ko zht-mg zht-mk zht-my zht-ne zht-nl zht-pa zht-pl zht-pt zht-ro 
   zht-ru zht-sq zht-sr zht-sv zht-sw zht-tet zht-tr zht-ur zht-zhs"""
    url = 'http://casmacat.eu/corpus/global-voices-tar-balls/training.tgz'
    cite = """Philipp Koehn, "Global Voices Corpus" http://casmacat.eu/corpus/global-voices.html """

    # any hot fixes for lang id mapping specific to this source
    code_map = {
        'jp': 'jpn', # there was never a jp in ISO 693, it was always a 'ja' not 'jp'
        'zhs': 'zho'  # map simplified to chinese
     }
    code_map = code_map.get
    for pair in data.split():
        if 'zht' in pair:
            continue  #skipping traditional chinese because I dont know the ISO code for it
        l1, l2 = pair.split('-')
        f1 = f'training/globalvoices.{l1}-{l2}.{l1}'
        f2 = f'training/globalvoices.{l1}-{l2}.{l2}'
        l1, l2 = code_map(l1, l1), code_map(l2, l2)  # map codes
        ent = Entry(langs=(l1, l2), name='GlobalVoices_2018Q4', url=url,
                    filename='GlobalVoices_2018Q4-training.tgz', in_ext='txt', cite=cite,
                    in_paths=[f1, f2])
        index.add_entry(ent)
