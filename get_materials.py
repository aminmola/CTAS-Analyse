import caption_cleaner_material as cc
import pandas as pd


def get_materials(caption):
    """input: Caption of an instagram post
    Output: List of material or empty list
    Extract material from a caption and return a list of material id"""
    # clean and tokenize a caption
    df1 = pd.read_csv('material_modified.csv')
    dic = {row['Title']: row['Id'] for index, row in df1.iterrows()}
    cc_arr = cc.clean_caption(caption)

    # try to find word "جنس" in the caption for extracting colors
    material_word = 'جنس'

    if material_word in cc_arr:

        length = min(cc_arr.index(material_word)+10,
                     cc_arr.index(material_word)+(len(cc_arr)-cc_arr.index(material_word)))

        mats_set = {cc_arr[i] for i in range(cc_arr.index(material_word), length) if cc_arr[i] in dic}

        set_ids = {dic[item] for item in mats_set}

        if not set_ids:
            mats_set = {cc_arr[i] for i in range(0, len(cc_arr)) if cc_arr[i] in dic}
            set_ids = {dic[item] for item in mats_set}

        return set_ids

    elif material_word not in cc_arr:

        mats_set = {cc_arr[i] for i in range(0, len(cc_arr)) if cc_arr[i] in dic}
        set_ids = {dic[item] for item in mats_set}

        return set_ids

    else:
        return {}
