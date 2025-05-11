from flask import Flask, render_template, request, send_file, redirect, url_for, flash
from encoder import encode_image
from decoder import decode_image
from config import config
import os
import logging
from werkzeug.utils import secure_filename

def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    # Настройка логирования
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        filename='app.log'
    )

    @app.context_processor
    def inject_globals():
        return dict(
            app_name=app.config['APP_NAME'],
            current_year=app.config['CURRENT_YEAR']
        )

    @app.errorhandler(413)
    def request_entity_too_large(error):
        flash(f'Файл слишком большой! Максимум {app.config["MAX_CONTENT_LENGTH"]//(1024*1024)}MB')
        return redirect(url_for('home')), 413

    @app.route("/", methods=["GET", "POST"])
    def home():
        if request.method == "POST":
            operation = 'encode' if 'encode' in request.form else 'decode' if 'decode' in request.form else None
            
            if not operation:
                flash('Неизвестная операция')
                return redirect(url_for('home'))
            
            if 'image' not in request.files:
                flash('Не выбран файл изображения')
                return redirect(url_for('home'))
                
            file = request.files['image']
            
            if file.filename == '':
                flash('Не выбран файл изображения')
                return redirect(url_for('home'))
                
            if not allowed_file(file.filename):
                flash('Разрешены только PNG, JPG, JPEG')
                return redirect(url_for('home'))

            try:
                filename = secure_filename(file.filename)
                temp_path = os.path.join(app.config['UPLOAD_FOLDER'], f"temp_{filename}")
                file.save(temp_path)
                
                if operation == 'encode':
                    text = request.form.get('text', '').strip()
                    if not text:
                        flash('Введите сообщение для кодирования')
                        return redirect(url_for('home'))
                    
                    encoded_path = os.path.join(app.config['UPLOAD_FOLDER'], f"encoded_{filename}")
                    encode_image(temp_path, text, encoded_path)
                    return send_file(encoded_path, as_attachment=True)
                    
                elif operation == 'decode':
                    secret = decode_image(temp_path)
                    return render_template('result.html', message=secret)
                    
            except Exception as e:
                flash(f'Ошибка: {str(e)}')
                return redirect(url_for('home'))
            finally:
                if 'temp_path' in locals() and os.path.exists(temp_path):
                    os.remove(temp_path)
        
        return render_template("index.html")

    def allowed_file(filename):
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)