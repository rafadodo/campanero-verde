import requests
import pandas as pd
from IPython import embed

URL_LOGIN = 'https://clientes.balanz.com/api/v1/login'
URL_LOGOUT = 'https://clientes.balanz.com/api/v1/logout'
URL_COTIZACIONES_BONOS = 'https://clientes.balanz.com/api/v1/cotizaciones/panel/23?token=0'
BONOS_HEADER_LIST = [
    'ticker', 'plazo', 'mo', 'cc', 'pc', 'pv', 'cv', 'u', 'v', 'min', 'max', 'f', 't'
    ]

if __name__ == "__main__":
    with requests.Session() as s:
        s.headers['accept'] = 'application/json'
        user_name = input('bueno aver dame tu usuario: ')
        password = input('bien, y pasame la pass: ')        
        r = s.post(URL_LOGIN, json={"data": {"user": user_name, "pass": password}})
        password = ''
        token = r.json()['AccessToken']
        bonos_soberanos = s.get(URL_COTIZACIONES_BONOS, headers={"authorization": token})
        r = s.post(URL_LOGOUT, headers={"authorization": token})

        df_bonos = pd.DataFrame(bonos_soberanos.json()['cotizaciones'])[BONOS_HEADER_LIST]
        ult_precio_GD30C = df_bonos[
                                    df_bonos['plazo']=='48hs'][
                                    df_bonos['ticker']=='GD30C'][
                                    'u'
                                    ].to_numpy()[0]
        ult_precio_GD30D = df_bonos[
                                    df_bonos['plazo']=='48hs'][
                                    df_bonos['ticker']=='GD30D'][
                                    'u'
                                    ].to_numpy()[0]
        canje = 100 * (ult_precio_GD30D / ult_precio_GD30C - 1)

        print('\nEl canje hoy anda en {}%'.format(round(canje), 1))
        print('''Igual te abro un ipython para que juegues, ya que estamos en desarrollo,
        no seamos caretas...\n''')
        embed(confirm_exit=False, colors='linux')