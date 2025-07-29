from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import os
import ejobs.constants as const
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import time
from selenium.common.exceptions import StaleElementReferenceException
import csv
from unidecode import unidecode
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException, ElementNotInteractableException, TimeoutException


class Ejobs(webdriver.Firefox):
    def __init__(self,driver_path=r"D:\Sele",teardown = False):
        self.driver_path = driver_path
        self.teardown = teardown
        os.environ['PATH'] += os.pathsep + self.driver_path
        options = Options()
        options.set_preference("dom.webnotifications.enabled",False)
        super(Ejobs,self).__init__(options=options)
        self.implicitly_wait(10)
        self.maximize_window()

    def __exit__(self, exc_type, exc, traceback):
        if self.teardown:
            self.quit()

    def land_first_page(self):
        self.get(const.BASE_URL)   

    def cookies(self):
        close_cookies = self.find_element(
            By.CSS_SELECTOR,
            'button[data-test-id="accept-all-cookies-button"]'
            )
        close_cookies.click()

    def connect_account(self):
        connect_button = self.find_element(
            By.CSS_SELECTOR,
            'button[data-test-id="web-login-button"]'
        )
        connect_button.click()
    
    def connect_id(self,id):
        my_id = self.find_element(By.CLASS_NAME,"ejobs-basic-input__input")
        my_id.send_keys(id)
    
    def connect_password(self,password):
        my_password = self.find_element(
            By.CSS_SELECTOR,
            'input[placeholder="Parola"]'
        )
        my_password.send_keys(password)
    
    def login(self):
        login_button = self.find_element(By.CLASS_NAME,"LoginForm__Button")
        login_button.click()

    def jobs(self):
        jobs_button = self.find_element(
            By.XPATH,
            "//div[@class='layout-header__item' and text()='Joburi']"
        )
        jobs_button.click()

    def search_job(self,job_name):
        job_options = self.find_element(
            By.CSS_SELECTOR,
            'input[data-test-id="keywords-search-input"]'
        )
        job_options.send_keys(job_name)

    def search(self):
        search_button = self.find_element(
            By.CLASS_NAME,
            "jobs-list-search__button"
        )
        search_button.click()

    def job_place(self):
        bucuresti = self.find_element(
            By.XPATH,
            "//li[@class='jobs-list-filters-desktop-cities__item']//label[contains(., 'București')]//input[@type='checkbox']"
        )
        self.execute_script("arguments[0].click();", bucuresti)

        remote = self.find_element(
            By.XPATH,
            "//li[@class='jobs-list-filters-desktop-cities__item']//label[contains(., 'Remote (de acasă)')]//input[@type='checkbox']"
        )
        self.execute_script("arguments[0].click();",remote)

    def job_level(self):
        no_exp = self.find_element(
    By.XPATH,
    "//li[@class='jobs-list-filters-desktop-career-levels__item']//label[contains(.,'Fără experiență')]//input[@type='checkbox']"
)
        self.execute_script("arguments[0].click();",no_exp)
        
        entry_level = self.find_element(
            By.XPATH,
                "//li[@class='jobs-list-filters-desktop-career-levels__item']//label[contains(.,'Entry-Level')]//input[@type='checkbox']"
        )
        self.execute_script("arguments[0].click();",entry_level)
    
    
    def scroll_page(self):
        last_height = self.execute_script("return document.body.scrollHeight")
        while True:
                self.execute_script("window.scrollTo(0, document.body.scrollHeight);") 
                time.sleep(2)  
                new_height = self.execute_script("return document.body.scrollHeight")
                if new_height == last_height:
                    break
                last_height = new_height

    def total_jobs(self):
        self.scroll_page()

        filtrated_jobs = self.find_elements(By.CLASS_NAME,"job-card")
        print(f"nr joburi:{len(filtrated_jobs)}")

        jobs_data = []

        for job in filtrated_jobs:
            try:
                title_element = job.find_element(By.CLASS_NAME, "job-card-content-middle__title")
                title = unidecode(title_element.text)

                company = unidecode(job.find_element(By.CLASS_NAME,"job-card-content-middle__info").text)

                link_element = job.find_element(By.CLASS_NAME, "job-card-content__logo")
                link = link_element.get_attribute("href")
                
                print(f"{title} - {company} - {link}")
                
                jobs_data.append({"title":title, "company":company, "link":link})
            except StaleElementReferenceException:
                continue
            except Exception as e:
                print(f"Nu am putut extrage complet datele pentru un job:{e}")
                continue
            
        print(f"nr extrase:{len(jobs_data)}")
        return jobs_data


    def go_to_next_page(self):
            try:
                paginator_buttons = self.find_elements(By.CLASS_NAME, "jobs-list-paginator__button-text")

                for button in paginator_buttons:
                    if button.text.strip() == "Pagina următoare":
                        button.click()
                        time.sleep(2)
                        return True

                print("Nu exista pagina urmatoare")
                return False

            except Exception as e:
                print(f"Eroare la paginare: {e}")
                return False
            

  

class Bestjobs(webdriver.Firefox):
        def __init__(self, driver_path = r"D:\Sele", teardown = False):
            self.driver_path = driver_path
            self.teardown = teardown
            os.environ['PATH'] += os.pathsep + self.driver_path
            options = Options()
            options.set_preference("dom.webnotifications.enabled",False)
            super(Bestjobs,self).__init__(options=options)
            self.implicitly_wait(10)
            self.maximize_window()

        def __exit__(self, exc_type, exc, traceback):
            if self.teardown:
                self.quit()

        def best_land_first_page(self):
            self.get(const.BASE_URL_BEST) 

        def best_accecpt_cookies(self):
            best_cookie = self.find_element(
                By.CSS_SELECTOR,
                'button[data-test-id="cookie-consent-accept"]'
                )
            best_cookie.click()

        def best_login_button(self):
            login_button = self.find_element(
                By.CSS_SELECTOR,
                'a[data-test-id="navbar-login-button"]'
            )
            login_button.click()
        
        def press_login(self):
            press_login_button = self.find_element(
                By.CLASS_NAME,
                'tab-item.border.strong'
            )
            press_login_button.click()
        def best_log_id(self, id):
            my_id = self.find_element(By.ID,"login_form__username")
            my_id.send_keys(id)
        
        def best_log_password(self, password):
            my_password = self.find_element(By.ID,"login_form__password")
            my_password.send_keys(password)

        def succes_login(self):
            succes_login_button = self.find_element(By.ID,"login_form_submit")
            succes_login_button.click()
            
        def jobs_button(self):
            press_jobs_button = self.find_element(
                By.XPATH,
                "//a[@href='/locuri-de-munca']"
                )
            press_jobs_button.click()
        
        def input_job_text(self,best_job):
            my_job = self.find_element(By.ID,"navbar_keyword")
            my_job.send_keys(best_job)
            my_job.send_keys(Keys.ENTER)

        def select_location(self):
            location_button = self.find_element(By.XPATH,'//button[span[text()="Locație: Alege"]]')
            location_button.click()
        
        def select_bucharest(self):
            bucharest_button = self.find_element(
                By.XPATH,
                '//button[span[text()="București"]]'
            )
            bucharest_button.click()

        

        def best_filters(self):
            best_filters_button = self.find_element(
                By.CSS_SELECTOR,
                'button[data-test-id="cv-search-filters-button"]'
            )
            best_filters_button.click()
        
        def best_select_exp_filters(self):
           
            select_filter = self.find_element(
                By.XPATH,
                "//button[.//span[contains(text(), 'Experien')]]"
                )
            select_filter.click()
            

        def level_of_exp(self):
            my_level_0 = self.find_element(By.ID,"careerLevels-0")
            my_level_1 = self.find_element(By.ID, "careerLevels-1")
            my_level_0.click()
            my_level_1.click()
            apply_filter = self.find_element(
                By.XPATH,
                "//button[normalize-space()='Aplică filtre']"
            )
            apply_filter.click()
        
        def close_filtration(self):
            close_filtration_button = self.find_element(By.XPATH, '//button[contains(text(), "Aplică filtre")]')
            close_filtration_button.click()

        def scroll_page(self):
            last_height = self.execute_script("return document.body.scrollHeight")
            
            while True:
                try:
                    wait = WebDriverWait(self,5)
                    load_more_button = wait.until(
                        EC.element_to_be_clickable(
                           (By.XPATH,'//button[text()="Încarcă mai mult"]'))
                    )

                    self.execute_script("arguments[0].scrollIntoView(true);", load_more_button)
                    time.sleep(.5)
                    load_more_button.click()  
                    time.sleep(1)  
                except (NoSuchElementException, ElementClickInterceptedException, TimeoutException):
                      break
                
            while True:
                self.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(1)
                
                new_height = self.execute_script("return document.body.scrollHeight")
                if new_height == last_height:
                    break
                last_height = new_height


        def total_jobs(self):
            self.scroll_page()
            job_cards = self.find_elements(By.CLASS_NAME,'absolute.inset-0.z-1')
            print(f"nr joburi:{len(job_cards)}")

            jobs_data = []

            for job in job_cards:
             try:
                # title_element = job.find_element(
                #     By.CSS_SELECTOR,
                #     "h2.line-clamp-2.text-base.font-bold.leading-6"
                #             )
                # title = unidecode(title_element.text)

                # company = unidecode(job.find_element(By.CSS_SELECTOR,"div.mt-2.line-clamp-1.w-full.text-sm.text-ink-medium").text)
                link = job.get_attribute("href")
                
                print(f"{link}")
                
                jobs_data.append({"link":link})
             except Exception as e:
                 print(f"Nu am putut extrage complet datele pentru un job:{e}")
                 continue
            
            print(f"nr extrase:{len(jobs_data)}")
            return jobs_data
 