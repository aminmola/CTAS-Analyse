import pandas as pd
import re
from unidecode import unidecode



def remove_emoji(string) :
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


def clean_caption(caption) :
    if pd.isna(caption) :
        return []
    caption = remove_emoji(caption)
    caption = caption.replace(')', ' ')
    caption = caption.replace('(', ' ')
    caption = caption.replace('t', ' t ')
    caption = caption.replace('T', ' t ')
    caption = caption.replace('=', ' ')
    caption = caption.replace(':', ' ')
    caption = caption.replace(',', '.')
    caption = caption.replace('٬', '.')
    caption = caption.replace('/', '.')
    caption = caption.replace('-', ' الی ')
    caption = caption.replace('_', ' الی ')
    caption = re.split('', caption)
    for i in range(len(caption)) :
        if unidecode(caption[i]).isnumeric() :
            caption[i] = unidecode(caption[i])
    caption = ''.join(caption)
    caption = re.sub('[^A-Za-z0-9آ-ی #@\n/_.]+', '', caption)
    caption = caption.replace('/', '')
    caption = caption.replace('.', '')
    caption = caption.replace('تومان', ' تومن ')
    caption = caption.replace('یورو', ' یورو ')
    caption = caption.replace('تومن', ' تومن ')
    caption = caption.replace('دلار', ' دلار ')
    caption = caption.replace('هزار', ' هزار ')
    caption = caption.replace('بر عهده', 'با')
    caption = caption.replace('به عهده', 'با')
    caption = caption.replace('مرجوع بفرمایید', 'مرجوعی داریم')
    caption = caption.replace('دارند', 'داریم')
    caption = caption.replace('دارد', 'داریم')
    caption = caption.replace('داره', 'داریم')
    caption = caption.replace('پذیرفته می شود', 'داریم')
    caption = caption.replace('مرجوع ', 'مرجوعی')
    caption = caption.replace('ضمانت مرجوعی', 'مرجوعی داریم')
    caption = caption.replace('گارانتی مرجوعی', 'مرجوعی داریم')

    caption = ' '.join(caption.split())
    caption_arr = re.split('[ \n]+', caption)
    return caption_arr

def extract_price(cleaned_caption, index_price_word) :
    """
        Extracts price for one post given the index of the word
        :param cleaned_caption: a list of words in one post
        :param index_price_word: integer
        :return: a data frame of price and unit_price index
    """
    dist_price = 0  # distance between the word 'قیمت' and first number after that
    price = ''
    price_unit = ''

    # Final price and unit
    final_price = -1
    #  تومان -> 1, ریال -> 2, لیر -> 3, دلار -> 4, یورو -> 5, null
    final_price_unit = -1

    # Finding the index of the word 'قیمت'
    # Finding index of the word
    #   'تله' , 'تل' ,'میلیون' ,'تومان', 'هزار', 'ت', 'تومن', 'لیر', 'هزارتومان', 't', 'ریال'
    if 'میلیون' in cleaned_caption :
        index_unit_word = cleaned_caption.index('میلیون')
    elif 'تومان' in cleaned_caption :
        index_unit_word = cleaned_caption.index('تومان')
    elif 'تومن' in cleaned_caption :
        index_unit_word = cleaned_caption.index('تومن')
    elif 'لیر' in cleaned_caption :
        index_unit_word = cleaned_caption.index('لیر')
    elif 'تل' in cleaned_caption :
        index_unit_word = cleaned_caption.index('تل')
    elif 'تله' in cleaned_caption :
        index_unit_word = cleaned_caption.index('تله')
    elif 'هزار' in cleaned_caption :
        index_unit_word = cleaned_caption.index('هزار')
    elif 'ت' in cleaned_caption :
        index_unit_word = cleaned_caption.index('ت')
    elif 'هزارتومان' in cleaned_caption :
        index_unit_word = cleaned_caption.index('هزارتومان')
    elif 'ریال' in cleaned_caption :
        index_unit_word = cleaned_caption.index('ریال')
    elif 't' in cleaned_caption :
        index_unit_word = cleaned_caption.index('t')
    elif 'دلار' in cleaned_caption :
        index_unit_word = cleaned_caption.index('دلار')
    elif 'یورو' in cleaned_caption :
        index_unit_word = cleaned_caption.index('یورو')
    else :
        index_unit_word = -1
    # Finding the first number after the word 'قیمت', In addition, saving the next word as a unit of the price.
    if (index_price_word[0] != -1) and (index_price_word[0] > 0) :
        j = index_price_word[0] + 1
        while j < len(cleaned_caption) and (not cleaned_caption[j].replace('.', '', 1).isnumeric()) :
            j = j + 1
        if j < len(cleaned_caption) :
            price = cleaned_caption[j]

            if (j + 1) < len(cleaned_caption) :
                price_unit = cleaned_caption[j + 1]
            else :
                price_unit = ''
        else :
            price = ''
        dist_price = j - index_price_word[0]
    # print(i, dist_price[i], len(cleaned_caption[i]))
    # print(price[i])

    # Finding price unit among the ones which hasn't "قیمت" in their captions
    if (index_price_word[0] == -1) and (index_unit_word != -1) and (index_unit_word > 0) :
        j = index_unit_word
        while j > 0 and (not cleaned_caption[j].replace('.', '', 1).isnumeric()) :
            j = j - 1
        if j > 0 :
            price = cleaned_caption[j]

        dist_price = index_unit_word - j
    # print(i, dist_price[i], len(cleaned_caption[i]))
    # print(price[i])

    # correcting price among the ones that have the price right before the unit
    if (index_price_word[0] != -2) and (index_price_word[1] != 2) and (index_unit_word != -1) and (
            index_unit_word > 0) :
        j = index_unit_word - 1
        if cleaned_caption[j].isnumeric() :
            price = cleaned_caption[j]
            price_unit = cleaned_caption[index_unit_word]
            dist_price = 1
    # print(i, dist_price[i], len(cleaned_caption[i]))
    # print(price[i])

    # Filtering out incorrect prices
    #  * 1 rd: If the distance between the word 'قیمت' and first number after that is larger than 5,\
    #  it is most probably incorrect.
    #  * 2 rd: Correcting the range of the price.
    #  * 3 rd: removing the prices that are larger than 100000000.\
    #  These are either (1) result of removing a dash between a range of the prices or\
    #  (2) they are phone number instead of the price.

    # 1st filter
    if dist_price > 6 :
        price = ''
        price_unit = ''

    # 2rd filter
    if price.isnumeric() :
        if float(price) < 1000 :
            if price_unit in ['هزار', 'هزارتومان'] :  # a thousand
                final_price = float(price) * 1000
                final_price_unit = 1  # 'تومان'
            elif price_unit in ['میلیون'] and float(price) < 10 :  # a million
                final_price = float(price) * 1000000
                final_price_unit = 1  # 'تومان'
            elif price_unit in ['تومان', 'ت', 'تومن', 't'] and float(price) < 5 :  # Milion
                final_price = float(price) * 1000000
                final_price_unit = 1  # 'تومان'
            elif price_unit in ['ریال'] :
                final_price = float(price) / 10
                final_price_unit = 1  # 'تومان'
            elif price_unit in ['تل', 'تله', 'لیر'] :
                final_price = float(price)
                final_price_unit = 3  # لیر
            elif price_unit in ['دلار'] :
                final_price = float(price)
                final_price_unit = 4  # دلار
            elif price_unit in ['یورو'] :
                final_price = float(price)
                final_price_unit = 5  # یورو
            elif price_unit in ['تومان', 'ت', 'تومن', 't'] and float(price) >= 10 :
                final_price = float(price) * 1000
                final_price_unit = 1  # 'تومان'
            else :
                final_price = float(price) * 1000
                final_price_unit = 1  # 'تومان'
        else :
            final_price = float(price)
            if price_unit in ['هزار', 'هزارتومان'] :
                final_price = float(price)  # * 1000
                final_price_unit = 1  # 'تومان'
            elif price_unit in ['ریال'] :
                final_price = float(price) / 10
                final_price_unit = 1  # 'تومان'
            elif price_unit in ['تل', 'تله', 'لیر'] :
                final_price_unit = 3  # لیر
            elif price_unit in ['دلار'] :
                final_price_unit = 4  # دلار
            elif price_unit in ['یورو'] :
                final_price_unit = 5  # یورو
            else :
                final_price_unit = 1  # 'تومان'

    # 3rd filter
    if final_price > 0 :
        if final_price > 40000000 :
            final_price = -1
            final_price_unit = -1  # ''
        if (final_price < 5000) and (final_price_unit == 1) :
            final_price = -1
            final_price_unit = -1  # ''
    if final_price < 1 :
        final_price = -1
        final_price_unit = -1  # ''
    if (final_price_unit == 3) and (final_price < 5) :
        final_price = -1
        final_price_unit = -1  # ''

    if final_price < 0 or final_price_unit < 0 :
        final_price = ''
        final_price_unit = ''
    return str(final_price), str(final_price_unit)


def extract_index_shipping_word(cleaned_caption) :
    index_shipping_word = -2
    cap = ' '.join(cleaned_caption)
    if 'هزینه پست' in cap :
        cap = cap.replace('هزینه پست', ' mfsdbkl ')
        cap = re.split('[ \n]+', cap)
        index_shipping_word = cap.index('mfsdbkl') + 1
    elif 'هزینه ارسال' in cap :
        cap = cap.replace('هزینه ارسال', ' mfsdbkl ')
        cap = re.split('[ \n]+', cap)
        index_shipping_word = cap.index('mfsdbkl') + 1
    elif 'هزینه پیک' in cap :
        cap = cap.replace('هزینه پیک', ' mfsdbkl ')
        cap = re.split('[ \n]+', cap)
        index_shipping_word = cap.index('mfsdbkl') + 1
    elif 'ارسال' in cleaned_caption :
        cap = cap.replace('ارسال', ' mfsdbkl ')
        cap = re.split('[ \n]+', cap)
        if cap[cap.index('mfsdbkl') + 1].isnumeric() :
            if int(float(cap[cap.index('mfsdbkl') + 1])) % 24 != 0 :
                index_shipping_word = cap.index('mfsdbkl')
    words = ['روزه', 'ساعته', 'دست', 'روز', 'ساعت', 'هفته', 'جفت', 'عدد', 'دست']
    if index_shipping_word != -2 and index_shipping_word + 2 < len(cap) :
        if cap[index_shipping_word + 2] in ['تا', 'الی', 'بالای'] :
            index_shipping_word = index_shipping_word + 2
        elif cap[index_shipping_word + 2] in words :
            index_shipping_word = index_shipping_word + 2
        elif cap[index_shipping_word + 1] in ['یک', 'دو', '1', '2', 'بالای'] :
            index_shipping_word = index_shipping_word + 2

    return index_shipping_word, 2


def dist(cleaned_caption, a, b) :
    if (a in cleaned_caption) and (b in cleaned_caption) :
        if cleaned_caption.index(b) > cleaned_caption.index(a) :
            distance = cleaned_caption.index(b) - cleaned_caption.index(a)
            return distance
        else :
            return 100
    else :
        return 100


def shipping(caption) :
    cleaned_caption = clean_caption(caption)
    cap = ' '.join(cleaned_caption)

    shipping_options = []
    a = 'ارسال'
    b = 'پیشتاز'
    c = 'اسنپ'
    d = 'پست'
    e = 'باکس'
    f = 'پیک'
    if 'تیپاکس' in cleaned_caption:
        shipping_options.append(1)
    if 'الوپیک' in cleaned_caption:
        shipping_options.append(2)
    if dist(cleaned_caption, a, b) < 6 or dist(cleaned_caption, d, b) < 6:
        shipping_options.append(3)
    if dist(cleaned_caption, a, c) < 6 or dist(cleaned_caption, a, e) == 1 or 'اسنپباکس' in cleaned_caption:
        shipping_options.append(4)
    if f in cleaned_caption :
        shipping_options.append(5)
    if dist(cleaned_caption, a, d) < 10 :
        shipping_options.append(6)

    buy_in_person = 0
    a = 'خرید'
    b = 'فروش'
    c = 'حضوری'
    if (dist(cleaned_caption, a, c) < 5) or (dist(cleaned_caption, b, c) < 5) or ('ادرس' in cleaned_caption) :
        buy_in_person = 1

    shipping_cost = ''
    a = 'ارسال'
    b = 'پست'
    c = 'پیک'
    d = 'رایگان'
    if (dist(cleaned_caption, a, d) < 5) or (dist(cleaned_caption, b, d) < 5) or (dist(cleaned_caption, c, d) < 5) :
        shipping_cost = str(0)
    elif 'ارسال رایگان' in ' '.join(cleaned_caption) or 'پست رایگان' in ' '.join(
            cleaned_caption) or 'پیک رایگان' in ' '.join(cleaned_caption) :
        shipping_cost = str(0)
    elif extract_index_shipping_word(cleaned_caption) != -2 :
        my_price = extract_price(cleaned_caption, extract_index_shipping_word(cleaned_caption))
        if my_price[0] != '' and float(my_price[0]) < 65000 :
            shipping_cost = my_price[0]
    elif "هزینه ارسال با مشتری" in cap :
        shipping_cost = str(1)

    shipping_locations = 0
    a = 'ارسال'
    b = 'کشور'
    c = 'ایران'
    d = 'سراسر'
    shipping_phrase = ['ارسال به سراسر نقاط کشور', 'ارسال به تمام نقاط کشور', 'ارسال ب تمام نقاط کشور',
                       'ارسال به سراسر ایران', 'شهرستان']
    for phrase in shipping_phrase :
        if phrase in cap :
            shipping_locations = 1
            break
    if (dist(cleaned_caption, a, b) < 5) or (dist(cleaned_caption, a, c) < 5) or (dist(cleaned_caption, d, b) < 5) :
        shipping_locations = 1
    return_option = 0
    if "مرجوعی" in cleaned_caption:
        return_option = 1
    change_option = 0
    if "تعویض" in cleaned_caption:
        change_option = 1

    return buy_in_person, shipping_cost, shipping_locations, shipping_options, return_option, change_option
