# -*- coding: utf-8 -*-

from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from codemirror2.widgets import CodeMirrorEditor
from mptt.forms import TreeNodeChoiceField
from vvcatalog.models import Product, Category, Brand, Customer
from vvcatalog.conf import CODE_MODE

     
class CustomerForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(CustomerForm, self).__init__(*args, **kwargs)
        self.fields['civility'].label = ''
        return
    
    class Meta:
        model = Customer
        fields = ['civility', 'first_name', 'last_name', 'telephone', 'email', 'address']
        widgets = {'civility': forms.RadioSelect()}

        
class BrandForm(forms.ModelForm):
    class Meta:
        model = Brand
        fields = ['title', 'slug', 'status', 'image', 'editor']
        widgets = {'status': forms.RadioSelect}


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['title', 'slug', 'parent', 'image', 'status', 'editor']
        widgets = {'status': forms.RadioSelect, 'description': CKEditorUploadingWidget(config_name='default')}
        
        
class ProductForm(forms.ModelForm):
    upc = forms.CharField()
    upc.required = False
    category = TreeNodeChoiceField(queryset=Category.objects.all())
        
    class Meta:
        model = Product
        exclude = ['created', 'edited', 'editor']
        description_widget = forms.Textarea(attrs={'style': 'width:100%;'})
        if CODE_MODE is True:
            description_widget = CodeMirrorEditor(options={
                                                             'mode':'htmlmixed',
                                                             'indentWithTabs':'true', 
                                                             'indentUnit' : '4',
                                                             #'lineNumbers':'false',
                                                             'autofocus':'true',
                                                             #'highlightSelectionMatches': '{showToken: /\w/, annotateScrollbar: true}',
                                                             'styleActiveLine': 'true',
                                                             'autoCloseTags': 'true',
                                                             'keyMap':'vim',
                                                             'theme':'blackboard',
                                                             }, 
                                                             modes=['css', 'xml', 'javascript', 'htmlmixed'],
                                                    )
        else:
            description_widget = CKEditorUploadingWidget(config_name='default')
        short_description_widget = forms.Textarea(attrs={'style': 'min-width:100% !important;', 'rows':6, 'cols':80})
        description_widget.label = ""
        widgets = {
                   'status': forms.RadioSelect,
                   'description': description_widget,
                   'short_description' : short_description_widget,
                   'deal_conditions' : description_widget,
                   'deal_description' : description_widget,
                   
                   }
