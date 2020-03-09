class Pages:
    def __init__(self):
        self.all_tokens = []
        self.last_tokens_freq = {}

        self.all_links = {}
        self.all_links_visited = {}

        self.largest_page = ''
        self.largest_page_token_count = 0

        self.ics_sub_domains = {}

    def get_all_tokens(self):
        return self.all_tokens

    def get_largest_page(self):
        return self.largest_page, self.largest_page_token_count

    def set_largest_page(self, new_largest_page, new_largest_page_token_count):
        if new_largest_page_token_count > self.largest_page_token_count:
            self.largest_page = new_largest_page
            self.largest_page_token_count = new_largest_page_token_count
            # print(self.get_largest_page())

    def get_last_tokens_freq(self):
        return self.last_tokens_freq

    def set_last_tokens_freq(self, new_last_tokens_freq):
        self.last_tokens_freq = new_last_tokens_freq

    def get_all_links(self):
        return self.all_links

    def get_all_links_visited(self):
        return self.all_links_visited

    def get_ics_sub_domains(self):
        return self.ics_sub_domains

