" ---------- Developed by Elpis as part of Master Thesis project elpidoforos@gmail.com ------------------------"
import re
import hashlib
import data as data

try:
    #Open the kept logfile, if not revert to a default one
    with open('logfile.txt', 'r') as afile:
        logs = afile.readlines()
        frame = []
        all_frame_ids = []
        for line_log in logs:
            id = re.search(r"(ID: )([0-9a-fA-F]+)",line_log)
            data = re.search(r"([0-9a-f]+ [0-9a-f]+ [0-9a-f]+ [0-9a-f]+ [0-9a-f]+ [0-9a-f]+ [0-9a-f]+ [0-9a-f]+)", line_log)
            #print line_log
            #print data.group(0)
            #print id.group(2)
            #frame.append((id.group(2),data.group(0)))
            #frame[id.group(2)] = data.group(0)
            all_frame_ids.append(id.group(2).lstrip('0'))
except:
    with open('logfile1.txt', 'r') as afile:
        logs = afile.readlines()
        frame = []
        for line_log in logs:
            print line_log

#Keep all the unique frame ids only
unique_ids = list(set(all_frame_ids))

print unique_ids
print len(unique_ids)


"""
for i in frame:
    a = hashlib.md5(i[0] + " " + i[1])
    print (i[0] + " " + i[1])
    print a.hexdigest()
"""