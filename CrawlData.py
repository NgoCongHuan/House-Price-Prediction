import requests
import pandas as pd
from bs4 import BeautifulSoup

def create_house(link):

    try:
        response = requests.get(link)
        soup = BeautifulSoup(response.content, 'html.parser')

        # Từ điển chứa các thuộc tính của căn nhà
        house = {}

        # Đường link của căn nhà
        house['Liên kết'] = link

        # Ngày đăng tin và mã của căn nhà
        date_code = soup.find('div', class_='date')
        for dc in date_code.text.split(' - '):
            dc = dc.split(':')
            house[str(dc[0]).strip()] = dc[1].strip()

        # Mô tả của căn nhà
        description = soup.find('div', class_='sc-6orc5o-18')
        house['Mô tả'] = description.text

        # Giá nhà
        price = soup.find('div', class_='price').text
        house['Giá tiền'] = price

        # Địa chỉ căn nhà
        address = soup.find('div', class_='address').text
        house['Địa chỉ'] = address

        # Các thông tin cơ bản của căn nhà
        informations = soup.find_all('li', class_='sc-6orc5o-25')
        for inf in informations:
            inf = inf.text.split(':')
            house[str(inf[0])] = inf[1]
    except:
        print('Error at link: ', link)

    return house

def crawl_data(start_page, end_page):

    try:
        # Dataframe rỗng chứa dữ liệu
        df_combined = pd.DataFrame()

        for page in range(start_page, end_page + 1):
            # Truy cập vào trang web
            response = requests.get('https://muaban.net/bat-dong-san/ban-nha-ho-chi-minh#page=' + str(page))
            soup = BeautifulSoup(response.content,'html.parser')

            # Lấy đường link của toàn bộ căn nhà có trong trang hiện tại
            titles = soup.find_all('a', class_='title')
            links = ['https://muaban.net/' + link.attrs['href'] for link in titles]

            # Vòng lặp duyệt qua từng căn nhà rồi đưa vào hàm để lấy các thuộc tính
            for number, link in enumerate(links):
                house = create_house(link)
                df_temp = pd.DataFrame([house])
                df_combined = pd.concat([df_combined, df_temp], ignore_index=True)

                print(f'House {number} on page {page} has been successfully scratched')
    except:
        print('Error at page: ', page)

    return df_combined

if __name__ == '__main__':
    df_combined = crawl_data(20000, 20000)
    print(df_combined.head())