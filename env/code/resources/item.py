from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel

#CRUD
class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
        type=float,
        required=True,
        help="This field can not be left blank!"
    )
    parser.add_argument('store_id',
        type=int,
        required=True,
        help="Every item needs store id"
    )
    #used for authenication
    @jwt_required()
    #return a single item in the get request
    def get(self,name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {"message":"item not found"},404

    def post(self,name):
        if ItemModel.find_by_name(name):
            return {"message":"'{}' already exist".format(name)},400

        data = Item.parser.parse_args()

        item = ItemModel(name, **data)

        try:
            item.save_to_db()
        except:
            return {"message":"There is an error inserting the item"},500 #internal server error

        return item.json(),201
    #creats a new list without the item search inserted
    def delete(self,name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
            return {"message":"message is deleted"}
        return {"message":"can not find item"},404

    def put(self,name):
        data = Item.parser.parse_args()

        item = ItemModel.find_by_name(name)

        if item is None:
            item = ItemModel(name, **data)
        else:
            item.price = data['price']

        item.save_to_db()

        return item.json()


class ItemList(Resource):
    def get(self):
        return {"items":[item.json()for item in ItemModel.query.all()]} # or list(map(lambda x: x.json(), ItemModel.query.all()))
