from flask import Flask, request
import os
import json

app = Flask(__name__)

w_dir = '/home/labs/tirosh/chaya1/advancedPython/'
# w_dir = '/Volumes/Tirosh/chaya1/advancedPython/'
student_path = 'wis-advanced-python-2021-2022/students/'

@app.route("/")
def main():
    # '\n'.join(DB_students.keys())
    return ("""
    <form method="POST" action="/search">
    <input name="field">
    <input type="submit" value="Search">
    </form>
    """)+clickable_student(DB_students)


def read_json(j_file):
    with open(j_file) as f_in:
        return json.load(f_in)


def DBSutudent():
    stud_dir = w_dir+student_path
    # list all student files
    stud_filenames = os.listdir(stud_dir)
    stud_DB = {}
    for f in stud_filenames:
        j_file = stud_dir + f
        # read the file, get as dictionary
        stud_data = read_json(j_file)
        stud_data['JSON file name'] = f
        stud_DB[stud_data['name'].title()] = stud_data

    return dict(sorted(stud_DB.items()))


def clickable_student(stud_dict, mark='_'):
    real_mark=''
    if mark!='_':
        real_mark=mark
    html = """
    <h1> Advanced Python Course - Students:</h1>
    <ul>
    {}
    </ul>
    """.format("".join(["<li><a href=/students/"+student.replace(' ','_')+'/'+mark+">"+
                        student.replace(real_mark, '<mark>'+real_mark+'</mark>')+"</a></li>" for student in stud_dict.keys()]))
    return(html)


@app.route("/students/<name>/<mark>")
def show_json(name, mark):
    name = name.replace('_', ' ')
    html = """
    <h1>Student Information: {}</h1>
    <p>
    {}
    </p>
    """.format(name,"<br>".join(["<b>{}</b>: {}".format(key.title(),value) for key,value in DB_students[name].items() if value!=None]))
    if mark!='_':
        html = html.replace(mark, '<mark>'+mark+'</mark>')
    return(html)


@app.route("/search", methods=['POST'])
def students_search():
    field = request.form.get('field')
    match_students = {}
    for student in DB_students.items():
        if any([field in v for v in student[1].values() if v!=None]):
            match_students[student[0]] = student[1]
    html = clickable_student(match_students, field).replace("Advanced Python Course - Students:",
                                                     "Students matching the search term '{}'".format(field))
    # add highlight for search term
    #html = html.replace(field, '<mark>'+field+'</mark>')
    return (html)


DB_students = DBSutudent()

