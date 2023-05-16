from time import sleep

import requests
from bs4 import BeautifulSoup as bs
from selenium import webdriver

driver_path = "./geckodriver"
browser = webdriver.Firefox(executable_path=driver_path)
browser.get('https://web.whatsapp.com')


# driver_path = "./chromedriver"
# browser = webdriver.Chrome(executable_path=driver_path)
# browser.get('https://web.whatsapp.com')


# def getNews():
#     text_box = browser.find_element_by_class_name("_2S1VP")
#     response = "Let me fetch and send top 5 latest news:\n"
#     text_box.send_keys(response)
#     soup = BeautifulSoup(requests.get(url).content, "html5lib")
#     articles = soup.find_all('article',
#                              class_="MQsxIb xTewfe R7GTQ keNKEd j7vNaf Cc0Z5d YKEnGe EyNMab t6ttFe Fm1jeb EjqUne")
#     news = [i.find_all('a', class_="ipQwMb Q7tWef")[0].text for i in articles[:5]]
#     links = [root + i.find('a')['href'][1:] for i in articles[:5]]
#     links = [requests.get("http://thelink.la/api-shorten.php?url=" + link).content.decode() for link in links]
#     for i in range(5):
#         text_box.send_keys(news[i] + "==>" + links[i] + "\n")

def data_update():
    print('Datalar çekiliyor')
    r = requests.get('https://kur.doviz.com')
    soup = bs(r.content, 'html.parser')
    value = soup.find_all('span', attrs={'class': 'value'})
    name = soup.find_all('span', attrs={'class': 'name'})

    g = requests.get('http://www.guvenkuyumcusu.com/monitor.asp')
    soup = bs(g.content, 'html.parser')
    gname = soup.find_all(attrs={'face': 'Tahoma'})
    gvalue = soup.find_all(attrs={'face': 'Georgia'})
    return value, gvalue, gname


def response_data(value, gvalue, gname, msg):

    # button = browser.find_element_by_class_name('_35EW6')

    if 'dolar' in msg or 'd' in msg:
        response = (
                '*Dolar* ' + value[1].text+ '\n'
        )
    elif ('euro' in msg) or ('avro' in msg) or 'e' in msg:
        response = (
                '*Euro* ' + value[2].text + '\n'
        )
    elif ('altin' in msg) or ('alt' in msg) or 'a' in msg:
        response = (
                '*Gram Altın* ' + value[0].text + '\n'
        )
    elif 'bist100' in msg:
        response = (
                '*BIST100* ' + value[3].text + '\n'
        )
    elif 'faiz' in msg:
        response = (
                '*Faiz* ' + value[4].text + '\n'
        )
    elif 'bitcoin' in msg:
        response = (
                '*BITCOIN* ' + value[5].text + '\n'
        )
    elif 'ethereum' in msg:
        response = (
                '*Ethereum* ' + value[6].text + '\n'
        )
    elif 'ripple' in msg:
        response = (
                '*Ripple* ' + value[7].text + '\n'
        )
    elif 'litecoin' in msg :
        response = (
                '*LiteCoin* ' + value[8].text + '\n'
        )


    elif 'piyasa' in msg or 'p' in msg:
        response = (
                '*Dolar* ' + value[1].text + '\n'
                + '*Euro* ' + value[2].text + '\n'
                + '*Gram Altın* ' + value[0].text + '\n'
        )
    elif 'kuyumcu' in msg or 'k' in msg:
        response = (
                '*Çeyrek Eski* ' + gvalue[0].text + '-' + gvalue[1].text + '\n'
                + '*Yarım Eski* ' + gvalue[4].text + '-' + gvalue[5].text + '\n'
                + '*Ata Eski* ' + gvalue[8].text + '-' + gvalue[9].text + '\n'
                + gname[16].text + '\n'
                + gname[17].text + gname[18].text + '\n'
        )

    else:
        print("y")
        response = 'Simdilik sadece asagıdaki bilgileri verebiliyorum. Ogrenmek istediginiz bilginin adını yazıp göndermeniz yeterli.\n' \
                   + '*Altin, Dolar, Euro, Kuyumcu, Piyasa, Bist100, Faiz, Bitcoin, Ethereum, Ripple, Litecoin* \n '

    return response


i = 58
buffer_msg = ''
buffer_cnt = 0
response=''

while True:

    i += 1
    print(i)

    if i == 60:
        i = 0
        try:
            value, gvalue, gname = data_update()
        except Exception as e:
            print(e)
        print('tamam')


    unread = browser.find_elements_by_class_name("OUeyt")
    if len(unread) > 0:

        ele = unread[-1]
        action = webdriver.common.action_chains.ActionChains(browser)
        action.move_to_element_with_offset(ele, 0, -20)
        try:
            action.click()
            action.perform()
            action.click()
            action.perform()
        except Exception as e:
            print(e)
            pass
        try:
            name = browser.find_element_by_class_name("_3XrHh").text  # Contact name
            message = browser.find_elements_by_class_name("vW7d1")[-1]  # the message content
            msg = message.text.lower()
            come_msg=msg.split()
            print(name)
            print(msg)

            if (name== buffer_msg) and (buffer_cnt == i):
                print('hata:aynı mesaj')
                buffer_cnt = i + 1
            else:
                buffer_msg = name
                buffer_cnt = i + 1
                response = response_data(value, gvalue, gname, msg)
                print('response :'+response)
                text_box = browser.find_element_by_class_name("_2S1VP")
                text_box.send_keys(response)
        except Exception as e:
            print(e)
            pass
    sleep(1)  # A 2 second pause so that the program doesn't run too fast
