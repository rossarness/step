'''This file contains SQL helpers for data manipulation'''
import sqlite3 as sql

DBASE = sql.connect('data/data.db')

def get_attribute(char, attribute):
    '''This function return selected attribute for the character'''
    char_id = get_character_id(char)
    cursor = DBASE.cursor()
    cursor.execute('''SELECT '''+ attribute +''' FROM attributes WHERE char_id=?''',(char_id,))
    raw = cursor.fetchone()
    if raw[0] == None:
        raw = " "
        return raw
    else:
        return raw[0]

def save_attribute(char, attribute, value):
    '''This function updates the character attribute in the db'''
    char_id = get_character_id(char)
    cursor = DBASE.cursor()
    cursor.execute('''UPDATE attributes SET '''+ attribute +'''=? WHERE char_id=?''',(value,char_id,))
    DBASE.commit()

def check_duplicate_character(char_name):
    '''This function check if new character is not a duplicate
    raises error if duplicate is found'''
    cursor = DBASE.cursor()
    cursor.execute('''SELECT name FROM characters WHERE name=?''',(char_name,))
    raw = cursor.fetchone()
    if raw:
        raise NameError

def get_character_list():
    '''Return the list of the characters from the database'''
    cursor = DBASE.cursor()
    cursor.execute('''SELECT name FROM characters;''')
    raw = cursor.fetchall()
    return formatresult(raw)

def get_character_id(char):
    cursor = DBASE.cursor()
    cursor.execute("""SELECT id FROM characters WHERE name=?""",(char,))
    raw = cursor.fetchone()
    return raw[0]


def delete_character(name):
    '''Deletes character from database'''
    char_id = get_character_id(name)
    equipment = get_backpack_list(name)
    cursor = DBASE.cursor()
    cursor.execute('''DELETE FROM characters WHERE id=?''', (char_id,))
    cursor.execute('''DELETE FROM attributes WHERE char_id=?''', (char_id,))
    if equipment:
        cursor.execute('''DELETE FROM equipment WHERE char_id=?''', (char_id,))
    DBASE.commit()

def add_character(new_char):
    '''Adds character to the database'''
    cursor = DBASE.cursor()
    cursor.execute("""INSERT INTO characters (name) VALUES (?)""",(new_char,))
    DBASE.commit()
    char_id = get_character_id(new_char)
    cursor.execute("""INSERT INTO attributes (char_id) VALUES (?)""",(char_id,))
    DBASE.commit()

def get_backpack_list(char):
    '''Returns list of items that are bound to the character'''
    char_id = get_character_id(char)
    cursor = DBASE.cursor()
    cursor.execute("""SELECT item_name FROM equipment WHERE char_id=?""", (char_id, ))
    raw = cursor.fetchall()
    return formatresult(raw)

def add_backpack_item(char, item):
    '''Adds item to the database'''
    char_id = get_character_id(char)
    cursor = DBASE.cursor()
    cursor.execute("""INSERT INTO equipment (char_id, item_name) VALUES (?,?)""",(char_id, item,) )
    DBASE.commit()

def delete_backpack_item(char, items):
    '''Deletes items from the database'''
    char_id = get_character_id(char)
    cursor = DBASE.cursor()
    for item in items:
        cursor.execute("""DELETE FROM equipment WHERE id IN 
            (
                SELECT id FROM equipment WHERE char_id=? AND item_name=? LIMIT 1
            )""", (char_id, item,))
    DBASE.commit()

def add_equipment_item(name, image, item_type):
    '''Adds new item to list of available armor or weapon items to choose for character'''
    cursor = DBASE.cursor()
    cursor.execute("""INSERT INTO items (item_name, img_source, item_type) VALUES (?,?,?)""", (name, image, item_type, ))
    DBASE.commit()

def get_equipment_list(item_type):
    '''Returns all items for requested type'''
    cursor = DBASE.cursor()
    cursor.execute("""SELECT * from items WHERE item_type=?""", (item_type, ))
    return cursor.fetchall()

#Helper functions   

def formatresult(raw):
    '''This function will format the result into pretty list'''
    result = []
    try:
        for row in raw:
            result.append(row[0])
    except IndexError:
        result = []
    return result

def closedb():
    '''This functon closes db on app exit'''
    DBASE.close()