from app import db
from ._base import SessionMixin
from app.models.project_book import ProjectBook
from app.models.project_picture import ProjectPicture


class Project(db.Model, SessionMixin):
    __tablename__ = 'project'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False, default='')
    summary = db.Column(db.Text, nullable=False, default='')  # 专题介绍
    creater_id = db.Column(db.Integer, nullable=False, default=0)
    picture_sort = db.Column(db.JsonBlob, nullable=False, default=[])  # 图片列表详情（排序）
    theme_id = db.Column(db.Integer, nullable=False, default=1) #样式id(1-7)

    def get_with_pictures(self):
        project_pictures = ProjectPicture.query.\
            filter_by(project_id=self.id).\
            all()
        res = self.to_dict()
        pictures = [picture.to_dict() for picture in project_pictures]
        res['pictures'] = pictures
        return res

    def get_with_books(self):
        project_books = ProjectBook.query.\
            filter_by(project_id=self.id).\
            all()
        res = self.to_dict()
        books = [book.to_dict() for book in project_books]
        res['books'] = books
        return res

    def __repr__(self):
        return '<Project: %r>' % self.id

    @staticmethod
    def generate_project(book_id, project_ids):
        ProjectBook.query.filter_by(book_id=book_id).delete()
        if not project_ids:
            project_book = ProjectBook(
                project_id=0,
                book_id=book_id
            )
            db.session.add(project_book)
            db.session.commit()
            return True
        projects = Project.query.filter(Project.id.in_(project_ids))
        projects_ids = [project.id for project in projects]
        for project_id in projects_ids:
            project_book = ProjectBook(
                project_id=project_id,
                book_id=book_id
            )
            db.session.add(project_book)
        db.session.commit()

    @staticmethod
    def get_book_project(book_id):
        projects = Project.query.\
            join(ProjectBook, Project.id == ProjectBook.project_id).\
            with_entities(Project.id, Project.title).\
            filter(ProjectBook.book_id == book_id).\
            all()
        res = [i._asdict() for i in projects]
        return res

    @staticmethod
    def get_picture_project(picture_id):
        pictures = Project.query.\
            join(ProjectPicture, Project.id == ProjectPicture.project_id).\
            with_entities(Project.id, Project.title).\
            filter(ProjectPicture.picture_id == picture_id).\
            all()
        res = [i._asdict() for i in pictures]
        return res

    @staticmethod
    def bindTitles(items):
        book_ids = [b['id'] for b in items]
        titles = ProjectBook.query.\
            join(Project, ProjectBook.project_id==Project.id).\
            add_columns(ProjectBook.book_id, Project.id, Project.title).\
            filter(ProjectBook.book_id.in_(book_ids)).\
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