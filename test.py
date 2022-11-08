from passlib.context import CryptContext
import json
from datetime import datetime
#set up the hash function
pwd = CryptContext(schemes=["bcrypt"], deprecated="auto")
dict = {'email':'thanhq'}
time = datetime.now()
dict["time"] = str(time)
print(type(time))
print(dict)
encoded = json.dumps(dict)
# print(encoded)



