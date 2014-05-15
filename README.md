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

APIs
======

* /  ---> Hello World
* /sys ---> System Info
* /site ---> Site Control
* /block ---> Block Control
* /m/{token} ---> Comment Interface
* /mp/{token} ---> Get Comment by IP (Only for Admin)
* /mf/{token} ---> Get Comment by Fid (Like tieba)
* /dp/{token} ---> Delete Comment by IP (Only for Admin)
* /dt/{token} ---> Delete Comment by Tid (Only for Admin)
* /df/{token} ---> Delete Comment by Fid (Only for Admin)
* /up/{token}/{cid} ---> Up vote a comment (Not Implement yet)

