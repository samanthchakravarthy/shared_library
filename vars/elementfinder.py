# Copyright 2008-2011 Nokia Networks
# Copyright 2011-2016 Ryan Tomac, Ed Manlove and contributors
# Copyright 2016-     Robot Framework Foundation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from robot.api import logger
from robot.utils import NormalizedDict
from selenium.webdriver.remote.webelement import WebElement

from SeleniumLibrary.base import ContextAware
from SeleniumLibrary.errors import ElementNotFound
from SeleniumLibrary.utils import escape_xpath_value, events, is_falsy
from selenium.common.exceptions import NoSuchElementException

from .customlocator import CustomLocator

import json
import boto3
import time
import os

class ElementFinder(ContextAware):

    def __init__(self, ctx):
        ContextAware.__init__(self, ctx)
        strategies = {
            'identifier': self._find_by_identifier,
            'id': self._find_by_id,
            'name': self._find_by_name,
            'xpath': self._find_by_xpath,
            'dom': self._find_by_dom,
            'link': self._find_by_link_text,
            'partial link': self._find_by_partial_link_text,
            'css': self._find_by_css_selector,
            'class': self._find_by_class_name,
            'jquery': self._find_by_sizzle_selector,
            'sizzle': self._find_by_sizzle_selector,
            'tag': self._find_by_tag_name,
            'scLocator': self._find_by_sc_locator,
            'default': self._find_by_default
        }
        self._strategies = NormalizedDict(initial=strategies, caseless=True,
                                          spaceless=True)
        self._default_strategies = list(strategies)
        self._key_attrs = {
            None: ['@id', '@name'],
            'a': ['@id', '@name', '@href',
                  'normalize-space(descendant-or-self::text())'],
            'img': ['@id', '@name', '@src', '@alt'],
            'input': ['@id', '@name', '@value', '@src'],
            'button': ['@id', '@name', '@value',
                       'normalize-space(descendant-or-self::text())']
        }

    def find(self, locator, tag=None, first_only=True, required=True,
             parent=None):
        element_type = 'Element' if not tag else tag.capitalize()
        if parent and not self._is_webelement(parent):
            raise ValueError('Parent must be Selenium WebElement but it '
                             'was {}.'.format(type(parent)))
        if self._is_webelement(locator):
            return locator
        prefix, criteria = self._parse_locator(locator)
        strategy = self._strategies[prefix]
        tag, constraints = self._get_tag_and_constraints(tag)
        elements = strategy(criteria, tag, constraints,
                            parent=parent or self.driver)
        if required and not elements:
            raise ElementNotFound("{} with locator '{}' not found."
                                  .format(element_type, locator))
        if first_only:
            if not elements:
                return None
            return elements[0]
        return elements

    def register(self, strategy_name, strategy_keyword, persist=False):
        strategy = CustomLocator(self.ctx, strategy_name, strategy_keyword)
        if strategy.name in self._strategies:
            raise RuntimeError("The custom locator '%s' cannot be registered. "
                               "A locator of that name already exists."
                               % strategy.name)
        self._strategies[strategy.name] = strategy.find
        if is_falsy(persist):
            # Unregister after current scope ends
            events.on('scope_end', 'current', self.unregister, strategy.name)

    def unregister(self, strategy_name):
        if strategy_name in self._default_strategies:
            raise RuntimeError("Cannot unregister the default strategy '%s'."
                               % strategy_name)
        if strategy_name not in self._strategies:
            raise RuntimeError("Cannot unregister the non-registered strategy '%s'."
                               % strategy_name)
        del self._strategies[strategy_name]

    def _is_webelement(self, element):
        # Hook for unit tests
        return isinstance(element, WebElement)

    def _disallow_webelement_parent(self, element):
        if self._is_webelement(element):
            raise ValueError('This method does not allow WebElement as parent')

    def _find_by_identifier(self, criteria, tag, constraints, parent):
        elements = self._normalize(parent.find_elements_by_id(criteria)) \
                   + self._normalize(parent.find_elements_by_name(criteria))
        return self._filter_elements(elements, tag, constraints)

    def _find_by_id(self, criteria, tag, constraints, parent):
        return self._filter_elements(parent.find_elements_by_id(criteria),
                                     tag, constraints)

    def _find_by_name(self, criteria, tag, constraints, parent):
        return self._filter_elements(parent.find_elements_by_name(criteria),
                                     tag, constraints)

    def _find_by_xpath(self, criteria, tag, constraints, parent):
        element = parent.find_elements_by_xpath(criteria)
        if len(element) > 0:
            # self._save('id', criteria, criteria + '1', parent)
            i = 0
        else:
            if os.environ['healEnabled'] == 'True':
                logger.console('Element not found and started healing')
                logger.console(criteria)
                t = time.localtime()
                current_time = time.strftime("%H:%M:%S", t)
                logger.console(current_time)
                element = self._heal('id', criteria, parent)
                t = time.localtime()
                current_time = time.strftime("%H:%M:%S", t)
                logger.console(current_time)
        return self._filter_elements(element, tag, constraints)

    def _find_by_dom(self, criteria, tag, constraints, parent):
        self._disallow_webelement_parent(parent)
        result = self.driver.execute_script("return %s;" % criteria)
        if result is None:
            return []
        if not isinstance(result, list):
            result = [result]
        return self._filter_elements(result, tag, constraints)

    def _find_by_sizzle_selector(self, criteria, tag, constraints, parent):
        self._disallow_webelement_parent(parent)
        js = "return jQuery('%s').get();" % criteria.replace("'", "\\'")
        return self._filter_elements(
            self.driver.execute_script(js),
            tag, constraints)

    def _find_by_link_text(self, criteria, tag, constraints, parent):
        return self._filter_elements(
            parent.find_elements_by_link_text(criteria),
            tag, constraints)

    def _find_by_partial_link_text(self, criteria, tag, constraints, parent):
        return self._filter_elements(
            parent.find_elements_by_partial_link_text(criteria),
            tag, constraints)

    def _find_by_css_selector(self, criteria, tag, constraints, parent):
        return self._filter_elements(
            parent.find_elements_by_css_selector(criteria),
            tag, constraints)

    def _find_by_class_name(self, criteria, tag, constraints, parent):
        return self._filter_elements(
            parent.find_elements_by_class_name(criteria),
            tag, constraints)

    def _find_by_tag_name(self, criteria, tag, constraints, parent):
        return self._filter_elements(
            parent.find_elements_by_tag_name(criteria),
            tag, constraints)

    def _find_by_sc_locator(self, criteria, tag, constraints, parent):
        self._disallow_webelement_parent(parent)
        js = "return isc.AutoTest.getElement('%s')" % criteria.replace("'", "\\'")
        return self._filter_elements([self.driver.execute_script(js)],
                                     tag, constraints)

    def _find_by_default(self, criteria, tag, constraints, parent):
        if tag in self._key_attrs:
            key_attrs = self._key_attrs[tag]
        else:
            key_attrs = self._key_attrs[None]
        xpath_criteria = escape_xpath_value(criteria)
        xpath_tag = tag if tag is not None else '*'
        xpath_constraints = self._get_xpath_constraints(constraints)
        xpath_searchers = ["%s=%s" % (attr, xpath_criteria) for attr in key_attrs]
        xpath_searchers.extend(self._get_attrs_with_url(key_attrs, criteria))
        xpath = "//%s[%s%s(%s)]" % (
            xpath_tag,
            ' and '.join(xpath_constraints),
            ' and ' if xpath_constraints else '',
            ' or '.join(xpath_searchers)
        )
        return self._normalize(parent.find_elements_by_xpath(xpath))

    def _get_xpath_constraints(self, constraints):
        xpath_constraints = [self._get_xpath_constraint(name, value)
                             for name, value in constraints.items()]
        return xpath_constraints

    def _get_xpath_constraint(self, name, value):
        if isinstance(value, list):
            return "@%s[. = '%s']" % (name, "' or . = '".join(value))
        else:
            return "@%s='%s'" % (name, value)

    def _get_tag_and_constraints(self, tag):
        if tag is None:
            return None, {}
        tag = tag.lower()
        constraints = {}
        if tag == 'link':
            tag = 'a'
        if tag == 'partial link':
            tag = 'a'
        elif tag == 'image':
            tag = 'img'
        elif tag == 'list':
            tag = 'select'
        elif tag == 'radio button':
            tag = 'input'
            constraints['type'] = 'radio'
        elif tag == 'checkbox':
            tag = 'input'
            constraints['type'] = 'checkbox'
        elif tag == 'text field':
            tag = 'input'
            constraints['type'] = ['date', 'datetime-local', 'email', 'month',
                                   'number', 'password', 'search', 'tel',
                                   'text', 'time', 'url', 'week', 'file']
        elif tag == 'file upload':
            tag = 'input'
            constraints['type'] = 'file'
        elif tag == 'text area':
            tag = 'textarea'
        return tag, constraints

    def _parse_locator(self, locator):
        if locator.startswith(('//', '(//')):
            return 'xpath', locator
        index = self._get_locator_separator_index(locator)
        if index != -1:
            prefix = locator[:index].strip()
            if prefix in self._strategies:
                return prefix, locator[index + 1:].lstrip()
        return 'default', locator

    def _get_locator_separator_index(self, locator):
        if '=' not in locator:
            return locator.find(':')
        if ':' not in locator:
            return locator.find('=')
        return min(locator.find('='), locator.find(':'))

    def _element_matches(self, element, tag, constraints):
        if not element.tag_name.lower() == tag:
            return False
        for name in constraints:
            if isinstance(constraints[name], list):
                if element.get_attribute(name) not in constraints[name]:
                    return False
            elif element.get_attribute(name) != constraints[name]:
                return False
        return True

    def _filter_elements(self, elements, tag, constraints):
        elements = self._normalize(elements)
        if tag is None:
            return elements
        return [element for element in elements
                if self._element_matches(element, tag, constraints)]

    def _get_attrs_with_url(self, key_attrs, criteria):
        attrs = []
        url = None
        xpath_url = None
        for attr in ['@src', '@href']:
            if attr in key_attrs:
                if url is None or xpath_url is None:
                    url = self._get_base_url() + "/" + criteria
                    xpath_url = escape_xpath_value(url)
                attrs.append("%s=%s" % (attr, xpath_url))
        return attrs

    def _get_base_url(self):
        url = self.driver.current_url
        if '/' in url:
            url = '/'.join(url.split('/')[:-1])
        return url

    def _normalize(self, elements):
        # Apparently IEDriver has returned invalid data earlier and recently
        # ChromeDriver has done sometimes returned None:
        # https://github.com/SeleniumHQ/selenium/issues/4555
        if not isinstance(elements, list):
            logger.debug("WebDriver find returned %s" % elements)
            return []
        return elements

    def _convertToJson(self, val):
        loaded_json = json.loads(val)
        i = len(loaded_json)
        reqItems = []
        while i > 5:
            element = loaded_json[i - 1]
            item = {}
            item['tag'] = element['tag']
            item['id'] = element['id']
            item['class'] = element['classes']
            if len(element['other']) > 0 and 'type' in element['other']:
                item['type'] = element['other']['type']
                # if 'id' in element:
                item['value'] = element['other']['value']
                if 'name' in element['other']:
                    item['name'] = element['other']['name']
            reqItems.append(item)
            i -= 1
        return reqItems

    def _save(self, source, value, dupValue, parent):
        str = open('1.js', 'r').read()
        # id = "//input[@" + source + "='" + value + "']"
        id = value
        val = parent.execute_script(str, parent.find_element_by_xpath(id))
        reqItems = self._convertToJson(val)
        self._insertItem(id, reqItems)
        # id = "//input[@" + source + "='" + dupValue + "']"
        id = value
        dupValue = id.split("'")[1]
        dupKey = id[0:-2]
        dupKey = dupKey + "1']"
        reqItems[0]['id'] = dupValue + "1"
        self._insertItem(dupKey, reqItems)

    def _insertItem(self, id, reqItems):
        # updating the DynamoDB table.
        item = {}
        item['id'] = id
        item['values'] = reqItems
        item['source'] = id
        dynamodb = boto3.setup_default_session(region_name='us-east-2')
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table('heal_xpath')
        table.put_item(
            Item=item
        )

    def _getItem(self, id):
        dynamodb = boto3.setup_default_session(region_name='us-east-2')
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table('heal_xpath')
        response = table.get_item(
            Key={
                'id': id
            }
        )

        if 'Item' in response:
            return response['Item']
        return []

    def _heal(self, source, value, parent):
        id = value
        item = self._getItem(id)
        if len(item) <= 0:
            return []
        Item = item['values'][0]
        xpath = "//input[("
        for i in Item.items():
            if i[0] != None and 'class' in i[0]:
                xpath1 = "contains(@" + i[0] + ",'" + i[1][0] + " " + i[1][1] + "')"
            if i[0] != None and 'value' in i[0]:
                xpath2 = "contains(@" + i[0] + ",'" + i[1] + "')"
            if i[0] != None and 'id' in i[0]:
                xpath3 = "contains(@" + i[0] + ",'" + i[1] + "')"
            if i[0] != None and 'name' in i[0]:
                xpath4 = "contains(@" + i[0] + ",'" + i[1] + "')"
        xpath = "//input[(" + xpath1 + " and " + xpath2 + " and " + xpath4 + " and " + xpath3 + ")]"
        elmt = self._getHealedElementByXPATH(xpath, parent)
        if elmt != '':
            logger.info("Element Found with healing", False)
            return self._compareLevels(item, elmt, parent)
        return None

    def _getHealedElementByXPATH(self, xpath, parent):
        elmt = ''
        try:
            elmt = parent.find_element_by_xpath(xpath)
            logger.console("Element found using class, value, name and id attributes.")
        except NoSuchElementException:
            lastIndex = xpath.rindex(' and')
            xpath = xpath[0:lastIndex] + ')]'
            try:
                elmt = parent.find_element_by_xpath(xpath)
                logger.console("Element found using class, value and name attributes.")
            except NoSuchElementException:
                lastIndex = xpath.rindex(' and')
                xpath = xpath[0:lastIndex] + ')]'
                try:
                    elmt = parent.find_element_by_xpath(xpath)
                    logger.console("Element found using class and value attributes.")
                except:
                    print("not able to find an element")
        return elmt

    def _compareLevels(self, item, elmt, parent):
        # str = open('1.js', 'r').read()
        str = """var items = [];
            var a = arguments[0];
            while (a != document) {
              var child = a;
              var i=0; while(child=child.previousElementSibling) i++;
              var node = {tag:null,id:null,index:null,classes:[],other:{},innerText:""};
              node.tag = a.tagName.toLowerCase();
              node.id = a.id;
              node.index = i;
              node.innerText = a.innerText;

              if (a.hasAttribute("class")) {
                  node.classes = a.attributes.class.value.split(' ');
              }
              for (index = 0; index < a.attributes.length; ++index) {
                  var attrName = a.attributes[index].name;
                  if (["id","class"].indexOf(attrName) == -1){
                        node.other[attrName] = a.attributes[index].value;
                  }
              };

              items.unshift(node);
              a = a.parentNode;
            }
            return JSON.stringify(items);"""
        val = parent.execute_script(str, elmt)
        reqItems = self._convertToJson(val)
        # verifying the parent elmets for class
        for i in range(1, len(item['values'])):
            if i <= int(os.environ['levels']):
                Item = item['values'][i]['class']
                reqItem = reqItems[i]['class']
                if Item != reqItem:
                    print("item not matched")
                    return
        logger.console("Verified parent levels " + os.environ['levels'])
        return [elmt]

