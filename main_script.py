import requests
from zk import ZK, const

from datetime import datetime

def run_attendance_sync():
    try:

        headers = {
            "Authorization": "token 097f1319d483fab:0cba7c96b0601e1"
        }
        shift_type = requests.get(
            'https://stablemarine.erpzix.com:8894/api/resource/Shift Type?fields=["*"]',
            headers=headers,
            verify=False
        )
        res = shift_type.json()
        
        if "data" in res:
            last_sync = list(filter(lambda a: a["name"] == "Day", res["data"]))[0]["last_sync_of_checkin"]
            conn = ZK('192.168.0.126', port=4370, timeout=15, force_udp=False, ommit_ping=False)
            zk = conn.connect()

            zk.disable_device()

            attendances = zk.get_attendance()

            users = conn.get_users()
            zk.enable_device()

            zk.disconnect()

            result= {}
           
            now = datetime.now()
            try:
                start_date = datetime.strptime(last_sync, "%Y-%m-%d %H:%M:%S.%f")
            except ValueError:
                start_date = datetime.strptime(last_sync, "%Y-%m-%d %H:%M:%S")
            
            end_date = now  # keep as datetime, NOT string

            result = {}

            for record in attendances:
                log_time = record.timestamp  # assuming this is already a datetime object

                if log_time >= start_date and log_time <= end_date:
                    # print(f"{record.user_id} - {log_time}, BETWEEN {start_date} and {end_date}")

                    if record.user_id in result:
                        result[record.user_id].append(record.timestamp)
                    else:
                        result[record.user_id] = [record.timestamp]
                    
            
            for each, value in result.items():
                emp = requests.get(
                    'https://stablemarine.erpzix.com:8894/api/method/get_employee_id',
                    data={ "id": each },
                    headers=headers,
                    verify=False
                )
                data = {
                    "in":"",
                    "out":""
                }
                emp_id = emp.json()["message"]["data"]
                if emp_id:
                    prev = ''
                    for j in value:
                        body = {
                            "employee": emp_id, 
                            "time": j,
                            "log_type": "IN"
                        }
                        
                        if j.time().hour < 12:
                            if data["in"] != "":
                                print(((j - data["in"]).total_seconds() / 3600), 'Diffrence \n\n\n')
                            body["log_type"] = "IN"
                        else:
                            body["log_type"] = "OUT"
                        # if prev !="" :
                        #     print("\n\n\n\n\n NE W",j,prev, (j - prev).total_seconds() / 3600, 'Diffrence \n\n\n')
                        prev = j
                        response = requests.post(
                            "https://stablemarine.erpzix.com:8894/api/resource/Employee Checkin",
                            data=body,
                            headers=headers,
                            verify=False
                        )
                        if response.status_code != 200:
                            print("Failed \n\n\n\n")
            
            # Set Shift Type of Last Sync Checkin 
            updated = requests.put(
                'https://stablemarine.erpzix.com:8894/api/resource/Shift Type/Day',
                data={ "last_sync_of_checkin": end_date },
                headers=headers,
                verify=False
            )
            if updated.status_code != 200:
                return "Failed to Update Last Sync of Checkin"
            return {"success": "Sync Completed" }
    except Exception as e:
        print("Error:", e)
        return f"Error {e}"


run_attendance_sync()