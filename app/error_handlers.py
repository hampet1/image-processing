from app import app
from flask import render_template, request


@app.errorhandler(404)
def url_not_found(error):
    return render_template('404.html')
    

@app.errorhandler(500)
def server_error(error):
    
    app.logger.error(f"Server error: {request.url}")
    return render_template('500.html')