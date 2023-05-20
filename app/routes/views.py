from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user


from app.models.database import db, Evaluation_Windows, Projects,ProjectsStatusCount, Researchers, Researchers_Projects

views = Blueprint('views', __name__)

@views.route('/')
@login_required
def home():
    return render_template('index.html')

@views.route('/projects')
@login_required
def projects():
    projects2show = Projects.query.all()
    user_type = request.args.get('user_type')
    user = current_user

    counts_by_status = {
            'approved': 0,
            'require changes': 0,
            'submitted for evaluation': 0,
            'not approved': 0
    }

    if user_type == 'evaluator':
        print('evaluator')
        projects2show = Projects.query.all()
        project_counts = ProjectsStatusCount.query.all()
        for row in project_counts:
            counts_by_status[row.status.value] = row.count

    elif user_type == 'researcher':
        print('researcher')
        render_template('404.html')

    researcher_profile_pictures = []
    for project in projects2show:
        project_id = project.id
        profile_pictures = db.session.query(Researchers.profile_picture) \
            .join(Researchers_Projects) \
            .filter(Researchers_Projects.fk_projects == project_id) \
            .all()
        researcher_profile_pictures.append(profile_pictures)


    evaluation_window = Evaluation_Windows.query.first()
    evaluation_window_from = evaluation_window.evaluation_windows_from.strftime("%Y/%m")
    evaluation_window_to = evaluation_window.evaluation_windows_to.strftime("%Y/%m")

    return render_template('projects.html',
                           name=user.name,
                           surname=user.surname,
                           from_date=evaluation_window_from,
                           to_date=evaluation_window_to,
                           counts_by_status=counts_by_status,
                           projects=projects2show,
                           researcher_profile_pictures=researcher_profile_pictures,
                           user_type=user_type)

@views.route('/project')
@login_required
def project():
    return render_template('project.html', name=current_user.name, surname=current_user.surname)