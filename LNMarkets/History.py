
import requests
from . import APIUrls


def getIndex():
    """
    Retrieves index value.
    """

    headers = {
        'accept': 'application/json',
    }
    indexData = requests.get(
        APIUrls.lnapi+APIUrls.indexUrl,
        headers=headers,
    )

    if indexData.status_code == 200:
        return indexData.json()
    else:
        raise RuntimeError(
            'Unable to fetch index data:\n'
            f'{indexData.text}'
        )


def getBidOffer():
    """
    Retrieves bid-offer values.
    """

    headers = {
        'accept': 'application/json',
    }
    bidOfferData = requests.get(
        APIUrls.lnapi+APIUrls.bidOfferUrl,
        headers=headers,
    )

    if bidOfferData.status_code == 200:
        return bidOfferData.json()
    else:
        raise RuntimeError(
            'Unable to fetch index data:\n'
            f'{bidOfferData.text}'
        )
