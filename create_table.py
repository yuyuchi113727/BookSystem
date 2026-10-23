# Neither admin nor guest can touch
from operation import build_connection

conn = build_connection()

# 图书信息表
try:
    with conn:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS LIB24331912 (
                    title_id varchar(10) primary key,
                    title varchar(40),
                    edition tinyint check(edition >= 1),
                    year int,
                    author varchar(20),
                    price decimal(10, 2)
                );
            """)
    print("successful")
except Exception as e:
    print("Error:", e)

# 库存
try:
    with conn:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS CNT24331912 (
                    title_id varchar(10) primary key,
                    remains int not NULL check(remains >= 0),
                    borrowed int not NULL check(borrowed >= 0 and remains >= borrowed),
                    total_record int not NULL check(total_record >= 0)
                );
            """)
    print("successful")
except Exception as e:
    print("Error:", e)

#采购情况    
try:
    with conn:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS PIN24331912 (
                    title_id varchar(10),
                    number int not NULL check(number >= 0),
                    time TIMESTAMP
                );
            """)
    print("successful")
except Exception as e:
    print("Error:", e)
    
#淘汰情况
try:
    with conn:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS POUT24331912 (
                    title_id varchar(10),
                    number int not NULL check(number >= 0),
                    time TIMESTAMP
                );
            """)
    print("successful")
except Exception as e:
    print("Error:", e)

#借书情况    
try:
    with conn:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS BORROW24331912 (
                    reader_id varchar(10) not NULL,
                    title_id varchar(10) not NULL,
                    number int not NULL check(number >= 0),
                    time TIMESTAMP,
                    not_returned int not NULL check(not_returned >= 0 and not_returned <= number)
                )
            """)
    print("successful")
except Exception as e:
    print("Error:", e)

# 还书情况
try:
    with conn:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS RETURN24331912 (
                    reader_id varchar(10) not NULL,
                    title_id varchar(10) not NULL,
                    number int not NULL check(number >= 0),
                    time TIMESTAMP
                )
            """)
    print("successful")
except Exception as e:
    print("Error:", e)

# 读者信息
try:
    with conn:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS READER24331912 (
                    reader_id varchar(10) primary key,
                    reader_name varchar(20) not NULL,
                    total_record int not NULL check(total_record >= 0),
                    not_returned int not NULL check(not_returned >= 0 and not_returned <= 20),
                    fine decimal(10, 2)
                )
            """)
    print("successful")
except Exception as e:
    print("Error:", e)

finally:
    conn.close()