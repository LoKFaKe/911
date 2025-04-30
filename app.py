from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

class ScheduleRepository:
    DB_PATH = 'schedule.db'

    @staticmethod
    def get_connection():
        conn = sqlite3.connect(ScheduleRepository.DB_PATH)
        conn.row_factory = sqlite3.Row
        return conn

    @classmethod
    def get_groups(cls):
        conn = cls.get_connection()
        groups = conn.execute('SELECT * FROM groups').fetchall()
        conn.close()
        return groups

    @classmethod
    def get_group_by_id(cls, group_id):
        conn = cls.get_connection()
        group = conn.execute('SELECT * FROM groups WHERE id = ?', (group_id,)).fetchone()
        conn.close()
        return group

    @classmethod
    def get_schedule_by_group(cls, group_id):
        conn = cls.get_connection()
        schedule_data = conn.execute('''
            SELECT schedule.*, subjects.name as subject_name, teachers.name as teacher_name 
            FROM schedule
            JOIN subjects ON schedule.subject_id = subjects.id
            JOIN teachers ON subjects.teacher_id = teachers.id
            WHERE group_id = ?
            ORDER BY day_of_week, time_start
        ''', (group_id,)).fetchall()
        conn.close()
        return schedule_data



@app.route('/')
def home():
    groups = ScheduleRepository.get_groups()

    project_description = """
    <h2>Описание проекта</h2>
    <p>Это веб-приложение для просмотра учебного расписания, преобразованное из Telegram-бота.</p>

    <h2>Основные функции:</h2>
    <ul>
        <li>Просмотр расписания по группам</li>
        <li>Часто задаваемые вопросы (FAQ)</li>
        <li>Простой и интуитивно понятный интерфейс</li>
    </ul>

    <h2>Как использовать:</h2>
    <ol>
        <li>Выберите группу из списка ниже</li>
        <li>Нажмите кнопку "Показать расписание"</li>
        <li>Просмотрите результаты</li>
    </ol>

    <h2>Технологии:</h2>
    <ul>
        <li>Python Flask</li>
        <li>SQLite база данных</li>
        <li>HTML/CSS шаблоны</li>
    </ul>
    """

    return render_template('index.html', 
                           description=project_description,
                           groups=groups)


@app.route('/schedule', methods=['POST'])
def schedule():
    group_id = request.form['group_id']
    
    group = ScheduleRepository.get_group_by_id(group_id)
    if not group:
        return render_template('error.html', message='Группа не найдена')

    schedule_data = ScheduleRepository.get_schedule_by_group(group_id)
    
    days = {}
    for item in schedule_data:
        day = item['day_of_week']
        if day not in days:
            days[day] = []
        days[day].append(item)
    
    day_names = {
        1: 'Понедельник',
        2: 'Вторник',
        3: 'Среда',
        4: 'Четверг',
        5: 'Пятница'
    }
    
    return render_template('schedule.html',
                           group_name=group['name'],
                           days=days,
                           day_names=day_names)


@app.route('/faq')
def faq():
    return render_template('faq.html')


if __name__ == '__main__':
    app.run(debug=True)
