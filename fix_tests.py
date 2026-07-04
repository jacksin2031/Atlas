import os
import re

os.chdir(r'E:\資料夾\桌面\Atlas\packages\vision\tests')

with open('test_unit.py', 'r', encoding='utf-8-sig') as f:
    content = f.read()

# Fix the mangled b"" strings
content = content.replace('b\")', 'b\"\")')

with open('test_unit.py', 'w', encoding='utf-8') as f:
    f.write(content)

print('Fixed test_unit.py')
