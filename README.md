* Resultados de metodos post en API para subida de archivos a base de datos en SQLite

Para Tabla Jobs:

![image](https://github.com/edsonOsva/globant_data_engineer/assets/129419209/6b265a42-63a8-45d9-bd99-8a0e6634882e)

Para tabla Departmens:
![image](https://github.com/edsonOsva/globant_data_engineer/assets/129419209/2c84ab6b-e30a-4781-9323-e95eef8c06c4)

Para tabla Hired:
![image](https://github.com/edsonOsva/globant_data_engineer/assets/129419209/be603681-9db0-41d7-9bda-7cfc75fbaa73)

* Endpoints de API
Primer query de stakeholders:

![image](https://github.com/edsonOsva/globant_data_engineer/assets/129419209/683c7c9f-b5ac-44e8-b9fe-2f4f0a330478)

Segundo query:
![image](https://github.com/edsonOsva/globant_data_engineer/assets/129419209/ade5b11a-8934-4f50-8b7d-ce6ce4ebfe0f)


•	Construyendo imagen de Docker:
docker build -t gcr.io/globant-dataengineer/globant-api:gdea -f C:\Users\edson.perez\Globant\app\dockerfile .
 
![image](https://github.com/edsonOsva/globant_data_engineer/assets/129419209/bdec7456-6ec7-4600-922b-c58aaa23a008)

Se toma dockerfile desde el path del proyecto

•	Subiendo imagen al Container Registry
docker push gcr.io/[YOUR_PROJECT_ID]/[IMAGE_NAME]:[TAG]
 
![image](https://github.com/edsonOsva/globant_data_engineer/assets/129419209/b2bd38b9-85b1-4eeb-b447-b2d6b99adf36)


•	Implementa imagen en cluster de GKE
o	Asegurarse de que el cluster este configurado

![image](https://github.com/edsonOsva/globant_data_engineer/assets/129419209/23160023-f5f9-472f-a8ee-4c4e09d80982)

gcloud container clusters get-credentials [CLUSTER_NAME] --zone [CLUSTER_ZONE] --project [YOUR_PROJECT_ID]

o	Crea un archive de configuración de despliegue (deployment:yaml)

Ejemplo:
apiVersion: apps/v1
kind: Deployment
metadata:
  name: [DEPLOYMENT_NAME]
spec:
  replicas: 3
  selector:
    matchLabels:
      app: [APP_NAME]
  template:
    metadata:
      labels:
        app: [APP_NAME]
    spec:
      containers:
      - name: [CONTAINER_NAME]
        image: gcr.io/[YOUR_PROJECT_ID]/[IMAGE_NAME]:[TAG]
        ports:
        - containerPort: 80


o	Implementa la configuración de tu cluster de GKE

kubectl apply -f deployment.yaml

![image](https://github.com/edsonOsva/globant_data_engineer/assets/129419209/ab91dbc3-478f-4fdb-b660-4df3f9506d7f) 

Revisando los despliegues:

![image](https://github.com/edsonOsva/globant_data_engineer/assets/129419209/096323be-fe95-42e1-b653-d7ca830657a4)


Creando el servicio:

![image](https://github.com/edsonOsva/globant_data_engineer/assets/129419209/7f96497e-188a-4136-b8d0-d8faaec1002a)

![image](https://github.com/edsonOsva/globant_data_engineer/assets/129419209/79619fe1-8753-44d5-a55f-9ea37f38dacd)

Configurando reglas de firewall para que se despliegue aplicación en puerto 80 protocolo TCP

![image](https://github.com/edsonOsva/globant_data_engineer/assets/129419209/ab6cdc54-cc2c-41f6-b214-da8e8f7c84b2)

Resultado

![image](https://github.com/edsonOsva/globant_data_engineer/assets/129419209/b726bf1a-bf4a-4a26-aa24-5354a8e7855f)
