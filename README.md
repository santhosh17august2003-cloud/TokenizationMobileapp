# NLP Tokenization Demo

A web application built with Python and Flet for demonstrating how a real NLP tokenizer produces tokens and token IDs, and how a real embedding model produces embedding vectors.

## Features

- Validates input as exactly 3 alphabetic letters.
- Tokenizes with a Hugging Face tokenizer.
- Generates token embeddings with a Hugging Face model.
- Stores tokenization history in MySQL using parameterized queries.
- Shows history and supports clearing stored records.
- Handles validation, tokenizer, embedding, and database errors without crashing.

## Setup

1. Create and activate a virtual environment:

```bash
python -m venv .venv
.venv\Scripts\activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Configure MySQL in `.env`:

```env
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=your_password_here
MYSQL_DATABASE=tokenization_db
TOKENIZER_MODEL=distilbert-base-uncased
EMBEDDING_MODEL=distilbert-base-uncased
HF_HOME=.cache/huggingface
JWT_SECRET_KEY=replace_with_a_long_random_secret
```

Do not commit real database credentials or the JWT secret.

## MySQL Database

The app creates the database and table automatically when it can connect to MySQL. You can also create them manually:

```sql
CREATE DATABASE IF NOT EXISTS tokenization_db;

USE tokenization_db;

CREATE TABLE IF NOT EXISTS tokenization_history (
    id INT AUTO_INCREMENT PRIMARY KEY,
    request_id CHAR(36) NOT NULL,
    input_word VARCHAR(3) NOT NULL,
    token VARCHAR(255) NOT NULL,
    token_id INT NOT NULL,
    embedding JSON NOT NULL,
    embedding_dimension INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX request_id_idx (request_id)
);
```

## Run the Web App

```bash
python web.py
```

The first tokenizer or embedding run may take time while Hugging Face downloads the selected model into the local `.cache/huggingface` directory.

To use another port on Windows PowerShell:

```powershell
$env:PORT="8081"
python web.py
```

## Project Structure

```text
.
+-- web.py
+-- requirements.txt
+-- .env
+-- README.md
+-- config/
|   +-- settings.py
+-- database/
|   +-- db.py
+-- embedding/
|   +-- embedding_service.py
+-- tokenizer/
|   +-- tokenizer_service.py
+-- ui/
    +-- main_page.py
```
