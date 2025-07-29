from ejobs.engine import Ejobs
from ejobs.engine import Bestjobs
import time
import csv
import os



if os.path.exists("ejobs_scraped.csv"):
    os.remove("ejobs_scraped.csv")

def save_to_csv(jobs_data, filename="jobs.csv"):
    if not jobs_data:
        print("Nu exista date de salvat")
        return
    keys = jobs_data[0].keys()
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=keys)
        writer.writeheader()
        writer.writerows(jobs_data)
    print(f"Datele au fost salvate in {filename}")

def scrape_ejobs():
    with Ejobs() as bot:
        bot.land_first_page()
        time.sleep(3)
        bot.cookies()
        bot.connect_account()
        bot.connect_id("vasilecristian2901@yahoo.com")
        bot.connect_password("Helmut2901")
        bot.login()
        time.sleep(5)
        bot.jobs()
        time.sleep(1)
        bot.search_job("contabil junior")
        time.sleep(1)
        bot.search()
        time.sleep(.5)
        bot.job_place()
        bot.job_level()
        time.sleep(1.5)
        all_jobs = []
        while True:
            jobs = bot.total_jobs()
            for job in jobs:
                job['source'] = 'Ejobs'
            all_jobs.extend(jobs)

            if not bot.go_to_next_page():
                break
        return all_jobs


def scrape_bestjobs():
    with Bestjobs() as best_bot:
        best_bot.best_land_first_page()
        time.sleep(1.6)
        best_bot.best_accecpt_cookies()
        time.sleep(1)
        best_bot.best_login_button()
        best_bot.press_login()
        best_bot.best_log_id("vasilecristian2901@gmail.com")
        best_bot.best_log_password("Helmut2901")
        best_bot.succes_login()
        time.sleep(1.5)
        best_bot.jobs_button()
        time.sleep(1.8)
        best_bot.select_location()
        time.sleep(1.2)
        best_bot.select_bucharest()
        time.sleep(3.3)
        best_bot.input_job_text("contabil junior")
        time.sleep(1.8)
        time.sleep(.3)
        best_bot.best_filters()
        time.sleep(1.8)
        best_bot.best_select_exp_filters()
        time.sleep(.5)
        best_bot.level_of_exp()
        time.sleep(1)
        best_bot.close_filtration()
        time.sleep(.5)
        best_bot.scroll_page()
        
        all_jobs = best_bot.total_jobs()
        for job in all_jobs:
            job['source'] = 'Bestjobs'
        return all_jobs

if __name__ == "__main__":
    jobs_ejobs = scrape_ejobs()
    jobs_bestjobs = scrape_bestjobs()


all_jobs = jobs_ejobs + jobs_bestjobs

save_to_csv(all_jobs, filename='all_jobs.csv')



    # while True:
    #     bot.total_jobs()
    #     if not bot.go_to_next_page():
    #         break