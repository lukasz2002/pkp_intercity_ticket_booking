from libs import Web


def run():
    web = Web()
    web.init_web()
    web.pass_station_and_date()


if __name__ == "__main__":
    run()
