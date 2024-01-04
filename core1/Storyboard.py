import requests
import json
import os
from urllib.parse import urlparse
import discord

def getChart(url,arg,json2,dpg,sb="0"):
    raw_data = requests.get(url).content.decode("utf-8")
    member = json.loads(raw_data)
    if sb == "1":
        member["chartBackup"]=member
        # 初始化陣列
    st = [0] * len(member["chartBackup"]["page_list"])  # start tick
    et = [0] * len(member["chartBackup"]["page_list"])  # end tick
    pgt = [0] * len(member["chartBackup"]["page_list"])  # page ticks
    drc = [0] * len(member["chartBackup"]["page_list"])  # scan line direction
    arg0 = [0] * len(member["chartBackup"]["page_list"])  # arguments 1
    arg1 = [0] * len(member["chartBackup"]["page_list"])  # arguments 2
    stp = [0] * len(member["chartBackup"]["page_list"])  # arg to noteY
    edp = [0] * len(member["chartBackup"]["page_list"])  # arg to noteY
    
    # 初始化陣列
    nid = [0] * len(member["chartBackup"]["note_list"])  # id
    ntk = [0] * len(member["chartBackup"]["note_list"])  # tick
    nht = [0] * len(member["chartBackup"]["note_list"])  # hold_tick
    nhs = [0] * len(member["chartBackup"]["note_list"])  # has_sibling
    nif = [0] * len(member["chartBackup"]["note_list"])  # is_forward
    nxd = [0] * len(member["chartBackup"]["note_list"])  # next_id
    ntp = [0] * len(member["chartBackup"]["note_list"])  # type
    npg = [0] * len(member["chartBackup"]["note_list"])  # page_index
    nx = [0] * len(member["chartBackup"]["note_list"])  # x
    ny = [0] * len(member["chartBackup"]["note_list"])  # y
    
    # 初始化陣列
    drg = [0] * len(member["chartBackup"]["note_list"])  # drag list
    drh = [0] * len(member["chartBackup"]["note_list"])  # drag list (drag head)

    for page in range(len(member["chartBackup"]["page_list"])):
        if arg == 1:
            arg0[page] = 1
            arg1[page] = 0
        elif arg == 0:
            arg0[page] = member["chartBackup"]["page_list"][page]["PositionFunction"]["Arguments"][0]
            arg1[page] = member["chartBackup"]["page_list"][page]["PositionFunction"]["Arguments"][1]
        st[page] = member["chartBackup"]["page_list"][page]["start_tick"]  # start tick
        et[page] = member["chartBackup"]["page_list"][page]["end_tick"]  # end tick
        pgt[page] = et[page] - st[page]
        drc[page] = member["chartBackup"]["page_list"][page]["scan_line_direction"]
        if drc[page] > 0:
            stp[page] = 0.5 * (arg1[page] - arg0[page] + 1)
            edp[page] = 0.5 * (arg1[page] + arg0[page] + 1)
        elif drc[page] < 0:
            stp[page] = 0.5 * (arg1[page] + arg0[page] + 1)
            edp[page] = 0.5 * (arg1[page] - arg0[page] + 1)
    for page in range(len(member["chartBackup"]["note_list"])):
        nid[page] = member["chartBackup"]["note_list"][page]["id"]
        ntk[page] = member["chartBackup"]["note_list"][page]["tick"]
        nht[page] = member["chartBackup"]["note_list"][page]["hold_tick"]
        nhs[page] = member["chartBackup"]["note_list"][page]["has_sibling"]
        nif[page] = member["chartBackup"]["note_list"][page]["is_forward"]
        nxd[page] = member["chartBackup"]["note_list"][page]["next_id"]
        ntp[page] = member["chartBackup"]["note_list"][page]["type"]
        npg[page] = member["chartBackup"]["note_list"][page]["page_index"]
        nx[page] = member["chartBackup"]["note_list"][page]["x"]
        r1 = npg[page]
        if nif[page]:
            npg[page] -= 1
        ny[page] = ((ntk[page] - st[r1]) * (edp[r1] - stp[r1]) / (et[r1] - st[r1])) + stp[r1]
        if ny[page] < 0:
            ny[page] = 0
        elif ny[page] > 1:
            ny[page] = 1
        w1 = 0
    w2 = 1
    w3 = 0
    n1 = 0
    for page in range(len(member["chartBackup"]["note_list"])):
        if ntp[page] == 3 or ntp[page] == 6:
            drh[w1] = nid[page]
            drg[page] = w1
            w3 = page
            while w2 > 0:
                n1 = nxd[w3]
                drg[n1] = w1
                w3 = n1
                if nxd[w3] == -1:
                    w2 = -1
            w1 += 1
            w2 = 1
    result_json = "["
    y1 = 0
    t1 = 0
    t2 = 0
    t4 = 0
    t5 = 0
    # 初始化 drgt2 列表
    drgt2 = [0] * len(member["chartBackup"]["note_list"])
    
    # 初始化 result_json 字串
    result_json = "["
    if json2>=120:
        json2=1.367*120/json2
    else:
        json2=1.367
    print(json2)
    for index in range(len(member["chartBackup"]["note_list"])):
        t1 = npg[index]
        y1 = ny[index]
        t4 = nid[index]
        t2 = 2.1 * drc[t1] + y1  # 將音符設為高處/低處
        mag = 1
    
        if abs(pgt[t1] - dpg) >= (dpg / 2):
            if pgt[t1] > dpg:
                mag = 1 + (pgt[t1] / dpg / 12)
            else:
                mag = 1 - (dpg / pgt[t1] / 12)
    
        intime = float(json2) * mag - 0.46
    
        if ntp[index] == 3 or ntp[index] == 6:
            intime = (float(json2) * 0.86 * mag) - 0.46
            drgt2[index] = t2  # 篩選drag頭
        if ntp[index] == 4 or ntp[index] == 7:
            intime = (float(json2) * 0.86 * mag) - 0.46
            t5 = drg[index]  # 將drag child依照drag頭位移
            t4 = drh[t5]
            t2 = drgt2[t4]
        y1 = "{:.4f}".format(y1)
        intime = "{:.3f}".format(intime)
    
        result_json += '{{"note": {}, "time": "intro:{}:-0.2", "override_y": true, "easing": "easeOutCubic", "comment": "storyboard_author=dyliu_{}", "y": "noteY:{}", "states": [{{"time": "intro:{}:{}", "y": "noteY:{}"}}]}}'.format(
            str(nid[index]), str(t4), str(nid[index]), str(float(t2)), str(t4), str(intime), str(float(y1)))
        if index < len(member["chartBackup"]["note_list"]) - 1:
            result_json += ","
    result_json += "]"
    result_json=json.loads(result_json)
    member["note_controllers"] = result_json
    path = urlparse(url).path
    filename = os.path.basename(path)
    with open("./text/drop_cache.json", 'w', encoding='utf-8') as file:
        json.dump(member, file, indent=2,ensure_ascii=False)
    file=discord.File("./text/drop_cache.json",filename=filename)
    return file



    