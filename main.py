from flask import Flask
from graphene import ObjectType, String, Schema, List, Int, AbstractType, Field, ID, Mutation, InputObjectType, Enum
from flask_graphql import GraphQLView

_id = 10

class BoxType(Enum):
    INBOX = 0
    OUTBOX = 1

class MessageSchema(ObjectType):
    id = ID()
    _from = String()
    _to = String()
    data = String()

class MessageInput(InputObjectType):
    _from = String()
    _to = String()
    data = String()

class UserSchema(ObjectType):
    name = String()
    inbox = List(MessageSchema)
    outbox = List(MessageSchema)
    def resolve_name(self, info):
        return self.name
'''
users_list = [
        UserSchema(
            name="jeova",
            inbox=[
                MessageSchema(id=0, _from="raimac", _to="jeova", data="mac1"),
                MessageSchema(id=1, _from="raimac", _to="jeova", data="mac2"),
                MessageSchema(id=2, _from="raimac", _to="jeova", data="mac3"),
                MessageSchema(id=3, _from="raimac", _to="jeova", data="mac4"),
                ],
            outbox=[
                MessageSchema(id=4, _from="jeova", _to="raimac", data="linux1"),
                MessageSchema(id=5, _from="jeova", _to="raimac", data="linux2"),
                MessageSchema(id=6, _from="jeova", _to="raimac", data="linux3"),
                MessageSchema(id=7, _from="jeova", _to="raimac", data="linux4"),
                ]
            ),
        UserSchema(
            name="raimac",
            inbox=[
                MessageSchema(id=0, _from="jeova", _to="raimac", data="mac1"),
                MessageSchema(id=1, _from="jeova", _to="raimac", data="mac2")
                ],
            outbox=[
                MessageSchema(id=4, _from="raimac", _to="jeova", data="linux1"),
                MessageSchema(id=5, _from="raimac", _to="jeova", data="linux2")
                ]
            )

        ]
'''
users_list = []
class Query(ObjectType):
    user = Field(UserSchema, name=String())
    users = List(UserSchema)

    def resolve_user(self, info, name):
        print("Hey")
        if(users_list == []): return None
        ans = [x  for x in users_list if (x.name == name)]
        return ans[0]

    def resolve_users(self, info):
        return users_list


class SendMessage(Mutation):
    class Arguments:
        pkg_msg = MessageInput()
    Output = List(MessageSchema)
    def mutate(self, info, pkg_msg):
        print("INFO", info)
        inbox = None
        outbox = None
        remet = pkg_msg._from
        dest = pkg_msg._to
        user_remet = [x  for x in users_list if (x.name == remet)][0]
        user_dest = [x  for x in users_list if (x.name == dest)][0]
        msg = pkg_msg

        global _id
        msg.id = _id

        inbox = user_dest.inbox
        outbox = user_remet.outbox

        msg_data = MessageSchema(id=_id, _from=msg._from, _to=msg._to, data=msg.data)
        inbox.append(msg_data)
        outbox.append(msg_data)
        _id = _id+1
        return user_remet.outbox



class AddUser(Mutation):
    class Arguments:
        name=String(required=True)
    Output = UserSchema
    def mutate(self, info, name):
        users_list.append(
                UserSchema(
                    name=name,
                    inbox=[],
                    outbox=[]
                )
        )
        return users_list[len(users_list)-1]



class MyMutations(ObjectType):
    add_user = AddUser.Field()
    send_message = SendMessage.Field()


view_func = GraphQLView.as_view('graphql', schema=Schema(query=Query, mutation=MyMutations), graphiql=True)

app = Flask(__name__)
app.add_url_rule('/', view_func=view_func)

if __name__ == '__main__':
    app.run()

