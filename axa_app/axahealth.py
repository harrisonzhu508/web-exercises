import requests
import json
import sqlite3 as sq3
import os

url='https://health.axa.ch/hack/api/care-providers/111111'

headers={'Authorization':'clumsy cannon'}

resp = requests.get(url,headers=headers)
print(resp.status_code)
print(resp.content)


url2='https://health.axa.ch/hack/api/care-providers?country=CH'
head2={'Authorization':'clumsy cannon'}
#head2={'count':'417','Authorization':'clumsy cannon'}
resp2=requests.get(url2,headers=head2)
print(resp2.status_code)
#print(resp2.content)

resp2json=resp2.content
resp2dict=json.loads(resp2json)
resp2_result=resp2dict['result'] #an array of dictionaries



path_to_db=os.path.join(os.getcwd(),'axadb.db')
table_to_modify="care_providers5"
key_is_text={'rownum':False,'_id':False,'name':True, 'firstName':True, 'street':True, 'houseNr':True, 'zipCode':False, 'city':True, 'country':True, 'mobile':True, 'email':True, 'lat':False, 'lng':False, 'place_id':True, 'type':True, 'title':True}

conn=sq3.connect(path_to_db)
cur=conn.cursor()
#cur.execute("INSERT INTO care_providers ")
#cur.execute("insert into care_providers(name,country) values ('anotherdoc','norway');")
for i in range(0,len(resp2_result)):
    print(i)
    res_inst=resp2_result[i]
    keyslist=list(res_inst.keys())
    cols_list=['rownum']
    vals_list=[i]

    for key in keyslist:
        if not(key=='geocode') and (key in list(key_is_text.keys())):
            cols_list.append(key)
            if key_is_text[key]:
                text_value=res_inst[key]
                if "'" in text_value:
                    text_value=text_value.replace("'","")
                vals_list.append(text_value)
                #cur.execute("insert into "+table_to_modify+"("+ key +") values('"+ text_value  +"');" )
                #cur.execute("insert into "+table_to_modify+"("+ key +") values('"+ res_inst[key] +"');" )
            else:
                vals_list.append(int(res_inst[key]))
                #cur.execute("insert into "+table_to_modify+"("+ key +") values("+ str(res_inst[key]) +");" )

        

        else:
            if not(res_inst['geocode']==None):
                gckeyslist=list(res_inst['geocode']['location'].keys())
                for gckey in gckeyslist:
                    cols_list.append(gckey)
                    vals_list.append(float(res_inst['geocode']['location'][gckey]))

                    #cur.execute("insert into "+table_to_modify+"("+ gckey +") values("+ str(res_inst['geocode']['location'][gckey]) +");" )
                 
    cols_str=(str(cols_list)[1:-1]).replace("'","")
    vals_str=str(vals_list)[1:-1]
    sq3_insert_command="insert into " +table_to_modify+ "(" +cols_str+ ") values ("+ vals_str  +");"
    cur.execute(sq3_insert_command)
    conn.commit()



    #cur.execute("insert into "+table_to_modify+"(__id,name,street,houseNr,zipCode,city,country,lat,lng,place_id,type,title) values (" +str(res_inst['_id'])+ ",'"+ res_inst['name']  +"','"+ res_inst['street'] +"',"+ str(res_inst['houseNr']) +","+ str(res_inst['zipCode']) +",'" + res_inst['city'] + "','" + res_inst['country'] +"'," + str(res_inst['geocode']['location']['lat']) +","+ str(res_inst['geocode']['location']['lng']) +",'"+ res_inst['geocode']['place_id'] +"','"+ res_inst['type'] +"','"+ res_inst['title'] +"');"   )


conn.close()


