Ymir aka Comment service
======
[![build status](http://ci.hunantv.com/projects/14/status.png?ref=master)](http://ci.hunantv.com/projects/14?ref=master)

Features
======

* Multiple method for site to get the comments
* Automatic and Dynamic create comments table for each site
* Full restfull
* Block list for robot
* 1 level replay
* Stream output
* All data packed as JSON

APIs
======

* /                 ---> [Hello World](#hello-world)
* /sys              ---> [System Info](#system-info)
* /site             ---> [Site Control](#site-control)
* /block            ---> [Block Control](#block-control)
* /m/{token}        ---> [Comment Interface](#comment-interface)
* /mp/{token}       ---> [Get Comment by IP (Only for Admin)](#get-comment-by-ip)
* /mf/{token}       ---> [Get Comment by Fid (Like tieba)](#get-comment-by-fid)
* /dp/{token}       ---> [Delete Comment by IP (Only for Admin)](#delete-comment-by-ip)
* /dt/{token}       ---> [Delete Comment by Tid (Only for Admin)](#delete-comment-by-tid)
* /df/{token}       ---> [Delete Comment by Fid (Only for Admin)](#delete-comment-by-fid)
* /up/{token}/{cid} ---> [Up vote a comment (Not Implement yet)](#)

Hello World
=========

```
GET / HTTP/1.1
Accept: */*
Accept-Encoding: gzip, deflate, compress
Host: localhost:8000
User-Agent: HTTPie/0.8.0

HTTP/1.1 200 OK
Connection: close
Date: Thu, 15 May 2014 07:34:23 GMT
Server: gunicorn/18.0
content-length: 11
content-type: application/json; charset=utf-8

Hello World
```

System Info
===========

```
GET /sys HTTP/1.1
Accept: */*
Accept-Encoding: gzip, deflate, compress
Host: localhost:8000
User-Agent: HTTPie/0.8.0

HTTP/1.1 200 OK
Connection: close
Date: Thu, 15 May 2014 07:38:20 GMT
Server: gunicorn/18.0
Transfer-Encoding: chunked
content-type: application/json; charset=utf-8

{
    "default_db": [
        "127.0.0.1",
        "comment",
        "",
        3306,
        "root"
    ],
    "deny": 180,
    "redis": [
        0,
        "127.0.0.1",
        "",
        100,
        6379,
        "comment:cache:"
    ],
    "store": [
        {
            "database": "comment",
            "host": "127.0.0.1",
            "password": "",
            "port": 3306,
            "user": "root"
        }
    ]
}
```

Site Control
===========

#### Method

* PUT

#### Create a Site

* Method
    * PUT
* Params
    * name
* Status
    * 201
    * 400
    * 500
* Response
    * token

**Example**

```
PUT /site HTTP/1.1
Accept: application/json
Accept-Encoding: gzip, deflate, compress
Content-Length: 17
Content-Type: application/json; charset=utf-8
Host: localhost:8000
User-Agent: HTTPie/0.8.0

{
    "name": "test3"
}

HTTP/1.1 201 Created
Connection: close
Date: Thu, 15 May 2014 07:49:34 GMT
Server: gunicorn/18.0
Transfer-Encoding: chunked
content-type: application/json; charset=utf-8

{
    "token": "1fc684e7a24043fab2ef1336fcde8905"
}
```

Block Control
============

#### Method

* PUT
* DELETE
* GET

#### Create a Blocked IP

* Method
    * PUT
* Params
    * ip
    * token
* Status
    * 201
    * 400
    * 500
* Response
    * id

**Example**

```
PUT /block HTTP/1.1
Accept: application/json
Accept-Encoding: gzip, deflate, compress
Content-Length: 67
Content-Type: application/json; charset=utf-8
Host: localhost:8000
User-Agent: HTTPie/0.8.0

{
    "ip": "192.168.1.10",
    "token": "c16a3a755c1f41c78124e4bc51ca81e0"
}

HTTP/1.1 201 Created
Connection: close
Date: Thu, 15 May 2014 08:01:23 GMT
Server: gunicorn/18.0
Transfer-Encoding: chunked
content-type: application/json; charset=utf-8

{
    "id": 17
}
```

#### Delete a Blocked IP

* Method
    * DELETE
* Params
    * id
* Status
    * 200
    * 400
    * 500
* Response

**Example**

```
DELETE /block HTTP/1.1
Accept: application/json
Accept-Encoding: gzip, deflate, compress
Content-Length: 57
Content-Type: application/json; charset=utf-8
Host: localhost:8000
User-Agent: HTTPie/0.8.0

{
    "id": "17",
    "token": "c16a3a755c1f41c78124e4bc51ca81e0"
}

HTTP/1.1 200 OK
Connection: close
Date: Thu, 15 May 2014 08:10:49 GMT
Server: gunicorn/18.0
content-length: 0
```

#### Get Blocked IPs

* Method
    * GET
* Params
    * token
    * page >= 1
    * num >= 1
* Status
    * 200
    * 400
    * 500
* Response
    A list contain less than num dicts. Each dicts describe a block ip info.

**Example**


```
GET /block HTTP/1.1
Accept: application/json
Accept-Encoding: gzip, deflate, compress
Content-Length: 66
Content-Type: application/json; charset=utf-8
Host: localhost:8000
User-Agent: HTTPie/0.8.0

{
    "num": 2,
    "page": 1,
    "token": "c16a3a755c1f41c78124e4bc51ca81e0"
}

HTTP/1.1 200 OK
Connection: close
Date: Thu, 15 May 2014 08:18:06 GMT
Server: gunicorn/18.0
Transfer-Encoding: chunked
content-type: application/json; charset=utf-8

[
    {
        "ctime": "2014-05-15 16:00:54",
        "id": 16,
        "ip": "192.168.1.9"
    },
    {
        "ctime": "2014-05-14 17:35:49",
        "id": 15,
        "ip": "192.168.1.7"
    }
]
```

Comment Interface
=================

#### Method

* PUT
* DELETE
* GET

#### Create a Comment

* Method
    * PUT
* Params
    * tid >= 0
    * fid >= 0
    * uid >= 1
    * ip
    * content
* Status
    * 200
    * 400
    * 403 if ip is blocked
    * 500
* Response
    * id

**Example**

```
PUT /m/c16a3a755c1f41c78124e4bc51ca81e0 HTTP/1.1
Accept: application/json
Accept-Encoding: gzip, deflate, compress
Content-Length: 77
Content-Type: application/json; charset=utf-8
Host: localhost:8000
User-Agent: HTTPie/0.8.0

{
    "content": "Hello World2",
    "fid": 0,
    "ip": "192.168.1.1",
    "tid": 7,
    "uid": 1
}

HTTP/1.1 201 Created
Connection: close
Date: Thu, 15 May 2014 08:27:09 GMT
Server: gunicorn/18.0
Transfer-Encoding: chunked
content-type: application/json; charset=utf-8

{
    "id": 17
}
```

**if IP was Blocked**

```
PUT /m/c16a3a755c1f41c78124e4bc51ca81e0 HTTP/1.1
Accept: application/json
Accept-Encoding: gzip, deflate, compress
Content-Length: 78
Content-Type: application/json; charset=utf-8
Host: localhost:8000
User-Agent: HTTPie/0.8.0

{
    "content": "Hello World2",
    "fid": 0,
    "ip": "192.168.1.2",
    "tid": 7,
    "uid": 1
}

HTTP/1.1 403 Forbidden
Connection: close
Date: Thu, 15 May 2014 08:28:11 GMT
Server: gunicorn/18.0
content-length: 78
content-type: application/json; charset=utf-8

{
    "description": "ip 192.168.1.2 deny",
    "title": "Request Forbidden"
}
```

#### Delete a Comment

* Method
    * DELETE
* Params
    * id
* Status
    * 200
    * 400
    * 404
    * 500
* Response

**Example**

```
DELETE /m/c16a3a755c1f41c78124e4bc51ca81e0 HTTP/1.1
Accept: application/json
Accept-Encoding: gzip, deflate, compress
Content-Length: 10
Content-Type: application/json; charset=utf-8
Host: localhost:8000
User-Agent: HTTPie/0.8.0

{
    "id": 31
}

HTTP/1.1 404 Not Found
Connection: close
Date: Thu, 15 May 2014 08:50:10 GMT
Server: gunicorn/18.0
content-length: 0
```

if comment exist.

```
DELETE /m/c16a3a755c1f41c78124e4bc51ca81e0 HTTP/1.1
Accept: application/json
Accept-Encoding: gzip, deflate, compress
Content-Length: 10
Content-Type: application/json; charset=utf-8
Host: localhost:8000
User-Agent: HTTPie/0.8.0

{
    "id": 17
}

HTTP/1.1 200 OK
Connection: close
Date: Thu, 15 May 2014 08:50:28 GMT
Server: gunicorn/18.0
content-length: 0
```

#### Get comments by topic id

* Method
    * GET
* Params
    * tid >= 1
    * page >= 1
    * num >= 1
    * expand 0 or 1
* Status
    * 200
    * 400
    * 500
* Response
    A list contain multiple lists. Each list contain more than one dict if expand is 1.

**Example**

```
GET /m/c16a3a755c1f41c78124e4bc51ca81e0 HTTP/1.1
Accept: application/json
Accept-Encoding: gzip, deflate, compress
Content-Length: 44
Content-Type: application/json; charset=utf-8
Host: localhost:8000
User-Agent: HTTPie/0.8.0

{
    "expand": 0,
    "num": 1,
    "page": 1,
    "tid": 7
}

HTTP/1.1 200 OK
Connection: close
Date: Thu, 15 May 2014 09:01:27 GMT
Server: gunicorn/18.0
Transfer-Encoding: chunked
content-type: application/json; charset=utf-8

[
    [
        {
            "content": "Hello World2",
            "count": 0,
            "ctime": "2014-05-15 16:26:06",
            "id": 16,
            "ip": "192.168.1.",
            "tid": 7
        }
    ]
]
```

with expand

```
GET /m/c16a3a755c1f41c78124e4bc51ca81e0 HTTP/1.1
Accept: application/json
Accept-Encoding: gzip, deflate, compress
Content-Length: 44
Content-Type: application/json; charset=utf-8
Host: localhost:8000
User-Agent: HTTPie/0.8.0

{
    "expand": 1,
    "num": 1,
    "page": 1,
    "tid": 7
}

HTTP/1.1 200 OK
Connection: close
Date: Thu, 15 May 2014 09:02:19 GMT
Server: gunicorn/18.0
Transfer-Encoding: chunked
content-type: application/json; charset=utf-8

[
    [
        {
            "content": "Hello World2",
            "count": 1,
            "ctime": "2014-05-15 16:26:06",
            "id": 16,
            "ip": "192.168.1.",
            "tid": 7
        },
        {
            "content": "Hello World2",
            "count": 0,
            "ctime": "2014-05-15 17:02:12",
            "id": 18,
            "ip": "192.168.1.11",
            "tid": 7
        }
    ]
]
```

