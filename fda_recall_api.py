import requests
import pandas as pd
import time


def main():
    def get_records():
        url = "https://api.fda.gov/device/recall.json"

        params = {'search': 'event_date_initiated:[20200101 TO 20221231]',
                  'limit': '1000'}

        recalls = requests.get(url, params=params)

        all_recalls = []

        for i in range(0, 100):

            time.sleep(1)

            params["skip"] = i * 1000

            print(recalls.url)

            recall_list = recalls.json()["results"]

            all_recalls.extend(recall_list)

            if recalls.status_code == 204:
                break

        print(recalls.json()["meta"]["results"]["total"])

        print(pd.DataFrame(all_recalls).info())

        frame = pd.DataFrame(all_recalls)

        return frame

    def muck_frame(frame):

        frame['event_date_initiated'] = pd.to_datetime(frame['event_date_initiated'])

        frame['month'] = frame['event_date_initiated'].dt.month

        frame['year'] = frame['event_date_initiated'].dt.year

        frame = frame[['recalling_firm', 'month', 'year', 'event_date_initiated', 'res_event_number']]

        grp_month = frame.groupby(['recalling_firm', 'month', 'year']).count().reset_index()

        grp_month['count_recalls'] = grp_month['res_event_number']

        grp_month = grp_month.drop(['res_event_number', 'event_date_initiated'], axis=1)

        print(grp_month)

        return grp_month

    def make_csv(grp_month):
        grp_month.to_csv(file.csv')

    make_csv(muck_frame(get_records()))


if __name__ == '__main__':
    main()
