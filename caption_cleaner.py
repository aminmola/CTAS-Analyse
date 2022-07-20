import re


def get_stop_words():
    """
    output: stopwords (List)
    This function read a file of Persian stop words (persian) and return it as a list.
    """
    # read from file
    with open('persian', encoding='utf-8') as f:
        content = f.read()
        # create list
        stop_words = content.split()
    return stop_words


def get_max_appearance(words: list):
    """
    input: all words in hashtags (List)
    output: the word with maximum appearance in hashtag (String), its number of appearance (Integer)
    This function gets a list of hashtags which are tokenized, and search for the word with maximum appearance. We use
    this word for finding the category
    """
    # create a dict for keeping each word and its counter
    counts = dict()

    # iteration over words to add them to dictionary or adding their counter
    for word in words:
        if word in counts:
            counts[word] += 1
        else:
            counts[word] = 1

    # get the word with maximum appearance
    maxim_word = max(counts, key=counts.get)
    # get the count of word with maximum appearance
    maxim_count = counts[maxim_word]

    return maxim_word, maxim_count

def remove_hashtags(caption: str):
    """
    input: original caption (String)
    output: caption without hashtags (String), a word with maximum appearance in hashtags (String)
    Extract pure caption and remove hashtags, also getting a keyword from hashtags which have the most occurrence in it.
    """
    # this probability can change
    percent_of_key_word = 0.4

    # get hashtags
    h = [x.group() for x in re.finditer('#(_*[a-zآ-ی0-9]*_*\s*)*', caption)]
    if h:
        hashtag_num = len(h)
    # print(h)
    # print(caption)
    # remove # and _ from hashtags
        h = [re.sub('#', '', x) for x in h]
        h = [re.sub('_', ' ', x) for x in h]
        # tokenizing hashtags
        h = [x.split() for x in h]
        h = [item for sublist in h for item in sublist]
        # get max word appearance
        mw, mc = get_max_appearance(h)
        # remove hashtags from caption
        caption = re.sub('#(_*[a-zآ-ی0-9]*_*\s*)*', '', caption)

        if mc / hashtag_num >= percent_of_key_word:
            return caption, mw
        return caption, None

    else:
        # remove hashtags from caption
        caption = re.sub('#(_*[a-zآ-ی0-9]*_*\s*)*', '', caption)
        return caption, None


def clean_caption(caption: str):
    """
        input: original caption without hashtags or a search term (String)
        output: tokenized cleaned caption (List)
        Punctuations, emojis, extra spaces and ... are removed.
        Some words are replaced for easy finding similar words.
        """
    stop_words = get_stop_words()
    #caption = remove_hashtags(caption)

    caption = re.sub('\'', '', caption)
    caption = re.sub('\w*\d\w*', '', caption)
    caption = re.sub(' +', ' ', caption)
    caption = re.sub(r'\n: \'\'.*', '', caption)
    caption = re.sub(r'\n!.*', '', caption)
    caption = re.sub(r'^:\'\'.*', '', caption)
    caption = re.sub(r'\n', ' ', caption)
    caption = re.sub(r'[^\w\s]', ' ', caption)
    caption = re.sub('[^آ-ی_ \n,،]', '', caption)

    caption = re.sub(r'\bتی شرت\b', 'تیشرت', caption)
    caption = re.sub(r'\bپولو شرت\b', 'پولوشرت', caption)
    caption = re.sub(r'\bنیم تنه\b', 'نیمتنه', caption)
    caption = re.sub(r'\bزیر پوش\b', 'زیرپوش', caption)
    caption = re.sub(r'\bلباس زیر\b', 'لباسزیر', caption)
    caption = re.sub(r'\bپا پوش\b', 'پاپوش', caption)
    caption = re.sub(r'\bسر همی\b', 'سرهمی', caption)
    caption = re.sub(r'\bسویی شرت\b', 'سوییشرت', caption)
    caption = re.sub(r'\bسوئی شرت\b', 'سوییشرت', caption)
    caption = re.sub(r'\bنیم بوت\b', 'نیمبوت', caption)
    caption = re.sub(r'\bاسپرت\b', 'اسپورت', caption)
    caption = re.sub(r'\bگرم کن\b', 'گرمکن', caption)
    caption = re.sub(r'\bهد بند\b', 'هدبند', caption)
    caption = re.sub(r'\bجوراب شلواری\b', 'جورابشلواری', caption)
    caption = re.sub(r'\bکمر بند\b', 'کمربند', caption)
    caption = re.sub(r'\bگردن بند\b', 'گردنبند', caption)
    caption = re.sub(r'\bدست بند\b', 'دستبند', caption)
    caption = re.sub(r'\bگوشوار\b', 'گوشواره', caption)
    caption = re.sub(r'\bگوش وار\b', 'گوشواره', caption)
    caption = re.sub(r'\bگوش واره\b', 'گوشواره', caption)
    caption = re.sub(r'\bپا بند\b', 'پابند', caption)
    caption = re.sub(r'\bساس بند\b', 'ساسبند', caption)
    caption = re.sub(r'\bسر دست\b', 'سردست', caption)
    caption = re.sub(r'\bنیم ساق\b', 'نیمساق', caption)

    caption_arr = re.split('[_ \n,،]+', caption)

    caption_arr = [word for word in caption_arr if word not in stop_words]
    return caption_arr
