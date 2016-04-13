import time
from openerp.report import report_sxw


class get(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context):
        super(get, self).__init__(cr, uid, name, context)
        self.val={}
        self.localcontext.update({
        
        'time': time,
        })
        
   
report_sxw.report_sxw('report.salary_repo','emp2','addons/verts_salary_slip/report/salary_report.rml', parser=get, header=False)
