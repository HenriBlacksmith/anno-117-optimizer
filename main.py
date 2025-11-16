from functools import lru_cache
import json
import yaml

from models import ProductionChain, ResidentType, Resource

@lru_cache
def load_resources() -> dict[str, Resource]:
    resources_index: dict[str, Resource] = dict()
    with open("ratios.yaml") as ratios_file:
        ratios = yaml.safe_load(ratios_file)
    for i in ratios["latium"].items():
        resources_index[i[0]] = Resource(
            name=i[0],
            production_ratio=i[1]["rate"],
            needs=i[1]["needs"],
            workforce=i[1]["workforce"],
        )
    return resources_index


def get_chains(
    resource_name: str, resource_rate: float, index: dict[str, Resource]
) -> ProductionChain:
    chain: ProductionChain = dict()
    needs = index[resource_name].needs
    ratio = index[resource_name].production_ratio
    for n in needs:
        chain[n] = (resource_rate / index[n].production_ratio) * ratio
    return chain


def compute_required_workforce(
    chain: ProductionChain, index: dict[str, Resource]
) -> dict[ResidentType, float]:
    total_workforce: dict[ResidentType, float] = {
        ResidentType.LIBERTI: 0,
        ResidentType.PLEBEIAN: 0,
    }
    for resource in chain.items():
        for item in index[resource[0]].workforce:
            total_workforce[item.type] += item.count * resource[1]
    return total_workforce


if __name__ == "__main__":
    index = load_resources()
    print(json.dumps(compute_required_workforce(get_chains("tiles", 2, index), index), indent=2))
