import sqlite3
import os
from flask import Flask, request

app = Flask(__name__)

@app.route('/login')
def login():
    username = request.args.get('username')
    
    # LỖI BẢO MẬT 1 (SAST - B608): SQL Injection
    # Bandit sẽ phát hiện việc cộng chuỗi trực tiếp vào query
    query = "SELECT * FROM users WHERE username = '" + username + "'"
    
    # LỖI BẢO MẬT 2 (SAST - B105): Hardcoded Password
    # Bandit sẽ phát hiện mật khẩu nằm chình ình trong code
    db_password = "admin_password_123" 
    
    return f"Đang kiểm tra user: {username} với query: {query}"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)