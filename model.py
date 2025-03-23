from datetime import datetime

class Exchange:
    def __init__(self, origin, id, name, year_established, country, url, logo_image, create_dt=None, update_dt=None):
        self.origin = origin
        self.id = id
        self.name = name
        self.year_established = year_established
        self.country = country
        self.url = url
        self.logo_image = logo_image
        self.create_dt = create_dt if create_dt else datetime.now()
        self.update_dt = update_dt if update_dt else datetime.now()

    def __repr__(self):
        return f"Exchange(origin={self.origin}, id={self.id}, name={self.name}, year_established={self.year_established}, country={self.country}, url={self.url}, logo_image={self.logo_image}, create_dt={self.create_dt}, update_dt={self.update_dt})"
