# CodeLoop

CodeLoop is a Python learning and practice web application designed to help beginners learn concepts, practice coding, understand their mistakes, and track their progress.

Instead of only reading tutorials, CodeLoop follows a simple learning loop:

**Learn → Practice → Debug → Review → Improve**

---

## 📚 Features

### 🐍 Python Learning Path

CodeLoop provides a structured learning path for Python beginners.

- 12 structured Python topics
- Topic explanations and examples
- Learning status tracking

### 📖 Reference Tutorials

Additional tutorials are provided for important Python sub-concepts.

These tutorials help learners explore concepts in more detail when needed.

### 💻 Coding Problem Bank

CodeLoop provides coding problems for practicing Python concepts.

- Basic and intermediate Python problems
- In-browser coding editor
- Run Python code and view the actual output

### 🧠 Debug Your Thinking

CodeLoop encourages learners to understand their mistakes instead of simply viewing the correct answer.

- Explain what you were trying to do
- Describe what you expected to happen
- Understand the reason behind a mistake
- Reveal the correct answer after reflection

### ❌ My Mistakes

Mistakes can be saved and reviewed later as learning material.

- Save mistakes for later review
- Revisit previous mistakes
- Learn from previous coding attempts

### ❓ Confusing Parts

This section focuses on commonly confused Python concepts.

Examples include:

- `=` vs `==`
- `append()` vs `extend()`
- `remove()` vs `pop()`
- `break` vs `continue`
- List vs Tuple
- List methods vs String methods

### 📊 Progress Tracking

CodeLoop tracks learning and coding activity.

- Track topic completion
- Track coding problem attempts
- Track solved problems

---

## 🛠️ Technology Stack

| Technology | Purpose |
|------------|---------|
| Python | Application development |
| Flask | Web framework |
| SQLite | Local database |
| HTML5 | Page structure |
| CSS3 | Styling |
| JavaScript | Client-side functionality |
| Jinja2 | Template rendering |

---

## 📁 Project Structure

```text
CodeLoop/
│
├── app.py
│
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── paths.html
│   ├── topics.html
│   ├── topic_detail.html
│   ├── practice.html
│   ├── practice_problem.html
│   ├── confusing_parts.html
│   ├── confusing_part_detail.html
│   ├── mistakes.html
│   └── progress.html
│
└── static/
    └── style.css
```

---

## 🚀 Running the Application

### 1. Install Flask

```bash
pip install flask
```

### 2. Run the Application

```bash
python app.py
```

### 3. Open in Browser

Open the following address in your browser:

```text
http://127.0.0.1:5000
```

The application runs locally on your computer.

---

## 🎯 Purpose

CodeLoop is designed to make Python learning more active and reflective rather than relying only on reading tutorials.

The application focuses on helping beginners understand not only what code to write, but also the mistakes they make while learning.

---

## 🔮 Future Improvements

- More Python topics
- More coding problems
- Additional debugging exercises
- More confusing-concept references
- Enhanced progress tracking
- User accounts
- Personalized learning paths

---

## 📄 License

This project was created for learning and educational purposes.
---

