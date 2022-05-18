from prometheus_client import start_http_server, Info, Gauge
import evnhanoi.client
import random
import time

# USER_INFO =
CONSUMPTION = Gauge('evn_consumption', 'EVN: Dientthu', ['type', 'year', 'month'])

if __name__ == '__main__':
    start_http_server(9184)
    username, password = 'PD0400T013913', 'HyperGaming@2022'
    year = 2022

    EVNClient = evnhanoi.client.Client()
    EVNClient.set_credential(username=username, password=password)
    EVNClient.auth()
    print('Auth done!')

    while True:
        evn_user = Info('evn_user', 'EVN: Userinfo')
        evn_user.info(EVNClient.get_user_info())

        evn_customer = Info('evn_customer', 'EVN: GetKhachHang')
        print(EVNClient.get_customer())
        evn_customer.info(EVNClient.get_customer())

        for evn_monthly_data in EVNClient.get_consumption(year=year)['tieuThuTheoThangList']:
            CONSUMPTION.labels(type='dienTthu',
                               year=evn_monthly_data['nam'],
                               month=evn_monthly_data['thang']).set(evn_monthly_data['dienTthu'])
            CONSUMPTION.labels(type='soTien',
                               year=evn_monthly_data['nam'],
                               month=evn_monthly_data['thang']).set(evn_monthly_data['soTien'])

        time.sleep(30)
