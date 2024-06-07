
import tqdm
import os
import shutil
from utils import PanoptoSession
from selenium.webdriver.common.by import By
import time



import warnings

warnings.filterwarnings('ignore', 'SettingWithCopyWarning')
warnings.simplefilter(action='ignore', category=FutureWarning)

def main():
    print(
"""
                      ░▓▓░   ░░                             
                       ░░    ▓▓                             
                   ░░       ░██░       ░░                   
                 ░░█▒░  ░██████████░  ░▒█░░                 
            ░▒░  ░░█▒░░     ░██░      ░▒█░░ ░░▒░            
             ▒     ░░        ▓▓        ░░    ░▒             
                    ░░░      ░░      ░░░                    
                 ▓███████▓░      ░▓███████▓                 
        ░▒▒░   ▒██▒░░░  ▒██▒░  ░▒██▒░░▒ ░▒██▒   ░▒▒░        
        ░███▓ ░██░░█▒    ░██░░░░██░░▓▓░▒█░░██░ ▓███░        
        ░▓░▓█▒▒█▒░▓░      ▒██████▒░█░░█░░  ▒█▒▒█▓░▓░        
         ░ ▒█▓░██░        ▓█▒░░▒█▓░░▓▓░   ░██░▓█▓ ░         
          ░▓██░▓█▓░     ░▒██░  ░▓█▓░     ░▓█▓░██▓░          
          ░████░░███▓▓▓███▒░    ░▒███▓▓▓███░░████░          
          ▒▒▒██░  ░▒▓▓▓▒░░        ░░▒▓▓▓▒░  ░██▒▒▒          
           ░███░       ░░░░      ░░░░       ░███░           
           ▒███░     ▒██████▒  ▒██████▒     ░███▒           
          ░██▒░    ▒████████████████████▒    ░▒██░          
         ░▓█████▓███████████▒░░▒███████████▓▓████▓░         
         ░███████████████▓░      ░▒███████████████░         
         ▓██▓███░░░░░░░     ░▓▓░     ░░░░░░░███▓██▓░        
        ░▓█░▓█████▓▓▓▓▓ ░  ▒████▒  ░ ▓▓▓▓▓█████▓░█▓░        
         ▒▓░███████████░▓░░██████░░█░███████████░▓▒         
          ░ █████████████▓▒██████▒▓█████████████ ░          
            ░██▒████████████████████████████▒██░            
             ▓█░████████████████████████████░█▓░            
             ░▓░▒██████████████████████████▒░▓░             
                 ▓██▒▓████████████████▓▒██▓                 
                 ░██▒░███▓▓███████▓███▒▒██░                 
                   ▒█░▒██▓▒██████▓▒██▒░█▒                   
                    ░░░░██░▓█████░▓█░ ░░                    
                         ▒▒░▓███░▒▒░                        
                             ▒▓                                             
""" )
    print("")
    print("www.canvaswizards.org.uk")
    print("")
    print("Welcome to the Canvas Wizards Caption Scaper Tool!")
    print("By Robert Treharne and Alan Radford, University of Liverpool. 2024")
    print("")

    # Ask user for panopto URL
    panopto_url = input("Please enter the Panopto folder URL: ")

    # Start Panopto Session
    panopto_session = PanoptoSession(panopto_url)

    # Breathe
    print("Breathe ...")
    time.sleep(10)

    # Get video URLs
    video_urls = get_video_urls(panopto_session)

    print(video_urls)

    for url in tqdm.tqdm(video_urls, desc="Getting transcripts ..."):
        video_urls[url]["transcript"] = get_transcript(panopto_session, url)

    # OK I now want to flatten my dictionary into a .csv file with the following headers:
    # video_url, date, time, transcript_url, transcript_text, transcript_timestamp
    # I will save this file as transcripts.csv
    with open("transcripts.tsv", "w") as f:
        f.write("video_url\tdate\ttime\ttranscript_url\tvideo_timestamp\ttranscript_text\ttranscript_timestamp\n")
        for url in video_urls:
            try:
                for t in video_urls[url]["transcript"]:
                    f.write(f"{url}\t{video_urls[url]['date']}\t{video_urls[url]['time']}\t{t[0]}\t{t[1]}\t{t[2]}\n")
            except:
                continue


def get_video_urls(panopto_session):
    # click button element with aria-label "Table view"
    table_view_button = panopto_session.browser.find_element(By.XPATH, "//button[@aria-label='Table view']")
    table_view_button.click()

    # Get all anchor elements on page with class "list-title"
    elements = panopto_session.browser.find_elements(By.CLASS_NAME, "list-title")

    video_urls = []
    dates = []
    times = []
    
    while True:     
        # Wait for 5 seconds
        print("wait ...")
        time.sleep(5)

        # Get all anchor elements on page with class "list-title"
        elements = panopto_session.browser.find_elements(By.CLASS_NAME, "list-title")

        for e in elements:
            if e.get_attribute("href"):
                video_urls.append(e.get_attribute("href"))

        datestamps = panopto_session.browser.find_elements(By.CLASS_NAME, "date-time-container")

        for dt in datestamps:
            # for each div in dt, get the text
            date = dt.find_elements(By.TAG_NAME, "div")[0].text
            t = dt.find_elements(By.TAG_NAME, "div")[1].text

            if date != '':
                dates.append(date)
                times.append(t)

        break
        # Find button element with aria label "Go to next page"
        try:
            next_page_button = panopto_session.browser.find_element(By.XPATH, "//button[@aria-label='Go to next page']")
            next_page_button.click()
        except:
            # exit while loop
            break
    
    data = {}

    for url, d, t in zip(video_urls, dates, times):
        data[url] = {"date": d, "time": t}
        
    return data

def get_transcript(panopto_session, video_url):
    panopto_session.browser.get(video_url)
    time.sleep(5)

    try:
        transcript_tab = transcript_tab = panopto_session.browser.find_element(By.ID, "transcriptTabHeader")
        transcript_tab.click()
    except:
        return None

    time.sleep(2)
    transcript_elements = panopto_session.browser.find_elements(By.CLASS_NAME, "event-text")
    transcript_timestamps = panopto_session.browser.find_elements(By.CLASS_NAME, "event-time")
    transcript = []

    for x, y in zip(transcript_timestamps, transcript_elements):
        print(f"{x.text} - {y.text}")
        try:
            minute = int(x.text.split(':')[0])
            second = int(x.text.split(':')[1])
        except:
            minute = 0
            second = 0

        transcript.append((f"{video_url}&start={minute*60 + second}", y.text, x.text))


    #except:
        #return None
        
    return transcript


if __name__ == "__main__":
    main()