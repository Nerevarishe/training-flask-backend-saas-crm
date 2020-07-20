from flask import request, jsonify
from . import bp
from .utils import filter_period
from app.models import Deal
from datetime import datetime


def convert_to_date(data: str) -> datetime:
    """
    Convert dd/mm/yyyy to datetime object
    """

    return datetime.strptime(data, '%d/%m/%Y')


@bp.route('/', methods=['GET'])
def get_all_deals():
    deals = Deal.objects()
    return jsonify(deals)


@bp.route('/chart_data', methods=['GET'])
def get_chart_data():
    period = request.args.get('period', default='monthly', type=str)
    # deals = Deal.objects.aggregate({
    deals = filter_period(period)
    deals = deals.aggregate({
        # Sort by deal date ASC
        '$sort': {
            'deal_date': 1
        }
    },
        # Group by deal date, converted to timestamp, and count documents that have same date
        {
            '$group': {
                '_id': {
                    '$toLong': '$deal_date'
                },
                'count': {
                    '$sum': 1
                }
            },
        },
        # Sort all by deal date
        {
            '$sort': {
                '_id': 1
            }
        })
    deals = list(deals)
    return jsonify(deals)


@bp.route('/add_in_bulk', methods=['POST'])
def add_in_bulk():
    if request.is_json:
        deals = request.get_json()
        object_counter = 0

        for deal in deals:
            new_deal = Deal()
            new_deal.deal_date = convert_to_date(deal["deal_date"])
            new_deal.amount = deal["amount"]
            new_deal.client = deal["client"]
            new_deal.save()
            object_counter += 1

        return {'msg': 'OK', 'saved_objects': object_counter}, 201
    return {'msg': 'Bad request'}, 400
