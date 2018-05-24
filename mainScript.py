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
    indexTableStart = text.find('<table')
    while indexTableStart >= 0:
        indexTableEnd = text.find('</table>', indexTableStart)
        text = text[:indexTableStart] + text[indexTableEnd + 8:]
        indexTableStart = text.find('<table')
    indexP = text.find('<script')
    while indexP >= 0:
        indexEndP = text.find('</script>', indexP)
        text = text[:indexP] + text[indexEndP + 9:]
        indexP = text.find('<script')
    text = text.replace("</form>", "")
    indexP = text.find('<input')
    while indexP >= 0:
        indexEndP = text.find('>', indexP)
        text = text[:indexP] + text[indexEndP + 1:]
        indexP = text.find('<input')
    text = text.replace("</body>", "")
    text = text.replace("</html>", "")
    indexP = text.find('<td')
    while indexP >= 0:
        indexEndP = text.find('>', indexP)
        text = text[:indexP] + text[indexEndP + 1:]
        indexP = text.find('<td')
        indexP = text.find('<td')
    indexP = text.find('<tr')
    while indexP >= 0:
        indexEndP = text.find('>', indexP)
        text = text[:indexP] + text[indexEndP + 1:]
        indexP = text.find('<tr')
    return text


#We import the module urlopen
from urllib2 import build_opener
import pymysql.cursors

connection = pymysql.connect(host='localhost', port=3306, user='root', password='mamma93', db='mercurio',
                             charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
# cursorObject = connection.cursor()

opener = build_opener()
opener.addheaders = [('User-Agent', 'Mozilla/5.0')]
list_of_companies = ['A2A', 'Atlantia','Azimut', 'Banca+Generali', 'Banco+BPM', 'BPER', 'Brembo', 'Buzzi+Unicem'
                     'Campari', 'CNH', 'Enel', 'Eni', 'Exor', 'Ferrari', 'FCA', 'Fineco', 'Generali', 'Intesa+Sanpaolo',
                     'Italgas', 'Leonardo', 'Luxottica', 'Mediaset', 'Mediobanca', 'Moncler', 'Pirelli',
                     'Poste+italiane','Prysmian', 'Recordati', 'Saipem', 'Ferragamo',
                     'Snam', 'STMicroelectronics', 'Telecom', 'Tenaris',
                     'Terna', 'UBI', 'UniCredit', 'Unipol', 'UnipolSai', 'Yoox']

with open('logFINANZAdotCOM.txt', 'a') as the_file:
    the_file.write('START OF THE FILE. \n Here i put what went wrong in the computation \n')
    '''the_file.write(str(datetime.datetime.time(datetime.datetime.now())))'''


# start cycle
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
        #assumptions: always 3 cypher numbers
        tempIndex = maximumNumberResultsBlock.find(':') + 2
        maximumTotalNumberOfResults = maximumNumberResultsBlock[tempIndex:tempIndex+3]
        maximumTotalNumberOfResults = int(maximumTotalNumberOfResults)/10 + 1
    # maximumTotalNumberOfResults
    while pageIndex < maximumTotalNumberOfResults:
        nextBlock = 0
        count = 0
        # NOTA BENE: nella prima magina sono 9
        while count < 10:
            # Block of the article
            indexPositionStringBegin = txt.find('<div class="div_articolo">', nextBlock, len(txt))
            # indexPositionStringEnd = txt.find('<div class="div"></div>\n</div>', 2)
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
            date = block[indexStartDate:indexEndDate]
            #I format date better
            date = date.replace("&igrave;", "i")
            date = date.lower()
            date = date.replace("lunedi ", "")
            date = date.replace("martedi ", "")
            date = date.replace("mercoledi ", "")
            date = date.replace("giovedi ", "")
            date = date.replace("venerdi ", "")
            date = date.replace("sabato ", "")
            date = date.replace("domenica ", "")
            date = date.replace(" gennaio ", "-01-")
            date = date.replace(" febbraio ", "-02-")
            date = date.replace(" marzo ", "-03-")
            date = date.replace(" aprile ", "-04-")
            date = date.replace(" maggio ", "-05-")
            date = date.replace(" giugno ", "-06-")
            date = date.replace(" luglio ", "-07-")
            date = date.replace(" agosto ", "-08-")
            date = date.replace(" settembre ", "-09-")
            date = date.replace(" ottobre ", "-10-")
            date = date.replace(" novembre ", "-11-")
            date = date.replace(" dicembre ", "-12-")


            #Sottotitolo (ST)
            block = block[indexStartTitle:len(block)]
            indexStartSubTitle = block.find('<p>') + 3
            indexEndSubtitle = block.find('</p>', indexStartSubTitle)
            subtitle = block[indexStartSubTitle:indexEndSubtitle]

            # Ora mi sposto e vado sulla pagina del link, per farlo la devo prima aprire e leggere.
            #Posso farlo pero solo se esiste l'articolo (siccome ci sono 7 / 8 / 10 articoli a pagina mi conviene fare cosi
            nomeAutore = ''
            if len(title) > 1:
                try:
                    articlePageUrl = opener.open(link)
                    articlePage = articlePageUrl.read()
                    #Autore
                    indexStartDivAutore = articlePage.find('div_autore')
                    indexStartAutore = articlePage.find('<h3>', indexStartDivAutore) + 4
                    indexEndAutore = articlePage.find('</h3>', indexStartAutore)
                    nomeAutore = articlePage[indexStartAutore:indexEndAutore]
                    indexStartDivLinkedCompanies = articlePage.find('link_azioni')
                    indexEndDivLinkedCompanies = articlePage.find('</div>', indexStartDivLinkedCompanies)
                    blockLinkedCompanies = articlePage[indexStartDivLinkedCompanies:indexEndDivLinkedCompanies]
                    linkedCompanies = ''
                    if indexStartDivLinkedCompanies >= 0:
                        indexStartDivLinkedCompanies = blockLinkedCompanies.find('<a')
                        while indexStartDivLinkedCompanies >= 0:
                            indexStartLinkedCompanies = blockLinkedCompanies.find('>', indexStartDivLinkedCompanies) + 1
                            indexEndLinkedCompanies = blockLinkedCompanies.find('</a>', indexStartLinkedCompanies)
                            linkedCompanies = linkedCompanies + blockLinkedCompanies[indexStartLinkedCompanies:indexEndLinkedCompanies] + ' '
                            indexStartDivLinkedCompanies = blockLinkedCompanies.find('<a', indexEndLinkedCompanies)
                    else:
                        linkedCompanies = 'None'
                    indexStartCorpoNotizia = articlePage.find('corponotizia') + 19
                    indexEndCorpoNotizia = articlePage.find('\n<div class="div_tags', indexStartCorpoNotizia)
                    bodyArticle = articlePage[indexStartCorpoNotizia:indexEndCorpoNotizia].decode("utf-8")
                    bodyArticle = cleaning(bodyArticle)
                    if len(bodyArticle)<10:
                        bodyArticle = 'None'
                    print nameCompany, linkedCompanies, ' ', count, ':', title, date, nomeAutore, link, bodyArticle
                    try:
                        with connection.cursor() as cursor:
                            query = "INSERT INTO articles_finanza_com (date, newspaper, section, title, body, company, author, tagged_companies) VALUES (%d-%m-%Y, %s, %s, %s, %s, %s, %s, %s)"
                            cursor.execute(query, [date, "finanza.com", "economy", title, bodyArticle, nameCompany, nomeAutore, linkedCompanies])
                            connection.commit()

                    except Exception, e:
                        print("Can't insert " + str(e))
                        with open('logFINANZAdotCOM.txt', 'a') as the_file:
                            the_file.write('\n\n')
                            the_file.write(company)
                            the_file.write(' --- ')
                            the_file.write(str(count))
                            the_file.write(' / ')
                            the_file.write(str(maximumTotalNumberOfResults))
                            the_file.write(' ---- on Date: ')
                            the_file.write(str(date))
                            the_file.write('\nTitle: ')
                            the_file.write(title)
                            the_file.write('\nLink: ')
                            the_file.write(link)
                            the_file.write('\nARTICOLO: ')
                            the_file.write(bodyArticle)
                            the_file.write('\nAUTORE: ')
                            the_file.write(nomeAutore)
                            the_file.write('\n')

                except:
                    print 'Url was not found'
            count = count + 1
            txt = txt[indexPositionStringEnd:len(txt)]
        print 'Page evaluated', pageIndex, ' out of ', maximumTotalNumberOfResults, 'for company #', \
            list_of_companies.index(nameCompany), ' out of 41'
        pageIndex = pageIndex + 1
        html = opener.open("http://www.finanza.com/cerca.asp?Text=" + str(nameCompany) + "&pagina=" + str(pageIndex))
        txt = html.read()
