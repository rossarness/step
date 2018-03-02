'''This file contains SQL helpers for data manipulation'''
import sqlite3 as sql

DBASE = sql.connect('data/data.db')

def get_character_list():
    '''Return the list of the characters from the database'''
    cursor = DBASE.cursor()
    cursor.execute('''SELECT name FROM characters;''')
    raw = cursor.fetchall()
    return formatresult(raw)

def formatresult(raw):
    '''This function will format the result into pretty list'''
    result = []
    result.append(raw[0])
    result = []
    for row in raw:
        result.append(row[0])
    return result

def closedb():
    '''This functon closes db on app exit'''
    DBASE.close()