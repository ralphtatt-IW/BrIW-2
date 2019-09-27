import pymysql
from data_config import *
from classes import *

def db_return_rows(query):
    con = get_sql_connection()
    try:
        with con.cursor() as cursor:
            cursor.execute(query)
            return cursor.fetchall()
    except Exception as e:
        print(f"Error occured: {e}")
    finally:
        con.close()


def db_insert_or_update_record(command, parameters):
    con = get_sql_connection()
    try:
        with con.cursor() as cursor:
            cursor.execute(command, parameters)
            con.commit()
    except Exception as e:
        print(f"Error occured: {e}")
    finally:
        con.close()

def db_insert_and_return_id(command, parameters):
    con = get_sql_connection()
    try:
        with con.cursor() as cursor:
            cursor.execute(command, parameters)
            inserted_id = cursor.lastrowid
            con.commit()
            return inserted_id
    except Exception as e:
        print(f"Error occured: {e}")
    finally:
        con.close()


def get_people_from_db():
    sql = """
    Select  Person_Id, 
            Person_First_Name, 
            Person_Last_Name, 
            Drink_Id, 
            Drink_Name, 
            Drink_Instructions
    From    tb_People p 
    Left Outer Join tb_Preferences pf on pf.Pref_Person = p.Person_Id 
    Left Outer Join tb_Drinks d on d.Drink_Id = pf.Pref_Drink 
    Order By Person_Id
    """
    people_db_rows = db_return_rows(sql)
    people_list = []

    for row in people_db_rows:
        fav_drink = Drink(row["Drink_Id"], row["Drink_Name"], row["Drink_Instructions"]) if row["Drink_Id"] is not None else None
        person = Person(row["Person_Id"], row["Person_First_Name"], row["Person_Last_Name"], fav_drink)
        people_list.append(person)

    return people_list


def get_drinks_from_db():
    sql = """
    Select Drink_Id, Drink_Name, Drink_Instructions
    From tb_Drinks 
    Order By Drink_Id
    """
    drink_db_rows = db_return_rows(sql)
    drinks_list = []

    for row in drink_db_rows:
        drinks_list.append(Drink(row["Drink_Id"], row["Drink_Name"], row["Drink_Instructions"]))

    return drinks_list


def get_rounds_from_db():
    sql = """
    Select Round_Id, Round_Active, Round_StartTimeUTC, Round_Initiator 
    From tb_Rounds 
    Order By Round_Id
    """
    round_db_rows = db_return_rows(sql)
    round_list = []

    print(round_db_rows)
    for row in round_db_rows:
        round_list.append(
            Round(
                row["Round_Id"], 
                row["Round_Active"], 
                row["Round_StartTimeUTC"], 
                row["Round_Initiator"]
            )
        )

    return round_list


def get_round_orders():
    sql = """
    Select 

    """
