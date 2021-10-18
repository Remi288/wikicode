import pywikibot


# List of wikidata pages
wd_pages = []
# Connect to wikipedia
enwiki = pywikibot.Site('en', 'wikipedia')
enwiki_repo = enwiki.data_repository()
page = pywikibot.Page(enwiki_repo, 'User:Ope28/Outreachy 1')
print (page.text)

# edit page
def editpage(page):
    text = page.get()
    text = text + "\nHello"
    page.text = text
    try:
        page.save("Saving test edit")
        return 1
    except:
        print ("That didn't work!")
        return 0

# Print wikidata
def printwikidata(wd_item):
    qid = wd_item.title()
    print (qid)

    item_dict = wd_item.get()

    try:
        print ('Name: ' + item_dict['labels']['en'])
    except:
        print ('No English label!')
    try:
        print (item_dict['claims']['P31'])
    except:
        print ('No P31')

    try:
        for claim in item_dict['claims']['P31']:
            p31_value = claim.getTarget()
            p31_item_dict = p31_value.get()
            print ('P31 value: ' + p31_value.title())
            print ('P31 label: ' + p31_item_dict['labels']['en'])
    except:
        print ("That didn't work!")
    return 0

edited_page = editpage(page)
print(edited_page)

# Get page from wikidata sandbox and from wikidata in User:Ope28/Outreachy 1 
page_sandbox = pywikibot.ItemPage(enwiki_repo, 'Q4115189')
page1 = pywikibot.ItemPage(enwiki_repo, 'Q14592615')
page2 = pywikibot.ItemPage(enwiki_repo, 'Q2055880')
page3 = pywikibot.ItemPage(enwiki_repo, 'Q320466')
page4 = pywikibot.ItemPage(enwiki_repo, 'Q1323171')
wd_pages.extend((page_sandbox, page1, page2, page3, page4))

# print all wikidata pages
for page in wd_pages:
    print(printwikidata(page))
print("Done!")
