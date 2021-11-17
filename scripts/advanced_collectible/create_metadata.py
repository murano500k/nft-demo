from brownie import AdvancedCollectible, network
from scripts.helpful_scripts import get_species
from metadata.sample_metadata import metadata_template
from pathlib import Path
import requests
import json
import os

species_to_image_uri = {
    "MARLA": "https://ipfs.io/ipfs/QmZPmdStrijPHySqb5z2yppwq4zpSBmcdjairRbm6PE3vb?filename=marla.png",
    "CAT_MAX": "https://ipfs.io/ipfs/QmNQBUyiDR85q5fDM3vjyiqFXgot4PgEQ323kFG535R56m?filename=cat-max.png",
    "CAT_MISHA": "https://ipfs.io/ipfs/QmeqnTKBseRjtB7PoekVC3UV6a9vSwwmAoFhVSLqPsYBbp?filename=cat-misha.png",
}


def main():
    advanced_collectible = AdvancedCollectible[-1]
    number_of_advanced_collectibles = advanced_collectible.tokenCounter()
    print(f"You have created {number_of_advanced_collectibles} collectibles!")
    for token_id in range(number_of_advanced_collectibles):
        species = get_species(advanced_collectible.tokenIdToSpecies(token_id))
        metadata_file_name = (
            f"./metadata/{network.show_active()}/{token_id}-{species}.json"
        )
        collectible_metadata = metadata_template
        if Path(metadata_file_name).exists():
            print(f"{metadata_file_name} already exists! Delete it to overwrite")
            print(f"{metadata_file_name}")
        else:
            print(f"Creating Metadata file: {metadata_file_name}")
            collectible_metadata["name"] = species
            collectible_metadata["description"] = f"An adorable {species} pet!"
            image_path = "./img/" + species.lower().replace("_", "-") + ".png"

            image_uri = None
            if os.getenv("UPLOAD_IPFS") == "true":
                image_uri = upload_to_ipfs(image_path)
            image_uri = image_uri if image_uri else species_to_image_uri[species]

            collectible_metadata["image"] = image_uri
            with open(metadata_file_name, "w") as file:
                json.dump(collectible_metadata, file)
            # if os.getenv("UPLOAD_IPFS") == "true":
            upload_to_ipfs(metadata_file_name)


# curl -X POST -F file=@metadata/rinkeby/0-SHIBA_INU.json http://localhost:5001/api/v0/add


def upload_to_ipfs(filepath):
    with Path(filepath).open("rb") as fp:
        image_binary = fp.read()
        ipfs_url = "http://127.0.0.1:5001"
        endpoint = "/api/v0/add"
        response = requests.post(ipfs_url + endpoint, files={"file": image_binary})
        ipfs_hash = response.json()["Hash"]
        # "./img/0-PUG.png" -> "0-PUG.png"
        filename = filepath.split("/")[-1:][0]
        image_uri = f"https://ipfs.io/ipfs/{ipfs_hash}?filename={filename}"
        print(image_uri)
        return image_uri
