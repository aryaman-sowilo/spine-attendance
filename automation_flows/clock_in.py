"""Dedicated Selenium flow for performing a clock-in."""

from __future__ import annotations

from dataclasses import dataclass

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from automation_shared import (
    should_use_headless,
    setup_driver,
    login,
    go_to_attendance,
)

# Locators specific to the clock-in flow
CLOCK_IN_BUTTON_1 = (By.ID, "ctl00_BodyContentPlaceHolder_navMarkIn")
CLOCK_IN_BUTTON_2 = (By.ID, "ctl00_BodyContentPlaceHolder_btnAddNew")


def _perform_clock_in(driver, wait):
    """Execute the Selenium steps needed to clock in."""

    try:
        try:
            clock_in_btn = wait.until(EC.element_to_be_clickable(CLOCK_IN_BUTTON_1))
            clock_in_btn.click()
            print("First clock-in button clicked.")
        except Exception:
            print("First clock-in button not found, trying second button...")

        driver.implicitly_wait(0)
        clock_in_btn_2 = wait.until(EC.presence_of_element_located(CLOCK_IN_BUTTON_2))
        driver.execute_script("arguments[0].scrollIntoView(true);", clock_in_btn_2)
        driver.execute_script("arguments[0].click();", clock_in_btn_2)
        print("Second clock-in button clicked.")

        try:
            clock_in_btn_2 = wait.until(EC.presence_of_element_located(CLOCK_IN_BUTTON_2))
            driver.execute_script("arguments[0].click();", clock_in_btn_2)
            print("Second clock-in button clicked again for confirmation.")
        except Exception:
            print("No confirmation needed or button not found.")

    finally:
        driver.implicitly_wait(5)


@dataclass
class ClockInAutomation:
    """Encapsulates the Selenium session for clocking in."""

    headless: bool | None = None

    def run(self) -> dict:
        driver = None
        try:
            driver = setup_driver(headless_preference=should_use_headless(self.headless))
            wait = WebDriverWait(driver, 20)

            login(driver, wait)
            go_to_attendance(driver, wait)
            _perform_clock_in(driver, wait)

            return {
                "success": True,
                "message": "Clock-in completed successfully.",
            }

        except Exception as exc:
            if driver:
                driver.save_screenshot("error_clock_in.png")
            return {
                "success": False,
                "message": f"Clock-in failed: {exc}",
            }

        finally:
            if driver:
                driver.quit()
