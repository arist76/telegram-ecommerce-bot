import chromadb
from ecommerce_client import models
from app import settings

def dict_to_string(my_dict):
    if my_dict == None:
        return ""
    
    result = ""
    for key, value in my_dict.items():
        result += f"\t{key}: {value}\n"
    return result.rstrip("\n")

class ChromaSingleton():
    __client = None

    def __new__(cls):
        if cls.__client is None:
            cls.__client = super(ChromaSingleton, cls).__new__(cls)
            cls.__client = chromadb.PersistentClient(str(settings.BASE_DIR))
        return cls.__client
    

class Chromaclient():
    def __init__(self) -> None:
        self.__client = ChromaSingleton()
        self.__collection = self.__client.get_or_create_collection("products")

    def add(self, products : list[models.Product]) -> None:
        self.__collection.add(
            ids = [str(product.id) for product in products],
            documents = [
                self.format_product(product) for product in products
            ],
        )

    def upsert(self, products : list[models.Product]) -> None:
        self.__collection.add(
            ids = [str(product.id) for product in products],
            documents = [
                self.format_product(product) for product in products
            ],
        )

    def delete(self, products : list[models.Product]) -> None:
        self.__collection.delete(
            ids = [str(product.id) for product in products]
        )


    def query(self, q : str, n_results : int):
        results = self.__collection.query(
            query_texts=[q],
            n_results=n_results
        )

        result_ids = list(map(int, results.get("ids", [[]])[0]))
        result_distances = results.get("distances")[0]
        id_distance = dict(zip(result_ids, result_distances))

        queryset = models.Product.objects.filter(id__in = result_ids)


        return sorted(queryset, key=lambda x : id_distance[x.id])

    def get_all_ids(self) -> list[int]:
        return list(map(int ,self.__collection.get()["ids"]))
    
    def format_product(self, product : models.Product) -> str:
        return "\n".join([
            f"name: {product}",
            f"category: {product.category.name}",
            f"description: {product.description}",
            f"detailed_description: {dict_to_string(product.detailed_description)}",
            f"price: {product.price}"
        ])