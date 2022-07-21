from app import app
from flask import Flask, render_template, request, jsonify


transactions = [
  Credit(1, 50),
  Credit(2, 40),
  Debit(3, 3),
  Debit(4, 2)
]
