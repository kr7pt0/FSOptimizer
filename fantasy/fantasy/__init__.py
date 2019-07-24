import os
from flask import Flask, flash, request, redirect, url_for, jsonify
from flask_mysqldb import MySQL
from werkzeug.utils import secure_filename
import json
import pandas as pd
from pydfs_lineup_optimizer import Site, Sport, get_optimizer, Player, CSVLineupExporter
import sys
import requests
import csv
from datetime import datetime
UPLOAD_FOLDER = './upload/'
ALLOWED_EXTENSIONS = set(['csv'])

static_file_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'static')

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['PROPAGATE_EXCEPTIONS'] = True

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'fsport'

mysql = MySQL(app)

# custom optimizer
def optimizeJSON(payload):
    raw = pd.read_json((payload["raw"]))
    data = pd.read_json((payload["posted"]))
    optimizer = None
    if (payload["site"] == "DRAFTKINGS"):
        optimizer = get_optimizer(Site.DRAFTKINGS, Sport.GOLF)
        raw['AvgPointsPerGame'] = raw[payload["projection"]]
        raw['AvgPointsPerGame'] = pd.to_numeric(raw["AvgPointsPerGame"]).fillna(0)
    else:
        optimizer = get_optimizer(Site.FANDUEL, Sport.GOLF)
        raw['FPPG'] = raw[payload["projection"]]
        raw['FPPG'] = pd.to_numeric(raw["FPPG"]).fillna(0)
        raw['First Name'] = raw['Name'].map(lambda x: str(x).split()[0])
        raw['Last Name'] = raw['Name'].map(lambda x: str(x).split()[1])
        raw["Injury Indicator"] = ""
        raw['Team'] = raw['TeamAbbrev']
    if os.path.exists("lineup.csv"):
        os.remove("lineup.csv")
    raw.to_csv("lineup.csv") 
    

    optimizer.load_players_from_csv("lineup.csv")

    # advanced options (lock, remove and exposure)
    
    for index, row in data.iterrows():

        if (row['Remove'] == 1):
            print("Removing player: " + row['Name'], row['Remove'])
            player = optimizer.get_player_by_id(row['ID'])
            optimizer.remove_player(player)
        if (row['Lock'] == 1):
            print("Lock player: " + row['Name'], row['Remove'])
            player = optimizer.get_player_by_id(row['ID'])
            optimizer.add_player_to_lineup(player)
        if ((row['Exposure'] >= 0) and (row['Exposure'] < 100)):
            print("Set exposure : " + row['Name'], row['Exposure'] / 100.0)
            player = optimizer.get_player_by_id(row['ID'])
            print(player)
            player.max_exposure = row['Exposure'] / 100.0
            
    lineupGenerator = optimizer.optimize(payload["lineups"])

    def render_player(player):
        # type: (LineupPlayer) -> str
        result = player.full_name
        #print player.id
        if player.id:
            result += '(%s)' % player.id
        return result

    rows = []
    header = None
    print(lineupGenerator)
    for index, lineup in enumerate(lineupGenerator):
        if index == 0:
            header = [player.lineup_position for player in lineup.lineup]
            header.extend(('Budget', 'FPPG'))
        row = [(render_player)(player) for player in lineup.lineup]
        row.append(str(lineup.salary_costs))
        row.append(str(lineup.fantasy_points_projection))
        rows.append(row)

    data = pd.DataFrame.from_records(rows, columns = header)

    lineups = pd.DataFrame()

    names = []
    positions = []
    teams = []
    fppgs = []
    salaries = []

    # add number to duplicate cols
    def rename_duplicates(old):
        new = []
        seen = {}
        for x in old:
            if x in seen:
                seen[x] += 1
                new.append( "%s_%d" % (x, seen[x]))
            else:
                seen[x] = 0
                new.append(x)
        return new

    data.columns = rename_duplicates(list(data.columns))

    for index, row in data.iterrows():
        for player in data.columns[:-2]:
            playerName = row[player].split("(")[0]
            names.append(playerName)
            positions.append(player)
            player = optimizer.get_player_by_name(playerName)
            fppgs.append(player.fppg)
            teams.append(player.team)
            salaries.append(player.salary)
        positions.append("Totals")
        names.append("")
        teams.append("")
        fppgs.append(row["FPPG"])
        salaries.append(row["Budget"])

        positions.append("")
        names.append("")
        teams.append("")
        fppgs.append("")
        salaries.append("")

        # print row["PG"]

    lineups["Positions"] = positions
    lineups["Name"] = names
    lineups["Team"] = teams
    lineups["Projection"] = fppgs
    lineups["salaries"] = salaries

    result = {"lineups": lineups.values.tolist(),
              "export": [list(data.columns)] + data.values.tolist()}

    return jsonify(result)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
           
from flask import send_file

@app.route('/api/players', methods=['GET', 'POST'])
def api_players():
    # coreCols = ["Name", "Salary", "Position", "TeamAbbrev", "Projection", "Custom"]
    print ("player api called")
    if request.method == 'GET':
        slate = request.args.get('slate')
        cur = mysql.connection.cursor()

        sql_select_query = """select salary, projection from slates where absid = %s"""
        cur.execute(sql_select_query, (slate, ))
        row = cur.fetchone()
        lineup_data = list()
        data = list()
        result = list()
        temp_data = list()
        for player in json.loads(row[0]):
            new_row = list()
            lineup_row = list()
            new_row.append("0")     # Lock
            new_row.append("0")     # Remove
            new_row = new_row + player[0:4]

            lineup_row = lineup_row + player[0:4]
            i = 0
            for projection in json.loads(row[1]):
                if new_row[2] == projection[0]:
                    new_row.append(projection[1])
                    lineup_row.append(projection[1])
                    i = 1
                    break
            if i == 0:
                new_row.append(0)
                lineup_row.append(0)
            new_row.append(new_row[6])
            new_row.append(50)
            lineup_row.append(new_row[6])
            lineup_row.append(50)
            lineup_row.append(player[4])

            temp_row = list(new_row)
            temp_row.append(player[4])
            data.append(new_row)
            lineup_data.append(lineup_row)
            temp_data.append(temp_row)
        cur.close()
        result.append(data)
        result.append(lineup_data)
        result.append(temp_data)
        return jsonify(result)
    if request.method == 'POST':
        coreCols = ["Name", "Salary", "Position", "TeamAbbrev", "Projection", "Custom"]
        print ("post called", file=sys.stderr)
        data = json.loads(request.data)

        lineup_data = data["lineup_data"]
        players = data["players"]
        lineups = data["lineups"]
        site = data["site"]
        projection = data["projection"]
        data = pd.DataFrame.from_records(players)
        data.columns =  ["Lock", "Remove"] + coreCols + ["Exposure", "ID"]

        lineup_writer = open('lineup_temp.csv', 'w+')

        # create the csv writer object

        csvwriter = csv.writer(lineup_writer)

        header = ["Name", "Salary", "Position", "TeamAbbrev", "Projection", "Custom", "Exposure", "ID"]
        csvwriter.writerow(header)

        for r in lineup_data:
            csvwriter.writerow(r)
                        
        lineup_writer.close()
        raw = None
        raw = pd.read_csv("lineup_temp.csv")
        
        payload = {'posted': data.to_json(),
                   "raw": raw.to_json(),
                   "site": site,
                   "projection": projection,
                   "lineups": lineups}

        return optimizeJSON(payload)

@app.route('/api/slates', methods=['GET', 'POST'])
def api_slates():
    print ("slate api called")
    if request.method == 'GET':
        site = request.args.get('site')
        sport_type = request.args.get('sport_type')
        cur = mysql.connection.cursor()
        slate_list = list()
        
        sql_select_query = """select absid, slate_name, slate_time from slates where site = %s and slate_time LIKE %s and sport_type = %s"""
        
        cur_date = "%" + datetime.today().strftime('%Y-%m-%d') + "%"
        cur.execute(sql_select_query, (site, cur_date, sport_type, ))
        records = cur.fetchall()

        for row in records:
            slate_info = {}
            slate_info["id"] = row[0]
            slate_info["name"] = row[2][11:16] + " " + row[1]
            slate_list.append(slate_info)
        cur.close()
        return jsonify(slate_list)








