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
  
  def __init__(self, driver):
    self.driver = driver
    self.driver.get("http://127.0.0.1:5500/souceCode/index.html")
    self.NEWGAME = (By.CSS_SELECTOR, "#minesweeper > div.game_actions > button.new-game")
    self.LEVEL_DROPDOWN = (By.ID, "level")
    self.TIMER = (By.ID, "#timer")
    self.reset()
    
  def updateBoxState(self, index):
    # x = int(box.get_attribute('data-x'))
    # y = int(box.get_attribute('data-y'))
    # index = (x) + (y)*self.width
    className = self.boxes[index].get_attribute('class')
    if index in self.unknownBoxes and className != 'cell unknown':
      if className == 'cell open':
        self.emptyBoxes.add(index)
      elif className == 'cell number':
        self.numberBoxes.add(index)
      elif className == 'cell ui-icon ui-icon-flag flagged':
        self.flagBoxes.add(index)
      self.unknownBoxes.remove(index)
  
  def getMineSweeperWidth(self):
    return int(self.driver.find_element_by_css_selector('#minesweeper > div.board-wrap > ul:last-child > li:last-child').get_attribute('data-x'))+1
  
  def getMineSweeperHeight(self):
    return int(self.driver.find_element_by_css_selector('#minesweeper > div.board-wrap > ul:last-child > li:last-child').get_attribute('data-y'))+1  

  def getTotalMines(self):
    return int(self.driver.find_element_by_css_selector('#mine_flag_display').get_attribute('value'))

  def getGameboardStats(self):
    return [self.getMineSweeperWidth(), self.getMineSweeperHeight(), self.getTotalMines()]

  def reset(self):
    self.width = self.getMineSweeperWidth();
    self.height = self.getMineSweeperHeight();
    # print(self.width, self.height)
    self.boxes = self.driver.find_elements_by_css_selector("#minesweeper > div.board-wrap > ul > li")
    self.emptyBoxes = set()
    self.flagBoxes = set()
    self.numberBoxes = set()
    self.clearedNumberBoxes = set()
    self.unknownBoxes = set(range(self.width*self.height))
    self.isGameOver = False

  def SelectGameLevel(self, level):
    levelDropdown = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(self.LEVEL_DROPDOWN))
    levelDropdown.click()
    for option in levelDropdown.find_elements_by_tag_name('option'):
      # print(option.text)
      if option.text == level:
          option.click() # select() in earlier versions of webdriver
          break

  def twoDimToOneDim(self, x, y):
    return x + y*self.width
  
  def clickBox(self, x, y):
    self.boxes[self.twoDimToOneDim(x,y)].click()

  def openMultipleBoxes(self, x, y):
    actionChains = ActionChains(self.driver)
    actionChains.move_to_element(self.boxes[self.twoDimToOneDim(x,y)])
    actionChains.click()
    actionChains.context_click()
    actionChains.perform()

  def markFlag(self, x, y):
    actionChains = ActionChains(self.driver)
    actionChains.context_click(self.boxes[self.twoDimToOneDim(x,y)]).perform()
  
  def getUnknownCount(self):
    return len([x for x in self.boxes if 'cell unknown' == x.get_attribute('class') or 'cell unknown test unblown' == x.get_attribute('class')])

  def getClearedBoxCount(self):
    return len([x for x in self.boxes if 'cell unknown unblown' == x.get_attribute('class') or 'cell unknown test unblown' == x.get_attribute('class') or 'cell open' == x.get_attribute('class')])

  def getFlagBoxCount(self):
    return len([x for x in self.boxes if 'cell ui-icon ui-icon-flag flagged ui-icon-close blown' == x.get_attribute('class') or 'cell ui-icon ui-icon-flag flagged' == x.get_attribute('class')])

  def unknownBox(self):
    return len([x for x in self.boxes if 'cell unknown' == x.get_attribute('class')])

  def getUnknownMines(self):
    return len([x for x in self.boxes if "cell unknown ui-icon ui-icon-close blown" == x.get_attribute('class') or 'cell unknown test ui-icon ui-icon-close blown' == x.get_attribute('class')])
  
  def getNumberCount(self):
    return len([x for x in self.boxes if 'cell number unblown' == x.get_attribute('class') or 'cell number' == x.get_attribute('class')])
  
  def getExplodeCount(self):
    return len([x for x in self.boxes if 'cell explode ui-icon ui-icon-close blown' == x.get_attribute('class')]) 
    
  def startNewGame(self):
    print("Start New Game")
    newGameButton = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(self.NEWGAME))
    newGameButton.click()
    self.boxes = self.driver.find_elements_by_css_selector("#minesweeper > div.board-wrap > ul > li")
    self.width = self.getMineSweeperWidth()
    self.height = self.getMineSweeperHeight()

  # def simpleMarkBomb(self):
  #   boxes = WebDriverWait(self.driver, 10).until(EC.visibility_of_all_elements_located(self.BOXES))

  def markSingleFlags(self, box):
    actionChains = ActionChains(self.driver)
    actionChains.context_click(box).perform()


  def clearAlert(self):
    WebDriverWait(self.driver, 0.1).until(EC.alert_is_present())
    alert = self.driver.switch_to.alert;
    alert.accept()
    WebDriverWait(self.driver, 0.1).until(EC.alert_is_present())
    alert = self.driver.switch_to.alert;
    alert.dismiss()

  def printEle(self):
    boxes = WebDriverWait(self.driver, 10).until(EC.visibility_of_all_elements_located(self.BOXES))
    [print(box.get_attribute('data-x'), box.get_attribute('data-y')) for box in boxes]

  def ElementsByClass(self, className):
    return self.driver.find_elements_by_class_name(className)
  
  def SelectCustomerGame(self, x, y, mines):
    self.SelectGameLevel('Custom')
    xInput = self.driver.find_element_by_css_selector('#dim_x')
    print(xInput)
    xInput.clear()
    xInput.send_keys(x)
    yInput = self.driver.find_element_by_css_selector('#dim_y')
    yInput.clear()
    yInput.send_keys(y)
    minesInput = self.driver.find_element_by_css_selector('#numMines')
    minesInput.clear()
    minesInput.send_keys(mines)

  