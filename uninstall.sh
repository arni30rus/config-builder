#!/bin/bash

# Выходим при любой ошибке
set -e

# Проверяем, запущен ли скрипт от root
if [ "$EUID" -ne 0 ]; then
  echo "❌ Пожалуйста, запустите скрипт с правами суперпользователя: sudo ./uninstall.sh"
  exit 1
fi

echo "⚠️  ВНИМАНИЕ: Этот скрипт удалит сервис Config Builder, его базу данных и конфигурации!"
read -p "Вы уверены, что хотите продолжить? (y/N): " confirm
if [[ "$confirm" != "y" && "$confirm" != "Y" ]]; then
    echo "Отмена удаления."
    exit 0
fi

APP_DIR="/data/projects/config-builder"

# 1. Остановка и удаление Systemd сервиса
echo "🛑 Остановка и удаление systemd сервиса..."
systemctl stop config-builder 2>/dev/null || true
systemctl disable config-builder 2>/dev/null || true
rm -f /etc/systemd/system/config-builder.service
systemctl daemon-reload
echo "✅ Сервис удален."

# 2. Удаление конфигурации Nginx
echo "🌐 Удаление конфигурации Nginx..."
rm -f /etc/nginx/sites-enabled/config-builder
rm -f /etc/nginx/sites-available/config-builder
# Перезагружаем Nginx, чтобы он перестал слушать порты этого сайта
systemctl reload nginx 2>/dev/null || true
echo "✅ Конфиг Nginx удален."

# 3. Удаление базы данных и пользователя PostgreSQL
echo "🗄️ Удаление базы данных и пользователя PostgreSQL..."
sudo -u postgres psql -c "DROP DATABASE IF EXISTS configdb;" 2>/dev/null || echo "Предупреждение: Не удалось удалить БД (возможно, она уже удалена)."
sudo -u postgres psql -c "DROP USER IF EXISTS admin;" 2>/dev/null || echo "Предупреждение: Не удалось удалить пользователя (возможно, он уже удален)."
echo "✅ База данных и пользователь удалены."

# 4. Удаление исходного кода (спрашиваем пользователя)
echo ""
read -p "❓ Хотите ли вы полностью удалить папку с исходным кодом ($APP_DIR)? (y/N): " del_code
if [[ "$del_code" == "y" || "$del_code" == "Y" ]]; then
    rm -rf "$APP_DIR"
    echo "🗑️ Папка с исходным кодом удалена."
else
    echo "📁 Папка с исходным кодом оставлена нетронутой."
fi

echo "=================================================="
echo "🎉 Приложение Config Builder успешно удалено с сервера!"
echo "================================================"
