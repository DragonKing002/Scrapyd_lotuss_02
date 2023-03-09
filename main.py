import os
from other import Outlook,Sharepoint,Secrect

def test_upload_files():

    sharepoint_url = "https://cpallgroup.sharepoint.com/sites/MST-MarketPriceCheckingforO2O"
    config =  Secrect().get_secret()
    username = config['username']
    password = config['password']

    # Check if the directory exists
    if not os.path.exists('Master Files'):
        # Create a new directory
        os.mkdir('Master Files')
    else:
        print('Directory already exists')

    try:
        s = Sharepoint(username, password, sharepoint_url)
        s.download_sharepoint('Master Files','Order_files.xlsx')
        s.upload_to_sharepoint('test directory', 'Order_files.xlsx')
    except Exception as e:
        print(e)

if __name__ == '__main__':

    test_upload_files()