import os
from playwright.sync_api import sync_playwright

PLAYER_ID = os.environ["PLAYER_ID"].strip()
STORE_URL = "https://store.eternalhero.rivvy.games/"

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1280, "height": 800})

        try:
            # 1. 웹 상점 사이트로 이동 후 쿠키 팝업이 뜰 때까지 잠깐 대기
            page.goto(STORE_URL, wait_until="networkidle")
            page.wait_for_timeout(1500)

            # 2. 쿠키 안내 팝업이 뜨면 닫기
            dismiss_btn = page.get_by_role("button", name="Dismiss")
            if dismiss_btn.is_visible():
                dismiss_btn.click()
                page.wait_for_timeout(500)

            # 3. 'Enter your player id...' 입력창을 정확히 찾아서 타이핑
            inp = page.get_by_placeholder("Enter your player id...")
            inp.click()
            inp.press_sequentially(PLAYER_ID, delay=50)
            print("입력된 ID 글자 수:", len(inp.input_value()))
            page.wait_for_timeout(500)

            # 4. 입력창 바로 아래에 있는 'Log in' 버튼만 정확히 클릭
            login_box = inp.locator("xpath=ancestor::*[.//button[contains(., 'Log in')]][1]")
            login_box.get_by_role("button", name="Log in").click()
            page.wait_for_timeout(4000)

            # 5. 로그인 후 화면 상태 확인용 로그
            print("로그인 후 입력창 남아있는지:", inp.is_visible())

            # 6. 무료 아이템(echo_shard_pack_free) 버튼 클릭
            free_btn = page.locator('[data-sku="echo_shard_pack_free"]').first
            free_btn.scroll_into_view_if_needed()
            free_btn.click()
            page.wait_for_timeout(3000)

            # 7. 장바구니(Cart) 버튼이 있으면 열어보기
            cart_btn = page.locator("button:has-text('Cart'):visible").first
            if cart_btn.is_visible():
                cart_btn.click()
                page.wait_for_timeout(2000)

        finally:
            page.screenshot(path="result.png", full_page=False)
            browser.close()

if __name__ == "__main__":
    run()
