# -*- coding: utf-8 -*-
# from odoo import http


# class Jetoil(http.Controller):
#     @http.route('/jetoil/jetoil/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/jetoil/jetoil/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('jetoil.listing', {
#             'root': '/jetoil/jetoil',
#             'objects': http.request.env['jetoil.jetoil'].search([]),
#         })

#     @http.route('/jetoil/jetoil/objects/<model("jetoil.jetoil"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('jetoil.object', {
#             'object': obj
#         })
