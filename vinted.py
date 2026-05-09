from playwright.sync_api import sync_playwright
import json
import os

SEEN_FILE = "seen.json"


def load_seen():
    if not os.path.exists(SEEN_FILE):
        return set()

    with open(SEEN_FILE, "r") as f:
        return set(json.load(f))


def save_seen(seen):
    with open(SEEN_FILE, "w") as f:
        json.dump(list(seen), f)


def search_items():
    seen = load_seen()

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        url = "https://www.vinted.pt/catalog?search_text=amazfit%20helio%20strap&order=newest_first"

        page.goto(url)

        # espera produtos carregarem
        page.wait_for_timeout(7000)

        # vai buscar links reais dos produtos
        links = page.eval_on_selector_all(
            "a",
            """els => els
                .map(e => e.href)
                .filter(h => h && h.includes('/items/'))"""
        )

        items = []

        for link in links[:10]:

            # evita duplicados
            if link in seen:
                continue

            try:
                product = browser.new_page()

                product.goto(link)

                product.wait_for_timeout(3000)

                # ------------------------
                # TÍTULO
                # ------------------------

                title_el = product.query_selector("h1")

                title = (
                    title_el.inner_text().strip()
                    if title_el
                    else "Produto Vinted"
                )

                # ------------------------
                # PREÇO
                # ------------------------

                price_el = product.query_selector(
                    "[data-testid='item-price']"
                )

                price = (
                    price_el.inner_text().strip()
                    if price_el
                    else "ver site"
                )

                # ------------------------
                # IMAGEM
                # ------------------------

                image = ""

                imgs = product.query_selector_all("img")

                for img in imgs:

                    src = (
                        img.get_attribute("src")
                        or img.get_attribute("data-src")
                        or img.get_attribute("srcset")
                    )

                    if src and (
                        "images" in src
                        or "photo" in src
                        or "f800" in src
                    ):
                        image = src.split(" ")[0]
                        break

                # ------------------------
                # GUARDAR ITEM
                # ------------------------

                items.append({
                    "id": link,
                    "title": title,
                    "price": price,
                    "url": link,
                    "image": image
                })

                # marca como visto
                seen.add(link)

                product.close()

            except Exception as e:
                print("Erro produto:", e)
                continue

        browser.close()

    save_seen(seen)

    return items