import os
from pickle import GET
from flask import Flask, redirect, url_for
from flask import render_template
from flask import request
from flask_sqlalchemy import SQLAlchemy

current_dir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + os.path.join(current_dir, "database.sqlite3") 
db = SQLAlchemy()
db.init_app(app)
app.app_context().push()


class student(db.Model):
    __tablename__ = 'student'
    student_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    roll_number = db.Column(db.String, unique=True,nullable=False)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String)
    courses = db.relationship('enrollments', backref='student')

class course(db.Model):
    __tablename__ = 'course'
    course_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    course_code = db.Column(db.String, unique=True,nullable=False)
    course_name = db.Column(db.String, nullable=False)
    course_description = db.Column(db.String)
    courses = db.relationship('enrollments', backref='course')

class enrollments(db.Model):
    __tablename__ = 'enrollments'
    enrollment_id = db.Column(db.Integer,autoincrement=True, primary_key=True)
    estudent_id = db.Column(db.Integer,  db.ForeignKey("student.student_id"), nullable=False)
    ecourse_id = db.Column(db.Integer,  db.ForeignKey("course.course_id"), nullable=False)



@app.route("/", methods=["GET", "POST"])
def index():
    count = None
    if request.method == "GET":
        if student.query.filter().first() == None:
            count = 0
            # return render_template("home.html")
        else:
            count = 1
        student_id = student.query.all()
        return render_template("index.html", student_id=student_id, count = count)

@app.route('/student/create', methods=['GET', 'POST'])
def add_student():
    if request.method == 'GET':
        return render_template('add_student.html')
    if request.method == 'POST': 
        roll = request.form['roll']
        f_name = request.form['f_name']
        l_name = request.form['l_name']
        courses = request.form.getlist('courses')

        stu = student(roll_number = roll, first_name = f_name, last_name = l_name)

        if bool(student.query.filter_by(roll_number =roll).first()) == False:
            db.session.add(stu)
            db.session.commit()

            for course in courses:
                if course == "course_1":
                    stu = enrollments(estudent_id = roll, ecourse_id = 1)
                    db.session.add(stu)
                    db.session.commit()

                if course == "course_2":
                    stu = enrollments(estudent_id = roll, ecourse_id = 2)
                    db.session.add(stu)
                    db.session.commit()

                if course == "course_3":
                    stu = enrollments(estudent_id = roll, ecourse_id = 3)
                    db.session.add(stu)
                    db.session.commit()

                if course == "course_4":
                    stu = enrollments(estudent_id = roll, ecourse_id = 4)
                    db.session.add(stu)
                    db.session.commit()

        else:
            return render_template('invalid.html')

    return redirect(url_for('index'))

@app.route('/student/<int:student_id>', methods=['GET', 'POST'])
def display_student(student_id):
    rolln = student.query.filter_by(student_id = student_id).first()
    roll, f_name, l_name = rolln.roll_number, rolln.first_name, rolln.last_name

    all_courses = course.query.all()
    course_taken = enrollments.query.filter_by(estudent_id = int(roll)).all()
    lists = []
    for ctaken in course_taken:
        lists.append(ctaken.ecourse_id)
    print(all_courses)

    return render_template('display.html',
                            roll = roll, f_name = f_name,
                            l_name = l_name, all_courses = all_courses,
                            lists = lists, course_taken = course_taken)


@app.route('/student/<int:student_id>/update', methods=['GET', 'POST'])
def update(student_id):
    rolln = student.query.filter_by(student_id = student_id).first()
    roll = rolln.roll_number
    f_name = rolln.first_name
    l_name = rolln.last_name
    # courses = request.form.getlist('courses')

    if request.method == 'POST':
        rolln = student.query.filter_by(student_id = student_id).first()
        roll = rolln.roll_number
        f_name = request.form['f_name']
        l_name = request.form['l_name']
        courses = request.form.getlist('courses')

        studs = student.query.filter_by(roll_number = roll).first()
        db.session.delete(studs)
        db.session.commit()

        stu = student(roll_number = roll, first_name = f_name, last_name = l_name)
        db.session.add(stu)
        db.session.commit()

        cour = enrollments.query.filter_by(estudent_id = roll).all()
        for i in cour:
            db.session.delete(i)


        for course in courses:
            if course == "course_1":
                stu = enrollments(estudent_id = roll, ecourse_id = 1)
                db.session.add(stu)
                db.session.commit()

            if course == "course_2":
                stu = enrollments(estudent_id = roll, ecourse_id = 2)
                db.session.add(stu)
                db.session.commit()

            if course == "course_3":
                stu = enrollments(estudent_id = roll, ecourse_id = 3)
                db.session.add(stu)
                db.session.commit()

            if course == "course_4":
                stu = enrollments(estudent_id = roll, ecourse_id = 4)
                db.session.add(stu)
                db.session.commit()

        return redirect(url_for('index'))

    return render_template('update.html',student_id= student_id, roll = roll, f_name = f_name,
                                         l_name = l_name)

@app.route('/student/<int:student_id>/delete', methods=['GET', 'POST'])
def delete(student_id):
    stud = student.query.filter_by(student_id = student_id).first()
    sid = stud.roll_number
    cour = enrollments.query.filter_by(estudent_id = sid).all()
    for i in cour:
        db.session.delete(i)
    
    db.session.delete(stud)
    db.session.commit()
    return redirect(url_for('index'))



if __name__ == '__main__':
  # Run the Flask app
  app.run(
    host='0.0.0.0',
    debug=True,
    port=8080
  )
