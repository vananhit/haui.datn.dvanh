from repositories import customers_repo,account_repo,face_repo
from dtos.auth.AccountDto import AccountDto 
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import configparser
config = configparser.ConfigParser()
config.read('example.ini')
import random
import string
import re
from fastapi import HTTPException
#Thêm tk mới
def create_account(user_name, password, email, customer_id, first_name, last_name, address):

    #kiểm user name và email đã tồn tại chưa
    if not account_repo.find_account_by_username_or_email(username=user_name,email=email):

        #Nếu mật khẩu chưa được tạo thì tạo ngẫu nhiên
        if not password:
            characters = string.ascii_letters + string.digits
            # Tạo mật khẩu ngẫu nhiên
            password = ''.join(random.choice(characters) for i in range(8))
            print(password)
        else:
            #Nếu gửi lên kèm mật khẩu
            #Kiểm tra định dạng password
            regex = r'^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[!@#$%^&*()_+=-])[0-9a-zA-Z!@#$%^&*()_+=-]{8,}$'
            if not re.match(regex, password):
                raise HTTPException(
                    status_code=400,
                    detail="Mật khẩu phải chứa ít nhất một chữ số, một ký tự hoa, một ký tự thường, một ký tự đăc biệt và dài ít nhất 8 ký tự!"
                )
        #Kiểm tra định dạng email
        regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(regex, email):
            raise HTTPException(
                status_code=400,
                detail='Email sai định dạng'
            )
        #Thêm tài khoản vào csdl
        ans = account_repo.insert_account(user_name, password, email, customer_id, first_name, last_name, address)
        
        if ans:
            #Gửi email thông báo cho người dùng tài khoản đã được tạo kèm mật khẩu nếu ko gửi kèm mật khẩu
            # Tạo message
            msg = MIMEMultipart()
            msg['From'] = config['SMTP']['username']
            msg['To'] = email
            msg['Subject'] = 'Thông tin tài khoản hệ thống điểm danh'
            # Thêm nội dung email
            text = MIMEText(f"Tên đăng nhập: {user_name}\nMật khẩu:{password}")
            msg.attach(text)

            # Gửi email
            try:
                server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
                server.ehlo()
                server.login(config['SMTP']['username'], config['SMTP']['password'])
                server.sendmail(config['SMTP']['username'], email, msg.as_string())
                server.close()

                print('Email sent!')
            except Exception as e:
                print('Something went wrong...')
                print(e)
            return ans
        
    return None

#Tìm tài khoản theo user name
def find_by_user_name(user_name):
    return account_repo.find_by_user_name(user_name=user_name)

#Tìm tài khoản theo email
def find_by_email(email):
    return account_repo.find_by_email(email=email)

#Xoá tài khoản theo account_id
def delete_by_id(account_id):
    #TODO Kiểm tra xem account có thuộc quền quản lý của khách hàng đó
    if face_repo.count_faces_by_account_id(account_id=account_id)>0:
        raise HTTPException(
            status_code= 400,
            detail='Xoá hết dữ liệu nhận dạng trước khi xoá tài khoản!'
        )
    return account_repo.delete_account_by_id(account_id=account_id)
