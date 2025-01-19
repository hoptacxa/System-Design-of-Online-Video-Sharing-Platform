import hashlib
import os

def b(input_string, orig):
    return hashlib.sha256(f"{orig}-{input_string}".encode('utf-8')).hexdigest()

orig = "Nghiem-Xuan-Hao"
c = orig

for _ in range(3):
    c = b(c, orig)[:len(c)]
    ping = f"ping -c 1 {c}.com"
    print(ping)
    if os.system(ping) == 0:
        print(f"Found valid domain: {c}.com")
        break

print(c)
