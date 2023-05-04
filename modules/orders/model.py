import datetime


from modules import db


class Orders(db.Model):
    """
    Class that represents a order of the application

    The following attributes of a order are stored in this table:
        * id: database id of the order
        * user_id: databse id of the user
        * amount - amount of the order
        * order_date - date & time that the order

    """

    __tablename__ = "orders"

    # __bind_key__ = "app_meta"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # TODO: update user_id as foreign key
    user_id = db.Column(db.Integer, autoincrement=False)
    order_date = db.Column(db.DateTime, nullable=False)
    amount = db.Column(db.Float, unique=False)

    def __init__(
        self,
        user_id: int,
        amount: int,
    ):
        """Create a new Order object using the user_id and amount"""
        self.user_id = user_id
        self.amount = amount
        self.order_date = datetime.datetime.utcnow()

    def __repr__(self):
        return f"<Order ID: {self.id}>"
