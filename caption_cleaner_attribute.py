
import pandas as pd
import re



def remove_emoji(string):
    emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"  # emoticons
                               u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                               u"\U0001F680-\U0001F6FF"  # transport & map symbols
                               u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                               u"\U00002500-\U00002BEF"  # chinese char
                               u"\U00002702-\U000027B0"
                               u"\U00002702-\U000027B0"
                               u"\U000024C2-\U0001F251"
                               u"\U0001f926-\U0001f937"
                               u"\U00010000-\U0010ffff"
                               u"\u2640-\u2642"
                               u"\u2600-\u2B55"
                               u"\u200d"
                               u"\u23cf"
                               u"\u23e9"
                               u"\u231a"
                               u"\ufe0f"  # dingbats
                               u"\u3030"
                               "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r' ', string)


def clean_caption(caption):
    # taking the whole caption and remove extra characters and returning split caption(cleaned_caption)
    if pd.isna(caption):
        return []
    caption = caption.replace('آ', 'ا')
    caption = caption.replace(':', ' ')
    caption = caption.lower()
    caption = re.sub('#(_*[آ-ی0-9a-z_]*_*\s*)', '', caption)
    caption = re.sub('[^A-Za-z0-9آ-ی #@\n/_.]+', '', caption)
    caption_arr = ' '.join(caption.split())
    return caption_arr

