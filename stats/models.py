from stats.db import db


class StatsSession(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    created_at = db.Column(db.DateTime, nullable=False)
    created_by = db.Column(db.String(80), nullable=False)
    active = db.Column(db.Boolean, nullable=False)
    revoked_at = db.Column(db.DateTime)
    revoked_by = db.Column(db.String(80))

    mean = db.Column(db.Float, nullable=False)
    m2 = db.Column(db.Float, nullable=False)
    count = db.Column(db.Integer, nullable=False)

    numbers = db.relationship('Numbers', backref='stats_session', lazy=True)


class Numbers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    stats_session_id = db.Column(db.Integer, db.ForeignKey('stats_session.id'), nullable=False)

    added_at = db.Column(db.DateTime, nullable=False)
    added_by = db.Column(db.String(80), nullable=False)
    value = db.Column(db.Float, nullable=False)
