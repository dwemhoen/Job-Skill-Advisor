import sys, sqlite3
import argparse
import os

def main():

    p = argparse.ArgumentParser("Takes as input a term-stats dump and a document name-length dump from an index. Creates a database of the term frequencies which can be used for tf-idf calculations")
    p.add_argument('-d','--db', help="specifies a name for the input db",default='locations.db')
    p.add_argument('-i','--input', help="specifies a name for the input",default='country-city_data.csv')
    args = p.parse_args()


    print('CONNECTING TO DATABASE')
    conn = sqlite3.connect(args.db)
    #conn = sqlite3.connect(location_db,':memory:')
    print('CONNECTED')

    #get largest currently used id
    cursor = conn.execute('''SELECT ID FROM LOCATIONS ORDER BY ID DESC LIMIT 1;''')
    results = cursor.fetchall()
    i = ''
    for topic in results:
        i = int(topic[0])
    i += 1
    
    reader = open(args.input)
    country = ''
    for line in reader:
        name = line.strip()
        if len(name) > 0 and not (name[0].isdigit() or name[0] =='"'):
            name = name.lower()
            name = name.split('-')[0].strip()
            name = name.split('(')[0].strip()
            name = name.replace('of america','').strip()
            name = name.replace('of great britain and northern ireland','').strip()
            if name[-1].isdigit():
                name = name[0:-1]
            if name[-1].isdigit():
                name = name[0:-1]
            #print(name)
            #check what type of location this is
            cursor = conn.execute('''select ID,CODE from LOCATIONS where NAME = "{}";'''.format(name)) 
            topics = cursor.fetchall()
            code = ''
            for topic in topics:
                code = topic[1]
                j = topic[0]

            if code == 'country':
                country = j
            #a city is anything that we have screened out as being invalid or another type of location
            elif not (code == 'ma' or code == 'region'):
                cursor = conn.execute('''INSERT INTO LOCATIONS VALUES (?,?,?);''',(i,name,'city'))
                cursor = conn.execute('''INSERT INTO INCLUDES VALUES (?,?);''',(country,i))
                i += 1
    
    print('TABLES LOADED')

    conn.commit()
    conn.close()

main()
