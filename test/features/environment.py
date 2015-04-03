#
# Copyright (c) 2015 ThoughtWorks, Inc.
#
# Pixelated is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Pixelated is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with Pixelated. If not, see <http://www.gnu.org/licenses/>.

from selenium import webdriver

import logging
import os

def before_scenario(context, scenario):
    context.browser = webdriver.Firefox()
    # context.browser = webdriver.PhantomJS(service_args=['--ignore-ssl-errors=yes'])
    context.browser.set_window_size(1280, 1024)
    context.browser.implicitly_wait(5)
    context.browser.set_page_load_timeout(60)  # wait for data
    context.browser.get(context.pixelated_url)

def after_scenario(context, scenario):
    context.browser.quit()

def take_screenshot(context):
    context.browser.save_screenshot('/tmp/screenshot.jpeg')

def save_source(context):
    with open('/tmp/source.html', 'w') as out:
        out.write(context.browser.page_source.encode('utf8'))

def before_all(context):
    logging.disable('INFO')

    context.pixelated_url = os.environ.get('PIXELATED_URL') or 'https://try.pixelated-project.org:8080/'
    context.leap_url = os.environ.get('LEAP_URL') or 'https://try.pixelated-project.org/'

    # get rid of this
    # context.browser = webdriver.PhantomJS(service_args=['--ignore-ssl-errors=yes'])
    # context.browser.set_window_size(1280, 1024)
    # context.browser.implicitly_wait(5)
    # context.browser.set_page_load_timeout(60)  # wait for data

    # create leap account
    # context.browser.get('https://staging.pixelated-project.org/signup')
    # fill_by_xpath(context, '//*[@name="user[login]"]', 'behave-testuser')
    # fill_by_xpath(context, '//*[@name="user[password]"]','Eido6aeg3za9ooNiekiemahm')
    # fill_by_xpath(context, '//*[@name="user[password_confirmation]"]', 'Eido6aeg3za9ooNiekiemahm')
    # context.browser.find_element_by_name("button").click()
    # context.browser.quit()
