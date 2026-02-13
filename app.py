import sqlite3

def get_user(username):
    # LỖI BẢO MẬT: SQL Injection (không nên cộng chuỗi trực tiếp)
    query = "SELECT * FROM users WHERE username = '" + username + "'"
    print("Đang chạy câu lệnh: " + query)
    
    # LỖI BẢO MẬT: Lộ mật khẩu (Hardcoded Secret)
    db_password = "admin_password_123" 
    
    return query

if __name__ == "__main__":
    get_user("admin")
# test