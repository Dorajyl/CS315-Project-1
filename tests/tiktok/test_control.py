from page_objects.PageTiktok import PageTiktok
import time

def test_control():
    # login with your control tiktok account
    page = PageTiktok()
    page.fetch_tiktok()
    time.sleep(60)
    page.iterate_through_batches_control()
    time.sleep(10)
