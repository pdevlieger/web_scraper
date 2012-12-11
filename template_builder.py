# I use the parameter rating here so I can use this for both final rating and match rating
def dict_builder(dict, rating):
	text = "  <li>%s: %s</li>\n" % (rating, dict[rating])
	for k,v in dict.iteritems():
		if k == rating:
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

def index_builder(string):
	index_html = """
<html>
    <head>
        <title>Home page!</title>
    </head>
<body>

<h1>Whose statistics do you want to see? %s</h1>

<a href="http://intense-citadel-9344.herokuapp.com/1">Christian Benteke</a><br/>
<a href="http://intense-citadel-9344.herokuapp.com/Moussa Dembele">Moussa Dembele</a><br/>
<a href="http://intense-citadel-9344.herokuapp.com/Marouane Fellaini">Marouane Fellaini</a><br/>
<a href="http://intense-citadel-9344.herokuapp.com/4">Eden Hazard</a><br/>
<a href="http://intense-citadel-9344.herokuapp.com/Vincent Kompany">Vincent Kompany</a><br/>
<a href="http://intense-citadel-9344.herokuapp.com/Romelu Lukaku">Romelu Lukaku</a><br/>
<a href="http://intense-citadel-9344.herokuapp.com/Simon Mignolet">Simon Mignolet</a><br/>
<a href="http://intense-citadel-9344.herokuapp.com/8">Kevin Mirallas</a><br/>
<a href="http://intense-citadel-9344.herokuapp.com/Thomas Vermaelen">Thomas Vermaelen</a><br/>
<a href="http://intense-citadel-9344.herokuapp.com/Jan Vertonghen">Jan Vertonghen</a><br/>
<a href="http://intense-citadel-9344.herokuapp.com/11">Kevin De Bruyne</a><br/>
<a href="http://intense-citadel-9344.herokuapp.com/12">Igor De Camargo</a><br/>
<a href="http://intense-citadel-9344.herokuapp.com/13">Timmy Simmons</a><br/>
<a href="http://intense-citadel-9344.herokuapp.com/14">Daniel Van Buyten</a><br/>
<a href="http://intense-citadel-9344.herokuapp.com/15">Thibaut Courtois</a><br/>
<a href="http://intense-citadel-9344.herokuapp.com/16">Jean-Francois Gillet</a><br/>
<a href="http://intense-citadel-9344.herokuapp.com/17">Gaby Mudingayi</a><br/>
<a href="http://intense-citadel-9344.herokuapp.com/18">Radja Nainggolan</a><br/>
<a href="http://intense-citadel-9344.herokuapp.com/19">Toby Alderweireld</a><br/>

</body>
</html>
""" % string
	return index_html