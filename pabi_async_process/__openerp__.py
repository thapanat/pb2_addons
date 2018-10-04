# -*- coding: utf-8 -*-
{
    'name': 'Asynchronous Actions',
    'version': '8.0.1.0.0',
    'author': 'Kitti U. (Ecosoft)',
    'license': 'AGPL-3',
    'category': 'Generic Modules',
    'depends': [
        'pabi_utils',
        'purchase_invoice_plan',
        'sale_invoice_plan',
        'pabi_procurement',
        'pabi_th_tax_report',
        'account_subscription_enhanced',
        'pabi_hr_salary',
        'pabi_budget_plan',
        'pabi_asset_management',
        'sale_automatic_workflow',
    ],
    'data': [
        'action_sale_create_invoice/sale_view.xml',
        'action_sale_create_invoice/pabi_process.xml',
        'action_purchase_create_invoice/purchase_view.xml',
        'action_purchase_create_invoice/pabi_process.xml',
        'action_run_tax_report/tax_report_wizard.xml',
        'action_run_tax_report/pabi_process.xml',
        'action_generate_entries/account_subscription_generate_view.xml',
        'action_generate_entries/pabi_process.xml',
        'action_open_hr_salary/hr_salary_view.xml',
        'action_open_hr_salary/pabi_process.xml',
        'action_generate_budget_plans/generate_budget_plan_wizard.xml',
        'action_generate_budget_plans/pabi_process.xml',
        'action_asset_depre_line/asset_view.xml',
        'action_asset_depre_line/pabi_process.xml',
        'action_confirm_pos_order/sale_view.xml',
        'action_confirm_pos_order/pabi_process.xml',
        # Using pabi.asset class as guideline
        'pabi_action_generate_entries/pabi_action_generate_entries.xml',
        'pabi_action_generate_entries/pabi_process.xml',
        'pabi_action_asset_compute/security/ir.model.access.csv',
        'pabi_action_asset_compute/pabi_process.xml',
        'pabi_action_asset_compute/xlsx_template/templates.xml',
        'pabi_action_asset_compute/xlsx_template/load_template.xml',
        'pabi_action_asset_compute/xlsx_template/xlsx_template_wizard.xml',
        'pabi_action_asset_compute/pabi_action_asset_compute.xml',
        'pabi_action_asset_compute/pabi_depre_batch_view.xml',
        'pabi_action_asset_compute/report/report_paperformat_data.xml',
        'pabi_action_asset_compute/report/report_asset_depre_batch.xml',
        'pabi_action_asset_compute/report/report_data.xml',
    ],
    'installable': True,
    'application': False,
}
