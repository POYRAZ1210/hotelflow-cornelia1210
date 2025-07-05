# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, jsonify, redirect, url_for, session, flash
import os
import sqlite3
import hashlib
import json
from datetime import datetime
import logging

# Initialize Flask app
app = Flask(__name__, 
           template_folder='../templates',
           static_folder='../static')

# Configuration
app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['JSON_AS_ASCII'] = False  # Türkçe karakter desteği

# Simple in-memory database for Vercel
HOTELS_DB = {
    'cornelia': {
        'id': 'cornelia',
        'name': 'Cornelia Diamond Resort & Spa',
        'domain': 'cornelia',
        'admin_username': 'admin',
        'admin_password': 'admin123',
        'gmail_email': '',
        'openai_key': '',
        'gmail_client_id': '',
        'gmail_client_secret': '',
        'created_at': '2025-01-01',
        'subscription_plan': 'premium',
        'is_active': True
    }
}

ADMIN_CREDENTIALS = {
    'username': 'admin',
    'password': 'admin123'
}

# Routes
@app.route('/')
def homepage():
    """YourBookingHub.org homepage"""
    return render_template('yourbookinghub_homepage_new.html')

@app.route('/admin')
def admin_login():
    """Admin login page"""
    return render_template('admin_login_new.html')

@app.route('/admin/login', methods=['POST'])
def admin_login_post():
    """Handle admin login"""
    username = request.form.get('username')
    password = request.form.get('password')
    
    if username == ADMIN_CREDENTIALS['username'] and password == ADMIN_CREDENTIALS['password']:
        session['admin_logged_in'] = True
        return redirect(url_for('admin_dashboard'))
    else:
        flash('Invalid credentials')
        return redirect(url_for('admin_login'))

@app.route('/admin/dashboard')
def admin_dashboard():
    """Admin dashboard"""
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    
    return render_template('admin_dashboard_new.html', hotels=HOTELS_DB)

@app.route('/admin/logout')
def admin_logout():
    """Admin logout"""
    session.pop('admin_logged_in', None)
    return redirect(url_for('homepage'))

@app.route('/dashboard/<domain>')
def hotel_dashboard_view(domain):
    """Hotel-specific dashboard"""
    if domain not in HOTELS_DB:
        flash('Hotel not found')
        return redirect(url_for('homepage'))
    
    hotel_data = HOTELS_DB[domain]
    
    # Simulate some stats for demo
    stats = {
        'daily_emails': 247,
        'auto_replies': 198,
        'new_customers': 15,
        'avg_response_time': 2
    }
    
    return render_template('hotel_dashboard.html', 
                         hotel_name=hotel_data['name'],
                         hotel_data=hotel_data,
                         **stats)

@app.route('/admin/create_hotel', methods=['POST'])
def create_hotel():
    """Create new hotel"""
    if not session.get('admin_logged_in'):
        return jsonify({'error': 'Unauthorized'}), 401
    
    data = request.get_json()
    hotel_id = data.get('domain')
    
    if hotel_id in HOTELS_DB:
        return jsonify({'error': 'Hotel already exists'}), 400
    
    HOTELS_DB[hotel_id] = {
        'id': hotel_id,
        'name': data.get('name'),
        'domain': hotel_id,
        'admin_username': data.get('admin_username', 'admin'),
        'admin_password': data.get('admin_password', 'admin123'),
        'gmail_email': data.get('gmail_email'),
        'openai_key': data.get('openai_key', ''),
        'gmail_client_id': data.get('gmail_client_id', ''),
        'gmail_client_secret': data.get('gmail_client_secret', ''),
        'created_at': datetime.now().strftime('%Y-%m-%d'),
        'subscription_plan': data.get('subscription_plan', 'standard'),
        'is_active': True
    }
    
    return jsonify({'success': True, 'hotel_id': hotel_id})

@app.route('/hotel/<hotel_domain>')
def hotel_login(hotel_domain):
    """Hotel login page"""
    hotel = HOTELS_DB.get(hotel_domain)
    if not hotel:
        return "Hotel not found", 404
    
    return render_template('hotel_login.html', hotel=hotel)

@app.route('/hotel/<hotel_domain>/login', methods=['POST'])
def hotel_login_post(hotel_domain):
    """Handle hotel login"""
    hotel = HOTELS_DB.get(hotel_domain)
    if not hotel:
        return "Hotel not found", 404
    
    username = request.form.get('username')
    password = request.form.get('password')
    
    if username == hotel['admin_username'] and password == hotel['admin_password']:
        session[f'hotel_{hotel_domain}_logged_in'] = True
        return redirect(url_for('hotel_dashboard', hotel_domain=hotel_domain))
    else:
        flash('Invalid credentials')
        return redirect(url_for('hotel_login', hotel_domain=hotel_domain))

@app.route('/hotel/<hotel_domain>/dashboard')
def hotel_dashboard(hotel_domain):
    """Hotel dashboard"""
    if not session.get(f'hotel_{hotel_domain}_logged_in'):
        return redirect(url_for('hotel_login', hotel_domain=hotel_domain))
    
    hotel = HOTELS_DB.get(hotel_domain)
    if not hotel:
        return "Hotel not found", 404
    
    # Mock stats for demo
    stats = {
        'total_emails': 127,
        'processed_today': 12,
        'response_rate': 98.5,
        'avg_response_time': '2.3 min',
        'languages_supported': ['Turkish', 'English', 'German', 'French', 'Russian']
    }
    
    return render_template('hotel_dashboard.html', hotel=hotel, stats=stats)

@app.route('/api/hotels')
def api_hotels():
    """API endpoint for hotels"""
    return jsonify(list(HOTELS_DB.values()))

@app.route('/api/stats/<hotel_domain>')
def api_stats(hotel_domain):
    """API endpoint for hotel stats"""
    hotel = HOTELS_DB.get(hotel_domain)
    if not hotel:
        return jsonify({'error': 'Hotel not found'}), 404
    
    # Mock stats
    stats = {
        'total_emails': 127,
        'processed_today': 12,
        'response_rate': 98.5,
        'avg_response_time': '2.3 min',
        'active_campaigns': 3,
        'revenue_this_month': 25000,
        'languages_supported': 5
    }
    
    return jsonify(stats)

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0'
    })

# Error handling for UTF-8
@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        'error': 'Internal server error',
        'message': 'Server encountered an error. Please try again.',
        'status': 500
    }), 500

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'error': 'Not found',
        'message': 'The requested resource was not found.',
        'status': 404
    }), 404

# Flask app'i Vercel için export et
application = app

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)