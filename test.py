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
        # chrome_options.add_argument('headless')
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

    def testCase1(self):
      self.home.SelectGameLevel('Beginner')
      self.assertEqual(self.home.getGameboardStats(), [9,9,10])
      self.home.SelectGameLevel('Intermediate')
      self.assertEqual(self.home.getGameboardStats(), [16,16,40])
      self.home.startNewGame()
      self.assertEqual(self.home.getGameboardStats(), [16,16,40])
      self.home.SelectGameLevel('Beginner')
      self.assertEqual(self.home.getGameboardStats(), [9,9,10])

    def testCase2(self):
      self.home.SelectGameLevel('Beginner')
      self.assertEqual(self.home.getGameboardStats(), [9,9,10])
      self.home.startNewGame()
      self.assertEqual(self.home.getGameboardStats(), [9,9,10])
      self.home.SelectGameLevel('Expert')
      self.assertEqual(self.home.getGameboardStats(), [30,16,99])
      self.home.startNewGame()
      self.assertEqual(self.home.getGameboardStats(), [30,16,99])
      self.home.SelectGameLevel('Intermediate')
      self.assertEqual(self.home.getGameboardStats(), [16,16,40])
      self.home.startNewGame()
      self.assertEqual(self.home.getGameboardStats(), [16,16,40])
      self.home.SelectGameLevel('Expert')
      self.assertEqual(self.home.getGameboardStats(), [30,16,99])
      self.home.SelectGameLevel('Beginner')
      self.assertEqual(self.home.getGameboardStats(), [9,9,10])

    def testCase3(self):
      self.home.SelectCustomerGame(25, 25, 50)
      self.home.startNewGame()
      self.assertEqual(self.home.getGameboardStats(), [25,25,50])
      self.home.startNewGame()
      self.assertEqual(self.home.getGameboardStats(), [25,25,50])
      self.home.SelectGameLevel('Expert')
      self.assertEqual(self.home.getGameboardStats(), [30,16,99])
      self.home.SelectGameLevel('Intermediate')
      self.assertEqual(self.home.getGameboardStats(), [16,16,40])
      
    
    # def testPath_AC2(self):
    #   self.home.SelectGameLevel('Intermediate')
    #   self.assertEqual(self.home.getMineSweeperWidth(), 16)
    #   self.assertEqual(self.home.getMineSweeperHeight(), 16)

    # def testPath_AC3(self):
    #   self.home.SelectGameLevel('Expert')
    #   self.assertEqual(self.home.getMineSweeperWidth(), 30)
    #   self.assertEqual(self.home.getMineSweeperHeight(), 16)

    # def test1(self):
    #   self.home.SelectGameLevel('Beginner')
    #   self.home.playUntilWin()
      # self.home.playUntilWin('Intermediate')


if __name__ == '__main__':
    unittest.main()