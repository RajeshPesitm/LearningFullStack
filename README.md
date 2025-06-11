### ✅ **Mini Project 1: Full-stack Form Submission Without Auth**

> 📌 Goal: Simple contact form with no login. Data goes into MySQL. Adminer used to verify stored data.
## 🎯 Goal
Supported endpoints:

    GET / → confirms app is running 

    GET /init-db → initializes DB
Testing:
```bash
curl http://localhost:8000/init-db
```

**👉 Step 1: `docker-compose.yml` + MySQL + Adminer + blank FastAPI and React services**


## My Correction:
👉 Step 1: docker-compose.yml + MySQL + Adminer + blank FastAPI and React services
Shall I generate this? 
Yes But please consider following:

I prefer to Run Fast API, MySQL, Adminer without docker-compose.yml? The reason is, in the past, FASTAPI try to connect to DB before it gets ready and failed.
I prefer commands like
docker network create myapp-net

Also Because i am in development stage i need a switch in backend that alows me to connect to DB manually so that i can wait untill DB gets ready.
once this set up is tested fine, can i include docker-compose.yml

To give you more clarity:
Trigger via a Backend Route (e.g., /init-db)

    FastAPI boots without DB.

    When you know MySQL is ready, you curl or http to localhost:8000/init-db.

    This triggers the DB connection and setup.

Prefer This layout if possible:
project-root/  
├── backend/  
│   ├── app/  
│   │   ├── main.py         ← starts FastAPI with /init-db (or wherever appropriate)  
│   │   └── database.py           ← db connection logic  
│   │   └── models.py           ← db model  
│   ├── Dockerfile  
│   ├── requirements.txt  
├── frontend/  
│   └── (will add later)  

The initial code should be in such a way that we can easily include another route to insert row in to "Messages" table  

## Response I Got
Perfect. Your **development-first** approach is solid and ideal for learning.

You want to:

* Start FastAPI **without DB initially**
* Use `docker` CLI (no `docker-compose` for now)
* Trigger DB connection manually via `/init-db`
* Use a layout that cleanly separates `main.py`, `database.py`, and `models.py`
* Prepare for a `POST /submit-message` route later

Let’s do exactly that ✅

---

## 🏗️ PHASE: Manual Docker Setup (MySQL + Adminer + FastAPI)

---

### ✅ 1. **Create Docker Network**

Run this once:

```bash
docker network create myapp-net
```

---

### ✅ 2. **Run MySQL Container**

```bash
docker run -d \
  --name myapp-mysql \
  --network myapp-net \
  -e MYSQL_ROOT_PASSWORD=root \
  -e MYSQL_DATABASE=myapp_db \
  -p 3306:3306 \
  -v myapp-mysql-data:/var/lib/mysql \
  mysql:5.7
```

---

### ✅ 3. **Run Adminer (to inspect MySQL)**

```bash
docker run -d \
  --name myapp-adminer \
  --network myapp-net \
  -p 8080:8080 \
  adminer
```

Visit: [http://localhost:8080](http://localhost:8080)

* Server: `myapp-mysql`
* User: `root`
* Password: `root`
* DB: `myapp_db`

---

### ✅ 4. **Project Layout**

```
project-root/
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── database.py
│   │   └── models.py
│   ├── Dockerfile
│   ├── requirements.txt
```
commands to create the above layout:
```bash
mkdir -p backend/app
touch backend/Dockerfile
touch backend/requirements.txt
touch backend/app/database.py
touch backend/app/main.py
touch backend/app/models.py
```
---

### ✅ 5. **`requirements.txt`**
---

### ✅ 6. **`models.py`**
---

### ✅ 7. **`database.py`**
---

### ✅ 8. **`main.py`**
---

### ✅ 9. **`Dockerfile`**
---

### ✅ 10. **Build and Run FastAPI Container**
  From inside project-root/backend  
  build
```bash
docker build -t myapp-backend .
```
  run
```bash
docker run -d \
  --name myapp-backend \
  --network myapp-net \
  -p 8000:8000 \
  myapp-backend
```

---

### ✅ 11. **Trigger DB Setup**

After MySQL is ready (check with Adminer), run:

```bash
curl http://localhost:8000/init-db
```

Expected response:

```json
{"status": "Database initialized successfully"}
```

Then check in Adminer → `messages` table will be created.

---

## ✅ Useful commands to handle containers
* stop
```bash
docker stop myapp-backend &&
docker stop myapp-adminer &&
docker stop myapp-mysql
```
* start
```bash
docker start myapp-mysql &&
docker start myapp-adminer &&
docker start myapp-backend
```
* logs
```bash
docker logs -f myapp-mysql
```
## ✅ Ready for Next Step?

Once this base is stable:

* You can now easily add `POST /submit-message` route in `main.py` (it will use `SessionLocal`)
* Later you can convert this into a `docker-compose.yml` setup

Would you like me to now generate the `POST /submit-message` route and DB session handling logic next?

