from src.main import (
    Car,
    Customer,
    Dog,
    Product,
    ProductData,
    User,
    UserComplete,
    UserData,
)


def test_user():
    user = User("Fernando", 27)

    assert user.name == "Fernando"
    assert user.age == 27
    assert user.greet() == "Hola, soy Fernando"


def test_dog():
    dog = Dog("Firulais")

    assert dog.name == "Firulais"
    assert dog.speak() == "El perro ladra"


def test_car():
    car = Car()

    assert car.start() == "Motor encendido"


def test_product():
    product = Product("Laptop", 15000)

    assert str(product) == "Laptop: $15000"


def test_user_data():
    user = UserData("Fernando", 27)

    assert user.name == "Fernando"
    assert user.age == 27


def test_product_data():
    product = ProductData("Laptop", 15000)

    assert product.name == "Laptop"
    assert product.price == 15000


def test_user_complete():
    user = UserComplete(
        name="Fernando",
        age=27,
    )

    assert user.name == "Fernando"
    assert user.age == 27


def test_customer():
    customer = Customer(
        name="Fernando",
        age=27,
        address={
            "street": "Av. Principal",
            "city": "Ciudad de México",
            "zip_code": "06000",
        },
    )

    assert customer.name == "Fernando"
    assert customer.address.city == "Ciudad de México"
