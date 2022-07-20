import re
import pandas as pd


def remove_emoji(string):

    emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"  # emoticons
                               u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                               u"\U0001F680-\U0001F6FF"  # transport & map symbols
                               u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                               u"\U00002500-\U00002BEF"  # chinese char
                               u"\U00002702-\U000027B0"
                               u"\U00002702-\U000027B0"
                               #  u"\U000024C2-\U0001F251"
                               u"\U0001f926-\U0001f937"
                               u"\U00010000-\U0010ffff"
                               u"\u2640-\u2642"
                               u"\u2600-\u2B55"
                               u"\u200d"
                               u"\u23cf"
                               u"\u23e9"
                               u"\u231a"
                               #  u"\ufe0f"  # dingbats """Bold Chars"""
                               u"\u3030"
                               "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r' ', string)


def remove_hashtags(caption):

    # taking the caption and remove its hashtags
    caption = re.sub('#(_*[آ-ی0-9]*_*\s*)', '', caption)
    return caption


def clean_caption(caption):

    # taking the whole caption and remove extra characters and returning split caption(cleaned_caption)
    if pd.isna(caption):
        # print('1')
        return []

    caption = remove_emoji(caption)
    caption = caption.replace('t', ' t ')
    caption = caption.replace('=', ' ')
    caption = caption.replace('_', ' ')
    caption = caption.replace('آ', 'ا')
    caption = caption.replace(':', ' ')
    caption = caption.replace(',', '.')
    caption = caption.replace('/', '.')
    if ('دلار' in re.split('[ \n]+', caption)) or ('یورو' in re.split('[ \n]+', caption)) \
            or ('لیر' in re.split('[ \n]+', caption)):
        cap = re.split('[ \n]+', caption)
        indices = [i for i, x in enumerate(re.split('[ \n]+', caption)) if x == "دلار"]
        if indices:
            for i in indices:
                if cap[i - 1].replace('.', '', 1).isnumeric():
                    caption = re.split('[ \n]+', caption)
                    caption[i - 1] = str(round(float(caption[i - 1])))
                    caption = ' '.join(caption)

        indices = [i for i, x in enumerate(re.split('[ \n]+', caption)) if x == "لیر"]
        if indices:
            for i in indices:
                if cap[i - 1].replace('.', '', 1).isnumeric():
                    caption = re.split('[ \n]+', caption)
                    caption[i - 1] = str(round(float(caption[i - 1])))
                    caption = ' '.join(caption)
        indices = [i for i, x in enumerate(re.split('[ \n]+', caption)) if x == "یورو"]
        if indices:
            for i in indices:
                if cap[i - 1].replace('.', '', 1).isnumeric():
                    caption = re.split('[ \n]+', caption)
                    caption[i - 1] = str(round(float(caption[i - 1])))
                    caption = ' '.join(caption)
    caption = re.sub('[^A-Za-z0-9آ-ی #@\n/_.]+', '', caption)
    caption = caption.replace('.', '')
    caption = re.sub('#(_*[آ-ی0-9]*_*\s*)', '', caption)
    caption = ' '.join(caption.split())
    caption_arr = re.split('[ \n]+', caption)

    return caption_arr



