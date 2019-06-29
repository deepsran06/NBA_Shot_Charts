import os

import pandas as pd
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine

from flask import Flask, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy

from config import username, password

app = Flask(__name__)


#################################################
# Database Setup
#################################################

# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db/bellybutton.sqlite"
app.config["SQLALCHEMY_DATABASE_URI"] = f'mysql://{username}:{password}@localhost/shot_list_db'
db = SQLAlchemy(app)

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(db.engine, reflect=True)
# print(Base.classes.keys())

# Save references to each table
Sample_Metadata = Base.classes.player_list
sample_other = Base.classes.master_shot
Season_Metadata = Base.classes.seasons


@app.route("/")
def index():
    """Return the homepage."""
    return render_template("index.html")

@app.route("/names")
def names():
    
    stmt = db.session.query(Sample_Metadata).statement
    df = pd.read_sql_query(stmt, db.session.bind)

    sample_data = df.loc[:,"full_name"]
    
    # Format the data to send as json
    data = sample_data.values.tolist()

    return jsonify(data)


@app.route("/seasons")
def seasons():
    
    stmt = db.session.query(Season_Metadata).statement
    df = pd.read_sql_query(stmt, db.session.bind)

    season_data = df.loc[:,"Season"]
    
    data = season_data.values.tolist()

    return jsonify(data)

@app.route("/metadata/<Player_Name>")
def sample_metadata(Player_Name):
    
    sel = [
        sample_other.Player_Name,
        sample_other.Loc_X,
        sample_other.Loc_Y,
        sample_other.Game_Date
    ]

    results = db.session.query(*sel).filter(sample_other.Player_Name == Player_Name).all()
    print(results)
    # Create a dictionary entry for each row of metadata information
    sample_metadata = []
    for result in results:
        single_metadata = {"Player_Name" : result[0],
        "Loc_X" : result[1],
        "Loc_Y" : result[2],
        "Game_Date" : result[3]}

        sample_metadata.append(single_metadata)

    print(sample_metadata)
    return jsonify(sample_metadata)



@app.route("/metadata/<Player_Name>/<season>")
def all_sample_metadata(Player_Name, season):
    
    sel = [
        sample_other.Player_Name,
        sample_other.Loc_X,
        sample_other.Loc_Y,
        sample_other.Game_Date
    ]

    results = db.session.query(*sel).filter(sample_other.Player_Name == Player_Name).filter(sample_other.Season == season).all()
    print(results)
    # Create a dictionary entry for each row of metadata information
    all_sample_metadata = []
    for result in results:
        single_metadata = {"Player_Name" : result[0],
        "Loc_X" : result[1],
        "Loc_Y" : result[2],
        "Game_Date" : result[3]}

        all_sample_metadata.append(single_metadata)

    print(all_sample_metadata)
    return jsonify(all_sample_metadata)



@app.route("/samples/<sample>")
def samples(sample):
    
    stmt = db.session.query(Sample_Metadata).statement #QUERY TABLE
    df = pd.read_sql_query(stmt, db.session.bind)

    data = {
        "Loc_X": df[Loc_X].values.tolist(),
        "Loc_Y": df[Loc_Y].values.tolist(),
        "Game_Date": df[Game_Date].tolist(),
    }
    return jsonify(data)


if __name__ == "__main__":
    app.run(debug=True)

