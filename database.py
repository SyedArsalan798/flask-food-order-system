import sqlite3 as s
# global countCustomers

class Database:
    def __init__(self):
        pass

    @staticmethod
    def CreateTableAdmin():
        connection = s.connect("foodSystem.db")
        cursor = connection.cursor()
        cursor.execute('''
        CREATE TABLE Admin(
        admin_id       int PRIMARY KEY ,
        admin_email    VARCHAR (30) ,
        admin_password VARCHAR (30)
        )
        ''')
        connection.commit()
        connection.close()

    @staticmethod
    def insertIntoAdmin(id, email, password):
        connection = s.connect("foodSystem.db")
        cursor = connection.cursor()
        try:
            cursor.execute("INSERT INTO ADMIN VALUES (?,?,?)",
                        (id, email, password))
            connection.commit()
        except:
            connection.rollback()
        connection.close()

    @staticmethod
    def checkInAdmin(email, password):
        connection = s.connect("foodSystem.db")
        cursor = connection.cursor()
        admins = cursor.execute("SELECT * from Admin")
        for admin in admins:
            if (email and password) in admin:
                return True
        return False

    @staticmethod
    def returnAdmins():
        connection = s.connect("foodSystem.db")
        cursor = connection.cursor()
        admins = cursor.execute("SELECT * from Admin")
        return admins

    @staticmethod
    def CreateTableCustomer():
        connection = s.connect("foodSystem.db")
        cursor = connection.cursor()
        cursor.execute('''
        CREATE TABLE Customers(
        customer_id    INTEGER PRIMARY KEY AUTOINCREMENT,
        phone_no       varchar (25),
        user_name      VARCHAR (30),
        first_name     VARCHAR (30),
        last_name      VARCHAR (30),
        password        VARCHAR (30),
        address        VARCHAR (100),
        email          VARCHAR (50),
        admin_id        int not null,
        FOREIGN KEY (ADMIN_ID) REFERENCES ADMIN(ADMIN_ID)
        )
        '''
                       )
        connection.commit()
        connection.close()

    @staticmethod
    def insertIntoCustomer(first_name, last_name, username, Useremail, Userpassword, phone, address):
        connection = s.connect("foodSystem.db")
        cursor = connection.cursor()
        cursor.execute("pragma foreign_keys=on")
        cursor.execute("BEGIN TRANSACTION")
        try:
            cursor.execute('''INSERT INTO CUSTOMERS(phone_no,user_name,first_name,last_name,password,address,email,admin_id) VALUES
            (?,?,?,?,?,?,?,?)
            ''', (phone, username, first_name, last_name, Userpassword, address, Useremail, 1))
            connection.commit()
        except:
            connection.rollback()
        connection.close()

    # @staticmethod
    # def updateCustomerWithPayId(cus_id, pay_id):
    #     connection = s.connect("foodSystem.db")
    #     cursor = connection.cursor()
    #     cursor.execute("pragma foreign_keys=on")
    #     cursor.execute(
    #         f"UPDATE Customers SET pay_id = '{pay_id}' WHERE customer_id = {cus_id}")
    #     connection.commit()
    #     connection.close()

    @ staticmethod
    def customerIdExists(id):
        connection = s.connect("foodSystem.db")
        cursor = connection.cursor()
        customerCountList = cursor.execute(
            f"SELECT COUNT(*) FROM Customers WHERE customer_id = {id}").fetchone()
        return int(''.join([str(n) for n in customerCountList])) == 1

    @staticmethod
    def deleteCustomer(id):
        connection = s.connect("foodSystem.db")
        cursor = connection.cursor()
        cursor.execute("pragma foreign_keys=on")
        cursor.execute("BEGIN TRANSACTION")
        try:
            cursor.execute(f"DELETE FROM Customers WHERE customer_id = {id}")
            connection.commit()
        except:
            connection.rollback()
        connection.close()

    @staticmethod
    def checkIfCustomerAlreadyExistForLogin(Useremail, Userpassword):
        connection = s.connect("foodSystem.db")
        cursor = connection.cursor()
        Customers = cursor.execute("SELECT * from Customers")
        for customer in Customers:
            if (Useremail and Userpassword) in customer:
                return True
        return False
    
    @staticmethod
    def checkIfCustomerAlreadyExistForSignUp(Useremail, Userpassword):
        connection = s.connect("foodSystem.db")
        cursor = connection.cursor()
        Customers = cursor.execute("SELECT * from Customers")
        for customer in Customers:
            if (Useremail and Userpassword) in customer:
                return True
            if (Useremail) in customer:
                return True
        return False

    @staticmethod
    def returnCustomerAccordingToSession(email, password):
        connection = s.connect("foodSystem.db")
        cursor = connection.cursor()
        customer = cursor.execute(
            f"SELECT * from Customers where email = '{email}' and password = '{password}'")
        return customer

    @staticmethod
    def returnCustomers():
        connection = s.connect("foodSystem.db")
        cursor = connection.cursor()
        customers = cursor.execute("SELECT * from Customers")
        return customers

    
##########################################################################################################################################

    @staticmethod
    def CreateTableRider():
        connection = s.connect("foodSystem.db")
        cursor = connection.cursor()
        cursor.execute('''
        CREATE TABLE Riders(
        rider_id    INTEGER PRIMARY KEY AUTOINCREMENT,
        phone_no       varchar (25),
        user_name      VARCHAR (30),
        first_name     VARCHAR (30),
        last_name      VARCHAR (30),
        password        VARCHAR (30),
        address        VARCHAR (100),
        email          VARCHAR (50),
        admin_id        int not null,
        FOREIGN KEY (ADMIN_ID) REFERENCES ADMIN(ADMIN_ID)
        )
        '''
                       )
        connection.commit()
        connection.close()

    @staticmethod
    def insertIntoRider(first_name_rider, last_name_rider, username_rider, Useremail_rider, Userpassword_rider, phone_rider, address_rider):
        connection = s.connect("foodSystem.db")
        cursor = connection.cursor()
        cursor.execute("pragma foreign_keys=on")
        cursor.execute("BEGIN TRANSACTION")
        try:
            cursor.execute('''INSERT INTO RIDERS(phone_no,user_name,first_name,last_name,password,address,email,admin_id) VALUES
            (?,?,?,?,?,?,?,?)
            ''', (phone_rider, username_rider, first_name_rider, last_name_rider, Userpassword_rider, address_rider, Useremail_rider, 1))
            connection.commit()
        except:
            connection.rollback()
        connection.close()

    @ staticmethod
    def riderIdExists(id):
        connection = s.connect("foodSystem.db")
        cursor = connection.cursor()
        riderCountList = cursor.execute(
            f"SELECT COUNT(*) FROM Riders WHERE rider_id = {id}").fetchone()
        return int(''.join([str(n) for n in riderCountList])) == 1

    @staticmethod
    def deleteRider(id):
        connection = s.connect("foodSystem.db")
        cursor = connection.cursor()
        cursor.execute("pragma foreign_keys=on")
        cursor.execute("BEGIN TRANSACTION")
        try:
            cursor.execute(f"DELETE FROM Riders WHERE rider_id = {id}")
            connection.commit()
        except:
            connection.rollback()
        connection.close()

    @staticmethod
    def checkIfRiderAlreadyExistForLogin(Useremail_rider, Userpassword_rider):
        connection = s.connect("foodSystem.db")
        cursor = connection.cursor()
        Riders = cursor.execute("SELECT * from Riders")
        for rider in Riders:
            if (Useremail_rider and Userpassword_rider) in rider:
                return True
        return False

    @staticmethod
    def checkIfRiderAlreadyExistForSignUp(Useremail, Userpassword):
        connection = s.connect("foodSystem.db")
        cursor = connection.cursor()
        Riders = cursor.execute("SELECT * from Riders")
        for rider in Riders:
            if (Useremail and Userpassword) in rider:
                return True
            if (Useremail) in rider:
                return True
        return False

    @staticmethod
    def returnRiderAccordingToSession(email, password):
        connection = s.connect("foodSystem.db")
        cursor = connection.cursor()
        rider = cursor.execute(
            f"SELECT * from Riders where email = '{email}' and password = '{password}'")
        return rider

    @staticmethod
    def returnRider():
        connection = s.connect("foodSystem.db")
        cursor = connection.cursor()
        riders = cursor.execute("SELECT * from Riders")
        return riders


############################################################################################################################################
    
    @staticmethod
    def CreateTableFood():
        connection = s.connect("foodSystem.db")
        cursor = connection.cursor()
        cursor.execute('''
        CREATE TABLE Food
    (
        food_no          INTEGER PRIMARY KEY AUTOINCREMENT ,
        food_image       VARCHAR(300) ,
        food_price       int,
        food_title       VARCHAR (100) ,
        food_description VARCHAR (500) ,
        admin_id         int NOT NULL,
        FOREIGN KEY (ADMIN_ID) REFERENCES ADMIN(ADMIN_ID)
    )

        ''')
        connection.commit()
        connection.close()
 
    @staticmethod
    def InsertIntoFood(img, price, title, desc, admin_id):
        connection = s.connect("foodSystem.db")
        cursor = connection.cursor()
        cursor.execute("pragma foreign_keys=on")
        cursor.execute("BEGIN TRANSACTION")
        try:
            cursor.execute('''
            INSERT INTO Food(food_image,food_price,food_title,food_description,admin_id) VALUES
            (?, ?, ?, ?, ?)
            ''', (img, price, title, desc, admin_id))
            connection.commit()
        except s.Error as e:
            print(f"Error inserting food item: {e}")
            connection.rollback()
        connection.close()

    @staticmethod
    def deleteFood(id):
        connection = s.connect("foodSystem.db")
        cursor = connection.cursor()
        cursor.execute("pragma foreign_keys=on")
        cursor.execute("BEGIN TRANSACTION")
        try:
            cursor.execute(f"DELETE FROM Food WHERE food_no = {id}")
            connection.commit()
        except:
            connection.rollback()
        connection.close()

    @staticmethod
    def updateFood(id, title, price, desc, img):
        connection = s.connect("foodSystem.db")
        cursor = connection.cursor()
        cursor.execute("pragma foreign_keys=on")
        cursor.execute("BEGIN TRANSACTION")
        try:
            cursor.execute(
                f"UPDATE FOOD SET food_title = '{title}' WHERE food_no = {id}")
            
            cursor.execute(
                f"UPDATE FOOD SET food_price = '{price}' WHERE food_no = {id}")
            
            cursor.execute(
                f"UPDATE FOOD SET food_description = '{desc}' WHERE food_no = {id}")
            
            cursor.execute(
                f"UPDATE FOOD SET food_image = '{img}' WHERE food_no = {id}")
            connection.commit()

        except:
            connection.rollback()
        connection.close()

    @ staticmethod
    def FoodsFilterBy(filter):
        connection = s.connect("foodSystem.db")
        cursor = connection.cursor()
        foods = cursor.execute("SELECT * FROM Food ORDER BY " + filter)
        return foods

    @ staticmethod
    def returnFoodById(id):
        connection = s.connect("foodSystem.db")
        cursor = connection.cursor()
        food = cursor.execute(f"SELECT * FROM Food WHERE food_no = {id}")
        return food

    @ staticmethod
    def foodIdExists(id):
        connection = s.connect("foodSystem.db")
        cursor = connection.cursor()
        foodcountList = cursor.execute(
            f"SELECT COUNT(*) FROM Food WHERE food_no = {id}").fetchone()
        return int(''.join([str(n) for n in foodcountList])) == 1

    @ staticmethod
    def returnFoods():
        connection = s.connect("foodSystem.db")
        cursor = connection.cursor()
        foods = cursor.execute("SELECT * from Food")
        return foods

    @staticmethod
    def deleteAllFoods():
        connection = s.connect("foodSystem.db")
        cursor = connection.cursor()
        cursor.execute("pragma foreign_keys=on")
        cursor.execute("BEGIN TRANSACTION")
        try:
            cursor.execute(f"DELETE FROM Food")
            connection.commit()
        except:
            connection.rollback()
        connection.close()

    @ staticmethod
    def CreateTableORDERED():
        connection = s.connect("foodSystem.db")
        cursor = connection.cursor()
        cursor.execute('''
    CREATE TABLE Ordered (
        Order_Id        INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_id	    int NOT NULL,
        food_no	        int NOT NULL,
        pay_id	        int NOT NULL,
        ordered_date	TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        quantity	    int DEFAULT 0,
        pay_amount	    int NOT NULL CHECK("pay_amount" > 0),
        order_status    VARCHAR(10) default 'Pending' CHECK(order_status='Pending' OR order_status='Delivered'),    
        FOREIGN KEY(pay_id) REFERENCES Payment(pay_id) on delete set NULL,
        FOREIGN KEY(food_no) REFERENCES FOOD(food_no) on delete cascade,
        FOREIGN KEY(customer_id) REFERENCES CUSTOMERS(customer_id) on delete cascade
    )
        ''')
        connection.commit()
        connection.close()


    @staticmethod
    def InsertIntoORDERED(customerId, foodno, quantity, payId, pay_amount):
        connection = s.connect("foodSystem.db")
        cursor = connection.cursor()
        cursor.execute("pragma foreign_keys=on")
        try:
            cursor.execute('''
            INSERT INTO ORDERED(customer_id,food_no,quantity,pay_id, pay_amount) VALUES
            (?, ?, ?, ?, ?)
            ''', (customerId, foodno, quantity, payId, pay_amount))
            cursor.execute("ROLLBACK TO SAVEPOINT restart_from_payment")
            connection.commit()
        except:
            cursor.execute("ROLLBACK TO SAVEPOINT restart_from_payment")
        connection.close()

    @staticmethod
    def updateOrderStatusToDelivered(order_id):
        connection = s.connect("foodSystem.db")
        cursor = connection.cursor()
        cursor.execute("pragma foreign_keys=on")
        try:
            cursor.execute(f"UPDATE ORDERED SET order_status = 'Delivered' where Order_Id = {order_id}")
            connection.commit()
        except:
            connection.rollback()
        connection.close()

    @staticmethod
    def deleteOrderWithOrderId(order_id):
        connection = s.connect("foodSystem.db")
        cursor = connection.cursor()
        cursor.execute("pragma foreign_keys=on")
        try:
            cursor.execute(f"delete from ORDERED where Order_Id = {order_id}")
            connection.commit()
        except:
            connection.rollback()
        connection.close()

    @staticmethod
    def returnOrderDetailsOfCustomerWithJoins(customerId):
        connection = s.connect("foodSystem.db")
        cursor = connection.cursor()
        orderDetails = cursor.execute(f'''
        SELECT ORDERED.Order_ID, FOOD.food_title, FOOD.food_price, FOOD.food_image, ORDERED.ordered_date,
        ORDERED.quantity, ORDERED.pay_amount, Payment.pay_number, ORDERED.order_status FROM ORDERED
        INNER JOIN CUSTOMERS
        ON ORDERED.customer_id = CUSTOMERS.customer_id
        INNER JOIN PAYMENT
        ON ORDERED.pay_id = PAYMENT.pay_id
        INNER JOIN FOOD
        ON ORDERED.food_no = FOOD.food_no
        where CUSTOMERS.customer_id = '{customerId}'
        order by ORDERED.Order_ID DESC
        ''')
        return orderDetails

    @staticmethod
    def returnAllOrderDetailsOfCustomerWithJoins():
        connection = s.connect("foodSystem.db")
        cursor = connection.cursor()
        orderDetails = cursor.execute(f'''
        SELECT Customers.first_name, Customers.last_name, ORDERED.Order_ID, FOOD.food_title, FOOD.food_price, FOOD.food_image, ORDERED.ordered_date,
        ORDERED.quantity, ORDERED.pay_amount, Payment.pay_number, ORDERED.order_status FROM ORDERED
        INNER JOIN CUSTOMERS
        ON ORDERED.customer_id = CUSTOMERS.customer_id
        INNER JOIN PAYMENT
        ON ORDERED.pay_id = PAYMENT.pay_id
        INNER JOIN FOOD
        ON ORDERED.food_no = FOOD.food_no
        order by ORDERED.Order_ID DESC
        ''')
        return orderDetails

    @ staticmethod
    def OrderIdExists(id):
        connection = s.connect("foodSystem.db")
        cursor = connection.cursor()
        OrderCountList = cursor.execute(
            f"SELECT COUNT(*) FROM Ordered WHERE Order_ID = {id}").fetchone()
        return int(''.join([str(n) for n in OrderCountList])) == 1

    @ staticmethod
    def returnORDERED():
        connection = s.connect("foodSystem.db")
        cursor = connection.cursor()
        ORDERED = cursor.execute("SELECT * from ORDERED")
        return ORDERED
#############################################################################################
    @ staticmethod
    def CreateTablePayment():
        connection = s.connect("foodSystem.db")
        cursor = connection.cursor()
        cursor.execute('''
        CREATE TABLE PAYMENT
    (
        pay_id                INTEGER PRIMARY KEY AUTOINCREMENT,
        pay_number            VARCHAR (15),
        customer_id           INT NOT NULL,
        FOREIGN KEY(customer_id) REFERENCES CUSTOMERS(customer_id) on delete cascade
    )
        ''')

        connection.commit()
        connection.close()

    # @staticmethod
    # def InsertIntoPayment(number, customer_id): #where customer_id = 1 last row id only
    #     connection = s.connect('foodSystem.db')
    #     cursor = connection.cursor()
    #     cursor.execute("pragma foreign_keys=on")
    #     cursor.execute("BEGIN TRANSACTION")
    #     cursor.execute("SAVEPOINT restart_from_payment")
    #     try:
    #         cursor.execute(f'''
    #         insert into PAYMENT (pay_number, customer_id)
    #         select '{number}', '{customer_id}'
    #         where not EXISTS (SELECT 1 from PAYMENT p where (p.customer_id <> {customer_id} or p.customer_id = {customer_id}) and p.pay_number = '{number}')
    #         ''')
    #         already = cursor.execute(f'''
    #         SELECT 'already'
    #         where EXISTS (SELECT 1 from PAYMENT p where p.customer_id <> {customer_id} and p.pay_number = '{number}')  
    #         ''')
    #         connection.commit()
    #     except:
    #         connection.rollback()
    #     cursor2 = connection.cursor()
    #     pay_id = cursor2.execute(f"SELECT pay_id from payment where pay_number = '{number}' and customer_id = {customer_id} limit 1")

    #     return already, pay_id

    @staticmethod
    def insertIntoPaymentThenOrders(number, customer_id, foodno, quantity, pay_amount):
        connection = s.connect('foodSystem.db')
        # cursor = connection.cursor()
        connection.execute("pragma foreign_keys=on")
        connection.execute("BEGIN TRANSACTION")
        try:
            connection.execute(f'''
            insert into PAYMENT (pay_number, customer_id)
            select '{number}', '{customer_id}'
            where not EXISTS (SELECT 1 from PAYMENT p where (p.customer_id <> {customer_id} or p.customer_id = {customer_id}) and p.pay_number = '{number}')
            ''')
            already = connection.execute(f'''
            SELECT 'already'
            where EXISTS (SELECT 1 from PAYMENT p where p.customer_id <> {customer_id} and p.pay_number = '{number}')  
            ''')
            connection.commit()
            # cursor2 = connection.cursor()
            pay_id = connection.execute(f"SELECT pay_id from payment where pay_number = '{number}' and customer_id = {customer_id} limit 1")
            StorePay_id = pay_id.fetchone()
            StoreAlready = already.fetchone()
            
            if StoreAlready == None:
                # cursor2 = connection.cursor()
                connection.execute("pragma foreign_keys=on")
                connection.execute('''
                INSERT INTO ORDERED(customer_id,food_no,quantity,pay_id, pay_amount) VALUES
                (?, ?, ?, ?, ?)
                ''', (customer_id, foodno, quantity, StorePay_id[0], pay_amount))
                connection.commit()
            return StoreAlready, StorePay_id
        except s.Error as e:
            print(e.with_traceback)
            connection.rollback()

    @ staticmethod
    def CreateTableReviews():
        connection = s.connect("foodSystem.db")
        cursor = connection.cursor()
        cursor.execute('''
        CREATE TABLE Reviews
    (
        review_id             INTEGER PRIMARY KEY AUTOINCREMENT,
        review_rate           DECIMAL (2,2) NOT NULL,
        review_description    VARCHAR (500) NOT NULL,
        Order_ID              int NOT NULL UNIQUE,
        FOREIGN KEY (Order_ID) REFERENCES ORDERED(Order_ID) ON DELETE CASCADE
    )
        ''')

        connection.commit()
        connection.close()
    @staticmethod
    def InsertIntoReviews(rate, revDesc, ord_id):
        connection = s.connect("foodSystem.db")
        cursor = connection.cursor()
        cursor.execute("pragma foreign_keys=on")
        cursor.execute("BEGIN TRANSACTION")
        try:
            cursor.execute('''
            INSERT INTO Reviews(review_rate, review_description, Order_ID) VALUES
            (?, ?, ?)
            ''', (rate, revDesc, ord_id))
            connection.commit()
        except s.IntegrityError as error:
            print("Can't insert more reviews for 1 customer", error)
            connection.close()
            return False
        except s.Error as error:
            print("There is a problem while insertion, rolling back.", error)
            connection.rollback()
        # connection.commit()
        # lastId = cursor.lastrowid
        connection.close()
        return True
        # return lastId

    @staticmethod
    def returnAllReviewsOfFood_noWithJoins(food_no):
        connection = s.connect("foodSystem.db")
        cursor = connection.cursor()
        reviews = cursor.execute(f'''
            SELECT c.first_name, c.last_name, r.review_rate, r.review_description from Reviews r
            inner join Ordered o
            on o.Order_Id = r.Order_Id
            INNER join Customers c
            on o.customer_id = c.customer_id
            inner join Food f
            on o.food_no = f.food_no
            where f.food_no = '{food_no}'
        ''')
        return reviews

    @staticmethod
    def returnAllReviewsRatesAndFood_nos():
        connection = s.connect("foodSystem.db")
        cursor = connection.cursor()
        reviews = cursor.execute(f'''
            SELECT f.food_no, avg(r.review_rate), count(*) from Reviews r
            inner join Ordered o
            on o.Order_Id = r.Order_Id
            INNER join Customers c
            on o.customer_id = c.customer_id
            inner join Food f
            on o.food_no = f.food_no
            GROUP by f.food_no
        ''')
        return reviews

    @staticmethod
    def returnReviewsOfFood_noWithJoins(food_id):
        connection = s.connect("foodSystem.db")
        cursor = connection.cursor()
        reviews = cursor.execute(f'''
            SELECT avg(r.review_rate), count(*) from Reviews r
            inner join Ordered o
            on o.Order_Id = r.Order_Id
            INNER join Customers c
            on o.customer_id = c.customer_id
            inner join Food f
            on o.food_no = f.food_no
            GROUP by f.food_no
            having f.food_no = '{food_id}'
        ''')
        return reviews

    @staticmethod
    def FoodsFilterByOrderRatings():
        connection = s.connect("foodSystem.db")
        cursor = connection.cursor()
        foods = cursor.execute('''
            SELECT f.food_no, f.food_image, f.food_price,f.food_title, f.food_description, f.admin_id
            from Food f left join Ordered o
            on f.food_no = o.food_no
            left join Reviews r
            on r.Order_Id = o.Order_Id
            group by f.food_no
            order by avg(review_rate) desc;
        ''')
        return foods

    @ staticmethod
    def returnTable(table):
        connection = s.connect("foodSystem.db")
        cursor = connection.cursor()
        tableTuples = cursor.execute(f"SELECT * from {table}")
        return tableTuples

    @staticmethod
    def testing(number,customer_id):
        connection = s.connect("foodSystem.db")
        cursor = connection.cursor()
        cursor.execute('''
        INSERT INTO Payment(pay_number, customer_id) VALUES
        (?, ?)
        ''', (number, customer_id))
        connection.commit()
        pay_id = cursor.execute(f"SELECT pay_id from payment where pay_number = '{number}' and customer_id = '{customer_id}'")
        cursor2 = connection.cursor()
        count = cursor2.execute("select count(*) from payment")
        return pay_id, count

    # @staticmethod
    # def testing2(number,customer_id):
    #     connection = s.connect("foodSystem.db")
    #     cursor = connection.cursor()
    #     cursor.execute(f'''
    #     insert into PAYMENT (pay_number, customer_id)
    #     select {number}, {customer_id}
    #     where not EXISTS (SELECT 1 from PAYMENT p where (p.customer_id <> {customer_id} or p.customer_id = {customer_id}) and p.pay_number = {number})
    #     ''')
    #     already = cursor.execute(f'''
    #     SELECT 'User with this  already exists'
    #     where EXISTS (SELECT 1 from PAYMENT p where p.customer_id <> {customer_id} and p.pay_number = {number})  
    #     ''')
    #     connection.commit()
    #     cursor2 = connection.cursor()
    #     pay_id = cursor2.execute(f"SELECT pay_id from payment where pay_number = {number} and customer_id = {customer_id} limit 1")

    #     return already, pay_id






        
