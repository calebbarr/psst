from unittest import TestLoader, TextTestRunner, TestSuite, TestCase
from utils import head,tail,
from psst import also_to,get_recipients,_get_message


message = "@walrusthecat @billiebaxter do all the things!"

class Tests(TestCase):

    def test_get_recipients(self):
        self.assertEqual(
            get_recipients(message.split())
            ,
            ["@walrusthecat", "@billiebaxter"]
        )

    def test_get_message(self):        
        self.assertEqual(
            _get_message(get_recipients(message.split()),message.split())
            ,
            "do all the things!"
        )
    
    
class UtilsTests(TestCase):
    
    def test_tail(self):
        self.assertEqual(tail([1,2,3,4,5]) , [2,3,4,5])
        self.assertEqual(tail([1,]) , [])
        
    def test_head(self):
        self.assertEqual(head([1,2,3,4,5]) , 1)
        self.assertEqual(head([]) , None)
        self.assertEqual(
            head(get_recipients(message.split()))
            ,
            "@walrusthecat")
    
def run():
    loader = TestLoader()
    suite = TestSuite((
        loader.loadTestsFromTestCase(UtilsTests),
        loader.loadTestsFromTestCase(Tests)
    ))
    runner = TextTestRunner(verbosity = 2)
    runner.run(suite)
    
if __name__ == '__main__':
    run()