from flask import Flask, render_template, redirect, request, url_for, session, abort
import os
from werkzeug.utils import secure_filename
from database import Database
db = Database()


def checkAppropriateFile(file):
    ALLOWED_EXTENSIONS = ['png', 'jpg', 'jpeg']
    for f in ALLOWED_EXTENSIONS:
        if file.endswith(f):
            return True
    return False


#db.CreateTableAdmin()
#db.insertIntoAdmin(1, 'xyz@gmail.com', 'cat1234')
#db.CreateTablePayment()
#db.CreateTableCustomer()
#db.CreateTableFood()
#db.CreateTableORDERED()
#db.CreateTableReviews()
#db.CreateTableRider()

app = Flask(__name__)
app.secret_key = '7457hhhyuft26442'

app.config['UPLOAD_FOLDER'] = 'static/images'


@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if "Useremail" and "Userpassword" not in session:
        if request.method == 'POST':
            first_name = request.form['first_name']
            last_name = request.form['last_name']
            username = request.form['username']
            Useremail = request.form['Useremail']
            Userpassword = request.form['Userpassword']
            phone = request.form['phone']
            address = request.form['address']

            session['first_name'] = first_name
            session['last_name'] = last_name
            session['username'] = username
            session['Useremail'] = Useremail
            session['Userpassword'] = Userpassword
            session['phone'] = phone
            session['address'] = address

            check = db.checkIfCustomerAlreadyExistForSignUp(Useremail, Userpassword)
            if not check:
                db.insertIntoCustomer(
                    first_name, last_name, username, Useremail, Userpassword, phone, address)
                return redirect(url_for('home'))
            else:
                session.pop('Useremail', None)
                session.pop('Userpassword', None)
                return render_template('signup.html', flag=True)
        else:
            return render_template('signup.html')
    return redirect(url_for('home'))


@app.route('/login', methods=['POST', 'GET'])
def login():
    if "Useremail" and "Userpassword" not in session:
        if request.method == 'POST':
            Useremail = request.form['Useremail']
            Userpassword = request.form['Userpassword']
            session["Useremail"] = Useremail
            session["Userpassword"] = Userpassword
            # we can not pass values withouot confirming that user is in the session so
            # return render_template("admin.html", email=email, password=password)
            check = db.checkIfCustomerAlreadyExistForLogin(Useremail, Userpassword)
            if (check == True):
                return redirect(url_for('home'))
            else:
                session.pop("Useremail", None)
                session.pop("Userpassword", None)
                return render_template("login.html", flag=True)
        else:
            return render_template("login.html")
    else:
        return redirect(url_for('home'))


@app.route('/')
def frontPage():
    return render_template('frontPage.html')


@app.route('/home')
def home():
    if "Useremail" and "Userpassword" in session:
        return render_template('home.html')
    return redirect(url_for('login'))


@app.route('/menu')
def menu():
    if "Useremail" and "Userpassword" in session:
        foods = db.returnFoods()
        foods = foods.fetchall()

        foodnosAndRates = db.returnAllReviewsRatesAndFood_nos()
        foodnosAndRates = foodnosAndRates.fetchall()

        return render_template("menu.html", foods=foods, foodnosAndRates=foodnosAndRates)
    return redirect(url_for('login'))


@app.route('/account')
def account():
    if "Useremail" and "Userpassword" in session:
        useremail = session["Useremail"]
        userpassword = session["Userpassword"]
        customer = db.returnCustomerAccordingToSession(useremail, userpassword)
        customer = customer.fetchone()
        return render_template('useraccount.html', customer=customer)
    return redirect(url_for('login'))


@app.route('/menu/<filter>')
def filter(filter):
    if "Useremail" and "Userpassword" in session:
        if filter == 'filterByPrice':
            foods = db.FoodsFilterBy("food_price")
            foods = foods.fetchall()
            foodnosAndRates = db.returnAllReviewsRatesAndFood_nos()
            foodnosAndRates = foodnosAndRates.fetchall()        
            return render_template('menu.html', foods=foods, foodnosAndRates=foodnosAndRates)

        elif filter == 'filterByRating':
            foods = db.FoodsFilterByOrderRatings()
            foods = foods.fetchall()
            foodnosAndRates = db.returnAllReviewsRatesAndFood_nos()
            foodnosAndRates = foodnosAndRates.fetchall()
            return render_template('menu.html', foods=foods, foodnosAndRates=foodnosAndRates)
        return redirect(url_for('menu'))
    return redirect(url_for('login'))

@app.route('/update_orderMarked/<int:or_id>')
def markAsDone(or_id):
    if "email" and "password" in session:
        db.updateOrderStatusToDelivered(or_id)
        return redirect(url_for('allOrders'))
    return redirect(url_for('adminLogin'))

@app.route('/remove_order/<int:or_id>')
def removeOrder(or_id):
    if "email" and "password" in session:
        db.deleteOrderWithOrderId(or_id)
        return redirect(url_for('allOrders'))
    return redirect(url_for('adminLogin'))

@app.route('/menu/customer_orders')
def orderDetails(flag=None):
    if "Useremail" and "Userpassword" in session:
        useremail = session["Useremail"]
        userpassword = session["Userpassword"]
        customer = db.returnCustomerAccordingToSession(useremail, userpassword)
        customer = customer.fetchone()
        customerId = customer[0]
        orderDetails = db.returnOrderDetailsOfCustomerWithJoins(customerId)
        orderDetails = orderDetails.fetchall()
        getFlag = flag
        return render_template('orderDetails.html', orderDetails=orderDetails, getFlag=getFlag)
    return redirect(url_for('login'))

@app.route('/allcustomer_orders')
def allOrders():
    if "email" and "password" in session:
        orderDetails = db.returnAllOrderDetailsOfCustomerWithJoins()
        orderDetails = orderDetails.fetchall()
        return render_template('AllorderDetails.html', orderDetails=orderDetails)
    return redirect(url_for('adminLogin'))

@app.route('/menu/<int:food_id>', methods=['POST', 'GET'])
def product(food_id):
    if "Useremail" and "Userpassword" in session:
        if request.method == 'POST':
            quantity = request.form['quantity']
            pay_number = request.form['pay_number']
            pay_amount = request.form['pay_amount']
            useremail = session["Useremail"]
            userpassword = session["Userpassword"]
            customer = db.returnCustomerAccordingToSession(useremail, userpassword)
            customer = customer.fetchone()
            customerId = customer[0]

            already, pay_id = db.insertIntoPaymentThenOrders(pay_number,customerId, food_id, quantity, pay_amount)

            if already == None:
                return redirect(url_for('orderDetails', flag=False))
            elif already[0] == 'already' and pay_id == None:
                return render_template('already.html')
            # we can cancel order here so we have to delete those things
            #db.updateCustomerWithPayId(customerId, payId)
        else:
            if db.foodIdExists(food_id):
                food = db.returnFoodById(food_id)
                food = food.fetchone()
                reviewsAndCount = db.returnReviewsOfFood_noWithJoins(food_id)
                reviewsAndCount = reviewsAndCount.fetchone()

                allRevs = db.returnAllReviewsOfFood_noWithJoins(food_id).fetchall()
                return render_template("productdetails.html", food=food, reviewsAndCount=reviewsAndCount, allRevs=allRevs)
            else:
                abort(404)
    return redirect(url_for('login'))

@app.route('/admin/login', methods=['POST', 'GET'])
def adminLogin():
    if "email" and "password" not in session:
        if request.method == 'POST':
            email = request.form['email']
            password = request.form['password']
            session["email"] = email
            session["password"] = password
            # we can not pass values withouot confirming that user is in the session so
            # return render_template("admin.html", email=email, password=password)
            check = db.checkInAdmin(email, password)
            if (check == True):
                return redirect(url_for('admin'))
            else:
                session.pop("email", None)
                session.pop("password", None)
                return render_template("adminLogin.html", flag=True)
        else:
            return render_template("adminLogin.html")
    else:
        return redirect(url_for('admin'))


@app.route('/admin/home')
def admin():
    if "email" and "password" in session:
        foods = db.returnFoods()
        foods = foods.fetchall()
        foodnosAndRates = db.returnAllReviewsRatesAndFood_nos()
        foodnosAndRates = foodnosAndRates.fetchall()
        return render_template('admin.html', foods=foods, foodnosAndRates=foodnosAndRates)
    return redirect(url_for('adminLogin'))


@app.route('/addfood', methods=['POST', 'GET'])
def addFood():
    if "email" and "password" in session:
        if request.method == 'POST':
            foodTitle = request.form['foodTitle']
            foodPrice = request.form['foodPrice']
            foodDesc = request.form['food_desc']
            imageFile = request.files['imageFile']

            if imageFile.filename == '':
                return redirect(request.url)
            if imageFile and checkAppropriateFile(imageFile.filename):
                Securefilename = secure_filename(imageFile.filename)
                imageFile.save(os.path.join(
                    app.config['UPLOAD_FOLDER'], Securefilename))
                db.InsertIntoFood(Securefilename,
                                  foodPrice, foodTitle, foodDesc, 1)
            return redirect(url_for('admin'))
        else:
            return render_template('addFood.html')
    return redirect(url_for("adminLogin"))


@app.route('/delete/<int:id>')
def delFood(id):
    if "email" and "password" in session:
        if db.foodIdExists(id):
            db.deleteFood(id)
            return redirect(url_for('admin'))
        else:
            abort(404)
    return redirect(url_for("adminLogin"))

@app.route('/edit/<int:id>', methods=['POST', 'GET'])
def editFood(id):
    if "email" and "password" in session:
        if db.foodIdExists(id):
            if request.method == 'POST':
                foodTitle = request.form['foodTitle']
                foodPrice = request.form['foodPrice']
                foodDesc = request.form['food_desc']
                imageFile = request.files['imageFile']
                if imageFile.filename == '':
                    return redirect(request.url)
                if imageFile and checkAppropriateFile(imageFile.filename):
                    Securefilename = secure_filename(imageFile.filename)
                    imageFile.save(os.path.join(
                        app.config['UPLOAD_FOLDER'], Securefilename))
                db.updateFood(id, foodTitle, foodPrice, foodDesc, Securefilename)
                return redirect(url_for('admin'))

            food = db.returnFoodById(id)
            food = food.fetchone()
            return render_template('updateFood.html', food=food)
        else:
            abort(404)
    return redirect(url_for("adminLogin"))

@app.route('/deleteall')
def deleteAll():
    if "email" and "password" in session:
        db.deleteAllFoods()
        return redirect(url_for('admin'))
    return redirect(url_for("adminLogin"))

@app.route('/allCustomers')
def allCustomers():
    if "email" and "password" in session:
        customers = db.returnCustomers()
        customers = customers.fetchall()
        return render_template('userdetails.html', customers=customers)
    return redirect(url_for("adminLogin"))

@app.route('/allRiders')
def allRiders():
    if "email" and "password" in session:
        print("entered all riders")
        riders = db.returnRider()
        riders = riders.fetchall()
        return render_template('riderdetails.html', riders= riders)
    return redirect(url_for("adminLogin"))

@app.route('/delRider/<int:id>')
def delRider(id):
    print("reached route del rider")
    if "email" and "password" in session:
        if db.riderIdExists(id):
            print("rider id exists")
            db.deleteRider(id)
            return redirect(url_for('allRiders'))
        else:
            abort(404)
    return redirect(url_for("adminLogin"))

@app.route('/delCustomer/<int:id>')
def delCustomer(id):
    if "email" and "password" in session:
        if db.customerIdExists(id):
            db.deleteCustomer(id)
            return redirect(url_for('allCustomers'))
        else:
            abort(404)
    return redirect(url_for("adminLogin"))

@app.route('/review/<int:order_id>', methods=['POST', 'GET'])
def Review(order_id):
    if "Useremail" and "Userpassword" in session:
        if db.OrderIdExists(order_id):
            if request.method == 'POST':
                review_rate = request.form['review_rate']
                review_desc = request.form['review_desc']

                uflag = db.InsertIntoReviews(review_rate, review_desc, order_id)
                if(uflag==True):
                    return redirect(url_for('orderDetails'))
                else:
                    return render_template('reviewForm.html', order_id = order_id, flag= True)
            else:
                return render_template('reviewForm.html', order_id = order_id)
        else:
            abort(404)
    return redirect(url_for("login"))

@app.route('/menufor_review')
def reviewMenu():
    if "email" and "password" in session:
        foods = db.returnFoods()
        foods = foods.fetchall()
        return render_template('menuForReview.html', foods=foods)
    return redirect(url_for("adminLogin"))

@app.route('/allreviews/<int:food_no>')
def allReviews(food_no):
    if "email" and "password" in session:
        allreviews = db.returnAllReviewsOfFood_noWithJoins(food_no)
        allreviews = allreviews.fetchall()
        reviewsAndCount = db.returnReviewsOfFood_noWithJoins(food_no)
        reviewsAndCount = reviewsAndCount.fetchone()
        return render_template('allReviews.html', allreviews=allreviews, reviewsAndCount=reviewsAndCount)
    return redirect(url_for("adminLogin"))

@app.route('/logout')
def userLogout():
    if "Useremail" and "Userpassword" in session:
        session.pop('Useremail', None)
        session.pop('Userpassword', None)
        return redirect(url_for('frontPage'))
    return redirect(url_for("frontPage"))

@app.route('/admin/logout')
def adminLogout():
    if "email" and "password" in session:
        session.pop('email', None)
        session.pop('password', None)
        return redirect(url_for('frontPage'))
    return redirect(url_for("frontPage"))


#############################################################################################################################################

@app.route('/rider/login', methods=['POST', 'GET'])
def riderLogin():
    session.pop('Rideremail', None)
    session.pop('Riderpassword', None)
    if "Rideremail" and "Riderpassword" not in session:
        if request.method == 'POST':
            Useremail_rider = request.form['Rideremail']
            Userpassword_rider = request.form['Riderpassword']
            session["Rideremail"] = Useremail_rider
            session["Riderpassword"] = Userpassword_rider
            print(Useremail_rider)
            print(Userpassword_rider)
            # we can not pass values withouot confirming that user is in the session so
            # return render_template("admin.html", email=email, password=password)
            check = db.checkIfRiderAlreadyExistForLogin(Useremail_rider, Userpassword_rider)
            if (check == True):
                return redirect(url_for('riderHome'))
            else:
                session.pop("Rideremail", None)
                session.pop("Riderpassword", None)
                return render_template("riderLogin.html", flag=True)
        else:
            return render_template("riderLogin.html")
    else:
        return redirect(url_for('frontPage'))
    
@app.route('/rider/signup', methods=['POST', 'GET'])
def riderSignup():
    if "Rideremail" and "Riderpassword" not in session:
        if request.method == 'POST':
            first_name_rider = request.form['first_name_rider']
            last_name_rider = request.form['last_name_rider']
            username_rider = request.form['username_rider']
            Useremail_rider = request.form['Rideremail']
            Userpassword_rider = request.form['Riderpassword']
            phone_rider = request.form['phone_rider']
            address_rider = request.form['address_rider']

            session['first_name_rider'] = first_name_rider
            session['last_name_rider'] = last_name_rider
            session['username_rider'] = username_rider
            session['Rideremail'] = Useremail_rider
            session['Riderpassword'] = Userpassword_rider
            session['phone_rider'] = phone_rider
            session['address_rider'] = address_rider

            check = db.checkIfRiderAlreadyExistForSignUp(Useremail_rider, Userpassword_rider)
            if not check:
                db.insertIntoRider(
                    first_name_rider, last_name_rider, username_rider, Useremail_rider, Userpassword_rider, phone_rider, address_rider)
                return redirect(url_for('riderHome'))
            else:
                session.pop('Rideremail', None)
                session.pop('Riderpassword', None)
                return render_template('riderSignup.html', flag=True)
        else:
            return render_template('riderSignup.html')
    return redirect(url_for('riderHome'))

@app.route('/rider/home')
def riderHome():
    if "Rideremail" and "Riderpassword" in session:
        return render_template('riderHome.html')
    return redirect(url_for('riderLogin'))

@app.route('/rider/available_orders')
def availableOrders():
    if "Rideremail" and "Riderpassword" in session:
        orderDetails = db.returnAvailableOrders()
        orderDetails = orderDetails.fetchall()
        if orderDetails == []: 
            return render_template('noIssued.html')
        else:
            return render_template('availableOrders.html', orderDetails=orderDetails)
    return redirect(url_for('riderLogin'))

@app.route('/rider/history')
def riderHistory():
    if "Rideremail" and "Riderpassword" in session:
        useremail = session["Rideremail"]
        userpassword = session["Riderpassword"]
        rider = db.returnRiderAccordingToSession(useremail, userpassword)
        rider_id = rider.fetchone()[0]
        orderDetails = db.returnOrderHistory(rider_id)
        print(orderDetails)
        orderDetails = orderDetails.fetchall()
        return render_template('riderHistory.html', orderDetails=orderDetails)
    return redirect(url_for('riderLogin'))

@app.route('/rider/account')
def riderAccount():
    if "Rideremail" and "Riderpassword" in session:
        useremail = session["Rideremail"]
        userpassword = session["Riderpassword"]
        print(useremail)
        print(userpassword)
        rider = db.returnRiderAccordingToSession(useremail, userpassword)
        print(rider)
        print(type(rider))
        rider = rider.fetchone()
        print(rider)
        return render_template('riderAccount.html', rider=rider)
    return redirect(url_for('riderLogin'))

@app.route('/rider/logout')
def riderLogout():
    if "Rideremail" and "Riderpassword" in session:
        session.pop('Rideremail', None)
        session.pop('Riderpassword', None)
        return redirect(url_for('frontPage'))
    return redirect(url_for("frontPage"))

@app.route('/choose_orderMarked/<int:or_id>')
def chooseOrderAsPending(or_id):
    if "Rideremail" and "Riderpassword" in session:
        Rideremail = session["Rideremail"]
        Riderpassword = session["Riderpassword"]
        rider = db.returnRiderAccordingToSession(Rideremail, Riderpassword)
        rider = rider.fetchone()
        db.updateOrderStatusToPending(or_id)
        db.updateRiderId(or_id, rider[0])
        return redirect(url_for('availableOrders'))
    return redirect(url_for('riderLogin'))

@app.route('/update_orderMarked_Rider/<int:or_id>')
def markAsDoneRider(or_id):
    if "Rideremail" and "Riderpassword" in session:
        db.updateOrderStatusToDelivered(or_id)
        return redirect(url_for('riderHistory'))
    return redirect(url_for('riderLogin'))

#############################################################################################################################################

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


if __name__ == "__main__":
    app.run(debug=False)
