
import requests
from . import APIUrls

def getState():
    """
    Shows informations about api.
    """

    headers = {'accept': 'application/json'}
    stateData = requests.get(APIUrls.lnapi+APIUrls.stateUrl,headers=headers)

    if stateData.status_code == 200:
        stateData = stateData.json()
        if stateData['state']['newPosition']:
            return stateData
        else:
            raise ValueError('New Positions currently not allowed')
    else:
        raise RuntimeError('Unable to fetch State Information: %s' % stateData.text)


def getNodeInformation():
    """
    Shows informations about the lightning node.
    """
    
    headers = {'accept': 'application/json'}
    nodeData = requests.get(APIUrls.lnapi+APIUrls.nodeUrl,headers=headers)

    if nodeData.status_code == 200:
        return nodeData.json()
    else:
        raise RuntimeError('Unable to fetch Node Information: %s' % nodeData.text)
