# -*- coding: utf-8 -*-
# from odoo import http


# class ProductCatalog(http.Controller):
#     @http.route('/product_catalog/product_catalog', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/product_catalog/product_catalog/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('product_catalog.listing', {
#             'root': '/product_catalog/product_catalog',
#             'objects': http.request.env['product_catalog.product_catalog'].search([]),
#         })

#     @http.route('/product_catalog/product_catalog/objects/<model("product_catalog.product_catalog"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('product_catalog.object', {
#             'object': obj
#         })
