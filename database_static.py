import lxml.etree
from lxml.cssselect import CSSSelector

parser = lxml.etree.HTMLParser(encoding='utf-8')
# would it not be possible to rewrite this without CSSSelectors?
statname_marker = CSSSelector('div.statLabelWrap')
statnumber_marker = CSSSelector('span')

url_by_player = {
    #'C. Benteke': 'http://www.goal.com/en-gb/people/congo-kinshasa/59775/c-benteke',
    'Moussa Dembele': 'http://www.goal.com/en-gb/people/belgium/13937/moussa-dembele',
    'Marouane Fellaini': 'http://www.goal.com/en-gb/people/belgium/16148/marouane-fellaini',
    #'Eden Hazard': 'http://www.goal.com/en-gb/people/belgium/23040/eden-hazard',
    'Vincent Kompany': 'http://www.goal.com/en-gb/people/belgium/5227/vincent-kompany',
    'Romelu Lukaku': 'http://www.goal.com/en-gb/people/belgium/36519/romelu-lukaku',
    'Simon Mignolet': 'http://www.goal.com/en-gb/people/belgium/35925/simon-mignolet',
    #'Kevin Mirallas': 'http://www.goal.com/en-gb/people/belgium/9536/kevin-mirallas',
    'Thomas Vermaelen': 'http://www.goal.com/en-gb/people/belgium/7710/thomas-vermaelen',
    'Jan Vertonghen': 'http://www.goal.com/en-gb/people/belgium/16549/jan-vertonghen',
    #'Kevin De Bruyne': 'http://www.goal.com/en-gb/people/belgium/33543/kevin-de-bruyne',
    #'Igor De Camargo': 'http://www.goal.com/en-gb/people/belgium/18663/i-de-camargo',
    #'Timmy Simmons': 'http://www.goal.com/en-gb/people/belgium/5248/timmy-simons',
    #'Daniel Van Buyten': 'http://www.goal.com/en-gb/people/belgium/1917/daniel-van-buyten',
    #'Thibaut Courtois': 'http://www.goal.com/en-gb/people/belgium/33521/thibaut-courtois',
    #'Jean-Francois Gillet': 'http://www.goal.com/en-gb/people/belgium/11565/jean-fran%C3%A7ois-gillet',
    #'Gaby Mudingayi': 'http://www.goal.com/en-gb/people/belgium/8098/gaby-mudingayi',
    #'Radja Nainggolan': 'http://www.goal.com/en-gb/people/belgium/12938/radja-nainggolan',
    #'Toby Alderweireld': 'http://www.goal.com/nl/people/netherlands/25746/toby-alderweireld',
}

def static_data(name):
    tree = lxml.etree.parse(url_by_player[name], parser)
    if statname_marker(tree):
        statnames = statname_marker(tree)
        statnumbers = [element for element in statnumber_marker(tree) if element.text is not None and '.' in element.text and 5>len(element.text)>2]
        temp_names = []
        temp_numbers = []
        for i in statnumbers:
            temp_numbers.append(i.text)
        for j in statnames:
            temp_names.append(j.text)

        # I don't understand what this is all about, but this is better
        if len(temp_numbers) == 11:
            stats = {'name': name, 'Final rating': 'N/A'}
            for i in range(temp_numbers):
                stats[temp_names[i]] = temp_numbers[i]
        elif len(temp_numbers) == 12:
            stats = {'name': name, 'Final rating': temp_numbers[0]}
            for i in range(len(temp_numbers)-1):
                stats[temp_names[i]] = temp_numbers[i+1]
    else:
        stats = None
    return stats
