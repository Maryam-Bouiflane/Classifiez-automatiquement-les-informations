---
title: P4 Classification App
emoji: 🌍
colorFrom: pink
colorTo: pink
sdk: docker
app_file: app.py
pinned: false
---

# Employee Churn Prediction App

# 1. Project Overview

Employee Churn Prediction App is a Machine Learning application designed to predict employee attrition risk based on HR data.

The project combines:

* Machine Learning
* FastAPI
* PostgreSQL
* Gradio
* GitHub Actions CI/CD
* Hugging Face Spaces

The objective is to provide HR teams with a decision-support tool capable of identifying employees at risk of leaving the company.

---

# 2. Business Context

The digital services company TechNova Partners is experiencing unusually high employee turnover.

Employee departures generate significant costs:

* Recruitment
* Onboarding
* Training
* Knowledge loss

The HR department wants to proactively identify employees at risk of leaving in order to implement retention strategies.

---

# 3. Solution Overview

The application predicts whether an employee is likely to leave the company based on HR indicators.

### Inputs
Employee HR data, examples of features:

* age
* genre
* revenu_mensuel
* heure_supplementaires

### Outputs

* Churn probability
* Binary prediction:

  * 0 = Employee likely to stay
  * 1 = Employee likely to leave

---

# 4. Project Architecture

The project is composed of four main components:

### Machine Learning Model

* Logistic Regression
* Scikit-learn Pipeline
* StandardScaler
* OneHotEncoder
* Optimized F1 threshold

### FastAPI Application

Provides:

* Prediction endpoint
* Employee retrieval endpoint
* Health monitoring endpoint
* OpenAPI documentation

### Gradio Interface

Mounted directly into FastAPI through:

```python
mount_gradio_app()
```

Accessible through:

```text
/ui
```

### PostgreSQL Database

Used to:

* Store employee data
* Store prediction logs
* Ensure full traceability

All prediction requests pass through the same trained model.

---

# 5. Technology Stack

### Backend

* Python
* FastAPI
* SQLAlchemy

### Machine Learning

* Scikit-learn
* Pandas
* Joblib

### Database

* PostgreSQL

### Frontend

* Gradio

### DevOps

* GitHub Actions
* Docker
* Hugging Face Spaces

---

# 6. Application Access

## Local Environment

Start the application:

```bash
poetry run uvicorn src.api:app --reload
```

Default URL:

```text
http://localhost:8000
```

Available Endpoints

| Method | Endpoint       | Description                   |
| ------ | -------------- | ----------------------------- |
| GET    | /              | API status                    |
| GET    | /health        | Health check                  |
| GET    | /employee/{id} | Retrieve employee information |
| POST   | /predict       | Predict employee churn        |


## Production Environment (Hugging Face Spaces)

REST API:

```text
https://maryamb123-p4-classification-app.hf.space/
```

Gradio Interface:

```text
https://maryamb123-p4-classification-app.hf.space/ui
```

---

# 7. Installation

## Prerequisites

* Python 3.12+
* Poetry
* PostgreSQL
* Git

## Clone Repository

```bash
git clone git@github.com:Maryam-Bouiflane/Classifiez-automatiquement-les-informations.git

cd Classifiez-automatiquement-les-informations
```

## Install Dependencies

```bash
poetry install --no-root
```

---

# 8. Configuration

Create a `.env` file at the root of the project:

```env
API_USER=app_backend
API_USER_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
```

---

# 9. Database Setup

## Database Creation

```bash
psql -U postgres -f database/create_db.sql
```

## Tables Creation

```bash
psql -U postgres -d churn_db -f database/create_tables.sql
```

## Security Configuration

```bash
psql -U postgres -d churn_db -f database/roles_and_permissions.sql
```

## Dataset Import

```bash
poetry run python database/insert_db.py
```

### Database Content

#### employees

Contains:

* Employee information
* Features used by the model

#### predictions_log

Contains:

* Employee identifier
* Input data
* Prediction result
* Prediction probability

---

# 10. Security

The application follows the Principle of Least Privilege.

Security mechanisms implemented:

* Dedicated database account (`app_backend`)
* Restricted PostgreSQL permissions
* Explicit GRANT strategy
* Revoked default privileges
* Environment-based secret management
* Prediction logging for auditability

Permissions granted:

* CONNECT
* USAGE
* SELECT
* INSERT

No administrative permissions are granted to the application.

---

# 11. API Documentation

FastAPI automatically generates OpenAPI documentation.

## Documentation

Swagger UI:

```text
/docs
```

ReDoc:

```text
/redoc
```

OpenAPI Specification:

```text
/openapi.json
```

---

# 12. Testing

Run all tests, with coverage report :

```bash
poetry run pytest --cov=src
```

Test categories:

### Unit Tests

Validate:

* Business logic
* Prediction functions
* Utility functions

### Functional Tests

Validate:

* API endpoints
* End-to-end prediction workflow

Objective:

* Detect regressions
* Improve reliability
* Validate application behavior

---

# 13. CI/CD Pipeline

Deployment is fully automated through GitHub Actions.

## Triggers

* Push on `main`
* Pull Request targeting `main`

## Pipeline Stages

1. Checkout repository
2. Install dependencies
3. Run unit tests
4. Run functional tests
5. Generate model artifacts
6. Generate threshold artifact
7. Build deployment package
8. Deploy to Hugging Face Spaces



