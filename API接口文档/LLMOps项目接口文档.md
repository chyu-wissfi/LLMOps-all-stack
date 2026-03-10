# **LLMOps 项目** **API** **文档**

应用 API 接口统一以 JSON 格式返回，并且包含 3 个字段： `code` 、 `data`  和  `message` ，分别代表 `业务状态码` 、 `业务数据` 和 `接口附加信息` 。

`业务状态码` 共有 6 种，其中只有  `success(成功)`  代表业务操作成功，其他 5 种状态均代表失败，并且失败时会附加相关的信息： `fail(通用失败)` 、 `not_found(未找到)` 、 `unauthorized(未授权)` 、 `forbidden(无权限)` 和 `validate_error(数据验证失败)` 。

接口示例：

```JSON

```

带有分页数据的接口会在  `data`  内固定传递  `list`  和  `paginator`  字段，其中  `list`  代表分页后的列表数据， `paginator`  代表分页的数据。

`paginator`  内存在 4 个字段： `current_page(当前页数)`  、 `page_size(每页数据条数)` 、 `total_page(总页数)` 、 `total_record(总记录条数)` ，示例数据如下：

```JSON

```

如果接口需要授权，需要在  `headers`  中添加  `Authorization`  ，并附加  `access_token`  即可完成授权登录，示例：

```Plain

```

## **01. 应用模块**