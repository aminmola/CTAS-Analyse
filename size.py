import re
import pandas as pd

class Transform:
    def __init__(self, ):
        self.size_df = pd.read_csv('size.csv')
        self.category_df = pd.read_csv('category.csv')

    def remove_hashtags(self, caption: str):
        """
        input: original caption (String)
        output: caption without hashtags (String)
        Extract pure caption and remove hashtags
        """
        caption = re.sub('#(_*[آ-ی0-9]*_*\s*)*', '', caption)
        return caption

    def clean_caption_size(self, caption: str):
        """
        input: original caption (String)
        output: tokenized cleaned caption (List)
        Some words are replaced for easy finding similar words.
        Uppercase for finding sizes in table 'Size'.
        """
        caption = self.remove_hashtags(caption)
        caption = caption.lower()
        caption = caption.replace('سایزهای', 'سایز')
        caption = caption.replace(' و ', '/')
        caption = caption.replace("[\]", '/')
        caption = caption.replace('سایز های', 'سایز')
        caption = caption.replace('تک سایز', 'سایز')
        caption = caption.replace('تکسایز', 'سایز')
        caption = caption.replace('مناسب برای', 'مناسب')
        caption = caption.replace('سایزبندی', 'سایز')
        caption = caption.replace('سایز بندی', 'سایز')
        caption = caption.replace(' ta ', 'تا')
        caption = re.sub(r'\bالی\b', 'تا', caption)
        caption = re.sub(r'\bxxl\b', '2xl', caption)
        caption = re.sub(r'\bxxxl\b', '3xl', caption)
        caption = re.sub(r'\bxxxxl\b', '4xl', caption)
        caption = re.sub(r'\bxxxxxl\b', '5xl', caption)
        caption = caption.replace('کتونی', 'کفش')
        caption = caption.replace('size', 'سایز')
        caption = caption.replace('free', 'فری')
        caption = caption.replace('فیری', 'فری')
        caption = re.sub('[^A-Za-z0-9آ-ی :#@\n/_.,،;؛-]+', '', caption)
        caption = caption.upper()
        caption = ' '.join(caption.split())
        caption_arr = re.split('[-_ \n,،:/;؛.*]+', caption)
        return caption_arr

    # def get_category_for_size(self, post_id: int,):
    #     """
    #     input: the id of post (Integer), connection to db (pyodbc.connect)
    #     output: the id of category of the post (Integer)
    #     By this function, we get the categoryId of post, if there is any.
    #     """
    #     # connection to db and getting categories as df
    #     query = "SELECT Value FROM PostInfo Where PostId = ? AND [Key] = ?"
    #     category_df = pd.read_sql(query, cnxn, params=[str(post_id), 'CategoryId'])
    #
    #     # if df isn't empty, return the categoryId
    #     if len(category_df):
    #         category = category_df.iloc[0]
    #         category = int(category.Value)
    #         return category

    def get_category_father(self, category: int):
        """
        input: the id of category of the post (Integer), table 'Category' (DataFrame)
        output: the id of father of the category
        Since the category structure is hierarchical and the CategoryId in table 'Size' is based on the basic categories in
        the second layer (لباس و کفش), we need the categoryId of the father of the category.
        """
        # valid categories are in second layer:
        # 7: لباس زنانه
        # 8: کفش زنانه
        # 10: لباس مردانه
        # 11: کفش مردانه
        # 13: لباس دخترانه
        # 14: کفش دخترانه
        # 16: لباس پسرانه
        # 17: کفش پسرانه
        # 19: لباس نوزاد و بچگانه
        # 20: کفش نوزاد و بچگانه
        # 22: لباس بقیه
        # 23: کفش بقیه
        valid_categories = [7, 8, 10, 11, 13, 14, 16, 17, 19, 20, 22, 23]

        # we need to reach to the father of each category, until we reach any of the valid categories.
        if category is not None:
            # reach a category in valid categories.

            if category in valid_categories:
                return category

            # no valid categoryId is bigger than 24.
            while category > 24:
                father_df = self.category_df[self.category_df.Id == category].iloc[0]
                father = father_df.CategoryId
                category = father

            # reach a category in valid categories.
            if category in valid_categories:
                return category

    def get_size_id(self, size: str, category: int):
        """
        input: the size in caption (String), table 'Size' (DataFrame), the categoryId (Integer)
        output: the id of size in table 'Size'
        Each combination of size and categoryId is unique in table 'Size' and we can get the id of the size, based on the
        category of caption. We put this id in table 'PostInfo'.
        """

        # getting the row of dataframe, with specific size and category.
        size_row = self.size_df[(self.size_df.CategoryId == category) & (self.size_df.Title == size)]
        return size_row.iloc[0].Id

    def get_size(self, record):
        """
        input: the id of post (Integer), the caption of post (String), table 'Category' (DataFrame),
        table 'Size' (DataFrame), connection to db (pyodbc.connect)
        output: the ids of sizes in caption (List)
        This function returns ids of sizes in the caption.
        """
        caption = record['Caption']
        category = record['category']
        # cleaning the caption and tokenizing
        caption_arr = self.clean_caption_size(caption)
        size_word = 'سایز'

        # distance between sizes and size word
        distance = 10

        # valid size types:
        numeric_sizes = range(32, 61, 2)  # 32, 34, ..., 60
        alphabet_sizes = ['XS', 'S', 'M', 'L', 'XL', '2XL', '3XL', '4XL', '5XL']
        women_shoe_size = range(35, 43)  # 35, 36, ..., 42
        men_shoe_size = range(39, 52)  # 39, 40, ..., 51
        kid_shoe_size = range(22, 36)  # 22, 23, ..., 35
        baby_shoe_size = range(16, 36)  # 16, 17, ..., 35
        other_shoe_size = range(16, 52)  # 16, 17, ..., 51
        kid_size = range(2, 16)  # 2, 3, ..., 15 : age
        baby_size = range(16)  # 0, 1, ..., 15
        bra_sizes = range(65, 106, 5)  # 65, 70, ..., 105
        bra_cups = ['B', 'C', 'D', 'E', 'F']

        # list for output
        sizes = []

        # list of indexes of word سایز
        size_word_indexes = [i for i, e in enumerate(caption_arr) if e == 'سایز']
        # list of indexes of word تا
        ta_indexes = [i for i, e in enumerate(caption_arr) if e == 'تا']

        # some words can appear before sizes in caption
        pre_size_words = ['سایز', 'فری', 'مناسب']

        # get the category father of post
        category_origin = self.get_category_father(category)

        # if category father isn't in table 'Size', return empty list.
        if not category_origin:
            return sizes

        # word سایز have to be in the caption
        if size_word in caption_arr:
            # iteration on different appearances of word سایز
            for size_word_index in size_word_indexes:
                # if word before سایز is فری and category father is in table 'Size', we get the id of it
                if size_word_index > 0 and caption_arr[size_word_index - 1] == 'فری':
                    if category_origin in [7, 10, 13, 16, 19, 22]:
                        sizes.append(self.get_size_id('فری', category_origin))
                        return sizes
                # iteration in different appearances of word تا
                for t in ta_indexes:
                    # this part is for sizes like: 36 ta 48
                    # word تا have to be near word سایز
                    if 1 <= (t - size_word_index) <= 7 and t < len(caption_arr) - 1:
                        # getting the words before and after word تا, as the beginning and end of interval of size
                        first_size = caption_arr[t - 1]
                        last_size = caption_arr[t + 1]

                        # size for سوتین
                        if first_size.isnumeric() and last_size.isnumeric() and category == 232 and int(
                                first_size) in bra_sizes and int(
                            last_size) in bra_sizes:  # both beginning and end have to be valid for bra sizes

                            # search for cup of bra
                            r = re.compile('کاپ[B-F]?')
                            cup_list = list(filter(r.match, caption_arr))

                            # if cup is specified in caption
                            if cup_list:
                                # iteration over valid cups
                                for cup in bra_cups:
                                    # for example, if cup C is in caption and sizes are 65 ta 75, we get the id of these
                                    # sizes: 65C, 70C, 75C
                                    if cup in caption_arr or ('کاپ' + cup) in bra_cups:
                                        for i in range(int(first_size), int(last_size) + 1, 5):
                                            size = str(i) + cup
                                            sizes.append(self.get_size_id(size, category))
                                return sizes

                            # if there's no cup details in caption, for example, sizes are 65 ta 75, we get the id of these
                            # sizes: 65, 70, 75
                            for i in range(int(first_size), int(last_size) + 1, 5):
                                sizes.append(self.get_size_id(str(i), category))
                            return sizes

                        # size for لباس زنانه، لباس مردانه، لباس همه with numeric type
                        elif first_size.isnumeric() and last_size.isnumeric() and (
                                category_origin == 7 or category_origin == 10 or category_origin == 22) and int(
                            first_size) in numeric_sizes and int(
                            last_size) in numeric_sizes:  # both beginning and end have to be valid for numeric sizes
                            # iteration on sizes between beginning and end
                            for i in range(int(first_size), int(last_size) + 1, 2):
                                # getting the id of size and adding it to output
                                sizes.append(self.get_size_id(str(i), category_origin))
                            return sizes

                        # size for لباس زنانه، لباس مردانه، لباس همه with alphabet type
                        elif first_size in alphabet_sizes and last_size in alphabet_sizes and (
                                category_origin == 7 or category_origin == 10 or category_origin == 22):  # both beginning and end have to be valid for alphabet sizes
                            first_size_index = alphabet_sizes.index(first_size)
                            last_size_index = alphabet_sizes.index(last_size)
                            for i in range(first_size_index, last_size_index + 1):
                                sizes.append(self.get_size_id(alphabet_sizes[i], category_origin))
                            return sizes

                        # size for لباس دخترانه، لباس پسرانه
                        elif first_size.isnumeric() and last_size.isnumeric() and (
                                category_origin == 13 or category_origin == 16) and int(
                            first_size) in kid_size and int(last_size) in kid_size:
                            for i in range(int(first_size), int(last_size) + 1):
                                sizes.append(self.get_size_id(str(i), category_origin))
                            return sizes

                        # size for لباس نوزاد و بچگانه
                        elif first_size.isnumeric() and last_size.isnumeric() and category_origin == 19 and int(
                                first_size) in baby_size and int(last_size) in baby_size:
                            for i in range(int(first_size), int(last_size) + 1):
                                sizes.append(self.get_size_id(str(i), category_origin))
                            return sizes

                        # size for کفش زنانه
                        elif first_size.isnumeric() and last_size.isnumeric() and category_origin == 8 and int(
                                first_size) in women_shoe_size and int(last_size) in women_shoe_size:
                            for i in range(int(first_size), int(last_size) + 1):
                                sizes.append(self.get_size_id(str(i), category_origin))
                            return sizes

                        # size for کفش مردانه
                        elif first_size.isnumeric() and last_size.isnumeric() and category_origin == 11 and int(
                                first_size) in men_shoe_size and int(last_size) in men_shoe_size:
                            for i in range(int(first_size), int(last_size) + 1):
                                sizes.append(self.get_size_id(str(i), category_origin))
                            return sizes

                        # size for کفش نوزاد و بچگانه
                        elif first_size.isnumeric() and last_size.isnumeric() and category_origin == 20 and int(
                                first_size) in baby_shoe_size and int(last_size) in baby_shoe_size:
                            for i in range(int(first_size), int(last_size) + 1):
                                sizes.append(self.get_size_id(str(i), category_origin))
                            return sizes

                        # size for کفش دخترانه، کفش پسرانه
                        elif first_size.isnumeric() and last_size.isnumeric() and (
                                category_origin == 14 or category_origin == 17) and int(
                            first_size) in kid_shoe_size and int(last_size) in kid_shoe_size:
                            for i in range(int(first_size), int(last_size) + 1):
                                sizes.append(self.get_size_id(str(i), category_origin))
                            return sizes

                        # size for کفش همه
                        elif first_size.isnumeric() and last_size.isnumeric() and category_origin == 23 and int(
                                first_size) in other_shoe_size and int(last_size) in other_shoe_size:
                            for i in range(int(first_size), int(last_size) + 1):
                                sizes.append(self.get_size_id(str(i), category_origin))
                            return sizes

                        # if post doesn't have category , but it has valid size in caption, its sizes will be returned with
                        # categoryIds of همه

                        # size for لباس بدون کتگوری type numeric
                        elif first_size.isnumeric() and last_size.isnumeric() and int(
                                first_size) in numeric_sizes and int(last_size) in numeric_sizes:
                            for i in range(int(first_size), int(last_size) + 1, 2):
                                sizes.append(self.get_size_id(str(i), 22))
                            return sizes

                        # size for لباس بدون کتگوری type alphabet
                        elif first_size in alphabet_sizes and last_size in alphabet_sizes:
                            first_size_index = alphabet_sizes.index(first_size)
                            last_size_index = alphabet_sizes.index(last_size)
                            for i in range(first_size_index, last_size_index + 1):
                                sizes.append(self.get_size_id(alphabet_sizes[i], 22))
                            return sizes

                        # size for کفش بدون کتگوری
                        elif first_size.isnumeric() and last_size.isnumeric() and int(
                                first_size) in other_shoe_size and int(last_size) in other_shoe_size:
                            for i in range(int(first_size), int(last_size) + 1, 2):
                                sizes.append(self.get_size_id(str(i), 23))
                            return sizes

                # checking for empty output until now, i.e. there's nothing like '36 ta 42' in caption
                # now, sizes are like: 36, 38, 40, 42
                if not sizes:

                    # size for سوتین
                    if category == 232:
                        # search for cup of bra
                        r = re.compile('کاپ[B-F]?')
                        cup_list = list(filter(r.match, caption_arr))

                        # if cup is specified in caption
                        if cup_list:
                            # iteration over valid cups
                            for cup in bra_cups:
                                # if there is a specific cup in the caption
                                if cup in caption_arr or ('کاپ' + cup) in bra_cups:
                                    # iteration over valid bra sizes
                                    for i in bra_sizes:
                                        size = str(i)
                                        if size in caption_arr and (  # bra size have to be in caption
                                                (caption_arr.index(size) - size_word_index) <= distance) and (
                                                # bra size have to be near word سایز
                                                (caption_arr[caption_arr.index(size) - 1].isnumeric() and
                                                 int(caption_arr[caption_arr.index(
                                                     size) - 1]) in bra_sizes) or  # token before that size in caption have to be another bra size
                                                (caption_arr[caption_arr.index(
                                                    size) - 1] in pre_size_words)):  # or of one of the valid pre words
                                            # for example, if size 65 and cup B are in caption, we get the id of size 65B
                                            size += cup
                                            sizes.append(self.get_size_id(size, category))
                            return sizes

                        # if there's no cup details in caption, for example for size 65, we get the id of size 65, with similar constraints
                        for i in bra_sizes:
                            size = str(i)
                            if size in caption_arr and 1 <= ((caption_arr.index(size) - size_word_index) <= distance) and (
                                    (caption_arr[caption_arr.index(size) - 1].isnumeric() and
                                     int(caption_arr[caption_arr.index(size) - 1]) in bra_sizes) or
                                    (caption_arr[caption_arr.index(size) - 1] in pre_size_words)):
                                sizes.append(self.get_size_id(str(i), category))
                        return sizes

                    # size for لباس زنانه، لباس مردانه، لباس همه
                    elif category_origin == 7 or category_origin == 10 or category_origin == 22:
                        # iteration over valid numeric sizes
                        # with numeric type
                        for i in numeric_sizes:
                            size = str(i)
                            if size in caption_arr and 1 <= ((caption_arr.index(size) - size_word_index) <= distance) and (
                                    # size have to be near word سایز in caption
                                    (caption_arr[caption_arr.index(size) - 1].isnumeric() and
                                     int(caption_arr[caption_arr.index(
                                         size) - 1]) in numeric_sizes) or  # token before that size in caption have to be another numeric size
                                    (caption_arr[caption_arr.index(
                                        size) - 1] in pre_size_words)):  # or of one of the valid pre words
                                # getting the id of that size
                                sizes.append(self.get_size_id(str(i), category_origin))
                        # with alphabet type
                        if not sizes:
                            for size in alphabet_sizes:
                                if size in caption_arr and 1 <= ((caption_arr.index(size) - size_word_index) <= distance) and (
                                        caption_arr[caption_arr.index(size) - 1] in alphabet_sizes or
                                        caption_arr[caption_arr.index(size) - 1] in pre_size_words):
                                    sizes.append(self.get_size_id(size, category_origin))
                        return sizes




                    # size for لباس دخترانه، لباس پسرانه
                    elif category_origin == 13 or category_origin == 16:
                        for i in kid_size:
                            size = str(i)
                            if size in caption_arr and 1 <= ((caption_arr.index(size) - size_word_index) <= distance) and (
                                    (caption_arr[caption_arr.index(size) - 1].isnumeric() and
                                     int(caption_arr[caption_arr.index(size) - 1]) in kid_size) or
                                    (caption_arr[caption_arr.index(size) - 1] in pre_size_words)):
                                sizes.append(self.get_size_id(str(i), category_origin))
                        return sizes

                    # size for لباس نوزاد و بچگانه
                    elif category_origin == 19:
                        for i in baby_size:
                            size = str(i)
                            if size in caption_arr and 1 <= ((caption_arr.index(size) - size_word_index) <= distance) and (
                                    (caption_arr[caption_arr.index(size) - 1].isnumeric() and
                                     int(caption_arr[caption_arr.index(size) - 1]) in baby_size) or
                                    (caption_arr[caption_arr.index(size) - 1] in pre_size_words)):
                                sizes.append(self.get_size_id(str(i), category_origin))
                        return sizes

                    # size for کفش زنانه
                    elif category_origin == 8:
                        for i in women_shoe_size:
                            size = str(i)
                            if size in caption_arr and 1 <= ((caption_arr.index(size) - size_word_index) <= distance) and (
                                    (caption_arr[caption_arr.index(size) - 1].isnumeric() and
                                     int(caption_arr[caption_arr.index(size) - 1]) in women_shoe_size) or
                                    (caption_arr[caption_arr.index(size) - 1] in pre_size_words)):
                                sizes.append(self.get_size_id(str(i), category_origin))
                        return sizes

                    # size for کفش مردانه
                    elif category_origin == 11:
                        for i in men_shoe_size:
                            size = str(i)
                            if size in caption_arr and 1 <= ((caption_arr.index(size) - size_word_index) <= distance) and (
                                    (caption_arr[caption_arr.index(size) - 1].isnumeric() and
                                     int(caption_arr[caption_arr.index(size) - 1]) in men_shoe_size) or
                                    (caption_arr[caption_arr.index(size) - 1] in pre_size_words)):
                                sizes.append(self.get_size_id(str(i), category_origin))
                        return sizes

                    # size for کفش نوزاد و بچگانه
                    elif category_origin == 20:
                        for i in baby_shoe_size:
                            size = str(i)
                            if size in caption_arr and  1 <= ((caption_arr.index(size) - size_word_index) <= distance) and (
                                    (caption_arr[caption_arr.index(size) - 1].isnumeric() and
                                     int(caption_arr[caption_arr.index(size) - 1]) in baby_shoe_size) or
                                    (caption_arr[caption_arr.index(size) - 1] in pre_size_words)):
                                sizes.append(self.get_size_id(str(i), category_origin))
                        return sizes

                    # size for کفش دخترانه، کفش پسرانه
                    elif category_origin == 14 or category_origin == 17:
                        for i in kid_shoe_size:
                            size = str(i)
                            if size in caption_arr and 1 <= ((caption_arr.index(size) - size_word_index) <= distance) and (
                                    (caption_arr[caption_arr.index(size) - 1].isnumeric() and
                                     int(caption_arr[caption_arr.index(size) - 1]) in kid_shoe_size) or
                                    (caption_arr[caption_arr.index(size) - 1] in pre_size_words)):
                                sizes.append(self.get_size_id(str(i), category_origin))
                        return sizes

                    # size for کفش همه
                    elif category_origin == 23:
                        for i in other_shoe_size:
                            size = str(i)
                            if size in caption_arr and 1 <= ((caption_arr.index(size) - size_word_index) <= distance) and (
                                    (caption_arr[caption_arr.index(size) - 1].isnumeric() and
                                     int(caption_arr[caption_arr.index(size) - 1]) in other_shoe_size) or
                                    (caption_arr[caption_arr.index(size) - 1] in pre_size_words)):
                                sizes.append(self.get_size_id(size, category_origin))
                        return sizes

                    # if post doesn't have category , but it has valid size in caption, its sizes will be returned with
                    # categoryIds of همه

                    # size for لباس بدون کتگوری type numeric
                    for i in numeric_sizes:
                        size = str(i)
                        if size in caption_arr and 1 <= ((caption_arr.index(size) - size_word_index) <= distance) and (
                                (caption_arr[caption_arr.index(size) - 1].isnumeric() and
                                 int(caption_arr[caption_arr.index(size) - 1]) in numeric_sizes) or
                                (caption_arr[caption_arr.index(size) - 1] in pre_size_words)):
                            sizes.append(self.get_size_id(str(i), 22))

                    # size for لباس بدون کتگوری type alphabet
                    if not sizes:
                        for size in alphabet_sizes:
                            if size in caption_arr and 1 <= ((caption_arr.index(size) - size_word_index) <= distance) and (
                                    caption_arr[caption_arr.index(size) - 1] in alphabet_sizes or
                                    caption_arr[caption_arr.index(size) - 1] in pre_size_words):
                                sizes.append(self.get_size_id(size, 22))

                    # size for کفش بدون کتگوری
                    if not sizes:
                        for i in other_shoe_size:
                            size = str(i)
                            if size in caption_arr and 1 <= ((caption_arr.index(size) - size_word_index) <= distance) and (
                                    (caption_arr[caption_arr.index(size) - 1].isnumeric() and
                                     int(caption_arr[caption_arr.index(size) - 1]) in other_shoe_size) or
                                    (caption_arr[caption_arr.index(size) - 1] in pre_size_words)):
                                sizes.append(self.get_size_id(str(i), 23))
                    return sizes