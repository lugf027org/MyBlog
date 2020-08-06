import math

import xlrd
import xlwt

def main():
    # 读取Excel
    wk = xlrd.open_workbook(r'a.xlsx')
    # 获取目标EXCEL文件sheet名
    sheets = wk.sheet_names()

    # 根据表索引
    ws = wk.sheet_by_index(0)
    # 获取总行数
    nrows = ws.nrows
    # 获取总列数
    ncols = ws.ncols
    print(nrows)
    print(ncols)
    print(wk.sheet_names())
    cellA=ws.cell(0,0).value
    print(cellA)

    results = []
    #result[0]=[000004, 1, 10, 0, ]

    for i in range(0, nrows):
        print(i)
        global exits
        exits = 0
        for j in range(0, len(results)):
            aaa = ws.cell(i, 0).value
            aab = ws.cell(i, 1).value
            aac = math.ceil(ws.cell(i, 2).value/3)
            # 数据已在临时结果中
            if aaa == results[j][0] and aab == results[j][1] and aac == results[j][2]:
                # 最大值比较
                if (ws.cell(i, 3).value > results[j][3]):
                    results[j][3] = ws.cell(i, 3).value
                if (ws.cell(i, 4).value > results[j][5]):
                    results[j][5] = ws.cell(i, 4).value
                if (ws.cell(i, 5).value > results[j][7]):
                    results[j][7] = ws.cell(i, 5).value
                if (ws.cell(i, 6).value > results[j][9]):
                    results[j][9] = ws.cell(i, 6).value
                if (ws.cell(i, 7).value > results[j][11]):
                    results[j][11] = ws.cell(i, 7).value
                if (ws.cell(i, 8).value > results[j][13]):
                    results[j][13] = ws.cell(i, 8).value
                if (ws.cell(i, 9).value > results[j][15]):
                    results[j][15] = ws.cell(i, 9).value
                if (ws.cell(i, 10).value > results[j][17]):
                    results[j][17] = ws.cell(i, 10).value
                if (ws.cell(i, 11).value > results[j][19]):
                    results[j][19] = ws.cell(i, 11).value
                if (ws.cell(i, 12).value > results[j][21]):
                    results[j][21] = ws.cell(i, 12).value
                # 最小值比较
                if (ws.cell(i, 3).value < results[j][4]):
                    results[j][4] = ws.cell(i, 3).value
                if (ws.cell(i, 4).value < results[j][6]):
                    results[j][6] = ws.cell(i, 4).value
                if (ws.cell(i, 5).value < results[j][8]):
                    results[j][8] = ws.cell(i, 5).value
                if (ws.cell(i, 6).value < results[j][10]):
                    results[j][10] = ws.cell(i, 6).value
                if (ws.cell(i, 7).value < results[j][12]):
                    results[j][12] = ws.cell(i, 7).value
                if (ws.cell(i, 8).value < results[j][14]):
                    results[j][14] = ws.cell(i, 8).value
                if (ws.cell(i, 9).value < results[j][16]):
                    results[j][16] = ws.cell(i, 9).value
                if (ws.cell(i, 10).value < results[j][18]):
                    results[j][18] = ws.cell(i, 10).value
                if (ws.cell(i, 11).value < results[j][20]):
                    results[j][20] = ws.cell(i, 11).value
                if (ws.cell(i, 12).value < results[j][22]):
                    results[j][22] = ws.cell(i, 12).value
                exits = 1
                break

        if exits == 0:

            tmp = [ws.cell(i, 0).value, ws.cell(i, 1).value,
                   math.ceil(ws.cell(i, 2).value/3),
                   ws.cell(i, 3).value, ws.cell(i, 3).value,
                   ws.cell(i, 4).value, ws.cell(i, 4).value,
                   ws.cell(i, 5).value, ws.cell(i, 5).value,
                   ws.cell(i, 6).value, ws.cell(i, 6).value,
                   ws.cell(i, 7).value, ws.cell(i, 7).value,
                   ws.cell(i, 8).value, ws.cell(i, 8).value,
                   ws.cell(i, 9).value, ws.cell(i, 9).value,
                   ws.cell(i, 10).value, ws.cell(i, 10).value,
                   ws.cell(i, 11).value, ws.cell(i, 11).value,
                   ws.cell(i, 12).value, ws.cell(i, 12).value,
                   ]

            results.append(tmp)
        else:
            exits = 0

    # 写文件
    writebook = xlwt.Workbook()  # 打开excel
    test = writebook.add_sheet('test')  # 添加一个名字叫test的sheet
    for k in range(0, len(results)):
        for l in range(0, 23):
            test.write(k, l, results[k][l])
    writebook.save('result_1.xls')



main()
