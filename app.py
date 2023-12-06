from genericpath import isdir
from flask import Flask, render_template, request, url_for, redirect

import json
from os import listdir
from os.path import join, isfile, exists
import requests
from hashlib import new
import mysql.connector

app = Flask(__name__)

def database_connection():
    mydb = mysql.connector.connect(
        host="sql8.freemysqlhosting.net",
        user="sql8668244",
        password="9S8qhGsQt6",
        database="sql8668244",
    )
    return mydb

# Establish a connection to the database
mydb = database_connection()

# Create a cursor object to interact with the database
mycursor = mydb.cursor()

# Define the structure of the 'Users' table
table_structure = (
    "id INT AUTO_INCREMENT PRIMARY KEY, "
    "Username VARCHAR(255) NOT NULL, "
    "Password VARCHAR(255) NOT NULL, "
    "Email VARCHAR(255) NOT NULL, "
    "Completed_exercises TEXT, "
    "Points INT DEFAULT 0"
)

# Write SQL query to create the 'Users' table
create_table_query = f"CREATE TABLE IF NOT EXISTS Users ({table_structure})"

# Execute the SQL query
mycursor.execute(create_table_query)


# Commit the changes to the database
mydb.commit()

# Close the cursor and database connection
mycursor.close()
mydb.close()

# parameters should a String
# only enter names of table and column (eg:Users,Username)
def insert_element(table, column, element):
    if isinstance(table, str) and isinstance(column, str) and isinstance(element, str):
        mydb = database_connection()
        mycursor = mydb.cursor()
        sql = f"INSERT INTO {table} ({column}) VALUES (%s)"
        val = element
        mycursor.execute(sql, val)
        mydb.commit()

# format:
# column = '(Username, Password,Email,Completed_exercises)'
# table = 'Users'
# val = ("Yin ","Bonj","leYin@comp.com",Ex20)
def insert_multiple_elements(mydb, table, columns, val):
    mycursor = mydb.cursor()
    number_of_c = 0
    for i in columns:
        if i == ",":
            number_of_c += 1
    sql = f"INSERT INTO {table} {columns} VALUES ({(number_of_c)*'%s,'+'%s'})"
    mycursor.execute(sql, val)
    mydb.commit()


# same requirements as insert_table
# displays either all or one columns at the moment
def row_displayer(table, column):
    if isinstance(table, str) and isinstance(column, str):
        mydb = database_connection()
        mycursor = mydb.cursor()
        mycursor.execute(f"SELECT {column} FROM {table}")
        row = mycursor.fetchall()
        return row


# name of exercise and username should be string
def add_completed_exercise(exercise, username):
    mydb = database_connection()
    mycursor = mydb.cursor()
    global user
    if exercise["difficulty"].lower() == "easy":
        difficulty = 1
    elif exercise["difficulty"].lower() == "medium":
        difficulty = 2
    else:
        difficulty = 3

    sql = f"SELECT Completed_exercises FROM Users WHERE Username='{username}'"
    mycursor.execute(sql)
    tupl = mycursor.fetchall()
    completed_exe = tupl[0][0].strip("][").split(",")
    for i in range(len(completed_exe)):
        completed_exe[i] = completed_exe[i].replace('"', "")
        completed_exe[i] = completed_exe[i].replace("'", "")
        completed_exe[i] = completed_exe[i].replace(" ", "")
    if f"Ex{exercise['id']}|" not in completed_exe:
        completed_exe.append(f"Ex{exercise['id']}|")
    else:
        difficulty = 0
    if "" in completed_exe:
        completed_exe.remove("")
    completed_exe = str(completed_exe)

    mydb.commit()
    users = row_displayer("Users", "*")
    found_flag = False
    for _user in users:
        if _user[1] == username:
            target_user = _user
            break
    user = target_user




# all paramters should be string
def change_detail(column, username, new_detail):
    mydb = database_connection()
    mycursor = mydb.cursor()
    if column == "Password":
        h = new("sha256")
        byte_string = bytes(new_detail, "utf-8")
        h.update(byte_string)
        new_detail = h.hexdigest()
    sql1 = f"UPDATE Users SET {column} = %s WHERE Username =%s"
    val1 = (new_detail, username)
    mycursor.execute(sql1, val1)

    mydb.commit()


def read_file(filepath):
    with open(filepath, "r") as file:
        test_in = file.read()
        return test_in


def get_exercise_list():
    exercise_list = []
    folders = [folder for folder in listdir("./questions") if isdir(join("./questions", folder))]
    for folder in folders:
        exerc_path = [file for file in listdir(join("./questions", folder)) if file.endswith(".json")][0]
        exercise = read_file(join("./questions", folder, exerc_path))
        exercise_list.append(json.loads(exercise))
    return exercise_list


def get_exercise(filepath):
    ex_json = read_file(filepath)
    ex_dict = json.loads(ex_json)
    return ex_dict


def test_fetcher():
    directory = f"questions/{question_number}"
    test_directory = f"{directory}/test_inputs"
    output_directory = f"{directory}/test_outputs"
    test_inputs = [
        file for file in listdir(test_directory) if isfile(join(test_directory, file))
    ]
    given_inputs = []
    expected_outputs = []
    for test in test_inputs:
        given_inputs.append(read_file(f"{test_directory}/{test}"))
        expected_outputs.append(read_file(f"{output_directory}/{test}"))
    return given_inputs, expected_outputs


def run_individual_test(language_id, source_code, stdin):
    payload = generate_payload(language_id, source_code, stdin)
    get_token = generate_token(payload)
    GET_URL = f"https://judge0-ce.p.rapidapi.com/submissions/{get_token}"
    get_response = requests.request(
        "GET", GET_URL, headers=GET_HEADERS, params=GET_QUERYSTRING
    )
    converted_get_response = json.loads(get_response.text)
    get_output = converted_get_response["stdout"]
    if not get_output:
        return
    return get_output[:-1]


def run_tests(language_id, source_code):
    inputs, expected_outputs = test_fetcher()
    fail_count = 0
    for test, expected in zip(inputs, expected_outputs):
        given_output = run_individual_test(language_id, source_code, test)
        if given_output != expected:
            fail_count += 1
    return fail_count


def initialise_language_ids():
    return {
        "Assembly (NASM 2.14.02)": 45,
        "Bash (5.0.0)": 46,
        "C (GCC 7.4.0)": 48,
        "C++ (GCC 7.4.0)": 52,
        "C (GCC 8.3.0)": 49,
        "C++ (GCC 8.3.0)": 53,
        "C (GCC 9.2.0)": 50,
        "C++ (GCC 9.2.0)": 54,
        "C# (Mono 6.6.0.161)": 51,
        "Common Lisp (SBCL 2.0.0)": 55,
        "D (DMD 2.089.1)": 56,
        "Elixir (1.9.4)": 57,
        "Erlang (OTP 22.2)": 58,
        "Executable": 44,
        "Fortran (GFortran 9.2.0)": 59,
        "Go (1.13.5)": 60,
        "Haskell (GHC 8.8.1)": 61,
        "Java (OpenJDK 13.0.1)": 62,
        "JavaScript (Node.js 12.14.0)": 63,
        "Lua (5.3.5)": 64,
        "OCaml (4.09.0)": 65,
        "Octave (5.1.0)": 66,
        "Pascal (FPC 3.0.4)": 67,
        "PHP (7.4.1)": 68,
        "Plain Text": 43,
        "Prolog (GNU Prolog 1.4.5)": 69,
        "Python (2.7.17)": 70,
        "Python (3.8.1)": 71,
        "Ruby (2.7.0)": 72,
        "Rust (1.40.0)": 73,
        "TypeScript (3.7.4)": 74,
    }


def generate_payload(language_id, dirty_source_code, stdin):
    source_code = dirty_source_code.replace('"', "'")
    source_code = source_code.replace("\n", "\\n")
    source_code = source_code.replace(
        chr(13), "\\n")  # Converts Carriage Returns
    source_code = source_code.replace(chr(9), "\\t")  # Converts Tabs
    payload = (
        '{"language_id":'
        + str(language_id)
        + ',"source_code":"'
        + str(source_code)
        + '","stdin":"'
        + str(stdin)
        + '"}'
    )
    return payload


def get_boilerplate(id):
    filepath = f"./boilerplates/{id}_boilerplate.txt"
    if not exists(filepath):
        return ""
    with open(filepath, "r") as file:
        boilerplate = file.read()
    return boilerplate


def generate_token(payload_data):
    post_response = requests.request(
        "POST",
        POST_URL,
        data=payload_data,
        headers=POST_HEADERS,
        params=POST_QUERYSTRING,
    )
    converted_response = json.loads(post_response.text)
    return converted_response["token"]


def check_valid_username(username, db):
    for row in row_displayer("Users", "*"):
        if username in row:
            return False
    return True


def hashify(string):
    h = new("sha256")
    byte_string = bytes(string, "utf-8")
    h.update(byte_string)
    return h.hexdigest()


def register_pressed(form):
    username = form["reg_username"]
    email = form["reg_email"]
    password = form["reg_password"]
    db = database_connection()
    if not check_valid_username(username, db):
        return "Invalid Username"
    if not check_valid_username(email, db):
        return "Invalid Email"
    hashed_password = hashify(password)
    hashed_email = hashify(email)
    insert_multiple_elements(
        db,
        "Users",
        "(Username, Password, Email, Completed_exercises)",
        [
            username,
            hashed_password,
            hashed_email,
            "",
        ],
    )
    users = row_displayer("Users", "*")
    for _user in users:
        if _user[1] == username:
            target_user = _user
            break
    global user
    user = target_user
    return "Logged in"


def get_position(username):
    sql = "SELECT Username, Points FROM Users ORDER BY Points DESC"

    mydb = database_connection()
    mycursor = mydb.cursor()
    mycursor.execute(sql)
    leaderboard = mycursor.fetchall()
    for index, _user in enumerate(leaderboard):
        if _user[0] == user[1]:
            return index + 1


def login_pressed(form):
    username = form["log_username"]
    password = form["log_password"]
    db = ["test"]
    users = row_displayer("Users", "*")
    found_flag = False
    for user in users:
        if user[1] == username:
            found_flag = True
            target_user = user
            break
    if not found_flag:
        return None, "No such user!"
    hashed_password = hashify(password)
    if target_user[2] != hashed_password:
        return None, "Invalid Password"
    return target_user, "Logged In"


def submit_code_pressed(form):
    global question_number
    language = form["language"]
    language_id = language_ids[language]
    source_code = form["codearea"]
    
    # Check if the source_code is empty or identical to the initial code.
    initial_code = get_boilerplate(language_id)  # Get initial code
    if not source_code or source_code.strip() == initial_code.strip():
        return 1, None, None
    
    # Run tests on the user-submitted code and get the fail count.
    fail_count = run_tests(language_id, source_code)

    # If there are no test failures and there is a logged-in user, update user's progress.
    if not fail_count and user:
        filepath = f"./questions/{question_number}/{question_number}.json"
        current_exercise = get_exercise(filepath)
        add_completed_exercise(current_exercise, user[1])

    return fail_count, source_code, language_id



language_ids = initialise_language_ids()
POST_URL = "https://judge0-ce.p.rapidapi.com/submissions"
POST_QUERYSTRING = {"base64_encoded": "false", "fields": "*"}
POST_HEADERS = {
    "content-type": "application/json",
    "x-rapidapi-host": "judge0-ce.p.rapidapi.com",
    "x-rapidapi-key": "bcde6420c5mshb86b99b73d8897ep160af9jsn208c98bd1a37",
}
GET_QUERYSTRING = {"base64_encoded": "false", "fields": "stdout"}
GET_HEADERS = {
    "x-rapidapi-host": "judge0-ce.p.rapidapi.com",
    "x-rapidapi-key": "bcde6420c5mshb86b99b73d8897ep160af9jsn208c98bd1a37",
}
user = None


@app.route("/profile")
def profile():
    global user
    if not user:
        return render_template("profile_page.html", user=None, rank="N/A", title="Profile Page")
    return render_template("profile_page.html", user=user, rank=get_position(user[1]), title=user[1]+"'s Profile")


@app.route("/login", methods=["GET", "POST"])
def login():
    global user
    valid = False
    if request.method == "POST":
        if "reg_username" in request.form:
            valid = register_pressed(request.form)
            if valid == "Logged in":
                return redirect(url_for("index"), code=302)
        else:
            user, valid = login_pressed(request.form)
            if valid == "Logged In":
                return redirect(url_for("index"), code=302)

    return render_template("login_page.html", valid=valid, title="Login")


@app.route("/", methods=["GET", "POST"])
def index():
    exercise_list = get_exercise_list()
    exercise_list = sorted(exercise_list, key=lambda d: d["id"])
    global question_number
    global user
    difficulty_filter = "all"
    if request.method == "POST":
        if "status" in request.form:
            difficulty_filter = request.form["status"]
        if "go_button" in request.form:
            question_number = request.form["go_button"][4:]
            return redirect(url_for("exercise"), code=302)
    return render_template(
        "index.html",
        exercises=exercise_list,
        difficulty=difficulty_filter,
        user=user,
        title="Exercises"
    )


@app.route("/exercise", methods=["GET", "POST"])
def exercise():
    global user
    global question_number
    fail_count = -1
    source_code = ""
    language_id = 71
    if request.method == "POST":
        form = request.form
        fail_count, source_code, language_id = submit_code_pressed(form)
    boilerplate = get_boilerplate(language_id)
    filepath = f"./questions/{question_number}/{question_number}.json"
    current_exercise = get_exercise(filepath)
    return render_template(
        "exercise.html",
        exercise=current_exercise,
        failed=fail_count,
        code=source_code,
        boilerplate=boilerplate,
        user=user,
        title=current_exercise["title"]
    )


@app.route("/help")
def help():
    return render_template("help.html", title="Help")


@app.route("/terms&conditions")
def terms():
    return render_template("terms&conditions.html", title="Terms & Conditions")


@app.route("/logout")
def logout():
    global user
    user = None
    return redirect(url_for("index"), code=302)


@app.route("/leaderboard")
def leaderboard():
    global user
    mydb = database_connection()
    mycursor = mydb.cursor()
    sql = f"SELECT Username, Points FROM Users ORDER BY Points DESC LIMIT 10"
    mycursor.execute(sql)
    ranking = mycursor.fetchall()
    if user:
        topbool = True if any(
            user[1] in subrank for subrank in ranking) else False
    else:
        topbool = False
    return render_template("leaderboard.html", ranking=ranking, user=user, topbool=topbool, title="Leaderboard")


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5050, debug=True)
