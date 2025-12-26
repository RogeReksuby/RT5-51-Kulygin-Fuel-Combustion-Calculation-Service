# Fuel Calculation Async Service

Асинхронный микросервис на Python + Django REST Framework. Отвечает за расчёт энергии сгорания c участием следующих переменных:
- L — удельная теплота сгорания (Дж/кг)
- m — масса (кг)
- k — коэффициент (1 для газов, 0 иначе)
- V — объём (м³)
- V₀ — молярный объём (м³/моль)
- ρ — плотность (кг/м³)

Интерфейс:
- POST — принимает данные заявки, возвращает промежуточные и итоговую энергию
- После расчёта делает PUT-запрос в основной бэкенд для обновления статуса и результатов

Требования:
- Один входной токен для псевдо-авторизации
- Без БД, stateless
- Используется только при завершении заявки инженером-энергетиком

Запуск:
- `python manage.py runserver 8001`
Ссылки:
- **Лабораторная работа 1** — [бэкенд](https://github.com/RogeReksuby/RT5-51-Kulygin-Fuel-Combustion-Calculation-Backend/tree/front_pages_design)  
  Дизайн интерфейса в Figma, статические HTML-страницы, подключение MinIO.

- **Лабораторная работа 2** — [бэкенд](https://github.com/RogeReksuby/RT5-51-Kulygin-Fuel-Combustion-Calculation-Backend/tree/backend_database)  
  Моделирование БД (PostgreSQL), ER-диаграмма, подключение к бэкенду, логическое удаление.

- **Лабораторная работа 3** — [бэкенд](https://github.com/RogeReksuby/RT5-51-Kulygin-Fuel-Combustion-Calculation-Backend/tree/backend_API)  
  Реализация веб-сервиса (REST API), CRUD для топлива и заявок, расчёт энергии сгорания.

- **Лабораторная работа 4** — [бэкенд](https://github.com/RogeReksuby/RT5-51-Kulygin-Fuel-Combustion-Calculation-Backend/tree/backend_auth)  
  Авторизация (JWT + Redis), Swagger, подготовка ТЗ и расчёт аппаратных требований.

- **Лабораторная работа 5** — [фронтенд](https://github.com/RogeReksuby/RT5-51-Kulygin-Fuel-Combustion-Calculation-Frontend/tree/front_spa)  
  Базовое SPA на React (без Redux), интеграция с API, mock-данные.

- **Лабораторная работа 6**
- - [PWA](https://github.com/RogeReksuby/RT5-51-Kulygin-Fuel-Combustion-Calculation-Frontend/tree/front_redux_pwa)
- - [Tauri](https://github.com/RogeReksuby/RT5-51-Kulygin-Fuel-Combustion-Calculation-Frontend/tree/front_tauri_changes)
- - [Github Pages](https://github.com/RogeReksuby/RT5-51-Kulygin-Fuel-Combustion-Calculation-Frontend/tree/gh-pages)    
  Redux Toolkit, адаптивность, PWA, развёртывание на GitHub Pages, нативное приложение на Tauri.

- **Лабораторная работа 7** — [фронтенд](https://github.com/RogeReksuby/RT5-51-Kulygin-Fuel-Combustion-Calculation-Frontend/tree/front_redux_auth_swag)  
  Авторизация в React, интерфейс потребителя топлива, кодогенерация Axios, redux-thunk.

- **Лабораторная работа 8**
- - [фронтенд](https://github.com/RogeReksuby/RT5-51-Kulygin-Fuel-Combustion-Calculation-Frontend/tree/temp_moderator_branch)
- - [бэкенд](https://github.com/RogeReksuby/RT5-51-Kulygin-Fuel-Combustion-Calculation-Backend/tree/backend_with_async)
- - [сервис для расчета](https://github.com/RogeReksuby/RT5-51-Kulygin-Fuel-Combustion-Calculation-Service/tree/main)  
  Асинхронный сервис (Django), short polling, интерфейс инженера-энергетика.
 
  Полная система: [бэкенд (Go)](https://github.com/RogeReksuby/RT5-51-Kulygin-Fuel-Combustion-Calculation-Backend),
  [фронтенд (React)](https://github.com/RogeReksuby/RT5-51-Kulygin-Fuel-Combustion-Calculation-Frontend),
  [асинхронный расчёт (Django)](https://github.com/RogeReksuby/RT5-51-Kulygin-Fuel-Combustion-Calculation-Service).
