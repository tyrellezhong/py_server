# from package_use_exp import os_use_exp
# from package_use_exp import yaml_exp
# import os

# if __name__ == "__main__":
#     os_use_exp.path_test()
#     yaml_exp.yaml_load("")
#     strss = "-+-xxx"
#     ok = strss.lstrip("+-")
#     xx = 0

# print(os.getenv("shell_val", "not found"))

# info = os.popen(r'p4 changes -m 1 ' + file)


import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

print (s.connect(('9.135.103.28', 9000)))

a = 4

print (s.send(a.to_bytes(4, byteorder='big') + b'1111'))