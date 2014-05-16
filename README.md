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
* /u/{token}        ---> [Up a comment](#up_a_comment)

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
    * 404
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

Get Comment by IP
=================

**import warning**

**this api without cache, that means it will toooooo slow when getting**

* Method
    * GET
* Params
    * ip
* Status
    * 200
    * 400
    * 500
* Response
    * list contain lots dicts, each dicts describe a record.

**Example**

```
GET /mp/c16a3a755c1f41c78124e4bc51ca81e0 HTTP/1.1
Accept: application/json
Accept-Encoding: gzip, deflate, compress
Content-Length: 21
Content-Type: application/json; charset=utf-8
Host: localhost:8000
User-Agent: HTTPie/0.8.0

{
    "ip": "192.168.1.3"
}

HTTP/1.1 200 OK
Connection: close
Date: Thu, 15 May 2014 09:14:01 GMT
Server: gunicorn/18.0
Transfer-Encoding: chunked
content-type: application/json; charset=utf-8

[
    {
        "content": "Hello World2",
        "count": 0,
        "ctime": "2014-05-14 15:04:30",
        "id": 11,
        "ip": "192.168.1.3",
        "tid": 7
    },
    {
        "content": "Hello World2",
        "count": 0,
        "ctime": "2014-05-14 15:04:53",
        "id": 12,
        "ip": "192.168.1.3",
        "tid": 7
    }
]
```

Get Comment by Fid
==================

* Method
    * GET
* Params
    * fid >= 1
    * page >= 1
    * num >= 1
* Status
    * 200
    * 404
    * 400
    * 500
* Response
    A list contain multiple dicts. Each dicts describe a record.

**Example**

```
GET /mf/c16a3a755c1f41c78124e4bc51ca81e0 HTTP/1.1
Accept: application/json
Accept-Encoding: gzip, deflate, compress
Content-Length: 31
Content-Type: application/json; charset=utf-8
Host: localhost:8000
User-Agent: HTTPie/0.8.0

{
    "fid": 5,
    "num": 2,
    "page": 1
}

HTTP/1.1 200 OK
Connection: close
Date: Thu, 15 May 2014 09:20:08 GMT
Server: gunicorn/18.0
Transfer-Encoding: chunked
content-type: application/json; charset=utf-8

[
    {
        "content": "Hello World2",
        "count": 0,
        "ctime": "2014-05-15 14:26:42",
        "id": 14,
        "ip": "192.168.1.",
        "tid": 7
    },
    {
        "content": "Hello World2",
        "count": 0,
        "ctime": "2014-05-15 12:49:06",
        "id": 13,
        "ip": "192.168.1.7",
        "tid": 7
    }
]
```

Delete Comment by IP
====================

**import warning**

**this api without cache, that means it will toooooo slow when getting**

* Method
    * DELETE
* Params
    * ip
* Status
    * 200
    * 400
    * 500
* Response


**Example**

```
(comment) ❯ http -j DELETE :8000/dp/c16a3a755c1f41c78124e4bc51ca81e0 ip=127.0.0.2 -v
DELETE /dp/c16a3a755c1f41c78124e4bc51ca81e0 HTTP/1.1
Accept: application/json
Accept-Encoding: gzip, deflate, compress
Content-Length: 19
Content-Type: application/json; charset=utf-8
Host: localhost:8000
User-Agent: HTTPie/0.8.0

{
    "ip": "127.0.0.2"
}

HTTP/1.1 200 OK
Connection: close
Date: Thu, 15 May 2014 09:29:10 GMT
Server: gunicorn/18.0
content-length: 0
```

Delete Comment by Tid
=====================

* Method
    * DELETE
* Params
    * tid
* Status
    * 200
    * 400
    * 500
* Response

**Example**

```
DELETE /dt/c16a3a755c1f41c78124e4bc51ca81e0 HTTP/1.1
Accept: application/json
Accept-Encoding: gzip, deflate, compress
Content-Length: 10
Content-Type: application/json; charset=utf-8
Host: localhost:8000
User-Agent: HTTPie/0.8.0

{
    "tid": 1
}

HTTP/1.1 200 OK
Connection: close
Date: Thu, 15 May 2014 09:33:05 GMT
Server: gunicorn/18.0
content-length: 0
```

Delete Comment by Fid
=====================

* Method
    * DELETE
* Params
    * tid
* Status
    * 200
    * 400
    * 500
* Response

**Example**

```
DELETE /df/c16a3a755c1f41c78124e4bc51ca81e0 HTTP/1.1
Accept: application/json
Accept-Encoding: gzip, deflate, compress
Content-Length: 11
Content-Type: application/json; charset=utf-8
Host: localhost:8000
User-Agent: HTTPie/0.8.0

{
    "fid": 16
}

HTTP/1.1 200 OK
Connection: close
Date: Thu, 15 May 2014 09:36:50 GMT
Server: gunicorn/18.0
content-length: 0
```

Up A Comment
============

#### Method

* PUT
* GET

#### Up a comment

* Method
    * PUT
* Params
    * cids
* Status
    * 200
    * 400
* Response

**Example**

```
PUT /u/c16a3a755c1f41c78124e4bc51ca81e0 HTTP/1.1
Accept: application/json
Accept-Encoding: gzip, deflate, compress
Content-Length: 22
Content-Type: application/json; charset=utf-8
Host: localhost:8000
User-Agent: HTTPie/0.8.0

{
    "cids": [
        "15",
        "16"
    ]
}

HTTP/1.1 200 OK
Connection: close
Date: Fri, 16 May 2014 08:20:31 GMT
Server: gunicorn/18.0
content-length: 0
```

#### Get comments counts

* Method
    * GET
* Params
    * cids
* Status
    * 200
    * 400
* Response
    A dict include count for each comment id.

**Example**
```
GET /u/c16a3a755c1f41c78124e4bc51ca81e0 HTTP/1.1
Accept: application/json
Accept-Encoding: gzip, deflate, compress
Content-Length: 22
Content-Type: application/json; charset=utf-8
Host: localhost:8000
User-Agent: HTTPie/0.8.0

{
    "cids": [
        "15",
        "16"
    ]
}

HTTP/1.1 200 OK
Connection: close
Date: Fri, 16 May 2014 08:22:58 GMT
Server: gunicorn/18.0
Transfer-Encoding: chunked
content-type: application/json; charset=utf-8

{
    "15": "1",
    "16": "1"
}
```

