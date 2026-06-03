# Используем легковесный образ Python
FROM python:3.12-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем requirements и устанавливаем зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем остальной код
COPY . .

# Сообщаем, что контейнер слушает этот порт
EXPOSE 8000

# Запускаем приложение (0.0.0.0 чтобы было доступно извне контейнера)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
