# -*- codeing=utf-8-*-
# @Time: 2021/8/28 20:34
# @AUthor: BaBa
# @File: demo.py
# @software: PyCharm

import re
import requests
import bs4
import execjs

findSeq = re.compile(r'<td align="center" height="32px">(.*)</td>')
findCate = re.compile(r'<td align="center" style="font-size: 9pt"><a href="\?infotype=.*">(.*)</a></td>')
findApart = re.compile(r'<td align="center" style="font-size: 9pt"><a href=".*\sonclick.*>(.*)</a></td>')
findDate = re.compile(r'<td align="center" style="font-size: 9pt">(\d*-\d*-\d*)</td>')
findId = re.compile(r'<a class="fontcolor3" href="view.asp\?id=(\d*)')

def dataFilter(url):
    html = askURL(url)
    soup = bs4.BeautifulSoup(html, "html.parser")
    # print(soup)
    datalist = []

    for itemSeq in soup.find_all(attrs={"align": "center", "height": "32px"}):

        item = itemSeq.parent
        itemStr = str(item)

        seq = re.findall(findSeq, itemStr)[0]

        cate = re.findall(findCate, itemStr)[0]
        apart = re.findall(findApart, itemStr)[0]
        title = item.find(attrs={"class": "fontcolor3"}).string
        date = re.findall(findDate, itemStr)[0]
        tapCount = item.find(attrs={"title": "累计点击数"}).string
        id = re.findall(findId, itemStr)[0]


        datalist.append([seq, cate, apart, title, date, tapCount, id])

    return datalist
def askURL(url):

    headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36"}
    session1 = requests.Session()
    session1.get("https://www1.szu.edu.cn/", headers=headers,verify=False)

    # 获取加密的password 开始
    crypt = session1.get("https://authserver.szu.edu.cn/authserver/custom/js/encrypt.js", headers=headers,verify=False).text
    encrypt = execjs.compile(crypt)  # 获取js加密代码
    # print(encrypt)
    res = session1.get("https://authserver.szu.edu.cn/authserver/login", headers=headers,verify=False)  # 请求登录界面

    bs = bs4.BeautifulSoup(res.content, "html.parser")
    bs = bs.find_all('input', {'type': "hidden"})  # 寻找登录界面中需要的数据
    dist = {}
    for i in bs:
        try:
            dist[re.search('(?<=name=").*?(?=")', str(i)).group()] = re.search('(?<=value=").*?(?=")', str(i)).group()
        except:
            dist[re.search('(?<=id=").*?(?=")', str(i)).group()] = re.search('(?<=value=").*?(?=")', str(i)).group()

    username = '334834'
    password = 'xiao1999'
    enPassword = encrypt.call("encryptAES", password, dist["pwdDefaultEncryptSalt"])  # 利用js代码加密
    # print(enPassword)
    # 获取加密过的password 结束

    # 登录时需要POST的数据
    data = {
        "username": username,
        "password": enPassword,
        "lt": dist["lt"],
        "dllt": dist["dllt"],
        "execution": dist["execution"],
        "_eventId": dist["_eventId"],
        "rmShown": dist["rmShown"]
    }

    login_url = "https://authserver.szu.edu.cn/authserver/login?service=http%3A%2F%2Fwww1%2Eszu%2Eedu%2Ecn%2Fmanage%2Fcaslogin%2Easp%3Frurl%3D%2F"
    session1.post(login_url, headers=headers, data=data,verify=False)

    askRes2 = session1.get("https://www1.szu.edu.cn/board/infolist.asp", headers=headers, verify=False)
    url = "https://www1.szu.edu.cn/board/infolist.asp?"
    global formData
    askRes = session1.post(url, headers=headers, data=formData, verify=False)
    askRes.encoding = 'gbk'
    # print(askRes.text)
    return askRes.text

formData = {}
def main2(index_sD,index_fr,keyW):
    global formData
    a = ["1#今天", "7#一周内", "30#30天内", "2021", "2020", "2019", "2018", "2017", "2016", "2015", "2014", "2013", "2012"]
    b = ['', '党政办公室', '档案馆', '督导室', '组织部', '统战部', '宣传部', '纪检（监察）室', '校工会', '妇女委员会', '校团委', '教务部', '招生办公室',
         '创新创业教育中心', '研究生院', '党委研工部', '发展规划部', '社会科学部', '学报社科版', '科学技术部', '学报理工版', '学生部', '党委学工部', '国际交流与合作部',
         '人力资源部', '党委教师工作部', '计划财务部', '招投标管理中心', '实验室与国有资产管理部', '审计室', '后勤保障部', '后勤保障部党委', '安全保卫部', '离退休办公室',
         '校友联络部', '教育发展基金会', '机关党委', '丽湖校区管理办公室', '师范学院（教育学部）', '艺术学部', '医学部', '马克思主义学院', '经济学院', '法学院', '人文学院',
         '外国语学院', '传播学院', '数学与统计学院', '物理与光电工程学院', '化学与环境工程学院', '生命与海洋科学学院', '机电与控制工程学院', '材料学院', '电子与信息工程学院',
         '计算机与软件学院', '建筑与城市规划学院', '土木与交通工程学院', '管理学院', '高等研究院', '金融科技学院（南特商学院）', '国际交流学院', '继续教育学院', '体育部',
         '体育部党总支', '图书馆', '图书馆党总支', '信息中心', '信息中心党总支', '资产经营公司', '技术转化中心', '深大总医院', '深大附属华南医院', '校医院', '深大师院附中',
         '中国经济特区研究中心', '港澳基本法研究中心', '文化产业研究院', '美学与文艺批评研究院', '饶宗颐文化研究院', '城市治理研究院', '中国海外利益研究院', '微纳光电子学研究院',
         '脑疾病与认知科学研究中心', '心理健康教育与咨询中心', '创新技术研究院', '原基建部']
    fr = b[index_fr]
    sDate = a[index_sD]

    searchDate = sDate
    searchDate = searchDate.encode("gb2312")
    ffrom = fr
    ffrom = ffrom.encode("gb2312")
    keyW=keyW.decode("utf")
    keyword = keyW.encode('gbk')
    searchb1 = "搜索"
    searchb1 = searchb1.encode("gb2312")
    formData = {
        "dayy": searchDate,
        "ffrom_username": ffrom,
        "keyword": keyword,
        "searchb1": searchb1
    }
    import warnings
    warnings.filterwarnings("ignore")

    baseurl = "https://www1.szu.edu.cn/board/infolist.asp?"
    return dataFilter(baseurl)
if __name__=="__main__":
    sttr = main2(1,0,"本科")
    # saar = sttr[0]
    # saar = str(saar)
    print(sttr)
