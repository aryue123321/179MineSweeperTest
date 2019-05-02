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
    
    def playGame(self, X, width, height, mines):
      self.home.startNewGame()
      while not self.home.randomClick() and not self.home.simpleMineDetecion():
        if self.home.isGameOver:
          self.assertEqual(len(self.home.driver.find_elements_by_class_name('blown')), mines)
          boxes = self.home.driver.find_elements_by_css_selector("#minesweeper > div.board-wrap > ul > li")
          for i in range(0, width):
            for j in range(0, height):
              dataNum = boxes[i+j*width].get_attribute('data-number')
              if dataNum == '':
                continue;
              dataNum = int(dataNum)
              surrondingMines = self.home.getNumOfMinesSurround(boxes, i, j, width, height)
              self.assertEqual(surrondingMines, dataNum)
              print('i: {}\tj: {}\tdatanum: {}\tmines: {}'.format(i, j, dataNum, surrondingMines))
          X-=1;
          if X == 0:
            break
          self.home.startNewGame()
          self.home.reset()

    def testCase4(self):
      X = 3
      self.home.SelectGameLevel('Beginner')
      width, height, mines = self.home.getGameboardStats()
      self.playGame(X, width, height, mines)
          
  
    def testCase5(self):
      X = 3
      self.home.SelectGameLevel('Intermediate')
      width, height, mines = self.home.getGameboardStats()
      self.playGame(X, width, height, mines)


if __name__ == '__main__':
    unittest.main()