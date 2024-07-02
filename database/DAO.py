from database.DB_connect import DBConnect
from model.state import State


class DAO():
    def __init__(self):
        pass
    @staticmethod
    def getAllYears():
        conn = DBConnect.get_connection()
        result=[]
        cursor = conn.cursor(dictionary=True)
        query="""select distinct(year(s.`datetime`)) as anno from sighting s order by s.`datetime` """
        cursor.execute(query)
        for row in cursor:
            result.append(row["anno"])
        cursor.close()
        conn.close()
        return result
    @staticmethod
    def getAllShapes():
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """select distinct(shape) from sighting s where s.shape!="" """
        cursor.execute(query)
        for row in cursor:
            result.append(row["shape"])
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllStates():
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """select * from state s"""
        cursor.execute(query)
        for row in cursor:
            result.append(State(**row))
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllWeightedNeigh(anno, shape):
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """select n.state1 as s1,n.state2 as s2, count(*) as N
                    from neighbor n, sighting s 
                    where year(s.`datetime`)=%s
                    and s.shape=%s
                    and (s.state=n.state1 or s.state=n.state2)
                    and n.state1 <n.state2 
                    group by n.state1,n.state2"""
        cursor.execute(query,(anno, shape))
        for row in cursor:
            result.append((row["s1"],row["s2"],row["N"]))
        cursor.close()
        conn.close()
        return result


