from django.db import connection

def getSelectedDate():
    query1 = "SELECT currentDate as DATE FROM tblselecteddate;"

    with connection.cursor() as cursor:
        cursor.execute(query1)
        single_value = cursor.fetchone()
        data1= single_value[0] if single_value else None
    
    return data1

def getFromToDT():
    query2 = "SELECT fromDT as fDT, toDT as tDT FROM tbldtspan;"
    with connection.cursor() as cursor:
        cursor.execute(query2)
        single_value = cursor.fetchone()
        return single_value

def updateSelectedDate(from_date,to_date):
    query4 = f"UPDATE tblselecteddate SET currentDate = '{from_date}';"
    existing_from_dt, existing_to_dt = getFromToDT()
    if existing_from_dt and existing_to_dt:
        # Split the existing time from the output ('2023-07-13 00:00:01', '2023-07-13 23:59:59')
        existing_from_time = existing_from_dt.split()[1]
        existing_to_time = existing_to_dt.split()[1]

        # Combine the updated date with the existing time
        from_dt_tobeupdated = f"{from_date} {existing_from_time}"
        to_dt_tobeupdated = f"{to_date} {existing_to_time}"

        # Update the data in the database
        query5 = f"UPDATE tbldtspan SET fromDT = '{from_dt_tobeupdated}';"
        query6 = f"UPDATE tbldtspan SET toDT = '{to_dt_tobeupdated}';"

        with connection.cursor() as cursor:
            cursor.execute(query5)
            cursor.execute(query6)    

    with connection.cursor() as cursor:
        cursor.execute(query4)


def gettodate():
    existing_from_dt, existing_to_dt = getFromToDT()
    existing_to_date = existing_to_dt.split()[0]
    print(existing_to_date)
    return existing_to_date

def getSwitchStatus():
    query3 = "SELECT STATUS FROM tblhrsswitch;"
    with connection.cursor() as cursor:
        cursor.execute(query3)
        single_value = cursor.fetchone()
        data1= single_value[0] if single_value else None
        return data1

def toggleSwitchStatus(status):
    query7 = f"UPDATE tblhrsswitch SET STATUS = '{status}';"
    if status == "OFF":
        NEW_FROM_TIME = "00:00:01"
        NEW_TO_TIME = "23:59:59"
    else:        
        NEW_FROM_TIME = "09:30:00"
        NEW_TO_TIME = "19:00:00"
    
    existing_from_dt, existing_to_dt = getFromToDT()
    if existing_from_dt and existing_to_dt:
        # Split the existing time from the output ('2023-07-13 00:00:01', '2023-07-13 23:59:59')
        existing_from_date = existing_from_dt.split()[0]
        existing_to_date = existing_to_dt.split()[0]

        # Combine the updated date with the existing time
        from_tm_tobeupdated = f"{existing_from_date} {NEW_FROM_TIME}"
        to_tm_tobeupdated = f"{existing_to_date} {NEW_TO_TIME}"

        # Update the data in the database
        query8 = f"UPDATE tbldtspan SET fromDT = '{from_tm_tobeupdated}';"
        query9 = f"UPDATE tbldtspan SET toDT = '{to_tm_tobeupdated}';"

        with connection.cursor() as cursor:
            cursor.execute(query8)
            cursor.execute(query9)  
    
    with connection.cursor() as cursor:
        cursor.execute(query7)


def glanceShortcut():
    existing_from_dt, existing_to_dt = getFromToDT()
    existing_from_date = existing_from_dt.split()[0]
    existing_to_date = existing_to_dt.split()[0]
    print(existing_from_date,existing_to_date)
    time = getSwitchStatus()
    if time == "on":
        query13 = f"""       
        SELECT USERID,
        TIME_FORMAT(SEC_TO_TIME(SUM(TIME_TO_SEC(W_PROTIME))), '%H:%i:%s') AS total_protime,
        TIME_FORMAT(SEC_TO_TIME(SUM(TIME_TO_SEC(W_UNPROTIME))), '%H:%i:%s') AS total_unprotime,
        TIME_FORMAT(SEC_TO_TIME(SUM(TIME_TO_SEC(W_IDLETIME))), '%H:%i:%s') AS total_idletime,
        MIN(W_INTIME) AS min_intime,
        MAX(W_OUTTIME) AS max_outtime,
        SUM(W_PROCOUNT) AS total_procount,
        SUM(W_UNPROCOUNT) AS total_unprocount,
        SUM(W_IDLECOUNT) AS total_idlecount
        FROM newproworkingdetails_page1
        WHERE DATE BETWEEN '{existing_from_date}' AND '{existing_to_date}'
        GROUP BY USERID;
        """
        with connection.cursor() as cursor:
            cursor.execute(query13)
            results = cursor.fetchall()

        # print(results)
    else:
        query13 = f"""
        SELECT USERID,
        TIME_FORMAT(SEC_TO_TIME(SUM(TIME_TO_SEC(PROTIME))), '%H:%i:%s') AS total_protime,
        TIME_FORMAT(SEC_TO_TIME(SUM(TIME_TO_SEC(UNPROTIME))), '%H:%i:%s') AS total_unprotime,
        TIME_FORMAT(SEC_TO_TIME(SUM(TIME_TO_SEC(IDLETIME))), '%H:%i:%s') AS total_idletime,
        MIN(INTIME) AS min_intime,
        MAX(OUTTIME) AS max_outtime,
        SUM(PROCOUNT) AS total_procount,
        SUM(UNPROCOUNT) AS total_unprocount,
        SUM(IDLECOUNT) AS total_idlecount
        FROM newproworkingdetails_page1
        WHERE DATE BETWEEN '{existing_from_date}' AND '{existing_to_date}'
        GROUP BY USERID;
        """
        with connection.cursor() as cursor:
            cursor.execute(query13)
            results = cursor.fetchall()
            
        # print(results)
    return results

def onlyglanceShortcut(user):
    existing_from_dt, existing_to_dt = getFromToDT()
    existing_from_date = existing_from_dt.split()[0]
    existing_to_date = existing_to_dt.split()[0]
    time = getSwitchStatus()
    if time == "on":
        query13 = f"""
        SELECT USERID,
            TIME_FORMAT(SEC_TO_TIME(SUM(TIME_TO_SEC(W_PROTIME))), '%H:%i:%s') AS total_protime,
            TIME_FORMAT(SEC_TO_TIME(SUM(TIME_TO_SEC(W_UNPROTIME))), '%H:%i:%s') AS total_unprotime,
            TIME_FORMAT(SEC_TO_TIME(SUM(TIME_TO_SEC(W_IDLETIME))), '%H:%i:%s') AS total_idletime,
            MIN(W_INTIME) AS min_intime,
            MAX(W_OUTTIME) AS max_outtime,
            SUM(W_PROCOUNT) AS total_procount,
            SUM(W_UNPROCOUNT) AS total_unprocount,
            SUM(W_IDLECOUNT) AS total_idlecount,
            (SELECT IP FROM newproworkingdetails_page1 WHERE USERID = '{user}' AND DATE = '{existing_from_date}') AS ip,
            (SELECT IP_LOCATION FROM newproworkingdetails_page1 WHERE USERID = '{user}' AND DATE = '{existing_from_date}') AS ip_location
        FROM newproworkingdetails_page1
        WHERE USERID = '{user}' AND DATE BETWEEN '{existing_from_date}' AND '{existing_to_date}'
        GROUP BY USERID;
        """
        with connection.cursor() as cursor:
            cursor.execute(query13)
            results = cursor.fetchall()
    else:
        query13 = f"""
        SELECT USERID,
            TIME_FORMAT(SEC_TO_TIME(SUM(TIME_TO_SEC(PROTIME))), '%H:%i:%s') AS total_protime,
            TIME_FORMAT(SEC_TO_TIME(SUM(TIME_TO_SEC(UNPROTIME))), '%H:%i:%s') AS total_unprotime,
            TIME_FORMAT(SEC_TO_TIME(SUM(TIME_TO_SEC(IDLETIME))), '%H:%i:%s') AS total_idletime,
            MIN(INTIME) AS min_intime,
            MAX(OUTTIME) AS max_outtime,
            SUM(PROCOUNT) AS total_procount,
            SUM(UNPROCOUNT) AS total_unprocount,
            SUM(IDLECOUNT) AS total_idlecount,
            (SELECT IP FROM newproworkingdetails_page1 WHERE USERID = '{user}' AND DATE = '{existing_from_date}') AS ip,
            (SELECT IP_LOCATION FROM newproworkingdetails_page1 WHERE USERID = '{user}' AND DATE = '{existing_from_date}') AS ip_location
        FROM newproworkingdetails_page1
        WHERE USERID = '{user}' AND DATE BETWEEN '{existing_from_date}' AND '{existing_to_date}'
        GROUP BY USERID;
        """
        with connection.cursor() as cursor:
            cursor.execute(query13)
            results = cursor.fetchall()

    # print(results)
            

    return results


#page2
   
def alltables(user):
    existing_from_dt, existing_to_dt = getFromToDT()
    existing_from_date = existing_from_dt.split()[0]
    existing_to_date = existing_to_dt.split()[0]
    time = getSwitchStatus()

    if time == "on":
        query14 = f"""           
            SELECT TITLE, PROCESSNAME, PRO_TYPE, W_TIME_FOR_DAY, TASK_TYPE
            FROM newproworkingdetails_page2
            WHERE USERID = '{user}' AND DATE BETWEEN '{existing_from_date}' AND '{existing_to_date}'
            ORDER BY W_TIME_FOR_DAY DESC;
        """
        with connection.cursor() as cursor:
            cursor.execute(query14)
            data = cursor.fetchall()
    else:
        query14 = f"""
            SELECT TITLE, PROCESSNAME, PRO_TYPE, TIME_FOR_DAY, TASK_TYPE
            FROM newproworkingdetails_page2
            WHERE USERID = '{user}' AND DATE BETWEEN '{existing_from_date}' AND '{existing_to_date}'
            ORDER BY TIME_FOR_DAY DESC;
        """
        with connection.cursor() as cursor:
            cursor.execute(query14)
            data = cursor.fetchall()


    return data 





