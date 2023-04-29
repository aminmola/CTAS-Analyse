from unidecode import unidecode
import re
import requests


def cleaning(caption: str):
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

    # caption = normalizer.normalize(caption)

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
    cap = cleaning(cap)

    def has_currency(cleaned_caption):
        has_unit = False
        unit_words = ['میلیون', 'تومان', 'تومن', 'لیر', 'تل', 'تله', 'هزار', 'ت', 'هزارتومان', 'ریال', 'دلار', 'یورو',
                      ' t ']
        for word in unit_words:
            if word in cleaned_caption:
                has_unit = True
                break

        return has_unit

    # caption = clean_caption(cap)
    #### can we extract price,shipping information, ...?
    ########################################################PRICE#############################################################
    url = "http://192.168.110.45:10009/price_manual_set"
    params = {"caption": f"{cap}"}
    vec = requests.request("POST", url, params=params)
    price_tips = list()
    has_price = 1
    if vec.json()['data'][0]['Price'] == "":
        price_tips.append("لطفا قیمت کالا را دقیق وارد کنید")
        has_price = 0
    if has_price and not has_currency(cap):
        price_tips.append("بهتر است واحد قیمت کالا را انتخاب کنید")
    price_grade = 70 * int(has_price) + 30 * int(has_currency(cap) and has_price)

    ########################################################PRICE#############################################################

    ########################################################SHIPPING#############################################################
    shipping_grade = 0
    shipping_tips = list()
    url = "http://192.168.110.45:10011/shipping_manual_set"
    params = {"caption": f"{cap}"}
    vec = requests.request("POST", url, params=params)
    if not vec.json()['data'][0]['BuyInPerson']:
        shipping_tips.append("اگر امکان خرید حضوری دارید بهتر است ادرس را وارد کنید")
    else:
        shipping_grade = shipping_grade + 10

    if not vec.json()['data'][0]['ShippingPrice']:
        shipping_tips.append("بهتر است هزینه ارسال را مشخص نمایید")
    else:
        shipping_grade = shipping_grade + 35
    if not vec.json()['data'][0]['ShippingOption']:
        shipping_tips.append("بهتر است برای ارسال یکی از روش های موجود را انتخاب کنید")
    else:
        shipping_grade = shipping_grade + 30
    if not vec.json()['data'][0]['ReturnOption']:
        shipping_tips.append("اگر امکان مرجوعی کالا را دارید لطفا ذکر نمایید.")
    else:
        shipping_grade = shipping_grade + 15
    if not "تعویض" in cap:
        shipping_tips.append("اگر امکان تعویض کالا را دارید لطفا ذکر نمایید.")
    else:
        shipping_grade = shipping_grade + 10

    ########################################################SHIPPING#############################################################

    ########################################################CATEGORY & MATERIAL#############################################################

    grade = 0
    tips = list()
    url = "http://192.168.110.45:10004/category_manual_set"
    params = {"caption": f"{cap}"}
    vec = requests.request("POST", url, params=params)
    if vec.json()['data'][0]['CategoryId'] < 6:
        tips.append("لطفا دسته بندی محصول خود را انتخاب نمایید")
    else:
        grade = grade + 30

    ###MATERIAL

    url = "http://192.168.110.45:10007/material_manual_set"
    params = {"caption": f"{cap}"}
    vec = requests.request("POST", url, params=params)
    if not vec.json()['data'][0]['MaterialId']:
        tips.append("بهتر است جنس کالا را انتخاب و یا وارد نمایید")
    else:
        grade = grade + 15

    ########################################################CATEGORY & MATERIAL#############################################################

    #########################################################BRAND & SIZE & ATTRIBUTE & COLOR #############################################################
    ###BRAND

    url = "http://192.168.110.45:10003/brand_manual_set"
    params = {"caption": f"{cap}"}
    vec = requests.request("POST", url, params=params)
    if vec.json()['data'][0]['BrandId'] == -1:
        tips.append("بهتر است برند کالا را انتخاب و یا وارد نمایید")
    else:
        grade = grade + 15

    ###SIZE
    url = "http://192.168.110.45:10012/size_manual_set"
    params = {"caption": f"{cap}"}
    vec = requests.request("POST", url, params=params)
    if not vec.json()['data'][0]['SizeId']:
        tips.append("بهتر است از جدول سایز ها، سایزهای موجود کالای خود را وارد کنید")
    else:
        grade = grade + 15

    ###ATTRIBUTE
    url = "http://192.168.110.45:10002/attribute_manual_set"
    params = {"caption": f"{cap}"}
    vec = requests.request("POST", url, params=params)
    if not vec.json()['data'][0]['Attributes']:
        tips.append("بهتر است طرح و مدل کالای خود را وارد نمایید")
    else:
        grade = grade + 10
    ###COLOR
    url = "http://192.168.110.45:10005/color_manual_set"
    params = {"caption": f"{cap}"}
    vec = requests.request("POST", url, params=params)
    if not vec.json()['data'][0]['ColorId']:
        tips.append("بهتر است از جدول رنگ ها، رنگهای موجود کالای خود را وارد کنید")
    else:
        grade = grade + 15

    ##########################################################BRAND & SIZE & ATTRIBUTE & COLOR#############################################################

    ##########################################overall grade json output################################################

    overall_grade = (price_grade * 30 + shipping_grade * 20 + grade * 30 + grade * 20) / 100
    output = {"overall_grade": overall_grade, "price": {"price_grade": price_grade, "price_tips": price_tips},
              "shipping": {"shipping_grade": shipping_grade, "shipping_tips": shipping_tips},
              "category_material_brand_size_attribute_colo": {"category_material_brand_size_attribute_color": grade,
                                                              "category_material_brand_size_attribute_color_tips": tips}}
    ##########################################overall grade json output################################################

    return output
