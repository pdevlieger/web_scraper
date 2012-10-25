# Import the modules we need to parse the data.
import urllib2
import lxml.etree

team_by_player = {	'C. Benteke': 'Aston Villa',
					'Moussa Dembele': 'Tottenham',
					'Marouane Fellaini': 'Everton',
					'Eden Hazard': 'Chelsea FC',
					'Vincent Kompany': 'Manchester City',
					'Romelu Lukaku': 'West Bromwich Albion',
					'Simon Mignolet': 'Sunderland',
					'Kevin Mirallas': 'Everton',
					'Thomas Vermaelen': 'Arsenal FC',
					'Jan Vertonghen': 'Tottenham',
					'Kevin De Bruyne': 'Werder Bremen',
					'Igor De Camargo': 'Borussia Moenchengladbach',
					'Timmy Simmons': 'Nuernberg',
					'Daniel Van Buyten': 'Bayern Muenchen',
					'Thibaut Courtois': 'Atletico de Madrid',
					'Jean-Francois Gillet': 'Torino',
					'Gaby Mudingayi': 'Inter Milan',
					'Radja Nainggolan': 'Cagliari',
					'Toby Alderweireld': 'Ajax'
				 }
				 		 
url_by_team = {'Ajax': 'http://www.goal.com/en-au/teams/netherlands/274/ajax/calendar',
				 'Arsenal FC': 'http://www.goal.com/en-gb/teams/england/94/arsenal/calendar',
				 'Aston Villa': 'http://www.goal.com/en-gb/teams/england/95/aston-villa/calendar',
				 'Atletico de Madrid': 'http://www.goal.com/en-gb/teams/spain/129/atl%C3%A9tico-de-madrid',
				 'Bayern Muenchen': 'http://www.goal.com/en-gb/teams/germany/148/fc-bayern-m%C3%BCnchen/calendar',
				 'Borussia Moenchengladbach': 'http://www.goal.com/en-gb/teams/germany/150/b-m%C3%B6nchengladbach/calendar',
				 'Cagliari': 'http://www.goal.com/en-gb/teams/italy/141/cagliari/calendar',
				 'Chelsea FC': 'http://www.goal.com/en-gb/teams/england/96/chelsea/calendar',
				 'Everton': 'http://www.goal.com/en-gb/teams/england/110/everton/calendar',
				 'FC Nuernberg': 'http://www.goal.com/en-gb/teams/germany/154/1-fc-n%C3%BCrnberg/calendar',
				 'Inter Milan': 'http://www.goal.com/en-gb/teams/italy/2/inter/calendar',
				 'Manchester City': 'http://www.goal.com/en-gb/teams/england/109/man-city/calendar',
				 'Sunderland': 'http://www.goal.com/en-gb/teams/england/537/sunderland/calendar',
				 'Torino': 'http://www.goal.com/en-gb/teams/italy/170/torino/calendar',
				 'Tottenham': 'http://www.goal.com/en-gb/teams/england/105/tottenham/calendar',
				 'Werder Bremen': 'http://www.goal.com/en-gb/teams/germany/147/werder-bremen/calendar',
				 'West Bromwich Albion': 'http://www.goal.com/en-gb/teams/england/112/west-bromwich/calendar',
				}

stat_dict = {'goal': 'g1.gif', 'own goal': 'og.gif', 'penalty scored': 'p.gif', 
			'penalty missed': 'pw.gif', 'yellow card': 'y1.gif', 'assist': 'assists.gif',
			'penalty save': 'penalty_saves.gif', 'penalty_shootout_goal':'penalty_shootout_goals.gif',
			'penalty shootout miss': 'penalty_shootout_misses.gif', 'second yellow card/red card': 'yr.gif', 
			'red card': 'r1.gif', 'injury': 'ij.gif'
			}

parser = lxml.etree.HTMLParser(encoding='utf-8')

def check_whether_game_url(tree_node):
	return 'en-gb/match' in tree_node.attrib['href'] and tree_node.getparent().attrib and 'match-entry' in tree_node.getparent().attrib['class']

def add_missing_parts_url(url):
	return 'http://www.goal.com' + url.replace('index', 'report')

def get_calendar_for_player(player):
	
	player_team = team_by_player[player]
	url = url_by_team[player_team]
	tree = lxml.etree.parse(url, parser)
	
	game_competition = [tag.text.strip().replace('\n', '') for tag in tree.xpath('//div[@class="div-competition"]')]
	game_completed = [tag.text for tag in tree.xpath('//div[@class="match-status"]')]
	game_result = [tag.text for tag in tree.xpath('//div[@class="match-result"]')]
	home_team = [tag.text for tag in tree.xpath('//div[@class="match-team-name home-team-name"]')]
	away_team = [tag.text for tag in tree.xpath('//div[@class="match-team-name away-team-name"]')]
	game_url = [tag.attrib['href'] for tag in tree.xpath('//a[@href]') if check_whether_game_url(tag)]
	game_url = [add_missing_parts_url(tag) for tag in game_url]

	game_result = game_result + ['n/a']*(len(game_competition) - len(game_result))
	game_url = game_url + ['n/a']*(len(game_competition) - len(game_url))

	zip(game_competition, game_completed, home_team, game_result, away_team, game_url)

def set_player_tree_node(url, player): # returns a 1-element or empty list.

	game_tree = lxml.etree.parse(url, parser)
	return [element for element in game_tree.xpath('//a[@class="player_lineup"]') if element.text == player]

def image_tag_in_subtree(node):
	children = node.getchildren()
	return [element for element in children if element.tag == 'img']
	# look up in lxml again, maybe easier way.
	
def get_player_match_stats(player_name_node):
	
	image_stats_bucket = player_name_node.getparent()
	player_root = player_name_node.getparent().getparent()
	image_vote = image_tag_in_subtree(player_root)
	image_stats = image_tag_in_subtree(player_name_node)
	images = [element.attrib['src'] for element in image_stats]
	
	mom = 'manOfTheMatch' in player_root.attrib['class']
	fom = 'flopOfTheMatch' in player_root.attrib['class']
	if image_vote:
		voted_mom = 'd4.gif' in image_vote[0].attrib['src']
		voted_fom = 'd5.gif' in image_vote[0].attrib['src']
	else:
		voted_mom = False
		voted_fom = False
	
	stats_match = {}
	for key, image_name in stat_dict.iteritems():
		stats_match[key] = get_stat_from_image(image_name, images)
	
	return stats_match
	
def get_stat_from_image(image_name, images):
#	return len([element for element in images if element.endswith(image_name)])
	return len(filter(lambda node: node.endswith(image_name), images))
	
# work this out with a user interface.
player = 'Eden Hazard'
stats = get_calendar_for_player(player)
for matchday in stats:
	url = matchday[5]
	if url != 'n/a':
		player_node = set_player_tree_node(url, player)
		if player_node:
			matchday.append(get_player_match_stats(player_node[0]))
print stats