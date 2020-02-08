from app import db
from ._base import SessionMixin, QueryWithSoftDelete


class Video(db.Model, SessionMixin):
    __tablename__ = 'video'
    query_class = QueryWithSoftDelete
    search_fields = ['title_like']

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), nullable=False, default='')  # 标题
    author = db.Column(db.String(64), nullable=False, default='')  # 作者
    image = db.Column(db.String(400), nullable=False, default='')   # 视频封面
    file_type = db.Column(db.String(16), nullable=False, default='')  # 文件类型
    file_path = db.Column(db.String(255), nullable=False, default='')  # 文件路径
    file_size = db.Column(db.Integer, nullable=False, default=0)  # 文件大小
    play_count = db.Column(db.Integer, nullable=False, default=0)  # 播放次数
    is_delete = db.Column(db.Boolean, nullable=False, default=False)

    def __repr__(self):
        return '<Video: %r>' % self.id



