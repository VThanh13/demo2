import math
from typing import Union

from flask import render_template, request, session, jsonify, url_for, abort
import hashlib
from flask_login import login_user, logout_user
from app.models import User
from app import *
from admin import *
import utils
import cloudinary
import cloudinary.uploader
import stripe
from sqlalchemy import *
stripe.api_key = app.config['STRIPE_SECRET_KEY']

@app.route("/")
def home():
    flights = utils.get_flight()
    flight_filter = utils.get_flight_filter(kw1=request.args.get("kw1"),
                                  kw2=request.args.get("kw2"),
                                  page=int(request.args.get("page", 1)))
    count = utils.count_flight()
    size = app.config["PAGE_SIZE"]
    return render_template("pages_user/home.html",
                           flights=flights,
                           flights_filter=flight_filter,
                           page_num=math.ceil(count/size))
@app.route("/search")
def search():
    flights = utils.get_flight()
    flight_filter = utils.get_flight_filter(kw1=request.args.get("kw1"),
                                  kw2=request.args.get("kw2"),
                                  page=int(request.args.get("page", 1)))
    count = utils.count_flight()
    size = app.config["PAGE_SIZE"]
    return render_template("pages_user/home.html",
                           flights=flights,
                           flights_filter=flight_filter,
                           page_num=math.ceil(count/size))

@app.route("/login", methods =['get', 'post'])
def normal_user_login():
    error_message = ""
    if request.method == 'POST':
        username = request.form.get("username")
        password = request.form.get("password")
        password = str(hashlib.md5(password.encode("utf-8")).digest())
        user = User.query.filter(and_(User.username == username,
                                 User.password == password,
                                 User.role == 'USER')).first()
        if user:  # dang nhap thanh cong
            login_user(user)
            return redirect(request.args.get("next", "/"))
        else:
            error_message = "Tài khoản hoặc mật khẩu không chính xấc hoặc không có quyền truy cập"
    return render_template("pages_user/login_user.html", error_message=error_message)

@app.route("/logout")
def normal_user_logout():
    logout_user()

    return redirect("/login")

@app.route("/register", methods=['post', 'get'])
def register():
    err_message =""
    if request.method == 'POST':
        try:
            fullname = request.form["fullname"]
            username = request.form["username"]
            password = request.form["password"]
            confirm_password = request.form["confirm_password"]
            birthday = request.form["birthday"]
            email = request.form["email"]
            identify = request.form["identify"]
            phone = request.form["phone"]
            if password.strip() == confirm_password.strip():
                avartar = request.files["avatar"]
                data = request.form.copy()
                del data['confirm_password']
                if avartar:
                    info = cloudinary.uploader.upload(avartar)
                    data["avatar"] = info["secure_url"]
                if utils.check_user(username):
                    if utils.add_user(**data):
                        return redirect("/login")
                    else:
                        err_message = "Dữ liệu vào có lỗi"
                else:
                   err_message = "Tài khoản đã tồn tại. Vui lòng nhập lại"
            else:
                err_message = "Mật khẩu không khớp. Vui lòng nhập lại"
        except :
            err_message = "Hệ thống đang có lỗi. Vui lòng thử lại sau"
    return render_template("pages_user/register.html", error_message=err_message)


@app.route("/user")
def get_user():
    getuser = utils.get_user_byid(userid=request.args.get("id"))
    show_transact = utils.show_and_cancel_ticket(userid=request.args.get("id"))

    return render_template("pages_user/profile.html",
                           user=getuser,
                           show_transact=show_transact)

@app.route("/cancel")
def cancel():
    utils.cancel(invoice_id=request.args.get("id"))
    return redirect("/user?id=" + str(current_user.id))

@my_login.user_loader
def user_load(user_id):
    return User.query.get(user_id)

@app.route("/user-edit")
def change_info_user():
    return render_template("pages_user/change-info-user.html")

@app.route("/user-load-update", methods=["post", "get"])
def load_update():
    success_message = ""
    err_message = ""
    if request.method == 'POST':
        try:
            fullname = request.form["fullname"]
            email = request.form["email"]
            birthday = request.form["birthday"]
            identify = request.form["identify"]
            phone = request.form["phone"]
            if utils.update_user(fullname, email, birthday, identify, phone, current_user.id):
                success_message = "Thổi thành công"
            else:
                err_message = "Dữ liệu vào có lỗi"
        except Exception as e:
            print("ERROR: " + str(e))
    return render_template("pages_user/change-info-user.html",
                           error_message=err_message,
                           success_message=success_message)

@app.route("/user-pw", methods=["post", "get"])
def change_pw_user():
    getuser = utils.get_user_byid(userid=request.args.get("id"))
    return render_template("pages_user/change-pw-user.html", user=getuser)

@app.route("/user-update-pw", methods=["post","get"])
def user_update_pw():
    err_message = ""
    success_message = ""
    if request.method == 'POST':
        try:
            password = request.form["password"]
            new_password = request.form["new_password"]
            confirm_password = request.form["confirm_password"]
            if utils.check_password_user(password, current_user.id):
                if new_password.strip() == confirm_password.strip():
                    if utils.update_password(new_password, current_user.id):
                        success_message = "Đổi mật khẩu thành công"
                    else:
                        err_message = "Dữ liệu vào có lỗi"
                else:
                    err_message = "Mật khẩu mới không khớp. Vui lòng nhập lại"
            else:
                err_message = "Mật khẩu cũ không đúng. Vui lòng nhập lại"
        except:
            err_message = "Hệ thống đang có lỗi. Vui lòng thử lại sau"
    return render_template("pages_user/change-pw-user.html",
                           error_message=err_message,
                           success_message=success_message)

@app.route("/flight")
def get_flight():
    get_flight = utils.get_flight_byid(flight_id=request.args.get("flight"),
                                        type_id=request.args.get("type"))
    getall_flight = utils.get_flight()
    return render_template("pages_user/flight-cart.html",
                           get_flight=get_flight,
                           getall_flight=getall_flight)

@app.route("/cart")
def cart():
    return render_template('pages_user/cart.html')


@app.route("/flight-cart")
def index():
    get_flight = utils.get_flight_cart(flight_id=request.args.get("id"))
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price': 'price_1JxntREMDYePyYSgIwLtqYJa',
            'quantity': 1,
        }],
        mode='payment',
        success_url=url_for('thanks', _external=True) + '?session_id={CHECKOUT_SESSION_ID}',
        cancel_url=url_for('index', _external=True),
    )
    return render_template(
        'pages_user/cart.html',
        checkout_session_id=session['id'],
        checkout_public_key=app.config['STRIPE_PUBLIC_KEY'],
        get_flight=get_flight
    )


@app.route('/stripe_pay')
def stripe_pay():
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price': 'price_1JxntREMDYePyYSgIwLtqYJa',
            'quantity': 1,
        }],
        mode='payment',
        success_url=url_for('thanks', _external=True) + '?session_id={CHECKOUT_SESSION_ID}',
        cancel_url=url_for('index', _external=True),
    )
    return {
        'checkout_session_id': session['id'],
        'checkout_public_key': app.config['STRIPE_PUBLIC_KEY']
    }

@app.route('/thanks')
def thanks():
    return render_template('pages_user/cart.html')

@app.route('/stripe_webhook', methods=['POST'])
def stripe_webhook():
    print('WEBHOOK CALLED')

    if request.content_length > 1024 * 1024:
        print('REQUEST TOO BIG')
        abort(400)
    payload = request.get_data()
    sig_header = request.environ.get('HTTP_STRIPE_SIGNATURE')
    endpoint_secret = 'YOUR_ENDPOINT_SECRET'
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        print('INVALID PAYLOAD')
        return {}, 400
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        print('INVALID SIGNATURE')
        return {}, 400

    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        print(session)
        line_items = stripe.checkout.Session.list_line_items(session['id'], limit=1)
        print(line_items['data'][0]['description'])

    return {}


@app.route("/admin/login", methods=['post'])
def login_exe():
    username = request.form.get("username")
    password = request.form.get("password")
    password = str(hashlib.md5(password.encode("utf-8")).digest())
    user = User.query.filter(and_(User.username == username,
                             User.password == password,
                             User.role == 'ADMIN')).first()
    if user: # dang nhap thanh cong
        login_user(user)

    return redirect("/admin")



@app.route("/api/add-item-cart", methods=['post'])
def add_to_cart():
    cart = session.get(CART_KEY)
    if not cart:
        cart = {}

    data = request.json

    ticket_id = str(data["ticket_id"])

    if ticket_id in cart: # san pham da tung bo vao gio
        p = cart[ticket_id]
        p['quantity'] = p['quantity'] + 1
    else: # san pham chua bo vao gio
        cart[ticket_id] = {
            "flight_id": data["flight_id"],
            "type_id": data["type_id"],
            "type_name": data["type_name"],
            "from": data["from"],
            "to": data["to"],
            "date_start": data["date_start"],
            "time_start": data["time_start"],
            "ticket_id": data["ticket_id"],
            "price": data["price"],
            "price_service": data["price_service"],
            "price_total": data["price_total"],
            "quantity": 1
        }

    session[CART_KEY] = cart

    return jsonify(utils.cart_stats(cart))


@app.route("/api/update-cart-item", methods=['put'])
def update_cart_item():
    cart = session.get(CART_KEY)

    if cart:
        data = request.json
        try:
            ticket_id = str(data['ticket_id'])
            quantity = data['quantity']
        except Union[IndexError, KeyError] as ex:
            print(ex)
        else:
            if ticket_id in cart:
                p = cart[ticket_id]
                p['quantity'] = quantity
                session[CART_KEY] = cart

                return jsonify({
                    "error_code": 200,
                    "cart_stats": utils.cart_stats(cart)
                })

    return jsonify({
        "error_code": 404
    })


@app.route("/api/delete-cart-item/<ticket_id>", methods=['delete'])
def delete_cart_item(ticket_id):
    cart = session.get(CART_KEY)
    if cart:
        if ticket_id in cart:
            del cart[ticket_id]
            session[CART_KEY] = cart

            return jsonify({
                "error_code": 200,
                "cart_stats": utils.cart_stats(cart)
            })

    return jsonify({
        "error_code": 404
    })

@app.route('/api/pay', methods=['post'])
def pay():
    cart = session.get(CART_KEY)
    if cart:
        if utils.add_invoice(cart):
            del session[CART_KEY]
            return jsonify({
                "error_code": 200
            })
    return jsonify({
        "error_code": 404
    })
#
#
# @app.route('/upload', methods=['post'])
# def upload():
#     avatar = request.files.get("avatar")
#     if avatar:
#         avatar.save("%s/static/images/%s" % (app.root_path, avatar.filename))
#         return "SUCCESSFUL"
#
#     return "FAILED"



# NHAN VIEN
@app.route("/staff-login", methods =['get', 'post'])
def staff_login():
    error_message = ""
    if request.method == 'POST':
        username = request.form.get("username")
        password = request.form.get("password")
        password = str(hashlib.md5(password.encode("utf-8")).digest())
        user = User.query.filter(and_(User.username == username,
                                  User.password == password,
                                  User.role == 'STAFF')).first()
        if user:  # dang nhap thanh cong
            login_user(user)
            return redirect("/staff")
        else:
            error_message = "Tài khoản hoặc mật khẩu không chính xác hoặc không có quyền truy cập"
    return render_template("pages_staff/signin.html", error_message=error_message)

@app.route("/staff-logout")
def staff_logout():
    logout_user()
    return redirect("/staff-login")

@app.route("/staff")
def staff_index():
    if current_user.is_authenticated:
        return render_template("pages_staff/index.html")
    else:
        return redirect("/staff-login")

@app.route("/staff-show")
def staff_get_flight():
    get_flight1 = utils.staff_get_flight_filter(kw1=request.args.get("kw1"),
                                  kw2=request.args.get("kw2"),
                                         kw3=request.args.get("kw3"))
    print(request.args.get("kw1"), request.args.get("kw2"), request.args.get("kw3"))
    return render_template("pages_staff/gallery.html",
                           get_flight=get_flight1)


@app.route("/staff-flight")
def show_fight():
    get_flight = utils.get_flight_byid(arg=request.args.get("id"))

    return render_template("pages_staff/ticket.html", get_flight=get_flight)

@app.route("/staff-cart",methods=["get","post"])
def staff_cart():
    if request.method == 'POST':
        get_customer = utils.staff_show_customer(fullname=request.form.get("fullname"),
                                                 identify=request.form.get("identify"),
                                                 phone=request.form.get("phone"))
    return render_template("pages_staff/staff_cart.html", get_customer=get_customer)
@app.route("/staff-register-user", methods=["post","get"])
def staff_register():
    err_message = ""
    flag = False

    if request.method == 'POST':
        try:
            fullname = request.form["fullname"]
            birthday = request.form["birthday"]
            email = request.form["email"]
            identify = request.form["identify"]
            phone = request.form["phone"]
            data = request.form.copy()
            if utils.add_user(**data):
                flag = True
                return redirect("/staff-register-user")
            else:
                err_message = "Dữ liệu vào có lỗi"
        except:
            err_message = "Hệ thống đang có lỗi. Vui lòng thử lại sau"
    return render_template("pages_staff/register.html", error_message=err_message, flag=flag)


@app.route("/staff-check-user", methods=["post","get"])
def checkuser():

    if request.method == 'POST':
        get_user_info = utils.staff_check_user(fullname=request.form.get("fullname"),
                                       identify=request.form.get("identify"))
        return render_template("pages_staff/customer.html", get_user=get_user_info)
    elif request.method == 'GET':
        return render_template("pages_staff/customer.html")

@app.route("/staff-delete-customer")
def staff_delete():
    err_message = ""
    success_message = ""
    if utils.staff_delete_user(request.args.get("id")):
        success_message = "Xóa thành công"
    else:
        err_message = "Xóa thất bại"
    return render_template("pages_staff/customer.html",
                           err_message=err_message,
                           success_message=success_message)

@app.route("/staff-load-customer")
def test():
    user = utils.get_user_byid(request.args.get("id"))
    return render_template("/pages_staff/edit_customer.html", user=user)


@app.route("/staff-edit-customer", methods=["post"])
def staff_edit_customer():
    fullname = request.form["fullname"]
    email = request.form["email"]
    birthday = request.form["birthday"]
    identify = request.form["identify"]
    phone = request.form["phone"]
    utils.staff_update_user(fullname=fullname, email=email, birthday=birthday, identify=identify, phone=phone)
    return redirect("/staff-check-user")

@app.route('/staff/api/pay', methods=['post'])
def staff_pay():

    cart = session.get(CART_KEY)
    if cart:
        if utils.staff_add_invoice(cart):
            del session[CART_KEY]
            return jsonify({
                "error_code": 200
            })
    return jsonify({
        "error_code": 404
    })



if __name__ == '__main__':
    app.run(debug=True)


