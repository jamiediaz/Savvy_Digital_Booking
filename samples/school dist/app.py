import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, text

from flask import (
    Flask,
    render_template,
    jsonify,
    request,
    redirect)
# from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)

# create connection to postgres DB on heroku
engine = create_engine("postgres://dazxhzuujjpiff:497bacf442be164459dc99767de73a4e9444203b9010665a463f437c58a2a7c4@ec2-174-129-238-192.compute-1.amazonaws.com:5432/dcr78ck60asptk")
conn = engine.connect()
# app.config["SQLALCHEMY_DATABASE_URI"] = "postgres://dazxhzuujjpiff:497bacf442be164459dc99767de73a4e9444203b9010665a463f437c58a2a7c4@ec2-174-129-238-192.compute-1.amazonaws.com:5432/dcr78ck60asptk"
# db = SQLAlchemy(app)

# reflect the database tables

Base = automap_base()
Base.prepare(engine, reflect=True)


# assign the tables to the variables. 
sqft_price = Base.classes.price
sc_ranking = Base.classes.ranking
h_price = Base.classes.house_price
d_avg = Base.classes.districtavg
p_avg = Base.classes.priceavg
d_ratio = Base.classes.districtratios
arc_prop = Base.classes.arc_prop
# arc_geo = Base.classes.arc_geo

# start flask
app = Flask(__name__)
CORS(app)

@app.route("/")
def index():
    """Return the homepage."""
    return render_template("index.html")


@app.route("/about.html")
def about():
    """Return the homepage."""
    return render_template("about.html")


@app.route("/school.html")
def school():
    """Return the homepage."""
    return render_template("school.html")

@app.route('/data')
def get_data():
    global data
    return json.dumps(data)
    
@app.route("/api")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/v1.0/price<br/>"
        f"/v1.0/ranking<br/>"
        f"/v1.0/house_price<br/>"
        f"/v1.0/dist_avg</br>"
        f"/v1.0/price_avg</br>"
        f"/v1.0/dist_ratio</br>"
        f"/v1.0/dist_names</br>"
        f"/v1.0/arc_data</br>"
       )


@app.route("/api/v1.0/price.json")
def price():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Prices per sqft by zip as of May 2018"""
    # Query all price per sqft tables using ORM and save to results
    results = session.query(sqft_price.zip_code, sqft_price.city, sqft_price.price).all()
    
    session.close()
    
    # Loop through results and grab the column data and put them into the prices_dict.  
    # Then append them to the all_prices list. 

    all_prices = []
    for zip_code, city, price in results:
        prices_dict = {}
        prices_dict["zip"] = zip_code
        prices_dict["city"] = city
        prices_dict["price"] = price
        all_prices.append(prices_dict)

    # Convert list of tuples into normal list
    # all_names = list(np.ravel(results))

    #jsonify the all_prices list for easy reading. 
    return jsonify(all_prices)


@app.route("/api/v1.0/ranking.json")
def ranking():

    
    session = Session(engine)

    """Return a list of school and district rankings"""
    
    results = session.query(sc_ranking.district_name, sc_ranking.school_id, sc_ranking.school_name, sc_ranking.date, sc_ranking.ela_exams_total, sc_ranking.ela_proficient_total, sc_ranking.math_exams_total, sc_ranking.math_proficient_total, sc_ranking.total_exams, sc_ranking.total_score, sc_ranking.school_rating).all()

    session.close()
    
    all_rankings = []
    for district_name, school_id, school_name, date, ela_exams_total, ela_proficient_total, math_exams_total, math_proficient_total, total_exams, total_score, school_rating in results:
        ranking_dict = {}
        # ranking_dict["state"] = State
        # ranking_dict["FIPST"] = FIPST
        # ranking_dict["state_id"] = State_ID
        ranking_dict["distric_name"] = district_name
        ranking_dict["school_id"] = school_id
        ranking_dict["school_name"] = school_name
        ranking_dict["date"] = date
        ranking_dict["ela_exams_total"] = ela_exams_total
        ranking_dict["ela_proficient_total"] = ela_proficient_total
        ranking_dict["math_exams_total"] = math_exams_total
        ranking_dict["math_proficient_total"] = math_proficient_total
        ranking_dict["total_exams"] = total_exams
        ranking_dict["total_score"] = total_score
        ranking_dict["school_rating"] = school_rating
        
        all_rankings.append(ranking_dict)

    return jsonify(all_rankings)


@app.route("/api/v1.0/house_price.json")
def house_price():
    
    session = Session(engine)

    """House prices, school ratings, and district ratings API"""
    
    results = session.query(h_price.district_name, h_price.district_code, h_price.school_id, h_price.zip_code, h_price.school_name, h_price.city, h_price.sizerank, h_price.price, h_price.school_type, h_price.total_score).all()
    
    session.close()
    
    house_prices = []
    for district_name, district_code, school_id, zip_code, school_name, city, sizerank, price, school_type, total_score in results:
        h_prices_dict = {}
        h_prices_dict["district_name"] = district_name
        h_prices_dict["district_code"] = district_code
        h_prices_dict["school_id"] = school_id
        h_prices_dict["zip"] = zip_code
        h_prices_dict["school_name"] = school_name
        h_prices_dict["city"] = city
        h_prices_dict["size_rank"] = sizerank
        h_prices_dict["price"] = price
        h_prices_dict["type"] = school_type
        h_prices_dict["score"] = total_score
        house_prices.append(h_prices_dict)

    return jsonify(house_prices)


@app.route("/api/v1.0/school_plots/<short_dist_name>")
def school_plot(short_dist_name):
    
    
    short_dist_name = short_dist_name.lower()
    # print(name)
    sqlquery = f"select * from house_price where short_dist_name = '{short_dist_name}';"

    plot_df = pd.read_sql_query(sqlquery, conn)
    # plot_df['total_score'] = plot_df.total_score.fillna(0) 
    #
    print(plot_df)
    
    district_plot = []
    # # for district_name, School_Name, Price, school_type, total_score in results:
    for x in plot_df.index:
        school_dict = {}
        school_dict["district_name"] = plot_df['district_name'][x]
        # school_dict["short_dist_name"] = result[1]
        school_dict["school_name"] = plot_df['school_name'][x]
        school_dict["price"] = plot_df['price'][x]
        school_dict["type"] = plot_df['school_type'][x]
        school_dict["score"] = plot_df['total_score'][x]
        school_dict["zip_code"] = int(plot_df['zip_code'][x])
        district_plot.append(school_dict)

    return jsonify(district_plot)


@app.route("/api/v1.0/dist_avg.json")
def dist_avg():
    
    session = Session(engine)

    """District avarage scores"""
    
    results = session.query(d_avg.district_name, d_avg.total_score, d_avg.district_rating).all()
    
    session.close()
    
    district_average = []
    for district_name, total_score, district_rating in results:
        d_avg_dict = {}
        d_avg_dict["district_name"] = district_name
        d_avg_dict["total_score"] = total_score
        d_avg_dict["district_rating"] = district_rating
        
        district_average.append(d_avg_dict)
       
    return jsonify(district_average)    


@app.route("/api/v1.0/price_avg.json")
def price_avg():
    
    session = Session(engine)

    """price avarage API"""
    
    results = session.query(p_avg.district_name, p_avg.price).all()
    
    session.close()
    
    price_average = []
    for district_name, price in results:
        p_avg_dict = {}
        p_avg_dict["district_name"] = district_name
        p_avg_dict["price"] = price
                
        price_average.append(p_avg_dict)
       
    return jsonify(price_average)    


@app.route("/api/v1.0/dist_ratio.json")
def dist_ratio():
    
    session = Session(engine)

    """d_ratio API"""
    
    results = session.query(d_ratio.district_name, d_ratio.price, d_ratio.total_score, d_ratio.district_rating, d_ratio.ratio).all()
    
    session.close()
    
    district_ratio = []
    for district_name, price, total_score, district_rating, ratio in results:
        d_ratio_dict = {}
        d_ratio_dict["district_name"] = district_name
        d_ratio_dict["price"] = price
        d_ratio_dict["total_score"] = total_score
        d_ratio_dict["district_rating"] = district_rating
        d_ratio_dict["ratio"] = ratio

                
        district_ratio.append(d_ratio_dict)
       
    return jsonify(district_ratio)   


@app.route("/api/v1.0/dist_names.json")
def dist_names():
    
    session = Session(engine)

    """d_names API"""
    
    results = session.query(d_avg.district_name).all()
    
    session.close()
    
    district_names = []
    for district_name in results:
        district_names.append(district_name[0])
               
    return jsonify(district_names)   





@app.route("/api/v1.0/arc_data.geojson")
def arc_data():
    
    session = Session(engine)

    """arc_data API"""
    
    results = session.query(arc_prop.campus, arc_prop.district, arc_prop.distname, arc_prop.phone, arc_prop.match_addr, arc_prop.cntyname, arc_prop.long, arc_prop.lat, arc_prop.zip, arc_prop.school_name, arc_prop.school_type, arc_prop.price, arc_prop.nn_1yr, arc_prop.nn_5yr, arc_prop.nn_10yr, arc_prop.gain_yr1, arc_prop.gain_yr5, arc_prop.gain_yr10,  arc_prop.total_score).all()
    
    session.close()
    
    arc_dict = dict(type ="FeatureCollection", features = []) 
    
    for campus, district, distname, phone, match_addr, cntyname, long, lat, zip, school_name, school_type, price, nn_1yr, nn_5yr, nn_10yr, gain_yr1, gain_yr5, gain_yr10, total_score in results:
        prop_dict = {}
        
        prop_dict["type"] = "Feature"
        prop_dict["properties"] = {}
        prop_dict["geometry"] = {}
        prop_dict["properties"]["school_id"] = campus
        prop_dict["properties"]["school_name"] = school_name
        prop_dict["properties"]["type"] = school_type
        prop_dict["properties"]["district_id"] = district
        prop_dict["properties"]["district_name"] = distname
        prop_dict["properties"]["phone"] = phone
        prop_dict["properties"]["address"] = match_addr
        prop_dict["properties"]["zip_code"] = zip
        prop_dict["properties"]["county"] = cntyname
        prop_dict["properties"]["price"] = price
        prop_dict["properties"]["year_01_forecast"] = nn_1yr
        prop_dict["properties"]["year_05_forecast"] = nn_5yr
        prop_dict["properties"]["year_10_forecast"] = nn_10yr
        prop_dict["properties"]["year_01_change"] = gain_yr1
        prop_dict["properties"]["year_05_change"] = gain_yr5
        prop_dict["properties"]["year_10_change"] = gain_yr10
        prop_dict["properties"]["total_score"] = total_score
        prop_dict["geometry"]["type"] = "Point"
        prop_dict["geometry"]["coordinates"] = [long, lat]
                        
        arc_dict['features'].append(prop_dict)

    return jsonify(arc_dict)   

if __name__ == '__main__':
    app.run()
