import unittest
from selenium import webdriver
from page import BasePage
import time

class TestBase(unittest.TestCase):
    """
    TBD
    """
    def setUp(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option("detach", True)
        chrome_options.add_argument('headless')
        # chrome_options.add_argument('window-size=1920x1080')
        self.driver = webdriver.Chrome(options=chrome_options)

    def tearDown(self):
        self.driver.close()

class TestHome(TestBase):
    """
    TBD
    """
    def setUp(self):
      super().setUp()
      self.home = BasePage(self.driver)

    def testIfNumofBoxOfBeginner(self):
      self.home.SelectGameLevel('Beginner')
      self.assertEqual(self.home.getMineSweeperWidth(), 9)
      self.assertEqual(self.home.getMineSweeperHeight(), 9)

    def testIfNumofBoxOfIntermediate(self):
      self.home.SelectGameLevel('Intermediate')
      self.assertEqual(self.home.getMineSweeperWidth(), 16)
      self.assertEqual(self.home.getMineSweeperHeight(), 16)

    def testIfNumofBoxOfExpert(self):
      self.home.SelectGameLevel('Expert')
      self.assertEqual(self.home.getMineSweeperWidth(), 30)
      self.assertEqual(self.home.getMineSweeperHeight(), 16)

    def test1(self):
      self.home.playUntilWin('Beginner')
      # self.home.playUntilWin('Intermediate')


if __name__ == '__main__':
    unittest.main()