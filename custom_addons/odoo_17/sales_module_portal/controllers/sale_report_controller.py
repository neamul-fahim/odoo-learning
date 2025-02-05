from odoo import http
from odoo.http import request
from odoo.addons.portal.controllers.portal import CustomerPortal,pager


class SalesDashboardController(CustomerPortal):
    def _prepare_home_portal_values(self, counters):
        values = super()._prepare_home_portal_values(counters)

        if 'sales_dashboard_count_portal' in counters:
            values['sales_dashboard_count_portal'] = 1
        return values

    @http.route('/sale_report_data', type='json', auth='user')
    def get_sales_data(self):
        print(f'===================rpc call================')

        SaleReport = request.env['sale.report']
        # Fetch total sales, confirmed orders, and average sales value
        total_sales = sum(SaleReport.search([]).mapped('price_total'))
        confirmed_orders = len(SaleReport.search([('state', '=', 'sale')]))
        average_sales_value = total_sales / confirmed_orders if confirmed_orders else 0
        print(f'total_sales===  {total_sales}')
        print(f'confirmed_orders===  {confirmed_orders}')
        print(f'average_sales_value===  {average_sales_value}')


        # Fetch sales distribution by category
        # sales_by_category = []
        # category_data = SaleReport.read_group(
        #     [], ['price_total'], ['product_category_id']
        # )
        # for category in category_data:
        #     category_name = request.env['product.category'].browse(
        #         category['product_category_id'][0]
        #     ).name if category['product_category_id'] else 'Uncategorized'
        #     sales_by_category.append({
        #         'name': category_name,
        #         'total': category['price_total'],
        #     })
        # print(f'average_sales_value===  {sales_by_category}')

        # Fetch recent sales orders
        # recent_orders = SaleReport.search([], limit=5).read(['name', 'partner_id', 'price_total', 'state'])
        return {
            'total_sales': total_sales,
            'confirmed_orders': confirmed_orders,
            'average_sales_value': average_sales_value,
            # 'recent_orders': recent_orders,
            # 'sales_by_category': sales_by_category,
        }



    @http.route('/sales_report_dashboard', type='http', auth='user', methods=['GET'], website=True)
    def sales_report(self, page=1, sortby='id', **kw):

        return request.render('sales_module_portal.sales_report_template')