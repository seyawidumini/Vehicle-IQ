from functools import wraps
from flask_login import current_user
from flask import redirect, url_for, flash

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            return redirect(url_for("admin.admin_login"))

        if not current_user.is_admin:
            flash("Admin access only!", "danger")
            return redirect(url_for("admin.admin_login"))

        return f(*args, **kwargs)
    return decorated_function