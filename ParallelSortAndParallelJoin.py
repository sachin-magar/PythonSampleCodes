#!/usr/bin/python2.7

import psycopg2
import os
import sys
import threading

FIRST_TABLE_NAME = 'table1'
SECOND_TABLE_NAME = 'table2'
SORT_COLUMN_NAME_FIRST_TABLE = 'column1'
SORT_COLUMN_NAME_SECOND_TABLE = 'column2'
JOIN_COLUMN_NAME_FIRST_TABLE = 'column1'
JOIN_COLUMN_NAME_SECOND_TABLE = 'column2'


def ParallelSort(InputTable, SortingColumnName, OutputTable, openconnection):
    try:
        cursor = openconnection.cursor()

        cursor.execute("SELECT COLUMN_NAME,DATA_TYPE FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME='" + InputTable + "'")
        schema = cursor.fetchall()

        cursor.execute("SELECT MIN(" + SortingColumnName + ") FROM " + InputTable + "")
        temp = cursor.fetchone()
        minimum_value = (float)(temp[0])

        cursor.execute("SELECT MAX(" + SortingColumnName + ") FROM " + InputTable + "")
        temp = cursor.fetchone()
        maximum_value = (float)(temp[0])

        interval = (maximum_value - minimum_value) / 5

        for i in range(5):
            cursor.execute("DROP TABLE IF EXISTS range_part" + str(i) + "")
            cursor.execute("CREATE TABLE IF NOT EXISTS range_part" + str(i) + "(" + schema[0][0] + " " + schema[0][1] + ")")

            for j in range(1, len(schema)):
                cursor.execute("ALTER TABLE range_part" + str(i) + " ADD COLUMN " + schema[j][0] + " " + schema[j][1] + ";")

        thread1 = threading.Thread(target=sort_range, args=(InputTable, SortingColumnName, minimum_value, minimum_value + interval,0, openconnection))
        thread1.start()
        minimum_value = minimum_value + interval

        thread2 = threading.Thread(target=sort_range, args=(InputTable, SortingColumnName, minimum_value, minimum_value + interval,1, openconnection))
        thread2.start()
        minimum_value = minimum_value + interval

        thread3 = threading.Thread(target=sort_range, args=(InputTable, SortingColumnName, minimum_value, minimum_value + interval,2, openconnection))
        thread3.start()
        minimum_value = minimum_value + interval

        thread4 = threading.Thread(target=sort_range, args=(InputTable, SortingColumnName, minimum_value, minimum_value + interval,3, openconnection))
        thread4.start()
        minimum_value = minimum_value + interval

        thread5 = threading.Thread(target=sort_range, args=(InputTable, SortingColumnName, minimum_value, minimum_value + interval,4, openconnection))
        thread5.start()


        cursor.execute("DROP TABLE IF EXISTS " + OutputTable + "")
        cursor.execute("CREATE TABLE " + OutputTable + " (" + schema[0][0] + " " + schema[0][1] + ")")

        for i in range(1, len(schema)):
            cursor.execute("ALTER TABLE " + OutputTable + " ADD COLUMN " + schema[i][0] + " " + schema[i][1] + "")

        for i in range(5):
            cursor.execute("INSERT INTO " + OutputTable + " SELECT * FROM " + "range_part" + str(i) + "")

    except Exception as e:
        print "Exception: ", e
    finally:
        openconnection.commit()


def sort_range(InputTable, SortingColumnName, minimum_value, maximum_value,i, openconnection):
    cursor = openconnection.cursor()
    if i == 0:
        cursor.execute(
            "INSERT INTO range_part0 SELECT * FROM " + InputTable +
            " WHERE " + SortingColumnName + " >= " + str(minimum_value) +
            " AND " + SortingColumnName + " <= " + str(maximum_value) +
            " ORDER BY " + SortingColumnName + " ASC")
    else:
        cursor.execute("INSERT INTO range_part" + str(i) + " SELECT * FROM " + InputTable +
                       " WHERE " + SortingColumnName + " > " + str(minimum_value) +
                       " AND " + SortingColumnName + " <= " + str(maximum_value) +
                       " ORDER BY " + SortingColumnName + " ASC")
    return


def ParallelJoin(InputTable1, InputTable2, Table1JoinColumn, Table2JoinColumn, OutputTable, openconnection):
    try:
        cursor = openconnection.cursor()

        cursor.execute("SELECT MIN(" + Table1JoinColumn + ") FROM " + InputTable1 + "")
        temp = cursor.fetchone()
        minimum_value1 = (float)(temp[0])

        cursor.execute("SELECT MIN(" + Table2JoinColumn + ") FROM " + InputTable2 + "")
        temp = cursor.fetchone()
        minimum_value2 = (float)(temp[0])

        cursor.execute("SELECT MAX(" + Table1JoinColumn + ") FROM " + InputTable1 + "")
        temp = cursor.fetchone()
        maximum_value1 = (float)(temp[0])

        cursor.execute("SELECT MAX(" + Table2JoinColumn + ") FROM " + InputTable2 + "")
        temp = cursor.fetchone()
        maximum_value2 = (float)(temp[0])

        final_max = maximum_value1 if maximum_value1 > maximum_value2 else maximum_value2
        final_min = minimum_value1 if minimum_value1 < minimum_value2 else minimum_value2

        interval = (final_max - final_min) / 5

        cursor.execute(
            "SELECT COLUMN_NAME,DATA_TYPE FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME='" + InputTable1 + "'")
        schema1 = cursor.fetchall()

        cursor.execute(
            "SELECT COLUMN_NAME,DATA_TYPE FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME='" + InputTable2 + "'")
        schema2 = cursor.fetchall()

        cursor.execute("DROP TABLE IF EXISTS " + OutputTable + "")
        cursor.execute("CREATE TABLE " + OutputTable + " (" + schema1[0][0] + " " + schema2[0][1] + ")")

        for i in range(1, len(schema1)):
            cursor.execute("ALTER TABLE " + OutputTable + " ADD COLUMN " + schema1[i][0] + " " + schema1[i][1] + ";")

        for i in range(len(schema2)):
            cursor.execute(
                "ALTER TABLE " + OutputTable + " ADD COLUMN " + schema2[i][0] + "1" + " " + schema2[i][1] + ";")

        low = final_min
        for i in range(5):
            high = low + interval
            cursor.execute("DROP TABLE IF EXISTS first_table_part" + str(i) + ";")
            cursor.execute("DROP TABLE IF EXISTS second_table_part" + str(i) + ";")

            if i == 0:
                cursor.execute("CREATE TABLE first_table_part" + str(i) + " AS SELECT * FROM " + InputTable1 +
                               " WHERE (" + Table1JoinColumn + " >= " + str(low) +
                               ") AND (" + Table1JoinColumn + " <= " + str(high) + ");")
                cursor.execute("CREATE TABLE second_table_part" + str(i) + " AS SELECT * FROM " + InputTable2 +
                               " WHERE (" + Table2JoinColumn + " >= " + str(low) +
                               ") AND (" + Table2JoinColumn + " <= " + str(high) + ");")
            else:
                cursor.execute("CREATE TABLE first_table_part" + str(i) + " AS SELECT * FROM " + InputTable1 +
                               " WHERE (" + Table1JoinColumn + " > " + str(low) +
                               ") AND (" + Table1JoinColumn + " <= " + str(high) + ");")
                cursor.execute("CREATE TABLE second_table_part" + str(i) + " AS SELECT * FROM " + InputTable2 +
                               " WHERE (" + Table2JoinColumn + " > " + str(low) +
                               ") AND (" + Table2JoinColumn + " <= " + str(high) + ");")

            low = high

            cursor.execute("DROP TABLE IF EXISTS output_table_part" + str(i) + "")
            cursor.execute("CREATE TABLE output_table_part" + str(i) + " (" + schema1[0][0] + " " + schema2[0][1] + ")")

            for j in range(1, len(schema1)):
                cursor.execute(
                    "ALTER TABLE output_table_part" + str(i) + " ADD COLUMN " + schema1[j][0] + " " + schema1[j][
                        1] + ";")

            for j in range(len(schema2)):
                cursor.execute(
                    "ALTER TABLE output_table_part" + str(i) + " ADD COLUMN " + schema2[j][0] + "1" + " " + schema2[j][
                        1] + ";")

        thread_1 = threading.Thread(target=join_range, args=(Table1JoinColumn, Table2JoinColumn, openconnection, 0))
        thread_1.start()

        thread_2 = threading.Thread(target=join_range, args=(Table1JoinColumn, Table2JoinColumn, openconnection, 1))
        thread_2.start()

        thread_3 = threading.Thread(target=join_range, args=(Table1JoinColumn, Table2JoinColumn, openconnection, 2))
        thread_3.start()

        thread_4 = threading.Thread(target=join_range, args=(Table1JoinColumn, Table2JoinColumn, openconnection, 3))
        thread_4.start()

        thread_5 = threading.Thread(target=join_range, args=(Table1JoinColumn, Table2JoinColumn, openconnection, 4))
        thread_5.start()

        for i in range(5):
            cursor.execute("INSERT INTO " + OutputTable + " SELECT * FROM output_table_part" + str(i))

    except Exception as e:
        print "Exception", e
    finally:
        openconnection.commit()


def join_range(Table1JoinColumn, Table2JoinColumn, openconnection, i):
    cursor = openconnection.cursor()

    cursor.execute("INSERT INTO output_table_part" + str(i) + " SELECT * FROM first_table_part" + str(i) +
                   " INNER JOIN second_table_part" + str(i) +
                   " ON first_table_part" + str(i) + "." + Table1JoinColumn + "=" + "second_table_part" + str(i) + "." + Table2JoinColumn + ";")
    return



def getOpenConnection(user='postgres', password='1234', dbname='ddsassignment3'):
    return psycopg2.connect("dbname='" + dbname + "' user='" + user + "' host='localhost' password='" + password + "'")


def createDB(dbname='ddsassignment3'):
    """
    We create a DB by connecting to the default user and database of Postgres
    The function first checks if an existing database exists for a given name, else creates it.
    :return:None
    """
    # Connect to the default database
    con = getOpenConnection(dbname='postgres')
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
    con.commit()
    con.close()


def deleteTables(ratingstablename, openconnection):
    try:
        cursor = openconnection.cursor()
        if ratingstablename.upper() == 'ALL':
            cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'")
            tables = cursor.fetchall()
            for table_name in tables:
                cursor.execute('DROP TABLE %s CASCADE' % (table_name[0]))
        else:
            cursor.execute('DROP TABLE %s CASCADE' % (ratingstablename))
        openconnection.commit()
    except psycopg2.DatabaseError, e:
        if openconnection:
            openconnection.rollback()
        print 'Error %s' % e
        sys.exit(1)
    except IOError, e:
        if openconnection:
            conn.rollback()
        print 'Error %s' % e
        sys.exit(1)
    finally:
        if cursor:
            cursor.close()


def saveTable(ratingstablename, fileName, openconnection):
    try:
        cursor = openconnection.cursor()
        cursor.execute("Select * from %s" % (ratingstablename))
        data = cursor.fetchall()
        openFile = open(fileName, "w")
        for row in data:
            for d in row:
                openFile.write(`d` + ",")
            openFile.write('\n')
        openFile.close()
    except psycopg2.DatabaseError, e:
        if openconnection:
            openconnection.rollback()
        print 'Error %s' % e
        sys.exit(1)
    except IOError, e:
        if openconnection:
            conn.rollback()
        print 'Error %s' % e
        sys.exit(1)
    finally:
        if cursor:
            cursor.close()


if __name__ == '__main__':
    try:
        # Creating Database ddsassignment3
        print "Creating Database named as ddsassignment3"
        createDB();

        # Getting connection to the database
        print "Getting connection from the ddsassignment3 database"
        con = getOpenConnection();

        # Calling ParallelSort
        print "Performing Parallel Sort"
        ParallelSort(FIRST_TABLE_NAME, SORT_COLUMN_NAME_FIRST_TABLE, 'parallelSortOutputTable', con);

        # Calling ParallelJoin
        print "Performing Parallel Join"
        ParallelJoin(FIRST_TABLE_NAME, SECOND_TABLE_NAME, JOIN_COLUMN_NAME_FIRST_TABLE, JOIN_COLUMN_NAME_SECOND_TABLE,
                     'parallelJoinOutputTable', con);

        # Saving parallelSortOutputTable and parallelJoinOutputTable on two files
        saveTable('parallelSortOutputTable', 'parallelSortOutputTable.txt', con);
        saveTable('parallelJoinOutputTable', 'parallelJoinOutputTable.txt', con);

        # Deleting parallelSortOutputTable and parallelJoinOutputTable
        deleteTables('parallelSortOutputTable', con);
        deleteTables('parallelJoinOutputTable', con);

        if con:
            con.close()

    except Exception as detail:
        print "Error ==> ", detail
