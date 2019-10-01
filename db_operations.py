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


def get_person_by_id(person_id):
    sql_query = """
    Select  Person_Id, Person_First_Name, Person_Last_Name,
            Drink_Id, Drink_Name, Drink_Instructions
    From    tb_People p
    Join    tb_Preferences pr
        On  Person_Id = Pref_Person
    Join    tb_Drinks d
        On  Drink_Id = Pref_Drink
    Where   Person_Id = %s
    """

    parameters = (person_id)
    row = db_return_rows(sql, parameters)[0]

    return Person(
        row["Person_Id"],
        row["Person_First_Name"],
        row["Person_Last_Name"],
        Drink(
            row["Drink_Id"],
            row["Drink_Name"],
            row["Drink_Instructions"]
        )
    )
    

def get_drink_by_id(drink_id):
    sql_query = """
    Select  Drink_Id, Drink_Name, Drink_Instructions
    From    tb_Drinks
    Where   Drink_Id = %s
    """

    parameters = (drink_id)
    row = db_return_rows(sql_query, parameters)[0]

    return Drink(
        row["Drink_Id"],
        row["Drink_Name"],
        row["Drink_Instructions"]
    )
    

def get_round_by_id(round_id):
    sql_query = """
    Select  Round_Id, Round_Active, Round_StartTimeUTC, Round_Initiator
    From    tb_Rounds
    Where   Round_Id = %s
    """
    parameters = (round_id)
    
    #should only return one row
    round_db_row = db_return_rows(sql_query, parameters)
    round_to_return = None

    for row in round_db_row:
        round_to_return = Round(
            row["Round_Id"], 
            row["Round_Active"], 
            row["Round_StartTimeUTC"],
            row["Round_Initiator"]
        )

    return round_to_return 


def get_round_order_by_id(order_id):
    sql_query = """
    Select  ROrder_Id, ROrder_Round_Id,
            Person_Id, Person_First_Name, Person_Last_Name,
            Drink_id, Drink_Name, Drink_Instructions
    From    tb_Round_Orders ro
    Join    tb_People p On p.Person_Id = ro.ROrder_Person
    Join    tb_Drinks d On d.Drink_Id = ro.ROrder_Drink
    Where   ROrder_Round_Id = %s
    """
    
    parameters = (round_id)
    row = db_return_rows(sql_query, parameters)[0]

    return {
        "id": row["ROrder_Id"],
        "round_id": row["ROrder_Round_Id"],
        "person": Person(
            row["Person_Id"],
            row["Person_First_Name"],
            row["Person_Last_Name"]
        ),
        "drink": Drink(
            row["Drink_Id"],
            row["Drink_Name"],
            row["Drink_Instructions"]
        )
    }

def get_people():
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


def get_drinks():
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


def get_rounds():
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


def get_round_orders(round_id):
    sql = """
    Select  ROrder_Id, Person_Id, Person_First_Name, Person_Last_Name, Drink_Id, Drink_Name, Drink_Instructions
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
        
        round_orders.append({
            "id": row["ROrder_Id"],
            "person": person,
            "drink": drink}
        )

    return round_orders


def insert_round_order(round_id, person_id, drink_id):
    sql_insert_command = """
    Insert Into tb_Round_Orders (ROrder_Round_Id, ROrder_Person, ROrder_Drink)
    Values (%s, %s, %s)
    """
    parameters = (round_id, person_id, drink_id)
    return db_insert_and_return_id(sql_insert_command, parameters)


def insert_person(first_name, last_name):
    sql_insert_command = """
    Insert Into tb_People (Person_First_Name, Person_Last_Name)
    Values (%s, %s);
    """

    parameters = (first_name, last_name)
    return db_insert_and_return_id(sql_insert_command, parameters)


def insert_person_drinks_pref(person_id, drink_id):
    sql_insert_command = """
    Insert Into tb_Preferences (Pref_Person, Pref_Drink)
    values (%s, %s);
    """

    parameters = (person_id, drink_id)
    return db_insert_and_return_id(sql_insert_command, parameters)


def insert_drink(name, instructions):
    sql_insert_command = """
    Insert Into tb_Drinks (Drink_Name, Drink_Instructions)
    values (%s, %s)
    """

    parameters = (name, instructions)
    return db_insert_and_return_id(sql_insert_command, parameters)


def insert_round(round_active, round_start_time_utc, round_initiator):
    sql_save_command  = """
    insert into tb_Rounds (Round_Active, Round_StartTimeUTC, Round_Initiator)
    values (%s, %s, %s)
    """
    
    parameters = (round_active, round_start_time_utc, round_initiator)
    return db_insert_and_return_id(sql_save_command, parameters)


def update_round_order(order_id, person_id, drink_id):
    sql_update_command = """
    update  tb_Round_Orders
    Set     ROrder_Person = %s,
            ROrder_Drink = %s
    Where   ROrder_Id = %s
    """
    parameters = (person_id, drink_id, order_id)
    db_insert_or_update_record(sql_update_command, parameters)


def update_person(person_id, first_name, last_name):
    sql_update_command = """
    Update  tb_people
    Set     Person_First_Name = %s,
            Person_Last_Name = %s
    From    Person_Id = %s
    """
    parameters = (first_name, last_name, person_id)
    db_insert_or_update_record(sql_update_command, parameters)


def update_drink(drink_id, name, instructions):
    sql_update_command = """
    Update  tb_Drinks
    Set     Drink_Name = %s,
            Drink_Instructions = %s
    Where   Drink_Id = %s
    """

    parameters = (name, instructions, drink_id)
    db_insert_or_update_record(sql_update_command, parameters)


def update_round(round_id, round_active, round_start_time_utc, round_initator):
    sql_update_command = """
    Update  tb_Rounds
    Set     Round_Active = %s,
            Round_StartTimeUTC = %s,
            Round_Initiator = %s
    Where   Round_Id = %s
    """
    
    parameters = (round_active, round_start_time_utc, round_initator, round_id)
    db_insert_or_update_record(sql_update_command, parameters)


def delete_round_order(order_id):
    sql_delete_commmand = """
    Delete From tb_Round_Orders
    Where ROrder_Id = %s
    """
    parameters = (order_id)
    db_insert_or_update_record(sql_delete_commmand, parameters)


def delete_person(person_id):
    sql_delete_commmand = """
    Delete From tb_People
    Where Person_Id = %s
    """

    parameters = (person_id)
    db_insert_or_update_record(sql_delete_commmand, parameters)


def delete_drink(drink_id):
    sql_delete_commmand = """
    Delete From tb_Drinks
    Where Drink_Id = %s
    """

    parameters = (drink_id)
    db_insert_or_update_record(sql_delete_commmand, parameters)


def delete_round(round_id):
    sql_delete_commmand = """
    Delete From tb_Rounds
    Where Round_Id = %s
    """

    parameters = (round_id)
    db_insert_or_update_record(sql_delete_commmand, parameters)
