#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Database Management Module for Cornelia Gmail System
"""

import sqlite3
import json
from datetime import datetime
from typing import Dict, List, Optional, Any

class CorneliaDatabase:
    """Advanced database management for Cornelia Gmail System"""
    
    def __init__(self, db_path: str = 'cornelia_emails.db'):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize comprehensive database schema"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Customer emails table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS customer_emails (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                gmail_message_id TEXT UNIQUE NOT NULL,
                thread_id TEXT,
                customer_email TEXT NOT NULL,
                sender_name TEXT,
                sender_domain TEXT,
                subject TEXT,
                email_content TEXT,
                email_snippet TEXT,
                detected_language TEXT,
                language_confidence REAL,
                email_type TEXT,
                booking_status TEXT,
                information_complete BOOLEAN DEFAULT 0,
                confidence_score REAL DEFAULT 0.0,
                missing_info TEXT,
                check_in_date TEXT,
                check_out_date TEXT,
                nights INTEGER,
                room_type TEXT,
                adults INTEGER DEFAULT 0,
                children INTEGER DEFAULT 0,
                children_ages TEXT,
                price_eur REAL,
                price_tl REAL,
                price_usd REAL,
                price_rub REAL,
                exchange_rate_eur_tl REAL,
                discount_applied REAL DEFAULT 0.0,
                is_returning_customer BOOLEAN DEFAULT 0,
                customer_tier TEXT DEFAULT 'standard',
                response_sent BOOLEAN DEFAULT 0,
                response_type TEXT,
                response_language TEXT,
                response_sent_at DATETIME,
                email_marked_read BOOLEAN DEFAULT 0,
                processing_time_ms INTEGER,
                sentiment_score REAL,
                urgency_level TEXT DEFAULT 'normal',
                received_at DATETIME,
                processed_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Email sending logs
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS email_send_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                to_email TEXT NOT NULL,
                subject TEXT,
                language TEXT,
                email_type TEXT,
                sent_successfully BOOLEAN DEFAULT 0,
                gmail_message_id TEXT,
                error_message TEXT,
                retry_count INTEGER DEFAULT 0,
                send_duration_ms INTEGER,
                sent_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # System metrics
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS system_metrics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                metric_name TEXT NOT NULL,
                metric_value REAL,
                metric_unit TEXT,
                measurement_time DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Language detection cache
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS language_cache (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                content_hash TEXT UNIQUE NOT NULL,
                detected_language TEXT,
                confidence REAL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Customer profiles
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS customer_profiles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email_address TEXT UNIQUE NOT NULL,
                first_name TEXT,
                last_name TEXT,
                preferred_language TEXT,
                country TEXT,
                phone TEXT,
                total_bookings INTEGER DEFAULT 0,
                total_spent_eur REAL DEFAULT 0.0,
                customer_tier TEXT DEFAULT 'standard',
                first_contact_date DATETIME,
                last_contact_date DATETIME,
                preferred_room_type TEXT,
                special_requests TEXT,
                marketing_consent BOOLEAN DEFAULT 0,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create indexes for better performance - with error handling
        indexes = [
            'CREATE INDEX IF NOT EXISTS idx_customer_email ON customer_emails(customer_email)',
            'CREATE INDEX IF NOT EXISTS idx_gmail_message_id ON customer_emails(gmail_message_id)',
            'CREATE INDEX IF NOT EXISTS idx_language ON customer_emails(detected_language)',
            'CREATE INDEX IF NOT EXISTS idx_response_sent ON customer_emails(response_sent)'
        ]
        
        for index_sql in indexes:
            try:
                cursor.execute(index_sql)
            except Exception as e:
                print(f"Index creation warning: {e}")
        
        conn.commit()
        conn.close()
    
    def get_connection(self):
        """Get database connection with row factory"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn
    
    def save_customer_email(self, email_data: Dict[str, Any]) -> int:
        """Save customer email to database"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO customer_emails (
                    gmail_message_id, thread_id, customer_email, sender_name,
                    subject, email_content, detected_language, language_confidence,
                    information_complete, missing_info, room_type, adults, children,
                    price_eur, price_tl, exchange_rate_eur_tl, is_returning_customer,
                    response_sent, response_type, response_language, email_marked_read,
                    processing_time_ms, received_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                email_data.get('gmail_message_id'),
                email_data.get('thread_id'),
                email_data.get('customer_email'),
                email_data.get('sender_name'),
                email_data.get('subject'),
                email_data.get('email_content'),
                email_data.get('detected_language'),
                email_data.get('language_confidence'),
                email_data.get('information_complete', False),
                email_data.get('missing_info', ''),
                email_data.get('room_type'),
                email_data.get('adults', 0),
                email_data.get('children', 0),
                email_data.get('price_eur'),
                email_data.get('price_tl'),
                email_data.get('exchange_rate_eur_tl'),
                email_data.get('is_returning_customer', False),
                email_data.get('response_sent', False),
                email_data.get('response_type'),
                email_data.get('response_language'),
                email_data.get('email_marked_read', False),
                email_data.get('processing_time_ms'),
                email_data.get('received_at')
            ))
            
            email_id = cursor.lastrowid
            conn.commit()
            return email_id
            
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
    
    def get_customer_history(self, customer_email: str, limit: int = 10) -> List[Dict]:
        """Get customer's email history"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM customer_emails 
            WHERE customer_email = ? 
            ORDER BY processed_at DESC
            LIMIT ?
        ''', (customer_email, limit))
        
        history = [dict(row) for row in cursor.fetchall()]
        conn.close()
        
        return history
    
    def update_customer_profile(self, email_address: str, **kwargs) -> bool:
        """Update or create customer profile"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            # Check if profile exists
            cursor.execute('SELECT id FROM customer_profiles WHERE email_address = ?', (email_address,))
            existing = cursor.fetchone()
            
            if existing:
                # Update existing profile
                set_clauses = []
                values = []
                
                for key, value in kwargs.items():
                    if key != 'email_address':
                        set_clauses.append(f"{key} = ?")
                        values.append(value)
                
                if set_clauses:
                    set_clauses.append("updated_at = CURRENT_TIMESTAMP")
                    sql = f"UPDATE customer_profiles SET {', '.join(set_clauses)} WHERE email_address = ?"
                    values.append(email_address)
                    cursor.execute(sql, values)
            else:
                # Create new profile
                kwargs['email_address'] = email_address
                columns = list(kwargs.keys())
                placeholders = ['?' for _ in columns]
                
                sql = f"INSERT INTO customer_profiles ({', '.join(columns)}) VALUES ({', '.join(placeholders)})"
                cursor.execute(sql, list(kwargs.values()))
            
            conn.commit()
            return True
            
        except Exception as e:
            conn.rollback()
            return False
        finally:
            conn.close()
    
    def log_email_send(self, send_data: Dict[str, Any]) -> None:
        """Log email sending attempt"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO email_send_log (
                to_email, subject, language, email_type, sent_successfully,
                gmail_message_id, error_message, send_duration_ms
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            send_data.get('to_email'),
            send_data.get('subject'),
            send_data.get('language'),
            send_data.get('email_type'),
            send_data.get('sent_successfully', False),
            send_data.get('gmail_message_id'),
            send_data.get('error_message'),
            send_data.get('send_duration_ms')
        ))
        
        conn.commit()
        conn.close()
    
    def get_system_statistics(self) -> Dict[str, Any]:
        """Get comprehensive system statistics"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        stats = {}
        
        # Total emails
        cursor.execute('SELECT COUNT(*) FROM customer_emails')
        stats['total_emails'] = cursor.fetchone()[0]
        
        # Responses sent
        cursor.execute('SELECT COUNT(*) FROM customer_emails WHERE response_sent = 1')
        stats['responses_sent'] = cursor.fetchone()[0]
        
        # Complete bookings
        cursor.execute('SELECT COUNT(*) FROM customer_emails WHERE information_complete = 1')
        stats['complete_bookings'] = cursor.fetchone()[0]
        
        # Today's activity
        cursor.execute('SELECT COUNT(*) FROM customer_emails WHERE DATE(processed_at) = DATE("now")')
        stats['today_count'] = cursor.fetchone()[0]
        
        # Language distribution
        cursor.execute('SELECT detected_language, COUNT(*) FROM customer_emails GROUP BY detected_language')
        stats['language_stats'] = dict(cursor.fetchall())
        
        # Average response time
        cursor.execute('SELECT AVG(processing_time_ms) FROM customer_emails WHERE processing_time_ms IS NOT NULL')
        avg_time = cursor.fetchone()[0]
        stats['avg_processing_time_ms'] = round(avg_time, 2) if avg_time else 0
        
        # Success rate
        success_rate = (stats['responses_sent'] / stats['total_emails'] * 100) if stats['total_emails'] > 0 else 0
        stats['success_rate'] = round(success_rate, 1)
        
        # Recent activity (last 24 hours)
        cursor.execute('''
            SELECT COUNT(*) FROM customer_emails 
            WHERE processed_at >= datetime('now', '-1 day')
        ''')
        stats['last_24h_count'] = cursor.fetchone()[0]
        
        # Top customer countries
        cursor.execute('''
            SELECT country, COUNT(*) as count FROM customer_profiles 
            WHERE country IS NOT NULL 
            GROUP BY country 
            ORDER BY count DESC 
            LIMIT 5
        ''')
        stats['top_countries'] = dict(cursor.fetchall())
        
        # Room type preferences
        cursor.execute('''
            SELECT room_type, COUNT(*) as count FROM customer_emails 
            WHERE room_type IS NOT NULL 
            GROUP BY room_type 
            ORDER BY count DESC
        ''')
        stats['room_preferences'] = dict(cursor.fetchall())
        
        conn.close()
        return stats
    
    def cleanup_old_data(self, days_old: int = 365) -> int:
        """Clean up old data (older than specified days)"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Delete old email records
        cursor.execute('''
            DELETE FROM customer_emails 
            WHERE processed_at < datetime('now', '-{} days')
        '''.format(days_old))
        
        deleted_count = cursor.rowcount
        
        # Delete old send logs
        cursor.execute('''
            DELETE FROM email_send_log 
            WHERE sent_at < datetime('now', '-{} days')
        '''.format(days_old))
        
        # Delete old metrics
        cursor.execute('''
            DELETE FROM system_metrics 
            WHERE measurement_time < datetime('now', '-{} days')
        '''.format(days_old))
        
        conn.commit()
        conn.close()
        
        return deleted_count
    
    def export_customer_data(self, customer_email: str) -> Dict[str, Any]:
        """Export all data for a specific customer (GDPR compliance)"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        export_data = {}
        
        # Customer profile
        cursor.execute('SELECT * FROM customer_profiles WHERE email_address = ?', (customer_email,))
        profile = cursor.fetchone()
        if profile:
            export_data['profile'] = dict(profile)
        
        # Email history
        cursor.execute('SELECT * FROM customer_emails WHERE customer_email = ?', (customer_email,))
        emails = [dict(row) for row in cursor.fetchall()]
        export_data['emails'] = emails
        
        # Send logs
        cursor.execute('SELECT * FROM email_send_log WHERE to_email = ?', (customer_email,))
        send_logs = [dict(row) for row in cursor.fetchall()]
        export_data['send_logs'] = send_logs
        
        conn.close()
        return export_data
    
    def delete_customer_data(self, customer_email: str) -> bool:
        """Delete all data for a specific customer (GDPR compliance)"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            # Delete from all tables
            cursor.execute('DELETE FROM customer_profiles WHERE email_address = ?', (customer_email,))
            cursor.execute('DELETE FROM customer_emails WHERE customer_email = ?', (customer_email,))
            cursor.execute('DELETE FROM email_send_log WHERE to_email = ?', (customer_email,))
            
            conn.commit()
            return True
            
        except Exception as e:
            conn.rollback()
            return False
        finally:
            conn.close()

# Example usage functions
def test_database():
    """Test database functionality"""
    db = CorneliaDatabase()
    
    # Test customer email save
    test_email = {
        'gmail_message_id': 'test_123',
        'thread_id': 'thread_123',
        'customer_email': 'test@example.com',
        'sender_name': 'Test User',
        'subject': 'Test Reservation',
        'email_content': 'Hello, I want to book a room',
        'detected_language': 'en',
        'language_confidence': 0.9,
        'information_complete': False,
        'missing_info': 'dates,guest_count',
        'response_sent': True,
        'response_type': 'info_request',
        'response_language': 'en',
        'processing_time_ms': 1500,
        'received_at': datetime.now().isoformat()
    }
    
    email_id = db.save_customer_email(test_email)
    print(f"Saved email with ID: {email_id}")
    
    # Test customer profile update
    profile_data = {
        'first_name': 'Test',
        'last_name': 'User',
        'preferred_language': 'en',
        'country': 'USA',
        'customer_tier': 'standard'
    }
    
    success = db.update_customer_profile('test@example.com', **profile_data)
    print(f"Profile update success: {success}")
    
    # Test statistics
    stats = db.get_system_statistics()
    print(f"System statistics: {stats}")
    
    # Test customer history
    history = db.get_customer_history('test@example.com')
    print(f"Customer history: {len(history)} emails")

if __name__ == '__main__':
    test_database()