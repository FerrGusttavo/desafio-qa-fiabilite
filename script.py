
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time

class Application:
    def __init__(self):

        # Dicionário de variáveis 
        self.SITE_LINK = "https://www.amazon.com.br/"
        self.PRODUCT_NAME = "Smartphone"
        self.SITE_MAP = {
            "FIELDS": {
                "SEARCH_INPUT": {
                    "ID": 'twotabsearchtextbox'
                },
                "PRODUCT": {
                    "XPATH": '//*[@id="search"]/div[1]/div[1]/div/span[3]/div[2]/div[4]/div/div'
                },
                "CART_ITEM": {
                    "XPATH": '//*[@id="activeCartViewForm"]/div[2]'
                }
            },
            "BUTTONS": {
                "CART_BUTTON": {
                    "ID": 'add-to-cart-button'
                },
                "COVERAGE_BUTTON": {
                    "XPATH": '//*[@id="attachSiAddCoverage"]/span/input'
                },
                "GO_CART_BUTTON": {
                    "XPATH": '//*[@id="sw-gtc"]/span/a'
                }
            }
        }

        # Chama o executável do chromedriver e inicializa
        print("Automação Web utilizando Python + Selenium")
        self.driver = webdriver.Chrome(executable_path="assets/chromedriver.exe")
        self.driver.maximize_window()

    def abrir_site(self):
        time.sleep(2)
        self.driver.get(self.SITE_LINK)
    
    def busca_produto(self):
        input = self.driver.find_element(By.ID, (self.SITE_MAP["FIELDS"]["SEARCH_INPUT"]["ID"]))
        input.send_keys(self.PRODUCT_NAME)
        inputText = self.driver.find_element(By.ID, (self.SITE_MAP["FIELDS"]["SEARCH_INPUT"]["ID"])).get_attribute('value')

        # Verifica se o mesmo nome de produto pesquisado corresponde a página
        def verifica_retorno(busca_produto):
            if (inputText == self.PRODUCT_NAME):
                input.submit()
                print("Retorno de Busca: PASS.")
            else:
                print("Retorno de Busca: FAILED.")

        verifica_retorno(inputText)

    def seleciona_produto(self):
        time.sleep(2)
        self.driver.find_element(By.XPATH, (self.SITE_MAP["FIELDS"]["PRODUCT"]["XPATH"])).click()

    def finaliza_pedido(self):
        time.sleep(2)
        self.driver.find_element(By.ID, (self.SITE_MAP["BUTTONS"]["CART_BUTTON"]["ID"])).click()
        time.sleep(2)

        # Verifica se existe a aba para cobertura contra-roubo do site
        def verifica_coverage():
            try:
                coverage_button = self.driver.find_element(By.XPATH, (self.SITE_MAP["BUTTONS"]["COVERAGE_BUTTON"]["XPATH"]))
                coverage_button.click()

            except NoSuchElementException:
                coverage_button = self.driver.find_element(By.XPATH, (self.SITE_MAP["BUTTONS"]["GO_CART_BUTTON"]["XPATH"])).click()

        verifica_coverage()

        # Verifica se existe algum produto ativo no carrinho de compras
        def verifica_pedido():
            try:
                self.driver.find_element(By.XPATH, (self.SITE_MAP["FIELDS"]["CART_ITEM"]["XPATH"]))
                print("Produto no Carrinho: PASS.")
                self.driver.close()
            except NoSuchElementException:
                print("Produto no Carrinho: FAILED.")
                self.driver.close()
                
        verifica_pedido()

selenium = Application()
selenium.abrir_site()
selenium.busca_produto()
selenium.seleciona_produto()
selenium.finaliza_pedido()