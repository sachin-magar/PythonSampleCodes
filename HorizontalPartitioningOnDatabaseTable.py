#!/usr/bin/python2.7


import psycopg2

DATABASE_NAME = 'dds_assgn1'


def getopenconnection(user='postgres', password='1234', dbname='dds_assgn1'):
    return psycopg2.connect("dbname='" + dbname + "' user='" + user + "' host='localhost' password='" + password + "'")


def loadratings(ratingstablename, ratingsfilepath, openconnection):
    cursor = openconnection.cursor()

    cursor.execute ("DROP TABLE IF EXISTS Ratings;")    
    cursor.execute ("CREATE TABLE IF NOT EXISTS Ratings (USerID INT not null, MovieID INT not null, Rating DECIMAL not null, Time TEXT);") 
 
    with open(ratingsfilepath, 'r') as file:
        singlebyte=file.read().replace('::', ':')

    with open(ratingsfilepath, "w") as file:
        file.write(singlebyte)
        
    file = open(ratingsfilepath, "r")
    cursor.copy_from(file, ratingstablename, ':')
    file.close()
    
    cursor.execute ("ALTER TABLE ratings DROP COLUMN Time;")

    with open(ratingsfilepath, 'r') as file:
        multybyte=file.read().replace(':', '::')

    with open(ratingsfilepath, "w") as file:
        file.write(multybyte)

def rangepartition(ratingstablename, numberofpartitions, openconnection):
    cursor = openconnection.cursor()
    start = -1;
    end = 0;    
    
    for i in range (numberofpartitions):        
        end += 5/float(numberofpartitions)
        cursor.execute ("DROP TABLE IF EXISTS range_part"+ str(i)+";")
        cursor.execute ("CREATE TABLE IF NOT EXISTS range_part" + str(i) + " AS ( SELECT * FROM "+ ratingstablename +" "+
                        "WHERE rating > " + str(start) + " AND rating <= " + str(end) + " );")        
        start = end
        
    try:
        cursor.execute ("CREATE TABLE IF NOT EXISTS partitionCount (type TEXT, count INT);")
        cursor.execute ("INSERT INTO partitionCount VALUES ('range', "+ str(numberofpartitions) +");")
    except:
        cursor.execute ("INSERT INTO partitionCount VALUES ('range', "+ str(numberofpartitions) +");")


def roundrobinpartition(ratingstablename, numberofpartitions, openconnection):
    cursor = openconnection.cursor()

    cursor.execute("ALTER TABLE "+ratingstablename+" ADD COLUMN rownumber SERIAL;")

    for i in range (numberofpartitions-1):
        cursor.execute ("DROP TABLE IF EXISTS rrobin_part"+ str(i)+";")
        cursor.execute ("CREATE TABLE IF NOT EXISTS rrobin_part" + str(i) + " AS SELECT UserID, MovieID, Rating FROM "+ ratingstablename +" "+
                            "WHERE mod(rownumber,"+str(numberofpartitions)+")-1 = "+str(i)+";")

    cursor.execute ("DROP TABLE IF EXISTS rrobin_part"+ str(numberofpartitions-1)+";")
    cursor.execute ("CREATE TABLE IF NOT EXISTS rrobin_part" + str(numberofpartitions-1) + " AS SELECT UserID, MovieID, Rating FROM "+ ratingstablename +" "+
                    "WHERE mod(rownumber,"+str(numberofpartitions)+") = 0;")
    
    cursor.execute("ALTER TABLE "+str(ratingstablename)+" DROP COLUMN rownumber;")
    
    try:
        cursor.execute ("CREATE TABLE IF NOT EXIST partitionCount (type TEXT, count INT);") 
        cursor.execute ("INSERT INTO partitioncount VALUES ('roundrobin', "+ str(numberofpartitions) +");")
    except:
        cursor.execute ("INSERT INTO partitionCount VALUES ('roundrobin', "+ str(numberofpartitions) +");")


def roundrobininsert(ratingstablename, userid, itemid, rating, openconnection):
    
    cursor = openconnection.cursor()
    
    cursor.execute("SELECT count FROM partitioncount where type = 'roundrobin';")
    numberofpartitions = cursor.fetchone()[0]
   
    cursor.execute("SELECT COUNT(*) FROM "+ ratingstablename+";")    
    count = cursor.fetchone()[0]
  
    next_table = "rrobin_part"+str(count % numberofpartitions)

    cursor.execute("INSERT INTO "+ ratingstablename+" (UserID, MovieID, Rating) VALUES ("+ str(userid) +", "+ str(itemid) + ", " + str(rating)+ ");")
    cursor.execute("INSERT INTO "+ next_table+" (UserID, MovieID, Rating) VALUES ("+ str(userid) +", "+ str(itemid) + ", " + str(rating)+ ");")

def rangeinsert(ratingstablename, userid, itemid, rating, openconnection):
    cursor = openconnection.cursor()
    
    cursor.execute("SELECT count FROM partitioncount where type = 'range';")
    numberofpartitions = cursor.fetchone()[0]
    
    partitions = [0] * numberofpartitions
    end = 0
    
    for i in range(numberofpartitions):        
        end = end + 5/ float(numberofpartitions)
        partitions[i] = end        
    
    for i in range(numberofpartitions):
        if rating <= partitions[i]:
            break
    target_table = "range_part"+str(i)
    
    
    cursor.execute("INSERT INTO "+ ratingstablename+" (UserID, MovieID, Rating) VALUES ("+ str(userid) +", "+ str(itemid) + ", " + str(rating)+ ");")
    cursor.execute("INSERT INTO "+ target_table+" (UserID, MovieID, Rating) VALUES ("+ str(userid) +", "+ str(itemid) + ", " + str(rating)+ ");")

def deletepartitionsandexit(con):
        cursor = con.cursor()
        cursor.execute("DROP SCHEMA public CASCADE;")
        cursor.execute("CREATE SCHEMA public;")
    
def create_db(dbname):
    """
    create a DB by connecting to the default user and database of Postgres
    The function first checks if an existing database exists for a given name, else creates it.
    :return:None
    """
    # Connect to the default database
    con = getopenconnection(dbname='postgres')
    con.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
    cur = con.cursor()

    # Check if an existing database with the same name exists
    cur.execute('SELECT COUNT(*) FROM pg_catalog.pg_database WHERE datname=\'%s\'' % (dbname,))
    count = cur.fetchone()[0]
    if count == 0:
        cur.execute('CREATE DATABASE %s' % (dbname,))  # Create the database
    else:
        print 'A database named {0} already exists'.format(dbname)

    cur.close()
    con.close()




if __name__ == '__main__':
    try:

        # function to do any set up before creating the DB
        before_db_creation_middleware()

        create_db(DATABASE_NAME)

        # function to do any set up after creating the DB
        after_db_creation_middleware(DATABASE_NAME)

        with getopenconnection() as con:
            
            before_test_script_starts_middleware(con, DATABASE_NAME)
            
            after_test_script_ends_middleware(con, DATABASE_NAME)

    except Exception as detail:
        print "Error ==> ", detail
