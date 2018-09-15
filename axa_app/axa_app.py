from flask import Flask,render_template, request
import sqlite3 as sq3
import os
import numpy as np

app=Flask(__name__)

db_path=os.path.join(os.getcwd(),'axadb.db')

@app.route("/")
def index():
    return(render_template('layout.html'))

@app.route("/idsearch")
def idsearchfn():
    return(render_template('idsearch.html'))
    #return("Search in this page by care provider ID")

#@app.route("/idsearchload",methods=['POST'])
#def idsearchloadfn():
#    return()

@app.route("/idsearch/result",methods=['GET','POST'])
def idsearchresultfn():
    error=None
    try:
        conn=sq3.connect(db_path)
        cur=conn.cursor()
        cur.execute("select * from care_providers5")
        column_names = [description[0] for description in cur.description]
        
        conn=sq3.connect(db_path)
        cur=conn.cursor()
        cur.execute("select * from care_providers5 where rownum=%s;"%(request.form['id_query']))
        cp_details=(cur.fetchall())[0]
        result={column_names[i]:cp_details[i] for i in range(0,len(column_names))}
        #print(cur.description)
    except:
        error='Queried ID not in database'
    #return(str(cp_details)+str(cur.description))
    return(str(result))
    #return(render_template('idsearchresult.html'))
    #return("Search in this page by care provider ID")


@app.route("/geosearch")
def geosearchfn():
    return(render_template('geosearch.html'))


@app.route("/geosearch/result",methods=['GET','POST'])
def geosearchresultfn():

    lat_q=float(request.form['lat_query'])/180*np.pi
    lng_q=float(request.form['lng_query'])/180*np.pi

    conn=sq3.connect(db_path)
    cur=conn.cursor()
    cur.execute("select lat,lng from care_providers5")
    coord_info=cur.fetchall()
    lat_arr=[]
    lng_arr=[]
    rows_with_coord_info=[]
    for i in range(0,len(coord_info)):
        row=coord_info[i]
        if row[0]!=None and row[1]!=None:
            lat_arr.append(float(row[0])/180*np.pi)
            lng_arr.append(float(row[1])/180*np.pi)
            rows_with_coord_info.append(i)

    lat_arr=np.array(lat_arr)
    lng_arr=np.array(lng_arr)

    straight_dist_norm=np.sqrt( (np.cos(lng_arr)*np.cos(lat_arr)-np.cos(lng_q)*np.cos(lat_q) )**2 +
                                (np.sin(lng_arr)*np.cos(lat_arr)-np.sin(lng_q)*np.cos(lat_q) )**2 +
                                (np.sin(lat_arr)-np.sin(lat_q) )**2   )
    index_nearest=rows_with_coord_info[np.argmin(straight_dist_norm)]

    error=None
    try:
        conn=sq3.connect(db_path)
        cur=conn.cursor()
        cur.execute("select * from care_providers5")
        column_names = [description[0] for description in cur.description]

        conn=sq3.connect(db_path)
        cur=conn.cursor()
        cur.execute("select * from care_providers5 where rownum=%s;"%(index_nearest))
        cp_details=(cur.fetchall())[0]
        output_dict={column_names[i]:cp_details[i] for i in range(0,len(column_names))}
        #print(cur.description)
        geo_dict={'lat':output_dict['lat'],'lng':output_dict['lng']}
        result='lat='+str(output_dict['lat'])+'\nlng='+str(output_dict['lng'])
    except:
        error='Queried ID not in database'
    return(render_template('geosearchresult.html',geo_dict=geo_dict))
    #return(str(cp_details)+str(cur.description))
    
    #return('hello')


@app.route("/bulbpage",methods=['GET','POST'])
def bulbpagefn():
    return("Just for fun")

if __name__=="__main__":
    app.run(debug=True)




