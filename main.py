import os
import smtplib
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from selenium.webdriver.common.by import By


def check_if_previous_exists(abs_file_path):
    return os.path.isfile(abs_file_path)


def get_previous_number_of_apt(abs_file_path):
    file = open(abs_file_path, "r")
    number_of_apt = file.real()
    return number_of_apt


def get_updated_number_of_apt():
    url = "https://www.shdm.org/fr/locataires/logements-a-louer/"
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)
    element = driver.find_element(By.CLASS_NAME, "the_num ng-binding")
    fetched_number = element.text
    driver.close()

    return fetched_number


def send_mail(previous_number_of_apt, updated_number_of_apt):
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.ehlo()
    server.strattls()
    server.ehlo()

    server.login(os.environ["GMAIL_USER"], os.environ["GMAIL_PWD"])

    subject = "SHDM.org - updated number of apartments!"
    bodyText = "SHDM.org has updated apartments from " + previous_number_of_apt + "=> " + updated_number_of_apt

    message = MIMEMultipart("alternative")
    message["Subject"] = subject
    message["From"] = os.environ["GMAIL_USER"]
    message["To"] = os.environ["RECEIVER_OF_APT_NOTIF"]

    part = MIMEText(bodyText, "plain")
    message.attach(part)

    server.sendmail(os.environ["GMAIL_USER"], os.environ["RECEIVER_OF_APT_NOTIF"], message.as_string())


def update_local(abs_file_path, updated_number):
    file = open(abs_file_path, "w")
    file.write(updated_number)
    file.close()


def check_if_updated():
    script_directory_path = os.path.dirname(__file__)
    file_name = "previous-number.txt"
    abs_file_path = os.path.join(script_directory_path, file_name)

    prev_exists = check_if_previous_exists(abs_file_path)

    if prev_exists:
        previous_number_of_apt = get_previous_number_of_apt(abs_file_path)
        update_number_of_apt = get_updated_number_of_apt()

        if(previous_number_of_apt != update_number_of_apt):
            send_mail(previous_number_of_apt, update_number_of_apt)
            updade_local(abs_file_path, update_number_of_apt)
    else:
        updated_number_of_apt = get_updated_number_of_apt()
        update_local(abs_file_path,updated_number_of_apt)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    check_if_updated()
