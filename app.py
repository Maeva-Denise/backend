import os
from flask import Flask, send_from_directory

from views.courses import courses_view
from views.students import students_view
from views.classes import class_view
from views.class_courses import class_course_view
from views.role import roles_view

app = Flask(__name__)

app.register_blueprint(courses_view)
app.register_blueprint(students_view)
app.register_blueprint(class_view)
app.register_blueprint(class_course_view)
app.register_blueprint(roles_view)
    