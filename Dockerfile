# Используем образ Python
FROM python:3.11-slim

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# Копируем зависимости
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем остальные файлы проекта
COPY . .requirements

# Указываем порт для приложения
EXPOSE 5000

# Команда для запуска приложения
CMD ["python", "app.py"]