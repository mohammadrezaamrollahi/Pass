import random
import sqlite3
import string

# تابع برای تولید پسورد 15 کاراکتری
def generate_password():
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for _ in range(15))
    return password

# تابع برای چک کردن تکراری نبودن پسورد
def is_unique_password(password, passwords):
    for user, passw in passwords.items():
        if passw == password:
            return False
    return True

# تابع برای ذخیره پسورد در دیتابیس
def save_password_to_database(username, password):
    # اتصال به دیتابیس یا ایجاد آن اگر وجود نداشته باشد
    connection = sqlite3.connect('passwords.db')
    cursor = connection.cursor()

    # ایجاد جدول اگر وجود نداشته باشد
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS passwords (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            password TEXT
        )
    ''')

    # وارد کردن نام کاربری و پسورد در دیتابیس
    cursor.execute('INSERT INTO passwords (username, password) VALUES (?, ?)', (username, password))

    # ذخیره تغییرات و بستن اتصال
    connection.commit()
    connection.close()

# ایجاد یک دیکشنری برای نگهداری نام کاربری و پسوردها
user_passwords = {}

# تعداد کاربرانی که می‌خواهید نام کاربری و پسورد برای آن‌ها بسازید
num_users = int(input('تعداد کاربران: '))

for i in range(num_users):
    # دریافت نام کاربری
    username = input(f'نام کاربری برای کاربر شماره {i+1}: ')

    # تولید پسورد تا زمانی که یک پسورد یکتا تولید شود
    while True:
        generated_password = generate_password()
        if is_unique_password(generated_password, user_passwords):
            break

    # ذخیره نام کاربری و پسورد در دیکشنری
    user_passwords[username] = generated_password

    # ذخیره نام کاربری و پسورد در دیتابیس
    save_password_to_database(username, generated_password)

# چاپ نام کاربری و پسورد هر کاربر
for user, password in user_passwords.items():
    print(f'نام کاربری: {user}, پسورد: {password}')
