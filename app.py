from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
import os
import uuid

app = Flask(__name__)
app = Flask(__name__, static_folder='static')
app.config['UPLOAD_FOLDER'] = 'static/uploads'

# Создаем словарь, который будет служить базой данных для хранения сообщений
messages = {}


@app.route('/', methods=['GET', 'POST'])
def create_message():
    if request.method == 'POST':
        # Получаем данные из формы
        text = request.form['text']
        duration = request.form['duration']
        views = int(request.form['views'])
        files = request.files.getlist('file[]')

        # Генерируем уникальный идентификатор для сообщения
        message_id = str(uuid.uuid4())

        # Генерируем ссылки
        display_link = f"{request.host_url}message/displayLink/{message_id}"
        display_url = f"{request.host_url}message/display/{message_id}"

        # Сохраняем данные сообщения в базе данных
        messages[message_id] = {
            'text': text,
            'duration': duration,
            'views': views,
            'remaining_views': views,
            'files': []  # Добавили список файлов
        }

        # Сохраняем файлы, если они были загружены
        for file in files:
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            if not os.path.exists(app.config['UPLOAD_FOLDER']):
                os.makedirs(app.config['UPLOAD_FOLDER'])
            file.save(file_path)
            messages[message_id]['files'].append(f"uploads/{filename}")  # Добавляем файлы в список

        return redirect(url_for('display_link', message_id=message_id))

    return render_template('index.html')


@app.route('/message/displayLink/<message_id>')
def display_link(message_id):
    message = messages.get(message_id)

    if message:
        message['display_url'] = f"{request.host_url}message/display/{message_id}"
        return render_template('display_link.html', message=message)

    return "Сообщение не найдено."


@app.route('/message/display/<message_id>')
def display_message(message_id):
    message = messages.get(message_id)

    if message:
        if message['remaining_views'] > 0:
            message['remaining_views'] -= 1

            return render_template('display_message.html', message=message)
        else:
            return "У вас закончились просмотры для этой ссылки."

    return "Сообщение не найдено."


@app.route('/static/<path:filename>')
def serve_static(filename):
    return app.send_static_file(filename)


@app.route('/favicon.ico')
def serve_favicon():
    return app.send_static_file('favicon.ico')


@app.route('/static/styles/<path:filename>')
def send_css(filename):
    return send_from_directory('static/styles', filename)


@app.route('/static/scripts/<path:filename>')
def send_js(filename):
    return send_from_directory('static/scripts', filename)


if __name__ == '__main__':
    app.run()
