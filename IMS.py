class User:
    def __init__(self, username, password, role):
        self.username = username
        self.password = password
        self.role = role


class Product:
    def __init__(self, product_id, name, category, price, stock_quantity):
        self.product_id = product_id
        self.name = name
        self.category = category
        self.price = price
        self.stock_quantity = stock_quantity

    def __str__(self):
        return (f"ID: {self.product_id}, Name: {self.name}, Category: {self.category}, "
                f"Price: ${self.price}, Stock: {self.stock_quantity}")

    def update_stock(self, quantity):
        self.stock_quantity += quantity

    def update_product(self, name=None, category=None, price=None, stock_quantity=None):
        if name: self.name = name
        if category: self.category = category
        if price: self.price = price
        if stock_quantity is not None: self.stock_quantity = stock_quantity


class InventorySystem:
    def __init__(self):
        self.users = {
            "admin": User("admin", "admin123", "Admin"),
            "user": User("user", "user123", "User")
        }
        self.products = {}
        self.current_user = None

    def login(self, username, password):
        user = self.users.get(username)
        if user and user.password == password:
            self.current_user = user
            print(f"Welcome {self.current_user.username}! You are logged in as {self.current_user.role}.")
            return True
        print("Invalid username or password.")
        return False

    def logout(self):
        self.current_user = None
        print("Logged out successfully.")

    def add_product(self, product_id, name, category, price, stock_quantity):
        if self.current_user.role != "Admin":
            print("Permission denied. Only Admins can add products.")
            return
        if product_id in self.products:
            print("Product with this ID already exists.")
            return
        self.products[product_id] = Product(product_id, name, category, price, stock_quantity)
        print(f"Product {name} added successfully.")

    def edit_product(self, product_id, name=None, category=None, price=None, stock_quantity=None):
        if self.current_user.role != "Admin":
            print("Permission denied. Only Admins can edit products.")
            return
        product = self.products.get(product_id)
        if not product:
            print("Product not found.")
            return
        product.update_product(name, category, price, stock_quantity)
        print(f"Product ID {product_id} updated successfully.")

    def delete_product(self, product_id):
        if self.current_user.role != "Admin":
            print("Permission denied. Only Admins can delete products.")
            return
        if product_id in self.products:
            del self.products[product_id]
            print(f"Product ID {product_id} deleted successfully.")
        else:
            print("Product not found.")

    def view_products(self):
        if not self.products:
            print("No products available.")
            return
        for product in self.products.values():
            print(product)

    def search_product(self, search_term):
        results = [product for product in self.products.values() if search_term.lower() in product.name.lower()]
        if results:
            for product in results:
                print(product)
        else:
            print("No products found matching the search term.")

    def filter_products_by_stock(self, threshold):
        results = [product for product in self.products.values() if product.stock_quantity <= threshold]
        if results:
            for product in results:
                print(product)
        else:
            print("No products found with stock below threshold.")

    def adjust_stock(self, product_id, quantity):
        product = self.products.get(product_id)
        if not product:
            print("Product not found.")
            return
        product.update_stock(quantity)
        print(f"Stock updated for Product ID {product_id}. New stock: {product.stock_quantity}")

        # Alert if stock is low
        if product.stock_quantity < 5:
            print(f"Alert: Stock for {product.name} is low, consider restocking!")


def main():
    ims = InventorySystem()

    while True:
        print("\n--- Inventory Management System ---")
        if ims.current_user:
            if ims.current_user.role == "Admin":
                print("1. Add Product")
                print("2. Edit Product")
                print("3. Delete Product")
                print("4. View Products")
                print("5. Search Product")
                print("6. Filter Products by Stock")
                print("7. Adjust Stock")
                print("8. Logout")
            else:
                print("1. View Products")
                print("2. Search Product")
                print("3. Filter Products by Stock")
                print("4. Logout")

            choice = input("Select an option: ")
            if choice == "1" and ims.current_user.role == "Admin":
                product_id = input("Enter product ID: ")
                name = input("Enter product name: ")
                category = input("Enter category: ")
                price = float(input("Enter price: "))
                stock_quantity = int(input("Enter stock quantity: "))
                ims.add_product(product_id, name, category, price, stock_quantity)
            elif choice == "2" and ims.current_user.role == "Admin":
                product_id = input("Enter product ID to edit: ")
                name = input("Enter new name (or press Enter to skip): ")
                category = input("Enter new category (or press Enter to skip): ")
                price = input("Enter new price (or press Enter to skip): ")
                stock_quantity = input("Enter new stock quantity (or press Enter to skip): ")
                ims.edit_product(product_id, name, category, float(price) if price else None, int(stock_quantity) if stock_quantity else None)
            elif choice == "3" and ims.current_user.role == "Admin":
                product_id = input("Enter product ID to delete: ")
                ims.delete_product(product_id)
            elif choice == "4":
                ims.view_products()
            elif choice == "5":
                search_term = input("Enter product name to search: ")
                ims.search_product(search_term)
            elif choice == "6":
                threshold = int(input("Enter stock threshold: "))
                ims.filter_products_by_stock(threshold)
            elif choice == "7" and ims.current_user.role == "Admin":
                product_id = input("Enter product ID to adjust stock: ")
                quantity = int(input("Enter quantity to adjust (positive to add, negative to reduce): "))
                ims.adjust_stock(product_id, quantity)
            elif choice == "8" or (choice == "4" and ims.current_user.role == "User"):
                ims.logout()
            else:
                print("Invalid option.")
        else:
            print("1. Login")
            print("2. Exit")
            choice = input("Select an option: ")
            if choice == "1":
                username = input("Enter username: ")
                password = input("Enter password: ")
                ims.login(username, password)
            elif choice == "2":
                print("Exiting the system.")
                break
            else:
                print("Invalid option.")

if __name__ == "__main__":
    main()
