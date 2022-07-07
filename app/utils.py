import bdb

from app.models import Flight,DetailFlight ,Invoice,City,Airport,User, TicketType, Ticket, DetailInvoice
from sqlalchemy import asc, func, join, update, and_
from app import *
import hashlib
from flask_login import current_user
import datetime
time = datetime.datetime.now()


def get_flight():
    flights = []
    peter = Flight.query.all()

    for i in peter:
        is_show = False
        airport_from = Airport.query.filter_by(id=i.airport_from_id).first()
        city_from = City.query.filter_by(id=airport_from.id).first()
        airport_to = Airport.query.filter_by(id=i.airport_to_id).first()
        city_to = City.query.filter_by(id=airport_to.id).first()
        airport_sp = []
        if i.airport_support > 0:
            peter1 = DetailFlight.query.filter_by(flight_id=i.id).order_by(asc(DetailFlight.airport_number))
            for j in peter1:
                ap = Airport.query.filter_by(id=j.airport_id)
                for z in ap:
                    airport_sp.append({
                        "fl_id": z.id,
                        "ap_name": z.name,
                        "stt": j.airport_number,
                        "time": j.time_rest
                    })
        if numOfDays(time.date(), i.day_start) >= 1:
            is_show = True
        flights.append({
            "flight_id": i.id,
            "date_start": i.day_start,
            "time_start": i.time_start,
            "from": city_from.name,
            "to": city_to.name,
            "airport_support": airport_sp,
            "price": i.price,
            "image": i.image,
            "active": i.active,
            "is_show": is_show
        })
    return flights[0:5]

def get_flight_filter(kw1=None, kw2=None, page=None):
    flights = []
    flights_filter = []
    flights_filter_has_page = []
    peter = Flight.query.all()
    for i in peter:
        is_show = False
        airport_from = Airport.query.filter_by(id=i.airport_from_id).first()
        city_from = City.query.filter_by(id=airport_from.id).first()
        airport_to = Airport.query.filter_by(id=i.airport_to_id).first()
        city_to = City.query.filter_by(id=airport_to.id).first()
        airport_sp = []
        if i.airport_support > 0:
            peter1 = DetailFlight.query.filter_by(flight_id=i.id).order_by(asc(DetailFlight.airport_number))
            for j in peter1:
                ap = Airport.query.filter_by(id=j.airport_id)
                for z in ap:
                    airport_sp.append({
                        "fl_id": z.id,
                        "ap_name": z.name,
                        "stt": j.airport_number,
                        "time": j.time_rest
                    })
        if numOfDays(time.date(), i.day_start) >= 1:
            is_show = True
        flights.append({
            "flight_id": i.id,
            "date_start": i.day_start,
            "time_start": i.time_start,
            "from": city_from.name,
            "to": city_to.name,
            "airport_support": airport_sp,
            "price": i.price,
            "image": i.image,
            "active": i.active,
            "is_show": is_show
        })

    if kw1 and kw2:
        for i in flights:
            if (kw1 in i.get("from") and kw2 in i.get("to")):
                flights_filter.append(i)
    else:
        flights_filter = flights
    if page:
        size = app.config["PAGE_SIZE"]
        start = (page - 1) * size
        end = start + size
        flights_filter_has_page = flights_filter[start:end]
    return flights_filter_has_page
# print(get_flight_filter())

def check_user(username=None):
    user = User.query.filter(User.username == username).first()
    if user:
        return False
    return True

def get_user_byid (userid=None):
    infoUser = {}
    user = User.query.filter(User.id == userid).first()
    infoUser = {
        "id": user.id,
        "fullname": user.fullname,
        "birthday": user.birthday,
        "email": user.email,
        "identify": user.identify,
        "phone": user.phone,
        "avatar": user.avatar
    }
    return infoUser
# print(get_user_byid(3))

def add_user(fullname=None, username=None, password=None, birthday=None, email=None, identify=None, phone=None, avatar=None):
    if password:
        password = str(hashlib.md5(password.encode("utf-8")).digest())
    user = User(fullname=fullname,
                birthday=birthday,
                email=email,
                identify=identify,
                avatar=avatar,
                phone=phone,
                username=username,
                password=password)
    db.session.add(user)
    try:
        db.session.commit()
        return True
    except:
        return False

def update_user(fullname=None,email= None,birthday=None, identify=None,phone=None,userid=None):
    user = User.query.filter_by(id=userid).first()
    user.fullname = fullname
    user.email = email
    user.birthday = birthday
    user.identify = identify
    user.phone = phone
    db.session.add(user)
    try:
        db.session.commit()
    except Exception as e:
        print("ERROR:" + str(e))
    return True
# update_user("12314","ad123"," 2021-01-21","1231","edad",3)

def check_password_user(password=None, userid=None ):
    password = str(hashlib.md5(password.encode("utf-8")).digest())
    user = User.query.filter(and_(User.password == password, User.id == userid)).first()
    if user:
        return True
    return False

def update_password(new_password=None, userid=None):
    password = str(hashlib.md5(new_password.encode("utf-8")).digest())
    user = User.query.filter_by(id=userid).first()
    user.password = password
    db.session.add(user)
    try:
        db.session.commit()
    except Exception as e:
        print("ERROR: " + str(e))
    return True

def count_flight():
    return Flight.query.count()



def get_flight_byid(flight_id=None, type_id=None):
    flights = []
    flightInfo = []
    service_arg = type_id
    service = TicketType.query.filter_by(name_type=service_arg).first()
    ticket = Ticket.query.all()
    for a in ticket:
        if a.ticketType_id == service.id:
            flight = Flight.query.filter_by(id=a.flight_id)
            for i in flight:
                airport_from = Airport.query.filter_by(id=i.airport_from_id).first()
                city_from = City.query.filter_by(id=airport_from.id).first()
                airport_to = Airport.query.filter_by(id=i.airport_to_id).first()
                city_to = City.query.filter_by(id=airport_to.id).first()
                airport_sp = []
                if i.airport_support > 0:
                    peter1 = DetailFlight.query.filter_by(flight_id=i.id)
                    for j in peter1:
                        ap = Airport.query.filter_by(id=j.airport_id)
                        for z in ap:
                            airport_sp.append({
                                "fl_id": z.id,
                                "ap_name": z.name,
                                "time": j.time_rest
                            })

                flights.append({
                    "flight_id": i.id,
                    "type_id": service.id,
                    "type_name": service.name_type,
                    "date_start": i.day_start,
                    "time_start": i.time_start,
                    "from": city_from.name,
                    "to": city_to.name,
                    "airport_support": airport_sp,
                    "ticket_id": a.id,
                    "price": int(i.price),
                    "price_service": 0,
                    "price_total": 0,
                    "image": i.image,
                    "active": i.active
                })
    if flight_id:
        if service_arg:
            for i in flights:
                service_price = TicketType.query.filter(TicketType.name_type == str(service_arg)).first()
                if (int(flight_id) == i.get("flight_id")):
                    # for j in i.ticketType_id:
                        i["price_service"] = int(service_price.price)
                        i["price_total"] = int(i.get("price")) + int(service_price.price)
                        flightInfo.append(i)
        else:
            for i in flights:
                if (int(flight_id) == i.get("flight_id")):
                    flightInfo.append(i)
    return flightInfo

# print(get_flight_byid(1,"VIP"))

def get_flight_cart(flight_id=None):
    flights = []
    flight = Flight.query.filter_by(id=flight_id).first()
    airport_from = Airport.query.filter_by(id=flight.airport_from_id).first()
    city_from = City.query.filter_by(id=airport_from.id).first()
    airport_to = Airport.query.filter_by(id=flight.airport_to_id).first()
    city_to = City.query.filter_by(id=airport_to.id).first()
    airport_sp = []
    if flight.airport_support > 0:
        peter1 = DetailFlight.query.filter_by(flight_id=flight.id).order_by(asc(DetailFlight.airport_number))
        for j in peter1:
            ap = Airport.query.filter_by(id=j.airport_id)
            for z in ap:
                airport_sp.append({
                    "fl_id": z.id,
                    "ap_name": z.name,
                    "stt": j.airport_number,
                    "time": j.time_rest
                })
    # if (i.day_start >= time.date()) and (i.time_start >= time.time()):
    flights.append({
        "flight_id": flight.id,
        "date_start": flight.day_start,
        "time_start": flight.time_start,
        "from": city_from.name,
        "to": city_to.name,
        "airport_support": airport_sp,
        "price": flight.price,
        "image": flight.image,
        "active": flight.active
    })
    return flights
# print(get_flight_cart(1),"asda")

def cart_stats(cart):
    total_quantity, total_amount = 0, 0
    ticket_id = ""
    if cart:
        for p in cart.values():
            total_quantity += p["quantity"]
            total_amount += p["quantity"] * p["price_total"]
            ticket_id = p["ticket_id"]

    return {
        "ticket_id": ticket_id,
        "total_quantity": total_quantity,
        "total_amount": total_amount,
    }

# Tao Hoa don
def add_invoice(cart):
    total = 0
    if cart:
        try:
            for item in cart.values():
                total += int(item["price_total"]*item["quantity"])
            invoice = Invoice(customer=current_user, total=total)
            db.session.add(invoice)
            for item in cart.values():
                detail_invoice = DetailInvoice(ticket_id=item["ticket_id"],
                                               invoice=invoice, quantity=item["quantity"])
                db.session.add(detail_invoice)
            db.session.commit()
            return True
        except Exception as e:
            print("ERROR:" + str(e))
    return False

def numOfDays(date1, date2):
    return (date2-date1).days

def show_and_cancel_ticket(userid=None):
    flights = []
    invoice = Invoice.query.filter_by(customer_id=userid)
    for invoice in invoice:
        detail_invoice = DetailInvoice.query.filter_by(invoice_id=invoice.id)
        for dt_invoice in detail_invoice:
            ticket = Ticket.query.filter_by(id=dt_invoice.ticket_id)
            for ticket in ticket:
                flight = Flight.query.filter_by(id=ticket.flight_id).first()
                airport_from = Airport.query.filter_by(id=flight.airport_from_id).first()
                city_from = City.query.filter_by(id=airport_from.id).first()
                airport_to = Airport.query.filter_by(id=flight.airport_to_id).first()
                city_to = City.query.filter_by(id=airport_to.id).first()
                is_cancel = False
                if numOfDays(time.date(), flight.day_start) > 1:
                    is_cancel = True
                flights.append({
                    "invoice_id": invoice.id,
                    "userid": userid,
                    "flight_id": flight.id,
                    "date_start": flight.day_start,
                    "time_start": flight.time_start,
                    "time_flight": flight.time_flight,
                    "from": city_from.name,
                    "to": city_to.name,
                    "quantity": dt_invoice.quantity,
                    "price": int(invoice.total) * int(dt_invoice.quantity),
                    "image": flight.image,
                    "is_cancel": is_cancel,
                    "active": dt_invoice.status.value
                })
    return flights
# print(show_and_cancel_ticket(3))
# print(numOfDays(time.date(), datetime.date(2021,11,12)))

def cancel(invoice_id=None):
    try:
        detail_invoice = DetailInvoice.query.filter_by(invoice_id=invoice_id).first()
        detail_invoice.status = 'AN'
        db.session.add(detail_invoice)
        db.session.commit()
    except Exception as e:
        print("ERROR:" + str(e))
    return True



# ====NHAN VIEN=====
def staff_get_flight_filter(kw1=None, kw2=None, kw3=None ):
    flights = []
    flights_filter = []
    flights_filter_has_page = []
    peter = Flight.query.all()
    for i in peter:
        is_show = False
        airport_from = Airport.query.filter_by(id=i.airport_from_id).first()
        city_from = City.query.filter_by(id=airport_from.id).first()
        airport_to = Airport.query.filter_by(id=i.airport_to_id).first()
        city_to = City.query.filter_by(id=airport_to.id).first()
        airport_sp = []
        if i.airport_support > 0:
            peter1 = DetailFlight.query.filter_by(flight_id=i.id).order_by(asc(DetailFlight.airport_number))
            for j in peter1:
                ap = Airport.query.filter_by(id=j.airport_id)
                for z in ap:
                    airport_sp.append({
                        "fl_id": z.id,
                        "ap_name": z.name,
                        "stt": j.airport_number,
                        "time": j.time_rest
                    })
        if numOfDays(time.date(), i.day_start) >= 1:
            is_show = True
        flights.append({
            "flight_id": i.id,
            "date_start": i.day_start,
            "time_start": i.time_start,
            "from": city_from.name,
            "to": city_to.name,
            "airport_support": airport_sp,
            "price": i.price,
            "image": i.image,
            "active": i.active,
            "is_show": is_show
        })
    if kw1 and kw2 and kw3:
        for i in flights:
            if (kw1 in i.get("from") and kw2 in i.get("to") and kw3 == str(i.get("date_start")) ):
                flights_filter.append(i)
    else:
        flights_filter = flights
    return flights_filter
# print(staff_get_flight_filter("Hà Nội", "Hồ Chí Minh"),"2021-12-02")



def staff_show_customer(fullname=None,identify=None,phone=None):
    if fullname and identify and phone:
        app.config['customer'] = {
            "fullname": fullname,
            "identify": identify,
            "phone": phone
        }
    return app.config['customer']

def staff_add_invoice(cart):
    if cart:
        try:
            # if fullname and identify and phone:
                customer = User(fullname=app.config['customer'].get("fullname"),
                                identify=app.config['customer'].get("identify"),
                                phone=app.config['customer'].get("phone"))
                db.session.add(customer)
                for item in cart.values():
                    invoice = Invoice(customer=customer, staff=current_user, total=item["price_total"])
                    db.session.add(invoice)
                    detail_invoice = DetailInvoice(ticket_id=item["ticket_id"],
                                                   invoice=invoice, quantity=item["quantity"])
                    db.session.add(detail_invoice)
                db.session.commit()
                return True
        except Exception as e:
            print("ERROE:" + str(e))
    return False

def staff_cart_stats(staff_cart):
    total_quantity, total_amount = 0, 0
    ticket_id = ""
    if staff_cart:
        for p in staff_cart.values():
            total_quantity += p["quantity"]
            total_amount += p["quantity"] * p["price_total"]
            ticket_id = p["ticket_id"]

    return {
        "ticket_id": ticket_id,
        "total_quantity": total_quantity,
        "total_amount": total_amount,
    }

def staff_check_user(fullname=None, identify=None):
    infoUser = []
    user = User.query.filter(User.fullname == fullname, User.identify == identify)
    for i in user:
        infoUser.append({
            "id": i.id,
            "fullname": i.fullname,
            "birthday": i.birthday,
            "email": i.email,
            "identify": i.identify,
            "phone": i.phone,
            "avatar": i.avatar
        })
    return infoUser

def staff_delete_user(userid=None):
    user = User.query.filter_by(id=userid).first()
    db.session.delete(user)
    try:
        db.session.commit()
    except Exception as e:
        print("ERROR: " + str(e))
    return

def staff_update_user(fullname=None, email= None, birthday=None, identify=None, phone=None):
    user = User.query.filter(User.identify == identify).first()
    user.fullname = fullname
    user.email = email
    user.birthday = birthday
    user.identify = identify
    user.phone = phone
    db.session.add(user)
    try:
        db.session.commit()
    except Exception as e:
        print("ERROR: " + str(e))
    return True




# ===== ADMIN STASISTICS ======
def ticket_stats(from_date=None, to_date=None):
    stats = db.session.query(Ticket.id,
                             Ticket.flight_id,
                             TicketType.name_type,
                             func.sum(Invoice.total*DetailInvoice.quantity))

    if from_date:
        stats = stats.filter(Invoice.create_date.__ge__(from_date))

    if to_date:
        stats = stats.filter(Invoice.create_date.__le__(to_date))

    return stats.join(DetailInvoice,
                      DetailInvoice.ticket_id == Ticket.id,
                      isouter=True).filter(DetailInvoice.status == 'HIEN_1') \
        .join(Invoice, DetailInvoice.invoice_id == Invoice.id, isouter=True) \
        .join(TicketType, TicketType.id == Ticket.ticketType_id) \
        .group_by(Ticket.flight_id, TicketType.name_type).all()


def ticket_stats_flight():
    stats = db.session.query(Ticket.flight_id,
                             TicketType.name_type,
                             Flight.ticket_of_flight,
                             DetailInvoice.quantity,
                             func.sum(DetailInvoice.quantity)/Flight.ticket_of_flight)

    return stats.join(DetailInvoice,
                      DetailInvoice.ticket_id == Ticket.id,
                      isouter=True).filter(DetailInvoice.status == 'HIEN_1') \
        .join(Flight, Flight.id == Ticket.id, isouter=True) \
        .join(TicketType, TicketType.id == Ticket.ticketType_id) \
        .group_by(Flight.id).all()



