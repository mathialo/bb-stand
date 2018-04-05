#! /usr/bin/python3

# HTML frontend
from flask import render_template, request, Flask

# Email functionality
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Random crap
import time


# Create Flask app
app = Flask(__name__)


def read_properties():
    user, password = None, None

    try:
        infile = open("email.properties", "r")

        for line in infile:
            key, val = line.split("=")
            key, val = key.strip(), val.strip()

            if key == "user":
                user = val
            elif key == "pass":
                password = val

        infile.close()

    except FileNotFoundError:
        infile = open("email.properties", "w")
        infile.write("user=\npass=\n")
        infile.close()

        print("email.properties was created, please provide login info for UiO user")
        raise Exception

    return user, password


def get_text(language):
    text = ""

    try:
        infile = open(language, "r")

        for line in infile:
            text += line

        infile.close()

    except FileNotFoundError:
        raise Exception("No email text made for language %s!" % language)

    return text


def send_mail(to_name, to_email, text):
    # Create message container
    msg = MIMEMultipart('alternative')
    msg['Subject'] = "BB-info!"
    msg['From'] = "\"Studentorchesteret Biorneblaes\" <noreply@grava.uio.no>"
    msg['To'] = "%s <%s>" % (to_name, to_email)
    msg['reply-to'] = "cc@grava.uio.no"

    # Create message body
    html = text

    # Attach body to message container
    part2 = MIMEText(html, 'html', "utf-8")
    msg.attach(part2)

    # Send the email
    s = smtplib.SMTP("smtp.uio.no", 587)
    s.ehlo()
    s.starttls()
    s.login(user, password)
    s.sendmail("noreply@grava.uio.no", to_email, msg.as_string())
    s.quit()


# Responds to user input
@app.route("/", methods=["GET"])
def main_screen():
    return render_template('index.html')


@app.route("/send", methods=["POST"])
def send_screen():
    # Read properties from request
    name = request.form["name"]
    email_addr = request.form["email_addr"]
    lang = request.form["lang"]

    print("Request: ", name, email_addr, lang)

    text = ""

    try:
        print("Sending email to %s..." % email_addr, end="")
        send_mail(name, email_addr, get_text(lang))
        logfile.write("%s,%s,%s,%s\n" % (name, email_addr, lang, "true"))
        print("   OK!")

        if lang == "nobm":
            text = "Vi har sendt deg en infomail!"

        elif lang == "eng":
            text = "We have sent you an info email!"

    except Exception as e:
        print("   Fail!")
        print("Could not send automatic email. Logging email either way.")
        logfile.write("%s,%s,%s,%s\n" % (name, email_addr, lang, "false"))
        print("  -> Error message: '%s'" % str(e))

        if lang == "nobm":
            text = "Vi kunne ikke sende eposten, kan du ha skrevet feil?"

        elif lang == "eng":
            text = "We could not send the email, could you have typed something wrong?"

    # Make sure file is actually updated
    logfile.flush()

    return render_template('sent.html', infotext=text)


def main():
    # Declare these as global vars, so that they are available from send_mail()
    global user
    global password
    global logfile

    try:
        user, password = read_properties()

    except:
        print("Error in reading email settings, closing app")
        return

    try:
        logfile = open("collected_%d.csv" % time.time(), "w")
        logfile.write("navn,epost,språk,sendt infomail\n")
        logfile.flush()

    except:
        print("Error in creating logfile, closing app")
        return

    app.run()

    logfile.close()


if __name__ == '__main__':
    main()
