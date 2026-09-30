from dataclasses import dataclass, field

from attrs import define
from pydantic import BaseModel, Field, field_validator

# 1. Clases


class User:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def greet(self):
        return f"Hola, soy {self.name}"


user = User("Fernando", 27)

print("Nombre:", user.name)
print("Edad:", user.age)
print(user.greet())


# 2. Herencia


class Animal:
    def __init__(self, name):
        self.name = name

    def speak(self):
        return "El animal hace un sonido"


class Dog(Animal):
    def speak(self):
        return "El perro ladra"


dog = Dog("Firulais")

print("\nHerencia:")
print("Nombre:", dog.name)
print("Sonido:", dog.speak())


# 3. Uso de super()


class Person:
    def __init__(self, name):
        self.name = name


class Employee(Person):
    def __init__(self, name, position):
        super().__init__(name)
        self.position = position


employee = Employee("Fernando", "Developer")

print("\nUso de super():")
print("Nombre:", employee.name)
print("Puesto:", employee.position)


# 4. Composición


class Engine:
    def start(self):
        return "Motor encendido"


class Car:
    def __init__(self):
        self.engine = Engine()

    def start(self):
        return self.engine.start()


car = Car()

print("\nComposición:")
print(car.start())


# 5. Dunder methods


class Product:
    def __init__(self, name, price):
        self.name = name
        self.price = price

    def __str__(self):
        return f"{self.name}: ${self.price}"

    def __repr__(self):
        return f"Product(name='{self.name}', price={self.price})"

    def __eq__(self, other):
        return self.price == other.price

    def __lt__(self, other):
        return self.price < other.price


product1 = Product("Laptop", 15000)
product2 = Product("PC", 15000)
product3 = Product("Mouse", 500)

print("\nDunder methods:")

print(product1)
print(repr(product1))

print("¿Mismo precio?", product1 == product2)
print("¿Laptop más barata que PC?", product1 < product2)
print("¿Mouse más barato que Laptop?", product3 < product1)


# 6. __len__


class ShoppingCart:
    def __init__(self, products):
        self.products = products

    def __len__(self):
        return len(self.products)


cart = ShoppingCart(
    [
        product1,
        product2,
        product3,
    ]
)

print("\n__len__:")
print("Productos en el carrito:", len(cart))


# 7. Dataclasses


@dataclass
class UserData:
    name: str
    age: int


user_data = UserData(
    name="Fernando",
    age=27,
)

print("\nDataclass:")
print(user_data)


# 8. Dataclass con valores por defecto


@dataclass
class UserProfile:
    name: str
    age: int = 18
    tags: list[str] = field(default_factory=list)


profile = UserProfile(
    name="Fernando",
    tags=["Python", "Angular"],
)

print("\nDataclass con valores por defecto:")
print(profile)


# 9. attrs


@define
class ProductData:
    name: str
    price: float


product_data = ProductData(
    name="Laptop",
    price=15000,
)

print("\nattrs:")
print(product_data)


# 10. Pydantic


class UserModel(BaseModel):
    name: str
    age: int


user_model = UserModel(
    name="Fernando",
    age=27,
)

print("\nPydantic:")
print(user_model)


# 11. Validación con Pydantic


class UserValidated(BaseModel):
    name: str
    age: int = Field(gt=0, lt=120)


user_validated = UserValidated(
    name="Fernando",
    age=27,
)

print("\nPydantic con validación:")
print(user_validated)


# 12. Validador personalizado


class UserComplete(BaseModel):
    name: str
    age: int = Field(gt=0, lt=120)

    @field_validator("name")
    @classmethod
    def validate_name(cls, value):
        if not value.strip():
            raise ValueError("El nombre no puede estar vacío")

        return value.strip()


user_complete = UserComplete(
    name=" Fernando ",
    age=27,
)

print("\nValidador personalizado:")
print(user_complete)


# 13. Serialización a diccionario

data = user_complete.model_dump()

print("\nSerialización a diccionario:")
print(data)


# 14. Serialización a JSON

json_data = user_complete.model_dump_json()

print("\nSerialización a JSON:")
print(json_data)


# 15. Crear modelo desde un diccionario

user_data = {
    "name": "Fernando",
    "age": 27,
}

user_from_dict = UserComplete.model_validate(user_data)

print("\nModelo desde diccionario:")
print(user_from_dict)


# 16. Ejemplo completo


class Address(BaseModel):
    street: str
    city: str
    zip_code: str


class Customer(BaseModel):
    name: str
    age: int = Field(gt=0)
    address: Address


customer = Customer(
    name="Fernando",
    age=27,
    address={
        "street": "Av. Principal",
        "city": "Ciudad de México",
        "zip_code": "06000",
    },
)

print("\nEjemplo completo:")
print(customer)

print("\nCliente como diccionario:")
print(customer.model_dump())

print("\nCliente como JSON:")
print(customer.model_dump_json())
