import pandas as pd
import matplotlib.pyplot as plt

# Messy product-inventory dataset
data = {
    "Product":  ["Cola", "Chips", "Milk", "Biscuits", "Juice",
                 "Yogurt", "Popcorn", "Water", "Cheese", "Nuts"],
    "Category": ["beverages ", "SNACKS", " Dairy", "Snacks", "beverages",
                 "DAIRY ", " snacks", "Beverages", "dairy", "SNACKS "],
    "Price":    ["Rs. 1,250", "Rs. 90", "Rs. 450", "Rs. 120", "Rs. 1,800",
                 "Rs. 200", "Rs. 150", "Rs. 60", "Rs. 1,100", "Rs. 950"],
    "Stock":    [40, 120, 60, 90, 35, 70, 80, 150, 25, 55],
}
df = pd.DataFrame(data)

# (a) Clean Category
df["Category"] = df["Category"].str.strip().str.title()

# (b) Convert Price to numeric
df["Price"] = (df["Price"].str.replace("Rs. ", "", regex=False)
                          .str.replace(",", "", regex=False)
                          .astype(float))

# (c) Label encoding + print
df["Category_Code"] = df["Category"].astype("category").cat.codes
print(df)

# (d) Bar (avg price) + pie (stock share) side by side
avg_price = df.groupby("Category")["Price"].mean()
stock_share = df.groupby("Category")["Stock"].sum()

fig, axes = plt.subplots(1, 2, figsize=(11, 4.5))

axes[0].bar(avg_price.index, avg_price.values,
            color=["#4C78A8", "#F58518", "#54A24B"])
axes[0].set_title("Average Price per Category")
axes[0].set_xlabel("Category")
axes[0].set_ylabel("Average Price (Rs.)")

axes[1].pie(stock_share.values, labels=stock_share.index,
            autopct="%1.1f%%", startangle=90,
            colors=["#4C78A8", "#F58518", "#54A24B"])
axes[1].set_title("Share of Total Stock by Category")

fig.suptitle("Inventory Overview")
plt.tight_layout()
plt.savefig("inventory_plots.png")
plt.show()
print("Saved inventory_plots.png")