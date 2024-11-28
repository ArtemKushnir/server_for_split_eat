from bs4 import BeautifulSoup
from rest_framework.response import Response
from models import *
# Create your views here.
from requests import Response, get


class TaskView:
    def __init__(self, task: BaseTask):
        self.task: BaseTask = task
        self.url: str = task.url

    def create_task(self):
        task = BaseTask(url=self.url)
        task.save()
        return Response({'message': f'Task to parse {self.url} was made.'})


class ParseView:
    def __init__(self, task: TaskView):
        self.task: BaseTask = task.task
        self.url: TaskView = task.task.url
        self.page: Response = get(task.url)
        self.soup: BeautifulSoup = BeautifulSoup(self.page.text, "html.parser")
        self.all_prices: list[str] = self.soup.findAll("div", class_="bottom__price")
        self.all_food: list[str] = self.soup.findAll("a", class_="inner__title")
        self.all_images: list[str] = self.soup.findAll("img")
        self.restaurant: str = ""
        self.filtered_prices: list[str] = []
        self.filtered_names: list[str] = []
        self.filtered_food: list[list[str]] = []

    def _filter_prices(self):
        filtered_prices = []
        for data in self.all_prices:
            data_str = str(data)
            filtered_prices.append(data_str[data_str.rfind("\t") + 1:data_str.rfind("<i")])
        self.filtered_prices = filtered_prices

    def _filter_names(self):
        filtered_names = []
        for data in self.all_food:
            data_str = str(data)
            filtered_names.append(data_str[data_str[:-1].rfind(">") + 1:data_str.rfind("<")])
        self.filtered_names = filtered_names

    def _get_restaurant_name(self):
        self.restaurant = BeautifulSoup(str(self.all_images[1]), "html.parser").find('img').get('alt')

    def _filter_img(self):
        filtered_food = []
        i = 0
        for data in self.all_images:
            soup_data = BeautifulSoup(str(data), "html.parser")
            img_tag = soup_data.find('img')
            if img_tag.get("loading"):
                name = self.filtered_names[i]
                src_url = img_tag.get('src')
                if str(src_url)[:5] != "https":
                    filtered_food.append([name, "https://avatars.mds.yandex.net/i?id"
                                                "=62fe6a095e0d46edbe96ecc85aa5aa9689e473b3"
                                                "-10812288-images-thumbs&n=13 "])
                else:
                    filtered_food.append([name, src_url])
                i += 1
        self.filtered_food = filtered_food

    def parse(self):
        self._filter_prices()
        self._filter_img()
        self._filter_names()
        parsed_menu = []
        for i in range(len(self.filtered_food)):
            parsed_menu.append([self.filtered_food[i][0], self.filtered_prices[i], self.filtered_food[i][1]])
        parse_result = RestaurantParse(task_id=self.task, restaurant_name=self.restaurant, menu=parsed_menu)
        parse_result.save()
        return Response({'message': f'{self.restaurant} page was parsed.'})
