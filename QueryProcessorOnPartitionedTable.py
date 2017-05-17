#!/usr/bin/python2.7
#


import psycopg2
import os
import sys

def RangeQuery(ratingsTableName, ratingMinValue, ratingMaxValue, openconnection):

    cursor = openconnection.cursor()


    cursor.execute ("select count(*) from RangeRatingsMetadata;")
    range_n = cursor.fetchone()[0]   
    
    
    for i in range(range_n):
        table_name = 'RangeRatingsPart' + str(i)
        cursor.execute ("select MinRating, MaxRating  from RangeRatingsMetadata where PartitionNum = "+ str(i)+";")
        
        result = cursor.fetchone()
        min = result[0]		
        max = result[1]
        
        if ( ratingMinValue > max or ratingMaxValue < min) :
            continue
                    
        else:            
            cursor.execute("select * from " + str(table_name) +" where rating between "+ str(ratingMinValue) +" and "+ str(ratingMaxValue)+";")            
            temp_data = cursor.fetchall()            
            with open('RangeQueryOut.txt', 'a') as file:
                for t in temp_data:
                    row = 'RangeRatingsPart' + str(i) +','+ str(t[0])+','+str(t[1])+','+ str(t[2])
                    file.write("%s\n" %row)
	
    #roundrobin partition
    cursor.execute ("select PartitionNum from RoundRobinRatingsMetadata;")
    rr_n = cursor.fetchone()[0]
    for i in range(rr_n):
	table_name =  'RoundRobinRatingsPart' + str(i)
	cursor.execute("select * from " + str(table_name) +" where rating between "+ str(ratingMinValue) +" and "+ str(ratingMaxValue)+";")
	temp_data = cursor.fetchall()
	with open('RangeQueryOut.txt', 'a') as file:
	    for t in temp_data:
		row = 'RoundRobinRatingsPart' + str(i) +','+ str(t[0])+','+str(t[1])+','+ str(t[2])
		file.write("%s\n" %row)		
			
	
def PointQuery(ratingsTableName, ratingValue, openconnection):
   
    cursor = openconnection.cursor()

    cursor.execute ("select count(*) from RangeRatingsMetadata;")
    range_n = cursor.fetchone()[0]
    for i in range(range_n):
	table_name = 'RangeRatingsPart' + str(i)
	cursor.execute ("select MinRating, MaxRating  from RangeRatingsMetadata where PartitionNum = "+ str(i)+";" )	
	result = cursor.fetchone()
        min = result[0]		
        max = result[1]        
	if ( ratingValue <= max and ratingValue >= min ):
	    cursor.execute("select * from " + str(table_name) +" where rating = " + str(ratingValue)+";")
	    temp_data = cursor.fetchall()	    
	    with open('PointQueryOut.txt', 'a') as file:
                for t in temp_data:
                    row = 'RangeRatingsPart' + str(i) +','+ str(t[0])+','+str(t[1])+','+ str(t[2])
                    file.write("%s\n" %row)
	
    cursor.execute ("select PartitionNum from RoundRobinRatingsMetadata;")
    rr_n = cursor.fetchone()[0]    
    for i in range(rr_n):
	table_name =  'RoundRobinRatingsPart' + str(i)
	cursor.execute("select * from " + str(table_name) +" where rating = " + str(ratingValue) +";")
	temp_data = cursor.fetchall()
	with open('PointQueryOut.txt', 'a') as file:
	    for t in temp_data:
		row = 'RoundRobinRatingsPart' + str(i) +','+ str(t[0])+','+str(t[1])+','+ str(t[2])
		file.write("%s\n" %row)
			
	
	
	
