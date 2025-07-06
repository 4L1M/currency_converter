from flask import Blueprint, render_template, request, jsonify, current_app
from datetime import datetime
from .utils import get_currency_rates, convert_currency

def init_routes(app, limiter):
    """Создаем и регистрируем blueprint"""
    
    main_bp = Blueprint('main', __name__)
    
    @main_bp.route('/')
    def index():
        try:
            rates = get_currency_rates()
            if not rates:
                raise ValueError("No currency rates available")
                
            popular = {code: rates[code] for code in ['USD', 'EUR', 'GBP', 'CNY'] if code in rates}
            
            return render_template(
                'index.html',
                currencies=rates,
                popular=popular,
                date=datetime.now().strftime('%d.%m.%Y')
            )
        except Exception as e:
            current_app.logger.error(f"Error: {str(e)}")
            return render_template('500.html'), 500

    @main_bp.route('/convert', methods=['POST'])
    @limiter.limit("100 per minute")
    def convert():
        try:
            data = request.get_json()
            amount = float(data.get('amount', 1))
            from_curr = data.get('from', 'USD').upper()
            to_curr = data.get('to', 'EUR').upper()
            
            result = convert_currency(amount, from_curr, to_curr)
            return jsonify({
                'result': result,
                'date': datetime.now().strftime('%d.%m.%Y')
            })
        except ValueError as e:
            current_app.logger.warning(f"Conversion error: {str(e)}")
            return jsonify({'error': str(e)}), 400
        except Exception as e:
            current_app.logger.error(f"Unexpected error: {str(e)}")
            return jsonify({'error': 'Internal error'}), 500
    
    app.register_blueprint(main_bp)