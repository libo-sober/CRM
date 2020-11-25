from django.utils.safestring import mark_safe


class MyPagination:

    def __init__(self, page_id, num, base_url, page_count=9, record=15):
        a, b = divmod(num, record)
        page = a + 1 if b else a  # 这些记录可以分多少页
        mid = page_count // 2
        if page_id is None:
            page_id = 1
        else:
            page_id = int(page_id)
        if page_id <= mid:
            page_num_list = range(1, page_count + 1)
        elif page_id > page - mid:
            page_num_list = range(page - page_count + 1, page + 1)
        else:
            page_num_list = range(page_id - mid, page_id + mid + 1)
        self.page_id = page_id
        self.num = num
        self.page = page
        self.page_num_list = page_num_list
        self.record = record
        self.base_url = base_url

    @property
    def get_record(self):
        return self.record

    @property
    def get_page_id(self):
        return self.page_id

    def html_page(self):
        page_html = '<div class="container"><div class="row"><div class="row-cols-8 offset-2"><nav aria-label="Page navigation"><ul class="pagination">'

        if self.page_id <= 1:
            page_pre = f'<li class="disabled"><a href="javascript:void(0)" aria-label="Previous"><span style="font-size: 25px" aria-hidden="true">&laquo;</span></a></li>'
        else:
            page_pre = f'<li><a href="{self.base_url}?page={self.page_id - 1}" aria-label="Previous"><span style="font-size: 25px" aria-hidden="true">&laquo;</span></a></li>'
        page_html += page_pre
        for i in self.page_num_list:
            if i == self.page_id:
                page_html += f'<li class="active" style="font-size: 25px"><a href="{self.base_url}?page={i}"> {i} </a></li>'
            else:
                page_html += f'<li style="font-size: 25px"><a href="{self.base_url}?page={i}"> {i} </a></li>'
        if self.page_id >= self.page:
            page_last = f'<li class="disabled"><a href="javascript:void(0)" aria-label="Next"><span style="font-size: 25px" aria-hidden="true">&raquo;</span></a></li>'
        else:
            page_last = f'<li><a href="{self.base_url}?page={self.page_id + 1}" aria-label="Next"><span style="font-size: 25px" aria-hidden="true">&raquo;</span></a></li>'
        page_html += page_last
        page_html += '</ul></nav></div></div></div>'
        # mark_safe()后端包裹后，前端就不要safe过滤了，自动识别成标签
        return mark_safe(page_html)
