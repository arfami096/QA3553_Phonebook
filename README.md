# 📞 Automated UI Testing Framework (Phonebook App)

[![UI Tests CI](https://github.com/arfami096/QA3553_Phonebook/actions/workflows/ci.yml/badge.svg)](https://github.com/ВАШ_ЛОГИН/ИМЯ_РЕПОЗИТОРИЯ/actions/workflows/ci.yml)

Автоматизированный фреймворк для тестирования веб-приложения (UI) «Phonebook». Проект покрывает полный спектр требований: от позитивных сценариев и работы с обязательными полями до негативной валидации (алерты, ограничения по длине, символам) и проверки уникальности записей.

## 🛠 Стек технологий
* **Language:** Python
* **Test Runner:** Pytest
* **Automation Tool:** Selenium WebDriver
* **Architecture:** Page Object Model (POM)
* **CI/CD:** GitHub Actions (Headless Chrome)

## 📂 Структура проекта
* `pages/` — Классы страниц (Page Objects) для взаимодействия с элементами интерфейса.
* `tests/` — Наборы автотестов (позитивные, негативные сценарии, граничные значения).
* `utils/` — Вспомогательные утилиты, генератор тестовых данных и API-клиенты.
* `.github/workflows/` — Конфигурация CI/CD для автоматического запуска тестов на GitHub.

## 🚀 Как запустить тесты локально

1. Клонируйте репозиторий:
   ```bash
   git clone [https://github.com/ВАШ_ЛОГИН/ИМЯ_РЕПОЗИТОРИЯ.git](https://github.com/ВАШ_ЛОГИН/ИМЯ_РЕПОЗИТОРИЯ.git)