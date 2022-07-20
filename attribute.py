import pandas as pd
from caption_cleaner_attribute import clean_caption as cc


def add_space(my_attribute):

    my_attr = my_attribute.rjust(len(my_attribute) + 1, ' ')
    my_attr = my_attr.ljust(len(my_attr) + 1, ' ')
    return my_attr


attributes = pd.read_csv('attributes_for_search.csv')
spaced_attributes = attributes.Title.apply(lambda z: add_space(z))
new_attributes = pd.DataFrame(list(zip(attributes.Id, spaced_attributes)),
                                  columns=['Id', 'Title'])


def get_attribute(caption):

    cleaned_caption = cc(caption)
    print(cleaned_caption)
    if pd.isna(cleaned_caption):
        return []
    attribute_id_list = list()
    for j in range(new_attributes.shape[0]):
        if new_attributes.iloc[j][1] in cleaned_caption:
            attribute_id_list.append(new_attributes.iloc[j][0])
    return attribute_id_list

