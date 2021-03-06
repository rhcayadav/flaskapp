from datetime import datetime

from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login
from flask_login import UserMixin
from flask import url_for

#cli API
class PaginatedAPIMixin(object):
    @staticmethod
    def to_collection_dict(query, page, per_page, endpoint, **kwargs):
        resources = query.paginate(page, per_page, False)
        data = {
            'items': [item.to_dict() for item in resources.items],
            '_meta': {
                'page': page,
                'per_page': per_page,
                'total_pages': resources.pages,
                'total_items': resources.total
            },
            '_links': {
                'self': url_for(endpoint, page=page, per_page=per_page,
                                **kwargs),
                'next': url_for(endpoint, page=page + 1, per_page=per_page,
                                **kwargs) if resources.has_next else None,
                'prev': url_for(endpoint, page=page - 1, per_page=per_page,
                                **kwargs) if resources.has_prev else None
            }
        }
        return data

#GUI DB Model for User
class User(PaginatedAPIMixin, UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
#    posts = db.relationship('Post', backref='author', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)

#cli API
    def from_dict(self, data, new_user=False):
        for field in ['username', 'email']:
            if field in data:
                setattr(self, field, data[field])
        if new_user and 'password' in data:
            self.set_password(data['password'])

    def to_dict(self, include_email=False):
        data = {
            'id': self.id,
            'username': self.username,
            # 'post_count': self.clusters.count(),
            '_links': {
                'self': url_for('api.get_user', id=self.id)
                # 'followers': url_for('api.get_', id=self.id),
            }
        }
        if include_email:
            data['email'] = self.email
        return data


#quit()

#GUI DB Model for Cluster
class Cluster(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cluster_name = db.Column(db.String(50), index=True, unique=True)
    description = db.Column(db.String(200))
    cluster_type = db.Column(db.String(20))
    cluster_os = db.Column(db.String(20))
    node_count = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Cluster {}>'.format(self.cluster_name)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))
