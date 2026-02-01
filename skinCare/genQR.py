from flask import Flask, render_template, jsonify, request
from bakong_khqr import KHQR
import uuid

app = Flask(__name__)
khqr = KHQR()

@app.route('/generate_khqr', methods=['POST'])
def generate_khqr():
    data = request.get_json()
    amount = float(data.get("amount", 0))

    bill_number = f"TRX-{uuid.uuid4().hex[:8]}"

    qr = khqr.create_qr(
        bank_account='thida_horm@aclb',
        merchant_name='Horm Thida',
        merchant_city='Phnom Penh',
        amount=round(amount, 2),
        currency='USD',
        store_label='SkinCare Shop',
        phone_number='0976970127',
        bill_number=bill_number,
        terminal_label='POS-01',
        static=False
    )

    # Some versions of bakong_khqr return dict
    if isinstance(qr, dict):
        qr = qr.get("qr") or qr.get("payload") or str(qr)

    return jsonify({"qrData": qr})

