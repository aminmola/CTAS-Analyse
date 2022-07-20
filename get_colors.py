import caption_cleaner_color as cc
import pandas as pd

def get_colors(caption):
    """input: Caption of an instagram post
    Output: List of colors or empty list
    Extract colors from a caption and return a list of colors id"""
    # clean and tokenize a caption
    df1 = pd.read_csv('color_modified.csv')
    dic = {row['color']: row['Id'] for index, row in df1.iterrows()}
    # dictionary for when we have no color word in caption
    new_dic = {key: val for key, val in dic.items() if
                    key not in ['تک', 'دو', 'سه', 'چهار', 'پنج', 'شش', 'هفت', 'هشت', 'ژورنال', 'تصاویر']}
    cc_arr = cc.clean_caption(caption)

    # try to find word "رنگ" in the caption for extracting colors
    color_word = 'رنگ'

    if color_word in cc_arr:

        # calculate the range of words to search for the color
        length = min(cc_arr.index(color_word)+10,
                     cc_arr.index(color_word)+(len(cc_arr)-cc_arr.index(color_word)))

        set_colors = {cc_arr[i] for i in
                      range(cc_arr.index(color_word),
                            length) if cc_arr[i] in dic}

        set_numbers = {cc_arr[cc_arr.index(color_word)-1] if cc_arr[cc_arr.index(color_word)-1] in dic else -1}

        if set_numbers == {-1}:
            set_ids = {dic[item] for item in set_colors}
        else:
            set_ids = set.union({dic[item] for item in set_colors}, {dic[item] for item in set_numbers})

        return set_ids

    elif color_word not in cc_arr:

        set_colors = {cc_arr[i] for i in range(0, len(cc_arr)) if cc_arr[i] in new_dic}
        set_ids = {new_dic[item] for item in set_colors}

        return set_ids

    else:
        return {}
