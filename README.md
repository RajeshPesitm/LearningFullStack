# Major Learnings and updates in this commit
# Learnings:
✨ Why You need __init__.py in /app folder?

    You need __init__.py so Python treats your app directory as a proper package, making your imports reliable everywhere. in other words, This declares app as a Python package. Otherwise You cant run scripts such as "# pytest app/test_main.py"

---
    The another reson is 
        insted you use
        from . import database
        from .models import Message, MessageInput
        from .database import get_db
            
        you use
        from app import database
        from app.models import Message, MessageInput
        from app.database import get_db

✨ In Dockerfile

    ✅ Below line ensures Python always knows your /app folder is the module root.
    ENV PYTHONPATH=/app



# Upgrades Planned:
✨ simplify test runs by mounting your codebase with -v so you don’t have to rebuild every time you edit tests.  
✅ Next Steps You Might Consider:

    Implement assigning subjects to faculties (many-to-many)

    Add update endpoints for each table

    Secure routes with authentication

    Generate OpenAPI docs (/docs)

✨ Ask AI that
    i want to create distibuted databse using 4 computers connected using LAN.
And in the same LAN i use another computers running FASTAPI to read and write data into this distributed database. And many Rest+VITE servers individual computers that end users use to read and write data into this distributed database.
I prefer
1. Distributed database that span across Four Computers (even if one computer fails, other three still provides availability)
2. If possible How can i make FASTAPI highly available (can i use Dockerised FASTAPI Backend)
3. Should i prefer Dockerised REACT + VITE frontend

tell me how i can achive this:
My Hardware resource:
1. LAN connecting 25 Computers (All are Desktop Ubuntu 16GB RAM + SSD Hard Disk)


## 🎯 Refactor Made: New Model "Department" Created
New chat detected… **initialising new database model build mode** 🧑‍💻

Let’s proceed step by step:

---

## 🧭 **Project Objective**

✅ Create **three tables**:

* Student
* Subject
* Faculty

✅ Define **relationships**:

* `Student` and `Subject`: each has `semester` (n:1 to semesters)
* `Faculty` handles many `Subjects` (n\:m)

✅ Define **Pydantic models** for validation.

✅ Expose **API routes** to:

* Insert/Delete Students, Subjects, Faculties
* Query students by semester
* Query faculties by subject
* Query subjects by faculty

---

## 🧮 **1️⃣ SQLAlchemy Models**

Below is a clean **pseudocode plan** for your models.

---

### **🎓 Student**

| Column   | Type    | Notes                |
| -------- | ------- | -------------------- |
| usn      | String  | PK, e.g., 4PM22CS001 |
| name     | String  |                      |
| semester | Integer | 1–8                  |

---

### **📚 Subject**

| Column        | Type    | Notes            |
| ------------- | ------- | ---------------- |
| subject\_code | String  | PK, e.g., BCS305 |
| name          | String  |                  |
| semester      | Integer | 1–8              |

---

### **👩‍🏫 Faculty**

| Column | Type   | Notes            |
| ------ | ------ | ---------------- |
| code   | String | PK, 4-digit code |
| name   | String |                  |

---

### **🔗 FacultySubjects Association Table**

| Column        | Type   | Notes                        |
| ------------- | ------ | ---------------------------- |
| faculty\_code | String | FK to Faculty(code)          |
| subject\_code | String | FK to Subject(subject\_code) |

---

## **2️⃣ SQLAlchemy Model Code**

Let’s implement the **full code** for `models.py`:


---

## 🛠️ **3️⃣ Database Initialization**

**No change needed to `database.py`**:

* `Base.metadata.create_all()` will create all tables.

---

## 🧩 **4️⃣ Routes Overview**

✅ **Student routes:**

* `POST /student` insert
* `DELETE /student/{usn}` delete
* `GET /students/semester/{semester}` list all students in a semester

✅ **Subject routes:**

* `POST /subject` insert
* `DELETE /subject/{subject_code}` delete

✅ **Faculty routes:**

* `POST /faculty` insert
* `DELETE /faculty/{code}` delete
* `GET /faculty/by-subject/{subject_code}` list faculties handling subject
* `GET /subject/by-faculty/{faculty_code}` list subjects handled by faculty

---

## ✨ **5️⃣ Example Route Implementation (FastAPI)**

Below are **example route signatures** you can copy into `main.py`:



✅ You can **expand** this with:

* Assign/Unassign subjects to faculties
* Validation

---

## 🏁 **6️⃣ Next Steps**

1. Copy the models code into `models.py`
2. Update `main.py` with these endpoints
3. Restart your FastAPI app
4. Call `/init-db` to create tables

✅ You’re ready to test!

If you want help with **unit tests or example payloads**, I’m here.

✅ Restart and test. (Assuming MySql and Adminer are running)

```
docker stop myapp-backend
```
#### Once Changes are made to backend:
commands to rebuild and restart containers:
#### From Project Root:

  remove old  
```
docker rm myapp-backend
```

#### Very Important: From inside project-root/backend 

  build  
  Note: use option --no-cache if required  

```bash
docker build -t myapp-backend .
```

##### Not to forget to Remove dangling null images
```bash
docker rmi $(docker images -f dangling=true -q)
```
#### Only Once: run Backend
```
docker run -d \
  --name myapp-backend \
  --network myapp-net \
  -p 8000:8000 \
  myapp-backend
```
## Test the Fast API Routes
### 🧪 Once Every Time Container restarts: get request:  /init-db: Works

```bash
curl http://localhost:8000/init-db
```





# If you are doing Fresh Start
## Compile and Run the Project
### ✅ 1. **Only Once: Create Docker Network**

Run this once:

```bash
docker network create myapp-net
```

---

### ✅ 2. **only Once: Run MySQL Container**

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

### ✅ 3. **Only Once: Run Adminer (to inspect MySQL)**

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



#### From Project Root: start MysQL+Adminer (no need to run again and again)

```bash
docker start myapp-mysql &&
docker start myapp-adminer &&
```

  #### From Project Root:
#### Only Once: run backend 

```bash
docker run -d \
  --name myapp-backend \
  --network myapp-net \
  -p 8000:8000 \
  myapp-backend
```

### ✅ 10. **Every time code is updated: Build and Run FastAPI Container**
#### Once Changes are made to backend:
commands to rebuild and restart containers:
#### From Project Root:

  remove old  
```
docker rm myapp-backend
```

#### Very Important: From inside project-root/backend 
```bash
docker build -t myapp-backend .
```
  build  Note: use option --no-cache if required  

#### Note:If you want to rebid From Project Root
```bash
docker build -t myapp-backend ./backend
```
  build  Note: use option --no-cache if required  

#### Only Once: run Backend
```
docker run -d \
  --name myapp-backend \
  --network myapp-net \
  -p 8000:8000 \
  myapp-backend
```
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


## Useful Commands to Handle Docker Containers

```bash
docker images
docker ps
```
##### Remove dangling null images
```bash
docker rmi $(docker images -f dangling=true -q)
```
##### Start or stop (followed by docker run)
```bash
docker start myapp-mysql &&
docker start myapp-adminer &&
```
```bash
docker stop myapp-backend && 
docker stop myapp-adminer && 
docker stop myapp-mysql
```
##### Rebuild and run Backend
```bash
docker stop myapp-backend &&
docker rm myapp-backend &&
docker rmi $(docker images -f dangling=true -q) &&
docker build -t myapp-backend ./backend &&
docker run -d   --name myapp-backend   --network myapp-net   -p 8000:8000   myapp-backend &&
```

##### Test Inside Backend Container
```bash
docker exec -it myapp-backend /bin/bash
pytest app/test_main.py
pytest app/test_main.py::test_add_student
```

Server Logs:
```bash
docker logs -f myapp-backend
```






