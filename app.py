from flask import Flask, request, jsonify
from flask_cors import CORS
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Email configuration
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USER = os.getenv('EMAIL_USER', 'cnwafor435@gmail.com')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')  # Use app password for Gmail

def send_email(name, email, message):
    """Send email using SMTP"""
    try:
        # Create message
        msg = MIMEMultipart()
        msg['From'] = EMAIL_USER
        msg['To'] = EMAIL_USER  # Send to yourself
        msg['Reply-To'] = email
        msg['Subject'] = f'Portfolio Contact Form: Message from {name}'
        
        # Create HTML email body
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background: linear-gradient(135deg, #00f7ff, #4b91f1); color: white; padding: 20px; text-align: center; border-radius: 10px 10px 0 0; }}
                .content {{ background: #f9f9f9; padding: 20px; border-radius: 0 0 10px 10px; }}
                .info {{ margin-bottom: 15px; padding: 10px; background: white; border-radius: 5px; border-left: 4px solid #00f7ff; }}
                .message {{ background: white; padding: 15px; border-radius: 5px; border: 1px solid #ddd; margin-top: 20px; }}
                .label {{ font-weight: bold; color: #005f6b; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h2>New Message from Portfolio Contact Form</h2>
                </div>
                <div class="content">
                    <div class="info">
                        <p><span class="label">From:</span> {name}</p>
                        <p><span class="label">Email:</span> <a href="mailto:{email}">{email}</a></p>
                        <p><span class="label">Date:</span> {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
                    </div>
                    <div class="message">
                        <p><span class="label">Message:</span></p>
                        <p>{message}</p>
                    </div>
                </div>
            </div>
        </body>
        </html>
        """
        
        # Attach HTML content
        msg.attach(MIMEText(html, 'html'))
        
        # Connect to SMTP server and send
        with smtplib.SMTP(EMAIL_HOST, EMAIL_PORT) as server:
            server.starttls()
            server.login(EMAIL_USER, EMAIL_PASSWORD)
            server.send_message(msg)
        
        logger.info(f"Email sent successfully from {name} ({email})")
        return True
        
    except Exception as e:
        logger.error(f"Failed to send email: {str(e)}")
        return False

@app.route('/send-email', methods=['POST'])
def send_email_route():
    """Handle email sending from contact form"""
    try:
        data = request.json
        
        # Validate required fields
        required_fields = ['name', 'email', 'message']
        for field in required_fields:
            if not data.get(field):
                return jsonify({
                    'success': False,
                    'message': f'{field} is required'
                }), 400
        
        # Send email
        success = send_email(
            name=data['name'],
            email=data['email'],
            message=data['message']
        )
        
        if success:
            return jsonify({
                'success': True,
                'message': 'Message sent successfully! I\'ll get back to you soon.'
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Failed to send message. Please try again later.'
            }), 500
            
    except Exception as e:
        logger.error(f"Error processing request: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'An error occurred. Please try again.'
        }), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint for deployment"""
    return jsonify({
        'status': 'healthy',
        'service': 'portfolio-backend',
        'version': '1.0.0'
    })

if __name__ == '__main__':
    # For development
    app.run(debug=True, host='0.0.0.0', port=5000)
