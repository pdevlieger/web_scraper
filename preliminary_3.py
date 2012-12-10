# Import the stuff we need to parse the data.
import urllib2
import lxml.etree
from lxml.cssselect import CSSSelector

playerdict = dict({	'C. Benteke': 'http://www.goal.com/en-gb/people/congo-kinshasa/59775/c-benteke',
					'Moussa Dembele': 'http://www.goal.com/en-gb/people/belgium/13937/moussa-dembele',
					'Marouane Fellaini': 'http://www.goal.com/en-gb/people/belgium/16148/marouane-fellaini',
					'Eden Hazard': 'http://www.goal.com/en-gb/people/belgium/23040/eden-hazard',
					'Vincent Kompany': 'http://www.goal.com/en-gb/people/belgium/5227/vincent-kompany',
					'Romelu Lukaku': 'http://www.goal.com/en-gb/people/belgium/36519/romelu-lukaku',
					'Simon Mignolet': 'http://www.goal.com/en-gb/people/belgium/35925/simon-mignolet',
					'Kevin Mirallas': 'http://www.goal.com/en-gb/people/belgium/9536/kevin-mirallas',
					'Thomas Vermaelen': 'http://www.goal.com/en-gb/people/belgium/7710/thomas-vermaelen',
					'Jan Vertonghen': 'http://www.goal.com/en-gb/people/belgium/16549/jan-vertonghen',
					'Kevin De Bruyne': 'http://www.goal.com/en-gb/people/belgium/33543/kevin-de-bruyne',
					'Igor De Camargo': 'http://www.goal.com/en-gb/people/belgium/18663/i-de-camargo',
					'Timmy Simmons': 'http://www.goal.com/en-gb/people/belgium/5248/timmy-simons',
					'Daniel Van Buyten': 'http://www.goal.com/en-gb/people/belgium/1917/daniel-van-buyten',
					'Thibaut Courtois': 'http://www.goal.com/en-gb/people/belgium/33521/thibaut-courtois',
					'Jean-Francois Gillet': 'http://www.goal.com/en-gb/people/belgium/11565/jean-fran%C3%A7ois-gillet',
					'Gaby Mudingayi': 'http://www.goal.com/en-gb/people/belgium/8098/gaby-mudingayi',
					'Radja Nainggolan': 'http://www.goal.com/en-gb/people/belgium/12938/radja-nainggolan',
					'Toby Alderweireld': 'http://www.goal.com/nl/people/netherlands/25746/toby-alderweireld'
				 })


parser = lxml.etree.HTMLParser(encoding='utf-8')
marker = CSSSelector('div.statLabelWrap')
sel = CSSSelector('span')

def parse_static_data(x):
	# set up a dictionary that has players for keys and an empty associated list (for now).
	player_static_data = dict.fromkeys(x.keys())
	for name in player_static_data.keys():
		tree = lxml.etree.parse(x[name], parser)
		if marker(tree) != []:
			markerlist = marker(tree)
			spanlist = sel(tree)[8:20]
			temp_data = []
			temp_stats = []
			for i in spanlist:
				temp_data.append(i.text)
			for j in markerlist:
				temp_stats.append(j.text)
			name_stats = {'Final rating': temp_data[0], temp_stats[0]: temp_data[1],
						  temp_stats[1]: temp_data[2], temp_stats[2]: temp_data[3],
						  temp_stats[3]: temp_data[4], temp_stats[4]: temp_data[5],
						  temp_stats[5]: temp_data[6], temp_stats[6]: temp_data[7],
						  temp_stats[7]: temp_data[8], temp_stats[8]: temp_data[9],
						  temp_stats[9]: temp_data[10], temp_stats[10]: temp_data[11]}
			if name == 'Vermaelen':
				name_stats = {'Final rating': 'N/A', temp_stats[0]: temp_data[0],
							  temp_stats[1]: temp_data[1], temp_stats[2]: temp_data[2],
							  temp_stats[3]: temp_data[3], temp_stats[4]: temp_data[4],
							  temp_stats[5]: temp_data[5], temp_stats[6]: temp_data[6],
							  temp_stats[7]: temp_data[7], temp_stats[8]: temp_data[8],
							  temp_stats[9]: temp_data[9], temp_stats[10]: temp_data[10]}
			player_static_data[name] = name_stats
		else:
			pass
	return player_static_data

final_result = parse_static_data(playerdict)
print final_result