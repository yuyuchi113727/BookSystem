# Neither admin nor guest can touch
from operation import build_connection

conn = build_connection()

try:
    with conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO LIB24331912 values
                ('D1001', 'Dynamic Equations for Weather Forecast', 3, 2023, 'Liu Lei', 34.80),
                ('B2003', 'Introduction to Linux', 4, 2015, 'Zhang Chi', 25.90),        
                ('B2005', 'Cheatsheet for Windows', 4, 2013, 'Zhang Chi', 26.70),
                ('A3001', 'Math Analysis', 4, 2020, 'Cheng Yi', 33.30),
                ('A2007', 'Linear Algebra', 3, 2021, 'Chen Falai', 32.80),
                ('A2003', 'Build a Math Model from Zero', 7, 2024, 'Cheng Yuchen', 19.90),
                ('C1003', 'Deep Learning', 2, 2023, 'Li Bin', 40.50),
                ('C2004', 'Excellent Papers of AI', 1, 2025, 'Guo Yida', 20.70),
                ('D3008', 'Comments on Models for Weather Forecast', 2, 2026, 'Yu Yuchi', 23.40),
                ('E1001', 'Advice for Green Hands in Lab', 1, 2026, 'Yu Yuchi', 13.80),
                ('E1003', '1000 Exercises of Electric Circuit', 4, 2025, 'Gao Yuan', 22.50),
                ('F1004', 'The Futures of China', 1, 2025, 'Yu Yuchi', 34.20)        
            """)
    print("successful")
except Exception as e:
    print("Error", e)

finally:
    conn.close()