from app import db
from ._base import SessionMixin, QueryWithSoftDelete

class Book(db.Model, SessionMixin):
    __tablename__ = 'book'
    query_class = QueryWithSoftDelete
    search_fields = ['title_like', 'author_like', 'source_like']

    id = db.Column(db.Integer, primary_key=True)  # 图书id
    pub_date = db.Column(db.Date, nullable=False, default='1970-01-01')  # 出版日期
    author = db.Column(db.String(255), nullable=False, default='')  # 作者
    title = db.Column(db.String(128), nullable=False, default='')  # 图书标题
    isbn = db.Column(db.String(32), nullable=False, default='')
    publisher = db.Column(db.String(64), nullable=False, default='')  # 出版社
    image = db.Column(db.String(400), nullable=False, default='')  # 图书封面
    pages = db.Column(db.Integer, nullable=False, default=0)  # 页数
    catalog = db.Column(db.Text, nullable=False, default='')  # 目录
    catalog_json = db.Column(db.JsonBlob, nullable=False, default=[])  # 解析目录
    summary = db.Column(db.Text, nullable=False, default='')  # 摘要
    file_path = db.Column(db.String(255), nullable=False, default='')  # 文件路径
    file_type = db.Column(db.String(255), nullable=False, default='')  # 文件类型
    file_size = db.Column(db.Integer, nullable=False, default=0)  # 文件大小
    source = db.Column(db.String(32), nullable=False, default='')  # 来源
    edition = db.Column(db.String(32), nullable=False, default='')  # 版次
    book_type = db.Column(db.String(32), nullable=False, default='book')  # 书本类型 book / magazine / paper
    read_count = db.Column(db.Integer, nullable=False, default=0)  # 阅读次数
    opf_path = db.Column(db.String(255), nullable=False, default='')
    is_delete = db.Column(db.Boolean, nullable=False, default=False)

    def __repr__(self):
        return '<Book: %r>' % self.title