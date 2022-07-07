from sqlalchemy import Column, String, Boolean, Integer, Float, ForeignKey, Time, Date, Enum
from sqlalchemy.orm import relationship
from flask_login import UserMixin
from app import db
from datetime import datetime
import enum

class MyRole(enum.Enum):
    USER = 0
    STAFF = 1
    ADMIN = 2

class StatusTicket(enum.Enum):
    HIEN_0 = 0
    HIEN_1 = 1
    AN = 2

class User(db.Model, UserMixin):
    id = Column(Integer, primary_key=True, autoincrement=True)
    fullname = Column(String(50), nullable=False)
    birthday = Column(Date, nullable=True)
    email = Column(String(50), nullable=True)
    identify = Column(String(50), nullable=False)
    avatar = Column(String(100), nullable=True)
    phone = Column(String(50), nullable=True)
    username = Column(String(50), nullable=True, unique=True)
    password = Column(String(100), nullable=True)
    role = Column(Enum(MyRole), default=MyRole.USER)
    def int (self):
        return self.id

class City(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    airport = relationship('Airport', backref="city", lazy=True)
    status = Column(Boolean, default=True)
    def __str__(self):
        return self.name

class Airport(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    city_id = Column(Integer, ForeignKey(City.id), nullable=False)
    status = Column(Boolean, default=True)
    detail_flight = relationship('DetailFlight', backref='airport', lazy=True)
    def __str__(self):
        return self.name

class Flight(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    airport_from_id = Column(Integer, ForeignKey(Airport.id), nullable=False)
    airport_to_id = Column(Integer, ForeignKey(Airport.id), nullable=False)
    day_start = Column(Date, default=datetime.now())
    time_start = Column(Time, default=datetime.now())
    time_flight = Column(Integer, nullable=False)
    ticket_of_flight = Column(Integer, nullable=False)
    ticket_avail = Column(Integer, nullable=False)
    airport_support = Column(Integer, nullable=False)
    image = Column(String(100), nullable=True)
    active = Column(Boolean, default=True)
    price = Column(Float, default=0)
    airport_from = relationship("Airport", foreign_keys=[airport_from_id])
    airport_to = relationship("Airport", foreign_keys=[airport_to_id])
    detail_flight = relationship('DetailFlight', backref='flight', lazy=True)
    ticket = relationship('Ticket', backref="flight", lazy=True)
    def itn (self):
        return self.id

class DetailFlight(db.Model):
    flight_id = Column(Integer, ForeignKey(Flight.id), primary_key=True, nullable=False)
    airport_id = Column(Integer, ForeignKey(Airport.id), primary_key=True, nullable=False)
    airport_number = Column(Integer, nullable=False)
    time_rest = Column(Integer, nullable=False)
    def int (self):
        return self.flight_id

class TicketType(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True);
    name_type = Column(String(50) , nullable=False)
    price = Column(Float, default=0)
    ticket = relationship('Ticket', backref="ticketType", lazy=True)
    def __str__(self):
        return self.name

class Ticket(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True);
    flight_id = Column(Integer, ForeignKey(Flight.id), nullable=False)
    ticketType_id = Column(Integer, ForeignKey(TicketType.id), nullable=False)
    amount = Column(Integer, default=1)
    price = Column(Float, default=0)
    detail_invoice = relationship('DetailInvoice', backref="ticket", lazy=True)
    def __str__(self):
        return self.name

class Invoice(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True);
    customer_id = Column(Integer, ForeignKey(User.id), nullable=False)
    staff_id = Column(Integer, ForeignKey(User.id), nullable=True)
    create_date = Column(Date, default=datetime.now())
    total = Column(Float, default=0)
    status = Column(Boolean, default=True)
    customer = relationship("User", foreign_keys=[customer_id])
    staff = relationship("User", foreign_keys=[staff_id])
    detail_invoice = relationship('DetailInvoice', backref="invoice", lazy=True)
    def int (self):
        return self.id

class DetailInvoice(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    ticket_id = Column(Integer, ForeignKey(Ticket.id), nullable=False);
    invoice_id = Column(Integer, ForeignKey(Invoice.id), nullable=False)
    quantity = Column(Integer, default=1, nullable=False)
    status = Column(Enum(StatusTicket), default=StatusTicket.HIEN_1, nullable=False)
    def int (self):
        return self.id

if __name__ == '__main__':
    db.create_all()