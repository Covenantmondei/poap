import qrcode
from io import BytesIO
import base64

def generate_event_qr(event_id):
    data = {
        "event_id": event_id,
    }

    qr = qrcode.make(data)
    buffered = BytesIO()

    # save the qrcode
    qr.save(buffered, format="PNG")

    img_base64 = base64.b64encode(buffered.getvalue()).decode()

    # Return the base64 encoded image as a data URI
    return f"data:image/png;base64,{img_base64}"