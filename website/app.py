import sqlalchemy as sa
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session 
from sqlalchemy import create_engine, func

from datetime import datetime, timedelta


from flask import (
    Flask,
    render_template,
    jsonify,
    request,
    redirect)


import numpy as np
import pandas as pd

from flask_cors import CORS

#connection to the database
engine = sa.create_engine('postgres://hsowclklmlcrcr:3406df177a4357c1ca87650b7591438a195116fd79eb64c7d37baf5cdf30a345@ec2-34-228-154-153.compute-1.amazonaws.com:5432/d3bahjahquj20r')
connection = engine.connect() 


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

    
    return jsonify(calendar_list)

    

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
    
    #query the database for only start and end times only on entries that are confirmed.
    sqlquery = f"SELECT event_begins, event_ends FROM calendar WHERE status = 'confirmed';"

    #copy SQL query results into a Pandas data frame. 
    df = pd.read_sql_query(sqlquery, engine)

    #Convert df['event_ends'] column to datetime
    df['event_ends_converted'] = pd.to_datetime(df['event_ends'])
    
    #Subtract 1 minute from the end time. 
    df['event_ends_converted'] = df['event_ends_converted'] - pd.to_timedelta(1, unit='minutes')
    
    #Convert column back to string
    df['event_ends_converted'] = df['event_ends_converted'].astype(str)
    
    #Fill in the empty space created when the string was converted to datetime with the letter T. 
    df['event_ends_converted'] = df['event_ends_converted'].replace(' ','T', regex=True)

    #Create a new column with the event begins and event ends together in a string.     
    df['date_range'] = "start: '" + df['event_begins'].astype(str) + "', end: '" + df['event_ends_converted'] + "'"
    
    #create a dictionary entry for the recurring invalid days.  Saturday and Sunday will show up as disabled on the calendar.
    recurring_dict = {'recurring': {'repeat': 'weekly', 'weekDays': 'SA,SU'}}

    #Create the API using this new date range column
    conf_dates_list = []
    
    #loop through the dataframe and put them into an array of dictionaries. 
    for x in df.index:
        conf_dates_dict = {}
        conf_dates_dict["start"] = df['event_begins'][x]
        conf_dates_dict["end"] = df['event_ends_converted'][x]
        #conf_dates_dict['date_range'] = df['date_range'][x]
        
        conf_dates_list.append(conf_dates_dict)
    
    #append the recurring dictionary entry at the end of the API.  
    conf_dates_list.append(recurring_dict)
    
    #jsonify the array and present it as a restfulAPI
    return jsonify(conf_dates_list)


@app.route("/DBentry")
def DBentry():

    #extract data from URL request
    start_date = request.args.get('sdmDate')
    start_time = request.args.get('sdmStartTime')
    fname = request.args.get('sdmFName')
    lname = request.args.get('sdmLName')
    user_email = request.args.get('sdmEmail')
    phone_number = request.args.get('sdmPhone')

    #concat start_time and start_date into ISO format. 
    start_date_time = start_date + "T" + start_time

    #change format to timedelta for end_time
    end_date_time = pd.to_datetime(start_date_time)
    
    #add 1 hour to start_date_time for end time variable. 
    end_date_time = end_date_time + pd.to_timedelta(1, unit='hours')

    #convert end_date_time to string and into ISO format.
    end_date_time = end_date_time.strftime('%Y-%m-%dT%H:%M:%S')
    
    #Concat first and last name 
    full_name = fname + ' ' + lname

    #create a dictionary called data with the contents
    data = {'summary':[full_name],
            'description':[phone_number],
            'event_begins':[start_date_time],
            'event_ends':[end_date_time],
            'attendees':[user_email]}
    
    #create a Pandas dataframe using the dictionary.
    new_SQL_row = pd.DataFrame(data)
    #new_SQL_row = new_SQL_row.reset_index(inplace=True, drop=True)

    #upload to the SQL database using the Pandas database updater
    new_SQL_row.to_sql(name='appt_requests', con=connection, if_exists='append')
    with engine.connect() as con:
         con.execute("select * from appt_requests")
    
    #insert new row into appt_request table in the SQL database using new data. 
    #connection.execute("INSERT INTO appt_requests(summary, description, event_begins, event_ends, attendees) VALUES (:full_name, :user_email, :start_date_time,:end_date_time,:user_email)",{"summary": full_name, "description": user_email, "event_begins": start_date_time, "event_ends": end_date_time, "attendees": user_email})
    
    #display the confrimation webpage
    return render_template("confirm.html")
    
if __name__ == "__main__":
    # app.run(host='0.0.0.0')
    app.run()
