from app import db
from ._base import SessionMixin, QueryWithSoftDelete


class Picture(db.Model, SessionMixin):
    __tablename__ = 'picture'
    query_class = QueryWithSoftDelete
    search_fields = ['title_like']

    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(400), nullable=False, default='') #图片
    title = db.Column(db.String(64), nullable=False, default='')  # 图片标题
    summary = db.Column(db.Text, nullable=False, default='') #说明
    type = db.Column(db.String(32), nullable=False, default='image') # 图片类型 image / banner
    is_delete = db.Column(db.Boolean, nullable=False, default=False)

    def __repr__(self):
        return '<Picture: %r>' % self.id



