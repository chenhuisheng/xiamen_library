from app import db
from ._base import SessionMixin


class StatisticLog(db.Model, SessionMixin):
    __tablename__ = 'statistic_log'

    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, nullable=False, default=0)
    video_id = db.Column(db.Integer, nullable=False, default=0)
    project_id = db.Column(db.Integer, nullable=False, default=0)

    @staticmethod
    def add_read_book_record(books):
        records = []
        for book in books:
            record = StatisticLog(
                book_id=book.id,
                project_id=book.project_id
            )
            records.append(record)
        db.session.bulk_save_objects(records)
        db.session.commit()

    @staticmethod
    def add_play_count_record(videos):
        records = []
        for video in videos:
            record = StatisticLog(
                video_id=video.id,
                project_id=video.project_id
            )
            records.append(record)
        db.session.bulk_save_objects(records)
        db.session.commit()

    def __repr__(self):
        return '<StatisticLog: %r>' % self.id



