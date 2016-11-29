[![Code Climate](https://codeclimate.com/github/carwallaby/level-up/badges/gpa.svg)](https://codeclimate.com/github/carwallaby/level-up)

# Level Up
Level Up is a habit tracker application created as a final project for Hackbright Academy Engineering School for Women. It allows users to track each time they complete a task. The idea is for users to gain motivation to reach their goals by seeing tangible representation of their progress. Example usages could be trying to quit smoking or attempting to cook more meals at home.

## Frontend
The frontend of Level Up is built on **Angular 1.5.x** with client-side routing via [Angular UI-Router](https://github.com/angular-ui/ui-router). The layout is done mostly with Flexbox, CSS media queries for responsiveness, and lots of handmade (with love) CSS UI compenents. The calendar is a directive powered by **Moment.js**, and the trend chart is powered by **Chart.js**.

## Backend
The backend is built on **Flask** with **Python** and uses a **PostgreSQL** database with the **Flask SQLAlchemy** ORM. User authentication is handled by the Flask Login library. Times and timezones are handled on the backend by **Arrow**.
