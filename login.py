import json
import time
from datetime import datetime
from selenium.webdriver.common.by import By
import login_gmail_selenium.common.constant as constant
from login_gmail_selenium.util import helper
from selenium.webdriver.common.action_chains import ActionChains
from getgmail import getgmail
import requests
import random
import openai
import re

FIRST_PAGE = 'FIRST_PAGE'
SIGNUP_PAGE = 'SIGNUP_PAGE'
CAPTCHA = 'CAPTCHA'
JOIN_AS_PAGE = 'JOIN_AS_PAGE'
SIGNUP_DATA_PAGE = 'SIGNUP_DATA_PAGE'
WELCOME_PAGE = 'WELCOME_PAGE'
EXPERIENCE_PAGE = 'EXPERIENCE_PAGE'
PROFILE_GOAL_PAGE = 'PROFILE_GOAL_PAGE'
WORK_PREFERENCE_PAGE = 'WORK_PREFERENCE_PAGE'
RESUME_IMPORT_PAGE = 'RESUME_IMPORT_PAGE'
TITLE_PAGE = 'TITLE_PAGE'
EMPLOYMENT_PAGE = 'EMPLOYMENT_PAGE'
EDUCATION_PAGE = 'EDUCATION_PAGE'
LANGUAGE_PAGE = 'LANGUAGE_PAGE'
SKILLS_PAGE = 'SKILLS_PAGE'
OVERVIEW_PAGE = 'OVERVIEW_PAGE'
CATEGORIES_PAGE = 'CATEGORIES_PAGE'
RATE_PAGE = 'RATE_PAGE'
LOCATION_PAGE = 'LOCATION_PAGE'
SUBMIT_PAGE = 'SUBMIT_PAGE'
FINISH_PAGE = 'FINISH_PAGE'
BEST_MATCH_PAGE = 'BEST_MATCH_PAGE'
LOGIN_PAGE = 'LOGIN_PAGE'
CERTIFICATION_PAGE = 'CERTIFICATION_PAGE'
PROPOSAL_PAGE = 'PROPOSAL_PAGE'
VERIFY_PAGE = 'VERIFY_PAGE'
CREATE_PAGE = 'CREATE_PAGE'

def get_fake_address_rand(fake_email_base, num):
    current_datetime = datetime.now()
    formatted_datetime = current_datetime.strftime("%Y%m%d%H%M%S")
    fake_email = fake_email_base.split('@')[0]
    fake_email += '+'
    fake_email += formatted_datetime+str(num)
    fake_email += '@'
    fake_email += fake_email_base.split('@')[1]
    return fake_email


def get_fake_address_rand_FEG(email):
    url = "https://api.products.aspose.app/email/api/FakeEmail/Generate"
    payload = {"email": email}
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    }
    response = requests.post(url, data=payload, headers=headers)
    print(response.json())
    try:
        response_data = response.json()
        generated_address = response_data.get('generatedAddress')
        if generated_address:
            return generated_address
        else:
            print("No 'generatedAddress' found in the JSON response:", response_data)
            return None
    except ValueError:
        print("Invalid JSON response:", response.text)
        return None


def data_load(i):
    with open(str(i)+'//data.json') as file:
        data = json.load(file)
    return data


class LoginUpwork:
    def __init__(self, driver, num):
        self.data = data_load(num)
        self.num = num
        self.driver = driver
        self.Set_Popup = self.data["set_popup"] == "True"
        self.Set_Notification = self.data["set_notification"] == "True"
        self.Save_Pass = self.data["save_pass"] == 'True'
        self.job_desc_text = ""
        self.last_page_url = ''
        self.last_page_url_count = 0
        self.refresh_count = 0
        self.proposal = 0
        self.bid = self.data["Bid"] == 'True'
        self.fake_address = ''

    def set_setting(self):
        if self.Set_Popup:
            self.set_popup()
        if self.Set_Notification:
            self.set_notification()
        if self.Save_Pass:
            self.save_pass_no()
    def save_pass_no(self):
        self.driver.get(constant.SAVE_PASS)
        time.sleep(1)
        try:
            element = helper.ensure_find_element(self.driver, By.CSS_SELECTOR, 'settings-ui')
            shadow_root = self.driver.execute_script('return arguments[0].shadowRoot', element)
            element = helper.ensure_find_element(shadow_root, By.ID, 'main')
            shadow_root = self.driver.execute_script('return arguments[0].shadowRoot', element)
            element = helper.ensure_find_element(shadow_root, By.CSS_SELECTOR, 'settings-basic-page')
            shadow_root = self.driver.execute_script('return arguments[0].shadowRoot', element)
            element = helper.ensure_find_element(shadow_root, By.CSS_SELECTOR, 'settings-autofill-page')
            shadow_root = self.driver.execute_script('return arguments[0].shadowRoot', element)
            element = helper.ensure_find_element(shadow_root, By.ID, 'passwordSection')
            shadow_root = self.driver.execute_script('return arguments[0].shadowRoot', element)
            element = helper.ensure_find_element(shadow_root, By.ID, 'passwordToggle')
            if element.get_attribute("checked"):
                element.click()
            return True
        except Exception:
            helper.refresh_page(self.driver)
            return False


    def set_notification(self):
        self.driver.get(constant.SET_NOT)
        time.sleep(1)
        try:
            element = helper.ensure_find_element(self.driver, By.CSS_SELECTOR, 'settings-ui')
            shadow_root = self.driver.execute_script('return arguments[0].shadowRoot', element)
            element = helper.ensure_find_element(shadow_root, By.ID, 'main')
            shadow_root = self.driver.execute_script('return arguments[0].shadowRoot', element)
            element = helper.ensure_find_element(shadow_root, By.CSS_SELECTOR, 'settings-basic-page')
            shadow_root = self.driver.execute_script('return arguments[0].shadowRoot', element)
            element = helper.ensure_find_element(shadow_root, By.CSS_SELECTOR, 'settings-privacy-page')
            shadow_root = self.driver.execute_script('return arguments[0].shadowRoot', element)
            helper.ensure_click(shadow_root, By.CSS_SELECTOR, 'settings-collapse-radio-button['
                                                              'label="Don\'t allow sites to send '
                                                              'notifications"]')
            return True
        except Exception:
            helper.refresh_page(self.driver)
            return False

    def set_popup(self):
        self.driver.get(constant.SET_POP)
        time.sleep(1)
        try:
            element = helper.ensure_find_element(self.driver, By.CSS_SELECTOR, 'settings-ui')
            shadow_root = self.driver.execute_script('return arguments[0].shadowRoot', element)
            element = helper.ensure_find_element(shadow_root, By.ID, 'main')
            shadow_root = self.driver.execute_script('return arguments[0].shadowRoot', element)
            element = helper.ensure_find_element(shadow_root, By.CSS_SELECTOR, 'settings-basic-page')
            shadow_root = self.driver.execute_script('return arguments[0].shadowRoot', element)
            element = helper.ensure_find_element(shadow_root, By.CSS_SELECTOR, 'settings-privacy-page')
            shadow_root = self.driver.execute_script('return arguments[0].shadowRoot', element)
            element = helper.ensure_find_element(shadow_root, By.CSS_SELECTOR, 'settings-category-default-radio-group')
            shadow_root = self.driver.execute_script('return arguments[0].shadowRoot', element)
            helper.ensure_click(shadow_root, By.ID, 'enabledRadioOption')
            return True
        except Exception:
            helper.refresh_page(self.driver)
            return False

    def recognize_page(self):
        try:
            current_url = self.driver.current_url.split('?')[0]
            print(current_url)
        except:
            curren_url = ""
        if current_url == constant.UPWORK_URL_2 or current_url == constant.UPWORK_URL:
            if helper.ensure_wait_for_element(self.driver, By.ID, 'visitor-v2-top-navigation-container'):
                print(FIRST_PAGE)
                return FIRST_PAGE
            elif helper.ensure_wait_for_element(self.driver, By.CSS_SELECTOR, "div.ray-id"):
                print(CAPTCHA)
                return CAPTCHA
        elif current_url == constant.SIGNUP_URL:
            if helper.ensure_wait_for_element(self.driver, By.CSS_SELECTOR, 'h2.display-rebrand.mt-20.pb-5'):
                return JOIN_AS_PAGE
            else:
                return SIGNUP_DATA_PAGE
        elif current_url.find(constant.LOGIN_URL) > -1:
            return LOGIN_PAGE
        elif current_url == constant.WELCOME_URL:
            return WELCOME_PAGE
        elif current_url.find(constant.EXPERIENCE_URL) > -1:
            return EXPERIENCE_PAGE
        elif current_url.find(constant.PROFILE_GOAL_URL) > -1:
            return PROFILE_GOAL_PAGE
        elif current_url.find(constant.WORK_PREFERENCE_URL) > -1:
            return WORK_PREFERENCE_PAGE
        elif current_url.find(constant.RESUME_IMPORT_URL) > -1:
            return RESUME_IMPORT_PAGE
        elif current_url.find(constant.TITLE_URL) > -1:
            return TITLE_PAGE
        elif current_url.find(constant.EMPLOYMENT_URL) > -1:
            return EMPLOYMENT_PAGE
        elif current_url.find(constant.EDUCATION_URL) > -1:
            return EDUCATION_PAGE
        elif current_url.find(constant.LANGUAGE_URL) > -1:
            return LANGUAGE_PAGE
        elif current_url.find(constant.SKILLS_URL) > -1:
            return SKILLS_PAGE
        elif current_url.find(constant.OVERVIEW_URL) > -1:
            return OVERVIEW_PAGE
        elif current_url.find(constant.CATEGORIES_URL) > -1:
            return CATEGORIES_PAGE
        elif current_url.find(constant.RATE_URL) > -1:
            return RATE_PAGE
        elif current_url.find(constant.LOCATION_URL) > -1:
            return LOCATION_PAGE
        elif current_url.find(constant.SUBMIT_URL) > -1:
            return SUBMIT_PAGE
        elif current_url.find(constant.FINISH_URL) > -1:
            return FINISH_PAGE
        elif current_url.find(constant.BEST_MATCH_URL) > -1 or current_url.find(constant.MOST_RECENT_URL) > -1:
            return BEST_MATCH_PAGE
        elif current_url.find(constant.CERTIFICATION_URL) > -1:
            return CERTIFICATION_PAGE
        elif current_url.find(constant.PROPOSAL_URL) > -1:
            return PROPOSAL_PAGE
        elif current_url.find(constant.VERIFY_URL)> -1:
            return VERIFY_PAGE
        elif current_url.find(constant.CREATE_PROFILE) > -1:
            return CREATE_PAGE
        elif current_url.find(constant.SEARCH_URL) > -1:
            return BEST_MATCH_PAGE
        else:
            helper.refresh_page(self.driver)
            time.sleep(5)
            print('Other URL')
            print(current_url)
            if 'upwork' not in current_url:
                self.driver.get(constant.UPWORK_URL)

    def act_on_page(self, page_id):
        if page_id == CAPTCHA:
            self.act_on_page_captcha()
        elif page_id == FIRST_PAGE:
            self.act_on_first_page()
        elif page_id == JOIN_AS_PAGE:
            self.act_on_join_as_page()
        elif page_id == LOGIN_PAGE:
            self.act_on_login_page()
        elif page_id == SIGNUP_DATA_PAGE:
            self.act_on_signup_data_page()
        elif page_id == VERIFY_PAGE:
            self.act_on_verify()
        elif page_id == WELCOME_PAGE:
            self.act_on_welcome_page()
        elif page_id == EXPERIENCE_PAGE:
            self.act_on_experience_page()
        elif page_id == PROFILE_GOAL_PAGE:
            self.act_on_profile_goal_page()
        elif page_id == WORK_PREFERENCE_PAGE:
            self.act_on_work_preference_page()
        elif page_id == RESUME_IMPORT_PAGE:
            self.act_on_resume_import_page()
        elif page_id == TITLE_PAGE:
            self.act_on_title_page()
        elif page_id == EMPLOYMENT_PAGE:
            self.act_on_employment_page()
        elif page_id == EDUCATION_PAGE:
            self.act_on_education_page()
        elif page_id == LANGUAGE_PAGE:
            self.act_on_language_page()
        elif page_id == SKILLS_PAGE:
            self.act_on_skills_page()
        elif page_id == OVERVIEW_PAGE:
            self.act_on_overview_page()
        elif page_id == CATEGORIES_PAGE:
            self.act_on_categories_page()
        elif page_id == RATE_PAGE:
            self.act_on_rate_page()
        elif page_id == LOCATION_PAGE:
            self.act_on_location_page()
        elif page_id == SUBMIT_PAGE:
            self.act_on_submit_page()
        elif page_id == FINISH_PAGE:
            self.act_on_finish_page()
        elif page_id == CREATE_PAGE:
            helper.ensure_click(self.driver, By.XPATH, "//button[@data-qa='get-started-btn']")
        elif page_id == BEST_MATCH_PAGE:
            data = data_load(self.num)
            self.bid = data["Bid"] == 'True'
            if self.bid:
                self.act_on_best_match_page()
            else:
                self.act_on_best_match_page_1()
        elif page_id == CERTIFICATION_PAGE:
            self.act_on_certification_page()
        elif page_id == PROPOSAL_PAGE:
            self.act_on_proposal_page()
        else:
            time.sleep(10)

    def act_on_first_page(self):
        print("act_on_first_page")
        helper.ensure_click(self.driver, By.XPATH,
                            '//a[@href="/nx/signup/" and contains(@class, "up-n-link") and contains('
                            '@class, "air3-btn") and contains(@class, "air3-btn-primary") and '
                            'contains(@class, "mr-0") and contains(@class, "mb-0") and contains('
                            '@class, "d-none") and contains(@class, "d-lg-inline-flex") and contains('
                            '@class, "vs-text-default")]')

    def act_on_page_captcha(self):
        print('Captcha Action')
        time.sleep(1)
        self.driver.execute_script("window.open('https://upwork.com', '_blank')")
        print("Captcha Required")
        time.sleep(120)
        self.driver.switch_to.window(self.driver.window_handles[1])
        self.driver.execute_script("window.close()")
        self.driver.switch_to.window(self.driver.window_handles[0])
        self.driver.get(constant.UPWORK_URL)
        helper.refresh_page(self.driver)

    def act_on_join_as_page(self):
        helper.ensure_click(self.driver, By.CSS_SELECTOR, 'div[data-cy="button-box"][data-qa="work"]')
        time.sleep(1)
        helper.ensure_click(self.driver, By.CSS_SELECTOR, 'button[data-qa="btn-apply"]')

    def act_on_signup_data_page(self):
        helper.type_text(self.driver, self.data["First_Name"], By.ID, 'first-name-input')
        helper.type_text(self.driver, self.data["Last_Name"], By.ID, 'last-name-input')
        self.fake_address = get_fake_address_rand(self.data["Email_Address"], self.num)
        helper.type_text(self.driver, self.fake_address, By.ID, 'redesigned-input-email')
        helper.type_text(self.driver, self.data["password"], By.ID, 'password-input')
        time.sleep(1)
        helper.ensure_click(self.driver, By.CSS_SELECTOR, 'div.up-dropdown-toggle-title')
        time.sleep(1)
        element = helper.ensure_find_element(self.driver, By.CSS_SELECTOR, 'div.up-dropdown-menu-container')
        element = helper.ensure_find_element(element, By.XPATH, './/input')
        ActionChains(self.driver).click(element).perform()
        element.send_keys(self.data["country"])
        time.sleep(1)
        element = helper.ensure_find_element(self.driver, By.ID, 'country-dropdown')
        helper.ensure_click(element, By.XPATH, './/li')
        time.sleep(2)
        helper.ensure_click(self.driver, By.XPATH, "//fieldset/div[2]")
        time.sleep(2)
        helper.ensure_click(self.driver, By.ID, 'button-submit-form')
        time.sleep(5)
        verify_address = getgmail(self.data["proxy_host"], self.data["proxy_port"], self.fake_address, self.num)
        print('verify_address', verify_address)
        self.driver.get(verify_address)

    def act_on_login_page(self):
        self.driver.get(constant.SIGNUP_URL)

    def act_on_verify(self):
        verify_address = getgmail(self.data["proxy_host"], self.data["proxy_port"], self.fake_address, self.num)
        time.sleep(10)
        print('verify_address', verify_address)
        self.driver.get(verify_address)

    def act_on_welcome_page(self):
        helper.ensure_click(self.driver, By.XPATH, "//button[@data-qa='get-started-btn']")

    def act_on_experience_page(self):
        helper.ensure_click(self.driver, By.XPATH, '//button[@data-test="skip-button"]')
        # helper.ensure_click(self.driver, By.XPATH, '//input[@value="FREELANCED_BEFORE"]')
        # helper.ensure_click(self.driver, By.XPATH, "//button[@data-test='next-button']")

    def act_on_profile_goal_page(self):
        # helper.ensure_click(self.driver, By.XPATH, '//input[@value="MAIN_INCOME"]')
        # helper.ensure_click(self.driver, By.XPATH, '//input[@type="radio" and @aria-labelledby="button-box-7" and @name="radio-group-167" and @data-ev-label="button_box_radio" and @class="air3-btn-box-input" and @value="MAIN_INCOME"]')
        helper.ensure_click(self.driver, By.XPATH, '//button[@data-test="skip-button"]')

    def act_on_work_preference_page(self):
        helper.ensure_click(self.driver, By.XPATH, '//button[@data-test="skip-button"]')

    def act_on_title_page(self):
        element = helper.ensure_find_element(self.driver, By.TAG_NAME, 'input')
        if element:
            element.clear()
            element.send_keys(self.data["PROFESSIONAL_ROLE"])
        helper.ensure_click(self.driver, By.XPATH, "//button[@data-test='next-button']")

    def act_on_resume_import_page(self):
        helper.ensure_click(self.driver, By.XPATH, '//button[contains(., "Upload your resume")]')
        try:
            helper.ensure_find_element(self.driver, By.XPATH, '//input[@type="file"]').send_keys(constant.CWD + '//' + str(self.num) + self.data["RESUME_ADDRESS"])
            time.sleep(10)
        except:
            pass
        helper.ensure_click(self.driver, By.XPATH, '//button[contains(., "Continue")]')
        time.sleep(3)
        helper.ensure_click(self.driver, By.XPATH, '//button[contains(., "Continue")]')

    def act_on_employment_page(self):
        helper.ensure_click(self.driver, By.XPATH, "//button[@data-test='next-button']")

    def act_on_education_page(self):
        #helper.ensure_click(self.driver, By.XPATH, "//button[@data-test='next-button']")
        helper.ensure_click(self.driver, By.XPATH, '//button[@data-test="skip-button"]')
        helper.ensure_click(self.driver, By.XPATH, "//button[@data-test='next-button']")

    def act_on_certification_page(self):
        helper.ensure_click(self.driver, By.XPATH, '//button[@data-test="skip-button"]')

    def act_on_language_page(self):
        helper.ensure_click(self.driver, By.XPATH, "//button[@data-test='next-button']")

    def act_on_skills_page(self):
        for MY_SKILL in self.data["MY_SKILLS"]:
            helper.type_text(self.driver, MY_SKILL, By.TAG_NAME, "input")
            time.sleep(2)
            li_parent = helper.ensure_find_element(self.driver, By.XPATH, "//div[@auto-scroll='window']")
            if not helper.ensure_click(li_parent, By.XPATH, './/li'):
                helper.ensure_click(self.driver, By.CSS_SELECTOR, "button[data-qa='clear-button']")
        # helper.refresh_page(self.driver)
        time.sleep(2)
        helper.ensure_click(self.driver, By.XPATH, "//button[@data-test='next-button']")

    def act_on_overview_page(self):
        helper.type_text(self.driver, self.data["OVERVIEW"], By.TAG_NAME, 'textarea')
        helper.ensure_click(self.driver, By.XPATH, "//button[@data-test='next-button']")

    def act_on_categories_page(self):
        helper.ensure_click(self.driver, By.CSS_SELECTOR,
                            'div[data-ev-sublocation="!dropdown"].fe-cat-dropdown[is-nested="true"]')
        time.sleep(1)
        element = helper.ensure_find_element(self.driver, By.XPATH, "//div[@class='onb-fe-categories-step mt-7']")
        lists = element.find_elements(By.TAG_NAME, 'li')
        if len(lists) > 70:
            for CATEGORY in self.data["CATEGORIES"]:
                try:
                    lists[CATEGORY].click()
                    time.sleep(1)
                except:
                    raise
                time.sleep(0.3)
        helper.ensure_click(self.driver, By.XPATH, "//button[@data-test='next-button']")

    def act_on_rate_page(self):
        element = helper.ensure_find_element(self.driver, By.XPATH, '//input[@data-test="currency-input"]')
        if element.get_attribute("value") == '$0.00' or not element.get_attribute("value"):
            element.send_keys(str(self.data["RATE"]), By.TAG_NAME, 'input')
        helper.ensure_click(self.driver, By.XPATH, "//button[@data-test='next-button']")

    def act_on_location_page(self):
        helper.ensure_click(self.driver, By.XPATH, "//button[@aria-label='Upload photo']")
        try:
            helper.ensure_find_element(self.driver, By.XPATH, '//input[@type="file"]').send_keys(constant.CWD + '//' + str(self.num) + self.data["PHOTO_ADDRESS"])
            helper.ensure_click(self.driver, By.XPATH, "//button[contains(text(), 'Attach photo')]")
        except:
            pass
        time.sleep(1)
        helper.type_text(self.driver, self.data["street"], By.CSS_SELECTOR, 'input[aria-labelledby="street-label"]')
        element = helper.ensure_find_element(self.driver, By.CSS_SELECTOR, 'input[aria-labelledby="city-label"]')
        element.click()
        ActionChains(self.driver).click(element).perform()
        try:
            element.send_keys(self.data["city"])
        except:
            pass
        # element.click()
        time.sleep(3)
        element = helper.ensure_find_element(self.driver, By.CLASS_NAME, "up-fe-location-step")
        if not helper.ensure_click(element, By.XPATH, './/li'):
            helper.ensure_click(self.driver, By.CSS_SELECTOR, "button[data-qa='clear-button']")
        helper.type_text(self.driver, self.data["phone_number"], By.CSS_SELECTOR, 'input[placeholder="Enter number"]')
        helper.ensure_click(self.driver, By.XPATH, "//button[@data-test='next-button']")

    def act_on_submit_page(self):
        helper.ensure_click(self.driver, By.CSS_SELECTOR, 'button.air3-btn.air3-btn-primary.width-md.m-0')

    def act_on_finish_page(self):
        self.proposal = 50
        helper.ensure_click(self.driver, By.CSS_SELECTOR, 'a.up-n-link.air3-btn.air3-btn-primary')
        self.proposal = 50

    def save_email(self):
        if not self.bid:
            with open('dataout.txt', "a+") as file:
                file.write(self.fake_address + '\n')
        else:
            with open(str(self.num) + '// ' + 'dataout_bid.json', "a+") as file:
                file.seek(0)
                data = self.fake_address
                try:
                    existing_data = json.load(file)
                except json.JSONDecodeError:
                    existing_data = []
                existing_data.append(data)
                file.seek(0)
                json.dump(existing_data, file, indent=4)

    def act_on_best_match_page_1(self):
        self.save_email()
        time.sleep(2)
        self.act_on_proposal_modal_best()
        self.act_on_proposal_modal()
        modal = helper.ensure_find_element(self.driver, By.CLASS_NAME, "up-modal-dialog")
        if modal:
            helper.ensure_click(modal, By.TAG_NAME, 'button')
        self.act_on_proposal_modal_best()
        modal = helper.ensure_find_element(self.driver, By.CLASS_NAME, "up-modal-dialog")
        if modal:
            helper.ensure_click(modal, By.TAG_NAME, 'button')
        self.act_on_proposal_modal_best()
        element = helper.ensure_find_element(self.driver, By.XPATH, '//nav/ul/li[9]')
        helper.ensure_click(element, By.TAG_NAME, "button")
        helper.ensure_click(element, By.XPATH, "./ul/li[4]/ul/li[2]/button")

    def act_on_best_match_page(self):
        time.sleep(3)
        data = data_load(self.num)
        self.act_on_proposal_modal_best()
        if self.proposal == 50:
            self.save_email()
            time.sleep(2)
            modal = helper.ensure_find_element(self.driver, By.CLASS_NAME, "up-modal-dialog")
            time.sleep(3)
            if modal:
                helper.ensure_click(modal, By.TAG_NAME, 'button')
            self.act_on_proposal_modal_best()
            # helper.ensure_click(self.driver, By.CSS_SELECTOR,
            #                     'button[type="button"][role="tab"][data-test="tab-most-recent"]')
            modal = helper.ensure_find_element(self.driver, By.CLASS_NAME, "up-modal-dialog")
            time.sleep(3)
            if modal:
                helper.ensure_click(modal, By.TAG_NAME, 'button')
            # helper.ensure_click(self.driver, By.CSS_SELECTOR,
            #                     'button[type="button"][role="tab"][data-test="tab-most-recent"]')
            time.sleep(5)
            helper.execute_with_retry(self.driver, self.driver.get("https://www.upwork.com/nx/jobs/search/?q=%28"+data["MY_SKILLS"][0]+
                                                                   "%20OR%20" + data["MY_SKILLS"][1] + "%20OR%20" + data["MY_SKILLS"][2] + 
                                                                   "%20OR%20" + data["MY_SKILLS"][3]+ "%29&sort=recency"))
            time.sleep(5)
            job_title = helper.ensure_find_element(self.driver, By.XPATH, '//div[@data-test="job-tile-list"]')

            try:
                jobs = job_title.find_elements(By.XPATH, './section')
            except:
                pass
            for job in jobs:
                price = helper.ensure_find_element(job, By.XPATH, './div[2]')
                price_text = price.text
                if price_text[0] == 'F':
                    try:
                        budget_regex = r"\$([\d,]+)"
                        matches = int(re.findall(budget_regex, price_text)[0])
                        try:
                            fixed_price = data["Fixed_Price"]
                        except:
                            fixed_price = 300
                        if matches < fixed_price:
                            continue
                    except:
                        pass
                if price_text[0] == 'H':
                    try:
                        budget_regex = r"\$([\d,]+)"
                        matches = int(re.findall(budget_regex, price_text)[1])
                        try:
                            hourly_rate = data["Hourly_Rate"]
                        except:
                            hourly_rate = 20
                        if matches < hourly_rate:
                            continue
                    except:
                        pass
                try:
                    job.click()
                    time.sleep(20)
                    job_desc = helper.ensure_find_element(self.driver, By.CSS_SELECTOR,
                                                          'div.job-description.break.mb-0')
                    self.job_desc_text = job_desc.text
                    helper.ensure_click(self.driver, By.XPATH, '//aside/div/div/div/div/span/span/button')
                    time.sleep(20)
                    helper.refresh_page(self.driver)
                    self.driver.switch_to.window(self.driver.window_handles[1])
                except:
                    pass
        else:
            modal = helper.ensure_find_element(self.driver, By.CLASS_NAME, "up-modal-dialog")
            if modal:
                helper.ensure_click(modal, By.TAG_NAME, 'button')
            self.act_on_proposal_modal()
            self.act_on_proposal_modal_best()
            modal = helper.ensure_find_element(self.driver, By.CLASS_NAME, "up-modal-dialog")
            if modal:
                helper.ensure_click(modal, By.TAG_NAME, 'button')
            self.act_on_proposal_modal()
            self.act_on_proposal_modal_best()
            element = helper.ensure_find_element(self.driver, By.XPATH, '//nav/ul/li[9]')
            helper.ensure_click(element, By.TAG_NAME, "button")
            helper.ensure_click(element, By.XPATH, "./ul/li[4]/ul/li[2]/button")
            self.driver.get(constant.SIGNUP_URL)

    def act_on_proposal_page(self):
        # helper.ensure_find_element(self.driver, By.CSS_SELECTOR, 'button[aria-describedby="popper_125"]').click()
        # time.sleep(5)
        self.act_on_proposal_modal()
        time.sleep(3)
        self.act_on_proposal_modal()
        # helper.ensure_find_element(self.driver, By.CSS_SELECTOR, 'button[aria-describedby="popper_125"]').click()
        # time.sleep(5)
        self.act_on_proposal_modal()
        time.sleep(3)
        try:
            self.act_on_boost_proposal()
        except:
            pass
        try:
            self.act_on_bid_additional_detail()
        except:
            pass
        try:
            self.act_on_terms()
        except:
            pass
        try:
            self.act_on_duration()
        except:
            pass

        helper.ensure_click(self.driver, By.XPATH, '//button[@type="button"][@class="up-btn up-btn-primary m-0"]')
        time.sleep(10)
        self.act_on_proposal_modal()
        time.sleep(10)
        self.act_on_proposal_modal()
        time.sleep(10)
        self.act_on_proposal_modal()
        time.sleep(10)
        self.act_on_proposal_modal()
        self.driver.execute_script("window.close()")
        self.driver.switch_to.window(self.driver.window_handles[0])
        time.sleep(2)
        self.driver.get(constant.BEST_MATCH_URL)
        time.sleep(2)
        element = helper.ensure_find_element(self.driver, By.XPATH, '//nav/ul/li[9]')
        helper.ensure_click(element, By.TAG_NAME, "button")
        helper.ensure_click(element, By.XPATH, "./ul/li[4]/ul/li[2]/button")
        self.proposal = 0
        self.driver.get(constant.SIGNUP_URL)

    def act_on_terms(self):
        term = helper.ensure_find_element(self.driver, By.XPATH, '//div[@class="fe-proposal-job-terms"]')
        helper.ensure_click(term, By.XPATH, '//fieldset/div[@class="up-radio"][2]')

    def act_on_duration(self):
        duration = helper.ensure_find_element(self.driver, By.XPATH, '//div[@class="fe-proposal-job-estimated-duration"]')
        helper.ensure_click(duration, By.XPATH, '//div[@data-test="dropdown-toggle"]')
        time.sleep(3)
        helper.ensure_click(duration, By.XPATH, '//div[@class="up-menu-container"]//li[4]')
        time.sleep(3)
        helper.ensure_click(duration, By.XPATH, '//div[@data-test="dropdown-toggle"]')
        time.sleep(3)
        helper.ensure_click(duration, By.XPATH, '//div[@class="up-menu-container"]//li[4]')
        time.sleep(3)
        helper.ensure_click(duration, By.XPATH, '//div[@data-test="dropdown-toggle"]')
        time.sleep(3)
        helper.ensure_click(duration, By.XPATH, '//div[@class="up-menu-container"]//li[4]')

    def chatgpt_get(self, question):
        data = data_load(self.num)
        openai.api_key = data["OPENAI_API"]
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": data["OPENAI_SYSTEM_ROLE"]},
                {"role": "assistant", "content": self.job_desc_text},
                {"role": "user", "content": question}
            ]
        )
        ans = response['choices'][0]['message']['content']
        ans = ans.replace('[Company Name]', 'your company')
        ans = ans.replace('[X years]', str(random.randint(5, 10))+' years')
        ans = ans.replace('[Your Name]', data["First_Name"])
        ans = ans.replace('[Recipient\'s Name]', 'Client')
        ans = ans.replace('Hiring Manager', 'Client')
        ans = re.sub(r"\[.*?\]", "", ans)
        ans = re.sub(r"\n\s*\n", r"\n", ans)
        return ans

    def act_on_bid_additional_detail(self):
        additional_details = helper.ensure_find_element(self.driver, By.XPATH, '//div[@class="fe-proposal-additional-details additonal-details"]')
        ans = self.chatgpt_get(self.data["OPENAI_USER_ROLE"])
        #ans = self.data["Cover_Letter"]
        helper.type_text(additional_details, ans, By.XPATH, './div/section/div//textarea')
        ques_area = helper.ensure_find_element(additional_details, By.XPATH, './div/section/div[2]')
        ques_areas = ques_area.find_elements(By.XPATH, './div')
        for ques_area in ques_areas:
            try:
                ques = helper.ensure_find_element(ques_area, By.XPATH, './label').text
                ans = self.chatgpt_get(self.data["OPENAI_USER_ROLE_1"] + ',' + ques)
                helper.type_text(ques_area, ans, By.XPATH, './div/textarea')
            except:
                pass
    def act_on_boost_proposal(self):
        helper.ensure_click(self.driver, By.XPATH,
                            '//div[@class="fe-proposal-boost-proposal"]//div[@class="cta-wrapper"]/button')
        helper.type_text(self.driver,  50,  By.XPATH,
                            '//div[@class="bidding-box"]//div[@class="up-input-group"]//input')

        helper.ensure_click(self.driver, By.XPATH,
                                   '//div[@class="bidding-box"]//div[@class="up-input-group"]//button')

    def act_on_proposal_modal(self):
        modal = helper.ensure_find_element(self.driver, By.CSS_SELECTOR, "div.up-modal-dialog")
        if modal:
            helper.ensure_click(modal, By.CSS_SELECTOR, '.checkbox input[name="checkbox"]')
            helper.ensure_click(modal, By.CSS_SELECTOR, 'button.up-btn.up-btn-primary')

    def act_on_proposal_modal_best(self):
        modal = helper.ensure_find_element(self.driver, By.CSS_SELECTOR, "div.modal-body")
        time.sleep(3)
        if modal:
            helper.ensure_click(modal, By.CSS_SELECTOR, 'label.up-checkbox-label')
            time.sleep(3)
            helper.ensure_click(modal, By.TAG_NAME, 'button')

    def stun_action(self, page_id):
        currenturl = ' '
        try:
            currenturl = self.driver.current_url
        except:
            pass
        if self.last_page_url == currenturl:
            self.last_page_url_count = self.last_page_url_count + 1
        else:
            self.last_page_url_count = 0
        self.last_page_url = currenturl
        if self.last_page_url_count % 10 == 0 and self.last_page_url_count > 9:
            helper.refresh_page(self.driver)
            time.sleep(10)
            self.refresh_count = self.refresh_count + 1
        else:
            self.refresh_count = 0
        if self.refresh_count > 2:
            self.driver.get(constant.SIGNUP_URL)

    def main_func(self):
        try:
            page_id = self.recognize_page()
        except:
            page_id = "unrecognized page"
        print('page_id:', page_id)
        self.stun_action(page_id)
        try:
            self.act_on_page(page_id)
        except:
            pass
        time.sleep(1)

    def accept_cookies(self):
        helper.ensure_click(self.driver, By.ID, 'onetrust-accept-btn-handler')

    def start(self):
        self.set_setting()
        time.sleep(1)
        self.driver.get(constant.SIGNUP_URL)
        time.sleep(1)
        self.accept_cookies()
        while True:
            self.main_func()
            time.sleep(2)
