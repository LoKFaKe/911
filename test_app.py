import unittest
import sqlite3
import tempfile
import os
from flask import Flask, template_rendered
from contextlib import contextmanager
from your_application_file import app, get_db_connection  # replace 'your_application_file' with your actual filename

class TestScheduleApp(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Create a temporary database
        cls.db_fd, cls.db_path = tempfile.mkstemp()
        cls.app = app
        cls.app.config['TESTING'] = True
        cls.app.config['DATABASE'] = cls.db_path
        cls.client = cls.app.test_client()
        
        # Initialize the test database
        with cls.app.app_context():
            cls.init_db()
            cls.populate_db()

    @classmethod
    def tearDownClass(cls):
        os.close(cls.db_fd)
        os.unlink(cls.db_path)

    @classmethod
    def init_db(cls):
        with get_db_connection() as conn:
            with app.open_resource('schema.sql', mode='r') as f:  # assuming you save the schema to schema.sql
                conn.executescript(f.read())
            conn.commit()

    @classmethod
    def populate_db(cls):
        # This is the same as your database initialization
        with get_db_connection() as conn:
            # Insert test data
            conn.executescript('''
                -- Заполнение таблицы преподавателей
                INSERT INTO teachers (name) VALUES 
                ('Куликовская А.А.'),
                ('Красильников А.В.'),
                ('Рыжков А.И.'),
                ('Коршиков А.А.'),
                ('Фимина А.А.'),
                ('Баранникова И.В.'),
                ('Шпилев А.С.');

                -- Заполнение таблицы групп
                INSERT INTO groups (name) VALUES 
                ('201'),
                ('202');

                -- Заполнение таблицы предметов
                INSERT INTO subjects (name, teacher_id) VALUES 
                ('Разработка кода информационных систем', 1),
                ('Технология разработки программного обеспечения', 2),
                ('Управление и автоматизация баз данных', 2),
                ('Инструментальные средства разработки программного обеспечения', 1),
                ('Моделирование и анализ программного обеспечения', 3),
                ('Иностранный язык в профессиональной деятельности', 4),
                ('Проектирование и дизайн информационных систем', 5),
                ('Устройство и функционирование информационной системы', 3),
                ('Стандартизация, сертификация и техническое документоведение', 6),
                ('Физическая культура и спорт', 7);

                -- Заполнение таблицы teacher_group (связи преподавателей и групп)
                INSERT INTO teacher_group (teacher_id, group_id) VALUES
                (1, 1), (1, 2),
                (2, 1), (2, 2),
                (3, 1), (3, 2),
                (4, 1), (4, 2),
                (5, 1),
                (6, 2),
                (7, 1), (7, 2);

                -- Для группы 201
                INSERT INTO schedule (group_id, day_of_week, time_start, time_end, subject_id, lesson_type, room) VALUES
                (1, 1, '10:10', '11:40', 1, 'Лекция', '304'),
                (1, 1, '11:50', '13:20', 5, 'Лабораторный практикум', '208'),
                (1, 1, '13:30', '15:00', 7, 'Лекция', '304'),
                (1, 2, '10:10', '11:40', 2, 'Лабораторный практикум', '208'),
                (1, 2, '11:50', '13:20', 4, 'Лекция', '304'),
                (1, 3, '13:30', '15:00', 6, 'Лабораторный практикум', '208'),
                (1, 3, '15:10', '16:40', 3, 'Лекция', '304'),
                (1, 4, '10:10', '11:40', 8, 'Лабораторный практикум', '208'),
                (1, 4, '11:50', '13:20', 10, 'Лекция', '304'),
                (1, 5, '15:10', '16:40', 9, 'Лекция', '304'),
                (1, 5, '16:50', '18:20', 1, 'Лабораторный практикум', '208');

                -- Для группы 202
                INSERT INTO schedule (group_id, day_of_week, time_start, time_end, subject_id, lesson_type, room) VALUES
                (2, 1, '11:50', '13:20', 3, 'Лекция', '304'),
                (2, 1, '13:30', '15:00', 2, 'Лабораторный практикум', '208'),
                (2, 2, '10:10', '11:40', 6, 'Лекция', '304'),
                (2, 2, '11:50', '13:20', 1, 'Лабораторный практикум', '208'),
                (2, 2, '15:10', '16:40', 5, 'Лекция', '304'),
                (2, 3, '10:10', '11:40', 4, 'Лабораторный практикум', '208'),
                (2, 3, '13:30', '15:00', 7, 'Лекция', '304'),
                (2, 4, '15:10', '16:40', 9, 'Лабораторный практикум', '208'),
                (2, 5, '10:10', '11:40', 10, 'Лекция', '304'),
                (2, 5, '11:50', '13:20', 8, 'Лабораторный практикум', '208'),
                (2, 5, '16:50', '18:20', 2, 'Лекция', '304');
            ''')
            conn.commit()

    @contextmanager
    def captured_templates(self):
        recorded = []
        
        def record(sender, template, context, **extra):
            recorded.append((template, context))
            
        template_rendered.connect(record, app)
        try:
            yield recorded
        finally:
            template_rendered.disconnect(record, app)

    def test_home_route(self):
        with self.client as c:
            # Test GET request to home page
            response = c.get('/')
            self.assertEqual(response.status_code, 200)
            
            # Check if groups are in the response
            self.assertIn(b'201', response.data)
            self.assertIn(b'202', response.data)
            
            # Check if description is in the response
            self.assertIn(b'Описание проекта', response.data.decode('utf-8'))
            
            # Check template rendering
            with self.captured_templates() as templates:
                c.get('/')
                self.assertEqual(len(templates), 1)
                template, context = templates[0]
                self.assertEqual(template.name, 'index.html')
                self.assertIn('groups', context)
                self.assertIn('description', context)
                self.assertEqual(len(context['groups']), 2)

    def test_schedule_route_valid_group(self):
        with self.client as c:
            # Test POST request with valid group_id
            response = c.post('/schedule', data={'group_id': '1'})
            self.assertEqual(response.status_code, 200)
            
            # Check if group name is in the response
            self.assertIn(b'201', response.data)
            
            # Check if schedule data is present
            self.assertIn(b'Понедельник', response.data)
            self.assertIn(b'10:10', response.data)
            
            # Check template rendering
            with self.captured_templates() as templates:
                c.post('/schedule', data={'group_id': '1'})
                self.assertEqual(len(templates), 1)
                template, context = templates[0]
                self.assertEqual(template.name, 'schedule.html')
                self.assertIn('group_name', context)
                self.assertIn('days', context)
                self.assertIn('day_names', context)
                self.assertEqual(context['group_name'], '201')
                self.assertGreater(len(context['days']), 0)

    def test_schedule_route_invalid_group(self):
        with self.client as c:
            # Test POST request with invalid group_id
            response = c.post('/schedule', data={'group_id': '999'})
            self.assertEqual(response.status_code, 200)
            
            # Check if error message is in the response
            self.assertIn('Группа не найдена'.encode('utf-8'), response.data)
            
            # Check template rendering
            with self.captured_templates() as templates:
                c.post('/schedule', data={'group_id': '999'})
                self.assertEqual(len(templates), 1)
                template, context = templates[0]
                self.assertEqual(template.name, 'error.html')
                self.assertIn('message', context)
                self.assertEqual(context['message'], 'Группа не найдена')

    def test_schedule_route_missing_group_id(self):
        with self.client as c:
            # Test POST request without group_id
            response = c.post('/schedule', data={})
            self.assertEqual(response.status_code, 400)

    def test_faq_route(self):
        with self.client as c:
            # Test GET request to FAQ page
            response = c.get('/faq')
            self.assertEqual(response.status_code, 200)
            
            # Check template rendering
            with self.captured_templates() as templates:
                c.get('/faq')
                self.assertEqual(len(templates), 1)
                template, context = templates[0]
                self.assertEqual(template.name, 'faq.html')

    def test_db_connection(self):
        with app.app_context():
            conn = get_db_connection()
            self.assertIsNotNone(conn)
            
            # Test groups table
            groups = conn.execute('SELECT * FROM groups').fetchall()
            self.assertEqual(len(groups), 2)
            
            # Test schedule for group 1
            schedule = conn.execute('SELECT * FROM schedule WHERE group_id = 1').fetchall()
            self.assertGreater(len(schedule), 0)
            
            conn.close()

if __name__ == '__main__':
    unittest.main()