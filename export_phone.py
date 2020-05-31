import requests
import csv


def get_list_phone_from_pub(pub_id):
    offer_ids = ['amulet_vn', 'amuletthanhcong', 'vongchido_vn', 'vonggo', 'vonggosua', 'vongvang_vn']
    res = []
    for offer_id in offer_ids:
        resp = requests.get('http://pub.devas.network/report_phone?pub_id=' + pub_id + '&offer_id=' + offer_id)
        if resp.status_code == 200:
            json = resp.json()
            phones = json['data']
            for phone in phones:
                res.append((pub_id, offer_id, phone))
    return res


def main():
    result_list = []
    result_list = result_list + get_list_phone_from_pub('levietdatxp') + get_list_phone_from_pub('sunsea')
    with open('phone_list_with_pub_20200108.csv', 'w', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow(['PUB_NAME', 'OFFER_ID', 'PHONE'])
        for account in result_list:
            spamwriter.writerow([account[0], account[1], account[2]])


if __name__ == "__main__":
    main()
