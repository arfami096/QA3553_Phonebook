# Используем официальный легкий образ Python
FROM python:3.10-slim

# Установка рабочей директории внутри контейнера
WORKDIR /app

# Установка системных зависимостей (удалили устаревший libgconf-2-4)
RUN apt-get update && apt-get install -y \
    wget \
    curl \
    gnupg \
    unzip \
    libxi6 \
    libnss3 \
    libfontconfig1 \
    libxss1 \
    libasound2 \
    xvfb \
    && rm -rf /var/lib/apt/lists/*

# Установка Google Chrome
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | gpg --dearmor -o /usr/share/keyrings/google-chrome.gpg \
    && echo "deb [arch=amd64 signed-by=/usr/share/keyrings/google-chrome.gpg] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list \
    && apt-get update && apt-get install -y google-chrome-stable \
    && rm -rf /var/lib/apt/lists/*

# Установка Mozilla Firefox
RUN apt-get update && apt-get install -y firefox-esr && rm -rf /var/lib/apt/lists/*

# Копируем файл зависимостей и устанавливаем их
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Копируем весь проект внутрь контейнера
COPY . .