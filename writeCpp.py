from os import path
import re

content = r'''{
    "configurations": [
        {
            "name": "Win32",
            "includePath": [
                "${workspaceFolder}/**",
                "D:/Program/MinGW/include/*"
            ],
            "defines": [
                "_DEBUG",
                "UNICODE",
                "_UNICODE"
            ],
            "compilerPath": "D:/Program/MinGW/bin/gcc.exe",
            "cStandard": "c11",
            "cppStandard": "c++17",
            "intelliSenseMode": "gcc-x86"
        }
    ],
    "version": 4
}'''    

def writeCpp(envPath, CodePath):
    with open(path.join(CodePath, r'.vscode/c_cpp_properties.json'), "wb") as code:
        code.write(content.replace(r'D:/Program/MinGW', getMinGW(envPath)).replace('\\', '/').encode('utf-8'))

def getMinGW(str):
    value = ''
    result = re.findall(r'([a-zA-Z]:((\\[a-zA-Z0-9_]{1,16}))+)\\bin', str)
    for one in result:
        if 'mingw' in one[0].lower():
            value = one[0]
    return value
