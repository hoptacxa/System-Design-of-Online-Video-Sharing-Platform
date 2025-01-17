import hashlib
import os

def b(input_string):
    return hashlib.sha256(input_string.encode('utf-8')).hexdigest()

c = "Nghiem-Xuan-Hao"

for _ in range(3):
    c = b(c)[:len(c)]
    ping = f"ping -c 1 {c}.com"
    print(ping)
    if os.system(ping) == 0:
        print(f"Found valid domain: {c}.com")
        break

print(c)
