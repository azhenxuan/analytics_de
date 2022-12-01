from redis import Redis
import mysql.connector

from app import establish_connection, get_query_result
from queries import MOST_OUTDATED_PAGE, TOP_TEN_CATEGORIES_COUNT


redis = Redis(host='redis', port=6379, decode_responses=True)

def precompute_cached_categories_result():
    cxn = establish_connection()
    top_ten_categories = (row[0] for row in get_query_result(cxn, TOP_TEN_CATEGORIES_COUNT))
    for category in top_ten_categories:
        category = category.decode()
        data = get_query_result(cxn, MOST_OUTDATED_PAGE.format(category=category))
        page_id = data[0][0] if len(data) != 0 else None
        redis.set(category, page_id)


if __name__ == "__main__":
    precompute_cached_categories_result()
