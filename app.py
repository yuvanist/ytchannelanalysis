from flask import Flask, Response, request, render_template
from engine import process_channel

app = Flask(__name__, static_url_path="/static")
app._static_folder = "/static/"


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "GET":
        return render_template("home.html")
    else:
        channel_link = request.form.get("channel_url").strip()
        if channel_link:
            display_text = process_channel(channel_link)
            return render_template("home.html", display_text=display_text)
        return render_template("home.html", display_text=[])


if __name__ == "__main__":
    app.run(use_reloader=True, debug=False)
