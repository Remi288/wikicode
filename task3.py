# Task 3
# -------- Item/Article title and description use for the script------------
# Ocean liner(item title)
# --ship designed to transport people from one seaport to another(desc)
# passenger ship(item title)
# --watercraft intended to carry people onboard(desc)

# Import modules
import pywikibot
from pywikibot.data import api
from pywikibot import pagegenerators
import requests
import pprint
import re 


def prettyPrint(variable):
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(variable)

def search_entities(site, query: str)-> dict:
    """Make a request to the MediaWiki API using the inputted parameters

    Args:
        site ([site repo]): the site repository
        itemtitle ([str]): an article title or term

    Returns:
        [dict]: the result of the request to the API
    """
    params = { 'action' :'wbsearchentities', 
                'format' : 'json',
                'language' : 'en',
                'type' : 'item',
                'search': query[0]}

    try:
        request = api.Request(site=site, parameters=params)
        dataEntries = request.submit()
        return dataEntries
    except:
        print("ERORR: Request to Mediawiki API failed")
        return


def itemTitle_desCheck(query, label_match, enwiki_repo):
    """This double-check the item/Article title QID using addtional info(descriptio)

    Args:
        query ([list]): Article title or item/sting title and addtional info(description)
        label_match ([list]): list of a label match 
        enwiki_repo ([site repo]): the site repository
    """
    
    for qid_check in label_match:

                item = pywikibot.ItemPage(enwiki_repo, qid_check)
                wd_item=item.get()



                descriptions=wd_item['descriptions']['en']
                x=re.findall(query[1], descriptions,flags=re.IGNORECASE)

                for value in x:
                    print("v", value)
                    if value.lower()==query[1].lower():
                        print(f"QID Match: {query[0]}-->{value}-->{qid_check}")


def itemtitle_label_check(query, dataEntries, enwiki_repo):
    """Item label check match

    Args:
        query ([list]): Article title or item/sting title and addtional info(description)
        dataEntries ([dict]): the result of the request to the API
        enwiki_repo ([site repo]): the site repository

    Returns:
        [List]: label match
    """
    label_match= []

    for data in dataEntries['search']: 
        item = pywikibot.ItemPage(enwiki_repo, data['title']) 
        wikidata_item=item.get()

        try:
            label=wikidata_item['labels']['en']
            print("label",label)
            if label==query[0]:
                label_match.append(data['title'])

        except: 
            print("Label do not match")
            return

    if len(label_match)>1:
        itemTitle_desCheck(query, label_match, enwiki_repo)
        return label_match 
    elif len(label_match)==0: 
        print("No match found in Wikidata Connected Pages")
    elif len(label_match)==1: 
        print(label_match[0])
    

# Unconnected pages

# def unconnected():
#     enwp = pywikibot.Site('en', 'wikipedia')
#     enwd = pywikibot.Site('wikidata', 'wikidata')
#     targetcats = ['Category:Articles_without_Wikidata_item']

#     for targetcat in targetcats:
#         cat = pywikibot.Category(enwp, targetcat)
#         pages = enwiki.querypage('UnconnectedPages')
#         pagey = pagegenerators.CategorizedPageGenerator(cat, recurse=False);
#         print(pagey)
#         


def main():
    # Connect to wikipedia
    enwiki = pywikibot.Site('en', 'wikipedia')
    enwiki_repo = enwiki.data_repository()
    query_info = input("Article/item title or label ")
    query = []
    query.append(query_info)
    if len(query) < 2:
        adinfo = input("Additon-Info: Article/Item Desc ")
        query.append(adinfo)
    dataEntries = search_entities(enwiki_repo, query)
    prettyPrint(dataEntries)
    label_match = itemtitle_label_check(query, dataEntries, enwiki_repo)
    print(itemTitle_desCheck(query, label_match, enwiki_repo))

if __name__ == '__main__':
    main()