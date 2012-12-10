def dict_builder(dict):
	text = "  <li>%s: %s</li>\n" % ('Final rating', dict['Final rating'])
	for k,v in dict.iteritems():
		if k == 'Final rating':
			pass
		else:
			text = text + "  <li>%s: %s</li>\n" % (k,v)
	return text

def list_builder(list):
	text = ""
	for k,v in list[-1].iteritems():
		if v != 0:
			text = text + "  <li>%s: %s</li>\n" % (k,v)
	home_team = list[2]
	score = list[3]
	away_team = list[4]+"<br/>"
	return text, home_team, score, away_team

def template_builder(stats_dict, match_list, unplayed_list, name):
	text_0 = dict_builder(stats_dict)
	text_1, home_team, score, away_team = list_builder(match_list)
	if unplayed_list:
		next_game_home, next_game_away = unplayed_list[2], " --- " + unplayed_list[4]
	else:
		next_game_home, next_game_away = "Season's over!", ""
	toSave = """<!DOCTYPE html>
<html>
<head>
<title>%s stats</title>
</head>
<body>
<h1>STATS %s</h1>
<h3>Permanent stats</h3>
%s
<hr>

<h3>Last Match</h3>
%s %s %s
%s
<h3>Next Match</h3>
%s %s
</body>
</html>
	""" % (name, name, text_0, home_team, score, away_team, text_1, next_game_home, next_game_away)
	file = open('%s.html' % name, 'w')
	file.write(toSave)
	file.close()