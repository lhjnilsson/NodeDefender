def Get(node, from_date = (datetime.now() - timedelta(days=7)), to_date =
        datetime.now()):
    return session.query(PowerModel).filter(name == node, date > from_date, date
                                            < to_date)

def Put(node, power, date):
    data = session.query(PowerModel).filter(name == node, date == date)
    if data:
        power = (data.power / 2)
        data.presision += 1
    else:
        power = PowerModel(power, date)
    db.session.add(power)
    db.session.commit()
