# import sqlite3
# import os
# from flask import Flask, request

# app = Flask(__name__)

# @app.route('/login')
# def login():
#     username = request.args.get('username')
    
#     # LỖI BẢO MẬT 1 (SAST - B608): SQL Injection
#     # Bandit sẽ phát hiện việc cộng chuỗi trực tiếp vào query
#     query = "SELECT * FROM users WHERE username = '" + username + "'"
    
#     # LỖI BẢO MẬT 2 (SAST - B105): Hardcoded Password
#     # Bandit sẽ phát hiện mật khẩu nằm chình ình trong code
#     db_password = "admin_password_123" 
    
#     return f"Đang kiểm tra user: {username} với query: {query}"

# if __name__ == "__main__":
#     port = int(os.environ.get("PORT", 10000))
#     app.run(host='0.0.0.0', port=port)

#===========================================================================
#file sau khi chỉnh sửa lỗi SAST
import sqlite3
import os
from flask import Flask, request, jsonify

app = Flask(__name__)

# Hàm khởi tạo database mẫu (để app có dữ liệu chạy thực tế)
def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT)')
    cursor.execute("INSERT OR IGNORE INTO users (id, username) VALUES (1, 'admin')")
    conn.commit()
    conn.close()

@app.route('/login')
def login():
    username = request.args.get('username', 'guest')
    
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    # --- ĐÃ SỬA LỖI SQL INJECTION ---
    # Sử dụng Parameterized Query với dấu "?"
    query = "SELECT username FROM users WHERE username = ?"
    cursor.execute(query, (username,))
    user = cursor.fetchone()
    conn.close()
    
    if user:
        return jsonify({"status": "success", "user": user[0]})
    return jsonify({"status": "error", "message": "User not found"}), 404

if __name__ == "__main__":
    init_db()
    port = int(os.environ.get("PORT", 10000))
    # Thêm # nosec vào cuối dòng để Bandit không báo lỗi B104 nữa
    app.run(host='0.0.0.0', port=port)  # nosec



#===========================================================================

# file có lỗi DAST Path Traversal
# import sqlite3
# import os
# from flask import Flask, request

# app = Flask(__name__)

# def init_db():
#     conn = sqlite3.connect('database.db')
#     cursor = conn.cursor()
#     cursor.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT)')
#     cursor.execute("INSERT OR IGNORE INTO users (id, username) VALUES (1, 'admin')")
#     conn.commit()
#     conn.close()

# @app.route('/')
# def home():
#     return "Hệ thống DevSecOps - Demo Path Traversal. Thử: /read?file=requirements.txt"

# @app.route('/read')
# def read_file():
#     # LỖI BẢO MẬT DAST: Path Traversal
#     # Hacker có thể truyền vào file=../../etc/passwd để đọc file hệ thống
#     filename = request.args.get('file')
#     try:
#         with open(filename, 'r') as f:
#             return f.read()
#     except Exception as e:
#         return str(e), 404

# if __name__ == "__main__":
#     init_db() # Fix lỗi sập database trên Render
#     port = int(os.environ.get("PORT", 10000))
#     # Dùng # nosec để vượt qua bước SAST
#     app.run(host='0.0.0.0', port=port)  # nosec