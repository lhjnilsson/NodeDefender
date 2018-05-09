from datetime import datetime
from NodeDefender.db.sql import SQL


class RuleModel(SQL.Model):
    __tablename__ = "rule"
    id=SQL.Column(SQL.Integer, primary_key=True)
    sensor_id=SQL.Column(SQL.Integer, SQL.ForeignKey("sensor.id"))
    commandclass_id=SQL.Column(SQL.Integer, SQL.ForeignKey("commandclass.id"))
    commandclass_type_id=SQL.Column(SQL.Integer,\
                                    SQL.ForeignKey("commandclasstype.id"))
    heat=SQL.relationship("HeatRuleModel", backref="rule",\
                          cascade="save-update, merge, delete")
    power=SQL.relationship("PowerRuleModel", backref="rule",\
                           cascade="save-update, merge, delete")
    event=SQL.relationship("EventRuleModel", backref="rule",\
                           cascade="save-update, merge, delete")

    trigger=SQL.relationship("TriggerModel", backref="rule",\
                             cascade="save-update, merge, delete")

class TriggerModel(SQL.Model):
    __tablename__="rule_trigger"
    id=SQL.Column(SQL.Integer, primary_key=True)
    rule_id=SQL.Column(SQL.Integer, SQL.ForeignKey("rule.id"))
    logg=SQL.Column(SQL.Boolean)
    mail=SQL.Column(SQL.Boolean)
    event=SQL.Column(SQL.Boolean)

class HeatRuleModel(SQL.Model):
    __tablename__ ="heat_rule"
    id=SQL.Column(SQL.Integer, primary_key=True)
    rule_id=SQL.Column(SQL.Integer, SQL.ForeignKey("rule.id"))
    low=SQL.Column(SQL.Float)
    high=SQL.Column(SQL.Float)
    step=SQL.Column(SQL.Float)

class PowerRuleModel(SQL.Model):
    __tablename__ ="power_rule"
    id=SQL.Column(SQL.Integer, primary_key=True)
    rule_id=SQL.Column(SQL.Integer, SQL.ForeignKey("rule.id"))
    low=SQL.Column(SQL.Float)
    high=SQL.Column(SQL.Float)
    step=SQL.Column(SQL.Float)

class EventRuleModel(SQL.Model):
    __tablename__="event_rule"
    id=SQL.Column(SQL.Integer, primary_key=True)
    rule_id=SQL.Column(SQL.Integer, SQL.ForeignKey("rule.id"))
    value=SQL.Column(SQL.Integer)

    def __init__(self, value):
        self.value = value
