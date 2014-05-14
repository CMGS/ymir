TODO
======
[![build status](http://ci.hunantv.com/projects/14/status.png?ref=master)](http://ci.hunantv.com/projects/14?ref=master)

1. 查询缓存
  * ~site 存于进程内存中~
  * ~block ip 进 rds backend~
  * 评论列表需要刷新
2. ~~遇到没有数据query层直接raise上来~~
3. 过热保护
  * IP 计数器

4. ~~删除单条消息接口~~
5. ~~删除基于 tid 消息接口~~
6. ~~删除基于 fid 消息接口~~
7. ~~删除基于 ip 消息接口~~

8. ~~获取 fid 消息接口~~
9. ~~获取 ip 消息接口~~

10. ~~测试 CommentByFid CommentByIP~~
11. 获取评论缓存设计
12. ~~获取评论跟帖设计~~

13. 赞
    * redis 计数器
14. 举报
    * redis 队列

15. 先发后审
16. refactor
    * ~cross transaction~
    * ~测试重命名~
    * ~500/404测试~
17. 日志收集
