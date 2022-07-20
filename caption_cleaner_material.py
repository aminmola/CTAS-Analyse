import re


def get_stop_words():
    """
    output: stopwords (List)
    This function read a file of Persian stop words (persian) and return it as a list.
    """
    # read from file
    with open('persian_material.txt', encoding='utf-8') as f:
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

    ### replacing similar words and handling two words material

    # handling کرپ material
    caption = re.sub(r'\bکرپ اسکاچی\b', 'کرپاسکاچ', caption)
    caption = re.sub(r'\bکرپ فلورانس\b', 'کرپفلور', caption)
    caption = re.sub(r'\bکرپ ژرژت\b', 'کرپژرژ', caption)
    caption = re.sub(r'\bکرپ کش\b', 'کرپکش', caption)
    caption = re.sub(r'\bکرپ باربی\b', 'کرپبارب', caption)
    caption = re.sub(r'\bکرپ مازراتی\b', 'کرپمازرا', caption)
    caption = re.sub(r'\bکرپ دیور\b', 'کرپدیور', caption)
    caption = re.sub(r'\bکرپ گاباردین\b', 'کرپگابار', caption)
    caption = re.sub(r'\bکرپ کاترینا\b', 'کرپکاترین', caption)
    caption = re.sub(r'\bکرپ مقنعه ای\b', 'کرپمق', caption)
    caption = re.sub(r'\bکرپ می سی نو\b', 'کرپمیسینو', caption)
    caption = re.sub(r'\bکرپ گلنس\b', 'کرپگلنس', caption)
    caption = re.sub(r'\bکرپ فرانسوی\b', 'کرپفرانس', caption)
    caption = re.sub(r'\bکرپ غواصی\b', 'کرپغواص', caption)
    caption = re.sub(r'\bکرپ پلاس\b', 'کرپلاس', caption)
    caption = re.sub(r'\bکرپ کریشه\b', 'کرپکریش', caption)
    caption = re.sub(r'\bکرپ بوگاتی\b', 'کربوگات', caption)
    caption = re.sub(r'\bکرپ میشل\b', 'کرمیشل', caption)
    caption = re.sub(r'\bکرپ گریت\b', 'کرگریت', caption)
    caption = re.sub(r'\bکرپ جودون\b', 'کرپجودو', caption)
    caption = re.sub(r'\bکرپ یاخما\b', 'کریاخما', caption)
    caption = re.sub(r'\bکرپ شنی\b', 'کرشنی', caption)
    caption = re.sub(r'\bکرپ حریر\b', 'کرپحر', caption)

    # handling ملانژ material
    caption = re.sub(r'\bملانژ خاویاری\b', 'ملانژخاویار', caption)
    caption = re.sub(r'\bملانژ پنبه\b', 'ملانژپنبه', caption)

    # handling کریشه material
    caption = re.sub(r'\bکریشه پفکی\b', 'کریشپفک', caption)
    caption = re.sub(r'\bکریشه نخی\b', 'کریشنخ', caption)

    # handling پنبه material
    caption = re.sub(r'\bپنبه کش\b', 'پنبکش', caption)
    caption = re.sub(r'\bپنبه لاکرا\b', 'پنلاک', caption)
    caption = re.sub(r'\bپنبه ویسکوز\b', 'پنویسکو', caption)

    # handling چرم material
    caption = re.sub(r'\bچرم مصنوعی\b', 'چرمصنوع', caption)
    caption = re.sub(r'\bچرم بیاله\b', 'چرمبیاله', caption)
    caption = re.sub(r'\bچرم حوله ای\b', 'چرمحوله', caption)
    caption = re.sub(r'\bچرم صنعتی\b', 'چرمصنعت', caption)

    # handling نخ material
    caption = re.sub(r'\bنخ پنبه\b', 'نخپنبه', caption)
    caption = re.sub(r'\bنخ بامبو\b', 'نخبامبو', caption)
    caption = re.sub(r'\bنخ استرچ\b', 'نخاسترچ', caption)
    caption = re.sub(r'\bنخی سنگشور\b', 'نخیسنگ', caption)
    caption = re.sub(r'\bنخ سنگشور\b', 'نخیسنگ', caption)
    caption = re.sub(r'\bنخی\b', 'نخ', caption)
    caption = re.sub(r'\bنخ اکرولیک\b', 'نخاکرولیک', caption)
    caption = re.sub(r'\bنخ ملانژ\b', 'نخملانژ', caption)
    caption = re.sub(r'\bنخ ژاکارد\b', 'نخژاکارد', caption)

    # handling مخمل material
    caption = re.sub(r'\bمخمل سوییت\b', 'مخسوییت', caption)
    caption = re.sub(r'\bمخمل کبریتی\b', 'مخکبریتی', caption)

    # handling کرکی material
    caption = re.sub(r'\bکرکی\b', 'توکرکی', caption)

    # handling لمه material
    caption = re.sub(r'\bلمه سیمی\b', 'لمسیمی', caption)
    caption = re.sub(r'\bسوپر لمه\b', 'سوپرلمه', caption)
    caption = re.sub(r'\bلمه بیزو\b', 'لمبیزو', caption)

    # handling کتان material
    caption = re.sub(r'\bکتون\b', 'کتان', caption)
    caption = re.sub(r'\bکتان کش\b', 'کتکش', caption)
    caption = re.sub(r'\bکتان پنبه\b', 'کتپنبه', caption)

    # handling other materials
    caption = re.sub(r'\bسوپر سافت\b', 'سوپرسافت', caption)
    caption = re.sub(r'\bحوله ای\b', 'حولا', caption)
    caption = re.sub(r'\bتور کش\b', 'تورکش', caption)
    caption = re.sub(r'\bتور کشی\b', 'تورکش', caption)
    caption = re.sub(r'\bابر و بادی\b', 'ابروبادی', caption)
    caption = re.sub(r'\bابرو بادی\b', 'ابروبادی', caption)
    caption = re.sub(r'\bابر وبادی\b', 'ابروبادی', caption)
    caption = re.sub(r'\bابروباد\b', 'ابروبادی', caption)
    caption = re.sub(r'\bوال اسلپ\b', 'والاسپ', caption)
    caption = re.sub(r'\bمیکرو جودون\b', 'میکروجودون', caption)
    caption = re.sub(r'\bغواصی گلاسکو\b', 'غواصیگلاس', caption)
    caption = re.sub(r'\bداکرون میله ای\b', 'داکرومیل', caption)
    caption = re.sub(r'\bجین کاغذی\b', 'جینکاغذ', caption)
    caption = re.sub(r'\bکانیوم ترک\b', 'کانیترک', caption)
    caption = re.sub(r'\bفانریپ کش\b', 'فانکش', caption)
    caption = re.sub(r'\bفانریپ کشی\b', 'فانکش', caption)
    caption = re.sub(r'\bجودون کشی\b', 'جودونکش', caption)
    caption = re.sub(r'\bجودون کش\b', 'جودونکش', caption)
    caption = re.sub(r'\bگیپور نشمیل\b', 'گیپنشمیل', caption)
    caption = re.sub(r'\bبنگال کش\b', 'بنگالکش', caption)
    caption = re.sub(r'\bبنگال کشی\b', 'بنگالکش', caption)
    caption = re.sub(r'\bاماس\b', 'آماس', caption)
    caption = re.sub(r'\bلنین\b', 'لینن', caption)
    caption = re.sub(r'\bاسترچ\b', 'استرج', caption)
    caption = re.sub(r'\bفیلامنت\b', 'فلامنت', caption)
    caption = re.sub(r'\bپارچه ای\b', 'پارچهای', caption)
    caption = re.sub(r'\bدورس ملانژ\b', 'دورسملانژ', caption)

    # finally, remove emojis from caption
    caption = remove_emoji(caption)

    # tokenizing
    caption_arr = re.split('[ \n]+', caption)

    caption_arr = [word for word in caption_arr if word not in stop_words]

    return caption_arr
