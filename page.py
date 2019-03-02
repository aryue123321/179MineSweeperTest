from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common import alert
import random
import time

class BasePage:
  
  def __init__(self, driver, level):
    self.driver = driver
    self.driver.get("http://michaelbutler.github.io/minesweeper/")
    self.NEWGAME = (By.CSS_SELECTOR, "#minesweeper > div.game_actions > button.new-game")
    self.LEVEL_DROPDOWN = (By.ID, "level")
    self.TIMER = (By.ID, "#timer")
    self.SelectGameLevel(level)
    self.width = int(self.driver.find_element_by_css_selector('#minesweeper > div.board-wrap > ul:last-child > li:last-child').get_attribute('data-x'))+1
    self.height = int(self.driver.find_element_by_css_selector('#minesweeper > div.board-wrap > ul:last-child > li:last-child').get_attribute('data-y'))+1
    print(self.width, self.height)


  def SelectGameLevel(self, level):
    levelDropdown = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(self.LEVEL_DROPDOWN))
    levelDropdown.click()
    for option in levelDropdown.find_elements_by_tag_name('option'):
      print(option.text)
      if option.text == level:
          option.click() # select() in earlier versions of webdriver
          break


  def playUntilWin(self):
    while not self.randomClick() and not self.simpleMineDetecion():
      if self.isGameOver():
        self.startNewGame()

  def randomClick(self):
    boxes = self.driver.find_elements_by_css_selector("#minesweeper > div.board-wrap > ul > li")
    # boxes = WebDriverWait(self.driver, 10).until(EC.visibility_of_all_elements_located(self.BOXES))
    unkwonBoxes = list(filter(lambda x: x.get_attribute('class') == 'cell unknown', boxes))
    unkwonBoxes[random.randint(0, len(unkwonBoxes)-1)].click()
    try:
      self.clearAlert()
      return True
    except TimeoutException:
      print('randomClickOK')
      return False

  def isGameOver(self):
    boxes = self.driver.find_elements_by_css_selector("#minesweeper > div.board-wrap > ul > li")
    return any(x.get_attribute('class') == 'cell explode ui-icon ui-icon-close blown' for x in boxes)
    
    
  def startNewGame(self):
    newGameButton = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(self.NEWGAME))
    newGameButton.click()

  def simpleMarkBomb(self):
    boxes = WebDriverWait(self.driver, 10).until(EC.visibility_of_all_elements_located(self.BOXES))

  def markSingleFlags(self, box):
    actionChains = ActionChains(self.driver)
    actionChains.context_click(box).perform()

  def simpleMineDetecion(self):
    while True:
      isDetect = False
      isClear = False
      boxes = self.driver.find_elements_by_css_selector("#minesweeper > div.board-wrap > ul > li")
      for box in boxes:
        if isDetect or isClear:
          break
        if box.get_attribute('class') == 'cell number':
          x = int(box.get_attribute('data-x'))
          y = int(box.get_attribute('data-y'))
          unknown = []
          known = 0
          num = int(box.get_attribute('data-number'))
          for i in range(-1, 2):
            for j in range(-1, 2):
              index = (x+i) + (y+j)*self.height
              if x+i >= 0 and x+i < self.width and y+j >= 0 and y+j < self.height:
                boxClass = boxes[index].get_attribute('class')
                if boxClass == 'cell unknown':
                  unknown.append(boxes[index])
                if boxClass == 'cell ui-icon ui-icon-flag flagged':
                  known += 1
          if len(unknown) + known == num:
            # isClear = True
            for box in unknown:
              self.markSingleFlags(box)
          elif known == num:
            isClear = True
            for box in unknown:
              try:
                box.click()
                self.clearAlert()
                return True
              except TimeoutException:
                continue
      if not isDetect and not isClear:
        return False

  def clearAlert(self):
    WebDriverWait(self.driver, 0.2).until(EC.alert_is_present())
    alert = self.driver.switch_to.alert;
    alert.accept()
    WebDriverWait(self.driver, 0.2).until(EC.alert_is_present())
    alert = self.driver.switch_to.alert;
    alert.dismiss()

  def printEle(self):
    boxes = WebDriverWait(self.driver, 10).until(EC.visibility_of_all_elements_located(self.BOXES))
    [print(box.get_attribute('data-x'), box.get_attribute('data-y')) for box in boxes] 
      