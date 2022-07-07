from flask_admin.contrib.sqla import ModelView
from flask_admin import BaseView, expose
from flask_login import logout_user, current_user
from flask import redirect


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
        return self.render("layout/home.html")

    def is_accessible(self):
        return current_user.is_authenticated


class LogoutView(BaseView):
    @expose("/")
    def index(self):
        logout_user()
        return redirect('/login')

    def is_accessible(self):
        return current_user.is_authenticated

