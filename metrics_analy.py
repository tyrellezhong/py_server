import os
import re

tps_mo = 2912.62
tps_mno = 2943.53

rsp_av_mo = 56.28
rsp_av_mno = 49.70

rsp_90_mo = 85
rsp_90_mno = 65

tps_ratio = (tps_mo - tps_mno) / tps_mno * 100
rsp_av_ratio = (rsp_av_mo - rsp_av_mno) / rsp_av_mno * 100
rsp_90_ratio = (rsp_90_mo - rsp_90_mno) / rsp_90_mno * 100

print("tps_ratio={} rsp_av_ratio={} rsp_90_ratio={}".format(tps_ratio, rsp_av_ratio, rsp_90_ratio))


cpu_av_mo = 48.18
cpu_av_mno = 42.93

cpu_90_mo = 87.43
cpu_90_mno = 73.57

cpu_av_ratio = (cpu_av_mo - cpu_av_mno) / cpu_av_mno * 100
cpu_90_ratio = (cpu_90_mo - cpu_90_mno) / cpu_90_mno * 100

print("cpu_av_ratio={} cpu_90_ratio={}".format(cpu_av_ratio, cpu_90_ratio))


net_rd_mo = 30742954
net_rd_mno = 31548428

net_wt_mo = 26298548
net_wt_mno = 26974272

net_rd_ratio = (net_rd_mo - net_rd_mno) / net_rd_mno * 100
net_wt_ratio = (net_wt_mo - net_wt_mno) / net_wt_mno * 100

print("net_rd_ratio={} net_wt_ratio={}".format(net_rd_ratio, net_wt_ratio))

pkg_rd_mo = 5139.97
pkg_rd_mno = 5296.49

pkg_wt_mo = 5538.41
pkg_wt_mno = 5671.75

pkg_rd_ratio = (pkg_rd_mo - pkg_rd_mno) / pkg_rd_mno * 100
pkg_wt_ratio = (pkg_wt_mo - pkg_wt_mno) / pkg_wt_mno * 100

print("pkg_rd_ratio={} pkg_wt_ratio={}".format(pkg_rd_ratio, pkg_wt_ratio))


agent_cpu_av_mo = 1.91
agent_cpu_av_mno = 1.83

agent_cpu_90_mo = 3.01
agent_cpu_90_mno = 2.19

agent_cpu_av_ratio = (agent_cpu_av_mo - agent_cpu_av_mno) / agent_cpu_av_mno * 100
agent_cpu_90_ratio = (agent_cpu_90_mo - agent_cpu_90_mno) / agent_cpu_90_mno * 100

print("agent_cpu_av_ratio={} agent_cpu_90_ratio={}".format(agent_cpu_av_ratio, agent_cpu_90_ratio))


def get_submitter_p4() -> str:
    str_users = ''
    users = []
    svn_version = ''

    files = ['/data/taylorzhong/dsdev/CFR/Content/UI/PVE/BluePrints/HUD/Weapon/BP_PVEWeaponAutoTrackUIView.uasset',
             '/data/taylorzhong/dsdev/CFR/Content/Characters/PVE/MiaoNv/Abilities/Skill_20081001/BP_PVE_20081001_UIView_Test.uasset']

    for file in files:
        file += "#have"
        info = os.popen(r'p4 changes -m 1 ' + file)
        info_texts = info.readline()
        result = re.search(r'\s+(\w+)@', info_texts)
        if result:
            users.append(result.group(1))

        users = list(set(users))
        cout = 0
    for user in users:
        str_users += '<@' + user + '>  '
        cout += 1
        if cout >= 4:
            break
    return str_users

# print(get_submitter_p4())

o