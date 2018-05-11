from flask import Flask
from graphene import ObjectType, String, Schema, List
from flask_graphql import GraphQLView

list = ['newbee', 'liquid']

class Query(ObjectType):
    teams = List(String)
    def resolve_teams(self, info):
        return list

view_func = GraphQLView.as_view('graphql', schema=Schema(query=Query), graphiql=True)

app = Flask(__name__)
app.add_url_rule('/', view_func=view_func)

if __name__ == '__main__':
    app.run()

