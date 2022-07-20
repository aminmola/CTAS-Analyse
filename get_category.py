"""Function for Category extraction"""
import pandas as pd
from caption_cleaner import remove_hashtags
from caption_cleaner import clean_caption


def get_category_father(category: int, category_df: pd.DataFrame):
    """
    input: the id of category of the post (Integer), table 'Category' (DataFrame)
    output: the id of father of the category
    Since the category structure is hierarchical, we need the categoryId of the father of the category to find out if
    its gender/age is obvious or not(همه).
    """

    # valid categories are in first layer:
    # زنانه: 1
    # مردانه: 2
    # دخترانه: 3
    # پسرانه: 4
    # کودکانه و نوزاد: 5
    # همه: 6

    valid_categories = list(range(1, 7))
    if category is not None:
        # reach a category in valid categories.
        if category in valid_categories:
            return category
        # we need to reach to the father of each category, until we reach any of the valid categories.
        while category > 6:
            father_df = category_df[category_df.Id == category].iloc[0]
            father = father_df.CategoryId
            category = father
        # reach a category in valid categories.
        if category in valid_categories:
            return category


def get_category(caption):
    caption_arr = clean_caption(caption)
    # tokenizing clean caption

    # 3 for loops, each for one layer
    # first layer: woman, man, child, other
    for word1 in caption_arr:
        if word1 in ['زنانه', 'زنونه', 'خانم', 'خانوم']:
            i = caption_arr.index(word1)
            if i > 0 and caption_arr[i-1] == 'پیج':
                continue

            # second layer: clothes, shoes, bag
            for word2 in caption_arr:
                i = caption_arr.index(word2)
                if i > 0 and caption_arr[i-1] == 'پیج':
                    continue

                # women clothes
                if word2 == 'کت':
                    return 188
                if word2 == 'ست':
                    if i < len(caption_arr)-1:
                        if len(caption_arr)-i > 5:
                            next_words = caption_arr[i+1:i+6]
                        else:
                            next_words = caption_arr[i+1:len(caption_arr)]
                        if any(i in ['رسمی', 'مجلسی', 'کت', 'دامن'] for i in next_words):
                            return 189
                        if any(i in ['ورزشی', 'اسپورت', 'گرمکن', 'لگ', 'لگینگ'] for i in next_words):
                            return 222
                        if any(i in ['لباسزیر', 'شورت', 'شرت', 'سوتین'] for i in next_words):
                            return 233
                        if any(i in ['گردنبند', 'دستبند', 'انگشتر', 'گوشواره', 'آویز', 'پابند', 'زیورآلات',
                                     'بدلیجات'] for i in next_words):
                            return 280
                if word2 in ['پیرهن', 'پیراهن']:
                    if i < len(caption_arr)-1 and caption_arr[i+1] in ['بارداری', 'حاملگی']:
                        return 202
                    return 26
                if word2 == 'لباس':
                    if i < len(caption_arr)-1:
                        if caption_arr[i+1] in ['مجلسی', 'رسمی']:
                            return 26
                        if caption_arr[i+1] in ['ورزشی', 'اسپورت']:
                            return 36
                        if caption_arr[i+1] == 'خواب':
                            return 190
                        if caption_arr[i+1] == 'راحتی':
                            if i < len(caption_arr)-2 and caption_arr[i+2] in ['بارداری', 'حاملگی']:
                                return 205
                            return 191
                        if caption_arr[i+1] == 'شنا':
                            return 41
                        if caption_arr[i+1] in ['بارداری', 'حاملگی']:
                            return 31
                    # return 7
                if word2 == 'مانتو':
                    if i < len(caption_arr)-1 and caption_arr[i+1] in ['بارداری', 'حاملگی']:
                        return 202
                    return 192
                if word2 == 'پانچو':
                    return 193
                # if word2 == 'رویه':
                #     return 194
                if word2 == 'شنل':
                    return 195
                if word2 == 'چادر':
                    return 196
                if word2 == 'مقنعه':
                    return 197
                if word2 in ['اسلش', 'شلوار']:
                    if i < len(caption_arr)-1 and caption_arr[i+1] in ['بارداری', 'حاملگی']:
                        return 203
                    return 198
                if word2 in ['سرهمی', 'اورال', 'اورآل']:
                    if i < len(caption_arr)-1 and caption_arr[i+1] in ['بارداری', 'حاملگی']:
                        return 203
                    return 199
                # if word2 in ['بافت', 'ژاکت']:
                if word2 in ['ژاکت']:
                    return 200
                if word2 in ['پولیور', 'پلیور']:
                    return 201
                if word2 in ['بارداری', 'حاملگی']:
                    return 31
                if word2 == 'کاپشن':
                    return 208
                if word2 == 'پالتو':
                    return 209
                if word2 in ['بارانی', 'بارونی']:
                    return 210
                if word2 in ['جلیقه', 'ژیله']:
                    return 211
                if word2 in ['بلوز', 'بولوز', 'بولیز']:
                    if i < len(caption_arr)-1 and caption_arr[i+1] in ['بارداری', 'حاملگی']:
                        return 206
                    return 212
                if word2 == 'شومیز':
                    if i < len(caption_arr)-1 and caption_arr[i+1] in ['بارداری', 'حاملگی']:
                        return 206
                    return 213
                if word2 == 'بادی':
                    return 214
                if word2 == 'شلوارک':
                    return 215
                if word2 in ['شرتک', 'شورتک']:
                    return 216
                if word2 == 'دامن':
                    if i < len(caption_arr)-1 and caption_arr[i+1] in ['بارداری', 'حاملگی']:
                        return 207
                    return 217
                if word2 in ['سارافن', 'سارافون']:
                    return 218
                if word2 in ['لگینگ', 'لگ', 'ساپرت', 'ساپورت']:
                    return 219
                if word2 == 'کاور':
                    return 220
                if word2 == 'گرمکن':
                    return 221
                if word2 == 'نیمتنه':
                    if i < len(caption_arr)-1:
                        if caption_arr[i+1] in ['ورزشی', 'اسپورت']:
                            return 223
                    return 230
                if word2 in ['دستکش', 'دسکش']:
                    if i < len(caption_arr)-1:
                        if caption_arr[i+1] in ['ورزشی', 'اسپورت', 'دروازه', 'بدنسازی']:
                            return 224
                    return 53
                if word2 == 'هدبند':
                    if i < len(caption_arr)-1:
                        if caption_arr[i+1] in ['ورزشی', 'اسپورت']:
                            return 224
                    return 252
                if word2 in ['سوییشرت', 'سویشرت']:
                    return 225
                if word2 == 'هودی':
                    return 226
                if word2 == 'تیشرت':
                    if i < len(caption_arr)-1 and caption_arr[i+1] in ['بارداری', 'حاملگی']:
                        return 204
                    return 227
                if word2 == 'پولوشرت':
                    if i < len(caption_arr)-1 and caption_arr[i+1] in ['بارداری', 'حاملگی']:
                        return 204
                    return 228
                if word2 == 'تاپ':
                    return 229
                if word2 in ['شورت', 'شرت', 'لامبادا']:
                    return 231
                if word2 == 'سوتین':
                    return 232
                if word2 == 'تونیک':
                    return 40
                if word2 in ['بیکینی', 'مایو', 'بکینی']:
                    return 41
                if word2 in ['لباسزیر', 'زیرپوش']:
                    return 42

                # women shoes
                if word2 in ['نیمبوت', 'نیمساق']:
                    return 43
                if word2 in ['بوت', 'چکمه']:
                    return 44
                if word2 == 'گیوه':
                    return 45
                if word2 in ['دمپایی', 'صندل']:
                    if 'عطر' not in caption_arr:
                        return 46
                if word2 == 'پاشنه':
                    return 47
                if word2 in ['کتانی', 'کتونی'] or (
                        word2 == 'کفش' and i < len(caption_arr)-1 and (caption_arr[i+1] in ['ورزشی', 'اسپورت'])):
                    return 48
                if word2 == 'کالج':
                    return 49
                if word2 == 'کفش':
                    return 8

                # women accessories
                if word2 == 'کیف':
                    if i < len(caption_arr)-1:
                        if caption_arr[i+1] == 'پول':
                            return 235
                    return 234
                if word2 == 'کوله':
                    return 236
                if word2 in ['چمدان', 'چمدون']:
                    return 237
                if word2 == 'عینک':
                    return 51
                if word2 in ['پاپوش', 'جوراب']:
                    return 238
                if word2 == 'جورابشلواری':
                    return 239
                if word2 == 'ساق':
                    return 240
                if word2 == 'کمربند':
                    return 54
                if word2 == 'گردنبند':
                    return 241
                if word2 == 'دستبند':
                    return 242
                if word2 == 'انگشتر':
                    return 243
                if word2 == 'گوشواره':
                    return 244
                if word2 == 'پیرسینگ':
                    return 245
                if word2 == 'آویز':
                    return 246
                if word2 == 'پابند':
                    return 247
                if word2 in ['گل', 'سنجاق']:
                    if i < len(caption_arr)-1:
                        if caption_arr[i+1] == 'سینه':
                            return 248
                        if caption_arr[i+1] == 'سر':
                            return 250
                if word2 in ['زیورآلات', 'بدلیجات']:
                    return 55
                if word2 == 'کش':
                    if i < len(caption_arr)-1:
                        if caption_arr[i+1] == 'سر':
                            return 249
                if word2 in ['کلیپس', 'کیلیپس']:
                    return 251
                if word2 == 'کلاه':
                    if (i < len(caption_arr)-1 and caption_arr[i+1] != 'دار') or i == len(caption_arr)-1:
                        return 253
                if word2 in ['شالگردن', 'شال']:
                    return 254
                if word2 in ['اسکارف', 'روسری']:
                    return 255
                if word2 in ['کراوات', 'کروات']:
                    return 256
                if word2 == 'پاپیون':
                    return 257
                if word2 == 'ساعت':
                    return 59
                # if word2 == 'ماسک':
                #     return 60
            if 'لباس' in caption_arr:
                return 7
            return 1
            #     if word2 == 'ست':
            #         return 176
        if word1 in ['مردونه', 'مردانه']:
            i = caption_arr.index(word1)
            if i > 0 and (caption_arr[i-1] == 'پیج' or caption_arr[i-1] == 'یقه'):
                continue
            for word2 in caption_arr:
                i = caption_arr.index(word2)
                if i > 0 and caption_arr[i-1] == 'پیج':
                    continue

                # men clothes
                if word2 == 'کت':
                    return 258
                if word2 == 'ست':
                    if i < len(caption_arr)-1:
                        if len(caption_arr)-i > 5:
                            next_words = caption_arr[i+1:i+6]
                        else:
                            next_words = caption_arr[i+1:len(caption_arr)]
                        if any(i in ['رسمی', 'مجلسی', 'کت'] for i in next_words):
                            return 259
                        if any(i in ['ورزشی', 'اسپورت', 'گرمکن', 'لگ', 'لگینگ'] for i in next_words):
                            return 271
                        if any(i in ['لباسزیر', 'شورت', 'شرت'] for i in next_words):
                            return 279
                        if any(i in ['گردنبند', 'دستبند', 'انگشتر', 'گوشواره', 'آویز', 'زیورآلات', 'بدلیجات'] for i in
                               next_words):
                            return 293
                if word2 in ['پیرهن', 'پیراهن']:
                    return 66
                if word2 == 'لباس':
                    if i < len(caption_arr)-1:
                        if caption_arr[i+1] in ['مجلسی', 'رسمی']:
                            return 61
                        if caption_arr[i+1] in ['ورزشی', 'اسپورت']:
                            return 68
                        if caption_arr[i+1] == 'خواب':
                            return 260
                        if caption_arr[i+1] == 'راحتی':
                            return 261
                        if caption_arr[i+1] == 'شنا':
                            return 73
                    # return 10
                if word2 in ['اسلش', 'شلوار']:
                    return 63
                # if word2 in ['بافت', 'ژاکت']:
                if word2 in ['ژاکت']:
                    return 262
                if word2 in ['پولیور', 'پلیور']:
                    return 263
                if word2 == 'کاپشن':
                    return 264
                if word2 == 'پالتو':
                    return 265
                if word2 in ['بارانی', 'بارونی']:
                    return 266
                if word2 in ['جلیقه', 'ژیله']:
                    return 267
                if word2 in ['بلوز', 'بولوز', 'بولیز']:
                    return 72
                if word2 == 'شلوارک':
                    return 67
                if word2 in ['لگینگ', 'لگ', 'ساپرت', 'ساپورت']:
                    return 268
                if word2 == 'کاور':
                    return 269
                if word2 == 'گرمکن':
                    return 270
                if word2 in ['دستکش', 'دسکش']:
                    if i < len(caption_arr)-1:
                        if caption_arr[i+1] in ['ورزشی', 'اسپورت', 'دروازه', 'بدنسازی']:
                            return 272
                    return 85
                if word2 == 'هدبند':
                    if i < len(caption_arr)-1:
                        if caption_arr[i+1] in ['ورزشی', 'اسپورت']:
                            return 272
                if word2 in ['سوییشرت', 'سویشرت']:
                    return 273
                if word2 == 'هودی':
                    return 274
                if word2 == 'تیشرت':
                    return 275
                if word2 == 'پولوشرت':
                    return 276
                if word2 == 'تاپ':
                    return 71
                if word2 in ['شورت', 'شرت']:
                    return 277
                if word2 == 'مایو':
                    return 72
                if word2 in ['رکابی', 'زیرپوش']:
                    return 278
                if word2 == 'لباسزیر':
                    return 74

                # men shoes
                if word2 in ['نیمبوت', 'نیمساق']:
                    return 75
                if word2 in ['بوت', 'چکمه']:
                    return 76
                if word2 == 'گیوه':
                    return 77
                if word2 in ['دمپایی', 'صندل']:
                    if 'عطر' not in caption_arr:
                        return 78
                if word2 == 'کفش' and i < len(caption_arr)-1 and (caption_arr[i+1] in ['رسمی', 'مجلسی']):
                    return 79
                if word2 in ['کتانی', 'کتونی'] or (
                        word2 == 'کفش' and i < len(caption_arr)-1 and (caption_arr[i+1] in ['ورزشی', 'اسپورت'])):
                    return 80
                if word2 == 'کالج':
                    return 81
                if word2 == 'کفش':
                    return 11

                # men accessories
                if word2 == 'کیف':
                    if i < len(caption_arr)-1:
                        if caption_arr[i+1] == 'پول':
                            return 282
                    return 281
                if word2 == 'کوله':
                    return 283
                if word2 in ['چمدان', 'چمدون']:
                    return 284
                if word2 == 'عینک':
                    return 83
                if word2 in ['پاپوش', 'جوراب']:
                    return 285
                if word2 == 'ساق':
                    return 286
                if word2 == 'کمربند':
                    return 458
                if word2 == 'ساسبند':
                    return 459
                if word2 == 'گردنبند':
                    return 287
                if word2 == 'دستبند':
                    return 288
                if word2 == 'انگشتر':
                    return 289
                if word2 == 'گوشواره':
                    return 290
                if word2 == 'پیرسینگ':
                    return 291
                if word2 == 'آویز':
                    return 292
                if word2 == 'دکمه' and (i < len(caption_arr)-1 and caption_arr[i+1] == 'سردست'):
                    return 294
                if word2 in ['زیورآلات', 'بدلیجات']:
                    return 87
                if word2 in ['شالگردن', 'شال']:
                    return 88
                if word2 == 'کلاه':
                    if (i < len(caption_arr)-1 and caption_arr[i+1] != 'دار') or i == len(caption_arr)-1:
                        return 89
                if word2 in ['کراوات', 'کروات']:
                    return 295
                if word2 == 'پاپیون':
                    return 296
                if word2 == 'ساعت':
                    return 91
                # if word2 == 'ماسک':
                #     return 92
                # if word2 == 'ست':
                #     return 177
            if 'لباس' in caption_arr:
                return 10
            return 2

        if word1 in ['دخترانه', 'دخترونه']:
            i = caption_arr.index(word1)
            if i > 0 and caption_arr[i-1] == 'پیج':
                continue
            for word2 in caption_arr:
                i = caption_arr.index(word2)
                if i > 0 and caption_arr[i-1] == 'پیج':
                    continue

                # girls clothes
                if word2 == 'کت':
                    return 297
                if word2 == 'ست':
                    if i < len(caption_arr)-1:
                        if len(caption_arr)-i > 5:
                            next_words = caption_arr[i+1:i+6]
                        else:
                            next_words = caption_arr[i+1:len(caption_arr)]
                        if any(i in ['رسمی', 'مجلسی', 'کت', 'دامن'] for i in next_words):
                            return 298
                        if any(i in ['ورزشی', 'اسپورت', 'گرمکن', 'لگ', 'لگینگ'] for i in next_words):
                            return 315
                        if any(i in ['لباسزیر', 'شورت', 'شرت', 'سوتین'] for i in next_words):
                            return 330
                        if any(i in ['گردنبند', 'دستبند', 'انگشتر', 'گوشواره', 'آویز', 'زیورآلات', 'بدلیجات'] for i in
                               next_words):
                            return 343
                if word2 in ['پیرهن', 'پیراهن']:
                    return 318
                if word2 == 'لباس':
                    if i < len(caption_arr)-1:
                        if caption_arr[i+1] in ['مجلسی', 'رسمی']:
                            return 102
                        if caption_arr[i+1] in ['ورزشی', 'اسپورت']:
                            return 99
                        if caption_arr[i+1] == 'خواب':
                            return 299
                        if caption_arr[i+1] == 'راحتی':
                            return 300
                        if caption_arr[i+1] == 'شنا':
                            return 104
                    # return 13
                if word2 in ['اسلش', 'شلوار']:
                    return 304
                if word2 in ['سرهمی', 'اورال', 'اورآل']:
                    return 305
                #if word2 in ['بافت', 'ژاکت']:
                if word2 in ['ژاکت']:
                    return 310
                if word2 in ['پولیور', 'پلیور']:
                    return 311
                if word2 == 'کاپشن':
                    return 324
                if word2 == 'پالتو':
                    return 325
                if word2 in ['بارانی', 'بارونی']:
                    return 326
                if word2 in ['جلیقه', 'ژیله']:
                    return 327
                if word2 in ['بلوز', 'بولوز', 'بولیز']:
                    return 321
                if word2 == 'شومیز':
                    return 322
                if word2 == 'شلوارک':
                    return 306
                if word2 in ['شرتک', 'شورتک']:
                    return 307
                if word2 == 'دامن':
                    return 319
                if word2 in ['سارافن', 'سارافون']:
                    return 320
                if word2 in ['لگینگ', 'لگ', 'ساپرت', 'ساپورت']:
                    return 312
                if word2 == 'کاور':
                    return 313
                if word2 == 'گرمکن':
                    return 314
                if word2 == 'نیمتنه':
                    if i < len(caption_arr)-1:
                        if caption_arr[i+1] in ['ورزشی', 'اسپورت']:
                            return 316
                    return 230
                if word2 in ['دستکش', 'دسکش']:
                    if i < len(caption_arr)-1:
                        if caption_arr[i+1] in ['ورزشی', 'اسپورت', 'دروازه', 'بدنسازی']:
                            return 317
                    return 110
                if word2 == 'هدبند':
                    if i < len(caption_arr)-1:
                        if caption_arr[i+1] in ['ورزشی', 'اسپورت']:
                            return 317
                    return 348
                if word2 in ['سوییشرت', 'سویشرت']:
                    return 308
                if word2 == 'هودی':
                    return 309
                if word2 == 'تیشرت':
                    return 301
                if word2 == 'پولوشرت':
                    return 302
                if word2 == 'تاپ':
                    return 303
                if word2 in ['شورت', 'شرت']:
                    return 328
                if word2 == 'سوتین':
                    return 329
                if word2 == 'تونیک':
                    return 323
                if word2 in ['بیکینی', 'مایو', 'بکینی']:
                    return 104
                if word2 in ['لباسزیر', 'زیرپوش']:
                    return 105

                # girls shoes
                if word2 in ['کتانی', 'کتونی'] or (
                        word2 == 'کفش' and i < len(caption_arr)-1 and (caption_arr[i+1] in ['ورزشی', 'اسپورت'])):
                    return 106
                if word2 in ['کفش', 'بوت', 'نیمبوت', 'چکمه', 'پاشنه', 'صندل', 'دمپایی', 'نیمساق']:
                    if 'عطر' not in caption_arr:
                        return 14

                # girls accessories
                if word2 == 'کیف':
                    if i < len(caption_arr)-1:
                        if caption_arr[i+1] == 'پول':
                            return 332
                    return 331
                if word2 == 'کوله':
                    return 333
                if word2 in ['چمدان', 'چمدون']:
                    return 334
                if word2 == 'عینک':
                    return 108
                if word2 in ['پاپوش', 'جوراب']:
                    return 335
                if word2 == 'جورابشلواری':
                    return 336
                if word2 == 'ساق':
                    return 337
                if word2 == 'کمربند':
                    return 111
                if word2 == 'گردنبند':
                    return 338
                if word2 == 'دستبند':
                    return 339
                if word2 == 'انگشتر':
                    return 340
                if word2 == 'گوشواره':
                    return 341
                if word2 == 'آویز':
                    return 342
                if word2 in ['گل', 'سنجاق']:
                    if i < len(caption_arr)-1:
                        if caption_arr[i+1] == 'سینه':
                            return 344
                        if caption_arr[i+1] == 'سر':
                            return 346
                if word2 in ['زیورآلات', 'بدلیجات']:
                    return 112
                if word2 == 'کش':
                    if i < len(caption_arr)-1:
                        if caption_arr[i+1] == 'سر':
                            return 345
                if word2 in ['کلیپس', 'کیلیپس']:
                    return 251
                if word2 == 'کلاه':
                    if (i < len(caption_arr)-1 and caption_arr[i+1] != 'دار') or i == len(caption_arr)-1:
                        return 349
                if word2 in ['شالگردن', 'شال']:
                    return 350
                if word2 == 'ساعت':
                    return 115
                # if word2 == 'ماسک':
                #     return 116
                # if word2 == 'ست':
                #     return 178
            if 'لباس' in caption_arr:
                return 13
            return 3

        if word1 in ['پسرانه', 'پسرونه']:
            i = caption_arr.index(word1)
            if i > 0 and caption_arr[i-1] == 'پیج':
                continue
            for word2 in caption_arr:
                i = caption_arr.index(word2)
                if i > 0 and caption_arr[i-1] == 'پیج':
                    continue

                # boys clothes
                if word2 == 'کت':
                    return 351
                if word2 == 'ست':
                    if i < len(caption_arr)-1:
                        if len(caption_arr)-i > 5:
                            next_words = caption_arr[i+1:i+6]
                        else:
                            next_words = caption_arr[i+1:len(caption_arr)]
                        if any(i in ['رسمی', 'مجلسی', 'کت'] for i in next_words):
                            return 352
                        if any(i in ['ورزشی', 'اسپورت', 'گرمکن', 'لگ', 'لگینگ'] for i in next_words):
                            return 369
                        if any(i in ['لباسزیر', 'شورت', 'شرت'] for i in next_words):
                            return 377
                        if any(i in ['گردنبند', 'دستبند', 'انگشتر', 'گوشواره', 'آویز', 'زیورآلات', 'بدلیجات'] for i in
                               next_words):
                            return 388
                if word2 in ['پیرهن', 'پیراهن']:
                    return 124
                if word2 == 'لباس':
                    if i < len(caption_arr)-1:
                        if caption_arr[i+1] in ['مجلسی', 'رسمی']:
                            return 126
                        if caption_arr[i+1] in ['ورزشی', 'اسپورت']:
                            return 123
                        if caption_arr[i+1] == 'خواب':
                            return 353
                        if caption_arr[i+1] == 'راحتی':
                            return 354
                        if caption_arr[i+1] == 'شنا':
                            return 128
                    # return 16
                if word2 in ['اسلش', 'شلوار']:
                    return 358
                if word2 in ['سرهمی', 'اورال', 'اورآل']:
                    return 359
                # if word2 in ['بافت', 'ژاکت']:
                if word2 in ['ژاکت']:
                    return 364
                if word2 in ['پولیور', 'پلیور']:
                    return 365
                if word2 == 'کاپشن':
                    return 371
                if word2 == 'پالتو':
                    return 372
                if word2 in ['بارانی', 'بارونی']:
                    return 373
                if word2 in ['جلیقه', 'ژیله']:
                    return 374
                if word2 in ['بلوز', 'بولوز', 'بولیز']:
                    return 125
                if word2 == 'شلوارک':
                    return 360
                if word2 in ['شرتک', 'شورتک']:
                    return 361
                if word2 in ['لگینگ', 'لگ', 'ساپرت', 'ساپورت']:
                    return 366
                if word2 == 'کاور':
                    return 367
                if word2 == 'گرمکن':
                    return 368
                if word2 in ['دستکش', 'دسکش']:
                    if i < len(caption_arr)-1:
                        if caption_arr[i+1] in ['ورزشی', 'اسپورت', 'دروازه', 'بدنسازی']:
                            return 370
                    return 134
                if word2 == 'هدبند':
                    if i < len(caption_arr)-1:
                        if caption_arr[i+1] in ['ورزشی', 'اسپورت']:
                            return 370
                if word2 in ['سوییشرت', 'سویشرت']:
                    return 362
                if word2 == 'هودی':
                    return 363
                if word2 == 'تیشرت':
                    return 355
                if word2 == 'پولوشرت':
                    return 356
                if word2 == 'تاپ':
                    return 357
                if word2 in ['شورت', 'شرت']:
                    return 375
                if word2 == 'مایو':
                    return 128
                if word2 in ['رکابی', 'زیرپوش']:
                    return 376
                if word2 == 'لباسزیر':
                    return 129

                # boys shoes
                if word2 in ['کتانی', 'کتونی'] or (
                        word2 == 'کفش' and i < len(caption_arr)-1 and (caption_arr[i+1] in ['ورزشی', 'اسپورت'])):
                    return 130
                if word2 in ['کفش', 'بوت', 'نیمبوت', 'چکمه', 'پاشنه', 'صندل', 'دمپایی', 'نیمساق']:
                    if 'عطر' not in caption_arr:
                        return 17

                # boys accessories
                if word2 == 'کیف':
                    if i < len(caption_arr)-1:
                        if caption_arr[i+1] == 'پول':
                            return 379
                    return 378
                if word2 == 'کوله':
                    return 380
                if word2 in ['چمدان', 'چمدون']:
                    return 381
                if word2 == 'عینک':
                    return 132
                if word2 in ['پاپوش', 'جوراب']:
                    return 382
                if word2 == 'ساق':
                    return 383
                if word2 == 'کمربند':
                    return 135
                if word2 == 'گردنبند':
                    return 384
                if word2 == 'دستبند':
                    return 385
                if word2 == 'انگشتر':
                    return 386
                if word2 == 'آویز':
                    return 387
                if word2 in ['زیورآلات', 'بدلیجات']:
                    return 136
                if word2 in ['شالگردن', 'شال']:
                    return 390
                if word2 == 'کلاه':
                    if (i < len(caption_arr)-1 and caption_arr[i+1] != 'دار') or i == len(caption_arr)-1:
                        return 389
                if word2 in ['کراوات', 'کروات']:
                    return 461
                if word2 == 'پاپیون':
                    return 462
                if word2 == 'ساعت':
                    return 138
                # if word2 == 'ماسک':
                #     return 139
            if 'لباس' in caption_arr:
                return 16
            return 4

        if word1 in ['نوزاد', 'کودک', 'کودکانه', 'بچگانه', 'بچگونه', 'نوزادی']:
            i = caption_arr.index(word1)
            if i > 0 and caption_arr[i-1] == 'پیج':
                continue
            for word2 in caption_arr:
                i = caption_arr.index(word2)
                if i > 0 and caption_arr[i-1] == 'پیج':
                    continue

                # babies clothes
                if word2 == 'کت':
                    return 391
                if word2 == 'ست':
                    if i < len(caption_arr)-1:
                        if len(caption_arr)-i > 5:
                            next_words = caption_arr[i+1:i+6]
                        else:
                            next_words = caption_arr[i+1:len(caption_arr)]
                        if any(i in ['رسمی', 'مجلسی', 'کت', 'دامن'] for i in next_words):
                            return 392
                        if caption_arr[i+1] == 'راحتی':
                            return 411
                        if any(i in ['گردنبند', 'دستبند', 'انگشتر', 'آویز', 'زیورآلات', 'بدلیجات'] for i in next_words):
                            return 483
                if word2 in ['پیرهن', 'پیراهن']:
                    return 147
                if word2 == 'لباس':
                    if i < len(caption_arr)-1:
                        if caption_arr[i+1] in ['مجلسی', 'رسمی']:
                            return 140
                        if caption_arr[i+1] in ['ورزشی', 'اسپورت']:
                            return 414
                        if caption_arr[i+1] == 'خواب':
                            return 141
                        if caption_arr[i+1] == 'راحتی':
                            return 141
                        if caption_arr[i+1] == 'شنا':
                            return 151
                    # return 19
                if word2 in ['اسلش', 'شلوار']:
                    return 413
                if word2 in ['سرهمی', 'اورال', 'اورآل', 'بادی']:
                    return 412
                # if word2 in ['بافت', 'ژاکت']:
                if word2 in ['ژاکت']:
                    return 398
                if word2 in ['پولیور', 'پلیور']:
                    return 399
                if word2 == 'کاپشن':
                    return 400
                if word2 == 'پالتو':
                    return 401
                if word2 in ['بارانی', 'بارونی']:
                    return 402
                if word2 in ['جلیقه', 'ژیله']:
                    return 393
                if word2 in ['بلوز', 'بولوز', 'بولیز']:
                    return 403
                if word2 == 'شومیز':
                    return 404
                if word2 == 'شلوارک':
                    return 146
                if word2 == 'دامن':
                    return 394
                if word2 in ['سارافن', 'سارافون']:
                    return 395
                if word2 in ['دستکش', 'دسکش']:
                    return 467
                if word2 == 'هدبند':
                    return 21
                if word2 in ['سوییشرت', 'سویشرت']:
                    return 396
                if word2 == 'هودی':
                    return 397
                if word2 == 'تیشرت':
                    return 406
                if word2 == 'پولوشرت':
                    return 407
                if word2 == 'تاپ':
                    return 408
                if word2 in ['شورت', 'شرت']:
                    return 152
                if word2 == 'تونیک':
                    return 405
                if word2 in ['بیکینی', 'مایو', 'بکینی']:
                    return 151
                if word2 in ['لباسزیر', 'زیرپوش']:
                    return 152
                if word2 in ['پاپوش', 'جوراب']:
                    return 409
                if word2 == 'جورابشلواری':
                    return 410

                # babies shoes
                if word2 in ['کتانی', 'کتونی'] or (
                        word2 == 'کفش' and i < len(caption_arr)-1 and (caption_arr[i+1] in ['ورزشی', 'اسپورت'])):
                    return 463
                if word2 in ['کفش', 'بوت', 'نیمبوت', 'چکمه', 'پاشنه', 'صندل', 'دمپایی', 'نیمساق']:
                    if 'عطر' not in caption_arr:
                        return 20

                # babies accessories
                if word2 == 'سیسمونی':
                    return 153
                if word2 == 'کیسه':
                    if i < len(caption_arr)-1 and caption_arr[i+1] == 'خواب':
                        return 153
                if word2 == 'کیف':
                    if i < len(caption_arr)-1:
                        if caption_arr[i+1] == 'پول':
                            return 475
                    return 474
                if word2 == 'کوله':
                    return 476
                if word2 in ['چمدان', 'چمدون']:
                    return 477
                if word2 == 'عینک':
                    return 465
                if word2 == 'ساق':
                    return 466
                if word2 == 'کمربند':
                    return 468
                if word2 == 'گردنبند':
                    return 478
                if word2 == 'دستبند':
                    return 479
                if word2 == 'انگشتر':
                    return 480
                if word2 == 'گوشواره':
                    return 481
                if word2 == 'آویز':
                    return 482
                if word2 in ['زیورآلات', 'بدلیجات']:
                    return 469
                if word2 in ['شالگردن', 'شال']:
                    return 471
                if word2 == 'کلاه':
                    if (i < len(caption_arr)-1 and caption_arr[i+1] != 'دار') or i == len(caption_arr)-1:
                        return 470
                if word2 == 'ساعت':
                    return 472
                # if word2 == 'ماسک':
                #     return 473
            if 'لباس' in caption_arr:
                return 19
            return 5

    for word in caption_arr:
        i = caption_arr.index(word)
        if i > 0 and caption_arr[i-1] == 'پیج':
            continue

        # other clothes
        if word == 'کت':
            return 416
        if word == 'ست':
            if i < len(caption_arr)-1:
                if len(caption_arr)-i > 5:
                    next_words = caption_arr[i+1:i+6]
                else:
                    next_words = caption_arr[i+1:len(caption_arr)]
                if any(i in ['رسمی', 'مجلسی', 'کت', 'دامن'] for i in next_words):
                    return 417
                if any(i in ['ورزشی', 'اسپورت', 'گرمکن', 'لگ', 'لگینگ'] for i in next_words):
                    return 438
                if any(i in ['لباسزیر', 'شورت', 'شرت'] for i in next_words):
                    return 169
                if 'سوتین' in next_words:
                    return 233
                if any(i in ['گردنبند', 'دستبند', 'انگشتر', 'گوشواره', 'آویز', 'پابند', 'زیورآلات',
                             'بدلیجات'] for i in next_words):
                    return 457
        if word in ['پیرهن', 'پیراهن']:
            if i < len(caption_arr)-1 and caption_arr[i+1] in ['بارداری', 'حاملگی']:
                return 202
            return 155
        if word == 'لباس':
            if i < len(caption_arr)-1:
                if caption_arr[i+1] in ['مجلسی', 'رسمی']:
                    return 154
                if caption_arr[i+1] in ['ورزشی', 'اسپورت']:
                    return 163
                if caption_arr[i+1] == 'خواب':
                    return 418
                if caption_arr[i+1] == 'راحتی':
                    if i < len(caption_arr)-2 and caption_arr[i+2] in ['بارداری', 'حاملگی']:
                        return 205
                    return 419
                if caption_arr[i+1] == 'شنا':
                    return 168
                if caption_arr[i+1] in ['بارداری', 'حاملگی']:
                    return 31
            # return 22
        if word == 'مانتو':
            if i < len(caption_arr)-1 and caption_arr[i+1] in ['بارداری', 'حاملگی']:
                return 202
            return 192
        if word == 'پانچو':
            return 193
        # if word == 'رویه':
        #     return 194
        if word == 'شنل':
            if 'عطر' not in caption_arr:
                return 195
        if word == 'چادر':
            return 196
        if word == 'مقنعه':
            return 197
        if word in ['اسلش', 'شلوار']:
            if i < len(caption_arr)-1 and caption_arr[i+1] in ['بارداری', 'حاملگی']:
                return 203
            return 420
        if word in ['سرهمی', 'اورال', 'اورآل', 'بادی']:
            if i < len(caption_arr)-1 and caption_arr[i+1] in ['بارداری', 'حاملگی']:
                return 203
            return 421
        # if word in ['بافت', 'ژاکت']:
        if word in ['ژاکت']:
            return 422
        if word in ['پولیور', 'پلیور']:
            return 423
        if word in ['بارداری', 'حاملگی']:
            return 31
        if word == 'کاپشن':
            return 424
        if word == 'پالتو':
            return 425
        if word in ['بارانی', 'بارونی']:
            return 426
        if word in ['جلیقه', 'ژیله']:
            return 427
        if word in ['بلوز', 'بولوز', 'بولیز']:
            if i < len(caption_arr)-1 and caption_arr[i+1] in ['بارداری', 'حاملگی']:
                return 206
            return 428
        if word == 'شومیز':
            if i < len(caption_arr)-1 and caption_arr[i+1] in ['بارداری', 'حاملگی']:
                return 206
            return 429
        if word == 'شلوارک':
            return 431
        if word in ['شرتک', 'شورتک']:
            return 432
        if word == 'دامن':
            if i < len(caption_arr)-1 and caption_arr[i+1] in ['بارداری', 'حاملگی']:
                return 207
            return 433
        if word in ['سارافن', 'سارافون']:
            return 434
        if word in ['لگینگ', 'لگ', 'ساپرت', 'ساپورت']:
            return 435
        if word == 'کاور':
            return 436
        if word == 'گرمکن':
            return 437
        if word == 'نیمتنه':
            if i < len(caption_arr)-1:
                if caption_arr[i+1] in ['ورزشی', 'اسپورت']:
                    return 223
            return 230
        if word in ['دستکش', 'دسکش']:
            if i < len(caption_arr)-1:
                if caption_arr[i+1] in ['ورزشی', 'اسپورت', 'دروازه', 'بدنسازی']:
                    return 439
            return 181
        if word == 'هدبند':
            if i < len(caption_arr)-1:
                if caption_arr[i+1] in ['ورزشی', 'اسپورت']:
                    return 439
            return 252
        if word in ['سوییشرت', 'سویشرت']:
            return 440
        if word == 'هودی':
            return 441
        if word == 'تیشرت':
            if i < len(caption_arr)-1 and caption_arr[i+1] in ['بارداری', 'حاملگی']:
                return 204
            return 442
        if word == 'پولوشرت':
            if i < len(caption_arr)-1 and caption_arr[i+1] in ['بارداری', 'حاملگی']:
                return 204
            return 443
        if word == 'تاپ':
            return 444
        if word in ['شورت', 'شرت']:
            return 169
        if word == 'سوتین':
            return 232
        if word == 'تونیک':
            return 430
        if word in ['بیکینی', 'بکینی']:
            return 41
        if word == 'مایو':
            return 168
        if word in ['لباسزیر', 'زیرپوش']:
            return 169
        if word == 'لامبادا':
            return 231
        if word == 'رکابی':
            return 278

        # other shoes
        if word in ['نیمبوت', 'نیمساق']:
            return 170
        if word == 'بوت':
            return 171
        if word == 'چکمه':
            return 177
        if word == 'گیوه':
            return 172
        if word in ['دمپایی', 'صندل']:
            if 'عطر' not in caption_arr:
                return 173
        if word == 'پاشنه':
            return 47
        if word == 'کفش' and i < len(caption_arr)-1 and (caption_arr[i+1] in ['رسمی', 'مجلسی']):
            return 174
        if word in ['کتانی', 'کتونی'] or (
                word == 'کفش' and i < len(caption_arr)-1 and (caption_arr[i+1] in ['ورزشی', 'اسپورت'])):
            return 175
        if word == 'کالج':
            return 176
        if word == 'کفش':
            return 23

        # other accessories
        if word == 'کیف':
            if i < len(caption_arr)-1:
                if caption_arr[i+1] == 'پول':
                    return 446
            return 445
        if word == 'کوله':
            return 447
        if word in ['چمدان', 'چمدون']:
            return 448
        if word == 'عینک':
            return 179
        if word in ['پاپوش', 'جوراب']:
            return 449
        if word == 'جورابشلواری':
            return 450
        if word == 'ساق':
            return 451
        if word == 'کمربند':
            return 182
        if word == 'ساسبند':
            return 459
        if word == 'گردنبند':
            return 452
        if word == 'دستبند':
            return 453
        if word == 'انگشتر':
            return 454
        if word == 'گوشواره':
            return 455
        if word == 'پیرسینگ':
            return 245
        if word == 'آویز':
            return 456
        if word == 'پابند':
            return 247
        if word == 'دکمه' and (i < len(caption_arr)-1 and caption_arr[i+1] == 'سردست'):
            return 294
        if word in ['گل', 'سنجاق']:
            if i < len(caption_arr)-1:
                if caption_arr[i+1] == 'سینه':
                    return 248
                if caption_arr[i+1] == 'سر':
                    return 250
        if word in ['زیورآلات', 'بدلیجات']:
            return 183
        if word == 'کش':
            if i < len(caption_arr)-1:
                if caption_arr[i+1] == 'سر':
                    return 249
        if word in ['کلیپس', 'کیلیپس']:
            return 251
        if word == 'کلاه':
            if (i < len(caption_arr)-1 and caption_arr[i+1] != 'دار') or i == len(caption_arr)-1:
                return 184
        if word in ['شالگردن', 'شال']:
            return 185
        if word in ['اسکارف', 'روسری']:
            return 255
        if word in ['کراوات', 'کروات']:
            return 295
        if word == 'پاپیون':
            return 296
        if word == 'ساعت':
            return 186
        # if word == 'ماسک':
        #     return 187
    if 'لباس' in caption_arr:
        return 22
        # if word == 'ست':
        #     return 179


def get_category_caption_and_hashtag(caption: str):
    """
    input: caption of post (String)
    output: categoryId of the whole caption (Integer)
    First, we remove hashtags from caption and we get the category from rest of it. We also get the most repetitive word
    in hashtags, if there is any. If the most repetitive word of hashtags wasn't valid, the categoryId will be the same
    as the category of caption without hashtag. Otherwise, the word from hashtag will probably be important in knowing
    the category of post. So, from table "Category" we get the Id of row which its title is that word and its category
    father is similar to the category father of caption without hashtags. If caption without hashtag doesn't have any
    categoryId, but the word is in table "Category", we return the Id of it in table "Category" with father همه.
    """
    # removing hashtags, getting word with reasonable repetition in hashtags, and get the categoryId of rest of caption
    caption, keyword = remove_hashtags(caption)
    categoryId = get_category(caption)

    # hashtag doesn't have word with reasonable repetition
    if not keyword:
        return categoryId

    category_df = pd.read_csv('category.csv')

    # word with reasonable repetition isn't in table "Category"
    if keyword not in list(category_df.Title):
        return categoryId

    # rest of caption doesn't have category and category is in hashtags -> word with reasonable repetition with father همه
    if not categoryId:
        return category_df[category_df.Title == keyword].iloc[-1].Id

    # get origin of rest of caption's category
    fatherId = get_category_father(categoryId, category_df)
    # get categories with title word with reasonable repetition
    similar_categories = category_df[category_df.Title == keyword]

    # iteration over similar_categories
    for index, row in similar_categories.iterrows():
        # get the id of category which its title is word with reasonable repetition and has the same origin as
        # categoryId from rest of caption
        temp_father = get_category_father(row.CategoryId, category_df)
        if fatherId == temp_father:
            return row.Id

    return categoryId
