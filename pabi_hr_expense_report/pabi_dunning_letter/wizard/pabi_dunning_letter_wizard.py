# -*- coding: utf-8 -*-
from datetime import datetime
from dateutil.relativedelta import relativedelta
from openerp import models, fields, api


class PABIDunnintLetterWizard(models.TransientModel):
    _name = 'pabi.dunning.letter.wizard'

    due_days = fields.Selection(
        [('10', '10 days to due date'),
         ('5', '5 days to due date'),
         ('0', 'On due date'),
         ('-1', 'Pass due date')],
        string='Due',
        required=True,
    )
    print_pdf = fields.Boolean(
        string='Print as PDF',
        default=True,
    )
    send_email = fields.Boolean(
        string='Send Email',
        default=True,
    )
    to_mail_group_ids = fields.Many2many(
        'mail.group',
        string='TO:',
    )
    cc_mail_group_ids = fields.Many2many(
        'mail.group',
        string='CC:',
    )
    dunning_list_ids = fields.One2many(
        'dunning.list',
        'wizard_id',
        string='List of Dunning',
    )

    @api.onchange('due_days')
    def _onchange_due_days(self):
        self.dunning_list_ids = []
        Line = self.env['dunning.list']
        Expense = self.env['hr.expense.expense']
        today = datetime.strptime(fields.Date.context_today(self),
                                  '%Y-%m-%d').date()
        date_due = today + relativedelta(days=int(self.due_days))
        date_due = date_due.strftime('%Y-%m-%d')
        operator = self.due_days == '-1' and '<=' or '='
        expenses = Expense.search([('state', '=', 'paid'),
                                   ('date_due', operator, date_due),
                                   ('amount_to_clearing', '>', 0.0)])
        for expense in expenses:
            new_line = Line.new()
            new_line.expense_id = expense
            new_line.select = True
            self.dunning_list_ids += new_line

    @api.multi
    def run_report(self):
        data = {'parameters': {}}
        report_name = 'pabi_dunning_letter'
        # For ORM, we search for ids, and only pass ids to parser and jasper
        exp_ids = [x.select and x.expense_id.id for x in self.dunning_list_ids]
        exp_ids = list(set(exp_ids))  # remove all False
        if False in exp_ids:
            exp_ids.remove(False)
        if not self.print_pdf or not exp_ids:
            return {}
        data['parameters']['ids'] = exp_ids
        data['parameters']['due_days'] = self.due_days
        res = {
            'type': 'ir.actions.report.xml',
            'report_name': report_name,
            'datas': data,
            'context': {'lang': 'th_TH'}
        }
        return res


class DunningList(models.TransientModel):
    _name = 'dunning.list'

    wizard_id = fields.Many2one(
        'pabi.dunning.letter.wizard',
        string='Wizard',
        readonly=True,
    )
    select = fields.Boolean(
        string='Select',
        default=True,
    )
    expense_id = fields.Many2one(
        'hr.expense.expense',
        string='Employee Advance',
    )
    employee_id = fields.Many2one(
        'hr.employee',
        related='expense_id.employee_id',
        string='Employee',
        readonly=True,
    )
    date_due = fields.Date(
        string='Date Due',
        related='expense_id.date_due',
        readonly=True,
    )
    amount_to_clearing = fields.Float(
        string='Amount Remaining',
        related='expense_id.amount_to_clearing',
        readonly=True,
    )
    description = fields.Char(
        string='Description',
        related='expense_id.name',
        readonly=True,
    )
