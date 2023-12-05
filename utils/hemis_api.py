import json
import requests


#  search techer by hemis_id
MY_TOKEN = "evoPgQkNb2QiG41GiE8DI_VqW1VYar-c"
SCHEDULE_LIST_URL = "https://talaba.tsue.uz/rest/v1/data/employee-list?type=teacher&search="

# todo:  API CALLING ----------------------------------


def hemis_api_call(hemis_id):
    headers = {"Authorization": f"Bearer {MY_TOKEN}"}
    response = requests.get(SCHEDULE_LIST_URL + str(hemis_id), headers=headers)
    res = response.json()["data"]["items"]
    if len(res)!=0:
        department=[]
        staff_position=[]
        for item in res:
            d = item['department']['name']
            s = item['staffPosition']['name']
            if (d not in department) or (s not in staff_position):
                department.append(item['department']['name'])
                staff_position.append(item['staffPosition']['name'])
                data={
                    'hemis_id': item['employee_id_number'],
                    'name': item['full_name'], 
                    'department': json.dumps(department),
                    'staff_position': json.dumps(staff_position)
                }
                # print('data', data)
        return data
    else:
        return [{
            "error_en": "The teacher is not available in the HEMIS Database of TSUE!",
            "error_uz": "O'qituvchi TDIU HEMIS Ma'lumotlar Bazasida mavjud emas!",
            "error_ru": "Преподавателя нет в базе данных ХЕМИС ТГЭУ!",
            }]


# todo: END ---------- API CALLING ---------------------
# hemis_api_call(3260211007)


# json_data = '[1, 2, 3, 4, 5]'
# data = json.loads(json_data)
# print(data, type(json_data))
