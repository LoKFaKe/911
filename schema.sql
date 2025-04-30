-- Создание базы данных расписания
BEGIN TRANSACTION;

-- Удаление таблиц если они существуют (для чистого создания)
DROP TABLE IF EXISTS schedule;
DROP TABLE IF EXISTS teacher_group;
DROP TABLE IF EXISTS subjects;
DROP TABLE IF EXISTS teachers;
DROP TABLE IF EXISTS groups;

-- Создание таблицы преподавателей
CREATE TABLE teachers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
);

-- Создание таблицы групп
CREATE TABLE groups (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
);

-- Создание таблицы предметов
CREATE TABLE subjects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    teacher_id INTEGER,
    FOREIGN KEY (teacher_id) REFERENCES teachers(id)
);

-- Создание промежуточной таблицы для связи многие-ко-многим
CREATE TABLE teacher_group (
    teacher_id INTEGER,
    group_id INTEGER,
    PRIMARY KEY (teacher_id, group_id),
    FOREIGN KEY (teacher_id) REFERENCES teachers(id),
    FOREIGN KEY (group_id) REFERENCES groups(id)
);

-- Создание таблицы расписания
CREATE TABLE schedule (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    group_id INTEGER,
    day_of_week INTEGER NOT NULL, -- 1-5 (пн-пт)
    time_start TEXT NOT NULL,
    time_end TEXT NOT NULL,
    subject_id INTEGER,
    lesson_type TEXT NOT NULL, -- Лекция или Лабораторный практикум
    room TEXT NOT NULL,
    FOREIGN KEY (group_id) REFERENCES groups(id),
    FOREIGN KEY (subject_id) REFERENCES subjects(id)
);

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
(1, 1), (1, 2),  -- Куликовская преподает в обеих группах
(2, 1), (2, 2),  -- Красильников преподает в обеих группах
(3, 1), (3, 2),  -- Рыжков преподает в обеих группах
(4, 1), (4, 2),  -- Коршиков преподает в обеих группах
(5, 1),          -- Фимина только в группе 201
(6, 2),          -- Баранникова только в группе 202
(7, 1), (7, 2);  -- Шпилев преподает в обеих группах

-- Функция для генерации случайного расписания
-- Для группы 201
INSERT INTO schedule (group_id, day_of_week, time_start, time_end, subject_id, lesson_type, room) VALUES
-- Понедельник
(1, 1, '10:10', '11:40', 1, 'Лекция', '304'),
(1, 1, '11:50', '13:20', 5, 'Лабораторный практикум', '208'),
(1, 1, '13:30', '15:00', 7, 'Лекция', '304'),
-- Вторник
(1, 2, '10:10', '11:40', 2, 'Лабораторный практикум', '208'),
(1, 2, '11:50', '13:20', 4, 'Лекция', '304'),
-- Среда
(1, 3, '13:30', '15:00', 6, 'Лабораторный практикум', '208'),
(1, 3, '15:10', '16:40', 3, 'Лекция', '304'),
-- Четверг
(1, 4, '10:10', '11:40', 8, 'Лабораторный практикум', '208'),
(1, 4, '11:50', '13:20', 10, 'Лекция', '304'),
-- Пятница
(1, 5, '15:10', '16:40', 9, 'Лекция', '304'),
(1, 5, '16:50', '18:20', 1, 'Лабораторный практикум', '208');

-- Для группы 202
INSERT INTO schedule (group_id, day_of_week, time_start, time_end, subject_id, lesson_type, room) VALUES
-- Понедельник
(2, 1, '11:50', '13:20', 3, 'Лекция', '304'),
(2, 1, '13:30', '15:00', 2, 'Лабораторный практикум', '208'),
-- Вторник
(2, 2, '10:10', '11:40', 6, 'Лекция', '304'),
(2, 2, '11:50', '13:20', 1, 'Лабораторный практикум', '208'),
(2, 2, '15:10', '16:40', 5, 'Лекция', '304'),
-- Среда
(2, 3, '10:10', '11:40', 4, 'Лабораторный практикум', '208'),
(2, 3, '13:30', '15:00', 7, 'Лекция', '304'),
-- Четверг
(2, 4, '15:10', '16:40', 9, 'Лабораторный практикум', '208'),
-- Пятница
(2, 5, '10:10', '11:40', 10, 'Лекция', '304'),
(2, 5, '11:50', '13:20', 8, 'Лабораторный практикум', '208'),
(2, 5, '16:50', '18:20', 2, 'Лекция', '304');

COMMIT;

-- Создание индексов для улучшения производительности
CREATE INDEX idx_schedule_group ON schedule(group_id);
CREATE INDEX idx_schedule_day ON schedule(day_of_week);
CREATE INDEX idx_subjects_teacher ON subjects(teacher_id);
CREATE INDEX idx_teacher_group_teacher ON teacher_group(teacher_id);
CREATE INDEX idx_teacher_group_group ON teacher_group(group_id);

-- Проверочные запросы
SELECT 'База данных успешно создана и заполнена!' as message;

-- Пример запроса: полное расписание группы 201
SELECT 
    g.name as group_name,
    CASE s.day_of_week 
        WHEN 1 THEN 'Понедельник'
        WHEN 2 THEN 'Вторник'
        WHEN 3 THEN 'Среда'
        WHEN 4 THEN 'Четверг'
        WHEN 5 THEN 'Пятница'
    END as day,
    s.time_start,
    s.time_end,
    sub.name as subject,
    t.name as teacher,
    s.lesson_type,
    s.room
FROM schedule s
JOIN groups g ON s.group_id = g.id
JOIN subjects sub ON s.subject_id = sub.id
JOIN teachers t ON sub.teacher_id = t.id
WHERE g.name = '201'
ORDER BY s.day_of_week, s.time_start;