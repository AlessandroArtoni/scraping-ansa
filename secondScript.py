#todo: aprire articoli e prendere le informazioni ma serve l'autenticazione
#todo: push database

#Second code
import requests

list_of_companies = ['A2A', 'Atlantia','Azimut', 'Banca Generali', 'Banco BPM', 'BPER', 'Brembo', 'Buzzi Unicem'
                     'Campari', 'CNH', 'Enel', 'Eni', 'Exor', 'Ferrari', 'FCA', 'Fineco', 'Generali', 'Intesa Sanpaolo',
                     'Italgas', 'Leonardo', 'Luxottica', 'Mediaset', 'Mediobanca', 'Moncler', 'Pirelli', 'Poste italiane',
                     'Prysmian', 'Recordati', 'Saipem', 'Ferragamo', 'Snam', 'STMicroelectronics', 'Telecom', 'Tenaris',
                     'Terna', 'UBI', 'UniCredit', 'Unipol', 'UnipolSai', 'Yoox']

for company in list_of_companies:
    print 'Evaluating company #', list_of_companies.index(company), ' out of 41'
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
    numResults = int(page[numResultsIndex:numResultsIndex+3])
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

            #Sottotitolo / abstract dell'articolo
            absIndexStart = newsBlock.find('<p>', titleIndexEnd)
            absIndexEnd = newsBlock.find('</p>')
            abstract = newsBlock[subtitleIndexStart:subtitleIndexEnd]
            #todo: forse replace non e esattamente il metodo migliore da usare
            abstract = abstract.replace('em', '')
            abstract = abstract.replace('<>', '')
            abstract = abstract.replace('</>', '')
            count = count + 1
            #Occasionalmente il subtitle e formattato male

            page = page[newsIndexStart+200:len(page)]
            #print
            print company, conta, '/', numResults, ':', title, date, category, link, abstract
            conta = conta + 1
        numRequests = numRequests + 12
        post_fields = {'tiponotizia': '',
                       'any': company,
                       'sezione': '63a85942-dedb-4b31-a3bf-a06f721c67e6',
                       'periodo': '',
                       'genere': '',
                       'sort': 'data:desc',
                       'start': numRequests-12,
                       'rows':  numRequests}

        url = 'https://www.ansa.it/ricerca/ansait/search.shtml'
        r = requests.post(url, post_fields)
        page = r.text
        count = 0
