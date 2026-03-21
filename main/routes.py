from flask import render_template,url_for,redirect,flash,request
from main import app,db,bcrypt,model,model_columns
from main.form import RegistrationForm,LoginForm,AdminLoginForm,FeedbackForm,BudgetRequestForm,VehiclePredictionForm,AddvehicleForm,AddBudgetForm,UpdateAccountForm
from main.models import User,Feedback,Prediction,Vehicles,Admin,Budgetrequest
from flask_login import login_user,current_user,logout_user,login_required
from main.decorator import admin_required
from main.utils import convert_form_to_model_input,predict_price
from sqlalchemy.orm import joinedload
from werkzeug.utils import secure_filename
import os

@app.route('/')
def home():
    return render_template('user/index.html')

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_pw=bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user=User(username=form.username.data,email=form.email.data,password=hashed_pw)
        db.session.add(user)
        db.session.commit()
        flash(f"Account Created ")
        return redirect(url_for('login'))
    return render_template("user/register.html", form=form)  

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            if not next_page or not next_page.startswith('/'):
                next_page = url_for('home')
            return redirect(next_page)
        flash('Login failed. Check username/password.', 'danger')
    return render_template('user/login.html', form=form)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route("/predict", methods=["GET", "POST"])
@login_required
def predict():
    form = VehiclePredictionForm()
    prediction = None

    if form.validate_on_submit():
        new_car = convert_form_to_model_input(form, model_columns)
        prediction = predict_price(new_car, model, model_columns)
        prediction_record = Prediction(
            model=form.car_model.data,
            model_year=str(form.model_year.data),
            milage=form.milage.data,
            fuel_type=form.fuel_type.data,
            transmission=form.transmission.data,
            ext_col=form.color.data,
            type=form.vehicle_type.data,
            condition=form.condition.data,
            location=form.location.data,
            cc=form.cc.data,
            power_steering=form.power_steering.data,
            push_start=form.push_start.data,
            user_id=current_user.id,
            price=prediction
        )
        db.session.add(prediction_record)
        db.session.commit()
        print("Prediction:", prediction)

    return render_template("user/predict.html", form=form, prediction=prediction)


@app.route("/feedback",methods=["GET","POST"])
@login_required
def feedback():
    form=FeedbackForm()
    if form.validate_on_submit():
        feedback=Feedback(rating=form.rating.data,message=form.message.data,user_id=current_user.id)
        db.session.add(feedback)
        db.session.commit()
        flash("Thank you for your feedback","success")
        return redirect(url_for('home'))
    return render_template("user/feedback.html",form=form)

@app.route("/search", methods=["GET", "POST"])
def search():
    form = BudgetRequestForm()
    vehicles = None
    if form.validate_on_submit():
        budget_value = form.budget.data
        min_price = max(0, budget_value - 500000)
        max_price = budget_value + 500000
        vehicles = Budgetrequest.query.filter(
            Budgetrequest.price.between(min_price, max_price)
        ).all()
    return render_template("user." \
    "/search.html", form=form, vehicles=vehicles)

@app.route("/about")
def about():
    vehicles = Vehicles.query.all()
    return render_template("user/about.html", vehicles=vehicles)

@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    return render_template('user/account.html', title='Account', form=form)

@app.route("/admin/dashboard")
@login_required
@admin_required
def admin_dashboard():
    return render_template("admin/admin_dashboard.html")


@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    form = AdminLoginForm()
    if form.validate_on_submit():
        admin = Admin.query.filter_by(email=form.email.data).first()
        if admin and bcrypt.check_password_hash(admin.password, form.password.data.strip()):
            login_user(admin)
            return redirect(url_for("admin_dashboard"))
        else:
            flash("Invalid email or password", "danger")
    return render_template("admin/admin_login.html", form=form)

@app.route("/admin/logout")
@admin_required
def admin_logout():
    logout_user()
    flash("Logged out successfully", "success")
    return redirect(url_for("admin_login"))

@app.route('/admin/feedback')
@login_required
def admin_feedback():
    if not current_user.is_admin:
        flash("Admin access only!", "danger")
        return redirect(url_for('login'))

    feedbacks = Feedback.query.options(joinedload(Feedback.user))\
                              .order_by(Feedback.created_at.desc()).all()

    for f in feedbacks:
        print(f.id, f.user_id, f.user)

    return render_template(
        'admin/admin_feedback.html',
        feedbacks=feedbacks,
        active_nav='feedback'
    )

@app.route('/admin/predictions')
@login_required
def admin_predictions():
    if not current_user.is_admin:
        flash("Admin access only!", "danger")
        return redirect(url_for('admin_login'))

    predictions = Prediction.query.options(joinedload(Prediction.user))\
                                  .order_by(Prediction.id.desc()).all()

    for p in predictions:
        print(p.id, p.user.username, p.model, p.price)

    return render_template(
        'admin/admin_predictions.html',
        predictions=predictions,
        active_nav='history' )

@app.route('/admin/vehicles')
@admin_required
def admin_vehicles():
    if not current_user.is_admin:
        flash("admin access only!", "danger")
        return redirect(url_for('admin_login'))
    
    vehicles = Vehicles.query.order_by(Vehicles.id.desc()).all()
    
    return render_template("admin/admin_vehicle.html", vehicles=vehicles)

@app.route("/admin/add_vehicle", methods=["GET", "POST"])
def add_vehicle():
    form = AddvehicleForm()
    if form.validate_on_submit():

        photo_path = None

        if form.photo.data:
            photo_file = form.photo.data
            filename = secure_filename(photo_file.filename)

            upload_folder = os.path.join(app.root_path, "static/vehicles")
            if not os.path.exists(upload_folder):
                os.makedirs(upload_folder)

            photo_file.save(os.path.join(upload_folder, filename))

            photo_path = f"vehicles/{filename}"

        new_vehicle = Vehicles(
            photo=photo_path,
            brand=form.brand.data,
            model=form.model.data,
            vehicle_category=form.vehicle_category.data,
            fuel_type=form.fuel_type.data
        )
        db.session.add(new_vehicle)
        db.session.commit()

        flash("Vehicle added successfully!", "success")
        return redirect(url_for("admin_vehicles"))

    return render_template("admin/admin_add_vehicle.html", form=form)



@app.route('/admin/vehicles/delete/<int:vehicle_id>', methods=['POST'])
@admin_required
def delete_vehicle(vehicle_id):
    vehicle = Vehicles.query.get_or_404(vehicle_id)

    db.session.delete(vehicle)
    db.session.commit()

    flash("Vehicle deleted successfully!", "success")
    return redirect(url_for('admin_vehicles'))

@app.route('/admin/search')
@admin_required
def admin_search():
    if not current_user.is_admin:
        flash("admin access only!", "danger")
        return redirect(url_for('admin_login'))
    
    budgetsearch = Budgetrequest.query.order_by(Budgetrequest.id.desc()).all()
    
    return render_template("admin/admin_budget_search.html", budgetsearch=budgetsearch)


@app.route('/admin/add', methods=["GET", "POST"])
@admin_required
def add_budget():
    form=AddBudgetForm()
    if form.validate_on_submit():
        budget=Budgetrequest(model=form.model.data,year=form.year.data,price=form.price.data)
        db.session.add(budget)
        db.session.commit()
        flash("Vehicle added successfully!", "success")
        return redirect(url_for("admin_search"))
    
    return render_template("admin/admin_add_budget.html", form=form)


@app.route('/admin/search/delete/<int:budget_id>', methods=['POST'])
@admin_required
def delete_budget_search(budget_id):
    budget = Budgetrequest.query.get_or_404(budget_id)

    db.session.delete(budget)
    db.session.commit()

    flash("Vehicle deleted successfully!", "success")
    return redirect(url_for('admin_search'))