from app import db
from ._base import SessionMixin
from app.models import Picture
from app.service.search import Search


class ProjectPicture(db.Model, SessionMixin):
    __tablename__ = 'project_picture'

    id = db.Column(db.Integer, primary_key=True)
    picture_id = db.Column(db.Integer, nullable=False, default=0)
    project_id = db.Column(db.Integer, nullable=False, default=0)

    def __repr__(self):
        return '<ProjectPicture: %r>' % self.id

    @staticmethod
    def remove_picture(project_id, picture_id):
        project_picture = ProjectPicture.get_project_picture(project_id, picture_id)
        if project_picture:
            project_picture.delete()

    @staticmethod
    def get_one_project_picture(project_id, picture_id):
        project_picture = ProjectPicture.query.filter_by(project_id=project_id).\
            filter_by(picture_id=picture_id).\
            first()
        return project_picture

    @staticmethod
    def get_project_image(project_id):
        project_image = Picture.query.\
            join(ProjectPicture, Picture.id==ProjectPicture.picture_id).\
            filter(Picture.type=='image').\
            filter(ProjectPicture.project_id==project_id).\
            order_by(ProjectPicture.created_at.desc()).\
            all()
        res = [image.to_dict() for image in project_image]
        return res

    @staticmethod
    def get_project_banner(project_id):
        project_banner = Picture.query.\
            join(ProjectPicture, Picture.id==ProjectPicture.picture_id).\
            filter(ProjectPicture.project_id==project_id). \
            filter(Picture.type == 'banner'). \
            order_by(ProjectPicture.created_at.desc()).\
            all()
        res = [banner.to_dict() for banner in project_banner]
        return res

    @staticmethod
    def get_project_image_with_paginate(project_id):
        query = Picture.query.\
            join(ProjectPicture, Picture.id==ProjectPicture.picture_id).\
            filter(Picture.type=='image').\
            filter(ProjectPicture.project_id==project_id).\
            order_by(ProjectPicture.created_at.desc())
        res = Search().init_query(query).load(Picture).paginate()
        return res

    @staticmethod
    def get_project_banner_with_paginate(project_id):
        query = Picture.query.\
            join(ProjectPicture, Picture.id==ProjectPicture.picture_id).\
            filter(Picture.type=='banner').\
            filter(ProjectPicture.project_id==project_id).\
            order_by(ProjectPicture.created_at.desc())
        res = Search().init_query(query).load(Picture).paginate()
        return res

    @staticmethod
    def generate_project_picture(project_id, picture_ids):
        pictures = Picture.query.filter(Picture.id.in_(picture_ids))
        picture_ids = [picture.id for picture in pictures]
        for picture_id in picture_ids:
            project_picture = ProjectPicture.get_one_project_picture(project_id, picture_id)
            if project_picture:
                continue
            project_picture = ProjectPicture(
                project_id=project_id,
                picture_id=picture_id
            )
            db.session.add(project_picture)
        db.session.commit()
