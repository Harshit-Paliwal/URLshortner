import pyqrcode
import png

class qr_code():
    def __init__(self) ->None:
        pass
    def make_qr(self,url,special_key):
        url = pyqrcode.create(url)  #genrate the QR code
        url.png(special_key+".png",scale = 6)
    