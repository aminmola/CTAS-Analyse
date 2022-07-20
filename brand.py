import pandas as pd


def add_space(my_brand):
    space_brand = str(my_brand)
    space_brand = space_brand.rjust(len(space_brand) + 1, ' ')
    space_brand = space_brand.ljust(len(space_brand) + 1, ' ')
    return space_brand


brands = pd.read_csv('brands_for_search.csv')
spaced_brands = brands.Title.apply(lambda m: add_space(m))
new_brands = pd.DataFrame(list(zip(brands.Id, spaced_brands)), columns=['Id', 'Title'])


def get_brand(cleaned_caption):

    brand_id = -1
    brand_title = ''
    for j in range(new_brands.shape[0]):
        if new_brands.iloc[j][1] in str(cleaned_caption):
            brand_id = int(brands.iloc[j][0])
            brand_title = str(brands.iloc[j][1])
            break
    return brand_id, brand_title


