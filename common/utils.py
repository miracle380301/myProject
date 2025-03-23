import csv
import os

def paginate_exchanges(exchange_list, page, items_per_page=50):
    total_exchanges = len(exchange_list)
    total_pages = (total_exchanges + items_per_page - 1) // items_per_page  # 전체 페이지 수

    start_idx = (page - 1) * items_per_page
    end_idx = min(start_idx + items_per_page, total_exchanges)

    return exchange_list[start_idx:end_idx], total_pages

def check_name_exists(name, file_path):
    with open(file_path, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        rows = list(reader)
        if not rows:
            return False
        for row in rows:
            if row['name'].lower() == name.lower():
                return True
    return False

def save_to_csv(exchanges, csv_file):
    with open(csv_file, 'a+', newline='', encoding='utf-8') as csv_file:
        fieldnames = ["origin", "id", "name", "year_established", "country", "url", "logo_image", "create_dt", "update_dt"]
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        if os.path.getsize(csv_file.name) == 0:  # Check if file is empty
                    writer.writeheader()  # Write header if file is empty
        for exchange in exchanges:
            writer.writerow({
                "origin": exchange.origin,
                "id": exchange.id,
                "name": exchange.name,
                "year_established": exchange.year_established,
                "country": exchange.country,
                "url": exchange.url,
                "logo_image": exchange.logo_image,
                "create_dt": exchange.create_dt,
                "update_dt": exchange.update_dt,
            })

    print("Exchange data has been saved to", csv_file)
