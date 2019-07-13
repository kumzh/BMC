def memo_percent(free_memo,total_memo):
    obj_data = {
        "legend":["已使用","空闲"],
        "data":[{},{}]
    }
    free = 0
    total = 0
    for i in free_memo:
        free += int(i)
    for i in total_memo:
        total += int(i)
    per = round(free / total, 2)
    obj_data["data"][0]["value"] = per
    obj_data["data"][0]["name"] = "空闲"
    obj_data["data"][1]["value"] = round(1 - per, 2)
    obj_data["data"][1]["name"] = "已使用"

    return obj_data

def cpu_percent(free_cpu):
    obj_data = {
        "legend": ["已使用", "空闲"],
        "data": [{}, {}]
    }
    free = 0
    # print("free_cpu",free_cpu)
    for i in free_cpu:
        free += float(i)
    free_per = round(free / len(free_cpu),2)
    obj_data["data"][0]["value"] = free_per
    obj_data["data"][0]["name"] = "空闲"
    obj_data["data"][1]["value"] = round(100 - free_per, 2)
    obj_data["data"][1]["name"] = "已使用"
    return obj_data