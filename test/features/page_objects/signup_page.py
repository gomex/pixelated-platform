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

from base_page_object import BasePageObject
from selenium.common.exceptions import TimeoutException


class SignupPage(BasePageObject):
    def __init__(self, context, timeout=10):
        self._context = context
        self._locators = {
            'username': 'input#srp_username',
            'password': 'input#srp_password',
            'password_confirmation': 'input#srp_password_confirmation',
            'signup_button': 'button[type=submit]'
        }
        super(SignupPage, self).__init__(context, timeout)

    def open(self):
        self._context.browser.get(self._context.leap_url + 'signup')
        return self

    def enter_username(self, username):
        self._username_field().send_keys(username)
        return self

    def enter_password(self, password):
        self._password_field().send_keys(password)
        self._password_confirmation_field().send_keys(password)
        return self

    def signup(self):
        self._signup_button().click()
        return self

    @property
    def has_signup_button(self):
        if (self._signup_button()):
            return True
        return False

    def _username_field(self):
        return self._find_element_by_locator(self._locators['username'])

    def _password_field(self):
        return self._find_element_by_locator(self._locators['password'])

    def _password_confirmation_field(self):
        return self._find_element_by_locator(self._locators['password_confirmation'])

    def _signup_button(self):
        return self._find_element_by_locator(self._locators['signup_button'])
