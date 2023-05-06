"""
Módulo que permite obtener el valor del canje entre dólar CCl y MEP.
Para ello ingresa a Balanz Capital con credenciales guardadas en las variables de entorno BNZ_USER y
BNZ_PASS.
"""

import os
import requests
import pandas as pd

URL_LOGIN = 'https://clientes.balanz.com/api/v1/login'
URL_LOGOUT = 'https://clientes.balanz.com/api/v1/logout'
URL_COTIZACIONES_BONOS = 'https://clientes.balanz.com/api/v1/cotizaciones/panel/23?token=0'
COLS_TABLA = ['plazo', 'ticker', 'u']

def get_canje():
    """Obtiene el canje entre dólar CCL y MEP según cotización de bonos de Balanz."""
    user_name = os.environ['BNZ_USER']
    password = os.environ['BNZ_PASS']
    with requests.Session() as s:
        s.headers['accept'] = 'application/json'
        r = s.post(URL_LOGIN, json={"data": {"user": user_name, "pass": password}})
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
    canje = get_canje()
    print('\nEl canje hoy anda en {}%'.format(round(canje, 1)))