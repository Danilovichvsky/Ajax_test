import re


def read_log_with_big(file):
    with open(file, "r", encoding="utf-8") as f:
        all_logs = []
        ok_ids = {}
        failed_detail = {}

        for line in f:
            if 'BIG' in line:
                all_logs.append(line)

        for log in all_logs:
            match = re.search(
                r"BIG;\d+;([A-Z0-9]{6});\d+;\d+;\d+;([0-9]{4});\d+;\d+;\d+;\d+;\d+;\d+;([0-9]{3}).*;(02|DD);", log)
            if match:
                sensor_id = match.group(1)
                spa_first = match.group(2)
                spa_second = match.group(3)
                state = match.group(4)

                if state == "02":
                    if sensor_id not in ok_ids:
                        ok_ids[sensor_id] = 0
                    ok_ids[sensor_id] += 1
                elif state == "DD":
                    # Обробка для помилок
                    spa_first = spa_first[:-1]
                    multi_spa = spa_first + spa_second
                    pairs = [multi_spa[i:i + 2] for i in range(0, len(multi_spa), 2)]

                    binary_pairs = [bin(int(pair, 16))[2:].zfill(8) for pair in pairs]
                    #print("binary_p", binary_pairs, f"----{sensor_id}")

                    errors = []
                    for i, binary in enumerate(binary_pairs):
                        if binary[4] == '1':  # 5-й прапорець (рахуємо з 1)
                            if i == 0:
                                errors.append("Battery device error")
                            if i == 1:
                                errors.append("Temperature device error")
                            if i == 2:
                                errors.append("Threshold central error")

                    if errors:
                        failed_detail[sensor_id] = errors
                    else:
                        failed_detail[sensor_id] = ["Unknown device error"]



        count_of_failed_logs = len(failed_detail)
        count_of_ok_logs = len(ok_ids)

        print("Count of messages with status OK:")
        for sensor_id, count in ok_ids.items():
            print(f"ID: {sensor_id}, Count: {count}")

        print(f"\nAll BIG messages: {count_of_ok_logs + count_of_failed_logs}")
        print(f"Successful BIG messages: {count_of_ok_logs}")
        print(f"Failed BIG messages: {count_of_failed_logs}")



        print("\nDetails of failed devices:")
        for sensor_id, errors in failed_detail.items():
            print(f"ID: {sensor_id}, Errors: {', '.join(errors)}")


# Виклик функції
read_log_with_big("app_2 (1) (1) (1) (2).log")
