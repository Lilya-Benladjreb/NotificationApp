import os
import smtplib
from email.mime.multipart import MIMEMultipart


def check_if_previous_exists(absFilePath):
    return os.path.isfile(absFilePath)

def send_mail(previous_number_of_apt, updated_number_of_apt):
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.ehlo()
    server.strattls()
    server.ehlo()

    server.login("lilya.benladjreb@gmail.com", "2014MMXIV")

    subject = "SHDM - updated number of apartments!"
    bodyText = "SHDM has updated apartments from " + previous_number_of_apt + "=> " + updated_number_of_apt

    message = MIMEMultipart("alternative")
    message["Subject"] = subject
    message["From"] = "lilya.benladjreb@gmail.com"
    message["To"] =

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
