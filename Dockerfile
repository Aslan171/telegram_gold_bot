# Используем официальный Python 3.11
FROM python:3.11-slim

# Устанавливаем системные зависимости для asyncpg
RUN apt-get update && apt-get install -y gcc libpq-dev && rm -rf /var/lib/apt/lists/*

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем зависимости
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь проект
COPY . .

# Указываем команду запуска бота
CMD ["python", "zapusk.py"]
