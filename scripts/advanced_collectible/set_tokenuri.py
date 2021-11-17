from brownie import network, AdvancedCollectible
from scripts.helpful_scripts import OPENSEA_URL, get_species, get_account

dog_metadata_dic = {
    "MARLA": "https://ipfs.io/ipfs/QmYfXiJu4mYiCYsWWkDWSNzY5QX4FDzyspK4xqua5PnNQZ?filename=10-MARLA.json",
    "CAT_MAX": "https://ipfs.io/ipfs/QmZu2WVgvK5XjVx2AKd6Sibc47NPgnY2xsne6y7ZJAq3vK?filename=0-CAT_MAX.json",
    "CAT_MISHA": "https://ipfs.io/ipfs/QmWZrM6wCGXr11nepjdnS4GS3rXE2sFitX9piDAkdg5ky1?filename=2-CAT_MISHA.json",
}


def main():
    print(f"Working on {network.show_active()}")
    advanced_collectible = AdvancedCollectible[-1]
    number_of_collectibles = advanced_collectible.tokenCounter()
    print(f"You have {number_of_collectibles} tokenIds")
    for token_id in range(number_of_collectibles):
        species = get_species(advanced_collectible.tokenIdToSpecies(token_id))
        if not advanced_collectible.tokenURI(token_id).startswith("https://"):
            print(f"Setting tokenURI of {token_id}")
            set_tokenURI(token_id, advanced_collectible, dog_metadata_dic[species])


def set_tokenURI(token_id, nft_contract, tokenURI):
    account = get_account()
    tx = nft_contract.setTokenURI(token_id, tokenURI, {"from": account})
    tx.wait(1)
    print(
        f"Awesome! You can view your NFT at {OPENSEA_URL.format(nft_contract.address, token_id)}"
    )
    print("Please wait up to 20 minutes, and hit the refresh metadata button")
