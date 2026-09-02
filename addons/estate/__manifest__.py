{
    'name': "Real Estate (Data Module)",
    'depends': ['base', 'base_import_module'],
    'data': [
        'models/real_estate_property_type.xml',
        'models/real_estate_property.xml',
        'security/ir.model.access.csv',
        'views/real_estate_property_views.xml',
        'views/real_estate_menus.xml',
    ],
}