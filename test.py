import unittest
from selenium import webdriver
from page import BasePage
from selenium.common.exceptions import TimeoutException
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
      self.mines = [[0, 2] ,
                    [2, 0] ,
                    [3, 4] ,
                    [2, 4] ,
                    [2, 2] ,
                    [2, 3] ,
                    [0, 4] ,
                    [1, 1] ,
                    [3, 3] ,
                    [0, 1]]
      self.notMines = [[1, 2] ,
                      [4, 3] ,
                      [4, 4] ,
                      [2, 1] ,
                      [1, 4] ,
                      [4, 2] ,
                      [1, 3] ,
                      [1, 0] ,
                      [0, 3] ,
                      [3, 1] ,
                      [3, 0] ,
                      [4, 1] ,
                      [4, 0] ,
                      [3, 2] ,
                      [0, 0] ,]

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

    def testCase4__0_1_2_3_2_4_7(self):
      self.home.SelectCustomerGame(5, 5, 10)
      self.home.startNewGame()
      self.home.markFlag(2, 0)
      self.home.clickBox(0, 2)
      self.assertEqual(self.home.getFlagBoxCount(), 1)
      self.assertEqual(self.home.getNumberCount(), 0)
      self.assertEqual(self.home.getExplodeCount(), 1)

    def testCase5__0_1_4_8_2_3_2_3_2_3_2_5_6_8_2____8_9_10(self):
      self.home.SelectCustomerGame(5, 5, 10)
      self.home.startNewGame()
      self.home.clickBox(2, 1)
      self.home.markFlag(0, 2)
      self.home.markFlag(1, 1)
      self.home.markFlag(2, 2)
      self.home.openMultipleBoxes(2,1)
      for x,y in self.notMines:
        self.home.clickBox(x, y)
      try:
        self.home.clearAlert()
      except TimeoutException:
        print(' ')
      
      self.assertEqual(self.home.getFlagBoxCount(), 3)
      self.assertEqual(self.home.getNumberCount(), 13)
      self.assertEqual(self.home.getExplodeCount(), 0)

    def testCase6__0_1_8_2__8_2__8_9_10_0(self):
      self.home.SelectCustomerGame(5, 5, 10)
      self.home.startNewGame()
      for x,y in self.notMines:
        self.home.clickBox(x, y)
      try:
        self.home.clearAlert()
      except TimeoutException:
        print(' ')
      self.home.startNewGame()
      self.assertEqual(self.home.getFlagBoxCount(), 0)
      self.assertEqual(self.home.getNumberCount(), 0)
      self.assertEqual(self.home.getExplodeCount(), 0)

    def testCase7__0_1_2_4_7_0(self):
      self.home.SelectCustomerGame(5, 5, 10)
      self.home.startNewGame()
      self.home.clickBox(0, 2)
      self.home.startNewGame()
      self.assertEqual(self.home.getFlagBoxCount(), 0)
      self.assertEqual(self.home.getNumberCount(), 0)
      self.assertEqual(self.home.getExplodeCount(), 0)    
  

if __name__ == '__main__':
    unittest.main()