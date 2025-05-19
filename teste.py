from flask import Flask
from flask_restful import reqparse, abort, Api, Resource

app = Flask(__name__)
api = Api(app)

app.config['JSON_AS_ASCII'] = False
app.config['RESTFUL_JSON'] = {  
    'ensure_ascii': False,
    'indent': 4,
    'sort_keys': False
}


TODOS = {
    'todo1': {'task': 'estudar Flask'},
    'todo2': {'task': 'beber água'},
    'todo3': {'task': 'dormir cedo'},
}

# função pra dar erro se a tarefa não existir
def abort_if_todo_doesnt_exist(todo_id):
    if todo_id not in TODOS:
        abort(404, message=f"Tarefa {todo_id} não existe")

# Cria o parser para ler dados do POST/PUT
parser = reqparse.RequestParser()
parser.add_argument('task')  # nome do campo que a gente envia pelo formulário

# Classe que lida com /todos/todo1, /todos/todo2, etc
class Todo(Resource):
    def get(self, todo_id):
        abort_if_todo_doesnt_exist(todo_id)
        return TODOS[todo_id]

    def delete(self, todo_id):
        abort_if_todo_doesnt_exist(todo_id)
        del TODOS[todo_id]
        return '', 204

    def put(self, todo_id):
        args = parser.parse_args()
        task = {'task': args['task']}
        TODOS[todo_id] = task
        return task, 201

# Classe que lida com /todos (lista geral)
class TodoList(Resource):
    def get(self):
        return TODOS

    def post(self):
        args = parser.parse_args()
        print(args)  # <- isso aqui
        new_id = f'todo{len(TODOS) + 1}'
        TODOS[new_id] = {'task': args['task']}
        return TODOS[new_id], 201


# Roteamento das URLs
api.add_resource(TodoList, '/todos')
api.add_resource(Todo, '/todos/<string:todo_id>')

if __name__ == '__main__':
    app.run(debug=True)

