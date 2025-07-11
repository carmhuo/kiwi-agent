import sqlite3

# 读取SQL初始化脚本
with open('kiwi_sqlite.sql', 'r', encoding='utf-8') as f:
    init_script = f.read()

# 创建并初始化数据库
conn = sqlite3.connect('../../data/kiwi/kiwi.sqlite.db')
conn.executescript(init_script)
conn.commit()

# 验证表创建
cursor = conn.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
print("创建的表列表:")
print(cursor.fetchall())

conn.close()