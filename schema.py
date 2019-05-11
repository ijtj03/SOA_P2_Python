import graphene
from bson import ObjectId
from graphene.relay import Node
from graphene_mongo import MongoengineConnectionField, MongoengineObjectType
from models import Catalog as CatalogModel


class Product(MongoengineObjectType):

    class Meta:
        model = CatalogModel


class CreateProduct(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        description = graphene.String(required=True)
        stock = graphene.Int(required=True)

    model = graphene.Field(Product)

    def mutate(self, info, name, description, stock):
        model = Product._meta.model(
            name=name, description=description, stock=stock)
        model.save(force_insert=True)
        return CreateProduct(model=model)


class DeleteProduct(graphene.Mutation):
    class Arguments:
        id = graphene.String(required=True)

    ok = graphene.Boolean()

    def mutate(self, info, id):
        model = CatalogModel.objects(id=ObjectId(id))
        ok = bool(model.delete())
        return DeleteProduct(ok=ok)


class UpdateProduct(graphene.Mutation):
    class Arguments:
        id = graphene.String(required=True)
        name = graphene.String()
        description = graphene.String()
        stock = graphene.Int()

    ok = graphene.Boolean()

    def mutate(self, info, id, name=None, description=None, stock=None):
        ok = True
        model = CatalogModel.objects(id=ObjectId(id))
        if name:
            model.update_one(name=name)
            ok = ok or bool(model.update_one(name=name))
        if stock:
            model.update_one(stock=stock)
            ok = ok or bool(model.update_one(stock=stock))
        if description:
            model.update_one(description=description)
            ok = ok or bool(model.update_one(description=description))

        return DeleteProduct(ok=ok)


class Mutations(graphene.ObjectType):
    create_product = CreateProduct.Field()
    delete_product = DeleteProduct.Field()
    update_product = UpdateProduct.Field()


class Query(graphene.ObjectType):
    products = graphene.List(Product)
    product_by_id = graphene.Field(Product, id=graphene.String(required=True))

    def resolve_products(self, info):
        return list(CatalogModel.objects.all())

    def resolve_product_by_id(self, info, id):
        p = None
        for product in list(CatalogModel.objects.all()):
            if str(product.id) == str(id):
                p = product
                break
        return p


schema = graphene.Schema(query=Query, mutation=Mutations)
