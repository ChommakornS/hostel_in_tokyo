
# ITCS443_Parallel and Distributed Systems
## Contributors
    6488189 Chommakorn Sontesadisai
    6488190 Nattanicha Sinsawet

## Introduction
Step to run the project

## Run kibana.bat and elastic.bat

## search dev console in elasticsearch

```
PUT hosteldata (index name) 
```
### Open Anaconda Prompt (conda activate flasktest2)

```
conda activate flasktest2
```

## Upload JSON to elasticsearch

```python elasticsearch_loader.py --file hoteldataset.json --index hosteldata```

## Check on Console elastic
```
GET hosteldata/_search{
    "query" {
        "match_all"={}
    }
}
```

## Set environment
```
set FLASK_APP=app
set FLASK_ENV=development
```

## Run flask
```
flask run
```





