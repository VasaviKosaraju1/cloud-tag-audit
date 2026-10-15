import unittest
from audit import audit
class Tests(unittest.TestCase):
    def config(self): return {'required_tags':['owner','environment'],'allowed_values':{'environment':['prod','dev']},'resources':[{'id':'one','tags':{'owner':'team','environment':'prod'}}]}
    def test_compliant(self): self.assertEqual(audit(self.config())['compliance_ratio'],1)
    def test_blank(self):
        c=self.config();c['resources'][0]['tags']['owner']=' ';self.assertEqual(audit(c)['findings'][0]['issues'][0]['reason'],'missing_or_blank')
    def test_invalid_value(self):
        c=self.config();c['resources'][0]['tags']['environment']='production';self.assertEqual(audit(c)['findings'][0]['issues'][0]['reason'],'invalid_value')
    def test_missing_required(self):
        c=self.config();del c['resources'][0]['tags']['owner'];self.assertEqual(len(audit(c)['findings']),1)
    def test_empty_inventory_not_full_compliance(self):
        c=self.config();c['resources']=[];self.assertIsNone(audit(c)['compliance_ratio'])
    def test_duplicate_id(self):
        c=self.config();c['resources']*=2
        with self.assertRaises(ValueError): audit(c)
    def test_nonstring_tag(self):
        c=self.config();c['resources'][0]['tags']['owner']=123
        with self.assertRaises(ValueError): audit(c)
    def test_case_sensitive_keys(self):
        c=self.config();c['resources'][0]['tags']['Owner']=c['resources'][0]['tags'].pop('owner');self.assertEqual(len(audit(c)['findings']),1)
if __name__=='__main__': unittest.main()
