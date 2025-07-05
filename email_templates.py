#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CORNELIA DIAMOND RESORT & SPA
PROFESSIONAL EMAIL TEMPLATES
Beautiful HTML email designs for all languages
"""

def get_professional_email_template(language, analysis_data, pricing_data, customer_name=""):
    """Generate professional HTML email template"""
    
    # Base data
    adults = analysis_data.get('adults', 2)
    children = analysis_data.get('children', 0)
    nights = analysis_data.get('nights', 5)
    room_type = analysis_data.get('room_type', 'suite')
    dates = analysis_data.get('dates', 'your selected dates')
    
    price_eur = pricing_data.get('price_eur', 1000)
    price_tl = pricing_data.get('price_tl', 46000)
    
    # Room type translations
    room_translations = {
        'en': {
            'standard': 'Standard Room',
            'suite': 'Suite Room', 
            'villa': 'Villa',
            'presidential': 'Presidential Villa'
        },
        'tr': {
            'standard': 'Standart Oda',
            'suite': 'Süit Oda',
            'villa': 'Villa',
            'presidential': 'Başkanlık Villa'
        },
        'de': {
            'standard': 'Standard Zimmer',
            'suite': 'Suite Zimmer',
            'villa': 'Villa',
            'presidential': 'Präsidenten Villa'
        },
        'fr': {
            'standard': 'Chambre Standard',
            'suite': 'Suite',
            'villa': 'Villa',
            'presidential': 'Villa Présidentielle'
        },
        'ru': {
            'standard': 'Стандартный номер',
            'suite': 'Люкс',
            'villa': 'Вилла',
            'presidential': 'Президентская вилла'
        }
    }
    
    # Language-specific content
    templates = {
        'en': {
            'subject': f'Your Booking Request - Cornelia Diamond Resort & Spa',
            'greeting': f'Dear {customer_name},' if customer_name else 'Dear Guest,',
            'thank_you': 'Thank you for your interest in Cornelia Diamond Resort & Spa.',
            'analyzed': 'Your request has been analyzed:',
            'guest_count': '👥 Guest Count',
            'duration': '🌙 Duration',
            'room_type': '🏨 Room Type',
            'dates_label': '📅 Dates',
            'estimated_price': 'Estimated Price:',
            'price': f'€{price_eur:,.0f} EUR (approximately {price_tl:,.0f} TL)',
            'contact': 'We will contact you shortly with detailed information.',
            'signature': 'Best regards,<br>Cornelia Diamond Resort & Spa',
            'facilities': 'Our luxury facilities include spa, private beach, golf course, and fine dining restaurants.',
            'children_text': f' + {children} children' if children > 0 else '',
            'adults_text': f'{adults} adult' + ('s' if adults > 1 else ''),
            'nights_text': f'{nights} night' + ('s' if nights > 1 else '')
        },
        'tr': {
            'subject': f'Rezervasyon Talebiniz - Cornelia Diamond Resort & Spa',
            'greeting': f'Sayın {customer_name},' if customer_name else 'Değerli Misafirimiz,',
            'thank_you': 'Cornelia Diamond Resort & Spa\'ya olan ilginiz için teşekkür ederiz.',
            'analyzed': 'Talebiniz analiz edilmiştir:',
            'guest_count': '👥 Misafir Sayısı',
            'duration': '🌙 Konaklama Süresi',
            'room_type': '🏨 Oda Tipi',
            'dates_label': '📅 Tarih',
            'estimated_price': 'Tahmini Fiyat:',
            'price': f'€{price_eur:,.0f} EUR (yaklaşık {price_tl:,.0f} TL)',
            'contact': 'Detaylı bilgi ile en kısa sürede sizinle iletişime geçeceğiz.',
            'signature': 'Saygılarımızla,<br>Cornelia Diamond Resort & Spa',
            'facilities': 'Lüks tesislerimiz arasında spa, özel plaj, golf sahası ve seçkin restoranlar bulunmaktadır.',
            'children_text': f' + {children} çocuk' if children > 0 else '',
            'adults_text': f'{adults} yetişkin',
            'nights_text': f'{nights} gece'
        },
        'de': {
            'subject': f'Ihre Buchungsanfrage - Cornelia Diamond Resort & Spa',
            'greeting': f'Liebe/r {customer_name},' if customer_name else 'Liebe Gäste,',
            'thank_you': 'Vielen Dank für Ihr Interesse am Cornelia Diamond Resort & Spa.',
            'analyzed': 'Ihre Anfrage wurde analysiert:',
            'guest_count': '👥 Anzahl Gäste',
            'duration': '🌙 Aufenthaltsdauer',
            'room_type': '🏨 Zimmertyp',
            'dates_label': '📅 Datum',
            'estimated_price': 'Geschätzter Preis:',
            'price': f'€{price_eur:,.0f} EUR (ca. {price_tl:,.0f} TL)',
            'contact': 'Wir werden uns in Kürze mit detaillierten Informationen bei Ihnen melden.',
            'signature': 'Mit freundlichen Grüßen,<br>Cornelia Diamond Resort & Spa',
            'facilities': 'Unsere luxuriösen Einrichtungen umfassen Spa, Privatstrand, Golfplatz und exquisite Restaurants.',
            'children_text': f' + {children} Kinder' if children > 0 else '',
            'adults_text': f'{adults} Erwachsene',
            'nights_text': f'{nights} Nächte'
        },
        'fr': {
            'subject': f'Votre Demande de Réservation - Cornelia Diamond Resort & Spa',
            'greeting': f'Cher/Chère {customer_name},' if customer_name else 'Chers clients,',
            'thank_you': 'Merci pour votre intérêt pour le Cornelia Diamond Resort & Spa.',
            'analyzed': 'Votre demande a été analysée:',
            'guest_count': '👥 Nombre d\'invités',
            'duration': '🌙 Durée du séjour',
            'room_type': '🏨 Type de chambre',
            'dates_label': '📅 Dates',
            'estimated_price': 'Prix estimé:',
            'price': f'€{price_eur:,.0f} EUR (environ {price_tl:,.0f} TL)',
            'contact': 'Nous vous contacterons sous peu avec des informations détaillées.',
            'signature': 'Cordialement,<br>Cornelia Diamond Resort & Spa',
            'facilities': 'Nos installations de luxe comprennent un spa, une plage privée, un terrain de golf et des restaurants raffinés.',
            'children_text': f' + {children} enfants' if children > 0 else '',
            'adults_text': f'{adults} adulte' + ('s' if adults > 1 else ''),
            'nights_text': f'{nights} nuit' + ('s' if nights > 1 else '')
        },
        'ru': {
            'subject': f'Ваш запрос на бронирование - Cornelia Diamond Resort & Spa',
            'greeting': f'Уважаемый/ая {customer_name},' if customer_name else 'Уважаемые гости,',
            'thank_you': 'Благодарим за интерес к Cornelia Diamond Resort & Spa.',
            'analyzed': 'Ваш запрос проанализирован:',
            'guest_count': '👥 Количество гостей',
            'duration': '🌙 Продолжительность',
            'room_type': '🏨 Тип номера',
            'dates_label': '📅 Даты',
            'estimated_price': 'Ориентировочная цена:',
            'price': f'€{price_eur:,.0f} EUR (примерно {price_tl:,.0f} TL)',
            'contact': 'Мы свяжемся с вами в ближайшее время с подробной информацией.',
            'signature': 'С уважением,<br>Cornelia Diamond Resort & Spa',
            'facilities': 'Наши роскошные удобства включают спа, частный пляж, поле для гольфа и изысканные рестораны.',
            'children_text': f' + {children} детей' if children > 0 else '',
            'adults_text': f'{adults} взрослых',
            'nights_text': f'{nights} ночей'
        }
    }
    
    # Get template for language (default to English)
    template = templates.get(language, templates['en'])
    
    # HTML Template with beautiful design
    html_template = f"""
    <!DOCTYPE html>
    <html lang="{language}">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{template['subject']}</title>
        <style>
            body {{
                font-family: 'Georgia', 'Times New Roman', serif;
                line-height: 1.6;
                color: #333;
                background-color: #f8f9fa;
                margin: 0;
                padding: 0;
            }}
            .container {{
                max-width: 600px;
                margin: 20px auto;
                background: #ffffff;
                border-radius: 15px;
                overflow: hidden;
                box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            }}
            .header {{
                background: linear-gradient(135deg, #d4af37 0%, #f4e4a6 100%);
                padding: 30px;
                text-align: center;
                color: #2c3e50;
            }}
            .logo {{
                font-size: 28px;
                font-weight: bold;
                margin-bottom: 10px;
                text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
            }}
            .subtitle {{
                font-size: 16px;
                opacity: 0.8;
                font-style: italic;
            }}
            .content {{
                padding: 40px 30px;
            }}
            .greeting {{
                font-size: 18px;
                margin-bottom: 20px;
                color: #2c3e50;
                font-weight: 600;
            }}
            .thank-you {{
                margin-bottom: 25px;
                font-size: 16px;
                color: #555;
            }}
            .analysis-section {{
                background: #f8f9fa;
                border-radius: 10px;
                padding: 25px;
                margin: 25px 0;
                border-left: 5px solid #d4af37;
            }}
            .analysis-title {{
                font-size: 18px;
                color: #2c3e50;
                margin-bottom: 15px;
                font-weight: 600;
            }}
            .analysis-item {{
                display: flex;
                justify-content: space-between;
                margin-bottom: 12px;
                padding: 8px 0;
                border-bottom: 1px solid #eee;
            }}
            .analysis-item:last-child {{
                border-bottom: none;
            }}
            .analysis-label {{
                font-weight: 600;
                color: #2c3e50;
            }}
            .analysis-value {{
                color: #d4af37;
                font-weight: 600;
            }}
            .price-section {{
                background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%);
                color: white;
                border-radius: 10px;
                padding: 25px;
                margin: 25px 0;
                text-align: center;
            }}
            .price-title {{
                font-size: 18px;
                margin-bottom: 15px;
                color: #d4af37;
            }}
            .price-amount {{
                font-size: 24px;
                font-weight: bold;
                color: #d4af37;
                text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
            }}
            .facilities {{
                background: #e8f4f8;
                border-radius: 10px;
                padding: 20px;
                margin: 25px 0;
                color: #2c3e50;
                font-style: italic;
            }}
            .contact-info {{
                margin: 25px 0;
                color: #555;
                font-size: 16px;
            }}
            .signature {{
                margin-top: 30px;
                color: #2c3e50;
                font-weight: 600;
                font-size: 16px;
            }}
            .footer {{
                background: #2c3e50;
                color: white;
                padding: 25px;
                text-align: center;
            }}
            .footer-contact {{
                margin-bottom: 15px;
            }}
            .footer-contact strong {{
                color: #d4af37;
            }}
            .footer-links {{
                font-size: 14px;
                opacity: 0.8;
            }}
            .divider {{
                height: 2px;
                background: linear-gradient(to right, transparent, #d4af37, transparent);
                margin: 20px 0;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <div class="logo">🏖️ CORNELIA DIAMOND RESORT & SPA</div>
                <div class="subtitle">Luxury All-Inclusive Resort Experience</div>
            </div>
            
            <div class="content">
                <div class="greeting">{template['greeting']}</div>
                
                <div class="thank-you">{template['thank_you']}</div>
                
                <div class="divider"></div>
                
                <div class="analysis-section">
                    <div class="analysis-title">📋 {template['analyzed']}</div>
                    <div class="analysis-item">
                        <span class="analysis-label">👥 {template['guest_count']}</span>
                        <span class="analysis-value">{template['adults_text']}{template['children_text']}</span>
                    </div>
                    <div class="analysis-item">
                        <span class="analysis-label">🌙 {template['duration']}</span>
                        <span class="analysis-value">{template['nights_text']}</span>
                    </div>
                    <div class="analysis-item">
                        <span class="analysis-label">🏨 {template['room_type']}</span>
                        <span class="analysis-value">{room_translations[language].get(room_type, room_type.title())}</span>
                    </div>
                    <div class="analysis-item">
                        <span class="analysis-label">{template['dates_label']}</span>
                        <span class="analysis-value">{dates}</span>
                    </div>
                </div>
                
                <div class="price-section">
                    <div class="price-title">💰 {template['estimated_price']}</div>
                    <div class="price-amount">{template['price']}</div>
                </div>
                
                <div class="facilities">
                    🏖️ {template['facilities']}
                </div>
                
                <div class="contact-info">
                    📞 {template['contact']}
                </div>
                
                <div class="signature">{template['signature']}</div>
            </div>
            
            <div class="footer">
                <div class="footer-contact">
                    <strong>📧 Email:</strong> corneliabooking@yourbookinghub.org<br>
                    <strong>📞 Phone:</strong> +90 242 710 16 00<br>
                    <strong>🌐 Website:</strong> corneliadiamond.com
                </div>
                <div class="footer-links">
                    Antalya, Turkey | Luxury All-Inclusive Resort<br>
                    © 2024 Cornelia Diamond Resort & Spa
                </div>
            </div>
        </div>
    </body>
    </html>
    """
    
    return {
        'subject': template['subject'],
        'html': html_template,
        'language': language
    }

# Test function
def test_templates():
    """Test all language templates"""
    test_analysis = {
        'adults': 2,
        'children': 2, 
        'nights': 5,
        'room_type': 'suite',
        'dates': 'August 10th to August 15th'
    }
    
    test_pricing = {
        'price_eur': 3500,
        'price_tl': 161000
    }
    
    languages = ['en', 'tr', 'de', 'fr', 'ru']
    
    for lang in languages:
        template = get_professional_email_template(lang, test_analysis, test_pricing, "John Smith")
        print(f"✅ {lang.upper()} template created: {template['subject']}")

if __name__ == "__main__":
    test_templates()