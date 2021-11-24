import sqlalchemy as sa
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify, render_template

import pandas as pd

engine = sa.create_engine('postgresql+psycopg2://postgres:postgres@10.0.2.62/FileSearch')



app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api")
def welcome():
    
    return "Available Routes:<br/> /v1.0/accounting<br/> /v1.0/company<br/> /v1.0/drilling<br/> /v1.0/land</br> /v1.0/production</br> /v1.0/well_files</br>"
            

# @app.route("/api/v1.0/accounting")
# def accountingAPI():
#     sqlquery = "SELECT * FROM accounting;"
#     df = pd.read_sql_query(sqlquery, engine)
#     accnt_list =[]
#     for x in df.index:
#         accnt_dict = {}
#         accnt_dict["FileName"] = df['filename'][x]
#         accnt_dict["FullPath"] = df['fullpath'][x]
#         accnt_dict["SubFolder1"] = df['subfolder1'][x]
#         accnt_dict["SubFolder2"] = df['subfolder2'][x]
#         accnt_dict["FileSize"] = int(df['filesize'][x])
#         accnt_dict["TimeStamp"] = df['timestamp'][x]
#         accnt_list.append(accnt_dict)

#     # print(accnt_list)
#     return jsonify(accnt_list)

# @app.route("/api/v1.0/company")
# def companyAPI():
#     sqlquery = "SELECT * FROM company;"
#     df = pd.read_sql_query(sqlquery, engine)
#     compy_list =[]
#     for x in df.index:
#         compy_dict = {}
#         compy_dict["FileName"] = df['filename'][x]
#         compy_dict["FullPath"] = df['fullpath'][x]
#         compy_dict["SubFolder1"] = df['subfolder1'][x]
#         compy_dict["SubFolder2"] = df['subfolder2'][x]
#         compy_dict["FileSize"] = int(df['filesize'][x])
#         compy_dict["TimeStamp"] = df['timestamp'][x]
#         compy_list.append(compy_dict)

#     return jsonify(compy_list)

# @app.route("/api/v1.0/drilling")
# def drillingAPI():
#     sqlquery = "SELECT * FROM drilling;"
#     df = pd.read_sql_query(sqlquery, engine)
#     drlng_list =[]
#     for x in df.index:
#         drlng_dict = {}
#         drlng_dict["FileName"] = df['filename'][x]
#         drlng_dict["FullPath"] = df['fullpath'][x]
#         drlng_dict["SubFolder1"] = df['subfolder1'][x]
#         drlng_dict["SubFolder2"] = df['subfolder2'][x]
#         drlng_dict["FileSize"] = int(df['filesize'][x])
#         drlng_dict["TimeStamp"] = df['timestamp'][x]
#         drlng_list.append(drlng_dict)

#     return jsonify(drlng_list)

# @app.route("/api/v1.0/land")
# def landAPI():
#     sqlquery = "SELECT * FROM land;"
#     df = pd.read_sql_query(sqlquery, engine)
#     land_list =[]
#     for x in df.index:
#         land_dict = {}
#         land_dict["FileName"] = df['filename'][x]
#         land_dict["FullPath"] = df['fullpath'][x]
#         land_dict["SubFolder1"] = df['subfolder1'][x]
#         land_dict["SubFolder2"] = df['subfolder2'][x]
#         land_dict["FileSize"] = int(df['filesize'][x])
#         land_dict["TimeStamp"] = df['timestamp'][x]
#         land_list.append(land_dict)

#     return jsonify(land_list)

# @app.route("/api/v1.0/production")
# def prodAPI():
#     sqlquery = "SELECT * FROM production;"
#     df = pd.read_sql_query(sqlquery, engine)
#     prod_list =[]
#     for x in df.index:
#         prod_dict = {}
#         prod_dict["FileName"] = df['filename'][x]
#         prod_dict["FullPath"] = df['fullpath'][x]
#         prod_dict["SubFolder1"] = df['subfolder1'][x]
#         prod_dict["SubFolder2"] = df['subfolder2'][x]
#         prod_dict["FileSize"] = int(df['filesize'][x])
#         prod_dict["TimeStamp"] = df['timestamp'][x]
#         prod_list.append(prod_dict)

#     return jsonify(prod_list)

# @app.route("/api/v1.0/well_files")
# def wellAPI():
#     sqlquery = "SELECT * FROM well_files;"
#     df = pd.read_sql_query(sqlquery, engine)
#     well_list =[]
#     for x in df.index:
#         well_dict = {}
#         well_dict["FileName"] = df['filename'][x]
#         well_dict["FullPath"] = df['fullpath'][x]
#         well_dict["SubFolder1"] = df['subfolder1'][x]
#         well_dict["SubFolder2"] = df['subfolder2'][x]
#         well_dict["FileSize"] = int(df['filesize'][x])
#         well_dict["TimeStamp"] = df['timestamp'][x]
#         well_list.append(well_dict)

#     return jsonify(well_list)

@app.route("/api/v1.0/accounting/<name_of_file>")
def accountingFilteredAPI(name_of_file):
    
    # queries database for specific file using name in URL
    sqlquery = f"SELECT * FROM accounting WHERE UPPER (filename) LIKE UPPER ('%%{name_of_file}%%') ORDER BY subfolder1 ASC NULLS FIRST, subfolder2 ASC NULLS FIRST, fullpath ASC NULLS FIRST;"

    #query the database using above query and copy results to a dataframe
    df = pd.read_sql_query(sqlquery, engine)
    
    # #jsonify the dataframe
    accnt_list = []
    
    for x in df.index:
        accnt_dict = {}
        accnt_dict["FileName"] = df['filename'][x]
        accnt_dict["FullPath"] = df['fullpath'][x]
        
        accnt_dict["SubFolder1"] = df['subfolder1'][x]
        accnt_dict["SubFolder2"] = df['subfolder2'][x]
        accnt_dict["SubFolder3"] = df['subfolder3'][x]
        accnt_dict["FileSize"] = int(df['filesize'][x])
        accnt_dict["TimeStamp"] = df['timestamp'][x]
        accnt_dict["Year"] = df['year'][x]
        accnt_dict["Month"] = df['month'][x]
        accnt_list.append(accnt_dict)

    # print(accnt_list)
    return jsonify(accnt_list)

    # df.columns = ['FileName','FullPath','SubFolder1','Subfolder2','Subfolder3','FileSize','TimeStamp','Year','Month']
    # df['FileSize'] = int(df["FileSize"])
    # Return df.to_json(orient="records")

@app.route("/api/v1.0/company/<name_of_file>")
def companyFilteredAPI(name_of_file):
    
    sqlquery = f"SELECT * FROM company WHERE UPPER (filename) LIKE UPPER ('%%{name_of_file}%%') ORDER BY subfolder1 ASC NULLS FIRST, subfolder2 ASC NULLS FIRST, fullpath ASC NULLS FIRST;"

    df = pd.read_sql_query(sqlquery, engine)
        
    compy_list = []
    for x in df.index:
        compy_dict = {}
        compy_dict["FileName"] = df['filename'][x]
        compy_dict["FullPath"] = df['fullpath'][x]
        compy_dict["SubFolder1"] = df['subfolder1'][x]
        compy_dict["SubFolder2"] = df['subfolder2'][x]
        compy_dict["SubFolder3"] = df['subfolder3'][x]
        compy_dict["FileSize"] = int(df['filesize'][x])
        compy_dict["TimeStamp"] = df['timestamp'][x]
        compy_dict["Year"] = df['year'][x]
        compy_dict["Month"] = df['month'][x]
        compy_list.append(compy_dict)

    return jsonify(compy_list)

@app.route("/api/v1.0/drilling/<name_of_file>")
def drillingFilteredAPI(name_of_file):
    
    sqlquery = f"SELECT * FROM drilling WHERE UPPER (filename) LIKE UPPER ('%%{name_of_file}%%') ORDER BY subfolder1 ASC NULLS FIRST, subfolder2 ASC NULLS FIRST, fullpath ASC NULLS FIRST;"

    df = pd.read_sql_query(sqlquery, engine)
        
    drlng_list = []
    for x in df.index:
        drlng_dict = {}
        drlng_dict["FileName"] = df['filename'][x]
        drlng_dict["FullPath"] = df['fullpath'][x]
        drlng_dict["SubFolder1"] = df['subfolder1'][x]
        drlng_dict["SubFolder2"] = df['subfolder2'][x]
        drlng_dict["SubFolder3"] = df['subfolder3'][x]
        drlng_dict["FileSize"] = int(df['filesize'][x])
        drlng_dict["TimeStamp"] = df['timestamp'][x]
        drlng_dict["Year"] = df['year'][x]
        drlng_dict["Month"] = df['month'][x]
        drlng_list.append(drlng_dict)

    return jsonify(drlng_list)

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
    app.run(host='0.0.0.0')
    # app.run()
