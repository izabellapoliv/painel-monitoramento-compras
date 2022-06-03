# coding: utf-8

from distutils.log import debug
import os
from flask import Flask, render_template, request, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)
SQLALCHEMY_DATABASE_URI = f'mysql://{os.environ.get("DATABASE_USERNAME")}:{os.environ.get("DATABASE_PASSWORD")}@{os.environ.get("DATABASE_HOST")}/{os.environ.get("DATABASE_NAME")}'
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
db = SQLAlchemy(app)


class Compras(db.Model):
    fk_id_compra = db.Column(db.Integer, primary_key=True)
    fk_id_login = db.Column(db.Integer, primary_key=True)
    data_compra = db.Column(db.DateTime)
    valor_compra = db.Column(db.Numeric)
    frete_compra = db.Column(db.Numeric)
    desconto_compra = db.Column(db.Numeric)
    local_compra = db.Column(db.String(255))
    tipo_frete_compra = db.Column(db.String(255))
    user_agent_compra = db.Column(db.String(255))
    status_hist = db.Column(db.String(255))
    data_hist = db.Column(db.DateTime)
    responsavel_hist = db.Column(db.String(255))

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def toDict(self):
        return {
            "fk_id_compra": self.fk_id_compra,
            "fk_id_login": self.fk_id_login,
            "data_compra": self.data_compra,
        }


@app.before_request
def limit_remote_addr():
    if app.debug == False:
        allowed_ips = [
            "189.113.170.21",
            "189.113.170.22",
            "189.113.170.23",
            "189.113.170.26",
            "189.113.170.27",
            "189.113.170.28",
            "189.113.170.29",
            "189.113.174.135",
            "189.113.174.136",
            "189.113.174.137",
            "189.113.174.206",
            "189.113.174.207",
            "189.113.174.208",
            "189.113.174.209",
            "189.113.174.134",
            "189.113.170.25",
            "189.113.170.24",
            "189.113.170.27",
        ]
        if request.remote_addr not in allowed_ips:
            abort(403)  # Forbidden


@app.route("/")
def welcome():
    return render_template("index.html")


@app.route("/api/compras", methods=["GET"])
def get_compras():
    page = request.args.get("page", default=1, type=int)
    per_page = request.args.get("per_page", default=100, type=int)
    pagination = Compras.query.paginate(page=page, per_page=per_page)

    result = {
        "items": [each.toDict() for each in pagination.items],
        "page": pagination.page,
        "pages": pagination.pages,
        "total": pagination.total,
    }
    return jsonify(result)


@app.route("/api/compras", methods=["POST"])
def post_compras():
    new_compra = Compras(
        fk_id_compra=request.json["fk_id_compra"],
        fk_id_login=request.json["fk_id_login"],
        data_compra=request.json["data_compra"],
        valor_compra=request.json["valor_compra"],
        frete_compra=request.json["frete_compra"],
        desconto_compra=request.json["desconto_compra"],
        local_compra=request.json["local_compra"],
        tipo_frete_compra=request.json["tipo_frete_compra"],
        user_agent_compra=request.json["user_agent_compra"],
        status_hist=request.json["status_hist"],
        data_hist=request.json["data_hist"],
        responsavel_hist=request.json["responsavel_hist"],
    )

    compra = db.session.get(
        Compras,
        {
            "fk_id_compra": request.json["fk_id_compra"],
            "fk_id_login": request.json["fk_id_login"],
        },
    )
    print(compra)

    try:
        db.session.merge(new_compra)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()

    return jsonify(new_compra.toDict())


if __name__ == "__main__":
    app.run(
        debug=True if os.environ.get("FLASK_ENV") == "development" else False,
        host="0.0.0.0",
    )
