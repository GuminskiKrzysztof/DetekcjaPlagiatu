from flask import Blueprint, render_template

project_bp = Blueprint('project', __name__)

@project_bp.route('/')
def home():
    return render_template('index.html', active_page='home')

@project_bp.route('/jak-to-dziala')
def jak_to_dziala():
    return render_template('how-it-works.html', active_page='how-it-works')

@project_bp.route('/dodaj-projekt')
def dodaj_projekt():
    return render_template('add-project.html', active_page='add-project')

@project_bp.route('/edytor')
def edytor():
    return render_template('editor-code.html', active_page='analyze-code')

@project_bp.route('/o-nas')
def o_nas():
    return render_template('about-us.html', active_page='about-us')
