from dataclasses import dataclass
from functools import lru_cache
import yaml

@dataclass
class Resource():
    name: str
    production_ratio: float
    needs: list[str]

@lru_cache
def load_resources() -> dict[str, Resource]:
    resources_index: dict[str, Resource] = dict()
    with open("ratios.yaml") as ratios_file:
        ratios = yaml.safe_load(ratios_file)
    for i in ratios["latium"].items():
        resources_index[i[0]] = Resource(name=i[0], production_ratio=i[1]["rate"], needs=i[1]["needs"])
    return resources_index

def get_chains(resource_name: str, resource_rate: float, index: dict[str, Resource]) -> dict[str,  float]:
    chain = dict()
    needs = index[resource_name].needs
    ratio = index[resource_name].production_ratio
    for n in needs:
        chain[n] = (resource_rate/index[n].production_ratio)*ratio
    return chain

if __name__ == "__main__":
    index = load_resources()
    print(get_chains("sawmill", 1, index))
    print(get_chains("pileus", 2, index))
    print(get_chains("bread", 2, index))
    print(get_chains("amphorae", 2, index))
    print(get_chains("olive_oil", 3, index))
