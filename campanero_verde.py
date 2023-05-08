"""
Módulo que permite obtener el valor del canje entre dólar CCl y MEP.
Para ello ingresa a Balanz Capital con credenciales guardadas en un archivo \'.env\'.
"""

import os
from dotenv import load_dotenv
import requests
import pandas as pd

CREDENTIALS_FILENAME = 'bnz_credentials.env'
URL_LOGIN = 'https://clientes.balanz.com/api/v1/login'
URL_LOGOUT = 'https://clientes.balanz.com/api/v1/logout'
URL_COTIZACIONES_BONOS = 'https://clientes.balanz.com/api/v1/cotizaciones/panel/23?token=0'
COLS_TABLA = ['plazo', 'ticker', 'u']

def get_canje(bnz_username, bnz_password):
    """Obtiene el canje entre dólar CCL y MEP según cotización de bonos de Balanz."""
    with requests.Session() as s:
        s.headers['accept'] = 'application/json'
        r = s.post(URL_LOGIN, json={"data": {"user": bnz_username, "pass": bnz_password}})
        token = r.json()['AccessToken']
        bonos_soberanos = s.get(URL_COTIZACIONES_BONOS, headers={"authorization": token})
        r = s.post(URL_LOGOUT, headers={"authorization": token})

    df_bonos = pd.DataFrame(bonos_soberanos.json()['cotizaciones'])[COLS_TABLA]
    ult_precio_GD30C = df_bonos[
                                df_bonos['ticker']=='GD30C'][
                                df_bonos['plazo']=='48hs'][
                                'u'
                                ].to_numpy()[0]
    ult_precio_GD30D = df_bonos[
                                df_bonos['ticker']=='GD30D'][
                                df_bonos['plazo']=='48hs'][
                                'u'
                                ].to_numpy()[0]
    canje = 100 * (ult_precio_GD30D/ult_precio_GD30C - 1)
    return canje


if __name__ == "__main__":
    load_dotenv(CREDENTIALS_FILENAME)
    bnz_username = os.environ.get('BNZ_USER')
    bnz_password = os.environ.get('BNZ_PASS')
    canje = get_canje(bnz_username, bnz_password)
    print('\nEl canje hoy anda en {}%'.format(round(canje, 1)))