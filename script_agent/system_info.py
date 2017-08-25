# -*- coding:utf-8 -*-
#支持在python2 环境下执行加入编码定义

import time
import subprocess


#定义服务器名及服务器IP,局点
server_name = 'SUSE-35'
server_ip = '192.168.0.35'
site_id = 'C10'

class getSystemInfo():

    #初始化函数判断文本是否存在,不存在则创建
    def __init__(self):
        self.file_name = 'system_info_' + time.strftime("%Y%m%d",time.localtime()) + '.txt'
        try:
            with open(self.file_name) as f:
                print("文件已存在，追加")
                pass
        except IOError:
            with open(self.file_name,'w') as f:
                print("文件不存在，已创建")
                pass

    #获取cpu信息,并写入文件
    """Cpu(s):  1.4%us,  0.4%sy,  0.0%ni, 97.9%id,  0.3%wa,  0.0%hi,  0.0%si,  0.0%st"""
    """server_name|server_ip|site_id|cpu|user_use|sys_use|io_use|idle|record_time"""
    def getCpuInfo(self):
        cmd = subprocess.Popen("top -b -n1|grep Cpu",shell=True,stdout=subprocess.PIPE)
        record_time = time.strftime("%Y%m%d%M%S",time.localtime())
        cpuinfo = cmd.stdout.readlines()[0]
        user_use = cpuinfo.split(' ')[2].split('%')[0]
        sys_use = cpuinfo.split(' ')[4].split('%')[0]
        io_use = cpuinfo.split(' ')[9].split('%')[0]
        idle = cpuinfo.split(' ')[7].split('%')[0]
        with open(self.file_name,'a') as f:
            line = server_name+'|'+server_ip+'|'+site_id+'|'+'cpu'+'|'+user_use+'|'+sys_use+'|'+io_use+'|'+idle+'|'+record_time+'\n'
            f.write(line)

    #获取内存信息,并写入文件
    """Mem:   8064424k total,  7987120k used,    77304k free,    44084k buffers"""
    """server_name|server_ip|site_id|mem|mem_use|mem_free|mem_buffer|mem_total|record_time"""
    def getMeminfo(self):
        cmd = subprocess.Popen("top -b -n1|grep Mem",shell=True,stdout=subprocess.PIPE)
        record_time = time.strftime("%Y%m%d%M%S",time.localtime())
        mem_info = cmd.stdout.readlines()[0]
        mem_use = mem_info.split(' ')[6].split('k')[0]
        mem_free = mem_info.split(' ')[11].split('k')[0]
        mem_buffer = mem_info.split(' ')[16].split('k')[0]
        mem_total = mem_info.split(' ')[3].split('k')[0]
        with open(self.file_name,'a') as f:
            line = server_name+'|'+server_ip+'|'+site_id+'|'+'mem'+'|'+mem_use+'|'+mem_free+'|'+mem_buffer+'|'+mem_total+'|'+record_time+'\n'
            f.write(line)


    #获取磁盘信息,并写入文件
    """
    server_name|server_ip|site_id|disk|/|disk_used|disk_total|record_time
    /dev/sda2             392G  108G  265G  29% /
    """
    def getDiskinfo(self):
        cmd = subprocess.Popen("df -hl|sed -n '2,$p'",shell=True,stdout=subprocess.PIPE)
        for line in cmd.stdout.readlines():
            record_time = time.strftime("%Y%m%d%M%S", time.localtime())
            disk_lun = line.split(' ')[-1].strip('\n')
            disk_uesd = line.split(' ')[-6]
            disk_total = line.split(' ')[-8]
            disk_line = server_name+'|'+server_ip+'|'+site_id+'|'+'disk'+'|'+disk_lun+'|'+disk_uesd+'|'+disk_total+'|'+record_time+'\n'
            with open(self.file_name,'a') as f:
                f.write(disk_line)




if __name__ == '__main__':
    sysinfo = getSystemInfo()
    sysinfo.getCpuInfo()
    sysinfo.getMeminfo()
    sysinfo.getDiskinfo()




