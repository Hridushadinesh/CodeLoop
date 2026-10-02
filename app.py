import sqlite3
import subprocess
import sys
import tempfile
from pathlib import Path

from flask import Flask, jsonify, redirect, render_template, request, url_for

app = Flask(__name__, static_folder="templates/static", static_url_path="/static")
DATABASE = Path(__file__).with_name("learning_tracker.db")


def get_db():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


# ---------------------------------------------------------
# Beginner-friendly Python curriculum
# ---------------------------------------------------------

PYTHON_TOPICS = [
    (
        "Python Basics",
        "Variables",
        "A variable is a name that we give to a value so we can use that value later. "
        "Think of it like a label attached to a value. For example, name = 'Anu' stores "
        "the text 'Anu' under the name name. The variable name goes on the left of =, "
        "and the value goes on the right. Variables are useful because you can store "
        "information once and use it many times.",
        "name = 'Anu'\nage = 21\n\nprint(name)\nprint(age)",
        "Create a variable called city, store a city name in it, and print the variable.",
    ),
    (
        "Python Basics",
        "Data Types",
        "A data type tells Python what kind of value something is. For example, 10 is an "
        "integer, 3.5 is a float, 'hello' is a string, and True is a boolean. Different "
        "types are used for different kinds of information. You can check a value's type "
        "with type().",
        "age = 21\nprice = 99.5\nname = 'Anu'\nready = True\n\nprint(type(age).__name__)",
        "Create one integer, one string, and one boolean, then print their types.",
    ),
    (
        "Python Basics",
        "Input and Output",
        "Input means getting information from the user. In Python, input() waits for the "
        "user to type something and gives that text to your program. Output means showing "
        "something on the screen, which we usually do with print(). A simple program can "
        "take input, store it in a variable, and then print a result.",
        "name = input('What is your name? ')\nprint(name)",
        "Ask the user for their name and print a greeting using that name.",
    ),
    (
        "Control Flow",
        "Conditions",
        "A condition lets your program make a decision. Python checks whether something is "
        "True or False and then chooses what to do. Use if when you want to check a "
        "condition. Use else when you want something different to happen when the condition "
        "is False. Use elif when there are more choices to check.",
        "age = 20\n\nif age >= 18:\n    print('Adult')\nelse:\n    print('Under 18')",
        "Write a condition that prints 'positive' when a number is greater than zero.",
    ),
    (
        "Control Flow",
        "Loops",
        "A loop is a way to repeat code. This is useful when you need to do the same kind "
        "of work many times. A for loop goes through items one by one. A while loop keeps "
        "running while a condition is True. Instead of writing the same line many times, "
        "a loop lets Python repeat it for you.",
        "for number in [1, 2, 3]:\n    print(number)",
        "Print the numbers 1, 2, and 3, one per line, using a loop.",
    ),
    (
        "Data Structures",
        "Lists",
        "A list stores several values together in one place. Lists keep their order and can "
        "be changed after they are created. Each item has a position called an index, and "
        "indexing starts at 0. You can add items with append(), remove items, and access "
        "an item by its index.",
        "foods = ['rice', 'pizza', 'apple']\n\nprint(foods[0])\nfoods.append('bread')",
        "Create a list of three foods and print the second item.",
    ),
    (
        "Data Structures",
        "Dictionaries",
        "A dictionary stores information as key-value pairs. Think of a key as a label and "
        "the value as the information stored under that label. For example, a student "
        "dictionary can have a key called 'name' and a value such as 'Anu'. You access a "
        "dictionary value by using its key.",
        "student = {'name': 'Anu', 'age': 21}\n\nprint(student['name'])",
        "Create a dictionary for a book with a title and an author, then print the title.",
    ),
    (
        "Data Structures",
        "Sets and Tuples",
        "A tuple is a collection that keeps its order but cannot normally be changed after "
        "it is created. A set is a collection that keeps only unique values. Use a tuple "
        "when you have a group of values that should stay fixed. Use a set when duplicate "
        "values are not wanted.",
        "point = (3, 4)\nunique_numbers = {1, 1, 2, 3}\n\nprint(point)\nprint(unique_numbers)",
        "Create a set containing 1, 1, 2, and 3, then print the number of unique values.",
    ),
    (
        "Functions",
        "Defining Functions",
        "A function is a named block of code that you can use whenever you need it. "
        "Functions help you avoid writing the same code again and again. You create a "
        "function with def, give it a name, and put the instructions inside it. A function "
        "can also receive information through parameters.",
        "def greet(name):\n    print('Hello', name)\n\n\ngreet('Anu')",
        "Write a function called greet(name) that prints a greeting for the given name.",
    ),
    (
        "Functions",
        "Return Values",
        "A function can give a result back to the code that called it. We do this with "
        "return. For example, an add function can receive two numbers, calculate their "
        "sum, and return that sum. The returned value can then be stored, printed, or used "
        "in another calculation.",
        "def add(a, b):\n    return a + b\n\nresult = add(2, 3)\nprint(result)",
        "Write a function that accepts length and width and returns the area of a rectangle.",
    ),
    (
        "OOP",
        "Classes and Objects",
        "A class is a blueprint for creating objects. It describes what an object can have "
        "and what it can do. An object is an actual thing created from that class. For "
        "example, Dog can be a class, while my_dog can be an object created from Dog. "
        "Classes are useful when we want to group related data and behavior together.",
        "class Dog:\n    pass\n\npet = Dog()\nprint(type(pet).__name__)",
        "Create a Dog class, create an object from it, and print the object's type name.",
    ),
    (
        "OOP",
        "Methods and Attributes",
        "An attribute is data that belongs to an object. A method is a function that belongs "
        "to a class and describes something an object can do. For example, a Dog object can "
        "have a name attribute and a bark() method. Inside a method, self refers to the "
        "current object.",
        "class Dog:\n    def bark(self):\n        return 'Woof'\n\npet = Dog()\nprint(pet.bark())",
        "Create a Dog class with a bark method that returns 'Woof', then print the result.",
    ),
]


# The editor starts empty. The expected answer stays on the server.
PRACTICE_TASKS = {
    "Variables": {
        "prompt": "Create a variable called city and print its value.",
        "starter": "",
        "expected": "Kozhikode",
        "accept_any_nonempty": True,
    },
    "Data Types": {
        "prompt": "Create an integer, a string, and a boolean, then print their types.",
        "starter": "",
        "expected": "int\nstr\nbool",
        "accept_any_nonempty": False,
    },
    "Input and Output": {
        "prompt": "Ask the user for their name and print a greeting using that name.",
        "starter": "",
        "expected": "",
        "accept_any_nonempty": True,
    },
    "Conditions": {
        "prompt": "Print 'positive' when number is greater than zero.",
        "starter": "",
        "expected": "positive",
        "accept_any_nonempty": False,
    },
    "Loops": {
        "prompt": "Print the numbers 1, 2, and 3, one per line, using a loop.",
        "starter": "",
        "expected": "1\n2\n3",
        "accept_any_nonempty": False,
    },
    "Lists": {
        "prompt": "Create a list of three foods and print the second item.",
        "starter": "",
        "expected": "",
        "accept_any_nonempty": True,
    },
    "Dictionaries": {
        "prompt": "Create a dictionary for a book with a title and an author, then print the title.",
        "starter": "",
        "expected": "",
        "accept_any_nonempty": True,
    },
    "Sets and Tuples": {
        "prompt": "Create a set containing 1, 1, 2, and 3, then print the number of unique values.",
        "starter": "",
        "expected": "3",
        "accept_any_nonempty": False,
    },
    "Defining Functions": {
        "prompt": "Write a function called greet(name) that prints a greeting for the given name.",
        "starter": "",
        "expected": "",
        "accept_any_nonempty": True,
    },
    "Return Values": {
        "prompt": "Write a function that accepts length and width and returns the area of a rectangle.",
        "starter": "",
        "expected": "",
        "accept_any_nonempty": True,
    },
    "Classes and Objects": {
        "prompt": "Create a Dog class, create an object from it, and print the object's type name.",
        "starter": "",
        "expected": "Dog",
        "accept_any_nonempty": False,
    },
    "Methods and Attributes": {
        "prompt": "Create a Dog class with a bark method that returns 'Woof', then print the result.",
        "starter": "",
        "expected": "Woof",
        "accept_any_nonempty": False,
    },
}
PRACTICE_SOLUTIONS = {
    "Variables": {
        "code": 'city = "Kozhikode"\nprint(city)',
        "explanation": "The variable city stores a city name, and print(city) displays the value stored in it.",
    },

    "Data Types": {
        "code": 'number = 7\nword = "hello"\nready = True\n\nprint(type(number).__name__)\nprint(type(word).__name__)\nprint(type(ready).__name__)',
        "explanation": "number is an integer, word is a string, and ready is a boolean. type() checks each value's type.",
    },

    "Input and Output": {
        "code": 'name = input("Enter your name: ")\nprint("Hello", name)',
        "explanation": "input() gets the user's name and stores it in name. print() then uses that value to display a greeting.",
    },

    "Conditions": {
        "code": 'number = 8\n\nif number > 0:\n    print("positive")',
        "explanation": "The if condition checks whether number is greater than zero. If it is, Python prints positive.",
    },

    "Loops": {
        "code": 'for number in range(1, 4):\n    print(number)',
        "explanation": "range(1, 4) produces 1, 2, and 3, and the for loop prints each number.",
    },

    "Lists": {
        "code": "foods = ['rice', 'pizza', 'apple']\nprint(foods[1])",
        "explanation": "List indexing starts at 0, so index 1 refers to the second item.",
    },

    "Dictionaries": {
        "code": 'book = {"title": "Python Basics", "author": "Anu"}\nprint(book["title"])',
        "explanation": 'The key "title" is used to access the title value from the dictionary.',
    },

    "Sets and Tuples": {
        "code": "numbers = {1, 1, 2, 3}\nprint(len(numbers))",
        "explanation": "A set keeps only unique values, so {1, 1, 2, 3} contains three values.",
    },

    "Defining Functions": {
        "code": 'def greet(name):\n    print("Hello", name)\n\ngreet("Anu")',
        "explanation": "The function is defined with def, receives name as a parameter, and is then called with Anu.",
    },

    "Return Values": {
        "code": "def area(length, width):\n    return length * width\n\nresult = area(5, 3)\nprint(result)",
        "explanation": "The function multiplies length by width and returns the area. The returned value is stored in result.",
    },

    "Classes and Objects": {
        "code": 'class Dog:\n    pass\n\npet = Dog()\nprint(type(pet).__name__)',
        "explanation": "Dog is the class and pet is an object created from that class. The object's type name is Dog.",
    },

    "Methods and Attributes": {
        "code": 'class Dog:\n    def bark(self):\n        return "Woof"\n\npet = Dog()\nprint(pet.bark())',
        "explanation": "bark() is a method of Dog. Calling pet.bark() runs the method and returns Woof.",
    },
}

# ---------------------------------------------------------
# Database
# ---------------------------------------------------------

def init_db():
    with get_db() as connection:
        connection.executescript(
            """
            CREATE TABLE IF NOT EXISTS learning_paths (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS topics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                path_id INTEGER NOT NULL,
                name TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'not_started'
                    CHECK (status IN ('not_started', 'learning', 'completed')),
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (path_id) REFERENCES learning_paths (id) ON DELETE CASCADE,
                UNIQUE (path_id, name)
            );

            CREATE TABLE IF NOT EXISTS mistakes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                topic_id INTEGER NOT NULL,
                mistake TEXT NOT NULL,
                thought TEXT NOT NULL,
                correction TEXT NOT NULL,
                why TEXT NOT NULL,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (topic_id) REFERENCES topics (id) ON DELETE CASCADE
            );

            CREATE TABLE IF NOT EXISTS practice_attempts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                topic_id INTEGER NOT NULL,
                passed INTEGER NOT NULL DEFAULT 0,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (topic_id) REFERENCES topics (id) ON DELETE CASCADE
            );
            CREATE TABLE IF NOT EXISTS coding_problem_progress (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                slug TEXT NOT NULL UNIQUE,
                status TEXT NOT NULL DEFAULT 'not_attempted'
                    CHECK (status IN ('not_attempted', 'attempted', 'solved')),
                attempts INTEGER NOT NULL DEFAULT 0,
                updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            );
            """
        )

        # Create a progress row for every Coding Problem Bank problem.
        # This keeps problem progress persistent in SQLite and means the
        # Practice page does not need to create missing rows on every visit.
        for slug in PRACTICE_PROBLEMS:
            connection.execute(
                """
                INSERT OR IGNORE INTO coding_problem_progress
                (slug, status, attempts)
                VALUES (?, 'not_attempted', 0)
                """,
                (slug,),
            )

        columns = {
            row["name"]
            for row in connection.execute("PRAGMA table_info(topics)")
        }

        for name, definition in {
            "section": "TEXT NOT NULL DEFAULT 'Python Basics'",
            "explanation": "TEXT NOT NULL DEFAULT ''",
            "example": "TEXT NOT NULL DEFAULT ''",
            "practice": "TEXT NOT NULL DEFAULT ''",
            "sort_order": "INTEGER NOT NULL DEFAULT 0",
        }.items():
            if name not in columns:
                connection.execute(
                    f"ALTER TABLE topics ADD COLUMN {name} {definition}"
                )

        path = connection.execute(
            "SELECT id FROM learning_paths WHERE name = 'Python'"
        ).fetchone()

        if path is None:
            cursor = connection.execute(
                "INSERT INTO learning_paths (name) VALUES ('Python')"
            )
            path_id = cursor.lastrowid
        else:
            path_id = path["id"]

        # Repair the early version's section/name layout if it was used.
        connection.execute(
            """
            UPDATE topics
            SET name = section, section = name
            WHERE path_id = ? AND name IN
            ('Python Basics', 'Control Flow', 'Data Structures', 'Functions', 'OOP')
            """,
            (path_id,),
        )

        for order, topic in enumerate(PYTHON_TOPICS, start=1):
            connection.execute(
                """
                INSERT OR IGNORE INTO topics
                (path_id, name, section, explanation, example, practice, sort_order)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    path_id,
                    topic[1],
                    topic[0],
                    topic[2],
                    topic[3],
                    topic[4],
                    order,
                ),
            )

            # Update the built-in Python topics every time the app starts,
            # so edited explanations appear immediately.
            connection.execute(
                """
                UPDATE topics
                SET section = ?, explanation = ?, example = ?, practice = ?, sort_order = ?
                WHERE path_id = ? AND name = ?
                """,
                (
                    topic[0],
                    topic[2],
                    topic[3],
                    topic[4],
                    order,
                    path_id,
                    topic[1],
                ),
            )


# ---------------------------------------------------------
# Dashboard
# ---------------------------------------------------------

def get_dashboard_data():
    with get_db() as connection:
        paths = connection.execute(
            """
            SELECT learning_paths.id, learning_paths.name,
                   COUNT(topics.id) AS topic_count,
                   COALESCE(SUM(topics.status = 'completed'), 0) AS completed_count,
                   COALESCE(SUM(topics.status = 'learning'), 0) AS learning_count
            FROM learning_paths
            LEFT JOIN topics ON topics.path_id = learning_paths.id
            GROUP BY learning_paths.id
            ORDER BY learning_paths.created_at
            """
        ).fetchall()

        totals = connection.execute(
            """
            SELECT COUNT(*) AS topic_count,
                   COALESCE(SUM(status = 'completed'), 0) AS completed_count,
                   COALESCE(SUM(status = 'learning'), 0) AS learning_count
            FROM topics
            """
        ).fetchone()

    total_topics = totals["topic_count"]
    completed_topics = totals["completed_count"]
    overall_progress = (
        round(completed_topics / total_topics * 100)
        if total_topics
        else 0
    )

    return paths, totals, overall_progress


@app.route("/")
def home():
    paths, totals, overall_progress = get_dashboard_data()

    return render_template(
        "index.html",
        paths=paths,
        totals=totals,
        overall_progress=overall_progress,
    )


@app.route("/paths")
def paths():
    with get_db() as connection:
        learning_paths = connection.execute(
            """
            SELECT learning_paths.id, learning_paths.name,
                   COUNT(topics.id) AS topic_count,
                   COALESCE(SUM(topics.status = 'completed'), 0) AS completed_count
            FROM learning_paths
            LEFT JOIN topics ON topics.path_id = learning_paths.id
            GROUP BY learning_paths.id
            ORDER BY learning_paths.created_at
            """
        ).fetchall()

    return render_template("paths.html", paths=learning_paths)


# Kept because the existing UI/database supports paths,
# but the current project remains focused on the built-in Python path.
@app.post("/paths/add")
def add_path():
    name = request.form.get("name", "").strip()

    if not name:
        return "Learning path name is required.", 400

    try:
        with get_db() as connection:
            connection.execute(
                "INSERT INTO learning_paths (name) VALUES (?)",
                (name,),
            )
    except sqlite3.IntegrityError:
        return "A learning path with that name already exists.", 400

    return redirect(url_for("paths"))


@app.route("/paths/<int:path_id>/topics")
def topics(path_id):
    with get_db() as connection:
        learning_path = connection.execute(
            "SELECT id, name FROM learning_paths WHERE id = ?",
            (path_id,),
        ).fetchone()

        if learning_path is None:
            return "Learning path not found", 404

        path_topics = connection.execute(
            """
            SELECT id, name, section, status
            FROM topics
            WHERE path_id = ?
            ORDER BY sort_order, id
            """,
            (path_id,),
        ).fetchall()

    completed = sum(topic["status"] == "completed" for topic in path_topics)
    progress = (
        round(completed / len(path_topics) * 100)
        if path_topics
        else 0
    )

    return render_template(
        "topics.html",
        path=learning_path,
        topics=path_topics,
        progress=progress,
    )


# Kept for compatibility with the existing project.
@app.post("/paths/<int:path_id>/topics/add")
def add_topic(path_id):
    name = request.form.get("name", "").strip()
    section = request.form.get("section", "").strip() or "General"
    explanation = request.form.get("explanation", "").strip()
    example = request.form.get("example", "").strip()
    practice = request.form.get("practice", "").strip()

    if not name:
        return "Topic name is required.", 400

    with get_db() as connection:
        path = connection.execute(
            "SELECT id FROM learning_paths WHERE id = ?",
            (path_id,),
        ).fetchone()

        if path is None:
            return "Learning path not found.", 404

        next_order = connection.execute(
            """
            SELECT COALESCE(MAX(sort_order), 0) + 1 AS next_order
            FROM topics
            WHERE path_id = ?
            """,
            (path_id,),
        ).fetchone()["next_order"]

        try:
            connection.execute(
                """
                INSERT INTO topics
                (path_id, name, section, explanation, example, practice, sort_order)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    path_id,
                    name,
                    section,
                    explanation,
                    example,
                    practice,
                    next_order,
                ),
            )
        except sqlite3.IntegrityError:
            return "A topic with that name already exists in this learning path.", 400

    return redirect(url_for("topics", path_id=path_id))


# ---------------------------------------------------------
# Topic
# ---------------------------------------------------------

@app.route("/topics/<int:topic_id>")
def topic_detail(topic_id):
    with get_db() as connection:
        topic = connection.execute(
            """
            SELECT topics.*, learning_paths.name AS path_name
            FROM topics
            JOIN learning_paths ON learning_paths.id = topics.path_id
            WHERE topics.id = ?
            """,
            (topic_id,),
        ).fetchone()

    if topic is None:
        return "Topic not found", 404

    practice = PRACTICE_TASKS.get(topic["name"])

    if practice is None and topic["practice"]:
        practice = {
            "prompt": topic["practice"],
            "starter": "",
            "expected": "",
            "accept_any_nonempty": True,
        }

    return render_template(
        "topic_detail.html",
        topic=topic,
        practice=practice,
        reference_tutorials=REFERENCE_TUTORIALS.get(topic["name"], []),
    )


@app.route("/reference/<path:topic_name>")
def reference_tutorials(topic_name):
    tutorials = REFERENCE_TUTORIALS.get(topic_name)
    if tutorials is None:
        return "Reference tutorials not found", 404

    return render_template(
        "reference_tutorials.html",
        topic_name=topic_name,
        tutorials=tutorials,
    )


@app.route("/reference/<path:topic_name>/<int:tutorial_index>")
def reference_tutorial_detail(topic_name, tutorial_index):
    tutorials = REFERENCE_TUTORIALS.get(topic_name)
    if tutorials is None:
        return "Reference tutorials not found", 404

    if tutorial_index < 0 or tutorial_index >= len(tutorials):
        return "Tutorial not found", 404

    return render_template(
        "reference_tutorial_detail.html",
        topic_name=topic_name,
        tutorial=tutorials[tutorial_index],
        tutorial_index=tutorial_index,
        total_tutorials=len(tutorials),
    )



# ---------------------------------------------------------
# Reference Tutorials
# ---------------------------------------------------------

# These are supporting lessons for important sub-concepts that
# should not all be packed into the short beginner explanation.
REFERENCE_TUTORIALS = {
    "Variables": [
        {
            "title": "Creating and naming variables",
            "description": "Learn how to create variables and choose valid, readable names.",
            "content": "A variable gives a name to a value. The name goes on the left of = and the value goes on the right.",
            "example": "name = 'Anu'\nage = 21\nprint(name)\nprint(age)",
        },
        {
            "title": "Reassigning a variable",
            "description": "Learn how a variable can point to a new value.",
            "content": "A variable can be given a new value later. The old value is replaced for that variable.",
            "example": "age = 20\nage = 21\nprint(age)",
        },
        {
            "title": "Multiple assignment",
            "description": "Learn how to assign values to multiple variables in one statement.",
            "content": "Python lets you assign several values at the same time.",
            "example": "name, age = 'Anu', 21\nprint(name)\nprint(age)",
        },
        {
            "title": "Checking a variable's type",
            "description": "Learn how to find what type of value a variable currently holds.",
            "content": "The type() function tells you the data type of a value.",
            "example": "age = 21\nprint(type(age).__name__)",
        },
    ],
    "Data Types": [
        {
            "title": "int, float, str and bool",
            "description": "Learn the four common basic Python data types.",
            "content": "int stores whole numbers, float stores decimal numbers, str stores text, and bool stores True or False.",
            "example": "age = 21\nprice = 99.5\nname = 'Anu'\nready = True",
        },
        {
            "title": "None",
            "description": "Understand what None means in Python.",
            "content": "None represents the absence of a value. It is different from 0, False, and an empty string.",
            "example": "result = None\nprint(result)\nprint(type(result).__name__)",
        },
        {
            "title": "type()",
            "description": "Learn how to check the type of a value.",
            "content": "Use type(value) when you want Python to tell you what type of value you have.",
            "example": "value = 'hello'\nprint(type(value).__name__)",
        },
        {
            "title": "Type conversion",
            "description": "Learn how to convert a value from one basic type to another.",
            "content": "Functions such as int(), float(), and str() can convert compatible values.",
            "example": "age_text = '21'\nage = int(age_text)\nprint(age + 1)",
        },
    ],
    "Input and Output": [
        {
            "title": "input()",
            "description": "Learn how Python receives text typed by the user.",
            "content": "input() pauses the program and returns what the user typed as a string.",
            "example": "name = input('Name: ')\nprint(name)",
        },
        {
            "title": "print()",
            "description": "Learn how to display values and messages.",
            "content": "print() sends values to the screen. You can print text, variables, and multiple values.",
            "example": "name = 'Anu'\nprint('Hello', name)",
        },
        {
            "title": "Input is a string",
            "description": "Understand why numbers typed with input() need conversion.",
            "content": "Even when the user types a number, input() returns text.",
            "example": "age = input('Age: ')\nprint(type(age).__name__)",
        },
        {
            "title": "Converting input",
            "description": "Learn how to turn numeric input into int or float values.",
            "content": "Wrap input() with int() or float() when you need to perform numeric calculations.",
            "example": "age = int(input('Age: '))\nprint(age + 1)",
        },
        {
            "title": "sep and end",
            "description": "Learn two useful print() options.",
            "content": "sep controls the separator between printed values. end controls what is printed after them.",
            "example": "print('A', 'B', 'C', sep='-')\nprint('Hello', end=' ')\nprint('World')",
        },
    ],
    "Conditions": [
        {
            "title": "if",
            "description": "Learn how to run code only when a condition is true.",
            "content": "An if block runs when its condition evaluates to True.",
            "example": "age = 20\nif age >= 18:\n    print('Adult')",
        },
        {
            "title": "elif and else",
            "description": "Learn how to handle additional choices.",
            "content": "elif checks another condition when earlier conditions were false. else handles the remaining case.",
            "example": "mark = 75\nif mark >= 90:\n    print('A')\nelif mark >= 50:\n    print('Pass')\nelse:\n    print('Fail')",
        },
        {
            "title": "Comparison operators",
            "description": "Learn operators such as ==, !=, >, <, >= and <=.",
            "content": "Comparison operators compare values and produce True or False.",
            "example": "age = 20\nprint(age >= 18)\nprint(age == 20)",
        },
        {
            "title": "Logical operators",
            "description": "Learn and, or and not for combining conditions.",
            "content": "and requires both conditions, or requires at least one, and not reverses a boolean result.",
            "example": "age = 20\nprint(age >= 18 and age < 60)",
        },
        {
            "title": "Nested conditions",
            "description": "Learn how one condition can be placed inside another.",
            "content": "A nested condition is an if statement inside another if, used when a second decision depends on the first.",
            "example": "age = 20\nif age >= 18:\n    if age < 60:\n        print('Adult')",
        },
    ],
    "Loops": [
        {
            "title": "for loop",
            "description": "Learn how to repeat code for each item in a sequence.",
            "content": "A for loop takes items one at a time and runs the indented block for each item.",
            "example": "for number in [1, 2, 3]:\n    print(number)",
        },
        {
            "title": "while loop",
            "description": "Learn how to repeat code while a condition remains true.",
            "content": "A while loop continues as long as its condition is True.",
            "example": "count = 1\nwhile count <= 3:\n    print(count)\n    count += 1",
        },
        {
            "title": "range()",
            "description": "Learn how range() is commonly used with for loops.",
            "content": "range() produces a sequence of numbers that is often used to control how many times a loop runs.",
            "example": "for number in range(1, 4):\n    print(number)",
        },
        {
            "title": "break",
            "description": "Learn how to stop a loop completely.",
            "content": "break immediately leaves the current loop.",
            "example": "for number in range(5):\n    if number == 2:\n        break\n    print(number)",
        },
        {
            "title": "continue",
            "description": "Learn how to skip the current loop iteration.",
            "content": "continue skips the remaining code in the current iteration and moves to the next iteration.",
            "example": "for number in range(5):\n    if number == 2:\n        continue\n    print(number)",
        },
        {
            "title": "pass",
            "description": "Learn when pass is used as an empty placeholder.",
            "content": "pass does nothing. It is useful when Python requires a statement but you are not ready to add the real code yet.",
            "example": "for number in range(3):\n    pass",
        },
        {
            "title": "Nested loops",
            "description": "Learn how to place one loop inside another.",
            "content": "The inner loop runs completely for each iteration of the outer loop.",
            "example": "for row in range(2):\n    for column in range(2):\n        print(row, column)",
        },
    ],
    "Lists": [
        {
            "title": "Creating a list",
            "description": "Learn how to store multiple values in a list.",
            "content": "Lists use square brackets and can contain multiple values.",
            "example": "foods = ['rice', 'pizza', 'apple']\nprint(foods)",
        },
        {
            "title": "Indexing and negative indexing",
            "description": "Learn how to access list items by position.",
            "content": "List indexing starts at 0. Negative indexes count from the end, with -1 meaning the last item.",
            "example": "foods = ['rice', 'pizza', 'apple']\nprint(foods[0])\nprint(foods[-1])",
        },
        {
            "title": "Slicing a list",
            "description": "Learn how to take a portion of a list.",
            "content": "A slice such as list[1:3] selects items from index 1 up to, but not including, index 3.",
            "example": "numbers = [10, 20, 30, 40]\nprint(numbers[1:3])",
        },
        {
            "title": "append()",
            "description": "Learn how to add one item to the end of a list.",
            "content": "append() adds its argument as one item.",
            "example": "numbers = [1, 2]\nnumbers.append(3)\nprint(numbers)",
        },
        {
            "title": "insert()",
            "description": "Learn how to add an item at a particular index.",
            "content": "insert(index, value) places a value at the requested position.",
            "example": "numbers = [1, 3]\nnumbers.insert(1, 2)\nprint(numbers)",
        },
        {
            "title": "extend()",
            "description": "Learn how to add items from another iterable.",
            "content": "extend() adds each item from another iterable to the list.",
            "example": "numbers = [1, 2]\nnumbers.extend([3, 4])\nprint(numbers)",
        },
        {
            "title": "remove() and pop()",
            "description": "Learn the difference between removing by value and removing by index.",
            "content": "remove(value) removes a matching value. pop(index) removes and returns the item at an index.",
            "example": "numbers = [10, 20, 30]\nnumbers.remove(20)\nremoved = numbers.pop(0)\nprint(removed)\nprint(numbers)",
        },
        {
            "title": "sort() and reverse()",
            "description": "Learn how to change the order of list items.",
            "content": "sort() arranges items according to their ordering. reverse() reverses the current order.",
            "example": "numbers = [3, 1, 2]\nnumbers.sort()\nprint(numbers)\nnumbers.reverse()\nprint(numbers)",
        },
        {
            "title": "count() and index()",
            "description": "Learn how to count a value and find its first position.",
            "content": "count(value) tells how many times a value occurs. index(value) gives its first index.",
            "example": "numbers = [1, 2, 2, 3]\nprint(numbers.count(2))\nprint(numbers.index(2))",
        },
    ],
    "Dictionaries": [
        {
            "title": "Dictionary basics",
            "description": "Understand the structure of a dictionary.",
            "content": "A dictionary stores data as key-value pairs. Keys identify the values stored under them.",
            "example": "student = {'name': 'Anu', 'age': 21}\nprint(student)",
        },
        {
            "title": "Keys and values",
            "description": "Understand what the key and value represent.",
            "content": "In {'name': 'Anu'}, 'name' is the key and 'Anu' is the value.",
            "example": "student = {'name': 'Anu'}\nprint(student.keys())\nprint(student.values())",
        },
        {
            "title": "Accessing a value using a key",
            "description": "Learn the basic dictionary lookup syntax.",
            "content": "Use dictionary[key] to access the value stored under that key.",
            "example": "student = {'name': 'Anu', 'age': 21}\nprint(student['name'])\nprint(student['age'])",
        },
        {
            "title": "keys(), values() and items()",
            "description": "Learn how to view dictionary keys, values, or both together.",
            "content": "keys() gives the keys, values() gives the values, and items() gives key-value pairs.",
            "example": "student = {'name': 'Anu', 'age': 21}\nprint(student.keys())\nprint(student.values())\nprint(student.items())",
        },
        {
            "title": "get()",
            "description": "Learn a safer way to retrieve a dictionary value.",
            "content": "get(key) returns the value for a key. If the key is missing, it can return a default instead of raising KeyError.",
            "example": "student = {'name': 'Anu'}\nprint(student.get('age', 'Not found'))",
        },
        {
            "title": "Adding and updating items",
            "description": "Learn how to add a new key or change an existing value.",
            "content": "Assigning to dictionary[key] creates the key if it is new, or updates its value if it already exists.",
            "example": "student = {'name': 'Anu'}\nstudent['age'] = 21\nstudent['name'] = 'Maya'\nprint(student)",
        },
        {
            "title": "pop(), popitem(), del and clear()",
            "description": "Learn the common ways to remove dictionary data.",
            "content": "pop() removes a chosen key, popitem() removes the last inserted pair, del removes a chosen item, and clear() empties the dictionary.",
            "example": "student = {'name': 'Anu', 'age': 21}\nage = student.pop('age')\nprint(age)\nprint(student)",
        },
        {
            "title": "in and looping through dictionaries",
            "description": "Learn how to check keys and visit dictionary data with a loop.",
            "content": "The in operator checks keys by default. A for loop can iterate through keys, values, or items.",
            "example": "student = {'name': 'Anu', 'age': 21}\nfor key, value in student.items():\n    print(key, value)",
        },
        {
            "title": "Nested dictionaries",
            "description": "Learn how dictionaries can contain other dictionaries.",
            "content": "A nested dictionary stores another dictionary as a value, allowing related structured information.",
            "example": "students = {\n    's1': {'name': 'Anu', 'age': 21}\n}\nprint(students['s1']['name'])",
        },
    ],
    "Sets and Tuples": [
        {
            "title": "Creating tuples",
            "description": "Learn how to create an ordered, fixed collection.",
            "content": "Tuples normally use parentheses and can contain multiple values.",
            "example": "point = (3, 4)\nprint(point)",
        },
        {
            "title": "Tuple indexing and slicing",
            "description": "Learn how to access tuple items.",
            "content": "Tuples support indexing and slicing just like lists.",
            "example": "numbers = (10, 20, 30, 40)\nprint(numbers[1])\nprint(numbers[1:3])",
        },
        {
            "title": "Tuple unpacking",
            "description": "Learn how to assign tuple values to separate variables.",
            "content": "Unpacking assigns the values inside a tuple to multiple variables.",
            "example": "point = (3, 4)\nx, y = point\nprint(x)\nprint(y)",
        },
        {
            "title": "Creating sets and uniqueness",
            "description": "Learn why duplicate values disappear from a set.",
            "content": "Sets store unique values. Repeated values are kept only once.",
            "example": "numbers = {1, 1, 2, 3}\nprint(numbers)",
        },
        {
            "title": "add(), remove() and discard()",
            "description": "Learn common ways to change a set.",
            "content": "add() inserts a value. remove() removes a value and errors if it is missing. discard() removes it without that error.",
            "example": "numbers = {1, 2}\nnumbers.add(3)\nnumbers.discard(5)\nprint(numbers)",
        },
        {
            "title": "Union, intersection and difference",
            "description": "Learn the basic set operations for comparing collections.",
            "content": "Union combines values, intersection keeps common values, and difference keeps values present in one set but not the other.",
            "example": "a = {1, 2, 3}\nb = {3, 4, 5}\nprint(a | b)\nprint(a & b)\nprint(a - b)",
        },
    ],
    "Defining Functions": [
        {
            "title": "def and calling a function",
            "description": "Learn how to define and then use a function.",
            "content": "def starts a function definition. The function runs when you call its name.",
            "example": "def greet():\n    print('Hello')\n\ngreet()",
        },
        {
            "title": "Parameters and arguments",
            "description": "Understand the difference between the placeholder in a function and the value passed to it.",
            "content": "A parameter is named in the function definition. An argument is the actual value supplied when calling the function.",
            "example": "def greet(name):\n    print('Hello', name)\n\ngreet('Anu')",
        },
        {
            "title": "Default arguments",
            "description": "Learn how a parameter can have a default value.",
            "content": "A default argument is used when the caller does not provide a value for that parameter.",
            "example": "def greet(name='Anu'):\n    print('Hello', name)\n\ngreet()\ngreet('Maya')",
        },
        {
            "title": "Keyword arguments",
            "description": "Learn how to pass an argument by parameter name.",
            "content": "Keyword arguments make the intended parameter explicit in a function call.",
            "example": "def introduce(name, age):\n    print(name, age)\n\nintroduce(age=21, name='Anu')",
        },
        {
            "title": "Local variables",
            "description": "Understand variables created inside a function.",
            "content": "A variable created inside a function is normally local to that function.",
            "example": "def show():\n    message = 'Hello'\n    print(message)\n\nshow()",
        },
    ],
    "Return Values": [
        {
            "title": "return",
            "description": "Learn how a function sends a value back to its caller.",
            "content": "return ends the function and gives a value back to the code that called it.",
            "example": "def add(a, b):\n    return a + b\n\nresult = add(2, 3)\nprint(result)",
        },
        {
            "title": "return vs print()",
            "description": "Understand why displaying a value is different from returning it.",
            "content": "print() displays a value. return sends a value back so the caller can store or use it.",
            "example": "def add(a, b):\n    return a + b\n\nresult = add(2, 3)\nprint(result)",
        },
        {
            "title": "Storing a returned value",
            "description": "Learn how to save a function's result in a variable.",
            "content": "The value returned by a function call can be assigned to a variable.",
            "example": "def square(n):\n    return n * n\n\nanswer = square(4)\nprint(answer)",
        },
        {
            "title": "Returning multiple values",
            "description": "Learn how a function can return more than one value.",
            "content": "Python can return multiple values together, which can then be unpacked into separate variables.",
            "example": "def get_point():\n    return 3, 4\n\nx, y = get_point()\nprint(x, y)",
        },
        {
            "title": "Early return",
            "description": "Learn how return can end a function before reaching its last line.",
            "content": "When Python reaches return, the function ends immediately.",
            "example": "def check(age):\n    if age < 18:\n        return 'Minor'\n    return 'Adult'\n\nprint(check(16))",
        },
    ],
    "Classes and Objects": [
        {
            "title": "What is a class?",
            "description": "Understand a class as a blueprint for objects.",
            "content": "A class describes the data and behavior that objects created from it can have.",
            "example": "class Dog:\n    pass",
        },
        {
            "title": "What is an object?",
            "description": "Learn how to create an actual object from a class.",
            "content": "An object is an instance created from a class.",
            "example": "class Dog:\n    pass\n\npet = Dog()\nprint(type(pet).__name__)",
        },
        {
            "title": "__init__()",
            "description": "Learn how __init__() is used when an object is created.",
            "content": "__init__() is commonly used to set up an object's initial data.",
            "example": "class Dog:\n    def __init__(self, name):\n        self.name = name\n\npet = Dog('Bruno')\nprint(pet.name)",
        },
        {
            "title": "self",
            "description": "Understand what self refers to inside an instance method.",
            "content": "self refers to the current object. It lets a method access that object's attributes and other methods.",
            "example": "class Dog:\n    def __init__(self, name):\n        self.name = name",
        },
        {
            "title": "Instance attributes",
            "description": "Learn how objects can store their own data.",
            "content": "An instance attribute belongs to a particular object and is commonly created with self.attribute.",
            "example": "class Dog:\n    def __init__(self, name):\n        self.name = name\n\npet = Dog('Bruno')\nprint(pet.name)",
        },
    ],
    "Methods and Attributes": [
        {
            "title": "Instance methods",
            "description": "Learn how functions inside a class become methods of its objects.",
            "content": "An instance method usually has self as its first parameter and works with a particular object.",
            "example": "class Dog:\n    def bark(self):\n        return 'Woof'\n\npet = Dog()\nprint(pet.bark())",
        },
        {
            "title": "Calling methods",
            "description": "Learn the object.method() syntax.",
            "content": "Call an object's method by writing the object name, a dot, the method name, and parentheses.",
            "example": "pet.bark()",
        },
        {
            "title": "Method parameters",
            "description": "Learn how methods can receive additional information.",
            "content": "Besides self, a method can accept parameters just like a normal function.",
            "example": "class Dog:\n    def greet(self, person):\n        return 'Hello ' + person\n\npet = Dog()\nprint(pet.greet('Anu'))",
        },
        {
            "title": "self in methods",
            "description": "Understand why self is used to access the current object's data.",
            "content": "self.name means the name attribute belonging to the current object.",
            "example": "class Dog:\n    def __init__(self, name):\n        self.name = name\n\n    def bark(self):\n        return self.name + ' says Woof'",
        },
        {
            "title": "Object attributes",
            "description": "Learn how to access data stored on an object.",
            "content": "Use object.attribute to read an attribute belonging to that object.",
            "example": "class Dog:\n    def __init__(self, name):\n        self.name = name\n\npet = Dog('Bruno')\nprint(pet.name)",
        },
        {
            "title": "Methods vs functions",
            "description": "Understand the difference between a normal function and a function defined inside a class.",
            "content": "A function can be called independently. A method is associated with a class or object and is normally called through it.",
            "example": "def greet():\n    print('Hello')\n\ngreet()\n\nclass Dog:\n    def bark(self):\n        print('Woof')\n\nDog().bark()",
        },
    ],
}


# ---------------------------------------------------------
# Confusing Parts
# ---------------------------------------------------------

CONFUSING_PARTS = [
    {
        "title": "= vs ==",
        "subtitle": "Assignment vs comparison",
        "description": "Understand the difference between storing a value and checking whether two values are equal.",
    },
    {
        "title": "append() vs extend()",
        "subtitle": "Adding items to a list",
        "description": "Learn why append() adds one item while extend() adds items from another iterable.",
    },
    {
        "title": "remove() vs pop()",
        "subtitle": "Removing from a list",
        "description": "Understand the difference between removing an item by value and removing it by position.",
    },
    {
        "title": "break vs continue",
        "subtitle": "Controlling loops",
        "description": "Learn when Python should stop a loop completely and when it should only skip the current iteration.",
    },
    {
        "title": "list vs tuple",
        "subtitle": "Changeable vs fixed collections",
        "description": "Understand when a list or tuple is the appropriate choice.",
    },
    {
        "title": "List methods vs String methods",
        "subtitle": "Which method belongs to which type?",
        "description": "Understand why methods like append(), remove(), and sort() belong to lists, while upper(), lower(), strip(), and split() belong to strings.",
    },
]


CONFUSING_PART_DETAILS = {
    "= vs ==": {
        "title": "= vs ==",
        "intro": "These symbols look similar, but Python uses them for two different jobs.",
        "sections": [
            {
                "heading": "=",
                "label": "Assignment",
                "text": "The single equals sign stores a value in a variable.",
                "code": "age = 20",
                "explanation": "Python stores the value 20 in the variable age.",
            },
            {
                "heading": "==",
                "label": "Comparison",
                "text": "The double equals sign checks whether two values are equal.",
                "code": "age == 20",
                "explanation": "Python checks whether the value stored in age is equal to 20.",
            },
        ],
        "try_code": "age = 20\nprint(age == 20)",
        "question": "What do you think Python will print?",
        "answer": "True",
        "why": "age = 20 stores the value 20. Then age == 20 checks whether age contains 20. Since they are equal, Python produces True.",
        "remember": "= stores a value. == checks whether values are equal.",
    },

    "append() vs extend()": {
        "title": "append() vs extend()",
        "intro": "Both methods add things to a list, but they do not add them in the same way.",
        "sections": [
            {
                "heading": "append()",
                "label": "Add one item",
                "text": "append() adds one item to the end of a list.",
                "code": "numbers = [1, 2]\nnumbers.append(3)",
                "explanation": "The list becomes [1, 2, 3]. One item was added.",
            },
            {
                "heading": "extend()",
                "label": "Add multiple items",
                "text": "extend() adds items from another iterable to the list.",
                "code": "numbers = [1, 2]\nnumbers.extend([3, 4])",
                "explanation": "The list becomes [1, 2, 3, 4]. Multiple items were added.",
            },
        ],
        "try_code": "numbers = [1, 2]\nnumbers.append([3, 4])\nprint(numbers)",
        "question": "What do you think Python will print?",
        "answer": "[1, 2, [3, 4]]",
        "why": "append() treats [3, 4] as one item, so the entire list is added as a single element.",
        "remember": "append() adds one item. extend() adds items from another iterable.",
    },

    "remove() vs pop()": {
        "title": "remove() vs pop()",
        "intro": "Both can remove something from a list, but they use different information to decide what to remove.",
        "sections": [
            {
                "heading": "remove()",
                "label": "Remove by value",
                "text": "remove() looks for a particular value and removes it.",
                "code": "numbers = [10, 20, 30]\nnumbers.remove(20)",
                "explanation": "The value 20 is removed from the list.",
            },
            {
                "heading": "pop()",
                "label": "Remove by position",
                "text": "pop() removes an item using its index.",
                "code": "numbers = [10, 20, 30]\nnumbers.pop(1)",
                "explanation": "The item at index 1, which is 20, is removed.",
            },
        ],
        "try_code": "numbers = [10, 20, 30]\nremoved = numbers.pop(1)\nprint(removed)\nprint(numbers)",
        "question": "What do you think Python will print?",
        "answer": "20\n[10, 30]",
        "why": "Index 1 refers to the second item in the list. pop(1) removes that item and returns its value.",
        "remember": "remove() uses a value. pop() uses an index.",
    },

    "break vs continue": {
        "title": "break vs continue",
        "intro": "Both change how a loop behaves, but one stops the loop while the other skips only the current iteration.",
        "sections": [
            {
                "heading": "break",
                "label": "Stop the loop",
                "text": "break immediately stops the loop.",
                "code": "for number in range(5):\n    if number == 2:\n        break\n    print(number)",
                "explanation": "When number becomes 2, the loop stops completely.",
            },
            {
                "heading": "continue",
                "label": "Skip one iteration",
                "text": "continue skips the current iteration and moves to the next one.",
                "code": "for number in range(5):\n    if number == 2:\n        continue\n    print(number)",
                "explanation": "When number is 2, that iteration is skipped, but the loop continues.",
            },
        ],
        "try_code": "for number in range(5):\n    if number == 2:\n        continue\n    print(number)",
        "question": "What do you think Python will print?",
        "answer": "0\n1\n3\n4",
        "why": "When number is 2, continue skips that iteration. The loop then continues with 3 and 4.",
        "remember": "break stops the loop. continue skips the current iteration.",
    },

    "list vs tuple": {
        "title": "list vs tuple",
        "intro": "Lists and tuples can both store multiple values, but they differ in whether their contents can be changed.",
        "sections": [
            {
                "heading": "List",
                "label": "Changeable",
                "text": "A list can be changed after it is created.",
                "code": "numbers = [1, 2, 3]\nnumbers[0] = 10",
                "explanation": "The first value can be changed, so the list becomes [10, 2, 3].",
            },
            {
                "heading": "Tuple",
                "label": "Fixed",
                "text": "A tuple cannot have its individual values changed after it is created.",
                "code": "numbers = (1, 2, 3)",
                "explanation": "The tuple keeps its values fixed.",
            },
        ],
        "try_code": "numbers = (1, 2, 3)\nnumbers[0] = 10\nprint(numbers)",
        "question": "What do you think Python will do?",
        "answer": "It produces an error.",
        "why": "Tuples are not changeable in the same way as lists. Trying to assign a new value to one of their positions causes an error.",
        "remember": "Lists are changeable. Tuples are fixed.",
    },

    "List methods vs String methods": {
        "title": "List methods vs String methods",
        "intro": "A common beginner confusion is remembering a method but forgetting which type of object it belongs to.",
        "sections": [
            {
                "heading": "List methods",
                "label": "Methods that work with lists",
                "text": "Methods such as append(), remove(), and sort() are commonly used with lists.",
                "code": "numbers = [3, 1, 2]\nnumbers.sort()",
                "explanation": "sort() changes the order of the items in the list.",
            },
            {
                "heading": "String methods",
                "label": "Methods that work with strings",
                "text": "Methods such as upper(), lower(), strip(), and split() are used with strings.",
                "code": 'name = "python"\nprint(name.upper())',
                "explanation": 'upper() works with a string and produces "PYTHON".',
            },
        ],
        "try_code": 'name = "python"\nname.append("!")',
        "question": "What do you think Python will do?",
        "answer": "It produces an error.",
        "why": "name contains a string. append() is a list method, so it is not available for a string.",
        "remember": "Before using a method, ask: what type of object am I working with?",
    },
}


@app.route("/confusing-parts")
def confusing_parts():
    return render_template(
        "confusing_parts.html",
        confusing_parts=CONFUSING_PARTS,
    )


@app.route("/confusing-parts/<path:part>")
def confusing_part_detail(part):
    detail = CONFUSING_PART_DETAILS.get(part)

    if detail is None:
        return "Confusing part not found", 404

    return render_template(
        "confusing_part_detail.html",
        part=part,
        detail=detail,
    )


# ---------------------------------------------------------
# ---------------------------------------------------------
# Coding Problem Bank
# ---------------------------------------------------------

PRACTICE_PROBLEMS = {
    "sum-of-digits": {
        "topic": "Loops",
        "title": "Sum of Digits", "difficulty": "Basic",
        "concepts": "Loops • Arithmetic",
        "prompt": "Given the number 5832, calculate and print the sum of its digits.",
        "expected": "18",
        "solution": 'number = 5832\ntotal = 0\n\nwhile number > 0:\n    total += number % 10\n    number //= 10\n\nprint(total)',
        "solution_explanation": "Use % 10 to take the last digit and // 10 to remove it. Keep adding the digits until the number becomes 0.",
    },
    "reverse-string": {
        "topic": "Loops",
        "title": "Reverse a String", "difficulty": "Basic",
        "concepts": "Strings • Loops",
        "prompt": "Store the word Python in a variable and print it in reverse order.",
        "expected": "nohtyP",
        "solution": 'word = "Python"\nprint(word[::-1])',
        "solution_explanation": "A string slice with [::-1] reads the string from the end to the beginning.",
    },
    "count-vowels": {
        "topic": "Loops",
        "title": "Count Vowels", "difficulty": "Basic",
        "concepts": "Strings • Loops • Conditions",
        "prompt": "Count how many vowels are in the word education and print the count.",
        "expected": "5",
        "solution": 'word = "education"\ncount = 0\n\nfor char in word:\n    if char in "aeiou":\n        count += 1\n\nprint(count)',
        "solution_explanation": "Loop through each character and increase the counter when the character is a vowel.",
    },
    "largest-in-list": {
        "topic": "Lists",
        "title": "Largest Number in a List", "difficulty": "Basic",
        "concepts": "Lists • Loops • Conditions",
        "prompt": "Find and print the largest number in the list [12, 7, 25, 9, 18]. Do not use max().",
        "expected": "25",
        "solution": 'numbers = [12, 7, 25, 9, 18]\nlargest = numbers[0]\n\nfor number in numbers:\n    if number > largest:\n        largest = number\n\nprint(largest)',
        "solution_explanation": "Start with the first item as the largest, then replace it whenever a larger number is found.",
    },
    "remove-duplicates": {
        "topic": "Lists",
        "title": "Remove Duplicates", "difficulty": "Basic",
        "concepts": "Lists • Sets",
        "prompt": "Remove duplicate values from [1, 2, 2, 3, 1, 4] and print the unique values as a sorted list.",
        "expected": "[1, 2, 3, 4]",
        "solution": 'numbers = [1, 2, 2, 3, 1, 4]\nunique_numbers = sorted(set(numbers))\nprint(unique_numbers)',
        "solution_explanation": "A set keeps only unique values. sorted() turns those values back into an ordered list.",
    },
    "character-frequency": {
        "topic": "Dictionaries",
        "title": "Character Frequency", "difficulty": "Intermediate",
        "concepts": "Strings • Dictionaries • Loops",
        "prompt": "Count how many times each character appears in the word banana and print the dictionary.",
        "expected": "{'b': 1, 'a': 3, 'n': 2}",
        "solution": 'word = "banana"\nfrequency = {}\n\nfor char in word:\n    frequency[char] = frequency.get(char, 0) + 1\n\nprint(frequency)',
        "solution_explanation": "Use a dictionary where each character is a key and its count is the value.",
    },
    "student-marks": {
        "topic": "Dictionaries",
        "title": "Student Marks Analyzer", "difficulty": "Intermediate",
        "concepts": "Dictionaries • Lists • Conditions",
        "prompt": "Using marks = {'Math': 80, 'Python': 90, 'English': 70}, calculate and print the average mark.",
        "expected": "80.0",
        "solution": 'marks = {"Math": 80, "Python": 90, "English": 70}\naverage = sum(marks.values()) / len(marks)\nprint(average)',
        "solution_explanation": "values() gives the marks, sum() adds them, and len() gives the number of subjects.",
    },
    "second-largest": {
        "topic": "Lists",
        "title": "Second Largest Number", "difficulty": "Intermediate",
        "concepts": "Lists • Sets • Sorting",
        "prompt": "Find and print the second largest unique number in [10, 4, 8, 10, 15, 6].",
        "expected": "10",
        "solution": 'numbers = [10, 4, 8, 10, 15, 6]\nunique_numbers = sorted(set(numbers))\nprint(unique_numbers[-2])',
        "solution_explanation": "Remove duplicates, sort the remaining values, and take the second value from the end.",
    },
    "contact-book": {
        "topic": "Dictionaries",
        "title": "Simple Contact Book", "difficulty": "Intermediate",
        "concepts": "Dictionaries • Conditions",
        "prompt": "Create a contact dictionary with Anu mapped to 9876543210 and print Anu's phone number.",
        "expected": "9876543210",
        "solution": 'contacts = {"Anu": "9876543210"}\nprint(contacts["Anu"])',
        "solution_explanation": "Store the person's name as the key and the phone number as its value.",
    },
    "shopping-cart": {
        "topic": "Lists",
        "title": "Shopping Cart Total", "difficulty": "Intermediate",
        "concepts": "Lists • Dictionaries • Loops",
        "prompt": "Using prices = [100, 250, 50], calculate and print the total price without using sum().",
        "expected": "400",
        "solution": 'prices = [100, 250, 50]\ntotal = 0\n\nfor price in prices:\n    total += price\n\nprint(total)',
        "solution_explanation": "Start the total at 0 and add each price as you loop through the list.",
    },
}


def get_practice_problem(slug):
    return PRACTICE_PROBLEMS.get(slug)


def check_problem_solution(problem, code, output):
    return bool(code.strip()) and output.strip() == problem["expected"]


# ---------------------------------------------------------
# Practice
# ---------------------------------------------------------

@app.route("/practice")
def practice():
    with get_db() as connection:
        rows = connection.execute(
            """
            SELECT slug, status, attempts
            FROM coding_problem_progress
            WHERE slug IN ({})
            """.format(",".join("?" for _ in PRACTICE_PROBLEMS)),
            tuple(PRACTICE_PROBLEMS.keys()),
        ).fetchall()

    progress = {
        row["slug"]: {
            "status": row["status"],
            "attempts": row["attempts"],
        }
        for row in rows
    }

    solved_count = sum(
        item["status"] == "solved"
        for item in progress.values()
    )

    attempted_count = sum(
        item["status"] in {"attempted", "solved"}
        for item in progress.values()
    )

    not_attempted_count = len(PRACTICE_PROBLEMS) - attempted_count

    return render_template(
        "practice.html",
        problems=PRACTICE_PROBLEMS,
        progress=progress,
        solved_count=solved_count,
        attempted_count=attempted_count,
        not_attempted_count=not_attempted_count,
        total_count=len(PRACTICE_PROBLEMS),
    )


@app.route("/practice/<slug>")
def practice_problem(slug):
    problem = get_practice_problem(slug)
    if problem is None:
        return "Practice problem not found", 404
    return render_template("practice_problem.html", problem=problem, slug=slug)


@app.post("/practice/<slug>/run")
def run_practice_problem(slug):
    problem = get_practice_problem(slug)
    if problem is None:
        return jsonify(error="Practice problem not found"), 404

    code = request.form.get("code", "")
    program_input = request.form.get("program_input", "")
    if not code.strip():
        return jsonify(error="Write some Python code first."), 400

    try:
        with tempfile.TemporaryDirectory() as directory:
            file_path = Path(directory) / "solution.py"
            file_path.write_text(code, encoding="utf-8")
            result = subprocess.run(
                [sys.executable, "-I", str(file_path)],
                input=program_input, capture_output=True, text=True,
                cwd=directory, timeout=3,
            )
    except subprocess.TimeoutExpired:
        return jsonify(error="Your code ran for more than 3 seconds and was stopped."), 400

    output = (result.stdout or result.stderr).strip()
    passed = bool(
        not result.returncode
        and check_problem_solution(problem, code, output)
    )

    # Record progress for the Coding Problem Bank.
    # A failed run counts as an attempt. A successful run marks
    # the problem as solved and keeps the total attempt count.
    with get_db() as connection:
        current = connection.execute(
            """
            SELECT attempts, status
            FROM coding_problem_progress
            WHERE slug = ?
            """,
            (slug,),
        ).fetchone()

        attempts = (current["attempts"] if current else 0) + 1

        if passed:
            status = "solved"
        else:
            # Never move a solved problem backwards to attempted.
            status = (
                "solved"
                if current and current["status"] == "solved"
                else "attempted"
            )

        connection.execute(
            """
            INSERT INTO coding_problem_progress
                (slug, status, attempts, updated_at)
            VALUES (?, ?, ?, CURRENT_TIMESTAMP)
            ON CONFLICT(slug)
            DO UPDATE SET
                status = excluded.status,
                attempts = excluded.attempts,
                updated_at = CURRENT_TIMESTAMP
            """,
            (slug, status, attempts),
        )

    return jsonify(
        output=output or "(no output)",
        passed=passed,
        has_error=bool(result.returncode),
    )


@app.post("/practice/<slug>/analyze")
def analyze_practice_problem(slug):
    problem = get_practice_problem(slug)
    if problem is None:
        return jsonify(error="Practice problem not found"), 404

    code = request.form.get("code", "")
    output = request.form.get("output", "")
    thought = request.form.get("thought", "").strip()
    expected_thought = request.form.get("expected_thought", "").strip()
    if not thought or not expected_thought:
        return jsonify(error="Tell us what you were trying to do and what you expected to happen."), 400

    analysis = explain_debugging_issue(problem["concepts"], code, output, thought, expected_thought)
    return jsonify(
        title=analysis["title"], explanation=analysis["explanation"], why=analysis["why"],
        concept=problem["concepts"], mistake=output, thought=thought,
        correction=analysis["explanation"], solution=problem["solution"],
        solution_explanation=problem["solution_explanation"],
    )


@app.post("/practice/<slug>/mistake")
def save_practice_mistake(slug):
    problem = get_practice_problem(slug)
    if problem is None:
        return jsonify(error="Practice problem not found"), 404

    values = [request.form.get(field, "").strip() for field in ("mistake", "thought", "correction", "why")]
    if not all(values):
        return jsonify(error="Complete the mistake details first."), 400

    concept_name = problem["topic"]
    with get_db() as connection:
        topic = connection.execute("SELECT id FROM topics WHERE name = ? LIMIT 1", (concept_name,)).fetchone()
        if topic is None:
            return jsonify(error="Could not connect this mistake to a topic."), 400
        connection.execute(
            "INSERT INTO mistakes (topic_id, mistake, thought, correction, why) VALUES (?, ?, ?, ?, ?)",
            (topic["id"], *values),
        )
    return jsonify(message="Saved to My Mistakes ✓")


@app.route("/progress")
def progress():
    paths, totals, overall_progress = get_dashboard_data()

    with get_db() as connection:
        weak_topics = connection.execute(
            """
            SELECT topics.id, topics.name, topics.status,
                   learning_paths.name AS path_name
            FROM topics
            JOIN learning_paths ON learning_paths.id = topics.path_id
            WHERE topics.status != 'completed'
            ORDER BY
                CASE topics.status
                    WHEN 'learning' THEN 0
                    WHEN 'not_started' THEN 1
                END,
                topics.sort_order
            LIMIT 8
            """
        ).fetchall()

        practice_totals = connection.execute(
            """
            SELECT
                COUNT(*) AS total,
                COALESCE(SUM(status = 'solved'), 0) AS solved,
                COALESCE(
                    SUM(status IN ('attempted', 'solved')),
                    0
                ) AS attempted
            FROM coding_problem_progress
            WHERE slug IN ({})
            """.format(",".join("?" for _ in PRACTICE_PROBLEMS)),
            tuple(PRACTICE_PROBLEMS.keys()),
        ).fetchone()

    return render_template(
        "progress.html",
        paths=paths,
        totals=totals,
        overall_progress=overall_progress,
        weak_topics=weak_topics,
        practice_totals=practice_totals,
    )


# ---------------------------------------------------------
# Mistake understanding
# ---------------------------------------------------------

def check_practice_solution(topic_name, code, output, practice_task):
    """Check whether the learner actually followed the practice instruction."""

    if not code.strip():
        return False

    # Variables:
    # The task asks for a variable named `city`, containing a city name,
    # and for that variable to be printed.
    if topic_name == "Variables":
        try:
            ast = __import__("ast")
            tree = ast.parse(code)

            has_city_string_assignment = False
            has_city_print = False

            for node in ast.walk(tree):
                if isinstance(node, ast.Assign):
                    for target in node.targets:
                        if (
                            isinstance(target, ast.Name)
                            and target.id == "city"
                            and isinstance(node.value, ast.Constant)
                            and isinstance(node.value.value, str)
                            and node.value.value.strip()
                        ):
                            has_city_string_assignment = True

                if isinstance(node, ast.Call):
                    if (
                        isinstance(node.func, ast.Name)
                        and node.func.id == "print"
                        and node.args
                        and isinstance(node.args[0], ast.Name)
                        and node.args[0].id == "city"
                    ):
                        has_city_print = True

            return has_city_string_assignment and has_city_print

        except SyntaxError:
            return False

    # For tasks with a concrete expected output, compare the actual output.
    expected = practice_task.get("expected", "")
    if expected:
        return output.strip() == expected.strip()

    # Keep the existing behaviour for tasks that do not yet have
    # a specific checker. These can be made task-specific later.
    return bool(practice_task.get("accept_any_nonempty") and output.strip())


def explain_debugging_issue(topic_name, code, output, thought, expected_thought):
    """Return a conceptual explanation without revealing corrected code."""

    text = f"{code}\n{output}".lower()

    if "list" in text and ".add(" in text:
        return {
            "title": "List method confusion",
            "explanation": (
                "Your code is treating a Python list as if it supported an operation "
                "from a different collection type. First identify that the object is a "
                "list, then review which operations belong to lists."
            ),
            "why": (
                "The object you created is a list, and the operation you attempted "
                "is not available on that object."
            ),
            "concept": "Choosing the correct method for a data structure",
        }

    if "dictionary" in text and (".add(" in text or ".append(" in text):
        return {
            "title": "Dictionary operation confusion",
            "explanation": (
                "Your code is using an operation commonly associated with another "
                "collection type. A dictionary organizes information using key-value "
                "pairs, so its operations work around keys and values."
            ),
            "why": (
                "Dictionaries organize information around keys, so their operations "
                "are different from sequence collections such as lists."
            ),
            "concept": "Dictionary operations and key-value thinking",
        }

    if "keyerror" in text:
        return {
            "title": "Dictionary key confusion",
            "explanation": (
                "Python could not find the key your code requested. Look at the keys "
                "actually stored in the dictionary and compare them with the key you "
                "tried to use."
            ),
            "why": (
                "A dictionary lookup only succeeds when the requested key exists "
                "in that dictionary."
            ),
            "concept": "Dictionary key access",
        }

    if "indexerror" in text:
        return {
            "title": "List index confusion",
            "explanation": (
                "Your code tried to access a list position that does not exist. "
                "Remember that list positions start at 0 and that the available "
                "positions depend on the number of items in the list."
            ),
            "why": (
                "The requested position is outside the valid index range of the list."
            ),
            "concept": "List indexing",
        }

    if "typeerror" in text:
        return {
            "title": "Type mismatch",
            "explanation": (
                "Python received a value whose type does not fit the operation you "
                "attempted. Look at the types of the values involved before choosing "
                "the operation."
            ),
            "why": (
                "Different Python data types support different operations, and some "
                "operations require compatible types."
            ),
            "concept": "Python data types and operations",
        }

    if "nameerror" in text:
        return {
            "title": "Name or variable confusion",
            "explanation": (
                "Python could not find the name your code tried to use. Check whether "
                "the variable was created, whether its spelling matches, and whether "
                "you are using it in the correct place."
            ),
            "why": (
                "Python can only use a name when that name has been defined "
                "where you are trying to use it."
            ),
            "concept": "Variables and names",
        }

    if "syntaxerror" in text:
        return {
            "title": "Syntax structure confusion",
            "explanation": (
                "Python could not understand the structure of your statement. Look "
                "carefully at the line reported by Python and check the punctuation, "
                "quotes, brackets, colons, and indentation around it."
            ),
            "why": (
                "Python follows specific syntax rules, so a missing or misplaced "
                "part can stop the program from being understood."
            ),
            "concept": "Python syntax structure",
        }

    if "attributeerror" in text:
        return {
            "title": "Object and method confusion",
            "explanation": (
                "The object exists, but it does not provide the attribute or method "
                "your code requested. Start by identifying what type of object you "
                "created, then think about what that type can do."
            ),
            "why": (
                "Python only provides attributes and methods that belong to the "
                "object or its classes."
            ),
            "concept": "Objects, attributes, and methods",
        }

    if output and not output.startswith("Traceback"):
        return {
            "title": "Your result does not match the task",
            "explanation": (
                "Your program ran, so Python accepted the code, but the result does "
                "not yet match the task. Trace your program one line at a time and "
                "compare what each line does with what you wanted the program to do."
            ),
            "why": (
                "A program can be valid Python and still produce a result that "
                "does not match the intended behavior."
            ),
            "concept": f"Reasoning through the {topic_name} problem",
        }

    return {
        "title": "Let's inspect your mental model",
        "explanation": (
            "Start with the value or object involved. Identify its type, then trace "
            "what each line is asking Python to do. Your explanation of what you "
            "expected is an important clue."
        ),
        "why": (
            "Debugging becomes easier when you compare your expected behavior with "
            "what Python actually did, one step at a time."
        ),
        "concept": f"Debugging {topic_name}",
    }


@app.post("/topics/<int:topic_id>/run")
def run_code(topic_id):
    with get_db() as connection:
        topic = connection.execute(
            "SELECT name, practice FROM topics WHERE id = ?",
            (topic_id,),
        ).fetchone()

    if topic is None:
        return jsonify(error="Topic not found"), 404

    code = request.form.get("code", "")
    program_input = request.form.get("program_input", "")

    if not code.strip():
        return jsonify(error="Write some Python code first."), 400

    try:
        with tempfile.TemporaryDirectory() as directory:
            file_path = Path(directory) / "solution.py"
            file_path.write_text(code, encoding="utf-8")

            result = subprocess.run(
                [sys.executable, "-I", str(file_path)],
                input=program_input,
                capture_output=True,
                text=True,
                cwd=directory,
                timeout=3,
            )
    except subprocess.TimeoutExpired:
        return jsonify(
            error="Your code ran for more than 3 seconds and was stopped."
        ), 400

    # Only return what the learner's own program produced.
    # The expected answer and correction are never sent to the browser.
    output = (result.stdout or result.stderr).strip()

    practice_task = PRACTICE_TASKS.get(topic["name"])

    passed = False

    if practice_task and not result.returncode:
        passed = check_practice_solution(
            topic["name"],
            code,
            output,
            practice_task,
        )

    with get_db() as connection:
        connection.execute(
            """
            INSERT INTO practice_attempts (topic_id, passed)
            VALUES (?, ?)
            """,
            (topic_id, int(passed)),
        )

    return jsonify(
        output=output or "(no output)",
        passed=passed,
        has_error=bool(result.returncode),
    )


@app.post("/topics/<int:topic_id>/analyze")
def analyze_mistake(topic_id):
    with get_db() as connection:
        topic = connection.execute(
            "SELECT name FROM topics WHERE id = ?",
            (topic_id,),
        ).fetchone()

    if topic is None:
        return jsonify(error="Topic not found"), 404

    code = request.form.get("code", "")
    output = request.form.get("output", "")
    thought = request.form.get("thought", "").strip()
    expected_thought = request.form.get("expected_thought", "").strip()

    if not thought or not expected_thought:
        return jsonify(
            error=(
                "Tell us what you were trying to do and what you expected "
                "to happen."
            )
        ), 400

    analysis = explain_debugging_issue(
        topic["name"],
        code,
        output,
        thought,
        expected_thought,
    )

    # The correct answer is kept on the server and returned only
    # after the learner submits their own thinking.
    solution = PRACTICE_SOLUTIONS.get(topic["name"], {})

    return jsonify(
        title=analysis["title"],
        explanation=analysis["explanation"],
        why=analysis["why"],
        concept=analysis["concept"],
        mistake=output,
        thought=thought,
        correction=analysis["explanation"],
        solution=solution.get("code", ""),
        solution_explanation=solution.get("explanation", ""),
    )

@app.post("/topics/<int:topic_id>/mistakes")
def save_mistake(topic_id):
    values = [
        request.form.get(field, "").strip()
        for field in ("mistake", "thought", "correction", "why")
    ]

    if not all(values):
        return "Complete every mistake field", 400

    with get_db() as connection:
        topic = connection.execute(
            "SELECT path_id FROM topics WHERE id = ?",
            (topic_id,),
        ).fetchone()

        if topic is None:
            return "Topic not found", 404

        connection.execute(
            """
            INSERT INTO mistakes
            (topic_id, mistake, thought, correction, why)
            VALUES (?, ?, ?, ?, ?)
            """,
            (topic_id, *values),
        )

    return redirect(url_for("topic_detail", topic_id=topic_id))


@app.route("/mistakes")
def mistakes():
    with get_db() as connection:
        items = connection.execute(
            """
            SELECT mistakes.*, topics.name AS topic_name
            FROM mistakes
            JOIN topics ON topics.id = mistakes.topic_id
            ORDER BY mistakes.created_at DESC
            """
        ).fetchall()

    return render_template("mistakes.html", mistakes=items)


@app.post("/topics/<int:topic_id>/status")
def update_topic_status(topic_id):
    status = request.form.get("status")

    if status not in {"not_started", "learning", "completed"}:
        return "Invalid topic status", 400

    with get_db() as connection:
        topic = connection.execute(
            "SELECT path_id FROM topics WHERE id = ?",
            (topic_id,),
        ).fetchone()

        if topic is None:
            return "Topic not found", 404

        connection.execute(
            "UPDATE topics SET status = ? WHERE id = ?",
            (status, topic_id),
        )

    return redirect(url_for("topics", path_id=topic["path_id"]))

@app.route("/python/<topic_name>")
def python_topic_link(topic_name):
    with get_db() as connection:
        topic = connection.execute(
            """
            SELECT id
            FROM topics
            WHERE name = ? AND path_id = (
                SELECT id FROM learning_paths WHERE name = 'Python'
            )
            """,
            (topic_name,),
        ).fetchone()

    if topic is None:
        return "Topic not found", 404

    return redirect(url_for("topic_detail", topic_id=topic["id"]))
init_db()

if __name__ == "__main__":
    app.run(debug=False)
