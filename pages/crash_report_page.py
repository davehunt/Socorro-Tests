#!/usr/bin/env python
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

from pages.base_page import CrashStatsBasePage


class CrashReport(CrashStatsBasePage):

    _reports_tab_locator = (By.ID, 'reports')
    _results_count_locator = (By.CSS_SELECTOR, 'span.totalItems')
    _reports_row_locator = (By.CSS_SELECTOR, '#reports-list tbody tr')
    _report_tab_button_locator = (By.CSS_SELECTOR, '#panels-nav .reports')
    _summary_table_locator = (By.CSS_SELECTOR, '.content')

    def __init__(self, base_url, selenium):
        CrashStatsBasePage.__init__(self, base_url, selenium)
        WebDriverWait(self.selenium, self.timeout).until(lambda s: s.find_element(*self._summary_table_locator).is_displayed())

    @property
    def reports(self):
        return [self.Report(self.base_url, self.selenium, element) for element in self.selenium.find_elements(*self._reports_row_locator)]

    @property
    def results_count_total(self):
        return int(self.selenium.find_element(*self._results_count_locator).text.replace(",", ""))

    def click_reports_tab(self):
        self.selenium.find_element(*self._report_tab_button_locator).click()
        WebDriverWait(self.selenium, self.timeout).until(lambda s: len(self.reports))

    class Report(CrashStatsBasePage):

        _product_locator = (By.CSS_SELECTOR, 'td:nth-of-type(3)')
        _version_locator = (By.CSS_SELECTOR, 'td:nth-of-type(4)')
        _report_date_link_locator = (By.CSS_SELECTOR, '#reports-list a.external-link')

        def __init__(self, base_url, selenium, element):
            CrashStatsBasePage.__init__(self, base_url, selenium)
            self._root_element = element

        @property
        def product(self):
            return self._root_element.find_element(*self._product_locator).text

        @property
        def version(self):
            return self._root_element.find_element(*self._version_locator).text

        def click_report_date(self):
            self.selenium.find_element(*self._report_date_link_locator).click()
            from uuid_report import UUIDReport
            return UUIDReport(self.base_url, self.selenium)
