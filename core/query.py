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
        NEW_FROM_TIME = "09:30:00"
        NEW_TO_TIME = "19:00:00"
    else:
        NEW_FROM_TIME = "00:00:01"
        NEW_TO_TIME = "23:59:59"
    
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

    

def convertCountToTime(time_count):
		time_sec = time_count * 10
		time_h_mod = int(time_sec // 3600)
		time_m_mod = int((time_sec - (time_h_mod * 3600)) // 60)
		time_s_mod = int(time_sec - (time_h_mod * 3600) - (time_m_mod * 60))

		if time_h_mod < 10:
			time_h_mod = "0" + str(time_h_mod)
		if time_m_mod < 10:
			time_m_mod = "0" + str(time_m_mod)
		if time_s_mod < 10:
			time_s_mod = "0" + str(time_s_mod)

		return f"{time_h_mod}:{time_m_mod}:{time_s_mod} (H)"

def log_values():
    existing_from_dt, existing_to_dt = getFromToDT()

    query11 = f"""SELECT USER_ID , MIN(SYNC_TIME) as LOGIN, MAX(SYNC_TIME) as LOGOUT FROM tblproworkingdetails WHERE SYNC_TIME>'{existing_from_dt}' AND SYNC_TIME<'{existing_to_dt}' GROUP BY USER_ID; """

    with connection.cursor() as cursor:
        cursor.execute(query11)
        results2=cursor.fetchall()

    
    formatted_results = []

    for user_id, login, logout in results2:
        formatted_results.append((user_id ,login.strftime('%H:%M:%S'), logout.strftime('%H:%M:%S')))
    

    return formatted_results

def getGlanceValues():
    cnt=0
    existing_from_dt, existing_to_dt = getFromToDT()
    logg_values = log_values()
    query10 = f"""
        SELECT USER_ID , RES1 , COUNT(*) as cnt FROM tblproworkingdetails WHERE SYNC_TIME>'{existing_from_dt}' AND SYNC_TIME<'{existing_to_dt}' GROUP BY USER_ID ,RES1 ;
    """

    with connection.cursor() as cursor:
        cursor.execute(query10)
        results = cursor.fetchall()
                
    user_counts = {}

    for name,status,count in results:
        if name not in user_counts:
            user_counts[name]={'id':'','Idle':0,'PRO':0,"UNPRO":0, 'login': '', 'logout': '','PIdle':0,'PPRO':0,'PUNPRO':0}
        user_counts[name][status]=count

    for name,counts in user_counts.items():
        counts['PIdle'] = convertCountToTime(counts['Idle'])
        counts['PPRO'] = convertCountToTime(counts['PRO'])
        counts['PUNPRO'] = convertCountToTime(counts['UNPRO'])

    for name , login ,logout in logg_values:
        if name in user_counts:
            user_counts[name]['login'] = login
            user_counts[name]['logout'] = logout
            user_counts[name]['id'] = name

    return user_counts


def rdpSessions(user):
 
    existing_from_dt, existing_to_dt = getFromToDT()
    
    query10 = f"""
        SELECT 
            PROCESS_TITLE AS title,
            PROCESS_NAME AS rdpProcessName,
            COUNT(*) AS rdpUsage
        FROM 
            tblproworkingdetails
        WHERE 
            USER_ID = '{user}'
            AND SYNC_TIME > '{existing_from_dt}'
            AND SYNC_TIME < '{existing_to_dt}'
            AND PROCESS_NAME LIKE '%mstsc%'
            AND PROCESS_TITLE <> ''
            AND PROCESS_TITLE <> 'Remote Desktop Connection'
        GROUP BY 
            PROCESS_TITLE, PROCESS_NAME
        ORDER BY 
            rdpUsage ASC;
    """

    with connection.cursor() as cursor:
        cursor.execute(query10)
        single_value = cursor.fetchall()

        return single_value 
    

def browsingSessions(user):
 
    existing_from_dt, existing_to_dt = getFromToDT()
    
    query11 = f"""
    SELECT PROCESS_TITLE as title,
                GROUP_CONCAT(DISTINCT PROCESS_NAME ORDER BY PROCESS_NAME ASC) as browsingProcessName,
                COUNT(*) as browsingUsage
        FROM tblproworkingdetails
        WHERE USER_ID = '{user}'
        AND SYNC_TIME > '{existing_from_dt}'
        AND SYNC_TIME < '{existing_to_dt}'
        AND PRO_TYPE = 'BROWSING'
        AND PROCESS_TITLE <> ''
        GROUP BY PROCESS_TITLE
        ORDER BY browsingUsage ASC;
    """

    with connection.cursor() as cursor:
        cursor.execute(query11)
        single_value = cursor.fetchall()

    return single_value

def processSessions(user):
 
    existing_from_dt, existing_to_dt = getFromToDT()
    
    query12 = f"""
        SELECT PROCESS_TITLE as title,
                    GROUP_CONCAT(DISTINCT PROCESS_NAME ORDER BY PROCESS_NAME ASC) as ProcessName,
                    COUNT(*) as timeUsage,
                    GROUP_CONCAT(DISTINCT RES1 ORDER BY RES1 ASC) as taskType
            FROM tblproworkingdetails
            WHERE USER_ID = '{user}'
            AND SYNC_TIME > '{existing_from_dt}'
            AND SYNC_TIME < '{existing_to_dt}'
            GROUP BY PROCESS_TITLE
            ORDER BY timeUsage ASC;

    """

    with connection.cursor() as cursor:
        cursor.execute(query12)
        single_value = cursor.fetchall()

    return single_value



