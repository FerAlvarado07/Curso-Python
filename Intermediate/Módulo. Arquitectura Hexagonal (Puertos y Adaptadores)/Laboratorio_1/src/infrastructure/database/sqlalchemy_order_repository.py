from uuid import UUID

from sqlalchemy import Float, String, create_engine, select
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column

from src.domain.entities.order import Order


class Base(DeclarativeBase): ...


class OrderModel(Base):
    __tablename__ = "orders"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    customer_name: Mapped[str] = mapped_column(String(150))
    product: Mapped[str] = mapped_column(String(150))
    amount: Mapped[float] = mapped_column(Float)
    status: Mapped[str] = mapped_column(String(30))


class SQLAlchemyOrderRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def save(self, order: Order) -> Order:
        model = self.session.get(OrderModel, str(order.id))

        if model is None:
            model = OrderModel(
                id=str(order.id),
                customer_name=order.customer_name,
                product=order.product,
                amount=order.amount,
                status=order.status,
            )
            self.session.add(model)
        else:
            model.customer_name = order.customer_name
            model.product = order.product
            model.amount = order.amount
            model.status = order.status

        self.session.commit()
        self.session.refresh(model)

        return self._to_entity(model)

    def find_by_id(self, order_id: UUID) -> Order | None:
        statement = select(OrderModel).where(OrderModel.id == str(order_id))
        model = self.session.scalar(statement)

        if model is None:
            return None

        return self._to_entity(model)

    @staticmethod
    def _to_entity(model: OrderModel) -> Order:
        return Order(
            id=UUID(model.id),
            customer_name=model.customer_name,
            product=model.product,
            amount=model.amount,
            status=model.status,
        )


def create_database(database_url: str = "sqlite:///orders.db"):
    engine = create_engine(database_url)
    Base.metadata.create_all(engine)
    return engine
