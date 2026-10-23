from collections import deque
from datetime import datetime

def sql_literal(value):
    """根据值的类型，返回符合SQL语法的字面量字符串"""
    if isinstance(value, (int, float)):
        return str(value)
    elif isinstance(value, datetime):
        return f"'{value.strftime('%Y-%m-%d %H:%M:%S')}'"
    else:
        escaped = str(value).replace("'", "''")
        return f"'{escaped}'"


def insert(stack, table_name, primary_keys):
    operation_count = 0
    
    try:
        stack.append(("insert", table_name, primary_keys, True))
        operation_count += 1
    except Exception as e:
        print(str(e))
        for _ in range(operation_count):
            stack.pop()
            
    return stack

def delete(stack, table_name, all_keys):
    operation_count = 0
    
    try:
        stack.append(("delete", table_name, all_keys, True))
        operation_count += 1
    except Exception as e:
        print(str(e))
        for _ in range(operation_count):
            stack.pop()
            
    return stack

def update(stack, table_name, primary_keys, critical_key, old_value):
    operation_count = 0
    
    try:
        stack.append(("update", table_name, primary_keys, critical_key, old_value, False))
        operation_count += 1
    except Exception as e:
        print(str(e))
        for _ in range(operation_count):
            stack.pop()
            
    return stack

def update_last(stack, table_name, primary_keys, critical_key, old_value):
    operation_count = 0
    
    try:
        stack.append(("update", table_name, primary_keys, critical_key, old_value, True))
        operation_count += 1
    except Exception as e:
        print(str(e))
        for _ in range(operation_count):
            stack.pop()
            
    return stack


def inv_operation(stack):
    if not stack:
        return stack
    
    operation = stack[-1][0]
    if operation == "insert":
        _, table_name, primary_keys, _ = stack.pop()
        sql = f"DELETE FROM {table_name} WHERE " + " AND ".join([f"{k}={sql_literal(v)}" for k, v in primary_keys.items()])
        print(f"Executing SQL: {sql}")
    elif operation == "delete":
        _, table_name, all_keys, _ = stack.pop()
        sql = f"INSERT INTO {table_name} (" + ", ".join(all_keys.keys()) + ") VALUES (" + ", ".join([sql_literal(v) for v in all_keys.values()]) + ")"
        print(f"Executing SQL: {sql}")
    elif operation == "update":
        _, table_name, primary_keys, critical_key, old_value, _ = stack.pop()
        sql = f"UPDATE {table_name} SET {critical_key}={sql_literal(old_value)} WHERE " + " AND ".join([f"{k}={sql_literal(v)}" for k, v in primary_keys.items()])
        print(f"Executing SQL: {sql}")
    
    while stack and stack[-1][-1] == False:
        operation = stack[-1][0]
        if operation == "insert":
            _, table_name, primary_keys, _ = stack.pop()
            sql = f"DELETE FROM {table_name} WHERE " + " AND ".join([f"{k}={sql_literal(v)}" for k, v in primary_keys.items()])
            print(f"Executing SQL: {sql}")
        elif operation == "delete":
            _, table_name, all_keys, _ = stack.pop()
            sql = f"INSERT INTO {table_name} (" + ", ".join(all_keys.keys()) + ") VALUES (" + ", ".join([sql_literal(v) for v in all_keys.values()]) + ")"
            print(f"Executing SQL: {sql}")
        elif operation == "update":
            _, table_name, primary_keys, critical_key, old_value, _ = stack.pop()
            sql = f"UPDATE {table_name} SET {critical_key}={sql_literal(old_value)} WHERE " + " AND ".join([f"{k}={sql_literal(v)}" for k, v in primary_keys.items()])
            print(f"Executing SQL: {sql}")
            
stack = deque()
stack.clear()

# 插入操作
title_id = "A1001"
reader_id = "510000F"
time = "2023-06-01 10:00:00"
stack = insert(stack, "BORROW24331912", {"title_id": title_id, "reader_id": reader_id, "time": time})
inv_operation(stack)

# 删除操作
title_id = "C2003"
remains = 0
borrowed = 0
total_records = 30
stack = delete(stack, "BORROW24331912", {"title_id": title_id, "remains": remains, "borrowed": borrowed, "total_records": total_records})


# 更新操作（非关键，可连续回滚）
title_id= "511524F"
prev_borrowed = 6
prev_total_records = 25
stack = update(stack, "CNT24331912", {"title_id": title_id}, "borrowed", prev_borrowed)

# 最后一个更新（关键，回滚终止点）
stack = update_last(stack, "CNT24331912", {"title_id": title_id}, "total_records", prev_total_records)

#inv_operation(stack)  # 回滚操作