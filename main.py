from flask import Flask, render_template, jsonify
import datetime as dt
import time
import sqlite3

# conn = sqlite3.connect('testDB')
# c = conn.cursor()
#
# # c.execute("""create table apiTable(timestamp text, algorithm text, range text, time_taken text,prime_count integer )""")
# conn.commit()
# conn.close()

app = Flask(__name__)

num_list = []
temp = []


def read():
    conn = sqlite3.connect('testDB')
    c = conn.cursor()
    k = c.execute("select * from apiTable")
    # c.execute(
    #     """create table apiTable(timestamp text, algorithm text, range text, time_taken text,prime_count integer )""")
    print(k.fetchall())
    conn.commit()
    conn.close()


def insert_data_into_table(time_stamp, algorithm, range_, time_taken, prime_count):
    conn = sqlite3.connect('testDB')
    c = conn.cursor()
    c.execute(f"""insert into apiTable Values('{time_stamp}','{algorithm}','{range_}','{time_taken}',{prime_count})""")
    # c.execute(
    #     """create table apiTable(timestamp text, algorithm text, range text, time_taken text,prime_count integer )""")
    conn.commit()
    conn.close()


def simple_method(num):
    if num == 1:
        return False
    factors = 0

    for i in range(1, num + 1):
        if num % i == 0:
            factors += 1

    if factors == 2:
        return True

    return False


def brut_force(num):
    if num == 1:
        return False

    k = 2
    while k * k <= num:
        if num % k == 0:
            return False
        k += 1
    return True


def sieve_of_erathosthenes(num):
    flag_list = [True for a in range(num + 1)]
    flag_list[0] = False
    flag_list[1] = False
    n = 2
    i = 2
    while n * i <= num:
        while n * i <= num:
            flag_list[n * i] = False
            i += 1
        n += 1
        i = 2
    for i in range(len(flag_list)):
        if flag_list[i] and i in temp:
            num_list.append(i)


@app.route('/simplemethod/<int:from_>/<int:to_>')
def simple_method_api(from_, to_):
    t0 = time.time()
    global num_list
    num_list = []
    a = from_
    b = to_
    for i in range(a, b + 1):
        if simple_method(i):
            num_list.append(i)
    datetime_stamp = dt.datetime.now()
    list_size = len(num_list)

    t1 = time.time()
    time_taken = str(t1 - t0)
    output_dictionary = {"date time stamp": datetime_stamp,
                         "total prime numbers returned": list_size,
                         "range": f"{a} to {b}",
                         "prime numbers": num_list,
                         "time_taken": time_taken}
    insert_data_into_table(str(datetime_stamp), "simple method", f"{a} to {b}", time_taken, list_size)
    read()
    return jsonify(output_dictionary)


@app.route('/brutforce/<from_>/<to_>')
def brutforce_method_api(from_, to_):
    global num_list
    num_list = []
    t0 = time.time()
    a = int(from_)
    b = int(to_)
    for i in range(a, b + 1):
        if brut_force(i):
            num_list.append(i)
    datetime_stamp = dt.datetime.now()
    list_size = len(num_list)
    t1 = time.time()
    time_taken = str(t1 - t0)
    output_dictionary = {"date time stamp": datetime_stamp,
                         "total prime numbers returned": list_size,
                         "range": f"{a} to {b}",
                         "prime numbers": num_list,
                         "time taken": time_taken}
    insert_data_into_table(str(datetime_stamp), "brut force", f"{a} to {b}", time_taken, list_size)
    read()
    return jsonify(output_dictionary)


@app.route('/sieve/<int:from_>/<int:to_>')
def seive_method_api(from_, to_):
    global num_list, temp
    t0 = time.time()
    num_list = []
    temp = []
    a = from_
    b = to_
    for i in range(a, b + 1):
        temp.append(i)
    sieve_of_erathosthenes(to_)
    datetime_stamp = dt.datetime.now()
    list_size = len(num_list)
    t1 = time.time()
    time_taken = str(t1 - t0)
    output_dictionary = {"date time stamp": datetime_stamp,
                         "total prime numbers returned": list_size,
                         "range": f"{a} to {b}",
                         "prime numbers": num_list,
                         "time taken": time_taken}
    insert_data_into_table(str(datetime_stamp), "sieve of erathosthenes", f"{a} to {b}", time_taken, list_size)
    read()
    return jsonify(output_dictionary)


if __name__ == "__main__":
    app.run(debug=True)
