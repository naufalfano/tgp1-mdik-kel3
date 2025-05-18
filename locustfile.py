from locust import HttpUser, task

class UserBehavior(HttpUser):
    host = "http://127.0.0.1:8000/"

# Test 1
    @task
    def index(self):
        self.client.get('api')

    @task()
    def incident(self):
        self.client.get('api/incident')

    @task()
    def casualties(self):
        self.client.get('api/casualties')

# Test 2
    @task
    def index_param(self):
        self.client.get('api?country_txt=Afganisthan&page=2&sort_by=iyear&order=desc')

    @task()
    def incident_param(self):
        self.client.get('api/incident?crit1=1&page=10&sort_by=iyear&order=desc')

    @task()
    def casualties_param(self):
        self.client.get('api/casualties?ransom=1&page=2&sort_by=iyear&order=desc')