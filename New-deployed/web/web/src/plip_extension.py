from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import os, time, requests


class ObtainInteractionsFromComplex:
    def __init__(self, protein_ligand_complex):
        self.cplx = protein_ligand_complex

    def connect_retrieve(self):
        try:
            options = Options()
            options.headless = True
            plip = webdriver.Firefox(options=options)
            plip.get("https://projects.biotec.tu-dresden.de/plip-web/plip")
            print("Connection to PLIP server successful")

            print("Processing file {}".format(self.cplx))
            select_pdb_input = plip.find_element_by_xpath(
                "//*[@id='select-pdb-by-file']").click()  # Click upload pdb

            browse = plip.find_element_by_xpath(
                '/html/body/div[1]/div[2]/div/form/div[1]/div[1]/div[3]/input'
            ).send_keys(  # search for browse button and choose complex
                os.getcwd() + '/{}'.format(self.cplx)
            )

            send_file = plip.find_element_by_xpath("//*[@id='submit']").click()  # apply operation
            time.sleep(10)  # wait for some time by the time connection is stabilized
            try:
                try:
                    open_interactions_1 = plip.find_element_by_xpath(
                        '/html/body/div/div[2]/div/div[1]/h2[2]').click()
                    open_interactions_2 = plip.find_element_by_xpath(
                        '/html/body/div[1]/div[2]/div/div[1]/div[2]/h3').click()
                    open_interactions_3 = plip.find_element_by_xpath(
                        '/html/body/div[1]/div[2]/div/div[1]/div[2]/div/h4').click()
                    pngs = plip.find_elements_by_xpath("//a[contains(@href,'.png')]")
                    pymolsessions = plip.find_elements_by_xpath("//a[contains(@href,'.pse')]")

                except:
                    open_interactions_1 = plip.find_element_by_xpath(
                        '/html/body/div[1]/div[2]/div/div[1]/h2[1]').click()
                    open_interactions_2 = plip.find_element_by_xpath(
                        '/html/body/div[1]/div[2]/div/div[1]/div[1]/h3').click()
                    open_interactions_3 = plip.find_element_by_xpath(
                        '/html/body/div[1]/div[2]/div/div[1]/div[1]/div/h4').click()
                    pngs = plip.find_elements_by_xpath("//a[contains(@href,'.png')]")
                    pymolsessions = plip.find_elements_by_xpath("//a[contains(@href,'.pse')]")

                for image in pngs:
                    print(image.get_attribute("href"))
                    output_image = requests.get(image.get_attribute("href"))
                    open(
                        os.getcwd() + '/results/{}'.format(self.cplx + '.png'), 'wb'
                    ).write(output_image.content)
                    print("Image saved as {}".format(self.cplx + '.png'))

                for pysession in pymolsessions:
                    print(pysession.get_attribute("href"))
                    pse = requests.get(pysession.get_attribute("href"))
                    open(
                        os.getcwd() + '/results/{}'.format(self.cplx + '.pse'), 'wb'
                    ).write(pse.content)
                    print("Pymol sessions saved as {}".format(self.cplx + '.pse'))

                restart_plip = plip.find_element_by_xpath('/html/body/div[1]/div[2]/div/p[3]/a').click()
                time.sleep(5)

            except:
                print("No interactions found for {} or damaged structure".format(self.cplx))
                try:
                    restart_plip = plip.find_element_by_xpath('/html/body/div[1]/div[2]/div/p[3]/a').click()
                    time.sleep(5)
                except:
                    restart_plip = plip.find_element_by_xpath('/html/body/div[1]/div[2]/div[2]/p/a').click()
        except Exception as e:
            print(e)
            pass
