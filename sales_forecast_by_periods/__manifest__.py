# -*- coding: utf-8 -*-
{
    "name": "Sales Trends and Forecast",
    "version": "14.0.1.0.1",
    "category": "Sales",
    "author": "faOtools",
    "website": "https://faotools.com/apps/14.0/sales-trends-and-forecast-546",
    "license": "Other proprietary",
    "application": True,
    "installable": True,
    "auto_install": False,
    "depends": [
        "sale"
    ],
    "data": [
        "security/security.xml",
        "security/ir.model.access.csv",
        "data/data.xml",
        "wizard/open_sales_series.xml",
        "views/res_config_settings.xml",
        "reports/report_sale_forecast_periods.xml"
    ],
    "qweb": [
        
    ],
    "js": [
        
    ],
    "demo": [
        
    ],
    "external_dependencies": {
        "python": [
                "pandas",
                "numpy",
                "statsmodels",
                "scipy",
                "xlsxwriter"
        ]
},
    "summary": "The tool to calculate sale trends and make prediction for future sales statistically. Sales Forecast",
    "description": """
For the full details look at static/description/index.html

* Features * 

- Statistical methods to forecast sales
- Usage requirements



#odootools_proprietary

    """,
    "images": [
        "static/description/main.png"
    ],
    "price": "198.0",
    "currency": "EUR",
    "live_test_url": "https://faotools.com/my/tickets/newticket?&url_app_id=96&ticket_version=14.0&url_type_id=3",
}