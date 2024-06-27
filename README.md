* Resultados de metodos post en API para subida de archivos a base de datos en SQLite

Para Tabla Jobs:

![image](https://github.com/edsonOsva/globant_data_engineer/assets/129419209/6b265a42-63a8-45d9-bd99-8a0e6634882e)

Para tabla Departmens:
![image](https://github.com/edsonOsva/globant_data_engineer/assets/129419209/2c84ab6b-e30a-4781-9323-e95eef8c06c4)

Para tabla Hired:
![image](https://github.com/edsonOsva/globant_data_engineer/assets/129419209/be603681-9db0-41d7-9bda-7cfc75fbaa73)

Resultado en Base de datos:
![image](https://github.com/edsonOsva/globant_data_engineer/assets/129419209/da913f83-d53f-4166-a4c4-7bd08e6a9fa6)

Tabla departments:
![image](https://github.com/edsonOsva/globant_data_engineer/assets/129419209/57b7b751-a3a8-4db8-aaed-46793e53bb0e)

Tabla jobs:
![image](https://github.com/edsonOsva/globant_data_engineer/assets/129419209/c0eb5c7a-19d6-4010-b2d6-11eff37eea81)

Tabla hired:
![image](https://github.com/edsonOsva/globant_data_engineer/assets/129419209/d5dbcc0f-918b-4c46-b1a4-898b24bcd850)


* Endpoints de API
Primer query de stakeholders:

![image](https://github.com/edsonOsva/globant_data_engineer/assets/129419209/683c7c9f-b5ac-44e8-b9fe-2f4f0a330478)

SQL:
![image](https://github.com/edsonOsva/globant_data_engineer/assets/129419209/3c34292c-9b74-4155-8c02-446e592413c6)


Segundo query:
![image](https://github.com/edsonOsva/globant_data_engineer/assets/129419209/ade5b11a-8934-4f50-8b7d-ce6ce4ebfe0f)

SQL:
![image](https://github.com/edsonOsva/globant_data_engineer/assets/129419209/25c2fd60-b1a5-4757-bdfb-81b3ab634578)


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

**Nota: en esta última parte no obtuve el resultado que deseaba, el tiempo no me ayudo, parece ser un detalle con el firewall y la transmisión de información por los puertos
