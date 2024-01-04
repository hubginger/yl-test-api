# yl_test_api

## 项目结构

```apl
yl_test_api                            |-> 项目名
├── cases                              |-> 用例总目录
│	└── test_case_xx1(包/模块)          |-> 自定义用例目录 / 自定义用例模块
│	└── test_case_xx2(包/模块)          |-> 自定义用例目录 / 自定义用例模块
│	└── test_case_xx3(包/模块)          |-> 自定义用例目录 / 自定义用例模块
│	└── conftest                       |-> 用例总 conftest, 编码日志
├── common                             |-> 公共封装目录
│	└── utils                          |-> 工具封装目录
│		└── do_conf                    |-> 配置文件操作
│		└── do_excel                   |-> Excel 读写
│		└── do_log                     |-> 日志操作
│		└── do_mongo                   |-> MongoDB 操作
│		└── do_mysql                   |-> MySql 操作, 自动释放连接
│		└── do_path                    |-> 路径操作
│		└── do_slow_api                |-> 慢接口记录操作
│		└── do_time                    |-> 时间和日期操作
│		└── do_try                     |-> emmm, with 简化 try, 没卵用其实
│	└── base_api                       |-> requests 封装, 发请求, 简化登录等
│	└── base_assert                    |-> assert 封装, 
│	└── base_data                      |-> Excel全量数据, 
│	└── base_device                    |-> emmm, 枚举, 没用, 当个注释吧
│	└── base_extract                   |-> 提值写值, 提响应, 写extract.yml
├── static                             |-> 静态资源目录
│	└── allure_report                  |-> allure 报告暂存目录
│	└── allure_result                  |-> allure 数据暂存目录
│	└── conf                           |-> 配置目录
│		└── db.yml                     |-> 数据库配置文件
│		└── excel.yml                  |-> excel 配置文件
│		└── log.yml                    |-> log 配置文件
│		└── login.yml                  |-> 登录配置文件
│		└── mongo.yml                  |-> MongoDB 数据库配置文件
│		└── request.yml                |-> 请求配置文件, host, verify_url
│		└── slow_api.yml               |-> 慢接口配置, 就一个, 多少毫秒
│	└── data                           |-> 数据目录, Excel 和 extract(存值)
│		└── Delivery_System_V1.5.xlsx  |-> Excel 文件, 这个 yft 的
│		└── extract.yml                |-> 存值文件, 运行时提取的值存在这里
│	└── log                            |-> 日志目录, 项目日志, 慢接口日志
├── .gitignore                         |-> git 忽略文件
├── pytest.ini                         |-> pytest 配置文件
├── readme.md                          |-> .
├── requirements.txt                   |-> 项目第三方库记录文件
└── run.py                             |-> 项目启动文件
```

## 部分说明

- cases
  ```apl
  cases 目录是用例总目录
      因为我们需要自定义用例, 所以该目录需要大家共同维护好
      常规操作是, 将自己的用例以层级关系管理好
      定义 conftest, 服务于自己的用例
  conftest 中包含:
  	前后置
  		各级别的前后置定义
  	登录
  		登录的 fixture 一般 scope 不为 function 级别, 一般定义为 class 或 module 或 package 级别
  	参数化
  		自定义参数化的 fixture, 将 fixture 传递给 test_case 实现 test_case 的参数化
  		原 libs 中的参数构造, 放在 fixture 中完成
  test_case
  	参数化
  		不再用 @pytest.mark.parametrize 进行参数化, 而是放在 conftest 中通过自定义 fixture 进行参数化
  	逻辑
  		test_case 中的逻辑应不少于调用接口, 断言结果, 可以增加提取和存值, 数据库断言等操作
  ```

- conftest
  ```apl
  这里仅说明总 conftest 文件
  总 conftest 中, 定义 session 级别的 fixture 或 hooks 
  当前有三个方法, 作用分别是:
  	收集用例时, 更改编码
  	运行用例前后, 打印一条分隔日志
  	运行用例时, 记录日志
  ```

- utils
  ```apl
  utils 中是工具封装
  
  do_conf, 
  	封装了配置文件的操作, 支持读取和写入, 
  	使用时, 注意不要随意调用写入方法写入配置文件, 
  	应当仅调用 set 方法写入 extract.yml 文件, 
  	其他 yml 配置文件中, 存在注释, 当前的实现方式里, 写入会覆盖注释, 慎用哈..
  
  do_excel, 
  	封装了 Excel 的操作, 一般通过 read_all 方法读取全部用例数据, 放到内存中, 然后再通过内存中的对象来过滤和匹配数据
  	注意放在内存时, 应当保持单例, 不用自己实现单例, 将变量定义到模块, 然后其他位置使用时, 从该模块导入, 即是单例的
  	do_excel 中, 读取 Excel 是根据 excel.yml 配置的列读取的, 读取出数据, 会处理成 ExcelData 对象, 使用数据时, obj.attribute 即可获取数据
  
  do_log,
  	封装了两个日志打印, 
  	一个是项目日志打印,
  	一个是慢接口的打印.
  	打印时, 是根据 log.yml 中定义的信息来打印的
  	log.yml:
  		日志收集级别
  		控制台输出级别
  		文件输出级别
  		输出格式
  		输出颜色
  
  do_mongo,
  	MongoDB 操作, 类中有详细的注释说明
  	详细操作请直接找到代码阅读或调试
  
  do_mysql,
  	MySql 操作, 基础的增删改查
  	创建对象时, 自动连接 Mysql 数据库
  	使用完毕, GC 时, 自动释放该连接
  	我们不需要关注什么时候释放连接
  	只需要创建操作对象, 直接调用方法即可
  
  do_path,
  	就是项目内的路径
  	如果增加了某配置, 增加了某目录
  	需要在这里将该配置或目录添加进来
  	添加时, 保持代码是灵活的, 而不是复制绝对路径进来
  
  do_slow_api,
  	慢接口记录功能
  	接口响应慢时, 记录该接口信息, 响应时间到日志中
  
  do_time,
  	时间操作
  	有的接口需要传递时间区间
  	如果时间区间使用当前封装不好实现
  	需要添加封装逻辑时
  	请将时间操作的逻辑封装到该模块中
  
  do_try,
  	没什么用, 就是 with 语句简化 try 语句
  ```

- base_api
  ```apl
  BaseApi
  	__init__
  		初始化对象时, 初始化 token, terminal, host
  	send
  		发起请求
  BaseLogin(BaseApi)
  	simple_login
  		简单登录, 
  		根据 device 参数去 yaml 文件加载信息, 
  		然后更新 username 和 password,
  		调用登录接口
  		返回 token 
  ```
  
- base_assert
  ```apl
  通用断言
  	断言没什么需要注意的
  	就是维护时, 大家不要写太多断言逻辑在这个文件
  	保持仅封装通用断言逻辑进来
  	个别场景下, 需要定制断言时, 直接在用例中写明即可
  ```

- base_data
  ```apl
  通用数据
  	这里就是用来存储单例的, 全局的, 全量的 Excel 数据
  	CaseData:
  		data 属性用来存储数据
  		get 方法用来匹配数据
  
  all_data 就是单例的, 全局的, 全量的 Excel 数据
  当多 Excel 文件时候, 保持每个 Excel 搭配一个变量
  每个变量都是创建 CaseData 对象来存储 Excel 数据
  例 :
      all_a = CaseData(do_conf.read_one('excel_a', 'file_name_a'))
      all_h = CaseData(do_conf.read_one('excel_h', 'file_name_h'))
      all_c = CaseData(do_conf.read_one('excel_c', 'file_name_c'))
  ```

- base_extract
  ```apl
  通用提取
  	直接对 dict 按照层级提取
  	jsonpath 提取
  	等等
  	遇到不能满足的场景时, 可以来这里封装新的提取逻辑
  	请保持代码整洁, 写好注释信息
  ```

- excel.yml
  ```apl
  file_name
  	当 Excel 多了之后, 可以维护多个 file_name, 定义好区分标记就行, 比如 file_name_a, file_name_h, file_name_doctor 等
  column
  	加载 Excel 时, 读取这些列, 需和 Excel 的第二行保持一致, 所有 Excel, 所有 Sheet 的第二行都需要包含这里配置的列明
  index
  	与 column 一一对应, 如果修改了 column, 请同步修改 index
  	修改 index 时, 有一个简便的方式, 就是直接运行 do_excel 模块的 show 方法, 控制台会打印出可以直接复制粘贴的 index
  ```

- log.yml
  ```apl
  这里可能需要修改的就两个位置
  1.log_collection
  	这个是日志收集器的等级, 如果不想看 debug 等级的日志, 将这里修改为 info 即可
  2.color
  	控制台的颜色配置, 可以在这里修改
  ```

- login.yml
  ```apl
  登录的相关配置, 其实可以考虑和 request.yml 进行合并
  
  该配置文件可能需要人工维护
  需要维护的场景是:
  	1.开发修改了登录的逻辑
  	2.自动化测试需要添加新的端, 登录逻辑在已有逻辑中不包含
  
  配置解释:
  pc
  	pc 端登录时, 需要的参数
  app
  	app 端, 医生和健管师登录时, 需要的参数
  public
  	app 端, 患者登录时, 需要的参数
  mini
  	小程序预留, 暂时没用
  password
  	'a123456' 加密之后的值
  	也就是默认密码
  	注意密码错误的接口, 不要从这里进行替换, 哈哈, 难调试
  pa_a
  	运营端登录的 url
  pc_c
  	CRM 端登录的 url
  pc_h
  	全病程登录的 url
  app_h
  	app 端, 医生和健管师登录的 url
  public_h
  	app 端, 患者登录的 url
  ```

- mongo.yml
  ```apl
  有用信息就是, host 到 database 这些
  其他的没啥卵用哈
  ```

- request.yml
  ```apl
  维护了 host 和 verify_url
  
  可以考虑和 login.yml 合并
  ```

- slow_api.yml
  ```apl
  九尾狐了 maximum_time 表示毫秒为单位的时间
  当接口处理时间比该时间长时, 就会记录到日志中
  
  awk '{print $2,$3,$6,$8}' slow_api_log.out | sort -k 4 -nr | sort -k 3,3 -u
  对日志记录进行排序, 去重, 留下关键信息
  ```

- extract.yml
  ```apl
  数据提取文件
  所有提取的数据存放在该文件中
  ```

## 规范说明

### 基础规范

基础规范直接参考 pep8 规范

该文档不介绍 Python 基础, 不介绍 Pytest 基础, 只是对于我们团队的编码规范做一个说明, 我们团队的编码规范, 和行业约定俗称的规范大差不差, 请大家编码时务必遵守, 共同维护好我们的项目, 共同提高编码能力, 共勉

### PEP8 

PEP8 是什么呢, 简单说就是一种编码规范, 是为了让代码 "更好看", 更容易被阅读. 具体 PEP8 规范内容, 请查看 [PEP8规范文档](https://peps.python.org/pep-0008/).

为什么要先说 PEP8 规范, 不仅仅是因为它是官方的, 大家公认, 共同遵守的, 更是因为 Pycharm 本身集成了该规范检查, 我们通过 Pycharm 的检查快捷键, 可以快速帮我们检查代码是否符合规范, 快速将规范统一起来. 在 Pycharm 中, 自动检查并调整到符合 PEP8 规范的快捷键: ``` Ctrl + Alt + L ```

当我们编辑完代码之后, 在编辑器页面, 按下 ``` Ctrl + Alt + L ``` Pycharm 会自动将代码调整到规范样式, 并对不规范部分进行标注, 大家可以通过编辑器页面右上角的黄色波浪线来了解详细信息, 并作出相应调整. 要养成多按 ``` Ctrl + Alt + L ``` 的习惯和关注右上角红色波浪线和黄色波浪线的习惯. 

### Py文件

- 变量
  变量主要就是命名规范, 好的名称是能很方便帮助我们阅读代码的, 就比如大家在编辑 Bug 时, 都是会注明是什么环境, 哪一个端, 小程序还是 App, 一样的, 如果我们变量命名很规范, 那么当其他人阅读我们代码时候, 就会非常轻松.

  ```apl
  # 强制规范:
      字母或下划线开头 ( 汉字其实也行, 但是不建议 )
      字幕数字下划线组成
      不能是 Python 关键字
  "强制规范是不遵守就命名不了的, 我们除了强制规范外还需要遵守如下规范"
  
  # 其他必要规范:
      基本都遵从小驼峰命名
      见名知意
      避开包名和模块名
      避开内置函数名
      避开库名
  " fle_name 而非 FileName 也非 File_Name, 当然部分变量有自己独有的命规范, 大多数都是要求小驼峰."
  " 取名时候要考虑到该变量是做什么使用的, 比如测试用例(test_case), 比如, 比如用例数据(case_data)等. 除了一些 for 循环的代码可以用 i 来表示循环次数外, 要求大家一定要按照含义来命名变量名."
  " 有个 requests 库, 用于发起 http 请求, 如果我们变量也叫做 requests, 就很容易报错"
  
  # 小技巧:
  	下划线
  	同义词
  "比如我们一个方法中要用到两个变量表示 "用例数据", 那我们可以是 case_data, 也可以是 _data_case. 或者我们有两个变量都是 "多个数据", 那我们可以是一个变量叫做 datas, 另一个变量叫做 _datas 或者 data_s 和 _data_s. 这样既区分了变量, 也做到了见名之意."
  ```

- 函数
  函数规范有函数命名, 函数参数, 函数返回值等

  ```apl
  # 命名
  见名知意, 简明扼要, 不要太长, 不要重名
  
  # 参数
  见名知意, 只定义必要参数, 不要太多(5)
  
  # 返回值
  一般都返回单个的返回值, 尽量不要返回多个返回值
  分支中, 避免有些分支定义了返回值, 而有些分支未定义返回值
  分支中, 避免不同分支返回不同的数据类型
  
  # 数量和分类
  同一个文件中, 保持函数功能一致, 不要全都放到一个文件中
  ```

- 注释

  ```apl
  注释是给阅读代码提供帮助的, 注释分为单行注释和多行注释.
  
  一定要给代码加上必要的注释. 大家按 ctrl 右键点击内置函数, 或者点击其他第三方的函数时, 都是能看到注释的, 因此我们也需要给我们的代码加上注释.
  
  注释注意文明用语, 书面语言, 将功能用法等关键信息将清楚, 言简意赅, 不要长篇大论, 如果注释的代码做了调整, 响应对代码注释也要进行调整.
  
  一般函数开头都要添加注释, 用于说明该函数的作用, 辅助理解和使用.
  ```

- 空行

  ```apl
  适当的空行
  
  空行可以用于给代码分块, 一段代码和一段代码之间可以用空行来隔开, 方便阅读. 
  
  连续空行不要太多, 也不要每行代码都加空行. 一定要和代码段结合起来
  ```

- 长度

  ```apl
  单行代码也不宜过长. 
  
  不过大家都是大屏写代码, 可以适当将 Pycharm 的长度检查调长一些. 
  ```

- 类

  ```apl
  # 类名
  	类名是遵从大驼峰, 首字母大写, 比如 CaseUtil, DBUtil 等. 
  # 属性
  	实例属性定义在 __init__() 方法中
  	类属性定义在类中
  # 方法
  	用的最多的是实例方法
  # 注释
  	类的文档注释, 类一般需要添加文档注释, 说明该类的功能作用. 文档注释位置是类开头, 用三引号来标记.
  	方法的说明注释, 方法也需要说明注释, 用来介绍方法的参数, 返回值, 方法的功能等信息, 也是在方法的一开头, 用三引号来标记.
  ```

- 异常

  ```apl
  对代码进行异常捕获时, 一定要清楚捕获什么异常, 避免使用 Exception. 而是使用具体的异常, 比如 NameError, KeyError 等这种具体的异常.
  ```

### 模块

- 导包

  ```apl
  先内置, 再第三方, 再自定义
  先 import 再 from xxx import xxxx
  
  避开相互导包 ( A中导B, B中又导A )
  
  不要一次性 import 多个包
  避免对导入的包进行重命名
  
  暂时避免在 __init__ 中定义导包相关信息
  ```

- 层级

  ```apl
  同一层级下, 放相同的封装, 相同功能的代码, 做好层级划分
  ```

- 包和文件夹

  ```apl
  包用来管理 py 文件
  文件夹用来管理静态文件资源
  
  包和文件夹的命名也需要见名之意, 也需要做好层级的划分.
  # 包名, 文件夹名, 文件名, 模块命, 都叫标识符, 标识符的命名规范遵从变量的命名规范
  ```

- 路径

  ```apl
  避免写死路径
  可以参考我们项目中的 path_util 来管理项目中的各路径信息
  ```

- 日志

  ```apl
  debug 日志可以随便打印
  info 日志打印关键节点信息
  error 日志不要使用 error 方法, 而使用 exception 方法.
  ```

### 环境

- 兼容性

  ```apl
  Python2 和 Python3 不兼容, 我们统一使用 Python3.
  ```

- 解释器环境和虚拟环境

  ```apl
  我们当前可以使用解释器环境, 但是当我们管理的项目多了, 复杂了, 就需要使用虚拟环境进行环境隔离了.
  
  如果大家更改了代码, 导入了新的第三方库, 一定要更新 requirements.txt 文件, 保证可以通过该文件来一次性导入所有项目中使用的第三方库信息. 详细的更新和使用方式可以参考项目中的 readme.md 文档.
  ```

### 最后

补充一点, 强调一点.

- 后续还会补充一些规范进来
  - 打开文件就配合关闭文件
  - 建立连接就配合关闭连接
  - 单一职责原则
  - 开闭原则
  - 等
- 强调大家多多使用 ``` Ctrl + Alt + L ``` 先锻炼起日常的编码规范, 熟练之后还需要遵守一些设计上的规范, 就是上边提到的补充规范的范畴

### 封装规范

封装逻辑时, 需要注意三点

- 先确定原逻辑不支持, 必须封装新逻辑
- 再确定封装是有效的, 避免留下太多无效封装, 比如已有的 do_try , base_device 这种
- 注意编码规范, 写清楚注释信息, 方便大家阅读和使用

### 用例规范

- 命名
  ```apl
  # 模块名
  	test_*
  # 类名
  	Test*
  # 方法名
  	test_*
  
  命名不要太随意, 需要和实际业务场景, 实际模块保持相关性, 比如医生用 doctor 来体现
  ```

- conftest
  ```apl
  # 层级
  	因为需要大家为不同接口定义不同的 test_case, 
  	所以 conftest 的编写会越来越多,
  	那么大家编写时, 就需要注意 conftest 的层级关系,
  	用例执行时, 距离最近的 conftest 是优先级最高的,
  	外层已有的 conftest 逻辑, 如果能应用到内部, 
  	就不要在内部再定义重复逻辑,
  	比如全局 conftest 中的三个方法, 不要在子集的 conftest 重新定义
  
  # 逻辑
  	主要就是 conftest 的应用范围
  	function / class / module / package / session
  	定义 conftest 的逻辑时, 请注意 scope, 大了一般没事, 小了容易报错
  	yield 关键字是用来分割运行前后的逻辑和定义返回值的
  	前置放在 yield 之前的行,
  	后置放在 yield 之后的行,
  	返回值定义在 yield 关键字后边
  	
  	注意一点就是, autouse 的 fixture, yield 返回值无效
  
  # 参数化
  	参数化都通过 fixture 来进行
  
  -----------------------------------------------------------------------------------------------
  # 参数化示例
  @pytest.fixture(scope='function', params=[{'pageSize': '10'}, {'pageSize': '20'}], name='page')
  def page(request):
      _data = request.param
      _data['pageNo'] = '1'
      _data['clientStatus'] = 'PROSPECTIVE_CUSTOMER'
      yield _data
  
  # 示例说明
  装饰器是固定格式, 可以仅定义 params
  name 时命名, test_case 使用时, 是根据 name 找 fixture 的, 如果 name 未定义, 则 name 为方法名
  参数化的 fixture, 必须有 request 参数, 通过 request.param 就可以获得实际参数化的数据
  实际使用时, params 传的都是类似于 all_data.get('登录模块', 'Login') 这种格式
  all_data 就是 Excel 读取出来的全量数据, 时导包进来的
  get 就是匹配值的方法, get 接收两个参数, 分别是 Sheet 页和 case_id 标识
  -----------------------------------------------------------------------------------------------
  ```

- test_case
  ```apl
  至少包含两处逻辑:
  1. 调用接口
  2. 断言结果
  
  test_case 的模块需要注意顺序, 模块层面是按照 ASCII 码来处理顺序的
  test_case 模块内部, 是按照定义顺序处理
  参数化用例是根据参数化顺序处理的
  ```

  
