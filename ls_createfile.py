# coding:utf-8
import uuid
import time
import os
l = input (u'in put the  count'+os.linesep)
# l = 500
for i in range(int(l)):
    file_name = str(i+1)+'.txt'
    with open(file_name,'a+') as f:
        f.write(str(uuid.uuid4()))
        f.flush()
        f.close()
print('finish......')
time.sleep(3)