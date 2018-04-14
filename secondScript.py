# todo: DOING aprire articoli e prendere le informazioni ma serve autenticazione occasionalmente
# todo: push database
# todo fix mod 12
# todo: ogni tanto il server di ansa non risponde correttamente quindi abbiamo dei campi vuoti a caso
# todo: bisognerebbe quindi refreshare la pagina credo

# Second code
import requests
from urllib2 import build_opener

# Used to open articles web pages
opener = build_opener()
opener.addheaders = [('User-Agent', 'Mozilla/5.0')]

list_of_companies = ['A2A', 'Atlantia','Azimut', 'Banca Generali', 'Banco BPM', 'BPER', 'Brembo', 'Buzzi Unicem',
                     'Campari', 'CNH', 'Enel', 'Eni', 'Exor', 'Ferrari', 'FCA', 'Fineco', 'Generali', 'Intesa Sanpaolo',
                     'Italgas', 'Leonardo', 'Luxottica', 'Mediaset', 'Mediobanca', 'Moncler', 'Pirelli', 'Poste italiane',
                     'Prysmian', 'Recordati', 'Saipem', 'Ferragamo', 'Snam', 'STMicroelectronics', 'Telecom', 'Tenaris',
                     'Terna', 'UBI', 'UniCredit', 'Unipol', 'UnipolSai', 'Yoox']

for company in list_of_companies:
    print 'Evaluating company #', list_of_companies.index(company), ' out of 41'
    # todo: remove
    company = 'A2A'
    post_fields = {'tiponotizia': '',
                   'any': company,
                   'sezione': '63a85942-dedb-4b31-a3bf-a06f721c67e6',
                   'periodo': '',
                   'genere': '',
                   'sort': 'data:desc',
                   'start': '',
                   'rows': '12'}

    url = 'https://www.ansa.it/ricerca/ansait/search.shtml'
    r = requests.post(url, post_fields)
    page = r.text
    numResultsIndex = page.find('num-result')+12
    # Handling 2 ciphers nu
    try:
        numResults = int(page[numResultsIndex:numResultsIndex+3])
    except:
        print page[numResultsIndex-10:numResultsIndex+10]
    count = 0
    conta = 0
    numRequests = 12;

    while numRequests <= numResults:
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
            link = 'https://www.ansa.it' + newsBlock[linkIndexStart:linkIndexEnd]
            titleIndexEnd = newsBlock.find('</a>', linkIndexEnd)
            title = newsBlock[linkIndexEnd+2:titleIndexEnd]

            # Sottotitolo / abstract dell'articolo
            absIndexStart = newsBlock.find('<p>', titleIndexEnd)
            absIndexEnd = newsBlock.find('</p>')
            abstract = newsBlock[absIndexStart:absIndexEnd]
            # todo: forse replace non e esattamente il metodo migliore da usare
            abstract = abstract.replace('em', '')
            abstract = abstract.replace('<>', '')
            abstract = abstract.replace('</>', '')
            count = count + 1
            # Occasionalmente il subtitle e formattato male
            # todo: rafforzare le condizioni di esistenza - c'è infatti una news senza titolo ma con body (a2a 4)
            body = 'Articolo non disponibile'
            if len(title) > 0 and link.find('professional') < 0:

                articlePageUrl = opener.open(link)
                articlePage = articlePageUrl.read()

                subtitleIndexStart = articlePage.find('news-stit')
                subtitleIndexEnd = articlePage.find('</h2>', subtitleIndexStart)
                subtitle = articlePage[subtitleIndexStart:subtitleIndexEnd]

                bodyStartIndex = articlePage.find('news-txt')
                bodyStartIndex = articlePage.find('<p>', bodyStartIndex)+3
                bodyEndIndex = articlePage.find('</p>', bodyStartIndex)
                body = articlePage[bodyStartIndex:bodyEndIndex].decode("utf-8")
                body = body.replace("\n", " ")
                body = body.replace("  ", " ")
                body = body.replace("   ", " ")
                body = body.replace("\t", " ")
                body = body.replace("<br>", " ")
                body = body.replace("</br>", ' ')
                body = body.replace('<br/>', ' ')
                body = body.replace("&nbsp;", "")

            page = page[newsIndexStart+absIndexEnd:len(page)]
            # print
            print company, conta, '/', numResults, ':', title, date, category, link, abstract
            print 'Articolo: ', body
            conta = conta + 1
        inc = 12
        if(numRequests+12) > numResults:
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

        url = 'https://www.ansa.it/ricerca/ansait/search.shtml'
        r = requests.post(url, post_fields)
        page = r.text
        count = 0
