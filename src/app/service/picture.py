import copy
from app import db
from flask import request
from app.models.project import Project
from app.models.picture import Picture
from app.models.project_picture import ProjectPicture


def add_project_picture(project_ids, picture_id):
    ProjectPicture.query.filter_by(picture_id=picture_id).delete()
    db.session.commit()
    for project_id in project_ids:
        project = Project.query.get(project_id)
        if project:
            pictures = Picture.query.\
                filter_by(id=picture_id).\
                first()
            new_picture_sort = copy.deepcopy(project.picture_sort)
            if picture_id not in new_picture_sort:
                new_picture_sort.insert(0, picture_id)
                project.picture_sort = new_picture_sort
                project.save()
            projectpictures = ProjectPicture(
                    project_id=project_id,
                    picture_id=picture_id
                )
            db.session.add(projectpictures)
            db.session.commit()


def generate_project(project_ids, picture_id):
    ProjectPicture.query.filter_by(picture_id=picture_id).delete()
    if not project_ids:
        project_picture = ProjectPicture(
            project_id=0,
            picture_id=picture_id
        )
        db.session.add(project_picture)
        db.session.commit()
        return True
    projects = Project.query.filter(Project.id.in_(project_ids))
    projects_ids = [project.id for project in projects]
    for project_id in projects_ids:
        project_picture = ProjectPicture(
            project_id=project_id,
            picture_id=picture_id
        )
        db.session.add(project_picture)
    db.session.commit()


def get_picture_query(project_id, type_):
    if not project_id:
        query = Picture.query.filter_by(type=type_)
    else:
        query = Picture.query. \
            join(ProjectPicture, Picture.id == ProjectPicture.picture_id). \
            filter(Picture.type == type_). \
            filter(ProjectPicture.project_id == project_id)
    return query


def bindTitles(items):
    picture_ids = [b['id'] for b in items]
    titles = ProjectPicture.query.\
        join(Project, ProjectPicture.project_id==Project.id).\
        add_columns(ProjectPicture.picture_id, Project.id, Project.title).\
        filter(ProjectPicture.picture_id.in_(picture_ids)).\
        all()
    titles_obj = {}
    for title in titles:
        title = title[1:]
        titles_obj.setdefault(title[0], []).append({
            'id': title[1],
            'name': title[2]
        })
    for item in items:
        item['projects'] = titles_obj.get(item['id'], [])
    return items