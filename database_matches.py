import lxml.etree

team_by_player = {
    'C. Benteke': 'Aston Villa','Moussa Dembele': 'Tottenham',
    'Marouane Fellaini': 'Everton','Eden Hazard': 'Chelsea FC',
    'Vincent Kompany': 'Manchester City','Romelu Lukaku': 'West Bromwich Albion',
    'Simon Mignolet': 'Sunderland','Kevin Mirallas': 'Everton',
    'Thomas Vermaelen': 'Arsenal FC','Jan Vertonghen': 'Tottenham',
    'Kevin De Bruyne': 'Werder Bremen','Igor De Camargo': 'Borussia Moenchengladbach',
    'Timmy Simmons': 'Nuernberg','Daniel Van Buyten': 'Bayern Muenchen',
    'Thibaut Courtois': 'Atletico de Madrid','Jean-Francois Gillet': 'Torino',
    'Gaby Mudingayi': 'Inter Milan','Radja Nainggolan': 'Cagliari',
    }

url_by_team = {
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
    'West Bromwich Albion': 'http://www.goal.com/en-gb/teams/england/112/west-bromwich/calendar'
}

stat_dict = {
    'goal': 'g1.gif',
    'own goal': 'og.gif',
    'penalty scored': 'p.gif',
    'penalty missed': 'pw.gif',
    'yellow card': 'y1.gif',
    'assist': 'assists.gif',
    'penalty save': 'penalty_saves.gif',
    'penalty_shootout_goal':'penalty_shootout_goals.gif',
    'penalty shootout miss': 'penalty_shootout_misses.gif',
    'second yellow card/red card': 'yr.gif',
    'red card': 'r1.gif',
    'injury': 'ij.gif'
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

    game_competition = [('competition', tag.text.strip().replace('\n', '')) for tag in tree.xpath('//div[@class="match-competition"]')]
    game_completed = [('completed', tag.text) for tag in tree.xpath('//div[@class="match-status"]')]
    game_result = [('score', tag.text) for tag in tree.xpath('//div[@class="match-result Completed"]')]
    home_team = [('home team', tag.text) for tag in tree.xpath('//div[@class="match-team-name home-team-name"]')]
    away_team = [('away team', tag.text) for tag in tree.xpath('//div[@class="match-team-name away-team-name"]')]
    game_url = [tag.attrib['href'] for tag in tree.xpath('//a[@href]') if check_whether_game_url(tag)]
    game_url = [('url', add_missing_parts_url(tag)) for tag in game_url]
    game_result = game_result + [('score', 'n/a')]*(len(game_competition) - len(game_result))
    game_url = game_url + [('url', 'n/a')]*(len(game_competition) - len(game_url))
    name = [('name', player),]*(len(game_competition))
    team = [('team', player_team),]*(len(game_competition))
    output = []
    for line in zip(name, team, game_competition, game_completed, home_team, game_result, away_team, game_url):
        element = dict(line)
        output.append(element)

    return output

def set_player_tree_node(tree, player):
    try:
        return (element for element in tree.xpath('//a[@class="player_lineup"]') if player in element.text).next()
    except StopIteration:
        return None

# need to parse the actual score as well.
def get_player_match_stats(url, player):
    if url == 'n/a':
        stats_match = {key: None for key in stat_dict}
        stats_match['Played'] = None
        stats_match['Man of the match'] = None
        stats_match['Flop of the match'] = None
        stats_match['Voted man of the match'] = None
        stats_match['Voted flop of the match'] = None
    else:
        game_tree = lxml.etree.parse(url, parser)
        player_name_node = set_player_tree_node(game_tree, player)
        if player_name_node is None:
            stats_match = {key: None for key in stat_dict}
            stats_match['Played'] = False
            stats_match['Man of the match'] = None
            stats_match['Flop of the match'] = None
            stats_match['Voted man of the match'] = None
            stats_match['Voted flop of the match'] = None
        else:
            stat_images = player_name_node.getparent().findall('img')
            vote_images = player_name_node.getparent().getparent().findall('img')
            mom = 'manOfTheMatch' in player_name_node.getparent().getparent().attrib['class']
            fom = 'flopOfTheMatch' in player_name_node.getparent().getparent().attrib['class']
            voted_mom, voted_fom = False, False
            if vote_images:
                voted_mom = get_stat_from_image('d4.gif', vote_images)
                voted_fom = get_stat_from_image('d5.gif', vote_images)
            stats_match = {}
            for key, image_name in stat_dict.iteritems():
                stats_match[key] = get_stat_from_image(image_name, stat_images)
            stats_match['Man of the match'] = mom
            stats_match['Flop of the match'] = fom
            stats_match['Voted man of the match'] = voted_mom
            stats_match['Voted flop of the match'] = voted_fom
    return stats_match

def get_stat_from_image(image_name, images):
    return len([element for element in images if element.attrib['src'].endswith(image_name)])
