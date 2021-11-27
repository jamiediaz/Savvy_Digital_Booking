import sqlalchemy as sa
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import (
    Flask,
    render_template,
    jsonify,
    request,
    redirect)
# from flask_sqlalchemy import SQLAlchemy


import numpy as np
import pandas as pd

from flask_cors import CORS

engine = sa.create_engine('postgres://hsowclklmlcrcr:3406df177a4357c1ca87650b7591438a195116fd79eb64c7d37baf5cdf30a345@ec2-34-228-154-153.compute-1.amazonaws.com:5432/d3bahjahquj20r')



app = Flask(__name__)

@app.route("/")
def index():
    
    return render_template("index.html")

@app.route("/api")
def welcome():
    
    return "Available Routes:<br/> /v1.0/calendar</br> /v1.0/appt_requests</br> /api/v1.0/confirmed_dates</br>"
            



@app.route("/api/v1.0/calendar")
def calendarAPI():
    
    # queries database for specific file using name in URL
    sqlquery = f"SELECT * FROM calendar WHERE status = 'confirmed';"

    #query the database using above query and copy results to a dataframe
    df = pd.read_sql_query(sqlquery, engine)
    
    # #jsonify the dataframe
    calendar_list = []
    
    for x in df.index:
        calendar_dict = {}
        calendar_dict["summary"] = df['summary'][x]
        calendar_dict["description"] = df['description'][x]
        
        calendar_dict["id"] = df['id'][x]
        calendar_dict["event_begins"] = df['event_begins'][x]
        calendar_dict["event_ends"] = df['event_ends'][x]
        calendar_dict["status"] = df['status'][x]
        
        calendar_list.append(calendar_dict)

    # print(accnt_list)
    return jsonify(calendar_list)

    # df.columns = ['FileName','FullPath','SubFolder1','Subfolder2','Subfolder3','FileSize','TimeStamp','Year','Month']
    # df['FileSize'] = int(df["FileSize"])
    # Return df.to_json(orient="records")

@app.route("/api/v1.0/appt_requests")
def appt_requestsAPI():
    
    sqlquery = f"SELECT * FROM appt_requests;"

    df = pd.read_sql_query(sqlquery, engine)
        
    appt_requests_list = []
    for x in df.index:
        appt_requests_dict = {}
        appt_requests_dict["summary"] = df['summary'][x]
        appt_requests_dict["description"] = df['description'][x]
        appt_requests_dict["incr_id"] = int(df['incr_id'][x])
        appt_requests_dict["event_begins"] = df['event_begins'][x]
        appt_requests_dict["event_ends"] = df['event_ends'][x]
        appt_requests_dict["attendees"] = df['attendees'][x]
        appt_requests_list.append(appt_requests_dict)

    return jsonify(appt_requests_list)

@app.route("/api/v1.0/confirmed_dates")
def confirmed_dates_API():
    
    sqlquery = f"SELECT event_begins, event_ends FROM calendar WHERE status = 'confirmed';"

    df = pd.read_sql_query(sqlquery, engine)

    df['date_range'] = "{start: '" + df['event_begins'].astype(str) + "', end: '" + df['event_ends'].astype(str) + "}"
    

    conf_dates_list = []
    for x in df.index:
        conf_dates_dict = {}
        conf_dates_dict["event_begins"] = df['event_begins'][x]
        conf_dates_dict["event_ends"] = df['event_ends'][x]
        conf_dates_dict['date_range'] = df['date_range'][x]
        
        conf_dates_list.append(conf_dates_dict)

    return jsonify(conf_dates_list)

@app.route("/api/v1.0/land/<name_of_file>")
def landFilteredAPI(name_of_file):
    
    sqlquery = f"SELECT * FROM land WHERE UPPER (filename) LIKE UPPER ('%%{name_of_file}%%') ORDER BY subfolder1 ASC NULLS FIRST, subfolder2 ASC NULLS FIRST, fullpath ASC NULLS FIRST;"

    df = pd.read_sql_query(sqlquery, engine)
        
    land_list = []
    for x in df.index:
        land_dict = {}
        land_dict["FileName"] = df['filename'][x]
        land_dict["FullPath"] = df['fullpath'][x]
        land_dict["SubFolder1"] = df['subfolder1'][x]
        land_dict["SubFolder2"] = df['subfolder2'][x]
        land_dict["SubFolder3"] = df['subfolder3'][x]
        land_dict["FileSize"] = int(df['filesize'][x])
        land_dict["TimeStamp"] = df['timestamp'][x]
        land_dict["Year"] = df['year'][x]
        land_dict["Month"] = df['month'][x]
        land_list.append(land_dict)

    return jsonify(land_list)

@app.route("/api/v1.0/production/<name_of_file>")
def productionFilteredAPI(name_of_file):
    
    sqlquery = f"SELECT * FROM production WHERE UPPER (filename) LIKE UPPER ('%%{name_of_file}%%') ORDER BY subfolder1 ASC NULLS FIRST, subfolder2 ASC NULLS FIRST, fullpath ASC NULLS FIRST;"

    df = pd.read_sql_query(sqlquery, engine)
        
    prod_list = []
    for x in df.index:
        prod_dict = {}
        prod_dict["FileName"] = df['filename'][x]
        prod_dict["FullPath"] = df['fullpath'][x]
        prod_dict["SubFolder1"] = df['subfolder1'][x]
        prod_dict["SubFolder2"] = df['subfolder2'][x]
        prod_dict["SubFolder3"] = df['subfolder3'][x]
        prod_dict["FileSize"] = int(df['filesize'][x])
        prod_dict["TimeStamp"] = df['timestamp'][x]
        prod_dict["Year"] = df['year'][x]
        prod_dict["Month"] = df['month'][x]
        prod_list.append(prod_dict)

    return jsonify(prod_list)

@app.route("/api/v1.0/well_files/<name_of_file>")
def wellfilesFilteredAPI(name_of_file):
    
    sqlquery = f"SELECT * FROM well_files WHERE UPPER (filename) LIKE UPPER ('%%{name_of_file}%%') ORDER BY subfolder1 ASC NULLS FIRST, subfolder2 ASC NULLS FIRST, fullpath ASC NULLS FIRST;"

    df = pd.read_sql_query(sqlquery, engine)
        
    well_list = []
    for x in df.index:
        well_dict = {}
        well_dict["FileName"] = df['filename'][x]
        well_dict["FullPath"] = df['fullpath'][x]
        well_dict["SubFolder1"] = df['subfolder1'][x]
        well_dict["SubFolder2"] = df['subfolder2'][x]
        well_dict["SubFolder3"] = df['subfolder3'][x]
        well_dict["FileSize"] = int(df['filesize'][x])
        well_dict["TimeStamp"] = df['timestamp'][x]
        well_dict["Year"] = df['year'][x]
        well_dict["Month"] = df['month'][x]
        well_list.append(well_dict)

    return jsonify(well_list)

if __name__ == "__main__":
    # app.run(host='0.0.0.0')
    app.run()
