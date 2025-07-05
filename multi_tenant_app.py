# -*- coding: utf-8 -*-
"""
YourBookingHub.org - Multi-Tenant Hotel Email Automation SaaS
Admin can create hotel accounts, each hotel gets their own branded system
"""
import os
import hashlib
import secrets
from datetime import datetime, timedelta
from flask import Flask, render_template, request, jsonify, redirect, url_for, session, flash
from email_processor import EmailProcessor
from database import CorneliaDatabase
import logging
from dotenv import load_dotenv
import sqlite3

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'yourbookinghub-secret-2025')

class MultiTenantDatabase:
    def __init__(self, db_path='yourbookinghub_saas.db'):
        self.db_path = db_path
        self.init_admin_database()
    
    def init_admin_database(self):
        """Initialize admin database for managing hotel tenants"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Hotels table - each hotel is a tenant
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS hotels (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            hotel_name TEXT NOT NULL,
            domain_name TEXT UNIQUE NOT NULL,
            admin_email TEXT NOT NULL,
            admin_password_hash TEXT NOT NULL,
            gmail_email TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            status TEXT DEFAULT 'active',
            subscription_type TEXT DEFAULT 'professional',
            monthly_fee REAL DEFAULT 199.0,
            last_payment TIMESTAMP,
            email_count_this_month INTEGER DEFAULT 0,
            max_emails_per_month INTEGER DEFAULT 5000
        )
        ''')
        
        # Admin users table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS admin_users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            email TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            is_super_admin BOOLEAN DEFAULT TRUE
        )
        ''')
        
        # Create default admin if not exists
        cursor.execute('SELECT COUNT(*) FROM admin_users')
        if cursor.fetchone()[0] == 0:
            admin_password = self.hash_password('admin123')
            cursor.execute('''
            INSERT INTO admin_users (username, password_hash, email)
            VALUES (?, ?, ?)
            ''', ('admin', admin_password, 'admin@yourbookinghub.org'))
        
        conn.commit()
        conn.close()
    
    def hash_password(self, password):
        """Hash password for storage"""
        salt = secrets.token_hex(16)
        password_hash = hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 100000)
        return salt + password_hash.hex()
    
    def verify_password(self, password, stored_hash):
        """Verify password against stored hash"""
        salt = stored_hash[:32]
        stored_password = stored_hash[32:]
        password_hash = hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 100000)
        return password_hash.hex() == stored_password
    
    def create_hotel(self, hotel_name, domain_name, admin_email, admin_password, gmail_email=None):
        """Create new hotel tenant"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        password_hash = self.hash_password(admin_password)
        
        cursor.execute('''
        INSERT INTO hotels (hotel_name, domain_name, admin_email, admin_password_hash, gmail_email)
        VALUES (?, ?, ?, ?, ?)
        ''', (hotel_name, domain_name, admin_email, password_hash, gmail_email))
        
        hotel_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return hotel_id
    
    def get_all_hotels(self):
        """Get all hotel tenants"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
        SELECT id, hotel_name, domain_name, admin_email, gmail_email, 
               created_at, status, subscription_type, monthly_fee, 
               email_count_this_month, max_emails_per_month
        FROM hotels ORDER BY created_at DESC
        ''')
        
        hotels = []
        for row in cursor.fetchall():
            hotels.append({
                'id': row[0], 'hotel_name': row[1], 'domain_name': row[2],
                'admin_email': row[3], 'gmail_email': row[4], 'created_at': row[5],
                'status': row[6], 'subscription_type': row[7], 'monthly_fee': row[8],
                'email_count_this_month': row[9], 'max_emails_per_month': row[10]
            })
        
        conn.close()
        return hotels
    
    def get_hotel_by_domain(self, domain_name):
        """Get hotel by domain name"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM hotels WHERE domain_name = ?', (domain_name,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return {
                'id': row[0], 'hotel_name': row[1], 'domain_name': row[2],
                'admin_email': row[3], 'admin_password_hash': row[4], 'gmail_email': row[5],
                'created_at': row[6], 'status': row[7], 'subscription_type': row[8],
                'monthly_fee': row[9], 'last_payment': row[10], 'email_count_this_month': row[11],
                'max_emails_per_month': row[12]
            }
        return None
    
    def verify_hotel_login(self, domain_name, password):
        """Verify hotel admin login"""
        hotel = self.get_hotel_by_domain(domain_name)
        if hotel and self.verify_password(password, hotel['admin_password_hash']):
            return hotel
        return None

# Initialize multi-tenant database
mt_db = MultiTenantDatabase()

# Routes
@app.route('/')
def homepage():
    """YourBookingHub.org marketing homepage"""
    return render_template('yourbookinghub_homepage.html')

@app.route('/admin')
def admin_login():
    """Admin login page"""
    return render_template('admin_login.html')

@app.route('/admin/login', methods=['POST'])
def admin_login_post():
    """Handle admin login"""
    username = request.form.get('username')
    password = request.form.get('password')
    
    conn = sqlite3.connect(mt_db.db_path)
    cursor = conn.cursor()
    cursor.execute('SELECT password_hash FROM admin_users WHERE username = ?', (username,))
    result = cursor.fetchone()
    conn.close()
    
    if result and mt_db.verify_password(password, result[0]):
        session['admin_logged_in'] = True
        session['admin_username'] = username
        return redirect(url_for('admin_dashboard'))
    
    flash('Invalid credentials', 'error')
    return redirect(url_for('admin_login'))

@app.route('/admin/dashboard')
def admin_dashboard():
    """Admin dashboard - manage all hotels"""
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    
    hotels = mt_db.get_all_hotels()
    
    # Calculate statistics
    stats = {
        'total_hotels': len(hotels),
        'active_hotels': len([h for h in hotels if h['status'] == 'active']),
        'total_monthly_revenue': sum(h['monthly_fee'] for h in hotels if h['status'] == 'active'),
        'total_emails_this_month': sum(h['email_count_this_month'] for h in hotels)
    }
    
    return render_template('admin_dashboard.html', hotels=hotels, stats=stats)

@app.route('/admin/create-hotel', methods=['GET', 'POST'])
def create_hotel():
    """Create new hotel tenant"""
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    
    if request.method == 'POST':
        hotel_name = request.form.get('hotel_name')
        domain_name = request.form.get('domain_name')
        admin_email = request.form.get('admin_email')
        admin_password = request.form.get('admin_password')
        gmail_email = request.form.get('gmail_email')
        
        try:
            hotel_id = mt_db.create_hotel(hotel_name, domain_name, admin_email, admin_password, gmail_email)
            flash(f'Hotel "{hotel_name}" created successfully!', 'success')
            return redirect(url_for('admin_dashboard'))
        except Exception as e:
            flash(f'Error creating hotel: {str(e)}', 'error')
    
    return render_template('create_hotel.html')

@app.route('/hotel/<domain_name>')
def hotel_login(domain_name):
    """Hotel login page"""
    hotel = mt_db.get_hotel_by_domain(domain_name)
    if not hotel:
        return "Hotel not found", 404
    
    return render_template('hotel_login.html', hotel=hotel)

@app.route('/hotel/<domain_name>/login', methods=['POST'])
def hotel_login_post(domain_name):
    """Handle hotel login"""
    password = request.form.get('password')
    
    hotel = mt_db.verify_hotel_login(domain_name, password)
    if hotel:
        session['hotel_logged_in'] = True
        session['hotel_id'] = hotel['id']
        session['hotel_name'] = hotel['hotel_name']
        session['hotel_domain'] = hotel['domain_name']
        return redirect(url_for('hotel_dashboard', domain_name=domain_name))
    
    flash('Invalid password', 'error')
    return redirect(url_for('hotel_login', domain_name=domain_name))

@app.route('/hotel/<domain_name>/dashboard')
def hotel_dashboard(domain_name):
    """Hotel dashboard - branded for specific hotel"""
    if not session.get('hotel_logged_in') or session.get('hotel_domain') != domain_name:
        return redirect(url_for('hotel_login', domain_name=domain_name))
    
    hotel = mt_db.get_hotel_by_domain(domain_name)
    if not hotel:
        return "Hotel not found", 404
    
    # Get hotel-specific email statistics
    # This would connect to the hotel's specific email database
    stats = {
        'total_processed': hotel['email_count_this_month'],
        'today_processed': 0,  # Would be calculated from today's emails
        'pending_emails': 0,   # Would be fetched from Gmail
        'processing_active': True,  # Would be checked from system status
        'subscription_type': hotel['subscription_type'],
        'monthly_limit': hotel['max_emails_per_month'],
        'emails_remaining': hotel['max_emails_per_month'] - hotel['email_count_this_month']
    }
    
    return render_template('hotel_dashboard.html', hotel=hotel, stats=stats)

@app.route('/hotel/<domain_name>/start-processing', methods=['POST'])
def start_processing(domain_name):
    """Start email processing for specific hotel"""
    if not session.get('hotel_logged_in') or session.get('hotel_domain') != domain_name:
        return jsonify({'error': 'Unauthorized'}), 401
    
    # Here you would start the email processing for this specific hotel
    # Using their Gmail credentials and branded templates
    
    return jsonify({'success': True, 'message': 'Email processing started'})

@app.route('/hotel/<domain_name>/stop-processing', methods=['POST'])
def stop_processing(domain_name):
    """Stop email processing for specific hotel"""
    if not session.get('hotel_logged_in') or session.get('hotel_domain') != domain_name:
        return jsonify({'error': 'Unauthorized'}), 401
    
    # Here you would stop the email processing for this specific hotel
    
    return jsonify({'success': True, 'message': 'Email processing stopped'})

@app.route('/admin/logout')
def admin_logout():
    """Admin logout"""
    session.clear()
    return redirect(url_for('homepage'))

@app.route('/hotel/<domain_name>/logout')
def hotel_logout(domain_name):
    """Hotel logout"""
    session.clear()
    return redirect(url_for('homepage'))

if __name__ == '__main__':
    logger.info("Starting YourBookingHub.org Multi-Tenant Hotel SaaS Platform")
    logger.info("Admin login: username=admin, password=admin123")
    logger.info("Create hotels at: http://localhost:5000/admin")
    app.run(host='0.0.0.0', port=5000, debug=True)

# Vercel WSGI application
application = app