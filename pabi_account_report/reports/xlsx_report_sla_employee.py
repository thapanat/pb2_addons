from openerp import models, fields, api, tools


class SLAEmployeeView(models.Model):
    _name = 'sla.employee.view'
    _auto = False

    id = fields.Integer(
        string='ID',
        readonly=True,
    )
    voucher_id = fields.Many2one(
        'account.voucher',
        string='Voucher',
        readonly=True,
    )
    invoice_id = fields.Many2one(
        'account.invoice',
        string='Invoice',
        readonly=True,
    )
    export_id = fields.Many2one(
        'payment.export',
        string='Export',
        readonly=True,
    )
    import_id = fields.Many2one(
        'pabi.bank.statement.import',
        string='Import',
        readonly=True,
    )

    def _get_sql_view(self):
        sql_view = """
            SELECT ROW_NUMBER() OVER(ORDER BY av.id) AS id,
                av.id AS voucher_id, inv.id AS invoice_id, exp_line.export_id,
                item.match_import_id AS import_id
            FROM account_move_line l
            LEFT JOIN account_invoice inv ON l.move_id = inv.move_id
            LEFT JOIN account_move_reconcile r ON l.reconcile_id = r.id
                OR l.reconcile_partial_id = r.id
            LEFT JOIN (SELECT * FROM account_move_line
                       WHERE doctype = 'payment') l2 ON
                r.id = l2.reconcile_id OR r.id = l2.reconcile_partial_id
            LEFT JOIN account_voucher av ON l2.move_id = av.move_id
            LEFT JOIN payment_export_line exp_line ON
                av.id = exp_line.voucher_id
            LEFT JOIN payment_export exp ON exp_line.export_id = exp.id
            LEFT JOIN (SELECT i.match_import_id, move.id AS move_id
                       FROM pabi_bank_statement_item i
                       LEFT JOIN account_move_line m_line
                        ON i.move_line_id = m_line.id
                       LEFT JOIN account_move move ON m_line.move_id = move.id
                       LEFT JOIN pabi_bank_statement_import imp
                        ON i.match_import_id = imp.id
                       WHERE i.match_import_id IS NOT NULL) item
                ON l2.move_id = item.move_id
            WHERE l.doctype IN ('in_invoice', 'in_refund') AND
                l.account_id = inv.account_id AND
                    SPLIT_PART(inv.source_document_id, ',', 1)
                        = 'hr.expense.expense' AND av.id IS NOT NULL AND
                        av.state = 'posted' AND exp.state = 'done'
        """
        return sql_view

    def init(self, cr):
        tools.drop_view_if_exists(cr, self._table)
        cr.execute("""CREATE OR REPLACE VIEW %s AS (%s)"""
                   % (self._table, self._get_sql_view()))


class XLSXReportSLAEmployee(models.TransientModel):
    _name = 'xlsx.report.sla.employee'
    _inherit = 'xlsx.report'

    # Search Criteria
    start_period_id = fields.Many2one(
        'account.period',
        string='Period From',
        domain=[('special', '=', False), ('state', '=', 'draft')],
    )
    end_period_id = fields.Many2one(
        'account.period',
        string='Period To',
        domain=[('special', '=', False), ('state', '=', 'draft')],
    )
    user_ids = fields.Many2many(
        'res.users',
        'xlsx_report_sla_employee_users',
        'report_id', 'user_id',
        string='Responsible By',
    )
    category_id = fields.Many2one(
        'res.partner.category',
        string='Supplier Category',
    )
    # Report Result
    results = fields.Many2many(
        'sla.employee.view',
        string='Results',
        compute='_compute_results',
        help='Use compute fields, so there is nothing store in database',
    )

    @api.multi
    def _compute_results(self):
        self.ensure_one()
        Result = self.env['sla.employee.view']
        dom = []
        if self.start_period_id:
            dom += [('voucher_id.period_id.date_start', '>=',
                     self.start_period_id.date_start)]
        if self.end_period_id:
            dom += [('voucher_id.period_id.date_start', '<=',
                     self.end_period_id.date_start)]
        if self.user_ids:
            dom += [('voucher_id.create_uid', 'in', self.user_ids.ids)]
        if self.category_id:
            dom += [('voucher_id.partner_id.category_id', '=',
                     self.category_id.id)]
        self.results = Result.search(dom)
