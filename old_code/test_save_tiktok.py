from page_objects.PageTiktok import PageTiktok
import time

class TiktokAudit(PageTiktok):
    def test_save_hashtag(self):
        self.fetch_tiktok()
        self.iterate_through_batches_save_by_hashtag()
        time.sleep(10)

    def test_save_random(self):
        self.fetch_tiktok()
        self.iterate_through_batches_save_random()
        time.sleep(10)
