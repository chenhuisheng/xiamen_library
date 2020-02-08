import copy
import os
from app import db
from flask import current_app
from app.models.project import Project
from app.models.video import Video
from app.models.project_video import ProjectVideo


def add_project_video(project_ids, video_id):
    ProjectVideo.query.filter_by(video_id=video_id).delete()
    db.session.commit()
    for project_id in project_ids:
        project = Project.query.get(project_id)
        if project:
            videos = Video.query.\
                filter_by(id=video_id).\
                first()
            new_video_sort = copy.deepcopy(project.video_sort)
            if video_id not in new_video_sort:
                new_video_sort.insert(0, video_id)
                project.video_sort = new_video_sort
                project.save()
            projectvideos = ProjectVideo(
                    project_id=project_id,
                    video_id=video_id
                )
            db.session.add(projectvideos)
            db.session.commit()


def generate_project(video_id, project_ids):
    ProjectVideo.query.filter_by(video_id=video_id).delete()
    if not project_ids:
        project_picture = ProjectVideo(
            project_id=0,
            video_id=video_id
        )
        db.session.add(project_picture)
        db.session.commit()
        return True
    projects = Project.query.filter(Project.id.in_(project_ids))
    projects_ids = [project.id for project in projects]
    for project_id in projects_ids:
        project_video = ProjectVideo(
            project_id=project_id,
            video_id=video_id
        )
        db.session.add(project_video)
    db.session.commit()
            
            
def get_video_query(project_id):
    if not project_id:
        query = Video.query
    else:
        query = Video.query. \
            join(ProjectVideo, Video.id == ProjectVideo.video_id). \
            filter(ProjectVideo.project_id == project_id)
    return query


def get_video_project(video_id):
    videos = Project.query.\
        join(ProjectVideo, Project.id == ProjectVideo.project_id).\
        with_entities(Project.id, Project.title).\
        filter(ProjectVideo.video_id == video_id).\
        all()
    res = [i._asdict() for i in videos]
    return res


def get_size(url):
    size = os.path.getsize(current_app.config['APP_PATH']+url)
    return size


def bindTitles(items):
    video_ids = [b['id'] for b in items]
    titles = ProjectVideo.query.\
        join(Project, ProjectVideo.project_id==Project.id).\
        add_columns(ProjectVideo.video_id, Project.id, Project.title).\
        filter(ProjectVideo.video_id.in_(video_ids)).\
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


def batch_add_videos(datas):
    for data in datas:
        data['file_type'] = os.path.splitext(data['file_path'])[1].strip('.')
        data['file_size'] = get_size(data['file_path'])
        video = Video.create(data)
        res = video.to_dict()
        project_ids = data.get('project_ids', [])
        generate_project(res['id'], project_ids)
