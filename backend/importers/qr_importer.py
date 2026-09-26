import cv2


def read_qr_code(file_path):
    image = cv2.imread(file_path)

    detector = cv2.QRCodeDetector()

    data, points, _ = detector.detectAndDecode(image)

    if not data:
        raise ValueError("No QR code found in image")

    return data