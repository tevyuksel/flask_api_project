import psycopg2
from flask import Flask, request
from psycopg2 import connect

app = Flask(__name__)
conn = psycopg2.connect(database="flask_api", user="postgres", password="", host="localhost", port="5432")

# For Create Table
# cur = conn.cursor()
# cur.execute(
#     '''CREATE TABLE IF NOT EXISTS cities (id serial
#     PRIMARY KEY, name varchar(100), plate varchar(2), description varchar(250));''')
# conn.commit()
# cur.close()
# conn.close()


def perform_insert_operation(table_name, columns, values):
    with connect(database="flask_api", user="postgres", password="", host="localhost", port="5432") as conn:
        with conn.cursor() as cur:
            query = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({', '.join(['%s' for _ in values])})"
            cur.execute(query, values)
            conn.commit()


def perform_select_operation(table_name, columns=None, where_clause=None):
    with connect(database="flask_api", user="postgres", password="", host="localhost", port="5432") as conn:
        with conn.cursor() as cur:
            # Sorgu için temel SELECT ifadesini oluştur
            query = f"SELECT {', '.join(columns) if columns else '*'} FROM {table_name}"

            # WHERE koşulu varsa ekleyin
            if where_clause:
                query += f" WHERE {where_clause}"

            cur.execute(query)
            result = cur.fetchall()

            return result


def perform_delete_operation(table_name, where_clause=None):
    with connect(database="flask_api", user="postgres", password="", host="localhost", port="5432") as conn:
        with conn.cursor() as cur:
            query = f"DELETE FROM {table_name}"

            if where_clause:
                query += f" WHERE {where_clause}"

            cur.execute(query)
            conn.commit()
            if cur.rowcount > 0:
                return True
            else:
                return False


@app.route('/')
def index():  # put application's code here
    return (
            "<h3>Flask ile Web API geliştirme</h3>"
            "<p><b>user işlemleri için</b></p>"
            "<p><a href=http://127.0.0.1:5000/user>http://127.0.0.1:5000/user</a></p>"       
            "<p><b>city işlemleri için</b></p>"
            "<p><a href=http://127.0.0.1:5000/city>http://127.0.0.1:5000/city</a></p>"
            "<p></br><b>Lütfen test ederken POSTMAN vb. bir araç kullanın!</b></p>"
            )


# User API Operations
@app.route('/user')
def user():  # put application's code here
    return (
            "<p><b>Sorgu Parametreleri Kullanımı ile NewUser:</b></p><p>http://127.0.0.1:5000/user endpointine name ve password değerlerini aşağıdaki şekilde yazıp yeni bir user oluşturmak için POST isteği gönderebilirsiniz; </p>"
            "<p>http://127.0.0.1:5000/user?name=Ali&password=123</p>"
            "<p><b>URL Parametreleri Kullanımı ile NewUser:</b></p> <p>http://127.0.0.1:5000/user/name/password endpointine name ve password değerlerini aşağıdaki şekilde yazıp yeni bir user oluşturmak için POST isteği gönderebilirsiniz; </p>"
            "<p>http://127.0.0.1:5000/user/Ali/123</p>"
            "<p><b>GetAll Kullanımı</b></p>"
            "<p>http://127.0.0.1:5000/user/get_all endpointine GET isteği atarak tüm user'ları json formatında listeleyebilirsiniz.</p>"
            "<p><b>GetUserById Kullanımı</b></p>"
            "<p>http://127.0.0.1:5000/user/get_user_by_id/id endpointine tüm bilgilerini görmek istediğiniz user'ın id değerini aşağıdaki şekilde yazıp GET isteği gönderebilirsiniz;</p>"
            "<p>http://127.0.0.1:5000/user/get_user_by_id/1</p>"
            "<p><b>GetUserNameById Kullanımı</b></p>"
            "<p>http://127.0.0.1:5000/user/get_user_name_by_id/id endpointine name değerini görmek istediğiniz user'ın id değerini aşağıdaki şekilde yazıp GET isteği gönderebilirsiniz;</p>"
            "<p>http://127.0.0.1:5000/user/get_user_name_by_id/1</p>"
            "<p><b>DeleteUserById Kullanımı</b></p>"
            "<p>http://127.0.0.1:5000/user/delete_user_by_id/id endpointine silmek istediğiniz user'ın id değerini aşağıdaki şekilde yazıp DELETE isteği gönderebilirsiniz;</p>"
            "<p>http://127.0.0.1:5000/user/delete_user_by_id/1</p>"
            )


@app.route('/user/get_all')
def get_all_users():
    table_name = "users"
    # columns_to_select = ['column1', 'column2', 'column3']
    # where_clause = "column1 = 'value'"
    results = perform_select_operation(table_name=table_name)
    return results


@app.route('/user/get_user_by_id/<int:user_id>')
def get_user_by_id(user_id):
    table_name = "users"
    print(user_id)
    # columns_to_select = ['column1', 'column2', 'column3']
    where_clause = f"id = {user_id}"
    results = perform_select_operation(table_name=table_name, where_clause=where_clause)
    return results


@app.route('/user/get_user_name_by_id/<int:user_id>')
def get_user_name_by_id(user_id):
    table_name = "users"
    print(user_id)
    columns_to_select = ['name']
    where_clause = f"id = {user_id}"
    results = perform_select_operation(table_name=table_name, columns=columns_to_select, where_clause=where_clause)
    return results


@app.route('/user/delete_user_by_id/<int:user_id>', methods=['DELETE'])
def delete_user_by_id(user_id):
    if request.method == 'DELETE':
        print(user_id)

        table_name = "users"
        where_clause = f"id = {user_id}"

        if perform_delete_operation(table_name=table_name, where_clause=where_clause):
            return f"User with ID {user_id} deleted successfully."
        else:
            return f"User with ID {user_id} not found or deletion failed."
    else:
        return "Invalid request method. Use DELETE."


# With Query Parameters
@app.route('/user', methods=['POST'])
def post_user_query():
    if request.method == 'POST':
        name = request.args.get('name')
        password = request.args.get('password')
        table_name = "users"
        columns = ['name', 'password']
        values = [name, password]
        perform_insert_operation(table_name, columns, values)
        return f"Name: {name}, Password: {password}"
    else:
        return "Invalid request method. Use POST."


# With URL Parameters
@app.route('/user/<string:name>/<string:password>', methods=['POST'])
def post_user_url(name, password):
    if request.method == 'POST':
        print(name)
        print(password)
        table_name = "users"
        columns = ['name', 'password']
        values = [name, password]
        perform_insert_operation(table_name, columns, values)
        return f"Name: {name}, Password: {password}"
    else:
        return "Invalid request method. Use POST."


# City API Operations
@app.route('/city')
def city():  # put application's code here
    return (
            "<p><b>GetAll Kullanımı</b></p>"
            "<p>http://127.0.0.1:5000/city/get_all endpointine GET isteği atarak tüm city'leri json formatında listeleyebilirsiniz.</p>"
            "<p><b>GetCityByPlate Kullanımı</b></p>"
            "<p>http://127.0.0.1:5000/city/get_city_by_plate/plate endpointine tüm bilgilerini görmek istediğiniz city'nin plate değerini aşağıdaki şekilde yazıp GET isteği gönderebilirsiniz;</p>"
            "<p>http://127.0.0.1:5000/city/get_city_by_plate/24</p>"
            "<p><b>GetCityNameByPlate Kullanımı</b></p>"
            "<p>http://127.0.0.1:5000/city/get_city_name_by_plate/plate endpointine name değerini görmek istediğiniz city'nin plate değerini aşağıdaki şekilde yazıp GET isteği gönderebilirsiniz;</p>"
            "<p>http://127.0.0.1:5000/city/get_city_name_by_plate/24</p>"
            "<p><b>DeleteCityByPlate Kullanımı</b></p>"
            "<p>http://127.0.0.1:5000/city/delete_city_by_plate/plate endpointine silmek istediğiniz city'nin plate değerini aşağıdaki şekilde yazıp DELETE isteği gönderebilirsiniz;</p>"
            "<p>http://127.0.0.1:5000/city/delete_city_by_plate/24</p>"
            )


@app.route('/city/get_all')
def get_all_cities():
    table_name = "cities"
    # columns_to_select = ['column1', 'column2', 'column3']
    # where_clause = "column1 = 'value'"
    results = perform_select_operation(table_name=table_name)
    return results


@app.route('/city/get_city_by_plate/<string:plate>')
def get_city_by_plate(plate):
    table_name = "cities"
    print(plate)
    # columns_to_select = ['column1', 'column2', 'column3']
    where_clause = f"plate = '{plate}'"
    results = perform_select_operation(table_name=table_name, where_clause=where_clause)
    return results


@app.route('/city/get_city_name_by_plate/<string:plate>')
def get_city_name_by_plate(plate):
    table_name = "cities"
    print(plate)
    columns_to_select = ['name']
    where_clause = f"plate = '{plate}'"
    results = perform_select_operation(table_name=table_name, columns=columns_to_select, where_clause=where_clause)
    return results


@app.route('/city/delete_city_by_plate/<string:plate>', methods=['DELETE'])
def delete_city_by_plate(plate):
    if request.method == 'DELETE':
        print(plate)
        table_name = "cities"
        where_clause = f"id = {plate}"
        if perform_delete_operation(table_name=table_name, where_clause=where_clause):
            return f"User with ID {plate} deleted successfully."
        else:
            return f"User with ID {plate} not found or deletion failed."
    else:
        return "Invalid request method. Use DELETE."


if __name__ == '__main__':
    app.run()