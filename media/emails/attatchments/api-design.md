+ **Comments Module**
  1. comments/\<int:problem_id>/ => 根据任务ID查找评论
  2. comments/post/ => 发布评论
  3. comments/\<int:comment_id>/replies/ => 根据评论ID获取评论的回复
  4. comments/replies/post/ => 发布回复
  5. comments/comment/\<int:comment_id>/ => 根据评论ID获取评论
  6. comments/reply/\<int:reply_id>/ => 根据回复ID获取回复
  7. comments/like/ => 点赞功能
+ **Distributions Module**
  1. all-distributions/ => 获取所有推给FLyMeCrods平台审核的发放佣金请求
  2. distributions/post/ => 发布平台发放佣金请求
  3. distributions/\<int:distribution_id>/update/ =>平台发放佣金
  4. distributions/\<int:distribution_id>/ => 根据请求ID获取佣金发放请求
+ **Presessions Module**
  1. all-presessions/ => 获取所有想做任务的请求
  2. presessions/\<int:presession_id>/ => 根据ID获取想做的任务请求
  3. presessions/post/ => 提交想做任务的请求
  4. presessions/\<int:presession_id>/update/ => FlyMeCrods审核想做任务的请求
+ **Problems Module**
  1. latest-problems/ => 获取最新发布的12条任务
  2. problems/search/ => 关键字搜索相应任务
  3. problems/post/ => 发布任务
  4. problems/\<int:problem_id>/update/ => 修改任务信息
  5. problems/\<slug:tag_slug>/\<slug:problem_slug>/ => 获取任务详细信息
  6. problems/\<int:status>/ => 根据任务状态获取任务
  7. problems/\<slug:tag_slug>/ => 根据任务标签获取任务
+ **Solution Module**
  1. solutions/\<int:picker_id>/ => 根据接包用户ID获取产品
  2. solutions/solution/\<int:solution_id>/ => 根据产品ID获取产品详情
  3. solutions/problem/\<int:problem_id>/ => 根据任务ID获取产品
  4. solutions/solution/\<int:solution_id>/update/ => 更新产品详情
+ **User Module**
  1. rank-users/ => 根据声誉排行用户
  2. users/register/ => 用户注册
  3. users/login/ => 用户登录
  4. users/\<int:user_id>/update-email/ => 更新用户邮箱
  5. users/\<int:user_id>/ => 获取用户个人信息
  6. users/\<int:user_id>/posted-problems/ => 获取用户发布的任务



32 个 后端API