from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from src.domain.entities.order import Order
from src.domain.ports.order_repository import OrderRepository
from src.infrastructure.database.models import OrderModel


class SqlAlchemyOrderRepository(OrderRepository):
    def __init__(self, session: Session) -> None:
        self._session = session

    @staticmethod
    def _to_entity(model: OrderModel) -> Order:
        return Order(
            id=model.id,
            customer_id=model.customer_id,
            amount=model.amount,
            currency=model.currency,
            status=model.status,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    @staticmethod
    def _to_model(order: Order) -> OrderModel:
        return OrderModel(
            id=order.id,
            customer_id=order.customer_id,
            amount=order.amount,
            currency=order.currency,
            status=order.status,
            created_at=order.created_at,
            updated_at=order.updated_at,
        )

    def save(self, order: Order) -> Order:
        model = self._session.get(OrderModel, order.id)

        if model is None:
            self._session.add(self._to_model(order))
        else:
            model.customer_id = order.customer_id
            model.amount = order.amount
            model.currency = order.currency
            model.status = order.status
            model.updated_at = order.updated_at

        self._session.commit()
        return order

    def find_by_id(self, order_id: UUID) -> Order | None:
        model = self._session.get(OrderModel, order_id)

        if model is None:
            return None

        return self._to_entity(model)

    def list_orders(self, offset: int, limit: int) -> list[Order]:
        statement = (
            select(OrderModel)
            .order_by(OrderModel.created_at.desc())
            .offset(offset)
            .limit(limit)
        )

        models = self._session.scalars(statement).all()
        return [self._to_entity(model) for model in models]

    def count(self) -> int:
        statement = select(func.count()).select_from(OrderModel)
        return int(self._session.scalar(statement) or 0)

    def delete(self, order_id: UUID) -> bool:
        order = self._session.get(OrderModel, order_id)

        if order is None:
            return False

        self._session.delete(order)
        self._session.commit()

        return True
