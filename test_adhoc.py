import unittest
import adhoc as parentclass

class testUM(unittest.TestCase):
    def setUp(self) -> None:
        pass
    def testadhoc(self):
        #Given
        x = 10

        #When
        b = parentclass.A()
        y = b.findnaturalnumber(10)
        #Then

        self.assertEqual(y,10)
        pass
    def tearDown(self) -> None:
        pass

if __name__ == '__main__':
    unittest.main()
