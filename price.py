import pandas as pd
import re


class Transform:
    def __init__(self,):
        pass

    @staticmethod
    def remove_emoji(string):
        emoji_pattern = re.compile("["
                                   u"\U0001F600-\U0001F64F"  # emoticons
                                   u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                                   u"\U0001F680-\U0001F6FF"  # transport & map symbols
                                   u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                                   u"\U00002500-\U00002BEF"  # chinese char
                                   u"\U00002702-\U000027B0"
                                   u"\U00002702-\U000027B0"
                                   u"\U0001f926-\U0001f937"
                                   u"\U00010000-\U0010ffff"
                                   u"\u2640-\u2642"
                                   u"\u2600-\u2B55"
                                   u"\u200d"
                                   u"\u23cf"
                                   u"\u23e9"
                                   u"\u231a"
                                   u"\u3030"
                                   "]+", flags=re.UNICODE)
        return emoji_pattern.sub(r' ', string)

    #
    # def cleaning(self, caption: str) :
    #     """Cleaning raw Caption
    #     :Parameters
    #     ------------------
    #     Raw Caption of the post
    #
    #     :returns
    #     ------------------
    #     Caption
    #     1 - with no persian number : DONE
    #     2 - whole space instead of half space : DONE
    #     3 - with Homogenization of char 'ک' : ...
    #     4 - with Homogenization of char "ی" : DONE
    #     5 - eradicate the hashtag in the middle of caption : ...
    #     6 - ...
    #     """
    #
    #     ### normalize the caption
    #
    #     caption = normalizer.normalize(caption)
    #
    #     ### 1 - with no persian number###
    #     caption = re.split('', caption)
    #     for i in range(len(caption)) :
    #         if unidecode(caption[i]).isnumeric() :
    #             caption[i] = unidecode(caption[i])
    #     caption = ''.join(caption)
    #     ##############################
    #
    #     ### 2 - whole space instead of half space###
    #     caption = caption.replace('\u200c', " ")
    #
    #     ##############################
    #
    #     return caption

    def clean_caption(self, caption) :
        # taking the whole caption and remove extra characters and returning split caption(cleaned_caption)
        if pd.isna(caption) :
            # print('1')
            return []
        caption = caption.replace('T', 't')
        ####################################################################################################
        # Persian and Arabic Numbers >>> English Numbers
        temp_cap = caption
        caption = re.split('', caption)
        # for i in range(len(caption)):
        #     if unidecode(caption[i]).isnumeric():
        #         caption[i] = unidecode(caption[i])
        # temp_cap = ''.join(caption)

        for i in range(len(caption) - 1):
            if caption[i].isnumeric():
                if caption[i + 1] == 'ت' :
                    a = caption[i] + 'ت'
                    temp_cap = temp_cap.replace(a, str(caption[i]) + " " + 'ت')
                if caption[i + 1] == 't' :
                    a = caption[i] + 't'
                    temp_cap = temp_cap.replace(a, str(caption[i]) + " " + 't')
        caption = temp_cap
        ####################################################################################################
        caption = caption.replace('=', ' ')
        caption = caption.replace('_', ' ')
        caption = caption.replace(':', ' ')
        caption = caption.replace('،', '.')
        caption = caption.replace(',', '.')
        caption = caption.replace('٬', '.')
        caption = caption.replace('/', '.')
        caption = caption.replace('هزار تومان', ' هزار ')
        caption = caption.replace('هزارتومان', ' هزار ')
        caption = caption.replace('تومان', ' تومن ')
        caption = caption.replace('یورو', ' یورو ')
        caption = caption.replace('تومن', ' تومن ')
        caption = caption.replace('دلار', ' دلار ')
        caption = caption.replace('ریال', ' ریال ')
        caption = caption.replace('هزار', ' هزار ')
        caption = caption.replace(' بها ', ' قیمت ')
        caption = caption.replace('price', ' قیمت ')
        caption = caption.replace('قیمت', ' قیمت ')
        caption = caption.replace('متری ', ' ')
        caption = self.remove_emoji(caption)
        caption = caption.replace('Off', ' تخفیف ')
        caption = caption.replace(' آف ', ' تخفیف ')
        caption = caption.replace(' اف ', ' تخفیف ')
        ####################################################################################################

        if ('دلار' in re.split('[ \n]+', caption)) or ('یورو' in re.split('[ \n]+', caption)) \
                or ('لیر' in re.split('[ \n]+', caption)) :
            cap = re.split('[ \n]+', caption)
            indices = [i for i, x in enumerate(re.split('[ \n]+', caption)) if x == "دلار"]
            if indices :
                for i in indices :
                    if cap[i - 1].replace('.', '', 1).isnumeric() :
                        caption = re.split('[ \n]+', caption)
                        caption[i - 1] = str(round(float(caption[i - 1])))
                        caption = ' '.join(caption)

            indices = [i for i, x in enumerate(re.split('[ \n]+', caption)) if x == "لیر"]
            if indices :
                for i in indices :
                    if cap[i - 1].replace('.', '', 1).isnumeric() :
                        caption = re.split('[ \n]+', caption)
                        caption[i - 1] = str(round(float(caption[i - 1])))
                        caption = ' '.join(caption)
            indices = [i for i, x in enumerate(re.split('[ \n]+', caption)) if x == "یورو"]
            if indices :
                for i in indices :
                    if cap[i - 1].replace('.', '', 1).isnumeric() :
                        caption = re.split('[ \n]+', caption)
                        caption[i - 1] = str(round(float(caption[i - 1])))
                        caption = ' '.join(caption)

        caption = caption.replace('.', '')
        caption = re.sub('[^A-Z0-9a-z0-9آ-ی #@\n/_.]+', ' ', caption)
        caption_arr = re.split('[ \n]+', caption)
        return caption_arr

    @staticmethod
    def remove_hashtags(caption) :
        # taking the caption and remove its hashtags
        caption = re.sub('#(_*[آ-ی0-9]*_*\s*)', '', caption)
        return caption

    def include_discount_words(self, caption) :
        # filter posts with ['تخفیف','حراج'] words
        caption = self.remove_hashtags(caption)
        " 1 is for the caption that has the word 'تخفیف' and 2 is for the caption that does not have discount"

        discount_words = ['تخفیف', 'حراج']
        if any(x in caption for x in discount_words) :
            return 1
        else :
            return 2

    @staticmethod
    def get_index_previous_price_word(cleaned_caption) :
        # taking the caption and returning the index of a specific ordered phrase describing price before discount

        if 'قیمت قبل از تخفیف' in ' '.join(cleaned_caption) :
            cap = ' '.join(cleaned_caption)
            cap = cap.replace('قیمت قبل از تخفیف', ' mfsdbkl ')
            cap = re.split('[ \n]+', cap)
            index_previous_price_word = cap.index('mfsdbkl') + 3
        elif 'قیمت اصلی' in ' '.join(cleaned_caption) :
            cap = ' '.join(cleaned_caption)
            cap = cap.replace('قیمت اصلی', ' mfsdbkl ')
            cap = re.split('[ \n]+', cap)
            index_previous_price_word = cap.index('mfsdbkl') + 1
        elif 'قیمت قبل' in ' '.join(cleaned_caption) :
            cap = ' '.join(cleaned_caption)
            cap = cap.replace('قیمت قبل', ' mfsdbkl ')
            cap = re.split('[ \n]+', cap)
            index_previous_price_word = cap.index('mfsdbkl') + 1

        else :
            index_previous_price_word = -2
        return index_previous_price_word, 2

    @staticmethod
    def get_index_discounted_price_word(cleaned_caption) :
        # taking the caption and returning the index of a specific ordered phrase describing price after discount

        if 'قیمت بعد از تخفیف' in ' '.join(cleaned_caption) :
            cap = ' '.join(cleaned_caption)
            cap = cap.replace('قیمت بعد از تخفیف', ' ffadkvmvma ')
            cap = re.split('[ \n]+', cap)
            index_after_price_word = cap.index('ffadkvmvma') + 3
        elif 'قیمت با تخفیف' in ' '.join(cleaned_caption) :
            cap = ' '.join(cleaned_caption)
            cap = cap.replace('قیمت با تخفیف', ' ffadkvmvma ')
            cap = re.split('[ \n]+', cap)
            index_after_price_word = cap.index('ffadkvmvma') + 2
        elif 'قیمت پس از تخفیف' in ' '.join(cleaned_caption) :
            cap = ' '.join(cleaned_caption)
            cap = cap.replace('قیمت پس از تخفیف', ' ffadkvmvma ')
            cap = re.split('[ \n]+', cap)
            index_after_price_word = cap.index('ffadkvmvma') + 3
        elif 'قیمت تخفیف خورده' in ' '.join(cleaned_caption) :
            cap = ' '.join(cleaned_caption)
            cap = cap.replace('قیمت تخفیف خورده', ' ffadkvmvma ')
            cap = re.split('[ \n]+', cap)
            index_after_price_word = cap.index('ffadkvmvma') + 2
        elif 'قیمت حراج' in ' '.join(cleaned_caption) :
            cap = ' '.join(cleaned_caption)
            cap = cap.replace('قیمت حراج', ' ffadkvmvma ')
            cap = re.split('[ \n]+', cap)
            index_after_price_word = cap.index('ffadkvmvma') + 1
        else :
            index_after_price_word = -2
        return index_after_price_word, 3

    ##############################################################################################################
    @staticmethod
    def get_index_percentive_discount(cleaned_caption) :
        index = -2
        discount_percent = -10
        if 'قیمت با تخفیف' in ' '.join(cleaned_caption) :
            cap = ' '.join(cleaned_caption)
            cap = cap.replace('قیمت با تخفیف', ' mfsdbkl ')
            cap = re.split('[ \n]+', cap)
            if len(cap) > cap.index('mfsdbkl') + 4 :
                if cap[cap.index('mfsdbkl') + 2] == 'درصد' and cap[cap.index('mfsdbkl') + 1].isnumeric() :
                    if 65 > float(cap[cap.index('mfsdbkl') + 1]) > 4 :
                        index = cap.index('mfsdbkl') + 4
                        discount_percent = float(cap[cap.index('mfsdbkl') + 1])
        elif 'قیمت با' in ' '.join(cleaned_caption) :
            cap = ' '.join(cleaned_caption)
            cap = cap.replace('قیمت با', ' mfsdbkl ')
            cap = re.split('[ \n]+', cap)
            if len(cap) > cap.index('mfsdbkl') + 3 :
                if cap[cap.index('mfsdbkl') + 2] == 'درصد' and cap[cap.index('mfsdbkl') + 3] == 'تخفیف' and cap[cap.index('mfsdbkl') + 1].isnumeric():
                    if 65 > float(cap[cap.index('mfsdbkl') + 1]) > 4 :
                        index = cap.index('mfsdbkl') + 4
                        discount_percent = float(cap[cap.index('mfsdbkl') + 1])
        return index, discount_percent

    ##############################################################################################################
    @staticmethod
    def get_index_price_word(cleaned_caption) :
        if 'قیمت' in cleaned_caption :
            index_price_word = cleaned_caption.index('قیمت')
        else :
            index_price_word = -1
        if (index_price_word > 0) and (index_price_word + 2 < len(cleaned_caption)) :
            if cleaned_caption[index_price_word + 2] == 'الی' :
                index_price_word = index_price_word + 3
            elif cleaned_caption[index_price_word + 1] == 'سایز' or cleaned_caption[index_price_word + 2] == 'سال' \
                    or cleaned_caption[index_price_word + 2] == 'ماه' :
                index_price_word = index_price_word + 2
            elif cleaned_caption[index_price_word + 1] == 'فقط' or cleaned_caption[index_price_word + 1] == 'ویژه' \
                    or cleaned_caption[index_price_word + 1] == 'عالی' :
                index_price_word = index_price_word + 1
            elif 'قیمت با احترام' in ' '.join(cleaned_caption) :
                index_price_word = index_price_word + 2
        return index_price_word, 1

    @staticmethod
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
        million_digit = 0
        if 'میلیون' in cleaned_caption :
            index_unit_word = cleaned_caption.index('میلیون')
            if index_unit_word + 3 < len(cleaned_caption) and index_price_word[1] != 3 :
                thousandth = ['هزار', 'هزارتومان', 'هزارتومن']
                if cleaned_caption[index_unit_word + 1] == 'و' and cleaned_caption[index_unit_word + 2].isnumeric() and \
                        cleaned_caption[index_unit_word + 3] in thousandth :
                    million_digit = 1
            if index_price_word[0] + 3 < len(cleaned_caption) and index_price_word[1] == 3 :
                thousandth = ['هزار', 'هزارتومان', 'هزارتومن']
                if cleaned_caption[index_price_word[0] + 2] == 'میلیون' and cleaned_caption[
                    index_price_word[0] + 3] == 'و' \
                        and cleaned_caption[index_price_word[0] + 4].isnumeric() and \
                        cleaned_caption[index_price_word[0] + 5] in thousandth :
                    index_unit_word = index_price_word[0] + 2
                    million_digit = 1

            if index_unit_word > 1 :
                dic = {'یک' : '1', 'دو' : '2', "سه" : '3', 'چهار' : '4', 'پنج' : '5'}
                if cleaned_caption[index_unit_word - 1] in dic :
                    cleaned_caption[index_unit_word - 1] = dic[cleaned_caption[index_unit_word - 1]]

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
        elif 'دلار' in cleaned_caption :
            index_unit_word = cleaned_caption.index('دلار')
        elif 'یورو' in cleaned_caption :
            index_unit_word = cleaned_caption.index('یورو')
        elif 't' in cleaned_caption :
            index_unit_word = cleaned_caption.index('t')
            if index_unit_word > 2 and index_unit_word + 1 < len(cleaned_caption) :
                if cleaned_caption[index_unit_word - 2] == 'کد' or not cleaned_caption[
                    index_unit_word - 1].isnumeric() or \
                        cleaned_caption[index_unit_word - 2] == 'مدل' or cleaned_caption[
                    index_unit_word + 1].isnumeric() or \
                        ('a' <= cleaned_caption[index_unit_word + 1] <= 'z') :
                    index_unit_word = -1
        else :
            index_unit_word = -1
        # Finding the first number after the word 'قیمت' and saving it as a potential price.\
        # In addition, saving the next word as a unit of the price.
        if (index_price_word[0] != -1) and (index_price_word[0] >= 0) :
            j = index_price_word[0]
            while j < len(cleaned_caption) and (not cleaned_caption[j].isnumeric()) :
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
        if (index_price_word[0] != -2) and (index_price_word[1] == 1) and (index_unit_word != -1) and (
                index_unit_word > 0) \
                and (dist_price != 1) and cleaned_caption[index_unit_word - 2] != 'ارسال' and cleaned_caption[index_unit_word - 2] != 'پست' :
            j = index_unit_word - 1
            if cleaned_caption[j].replace('.', '', 1).isnumeric() :
                price = cleaned_caption[j]
                price_unit = cleaned_caption[index_unit_word]
                dist_price = 1
        # print(i, dist_price[i], len(cleaned_caption[i]))
        # print(price[i])

        # Filtering out incorrect prices
        #  * first: If the distance between the word 'قیمت' and first number after that is larger than 5,\
        #  it is most probably incorrect.
        #  * second: Correcting the range of the price.
        #  * third: removing the prices that are larger than 100000000. These are either (1) result of removing a \
        # dash between a range of the prices or (2) they are phone number instead of the price.

        # 1st filter
        if dist_price > 5 :
            price = ''
            price_unit = ''
        # 2rd filter
        if price.replace('.', '', 1).isnumeric() :
            if float(price) < 1000 :
                if price_unit in ['هزار', 'هزارتومان'] :  # a thousand
                    final_price = float(price) * 1000
                    final_price_unit = 1  # 'تومان'
                elif price_unit in ['میلیون'] and float(price) < 14 :  # Milion
                    final_price = float(price) * 1000000
                    final_price_unit = 1  # 'تومان'
                    if million_digit == 1 :
                        final_price = final_price + float(cleaned_caption[index_unit_word + 2]) * 1000
                elif price_unit in ['تومان', 'ت', 'تومن', 't'] and float(price) < 10 :  # Milion
                    final_price = float(price) * 1000000
                    final_price_unit = 1  # 'تومان'
                elif price_unit in ['ریال'] :
                    final_price = float(price) / 10
                    final_price_unit = 1  # 'تومان'
                elif price_unit in ['تل', 'تله', 'لیر']:
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
            if (final_price < 10001) and (final_price_unit == 1) :
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
        if final_price :
            if ((final_price % 100) != 0) and (final_price_unit == 1):
                final_price = ''
                final_price_unit = ''
        if 'قیمت دایرکت' in ' '.join(cleaned_caption) :
            final_price = ''
            final_price_unit = ''

        return str(final_price), str(final_price_unit)

    def extract_discount_prices(self, cleaned_caption) :
        # extract discounted price and price before discount and their unit from a single caption
        # input splinted cleaned caption
        # output strings for prices and their units

        caption = ' '.join(cleaned_caption)
        if self.include_discount_words(caption) == 1 :
            caption = caption.replace('درصدی', ' درصد ')
            caption = caption.replace('درصد', ' درصد ')
            caption = caption.replace(' در صد', ' درصد')
            caption = caption.replace('%', ' درصد ')
            caption = caption.replace('احتساب', '')
            caption = caption.replace('اعمال', '')
            caption = caption.replace('قیمت تخفیفی', 'قیمت بعد از تخفیف')
            cleaned_caption = re.split('[ \n]+', caption)

            final_previous_price, final_previous_price_unit = \
                self.extract_price(cleaned_caption, self.get_index_previous_price_word(cleaned_caption))
            final_discounted_price, final_discounted_price_unit = self.extract_price(cleaned_caption,
                                                                                     self.get_index_discounted_price_word(
                                                                                         cleaned_caption))

            if self.get_index_percentive_discount(cleaned_caption)[1] > 0 :
                if self.extract_price(cleaned_caption, (self.get_index_percentive_discount(cleaned_caption)[0], 2))[0] :
                    final_discounted_price, final_discounted_price_unit = self.extract_price(cleaned_caption, (
                        self.get_index_percentive_discount(cleaned_caption)[0], 4))
                    final_previous_price, final_previous_price_unit = str(1000 * int((float(
                        final_discounted_price) * 100 / (100 - self.get_index_percentive_discount(cleaned_caption)[1])) / 1000)), self.extract_price(cleaned_caption, (self.get_index_percentive_discount(cleaned_caption)[0], 4))[1]

            if final_discounted_price != '' and final_previous_price != '' :
                if (float(final_discounted_price) < 0.26 * float(final_previous_price)) or \
                        (not float(final_discounted_price) < float(final_previous_price)) :
                    final_previous_price = ''
                    final_previous_price_unit = ''
                    final_discounted_price = ''
                    final_discounted_price_unit = ''

        else :
            final_previous_price = ''
            final_previous_price_unit = ''
            final_discounted_price = ''
            final_discounted_price_unit = ''
        return str(final_previous_price), str(final_previous_price_unit), str(final_discounted_price), str(
            final_discounted_price_unit)

    def has_currency(self, cleaned_caption):
        has_unit = False
        unit_words = ['میلیون', 'تومان', 'تومن', 'لیر', 'تل', 'تله', 'هزار', 'ت', 'هزارتومان', 'ریال', 'دلار', 'یورو',
                      't']
        for word in unit_words:
            if word in cleaned_caption:
                has_unit = True
                break

        return has_unit

