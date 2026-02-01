from flask import Flask, jsonify, request
from flask_cors import CORS
from bakong_khqr import KHQR
import uuid

app = Flask(__name__)
CORS(app)

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

    if isinstance(qr, dict):
        qr = qr.get("qr")

    return jsonify({"qrData": qr})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)

