from flask import render_template, request, redirect, url_for, flash, jsonify, make_response
from flask_login import login_user, logout_user, login_required, current_user
from urllib.parse import urlparse
import csv
import io
from datetime import datetime

from app import app, db, ml_model
from models import User, Prediction
from forms import LoginForm, RegistrationForm, PredictionForm

@app.route('/')
def index():
    """Home page"""
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login"""
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password', 'error')
            return redirect(url_for('login'))
        
        login_user(user)
        next_page = request.args.get('next')
        if not next_page or urlparse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    
    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    """User registration"""
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html', form=form)

@app.route('/logout')
@login_required
def logout():
    """User logout"""
    logout_user()
    return redirect(url_for('index'))

@app.route('/predict', methods=['GET', 'POST'])
@login_required
def predict():
    """Beam deflection prediction"""
    form = PredictionForm()
    prediction_result = None
    
    if form.validate_on_submit():
        try:
            # Make prediction using ML model
            predicted_deflection = ml_model.predict(
                beam_type=form.beam_type.data,
                length_mm=form.length_mm.data,
                width_mm=form.width_mm.data,
                depth_mm=form.depth_mm.data,
                reinforcement_percent=form.reinforcement_percent.data,
                load_kn=form.load_kn.data
            )
            
            if predicted_deflection is not None:
                # Save prediction to database
                prediction = Prediction(
                    user_id=current_user.id,
                    beam_type=form.beam_type.data,
                    length_mm=form.length_mm.data,
                    width_mm=form.width_mm.data,
                    depth_mm=form.depth_mm.data,
                    reinforcement_percent=form.reinforcement_percent.data,
                    load_kn=form.load_kn.data,
                    predicted_deflection_mm=predicted_deflection
                )
                
                db.session.add(prediction)
                db.session.commit()
                
                prediction_result = {
                    'deflection': round(predicted_deflection, 4),
                    'beam_type': form.beam_type.data,
                    'load': form.load_kn.data
                }
                
                flash(f'Prediction successful! Estimated deflection: {predicted_deflection:.4f} mm', 'success')
            else:
                flash('Prediction failed. Please check your inputs and try again.', 'error')
                
        except Exception as e:
            flash(f'Error making prediction: {str(e)}', 'error')
    
    return render_template('predict.html', form=form, prediction=prediction_result)

@app.route('/history')
@login_required
def history():
    """View prediction history"""
    page = request.args.get('page', 1, type=int)
    predictions = current_user.predictions.order_by(Prediction.created_at.desc()).paginate(
        page=page, per_page=10, error_out=False
    )
    
    return render_template('history.html', predictions=predictions)

@app.route('/download_history')
@login_required
def download_history():
    """Download prediction history as CSV"""
    predictions = current_user.predictions.order_by(Prediction.created_at.desc()).all()
    
    # Create CSV in memory
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Write header
    writer.writerow([
        'ID', 'Beam Type', 'Length (mm)', 'Width (mm)', 'Depth (mm)',
        'Reinforcement (%)', 'Load (kN)', 'Predicted Deflection (mm)', 'Date'
    ])
    
    # Write data
    for prediction in predictions:
        writer.writerow([
            prediction.id,
            prediction.beam_type,
            prediction.length_mm,
            prediction.width_mm,
            prediction.depth_mm,
            prediction.reinforcement_percent,
            prediction.load_kn,
            prediction.predicted_deflection_mm,
            prediction.created_at.strftime('%Y-%m-%d %H:%M:%S')
        ])
    
    # Create response
    response = make_response(output.getvalue())
    response.headers['Content-Type'] = 'text/csv'
    response.headers['Content-Disposition'] = f'attachment; filename=beam_predictions_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
    
    return response

@app.route('/api/stats')
@login_required
def api_stats():
    """API endpoint for user statistics"""
    total_predictions = current_user.predictions.count()
    
    # Get recent predictions for chart
    recent_predictions = current_user.predictions.order_by(Prediction.created_at.desc()).limit(10).all()
    chart_data = {
        'loads': [p.load_kn for p in reversed(recent_predictions)],
        'deflections': [p.predicted_deflection_mm for p in reversed(recent_predictions)],
        'dates': [p.created_at.strftime('%m/%d') for p in reversed(recent_predictions)]
    }
    
    return jsonify({
        'total_predictions': total_predictions,
        'chart_data': chart_data
    })

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500
