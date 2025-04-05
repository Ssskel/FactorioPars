import requests
import re
from bs4 import BeautifulSoup
from colorama import Fore, init
import xml.etree.ElementTree as ET

init(autoreset=True)

links = ["https://wiki.factorio.com/Template:LogisticsNav",
         "https://wiki.factorio.com/Template:ProductionNav",
         "https://wiki.factorio.com/Template:IntermediateNav",
         "https://wiki.factorio.com/Template:SpaceNav",
         "https://wiki.factorio.com/Template:CombatNav",
         "https://wiki.factorio.com/Template:EnvironmentNav",
         'https://wiki.factorio.com/Template:TechNav']

root = ET.Element("library")

sub_category = None
for link in links:
    response = requests.get(link).text
    soup = BeautifulSoup(response, "lxml")

    block = soup.find('div', {'id': "mw-content-text"})
    tag_table = block.find('table', {'class': "navbox-inner"})
    tag_tr = tag_table.find_all('tr')

    for tag_tr_iter in tag_tr:
        tag_td_gd = tag_tr_iter.find('td', {'class': "group-data"})
        tag_td_ld = tag_tr_iter.find('td', {'class': "list-data"})

        if tag_td_gd:
            tag_p = tag_td_gd.find('p')
            if tag_p and tag_p.text.strip() == 'Navigation':
                continue
            else:
                div_tag = tag_td_gd.find('div')
                if div_tag:
                    title_div = div_tag.text.strip()
                    print(Fore.GREEN + title_div + ':')
                    if sub_category is not None:
                        sub_category = None
                    sub_category = ET.SubElement(category, 'sub_category')
                    sub_category.set('name', title_div)
        else:
            tag_th = tag_tr_iter.find('th', {'class': "navbox-header"})
            if tag_th:
                div_tag = tag_th.find('div')
                if div_tag:
                    title_div = div_tag.text.strip()
                    print(Fore.RED + '-----' + title_div + '-----')
                    category = ET.SubElement(root, 'category')
                    category.set('name', title_div)

        if tag_td_ld:
            li_tag = tag_td_ld.find_all('li')
            for li_tag_iter in li_tag:
                title_li = li_tag_iter.find('a').get('title', '')
                print(title_li)
                if sub_category is not None:
                    title = ET.SubElement(sub_category, 'title')
                    title.text = title_li


def prettify(elem):
    from xml.dom import minidom
    rough_string = ET.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")

with open("library.xml", "w", encoding="utf-8") as file:
    file.write(prettify(root))

print(Fore.YELLOW + "XML файл згенеровано: library.xml")
