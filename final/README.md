# CPS420 Final Project

This project is a FastAPI-based application for managing items. Below are the instructions to set up the virtual environment, install dependencies, and run the application and tests.

---

## **Setup Instructions**

### **2. Set Up a Virtual Environment**

#### **Mac/Linux**
```bash
python3 -m venv venv
source venv/bin/activate
```

#### **Windows**
```bash
python -m venv venv
.\venv\Scripts\activate
```

---

### **3. Install Dependencies**
```bash
pip install -r requirements.txt
```

---

## **Run the Application**

### **1. Start the FastAPI Application**
Run the following command to start the application:
```bash
python src/main.py
```

The application will be available at:  
[http://127.0.0.1:8000](http://127.0.0.1:8000)

---

## **Run the Tests**

### **1. Run All Tests**
Use the following commands to navigate to the test directory and run the tests:
```bash
cd src/test/
python test_main.py
```

---

### **Test Results**
#### POST /item/ 
##### Creating an item:
    Status code:  201
    Response:  {'name': 'Ronald Thomas', 'description': 'Specific sign measure discussion relate.\nMilitary reality since arm contain. Their him ask east.\nOr it why begin. Air society example must.', 'value': 763.65, 'id': 1}

##### Creating an item without a description:
    Status code:  201
    Response:  {'name': 'Christopher Ball', 'description': None, 'value': 152.31, 'id': 2}

##### Creating an item without a name:
    Status code:  422
    Response:  {'detail': [{'type': 'missing', 'loc': ['body', 'name'], 'msg': 'Field required', 'input': {'description': 'Half think figure great according social. Know culture room half Republican also walk American. Home sit age turn behavior wait. Simple education detail white general foreign.', 'value': 398.59}}]}

#### GET /item/{id}
##### Getting first item:
    Status code:  200
    Response:  {'name': 'Ronald Thomas', 'description': 'Specific sign measure discussion relate.\nMilitary reality since arm contain. Their him ask east.\nOr it why begin. Air society example must.', 'value': 763.65}
##### Getting second item:
    Status code:  200
    Response:  {'name': 'Christopher Ball', 'description': None, 'value': 152.31}
##### Getting item with id 3 should have status code 404:
    Status code:  404
##### Getting item with id 2 should have status code 200:
    Status code:  200

---

## **Note**
- Use `deactivate` to exit the virtual environment when done.