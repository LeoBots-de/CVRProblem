# CVRProblem
This project was created in the Relaxdays Code Challenge Vol. 1. See https://sites.google.com/relaxdays.de/hackathon-relaxdays/startseite for more information.
Our participant IDs in the challenge were: CC-VOL1-14, CC-VOL1-16, CC-VOL1-85





## Docker
Please use the following commands to execute the project 
and enter the relative path to the root directory as the path.
```commandline
docker build -t cvrp .   

docker run -d -p 5000:5000 cvrp python /CVRProblem/app.py "testcase.json"
```


## Alternative: API
Alternatively, you can also run the programme via an API. 
Please do not pass a JSON file as an argument. 
You will receive the answer as JSON via http://127.0.0.1:5000/pathfinding via POST request.


## JSON Input
```json
{
"graph": {
  "nodes": 5,
  "edges":[[1,2,4],[1,3,4],[3,4,5],[1,5,1]]
},
"pickpool":[[3,5],[2,4],[4,3],[3,9]],
"cap": 10
}
```

## Output
```json
[[2,0],[3],[1]]
```
