from typing import Protocol

"""
MÓDULO: PRINCIPIOS SOLID APLICADOS EN PYTHON

SOLID:
    S -> Single Responsibility Principle
    O -> Open/Closed Principle
    L -> Liskov Substitution Principle
    I -> Interface Segregation Principle
    D -> Dependency Inversion Principle
"""

# ============================================================
# 1. SRP - SINGLE RESPONSIBILITY PRINCIPLE
# ============================================================

"""
SRP significa:

    Single Responsibility Principle

Una clase o función debe tener una única responsabilidad.

En otras palabras:

    Una clase debería tener una sola razón para cambiar.

------------------------------------------------------------
EJEMPLO INCORRECTO
------------------------------------------------------------

Esta clase tiene demasiadas responsabilidades:

    - Crear usuarios
    - Validar usuarios
    - Guardar usuarios
    - Enviar correos
"""


class UserServiceBad:
    def create_user(self, name: str, email: str) -> None:
        # Crear usuario
        print(f"Usuario creado: {name}")

        # Validar email
        if "@" not in email:
            raise ValueError("Email inválido")

        # Guardar en base de datos
        print("Usuario guardado en la base de datos")

        # Enviar correo
        print(f"Correo enviado a {email}")


"""
El problema es que UserServiceBad tiene varias razones para cambiar:

    - Cambia la validación
    - Cambia la base de datos
    - Cambia el sistema de correo
    - Cambia la lógica de creación

------------------------------------------------------------
SOLUCIÓN
------------------------------------------------------------

Separamos las responsabilidades.
"""


class UserValidator:
    """Responsable únicamente de validar usuarios."""

    def validate_email(self, email: str) -> bool:
        return "@" in email


class UserRepository:
    """Responsable únicamente de almacenar usuarios."""

    def save(self, name: str, email: str) -> None:
        print(f"Usuario guardado: {name} - {email}")


class EmailService:
    """Responsable únicamente de enviar correos."""

    def send_welcome_email(self, email: str) -> None:
        print(f"Correo de bienvenida enviado a {email}")


class UserService:
    """
    Orquesta las diferentes responsabilidades.

    No valida directamente.
    No guarda directamente.
    No envía correos directamente.
    """

    def __init__(
        self,
        validator: UserValidator,
        repository: UserRepository,
        email_service: EmailService,
    ):
        self.validator = validator
        self.repository = repository
        self.email_service = email_service

    def create_user(
        self,
        name: str,
        email: str,
    ) -> None:
        if not self.validator.validate_email(email):
            raise ValueError("Email inválido")

        self.repository.save(name, email)

        self.email_service.send_welcome_email(email)


# ============================================================
# 2. OCP - OPEN/CLOSED PRINCIPLE
# ============================================================

"""
OCP significa:

    Open/Closed Principle

Una entidad debe estar:

    - abierta para extensión
    - cerrada para modificación

Es decir, debemos poder agregar comportamiento sin modificar
constantemente el código existente.

------------------------------------------------------------
EJEMPLO PROBLEMÁTICO
------------------------------------------------------------

Una solución poco flexible sería utilizar if/elif:

    if payment_type == "card":
        ...
    elif payment_type == "paypal":
        ...
    elif payment_type == "crypto":
        ...

Cada nuevo método obliga a modificar la clase.
"""


class CardPayment:
    def pay(self, amount: float) -> None:
        print(f"Pago con tarjeta: ${amount:.2f}")


class PaypalPayment:
    def pay(self, amount: float) -> None:
        print(f"Pago con PayPal: ${amount:.2f}")


class CryptoPayment:
    def pay(self, amount: float) -> None:
        print(f"Pago con criptomonedas: ${amount:.2f}")


class PaymentProcessor:
    """
    No necesita conocer los tipos concretos de pago.

    Se limita a utilizar el método pay().
    """

    def process(
        self,
        payment_method,
        amount: float,
    ) -> None:
        payment_method.pay(amount)


"""
Ahora podemos agregar nuevos métodos sin modificar
PaymentProcessor.
"""


class BankTransferPayment:
    def pay(self, amount: float) -> None:
        print(f"Transferencia bancaria: ${amount:.2f}")


# ============================================================
# 3. LSP - LISKOV SUBSTITUTION PRINCIPLE
# ============================================================

"""
LSP significa:

    Liskov Substitution Principle

Una implementación concreta debe poder sustituir a la abstracción
sin romper el comportamiento esperado.

Una forma sencilla de entenderlo:

    Si una función espera un objeto que puede "pagar",
    cualquier implementación válida debe poder utilizarse
    sin producir comportamientos inesperados.

------------------------------------------------------------
EJEMPLO CORRECTO
------------------------------------------------------------

Todas las implementaciones tienen el mismo contrato:

    pay(amount)
"""


class Payment:
    def pay(self, amount: float) -> None:
        raise NotImplementedError


class CreditCardPayment(Payment):
    def pay(self, amount: float) -> None:
        print(f"Pago con tarjeta de crédito: ${amount:.2f}")


class DebitCardPayment(Payment):
    def pay(self, amount: float) -> None:
        print(f"Pago con tarjeta de débito: ${amount:.2f}")


def execute_payment(
    payment: Payment,
    amount: float,
) -> None:
    payment.pay(amount)


"""
Podemos sustituir Payment por cualquiera de sus implementaciones:

    CreditCardPayment
    DebitCardPayment

sin modificar execute_payment().
"""


# ============================================================
# 4. ISP - INTERFACE SEGREGATION PRINCIPLE
# ============================================================

"""
ISP significa:

    Interface Segregation Principle

Los clientes no deberían estar obligados a depender de métodos
que no necesitan.

En Python esto se puede implementar muy bien utilizando
Protocols pequeños y específicos.

------------------------------------------------------------
MAL DISEÑO
------------------------------------------------------------

Un único contrato demasiado grande:

    Printer
        - print()
        - scan()
        - fax()

Una impresora sencilla que solamente imprime estaría obligada
a implementar métodos que no necesita.
"""


class PrinterBad:
    def print(self, document: str) -> None:
        print(f"Imprimiendo: {document}")

    def scan(self) -> None:
        print("Escaneando")

    def fax(self) -> None:
        print("Enviando fax")


"""
------------------------------------------------------------
MEJOR DISEÑO
------------------------------------------------------------

Creamos contratos pequeños.
"""


class Printable(Protocol):
    def print(self, document: str) -> None: ...


class Scannable(Protocol):
    def scan(self) -> None: ...


class Faxable(Protocol):
    def fax(self) -> None: ...


class SimplePrinter:
    def print(self, document: str) -> None:
        print(f"Imprimiendo: {document}")


class MultifunctionPrinter:
    def print(self, document: str) -> None:
        print(f"Imprimiendo: {document}")

    def scan(self) -> None:
        print("Escaneando")

    def fax(self) -> None:
        print("Enviando fax")


def print_document(
    printer: Printable,
    document: str,
) -> None:
    printer.print(document)


"""
SimplePrinter solamente necesita cumplir con Printable.

No necesita implementar scan() ni fax().
"""


# ============================================================
# 5. DIP - DEPENDENCY INVERSION PRINCIPLE
# ============================================================

"""
DIP significa:

    Dependency Inversion Principle

Los módulos de alto nivel no deberían depender directamente
de módulos de bajo nivel.

Ambos deberían depender de abstracciones.

------------------------------------------------------------
EJEMPLO PROBLEMÁTICO
------------------------------------------------------------

OrderService depende directamente de MySQLRepository.
"""


class MySQLRepository:
    def save(self, data: str) -> None:
        print(f"Guardando en MySQL: {data}")


class OrderServiceBad:
    def __init__(self):
        self.repository = MySQLRepository()

    def create_order(self, order: str) -> None:
        self.repository.save(order)


"""
Problemas:

    - OrderService conoce MySQL.
    - Es difícil cambiar a PostgreSQL.
    - Es difícil hacer pruebas.
    - Existe un acoplamiento fuerte.

------------------------------------------------------------
SOLUCIÓN
------------------------------------------------------------

OrderService dependerá de una abstracción.
"""


class Repository(Protocol):
    def save(self, data: str) -> None: ...


class PostgreSQLRepository:
    def save(self, data: str) -> None:
        print(f"Guardando en PostgreSQL: {data}")


class InMemoryRepository:
    """
    Implementación útil para pruebas.
    """

    def __init__(self):
        self.data: list[str] = []

    def save(self, data: str) -> None:
        self.data.append(data)


class OrderService:
    """
    No conoce MySQL, PostgreSQL ni ninguna implementación concreta.

    Depende del contrato Repository.
    """

    def __init__(
        self,
        repository: Repository,
    ):
        self.repository = repository

    def create_order(self, order: str) -> None:
        self.repository.save(order)


# ============================================================
# 6. PROTOCOLS
# ============================================================

"""
En Python podemos utilizar typing.Protocol para definir contratos
sin necesidad de crear jerarquías de herencia.

Esto se conoce como:

    Structural Typing

Un objeto cumple el contrato si tiene los métodos requeridos.

No es necesario heredar explícitamente del Protocol.
"""


class Logger(Protocol):
    def log(self, message: str) -> None: ...


class ConsoleLogger:
    def log(self, message: str) -> None:
        print(f"[LOG] {message}")


class FileLogger:
    def log(self, message: str) -> None:
        print(f"[FILE] {message}")


def process_data(
    logger: Logger,
) -> None:
    logger.log("Procesando información")


"""
ConsoleLogger y FileLogger cumplen el contrato Logger.

No necesitan heredar de Logger.
"""


# ============================================================
# 7. FACTORY PATTERN
# ============================================================

"""
Una Factory encapsula la creación de objetos.

En lugar de repartir lógica de creación por toda la aplicación,
podemos centralizarla.
"""


class Notification(Protocol):
    def send(self, message: str) -> None: ...


class EmailNotification:
    def send(self, message: str) -> None:
        print(f"Email: {message}")


class SmsNotification:
    def send(self, message: str) -> None:
        print(f"SMS: {message}")


class PushNotification:
    def send(self, message: str) -> None:
        print(f"Push notification: {message}")


class NotificationFactory:
    """
    Factory responsable de crear notificaciones.
    """

    @staticmethod
    def create(
        notification_type: str,
    ) -> Notification:
        notifications = {
            "email": EmailNotification,
            "sms": SmsNotification,
            "push": PushNotification,
        }

        notification_class = notifications.get(notification_type)

        if notification_class is None:
            raise ValueError(f"Tipo de notificación no soportado: {notification_type}")

        return notification_class()


# ============================================================
# 8. PROVIDER PATTERN
# ============================================================

"""
Un Provider suministra una dependencia.

Es especialmente útil cuando queremos controlar cómo se obtiene
un objeto.

Por ejemplo:

    Database
    Logger
    API Client
    Configuration

El consumidor no necesita saber cómo se construye.
"""


class Database(Protocol):
    def query(self, sql: str) -> list[str]: ...


class InMemoryDatabase:
    def query(self, sql: str) -> list[str]:
        print(f"Ejecutando query: {sql}")

        return [
            "Fernando",
            "Ana",
            "Luis",
        ]


def database_provider() -> Database:
    """
    Provider.

    Decide qué implementación proporcionar.
    """

    return InMemoryDatabase()


class UserQueryService:
    def __init__(
        self,
        database: Database,
    ):
        self.database = database

    def get_users(self) -> list[str]:
        return self.database.query("SELECT * FROM users")


"""
La aplicación puede obtener la dependencia mediante el Provider:

    database = database_provider()

    service = UserQueryService(database)
"""


# ============================================================
# 9. ACOPLAMIENTO
# ============================================================

"""
Acoplamiento:

    Mide qué tan dependiente es un componente de otros componentes.

------------------------------------------------------------
ALTO ACOPLAMIENTO
------------------------------------------------------------

Una clase crea y conoce directamente sus dependencias.
"""


class ReportServiceBad:
    def __init__(self):
        self.database = MySQLRepository()
        self.logger = ConsoleLogger()


"""
ReportServiceBad conoce implementaciones concretas.

Esto genera mayor acoplamiento.

------------------------------------------------------------
BAJO ACOPLAMIENTO
------------------------------------------------------------

Utilizamos Dependency Injection.
"""


class ReportService:
    def __init__(
        self,
        database: Repository,
        logger: Logger,
    ):
        self.database = database
        self.logger = logger

    def generate(self) -> None:
        self.logger.log("Generando reporte")

        self.database.save("Reporte generado")


"""
Ahora ReportService no sabe si utiliza:

    MySQL
    PostgreSQL
    memoria
    un mock
    otro sistema

Solo conoce los contratos.
"""


# ============================================================
# 10. COHESIÓN
# ============================================================

"""
Cohesión:

    Mide qué tan relacionadas están las responsabilidades
    dentro de un componente.

Alta cohesión:

    Una clase tiene responsabilidades relacionadas.

Baja cohesión:

    Una clase hace muchas cosas que no tienen relación.

------------------------------------------------------------
BAJA COHESIÓN
------------------------------------------------------------

Una clase que:

    - Calcula salarios
    - Envía emails
    - Guarda usuarios
    - Genera reportes

tiene demasiadas responsabilidades.
"""


class CompanyServiceBad:
    def calculate_salary(self):
        pass

    def send_email(self):
        pass

    def save_user(self):
        pass

    def generate_report(self):
        pass


"""
------------------------------------------------------------
ALTA COHESIÓN
------------------------------------------------------------

Separamos las responsabilidades.
"""


class SalaryCalculator:
    def calculate(self, salary: float) -> float:
        return salary * 1.16


class UserRepositoryService:
    def save(self, user: str) -> None:
        print(f"Guardando usuario: {user}")


class ReportGenerator:
    def generate(self) -> str:
        return "Reporte generado"


# ============================================================
# 11. TESTABILIDAD
# ============================================================

"""
Una buena arquitectura facilita las pruebas.

El Dependency Injection + Protocol permite sustituir
dependencias reales por implementaciones falsas.

Por ejemplo:

    Production:
        PostgreSQLRepository

    Test:
        FakeRepository
"""


class FakeRepository:
    def __init__(self):
        self.saved_data: list[str] = []

    def save(self, data: str) -> None:
        self.saved_data.append(data)


def test_order_service() -> None:
    """
    Ejemplo conceptual de una prueba.

    No necesitamos una base de datos real.
    """

    repository = FakeRepository()

    service = OrderService(repository)

    service.create_order("Order #123")

    assert repository.saved_data == ["Order #123"]


# ============================================================
# 12. EJEMPLO INTEGRADOR
# ============================================================

"""
Este ejemplo combina varios principios SOLID.

Tenemos:

    Protocol
        ↓
    Repository

    Factory
        ↓
    Repository implementation

    Dependency Injection
        ↓
    OrderService

Principios involucrados:

    SRP
        Cada clase tiene una responsabilidad.

    OCP
        Podemos agregar nuevos repositorios.

    LSP
        Los repositorios pueden sustituirse.

    ISP
        Los contratos son pequeños.

    DIP
        OrderService depende de Repository,
        no de una implementación concreta.
"""


class OrderRepository(Protocol):
    def save(self, order: str) -> None: ...

    def find(self, order_id: int) -> str | None: ...


class MemoryOrderRepository:
    def __init__(self):
        self.orders: dict[int, str] = {}

    def save(self, order: str) -> None:
        order_id = len(self.orders) + 1

        self.orders[order_id] = order

    def find(self, order_id: int) -> str | None:
        return self.orders.get(order_id)


class OrderServiceFinal:
    """
    Servicio de alto nivel.

    Depende del Protocol OrderRepository.
    """

    def __init__(
        self,
        repository: OrderRepository,
    ):
        self.repository = repository

    def create_order(
        self,
        order: str,
    ) -> None:
        self.repository.save(order)

    def get_order(
        self,
        order_id: int,
    ) -> str | None:
        return self.repository.find(order_id)


# ============================================================
# 13. MAIN
# ============================================================


def main() -> None:
    print("========================================")
    print(" PRINCIPIOS SOLID EN PYTHON")
    print("========================================")

    # --------------------------------------------------------
    # SRP
    # --------------------------------------------------------

    print("\n--- SRP ---")

    validator = UserValidator()
    repository = UserRepository()
    email_service = EmailService()

    user_service = UserService(
        validator,
        repository,
        email_service,
    )

    user_service.create_user(
        "Fernando",
        "fernando@example.com",
    )

    # --------------------------------------------------------
    # OCP
    # --------------------------------------------------------

    print("\n--- OCP ---")

    processor = PaymentProcessor()

    processor.process(
        CardPayment(),
        100,
    )

    processor.process(
        PaypalPayment(),
        200,
    )

    processor.process(
        BankTransferPayment(),
        300,
    )

    # --------------------------------------------------------
    # LSP
    # --------------------------------------------------------

    print("\n--- LSP ---")

    execute_payment(
        CreditCardPayment(),
        500,
    )

    execute_payment(
        DebitCardPayment(),
        250,
    )

    # --------------------------------------------------------
    # ISP
    # --------------------------------------------------------

    print("\n--- ISP ---")

    printer = SimplePrinter()

    print_document(
        printer,
        "Documento importante",
    )

    # --------------------------------------------------------
    # DIP
    # --------------------------------------------------------

    print("\n--- DIP ---")

    memory_repository = InMemoryRepository()

    order_service = OrderService(memory_repository)

    order_service.create_order("Order #001")

    print(memory_repository.data)

    # --------------------------------------------------------
    # Protocol
    # --------------------------------------------------------

    print("\n--- PROTOCOL ---")

    process_data(ConsoleLogger())

    process_data(FileLogger())

    # --------------------------------------------------------
    # Factory
    # --------------------------------------------------------

    print("\n--- FACTORY ---")

    notification = NotificationFactory.create("email")

    notification.send("Hola Fernando")

    # --------------------------------------------------------
    # Provider
    # --------------------------------------------------------

    print("\n--- PROVIDER ---")

    database = database_provider()

    query_service = UserQueryService(database)

    users = query_service.get_users()

    print(users)

    # --------------------------------------------------------
    # Testabilidad
    # --------------------------------------------------------

    print("\n--- TESTABILIDAD ---")

    test_order_service()

    print("Test ejecutado correctamente")

    order_repository = MemoryOrderRepository()

    service = OrderServiceFinal(order_repository)

    service.create_order("Laptop")

    print(service.get_order(1))

    print("\n========================================")
    print(" FIN")
    print("========================================")


if __name__ == "__main__":
    main()
