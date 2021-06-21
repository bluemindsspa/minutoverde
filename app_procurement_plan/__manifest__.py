# -*- coding: utf-8 -*-

# Created on 20120-01-05
# author: 广州尚鹏，https://www.sunpop.cn
# email: 300883@qq.com
# resource of Sunpop
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

# Odoo12在线用户手册（长期更新）
# https://www.sunpop.cn/documentation/user/12.0/zh_CN/index.html

# Odoo12在线开发者手册（长期更新）
# https://www.sunpop.cn/documentation/12.0/index.html

# Odoo10在线中文用户手册（长期更新）
# https://www.sunpop.cn/documentation/user/10.0/zh_CN/index.html

# Odoo10离线中文用户手册下载
# https://www.sunpop.cn/odoo10_user_manual_document_offline/
# Odoo10离线开发手册下载-含python教程，jquery参考，Jinja2模板，PostgresSQL参考（odoo开发必备）
# https://www.sunpop.cn/odoo10_developer_document_offline/

##############################################################################
#    Copyright (C) 2009-TODAY Sunpop.cn Ltd. https://www.sunpop.cn
#    Author: Ivan Deng，300883@qq.com
#    You can modify it under the terms of the GNU LESSER
#    GENERAL PUBLIC LICENSE (LGPL v3), Version 3.
#    See <http://www.gnu.org/licenses/>.
#
#    It is forbidden to publish, distribute, sublicense, or sell copies
#    of the Software or modified copies of the Software.
##############################################################################

{
    'name': "Sale Procurement Plan. 自定义MRP销售安排",
    'version': '14.21.03.11',
    'author': 'Sunpop.cn',
    'category': 'Base',
    'website': 'https://www.sunpop.cn',
    'license': 'LGPL-3',
    'sequence': 2,
    'price': 98.00,
    'currency': 'EUR',
    'images': ['static/description/banner.gif'],
    'depends': [
        'mrp',
        'purchase_stock',
        'purchase_requisition_stock',
        'procurement_jit',
    ],
    'summary': '''
    Manual set how product supply in Sale order. sale order manufacture plan , purchase plan, use stock plan.
    Set every product supply by manufacture + buy + use stock.  
    Add a manual node before normal procurement.增加人工控制的补货组。 
    ''',
    'description': '''    
    Support Odoo 14,13,12, Enterprise and Community Edition
    1. Manual set how product supply in Sale order
    2. Set every sale product supply by manufacture + buy + stock, MTO and MTS　supported follow odoo origin rule
    3. The sales plan can also be arranged in batches. Merge several sale orders into 1 plan.
    4. The plan  follow all the odoo advance stock rule setup. U can use odoo pulll and push rule
    5. Multi-language Support.
    6. Multi-Company Support.
    7. Support Odoo 14， 13，12, Enterprise and Community Edition
    ==========
    1. 人工设置销售订单补货方式
    2. 可将每个销售订单行中的产品按 生产+采购+现货
    3. 可批量安排，即将多张销售订单一并安排 生产+采购+现货, 支持MTO 及 MTS 等 odoo 原生高级路线设置
    4. 原生库存高级路线兼容，可匹配高级推拉规则
    3. 多语言支持
    4. 多公司支持
    5. Odoo 14， 13, 12, 企业版，社区版，多版本支持
    ''',
    'data': [
        'security/app_security.xml',
        'security/ir.model.access.csv',
        'data/ir_sequence_data.xml',
        'data/stock_location_route_data.xml',
        'views/res_config_settings_views.xml',
        'views/stock_location_route_views.xml',
        'views/sale_order_views.xml',
        'views/sale_order_line_views.xml',
        'views/procurement_plan_views.xml',
        'views/procurement_group_views.xml',
        'views/purchase_order_views.xml',
        'views/purchase_requisition_views.xml',
        'wizard/sale_order_to_plan_views.xml',
        # 'report/.xml',
    ],
    'qweb': [
        'static/src/xml/*.xml',
    ],
    'demo': [],
    # 'pre_init_hook': 'pre_init_hook',
    # 'post_init_hook': 'post_init_hook',
    # 'uninstall_hook': 'uninstall_hook',
    'installable': True,
    'application': True,
    'auto_install': False,
}
