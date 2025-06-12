# 📘 **FastAPI + SQLAlchemy: How `/submit-message` Interacts with the Database**

## 🎯 Goal
Supported endpoints:

    GET / → confirms app is running (Already done in previous commit)

    GET /init-db → initializes DB (create tables) (Already done in previous commit)

    POST /submit-message → accepts form input and stores in DB (New addition in this commit)

Testing:  
```bash
curl http://localhost:8000/init-db
```
send a POST request:  

```bash
curl -X POST http://localhost:8000/submit-message \
  -H "Content-Type: application/json" \
  -d '{"name":"Alice", "email":"alice@example.com", "message":"Hi!"}'
```

Enable users to submit messages via a REST API. FastAPI handles:

* **Input validation**
* **Database session management**
* **Data persistence**

---
# 📘 **FastAPI + SQLAlchemy: How `/submit-message` Interacts with the Database**
## 📁 Project Structure: (Key changes)

```
project-root/
├── backend/
│   └── app/
│       ├── main.py        # FastAPI app with routes: Modified
│       ├── database.py    # DB engine, session, and get_db() dependency: Modified
│       └── models.py      # SQLAlchemy model + Pydantic input model: Modified
```



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


### ✅ 10. **Every time code is updated: Build and Run FastAPI Container**
### Once Changes are made to backend:
commands to rebuild and restart containers:
### From Project Root:

  remove old  
```
docker rm myapp-backend
```


### Very Important: From inside project-root/backend 

  build  
  Note: use option --no-cache if required  

```bash
docker build -t myapp-backend .
```

### From Project Root: start MysQL+Adminer (no need to run again and again)

```bash
docker start myapp-mysql &&
docker start myapp-adminer &&
```

  ### From Project Root:
run backend

```bash
docker run -d \
  --name myapp-backend \
  --network myapp-net \
  -p 8000:8000 \
  myapp-backend
```
---

## 🧩 Key Files and Responsibilities

### 🔹 `models.py`

* **Defines the DB model (`Message`)** using SQLAlchemy
* **Defines the request schema (`MessageInput`)** using Pydantic

```python
class Message(Base):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    email = Column(String(100))
    message = Column(Text)

class MessageInput(BaseModel):
    name: constr(strip_whitespace=True, min_length=1)
    email: EmailStr
    message: constr(strip_whitespace=True, min_length=1)
```

---

### 🔹 `database.py`

* **Holds global `engine` and `SessionLocal` objects**
* **Provides `init_db()`** → Initializes database and creates tables
* **Provides `get_db()`** → Dependency used by FastAPI to manage DB sessions

```python
def get_db():
    if SessionLocal is None:
        raise HTTPException(503, "DB not initialized. Call /init-db.")
    db = SessionLocal()
    try:
        yield db   # hand off control to route
    finally:
        db.close() # cleanup after route completes
```

---

### 🔹 `main.py`

* Defines FastAPI app
* Contains the `/submit-message` route
* Uses `Depends(get_db)` to inject the DB session

```python
@app.post("/submit-message")
def submit_message(payload: MessageInput, db: Session = Depends(get_db)):
    new_msg = Message(
        name=payload.name,
        email=payload.email,
        message=payload.message,
    )
    db.add(new_msg)
    db.commit()
    db.refresh(new_msg)
    return {"message": "Submitted", "id": new_msg.id}
```

---

## 🔄 How It All Works — Step-by-Step

### 🧪 Once Every Time Container restarts: /init-db:

```bash
curl http://localhost:8000/init-db
```

### 🧪 Any number of times: When you send a POST request:

```bash
curl -X POST http://localhost:8000/submit-message \
  -H "Content-Type: application/json" \
  -d '{"name":"Alice", "email":"alice@example.com", "message":"Hi!"}'
```

---

### 🧠 FastAPI handles it like this:

1. ✅ **Validates** the incoming JSON using `MessageInput` (Pydantic)
2. 🔄 **Calls `get_db()`** because `submit_message()` depends on it
3. 💾 `get_db()`:

   * Creates a `SessionLocal()` DB session
   * `yield`s the session (`db`) to `submit_message()`
    try:  
        yield db  
4. 📥 `submit_message()` uses the session (`db`) to:

   * Insert a new row into the `messages` table
   * Commit the transaction
5. 🔚 After route returns, FastAPI automatically calls the code **after** `yield` in `get_db()`:

   * Calls   
       finally:  
        db.close()
   * Closes the DB connection cleanly

---

## 🔑 Key Concepts

| Concept                         | Description                                                                   |
| ------------------------------- | ----------------------------------------------------------------------------- |
| `Depends(get_db)`               | Tells FastAPI to call `get_db()` before running the route.                    |
| `yield` in `get_db()`           | Creates a temporary session, which is cleaned up after the route is executed. |
| Pydantic model (`MessageInput`) | Validates user input: ensures fields are not empty and email is valid.        |
| SQLAlchemy model (`Message`)    | Maps the data to the `messages` table in MySQL.                               |

---

## ✅ Benefits of This Pattern

* 🧼 Clean resource management (DB sessions are always closed)
* 🚫 Prevents accessing DB before it's initialized
* 🔁 Easy to reuse `get_db()` in other routes
* ✅ Scales well when more routes or models are added

---

Would you like a visual diagram to go with this explanation for student slides?
