# Online Store Sales: Data Cleaning & Analysis

A data analysis project built with **Python, NumPy and pandas**. It takes a messy sales dataset, cleans it step by step, and analyzes it to find business insights.

---

## 1. Objective

- Clean a raw dataset that contains duplicates, missing values, wrong formats and outliers.
- Analyze the cleaned data to find which categories, cities and months earn the most revenue.
- Give simple business recommendations based on the findings.

---

## 2. Tools Used

| Tool | Purpose |
|------|---------|
| Python 3 | Main programming language |
| pandas | Loading, cleaning, grouping and pivoting data |
| NumPy | Random data generation, `np.where`, median, standard deviation |

---

## 3. Project Structure

```
sales_analysis_project/
|-- data/
|   |-- raw_sales_data.csv        # messy dataset (515 rows)
|   `-- clean_sales_data.csv      # cleaned dataset (492 rows)
|-- notebooks/
|   `-- sales_analysis.ipynb      # step-by-step Jupyter notebook
|-- sales_analysis_project.py     # same project as a single Python script
`-- README.md                     # project documentation
```

| Folder / File | Description |
|---------------|-------------|
| `data/` | Raw and cleaned CSV files |
| `notebooks/` | Notebook with markdown headings and one cell per cleaning/analysis step |
| `sales_analysis_project.py` | Complete script (generates, cleans and analyzes data) |

---

## 4. How to Run

1. Install Python 3.8 or higher.
2. Install the libraries:
   ```
   pip install numpy pandas jupyter
   ```
3. **Option A: Notebook (recommended)**
   ```
   cd notebooks
   jupyter notebook sales_analysis.ipynb
   ```
   Then run the cells from top to bottom (Kernel > Restart & Run All).

4. **Option B: Script**
   ```
   python sales_analysis_project.py
   ```
   Run it from the project's main folder.

Both options read and write the CSV files inside the `data/` folder.

> To use your own dataset, put the CSV in `data/` and replace the data creation step with `df = pd.read_csv("../data/yourfile.csv")` (notebook) or `pd.read_csv("data/yourfile.csv")` (script). Then change the column names in the cleaning steps.

---

## 5. Dataset Description

| Column | Description |
|--------|-------------|
| `order_id` | Unique order number |
| `order_date` | Date of the order (dd-mm-yyyy) |
| `city` | City where the order was placed |
| `category` | Product category (Electronics, Clothing, Grocery, Books, Home) |
| `quantity` | Number of items ordered |
| `unit_price` | Price per item (Rs.) |
| `discount_pct` | Discount given (%) |
| `rating` | Customer rating (1 to 5) |

**New columns created during cleaning:** `total_amount`, `month`, `order_size`

---

## 6. Data Problems Found

| Problem | Example |
|---------|---------|
| Duplicate rows | 15 repeated orders |
| Inconsistent text | `DELHI`, ` mumbai `, `Bangalore` vs `Bengaluru` |
| Numbers stored as text | `"Rs. 1200"` |
| Invalid dates | `"not available"` |
| Missing values | `quantity`, `discount_pct`, `rating` |
| Impossible values | Negative price, rating of 99 |
| Outliers | Quantity of 500 |

---

## 7. Cleaning Steps

1. **Removed duplicates** using `drop_duplicates()`.
2. **Standardized text** using `str.strip()`, `str.title()` and `replace()`.
3. **Converted price to numeric** by removing `Rs.` with regex and using `pd.to_numeric()`.
4. **Converted dates** with `pd.to_datetime(errors="coerce")`.
5. **Removed invalid values**: negative prices were dropped, and ratings outside 1 to 5 were set to NaN.
6. **Handled outliers** with the IQR method (values above Q3 + 1.5 x IQR were capped).
7. **Filled missing values**:
   - `quantity`: median
   - `discount_pct`: 0 (no information means no discount)
   - `rating`: median of its category
   - `order_date`: rows dropped (a date cannot be guessed)
8. **Fixed data types** (quantity and rating converted to integers).
9. **Created new columns**: `total_amount`, `month`, `order_size`.

**Result:** 515 raw rows became 492 clean rows.

---

## 8. Analysis Performed

- Total revenue, average, median and standard deviation of order value
- Revenue by category
- Revenue by city
- Monthly revenue trend (best and worst month)
- Average rating by category
- Top 5 biggest orders
- Order size distribution (Small, Medium, Large)
- Pivot table of city vs category
- Correlation matrix

---

## 9. Key Findings

1. **Electronics** brings in the most revenue because of its high unit price.
2. **Mumbai** is the top city by revenue.
3. **January** is the best month and **September** is the weakest.
4. `unit_price` has a strong correlation (about 0.88) with `total_amount`, while `rating` and `discount_pct` have almost none.
5. Most orders (about 64%) are small, but large orders contribute a big share of revenue.

> The dataset is synthetic (randomly generated), so these results are for learning purposes only.

---

## 10. Conclusion and Recommendations

- Focus marketing on the top category (Electronics) and the top cities.
- Run offers or campaigns in the weakest month to boost sales.
- Improve quality in low-rated categories (Books, Clothing).
- Collect cleaner data in future (use dropdowns for city and category, validate rating and price) to avoid cleaning problems.

---

## 11. Concepts Learned

- Inspecting data with `head()`, `info()`, `dtypes`, `isnull()`
- Handling duplicates, missing values, wrong types and outliers
- `groupby`, `pivot_table`, `value_counts`, `nlargest`
- Vectorized operations and `np.where` for conditional columns
- Correlation and basic statistics

---

## 12. Author

**Name:** Ayush Singh
**Course:** Data Analysis
**ADD NO.:** 2026B01011011

