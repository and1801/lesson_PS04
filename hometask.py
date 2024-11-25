from selenium import webdriver
from selenium.webdriver.common.by import By

def get_paragraphs(driver):
    paragraphs = driver.find_elements(By.XPATH, "//p")
    return [p.text for p in paragraphs if p.text.strip()]

def get_internal_links(driver):
    links = driver.find_elements(By.XPATH, "//a[@href]")
    internal_links = {}
    for link in links:
        href = link.get_attribute('href')
        # Проверяем относительные и абсолютные пути
        if href and ('/wiki/' in href and not href.startswith('https://ru.wikipedia.org/')):
            href = "https://ru.wikipedia.org" + href
        if href and href.startswith('https://ru.wikipedia.org/wiki/'):  # Фильтруем только страницы Википедии
            text = link.text.strip()
            if not text:  # Если текст пустой, берем title или часть URL
                text = link.get_attribute('title') or href.split('/')[-1]
            internal_links[text] = href
    return internal_links

def main():
    driver = webdriver.Firefox()

    try:
        while True:
            # Запрос у пользователя
            search_query = input("Введите запрос для поиска на Википедии: ")
            search_url = f"https://ru.wikipedia.org/wiki/{search_query.replace(' ', '_')}"
            driver.get(search_url)

            action = ''
            while action != '3':
                print("\nВыберите действие:")
                print("1. Листать параграфы текущей статьи")
                print("2. Перейти на одну из связанных страниц")
                print("3. Выйти из программы")
                action = input("Введите номер действия: ").strip()

                if action == '1':
                    paragraphs = get_paragraphs(driver)
                    if not paragraphs:
                        print("Нет доступных параграфов для отображения.")
                        continue

                    for i, paragraph in enumerate(paragraphs):
                        print(f"\nПараграф {i+1}:\n{paragraph}")
                        if input("\nНажмите Enter для продолжения или введите 'стоп' для остановки: ").strip().lower() == 'стоп':
                            break

                elif action == '2':
                    links = get_internal_links(driver)
                    if not links:
                        print("Нет доступных связанных страниц.")
                        continue

                    print("\nДоступные связанные страницы:")
                    for i, (title, url) in enumerate(links.items(), start=1):
                        print(f"{i}. {title}")

                    link_choice = input("Введите номер страницы для перехода или 'назад' для возврата: ").strip()

                    if link_choice.isdigit() and 1 <= int(link_choice) <= len(links):
                        selected_link = list(links.values())[int(link_choice) - 1]
                        print(f"Переход к странице: {selected_link}")
                        driver.get(selected_link)
                    else:
                        print("Неверный выбор или возврат.")

                elif action == '3':
                    print("Выход из программы...")
                    break

                else:
                    print("Неверный выбор, попробуйте снова.")

    finally:
        driver.quit()

if __name__ == "__main__":
    main()

