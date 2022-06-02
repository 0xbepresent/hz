Horuz!. Save and query your recon data on ElasticSearch.

Installing
----------
**Install and setting up ElasticSearch**

https://www.elastic.co/guide/en/elasticsearch/reference/current/install-elasticsearch.html


**Install and setting up Horuz**

```console
$ pip3 install horuz

$ hz config server:add http://yourelasticsearchendpoint:9200
```

Usage
-----

```console
$ hz --help

$ hz config server:status
ElasticSearch is connected to http://localhost:9200 successfully!
```

Collect data
---------------------
##### Custom JSON files

In this example, we have an httprobe.txt file, then it will be transformed to JSON file.

```
$ cat httprobe.txt | jq -Rnc '[inputs|split("\n")|{("host"):.[0]}]' > httprobe.json
```

Then, upload it to ES.

```
$ hz collect -p example.com -f httprobe.json
⠦ Collecting...
Session name: gallant_satoshi_8455236

Results: 1366

$ hz search -p example.com -q "session:gallant_satoshi_8455236" -oJ -f time,host -s 2

```

Query search
--------------

Search by range dates:

```console
$ hz search -p example.com -q "time:[2020-04-15 TO 2020-05-20]"
```

Search by wildcard in the field

```console
$ hz search -p example.com -q "result.html:*key*" -oJ -f html
```


Pipe the result to other commands

```console
$ hz search -p example.com -q "session:*" -oJ -f _id,session,time | jq ".[].session" | sort -
```

