from libs import Web


def run():
    web = Web()
    # web.get_user_date_into_dict()
    web.validate_hour()
    web.init_web()
    # web.pass_station()
    # web.pass_date()
    web.pass_hour()


if __name__ == "__main__":
    run()
