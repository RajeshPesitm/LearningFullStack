
## 🎯 Refactor Made: Safley Delete Message Model and messages table
New change detected... **initialising schema removal protocol** 🧑‍💻

You want to:
✅ **Remove**:

* `Message` SQLAlchemy model
* `MessageInput` Pydantic model
* `/submit-message` route
* `/delete-message` route
* The table itself from your MySQL database

✅ **Retain**:

* `GET /` route
* `GET /init-db` route
* `get_db()` dependency
* Database initialization capability

---

Below is a **step-by-step guide** to safely perform this cleanup:

---

## 🧾 **1️⃣ Clean Up `models.py`**

**Edit to remove everything related to messages:**

```python
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
```

✅ That’s it. The model is fully removed from your code.

---

## 🗂️ **2️⃣ Remove Routes from `main.py`**

**Delete these functions completely:**

* `submit_message()`
* `delete_message_by_email()`

**Be sure to also remove these imports at the top:**

```python
from .models import Message, MessageInput
```

---

✅ This removes all endpoints using the `messages` table.

---

## 🗄️ **3️⃣ Drop the Table from MySQL**

Since you have **MySQL Admin access**, simply run:

```sql
DROP TABLE IF EXISTS messages;
```
You can also do the same using GUI

✅ This ensures your database volume is cleaned up.

---

## 🛡️ **4️⃣ Verify**

**Restart your FastAPI app**, then test:

* `GET /` → should still work
* `GET /init-db` → should work, but now it will not recreate `messages` (since no models are defined)

✅ **Note:** `Base.metadata.create_all()` will do nothing now, because there are no models left in `Base`.

---

## 🧠 **5️⃣ Considerations**

> **Optional cleanup:**

* You might consider eventually removing `Base` entirely if you no longer need any tables.
* If you plan to add new models later, keep `Base` as is.

✅ You don’t need to change `get_db()` in `database.py`; it remains useful for future queries.

---

## 🔍 **Summary Checklist**

✅ Remove:

* `Message` and `MessageInput` from `models.py`
* Imports and related routes from `main.py`

✅ Drop table:

```sql
DROP TABLE IF EXISTS messages;
```

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

### 🧪 Fails Now: Any number of times: POST request:/submit-message

```bash
curl -X POST http://localhost:8000/submit-message \
  -H "Content-Type: application/json" \
  -d '{"name":"Alice", "email":"alice@example.com", "message":"Hi!"}'
```

### 🧪 Fails Now: Any number of times: DELETE request: /delete-message

```bash
curl -X DELETE "http://localhost:8000/delete-message?email=alice@example.com"
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

  build  
  Note: use option --no-cache if required  

```bash
docker build -t myapp-backend .
```
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