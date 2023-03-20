# AllenAi version of NLLB dataset
# Originally published on HF dataset hub https://huggingface.co/datasets/allenai/nllb

from mtdata.index import Index, Entry, DatasetId
import itertools
from pathlib import Path

_FLORES200_URL = "https://tinyurl.com/flores200dataset"
_LICENSE = "https://creativecommons.org/licenses/by-sa/4.0/"
_FLORES200_LANGS = ("ace_Arab ace_Latn acm_Arab acq_Arab aeb_Arab afr_Latn ajp_Arab aka_Latn als_Latn amh_Ethi"
    " apc_Arab arb_Arab arb_Latn ars_Arab ary_Arab arz_Arab asm_Beng ast_Latn awa_Deva ayr_Latn azb_Arab azj_Latn"
    " bak_Cyrl bam_Latn ban_Latn bel_Cyrl bem_Latn ben_Beng bho_Deva bjn_Arab bjn_Latn bod_Tibt bos_Latn bug_Latn"
    " bul_Cyrl cat_Latn ceb_Latn ces_Latn cjk_Latn ckb_Arab crh_Latn cym_Latn dan_Latn deu_Latn dik_Latn dyu_Latn"
    " dzo_Tibt ell_Grek eng_Latn epo_Latn est_Latn eus_Latn ewe_Latn fao_Latn fij_Latn fin_Latn fon_Latn fra_Latn"
    " fur_Latn fuv_Latn gaz_Latn gla_Latn gle_Latn glg_Latn grn_Latn guj_Gujr hat_Latn hau_Latn heb_Hebr hin_Deva"
    " hne_Deva hrv_Latn hun_Latn hye_Armn ibo_Latn ilo_Latn ind_Latn isl_Latn ita_Latn jav_Latn jpn_Jpan kab_Latn"
    " kac_Latn kam_Latn kan_Knda kas_Arab kas_Deva kat_Geor kaz_Cyrl kbp_Latn kea_Latn khk_Cyrl khm_Khmr kik_Latn"
    " kin_Latn kir_Cyrl kmb_Latn kmr_Latn knc_Arab knc_Latn kon_Latn kor_Hang lao_Laoo lij_Latn lim_Latn lin_Latn"
    " lit_Latn lmo_Latn ltg_Latn ltz_Latn lua_Latn lug_Latn luo_Latn lus_Latn lvs_Latn mag_Deva mai_Deva mal_Mlym"
    " mar_Deva min_Arab min_Latn mkd_Cyrl mlt_Latn mni_Beng mos_Latn mri_Latn mya_Mymr nld_Latn nno_Latn nob_Latn"
    " npi_Deva nso_Latn nus_Latn nya_Latn oci_Latn ory_Orya pag_Latn pan_Guru pap_Latn pbt_Arab pes_Arab plt_Latn"
    " pol_Latn por_Latn prs_Arab quy_Latn ron_Latn run_Latn rus_Cyrl sag_Latn san_Deva sat_Olck scn_Latn shn_Mymr"
    " sin_Sinh slk_Latn slv_Latn smo_Latn sna_Latn snd_Arab som_Latn sot_Latn spa_Latn srd_Latn srp_Cyrl ssw_Latn"
    " sun_Latn swe_Latn swh_Latn szl_Latn tam_Taml taq_Latn taq_Tfng tat_Cyrl tel_Telu tgk_Cyrl tgl_Latn tha_Thai"
    " tir_Ethi tpi_Latn tsn_Latn tso_Latn tuk_Latn tum_Latn tur_Latn twi_Latn tzm_Tfng uig_Arab ukr_Cyrl umb_Latn"
    " urd_Arab uzn_Latn vec_Latn vie_Latn war_Latn wol_Latn xho_Latn ydd_Hebr yor_Latn yue_Hant zho_Hans zho_Hant"
    " zsm_Latn zul_Latn").split()
_FLORES101_URL = "https://dl.fbaipublicfiles.com/flores101/dataset/flores101_dataset.tar.gz"
_FLORES101_LANGS = ("afr amh ara asm ast azj bel ben bos bul cat ceb ces ckb cym dan deu ell eng est fas fin fra ful gle"
    " glg guj hau heb hin hrv hun hye ibo ind isl ita jav jpn kam kan kat kaz kea khm kir kor lao lav lin lit ltz lug"
    " luo mal mar mkd mlt mon mri msa mya nld nob npi nso nya oci orm ory pan pol por pus ron rus slk slv sna snd som"
    " spa srp swe swh tam tel tgk tgl tha tur ukr umb urd uzb vie wol xho yor zho_Hans zho_Hant zul").split()

def ad_hoc_fix(lang):
    # Flores-200 uses "arb" code in place of "ara"
    if lang == "arb_Arab":
        return "ara_Arab"
    else:
        return lang


def load_all(index: Index):

    # these bib keys are as per listed on https://github.com/facebookresearch/flores/tree/main/flores200
    bibkeys = ("nllb-2022", "goyal2021", "guzman2019")

    for i, lang1 in enumerate(_FLORES200_LANGS):
        for lang2 in _FLORES200_LANGS[i + 1 :]:
            # Fixin some language codes
            l1, l2 = ad_hoc_fix(lang1), ad_hoc_fix(lang2)
            # dev set
            index += Entry(
                did=DatasetId(group="Flores", name="flores200_dev", version="1", langs=(l1, l2)),
                cite=bibkeys,
                ext="tar.gz",
                url=_FLORES200_URL,
                filename="flores200_dataset.tar.gz",
                in_ext="txt",
                in_paths=[f"flores200_dataset/dev/{lang1}.dev", f"flores200_dataset/dev/{lang2}.dev"],
            )

            # devtest set
            index += Entry(
                did=DatasetId(group="Flores", name="flores200_devtest", version="1", langs=(l1, l2)),
                cite=bibkeys,
                ext="tar.gz",
                url=_FLORES200_URL,
                filename="flores200_dataset.tar.gz",
                in_ext="txt",
                in_paths=[f"flores200_dataset/devtest/{lang1}.devtest", f"flores200_dataset/devtest/{lang2}.devtest"],
            )
    for i, l1 in enumerate(_FLORES101_LANGS):
        for l2 in _FLORES101_LANGS[i + 1 :]:
            # dev set
            index += Entry(
                did=DatasetId(group="Flores", name="flores101_dev", version="1", langs=(l1, l2)),
                cite=bibkeys, ext="tar.gz", url=_FLORES101_URL, filename="flores101_dataset.tar.gz",
                in_ext="txt", in_paths=[f"flores101_dataset/dev/{lang1}.dev", f"flores101_dataset/dev/{lang2}.dev"])
            # devtest set
            index += Entry(
                did=DatasetId(group="Flores", name="flores101_devtest", version="1", langs=(l1, l2)),
                cite=bibkeys, ext="tar.gz", url=_FLORES101_URL, filename="flores101_dataset.tar.gz",
                in_ext="txt", in_paths=[f"flores101_dataset/dev/{lang1}.dev", f"flores101_dataset/dev/{lang2}.dev"],
            )
