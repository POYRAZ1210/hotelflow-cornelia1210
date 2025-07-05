# -*- coding: utf-8 -*-
import os
import json
import logging
from openai import OpenAI
from langdetect import detect
from COMPLETE_DYNAMIC_HOTEL_SYSTEM import CompleteDynamicHotelSystem

logger = logging.getLogger(__name__)

class EmailProcessor:
    """Email processing with GPT analysis and multilingual responses"""
    
    def __init__(self):
        self.openai_client = None
        self.hotel_system = None
        self._initialize_services()
    
    def _initialize_services(self):
        """Initialize OpenAI and hotel system"""
        try:
            # Initialize OpenAI
            api_key = os.getenv('OPENAI_API_KEY')
            if api_key:
                self.openai_client = OpenAI(api_key=api_key)
                logger.info("OpenAI client initialized for email processing")
            else:
                logger.warning("OpenAI API key not found")
            
            # Initialize hotel system
            self.hotel_system = CompleteDynamicHotelSystem()
            logger.info("Hotel system initialized for email processing")
            
        except Exception as e:
            logger.error(f"Error initializing email processor: {e}")
    
    def process_email(self, email_data):
        """Process incoming email with GPT analysis"""
        try:
            sender = email_data['sender']
            subject = email_data['subject']
            body = email_data['body']
            
            logger.info(f"Processing email from {sender}: {subject}")
            
            # Detect language
            language = self._detect_language(body)
            logger.info(f"Detected language: {language}")
            
            # Analyze email with GPT
            analysis = self._analyze_email_content(body, language)
            
            # Generate response
            response_html = self._generate_response(analysis, language, sender)
            
            return {
                'success': True,
                'sender': sender,
                'subject': f"Re: {subject}",
                'response_html': response_html,
                'analysis': analysis,
                'language': language
            }
            
        except Exception as e:
            logger.error(f"Error processing email: {e}")
            return {
                'success': False,
                'error': str(e),
                'sender': email_data.get('sender', 'Unknown'),
                'subject': email_data.get('subject', 'No Subject')
            }
    
    def _detect_language(self, text):
        """Advanced email language detection"""
        try:
            # Clean text for better detection
            text_clean = text.lower().strip()
            
            # Specific language patterns (more accurate than keywords)
            language_patterns = {
                'tr': ['merhaba', 'rezervasyon', 'tatil', 'otel', 'teşekkür', 'saygılar', 'istiyorum', 'bilgi'],
                'de': ['guten tag', 'reservierung', 'urlaub', 'hotel', 'danke', 'freundlichen grüßen', 'möchte', 'buchung'],
                'fr': ['bonjour', 'réservation', 'vacances', 'hôtel', 'merci', 'cordialement', 'voudrais', 'information'],
                'ru': ['здравствуйте', 'бронирование', 'отпуск', 'отель', 'спасибо', 'уважением', 'хочу', 'информация'],
                'en': ['hello', 'booking', 'vacation', 'hotel', 'thank', 'regards', 'would like', 'information']
            }
            
            # Score each language based on pattern matches
            scores = {}
            for lang, patterns in language_patterns.items():
                score = 0
                for pattern in patterns:
                    if pattern in text_clean:
                        score += 1
                scores[lang] = score
            
            # Find language with highest score
            if scores:
                best_lang = max(scores.items(), key=lambda x: x[1])
                if best_lang[1] > 0:  # At least one pattern match
                    logger.info(f"Language detected by patterns: {best_lang[0]} (score: {best_lang[1]})")
                    return best_lang[0]
            
            # Fallback to langdetect library
            from langdetect import detect
            detected = detect(text)
            
            # Ensure we return supported languages only
            supported_languages = ['tr', 'en', 'de', 'fr', 'ru']
            if detected in supported_languages:
                logger.info(f"Language detected by langdetect: {detected}")
                return detected
            else:
                logger.info(f"Unsupported language {detected}, defaulting to English")
                return 'en'
            
        except Exception as e:
            logger.warning(f"Language detection failed: {e}")
            return 'en'
    
    def _analyze_email_content(self, email_content, language):
        """Analyze email content using GPT"""
        try:
            if self.hotel_system and hasattr(self.hotel_system, 'analyze_email_dynamically'):
                # Use hotel system's GPT analysis
                return self.hotel_system.analyze_email_dynamically(email_content, language)
            
            # Fallback GPT analysis
            return self._fallback_gpt_analysis(email_content, language)
            
        except Exception as e:
            logger.error(f"Email analysis failed: {e}")
            # Return default analysis
            return {
                'adults': 2,
                'children': 0,
                'nights': 7,
                'room_type': 'suite',
                'dates': '',
                'is_complete': False,
                'missing_info': ['details needed'],
                'confidence': 0.5,
                'analysis_method': 'fallback'
            }
    
    def _fallback_gpt_analysis(self, email_content, language):
        """Fallback GPT analysis if hotel system unavailable"""
        if not self.openai_client:
            return self._default_analysis()
        
        try:
            prompt = f"""
            Analyze this hotel booking email and extract information:
            
            Email: {email_content}
            Language: {language}
            
            Extract and return JSON:
            {{
                "adults": number of adults,
                "children": number of children,
                "nights": number of nights,
                "room_type": "standard|suite|villa|presidential",
                "dates": "dates mentioned",
                "is_complete": boolean,
                "missing_info": ["list of missing information"],
                "confidence": 0.8
            }}
            """
            
            response = self.openai_client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are a hotel booking analyst. Extract information and return valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                response_format={"type": "json_object"},
                temperature=0.1
            )
            
            result = json.loads(response.choices[0].message.content)
            result['analysis_method'] = 'gpt_fallback'
            
            return result
            
        except Exception as e:
            logger.error(f"Fallback GPT analysis failed: {e}")
            return self._default_analysis()
    
    def _default_analysis(self):
        """Default analysis when all else fails"""
        return {
            'adults': 2,
            'children': 0,
            'nights': 7,
            'room_type': 'suite',
            'dates': '',
            'is_complete': False,
            'missing_info': ['complete booking details needed'],
            'confidence': 0.3,
            'analysis_method': 'default'
        }
    
    def _generate_response(self, analysis, language, sender_email):
        """Generate professional HTML email response"""
        try:
            # Calculate pricing first
            pricing = self._calculate_pricing(analysis)
            
            # Extract customer name from analysis or email content, not sender email
            customer_name = analysis.get('customer_name', '') or ""
            
            # Generate professional response
            response = self._generate_professional_response(analysis, pricing, language, customer_name)
            
            if response and 'html_content' in response:
                return response['html_content']
            else:
                # Fallback if professional template fails
                return self._generate_fallback_response(analysis, language)
            
        except Exception as e:
            logger.error(f"Response generation failed: {e}")
            return self._generate_fallback_response(analysis, language)
    
    def _calculate_pricing(self, analysis):
        """Calculate pricing for booking"""
        try:
            if self.hotel_system and hasattr(self.hotel_system, 'get_pricing_info'):
                return self.hotel_system.get_pricing_info(
                    analysis.get('room_type', 'suite'),
                    analysis.get('nights', 7),
                    analysis.get('adults', 2),
                    []  # children ages
                )
            
            # Monthly pricing table (per night in EUR) - EXACT CORNELIA DIAMOND RATES
            monthly_prices = {
                'standard': {1: 1000, 2: 1000, 3: 1000, 4: 1000, 5: 1000, 6: 1000, 7: 1000, 8: 1000, 9: 1000, 10: 1000, 11: 1000, 12: 1000},
                'suite': {1: 1000, 2: 2000, 3: 2500, 4: 3000, 5: 3500, 6: 4500, 7: 7000, 8: 7000, 9: 5500, 10: 4000, 11: 3000, 12: 1500},
                'villa': {1: 1000, 2: 3500, 3: 5000, 4: 7000, 5: 8000, 6: 10000, 7: 10000, 8: 10000, 9: 8500, 10: 8000, 11: 5000, 12: 2500},
                'presidential': {1: 15000, 2: 15000, 3: 15000, 4: 15000, 5: 15000, 6: 15000, 7: 15000, 8: 15000, 9: 15000, 10: 15000, 11: 15000, 12: 15000}
            }
            
            # Get month (August = 8 for example)
            month = 8  # Default August
            room_type = analysis.get('room_type', 'suite').lower()
            
            # Get correct monthly price
            if room_type in monthly_prices:
                room_price = monthly_prices[room_type][month]
            else:
                room_price = 1000  # Default
            
            total_eur = room_price * analysis.get('nights', 5)
            total_tl = total_eur * 46.02  # Current exchange rate
            
            return {
                'total_eur': total_eur,
                'total_tl': total_tl,
                'price_per_night': room_price,
                'exchange_rate': 46.02,
                'room_type': room_type,
                'nights': analysis.get('nights', 5),
                'month': month
            }
            
        except Exception as e:
            logger.error(f"Pricing calculation failed: {e}")
            return {'total_eur': 1400, 'total_tl': 64400, 'price_per_night': 200, 'exchange_rate': 46.0}
    
    def _generate_professional_response(self, analysis, pricing, language, customer_name=""):
        """Generate professional HTML response using email templates"""
        try:
            from email_templates import get_professional_email_template
            
            # Prepare analysis data
            analysis_data = {
                'adults': analysis.get('adults', 2),
                'children': analysis.get('children', 0),
                'nights': analysis.get('nights', 5),
                'room_type': analysis.get('room_type', 'suite'),
                'dates': analysis.get('dates', 'your selected dates')
            }
            
            # Prepare pricing data
            pricing_data = {
                'price_eur': int(pricing.get('total_eur', 1000)),
                'price_tl': int(pricing.get('total_tl', 46000))
            }
            
            # Generate template
            template = get_professional_email_template(language, analysis_data, pricing_data, customer_name)
            
            return {
                'subject': template['subject'],
                'html_content': template['html'],
                'language': template['language']
            }
            
        except Exception as e:
            logger.error(f"Professional template generation failed: {e}")
            return self._generate_fallback_response(analysis, language)
    
    def _generate_fallback_response(self, analysis, language):
        """Generate fallback response"""
        greetings = {
            'tr': 'Merhaba',
            'en': 'Hello',
            'de': 'Guten Tag',
            'fr': 'Bonjour',
            'ru': 'Здравствуйте'
        }
        
        closings = {
            'tr': 'Saygılarımla',
            'en': 'Best regards',
            'de': 'Mit freundlichen Grüßen',
            'fr': 'Cordialement',
            'ru': 'С уважением'
        }
        
        greeting = greetings.get(language, 'Hello')
        closing = closings.get(language, 'Best regards')
        
        html_content = f"""
        <html>
        <body>
            <h2>{greeting},</h2>
            <p>Thank you for your interest in Cornelia Diamond Resort & Spa.</p>
            <p>We have received your booking inquiry for:</p>
            <ul>
                <li>Adults: {analysis.get('adults', 2)}</li>
                <li>Children: {analysis.get('children', 0)}</li>
                <li>Nights: {analysis.get('nights', 7)}</li>
                <li>Room Type: {analysis.get('room_type', 'Suite').title()}</li>
            </ul>
            <p>Our team will contact you shortly with detailed pricing and availability.</p>
            <p>{closing},<br>Cornelia Diamond Resort & Spa Team</p>
        </body>
        </html>
        """
        
        return html_content
    
    def _generate_basic_response(self, language):
        """Generate very basic response when all else fails"""
        greetings = {
            'tr': 'Merhaba, rezervasyon talebiniz alınmıştır.',
            'en': 'Hello, your reservation request has been received.',
            'de': 'Hallo, Ihre Reservierungsanfrage wurde erhalten.',
            'fr': 'Bonjour, votre demande de réservation a été reçue.',
            'ru': 'Здравствуйте, ваш запрос на бронирование получен.'
        }
        
        message = greetings.get(language, 'Hello, your reservation request has been received.')
        
        return f"""
        <html>
        <body>
            <p>{message}</p>
            <p>Cornelia Diamond Resort & Spa</p>
        </body>
        </html>
        """