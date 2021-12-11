import platform

def aaa():
    if platform.system().lower() == 'windows':
        print("windows")
    elif platform.system().lower() == 'linux':
        print("linux")

print(platform.system().lower())