"""
The MIT License (MIT)

Copyright (c) <2023> Cybrasaurus

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""
import logging
import json

logging.basicConfig(level=logging.INFO)
# create and init faker generator
    # localized faker gen for Germany
    # --see docs: https://faker.readthedocs.io/en/master/#localization
    # -- docs for different localizations: https://faker.readthedocs.io/en/master/locales.html
from faker import Faker
    # localized provider for Germany: https://faker.readthedocs.io/en/master/locales/de_DE.html
fake = Faker("de_DE")


def generate_name_data(first_name=None, last_name=None, full_name=None, prefix=None, suffix=None,
                       gender_distribution=0.5, prefix_distribution=0.2, suffix_distribution=0.2):
    """

    :param first_name: Whether to generate a first name for the return dictionary
    :param last_name: Whether to generate a last name for the return dictionary
    :param full_name: Whether to generate a full name for the return dictionary, this automatically sets first_name and last_name to TRUE
    :param prefix: Whether to generate a prefix. Defaults to "Herr" or "Frau", gender dependant
    :param suffix: Whether to generate a suffix
    :param gender_distribution: Percentage chance for male or female names. Parameter represents chance for male
    :param prefix_distribution: Percentage chance for a prefix other than "Herr" or "Frau"
    :param suffix_distribution: Percentage chance for a suffix
    :return: return_dict: A dictionary containing all data of the person
    """
    import random
    assert first_name is None or first_name is True, f"Invalid parameter '{first_name}' for parameter first_name, valid options are: [None, True]"
    assert last_name is None or last_name is True, f"Invalid parameter '{last_name}' for parameter last_name, valid options are: [None, True]"
    assert full_name is None or full_name is True, f"Invalid parameter '{full_name}' for parameter full_name, valid options are: [None, True]"
    assert prefix is None or prefix is True, f"Invalid parameter '{prefix}' for parameter prefix, valid options are: [None, True]"
    assert suffix is None or suffix is True, f"Invalid parameter '{suffix}' for parameter suffix, valid options are: [None, True]"
    assert type(
        gender_distribution) == float, f"Invalid parameter '{suffix}' for parameter suffix, valid options are: floats"
    assert type(
        prefix_distribution) == float, f"Invalid parameter '{suffix}' for parameter suffix, valid options are: floats"
    assert type(
        suffix_distribution) == float, f"Invalid parameter '{suffix}' for parameter suffix, valid options are: floats"

    return_dict = {
    }
    # decide whether to generate a male or a female, x<=0.5 is male, x>=0.5 is female
    gender = random.random()
    if gender <= gender_distribution:
        gender = "Male"
    else:
        gender = "Female"

    if full_name is True:
        first_name = True
        last_name = True

    if first_name is True:
        if gender == "Male":
            return_dict["Vorname"] = fake.first_name_male()
        else:
            return_dict["Vorname"] = fake.first_name_female()

    if last_name is True:
        return_dict["Nachname"] = fake.last_name()

    if full_name is True:
        return_dict["Name"] = f"{return_dict['Vorname']} {return_dict['Nachname']}"

    if prefix is True:
        if random.random() <= prefix_distribution:
            return_dict["Anrede"] = fake.prefix_nonbinary()
        else:
            if gender == "Male":
                return_dict["Anrede"] = "Herr"
            else:
                return_dict["Frau"] = "Herr"

    if suffix is True:
        if random.random() <= suffix_distribution:
            return_dict["Titel"] = fake.suffix_nonbinary()

    return return_dict

# TODO generate 1 json per person or have all of them bundled in a list (array)


def generate_adress_data():
    returndict = {}
    tempdict = {}

    tempdict["Straße"] = fake.street_name()
    tempdict["Hausnummer"] = fake.building_number()
    tempdict["PLZ"] = fake.postcode()
    tempdict["Stadt"] = fake.city_name()

    returndict["Adresse"] = tempdict
    return returndict

def make_json_file(input_dict, json_name):
    with open(f"{json_name}.json", "w", encoding="utf-8") as outfile:
        outfile.write(json.dumps(input_dict, indent=2, ensure_ascii=False))


def Dataset_Generator(iterations: int, name_parameters: dict = None, name_bool: bool = False, address_bool: bool = False):

    assert name_bool is True or address_bool is True, "One of the Bools must be true, otherwise there is no data to" \
                                                     " create a json with"

    for i in range(iterations):
        if name_bool is True:
            name_data = generate_name_data(name_parameters)
        else:
            name_data = {}
        if address_bool is True:
            address_data = generate_adress_data()
        else:
            address_data = {}

        # TODO other gens
        dict_to_json = name_data | address_data
        make_json_file(dict_to_json, f"jsons/Dataset{i}")

if __name__ == "__main__":
    Dataset_Generator(iterations=2, address_bool=True)


