import selenium
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd


def recherche_comm():
    suivant = True
    compteur = 0
    nom_hotel = driver.find_element(By.ID, "HEADING").text

    adresse = driver.find_element(By.XPATH,
                                  "/html/body/div[2]/div[1]/div/div[6]/div/div/div/div[2]/div/div[2]/div/div/div/span[2]/span").text
    note_global = driver.find_element(By.XPATH,
                                      '/html/body/div[2]/div[2]/div[2]/div[4]/div/div[1]/div[4]/div/div/div/div/div[2]/div[1]/div[1]/span').text
    info_hotel = [nom_hotel, adresse, note_global]
    info_comm = []
    while suivant == True:
        compteur += 1
        time.sleep(2)

        container = driver.find_elements(By.XPATH, "//div[@data-reviewid]")

        for j in range(len(container)):
            nom_auteur = container[j].find_element(By.XPATH, "../div[1]/div/div[2]/span/a").text
            try:
                note_comm = container[j].find_element(By.XPATH,
                                                      ".//span[contains(@class, 'ui_bubble_rating bubble_')]").get_attribute(
                    "class").split("_")[3]
            except:
                note_comm = ""
            try:
                comm = container[j].find_element(By.XPATH, "./div[3]/div[1]/div[1]/q/span").text.replace("\n", "  ")
            except:
                comm = container[j].find_element(By.XPATH, "./div[4]/div[1]/div[1]/q/span").text.replace("\n", "  ")
            info_comm.append([nom_hotel, nom_auteur, note_comm, comm])

        if compteur == 1:
            try:
                driver.find_element(By.XPATH,
                                    "/html/body/div[2]/div[2]/div[2]/div[9]/div/div[1]/div[1]/div/div/div[3]/div[13]/div/a").click()
            except:
                suivant = False
        else:
            try:
                driver.find_element(By.XPATH,
                                    "/html/body/div[2]/div[2]/div[2]/div[9]/div/div[1]/div[1]/div/div/div[3]/div[13]/div/a[2]").click()
            except:
                suivant = False

    return (info_hotel, info_comm)


def recherche(link):
    driver.implicitly_wait(4)
    suivant = True
    compteur_hotel = 1
    info_hotels = []
    info_comms = []
    backup_h = open("backup_h2.txt", "a", encoding="utf-8""")
    backup_c = open("backup_c2.txt", "a", encoding="utf-8""")
    df_hotel_partiel = pd.DataFrame({"nom_hotel", "adresse", "note"})
    df_hotel = pd.DataFrame({"nom_hotel", "adresse", "note"})
    df_comm_partiel = pd.DataFrame({"nom_hotel", "nom_auteur", "note_comm", "contenue"})
    df_comm = pd.DataFrame({"nom_hotel", "nom_auteur", "note_comm", "contenue"})
    while suivant == True:
        try:
            driver.find_element(By.ID, "onetrust-reject-all-handler").click()
        except:
            None
        driver.implicitly_wait(4)
        compteur_hotel += 1
        print(compteur_hotel)
        container_hotel = driver.find_elements(By.XPATH,'//div[@class="prw_rup prw_meta_hsx_responsive_listing ui_section listItem reducedWidth rounded"]')

        last_link = driver.current_url

        tablink = []

        for j in range(len(container_hotel)):
            driver.implicitly_wait(2)
            try:
                tablink.append(
                    container_hotel[j].find_element(By.XPATH, './div/div[1]/div[2]/div[1]/div/div/a').get_attribute('href'))
            except:
                None

        for link in tablink:
            driver.get(link)
            driver.implicitly_wait(4)
            try:
                driver.find_element((By.XPATH, '/html/body/div[13]/div/div[1]/div/div[1]/button'))
            except:
                None
            try:
                driver.find_element(By.ID, "onetrust-reject-all-handler").click()
            except:
                None
            info_hotel, info_comm = recherche_comm()
            info_hotels.append(info_hotel)
            info_comms.append(info_comm)
            df_hotel_partiel = pd.DataFrame(info_hotel)
            df_comm_partiel = pd.DataFrame(info_comm)
            df_hotel_partiel.to_json('table_info_hotels_partiel2.csv')
            df_comm_partiel.to_csv('table_info_comms_partiel2.csv')
            backup_h.write(str(info_hotel)+";")

            for info in info_comm:
                backup_c.write(str(info)+";")

            print(info_hotels)

        driver.get(last_link)

        if compteur_hotel == 1:
            try:
                driver.implicitly_wait(4)
                link2 = str(driver.find_element(By.XPATH,
                                                "/html/body/div[2]/div[1]/div[1]/div/div[2]/div[4]/div[2]/div[11]/div/div/div/a").get_attribute('href'))
                link2 = link2
                driver.implicitly_wait(2)
                driver.get(link2)
                driver.implicitly_wait(4)

            except:
                suivant = False
        else:
            try:
                driver.implicitly_wait(4)
                link2 = str(driver.find_element(By.XPATH,
                                                "/html/body/div[2]/div[1]/div[1]/div/div[2]/div[4]/div[2]/div[11]/div/div/div/a[2]").get_attribute('href'))
                link2 = link2
                driver.implicitly_wait(2)
                driver.get(link2)
                driver.implicitly_wait(4)

            except:
                suivant = False

    df_hotel = pd.DataFrame(info_hotels)
    df_comm = pd.DataFrame(info_comms)
    df_hotel.to_csv('table_info_hotels2.csv')
    df_comm.to_csv('table_info_comms2.csv')


driver = selenium.webdriver.Firefox()
link = "https://www.tripadvisor.com/Hotels-g187147-oa510-Paris_Ile_de_France-Hotels.html"
driver.get(link)  # connection tripadvisor
driver.implicitly_wait(4)
driver.find_element(By.ID, "onetrust-reject-all-handler").click()

recherche(link)
# driver.close()