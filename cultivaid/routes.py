# Imports
import stripe
from flask import Flask, redirect, render_template, url_for, flash, request
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from functools import wraps
import os
from datetime import datetime
from flask import jsonify

from cultivaid import app, bcrypt
from cultivaid.models import User,Payment ,Service, Equipment, db, ServiceBooking
from cultivaid.forms import RegistrationForm, LoginForm,ServiceBookingForm,ServiceEditForm ,ServiceCreationForm, UpdateProfileForm

# Initialize LoginManager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth'  # Redirect to auth route when login is required
login_manager.login_message_category = 'info'


icons = {
    'Soil Testing and Consultation': 'fa-vial',
    'Pest Control': 'fa-spaghetti-monster-flying',
    'Irrigation and Setup': 'fa-droplet',
    'Livestock Transport': 'fa-truck-pickup',
    'Grain Drying and Storage': 'fa-warehouse',
    'Hydroponic Installation': 'fa-hammer',
    'default': 'fa-leaf'  # Default icon for services not in the dictionary
}

# User Loader
@login_manager.user_loader
def load_user(user_id):
    return User.objects(id=user_id).first()

# Admin Required Decorator
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            flash('You must be an admin to access this page.', 'error')
            return redirect(url_for('home'))
        return f(*args, **kwargs)
    return decorated_function

# Routes

@app.route('/')
@app.route('/home')
def home():
    services = Service.objects.limit(3)
    form = ServiceCreationForm()
    edit_form = ServiceEditForm()  # Add this line
    return render_template('home.html', services=services, form=form, edit_form=edit_form, icons=icons)

@app.route('/services')
def services():
    services = Service.objects()
    edit_form = ServiceEditForm()
    booking_form = ServiceBookingForm()
    return render_template('services.html', 
                         services=services, 
                         edit_form=edit_form, 
                         booking_form=booking_form,
                         icons=icons)


@app.route('/signup', methods=['GET', 'POST'])
def auth():
    form1 = RegistrationForm()
    form2 = LoginForm()

    # Handle Login
    if form2.is_submitted():
        user = User.objects(email=form2.email.data).first()
        
        # Admin Login
        if form2.email.data == "eric@gmail.com" and form2.password.data == "iloveTrump":
            # Create admin user if doesn't exist
            if not user:
                hashed_password = bcrypt.generate_password_hash("iloveTrump").decode('utf-8')
                user = User(
                    name="Admin",
                    email="eric@gmail.com",
                    phone_number="1234567890",
                    password=hashed_password,
                    is_admin=True
                )
                user.save()
            elif not user.is_admin:
                user.is_admin = True
                user.save()

            login_user(user)
            flash('Logged in as administrator!', 'success')
            return redirect(url_for('home'))

        # Regular User Login
        if user and bcrypt.check_password_hash(user.password, form2.password.data):
            login_user(user)
            next_page = request.args.get('next')
            flash('Logged in successfully!', 'success')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login unsuccessful. Please check email and password', 'error')

    # Handle Registration
    if form1.is_submitted() and form1.validate():
        if User.objects(email=form1.email.data).first():  # Check if email already exists
            flash('Email already registered', 'error')
        else:
            try:
                hashed_password = bcrypt.generate_password_hash(form1.password.data).decode('utf-8')
                user = User(
                    name=form1.name.data,
                    email=form1.email.data,
                    phone_number=form1.number.data,
                    password=hashed_password
                )
                user.save()  # Save the new user to the database
                flash('Account created successfully! Please login.', 'success')
                return redirect(url_for('auth'))
            except Exception as e:
                app.logger.error(f'Registration error: {str(e)}')
                flash('An error occurred during registration', 'error')

    return render_template('register.html', form1=form1, form2=form2)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth'))

@app.route('/add-service', methods=['POST'])
@login_required
@admin_required
def add_service():
    form = ServiceCreationForm()
    if form.validate_on_submit():
        try:
            # Create a new service object with matching field names
            service = Service(
                name=form.name.data,
                description=form.description.data,
                price=form.price.data,
                location=form.location.data
            )
            service.save()  # Save the new service to the database
            flash('Service added successfully!', 'success')
        except Exception as e:
            app.logger.error(f'Service creation error: {str(e)}')
            flash('An error occurred while adding the service', 'error')
        return redirect(url_for('home'))

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = UpdateProfileForm()  # Form for updating profile
    if form.validate_on_submit():
        try:
            # Update the current user's profile
            current_user.name = form.name.data
            current_user.email = form.email.data
            current_user.phone_number = form.phone_number.data
            current_user.password = form.password.data
            current_user.save()
            flash('Profile updated successfully!', 'success')
        except Exception as e:
            flash('Error updating profile.', 'error')
            app.logger.error(f'Profile update error: {str(e)}')
    elif request.method == 'GET':
        # Pre-fill the form with current user data
        form.name.data = current_user.name
        form.email.data = current_user.email
        form.phone_number.data = current_user.phone_number
        form.password.data = current_user.password
    
    return render_template('profile.html', form=form)

@app.route('/equipment')
def equipment():
    return render_template('equipment.html')
@app.route('/services/booked')
def booked_services():
    return render_template('booked.html')

@app.route('/delete-service/<service_id>', methods=['POST'])
@login_required
@admin_required
def delete_service(service_id):
    try:
        service = Service.objects(id=service_id).first()
        if service:
            service.delete()
            flash('Service deleted successfully!', 'success')
        else:
            flash('Service not found!', 'error')
    except Exception as e:
        app.logger.error(f'Service deletion error: {str(e)}')
        flash('An error occurred while deleting the service', 'error')
    return redirect(url_for('services'))


@app.route('/edit-service/<service_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_service(service_id):
    form = ServiceEditForm()
    if form.validate_on_submit():
        try:
            service = Service.objects(id=service_id).first()
            if service:
                service.update(
                    name=form.name.data,
                    description=form.description.data,
                    price=form.price.data,
                    location=form.location.data
                )
                flash('Service updated successfully!', 'success')
            else:
                flash('Service not found!', 'error')
        except Exception as e:
            app.logger.error(f'Service update error: {str(e)}')
            flash('An error occurred while updating the service', 'error')
    return redirect(request.referrer or url_for('home'))

@app.route('/book-service/<service_id>', methods=['POST'])
@login_required
def book_service(service_id):
    try:
        service = Service.objects(id=service_id).first()
        if not service:
            flash('Service not found!', 'error')
            return redirect(url_for('services'))
        
        booking_date_str = request.form.get('booking_date')
        if not booking_date_str:
            flash('Please select a booking date!', 'error')
            return redirect(url_for('services'))
        
        try:
            # Parse the datetime string
            booking_date = datetime.strptime(booking_date_str, '%Y-%m-%dT%H:%M')
            
            # Create the booking first
            booking = ServiceBooking(
                user=current_user.id,
                service=service.id,
                booking_date=booking_date,
                status='pending'
            )
            booking.save()
            
            # Create Stripe checkout session
            stripe_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': 'usd',
                        'unit_amount': int(service.price * 100),  # Convert to cents
                        'product_data': {
                            'name': service.name,
                        },
                    },
                    'quantity': 1,
                }],
                mode='payment',
                success_url=f"{request.host_url}payment/success?session_id={{CHECKOUT_SESSION_ID}}",
                cancel_url=f"{request.host_url}payment/cancel",
                metadata={
                    'booking_id': str(booking.id)
                }
            )
            
            # Create payment record
            payment = Payment(
                user=current_user.id,
                amount=service.price,
                stripe_payment_id=stripe_session.id,
                service_booking=booking.id,
                status='pending'
            )
            payment.save()
            
            # Update relationships
            booking.payment = payment
            booking.save()
            
            current_user.service_bookings.append(booking)
            current_user.payments.append(payment)
            current_user.save()
            
            return jsonify({
                'sessionId': stripe_session.id
            })
            
        except ValueError:
            flash('Invalid date format!', 'error')
            return redirect(url_for('services'))
            
    except Exception as e:
        app.logger.error(f'Booking error: {str(e)}')
        flash('An error occurred while booking the service', 'error')
        return redirect(url_for('services'))

@app.route('/payment/success')
@login_required
def payment_success():
    session_id = request.args.get('session_id')
    if session_id:
        try:
            # Find the payment record
            payment = Payment.objects(stripe_payment_id=session_id).first()
            if not payment:
                raise ValueError('Payment not found')
                
            # Verify payment with Stripe
            session = stripe.checkout.Session.retrieve(session_id)
            
            if session.payment_status == 'paid':
                # Update payment status
                payment.status = 'completed'
                payment.save()
                
                # Update booking status
                booking = payment.service_booking
                if booking:
                    booking.status = 'confirmed'
                    booking.save()
                    
                flash('Payment successful! Your booking is confirmed.', 'success')
                return redirect(url_for('my_bookings'))
                
        except Exception as e:
            app.logger.error(f'Payment verification error: {str(e)}')
    
    flash('Payment verification failed.', 'error')
    return redirect(url_for('services'))

@app.route('/payment/cancel')
@login_required
def payment_cancel():
    session_id = request.args.get('session_id')
    if session_id:
        try:
            payment = Payment.objects(stripe_payment_id=session_id).first()
            if payment:
                payment.status = 'failed'
                payment.save()
                
                # Also update booking status
                booking = payment.service_booking
                if booking:
                    booking.status = 'cancelled'
                    booking.save()
        except Exception as e:
            app.logger.error(f'Payment cancellation error: {str(e)}')
    
    flash('Payment was cancelled. Please try again.', 'warning')
    return redirect(url_for('services'))

@app.route('/my-bookings')
@login_required
def my_bookings():
    if current_user.is_admin:
        # Admin sees all bookings
        bookings = ServiceBooking.objects().order_by('-created_at')
        return render_template('booked.html', bookings=bookings, is_admin=True)
    else:
        # Regular users see only their bookings
        bookings = ServiceBooking.objects(user=current_user.id).order_by('-created_at')
        return render_template('booked.html', bookings=bookings, is_admin=False)
    

@app.route('/update-booking-status/<booking_id>/<status>')
@login_required
@admin_required
def update_booking_status(booking_id, status):
    try:
        booking = ServiceBooking.objects(id=booking_id).first()
        if booking and status in ['confirmed', 'cancelled']:
            booking.status = status
            booking.save()
            
            # If cancelling, also update payment status
            if status == 'cancelled' and booking.payment:
                booking.payment.status = 'cancelled'
                booking.payment.save()
                
            flash(f'Booking status updated to {status}!', 'success')
        else:
            flash('Invalid booking or status!', 'error')
    except Exception as e:
        app.logger.error(f'Booking status update error: {str(e)}')
        flash('An error occurred while updating the booking status', 'error')
    
    return redirect(url_for('my_bookings'))


@app.route('/create-payment-session/<booking_id>', methods=['POST'])
@login_required
def create_payment_session(booking_id):
    try:
        print(f"Creating payment session for booking {booking_id}")  # Debug print
        
        booking = ServiceBooking.objects(id=booking_id).first()
        if not booking:
            return jsonify({'error': 'Booking not found'}), 404

        # Create Stripe checkout session
        stripe_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'unit_amount': int(booking.service.price * 100),  # Convert to cents
                    'product_data': {
                        'name': booking.service.name,
                        'description': f'Booking for {booking.booking_date.strftime("%Y-%m-%d %H:%M")}'
                    },
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url=request.host_url + f'payment/success?session_id={{CHECKOUT_SESSION_ID}}&booking_id={booking_id}',
            cancel_url=request.host_url + f'payment/cancel?booking_id={booking_id}',
            metadata={
                'booking_id': str(booking.id)
            }
        )
        
        print(f"Stripe session created: {stripe_session.id}")  # Debug print

        # Create or update payment record
        if not booking.payment:
            payment = Payment(
                user=current_user.id,
                amount=booking.service.price,
                stripe_payment_id=stripe_session.id,
                service_booking=booking.id,
                status='pending'
            )
            payment.save()
            booking.payment = payment
            booking.save()
        else:
            booking.payment.stripe_payment_id = stripe_session.id
            booking.payment.status = 'pending'
            booking.payment.save()

        return jsonify({
            'sessionId': stripe_session.id
        })

    except Exception as e:
        print(f"Error creating payment session: {str(e)}")  # Debug print
        return jsonify({'error': str(e)}), 500