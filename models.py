from sqlalchemy import create_engine, Column, String, Integer, Boolean, Float, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy_utils.types import ChoiceType

# Conexão do banco
db = create_engine("sqlite:///database/banco.db")

# Base do banco de dados
Base = declarative_base()

# Classes e tabelas do banco


# User
class User(Base):
    __tablename__ = "users"

    id = Column("id", Integer, primary_key=True, autoincrement=True, index=True)
    name = Column("name", String, unique=True, index=True, nullable=False)
    email = Column("email", String, unique=True, index=True, nullable=False)
    password = Column("password", String, nullable=False)
    is_active = Column("is_active", Boolean, default=True)
    is_admin = Column("is_admin", Boolean, default=False)

    def __init__(self, name, email, password, is_active=True, is_admin=False):
        self.name = name
        self.email = email
        self.password = password
        self.is_active = is_active
        self.is_admin = is_admin


# Order
class Order(Base):
    __tablename__ = "orders"

    # STATUS_PEDIDOS = (
    #     ("PENDDING", "PENDDING"),
    #     ("CANCELED", "CANCELED"),
    #     ("FINISHED", "FINISHED"),
    # )

    id = Column("id", Integer, primary_key=True, autoincrement=True, index=True)
    status = Column("status", String)
    user = Column("user", ForeignKey("users.id"), nullable=False)
    price = Column("price", Float, default=0.00)
    order_items = relationship("OrderItems", cascade="all, delete")

    def __init__(self, user, status="PENDDING", price=0.00):
        self.user = user
        self.status = status
        self.price = price

    def price_calculator(self):
        # order_price = 0
        # for item in self.order_items:
        #     item_price = item.quantity * item.price
        #     order_price += item_price

        self.price = sum(item.price * item.quantity for item in self.order_items)


# OrderItems


class OrderItems(Base):
    __tablename__ = "order_items"

    id = Column("id", Integer, primary_key=True, autoincrement=True, index=True)
    quantity = Column("quantity", Integer)
    flavor = Column("flavor", String)
    size = Column("size", String)
    price = Column("price", Float, default=0.00)
    order = Column("order", ForeignKey("orders.id"))

    def __init__(self, quantity, flavor, size, price, order):
        self.quantity = quantity
        self.flavor = flavor
        self.size = size
        self.price = price
        self.order = order


# Executa a criação dos metadados no banco (basicamente cria o banco)

# Criar migration: alembic revision --autogenerate -m "mensagem"
# Executar a migraiton : alembic upgrade head