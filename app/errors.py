from flask import render_template, request
import logging

logger = logging.getLogger('currency_app')

def handle_404(e):
    logger.warning(f"404 Not Found: {request.url}")
    return render_template('404.html'), 404

def handle_500(e):
    logger.error(f"500 Internal Server Error: {str(e)}")
    return render_template('500.html'), 500