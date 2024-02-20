from page_objects.PageTiktok import PageTiktok
import time

def test_save_random():
    # login with your active tiktok account
    page = PageTiktok()
    page.fetch_tiktok()
    time.sleep(60)
    page.iterate_through_batches_save_random()
    time.sleep(10)


