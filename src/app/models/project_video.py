from app import db
from ._base import SessionMixin
from app.models import Video
from app.service.search import Search


class ProjectVideo(db.Model, SessionMixin):
    __tablename__ = 'project_video'

    id = db.Column(db.Integer, primary_key=True)
    video_id = db.Column(db.Integer, nullable=False, default=0)
    project_id = db.Column(db.Integer, nullable=False, default=0)

    def __repr__(self):
        return '<ProjectVideo: %r>' % self.id

    @staticmethod
    def remove_video(project_id, video_id):
        project_video = ProjectVideo.get_project_video(project_id, video_id)
        if project_video:
            project_video.delete()

    @staticmethod
    def get_project_video(project_id, video_id):
        project_video = ProjectVideo.query.filter_by(project_id=project_id).\
            filter_by(video_id=video_id).\
            first()
        return project_video

    @staticmethod
    def generate_project_video(project_id, video_ids):
        videos = Video.query.filter(Video.id.in_(video_ids))
        video_ids = [video.id for video in videos]
        for video_id in video_ids:
            project_video = ProjectVideo.get_project_video(project_id, video_id)
            if project_video:
                continue
            project_video = ProjectVideo(
                project_id=project_id,
                video_id=video_id
            )
            db.session.add(project_video)
        db.session.commit()

    @staticmethod
    def get_project_videos_with_paginate(project_id):
        query = Video.query. \
            join(ProjectVideo, ProjectVideo.video_id==Video.id).\
            filter(ProjectVideo.project_id==project_id). \
            order_by(ProjectVideo.created_at.desc())
        res = Search().init_query(query).load(Video).paginate()
        return res
