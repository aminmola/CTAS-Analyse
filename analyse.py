from price import Transform as priceClass
from size import Transform as sizeClass
from shipping import shipping
from brand import get_brand
import pandas as pd
from attribute import get_attribute
from clean_caption import clean_caption
import get_category as gc
import get_materials as gm
from get_colors import get_colors
from unidecode import unidecode
from hazm import *
import re

normalizer = Normalizer()

def cleaning(normalizer: Normalizer, caption: str):
    """Cleaning raw Caption
    :Parameters
    ------------------
    Raw Caption of the post

    :returns
    ------------------
    Caption
    1 - with no persian number : DONE
    2 - whole space instead of half space : DONE
    3 - with Homogenization of char 'ک' : ...
    4 - with Homogenization of char "ی" : DONE
    5 - eradicate the hashtag in the middle of caption : ...
    6 - ...
    """

    ### normalize the caption
    caption = normalizer.normalize(caption)


    ### 1 - with no persian number###
    caption = re.split('', caption)
    for i in range(len(caption)):
        if unidecode(caption[i]).isnumeric():
            caption[i] = unidecode(caption[i])
    caption = ''.join(caption)
    ##############################

    ### 2 - whole space instead of half space###
    caption = caption.replace('\u200c', " ")
    caption = caption.replace('آ', "ا")

    ##############################
    return caption

def analyse(cap):


    ## input : caption
    ## output : json for price, shipping , ...
    cap = cleaning(normalizer, cap)
    caption = clean_caption(cap)
    #### can we extract price,shipping information, ...?

    ########################################################PRICE#############################################################


    price = priceClass()
    price_tips = list()
    func = lambda x: True if price.extract_price(x, price.get_index_price_word(x))[0] else False
    price_caption = price.clean_caption(cap)
    has_price = func(price_caption)
    if not has_price:
        price_tips.append("لطفا قیمت کالا را دقیق وارد کنید")
    if has_price and not price.has_currency(price_caption):
        price_tips.append("بهتر است واحد قیمت کالا را انتخاب کنید")
    price_grade = 70 * int(has_price) + 30 * int(price.has_currency(price_caption) and has_price)


    ########################################################PRICE#############################################################

    ########################################################SHIPPING#############################################################
    shipping_grade = 0
    shipping_tips = list()
    shipping_information = shipping(cap)
    if not shipping_information[0]:
        shipping_tips.append("اگر امکان خرید حضوری دارید بهتر است ادرس را وارد کنید")
    else:
        shipping_grade = shipping_grade + 10

    if not shipping_information[1]:
        shipping_tips.append("بهتر است هزینه ارسال را مشخص نمایید")
    else:
        shipping_grade = shipping_grade + 35
    if not shipping_information[3]:
        shipping_tips.append("بهتر است برای ارسال یکی از روش های موجود را انتخاب کنید")
    else:
        shipping_grade = shipping_grade + 30
    if not shipping_information[4]:
        shipping_tips.append("اگر امکان مرجوعی کالا را دارید لطفا ذکر نمایید.")
    else:
        shipping_grade = shipping_grade + 15
    if not shipping_information[5]:
        shipping_tips.append("اگر امکان تعویض کالا را دارید لطفا ذکر نمایید.")
    else:
        shipping_grade = shipping_grade + 10




    ########################################################SHIPPING#############################################################

    ########################################################CATEGORY & MATERIAL#############################################################

    grade = 0
    tips = list()
    category = gc.get_category_caption_and_hashtag(cap)
    if pd.isna(category):
        tips.append("لطفا دسته بندی محصول خود را انتخاب نمایید")
    else:
        grade = grade + 30

    ###MATERIAL

    materials = gm.get_materials(cap)
    if not materials:
        tips.append("بهتر است جنس کالا را انتخاب و یا وارد نمایید")
    else:
        grade = grade + 15


    ########################################################CATEGORY & MATERIAL#############################################################

    #########################################################BRAND & SIZE & ATTRIBUTE & COLOR #############################################################
    ###BRAND

    func_brand = lambda x: True if get_brand(x)[1] else False
    has_brand = func_brand(" " + cap + " ")
    if not has_brand:
        tips.append("بهتر است برند کالا را انتخاب و یا وارد نمایید")
    else:
        grade = grade + 15

    ###SIZE
    size = sizeClass()
    record = {'Caption': cap, 'category': category}
    sizes = size.get_size(record)
    if not sizes:
        tips.append("بهتر است از جدول سایز ها، سایزهای موجود کالای خود را وارد کنید")
    else:
        grade = grade + 15

    ###ATTRIBUTE

    func_attribute = lambda x: True if get_attribute(x) else False
    has_attribute = func_attribute(cap)
    if not has_attribute:
        tips.append("بهتر است طرح و مدل کالای خود را وارد نمایید")
    else:
        grade = grade + 10
    ###COLOR
    colors = get_colors(cap)
    if not colors:
        tips.append("بهتر است از جدول رنگ ها، رنگهای موجود کالای خود را وارد کنید")
    else:
        grade = grade + 15

    ##########################################################BRAND & SIZE & ATTRIBUTE & COLOR#############################################################

    ##########################################overall grade json output################################################

    overall_grade = (price_grade * 30 + shipping_grade * 20 + grade * 30 + grade * 20) / 100
    output = {"overall_grade": overall_grade, "price": {"price_grade": price_grade, "price_tips": price_tips}, "shipping": {"shipping_grade": shipping_grade, "shipping_tips": shipping_tips}, "category_material_brand_size_attribute_colo": {"category_material_brand_size_attribute_color": grade, "category_material_brand_size_attribute_color_tips": tips}}
    ##########################################overall grade json output################################################

    return output

