from dataclasses import dataclass

"""
MÓDULO: PATRONES DE DISEÑO EN PYTHON

CONTENIDO:

1. ¿Qué son los patrones de diseño?
2. Patrones Creacionales
   - Factory
   - Abstract Factory
   - Builder
   - Singleton
3. Patrones Estructurales
   - Adapter
   - Facade
   - Composite
   - Decorator
   - Proxy
4. Patrones de Comportamiento
   - Strategy
   - Observer
   - Command
   - Mediator
   - Template Method
   - State
5. Patrones Idiomáticos de Python
   - Decoradores
   - Context Managers
   - Dataclasses
6. Resumen: cuándo utilizar cada patrón


======================================================================
1. ¿QUÉ SON LOS PATRONES DE DISEÑO?
======================================================================

Un patrón de diseño es una solución reutilizable para un problema
común de diseño de software.

Un patrón NO es una biblioteca ni código que debamos copiar
exactamente.

Es una guía para estructurar nuestras clases, funciones y objetos.

Los patrones normalmente se clasifican en:

    Creacionales
        Se enfocan en cómo crear objetos.

    Estructurales
        Se enfocan en cómo combinar objetos y clases.

    De comportamiento
        Se enfocan en cómo los objetos colaboran entre sí.

En Python muchos patrones clásicos pueden implementarse de manera
más sencilla gracias a:

    - funciones de primera clase
    - duck typing
    - Protocol
    - decoradores
    - context managers
    - dataclasses
"""

# ======================================================================
# 2. PATRONES CREACIONALES
# ======================================================================

"""
Los patrones creacionales ayudan a controlar y organizar la creación
de objetos.

Principales patrones:

    Factory
    Abstract Factory
    Builder
    Singleton


----------------------------------------------------------------------
2.1 FACTORY
----------------------------------------------------------------------

PROBLEMA:

Tenemos que crear diferentes objetos dependiendo de algún dato,
pero no queremos que el código cliente conozca todos los detalles
de creación.

SOLUCIÓN:

Centralizar la creación de objetos en una función o clase Factory.

En Python, una Factory muchas veces puede ser simplemente una función.
"""


class EmailNotification:
    def send(self, message: str) -> None:
        print(f"Email: {message}")


class SmsNotification:
    def send(self, message: str) -> None:
        print(f"SMS: {message}")


def create_notification(
    notification_type: str,
):
    if notification_type == "email":
        return EmailNotification()

    if notification_type == "sms":
        return SmsNotification()

    raise ValueError(f"Tipo de notificación no soportado: {notification_type}")


def factory_example() -> None:
    notification = create_notification("email")

    notification.send("Hola Fernando")


"""
VENTAJAS:

    - Centraliza la creación.
    - Reduce acoplamiento.
    - Facilita agregar nuevas implementaciones.

CUÁNDO USARLO:

    Cuando la creación de objetos tiene lógica.
    Cuando existen diferentes implementaciones.
    Cuando el código cliente no debería conocer las clases concretas.

En Python:

    No siempre necesitamos una clase Factory.
    Una función puede ser suficiente.
"""


# ----------------------------------------------------------------------
# 2.2 ABSTRACT FACTORY
# ----------------------------------------------------------------------

"""
PROBLEMA:

Necesitamos crear familias de objetos relacionados.

Por ejemplo:

    WindowsButton
    WindowsCheckbox

o:

    MacButton
    MacCheckbox

Queremos asegurarnos de que los objetos creados pertenecen a la
misma familia.
"""


class Button:
    def render(self) -> None:
        raise NotImplementedError


class Checkbox:
    def render(self) -> None:
        raise NotImplementedError


class WindowsButton(Button):
    def render(self) -> None:
        print("Windows Button")


class WindowsCheckbox(Checkbox):
    def render(self) -> None:
        print("Windows Checkbox")


class MacButton(Button):
    def render(self) -> None:
        print("Mac Button")


class MacCheckbox(Checkbox):
    def render(self) -> None:
        print("Mac Checkbox")


class UIFactory:
    def create_button(self) -> Button:
        raise NotImplementedError

    def create_checkbox(self) -> Checkbox:
        raise NotImplementedError


class WindowsUIFactory(UIFactory):
    def create_button(self) -> Button:
        return WindowsButton()

    def create_checkbox(self) -> Checkbox:
        return WindowsCheckbox()


class MacUIFactory(UIFactory):
    def create_button(self) -> Button:
        return MacButton()

    def create_checkbox(self) -> Checkbox:
        return MacCheckbox()


def abstract_factory_example() -> None:
    factory = WindowsUIFactory()

    button = factory.create_button()
    checkbox = factory.create_checkbox()

    button.render()
    checkbox.render()


"""
ABSTRACT FACTORY:

    Factory
       |
       +-- Button
       |
       +-- Checkbox

Permite crear una familia completa de objetos compatibles.

CUÁNDO USARLO:

    Cuando existen múltiples familias de objetos relacionados.

EJEMPLO:

    Windows UI
    Mac UI
    Dark theme
    Light theme
"""


# ----------------------------------------------------------------------
# 2.3 BUILDER
# ----------------------------------------------------------------------

"""
PROBLEMA:

Tenemos objetos complejos que requieren muchos parámetros.

Ejemplo:

    User(
        name,
        email,
        age,
        phone,
        address,
        role,
        active
    )

Esto puede volverse difícil de leer.

SOLUCIÓN:

Construir el objeto paso a paso.
"""


@dataclass
class User:
    name: str
    email: str
    age: int | None = None
    phone: str | None = None
    role: str = "user"


class UserBuilder:
    def __init__(
        self,
        name: str,
        email: str,
    ) -> None:
        self.user = User(
            name=name,
            email=email,
        )

    def with_age(
        self,
        age: int,
    ) -> "UserBuilder":
        self.user.age = age

        return self

    def with_phone(
        self,
        phone: str,
    ) -> "UserBuilder":
        self.user.phone = phone

        return self

    def with_role(
        self,
        role: str,
    ) -> "UserBuilder":
        self.user.role = role

        return self

    def build(self) -> User:
        return self.user


def builder_example() -> None:
    user = (
        UserBuilder(
            "Fernando",
            "fernando@example.com",
        )
        .with_age(30)
        .with_phone("5555555555")
        .with_role("admin")
        .build()
    )

    print(user)


"""
VENTAJAS:

    - Construcción paso a paso.
    - Código más legible.
    - Permite diferentes configuraciones.

IMPORTANTE:

En Python muchas veces un Builder es innecesario.

Podemos utilizar:

    dataclasses
    argumentos con valores por defecto
    keyword arguments

Por ejemplo:

    User(
        name="Fernando",
        email="fernando@example.com",
        role="admin",
    )

Si el objeto es sencillo, probablemente NO necesitas Builder.
"""


# ----------------------------------------------------------------------
# 2.4 SINGLETON
# ----------------------------------------------------------------------

"""
PROBLEMA:

Queremos que exista una única instancia de una clase.

Ejemplos clásicos:

    configuración global
    logger
    conexión compartida

Sin embargo...

EN PYTHON GENERALMENTE DEBEMOS EVITAR SINGLETON.

¿Por qué?

Porque introduce estado global y aumenta el acoplamiento.

También dificulta:

    - testing
    - dependency injection
    - paralelismo
    - mantenimiento


Una implementación sencilla sería:
"""


class Singleton:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)

        return cls._instance


def singleton_example() -> None:
    first = Singleton()
    second = Singleton()

    print(first is second)


"""
Resultado:

    True

PERO...

En lugar de Singleton normalmente es preferible:

    - Dependency Injection
    - una instancia compartida administrada por composición
    - funciones o módulos
    - providers

Ejemplo:

    service = MyService(database)

    En lugar de:

    service = MyService()
    # busca un Singleton global


REGLA:

    Si puedes evitar Singleton, evítalo.
"""


# ======================================================================
# 3. PATRONES ESTRUCTURALES
# ======================================================================

"""
Los patrones estructurales se enfocan en cómo combinar objetos.

Incluyen:

    Adapter
    Facade
    Composite
    Decorator
    Proxy
"""


# ----------------------------------------------------------------------
# 3.1 ADAPTER
# ----------------------------------------------------------------------

"""
PROBLEMA:

Tenemos una clase existente cuya interfaz no coincide con la interfaz
que necesita nuestro código.

SOLUCIÓN:

Crear un Adapter.
"""


class OldPaymentSystem:
    def make_payment(
        self,
        amount: float,
    ) -> None:
        print(f"Pago antiguo: ${amount}")


class PaymentAdapter:
    def __init__(
        self,
        old_system: OldPaymentSystem,
    ) -> None:
        self.old_system = old_system

    def pay(
        self,
        amount: float,
    ) -> None:
        self.old_system.make_payment(amount)


def adapter_example() -> None:
    old_system = OldPaymentSystem()

    payment = PaymentAdapter(old_system)

    payment.pay(100)


"""
El código cliente utiliza:

    payment.pay()

Aunque internamente existe:

    old_system.make_payment()

El Adapter traduce una interfaz en otra.

CUÁNDO USARLO:

    Cuando integramos:

        APIs externas
        librerías antiguas
        sistemas legacy
        servicios con interfaces incompatibles
"""


# ----------------------------------------------------------------------
# 3.2 FACADE
# ----------------------------------------------------------------------

"""
PROBLEMA:

Un sistema tiene muchas clases y operaciones.

El cliente no debería conocer todos los detalles.

SOLUCIÓN:

Crear una interfaz sencilla que esconda la complejidad.
"""


class InventoryService:
    def check_product(
        self,
        product: str,
    ) -> bool:
        print(f"Checking inventory: {product}")

        return True


class PaymentService:
    def charge(
        self,
        amount: float,
    ) -> None:
        print(f"Charging ${amount}")


class ShippingService:
    def ship(
        self,
        product: str,
    ) -> None:
        print(f"Shipping: {product}")


class OrderFacade:
    def __init__(self) -> None:
        self.inventory = InventoryService()
        self.payment = PaymentService()
        self.shipping = ShippingService()

    def place_order(
        self,
        product: str,
        amount: float,
    ) -> None:
        if not self.inventory.check_product(product):
            raise ValueError("Product unavailable")

        self.payment.charge(amount)

        self.shipping.ship(product)


def facade_example() -> None:
    facade = OrderFacade()

    facade.place_order(
        "Laptop",
        1500,
    )


"""
El cliente solamente necesita:

    facade.place_order()

No necesita conocer:

    InventoryService
    PaymentService
    ShippingService

CUÁNDO USARLO:

    Cuando un subsistema es complejo.
    Cuando queremos una API sencilla.
"""


# ----------------------------------------------------------------------
# 3.3 COMPOSITE
# ----------------------------------------------------------------------

"""
PROBLEMA:

Queremos tratar objetos individuales y grupos de objetos de la
misma manera.

Ejemplo:

    File
    Folder

Una carpeta contiene archivos y otras carpetas.
"""


class File:
    def __init__(
        self,
        name: str,
    ) -> None:
        self.name = name

    def show(self) -> None:
        print(f"File: {self.name}")


class Folder:
    def __init__(
        self,
        name: str,
    ) -> None:
        self.name = name
        self.children = []

    def add(self, item) -> None:
        self.children.append(item)

    def show(self) -> None:
        print(f"Folder: {self.name}")

        for child in self.children:
            child.show()


def composite_example() -> None:
    root = Folder("Root")

    root.add(File("document.txt"))

    images = Folder("Images")

    images.add(File("photo.jpg"))

    root.add(images)

    root.show()


"""
La ventaja es que podemos llamar:

    item.show()

Sin importar si item es:

    File
    Folder

Esto crea una estructura tipo árbol.
"""


# ----------------------------------------------------------------------
# 3.4 DECORATOR
# ----------------------------------------------------------------------

"""
PROBLEMA:

Queremos agregar comportamiento a una función u objeto sin modificar
su código original.

Python tiene soporte nativo para Decorator.
"""


def log_execution(function):
    def wrapper(*args, **kwargs):
        print(f"Executing {function.__name__}")

        result = function(*args, **kwargs)

        print(f"Finished {function.__name__}")

        return result

    return wrapper


@log_execution
def calculate_total(
    price: float,
    quantity: int,
) -> float:
    return price * quantity


def decorator_example() -> None:
    result = calculate_total(
        100,
        3,
    )

    print(result)


"""
Un decorador permite agregar:

    logging
    authentication
    caching
    validation
    timing
    authorization

sin modificar la función original.
"""


# ----------------------------------------------------------------------
# 3.5 PROXY
# ----------------------------------------------------------------------

"""
PROBLEMA:

Queremos controlar el acceso a otro objeto.

El Proxy actúa como intermediario.

Puede utilizarse para:

    - logging
    - cache
    - autorización
    - lazy loading
"""


class Database:
    def get_user(
        self,
        user_id: int,
    ) -> str:
        print("Consultando base de datos...")

        return f"User {user_id}"


class DatabaseProxy:
    def __init__(
        self,
        database: Database,
    ) -> None:
        self.database = database
        self.cache = {}

    def get_user(
        self,
        user_id: int,
    ) -> str:
        if user_id in self.cache:
            print("Returning cached user")

            return self.cache[user_id]

        user = self.database.get_user(user_id)

        self.cache[user_id] = user

        return user


def proxy_example() -> None:
    database = Database()

    proxy = DatabaseProxy(database)

    print(proxy.get_user(1))
    print(proxy.get_user(1))


"""
El Proxy controla el acceso al objeto real.
"""


# ======================================================================
# 4. PATRONES DE COMPORTAMIENTO
# ======================================================================

"""
Estos patrones se enfocan en cómo los objetos colaboran y distribuyen
responsabilidades.

Incluyen:

    Strategy
    Observer
    Command
    Mediator
    Template Method
    State
"""


# ----------------------------------------------------------------------
# 4.1 STRATEGY
# ----------------------------------------------------------------------

"""
PROBLEMA:

Tenemos diferentes algoritmos para realizar una operación.

Queremos poder cambiar el algoritmo sin modificar el código cliente.
"""


class CreditCardPayment:
    def pay(
        self,
        amount: float,
    ) -> None:
        print(f"Paying ${amount} with credit card")


class PayPalPayment:
    def pay(
        self,
        amount: float,
    ) -> None:
        print(f"Paying ${amount} with PayPal")


class PaymentProcessor:
    def __init__(
        self,
        payment_method,
    ) -> None:
        self.payment_method = payment_method

    def process(
        self,
        amount: float,
    ) -> None:
        self.payment_method.pay(amount)


def strategy_example() -> None:
    processor = PaymentProcessor(CreditCardPayment())

    processor.process(100)

    processor = PaymentProcessor(PayPalPayment())

    processor.process(100)


"""
El algoritmo puede cambiar en tiempo de ejecución.

Esto es Strategy.

En Python podemos implementar Strategy fácilmente con:

    funciones
    lambdas
    Protocol
    clases
"""


# ----------------------------------------------------------------------
# 4.2 OBSERVER
# ----------------------------------------------------------------------

"""
PROBLEMA:

Cuando ocurre un evento, necesitamos notificar a múltiples objetos.

Ejemplo:

    Order created

Debe notificarse a:

    EmailService
    NotificationService
    AnalyticsService
"""


class Observer:
    def update(
        self,
        message: str,
    ) -> None:
        raise NotImplementedError


class EmailObserver(Observer):
    def update(
        self,
        message: str,
    ) -> None:
        print(f"Email notification: {message}")


class LoggingObserver(Observer):
    def update(
        self,
        message: str,
    ) -> None:
        print(f"Log: {message}")


class EventManager:
    def __init__(self) -> None:
        self.observers = []

    def subscribe(
        self,
        observer: Observer,
    ) -> None:
        self.observers.append(observer)

    def notify(
        self,
        message: str,
    ) -> None:
        for observer in self.observers:
            observer.update(message)


def observer_example() -> None:
    events = EventManager()

    events.subscribe(EmailObserver())

    events.subscribe(LoggingObserver())

    events.notify("Order created")


"""
Observer crea una relación:

    Subject
       |
       +---- Observer
       +---- Observer
       +---- Observer

Útil para sistemas orientados a eventos.
"""


# ----------------------------------------------------------------------
# 4.3 COMMAND
# ----------------------------------------------------------------------

"""
PROBLEMA:

Queremos convertir una operación en un objeto.

Esto permite:

    - almacenar comandos
    - ejecutarlos posteriormente
    - deshacer operaciones
    - crear colas
"""


class Light:
    def turn_on(self) -> None:
        print("Light ON")

    def turn_off(self) -> None:
        print("Light OFF")


class TurnOnCommand:
    def __init__(
        self,
        light: Light,
    ) -> None:
        self.light = light

    def execute(self) -> None:
        self.light.turn_on()


class TurnOffCommand:
    def __init__(
        self,
        light: Light,
    ) -> None:
        self.light = light

    def execute(self) -> None:
        self.light.turn_off()


def command_example() -> None:
    light = Light()

    turn_on = TurnOnCommand(light)

    turn_off = TurnOffCommand(light)

    turn_on.execute()
    turn_off.execute()


"""
La operación:

    light.turn_on()

se convierte en:

    TurnOnCommand(light)

y posteriormente:

    command.execute()
"""


# ----------------------------------------------------------------------
# 4.4 MEDIATOR
# ----------------------------------------------------------------------

"""
PROBLEMA:

Tenemos muchos objetos que necesitan comunicarse entre ellos.

Sin Mediator:

    A -> B
    A -> C
    B -> C
    C -> A

El acoplamiento aumenta.

SOLUCIÓN:

Centralizar la comunicación.
"""


class ChatMediator:
    def send(
        self,
        message: str,
        sender,
    ) -> None:
        raise NotImplementedError


class User:
    def __init__(
        self,
        name: str,
        mediator: ChatMediator,
    ) -> None:
        self.name = name
        self.mediator = mediator

    def send(
        self,
        message: str,
    ) -> None:
        self.mediator.send(message, self)

    def receive(
        self,
        message: str,
    ) -> None:
        print(f"{self.name} received: {message}")


class ChatRoom(ChatMediator):
    def __init__(self) -> None:
        self.users = []

    def add_user(
        self,
        user: User,
    ) -> None:
        self.users.append(user)

    def send(
        self,
        message: str,
        sender: User,
    ) -> None:
        for user in self.users:
            if user != sender:
                user.receive(message)


def mediator_example() -> None:
    chat = ChatRoom()

    user1 = User(
        "Fernando",
        chat,
    )

    user2 = User(
        "Ana",
        chat,
    )

    chat.add_user(user1)
    chat.add_user(user2)

    user1.send("Hola Ana")


"""
Mediator centraliza la comunicación.

Los usuarios no necesitan conocer directamente a los demás usuarios.
"""


# ----------------------------------------------------------------------
# 4.5 TEMPLATE METHOD
# ----------------------------------------------------------------------

"""
PROBLEMA:

Tenemos algoritmos que siguen los mismos pasos, pero algunos pasos
cambian dependiendo de la implementación.

SOLUCIÓN:

Definir la estructura general y permitir que las subclases implementen
los pasos variables.
"""


class DataProcessor:
    def process(self) -> None:
        self.load_data()
        self.validate_data()
        self.save_data()

    def load_data(self) -> None:
        raise NotImplementedError

    def validate_data(self) -> None:
        raise NotImplementedError

    def save_data(self) -> None:
        raise NotImplementedError


class CsvProcessor(DataProcessor):
    def load_data(self) -> None:
        print("Loading CSV")

    def validate_data(self) -> None:
        print("Validating CSV")

    def save_data(self) -> None:
        print("Saving CSV")


class JsonProcessor(DataProcessor):
    def load_data(self) -> None:
        print("Loading JSON")

    def validate_data(self) -> None:
        print("Validating JSON")

    def save_data(self) -> None:
        print("Saving JSON")


def template_method_example() -> None:
    processor = CsvProcessor()

    processor.process()


"""
La estructura siempre es:

    load
      |
    validate
      |
    save

Pero cada implementación decide cómo realizar cada paso.
"""


# ----------------------------------------------------------------------
# 4.6 STATE
# ----------------------------------------------------------------------

"""
PROBLEMA:

El comportamiento de un objeto cambia dependiendo de su estado.

Ejemplo:

    Order

Estados:

    Pending
    Paid
    Shipped
"""


class OrderState:
    def pay(self, order) -> None:
        raise NotImplementedError

    def ship(self, order) -> None:
        raise NotImplementedError


class PendingState(OrderState):
    def pay(self, order) -> None:
        print("Order paid")

        order.state = PaidState()

    def ship(self, order) -> None:
        print("Cannot ship unpaid order")


class PaidState(OrderState):
    def pay(self, order) -> None:
        print("Order already paid")

    def ship(self, order) -> None:
        print("Order shipped")

        order.state = ShippedState()


class ShippedState(OrderState):
    def pay(self, order) -> None:
        print("Cannot pay shipped order")

    def ship(self, order) -> None:
        print("Order already shipped")


class Order:
    def __init__(self) -> None:
        self.state = PendingState()

    def pay(self) -> None:
        self.state.pay(self)

    def ship(self) -> None:
        self.state.ship(self)


def state_example() -> None:
    order = Order()

    order.ship()

    order.pay()

    order.ship()


"""
En lugar de tener:

    if state == "pending":
        ...

    elif state == "paid":
        ...

    elif state == "shipped":
        ...

Cada estado encapsula su propio comportamiento.
"""


# ======================================================================
# 5. PATRONES IDIOMÁTICOS DE PYTHON
# ======================================================================

"""
Python tiene características propias que permiten implementar patrones
de manera mucho más sencilla.

Tres ejemplos importantes:

    Decoradores
    Context Managers
    Dataclasses
"""


# ----------------------------------------------------------------------
# 5.1 DECORADORES
# ----------------------------------------------------------------------

"""
Un decorador recibe una función y devuelve otra función.

Se utiliza con:

    @decorator
"""


def log_call(function):
    def wrapper(*args, **kwargs):
        print(f"Calling {function.__name__}")

        return function(*args, **kwargs)

    return wrapper


@log_call
def greet(
    name: str,
) -> None:
    print(f"Hello {name}")


def python_decorator_example() -> None:
    greet("Fernando")


"""
Los decoradores son muy utilizados para:

    logging
    authentication
    caching
    authorization
    validation
    retries
"""


# ----------------------------------------------------------------------
# 5.2 CONTEXT MANAGERS
# ----------------------------------------------------------------------

"""
Un Context Manager controla la entrada y salida de un bloque.

Se utiliza con:

    with


Ejemplo clásico:

    with open("file.txt") as file:
        ...


Podemos crear nuestro propio Context Manager.
"""


class DatabaseConnection:
    def __enter__(self):
        print("Opening connection")

        return self

    def __exit__(
        self,
        exc_type,
        exc_value,
        traceback,
    ):
        print("Closing connection")


def context_manager_example() -> None:
    with DatabaseConnection():
        print("Executing query")


"""
El Context Manager garantiza que el código de limpieza se ejecute.

Muy útil para:

    archivos
    conexiones
    locks
    transacciones
    recursos externos


También podemos utilizar:

    contextlib.contextmanager

para crear context managers basados en funciones.
"""


# ----------------------------------------------------------------------
# 5.3 DATACLASSES
# ----------------------------------------------------------------------

"""
Las dataclasses permiten crear clases enfocadas principalmente
en almacenar datos.

Python genera automáticamente:

    __init__
    __repr__
    __eq__

entre otros métodos.
"""


@dataclass
class Product:
    name: str
    price: float
    stock: int = 0


def dataclass_example() -> None:
    product = Product(
        name="Laptop",
        price=1500,
        stock=10,
    )

    print(product)


"""
En lugar de escribir manualmente:

    __init__
    __repr__
    __eq__

podemos utilizar:

    @dataclass

Las dataclasses son ideales para:

    DTOs
    modelos de datos
    configuraciones
    objetos de valor
"""


# ======================================================================
# 6. RESUMEN
# ======================================================================

"""
======================================================================
PATRONES CREACIONALES
======================================================================

Factory
    Centraliza la creación de objetos.

    Úsalo cuando:
        Existen diferentes implementaciones.

Abstract Factory
    Crea familias de objetos relacionados.

    Úsalo cuando:
        Necesitas objetos compatibles entre sí.

Builder
    Construye objetos complejos paso a paso.

    Úsalo cuando:
        La construcción tiene muchos parámetros o pasos.

Singleton
    Garantiza una única instancia.

    Úsalo con precaución.

    En Python:
        Preferir Dependency Injection cuando sea posible.


======================================================================
PATRONES ESTRUCTURALES
======================================================================

Adapter
    Convierte una interfaz en otra.

    Útil para:
        APIs externas
        Legacy
        Librerías incompatibles.


Facade
    Simplifica un sistema complejo.

    Útil cuando:
        Tenemos muchos servicios internos.


Composite
    Trata objetos individuales y grupos de objetos de la misma forma.

    Útil para:
        árboles
        archivos/carpetas
        componentes UI.


Decorator
    Agrega comportamiento sin modificar el objeto original.

    Útil para:
        logging
        caching
        autorización
        validación.


Proxy
    Controla el acceso a otro objeto.

    Útil para:
        cache
        seguridad
        lazy loading
        logging


======================================================================
PATRONES DE COMPORTAMIENTO
======================================================================

Strategy
    Permite intercambiar algoritmos.

    Útil para:
        diferentes métodos de pago
        diferentes algoritmos
        diferentes reglas de negocio.


Observer
    Notifica a múltiples objetos cuando ocurre un evento.

    Útil para:
        eventos
        notificaciones
        sistemas reactivos.


Command
    Convierte una operación en un objeto.

    Útil para:
        colas
        undo/redo
        acciones diferidas.


Mediator
    Centraliza la comunicación entre objetos.

    Útil cuando:
        Muchos objetos se comunican entre sí.


Template Method
    Define la estructura de un algoritmo.

    Útil cuando:
        Varios algoritmos comparten los mismos pasos.


State
    Cambia el comportamiento dependiendo del estado.

    Útil cuando:
        Tenemos muchos if/elif relacionados con estados.


======================================================================
PATRONES IDIOMÁTICOS DE PYTHON
======================================================================

Decorators
    Agregan comportamiento a funciones o clases.

Context Managers
    Controlan recursos utilizando:

        with

Dataclasses
    Simplifican clases destinadas principalmente a almacenar datos.


======================================================================
7. ¿CÓMO ELEGIR UN PATRÓN?
======================================================================

No debemos utilizar patrones solamente porque existen.

Primero debemos identificar el problema.

Por ejemplo:

    "Tengo diferentes formas de calcular un precio"

        -> Strategy


    "Tengo que crear diferentes tipos de objetos"

        -> Factory


    "Una API externa tiene una interfaz incompatible"

        -> Adapter


    "Tengo muchos servicios y quiero simplificar su uso"

        -> Facade


    "Necesito agregar logging a muchas funciones"

        -> Decorator


    "El comportamiento depende del estado"

        -> State


    "Tengo que notificar a múltiples componentes"

        -> Observer


    "Necesito controlar el acceso a un objeto"

        -> Proxy


    "Tengo un proceso con pasos fijos pero implementaciones
     diferentes"

        -> Template Method


    "Necesito construir un objeto complejo"

        -> Builder
"""
