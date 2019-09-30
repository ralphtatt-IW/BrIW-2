import pymysql
from data_config import *
from classes import *
from classes import Round

def db_return_rows(query, parameters=None):
    con = get_sql_connection()
    try:
        with con.cursor() as cursor:
            if parameters is None:
                cursor.execute(query)
            else:
                cursor.execute(query, parameters)
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
    Select  Round_Id, Round_Active, Round_StartTimeUTC, Round_Initiator
    From    tb_Rounds r
    Order By Round_Id
    """
    round_db_rows = db_return_rows(sql)
    round_list = []

    for row in round_db_rows:
        round_list.append(Round(
                row["Round_Id"], 
                row["Round_Active"], 
                row["Round_StartTimeUTC"], 
                row["Round_Initiator"]
            )
        )

    return round_list


def get_round_from_db_by_id(round_id):
    sql = """
    Select  Round_Id, Round_Active, Round_StartTimeUTC, Round_Initiator
    From    tb_Rounds
    Where   Round_Id = %s
    """
    parameters = (round_id)
    
    #should only return one row
    round_db_row = db_return_rows(sql, parameters)
    round_to_return = None

    for row in round_db_row:
        round_to_return = Round(
            row["Round_Id"], 
            row["Round_Active"], 
            row["Round_StartTimeUTC"],
            row["Round_Initiator"]
        )

    return round_to_return
    


def get_round_orders_from_db(round_id):
    sql = """
    Select  Person_Id, Person_First_Name, Person_Last_Name, Drink_Id, Drink_Name, Drink_Instructions
    From    tb_Round_Orders ro
    Join    tb_People p on p.Person_Id = ro.ROrder_Person
    Join    tb_Drinks d on d.Drink_Id = ro.ROrder_Drink
    Where   ROrder_Round_Id = %s
    """
    
    round_orders_db_rows = db_return_rows(sql, (round_id))
    round_orders = []

    for row in round_orders_db_rows:
        person = Person(
            row["Person_Id"],
            row["Person_First_Name"],
            row["Person_Last_Name"]
        )

        drink = Drink(
            row["Drink_Id"],
            row["Drink_Name"],
            row["Drink_Instructions"]
        )
        
        round_orders.append([person, drink])

    return round_orders

def add_order_to_db(round_id, person_id, drink_id):
        sql_insert_command = """
        Insert Into tb_Round_Orders (ROrder_Round_Id, ROrder_Person, ROrder_Drink)
        Values (%s, %s, %s)
        """
        parameters = (round_id, person_id, drink_id)
        db_insert_or_update_record(sql_insert_command, parameters)


