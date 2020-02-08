from plugin.exceptions import ApiError
from app import db
from ._base import SessionMixin
from app.service.search import Search
from app.models import Book
from app.service.utils import sort_by_id_list


class ProjectBook(db.Model, SessionMixin):
    __tablename__ = 'project_book'

    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, nullable=False, default=0)
    project_id = db.Column(db.Integer, nullable=False, default=0)

    @staticmethod
    def get_project_book(project_id, book_id):
        project_book = ProjectBook.query.filter_by(project_id=project_id).\
            filter_by(book_id=book_id).\
            first()
        return project_book

    @staticmethod
    def get_project_books(project_id):
        project_books = ProjectBook.query.\
            filter_by(project_id=project_id).\
            order_by(ProjectBook.created_at.desc()).\
            all()
        book_ids = [d.book_id for d in project_books]
        books = Book.query.filter(Book.id.in_(book_ids)).all()
        books = sort_by_id_list(books, book_ids)
        res = [book.to_dict() for book in books]
        return res

    @staticmethod
    def get_project_books_with_paginate(project_id):
        query = Book.query. \
            join(ProjectBook, ProjectBook.book_id==Book.id).\
            filter(ProjectBook.project_id==project_id). \
            filter(Book.book_type=='book').\
            order_by(ProjectBook.created_at.desc())
        res = Search().init_query(query).load(Book).paginate()
        return res

    @staticmethod
    def get_project_magazines_with_paginate(project_id):
        query = Book.query. \
            join(ProjectBook, ProjectBook.book_id==Book.id).\
            filter(ProjectBook.project_id==project_id). \
            filter(Book.book_type=='magazine').\
            order_by(ProjectBook.created_at.desc())
        res = Search().init_query(query).load(Book).paginate()
        return res

    @staticmethod
    def get_project_papers_with_paginate(project_id):
        query = Book.query. \
            join(ProjectBook, ProjectBook.book_id==Book.id).\
            filter(ProjectBook.project_id==project_id). \
            filter(Book.book_type=='paper').\
            order_by(ProjectBook.created_at.desc())
        res = Search().init_query(query).load(Book).paginate()
        return res

    @staticmethod
    def generate(project_id, books):
        ids = [book['book_id'] for book in books]
        books = Book.query.filter(Book.id.in_(ids))
        book_ids = [book.id for book in books]
        for book_id in book_ids:
            project_book = ProjectBook.get_project_book(project_id, book_id)
            if project_book:
                continue
            project_book = ProjectBook(
                project_id=project_id,
                book_id=book_id
            )
            db.session.add(project_book)
        db.session.commit()

    @staticmethod
    def remove_book(project_id, book_id):
        project_book = ProjectBook.get_project_book(project_id, book_id)
        if not project_book:
            raise ApiError('专题不存在或该专题无此书')
        project_book.delete()


    def __repr__(self):
        return '<ProjectBook: %r>' % self.id

