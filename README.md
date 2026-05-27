# 📘 Automatic Question Paper Generation System using NLP & Machine Learning

## 🚀 Overview

The **Automatic Question Paper Generation System** is an AI-powered application that automatically generates structured question papers from text or PDF content using **Natural Language Processing (NLP)** and **Machine Learning (ML)** techniques.

The system supports multiple question types such as:

* Multiple Choice Questions (MCQ)
* Fill in the Blanks (FIB)
* True/False
* Short Answer Questions

Additionally, the system classifies questions based on:

* **Bloom’s Taxonomy**
* **Difficulty Levels**

using trained **DistilBERT-based classification models**.

---

# 🎯 Problem Statement

Manual question paper creation is:

* Time-consuming
* Repetitive
* Difficult to balance difficulty levels
* Hard to maintain Bloom’s Taxonomy distribution

This project automates the entire process while allowing teachers to control:

* Question types
* Bloom levels
* Difficulty levels
* Distribution of questions

---

# ✨ Features

## ✅ Automatic Question Generation

Generate questions automatically from:

* Plain Text
* PDF Documents

---

## ✅ Supported Question Types

* MCQ
* Fill in the Blanks
* True/False
* Short Answer

---

## ✅ Bloom’s Taxonomy Classification

Questions are classified into:

* Remember
* Understand
* Apply
* Analyze
* Evaluate
* Create

---

## ✅ Difficulty Classification

Questions are categorized as:

* Easy
* Medium
* Hard

---

## ✅ User-Controlled Distribution

Teachers can specify:

* Number of questions
* Bloom level distribution
* Difficulty levels
* Question types

Example:

```json
{
  "Remember": 2,
  "Understand": 3
}
```

---

## ✅ ML + Rule-Based Hybrid System

The project combines:

* Machine Learning classification
* Rule-based filtering and correction

to improve output quality and enforce user-defined constraints.

---

## ✅ REST API Support

Built using **FastAPI** with:

* Background task processing
* Job status tracking
* Async generation workflow

---

# 🏗️ System Architecture

```text
User Input
   ↓
Text / PDF Processing
   ↓
Question Generation Engine
   ↓
ML Classification (DistilBERT)
   ↓
Filtering & Distribution Enforcement
   ↓
Final Question Paper
```

---

# 🧠 Technologies Used

## 🔹 Programming Language

* Python

---

## 🔹 Framework

* FastAPI

---

## 🔹 Machine Learning / NLP

* Hugging Face Transformers
* DistilBERT
* Text Classification Pipelines

---

## 🔹 Libraries


* Pydantic
* Transformers

---

## 🔹 API & Backend

* REST APIs
* Async Background Tasks

---

# 📂 Project Structure

```text
project/
│
├── routes/
│   └── generate.py
│
├── generators/
│   ├── mcq_generator.py
│   ├── fib_generator.py
│   ├── true_false_generator.py
│   └── short_answer_generator.py
│
├── jobs/
│   ├── generate_worker.py
│   └── job_store.py
│
├── utils/
│   └── predictors.py
│
├── models/
│   ├── bloom_classifier/
│   └── difficulty_final_model/
│
├── main.py
└── requirements.txt
```

---

# ⚙️ Installation

## 1️⃣ Clone Repository

```bash
git clone https://github.com/HELAN-S/Automatic_Question_Generation_.git
```

---

## 2️⃣ Navigate to Project

```bash
cd your-repository-name
```

---

## 3️⃣ Create Virtual Environment

```bash
python -m venv venv
```

---

## 4️⃣ Activate Environment

### Windows

```bash
venv\Scripts\activate
```

### Linux / Mac

```bash
source venv/bin/activate
```

---

## 5️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

# ▶️ Running the Project

```bash
uvicorn main:app --reload
```

---

# 📌 API Endpoints

## 🔹 Generate Questions

### POST `/generate`

### Request Example

```json
{
  "source_type": "text",
  "text": "Cybersecurity protects systems and data from cyber threats.",
  "num_questions": 5,
  "question_types": ["mcq", "fib"],
  "target_bloom_levels": ["Remember", "Understand"],
  "target_difficulty_levels": ["Easy"],
  "bloom_distribution": {
    "Remember": 2,
    "Understand": 3
  }
}
```

---

## 🔹 Get Job Status

### GET `/generate/status/{job_id}`

---

# 🧪 Example Output

```json
{
  "question": "What is cybersecurity?",
  "type": "short_answer",
  "bloom_level": "Remember",
  "difficulty": "Easy"
}
```

---

# 🔥 Key Improvements

## ✅ Bloom Distribution Enforcement

Ensures generated questions follow exact Bloom level distribution.

---

## ✅ Difficulty Filtering

Filters questions according to user-selected difficulty.

---

## ✅ Post-Processing Validation

Removes low-quality or mismatched questions.

---

## ✅ Hybrid ML + Rule-Based Approach

Improves reliability and consistency of generated output.

---

# 📊 Future Enhancements

* Semantic answer validation
* Automatic distractor generation
* Adaptive difficulty adjustment
* Web-based frontend UI
* Database integration
* Export to PDF / DOCX

---

# ⚠️ Limitations

* Output quality depends on training data quality
* Complex analytical questions may require further tuning
* Classification accuracy may vary for domain-specific content

---

# 👨‍💻 Author

### Your Name

* GitHub:https://github.com/HELAN-S

---

# 📜 License

This project is developed for educational and research purposes.

---

# ⭐ Acknowledgements

* Hugging Face Transformers
* FastAPI
* Bloom’s Taxonomy Framework
* Open-source NLP community
