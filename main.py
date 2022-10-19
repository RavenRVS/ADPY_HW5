import csv
import re
import os
from trace_dec import trace_decorator

with open("phonebook_raw.csv", "r", encoding="utf-8") as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)

# TODO 1: выполните пункты 1-3 ДЗ

surname_list = []
name_list = []
patronymic_list = []
org_list = []
position_list = []
phone_list = []
email_list = []

title_sur = contacts_list[0][0]
title_name = contacts_list[0][1]
title_pat = contacts_list[0][2]
title_org = contacts_list[0][3]
title_pos = contacts_list[0][4]
title_pho = contacts_list[0][5]
title_eml = contacts_list[0][6]

pattern = r'([а-яА-ЯёЁ]+)'
pattern2 = r'([а-яА-ЯёЁ]+)\s*([а-яА-ЯёЁ]+)'
pattern3 = r'([а-яА-ЯёЁ]+)\s*([а-яА-ЯёЁ]+)\s*([а-яА-ЯёЁ]+)'
pattern4 = '.*'
pattern_phone = r'(\+7|8)+\s?\(?(\d{3})\)?\D?(\d{3})\D?(\d{2})\D?(\d{2})\s?\(?(доб.)?\s?(\d*)'


def get_surname(cont_list):
    for contact in cont_list:
        if contact[0] == title_sur:
            pass
        else:
            surname = re.match(pattern, contact[0])
            surname_list.append(surname.group(0))


def get_name(cont_list):
    for contact in cont_list:
        name = re.search(pattern, contact[1])
        name2 = re.search(pattern2, contact[0])
        name3 = re.search(pattern3, contact[0])

        if contact[1] == title_name:
            pass
        elif name is not None:
            name_list.append(name.group(1))
        elif name2 is not None:
            name_list.append(name2.group(2))
        else:
            name_list.append(name3.group(2))


def get_patronymic(cont_list):
    for contact in cont_list:
        patronymic = re.search(pattern, contact[2])
        patronymic2 = re.match(pattern2, contact[1])
        patronymic3 = re.search(pattern3, contact[0])

        if contact[2] == title_pat:
            pass
        elif patronymic is not None:
            patronymic_list.append(patronymic.group(1))
        elif patronymic2 is not None:
            patronymic_list.append(patronymic2.group(2))
        else:
            patronymic_list.append(patronymic3.group(3))


def get_organisation(cont_list):
    for contact in cont_list:
        org = re.search(pattern, contact[3])
        if contact[3] == title_org:
            pass
        elif org is None:
            org_list.append("")
        else:
            org_list.append(org.group(0))


def get_position(cont_list):
    for contact in cont_list:
        pos = re.search(pattern4, contact[4])
        if contact[4] == title_pos:
            pass
        elif pos is None:
            position_list.append("")
        else:
            position_list.append(pos.group(0))


def get_phone(cont_list):
    for contact in cont_list:
        phone = re.search(pattern_phone, contact[5])
        if contact[5] == title_pho:
            pass
        elif phone is None:
            phone_list.append("")
        elif phone.group(6) is not None:
            phone_list.append(
                f'+7({phone.group(2)}){phone.group(3)}-{phone.group(4)}-{phone.group(5)} доб.{phone.group(7)}')
        else:
            phone_list.append(f'+7({phone.group(2)}){phone.group(3)}-{phone.group(4)}-{phone.group(5)}')


def get_email(cont_list):
    for contact in cont_list:
        email = re.search(pattern4, contact[6])
        if contact[6] == title_eml:
            pass
        elif email is None:
            email_list.append("")
        else:
            email_list.append(email.group(0))


@trace_decorator(path=os.getcwd())
def sort_contacts(cont_list):
    get_surname(cont_list)
    get_name(cont_list)
    get_patronymic(cont_list)
    get_phone(cont_list)
    get_organisation(cont_list)
    get_position(cont_list)
    get_email(cont_list)

    temp_dict = {}

    for i in range(0, len(surname_list)):
        full_name = f'{surname_list[i]} {name_list[i]}'
        if full_name not in temp_dict:
            temp_dict[f'{surname_list[i]} {name_list[i]}'] = [patronymic_list[i], org_list[i], position_list[i],
                                                              phone_list[i], email_list[i]]
        else:
            if temp_dict[full_name][0] == "" and patronymic_list[i] != "":
                temp_dict[full_name][0] = patronymic_list[i]
            if temp_dict[full_name][1] == "" and org_list[i] != "":
                temp_dict[full_name][1] = org_list[i]
            if temp_dict[full_name][2] == "" and position_list[i] != "":
                temp_dict[full_name][2] = position_list[i]
            if temp_dict[full_name][3] == "" and phone_list[i] != "":
                temp_dict[full_name][3] = phone_list[i]
            if temp_dict[full_name][4] == "" and email_list[i] != "":
                temp_dict[full_name][4] = email_list[i]

    sorted_contact_list = [[title_sur, title_name, title_pat, title_org, title_pos, title_pho, title_eml]]

    for i in temp_dict:
        contact = [i.split(" ")[0], i.split(" ")[1], temp_dict[i][0], temp_dict[i][1], temp_dict[i][2], temp_dict[i][3],
                   temp_dict[i][4]]
        sorted_contact_list.append(contact)
    return sorted_contact_list


sort_list = sort_contacts(contacts_list)

# TODO 2: сохраните получившиеся данные в другой файл
# код для записи файла в формате CSV
with open("phonebook.csv", "w", encoding="utf-8") as f:
    data_writer = csv.writer(f, delimiter=',')
    # Вместо contacts_list подставьте свой список
    data_writer.writerows(sort_list)
