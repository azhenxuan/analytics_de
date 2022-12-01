from flask import Flask
from redis import Redis
import mysql.connector

from queries import MOST_OUTDATED_PAGE

app = Flask(__name__)
redis = Redis(host='redis', port=6379, decode_responses=True)

def establish_connection():
    connection = mysql.connector.connect(
        user='root',
        host='db',
        password='mydbpwd',
        database='newdb',
    )
    return connection

def get_query_result(cxn, query_string):
    cursor = cxn.cursor()
    cursor.execute(query_string)
    data = cursor.fetchall()
    return data

@app.route("/<query_string>", methods=["GET"])
def get_result_from_arbitrary_query(query_string):
    cxn = establish_connection()
    return get_query_result(cxn, query_string)

@app.route("/outdated_page/<category>", methods=["GET"])
def get_most_outdated_page(category):
    page_id = redis.get(category)
    if page_id:
        return page_id
    else:
        cxn = establish_connection()
        return get_query_result(cxn, MOST_OUTDATED_PAGE)


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
