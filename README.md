# Yellow-Cab

The YellowCab API provides relevant and authentic statistics about New York Yellow Trips. To access these, it is necessary to carry out an authentication and authorization process.

## Structure

The Yellow Cab project is based on a microservices architecture, which is the main factor of our file system. This way, the main directory is divided into workflows - series of automated steps, and app - implementation, analysis, testing and deployment units.
In turn, the app contains four microservices and protobuf folder - essential for communication via gRPC, a prometheus folder, static-analyzer folder, tests folder, and kubernetes config folder.

```
yellow_cab_project/
    .github/
	workflows/
		analyze-test-build.yml
		deploy-cluster.yml
		send-deploy-slack.yml
		send-events-slack.yml
    app/
        authentication/
	    	templates/
                home.html
		__init__.py 
        	authentication.py
            	config.py
            	Dockerfile
		main.py
            	openapi_authentication.yaml
            	requirements.txt
        business-intelligence/
	    	__init__.py
            	bi.py
            	config.py
            	Dockerfile
		main.py
            	openapi_bi.yaml
            	requirements.txt
		utils.py
            	zone_pb2_grpc.py
            	zone_pb2.py
        k8s-config/
            	configmap.yaml
            	deployment.yaml
            	horizontalpodautoscaler.yaml
            	ingress.yaml
		prometheus.yaml
            	services.yaml
	locust/
		locust_authentication.py
		locust_business_intelligence.py
		locust_statistics.py
	prometheus/
		prometheus-cm.yaml
        protobuf/
	   	__init__.py
        	zone_pb2_grpc.py
           	zone_pb2.py
            	zone.proto
	static-analyzer/
		.pylintrc
		requirements.txt
        statistics/
		__init__.py
            	config.py
            	Dockerfile
		main.py
            	openapi_statistics.yaml
            	requirements.txt
            	statistics.py
		utils.py
            	zone_pb2_grpc.py
            	zone_pb2.py
	tests/
		__init__.py
		conftest.py
		init_tests.py
		requirements.txt
		test_business_intelligence.py
		test_statistics.py
		test_zones.py
		zone_pb2_grpc.py
            	zone_pb2.py
        zones/
		__init__.py
            	config.py
            	Dockerfile
		main.py
            	requirements.txt
            	zone_pb2_grpc.py
            	zone_pb2.py
		zones.py
    	__init__.py
    .gitattributes
    .gitignore
    authorization.txt
    cert.crt
    csr.csr	 
    delete.sh
    deployment.sh
    key.key
    openapi_yellow_cab.yaml
    README.md
    requests.rest
    rolling-update.txt
```

## Usage

Initially you need to select your Google Cloud project.

```bash
gcloud config set project [PROJECT_ID]
```

Create a GKE Standard Cluster by using gcloud or using the Google Cloud UI (Kubernetes Engine -> Clusters).

To interact with the Cluster via kubectl, you need to run the following command:

```
gcloud container clusters get-credentials [CLUSTER-NAME] --zone=[ZONE]
```

After the first steps, you are ready to set and configure Kubernetes:

```
sh deployment.sh
```

Now you need to get the external IP address of the ingress-ngix-controller, in order to access the services.

```
kubectl get svc -n ingress-nginx
```

To assess our cloud-native application, utilize the provided endpoints and the address that you got.

***Authentication***

- https://{{address}}/api/authentication
- https://{{address}}/api/authentication/login
- https://{{address}}/api/authentication/logout

***Business Intelligence***

* https://{{address}}/api/bi/tips?PULocationName={{PULocationName}}&DOLocationName={{DOLocationName}}&token={{token}}
* https://{{address}}/api/bi/amount?PULocationName={{PULocationName}}&DOLocationName={{DOLocationName}}&token={{token}}

***Statistics***

* https://{{address}}/api/stats/time?PULocationName={{PULocationName}}&DOLocationName={{DOLocationName}}&PULocationName2={{PULocationName2}}&DOLocationName2={{DOLocationName2}}&token={{token}}
* https://{{address}}/api/stats/congestion?PULocationName={{PULocationName}}&DOLocationName={{DOLocationName}}&PULocationName2={{PULocationName2}}&DOLocationName2={{DOLocationName2}}&token={{token}}
* https://{{address}}/api/stats/cabs?LocationName={{LocationName}}&LocationName2={{LocationName2}}&token={{token}}

***Prometheus***

To open the monitoring system, run the command:

```
kubectl port-forward service/prometheus-svc 8080:9090
```

Then select Web View option and select the port 8080.

For any reason, if needed to delete all components deployed, run the command:

```
sh delete.sh
```

## Contributions

- Tiago Pereira 54464
- Tiago Badalo 55311
- Alexandre Sobreira 59451
