from typing import Union

import asyncpg
from asyncpg.pool import Pool

from data import config


class Database:
    def __init__(self):
        self.pool: Union[Pool, None] = None

    async def create(self):
        pool = await asyncpg.create_pool(
            user=config.PGUSER,
            password=config.PGPASSWORD,
            host=config.IP,
            database=config.DATABASE
        )
        self.pool = pool

    async def create_tables(self):
        sql = """
        CREATE TABLE Users(
        user_id int NOT NULL,
        user_name varchar(50),
        PRIMARY KEY(user_id)
        );
        CREATE TABLE Refuels(
        user_id int REFERENCES Users,
        date timestamp NOT NULL,
        price NUMERIC NOT NULL,
        liters NUMERIC NOT NULL,
        mileage int NOT NULL,
        per_liter NUMERIC,
        PRIMARY KEY(date)
        );
        """
        await self.pool.execute(sql)

    @staticmethod
    def format_args1(sql, parameters: dict):
        sql += ' AND '.join([
            f'{item} = ${num + 1}' for num, item in enumerate(parameters)
        ]) + ' ORDER BY date DESC LIMIT 5 '
        return sql, tuple(parameters.values())

    async def add_user(self, user_id: int, user_name: str):
        sql = "INSERT INTO Users(user_id, user_name) VALUES($1, $2)"
        await self.pool.execute(sql, user_id, user_name)

    async def add_refuel(self, user_id: int, date: int, price: float, liters: float, mileage: int, per_liter: float):
        sql = "INSERT INTO Refuels(user_id, date, price, liters ,mileage, per_liter) VALUES($1, $2, $3, $4, $5, $6)"
        await self.pool.execute(sql, user_id, date, price, liters, mileage, per_liter)

    async def select_last_five_refuels(self, **kwargs):
        sql = "SELECT * FROM Refuels WHERE "
        sql, parameters = self.format_args1(sql, kwargs)
        print(sql)
        return await self.pool.fetch(sql, *parameters)

    @staticmethod
    def format_args2(sql, parameters: dict):
        sql += ' AND '.join([
            f'{item} = ${num + 1}' for num, item in enumerate(parameters)
        ])
        return sql, tuple(parameters.values())

    async def select_max_per_liter(self, **kwargs):
        sql = "SELECT MAX(per_liter) FROM Refuels WHERE "
        sql, parameters = self.format_args2(sql, kwargs)
        print(sql)
        return await self.pool.fetch(sql, *parameters)

    async def select_min_per_liter(self, **kwargs):
        sql = "SELECT MIN(per_liter) FROM Refuels WHERE "
        sql, parameters = self.format_args2(sql, kwargs)
        print(sql)
        return await self.pool.fetch(sql, *parameters)

    async def select_count_refuels(self, **kwargs):
        sql = "SELECT COUNT(*) FROM Refuels WHERE "
        sql, parameters = self.format_args2(sql, kwargs)
        print(sql)
        return await self.pool.fetch(sql, *parameters)

    async def select_sum_price(self, **kwargs):
        sql = "SELECT SUM(price) FROM Refuels WHERE "
        sql, parameters = self.format_args2(sql, kwargs)
        print(sql)
        return await self.pool.fetch(sql, *parameters)
