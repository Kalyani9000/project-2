def Registration():
    user_name=input('enter your name:')
    user_age=int(input('enter your age:'))
    phone=input('enter the mobile number:')
    gender=input('enter your self-identified gender:')
    aadharno=input('enter your addhar number:')
    account_type=input('enter the account type:')
    address=input('enter your address:')
    email=input('enter the email:') 
    account_id=letter+str(random.randint(000000000000,999999999999))      
    pin_no=int(input( 'enter the pin:'))
    c_pin=int(input('conform the  pin:'))
    if pin_no==c_pin:
        date_time=datetime.now()
        cur.execute('''
        INSERT INTO customers (name,age,phone,gender,aadhar_no,account_type,address,email,account_number,pin,date_time)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s,%s,%s)
        ''', [user_name, user_age, phone, gender,aadharno, account_type,address,email,account_id, c_pin, date_time])
        con.commit()
    else:
        print('pin does not match....')
    return f" Registration successful! Your account number is: {account_id}"
def Login():
    user_account=input('enter the account number :')
    user_pin=int(input('enterv your pin :'))
    cur.execute('SELECT * FROM customers WHERE account_number=%s AND pin=%s', [user_account, user_pin])
    res=cur.fetchall()
    return res,user_account,user_pin
def View_details():
    cur.execute('''select c.name,t.account_number,c.account_type,
    c.avl_balance from customers as c left join transactions as t
    on c.account_number=t.account_number
    WHERE c.account_number=%s AND c.pin=%s''', [user_account, user_pin] )
    View_account=cur.fetchone()
    return View_account
def Debit():
    cur.execute("SELECT avl_balance FROM customers WHERE account_number = %s", [user_account])
    res = cur.fetchall()[0]
    if res:
        avl_balance=res[0]
        amount = int(input("Hi there! How much would you like to debit: "))
        if amount <= 0:
            print("Amount must be positive.")
        elif amount > avl_balance:
            print("Insufficient balance!")
        else:
            transaction_id = 'tnx' + str(random.randint(100000, 999999999))
            trans_type = 'Debit'
            date_time = datetime.now()
            total_balance = avl_balance - amount  
            cur.execute('''INSERT INTO transactions
            (transaction_id, account_number, transaction_type,amount, date)
            VALUES (%s, %s, %s, %s, %s)''',
            [transaction_id, user_account, trans_type, amount, date_time])
            cur.execute('update customers set avl_balance=%s where account_number=%s',[total_balance,user_account])
            con.commit()
            return f'A/c Debited  for Rs:{amount} on {date_time} by ref no {transaction_id} Avl bal Rs:{total_balance}'
    else:
        print("Account not found.")
def Credit():
    cur.execute("SELECT avl_balance FROM customers WHERE account_number = %s", [user_account])
    res = cur.fetchone()
    if res:
        avl_balance = res[0]
        amount = int(input("Hi there! How much would you like to credit : "))
        transaction_id = 'tnx' + str(random.randint(100000, 999999999))
        trans_type = 'Credit'
        date_time = datetime.now()
        avl_balance += amount  
        cur.execute('''INSERT INTO transactions
        (transaction_id, account_number, transaction_type,amount, date)VALUES (%s, %s, %s, %s, %s)''',
        [transaction_id, user_account, trans_type, amount, date_time])
        cur.execute(''' update customers set avl_balance=%s where account_number=%s''',[avl_balance,user_account])
        con.commit()
        print("Transaction successful! Updated balance:", avl_balance)
        return f'Your SB A/c Credited  for Rs:{amount} on {date_time} by ref no {transaction_id} Avl bal Rs:{avl_balance}'
    else:
        print('Account not found.')
import mysql.connector as db
from datetime import datetime
time_now = datetime.now()
import random
con=db.connect(user='root',password='nani123',host='localhost',database='bank')
cur=con.cursor()
letter ='acc'
while True:
    print('1.Admin Login')
    print('2.User Login')
    
    print('3.exit')
    ch=input('Kindly choose your access level(Admin | User):')
    if ch.isalpha():
        print('Error: option must contain only digits!')      
    elif ch=='1':
        admin_id=input('enter the id:')
        admin_password=input('enter the password :')
        if admin_id.isdigit():
            admin_id = int(admin_id)
            cur.execute('select * from admin where admin_id=%s and admin_password=%s',[admin_id,admin_password])
            result=cur.fetchone()
            if result:
                while True:
                    print('1.View all Users')
                    print('2.View complete Account Details of Particular User')
                    print('3.View complete Transcations of Particular User')
                    print('4.View complete Transcations of Particular day')
                    print('5.exit')
                    admin=input('Kindly choose the options:')
                    if admin=='1':
                        def View_all_users():
                            cur.execute('select * from  customers')
                            data=cur.fetchall()
                            return data
                        for i in View_all_users():
                            print(i)
                    elif admin=='2':
                        def View_particular_user():
                            user=int(input('enter the particular customer_id:'))
                            cur.execute('select * from customers where customer_id=%s',[user])
                            particular_user=cur.fetchall()
                            return particular_user
                        print(View_particular_user())
                    elif admin=='3':
                       def view_trans_user():
                           user_account=input('enter the account number :')
                           cur.execute('select* from transactions where account_number=%s',[user_account])
                           result= cur.fetchall()
                           return result
                       res=view_trans_user()
                       print(res)
                    elif admin=='4':
                        def view_trans_day():
                            day = input('Enter the day you want the transaction (YYYY-MM-DD): ')
                            cur.execute('SELECT*FROM transactions where date = %s', (day,))
                            data = cur.fetchall()
                            return data
                        res = view_trans_day()
                        print(res)
                    elif admin=='5':
                        print('exiting from admin ')
                        break
                    else:
                        print('invalid option! Please enter vaild options')           
            else:                       
                print('invalid id or password!')
        elif ch=='3':
            print('exiting')
            break
        else:
            print('Error: Admin ID must contain only digits!') 
    elif ch=='2':
        print('1.Registration')
        print('2.Login')
        ch1=input('if you should want Login/Registration:')
        if ch1=='1':
            print("=== Bank Application Registration ===")
            result_rigistration=Registration()
            print(result_rigistration)
        elif ch1=='2':
            print("=== Login To your Bank account ===")
            Login_user,user_account,user_pin=Login()
            if Login_user:
                while True:
                    print('1.View Account details')
                    print('2.Debit Ammount')
                    print('3.Credit Ammount')
                    print('4.Pin Change')
                    print('5.Statement')
                    print('6.exit')
                    user_check=input('Kindly choose the options :')
                    if user_check =='1':
                       result=View_details()
                       print(result)
                    elif user_check=='2':
                        print('=== Debit Ammount ===')
                        result_Debit=Debit()
                        print(result_Debit)
                    elif user_check=='3':
                        print('=== Credit Ammount ===')
                        result_credit=Credit()
                        print(result_credit)
                    elif user_check=='4':
                        def pin_change():
                            account_number=input('enter the account number :')
                            cur.execute('SELECT * FROM customers WHERE account_number=%s', [account_number])
                            res=cur.fetchone()
                            if res:   
                                modify_pin=int(input('enter the new pin :'))
                                c_modify_pin=int(input('Renter the new pin :'))
                                if modify_pin==c_modify_pin:
                                    cur.execute('''update customers set pin=%s where account_number=%s''',
                                                [c_modify_pin,account_number])
                                    con.commit()
                                    return f'pin changed succesfully to {account_number} number'
                                else:
                                    print('modify_pin & c_modify_pin is does not match')
                            else:
                                print('please valid account number!')
                        res=pin_change()
                        print(res)   
                              
                    elif user_check=='5':
                        def statements():
                            account_id=input('enter the account number :')
                            cur.execute('SELECT * FROM transactions WHERE account_number=%s', [account_id])
                            res=cur.fetchall()
                            return f'{res}' 
                        result=statements()
                        print(result) 
                    elif user_check=='6':
                        print('''Thank you for banking with us. Your trust means everything,and we look forward to serving you again. Have a secure and successful day!''')
                        break
                    else:
                        print('invalid option! Please enter vaild') 
            else:
                print('Account number & pin not found. Please check and try again.')
        else:
            print('invalid option! Please enter either 1 or 2')      
    else:
        print('Error:Please choose Admin or User to proceed')
    exit_prompt = input('Do you want to continue? (yes/no): ').strip().lower()
    if exit_prompt != 'yes':
        break
cur.close()
con.close()
print(" Connection closed. Thank you for using Bank Management System.")
