# -*- encoding: utf-8 -*-
###############################################################################
#
#   account_fiscal_position_rule_sale for OpenERP
#   Copyright (C) 2009-TODAY Akretion <http://www.akretion.com>
#     @author Sébastien BEAU <sebastien.beau@akretion.com>
#     @author Renato Lima <renato.lima@akretion.com>
#     @author Raphaël Valyi <raphael.valyi@akretion.com>
#   Copyright 2012 Camptocamp SA
#     @author: Guewen Baconnier
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU Affero General Public License as
#   published by the Free Software Foundation, either version 3 of the
#   License, or (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU Affero General Public License for more details.
#
#   You should have received a copy of the GNU Affero General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################

from openerp.osv import fields, osv


class sale_order(osv.Model):
    _inherit = 'sale.order'

    def _fiscal_position_map(self, cr, uid, result, **kwargs):

        if not kwargs.get('context', False):
            kwargs['context'] = {}
        #NotImplementedError: 'update' not supported on frozendict
        #kwargs['context'].update({'use_domain': ('use_sale', '=', True)})
        company_id = kwargs.get('company_id')
        kwargs.update({'company_id': company_id})
        fp_rule_obj = self.pool.get('account.fiscal.position.rule')
        return fp_rule_obj.apply_fiscal_mapping(cr, uid, result, **kwargs)

    def onchange_partner_id(self, cr, uid, ids, partner_id, context=None):
        if not context:
            context = {}
        result = super(sale_order, self).onchange_partner_id(cr, uid, ids, partner_id, context=context)

        if not context.get('company_id'):
            return result

        values = result['value']
        kwargs = {
            'company_id': context['company_id'],
            'partner_id': partner_id,
            'partner_invoice_id': values.get('partner_invoice_id', False),
            'partner_shipping_id': values.get('partner_shipping_id', False),
            'context': context
        }
        return self._fiscal_position_map(cr, uid, result, **kwargs)

   
    #method not being called
    def onchange_warehouse_id(self, cr, uid, ids, warehouse_id, context=None, **kwargs):
        result = super(sale_order,self).onchange_warehouse_id(cr, uid, ids, warehouse_id, context=context)
        
        if not context:
            context = {}
            
        if not warehouse_id:
            return result
        
        kwargs.update({
            'company_id': context.get('company_id',False),
            'partner_id': context.get('partner_id',False),
            'partner_invoice_id': context.get('partner_invoice_id',False),
            'partner_shipping_id': context.get('partner_shipping_id',False),
            'context': context
        })
        
        return self._fiscal_position_map(cr, uid, result, **kwargs)
    
    
    
    def onchange_delivery_id(self, cr, uid, ids, company_id, partner_id, delivery_id, fiscal_position, context=None, **kwargs):
        result = super(sale_order,self).onchange_delivery_id( cr, uid, ids, company_id = company_id, partner_id = partner_id, delivery_id = delivery_id, fiscal_position = fiscal_position, context=context)
        if not context:
            context = {}
        if not company_id and not partner_id:
            return result
        
        kwargs.update({
            'company_id': company_id,
            'partner_id': partner_id,
            'partner_invoice_id': context.get('partner_invoice_id',False),
            'partner_shipping_id': delivery_id,
            'context': context
        })
        
        return self._fiscal_position_map(cr, uid, result, **kwargs)