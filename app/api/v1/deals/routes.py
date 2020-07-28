from flask import request, jsonify
from . import bp
from .utils import filter_period


@bp.route('/chart_data', methods=['GET'])
def get_chart_data():
    period = request.args.get('period', default='monthly', type=str)
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
