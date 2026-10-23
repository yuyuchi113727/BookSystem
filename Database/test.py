from operation import build_connection

conn = build_connection()

"""
try:
    with conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM PIN24331912;")
            rows = cur.fetchall()
            for row in rows:
                title_id, num, ts = row
                # 把datetime对象转为字符串：'2020-01-01 00:00:00'
                ts_str = ts.strftime("%Y-%m-%d %H:%M:%S")
                print(f"title_id:{title_id}, number:{num}, time:{ts_str}")
    print("Data retrieved successfully.")
except Exception as e:
    print("Error retrieving data:", e)
finally:
    conn.close()
"""

"""
try:
    with conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM POUT24331912;")
    print("Data delete successfully.")
except Exception as e:
    print("Error retrieving data:", e)
finally:
    conn.close()
"""

"""
try:
    with conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM BORROW24331912 where time = '2026-09-18 18:00:00';")
            rows = cur.fetchall()
            for row in rows:
                print(row)
    print("Data retrieved successfully.")
except Exception as e:
    print("Error retrieving data:", e)
finally:
    conn.close()
"""

"""
try:
    with conn:
        with conn.cursor() as cur:
            cur.execute("update READER24331912 set fine = 0 where reader_id = '340000M'")
    print("update data successfully.")
except Exception as e:
    print("Error drop table:", e)
finally:
    conn.close()
"""