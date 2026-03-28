from flask import render_template,url_for,redirect,flash,Blueprint
from main import app,bcrypt
from main.Admins.forms import AdminLoginForm
from main.models import Admin
from flask_login import login_user,logout_user,login_required
from main.Admins.decorator import admin_required

admin=Blueprint('admin',__name__)

@admin.route("/admin/dashboard")
@login_required
@admin_required
def admin_dashboard():
    return render_template("admin/admin_dashboard.html")


@admin.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    form = AdminLoginForm()
    if form.validate_on_submit():
        admin = Admin.query.filter_by(email=form.email.data).first()
        if admin and bcrypt.check_password_hash(admin.password, form.password.data.strip()):
            login_user(admin)
            return redirect(url_for("admin.admin_dashboard"))
        else:
            flash("Invalid email or password", "danger")
    return render_template("admin/admin_login.html", form=form)

@admin.route("/admin/logout")
@admin_required
def admin_logout():
    logout_user()
    flash("Logged out successfully", "success")
    return redirect(url_for("admin.admin_login"))