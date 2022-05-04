import os
import random
from matplotlib.image import imread
import json
import operator
import requests
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from azure.cognitiveservices.vision.customvision.prediction import (
    CustomVisionPredictionClient
)
from msrest.authentication import ApiKeyCredentials
# import time

url = ""
api_keys = ''
headers={'content-type':'application/octet-stream','Prediction-Key':api_keys}


def open_waste_slot():

    """
        open the machine so that
        an user can enter the machine
    :return:
    """

    send_command_to_machine("open_waste_slot")
    return True


def close_waste_slot():
    """
    close the waste box for user safety
    :return:
    """

    send_command_to_machine("close_waste_slot")
    return True


def process_waste(waste_type):

    """
    move the good slot and shredd the waste
    :return:
    """

    move_container(waste_type)
    was_sucessful = shred_waste()

    return was_sucessful



def move_container(waste_type):

    BOTTLE_BOX = 0
    GLASS_BOX = 1
    CUTLERY_BOX = 0
    command_name = "move_container"

    if waste_type == "bottles":
        send_command_to_machine(command_name, BOTTLE_BOX)
    elif waste_type == "glass":
        send_command_to_machine(command_name, GLASS_BOX)
    elif waste_type == "cutlery":
        send_command_to_machine(command_name, CUTLERY_BOX)

    return True


def send_command_to_machine(command_name, value=None):

    """
    simulate command sending to rasberry pi
    do nothing to work even if the machine is not connected
    :param command_name:
    :param value:
    :return:
    """
    return True



def shred_waste():

    send_command_to_machine("shred_waste")

    return True


def take_trash_picture():

    """
        Call this function to ask the machine to
        take picutre of the trash
        return : np array of the picture
    """

    send_command_to_machine("take_picture")

    paths = os.listdir('/Users/opheliesabanowski/Desktop/exercices/ProjetP8Triof/triof/static/images/camera/propre/')
    path = random.choice(paths)

    return path



def pred_func(data):
    print(data)
    r =requests.post(url,data=data,headers=headers).content
    print(r)
    pred = {x["tagName"]:x["probability"]  for x in json.loads(r)["prediction"]}
    return max(pred.items(), key=operator.itemgetter(1))[0]


def scrap(): 

# Lien de la page à scraper

    driver = webdriver.Chrome()
    driver.get("https://www.google.com/")
 

 
# que la page charge avant de passer à la suite
    sleep(10)
    search_bar = driver.find_element_by_name("_nkw")
    search_bar.send_keys("images plastiques bouteille")
    search_bar.send_keys(Keys.ENTER)
    is_last_page = False
    while not is_last_page:
        offers = driver.find_elements_by_css_selector("a.x0Sesd pla-link")
        for offer in offers:
            image = offer.find_element_by_css_selector("a.x0Sesd pla-link").get_attribute("src")
            print("Image : ",image)
            print("")
        next_page = driver.find_element_by_css_selector("table#Pagination a.next")
        is_last_page = next_page.get_attribute("arial-disabled")
        if is_last_page == "true" or is_last_page == "True":
            is_last_page = True
        else:
            next_page.click()
        sleep(10)
    #imagge = selector.css("x0Sesd pla-link")
    