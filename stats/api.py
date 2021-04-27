from datetime import datetime

from flask import Blueprint, jsonify, request

from stats import BadRequest
from stats.db import db
from stats.models import StatsSession, Numbers
from stats.welford import calculate_stats, update


class RequestPayload:
    def __init__(self, the_request):
        self._json_data = the_request.get_json()

        if self._json_data is None:
            raise BadRequest('Missing JSON payload')

        if not isinstance(self._json_data, dict):
            raise BadRequest(f'Expected dict in JSON payload, got {type(self._json_data)}')

    def get_user_name(self) -> str:
        try:
            user_name = self._json_data['userName']
        except KeyError:
            raise BadRequest('Missing userName field')

        if not isinstance(user_name, str):
            raise BadRequest(f'Expected userName of type string, got {type(user_name)}')

        return user_name

    def get_number(self) -> float:
        try:
            number = self._json_data['number']
        except KeyError:
            raise BadRequest('Missing number field')

        try:
            number = float(number)
        except TypeError:
            raise BadRequest('Invalid number')

        return number


bp = Blueprint('api', __name__, url_prefix='/api')


@bp.route('/stats')
def get_stats():
    active_session = StatsSession.query.filter(StatsSession.active).first()
    if active_session:
        stats = calculate_stats(active_session.count,
                                active_session.mean,
                                active_session.m2)
    else:
        stats = {}

    return jsonify(stats)


@bp.route('/add', methods=('POST',))
def add():
    request_payload = RequestPayload(request)
    user_name = request_payload.get_user_name()
    number = request_payload.get_number()

    now = datetime.utcnow()

    # We're doing a read-modify-write here so use FOR UPDATE
    #
    # TODO Should be using serializable isolation level here too
    # as we have chance of a write skew (if two requests try to
    # create a new active record at the same time)
    active_session = db.session.query(StatsSession).filter(
        StatsSession.active).populate_existing().with_for_update().first()

    if not active_session:
        # Set initial values for the algorithm
        active_session = StatsSession(created_at=now,
                                      created_by=user_name,
                                      active=True,
                                      mean=0.0,
                                      m2=0.0,
                                      count=0)
        db.session.add(active_session)

    new_count, new_mean, new_m2 = update(active_session.count,
                                         active_session.mean,
                                         active_session.m2,
                                         number)
    active_session.count = new_count
    active_session.mean = new_mean
    active_session.m2 = new_m2

    # Record the addition of this number by this user
    number_record = Numbers(stats_session=active_session,
                            added_at=now,
                            added_by=user_name,
                            value=number)
    db.session.add(number_record)
    db.session.commit()

    stats = calculate_stats(new_count, new_mean, new_m2)
    return jsonify(stats)


@bp.route('/reset', methods=('PUT',))
def reset():
    request_payload = RequestPayload(request)
    user_name = request_payload.get_user_name()

    # We're doing a read-modify-write here so use FOR UPDATE
    active_session = db.session.query(StatsSession).filter(
        StatsSession.active).populate_existing().with_for_update().first()

    if active_session:
        active_session.active = False
        active_session.revoked_at = datetime.utcnow()
        active_session.revoked_by = user_name
        db.session.commit()

    return jsonify({})
