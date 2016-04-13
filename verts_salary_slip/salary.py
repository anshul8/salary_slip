# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2011-2015 Verts Services India Pvt. Ltd. (<http://www.verts.co.in>)
#    Copyright (C) 2004-2010 OpenERP SA (<http://www.openerp.com>)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>
#
##############################################################################


from openerp.osv import fields, osv
from openerp import tools
from openerp.tools.translate import _
from openerp import netsvc
from datetime import datetime, timedelta
from email import _name
from bsddb.dbtables import _columns
from numpy.ma.core import ids


class emp1(osv.osv):
    
    _name= "emp1"
    _rec_name="emp_name"
    #_rec_name="emp_id"
    _columns= {
               'xls':fields.binary('xls'),
               'file':fields.text('File'),
               'emp_id':fields.integer('S.No'),
               'emp_name' : fields.char('Employee Name', size=64),
               'emp_desig':fields.char('Employee Designation',size=64),
               'emp_dep': fields.selection([('hr','HR'),
                                           ('designer','Designer'),('developer','Developer')],'Department'),
               'emp_basic':fields.integer('Basic Pay'),
               'state':fields.selection([('draft','Draft'),('confirm','Confirm')],'State'),
               
               }
    def write_draft(self,cr,uid,ids,emp_id,context=None):
       
        
        print "Self===",self
        print "cursor===",cr
        print "UID===",uid
        print "ID===",ids
        for mov in self.browse(cr, uid, ids, context=None):
            print "id=",mov.emp_id
            print "name=",mov.emp_name
            print "department=",mov.emp_dep
            
        rec_ids = self.pool.get('emp.details').search(cr, uid,()) 
        print "reccccccccc",rec_ids,len(rec_ids)   
        emp_obj=self.pool.get('emp.details').browse(cr,uid,rec_ids)
        print "emp_obj=",emp_obj  
        for i in range(len(rec_ids)):
            print"hjgjhg=",emp_obj,",",emp_obj[i].emp_name,"\n"
     

        
        return True
    def write_confirm(self,cr,uid,ids,context=None):
        return True
#     def import_excel(self,cr,uid,ids,context=None):
#            
#             import xlrd
#             from xlrd import open_workbook, cellname
# 
#             book = open_workbook('/home/anshul/Desktop/abc.xlsx')
#             print "book=",book
#             
#             sheet = book.sheet_by_index(0)
#             print"sheet",sheet
#         
# 
#             print"KEYS=",sheet.ncols
#             print"Keys=",sheet.cell(0,1).value
#             x=sheet.nrows
#           
#           
#             self.lis=[]
#            
#             
#             print "Rows=",x
#             for i in range(0,x):
#                 for j in range(0,sheet.ncols):
#                    
#                     self.lis.append(sheet.cell(i,j).value)
#                     print "LIST 2=",self.lis
#                    
# #                  {keys[col_index]: sheet.cell(row_index, col_index).value 
# #                      for col_index in xrange(sheet.ncols)}
#               
#             
#             print "Length=",len(self.lis)
#             self.write(cr,uid,ids,{'file':self.lis})
# 
#     def write_excel(self,cr,uid,ids,context=None):  
#             import xlwt
#             k=0
#             i=0
#             workbook = xlwt.Workbook() 
#             sheet = workbook.add_sheet("Sheet Name")
#             print "list==",self.lis 
#             print"length=",len(self.lis)
#             for rec in self.browse(cr,uid,ids,context=None):
#                 print "Record=",rec
#                 
#                 for j in range(4):
#                     for k in range(3):
#                         print "length1=",len(self.lis)
#                         sheet.write(k, j, self.lis[i])
#                         i=i+1
#             workbook.save("test.xls")
#     _defaults = {
#                      'emp_name': lambda obj, cr, uid, context: obj.pool.get('ir.sequence').get(cr, uid, 'emp1'),
#                      }
            
    _defaults = {
        'emp_name': lambda obj, cr, uid, context: '/', 
        'state': 'draft',
        'emp_dep':'hr',
    }
 
 
    def create(self, cr, uid, vals, context=None):
        if vals.get('emp_name','/')=='/':
            vals['emp_name'] = self.pool.get('ir.sequence').get(cr, uid, 'emp1') or '/'
        return super(emp1, self).create(cr, uid, vals, context=context)
    
class emp2(osv.osv):
    _name="emp2"
    _columns={
              'emp_id':fields.many2one('emp1','Select Employee Id'),
              'emp_name':fields.char('Employee Name', size=64),
              'emp_desig':fields.char('Employee Designation',size=64),
              'emp_dep':fields.char('Employee Department',size=64),
              'emp_basic':fields.integer('Basic Salary'),
              'emp_hra':fields.integer('HRA'),
              'emp_ta':fields.integer('TA'),
              'emp_da':fields.integer('DA'),
              'emp_pf':fields.integer('PF'),
              'emp_it':fields.integer('IT'),
              'emp_net':fields.integer('Net Salary'),
              'date':fields.date('Date'),
              'pq':fields.many2one('emp3')
              }
    def onchange_emp_id(self,cr,uid,ids,emp_id,context=None):
        res={}
        rec=self.pool.get("emp1").browse(cr,uid,emp_id)
        name=rec.emp_name
        desig=rec.emp_desig
        dep=rec.emp_dep
        basic=rec.emp_basic
        emp_hra=(basic*18)/100
        emp_ta=(basic*16)/100
        emp_da=(basic*12)/100
        emp_pf=(basic*8)/100
        emp_it=(basic*9)/100
        emp_net=basic+emp_hra+emp_da+emp_ta-emp_pf-emp_it
        res={'value': {'emp_name': name,'emp_desig':desig,'emp_dep':dep,'emp_basic':basic,'emp_hra':emp_hra,'emp_ta':emp_ta,'emp_da':emp_da,'emp_pf':emp_pf,'emp_it':emp_it,'emp_net':emp_net}}
        return res
    
class emp3(osv.osv):
    _name="emp3"
    
    def _calc_total(self,cr,uid,ids,field_name, arg,context=None):
        a=0
        res={}
        emp_ids=self.search(cr,uid,())
        print"emp2browse=",emp_ids
       
       
        for i in self.browse(cr,uid,ids):
            for j in i.xy:
                print j.emp_hra
                a+=j.emp_hra
                res[i.id] = a
        print a
        return res
    
            
    _columns={
              'xy':fields.one2many('emp2','pq','Employee'),
              'total':fields.function(_calc_total,string='TOTAL'),
            
              }
    
         
