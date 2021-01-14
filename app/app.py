import datetime
from flask import Flask, jsonify, request, render_template, redirect, url_for
from redis import Redis

app = Flask(__name__)

redis = Redis(host='redis', port=6379)


@app.route('/')
def hello():
    return jsonify({'hello': 'world'})


@app.route('/error', methods=['GET'])
def error():
    try:
        ttl = redis.ttl(redis.keys()[0])
    except:
        ttl = "the key is not exist"
    return render_template('error.html', ttl=ttl)


@app.route('/ip_watcher')
def ip_watcher():
    blacklist = set()
    max_visits = 60
    while True:
        addr = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)   # pylint: disable=invalid-name
        now = datetime.datetime.now()
        n = redis.incrby(addr, 1)    # pylint: disable=invalid-name
        redis.expire(addr, 60)
        check_exist = redis.exists(addr)
        if check_exist == 1 and n > max_visits:
            blacklist.add(addr)
            return redirect(url_for('error'))
        else:
            return f"{now}:  saw {addr}, times: {n}, {check_exist}"


@app.route('/keys', methods=['GET'])
def all_visitors():
    try:
        ttl = redis.ttl(redis.keys()[0])
    except:
        ttl = "the key is not exist"
    return f"dbsize: {redis.dbsize()},  keys: {redis.keys()}, time_to_live: {ttl}"


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
