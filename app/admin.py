from flask_admin.contrib.sqla import ModelView
from flask_admin import BaseView, expose
from flask_login import logout_user, current_user
from flask import redirect, request
from app.models import City, Airport, Flight, User, TicketType, DetailFlight
from app import db, admin
import utils


class AuthenticatedView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated


class CategoryModelView(AuthenticatedView):
    can_export = True


class ProductModelView(AuthenticatedView):
    can_export = True


class StatsView(BaseView):
    @expose("/")
    def index(self):
        from_date = request.args.get('from_date')
        to_date = request.args.get('to_date')
        stats = utils.ticket_stats(from_date=from_date, to_date=to_date)
        stats_flight = utils.ticket_stats_flight()
        return self.render("admin/stats.html",
                           stats=stats,
                           stats_flight=stats_flight)

    def is_accessible(self):
        return current_user.is_authenticated


class LogoutView(BaseView):
    @expose("/")
    def index(self):
        logout_user()
        return redirect('/admin')

    def is_accessible(self):
        return current_user.is_authenticated


admin.add_view(ProductModelView(User, db.session, name="Quản Lí Nhân Sự"))
admin.add_view(ProductModelView(TicketType, db.session, name="Quản Lí Loại Vé"))
admin.add_view(CategoryModelView(City, db.session, name="Quản Lí Thành Phố"))
admin.add_view(ProductModelView(Airport, db.session, name="Quản Lí Sân Bay"))
admin.add_view(ProductModelView(Flight, db.session, name="Quản Lí Chuyến Bay"))
admin.add_view(ProductModelView(DetailFlight, db.session, name="Quản Lí Chi Tiết Chuyến Bay"))
admin.add_view(StatsView(name="Thống Kê Doanh Thu"))
admin.add_view(LogoutView(name="Đăng xuất"))