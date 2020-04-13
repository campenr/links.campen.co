from flask import redirect, request, url_for, jsonify
from flask_login import current_user
from flask_login import login_required

from sqlalchemy import desc

from app import flask_app
from app.models import User, Link


@flask_app.route('/api/links', methods=['GET'])
@login_required
def get_links():

    # get table sorting preferences from request
    r = request.args

    sort_column = r['column']
    if sort_column == 'long_link':
        sort_column = 'link_name'
    elif sort_column == 'short_link':
        sort_column = 'link_token'
    sort_desc = r['desc'] == 'true'
    page_start = int(r['start'])

    PAGE_COUNT = 10
    if page_start == 0:
        page_number = 1
    else:
        page_number = ( page_start // PAGE_COUNT ) + 1

    query = Link.query
    query = query.filter_by(owner=current_user)

    if sort_desc:
        records = query.order_by(desc(sort_column)).paginate(page=page_number, per_page=PAGE_COUNT, error_out=False)
    else:
        records = query.order_by(sort_column).paginate(page=page_number, per_page=PAGE_COUNT, error_out=False)

    link_records = records.items

    # format links
    formatted_links = []
    for link_record in link_records:

        new_link_record = dict()
        new_link_record['long_link'] = dict()

        # format record values
        new_link_record['long_link']['name'] = link_record.link_name
        new_link_record['long_link']['url'] = link_record.link_url
        new_link_record['created'] = Link.format_date(link_record.created)
        new_link_record['short_link'] = link_record.link_token

        # also need to add dummy elements for the buttons and send the link_token
        new_link_record['copy'] = link_record.link_token
        new_link_record['delete'] = link_record.link_token

        formatted_links.append(new_link_record)

    return jsonify({'data': formatted_links, 'recordsTotal': records.total, 'recordsFiltered': records.total})


@flask_app.route('/api/link/delete', methods=['POST'])
@login_required
def delete_link():
    """Delete supplied link from the database."""

    try:
        link_token = request.form['link_token']
        link_data = Link.delete_link(link_token=link_token)
    except Exception as e:
        print(e)

    return redirect(url_for('index'))

# TODO: add api for adding a link to make full use of the the ajax calls
# TODO: add api for deleting a link to make full use of the the ajax calls
