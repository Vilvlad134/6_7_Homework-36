import requests

# response = requests.post('http://127.0.0.1:5000/register/', json={'email': 'snt@mail.ru',
#                                                                  'password': '52412-JfMdKzx'})

# response = requests.post('http://127.0.0.1:5000/login/', json={'email': 'snt@mail.ru',
#                                                               'password': '52412-JfMdKzx'})

response = requests.get('http://127.0.0.1:5000/users/1/')

# response = requests.post('http://127.0.0.1:5000/send/', json={'header': 'computer',
#                                                               'description': 'good'},
#                          headers={'token': '1a3600b6-ec73-42c8-a17d-a772556a12f0'})

# response = requests.get('http://127.0.0.1:5000/advertisments/4/')

# response = requests.patch('http://127.0.0.1:5000/advertisments/4/', json={'header': 'computer_s'},
#                          headers={'token': '08e59a06-0d12-4346-989b-d524893e06bc'})

# response = requests.delete("http://127.0.0.1:5000/advertisments/4/",
#                            headers={'token': 'e64b2147-1919-4660-9b5e-5ff864c0ad55'})

print(response.status_code)
print(response.text)