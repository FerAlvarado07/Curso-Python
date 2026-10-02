import asyncio

from motor.motor_asyncio import AsyncIOMotorClient

MONGODB_URL = "mongodb://localhost:27017"


async def create_user(
    collection,
) -> None:
    user = {
        "name": "Fernando",
        "email": "fernando@example.com",
        "skills": [
            "Python",
            "Angular",
            "SQL",
        ],
    }

    result = await collection.insert_one(
        user,
    )

    print(f"Usuario creado: {result.inserted_id}")


async def get_user(
    collection,
) -> None:
    user = await collection.find_one(
        {
            "email": "fernando@example.com",
        }
    )

    print("Usuario:")
    print(user)


async def get_users(
    collection,
) -> None:
    cursor = collection.find()

    async for user in cursor:
        print(user)


async def main() -> None:
    client = AsyncIOMotorClient(
        MONGODB_URL,
    )

    database = client["curso_python"]

    collection = database["users"]

    try:
        await create_user(collection)

        await get_user(collection)

        print("\nTodos los usuarios:")

        await get_users(collection)

    finally:
        client.close()


if __name__ == "__main__":
    asyncio.run(main())
