"""
Módulo que permite obtener el valor del canje entre dólar CCl y MEP según sus valores de ultima
operacion en invertironline-
"""
import requests
import pandas as pd

URL_COTIZACIONES_BONOS = 'https://iol.invertironline.com/mercado/cotizaciones/argentina/bonos/todos'

def get_canje():
    """Obtiene el canje entre dólar CCL y MEP según cotización de bonos de invertironline."""
    r = requests.get(URL_COTIZACIONES_BONOS)
    df_bonos = pd.read_html(r.text)[0]
    ult_precio_GD30C = df_bonos[
                                df_bonos['Símbolo']=='GD30C'][
                                'ÚltimoOperado'
                                ].to_numpy()[0]
    ult_precio_GD30D = df_bonos[
                                df_bonos['Símbolo']=='GD30D'][
                                'ÚltimoOperado'
                                ].to_numpy()[0]
    canje = 100 * (ult_precio_GD30D/ult_precio_GD30C - 1)
    return canje


if __name__ == "__main__":
    load_dotenv(CREDENTIALS_FILENAME)
    bnz_username = os.environ.get('BNZ_USER')
    bnz_password = os.environ.get('BNZ_PASS')
    canje = get_canje(bnz_username, bnz_password)
    print('\nEl canje hoy anda en {}%'.format(round(canje, 1)))