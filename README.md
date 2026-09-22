# AI SQL Assistant using Groq Function Calling

## Overview

This project demonstrates how an AI model can interact with a database using Function Calling.

The user asks questions in plain English, and the AI:

1. Understands the request
2. Converts the request into a SQL query
3. Executes the query on a SQLite database
4. Reads the database results
5. Returns a human-friendly answer

This project is designed for learning:

- Function Calling
- Natural Language to SQL
- SQLite Integration
- AI Tool Usage
- Safe Database Access

---

## Project Structure

```text
AI-SQL-Assistant/
│
├── app.py
├── create_db.py
├── employees.db
├── requirements.txt
└── README.md
```

---

## Architecture

```text
User Question
      │
      ▼
Groq GPT-OSS-20B
      │
      ▼
Function Calling
      │
      ▼
run_sql()
      │
      ▼
SQLite Database
      │
      ▼
Database Results
      │
      ▼
AI Response
```

---

## Database Creation

Run the following command:

```bash
python create_db.py
```

This creates a SQLite database named:

```text
employees.db
```

### Database Schema

Table Name:

```sql
employees
```

Columns:

| Column | Type |
|----------|----------|
| empid | INTEGER |
| name | TEXT |
| department | TEXT |

### Sample Data

| empid | name | department |
|--------|--------|------------|
| 1001 | Vamsi | Security |
| 1002 | Ravi | HR |

---

## How It Works

### Example 1

User:

```text
Show all employees
```

AI Generates:

```sql
SELECT * FROM employees;
```

Database Returns:

```text
[(1001, 'Vamsi', 'Security'),
 (1002, 'Ravi', 'HR')]
```

AI Response:

```text
There are 2 employees in the database.
```

---

### Example 2

User:

```text
Show employees in HR department
```

AI Generates:

```sql
SELECT * FROM employees
WHERE department='HR';
```

Database Returns:

```text
[(1002, 'Ravi', 'HR')]
```

AI Response:

```text
Ravi works in the HR department.
```

---

## Installation

Install dependencies:

```bash
pip install openai
```

---

## Configure Groq API

Update your API key inside `app.py`:

```python
client = OpenAI(
    api_key="YOUR_GROQ_API_KEY",
    base_url="https://api.groq.com/openai/v1"
)
```

---

## Run Application

```bash
python app.py
```

Example:

```text
Ask Database > show all employees

Generated SQL:
SELECT * FROM employees;

Database Result:
[(1001, 'Vamsi', 'Security'),
 (1002, 'Ravi', 'HR')]

AI Response:
There are 2 employees in the database.
```

---

## Security Controls

To prevent database modification, the application blocks:

- DROP
- DELETE
- UPDATE
- INSERT
- ALTER
- CREATE
- TRUNCATE

Only safe SELECT queries are allowed.

---

## Example Questions

```text
Show all employees

Show employee ID 1001

Show employees in Security department

List all departments

How many employees are available?

Show HR employees
```

---

## Technologies Used

- Python
- SQLite
- OpenAI SDK
- Groq API
- Function Calling
- GPT-OSS-20B

---

## Learning Outcomes

This project demonstrates:

- AI Function Calling
- Tool Integration
- Natural Language Processing
- SQL Query Generation
- Database Query Execution
- Safe AI Application Design

---

## Author

Kommireddy Vamsi

Lotus Notes Administrator | Web Application Security Analyst | AI Enthusiast
