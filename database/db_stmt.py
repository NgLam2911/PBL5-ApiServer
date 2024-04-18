# Datatype: SQLite3

def init_table():
    return """
    CREATE TABLE IF NOT EXISTS sensor_data (
        time INTEGER PRIMARY KEY NOT NULL,
        data TEXT NOT NULL
    )
    """
    
def insert_data(time: int, data: str):
    return f"""
    INSERT INTO sensor_data (time, data)
    VALUES ({time}, '{data}')
    """
    
def get_data(time, from_time, to_time):
    if time is not None:
        return f"""
        SELECT * FROM sensor_data
        WHERE time = {time}
        """
    if from_time is None and to_time is None:
        return """
        SELECT * FROM sensor_data
        """
    else:
        if from_time is None:
            return f"""
            SELECT * FROM sensor_data
            WHERE time <= {to_time}
            """
        else:
            if to_time is None:
                return f"""
                SELECT * FROM sensor_data
                WHERE time >= {from_time}
                """
            else:
                return f"""
                SELECT * FROM sensor_data
                WHERE time >= {from_time} AND time <= {to_time}
                """
                
def delete_data(time, from_time, to_time):
    if time is not None:
        return f"""
        DELETE FROM sensor_data
        WHERE time = {time}
        """
    if from_time is None and to_time is None:
        return """
        DELETE FROM sensor_data
        """
    else:
        if from_time is None:
            return f"""
            DELETE FROM sensor_data
            WHERE time <= {to_time}
            """
        else:
            if to_time is None:
                return f"""
                DELETE FROM sensor_data
                WHERE time >= {from_time}
                """
            else:
                return f"""
                DELETE FROM sensor_data
                WHERE time >= {from_time} AND time <= {to_time}
                """
                

                
    