#!/bin/bash

# Выходим при любой ошибке
set -e

APP_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
echo "🚀 Установка Config Builder. Рабочая директория: $APP_DIR"

# 1. Установка системных зависимостей
echo "📦 Установка системных пакетов (PostgreSQL, Nginx, Python, Curl)..."
sudo apt-get update
sudo apt-get install -y python3-pip python3-venv postgresql postgresql-contrib nginx curl

# 2. Установка/Обновление Node.js 22 (Vite требует версию 20+)
NODE_MAJOR_VERSION=$(node -v 2>/dev/null | cut -d'v' -f2 | cut -d'.' -f1)
if [ -z "$NODE_MAJOR_VERSION" ] || [ "$NODE_MAJOR_VERSION" -lt 20 ]; then
    echo "📦 Установка/Обновление Node.js 22 (текущая: $(node -v 2>/dev/null || echo 'не установлена'))..."
    curl -fsSL https://deb.nodesource.com/setup_22.x | sudo -E bash -
    sudo apt-get install -y nodejs
else
    echo "✅ Подходящая версия Node.js уже установлена ($(node -v))"
fi


# 3. Настройка базы данных PostgreSQL
echo "🗄️ Настройка базы данных..."
sudo -u postgres psql -c "SELECT 1 FROM pg_roles WHERE rolname='admin'" | grep -q 1 || sudo -u postgres psql -c "CREATE USER admin WITH PASSWORD 'password';"
sudo -u postgres psql -c "SELECT 1 FROM pg_database WHERE datname='configdb'" | grep -q 1 || sudo -u postgres psql -c "CREATE DATABASE configdb OWNER admin;"

echo "✅ База данных configdb и пользователь admin готовы."

# 4. Настройка Backend (Python)
echo "🐍 Настройка Python окружения..."
cd "$APP_DIR/backend"
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
deactivate

# 5. Сборка Frontend (Vue.js)
echo "🎨 Сборка фронтенда..."
cd "$APP_DIR/frontend"
npm install
npm run build

echo "✅ Фронтенд успешно собран в папку dist/"

# 6. Настройка Nginx
echo "🌐 Настройка Nginx..."
sudo cp "$APP_DIR/config-builder.nginx" /etc/nginx/sites-available/config-builder
sudo ln -sf /etc/nginx/sites-available/config-builder /etc/nginx/sites-enabled/config-builder
# Удаляем дефолтный сайт, если он мешает
# sudo rm -f /etc/nginx/sites-enabled/default
sudo nginx -t
echo "✅ Nginx настроен."

# 7. Настройка Systemd сервиса
echo "⚙️ Настройка Systemd сервиса..."
sudo cp "$APP_DIR/config-builder.service" /etc/systemd/system/config-builder.service
sudo systemctl daemon-reload
sudo systemctl enable config-builder
echo "✅ Сервис добавлен в автозагрузку."

# Завершение
echo "=================================================="
echo "🎉 Установка завершена!"
echo ""
echo "Для ЗАПУСКА приложения выполните:"
echo "sudo systemctl start config-builder"
echo ""
echo "Проверить СТАТУС:"
echo "sudo systemctl status config-builder"
echo ""
echo "Перезапустить NGINX (если не стартанул сам):"
echo "sudo systemctl restart nginx"
echo ""
echo "Приложение будет доступно по адресу: http://<IP_СЕРВЕРА>:8800"
echo "=================================================="
