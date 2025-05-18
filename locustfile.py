from locust import HttpUser, task

class UserBehavior(HttpUser):
    host = "http://127.0.0.1:8000/"

    # # Komparasi skema
    # @task
    # def attack_param(self):
    #     self.client.get('api/attack?limit=10&iyear=2000')

    # @task()
    # def incident_param(self):
    #     self.client.get('api/incident?iyear=2000&country=217')

    # @task()
    # def casualties_param(self):
    #     self.client.get('api/casualties?country_txt=Afghanistan&page=2&sort_by=iyear&order=desc')

    # # Test 1
    # @task
    # def index(self):
    #     self.client.get('api')

    # @task()
    # def incident(self):
    #     self.client.get('api/incident')

    # @task()
    # def casualties(self):
    #     self.client.get('api/casualties')

    # # Test 2
    # @task
    # def index_param(self):
    #     self.client.get('api?country_txt=Afghanistan&page=2&sort_by=iyear&order=desc')

    # @task()
    # def incident_param(self):
    #     self.client.get('api/incident?crit1=1&page=10&sort_by=iyear&order=desc')

    # @task()
    # def casualties_param(self):
    #     self.client.get('api/casualties?ransom=1&page=2&sort_by=iyear&order=desc')