from flask import Flask
from flask_graphql import GraphQLView
from schema import schema
from mongoengine import connect

connect(
    host=
    'mongodb://192.168.50.10:7001,192.168.50.11:7002,192.168.50.12:7003/compras?replicaSet=bdcluster0',
    alias='default')

app = Flask(__name__)
app.debug = True

app.add_url_rule(
    '/productos',
    view_func=GraphQLView.as_view('graphql', schema=schema, graphiql=True)
)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
