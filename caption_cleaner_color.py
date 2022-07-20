import re


def get_stop_words():
    """
    output: stopwords (List)
    This function read a file of Persian stop words (persian) and return it as a list.
    """
    # read from file
    with open('persian_color', encoding='utf-8') as f:
        content = f.read()
        # create list
        stop_words = content.split()
    return stop_words


def remove_hashtags(caption: str):
    """
    input: original caption (String)
    output: caption without hashtags (String)
    Extract pure caption and remove hashtags.
    """
    caption = re.sub('#(_*[آ-ی0-9]*_*\s*)*', '', caption)
    return caption


def remove_emoji(caption: str):
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
    return emoji_pattern.sub(r' ', caption)


def clean_caption(caption: str):
    """
            input: original caption without hashtags or a search term (String)
            output: tokenized cleaned caption (List)
            Punctuations, emojis, extra spaces and ... are removed.
            Some words are replaced for easy finding similar words.
            """

    stop_words = get_stop_words()

    caption = remove_hashtags(caption)

    caption = caption.replace(':', ' ')
    caption = caption.replace(',', '')
    caption = caption.replace('ـ', '')
    caption = caption.replace('_', '')
    caption = caption.replace('،', '')
    #caption = re.sub('[A-Za-z\n]+', '', caption)

    # replacing similar words and handling two words color
    caption = re.sub(r'\bسورمه ای\b', 'سرمه', caption)
    caption = re.sub(r'\bسرمه ای\b', 'سرمه', caption)
    caption = re.sub(r'\bسورمه\b', 'سرمه', caption)

    # handling blue colors
    caption = re.sub(r'\bابی\b', 'آبی', caption)
    caption = re.sub(r'\bآبی آسمانی\b', 'آبیاس', caption)
    caption = re.sub(r'\bآبی روشن\b', 'آبیرو', caption)
    caption = re.sub(r'\bآبی روشن\b', 'آبیرو', caption)
    caption = re.sub(r'\bآبی نفتی\b', 'آبینف', caption)
    caption = re.sub(r'\bآبی فیروزه ای\b', 'آبیفیرو', caption)
    caption = re.sub(r'\bآبی کاربنی\b', 'آبیکار', caption)
    caption = re.sub(r'\bآبی کمرنگ\b', 'آبیکم', caption)

    # handling green colors
    caption = re.sub(r'\bسبز روشن\b', 'سبزروش', caption)
    caption = re.sub(r'\bسبز ارتشی\b', 'سبزار', caption)
    caption = re.sub(r'\bسبز آبی\b', 'سبزاب', caption)
    caption = re.sub(r'\bسبز کله غازی\b', 'سبزکلغ', caption)
    caption = re.sub(r'\bآبی آسمانی\b', 'آبیاس', caption)

    # handling gray colors
    caption = re.sub(r'\bتوسی\b', 'طوسی', caption)
    caption = re.sub(r'\bطوسی روشن\b', 'طوسیرو', caption)
    caption = re.sub(r'\bطوسی تیره\b', 'طوسیتی', caption)

    # handling other colors
    caption = re.sub(r'\bسرخ آبی\b', 'سرخابی', caption)
    caption = re.sub(r'\bفیروزه ای\b', 'فیروزا', caption)
    caption = re.sub(r'\bقهوه ای\b', 'قهوه', caption)
    caption = re.sub(r'\bگوجه ای\b', 'گوجا', caption)
    caption = re.sub(r'\bنقره ای\b', 'نقرا', caption)
    caption = re.sub(r'\bنوک مدادی\b', 'نوکمدادی', caption)
    caption = re.sub(r'\bمدادی\b', 'نوکمدادی', caption)
    caption = re.sub(r'\bپوست پیازی\b', 'پوستپیاز', caption)
    caption = re.sub(r'\bنسکافه ای\b', 'نسکافا', caption)
    caption = re.sub(r'\bکرم\b', 'کرمی', caption)
    caption = re.sub(r'\bسیاه\b', 'مشکی', caption)
    caption = re.sub(r'\bبادمجونی\b', 'بادمجانی', caption)

    # handling the word "رنگ"
    caption = re.sub(r'\bرنگبندی\b', 'رنگ', caption)
    caption = re.sub(r'\bرنگ بندی\b', 'رنگ', caption)
    caption = re.sub(r'\bرنکبندی\b', 'رنگ', caption)
    caption = re.sub(r'\b1 رنگ\b', 'تک رنگ', caption)
    caption = re.sub(r'\b2 رنگ\b', 'دو رنگ', caption)
    caption = re.sub(r'\b3 رنگ\b', 'سه رنگ', caption)
    caption = re.sub(r'\b4 رنگ\b', 'چهار رنگ', caption)
    caption = re.sub(r'\b5 رنگ\b', 'پنج رنگ', caption)
    caption = re.sub(r'\b6 رنگ\b', 'شش رنگ', caption)
    caption = re.sub(r'\b7 رنگ\b', 'هفت رنگ', caption)
    caption = re.sub(r'\b8 رنگ\b', 'هشت رنگ', caption)
    caption = re.sub(r'\b9 رنگ\b', 'نه رنگ', caption)
    caption = re.sub(r'\bرنگ\u200cهای\b', 'رنگ', caption)

    # handling similar words
    caption = re.sub(r'\bتصویر\b', 'تصاویر', caption)
    caption = re.sub(r'\bعکس\b', 'تصاویر', caption)
    #caption = re.sub(r'\bپست\b', 'تصاویر', caption)

    # finally, remove emojis from caption
    caption = remove_emoji(caption)

    # tokenizing
    caption_arr = re.split('[ \n]+', caption)

    caption_arr = [word for word in caption_arr if word not in stop_words]

    return caption_arr
