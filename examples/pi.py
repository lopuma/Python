import os
target = "OS_Linux_FT_CSD_PREG:174"
initial_dir = '/home/esy9d7l1/compliance/extracion'
path = ''
for root, _, files in os.walk(initial_dir):
    if target in files:
        path = os.path.join(root, target)
        break
print(path)