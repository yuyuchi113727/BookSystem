import psycopg2
from datetime import datetime, timedelta
from math import ceil
from collections import deque
from decimal import Decimal

def build_connection():
    hosts = ["202.38.88.80", "192.168.109.218"]
    for host in hosts:
        try:
            return psycopg2.connect(
                host=host,
                port=5432,
                dbname="student",
                user="student",
                password="Student123",
                sslmode="disable",
                connect_timeout=3
            )
        except psycopg2.OperationalError:
            continue
    return None

def reset_soft():
    conn = build_connection()
    
    flag = True
    msg = "Reset borrow/return record successfully!"
    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute("update CNT24331912 set borrowed = 0")
                cur.execute("delete from BORROW24331912")
                cur.execute("delete from RETURN24331912")
                cur.execute("update READER24331912 set total_record= 0, not_returned = 0, fine = 0.00")
    except Exception as e:
        flag = False
        msg = str(e)
        
    return flag, msg
                
def reset_heavy():
    conn = build_connection()
    
    flag = True
    msg = "Reset all system successfully!"
    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute("delete from LIB24331912")
                cur.execute("delete from CNT24331912")
                cur.execute("delete from PIN24331912")
                cur.execute("delete from POUT24331912")
                cur.execute("delete from BORROW24331912")
                cur.execute("delete from RETURN24331912")
                cur.execute("delete from READER24331912")
    except Exception as e:
        flag = False
        msg = str(e)
        
    return flag, msg

def check_format(num_str, time_str):
    flag = True
    msg = ""
    
    try:
        number = int(num_str)
        if number < 0:
            flag = False
            msg = "number must >= 0"
            return flag, msg
    except ValueError:
        flag = False
        msg = "number must be integer"
        return flag, msg
    
    try:
        datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S")
    except (ValueError, TypeError):
        flag = False
        msg = "invalid time format"
    
    return flag, msg
    

def check_book_exists(title_id):
    conn = build_connection()
    
    flag = True
    msg = ""
    
    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute("select 1 from LIB24331912 where title_id = %s", (title_id, ))
                res = cur.fetchone()
                if res is None:
                    flag = False
                    msg = f"Title_id {title_id} does not exist in database. Please add it first."
    except Exception as e:
        flag = False
        msg = str(e)
    
    finally:
        conn.close()
    
    return flag, msg

def check_reader_exists(reader_id):
    conn = build_connection()
    
    flag = True
    msg = ""
    
    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute("select 1 from READER24331912 where reader_id = %s", (reader_id, ))
                res = cur.fetchone()
                if res is None:
                    flag = False
                    msg = f"Reader_id {reader_id} does not exist in database. Plaese add it first."
    except Exception as e:
        flag = False
        msg = str(e)
        
    finally:
        conn.close()
        
    return flag, msg

def check_limit(reader_id):
    conn = build_connection()
    
    flag = True
    msg = ""
    
    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute("select not_returned, fine from READER24331912 where reader_id = %s", (reader_id, ))
                res = cur.fetchone()
                if res[0] > 20:
                    flag = False
                    msg = "Exceed the limitation of books not returned."
                elif res[1] > 0.0:
                    flag = False
                    msg = "You have fines record. Please deal with that before borrowing any book."
    except Exception as e:
        flag = False
        msg = str(e)
        
    finally:
        conn.close()
        
    return flag, msg

def register_book(title_id, title, edition, year, author, price, stack):
    conn = build_connection()
    
    flag = True
    msg = "Register new book successfully!"
    operation_count = 0
    
    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute("select 1 from LIB24331912 where title_id = %s", (title_id, ))
                res = cur.fetchone()
                if res is not None:
                    flag = False
                    msg = f"Title_id {title_id} already exists in database!"
                else:
                    sql = "insert into LIB24331912 values(%s, %s, %s, %s, %s, %s)"
                    cur.execute(sql, (title_id, title, edition, year, author, price)),
                    stack.append(("insert", "LIB24331912", {"title_id": title_id}, True))
                    operation_count += 1
                    
    except Exception as e:
        flag = False
        msg = str(e)
        for _ in range(operation_count):
            stack.pop()
        
    finally:
        conn.close()
        
    return flag, msg, stack

def register_reader(reader_id, reader_name, stack):
    conn = build_connection()
    
    flag = True
    msg = "Register new reader successfully!"
    operation_count = 0
    
    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute("select 1 from READER24331912 where reader_id = %s", (reader_id, ))
                res = cur.fetchone()
                if res is not None:
                    flag = False
                    msg = f"Reader_id {reader_id} already exists in database!"
                else:
                    sql = "insert into READER24331912 values(%s, %s, 0, 0, 0.0)"
                    cur.execute(sql, (reader_id, reader_name))
                    stack.append(("insert", "READER24331912", {"reader_id": reader_id}, True))
                    operation_count += 1
    except Exception as e:
        flag = False
        msg = str(e)
        for _ in range(operation_count):
            stack.pop()
    
    finally:
        conn.close()
        
    return flag, msg, stack

def purchase_book(title_id, delta_remains, time, stack):
    conn = build_connection()
    
    flag = True
    msg = "Insert purchase record successfully!"
    operation_count = 0
    
    try:
        with conn:
            with conn.cursor() as cur:
                sql = "insert into PIN24331912 values(%s, %s, %s)"
                cur.execute(sql, (title_id, delta_remains, time))
                stack.append(("insert", "PIN24331912", {"title_id": title_id, "time": time}, False))
                operation_count += 1
                
                cur.execute("select 1 from CNT24331912 where title_id = %s", (title_id, ))
                res = cur.fetchone()
                if res:
                    cur.execute("select remains from CNT24331912 where title_id = %s", (title_id, ))
                    old_value = cur.fetchone()[0]
                    
                    cur.execute("update CNT24331912 set remains = remains + %s WHERE title_id = %s", (delta_remains, title_id))
                    stack.append(("update", "CNT24331912", {"title_id": title_id}, "remains", old_value, True))
                    operation_count += 1
                else:
                    cur.execute("insert into CNT24331912 values(%s, %s, 0, 0)", (title_id, delta_remains))
                    stack.append(("insert", "CNT24331912", {"title_id": title_id}, True))
                    operation_count += 1
    except Exception as e:
        flag = False
        msg = str(e)
        for _ in range(operation_count):
            stack.pop()
    finally:
        conn.close()
        
    return flag, msg, stack

def check_remains(title_id, delta):
    conn = build_connection()
    
    flag = True
    msg = ""
    
    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute("select remains, borrowed from CNT24331912 where title_id = %s", (title_id, ))
                res = cur.fetchone()
                if res is None:
                    flag = False
                    msg = f"Title_id {title_id} is does not exist in bookstore, please check it again."
                else:
                    remains, borrowed = res[0], res[1]
                    if remains - borrowed < delta:
                        flag = False
                        msg = "There are not enough books to operate now."
    except Exception as e:
        flag = False
        msg = str(e)
    
    finally:
        conn.close()
        
    return flag, msg

def delete_book(title_id, delta_remains, time, stack):
    conn = build_connection()
    
    flag = True
    msg = "Insert abandon record successfully!"
    operation_count = 0
    
    try:
        with conn:
            with conn.cursor() as cur:
                sql = "insert into POUT24331912 values(%s, %s, %s)"
                cur.execute(sql, (title_id, delta_remains, time))
                stack.append(("insert", "POUT24331912", {"title_id": title_id, "time": time}, False))
                operation_count += 1
                
                cur.execute("select remains from CNT24331912 where title_id = %s", (title_id, ))
                old_value = cur.fetchone()[0]
                sql = "update CNT24331912 set remains = remains - %s where title_id = %s"
                cur.execute(sql, (delta_remains, title_id))
                stack.append(("update", "CNT24331912", {"title_id": title_id}, "remains", old_value, True))
                operation_count += 1 
                      
                cur.execute("select remains from CNT24331912 where title_id = %s", (title_id, ))
                res = cur.fetchone()
                if res[0] <= 0:
                    temp_op = stack.pop()
                    temp_op = temp_op[:-1] + (False, )
                    stack.append(temp_op)
                    cur.execute("select total_record from CNT24331912 where title_id = %s", (title_id, ))
                    total_record = cur.fetchone()[0]
                    
                    cur.execute("delete from CNT24331912 where title_id = %s", (title_id, ))
                    stack.append(("delete", "CNT24331912", {"title_id": title_id, "remains": 0, "borrowed": 0, "total_record": total_record}, True))
                    operation_count += 1
                    
    except Exception as e:
        flag = False
        msg = str(e)
        for _ in range(operation_count):
            stack.pop()
        
    finally:
        conn.close()
        
    return flag, msg, stack

def borrow_book(reader_id, title_id, delta_borrowed, time, stack):
    conn = build_connection()
    
    flag = True
    msg = "Insert borrow record successfully!"
    operation_count = 0
    
    try:
        with conn:
            with conn.cursor() as cur:
                sql = "insert into BORROW24331912 values(%s, %s, %s, %s, %s)"
                cur.execute(sql, (reader_id, title_id, delta_borrowed, time, delta_borrowed))
                stack.append(("insert", "BORROW24331912", {"reader_id": reader_id, "title_id": title_id, "time":time}, False))
                operation_count += 1
                
                cur.execute("select borrowed, total_record from CNT24331912 where title_id = %s", (title_id, ))
                res = cur.fetchone()
                old_borrowed, old_book_record = res[0], res[1]
                
                sql = "update CNT24331912 set borrowed = borrowed + %s, total_record = total_record + %s where title_id = %s"
                cur.execute(sql, (delta_borrowed, delta_borrowed, title_id))
                stack.append(("update", "CNT24331912", {"title_id": title_id}, "borrowed", old_borrowed, False))
                operation_count += 1
                stack.append(("update", "CNT24331912", {"title_id": title_id}, "total_record", old_book_record, False))
                operation_count += 1
                
                cur.execute("select total_record, not_returned from READER24331912 where reader_id = %s", (reader_id, ))
                res = cur.fetchone()
                old_reader_record, old_not_returned = res[0], res[1]
                
                sql = "update READER24331912 set total_record = total_record + %s, not_returned = not_returned + %s where reader_id = %s"
                cur.execute(sql, (delta_borrowed, delta_borrowed, reader_id))
                stack.append(("update", "READER24331912", {"reader_id": reader_id}, "total_record", old_reader_record, False))
                operation_count += 1
                stack.append(("update", "READER24331912", {"reader_id": reader_id}, "not_returned", old_not_returned, True))
                operation_count += 1
    except Exception as e:
        flag = False
        msg = str(e)
        for _ in range(operation_count):
            stack.pop()
        
    finally:
        conn.close()
        
    return flag, msg, stack

def check_ownbook(reader_id, title_id, delta_borrowed):
    conn = build_connection()
    
    flag = True
    msg = ""
    
    try:
        with conn:
            with conn.cursor() as cur:
                sql = "select not_returned from BORROW24331912 where reader_id = %s and title_id = %s"
                cur.execute(sql, (reader_id, title_id))
                rows = cur.fetchall()
                
                if rows is None:
                    flag = False
                    msg = f"Reader {reader_id} has not borrowed book {title_id} before."
                
                else:
                    total_not_returned = 0
                    for row in rows:
                        total_not_returned += row[0]
                    
                    if total_not_returned == 0:
                        flag = False
                        msg = f"Reader {reader_id} has not borrowed book {title_id} before."
                    elif total_not_returned < delta_borrowed:
                        flag = False
                        msg = f"Reader {reader_id} has not borrowed enough book {title_id} to return."
    except Exception as e:
        flag = False
        msg = str(e)
    
    finally:
        conn.close()
    
    return flag, msg

def calculate_duration(current_timestamp, history_timestamp):
    delta = current_timestamp - history_timestamp
    duration_seconds = delta.total_seconds()
    duration_days = ceil(duration_seconds / 86400)
    return duration_days

def return_book(reader_id, title_id, delta_borrowed, current_timestamp, stack):
    total_books = delta_borrowed
    total_fine = 0.0
    
    flag = True
    msg = f"Insert return record successfully! The fine of reader_id {reader_id} needs to pay is: "
    operation_count = 0
    
    conn = build_connection()
    
    try:
        with conn:
            with conn.cursor() as cur:
                sql = "insert into RETURN24331912 values(%s, %s, %s, %s)"
                cur.execute(sql, (reader_id, title_id, delta_borrowed, current_timestamp))
                stack.append(("insert", "RETURN24331912", {"reader_id": reader_id, "title_id": title_id, "time": current_timestamp}, False))
                operation_count += 1
                
                cur.execute("select borrowed from CNT24331912 where title_id = %s", (title_id, ))
                old_borrowed = cur.fetchone()[0]
                sql = "update CNT24331912 set borrowed = borrowed - %s where title_id = %s"
                cur.execute(sql, (delta_borrowed, title_id))
                stack.append(("update", "CNT24331912", {"title_id": title_id}, "borrowed", old_borrowed, False))
                operation_count += 1
                
                cur.execute("select not_returned from READER24331912 where reader_id = %s", (reader_id, ))
                old_not_returned = cur.fetchone()[0]
                sql = "update READER24331912 set not_returned = not_returned - %s where reader_id = %s"
                cur.execute(sql, (delta_borrowed, reader_id))
                stack.append(("update", "READER24331912", {"reader_id": reader_id}, "not_returned", old_not_returned, False))
                operation_count += 1
                
                sql = "select fine from READER24331912 where reader_id = %s"
                cur.execute(sql, (reader_id, ))
                total_fine += float(cur.fetchone()[0])
                old_fine = total_fine
                
                #核心读者更新逻辑
                current_timestamp = datetime.strptime(current_timestamp, "%Y-%m-%d %H:%M:%S")
                cur.execute("select price from LIB24331912 where title_id = %s", (title_id, ))
                price = float(cur.fetchone()[0])
                sql = "select time, not_returned from BORROW24331912 where reader_id = %s and title_id = %s and not_returned > 0 order by time"
                cur.execute(sql, (reader_id, title_id))
                rows = cur.fetchall()
                for row in rows:
                    history_timestamp, not_returned = row[0], row[1]
                    time = history_timestamp.strftime('%Y-%m-%d %H:%M:%S')
                    days = calculate_duration(current_timestamp, history_timestamp)
                    
                    if not_returned <= total_books:
                        total_fine += min(price * not_returned, max(price * not_returned * 0.1 * (days - 30), 0)) #超过30天未还罚款规则
                        sql = "update BORROW24331912 set not_returned = 0 where reader_id = %s and title_id = %s and time = %s"
                        cur.execute(sql, (reader_id, title_id, history_timestamp))
                        stack.append(("update", "BORROW24331912", {"reader_id": reader_id, "title_id": title_id, "time": time}, "not_returned", not_returned, False))
                        operation_count += 1
                        total_books -= not_returned
                    else:
                        total_fine += min(price * total_books, max(price * not_returned * 0.1 * (days - 30), 0))
                        sql = "update BORROW24331912 set not_returned = %s where reader_id = %s and title_id = %s and time = %s"
                        cur.execute(sql, (not_returned - total_books, reader_id, title_id, history_timestamp))
                        stack.append(("update", "BORROW24331912", {"reader_id": reader_id, "title_id": title_id, "time": time}, "not_returned", not_returned, False))
                        operation_count += 1
                        total_books = 0
                        
                    if total_books == 0: #本次还书已经记录完毕
                        break
                
                sql = "update READER24331912 set fine = %s where reader_id = %s"
                cur.execute(sql, (Decimal(str(total_fine)), reader_id))
                stack.append(("update", "READER24331912", {"reader_id": reader_id}, "fine", old_fine, True))
                operation_count += 1
                
                msg += f"{total_fine:.2f}"
    except Exception as e:
        flag = False
        msg = str(e)
        for _ in range(operation_count):
            stack.pop()
    
    finally:
        conn.close()
        
    return flag, msg, stack

def get_library():
    conn = build_connection()
    
    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute("select * from LIB24331912 order by title_id")
                rows = cur.fetchall()
    except Exception as e:
        return None
    
    finally:
        conn.close()
    
    return rows

def get_bookstore():
    conn = build_connection()
    
    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute("select lib.title_id, lib.title, lib.author, cnt.remains, cnt.borrowed from LIB24331912 lib, CNT24331912 cnt where lib.title_id = cnt.title_id order by lib.title_id")
                rows = cur.fetchall()
    except Exception as e:
        return None
    
    finally:
        conn.close()
        
    return rows

def get_readers():
    conn = build_connection()
    
    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute("select reader_id, reader_name, fine from READER24331912 order by reader_id")
                rows = cur.fetchall()
    except Exception as e:
        return None
    
    finally:
        conn.close()
    
    new_rows = []
    for row in rows:
        reader_id, reader_name, fine = row
        if float(fine) == 0.00:
            status = "normal"
        else:
            status = "overdue"
        new_rows.append( (reader_id, reader_name, status) )

    return new_rows

def get_history():
    conn = build_connection()
    
    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute("select lib.title_id, lib.title, lib.author, pin.number, pin.time from LIB24331912 lib, PIN24331912 pin where lib.title_id = pin.title_id")
                purchase_rows = cur.fetchall()
                cur.execute("select lib.title_id, lib.title, lib.author, pout.number, pout.time from LIB24331912 lib, POUT24331912 pout where lib.title_id = pout.title_id")
                abandon_rows = cur.fetchall()           
    except Exception as e:
        return None
    
    finally:
        conn.close()
    
    new_rows = []
    for row in purchase_rows:
        title_id, title, author, number, time = row
        new_rows.append( (title_id, title, author, number, time, "purchase") )
    for row in abandon_rows:
        title_id, title, author, number, time = row
        new_rows.append( (title_id, title, author, number, time, "abandon") )
        
    new_rows.sort(key = lambda x: x[4])
    return new_rows

def get_borrow(reader_id = None, title_id = None):
    conn = build_connection()
    
    try:
        with conn:
            with conn.cursor() as cur:
                if reader_id is not None:
                    sql = "select lib.title_id, lib.title, lib.author, bor.time, bor.not_returned from LIB24331912 lib, BORROW24331912 bor where lib.title_id = bor.title_id and bor.not_returned > 0 and reader_id = %s order by time"
                    cur.execute(sql, (reader_id, ))
                    rows = cur.fetchall()
                elif title_id is not None:
                    sql = "select re.reader_id, re.reader_name, bor.time from READER24331912 re, BORROW24331912 bor where re.reader_id = bor.reader_id and title_id = %s and bor.not_returned > 0 order by time"
                    cur.execute(sql, (title_id, ))
                    rows = cur.fetchall()
    except Exception as e:
        return None
    
    finally:
        conn.close()
    
    new_rows = []

    if reader_id is not None:
        for row in rows:
            title_id, title, author, borrow_time, not_returned = row
            expected_return_time =  borrow_time + timedelta(days=30)
            new_rows.append( (title_id, title, author, borrow_time, not_returned, expected_return_time) )
    elif title_id is not None:
        for row in rows:
            reader_id, reader_name, borrow_time = row
            expected_return_time = borrow_time + timedelta(days=30)
            new_rows.append( (reader_id, reader_name, borrow_time, expected_return_time) )
    
    return new_rows

def get_reader_rank():
    conn = build_connection()
    
    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute("select reader_name, total_record from READER24331912 where total_record > 0 order by total_record desc, reader_id")
                rows = cur.fetchall()
    except Exception as e:
        return None
    
    finally:
        conn.close()
    
    return rows

def get_book_rank():
    conn = build_connection()
    
    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute("select lib.title, cnt.total_record from LIB24331912 lib, CNT24331912 cnt where lib.title_id = cnt.title_id and cnt.total_record > 0 order by cnt.total_record desc")
                rows = cur.fetchall()
    except Exception as e:
        print(str(e))
        return None
    
    finally:
        conn.close()
    
    return rows

def sql_literal(value):
    """根据值的类型，返回符合SQL语法的字面量字符串"""
    if isinstance(value, (int, float)):
        return str(value)
    elif isinstance(value, datetime):
        return f"'{value.strftime('%Y-%m-%d %H:%M:%S')}'"
    else:
        escaped = str(value).replace("'", "''")
        return f"'{escaped}'"

#撤销操作逻辑
class UnknownOpError(Exception):
    pass

class LackTagError(Exception):
    pass

def inv_operation(stack):
    flag = True
    msg = "Undo latest operation successfully!"

    if not stack:
        flag = False
        msg = "You have no operation concerning writing data before."
        return flag, msg, stack

    temp_buf = deque()

    conn = build_connection()
    try:
        with conn:
            with conn.cursor() as cur:
                temp_buf.append(stack[-1])
                
                operation = stack[-1][0]
                if operation == "insert":
                    if len(stack[-1]) != 4:
                        raise LackTagError("Lack necessary tags")
                    
                    _, table_name, primary_keys, _ = stack.pop()
                    sql = f"DELETE FROM {table_name} WHERE " + " AND ".join([f"{k}={sql_literal(v)}" for k, v in primary_keys.items()])
                    print(f"Executing SQL: {sql}")
                elif operation == "delete":
                    if len(stack[-1]) != 4:
                        raise LackTagError("Lack necessary tags")
                    
                    _, table_name, all_keys, _ = stack.pop()
                    sql = f"INSERT INTO {table_name} (" + ", ".join(all_keys.keys()) + ") VALUES (" + ", ".join([sql_literal(v) for v in all_keys.values()]) + ")"
                    print(f"Executing SQL: {sql}")
                elif operation == "update":
                    if len(stack[-1]) != 6:
                        raise LackTagError("Lack necessary tags")
                    
                    _, table_name, primary_keys, critical_key, old_value, _ = stack.pop()
                    sql = f"UPDATE {table_name} SET {critical_key}={sql_literal(old_value)} WHERE " + " AND ".join([f"{k}={sql_literal(v)}" for k, v in primary_keys.items()])
                    print(f"Executing SQL: {sql}")
                else:
                    raise UnknownOpError(f"Unknown operation type: {operation}")
                cur.execute(sql)

                while stack and stack[-1][-1] == False:
                    temp_buf.append(stack[-1])
                    
                    operation = stack[-1][0]
                    if operation == "insert":
                        if len(stack[-1]) != 4:
                            raise LackTagError("Lack necessary tags")
                        
                        _, table_name, primary_keys, _ = stack.pop()
                        sql = f"DELETE FROM {table_name} WHERE " + " AND ".join([f"{k}={sql_literal(v)}" for k, v in primary_keys.items()])
                        print(f"Executing SQL: {sql}")
                    elif operation == "delete":
                        if len(stack[-1]) != 4:
                            raise LackTagError("Lack necessary tags")
                        
                        _, table_name, all_keys, _ = stack.pop()
                        sql = f"INSERT INTO {table_name} (" + ", ".join(all_keys.keys()) + ") VALUES (" + ", ".join([sql_literal(v) for v in all_keys.values()]) + ")"
                        print(f"Executing SQL: {sql}")
                    elif operation == "update":
                        if len(stack[-1]) != 6:
                            raise LackTagError("Lack necessary tags")
                        
                        _, table_name, primary_keys, critical_key, old_value, _ = stack.pop()
                        sql = f"UPDATE {table_name} SET {critical_key}={sql_literal(old_value)} WHERE " + " AND ".join([f"{k}={sql_literal(v)}" for k, v in primary_keys.items()])
                        print(f"Executing SQL: {sql}")
                    else:
                        raise UnknownOpError(f"Unknown operation type: {operation}")
                    cur.execute(sql)

    except LackTagError as e:
        flag = False
        msg = str(e)
        while temp_buf:
            top = temp_buf.pop()
            stack.append(top)

    except UnknownOpError as e:
        flag = False
        msg = str(e)
        while temp_buf:
            top = temp_buf.pop()
            stack.append(top)
    
    except Exception as e:
        flag = False
        msg = str(e)
        while temp_buf:
            top = temp_buf.pop()
            stack.append(top)
            
    return flag, msg, stack