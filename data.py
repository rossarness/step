"""This file contains SQL helpers for data manipulation"""
import sqlite3 as sql
from urllib.request import pathname2url


def create_database():
    """This function will create db structure on empty DB file"""
    cursor = DBASE.cursor()
    cursor.execute("""PRAGMA foreign_keys = off;""")
    cursor.execute(
        """CREATE TABLE attributes (id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL, char_id INTEGER REFERENCES characters (id) ON DELETE NO ACTION, origin STRING, age INTEGER, height INTEGER, weight INTEGER, zw INTEGER, kon INTEGER, czj INTEGER, um INTEGER, dh INTEGER, inu INTEGER, zd_current INTEGER, lr_current INTEGER, cr_current INTEGER, kr_current INTEGER, um_current INTEGER, sr_current INTEGER, vis INTEGER, tired INTEGER);"""
    )
    cursor.execute(
        """CREATE TABLE character_items (id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL, char_id INTEGER REFERENCES characters (id), slot STRING, item_id INTEGER REFERENCES items (id));"""
    )
    cursor.execute(
        """CREATE TABLE characters (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE, name NOT NULL UNIQUE);"""
    )
    cursor.execute(
        """CREATE TABLE equipment (id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL, char_id INTEGER REFERENCES characters (id) ON DELETE SET NULL MATCH SIMPLE, item_name STRING NOT NULL);"""
    )
    cursor.execute(
        """CREATE TABLE items (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, item_name STRING NOT NULL, img_source STRING, item_type STRING, item_dmg STRING, item_description STRING, item_def INTEGER, sub_type STRING);"""
    )
    cursor.execute("""PRAGMA foreign_keys = on;""")
    DBASE.commit()


try:
    dburi = "file:{}?mode=rw".format(pathname2url("data.db"))
    DBASE = sql.connect(dburi, uri=True)
except sql.OperationalError:
    DBASE = sql.connect("data.db")
    print("DB not found creating new one")
    create_database()


def get_attribute(char, attribute):
    """This function return selected attribute for the character"""
    char_id = get_character_id(char)
    cursor = DBASE.cursor()
    cursor.execute(
        """SELECT """ + attribute + """ FROM attributes WHERE char_id=?""", (char_id,)
    )
    raw = cursor.fetchone()
    if raw[0] == None:
        raw = " "
        return raw
    else:
        return raw[0]


def save_attribute(char, attribute, value):
    """This function updates the character attribute in the db"""
    char_id = get_character_id(char)
    cursor = DBASE.cursor()
    cursor.execute(
        """UPDATE attributes SET """ + attribute + """=? WHERE char_id=?""",
        (value, char_id),
    )
    DBASE.commit()


def check_duplicate_character(char_name):
    """This function check if new character is not a duplicate
    raises error if duplicate is found"""
    cursor = DBASE.cursor()
    cursor.execute("""SELECT name FROM characters WHERE name=?""", (char_name,))
    raw = cursor.fetchone()
    if raw:
        raise NameError


def get_character_list():
    """Return the list of the characters from the database"""
    cursor = DBASE.cursor()
    cursor.execute("""SELECT name FROM characters;""")
    raw = cursor.fetchall()
    return formatresult(raw)


def get_character_id(char):
    cursor = DBASE.cursor()
    cursor.execute("""SELECT id FROM characters WHERE name=?""", (char,))
    raw = cursor.fetchone()
    return raw[0]


def delete_character(name):
    """Deletes character from database"""
    char_id = get_character_id(name)
    equipment = get_backpack_list(name)
    cursor = DBASE.cursor()
    cursor.execute("""DELETE FROM characters WHERE id=?""", (char_id,))
    cursor.execute("""DELETE FROM attributes WHERE char_id=?""", (char_id,))
    if equipment:
        cursor.execute("""DELETE FROM equipment WHERE char_id=?""", (char_id,))
    DBASE.commit()


def add_character(new_char):
    """Adds character to the database"""
    cursor = DBASE.cursor()
    cursor.execute("""INSERT INTO characters (name) VALUES (?)""", (new_char,))
    DBASE.commit()
    char_id = get_character_id(new_char)
    cursor.execute("""INSERT INTO attributes (char_id) VALUES (?)""", (char_id,))
    DBASE.commit()


def get_backpack_list(char):
    """Returns list of items that are bound to the character"""
    char_id = get_character_id(char)
    cursor = DBASE.cursor()
    cursor.execute("""SELECT item_name FROM equipment WHERE char_id=?""", (char_id,))
    raw = cursor.fetchall()
    return formatresult(raw)


def add_backpack_item(char, item):
    """Adds item to the database"""
    char_id = get_character_id(char)
    cursor = DBASE.cursor()
    cursor.execute(
        """INSERT INTO equipment (char_id, item_name) VALUES (?,?)""", (char_id, item)
    )
    DBASE.commit()


def delete_backpack_item(char, items):
    """Deletes items from the database"""
    char_id = get_character_id(char)
    cursor = DBASE.cursor()
    for item in items:
        cursor.execute(
            """DELETE FROM equipment WHERE id IN 
            (
                SELECT id FROM equipment WHERE char_id=? AND item_name=? LIMIT 1
            )""",
            (char_id, item),
        )
    DBASE.commit()


def add_equipment_item(name, image, item_type, statistic, description, stype):
    """Adds new item to list of available armor or weapon items to choose for character"""
    field = check_field(item_type)
    if field == "item_def":
        if statistic != "":
            statistic = int(statistic)
        else:
            statistic = 0
    elif field == "item_dmg":
        if statistic != "":
            statistic = str(statistic)
        else:
            statistic = "0"
    cursor = DBASE.cursor()
    if field != None:
        cursor.execute(
            """INSERT INTO items (item_name, img_source, item_type,
                          item_description, """
            + field
            + """, sub_type)
                          VALUES (?,?,?,?,?,?)""",
            (name, image, item_type, description, statistic, stype),
        )
    else:
        cursor.execute(
            """INSERT INTO items (item_name, img_source, item_type, item_description) 
                      VALUES (?,?,?,?)""",
            (name, image, item_type, description),
        )
    item_id = cursor.lastrowid
    DBASE.commit()
    return item_id


def get_equipment_list(item_type):
    """Returns all items for requested type"""
    cursor = DBASE.cursor()
    cursor.execute("""SELECT * from items WHERE item_type=?""", (item_type,))
    return cursor.fetchall()


def get_equipment_item(id):
    """Return item based on id"""
    cursor = DBASE.cursor()
    cursor.execute("""SELECT * from items WHERE id=?""", (id,))
    return cursor.fetchall()


def load_character_item(char_id, item_slot):
    """Returns item that is currently equipped"""
    cursor = DBASE.cursor()
    cursor.execute(
        """SELECT item_id from character_items WHERE char_id =? AND slot=?""",
        (char_id, item_slot),
    )
    result = cursor.fetchone()
    if result:
        result = result[0]
    return result


def save_character_item(char_id, item_id, item_slot):
    """Saves currently equiped items to db"""
    cursor = DBASE.cursor()
    current = load_character_item(char_id, item_slot)
    if current:
        cursor.execute(
            """UPDATE character_items SET item_id=? WHERE char_id=? AND slot=?""",
            (item_id, char_id, item_slot),
        )
    else:
        cursor.execute(
            """INSERT INTO character_items (char_id, slot, item_id)
            VALUES (?,?,?)""",
            (char_id, item_slot, item_id),
        )
    DBASE.commit()
    return True


def save_equipment_item(id, name, image, item_type, statistic, description, stype):
    """Saves changes done by edit menu"""
    cursor = DBASE.cursor()
    description = str(description)
    field = check_field(item_type)
    if field is not None:
        cursor.execute(
            """UPDATE items SET item_name=?, img_source=?, item_type=?,
                         """
            + field
            + """=?, item_description=?, sub_type=?
                         WHERE id=?""",
            (name, image, item_type, statistic, description, stype, id),
        )
    else:
        cursor.execute(
            """UPDATE items SET item_name=?, img_source=?, item_type=?,
                         item_description=?, sub_type=?
                         WHERE id=?""",
            (name, image, item_type, description, stype, id),
        )

    DBASE.commit()


# Helper functions


def formatresult(raw):
    """This function will format the result into pretty list"""
    result = []
    try:
        for row in raw:
            result.append(row[0])
    except IndexError:
        result = []
    return result


def closedb():
    """This functon closes db on app exit"""
    DBASE.close()


def check_field(item_type):
    """This function returns field type for db operations"""
    field = None
    if item_type in ["weapon"]:
        field = "item_dmg"
    elif item_type in ["hand", "boots", "helm", "chest"]:
        field = "item_def"
    elif item_type in ["cape"]:
        field = None
    return field
