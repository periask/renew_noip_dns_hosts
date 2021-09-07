#!/usr/bin/env python3

import time
from PIL import Image
import cv2
import numpy as np
from datetime import date
import argparse
import os

from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

SCREENSHOTS = 'screeshots'

class NOIP2:
    def __init__(self, username, password):
        self.loginurl = 'https://www.noip.com/login'
        self.dnsurl   = 'https://my.noip.com/dynamic-dns'
        self.auth = {
            'username' : username,
            'password' : password
        }

        options = FirefoxOptions()
        options.add_argument("--headless")
        self.browser = webdriver.Firefox(options=options)
        self.browser.set_page_load_timeout(120)

        # Make directory
        if not os.path.isdir(SCREENSHOTS):
            os.mkdir(SCREENSHOTS)

    def login(self):
        """Login to noip with the given username/password
        and wait for the page load to complete. """
        # open the login page
        self.browser.get(self.loginurl)

        # Enter the credential
        for k in self.auth.keys():
            field = self.browser.find_element_by_name(k)
            field.send_keys(self.auth[k])

        # Click Login
        self.browser.find_element_by_id("clogs-captcha-button").click()

        # Wait till the loads
        try:
            elem = WebDriverWait(self.browser, 10).until(
                EC.presence_of_element_located((By.ID, "content-wrapper")) #This is a dummy element
            )
        except:
             self.browser.quit()

        time.sleep(5)
        # print(self.browser.page_source.encode("utf-8"))

    def xpath_of_button(self, cls_name):
        return "//button[contains(@class, '%s')]" % cls_name

    def confirm_host_enter(self, button):
        """Click the confirm button and renew then host"""
        button.click()
        time.sleep(5)


    def update_hosts(self):
        """Find all the hosts which are to be renewed"""
        # load the DNS host page
        self.browser.get(self.dnsurl)

        # Wait till the loads
        try:
            elem = WebDriverWait(self.browser, 10).until(
                EC.presence_of_element_located((By.ID, "content-wrapper")) #This is a dummy element
            )
        except:
             self.browser.quit()

        time.sleep(5)
        # print(self.browser.page_source.encode("utf-8"))
        while True:

            buttons_confirm = self.browser.find_elements_by_xpath("//button[contains(.,'Confirm')]")
            buttons_done = self.browser.find_elements_by_xpath("//button[contains(.,'Modify')]")
            # buttons_done = self.browser.find_elements_by_xpath("//button[normalize-space()='Modify']")

            print("Before confirmation : Confirm - {}      Done - {}".format(len(buttons_confirm), len(buttons_done)))

            if len(buttons_confirm):
                self.confirm_host_enter(buttons_confirm[0])
            else:
                break

            # if len(buttons_confirm) != 0:
            #     buttons_confirm[0].find_element_by_xpath('../../../..').screenshot(os.path.join(SCREENSHOTS, 'confirm.png'))
            # elif len(buttons_done) != 0:
            #     buttons_done[0].find_element_by_xpath('../../../..').screenshot(os.path.join(SCREENSHOTS, 'confirm.png'))

            # img1 = Image.open(os.path.join(SCREENSHOTS, 'confirm.png'))
            # # im1.show(title='confirm.png')

            # if len(buttons_confirm) != 0:
            #     button_index = 0;

            #     for button_confirm in buttons_confirm:
            #         self.confirm_host_enter(button_confirm)

            # buttons_confirm = self.browser.find_elements_by_xpath(self.xpath_of_button('btn-confirm'))
            # buttons_done = self.browser.find_elements_by_xpath(self.xpath_of_button('btn-configure'))

            # print("After confirmation  : Confirm - {}      Done - {}".format(len(buttons_confirm), len(buttons_done)))

            # if len(buttons_confirm) != 0:
            #     buttons_confirm[0].find_element_by_xpath('../../../..').screenshot(os.path.join(SCREENSHOTS, 'done.png'))
            # elif len(buttons_done) != 0:
            #     buttons_done[0].find_element_by_xpath('../../../..').screenshot(os.path.join(SCREENSHOTS, 'done.png'))

            # img2 = Image.open(os.path.join(SCREENSHOTS, 'done.png'))
            # # im2.show('done.png')

            # today = date.today()
            # Verti = np.concatenate((img1, img2), axis=0)
            # cv2.imwrite(os.path.join(SCREENSHOTS, '{}.png'.format(today.strftime("%Y_%m_%d"))), Verti)
            # # cv2.imshow('VERTICAL', Verti)


    def __del__(self):
        self.browser.close()

def remove_old_files(dir):
    now = time.time()
    for f in os.listdir(dir):
        fullpath = os.path.join(dir, f)
        # print('{} :  {} - {}'.format(fullpath, os.stat(fullpath).st_mtime, now - 864000))
        if os.stat(fullpath).st_mtime < (now - 864000):
            if os.path.isfile(fullpath):
                os.remove(fullpath)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--username',
                        required=True,
                        help='Username for the noip2 website.' )
    parser.add_argument('-p', '--password',
                        required=True,
                        help='Password for the noip2 website.' )
    args = parser.parse_args()

    noip2 = NOIP2(args.username, args.password)
    noip2.login()
    noip2.update_hosts()

if __name__ == '__main__':
    main()
    remove_old_files(SCREENSHOTS)
