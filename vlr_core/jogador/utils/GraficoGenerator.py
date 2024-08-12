import base64
import io
import urllib

from matplotlib import pyplot as plt


class GraficoGenerator:
    @staticmethod
    def generate(datas, valores, titulo):
        plt.figure(figsize=(10, 5))
        plt.plot(datas, valores, marker='o')
        plt.title(titulo)
        plt.xlabel('Data')
        plt.ylabel('Valor')
        plt.grid(True)

        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        string = base64.b64encode(buf.read())
        uri = 'data:image/png;base64,' + urllib.parse.quote(string)
        return uri
