#We import the module urlopen
from urllib2 import build_opener


opener = build_opener()
opener.addheaders = [('User-Agent', 'Mozilla/5.0')]
list_of_companies = ['A2A', 'Atlantia','Azimut', 'Banca+Generali', 'Banco+BPM', 'BPER', 'Brembo', 'Buzzi+Unicem'
                     'Campari', 'CNH', 'Enel', 'Eni', 'Exor', 'Ferrari', 'FCA', 'Fineco', 'Generali', 'Intesa+Sanpaolo',
                     'Italgas', 'Leonardo', 'Luxottica', 'Mediaset', 'Mediobanca', 'Moncler', 'Pirelli', 'Poste+italiane',
                     'Prysmian', 'Recordati', 'Saipem', 'Ferragamo', 'Snam', 'STMicroelectronics', 'Telecom', 'Tenaris',
                     'Terna', 'UBI', 'UniCredit', 'Unipol', 'UnipolSai', 'Yoox']

for company in list_of_companies:
    nameCompany = company
    pageIndex = 1

    html = opener.open("http://www.finanza.com/cerca.asp?Text=" + str(nameCompany) + "&pagina=" + str(pageIndex))
    txt = html.read()
    #Here i calculate the maximum page per company
    indexRicercaNotizie = txt.find("Ricerca notizie: ")
    maximumNumberResultsBlock = txt[indexRicercaNotizie: txt.find('contenenti', indexRicercaNotizie)]

    if 'oltre' in maximumNumberResultsBlock:
        maximumTotalNumberOfResults = 100
    else:
        #assumptions: always 3 cypher numbers todo: release this assumption
        tempIndex = maximumNumberResultsBlock.find(':') + 2
        maximumTotalNumberOfResults = maximumNumberResultsBlock[tempIndex:tempIndex+3]
        maximumTotalNumberOfResults = int(maximumTotalNumberOfResults)/10 + 1

    while pageIndex < maximumTotalNumberOfResults:
        nextBlock = 0
        count = 0
        #NOTA BENE: nella prima magina sono 9
        while count < 10:
            #Block of the article
            indexPositionStringBegin = txt.find('<div class="div_articolo">', nextBlock, len(txt))
            #indexPositionStringEnd = txt.find('<div class="div"></div>\n</div>', 2)
            # mettere 2 come inizio stringa ha poco senso, se proprio bisogna metterla ha senso usare l'index di inizio
            indexPositionStringEnd = txt.find('<div class="div"></div>\n</div>', indexPositionStringBegin)
            block = txt[indexPositionStringBegin:indexPositionStringEnd]

            indexStartArticleLink = block.find('href') + 6
            indexEndArticleLink = block.find('">', 76, len(block))
            if (indexEndArticleLink - indexStartArticleLink) > 5:
                link = 'http://www.finanza.com' + block[indexStartArticleLink:indexEndArticleLink]
            else:
                link = ''

            #Article title
            indexStartTitle = indexEndArticleLink + 2
            indexEndTitle = block.find('</a>', indexStartTitle, len(block))
            title = block[indexStartTitle:indexEndTitle]
            #Potrei filtrare le informazioni - solo Italia...

            #Date (TS)
            #Data (TS)
            block = block[indexStartTitle:len(block)]
            indexStartDate = block.find('data">') + 6
            #il -5 serve per eliminare l'orario dalla data
            indexEndDate = block.find('</span>', indexStartDate) - 5
            indexEndDate = block.find('</span>', indexStartDate)
            date = block[indexStartDate:indexEndDate]
            #I format date better
            date = date.replace("&igrave;", "i")

            #Sottotitolo (ST)
            block = block[indexStartTitle:len(block)]
            indexStartSubTitle = block.find('<p>') + 3
            indexEndSubtitle = block.find('</p>', indexStartSubTitle)
            subtitle = block[indexStartSubTitle:indexEndSubtitle]

            # Ora mi sposto e vado sulla pagina del link, per farlo la devo prima aprire e leggere.
            #Posso farlo pero solo se esiste l'articolo (siccome ci sono 7 / 8 / 10 articoli a pagina mi conviene fare cosi
            nomeAutore = ''
            if len(title) > 1:
                articlePageUrl = opener.open(link)
                articlePage = articlePageUrl.read()
                #Autore
                indexStartDivAutore = articlePage.find('div_autore')
                indexStartAutore = articlePage.find('<h3>', indexStartDivAutore) + 4
                indexEndAutore = articlePage.find('</h3>', indexStartAutore)
                nomeAutore = articlePage[indexStartAutore:indexEndAutore]

                #corpoNotizia todo: clear body
                indexStartCorpoNotizia = articlePage.find('corponotizia') + 19
                indexEndCorpoNotizia = articlePage.find('\n<div class="div_tags', indexStartCorpoNotizia)
<<<<<<< Updated upstream
                bodyArticle = articlePage[indexStartCorpoNotizia:indexEndCorpoNotizia].decode("utf-8")
=======
                bodyArticle = articlePage[indexStartCorpoNotizia:indexEndCorpoNotizia]
                #ora puliamo il corpo della notizia da tutte le pubblicita'
>>>>>>> Stashed changes

            print nameCompany, ' ', count, ':', title, date, nomeAutore, link
            # print subtitle
            # print bodyArticle
            count = count + 1
            txt = txt[indexPositionStringEnd:len(txt)]
        print 'Page evaluated', pageIndex, ' out of ', maximumTotalNumberOfResults, 'for company #', \
            list_of_companies.index(nameCompany), ' out of 41'
        pageIndex = pageIndex + 1
        html = opener.open("http://www.finanza.com/cerca.asp?Text=" + str(nameCompany) + "&pagina=" + str(pageIndex))
        txt = html.read()
