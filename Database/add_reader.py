# Neither admin nor guest can touch
from operation import build_connection

conn = build_connection()

try:
    with conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO READER24331912 values
                ('510721M', 'Zhang Jie', 0, 0, 0.00),
                ('511523F', 'Fan Wei', 0, 0, 0.00),
                ('511524F', 'Yu Nengbin', 0, 0, 0.00),
                ('510923M', 'Guo Zhenghua', 0, 0, 0.00),
                ('710234F', 'Mary Wong', 0, 0, 0.00),
                ('710222M', 'Tom Lee', 0, 0, 0.00),
                ('511514M', 'Gong Yexiu', 0, 0, 0.00),
                ('511211M', 'Xie Jinpeng', 0, 0, 0.00) 
            """)
    print("successful")
except Exception as e:
    print("Error", e)

finally:
    conn.close()