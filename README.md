# Bujji Bus Booking Engine
A full-featured bus booking engine built with **FastAPI**, **SQLAlchemy**, and **SQLite**, supporting:
- Operator login & JWT authentication
- Bus creation & seat mapping
- Route & stop management
- Passenger-side search with filters
- Booking with seat selection & PNR generation
- Booking cancellation (partial/full)
- Booking summary and seat map availability
- Support for recurring routes and segment-based availability
---
## Features
- JWT-based authentication for operators
- Search routes with filters like AC, time of day, price range
- Real-time seat availability from booking records
- Partial segment matching in search
- Full booking lifecycle including passengers and cancellation
- Clean architecture using Unit of Work, Repository, and Services
- SQLite support with SQLAlchemy ORM
---
## Setup Instructions
### 1. Clone the Repo
```bash
git clone https://github.com/surya0210/bujji-bus.git
cd bujji-bus
### 2. Setup VM
<pre><code>```bash python3 -m venv bujji_app source bujji_app/bin/activate # On Windows use `bujji_app\Scripts\activate` ``` </code></pre>
### 3. Install Requirements
<pre><code> ``` pip3 freeze > requirements.txt```</code></pre>

### 4.Initalize the database
<pre><code>```python3 build_db.py```</pre></code>

### 5.Run the app
<pre><code>```python3 run_server.py```</pre></code>

###6. API Docs
Redoc: http://0.0.0.0:8001/bujji-app-api-redoc
Swagger:http://0.0.0.0:8001/bujji-app-api



