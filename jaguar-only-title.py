from bs4 import BeautifulSoup
import requests
import csv

def get_last_page(page):
    '''get total number of pages to scrape'''
    pages = page.find('div', class_ = 'pager')
    try:
        last_page = pages.find('li', class_ = 'last-page').a['data-page']
        print(f'>> last pg - {last_page}')
    except Exception as e:
        # print(e)
        last_page = page.find_all('li', class_ = 'individual-page')[-1].a['data-page']
        print(f'>> last pg - {last_page}')
    except IndexError:
        print(999)
        last_page = 1
        print(f'>> last pg - {last_page}')
    return last_page

def scrape(site, path):
    FILTER = '#/pageSize=12&orderBy=0&pageNumber='
    temp_source = requests.get(f'{site}{path}').text
    temp_page = BeautifulSoup(temp_source, 'lxml')
    last_page = get_last_page(temp_page)

    # csv_file = open('data/jaguar/faucets/laguna.csv', 'w')
    # csv_file = open('data/jaguar/faucets/continental-prime.csv', 'w')
    # csv_file = open('data/jaguar/faucets/queens-prime.csv', 'w')
    # csv_file = open('data/jaguar/faucets/body-showers.csv', 'w')
    # csv_file = open('data/jaguar/faucets/whirlpools-bathtubs.csv', 'w')
    # csv_file = open('data/jaguar/faucets/built-in-bath-tubs.csv', 'w')
    # csv_file = open('data/jaguar/faucets/free_standing_bath_tubs.csv', 'w')
    # csv_file = open('data/jaguar/faucets/bath-tub-fillers.csv', 'w')
    # csv_file = open('data/jaguar/faucets/i-flush.csv', 'w')
    # csv_file = open('data/jaguar/faucets/jaquar-spas.csv', 'w')
    # csv_file = open('data/jaguar/faucets/free_standing_bath_tubs.csv', 'w', newline='', encoding="utf-8")
    csv_file = open('data/jaguar/faucets/bath-tub-fillers.csv', 'w')


    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(['url', 'name', 'code', 'description', 'mrp', 'colors', 'image links'])

    for pg in range(1, int(last_page) + 1):
        print(f'>> {pg}')

        source = requests.get(f'{site}{path}{FILTER}{pg}').text
        page = BeautifulSoup(source, 'lxml')

        try:
            item_box = page.find_all('li', class_='item-box')
        except Exception as e:
            # print(e)
            break

        for item in item_box:
            try:
                href = item.find('h2', class_ = 'product-title').a['href']
                # print(href)
            except Exception as e:
                # print(e)
                print('item page not available')
                break

            url = f'{site}{href}'
            # print(url)

            try:
                code = item.find('div', class_ = 'product-code sku').span.text
                # print(code)
            except Exception as e:
                # print(e)
                print('code unavailable')
                code = 'unavailable'

            try:
                mrp = item.find('span', class_ = 'price actual-price').text
                # print(mrp)
            except Exception as e:
                # print(e)
                print('mrp unavailable')
                mrp = 'unavailable'

            try:
                item_source = requests.get(url).text
                item_page = BeautifulSoup(item_source, 'lxml')
            except Exception as e:
                # print(e)
                print('product url broken')
                break

            try:
                name = item_page.find('div', class_ = 'detail-header').h1.text
                # print(name)
            except Exception as e:
                # print(e)
                print('how tf is the name not available??')
                name = 'unavailable'

            try:
                description = item_page.find('div', class_ = 'shortDdiv').find_next('span').find_next('span').text
                # print(description)
            except Exception as e:
                # print(e)
                print('description unavailable')
                print(f'check the website tho just to be sure. product name - {name}')
                description = 'unavailable'

            # ik this outer try-except is bad but i dont trust websites
            # try:
            colors = []
            img_links = []
            try:
                colors_div = item_page.find('div', class_ = 'colors')
                color_list = colors_div.find_all('li')
            except TypeError:
                print('no colours')
                color_list = []
                print('wow such website. much kawaii -_-')
                img = item_page.find('img', title = f'Show details for {name}')['src']
                img_links.append(img)
            except Exception as e:
                # print(e)
                color_list = []
                img = item_page.find('img', title = f'Picture of {name}')['src']
                img_links.append(img)

            for i in color_list:
                c = i.find('input', type = "radio")['title']
                try:
                    # there are some pages in which there is no space between {name} and {c} -_-
                    img = item_page.find('img', alt = f'Picture of {name} - {c}')['src']
                    # print(img)
                except Exception as e:
                    # print(e)
                    print('no colour image?? pls check site just to be sure')
                    img = item_page.find('img', alt = f'Picture of {name}')['src']
                    # print(img)
                colors.append(c)
                img_links.append(img)
            # except Exception as e:
            #     # print(e)
            #     print('color or image broken')
            
            name_ = item.find('h2', class_ = 'product-title').a.text
            print(name_)
            
            # csv_writer.writerow([url, name, code, description, mrp, colors, img_links])
            csv_writer.writerow([url, name_, code, description, mrp, colors, img_links])

    csv_file.close()

def main():
    # scrape('https://www.jaquar.com', '/en/laguna-faucets')
    # scrape('https://www.jaquar.com', '/en/continental-prime')
    # scrape('https://www.jaquar.com', '/en/queens-prime')
    # scrape('https://www.jaquar.com', '/en/body-showers')
    # scrape('https://www.jaquar.com', '/en/built-in-bath-tubs')
    # scrape('https://www.jaquar.com', '/en/free_standing_bath_tubs')
    # scrape('https://www.jaquar.com', '/en/bath-tub-fillers')
    # scrape('https://www.jaquar.com', '/en/i-flush')
    scrape('https://www.jaquar.com', '/en/bath-tub-fillers')

if __name__ == '__main__':
    main()
