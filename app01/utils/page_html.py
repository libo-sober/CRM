from django.utils.safestring import mark_safe


class MyPagination:

    def __init__(self, page_id, num, base_url, get_data=None, page_count=9, record=15):
        """
        初始化数据
        :param page_id: 当前页码数
        :param num: 要展示的总共记录数
        :param base_url: 请求路径
        :param page_count: 页数栏显示多少个数，是个奇数
        :param record: 每页显示多少条记录
        """
        a, b = divmod(num, record)
        page = a + 1 if b else a  # 这些记录可以分多少页
        mid = page_count // 2  # 页码栏中间值

        # GET请求得到的值位字符串或者None
        if page_id is None:
            page_id = 1
        else:
            page_id = int(page_id)

        # 请求当前页码小于等于页码栏中间值
        if page_id <= mid:
            page_num_list = range(1, page_count + 1)
        elif page_id > page - mid:
            page_num_list = range(page - page_count + 1, page + 1)
        else:
            page_num_list = range(page_id - mid, page_id + mid + 1)

        # 如果总页数小于要显示的页数
        if page < page_count:
            page_num_list = range(1, page + 1)

        self.page_id = page_id
        self.num = num
        self.page = page
        self.page_num_list = page_num_list
        self.record = record
        self.base_url = base_url
        self.get_data = get_data

    @property
    def get_record(self):
        return self.record

    @property
    def get_page_id(self):
        return self.page_id

    def html_page(self):
        page_html = '<div class="container"><div class="row"><div class="row-cols-8 offset-2"><nav aria-label="Page navigation"><ul class="pagination">'
        # 首页
        self.get_data['page'] = 1
        first_page = f'<li><a href="{self.base_url}?{self.get_data.urlencode()}" aria-label="Previous"><span style="font-size: 25px" aria-hidden="true">首页</span></a></li>'
        page_html += first_page
        # 上一页
        # 小于等于1后不允许点击上一页
        if self.page_id <= 1:
            page_pre = f'<li class="disabled"><a href="javascript:void(0)" aria-label="Previous"><span style="font-size: 25px" aria-hidden="true">&laquo;</span></a></li>'
        else:
            self.get_data['page'] = self.page_id - 1
            page_pre = f'<li><a href="{self.base_url}?{self.get_data.urlencode()}" aria-label="Previous"><span style="font-size: 25px" aria-hidden="true">&laquo;</span></a></li>'
        page_html += page_pre
        # 动态生成page
        for i in self.page_num_list:
            self.get_data['page'] = i  # 把发来的page动态生成
            if i == self.page_id:
                page_html += f'<li class="active" style="font-size: 25px"><a href="{self.base_url}?{self.get_data.urlencode()}"> {i} </a></li>'
            else:
                page_html += f'<li style="font-size: 25px"><a href="{self.base_url}?{self.get_data.urlencode()}"> {i} </a></li>'
        # 下一页
        if self.page_id >= self.page:
            page_last = f'<li class="disabled"><a href="javascript:void(0)" aria-label="Next"><span style="font-size: 25px" aria-hidden="true">&raquo;</span></a></li>'
        else:
            self.get_data['page'] = self.page_id + 1
            page_last = f'<li><a href="{self.base_url}?{self.get_data.urlencode()}" aria-label="Next"><span style="font-size: 25px" aria-hidden="true">&raquo;</span></a></li>'
        page_html += page_last
        # 尾页
        self.get_data['page'] = self.page
        last_page = f'<li><a href="{self.base_url}?{self.get_data.urlencode()}" aria-label="Previous"><span style="font-size: 25px" aria-hidden="true">尾页</span></a></li>'
        page_html += last_page
        page_html += '</ul></nav></div></div></div>'
        # mark_safe()后端包裹后，前端就不要safe过滤了，自动识别成标签
        return mark_safe(page_html)
