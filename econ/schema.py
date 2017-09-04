import graphene
from itertools import chain, groupby
from graphene_django import DjangoObjectType,DjangoConnectionField
from graphene_django.debug import DjangoDebug
from django.contrib.auth.models import User

from django.db.models import Prefetch
from .models import (
    Specific,
    SpecificDetail,
    ProductSpecDetail,
    Product,
    ProductImage,
    ProductInfo,
    ProductOption,
    Cagetory,
    Brand,
)

from haystack.query import SearchQuerySet, SQ


def get_field_names(info):

    from graphql.language.ast import FragmentSpread,InlineFragment
    fragments = info.fragments

    def iterate_field_names(prefix, field):

        if isinstance(field, FragmentSpread):
            name = field.name.value
            results = []
            new_prefix = prefix
            sub_selection = fragments[field.name.value].selection_set.selections
        elif isinstance(field, InlineFragment):
            name = field.type_condition.name.value
            results = [prefix + 'type_' + name]
            new_prefix = prefix + 'type_' + name + "."
            sub_selection = field.selection_set.selections if field.selection_set else []

        else:
            name = field.name.value
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

    if ('%s.productoptionSet.' % prefix) in fields:
        prefetch_related_args += [
            'productoption_set'
        ]

    if ('%s.productoptionSet.productspecdetailSet' % prefix) in fields:
        prefetch_related_args += [
            'productoption_set__productspecdetail_set__spec__detail_field'
        ]

    if ('%s.productinfo' % prefix) in fields:
        select_related_args += ['productinfo']

    if ('%s.productBranch' % prefix) in fields:
        select_related_args += ['branch']

        
    if ('%s.productCagetory' % prefix) in fields:
        select_related_args += ['cagetory']

    print fields

    productQuery = query

    return productQuery.select_related(*select_related_args).prefetch_related(*prefetch_related_args)


class ProductSet:
    product_set = graphene.List(lambda: ProductsView)

    def resolve_product_set(self, args, context, info):
        return prefetch_product(
            self.product_set,
            get_field_names(info),
            'productSet'
        ) 

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
    
class ProductSpecValueView(DjangoObjectType):
    
    class Meta:
        model = SpecificDetail

class ProductSpecView(DjangoObjectType):
    
    class Meta:
        model = Specific



class ProductInfoView(DjangoObjectType):
    class Meta:
        model = ProductInfo

class UserInfoView(DjangoObjectType):
    class Meta:
        model = User

    

class CagetoryView(DjangoObjectType,ProductSet):
    class Meta:
        model = Cagetory

    paths = graphene.List(lambda: CagetoryView)
    specs = graphene.List(lambda: ProductSpecView)

    def resolve_paths(self, args, context, info):
        return self.paths()#[(name,id,slug) for (name,id,slug) in self.paths()]

    def resolve_specs(self, args, context, info):
        return self.specific_set.all()

class SearchResultView(graphene.types.Union):
    class Meta:
        types = [ProductsView, BrandView, CagetoryView]

    searchTypeMapping = {
        'product' : lambda  values, fieldInfo = [], prefix = '' : prefetch_product(
            Product.objects.filter(id__in=values),
            fieldInfo,
            '%s.type_ProductsView' % prefix
        ),
        'cagetory' :lambda  values, fieldInfo = [], prefix = '' : Cagetory.objects.filter(id__in=values),
        'brand' : lambda  values, fieldInfo = [], prefix = '' : Brand.objects.filter(id__in=values),
    }

    @staticmethod
    def process_search_datas(searchqueryset,fieldInfo,prefix):
        datas = searchqueryset.values_list('pk','model_name')[:]
        results = {}
        querySet = []
        for pk,ob_type in datas:
            if not results.has_key(ob_type):
                results[ob_type] = []
            results[ob_type].append(pk)

        for key in results.keys():
            values = results.get(key)
            objectType = SearchResultView.searchTypeMapping.get(key)
            if objectType:
                querySet += [objectType(values,fieldInfo,prefix)]

        return chain(*querySet)


class ProductOptionView(DjangoObjectType):
    class Meta:
        model = ProductOption

class Query(graphene.ObjectType):
    product = graphene.Field(ProductsView,id=graphene.Argument(graphene.String),slug=graphene.Argument(graphene.String))
    products = graphene.List(ProductsView,search=graphene.Argument(graphene.String))

    cagetory = graphene.Field(CagetoryView,id=graphene.Argument(graphene.String),slug=graphene.Argument(graphene.String))
    cagetories = graphene.List(CagetoryView,search=graphene.Argument(graphene.String))


    search = graphene.List(SearchResultView,search=graphene.Argument(graphene.String))
    fuzysearch = graphene.List(SearchResultView,search=graphene.Argument(graphene.String))
    autocomplete = graphene.List(graphene.String,search=graphene.Argument(graphene.String))

    profile = graphene.Field(UserInfoView)

    def resolve_profile(root, args, context, info):
        return context.user
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

    def resolve_products(root, args, context, info):
        productQuery = None

        search = args.get('search')

        if search:
            ids = SearchQuerySet().models(Product).filter(content=search).values_list('pk',flat=True)[:]
            productQuery = Product.objects.filter(id__in=ids)
        else :
            productQuery = Product.objects.all()

        return prefetch_product(
            productQuery,
            get_field_names(info),
            'products'
        )

    def resolve_cagetory(root, args, context, info):
        id = args.get('id')
        slug = args.get('slug')

        if id :
            return Cagetory.objects.get(id=id)
        elif slug:
            return Cagetory.objects.get(slug=slug)
        else:
            return Cagetory.objects.none()

    def resolve_cagetories(root, args, context, info):
        search = args.get('search')
        if search :
            ids = SearchQuerySet().models(Cagetory).filter(content=search).values_list('pk',flat=True)[:]
            return Cagetory.objects.filter(id__in=ids)
        else:
            return Cagetory.objects.all()

    def resolve_search(root,args,context,info):
        fieldInfo = get_field_names(info)
        search = args.get('search')
        if search :
            # datas = SearchQuerySet().filter(content=search)
            return SearchResultView.process_search_datas(
                SearchQuerySet().filter(content=search),
                fieldInfo,
                'search'
            )
        else:
            return []

    def resolve_fuzysearch(root,args,context,info):
        fieldInfo = get_field_names(info)
        search = args.get('search')
        if search :
            # datas = SearchQuerySet().filter(content=search)
            return SearchResultView.process_search_datas(
                SearchQuerySet().autocomplete(title=search),
                fieldInfo,
                'fuzysearch',
            )
        else:
            return []
    
    def resolve_autocomplete(root,args,context,info):
        search = args.get('search')
        sqs = SearchQuerySet().filter(
            (SQ(tags=search) | SQ(title=search))
        ).values_list('title',flat=True) [:5]
        return sqs

schema = graphene.Schema(query=Query)
