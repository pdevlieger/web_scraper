## ------------------------------------------------------------------------------------ ##
## -- This is proverbial scrap paper to set up a database from match-to-match stats. -- ##
## ------------------------------------------------------------------------------------ ##

# Import the stuff we need to parse the data.
import numpy
import urllib2
import lxml.etree
from lxml.cssselect import CSSSelector
import codecs

# Set up the dicts we need linking players to their urls.
playerdict = dict({	'C. Benteke': 'Aston Villa',
					'Moussa Dembele': 'Tottenham Hotspur',
					'Marouane Fellaini': 'Everton',
					'Eden Hazard': 'Chelsea',
					'Vincent Kompany': 'Manchester City',
					'Romelu Lukaku': 'West Bromwich Albion',
					'Simon Mignolet': 'Sunderland',
					'Kevin Mirallas': 'Everton',
					'Thomas Vermaelen': 'Arsenal',
					'Jan Vertonghen': 'Tottenham Hotspur',
					#'Kevin De Bruyne': 'Werder Bremen',
					#'Igor De Camargo': 'Borussia Moenchengladbach',
					#'Timmy Simmons': 'Nuernberg',
					#'Daniel Van Buyten': 'Bayern Muenchen',
					#'Thibaut Courtois': 'Atletico de Madrid',
					#'Jean-Francois Gillet': 'Torino',
					#'Gaby Mudingayi': 'Inter Milan',
					#'Radja Nainggolan': 'Cagliari',
					'Toby Alderweireld': 'Ajax'
				 })
				 
teamdict = dict({'Ajax': 'http://www.goal.com/en-au/teams/netherlands/274/ajax/calendar',
				 'Arsenal': 'http://www.goal.com/en-gb/teams/england/94/arsenal/calendar',
				 'Aston Villa': 'http://www.goal.com/en-gb/teams/england/95/aston-villa/calendar',
				 #'Atletico de Madrid': 'http://www.goal.com/en-gb/teams/spain/129/atl%C3%A9tico-de-madrid',
				 #'Bayern Muenchen': 'http://www.goal.com/en-gb/teams/germany/148/fc-bayern-m%C3%BCnchen/calendar',
				 #'Borussia Moenchengladbach': 'http://www.goal.com/en-gb/teams/germany/150/b-m%C3%B6nchengladbach/calendar',
				 #'Cagliari': 'http://www.goal.com/en-gb/teams/italy/141/cagliari/calendar',
				 'Chelsea': 'http://www.goal.com/en-gb/teams/england/96/chelsea/calendar',
				 'Everton': 'http://www.goal.com/en-gb/teams/england/110/everton/calendar',
				 #'FC Nuernberg': 'http://www.goal.com/en-gb/teams/germany/154/1-fc-n%C3%BCrnberg/calendar',
				 #'Inter Milan': 'http://www.goal.com/en-gb/teams/italy/2/inter/calendar',
				 'Manchester City': 'http://www.goal.com/en-gb/teams/england/109/man-city/calendar',
				 'Sunderland': 'http://www.goal.com/en-gb/teams/england/537/sunderland/calendar',
				 #'Torino': 'http://www.goal.com/en-gb/teams/italy/170/torino/calendar',
				 'Tottenham Hotspur': 'http://www.goal.com/en-gb/teams/england/105/tottenham/calendar',
				 #'Werder Bremen': 'http://www.goal.com/en-gb/teams/germany/147/werder-bremen/calendar',
				 'West Bromwich Albion': 'http://www.goal.com/en-gb/teams/england/112/west-bromwich/calendar',
				})

statdict = dict({'g1.gif': 'goal', 'og.gif': 'own goal', 'p.gif': 'penalty scored', 
				 'pw.gif': 'penalty missed', 'y1.gif': 'yellow card', 'assists.gif': 'assist',
				 'penalty saves.gif': 'penalty save', 'penalty shootout goals.gif': 'penalty shootout goal',
				 'penalty shootout misses.gif': 'penalty shootout miss', 'yr.gif': 'second yellow card/red card', 
				 'r1.gif': 'red card', 'ij.gif': 'injury'
				})

# Define the parser method.
parser = lxml.etree.HTMLParser(encoding='utf-8')

# We begin with a function that reads in the club calendar.
def calendar(name):
	tree = lxml.etree.parse(teamdict[playerdict[name]], parser)
	
	# We look up type of match (friendly, premier league, european, etc.), whether it has
	# been played, and the home and away team.
	match_type = CSSSelector('div.match-competition')
	match_played = CSSSelector('div.match-status')
	match_teams = CSSSelector('div.match-team-name')
	
	# we turn this into lists and add the hyperlink for further information.
	
	# type of match (what competition?)
	temp_type = []
	for i in match_type(tree):
		temp_type.append(i.text[21:])
	fixtures = numpy.arange(len(temp_type))
	
	# match completed or not?
	temp_played = []
	for i in match_played(tree):
		temp_played.append(i.text)
	
	# teams playing in all the matches, setting up home and away teams, contenders and 
	# away boolean variable.
	temp_teams = []
	for i in match_teams(tree):
		temp_teams.append(i.text)
	home_team = map(lambda x: temp_teams[x], filter(lambda x: x%2 == 0, range(len(temp_teams))))
	away_team = map(lambda x: temp_teams[x], filter(lambda x: x%2 == 1, range(len(temp_teams))))
	if playerdict[name] != 'Tottenham Hotspur':
		away_play = map(lambda x: x == playerdict[name], away_team)
		contender = []
		for i in fixtures:
			if home_team[i] == playerdict[name]:
				contender.append(away_team[i])
			elif home_team[i] != playerdict[name]:
				contender.append(home_team[i])
			else:
				pass
	else:
		away_play = map(lambda x: x == 'Tottenham', away_team)
		contender = []
		for i in fixtures:
			if home_team[i] == 'Tottenham':
				contender.append(away_team[i])
			elif home_team[i] != 'Tottenham':
				contender.append(home_team[i])
			else:
				pass		
	
	# urls that have the specific match information and statistics
	# we need to 
	urls = tree.xpath('//a/@href')
	links_temp = []
	for i in urls:
		if i.startswith('/en-gb/match') == True:
			links_temp.append('http://www.goal.com' + i)
		else:
			pass
	urls  = links_temp[8:]
	urls_none = ['n/a'] * (len(fixtures)-len(links_temp[8:]))
	urls.extend(urls_none)
	
	# Set up the outcome: a list containing the following information.
	# [index, competition, played, away_play, contender, url, None]
	calendar_stats = []
	for i in fixtures:
		if temp_type[i].startswith('Premier League'):
			pass
		else:
			calendar_stats_temp = [fixtures[i], temp_type[i], temp_played[i], away_play[i], urls[i], contender[i], None]
			calendar_stats.extend([calendar_stats_temp])
#		else:
#			pass
	return calendar_stats

# A function that sets the marker tab for the player.
def markit(url, boolean, name):
	# Parse the site of match url.
	tree = lxml.etree.parse(url, parser)	
	
	# Find the marker tab.
	mom = False
	fom = False
	voted_mom = False
	voted_fom = False
	if boolean == False:
		path_mom = '//div[@class="player_info_tab_lineup manOfTheMatch"]/div[@class="player_name_lineup"]/a[@href]'
		path_fom = '//div[@class="player_info_tab_lineup flopOfTheMatch"]/div[@class="player_name_lineup"]/a[@href]'
		marker_temp = tree.xpath('//div[@class="player_name_lineup"]')
		marker = filter(lambda x: x.getchildren()[0].text == name, marker_temp)
		if marker != []:
			marker = marker[0]
		elif marker == []:
			if tree.xpath(path_mom) != [] and tree.xpath(path_mom)[0].text == name:
				mom = True
				marker_temp = tree.xpath('//div[@class="player_info_tab_lineup manOfTheMatch"]/div[@class="player_name_lineup"]')
				marker = marker_temp[0]
			elif tree.xpath(path_fom) != [] and tree.xpath(path_fom)[0].text == name:
				fom = True
				marker_temp = tree.xpath('//div[@class="player_info_tab_lineup flopOfTheMatch"]/div[@class="player_name_lineup"]')
				marker = marker_temp[0]
			else:
				pass
	elif boolean == True:
		path_mom = '//div[@class="player_info_tab_lineup manOfTheMatch"]/div[@class="player_name_lineup right-col"]/a[@href]'
		path_fom = '//div[@class="player_info_tab_lineup flopOfTheMatch"]/div[@class="player_name_lineup right-col"]/a[@href]'
		marker_temp = tree.xpath('//div[@class="player_name_lineup right-col"]')
		marker = filter(lambda x: x.getchildren()[0].text == name, marker_temp)
		if marker != []:
			marker = marker[0]
		elif marker == []:
			if tree.xpath(path_mom) != [] and tree.xpath(path_mom)[0].text == name:
				mom = True
				marker_temp = tree.xpath('//div[@class="player_info_tab_lineup manOfTheMatch"]/div[@class="player_name_lineup right-col"]')
				marker = marker_temp[0]
			elif tree.xpath(path_fom) != [] and tree.xpath(path_fom)[0].text == name:
				fom = True
				marker_temp = tree.xpath('//div[@class="player_info_tab_lineup flopOfTheMatch"]/div[@class="player_name_lineup right-col"]')
				marker = marker_temp[0]
			else:
				pass
	else:
		pass
	
	return marker

# A function that retrieves the stats for every match.
def matchstats(mark):
#	stats_temp = []
	# get the score for the match.
	parent = mark.getparent()
	score = filter(lambda x: x.attrib['class'][:13] == 'player_rating', filter(lambda x: x.tag == 'div', parent))
	score = score[0].text
	# obtain votes for man and flop of the match and set to boolean.
	voted_mom = map(lambda x: x.attrib['src'].endswith('d4.gif'), filter(lambda x: x.tag == 'img', parent))
	if voted_mom == []:
		voted_mom = [False]
	voted_mom = voted_mom[0]
	voted_fom = map(lambda x: x.attrib['src'].endswith('d5.gif'), filter(lambda x: x.tag == 'img', parent))
	if voted_fom == []:
		voted_fom = [False]
	voted_fom = voted_fom[0]
	# obtain the "gif-figure-stats".
	children = mark.getchildren()
	images = map(lambda x: x.attrib['src'], filter(lambda x: x.tag == 'img', children))
	if images == []:
		images = ['a']
	goals = len(filter(lambda x: x.endswith('g1.gif'), images))
	assists = len(filter(lambda x: x.endswith('assists.gif'), images))
	own_goals = len(filter(lambda x: x.endswith('og.gif'), images))
	penalty_goals = len(filter(lambda x: x.endswith('p.gif'), images))
	penalty_missed = len(filter(lambda x: x.endswith('pw.gif'), images))
	penalty_saves = len(filter(lambda x: x.endswith('penalty_saves.gif'), images))
	ps_goal = len(filter(lambda x: x.endswith('penalty_shootout_goals.gif'), images))
	ps_miss = len(filter(lambda x: x.endswith('penalty_shootout_misses.gif'), images))
	yellow_card = len(filter(lambda x: x.endswith('y1.gif'), images))
	yellowred_card = len(filter(lambda x: x.endswith('yr.gif'), images))
	red_card = len(filter(lambda x: x.endswith('r1.gif'), images))
	injury = len(filter(lambda x: x.endswith('ij.gif'), images))
	stats_match = dict({
						#'Man of the match': mom,
						#'Flop of the match': fom,
						'Voted man of the match': voted_mom,
						'Voted flop of the match': voted_fom,
						'Score': score,
						'Goals': goals,
						'Assists': assists,
						'Own goals': own_goals,
						'Penalty goals': penalty_goals,
						'Penalty missed': penalty_missed,
						'Penalty saves': penalty_saves,
						'Penalty shootout goal': ps_goal,
						'Penalty shootout miss': ps_miss,
						'Yellow card': yellow_card,
						'Second yellow card/red card': yellowred_card,
						'Red card': red_card,
						'Injury': injury
						})
	return stats_match
	
#name = 'Vincent Kompany'
calendar = calendar('Eden Hazard')
#print calendar
for i in calendar:
	if i[4] != 'n/a':
		if markit(i[4], i[3], 'Eden Hazard') != []:
			i[6] = matchstats(markit(i[4], i[3], 'Eden Hazard'))
		else:
			pass
	print i
