# todo: aprire professional / non ho ancora capito come ottenere le credenziali...
# todo: push database

import requests
import datetime
from urllib2 import build_opener

def cleaning(text):
    text = text.replace("DIV", "div")
    text = text.replace("BR", "br")
    text = text.replace("<P", "<p")
    text = text.replace("P>", "p>")
    indexStartAd = text.find('<div')
    while indexStartAd != -1:
        newStart = indexStartAd
        countDent = 1
        while countDent > 0:
            indexIn = text.find('<div', newStart)
            indexEnd = text.find('</div>', newStart)
            if indexIn < indexEnd & indexIn > 0:
                countDent = countDent + 1
                newStart = indexIn
            else:
                countDent = countDent - 1
                newStart = indexEnd
        text = text[:indexStartAd] + text[newStart + 6:]
        indexStartAd = text.find('<div')
    text = text.replace("<strong>", "")
    text = text.replace("<br>", "")
    indexP = text.find('<p')
    while indexP >= 0:
        indexEndP = text.find('>', indexP)
        text = text[:indexP] + text[indexEndP + 1:]
        indexP = text.find('<p')
    text = text.replace("</p>", "")
    indexP = text.find('<span')
    while indexP >= 0:
        indexEndP = text.find('>', indexP)
        text = text[:indexP] + text[indexEndP + 1:]
        indexP = text.find('<span')
    text = text.replace("</span>", "")
    text = text.replace("&agrave;", "a'")
    text = text.replace("&Agrave;", "A'")
    text = text.replace("&Egrave;", "E'")
    text = text.replace("&egrave;", "e'")
    text = text.replace("&Eacute;", "E'")
    text = text.replace("&eacute;", "e'")
    text = text.replace("&Iacute;", "I'")
    text = text.replace("&Ograve;", "O'")
    text = text.replace("&ograve;", "o'")
    text = text.replace("&Oacute;", "O'")
    text = text.replace("&oacute;", "o'")
    text = text.replace("&Uacute;", "U'")
    text = text.replace("&uacute;", "u'")
    text = text.replace("&igrave;", "i'")
    text = text.replace("&rsquo;", "'")
    text = text.replace("&nbsp;", "")
    text = text.replace("</em>", "")
    text = text.replace("<em>", "")
    text = text.replace("</div>", "")
    text = text.replace("<br />", "")
    text = text.replace("</strong>", "")
    #Added some cleaning to the previous function
    text = text.replace("\n", "")
    text = text.replace("  ", " ")
    text = text.replace("   ", "")
    text = text.replace("\t", " ")
    text = text.replace('<br/>', '')
    return text


print datetime.datetime.time(datetime.datetime.now())
# Used to open articles web pages
opener = build_opener()
opener.addheaders = [('User-Agent', 'Mozilla/5.0')]
#todo: check tags properly

list_of_companies = ['A2A', 'Atlantia','Azimut', 'Banca+Generali', 'Banco+BPM', 'BPER', 'Brembo', 'Buzzi+Unicem'
                     'Campari', 'CNH', 'Enel', 'Eni', 'Exor', 'Ferrari', 'FCA', 'Fineco', 'Generali', 'Intesa+Sanpaolo',
                     'Italgas', 'Leonardo', 'Luxottica', 'Mediaset', 'Mediobanca', 'Moncler', 'Pirelli', 'Poste+italiane',
                     'Prysmian', 'Recordati', 'Saipem', 'Ferragamo', 'Snam', 'STMicroelectronics', 'Telecom', 'Tenaris',
                     'Terna', 'UBI', 'UniCredit', 'Unipol', 'UnipolSai', 'Yoox']

with open('secondScriptFINAL.txt', 'a') as the_file:
    the_file.write('START OF THE FILE\n')
    the_file.write(str(datetime.datetime.time(datetime.datetime.now())))

for company in list_of_companies:
    print 'Evaluating company #', list_of_companies.index(company), ' out of 41'

    with open('secondScriptFINAL.txt', 'a') as the_file:
        the_file.write('\nEvaluating company #')
        the_file.write(str(list_of_companies.index(company)))
        the_file.write('out of #41\n')

    # sezione '...' is actually 'Economia'
    post_fields = {'tiponotizia': '',
                   'any': company,
                   'sezione': '63a85942-dedb-4b31-a3bf-a06f721c67e6',
                   'periodo': '',
                   'genere': '',
                   'sort': 'data:desc',
                   'start': '',
                   'rows': '12'}
    # In case page doesn't load correctly, we reload it
    page = ''
    while len(page) < 1000:
        url = 'https://www.ansa.it/ricerca/ansait/search.shtml'
        r = requests.post(url, post_fields)
        page = r.text
        numResultsIndex = page.find('num-result')+12

    # Handles 2,3,4 ciphers numResults
    try:
        numResults = int(page[numResultsIndex:numResultsIndex+4])
    except:
        try:
            numResults = int(page[numResultsIndex:numResultsIndex + 3])
        except:
            try:
                numResults = int(page[numResultsIndex:numResultsIndex + 2])
            except:
                print 'Error in numResults ', company, ' will be skipped'
                numResults = 0
    #We initialize loop variables. Conta is external loop, count is the more internal
    conta = 1
    numRequests = 12;

    while conta <= numResults:
        count = 0
        while count < 12:
            # getting the Block of the news and from there we get all the info we need
            newsIndexStart = page.find('search-content-result')
            newsIndexEnd = page.find('</div>', newsIndexStart)
            newsBlock = page[newsIndexStart:newsIndexEnd]

            # date
            date = newsBlock[newsBlock.find('date">')+6:newsBlock.find('</span>')]

            # category (but we usually have just economia for now )
            categoryIndexStart = newsBlock.find('search-category"') + 17
            categoryIndexEnd = newsBlock.find('</span>', categoryIndexStart)
            category = newsBlock[categoryIndexStart:categoryIndexEnd]

            # NewsTitle and link
            linkIndexStart = newsBlock.find('href="', categoryIndexEnd) + 6
            linkIndexEnd = newsBlock.find('">', linkIndexStart)

            # Sometimes i can't access the news for some reasons, i handle wrong href init
            if linkIndexStart != -1:
                link = 'https://www.ansa.it' + newsBlock[linkIndexStart:linkIndexEnd]
            titleIndexEnd = newsBlock.find('</a>', linkIndexEnd)
            title = newsBlock[linkIndexEnd+2:titleIndexEnd]

            # Abstract article
            absIndexStart = newsBlock.find('<p class="search-abs">', titleIndexEnd) + 22
            absIndexEnd = newsBlock.find('</p>')

            abstract = newsBlock[absIndexStart:absIndexEnd].encode('utf-8')
            '''if abstract.find('<p>') > 0 and len(link) > 19:
                absIndexStart = newsBlock.find('<p>', absIndexStart) + 4
                absIndexEnd = newsBlock.find('</p>', absIndexStart)
                abstract = newsBlock[absIndexStart:absIndexEnd].encode('utf-8')
                # print 'TRUE ONE', abstract, absIndexStart, absIndexStart
            '''
            # I clean the abstract
            # todo: forse replace non e esattamente il metodo migliore da usare
            '''abstract = abstract.replace('<p>', '')
            abstract = abstract.replace('em', '')
            abstract = abstract.replace('<>', '')
            abstract = abstract.replace('</>', '')
            abstract = abstract.replace('\n', '')'''
            abstract = cleaning(abstract)

            count = count + 1

            body = 'Articolo non disponibile'
            if len(date) > 0 and link.find('professional') < 0:
                try:
                    articlePageUrl = opener.open(link)
                    articlePage = articlePageUrl.read()

                    subtitleIndexStart = articlePage.find('news-stit')
                    subtitleIndexEnd = articlePage.find('</h2>', subtitleIndexStart)
                    subtitle = articlePage[subtitleIndexStart:subtitleIndexEnd]

                    bodyStartIndex = articlePage.find('news-txt')
                    bodyStartIndex = articlePage.find('<p>', bodyStartIndex)+3
                    bodyEndIndex = articlePage.find('</p>', bodyStartIndex)
                    body = articlePage[bodyStartIndex:bodyEndIndex].decode("utf-8")
                    # I clean the body
                    '''body = body.replace("\n", "")
                    body = body.replace("  ", " ")
                    body = body.replace("   ", "")
                    body = body.replace("\t", " ")
                    body = body.replace("<br>", "")
                    body = body.replace("</br>", '')
                    body = body.replace('<br/>', '')
                    body = body.replace("&nbsp;", "")'''
                    body = cleaning(body)
                    body = body.encode("utf-8")
                except:
                    print 'Url was not found'

            print company, conta, '/', numResults, ':', title, date, category, link, abstract
            print 'ARTICOLO: ', body

            with open('secondScriptFINAL.txt', 'a') as the_file:
                the_file.write('\n\n')
                the_file.write(company)
                the_file.write(' --- ')
                the_file.write(str(conta))
                the_file.write(' / ')
                the_file.write(str(numResults))
                the_file.write(' ---- on Date: ')
                the_file.write(str(date))
                the_file.write('\nTitle: ')
                the_file.write(title)
                the_file.write('\nCategory: ')
                the_file.write(category)
                the_file.write('\nLink: ')
                the_file.write(link)
                the_file.write('\nAbstract: ')
                the_file.write(abstract)
                the_file.write('\nARTICOLO: ')
                the_file.write(body)

            # I consider the next article block
            # omitting len(page) because [index:] means from index to the end
            page = page[newsIndexStart+absIndexEnd:]
            conta = conta + 1
            if conta > numRequests:
                count = count + 12
        # Properly handling request
        inc = 12
        if(numRequests+12) >= numResults:
            inc = abs((numResults - conta))
        numRequests = numRequests + inc

        post_fields = {'tiponotizia': '',
                       'any': company,
                       'sezione': '63a85942-dedb-4b31-a3bf-a06f721c67e6',
                       'periodo': '',
                       'genere': '',
                       'sort': 'data:desc',
                       'start': numRequests-inc,
                       'rows':  '12'}
        page = ''
        # Sometime page doesn't load. With this i assure that page loads.
        while len(page) < 1000:
            url = 'https://www.ansa.it/ricerca/ansait/search.shtml'
            r = requests.post(url, post_fields)
            page = r.text
        # end of articles loop
    # end of companies loop
# end of file
print datetime.datetime.time(datetime.datetime.now())

with open('secondScriptFINAL.txt', 'a') as the_file:
    the_file.write('\nEND OF THE FILE\n')
    the_file.write(str(datetime.datetime.time(datetime.datetime.now())))
