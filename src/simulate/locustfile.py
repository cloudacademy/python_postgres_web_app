import random
from bs4 import BeautifulSoup
from locust import HttpUser, task, between

class WebsiteUser(HttpUser):
    wait_time = between(5, 10)

    @task
    def index_page(self):
        # Simulate user requests to the index page
        response = self.client.get("/")

        # Use BeautifulSoup to parse the content
        soup = BeautifulSoup(response.text, 'lxml')
        
        # Extract links to user profiles
        links = [a['href'] for a in soup.select("ul.menu.simple li a") if '/user/' in a['href']]

        # Randomly select a link
        if links:
            user_detail = random.choice(links)
            self.client.get(user_detail)

