""" Test File """

from flask import Flask
from redis import Redis

app = Flask(__name__)
redis_client = Redis(
    host='redis_db',
    port=6379
)


@app.route('/')
def hello():
    """
    Main app route, simply returns a Hello
    """
    count_key = redis_client.get('count')
    count = int(count_key) if count_key else 0
    redis_client.set('count', count+1)

    return f'Hello World {count}'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int('5000'), debug=True)
