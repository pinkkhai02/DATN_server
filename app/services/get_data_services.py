import requests
from bs4 import BeautifulSoup

def scrape_data_content():
    # URL của trang website
    url = 'https://thuvienphapluat.vn/van-ban/Quyen-dan-su/Luat-Hon-nhan-va-gia-dinh-2014-238640.aspx'
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')

        # Tìm các phần tử HTML chứa nội dung cần lấy

        content_element = soup.find('div', class_='content1')

        a_elements = content_element.find_all('a')
        for index, a_element in enumerate(a_elements):

            if 'onmouseover' in a_element.attrs:
                del a_element['onmouseover']

            if 'onmouseout' in a_element.attrs:
                del a_element['onmouseout']

            if 'onclick' in a_element.attrs:
                del a_element['onclick']

            data_id = 'Dieu_' + str(index + 1 )
            a_element['id'] = data_id

        content_law = content_element.prettify()


        scraped_data = {
            'content_law': content_law,
        }

        return scraped_data
    else:
        print('Failed to fetch data from the website')
        return None

