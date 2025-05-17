from locust import HttpUser, task

class UserBehavior(HttpUser):
    host = "http://127.0.0.1:8000/"
    
    # @task
    # def index(self):
    #     self.client.get('/api')

    @task()
    def case(self):
        self.client.get('api/attack')

    # @task()
    # def casualties(self):
    #     self.client.get('api/casualties')

    # @task()
    # def incident(self):
    #     self.client.get('api/incident')

    # @task()
    # def perpetrator(self):
    #     self.client.get('api/perpetrator')

    # @task()
    # def target(self):
    #     self.client.get('api/target')

    # @task()
    # def weapon(self):
    #     self.client.get('api/weapon')

# REDIS

    # @task()
    # def redis_api(self):
    #     self.client.get('/redis/api')
    
    # @task()
    # def redis_attack(self):
    #     self.client.get('redis/api/attack')

    # @task()
    # def redis_casualties(self):
    #     self.client.get('redis/api/casualties')

    # @task()
    # def redis_incident(self):
    #     self.client.get('redis/api/incident')

    # @task()
    # def redis_perpetrator(self):
    #     self.client.get('redis/api/perpetrator')
    
    # @task()
    # def redis_target(self):
    #     self.client.get('redis/api/target')
    
    # @task()
    # def redis_weapon(self):
    #     self.client.get('redis/api/weapon')

# Test

    # @task()
    # def redis_weapon_test(self):
    #     self.client.get('redis/api/weapon', params={"page" : 1, "limit" : 100})