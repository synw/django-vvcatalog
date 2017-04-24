# Django VVcatalog

Vue.js product catalog

## Install

Install [Django Vite Vue](https://github.com/synw/django-vitevue) then:

  ```bash
pip install graphene graphene_django django-filter django-braces
pip install git+https://github.com/synw/django-graphql-utils.git
pip install git+https://github.com/synw/django-vvcatalog.git
  ```

Make a `schema.py` file in the directory where settings.py is with this content:

  ```python
import graphene
from graphene_django.debug import DjangoDebug
from vvcatalog import schema


class Query(schema.Query, graphene.ObjectType):
    debug = graphene.Field(DjangoDebug, name='__debug')


schema = graphene.Schema(query=Query)
  ```
 
Add to INSTALLED_APPS:

  ```python
"graphene",
"graphene_django",
"graphql_utils",
"vv",
"vvcatalog",
  ```
  
In `settings.py`:

  ```python
GRAPHENE = {
    'SCHEMA': 'myprojectname.schema.schema'
}
  ```
  
Where `myprojectname` is the name of the directory that contains `settings.py`
   
Urls:

  ```python
from graphql_utils.views import TGraphQLView

urlpatterns = [
	# ...
	url(r'^graphql', TGraphQLView.as_view()),
	url(r'^catalog/',include('vvcatalog.urls')),
]
  ```
  
Javascript libs to include:

  ```django
<script type="text/javascript" src="{% static 'js/vue.min.js' %}"></script>
<script type="text/javascript" src="{% static 'js/page.js' %}"></script>
<script type="text/javascript" src="{% static 'js/axios.min.js' %}"></script>
<script type="text/javascript" src="{% static 'js/hammer.min.js' %}"></script>
  ```
