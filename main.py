from abc import ABC, abstractmethod


class Storage(ABC):
    @abstractmethod
    def __init__(self, items, capacity):
        self._items = items
        self._capacity = int(capacity)

    @abstractmethod
    def add(self, title, count):
        pass

    @abstractmethod
    def remove(self, title, count):
        pass

    @property
    @abstractmethod
    def get_free_space(self):
        pass

    @property
    @abstractmethod
    def items(self):
        pass

    @property
    @abstractmethod
    def get_unique_items_count(self):
        pass


class Store(Storage):
    def __init__(self):
        self._items = {}
        self._capacity = 100

    def add(self, title, count):
        if title in self._items:
            self._items[title] += count
        else:
            self._items[title] = count
        self._capacity -= count

    def remove(self, title, count):
        result = self._items[title] - count
        if result > 0:
            self._items[title] = result
        else:
            del self._items[title]
        self._capacity += count

    @property
    def get_free_space(self):
        return self._capacity

    @property
    def items(self):
        return self._items

    @items.setter
    def items(self, new_items):
        self._items = new_items
        self._capacity -= sum(self._items.values())

    @property
    def get_unique_items_count(self):
        return len(self._items.keys())


class Shop(Store):
    def __init__(self):
        super().__init__()
        self._capacity = 20


class Request:
    def __init__(self, info):
        self.info = self._split_info(info)
        self.from_ = self.info[4]
        self.to = self.info[6]
        self.amount = int(self.info[1])
        self.product = self.info[2]

    @staticmethod
    def _split_info(info):
        return info.split(" ")

    def __repr__(self):
        return f"Доставить {self.amount} {self.product} из {self.from_} в {self.to}"


def main():
    while True:
        print("Добро пожаловать в онлайн магазин")
        user_input = input("Введите запрос: ")

        if user_input == "stop":
            break

        while True:

            request = Request(user_input)

            from_ = store if request.from_ == "склад" else shop
            to = store if request.to == "склад" else shop

            if request.product in from_.items:
                print(f"Нужный товар ({request.product}) есть в пункте \"{request.from_}\"")
            else:
                print(f"Не хватает товара в пункте {request.from_}, попробуйте заказать меньше")
                break

            if from_.items[request.product] >= request.amount:
                print(f"Нужное количество товара есть в пункте \"{request.from_}\"")
            else:
                print(f"В пункте {request.from_}, не хватает "
                      f"{request.amount - from_.items[request.product]} {request.product}, попробуйте заказать меньше")
                break

            if to.get_free_space >= request.amount:
                print(f"В пункте \"{request.to}\" достаточно места")

            else:
                print(f"В пункте {request.to}, не хватает места для "
                      f"{request.amount - to.get_free_space} {request.product}")
                break

            if request.to == "магазин" and to.get_unique_items_count == 5 and request.product not in to.items:
                print("В магазине достаточно уникальных значений")
                break

            from_.remove(request.product, request.amount)

            print(f"Курьер забрал {request.amount} {request.product} из пункта {request.from_}")
            print(f"Курьер везет {request.amount} {request.product} из пункта {request.from_} в пункт {request.to}")

            to.add(request.product, request.amount)

            print(f"Курьер доставил {request.amount} {request.product} в пункт {request.to}")

            print("=" * 30)
            print("На складе хранится:")
            for title, count in store_items.items():
                print(f"{title}:{count}")
            print(f"Свободного места: {store.get_free_space}")

            print("=" * 30)
            print("В магазине хранится:")
            for title, count in shop.items.items():
                print(f"{title}:{count}")
            print(f"Свободного места: {shop.get_free_space}")
            print("=" * 30)
            break


if __name__ == "__main__":

    store = Store()
    shop = Shop()

    store_items = {
        "чипсы": 10,
        "макароны": 20,
        "печеньки": 30
    }

    store.items = store_items
    main()
