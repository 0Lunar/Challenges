import os
from flask import (
    Flask,
    request,
    render_template,
    make_response,
)
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
import base64

aes_key = get_random_bytes(16)
cipher = AES.new(aes_key, mode=AES.MODE_ECB)
app = Flask(__name__)
FLAG = os.getenv("FLAG", "flag{tux_loves_ecb}")


@app.route("/")
def home():
    if "id" in request.cookies:
        try:
            cookie = request.cookies.get("id")
            decrypted = cipher.decrypt(base64.b64decode(cookie))
            user_data = unpad(decrypted, 16)

            # Parsing: username={name}-is_admin={bool}
            parts = user_data.split(b"-")
            username = parts[0].split(b"=")[1].decode(errors="ignore")
            admin_part = parts[1].split(b"=")[1]

            is_admin = admin_part == b"true"
            return render_template(
                "index.html",
                page="home",
                logged_in=True,
                user=username,
                is_admin=is_admin,
                flag=FLAG,
            )
        except:
            resp = make_response(
                render_template("index.html", page="home", logged_in=False)
            )
            resp.set_cookie("id", "", expires=0)
            return resp
    else:
        return render_template("index.html", page="home", logged_in=False)


@app.route("/login/<username>")
def login(username):
    safe_username = username.replace("-", "").replace("=", "")
    cookie_payload = f"username={safe_username}-is_admin=false".encode()
    cookie_padded = pad(cookie_payload, 16)
    encrypted_cookie = base64.b64encode(cipher.encrypt(cookie_padded)).decode()

    resp = make_response(
        render_template("index.html", page="login_success", user=safe_username)
    )
    resp.set_cookie("id", encrypted_cookie)
    return resp


@app.route("/logout")
def logout():
    resp = make_response(render_template("index.html", page="home", logged_in=False))
    resp.set_cookie("id", "", expires=0)
    return resp


if __name__ == "__main__":
    app.run()
