#! /usr/bin/env python3

import os
from selenium.webdriver import Firefox
from selenium.webdriver import FirefoxOptions
from selenium.webdriver.common.keys import Keys    
from selenium.webdriver.common.action_chains import ActionChains

#os.system("export DISPLAY=:0")
os.environ["MOZ_HEADLESS"] = "1"

#option = FirefoxOptions()
#option.add_argument("--headless")
#driver = Firefox(firefox_options=option)
driver = Firefox()
driver.set_window_size(1024, 768)
#driver.get('https://www.violapterin.com')
driver.get("https://www.violapterin.com/post/191004--twilight-gods.html")
#screen = driver.get_screenshot_as_png()
#driver.save_screenshot('test.png')

#os.remove("test.png")
zoom = ActionChains(driver)
main = driver.find_element_by_tag_name('main')
#for _ in range(3):
main.screenshot("test-1.png")
zoom.send_keys_to_element(main, Keys.CONTROL, "+").perform()
main.screenshot("test-2.png")
zoom.send_keys_to_element(main, Keys.CONTROL, "+").perform()
main.screenshot("test-3.png")
#screen = main.get_screenshot_as_png()
driver.quit()
