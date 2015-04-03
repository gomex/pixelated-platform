#
# Copyright (c) 2014 ThoughtWorks, Inc.
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

from selenium.webdriver.common.by import By

from behave import *
from common import *
from .page_objects import LoginPage
from .page_objects import TagList

import time

@when(u'I visit the dispatcher')
def step_impl(context):
    login_page = LoginPage(context)
    login_page.open()

@then(u'I should see a login button')
def step_impl(context):
    login_page = LoginPage(context)
    assert login_page.has_login_button

@when(u'I login')
def step_impl(context):
    login_page = LoginPage(context)
    login_page.enter_username(random_username()).enter_password(random_password()).login()
    login_page.wait_intersitial_page()

@then(u'I see the inbox')
def step_impl(context):
    login_page = LoginPage(context)
    login_page.wait_intersitial_page()
    tag_list = TagList(context)
    assert tag_list.has_inbox_tag

@when(u'I logout')
def step_impl(context):
    context.browser.get(context.pixelated_url + 'auth/logout')

@when(u'I visit the signup page')
def step_impl(context):
    context.browser.get(context.leap_url + 'signup')

@then(u'I should see a signup button')
def step_impl(context):
    form = context.browser.find_element_by_name('button')

@when(u'I register')
def step_impl(context):
    fill_by_xpath(context, '//*[@name="user[login]"]', random_username())
    fill_by_xpath(context, '//*[@name="user[password]"]', random_password())
    fill_by_xpath(context, '//*[@name="user[password_confirmation]"]', random_password())
    context.browser.find_element_by_name("button").click()

@then(u'I see the control panel')
def step_impl(context):
    find_element_containing_text(context,'user control panel')
    context.browser.save_screenshot('/tmp/screenshot.png')
