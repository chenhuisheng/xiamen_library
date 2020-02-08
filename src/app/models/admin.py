import bcrypt
from app import db
from plugin.exceptions import ApiError
from ._base import SessionMixin, QueryWithSoftDelete


class Admin(db.Model, SessionMixin):
    query_class = QueryWithSoftDelete

    __tablename__ = 'admin'
    protected_field = ['password']
    ignore_update_fields = ['password']
    schema = {
        'phone': {'type': 'string', 'required': True},
        'name': {'type': 'string', 'required': True},
        'password': {'type': 'string', 'required': True}
    }

    id = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String(128))
    phone = db.Column(db.String(16))
    name = db.Column(db.String(32))
    creater_id = db.Column(db.Integer, nullable=False, default=0)
    is_delete = db.Column(db.Boolean, nullable=False, default=False)

    def __repr__(self):
        return '<Admin: %r>' % self.phone

    @staticmethod
    def generate_password(password):
        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(8, prefix=b'2a'))
        return hashed.decode('utf-8')

    def verify_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))

    @classmethod
    def create(cls, data):
        admin = cls.assemble(data)
        admin.password = cls.generate_password(admin.password)
        if Admin.query.filter_by(phone=admin.phone).first():
            raise ApiError('手机号已存在')
        admin.save()
        return admin

    def update(self, data):
        data_keys = data.keys()
        for field in self.ignore_update_fields:
            if field in data_keys:
                del(data[field])
        if data.get('phone'):
            admin = Admin.query.\
                filter_by(phone=data.get('phone')).\
                filter(Admin.id != self.id).\
                first()
            if admin:
                raise ApiError('手机号已存在')
        self = Admin.assemble(data, self)
        self.save()
        return self
