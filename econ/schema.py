import graphene
from graphene_django import DjangoObjectType,DjangoConnectionField
from graphene_django.debug import DjangoDebug
from graphene.types.generic import GenericScalar

from django.db.models import Prefetch
from models import (
    Specific,
    SpecificDetail,
    ProductSpecDetail,
    Product,
    ProductImage,
    ProductInfo,
    ProductOption,
    Cagetory,
    Brand,
    Agency,
)


def get_field_names(info):

    from graphql.language.ast import FragmentSpread
    fragments = info.fragments

    def iterate_field_names(prefix, field):
        name = field.name.value

        if isinstance(field, FragmentSpread):
            results = []
            new_prefix = prefix
            sub_selection = fragments[field.name.value].selection_set.selections
        else:
            results = [prefix + name]
            new_prefix = prefix + name + "."
            sub_selection = field.selection_set.selections if field.selection_set else []

        for sub_field in sub_selection:
            results += iterate_field_names(new_prefix, sub_field)

        return results

    results = iterate_field_names('', info.field_asts[0])
    return results

def prefetch_product(query,fields,prefix):

    prefetch_related_args = []
    select_related_args = []
    if ('%s.images' % prefix) in fields:
        prefetch_related_args += ['productimage_set']

    if ('%s.productspecdetailSet' % prefix) in fields:
        prefetch_related_args += [
            'productspecdetail_set__spec__detail_field'
        ]
    if ('%s.productinfo' % prefix) in fields:
        select_related_args += ['productinfo']

    if ('%s.productBranch' % prefix) in fields:
        select_related_args += ['product_branch']

    if ('%s.productAgency' % prefix) in fields:
        select_related_args += ['product_agency']
        
    if ('%s.productCagetory' % prefix) in fields:
        select_related_args += ['product_cagetory']

    productQuery = query

    if len(select_related_args)> 0:
        productQuery = productQuery.select_related(*select_related_args)
    if len(prefetch_related_args) > 0:
        productQuery = productQuery.prefetch_related(*prefetch_related_args)
        
    return productQuery


class ProductSet:
    product_set = graphene.List(lambda: ProductsView)

    def resolve_product_set(self, args, context, info):
        return prefetch_product(
            self.product_set,
            get_field_names(info),
            'productSet'
        )

class AgencyView(DjangoObjectType,ProductSet):
    class Meta:
        model = Agency

class BrandView(DjangoObjectType,ProductSet):
    class Meta:
        model = Brand

class ProductSpecDetailView(DjangoObjectType):
    class Meta:
        model = ProductSpecDetail

    spec = graphene.Field(graphene.String)
    value = graphene.Field(graphene.String)

    def resolve_spec(self, args, context, info):
        return self.spec.detail_field

    def resolve_value(self, args, context, info):
        return self.spec.detail_value
    


class ProductsView(DjangoObjectType):
    debug = graphene.Field(DjangoDebug, name='__debug')
    
    class Meta:
        model = Product

    images = graphene.List(graphene.String)

    def resolve_images(self, args, context, info):
        return self.images()


class ProductImagesView(DjangoObjectType):
    class Meta:
        model = ProductImage

    url = graphene.String()

    def resolve_url(self, args, context, info):
        return self.url()
    

class ProductInfoView(DjangoObjectType):
    class Meta:
        model = ProductInfo


class CagetoryView(DjangoObjectType,ProductSet):
    class Meta:
        model = Cagetory

    paths = graphene.List(lambda: CagetoryView)

    def resolve_paths(self, args, context, info):
        return self.paths()#[(cagetory_name,id,slug) for (cagetory_name,id,slug) in self.paths()]


class Query(graphene.ObjectType):
    product = graphene.Field(ProductsView,id=graphene.Argument(graphene.String),slug=graphene.Argument(graphene.String))

    def resolve_product(root, args, context, info):
        productQuery = prefetch_product(
            Product.objects,
            get_field_names(info),
            'product'
        )
            
        id = args.get('id')
        slug = args.get('slug')

        if id :
            return productQuery.get(id=id)
        elif slug:
            return productQuery.get(slug=slug)
        else:
            return productQuery.none()



schema = graphene.Schema(query=Query)
